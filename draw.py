#!/usr/bin/env python3
"""THE WORLD TODAY — Sunday 22 November 2026. Draws entry.png (1024x1024).
Layout follows the top-20 pattern: masthead -> kicker -> number strip ->
region bar -> UTC strip -> 3 hero scenes -> 10 small cards -> map + list ->
DATE CHECK -> footer. All scenes drawn with PIL shapes (no photos)."""
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 243, 230)
INK = (17, 17, 17)
RED = (164, 30, 34)
NAVY = (28, 47, 87)
GREEN = (30, 122, 52)
GRAY = (90, 90, 90)
SEA = (207, 224, 234)
LAND = (227, 211, 168)

F = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(F + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)

def chip(x, y, label, bg, fg=(255, 255, 255)):
    fnt = SANS_B(9)
    w = d.textlength(label, font=fnt) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=bg)
    d.text((x + 5, y + 2), label, font=fnt, fill=fg)
    return w

CHIP_COLOR = {
    "CONFIRMED": (30, 122, 52),
    "REPORTED": (28, 47, 87),
    "CLAIM": (184, 134, 11),
    "OFFICIAL": (70, 70, 70),
    "ONGOING": (120, 60, 140),
}

# ---------- frame ----------
d.rectangle([4, 4, 1020, 1020], outline=RED, width=3)

# ---------- masthead ----------
text(14, 12, "THE WORLD TODAY", SERIF_B(46), INK)
text(1010, 16, "SUNDAY 22 NOVEMBER 2026", SANS_B(19), RED, anchor="ra")
text(1010, 42, "36 STORIES  ·  7 REGIONS", SANS_B(11), INK, anchor="ra")
d.line([14, 66, 1010, 66], fill=INK, width=2)

# ---------- kicker ----------
text(14, 70, "The world in one day", SERIF(14), RED)
text(1010, 71, "EVERY ITEM FIRST REPORTED 22 NOV 2026", SANS_B(10), INK, anchor="ra")

# ---------- number strip ----------
d.rectangle([10, 82, 1014, 110], fill=NAVY)
nums = [
    ("186", "drones fired"), ("161", "shot down"), ("720/9", "India declare"),
    ("98,79%", "HK turnout"), ("$120bn", "target dropped"), ("35%", "power goal kept"),
    ("44h", "overtime"), ("258", "House seats"),
]
seg = 1004 / len(nums)
for i, (n, lab) in enumerate(nums):
    cx = 10 + seg * i + seg / 2
    text(cx, 86, n, SANS_B(15), (255, 200, 60), anchor="ma")
    text(cx, 99, lab, SANS(8), (255, 255, 255), anchor="ma")

# ---------- region bar ----------
regions = [
    ("EUROPE 8", 8, (28, 47, 87)), ("MIDDLE EAST 7", 7, (164, 30, 34)),
    ("ASIA-PACIFIC 7", 7, (30, 122, 52)), ("AMERICAS 5", 5, (184, 134, 11)),
    ("AFRICA 3", 3, (120, 60, 140)), ("OCEANIA 3", 3, (0, 120, 120)),
    ("WORLD 3", 3, (70, 70, 70)),
]
x = 10
for label, cnt, col in regions:
    w = 1004 * cnt / 36
    d.rectangle([x, 112, x + w - 1, 130], fill=col)
    text(x + w / 2, 117, label, SANS_B(10), (255, 255, 255), anchor="ma")
    x += w

# ---------- UTC strip ----------
d.rectangle([10, 132, 1014, 152], fill=(233, 226, 205))
text(16, 137, "THE DAY IN UTC", SANS_B(10), RED)
utc = [
    ("01:00", "HK polls open"), ("03:00", "COP31 objections end"),
    ("06:00", "COP31 session"), ("~16:00", "COP31 collapses"),
    ("17:00", "Alcaraz wins"), ("18:13", "Dems reach 258"),
]
ux = 140
for t, lab in utc:
    text(ux, 137, t, SANS_B(10), NAVY)
    ux += d.textlength(t, font=SANS_B(10)) + 4
    text(ux, 137, lab, SANS(10), INK)
    ux += d.textlength(lab, font=SANS(10)) + 12

