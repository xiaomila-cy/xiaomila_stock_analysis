#!/usr/bin/env python3
"""
fetch_quote.py — 腾讯行情API采集（v2.0 含K线交叉验证）
用法: python3 fetch_quote.py 600519
      python3 fetch_quote.py 600519 --cross-check    # 启用K线交叉验证（推荐）
      python3 fetch_quote.py --batch 600519,000858,601899 --cross-check
输出: JSON到stdout
"""
import sys, json, subprocess, re
from datetime import datetime, timedelta


def _resolve_full_code(code: str) -> str:
    """解析股票代码 → 腾讯前缀"""
    if code.startswith(('6', '9')):
        return f'sh{code}'
    elif code.startswith(('0', '3', '2')):
        return f'sz{code}'
    return code


def fetch_one(code: str) -> dict | None:
    """拉取单只股票行情"""
    full = _resolve_full_code(code)
    url = f'http://qt.gtimg.cn/q={full}'
    try:
        result = subprocess.run(
            ['curl', '-s', '--connect-timeout', '5', '--max-time', '10', url],
            capture_output=True, timeout=15
        )
        raw_bytes = result.stdout
        if not raw_bytes:
            return None

        decoded = subprocess.run(
            ['iconv', '-f', 'GBK', '-t', 'UTF-8'],
            input=raw_bytes, capture_output=True, timeout=5
        ).stdout.decode('utf-8', errors='replace')

        if not decoded:
            return None

        m = re.search(r'v_[a-z]+\d+="(.*?)"', decoded)
        if not m:
            return None

        fields = m.group(1).split('~')
        if len(fields) < 45:
            return None

        def f(i, default=0.0):
            try:
                return float(fields[i]) if fields[i] else default
            except (ValueError, IndexError):
                return default

        def fs(i, default=''):
            try:
                return fields[i] if fields[i] else default
            except IndexError:
                return default

        return {
            'code': code,
            'full_code': full,
            'name': fs(1),
            'price': f(3),
            'prev_close': f(4),
            'open': f(5),
            'volume_hands': int(f(6)) if fs(6) else 0,
            'change_amount': f(31),
            'change_pct': f(32),
            'high': f(33),
            'low': f(34),
            'turnover_rate': f(38),
            'pe_ttm': f(39),
            'amplitude': f(43),
            'total_market_cap': f(45) if len(fields) > 45 else 0,
            'circulating_market_cap': f(44),
            'pb': f(46) if len(fields) > 46 else 0,
            'timestamp': fs(30),
            'gp_a_month': f(62),
            'gp_a_3month': f(63),
            'gp_a_6month': f(64),
            'gp_a_year': f(65),
        }
    except Exception:
        return None


def _fetch_kline_raw(code: str, days: int = 300) -> list | None:
    """
    拉取原始K线数据（ifzq API），返回 [日期, 开, 收, 高, 低, 量] 的列表。
    与 fetch_kline.py 使用同一数据源，保证一致性。
    """
    full = _resolve_full_code(code)
    url = f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={full},day,,,{days},qfq'
    try:
        result = subprocess.run(
            ['curl', '-s', '--connect-timeout', '5', '--max-time', '10', url],
            capture_output=True, timeout=15
        )
        data = json.loads(result.stdout)
        stock_data = data.get('data', {}).get(full, {})
        klines = stock_data.get('qfqday', stock_data.get('day', []))
        if not klines:
            return None
        return klines
    except Exception:
        return None


