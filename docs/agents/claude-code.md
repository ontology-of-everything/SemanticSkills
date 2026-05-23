# Claude Code

Install a skill from this repo:

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill <skill-name> \
  --agent claude-code \
  --copy
```

Or copy `skills/<skill-name>/` to:

- `~/.claude/skills/` (user-wide), or
- `.claude/skills/` (project)

Folder name must match `name` in `SKILL.md` frontmatter.

See [agentskills.io](https://agentskills.io/) and Claude Code docs for skill discovery behavior.
