#!/usr/bin/env python3
"""check-seams.py — measures the ground showing along every contact
check-curves.js --contacts lists, on look-renders.py contacts' crops at each
of its SCALES (design-vault#341).

USAGE
  python3 check-seams.py <svg file or saved page> --out DIR [--times MS,MS,…]
        [--width W] [--height H] [--wait SEL] [--timeout MS]

The file is the one check-curves.js --contacts reads: an .svg, or a page saved
after its scripts ran. At each scale and frame look-renders.py contacts shoots,
each contact is shot three times: as drawn, then with every element but its
two shapes hidden over a black ground, then over a white one. Their difference
is each device pixel's share of ground, and the pixel the two fills would make
with no ground showing (docs/research/contact-seams.md §3). Each pixel's
luminance Weber contrast against that pixel, summed across the contact per
unit of its length, times one device pixel's visual angle, is the seam's width
x contrast in arcsec: a contact fails at a scale where it reaches
THRESHOLD_ARCSEC. An overlap of two opaque
fills leaves the same pixels as an underlap, so it stays with
vault.contacts-look (§5). Residual: the window follows the edge's tangent at
the contact's point, so on an edge curving tighter than REACH across WINDOW a
seam bends out of it and is under-measured.

It writes look-renders.py's crops into DIR, and beside each the two mattes,
<name>-<ms>ms-<n>x-black.png and -white.png, at device size.

EXITS 0 no seam reaches the threshold / 1 one or more does (each printed) / 2
the arguments are wrong, or check-curves.js cannot read the file / 3 Node,
Playwright, its browser, numpy or Pillow is missing / 4 the page did not render
in time / 5 the browser refused the page / 6 none fails, but a contact cannot be
measured: a fill that lets the ground through, a contact off its crop, a shape
check-curves.js cannot read, or a page that cannot be rendered frame by frame.
Exits 0, 1 and 6 print on stdout; the rest print on stderr.
"""

import argparse
import importlib.util
import io
import json
import math
import os
import shlex
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


renders = _load("look_renders", os.path.join(HERE, "look-renders.py"))
flow = renders.flow
try:
    import numpy as np
    from PIL import Image
except ImportError as err:
    sys.exit(flow.missing(err))
colour_space = _load(
    "colour_space",
    os.path.join(HERE, "..", "..", "design-project", "scripts", "colour_space.py"),
)

# A seam shows once its width x luminance contrast reaches 0.5 arcsec: Hecht & Mintz 1939's thin-line floor, its
# partial-contrast form derived (docs/research/contact-seams.md §1.1, §6). A lab floor: everyday viewing's is untraced.
THRESHOLD_ARCSEC = 0.5
# One device pixel's visual angle in arcsec at the nearest typical viewing distance: derived (§1.2).
ARCSEC = {1: 109.0, 2: 47.0, 3: 35.0}
# Untraced, the #340 instrument's settings (§6): a ground share at or under half a code value is rounding; past
# ALL_GROUND, black / (1 - share) is too noisy and the fill on the pixel's side stands in; a luminance floor so a
# black fill cannot divide by zero.
NOISE = 0.5 / 255
ALL_GROUND = 0.95
DARK = 1e-4
# Untraced guesses, in CSS px: how far each side of the contact's point along its edge is measured, inside the
# CONTACT_SIZE crop; and how far across the edge each fill is looked for, past check-curves.js's 2 px contact
# distance with a pixel to spare.
WINDOW = 5
REACH = 3

# The underlap the remedy asks for: one device pixel at DPR 1 (§2).
UNDERLAP_CSS_PX = 1

CURVES = os.path.join(HERE, "check-curves.js")
GROUNDS = {"black": "#000", "white": "#fff"}
UNMEASURED = {
    "coincident": "both fills lie on one side of one edge, so no ground lies between them",
    "covered": "a shape painted over both fills its gap",
}
MATTE_CSS = """
:root, body {{ background: {ground} !important; }}
*, *::before, *::after {{ transition: none !important; }}
* {{ visibility: hidden !important; }}
{pair} {{ visibility: visible !important; }}
"""
# A <style> in the document's own namespace, so a bare SVG file takes it as an HTML page does.
MATTE_JS = r"""
(css) => {
  const root = document.documentElement;
  const ns = root.namespaceURI === 'http://www.w3.org/2000/svg' ? root.namespaceURI : 'http://www.w3.org/1999/xhtml';
  const style = document.createElementNS(ns, 'style');
  style.textContent = css;
  root.appendChild(style);
  window.__seamMatte = style;
}
"""
UNMATTE_JS = "() => { window.__seamMatte.remove(); delete window.__seamMatte; }"


