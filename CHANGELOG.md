# Changelog

## 2.1.0 - 2026-05-23

### Features

- `huawei-cloud-billing-scout`: expand Huawei Cloud BSS semantic coverage to
  58 read-only query operations across customer billing, cost and usage,
  discount entitlement, order evidence, enterprise, partner, reference
  dimensions, pricing, and identity review domains
- Add `StoredValueCard` and other new semantic fact files so routing covers
  stored-value cards, amortized cost, usage, billing statements, order evidence,
  enterprise/partner context, pricing quotes, and reference dimensions

### Documentation

- Refresh README, skill docs, authoring guidance, catalog metadata, and agent
  install docs for skills.sh, SkillsMP, ClawHub, Cursor, Claude Code, Codex, and
  Hermes Agent direct skill installs
- Document ClawHub MIT-0 publishing behavior while keeping the repository source
  license under Apache-2.0

### Tests

- Rebuild `qa/huawei-cloud-billing-scout` around the 58-operation contract,
  semantic/doc consistency checks, eval schema validation, marketplace readiness
  checks, and mutable BSS operation guards
- Replace stale iteration helper scripts with the current offline verifier and
  17 objective eval cases covering all semantic domains

## 2.0.1 - 2026-05-22

### Documentation

- `huawei-cloud-billing-scout`: refactor `SKILL.md` with eval-aligned acceptance criteria and a six-step protocol; ~10% shorter body
- Replace FAQ / classic-question wording with semantic routing and fixed-question-template language across playbook, semantics, and QA assertions

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
