#!/usr/bin/env python3
"""Write the About and Contact pages from the privacy page's shell (head, header, footer).

    python3 tools/make-info-pages.py

The two pages are plain static HTML like /privacy/ and /work/. They are listed in STATIC_PAGES in
build-articles.py so they reach sitemap.xml. Edit the text below and rerun to change them.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
shell = (ROOT / "privacy" / "index.html").read_text(encoding="utf-8")

PAGES = {
    "about": {
        "title": "About Codesarray",
        "desc": "Codesarray makes calm Android games and teaches Python and JavaScript in short videos and "
                "written lessons, with every example run before it is shown.",
        "body": """    <h1>About Codesarray</h1>
    <p>Codesarray makes calm games for Android, and teaches programming through short videos and written lessons. The lessons come first on this site: each one explains a single idea, shows real code, and prints the real output.</p>
    <h2>What you will find here</h2>
    <ul>
      <li><strong>Lessons.</strong> Written articles for <a href="/articles/python/">Python</a> and <a href="/articles/javascript/">JavaScript</a>, filed by level: beginner, intermediate and advanced. Each article goes with a video of the same name on <a href="https://www.youtube.com/@codesarray">YouTube</a>, so you can read it, watch it, or do both.</li>
      <li><strong>Short notes.</strong> Small articles that explain one surprising behaviour, such as why a Python <code>int</code> never overflows, and point to the full lesson it belongs to.</li>
      <li><strong>Games.</strong> Three games for Android: <a href="/blockfall/">Blockfall</a>, <a href="/pawsandperils/">Paws &amp; Perils</a> and <a href="/synapsy/">Synapsy</a>. They play offline, with no accounts.</li>
    </ul>
    <h2>How the lessons are made</h2>
    <p>Every code example in a lesson is a real file that was run before it was written up. The output you see under it is what the program printed, copied exactly. If an example could crash on an input the lesson's claim covers, it is changed or the claim is narrowed before publishing.</p>
    <p>Lessons teach the current versions: Python 3.14 and Node 24. When a feature is new, the lesson says which version added it. The videos are drawn with code rather than recorded from a screen, and the narration is written first, so what appears on screen matches what is said.</p>
    <p>Lessons go in order, one idea at a time, each building on the ones before it. Plain words come before technical ones, and a lesson ends with the questions a learner at that point tends to ask.</p>
    <h2>Corrections</h2>
    <p>If a lesson is wrong, unclear, or out of date, please <a href="/contact/">tell us</a> with the page address and the line in question. Mistakes are fixed on the page itself.</p>
    <h2>Who makes it</h2>
    <p>Codesarray is an independent developer's studio. Background and experience are on the <a href="/work/">Work</a> page. The site has no accounts, no comments and no tracking of its own; see the <a href="/privacy/">privacy policy</a> for exactly what that means.</p>
    <h2>Advertising</h2>
    <p>The lessons are free to read. The site may show ads through Google AdSense. Ads never change what a lesson says, and nothing on the site is sponsored content.</p>
""",
    },
    "contact": {
        "title": "Contact Codesarray",
        "desc": "How to reach Codesarray: report a mistake in a lesson, ask for help with a game, or get in touch "
                "about work.",
        "body": """    <h1>Contact Codesarray</h1>
    <p>The best way to reach Codesarray is email: <a href="mailto:codesarray@gmail.com">codesarray@gmail.com</a>.</p>
    <h2>Report a mistake in a lesson</h2>
    <p>Include the page address and the sentence or line of code that looks wrong. If you can, say what you expected and what you saw instead, and which Python or Node version you ran. Mistakes are fixed on the page itself.</p>
    <h2>Help with a game</h2>
    <p>Name the game (<a href="/blockfall/">Blockfall</a>, <a href="/pawsandperils/">Paws &amp; Perils</a> or <a href="/synapsy/">Synapsy</a>), your phone model, and your Android version, and describe what happened. Each game's privacy policy is linked from the <a href="/privacy/">privacy page</a>.</p>
    <h2>Suggest a lesson</h2>
    <p>Tell us what you got stuck on. Lessons follow the Python and JavaScript tracks in order, and suggestions help decide which small notes and questions to add.</p>
    <h2>Work and other requests</h2>
    <p>For project work, see the <a href="/work/">Work</a> page, then write to the address above.</p>
    <h2>Elsewhere</h2>
    <p>Codesarray is also on <a href="https://www.youtube.com/@codesarray">YouTube</a>, <a href="https://www.instagram.com/codesarray/">Instagram</a>, <a href="https://x.com/codesarray">X</a> and <a href="https://www.facebook.com/codesarray">Facebook</a>. Email is the only place requests are tracked, so use it for anything that needs an answer.</p>
    <p>Please do not send passwords, payment details or other private information.</p>
""",
    },
}

for slug, p in PAGES.items():
    url = f"https://codesarray.com/{slug}/"
    page = shell
    page = re.sub(r"<title>.*?</title>", f"<title>{p['title']}: Codesarray</title>" if slug != "about"
                  else f"<title>{p['title']}</title>", page, count=1)
    page = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + p["desc"] + m.group(2), page, count=1)
    page = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), page, count=1)
    page = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + p["title"] + m.group(2), page, count=1)
    page = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + p["desc"] + m.group(2), page, count=1)
    page = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), page, count=1)
    page = re.sub(r'(<article class="prose">\n).*?(  </article>)', lambda m: m.group(1) + p["body"] + m.group(2), page, count=1, flags=re.S)
    out = ROOT / slug / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))
