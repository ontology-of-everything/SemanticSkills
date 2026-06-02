# 华为云成本估算

`huawei-cloud-cost-estimation` · **Huawei Cloud Pre-Order Cost Estimation — Period & On-Demand via hcloud (Read-Only)**

Deterministic **pre-order** quotes via hcloud BSS: period (`ListRateOnPeriodDetail`) and on-demand (`ListOnDemandResourceRatings`). Prices come only from the live hcloud response—never guessed. Clarify before quoting when the four-tuple (service / resource / region / spec) or duration/usage is incomplete.

> **华为社区版** · 社区维护，非华为云官方；结论以当次 hcloud/BSS 响应为准。

**Version:** 1.0.2 · Changelog: [qa/huawei-cloud-cost-estimation/CHANGELOG.md](../../qa/huawei-cloud-cost-estimation/CHANGELOG.md) · 中文仓库说明：[README-CN.md](../../README-CN.md)

## What it does

| Capability | Typical questions |
| --- | --- |
| Period RFQ | 包年/包月 ECS、RDS、EVS、带宽等多少钱 |
| On-demand RFQ | 按小时/按量跑 N 小时/GB 多少钱 |
| Multi-product | 一套环境（多台 ECS + 盘 + 带宽）分项加总 |
| Dimension lookup | 查 `cloud_service_type` / flavor / measure unit |
| Out of scope | 历史账单、余额、对账 → 费用中心或 BSS 账单只读 API；跨云；下单/支付；对话中 AK/SK |

Independent from [huawei-cloud-billing-scout](huawei-cloud-billing-scout.md) (past spend)—install either or both; skills do not cross-route.

## Runtime bundle (install payload)

```text
skills/huawei-cloud-cost-estimation/
├── SKILL.md
└── references/
    ├── related-commands.md
    ├── cli-installation.md
    ├── iam-policies.md
    └── semantic/
        ├── catalog.yml
        ├── rfq-period-model.yml
        ├── rfq-ondemand-model.yml
        └── rfq-shared-dimensions.yml
```

No `evals/`, `qa/`, or `*-workspace/` under `skills/`.

## In-skill flow

```text
User question
     │
     ▼
Phase 1 · Parse ─── catalog.yml → rfq-period | rfq-ondemand model
     │
     ▼
Phase 1 · Clarify ─ one round with 2–4 candidates when ambiguous
     │
     ▼
Phase 1 · Spec Review ─ confirmed / missing / defaults table
     │
     ▼
Phase 2 · Query ─── related-commands.md minimal hcloud command
     │
     ▼
Phase 2 · Calculate / Verify / Present ─ line items + basis labels + total
```

Primary operations: `BSS/ListRateOnPeriodDetail`, `BSS/ListOnDemandResourceRatings`, plus dimension/flavor lookups documented in `related-commands.md`.

## SKILL.md structure

| Section | Purpose |
| --- | --- |
| Workflow | Phase 1 Analysis (Parse, Clarify, Spec Review) → Phase 2 Estimation |
| Critical Rules | Never guess; never-assume vs safe-default; label basis; no credentials in chat; route out-of-scope |
| Reference Index | When to load each semantic / command file |

## Safety boundary

```text
Allowed: BSS RFQ read APIs; IAM project scope; dimension/flavor List* helpers in related-commands.md
Refused: order placement, payment, credential intake in chat, cross-cloud quotes
Note: estimate ≠ final bill; discounts are account-view only
```

IM-safe delivery: use `·` bullets or numbered lines—no GFM pipe tables in user-facing chat.

## QA (not installed with skill)

```text
qa/huawei-cloud-cost-estimation/
├── validate.sh
├── evals/evals.json          # 7 offline eval cases
├── assertions/README.md
└── .markdownlint.json
```

```bash
./qa/huawei-cloud-cost-estimation/validate.sh
```

## Install

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-cost-estimation \
  --agent cursor \
  --copy -y
```

**Hermes:** [hermes.md](../agents/hermes.md) · local sync:

```bash
rsync -a --delete ./skills/huawei-cloud-cost-estimation/ ~/.hermes/skills/huawei-cloud-cost-estimation/
```

Requires hcloud ≥7.2 and BSS IAM with `bss:order:view`. Agent does not auto-install `hcloud`.
