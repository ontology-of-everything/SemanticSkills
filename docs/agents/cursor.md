# Cursor

Install a skill from this repo:

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill <skill-name> \
  --agent cursor \
  --copy
```

Local path:

```bash
npx skills add ./skills/<skill-name> \
  --skill <skill-name> \
  --agent cursor \
  --copy
```

Skills install to `./.agents/skills/` (gitignored). Review skill content before use; skills run with agent permissions.

Cursor also discovers user and project skills from `~/.cursor/skills/`,
`.cursor/skills/`, `~/.agents/skills/`, and compatible Claude/Codex skill
directories. Keep the skill folder name equal to the `name` frontmatter field.

**Interaction discipline** (一次只问一事): [authoring.md § Interaction discipline](../authoring.md#interaction-discipline-all-skills).
