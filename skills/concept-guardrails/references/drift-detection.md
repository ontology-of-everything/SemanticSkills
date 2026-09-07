# 漂移检测程序（wyx:concept drift）

当参数以 `drift` 开头时，扫描规格与代码的脱节。

## 工作方式

1. **找出全部规格**：定位目标路径下（未给路径则为整个项目）所有 `CONCEPT.md`、`PIPELINE.md`、`SYNCS.md`。限定了路径时，还要找范围之外的相关规格：向上查找祖先规格，并找出别处任何引用了目标路径内概念的 `SYNCS.md` 或 `PIPELINE.md`。这样即使在限定范围的模式下，跨规格校验也仍然完整。
2. **对每份规格**：同时读规格**和**对应的实现代码。
3. **对比**：按下面各个类别检查脱节。
4. **报告**：产出结构化的漂移报告。

**多语言项目**：当一个概念有多种语言的实现时，把漂移检查的范围扩大到全部相关目录，或者在每种语言的实现旁边各放一份 `CONCEPT.md`。漂移检测与语言无关——模型能读任何语言。

## 并行扫描

发现 5 份以上规格时，用只读的探索型子 agent 并行扫描。只读子 agent（结构上没有写入 / 编辑能力）做漂移分析是安全的。阈值比 `wyx:map` 的 10 份更低，因为漂移子 agent 每个任务要同时读规格**和**实现代码；单任务负载更重，在更小的 N 上就能摊平 agent 启动开销。

**必须在派发时显式指定模型，而且要用比 `wyx:map` 更强的档位**（上游 wyx 固定用 `opus`，`wyx:map` 用 `sonnet`）。原因在失败方向：这些子 agent 会给出**「不存在」类断言**（`Missing action: ✓ clean`），而错误的判定不会产生任何可被察觉的输出。永远不要让派发继承会话模型——那样 N 个子 agent 会跑在用户当时恰好在用的档位上。

- 每个子 agent 分配 **2-3 份相邻的规格**；只有当单份规格的实现大到分组会撑爆子 agent 上下文时，才降到一份一个。分组是让高档位模型负担得起的成本控制手段——如果一份规格一个 agent，一个 20 份规格的项目就会派发 20 个。
- 每个子 agent 读规格 + 实现代码，按漂移报告格式返回发现（类别、严重度、文件:行、描述）。
- 全部子 agent 完成后，把发现合并成单份漂移报告，然后在主上下文里做跨规格校验和系统性模式聚合。

### 子 agent 输出要求

每个子 agent 必须对每一个适用的检查类别都给出判定（例如「Missing action: ✓ clean」、「Changed signature: Low —— 命名风格差异」）。合并阶段把被省略的类别标为「未核实」。

### 子 agent 提示词模板

派发子 agent 做并行漂移扫描时，每个提示词里都要包含：

1. 分配给它的规格路径及其类型（CONCEPT / PIPELINE / SYNCS）。
2. 本文「漂移严重度校准」整段（逐字照抄）。
3. 所分配规格类型对应的检查表——**表里的严重度取值具有权威性；子 agent 必须逐字照抄，不得凭自己的判断上调**。
4. 项目约定：要求它读项目根目录的 `CLAUDE.md` / `AGENTS.md`，记下任何被记录在案的横切参数约定（如依赖注入参数、作用域参数）。这些约定在规格 `## actions` 里没有被记录的出现，即使只在单份规格范围内，也算 Medium 的「Cross-cutting parameter」发现。
5. 输出要求：每个检查类别都要有判定——省略即视为未核实。

## 每份 CONCEPT.md 检查什么

| 类别 | 如何识别 | 严重度 |
| --- | --- | --- |
| **Missing action** | 函数 / 方法在代码里存在，但规格 `## actions` 没声明 | **Medium** |
| **Removed action** | 规格声明了动作，但代码里函数已不存在 | **High** |
| **Changed signature** | 函数参数和 / 或返回类型与规格声明不一致——要追踪实际的 return 语句，不能只看类型标注 | **Medium** |
| **New state** | 新的表字段、类字段或持久化数据不在规格 `## state` 里。同时要核查持久化定义（schema 文件、迁移脚本）中是否有既未反映在规格、也未反映在应用类型里的状态 | **Medium** |
| **New dependency** | 引用了某个概念，但它不在规格 `## dependencies` 里 | **High** |
| **Boundary violation** | 直接引用另一个概念的内部实现（未走其声明的动作） | **Critical** |
| **Cross-cutting parameter** | 某参数出现在 3 个以上动作实现里，但 `## actions` 的任何动作签名都没有记录它 | **Medium** |
| **Resolved known gap** | 若规格含 `## known gaps` 段，检查其中记录的缺口是否已被现有代码解决 | **Low** |
| **Resolved known coupling** | 某条 `status: refactor` 的 `## known coupling` 在代码里已不存在（可用 grep 验证所声明的访问方式确已消失）——规格应更新以反映这次解决 | **Low** |

