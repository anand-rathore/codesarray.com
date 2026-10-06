#!/usr/bin/env python3
"""Build the articles from Markdown.

    python3 build-articles.py

Articles are filed by language (the category), then by level (the sub-category):

    articles/categories.json                      the languages and levels, in display order
    articles/<language>/<level>/<slug>/article.md  one article (source of truth)

and the script writes:

    articles/<language>/<level>/<slug>/index.html  the article
    articles/<language>/<level>/index.html         every article in that level
    articles/<language>/index.html                 the language, grouped by level
    articles/index.html                            everything, grouped by language then level
    <alias>/index.html                             a forwarding page for each old address
    sitemap.xml, robots.txt                        every indexable page, for search engines

Every article page also carries Open Graph tags, its own preview image, and
TechArticle and BreadcrumbList structured data (JSON-LD) built from the header.

To add a language, add it to categories.json and create its folder. A language or
level with no articles is left off the site until it has one.

article.md starts with a header, then a line of three dashes, then the text:

    title: Python Hello World: your first program, step by step
    summary: One or two sentences, shown under the title and in the lists.
    description: Optional. What search results show (120 to 155 characters, the search
                 term near the start); the summary is used when it is missing.
    date: 2026-10-02
    read: 4 min read
    lesson: 1
    video: Hello, Python | https://youtu.be/NExcPTw_LvQ
    image: cover.png
    aliases: /articles/your-first-python-program/
    ---
    Text. Supported: ## headings, paragraphs, - and 1. lists, **bold**, `code`,
    [links](https://example.com), and fenced code blocks. A block fenced with
    ```output is styled as program output.

    lesson    the number of the long-form video in its track; these come first, in order
    follows   for an article made from a short: the lesson number it belongs after
    video     the name of the video and its YouTube URL
    image     optional preview image in the article's folder (the video's thumbnail, or
              the first post slide for a short note); shared links and search results use it
    aliases   optional old addresses of this article, comma separated; each gets a
              page that forwards here, so a published link never breaks

The three newest articles are also listed by hand on the front page (index.html,
the #articles section). Needs only the standard library.
"""
import html
import json
import re
import sys
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
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@codesarray">{extra}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
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
      <svg class="mark" viewBox="0 0 48 48" role="img" aria-label="Codesarray">
        <path d="M38 10.4L18.4 10.4L10.4 18.4L10.4 29.6L18.4 37.6L29.6 37.6" fill="none" stroke="currentColor" stroke-width="8.4" stroke-linejoin="round"/>
        <circle cx="34.4" cy="37.6" r="5.32" fill="none" stroke="#ff6a13" stroke-width="4.56"/>
      </svg>
      CODESARRAY
    </a>
    <nav class="site-nav" aria-label="Primary">
      <a href="/#games">Games</a>
      <a href="/#videos">Videos</a>
      <a href="/articles/"{articles_current}>Articles</a>
      <a href="/work/">Work</a>
      <button class="mode-toggle" type="button" hidden>
        <svg class="sun" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        <svg class="moon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>
      </button>
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

MOVED = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url={path}">
<title>{title} has moved: Codesarray</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#1d2024">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/styles.css">
<script>try{{var m=localStorage.getItem("mode");if(m)document.documentElement.dataset.mode=m}}catch(e){{}}</script>
<script src="/theme.js" defer></script>
</head>
<body>
<main id="main">
  <div class="container">
  <article class="article">
    <h1>This article has moved</h1>
    <p><a href="{path}">{title}</a> now lives at codesarray.com{path}. You should be sent there automatically; if not, follow the link.</p>
  </article>
  </div>
