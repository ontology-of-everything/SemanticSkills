---
name: jackson-concept-implementation
description: Maps a confirmed Jackson concept model onto a modular monolith (one module per concept, syncs as mediators or a rule engine). Use this skill whenever the user asks to implement the concept model, 模块单体, or mentions jackson-concept-implementation.
---

# Jackson 概念实现（模块单体）

输入是已确认的概念模型（`jackson-concept-design` 的输出：concepts、syncs、依赖图）。本技能只做模型到代码结构的映射，不重开概念讨论；概念边界有疑问回上游技能，存量工程审计用 `jackson-concept-audit`。

## 映射总则

| 模型元素 | 代码落点 |
| --- | --- |
| 一个 concept | 一个独立编译单元（模块/crate/包），对外只暴露 actions 与状态查询 |
| 类型参数 `[U]` | 泛型参数或不透明 ID（值对象），不引入对方类型 |
| state | 模块私有，经 port 抽象持久化；不是全局数据模型 |
| actions | 模块的公开方法/服务；错误是独立的输出 case（可被错误 sync 匹配），不是抛出即忘的异常 |
| queries（`_` 前缀） | 模块的只读查询方法，不改状态；供 sync 的 where 段与展示层 |
| OP | 该模块的集成测试场景（after/then 场景 = 测试用例） |
| sync | 组合层代码：唯一允许同时引用多个概念的地方 |
| extrinsic 依赖图 | 构建/交付顺序与产品裁剪（feature/构建开关），不产生代码依赖 |

铁律（intrinsic 禁令的代码化）：**概念模块之间零相互引用**；数据与控制流全部经组合层流动。

概念模块内部按整洁架构分层（端口-适配器）：domain 放不变量与纯逻辑（零外部依赖）、actions 即应用服务（依赖 port 抽象）、adapter 实现 port；组合根是唯一命名具体 adapter 的地方。

## Sync 的两种落地（官方路线）

设计层语义是**因果规则**（when 匹配动作完成、where 经 queries 绑定变量、then 触发新调用）：不要求事务，错误是可匹配的输出 case。两条落地路线都实现同一语义：

1. **过程式 mediator**（默认）：每个 flow 入口（`Requesting` 动作）一个编排函数，把该 flow 的若干 sync 顺序内联，调用各概念 actions、组装响应。最简单、最贴近常规 web 实践，Jackson 课程即此教法。
2. **声明式规则引擎**：sync 按条写成 `when / where / then` 规则注册进引擎，由引擎派发并留下动作溯源。表达力强、行为增量可按条增删，但需引入引擎运行时。

行为规则多、需要审计追踪或按规则粒度演进时才选 2。

**时机与错误隔离（实现层工程分类，不改变设计语义）**：落地时按触发源把 sync 归为三类并配对错误策略——
**动作后**（when 匹配概念动作完成：源动作已成功，sync 失败走错误 sync 或记录，不回滚源）、
**前置校验**（where 绑定失败即 flow 不继续：天然阻断，错误返回给请求方）、
**定时**（when 匹配定时器动作：逐条处理，单条失败记录并继续）。
设计层不设"单方向/无环"限制，级联 sync 合法，但实现时为可观测性声明级联深度上限。

## Syncs 层范式

syncs 层是应用级的用例层（整洁架构的 use-case 层），没有自己的 domain，不套完整分层。三原则：

- **薄**：只做编排与数据流；业务不变量必须在概念的 domain 里，出现在 syncs 里就下沉。
- **无自有持久状态**：某组 sync 开始积攒状态 = 升格为概念的信号，回上游技能。
- **按 flow 组织**：每个 flow 一个模块/文件，与 PRD 的 flow 文档一一对应。

## 规模化：概念分组与 syncs 拆包

概念多到平铺难导航、构建变慢或多团队分治时（经验上十余个概念起）按**概念分组**（俗称分域）拆解；无痛点不分组。

- **分组无架构语义**：Jackson 模型没有"域"元素，分组纯属工程组织（目录、交付、团队归属）。零引用铁律对全体概念平坦生效——不存在"同组可互引"，也不存在"组间接口"；跨组唯一通道仍是 syncs。看护规则不必按组升级：组无依赖语义，没有新规则可写。
- **按模型自带产物划分**：首选 extrinsic 依赖图聚类 + flow 亲和（常被同一批 flow 触达的概念归一组），团队所有权决胜，业务命名只作参考——这样分出的组天然是可独立交付的产品子集。
- **默认纯目录分组**（`concepts/<组>/<概念>/`），构建单元不变；团队按组分治或构建时间失控时才升级为构建边界（嵌套 workspace / 父 POM），那只是多一道既有防线，不新增语义。
- **syncs 按组拆包**：flow 是拆解原子、不拆散，flow 模块按组归堆成多个 sync 包。跨组 flow 按**入口 `Requesting` 动作的归属组**落位，不设公共组垃圾抽屉；组合根仍唯一。sync 引用任意组的概念照常合法——syncs 本来就是唯一的多概念引用点，分组不给它加任何限制。
- **规格随包走**：每个 sync 包一份 SYNCS.md，coordination graph 只画本包 flow，不设全局副本（全局视图 = 总体 PRD 依赖图 + `wyx:map` 合成）；CONCEPT.md 跟概念模块走，目录嵌套自动继承。

