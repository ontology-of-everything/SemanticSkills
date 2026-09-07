---
name: concept-audit
description: Audits an existing codebase against its Jackson concept model (spec drift with calibrated severity checklists, boundaries, criteria, composition, dependencies, cross-spec validation). Use this skill whenever the user asks to audit a concept model, 概念审计, or mentions concept-audit (formerly jackson-concept-audit); read-only.
---

# Jackson 概念审计

输入：概念规格（与代码共存的 CONCEPT.md / SYNCS.md，以及被审计仓库集中 PRD 目录下的总体 PRD——两处都找）+ 代码库。**只读**：不修改任何文件，产出发现清单；修复由路由到的技能执行。无规格文档时降级为纯边界与判据审计，并在报告中声明。

## 五个维度

| 维度 | 检查 | 发现路由 |
| --- | --- | --- |
| **规格漂移** | 规格 ↔ 代码逐类别对账（见下方检查表与校准） | 文档过期 → `concept-prd`；模型过期 → `concept-design`；代码缺陷 → `concept-implementation` |
| **边界违规** | 概念模块互引、共享表或全局数据模型、DTO/传输类型进概念签名、业务不变量出现在 syncs 层 | `concept-implementation` |
| **判据重审** | 用资格判据与四词审存量模块：一模块多目的（conflation）、目的碎片化（fragmentation）、无理由背离熟悉概念、非 user-facing 的基础设施被当成概念 | `concept-design` |
| **组合质量** | 欠同步（漏自动化）、过同步（抢用户控制）、可失败动作缺错误 sync、概念动作直通外部 API、sync 积攒自有状态（升格信号） | 模型层 → `concept-design`；代码层 → `concept-implementation` |
| **依赖与子集** | 总体 PRD 依赖图与代码实际依赖不符、违反 Parnas 规则（合理的产品子集被不当依赖阻断）、MVP 子集不可裁剪构建 | `concept-design` |

## 执行步骤

1. **定位规格**：Glob 找全部 CONCEPT.md / SYNCS.md 与集中 PRD 目录；同时利用工程自带素材（Spring Modulith `Documenter` 模块文档、cargo/dependency-cruiser 依赖图输出）。
2. **逐份对账**：每份规格连同其实现代码按检查表过一遍；规格 ≥5 份时按「并行扫描」派发。
3. **跨规格校验**：SYNCS.md 引用的动作/查询在目标 CONCEPT.md 中逐一核对（见跨规格表）。
4. **合并根因与系统性聚合**：同一问题跨维度出现时合并指向根因；同一类别+描述出现在 3 份以上规格时归为系统性问题，不逐条列。
5. **输出报告**：给出修复顺序，上游优先——先模型（design）、再文档（prd）、后代码（implementation）。

## 漂移检查表

每份 `CONCEPT.md`（queries 按 action 同规则对待）：

| 类别 | 如何识别 | 严重度 |
| --- | --- | --- |
| **Missing action** | 公开函数/方法在代码里存在，规格 `## actions` 没声明 | Medium |
| **Removed action** | 规格声明了动作，代码里已不存在 | High |
| **Changed signature** | 参数/返回与规格不一致（追踪实际 return，不只看类型标注；错误 case 增减也算） | Medium |
| **New state** | 新表字段、类字段或持久化数据不在 `## state`（含 schema/迁移脚本里的） | Medium |
| **Spec naming violation** | 四节（purpose/state/actions/OP）点名其他概念，或出现 interactions / dependencies 段 | High（路由 prd/design） |
| **Boundary violation** | 代码直接引用另一概念模块内部（未走声明的动作） | Critical |
| **Cross-cutting parameter** | 某参数出现在 3 个以上动作实现里，`## actions` 任何签名都没记录 | Medium |
| **OP 无测试** | OP 的 after/then 场景没有对应集成测试 | Medium |
| **排除动作被使用** | 模型标为排除的动作被组合层调用或经 API 暴露 | High |

每份 `SYNCS.md`：

