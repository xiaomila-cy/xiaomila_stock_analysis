#!/usr/bin/env python3
"""
fetch_finance.py — 东财F10财务数据提取指令
用法: python3 fetch_finance.py 600519
输出: 结构化提取指令JSON，Agent按指令使用browser工具提取
"""

import sys, json

def generate_instructions(code: str) -> dict:
    """生成东财F10财务数据提取指令"""
    market = 'sh' if code.startswith(('6','9')) else 'sz'
    f10_url = f'https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={market}{code}&color=r#/cwfx'

    return {
        'success': True,
        'script': 'fetch_finance',
        'code': code,
        'type': 'browser_extraction',
        'instructions': {
            'step1': {
                'action': 'browser_navigate',
                'url': f10_url,
                'note': '东财F10-财务分析页'
            },
            'step2': {
                'action': 'browser_console',
                'note': '等待页面加载完成（约3秒），执行以下JS提取核心财务数据',
                'js': '''
// 提取财务数据
const result = {};
// 关键指标
const items = document.querySelectorAll('.cwzb-item');
items.forEach(item => {
    const label = item.querySelector('.name')?.textContent?.trim();
    const value = item.querySelector('.number')?.textContent?.trim();
    if (label && value) result[label] = value;
});
// 如果有利润表/资产负债表表格，尝试提取
const tables = document.querySelectorAll('table');
tables.forEach((t, i) => {
    const rows = t.querySelectorAll('tr');
    const data = [];
    rows.forEach(r => {
        const cells = r.querySelectorAll('td,th');
        data.push(Array.from(cells).map(c => c.textContent?.trim()));
    });
    if (data.length > 2) result[`table_${i}`] = data;
});
return JSON.stringify(result, null, 2);
'''
            },
            'step3': {
                'action': 'terminal',
                'command': f'python3 ~/.hermes/profiles/stock-expert/skills/finance/stock-analysis-framework/scripts/fetch_finance.py {code} --parse "<PASTE_EXTRACTED_JSON_HERE>"',
                'note': '将browser_console返回的JSON粘贴到--parse参数中，脚本自动格式化输出'
            }
        },
        '降级方案': {
            'url': f'https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={market}{code}&color=r#/cwfx',
            'note': '如果browser_console提取失败，改为browser_snapshot(full=true)获取页面全文，手动提取关键指标'
        }
    }


def parse_extracted(data_str: str) -> dict:
    """解析从浏览器提取的原始JSON，格式化为标准财务数据"""
    try:
        raw = json.loads(data_str)
    except json.JSONDecodeError:
        return {'success': False, 'error': 'Invalid JSON input'}

    # 从原始数据中提取关键指标
    result = {
        'success': True,
        'data': {
            'raw': raw,
            'key_metrics': {},
            'note': '提取自东财F10财务分析页，需人工核对数值准确性'
        }
    }

    # 常见指标映射
    key_map = {
        '营业总收入': 'revenue',
        '营业收入': 'revenue',
        '归母净利润': 'net_profit_attr',
        '归属于母公司所有者的净利润': 'net_profit_attr',
        '扣非净利润': 'net_profit_deduct',
        '毛利率': 'gross_margin',
        '净利率': 'net_margin',
        'ROE': 'roe',
        '净资产收益率': 'roe',
        '资产负债率': 'debt_ratio',
        '基本每股收益': 'eps',
    }

    for cn_name, en_name in key_map.items():
        if cn_name in raw:
            result['data']['key_metrics'][en_name] = raw[cn_name]

    return result


def main():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({'success': False, 'error': 'Usage: fetch_finance.py CODE [--parse JSON]'}, ensure_ascii=False))
        sys.exit(1)

    if '--parse' in args:
        idx = args.index('--parse')
        data_str = ' '.join(args[idx+1:])
        result = parse_extracted(data_str)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    code = args[0]
    instructions = generate_instructions(code)
    print(json.dumps(instructions, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