## 接口层

- **对外 API 只暴露应用动作（即 sync），永不直通概念动作**——概念动作绕过组合层可达，所有 sync 约束（认证、级联、通知）即被穿透。
- 端点 = 组合层入口：路由与 DTO 映射写在接口适配器，概念对 HTTP/协议一无所知，签名中不出现传输格式（JSON、状态码）。
- REST/RPC 入站、webhook 出站等协议适配器全部放 app 边缘的接口模块；契约（OpenAPI/proto）是组合层资产，随应用版本演进，与概念版本无关——同一概念可复用于多个应用，各应用契约不同。路由前缀 / OpenAPI tag 可借用概念分组命名，纯属命名习惯，不改变契约归属。
- 官方模式：外部请求本身是动作——具体化为 `Requesting` 伪概念（论文的 Web 引导概念的现名），端点触发 sync，响应也由 sync 产生；认证、鉴权因此都是普通 sync，不是中间件魔法。

## 失败路径与事务

现行设计语义（因果规则）不要求跨概念事务：动作失败是可匹配的错误输出，默认由**错误 sync** 响应或补偿。工程强化：

- **共享事务（可选）**：模块单体单库时可用 DB 事务包住 mediator 函数（单体红利），换取强一致；各概念仍保持私有 schema/表，跨概念只经 actions 与组合层查询。
- **规则引擎路线**：不做跨概念回滚，全部走错误 sync 补偿。
- 概念内部：单个 action 自身原子，由其存储适配器保证。
- 每条 sync 的失败路径二选一并可指认：错误 sync 补偿，或共享事务。

## 规格共存落位

实现开始时把规格迁到代码旁（`jackson-concept-prd` 暂存于集中 PRD 目录的部分）：每概念 CONCEPT.md 进模块目录、SYNCS.md 进 syncs 目录（按组拆包时随包拆分，见规模化一节）。
此后**规格先行**：先改规格再改实现——共存规格即 wyx 架构护栏（`wyx:concept drift`、边界注入）的扫描对象，也是每个概念可独立重生成的 prompt（概念独立 = 生成时上下文不必带其他概念）。

## 语言落地（按需读取，只读目标语言一份）

- Rust：[references/rust.md](references/rust.md) — cargo workspace、trait 即 port、组合根；cargo/cargo-deny 看护。
- Java：[references/java-spring.md](references/java-spring.md) — Spring Modulith 主线：`@ApplicationModule` 即概念模块、事件即声明式 sync、`verify()` 看护。
- TypeScript：[references/typescript.md](references/typescript.md) — workspace 包边界、LegibleSync 引擎路线；dependency-cruiser 看护。

## 违规信号

- 概念模块引用了另一概念模块 → intrinsic dependency，参数化或把耦合上移到 syncs。
- syncs 里出现业务不变量 → 下沉到所属概念的 domain。
- 一个概念模块服务两个 purpose、或一条 sync 长成流程脚本 → 回上游技能拆分。
- 概念间共享数据库表或全局模型 → 拆为各概念私有 state，跨概念查询放组合层。
- 概念签名出现 DTO/HTTP 类型 → 传输映射上移到接口层 adapter。
- 外部 API 直通概念动作 → 补一条 sync 作为应用动作，端点改挂 sync。
- 以同组为由引用兄弟概念，或给概念分组发明"组间接口" → 分组无架构语义，耦合上移 syncs。
- 共存 CONCEPT.md 出现 interactions / dependencies 段或四节点名其他概念 → 回 `jackson-concept-prd` 重新转录。

## 完成条件

- 模块依赖图核验：概念模块互不依赖；只有 syncs 与 app 引用多个概念。
- 边界规则已固化为架构看护测试并进 CI（工具见语言参考文件）。
- 每条 sync 的失败路径明确：错误 sync 补偿或共享事务，二选一并可指认。
- 每个概念的 OP 有对应集成测试；每条 sync 有对应测试。
- 规格已共存落位（模块目录 CONCEPT.md、syncs 目录 SYNCS.md），且与代码一致。
- 概念模型中的排除动作在代码中未被组合层调用，也未经 API 暴露。
- 依赖图中的产品子集可通过 feature/构建开关裁剪。

## 依据

官方：

- [Beyond Objects](https://arxiv.org/abs/2606.27258)（因果规则语义、Requesting 伪概念、queries、废弃事务语义）
- [WYSIWID 论文](https://arxiv.org/abs/2508.14511)（概念规范格式、sync 语言与引擎、两条落地路线）
- [概念设计综述](https://essenceofsoftware.com/posts/distillation/)（mediator 与零引用原则）
- [conceptbox](https://github.com/61040-fa25/conceptbox)（官方课程模板：规格与代码同仓、规格驱动开发）
- [Spring Modulith](https://spring.io/projects/spring-modulith)（Spring 官方模块单体工具）

社区：[LegibleSync](https://github.com/mastepanoski/legiblesync)（TypeScript 规则引擎实现）；各语言六边形架构与边界看护惯例见语言参考文件。
