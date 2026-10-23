#!/usr/bin/env python3
"""Checks owned by the coherence and end-of-year projects work.

Run from the repository root:

    python3 tools/check_project_sections.py

Exit 0 when every science source without a TODO placeholder has a complete
projects section, the end-of-year page covers each home-page route and each
official track, the evolution note names the commits on master and on
ccr-35a7ca30-pszhhr, and the coherence note names every catalogue slug and
no UE code.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / "data/catalog-2026-2027.json").read_text(encoding="utf-8"))
COURSES = CATALOG["courses"]
BY_SLUG = {c["slug"]: c for c in COURSES}
HISTORY_REFS = ("master", "ccr-35a7ca30-pszhhr")
EVOLUTION = ROOT / "specs/commit-evolution-2026-10.md"
COHERENCE = ROOT / "specs/coherence-objectives.md"
PROJECTS_QMD = ROOT / "projects/index.qmd"
PROJECTS_HTML = ROOT / "projects/index.html"
ROUTE_IDS = ("route-theory", "route-vision", "route-genai")
TRACK_IDS = ("track-sante", "track-ii", "track-rr")
PROGRAMMES = ROUTE_IDS + TRACK_IDS
SECTION_H3 = (
    "### Courses",
    "### Research question",
    "### Milestones",
    "### Deliverables",
    "### Evaluation",
    "### Variants",
)

failures: list[str] = []
passed = 0


def check(ok: bool, label: str, detail: str = "") -> None:
    global passed
    if ok:
        passed += 1
    else:
        failures.append(f"{label}{': ' + detail if detail else ''}")


def subsection(src: str, start: str) -> str:
    i = src.find(start)
    if i < 0:
        return ""
    m = re.compile(r"^#{2,3} ", re.M).search(src, i + len(start))
    return src[i: m.start() if m else len(src)]


def h2_block(src: str, anchor: str) -> str:
    m = re.search(rf"^## .+\{{#{re.escape(anchor)}\}}\s*$", src, re.M)
    if not m:
        return ""
    nxt = re.compile(r"^## ", re.M).search(src, m.end())
    return src[m.start(): nxt.start() if nxt else len(src)]


def top_points(exam: str) -> list[int | None]:
    pts = []
    for line in exam.splitlines():
        if re.match(r"^\d+\.\s+\*\*", line):
            m = re.search(r"\((\d+)\s+points?\)", line, re.I)
            pts.append(int(m.group(1)) if m else None)
    return pts


def rubric_weights(text: str) -> list[float]:
    weights = []
    for line in text.splitlines():
        if not line.strip().startswith("|") or "---" in line or "Weight" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        m = re.search(r"(\d+(?:\.\d+)?)\s*%", cells[1])
        if m:
            weights.append(float(m.group(1)))
    return weights


def rev_list(ref: str) -> list[str]:
    out = subprocess.run(
        ["git", "rev-list", ref], cwd=ROOT, capture_output=True, text=True
    )
    check(out.returncode == 0, f"git rev-list {ref}", out.stderr.strip()[:200])
    return out.stdout.split()


def check_science_pages() -> None:
    full = skeleton = missing = 0
    for course in COURSES:
        if course["kind"] != "science":
            continue
        path = ROOT / "courses" / course["slug"] / "index.qmd"
        if not path.is_file():
            missing += 1
            continue
        src = path.read_text(encoding="utf-8")
        if "TODO" in src:
            skeleton += 1
            continue
        full += 1
        cid = course["slug"]
        check(
            "## Projects and assessment {#projects}" in src,
            f"{cid}: projects section",
        )
        if "## Projects and assessment {#projects}" not in src:
            continue
        body = src.split("## Projects and assessment {#projects}", 1)[1].split("\n## ", 1)[0]
        solo = len(re.findall(r"^\d+\.\s+\*\*\[Solo", body, re.M))
        group = len(re.findall(r"^\d+\.\s+\*\*\[Group", body, re.M))
        exam = subsection(body, "### Written exam")
        questions = len(re.findall(r"^\d+\.\s", exam, re.M))
        points = top_points(exam)
        rubric = subsection(body, "### Grading rubric")
        weights = rubric_weights(rubric)
        paper = ("paper study" in body.lower()) or ("Paper:" in body)
        check(solo >= 2, f"{cid}: >= 2 solo subjects", f"found {solo}")
        check(group >= 2, f"{cid}: >= 2 group subjects", f"found {group}")
        check(questions >= 3, f"{cid}: >= 3 exam questions", f"found {questions}")
        check(
            points and all(p is not None for p in points) and sum(points) == 20,
            f"{cid}: exam points sum to 20",
            str(points),
        )
        check(abs(sum(weights) - 100) < 0.1, f"{cid}: rubric weights sum to 100", str(weights))
        check(paper, f"{cid}: a named paper subject")
        check(
            src.find("## Exercises {#ex}")
            < src.find("## Projects and assessment")
            < src.find("## References {#refs}"),
            f"{cid}: projects section between exercises and references",
        )
    print(f"science pages: {full} substantial, {skeleton} skeleton, {missing} missing")


def check_projects_page() -> None:
    check(PROJECTS_QMD.is_file(), "projects/index.qmd exists")
    check(PROJECTS_HTML.is_file(), "projects/index.html exists")
    if not PROJECTS_QMD.is_file():
        return
    src = PROJECTS_QMD.read_text(encoding="utf-8")
    check("TODO" not in src, "projects page: no TODO")
    links = re.findall(r"\.\./courses/([\w-]+)/index\.html", src)
    unknown = sorted({s for s in links if s not in BY_SLUG})
    check(not unknown, "projects page: links are catalogue slugs", ", ".join(unknown))
    absent = sorted(
        {
            s
            for s in links
            if s in BY_SLUG and not (ROOT / "courses" / s / "index.html").is_file()
        }
    )
    check(not absent, "projects page: every linked course has index.html", ", ".join(absent))
    for anchor in PROGRAMMES:
        block = h2_block(src, anchor)
        check(bool(block), f"projects page: section #{anchor}")
        if not block:
            continue
        for heading in SECTION_H3:
            check(heading in block, f"#{anchor}: {heading}")
        check("**[Solo" in block, f"#{anchor}: solo variant")
        check("**[Group" in block, f"#{anchor}: group variant")
        check(len(re.findall(r"^\d+\.\s", block, re.M)) >= 4, f"#{anchor}: at least 4 milestones")
        check(re.search(r"\.\./courses/s1-[\w-]+/index\.html", block), f"#{anchor}: a semester 1 link")
        check(re.search(r"\.\./courses/s2-[\w-]+/index\.html", block), f"#{anchor}: a semester 2 link")
        check("100 %" in block or "100%" in block, f"#{anchor}: evaluation weights mention 100%")
    home = ROOT / "index.html"
    home_txt = home.read_text(encoding="utf-8") if home.is_file() else ""
    check('href="projects/index.html"' in home_txt, "home page links to projects/index.html")


def check_evolution() -> None:
    check(EVOLUTION.is_file(), "commit-evolution note exists")
    if not EVOLUTION.is_file():
        return
    text = EVOLUTION.read_text(encoding="utf-8")
    known: set[str] = set()
    for ref in HISTORY_REFS:
        for sha in rev_list(ref):
            known.add(sha)
            check(sha[:7] in text, f"evolution note names {sha[:7]} ({ref})")
    mentioned = re.findall(r"`([0-9a-f]{7,40})`", text)
    check(bool(mentioned), "evolution note cites commit hashes in backticks")
    for short in mentioned:
        match = [sha for sha in known if sha.startswith(short) or short.startswith(sha)]
        check(len(match) == 1, f"evolution hash `{short}` is one commit on master or the WIP branch", str(len(match)))


def check_coherence() -> None:
    check(COHERENCE.is_file(), "coherence note exists")
    if not COHERENCE.is_file():
        return
    text = COHERENCE.read_text(encoding="utf-8")
    check(not re.search(r"\bUE[\s-]*\d", text), "coherence note: no UE code")
    for slug in BY_SLUG:
        check(
            re.search(rf"(?<![\w-]){re.escape(slug)}(?![\w-])", text) is not None,
            f"coherence note names {slug}",
        )
    extra = sorted(
        {
            m.group(0)
            for m in re.finditer(r"(?<![\w-])s[0-3]-[\w-]+", text)
            if m.group(0) not in BY_SLUG
        }
    )
    check(not extra, "coherence note: no unknown course slug", ", ".join(extra))


def main() -> int:
    check_science_pages()
    check_projects_page()
    check_evolution()
    check_coherence()
    total = passed + len(failures)
    print(f"check_project_sections: {passed}/{total} checks passed")
    for item in failures:
        print(f"FAIL  {item}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
