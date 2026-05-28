# huawei-cloud-cost-estimation Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 1.0.0 - 2026-05-28

First stable release (**Huawei Community Edition**).

### Features

- Pre-order BSS pricing — period (`ListRateOnPeriodDetail`) and on-demand (`ListOnDemandResourceRatings`)
- Workflow: Phase 1 (Parse, Clarify, Spec Review) → Phase 2 (Query, Calculate, Verify, Present)
- Semantic routing via `rfq-period-model.yml`, `rfq-ondemand-model.yml`, `rfq-shared-dimensions.yml`
- ECS/RDS/DCS/EVS/disk/bandwidth/EIP coverage; dimension and flavor lookup commands
- **Independent skill** — no cross-routing to billing-scout; historical billing → console / BSS bill read APIs

### qa

- `validate.sh` (layout, skills-ref, markdownlint, skillcheck)
- Seven offline evals in `evals/evals.json`

### Documentation

- `docs/skills/huawei-cloud-cost-estimation.md`; `docs/catalog.yml` index entry
- README install and skill table
