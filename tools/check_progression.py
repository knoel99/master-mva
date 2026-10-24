#!/usr/bin/env python3
"""Gate for specs/hours-and-progression.md.

Run from the repository root:
    python3 tools/check_progression.py              # every science module
    python3 tools/check_progression.py s2-kernel-methods    # some modules, with a report
Exit code 0 = every rule holds.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / "data/catalog-2026-2027.json").read_text(encoding="utf-8"))["courses"]
# Pages without a session plan: kind "non-science" in the catalogue (specs/non-science-pages.md).
NON_SCIENCE = {c["slug"] for c in CATALOG if c["kind"] == "non-science"}
PLAN_HOURS = {c["slug"]: c["plan_hours"] for c in CATALOG if c["kind"] != "non-science"}
BAND = (100, 320)  # prose words per in-class hour (R2)

TOTAL_RE = re.compile(r"\*\*(\d+(?:\.\d+)?) h (?:in class|of guided self-study)")
CHAPTER_RE = re.compile(r"^## (\d+)\. (.*?)\{#(ch\d+)[^}]*\}\s*$", re.M)
EX_RE = re.compile(r"^(\d+)\.\s+\*\*(★{1,3})\s", re.M)
EX_ANY_RE = re.compile(r"^(\d+)\.\s+\*\*", re.M)
CH_REF_RE = re.compile(r"\bch\. ?(\d+)")


def prose_words(text: str) -> int:
    text = re.sub(r"^(```|~~~).*?^\1", "", text, flags=re.S | re.M)
    text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.S)
    text = re.sub(r"\$[^$\n]*\$", "", text)
    return len(re.findall(r"[A-Za-z]{2,}", text))


def section(body: str, start: str) -> str:
    i = body.find(start)
    if i < 0:
        return ""
    m = re.compile(r"^#{2,3} ", re.M).search(body, i + len(start))
    return body[i: m.start() if m else len(body)]


def check_module(slug: str) -> tuple[list[str], str]:
    errs: list[str] = []
    src = (ROOT / "courses" / slug / "index.qmd").read_text(encoding="utf-8")
    body = src.split("\n---\n", 1)[1]

    # R3 — chapters numbered in page order, id chN
    chapters = CHAPTER_RE.findall(body)
    nums = [int(n) for n, _, _ in chapters]
    if not chapters:
        errs.append("no numbered chapters '## N. Title {#chN}'")
    elif nums != list(range(nums[0], nums[0] + len(nums))):
        errs.append(f"chapters not consecutive: {nums}")
    for n, _, cid in chapters:
        if cid != f"ch{n}":
            errs.append(f"chapter {n} has id {cid}")

    # Internal anchors resolve
    ids = set(re.findall(r"\{#([\w-]+)", body)) | set(re.findall(r'id="([\w-]+)"', body))
    for target in sorted(set(re.findall(r"\]\(#([\w-]+)\)", body))):
        if target not in ids:
            errs.append(f"broken internal link #{target}")

    # R1 — session plan
    plan = section(body, "### Session plan {#sessions}")
    if not plan:
        errs.append("missing '### Session plan {#sessions}'")
        return errs, ""
    m = TOTAL_RE.search(plan)
    if not m:
        errs.append("session plan: missing bold '**N h in class' total")
        return errs, ""
    total = float(m.group(1))
    if slug in PLAN_HOURS and abs(total - PLAN_HOURS[slug]) > 1e-6:
        errs.append(f"session plan total {total:g} h differs from the catalogue volume {PLAN_HOURS[slug]:g} h")
    rows = [r for r in plan.splitlines() if re.match(r"^\|\s*\d+\s*\|", r)]
    hours, levels, firsts, taught = 0.0, [], [], set()
    for r in rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if len(cells) < 4:
            errs.append(f"session row too short: {r[:60]}")
            continue
        hm = re.match(r"(\d+(?:\.\d+)?)\s*h", cells[1])
        lm = re.match(r"([123])", cells[2])
        if not hm or not lm:
            errs.append(f"session {cells[0]}: hours or level unreadable")
            continue
        hours += float(hm.group(1))
        levels.append(int(lm.group(1)))
        refs = [int(x) for x in CH_REF_RE.findall(cells[3])]
        if refs:
            firsts.append(refs[0])
            taught.update(refs)
    if abs(hours - total) > 1e-6:
        errs.append(f"session hours sum to {hours:g}, total says {total:g}")
    if any(b < a for a, b in zip(levels, levels[1:])):
        errs.append(f"levels decrease: {levels}")
    if any(b < a for a, b in zip(firsts, firsts[1:])):
        errs.append(f"sessions go back in the page: first chapters {firsts}")
    self_m = re.search(r"\*\*Self-study, outside the .*", plan)
    self_study = set(int(x) for x in CH_REF_RE.findall(self_m.group(0))) if self_m else set()
    missing = [n for n in nums if n not in taught and n not in self_study]
    if missing:
        errs.append(f"chapters neither in a session nor in self-study: {missing}")
    if self_study and not self_m.group(0).count("≈"):
        errs.append("self-study line gives no time estimate (≈ N h)")

    # R2 — calibration on the chapters taught in class
    texts = {int(n): t for n, t in re.findall(
        r"^## (\d+)\. .*?\n(.*?)(?=^## |\Z)", body, flags=re.S | re.M)}
    words = sum(prose_words(texts[n]) for n in taught if n in texts)
    per_h = words / total if total else 0
    if not BAND[0] <= per_h <= BAND[1]:
        errs.append(f"in-class prose {per_h:.0f} words/h outside {BAND}")

    # R4 — graded exercises, sorted
    ex = section(body, "## Exercises")
    all_ex = EX_ANY_RE.findall(ex)
    graded = EX_RE.findall(ex)
    if len(graded) != len(all_ex):
        errs.append(f"{len(all_ex) - len(graded)} exercises without a ★ level")
    stars = [len(s) for _, s in graded]
    if any(b < a for a, b in zip(stars, stars[1:])):
        errs.append(f"exercise levels not sorted: {stars}")

    report = (f"{total:g} h, {len(rows)} sessions, levels {levels}, "
              f"{per_h:.0f} words/h in class, self-study ch. {sorted(self_study)}, "
              f"exercises {stars}")
    return errs, report


def main(argv: list[str]) -> int:
    slugs = argv or sorted(p.parent.name for p in (ROOT / "courses").glob("*/index.qmd")
                           if p.parent.name not in NON_SCIENCE)
    failed = 0
    for slug in slugs:
        errs, report = check_module(slug)
        if errs:
            failed += 1
            print(f"FAIL {slug}")
            for e in errs:
                print(f"     - {e}")
        elif argv:
            print(f"ok   {slug}: {report}")
    print(f"check_progression: {len(slugs) - failed}/{len(slugs)} modules pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
