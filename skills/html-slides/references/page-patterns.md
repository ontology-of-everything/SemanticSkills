# page-patterns.md — 页型目录与骨架

页型 = 一页的版式模式。阶段 3 用 §1–2 选型，阶段 4 用 §3 骨架拼页。骨架只用 CSS 变量与基础 class（`deck-format.md` §4），任何风格直接可用；风格专属页型见 `styles/<style>.md` §5。

## 1. 固定页

| 页 | 位置 | class | 规则 |
| --- | --- | --- | --- |
| 封面 | 第 1 页 | `cover` | 标题 + 副题 + 汇报人 / 部门 / 日期；背景 `--bg-cover` |
| 目录 | 第 2 页 | `toc` | 条目 = 当前大纲章数，章名逐字一致；可作章节过渡页重复出现、只切换高亮项 |
| 致谢 | 末页 | `thanks` | 大字致谢 + 联系方式 / 声明；不是普通总结页 |

三页不可省略、不可用自制页替代；封面与致谢内容随需求改，结构不变。

## 2. 页型目录

`data-family` 取值：门面 / 网格 / 分栏 / 流程 / 矩阵 / 证据 / 全图 / 观点 / 互动。`data-density`：light / normal / dense。**连续 3 页同一家族返工；dense 后接 light。**

| 页型 | 家族 / 密度 | 用于 | 版式要点 | 场景限制 |
| --- | --- | --- | --- | --- |
| 章扉 `chapter` | 门面 / light | 每章开头 | 超大浅色章号 + 章名判断句 + 2–3 句叙事线 + 关键词胶囊 | 短汇报可省 |
| 问题页 `question` | 门面 / light | 引出痛点 | 一个具体可讨论的真问题，不给答案 | — |
| 议程 / 结论 `summary` | 观点 / normal | 第 3 页或首内容页 | 授课：目标四行；汇报：TL;DR 四句结论先行 + 3 个关键数字 | — |
| 卡片网格 `card-grid` | 网格 / normal | 并列要点 3–6 项 | 等宽同构卡，标题四到六字断言 | — |
| 密集多栏 `dense-columns` | 网格 / dense | 全景、清单 | 3–4 栏各 4–8 条，靠对齐维持秩序；后接轻页 | — |
| 数字大字带 `kpi-band` | 网格 / normal | KPI、成果 | 3–6 格 `.num` + 单位 + 口径小字；好坏都上墙 | — |
| 左图右文 `image-text` | 分栏 / normal | 一图一论 | 图 `height:100%` 填满，右侧小标题 + 正文 | — |
| 对比两栏 `compare` | 分栏 / normal | AS-IS / TO-BE、方案 A/B | 左灰右强调；数字「过去→现在 + 箭头」 | — |
| 痛点·方案·价值 `pain-solution-value` | 分栏 / dense | B2B 方案页 | 1-2-1 三段：痛点（窄）｜方案主体（宽）｜价值（窄） | 汇报优先 |
| 流程条 `flow` | 流程 / normal | 步骤、管线、时间轴 | 节点 → 箭头 → 节点，瓶颈节点 `hot`；时间轴节点上下交错 | — |
| 分层架构 `architecture` | 流程 / dense | 系统结构 | 横向色带分层 + 底座；异构单元必须展开（`visuals.md` §3） | — |
| 表格混排 `table-mix` | 矩阵 / dense | 对比、枚举 | 标准表格（`visuals.md` §4）+ 侧栏结论 | — |
| 勾叉 / 热力矩阵 `matrix` | 矩阵 / dense | 能力盘点、进度 | 行头 × 列头，格内 ✓/✕/— 或四态色块 + 图例 | — |
| 方案决策 `decision` | 矩阵 / normal | 选型 | 方案 × 维度评分，选中列 `hot` + 决策理由 + 翻盘条件 | — |
| 截图对照 `screenshot-pair` | 证据 / normal | 用真料说话 | 等高截图 2–3 张 + 逐张一句解说 | — |
| 代码·曲线·指标 `code-curve-metrics` | 证据 / dense | 实验证据链 | 左最小代码，右上曲线，右下同口径指标 + 结论 | 技术分享 |
| 案例五段式 `case` | 证据 / dense | 客户 / 项目案例 | 「案例｜对象：做法，价值」标题；背景 → 过程 → 成果数字 → 实证图 → 引文署名 | 汇报 |
| 全幅大图 `full-image` | 全图 / light | 换气、震撼图 | 图铺满 + 一行图注 | — |
| 金句 / 小结 `quote` | 观点 / light | 章末 | 深底大字一句判断 + 出处 | — |
| Takeaway `takeaway` | 观点 / normal | 收尾巩固 | 编号 01–04 可复述的技术判断 | — |
| 下一步 `next-steps` | 观点 / normal | 汇报收尾 | 本周 / 本月 / 本季三栏，动词开头 + Owner | 汇报 |
| 研讨 `workshop` | 互动 / normal | 课堂讨论 | 编号议题条，开放式问题 | **仅授课** |
| 动手实验 `lab` | 互动 / normal | 演示、实操 | 步骤 + 预期结果 + iframe/截图 | 授课、自读 |
| 题卡 `quiz` | 互动 / normal | 巩固 | 题干一拍、答案一拍（`motion.md`） | **仅授课** |

