# huawei-cloud-billing-scout

Read-only **Huawei Cloud / 华为云** billing scout via KooCLI/BSS. Community edition, not official Huawei Cloud.

中文摘要见 [README-CN.md](../../README-CN.md#技能).

## Capabilities

| Capability | Typical questions |
| --- | --- |
| Account facts | Balance, debt, stored-value cards, monthly spend, cash/credit/coupon ledgers |
| Attribution | Top spenders, resource-level charges, usage, amortized cost, why charges continue after delete |
| Reconciliation | Console vs export, summary vs detail, order vs usage, billed vs paid vs amortized |
| Entitlements | Resource packages, package usage records, coupon ledgers, partner coupon quotas |
| Scope | Current account, enterprise/sub-account, partner/reseller and indirect partner views |
| Consulting | Export rules, billing cycle, pricing estimates, discounts, identity-review status |

## In-skill flow

```text
User question
     │
     ▼
┌─────────────┐     semantic/Catalog.yml
│  Catalog    │──── domain → fact/dimensions/measures → source_operation(s)
└──────┬──────┘
       ▼
┌─────────────┐     semantic/*.yml
│  Facts      │──── grain, dimensions, measures, evidence boundary
└──────┬──────┘
       ▼
┌─────────────┐     related-commands.md (+ iam, cli-installation)
│  Commands   │──── execute read-only hcloud BSS (no --help first)
└──────┬──────┘
       ▼
 billing-playbook.md → evidence table → short conclusion → caveats
```

## Semantic Coverage

`references/semantic/Catalog.yml` routes user intent across 8 domains and 58 unique read-only BSS query operations from KooCLI 7.2.2.

| Domain | Fact files / entities | Representative operations |
| --- | --- | --- |
| `customer_billing` | `AccountBalance`, `StoredValueCard`, `MonthlyBillSummary`, `BillingStatement`, `ResourceBillRecord`, `ResourceBillDetail`, `AccountChangeRecord` | `ShowCustomerAccountBalances`, `ListCustomerBillsFeeRecords`, `ListStoredValueCards` |
| `cost_and_usage` | `CostAnalysis`, `AmortizedCost`, `ResourceUsage` | `ListCosts`, `ListCustomerBillsMonthlyBreakDown`, `ListResourceUsageSummary`, `ListResourceUsage` |
| `discount_entitlement` | `FreeResourcePackage`, `CouponChangeRecord`, `CouponQuota` | `ListFreeResourceInfos`, `ListFreeResourceUsages`, `ListQuotaCoupons`, `ListIssuedPartnerCoupons` |
| `order_evidence` | `OrderEvidence` | `ListCustomerOrders`, `ShowCustomerOrderDetails`, `ShowRefundOrderDetails` |
| `enterprise_multi_account` | `EnterpriseAccountContext`, `EnterpriseBilling` | `ListEnterpriseSubCustomers`, `ListConsumeSubCustomers`, `ListSubCustomerBillDetail` |
| `partner_resale` | `PartnerAccountContext`, `PartnerBilling` | `ListSubCustomers`, `ListCustomersBalancesDetail`, `ListPartnerAdjustRecords` |
| `reference_dimensions` | `ReferenceDimensions` | `ListServiceTypes`, `ListResourceTypes`, `ListUsageTypes`, `ListConversions` |
| `quote_and_identity` | `PricingQuote`, `IdentityReview` | `ListOnDemandResourceRatings`, `ListRenewRateOnPeriod`, `ShowRealnameAuthenticationReviewResult` |

## Safety Boundary

```text
Allowed: BSS List* / Show* query operations, plus product-side List/Show/Get only after BSS identifies a resource.
Refused: payment, renewal, refund execution, unsubscribe/cancel, create, update, delete, reclaim, transfer, send-code, or any balance/resource mutation.
```

## Runtime bundle

```text
skills/huawei-cloud-billing-scout/
├── SKILL.md
└── references/
    ├── billing-playbook.md
    ├── related-commands.md
    ├── iam-policies.md
    ├── cli-installation.md
    └── semantic/
        ├── Catalog.yml
        └── *.yml
```

No `evals/`, `scripts/`, `analysis/`, or workspaces inside the skill directory.

## Install

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

Cursor:

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

Claude Code:

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent claude-code \
  --copy -y
```

Codex:

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent codex \
  --copy -y
```

```bash
npx skills add ontology-of-everything/SemanticSkills --list
```

## Marketplaces

- [skills.sh](https://www.skills.sh/ontology-of-everything/SemanticSkills/huawei-cloud-billing-scout):
  public GitHub repo plus `npx skills add`.
- [SkillsMP](https://skillsmp.com/):
  auto-indexes public GitHub skills with `SKILL.md` frontmatter. Add the
  `claude-skills` or `claude-code-skill` GitHub topic before the next sync.
- [ClawHub](https://clawhub.ai/):
  publish from the skill directory after local validation. ClawHub publishes
  skills under MIT-0 terms; this repo's source license remains Apache-2.0.

ClawHub publish command (run only after explicit release approval):

```bash
clawhub skill publish ./skills/huawei-cloud-billing-scout \
  --slug huawei-cloud-billing-scout \
  --name "Huawei Cloud Billing Scout" \
  --version 2.1.0 \
  --changelog "58-operation Huawei Cloud BSS semantic coverage" \
  --clawscan-note "Read-only hcloud BSS List/Show queries; no writes" \
  --tags latest
```

## Validate

```bash
./qa/huawei-cloud-billing-scout/validate.sh
```

The QA gate checks install purity, YAML parseability, Catalog/semantic/command/contract consistency, 58-operation coverage, eval schema and safety wording. It does not run real BSS calls unless explicitly enabled by maintainers outside the default gate.
