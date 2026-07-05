#!/usr/bin/env python3
"""提取东方财富 F10 财务数据（需 browser_console 环境）"""
import sys, json

# 此脚本通过 browser_console 执行，提取 __NEXT_DATA__
# 用法：browser_navigate → browser_console 执行 → 返回 JSON

JS_CODE = """
(function() {
  var data = JSON.parse(document.getElementById('__NEXT_DATA__').textContent);
  var props = data.props.pageProps;
  return JSON.stringify({
    code: props.code,
    name: props.name,
    main: props.data?.main || [],
    debt: props.data?.debt || [],
    profit: props.data?.profit || [],
    growth: props.data?.growth || []
  });
})()
"""

if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "002460"
    url = f"https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={code}&color=r#/cwfx"
    print(f"1. browser_navigate('{url}')")
    print(f"2. browser_console 执行提取脚本")
    print(f"\n提取脚本:\n{JS_CODE}")
