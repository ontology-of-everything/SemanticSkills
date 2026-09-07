---
name: concept-implementation
description: Maps a confirmed concept model (Daniel Jackson's concept design) onto a modular monolith (one module per concept, syncs as mediators or a rule engine). Use this skill whenever the user asks to implement the concept model, 模块单体, or mentions concept-implementation.
---

# 概念实现（模块单体）

## 目标

输入：已确认的概念模型（`concept-design` 输出的 concepts、syncs、依赖图）与 `concept-prd` 的规格文件。输出：模型到代码结构的映射——模块骨架、组合层、接口层、看护测试与共存规格。不重开概念讨论：边界有疑问回 `concept-design`，存量工程审计用 `concept-audit`。

## 原则

1. **概念模块之间零相互引用**（intrinsic 禁令的代码化）：数据与控制流全部经组合层流动；syncs 是唯一允许同时引用多个概念的地方。
2. 对外 API 只暴露应用动作（即 sync），永不直通概念动作。
3. 业务不变量只在概念的 domain；syncs 层薄、无自有持久状态、按 flow 组织。
4. 错误是可匹配的输出 case，不是抛出即忘的异常；每条 sync 的失败路径二选一并可指认（错误 sync 补偿 / 共享事务）。
5. 规格与代码共存，此后规格先行：先改规格再改实现。
6. 分组只是工程组织，不带架构语义；无痛点不分组。

## 流程

1. **映射模型元素**：按下表为每个 concept 建独立编译单元，按端口-适配器分层（domain 零外部依赖 → actions 即应用服务、依赖 port → adapter 实现 port；组合根是唯一命名具体 adapter 的地方）。
2. **选 sync 落地路线**：读 `references/composition-layer.md`；默认过程式 mediator，规则多、需审计追踪或按规则演进时选规则引擎。为每条 sync 定时机类别（动作后 / 前置校验 / 定时）与失败路径。
3. **接口层**：端点 = 组合层入口，路由与 DTO 映射写在接口适配器；`Requesting` 动作触发 sync，响应由 sync 产生。
4. **规格共存落位**：CONCEPT.md 进模块目录、SYNCS.md 进 syncs 目录。
5. **语言落地**：只读目标语言一份参考，固化边界看护测试进 CI。
6. **规模化**（仅当十余个概念以上、平铺难导航或多团队分治）：读 `references/scaling.md`。
7. 逐条核对「命题」。

## 命题

- 模块依赖图核验：概念模块互不依赖；只有 syncs 与 app 引用多个概念。
- 边界规则已固化为架构看护测试并进 CI。
- 每条 sync 的失败路径明确：错误 sync 补偿或共享事务，二选一并可指认。
- 每个概念的 OP 有对应集成测试；每条 sync 有对应测试。
- 规格已共存落位且与代码一致；CONCEPT.md 无 interactions / dependencies 段、四节不点名其他概念（否则回 `concept-prd` 重新转录）。
- 模型中的排除动作未被组合层调用，也未经 API 暴露。
- 依赖图中的产品子集可通过 feature / 构建开关裁剪。

## 记法与模板

| 模型元素 | 代码落点 |
| --- | --- |
| 一个 concept | 一个独立编译单元（模块 / crate / 包），对外只暴露 actions 与状态查询 |
| 类型参数 `[U]` | 泛型参数或不透明 ID（值对象），不引入对方类型 |
| state | 模块私有，经 port 抽象持久化；不是全局数据模型 |
| actions | 模块的公开方法 / 服务；错误是独立的输出 case |
| queries（`_` 前缀） | 模块的只读查询方法；供 sync 的 where 段与展示层 |
| OP | 该模块的集成测试场景（after/then 场景 = 测试用例） |
| sync | 组合层代码：mediator 函数或规则引擎规则 |
| extrinsic 依赖图 | 构建 / 交付顺序与产品裁剪，不产生代码依赖 |

违规信号 → 处置：概念模块引用另一概念模块 → 参数化或上移 syncs；syncs 里出现业务不变量 → 下沉 domain；一个模块服务两个 purpose 或一条 sync 长成流程脚本 → 回 `concept-design`；概念间共享表或全局模型 → 拆为私有 state；概念签名出现 DTO/HTTP 类型 → 上移接口适配器；外部 API 直通概念动作 → 补一条 sync 并改挂。

## 参考

| 何时读 | 文件 |
| --- | --- |
| 流程第 2–4 步：sync 两条路线、时机与错误隔离、syncs 层范式、接口层、失败路径与事务、规格共存 | `references/composition-layer.md` |
| 流程第 6 步：概念分组与 syncs 拆包 | `references/scaling.md` |
| 流程第 5 步：Rust（cargo workspace、trait 即 port、cargo-deny 看护） | `references/rust.md` |
| 流程第 5 步：Java（Spring Modulith：`@ApplicationModule` 即概念模块、事件即声明式 sync、`verify()` 看护） | `references/java-spring.md` |
| 流程第 5 步：TypeScript（workspace 包边界、LegibleSync 引擎路线、dependency-cruiser 看护） | `references/typescript.md` |
| 核验出处 | `references/sources.md` |
