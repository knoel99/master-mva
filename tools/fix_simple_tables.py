#!/usr/bin/env python3
"""Turn misaligned Pandoc simple tables into pipe tables.

Usage (repository root):
    python3 tools/fix_simple_tables.py <slug> [<slug>…]   # rewrite in place
    python3 tools/fix_simple_tables.py --check <slug>…    # only report

A simple table is a header line, a rule of dash groups, rows, and a blank
line. Pandoc cuts each row at the column positions of the dash rule, so a
cell that starts one character too far left or right loses a character to
its neighbour — a formula then shows a stray "$". A table is rewritten only
when one of its lines has a non-space character just before a column start,
and only if every line splits into exactly one cell per column on runs of
two or more spaces, or cut at the nearest spaces around the column starts
(such rows are printed for review); otherwise it is reported and left alone.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULE = re.compile(r"^(\s*)(-+)((?:\s+-+)+)\s*$")


def columns(rule: str):
    return [m.start() for m in re.finditer(r"-+", rule)]


def misaligned(lines, starts) -> bool:
    for l in lines:
        for s in starts[1:]:
            if s < len(l) and l[s - 1] != " ":
                return True
    return False


def split(line: str, starts):
    """Cells of one line: split on runs of 2+ spaces when that gives one cell
    per column, else cut at the column starts moved to the nearest space."""
    n = len(starts)
    cells = re.split(r"\s{2,}", line.strip())
    if len(cells) == n:
        return cells
    cuts = []
    for s in starts[1:]:
        if s >= len(line) or line[s - 1] == " ":
            cuts.append(s)
            continue
        for k in range(1, 5):
            if s + k <= len(line) and line[s + k - 1] == " ":
                cuts.append(s + k)
                break
            if line[s - k - 1] == " ":
                cuts.append(s - k)
                break
        else:
            return None
    bounds = [0] + cuts + [len(line)]
    cells = [line[a:b].strip() for a, b in zip(bounds, bounds[1:])]
    if cells[0]:  # an empty first header cell is normal; anything else deserves a look
        print(f"  check this row (cut by position): {' | '.join(cells)}")
    return cells


def fix(src: str, slug: str, write: bool):
    lines = src.split("\n")
    out, i, changed, problems = [], 0, 0, []
    in_code = False
    while i < len(lines):
        l = lines[i]
        if l.strip().startswith(("```", "~~~")):
            in_code = not in_code
        m = None if in_code else RULE.match(l)
        # simple table: header line, rule, rows until blank line (no leading rule)
        if m and i > 0 and lines[i - 1].strip() and not (i + 1 < len(lines) and RULE.match(lines[i + 1])):
            head = lines[i - 1]
            j = i + 1
            ind0 = len(m.group(1))
            while (j < len(lines) and lines[j].strip() and not RULE.match(lines[j])
                   and len(lines[j]) - len(lines[j].lstrip()) >= min(ind0, 2)):
                j += 1
            rows = lines[i + 1:j]
            starts = columns(l)
            if rows and misaligned([head] + rows, starts):
                n = len(starts)
                cells = [split(r, starts) for r in [head] + rows]
                if all(cells):
                    ind = " " * max(0, len(m.group(1)) - 2)
                    out[-1:] = [ind + "| " + " | ".join(cells[0]) + " |",
                                ind + "|" + "|".join("---" for _ in range(n)) + "|"]
                    out += [ind + "| " + " | ".join(c) + " |" for c in cells[1:]]
                    changed += 1
                    i = j
                    continue
                problems.append(i)
        out.append(l)
        i += 1
    for p in problems:
        print(f"{slug}: line {p + 1}: misaligned table not converted (cells do not split cleanly)")
    return "\n".join(out), changed


def main(args):
    write = "--check" not in args
    for slug in [a for a in args if a != "--check"]:
        path = ROOT / "courses" / slug / "index.qmd"
        src = path.read_text(encoding="utf-8")
        new, n = fix(src, slug, write)
        if n and write:
            path.write_text(new, encoding="utf-8")
        print(f"{slug}: {n} table(s) {'converted' if write else 'to convert'}")


if __name__ == "__main__":
    main(sys.argv[1:])
