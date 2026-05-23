# huawei-cloud-billing-scout

Read-only **Huawei Cloud / 华为云** billing scout via KooCLI/BSS. Community edition, not official Huawei Cloud.

中文摘要见 [README-CN.md](../../README-CN.md#技能).

## Capabilities

| Capability | Typical questions |
| --- | --- |
| Account facts | Balance, debt, stored-value cards, monthly spend, cash/credit/coupon ledgers |
| Charge attribution | Top spenders, resource-level charges, charges after delete, usage and amortized cost |
| Reconciliation | Console vs export, summary vs detail, order vs usage, billed vs paid vs amortized |
| Entitlements | Resource packages, coupon ledgers, partner coupon quotas, deduction gaps |
| Scope | Current account, enterprise/sub-account, partner/reseller and indirect partner views |
| Consulting | Pricing estimates, discount policies, billing-cycle interpretation, identity-review status |

## ClawHub-first layout

The runtime bundle now follows a ClawHub-first split:

- `SKILL.md` is the single runtime entry: when to use, core rules, the semantic-ontology workflow, and the output contract.
- `references/README.md` is the lightweight navigation file for the reference bundle.
- `references/semantic/catalog.yml` is a thin router from user questions to ontology entities.
- `references/semantic/billing-ontology.yml` is the single ontology file covering facts, scope, money basis, evidence boundaries, and 58 read-only query operations.
- `references/related-commands.md` is a thin command-contract appendix for maintainers and QA.

## In-skill flow

```text
User question
     │
     ▼
catalog.yml ─── route to ontology entities
     │
     ▼
billing-ontology.yml ─── pick fact, scope, money basis, evidence boundary
     │
     ▼
related-commands.md ─── execute the smallest read-only hcloud BSS query set
     │
     ▼
fact table ─── summary ─── optional next step
```

## Ontology Coverage

`references/semantic/catalog.yml` plus `references/semantic/billing-ontology.yml` cover 58 unique read-only BSS query operations from KooCLI 7.2.2.

| Layer | What it owns | Examples |
| --- | --- | --- |
| `catalog.yml` | Question routing | balance/debt, charge attribution, reconciliation, entitlements, account scope |
| `billing-ontology.yml` | Facts, dimensions, scope, money basis, evidence boundaries | `AccountBalance`, `BillingStatement`, `ResourceBillDetail`, `EnterpriseAndPartnerContext`, `PricingQuote` |
| `related-commands.md` | Operation contract | required parameters, verified dot-notation templates, safety limits |

## Safety Boundary

```text
Allowed: BSS List* / Show* query operations, plus product-side List/Show/Get only after BSS identifies a resource.
Refused: payment, renewal, refund execution, unsubscribe/cancel, create, update, delete, reclaim, transfer, send-code, or any balance/resource mutation.
```

## Output Contract

Final answers use a compact fact table (`事实项 | 结果 | 状态`; `proven` / `needs verification` only), a 1-2 sentence summary, and an optional smallest read-only next step when verification is still needed. Unproven but plausible explanations stay in the summary with qualifiers such as "more likely", never as table status. Raw command output, JSON, traces, profile/region details, and internal IDs stay out of the final answer; 0 or low amounts must not be used to infer free-tier coverage, no usage, no future charges, final billing, or all-service completeness unless the queried evidence directly proves that scope.

## Runtime bundle

```text
skills/huawei-cloud-billing-scout/
├── SKILL.md
└── references/
    ├── README.md
    ├── related-commands.md
    ├── iam-policies.md
    ├── cli-installation.md
    └── semantic/
        ├── catalog.yml
        └── billing-ontology.yml
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
  --version 1.0.3 \
  --changelog "Consolidate catalog.yml + billing-ontology.yml; compact fact output; 21 evals" \
  --clawscan-note "Read-only hcloud BSS List/Show queries; no writes" \
  --tags latest
```

## Validate

```bash
./qa/huawei-cloud-billing-scout/validate.sh
```

The QA gate checks install purity, YAML parseability, Catalog/ontology/command/contract consistency, verified KooCLI dot-notation templates, 58-operation coverage, eval schema, and safety wording. It does not run real BSS calls unless explicitly enabled by maintainers outside the default gate.
