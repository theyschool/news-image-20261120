#!/usr/bin/env python3
"""Render the 20 November 2026 world-news poster (1024x1024 PNG).

Deterministic: fixed fonts, fixed layout, no timestamps, no randomness.
All text is drawn with PIL using real system fonts - no AI-generated text.
Run: python3 build_image.py  -> writes entry.png next to this file.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/noto"

# Palette
PAPER = (247, 243, 234)      # warm off-white
INK = (17, 24, 39)           # near-black
NAVY = (15, 42, 68)          # masthead band
GOLD = (201, 162, 39)        # masthead rule
RED = (178, 34, 34)          # lead accent
TEAL = (14, 116, 116)        # kicker accent
GREY = (90, 96, 108)         # secondary text
PALE_BLUE = (203, 213, 225)  # decorative rings
RULE = (200, 192, 176)       # hairline rules


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("NotoSans-Black.ttf", 70)
F_DATE = font("NotoSans-Bold.ttf", 26)
F_KICKER = font("NotoSans-Bold.ttf", 23)
F_LEAD = font("NotoSans-Black.ttf", 66)
F_LEAD_CAP = font("NotoSans-Regular.ttf", 27)
F_FACT = font("NotoSans-Regular.ttf", 24)
F_CELL_KICK = font("NotoSans-Bold.ttf", 20)
F_CELL_HEAD = font("NotoSans-Bold.ttf", 30)
F_CELL_CAP = font("NotoSans-Regular.ttf", 22)
F_FOOT = font("NotoSans-Regular.ttf", 18)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 36                      # side margin
    CW = W - 2 * MX              # content width = 952

    # ---- Masthead: full-bleed navy band ----
    d.rectangle([0, 0, W, 168], fill=NAVY)
    draw_centered(d, 26, "FRIDAY, 20 NOVEMBER 2026", F_DATE, (232, 226, 200))
    draw_centered(d, 62, "THE WORLD IN ONE DAY", F_TITLE, (255, 255, 255))
    d.rectangle([MX, 152, W - MX, 155], fill=GOLD)

    # ---- Lead story: Cyclone Akvan ----
    y = 192
    d.rectangle([MX, y + 4, MX + 8, y + 34], fill=RED)
    d.text((MX + 20, y), "LEAD STORY  ·  ODISHA & ANDHRA PRADESH", font=F_KICKER, fill=RED)

    # Decorative cyclone rings, top-right of the lead block (clear of text).
    cx, cy = 892, 330
    for r, wd in ((118, 3), (88, 3), (58, 4)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=PALE_BLUE, width=wd)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=PALE_BLUE)

    y = 228
    for line in ("CYCLONE AKVAN", "HITS ODISHA"):
        d.text((MX, y), line, font=F_LEAD, fill=INK)
        y += 74
    y = 384
    for line in ("Landfall due around noon — 300,000 evacuated,",
                 "423 rescue teams on standby"):
        d.text((MX, y), line, font=F_LEAD_CAP, fill=(51, 56, 66))
        y += 36
    d.text((MX, 456), "Winds 90–100 kmph, gusts to 110  ·  69 trains cancelled",
           font=F_FACT, fill=GREY)

    # ---- Divider ----
    d.rectangle([MX, 502, W - MX, 504], fill=RULE)

    # ---- 2x2 grid of the other four stories ----
    cells = [
        ("USA  ·  IRAN", "TRUMP PUTS IRAN DECISION OFF TO 2027",
         "Senate rejects war-powers bid 51–48", TEAL),
        ("CRICKET  ·  WELLINGTON", "NICHOLLS & PHILLIPS: TWIN TONS IN WELLINGTON",
         "NZ 257 for 5 — Nicholls 118*, Phillips 103*", TEAL),
        ("TAIWAN  ·  MARKETS", "TAIWAN MOVES TO STEADY STOCKS",
         "Five measures; short-selling limits from today", TEAL),
        ("CRICKET  ·  ASIA CUP", "INDIA A OPEN AGAINST NEPAL IN DOHA",
         "3:30 PM IST, West End Park; Pakistan A v UAE", TEAL),
    ]
    col_w = (CW - 24) // 2        # 464
    row_h = 196
    gx0, gy0 = MX, 524
    for i, (kicker, head, cap, color) in enumerate(cells):
        x = gx0 + (i % 2) * (col_w + 24)
        y = gy0 + (i // 2) * (row_h + 18)
        d.text((x, y), kicker, font=F_CELL_KICK, fill=color)
        lines = wrap(d, head, F_CELL_HEAD, col_w)
        ly = y + 32
        for line in lines:
            d.text((x, ly), line, font=F_CELL_HEAD, fill=INK)
            ly += 37
        d.text((x, ly + 4), cap, font=F_CELL_CAP, fill=GREY)
        # hairline above each cell except the top row is handled by divider
        if i // 2 == 1:
            d.rectangle([x, y - 10, x + col_w, y - 8], fill=RULE)

    # ---- Footer: sources ----
    d.rectangle([MX, 946, W - MX, 948], fill=RULE)
    draw_centered(d, 958, "Sources: IMD · The Hindu · Reuters · BusinessWorld · Cricinfo", F_FOOT, GREY)
    draw_centered(d, 982, "NZ Herald · SimpleLife · Khel Now · The Sports Tak", F_FOOT, GREY)

    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
    print("wrote", OUT)
