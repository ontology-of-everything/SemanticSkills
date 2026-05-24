# Skill authoring

Conventions for skills in this monorepo. Spec baseline: [agentskills.io](https://agentskills.io/specification).

## Layout

| Path | Purpose |
| --- | --- |
| `skills/<name>/` | Installable runtime only (`SKILL.md` + optional `references/`, `scripts/`, `assets/`) |
| `qa/<name>/` | Validation, evals, assertions — never copied by `npx skills add` |
| `docs/skills/<name>.md` | Human-facing skill overview for the repo README index |

QA layout (gate files stay under `qa/`, not `skills/`):

```text
qa/<name>/
├── validate.sh
├── skillcheck.toml
├── .markdownlint.json
├── policy.skill-scanner.yaml   # optional
├── README.md
├── evals/evals.json
├── evals/llm-rubric.yml
├── assertions/README.md
├── fixtures/
└── bin/
    ├── gate.py                 # optional: gate.py style (skillcheck + markdownlint + skill-scanner)
    └── …
```

## Naming

- Folder name = `name` in `SKILL.md` frontmatter (kebab-case, lowercase)
- English paths only under `skills/` and `references/`
- Flat `references/*.md`; entity YAML under `references/semantic/` when needed

## SKILL.md frontmatter

Required: `name`, `description` (trigger keywords + scope).

Recommended for marketplace discovery ([SkillsMP](https://skillsmp.com/), [skills.sh](https://www.skills.sh/), [ClawHub](https://clawhub.ai/)):

```yaml
compatibility: <bins, IAM, network; note if agent must not auto-install>
metadata:
  openclaw:          # ClawHub security review only
    requires:
      bins: [<cli>]
    homepage: https://github.com/<org>/<repo>/tree/main/skills/<name>
    envVars:         # optional; required: false for profile-based auth
      - name: EXAMPLE_API_KEY
        required: false
        description: ...
```

- **`description`**: English + Chinese trigger phrases, task scope, and explicit refuse rules (payment/delete/refund).
- **License**: keep the repository license at the repo root. Do not put a
  conflicting `license` field in installable skill frontmatter when targeting
  ClawHub, because ClawHub-published skills are MIT-0.
- **SkillsMP**: public GitHub repo with `SKILL.md` frontmatter. Add GitHub
  topic `claude-skills` or `claude-code-skill` before the next crawler sync.
- **skills.sh**: same layout; promote `npx skills add <org>/SemanticSkills --skill <name> -y` in README; optional badge `https://skills.sh/b/<org>/SemanticSkills`.
- **ClawHub**: publish from `skills/<name>/` with `clawhub skill publish`.
  Declare `metadata.openclaw` so scans match runtime behavior.

Keep frontmatter concise; put long guidance in `references/`.

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
        ├── with_skill ──► <name>-workspace/iteration-N/eval-<id>/with_skill/
        └── baseline   ──► .../without_skill/
```

`<name>-workspace/` at repo root is gitignored; do not commit it.

Register the skill in `docs/catalog.yml` when adding a new package.
