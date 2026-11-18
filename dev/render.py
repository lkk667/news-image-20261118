#!/usr/bin/env python3
"""Render the 18 November 2026 one-image news summary (1024x1024 PNG).

Newspaper front page: masthead, navy date bar, deck line, six panels
(2 cols x 3 rows). Each panel has a coloured kicker, a headline and one
summary line beside a small flat illustration drawn with Pillow shapes.
No photos, no copied artwork. Run: python3 dev/render.py -> entry.png
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (255, 255, 255)
INK = (20, 20, 20)
NAVY = (27, 42, 74)
GREY = (110, 110, 110)
RED = (179, 57, 46)
TEAL = (14, 110, 110)
GOLD = (176, 124, 18)
BLUE = (36, 84, 160)
GREEN = (46, 125, 50)
PURPLE = (96, 60, 140)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"

masthead_f = ImageFont.truetype(SERIF_B, 62)
date_f = ImageFont.truetype(SANS_B, 24)
deck_f = ImageFont.truetype(SANS_B, 21)
kick_f = ImageFont.truetype(SANS_B, 18)
head_f = ImageFont.truetype(SANS_B, 30)
sum_f = ImageFont.truetype(SANS, 22)


def wrap(draw, text, font, width):
    """Greedy word wrap by pixel width."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_jet(d, x, y, s, color):
    """Simple side-view jet silhouette."""
    d.polygon([(x, y + s * 0.45), (x + s * 0.75, y + s * 0.35),
               (x + s, y + s * 0.5), (x + s * 0.75, y + s * 0.6),
               (x, y + s * 0.55)], fill=color)
    d.polygon([(x + s * 0.45, y + s * 0.35), (x + s * 0.55, y),
               (x + s * 0.65, y + s * 0.35)], fill=color)
    d.polygon([(x + s * 0.5, y + s * 0.6), (x + s * 0.58, y + s * 0.9),
               (x + s * 0.68, y + s * 0.6)], fill=color)


def draw_burst(d, cx, cy, r, color):
    """Eight-point star burst."""
    pts = []
    for i in range(16):
        ang = i * 3.14159 / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * __import__("math").cos(ang),
                    cy + rr * __import__("math").sin(ang)))
    d.polygon(pts, fill=color)


def draw_columns(d, x, y, w, h, color):
    """Parliament building: base, columns, dome."""
    d.rectangle([x, y + h - 12, x + w, y + h], fill=color)
    d.rectangle([x + 6, y + h * 0.55, x + w - 6, y + h - 12], fill=color)
    for i in range(4):
        cx = x + 16 + i * (w - 32) / 3
        d.rectangle([cx - 5, y + h * 0.55, cx + 5, y + h - 12], fill=PAPER)
    d.pieslice([x + w * 0.25, y, x + w * 0.75, y + h * 0.55],
               180, 360, fill=color)
    d.rectangle([x + w * 0.47, y - 6, x + w * 0.53, y + 4], fill=color)


def draw_quake(d, x, y, w, h, color):
    """Seismograph zigzag over cracked ground."""
    pts = [(x + 6, y + h * 0.4)]
    import random
    random.seed(7)
    px = x + 6
    while px < x + w - 6:
        px += 9
        pts.append((px, y + h * 0.4 + random.choice([-26, -12, 0, 12, 26])))
    pts.append((x + w - 6, y + h * 0.4))
    d.line(pts, fill=color, width=4)
    d.line([(x + 10, y + h - 8), (x + w * 0.35, y + h * 0.62),
            (x + w * 0.5, y + h - 14), (x + w * 0.72, y + h * 0.7),
            (x + w - 12, y + h - 6)], fill=INK, width=4)


def draw_globe(d, x, y, s, color):
    """Globe with meridian lines and a small plane."""
    cx, cy, r = x + s / 2, y + s / 2, s / 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 0, 360,
          fill=color, width=3)
    draw_jet(d, x + s * 0.55, y + s * 0.08, s * 0.3, RED)


def draw_virus(d, x, y, s, color):
    """Spiky virus circle."""
    cx, cy, r = x + s / 2, y + s / 2, s * 0.28
    import math
    for i in range(10):
        ang = i * 2 * math.pi / 10
        d.line([cx + r * math.cos(ang), cy + r * math.sin(ang),
                cx + (r + 14) * math.cos(ang),
                cy + (r + 14) * math.sin(ang)], fill=color, width=5)
        d.ellipse([cx + (r + 14) * math.cos(ang) - 5,
                   cy + (r + 14) * math.sin(ang) - 5,
                   cx + (r + 14) * math.cos(ang) + 5,
                   cy + (r + 14) * math.sin(ang) + 5], fill=color)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    d.ellipse([cx - r * 0.4, cy - r * 0.45, cx - r * 0.1, cy - r * 0.15],
              fill=(255, 255, 255))


