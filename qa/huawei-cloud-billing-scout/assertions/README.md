# A/B eval (Skill Creator)

After agent runs land under repo-root `huawei-cloud-billing-scout-workspace/iteration-1/<eval-name>/{with_skill,old_skill}/outputs/response.md`:

```bash
python3 qa/huawei-cloud-billing-scout/bin/run_ab_eval.py snapshot-old-skill   # once: git HEAD → skill-snapshot/
python3 qa/huawei-cloud-billing-scout/bin/run_ab_eval.py init-metadata
python3 qa/huawei-cloud-billing-scout/bin/run_ab_eval.py grade-all
python3 qa/huawei-cloud-billing-scout/bin/run_ab_eval.py aggregate          # benchmark.json + benchmark-review.html
```

- **with_skill** — `skills/huawei-cloud-billing-scout/` (working tree)
- **old_skill** — `iteration-1/skill-snapshot/` (committed HEAD before local edits)

Grader: `bin/grade_response.py` (protocol rules from `protocol_grading.py`; not a substitute for human/LLM rubric on tone).
