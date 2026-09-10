# concept-guardrails QA

Per-skill quality gate. Run `validate.sh` locally and in CI via
`tools/validate-all.sh`.

## Layout

```text
qa/concept-guardrails/
├── validate.sh              # entry point (required)
├── README.md
├── VERSION
├── CHANGELOG.md
├── .markdownlint.json
├── evals/evals.json         # Skill Creator eval cases
└── assertions/README.md     # assertion rubric for eval authors
```

## Checks beyond the shared template

- **References routing** — each of the seven `references/*.md` files exists and is
  reachable from `SKILL.md`'s mode table. A mode that routes nowhere is a dead mode.
  The six bare mode names (`audit`, `concept`, `drift`, `pipeline`, `sync`, `map`)
  must appear in the table, and the pre-0.30.0 `wyx:` prefix must not reappear in
  `SKILL.md` or `references/`.
- **Runtime integrity** — the three upstream hook scripts parse under `bash -n`,
  `hooks.json` still registers SessionStart / PreToolUse / PostToolUse, both JSON
  files are parseable, and the upstream MIT notice is present. The runtime is
  vendored verbatim, so this gate catches an accidental edit rather than a bug.

## Commands

```bash
./qa/concept-guardrails/validate.sh
```
