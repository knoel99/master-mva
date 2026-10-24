#!/usr/bin/env python3
"""Create the skeleton of a course page from the catalogue (specs/catalog-source.md).

Usage (repository root):
    python3 tools/new_course.py s2-kernel-methods          # writes courses/<slug>/index.qmd
    python3 tools/new_course.py --print s2-kernel-methods  # prints it instead

The skeleton holds the Quarto shell (paper.css, theme.js, pinned KaTeX), the
subtitle line and the facts of the fiche that come straight from
data/catalog-2026-2027.json. Every line marked TODO is for the author;
tools/check_gates.py fails while a TODO remains in a source.
Refuses to overwrite an existing index.qmd.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "catalog-2026-2027.json"
KATEX = "https://cdn.jsdelivr.net/npm/katex@0.19.0/dist/katex.min.js"

YAML = '''---
title: "{title}"
subtitle: "{subtitle}"
lang: en
format:
  html:
    theme: none
    minimal: true
    toc: false
    anchor-sections: false
    html-math-method:
      method: katex
      url: "{katex}"
    highlight-style: github
    embed-resources: false
    css: ../../assets/paper.css
    include-in-header:
      - text: |
          <meta name="color-scheme" content="light dark">
          <script>(function(){{try{{var t=localStorage.getItem("mva-theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}}})();</script>
    include-before-body:
      - text: |
          <a class="skip" href="#main">Skip to content</a>
          <header class="topbar">
            <button type="button" class="tb-btn" id="toc-toggle" aria-controls="sidetoc" aria-expanded="false"><span aria-hidden="true">☰</span><span class="tb-label">Contents</span></button>
            <a class="brand" href="../../index.html">MVA<span class="brand-sub"> · Course notes</span></a>
            <span class="tb-title" id="tb-title"></span>
            <button type="button" class="tb-btn" id="theme-toggle"><span aria-hidden="true">◐</span><span class="tb-label">Theme</span></button>
          </header>
          <div class="layout">
          <nav class="sidetoc" id="sidetoc" aria-label="Contents"></nav>
          <main class="paper" id="main">
    include-after-body:
      - text: |
          </main>
          </div>
          <footer class="foot"><p><a href="../../index.html">← Master's programme</a></p></footer>
          <script defer src="../../assets/theme.js"></script>
---
'''

SEMESTER = {
    1: "Semester 1 · period 1 (28/09/2026 – 08/01/2027)",
    2: "Semester 2 · period 2 (04/01/2027 – 02/04/2027)",
    "both": "Both semesters (2026–2027)",
    0: "Before semester 1 · refresher fortnight (14/09/2026 – 24/09/2026)",
    3: "After the courses · from 05/04/2027, at least four months",
}


def load():
    return {c["slug"]: c for c in json.loads(CATALOG.read_text(encoding="utf-8"))["courses"]}


def fmt_h(x):
    return f"{x:g} h"


def volume(c):
    h = c.get("hours_official") or {}
    parts = [f"{k} {fmt_h(h[v])}" for k, v in
             [("lectures", "lecture"), ("tutorials", "td"), ("labs", "tp"), ("project", "project")]
             if h.get(v)]
    if c["hours_status"] == "official":
        return (f"{c['ects']:g} ECTS · {fmt_h(c['plan_hours'])} "
                f"({', '.join(parts)}) per the Université Paris-Saclay programme table")
    if c["hours_status"] == "self-study":
        return f"no ECTS · {fmt_h(c['plan_hours'])} of guided self-study ({c['hours_source']})"
    if c["hours_status"] == "assumed":
        note = re.sub(r"^assumed(?: from)?:?\s*", "", c["plan_hours_note"])
        return f"{c['ects']:g} ECTS · {fmt_h(c['plan_hours'])} (assumed: {note})"
    return f"{c['ects']:g} ECTS · volume: TODO"


def label(c):
    bits = [f"[{t}]{{.badge .label}}" for t in c["types"]]
    bits += [f"[Track {t}]{{.badge .track}}" for t in c["tracks"]]
    return "".join(bits) or "TODO"


def skeleton(c):
    sem = c["semester"]
    sem_txt = {1: "Semester 1", 2: "Semester 2", "both": "Both semesters", 0: "Refresher", 3: "Internship"}[sem]
    sub = " · ".join(["M2 MVA", sem_txt] + c["types"] + [f"{c['ects']:g} ECTS"])
    rows = [
        ("Module", c["title_en"]),
        ("Official title", c["title_official"]),
        ("Instructors", f"{c['instructors']} (master-mva.com, 2026–2027)"),
        ("Period", SEMESTER[sem]),
        ("Credits and volume", volume(c)),
        ("Label", label(c) + (f" · domains on master-mva.com: {', '.join(c['domains'])}" if c["domains"] else "")),
        ("Language", "TODO (from the official pages)"),
        ("Assessment", "TODO (official “Mode de validation”, in English)"),
        ("Prerequisites", "TODO (official “Prérequis”, in English, or “not displayed”)"),
    ]
    if c.get("discrepancy_note"):
        rows.append(("Note on sources", c["discrepancy_note"]))
    w = max(len(k) for k, _ in rows) + 2
    rule = "-" * w + " " + "-" * 120
    table = "\n".join(["  " + rule] + [f"  {k.ljust(w)} {v}" for k, v in rows] + ["  " + rule])
    return YAML.format(title=c["title_en"].replace('"', "'"), subtitle=sub, katex=KATEX) + f"""
## Contents

TODO: one bullet per level-2 heading, in page order.

## Introduction and overview {{#intro}}

{table}

TODO: audience line, empirical-first line, “What you will be able to do”, “Official objectives and syllabus (2026–2027)”, “Where this course fits in the programme”, “Course outline”, “Session plan {{#sessions}}”, “How to study this module”.

## Exercises {{#ex}}

TODO

## Projects and assessment {{#projects}}

TODO

## References {{#refs}}

TODO
"""


def main(argv):
    to_stdout = "--print" in argv
    slugs = [a for a in argv if not a.startswith("--")]
    if not slugs:
        sys.exit(__doc__)
    cat = load()
    for slug in slugs:
        c = cat[slug]
        text = skeleton(c)
        if to_stdout:
            print(text)
            continue
        path = ROOT / "courses" / slug / "index.qmd"
        if path.exists():
            print(f"{slug}: index.qmd exists, left untouched")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"{slug}: skeleton written")


if __name__ == "__main__":
    main(sys.argv[1:])
