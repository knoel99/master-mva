# AGENTS.md — Spec-Driven / BMAD (light) gates for master-mva

This repository is an **HTML course-notes site** (GitHub Pages) for the M2 **Mathématiques, Vision, Apprentissage (MVA)** of ENS Paris-Saclay. It starts from the final state of the LLGA notes framework (`specs/lessons-from-llga.md`): spec → plan → implement → prove.

## Principles

1. **One structural source** — `data/catalog-2026-2027.json` (master-mva.com + Université Paris-Saclay programme table) decides which courses exist, their semester, label, track, ECTS and volume (`specs/catalog-source.md`). Pages and the home page are generated from it or checked against it.
2. **No invented facts** — no course code, ECTS, instructor or assessment rule outside the official sources; missing facts are “not displayed”; derived volumes are “assumed”.
3. **English only** — `specs/en-only.md`.
4. **Projector-readable look** — `assets/paper.css` + `assets/theme.js` (`specs/front-redesign.md`), airy prose gate.
5. **Proofs before “done”** — the gates below.

## Mandatory gates (Definition of Done)

- [ ] **Contract**: page follows `specs/course-page.md` (science / refresher) or `specs/non-science-pages.md`.
- [ ] **Pages**: `courses/<slug>/index.qmd` (started with `python3 tools/new_course.py <slug>`) + rendered `index.html` (`python3 tools/render.py <slug>`).
- [ ] **Home**: regenerated with `python3 tools/build_home.py`; every page in the tree.
- [ ] **Hours and progression**: `python3 tools/check_progression.py` passes (`specs/hours-and-progression.md`).
- [ ] **Airy prose**: `python3 tools/check_airiness.py` passes.
- [ ] **Pedagogy**: ≥ 8 graded exercises (≥ 10 recommended) on science and refresher pages; **Projects and assessment** section on science pages (`specs/projects-and-assessment.md`); NumPy / PyTorch code that runs.
- [ ] **Smoke**: KaTeX and boxes readable in light and dark; no horizontal overflow on a phone.
- [ ] **Mechanical proof**: `python3 tools/check_gates.py` passes.

## Key files

- `data/catalog-2026-2027.json` — the catalogue (official facts, read 22 October 2026)
- `tools/new_course.py` · `tools/render.py` · `tools/build_home.py` · `tools/check_gates.py` · `tools/check_progression.py` · `tools/check_airiness.py` · `tools/renumber_chapters.py` · `tools/grade_exercises.py` · `tools/fix_simple_tables.py`
- `specs/README.md` — contract index
