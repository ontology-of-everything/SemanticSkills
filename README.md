# Ontology & Concept Design

[![GitHub release](https://img.shields.io/github/v/release/ontology-of-everything/SemanticSkills)](https://github.com/ontology-of-everything/SemanticSkills/releases/tag/v4.1.0)
[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

> Name the meaning first — then write code, run a CLI, or draft a spec.

[SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills) is a set of eleven [Agent Skills](https://agentskills.io/) for ontology, semantic layers, and concept design. Each skill keeps its protocol in a thin `SKILL.md` and loads bulky domain material from `references/` only when the task needs it. Huawei Cloud FinOps skills ship in the same repo.

The concept-design skills adapt Daniel Jackson's concepts-and-synchronizations model — [The Essence of Software](https://essenceofsoftware.com/) (2021), with the current when/where/then sync notation from *Beyond Objects* ([arXiv:2606.27258](https://arxiv.org/abs/2606.27258)) — for agent use; an adaptation, not endorsed by the author.

中文说明见 [README-CN.md](README-CN.md).

Current release **[v4.1.0](CHANGELOG.md#410---2026-09-09)** ([中文](CHANGELOG.zh.md#410---2026-09-09)). Install names in this release: `semantic-km-creator` (was `semantic-creator`); new `html-slides`.

## Table of Contents

- [Skills](#skills)
- [Install](#install)
- [Usage](#usage)
- [Contributing](#contributing)
- [Changelog](CHANGELOG.md)
- [License](#license)

## Skills

### Concept design

Requirements to modules, with the concept model as the contract. Each skill stops at its own boundary and hands off: `design` → `prd` / `implementation` → `audit`.

| Skill | Version | What it does |
| --- | --- | --- |
| [`concept-design`](docs/skills/concept-design.md) | 0.5.0 | Models requirements as concepts (purpose, operational principle, state, actions) composed by syncs, with a dependency graph and product subset. Produces the model; continues to PRD or code when requested |
| [`concept-prd`](docs/skills/concept-prd.md) | 0.4.0 | Transcribes a confirmed model into a central PRD plus one colocated `CONCEPT.md` per concept and a flow-grouped `SYNCS.md`. Gaps route back to design |
| [`concept-implementation`](docs/skills/concept-implementation.md) | 0.5.0 | Maps the model onto a modular monolith: one module per concept, syncs as mediators or a rule engine, specs colocated with code. Notes for Rust, Java/Spring Modulith, TypeScript |
| [`concept-audit`](docs/skills/concept-audit.md) | 0.4.0 | Read-only five-dimension audit of code against its model — drift, boundaries, criteria, composition, dependencies — with severity calibration and fix routing |
| [`concept-guardrails`](docs/skills/concept-guardrails.md) | 0.28.0 | Explicit-only skill for colocated `CONCEPT.md` / `PIPELINE.md` / `SYNCS.md` boundaries and spec–code drift. Six routes: audit, concept, drift, pipeline, sync, map |

### Ontology and semantics

Enterprise knowledge from APIs and databases (`semantic-km-creator`); personal knowledge from source text (`semantic-pkm-creator`).

| Skill | Version | What it does |
| --- | --- | --- |
| [`semantic-km-creator`](docs/skills/semantic-km-creator.md) | 0.6.0 | Enterprise knowledge: turns an API, CLI, or table/database into a grain-first Kimball semantic layer through an HTML decision workbench; emits OKF or YAML, every field traceable to observed evidence |
| [`semantic-pkm-creator`](docs/skills/semantic-pkm-creator.md) | 0.3.0 | Personal knowledge: extracts scenes, concepts, and entities from source text in two rounds — skeleton for human confirmation, then IPO, decomposition, assembly, and eight relation types |

### Presentation

| Skill | Version | What it does |
| --- | --- | --- |
| [`html-slides`](docs/skills/html-slides.md) | 0.1.0 | Explicit-only deck builder: outline → per-page table → plain single-file HTML deck in a pluggable style (generic, Huawei official light/dark, Apple); optional PPTX export |

### Huawei Cloud

Community-maintained, not official Huawei Cloud. Read-only by default; every figure is traceable to the KooCLI/BSS response of that run.

| Skill | Version | What it does |
| --- | --- | --- |
| [`huawei-cloud-billing-scout`](docs/skills/huawei-cloud-billing-scout.md) | 2.3.9 | Where money already went — balance, bills, attribution, reconciliation, coupons, stored-value cards, partner accounts. One-page briefing from 53 read-only BSS operations; refuses pay, renew, refund, delete |
| [`huawei-cloud-cost-estimation`](docs/skills/huawei-cloud-cost-estimation.md) | 3.2.4 | Period and on-demand quotes before you buy; allowlisted creates gated by `--dryrun`, fee review, and explicit confirmation. Unsubscribe is routed to the console, never executed |
| [`huawei-cloud-account-onboarding`](docs/skills/huawei-cloud-account-onboarding.md) | 1.0.0 | Read-only real-name (实名认证) status check, then renders the face-scan QR in the terminal and polls until verified. No ID, document, bank-card, or SMS intake |

Per-skill details and safety boundaries: [docs/skills/](docs/skills/). Machine-readable index: [docs/catalog.yml](docs/catalog.yml). Monorepo changelog: [CHANGELOG.md](CHANGELOG.md). Per-skill changelogs: `qa/<name>/CHANGELOG.md`.

## Install

Requires Node.js (for `npx`); the Huawei Cloud skills additionally need [KooCLI](https://support.huaweicloud.com/intl/en-us/productdesc-hcli/hcli_01.html) 7.2+, which the agent will not install for you.

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill <skill-name> \
  --agent cursor \
  --copy -y
```

`--agent` accepts `cursor`, `claude-code`, or `codex`. Several skills at once, and `--global` to install into `~/.agents/skills/` (scanned by both Cursor and Codex) instead of the project's `.agents/skills/`:

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill concept-design concept-prd concept-guardrails \
  --agent cursor codex \
  --global --copy -y
```

List what's available, or install from a local checkout while developing:

```bash
npx skills add ontology-of-everything/SemanticSkills --list
npx skills add ./skills/<skill-name> --skill <skill-name> --agent cursor --copy -y
```

Discovery: [skills.sh](https://skills.sh/ontology-of-everything/SemanticSkills) (groups in [`skills.sh.json`](skills.sh.json)) · [SkillsMP](https://skillsmp.com/) (GitHub topics `claude-skills`, `claude-code-skill`) · [ClawHub](https://clawhub.ai/).

[Hermes](docs/agents/hermes.md): `hermes skills install ontology-of-everything/SemanticSkills/<skill-name> -y`. Agent-specific notes: [Cursor](docs/agents/cursor.md) · [Claude Code](docs/agents/claude-code.md) · [Codex](docs/agents/codex.md).

Read a skill before using it — skills run with your agent's permissions.

## Usage

Skills normally activate from their description, so plain requests are enough. In Codex, `concept-guardrails` is explicit-only and must be named:

```text
把这个需求建成概念模型                      → concept-design
模型定了，出一份 PRD 规格                   → concept-prd
$concept-guardrails 给 src/orders 写概念规格，然后查漂移
把这套接口做成语义层                        → semantic-km-creator
3 月华为云为什么扣了这笔                     → huawei-cloud-billing-scout
```

To pin a skill explicitly: `/skill-name` in Cursor, `$skill-name` in Codex.

## Contributing

[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) · [docs/authoring.md](docs/authoring.md)

```bash
./tools/skill-scaffold.sh <skill-name>   # new skill
./tools/install-git-hooks.sh             # pre-commit → validate-all.sh
./tools/validate-all.sh                  # all skills, same as CI
./qa/<skill-name>/validate.sh            # one skill
```

`skills/<name>/` is the install payload; gates and evals live in `qa/<name>/` and are never installed. Sync on every skill change: `skills/`, `qa/` (`VERSION`, `CHANGELOG.md`), `docs/catalog.yml`, `docs/skills/<name>.md`.

## License

[Apache-2.0](LICENSE) © SemanticSkills contributors. Bundles published to [ClawHub](https://clawhub.ai/) are MIT-0 there; the repository source stays Apache-2.0.
