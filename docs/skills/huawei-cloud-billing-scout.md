# huawei-cloud-billing-scout

Read-only **Huawei Cloud / 华为云** FinOps billing assistant via KooCLI/BSS (**hcloud ≥7.2**). Delivers one-page, **briefing-style** answers: how much, why charged, what differs, what evidence is still missing. Community edition, not official Huawei Cloud.

**Version:** 2.3.2 · 中文仓库说明：[README-CN.md](../../README-CN.md)

## What it does

| Capability | Typical questions |
| --- | --- |
| Account facts | Balance, debt, stored-value cards, monthly spend, ledgers |
| Charge attribution | Top spenders, resource charges, charges after delete, usage and amortized cost |
| Reconciliation | Console vs export, summary vs detail, order vs usage |
| Entitlements | Resource packages, coupons, partner quotas, deduction gaps |
| Scope | Enterprise/sub-account, partner/reseller views |
| Consulting | Pricing estimates, billing-cycle interpretation (read-only) |

## Runtime bundle (install payload)

Only this tree is copied by `npx skills add` or Hermes local sync:

```text
skills/huawei-cloud-billing-scout/
├── SKILL.md                 # 工作准则 · 安全红线 · 查证路径 · 答复格式
└── references/
    ├── related-commands.md
    ├── cli-installation.md
    ├── iam-policies.md
    └── semantic/
        ├── catalog.yml
        └── billing-ontology.yml
```

No `evals/`, `qa/`, `skillgate.sh`, lint configs, or `*-workspace/` under `skills/`.

## In-skill flow

```text
User question
     │
     ▼
catalog.yml ─── triggers → ontology_entities
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

58 unique read-only BSS query operations (KooCLI 7.2.2), aligned across ontology, commands, and `qa/.../fixtures/ops_contracts.yml`.

## SKILL.md structure

| Section | Purpose |
| --- | --- |
| North star | One-page: 花、因、差；有据则证 |
| 工作准则 | Scope/口径、对账分列、不甩锅调查、只读相伴 |
| 安全红线 | 只读、不泄密、不越界推断、非官方 |
| 查证路径 | 定口径 → 选入口 → 取证 → 交付 |
| 答复格式 | Briefing delivery contract (see below) |

## 答复格式 (briefing-style output contract)

Answers follow **答复格式** in `SKILL.md` (conclusion-first summary, then fact bullets):

1. **Briefing summary** (1–3 sentences) — scope, billing period, money basis; spend / cause / delta / gaps.
2. **Fact bullets** — only **queried** facts; **易懂的事实称呼** (console-aligned; no API names in user text).
3. **Delivery floor** — no JSON walls, command logs, full business IDs, credentials, or `profile/region`; at most **one** read-only next step in plain language; never「请自行对账」.

**IM-safe:** single chat messages must **not** use GFM pipe tables (`|...|`). Use `·` or short paragraphs (Feishu, WeChat, and similar channels).

Grading: `qa/huawei-cloud-billing-scout/evals/llm-rubric.yml` (merged into all **21** eval cases).

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
    ├── skillgate.sh
    ├── run_protocol_eval.py
    ├── build_iteration1.py
    └── verify_ops.py
```

```bash
./qa/huawei-cloud-billing-scout/validate.sh
./qa/huawei-cloud-billing-scout/bin/skillgate.sh   # optional style-only
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
- [SkillsMP](https://skillsmp.com/) — topic `claude-skills` or `claude-code-skill`
- [ClawHub](https://clawhub.ai/) — publish from `skills/huawei-cloud-billing-scout/` after `./qa/.../validate.sh`

ClawHub publish (only after explicit release approval):

```bash
clawhub skill publish ./skills/huawei-cloud-billing-scout \
  --slug huawei-cloud-billing-scout \
  --name "Huawei Cloud Billing Scout" \
  --version 2.3.2 \
  --changelog "IM-safe briefing delivery; 答复格式; qa skillgate; 58 read-only BSS ops" \
  --clawscan-note "Read-only hcloud BSS List/Show; no writes" \
  --tags latest
```

ClawHub skill bundle is **MIT-0**; repository source remains **Apache-2.0**. Installable `SKILL.md` must not declare a conflicting `license` in frontmatter.
