# HTML 胶片

`html-slides` · **HTML Slides — Styled Single-File Decks**

> 本文是给人看的中文说明，**不是** `npx skills add` 安装包内容。Agent 加载 [`skills/html-slides/SKILL.md`](../../skills/html-slides/SKILL.md)。

**Version:** 0.1.0 · Changelog:
[qa/html-slides/CHANGELOG.md](../../qa/html-slides/CHANGELOG.md)

## 一句话

把一句话需求做成一份**明文单文件 1920×1080 HTML 演示**：先定场景 / 对象 / 时长 / 风格，确认大纲再确认逐页表，然后写 HTML；视觉由风格插拔（`generic` 默认、`huawei` 官方胶片浅 / 深色、`apple` 经验版）；需要时导出截图版 PPTX 或用 python-pptx 重建可编辑版。

## 显式调用

技能默认不触发。只在用户写 `$html-slides` / `/html-slides` 且要做一份 PPT / 胶片 / 汇报 / 授课 / 技术分享时启动；一般性「封面怎么设计好看」之类问题不启动。

```text
$html-slides 15 分钟华为云 DME 产品介绍，对象客户 IT 主管，华为风格浅色，先出大纲
```

## 设计取舍

| 问题 | 本技能做法 |
| --- | --- |
| 单一模板硬编码色值 | 核心只用 CSS 变量；`assets/<style>/vars-*.css` 给值；新增风格不改核心 |
| 知识与工具混在一起 | 只保留「怎么做好一份胶片」的知识 + 一个可选导出脚本 |
| 代码散落在 markdown 里 | 代码集中在 `assets/`（可直接用浏览器打开预览），`references/` 只讲规则 |
| 素材体积大 | 华为素材精选 5 件约 1 MB；其余用户自带 |
| 溢出检查靠脚本 | 运行时内置 `?debug` 标记 + agent 自检清单 |

## 方法

1. **阶段 1 聊清楚**：场景、对象、时长、风格与 profile、密级。用户已说的不重问。
2. **大纲 → 硬门**：章、每章回答的问题、时长预算，确认后才进下一步。
3. **逐页表 → 硬门**：label、页型、核心观点、素材占位，写进 `<deck>.plan.md`。
4. **写 HTML**：按 `deck-format.md` 顺序内联 `vars-*.css` → `base.css` → 风格 css，从 `skeletons.html` / `patterns.html` 复制页骨架，末尾内联 `runtime.js`。
5. **素材两阶段**：先占位（类型 + 来源 + 内容一句 + 长宽比），后落图（原图 data URI / 自绘 SVG / 标准表格）。
6. **自检**：`?debug` 标题 ✓、`data-label` 数 = 逐页表行数、`data-todo` = 0、无外链资源。
7. **交付**：HTML 为主；PPTX 分「截图贴图版」与「python-pptx 重建版」两档，说明差异。

## 运行时（deck 内置）

滚动模式默认；`P` 放映（方向键 / 空格 / 点击 / 滚轮逐拍，`Home` / `End`，`F` 全屏）；`build` 逐拍、`layer` 互斥画面；刷新回到上次页；`?debug` 溢出红框 + 控制台清单。

## 安装载荷

```text
skills/html-slides/
├── SKILL.md                     # 概论 / 原则 / 流程 / 输出格式 / 完成条件 / 参考路由
├── agents/openai.yaml
├── references/
│   ├── process.md               # 七阶段、场景适配表、常见错误
│   ├── style-guide.md           # 风格无关硬规则：色 / 字 / 字号档 / 文案 / 版式 / 术语
│   ├── page-patterns.md         # 页型目录（视觉家族 × 密度）与骨架索引
│   ├── deck-format.md           # 单文件契约、组装顺序、变量契约、运行时行为、PPTX 重建
│   ├── visuals.md               # 素材两阶段、占位规格、自绘与标准表格规则
│   ├── motion.md                # build / layer 协议与键位
│   └── styles/
│       ├── _template.md         # 新风格六节空表
│       ├── generic.md
│       ├── huawei.md
│       └── apple.md
├── assets/
│   ├── core/                    # base.css · runtime.js · skeletons.html（骨架画廊）
│   ├── generic/                 # vars-light.css · vars-dark.css
│   ├── huawei/                  # vars-*.css · style.css · patterns.html · 5 件素材
│   └── apple/                   # vars-*.css · style.css
└── tools/export_pptx.py         # 可选：截图贴图版 PPTX（playwright + python-pptx，不自动安装）
```

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill html-slides \
  --agent cursor \
  --copy -y
```

Local checkout:

```bash
npx skills add ./skills/html-slides \
  --skill html-slides \
  --agent cursor \
  --copy -y
```

## Marketplaces

- [skills.sh](https://skills.sh/ontology-of-everything/SemanticSkills/html-slides)
- [SkillsMP](https://skillsmp.com/) — repo topics `claude-skills`, `claude-code-skill`
- [ClawHub](https://clawhub.ai/agenticweb4/html-slides)

## 素材声明

`assets/huawei/` 内 logo 与 KV 提取自华为官方公开胶片，商标归华为所有，仅供制作华为风格演示；Apple 风格不含任何 Apple 商标或产品图。
