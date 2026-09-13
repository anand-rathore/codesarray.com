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

BLOCKS_MARK = """      <svg class="mark" viewBox="0 0 32 32" role="img" aria-label="Codesarray">
        <rect x="1" y="1" width="14" height="14" rx="3.5" fill="#ff6b6b"/>
        <rect x="17" y="1" width="14" height="14" rx="3.5" fill="#ffe066"/>
        <rect x="1" y="17" width="14" height="14" rx="3.5" fill="#4da3ff"/>
        <rect x="17" y="17" width="14" height="14" rx="3.5" fill="#5cd68d"/>
      </svg>"""

# Paw print by Lorc, game-icons.net, CC BY 3.0; same path data as the app's
# res/drawable/ic_paw.xml.
PAW_MARK = """      <svg class="mark" viewBox="0 0 512 512" role="img" aria-label="Codesarray">
        <path fill="#ff8a5b" d="M258.53 16.727l-7.553 10.367s-14.79 20.28-29.64 44.75c-7.424 12.236-14.9 25.517-20.622 38.108-5.722 12.588-9.965 24.188-9.965 35.076 0 37.323 30.458 67.783 67.78 67.783 37.327 0 67.784-30.46 67.784-67.782 0-10.888-4.242-22.488-9.964-35.076-5.723-12.59-13.162-25.872-20.586-38.108-14.85-24.47-29.676-44.75-29.676-44.75l-7.557-10.367zm0 32.778c4.848 6.853 10.65 14.592 21.245 32.05 7.185 11.838 14.33 24.617 19.565 36.133 5.235 11.518 8.285 22.092 8.285 27.34 0 14.03-5.816 26.627-15.172 35.553 1.712-4.232 2.662-8.853 2.662-13.698 0-20.197-36.57-70.364-36.57-70.364s-36.572 50.167-36.572 70.364c0 4.86.955 9.492 2.675 13.734-9.377-8.928-15.21-21.54-15.21-35.588 0-5.248 3.087-15.822 8.322-27.34 5.234-11.516 12.38-24.295 19.564-36.133 10.594-17.457 16.36-25.195 21.207-32.05zM60.66 79.365l-3.285 12.374s-6.49 24.27-11.496 52.45c-2.503 14.09-4.652 29.19-5.44 42.998-.786 13.807-.538 26.13 3.395 36.28 13.484 34.803 52.873 52.214 87.676 38.73 34.803-13.486 52.21-52.913 38.728-87.713-3.933-10.153-12.09-19.383-21.974-29.055-9.884-9.67-21.653-19.38-32.996-28.105C92.578 99.875 71.463 86.3 71.463 86.3l-10.805-6.936zm394.725 0L444.578 86.3s-21.114 13.574-43.8 31.025c-11.344 8.726-23.114 18.434-33 28.105-9.883 9.672-18.002 18.902-21.936 29.055-13.483 34.8 3.888 74.227 38.69 87.713 34.804 13.484 74.23-3.927 87.714-38.73 3.934-10.15 4.145-22.473 3.358-36.28-.787-13.807-2.935-28.907-5.438-42.998-5.006-28.18-11.498-52.45-11.498-52.45l-3.285-12.376zm-11.826 30.55c2.042 8.137 4.64 17.446 8.213 37.56 2.42 13.636 4.46 28.142 5.18 40.772.72 12.63-.255 23.576-2.15 28.47-5.067 13.076-15.038 22.716-26.98 27.66 3.116-3.325 5.666-7.28 7.412-11.788 7.298-18.834-8.68-78.824-8.68-78.824s-52.227 33.564-59.523 52.395c-1.75 4.516-2.533 9.164-2.467 13.725-5.504-11.706-6.38-25.56-1.31-38.648 1.897-4.893 8.553-13.598 17.595-22.445 9.042-8.85 20.34-18.203 31.316-26.647 16.206-12.465 24.41-17.6 31.393-22.23zm-371.035.037c6.997 4.64 15.17 9.745 31.355 22.193 10.977 8.444 22.276 17.798 31.318 26.647 9.042 8.847 15.696 17.552 17.592 22.445 5.068 13.082 4.197 26.932-1.3 38.635.063-4.557-.722-9.2-2.47-13.71-7.295-18.832-59.523-52.396-59.523-52.396s-15.975 59.99-8.678 78.823c1.748 4.508 4.298 8.466 7.415 11.79-11.945-4.942-21.92-14.583-26.988-27.663-1.896-4.894-2.872-15.84-2.152-28.47.72-12.63 2.797-27.137 5.22-40.772 3.568-20.096 6.167-29.375 8.212-37.523zm184.294 122.39c-43.658 0-79.31 28.473-87.347 66.686-22.89 8.593-43.324 19.73-57.71 34.275-15.516 15.688-25.112 34.84-25.112 55.518 0 30.856 20.97 57.578 52.124 75.997 31.154 18.418 73.17 29.38 119.322 29.38s87.99-10.95 118.994-29.38c31.004-18.43 51.832-45.18 51.832-75.996 0-20.867-9.736-40.188-25.48-55.99-14.613-14.672-35.395-25.875-58.692-34.423-8.38-37.994-44.513-66.066-87.932-66.066zm0 18.686c37.094 0 66.64 24.44 71.178 54.936l.838 5.656 5.44 1.832c23.44 7.892 42.783 19.37 55.92 32.557 13.136 13.187 20.04 27.7 20.04 42.817 0 14.93-6.83 29.376-19.52 42.178 3.65-7.606 5.618-15.66 5.618-24.004 0-25.25-31.607-64.705-89.514-79.745.172-1.57.26-3.162.26-4.774 0-25.574-22.076-46.31-49.308-46.31-27.233 0-49.31 20.736-49.31 46.31 0 1.543.085 3.065.24 4.568-58.223 14.926-89.483 54.81-89.483 79.953h-.002c0 8.25 1.937 16.215 5.533 23.743-12.622-12.743-19.41-27.096-19.41-41.916 0-14.955 6.777-29.303 19.71-42.38C137.982 333.37 157.032 321.95 180.09 314l5.402-1.868.805-5.694c4.324-30.847 33.236-55.41 70.52-55.41z"/>
      </svg>"""

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
        "mark": BLOCKS_MARK,
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
        "mark": PAW_MARK,
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
