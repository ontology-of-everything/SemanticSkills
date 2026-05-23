# huawei-cloud-billing-scout QA

Quality gate for the Huawei Cloud billing skill. Run it after changing `SKILL.md`,
`references/semantic/*.yml`, `references/related-commands.md`, `billing-playbook.md`,
or the public docs.

## Commands

```bash
./qa/huawei-cloud-billing-scout/validate.sh
./tools/validate-all.sh
```

The default gate is offline and read-only. It parses YAML, checks install purity,
verifies the 58-operation Catalog against semantic source operations, command docs
and `fixtures/ops_contracts.yml`, validates eval schema, and blocks mutable BSS
operation examples.

## Layout

```text
qa/huawei-cloud-billing-scout/
├── validate.sh
├── README.md
├── evals/evals.json
├── assertions/README.md
├── fixtures/ops_contracts.yml
└── bin/verify_ops.py
```

Do not store raw BSS responses, credentials, account IDs, resource IDs, order IDs,
or agent workspaces under `qa/`.
