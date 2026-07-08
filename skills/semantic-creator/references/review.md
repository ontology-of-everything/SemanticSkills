# Phase 2 · Review（访谈收集 + HTML 评审 + 迭代）

输入：Phase 1 操作清单。产出：**用户批准的建模决策集**（含 `amendments.md` 迭代记录）。
流程：§1 收集 → §2 出报告 → §3 批注回传 → §4 迭代，直到通过。

## §1 访谈收集（按序，每项记录结论 + 证据出处 + 置信度）

置信度三级：`confirmed`（用户或接口明证）/ `inferred`（由结构推断）/ `assumed`（safe-default）。

1. **Facts & Grain**（最先，最关键）— grain 必须**可证伪**（如「product_infos[] 每元素一条」）；请求头 vs 明细行 → header(primary) + line(child, parent_fact=header)；grain 不明 → 阻塞提问，给 2–4 候选（never-assume）。
2. **Dimensions** — `kind` / `business_key` / `source_operations` / `attributes` / `parent_dimension`（字段约束见 `emit-yaml.md` §4）；同义维度跨事实复用一个；退化键（如 `id`）记入 fact.`degenerate_dimensions`，不单列。
3. **Measures** — additivity：`additive`（跨所有维可加）/ `semi_additive`（如余额，不跨时间）/ `non_additive`（比率）+ 单位口径；单位枚举值归契约层。
4. **Routing & Boundary** — `entry_points`（每场景 → primary_facts + 文件）；`evidence_boundary` 逐条写「不能回答什么」。

> 阻塞提问只用于 never-assume 缺口（grain / business_key / 读写语义）；可选属性、命名等 safe-default 标 inferred/assumed，留给报告批注。

出报告前自检：每个事实有 grain 草案、每个维度有 kind+business_key（或 `TODO(verify)`）、每个度量有 additivity、写操作已 frame、每项带证据与置信度。任一缺 → 补齐再出。

## §2 HTML 评审报告

- 写到 `$TMPDIR`（缺省 `/tmp`）下 `semantic-review-<timestamp>.html`，不进 repo；macOS `open` / Linux `xdg-open` 打开，聊天里给绝对路径。
- **零外部依赖**：内联 CSS + 内联 JS，无 CDN、无网络。
- 每个 fact / dimension / measure / entry_point 一张卡片：

| 区块 | 内容 |
| --- | --- |
| 标题 | 对象名 + 类型（Fact / Dimension / Measure / Routing） |
| 结论 | grain、kind/business_key、additivity 等建模结论 |
| 证据 | 出处（接口字段路径 / doc url / DDL 行）；`TODO(verify)` 高亮 |
| 置信度徽章 | `confirmed`（绿）/ `inferred`（黄）/ `assumed`（灰） |
| 批注控件 | 单选：通过 / 修改 / 拒绝 + 备注输入框 |

- 头部放图例；尾部放**开放问题**清单（全部 `TODO(verify)` 与 assumed 项）。

## §3 批注回传（剪贴板）

底部「导出批注」按钮：序列化所有卡片状态为紧凑 JSON 并复制到剪贴板，用户回聊天粘贴。只含非 approve 项：

```json
{"verdicts": [
  {"id": "fact/sales_order", "action": "edit", "field": "grain", "note": "一行=一个订单行而非订单头"},
  {"id": "dim/currency", "action": "reject", "note": "不需要"}
], "approved_rest": true}
```

## §4 Amendments 迭代

1. 逐条追加到输出目录 `amendments.md`：`日期 + 对象 / 原值 → 新值 / 理由`（新→旧）。重跑 skill 时该文件是已确认决策，不再重问。
2. 应用修改（rejected 对象移出模型或归 evidence_boundary）。
3. 重新生成报告再确认。批注与访谈证据冲突且不能机械取舍 → One blocking ask 回给用户，不自行择一。

## §5 退出条件

- [ ] 报告全部通过（`approved_rest: true` 且无未处理 verdicts）
- [ ] 无未决 never-assume 缺口；剩余 `TODO(verify)` 已列入交付说明

满足 → 进 Phase 3（`emit-okf.md` 默认 / `emit-yaml.md` 可选）。
