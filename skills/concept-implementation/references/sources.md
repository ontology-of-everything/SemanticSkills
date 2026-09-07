# 依据：本技能取用的原则

| 来源 | 取用的原则 |
| --- | --- |
| [Beyond Objects](https://arxiv.org/abs/2606.27258)（Daniel Jackson, 2026-06-25，v1） | 因果规则语义；`Requesting` 伪概念；queries；书版事务语义已废弃 |
| [WYSIWID 论文](https://arxiv.org/abs/2508.14511)（Eagon Meng & Daniel Jackson, 2025-08-27，v2） | 概念规范格式；sync 语言与引擎；mediator 与规则引擎两条落地路线 |
| [概念设计综述](https://essenceofsoftware.com/posts/distillation/) | mediator 组合；概念之间零引用 |
| [conceptbox](https://github.com/61040-fa25/conceptbox)（官方课程模板） | 规格与代码同仓；规格驱动开发 |
| [Spring Modulith](https://spring.io/projects/spring-modulith) | 模块单体的官方 Java 工具（见 `java-spring.md`） |
| [LegibleSync](https://github.com/mastepanoski/legiblesync)（社区） | TypeScript 规则引擎实现（见 `typescript.md`） |

各语言六边形架构与边界看护惯例见语言参考文件。

核验日期：2026-09-07。补充 [Making Software Meaningful（2026-06-09，v1）](https://arxiv.org/abs/2606.11051)：意义贯穿用户、实现与日志，工程组织不等同概念语义。
[Verified LLM-Driven Synthesis for Concept Design（Cunha，2026-07-17，v1）](https://arxiv.org/abs/2607.15718) 是后续独立形式化研究，其 reaction/error 语义不同，不与本文 WYSIWID 的普通错误输出混用。

固定 Markdown 标题、query API 封装、规则节点图、目录和审计等级均为本仓约定。作者允许查询公开抽象状态；采用 query API 是本仓实现边界。`notes` 的上下文约定来自 [课程 rubric](https://61040-fa25.github.io/resources/concept-rubric)。
