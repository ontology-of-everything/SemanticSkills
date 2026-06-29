# Assertions

Define objective checks for Skill Creator runs. Copy assertions into each eval in `../evals/evals.json`.

Include interaction-discipline cases when the skill has routing or scope decisions:

- User already stated scope, billing cycle, or read-only intent → agent proceeds without re-asking.
- Blocking ID missing (partner customer, full order id) → one clarifying question, not a questionnaire.
