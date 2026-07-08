---
name: semantic-creator
description: Turns an interface (REST/OpenAPI, CLI, or table/DDL) into a governed Kimball semantic layer via a guided interview and an interactive HTML design-review report—confirm facts, grain, dimensions, measures—then emits a Google OKF (Open Knowledge Format) bundle by default, or repo YAML. Use when modeling an API/CLI/table into a semantic layer, ontology, or dimensional (star/snowflake) model, or exporting OKF. 触发词：语义层 / 元技能 / 接口(REST/CLI/数据表)转语义 / 事实·粒度·维度·度量 / 维度建模 / 本体 / OKF。Refuses to invent fields, grain, or values the interface does not evidence.
license: Apache-2.0
compatibility: No external tools or network; pure modeling + file generation. Review report is a self-contained HTML file (inline CSS/JS, no CDN).
metadata:
  author: ontology-of-everything
  version: "0.3.0"
---

# Semantic Creator（接口 → 语义层 元技能）

把**接口契约**（REST/OpenAPI、CLI、表/DDL）一次通过地建成**受治理语义层**。四个阶段严格串行，每阶段一个参考文件、一组退出条件——满足才前进，不满足不硬闯：

```text
Phase 1 Ingest → Phase 2 Review → Phase 3 Emit → Phase 4 Verify
   ingest.md       review.md      emit-okf.md      verify.md
                                  emit-yaml.md
```

> 唯一真源是接口。**不臆造**字段/粒度/枚举/取值；缺证据停下，一次一问。

## Workflow

### Phase 1 · Ingest（`references/ingest.md`）

接口归一成「操作清单」，每个 op 判定角色（fact / dimension-lookup）。
**退出条件**：清单完整，每个 op 有角色与读写标记。

### Phase 2 · Review（`references/review.md`）

访谈收集 fact/grain、dimension、measure、routing/boundary——每项带证据出处与置信度；汇成**交互式 HTML 评审报告**给用户批注；批注 JSON 回粘 → `amendments.md` → 应用 → 重出报告。
**退出条件**：报告全部通过，无未决 never-assume 缺口。

### Phase 3 · Emit（`references/emit-okf.md` 默认 / `references/emit-yaml.md` 可选）

默认生成 **Google OKF v0.1** bundle；用户明确要求时生成 repo-YAML（Kimball 星型）。字段语义两个目标共享（定义在 `emit-yaml.md` §2–§4）。≥2 个 bundle 时生成薄根索引。
**退出条件**：产物文件完整落盘。

### Phase 4 · Verify（`references/verify.md`）

跑结构检查 + 语义 lint +（如导出 OKF）OKF 硬约束，逐条回报 pass/fail。
**退出条件**：全部 pass；不可机械修复的 fail → 回 Phase 2 One blocking ask，不静默通过。

## Critical Rules

1. **Evidence-only** — 字段/粒度/枚举/取值仅来自接口；缺证据写 `TODO(verify)` 并列入待确认，不编造。
2. **Grain first** — 未锁 grain 不挂维度、不写度量。
3. **One blocking ask** — 仅在改变建模结果处停（一次一问，带候选），不连环问；批量确认走 HTML 评审。
4. **Layer split** — 形态/路由/粒度归语义层；可键入或读取的取值（枚举、code、字段路径、命令）归契约层，语义层只指向。
5. **Stable names** — 事实/维度名确认后不重命名（OKF 概念 ID = 文件路径，改名即断链）。

## Reference Index（按阶段加载）

| 阶段 | 文件 |
| --- | --- |
| Phase 1 物料归一 + 角色判定 | `references/ingest.md` |
| Phase 2 访谈 + HTML 评审 + amendments | `references/review.md` |
| Phase 3 默认目标 OKF 布局/映射 | `references/emit-okf.md` |
| Phase 3 可选目标 YAML + 共享字段语义 | `references/emit-yaml.md` |
| Phase 4 全部校验 + 升级回路 | `references/verify.md` |
| 端到端样例 | `references/examples.md` |
