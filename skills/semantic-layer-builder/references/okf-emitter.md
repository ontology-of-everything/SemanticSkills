# Google OKF Emitter（导出 Open Knowledge Format v0.1）

把 `schema-spec.md` 的语义对象导出成 **OKF v0.1** bundle：markdown 文件目录，每文件一 concept，frontmatter 用 YAML。唯一硬要求：每个非保留 `.md` 有可解析 frontmatter 且含非空 `type`，其余皆软约定。来源：Open Knowledge Format v0.1（Google Cloud, 2026-06）。

## 1. Bundle 布局

```text
<bundle>/                         # = semantic_catalog.domain
├── index.md                      # 保留：根目录清单（唯一可带 frontmatter 的 index）
├── log.md                        # 保留（可选）：变更历史，新→旧
├── facts/
│   ├── index.md
│   └── <fact>.md                 # 每个 fact 一个 concept
├── dimensions/
│   ├── index.md
│   └── <dim>.md                  # 每个 dimension 一个 concept
├── metrics/
│   └── <measure>.md              # 每个 measure 一个 concept（可选拆）
└── references/
    └── <operation>.md            # 每个 source operation 一个 API Endpoint concept
```

Concept ID = 去掉 `.md` 的 bundle 相对路径（`facts/rfq_line`）。**ID = 文件路径 = 身份**；确认后不重命名（会断链）。

## 2. 语义对象 → OKF concept 映射

| 语义对象 | OKF `type` | 落点 | body 约定段 |
| --- | --- | --- | --- |
| semantic_catalog | `Semantic Catalog` | 根 `index.md`（带 `okf_version`） | 见 §4 |
| fact | `Semantic Fact` | `facts/<fact>.md` | `# Grain` / `# Dimensions` / `# Schema` / `# Citations` |
| dimension | `Dimension` | `dimensions/<dim>.md` | `# Schema`（attributes 表）/ `# Selection`（abstract）/ `# Citations` |
| measure | `Metric` | `metrics/<measure>.md` | `# Definition`（additivity, basis, unit）/ `# Citations` |
| source operation | `API Endpoint` | `references/<op>.md` | `# Schema`（inputs/outputs）/ `# Citations` |

`time` / `scope` 路由轴 → frontmatter `tags` 或 prose。OKF 链接为无类型有向边，关系语义靠 prose（「joins-with」「parent of」）。

## 3. Concept frontmatter（必填 + 推荐）

```yaml
---
type: <见 §2>                    # 必填，唯一硬要求
title: <人类可读名>
description: <一句话>
resource: <底层资产 URI；抽象概念可省>   # 如 doc url / 表 URI
tags: [<domain>, <axis:value>, ...]
timestamp: <ISO 8601>
# 可加生产者自定义键（消费者须容忍未知键）
---
```

扩展键：把结构化属性（`grain`/`kind`/`business_key`/`additivity`/`role`/`parent_fact`）作为额外 frontmatter 键，便于 agent 检索；body 用结构化 markdown 同步给人读。

## 4. 保留文件

### `index.md`（根）

唯一允许 frontmatter 的 index，只放 `okf_version`：

```markdown
---
okf_version: "0.1"
---

# Facts
* [RFQ Line](facts/rfq_line.md) - product_infos[] 每元素一条
# Dimensions
* [Cloud Service Type](dimensions/cloud_service_type.md) - 服务类目
```

子目录 `index.md` **不带 frontmatter**，只列本目录条目（带描述）。

### `log.md`（可选）

```markdown
# Update Log
## 2026-06-29
* **Initialization**: 从 <interface> 生成首版 bundle。
```

日期用 `YYYY-MM-DD`，新→旧；前导加粗词（**Update**/**Creation**/**Deprecation**）是约定非强制。

## 5. 交叉链接

- 用 bundle 绝对路径（`/` 开头）：`[customers](/dimensions/customers.md)`，移动子目录仍稳。
- 关系类型由 prose 表达；消费者须容忍断链（未写知识不算错）。
- 外部来源放 `# Citations` 编号列表，可指向 `references/` 内镜像 concept。

完整 concept 示例（含 frontmatter + body 段）见 `examples.md` §5。

## 6. OKF Conformance（导出后必跑）

1. 每个非保留 `.md` 有可解析 YAML frontmatter。
2. 每个 frontmatter 有非空 `type`。
3. `index.md`/`log.md` 符合 §4（根 index 仅 `okf_version`）。

逐条回报 pass/fail；并跑 `schema-spec.md` §6（OKF 是承载，不替代语义校验）。
