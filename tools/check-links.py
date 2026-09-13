#!/usr/bin/env python3
"""Check every link and asset reference in the site's HTML.

Run from anywhere:

    python3 tools/check-links.py

It walks every .html file in the repository and, for each href/src/srcset:

  * resolves internal references (root-relative like /blockfall/img/x.jpg, or
    relative like img/x.jpg) to a file on disk and reports the ones that miss;
  * checks that in-page #fragments name an id that exists in that file;
  * flags any github.com link, because the site links to none;
  * flags any surviving /img/ root path, left over from the old flat layout.

External http(s), mailto: and tel: links are not fetched, only inspected.
Prints "ok" and exits 0 when nothing is wrong.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent

# Attributes that point at something we can resolve.
URL_ATTRS = {"href", "src", "poster", "action"}


class Refs(HTMLParser):
    """Collect (attribute, value) pairs plus every id= in the document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value is None:
                continue
            if name == "id":
                self.ids.add(value)
            elif name in URL_ATTRS:
                self.refs.append((name, value.strip()))
            elif name == "srcset":
                for candidate in value.split(","):
                    url = candidate.strip().split()[0] if candidate.strip() else ""
                    if url:
                        self.refs.append(("srcset", url))
            elif name == "content" and tag == "meta":
                # <meta http-equiv="refresh" content="0; url=/somewhere">
                m = re.search(r"url\s*=\s*([^;]+)$", value, re.I)
                if m:
                    self.refs.append(("refresh", m.group(1).strip()))


def resolve(page: Path, url: str) -> Path:
    """Map an internal URL to the file GitHub Pages would serve for it."""
    path = unquote(urlsplit(url).path)
    target = ROOT / path.lstrip("/") if path.startswith("/") else page.parent / path
    target = Path(target)
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def main() -> int:
    problems: list[str] = []
    pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
    if not pages:
        print("no .html files found under %s" % ROOT)
        return 1

    for page in pages:
        rel = page.relative_to(ROOT)
        parser = Refs()
        parser.feed(page.read_text(encoding="utf-8"))
        parser.close()

        for attr, url in parser.refs:
            if "github.com" in url:
                problems.append("%s: %s=%r links to github.com" % (rel, attr, url))
                continue
            if re.match(r"^/img/", url):
                problems.append("%s: %s=%r still uses the old /img/ root" % (rel, attr, url))
                continue
            split = urlsplit(url)
            if split.scheme or split.netloc:
                continue  # external, or mailto:/tel:
            if not split.path:
                fragment = split.fragment
                if fragment and fragment not in parser.ids:
                    problems.append("%s: %s=%r has no matching id" % (rel, attr, url))
                continue
            target = resolve(page, url)
            if not target.is_file():
                problems.append(
                    "%s: %s=%r -> missing %s"
                    % (rel, attr, url, target.relative_to(ROOT) if ROOT in target.parents else target)
                )

    if problems:
        for problem in problems:
            print(problem)
        print("%d problem(s) in %d page(s)" % (len(problems), len(pages)))
        return 1

    print("ok (%d pages checked)" % len(pages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
