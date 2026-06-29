# Semantic Object Schema（语义对象 Schema 约束）

Phase 3 产物必须符合本 Schema。建模法：Kimball 星型/星座。三类文件：**catalog（薄路由）** → **shared-dimensions（一致性维度）** → **model（事实）**。OKF 形态见 `okf-emitter.md`。

铁律：形态/路由/粒度 → 语义层；可键入或读取的取值（枚举、code、字段路径、命令）→ 契约层，语义层只指向。

## 1. `semantic_catalog`（路由，1 个）

```yaml
name: <PascalCaseName>
type: semantic_catalog
version: <semver>
domain: <snake_case_domain>
modeling_method: kimball_star_constellation
description: <一句话；薄路由，触发词/对话流不放这里>
entry_points:
  <entry_key>:                 # 按场景
    <axis>: <value>            # 可选路由轴（如 time）
    primary_facts: [<Fact>, ...]
    ontology_files: [<file>, ...]
primary_operations: [<Service/Operation>, ...]
primary_doc_urls: [<url>, ...]
command_contracts_file: <相对路径或 null>   # 指向契约层
```

约束：`name/type/domain/entry_points` 必填；每个 entry_point 至少 1 个 `ontology_files`；catalog 不得内联事实/维度定义。

## 2. `semantic_ontology` — shared dimensions（一致性维度，按需 1 个）

```yaml
name: <Name>
type: semantic_ontology
description: <共享维度集；被各 model 引用>
source_evidence: { <key>: <url> }     # 可选，证据出处
dimensions:
  - name: Dim_<Name>                  # PascalCase，以 Dim_ 前缀
    kind: <见 §4>
    business_key: <field>
    parent_dimension: <Dim_*>         # 仅 snowflake
    source_operations: [<Service/Operation>, ...]
    source_documents: [<url>, ...]    # 无 List API 时
    attributes: [<field>, ...]
    notes: <可选>
evidence_boundary: [<句>, ...]
```

## 3. `semantic_ontology` — model（事实，每个业务过程/计费模式 1 个）

```yaml
name: <Name>
type: semantic_ontology
description: <对齐哪个 operation 的哪段结构>
<axis>: <value>                       # 可选路由轴，与 catalog 对应
shared_dimensions_file: <相对路径>
facts:
  - name: <Fact>                      # PascalCase
    role: primary | child
    grain: <一句可证伪的粒度>
    parent_fact: <Fact>               # 仅 child
    child_facts: [<Fact>, ...]        # 仅 primary
    cardinality_max: <int>            # 可选
    degenerate_dimensions: [<field>, ...]
    dimensions: [Dim_<Name>, ...]     # 引用 §2/§4 的维度名
    attributes:
      - name: <field>
        type: string|integer|number|boolean|date|datetime
        dimension: Dim_<Name>         # 该列是某维度的外键时
        required: true | false | conditional
        condition: <when conditional>
        max_length: <int>             # 可选
        min: <n>; max: <n>            # 可选
        notes: <取值/枚举指向契约层>
    measures:                         # 可加性度量
      - { name: <field>, additivity: additive|semi_additive|non_additive, unit: <或指向契约层>, notes: <basis> }
evidence_boundary: [<句>, ...]
```

约束：每个 fact 必有 `name/role/grain`；`child` 必有 `parent_fact`；`dimensions` 中每名必须在 shared-dimensions 或本文件可解析；可被键入/读取的枚举值不得写进 `attributes`（只在 `notes` 指向契约层）。

## 4. Dimension `kind` 取值

| kind | 用途 | 必填 |
| --- | --- | --- |
| `conformed_dimension` | 跨事实复用的一致性维度 | business_key, source_operations |
| `snowflake_dimension` | 规范化子维（挂在父维下） | business_key, parent_dimension |
| `degenerate`（不单列） | 事实里的裸键 | 记于 fact.degenerate_dimensions |

## 5. Conformance（生成后必跑，逐条回报）

1. 恰好 1 个 `semantic_catalog`；其 `entry_points.*.ontology_files` 指向存在的 model/shared 文件。
2. 每个 `semantic_ontology` 有 `name` + `type`。
3. 每个 fact 有 `name/role/grain`；child 有 `parent_fact` 且其父存在。
4. fact `dimensions[]` 每个名字能在 shared-dimensions 或本文件解析。
5. 无内联枚举/code/字段路径取值（grep 反例：长枚举表、`documented_examples` 代码目录）→ 应在契约层。
6. 每个文件有 `evidence_boundary`（catalog 除外）。
7. 无悬空引用：`dimension:`/`parent_dimension:`/`parent_fact:` 目标均存在。
8. 所有 `TODO(verify)` 已列入交付说明的待确认清单（允许保留，但必须可见）。

任一 fail → 修复或回到确认步骤；不得「静默通过」。
