# semantic-layer-builder Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 0.1.0 - 2026-06-29

First release — meta-skill that turns an interface into a governed semantic layer.

### Features

- Guided, one-fact-at-a-time interview: Ingest → Frame → Confirm (facts/grain/dimensions/measures/routing) → Emit
- Schema constraints for semantic objects (Kimball star/constellation): `catalog` (thin router) → shared-dimensions → model, in `references/schema-spec.md` with a Conformance checklist
- Google OKF v0.1 export (recommended): concept-per-file mapping, reserved files, frontmatter, and OKF §9 hard-constraint check in `references/okf-emitter.md`
- Evidence-only discipline: refuses to invent fields, grain, enums, or values; missing sources marked `TODO(verify)`
- Ingest rules for REST/OpenAPI, CLI, and table/DDL inputs; end-to-end worked example (`references/examples.md`)

### qa

- `validate.sh` (layout, version sync, skills-ref, markdownlint, skillcheck)
- Five offline evals in `evals/evals.json` (grain-first, no-invented-fields, OKF default target, one-blocking-ask, layer-split)

### Documentation

- `docs/skills/semantic-layer-builder.md`; `docs/catalog.yml` index entry
