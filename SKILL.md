---
name: golden-cross-stock-analysis
description: Use when the user asks to analyze Chinese A-share stocks (个股分析), industries (行业分析), or compare multiple stocks (多股对比). Provides a complete framework covering data collection, fundamental analysis, industry landscape, valuation, and ranking. Covers resource stocks, cyclical sectors, and event-driven analysis.
version: 1.0.0
author: 金叉 · 小米辣
license: MIT
tags: [stock, a-share, finance, investment, analysis, industry]
---

# 金叉 · A股分析框架

完整工作流：触发 → 数据采集 → 分析 → 排名 → 输出。

## 触发场景

| 用户输入 | 触发模式 | 加载参考 |
|---------|---------|---------|
| "分析下XX股票" | 个股深度 | `references/framework.md` §八 |
| "XX行业怎么看" | 行业全景 | `references/framework.md` §七 |
| "这三只哪个好" | 多股对比 | `references/framework.md` §九 |
| "最近XX跌了好多" | 事件驱动 | `references/framework.md` §十 |

## 执行步骤

### 1. 数据采集

按需使用 `scripts/` 下的工具：

脚本 | 用途 | 用法
---|---|---
`fetch_quote.py` | 实时行情 | `python3 fetch_quote.py sz002460`
`fetch_kline.py` | K线+MA | `python3 fetch_kline.py sz002460`
`fetch_finance.py` | 财务数据 | `python3 fetch_finance.py 002460`
`fetch_holders.py` | 十大股东 | `python3 fetch_holders.py 002460`
`fetch_fund_flow.py` | 北向/融资融券 | `python3 fetch_fund_flow.py 002460`
`fetch_announce.py` | 公告列表 | `python3 fetch_announce.py 002460`

详细 API 说明见 `references/framework.md` §二~§五。

### 2. 分析

根据触发模式选择分析维度（见 `references/framework.md`）：

- **行业全景**：宏观层→产业层→市场层（§七）
- **个股深度**：市场面→财务面→资源面→估值面（§八）
- **多股对比**：六维排名矩阵（§九）

### 3. 输出

按 `references/h5-template.md` 生成 H5 报告，结构见 `references/framework.md` §十一~§十二。

## 9 条铁律

1. 所有行情数据从腾讯 API 实时拉取，不编造、不记忆
2. 政策消息先验证再引用，用 ✅/❌ 标记真伪
3. 同板块至少横评 5 只以上，不孤立看一只
4. PE 必须同业对比，不跨行业比
5. 亏损股标"亏损"，不参与 PE 排名
6. 每次分析必须给明确结论，不模棱两可
7. 结论说明：什么风格的投资者适合什么标的
8. 商品价格使用 GP-A 定位法提取周期涨跌幅
9. 表单数据以腾讯 API 为准，东财 F10 为辅

## Pitfalls

- 腾讯 API 返回 GBK 编码，需 `iconv -f GBK -t UTF-8`
- 东方财富 F10 页面含大量 JS 渲染，用 `browser_console` 提取 `__NEXT_DATA__`
- PE 为负时标注"亏损"而非显示负数
- 跨行业对比 PE 无意义（银行 vs 锂矿）
- 盈亏切换的票需要特别标注
- 深市用 `sz` 前缀，沪市用 `sh` 前缀
