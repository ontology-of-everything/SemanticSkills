# 订位转录例：权威文件与追溯

受 *Beyond Objects* 的 Reserving/Availability 分离启发。这里仅展示**已有模型的一个确认片段**如何落盘，不是论文原文或完整预约产品；不会补写身份认证、Karma 或查询错误 case。

## 已确认输入

- Reserving [User, Slot] 维护预约承诺；Availability [Venue] 提供时段。
- Reserving.reserve 成功返回 reservation；冲突返回 Conflict 且不改状态。
- Availability._find 返回该 venue 全部 offered 时段，空集合表示无候选。
- 用户选择单一 slot 后发送 Requesting.reserve；响应按同一 flow/request 关联。

## 转录落点

| 模型内容 | 模块已存在 | 尚无模块 |
| --- | --- | --- |
| Reserving 的完整四节 | `reserving/CONCEPT.md` | `docs/prd/concepts/Reserving.md` |
| Availability 的完整四节 | `availability/CONCEPT.md` | `docs/prd/concepts/Availability.md` |
| 应用实例化与规则 | `syncs/SYNCS.md` | `docs/prd/SYNCS.md` |
| 用户需要、依赖、图及未决项 | `docs/prd/README.md` | 同左 |

四节从确认模型逐项转录；本例未提供的字段不得推断。CONCEPT.md 内仍使用局部类型参数，实际实例化只进入 SYNCS.md。

## syncs/SYNCS.md 片段

```text
# app Reservations
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

## 验收与缺口

将“成功预约后可兑现承诺”的 principle 编为代表性验收场景，链接 reserve/grant 契约；冲突且状态不变的边界场景追溯到 reserve 的错误 case。两者均源于模型，不发明新要求。

`_find` 的空集合不能转录成 `(error)`，多候选也不能变成预约全部。若上游尚未说明身份、并发、到场条件或取消入口，把这些保留为未决；只有用户确认后才更新对应规格及派生图。

交付检查：每个确认元素有唯一权威位置，索引链接有效；声明片段未冒充完整模型。同步图以规则节点保留 accepted/rejected 的两个合取输入，不把 where 查询当动作完成。
