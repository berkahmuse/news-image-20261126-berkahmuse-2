#!/usr/bin/env python3
"""news-image-20261126 — entry for @berkahmuse-2.

Draws a dense one-page newspaper collage that sums up the world news of
Thursday 26 November 2026: a masthead, a lead story with a drawn refinery
scene, three featured stories, a 48-story grid grouped by region, and an
"also today" ticker — 56 stories in total, 6 regions.

Deterministic: pure Pillow drawing, no network, no clock, no randomness.
Running it twice writes byte-identical output.

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

PAPER = (246, 241, 230)
INK = (18, 18, 18)
GREY = (90, 86, 78)
RULE = (18, 18, 18)
RED = (176, 32, 32)
BLUE = (31, 78, 156)
GREEN = (30, 122, 70)
ORANGE = (194, 94, 0)
PURPLE = (106, 63, 160)
TEAL = (14, 124, 123)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, width, max_lines):
    """Wrap text, cap at max_lines, ellipsis on the last line if cut."""
    lines = wrap(draw, text, fnt, width)
    if len(lines) <= max_lines:
        return lines
    out = lines[:max_lines]
    last = out[-1]
    while last and draw.textlength(last + "…", font=fnt) > width:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    out[-1] = last + "…"
    return out


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_refinery(draw, x0, y0, x1, y1):
    """Dusk refinery scene, drawn from rectangles, ellipses and polygons."""
    # sky bands
    bands = [(255, 176, 92), (247, 138, 66), (214, 96, 52), (150, 62, 58)]
    bh = (y1 - y0) // 4
    for i, col in enumerate(bands):
        draw.rectangle([x0, y0 + i * bh, x1, y0 + (i + 1) * bh + 1], fill=col)
    # low sun
    draw.ellipse([x1 - 92, y0 + 18, x1 - 32, y0 + 78], fill=(255, 236, 170))
    # smoke
    for cx, cy, r in [(x0 + 60, y0 + 42, 26), (x0 + 96, y0 + 30, 32),
                      (x0 + 140, y0 + 46, 22), (x1 - 70, y0 + 96, 24)]:
        draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(120, 96, 92))
    ground = y1 - 34
    draw.rectangle([x0, ground, x1, y1], fill=(38, 30, 28))
    # storage tanks
    for tx in (x0 + 18, x0 + 108):
        draw.rectangle([tx, ground - 52, tx + 78, ground], fill=(72, 58, 52))
        draw.ellipse([tx, ground - 62, tx + 78, ground - 42], fill=(96, 78, 70))
    # distillation towers
    for tx, th in ((x0 + 210, 108), (x0 + 252, 128), (x0 + 294, 92)):
        draw.rectangle([tx, ground - th, tx + 26, ground], fill=(52, 44, 42))
        draw.polygon([(tx, ground - th), (tx + 13, ground - th - 18),
                      (tx + 26, ground - th)], fill=(52, 44, 42))
        for wy in range(ground - th + 12, ground - 8, 16):
            draw.rectangle([tx + 4, wy, tx + 22, wy + 5], fill=(255, 176, 92))
    # flame over the middle tower
    fx = x0 + 265
    draw.polygon([(fx - 16, ground - 146), (fx, ground - 190),
                  (fx + 16, ground - 146)], fill=(255, 120, 30))
    draw.polygon([(fx - 8, ground - 146), (fx, ground - 172),
                  (fx + 8, ground - 146)], fill=(255, 220, 90))
    # flame over a tank
    tx = x0 + 57
    draw.polygon([(tx - 13, ground - 52), (tx, ground - 88),
                  (tx + 13, ground - 52)], fill=(255, 120, 30))
    draw.polygon([(tx - 6, ground - 52), (tx, ground - 72),
                  (tx + 6, ground - 52)], fill=(255, 220, 90))
    # caption tag
    draw.rectangle([x0, y1 - 20, x0 + 208, y1], fill=(18, 18, 18))
    draw.text((x0 + 8, y1 - 17), "RAS TANURA, SAUDI ARABIA",
              font=font(SANS_B, 10), fill=(255, 255, 255))


# --- story data: 1 lead + 3 featured + 48 grid + 4 ticker = 56 stories ---

FEATURED = [
    ("TRADE", BLUE, "US PROPOSES TARIFFS UP TO 15% ON 14 PARTNERS",
     "China, the EU, India and Taiwan named; markets slide."),
    ("WAR", RED, "UKRAINE HITS TWO RUSSIAN REFINERIES; PUTIN VOWS REVENGE",
     "Samara sites ablaze; Moscow says revenge is \u201cinevitable\u201d."),
    ("GAZA", RED, "ISRAEL KILLS HAMAS SECURITY CHIEF IN GAZA",
     "Mohammad Abuelouf killed with his family, medics say."),
]

# (region, colour, [story, story]) — 24 tiles x 2 stories = 48 stories
GRID = [
    ("MIDDLE EAST", RED, ["Saudi coalition: four drones downed over Ras Tanura",
                           "Houthi projectile hits Jazan port; minor damage"]),
    ("MIDDLE EAST", RED, ["US tells citizens to leave Iran after Riyadh tower attack",
                           "Iran says it shot down two US drones near Hormuz"]),
    ("MIDDLE EAST", RED, ["Two oil tankers hit naval mines in Strait of Hormuz",
                           "Two Libyan officers die in drone strike on Russian warship"]),
    ("MIDDLE EAST", RED, ["Libya vows retaliation after Benghazi strike",
                           "Coalition strikes Hodeidah port after refinery claim"]),
    ("MIDDLE EAST", RED, ["India condemns Riyadh attack; two Indians hurt, discharged",
                           "Gaza families fear violence near camps as truce frays"]),
    ("MIDDLE EAST", RED, ["Sudan drone strikes kill 19 civilians",
                           "Arab states condemn attacks; oil prices rise 2%"]),
    ("AMERICAS", BLUE, ["Trump unveils new global tariffs on Japan, China, EU",
                         "Huawei guilty on 10 of 12 counts in Brooklyn trial"]),
    ("AMERICAS", BLUE, ["Trump: Nvidia CEO pardon is \u201calways an option\u201d",
                         "Vance: Huang won\u2019t need a pardon"]),
    ("AMERICAS", BLUE, ["US Army destroys entire lead-azide stockpile in Iowa",
                         "Abrego Garcia leaves US for Spain"]),
    ("AMERICAS", BLUE, ["Thanksgiving NFL: Bears-Lions, Eagles-Cowboys, Chiefs",
                         "Colombia police free 20 hostages after 17 hours"]),
    ("AMERICAS", BLUE, ["US pauses joint ops with Ecuador over Sept raid probe",
                         "Fed Beige Book: modest growth, sticky prices"]),
    ("AMERICAS", BLUE, ["US attorney general dodges Nvidia probe questions",
                         "US FinCEN systems offline after suspected cyberattack"]),
    ("EUROPE", GREEN, ["Leaked data: 490,334 Russian soldiers dead in Ukraine",
                        "Russia hits Odesa: two killed, child hurt; Kyiv flat ablaze"]),
    ("EUROPE", GREEN, ["UK warns firms of Russian sabotage threat",
                        "Zelenskyy: Ukraine needs EUR 115bn for 2027"]),
    ("EUROPE", GREEN, ["EU proposes EUR 45bn Ukraine loan",
                        "Xi graft probe hits Shanghai rising star"]),
    ("EUROPE", GREEN, ["Lille stun Bayern in Champions League",
                        "Sporting 2-2 Man Utd: Fernandes double, VAR drama"]),
    ("ASIA-PACIFIC", ORANGE, ["Pakistan\u2019s first astronaut to fly Shenzhou-24 to Tiangong",
                               "Taiwan shares plunge 1,927 pts; dollar past 33"]),
    ("ASIA-PACIFIC", ORANGE, ["India marks Constitution Day; 18 years since 26/11",
                               "IITs to add 6,000 seats in robotics, AI, space"]),
    ("ASIA-PACIFIC", ORANGE, ["India unveils Rs 15,000-crore package for Nepal",
                               "Hasina seeks return to Bangladesh on Dec 16"]),
    ("ASIA-PACIFIC", ORANGE, ["Bangladesh raises garment wage 36%",
                               "Flipkart CEO to step down in December"]),
    ("SPORT & SCIENCE", TEAL, ["Gukesh faces Sindarov at World Chess Championship",
                                "Sooryavanshi, 15, hits fastest List A double ton"]),
    ("SPORT & SCIENCE", TEAL, ["IPL 2027 auction draws 1,220 players",
                                "Sterling spared jail over dangerous driving"]),
    ("SPORT & SCIENCE", TEAL, ["AI-bubble fears hit tech stocks; Nvidia down 8%",
                                "US tightens remote AI-chip access rules"]),
    ("SPORT & SCIENCE", TEAL, ["Wolbachia mosquitoes cut Brazil infections 68%",
                                "Cairo tanker fire kills at least 31"]),
]

TICKER = ("DART asteroid close-ups to be revealed  •  India\u2019s space economy: "
          "$9bn to $45bn  •  Biovac scales vaccines with EU loan  •  "
          "Fiji polls on track")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([6, 6, W - 7, H - 7], outline=RULE, width=3)

    # ---- masthead ----
    d.rectangle([16, 14, W - 17, 16], fill=RULE)
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 24), title, font=tf, fill=INK)
    sub = ("THURSDAY 26 NOVEMBER 2026   •   56 STORIES   •   6 REGIONS   •   "
           "EVERY CLAIM VERIFIED AS REPORTED")
    sf = font(SANS_B, 15)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 92), sub, font=sf, fill=RED)
    d.rectangle([16, 116, W - 17, 118], fill=RULE)

    # ---- lead story ----
    lx, lw = 22, 630
    d.text((lx, 130), "LEAD  —  MIDDLE EAST  •  ENERGY", font=font(SANS_B, 13), fill=RED)
    head = "HOUTHIS HIT SAUDI REFINERY AS BRENT TOPS $94"
    hf = font(SERIF_B, 33)
    y = text_block(d, lx, 152, fit_lines(d, head, hf, lw, 3), hf, INK, 40)
    deck = ("Yemen\u2019s Houthis say they struck Ras Tanura, the kingdom\u2019s largest "
            "refinery; the Saudi-led coalition says four drones were downed and "
            "fires broke out. Oil jumped more than 2%.")
    y = text_block(d, lx, y + 8, fit_lines(d, deck, font(SANS, 15), lw, 3),
                   font(SANS, 15), (52, 50, 46), 20)
    d.text((lx, 300), "OIL $94+  •  550,000 BARRELS A DAY AT RISK",
           font=font(SANS_B, 12), fill=GREY)
    draw_refinery(d, 668, 126, 1002, 322)
    d.rectangle([16, 330, W - 17, 332], fill=RULE)

    # ---- three featured stories ----
    fx, fw, gap = 16, 322, 7
    for i, (tag, col, h, deck) in enumerate(FEATURED):
        x = fx + i * (fw + gap)
        d.rectangle([x, 340, x + fw, 344], fill=col)
        d.text((x, 350), tag, font=font(SANS_B, 12), fill=col)
        hf2 = font(SERIF_B, 18)
        y = text_block(d, x, 366, fit_lines(d, h, hf2, fw, 3), hf2, INK, 22)
        text_block(d, x, y + 4, fit_lines(d, deck, font(SANS, 11), fw, 2),
                   font(SANS, 11), (52, 50, 46), 12)
    d.rectangle([16, 466, W - 17, 468], fill=RULE)

    # ---- section header ----
    d.text((16, 476), "THE DAY IN 48 MORE STORIES — BY REGION",
           font=font(SANS_B, 14), fill=INK)
    d.rectangle([16, 498, W - 17, 500], fill=RULE)

    # ---- 48-story grid: 6 rows x 4 cols, 2 stories per tile ----
    gx, gy = 16, 508
    tw, th, tgap = 239, 64, 6
    for row in range(6):
        for col_i in range(4):
            region, colour, stories = GRID[row * 4 + col_i]
            x = gx + col_i * (tw + tgap)
            y = gy + row * (th + tgap)
            d.rectangle([x, y, x + tw, y + th], outline=(190, 184, 170), width=1)
            d.rectangle([x, y, x + tw, y + 4], fill=colour)
            d.text((x + 6, y + 7), region, font=font(SANS_B, 9), fill=colour)
            yy = y + 19
            for story in stories:
                lines = fit_lines(d, story, font(SANS_B, 10), tw - 12, 2)
                yy = text_block(d, x + 6, yy, lines, font(SANS_B, 10), INK, 11)
                yy += 1

    # ---- ticker ----
    ty = 928
    d.rectangle([16, ty, W - 17, ty + 36], fill=INK)
    tf2 = font(SANS_B, 13)
    d.text((26, ty + 10), "ALSO TODAY:", font=tf2, fill=(255, 200, 90))
    tx = 26 + int(d.textlength("ALSO TODAY:  ", font=tf2))
    d.text((tx, ty + 11), TICKER, font=font(SANS, 12), fill=(255, 255, 255))

    # ---- footer ----
    foot = ("Drawn entirely by code — no photographs. Every story above was first "
            "reported on 26 November 2026 in at least one time zone; wording follows "
            "the reporting, without hype or speculation. Sources: AP, Reuters, BBC, AFP.")
    text_block(d, 22, 972, fit_lines(d, foot, font(SANS, 10), W - 44, 2),
               font(SANS, 10), GREY, 13)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
