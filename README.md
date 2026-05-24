# SemanticSkills

> Community edition — not official Huawei Cloud.

Cloud agents get billing wrong in repeatable ways: wrong grain, skipped reconciliation, answers with no evidence—or tables that break in Feishu and WeChat. SemanticSkills packages [Agent Skills](https://agentskills.io/) where domain semantics live in `references/`, not in a bloated `SKILL.md`, so the agent picks the right fact entity before it runs a CLI.

中文说明见 [README-CN.md](README-CN.md).

## Design

**Ontology-first.** Each skill defines facts, grain, dimensions, measures, and read-only operations in `references/semantic/*.yml`. Command templates stay in `related-commands.md`. `SKILL.md` holds safety rules, the query workflow, and how to deliver answers (for example briefing-style, IM-safe text—not pipe tables in chat).

```text
User question
     │
     ▼
catalog.yml ──────► route by scope / time / money_basis
     │
     ▼
billing-ontology.yml ► fact + evidence_boundary + source_operation(s)
     │
     ▼
related-commands.md ► minimal read-only CLI (no --help first)
     │
     ▼
答复 / delivery format ► conclusion first, fact bullets, one follow-up
```

| Layer | Role | Typical files |
| --- | --- | --- |
| Routing | Entry points and triggers | `references/semantic/catalog.yml` |
| Ontology | Facts, scope, money basis, evidence limits | `references/semantic/billing-ontology.yml` |
| Commands | Parameter templates, safety limits | `related-commands.md`, `cli-installation.md`, `iam-policies.md` |
| Protocol | North star, workflow, output contract | `SKILL.md` |

`skills/<name>/` is the **install payload** (`npx skills add` copies only this tree). `qa/<name>/` holds `validate.sh`, evals, and audit configs (`bin/gate.py`, `skillcheck.toml`, etc.)—never installed with the skill.

Example skill: [huawei-cloud-billing-scout](docs/skills/huawei-cloud-billing-scout.md) (**v2.3.2**). Authoring: [docs/authoring.md](docs/authoring.md).

## Repository layout

```text
SemanticSkills/
├── skills/<name>/       # SKILL.md + references/ (install bundle)
├── qa/<name>/           # validate.sh, evals/, bin/gate.py, lint configs
├── docs/                # catalog.yml, authoring, per-agent install notes
├── tools/               # validate-all.sh, skill-scaffold.sh
├── template/{skill,qa}/
├── *-workspace/         # Skill Creator eval output (gitignored)
├── .agents/             # Local npx skills add copies (gitignored)
└── .credentials/        # Local credential samples (gitignored)
```

## Skills

| Skill | Version | Summary | Docs |
| --- | --- | --- | --- |
| `huawei-cloud-billing-scout` | 2.3.2 | Read-only Huawei Cloud BSS FinOps via KooCLI; semantic routing; **IM-safe briefing** answers | [details](docs/skills/huawei-cloud-billing-scout.md) |

Index: [docs/catalog.yml](docs/catalog.yml).

## Install

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

**GitHub** ([Cursor](docs/agents/cursor.md), [Claude Code](docs/agents/claude-code.md), [Codex](docs/agents/codex.md)):

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

Replace `--agent cursor` with `claude-code` or `codex` as needed. List skills:

```bash
npx skills add ontology-of-everything/SemanticSkills --list
```

**Local path** (development):

```bash
npx skills add ./skills/huawei-cloud-billing-scout \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

**Hermes** ([Hermes agent](docs/agents/hermes.md)): `hermes skills install ontology-of-everything/SemanticSkills/huawei-cloud-billing-scout -y`, or rsync the local bundle into `~/.hermes/skills/`.

## Validate

All skills:

```bash
./tools/validate-all.sh
```

One skill (layout, contracts, evals, optional style gates):

```bash
./qa/huawei-cloud-billing-scout/validate.sh
```

Style-only audit (skillcheck + markdownlint + skill-scanner):

```bash
python3 qa/huawei-cloud-billing-scout/bin/gate.py style
```

Optional real BSS smoke test:

```bash
HUAWEICLOUD_BILLING_SCOUT_REAL=1 \
HUAWEICLOUD_BILLING_SCOUT_CYCLE=2025-04 \
./qa/huawei-cloud-billing-scout/validate.sh
```

Offline protocol benchmark (Skill Creator layout):

```bash
# viewer: huawei-cloud-billing-scout-workspace/iteration-1/benchmark-review.html
```

## Contributing

[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) · [docs/authoring.md](docs/authoring.md)

New skill:

```bash
./tools/skill-scaffold.sh <skill-name>
```

Sync on every skill change: `skills/`, `qa/`, `docs/catalog.yml`, `docs/skills/<name>.md`.

## Marketplaces

| Channel | Notes |
| --- | --- |
| [skills.sh](https://www.skills.sh/) | Public GitHub + `npx skills add` |
| [SkillsMP](https://skillsmp.com/) | `SKILL.md` frontmatter; topic `claude-skills` or `claude-code-skill` |
| [ClawHub](https://clawhub.ai/) | `clawhub skill publish`; `metadata.openclaw`; skill bundle is **MIT-0** on ClawHub (repo source Apache-2.0) |
| Cursor / Claude Code / Codex | `npx skills add ... --agent <agent>` |
| Hermes | `hermes skills install` or copy `skills/<name>/` — see [docs/agents/hermes.md](docs/agents/hermes.md) |

Reference publish flow: [docs/skills/huawei-cloud-billing-scout.md](docs/skills/huawei-cloud-billing-scout.md).
