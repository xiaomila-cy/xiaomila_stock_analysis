#!/usr/bin/env python3
"""
fetch_kline.py — 历史K线数据采集（ifzq API）
用法: python3 fetch_kline.py 600519 [--days 250]
输出: JSON，包含日期/开/高/低/收/量数组
"""

import sys, json, subprocess, re
from datetime import datetime

def fetch_kline(code: str, days: int = 250) -> dict | None:
    """拉取历史日K线"""
    if code.startswith(('6', '9')):
        full = f'sh{code}'
    else:
        full = f'sz{code}'

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

        records = []
        for row in klines:
            records.append({
                'date': row[0],
                'open': float(row[1]),
                'close': float(row[2]),
                'high': float(row[3]),
                'low': float(row[4]),
                'volume': int(float(row[5])) if len(row) > 5 and row[5] else 0,
            })

        return {
            'code': code,
            'full_code': full,
            'days_requested': days,
            'records_returned': len(records),
            'from_date': records[0]['date'] if records else None,
            'to_date': records[-1]['date'] if records else None,
            'klines': records,
        }
    except Exception as e:
        return None


def main():
    args = sys.argv[1:]
    code = None
    days = 250
    full_output = False

    for a in args:
        if a.startswith('--days='):
            days = int(a.split('=')[1])
        elif a == '--full':
            full_output = True
        elif not a.startswith('--'):
            code = a

    if not code:
        print(json.dumps({'success': False, 'error': 'Usage: fetch_kline.py CODE [--days=250]'}, ensure_ascii=False))
        sys.exit(1)

    data = fetch_kline(code.strip(), days)
    if data:
        # 为了减少输出体积，默认不打印全部klines，加--full才输出
        if full_output:
            output = {'success': True, 'data': data}
        else:
            summary = {k: v for k, v in data.items() if k != 'klines'}
            # 最近5条+首尾关键位
            if data['klines']:
                summary['latest_5'] = data['klines'][-5:]
                summary['first_5'] = data['klines'][:5]
                # 计算关键统计
                closes = [r['close'] for r in data['klines']]
                summary['stats'] = {
                    'max_close': max(closes),
                    'min_close': min(closes),
                    'latest_close': closes[-1],
                    'ma20': round(sum(closes[-20:]) / min(20, len(closes)), 2),
                    'ma60': round(sum(closes[-60:]) / min(60, len(closes)), 2),
                }
            output = {'success': True, 'data': summary}
    else:
        output = {'success': False, 'data': None, 'error': f'Failed to fetch kline for {code}'}

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
