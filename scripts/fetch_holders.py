#!/usr/bin/env python3
"""
fetch_holders.py — 股东/基金持仓数据提取指令
用法: python3 fetch_holders.py 600519
输出: 浏览提取指令，按指令用browser工具获取数据
"""

import sys, json

def generate(code: str) -> dict:
    market = 'sh' if code.startswith(('6','9')) else 'sz'
    return {
        'success': True,
        'script': 'fetch_holders',
        'code': code,
        'type': 'browser_extraction',
        'steps': [
            {
                'what': '十大股东',
                'url': f'https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={market}{code}&color=r#/sdgd',
                'js': "JSON.stringify(Array.from(document.querySelectorAll('table tr')).slice(0,12).map(r=>Array.from(r.querySelectorAll('td,th')).map(c=>c.textContent?.trim())))",
                '降级': f'browser_navigate后执行browser_snapshot(full=true)，手动提取前十大股东表格'
            },
            {
                'what': '基金持仓',
                'url': f'https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={market}{code}&color=r#/jjcg',
                'js': "JSON.stringify(Array.from(document.querySelectorAll('table tr')).slice(0,15).map(r=>Array.from(r.querySelectorAll('td,th')).map(c=>c.textContent?.trim())))",
                '降级': f'同样用browser_snapshot提取基金持仓变化趋势'
            },
        ]
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': 'Usage: fetch_holders.py CODE'}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(generate(sys.argv[1]), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
