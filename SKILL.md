---
name: golden-cross-stock-analysis
description: Use when the user asks to analyze Chinese A-share stocks (个股分析), industries (行业分析), or compare multiple stocks (多股对比). Provides a complete framework covering data collection, fundamental analysis, industry landscape, valuation, and ranking. Covers resource stocks, cyclical sectors, and event-driven analysis.
version: 1.0.0
author: 小米辣 (Hermes Agent)
license: MIT
tags: [stock, a-share, finance, investment, analysis, industry, china]
---

# 金叉 · A股分析框架

> 完整工作流：给你一个股票或行业，知道拉什么数据、做什么分析、输出什么结构。

## 触发场景

- "分析下XX股票" → 个股深度分析（见 `references/individual-analysis.md`）
- "XX行业怎么看" → 行业全景分析（见 `references/industry-analysis.md`）
- "这三只哪个好" → 多股对比分析（见 `references/stock-comparison.md`）
- "最近XX跌了好多" → 事件驱动分析（先查跌因，再判断错杀还是基本面恶化）

## 工作流

### Step 1：数据采集

按需拉取以下数据源，详见 `references/data-sources.md`：

1. **行情数据** — 腾讯 `qt.gtimg.cn` API
2. **商品现货价格** — 东方财富搜索 + Mysteel/生意社
3. **政策消息验证** — 拆分陈述 → 原文对照 → ✅/❌ 标记
4. **财务数据** — 东方财富 F10
5. **机构研报** — 供需平衡表 + 价格预测
6. **历史K线** — 前复权日线，120条

### Step 2：分析

根据触发场景选择分析维度：

- **行业分析**：宏观层 → 产业层 → 市场层（三维）
- **个股分析**：市场面 → 财务面 → 资源面 → 估值面（四维）

详见 `references/analysis-dimensions.md`

### Step 3：排名与对比

同板块至少横评5-8只，6维度排名矩阵：
长期投资价值 · 周期弹性 · 抗周期能力 · 成本优势 · 资源安全性 · 估值修复空间

### Step 4：输出

见 `templates/` 目录：
- `templates/industry-report.md` — 行业全景报告模板
- `templates/stock-comparison.md` — 多股对比模板

## 评分信号

| 信号 | 标记 | 含义 |
|------|------|------|
| 强烈推荐 | 🟢 首选 | 基本面+估值+技术面多重共振 |
| 关注观察 | 🟡 次选 | 逻辑成立但有瑕疵 |
| 谨慎参与 | 🔴 回避 | 基本面有硬伤或纯博弈 |
| 防守配置 | 🛡️ | 低估值+高安全边际 |
| 弹性博弈 | 🎯 | 小市值+高波动+超跌 |

## 铁律

1. 所有行情数据从腾讯API实时拉取，不编造、不记忆
2. 政策消息先验证再引用，用 ✅/❌ 标记真伪
3. 同板块至少横评5只以上，不孤立看一只
4. PE必须同业对比，不能跨行业比
5. 亏损股标"亏损"，不参与PE排名
6. 每次分析必须给明确结论
