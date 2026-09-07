# concept-design QA

Per-skill quality gate. Run `validate.sh` locally and in CI via
`tools/validate-all.sh`.

## Layout

```text
qa/concept-design/
├── validate.sh              # entry point (required)
├── README.md
├── evals/evals.json         # Skill Creator eval cases
├── assertions/README.md     # assertion rubric for eval authors
├── fixtures/                # optional: contract YAML, golden files
└── bin/                     # optional: helper scripts
```

Add `fixtures/` and `bin/` when the skill needs cross-layer checks beyond
`skills-ref`, markdownlint, and skillcheck.

## Commands

```bash
./qa/concept-design/validate.sh
```

## Token 复核

`token-baseline.json` 保存本次任务开始时工作树（包含已有未提交修改）的各文件 token 数与 SHA-256；不是 HEAD 基线。
使用 o200k_base，复核命令：

```bash
uv run --with tiktoken python qa/concept-design/measure-tokens.py
```

分别报告入口、全部 Markdown 和包含原样 runtime 的全部载荷；文件搬到 references 不算总量压缩。基线记录 tokenizer 版本；新 runtime/参考文件也纳入当前统计。
