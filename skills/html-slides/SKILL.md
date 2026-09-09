---
name: html-slides
description: "Builds a PPT / 胶片 / 汇报 / 授课 deck as a plain single-file 1920×1080 HTML in a pluggable style (Huawei 华为 official light/dark, Apple, generic), confirming outline and per-page table first; optional PPTX export. Use when the user explicitly invokes $html-slides; not for general slide-design questions."
compatibility: File read/write only. Optional PPTX export needs Python 3, playwright and python-pptx (never auto-installed).
metadata:
  author: ontology-of-everything
  version: "0.1.0"
  openclaw:
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/html-slides
---

# 演示文稿生成（多风格）

## 概论

把一句话需求做成一份**明文单文件 HTML 演示**（1920×1080，内联 CSS，≤120 行运行时 JS）。

代码与文档分离：`assets/core/` 放基础 CSS、运行时 JS 与页型骨架画廊，`assets/<style>/` 放风格变量与专属组件，`references/` 下的 md 只讲规则并指向这些文件。
视觉由风格插拔：核心只用 CSS 变量名，风格给取值、字体、专属页型与素材。首版收录 `generic`（默认兜底）、`huawei`（官方胶片分析）、`apple`（经验版）；新增风格按 `references/styles/_template.md` 建一份 md + 一个 `assets/<style>/` 目录即可。

**仅显式调用**：用户写 `$html-slides`（或同名斜杠命令）或点名本技能时启用；泛泛聊 PPT 不触发。不做的事：不代用户编造数据与引文；不安装依赖；PPTX 只在用户要求时导出并明说是哪一档（见输出格式）。

## 原则

每条只在指向的文件里定义细则，本节不重述。

1. **先对齐再动手**：主题与大纲未经用户确认不写页面 → `process.md` §1–2
2. **标题即观点且点名技术**：内容页标题是有判断的句子并含关键技术 / 方法名；全部标题连读 = 论证链 → `style-guide.md` §4
3. **固定三页**：第 1 页封面、第 2 页目录、末页致谢，目录随当前大纲重建 → `page-patterns.md` §1
4. **每页塞进 1080**：`section` 固定尺寸 + `overflow:hidden`，超出被无声裁切；交付前 `?debug` 零红框 → `deck-format.md` §5
5. **字号按场景分档**：授课散文 ≥21px；汇报 / 自读短语卡 ≥18px；表格、轴标签、图内文字 15px 图元豁免 → `style-guide.md` §3
6. **连续 3 页换视觉家族**，密页后接轻页；两个以上耦合维度用复合页型不拆薄 → `page-patterns.md` §2
7. **同级卡片同构**：同组同角色卡片的底 / 边 / 圆角 / 字体层级完全一致，只有文案说明了差异才允许单卡高亮 → `style-guide.md` §5
8. **语言朴实可核验**：不写套话、广告词、自造比喻，页面上不写「点击查看」类操作提示 → `style-guide.md` §4
9. **字不如表，表不如图**：机制 / 流程 / 架构页以图表为主表达；初版放类型化占位，终版落地并清零 `data-todo` → `visuals.md`
10. **动画只手动推进**，汇报与自读默认静态 → `motion.md`
11. **风格只改变量与专属组件**：`assets/core/` 与骨架不出现具体色值；取值一律来自 `assets/<style>/vars-*.css` → `deck-format.md` §3
12. **图片经 data URI 内联**，deck 拷走即用；素材来自 `assets/<style>/` 或用户提供 → `deck-format.md` §4

## 流程

七阶段，三个「讨论」是硬闸门；细则与场景适配表见 `process.md`。

| # | 阶段 | 产出 | 闸门 |
| --- | --- | --- | --- |
| 1 | 主题讨论 | 五问一次问完（听众 / 场合时长 / 目标 / 素材 / 风格与交付）→ 需求共识一段 | 用户确认 |
| 2 | 大纲规划 | 章 / 问题 / 分钟 / 页数表；确认后落盘 `<deck>.plan.md` | 用户确认 |
| 3 | 选择页型 | 大纲条目 → 页型 → 视觉家族 / 密度 映射表 | 随 4 给出 |
| 4 | 初版 | 逐页规划表 + `<deck>.html`（配图为占位块） | — |
| 5 | 讨论修改 | 逐章引导反馈，按页记录修改清单 | 用户点头「结构定了」 |
| 6 | 终版 | 配图落地、动画节拍（仅授课）、`?debug` 零溢出、按需 PPTX | — |
| 7 | 交付确认 | 微调、数字核对、交付话术 | 用户验收 |

用户催「直接做」：五问改为带默认值的一轮快答，用户只需纠偏；闸门不豁免。未指明风格 → `generic`，并在需求共识里写明「当前风格：通用商务，可改」。

## 输出格式

**`<deck>.plan.md`**（阶段 2 建、随改随更）：

```markdown
# <标题> · 页面规划
风格：huawei-light · 场景：汇报 · 时长：10 min · 交付：HTML(+PPTX)
## 大纲
- 01 章名 — 本章要回答的问题（N 页）
## 逐页
| # | label | 核心观点（一句话） | 页型 | 视觉家族/密度 | 配图（类型+规格） | 拍数 |
```

**`<deck>.html`**：按 `deck-format.md` §1 顺序把 `assets/<style>/vars-*.css` → `assets/core/base.css` → `assets/<style>/style.css` 内联进 `<style>`，
从 `assets/core/skeletons.html` / `assets/<style>/patterns.html` 复制 `<section>`，末尾内联 `assets/core/runtime.js`；每页 `<section data-label>` 直接可读可编辑。

**PPTX 两档**（用户要求时）：① `python3 tools/export_pptx.py <deck>.html [--notes <deck>.plan.md]` 截图贴图版，像素一致、不可编辑、讲稿进备注；② 用户要「可编辑」时按 `deck-format.md` §7 用 python-pptx 原生重建。交付话术必须写明档次与差异。

## 完成条件

- [ ] `<deck>.plan.md` 与 `<deck>.html` 页数、顺序、label 一一对应；封面 / 目录 / 致谢齐全且目录章名 = 大纲
- [ ] 每个内容页标题是含技术名词的判断句；无套话、无操作提示
- [ ] `?debug` 打开无溢出红框；连续 3 页无同一视觉家族
- [ ] `data-todo` 计数为 0（终版）；图片均为 data URI，无外链依赖
- [ ] 变量块完整（`deck-format.md` §3 清单）；`base.css` / `runtime.js` 原样内联未改动；骨架无硬编码色值
- [ ] 交付说明含：放映键位一句、如何自助改文案、PPTX 档次（如有）

## 按需参考

| 何时读 | 文件 |
| --- | --- |
| 阶段 1–2、场景适配、快答模板、常见错误 | `references/process.md` |
| 风格无关硬规：字号分档、卡片体系、文案句式、术语表 | `references/style-guide.md` |
| 阶段 3–4 选页型、视觉家族轮换、骨架索引 | `references/page-patterns.md` |
| 写 HTML：组装顺序、页面约定、变量契约、运行时行为、debug、PPTX 原生重建 | `references/deck-format.md` |
| 基础 CSS / 运行时 / 骨架画廊（复制用，浏览器可直接打开预览） | `assets/core/base.css`、`runtime.js`、`skeletons.html` |
| 配图：占位 → 自绘 SVG/div → 标准表格 → 验收 | `references/visuals.md` |
| 授课动画：build / layer / 键位 / 排拍法 | `references/motion.md` |
| 选定风格后必读；新增风格 | `references/styles/<style>.md` + `assets/<style>/`；`references/styles/_template.md` |