def parse(argv):
    p = argparse.ArgumentParser(
        prog="check-seams.py", description=__doc__.split("\n\n")[0]
    )
    p.add_argument("file")
    p.add_argument("--out", required=True, metavar="DIR")
    p.add_argument("--times", metavar="MS,MS,…")
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--wait", metavar="SELECTOR")
    p.add_argument("--timeout", type=int, metavar="MS")
    args = p.parse_args(argv)
    if not os.path.isfile(args.file):
        p.error(
            f"no such file: {args.file} (check-curves.js reads a file, never a URL)"
        )
    return args


class UnlistedError(Exception):
    def __init__(self, code, why):
        super().__init__(why)
        self.code = code


def list_contacts(file):
    try:
        proc = subprocess.run(
            ["node", CURVES, "--contacts", "--json", file],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        raise UnlistedError(
            3,
            "Node is not on PATH; check-seams.py lists contacts with check-curves.js. Install Node.",
        ) from None
    if proc.returncode not in (0, 1, 6):
        raise UnlistedError(
            2, f"check-curves.js --contacts cannot read {file}: {proc.stderr.strip()}"
        )
    try:
        return json.loads(proc.stdout)
    except ValueError:
        raise UnlistedError(
            2,
            f"check-curves.js --contacts --json failed on {file} (exit {proc.returncode}): {proc.stderr.strip()}",
        ) from None


def look_args(args, measured):
    """look-renders.py contacts' arguments for the measured contacts, each carrying its pair and edge."""
    argv = ["contacts", args.file, "--out", args.out]
    for flag in ("times", "width", "height", "wait", "timeout"):
        if getattr(args, flag) is not None:
            argv += [f"--{flag}", str(getattr(args, flag))]
    for c in measured:
        argv += ["--contact", c["word"]]
    parsed = renders.parse(argv)
    for entry, c in zip(parsed.contact, measured, strict=True):
        entry.update(lower=c["lower"], upper=c["upper"], along=c["along"])
    return parsed


def shoot_mattes(page, args, *, contact, point, png):
    """Transitions are off while matted, or a hidden element would fade out across the shot."""
    ahead = page.evaluate(
        renders.POINT_JS,
        {"sel": contact["sel"], "x": contact["along"][0], "y": contact["along"][1]},
    )
    tangent = [ahead[0] - point[0], ahead[1] - point[1]]
    out = {"tangent": tangent, "drawn": png}
    for ground, colour in GROUNDS.items():
        css = MATTE_CSS.format(
            ground=colour, pair=f"{contact['lower']}, {contact['upper']}"
        )
        page.evaluate(MATTE_JS, css)
        try:
            png = page.screenshot(
                clip=renders.square(point, renders.CONTACT_SIZE),
                full_page=args.full_page,
            )
        finally:
            page.evaluate(UNMATTE_JS)
        out[ground] = png
    return out


def pixels(png):
    return np.asarray(Image.open(io.BytesIO(png)).convert("RGB"), dtype=float)


def luminance(rgb):
    """Relative luminance of an sRGB pixel of 0-255 floats, colour_space's weights."""
    return sum(
        w * colour_space.lin(v / 255)
        for w, v in zip(colour_space.SRGB_TO_XYZ[1], rgb, strict=True)
    )


def measure(drawn, mattes, tangent, scale):
    """The seam's width x contrast in arcsec, or None where no stretch of the window has an opaque fill on each side."""
    black, white = mattes["black"], mattes["white"]
    norm = math.hypot(*tangent)
    if norm == 0:
        return None
    tx, ty = tangent[0] / norm, tangent[1] / norm
    nx, ny = -ty, tx
    share = np.clip(((white - black) / 255).mean(axis=2), 0, 1)
    size = share.shape[0]
    mid = size / 2
    reach = REACH * scale

    def at(x, y):
        i, j = int(math.floor(y)), int(math.floor(x))
        return (i, j) if 0 <= i < size and 0 <= j < size else None

    def fill(x, y, sign):
        """The nearest opaque fill across the edge on one side, its colour and its distance, or None within reach."""
        for k in range(reach):
            step = sign * (k + 0.5)
            p = at(x + step * nx, y + step * ny)
            if p and share[p] <= NOISE:
                return black[p], step
        return None

    # Each device pixel's step along the edge where both fills are found is part of the contact's length; only the
    # pixels between those two fills are across the edge, never ground past a thin fill's far side.
    sides = {}
    for t in range(-WINDOW * scale, WINDOW * scale):
        x, y = mid + t * tx, mid + t * ty
        found = fill(x, y, -1), fill(x, y, 1)
        if found[0] is not None and found[1] is not None:
            sides[t] = found
    if not sides:
        return None
    weber = 0.0
    for i in range(size):
        for j in range(size):
            g = share[i, j]
            if g <= NOISE:
                continue
            dx, dy = j + 0.5 - mid, i + 0.5 - mid
            t, d = math.floor(dx * tx + dy * ty + 0.5), dx * nx + dy * ny
            if t not in sides or not sides[t][0][1] < d < sides[t][1][1]:
                continue
            clean = black[i, j] / (1 - g) if g < ALL_GROUND else sides[t][d >= 0][0]
            yc = luminance(np.clip(clean, 0, 255))
            weber += abs(luminance(drawn[i, j]) - yc) / max(yc, DARK)
    return weber / len(sides) * ARCSEC[scale]


def matte_name(shot, ground):
    return shot["file"].replace(".png", f"-{ground}.png")


def judge(contact, shots, out):
    seen, lost = {}, []
    for shot in shots:
        mats = {}
        for ground in GROUNDS:
            with open(os.path.join(out, matte_name(shot, ground)), "wb") as fh:
                fh.write(shot[ground])
            mats[ground] = pixels(shot[ground])
        drawn = pixels(shot["drawn"])
        wc = measure(drawn, mats, shot["tangent"], shot["scale"])
        where = f"{renders.frames.ms(shot['ms'])} ms {shot['scale']}x"
        if wc is None:
            lost.append(where)
        else:
            seen[where] = wc
    name, cls = contact["name"], contact["cls"]
    over = [w for w, v in seen.items() if v >= THRESHOLD_ARCSEC]
    figures = ", ".join(f"{w} {v:.2g}″" for w, v in seen.items())
    lines = []
    if over:
        lines.append(
            f"FAIL {name} ({cls}): the ground shows along the contact, width x contrast {figures}, "
            f"at or over {THRESHOLD_ARCSEC}″ at {', '.join(over)}; make the two fills one path, or run one "
            f"on under the other by at least {UNDERLAP_CSS_PX} CSS px. --contact {shlex.quote(contact['word'])}"
        )
    if lost:
        lines.append(
            f"NOT MEASURED {name} at {', '.join(lost)}: no opaque fill on each side of the contact within "
            f"{REACH} CSS px of its crop's centre; a translucent fill reads as ground. Judge it under "
            "vault.contacts-look."
        )
    elif not over:
        lines.append(f"pass {name} ({cls}): width x contrast {figures}")
    return lines, bool(over), bool(lost)


def main(argv):
    args = parse(argv)
    listed = list_contacts(args.file)
    for line in listed["notes"] + listed["unread"]:
        print(line)
    contacts = listed["contacts"]
    measured = [c for c in contacts if c["cls"] not in UNMEASURED]
    os.makedirs(args.out, exist_ok=True)
    lines, faults, unmeasured = [], 0, len(listed["unread"])
    for c in contacts:
        if c["cls"] in UNMEASURED:
            lines.append(f"pass {c['name']} ({c['cls']}): {UNMEASURED[c['cls']]}")
    if measured:
        look = look_args(args, measured)
        renders.clear(look.out)

        def run():
            # Animations on the main thread, so a matte and its crop draw one moment.
            with flow.chromium(renders.frames.HASH_ARGS) as browser:
                return renders.render_contacts(browser, look, also=shoot_mattes)

        result, code = flow.run_browser(
            run,
            look.timeout,
            look.url,
            (
                f"cannot render {look.url}, because this page:",
                "Judge its seams under vault.contacts-look from look-renders.py's crops, shot by hand.",
            ),
        )
        if code:
            return code
        for c in measured:
            said, failed, lost = judge(
                c, [s for s in result["shots"] if s["contact"] == c["name"]], look.out
            )
            lines += said
            faults += failed
            unmeasured += lost
        # look-renders.py's record, its mattes named, so the next run's clear() deletes them too.
        shots = [
            {
                **{k: v for k, v in s.items() if k not in (*GROUNDS, "drawn")},
                **{g: matte_name(s, g) for g in GROUNDS},
            }
            for s in result["shots"]
        ]
        shots += [{"file": matte_name(s, g)} for s in result["shots"] for g in GROUNDS]
        with open(os.path.join(look.out, "renders.json"), "w", encoding="utf8") as fh:
            json.dump({"page": look.url, **result, "shots": shots}, fh, indent=1)
            fh.write("\n")
    print(
        f"check-seams: {args.file}: {len(contacts)} contact(s), {len(measured)} measured at scales "
        f"{', '.join(f'{s}x' for s in renders.SCALES)}; a seam fails at {THRESHOLD_ARCSEC}″ width x contrast "
        "(docs/research/contact-seams.md)"
    )
    for line in lines:
        print(line)
    if not contacts and not unmeasured:
        print("no contact to measure: vault.contacts-seam does not apply")
    if faults:
        return 1
    return 6 if unmeasured else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except UnlistedError as err:
        print(err, file=sys.stderr)
        sys.exit(err.code)
