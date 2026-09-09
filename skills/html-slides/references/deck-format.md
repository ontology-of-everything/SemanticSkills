# deck-format.md — 明文单文件 HTML 契约

deck 是一份可读、可 diff、可直接编辑的 HTML：`<style>` 里放变量块 + 基础 CSS（+ 风格专属 CSS），`<body>` 里每页一个 `<section class="slide">`，末尾一段运行时 JS。图片全部 data URI 内联，拷走即用，无网络依赖。**所有代码都在 `assets/` 的源文件里，本文只讲规则。**

## 1. 组装顺序

| 位置 | 复制自 | 说明 |
| --- | --- | --- |
| `<style>` ① | `assets/<style>/vars-light.css` 或 `vars-dark.css` | 风格变量块，浅 / 深 profile 二选一 |
| `<style>` ② | `assets/core/base.css` | 风格无关基础 CSS：画布缩放、四段结构、卡片、数字、页脚、动画协议、工具条、debug 标记 |
| `<style>` ③ | `assets/<style>/style.css`（如有） | 风格专属组件 |
| `<body>` 开头 | `assets/core/skeletons.html` 的 `<nav class="bar">` | 页码 + 放映 / 滚动切换钮 |
| `<body>` 主体 | `skeletons.html` / `assets/<style>/patterns.html` 里的 `<section>` | 每页一个 `<div class="slide-wrap"><section class="slide …">` |
| `<script>` | `assets/core/runtime.js` | 运行时，整段内联 |

`skeletons.html` 与 `patterns.html` 本身可用浏览器直接打开预览（画廊用外链 css/js），deck 里必须内联。

## 2. 页面约定

- `<section>` 必带 `class="slide"`、唯一 `data-label`（= plan.md 逐页表 label 列）、`data-family`、`data-density`（取值见 `page-patterns.md` §2）。
- 固定三页 class：`cover` / `toc` / `thanks`；`chapter` / `question` 同属门面页，padding 与背景由基础 CSS 处理。密页加 `dense` 类把标题降到 40px。
- 内容页四段：`.eyebrow` → `<h3>` → 可选 `.intro` → `.body`（`flex:1;min-height:0`，主体吃满并可收缩）。
- 卡片：`.card > .ct + .cb`；点明差异的那一张加 `hot`。数字大字 `.num > small`。
- 页脚 `.foot` 是风格插槽：`.foot-l` 文本（运行时自动追加页码）、`.foot-r img` logo；无风格要求可省略整个 `<footer>`。
- 相邻内容页背景自动在 `--bg` / `--bg-alt` 间交替（`nth-child(even)`），不用手工设。
- `.build` / `data-step` / `data-layer-*` 只在需要动画时出现（`motion.md`）。

## 3. 变量契约

每个风格的 `vars-*.css` **必须**定义以下全部变量；核心 CSS 与骨架只引用变量名：

| 变量 | 含义 |
| --- | --- |
| `--bg` / `--bg-alt` | 内容页背景及相邻页交替色 |
| `--bg-cover` | 门面页背景（色或 `url(data:…)`） |
| `--surface` / `--line` | 卡片底 / 细线 |
| `--fg` / `--fg-body` / `--fg-muted` | 标题 / 正文 / 次要 |
| `--accent` / `--accent-soft` | 品牌强调色（唯一）/ 其淡底 |
| `--accent-2` | 第二色：对比、旧方案、次要徽标；深色 profile 常为「工作色」 |
| `--font-sans` / `--font-mono` | 中文正文栈 / 数字英文代码栈（系统字体栈，不引入网络字体） |
| `--radius` / `--shadow` | 卡片圆角 / 阴影 |
| `--table-head` | 标准表格表头底色 |

新增风格时对照此表逐项填写；漏一项基础 CSS 就会出现无样式区域。

## 4. 图片内联

- 生成 base64：macOS `base64 -i f.png | tr -d '\n'`；Linux `base64 -w0 f.png`；或 Python `base64.b64encode(...)`。
- 写法 `<img alt="一句说明" src="data:image/png;base64,…">`；JPEG 用 `image/jpeg`；SVG 直接内联 `<svg>` 不转 base64。
- 单图 >1 MB 先降采样；一份 deck 图片总量控制在 15 MB 内。
- `assets/<style>/` 的素材同样转 data URI 进 deck，不用相对路径。

## 5. 运行时行为（`runtime.js`）

- 默认**滚动模式**：所有 build 已显示、layer 可点选，便于阅读、审阅与 debug。
- `P` 或右上 ▶ 进入**放映模式**（自动全屏）：方向键 / 空格 / 点击空白 / 滚轮逐拍推进，`Home` / `End` 首末页，`F` 全屏。
- 刷新回到上次页：`#页号` 优先，其次 localStorage。
- 页码：`.pn` 显示 `当前 / 总数`；每页 `.foot-l` 自动追加页号。
- **`?debug`**：section 级溢出加红实框、内层 `overflow` 裁切加橙虚框，控制台逐条列出，标题前缀 `⚠N` / `✓`。debug 在滚动模式测量；非激活 layer 面板 `display:none` 不参与，多标签页要手动切到每个标签再看。

## 6. 写 HTML 的自检

- 每写完一章：浏览器打开 `<deck>.html?debug`，标题前缀为 ✓。
- `grep -c 'data-label=' <deck>.html` = plan.md 逐页表行数；`grep -c 'data-todo'` 终版 = 0。
- 无 `src="http` 资源引用；iframe 嵌网页是例外且要有「复制链接」兜底。
- `cover` / `toc` / `thanks` 各出现 1 次；目录条目数 = 大纲章数。
- 变量块含 §3 全部变量名。
- 宿主有浏览器工具时：重点页与深色页截图目检；SVG 文字与箭头不能靠 debug 数值，必须目检（`visuals.md` §5）。

## 7. PPTX 原生重建（用户要「可编辑」时）

`tools/export_pptx.py` 产出截图贴图版。用户要求可编辑 PPTX 时，agent 运行期写一段一次性 python-pptx 脚本（不入技能），以 `<deck>.plan.md` 逐页表 + `<deck>.html` 文案为源重建，并在交付时说明「版式为重建版，与 HTML 有出入」：

| deck 元素 | PPTX 映射 |
| --- | --- |
| eyebrow + h3 + intro | 顶部标题文本框（h3 → 标题，eyebrow 小字，intro 副标题），字号 px × 0.5 = pt |
| `.card` 网格 | 等宽矩形 + 文本框，`--surface` 底、`--line` 边、`--radius` 圆角；同组同构 |
| `.num` | 大号文本框（`--accent`）+ 单位小字 |
| 标准表格 | `add_table`，表头 `--table-head` 底白字，全黑边框 |
| 图片 / SVG 图 | 有浏览器工具则截图后 `add_picture`；否则留占位矩形并注明 |
| build / layer | 全部展开为静态；layer 每个标签一页 |
| 讲稿 | plan.md「核心观点」列写入 `notes_slide` |

幻灯片 `13.333in × 7.5in`（16:9）；`in = px / 144`；颜色取变量块实际值。
