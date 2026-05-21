# huawei-cloud-billing-scout

Read-only **Huawei Cloud / 华为云** billing scout via KooCLI/BSS.

中文摘要见 [README-CN.md](../../README-CN.md#技能).

## Capabilities

| Capability | Typical questions |
| --- | --- |
| Facts | Balance, monthly spend, sub-account or enterprise-project totals |
| Attribution | Where money goes, top spenders, why charges continue after delete |
| Reconciliation | Console vs export, summary vs detail, order vs usage |
| Consulting | Export rules, billing cycle, coupons, packages, allocation |

## In-skill flow

```text
User question
     │
     ▼
┌─────────────┐     billing-playbook.md
│  Playbook   │──── capability → query basis → order → user-readable output
└──────┬──────┘
       ▼
┌─────────────┐     billing-semantics.md + semantic/*.yml
│  Semantics  │──── pick fact entity (grain, dims, measures)
└──────┬──────┘
       ▼
┌─────────────┐     related-commands.md (+ iam, cli-installation)
│  Commands   │──── read-only hcloud BSS operations
└──────┬──────┘
       ▼
 Table → summary → user-readable note → evidence boundary
 (read-only only; no conclusion before evidence)
```

## Semantic entities (8)

```text
AccountBalance ── ShowCustomerAccountBalances
MonthlyBillSummary ── ShowCustomerMonthlySum
ResourceBillRecord ── ListCustomerselfResourceRecords
ResourceBillDetail ── ListCustomerselfResourceRecordDetails
FreeResourcePackage ── ListFreeResourceInfos (+ usage APIs)
AccountChangeRecord ── ListCustomerAccountChangeRecords
CouponChangeRecord ── ListCustomerCouponChangeRecords
CostAnalysis ── ListCosts
```

## Runtime bundle

```text
skills/huawei-cloud-billing-scout/
├── SKILL.md
└── references/
    ├── billing-playbook.md
    ├── billing-semantics.md
    ├── related-commands.md
    ├── iam-policies.md
    ├── cli-installation.md
    └── semantic/*.yml
```

No `evals/`, `scripts/`, `analysis/`, or workspaces inside the skill directory.

## Install

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy
```

## Validate

```bash
./qa/huawei-cloud-billing-scout/validate.sh
```
