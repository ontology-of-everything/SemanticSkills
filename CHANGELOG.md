## 1.0.5 - 2026-05-21

### Fixes
- Tighten `huawei-cloud-billing-scout` read-only guardrails so BSS `List*ChangeRecords` evidence queries are not mistaken for mutable operations
- Correct the `ResourceBillDetail` semantic path for `resource_type_code`

### Tests
- Add validation coverage for read-only ChangeRecords policy and stale resource detail field paths

## 1.0.4 - 2026-05-21

### Refactor
- Make `huawei-cloud-billing-scout` outputs user-readable by replacing fixed query-basis wording with plain-language notes, evidence boundaries, and hidden technical details by default

### Documentation
- Update README, skill docs, and QA assertions to describe user-readable billing output and evidence-boundary behavior

## 1.0.3 - 2026-05-21

### Refactor
- Replace `billing-scenarios` and `billing-scout-workflow` with unified `billing-playbook` organized by collaboration modes (facts, attribution, reconciliation, consulting)

### Documentation
- Update README, skill docs, and validation layout for playbook-first architecture

## 1.0.2 - 2026-05-21

### Documentation
- Add ontology-driven design section to README and README-CN: semantic layers, runtime flow, and `skills/` vs `qa/` split

## 1.0.1 - 2026-05-21

### Refactor
- Adopt standard monorepo layout (plan B): `qa/`, `docs/`, `tools/`, `template/`, and GitHub validate workflow

### Documentation
- Add community edition disclaimer to README, README-CN, and `huawei-cloud-billing-scout` SKILL.md (unofficial, not Huawei Cloud official)

## 1.0.0 - 2026-05-21

### Features
- Initial [SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills) release with `huawei-cloud-billing-scout`: read-only Huawei Cloud billing investigation via KooCLI/BSS (facts, attribution, reconciliation, consulting)

### Documentation
- README / README-CN for monorepo layout, SkillsMP discovery metadata, and GitHub install
- Agent Skills frontmatter aligned with agentskills.io and SkillsMP indexing

### Tests
- Validation pipeline: `skills-ref validate`, skillcheck, markdownlint, skill-scanner, and Cursor install smoke test
- `skillcheck.toml` for agentskills.io extension fields (`license`, `compatibility`, `metadata`)

### Maintenance
- Gitignore local-only paths: `dev/`, `.agents/`, `.workspaces/`, `.credentials/`
