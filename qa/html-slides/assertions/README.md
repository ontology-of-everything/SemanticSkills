# Assertions

Evaluate observable deck-building behavior, not exact wording. Copy assertions into each eval in `../evals/evals.json`.

- The skill runs only on explicit `$html-slides` / `/html-slides` invocation; a general slide-design question gets a plain answer.
- Stage 1 settles scene, audience, duration, style/profile and confidentiality before any outline; questions the user already answered are not re-asked.
- Three hard gates: outline confirmed → per-page table confirmed → HTML written; no HTML before the table is confirmed.
- The deck is one `.html` file: inlined variable block + `assets/core/base.css` + optional style css, `<section class="slide" data-label>` per page, inlined `runtime.js`; no `src="http`.
- Colors come only from the style's `vars-*.css`; no hardcoded brand hex inside skeletons or page markup.
- Fixed pages `cover` / `toc` / `thanks` appear exactly once; toc entries equal outline chapters; `data-label` count equals per-page table rows.
- No `data-todo` placeholder remains in the final deck; `?debug` reports ✓.
- PPTX is offered as two tiers (screenshot via `tools/export_pptx.py`, or rebuilt editable) and the delivery note states which tier and its limits; dependencies are never auto-installed.
- Huawei style: single red `#C7000B` as small-area focus, footer trio consistent, cover/thanks titles black, digits with source footnote.
