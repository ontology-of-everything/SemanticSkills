# Changelog

Monorepo **infrastructure** history. Each skill has its own changelog:

| Skill | Changelog |
| --- | --- |
| huawei-cloud-billing-scout | [qa/huawei-cloud-billing-scout/CHANGELOG.md](qa/huawei-cloud-billing-scout/CHANGELOG.md) |
| huawei-cloud-cost-estimation | [qa/huawei-cloud-cost-estimation/CHANGELOG.md](qa/huawei-cloud-cost-estimation/CHANGELOG.md) |

## 3.0.3 - 2026-06-02

### Changed

- **huawei-cloud-billing-scout** **2.3.9**: BSS `--cli-region=cn-north-1` rule, eval #25, semantic DRY, A/B grading harness (see skill changelog)
- **huawei-cloud-cost-estimation** **1.0.2**: BSS cli-region rule and eval #11 (see skill changelog)

## 3.0.2 - 2026-05-29

### Changed

- **huawei-cloud-cost-estimation** **1.0.1**: BSS command/semantic alignment, `response_contract`, DRY layer split in `CLAUDE.md`, 10 eval cases with A/B grading harness (see skill changelog)

## 3.0.1 - 2026-05-28

### Changed

- **versioning**: per-skill `qa/<name>/VERSION`; billing-scout **2.3.8**, cost-estimation **1.0.0** (decoupled from repo tag v3.0.0 skill bumps)
- **changelog**: split skill histories into `qa/<name>/CHANGELOG.md` (+ `.zh.md`; repo index here)

### Documentation

- README: dual-skill design, install, validate, and version tables updated

## 3.0.0 - 2026-05-28

### Changed

- **CI**: validate workflow installs required Python/Node QA tools; skill-scanner mandatory
- **hooks**: `.githooks/pre-commit` → `validate-all.sh`; `tools/install-git-hooks.sh`

### Features

- **huawei-cloud-cost-estimation** skill and QA bundle added to the monorepo (see skill changelog for **1.0.0** scope)
