# 模板：CONCEPT.md 与 SYNCS.md

流程第 3–4 步读本文。实现期 syncs 按组拆包时，由 `concept-implementation` 把 `SYNCS.md` 按 flow 群随包拆分（flow 不拆散，协调图随包局部化）。

```markdown
# concept: <Name> [<TypeParam>]

## purpose
[恰好一个]

## state
- <字段>: <TypeParam> -> <类型>

## actions
（签名 + requires/ensures；错误是独立输出 case；`_` 前缀 queries 只读）

## operational principle
after <动作>(<参数>) : (<结果>) then <动作>(<参数>) : (<结果>)

## notes
[可选：应用角色、类型参数实例化、非功能约束占位]
```

```markdown
# syncs: <应用名>

## coordination graph
[Concept] --(action)--> (SyncName) --> [Concept]

## flow: <名>
触发: Requesting.<动作>
（sync 块，when / where / then 记法同 concept-design；含匹配 (error: …) 的错误 sync）
排除动作: 本 flow 有意不同步的概念动作及理由
```