## 每份 PIPELINE.md 检查什么

| 类别 | 如何识别 | 严重度 |
| --- | --- | --- |
| **Missing stage** | 代码里新增的转换步骤未声明在规格 `## stages` | **Medium** |
| **Changed invariant** | 代码逻辑与已声明的不变量相矛盾 | **High** |
| **New data source** | 代码读取了未列在规格 `## sources` 的表 / API | **Medium** |
| **Boundary violation** | 为获取另一个概念拥有的数据而直接引用数据库 | **Critical** |

## 每份 SYNCS.md 检查什么

| 类别 | 如何识别 | 严重度 |
| --- | --- | --- |
| **Missing sync** | 代码里新增的跨概念协调未声明在规格里 | **Medium** |
| **Changed timing** | 代码用的触发方式与规格声明的不同（如定时 vs 动作后） | **Medium** |
| **New participant** | sync 处理器涉及了规格里没列出的概念 | **High** |
| **Removed sync** | 规格声明了 sync，但代码里处理器已不存在 | **High** |
| **Graph inconsistency** | `## coordination graph` 列出的流程没有对应的 `## sync:` 块，或反之 | **Medium** |
| **Missing SYNCS coverage** | 某份 `CONCEPT.md` 的 `## interactions` 声明了协调关系，但任何 `SYNCS.md` 里都没有对应的 sync | **Medium** |

## 漂移严重度校准

- 当规格用的签名比实现的语言特定类型包装更简单时（如异步包装、result / error 类型），视为 Low——除非它改变了错误处理或调用契约。
- 属于实现细节（私有变量、内部缓存、派生计算值）而非概念公开 API 契约的状态字段，标为 Low。
- 私有辅助方法或内部实现函数（未导出、不被模块外调用）被判为「Missing action」时，按 Low 处理——它们是实现细节，不是概念公开 API 契约的一部分。
- 规格与代码之间的命名风格差异（camelCase vs snake_case、缩写 vs 全称）是 Low——风格问题，不是契约破坏。
  例外：如果这个不一致的名字出现在跨规格引用里（`PIPELINE.md` 或 `SYNCS.md`），这**不是**同类别内的升级，而是**重新归类**到跨规格校验类别（`PIPELINE→CONCEPT name mismatch` 或 `SYNCS→CONCEPT missing reference`，二者在下面的跨规格表里都是 High）。
- 同一条 Low 在一份规格的多个动作里重复出现时（如同一个未记录参数出现在 3 个以上动作里），合并为一条 Low，附注列出受影响的动作。合并后的 Low 在 `low_by_spec` 字段里计为 1。
- 把一条发现报为 Medium 或更高之前，先用 grep 或读文件确认它存在于**当前**代码里。不要凭记忆或先前读文件时的印象报漂移。
- **规格的沉默不是漂移。** 不要从规格「没说什么」推出矛盾：规格没提到的行为是**未记录**，不是**被否定**；规格里一句范围狭窄的陈述，并不隐含它所省略的一切都被否定（例如「字段 X 不可过滤」并不等于断言「X 不会被返回」）。
  只有针对规格里明确的陈述才能标为矛盾。这一条不放松 Missing action / New state / New dependency / Missing stage 这几项检查——它们的存在正是为了刻意暴露特定的**未记录的新增项**，继续有效。
- 如果单份规格累积了 5 条以上 Low（去重后），在漂移报告摘要里注明，并建议重新评估该规格的 `## actions` 或 `## state` 是否还足以描述模块当前的公开面。
- 已被源概念 `## known coupling` 记录在案的跨概念数据访问，按 Low 处理，而不是 Critical / High。**未记录**的跨概念数据访问仍然是 Critical。
- 若项目的 `CLAUDE.md` / `AGENTS.md` **明确**把某种跨概念访问记录为有意的架构约定（如「路由 load 函数可以跨概念读取标量字段」），该发现是 Low 而非 Critical——
  但这条发现**必须**建议把它正式写进源概念的 `## known coupling`，让这份许可存在于规格里，而不只存在于项目散文里。
  降级要求约定是**明确记录**的，绝不能靠推断或暗示；有疑问时该访问仍然是 Critical。此类发现要报为 Low，绝不能悄悄压掉。
