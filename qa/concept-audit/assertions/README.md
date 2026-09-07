# Assertions

Evaluate observable audit behavior rather than exact headings or wording.

- The run stays read-only: no files are created or edited.
- All five dimensions run, or skipped dimensions are named with a reason.
- Each finding has a location, evidence a reviewer can re-check, a severity,
  and exactly one routing target.
- Related findings collapse to a root cause when they share one model or code
  defect.
- Repair order is upstream-first: design, then PRD, then implementation.
