---
name: huawei-cloud-account-onboarding
description: Guides Huawei Cloud real-name verification (实名认证) via terminal QR code — check account status, generate a scan-to-verify QR, poll every 3s until approved/rejected/expired. Use when the user mentions 华为云/Huawei Cloud plus 实名认证/实名/认证状态/real-name verification, or an account-opening flow says verification is required. Currently a local mock demo; refuses to collect real ID documents or credentials, and non-Huawei-Cloud identity flows.
license: Apache-2.0
compatibility: Node.js 18+, local network (phone on same WiFi to scan); mock only, no Huawei Cloud credentials needed
metadata:
  author: ontology-of-everything
  version: "0.1.0"
---

# 华为云账号开通 · 实名认证引导

> **华为社区版** · 社区维护，非华为云官方。当前为 **本地 mock 演示**：接口形态参考业界标准（创建会话 → 轮询状态 → 终态收敛，同飞书扫码/支付宝实人认证/Stripe Identity），真实 API 上线后仅需替换 `HUAWEICLOUD_ONBOARDING_BASE_URL`。

## Workflow

所有命令在本技能目录执行；首次使用先 `cd scripts && npm install`。

### Step 0 · 确保 mock 服务在运行

```bash
curl -s http://127.0.0.1:3923/healthz || (node scripts/mock-server.js &)
```

服务监听 `0.0.0.0`，二维码 URL 自动使用本机局域网 IP——**用户手机须与本机同一 WiFi**。

### Step 1 · 查账号实名状态

```bash
curl -s http://127.0.0.1:3923/v1/customers/me/verification-status
```

- `verified: true` → 告知用户已完成实名认证，无需重复操作，流程结束。
- `verified: false` → 进入 Step 2。

### Step 2 · 生成二维码

```bash
node scripts/create-verification.js
```

终端渲染彩框二维码（码体黑白保证可扫性），并输出 `VERIFICATION_ID=<uuid>`。提示用户：**用手机扫码，在打开的页面上完成认证**；二维码有效期 180 秒（可用 `HUAWEICLOUD_ONBOARDING_QR_TTL_SECONDS` 覆盖），已扫码后不再过期。

### Step 3 · 每 3 秒轮询直至终态

```bash
node scripts/poll-verification.js <VERIFICATION_ID>
```

脚本自带 3 秒间隔轮询与状态提示（等待扫码 → 已扫码请在手机完成 → 终态）。按退出码收敛：

| 退出码 | 含义 | 对用户说什么 |
| --- | --- | --- |
| 0 | approved | 恭喜，实名认证已完成 |
| 2 | rejected | 认证被拒绝，可重新发起（回 Step 2） |
| 3 | expired | **二维码已失效**，询问是否重新生成一张（回 Step 2） |
| 4 | 轮询超时/错误 | 检查 mock 服务是否存活，报告错误原因 |

## Critical Rules

1. **绝不采集真实身份信息** — 用户在对话里粘身份证号、证件照、AK/SK 一律拒收；mock 页面也不输入任何真实信息。
2. **不代替用户认证** — 扫码和手机上的确认必须由用户本人完成；技能只生成二维码和轮询状态。
3. **过期必须重问** — 轮询到 `expired` 后不要自动重新生成，先提示"二维码已失效"并询问用户是否再来一张。
4. **只服务华为云场景** — 其他云厂商或通用 KYC 流程不适用本技能。
5. **如实声明 mock** — 用户询问时明确当前为本地演示环境，不产生真实的华为云实名记录。

## References

| 何时读 | 文件 |
| --- | --- |
| 接口契约 / 状态机 / 环境变量 / 退出码 | `references/api-contract.md` |