- **被许可的耦合**：通过公开 API 调用另一个概念声明的动作（包括从 sync 处理器里调用）不是边界破坏。边界破坏需要引用绕过动作接口的内部文件 / 符号。
- **严重度逐字采用检查表的取值。** 检查表里的严重度是经过校准的——不要基于你对影响面的独立判断把 Low 升为 Medium、Medium 升为 High。
  如果一条发现比它最初的类别更严重，**把它重新归类到正确的检查类别**（例如一条「Missing action」实际上是跨概念内部访问 → 归为 Critical 的「Boundary violation」）。
  不要在类别内升级严重度；只允许按上面的校准规则向下调整（如私有辅助函数 → Low、命名风格 → Low）。

## 漂移报告格式

报告按这个格式呈现：

```text
# Drift Report — [日期]

## Summary
- Specs scanned: [N]
- Specs with drift: [N]
- Critical: [N] | High: [N] | Medium: [N] | Low: [N]

## [概念/管道名称] — [path/to/CONCEPT.md]

### Critical
- **Boundary violation**: [文件:行] 直接引用了 [模块] —— 规格声明只能通过 [动作] 交互

### High
- **Removed action**: 规格声明了 `deleteUser`，但代码里已不存在
- **New dependency**: 代码引用了 `PaymentConcept`，但规格 `## dependencies` 只列了 `AuthConcept`

### Medium
- **Missing action**: `exportToCSV()` 在代码里存在，但规格未声明
- **Changed signature**: `createUser` 规格写的是 `[name: string]`，代码接收 `[name: string, email: string]`

## [下一份规格...]
```

## 跨规格引用校验

逐份检查完之后，在扫描范围内交叉校验各类规格之间的引用：

| 检查什么 | 如何识别 | 严重度 |
| --- | --- | --- |
| **PIPELINE→CONCEPT name mismatch** | `PIPELINE.md` 的 `## stages` 或 `## data boundary` 引用的概念动作名，在目标 `CONCEPT.md` 的 `## actions` 里找不到匹配 | **High** |
| **SYNCS→CONCEPT missing reference** | `SYNCS.md` 的 sync 块引用了 `Concept.action`，而该动作在目标 `CONCEPT.md` 里不存在 | **High** |
| **SYNCS→CONCEPT missing participant** | `SYNCS.md` 的 sync 块点名了某个概念，但没有对应的 `CONCEPT.md` | **Medium** |
| **CONCEPT→CONCEPT missing action** | `## interactions` 引用了 `OtherConcept.actionName()`（仅限显式方法调用语法），但该动作在目标 `CONCEPT.md` 的 `## actions` 里不存在 | **High** |
| **CONCEPT→CONCEPT missing concept** | `## dependencies` 引用的概念名没有对应的 `CONCEPT.md` | **Medium** |

不匹配项在逐份规格结果之后报告：

```text
## Cross-spec reference validation

### High
- **PIPELINE→CONCEPT name mismatch**: pipelines/PIPELINE.md 引用 `getExpired`，但 scoring/CONCEPT.md 声明的是 `findExpiredItems`
- **SYNCS→CONCEPT missing reference**: SYNCS.md 的 `sync: onPurchase` 引用 `Inventory.decrementStock`，但 Inventory 的 CONCEPT.md 没有 `decrementStock` 动作

### Medium
- **SYNCS→CONCEPT missing participant**: SYNCS.md 引用了 `AuditLog`，但不存在 AuditLog 的 CONCEPT.md
```

## 系统性模式聚合

在逐份结果和跨规格校验之后，识别在多份规格里重复出现的漂移模式。当同一个漂移类别和描述出现在 3 份以上规格里时，把它们归为一个系统性问题，而不是逐条列出：

