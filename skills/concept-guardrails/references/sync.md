# Sync 协调映射（wyx:sync）

生成 **`SYNCS.md`**——相互独立的概念如何通过同步规则交互。Jackson 方言采用基于 Daniel Jackson *Beyond Objects*（2026）的本仓记法：因果规则 `when` / `where` / `then`，入口是 `Requesting` 伪概念。回填与审计仍需核对实现。

概念规格不点名其他概念。组合只写在 `SYNCS.md`。

## 如何解读用户参数

从参数判断模式：

- **sync 目录路径**（如 `src/lib/server/syncs/`）：**回填模式** —— 读现有的 sync 处理器，映射成 when / where / then，提出一份 `SYNCS.md`。把任何绕过概念边界的做法标出来。
- **sync 描述**（如 `订单履约 → 库存更新`）：**新建模式** —— 为所描述的协调写 sync 规格。复杂分解回 `concept-design`。
- **没有参数**：**发现模式** —— 分析项目里类似 sync 的模式（事件处理器、跨概念调用、定时任务），列出候选。**不要**生成完整规格；询问用户想细化哪些。如果发现的其实是没有跨概念协调的数据转换链，提示 `wyx:pipeline`。

## SYNCS.md 格式

已有 wyx 原生格式保留 dispatching、coordination graph、sync 条目及 trigger/timing/qualification/flow/error/file；本节为 Jackson 模板。迁移时逐条保留触发、绑定、效果与错误路径，不能仅换标题。

规格写成 `SYNCS.md` 文件，放在 **sync 目录里**（如 `src/lib/server/syncs/SYNCS.md`）。

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

`when` 匹配已完成动作及其输出（允许只匹配参数子集）。`where` 经 `_` queries 读概念状态并绑定变量；绑定不成立则本条不触发。`then` 对 where（可选）产生的每个绑定调用已声明动作。只有已声明的错误 case 才能匹配；查询返回空集合不产生 error，也不自动响应。为预期拒绝声明独立查询/动作分支。then 内调用不能互相使用尚未完成的输出。

`// flow:` 是规则组织注释；运行时 flow 是同一外部事件引发的因果实例，需隔离不同请求，不是规格节。规模化后每个 syncs 包一份 `SYNCS.md`，同一 flow 不拆散；`wyx:map` 从 when → then 合成全局视图。

Jackson 模板不写 `## dispatching`、`## coordination graph`、`trigger` / `timing` / `qualification` / `file`。时机分类（动作后 / 前置校验 / 定时）属于 `concept-implementation`，不进规格。

## sync 模式的设计规则

1. **sync 存在于概念之间**：一个 sync 不属于单个概念。sync 代码放在专门的目录里，不要放进概念目录内部。

2. **行为保持**：then 只调用概念已声明的动作；where 只经 queries 读状态。sync 不能使概念做出孤立时不可能的行为。

3. **错误与响应**：为实际可达失败声明响应、重试、补偿或有意忽略策略。需要响应的请求覆盖成功与拒绝分支，并通过 request/flow 关联，避免串请求；后台事件不强求 HTTP 响应。

4. **级联**：then 触发的动作可再匹配其他 sync。级联合法；循环须有终止或受控持续运行策略，深度上限只是可选保护。成环且无终止条件归 `concept-audit`。

5. **欠同步 / 过同步**：该自动的联动缺失 → 补 sync；自动化抢走用户控制且不可配置 → loosen。细节见 `concept-design` 的 sync 记法。

## 回填模式指引

分析现有 sync 代码时：

1. 读该目录下所有 sync 处理器文件。
2. 读索引 / 注册文件，理解注册与派发。
3. 把每个处理器映射成：when（触发的完成动作）→ where（查询与跳过条件）→ then（调用的动作）。
4. 编排函数（顺序调用多个概念动作、自己不拥有状态）写成一条或多条 sync，不要写进某个 `CONCEPT.md`。
5. 检查 sync 内部的概念边界破坏（为访问其他概念拥有的数据而直接引入数据库——应改用 `_` query 或动作）。

发现按这个格式呈现：

```text
## patterns detected
- [N] 条 sync（when / where / then）
- [N] 条错误 sync（匹配 (error)）

## boundary concerns
- [文件:行] sync 直接查询了归 [概念] 所有的 [表] —— 应该用 [概念._query] 或 [概念.动作]
```

## 新建模式指引

从 sync 描述设计时：

1. 识别源概念与目标概念（各自应已有 `CONCEPT.md`，或至少是候选）。
2. 把协调写成 when（已完成的动作）/ where（queries）/ then（要触发的动作）。
3. 为可失败动作写错误 sync，或记入排除。
4. 考虑级联：这条 sync 的 then 会不会再触发另一条。

## 与其他 wyx 模式的关系

- **`wyx:concept`**：每个被 sync 点名的概念都应有 `CONCEPT.md`。`SYNCS.md` 只引用其中声明的动作与 `_` queries。
  **放置**：每个 sync 目录只保留一份 `SYNCS.md`。hook 的向上查找行为见 `concept.md`。
- **`wyx:pipeline`**：sync 里的数据转换阶段可以另写 `PIPELINE.md`。`SYNCS.md` 管协调，`PIPELINE.md` 管数据质量。
