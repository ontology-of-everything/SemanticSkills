# Elicitation Playbook（抽取 + 逐项确认）

驱动 Phase 1–2：把接口变成可生成的 fact / grain / dimension / measure。每步回显小表，确认后再前进。

## §1 Ingest — 物料归一

每个 operation 抽取 `name / method / safety(read|write) / inputs[] / outputs[] / doc`。

| 物料 | 抽取 | grain 线索 |
| --- | --- | --- |
| **REST/OpenAPI** | path+method=op；`parameters`/`requestBody`=inputs；`responses.2xx.schema`=outputs | 响应 `array` → 一行=元素；单对象 → 一行=资源时点 |
| **CLI** | 子命令=op；flags=inputs；`--output`/示例 JSON=outputs；`list/describe/show`=读，`create/update/delete/pay`=写 | `list*`→明细事实；`show*/get*`→快照 |
| **表/DDL/CSV** | 表=事实或维度；列=attribute/measure；PK=business_key 或 degenerate；FK=维度引用 | 唯一键组合=grain |

> 写操作标 `safety: write`；若语义层定位只读，则归 `evidence_boundary`，不建模为事实。
> 证据缺口 → `TODO(verify): <来源>`，列入待确认，不猜。

## §2 Frame — 角色

| 角色 | 判定 |
| --- | --- |
| **fact** | 度量某业务过程/事件（`list*` 明细或可聚合快照） |
| **dimension-lookup** | 翻译/枚举 code 的字典 |

## §3 Confirm — 顺序（一次一问）

### 3.1 Facts & Grain（最先，最关键）

| fact | grain（一行=什么） | role | parent_fact | cardinality_max |
| --- | --- | --- | --- | --- |

- grain 必须**可证伪**（如「product_infos[] 每元素一条」）。
- 请求头 vs 明细行 → header(primary) + line(child, parent_fact=header)。
- grain 不明 → 给 2–4 候选让用户选（never-assume）。

### 3.2 Dimensions

| dimension | kind | business_key | source_operations | attributes | parent_dimension |
| --- | --- | --- | --- | --- | --- |

`kind` 取值见 `schema-spec.md` §4。

- 同义维度跨事实复用一个，不重复定义。
- 退化键（如 `id`）记入 fact.`degenerate_dimensions`，不单列。
- 缺 business_key / source_operations → 问或 `TODO(verify)`。

### 3.3 Measures

| measure | additivity | unit / basis | source field | notes |
| --- | --- | --- | --- | --- |

additivity：`additive`（跨所有维可加）/ `semi_additive`（如余额，不跨时间）/ `non_additive`（比率）。单位枚举值归契约层。

### 3.4 Routing & Boundary

- `entry_points`：每场景 → primary_facts + ontology_files。
- `evidence_boundary`：逐条写「不能回答什么」（粒度/口径/范围外）。

## §4 Gate（进 Phase 3 前）

- [ ] 每个事实有已确认的 grain
- [ ] 每个维度有 kind + business_key（或 `TODO(verify)`）
- [ ] 每个度量有 additivity
- [ ] 写操作已 frame（建模或归 boundary）
- [ ] 无未决 never-assume 缺口

任一未满足 → 回 §3，不生成。
