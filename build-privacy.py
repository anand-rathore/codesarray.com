#!/usr/bin/env python3
"""Regenerate <slug>/privacy-policy.html from <slug>/privacy-policy.md.

Each game keeps its policy under its own directory, and the markdown is the
source of truth for the wording (a copy of docs/privacy-policy.md in that game's
repo). Update the markdown, then run:

    python3 build-privacy.py blockfall
    python3 build-privacy.py pawsandperils
    python3 build-privacy.py synapsy
    python3 build-privacy.py                # all

Only the small subset of markdown that the policies use is supported: an h1, h2
headings, paragraphs, "- " bullets, and bare URLs (linked automatically).
"""

import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent

ARRAY_MARK = """      <svg class="mark" viewBox="0 0 48 48" role="img" aria-label="Codesarray">
        <path d="M38 10.4L18.4 10.4L10.4 18.4L10.4 29.6L18.4 37.6L29.6 37.6" fill="none" stroke="currentColor" stroke-width="8.4" stroke-linejoin="round"/>
        <circle cx="34.4" cy="37.6" r="5.32" fill="none" stroke="#ff6a13" stroke-width="4.56"/>
      </svg>
"""

STUDIO_NAV = [("Games", "/#games"), ("Videos", "/#videos"), ("Articles", "/articles/"), ("Work", "/work/")]

MODE_TOGGLE = """      <button class="mode-toggle" type="button" hidden>
        <svg class="sun" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        <svg class="moon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>
      </button>
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
        "theme_attr": "",
        "theme_color": "#1d2024",
        "mark": ARRAY_MARK,
        "nav": STUDIO_NAV,
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
        "theme_attr": "",
        "theme_color": "#1d2024",
        "mark": ARRAY_MARK,
        "nav": STUDIO_NAV,
        "store": ("Coming soon to Google Play", None),
    },
    "synapsy": {
        "name": "Synapsy",
        "title": "Synapsy Privacy Policy — Codesarray",
        "description": (
            "What the Synapsy Android game does with your information: on-device "
            "saves, Google AdMob advertising, optional Google Play Games sign-in "
            "and cloud save, and the one-time Remove Ads purchase."
        ),
        "og_title": "Synapsy Privacy Policy",
        "theme_attr": "",
        "theme_color": "#1d2024",
        "mark": ARRAY_MARK,
        "nav": STUDIO_NAV,
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/styles.css">
<script>try{{var m=localStorage.getItem("mode");if(m)document.documentElement.dataset.mode=m}}catch(e){{}}</script>
<script src="/theme.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="container">
    <a class="wordmark brand" href="/">
{mark}
      CODESARRAY
    </a>
    <nav class="site-nav" aria-label="Primary">
{nav}
{toggle}    </nav>
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
        mark=site["mark"].rstrip("\n"),
        toggle=MODE_TOGGLE,
        nav=nav,
    )
    # utf-8 on both sides: the Windows default (cp1252) wrote the dashes as bytes browsers cannot read
    out.write_text(head + render(src.read_text(encoding="utf-8"), slug, site["name"]) + FOOT.format(store=store),
                   encoding="utf-8", newline="\n")
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
