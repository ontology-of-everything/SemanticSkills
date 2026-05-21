# Skill authoring

Conventions for skills in this monorepo. Spec baseline: [agentskills.io](https://agentskills.io/specification).

## Layout

| Path | Purpose |
| --- | --- |
| `skills/<name>/` | Installable runtime only (`SKILL.md` + optional `references/`, `scripts/`, `assets/`) |
| `qa/<name>/` | Validation, evals, assertions — never copied by `npx skills add` |
| `docs/skills/<name>.md` | Human-facing skill overview for the repo README index |

## Naming

- Folder name = `name` in `SKILL.md` frontmatter (kebab-case, lowercase)
- English paths only under `skills/` and `references/`
- Flat `references/*.md`; entity YAML under `references/semantic/` when needed

## SKILL.md frontmatter

Required: `name`, `description` (trigger keywords + scope).

Recommended for SkillsMP discovery:

```yaml
license: Apache-2.0
compatibility: <short environment requirement>
metadata:
  author: ontology-of-everything
  version: "1.0.0"
```

Keep frontmatter under ~100 tokens; put long guidance in `references/`.

## Install purity

Do **not** place inside `skills/<name>/`:

- `evals/`, `tests/`, `qa/`
- `.workspaces/`, `analysis/`
- repo-level scripts or credentials

## Validation

Per skill:

```bash
./qa/<name>/validate.sh
```

All skills:

```bash
./tools/validate-all.sh
```

New skill scaffold:

```bash
./tools/skill-scaffold.sh <skill-name>
```

## Skill Creator eval loop

```text
qa/<name>/evals/evals.json
        │
        ├── with_skill ──► .workspaces/<name>/iteration-N/<eval>/with_skill/
        └── baseline   ──► .../without_skill/
```

Register the skill in `docs/catalog.yml` when adding a new package.
