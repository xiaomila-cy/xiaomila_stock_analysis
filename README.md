# 金叉 · A股分析框架

> 面向 AI Agent 的 A 股投资分析 Skill —— 从「问一句」到「投资建议」的全流程自动化

<img width="879" height="1155" alt="image" src="https://github.com/user-attachments/assets/7e79ef07-97e4-4b02-aa8c-7eda5480b3a8" />

---

## 📂 目录结构

```
xiaomila_stock_analysis/
├── SKILL.md                    ← 入口：触发条件、执行步骤、9条铁律
├── README.md
├── references/
│   ├── framework.md            ← 核心：完整分析框架（§一~§十三）
│   └── h5-template.md          ← H5 输出模板（CSS + 结构规范）
└── scripts/
    ├── fetch_quote.py          ← 实时行情（腾讯 API qt.gtimg.cn）
    ├── fetch_kline.py          ← K线 + MA 计算（250日）
    ├── fetch_finance.py        ← 财务数据（东财 F10 浏览器提取）
    ├── fetch_holders.py        ← 十大股东 + 基金持仓
    ├── fetch_fund_flow.py      ← 北向资金 + 融资融券
    └── fetch_announce.py       ← 公告列表（巨潮资讯网）
```

---

## 是什么

金叉是一套完整的 A 股分析工作流，让 AI Agent 像专业分析师一样工作：

📊 **数据采集**：腾讯行情 API · 东方财富数据 · 机构研报 · 商品现货价格

🔬 **分析框架**：宏观→产业→市场三层 + 个股四维（市场/财务/资源/估值）

📋 **输出模板**：行业全景报告 · 多股对比 · 评分信号 · 分层配置

---

## 安装使用

### Hermes Agent

```bash
hermes skills install https://github.com/xiaomila-cy/xiaomila_stock_analysis/blob/main/SKILL.md
```

### 手动安装

```bash
git clone https://github.com/xiaomila-cy/xiaomila_stock_analysis.git
cp -r xiaomila_stock_analysis ~/.hermes/skills/finance/
```

### 其他 AI Agent

将 `SKILL.md` 和 `references/framework.md` 内容粘贴到你的 Agent 的系统提示词或 Skills 目录。

---

## 分析体系总览

```
触发场景 → 四种分析模式自动匹配
数据采集 → 6 个脚本覆盖 6 类数据源
分析层   → 行业三维 + 个股四维
排名层   → 6 维度矩阵 + 分层配置
输出层   → H5 报告模板
```

---

## 适用场景

| 用户输入 | 触发模式 |
|---------|---------|
| "分析下 XX 股票" | 个股深度分析 |
| "XX 行业怎么看" | 行业全景分析 |
| "这三只哪个好" | 多股对比分析 |
| "最近 XX 跌了好多" | 事件驱动分析 |

---

## 执行原则

1. 所有行情数据从腾讯 API 实时拉取，不编造、不记忆
2. 政策消息先验证再引用，用 ✅/❌ 标记真伪
3. 同板块至少横评 5 只以上，不孤立看一只
4. PE 必须同业对比，不跨行业比
5. 每次分析必须给明确结论，不模棱两可

---

## 许可证

MIT License
