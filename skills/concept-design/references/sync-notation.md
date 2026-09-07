# 组合：Sync 记法、语义、信号、依赖图

流程第 5 步「组合再设计」读本文。Sync 是概念之外的独立组合层：按因果规则，某些动作发生后引发另一些动作。概念规范不点名其他 concepts；组合只写在 app 级的 syncs。

## 记法（when / where / then，作者现行版）

示例改写自 Jackson 的 ExpiringUserSession：

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

## 语义规则

- **when** 匹配已完成的动作（completion）及其输出；参数全部具名，允许只匹配子集。
- **where** 经 queries 读取概念状态并绑定变量；绑定不成立则本条 sync 不触发。
- **then** 触发新的动作调用（invocation）；绑定变量跨段传递，sync 同时是数据流。
- **外部请求也是动作**：端点、定时器等外部入口具体化为 `Requesting` 伪概念的动作，由 sync 接力，响应同样由 sync 产生；应用动作 = 由 Requesting 触发的 sync。
- **错误即输出**：动作失败输出 `(error: …)` 这个普通的可匹配 case，由错误 sync 响应或补偿，不需要事务语义。
- **行为保持**：sync 只能调用概念已声明的动作、只能经 queries 读状态，不能使概念做出孤立时不可能的行为；组合因此不破坏一致（Integrity）。
- **旧版语义已废弃**：书（2021）的 CSP 对称约束与"全有或全无"事务语义被作者本人放弃（Beyond Objects：设计者难理解、实现需事务）。存量模型的旧记法按本节改写。
- 未被任何 sync 提及的概念动作不在应用中出现；排除是设计决策（Yellkey 不开放 renew），记入排除与未决表。
- **实现层**由 mediator 或规则引擎落地 sync：组合层引用概念，概念之间零相互引用。

## 模式与信号

- **Placeholder 动作**：为同步而设计的概念提供占位动作，钉到其他概念的真实动作上——访问控制的 access、订阅的 notify。
- **欠同步**：漏掉的自动化（Zoom 举手不随发言结束自动放下）→ tighten。
- **过同步**：自动化抢走用户控制（日历删除事件即向邀请人发拒绝）→ loosen 或做成可配置。
- **分解线索**：表面单概念、目的冲突，常是多概念同步（Facebook Like ≈ Upvote、Reaction 等的 sync）；回流程第 4 步拆分。
- **Flow**：打穿概念的业务流程 = 一个外部请求触发、多条细粒度 sync 接力的动作链；流程本身不是另立概念的理由，升格判据见误判速查表末行。
- **Synergy**：一个概念借另一概念实现自身功能，整体大于部分之和（Trash 做成 Folder，移动动作免费获得还原）；强求则反噬（Outlook 把系统日志装进邮件文件夹）。

## 依赖图与子集

- **Intrinsic dependency**：concept 定义引用另一 concept——必须消除（参数化或移至 sync）。
- **Extrinsic dependency**：在具体应用中，没有 C2 则纳入 C1 没有意义（Comment 依赖 Post）；可以存在，但不写进 C1 的定义。

以 extrinsic 依赖画图（Parnas 的 uses relation）：节点为概念，边 C1 → C2 表示含 C1 的版本必须含 C2。Parnas 规则：**不能没有 B 就用 A，就永远不该想没有 B 用 A**。

产出：

- **产品家族**：每个"不缺依赖"的概念子集是一个可行产品；用它圈定 MVP 与版本演进。
- **顺序**：讲解与开发都先做被依赖者（先 Post 后 Comment）。
