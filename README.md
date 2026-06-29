# SemanticSkills

> **Huawei Community Edition** · community-maintained, not official Huawei Cloud.

Cloud agents get billing and pricing wrong in repeatable ways: wrong grain, guessed quotes, skipped reconciliation, answers with no evidence—or tables that break in Feishu and WeChat. **SemanticSkills (Huawei Community Edition)** packages [Agent Skills](https://agentskills.io/) where domain semantics live in `references/`, not in a bloated `SKILL.md`, so the agent picks the right fact entity before it runs a CLI.

中文说明见 [README-CN.md](README-CN.md). **Repo release:** v3.0.1 · see [CHANGELOG.md](CHANGELOG.md) (skill histories under `qa/<name>/CHANGELOG.md`).

## Design

**Ontology-first, skill-specific models.** Each skill defines facts, grain, dimensions, and read-only operations in `references/semantic/*.yml`. Command templates stay in `related-commands.md`. `SKILL.md` holds safety rules, the workflow, and how to deliver answers (briefing-style or quote lines—IM-safe text, not pipe tables in chat).

**Two skills today** (independent install bundles; do not cross-route):

| Skill | Concern | Primary ontology | Main BSS ops |
| --- | --- | --- | --- |
| [huawei-cloud-billing-scout](docs/skills/huawei-cloud-billing-scout.md) | **Past** spend — balance, bills, reconciliation, coupons | `billing-ontology.yml` | 53 read-only query ops |
| [huawei-cloud-cost-estimation](docs/skills/huawei-cloud-cost-estimation.md) | **Future** quotes — period & on-demand RFQ | `rfq-period-model.yml`, `rfq-ondemand-model.yml` | `ListRateOnPeriodDetail`, `ListOnDemandResourceRatings` |

Shared routing pattern:

```text
User question
     │
     ▼
catalog.yml ──────► route by pricing_mode or entry_point / triggers
     │
     ▼
semantic/*.yml ────► fact + evidence_boundary + dimensions
     │
     ▼
related-commands.md ► minimal read-only hcloud CLI (no --help first)
     │
     ▼
SKILL.md delivery ──► conclusion first · labeled basis · IM-safe bullets
```

| Layer | Role | Typical files |
| --- | --- | --- |
| Routing | Entry points and triggers | `references/semantic/catalog.yml` |
| Ontology | Facts, scope, evidence limits | `billing-ontology.yml` or `rfq-*-model.yml` + `rfq-shared-dimensions.yml` |
| Commands | Parameter templates, traps | `related-commands.md`, `cli-installation.md`, `iam-policies.md` |
| Protocol | Workflow, output contract | `SKILL.md` |

`skills/<name>/` is the **install payload** (`npx skills add` copies only this tree). `qa/<name>/` holds `validate.sh`, evals, and audit configs (`bin/gate.py` where present, `skillcheck.toml`, etc.)—never installed with the skill.

Authoring: [docs/authoring.md](docs/authoring.md). **Interaction discipline** (一次只问一事): [authoring § Interaction discipline](docs/authoring.md#interaction-discipline-all-skills).

## Repository layout

```text
SemanticSkills/
├── skills/<name>/       # SKILL.md + references/ (install bundle)
├── qa/<name>/           # validate.sh, evals/, bin/gate.py (optional), lint configs
├── docs/                # catalog.yml, authoring, per-agent install notes
├── tools/               # validate-all.sh, skill-scaffold.sh, install-git-hooks.sh
├── .githooks/           # pre-commit → validate-all.sh (set via install-git-hooks.sh)
├── template/{skill,qa}/
├── *-workspace/         # Skill Creator eval output (gitignored)
├── .agents/             # Local npx skills add copies (gitignored)
└── .credentials/        # Local credential samples (gitignored)
```

## Skills

| Skill | Version | Summary | Docs |
| --- | --- | --- | --- |
| `huawei-cloud-billing-scout` | 2.3.8 | **Huawei Cloud Read-Only Billing — Spend, Charges & Reconciliation** — one-page BSS briefing via KooCLI | [details](docs/skills/huawei-cloud-billing-scout.md) · [changelog](qa/huawei-cloud-billing-scout/CHANGELOG.md) |
| `huawei-cloud-cost-estimation` | 1.0.0 | **Huawei Cloud Pre-Order Cost Estimation** — period and on-demand quotes via hcloud BSS | [details](docs/skills/huawei-cloud-cost-estimation.md) · [changelog](qa/huawei-cloud-cost-estimation/CHANGELOG.md) |
| `semantic-layer-builder` | 0.1.0 | **Semantic Layer Builder** — meta-skill: interface → governed Kimball semantic layer + OKF export | [details](docs/skills/semantic-layer-builder.md) · [changelog](qa/semantic-layer-builder/CHANGELOG.md) |

Index: [docs/catalog.yml](docs/catalog.yml).

## Install

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

**GitHub** ([Cursor](docs/agents/cursor.md), [Claude Code](docs/agents/claude-code.md), [Codex](docs/agents/codex.md)):

```bash
# Billing (past spend / reconciliation)
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y

# Pre-order pricing (period / on-demand quotes)
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-cost-estimation \
  --agent cursor \
  --copy -y
```

Replace `--agent cursor` with `claude-code` or `codex` as needed. List skills:

```bash
npx skills add ontology-of-everything/SemanticSkills --list
```

**Local path** (development):

```bash
npx skills add ./skills/huawei-cloud-cost-estimation \
  --skill huawei-cloud-cost-estimation \
  --agent cursor \
  --copy -y
```

**Hermes** ([Hermes agent](docs/agents/hermes.md)): `hermes skills install ontology-of-everything/SemanticSkills/<skill-name> -y`, or rsync `./skills/<name>/` into `~/.hermes/skills/`.

## Validate

Install local pre-commit (runs `./tools/validate-all.sh` on every commit):

```bash
./tools/install-git-hooks.sh
```

All skills (same as CI):

```bash
./tools/validate-all.sh
```

Per skill:

```bash
./qa/huawei-cloud-billing-scout/validate.sh      # full gate: layout, ops, protocol eval, style
./qa/huawei-cloud-cost-estimation/validate.sh    # layout, skills-ref, markdownlint, skillcheck
```

Style-only audit (billing-scout):

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

Sync on every skill change: `skills/`, `qa/` (`VERSION`, `CHANGELOG.md`), `docs/catalog.yml`, `docs/skills/<name>.md`.

## Marketplaces

| Channel | Notes |
| --- | --- |
| [skills.sh](https://www.skills.sh/ontology-of-everything/SemanticSkills) | Listed; install via `npx skills add ontology-of-everything/SemanticSkills --skill <name>` |
| [SkillsMP](https://skillsmp.com/) | Repo topics `claude-skills`, `claude-code-skill`; `SKILL.md` frontmatter; crawler sync is periodic |
| [ClawHub](https://clawhub.ai/) | `clawhub skill publish`; `metadata.openclaw`; skill bundle is **MIT-0** on ClawHub (repo source Apache-2.0) |
| Cursor / Claude Code / Codex | `npx skills add ... --agent <agent>` |
| Hermes | `hermes skills install` or copy `skills/<name>/` — see [docs/agents/hermes.md](docs/agents/hermes.md) |

Reference publish flow: [docs/skills/huawei-cloud-billing-scout.md](docs/skills/huawei-cloud-billing-scout.md).