# ---------- hero scenes ----------
def scene_cop31(x0, y0, w, h):
    for i in range(h):
        r = int(245 - (245 - 190) * i / h)
        g = int(166 - (166 - 60) * i / h)
        b = int(38 + (60 - 38) * i / h)
        d.line([x0, y0 + i, x0 + w, y0 + i], fill=(r, g, b))
    d.ellipse([x0 + w - 78, y0 + 14, x0 + w - 18, y0 + 74], fill=(255, 236, 170))
    cx, cy, r = x0 + w // 2 - 30, y0 + h // 2 + 8, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 139, 87), outline=(20, 60, 30), width=2)
    d.ellipse([cx - 30, cy - 18, cx - 2, cy + 6], fill=(34, 110, 60))
    d.ellipse([cx + 6, cy + 8, cx + 30, cy + 30], fill=(34, 110, 60))
    d.ellipse([cx - 8, cy - 34, cx + 14, cy - 14], fill=(60, 160, 100))
    d.line([(cx - 26, cy - 30), (cx - 8, cy - 8), (cx - 18, cy + 12), (cx + 4, cy + 30)],
           fill=(255, 255, 255), width=3)
    d.line([(cx - 8, cy - 8), (cx + 14, cy - 16), (cx + 28, cy - 2)],
           fill=(255, 255, 255), width=2)
    d.polygon([(x0, y0 + h), (x0, y0 + h - 16), (x0 + 40, y0 + h - 26),
               (x0 + w - 40, y0 + h - 26), (x0 + w, y0 + h - 16), (x0 + w, y0 + h)],
              fill=(40, 20, 20))
    for i in range(9):
        d.rectangle([x0 + 14 + i * 34, y0 + h - 14, x0 + 26 + i * 34, y0 + h - 4],
                    fill=(255, 220, 120))

def scene_drones(x0, y0, w, h):
    for i in range(h):
        b = int(13 + 30 * i / h)
        d.line([x0, y0 + i, x0 + w, y0 + i], fill=(10, 20, b + 20))
    rnd = random.Random(7)
    for _ in range(40):
        sx, sy = x0 + rnd.randint(2, w - 2), y0 + rnd.randint(2, h - 30)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # narrow searchlight beams
    d.polygon([(x0 + 60, y0 + h), (x0 + 96, y0 + 12), (x0 + 104, y0 + 12), (x0 + 78, y0 + h)],
              fill=(170, 185, 215))
    d.polygon([(x0 + w - 70, y0 + h), (x0 + w - 120, y0 + 22), (x0 + w - 112, y0 + 22),
               (x0 + w - 52, y0 + h)], fill=(170, 185, 215))
    # drones
    for dx, dy in [(70, 26), (150, 44), (230, 20), (110, 60), (260, 55)]:
        d.ellipse([x0 + dx - 3, y0 + dy - 3, x0 + dx + 3, y0 + dy + 3], fill=(20, 20, 20))
        d.ellipse([x0 + dx - 9, y0 + dy - 2, x0 + dx - 5, y0 + dy + 2], fill=(255, 60, 60))
        d.ellipse([x0 + dx + 5, y0 + dy - 2, x0 + dx + 9, y0 + dy + 2], fill=(60, 255, 90))
        d.line([x0 + dx - 12, y0 + dy, x0 + dx + 12, y0 + dy], fill=(20, 20, 20), width=2)
    # collapsed block: upright building + tilted slab + rubble + fires
    d.rectangle([x0 + 30, y0 + h - 56, x0 + 130, y0 + h], fill=(110, 110, 116))
    for wy in (y0 + h - 48, y0 + h - 34, y0 + h - 20):
        for wx in (40, 62, 84, 106):
            d.rectangle([x0 + wx, wy, x0 + wx + 10, wy + 8], fill=(255, 220, 120))
    d.polygon([(x0 + 130, y0 + h), (x0 + 150, y0 + h - 34), (x0 + 230, y0 + h - 28),
               (x0 + 280, y0 + h)], fill=(85, 85, 90))
    for fx, fh in [(180, 26), (210, 20), (250, 30)]:
        d.polygon([(x0 + fx, y0 + h), (x0 + fx + 6, y0 + h - fh),
                   (x0 + fx + 12, y0 + h)], fill=(255, 140, 0))
        d.polygon([(x0 + fx + 3, y0 + h), (x0 + fx + 6, y0 + h - fh + 8),
                   (x0 + fx + 9, y0 + h)], fill=(255, 220, 0))

