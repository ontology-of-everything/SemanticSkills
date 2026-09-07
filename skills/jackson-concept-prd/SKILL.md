---
name: jackson-concept-prd
description: Transcribes a confirmed Jackson concept model into PRD specs (central overall PRD plus wyx-compatible colocated CONCEPT.md and flow-grouped SYNCS.md). Use this skill whenever the user asks for a concept PRD, 规格文档, or mentions jackson-concept-prd; do not invent model content.
---

# Jackson 概念 PRD（设计规格）

输入是已确认的概念模型（`jackson-concept-design` 的输出）。概念设计即设计规格：本技能只做转录与编排，不发明模型外的内容；发现模型缺口时回上游技能补模，不在文档里私自填补。文档交付后，代码落地用 `jackson-concept-implementation`。

## 文档族（双轨放置）

应用层视图集中，概念与 sync 规格贴近代码：

```text
docs/prd/README.md        # 总体 PRD：应用层视图（始终集中）
<模块目录>/CONCEPT.md      # 每概念一份：模块目录已存在时与代码共存
<syncs 目录>/SYNCS.md      # 全部 sync 单文件，放 syncs 目录（实现期拆包见下）
docs/prd/concepts/<名>.md  # 代码未就绪时的暂存位，同为 CONCEPT.md 格式
docs/prd/SYNCS.md          # 同上，syncs 目录未建时暂存
```

- **共存优先**：模块目录已存在（回填或实现后）就把 `CONCEPT.md` 放进去；代码未就绪先集中暂存，落地时由 `jackson-concept-implementation` 迁移共存。
- **wyx 兼容**：文件名与段落头（`## purpose` / `## state` / `## actions` / `## operational principle`）与 wyx 架构护栏一致，
  `wyx:concept drift`、`wyx:map` 可直接消费。但**不产出** `## interactions` / `## dependencies` 段——跨概念边全部在
  `SYNCS.md` 与总体 PRD 的依赖图（wyx 建图的最高优先级来源本就是 SYNCS.md 的 coordination graph）。
- 生成后这组文件就是模型的**持久形态（single source）**：模型变更后重新生成对应文件，不手改，避免规格与模型漂移。

## 总体 PRD（docs/prd/README.md）

- **需求与 Misfits**：用户 / 需要 / 问题 / 结果 / 约束。
- **概念索引**：每概念一行 purpose + 规格文件链接（共存或暂存路径）。
- **依赖图与子集**：extrinsic 依赖、MVP 与版本裁剪——依赖信息只在这里，不进任何概念规格。
- **排除与未决**：全量转录。

## 每概念 CONCEPT.md

铁律：**零点名其他概念**——purpose / state / actions / operational principle 四节不得出现其他概念名；上下文只以类型参数出现（`Comment [Target]`）。唯一豁免是 `## notes`（作者裁定的使用上下文备注落点），且只是散文备注，不是依赖声明。

```markdown
# concept: <Name> [<TypeParam>]

## purpose
[恰好一个]

## state
- <字段>: <TypeParam> -> <类型>

## actions
（签名 + requires/ensures；错误是独立输出 case；`_` 前缀 queries 只读）

## operational principle
after <动作>(<参数>) : (<结果>) then <动作>(<参数>) : (<结果>)
[可多条场景——验收场景即由此机械导出：OP 的每条 after/then 场景 = 一条验收]

## notes
[可选：应用角色、类型参数实例化、非功能约束占位（由人补充）]
```

## SYNCS.md（按 flow 分节）

Flow = 一个外部请求（`Requesting` 动作）触发、多条细粒度 sync 接力的动作链。**sync 按 flow 聚合、不按域分节**——sync 常跨域，按 flow 才能看出欠同步与过同步。
转录期全部 sync 单文件、自带完整协调图；实现期 syncs 层按概念分组拆包时，由 `jackson-concept-implementation` 把本文件按 flow 群随包拆分（flow 不拆散，协调图随包局部化）。

```markdown
# syncs: <应用名>

## coordination graph
[Concept] --(action)--> (SyncName) --> [Concept]

## flow: <名>
触发: Requesting.<动作>

（sync 块，when / where / then 记法同 jackson-concept-design；
含错误 flow：匹配 (error: …) 输出的错误 sync）

排除动作: 本 flow 有意不同步的概念动作及理由
```

## 完成条件

- 模型输出的每个部分（concepts、syncs、依赖图、排除与未决）都有唯一落点，无遗漏无重复。
- 每份 CONCEPT.md 四节零点名其他概念，无 interactions / dependencies 段；上下文备注只在 notes。
- 每条验收场景可追溯到 OP；文档无模型外的新信息（notes 占位除外）。
- SYNCS.md 转录期单文件、有 coordination graph、按 flow 分节（实现期拆包归 `jackson-concept-implementation` 管辖）；每个可失败动作有错误 sync 或记入排除。
- 总体 PRD 可导航到全部规格文件，链接有效。

## 依据

概念规范即规格：[WYSIWID 论文](https://arxiv.org/abs/2508.14511)（概念规范可直接生成代码与测试、行为增量 = sync 的增删）；
[Beyond Objects](https://arxiv.org/abs/2606.27258)（现行记法与 notes 惯例）；官方课程模板
[conceptbox](https://github.com/61040-fa25/conceptbox)（规格与代码同仓、规格驱动开发）。
记法与判据沿用 `jackson-concept-design`，不另立标准。
