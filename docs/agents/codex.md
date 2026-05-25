# Codex

Install a skill from this repo:

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill <skill-name> \
  --agent codex \
  --copy
```

Codex direct skill installs use the same `SKILL.md` structure as Cursor and
Claude Code. For repo-scoped authoring, Codex scans `.agents/skills/` from the
current working directory up to the repository root.

For broad reusable distribution, Codex recommends plugins, but plugin packaging
is optional and not required for this repository's direct skill install path.

**Interaction discipline** (一次只问一事): [authoring.md § Interaction discipline](../authoring.md#interaction-discipline-all-skills).
