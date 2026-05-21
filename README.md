# SemanticSkills

> Community edition — not official Huawei Cloud.

Cloud agents get billing wrong in boring, repeatable ways: wrong grain, skipped reconciliation, answers with no table behind them. SemanticSkills packages [Agent Skills](https://agentskills.io/) where domain semantics live in versioned references—not in a fat `SKILL.md`—so the agent picks the right fact entity before it touches a CLI.

中文说明见 [README-CN.md](README-CN.md).

## Design

**Build ontology-first.** Each skill defines stable domain vocabulary in `references/semantic/*.yml` (entities, grain, dimensions, measures) and keeps command parameters in a separate layer. A playbook sits on top: it routes user intent into collaboration modes, query order, and output shape without duplicating the semantic model.

At runtime a question flows like this:

```text
User question
     │
     ▼
Playbook ───► capability → query basis → order → user-readable output
     │
     ▼
Semantics ──► pick fact entity (references/semantic/*.yml)
     │
     ▼
Commands ───► read-only operations (e.g. hcloud BSS)
     │
     ▼
Evidence table → summary → user-readable note → evidence boundary
```

| Layer | What it holds | Typical files |
| --- | --- | --- |
| Ontology | Fact entities the agent can cite | `references/semantic/*.yml`, `*-semantics.md` |
| Playbook | Collaboration modes, query basis, query order, user-readable output | `*-playbook.md` |
| Commands | API/CLI mapping only | `related-commands.md`, IAM, install notes |

`skills/<name>/` is the installable runtime bundle; `qa/<name>/` holds evals and validation and is never copied by `npx skills add`. Compatible with Claude Code, Cursor, Codex CLI, and [SkillsMP](https://skillsmp.com/).

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

From GitHub ([Cursor](docs/agents/cursor.md) example):

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy
```

Local path:

```bash
npx skills add ./skills/huawei-cloud-billing-scout \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy
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

## SkillsMP

Each skill lives at `skills/<name>/SKILL.md` with `name`, keyword-rich `description`, and optional `license` / `compatibility` / `metadata` for marketplace indexing.
