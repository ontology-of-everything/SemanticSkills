# Sync 语义与组合检查

概念之间保持独立，应用级 sync 把动作完成关联为后续调用。以下采用因果规则；具体符号和查询接口是本仓规格约定，不能与论文或引擎语法逐字等同。

## 一个有绑定来源的例子

示意契约：Session.start 返回 session；ExpiringResource.allocate 接收 resource；Requesting 的请求有 request 身份。错误 case 必须由对应动作实际声明。

```text
app ExpiringSession
  include Session [U]
  include ExpiringResource [Session.Session]

  sync start
    when Requesting.login (request: r, user: u)
    then Session.start (user: u)

  sync expireLater
    when Session.start (user: u) : (session: s)
    then ExpiringResource.allocate (resource: s, ttl: 300)

  sync success
    when Requesting.login (request: r),
         Session.start () : (session: s)
    then Requesting.respond (request: r, session: s)

  sync failure
    when Requesting.login (request: r),
         Session.start () : (error: e)
    then Requesting.respond (request: r, error: e)
```

多 when 必须属于同一 flow/因果实例，不能任意拼接并发请求的历史。上例省略身份验证、allocate 失败与到期动作，仅说明数据依赖拆规则，不能直接作为完整登录方案。

## 匹配、绑定与执行

- **when** 匹配已完成动作及其输出，允许匹配部分具名参数；多个模式共同匹配。保留完成事件身份与 flow 关联，避免重复或跨请求组合。
- **where** 求只读查询及关系/过滤条件，产生零、一或多组绑定。读取本仓概念状态只走声明 query。零行表示不触发；如果需要拒绝响应，必须另有可匹配分支，不能凭空给 query 添加 `(error)`。
- **then** 对每组绑定发出动作调用。各调用使用 when/where 已绑定值或常量；同一 then 中前一调用的未来输出不能供后一调用使用，应在新 sync 的 when 匹配其完成。
- **错误** 是已声明的输出 case，可由 sync 响应、重试或补偿；预期拒绝与运行时故障分开建模。失败不意味自动回滚已完成动作。
- **行为保持**：只使用概念自身允许的动作/状态转移。接口访问是必要条件，还须满足前置条件、原子性及并发约束；query 检查不能替代写动作原子维护不变量。
- 引擎应按选定语义抑制同一完成事件组合的重复触发，并保留溯源。它不自动保证外部副作用 exactly-once；重放/投递重试另需幂等与持久记录。

书版的对称/事务同步与当前因果规则不同；升级既有模型需核对其原子性与可观察行为，不能机械改写。mediator 或规则引擎只要保持这些语义都可落地。

## Flow、图与覆盖

运行时 **flow** 是一个外部事件引发的因果执行实例。HTTP 请求可建模为 `Requesting`，定时/消息也可有明确的入口动作；不要求所有后台事件伪装成请求。

本仓用 `// flow:` 按入口/规则职责组织文档；一段分组覆盖多个运行时实例，共享规则可服务多个入口，不复制规则身份。需要同步响应的请求应覆盖成功、拒绝与故障策略并检查恰当关联；后台链允许无响应。未使用动作列入应用级排除表。

**同步图** 每条 sync 一个规则节点：多个 when 连入、多 then 连出，where 以查询依赖另标。普通 A→B 图是有损简图，必须保留规则名与合取说明；它不表达“没有 B 就不能纳入 A”。循环合法，但需终止条件或有意持续运行的控制策略；深度上限只是工程保护，截断必须可观察。

## 设计信号

- 欠同步：具体用户场景中遗漏应自动的联动 → tighten。
- 过同步：自动化夺走需要的控制 → loosen/配置。
- Placeholder action：用可同步的占位动作表达 access/notify 等功能；仍需明确契约。
- Synergy：概念复用另一概念的能力带来额外价值；若扭曲被复用者的 purpose，重新拆分。
- 多概念参与或长 flow 只是检查线索；有多个目的或自有业务状态才是重审边界的证据。溯源日志、队列不是新业务概念的充分理由。

## 依赖与产品子集

Intrinsic dependency 指概念定义依赖另一概念，应通过参数化/组合消除。Extrinsic dependency 是应用选择：纳入 A 只有在纳入 B 时才有意义；在总体 PRD 写 `A → B`。

Parnas 原则用于使实现限制与有意义的产品子集相符，不能以代码耦合倒推产品必须依赖。依赖闭包是候选子集的必要检查，还须核对该子集的入口、sync、目的与外部资源。分组不自动成为独立可交付产品；有环时按依赖组处理，不强行拓扑排序。
