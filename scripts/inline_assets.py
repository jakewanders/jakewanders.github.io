#!/usr/bin/env python3
"""Inline assets/site.css and assets/theme.js into every page. Run in CI after build_blog.py.

The pages link the two files normally, so local preview and editing work as before.
At deploy time this swaps each link for the file's contents, so a visitor needs a
single request (the HTML) before first paint instead of three. That round trip is most
of First Contentful Paint on a slow connection, and GitHub Pages only lets the
files be cached for 10 minutes anyway.

Rewrites files in place. Don't run it on a working copy you mean to commit.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = (ROOT / "assets/site.css").read_text(encoding="utf-8")
JS = (ROOT / "assets/theme.js").read_text(encoding="utf-8")

CSS_LINK = re.compile(r'<link rel="stylesheet" href="/assets/site\.css(?:\?v=\w+)?">')
JS_TAG = re.compile(r'<script src="/assets/theme\.js(?:\?v=\w+)?"></script>')


def main():
    if "</style" in CSS or "</script" in JS:
        sys.exit("asset contains a closing tag; can't inline it safely")
    pages = 0
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        src = path.read_text(encoding="utf-8")
        # Lambdas, so backslashes in the CSS/JS aren't read as regex escapes.
        out = CSS_LINK.sub(lambda _: f"<style>\n{CSS}</style>", src)
        out = JS_TAG.sub(lambda _: f"<script>\n{JS}</script>", out)
        if out != src:
            path.write_text(out, encoding="utf-8")
            pages += 1
    if pages == 0:
        sys.exit("no pages referenced site.css or theme.js; did the link format change?")
    print(f"inlined site.css and theme.js into {pages} pages")


if __name__ == "__main__":
    main()
