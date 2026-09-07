---
name: concept-guardrails
description: Run wyx spec guardrails only when the user explicitly invokes $concept-guardrails. / 仅在用户显式调用 $concept-guardrails 时运行 wyx 规格护栏。
compatibility: 只需读写文件与 Grep/Glob；可选的边界注入运行时需要 Claude Code hooks 与 jq。
metadata:
  author: ontology-of-everything
  version: "0.27.0"
---

# 概念护栏（wyx 架构护栏 · 中文版）

## 目标

把模块边界写成规格放在实现代码旁，让 agent 动手前就看见「什么可以碰、什么不可以碰」，并定期核对规格是否已和代码脱节。两个动作：**声明边界**（写规格）、**核对边界**（查漂移）；从一个模块开始就有价值。

[jlifyio/wyx](https://github.com/jlifyio/wyx) v0.26.0 的中文改写版（MIT，见 `LICENSE.upstream`）；在 concept-* 链中是看护环：`concept-design` → `concept-prd` → `concept-implementation` → 本技能日常看护共存规格 → `concept-audit` 周期性全面审计。仅在用户显式调用时运行。

## 原则

1. **先给用户看，再落盘。** 写规格前先呈现草案或 diff，同意后才写；只有 `wyx:map` 例外（完全派生自规格，可直接覆盖）。
2. **`wyx:audit` 与漂移报告全程只读。** 漂移分两段：先审计并呈现报告，用户确认后才改规格或改代码。
3. **规格贴着代码。** `CONCEPT.md` 放在它描述的模块目录，根目录不放（会成为所有子目录的兜底边界）；`PIPELINE.md` 与所属概念同目录。
4. **既有模块规格先行。** 先改 `## actions` / `## state` 再改实现；回填只用于首次为存量代码建规格。
5. **一个仓库一种方言。** 规格格式按下节「方言」表二选一，不混用。
6. 只在会改变路线时提问，一次只问一个阻塞性问题；不做问卷。

## 流程

1. **判定方言**：仓库已有 `concept-prd` 产出的规格、或用户在用 concept-* 链 → **零点名方言**；否则 → **wyx 原生方言**。
2. **判定模式**，读对应参考文件后再动手（参考文件是完整执行程序，不凭记忆执行）：

   | 模式 | 用户会怎么说 | 产出 | 参考文件 |
   | --- | --- | --- | --- |
   | `wyx:audit` | 哪些模块还没规格 | 行动计划（只读） | `references/audit.md` |
   | `wyx:concept` | 写 / 回填概念规格 | `CONCEPT.md` | `references/concept.md` |
   | `wyx:concept drift` | 查漂移 | 漂移报告 | `references/drift-detection.md` |
   | `wyx:pipeline` | 记录数据流与质量不变量 | `PIPELINE.md` | `references/pipeline.md` |
   | `wyx:sync` | 映射跨概念协调 | `SYNCS.md` | `references/sync.md` |
   | `wyx:map` | 生成架构地图 | `ARCHITECTURE.md` | `references/map.md` |

   没有任何规格、也没指定模块时先走 `wyx:audit`。模式名沿用上游命令名；「wyx 审计」与上游带斜杠的 audit 命令是一回事。
3. **执行参考文件**中的程序；写规格的模式在落盘前呈现草案或 diff。
4. **收尾**：规格有变更且项目里存在 `ARCHITECTURE.md` 时，提示用户跑 `wyx:map`。

## 命题

- 每份新写的 `CONCEPT.md` / `PIPELINE.md` 位于它描述的模块目录；根目录无 `CONCEPT.md`。
- `wyx:audit` 与漂移第一段未写入任何文件；漂移修改发生在用户确认之后。
- 零点名方言下，`CONCEPT.md` 只含 `## purpose` / `## state` / `## actions` / `## operational principle`（可选 `## notes`），跨概念边全部在 `SYNCS.md`。
- 同一 flow 的 sync 不拆到多个文件；每个 syncs 目录（或 syncs 包）恰好一份 `SYNCS.md`。
- 规格变更后，若存在 `ARCHITECTURE.md`，已提示重画。

## 记法与模板

三类规格：`CONCEPT.md` 说模块**是什么**（目的、自有状态、对外动作）；`PIPELINE.md` 说数据**怎么流**（阶段、可断言的质量不变量、`## data boundary`）；`SYNCS.md` 说概念**怎么协同**（协调图 + 每条 sync）。地图是合成视图，不参与护栏。

方言对照——漂移检查、地图与 hooks 两种都能处理，差别只在边界写在哪：

| | wyx 原生 | 零点名（concept-* 链） |
| --- | --- | --- |
| `CONCEPT.md` 边界段 | `## interactions` / `## dependencies` / `## known coupling` | 不写；跨概念边只在 `SYNCS.md` 的 `## coordination graph`（`wyx:map` 本就以它为最高优先级来源） |
| `SYNCS.md` 结构 | `## dispatching` + `## sync:` 条目（trigger / timing / flow / qualification / error / file） | 按 flow 分节，sync 用 when / where / then（`concept-prd` 格式）；对应关系 trigger≈when、qualification≈where、flow≈then、timing = `concept-implementation` 的三类时机 |
| 拆分 | 单文件 | 按 syncs 包各一份，flow 不拆散，`wyx:map` 合成全局视图 |
| 级联 | 一个 sync 一个方向、图无环 | 级联合法但须声明 depth-limit；成环归 `concept-audit` 的组合缺陷 |
| hooks 注入的边界 | interactions / dependencies 段 | 段为空，只列出规格；边界靠漂移检查与 `SYNCS.md` |

与 concept-* 其他技能的分工：

| 用户要的是 | 用 |
| --- | --- |
| 哪些模块还没规格（覆盖审计） | 本技能 `wyx:audit` |
| 对照概念模型审计代码：独立性、组合缺陷、五维度 | `concept-audit`（其漂移检查表与本技能同源） |
| 为**存量代码**回填规格、改一个模块的规格、查单模块漂移 | 本技能 `wyx:concept` / `wyx:concept drift` |
| 从**需求**设计新概念、拆边界 | `concept-design` → `concept-prd` |

## 参考

| 何时读 | 文件 |
| --- | --- |
| 六种模式各自的完整程序 | 见「流程」第 2 步表 |
| 接上「每次编辑前后自动注入边界」的 Claude Code hooks（`runtime/` 原样收录上游脚本） | `references/hooks-runtime.md` |
| 上游思想来源（WYSIWID、WYWIWID）与改写差异 | 仓库文档 docs/skills 下本技能页（不随技能安装） |
