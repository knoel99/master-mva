# Front-end redesign: projector contrast, dark mode, side contents, airy pages

Inherited from the LLGA notes (polytechnique-llga, PR #41–#42, 22 October 2026): the MVA site starts with this front end.

- The colours must be more contrasted: over HDMI (projector) the grey shades of the old "paper" theme disappear.
- Dark mode.
- Much more mobile friendly.
- The contents list must be visible at any time.
- Airy content: not too many equations in the same sentence or block, line breaks between ideas, important results on a line of their own.

This contract supersedes the "paper look" principle of `AGENTS.md` (light LaTeX-like greys): the visual source of truth is still `assets/paper.css`, now under the rules below.

## V — Visual rules (`assets/paper.css`)

- **V1 Contrast.** Every text colour reaches at least **7:1** (WCAG AAA) against its background, in light and in dark mode, including secondary text, box titles, table headers and code tokens. There is no light-grey text. Lines that carry structure (table borders, box frames, rules under headings) are drawn in mid or dark tones at 2–7 px, never as hairlines.
- **V2 Boxes by colour.** Each kind of box has a tinted background and a 7 px coloured left bar, so the kinds stay distinct on a washed-out projector:
  - definition: blue;
  - theorem, proposition, lemma: amber;
  - example: green;
  - note: violet;
  - recap: slate;
  - key result (`::: key`, new): red, with a centred, enlarged formula.

  Proofs keep a plain left bar. Theorem bodies are upright, not italic.
- **V3 Dark mode.** The light and dark palettes are defined as tokens on `:root`. Dark mode follows `prefers-color-scheme` until the reader presses the theme button in the top bar. The choice is stored in `localStorage` under `mva-theme`.
- **V4 Type and rhythm.**
  - Body text: 18 px with line height 1.75 (17 px on phones).
  - Paragraphs: about 1 rem apart.
  - Display formulas: 1.5 rem of space above and below, set slightly larger than the text.
  - Headings: heavier, and h2 is underlined in the accent colour.

## N — Navigation (`assets/theme.js`, shared header in every `index.qmd`)

- **N1 Top bar.** Every page has a sticky top bar containing:
  - the *Contents* button;
  - the site name, linking home;
  - the title of the section being read;
  - the *Dark / Light* button.

  A thin bar under it shows how far the reader is through the page.
- **N2 Side contents, always available.** The panel is built from the h2 and h3 headings of `<main>`.
  - From 75 rem (1200 px) wide, it is a sticky left column that is always visible; the button hides it, and the choice is remembered.
  - Below that width, it is a drawer opened from the top bar. It closes with *Close*, Escape, the backdrop or a link.
  - The current section is highlighted, and its subsections unfold.
- **N3 Mobile.**
  - At 390 px there is no horizontal page scroll.
  - Tables scroll sideways inside their own frame.
  - Two-column key/value tables (course sheets) stack, with the label above the value.
  - Long display formulas scroll inside their line.
  - Buttons are at least 40 px high.

## A — Airy prose (gate `tools/check_airiness.py`, run by `tools/check_gates.py`)

A *block* is a paragraph or one list item, outside code, display maths, tables, headings and References.

- **A1** A block has at most 100 words (an inline formula counts as one word).
- **A2** A block has at most 6 inline formulas.
- **A3** No inline formula is longer than 50 TeX characters, spaces excluded. Such a formula goes on its own line as display maths.

Beyond the gate, the editorial rules are:

- The conclusion of each theorem, the formula of each definition used later, and the final numbers of worked examples stand on a line of their own.
- Multi-step proofs and examples are written as lists or short paragraphs, one step each.
- At most about one `::: key` box per chapter, for the formula to remember.

These are changes of form only: content and mathematics are unchanged, and `tools/check_progression.py` still passes.

Pandoc simple tables whose cells overflowed their column, which cut formulas and showed a stray `$`, become pipe tables with `tools/fix_simple_tables.py`. The tool prints every row it had to cut by position, for review.

## Proof

- `python3 tools/check_gates.py` passes. It now includes the airiness gate.
- KaTeX renders every span of every page (`katex.renderToString` over the rendered HTML).
- No literal `$` outside maths in any rendered page, except escaped currency signs.
- Playwright, on every page, at 1440 px and 390 px, in light and in dark mode:
  - no horizontal overflow;
  - no script error;
  - minimum text contrast ≥ 7:1.
