#!/usr/bin/env python3
"""提取十大股东 + 基金持仓 — 东方财富 F10 浏览器提取"""
import sys

JS_CODE = """
(function() {
  var rows = document.querySelectorAll('.shareholder-table tr, .gd_table tr');
  var result = [];
  rows.forEach(function(row) {
    var cells = row.querySelectorAll('td, th');
    if (cells.length >= 3) {
      result.push({
        name: cells[0].textContent.trim(),
        shares: cells[1].textContent.trim(),
        ratio: cells[2].textContent.trim(),
        change: cells.length > 3 ? cells[3].textContent.trim() : ''
      });
    }
  });
  return JSON.stringify(result);
})()
"""

if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "002460"
    url = f"https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={code}&color=r#/sdgd"
    print(f"1. browser_navigate('{url}')")
    print(f"2. 等待页面加载，执行提取脚本")
    print(f"\n提取脚本:\n{JS_CODE}")
