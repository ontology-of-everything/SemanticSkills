# SemanticSkills

Community skills monorepo — not official Huawei Cloud.

## Do not get wrong

- **`skills/<name>/` = install payload only** (`npx skills add` copies this tree). Put gates, evals, and `skillcheck.toml` under **`qa/<name>/`** (`validate.sh` → `bin/gate.py full`); never inside `skills/`.
- **Skill Creator eval output:** `<name>-workspace/` at **repo root only** (gitignored). Never under `skills/` — `npx skills add` would ship it. Run evals from repo root so paths resolve to `./<name>-workspace/`.
- **Do not edit or commit:** `.agents/`, `*-workspace/`, `.workspaces/`, `.credentials/`, gate reports.
- **Done means** `./qa/<name>/validate.sh` (or `./tools/validate-all.sh`) passes — say so only after running it.
- **Skill change** syncs five places: `skills/`, `qa/` (`VERSION`, `CHANGELOG.md`), `docs/catalog.yml`, `docs/skills/<name>.md`. New skill: `./tools/skill-scaffold.sh <name>`.
- **Routing** is by fact / dimension / measure / time / scope — not FAQ lists. BSS operation change → update `references/semantic/*.yml`, `related-commands.md`, and `qa/.../fixtures/ops_contracts.yml` together.
- **Layer split (semantic vs command)** — `semantic/*.yml` = facts, dimension shape (keys / source ops / selection & pairing rules), routing; keep **thin**. `related-commands.md` = CLI contracts, concrete spec/code/measure values, enum tables, response field paths, command examples. Any value an agent **types into hcloud or reads from the response** lives ONLY in `related-commands.md`; semantic points to it, never re-lists (no `documented_examples` code catalogs, no enum value maps). Behavior defaults (OS=linux, AZ=空, fee_installment_mode=NA) live in `SKILL.md`.
- **No commit** unless asked. Never commit `.env*`, AK/SK, or credential files. Minimal diffs; no extra markdown unless asked.

## huawei-cloud-billing-scout

- **Read-only BSS** — refuse pay, renew, refund, delete, update, create. `ListCustomer*ChangeRecords` are read ledgers (`Change` ≠ write).
- No auto-install `hcloud`. Real BSS calls only when `HUAWEICLOUD_BILLING_SCOUT_REAL=1`.
