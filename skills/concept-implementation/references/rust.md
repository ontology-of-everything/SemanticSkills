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

概念分组落为目录嵌套（`concepts/billing/invoice/`），workspace `members` 用 glob（`concepts/*/*`）覆盖；crate 名与依赖规则不变，不产生组级新规则。syncs 拆包即 `syncs/` 下每组一个 crate。按组分治时才升级嵌套 workspace。

## 概念 crate 内部

```text
concepts/password/src/
  domain.rs      # 不变量与纯逻辑，零外部依赖
  actions.rs     # 概念 actions，依赖 port trait
  ports.rs       # 如 trait PasswordStore
  adapters/      # sqlx / 内存实现，供组合根选用
```

port 即 trait、adapter 实现 trait、依赖只指向 domain；用泛型做零开销静态分发，需要运行期换实现时用 `Arc<dyn Trait>`。

## 示例

概念规范 `Password [U]` 与一条 sync 的映射：

```rust
// concepts/password：类型参数 U 落为泛型，不认识 User 概念
impl<U: Copy + Eq, S: PasswordStore<U>> Password<U, S> {
    pub fn set(&mut self, user: U, password: &str) -> Result<U, PasswordError> { /* … */ }
    pub fn check(&self, user: U, password: &str) -> Result<bool, PasswordError> { /* … */ }
}

// syncs：sync Registration 的过程式落地
pub fn register(
    users: &mut UserConcept,
    passwords: &mut PasswordConcept<UserId>,
    req: RegisterRequest,
) -> Result<Registered, AppError> {
    let user = users.register(&req.username, &req.email)?; // when User.register 成功
    passwords.set(user, &req.password)?;                   // then Password.set
    Ok(Registered { user })
}
```

## 接口层落点

app 内 `api` 模块（或独立 interfaces crate）：axum/tonic 路由只调 syncs 函数；serde DTO、OpenAPI/proto 契约只存在于此层，概念 crate 不依赖任何协议库。

## 架构看护

- **cargo 本身是第一道防线**：crate 间依赖必须在 `Cargo.toml` 显式声明，概念 crate 之间不声明即编译不过——workspace 依赖图就是规则。
- **cargo-deny（bans）**：禁止概念 crate 引入协议/框架依赖（如 axum、serde_json 进 domain）。
- CI 核验：`cargo tree -i <concept-crate>` 确认反向依赖只来自 syncs 与 app。
