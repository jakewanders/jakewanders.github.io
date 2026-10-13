#!/usr/bin/env python3
"""Generate blog/ from the posts in Sanity (the same posts twoweeksites.com/blog shows).

Stdlib only, so CI needs nothing but python3. Output is static HTML:

  blog/index.html           list of posts, newest first
  blog/<slug>/index.html    one page per post

Run locally with `python3 scripts/build_blog.py`, then serve the repo root.
Sanity's API refuses browser requests from this origin (CORS), which is why the
posts are fetched at build time instead of in the page.
"""

import html
import json
import math
import re
import shutil
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "blog"

SANITY_URL = "https://zxkyssqi.apicdn.sanity.io/v2025-02-19/data/query/production"
SOURCE_SITE = "https://twoweeksites.com"
SITE = "https://jakewanders.github.io"
ASSET_VERSION = "blog1"  # keep in sync with the ?v= in index.html and work.html

QUERY = """
*[_type == "post" && defined(slug.current) && !(_id in path("drafts.**"))]{
  title,
  "slug": slug.current,
  "date": coalesce(publishedAt, _createdAt),
  "categories": categories[]->title,
  body
} | order(date desc)
"""

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def fetch_posts():
    url = SANITY_URL + "?" + urllib.parse.urlencode({"query": QUERY})
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.load(resp)["result"]


# ---------- Portable Text -> HTML ----------

MARK_TAGS = {"strong": "strong", "em": "em", "code": "code", "underline": "u", "strike-through": "s"}
BLOCK_TAGS = {"normal": "p", "h1": "h2", "h2": "h2", "h3": "h3", "h4": "h4", "blockquote": "blockquote"}


def safe_href(href):
    href = (href or "").strip()
    if href.startswith(("http://", "https://", "mailto:", "/", "#")):
        return href
    return None


def render_spans(block):
    defs = {d["_key"]: d for d in block.get("markDefs") or []}
    out = []
    for span in block.get("children") or []:
        if span.get("_type") != "span":
            continue
        text = html.escape(span.get("text", "")).replace("\n", "<br>")
        for mark in span.get("marks") or []:
            if mark in MARK_TAGS:
                tag = MARK_TAGS[mark]
                text = f"<{tag}>{text}</{tag}>"
            elif mark in defs and defs[mark].get("_type") == "link":
                href = safe_href(defs[mark].get("href"))
                if href:
                    text = f'<a href="{html.escape(href)}">{text}</a>'
        out.append(text)
    return "".join(out)


def render_body(blocks):
    out = []
    open_list = None  # "ul" / "ol" while inside a run of list items
    for block in blocks or []:
        if block.get("_type") != "block":
            continue  # images and custom types aren't used in posts yet
        list_tag = {"bullet": "ul", "number": "ol"}.get(block.get("listItem"))
        if open_list and list_tag != open_list:
            out.append(f"</{open_list}>")
            open_list = None
        inner = render_spans(block)
        if list_tag:
            if not open_list:
                out.append(f"<{list_tag}>")
                open_list = list_tag
            out.append(f"<li>{inner}</li>")
            continue
        if not inner.strip():
            continue
        tag = BLOCK_TAGS.get(block.get("style"), "p")
        out.append(f"<{tag}>{inner}</{tag}>")
    if open_list:
        out.append(f"</{open_list}>")
    return "\n".join(out)


def plain_text(blocks):
    return " ".join(
        s.get("text", "")
        for b in blocks or [] if b.get("_type") == "block"
        for s in b.get("children") or []
    )


def summary(blocks, limit=180):
    for b in blocks or []:
        if b.get("_type") == "block" and b.get("style", "normal") == "normal" and not b.get("listItem"):
            spans = b.get("children") or []
            if spans and all("em" in (s.get("marks") or []) for s in spans):
                continue  # an all-italic lead-in like "Part 1 of 3 in our series…" isn't a summary
            text = " ".join(s.get("text", "") for s in spans).strip()
            if text:
                return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "…"
    return ""


def reading_minutes(blocks):
    return max(1, math.ceil(len(plain_text(blocks).split()) / 220))


def fmt_date(iso):
    d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return d.strftime("%b %-d, %Y"), d.strftime("%Y-%m-%d")


# ---------- page shell (mirrors work.html) ----------

FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' "
    "height='32' rx='6' fill='%230f6e76'/%3E%3Ctext x='16' y='22' font-family='monospace' font-size='18' "
    "fill='white' text-anchor='middle'%3Ejn%3C/text%3E%3C/svg%3E"
)
FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap"


