# 华为云成本估算与资源开通

`huawei-cloud-cost-estimation` · **Huawei Cloud Cost Estimation & Controlled Provisioning — Quote, Create, Unsubscribe via hcloud**

Deterministic pre-order quotes via hcloud BSS (period `ListRateOnPeriodDetail`, on-demand `ListOnDemandResourceRatings`, specs resolved live via `ListResourceSpecs`) plus a controlled lifecycle: 73 allowlisted create operations and unified unsubscribe (`BSS CancelResourcesSubscription`). Every write goes through runtime `--help`, read-only dependency lookups, a fee echo (or an extra unknown-fee confirmation), a mandatory local `--dryrun`, and explicit user confirmation before the real call.

> **华为社区版** · 社区维护，非华为云官方；结论以当次 hcloud 响应为准。

**Version:** 2.0.0 · Changelog: [qa/huawei-cloud-cost-estimation/CHANGELOG.md](../../qa/huawei-cloud-cost-estimation/CHANGELOG.md) · 中文仓库说明：[README-CN.md](../../README-CN.md)

## What it does

| Capability | Typical requests |
| --- | --- |
| Period / on-demand RFQ | 包年包月、按小时/按量多少钱；多产品分项加总 |
| Spec & dimension lookup | `ListResourceSpecs` 模糊实查规格；service/resource/measure 字典 |
| Controlled create | 开通/购买白名单内资源（ECS/RDS/CCE/EIP/WAF 等 73 个命令主体） |
| Unified unsubscribe | 退订包年/包月资源，仅 `BSS CancelResourcesSubscription`，独立高强度确认 |
| Out of scope | 历史账单/余额/对账 → 费用中心或只读账单 API；跨云；支付/续费/删除；对话中 AK/SK |

Independent from [huawei-cloud-billing-scout](huawei-cloud-billing-scout.md) (past spend)—install either or both; skills do not cross-route.

## Runtime bundle (install payload)

```text
skills/huawei-cloud-cost-estimation/
├── SKILL.md                     # route + pricing flow + lifecycle gates
└── references/
    ├── cli-installation.md
    ├── pricing/
    │   ├── commands.md          # RFQ command contracts, response paths, traps
    │   ├── iam-policies.md
    │   └── semantic/            # catalog + rfq-{period,ondemand,shared} models
    └── lifecycle/               # thin flow, no semantic layer
        ├── concepts.md          # help/lookup/--dryrun/fee-state/batch/cancel semantics
        └── commands.md          # 73 create ops + 1 cancel op, bodies only
```

No `evals/`, `qa/`, or `*-workspace/` under `skills/`.

## In-skill flow

```text
User request
     │
     ├─ Quote ──► pricing/semantic catalog → spec lookup → RFQ → verify → present
     │
     ├─ Create ─► allowlist → runtime --help → resolve deps (read-only)
     │            → cost echo (quote or unknown-fee extra confirm)
     │            → mandatory --dryrun → batch echo + explicit confirm
     │            → execute (remove --dryrun only) · fail-fast · no auto-rollback
     │
     └─ Cancel ─► BSS CancelResourcesSubscription only → help → --dryrun
                  → independent high-intensity confirm → execute
```

Parameters are never stored in the skill: each write op is explored with `hcloud <Service> <Operation> --help` at run time; if help fails (`[APIE_ERROR]`), the flow stops. Local `--dryrun` (prints the request, skips the call) is distinct from the server-side `dry_run` parameter a few APIs offer.

## Safety boundary

```text
Allowed: BSS RFQ/dictionary reads; read-only dependency lookups;
         73 allowlisted create ops + BSS CancelResourcesSubscription,
         each behind --dryrun + fee echo + explicit confirmation
Refused: chat AK/SK intake, payment, renewal, refund, delete,
         non-allowlisted writes, vague bulk unsubscribe, cross-cloud
Note:    estimate ≠ final bill; unsubscribe order id ≠ stopped/refunded
```

Automated evals only exercise the `--dryrun` stage; real provisioning tests are manual. Evidence snapshot: [docs/hcloud/evidence/normative-allowlist.md](../hcloud/evidence/normative-allowlist.md).

## QA (not installed with skill)

```text
qa/huawei-cloud-cost-estimation/
├── validate.sh                  # layout, version sync, write-allowlist gate, lint, skillcheck
├── fixtures/ops_contracts.yml   # 73 create + 1 cancel, single source
├── evals/evals.json             # 18 offline cases (13–18 lifecycle, dry-only)
├── assertions/README.md
└── bin/                         # grade_response.py, run_ab_eval.py, aggregate_ab.py
```

```bash
./qa/huawei-cloud-cost-estimation/validate.sh
```

## Install

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-cost-estimation \
  --agent cursor \
  --copy -y
```

**Hermes:** [hermes.md](../agents/hermes.md) · local sync:

```bash
rsync -a --delete ./skills/huawei-cloud-cost-estimation/ ~/.hermes/skills/huawei-cloud-cost-estimation/
```

Requires hcloud ≥7.2 and IAM permissions matching the requested read/write operations. Agent does not auto-install `hcloud`.
