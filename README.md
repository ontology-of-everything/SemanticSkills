# SemanticSkills

> Community edition — not official Huawei Cloud.

Cloud agents get billing wrong in boring, repeatable ways: wrong grain, skipped reconciliation, answers with no table behind them. SemanticSkills packages [Agent Skills](https://agentskills.io/) where domain semantics live in versioned references—not in a fat `SKILL.md`—so the agent picks the right fact entity before it touches a CLI.

中文说明见 [README-CN.md](README-CN.md).

## Design

**Build ontology-first.** Each skill defines stable domain vocabulary in `references/semantic/*.yml` (fact entities, grain, dimensions, measures, source operations) and keeps command parameters in a separate layer. `SKILL.md` holds the execution protocol; the playbook covers multi-step flows and output shape.

At runtime a question flows like this:

```text
User question
     │
     ▼
Semantic layer ─► extract fact/dimensions/measures → source_operation(s)
     │
     ▼
Commands ───────► related-commands.md templates → execute (no --help first)
     │
     ▼
Playbook (if multi-step) ──► query order + output structure
     │
     ▼
Same YAML ───────► parse dimensions/measures → conclusion → evidence facts
```

| Layer | What it holds | Typical files |
| --- | --- | --- |
| Ontology | Fact definitions + response parsing | `references/semantic/*.yml` |
| Commands | API/CLI templates | `related-commands.md`, IAM, install notes |
| Playbook | Multi-step flows, user-readable output | `*-playbook.md` |
| Catalog / terms | Domain routing, semantic model and optional glossary | `semantic/catalog.yml`, `*-semantics.md` |

`skills/<name>/` is the installable runtime bundle; `qa/<name>/` holds evals and validation and is never copied by `npx skills add`. Listed on [skills.sh](https://www.skills.sh/), indexed by [SkillsMP](https://skillsmp.com/), and publishable to [ClawHub](https://clawhub.ai/).

Working example: [huawei-cloud-billing-scout](docs/skills/huawei-cloud-billing-scout.md). Authoring conventions: [docs/authoring.md](docs/authoring.md).

## Repository layout

```text
SemanticSkills/
├── skills/              # Installable runtime packages (SKILL.md + references/)
├── qa/                  # Per-skill validation (evals, assertions, validate.sh)
├── docs/                # Contributing, authoring, catalog, agent install guides
├── tools/               # validate-all.sh, skill-scaffold.sh
├── template/skill/      # New skill skeleton (not installable)
├── .workspaces/         # Skill Creator outputs (gitignored)
├── .agents/             # Local npx skills add copies (gitignored)
└── .credentials/        # Local credential samples (gitignored)
```

## Skills

| Skill | Path | Summary | Docs |
| --- | --- | --- | --- |
| `huawei-cloud-billing-scout` | `skills/huawei-cloud-billing-scout/` | Read-only Huawei Cloud billing scout via KooCLI/BSS | [details](docs/skills/huawei-cloud-billing-scout.md) |

Machine-readable index: [docs/catalog.yml](docs/catalog.yml).

## Install

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

From GitHub ([Cursor](docs/agents/cursor.md) example):

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

Claude Code or Codex:

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent claude-code \
  --copy -y

npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent codex \
  --copy -y
```

List skills in this repo before installing:

```bash
npx skills add ontology-of-everything/SemanticSkills --list
```

Local path:

```bash
npx skills add ./skills/huawei-cloud-billing-scout \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

## Validate

All skills:

```bash
./tools/validate-all.sh
```

Single skill:

```bash
./qa/huawei-cloud-billing-scout/validate.sh
```

Optional real BSS smoke test:

```bash
HUAWEICLOUD_BILLING_SCOUT_REAL=1 \
HUAWEICLOUD_BILLING_SCOUT_CYCLE=2025-04 \
./qa/huawei-cloud-billing-scout/validate.sh
```

## Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) and [docs/authoring.md](docs/authoring.md).

New skill:

```bash
./tools/skill-scaffold.sh <skill-name>
```

## Marketplaces

- [skills.sh](https://www.skills.sh/):
  public GitHub plus `npx skills add`; requires valid
  `skills/<name>/SKILL.md` and README install commands.
- [SkillsMP](https://skillsmp.com/):
  GitHub crawler and semantic search; requires `SKILL.md` frontmatter and the
  `claude-skills` or `claude-code-skill` GitHub topic.
- [ClawHub](https://clawhub.ai/):
  `clawhub skill publish <path>`; requires GitHub account age, semver version,
  text-only bundle, and accurate `metadata.openclaw`.
- Cursor:
  `npx skills add ... --agent cursor`; also discovers `.cursor/skills/` and
  `.agents/skills/`.
- Claude Code:
  `npx skills add ... --agent claude-code`; plugin packaging is optional here.
- Codex:
  `npx skills add ... --agent codex`; plugin packaging is optional for direct
  skill installs.

Each skill lives at `skills/<name>/SKILL.md` with `name`, a keyword-rich
`description`, concise `compatibility`, and registry metadata when needed.
ClawHub publishes skills under MIT-0 terms, so installable skill frontmatter must
not declare a conflicting license even though this repository remains
Apache-2.0. See
[docs/skills/huawei-cloud-billing-scout.md](docs/skills/huawei-cloud-billing-scout.md)
for the reference skill.