```text
## Systemic patterns
- **未记录的参数 `modified_by`** 出现在 7 份概念规格中的 4 份 —— 它出现在写操作动作里，但没有声明在 ## actions 签名中。建议在每份受影响的规格里把它记录为公共参数。
- **缺少 `## dependencies` 段** —— 5 份概念规格中有 3 份引用了其他概念却没有这一段。
```

系统性模式指向横切关注点，而不是单份规格的漂移。把它们标出来做批量处理。

## 漂移报告之后

### 第一阶段 —— 审计（只读）

1. 把完整报告呈现给用户。
2. 对每份有漂移的规格询问：「是更新规格去匹配代码，还是这其实是代码缺陷？」对每条发现，简要说明规格和代码哪一边看起来更新，帮用户决定修复方向（改规格 vs 改代码）。
3. 当发现指向结构性问题（边界破坏、状态重叠、横切模式）时，指出适用的是哪条设计规则（1-5），并建议对应的 wyx 模式——无论是更新既有规格还是新建一份（`wyx:concept`、`wyx:pipeline`、`wyx:sync`、`wyx:audit`）。
4. 摘要之后加一行「建议的下一步」，列出优先级最高的 wyx 命令（如对有漂移的规格跑 `wyx:concept 路径/`，若发现未覆盖模块则跑 `wyx:audit`）。
5. 如果扫描过程中观察到未覆盖的模块，建议：「跑 `wyx:audit` 检查整体规格覆盖。」

### 第二阶段 —— 修复（用户批准后才写入）

1. 若更新规格：生成所需的最小改动，经用户确认后应用。
2. 若是代码缺陷：标出待修（规格是预期契约）。
3. 若已应用规格改动且存在 `ARCHITECTURE.md`，提醒用户：「规格已更新——跑 `wyx:map` 重新生成 ARCHITECTURE.md。」

### 第三阶段 —— 记录漂移历史

#### detect 记录

向 `.claude/wyx-drift-history.jsonl` 追加一条 detect 记录：

```json
{"ts":"<ISO-8601>","action":"detect","specs_scanned":<N>,"specs_with_drift":<N>,"critical":<N>,"high":<N>,"medium":<N>,"low":<N>,"low_by_spec":{"path/CONCEPT.md":<N>},"path":"<扫描路径或 project>"}
```

`action` 字段用于区分 detect 与 fix 记录（见下一条）。没有 `action` 字段的旧记录按 `"detect"` 处理以保持向后兼容。

`low_by_spec` 记录每份规格的 Low 数量，用于观察累积趋势。与先前记录比较时，标出 Low 数量上升的规格——Low 的累积说明规格对公开面的描述正在落后于实现的增长。这条 detect 记录让 SessionStart hook 能报告上次漂移检查的时间。

#### fix 记录

**如果在同一会话里应用了修复**（第二阶段），追加一条引用该 detect 记录的 fix 记录：

```json
{"ts":"<ISO-8601>","action":"fix","specs_fixed":<N>,"specs_remaining":<N>,"ref_ts":"<detect 记录的 ts>"}
```

- `specs_fixed`：本轮修复解决的规格数量
- `specs_remaining`：仍在漂移的规格数量（detect 的 `specs_with_drift` 减去已修复的）；`0` 表示漂移已完全解决
- `ref_ts`：**最近一条 detect** 记录的 `ts` —— 也就是这次修复所针对的那一次扫描（把修复与它的来源扫描绑定起来）

JSONL 是只追加的——绝不修改已有记录。SessionStart hook 读最后一条：如果 `action=fix`，它报告 `specs_remaining` 而不是更早的 `specs_with_drift`，这样会话头部反映的是真实的待处理数量，而不是过时的检测数字。

### 清除「修复后需重扫」提醒（可选）

一轮修复会编辑规格文件，它们的 mtime 因此比原来的 detect 记录更新——下次会话开始时 hook 会再次提示这些规格在上次漂移检查之后被改过。这是预期行为：规格被编辑正是该提醒要追踪的事情。

要诚实地清除它，重新跑一次 `wyx:concept drift` —— 对现在已经干净的规格做一次真实扫描，会写入一条时间戳晚于修复的新 detect 记录，于是规格不再比最后一次测量更新。

**不要**凭记忆手写一条 `specs_with_drift: 0` 的 detect 记录：detect 记录断言的是一次真实测量，伪造一条干净记录会让未来的警告对着未经核实的规格闭嘴（正是「陈旧规格」这种失效模式）。要重新测量，不要凭空合成。

### 快照语义（v0.17 不变量）

每条记录都是快照，不是账本。一条新的 detect 记录覆盖之前任何 fix 记录的 `specs_remaining` —— SessionStart 只读最后一条，所以新测得的 `specs_with_drift` 取代先前的待处理状态。如果一轮 fix 只解决了部分规格、用户随后重扫，新的 detect 就是权威计数；hook 不会回溯去合并 detect / fix 配对。
