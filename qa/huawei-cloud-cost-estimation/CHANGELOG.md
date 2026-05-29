# huawei-cloud-cost-estimation Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 1.0.1 - 2026-05-29

Semantic/command consistency pass against official BSS docs and hcloud 7.2.2 `--help`/`--dryrun`.

### Fixed

- Period ECS example mislabeled 包年 while using `period_type=2` (month) → corrected to `period_type=3` (year)
- `ListUsageTypes` pagination corrected: it accepts `--limit/--offset` (was marked no-pagination)
- On-demand `usage_measure_id`: removed misleading `max: 4` (it is field length, not an enum cap)

### Changed

- Added `response_contract` section to `related-commands.md` (official price vs discounted amount, exact field paths for both APIs)
- ECS OS default unified as safe-default `.linux` (disclosed in Spec Review) across SKILL.md and `rfq-shared-dimensions.yml`
- `iam-policies.md`: added `ListOnDemandResourceRatings`; fixed stale `rfq-operations.yml` / `quote_gate` references
- Documented GPSSD2 disk spec constants (`GPSSD2.storage/.iops/.throughput`)
- SKILL.md: defined confirm phrasing and response-reading pointer
- Universal Trap used wrong param `region_id` → `region` (matches API/CLI/examples)
- Eval suite expanded to 10 cases with programmatic `expectations`; A/B harness (`bin/grade_response.py`, `bin/run_ab_eval.py`, `bin/aggregate_ab.py`)
- DRY/layer split: moved concrete spec/code/measure/enum values out of `semantic/*.yml` (dropped `documented_examples` catalogs and enum maps that duplicated and drifted from `related-commands.md`); semantic now references the command layer as single source. OS-default policy consolidated to SKILL.md. Codified the rule in repo `CLAUDE.md`.

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
- Ten offline evals in `evals/evals.json` (with programmatic expectations)

### Documentation

- `docs/skills/huawei-cloud-cost-estimation.md`; `docs/catalog.yml` index entry
- README install and skill table
