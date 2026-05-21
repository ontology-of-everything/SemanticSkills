# Contributing

Thanks for contributing to [SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills).

## Quick start

1. Fork and clone the repo.
2. Add or edit a skill under `skills/<name>/` (runtime only).
3. Add matching QA under `qa/<name>/` with `validate.sh` and optional `evals/`.
4. Register the skill in `docs/catalog.yml`.
5. Run `./tools/validate-all.sh` before opening a PR.

See [authoring.md](authoring.md) for conventions and [agents/](agents/) for install paths per agent.

## Pull requests

- One skill or one focused change per PR when possible.
- Keep `skills/<name>/` installable — no test assets inside skill folders.
- Update `docs/skills/<name>.md` and README skill table for new or changed skills.
- CI must pass (`validate` workflow).

## Commit messages

Use conventional commits:

```text
feat(huawei-cloud-billing-scout): add coupon reconciliation scenario
fix(project): correct catalog path for new skill
docs(authoring): clarify frontmatter token budget
test(skill-name): add eval for export reconciliation
```

## License

Contributions are licensed under the same terms as the repository ([Apache-2.0](../LICENSE)).
