---
name: concept-design
description: Models or reviews requirements as concepts (Daniel Jackson's concept design) defined by Purpose, OP, State, and Actions, then composes them with Syncs. Use this skill whenever the user asks to discuss requirements, review a concept model, or mentions 概念设计 / 概念建模; stop at model confirmation without producing PRD or code.
---

# 概念设计

## 目标

输入：需求、访谈记录或既有概念模型。输出：由独立 concepts 与 synchronizations 组成的概念模型（模板见「记法与模板」），停在模型确认——除非用户明确要求，不出 PRD、架构或代码。确认后交接：文档化 → `concept-prd`；代码落地 → `concept-implementation`；存量审计 → `concept-audit`。

Concept 同时是用户为有效使用软件而掌握的**心理构造**，和与之对应的**连贯功能单元**；界面和术语表达概念，代码实现概念，都不是概念本身。本文是按 Daniel Jackson 的结构、判据与设计动作整理的操作循环，不冒充作者原文流程。

## 原则

1. 先确认 purpose 与边界，再确认名称和细节；全程区分已确认、推断与待决定。
2. 从具体场景自下而上找目的；表、页面、实体名、团队边界都不直接映射成 concept。
3. 概念规格零点名其他概念（`notes` 段除外）；共享对象用类型参数抽象（`Comment [Target]`）；跨概念行为只写在 sync。
4. State 与 actions 完整规定行为，OP 只解释本质；三者都不写界面、协议或表结构。
5. **Sync 是唯一的组合机制**：when 匹配已完成动作、where 只经 queries 读状态、then 只触发已声明动作（行为保持）；应用动作 = `Requesting` 入口触发的 sync；错误是可匹配输出，由错误 sync 处理。书（2021）的事务语义已被作者废弃，存量旧记法按现行改写。
6. **组合有结构**：sync 按 flow 分组（一个 `Requesting` 入口 = 一个 flow），组合层交付同步图（coordination graph）与依赖图两张图——前者说"谁触发谁"，后者说"没有谁就不能有谁"，不互相替代。
7. 被否决的候选与待决取舍全部进「排除与未决」表，不留空悬。

## 流程

重复 1–5 直到 misfits 消失，再进入 6。

1. **找需要**：受益者、misfit、现有做法、期望结果与约束；把"要什么"追问成"为什么"。完成：「需求与 Misfits」节可填。
2. **识别候选**：从具体场景找细粒度目的，优先熟悉、可复用的概念；边界不明先保留备选。完成：每个候选有一句 purpose。
3. **逐个刻画**：写 Name、Purpose、具体 OP，由 OP 推导 actions 与最小 state；删除行为不需要的 state，补齐必要 action；成立后把上下文对象参数化。完成：每个候选四节齐。
4. **批评边界**：读 `references/criteria.md`，按资格五条与四词逐个判断；结论只用 `保留 / 拆分 / 合并 / 参数化 / 降级为 type、action、implementation / 移至 sync / 待确认`。完成：每个候选有结论词。
5. **组合再设计**：读 `references/sync-notation.md`。
   - include 并实例化 concepts；
   - 按 flow 写 syncs：每个 `Requesting` 入口一个 flow，含成功路径与错误路径的响应 sync；
   - 画同步图：每条 sync 一条边 `[Concept.action] --(sync)--> [Concept.action]`；
   - 核查未被 sync 提及的动作是否有意排除；按欠同步、过同步、synergy、分解线索检视并用 tighten / loosen 调整；
   - 画依赖图（extrinsic）、枚举子集圈定 MVP。

   完成：「命题」全部成立。
6. **呈现并确认**：按模板输出，请用户确认模型；不主动进入 PRD 或代码。

## 命题

产出必须满足，每条可对照文本判真假：

- 每个 concept 恰好一个 purpose；OP 至少一条场景，且以兑现该 purpose 的结局收尾。
- 每个 concept 附四词结论（专一 / 完整 / 独立 / 熟悉），结论词出自流程第 4 步词表。
- 规格只含 purpose / state / actions / operational principle（可选 notes）；除 notes 外不出现其他概念名，无 interactions / dependencies 段。
- 每个 action 带 requires / ensures；错误是独立输出 case `(error: String)`；queries 以 `_` 开头且只读。
- 每条 sync 满足行为保持：只调用概念已声明的动作、只经 queries 读状态；每条附组合理由或风险。
- 每条 sync 恰好属于一个 flow；每个 `Requesting` 入口有成功与错误两条响应路径（或错误路径记入排除表）。
- 同步图的边与 sync 块一一对应；每个可失败动作有错误 sync，或有意不处理并记入排除表。
- 未被 sync 提及的动作均为有意排除并记入排除表。
- 依赖图只含 extrinsic 依赖、无违反 Parnas 规则处；MVP 子集从图中圈定。

## 记法与模板

- **Purpose**：need-focused、specific、evaluable，恰好一个。
- **OP**：少量端到端故事，只写 actions 与结果；先用具体对象写以检验价值，再改写为多态通用版。
- **State**：为支持行为必须记住的事实，Alloy 风格关系式（`password: U -> String`）；User、Item 等实体通常是类型参数，不是顶层模块。
- **Actions**：`动作 (入参: 类型) : (出参: 类型)` + requires / ensures，按输出模式拆 case；不拆成界面步骤。
- **Queries**：`_getUser (session) : (user)`，只读不改 state，专供 sync 的 where 段。
- **四词**：专一（多目的即 conflation → 拆分）、完整（只有片段即 fragmentation → 合并或补齐）、独立（无需引用其他 concept 即可理解）、熟悉（沿用已知概念；新概念须给出既有组合给不了的价值）。

输出模板：

````markdown
## 需求与 Misfits
- 用户 / 需要 / 问题 / 结果 / 约束

## Concepts

```text
concept <Name> [<TypeParam>]

## purpose
[恰好一个]

## state
- <字段>: <TypeParam> -> <类型>

## actions
<动作> (<入参: 类型>) : (<出参: 类型>)
  requires [前置] ensures [效果]
<动作> (<入参: 类型>) : (error: String)
_<查询> (<入参>) : (<出参>)

## operational principle
after <动作> (<参数>) : (<结果>)
then <动作> (<参数>) : (<结果>)

## notes
[可选：应用角色、类型参数实例化；不设 interactions / dependencies 段]
```

- 判断: 专一 / 完整 / 独立 / 熟悉（每概念附结论）

## Synchronizations
```text
app <应用名>
  include <Concept> [<Type>]

  // flow: <名>（入口 Requesting.<动作>）
  sync <名>
    when <Concept.action (参数)>
    where <Concept._query (参数) : (绑定)>
    then <Concept.action (参数)>    // 组合理由 / 风险
  sync <名>Failed
    when ...  where ... : (error)  then Requesting.respond (error)
```

## 同步图
[Concept.action] --(sync)--> [Concept.action]

## 依赖图与子集
- 依赖: C1 -> C2, ...（extrinsic，只在此处）
- 子集: {MVP: ...} / {扩展: ...}

## 排除与未决
| 候选/问题 | 结论 | 理由/取舍 |
````

## 参考

| 何时读 | 文件 |
| --- | --- |
| 流程第 4 步：资格五条、四词展开、组合后再查、误判速查表、design moves | `references/criteria.md` |
| 流程第 5 步：sync 记法示例、因果语义规则、flow 与同步图结构、模式与信号、依赖图与子集 | `references/sync-notation.md` |
| 需要核验判据出处或引用作者原文 | `references/sources.md` |
