# huawei-cloud-billing-scout QA

Quality gate for the Huawei Cloud billing skill. Run it after changing `SKILL.md`,
`references/semantic/catalog.yml`, `references/semantic/billing-ontology.yml`,
`references/related-commands.md`, or the public docs.

## Commands

```bash
./qa/huawei-cloud-billing-scout/validate.sh
./tools/validate-all.sh

# Skill-creator iteration-1 (offline with_skill vs naive baseline, benchmark + HTML viewer):
python3 qa/huawei-cloud-billing-scout/bin/build_iteration1.py
# Open: huawei-cloud-billing-scout-workspace/iteration-1/benchmark-review.html
# Timing in benchmark is local golden-answer generation only (see benchmark-mode.json), not live agent latency.
```

The default gate is offline and read-only. It parses YAML, checks install purity,
verifies the thin Catalog, single billing ontology, command appendix, and
`fixtures/ops_contracts.yml` stay aligned on the same 58 read-only query
operations, enforces verified dot-notation templates for complex KooCLI
parameters, validates eval schema (including `llm-rubric.yml`), runs
markdownlint-cli2 and skillcheck when installed, exports 21 LLM eval cases, runs
protocol eval (`bin/run_protocol_eval.py`) against merged global + per-case
assertions, and blocks mutable BSS operation examples.

## Layout

```text
qa/huawei-cloud-billing-scout/
├── validate.sh
├── README.md
├── evals/evals.json
├── evals/llm-rubric.yml
├── bin/export_llm_eval.py
├── bin/run_protocol_eval.py
├── assertions/README.md
├── fixtures/ops_contracts.yml
└── bin/verify_ops.py
```

Do not store raw BSS responses, credentials, account IDs, resource IDs, order IDs,
or agent workspaces under `qa/`.
