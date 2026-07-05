#!/usr/bin/env python3
"""拉取腾讯股票行情 API — qt.gtimg.cn"""
import sys, subprocess, json

def fetch_quote(codes):
    """拉取实时行情，返回 dict"""
    q = ",".join(codes)
    raw = subprocess.check_output(
        f"curl -s 'https://qt.gtimg.cn/q={q}' | iconv -f GBK -t UTF-8",
        shell=True
    ).decode()
    
    results = {}
    for line in raw.strip().split("\n"):
        if not line.startswith("v_"): continue
        # v_sz002460="1~赣锋锂业~002460~..."
        parts = line.split("~")
        code = parts[2]
        results[code] = {
            "name": parts[1],
            "price": float(parts[3]),
            "prev_close": float(parts[4]),
            "open": float(parts[5]),
            "volume": float(parts[6]),
            "change_pct": float(parts[32]),
            "high": float(parts[33]),
            "low": float(parts[34]),
            "turnover": float(parts[38]) if len(parts) > 38 else 0,
            "pe": float(parts[39]) if len(parts) > 39 else 0,
            "amplitude": float(parts[43]) if len(parts) > 43 else 0,
            "market_cap": float(parts[44]) if len(parts) > 44 else 0,
        }
    return results

if __name__ == "__main__":
    codes = sys.argv[1:] if len(sys.argv) > 1 else ["sz002460"]
    data = fetch_quote(codes)
    print(json.dumps(data, ensure_ascii=False, indent=2))
