# 判据：资格五条、四词、误判速查、design moves

流程第 4 步「批评边界」读本文。结论只用：`保留`、`拆分`、`合并`、`参数化`、`降级为 type/action/implementation`、`移至 sync`、`待确认`。

## 资格五条——候选是否够格成为 concept

- **用户可感（User-facing）**：用户能体验其功能；API 中程序员也是用户。
- **语义性（Semantic）**：表达抽象意义，不是控件、样式或技术机制。
- **行为性（Behavioral）**：有动态行为，不只是分类与属性。
- **目的性（Purposive）**：独立带来真实、可评价的价值。
- **端到端（End-to-end）**：从动作延伸到兑现目的的结果。

第六条资格——独立性——与四词中的**独立**是同一判据。

## 四词——批评边界与输出判断统一用词

- **专一（Specificity）**：只承担一个不可分的目的；多目的即 conflation → 拆分。
- **完整（Completeness）**：含兑现目的所需的全部功能；只有片段即 fragmentation → 合并或补齐。
- **独立（Independence）**：无需引用其他 concept 即可理解；共享对象用类型参数抽象，如 `Comment [Target]` 而非 `Comment [Post]`。
- **熟悉（Familiarity）**：优先沿用已知概念并保持惯例；新概念须提供熟悉概念或其组合给不了的价值。

## 组合后再查

- **复用（Reusability）**：通常是四词达标的结果，不是充分条件。
- **一致（Integrity）**：同一 concept 各处保持名称、目的与行为，组合不改变其含义。

## 常见误判速查

名称只是线索：Trash、Password、Reservation 因 purpose 与 behavior 成为 concepts。

| 候选 | 通常归属 | 另立 concept 的条件 |
| --- | --- | --- |
| User、Order 等实体 | state 中的类型/身份 | 自身有独立目的和完整动态行为 |
| 表、类、微服务、页面、控件 | 实现或表达层 | 实现结构恰好承载一个完整 concept 时才可能对应；界面元素不成为 concept |
| register、save 等 | 单个 action | 自身兑现独立目的时重新判断 |
| 故事、用例、feature、workflow | 场景/流程切片 | 独立、端到端服务恰好一个目的且有自己的状态机 |
| 跨概念触发规则 | sync | 自有目的、状态和完整行为 |

## Design moves——调整边界的三对动作

- **split / merge**：控制力 vs 简单。
- **unify / specialize**：通用 vs 贴合。
- **tighten / loosen**：自动化 vs 灵活（对应欠同步 / 过同步）。
