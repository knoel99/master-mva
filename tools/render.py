#!/usr/bin/env python3
"""Render course pages with Quarto, then put back the pinned KaTeX tags.

Quarto rewrites the KaTeX <script>/<link> tags on every render and drops the
subresource-integrity attributes (see tools/check_gates.py). This wrapper
renders each given module and restores the two tags exactly as published.

Usage (repository root):
    python3 tools/render.py s1-convex-optimization s2-kernel-methods
    python3 tools/render.py --all
    python3 tools/render.py projects        # the end-of-year projects page
Quarto 1.7.32 reproduces the committed pages byte for byte
(pip install quarto-cli==1.7.32).
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://cdn.jsdelivr.net/npm/katex@0.19.0/dist/"
JS_TAG = (
    '<script>window.backupDefine = window.define; window.define = undefined;</script>'
    f'<script src="{BASE}katex.min.js" integrity="sha384-QFFtAGzvvj+bfgCGxXJlNZZR1nXEZgvG8tDLCCY1F19xl20WlfTYgguB4VcNdxYk" crossorigin="anonymous"></script>'
)
CSS_TAG = (
    '<script>window.define = window.backupDefine; window.backupDefine = undefined;</script>'
    f'<link rel="stylesheet" href="{BASE}katex.min.css" integrity="sha384-3rdsX6e5mueWyoweR9NIVmtEsUkokpBT/0ALqKKIBMr9j4qhHkaIkAcGgsE6uVlp" crossorigin="anonymous">'
)
JS_RE = re.compile(r'<script defer="" src="https://cdn\.jsdelivr\.net/npm/katex@0\.19\.0/dist/katex\.min\.js(?:katex\.min\.js)?"></script>')
CSS_RE = re.compile(r'<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/npm/katex@0\.19\.0/dist/katex\.min\.js(?:katex\.min\.css)?">')


def render(slug: str) -> None:
    qmd = ROOT / ("projects" if slug == "projects" else f"courses/{slug}") / "index.qmd"
    subprocess.run(["quarto", "render", str(qmd), "--quiet"], check=True)
    html_path = qmd.with_name("index.html")
    html = html_path.read_text(encoding="utf-8")
    html = JS_RE.sub(lambda _: JS_TAG, html)
    html = CSS_RE.sub(lambda _: CSS_TAG, html)
    html_path.write_text(html, encoding="utf-8")
    ok = "katex" not in html or (JS_TAG in html and CSS_TAG in html)
    print(f"{slug}: rendered{'' if ok else ' (KaTeX tags NOT restored)'}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--all"]:
        args = sorted(p.parent.name for p in (ROOT / "courses").glob("*/index.qmd"))
        if (ROOT / "projects/index.qmd").is_file():
            args.append("projects")
    if not args:
        sys.exit(__doc__)
    for slug in args:
        render(slug.strip("/").split("/")[-1])
