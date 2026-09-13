#!/usr/bin/env python3
"""Regenerate <slug>/privacy-policy.html from <slug>/privacy-policy.md.

Each game keeps its policy under its own directory, and the markdown is the
source of truth for the wording (a copy of docs/privacy-policy.md in that game's
repo). Update the markdown, then run:

    python3 build-privacy.py blockfall
    python3 build-privacy.py pawsandperils
    python3 build-privacy.py                # both

Only the small subset of markdown that the policies use is supported: an h1, h2
headings, paragraphs, "- " bullets, and bare URLs (linked automatically).
"""

import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent

ARRAY_MARK = """      <svg class="mark" viewBox="0 0 32 32" role="img" aria-label="Codesarray">
        <defs><linearGradient id="cs-g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#262a4d"/><stop offset="1" stop-color="#12142b"/></linearGradient></defs>
        <rect width="32" height="32" rx="7" fill="url(#cs-g)"/>
        <path d="M11 8H7v16h4M21 8h4v16h-4" fill="none" stroke="#f2f3ff" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="11.2" cy="16" r="1.7" fill="#ffc53d"/>
        <circle cx="16" cy="16" r="1.7" fill="#ffc53d"/>
        <circle cx="20.8" cy="16" r="1.7" fill="#ffc53d"/>
      </svg>
"""

PLAY_URL = "https://play.google.com/store/apps/details?id=com.codesarray.blockfall"

SITES = {
    "blockfall": {
        "name": "Blockfall",
        "title": "Blockfall Privacy Policy — Codesarray",
        "description": (
            "What the Blockfall Android game does with your information: on-device "
            "saves, Google AdMob advertising and optional Google Play Games sign-in."
        ),
        "og_title": "Blockfall Privacy Policy",
        "theme_attr": ' data-theme="blockfall"',
        "theme_color": "#1c1f3a",
        "mark": ARRAY_MARK,
        "nav": [("Home", "/"), ("Paws &amp; Perils", "/pawsandperils/")],
        "store": ("Google Play", PLAY_URL),
    },
    "pawsandperils": {
        "name": "Paws &amp; Perils",
        "title": "Paws &amp; Perils Privacy Policy — Codesarray",
        "description": (
            "What the Paws &amp; Perils Android game does with your information: "
            "on-device saves, Google AdMob advertising, optional Google Play Games "
            "sign-in and the one-time Premium purchase."
        ),
        "og_title": "Paws &amp; Perils Privacy Policy",
        "theme_attr": ' data-theme="paws"',
        "theme_color": "#fff7ec",
        "mark": ARRAY_MARK,
        "nav": [("Home", "/"), ("Blockfall", "/blockfall/")],
        "store": ("Coming soon to Google Play", None),
    },
}

HEAD = """<!doctype html>
<html lang="en"{theme_attr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="{theme_color}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Codesarray">
<meta property="og:title" content="{og_title}">
<meta property="og:url" content="{canonical}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="container">
    <a class="wordmark" href="/">
{mark}
      Codesarray
    </a>
    <nav class="site-nav" aria-label="Primary">
{nav}
    </nav>
  </div>
</header>

<main id="main">
  <div class="container">
  <article class="prose">
"""

FOOT = """  </article>
  </div>
</main>

<footer class="site-footer">
  <div class="container">
    <p>&copy; 2026 Codesarray</p>
    <nav class="footer-links" aria-label="Footer">
      <a href="/">Home</a>
{store}
      <a href="mailto:codesarray@gmail.com">Support: codesarray@gmail.com</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""


def inline(text: str) -> str:
    """Escape, then turn bare URLs into links and **bold** into <strong>."""
    out = html.escape(text, quote=False)
    out = re.sub(r'"([^"]+)"', r"“\1”", out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    # Trailing sentence punctuation must stay outside the link.
    out = re.sub(
        r"(https?://[^\s)<>]*[^\s)<>.,;:])",
        lambda m: '<a href="%s">%s</a>' % (m.group(1), m.group(1)),
        out,
    )
    return out


def render(md: str, slug: str, name: str) -> str:
    body: list[str] = []
    para: list[str] = []
    in_list = False

    def flush_para() -> None:
        if para:
            body.append("    <p>%s</p>" % inline(" ".join(para)))
            para.clear()

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            body.append("    </ul>")
            in_list = False

    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("# "):
            flush_para()
            close_list()
            body.append("    <h1>%s</h1>" % inline(line[2:]))
        elif line.startswith("## "):
            flush_para()
            close_list()
            body.append("    <h2>%s</h2>" % inline(line[3:]))
        elif line.startswith("- "):
            flush_para()
            if not in_list:
                body.append("    <ul>")
                in_list = True
            body.append("      <li>%s</li>" % inline(line[2:]))
        elif not line.strip():
            flush_para()
            close_list()
        elif line.startswith("Effective date:"):
            flush_para()
            close_list()
            body.append('    <p class="updated">%s</p>' % inline(line))
        else:
            para.append(line.strip())

    flush_para()
    close_list()
    body.append(
        '    <p style="margin-top:48px">'
        '<a class="back-link" href="/%s/">'
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M19 12H5M11 18l-6-6 6-6"/></svg>Back to %s</a></p>' % (slug, name)
    )
    return "\n".join(body) + "\n"


def build(slug: str) -> None:
    site = SITES[slug]
    src = HERE / slug / "privacy-policy.md"
    out = HERE / slug / "privacy-policy.html"

    nav = "\n".join(
        '      <a href="%s">%s</a>' % (href, label) for label, href in site["nav"]
    )
    store_label, store_href = site["store"]
    if store_href:
        store = '      <a href="%s">%s</a>' % (store_href, store_label)
    else:
        store = "      <span>%s</span>" % store_label

    head = HEAD.format(
        theme_attr=site["theme_attr"],
        title=site["title"],
        description=site["description"],
        canonical="https://codesarray.com/%s/privacy-policy.html" % slug,
        theme_color=site["theme_color"],
        og_title=site["og_title"],
        mark=site["mark"],
        nav=nav,
    )
    out.write_text(head + render(src.read_text(), slug, site["name"]) + FOOT.format(store=store))
    print("wrote %s (%d bytes)" % (out.relative_to(HERE), out.stat().st_size))


def main() -> None:
    slugs = sys.argv[1:] or list(SITES)
    for slug in slugs:
        if slug not in SITES:
            sys.exit("unknown slug %r; known: %s" % (slug, ", ".join(SITES)))
    for slug in slugs:
        build(slug)


if __name__ == "__main__":
    main()