def page(*, title, description, canonical, og_type, main, footer_link):
    t, d = html.escape(title), html.escape(description)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t}</title>
  <meta name="description" content="{d}">
  <link rel="canonical" href="{html.escape(canonical)}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <link rel="icon" href="{FAVICON}">
  <script>
    (function () {{
      // Read the saved theme from localStorage, then a cookie fallback, then the OS preference.
      var t = null;
      try {{ t = localStorage.getItem("theme"); }} catch (e) {{}}
      if (t !== "dark" && t !== "light") {{
        var m = document.cookie.match(/(?:^|; )theme=(dark|light)/);
        if (m) t = m[1];
      }}
      if (t !== "dark" && t !== "light") {{
        t = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      }}
      document.documentElement.setAttribute("data-theme", t);
    }})();
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="{FONTS}">
  <link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="{FONTS}"></noscript>
  <link rel="stylesheet" href="/assets/site.css?v={ASSET_VERSION}">
</head>
<body>
<div class="page">

  <header class="topbar">
    <nav class="nav" aria-label="Site">
      <a href="/">résumé</a>
      <a href="/work.html">work</a>
      <a href="/blog/" aria-current="page">blog</a>
    </nav>
    <button class="theme-toggle" type="button" data-theme-toggle aria-label="Toggle dark mode">
      <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
      <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
    </button>
  </header>

  <main id="content">
{main}
  </main>

  <footer class="colophon mono">
    <span>Jake Nelson · <span id="year">2026</span></span>
    <span>{footer_link}</span>
  </footer>
</div>
<script src="/assets/theme.js?v={ASSET_VERSION}"></script>
<script>document.getElementById("year").textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def render_index(posts):
    entries = []
    for p in posts:
        shown, iso = fmt_date(p["date"])
        tags = "".join(f"<li>{html.escape(c)}</li>" for c in p.get("categories") or [])
        entries.append(f"""      <article class="entry post-entry">
        <time class="when" datetime="{iso}">{shown}</time>
        <div>
          <h3><a href="/blog/{p['slug']}/">{html.escape(p['title'] or 'Untitled')}</a></h3>
          <p class="summary">{html.escape(summary(p.get('body')))}</p>
          <p class="mono">{reading_minutes(p.get('body'))} min read</p>
          {f'<ul class="tags">{tags}</ul>' if tags else ''}
        </div>
      </article>""")
    main = f"""  <section class="masthead">
    <h1>Blog</h1>
    <p class="role">Plain-English notes on building, securing, and speeding up small-business websites. Also published on <a href="{SOURCE_SITE}/blog">twoweeksites.com</a>.</p>
  </section>

  <section class="section entries">
    <h2>Posts</h2>
{chr(10).join(entries)}
  </section>"""
    return page(
        title="Blog — Jake Nelson",
        description="Posts by Jake Nelson on small-business websites: speed, security, accessibility, and React.",
        canonical=f"{SITE}/blog/",
        og_type="website",
        main=main,
        footer_link='<a href="/">← résumé</a>',
    )


def render_post(p):
    shown, iso = fmt_date(p["date"])
    title = p["title"] or "Untitled"
    original = f"{SOURCE_SITE}/post/{p['slug']}"
    tags = "".join(f"<li>{html.escape(c)}</li>" for c in p.get("categories") or [])
    main = f"""  <article class="post">
    <header class="masthead">
      <p class="mono"><a href="/blog/">← all posts</a></p>
      <h1>{html.escape(title)}</h1>
      <p class="where"><time datetime="{iso}">{shown}</time> · {reading_minutes(p.get('body'))} min read</p>
      {f'<ul class="tags">{tags}</ul>' if tags else ''}
    </header>
    <div class="prose">
{render_body(p.get('body'))}
    </div>
    <p class="mono post-origin">Originally published on <a href="{html.escape(original)}">twoweeksites.com</a>.</p>
  </article>"""
    return page(
        title=f"{title} — Jake Nelson",
        description=summary(p.get("body")) or title,
        # The post's home is twoweeksites.com; point search engines there so the copies don't compete.
        canonical=original,
        og_type="article",
        main=main,
        footer_link='<a href="/blog/">← blog</a>',
    )


def main():
    posts = fetch_posts()
    valid = []
    for p in posts:
        if SLUG_RE.match(p.get("slug") or ""):
            valid.append(p)
        else:
            print(f"skipping post with unsafe slug: {p.get('slug')!r}", file=sys.stderr)
    if not valid:
        # Fail the deploy rather than publish an empty blog; Pages keeps serving the last good build.
        sys.exit("Sanity returned no posts; refusing to build an empty blog")

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "index.html").write_text(render_index(valid), encoding="utf-8")
    for p in valid:
        d = OUT / p["slug"]
        d.mkdir()
        (d / "index.html").write_text(render_post(p), encoding="utf-8")
    print(f"wrote {len(valid)} posts to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
