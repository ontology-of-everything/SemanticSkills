# Mock 实名认证接口契约

接口形态参考业界三段式（飞书扫码登录 / 支付宝 `certify.initialize`+`certify.query` /
Stripe Identity verification sessions）：**创建会话 → 轮询状态 → 终态收敛**。

## Base URL 与环境变量

| 变量 | 默认 | 作用 |
| --- | --- | --- |
| `HUAWEICLOUD_ONBOARDING_BASE_URL` | `http://127.0.0.1:3923` | 客户端脚本指向的服务地址（真实 API 上线后只改这里） |
| `HUAWEICLOUD_ONBOARDING_MOCK_PORT` | `3923` | mock server 监听端口 |
| `HUAWEICLOUD_ONBOARDING_QR_TTL_SECONDS` | `180` | 二维码有效期（演示超时场景可设 15） |
| `HUAWEICLOUD_ONBOARDING_POLL_INTERVAL_SECONDS` | `3` | 轮询间隔 |
| `HUAWEICLOUD_ONBOARDING_POLL_TIMEOUT_SECONDS` | `600` | 轮询安全上限（防止 scanned 永久挂起） |

## 状态机

```text
pending ──扫码(打开 H5 页)──> scanned ──手机确认──> approved | rejected
   │
   └─ 超过 expires_at 未扫码 ──> expired      （scanned 之后不再过期）
```

任一会话 `approved` 后，账号级状态 `verified` 翻转为 `true` 并持续（server 进程内）。

## 端点

### `POST /v1/verifications` — 创建认证会话

- `201` 返回：`verification_id`（uuid）、`status=pending`、`created_at`、
  `expires_at`、`verify_url`（二维码内容，指向本机局域网 IP 的 H5 页）
- `409`（`ONBOARD.0409`）：账号已实名，不允许重复创建

### `GET /v1/verifications/{id}` — 会话状态查询（轮询）

- `200` 返回：`status`（`pending|scanned|approved|rejected|expired`）、
  `scanned_at`、`completed_at`、`reason`（rejected 时的原因）
- `404`（`ONBOARD.0404`）：会话不存在

### `GET /v1/customers/me/verification-status` — 账号级实名状态

- `200` 返回：`verified`（bool）、`verified_at`、`method`（mock 固定 `qr_mock`）

### `GET /verify/{id}` — 手机扫码打开的 H5 页

打开瞬间将 `pending` 置为 `scanned`；页面提供「通过认证 / 拒绝」两个按钮。
过期/已完成的会话展示对应终态页。

### `POST /verify/{id}/decision` — H5 页提交决定（内部端点）

- Body：`{"action": "approve" | "reject"}`
- 仅 `pending/scanned` 可提交；终态会话返回 `409`（`ONBOARD.0410`）

## 客户端脚本

| 脚本 | 作用 | 机器可读输出 |
| --- | --- | --- |
| `scripts/create-verification.js` | 创建会话 + 终端渲染二维码 | 末行 `VERIFICATION_ID=<uuid>`；已实名时 `ALREADY_VERIFIED=1` |
| `scripts/poll-verification.js <id>` | 3s 轮询至终态 | 末行 `RESULT=approved\|rejected\|expired\|poll_timeout` |

### 退出码（poll-verification.js）

| 码 | 含义 |
| --- | --- |
| 0 | approved |
| 2 | rejected |
| 3 | expired |
| 4 | 轮询超时 / 网络或参数错误 |