def draw_tower(d, x, y, w, h, color):
    """Control tower with a lightning bolt."""
    d.rectangle([x + w * 0.42, y + h * 0.3, x + w * 0.58, y + h], fill=color)
    d.rectangle([x + w * 0.3, y + h * 0.12, x + w * 0.7, y + h * 0.32],
                fill=color)
    d.polygon([(x + w * 0.82, y + h * 0.05), (x + w * 0.62, y + h * 0.45),
               (x + w * 0.76, y + h * 0.45), (x + w * 0.6, y + h * 0.85),
               (x + w * 0.88, y + h * 0.38), (x + w * 0.72, y + h * 0.38)],
              fill=GOLD)


PANELS = [
    ("THE GULF", RED, "US jets hit Iran missile site",
     "Bahrain and Kuwait fend off Iranian drones as Gulf allies stay on alert.",
     "jet"),
    ("ISRAEL", BLUE, "Knesset picks Eisenkot ally",
     "Matan Kahana wins speaker 66-52, a blow to Netanyahu's camp.",
     "columns"),
    ("ROMANIA", TEAL, "M5.3 quake shakes Vrancea",
     "Deep tremor felt in 17 countries; no major damage reported.",
     "quake"),
    ("ASIA", GREEN, "Trump meets Marcos in Manila",
     "Putin lands in China ahead of Thursday's Xi-Trump-Putin summit.",
     "globe"),
    ("HEALTH", PURPLE, "US loses measles-free status",
     "PAHO ends 26 years of elimination after 5,400 cases this year.",
     "virus"),
    ("UNITED STATES", GOLD, "Outages 'not a cyberattack'",
     "Spy chief blames updates; transport chief seeks $50bn to fix aviation.",
     "tower"),
]

ILLUS_BG = (238, 240, 244)


def draw_illus(d, kind, x, y, s, color):
    d.rectangle([x, y, x + s, y + s], fill=ILLUS_BG)
    if kind == "jet":
        d.rectangle([x, y + s * 0.62, x + s, y + s], fill=(190, 220, 235))
        draw_jet(d, x + 12, y + 18, s * 0.55, NAVY)
        draw_burst(d, x + s * 0.78, y + s * 0.72, 16, RED)
    elif kind == "columns":
        draw_columns(d, x + 14, y + 26, s - 28, s - 44, color)
    elif kind == "quake":
        draw_quake(d, x + 8, y + 12, s - 16, s - 24, color)
    elif kind == "globe":
        draw_globe(d, x + 10, y + 10, s - 20, color)
    elif kind == "virus":
        draw_virus(d, x + 8, y + 8, s - 16, color)
    elif kind == "tower":
        draw_tower(d, x + 16, y + 8, s - 32, s - 16, color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=masthead_f)) / 2, 26),
            title, font=masthead_f, fill=INK)
    d.line([24, 102, W - 24, 102], fill=INK, width=2)

    d.rectangle([24, 112, W - 24, 146], fill=NAVY)
    date = "WEDNESDAY 18 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=date_f)) / 2, 118),
            date, font=date_f, fill=PAPER)
    deck = "T H E   D A Y   I N   S I X   S T O R I E S"
    d.text(((W - d.textlength(deck, font=deck_f)) / 2, 156),
            deck, font=deck_f, fill=GREY)

    gx, gy = 24, 188
    pw, ph, gap = 482, 262, 12
    for i, (kicker, color, head, summ, kind) in enumerate(PANELS):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        d.rectangle([px, py, px + pw, py + ph], outline=INK, width=2)
        d.rectangle([px, py, px + pw, py + 5], fill=color)
        d.text((px + 14, py + 14), kicker, font=kick_f, fill=color)
        lines = wrap(d, head, head_f, pw - 28)[:2]
        hy = py + 40
        for ln in lines:
            d.text((px + 14, hy), ln, font=head_f, fill=INK)
            hy += 36
        ix, iy, s = px + 14, py + 118, 132
        draw_illus(d, kind, ix, iy, s, color)
        sx = ix + s + 12
        slines = wrap(d, summ, sum_f, pw - (s + 12) - 28)[:4]
        sy = iy + 4
        for ln in slines:
            d.text((sx, sy), ln, font=sum_f, fill=INK)
            sy += 28

    img.save("entry.png", "PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