选型顺序：有真素材 → 证据家族；两个以上耦合维度 → dense 复合页；讲机制 → 流程家族；并列 → 网格；其余观点家族。

## 3. 骨架

全部骨架在 `assets/core/skeletons.html`（可直接用浏览器打开预览），每段以 `<!-- ===== 页型名 ===== -->` 注释分隔，复制对应 `<div class="slide-wrap">…</div>` 后替换文字：

| 骨架 | 要点 |
| --- | --- |
| 封面 `cover` | 主标题 84px 判断句 + 副题；底部左「部门 · 汇报人 · 日期」右「SECURITY LEVEL」占位（`data-classification`） |
| 目录 `toc` | 大字「目录」+ 强调色短下划线；每章一个 `li`（序号 / 章名 / 本章问题）；作过渡页时给当前项 `color:var(--accent)` |
| 章扉 `chapter` | 超大 8% 透明章号置底 + eyebrow「SECTION 0N · N MIN」+ 100px 章名 + 2–3 句叙事线 |
| 卡片网格 `card-grid` | `.body` 为 `grid` 3 列；同构 `.card`；结论卡加 `hot` |
| 左图右文 `image-text` | 图容器 `flex:0 0 auto;max-width:60%;height:100%`，图 `height:100%;width:auto`（不用 `max-*`，否则小图不放大） |
| 痛点·方案·价值 `pain-solution-value` | 三张 `.card` 按 `flex:1 / 2 / 1` |
| 对比两栏 `compare` | 左卡灰标题 + 灰 `.num`，中间强调色箭头，右卡 `hot` + 强调色 `.num` |
| 数字大字带 `kpi-band` | `grid` 4 列居中卡，每卡 `.num` + 类别词 + 15px 口径 |
| 流程条 `flow` | 横向 `.card` 节点 + 箭头字符，瓶颈 `hot`；示例同时演示 build 逐拍 |
| 标准表格 | 见 `visuals.md` §4 规则，骨架在同一文件 |
| layer 示例 | 三按钮三面板，默认按钮无 `data-step` |
| 致谢 `thanks` | 120px 大字 + 联系方式 / 声明 |

其余页型由以上组合：`dense-columns` = card-grid 4 列 + 每卡 5–8 条；`table-mix` = 标准表格 + 右侧 1 张结论卡；`matrix` = 表格里只放 ✓/✕/—；`quote` = `chapter` 骨架换深色 profile + 单句；
`screenshot-pair` = image-text 横排 2–3 张等高图；`summary` = card-grid 4 列短句或 kpi-band + 一行结论。风格专属页型骨架在 `assets/<style>/patterns.html`。
