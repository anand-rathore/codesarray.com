#!/usr/bin/env python3
"""Every Codesarray brand asset, drawn from one definition of the mark and palette.

    python3 brand/make_brand.py

Writes (all paths relative to brand/):
  logo/        the mark as SVG and PNG (on graphite, transparent for dark and light
               backgrounds, single colour) and the horizontal lockup
  youtube/     profile picture, channel banner (+ safe-area preview), video watermark
  instagram/   profile picture, four story-highlight covers
  x/           profile picture, header
  facebook/    profile picture, cover
  google-play/ developer icon, developer page header
  site/        og image, apple-touch-icon and favicon; copied to the site root too

Needs Pillow. The mark is "Trace": the letter C as a circuit-board trace with
45-degree corners, ending in a via. Everything is drawn at 2x and downsampled.
See README.md in this folder for the usage rules.
"""
import random
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
ROOT = HERE.parent
FONTS = HERE / "fonts"
SS = 2  # supersampling

GRAPHITE, CARBON = "#1d2024", "#15171a"     # ground, and the darker surface
BONE, STEEL, RULE = "#f3f1ec", "#9aa0a6", "#34383e"
ORANGE = "#ff6a13"
INK = "#14171a"                              # the mark's colour on light backgrounds
TAGLINE = "Small games, and the code behind them."

# The mark on a 48-unit grid: one stroke with two 45-degree corners, then the via.
TRACE = [(38, 10.4), (18.4, 10.4), (10.4, 18.4), (10.4, 29.6), (18.4, 37.6), (29.6, 37.6)]
TRACE_W, VIA, VIA_R, HOLE_R = 8.4, (34.4, 37.6), 7.6, 3.04


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def font(name, size, wght=None):
    f = ImageFont.truetype(str(FONTS / name), int(round(size * SS)))
    if wght:
        f.set_variation_by_axes([wght])
    return f


def display(size):
    return font("BigShouldersDisplay.ttf", size, 800)


def canvas(w, h, fill=GRAPHITE, alpha=False):
    if alpha:
        return Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    return Image.new("RGB", (w * SS, h * SS), rgb(fill))


def save(img, w, h, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.resize((w, h), Image.LANCZOS).save(path, optimize=True)
    return path


def draw_mark(d, x, y, s, ink=BONE, accent=ORANGE, hole=GRAPHITE):
    """The mark in a box of side s (already in canvas pixels) at (x, y)."""
    u = s / 48
    path = [(x + px * u, y + py * u) for px, py in TRACE]
    d.line(path, fill=rgb(ink), width=round(TRACE_W * u), joint="curve")
    cx, cy = x + VIA[0] * u, y + VIA[1] * u
    r = VIA_R * u
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgb(accent))
    if hole:
        r = HOLE_R * u
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgb(hole) if isinstance(hole, str) else hole)


def mark_svg(ink, accent=ORANGE, tile=None):
    d = "M" + " L".join(f"{x:g} {y:g}" for x, y in TRACE)
    ring_r, ring_w = (VIA_R + HOLE_R) / 2, VIA_R - HOLE_R
    bg = f'  <rect width="48" height="48" rx="5" fill="{tile}"/>\n' if tile else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">\n{bg}'
            f'  <path d="{d}" fill="none" stroke="{ink}" stroke-width="{TRACE_W}" stroke-linejoin="round"/>\n'
            f'  <circle cx="{VIA[0]}" cy="{VIA[1]}" r="{ring_r:g}" fill="none" stroke="{accent}" stroke-width="{ring_w:g}"/>\n'
            f'</svg>\n')


def lockup_width(d, mark, size):
    return mark + mark * 0.3 + d.textlength("CODESARRAY", font=display(size / SS))


def draw_lockup(d, x, y, mark, ink=BONE, hole=GRAPHITE):
    """Mark + CODESARRAY, the wordmark's cap height matched to the mark. Returns the width."""
    size = mark * 1.02
    f = display(size / SS)
    draw_mark(d, x, y, mark, ink=ink, hole=hole)
    d.text((x + mark * 1.3, y + mark * 0.51), "CODESARRAY", font=f, anchor="lm", fill=rgb(ink))
    return mark * 1.3 + d.textlength("CODESARRAY", font=f)


