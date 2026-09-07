---
name: concept-audit
description: Audits a codebase against its concept model (Daniel Jackson's concept design)—are concepts truly independent, is their sync composition free of defects—plus spec drift, criteria, and dependency integrity, with calibrated severities and fix routing. Use whenever the user asks to audit a concept model, 概念审计, or mentions concept-audit; read-only.
---

# 概念审计

## 目标

输入：概念规格（与代码共存的 `CONCEPT.md` / `SYNCS.md`，以及集中 PRD 目录下的总体 PRD——两处都找）+ 代码库。输出：带证据与路由的发现清单和修复顺序。**只读**：不修改任何文件；修复由路由到的技能执行。无规格文档时降级为纯独立性、组合与判据审计，并在报告中声明。

审计回答两个主问题：**概念是否真独立**（每个概念离开其他概念仍可理解、可实现、可测试），**概念的组合是否有缺陷**（sync 层是否违背因果语义、漏掉联动或抢走控制）。其余三维为这两问提供证据。

## 原则

1. 每条发现有位置与证据，可独立复核；无「疑似」空泛项。
2. 严重度逐字出自检查表；只降不升，越级则重新归类。
3. 规格的沉默不是漂移：只有针对规格明确陈述的矛盾、或违背因果语义的组合才算问题。
4. 每条发现唯一路由；修复顺序上游优先——先模型（design）、再文档（prd）、后代码（implementation）。
5. 报 Medium 及以上前，用 grep 或读文件确认发现存在于**当前**代码。

## 流程

1. **定位规格**：Glob 找全部 `CONCEPT.md` / `SYNCS.md` 与集中 PRD 目录；同时利用工程自带素材（Spring Modulith `Documenter` 文档、cargo / dependency-cruiser 依赖图）。
2. **规格漂移**：读 `references/drift-checklist.md`，每份规格连同其实现代码过检查表；规格 ≥5 份时按该文「并行扫描」派发。
3. **独立性**：每个概念模块查——互引其他概念模块、共享表或全局数据模型、DTO / 传输类型进签名、规格四节点名其他概念或含 interactions / dependencies 段。
4. **组合缺陷**：读 `references/composition-checklist.md`，对 `SYNCS.md` 与组合层代码逐类别判定。
5. **判据重审**：用资格五条与四词审存量模块——一模块多目的（conflation）、目的碎片化（fragmentation）、无理由背离熟悉概念、非 user-facing 的基础设施被当成概念。
6. **依赖与子集**：总体 PRD 依赖图 ↔ 代码实际依赖；Parnas 违规（合理子集被不当依赖阻断）；MVP 子集能否裁剪构建。
7. **跨规格校验与聚合**：`SYNCS.md` 引用的动作 / 查询逐一在目标 `CONCEPT.md` 核对；同一问题跨维度出现时合并指向根因；同一类别 + 描述出现在 3 份以上规格时归为系统性问题。
8. **输出报告**（模板见下），逐条核对「命题」。

## 命题

- 五维度全部执行，或明确声明跳过原因；每个检查类别有判定或标「未核实」。
- 每条发现有位置、证据、严重度、路由四项，严重度出自检查表且遵守校准。
- 独立性维度对每个概念模块给出结论（独立 / 违规 + 证据）。
- 组合缺陷维度对每个 flow 给出结论；欠 / 过同步的发现附用户视角场景。
- 系统性模式合并陈述，不逐条重复；修复顺序按上游优先排列。
- 未修改任何文件。

## 记法与模板

| 维度 | 问题 | 发现路由 |
| --- | --- | --- |
| 规格漂移 | 规格 ↔ 代码是否仍一致 | 文档过期 → `concept-prd`；模型过期 → `concept-design`；代码缺陷 → `concept-implementation` |
| 独立性 | 概念是否真独立 | 代码耦合 → `concept-implementation`；规格点名 → `concept-prd` / `concept-design` |
| 组合缺陷 | sync 层是否违背因果语义、漏联动、抢控制 | 模型层 → `concept-design`；代码层 → `concept-implementation` |
| 判据重审 | 存量模块是否够格为概念 | `concept-design` |
| 依赖与子集 | 依赖图是否真实、子集是否可裁剪 | `concept-design` |

```markdown
# 审计报告 <日期>
范围: <规格版本 / 代码版本>；跳过的维度及原因
Summary: 规格 <N> 份，有漂移 <N> 份；Critical <N> / High <N> / Medium <N> / Low <N>

## <维度名>
| 发现 | 位置 | 证据 | 严重度 | 路由 |

## 跨规格校验
（同表结构）

## 系统性模式
- <出现在 3+ 份规格的同类问题，合并陈述并给批量处理建议>

## 修复顺序
1. <根因级发现，上游优先>
```

## 参考

| 何时读 | 文件 |
| --- | --- |
| 流程第 2 步：CONCEPT.md / SYNCS.md / 跨规格检查表、严重度校准、并行扫描派发 | `references/drift-checklist.md` |
| 流程第 4 步：组合缺陷检查表与校准 | `references/composition-checklist.md` |
| 核验判据出处 | `references/sources.md` |
