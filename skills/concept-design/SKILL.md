---
name: concept-design
description: Models or reviews requirements as Jackson concepts defined by Purpose, OP, State, and Actions, then composes them with Syncs. Use this skill whenever the user asks to discuss requirements, review a concept model, or mentions 概念设计 / 概念建模 / concept-design (formerly jackson-concept-design); stop at model confirmation without producing PRD or code.
---

# Jackson 概念设计

把需求转成可理解、可评价、可组合的概念模型。停在模型确认；除非用户明确要求，不生成 PRD、架构或代码。本文是按 Jackson 的结构、判据与设计动作整理的操作循环，不冒充作者原文流程。模型确认后：文档化为 PRD 规格用伴生技能 `concept-prd`，代码落地用 `concept-implementation`，存量审计用 `concept-audit`。

## 核心模型

Concept 同时是用户为有效使用软件而掌握的**心理构造**，和与之对应的**连贯功能单元**。应用由独立 concepts 组成，由 synchronizations（syncs）联结成应用行为；界面和术语表达概念，代码实现概念，但都不是概念本身。

```text
Concept = Name + Purpose + Operational Principle + State + Actions
```

- **Name**：简短易记，唤起正确、熟悉的心理模型。
- **Purpose**：为何存在、给谁什么价值；need-focused、specific、evaluable，且恰好一个。
- **Operational Principle（OP）**：少量端到端典型故事，展示如何使用并兑现 purpose。写法：
  - 历史要足够长，结尾兑现 purpose——注册本身无价值，随后认证才展示 Password 的目的；
  - 一次只解释一个 concept，写 actions 与结果，不写界面、协议或表结构；
  - 先用当前场景的具体对象写以检验价值，成立后再改写为多态通用版本；
  - OP 解释本质，不替代规范：行为由 state machine（state + actions）完整规定。
- **State**：运行中为支持行为必须记住的事实，不是领域知识或数据库设计。记法用 Alloy 风格关系式（`password: U -> String`；课程 SSF 散文式等价）。User、Item 等实体通常只是类型参数或身份类型，不是顶层模块。
- **Actions**：用户或系统执行的抽象行为，读取或改变 state；签名写 `动作 (入参: 类型) : (出参: 类型)` 加 requires/ensures，按输出模式拆 case——错误是独立的输出 case（`: (error: String)`），供错误 sync 匹配；不拆成界面步骤。
- **Queries**（`_` 前缀）：只读、不改 state 的查询（`_getUser (session) : (user)`），是常用读取模式的速记，专供 sync 的 where 段；不是 action。

## 设计循环

重复 1–5 直到 misfits 消失。先确认 purpose 与边界，再确认名称和细节；全程区分已确认、推断与待决定。

1. **找需要**：明确受益者、misfit、现有做法、期望结果与约束；把"要什么"追问成"为什么"。暂不讨论页面、数据库和服务。
2. **识别候选**：从具体场景自下而上找细粒度目的，优先熟悉、可复用的概念；不从名词表、实体、页面或团队边界映射。边界不明先保留备选。
3. **逐个刻画**：写 Name、Purpose、具体 OP，由 OP 推导 actions 和最小 state；删除行为不需要的 state，补齐必要 action，成立后参数化上下文对象。
4. **批评边界**：对每个候选过一遍资格判据与四词（见下节），结论只用：`保留`、`拆分`、`合并`、`参数化`、`降级为 type/action/implementation`、`移至 sync`、`待确认`。
5. **组合再设计**（记法与规则见「组合：Sync」）：
   - 选入 concepts 并以类型参数实例化（`include Session [User.User]`）；
   - 写 syncs 表达跨概念行为与应用入口；
   - 核查未被 sync 提及的动作——它们不在应用中出现，须是有意排除；
   - 按欠同步、过同步与 synergy 检视组合质量；
   - 画依赖图、枚举子集，圈定 MVP 与讲解、开发顺序。

   调整用三对 design moves：**split/merge**（控制力 vs 简单）、**unify/specialize**（通用 vs 贴合）、**tighten/loosen**（自动化 vs 灵活）。

## 判据

**资格**——候选是否够格成为 concept：

- **用户可感（User-facing）**：用户能体验其功能；API 中程序员也是用户。
- **语义性（Semantic）**：表达抽象意义，不是控件、样式或技术机制。
- **行为性（Behavioral）**：有动态行为，不只是分类与属性。
- **目的性（Purposive）**：独立带来真实、可评价的价值。
- **端到端（End-to-end）**：从动作延伸到兑现目的的结果。

