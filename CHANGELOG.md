# Changelog

## 2.0.0 - 2026-05-22

First public release of [SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills) — community edition, not official Huawei Cloud.

### Features

- `huawei-cloud-billing-scout`: read-only Huawei Cloud billing investigation via KooCLI/BSS (facts, attribution, reconciliation, consulting)
- Ontology-first skill model: `references/semantic/*.yml` defines fact entities; `SKILL.md` holds execution protocol; commands and playbook stay in separate reference layers

### Refactor

- Standard monorepo layout: `skills/`, `qa/`, `docs/`, `tools/`, `template/`; install bundle excludes evals and QA
- Unified `billing-playbook.md` (replaces scattered scenario/workflow docs); user-readable, table-first, evidence-led output
- Semantic routing by fact / dimension / measure / time / scope — not FAQ matching; removed `common_questions` from entity YAML
- Purpose-led execution protocol with precondition checks; `related-commands.md` before `--help`
- Read-only guardrails: BSS `List*ChangeRecords` ledger APIs allowed; mutable ops refused
- Semantic field alignment: `CouponChangeRecord.trade_id`, `ResourceBillDetail` region/enterprise project, `resource_type_code` path fix

### Documentation

- README / README-CN: ontology runtime flow, `npx skills` install paths, skills.sh badge, marketplace table (skills.sh / SkillsMP / ClawHub)
- Enhanced `SKILL.md` frontmatter (`description`, `compatibility`, `metadata.openclaw`) for discovery and ClawHub security review
- Skill docs, authoring guide, catalog, assertions, and `CLAUDE.md` aligned with semantic-layer model and QA layout

### Tests

- Per-skill `validate.sh`; repo-wide `./tools/validate-all.sh` (CI)
- Evals, semantic routing checks, entity coverage, read-only policy guards
- Cross-layer verifier: `qa/.../fixtures/ops_contracts.yml` + `bin/verify_ops.py` (semantic ↔ commands ↔ optional `hcloud --help`)
- External gates: `skills-ref`, skillcheck, markdownlint, skill-scanner, install smoke test

### Maintenance

- Gitignore: `.agents/`, `.workspaces/`, `.credentials/`, `skills/*-workspace/`, gate reports
