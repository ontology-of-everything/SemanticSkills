# Java 落地（Spring Modulith 主线）

[Spring Modulith](https://spring.io/projects/spring-modulith) 是 Spring 官方的模块单体工具（2.x GA，Maven Central，BOM `spring-modulith-bom`），与概念映射几乎一一对应。备选：纯 Maven/Gradle 多模块 + ArchUnit，规则同理但需手写。

## 工程骨架

单个 Spring Boot 应用，顶级包即模块边界：

```text
com.example.app/
  user/          # 一个 concept 一个 application module
  password/
  session/
  syncs/         # 组合模块：mediator 应用服务或事件监听
  api/           # 接口适配层：controller → syncs
```

- 概念包即 `@ApplicationModule`：对外只暴露包根的公开类型（module API），内部子包默认对外不可见。
- 概念间零引用由 Modulith 校验；类型参数落为泛型或 ID 值对象（record）。
- 概念包内部照端口-适配器分层：domain / actions（应用服务）/ ports（接口）/ adapters（JPA 等实现）。
- 概念分组落为中间包层（`com.example.app.billing.invoice`），用 Modulith 的嵌套 application module 声明；模块可见性与 `verify()` 规则不变，不产生组级新规则。syncs 拆包即 syncs 下每组一个子包。

## Sync 两种落地

- **过程式**：syncs 模块里的应用服务，`@Transactional` 包住一条 sync（单库共享事务），顺序调用各概念的 module API。
- **声明式（事件即 sync）**：概念完成动作时经 `ApplicationEventPublisher` 发布自身事件（事件类型属于概念自己，不点名他人）；syncs 模块用 `@ApplicationModuleListener` 监听并调用下一个概念动作。跨事务可靠性用 Modulith 的事件发布日志/外化 outbox。

## 接口层

api 模块的 `@RestController` 只调 syncs 应用服务；DTO 与 OpenAPI 契约都在 api 模块，概念包不出现 web 依赖。

## 测试与看护

- `ApplicationModules.of(App.class).verify()`——一条测试固化全部模块边界规则（底层 ArchUnit），进 CI。
- `@ApplicationModuleTest` 按模块切片做集成测试，概念的 OP 场景落在这里。
- `Documenter` 可从代码生成各模块文档与关系图——与 PRD 对账的现成素材（供 `jackson-concept-audit` 使用）。
