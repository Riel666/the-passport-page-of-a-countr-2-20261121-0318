#!/usr/bin/env python3
"""Build the invented passport spread for the Republic of Halvoria.

Draws a 1024x1024 PNG of an open passport spread with Pillow only:
a data page (portrait, personal data, machine-readable strip) and a
visas page (arrival/departure stamps from neighbouring fictional
countries plus a visa with a fee stamp). No downloaded assets, no
network; every shape and letter is drawn here.

Fictional consistency (checked by hand while writing this file):
  - Holder: Mira Solen Vask, born 12 APR 1996 in Port Alver, Halvoria.
  - Passport issued 14 MAR 2024 in Port Alver, expires 13 MAR 2034.
  - Every stamp is dated after 14 MAR 2024 and none contradicts the
    place of issue: departures from Halvoria, arrivals in Tarnwick,
    Ostara and Kessan, returns to Halvoria.
  - MRZ check digits follow ICAO 9303 (weights 7, 3, 1).
"""

import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")
MONO_BOLD = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")

W, H = 1024, 1024

# Palette: one coherent document, printed in dark navy on cream paper,
# stamps in three ink colours only.
INK = (28, 38, 66)
INK_SOFT = (74, 84, 110)
PAPER = (247, 242, 228)
PAPER_EDGE = (226, 219, 198)
DESK = (196, 192, 180)
GOLD = (150, 112, 52)
STAMP_BLUE = (38, 74, 148)
STAMP_PURPLE = (104, 58, 138)
STAMP_RED = (168, 44, 40)
STAMP_GREEN = (38, 110, 74)
SKIN = (222, 178, 138)
SKIN_SHADOW = (198, 150, 112)
HAIR = (62, 42, 30)
JACKET = (42, 96, 110)
PHOTO_BG = (178, 196, 208)


def font(path, size):
    return ImageFont.truetype(path, size)


def text(draw, xy, s, f, fill=INK, anchor="la"):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)


def mrz_check(s):
    """ICAO 9303 check digit for a string of A-Z, 0-9 and '<'."""
    values = {}
    for i in range(10):
        values[str(i)] = i
    for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        values[ch] = 10 + i
    values["<"] = 0
    total = 0
    for i, ch in enumerate(s):
        total += values[ch] * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    surname = "VASK"
    given = "MIRA<SOLEN"
    name_field = (surname + "<<" + given).ljust(39, "<")
    line1 = "P<HLV" + name_field
    assert len(line1) == 44
    doc_no = "HV4829137"
    dob = "960412"
    expiry = "340313"
    personal = "HLVMIRA000000<"[:14]
    line2 = (
        doc_no
        + mrz_check(doc_no)
        + "HLV"
        + dob
        + mrz_check(dob)
        + "F"
        + expiry
        + mrz_check(expiry)
        + personal
        + mrz_check(personal)
    )
    line2 += mrz_check(line2)
    assert len(line2) == 44
    return line1, line2


def guilloche(draw, box, colour, step=14):
    """Faint wavy security lines across a page, like a printed ground."""
    x0, y0, x1, y1 = box
    for y in range(y0 + 8, y1 - 8, step):
        pts = []
        for x in range(x0, x1 + 1, 8):
            pts.append((x, y + 3 * math.sin((x - x0) / 46.0 + y / 30.0)))
        draw.line(pts, fill=colour, width=1)


def coat_of_arms(draw, cx, cy, scale=1.0):
    """Halvoria's arms: a shield with a wave and a four-point star."""
    w, h = int(58 * scale), int(66 * scale)
    x0, y0 = cx - w // 2, cy - h // 2
    shield = [
        (x0, y0),
        (x0 + w, y0),
        (x0 + w, y0 + int(h * 0.62)),
        (cx, y0 + h),
        (x0, y0 + int(h * 0.62)),
    ]
    draw.polygon(shield, outline=GOLD, width=3)
    # wave band
    wave = []
    for x in range(x0 + 4, x0 + w - 3, 4):
        wave.append((x, y0 + int(h * 0.52) + int(5 * math.sin((x - x0) / 9.0))))
    draw.line(wave, fill=GOLD, width=3)
    # four-point star
    sx, sy = cx, y0 + int(h * 0.30)
    r = int(11 * scale)
    star = [
        (sx, sy - r),
        (sx + 3, sy - 3),
        (sx + r, sy),
        (sx + 3, sy + 3),
        (sx, sy + r),
        (sx - 3, sy + 3),
        (sx - r, sy),
        (sx - 3, sy - 3),
    ]
    draw.polygon(star, fill=GOLD)


