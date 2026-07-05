#!/usr/bin/env python3
"""拉取历史K线 + MA均线 — 腾讯前复权日线"""
import sys, subprocess, json

def fetch_kline(code, days=250):
    """拉取前复权日K线，返回 [{date,open,close,high,low,volume,ma20}]"""
    raw = subprocess.check_output(
        f"curl -s 'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={code},day,,,{days},qfq'",
        shell=True
    ).decode()
    
    import re
    # 提取 JSON 部分
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match: return []
    data = json.loads(match.group())
    
    klines = data.get("data", {}).get(code, {}).get("qfqday", [])
    if not klines and "day" in data.get("data", {}).get(code, {}):
        klines = data["data"][code]["day"]
    
    result = []
    for row in klines:
        if len(row) < 6: continue
        result.append({
            "date": row[0],
            "open": float(row[1]),
            "close": float(row[2]),
            "high": float(row[3]),
            "low": float(row[4]),
            "volume": float(row[5]),
        })
    
    # 计算 MA20
    for i in range(len(result)):
        if i >= 19:
            ma20 = sum(r["close"] for r in result[i-19:i+1]) / 20
            result[i]["ma20"] = round(ma20, 2)
    
    return result

if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "sz002460"
    data = fetch_kline(code)
    print(json.dumps(data[-5:], ensure_ascii=False, indent=2))
    print(f"\n总条数: {len(data)}")
