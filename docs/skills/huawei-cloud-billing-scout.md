# huawei-cloud-billing-scout

Read-only **Huawei Cloud / 华为云** FinOps billing assistant via KooCLI/BSS: one-page, conclusion-first answers for cost, attribution, and reconciliation. Community edition, not official Huawei Cloud.

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

- `SKILL.md` is the single runtime entry: FinOps north star, Constitution, hard constraints, one-page workflow, IM-friendly output contract; CLI install detail in `cli-installation.md`.
- `references/README.md` is the lightweight navigation file for the reference bundle.
- `references/semantic/catalog.yml` routes by `required_context` (scope/time/money_basis) and `triggers` to ontology entities.
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
summary (conclusion first) ─── fact items ─── optional next step
```

## Ontology Coverage

`references/semantic/catalog.yml` plus `references/semantic/billing-ontology.yml` cover 58 unique read-only BSS query operations from KooCLI 7.2.2.

| Layer | What it owns | Examples |
| --- | --- | --- |
| `catalog.yml` | Process routing (`required_context` + `triggers`) | balance/debt, charge attribution, reconciliation, entitlements, account scope |
| `billing-ontology.yml` | Facts, dimensions, scope, money basis, evidence boundaries | `AccountBalance`, `BillingStatement`, `ResourceBillDetail`, `EnterpriseAndPartnerContext`, `PricingQuote` |
| `related-commands.md` | Operation contract | required parameters, verified dot-notation templates, safety limits |

## Safety Boundary

```text
Allowed: BSS List* / Show* query operations, plus product-side List/Show/Get only after BSS identifies a resource.
Refused: payment, renewal, refund execution, unsubscribe/cancel, create, update, delete, reclaim, transfer, send-code, or any balance/resource mutation.
```

## Output Contract

Final answers follow the skill **答复格式** in `SKILL.md` (briefing-style: conclusion-first summary with scope/cycle/basis, then concise fact bullets from queries only; uncertainty in summary; chat-safe formatting; redaction; one read-only follow-up). See `qa/huawei-cloud-billing-scout/evals/llm-rubric.yml` for eval grading dimensions.

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
  --version 2.3.2 \
  --changelog "Consolidate catalog.yml + billing-ontology.yml; compact fact output; 21 evals" \
  --clawscan-note "Read-only hcloud BSS List/Show queries; no writes" \
  --tags latest
```

## Validate

```bash
./qa/huawei-cloud-billing-scout/validate.sh
```

The QA gate checks install purity, YAML parseability, Catalog/ontology/command/contract consistency, verified KooCLI dot-notation templates, 58-operation coverage, eval schema, and safety wording. It does not run real BSS calls unless explicitly enabled by maintainers outside the default gate.
