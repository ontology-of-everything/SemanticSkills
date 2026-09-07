# 模板：CONCEPT.md 与 SYNCS.md

流程第 3–4 步读本文。规格采用基于 Daniel Jackson *Beyond Objects*（2026）的本仓记法；本技能只把模型转录进文件。
填好的对照见 `references/example-reserving.md`。实现期 syncs 按组拆包时，由 `concept-implementation` 把 `SYNCS.md` 按 flow 群随包拆分（flow 不拆散）。

## CONCEPT.md

规格写成 `CONCEPT.md`，放在实现代码旁边（如 `src/lib/server/auth/CONCEPT.md`）。
模块目录未就绪则暂存 `docs/prd/concepts/<名>.md`。严格使用这个结构：

```markdown
# concept Name [T, ...]

## purpose
[恰好一个：这个概念解决什么需要]

## principle
after [用户做了什么]
then [purpose 被兑现的结局]
[原型故事，可多条。每条故事导出代表性场景，完整验收还核对 actions/state。不写其他概念名。]

## state
a set of [实体] with
  a [字段] [类型]
  a [字段] [类型]

## actions
name (arg: Type, ...) : (result: Type)
  requires [前置；不成立则动作不得发生]
  ensures [效果]

name (arg: Type, ...) : (error: String)
  requires [前置]
  ensures [该错误输出]

_query (arg: Type) : (result: Type)
  returns [只读绑定集合；供 sync 的 where 段]
```

可选 `## notes`：应用角色、类型参数实例化、非功能约束占位。
四节（purpose / principle / state / actions）不依赖其他概念定义；同名局部参数合法，不写 `## interactions` / `## dependencies` / `## known coupling`。

类型参数是列表：可零个（省略 `[]`）、一个（`Availability [Venue]`）或多个（`Reserving [User, Slot]`）。
每个参数是无约束的身份，概念不得假定其字段。
应用侧实例化写在 `include`（`include Reserving [User.User, Availability.Slot]`）。

状态也可用等价的 Alloy 关系式（`password: U -> String`）。错误是声明的输出 case；实现可映射 Result/异常但须保留契约。queries 以 `_` 开头，不是动作，不改 state。

## SYNCS.md

规格写成 `SYNCS.md`，放在 sync 目录（转录期单文件）。
模块目录未就绪则暂存 `docs/prd/SYNCS.md`。严格使用这个结构：

```markdown
# app AppName

include Concept [T, ...]

// flow: Name
sync invoke
when Requesting.action (request: r, value: v)
then Concept.action (value: v)

sync succeeded
when Requesting.action (request: r),
     Concept.action () : (result: x)
then Requesting.respond (request: r, result: x)

sync failed
when Requesting.action (request: r),
     Concept.action () : (error: e)
then Requesting.respond (request: r, error: e)
```

`when` 匹配已完成动作；`where` 经 queries 绑定变量（失败则本条不触发）；`then` 对每个绑定调用已声明动作。`// flow:` 注释只为分组（按入口/规则职责组织，运行时各 flow 实例独立关联），不是规格节。排除动作与理由记在总体 PRD，不写进概念规格。同步图、依赖图只在总体 PRD（及设计产出），不重复进 `SYNCS.md`。

上例须对应模型已声明的 result/error 输出；where 可按需添加已声明 query，空集合不自动变成 error。多 when 保留同一 flow 关联；then 的变量须由 when/where 绑定。同一 then 的未来输出须拆到下一条 sync。响应所需 request 身份不可省略。示意占位不能当作已确认模型。
