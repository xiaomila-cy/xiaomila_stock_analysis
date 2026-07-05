# H5输出模板 v2.7.0 · 设计人：小米辣

当完成Markdown分析报告后，将其渲染为暗色金融终端风格的H5页面。

## 设计哲学

对标 Bloomberg Terminal / 暗色交易终端——克制、精准、信息密度高但不拥挤。字体用 `Inter`（正文）+ `JetBrains Mono`（数字/表格），配色以降饱和深色为主，金色仅用于关键标注。

## ⛔ 排版铁律

**H5板块必须按编号顺序排列：一→二→三→四→五→六→七→八→九→十→十一→十二→十三。**

## 完整CSS（直接嵌入H5，无需外部文件）

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root{
  --bg:#0b0e11;
  --card:#13171d;
  --card-hover:#181d25;
  --border:#1a1f2b;
  --t1:#e4e8ee;
  --t2:#848e9c;
  --t3:#5a6473;
  --gold:#bfa15a;
  --gold-bright:#d4b86a;
  --green:#26a69a;
  --green-bg:rgba(38,166,154,.08);
  --red:#e05555;
  --red-bg:rgba(224,85,85,.06);
  --blue:#5b9bd5;
  --blue-bg:rgba(91,155,213,.08);
  --purple:#8b7ec8;
  --orange:#d4914a;
  --radius:6px;
  --radius-lg:10px;
}

*{margin:0;padding:0;box-sizing:border-box}

body{
  background:var(--bg);
  color:var(--t1);
  font-family:'Inter',-apple-system,sans-serif;
  max-width:900px;
  margin:0 auto;
  padding:2rem 1.5rem 3rem;
  line-height:1.65;
  -webkit-font-smoothing:antialiased;
}

.page-title{
  font-size:2.2rem;
  font-weight:900;
  color:var(--gold-bright);
  letter-spacing:-.04em;
  margin-bottom:.1rem;
  line-height:1.2;
}
.page-title small{font-size:.45em;color:var(--t3);font-weight:400;margin-left:.5rem;letter-spacing:.02em}
.page-subtitle{
  font-size:.82rem;
  color:var(--t2);
  margin-bottom:1rem;
  display:flex;
  align-items:center;
  gap:.6rem;
  flex-wrap:wrap;
}
.badge{
  display:inline-flex;
  align-items:center;
  gap:4px;
  padding:2px 10px;
  border-radius:20px;
  font-size:.68rem;
  font-weight:500;
  font-family:'JetBrains Mono',monospace;
}
.badge-skill{background:var(--blue-bg);color:var(--blue);border:1px solid rgba(91,155,213,.2)}
.badge-author{background:rgba(191,161,90,.06);color:var(--gold);border:1px solid rgba(191,161,90,.15)}

.meta-bar{
  display:flex;
  gap:.4rem .8rem;
  flex-wrap:wrap;
  padding:.6rem 1rem;
  background:var(--card);
  border:1px solid var(--border);
  border-radius:var(--radius);
  font-size:.74rem;
  color:var(--t2);
  font-family:'JetBrains Mono',monospace;
  margin-bottom:1.2rem;
}
.meta-bar .ml{color:var(--t3)}
.meta-bar .mv{color:var(--t1);font-weight:500}

.exec-summary{
  background:linear-gradient(135deg,rgba(191,161,90,.07),rgba(191,161,90,.01));
  border:1px solid rgba(191,161,90,.18);
  border-radius:var(--radius-lg);
  padding:1.4rem;
  margin:1.2rem 0;
}
.exec-summary h2{
  font-size:1.2rem;
  font-weight:800;
  color:var(--t1);
  margin-bottom:1rem;
  display:flex;
  align-items:center;
  gap:.5rem;
  letter-spacing:-.02em;
}
.exec-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
  gap:.7rem;
  margin-bottom:.8rem;
}
.exec-item .lbl{font-size:.66rem;color:var(--t3);text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px}
.exec-item .val{font-size:1rem;font-weight:600;color:var(--t1)}
.exec-item .val.big{font-size:1.3rem}

