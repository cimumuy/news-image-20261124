#!/usr/bin/env python3
"""Draw "The World in One Page: Tuesday 24 November 2026" as a single PNG.

A dense broadsheet front page rendered with Pillow only. The output is
fully deterministic: fixed text, fixed fonts, no randomness, no clock.
Running it twice produces byte-identical files.

Usage: python3 compose.py [output-path]   (default: entry.png)
"""

import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- setup

W = H = 1024
MX = 16                      # side margin
CW = W - 2 * MX              # content width

PAPER = (247, 243, 234)      # #f7f3ea
INK = (26, 23, 18)           # #1a1712
RED = (143, 29, 34)          # #8f1d22

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
SERIF = FONT_DIR + "LiberationSerif-Regular.ttf"
SERIF_B = FONT_DIR + "LiberationSerif-Bold.ttf"
SERIF_I = FONT_DIR + "LiberationSerif-Italic.ttf"
SANS = FONT_DIR + "LiberationSans-Regular.ttf"
SANS_B = FONT_DIR + "LiberationSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def text_h(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[3] - box[1], box[1]  # (glyph height, ascender-to-glyph-top)


def fit_font(draw, text, path, max_size, max_width, min_size=10):
    """Largest font size <= max_size whose single line fits max_width."""
    size = max_size
    while size > min_size:
        fnt = font(path, size)
        if text_w(draw, text, fnt) <= max_width:
            return fnt
        size -= 1
    return font(path, min_size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that each fit max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if text_w(draw, trial, fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill):
    """Draw text horizontally centred on cx with its glyph top at y."""
    h, off = text_h(draw, text, fnt)
    draw.text((cx - text_w(draw, text, fnt) / 2, y - off), text,
              font=fnt, fill=fill)
    return h


def draw_left(draw, x, y, text, fnt, fill):
    h, off = text_h(draw, text, fnt)
    draw.text((x, y - off), text, font=fnt, fill=fill)
    return h


def rule(draw, x0, x1, y, width, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)

# ---------------------------------------------------------------- content

MASTHEAD = "THE WORLD IN ONE PAGE"

LEAD_HEADLINE = "JENSEN HUANG REINSTATED AS NVIDIA CEO"
LEAD_SUB = ("Trump intervenes after shock ouster - Nvidia shares leap 31% "
            "and chip stocks rally worldwide")

BAND_LINE_1 = "TUESDAY"
BAND_LINE_2 = "24 NOVEMBER 2026"

SECONDARIES = [
    ("UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
     "Sea drones strike a corvette at Benghazi; a second ship hit in the "
     "Gulf of Finland"),
    ("TRUMP TO MEET NATO CHIEF RUTTE ON WEDNESDAY",
     "Florida talks follow Putin and Xi meetings; Europe demands a seat "
     "at the Ukraine table"),
    ("NATO VOWS SPACE DEFENCE OVER RUSSIAN NUCLEAR SATELLITE",
     "Alliance responds to reports Moscow may put a nuclear weapon in "
     "orbit by December"),
]

BRIEFS = [
    "UN COURT: MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA",
    "EU PROPOSES 22ND SANCTIONS PACKAGE ON RUSSIA",
    "LAGARDE RESIGNS; EU HUNTS FOR NEW ECB CHIEF",
    "SEOUL SCRAMBLES JETS AS RUSSIAN AIRCRAFT NEAR ISLAND",
    "ISRAELI DRONE STRIKE KILLS THREE AT GAZA POLICE POST",
    "ISRAEL BEGINS GROUND OPERATION IN CENTRAL GAZA",
    "SETTLER ARSON DENOUNCED AS 'JEWISH TERRORISM'",
    "US SANCTIONS IRAN SHADOW-BANKING NETWORK",
    "MEXICO TO TRY 'EL CHAPO ISIDRO', DEFYING US",
    "CAR BOMB HITS GOVERNOR'S OFFICE IN COLOMBIA",
    "DEADLY STORM DISPLACES THOUSANDS IN BRAZIL",
    "BOLSONARO BACK IN JAIL IN SAO PAULO",
    "INDONESIA FACTORY FIRE: WORKERS STILL MISSING",
    "MIGRANT BOAT CAPSIZES OFF SENEGAL; DOZENS MISSING",
    "RSF DRONES BLACK OUT SUDAN POWER STATIONS",
    "SAHEL STATES RESTART TALKS WITH WEST AFRICA BLOC",
    "KENYA LANDS 293,600 JOBS IN SAUDI ARABIA",
    "KENYA DISCHARGES LAST EBOLA PATIENT",
    "TANZANIA OPPOSITION OFFICIAL CHARGED WITH TREASON",
    "SOUTH AFRICANS VOTE AMID ANGER AT ANC",
    "UN CHIEF: AGREE GLOBAL AI RULES WITHIN A YEAR",
    "US BLACKLISTS MEGASPEED IN NVIDIA SCANDAL",
    "WAYMO PULLS DRIVERLESS TAXIS FROM US FREEWAYS",
    "ICE ARRESTS AT SEATTLE AIRPORT SPARK OUTCRY",
    "OIL FALLS 3% AS LIBYAN PIPELINE RESTARTS",
    "SK HYNIX SHARES JUMP 20% ON HUANG RETURN",
    "INDIA HOLDS THIRD PLACE IN ASIA POWER INDEX",
    "CHINA SENTENCES OFFICIAL TO DEATH FOR SPYING",
    "NORWAY COURT VOIDS DISPUTED OIL LICENCES",
    "DENMARK TOP COURT UPHOLDS 'GHETTO LAW'",
    "SINGAPORE, AUSTRALIA SIGN PARTNERSHIP PACTS",
    "SPORT: TRESOLDI HAT-TRICK SINKS INTER AT SAN SIRO",
    "SPORT: AUSTRALIA ON TOP IN SOUTH AFRICA DECIDER",
]

FOOTER = "All the day's news, in one page - Tuesday 24 November 2026"

# ---------------------------------------------------------------- layout

def split_columns(wrapped):
    """Split sequentially wrapped briefs into 3 columns of balanced line
    counts, preserving the reading order down each column."""
    total = sum(len(b) for b in wrapped)
    target = -(-total // 3)
    columns, current, count = [], [], 0
    for brief in wrapped:
        if current and count + len(brief) > target and len(columns) < 2:
            columns.append(current)
            current, count = [], 0
        current.append(brief)
        count += len(brief)
    columns.append(current)
    return columns


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    cx = W // 2

    # --- masthead ------------------------------------------------------
    rule(draw, MX, W - MX, 14, 3)
    rule(draw, MX, W - MX, 20, 1)
    mast_font = fit_font(draw, MASTHEAD, SERIF_B, 52, CW)
    y = 27
    y += draw_centered(draw, cx, y, MASTHEAD, mast_font, INK)
    y += 5
    rule(draw, MX, W - MX, y, 1)
    rule(draw, MX, W - MX, y + 6, 3)
    y += 11

    # --- lead story ----------------------------------------------------
    lead_font = font(SERIF_B, 64)
    lead_lines = wrap(draw, LEAD_HEADLINE, lead_font, CW)
    for line in lead_lines:
        draw_centered(draw, cx, y, line, lead_font, INK)
        y += 55
    y += 2
    sub_font = font(SERIF, 22)
    for line in wrap(draw, LEAD_SUB, sub_font, CW):
        draw_centered(draw, cx, y, line, sub_font, INK)
        y += 22
    y += 5
    rule(draw, MX, W - MX, y, 1)
    y += 9

    # --- secondary stories ---------------------------------------------
    for i, (head, sub) in enumerate(SECONDARIES):
        head_font = fit_font(draw, head, SANS_B, 30, CW, min_size=20)
        draw_left(draw, MX, y, head, head_font, INK)
        y += 28
        sub2_font = fit_font(draw, sub, SANS, 20, CW, min_size=14)
        draw_left(draw, MX, y, sub, sub2_font, INK)
        y += 19
        if i < len(SECONDARIES) - 1:
            y += 4

    # --- date band (vertical centre of the page) ------------------------
    band_f1 = fit_font(draw, BAND_LINE_1, SERIF_B, 120, CW)
    band_f2 = fit_font(draw, BAND_LINE_2, SERIF_B, 120, CW)
    bh1, _ = text_h(draw, BAND_LINE_1, band_f1)
    bh2, _ = text_h(draw, BAND_LINE_2, band_f2)
    band_h = bh1 + bh2 + 14
    band_top = y + 8
    draw.rectangle([0, band_top, W, band_top + band_h], fill=RED)
    by = band_top + 6
    draw_centered(draw, cx, by, BAND_LINE_1, band_f1, PAPER)
    by += bh1 + 2
    draw_centered(draw, cx, by, BAND_LINE_2, band_f2, PAPER)
    band_bottom = band_top + band_h

    # --- briefs grid ------------------------------------------------------
    footer_rule_y = H - 30
    region_top = band_bottom + 10
    region_h = footer_rule_y - 6 - region_top
    gutter = 10
    col_w = (CW - 2 * gutter) // 3
    brief_font = font(SANS, 19)
    wrapped = [wrap(draw, b, brief_font, col_w - 11) for b in BRIEFS]
    columns = split_columns(wrapped)
    line_counts = [sum(len(b) for b in col) for col in columns]
    max_lines = max(line_counts)
    max_briefs = max(len(col) for col in columns)
    lh = min(20, (region_h - (max_briefs - 1) * 2) // max_lines)
    briefs_bottom = region_top
    for ci, col in enumerate(columns):
        col_x = MX + ci * (col_w + gutter)
        cy = region_top
        for lines in col:
            draw.rectangle([col_x, cy + 5, col_x + 6, cy + 11], fill=RED)
            for line in lines:
                draw_left(draw, col_x + 11, cy, line, brief_font, INK)
                cy += lh
            cy += 2
        briefs_bottom = max(briefs_bottom, cy - 2)

    # --- footer -----------------------------------------------------------
    rule(draw, MX, W - MX, footer_rule_y, 1)
    foot_font = font(SERIF_I, 15)
    draw_centered(draw, cx, footer_rule_y + 6, FOOTER, foot_font, INK)

    img.save(out_path)
    print(f"wrote {out_path}")
    print(f"lead lines: {len(lead_lines)}; band: {band_top}..{band_bottom} "
          f"(centre {band_top + band_h // 2}); brief lines/col: "
          f"{line_counts}; lh {lh}; briefs bottom: {briefs_bottom}; "
          f"footer rule: {footer_rule_y}")


if __name__ == "__main__":
    main()
