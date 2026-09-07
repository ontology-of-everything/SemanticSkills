# TypeScript 落地

## 工程骨架

pnpm workspace（monorepo），一个 concept 一个包：

```text
packages/
  concepts/
    user/            # 独立包：src/domain.ts, actions.ts, ports.ts, adapters/
    password/
  syncs/             # 组合层：每个 flow 一个模块
  app/               # 组合根 + 接口适配（fastify/express 路由 → syncs）
  shared-kernel/     # 仅基础类型
```

- port 用 `interface`，adapter 实现之，组合根构造注入；概念包的 `package.json` 不声明其他概念包为依赖。
- 类型参数直接用 TS 泛型（`Password<U>`）或不透明 ID（branded type）。
- 概念分组落为目录嵌套（`packages/concepts/billing/invoice/`），workspace glob（`packages/concepts/*/*`）覆盖；包名与 dependency-cruiser 规则不变，不产生组级新规则。syncs 拆包即每组一个 sync 包。

## Sync 两种落地

- **过程式**：syncs 包中每 flow 一个模块，async mediator 函数顺序调用概念 actions。
- **声明式**：[LegibleSync](https://github.com/mastepanoski/legiblesync)（`@legible-sync/core`，WYSIWID 论文的社区引擎实现）——概念实现 `execute(action)` 接口，sync 写成 `when`/`then` 规则对象注册进引擎，引擎派发并自带动作溯源。

## 接口层

app 包的路由只调 syncs；DTO 校验（zod）与 OpenAPI 契约都在 app 包，概念包零 HTTP 依赖。

## 架构看护

- **dependency-cruiser**（CI 校验的事实标准）：固化规则——概念包互不引用、只有 syncs 与 app 可引用多个概念、概念的 domain 不得引协议库；`depcruise` 进 CI，违规即失败。
- **eslint-plugin-boundaries**：同样的规则做成 IDE 实时反馈，写代码时即报错。
