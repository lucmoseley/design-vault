#!/usr/bin/env python3
"""USAGE
  python3 scripts/de00-look-test.py OUT_DIR
Writes OUT_DIR/items.json and OUT_DIR/img/*.png for plugin/review-page, and
prints the measured pairs, each ΔE00 measured from the rounded hex, and the key
from card id to ΔE00, which the page withholds. Exits 1 if a pair lands more than TOLERANCE
from its target. The small cards' words need DejaVu Sans Bold at FONT.
"""

import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "plugin",
        "skills",
        "design-project",
        "scripts",
    ),
)
from colour_space import D65_WHITE, de2000, lab

# guess, #178
TARGETS = (4, 7, 10, 13, 16)
# guess, #178
TOLERANCE = 0.15
# #178
SHOWN = {"large": (13, 4, 16, 7, 10), "small": (7, 16, 10, 4, 13)}
# guess, #178
BASES = (("dark", "#404040", 1), ("pale", "#D9D9D9", -1))
GROUND = (255, 255, 255)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def unlin(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


# sRGB's XYZ-to-RGB matrix under D65: http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
M_INV = (
    (3.2404542, -1.5371385, -0.4985314),
    (-0.9692660, 1.8760108, 0.0415560),
    (0.0556434, -0.2040259, 1.0572252),
)


def hex_to_rgb(h):
    return tuple(int(h[i : i + 2], 16) for i in (1, 3, 5))


def lab_to_hex(l_star, a, b):
    def finv(t):
        return t**3 if t > 6 / 29 else 3 * (6 / 29) ** 2 * (t - 4 / 29)

    fy = (l_star + 16) / 116
    xyz = (
        D65_WHITE[0] * finv(fy + a / 500),
        D65_WHITE[1] * finv(fy),
        D65_WHITE[2] * finv(fy - b / 200),
    )
    rgb = [unlin(sum(m * c for m, c in zip(row, xyz, strict=True))) for row in M_INV]
    if any(c < -0.5 / 255 or c > 1 + 0.5 / 255 for c in rgb):
        return None
    return "#" + "".join(f"{round(min(max(c, 0), 1) * 255):02X}" for c in rgb)


def moved(base, sign, t):
    lightness, a, b = lab(base)
    return (lightness + sign * t, a, b)


def pair_at(base, sign, target):
    # guess, #501
    lo, hi = (
        0.0,
        60.0,
    )

    # guess, #501
    for _ in range(60):
        mid = (lo + hi) / 2
        h = lab_to_hex(*moved(base, sign, mid))
        if h is None or de2000(lab(base), lab(h)) > target:
            hi = mid
        else:
            lo = mid
    found = [
        (h, de2000(lab(base), lab(h)))
        for h in (lab_to_hex(*moved(base, sign, t)) for t in (lo, hi))
        if h
    ]
    return min(found, key=lambda f: abs(f[1] - target))


S = 4


def draw_large(rows):
    # guess, #501
    w, h, gap = 1200, 900, 24
    img = Image.new("RGB", (w * S, h * S), GROUND)
    pen = ImageDraw.Draw(img)
    fw, fh = (w - 3 * gap) // 2, (h - (len(rows) + 1) * gap) // len(rows)
    for r, (a, b) in enumerate(rows):
        y = gap + r * (fh + gap)
        for c, col in enumerate((a, b)):
            x = gap + c * (fw + gap)
            pen.rectangle([x * S, y * S, (x + fw) * S - 1, (y + fh) * S - 1], fill=col)
    return img.resize((w, h), Image.BOX)


def draw_small(rows):
    w, h = 288, 216
    img = Image.new("RGB", (w * S, h * S), GROUND)
    pen = ImageDraw.Draw(img)
    # guess, #501
    font = ImageFont.truetype(FONT, 13 * S)
    for r, (a, b) in enumerate(rows):
        cy = h * (2 * r + 1) // (2 * len(rows))
        for c, col in enumerate((a, b)):
            x = 28 + c * 18
            pen.ellipse([x * S, (cy - 6) * S, (x + 12) * S, (cy + 6) * S], fill=col)
            x = 88 + c * 42
            pen.rectangle(
                [x * S, (cy - 1.5) * S, (x + 36) * S, (cy + 1.5) * S], fill=col
            )
            pen.text(
                ((186 + c * 44) * S, cy * S), "Bed", font=font, fill=col, anchor="lm"
            )
    return img.resize((w, h), Image.BOX)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = sys.argv[1]
    os.makedirs(os.path.join(out, "img"), exist_ok=True)
    levels, failed = [], False
    for target in TARGETS:
        rows = []
        for name, base, sign in BASES:
            h, d = pair_at(base, sign, target)
            failed |= abs(d - target) > TOLERANCE
            rows.append((name, base, h, d))
            print(f"ΔE00 {target:>2}  {name:<5} {base} → {h}  measured {d:.2f}")
        levels.append((target, rows))
    if failed:
        print(f"a pair landed more than {TOLERANCE} from its target", file=sys.stderr)
        sys.exit(1)

    items = []
    by_target = dict(levels)
    draw = {"large": draw_large, "small": draw_small}
    for size, order in SHOWN.items():
        for letter, target in zip("ABCDE", order, strict=True):
            iid = f"{size}-{letter.lower()}"
            rows = by_target[target]
            draw[size]([(hex_to_rgb(b), hex_to_rgb(h)) for _, b, h, _ in rows]).save(
                os.path.join(out, "img", f"{iid}.png")
            )
            items.append(
                {
                    "id": iid,
                    "name": f"{size.capitalize()} {letter}",
                    "image": f"img/{iid}.png",
                    "line": "Top: the logo grey and a lighter grey. Bottom: a pale grey and a darker one.",
                }
            )
            print(f"key: {iid} is ΔE00 {target}")
    data = {
        "title": "When do two greys look like a mistake?",
        "intro": (
            "Each card shows two pairs of greys. On top, the mmm-infra logo grey beside a lighter grey; below, a pale "
            "grey, of the kind a border or panel uses, beside a darker one. On one card both pairs are the same "
            "measured distance apart; the cards differ in how far, and are shuffled.\n\n"
            "Research has settled when other colours stop looking like a mistake, but for two greys its sources "
            "disagree, and every near-miss found in mmm-infra's designs so far is a pair of greys. So this line "
            "waits on your eye.\n\n"
            "Mark each card by how its pairs look to you, and note it if the top and bottom pairs look different. "
            "Open each large card to full size before you mark it. On a computer screen the small cards show at "
            "about their real size: dots, thin lines and words."
        ),
        "marks": [
            {"id": "alike", "label": "Can't tell them apart"},
            {"id": "slip", "label": "Looks like a mistake", "tone": "no"},
            {"id": "apart", "label": "Two greys, on purpose", "tone": "yes"},
        ],
        "pageNote": "Anything about the set as a whole? Once every card is marked, Claude shows you which gap each "
        "card was and proposes the grey line from your marks.",
        "items": items,
    }
    with open(os.path.join(out, "items.json"), "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()