def draw_portrait(draw, box):
    """Flat stylised portrait of Mira Solen Vask, drawn, not pasted."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PHOTO_BG)
    cx = (x0 + x1) // 2
    # shoulders / jacket
    draw.polygon(
        [
            (x0 + 8, y1),
            (x0 + 18, y0 + 138),
            (cx - 34, y0 + 122),
            (cx + 34, y0 + 122),
            (x1 - 18, y0 + 138),
            (x1 - 8, y1),
        ],
        fill=JACKET,
    )
    # shirt V
    draw.polygon(
        [(cx - 16, y0 + 122), (cx + 16, y0 + 122), (cx, y0 + 158)],
        fill=(240, 238, 230),
    )
    # neck
    draw.rectangle([cx - 13, y0 + 96, cx + 13, y0 + 128], fill=SKIN_SHADOW)
    # face
    draw.ellipse([cx - 34, y0 + 26, cx + 34, y0 + 102], fill=SKIN)
    # hair: bob framing the face
    draw.pieslice([cx - 40, y0 + 8, cx + 40, y0 + 92], 180, 360, fill=HAIR)
    draw.rectangle([cx - 40, y0 + 40, cx - 30, y0 + 108], fill=HAIR)
    draw.rectangle([cx + 30, y0 + 40, cx + 40, y0 + 108], fill=HAIR)
    draw.ellipse([cx - 34, y0 + 22, cx + 34, y0 + 62], fill=HAIR)
    draw.ellipse([cx - 30, y0 + 34, cx + 30, y0 + 66], fill=SKIN)
    # brows, eyes, nose, mouth
    draw.line([(cx - 20, y0 + 58), (cx - 8, y0 + 56)], fill=HAIR, width=2)
    draw.line([(cx + 8, y0 + 56), (cx + 20, y0 + 58)], fill=HAIR, width=2)
    draw.ellipse([cx - 19, y0 + 62, cx - 11, y0 + 68], fill=(40, 32, 26))
    draw.ellipse([cx + 11, y0 + 62, cx + 19, y0 + 68], fill=(40, 32, 26))
    draw.line([(cx, y0 + 68), (cx - 2, y0 + 80)], fill=SKIN_SHADOW, width=2)
    draw.arc([cx - 9, y0 + 82, cx + 9, y0 + 94], 20, 160, fill=(150, 80, 70), width=2)
    # photo frame
    draw.rectangle(box, outline=INK, width=2)


def field(draw, x, y, label, value, value_size=16, label_size=10):
    text(draw, (x, y), label, font(SANS, label_size), fill=INK_SOFT)
    text(draw, (x, y + 13), value, font(SANS_BOLD, value_size), fill=INK)


def stamp(draw, cx, cy, angle, colour, lines, size=(190, 96), circle=False):
    """A rotated entry/exit stamp: a rounded rectangle, or a circle
    with a date across it, drawn on its own layer so the ink is
    translucent like a real rubber stamp."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w, h = size
    x0, y0 = cx - w // 2, cy - h // 2
    if circle:
        d.ellipse([x0, y0, x0 + w, y0 + h], outline=colour + (210,), width=3)
        d.ellipse([x0 + 10, y0 + 10, x0 + w - 10, y0 + h - 10],
                  outline=colour + (210,), width=2)
        for i, ln in enumerate(lines):
            d.text((cx, y0 + 24 + i * 20), ln,
                   font=font(SANS_BOLD, 15), fill=colour + (225,),
                   anchor="ma")
    else:
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=8,
                            outline=colour + (220,), width=3)
        d.line([(x0 + 8, y0 + h // 2), (x0 + w - 8, y0 + h // 2)],
               fill=colour + (200,), width=2)
        for i, ln in enumerate(lines):
            d.text((cx, y0 + 10 + i * 22), ln,
                   font=font(SANS_BOLD, 15), fill=colour + (225,),
                   anchor="ma")
    layer = layer.rotate(angle, resample=Image.BICUBIC, center=(cx, cy))
    draw._image.alpha_composite(layer)


def build():
    img = Image.new("RGBA", (W, H), DESK + (255,))
    draw = ImageDraw.Draw(img, "RGBA")

    # Booklet shadow and pages.
    draw.rounded_rectangle([14, 108, 1010, 916], radius=6, fill=(120, 116, 104))
    left = (24, 116, 508, 908)
    right = (516, 116, 1000, 908)
    for page in (left, right):
        draw.rectangle(page, fill=PAPER)
    # Centre gutter.
    draw.rectangle([508, 116, 516, 908], fill=(214, 206, 184))
    draw.line([(512, 116), (512, 908)], fill=(190, 182, 160), width=2)
    guilloche(draw, (30, 122, 502, 902), (232, 224, 200))
    guilloche(draw, (522, 122, 994, 902), (232, 224, 200))
    # Page furniture: thin rules and page numbers.
    for page in (left, right):
        draw.rectangle(page, outline=PAPER_EDGE, width=2)
    text(draw, (40, 886), "12", font(SANS, 11), fill=INK_SOFT)
    text(draw, (968, 886), "13", font(SANS, 11), fill=INK_SOFT, anchor="ra")

    # ---------------- Left page: data page ----------------
    coat_of_arms(draw, 266, 168)
    text(draw, (266, 208), "REPUBLIC OF HALVORIA", font(SERIF_BOLD, 25),
         fill=INK, anchor="ma")
    text(draw, (266, 238), "P A S S P O R T", font(SANS, 15),
         fill=INK_SOFT, anchor="ma")
    draw.line([(60, 268), (472, 268)], fill=GOLD, width=2)

    draw_portrait(draw, (44, 292, 194, 482))
    field(draw, 214, 292, "TYPE", "P")
    field(draw, 268, 292, "CODE", "HLV")
    field(draw, 330, 292, "PASSPORT No.", "HV 4829137")
    field(draw, 214, 340, "SURNAME", "VASK")
    field(draw, 214, 388, "GIVEN NAMES", "MIRA SOLEN")
    field(draw, 214, 436, "NATIONALITY", "HALVORIAN")
    draw.line([(44, 500), (488, 500)], fill=PAPER_EDGE, width=2)

    field(draw, 44, 518, "DATE OF BIRTH", "12 APR 1996")
    field(draw, 214, 518, "PLACE OF BIRTH", "PORT ALVER")
    field(draw, 384, 518, "SEX", "F")
    field(draw, 44, 566, "DATE OF ISSUE", "14 MAR 2024")
    field(draw, 214, 566, "DATE OF EXPIRY", "13 MAR 2034")
    field(draw, 384, 566, "HEIGHT", "168 cm")
    field(draw, 44, 614, "AUTHORITY", "PASSPORT OFFICE, PORT ALVER")
    field(draw, 44, 662, "HOLDER'S SIGNATURE", "M. S. Vask")
    draw.line([(44, 700), (300, 700)], fill=INK_SOFT, width=1)
    text(draw, (330, 668), "Languages of this document:\nHalvorian / English",
         font(SANS, 12), fill=INK_SOFT)
    draw.line([(44, 726), (488, 726)], fill=INK, width=2)
    line1, line2 = mrz_lines()
    text(draw, (266, 744), line1, font(MONO, 15), fill=INK, anchor="ma")
    text(draw, (266, 768), line2, font(MONO, 15), fill=INK, anchor="ma")
    text(draw, (266, 806), "This passport remains the property of the",
         font(SANS, 11), fill=INK_SOFT, anchor="ma")
    text(draw, (266, 822), "Republic of Halvoria.",
         font(SANS, 11), fill=INK_SOFT, anchor="ma")

    # ---------------- Right page: visas and stamps ----------------
    text(draw, (758, 140), "V I S A S", font(SERIF_BOLD, 22),
         fill=INK, anchor="ma")
    draw.line([(552, 172), (964, 172)], fill=GOLD, width=2)

    # Visa sticker.
    draw.rectangle([552, 190, 964, 330], fill=(238, 236, 222),
                   outline=INK, width=2)
    draw.rectangle([560, 198, 956, 322], outline=GOLD, width=1)
    text(draw, (570, 208), "VISITOR VISA — REPUBLIC OF TARNWICK",
         font(SANS_BOLD, 14), fill=INK)
    text(draw, (570, 234), "Valid 90 days — single entry. Issued 28 MAY 2024,",
         font(SANS, 13), fill=INK)
    text(draw, (570, 254), "Port Alver. Holder may not take paid work",
         font(SANS, 13), fill=INK)
    text(draw, (570, 274), "(Condition 7, Tarnwick Immigration Act).",
         font(SANS, 13), fill=INK)
    text(draw, (570, 298), "Fee paid: 40 KR — receipt No. 8814",
         font(SANS_BOLD, 13), fill=STAMP_RED)

    # Stamps, in travel order, every date after the 14 MAR 2024 issue.
    stamp(draw, 660, 400, -6, STAMP_BLUE,
          ["HALVORIA", "DEPARTURE", "02 JUN 2024", "PORT ALVER"])
    stamp(draw, 868, 400, 5, STAMP_PURPLE,
          ["TARNWICK", "ARRIVAL", "03 JUN 2024", "KESSAN BORDER"])
    stamp(draw, 660, 520, 4, STAMP_PURPLE,
          ["TARNWICK", "DEPARTURE", "18 JUN 2024", "KESSAN BORDER"])
    stamp(draw, 868, 520, -5, STAMP_BLUE,
          ["HALVORIA", "ARRIVAL", "07 JUL 2024", "PORT ALVER"])
    stamp(draw, 660, 640, -4, STAMP_GREEN,
          ["OSTARA", "ARRIVAL", "12 SEP 2025", "HAVEN PORT"])
    stamp(draw, 868, 640, 6, STAMP_BLUE,
          ["HALVORIA", "ARRIVAL", "28 OCT 2025", "PORT ALVER"])

    draw.line([(552, 706), (964, 706)], fill=PAPER_EDGE, width=2)
    text(draw, (758, 724), "NOT VALID FOR TRAVEL TO",
         font(SANS_BOLD, 14), fill=STAMP_RED, anchor="ma")
    text(draw, (758, 746), "THE NORTHERN MARCHES",
         font(SANS_BOLD, 14), fill=STAMP_RED, anchor="ma")
    text(draw, (758, 782), "Entries in Halvorian and English. One journey",
         font(SANS, 12), fill=INK_SOFT, anchor="ma")
    text(draw, (758, 800), "per stamp; a stamp out of order is void.",
         font(SANS, 12), fill=INK_SOFT, anchor="ma")
    text(draw, (758, 836), "Holder: Mira Solen Vask — born Port Alver,",
         font(SANS, 12), fill=INK_SOFT, anchor="ma")
    text(draw, (758, 854), "a harbour city of the Halvorian coast.",
         font(SANS, 12), fill=INK_SOFT, anchor="ma")

    return img


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build().convert("RGB")
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    digest = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print(f"wrote {out} {img.size[0]}x{img.size[1]} {size} bytes")
    print(f"sha256 {digest}")
    assert size <= 1_048_576, "entry.png exceeds 1 MiB"
    assert img.size[0] <= 1024 and img.size[1] <= 1024


if __name__ == "__main__":
    main()
