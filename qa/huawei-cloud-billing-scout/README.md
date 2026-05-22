# huawei-cloud-billing-scout QA

Per-skill quality gate. Run `validate.sh` locally and in CI.

## Layout

```text
qa/huawei-cloud-billing-scout/
├── validate.sh
├── README.md
├── evals/evals.json
├── assertions/README.md
├── fixtures/ops_contracts.yml
└── bin/
    ├── verify_ops.py          # cross-layer verifier
    ├── manual_verify_ops.sh   # --list / --print-command / --verify-help
    └── publish_clawhub.sh     # ClawHub publish (after clawhub login)
```

## Commands

```bash
./qa/huawei-cloud-billing-scout/validate.sh
./qa/huawei-cloud-billing-scout/bin/manual_verify_ops.sh --list
./qa/huawei-cloud-billing-scout/bin/manual_verify_ops.sh ListCosts
HUAWEICLOUD_BILLING_SCOUT_VERIFY_HELP=1 ./qa/huawei-cloud-billing-scout/validate.sh
```

## ClawHub publish

Prerequisites: [clawhub.ai](https://clawhub.ai/) account, GitHub linked (account ≥1 week), `npm i -g clawhub`.

```bash
clawhub login
# or headless: clawhub login --device

./qa/huawei-cloud-billing-scout/bin/publish_clawhub.sh 2.0.0 "Initial ClawHub release"
```

ClawHub registry applies **MIT-0** to published artifacts; this repo’s `SKILL.md` may keep **Apache-2.0** on GitHub.

## verify_ops.py

Functional pipeline: `verify()` → `Report(findings=...)` → `emit()`.

Pure checks live in `check_op()`; file/subprocess I/O only in `main()`.

Edit `fixtures/ops_contracts.yml` when semantic dimensions, CLI filters, or
KooCLI response roots change.
