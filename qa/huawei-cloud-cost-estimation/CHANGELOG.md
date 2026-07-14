# huawei-cloud-cost-estimation Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 3.1.0 - 2026-07-14

### Added

- Allowlisted `CloudIDE/CreateInstance` for standard CodeArts IDE Online environment provisioning; the third-party integration path remains excluded

### Changed

- Rewrote all 74 lifecycle command semantics with official product names, exact resource/action scope, API generations, legacy status, and billing boundaries
- Kept opening prerequisites and configuration actions compatible while explicitly marking them as non-independent billing operations
- Confirmed that ordinary CodeArts repository, build, pipeline, artifact, check, deploy, and project `Create*` operations remain outside the provisioning allowlist

## 3.0.0 - 2026-07-14

Breaking safety change: unsubscribe is now console-guidance-only. The skill no longer runs, previews, or emits unsubscribe CLI/API commands.

### Changed

- Route package subscriptions to Billing Center → Order Management → Cloud Service Unsubscription, with backup, exact-resource, linked-resource, refund/fee, and refund-destination checks
- Route on-demand cleanup to the relevant service console; deletion remains outside the skill
- Keep the 73-operation create allowlist and its `--dryrun`/fee/confirmation gates unchanged
- Replace the cancel confirmation eval with an insistence-resistant console-only eval; validation now rejects destructive lifecycle operations from the install payload

### Removed

- Executable `BSS/CancelResourcesSubscription` allowlist entry and dry-run/confirmation flow

## 2.0.0 - 2026-07-13

Major capability change: controlled resource lifecycle (create + unified unsubscribe) added on top of pricing. Safety boundary shifted from "refuse all writes" to "allowlisted writes behind --dryrun + explicit confirmation". Evidence: KooCLI 7.2.2 service-level help; see `docs/hcloud/evidence/normative-allowlist.md`.

### Added

- **references/lifecycle/** — thin-flow, no semantic layer: `concepts.md` (help/lookup/--dryrun/fee-state/batch/cancel semantics) + `commands.md` (73 canonical create ops + `BSS/CancelResourcesSubscription`, command bodies and dependency pointers only; parameters resolved via runtime `--help`)
- **SKILL.md Route/Lifecycle sections** — create flow: allowlist → help → resolve → cost (quote or unknown-fee extra confirm) → mandatory local `--dryrun` → batch echo + explicit confirm → fail-fast execute, no auto-rollback; cancel flow: independent high-intensity confirmation
- **qa/fixtures/ops_contracts.yml** — write allowlist single source (73 create + 1 cancel); `validate.sh` `check_write_allowlist` enforces fixture ↔ `lifecycle/commands.md` 1:1, BSS mutable = cancel only, forbidden BSS write prefixes, dry-only write evals
- **evals #13–18** — create fee-echo/dry/confirm, unknown-fee extra confirm, refuse skip-dry, batch fail-fast, cancel high-intensity, refuse non-allowlist writes; grader branches for each
- **docs/hcloud/evidence/normative-allowlist.md** — manual evidence snapshot (canonical list, `--dryrun` vs server-side `dry_run`, known help gaps)

### Changed

- **references/ reorganized by domain** — pricing files moved to `references/pricing/` (`commands.md`, `iam-policies.md`, `semantic/*`); `related-commands.md` renamed to `pricing/commands.md`
- **eval #4** re-scoped: still refuses chat AK/SK, but routes ordering intent to the controlled create flow instead of blanket refusal
- Original interface list normalized against live CLI: CDN/CSS/MRS/ELB expanded to version suffixes; Kafka → `CreatePostPaidKafkaInstance`; RocketMQ → `CreateInstanceByEngine`; `GaussDB CreateClickHouseInstance` dropped (absent in current CLI; StarRocks is not an equivalent)

## 1.1.0 - 2026-07-13

`resource_spec` resolution unified on the new `BSS/ListResourceSpecs` API ([qct_00008](https://support.huaweicloud.com/api-oce/qct_00008.html)); verified live against hcloud 7.2.2 (ECS code/name fuzzy search, bandwidth catalog).

### Added

- **related-commands.md**: `resource_spec_lookup` rewritten around `BSS/ListResourceSpecs` — full contract (required four params, `filters.[N].key=RESOURCE_SPEC` fuzzy search on spec code or name, `marker`+`limit` must be used together), query discipline (filter mandatory when any hint exists, `limit=100`, 3-page pagination circuit breaker, single 2s backoff on throttling, no retry loops), and a `resource_type`→`size_measure_id` pairing table for linear products
- **Universal Trap #4**: spec values in quote templates are format examples only; real values must come from the live `ListResourceSpecs` response
- **SKILL.md Critical Rule #7**: spec resolution is live-query only (same region, same charge_mode as the quote); no docs, no memory, no OS-suffix concatenation
- **eval #12** `spec-resolve-8c16g-via-listresourcespecs` + grader assertions (ListResourceSpecs before quoting, RESOURCE_SPEC filter, charge_mode alignment)

### Changed

- **rfq-shared-dimensions.yml**: five `Dim_ResourceSpec_*` snowflakes collapsed into one conformed `Dim_ResourceSpec` (source: `BSS/ListResourceSpecs`) with charge_mode/region alignment pairing rules; `flavor_id + os_suffix` transform removed (API returns the complete spec code)
- **iam-policies.md**: per-product ListFlavors permission layer replaced by BSS-dict-covered `ListResourceSpecs` (AZ lookup kept); error table adds 429 backoff, `CBC.0100`, `CBC.0151`
- **catalog.yml**: `BSS/ListResourceSpecs` added to primary_operations

### Removed

- Product ListFlavors path (ECS/RDS/DCS/EVS) and the hardcoded bandwidth/EIP/EVS constant tables — specs are always queried live; only the linear `size_measure_id` pairing survives in the command layer

## 1.0.2 - 2026-06-02

### Added

- **SKILL.md**: BSS 端点规则 — 所有 `hcloud BSS` 固定 `--cli-region=cn-north-1`；`product_infos.N.region` 仍为资源部署区
- **eval #11** `bss-cli-region-shanghai-period` + `grade_response.py` cli-region 断言；真实 hcloud A/B 验证

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
