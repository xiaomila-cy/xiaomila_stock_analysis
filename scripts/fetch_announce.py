#!/usr/bin/env python3
"""拉取巨潮资讯网公告列表"""
import sys

JS_CODE = """
(function() {
  var rows = document.querySelectorAll('table tbody tr');
  var result = [];
  rows.forEach(function(row) {
    var cells = row.querySelectorAll('td');
    if (cells.length >= 3) {
      var link = cells[0].querySelector('a');
      result.push({
        date: cells[0].textContent.trim().split('\\n')[0],
        title: link ? link.textContent.trim() : cells[1].textContent.trim(),
        url: link ? link.href : '',
        type: cells.length > 2 ? cells[2].textContent.trim() : ''
      });
    }
  });
  return JSON.stringify(result.slice(0, 20));
})()
"""

if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "002460"
    url = f"http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice&stockCode={code}&pageSize=30&pageNum=1"
    print(f"1. browser_navigate('{url}')")
    print(f"2. browser_console 执行提取脚本")
    print(f"\n提取脚本:\n{JS_CODE}")