第六条资格——独立性——与四词中的**独立**是同一判据，见下。

**四词**——批评边界与输出判断统一用这四个词：

- **专一（Specificity）**：只承担一个不可分的目的；多目的即 conflation，拆分。
- **完整（Completeness）**：含兑现目的所需的全部功能；只有片段即 fragmentation，合并或补齐。
- **独立（Independence）**：无需引用其他 concept 即可理解；共享对象用类型参数抽象，如 `Comment<Target>` 而非 `Comment<Post>`。
- **熟悉（Familiarity）**：优先沿用已知概念并保持惯例；新概念须提供熟悉概念或其组合给不了的价值。

**组合后再查**：

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

## 组合：Sync

Sync 是概念之外的独立组合层：按因果规则，某些动作发生后引发另一些动作。Concept 规范不点名其他 concepts；组合只写在组合层（app 级的 syncs）。现行记法是 when / where / then 三段式（Beyond Objects，2026；示例改写自 Jackson 的 ExpiringUserSession）：

```text
app ExpiringUserSession
  include User
  include Session [User.User]
  include ExpiringResource [Session.Session]

  sync login
    when Requesting.login (name, pass)
    where User._authenticate (name, pass) : (user)
    then Session.start (user), ExpiringResource.allocate (session, 300)

  sync loginFailed
    when Requesting.login (name, pass)
    where User._authenticate (name, pass) : (error)
    then Requesting.respond (error)

  sync terminate
    when ExpiringResource.expire (resource)
    then Session.end (resource)
```

**语义规则（因果规则，现行版）：**

- **when** 匹配已完成的动作（completion）及其输出；参数全部具名，允许只匹配子集。
- **where** 经 queries 读取概念状态并绑定变量；绑定不成立则本条 sync 不触发。
- **then** 触发新的动作调用（invocation）；绑定变量跨段传递，sync 同时是数据流。
- **外部请求也是动作**：端点、定时器等外部入口具体化为 `Requesting` 伪概念的动作，由 sync 接力，响应同样由 sync 产生；应用动作 = 由 Requesting 触发的 sync。
- **错误即输出**：动作失败输出 `(error: …)` 这个普通的可匹配 case，由错误 sync 响应或补偿，不需要事务语义。
- **行为保持**：sync 只能调用概念已声明的动作、只能经 queries 读状态，不能使概念做出孤立时不可能的行为；组合因此不破坏一致（Integrity）。
- **旧版语义已废弃**：书（2021）的 CSP 对称约束与"全有或全无"事务语义被作者本人放弃——"designers find this approach hard to understand … hard to implement, since it requires transactions"（Beyond Objects）。存量模型的旧记法按本节改写。
- 未被任何 sync 提及的概念动作不在应用中出现；排除是设计决策（Yellkey 不开放 renew），记入排除与未决表。
- **实现层**由 mediator 或规则引擎落地 sync：组合层引用概念，概念之间零相互引用。

**模式与信号：**

- **Placeholder 动作**：为同步而设计的概念提供占位动作，钉到其他概念的真实动作上——访问控制的 access、订阅的 notify。
- **欠同步**：漏掉的自动化（Zoom 举手不随发言结束自动放下）→ tighten。
- **过同步**：自动化抢走用户控制（日历删除事件即向邀请人发拒绝）→ loosen 或做成可配置。
- **分解线索**：表面单概念、目的冲突，常是多概念同步（Facebook Like ≈ Upvote、Reaction 等的 sync）；回循环第 4 步拆分。
- **Flow**：打穿概念的业务流程 = 一个外部请求触发、多条细粒度 sync 接力的动作链；流程本身不是另立概念的理由，升格判据见速查表末行（自有目的、状态和完整行为）。
- **Synergy**：一个概念借另一概念实现自身功能，整体大于部分之和（Trash 做成 Folder，移动动作免费获得还原）；强求则反噬（Outlook 把系统日志装进邮件文件夹）。

## 依赖图与子集

- **Intrinsic dependency**：concept 定义引用另一 concept——必须消除（参数化或移至 sync）。
- **Extrinsic dependency**：在具体应用中，没有 C2 则纳入 C1 没有意义（Comment 依赖 Post）；可以存在，但不写进 C1 的定义。

