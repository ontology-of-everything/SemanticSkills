---
name: wyx-zh-cn
description: Run wyx spec guardrails only when the user explicitly invokes $wyx-zh-cn. / 仅在用户显式调用 $wyx-zh-cn 时运行规格护栏。
compatibility: 只需读写文件与 Grep/Glob；可选的边界注入运行时需要 Claude Code hooks 与 jq。
metadata:
  author: ontology-of-everything
  version: "0.26.1"
---

# wyx 架构护栏（中文版）

把模块边界写成规格，放在实现代码旁边，让 agent 在动手写代码之前就看见「什么可以碰、什么不可以碰」，并能定期核对规格是否已经和代码脱节。

这套方法只有两个动作：**声明边界**（写规格）和**核对边界**（查漂移）。规格是加法——覆盖的模块越多，护栏越密；从一个模块开始就有价值。

## 五种模式

从用户的说法判断模式，然后读取对应的参考文件再动手。参考文件是完整的执行程序，不要凭记忆执行。

| 模式 | 用户会怎么说 | 产出 | 参考文件 |
| --- | --- | --- | --- |
| `wyx:audit` | 审计规格覆盖、有哪些模块还没规格、给我待办清单 | 行动计划（只读，不产出规格） | `references/audit.md` |
| `wyx:concept` | 给这个模块写概念规格、回填规格、设计新模块 | `CONCEPT.md` | `references/concept.md` |
| `wyx:concept drift` | 查漂移、规格和代码对不上、drift 检测 | 漂移报告 | `references/drift-detection.md` |
| `wyx:pipeline` | 记录数据流、描述转换阶段、写数据质量不变量 | `PIPELINE.md` | `references/pipeline.md` |
| `wyx:sync` | 梳理跨概念协调、映射 sync 处理器 | `SYNCS.md` | `references/sync.md` |
| `wyx:map` | 生成架构地图、可视化概念依赖 | `ARCHITECTURE.md` | `references/map.md` |

模式名沿用上游 wyx 的命令名，便于与上游文档、`ARCHITECTURE.md` 里的提示互相对照；本技能里它们是模式，不是必须带斜杠的命令。用户说「wyx 审计」和用上游那条带斜杠的 audit 命令是一回事。

**没有任何规格、也没指定模块时**：先走 `wyx:audit`，让用户看到从哪里开始收益最大，而不是直接挑一个模块写规格。

## 三类规格与它们的分工

- **`CONCEPT.md`** —— 一个模块「是什么」：单一目的、自己拥有的状态、对外的动作、以及 `## interactions` / `## dependencies` 两段边界声明。
- **`PIPELINE.md`** —— 数据「怎么流」：来源、阶段、输出、运行时可断言的质量不变量，以及 `## data boundary` 声明谁拥有输入输出数据。
- **`SYNCS.md`** —— 概念之间「怎么协同」：触发时机、数据流向、跳过条件、错误传播策略。`CONCEPT.md` 的 `## interactions` 声明关系，`SYNCS.md` 描述执行机制。

三者的关系是：概念定义边界，管道在边界内保证数据质量，sync 负责跨概念的编排；架构地图是它们的合成视图，不参与护栏，只给人看。

## 规格放在哪里

规格必须紧贴它描述的实现代码。边界注入 hook 从被编辑文件所在目录**向上**走，在**第一个含 `CONCEPT.md` 或 `PIPELINE.md` 的目录**停下；`SYNCS.md` 会被列出但不终止向上查找。

```text
src/lib/
├── orders/              # 一个概念 = 一个目录
│   ├── CONCEPT.md       # 本模块的边界声明
│   ├── service.ts
│   └── repository.ts
├── scoring/
│   ├── CONCEPT.md       # 边界
│   ├── PIPELINE.md      # 与概念同目录共存（安全）
│   ├── calculate.ts
│   └── aggregate.ts
└── syncs/
    ├── SYNCS.md         # 所有 sync 流写在同一个文件里（保持单文件）
    ├── order-to-inventory.ts
    └── order-to-scoring.ts
```

三个要避开的反模式：

- **根目录放 `CONCEPT.md`** —— 它会成为所有子目录的兜底边界，把过宽的约束套到没有自己规格的模块上。
- **`PIPELINE.md` 单独放在没有 `CONCEPT.md` 的子目录** —— 例如把它放进 scoring 的 transforms 子目录，会让向上查找停在 transforms 这一层；hook 能识别缺失的 `CONCEPT.md` 并带 `[SHADOWED]` 标注注入祖先边界，但这说明放置位置不理想。
- **拆分 `SYNCS.md`** —— 协调图需要完整视图，局部图只会给出虚假的信心。

## 通用纪律

- **先给用户看，再落盘。** `wyx:concept`、`wyx:pipeline`、`wyx:sync` 都必须先呈现草案、征得同意才写文件；文件已存在时先给 diff。只有 `wyx:map` 例外（它完全派生自规格，可直接覆盖重写）。
- **`wyx:audit` 全程只读。** 它报告问题、输出该跑哪些命令，永远不产出规格文件。
- **漂移分两段。** 第一段只做审计并呈现报告，第二段才在用户确认后改规格或改代码——不要把两段合成一步。
- **规格改了就提醒重画地图。** 若项目里存在 `ARCHITECTURE.md`，在规格变更后提示用户跑 `wyx:map`。
- **既有模块优先「规格先行」。** 已经有规格的模块，先改 `## actions` / `## state` 再改实现，这样边界注入立刻生效；回填模式（先代码后规格）只适合首次为存量代码建规格。

## Agent 纪律

只在会改变路线时提问；用户已经说明或已确定的事实不要重复追问；上下文足够就直接推进；确实需要用户判断时，一次只问一个阻塞性问题。领域必需的澄清项（模块范围、要不要落盘、改规格还是改代码）仍然要问——但不要做成问卷。

## 边界自动注入运行时（可选）

本技能的规格与检查流程与 agent 无关，任何 agent 都能执行。而「每次编辑前后自动注入边界」是上游 wyx 的 Claude Code hooks 机制，脚本原样收录在 `runtime/`，未作任何改动。接线方式见 `references/hooks-runtime.md`。

没有这套运行时，规格依然有用（agent 按本技能主动读取规格、漂移检测照常工作）；有了它，边界会在每次写入前后被动送到模型眼前。

## 参考文件

| 主题 | 文件 |
| --- | --- |
| 规格覆盖审计与命令排序 | `references/audit.md` |
| 概念规格设计（回填 / 新建 / 发现） | `references/concept.md` |
| 漂移检测完整程序与严重度校准 | `references/drift-detection.md` |
| 数据管道规格与质量不变量 | `references/pipeline.md` |
| Sync 协调映射 | `references/sync.md` |
| 架构地图生成 | `references/map.md` |
| hooks 运行时接线与排错 | `references/hooks-runtime.md` |

## 来源与致谢

本技能是 [jlifyio/wyx](https://github.com/jlifyio/wyx) v0.26.0 的中文改写版，遵循上游 MIT 许可（见 `LICENSE.upstream`）。上游的思想来源：

- **WYSIWID** —— Meng & Jackson, "What You See Is What It Does"（MIT, Onward! 2025）：把概念规格与边界声明作为让软件可读的结构化手段。
- **WYWIWID** —— Dr. Ernie, "What You Write Is What It Did"：用漂移检测与数据管道不变量提供基于证据的可读性。
