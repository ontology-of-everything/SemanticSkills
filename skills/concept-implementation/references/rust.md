# Rust 落地

## 工程骨架

cargo workspace，一个 concept 一个 crate：

```text
app/                # 组合根：唯一命名具体 adapter 的地方，装配后接路由
syncs/              # 组合层：每个 flow 一个模块
concepts/
  user/             # 一个 concept 一个 crate
  password/
  session/
shared-kernel/      # 仅通用基础类型（Id、时间），无业务
```

依赖方向由 cargo 强制：`app → syncs → concepts/*`；`concepts/*` 互不声明依赖，即互不可引用。adapters 是概念 crate 内的子模块，具体实现由 app 组合根选用。

概念分组落为目录嵌套（`concepts/billing/invoice/`），workspace `members` 用 glob（`concepts/*/*`）覆盖；crate 名与依赖规则不变，不产生组级新规则。syncs 拆包即 `syncs/` 下每组一个 crate。成员只能属于一个 workspace；多层目录不等于嵌套 workspace，拆独立 workspace 时重新配置成员与构建。

## 概念 crate 内部

```text
concepts/password/src/
  domain.rs      # 不变量与纯逻辑，不依赖其他概念/协议
  actions.rs     # 概念 actions，依赖 port trait
  ports.rs       # 如 trait PasswordStore
  adapters/      # sqlx / 内存实现，供组合根选用
```

port 即 trait、adapter 实现 trait、依赖只指向 domain；用泛型做零开销静态分发，需要运行期换实现时用 `Arc<dyn Trait>`。

## 错误与身份

`Password<U>` 的 U 是泛型身份，不引用 User 概念类型。公开方法可用 `Result` 表达已声明输出，但 mediator 中 `users.register(...)?; passwords.set(...)?` 可能留下只注册用户的部分状态：必须按已确认契约补偿/重试或采用适用事务，不能用 `?` 当作完整注册流程。

## 接口层落点

app 内 `api` 模块（或独立 interfaces crate）：axum/tonic 路由只调 syncs 函数；serde DTO、OpenAPI/proto 契约只存在于此层，概念 crate 不依赖任何协议库。

## 架构看护

- **cargo 本身是第一道防线**：crate 间依赖必须在 `Cargo.toml` 显式声明，概念 crate 之间不声明即编译不过——workspace 依赖图就是规则。
- **cargo-deny** 检查包级依赖政策，不能区分同一 crate 内 domain 与 adapter；层级约束需拆 crate 或源码边界检查。
- CI 用 `cargo metadata` 的解析图断言概念间无依赖（包含项目支持的 features）；`cargo tree -i` 仅供人工诊断，不是自动断言。

依据：[Cargo workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)、[cargo-deny bans](https://embarkstudios.github.io/cargo-deny/checks/bans/cfg.html)。