def scene_radar(x0, y0, w, h):
    for i in range(h):
        b = int(15 + 25 * i / h)
        d.line([x0, y0 + i, x0 + w, y0 + i], fill=(12, 18, b + 15))
    rnd = random.Random(11)
    for _ in range(30):
        sx, sy = x0 + rnd.randint(2, w - 2), y0 + rnd.randint(2, h - 40)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # low orange glow along the ground
    d.ellipse([x0 + 60, y0 + h - 46, x0 + w - 60, y0 + h + 10], fill=(110, 45, 8))
    # radar dishes: tilted bowl (arc) + mast + feed arm
    for dx, dy, s, tilt in [(70, 60, 30, -18), (165, 50, 40, 12), (258, 64, 28, -8)]:
        d.line([x0 + dx, y0 + dy + 10, x0 + dx, y0 + h - 8], fill=(200, 200, 200), width=4)
        d.arc([x0 + dx - s, y0 + dy - s, x0 + dx + s, y0 + dy + s],
              start=180 + tilt, end=360 + tilt, fill=(235, 235, 235), width=5)
        d.line([x0 + dx - s, y0 + dy, x0 + dx + s, y0 + dy], fill=(235, 235, 235), width=3)
        d.line([x0 + dx, y0 + dy, x0 + dx + tilt, y0 + dy - 14], fill=(235, 235, 235), width=2)
        d.ellipse([x0 + dx + tilt - 3, y0 + dy - 17, x0 + dx + tilt + 3, y0 + dy - 11],
                  fill=(255, 80, 60))
    # flames at base
    for fx, fh in [(50, 24), (140, 30), (230, 26), (285, 20)]:
        d.polygon([(x0 + fx, y0 + h), (x0 + fx + 7, y0 + h - fh),
                   (x0 + fx + 14, y0 + h)], fill=(255, 140, 0))
        d.polygon([(x0 + fx + 4, y0 + h), (x0 + fx + 7, y0 + h - fh + 9),
                   (x0 + fx + 10, y0 + h)], fill=(255, 220, 0))
    # smoke
    for sx, sy, r in [(90, 26, 10), (200, 18, 12), (270, 30, 9)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r], fill=(60, 60, 65))

heroes = [
    ("CLIMATE · ANTALYA", "NO DEAL", "CONFIRMED",
     "COP31 collapses in Antalya: the text, with no fossil-fuel language, is rejected by the EU and ~130 parties. Longest COP ever.",
     "“The worst COP ever — its collapse must be a wake-up call.”",
     "CNN · Reuters · Power Shift Africa", scene_cop31),
    ("WAR · UKRAINE", "186 DRONES", "REPORTED",
     "Russia fires 186 drones at Ukraine overnight; 161 are shot down or jammed. A five-storey block in Dymer collapses — 1 killed, 14 missing.",
     "161 of 186 down; strikes in 18 places.",
     "Ukrainian Air Force · AP", scene_drones),
    ("WAR · BAHRAIN", "RADARS HIT", "CLAIM",
     "Iran claims its forces hit 2 US Patriot radars in Bahrain; Bahrain denies any military attack. A site in Sitra burns; 2 hurt, none killed.",
     "Claim and denial — the strike itself is unverified.",
     "IRGC · Bahrain MoI", scene_radar),
]
HX = [10, 342, 674]
HW = 322
for (kicker, head, ch, body, quote, src, painter), x0 in zip(heroes, HX):
    painter(x0, 150, HW, 102)
    d.rectangle([x0, 150, x0 + HW, 252], outline=INK, width=1)
    text(x0, 256, kicker, SANS_B(11), RED)
    chip(x0 + HW - 78, 254, ch, CHIP_COLOR[ch])
    text(x0, 274, head, SERIF_B(27), INK)
    yy = 306
    for ln in wrap(body, SANS(11), HW):
        text(x0, yy, ln, SANS(11), INK)
        yy += 15
    for ln in wrap(quote, SERIF(11), HW):
        text(x0, yy, ln, SERIF(11), (80, 60, 20))
        yy += 14
    text(x0, 376, src, SANS(10), GRAY)

