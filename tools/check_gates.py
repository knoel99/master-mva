#!/usr/bin/env python3
"""Mechanical gates from AGENTS.md (Spec Kit-compatible / BMAD light).

Run from the repository root:  python3 tools/check_gates.py
Exit code 0 = all gates pass; 1 = at least one gate failed.

Checks (code-level proxies for the manual gates):
- Catalogue coverage: every course of data/catalog-2026-2027.json has a page
  courses/<slug>/index.qmd + rendered index.html, and no page is outside the catalogue.
- Pages: lang="en", theme.js loaded, no FR switcher, no TODO left in a source.
- Fiche: the introduction quotes the catalogue's ECTS and volume.
- Pedagogy: >= 8 graded exercises on science and refresher pages; a
  "Projects and assessment" section on science pages, and its refresher variant
  (self-check, practice projects, grid) on refresher pages (specs/projects-and-assessment.md).
- Home: generated tree lists every page; tracks and routes wired; every route
  is a feasible programme under the validation rules (specs/home-and-tracks.md).
- KaTeX: published pages and Quarto sources pin 0.19.0 with subresource integrity.
- Specs: every contract file has a row in specs/README.md.
- Runs tools/check_progression.py and tools/check_airiness.py.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / "data/catalog-2026-2027.json").read_text(encoding="utf-8"))["courses"]
BY_SLUG = {c["slug"]: c for c in CATALOG}

FR_SWITCHER = re.compile(r"français|lang-toggle|href=\"[^\"]*/fr/", re.IGNORECASE)
EX_SECTION = re.compile(r'<h2 id="ex(?:ercises)?"[^>]*>', re.IGNORECASE)
NEXT_H2 = re.compile(r"<h2[ >]")
LI = re.compile(r"<li[ >]")

failures: list[str] = []
passed = 0


def check(ok: bool, label: str, detail: str = "") -> None:
    global passed
    if ok:
        passed += 1
    else:
        failures.append(f"{label}{': ' + detail if detail else ''}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def exercise_count(html: str) -> int:
    """<li> items between the Exercises <h2> and the next <h2>."""
    m = EX_SECTION.search(html)
    if not m:
        return 0
    end = NEXT_H2.search(html, m.end())
    body = html[m.end(): end.start() if end else len(html)]
    return len(LI.findall(body))


def subsection(src: str, start: str) -> str:
    i = src.find(start)
    if i < 0:
        return ""
    m = re.compile(r"^#{2,3} ", re.M).search(src, i + len(start))
    return src[i: m.start() if m else len(src)]


# --- Catalogue coverage ------------------------------------------------------
course_dirs = sorted(p for p in (ROOT / "courses").iterdir() if p.is_dir())
names = {p.name for p in course_dirs}
for slug in BY_SLUG:
    check(slug in names, f"catalogue: {slug} has a page directory")
for name in names:
    check(name in BY_SLUG, f"catalogue: courses/{name} is in the catalogue")

# --- Pages -------------------------------------------------------------------
for cdir in course_dirs:
    cid = cdir.name
    c = BY_SLUG.get(cid)
    qmd_path, html_path = cdir / "index.qmd", cdir / "index.html"
    check(qmd_path.is_file(), f"{cid}: index.qmd source present")
    check(html_path.is_file(), f"{cid}: rendered index.html present")
    if not (qmd_path.is_file() and html_path.is_file()) or c is None:
        continue
    src, html = read(qmd_path), read(html_path)
    check("TODO" not in src, f"{cid}: no TODO left in the source")
    check('lang="en"' in html[:400], f"{cid}: lang=en")
    check("theme.js" in html, f"{cid}: theme.js loaded")
    check(not FR_SWITCHER.search(html), f"{cid}: no FR switcher / French link")
    check('localStorage.getItem("mva-theme")' in src, f"{cid}: MVA theme key in the Quarto shell")
    intro = subsection(src, "## Introduction and overview {#intro}")
    check(bool(intro), f"{cid}: introduction section with id #intro")
    if c["kind"] != "non-science":
        check(f"{c['ects']:g} ECTS" in intro or c["kind"] == "refresher",
              f"{cid}: fiche quotes {c['ects']:g} ECTS")
        check(f"{c['plan_hours']:g} h" in intro, f"{cid}: fiche quotes the {c['plan_hours']:g} h volume")
        n_ex = exercise_count(html)
        check(n_ex >= 8, f"{cid}: >= 8 exercises", f"found {n_ex}")
    if c["kind"] == "science":
        proj = src.split("## Projects and assessment {#projects}", 1)
        check(len(proj) == 2, f"{cid}: '## Projects and assessment {{#projects}}' section")
        if len(proj) == 2:
            body = proj[1].split("\n## ", 1)[0]
            solo = len(re.findall(r"^\d+\.\s+\*\*\[Solo", body, re.M))
            group = len(re.findall(r"^\d+\.\s+\*\*\[Group", body, re.M))
            check(solo >= 2, f"{cid}: >= 2 solo project subjects", f"found {solo}")
            check(group >= 2, f"{cid}: >= 2 group project subjects", f"found {group}")
            exam = subsection(proj[1], "### Written exam")
            nq = len(re.findall(r"^\d+\.\s", exam, re.M))
            check(nq >= 3, f"{cid}: written-exam proposal with >= 3 questions", f"found {nq}")
            check(src.find("## Exercises {#ex}") < src.find("## Projects and assessment")
                  < src.find("## References {#refs}"),
                  f"{cid}: Projects section between Exercises and References")
    if c["kind"] == "refresher":
        proj = src.split("## Projects and assessment {#projects}", 1)
        check(len(proj) == 2, f"{cid}: '## Projects and assessment {{#projects}}' section")
        if len(proj) == 2:
            body = proj[1].split("\n## ", 1)[0]
            for sub in ("projects-selfcheck", "projects-practice", "projects-rubric"):
                check(f"{{#{sub}}}" in body, f"{cid}: refresher variant has {{#{sub}}}")
            practice = subsection(proj[1], "### Practice projects")
            n = len(re.findall(r"^\d+\.\s+\*\*\[(?:Solo|Group)", practice, re.M))
            check(n >= 2, f"{cid}: >= 2 practice projects", f"found {n}")
            check(src.find("## Exercises {#ex}") < src.find("## Projects and assessment")
                  < src.find("## References {#refs}"),
                  f"{cid}: Projects section between Exercises and References")

# --- Projects page -----------------------------------------------------------
pq, ph = ROOT / "projects/index.qmd", ROOT / "projects/index.html"
check(pq.is_file() and ph.is_file(), "projects/: end-of-year projects page (qmd + html)")
if pq.is_file():
    psrc = read(pq)
    check("TODO" not in psrc, "projects/: no TODO left")
    links = set(re.findall(r"\.\./courses/([\w-]+)/index\.html", psrc))
    unknown = sorted(links - set(BY_SLUG))
    check(not unknown, "projects/: links only to catalogue pages", ", ".join(unknown))

# --- Home --------------------------------------------------------------------
home_path = ROOT / "index.html"
check(home_path.is_file(), "root: index.html present")
home = read(home_path) if home_path.is_file() else ""
check(not FR_SWITCHER.search(home), "root: index.html no FR switcher")
tree_html = home.split('id="curriculum-tree"')[1].split("</section>")[0] if 'id="curriculum-tree"' in home else ""
check(bool(tree_html), "home: curriculum tree present")
for slug in BY_SLUG:
    check(f"courses/{slug}/index.html" in tree_html, f"home tree: {slug} listed")
check('href="projects/index.html"' in home, "home: link to the end-of-year projects page")
for sec in ["description", "about", "rules", "tree", "programme", "projects", "official", "after"]:
    check(f'id="{sec}"' in home, f"home: #{sec} section present")
check("<!-- programme:start -->" in home, "home: programme table present")
for token in ["sante", "ii", "rr", "theory", "vision", "genai"]:
    check(f'data-path="{token}"' in home, f"home: button for {token}")
    check(f'.tree[data-path="{token}"]' in read(ROOT / "assets/paper.css"), f"paper.css: dim rule for {token}")

# Routes are feasible programmes: 8 modules, >= 4 in S1, >= 3 in S2, >= 2 Learning, >= 2 Modelling.
for route in ["theory", "vision", "genai"]:
    slugs = [m.group(2) for m in re.finditer(
        r'<li data-p="([^"]*)"><a href="courses/([\w-]+)/', tree_html) if route in m.group(1).split()]
    cs =[BY_SLUG[s] for s in dict.fromkeys(slugs)]
    ects = sum(c["ects"] for c in cs)
    s1 = sum(1 for c in cs if c["semester"] == 1)
    s2 = sum(1 for c in cs if c["semester"] == 2)
    learn = sum(1 for c in cs if "Learning" in c["types"])
    model = sum(1 for c in cs if "Modelling" in c["types"])
    check(len(cs) == 8 and ects >= 40, f"route {route}: 8 modules, >= 40 ECTS", f"{len(cs)} modules, {ects:g} ECTS")
    check(s1 >= 4 and s2 >= 3, f"route {route}: >= 4 in S1 and >= 3 in S2", f"S1 {s1}, S2 {s2}")
    check(learn >= 2 and model >= 2, f"route {route}: >= 2 Learning and >= 2 Modelling", f"L {learn}, M {model}")

# Track buttons highlight exactly the courses carrying the label.
for token, name in [("sante", "Santé"), ("ii", "I&I"), ("rr", "RR")]:
    lit = {m.group(2) for m in re.finditer(r'<li data-p="([^"]*)"><a href="courses/([\w-]+)/', tree_html)
           if token in m.group(1).split()}
    want = {c["slug"] for c in CATALOG if name in c["tracks"]}
    check(lit == want, f"track {name}: button highlights the labelled courses", f"{sorted(lit ^ want)}")

# --- Assets ------------------------------------------------------------------
css = read(ROOT / "assets/paper.css")
check(".def" in css and ".thm" in css and ".note" in css, "paper.css: .def/.thm/.note styles")
check("prefers-color-scheme: dark" in css and 'data-theme="dark"' in css, "paper.css: dark blocks present")
js = read(ROOT / "assets/theme.js")
check("localStorage" in js and '"mva-theme"' in js, "theme.js: localStorage toggle with the MVA key")

# --- Third-party math: pinned KaTeX + subresource integrity -------------------
KATEX_JS = "https://cdn.jsdelivr.net/npm/katex@0.19.0/dist/katex.min.js"
KATEX_CSS = "https://cdn.jsdelivr.net/npm/katex@0.19.0/dist/katex.min.css"
KATEX_JS_SRI = "sha384-QFFtAGzvvj+bfgCGxXJlNZZR1nXEZgvG8tDLCCY1F19xl20WlfTYgguB4VcNdxYk"
KATEX_CSS_SRI = "sha384-3rdsX6e5mueWyoweR9NIVmtEsUkokpBT/0ALqKKIBMr9j4qhHkaIkAcGgsE6uVlp"
published = [home_path, ph] + list((ROOT / "courses").glob("*/index.html"))
for page in published:
    if not page.is_file():
        continue
    h = read(page)
    rel = str(page.relative_to(ROOT))
    check("katex@latest" not in h, f"{rel}: KaTeX is not the floating @latest tag")
    if "cdn.jsdelivr.net/npm/katex" not in h:
        continue
    check(KATEX_JS in h and KATEX_JS_SRI in h and 'crossorigin="anonymous"' in h,
          f"{rel}: pinned KaTeX script with integrity")
    check(KATEX_CSS in h and KATEX_CSS_SRI in h, f"{rel}: pinned KaTeX stylesheet with integrity")
for qmd in list((ROOT / "courses").glob("*/index.qmd")) + [pq]:
    if qmd.is_file() and "html-math-method" in read(qmd):
        check("katex@latest" not in read(qmd) and KATEX_JS in read(qmd),
              f"{qmd.relative_to(ROOT)}: Quarto math URL pinned")

# --- Specs index honesty -----------------------------------------------------
readme = read(ROOT / "specs/README.md")
for spec in sorted((ROOT / "specs").glob("*.md")):
    if spec.name in {"README.md", "_template-module.md"}:
        continue
    check(f"`{spec.stem}`" in readme, f"specs index: {spec.stem} listed")

# --- Hours and progression, airy prose ---------------------------------------
prog = subprocess.run([sys.executable, str(ROOT / "tools/check_progression.py")],
                      capture_output=True, text=True)
check(prog.returncode == 0, "check_progression: every science and refresher page passes",
      prog.stdout.strip().splitlines()[-1] if prog.stdout.strip() else prog.stderr[-200:])
air = subprocess.run([sys.executable, str(ROOT / "tools/check_airiness.py")],
                     capture_output=True, text=True)
check(air.returncode == 0, "check_airiness: every page passes A1-A3 (specs/front-redesign.md)",
      "; ".join(l for l in air.stdout.splitlines() if "FAIL" in l)[:300])

# --- Report ------------------------------------------------------------------
total = passed + len(failures)
print(f"check_gates: {passed}/{total} checks passed")
for f in failures[:200]:
    print(f"FAIL  {f}")
if len(failures) > 200:
    print(f"... and {len(failures) - 200} more")
sys.exit(1 if failures else 0)
