# 依据：本技能取用的原则

记法与判据沿用 `concept-design`（见其 `references/sources.md`），本技能只补"概念规范即规格"的出处。

| 来源 | 取用的原则 |
| --- | --- |
| [WYSIWID 论文](https://arxiv.org/abs/2508.14511) | 概念规范可直接生成代码与测试；行为增量 = sync 的增删 |
| [Beyond Objects](https://arxiv.org/abs/2606.27258) | 规格要素与因果组合；notes 约定另见课程 rubric |
| [conceptbox](https://github.com/61040-fa25/conceptbox)（官方课程模板） | 规格与代码同仓；规格驱动开发 |

核验日期：2026-09-07。补充 [Making Software Meaningful（2026-06-09，v1）](https://arxiv.org/abs/2606.11051)：意义贯穿用户、实现与日志，工程组织不等同概念语义。
[Verified LLM-Driven Synthesis for Concept Design（Cunha，2026-07-17，v1）](https://arxiv.org/abs/2607.15718) 是后续独立形式化研究，其 reaction/error 语义不同，不与本文 WYSIWID 的普通错误输出混用。

固定 Markdown 标题、query API 封装、规则节点图、目录和审计等级均为本仓约定。作者允许查询公开抽象状态；采用 query API 是本仓实现边界。`notes` 的上下文约定来自 [课程 rubric](https://61040-fa25.github.io/resources/concept-rubric)。