.section-header{
  display:flex;
  align-items:baseline;
  gap:.7rem;
  margin:2.2rem 0 .8rem;
  padding:.6rem 0;
  border-bottom:1px solid var(--border);
}
.section-num{
  font-size:1rem;
  color:var(--gold);
  font-weight:800;
  font-family:'JetBrains Mono',monospace;
  opacity:.85;
}
.section-title{
  font-size:1.15rem;
  font-weight:800;
  color:var(--purple);
  letter-spacing:-.02em;
}
.section-num{
  font-size:1rem;
  color:var(--purple);
  font-weight:800;
  font-family:'JetBrains Mono',monospace;
  opacity:.85;
}
.section-sub{
  margin-left:auto;
  font-size:.68rem;
  color:var(--t3);
}

.card{
  background:var(--card);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:1rem 1.2rem;
  margin:.5rem 0;
  transition:border-color .2s;
}
.card:hover{border-color:#283040}
.card-sm{padding:.65rem 1rem}

.table-wrap{overflow-x:auto;margin:.6rem 0}
table{
  width:100%;
  border-collapse:collapse;
  font-size:.78rem;
}
th{
  text-align:left;
  padding:.45rem .65rem;
  font-weight:600;
  font-size:.68rem;
  color:var(--t3);
  text-transform:uppercase;
  letter-spacing:.04em;
  border-bottom:1px solid var(--border);
}
td{
  padding:.4rem .65rem;
  border-bottom:1px solid rgba(26,31,43,.5);
  color:var(--t2);
  font-family:'JetBrains Mono',monospace;
  font-size:.74rem;
}
td:first-child{font-family:'Inter',sans-serif;color:var(--t1);font-size:.78rem}
tr.row-hl{background:rgba(191,161,90,.03)}
tr.row-hl td:first-child{color:var(--gold-bright)}
tr:last-child td{border-bottom:none}

.green{color:var(--green)}
.red{color:var(--red)}
.gold{color:var(--gold)}
.ic-ok{color:var(--green);font-weight:600}
.ic-warn{color:var(--gold);font-weight:600}
.ic-bad{color:var(--red);font-weight:600}

.chart-container{
  background:var(--card);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:1rem;
  margin:.8rem 0;
}
.chart-container svg{width:100%;height:auto}
.chart-legend{
  display:flex;
  gap:1.2rem;
  justify-content:center;
  font-size:.68rem;
  color:var(--t3);
  margin-top:.4rem;
}
.legend-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px;vertical-align:middle}

.cross-grid{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:.6rem;
  margin:.5rem 0;
}
.cross-card{
  background:var(--card);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:.9rem;
  font-size:.76rem;
}
.cross-card h3{font-size:.85rem;font-weight:600;margin-bottom:.5rem}
.cross-card p{margin:.35rem 0;color:var(--t2);line-height:1.5}
.cross-card.bull{border-top:2px solid var(--blue)}
.cross-card.bear{border-top:2px solid var(--red)}
.cross-card.audit{border-top:2px solid var(--t3)}

.consensus-block{
  background:var(--card);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:.7rem 1rem;
  margin:.5rem 0;
  font-size:.78rem;
}

.score-grid{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:.6rem;
  margin:.5rem 0;
}
.score-card{
  background:var(--card);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:.8rem;
  text-align:center;
}
.score-card .dim{font-size:.66rem;color:var(--t3);text-transform:uppercase;letter-spacing:.04em}
.score-card .val{
  font-size:1.9rem;
  font-weight:800;
  color:var(--gold-bright);
  font-family:'JetBrains Mono',monospace;
  margin:.15rem 0;
  line-height:1.1;
}
.score-card .wt{font-size:.64rem;color:var(--t3)}

