# Assertions

Define objective checks for Skill Creator runs. Copy assertions into each eval in `../evals/evals.json`.

Include interaction-discipline cases when the skill has routing or scope decisions:

- User already stated scope, billing cycle, or read-only intent → agent proceeds without re-asking.
- Blocking ID missing (partner customer, full order id) → one clarifying question, not a questionnaire.

For the Phase 2 decision workbench, assert:

- Object metadata and evidence are shared, while each decision asks exactly one question.
- `basis`, `confidence`, and user `status` remain separate.
- Non-explicit decisions have complete, mutually exclusive options; no option hides its
  conditions, benefit, cost, risk, evidence, or recommendation reason.
- `depends_on` blocks downstream decisions until its target is explicitly resolved.
- The report never defaults decisions to approved and cannot emit `approved:true` while
  any actionable decision is pending, blocked, corrected, supplemented, or rejected.
