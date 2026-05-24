# SemanticSkills

Community Agent Skills monorepo — **not** official Huawei Cloud.

## Layout

| Path | Role |
| --- | --- |
| `skills/<name>/` | Install payload (`npx skills add` copies **only** this) |
| `qa/<name>/` | `validate.sh`, `evals/`, `assertions/`, `fixtures/`, `bin/` |
| `docs/catalog.yml`, `docs/skills/<name>.md` | Index + overview |
| `tools/` | `validate-all.sh`, `skill-scaffold.sh` |
| `template/{skill,qa}/` | Scaffolds — not installable |

**Never edit:** `.agents/`, `.workspaces/`, `skills/*-workspace/`, `qa/*-workspace/`, gate reports, `.credentials/`.

**`skills/` purity:** no `evals/`, `qa/`, `tests/`, credentials, or repo scripts inside `skills/`.

```text
skills/<name>/SKILL.md              # protocol; folder name = frontmatter `name` (kebab-case)
skills/<name>/references/
  related-commands.md               # CLI templates
  *-playbook.md | *-semantics.md    # steps/output | terms
  semantic/*.yml                    # grain, dimensions, measures, source_operation(s)

qa/<name>/validate.sh               # run before claiming done
```

Route by **fact / dimension / measure / time / scope** (not FAQ). Op change → sync `semantic/*.yml` + `related-commands.md` + `qa/.../fixtures/ops_contracts.yml`. Long text → `references/`, not SKILL frontmatter.

Skill change: sync `skills/`, `qa/`, `docs/catalog.yml`, `docs/skills/<name>.md`. New skill: `./tools/skill-scaffold.sh <name>`.

## huawei-cloud-billing-scout

Read-only BSS — refuse pay/renew/refund/delete/update/create. `ListCustomer*ChangeRecords` are **read** ledgers (`Change` ≠ write). No auto `hcloud`; real API only if `HUAWEICLOUD_BILLING_SCOUT_REAL=1`.

## Git & scope

No commit unless asked. No `.credentials/`, `.env*`, AK/SK. Minimal diffs; no extra markdown unless asked.
