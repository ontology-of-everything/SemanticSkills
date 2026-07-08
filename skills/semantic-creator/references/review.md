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

## §2 HTML 评审报告（模板 + 数据）

**不手写 HTML。** 壳模板 `assets/review-template.html` 已内联 CSS/JS/petite-vue（零外部依赖，无 CDN、无网络）；agent 只产出 model JSON 并注入：

1. 按下方 schema 生成紧凑 model JSON（只放数据，不放任何标记/样式）。
2. 读模板，把占位符 `/*__MODEL_JSON__*/` 整体替换为该 JSON。
3. 写到 `$TMPDIR`（缺省 `/tmp`）下 `semantic-review-<timestamp>.html`，不进 repo；macOS `open` / Linux `xdg-open` 打开，聊天里给绝对路径。

```json
{"meta": {"title": "<域名评审>", "generated_at": "<ISO 8601>", "iteration": 1},
 "cards": [
   {"id": "fact/sales_order", "section": "fact", "title": "SalesOrder",
    "confidence": "confirmed",
    "conclusion": {"grain": "orders[] 每元素一条", "role": "primary",
                   "degenerate_dimensions": ["order_id"]},
    "evidence": ["ListOrders 响应 orders[] 数组结构"]}
 ],
 "open_questions": ["Dim_Currency 字典来源 TODO(verify)"]}
```

- `section`: `fact | dimension | measure | routing`；`confidence`: `confirmed | inferred | assumed`。
- `conclusion` 是键值对象（grain / kind / business_key / additivity 等建模结论，值为字符串或数组）。
- `evidence` 是字符串数组（接口字段路径 / doc url / DDL 行）；含 `TODO(verify)` 的项模板自动高亮。
- 全部 `TODO(verify)` 与 assumed 项汇总进 `open_questions`。

模板自带：分区折叠 + 锚点导航 + 文本过滤、置信度徽章、每卡批注控件（通过/修改/拒绝 + 备注）。

## §3 批注回传

「导出批注」优先复制到剪贴板；`file://` 下剪贴板不可用时模板自动降级为文本框全选 + 下载 `verdicts.json`，用户任选一种回传聊天。只含非 approve 项：

```json
{"verdicts": [
  {"id": "fact/sales_order", "action": "edit", "field": "grain", "note": "一行=一个订单行而非订单头"},
  {"id": "dim/currency", "action": "reject", "note": "不需要"}
], "approved_rest": true}
```

迭代重出报告时，用户可用「导入上轮批注」把上一轮 verdicts 回填到卡片，不必从头点。

## §4 Amendments 迭代

1. 逐条追加到 `$TMPDIR` 下与报告同目录的 `amendments.md`：`日期 + 对象 / 原值 → 新值 / 理由`（新→旧）；Phase 3 落盘时随产物 copy 进输出目录。重跑 skill 时该文件是已确认决策，不再重问。
2. 应用修改（rejected 对象移出模型或归 evidence_boundary）。
3. 重新生成报告（`iteration` +1）再确认。批注与访谈证据冲突且不能机械取舍 → One blocking ask 回给用户，不自行择一。

## §5 退出条件（硬门禁）

**出报告后必须停下**，显式等待用户回传批注/批准；未拿到 `approved_rest: true` **禁止进入 Phase 3**，不得替用户批准或自动前进。

- [ ] 报告全部通过（`approved_rest: true` 且无未处理 verdicts）
- [ ] 无未决 never-assume 缺口；剩余 `TODO(verify)` 已列入交付说明

满足 → 进 Phase 3（`emit-okf.md` 默认 / `emit-yaml.md` 可选）。
