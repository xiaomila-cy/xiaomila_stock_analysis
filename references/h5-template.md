# H5 报告输出模板

所有分析报告以自包含 HTML 格式输出，手机自适应，暗色主题。

## CSS 变量

```css
:root {
  --bg: #0f172a; --surface: #1e293b; --text: #e2e8f0;
  --muted: #94a3b8; --accent: #f59e0b; --green: #22c55e;
  --red: #ef4444; --border: #334155;
}
```

## 结构规范

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>分析报告标题</title>
  <style>/* CSS */</style>
</head>
<body>
  <div class="header">
    <h1>📊 报告标题</h1>
    <p>数据时间 | 来源</p>
  </div>

  <div class="container">
    <!-- 行情仪表盘 -->
    <div class="card-grid" id="dashboard">
      <div class="card">
        <div class="label">现价</div>
        <div class="value">¥XX.XX</div>
        <div class="change positive">+X.XX%</div>
      </div>
    </div>

    <!-- 分析章节 -->
    <div class="section">
      <h2>章节标题</h2>
      <!-- 内容 -->
    </div>
  </div>
</body>
</html>
```

## 卡片组件

行情卡片：
```html
<div class="card">
  <div class="label">指标名</div>
  <div class="value">数值</div>
  <div class="change positive">变动</div>
</div>
```

表格组件：
```html
<table>
  <thead><tr><th>列1</th><th>列2</th></tr></thead>
  <tbody><tr><td>值</td><td>值</td></tr></tbody>
</table>
```

## 样式规范

- 字体：system-ui, -apple-system, "Noto Sans SC"
- 卡片：背景 `var(--surface)`, 圆角 12px, border `var(--border)`
- 涨：绿色 `#22c55e`, 跌：红色 `#ef4444`
- 表格：斑马纹 `:nth-child(even)`, 表头 `var(--border)` 下划线
- 响应式：768px 以下单列
