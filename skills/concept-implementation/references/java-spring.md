# Java / Spring Modulith

一个概念对应一个 application module；默认主包的直接子包被识别为模块。推荐 `concept/actions/ports/adapters` 的内部组织，`syncs` 组合、`api` 处理协议。类型参数用泛型/不透明 ID，避免引用其他概念实体。

## 显式验证独立性

`ApplicationModules.of(App.class).verify()` 默认检查无环与内部包访问；它**不禁止所有概念间 API 依赖**。为概念配置 `@ApplicationModule(allowedDependencies = {})`，或仅允许必要的非概念支撑模块，再运行 verify。另用 ArchUnit 验证 api/syncs/domain 的项目约束。见[官方验证规则](https://docs.spring.io/spring-modulith/reference/verification.html)。

公开 actions/query 放模块 API；内部适配器的装配遵循模块可见性，可在模块内配置 Bean。若应用组合根显式选择适配器，应暴露工厂/配置接口，不能要求它穿透内部包。

## 组合与测试

mediator 放 syncs。使用 `@Transactional` 前遵守组合参考中的提交/完成事件契约；单库并不保证外部副作用可回滚。

事件监听只实现它实际支持的规则；概念发布自己的完成事件，syncs 消费并调用目标动作。`@ApplicationModuleListener` 与事件发布记录可辅助异步可靠性，但多事件合取、flow 关联、查询绑定和业务幂等需明确实现，不能把“事件即 sync”当完整语义。

`@ApplicationModuleTest` 验证概念 OP 与不变量；组合测试覆盖失败、并发请求隔离与重放。`Documenter` 生成代码关系图可供审计，但不替代产品依赖图。

需要中间包/嵌套模块时先核对项目版本的[模块发现及嵌套可见性](https://docs.spring.io/spring-modulith/reference/fundamentals.html)，重新证明每个概念边界仍受检查；包分组不自动保留原来的 verify 约束。
