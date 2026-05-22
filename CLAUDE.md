# SemanticSkills

Community Agent Skills monorepo — **not** official Huawei Cloud.

## Edit targets

- **Change** `skills/<name>/`, `qa/<name>/`, `docs/catalog.yml`, `docs/skills/<name>.md`
- **Never** edit `.agents/`, `.workspaces/`, `skills/*-workspace/`, gate reports — all generated/gitignored
- **Never** put `evals/`, `qa/`, `tests/`, credentials, or repo scripts inside `skills/` — `npx skills add` copies only `skills/`

## Routing (don't get this wrong)

- Route by **fact / dimension / measure / time / scope** — not FAQ, not `common_questions` (removed from semantic YAML)
- `SKILL.md` = protocol + hard rules | `semantic/*.yml` = grain/dimensions/measures/source_operation(s) only | `related-commands.md` = CLI templates (no `--help` first) | `*-playbook.md` = multi-step + output | `*-semantics.md` = terms only
- kebab-case folder = `name` in frontmatter; English paths under `references/`

## Done means validated

- Run `./qa/<name>/validate.sh` or `./tools/validate-all.sh` before claiming done
- Skill changes: sync `skills/`, `qa/`, `docs/catalog.yml` version, `docs/skills/<name>.md`
- New skill: `./tools/skill-scaffold.sh <name>` + catalog entry

## huawei-cloud-billing-scout

- **Read-only BSS.** Refuse pay/renew/refund/delete/update/create
- `ListCustomerAccountChangeRecords` / `ListCustomerCouponChangeRecords` **are allowed** (read-only ledger; `Change` in name ≠ write op)
- Operation change = **3 files**: `semantic/*.yml` + `related-commands.md` + `qa/.../fixtures/ops_contracts.yml`
- No auto `hcloud` install; no real BSS unless `HUAWEICLOUD_BILLING_SCOUT_REAL=1`

## Git

- **No commit** unless user asks
- **No** `.credentials/`, `.env*`, AK/SK, credential CSV/JSON

## Scope

- Minimal diffs; no extra markdown unless asked
- Long guidance → `references/`, not SKILL.md frontmatter
