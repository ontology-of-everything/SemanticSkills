# 依据：本技能取用的原则

| 来源 | 取用的原则 |
| --- | --- |
| `concept-design`（伴生技能） | 批评循环、资格五条与四词；sync 行为保持；欠 / 过同步；Parnas 规则 |
| [资格判据教程](https://essenceofsoftware.com/tutorials/concept-basics/criteria/) | user-facing 判据（API 程序员也是用户） |
| [Sync 组合教程](https://essenceofsoftware.com/tutorials/concept-basics/sync/) | 组合层独立于概念；欠同步 / 过同步 |
| [概念设计综述](https://essenceofsoftware.com/posts/distillation/) | mediator 与零引用；synergy 及其反噬 |
| [依赖与子集教程](https://essenceofsoftware.com/tutorials/concept-basics/dependency/) | Parnas 规则；子集即产品家族 |
| [Beyond Objects](https://arxiv.org/abs/2606.27258)（Daniel Jackson, 2026） | 因果规则语义；`Requesting` 入口；错误即可匹配输出 |
| [WYSIWID 论文](https://arxiv.org/abs/2508.14511)（Eagon Meng & Daniel Jackson, 2025） | 规范可从代码提取；行为增量 = sync 增删 |
| [jlifyio/wyx](https://github.com/jlifyio/wyx)（`concept-guardrails` 的上游） | 漂移检查表、严重度校准、并行扫描机制（已适配零点名规格格式） |

架构 fitness functions 管持续（CI 工具见 `concept-implementation` 语言参考），审计管周期，两层互补。
