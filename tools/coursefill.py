#!/usr/bin/env python3
"""Hour grid and page check for the sixteen thin science and refresher pages.

The catalogue decides the hours. This module prints the session plan a page
must contain, and refuses a page whose plan, chapters, or project headings
disagree with that grid. It does not write course files.

    python3 tools/coursefill.py --plan s1-convex-optimization
    python3 tools/coursefill.py --check s1-convex-optimization
    python3 tools/coursefill.py --self-test
"""

import fcntl
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "catalog-2026-2027.json"

FILL = (
    "s0-refresher-linear-algebra-optimization",
    "s0-refresher-python-scientific-computing",
    "s1-convex-optimization",
    "s1-deep-learning",
    "s1-distributed-optimization",
    "s1-extreme-values",
    "s1-foundations-llms",
    "s1-geometric-data-analysis",
    "s1-optimal-transport-ml",
    "s1-stochastic-calculus-ml",
    "s1-tda-imaging-ml",
    "s2-graphical-models-discrete",
    "s2-interactions",
    "s2-reinforcement-learning",
    "s2-representation-learning-medical",
    "s2-stopping-times-online",
)

OWNER_LEAVE = ("s1-turing-seminar-ai-safety",)

EXPECTED_BOLD = {
    "s0-refresher-linear-algebra-optimization": "**12 h of guided self-study = 4 steps of 3 h.**",
    "s0-refresher-python-scientific-computing": "**12 h of guided self-study = 4 steps of 3 h.**",
    "s1-convex-optimization": "**21 h in class = 7 sessions of 3 h.**",
    "s1-extreme-values": "**25 h in class = 8 sessions (7 x 3 h + 1 x 4 h).**",
    "s1-geometric-data-analysis": "**21 h in class = 6 sessions (3 x 3 h + 1 x 5 h + 1 x 3 h + 1 x 4 h).**",
    "s1-optimal-transport-ml": "**18 h in class = 6 sessions of 3 h.**",
    "s1-foundations-llms": "**24 h in class (assumed) = 8 sessions of 3 h.**",
    "s2-reinforcement-learning": "**24 h in class (assumed) = 8 sessions of 3 h.**",
}


def load():
    return {c["slug"]: c for c in json.loads(CATALOG.read_text(encoding="utf-8"))["courses"]}


def split_component(hours: int) -> tuple[int, ...]:
    """Join a remainder onto the last session of this component."""
    q, r = divmod(int(hours), 3)
    if r == 0:
        return tuple(3 for _ in range(q))
    if q == 0:
        return (r,)
    return tuple(3 for _ in range(q - 1)) + (3 + r,)


def session_hours(record: dict) -> tuple[int, ...]:
    if record["hours_status"] == "self-study":
        return (3, 3, 3, 3)
    official = record.get("hours_official") or {}
    parts = [official.get(k) or 0 for k in ("lecture", "td", "tp", "project")]
    if record["hours_status"] == "assumed" or not any(parts):
        return split_component(record["plan_hours"])
    hours: list[int] = []
    for part in parts:
        if part:
            hours.extend(split_component(part))
    return tuple(hours)


def levels_for(n: int, refresher: bool) -> tuple[int, ...]:
    if refresher:
        if n != 4:
            raise ValueError(f"refresher grid has {n} sessions, expected 4")
        return (1, 1, 2, 3)
    out = []
    for i in range(n):
        if i < n // 3:
            out.append(1)
        elif i < (2 * n) // 3:
            out.append(2)
        else:
            out.append(3)
    return tuple(out)


def bold_line(record: dict, hours: tuple[int, ...]) -> str:
    total = int(record["plan_hours"])
    if record["hours_status"] == "self-study":
        return f"**{total:g} h of guided self-study = {len(hours)} steps of 3 h.**"
    where = "in class (assumed)" if record["hours_status"] == "assumed" else "in class"
    if len(set(hours)) == 1:
        body = f"{len(hours)} sessions of {hours[0]} h"
    else:
        groups = []
        run = 1
        for prev, cur in zip(hours, hours[1:]):
            if cur == prev:
                run += 1
            else:
                groups.append(f"{run} x {prev} h")
                run = 1
        groups.append(f"{run} x {hours[-1]} h")
        body = f"{len(hours)} sessions ({' + '.join(groups)})"
    return f"**{total:g} h {where} = {body}.**"


def practice(n: int) -> tuple[tuple[int, ...], ...]:
    base, extra = divmod(10, n)
    counts = [base + 1] * extra + [base] * (n - extra)
    rows = []
    nxt = 1
    for count in counts:
        rows.append(tuple(range(nxt, nxt + count)))
        nxt += count
    return tuple(rows)


