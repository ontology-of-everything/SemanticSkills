# Assertions

Eval prompts and programmatic expectations live in `../evals/evals.json` (`expectations` per case).

After A/B runs land under repo-root `huawei-cloud-cost-estimation-workspace/iteration-1/<eval-name>/{with_skill,without_skill}/outputs/response.md`:

```bash
python3 qa/huawei-cloud-cost-estimation/bin/run_ab_eval.py grade-all
python3 qa/huawei-cloud-cost-estimation/bin/run_ab_eval.py aggregate
```

Grader: `../bin/grade_response.py` (keyword/contract checks; not a substitute for human review on subjective tone).

Define objective checks for Skill Creator runs. Assertions are inlined in `../evals/evals.json` per eval.

Include interaction-discipline cases when the skill has routing or scope decisions:

- User already stated scope, billing cycle, or read-only intent → agent proceeds without re-asking.
- Blocking ID missing (partner customer, full order id) → one clarifying question, not a questionnaire.