# ---------- small cards header ----------
text(10, 392, "THE DAY IN PICTURES — 10 MORE STORIES", SANS_B(12), INK)
text(1010, 392, "ALL TIMES UTC", SANS(10), GRAY, anchor="ra")
d.line([10, 408, 1014, 408], fill=INK, width=1)

# ---------- small card scene strips ----------
def strip_fire(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(30, 20, 25))
    for fx in (20, 70, 120, 165):
        d.polygon([(x0 + fx, y0 + h), (x0 + fx + 7, y0 + h - 16),
                   (x0 + fx + 14, y0 + h)], fill=(255, 140, 0))
        d.polygon([(x0 + fx + 4, y0 + h), (x0 + fx + 7, y0 + h - 9),
                   (x0 + fx + 10, y0 + h)], fill=(255, 220, 0))

def strip_ball(x0, y0, w, h, bg, ball=(255, 255, 255)):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=bg)
    d.ellipse([x0 + w - 34, y0 + 4, x0 + w - 12, y0 + h - 4], fill=ball, outline=INK)
    d.line([x0 + 8, y0 + h - 6, x0 + w - 44, y0 + 6], fill=(255, 255, 255), width=2)

def strip_flag(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(20, 30, 60))
    for r in range(2):
        for c in range(6):
            if (r + c) % 2 == 0:
                d.rectangle([x0 + 8 + c * 12, y0 + 3 + r * 10,
                             x0 + 20 + c * 12, y0 + 13 + r * 10], fill=(255, 255, 255))
    d.rectangle([x0 + 110, y0 + 8, x0 + 170, y0 + h - 6], fill=(200, 30, 30))
    d.ellipse([x0 + 118, y0 + h - 10, x0 + 126, y0 + h - 2], fill=(20, 20, 20))
    d.ellipse([x0 + 154, y0 + h - 10, x0 + 162, y0 + h - 2], fill=(20, 20, 20))