.final-score{
  background:linear-gradient(135deg,rgba(191,161,90,.1),rgba(191,161,90,.02));
  border:1px solid rgba(191,161,90,.25);
  border-radius:var(--radius-lg);
  padding:1.1rem;
  text-align:center;
  margin:.7rem 0;
}
.final-score .big{
  font-size:3rem;
  font-weight:900;
  color:var(--gold-bright);
  font-family:'JetBrains Mono',monospace;
  line-height:1.1;
}
.final-score .sub{font-size:.78rem;color:var(--t2);margin-top:.3rem}

.fin-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
  gap:.5rem;
  margin:.4rem 0;
}
.fin-card{
  background:var(--card);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:.6rem .8rem;
}
.fin-card .val{font-size:1.1rem;font-weight:700;font-family:'JetBrains Mono',monospace;color:var(--t1)}
.fin-card .lbl{font-size:.62rem;color:var(--t3);margin-top:2px}

.rule-box{
  background:var(--card);
  border-left:3px solid var(--gold);
  border-radius:0 var(--radius) var(--radius) 0;
  padding:.65rem .9rem;
  margin:.35rem 0;
  font-family:'JetBrains Mono',monospace;
  font-size:.72rem;
  color:var(--t2);
  line-height:1.55;
}
.rule-box.exit{border-color:var(--red)}
.rule-box .kw{color:var(--blue);font-weight:500}
.rule-box .act{color:var(--gold-bright);font-weight:500}
.rule-box .dng{color:var(--red);font-weight:500}

.news-item{
  font-size:.74rem;
  color:var(--t2);
  margin:.25rem 0;
  padding:.25rem 0 .25rem .55rem;
  border-left:2px solid var(--border);
}
.news-item .nd{color:var(--t3);font-size:.64rem;font-family:'JetBrains Mono',monospace}
.news-item:hover{border-left-color:var(--gold)}

.alert-row{display:flex;gap:.45rem;margin:.3rem 0;font-size:.76rem;align-items:flex-start}
.alert-row .ai{flex-shrink:0;font-size:.8rem}

.plan-grid{display:grid;grid-template-columns:1fr 1fr;gap:.6rem;margin:.5rem 0}
.plan-box{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:.85rem}
.plan-box.entry{border-left:3px solid var(--green)}
.plan-box.exit{border-left:3px solid var(--red)}
.plan-box h4{font-size:.78rem;font-weight:600;margin-bottom:.45rem}

.source{font-size:.64rem;color:var(--t3);border-top:1px solid var(--border);padding-top:.4rem;margin-top:.7rem}

.disclaimer{
  background:rgba(224,85,85,.03);
  border:1px solid rgba(224,85,85,.08);
  border-radius:var(--radius);
  padding:.85rem;
  font-size:.66rem;
  color:var(--t3);
  margin-top:2rem;
  line-height:1.6;
}

.skill-divergence{
  border-left:3px solid var(--orange);
  background:rgba(212,145,74,.03);
  border-radius:0 var(--radius) var(--radius) 0;
  padding:.7rem 1rem;
  font-size:.72rem;
  color:var(--t2);
}

@media(max-width:700px){
  body{padding:1rem}
  .cross-grid,.score-grid{grid-template-columns:1fr}
  .plan-grid{grid-template-columns:1fr}
  .fin-grid{grid-template-columns:repeat(2,1fr)}
  .exec-grid{grid-template-columns:1fr}
}
```

## 页面结构

1. **Header**：`.page-title` + `.page-subtitle`（badge行）
2. **Meta bar**：代码/行业/类型/日期/价格等
3. **执行摘要**（结论前置）
4. **§一~§十三**按编号顺序
5. **Disclaimer**

## 字体规范
- 正文/标题：`Inter`
- 所有数字/价格/表格内数据：`JetBrains Mono`
- 代码/规则：`JetBrains Mono`

## 颜色语义
- 金色：标题、关键标注、价位
- 墨绿：利多、上涨、正收益
- 暗红：利空、下跌、亏损
- 钢蓝：链接、强调、条件触发词
