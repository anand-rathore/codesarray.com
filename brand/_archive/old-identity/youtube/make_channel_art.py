#!/usr/bin/env python3
"""YouTube channel art for Codesarray, drawn from the site's mark and palette.

    python3 make_channel_art.py

Writes to out/:
  banner-2560x1440.png        channel banner; everything that matters sits in YouTube's
                              1546x423 safe area so it survives phone, desktop and TV crops
  banner-preview.png          the banner with the safe area outlined, for checking only
  profile-800.png             channel picture (YouTube shows it round)
  watermark-150.png           video watermark: the mark alone on a transparent background
  watermark-blockfall-150.png alternative watermark: the Blockfall squares

Needs Pillow. The mark is the favicon's geometry (32-unit box: two brackets and three gold
dots) scaled up; everything is drawn at 4x and downsampled so strokes stay smooth.
"""
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
OUT = HERE / "out"
FONTS = HERE.parent / "fonts"
SS = 4  # supersampling

NAVY = (0x1C, 0x1F, 0x3A)
SURFACE = (0x12, 0x14, 0x2B)
TEXT = (0xF2, 0xF3, 0xFF)
DIM = (0x9D, 0xA2, 0xC7)
GOLD = (0xFF, 0xC5, 0x3D)
PIECES = [(0xFF, 0x6B, 0x6B), (0xFF, 0xE0, 0x66), (0x4D, 0xA3, 0xFF), (0x5C, 0xD6, 0x8D), (0xFF, 0xB8, 0x4D), (0xC7, 0x7D, 0xFF)]
BLOCKFALL = [(0xFF, 0x6B, 0x6B), (0xFF, 0xE0, 0x66), (0x4D, 0xA3, 0xFF), (0x5C, 0xD6, 0x8D)]  # tl, tr, bl, br
PAWS = (0xFF, 0x8A, 0x5B)
SYNAPSY_BG, SYNAPSY, SYNAPSY_GOLD = (0x0F, 0x16, 0x26), (0x3F, 0xC1, 0xB0), (0xF2, 0xB4, 0x41)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), int(size))


def rounded(d, x, y, w, h, r, fill):
    d.rounded_rectangle((x, y, x + w, y + h), radius=r, fill=fill)


def draw_mark(d, x, y, size, square=True, ink=TEXT, stroke_scale=1.0):
    """The Codesarray mark in a `size` box at (x, y), in favicon units (32 per box)."""
    u = size / 32
    if square:
        rounded(d, x, y, size, size, 7 * u, NAVY)
    w = 2 * u * stroke_scale
    # left bracket: (11,8) -> (7.5,8) -> (7.5,24) -> (11,24); right bracket mirrored
    for pts in (
        [(11, 8), (7.5, 8), (7.5, 24), (11, 24)],
        [(21, 8), (24.5, 8), (24.5, 24), (21, 24)],
    ):
        path = [(x + px * u, y + py * u) for px, py in pts]
        d.line(path, fill=ink, width=int(w), joint="curve")
        for p in (path[0], path[-1]):
            d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=ink)
    for cx in (11.2, 16, 20.8):
        r = 1.6 * u
        d.ellipse((x + cx * u - r, y + 16 * u - r, x + cx * u + r, y + 16 * u + r), fill=GOLD)


