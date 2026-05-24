# huawei-cloud-billing-scout QA

Quality gate for the Huawei Cloud billing skill. Run after changing `SKILL.md`,
semantic YAML, `related-commands.md`, or public docs.

## Commands

```bash
./qa/huawei-cloud-billing-scout/validate.sh              # full gate (CI / Done)
python3 qa/huawei-cloud-billing-scout/bin/gate.py fast   # deterministic only
python3 qa/huawei-cloud-billing-scout/bin/gate.py style  # skillcheck + markdownlint + skill-scanner
./tools/validate-all.sh
```

`validate.sh` is offline and read-only: layout, ripgrep guards, YAML/docs/evals,
58-op contracts (`verify_ops.py`), eval export, optional style tools, offline
protocol eval (golden answers + assertion rules — no LLM API).

## Layout

```text
qa/huawei-cloud-billing-scout/
├── validate.sh
├── skillcheck.toml
├── .markdownlint.json
├── policy.skill-scanner.yaml
├── evals/evals.json
├── evals/llm-rubric.yml
├── fixtures/ops_contracts.yml
└── bin/
    ├── gate.py
    ├── gate_checks.py
    ├── qa_common.py
    ├── protocol_grading.py
    ├── export_llm_eval.py
    └── verify_ops.py
```

Do not store raw BSS responses, credentials, IDs, or agent workspaces under `qa/`.