def cross_check_period_returns(code: str, api_values: dict) -> dict:
    """
    用K线数据独立计算周期涨跌幅，与腾讯API GP-A交叉验证。

    api_values: {'gp_a_month': float, 'gp_a_3month': float, ...}
    返回:
    {
      'status': 'pass' | 'fail' | 'unverified',
      'checks': {周期: {api, kline, diff, pass, base_date, base_close}},
      'corrected': {周期: float},    # status=fail时用K线值替换API值
      'summary': str                  # 人类可读的汇总
    }
    """
    PERIODS = {
        'gp_a_month':   ('近1月', timedelta(days=30)),
        'gp_a_3month':  ('近3月', timedelta(days=90)),
        'gp_a_6month':  ('近6月', timedelta(days=180)),
        'gp_a_year':    ('近1年', timedelta(days=365)),
    }
    DEVIATION_THRESHOLD = 5.0  # 偏差超过5个百分点 → 判定API异常

    klines = _fetch_kline_raw(code, days=300)
    if not klines or len(klines) < 20:
        return {
            'status': 'unverified',
            'checks': {},
            'corrected': dict(api_values),
            'summary': '⚠️ 无法获取K线数据，交叉验证跳过',
        }

    # 解析K线为 (date, close)
    records = []
    for row in klines:
        try:
            d = datetime.strptime(row[0], '%Y-%m-%d')
            records.append({'date': d, 'close': float(row[2])})
        except (ValueError, IndexError):
            continue

    if not records:
        return {
            'status': 'unverified',
            'checks': {},
            'corrected': dict(api_values),
            'summary': '⚠️ K线日期解析失败，交叉验证跳过',
        }

    latest = records[-1]
    latest_date = latest['date']
    latest_close = latest['close']

    checks = {}
    corrected = dict(api_values)
    failures = []
    all_ok = True

    for key, (label, delta) in PERIODS.items():
        target_date = latest_date - delta
        # 找最接近目标日期的K线记录
        closest = None
        min_diff = timedelta(days=9999)
        for r in records:
            diff = abs(r['date'] - target_date)
            if diff < min_diff:
                min_diff = diff
                closest = r

        if not closest or closest['close'] <= 0:
            checks[key] = {
                'label': label,
                'api': api_values.get(key, 0),
                'kline': None,
                'diff': None,
                'pass': None,
                'error': '找不到基准日期',
            }
            all_ok = False
            continue

        kline_return = round((latest_close - closest['close']) / closest['close'] * 100, 2)
        api_return = round(api_values.get(key, 0), 2)
        diff_abs = round(abs(kline_return - api_return), 2)
        passed = diff_abs <= DEVIATION_THRESHOLD

        checks[key] = {
            'label': label,
            'api': api_return,
            'kline': kline_return,
            'diff': diff_abs,
            'pass': passed,
            'base_date': closest['date'].strftime('%Y-%m-%d'),
            'base_close': round(closest['close'], 2),
            'latest_date': latest_date.strftime('%Y-%m-%d'),
            'latest_close': round(latest_close, 2),
        }

        if not passed:
            all_ok = False
            failures.append(f"{label}: API报{api_return}% 实际{kline_return}%（差{diff_abs}pp）")
            corrected[key] = kline_return

    if all_ok:
        status = 'pass'
        summary = '✅ 四段涨跌幅全部通过交叉验证（偏差<5pp）'
    else:
        status = 'fail'
        summary = f'⚠️ GP-A交叉验证失败！{len(failures)}/4个周期偏差超{DEVIATION_THRESHOLD}pp:\n  ' + '\n  '.join(failures)

    return {
        'status': status,
        'checks': checks,
        'corrected': corrected,
        'summary': summary,
    }


def main():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({
            'success': False, 'data': None,
            'error': 'Usage: fetch_quote.py CODE [CODE...] [--cross-check]'
        }, ensure_ascii=False))
        sys.exit(1)

    # 解析参数
    cross_check = False
    codes = []

    i = 0
    while i < len(args):
        a = args[i]
        if a == '--cross-check':
            cross_check = True
        elif a == '--batch':
            i += 1
            codes = [c.strip() for c in args[i].split(',')]
        elif not a.startswith('--'):
            codes.append(a)
        i += 1

    if not codes:
        print(json.dumps({'success': False, 'data': None, 'error': 'No stock codes provided'}, ensure_ascii=False))
        sys.exit(1)

    results = []
    errors = []

    for code in codes:
        data = fetch_one(code.strip())
        if data:
            # 交叉验证
            if cross_check:
                api_vals = {
                    'gp_a_month': data['gp_a_month'],
                    'gp_a_3month': data['gp_a_3month'],
                    'gp_a_6month': data['gp_a_6month'],
                    'gp_a_year': data['gp_a_year'],
                }
                cc = cross_check_period_returns(code.strip(), api_vals)
                data['gp_cross_check'] = cc
                # 如果验证失败，用K线计算值替换API原始值
                if cc['status'] == 'fail':
                    data['gp_a_month'] = cc['corrected']['gp_a_month']
                    data['gp_a_3month'] = cc['corrected']['gp_a_3month']
                    data['gp_a_6month'] = cc['corrected']['gp_a_6month']
                    data['gp_a_year'] = cc['corrected']['gp_a_year']
                    data['gp_cross_check_replaced'] = True
            results.append(data)
        else:
            errors.append(code)

    output = {
        'success': len(errors) == 0,
        'data': results if len(codes) > 1 else (results[0] if results else None),
        'count': len(results),
        'errors': errors if errors else None,
        'cross_check_enabled': cross_check,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
