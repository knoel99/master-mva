#!/usr/bin/env python3
"""Tag each exercise with its level and sort the list by level (stable).

Usage (repository root):
    python3 tools/grade_exercises.py <module> <level of exercise 1>,<level of 2>,...
    python3 tools/grade_exercises.py s1-convex-optimization 1,1,1,2,2,1,2,2,2,2,3,3

Levels: 1 = ★ apply the course, 2 = ★★ combine or prove a short result,
3 = ★★★ open-ended or research-flavoured (specs/hours-and-progression.md, R4).
Existing ★ tags are replaced. Prints the old→new numbering so that mentions
such as "exercise 7" elsewhere in the page can be updated by hand.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ITEM_RE = re.compile(r"^(\d+)\.(\s+)\*\*(?:★{1,3}\s+)?", re.M)


def main(slug: str, levels: list[int]) -> None:
    path = ROOT / "courses" / slug / "index.qmd"
    src = path.read_text(encoding="utf-8")
    start = src.index("\n## Exercises")
    head_end = src.index("\n", start + 1) + 1
    end = src.index("\n## ", head_end)
    section = src[head_end:end]
    starts = [m.start() for m in ITEM_RE.finditer(section)]
    if len(starts) != len(levels):
        sys.exit(f"{len(starts)} exercises found, {len(levels)} levels given")
    if not set(levels) <= {1, 2, 3}:
        sys.exit("levels must be 1, 2 or 3")
    intro, items = section[:starts[0]], []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(section)
        items.append(section[s:e])
    order = sorted(range(len(items)), key=lambda i: levels[i])
    out = []
    for new, old in enumerate(order, 1):
        item = items[old]
        if not item.endswith("\n"):
            item += "\n"
        width = len(str(int(ITEM_RE.match(item).group(1))))
        item = ITEM_RE.sub(lambda m: f"{new}.{' ' * max(1, len(m.group(2)) + width - len(str(new)))}**{'★' * levels[old]} ",
                           item, count=1)
        out.append(item)
    body = intro + "".join(out)
    if not section.endswith("\n"):
        body = body.rstrip("\n")
    path.write_text(src[:head_end] + body + src[end:], encoding="utf-8")
    moves = {old + 1: new for new, old in enumerate(order, 1) if old + 1 != new}
    print(f"{slug}: exercises graded {sorted(levels)}; renumbered old→new {moves or 'none'}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], [int(x) for x in sys.argv[2].split(",")])
