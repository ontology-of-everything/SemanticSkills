# semantic-creator QA

Per-skill quality gate. Run `validate.sh` locally and in CI via
`tools/validate-all.sh`.

## Layout

```text
qa/semantic-creator/
├── validate.sh              # entry point (required)
├── README.md
├── evals/evals.json         # Skill Creator eval cases
├── assertions/README.md     # assertion rubric for eval authors
├── fixtures/                # optional: contract YAML, golden files
└── bin/                     # optional: helper scripts
```

Add `fixtures/` and `bin/` when a skill needs cross-layer checks beyond
`skills-ref`, markdownlint, and skillcheck.

## Commands

```bash
./qa/semantic-creator/validate.sh
```
