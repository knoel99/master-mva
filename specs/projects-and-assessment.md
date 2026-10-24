# Contract — projects and assessment on every science page; end-of-year projects

| Field | Value |
|---|---|
| ID | `projects-and-assessment` |
| Scope | Section `## Projects and assessment {#projects}` of every science page; page `projects/index.qmd` |
| Gate | `tools/check_gates.py` (counts below) |
| Shared with | `knoel99/polytechnique-llga` (same section format, added in the same round) |

## Why

MVA courses are assessed mostly by a project — very often the study and reimplementation of a research paper, presented orally — and by a written exam; several also use homework or a data challenge. A student reading the notes needs ready-to-use project subjects at the right scale and a picture of what an exam on the course looks like.

## Section format (between *Exercises* and *References*)

```
## Projects and assessment {#projects}

One paragraph: the official assessment of the course (from the fiche) and how the proposals below fit it.

### Solo projects {#projects-solo}

1.  **[Solo · ≈ 20 h] Title.** Question studied; what to implement or prove; data or paper used; deliverables (code, 4–6 page report, 10-min talk); chapters used (ch. 2, 4).

### Group projects {#projects-group}

1.  **[Group of 2–3 · ≈ 30 h each] Title.** Same fields, plus how the work splits between members.

### Written exam (proposal) {#projects-exam}

Format line (duration, documents allowed, number of exercises).

1.  **Question (n points).** Statement. *Expected*: the outline of a full-mark answer.

### Grading rubric (proposal) {#projects-rubric}

| Criterion | Weight | What earns the marks |
|---|---|---|
```

## Rules

- **P1** At least **2 solo** and **2 group** subjects; each names its scale (hours), its deliverables, the chapters it uses and how it is evaluated. At least one subject per page is a **paper study**: reproduce or extend a named, real research paper (authors, year), the MVA tradition.
- **P2** Subjects are feasible: public data or synthetic data, a laptop or a free GPU tier, a clear success criterion (a number to reach, a figure to reproduce, a theorem to prove).
- **P3** The **written exam** proposal has at least **3 questions** with points summing to 20 and an expected-answer outline for each; it mixes a course question, a computation and a short proof.
- **P4** A **rubric** table gives criteria and weights (summing to 100 %).
- **P5** Prose follows the airy rules (each list item ≤ 100 words; sub-bullets allowed).
- **P6 Refresher variant.** The three refresher pages (kind `refresher`: no ECTS, no assessment) replace the exam and the 2 + 2 subjects by a lighter variant, in this order:
  - `### Diagnostic self-check {#projects-selfcheck}`: short questions, each naming the chapter that answers it, with expected answers;
  - `### Practice projects {#projects-practice}`: at least 2 numbered `**[Solo` or `**[Group` subjects of a few hours, at least one a paper study;
  - `### Self-assessment grid {#projects-rubric}`: criteria and weights summing to 100 %.

## End-of-year projects page (`projects/index.qmd`)

Integrative projects that combine courses of a route or a track, sized for 4–6 weeks of a group of 3–4, the way the research internship will: for each, the courses it draws on (links), the research question, the milestones, the deliverables, the evaluation and the variants (solo / group). At least one project per route of `specs/home-and-tracks.md` and per track (Santé, I&I, RR).

## Proof

- `python3 tools/check_gates.py`: for each science page, the section exists in the right place, ≥ 2 `**[Solo` items, ≥ 2 `**[Group` items, ≥ 3 numbered exam questions; for each refresher page, the three anchors of P6 and ≥ 2 practice subjects; the projects page exists, has no TODO and links only catalogue pages.
