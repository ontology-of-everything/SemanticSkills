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
┌─────────────┐     semantic/*.yml
│  Ontology   │──── fact/dimensions/measures → source_operation(s)
└──────┬──────┘
       ▼
┌─────────────┐     related-commands.md (+ iam, cli-installation)
│  Commands   │──── execute read-only hcloud BSS (no --help first)
└──────┬──────┘
       ▼
┌─────────────┐     billing-playbook.md (multi-step only)
│  Playbook   │──── query order + output structure
└──────┬──────┘
       ▼
 Same YAML → evidence table → summary → user-readable note
 (billing-semantics.md = semantic model + glossary; read-only; no conclusion before evidence)
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

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

```bash
npx skills add ontology-of-everything/SemanticSkills --list
```

## Marketplaces

| Platform | Listing |
| --- | --- |
| [skills.sh](https://www.skills.sh/ontology-of-everything/SemanticSkills/huawei-cloud-billing-scout) | Public GitHub + `npx skills add` installs |
| [SkillsMP](https://skillsmp.com/) | Auto-index from GitHub (`skills/*/SKILL.md`; repo needs ≥2 stars) |
| [ClawHub](https://clawhub.ai/) | `cd skills/huawei-cloud-billing-scout && clawhub publish` (MIT-0 on registry; GitHub stays Apache-2.0) |

Frontmatter includes `metadata.openclaw` (`requires.bins: hcloud`, optional `HUAWEICLOUD_SDK_*` env vars) for ClawHub security review.

## Validate

```bash
./qa/huawei-cloud-billing-scout/validate.sh
```
