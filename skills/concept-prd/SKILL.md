---
name: concept-prd
description: Transcribes a confirmed concept model (Daniel Jackson's concept design) into PRD specs (central overall PRD plus wyx-compatible colocated CONCEPT.md and flow-grouped SYNCS.md). Use this skill whenever the user asks for a concept PRD, 规格文档, or mentions concept-prd; do not invent model content.
---

# 概念 PRD

## 目标

输入：`concept-design` 确认过的模型（concepts、syncs、依赖图、排除与未决）。输出：总体 PRD + 每概念一份 `CONCEPT.md` + 一份 `SYNCS.md`。概念设计即设计规格，本技能只转录与编排。交付后代码落地 → `concept-implementation`；模型缺口 → 回 `concept-design`。

## 原则

1. 只转录，不发明；缺口回上游，不在文档里填补。
2. 跨概念信息只有两个落点：`SYNCS.md` 与总体 PRD 的依赖图。概念规格里的上下文只以类型参数出现（`Comment [Target]`），散文备注只进 `## notes`。
3. 规格贴近代码：模块目录已存在就与代码共存，未就绪先集中暂存，落地时由 `concept-implementation` 迁移。
4. 文档族是模型的持久形态：模型变了就重新生成，不手改。

## 流程

1. **定位落点**——每个概念与 syncs 各得唯一路径：

   ```text
   docs/prd/README.md        # 总体 PRD（始终集中）
   <模块目录>/CONCEPT.md      # 模块目录已存在时与代码共存
   <syncs 目录>/SYNCS.md      # 转录期单文件
   docs/prd/concepts/<名>.md  # 暂存位，格式同 CONCEPT.md
   docs/prd/SYNCS.md          # 暂存位
   ```

2. **总体 PRD**：需求与 Misfits；概念索引（每概念一行 purpose + 规格链接）；依赖图与子集；排除与未决全量转录。
3. **每概念 CONCEPT.md**：按 `references/templates.md`；OP 的每条 after/then 场景即一条验收场景。
4. **SYNCS.md**：`## coordination graph` 直接转录模型的同步图；按 flow 分节（flow = 一个 `Requesting` 动作触发、多条 sync 接力的动作链），不按域分节；含错误 flow 与排除动作。
5. 逐条核对「命题」后交付。

## 命题

- 模型的每个部分（concepts、syncs、依赖图、排除与未决）都有唯一落点，无遗漏无重复。
- 每份 `CONCEPT.md` 四节不出现其他概念名，无 `## interactions` / `## dependencies` 段。
- 每条验收场景可追溯到某条 OP；文档无模型外的新信息（notes 占位除外）。
- `SYNCS.md` 单文件、有 coordination graph、按 flow 分节；每个可失败动作有错误 sync 或记入排除。
- 总体 PRD 可导航到全部规格文件，链接有效。

## 记法与模板

段落头 `## purpose` / `## state` / `## actions` / `## operational principle` / `## notes` 与 `concept-guardrails`（wyx）一致，`wyx:concept drift`、`wyx:map` 可直接消费；sync 块记法同 `concept-design`。

## 参考

| 何时读 | 文件 |
| --- | --- |
| 流程第 3–4 步：`CONCEPT.md` 与 `SYNCS.md` 模板 | `references/templates.md` |
| 核验"规格即规范"的出处 | `references/sources.md` |
