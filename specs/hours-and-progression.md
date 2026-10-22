# Contract — hours, session plans and increasing difficulty

| Field | Value |
|---|---|
| ID | `hours-and-progression` |
| Scope | Every science and refresher page + the home programme table |
| Source of hours | `plan_hours` of `data/catalog-2026-2027.json` (`specs/catalog-source.md`) |
| Gate | `python3 tools/check_progression.py` (also run by `tools/check_gates.py`) |
| Origin | LLGA contract of the same name (polytechnique-llga PR #40), adapted to MVA volumes |

## Rules

### R1 — Session plan (`### Session plan {#sessions}`)

Placed in the introduction, after *Course outline* and before *How to study this module*. It opens with one bold line:

```
**24 h in class = 8 sessions of 3 h.**
```

Variants: `**23 h in class = 9 sessions (7 × 3 h + 1 × 2 h).**`, `**24 h in class (assumed) = 8 sessions of 3 h.**` when the catalogue marks the volume assumed, and `**12 h of guided self-study = 4 steps of 3 h.**` for the refreshers. The total equals the catalogue's `plan_hours`. Then one sentence naming the source of the volume (and the master-mva.com organisation when it differs), saying that the split into sessions is a proposal. Then a pipe table:

| Session | Hours | Level | Content | Practice |
|---|---|---|---|---|
| 1 | 3 h | 1 | ch. 0 Review …; ch. 1.1–1.2 … | Ex. 1–2 |

- **Hours** sum exactly to the bold total.
- **Level** is `1` (foundations), `2` (core results and algorithms) or `3` (advanced, research-level); it **never decreases**.
- **Content** cites chapters as `ch. N` (sections `ch. 2.1–2.3`); the first chapter cited in each row never goes back.
- After the table, one line `**Self-study, outside the N h** (about K h in total): ch. 8 … (≈ 2 h) · …` lists every chapter not taught in class with a time estimate (the research-directions chapter at least).
- Every numbered chapter appears in the table or in the self-study line.

### R2 — Volume calibration

Prose words (code and maths stripped) of the chapters cited in the table, divided by the in-class hours, lie in **[100, 320] words per hour**.

### R3 — Chapter order = difficulty order

Chapters are numbered in page order (`## N. Title {#chN}`, consecutive, from 0). A chapter never relies on a later one.

### R4 — Graded exercises

Each exercise title starts with its level: `1.  **★ Title.**` (★ apply the course, ★★ combine or prove a short result, ★★★ open-ended or research-flavoured). Exercises are sorted by non-decreasing level.

## Proof

- `python3 tools/check_progression.py` exits 0 (it also checks that the bold total equals the catalogue volume).
- Pages rendered with `python3 tools/render.py <slug>`.
