---
name: concept-prd
description: Generates PRD specifications from a confirmed Daniel Jackson concept model, with an overall PRD and colocated CONCEPT.md and SYNCS.md. Use when the user requests a concept PRD, 概念规格文档, or concept-prd; preserve the model without inventing content.
metadata:
  openclaw:
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/concept-prd
---

# 概念 PRD

## 目标

输入：`concept-design` 确认过的模型（concepts、syncs、依赖图、排除与未决）。输出：总体 PRD + 每概念一份 `CONCEPT.md` + 一份 `SYNCS.md`。概念设计即设计规格，本技能只转录与编排。交付后代码落地 → `concept-implementation`；模型缺口 → 回 `concept-design`。

## 原则

1. 只转录，不发明；缺口回上游，不在文档里填补。
2. 跨概念行为与依赖的权威落点为：`SYNCS.md`（行为）与总体 PRD（产品依赖及派生同步图）。概念规格里的上下文只以类型参数列表出现（`Reserving [User, Slot]`），散文备注只进 `## notes`。
3. 规格贴近代码：模块目录已存在就与代码共存，未就绪先集中暂存，落地时由 `concept-implementation` 迁移。
4. 共存规格是模型的权威持久形态；已确认变更可直接做最小编辑，并同步索引/派生图，避免全量生成覆盖人工维护信息。

## 流程

1. **定位落点**——每个概念与 syncs 各得唯一路径：

   ```text
   docs/prd/README.md        # 总体 PRD（始终集中）
   <模块目录>/CONCEPT.md      # 模块目录已存在时与代码共存
   <syncs 目录>/SYNCS.md      # 转录期单文件
   docs/prd/concepts/<名>.md  # 暂存位，格式同 CONCEPT.md
   docs/prd/SYNCS.md          # 暂存位
   ```

2. **总体 PRD**：需求与 Misfits；概念索引（每概念一行 purpose + 规格链接）；同步图与依赖图与子集；排除与未决全量转录。
3. **每概念 CONCEPT.md**：按 `references/templates.md`；principle 导出代表性验收场景；actions/state 的边界与不变量导出补充场景，均附模型出处。
4. **SYNCS.md**：按 `references/templates.md` 转录 `app` / `include` / `sync` 的 when / where / then；用 `// flow:` 注释分组，不按域分节；含错误 sync。
5. 逐条核对「命题」后交付。

## 命题

- 模型的每个部分（concepts、syncs、依赖图、排除与未决）都有唯一落点，无遗漏无重复。
- 每份 `CONCEPT.md` 四节不依赖其他概念定义（同名局部类型参数合法），无 `## interactions` / `## dependencies` 段。
- 每条验收场景可追溯到 principle 或动作/状态契约；文档无模型外的新信息（notes 占位除外）。
- `SYNCS.md` 单文件、`app` + `include` + `sync` 块；可达失败有明确处理策略；查询空集不冒充错误输出。
- 总体 PRD 可导航到全部规格文件，链接有效。

## 记法与模板

`CONCEPT.md` / `SYNCS.md` 采用基于 *Beyond Objects* 的本仓 Markdown 记法（见 `references/templates.md`），与 `concept-design` 产出一致。`wyx:concept drift`、`wyx:map` 按同一记法消费。

## 参考

| 何时读 | 文件 |
| --- | --- |
| 流程第 3–4 步：`CONCEPT.md` 与 `SYNCS.md` 模板 | `references/templates.md` |
| 流程第 3–4 步：填好的餐厅订位例（转录后的文件形态） | `references/example-reserving.md` |
| 核验"规格即规范"的出处 | `references/sources.md` |
