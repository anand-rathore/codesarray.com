#!/usr/bin/env python3
"""Regenerate privacy-policy.html from privacy-policy.md.

privacy-policy.md is a copy of docs/privacy-policy.md in the blockfall repo and
is the source of truth for the wording. Update the markdown, then run:

    python3 build-privacy.py

Only the small subset of markdown that policy uses is supported: an h1, h2
headings, paragraphs, "- " bullets, and bare URLs (linked automatically).
"""

import html
import re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "privacy-policy.md"
OUT = HERE / "privacy-policy.html"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Blockfall Privacy Policy — Codesarray</title>
<meta name="description" content="What the Blockfall Android game does with your information: on-device saves, Google AdMob advertising and optional Google Play Games sign-in.">
<link rel="canonical" href="https://codesarray.com/privacy-policy.html">
<meta name="theme-color" content="#1c1f3a" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#f4f5fb" media="(prefers-color-scheme: light)">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Codesarray">
<meta property="og:title" content="Blockfall Privacy Policy">
<meta property="og:url" content="https://codesarray.com/privacy-policy.html">
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
      <svg class="mark" viewBox="0 0 32 32" role="img" aria-label="Codesarray">
        <rect x="1" y="1" width="14" height="14" rx="3.5" fill="#ff6b6b"/>
        <rect x="17" y="1" width="14" height="14" rx="3.5" fill="#ffe066"/>
        <rect x="1" y="17" width="14" height="14" rx="3.5" fill="#4da3ff"/>
        <rect x="17" y="17" width="14" height="14" rx="3.5" fill="#5cd68d"/>
      </svg>
      Codesarray
    </a>
    <nav class="site-nav" aria-label="Primary">
      <a href="/#blockfall">Blockfall</a>
      <a href="https://github.com/anand-rathore/blockfall">GitHub</a>
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
      <a href="https://github.com/anand-rathore/blockfall">Source &amp; issues</a>
      <a href="https://play.google.com/store/apps/details?id=com.codesarray.blockfall">Google Play</a>
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


def render(md: str) -> str:
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
        '<a class="back-link" href="/">'
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M19 12H5M11 18l-6-6 6-6"/></svg>Back to Codesarray</a></p>'
    )
    return "\n".join(body) + "\n"


def main() -> None:
    OUT.write_text(HEAD + render(SRC.read_text()) + FOOT)
    print("wrote %s (%d bytes)" % (OUT.name, OUT.stat().st_size))


if __name__ == "__main__":
    main()
