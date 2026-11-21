#!/usr/bin/env python3
"""contact-seams — the #340 instrument: what a gap or conflation seam at a
contact between two SVG fills leaves in look-renders.py contacts' crops at
device pixel ratios 1, 2 and 3, as docs/research/contact-seams.md reads it.

  python3 docs/data/contact-seams-2026-10-16.py RUN_DIR OUT.csv

From the repo root. On each of five grounds, two fills, A drawn first and B
second, meet at a contact through the centre of a crop. Each contact is a
shared edge (vertical at five sub-pixel offsets, slanted, or on a circle), a
gap of a given CSS px width, or an underlap (A runs on under B). It writes
the page three times, RUN_DIR/page-drawn.html, then with every ground black
(page-black.html), then white (page-white.html), and renders each through
look-renders.py contacts. The ground share of each device px is
(white - black) / 255, the two-backing matte; the pixel the fills would make
with no ground showing is black / (1 - share).

Per crop, over a window WIN CSS px each side of the contact, it reports the
largest ground share; the ground share summed across the edge per unit of
its length, in CSS px (the equivalent ground width); and the luminance Weber
contrast of each pixel against its no-ground pixel, summed the same way and
times one device px's visual angle (wc_arcsec: width x contrast, the form of
Hecht & Mintz 1939's thin-line threshold).
"""

import csv
import importlib.util
import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image

ROOT = os.getcwd()
SCRIPTS = os.path.join(ROOT, "plugin/skills/design-round/scripts")
LOOK_RENDERS = os.path.join(SCRIPTS, "look-renders.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cs = load(
    "colour_space",
    os.path.join(ROOT, "plugin/skills/design-project/scripts/colour_space.py"),
)
look = load("look_renders", LOOK_RENDERS)
SCALES = look.SCALES
# Each crop is look.MAGNIFY x larger by repeating pixels, so every
# MAGNIFY-th pixel is the device pixel itself.
MAGNIFY = look.MAGNIFY
CONTACT_SIZE = look.CONTACT_SIZE  # CSS px

# Untraced guesses, each enough for its job and nothing more:
WIN = 5  # CSS px each side of the contact, inside the 16 px crop
SIDE = 4  # CSS px from the contact where each fill is read, inside WIN
SHIFT = 0.37  # CSS px, off the pixel grid at every DPR, for all but shared-v
NOISE = 0.5 / 255  # a ground share at or under half a code value is rounding
ALL_GROUND = 0.95  # past this share, black / (1 - share) is too noisy to use
DARK = 1e-4  # a luminance floor, so a black no-ground pixel cannot divide by 0
ARC_SAMPLES = 20000  # points along a circle when counting its length in WIN

# One cell per contact: a SHAPE px square pair inside a MARGIN of its ground.
# A slanted pair runs SHAPE / 2 past the square on each side, so its ends fall
# outside the crop and every neighbour's window.
SHAPE, MARGIN = 40, 10
CELL = SHAPE + 2 * MARGIN
HALF = SHAPE / 2

# One device px's visual angle in arcsec, at the nearest typical viewing:
# 96 dpi at 50 cm (OSHA's near end), 224 ppi at 50 cm, 460 ppi at 32.2 cm
# (Bababekova et al. 2011's mean for web reading).
ARCSEC = {1: 109.0, 2: 47.0, 3: 35.0}

GROUNDS = {
    # name: (A, B, ground)
    "light-on-dark": ("#e8dcc4", "#d9c7a6", "#14181f"),
    "blue-orange-on-white": ("#1a4d8f", "#e0a030", "#ffffff"),
    "near-ground": ("#6f7a70", "#7d7468", "#76786f"),
    "dark-on-paper": ("#2b2b2b", "#3a3530", "#f4efe6"),
    "ground-between": ("#1d2a4a", "#efe3c8", "#b0503c"),
}

# (case, param, shape, gap, where): gap is CSS px of ground between the fills,
# negative for an underlap; where is the edge's offset off the pixel grid for
# "v", its slant in degrees for "slant", and the disc's radius for "arc".
CASES = (
    [("shared-v", round(o, 3), "v", 0.0, o) for o in (0, 0.125, 0.25, 1 / 3, 0.5)]
    + [("shared-slant", d, "slant", 0.0, d) for d in (5, 30, 45)]
    + [("shared-arc", 15, "arc", 0.0, 15)]
    + [
        ("gap-v", round(g, 3), "v", g, SHIFT)
        for g in (0.02, 0.05, 0.1, 0.2, 0.25, 1 / 3, 0.5, 1, 2)
    ]
    + [("gap-slant30", g, "slant", g, 30) for g in (0.05, 0.1, 0.25, 0.5, 1)]
    + [("gap-arc", g, "arc", g, 15) for g in (0.05, 0.1, 0.25, 0.5)]
    + [("underlap-v", u, "v", -u, SHIFT) for u in (0.5, 2)]
    + [("underlap-slant30", 2, "slant", -2, 30), ("underlap-arc", 2, "arc", -2, 15)]
)


