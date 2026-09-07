# 依据：作者原文与本技能取用的原则

核验只用作者原文。引用时区分**原句**、**忠实转述**与**本技能的操作性综合**；本技能正文不引原句，只写原则。

| 来源 | 本技能取用的原则 |
| --- | --- |
| [Beyond Objects](https://arxiv.org/abs/2606.27258)（Daniel Jackson, 2026-06-25，v1） | 规格五要素 + queries；when / where / then 因果语义；`Requesting` 伪概念；书版事务语义由作者废弃 |
| [WYSIWID 论文](https://arxiv.org/abs/2508.14511)（Eagon Meng & Daniel Jackson, Onward! 2025，arXiv v2） | 规格四节无跨概念段；错误是可匹配输出；规格即实现 prompt |
| [资格判据教程](https://essenceofsoftware.com/tutorials/concept-basics/criteria/) | 资格五条；user-facing 含 API 程序员 |
| [Sync 组合教程](https://essenceofsoftware.com/tutorials/concept-basics/sync/) | 组合层独立于概念；欠同步 / 过同步；placeholder 动作 |
| [依赖与子集教程](https://essenceofsoftware.com/tutorials/concept-basics/dependency/) | intrinsic / extrinsic 依赖；Parnas 规则；子集即产品家族 |
| [概念设计综述](https://essenceofsoftware.com/posts/distillation/) | 概念独立性（各概念定义不引用其他概念）；synergy；mediator |
| [Design moves](https://essenceofsoftware.com/posts/design-moves/) | split/merge、unify/specialize、tighten/loosen 三对动作 |
| [6.1040 概念评分标准](https://61040-fa25.github.io/resources/concept-rubric) | 使用上下文引用仅限 notes 段 |

仓库维护者可在 `docs/references/jackson/` 查阅上述原文镜像（不随技能安装）。

核验日期：2026-09-07。补充 [Making Software Meaningful（2026-06-09，v1）](https://arxiv.org/abs/2606.11051)：意义贯穿用户、实现与日志，工程组织不等同概念语义。
[Verified LLM-Driven Synthesis for Concept Design（Cunha，2026-07-17，v1）](https://arxiv.org/abs/2607.15718) 是后续独立形式化研究，其 reaction/error 语义不同，不与本文 WYSIWID 的普通错误输出混用。

固定 Markdown 标题、query API 封装、规则节点图、目录和审计等级均为本仓约定。作者允许查询公开抽象状态；采用 query API 是本仓实现边界。`notes` 的上下文约定来自 [课程 rubric](https://61040-fa25.github.io/resources/concept-rubric)。