| 类别 | 如何识别 | 严重度 |
| --- | --- | --- |
| **Missing sync** | 代码里新增的跨概念协调未声明 | Medium |
| **Removed sync** | 规格声明了 sync，代码处理器已不存在 | High |
| **Changed trigger** | 代码触发方式与 when 声明不同（如定时 vs 动作后） | Medium |
| **New participant** | sync 实现涉及规格没列出的概念 | High |
| **Graph inconsistency** | coordination graph 与 sync 块互不对应 | Medium |

跨规格校验（逐份检查完之后）：

| 类别 | 如何识别 | 严重度 |
| --- | --- | --- |
| **SYNCS→CONCEPT missing reference** | sync 块引用的 `Concept.action` / `Concept._query` 在目标 CONCEPT.md 里不存在 | High |
| **SYNCS→CONCEPT missing participant** | sync 块点名的概念没有 CONCEPT.md | Medium |
| **依赖图不符** | 总体 PRD 依赖图与 SYNCS.md/代码实际依赖不一致 | Medium（归依赖与子集维度） |

## 严重度校准

- **规格的沉默不是漂移**：规格没提到的行为是未记录，不是被否定；只有针对规格明确陈述的矛盾才算矛盾。Missing action / New state 这类"暴露未记录新增"的检查不受此条影响。
- **严重度逐字采用检查表取值**：不凭影响面判断在类别内升级；比类别更严重的发现应**重新归类**（如 Missing action 实为跨概念内部访问 → Boundary violation/Critical）。允许按下列规则下调。
- 私有辅助函数、内部实现细节（私有缓存、派生值）→ Low；规格签名比语言包装（异步、Result 包装）更简单且不改变契约 → Low。
- 命名风格差异（camelCase/snake_case）→ Low；但该名字出现在跨规格引用里时重新归类为跨规格类别（High），不是类别内升级。
- 同一条 Low 在一份规格多个动作重复 → 合并为一条，附注受影响动作；单份规格去重后 ≥5 条 Low → 在摘要注明并建议重审该规格。
- 报 Medium 及以上前，用 grep 或读文件确认发现存在于**当前**代码，不凭记忆或旧印象。

## 并行扫描

规格 ≥5 份时用只读子代理并行对账。派发规则：

- **显式指定强档模型**，不继承会话档位——对账要给出「不存在」类断言（如 `Missing action: clean`），错误判定不产生可察觉输出，弱模型漏报无法被发现。
- 每个子代理分配 2–3 份相邻规格；提示词附上「严重度校准」整段与对应检查表（严重度取值逐字照抄，不得自行上调）。
- 每个检查类别都必须给判定，省略视为未核实；合并阶段把未核实类别标出。
- 全部返回后，在主上下文做跨规格校验与系统性聚合。

## 报告格式

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

## 完成条件

- 五维度全部执行，或明确声明跳过原因。
- 每条发现有位置与证据，可独立复核；无「疑似」空泛项；每个检查类别有判定或标未核实。
- 严重度全部出自检查表并遵守校准规则（只降不升、越级重新归类）。
- 每条发现有唯一路由；修复顺序按上游优先排列。
- 未修改任何文件。

## 依据

Jackson：

- 批评循环与判据（`concept-design`；user-facing 判据见[资格判据教程](https://essenceofsoftware.com/tutorials/concept-basics/criteria/)）
- 欠/过同步与 mediator 原则（[概念设计综述](https://essenceofsoftware.com/posts/distillation/)）
- Parnas 规则（[依赖与子集教程](https://essenceofsoftware.com/tutorials/concept-basics/dependency/)）
- 规范可从代码提取（[WYSIWID 论文](https://arxiv.org/abs/2508.14511)）；现行记法（[Beyond Objects](https://arxiv.org/abs/2606.27258)）

业界：漂移检查表、严重度校准与并行扫描机制改编自 [jlifyio/wyx](https://github.com/jlifyio/wyx)（本仓 `concept-guardrails` 的上游），适配到零点名的 Jackson 规格格式；架构 fitness functions 管持续（CI 工具见 `concept-implementation` 语言参考），审计管周期，两层互补。
