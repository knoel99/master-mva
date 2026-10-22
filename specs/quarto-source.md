# Contract — Quarto sources

| Field | Value |
|---|---|
| ID | `quarto-source` |
| Origin | LLGA `quarto-pilot` and `quarto-migration` (PRs #16–#22) |

- Source of truth: `courses/<slug>/index.qmd`; the rendered `index.html` is committed (GitHub Pages serves it).
- Shell: written by `tools/new_course.py` — `theme: none`, `minimal: true`, `paper.css`, top bar and side contents, `theme.js`, KaTeX 0.19.0.
- Render: `python3 tools/render.py <slug>` (Quarto 1.7.32), which puts back the pinned KaTeX tags with subresource integrity.
- Pitfalls carried over: display maths with `$$` (never `\[ \]`); no unbalanced `:::` fences; code fences carry a real language (```` ```python ````) so that Quarto highlights them; figures as SVG next to the page, referenced as `![caption](schema-name.svg){fig-alt="…" width="100%"}`.
