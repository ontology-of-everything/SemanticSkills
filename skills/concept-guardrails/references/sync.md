# Sync 协调映射（wyx:sync）

生成 **sync 协调图**——一份结构化描述：相互独立的概念如何通过同步处理器交互。一份 sync 图用一页纸呈现协调拓扑、时机模式与错误策略，替代翻阅几十个处理器文件。

sync 实现的是概念交互的**执行机制**。`CONCEPT.md` 的 `## interactions` 声明关系，`SYNCS.md` 则规定执行机制：sync 何时触发、什么数据流动、何时跳过、错误如何传播。

## 如何解读用户参数

从参数判断模式：

- **sync 目录路径**（如 `src/lib/server/syncs/`）：**回填模式** —— 读现有的 sync 处理器，映射出协调模式，提出一份 `SYNCS.md`。把任何绕过概念边界的做法标出来。
- **sync 描述**（如 `订单履约 → 库存更新`）：**新建模式** —— 为所描述的协调设计一份 sync 规格。定义触发、流程、执行条件与错误策略。
- **没有参数**：**发现模式** —— 分析项目里类似 sync 的模式（事件处理器、跨概念调用、定时任务、dispatch 注册），列出候选。**不要**生成完整规格；询问用户想细化哪些。如果发现的其实是没有跨概念协调的数据转换链，提示 `wyx:pipeline` 覆盖那类模式。

## SYNCS.md 格式

规格写成 `SYNCS.md` 文件，放在 **sync 目录里**（如 `src/lib/server/syncs/SYNCS.md`）。

```markdown
# syncs: [模块/领域名称]

## coordination graph
[文本示意图，展示概念经由 sync 到概念的流向]

[概念] --(动作)--> (SyncName) --> [概念]
[概念] --(动作)--> (SyncName) --> [概念]
                              --> [概念]

## dispatching
- pattern: [event-driven | explicit-call | hybrid]
- error-isolation: [sync 失败不传播到源 | 传播]
- depth-limit: [级联深度上限，如适用]
- context: [跨 sync 边界的关联/追踪如何工作]

## sync: [SyncName]
trigger: [Concept.action | schedule(interval) | manual]
timing: [post-action | pre-validation | scheduled]
flow:
  1. [Concept.action] → [读了什么数据]
  2. [transform/filter/validate] → [发生了什么]
  3. [Concept.action] → [写了什么数据]
qualification: [执行 vs 跳过的条件]
error: [isolated | propagates | skip-and-log]
file: [实现文件的相对路径]
```

## sync 模式的设计规则

1. **sync 存在于概念之间**：一个 sync 永远不属于单个概念，它协调两个或更多概念。sync 代码放在专门的目录里，不要放进概念目录内部。

2. **一个 sync 一个方向**：每个 sync 有清晰的源和目标。如果两个概念需要双向协调，用两个独立的 sync。这样协调图才能保持无环，也不会出现级联回路。

3. **三种时机模式**：
   - **动作后（post-action）**：在源概念的动作完成**之后**运行。无论 sync 结果如何，源都算成功。错误隔离。
   - **前置校验（pre-validation）**：在目标概念的动作**之前**运行。校验跨概念引用。失败时阻断目标动作。错误传播。
   - **定时（scheduled）**：按定时器运行。检查有什么需要更新，批量处理。与单个概念动作无关。

4. **显式执行条件优于静默过滤**：sync 处理器应该声明明确的执行条件（何时执行、何时跳过）。这让协调图是诚实的——你能准确看出 sync 什么时候会触发、什么时候被跳过。

5. **按时机决定错误隔离**：动作后 sync **不应该**让源动作失败——源概念已经完成了它的工作。前置校验 sync **应该**让目标动作失败——这正是它的目的。定时 sync 应该记录错误并继续处理剩余条目。

## 回填模式指引

分析现有 sync 代码时：

1. 读该目录下所有 sync 处理器文件。
2. 读索引 / 注册文件，理解注册与派发模式。
3. 读任何 dispatcher 或 context 模块，理解执行基础设施。
4. 把每个 sync 映射成：触发 → 流程 → 目标。
5. 归类时机模式（动作后、前置校验、定时）。
6. 检查 sync 内部的概念边界破坏（为访问其他概念拥有的数据而直接引入数据库）。
7. 记下错误处理策略与关联追踪方式。

发现按这个格式呈现：

```text
## patterns detected
- [N] 个动作后 sync（事件驱动，错误隔离）
- [N] 个前置校验 sync（在目标动作前调用，错误传播）
- [N] 个定时 sync（周期性批处理）

## boundary concerns
- [文件:行] sync 直接查询了归 [概念] 所有的 [表] —— 应该用 [概念.动作]
```

## 新建模式指引

从 sync 描述设计时：

1. 识别源概念与目标概念（各自应已有 `CONCEPT.md`，或至少是候选）。
2. 确定时机：动作后、前置校验，还是定时？
3. 定义数据契约：哪些字段从源流向目标？
4. 明确执行条件：这个 sync 什么时候执行、什么时候跳过？
5. 按时机模式选择错误策略（见设计规则 5）。
6. 考虑级联：这个 sync 会不会触发另一个 sync？如果会，声明深度上限。

## 生成之后

1. 把 sync 图呈现给用户评审。
2. 询问：「时机模式对吗？有 sync 需要拆开或合并吗？」
3. 只有在用户同意之后才写 `SYNCS.md` 文件。
4. 如果 `SYNCS.md` 已存在，展示改动的 diff。
5. 如果项目里存在 `ARCHITECTURE.md`，提醒用户：「SYNCS.md 已变更——跑 `wyx:map` 重新生成 ARCHITECTURE.md。」`## coordination graph` 是架构地图边的最高优先级来源（见 `map.md` 第二步的优先级顺序第 1 位），所以 sync 的改动与图直接相关。
6. 如果存在相关的 `CONCEPT.md`，建议：「跑 `wyx:concept drift` 核实 sync 引用是否与当前概念声明一致。」

## 与其他 wyx 模式的关系

- **`wyx:concept`**：协调图里的每个概念都应该有 `CONCEPT.md`。`SYNCS.md` 引用的是 `CONCEPT.md` 里声明的概念动作。
  `CONCEPT.md` 的 `## interactions` 是概念视角看自己的 sync 关系；`SYNCS.md` 是 sync 目录视角看同一批关系——附带执行细节。
  **放置**：每个 sync 目录只保留一份 `SYNCS.md`——协调图需要所有 sync 流的完整视图。hook 的向上查找行为见 `concept.md`。
- **`wyx:pipeline`**：当一个 sync 包含数据转换阶段时，这些阶段可能也会出现在某份 `PIPELINE.md` 里。`SYNCS.md` 管协调，`PIPELINE.md` 管数据质量。会做数据转换的 sync 应该引用它的 `PIPELINE.md`。