def luminance(rgb):
    """Relative luminance of an sRGB pixel of 0-255 floats."""
    return sum(w * cs.lin(v / 255) for w, v in zip(cs.SRGB_TO_XYZ[1], rgb, strict=True))


def arc_length(cx, cy, r, centre):
    inside = sum(
        abs(cx + r * math.cos(2 * math.pi * i / ARC_SAMPLES) - centre[0]) <= WIN
        and abs(cy + r * math.sin(2 * math.pi * i / ARC_SAMPLES) - centre[1]) <= WIN
        for i in range(ARC_SAMPLES)
    )
    return 2 * math.pi * r * inside / ARC_SAMPLES


def cell(case, origin, fills):
    """The SVG for one contact, its centre, its unit normal and the edge's
    length inside the window, in CSS px."""
    _, _, shape, gap, where = case
    (x0, y0), (a, b) = origin, fills
    cx, cy = x0 + HALF, y0 + HALF
    over = max(-gap, 0)
    gap = max(gap, 0)
    if shape == "v":
        ex = cx + where
        svg = (
            f'<rect x="{x0}" y="{y0}" width="{ex + over - x0}" height="{SHAPE}" fill="{a}"/>'
            f'<rect x="{ex + gap}" y="{y0}" width="{x0 + SHAPE - ex - gap}" height="{SHAPE}" fill="{b}"/>'
        )
        return svg, (ex + gap / 2, cy), (1.0, 0.0), 2 * WIN
    if shape == "slant":
        tan = math.tan(math.radians(where))
        cos = math.cos(math.radians(where))
        ex = cx + SHIFT

        def at(y, shift):
            return ex + shift + (y - cy) * tan

        y1 = y0 + SHAPE
        left, right = x0 - HALF, x0 + SHAPE + HALF
        svg = (
            f'<polygon points="{left},{y0} {at(y0, over)},{y0} {at(y1, over)},{y1} {left},{y1}" fill="{a}"/>'
            f'<polygon points="{at(y0, gap)},{y0} {right},{y0} {right},{y1} {at(y1, gap)},{y1}" fill="{b}"/>'
        )
        normal = (cos, -math.sin(math.radians(where)))
        return svg, (ex + gap / 2, cy), normal, 2 * WIN / cos
    # A disc of radius `where`, B a square with a hole of where + gap; the
    # contact at 45 degrees on it.
    cx += SHIFT
    ra, rb = where + over, where + gap
    svg = (
        f'<circle cx="{cx}" cy="{cy}" r="{ra}" fill="{a}"/>'
        f'<path fill-rule="evenodd" fill="{b}" d="M{x0 - MARGIN} {y0 - MARGIN}h{CELL}v{CELL}h-{CELL}z'
        f'M{cx - rb} {cy}a{rb} {rb} 0 1 0 {2 * rb} 0a{rb} {rb} 0 1 0 {-2 * rb} 0z"/>'
    )
    ang = math.radians(-45)
    rm = where + gap / 2
    centre = (cx + rm * math.cos(ang), cy + rm * math.sin(ang))
    return svg, centre, (math.cos(ang), math.sin(ang)), arc_length(cx, cy, rm, centre)