def strip_dome(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(28, 47, 87))
    d.pieslice([x0 + w // 2 - 26, y0 + 2, x0 + w // 2 + 26, y0 + 34],
               start=180, end=360, fill=(255, 255, 255))
    d.rectangle([x0 + w // 2 - 30, y0 + 18, x0 + w // 2 + 30, y0 + h - 2],
                fill=(255, 255, 255))
    for i in range(4):
        d.rectangle([x0 + w // 2 - 24 + i * 13, y0 + 20, x0 + w // 2 - 16 + i * 13,
                     y0 + h - 4], fill=(28, 47, 87))

def strip_city(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(70, 90, 120))
    for bx, bh in [(10, 14), (40, 20), (75, 12), (105, 18), (140, 15)]:
        d.rectangle([x0 + bx, y0 + h - bh, x0 + bx + 24, y0 + h], fill=(40, 50, 70))
        d.rectangle([x0 + bx + 5, y0 + h - bh + 4, x0 + bx + 9, y0 + h - bh + 8],
                    fill=(255, 220, 120))

def strip_court(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(200, 90, 20))
    d.ellipse([x0 + 20, y0 + 5, x0 + 40, y0 + h - 5], fill=(120, 60, 20), outline=(255, 255, 255))
    d.line([x0 + 60, y0 + h - 4, x0 + w - 10, y0 + 4], fill=(255, 255, 255), width=2)

def strip_cross(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(120, 20, 20))
    d.rectangle([x0 + w // 2 - 4, y0 + 3, x0 + w // 2 + 4, y0 + h - 3], fill=(255, 255, 255))
    d.rectangle([x0 + w // 2 - 12, y0 + 7, x0 + w // 2 + 12, y0 + 15], fill=(255, 255, 255))

def strip_pitch(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(30, 122, 52))
    d.line([x0 + 10, y0 + 6, x0 + w - 10, y0 + 6], fill=(255, 255, 255), width=2)
    d.line([x0 + 10, y0 + 6, x0 + 10, y0 + h - 6], fill=(255, 255, 255), width=2)
    d.ellipse([x0 + w - 34, y0 + 6, x0 + w - 14, y0 + h - 6], fill=(255, 255, 255), outline=INK)

small = [
    ("02", "ASIA-PACIFIC · HONG KONG", "Hong Kong votes 98,79%",
     "856 candidates, 723 seats; 5,640 of 5,709 turn out.", "SCMP", "CONFIRMED",
     lambda x, y, w, h: strip_ball(x, y, w, h, (164, 30, 34))),
    ("03", "AMERICAS · LAS VEGAS", "Verstappen wins by 0,639s",
     "Beats Norris in Las Vegas; Piastri third; 75th win.", "AP", "CONFIRMED", strip_flag),
    ("04", "EUROPE · TURIN", "Alcaraz takes ATP Finals",
     "Beats Zverev 6–2, 7–6(7); first Finals title.", "ATP", "CONFIRMED",
     lambda x, y, w, h: strip_ball(x, y, w, h, (30, 122, 52), (220, 255, 120))),
    ("16", "ASIA-PACIFIC · CIKANDE", "Factory fire: 3 dead",
     "36 missing; 15 survive; fire began Saturday night.", "Detiknews", "REPORTED",
     strip_fire),
    ("17", "ASIA-PACIFIC · NEW ZEALAND", "India declare 720/9",
     "Highest Test total in NZ; Rahul 136, Pant 128.", "ESPNcricinfo", "CONFIRMED",
     lambda x, y, w, h: strip_ball(x, y, w, h, (30, 122, 52))),
    ("18", "ASIA-PACIFIC · SEOUL", "Minister quits over AI cheat",
     "Choi Kyo-jin resigns; 111 device cases.", "Yonhap", "CONFIRMED", strip_city),
    ("23", "AMERICAS · WASHINGTON", "Dems take House: 258",
     "Hubbard beats Foxx by 330; 4 races uncalled.", "AP", "CONFIRMED",
     strip_dome),
    ("25", "AMERICAS · SAN ANTONIO", "Wembanyama scores 50",
     "19 rebounds, 5 blocks; Spurs win 114–91.", "NBA", "CONFIRMED", strip_court),
    ("30", "AFRICA · D.R. CONGO", "Ebola cases hit 11,613",
     "WHO count; fighting traps medics.", "WHO", "OFFICIAL", strip_cross),
    ("36", "WORLD · LIVERPOOL", "Liverpool rout United 4–0",
     "Pochettino debut ends in rout at Anfield.", "BBC", "CONFIRMED", strip_pitch),
]
CX = [10, 208, 406, 604, 802]
for i, (num, kicker, title, body, src, ch, painter) in enumerate(small):
    x0 = CX[i % 5]
    y0 = 412 + (i // 5) * 98
    cw = 190
    painter(x0, y0, cw, 24)
    d.rectangle([x0, y0, x0 + cw, y0 + 94], outline=(150, 150, 150), width=1)
    text(x0 + 4, y0 + 27, num, SANS_B(11), RED)
    text(x0 + 26, y0 + 27, kicker, SANS_B(9), RED)
    yy = y0 + 40
    for ln in wrap(title, SANS_B(11), cw - 8):
        text(x0 + 4, yy, ln, SANS_B(11), INK)
        yy += 13
    for ln in wrap(body, SANS(10), cw - 8):
        text(x0 + 4, yy, ln, SANS(10), INK)
        yy += 12
    text(x0 + 4, y0 + 82, src, SANS(9), GRAY)
    chip(x0 + cw - 78, y0 + 80, ch, CHIP_COLOR[ch])

# ---------- map + list header ----------
text(10, 612, "WHERE IT HAPPENED — ALSO ON SUNDAY, 23 MORE STORIES", SANS_B(12), INK)
text(1010, 612, "PIN NUMBERS MATCH STORY NUMBERS", SANS(10), GRAY, anchor="ra")
d.line([10, 628, 1014, 628], fill=INK, width=1)

# ---------- map ----------
MX0, MY0, MW, MH = 10, 632, 320, 236
d.rectangle([MX0, MY0, MX0 + MW, MY0 + MH], fill=SEA, outline=INK, width=1)

def poly(pts, fill=LAND):
    d.polygon([(MX0 + x, MY0 + y) for x, y in pts], fill=fill, outline=(120, 100, 60))

poly([(18, 48), (95, 42), (118, 62), (108, 88), (72, 104), (46, 96), (26, 80)])
poly([(72, 132), (102, 136), (108, 176), (92, 216), (76, 192), (66, 152)])
poly([(98, 18), (122, 16), (128, 32), (102, 36)])
poly([(166, 48), (206, 44), (216, 62), (202, 78), (182, 74), (166, 62)])
poly([(166, 88), (212, 88), (222, 122), (206, 168), (186, 168), (170, 122)])
poly([(216, 38), (312, 34), (316, 74), (292, 98), (262, 94), (236, 78), (216, 58)])
poly([(272, 178), (306, 172), (312, 192), (286, 202), (270, 192)])
poly([(158, 44), (165, 42), (166, 54), (158, 56)])

def pin(x, y, n):
    d.ellipse([MX0 + x - 6, MY0 + y - 6, MX0 + x + 6, MY0 + y + 6],
              fill=RED, outline=(255, 255, 255), width=1)
    text(MX0 + x, MY0 + y - 5, str(n), SANS_B(8), (255, 255, 255), anchor="ma")

def leader_pin(tx, ty, cx, cy, n):
    # dot at true spot, numbered circle offset, thin leader line
    d.ellipse([MX0 + tx - 2, MY0 + ty - 2, MX0 + tx + 2, MY0 + ty + 2], fill=RED)
    d.line([MX0 + tx, MY0 + ty, MX0 + cx, MY0 + cy], fill=RED, width=1)
    pin(cx, cy, n)

pins = {
    2: (298, 94), 3: (38, 78), 9: (228, 82), 11: (206, 112),
    16: (278, 130), 17: (308, 212), 18: (300, 70), 19: (264, 86), 20: (280, 98),
    21: (292, 142), 22: (298, 198), 23: (84, 72), 24: (86, 166), 25: (54, 92),
    26: (80, 92), 27: (36, 44), 28: (206, 136), 29: (186, 136), 30: (196, 156),
    31: (282, 210), 32: (310, 192), 33: (296, 184), 35: (26, 60),
}
for n, (px, py) in pins.items():
    pin(px, py, n)
# Europe cluster via leader lines (true spots too close together)
leader_pin(160, 46, 146, 36, 36)   # Liverpool
leader_pin(170, 58, 150, 60, 7)    # Brussels
leader_pin(184, 48, 176, 30, 6)    # Copenhagen
leader_pin(182, 68, 166, 80, 4)    # Turin
leader_pin(202, 44, 210, 28, 5)    # Estonia
leader_pin(196, 36, 198, 20, 8)    # Finland
leader_pin(206, 60, 218, 52, 1)    # Kyiv
# Middle East cluster via leader lines (true spots close together)
leader_pin(240, 100, 232, 116, 13)   # Gaza
leader_pin(244, 96, 252, 88, 14)     # Israel
leader_pin(242, 99, 236, 84, 15)     # Ramallah
leader_pin(256, 104, 264, 118, 10)   # Bahrain
leader_pin(264, 92, 272, 78, 12)     # Tehran
text(MX0 + 8, MY0 + MH - 14, "34 Bitcoin (global) — no pin", SANS(8), GRAY)

# ---------- ALSO list ----------
alist = [
    ("05", "Estonia closes 5 crossings", "Russia border shut from 1 Dec after sabotage bid.", "Reuters"),
    ("06", "Denmark expels Russian attaché", "Alleged plot to kill US-Ukrainian rapper.", "DR"),
    ("07", "Belgium strike grounds flights", "Controllers join national strike; Monday flights axed.", "Belga"),
    ("08", "Sparta II still burning", "Hit Saturday; 16 crew safe; Finland blames Kyiv.", "Yle"),
    ("11", "Merkury capsizes off Benghazi", "Sea drone hits corvette; several killed.", "France 24"),
    ("12", "Iran rations power", "Blackouts ~2 hours a day as gas output falls.", "IRNA"),
    ("13", "Gaza: 4 killed by Israeli fire", "3 die in drone hit on food-aid van; WCK: not ours.", "Al Jazeera"),
    ("14", "Eisenkot invites Likud to talks", "48-seat bloc, 13 short of a majority.", "Haaretz"),
    ("15", "Settlers burn 12 cars", "Ramallah torched; homes attacked in Hebron.", "Guardian"),
    ("19", "Nepal PM lands in Delhi", "First foreign trip; meets Modi Monday.", "ANI"),
    ("20", "Manipur liquor toll rises", "16–19 dead; ~600 treated; 6 held.", "PTI"),
    ("21", "EU–Indonesia deal signed", "Date split Sat/Sun — see DATE CHECK.", "EU"),
    ("22", "Marles rejects AUKUS report", "Calls US budget-office sub claim “wrong”.", "ABC"),
    ("24", "Bolsonaro in intensive care", "Acute bowel obstruction; stable at 71.", "Globo"),
    ("26", "Falcon 9 launches NROL-136", "Pad record 32 hours; booster lands.", "SpaceX"),
    ("27", "FBI probes NCIC hack", "Washington delays dealer gun checks.", "FBI"),
    ("28", "Khartoum drones kill 4", "UN site hit in strikes.", "AP"),
    ("29", "Nigeria boat capsizes", "24 mourners drown in Bayelsa.", "Reuters"),
    ("31", "Melbourne: 70 years on", "1956 Olympics opened this day in 1956.", "ABC"),
    ("32", "Fred Nile dies at 92", "Died 21 Nov, announced 22 Nov.", "Guardian"),
    ("33", "Cummins stays Test captain", "Australia confirms skipper.", "CA"),
    ("34", "Bitcoin tops $60,000", "R16: $60,020, up 1.85%.", "CoinDesk"),
    ("35", "Nvidia faces SEC probe", "Shares down ~14% on Friday.", "Bloomberg"),
]
LX = [340, 680]
for i, (num, head, body, src) in enumerate(alist):
    x0 = LX[i // 12]
    y0 = 636 + (i % 12) * 19
    text(x0, y0, num, SANS_B(11), RED)
    text(x0 + 24, y0, head, SANS_B(11), INK)
    text(x0 + 24, y0 + 10, body, SANS(10), (60, 60, 60))
    text(x0 + 330, y0 + 10, src, SANS(9), GRAY, anchor="ra")

# ---------- DATE CHECK ----------
d.rectangle([10, 872, 1014, 972], outline=RED, width=2, fill=(255, 244, 240))
text(16, 877, "DATE CHECK — EVERY STORY FIRST REPORTED 22 NOV 2026", SANS_B(12), RED)
text(16, 894, "Wires read up to 23:00 UTC Sunday. Every story on this page happened, or was first",
     SANS(10), INK)
text(16, 906, "reported, on Sunday 22 November 2026.", SANS(10), INK)
text(360, 894, "LEFT OUT — NOT 22 NOV:", SANS_B(10), RED)
leftout = ("400-drone barrage 19–20 Nov · El Chapo Isidro 20 Nov · BepiColombo 21 Nov "
           "(burn 18:24 GMT) · Kryvyi Rih 20 Nov · Peru quake 20 Nov · Hormuz tanker hit "
           "Sat 21 Nov 05:00 GMT")
yy = 906
for ln in wrap(leftout, SANS(10), 330):
    text(360, yy, ln, SANS(10), INK)
    yy += 12
yy += 2
text(360, yy, "DATE SPLIT — shown as reported Sun: EU–Indonesia deal · FBI NCIC hack ·",
     SANS(9), (120, 60, 0))
yy += 12
text(360, yy, "Nigeria boat (most wires: Fri 20) · Sparta II (hit Sat 21, still burning Sun).",
     SANS(9), (120, 60, 0))
text(720, 894, "NOT YET:", SANS_B(10), RED)
notyet = ("4 House races uncalled · COP32 venue not set · Gaza ceasefire talks: no deal "
          "announced · Dymer final toll")
yy = 906
for ln in wrap(notyet, SANS(10), 288):
    text(720, yy, ln, SANS(10), INK)
    yy += 12

# ---------- footer ----------
text(10, 978, "SOURCES: AP · Reuters · BBC · CNN · France 24 · Al Jazeera · Guardian · SCMP · Yonhap · WHO · ATP · NBA · IRNA · Detiknews · FBI",
     SANS(9), GRAY)
text(10, 992, "CONFIRMED = 2+ outlets · REPORTED = wires that day · CLAIM = one side alleges, unverified · OFFICIAL = recorded result · FORECAST = not yet decided",
     SANS(9), GRAY)
text(10, 1004, "Scenes are drawn illustrations, not photographs.", SERIF(10), GRAY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
import os
print("bytes:", os.path.getsize("entry.png"))