</main>
</body>
</html>
"""


def esc(s):
    return html.escape(s, quote=True)


def inline(text):
    """Escape, then apply `code`, **bold** and [links](url)."""
    out = []
    for part in re.split(r"(`[^`]+`)", text):
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


def load(path, languages, levels):
    lang, level, slug = path.parts[-4:-1]
    if lang not in languages or level not in levels:
        sys.exit(f"{path}: '{lang}/{level}' is not in articles/categories.json")
    head, _, body = path.read_text(encoding="utf-8").partition("\n---\n")
    a = dict((k.strip(), v.strip()) for k, v in (l.split(":", 1) for l in head.splitlines() if ":" in l))
    for key in ("title", "summary", "date", "read"):
        if not a.get(key):
            sys.exit(f"{path}: the header needs '{key}:'")
    a.update(lang=lang, level=level, slug=slug, body=body, day=date.fromisoformat(a["date"]),
             path=f"/articles/{lang}/{level}/{slug}/")
    # lessons in track order; an article made from a short sits after the lesson it follows
    a["sort"] = (float(a.get("lesson") or a.get("follows") or 9999), 0 if a.get("lesson") else 1, a["day"])
    a["label"] = f"Lesson {a['lesson']}" if a.get("lesson") else "Short note"
    a["aliases"] = [s.strip() for s in a.get("aliases", "").split(",") if s.strip()]
    return a


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(HERE).as_posix()}")


def head(title, description, path, og_type="website", current=False, image=None, extra=""):
    return HEAD.format(title=esc(title), description=esc(description), canonical=SITE + path, og_type=og_type,
                       articles_current=' aria-current="page"' if current else "",
                       image=image or f"{SITE}/og.png", extra=extra)


def jsonld(data):
    """A JSON-LD block for search engines. The data is what the builder already knows."""
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return '\n<script type="application/ld+json">' + text.replace("</", "<\\/") + "</script>"


def article_ld(a, trail, image):
    day = a["day"].isoformat()
    org = {"@type": "Organization", "name": "Codesarray", "url": SITE + "/",
           "logo": {"@type": "ImageObject", "url": f"{SITE}/brand/logo/mark-tile-1024.png"}}
    article = {"@context": "https://schema.org", "@type": "TechArticle", "headline": a["title"],
               "description": a["summary"], "image": image, "datePublished": day, "dateModified": day,
               "inLanguage": "en", "author": org, "publisher": org,
               "mainEntityOfPage": {"@type": "WebPage", "@id": SITE + a["path"]},
               "proficiencyLevel": a["level"].capitalize(),
               "articleSection": trail[1][0]}
    if a.get("video"):
        name, _, link = (s.strip() for s in a["video"].partition("|"))
        article["video"] = {"@type": "VideoObject", "name": name, "url": link, "embedUrl": link,
                            "thumbnailUrl": image, "uploadDate": day, "description": a["summary"]}
    crumbs_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail, 1)
    ] + [{"@type": "ListItem", "position": len(trail) + 1, "name": a["title"]}]}
    return jsonld(article) + jsonld(crumbs_ld)


def pretty_date(day):
    return f"{day.day} {day:%B %Y}"


def crumbs(trail):
    """Breadcrumb. trail is [(name, path), ...]; the page itself is not included."""
    items = "".join(f'<li><a href="{p}">{esc(n)}</a></li>' for n, p in trail)
    return f'<nav aria-label="Breadcrumb"><ol class="crumbs">{items}</ol></nav>\n'


def rows(articles, indent="      "):
    out = [f'{indent}<ul class="rows">']
    for a in articles:
        out.append(f'{indent}  <li class="row text">\n'
                   f'{indent}    <div class="kind"><b>{a["label"]}</b>{esc(a["read"])}'
                   f'<time datetime="{a["day"].isoformat()}">{pretty_date(a["day"])}</time></div>\n'
                   f'{indent}    <div>\n{indent}      <h3><a href="{a["path"]}">{esc(a["title"])}</a></h3>\n'
                   f'{indent}      <p>{inline(a["summary"])}</p>\n{indent}    </div>\n'
                   f'{indent}    <div class="go"><a class="more" href="{a["path"]}">Read the article</a></div>\n'
                   f'{indent}  </li>')
    out.append(f"{indent}</ul>")
    return "\n".join(out) + "\n"


def intro(title, lede, trail=None):
    return ('  <section class="intro small">\n    <div class="container">\n'
            + (f"      {crumbs(trail)}" if trail else "")
            + f"      <h1>{esc(title)}</h1>\n      <p class=\"lede\">{esc(lede)}</p>\n    </div>\n  </section>\n\n")


def build():
    cats = json.loads((ARTICLES / "categories.json").read_text(encoding="utf-8"))
    languages = {l["slug"]: l for l in cats["languages"]}
    levels = {l["slug"]: l for l in cats["levels"]}
    articles = sorted((load(p, languages, levels) for p in ARTICLES.glob("*/*/*/article.md")), key=lambda a: a["sort"])
    tree = {}       # language -> level -> [articles], both in categories.json order
    for lang in languages:
        for level in levels:
            found = [a for a in articles if (a["lang"], a["level"]) == (lang, level)]
            if found:
                tree.setdefault(lang, {})[level] = found

    for lang, by_level in tree.items():
        L = languages[lang]
        for level, group in by_level.items():
            V = levels[level]
            trail = [("Articles", "/articles/"), (L["name"], f"/articles/{lang}/"),
                     (V["name"], f"/articles/{lang}/{level}/")]
            for i, a in enumerate(group):
                day = pretty_date(a["day"])
                # the preview image: the article's own cover.png (the video's thumbnail), else the site's
                image = SITE + a["path"] + a["image"] if a.get("image") else None
                if a.get("image") and not (HERE / a["path"].strip("/") / a["image"]).exists():
                    sys.exit(f"{a['path']}: image '{a['image']}' is missing")
                published = (f'\n<meta property="article:published_time" content="{a["day"].isoformat()}">'
                             f'\n<meta property="article:section" content="{esc(trail[1][0])}">')
                page = head(a["title"], a.get("description") or a["summary"], a["path"], og_type="article", image=image,
                            extra=published + article_ld(a, trail, image or f"{SITE}/og.png"))
                page += '  <div class="container">\n  <article class="article">\n    ' + crumbs(trail)
                page += (f'    <p class="meta">{a["label"]}, by Codesarray, '
                         f'<time datetime="{a["day"].isoformat()}">{day}</time>, {esc(a["read"])}</p>\n')
                page += f'    <h1>{esc(a["title"])}</h1>\n'
                page += f'    <p class="standfirst">{inline(a["summary"])}</p>\n'
                page += render(a["body"]) + "\n"
                if a.get("video"):
                    name, _, link = (s.strip() for s in a["video"].partition("|"))
                    page += (f'    <p class="watch">This article goes with the video <strong>{esc(name)}</strong>. '
                             f'<a href="{link}">Watch it on YouTube</a>.</p>\n')
                page += '    <nav class="pager" aria-label="More in this level">\n'
                if i > 0:
                    page += f'      <a href="{group[i - 1]["path"]}"><span>Previous</span>{esc(group[i - 1]["title"])}</a>\n'
                if i < len(group) - 1:
                    page += f'      <a class="next" href="{group[i + 1]["path"]}"><span>Next</span>{esc(group[i + 1]["title"])}</a>\n'
                page += "    </nav>\n  </article>\n  </div>\n" + FOOT
                write(HERE / a["path"].strip("/") / "index.html", page)
                for alias in a["aliases"]:
                    write(HERE / alias.strip("/") / "index.html",
                          MOVED.format(title=esc(a["title"]), path=a["path"], canonical=SITE + a["path"]))

            # the level: /articles/<language>/<level>/
            title = f"{V['name']} {L['name']}"
            page = head(title, f"{L['name']} articles for the {V['name'].lower()} track. {V['summary']}",
                        f"/articles/{lang}/{level}/")
            page += intro(title, V["summary"], trail[:2])
            page += '  <div class="container board">\n' + rows(group, "    ") + "  </div>\n" + FOOT
            write(ARTICLES / lang / level / "index.html", page)

        # the language: /articles/<language>/
        page = head(f"{L['name']} articles", L["summary"], f"/articles/{lang}/")
        page += intro(L["name"], L["summary"], [("Articles", "/articles/")])
        page += '  <div class="container board">\n'
        for level, group in by_level.items():
            V = levels[level]
            page += (f'    <section class="block" id="{level}">\n'
                     f'      <h2><a href="/articles/{lang}/{level}/">{V["name"]}</a></h2>\n'
                     f'      <p class="about">{esc(V["summary"])}</p>\n' + rows(group) + "    </section>\n")
        page += "  </div>\n" + FOOT
        write(ARTICLES / lang / "index.html", page)

    # everything: /articles/
    page = head("Articles", "Short written lessons on coding, algorithms and data structures, "
                "filed by language and level, with code you can copy.", "/articles/", current=True)
    page += intro("Articles", "The lessons from the videos, written down, with code you can copy. "
                  "Filed by language, then by level, in the order they are taught.")
    page += '  <div class="container board">\n'
    for lang, by_level in tree.items():
        L = languages[lang]
        page += (f'    <section class="block" id="{lang}">\n'
                 f'      <h2><a href="/articles/{lang}/">{L["name"]}</a></h2>\n'
                 f'      <p class="about">{esc(L["summary"])}</p>\n')
        for level, group in by_level.items():
            V = levels[level]
            count = f"{len(group)} article" + ("" if len(group) == 1 else "s")
            page += (f'      <h3 class="level"><a href="/articles/{lang}/{level}/">{V["name"]}</a>'
                     f'<span>{count}</span></h3>\n' + rows(group))
        page += "    </section>\n"
    page += "  </div>\n" + FOOT
    write(ARTICLES / "index.html", page)

    # sitemap.xml and robots.txt: every page worth indexing, articles with their dates
    entries = [(p, None) for p in STATIC_PAGES]
    entries += [(f"/articles/{lang}/", None) for lang in tree]
    entries += [(f"/articles/{lang}/{level}/", None) for lang in tree for level in tree[lang]]
    entries += [(a["path"], a["day"].isoformat()) for a in articles]
    urls = "".join(f"  <url>\n    <loc>{SITE}{p}</loc>\n" + (f"    <lastmod>{d}</lastmod>\n" if d else "") + "  </url>\n"
                   for p, d in entries)
    write(HERE / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    write(HERE / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


# Pages that are not articles but belong in the sitemap. Add a page here when you add one.
STATIC_PAGES = ["/", "/work/", "/articles/", "/blockfall/", "/pawsandperils/", "/synapsy/",
                "/blockfall/privacy-policy.html", "/pawsandperils/privacy-policy.html", "/synapsy/privacy-policy.html"]


if __name__ == "__main__":
    build()
