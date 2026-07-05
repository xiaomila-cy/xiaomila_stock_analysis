# 金叉 · stock-analysis-framework

A股个股深度分析标准化框架。12个分析模块 + 三视角交叉验证 + 行业权重调节 + 脚本驱动的数据采集。

## 核心能力

- **8段基础分析**：基本面（含管理层画像）→ 财务（含ROA同业排名）→ 估值（横向PK）→ 行情（四段折线图+极端行情诊断）→ 热点（含资金流向）→ 行业政策（含研报PK+ESG）→ 预期差 → 综合评分
- **三视角交叉验证**：多头/空头/审计三立场独立分析，量化置信度，修正最终评分
- **行业权重调节**：周期/成长/消费/金融/ST五类行业差异化评分
- **特殊标的适配**：ST股（退市风险+摘帽核查）/ 亏损股（PB估值替代）/ 次新股 / 周期股
- **7条铁律**：数据来源红线、溯源标注、时效性、利益相关、可比公司、交叉验证、数据缺失透明化

## 目录结构

```
stock-analysis-framework/
├── SKILL.md                    # Skill入口：触发/铁律/执行步骤/输出规范
├── references/
│   ├── framework.md            # §一~§十二 完整分析框架
│   └── h5-template.md          # H5输出模板（暗色金融终端）
├── scripts/
│   ├── fetch_quote.py          # 腾讯行情API（纯curl）
│   ├── fetch_kline.py          # 历史K线+MA（纯curl）
│   ├── fetch_finance.py        # 东财F10财务提取指令
│   ├── fetch_holders.py        # 股东/基金持仓提取指令
│   ├── fetch_fund_flow.py      # 北向/融资流向提取指令
│   └── fetch_announce.py       # 巨潮公告检索指令
└── README.md
```

## 输出产物

- Markdown 结构化分析全文
- 暗色金融终端风格 H5 页面
- 每条分析开头标识：`📋 分析框架：金叉 v2.3.1 | stock-analysis-framework`

## 数据源

| 类型 | 首选 | 降级 |
|------|------|------|
| 行情/K线 | 腾讯API `qt.gtimg.cn` | 东财个股页浏览器提取 |
| 财务/股东 | 东财F10 | 巨潮资讯网年报原文 |
| 政策 | 东财搜索 + 政府官网 | — |
| 研报 | 东财研报中心 | 券商官网 |
| 公告 | 巨潮资讯网 | 交易所官网 |
| 资金流向 | 东财数据中心 | 同花顺公开数据 |

## 快速开始

```bash
# 拉行情
python3 scripts/fetch_quote.py 600519

# 拉K线
python3 scripts/fetch_kline.py 600519 --days=250

# 完整分析流程见 SKILL.md → 执行步骤
```

## 版本

**v2.3.1** — 对齐 hermes-agent-skill-authoring 标准。此前 v2.3 完成11项综合优化+极端行情诊断+行业权重+特殊标的适配+6个数据采集脚本。
