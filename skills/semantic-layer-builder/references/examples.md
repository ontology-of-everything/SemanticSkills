# Worked Example（接口 → 确认 → 语义对象 + OKF）

最小端到端：1 个 REST 操作 → 语义对象（YAML）+ OKF concept。示范节奏，非模板填空。

## 0. 输入物料（REST）

```
GET /v1/orders?store_id&from&to  →  200: { orders: [ { order_id, store_id, placed_at, total_amount, currency, line_count } ] }
GET /v1/stores                   →  200: { stores: [ { store_id, store_name, region } ] }
```

## 1. Ingest → 操作清单

| name | method | safety | inputs | outputs(数组) | doc |
| --- | --- | --- | --- | --- | --- |
| ListOrders | GET | read | store_id, from, to | orders[] | <doc> |
| ListStores | GET | read | — | stores[] | <doc> |

## 2. Frame

- `ListOrders` → **fact**（业务过程：下单）。
- `ListStores` → **dimension-lookup**（门店字典）。

## 3. Confirm（逐项，回显小表）

**Grain**（确认）：

| fact | grain | role |
| --- | --- | --- |
| SalesOrder | orders[] 每个元素一条（一笔订单） | primary |

**Dimensions**（确认）：

| dimension | kind | business_key | source_operations | attributes |
| --- | --- | --- | --- | --- |
| Dim_Store | conformed | store_id | [ListStores] | [store_id, store_name, region] |
| Dim_Currency | conformed | currency | [TODO(verify): 字典接口?] | [currency] |
| Dim_Date | conformed | date | [—] | [date] |

`order_id` → 退化维度（degenerate）。`region` 在 Dim_Store 内，不另列（除非需独立分析）。

**Measures**（确认）：

| measure | additivity | unit | source | notes |
| --- | --- | --- | --- | --- |
| total_amount | additive | currency | total_amount | 跨门店/时间可加 |
| line_count | additive | count | line_count | |

## 4. Emit — repo-yaml（节选）

`catalog.yml`：

```yaml
name: SalesSemanticCatalog
type: semantic_catalog
version: 0.1.0
domain: sales
modeling_method: kimball_star_constellation
description: 薄路由；下单事实 + 门店字典。
entry_points:
  sales_orders:
    primary_facts: [SalesOrder]
    ontology_files: [shared-dimensions.yml, sales-model.yml]
primary_operations: [ListOrders, ListStores]
command_contracts_file: ../related-commands.md
```

`sales-model.yml`：

```yaml
name: SalesModel
type: semantic_ontology
description: 下单事实；对齐 ListOrders.orders[]。
shared_dimensions_file: shared-dimensions.yml
facts:
  - name: SalesOrder
    role: primary
    grain: orders[] 每个元素一条（一笔订单）
    degenerate_dimensions: [order_id]
    dimensions: [Dim_Store, Dim_Currency, Dim_Date]
    attributes:
      - { name: store_id,   type: string,   required: true, dimension: Dim_Store }
      - { name: placed_at,  type: datetime, required: true, dimension: Dim_Date }
      - { name: currency,   type: string,   required: true, dimension: Dim_Currency }
    measures:
      - { name: total_amount, additivity: additive, unit: currency }
      - { name: line_count,   additivity: additive, unit: count }
evidence_boundary:
  - 仅下单事实；退款/履约/库存超出本对象。
```

## 5. Emit — OKF（节选）

`facts/sales_order.md`：

```markdown
---
type: Semantic Fact
title: Sales Order
description: 一笔订单（ListOrders.orders[] 的一个元素）。
role: primary
grain: orders[] 每个元素一条
tags: [sales]
timestamp: 2026-06-29T00:00:00Z
---

# Grain
orders[] 每个元素一条记录（一笔订单）。

# Dimensions
[Store](/dimensions/store.md) · [Currency](/dimensions/currency.md) · [Date](/dimensions/date.md)

# Schema
| field | type | required | dimension |
| --- | --- | --- | --- |
| store_id | string | true | Store |
| placed_at | datetime | true | Date |

# Citations
[1] [ListOrders 文档](<doc>)
```

`dimensions/store.md`、`metrics/total_amount.md` 同法；根 `index.md` 结构见 `okf-emitter.md` §4。

## 6. Verify

- schema-spec §6：catalog 1 个 ✓；SalesOrder 有 grain ✓；Dim_Currency `source_operations`=`TODO(verify)` ⚠ → 交付说明点名。
- okf-emitter §6：所有 concept 有 `type` ✓；根 index 仅 `okf_version` ✓。
