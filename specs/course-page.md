# Contract — anatomy of a science course page

| Field | Value |
|---|---|
| ID | `course-page` |
| Scope | Every `courses/<slug>/index.qmd` of kind `science` or `refresher` in `data/catalog-2026-2027.json` |
| Start | `python3 tools/new_course.py <slug>` writes the Quarto shell and the catalogue facts |
| Gates | `tools/check_gates.py`, `tools/check_progression.py`, `tools/check_airiness.py` |

A page is a self-contained course for a student with a good M1 in mathematics, computer science or physics (the MVA admission level). It reconstructs what the official course description announces; it does not claim to be the instructors' material.

## Order of sections

1. `## Contents` — one bullet per level-2 heading, in page order: `-   [Introduction and overview](#intro)`, `-   [0. Review: …](#ch0)`, …, `-   [Exercises](#ex)`, `-   [Projects and assessment](#projects)`, `-   [References](#refs)`.
2. `## Introduction and overview {#intro}`
   - **Fiche** (pandoc simple table from the skeleton). Fill *Language*, *Assessment* and *Prerequisites* from the official pages, in English, faithfully (translate French; quote numbers and weights exactly; “not displayed” when absent). Do not change the catalogue facts.
   - `**Audience**:` one sentence. `**Empirical first**:` one or two sentences naming a concrete phenomenon, failure or data set the course explains, before any theory.
   - One short paragraph saying what the course is about, with links to related MVA pages (`../<slug>/index.html`).
   - `### What you will be able to do` — 6 to 12 bullets, each starting with a verb.
   - `### Official objectives and syllabus (2026–2027)` — the official objective restated in English and attributed (“The course description on master-mva.com…”); then a pipe table `| Official topic | Course section |` with **one row per official topic** (each item of “Thèmes abordés”, each announced session, each item of the Université Paris-Saclay “Programme / plan / contenus”); every topic is taught somewhere on the page, or the row says “not covered” with a one-clause reason. Then one sentence naming this page's extensions beyond the syllabus.
   - `### Where this course fits in the programme` — official prerequisites; which MVA refreshers and courses prepare it; which MVA courses build on it or share tools with it (links). Same-semester courses are “related”, never “prerequisites”.
   - `### Course outline` — one bullet per chapter: `-   **Title** — what it does.`
   - `### Session plan {#sessions}` — see `specs/hours-and-progression.md`.
   - `### How to study this module` — a few bullets: reading order, which exercises after which session, the Python environment.
3. Chapters `## N. Title {#chN}`, numbered from 0, in order of difficulty:
   - `## 0. Review: …` — the M1-level tools the course needs (level 1), short and targeted.
   - Core chapters (levels 1–2), then advanced ones (level 3).
   - Last chapter: `## N. Research directions and open problems {#chN}` — self-study; neutral voice (“work by X and coauthors shows…”), never “our team”; only papers you are sure exist, with authors and year.
4. `## Exercises {#ex}` — at least 10, graded and sorted (`specs/hours-and-progression.md` R4), each with a *Solution* or *Hints and expected result* paragraph; at least two are computational (Python).
5. `## Projects and assessment {#projects}` — `specs/projects-and-assessment.md`.
6. `## References {#refs}` — the official references first (from the catalogue), then standard textbooks and papers. Every entry must be real: authors, title, venue or publisher, year.

## Inside a chapter

- Open with one or two plain sentences: what problem the chapter solves.
- Boxes (Pandoc fenced divs, classes styled by `assets/paper.css`):
  `::: def`, `::: thm`, `::: prop`, `::: proof`, `::: ex`, `::: note`, `::: key` (at most about one per chapter, the formula to remember), `::: recap` (end of chapter, “Key takeaways — chapter N” on its first line).
  Labels: `[Definition 2.3 — Name]{.tag}`, `[Theorem 2.4 — Name]{.tag}`, numbered per chapter.
- Proofs: complete for the central results; a precise sketch with the key step otherwise; a reference when a proof is out of scope.
- Worked examples with actual numbers.
- Code: short, runnable, ```` ```python ```` fences; NumPy / SciPy / PyTorch / scikit-learn / domain libraries; seeds fixed; no hidden data (use synthetic data or a public data set named precisely).
- Mathematics: `$…$` inline, `$$…$$` on their own lines for display; never `\[ \]`; `|x|` for absolute values, `\|x\|` for norms; English decimal points.
- Airy prose (`specs/front-redesign.md`): blocks ≤ 100 words, ≤ 6 inline formulas, no inline formula over 50 TeX characters; the conclusion of each theorem on its own line; full sentences, no note-taking style.
- Cross-references to chapters and boxes of the same page use their numbers (`ch. 3`, `Theorem 3.2`) and anchors (`[ch. 3](#ch3)`).

## Size

The in-class chapters hold 100–320 prose words per official hour (`tools/check_progression.py`); self-study chapters add to that. A typical 24 h course page is 50–90 kB of Quarto source.

## Rendering

`python3 tools/render.py <slug>` (Quarto 1.7.32, `pip install quarto-cli==1.7.32`) renders `index.html` and restores the pinned KaTeX tags.