def build(run):
    svg, contacts = [], []
    for row, (name, (a, b, ground)) in enumerate(GROUNDS.items()):
        for col, case in enumerate(CASES):
            origin = (col * CELL + MARGIN, row * CELL + MARGIN)
            body, centre, normal, length = cell(case, origin, (a, b))
            svg.append(
                f'<rect x="{origin[0] - MARGIN}" y="{origin[1] - MARGIN}" width="{CELL}" '
                f'height="{CELL}" fill="{ground}"/>' + body
            )
            contacts.append(
                {
                    "name": f"{name}.{case[0]}.{case[1]}",
                    "ground": name,
                    "case": case[0],
                    "param": case[1],
                    "centre": centre,
                    "normal": normal,
                    "length": length,
                }
            )
    html = (
        '<!doctype html><html><body style="margin:0;background:#888">'
        f'<svg width="{len(CASES) * CELL}" height="{len(GROUNDS) * CELL}" style="display:block">'
        + "".join(svg)
        + "</svg></body></html>"
    )
    os.makedirs(run, exist_ok=True)
    pages = {"drawn": html}
    for tag, colour in (("black", "#000000"), ("white", "#ffffff")):
        page = html.replace("background:#888", f"background:{colour}")
        for _, _, ground in GROUNDS.values():
            page = page.replace(f'fill="{ground}"/>', f'fill="{colour}"/>')
        pages[tag] = page
    args = []
    for contact in contacts:
        x, y = contact["centre"]
        args += ["--contact", f"{contact['name']}={x:.4f},{y:.4f}"]
    for tag, page in pages.items():
        path = os.path.join(run, f"page-{tag}.html")
        with open(path, "w") as f:
            f.write(page)
        subprocess.run(
            [
                sys.executable,
                LOOK_RENDERS,
                "contacts",
                path,
                *args,
                "--out",
                os.path.join(run, tag),
            ],
            check=True,
            capture_output=True,
        )
    return contacts


def crop(run, tag, name, scale):
    path = os.path.join(run, tag, f"{name}-0ms-{scale}x.png")
    return np.asarray(Image.open(path).convert("RGB"), dtype=float)[
        ::MAGNIFY, ::MAGNIFY
    ]


def measure(run, contact, scale):
    drawn, black, white = (
        crop(run, t, contact["name"], scale) for t in ("drawn", "black", "white")
    )
    share = np.clip(((white - black) / 255).mean(axis=2), 0, 1)
    mid = CONTACT_SIZE * scale / 2
    nx, ny = contact["normal"]

    def side(d):
        y, x = int(mid + d * ny * scale), int(mid + d * nx * scale)
        return black[y, x] / max(1 - share[y, x], 1e-6)

    fills = (side(-SIDE), side(SIDE))
    lo, hi = int(mid - WIN * scale), int(mid + WIN * scale)
    ground_sum = weber_sum = peak = 0.0
    for y in range(lo, hi):
        for x in range(lo, hi):
            g = share[y, x]
            if g <= NOISE:
                continue
            peak = max(peak, g)
            ground_sum += g
            if g < ALL_GROUND:
                clean = black[y, x] / (1 - g)
            else:  # the fill on this pixel's side of the contact
                d = (x + 0.5 - mid) * nx + (y + 0.5 - mid) * ny
                clean = fills[d >= 0]
            yc = luminance(np.clip(clean, 0, 255))
            weber_sum += abs(luminance(drawn[y, x]) - yc) / max(yc, DARK)
    length = contact["length"] * scale  # device px
    return {
        "peak_ground": round(peak, 4),
        "ground_width_css": round(ground_sum / length / scale, 4),
        "wc_arcsec": round(weber_sum / length * ARCSEC[scale], 2),
    }


def blend_check(run):
    """The edge pixel of blue-orange-on-white's shared-v 0.25 at DPR 1, where
    A covers 1/4 of it and B 3/4, against source-over blending in
    sRGB-encoded values and in linear light."""
    a, b, ground = (
        np.array([int(h[i : i + 2], 16) for i in (1, 3, 5)], dtype=float)
        for h in GROUNDS["blue-orange-on-white"]
    )
    mid = CONTACT_SIZE // 2
    seen = crop(run, "drawn", "blue-orange-on-white.shared-v.0.25", 1)[mid, mid]
    cover = 0.25
    encoded = (1 - cover) * b + cover * (cover * a + (1 - cover) * ground)

    def decode(v):
        return np.array([cs.lin(c / 255) for c in v])

    def encode(v):
        return np.array(
            [
                255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)
                for c in v
            ]
        )

    linear = encode(
        (1 - cover) * decode(b)
        + cover * (cover * decode(a) + (1 - cover) * decode(ground))
    )
    print(
        f"edge pixel {seen.tolist()}; sRGB-encoded blend {encoded.round(1).tolist()}; linear-light blend {linear.round(1).tolist()}"
    )


def main(run, out):
    contacts = build(run)
    blend_check(run)
    rows = [
        {
            "contact": contact["name"],
            "ground": contact["ground"],
            "case": contact["case"],
            "param": contact["param"],
            "dpr": s,
            **measure(run, contact, s),
        }
        for contact in contacts
        for s in SCALES
    ]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(run, "contacts.json"), "w") as f:
        json.dump(contacts, f, indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:3])
