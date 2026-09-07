# 漂移检查表、严重度校准、并行扫描

流程第 2–3 步（规格漂移维度）读本文。检查表与校准改编自 jlifyio/wyx，适配到零点名的概念规格格式。

## 每份 CONCEPT.md（queries 按 action 同规则对待）

| 类别 | 如何识别 | 严重度 |
| --- | --- | --- |
| **Missing action** | 公开函数/方法在代码里存在，规格 `## actions` 没声明 | Medium |
| **Removed action** | 规格声明了动作，代码里已不存在 | High |
| **Changed signature** | 参数/返回与规格不一致（追踪实际 return，不只看类型标注；错误 case 增减也算） | Medium |
| **New state** | 新表字段、类字段或持久化数据不在 `## state`（含 schema/迁移脚本里的） | Medium |
| **Spec naming violation** | 四节点名其他概念，或出现 interactions / dependencies 段 | High（路由 prd/design） |
| **Boundary violation** | 代码直接引用另一概念模块内部（未走声明的动作） | Critical |
| **Cross-cutting parameter** | 某参数出现在 3 个以上动作实现里，`## actions` 任何签名都没记录 | Medium |
| **OP 无测试** | OP 的 after/then 场景没有对应集成测试 | Medium |
| **排除动作被使用** | 模型标为排除的动作被组合层调用或经 API 暴露 | High |

## 每份 SYNCS.md

| 类别 | 如何识别 | 严重度 |
| --- | --- | --- |
| **Missing sync** | 代码里新增的跨概念协调未声明 | Medium |
| **Removed sync** | 规格声明了 sync，代码处理器已不存在 | High |
| **Changed trigger** | 代码触发方式与 when 声明不同（如定时 vs 动作后） | Medium |
| **New participant** | sync 实现涉及规格没列出的概念 | High |
| **Graph inconsistency** | coordination graph 与 sync 块互不对应 | Medium |

## 跨规格校验（逐份检查完之后）

| 类别 | 如何识别 | 严重度 |
| --- | --- | --- |
| **SYNCS→CONCEPT missing reference** | sync 块引用的 `Concept.action` / `Concept._query` 在目标 CONCEPT.md 里不存在 | High |
| **SYNCS→CONCEPT missing participant** | sync 块点名的概念没有 CONCEPT.md | Medium |
| **依赖图不符** | 总体 PRD 依赖图与 SYNCS.md/代码实际依赖不一致 | Medium（归依赖与子集维度） |

## 严重度校准

- **规格的沉默不是漂移**：规格没提到的行为是未记录，不是被否定；只有针对规格明确陈述的矛盾才算矛盾。Missing action / New state 这类"暴露未记录新增"的检查不受此条影响。
- **严重度逐字采用检查表取值**：不凭影响面在类别内升级；比类别更严重的发现应**重新归类**（如 Missing action 实为跨概念内部访问 → Boundary violation/Critical）。允许按下列规则下调。
- 私有辅助函数、内部实现细节（私有缓存、派生值）→ Low；规格签名比语言包装（异步、Result 包装）更简单且不改变契约 → Low。
- 命名风格差异（camelCase/snake_case）→ Low；但该名字出现在跨规格引用里时重新归类为跨规格类别（High）。
- 同一条 Low 在一份规格多个动作重复 → 合并为一条，附注受影响动作；单份规格去重后 ≥5 条 Low → 在摘要注明并建议重审该规格。
- 报 Medium 及以上前，用 grep 或读文件确认发现存在于**当前**代码，不凭记忆或旧印象。

## 并行扫描（规格 ≥5 份）

用只读子代理并行对账：

- **显式指定强档模型**，不继承会话档位——对账要给出「不存在」类断言（如 `Missing action: clean`），错误判定不产生可察觉输出，弱模型漏报无法被发现。
- 每个子代理分配 2–3 份相邻规格；提示词附上「严重度校准」整段与对应检查表（严重度取值逐字照抄，不得自行上调）。
- 每个检查类别都必须给判定，省略视为未核实；合并阶段把未核实类别标出。
- 全部返回后，在主上下文做跨规格校验与系统性聚合。
