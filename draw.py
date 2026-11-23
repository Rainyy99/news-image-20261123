#!/usr/bin/env python3
"""Build entry.png: one image summing up Monday 23 November 2026.

Build-time only. The entry itself is main.ts + entry.png.
Layout: newspaper front page. Masthead + date line, two stacked hero
stories, a 2x3 grid of the remaining stories, and an honest DATE CHECK
footer. Every story carries its own date chip.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 232)
CARD = (255, 253, 246)
INK = (25, 22, 19)
RED = (163, 29, 33)
NAVY = (39, 65, 86)
GRAY = (105, 98, 88)
LINE = (201, 191, 169)

FD = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


def serif_b(s):
    return F("DejaVuSerif-Bold.ttf", s)


def sans_b(s):
    return F("DejaVuSans-Bold.ttf", s)


def sans(s):
    return F("DejaVuSans.ttf", s)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_cx(cx, y, s, f, fill):
    d.text((cx - f.getlength(s) / 2, y), s, font=f, fill=fill)


def chip(x, y, label, bg):
    """Small date pill. Returns its width."""
    f = sans_b(16)
    w = f.getlength(label) + 18
    d.rounded_rectangle([x, y, x + w, y + 26], radius=13, fill=bg)
    d.text((x + 9, y + 4), label, font=f, fill=(255, 255, 255))
    return w


def icon(kind, cx, cy, s, fg):
    """Flat geometric pictogram, centred at (cx, cy), bounding size s.
    fg is the glyph colour (white on the coloured tile)."""
    u = s / 100.0
    if kind == "chip":
        d.rounded_rectangle(
            [cx - 30 * u, cy - 22 * u, cx + 30 * u, cy + 22 * u],
            radius=6 * u, outline=fg, width=max(3, int(4 * u)))
        d.rectangle([cx - 14 * u, cy - 10 * u, cx + 14 * u, cy + 10 * u],
                    outline=fg, width=max(3, int(4 * u)))
        for i in (-1, 0, 1):
            d.line([cx + i * 18 * u, cy - 34 * u, cx + i * 18 * u, cy - 22 * u],
                   fill=fg, width=max(3, int(4 * u)))
            d.line([cx + i * 18 * u, cy + 22 * u, cx + i * 18 * u, cy + 34 * u],
                   fill=fg, width=max(3, int(4 * u)))
            d.line([cx - 42 * u, cy + i * 14 * u, cx - 30 * u, cy + i * 14 * u],
                   fill=fg, width=max(3, int(4 * u)))
            d.line([cx + 30 * u, cy + i * 14 * u, cx + 42 * u, cy + i * 14 * u],
                   fill=fg, width=max(3, int(4 * u)))
    elif kind == "ship":
        d.polygon([(cx - 42 * u, cy - 2 * u), (cx + 42 * u, cy - 2 * u),
                   (cx + 28 * u, cy + 26 * u), (cx - 28 * u, cy + 26 * u)],
                  fill=fg)
        d.rectangle([cx - 16 * u, cy - 20 * u, cx + 10 * u, cy - 2 * u], fill=fg)
        d.line([cx + 10 * u, cy - 38 * u, cx + 10 * u, cy - 2 * u],
               fill=fg, width=max(3, int(4 * u)))
        d.polygon([(cx + 10 * u, cy - 38 * u), (cx + 30 * u, cy - 30 * u),
                   (cx + 10 * u, cy - 22 * u)], fill=fg)
        for dx in (-30, 0, 30):
            d.arc([cx + (dx - 14) * u, cy + 32 * u, cx + (dx + 14) * u, cy + 46 * u],
                  0, 180, fill=fg, width=max(3, int(4 * u)))
    elif kind == "shield":
        d.polygon([(cx - 30 * u, cy - 32 * u), (cx + 30 * u, cy - 32 * u),
                   (cx + 30 * u, cy + 2 * u), (cx, cy + 36 * u),
                   (cx - 30 * u, cy + 2 * u)], fill=fg)
        d.line([cx - 14 * u, cy + 0 * u, cx - 3 * u, cy + 12 * u,
                cx + 16 * u, cy - 14 * u], fill=NAVY,
               width=max(3, int(5 * u)), joint="curve")
    elif kind == "building":
        d.rectangle([cx - 30 * u, cy - 32 * u, cx + 30 * u, cy + 34 * u], fill=fg)
        for r in range(3):
            for c in range(2):
                d.rectangle(
                    [cx + (-22 + c * 26) * u, cy + (-22 + r * 20) * u,
                     cx + (-10 + c * 26) * u, cy + (-10 + r * 20) * u],
                    fill=NAVY)
        d.rectangle([cx - 8 * u, cy + 18 * u, cx + 8 * u, cy + 34 * u], fill=NAVY)
    elif kind == "globe":
        d.ellipse([cx - 34 * u, cy - 34 * u, cx + 34 * u, cy + 34 * u],
                  outline=fg, width=max(3, int(4 * u)))
        d.ellipse([cx - 14 * u, cy - 34 * u, cx + 14 * u, cy + 34 * u],
                  outline=fg, width=max(3, int(3 * u)))
        d.line([cx - 34 * u, cy, cx + 34 * u, cy], fill=fg,
               width=max(3, int(3 * u)))
        d.arc([cx - 34 * u, cy - 18 * u, cx + 34 * u, cy + 18 * u], 200, 340,
              fill=fg, width=max(3, int(3 * u)))
        d.arc([cx - 34 * u, cy - 18 * u, cx + 34 * u, cy + 18 * u], 20, 160,
              fill=fg, width=max(3, int(3 * u)))
    elif kind == "capitol":
        d.polygon([(cx - 34 * u, cy - 6 * u), (cx, cy - 34 * u),
                   (cx + 34 * u, cy - 6 * u)], fill=fg)
        for c in (-22, 0, 22):
            d.rectangle([cx + (c - 5) * u, cy - 2 * u, cx + (c + 5) * u,
                         cy + 26 * u], fill=fg)
        d.rectangle([cx - 38 * u, cy + 26 * u, cx + 38 * u, cy + 34 * u], fill=fg)
        d.ellipse([cx - 8 * u, cy - 42 * u, cx + 8 * u, cy - 28 * u], fill=fg)
    elif kind == "flame":
        d.polygon([(cx, cy - 38 * u), (cx + 16 * u, cy - 12 * u),
                   (cx + 28 * u, cy + 6 * u), (cx + 20 * u, cy + 30 * u),
                   (cx - 20 * u, cy + 30 * u), (cx - 28 * u, cy + 6 * u),
                   (cx - 16 * u, cy - 12 * u)], fill=fg)
        d.polygon([(cx, cy + 2 * u), (cx + 10 * u, cy + 14 * u),
                   (cx + 6 * u, cy + 26 * u), (cx - 6 * u, cy + 26 * u),
                   (cx - 10 * u, cy + 14 * u)], fill=RED)


# ---- masthead -------------------------------------------------------------
text_cx(W // 2, 12, "THE WORLD IN ONE DAY", serif_b(54), INK)
d.line([16, 78, 1008, 78], fill=LINE, width=2)
text_cx(W // 2, 86, "MONDAY, 23 NOVEMBER 2026", sans_b(30), RED)
d.line([16, 124, 1008, 124], fill=INK, width=3)

# ---- hero A: Nvidia --------------------------------------------------------
box = (16, 134, 1008, 316)
d.rectangle(box, fill=CARD, outline=LINE, width=2)
d.rectangle([16, 134, 196, 316], fill=RED)
icon("chip", 106, 225, 110, (255, 255, 255))
tx = 214
d.text((tx, 146), "TOP STORY  ·  MARKETS", font=sans_b(17), fill=RED)
chip(1008 - 86, 144, "23 NOV", RED)
d.text((tx, 168), "HUANG IS BACK", font=sans_b(50), fill=INK)
sub = wrap("Nvidia reinstates Jensen Huang as CEO — shares jump 31%, Nasdaq +6%",
           sans(23), 1008 - tx - 16)
y = 226
for ln in sub:
    d.text((tx, y), ln, font=sans(23), fill=INK)
    y += 29
d.text((tx, y + 2),
       "Board acted 11 days after his resignation; Trump had pressed for his return.",
       font=sans(18), fill=GRAY)

# ---- hero B: Merkury -------------------------------------------------------
box = (16, 328, 1008, 490)
d.rectangle(box, fill=CARD, outline=LINE, width=2)
d.rectangle([16, 328, 196, 490], fill=NAVY)
icon("ship", 106, 409, 110, (255, 255, 255))
tx = 214
d.text((tx, 340), "WAR AT SEA", font=sans_b(17), fill=NAVY)
chip(1008 - 86, 338, "23 NOV", NAVY)
d.text((tx, 362), "UKRAINE SINKS RUSSIAN CORVETTE", font=sans_b(36), fill=INK)
sub = wrap("Zelenskyy: seven sea drones sank the Merkury off Benghazi; a Ka-27 "
           "helicopter aboard was destroyed.", sans(21), 1008 - tx - 16)
y = 408
for ln in sub:
    d.text((tx, y), ln, font=sans(21), fill=INK)
    y += 27
d.text((tx, y + 2), "Attack was early Sunday; Kyiv released the video on Monday.",
       font=sans(18), fill=GRAY)

d.line([16, 502, 1008, 502], fill=INK, width=2)

# ---- grid: 2 cols x 3 rows --------------------------------------------------
stories = [
    ("ship", NAVY, "TANKER ATTACKS HIT RECORD HIGH",
     "Three tankers struck Fri–Sat; 22 attacks in Nov, most since the war began",
     "22 NOV", NAVY),
    ("shield", NAVY, "NATO MEETS AFTER POLAND INCURSION",
     "Emergency council today; 3 Russian objects crossed Fri 20 Nov",
     "23 NOV", RED),
    ("building", RED, "15 KILLED IN STRIKES NEAR KYIV",
     "Dymer block hit overnight Sun; rescuers search rubble Mon",
     "23 NOV", RED),
    ("globe", NAVY, "CLIMATE TALKS COLLAPSE — NO DEAL",
     "Longest COP ever ends Sun without agreement on fossil fuels",
     "22 NOV", NAVY),
    ("capitol", RED, "DEMOCRATS TAKE 258 SEATS",
     "Biggest House majority since 1992; Hubbard beats Foxx in N. Carolina",
     "22 NOV", NAVY),
    ("flame", RED, "24 DEAD IN FACTORY FIRE",
     "Banten candy plant burned Sat; toll confirmed Mon, ~30 missing",
     "23 NOV", RED),
]

gx0, gy0 = 16, 514
cw, ch, gap = 488, 136, 12
for i, (kind, accent, head, body, date, chip_bg) in enumerate(stories):
    x = gx0 + (i % 2) * (cw + gap)
    y = gy0 + (i // 2) * (ch + gap)
    d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=LINE, width=2)
    d.rectangle([x, y, x + 64, y + ch], fill=accent)
    icon(kind, x + 32, y + ch // 2, 44, (255, 255, 255))
    tx = x + 78
    tw = x + cw - 14 - tx
    chip(x + cw - 89, y + 10, date, chip_bg)
    lines = wrap(head, sans_b(22), tw - 95)
    ly = y + 12
    for ln in lines[:2]:
        d.text((tx, ly), ln, font=sans_b(22), fill=INK)
        ly += 27
    blines = wrap(body, sans(16), tw)
    for ln in blines[:2]:
        d.text((tx, ly), ln, font=sans(16), fill=GRAY)
        ly += 21

# ---- footer ----------------------------------------------------------------
d.line([16, 964, 1008, 964], fill=INK, width=2)
text_cx(W // 2, 974,
        "DATE CHECK — 5 stories from 23 Nov · 3 from the weekend (22 Nov) "
        "that led Monday's news.",
        sans_b(16), INK)
text_cx(W // 2, 996, "Sources: Reuters · CNN · AP · WSJ — 23 Nov 2026",
        sans(14), GRAY)

img.save("entry.png")
print("saved entry.png", img.size)
