# huawei-cloud-account-onboarding Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 0.1.0 - 2026-07-04

First release (**Huawei Community Edition**, local mock).

### Features

- Real-name verification (实名认证) QR flow modeled on industry three-part shape
  (create session → poll status → terminal state; Feishu QR login / Alipay certify / Stripe Identity)
- `scripts/mock-server.js` — zero-dep mock: `POST /v1/verifications`,
  `GET /v1/verifications/{id}`, `GET /v1/customers/me/verification-status`,
  H5 approve/reject page on LAN IP; TTL 180s (env-overridable), scanned sessions never expire
- `scripts/create-verification.js` — terminal QR (colored frame, black/white modules via `qrcode`),
  machine-readable `VERIFICATION_ID=` output, idempotent on already-verified accounts
- `scripts/poll-verification.js` — 3s polling with status transitions
  (pending → scanned → approved/rejected/expired), exit codes 0/2/3/4
- SKILL.md workflow: check account status → generate QR → poll → converge;
  expired QR prompts user before regenerating; refuses real ID/credential intake
- QA gate: layout + version sync + script syntax/e2e smoke + skills-ref + markdownlint + skillcheck
