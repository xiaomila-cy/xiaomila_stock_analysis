#!/usr/bin/env python3
"""
fetch_fund_flow.py — 资金流向数据提取指令
用法: python3 fetch_fund_flow.py 600519
"""

import sys, json

def generate(code: str) -> dict:
    market = 'sh' if code.startswith(('6','9')) else 'sz'
    return {
        'success': True,
        'script': 'fetch_fund_flow',
        'code': code,
        'type': 'browser_extraction',
        'steps': [
            {
                'what': '北向资金（沪深港通）',
                'url': f'https://data.eastmoney.com/hsgtcg/StockHdDetail.aspx?stock={market}{code}',
                'js': "(()=>{const r={};const t=document.querySelectorAll('table tr');t.forEach(tr=>{const c=tr.querySelectorAll('td,th');if(c.length>=2){const k=c[0].textContent?.trim();const v=c[1]?.textContent?.trim();if(k&&v)r[k]=v}});return JSON.stringify(r)})()",
                '降级': f'browser_navigate 后 browser_snapshot(full=true)，提取北向持股比例/近1月净流入趋势'
            },
            {
                'what': '融资融券',
                'url': f'https://data.eastmoney.com/rzrq/detail/{code}.html',
                'js': "(()=>{const r={};document.querySelectorAll('table tr').forEach(tr=>{const c=tr.querySelectorAll('td,th');if(c.length>=2)r[c[0].textContent?.trim()]=c[1]?.textContent?.trim()});return JSON.stringify(r)})()",
                '降级': '同上，提取融资余额/融券余额/环比变化'
            },
        ],
        'note': '资金流向数据为日频更新，分析时标注数据截止日期'
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': 'Usage: fetch_fund_flow.py CODE'}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(generate(sys.argv[1]), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
