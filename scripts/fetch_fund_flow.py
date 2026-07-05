#!/usr/bin/env python3
"""拉取北向资金 + 融资融券 — 东方财富数据中心"""
import sys, subprocess, json

def fetch_north_fund(code):
    """北向资金持仓"""
    secid = f"0.{code}" if code.startswith("0") else f"1.{code}"
    raw = subprocess.check_output(
        f"curl -s 'https://push2his.eastmoney.com/api/qt/stock/hsgt/hq?secid={secid}&fields=f2,f3,f4,f12,f14'",
        shell=True
    ).decode()
    return json.loads(raw)

def fetch_margin(code):
    """融资融券余额"""
    secid = f"0.{code}" if code.startswith("0") else f"1.{code}"
    raw = subprocess.check_output(
        f"curl -s 'https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f117,f118,f46,f44,f45'",
        shell=True
    ).decode()
    data = json.loads(raw).get("data", {})
    return {
        "margin_balance": data.get("f117", 0),  # 融资余额
        "short_balance": data.get("f118", 0),   # 融券余额
    }

if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "002460"
    north = fetch_north_fund(code)
    margin = fetch_margin(code)
    print(json.dumps({"north": north, "margin": margin}, ensure_ascii=False, indent=2))
