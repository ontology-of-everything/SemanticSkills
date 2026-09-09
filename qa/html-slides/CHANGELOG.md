# html-slides Changelog

## 0.1.0 - 2026-09-09

### Added

- Initial `html-slides` (skill id; invoke `$html-slides`): explicit-invocation
  deck builder that writes a plain
  single-file 1920×1080 HTML with a pluggable visual style; optional
  screenshot PPTX via `tools/export_pptx.py` (deps never auto-installed)
- Knowledge base: seven-stage workflow with three hard-gate discussions,
  style-agnostic rules, page-type catalog by visual family, two-stage artwork
  workflow, build/layer motion protocol
- Code split from prose: `assets/core/` (base.css, runtime.js, skeletons.html
  gallery), `assets/<style>/` (vars-light/dark.css, style.css, patterns.html);
  `references/*.md` hold rules only and point to these files
- Styles: `generic` (default), `huawei` (official-deck analysis, light/dark,
  five bundled assets ≈1 MB), `apple` (experience-based, no assets);
  `styles/_template.md` for adding more
- Runtime verified in Chromium: scroll/present modes, build/layer stepping,
  Home/End, hash + localStorage resume, `?debug` overflow markers

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).