def trace_field(d, W, H, pitch, seed, clear=None, count=26, hot=2):
    """Board traces behind the artwork: horizontal runs with 45-degree jogs between lanes,
    a via at each end. `clear` is a box (canvas pixels) no trace may enter."""
    rnd = random.Random(seed)
    w = max(2, round(pitch * 0.2))
    placed, tries, ends, traces = 0, 0, [], []

    def crosses(a, b, c, e):
        def side(p, q, r):
            return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return side(a, b, c) * side(a, b, e) <= 0 and side(c, e, a) * side(c, e, b) <= 0

    while placed < count and tries < count * 80:
        tries += 1
        lane = rnd.randrange(1, max(2, H // pitch)) * pitch
        x = rnd.uniform(-0.05, 0.9) * W
        pts = [(x, lane)]
        for _ in range(rnd.choice((1, 2, 2, 3))):
            x += rnd.uniform(0.06, 0.22) * W
            pts.append((x, lane))
            k = rnd.choice((-2, -1, 1, 2)) * pitch
            x, lane = x + abs(k), lane + k
            pts.append((x, lane))
        pts.append((x + rnd.uniform(0.04, 0.16) * W, lane))
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        if min(ys) < pitch * 0.5 or max(ys) > H - pitch * 0.5:
            continue
        if clear and max(xs) > clear[0] and min(xs) < clear[2] and max(ys) > clear[1] - pitch and min(ys) < clear[3] + pitch:
            continue
        if any(abs(py - ey) < pitch * 0.9 and abs(px - ex) < pitch * 3 for px, py in (pts[0], pts[-1]) for ex, ey in ends):
            continue
        segs = list(zip(pts, pts[1:]))
        if any(crosses(a, b, c, e) for a, b in segs for other in traces for c, e in zip(other, other[1:])):
            continue                            # traces on one layer never cross
        if any(abs(a[1] - c[1]) < pitch * 0.5 and a[1] == b[1] and c[1] == e[1] and
               min(a[0], b[0]) < max(c[0], e[0]) + pitch and max(a[0], b[0]) > min(c[0], e[0]) - pitch
               for a, b in segs for other in traces for c, e in zip(other, other[1:])):
            continue                            # nor run on top of each other in a lane
        traces.append(pts)
        ends += [pts[0], pts[-1]]
        placed += 1
    for pts in traces:
        d.line(pts, fill=rgb(RULE), width=w, joint="curve")
    for n, pts in enumerate(traces):            # vias last, so no trace runs over one
        for px, py in (pts[0], pts[-1]):
            r = w * 1.9
            is_hot = hot > 0 and n % 5 == 2 and (px, py) == pts[-1] and 0 < px < W
            d.ellipse([px - r, py - r, px + r, py + r], fill=rgb(ORANGE if is_hot else RULE))
            d.ellipse([px - r * 0.42, py - r * 0.42, px + r * 0.42, py + r * 0.42], fill=rgb(GRAPHITE))
            hot -= is_hot


def centred_lockup(d, W, y, mark):
    w = lockup_width(d, mark, mark * 1.02)
    draw_lockup(d, (W - w) / 2, y, mark)
    return (W - w) / 2, w


# ---------------------------------------------------------------- logo/

def logo():
    out = HERE / "logo"
    out.mkdir(exist_ok=True)
    (out / "mark-tile.svg").write_text(mark_svg(BONE, tile=GRAPHITE), encoding="utf-8")
    (out / "mark-on-dark.svg").write_text(mark_svg(BONE), encoding="utf-8")
    (out / "mark-on-light.svg").write_text(mark_svg(INK), encoding="utf-8")
    (out / "mark-white.svg").write_text(mark_svg("#ffffff", accent="#ffffff"), encoding="utf-8")
    S = 1024
    img = canvas(S, S)
    draw_mark(ImageDraw.Draw(img), S * SS * 0.14, S * SS * 0.13, S * SS * 0.72)
    save(img, S, S, out / "mark-tile-1024.png")
    for name, ink in (("mark-on-dark-1024.png", BONE), ("mark-on-light-1024.png", INK)):
        img = canvas(S, S, alpha=True)
        draw_mark(ImageDraw.Draw(img), S * SS * 0.08, S * SS * 0.07, S * SS * 0.84, ink=ink, hole=(0, 0, 0, 0))
        save(img, S, S, out / name)
    for name, ground, ink, alpha in (("lockup-on-dark.png", GRAPHITE, BONE, False),
                                     ("lockup-on-light.png", BONE, INK, False),
                                     ("lockup-transparent-light-text.png", None, BONE, True),
                                     ("lockup-transparent-dark-text.png", None, INK, True)):
        W, H, mark = 2000, 520, 300 * SS
        img = canvas(W, H, alpha=True) if alpha else canvas(W, H, ground)
        d = ImageDraw.Draw(img)
        w = lockup_width(d, mark, mark * 1.02)
        draw_lockup(d, (W * SS - w) / 2, (H * SS - mark) / 2, mark, ink=ink,
                    hole=(0, 0, 0, 0) if alpha else ground)
        save(img, W, H, out / name)


# ---------------------------------------------------------------- profile pictures

def profile(size, path, scale=0.56):
    """Profile picture: the mark on graphite, sized to survive a round crop."""
    img = canvas(size, size)
    S = size * SS
    m = S * scale
    draw_mark(ImageDraw.Draw(img), (S - m) / 2 + m * 0.01, (S - m) / 2 - m * 0.02, m)
    save(img, size, size, path)


# ---------------------------------------------------------------- banners

def banner(w, h, path, mark, clear, lockup_y=None, tag_size=None, extra=None, seed=5, pitch=None, align="center", x=None):
    """A banner: board traces, the lockup, the tagline, and an optional small third line."""
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    W, H, mark = w * SS, h * SS, mark * SS
    cl = tuple(v * SS for v in clear)
    trace_field(d, W, H, (pitch or round(h / 22)) * SS, seed, clear=cl, count=34, hot=3)
    tag_f = font("Barlow-Regular.ttf", tag_size or mark / SS * 0.3)
    block_h = mark + mark * 0.34 + tag_f.size * 1.1 + (mark * 0.5 if extra else 0)
    y = lockup_y * SS if lockup_y is not None else (cl[1] + cl[3] - block_h) / 2
    lw = lockup_width(d, mark, mark * 1.02)
    lx = (W - lw) / 2 if align == "center" else x * SS
    draw_lockup(d, lx, y, mark)
    ty = y + mark + mark * 0.34
    tw = d.textlength(TAGLINE, font=tag_f)
    d.text(((W - tw) / 2 if align == "center" else lx, ty), TAGLINE, font=tag_f, fill=rgb(STEEL))
    if extra:
        ef = font("Barlow-Medium.ttf", (tag_size or mark / SS * 0.3) * 0.82)
        ew = d.textlength(extra, font=ef)
        d.text(((W - ew) / 2 if align == "center" else lx, ty + tag_f.size * 1.75), extra, font=ef, fill=rgb(BONE))
    return save(img, w, h, path), img


def youtube():
    out = HERE / "youtube"
    profile(800, out / "profile-800.png")
    # everything that matters sits in YouTube's 1546x423 safe area, which survives every crop
    sx, sy = (2560 - 1546) // 2, (1440 - 423) // 2
    clear = (sx - 40, sy - 30, sx + 1546 + 40, sy + 423 + 30)
    _, img = banner(2560, 1440, out / "banner-2560x1440.png", mark=150, clear=clear, tag_size=46,
                    extra="codesarray.com", seed=11, pitch=64)
    prev = img.resize((2560, 1440), Image.LANCZOS)
    pd = ImageDraw.Draw(prev)
    pd.rectangle((sx, sy, sx + 1546, sy + 423), outline=(255, 80, 80), width=3)
    pd.rectangle((0, sy, 2560, sy + 423), outline=(255, 200, 80), width=2)
    pd.text((sx + 8, sy - 34), "1546x423 safe area (all devices)   |   2560x423 desktop",
            fill=(255, 120, 120), font=ImageFont.truetype(str(FONTS / "Barlow-Medium.ttf"), 24))
    prev.save(out / "banner-preview.png", optimize=True)
    # watermark: transparent, white trace so it reads over any video, the via stays orange
    img = canvas(150, 150, alpha=True)
    draw_mark(ImageDraw.Draw(img), 0, 0, 150 * SS, ink="#ffffff", hole=(0, 0, 0, 0))
    save(img, 150, 150, out / "watermark-150.png")


def instagram():
    out = HERE / "instagram"
    profile(1080, out / "profile-1080.png")
    # story-highlight covers: Instagram shows only the centre circle, so the word sits there
    for word in ("Games", "Python", "Shorts", "About"):
        img = canvas(1080, 1920)
        d = ImageDraw.Draw(img)
        W, H = 1080 * SS, 1920 * SS
        f = display(150)
        d.text((W / 2, H / 2 - 20 * SS), word, font=f, anchor="mm", fill=rgb(BONE))
        tw = d.textlength(word, font=f)
        y = H / 2 + 92 * SS                       # a short trace under the word, ending in a via
        d.line([(W / 2 - tw / 2, y), (W / 2 + tw / 2 - 44 * SS, y)], fill=rgb(BONE), width=12 * SS)
        r = 24 * SS
        cx = W / 2 + tw / 2 - 24 * SS
        d.ellipse([cx - r, y - r, cx + r, y + r], fill=rgb(ORANGE))
        d.ellipse([cx - r * 0.4, y - r * 0.4, cx + r * 0.4, y + r * 0.4], fill=rgb(GRAPHITE))
        save(img, 1080, 1920, out / f"highlight-{word.lower()}.png")


def x_twitter():
    out = HERE / "x"
    profile(400, out / "profile-400.png")
    # the profile picture covers the bottom-left corner, so the artwork sits right of centre
    banner(1500, 500, out / "header-1500x500.png", mark=96, clear=(470, 110, 1500, 400), tag_size=30,
           seed=3, pitch=30, align="left", x=560)


def facebook():
    out = HERE / "facebook"
    profile(720, out / "profile-720.png")
    # phones crop the sides and desktop crops top and bottom: keep to the centre
    banner(1640, 624, out / "cover-1640x624.png", mark=104, clear=(330, 150, 1310, 474), tag_size=32,
           seed=8, pitch=36)


def google_play():
    out = HERE / "google-play"
    profile(512, out / "developer-icon-512.png")
    banner(4096, 2304, out / "developer-header-4096x2304.png", mark=300, clear=(780, 760, 3316, 1544),
           tag_size=92, extra="codesarray.com", seed=21, pitch=104)


def site():
    out = HERE / "site"
    banner(1200, 630, out / "og-1200x630.png", mark=92, clear=(150, 170, 1050, 460), tag_size=30, seed=4, pitch=32)
    profile(180, out / "apple-touch-icon.png", scale=0.62)
    (out / "favicon.svg").write_text(mark_svg(BONE, tile=GRAPHITE), encoding="utf-8")
    # the site serves these three from its root
    shutil.copy(out / "og-1200x630.png", ROOT / "og.png")
    shutil.copy(out / "apple-touch-icon.png", ROOT / "apple-touch-icon.png")
    shutil.copy(out / "favicon.svg", ROOT / "favicon.svg")


if __name__ == "__main__":
    for step in (logo, youtube, instagram, x_twitter, facebook, google_play, site):
        step()
    for p in sorted(HERE.rglob("*")):
        if p.is_file() and p.suffix in (".png", ".svg") and "_archive" not in p.parts:
            print(f"{str(p.relative_to(HERE)):48} {p.stat().st_size / 1024:7.0f} KB")
