# 金叉 · A股分析框架

> 一个面向 AI Agent 的 A 股投资分析 Skill
>
> <img width="879" height="1155" alt="image" src="https://github.com/user-attachments/assets/7e79ef07-97e4-4b02-aa8c-7eda5480b3a8" />


## 这是什么

金叉是一套完整的 A 股分析工作流，定义了从「用户问一句」到「给出投资建议」的全过程：

- 📊 **数据采集**：腾讯行情 API、东方财富数据、机构研报
- 🔬 **分析框架**：宏观→产业→市场三层 + 个股四维（市场/财务/资源/估值）
- 📋 **输出模板**：行业全景 + 多股对比 + 评分信号系统

## 适用场景

- "分析下 XX 股票" → 个股深度分析
- "XX 行业怎么看" → 行业全景分析  
- "这三只哪个好" → 多股对比分析
- "最近 XX 跌了好多" → 事件驱动分析

## 使用方式

### Hermes Agent

```bash
hermes skills install git地址


### 其他 Agent

将 `SKILL.md` 内容粘贴到你的 Agent 的系统提示词或 Skills 目录中。

## 许可证

MIT