def plan_markdown(record: dict) -> str:
    hours = session_hours(record)
    refresher = record["kind"] == "refresher"
    levels = levels_for(len(hours), refresher)
    dealt = practice(len(hours))
    n = len(hours)
    lines = [
        "### Session plan {#sessions}",
        "",
        bold_line(record, hours),
        "",
        "The split into sessions is a proposal.",
        "",
        "| Session | Hours | Level | Content | Practice |",
        "| --- | --- | --- | --- | --- |",
    ]
    for i, (h, level, exs) in enumerate(zip(hours, levels, dealt), start=1):
        practice_cell = ", ".join(f"Ex. {k}" for k in exs)
        lines.append(f"| {i} | {h} h | {level} | ch. {i - 1} | {practice_cell} |")
    lines.append("")
    lines.append(
        f"**Self-study, outside the {int(record['plan_hours'])} h** "
        f"(about 4 h in total): ch. {n} Research directions and open problems (≈ 4 h)."
    )
    return "\n".join(lines) + "\n"


def check_page(slug: str, courses: dict) -> list[str]:
    if slug in OWNER_LEAVE:
        return [f"{slug} is left untouched"]
    if slug not in FILL:
        return [f"{slug} is outside the sixteen"]
    path = ROOT / "courses" / slug / "index.qmd"
    if not path.exists():
        return ["missing index.qmd"]
    text = path.read_text(encoding="utf-8")
    errs = []
    if "TODO" in text:
        errs.append("TODO remains")
    if re.search(r"français", text, re.I):
        errs.append("the source contains français")
    record = courses[slug]
    plan = plan_markdown(record)
    if "### Session plan {#sessions}" not in text:
        errs.append("missing session-plan heading")
    for line in plan.splitlines():
        if line.startswith("| ") and not line.startswith("| ---") and not line.startswith("| Session"):
            if line not in text:
                errs.append(f"session row missing or edited: {line}")
        if line.startswith("**") and line not in text:
            errs.append(f"required line missing: {line}")
    hours = session_hours(record)
    last = len(hours)
    for i in range(last + 1):
        if not re.search(rf"^## {i}\. .+\{{#ch{i}", text, re.M):
            errs.append(f"missing chapter {i}")
    if slug_is_science(record):
        projects = text.split("## Projects and assessment {#projects}", 1)
        if len(projects) < 2:
            errs.append("missing projects heading")
        else:
            block = projects[1].split("\n## ", 1)[0]
            solos = len(re.findall(r"^\d+\.\s+\*\*\[Solo", block, re.M))
            groups = len(re.findall(r"^\d+\.\s+\*\*\[Group", block, re.M))
            exam = block.split("### Written exam", 1)
            questions = len(re.findall(r"^\d+\.\s", exam[1], re.M)) if len(exam) > 1 else 0
            if solos < 2:
                errs.append(f"solo subjects {solos}")
            if groups < 2:
                errs.append(f"group subjects {groups}")
            if questions < 3:
                errs.append(f"exam questions {questions}")
    return errs


def slug_is_science(record: dict) -> bool:
    return record["kind"] == "science"


def render_locked(slug: str) -> None:
    """Run tools/render.py for one slug. One render at a time."""
    if slug not in FILL:
        raise SystemExit(f"{slug} is outside the sixteen")
    lock_path = Path("/tmp/coursefill-render.lock")
    with lock_path.open("w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        subprocess.check_call(
            [sys.executable, str(ROOT / "tools" / "render.py"), slug],
            cwd=ROOT,
        )


def self_test(courses: dict) -> list[str]:
    errs = []
    for slug in FILL:
        record = courses[slug]
        hours = session_hours(record)
        if sum(hours) != record["plan_hours"]:
            errs.append(f"{slug} hours {hours} sum {sum(hours)} != {record['plan_hours']}")
        line = bold_line(record, hours)
        if slug in EXPECTED_BOLD and line != EXPECTED_BOLD[slug]:
            errs.append(f"{slug} bold {line}")
        elif slug not in EXPECTED_BOLD and line != f"**{int(record['plan_hours'])} h in class = {len(hours)} sessions of 3 h.**":
            errs.append(f"{slug} unexpected bold {line}")
        if record["kind"] == "refresher" and levels_for(len(hours), True) != (1, 1, 2, 3):
            errs.append(f"{slug} levels")
    if "s1-turing-seminar-ai-safety" in FILL:
        errs.append("turing seminar is in the fill set")
    return errs


def main(argv: list[str]) -> int:
    courses = load()
    if len(argv) == 1 and argv[0] == "--self-test":
        errs = self_test(courses)
        if errs:
            print("\n".join(errs))
            return 1
        print(f"coursefill: {len(FILL)} grids match the catalogue")
        return 0
    if len(argv) == 2 and argv[0] == "--plan":
        print(plan_markdown(courses[argv[1]]), end="")
        return 0
    if len(argv) == 2 and argv[0] == "--render":
        render_locked(argv[1])
        return 0
    if len(argv) == 2 and argv[0] == "--check":
        errs = check_page(argv[1], courses)
        if errs:
            print(f"FAIL {argv[1]}")
            for err in errs:
                print(f" - {err}")
            return 1
        print(f"ok {argv[1]}")
        return 0
    print("usage: coursefill.py --self-test | --plan SLUG | --check SLUG | --render SLUG", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
