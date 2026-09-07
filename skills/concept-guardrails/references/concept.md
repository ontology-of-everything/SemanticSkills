# 有边界的概念设计（wyx:concept）

生成**概念规格**——一份结构化的模块描述，作为代码生成的压缩上下文。它提供行为契约，但不能替代审计时读取实现。

新建规格采用基于 Daniel Jackson *Beyond Objects*（2026）的本仓记法；已有 wyx 原生格式保留其边界段与约定。Jackson 模板为：`purpose` / `principle` / `state` / `actions`（含 `_` queries）。跨概念边只写在 `SYNCS.md`。

## 如何解读用户参数

从参数判断模式：

- **目录或文件路径**（如 `src/lib/server/auth/`）：**回填模式** —— 读现有代码，提出一份描述「已经存在的东西」的概念规格。发现的任何边界破坏都要标出来（引用了其他模块的内部实现、共享可变状态等）。
- **功能描述**（如 `带自选清单的投资组合跟踪`）：**新建模式** —— 从描述设计一份新的概念规格。强制分解：如果这个功能包含多个互相独立的目的，就拆成多个概念。缺口或边界不明时回 `concept-design`，不要在回填里发明模型。
- **`drift` 或 `check`**（可带路径，如 `drift src/lib/server/`）：**漂移检测模式** —— 把现有 `CONCEPT.md` / `PIPELINE.md` / `SYNCS.md` 与当前代码对比，产出结构化的漂移报告。
- **没有参数**：**发现模式** —— 分析项目结构，提出哪些模块应该有概念规格。每个候选列一行 purpose。**不要**生成完整规格；询问用户想细化哪些。列完概念候选后，如果项目里存在数据转换模式或跨概念协调，简短提示 `wyx:pipeline` 和 `wyx:sync`。

## 概念规格格式

规格写成 `CONCEPT.md` 文件，放在**实现代码旁边**（如 `src/lib/server/auth/CONCEPT.md`）。

Jackson 方言使用以下结构（与 `concept-prd` / `concept-design` 对齐）；原生方言保留现有模板，不静默迁移。
填好的对照：`Reserving [User, Slot]` 与 `Availability [Venue]`（query `_getAvailableSlot` 在 Availability；组合只在 sync）。

```markdown
# concept Name [T, ...]

## purpose
[恰好一个：这个概念解决什么需要]

## principle
after [用户做了什么]
then [purpose 被兑现的结局]

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

可选 `## notes`：应用角色、类型参数实例化。四节不出现其他概念名。
Jackson 方言不写 `## interactions` / `## dependencies` / `## known coupling`；旧版耦合记录保留在原生格式，迁移时转入应用级取舍记录。
类型参数是列表：可零个（省略 `[]`）、一个或多个（`Reserving [User, Slot]`）；每个参数是无约束身份。
状态也可用等价 Alloy 关系式（`password: U -> String`）。
回填时若发现绕过动作接口的耦合，报告为漂移的 Boundary violation，不写进规格。

## 设计规则

生成或评审概念规格时，应用这五条规则：

1. **单一目的**：每个概念只服务一个目的。如果你在写 purpose 时用上了「并且」，就考虑拆分。

2. **概念独立性**：一个概念的定义不引用另一个概念。概念之间不互相调用；组合只经 `SYNCS.md`。看到直接引用其他模块的内部类型或状态，就标为边界破坏。

3. **状态归属**：每一份状态只归属一个概念。概念之间没有共享可变状态。组合层经拥有者的 query 或动作传递数据；概念之间仍不互调。

4. **动作即接口**：对一个概念的全部外部访问都走它声明的动作或 `_` query。不允许伸手进实现细节。

5. **动作是声明，不是事件**：动作定义模块「能做什么」，不定义「它运行时发生了什么」。不要从动作声明推导出运行时基础设施（日志、指标、拦截器、中间件）。基础设施只有满足独立目的与完整行为判据时才建模为概念，否则保留为实现支撑。

## 执行与核对

回填：读取导出项、调用点、import/use/require、持久化定义，识别 purpose、状态归属、动作及实际使用故事。把纯编排归入 SYNCS，支撑类型/工具不强行建概念；跨概念内部访问、共享可变状态、多个不相关目的逐项附文件位置报告，不能写进理想规格后宣称现状正确。

新建/更新：定义目的与最小状态，补齐公开动作、输出 case 及不变量，再用 principle 检验价值。复杂分解或未决产品边界交接 concept-design；已有授权的明确部分继续完成。

公开契约包含必要的权限/身份参数；公共参数可以集中定义，但须标适用动作、类型及展开规则，确保 sync 能逐项核对。省略无可观察影响的缓存/索引，不把内部辅助函数漏写当契约漂移。

交付前按入口的授权约定呈现草案/diff；每个语义依赖、动作/query 引用均可定位。principle 是代表性故事，不能替代 actions/state 定义的完整正确性。

## 规格放置与 hook 行为

边界注入 hook 从被编辑文件所在目录**向上**走，在**第一个含 `CONCEPT.md` 或 `PIPELINE.md` 的目录**停下（这两者提供边界）。`SYNCS.md` 会被识别并列出，但**不**终止向上查找。

上游 hook 脚本仍提取 `## interactions` / `## dependencies`（见 `hooks-runtime.md`）；Jackson 规格没有这两段，hook 仅列规格并提示缺边界段。
agent 应自己读本目录 `CONCEPT.md` 全文，以及 `SYNCS.md` 里点名本概念的 `sync` 块。`PIPELINE.md` 的 `## data boundary` 仍会被注入。

```text
src/lib/
├── orders/              # 一个概念 = 一个目录
│   ├── CONCEPT.md
│   └── service.ts
├── scoring/
│   ├── CONCEPT.md
│   ├── PIPELINE.md      # 与概念同目录共存
│   └── calculate.ts
└── syncs/
    ├── SYNCS.md         # 本 syncs 目录的全部 sync
    └── order-to-inventory.ts
```

**规格同目录共存**：当管道属于某个概念时，把 `CONCEPT.md` 与 `PIPELINE.md` 放在同一目录。

### 要避开的反模式

- **根目录级 `CONCEPT.md`**：放在 `src/` 的 `CONCEPT.md` 会成为所有子目录（那些没有更近规格的）的兜底边界——把过宽的约束套到未覆盖模块上。
- **规格放在子目录**：`scoring/transforms/PIPELINE.md` 会让 hook 在查找边界时停在那里。hook 随后向上走到 `scoring/CONCEPT.md`，带 `[SHADOWED]` 标注——能用，但放置不理想。
- **规格离代码太远**：放得离实现很远的 `CONCEPT.md`，在附近文件被编辑时不会触发。

## 漂移检测模式

当参数以 `drift` 开头时，跨全部规格类型检测规格与代码的脱节，包含跨规格引用校验。程序见 `drift-detection.md`。
