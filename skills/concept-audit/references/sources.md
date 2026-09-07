# 依据：本技能取用的原则

| 来源 | 取用的原则 |
| --- | --- |
| `concept-design`（伴生技能） | 批评循环、资格五条与四词；sync 行为保持；欠 / 过同步；Parnas 规则 |
| [资格判据教程](https://essenceofsoftware.com/tutorials/concept-basics/criteria/) | user-facing 判据（API 程序员也是用户） |
| [Sync 组合教程](https://essenceofsoftware.com/tutorials/concept-basics/sync/) | 组合层独立于概念；欠同步 / 过同步 |
| [概念设计综述](https://essenceofsoftware.com/posts/distillation/) | mediator 与零引用；synergy 及其反噬 |
| [依赖与子集教程](https://essenceofsoftware.com/tutorials/concept-basics/dependency/) | Parnas 规则；子集即产品家族 |
| [Beyond Objects](https://arxiv.org/abs/2606.27258)（Daniel Jackson, 2026-06-25，v1） | 因果规则语义；`Requesting` 入口；错误即可匹配输出 |
| [WYSIWID 论文](https://arxiv.org/abs/2508.14511)（Eagon Meng & Daniel Jackson, 2025-08-27，v2） | 规格与实现可对应；部分行为扩展可通过 sync 增删/替换实现；也可能需要改变概念 |
| [jlifyio/wyx](https://github.com/jlifyio/wyx)（`concept-guardrails` 的上游） | 漂移检查表、严重度校准、并行扫描机制（已适配零点名规格格式） |

架构 fitness functions 管持续（CI 工具见 `concept-implementation` 语言参考），审计管周期，两层互补。

核验日期：2026-09-07。补充 [Making Software Meaningful（2026-06-09，v1）](https://arxiv.org/abs/2606.11051)：意义贯穿用户、实现与日志，工程组织不等同概念语义。
[Verified LLM-Driven Synthesis for Concept Design（Cunha，2026-07-17，v1）](https://arxiv.org/abs/2607.15718) 是后续独立形式化研究，其 reaction/error 语义不同，不与本文 WYSIWID 的普通错误输出混用。

固定 Markdown 标题、query API 封装、规则节点图、目录和审计等级均为本仓约定。作者允许查询公开抽象状态；采用 query API 是本仓实现边界。`notes` 的上下文约定来自 [课程 rubric](https://61040-fa25.github.io/resources/concept-rubric)。