def draw_blockfall_icon(d, x, y, size):
    gap = size * 0.06
    b = (size - gap) / 2
    for k, col in enumerate(BLOCKFALL):
        bx = x + (k % 2) * (b + gap)
        by = y + (k // 2) * (b + gap)
        rounded(d, bx, by, b, b, b * 0.23, col)


def draw_paws_icon(d, x, y, size):
    """A paw print in the Paws & Perils orange: four toes over a pad, like the icon's silhouette."""
    cx, cy = x + size / 2, y + size / 2
    pad_w, pad_h = size * 0.56, size * 0.44
    d.ellipse((cx - pad_w / 2, cy + size * 0.06 - pad_h / 2, cx + pad_w / 2, cy + size * 0.06 + pad_h / 2), fill=PAWS)
    toes = [(-0.30, -0.16, 0.19), (-0.11, -0.34, 0.19), (0.11, -0.34, 0.19), (0.30, -0.16, 0.19)]
    for tx, ty, tr in toes:
        r = tr * size / 2
        d.ellipse((cx + tx * size - r, cy + ty * size - r, cx + tx * size + r, cy + ty * size + r), fill=PAWS)


def draw_synapsy_icon(d, x, y, size):
    u = size / 108
    rounded(d, x, y, size, size, 24 * u, SYNAPSY_BG)
    centre = (x + 54 * u, y + 54 * u)
    nodes = [(76.6, 45.8), (58.2, 30.4), (35.6, 38.6), (31.4, 62.2), (49.8, 77.6), (72.4, 69.4)]
    for nx, ny in nodes:
        d.line([centre, (x + nx * u, y + ny * u)], fill=SYNAPSY, width=max(1, int(3.2 * u)))
    for nx, ny in nodes[1:]:
        r = 4 * u
        d.ellipse((x + nx * u - r, y + ny * u - r, x + nx * u + r, y + ny * u + r), fill=SYNAPSY)
    r = 9 * u
    d.ellipse((centre[0] - r, centre[1] - r, centre[0] + r, centre[1] + r), fill=SYNAPSY)
    r = 3.5 * u
    d.ellipse((centre[0] - r, centre[1] - r, centre[0] + r, centre[1] + r), fill=SYNAPSY_BG)
    nx, ny, r = 76.6, 45.8, 5.5 * u
    d.ellipse((x + nx * u - r, y + ny * u - r, x + nx * u + r, y + ny * u + r), fill=SYNAPSY_GOLD)


def drifting_blocks(img, seed=42, count=34, keep_clear=None):
    """Faint pieces scattered behind everything, as in the trailer. `keep_clear` is a box left empty."""
    W, H = img.size
    rnd = random.Random(seed)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    shapes = [[(0, 0)], [(0, 0), (1, 0)], [(0, 0), (0, 1), (1, 0)], [(0, 0), (1, 0), (1, 1)], [(0, 0), (0, 1), (0, 2)]]
    placed = 0
    while placed < count:
        cx, cy = rnd.uniform(-0.05, 1.05) * W, rnd.uniform(-0.05, 1.05) * H
        size = rnd.uniform(0.05, 0.12) * H
        shape = rnd.choice(shapes)
        if keep_clear:
            x0, y0, x1, y1 = keep_clear
            ext = size * 1.08 * 3
            if cx + ext > x0 and cx < x1 and cy + ext > y0 and cy < y1:
                continue
        col = rnd.choice(PIECES) + (rnd.randint(16, 40),)
        for r, c in shape:
            rounded(d, cx + c * size * 1.08, cy + r * size * 1.08, size, size, size * 0.22, col)
        placed += 1
    img.alpha_composite(layer)


def text_w(d, text, f):
    return d.textlength(text, font=f)


def banner():
    W, H = 2560 * SS, 1440 * SS
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    # a soft vertical lift behind the safe band so the text sits on something
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    for i in range(60):
        a = int(26 * (1 - abs(i - 30) / 30))
        y0 = H / 2 - 290 * SS + i * (580 * SS / 60)
        bd.rectangle((0, y0, W, y0 + 580 * SS / 60 + 1), fill=SURFACE + (a,))
    img.alpha_composite(band)
    safe_w, safe_h = 1546 * SS, 423 * SS
    sx, sy = (W - safe_w) / 2, (H - safe_h) / 2
    drifting_blocks(img, seed=7, count=40, keep_clear=(sx - 40 * SS, sy - 20 * SS, sx + safe_w + 40 * SS, sy + safe_h + 20 * SS))
    d = ImageDraw.Draw(img)

    # Row 1: mark + wordmark, centred in the safe area
    mark = 150 * SS
    f_word = font("SpaceGrotesk-Bold.ttf", 132 * SS)
    gap = 34 * SS
    word_w = text_w(d, "Codesarray", f_word)
    row_w = mark + gap + word_w
    x = (W - row_w) / 2
    y = sy + 44 * SS
    draw_mark(d, x, y, mark, square=False, stroke_scale=1.1)
    # vertically centre the wordmark on the mark (cap height sits above the baseline)
    bbox = d.textbbox((0, 0), "Codesarray", font=f_word)
    text_h = bbox[3] - bbox[1]
    d.text((x + mark + gap, y + (mark - text_h) / 2 - bbox[1]), "Codesarray", font=f_word, fill=TEXT)

    # Row 2: tagline
    f_tag = font("Archivo-Regular.ttf", 46 * SS)
    tag = "Small games, made to be played every day."
    tw = text_w(d, tag, f_tag)
    ty = y + mark + 34 * SS
    d.text(((W - tw) / 2, ty), tag, font=f_tag, fill=DIM)

    # Row 3: the three games
    f_game = font("Archivo-SemiBold.ttf", 34 * SS)
    icon = 64 * SS
    games = [("Blockfall", draw_blockfall_icon), ("Paws & Perils", draw_paws_icon), ("Synapsy", draw_synapsy_icon)]
    widths = [icon + 18 * SS + text_w(d, n, f_game) for n, _ in games]
    spacing = 70 * SS
    total = sum(widths) + spacing * (len(games) - 1)
    gx = (W - total) / 2
    gy = ty + 46 * SS + 44 * SS
    for (name, draw_icon), w in zip(games, widths):
        draw_icon(d, gx, gy, icon)
        bbox = d.textbbox((0, 0), name, font=f_game)
        d.text((gx + icon + 18 * SS, gy + (icon - (bbox[3] - bbox[1])) / 2 - bbox[1]), name, font=f_game, fill=TEXT)
        gx += w + spacing

    final = img.resize((2560, 1440), Image.LANCZOS).convert("RGB")
    final.save(OUT / "banner-2560x1440.png", optimize=True)

    preview = final.convert("RGBA")
    pd = ImageDraw.Draw(preview)
    pd.rectangle((sx / SS, sy / SS, (sx + safe_w) / SS, (sy + safe_h) / SS), outline=(255, 80, 80), width=3)
    pd.rectangle((0, sy / SS, 2560, (sy + safe_h) / SS), outline=(255, 200, 80), width=2)
    pd.text((sx / SS + 8, sy / SS - 28), "1546x423 safe area (all devices)   |   2560x423 desktop", fill=(255, 120, 120), font=font("Archivo-SemiBold.ttf", 22))
    preview.convert("RGB").save(OUT / "banner-preview.png")


def profile():
    S = 800 * SS
    img = Image.new("RGBA", (S, S), NAVY + (255,))
    d = ImageDraw.Draw(img)
    # the mark without its own square (the picture is the square); brackets a touch bolder at this size
    draw_mark(d, S * 0.1, S * 0.1, S * 0.8, square=False, stroke_scale=1.15)
    img.resize((800, 800), Image.LANCZOS).convert("RGB").save(OUT / "profile-800.png", optimize=True)


def watermark():
    S = 150 * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    draw_mark(d, 0, 0, S, square=False, ink=(255, 255, 255), stroke_scale=1.3)
    img.resize((150, 150), Image.LANCZOS).save(OUT / "watermark-150.png", optimize=True)

    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    draw_blockfall_icon(d, S * 0.05, S * 0.05, S * 0.9)
    img.resize((150, 150), Image.LANCZOS).save(OUT / "watermark-blockfall-150.png", optimize=True)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    banner()
    profile()
    watermark()
    for p in sorted(OUT.iterdir()):
        print(f"{p.name:32} {p.stat().st_size / 1024:7.0f} KB")
