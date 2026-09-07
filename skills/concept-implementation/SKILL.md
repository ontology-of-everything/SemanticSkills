---
name: concept-implementation
description: Maps a confirmed concept model (Daniel Jackson's concept design) onto a modular monolith (one module per concept, syncs as mediators or a rule engine). Use to implement an established concept model as a 模块单体, or for concept-implementation.
metadata:
  openclaw:
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/concept-implementation
---

# 概念实现（模块单体）

## 目标

将已确认模型与规格落为概念模块、组合/接口层、共存规格和验证。已确认边界不重开讨论；只把影响实现的模型缺口交回 concept-design，其他部分继续。按请求交付架构方案或实际代码，不以骨架替代已要求的实现。

## 原则

1. **概念模块之间零相互引用**（本仓对独立性的工程约定）：数据与控制流全部经组合层流动；syncs 是唯一允许同时引用多个概念的地方。
2. 对外 API 经应用入口执行已确认的协调/权限策略；应用动作可引发多条 sync，不等于单条规则。
3. 概念自身不变量由其 domain 保证；跨概念策略放 syncs。组合层无自有业务状态，但可持久保存溯源、重试与幂等记录。
4. 错误是可匹配的输出 case，不是抛出即忘的异常；每个可达失败有响应、重试、补偿或有意忽略策略，不能以共享事务替代错误契约。
5. 规格与代码共存，此后规格先行：先改规格再改实现。
6. 分组只是工程组织，不带架构语义；无痛点不分组。

## 流程

1. **映射模型元素**：按下表为每个 concept 建可验证边界的模块（独立包是优选，不强制新建构建单元），按端口-适配器分层（domain 不依赖其他概念或传输协议 → actions 即应用服务、依赖 port → adapter 实现 port；组合根是唯一命名具体 adapter 的地方）。
2. **选 sync 落地路线**：读 `references/composition-layer.md`；默认过程式 mediator，规则多、需审计追踪或按规则演进时选规则引擎。核对入口、完成事件、查询绑定、请求关联与失败路径。
3. **接口层**：端点 = 组合层入口，路由与 DTO 映射写在接口适配器；`Requesting` 动作触发 sync，响应由 sync 产生。
4. **规格共存落位**：CONCEPT.md 进模块目录、SYNCS.md 进 syncs 目录。
5. **语言落地**：只读目标语言一份参考，固化边界看护测试进 CI。
6. **规模化**（仅当十余个概念以上、平铺难导航或多团队分治）：读 `references/scaling.md`。
7. 逐条核对「命题」。

## 命题

- 模块依赖图核验：概念模块互不依赖；只有 syncs 与 app 引用多个概念。
- 边界规则已固化为架构看护测试并进 CI。
- 失败、无匹配、多匹配、重放与并发请求的行为符合契约；事务未改变已完成动作的可观察语义。
- OP 有代表性测试；动作不变量及 sync 的绑定、错误、隔离和重试由行为测试覆盖。
- 规格已共存落位且与代码一致；CONCEPT.md 无 interactions / dependencies 段、四节不依赖其他概念定义（否则回 `concept-prd` 重新转录）。
- 模型中的排除动作未被组合层调用，也未经 API 暴露。
- 依赖图中的产品子集可通过 feature / 构建开关裁剪。

## 记法与模板

| 模型元素 | 代码落点 |
| --- | --- |
| 一个 concept | 一个独立模块，按项目需要选择 crate / 包，对外只暴露 actions 与状态查询 |
| 类型参数 `[T, ...]` | 泛型参数或不透明 ID（值对象），不引入对方类型；可零个或多个 |
| state | 模块私有，经 port 抽象持久化；不是全局数据模型 |
| actions | 模块的公开方法 / 服务；错误是独立的输出 case |
| queries（`_` 前缀） | 模块的只读查询方法；供 sync 的 where 段与展示层 |
| OP | 代表性测试场景，辅以 actions/state 的边界测试 |
| sync | 组合层代码：mediator 函数或规则引擎规则 |
| extrinsic 依赖图 | 构建 / 交付顺序与产品裁剪，不产生代码依赖 |

## 参考

| 何时读 | 文件 |
| --- | --- |
| 选择组合路线时：匹配/绑定、flow、接口、状态、错误与事务、规格共存 | `references/composition-layer.md` |
| 流程第 6 步：概念分组与 syncs 拆包 | `references/scaling.md` |
| 流程第 5 步：Rust（cargo workspace、trait 即 port、依赖图与边界看护） | `references/rust.md` |
| 流程第 5 步：Java（Spring Modulith：`@ApplicationModule` 即概念模块、事件实现部分 sync、`verify()` 看护） | `references/java-spring.md` |
| 流程第 5 步：TypeScript（workspace 包边界、LegibleSync 引擎路线、dependency-cruiser 看护） | `references/typescript.md` |
| 核验出处 | `references/sources.md` |
