# Hermes

Install **huawei-cloud-billing-scout** (or any skill from this repo) into [Hermes Agent](https://github.com/NousResearch/Hermes) — community skills, same `SKILL.md` + `references/` bundle as `npx skills add`.

## From GitHub (registry)

```bash
hermes skills install ontology-of-everything/SemanticSkills/huawei-cloud-billing-scout -y
```

Uses the published tree on GitHub. To pick up **local edits** before push, sync the install bundle instead (below).

## Local development sync

Hermes does not install from a filesystem path reliably; copy the install payload:

```bash
rsync -a --delete \
  ./skills/huawei-cloud-billing-scout/ \
  ~/.hermes/skills/huawei-cloud-billing-scout/
```

Only `SKILL.md` and `references/` belong in that directory — not `qa/` or gate scripts.

## Credentials

Configure BSS read-only credentials per Hermes / `hcloud` docs (`HUAWEICLOUD_SDK_AK`, `SK`, `REGION` in `~/.hermes` or profile). The skill does not auto-install `hcloud` or run writes.

## Verify in Hermes

```bash
hermes skills list | rg huawei
```

Optional repo gate before sync:

```bash
./qa/huawei-cloud-billing-scout/validate.sh
```

**Interaction discipline** (一次只问一事): [authoring.md § Interaction discipline](../authoring.md#interaction-discipline-all-skills).