以 extrinsic 依赖画图（Parnas 的 uses relation）：节点为概念，边 C1 → C2 表示含 C1 的版本必须含 C2。Parnas 规则：**不能没有 B 就用 A，就永远不该想没有 B 用 A**。

依赖图的产出：

- **产品家族**：每个"不缺依赖"的概念子集是一个可行产品；用它圈定 MVP 与版本演进。
- **顺序**：讲解与开发都先做被依赖者（先 Post 后 Comment）。

## 输出格式

每概念四节 + 可选 notes，除 notes 外零点名其他概念；确认后可经 `concept-prd` 原样落为与代码共存的 `CONCEPT.md`（与 wyx 架构护栏兼容）。

````markdown
## 需求与 Misfits
- 用户 / 需要 / 问题 / 结果 / 约束

## Concepts

```text
concept <Name> [<TypeParam>]

## purpose
[恰好一个：为何存在、给谁什么价值]

## state
- <字段>: <TypeParam> -> <类型>

## actions
<动作> (<入参: 类型>) : (<出参: 类型>)
  requires [前置] ensures [效果]
<动作> (<入参: 类型>) : (error: String)
  [错误 case 单列，供错误 sync 匹配]
_<查询> (<入参>) : (<出参>)
  [只读；供 where 段]

## operational principle
after <动作> (<参数>) : (<结果>)
then <动作> (<参数>) : (<结果>)
[可多条场景，每条以兑现 purpose 收尾]

## notes
[可选。使用上下文备注的唯一落点（应用角色、类型参数实例化）；
不设 interactions / dependencies 段——跨概念信息属于 syncs 与依赖图]
```

- 判断: 专一 / 完整 / 独立 / 熟悉（每概念附结论）

## Synchronizations
```text
app <应用名>
  include <Concept> [<Type>]

  sync <名>
    when <Concept.action (参数)>
    where <Concept._query (参数) : (绑定)>
    then <Concept.action (参数)>    // 每条 sync 注明组合理由/风险
```

## 依赖图与子集
- 依赖: C1 -> C2, ...（extrinsic，只在此处；不写进概念规格）
- 子集: {MVP: ...} / {扩展: ...}

## 排除与未决
| 候选/问题 | 结论 | 理由/取舍 |
````

## 完成条件

- 每个 concept 恰好一个 purpose，OP 以兑现该 purpose 的结局收尾。
- 每个 concept 的四词判断均有结论，结论词出自设计循环第 4 步词表。
- State 与 actions 完整规定行为（queries 只读不改 state），无界面、协议或表结构细节。
- 概念规格只含 purpose / state / actions / operational principle（可选 notes）；除 notes 外零点名其他概念，无 interactions / dependencies 段；跨概念行为全部落在 sync 块，且每条满足行为保持。
- Sync 用 when / where / then 记法；每个可失败动作的 error case 有错误 sync 处理，或有意不处理并记入排除与未决表。
- 未被 sync 提及的动作均为有意排除；欠同步、过同步已按 tighten/loosen 检视。
- 依赖图画出且无违反 Parnas 规则处；MVP 子集从图中圈定。
- 被否决的候选与待决取舍全部进入排除与未决表，无空悬项。

## 依据

核验只用作者原文：

- [Beyond Objects](https://arxiv.org/abs/2606.27258)（2026：现行规格五要素 + queries、when/where/then 因果语义、废弃书版事务语义）
- [WYSIWID 论文](https://arxiv.org/abs/2508.14511)（规格四节无跨概念段、错误作为可匹配输出、规格即实现 prompt）
- [官方教程](https://essenceofsoftware.com/tutorials/)（含
  [资格判据](https://essenceofsoftware.com/tutorials/concept-basics/criteria/)、
  [Sync 组合](https://essenceofsoftware.com/tutorials/concept-basics/sync/)、
  [依赖与子集](https://essenceofsoftware.com/tutorials/concept-basics/dependency/)）
- [概念设计综述](https://essenceofsoftware.com/posts/distillation/)（概念独立性原句 "Each concept is defined without reference to any other concepts"）
- [Design moves](https://essenceofsoftware.com/posts/design-moves/)
- [6.1040 概念评分标准](https://61040-fa25.github.io/resources/concept-rubric)（使用上下文引用仅限 notes 段）

引用时区分原句、忠实转述与本技能的操作性综合。
