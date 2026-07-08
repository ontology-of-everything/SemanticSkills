# 华为云账号开通 · 实名认证引导

`huawei-cloud-account-onboarding` · **Huawei Cloud Account Onboarding — Real-Name Verification via QR (Mock)**

Guides the user through Huawei Cloud real-name verification (实名认证) with a Feishu-style QR flow: check account status → render a terminal QR pointing to a LAN H5 page → the user scans and confirms on their phone → poll every 3 seconds until approved / rejected / expired. Currently a **local mock**; the API shape follows the industry-standard create-session/poll pattern so the base URL can be swapped for a real endpoint later.

> **华为社区版** · 社区维护，非华为云官方；当前为本地 mock 演示，不产生真实华为云实名记录。

**Version:** 0.1.0 · Changelog: [qa/huawei-cloud-account-onboarding/CHANGELOG.md](../../qa/huawei-cloud-account-onboarding/CHANGELOG.md)

## What it does

| Capability | Behavior |
| --- | --- |
| Account status check | `GET /v1/customers/me/verification-status`; verified accounts short-circuit with "无需重复认证" |
| QR generation | `create-verification.js` renders a colored-frame, black/white-module QR in the terminal (phone must share the machine's WiFi) |
| Status polling | `poll-verification.js` polls every 3s: pending → scanned（提示手机完成）→ approved / rejected / expired; exit codes 0/2/3/4 |
| Expiry handling | QR TTL 180s (pending only; scanned never expires); on expiry the agent asks before regenerating |
| Out of scope | Real ID documents / credentials in chat; verifying on the user's behalf; non-Huawei-Cloud identity flows |

## Runtime bundle (install payload)

```text
skills/huawei-cloud-account-onboarding/
├── SKILL.md
├── references/
│   └── api-contract.md
└── scripts/
    ├── mock-server.js            # create/poll/account-status endpoints + H5 page
    ├── create-verification.js    # terminal QR client
    ├── poll-verification.js      # 3s polling client
    └── package.json              # dep: qrcode (npm install at first use)
```

No `evals/`, `qa/`, or `*-workspace/` under `skills/`; `node_modules/` is installed locally and never committed.

## In-skill flow

```text
User needs real-name verification
     │
     ▼
Step 0 · mock server up? (healthz, start if not)
     │
     ▼
Step 1 · account status ── verified ──> done, no QR
     │ unverified
     ▼
Step 2 · create session + terminal QR (TTL 180s)
     │
     ▼
Step 3 · poll every 3s ──> approved(0) | rejected(2) | expired(3, ask to regenerate)
```

## QA

```bash
./qa/huawei-cloud-account-onboarding/validate.sh
```

Gate = layout purity + version sync + script syntax & end-to-end smoke (create → scan → approve → poll → account flips verified) + skills-ref + markdownlint + skillcheck.
