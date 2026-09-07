---
name: concept-design
description: Generates and revises Daniel Jackson concept models from requirements with independent purposes, behavior specifications, and causal synchronizations. Use when the user requests 概念设计, 概念建模, or concept-design; generic requirement discussions do not require it.
metadata:
  openclaw:
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/concept-design
---

# 概念设计

把需求、访谈或既有模型转成独立 concepts、syncs、产品依赖与取舍。Concept 既是用户理解功能的心理构造，也对应连贯功能单元；页面、实体和代码模块不直接等同概念。以下是本仓对 Jackson 方法的操作化，不是作者规定的固定流程。

只要求建模时交付模型；用户同时要求 PRD/实现且取舍已明确时继续交接 `concept-prd` / `concept-implementation`，不重复索要确认。未安装伴生技能时交付可用模型与缺口，不假定其存在。

## 设计循环

1. **找需要**：从受益者、具体 misfit、现有做法、期望结果与约束识别目的；区分确认事实、推断和待决项。
2. **刻画候选**：每个候选写一个 purpose、具体 principle、最小 state 与完整 actions。先用具体故事检验价值，再把外部身份抽象为类型参数。
3. **批评边界**：读 [criteria.md](references/criteria.md)，检查资格与专一/完整/独立/熟悉；逐候选给理由和结论：保留、拆分、合并、参数化、降级为 type/action/implementation、移至 sync、待确认。
4. **组合检验**：读 [sync-notation.md](references/sync-notation.md)，实例化 concepts，写成功、拒绝及后台联动；检查绑定、响应、并发与排除动作。分别派生同步图与 extrinsic 依赖图，圈定 MVP。
5. **解决 misfits**：用 split/merge、unify/specialize、tighten/loosen 回到边界或组合；仍需产品判断的取舍进入未决表，不把“所有 misfits 消失”当作无限循环条件。
6. **交付**：按下列结构呈现，核对完成条件。未决项只阻塞依赖它的部分。

## 规格契约

- **purpose**：恰好一个可评价的需要；**principle**（operational principle/OP）：说明如何兑现目的的原型故事，可用 after/then。它是代表性行为，不是完整正确性规格。
- **state/actions** 完整定义允许行为、前置条件、效果及不变量；不混入页面步骤、协议、表布局。每个输出 case 说明条件与状态效果，错误不必固定为 String。
- 类型参数 `[T, ...]` 可零个或多个，是不假定字段的身份。定义不依赖其他概念；同名局部参数不是外部引用。可选 notes 记录应用背景，不能藏跨概念执行规则。
- `_` queries 是只读查询，集中列在 actions 节便于导航，但不产生动作完成事件。查询只返回已声明的绑定/case；无匹配不自动成为错误。
- 跨概念联动写 sync；where 经公开查询读状态，then 仅调用已声明动作。具体语法、flow 关联与行为保持检查见组合参考。

## 输出结构

````markdown
## 需求与 Misfits
用户 / 需要 / 现状 / 结果 / 约束；确认与推断

## Concepts
```text
# concept Name [T, ...]
## purpose
<一个需要>
## principle
after <动作序列与条件>
then <目的兑现的结果>
## state
<本概念需要记住的事实与约束>
## actions
act (arg: T) : (result: R)
  requires <允许条件>
  ensures <效果与未改变的状态>
act (arg: T) : (error: E)
  requires <失败条件>
  ensures <失败效果>
_query (arg: T) : (result: R)
  returns <只读绑定；空集/多结果语义>
```
专一 / 完整 / 独立 / 熟悉：<各自结论及理由>

## Synchronizations
<app / include / sync；按入口或规则职责归组>

## 同步图
<when 动作 → sync 节点 → then 动作；where 另标读取>

## 依赖图与子集
A → B 表示纳入 A 需要 B；<MVP 与其余约束>

## 排除与未决
| 候选/动作/问题 | 结论 | 理由及影响 |
````

## 完成条件

- 候选均有完整四节与边界结论；principle 能演示 purpose，state/actions 支持其行为。
- include 类型实例化、sync 动作/query、参数、输出与变量绑定逐一可解析；旧记法迁移保留原有行为，不能只替换关键字。
- 每个外部入口的可达结果有明确策略；需要响应时覆盖成功与拒绝，后台事件允许无响应。错误处理或有意不处理均可追踪。
- 同步图保留每条规则的多源合取和多目标；与产品依赖图区分。循环有终止或受控持续运行依据。
- 未暴露动作与产品取舍有理由；MVP 对依赖闭包成立，并核查剩余 sync、入口及所需外部资源；闭包本身不保证产品可用。

## 按需参考

- 首次应用四节/组合，或核对多类型参数时读 [订位例](references/example-reserving.md)。它标明示例范围，不能当生产完整模型。
- 核验论文、历史语义或引用出处时读 [sources.md](references/sources.md)。
