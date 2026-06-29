---
name: semantic-creator
description: Turns an interface (REST/OpenAPI, CLI, or table/DDL) into a governed Kimball semantic layer via a guided, one-fact-at-a-time interview—confirm facts, grain, dimensions, measures—then emits semantic objects as YAML/markdown or a Google OKF (Open Knowledge Format) bundle. Use when modeling an API/CLI/table into a semantic layer, ontology, or dimensional (star/snowflake) model, or exporting OKF. 触发词：语义层 / 元技能 / 接口(REST/CLI/数据表)转语义 / 事实·粒度·维度·度量 / 维度建模 / 本体 / OKF。Refuses to invent fields, grain, or values the interface does not evidence.
license: Apache-2.0
compatibility: No external tools or network; pure modeling + file generation. Optional YAML/markdown linter.
metadata:
  author: ontology-of-everything
  version: "0.2.0"
---

# Semantic Creator（接口 → 语义层 元技能）

把**接口契约**（REST/OpenAPI、CLI、表/DDL）建成**受治理语义层**：确认事实与粒度 → 挂维度与度量 → 按 Schema 生成，可导出 **Google OKF**（推荐）。

> 唯一真源是接口。**不臆造**字段/粒度/枚举/取值；缺证据停下，一次一问。

## Workflow

### Phase 1 · Ingest & Frame

1. **Ingest** — 接口归一成「操作清单」：每个 op 取 `name / method / safety(读写) / inputs / outputs / doc`（规则见 `references/elicitation-playbook.md` §1）。
2. **Frame** — 每个 op 定一句业务过程，归类 fact / dimension-lookup / scope。按 fact·dimension·measure·time·scope 路由。

### Phase 2 · Confirm（一次一问，每步回显小表待确认）

顺序见 `elicitation-playbook.md` §3：

1. **Facts & Grain** — 「一行=什么」；事实类型（事务 / 周期快照 / 累积快照）、role、parent_fact。
2. **Dimensions** — `kind`（conformed / snowflake / degenerate）/ `business_key` / `source_operations` / `attributes`；共享维度复用，命名稳定。
3. **Measures** — 可加性（additive / semi / non）+ 口径。
4. **Routing & boundary** — `entry_points` + `evidence_boundary`（不能回答什么）。

> 缺 never-assume（grain / business_key / 读写）→ 必须问。缺 safe-default（可选属性、命名）→ 披露后继续。

### Phase 3 · Emit

1. **Target** — `repo-yaml`（Kimball 星型/星座，**默认**）/ `markdown`；`okf`（Google OKF v0.1）为可选导出。
2. **Generate** — 按 `schema-spec.md` 生成；如需 OKF，映射按 `okf-emitter.md`。
3. **Verify** — 跑 `schema-spec.md` §5 Conformance；若导出 OKF，再跑 `okf-emitter.md` §6 三条硬约束。逐条回报 pass/fail。

## Critical Rules

1. **Evidence-only** — 字段/粒度/枚举/取值仅来自接口；缺证据写 `TODO(verify)` 并列入待确认，不编造。
2. **Grain first** — 未锁 grain 不挂维度、不写度量。
3. **One blocking ask** — 仅在改变建模结果处停（一次一问，带候选），不连环问。
4. **Layer split** — 形态/路由/粒度归语义层；可键入或读取的取值（枚举、code、字段路径、命令）归契约层，语义层只指向。
5. **Stable names** — 事实/维度名确认后不重命名（OKF 概念 ID = 文件路径，改名即断链）。

## Reference Index（按需加载）

| 何时读 | 文件 |
| --- | --- |
| Phase 1–2 抽取 + 确认顺序 + 检查表 | `references/elicitation-playbook.md` |
| Phase 3 Schema 约束 + Conformance | `references/schema-spec.md` |
| 可选导出 OKF：映射 / 保留文件 / 硬约束 | `references/okf-emitter.md` |
| 端到端样例 | `references/examples.md` |
