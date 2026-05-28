# Hermes

Install skills from [SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills) into [Hermes Agent](https://github.com/NousResearch/Hermes) — **Huawei Community Edition**, community-maintained, not official Huawei Cloud. Same `SKILL.md` + `references/` bundle as `npx skills add`.

| Skill | Use when |
| --- | --- |
| `huawei-cloud-billing-scout` | Past spend — balance, bills, reconciliation, coupons |
| `huawei-cloud-cost-estimation` | Pre-order quotes — period & on-demand RFQ |

## From GitHub (registry)

```bash
hermes skills install ontology-of-everything/SemanticSkills/huawei-cloud-billing-scout -y
hermes skills install ontology-of-everything/SemanticSkills/huawei-cloud-cost-estimation -y
```

Uses the published tree on GitHub. To pick up **local edits** before push, sync the install bundle instead (below).

## Local development sync

Hermes does not install from a filesystem path reliably; copy the install payload:

```bash
rsync -a --delete \
  ./skills/huawei-cloud-billing-scout/ \
  ~/.hermes/skills/huawei-cloud-billing-scout/

rsync -a --delete \
  ./skills/huawei-cloud-cost-estimation/ \
  ~/.hermes/skills/huawei-cloud-cost-estimation/
```

Only `SKILL.md` and `references/` belong in each directory — not `qa/` or gate scripts.

## Credentials

Configure BSS credentials per Hermes / `hcloud` docs (`HUAWEICLOUD_SDK_AK`, `SK`, `REGION` in `~/.hermes` or profile). Skills do not auto-install `hcloud` or run writes.

## Verify in Hermes

```bash
hermes skills list | rg huawei
```

Optional repo gate before sync:

```bash
./tools/validate-all.sh
```

**Interaction discipline** (一次只问一事): [authoring.md § Interaction discipline](../authoring.md#interaction-discipline-all-skills).
