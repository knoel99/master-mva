# Contract — the catalogue is the single structural source

| Field | Value |
|---|---|
| ID | `catalog-source` |
| File | `data/catalog-2026-2027.json` |
| Sources | master-mva.com (semester lists, every course page, validation rules, planning, tracks, internship) and the Université Paris-Saclay programme page (table of ECTS and hourly volumes, course-detail fragments), all read on 22 October 2026 |

## Rules

1. **Which courses exist, and when.** The two semester lists of master-mva.com decide which courses are offered in 2026–2027, their semester, their label (Learning / Modelling / Opening), their domain tags and their track (Santé, I&I, RR). The master's own site wins when the Université Paris-Saclay table places a course in another semester; the fiche then says so in a *Note on sources* row.
2. **Volumes and ECTS.** The Université Paris-Saclay table gives the official ECTS and the hours split into lectures, tutorials, labs and project. The session plan of a page sums to that total (`plan_hours`).
3. **No official volume.** When the table shows no volume (Foundations of LLMs, Learning Physical Phenomena, Reinforcement Learning), the volume comes from the session list on master-mva.com and is marked *assumed*, with the reason, in the catalogue and in the fiche.
4. **No invented facts.** No course code, ECTS value, instructor or assessment rule appears on a page unless one of the two sources states it. Missing facts are written “not displayed”.
5. **Kinds.** `science` (64 courses: full page), `non-science` (hospital immersion, Regulating AI, reproducible-research project, internship: framing page, `specs/non-science-pages.md`), `refresher` (three independent pages for the official refresher fortnight, whose programme is not published).
6. **Generated views.** `tools/new_course.py` writes the fiche facts into a new page; `tools/build_home.py` writes the home tree and programme table. Neither is edited by hand.

## Proof

- `python3 tools/check_gates.py`: every catalogue course has a page, no page is outside the catalogue, the fiche quotes the catalogue's ECTS and volume, the home tree lists every page.
