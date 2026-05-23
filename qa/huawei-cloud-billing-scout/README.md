# huawei-cloud-billing-scout QA

Quality gate for the Huawei Cloud billing skill. Run it after changing `SKILL.md`,
`references/semantic/catalog.yml`, `references/semantic/billing-ontology.yml`,
`references/related-commands.md`, or the public docs.

## Commands

```bash
./qa/huawei-cloud-billing-scout/validate.sh
./tools/validate-all.sh
```

The default gate is offline and read-only. It parses YAML, checks install purity,
verifies the thin Catalog, single billing ontology, command appendix, and
`fixtures/ops_contracts.yml` stay aligned on the same 58 read-only query
operations, enforces verified dot-notation templates for complex KooCLI
parameters, validates eval schema, and blocks mutable BSS operation examples.

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
