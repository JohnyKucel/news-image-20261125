#!/usr/bin/env python3
"""Pre-render step for news-image-20261125 (PIL allowed HERE only).

Renders every text tile and illustration into assets/ as PNGs.
main.py (stdlib-only) then assembles them into out/entry.png.
Deterministic: fixed seed, no timestamps, no random without seed.
Run: python3 build_assets.py  (from the repo root)
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

INK = (17, 17, 17)
PAPER = (241, 236, 224)
CREAM = (245, 240, 228)
NAVY = (34, 48, 74)
SLATE = (58, 67, 86)
RED = (166, 27, 27)
DIVIDER = (180, 170, 145)
MUTED = (96, 90, 74)
OCHRE = (185, 138, 47)
LIGHTPANEL = (233, 224, 205)

F_DIR = "/usr/share/fonts/truetype"
DISPLAY = os.path.join(F_DIR, "noto/NotoSerifDisplay-Black.ttf")
DISPLAY_B = os.path.join(F_DIR, "noto/NotoSerifDisplay-Bold.ttf")
SERIF = os.path.join(F_DIR, "dejavu/DejaVuSerif.ttf")
SERIF_B = os.path.join(F_DIR, "dejavu/DejaVuSerif-Bold.ttf")
SANS = os.path.join(F_DIR, "dejavu/DejaVuSans.ttf")
SANS_B = os.path.join(F_DIR, "dejavu/DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def save(img, name):
    img.save(os.path.join(ASSETS, name), "PNG")
    print("wrote", name, img.size)


def tile(w, h, bg=None):
    if bg is None:
        return Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return Image.new("RGBA", (w, h), bg + (255,))


# ---------------------------------------------------------------- text tiles
def topband():
    img = tile(976, 18)
    d = ImageDraw.Draw(img)
    f = font(SANS_B, 10)
    d.text((0, 3), "WEDNESDAY 25 NOVEMBER 2026", font=f, fill=INK)
    right = "35 DATED STORIES  \u00b7  8 REGIONS  \u00b7  SOURCES: REUTERS, CNN, AP, COINDESK"
    d.text((976 - d.textlength(right, font=f), 3), right, font=f, fill=INK)
    save(img, "t_topband.png")


def masthead():
    img = tile(976, 88)
    d = ImageDraw.Draw(img)
    f = font(SANS, 10)
    d.text((0, 34), "EST. 1851", font=f, fill=INK)
    d.text((0, 48), "ONE DAY, ONE PAGE", font=f, fill=MUTED)
    right1 = "PRICE: FREE"
    right2 = "WEDNESDAY 25 NOV 2026"
    d.text((976 - d.textlength(right1, font=f), 34), right1, font=f, fill=INK)
    d.text((976 - d.textlength(right2, font=f), 48), right2, font=f, fill=MUTED)
    mf = font(DISPLAY, 80)
    t = "THE WORLD"
    d.text(((976 - d.textlength(t, font=mf)) / 2, 0), t, font=mf, fill=INK)
    d.line([(0, 86), (976, 86)], fill=INK, width=2)
    save(img, "t_masthead.png")


def ticker():
    img = tile(976, 20)
    d = ImageDraw.Draw(img)
    f = font(SANS, 11)
    d.text((0, 4), "LONDON  \u00b7  NEW YORK  \u00b7  TOKYO", font=f, fill=INK)
    right = ("BTC $59,100 \u25bc2.1%   \u00b7   ETH $1,660 \u25bc2.4%   \u00b7   "
             "SOL $68.70 \u25bc4.0%   \u00b7   FEAR & GREED 13 \u2014 EXTREME FEAR")
    d.text((976 - d.textlength(right, font=f), 4), right, font=f, fill=RED)
    save(img, "t_ticker.png")


STATS = [
    ("$952BN", "NVIDIA GAIN IN ONE DAY"),
    ("204 / 53", "SOORYAVANSHI, 15 \u2014 BALLS FACED"),
    ("$569.7M", "BTC ETF OUTFLOW, MONDAY"),
    ("-5.6%", "KOSPI, WEDNESDAY"),
    ("$59,100", "BITCOIN, WED 07:20 UTC"),
    ("26", "MINERS TRAPPED, BOGOR"),
]


def stats():
    img = tile(976, 36)
    d = ImageDraw.Draw(img)
    big = font(DISPLAY_B, 19)
    lab = font(SANS, 8)
    cw = 976 // 6
    for i, (num, label) in enumerate(STATS):
        x = i * cw + (8 if i else 0)
        d.text((x, 0), num, font=big, fill=INK)
        d.text((x, 25), label, font=lab, fill=MUTED)
        if i:
            d.line([(i * cw, 2), (i * cw, 34)], fill=DIVIDER, width=1)
    save(img, "t_stats.png")


def regions():
    img = tile(976, 16)
    d = ImageDraw.Draw(img)
    f = font(SANS_B, 11)
    t = ("NORTH AMERICA  \u00b7  SOUTH AMERICA  \u00b7  EUROPE  \u00b7  MIDDLE EAST  \u00b7  "
         "ASIA-PACIFIC  \u00b7  AFRICA  \u00b7  OCEANIA  \u00b7  SPACE")
    d.text(((976 - d.textlength(t, font=f)) / 2, 2), t, font=f, fill=INK)
    save(img, "t_regions.png")


def feature():
    img = tile(976, 104)
    d = ImageDraw.Draw(img)
    kf = font(SANS_B, 11)
    d.text((0, 0), "TECH  \u00b7  WHITE HOUSE  \u00b7  TUESDAY 24 NOVEMBER 2026", font=kf, fill=RED)
    hf = font(DISPLAY, 30)
    d.text((0, 14), "HUANG IS BACK \u2014 AND SAYS SORRY", font=hf, fill=INK)
    df = font(SERIF, 15)
    deck = ("Nvidia\u2019s board restores its chief 11 days after he quit; Trump called the board himself.")
    d.text((0, 50), deck, font=df, fill=INK)
    bf = font(SERIF, 12)
    body = ("Jensen Huang apologised to staff on Tuesday, a day after Nvidia\u2019s board unanimously "
            "restored him as chief executive. Shares soared 31.5% on Monday to about $165 \u2014 "
            "adding roughly $952bn in a day \u2014 then fell 5.9% on Tuesday. Inquiries continue.")
    y = 70
    for line in wrap(d, body, bf, 976):
        d.text((0, y), line, font=bf, fill=INK)
        y += 16
    save(img, "t_feat0.png")


SMALL = [
    ("MARKETS \u00b7 WED 25 NOV", "ASIA SINKS AS AI RALLY DIES",
     "Kospi \u22125.6%, Taiex \u22126%, Nikkei \u22123.6%. Nasdaq fell first."),
    ("TRADE \u00b7 TUE 24 NOV", "US READIES TARIFFS ON 16 PARTNERS",
     "Trump team set to unveil USTR findings. Rates not yet out."),
    ("SPACE \u00b7 WED 25 NOV", "FIRST FOREIGNER REACHES TIANGONG",
     "Shenzhou-24 lifts off 00:18 UTC; first Pakistani in orbit."),
    ("INDONESIA \u00b7 MON 23 NOV", "26 MINERS TRAPPED IN FLOODED PIT",
     "Illegal miners stuck 100m down at Gunung Butak after floods."),
    ("CLIMATE \u00b7 SUN 22 NOV", "COP31 ENDS WITH NO DEAL",
     "First climate summit to fail since Copenhagen 2009."),
    ("WAR \u00b7 TUE 24 NOV", "PUTIN VOWS REFINERY REVENGE",
     "Moscow admits strikes cut refining ~30%."),
    ("COLOMBIA \u00b7 TUE 24 NOV", "30 HOSTAGES IN CARTAGENA STORE",
     "Failed van robbery ends in siege; 10 freed, talks under way."),
    ("CULTURE \u00b7 TUE 24 NOV", "FIRST MOTHER WINS MISS UNIVERSE",
     "Barreto, 27, wins the 75th contest in San Juan."),
    ("CRICKET \u00b7 TUE 24 NOV", "15-YEAR-OLD SMASHES 204 OFF 53",
     "Sooryavanshi hits 28 sixes; India A chase 250 in 14.2 overs."),
    ("WALL ST \u00b7 TUE 24 NOV", "DOW CLOSES ABOVE 50,000 FIRST TIME",
     "Dow +0.9% to 50,019; Nasdaq \u22121.5% as S&P falls again."),
    ("UKRAINE \u00b7 TUE 24 NOV", "ODESA STRIKE KILLS TWO, KYIV HIT",
     "Two killed in Odesa; drones set a Kyiv apartment block ablaze."),
    ("TECH \u00b7 TUE 24 NOV", "MICROSOFT IN \u2018CODE RED\u2019",
     "After a ~24-hour outage, firm vows one-hour recovery."),
]


def small_stories():
    kf = font(SANS_B, 8)
    hf = font(SERIF_B, 12)
    bf = font(SERIF, 9)
    for i, (kick, head, body) in enumerate(SMALL):
        img = tile(160, 66)
        d = ImageDraw.Draw(img)
        d.text((0, 0), kick, font=kf, fill=RED)
        y = 11
        for line in wrap(d, head, hf, 160)[:2]:
            d.text((0, y), line, font=hf, fill=INK)
            y += 15
        y = 41
        for line in wrap(d, body, bf, 160)[:2]:
            d.text((0, y), line, font=bf, fill=INK)
            y += 11
        save(img, "t_small%d.png" % i)


CRYPTO = [
    ("BTC BACK BELOW $60,000", "$59,100, \u22122.1% \u2014 Monday\u2019s rally to $64,500 is gone."),
    ("ETF EXODUS NEARS $5BN IN NOV", "Bitcoin ETFs lost $569.7m on Monday alone."),
    ("ANSEM WALLET DRAINED $2.57M", "Cause disputed; Bullpen admits 18\u201319 accounts hit."),
    ("VELOCITY DEX HALTS TRADING", "Solana perpetuals stop over a software bug."),
    ("SOL ETFS: THE ONLY INFLOW", "+$4.4m last week; tokenised stocks hit $1.8bn."),
]


def crypto():
    img = tile(976, 56, NAVY)
    d = ImageDraw.Draw(img)
    hf = font(SANS_B, 12)
    d.text((10, 4), "CRYPTO NEWS", font=hf, fill=(255, 255, 255))
    rf = font(SANS, 10)
    right = "BTC $59,100 \u25bc2.1%  \u00b7  ETH $1,660 \u25bc2.4%  \u00b7  SOL $68.70 \u25bc4.0%  \u00b7  SNAPSHOT 07:20 UTC"
    d.text((976 - 10 - d.textlength(right, font=rf), 6), right, font=rf, fill=(214, 205, 180))
    d.line([(0, 22), (976, 22)], fill=(120, 125, 145), width=1)
    tf = font(SANS_B, 9)
    bf = font(SANS, 8)
    cw = 976 // 5
    for i, (head, body) in enumerate(CRYPTO):
        x = i * cw + 10
        d.text((x, 26), head, font=tf, fill=(255, 255, 255))
        y = 37
        for line in wrap(d, body, bf, cw - 20)[:2]:
            d.text((x, y), line, font=bf, fill=(214, 205, 180))
            y += 9
        if i:
            d.line([(i * cw, 26), (i * cw, 54)], fill=(120, 125, 145), width=1)
    save(img, "t_crypto.png")


BRIEFS_L = [
    "UKRAINE SINKS RUSSIAN SHIP \u2014 Corvette Merkury sunk off Libya by sea drone, 24 Nov.",
    "NORWAY PLEDGES $7BN FOR UKRAINE \u2014 2027 aid; Russia lifts defence spending 27%.",
    "NATO SENDS AWACS TO POLAND \u2014 After three Russian cruise missiles landed there, 20 Nov.",
    "GERMAN INTEL: NUCLEAR SATELLITE \u2014 Russia may launch an armed satellite in December.",
    "GAZA STRIKE KILLS HAMAS SECURITY CHIEF \u2014 Brig-Gen Naeem Abu Nahal dead, 24 Nov.",
    "ISRAEL: FIRST COALITION PACT \u2014 Eisenkot signs with Lieberman; 48 of 120 seats.",
    "HORMUZ MINES: CLAIM ONLY \u2014 IRGC says three tankers hit; US Central Command denies it.",
    "RUSSIAN JETS ENTER KOREAN ZONE \u2014 Seoul reports jets in its air-defence zone, 25 Nov.",
    "AUSTRALIA\u2013SOLOMONS SECURITY PACT \u2014 Canberra named lead security partner, 25 Nov.",
]
BRIEFS_R = [
    "CONGO REBELS RETREAT \u2014 After heavy fighting in the east, 25 Nov.",
    "TWO HELD OVER WILLIAM BURGLARY \u2014 Arrests after a break-in at the Prince\u2019s home.",
    "DUTCH COURT KEEPS CLIMATE TARGETS \u2014 Binding goals stand during the appeal, 25 Nov.",
    "GOLD $3,549 \u00b7 BRENT $90.05 \u2014 Oil slides on glut fears; gold near a 14-month low.",
    "INDIA\u2013NZ TEST DRAWN \u2014 New Zealand survive 120 overs, 239/5, in Wellington, 23 Nov.",
    "CHESS: GUKESH\u2013SINDAROV DRAW \u2014 Game 1 of the world title ends level, 24 Nov.",
    "ENGLAND LEVEL T20I SERIES \u2014 Eight-wicket win over Australia, 1\u20131, 24 Nov.",
    "FEAR & GREED 13 \u2014 Extreme fear for 10+ days; $472m liquidated in 24 hours.",
]


def briefs():
    img = tile(415, 206)
    d = ImageDraw.Draw(img)
    hf = font(SANS_B, 11)
    d.text((0, 0), "IN BRIEF", font=hf, fill=INK)
    d.line([(0, 15), (415, 15)], fill=INK, width=1)
    bf = font(SERIF, 8)
    y = 20
    for item in BRIEFS_L + BRIEFS_R:
        line = wrap(d, item, bf, 415)
        d.text((0, y), line[0] if line else "", font=bf, fill=INK)
        y += 10
    save(img, "t_briefs.png")


DATECHECK = [
    "COP31: NO deal was reached. Never write \u2018deal agreed\u2019.",
    "Hormuz tankers: an IRGC claim, unverified. CENTCOM denies it.",
    "Ansem drain: cause disputed. Do not call it a proven hack.",
    "US tariffs: reported as ready, NOT announced or in force.",
    "Bogor miners: police say 26; the figure is still moving.",
    "Nvidia: +31.5% Monday, \u22125.9% Tuesday. Different days.",
]


def datecheck():
    img = tile(172, 206)
    d = ImageDraw.Draw(img)
    hf = font(SANS_B, 11)
    d.text((0, 0), "DATE CHECK", font=hf, fill=RED)
    d.line([(0, 15), (172, 15)], fill=RED, width=1)
    bf = font(SERIF, 9)
    y = 20
    for item in DATECHECK:
        for line in wrap(d, item, bf, 172):
            d.text((0, y), line, font=bf, fill=INK)
            y += 11
        y += 6
    save(img, "t_datecheck.png")


TIMELINE = [
    ("24 NOV 07:00", "Ansem wallet drained, $2.57m"),
    ("24 NOV 12:00", "Eisenkot\u2013Lieberman pact signed"),
    ("24 NOV 19:00", "Odesa strike; Huang apologises"),
    ("25 NOV 00:18", "Shenzhou-24 launches"),
    ("25 NOV 03:00", "Asian markets plunge"),
    ("25 NOV 07:20", "Snapshot: BTC $59,100"),
]


def timeline():
    img = tile(330, 72)
    d = ImageDraw.Draw(img)
    hf = font(SANS_B, 11)
    d.text((0, 0), "TIMELINE \u2014 UTC", font=hf, fill=INK)
    d.line([(0, 14), (330, 14)], fill=INK, width=1)
    tf = font(SANS_B, 9)
    bf = font(SANS, 9)
    y = 18
    for t, ev in TIMELINE:
        d.text((0, y), t, font=tf, fill=RED)
        d.text((92, y), ev, font=bf, fill=INK)
        y += 9
    save(img, "t_timeline.png")


def footband():
    img = tile(1024, 24, INK)
    d = ImageDraw.Draw(img)
    f = font(SANS, 10)
    t = ("THE WORLD \u2014 Wednesday 25 November 2026 \u2014 Every story dated 23\u201325 Nov 2026 \u2014 "
         "Sources: Reuters, CNN, AP, CoinDesk, Cointelegraph, The Block \u2014 All drawings original, drawn in code.")
    d.text(((1024 - d.textlength(t, font=f)) / 2, 7), t, font=f, fill=CREAM)
    save(img, "t_footband.png")


# ------------------------------------------------------------- illustrations
def adult_figure(d, cx, top, h, suit, shirt, tie):
    """Modern flat 2D adult: head ~1/7 of height, broad shoulders, suit."""
    head_r = h / 14.0
    head_cy = top + head_r
    d.ellipse([cx - head_r, top, cx + head_r, top + 2 * head_r],
              fill=(232, 190, 150), outline=INK, width=1)
    # hair: dark cap on top half of head
    d.pieslice([cx - head_r, top, cx + head_r, top + 2 * head_r],
               180, 360, fill=(30, 30, 30))
    shoulder_y = top + 2 * head_r + 2
    shoulder_w = h * 0.34
    body_h = h - (shoulder_y - top)
    # jacket: broad shoulders, slight taper
    d.polygon([(cx - shoulder_w / 2, shoulder_y),
               (cx + shoulder_w / 2, shoulder_y),
               (cx + shoulder_w * 0.42, shoulder_y + body_h),
               (cx - shoulder_w * 0.42, shoulder_y + body_h)],
              fill=suit, outline=INK, width=1)
    # shirt V + tie
    d.polygon([(cx - 6, shoulder_y), (cx + 6, shoulder_y),
               (cx, shoulder_y + 16)], fill=shirt, outline=INK, width=1)
    d.polygon([(cx - 3, shoulder_y + 14), (cx + 3, shoulder_y + 14),
               (cx + 2, shoulder_y + 34), (cx - 2, shoulder_y + 34)],
              fill=tie)
    return shoulder_y


def hero():
    W, H = 976, 158
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    # left panel: the empty chair (12 Nov, he quits) — dark navy
    d.rectangle([0, 0, 488, H], fill=NAVY)
    # right panel: the return (23-24 Nov) — light paper
    d.rectangle([488, 0, W, H], fill=LIGHTPANEL)
    d.line([(488, 0), (488, H)], fill=INK, width=2)
    lf = font(SANS_B, 11)
    d.text((14, 10), "MON 12 NOV 2026 \u2014 HE QUITS", font=lf, fill=CREAM)
    d.text((502, 10), "MON 23 NOV \u2014 HE RETURNS  \u00b7  TUE 24 NOV \u2014 APOLOGY",
           font=font(SANS_B, 10), fill=INK)
    # --- left: office, empty chair, desk, crooked picture
    d.rectangle([40, 40, 180, 112], outline=(150, 158, 175), width=2)  # window
    d.line([(40, 76), (180, 76)], fill=(150, 158, 175), width=1)
    d.line([(110, 40), (110, 112)], fill=(150, 158, 175), width=1)
    for wx, wy in [(60, 56), (130, 56), (95, 90), (155, 94)]:
        d.ellipse([wx - 2, wy - 2, wx + 2, wy + 2], fill=(214, 205, 180))
    # desk
    d.rectangle([230, 108, 440, 118], fill=(90, 70, 50), outline=INK, width=1)
    d.rectangle([240, 118, 250, 148], fill=(90, 70, 50))
    d.rectangle([420, 118, 430, 148], fill=(90, 70, 50))
    # nameplate on the desk front, clear of the chair
    d.rectangle([302, 110, 378, 120], fill=CREAM, outline=INK, width=1)
    nf = font(SANS_B, 8)
    d.text((308, 111), "CHIEF EXECUTIVE", font=nf, fill=INK)
    # empty chair (no figure — that is the story): slatted back, thin seat
    d.rectangle([318, 54, 362, 96], outline=INK, width=1)
    d.line([(330, 54), (330, 96)], fill=INK, width=1)
    d.line([(342, 54), (342, 96)], fill=INK, width=1)
    d.line([(354, 54), (354, 96)], fill=INK, width=1)
    d.rectangle([312, 96, 368, 104], fill=(150, 128, 100), outline=INK, width=1)
    d.rectangle([336, 104, 344, 110], fill=(120, 100, 80))
    # crooked picture frame on the wall
    d.rectangle([420, 48, 458, 78], outline=(214, 205, 180), width=2)
    d.line([(420, 48), (458, 56)], fill=(214, 205, 180), width=2)
    # red down arrow + label
    d.polygon([(60, 128), (72, 128), (72, 138), (84, 138), (66, 152), (48, 138),
               (60, 138)], fill=RED)
    af = font(SANS_B, 10)
    d.text((92, 134), "THE CHAIR STAYS EMPTY", font=af, fill=CREAM)
    # --- right: Huang back at the desk, adult figure, chart up
    # desk
    d.rectangle([560, 118, 830, 128], fill=(90, 70, 50), outline=INK, width=1)
    d.rectangle([570, 128, 580, 154], fill=(90, 70, 50))
    d.rectangle([810, 128, 820, 154], fill=(90, 70, 50))
    # adult figure behind the desk, larger: head ~1/7 of height
    adult_figure(d, 640, 14, 118, NAVY, (255, 255, 255), RED)
    # left arm hanging at the side
    d.line([(622, 42), (618, 80)], fill=NAVY, width=8)
    d.ellipse([614, 78, 624, 88], fill=(232, 190, 150), outline=INK, width=1)
    # raised right arm (apology / greeting): upper arm + forearm + open hand
    d.line([(672, 48), (700, 36)], fill=NAVY, width=10)
    d.line([(700, 36), (706, 24)], fill=(232, 190, 150), width=7)
    d.ellipse([700, 16, 712, 28], fill=(232, 190, 150), outline=INK, width=1)
    # laptop on desk
    d.rectangle([740, 104, 790, 118], fill=SLATE, outline=INK, width=1)
    d.rectangle([744, 92, 786, 104], fill=(180, 200, 220), outline=INK, width=1)
    # chart arrow up, right side
    d.line([(860, 140), (890, 110), (908, 122), (946, 86)], fill=INK, width=3)
    d.polygon([(946, 86), (930, 88), (942, 100)], fill=INK)
    cf = font(SANS_B, 13)
    d.text((856, 56), "+31.5% MON", font=cf, fill=RED)
    sf = font(SANS, 10)
    d.text((856, 74), "\u22125.9% Tue", font=sf, fill=INK)
    # --- seam stamp
    cx, cy, r = 488, 79, 28
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PAPER, outline=RED, width=3)
    d.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5],
              outline=RED, width=1)
    stf = font(SANS_B, 9)
    for i, line in enumerate(("BACK IN", "11 DAYS")):
        d.text((cx - d.textlength(line, font=stf) / 2, cy - 10 + i * 11),
               line, font=stf, fill=RED)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=2)
    save(img, "illo_hero.png")


def _base_illo():
    img = Image.new("RGBA", (158, 36), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def illo_markets():
    img, d = _base_illo()
    bars = [(20, 26), (52, 18), (84, 10)]
    for x, top in bars:
        d.rectangle([x, top, x + 22, 34], fill=RED, outline=INK, width=1)
    d.line([(14, 8), (60, 20), (100, 26), (140, 32)], fill=INK, width=2)
    d.polygon([(140, 32), (128, 30), (136, 22)], fill=INK)
    save(img, "illo_s0.png")


def illo_tariffs():
    img, d = _base_illo()
    d.rectangle([18, 20, 140, 32], fill=NAVY, outline=INK, width=1)  # hull
    for x, c in [(26, RED), (56, OCHRE), (86, SLATE), (112, (120, 140, 120))]:
        d.rectangle([x, 8, x + 22, 20], fill=c, outline=INK, width=1)
    d.line([(140, 20), (150, 8)], fill=INK, width=2)
    save(img, "illo_s1.png")


def illo_space():
    img, d = _base_illo()
    # rocket: body + nose + fins + flame
    d.polygon([(76, 2), (84, 12), (84, 26), (76, 26), (68, 12)], fill=CREAM,
              outline=INK, width=1)
    d.polygon([(68, 22), (60, 30), (68, 28)], fill=RED)
    d.polygon([(84, 22), (92, 30), (84, 28)], fill=RED)
    d.polygon([(72, 26), (80, 26), (76, 35)], fill=(230, 120, 40))
    for sx, sy in [(30, 6), (120, 10), (140, 24), (20, 24)]:
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=INK)
    d.ellipse([118, 4, 126, 12], outline=INK, width=1)  # small moon
    save(img, "illo_s2.png")


def illo_mine():
    img, d = _base_illo()
    d.rectangle([20, 4, 138, 34], fill=(60, 52, 44), outline=INK, width=1)
    d.pieslice([52, 8, 106, 34], 180, 360, fill=(20, 16, 12))
    d.rectangle([52, 21, 106, 34], fill=(20, 16, 12))
    # helmet
    d.pieslice([66, 14, 92, 28], 180, 360, fill=OCHRE, outline=INK, width=1)
    d.rectangle([64, 26, 94, 29], fill=OCHRE, outline=INK, width=1)
    # water line
    d.line([(20, 30), (138, 30)], fill=(90, 140, 180), width=2)
    save(img, "illo_s3.png")


def illo_cop():
    img, d = _base_illo()
    d.ellipse([58, 2, 100, 34], outline=INK, width=2, fill=(150, 180, 150))
    d.line([(58, 18), (74, 14), (82, 22), (100, 16)], fill=INK, width=1)
    d.line([(76, 4), (70, 14), (80, 20), (76, 32)], fill=RED, width=2)
    d.text((104, 12), "NO DEAL", font=font(SANS_B, 10), fill=RED)
    save(img, "illo_s4.png")


def illo_refinery():
    img, d = _base_illo()
    for x in (30, 62, 94):
        d.rectangle([x, 12, x + 16, 34], fill=SLATE, outline=INK, width=1)
        d.rectangle([x + 4, 4, x + 12, 12], fill=SLATE, outline=INK, width=1)
    d.polygon([(118, 34), (124, 18), (130, 34)], fill=(230, 120, 40),
              outline=INK, width=1)
    d.ellipse([112, 8, 136, 20], outline=MUTED, width=1)
    save(img, "illo_s5.png")


def illo_cartagena():
    img, d = _base_illo()
    d.rectangle([30, 8, 128, 34], fill=CREAM, outline=INK, width=1)
    for i, c in enumerate((RED, CREAM, RED, CREAM, RED)):
        d.polygon([(30 + i * 19, 8), (30 + (i + 1) * 19, 8),
                   (30 + (i + 1) * 19 + 4, 16), (30 + i * 19 + 4, 16)], fill=c,
                  outline=INK, width=1)
    d.rectangle([66, 18, 92, 34], fill=NAVY, outline=INK, width=1)
    d.line([(20, 28), (140, 28)], fill=RED, width=2)
    save(img, "illo_s6.png")


def illo_crown():
    img, d = _base_illo()
    # adult woman in long dress + crown (flat 2D, adult proportions)
    d.polygon([(76, 4), (70, 12), (76, 9), (82, 12), (88, 4), (88, 12),
               (76, 16)], fill=OCHRE, outline=INK, width=1)
    d.ellipse([73, 14, 83, 24], fill=(232, 190, 150), outline=INK, width=1)
    d.polygon([(68, 26), (84, 26), (92, 35), (62, 35)], fill=(120, 40, 60),
              outline=INK, width=1)
    d.polygon([(76, 24), (70, 34), (82, 34)], fill=(232, 190, 150))
    save(img, "illo_s7.png")


def illo_cricket():
    img, d = _base_illo()
    d.line([(40, 30), (80, 6)], fill=(150, 110, 60), width=6)
    d.rectangle([76, 2, 92, 10], fill=(150, 110, 60), outline=INK, width=1)
    d.ellipse([104, 8, 114, 18], fill=RED, outline=INK, width=1)
    for x in (124, 131, 138):
        d.line([(x, 20), (x, 34)], fill=INK, width=2)
    d.line([(122, 20), (140, 20)], fill=INK, width=2)
    d.text((14, 20), "204", font=font(SANS_B, 10), fill=INK)
    save(img, "illo_s8.png")


def illo_dow():
    img, d = _base_illo()
    d.text((52, 0), "50,000", font=font(SANS_B, 9), fill=INK)
    d.rectangle([30, 12, 128, 18], fill=NAVY, outline=INK, width=1)
    for x in (36, 58, 80, 102):
        d.rectangle([x, 18, x + 8, 28], fill=NAVY, outline=INK, width=1)
    d.rectangle([30, 28, 128, 33], fill=INK)
    save(img, "illo_s9.png")


def illo_odesa():
    img, d = _base_illo()
    for x, h in [(24, 18), (48, 26), (74, 14), (100, 22)]:
        d.rectangle([x, 34 - h, x + 18, 34], fill=SLATE, outline=INK, width=1)
    d.ellipse([122, 4, 146, 12], fill=INK)  # drone body
    for cx in (122, 146):
        d.ellipse([cx - 4, 2, cx + 4, 10], outline=INK, width=1)
    d.line([(134, 12), (134, 20)], fill=INK, width=1)
    save(img, "illo_s10.png")


def illo_ms():
    img, d = _base_illo()
    d.ellipse([40, 10, 70, 30], fill=(200, 210, 225), outline=INK, width=1)
    d.ellipse([62, 6, 96, 30], fill=(200, 210, 225), outline=INK, width=1)
    d.ellipse([88, 12, 118, 30], fill=(200, 210, 225), outline=INK, width=1)
    d.rectangle([40, 22, 118, 30], fill=(200, 210, 225))
    d.line([(40, 30), (118, 30)], fill=INK, width=1)
    d.line([(128, 8), (142, 26)], fill=RED, width=3)
    d.line([(142, 8), (128, 26)], fill=RED, width=3)
    save(img, "illo_s11.png")


# ---------------------------------------------------------------- world map
CONTINENTS = {
    "na": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
           (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
           (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    "sa": [(-80, 10), (-60, 10), (-35, -8), (-40, -20), (-50, -30), (-65, -40),
           (-70, -52), (-73, -35), (-80, -15)],
    "eu": [(-10, 36), (0, 44), (-2, 48), (5, 58), (10, 60), (20, 70), (30, 70),
           (40, 60), (30, 45), (20, 40), (10, 38), (0, 36)],
    "af": [(-17, 15), (-10, 30), (10, 37), (30, 32), (35, 28), (43, 12),
           (51, 11), (40, -5), (35, -20), (20, -35), (12, -18), (9, 0), (-8, 5)],
    "as": [(40, 70), (60, 72), (90, 75), (120, 73), (150, 70), (170, 66),
           (162, 60), (140, 40), (130, 35), (120, 25), (105, 10), (100, 8),
           (90, 20), (80, 8), (70, 20), (60, 25), (50, 30), (43, 38), (40, 45)],
    "oc": [(113, -22), (130, -12), (142, -11), (150, -22), (153, -32),
           (140, -38), (129, -32), (115, -35)],
}
DOTS = [  # (lon, lat, label or None)
    (-74, 41, "NEW YORK"), (-75, 10, "CARTAGENA"), (0, 51, "LONDON"),
    (30, 50, "KYIV"), (35, 31, None), (107, -6, "BOGOR"), (127, 37, None),
    (139, 36, "TOKYO"), (100, 41, None), (167, -41, None), (160, -9, None),
]


def worldmap():
    W, H = 330, 128
    img = tile(W, H)
    d = ImageDraw.Draw(img)
    hf = font(SANS_B, 10)
    d.text((0, 0), "WORLD MAP \u2014 WHERE THE NEWS HAPPENED", font=hf, fill=INK)

    def px(lon, lat):
        return (4 + (lon + 180) / 360.0 * (W - 8),
                14 + (75 - lat) / 130.0 * (H - 18))

    for poly in CONTINENTS.values():
        d.polygon([px(lon, lat) for lon, lat in poly], fill=(196, 188, 164),
                  outline=INK, width=1)
    lf = font(SANS, 7)
    offsets = {"LONDON": (-32, -12), "KYIV": (4, 5)}
    for lon, lat, label in DOTS:
        x, y = px(lon, lat)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=RED, outline=INK, width=1)
        if label:
            dx, dy = offsets.get(label, (4, -4))
            d.text((x + dx, y + dy), label, font=lf, fill=INK)
    save(img, "t_map.png")


def grain():
    rng = random.Random(42)
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    px = img.load()
    for y in range(256):
        for x in range(256):
            v = rng.randint(0, 255)
            px[x, y] = (0, 0, 0, 10 if v > 200 else 0)
    save(img, "grain_256.png")


def main():
    os.makedirs(ASSETS, exist_ok=True)
    topband()
    masthead()
    ticker()
    stats()
    regions()
    feature()
    small_stories()
    crypto()
    briefs()
    datecheck()
    timeline()
    footband()
    hero()
    illo_markets()
    illo_tariffs()
    illo_space()
    illo_mine()
    illo_cop()
    illo_refinery()
    illo_cartagena()
    illo_crown()
    illo_cricket()
    illo_dow()
    illo_odesa()
    illo_ms()
    worldmap()
    grain()
    print("all assets rendered")


if __name__ == "__main__":
    main()
