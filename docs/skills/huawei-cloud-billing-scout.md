# 华为云 · 花多少为何扣 · 只读对账

`huawei-cloud-billing-scout` · **Huawei Cloud Read-Only Billing — Spend, Charges & Reconciliation**

Read-only **Huawei Cloud / 华为云** BSS FinOps via KooCLI (**hcloud ≥7.2**): balance, monthly spend, charge attribution, reconciliation, coupons, enterprise and partner billing. One-page briefing—how much, why charged, what differs, what evidence is still missing.

> **华为社区版** · 社区维护，非华为云官方；结论以当次 hcloud/BSS 响应为准。

**Version:** 2.3.9 · Changelog: [qa/huawei-cloud-billing-scout/CHANGELOG.md](../../qa/huawei-cloud-billing-scout/CHANGELOG.md) · Pre-order pricing: [huawei-cloud-cost-estimation.md](huawei-cloud-cost-estimation.md)

## What it does

| Capability | Typical questions |
| --- | --- |
| Account facts | Balance, debt, stored-value cards, monthly spend, ledgers |
| Charge attribution | Top spenders, resource charges, charges after delete, usage and amortized cost |
| Reconciliation | Console vs export, summary vs detail, order vs usage |
| Entitlements | Resource packages, coupons, partner quotas, deduction gaps |
| Scope | Enterprise/sub-account, partner/reseller views |
| Out of scope | Pricing quotes → use [huawei-cloud-cost-estimation](huawei-cloud-cost-estimation.md); real-name review; non-Huawei-Cloud billing |

## Runtime bundle (install payload)

Only this tree is copied by `npx skills add` or Hermes local sync:

```text
skills/huawei-cloud-billing-scout/
├── SKILL.md                 # 原则 · 分工 · 查证路径（四阶段表）· 红线 · 答复 · 边界
└── references/
    ├── related-commands.md
    ├── cli-installation.md
    ├── iam-policies.md
    └── semantic/
        ├── catalog.yml
        └── billing-ontology.yml
```

No `evals/`, `qa/`, `gate.py`, lint configs, or `*-workspace/` under `skills/`.

## In-skill flow

```text
User question
     │
     ▼
SKILL.md 华为云门禁 ─── confirm Huawei Cloud scope / profile when unclear
     │
     ▼
catalog.yml ─── triggers (华为云-prefixed) → ontology_entities
     │
     ▼
billing-ontology.yml ─── fact, scope, money_basis, evidence_boundary
     │
     ▼
related-commands.md ─── smallest read-only hcloud BSS query set
     │
     ▼
答复格式 ─── 小结 → 事实要点 → 一条只读下一步（如有）
```

53 unique read-only BSS query operations (KooCLI 7.2.2), aligned across ontology, commands, and `qa/.../fixtures/ops_contracts.yml`. Pricing-quote and real-name review operations were removed in 2.3.7 to retract the skill to a billing-only boundary; see `out_of_scope` in `catalog.yml`.

## SKILL.md structure

| Section | Purpose |
| --- | --- |
| 原则 | 北极星 + 三件套（scope/账期/口径）+ 单一事实不混 + 证据边界自洽 |
| 分工 | SKILL.md / catalog.yml / billing-ontology.yml / related-commands.md 四件套各司其职 |
| 查证路径 | 华为云门禁 + 四阶段表（定口径 → 选入口 → 取证 → 交付），含对账与企业/伙伴默认 |
| 红线 | 只读 / 不泄密 / 不外推，三条各附一句「为何」从原则派生 |
| 答复 | 答复格式 briefing delivery contract（见下） |
| 边界 | 服务范围（仅 BSS 只读账务）、拒绝路由（报价/实名/非华为云）、华为社区版声明、答复语言、环境就绪 |

## 答复格式 (briefing-style output contract)

Answers follow **答复格式** in `SKILL.md` (conclusion-first summary, then fact bullets):

1. **Briefing summary** (1–3 sentences) — scope, billing period, money basis; spend / cause / delta / gaps.
2. **Fact bullets** — only **queried** facts; **业务称呼** (console-aligned; no API names in user text).
3. **Delivery floor** — no JSON walls, command logs, full business IDs, credentials, or `profile/region`; at most **one** read-only next step in plain language; never「请自行对账」.

**IM-safe:** facts are rendered as `·` lists or short paragraphs, not Markdown tables — the delivery channel is often IM (Feishu, WeChat, etc.) where pipe characters do not render.

Grading: `qa/huawei-cloud-billing-scout/evals/llm-rubric.yml` (merged into all **24** eval cases; evals 22–24 exercise dialogue-progression discipline — "一次一问").

## Safety boundary

```text
Allowed: BSS List* / Show* queries; product List/Show/Get only after BSS identifies a resource.
Refused: pay, renew, refund, unsubscribe, create, update, delete, reclaim, transfer, or any mutation.
```

`ListCustomer*ChangeRecords` are **read** ledgers (`Change` ≠ write). No auto-install of `hcloud`. Real BSS only when maintainers set `HUAWEICLOUD_BILLING_SCOUT_REAL=1`.

## QA (not installed with skill)

```text
qa/huawei-cloud-billing-scout/
├── validate.sh
├── skillcheck.toml
├── .markdownlint.json
├── policy.skill-scanner.yaml
├── evals/evals.json
├── evals/llm-rubric.yml
├── fixtures/ops_contracts.yml
└── bin/
    ├── gate.py
    ├── verify_ops.py
    └── export_llm_eval.py
```

```bash
./qa/huawei-cloud-billing-scout/validate.sh
python3 qa/huawei-cloud-billing-scout/bin/gate.py style   # optional style-only
```

Default gate is offline. It does not call BSS unless `HUAWEICLOUD_BILLING_SCOUT_REAL=1` is set for maintainer smoke tests.

## Install

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

Agents: `cursor`, `claude-code`, `codex` — see [docs/agents/](../../docs/agents/). **Hermes:** [hermes.md](../agents/hermes.md).

Local development:

```bash
npx skills add ./skills/huawei-cloud-billing-scout \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

## Marketplaces

- [skills.sh](https://www.skills.sh/ontology-of-everything/SemanticSkills/huawei-cloud-billing-scout)
- [SkillsMP](https://skillsmp.com/) — repo topics `claude-skills`, `claude-code-skill`; verify with `curl "https://skillsmp.com/api/v1/skills/search?q=huawei-cloud-billing-scout"`
- [ClawHub](https://clawhub.ai/) — publish from `skills/huawei-cloud-billing-scout/` after `./qa/.../validate.sh`

ClawHub publish (only after explicit release approval):

```bash
# Use absolute path to the skill folder (relative ./skills/... may fail on some CLI versions)
clawhub skill publish "$PWD/skills/huawei-cloud-billing-scout" \
  --slug huawei-cloud-billing-scout \
  --name "Huawei Cloud Read-Only Billing — Spend, Charges & Reconciliation" \
  --version <semver> \
  --changelog "<semver>: ClawHub audit alignment — drop pricing-quote and real-name review (retract to billing-only boundary), Huawei Cloud-prefixed catalog triggers, provider_gate" \
  --clawscan-note "Huawei Cloud BSS List/Show read-only only. Billing scope only (balance/spend/attribution/reconciliation/coupons/cards/enterprise/partner); refuses pricing-quote, real-name review, and non-Huawei-Cloud billing; agent must not install hcloud; no writes" \
  --tags latest
```

ClawHub skill bundle is **MIT-0**; repository source remains **Apache-2.0**. Installable `SKILL.md` must not declare a conflicting `license` in frontmatter.
