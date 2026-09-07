# 订位例：多类型参数与组合边界

受 *Beyond Objects* §13 启发的**教学改写**，不是论文图的逐字转录。保留“承诺”与“可用性”的区分；下面明确选取最小预约片段，未定义整套餐厅产品。依赖项与缺口不能从论文示意图自动补成已确认需求。

## 两个概念

```text
# concept Reserving [User, Slot]
## purpose
为用户保留未来使用某资源时段的承诺。
## principle
after 用户成功预约某时段，
then 其在约定时间到场且预约未取消时，可兑现该承诺。
## state
预约集合：每项有 user: User、slot: Slot、status: booked/canceled/granted。
一个 slot 最多有一个 booked 预约；Slot 是外部身份，不读取其字段。
## actions
reserve (user: User, slot: Slot) : (reservation: Reservation)
  requires slot 无 booked 预约
  ensures 原子创建 booked 预约，其他预约不变
reserve (user: User, slot: Slot) : (error: Conflict)
  requires slot 已有 booked 预约
  ensures 状态不变
cancel (reservation: Reservation)
  requires 预约为 booked
  ensures 仅将该预约改为 canceled
grant (reservation: Reservation)
  requires 预约为 booked，且已满足本概念约定的到场条件
  ensures 仅将该预约改为 granted
```

到场条件在正式模型中需细化为可判定输入/时间契约；本例不据此生成生产实现。专一：承诺；完整：预约/取消/兑现；独立：只用身份；熟悉：沿用预约含义。

```text
# concept Availability [Venue]
## purpose
让使用者找到指定场所当前提供的资源时段。
## principle
after 场所发布时段并保持其可用，
then 使用者查询该场所时能找到它；撤下后不再返回。
## state
时段集合：venue: Venue、offered: Flag。
## actions
publish (venue: Venue) : (slot: Slot)
  requires true
  ensures 创建 offered=true 的时段，其他时段不变
withdraw (slot: Slot)
  requires 时段存在
  ensures 该时段 offered=false，其他时段不变
_find (venue: Venue) : (slot: Slot)
  returns 该 venue 的全部 offered 时段；无结果为空集合
```

专一：可用时段；完整：发布/撤下/查询；独立：不认识预约；熟悉：沿用资源列表。是否要排除已预约时段由应用组合决定，不能偷偷让 Availability 读取 Reserving。

## 预约请求片段

应用边界已提供不透明 UserId/VenueId；调用者选择具体 slot。所有多 when 在同一 flow 匹配；request 标识响应关联。

```text
app Reservations
  include Availability [VenueId]
  include Reserving [UserId, Availability.Slot]

  // flow: reserve
  sync reserve
    when Requesting.reserve (request: r, user: u, slot: s)
    then Reserving.reserve (user: u, slot: s)

  sync accepted
    when Requesting.reserve (request: r),
         Reserving.reserve () : (reservation: x)
    then Requesting.respond (request: r, reservation: x)

  sync rejected
    when Requesting.reserve (request: r),
         Reserving.reserve () : (error: e)
    then Requesting.respond (request: r, error: e)
```

`_find` 没有 error case，不能写 `_find(...) : (error)` 处理无槽位。它返回全部候选，也不能直接让 then 为每个候选创建预约；应用先让用户选一个，或明确唯一选择规则。

## 图与未决

同步图：Requesting.reserve → reserve → Reserving.reserve；accepted/rejected 各有两个合取输入，输出 Requesting.respond。查询没有画成被触发动作。

产品若只提供已知 slot 的承诺，可单独使用 Reserving；若要求发现时段才可预约，则该产品声明 Reserving → Availability。依赖随需求确定，不能从类型实例化机械推导。

正式交付前还需决定：身份认证、slot 是否属于所选场所、撤下与预约的竞态、已预约时段是否隐藏、到场条件、取消与兑现入口、运行时故障策略。本文没有把这些当成已确认实现，也没有引入论文未声明的 Karma/UserAuthentication 查询。
