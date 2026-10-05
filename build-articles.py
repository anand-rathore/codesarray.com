#!/usr/bin/env python3
"""Build the articles from Markdown.

    python3 build-articles.py

Reads every articles/<slug>/article.md and writes articles/<slug>/index.html, then
rewrites articles/index.html (the list, newest first). The three newest articles are
also listed by hand on the front page (index.html, the #articles section); update
those rows when you add one.

article.md starts with a header, then a line of three dashes, then the text:

    title: Your first Python program
    summary: One or two sentences, shown under the title and in the list.
    date: 2026-10-05
    topic: Python
    read: 4 min read
    video: Hello, Python | https://youtu.be/NExcPTw_LvQ
    ---
    Text. Supported: ## headings, paragraphs, - and 1. lists, **bold**, `code`,
    [links](https://example.com), and fenced code blocks. A block fenced with
    ```output is styled as program output.

Needs only the standard library.
"""
import html
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
ARTICLES = HERE / "articles"
SITE = "https://codesarray.com"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}: Codesarray</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#1d2024">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Codesarray">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://codesarray.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@codesarray">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="container">
    <a class="wordmark brand" href="/">
      <svg class="mark" viewBox="0 0 48 48" role="img" aria-label="Codesarray">
        <path d="M38 10.4L18.4 10.4L10.4 18.4L10.4 29.6L18.4 37.6L29.6 37.6" fill="none" stroke="#f3f1ec" stroke-width="8.4" stroke-linejoin="round"/>
        <circle cx="34.4" cy="37.6" r="5.32" fill="none" stroke="#ff6a13" stroke-width="4.56"/>
      </svg>
      CODESARRAY
    </a>
    <nav class="site-nav" aria-label="Primary">
      <a href="/#games">Games</a>
      <a href="/#videos">Videos</a>
      <a href="/articles/"{articles_current}>Articles</a>
      <a href="/work/">Work</a>
    </nav>
  </div>
</header>

<main id="main">
"""

FOOT = """</main>

<footer class="site-footer">
  <div class="container">
    <p>&copy; 2026 Codesarray</p>
    <nav class="footer-links social" aria-label="Codesarray elsewhere">
      <a href="https://www.youtube.com/@codesarray">YouTube</a>
      <a href="https://www.instagram.com/codesarray/">Instagram</a>
      <a href="https://x.com/codesarray">X</a>
      <a href="https://www.facebook.com/codesarray">Facebook</a>
    </nav>
    <nav class="footer-links" aria-label="Footer">
      <a href="/">Home</a>
      <a href="/articles/">Articles</a>
      <a href="mailto:codesarray@gmail.com">codesarray@gmail.com</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""


def inline(text):
    """Escape, then apply `code`, **bold** and [links](url)."""
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) > 2:
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        s = html.escape(part, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        out.append(s)
    return "".join(out)


def render(md):
    out, para, items, kind = [], [], [], None

    def flush():
        nonlocal para, items, kind
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para = []
        if items:
            out.append(f"<{kind}>\n" + "\n".join(f"  <li>{inline(i)}</li>" for i in items) + f"\n</{kind}>")
            items, kind = [], None

    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            lang = line[3:].strip()
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            cls = ' class="out"' if lang == "output" else ""
            out.append(f"<pre{cls}><code>{html.escape(chr(10).join(block))}</code></pre>")
        elif line.startswith("## "):
            flush()
            out.append(f"<h2>{inline(line[3:].strip())}</h2>")
        elif re.match(r"^(- |\d+\. )", line):
            new_kind = "ul" if line.startswith("- ") else "ol"
            if para or (kind and kind != new_kind):
                flush()
            kind = new_kind
            items.append(re.sub(r"^(- |\d+\. )", "", line))
        elif not line.strip():
            flush()
        else:
            if items:
                flush()
            para.append(line.strip())
        i += 1
    flush()
    return "\n".join(out)


def load(path):
    head, _, body = path.read_text(encoding="utf-8").partition("\n---\n")
    meta = dict((k.strip(), v.strip()) for k, v in (l.split(":", 1) for l in head.splitlines() if ":" in l))
    meta["slug"] = path.parent.name
    meta["body"] = body
    meta["day"] = date.fromisoformat(meta["date"])
    return meta


def write(path, text):
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(HERE).as_posix()}")


def build():
    articles = sorted((load(p) for p in ARTICLES.glob("*/article.md")), key=lambda a: a["day"], reverse=True)
    for a in articles:
        url = f"{SITE}/articles/{a['slug']}/"
        day = f"{a['day'].day} {a['day']:%B %Y}"
        page = HEAD.format(title=html.escape(a["title"]), description=html.escape(a["summary"], quote=True),
                           canonical=url, og_type="article", articles_current="")
        page += '  <div class="container">\n  <article class="article">\n'
        page += f'    <p class="meta">{html.escape(a["topic"])}, {day}, {html.escape(a["read"])}</p>\n'
        page += f'    <h1>{html.escape(a["title"])}</h1>\n'
        page += f'    <p class="standfirst">{inline(a["summary"])}</p>\n'
        page += render(a["body"]) + "\n"
        if a.get("video"):
            name, _, link = (s.strip() for s in a["video"].partition("|"))
            page += (f'    <p class="watch">This article goes with the video <strong>{html.escape(name)}</strong>. '
                     f'<a href="{link}">Watch it on YouTube</a>.</p>\n')
        page += '    <p><a class="back-link" href="/articles/">All articles</a></p>\n'
        page += "  </article>\n  </div>\n" + FOOT
        write(ARTICLES / a["slug"] / "index.html", page)

    page = HEAD.format(title="Articles", canonical=f"{SITE}/articles/", og_type="website",
                       description="Short written lessons on coding, algorithms and data structures, with code you can copy.",
                       articles_current=' aria-current="page"')
    page += ('  <section class="intro small">\n    <div class="container">\n      <h1>Articles</h1>\n'
             '      <p class="lede">The lessons from the videos, written down, with code you can copy.</p>\n'
             '    </div>\n  </section>\n\n  <div class="container board">\n    <ul class="rows">\n')
    for a in articles:
        href = f"/articles/{a['slug']}/"
        page += (f'      <li class="row text">\n'
                 f'        <div class="kind"><b>{html.escape(a["topic"])}</b>{html.escape(a["read"])}</div>\n'
                 f'        <div>\n          <h3><a href="{href}">{html.escape(a["title"])}</a></h3>\n'
                 f'          <p>{inline(a["summary"])}</p>\n        </div>\n'
                 f'        <div class="go"><a class="more" href="{href}">Read the article</a></div>\n'
                 f'      </li>\n')
    page += "    </ul>\n  </div>\n" + FOOT
    write(ARTICLES / "index.html", page)


if __name__ == "__main__":
    build()
