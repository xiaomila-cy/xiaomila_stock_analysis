#!/usr/bin/env python3
"""
fetch_announce.py — 公告检索指令
用法: python3 fetch_announce.py 600519 [--keyword 减持] [--days 30]
"""

import sys, json
from datetime import datetime, timedelta

def generate(code: str, keyword: str = None, days: int = 30) -> dict:
    market = 'sh' if code.startswith(('6','9')) else 'sz'
    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    kw_param = f'&keyword={keyword}' if keyword else ''

    return {
        'success': True,
        'script': 'fetch_announce',
        'code': code,
        'type': 'browser_extraction',
        'period': f'{start} ~ {end} ({days}天)',
        'keyword': keyword,
        'steps': [
            {
                'what': '巨潮资讯网公告检索',
                'url': f'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord={code}&maxSecLevel=& industry=&tradeType=&publishDateS={start}&publishDateE={end}&pageNum=1&pageSize=20{kw_param}&stockCodeSelBox=1',
                'js': "JSON.stringify(Array.from(document.querySelectorAll('.tuiwen-list li, table tr')).slice(0,20).map(r=>({text:r.textContent?.trim()?.substring(0,200), link:r.querySelector('a')?.href})))",
                '降级': 'browser_navigate + browser_snapshot，手动提取公告标题、日期、类型'
            },
            {
                'what': '东方财富个股公告（备选）',
                'url': f'https://data.eastmoney.com/notices/detail/{code}.html',
                '降级': '同上'
            }
        ],
        'note': '优先巨潮（官方），东财为降级方案。公告按时间倒序排列。'
    }


def main():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({'success': False, 'error': 'Usage: fetch_announce.py CODE [--keyword KEYWORD] [--days 30]'}, ensure_ascii=False))
        sys.exit(1)

    code = args[0]
    keyword = None
    days = 30

    i = 1
    while i < len(args):
        if args[i] == '--keyword' and i + 1 < len(args):
            keyword = args[i + 1]
            i += 2
        elif args[i].startswith('--days='):
            days = int(args[i].split('=')[1])
            i += 1
        else:
            i += 1

    print(json.dumps(generate(code, keyword, days), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
