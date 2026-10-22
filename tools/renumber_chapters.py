#!/usr/bin/env python3
"""Reorder the numbered chapters of a module and renumber every reference.

Usage (repository root):
    python3 tools/renumber_chapters.py <module> <new order of old numbers>
    python3 tools/renumber_chapters.py s1-convex-optimization 0,1,2,3,9,4,5,6,7,8

The order lists the *old* chapter numbers in their new page order; the first
one gets the lowest existing number. Rewritten (outside code blocks and math):
headings `## N.` / `### N.k.`, ids `{#chN}`, links `#chN` (also from other
modules' pages), the Contents list, and numbers that follow a keyword such as
`ch.`, `chapter`, `section`, `Theorem`, `Definition`, `example` — including
lists like `ch. 2 and 3` or `sections 9.2–9.5`, and parenthesised `(9.2)`.
Anything that still looks like an old chapter-section number is printed for a
manual check. Run `python3 tools/check_progression.py <module>` afterwards.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEYWORDS = (r"ch\.|chs\.|chapters?|sections?|§|definitions?|def\.|theorems?|thm\.|"
            r"propositions?|props?\.|lemmas?|corollar(?:y|ies)|examples?|remarks?|"
            r"figures?|fig\.|tables?|algorithms?|equations?|eq\.|notes?|boxes|box|"
            r"recap|subsections?|paragraphs?|models?|cf\.")
NUM = r"\d+(?:\.\d+)*"
LIST = rf"{NUM}(?:\s*(?:,|and|or|to|–|-|&)\s*{NUM})*"
KW_RE = re.compile(rf"(?i)(?<![\w.])({KEYWORDS})(\s*\(?)\s*({LIST})")
PAREN_RE = re.compile(rf"\((?:cf\.\s*)?({NUM}\.\d+)\)")
CITATION_RE = re.compile(r"\b(?:19|20)\d\d\b|et al\.|\*[^*]+\*,[^.]*$")
PROTECT_RE = re.compile(r"(?m:^(?:```|~~~)[\s\S]*?^(?:```|~~~))|```.*?```|\$\$.*?\$\$|\$[^$\n]*\$", re.S)


def remap_number(num: str, mapping: dict[int, int]) -> str:
    head, _, rest = num.partition(".")
    n = int(head)
    if n in mapping:
        return f"\x00{mapping[n]}\x00" + (f".{rest}" if rest else "")
    return num


def remap_list(text: str, mapping: dict[int, int]) -> str:
    return re.sub(NUM, lambda m: remap_number(m.group(0), mapping), text)


def rewrite_prose(text: str, mapping: dict[int, int], slug: str) -> str:
    text = re.sub(r"^(#{2,3} )(\d+)((?:\.\d+)*\.)",
                  lambda m: m.group(1) + remap_number(m.group(2), mapping) + m.group(3),
                  text, flags=re.M)
    text = re.sub(r"#ch(\d+)\b",
                  lambda m: f"#ch\x00{mapping.get(int(m.group(1)), int(m.group(1)))}\x00",
                  text)
    text = re.sub(r"(\[)(\d+)(\. )", lambda m: m.group(1) + remap_number(m.group(2), mapping) + m.group(3), text)
    text = re.sub(r"(\[[A-Z][\w-]*(?: [\w-]+)? )(\d+)(\.\d+)", lambda m: m.group(1) + remap_number(m.group(2), mapping) + m.group(3), text)
    def kw(m: re.Match) -> str:
        before = text[max(0, m.start() - 70): m.start()]
        if CITATION_RE.search(before):
            print(f"  left as a book citation, check: …{before[-50:]}{m.group(0)}")
            return m.group(0)
        return m.group(1) + m.group(2) + remap_list(m.group(3), mapping)
    text = KW_RE.sub(kw, text)
    text = PAREN_RE.sub(lambda m: m.group(0).replace(m.group(1), remap_number(m.group(1), mapping)), text)
    return text


def rewrite(text: str, mapping: dict[int, int], slug: str) -> str:
    out, last = [], 0
    for m in PROTECT_RE.finditer(text):
        out.append(rewrite_prose(text[last:m.start()], mapping, slug))
        out.append(m.group(0))
        last = m.end()
    out.append(rewrite_prose(text[last:], mapping, slug))
    return "".join(out)


def main(slug: str, order: list[int]) -> None:
    path = ROOT / "courses" / slug / "index.qmd"
    src = path.read_text(encoding="utf-8")
    head, body = src.split("\n---\n", 1)
    blocks = list(re.finditer(r"^## (\d+)\. .*?(?=^## |\Z)", body, flags=re.S | re.M))
    old = [int(b.group(1)) for b in blocks]
    if sorted(order) != sorted(old):
        sys.exit(f"order {order} is not a permutation of chapters {old}")
    texts = {int(b.group(1)): b.group(0) for b in blocks}
    start, end = blocks[0].start(), blocks[-1].end()
    body = body[:start] + "".join(texts[n] for n in order) + body[end:]
    mapping = {o: old[i] for i, o in enumerate(order)}
    mapping = {k: v for k, v in mapping.items() if k != v}

    # Contents list: rebuild the chapter lines in the new order
    refs_at = body.find("\n## References")
    refs_at = refs_at if refs_at >= 0 else len(body)
    marked = rewrite(body[:refs_at], mapping, slug) + body[refs_at:]
    body = marked.replace("\x00", "")
    lines = body.split("\n")
    toc = [i for i, l in enumerate(lines) if re.match(r"-\s+\[\d+\. .*\]\(#ch\d+\)", l)]
    if toc:
        entries = sorted((lines[i] for i in toc),
                         key=lambda l: int(re.search(r"#ch(\d+)", l).group(1)))
        for i, e in zip(toc, entries):
            lines[i] = e
    body = "\n".join(lines)
    path.write_text(head + "\n---\n" + body, encoding="utf-8")

    for other in sorted((ROOT / "courses").glob("*/index.qmd")) + [ROOT / "index.html"]:
        if other == path:
            continue
        t = other.read_text(encoding="utf-8")
        n = re.sub(rf"({re.escape(slug)}/index\.html#ch)(\d+)",
                   lambda m: m.group(1) + str(mapping.get(int(m.group(2)), int(m.group(2)))), t)
        if n != t:
            other.write_text(n, encoding="utf-8")
            print(f"updated links in {other.relative_to(ROOT)}")

    print(f"{slug}: mapping old→new {mapping}")
    if mapping:
        moved = "|".join(str(k) for k in mapping)
        sus = re.compile(rf"(?<![\w.$\\{{\x00])(?:{moved})\.\d+(?![\w.])")
        prose = PROTECT_RE.sub(" ", marked)
        for i, line in enumerate(prose.split("\n"), 1):
            if sus.search(line) and not re.match(r"#{2,3} ", line):
                print(f"  unrewritten number, check: {line.replace(chr(0), '').strip()[:160]}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], [int(x) for x in sys.argv[2].split(",")])
