#!/usr/bin/env python3
"""Measures the ground showing along every contact check-curves.js --contacts
lists, on look-renders.py contacts' crops at each of its SCALES.

USAGE
  python3 check-seams.py <svg file or saved page> --out DIR [--times MS,MS,…]
        [--width W] [--height H] [--wait SEL] [--timeout MS]

The file is the one check-curves.js --contacts reads: an .svg, or a page saved
after its scripts ran. At each scale and frame look-renders.py contacts shoots,
each contact is shot three times: as drawn, then with every element but its
two shapes and, for a covered contact, the covers check-curves.js names hidden,
over a black ground, then over a white one. So a cover whose paint lets the
ground through shows as a seam, whatever sets that paint. The matte forces what
it shows visible, so a cover the page's visibility hides at that frame is left
out of it, and the gap it would have filled shows. Their difference
is each device pixel's share of ground, and the pixel the two fills would make
with no ground showing. Each pixel's
luminance Weber contrast against that pixel, summed across the contact per
unit of its length, times one device pixel's visual angle, is the seam's width
x contrast in arcsec: a contact fails at a scale where it reaches
THRESHOLD_ARCSEC. An overlap of two opaque fills is not judged here:
vault.contacts-look judges it.

It writes look-renders.py's crops into DIR, and beside each the two mattes,
<name>-<ms>ms-<n>x-black.png and -white.png, at device size.

EXITS 0 no seam reaches the threshold / 1 one or more does (each printed) / 2
the arguments are wrong, or check-curves.js cannot read the file / 3 Node,
Playwright, its browser, numpy or Pillow is missing / 4 the page did not render
in time / 5 the browser refused the page / 6 none fails, but a contact cannot be
measured: a fill that lets the ground through, a contact off its crop, a shape
check-curves.js cannot read, a cover whose selector names no element in the
page, or a page that cannot be rendered frame by frame.
Exits 0, 1 and 6 print on stdout; the rest print on stderr.
An exception it does not handle exits 2, its traceback on stderr.
"""

import argparse
import io
import json
import math
import os
import shlex
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import crash_exit  # noqa: E402

crash_exit.guard(__name__)
import siblings  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402


renders = siblings.load(HERE, "look-renders.py")
frames = siblings.load(HERE, "check-frames.py")
runner = siblings.load(HERE, "runner.py")
colour_space = siblings.load(
    HERE, os.path.join("..", "..", "design-project", "scripts", "colour_space.py")
)

# measured 0.5 arcsec (Hecht & Mintz 1939), #341
THRESHOLD_ARCSEC = 0.5
# guess, #341
ARCSEC = {1: 109.0, 2: 47.0, 3: 35.0}
# guess, #341
NOISE = 0.5 / 255
# guess, #341
ALL_GROUND = 0.95
# guess, #341
DARK = 1e-4
# guess, #341
WINDOW = 5
# guess, #544
REACH_PAST_CONTACT_PX = 1

# guess, #341
UNDERLAP_CSS_PX = 1

CURVES = os.path.join(HERE, "check-curves.js")
GROUNDS = {"black": "#000", "white": "#fff"}
UNMEASURED = {
    "coincident": "both fills lie on one side of one edge, so no ground lies between them",
}
MATTE_CSS = """
:root, body {{ background: {ground} !important; }}
*, *::before, *::after {{ transition: none !important; }}
*:not(clipPath *, mask *, pattern *) {{ visibility: hidden !important; }}
clipPath, mask, pattern, {shown} {{ visibility: visible !important; }}
"""
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
COVERS_JS = r"""
(sels) => sels.map((sel) => {
  const el = document.querySelector(sel);
  return el ? getComputedStyle(el).visibility === 'visible' : null;
})
"""


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
    argv = ["contacts", args.file, "--out", args.out]
    for flag in ("times", "width", "height", "wait", "timeout"):
        if getattr(args, flag) is not None:
            argv += [f"--{flag}", str(getattr(args, flag))]
    for c in measured:
        argv += ["--contact", c["word"]]
    parsed = renders.parse(argv)
    for entry, c in zip(parsed.contact, measured, strict=True):
        entry.update(
            lower=c["lower"], upper=c["upper"], along=c["along"], covers=c["covers"]
        )
    return parsed


def shoot_mattes(page, full_page, *, contact, point, png):
    ahead = page.evaluate(
        renders.POINT_JS,
        {"sel": contact["sel"], "x": contact["along"][0], "y": contact["along"][1]},
    )
    tangent = [ahead[0] - point[0], ahead[1] - point[1]]
    out = {"tangent": tangent, "drawn": png}
    drawn = page.evaluate(COVERS_JS, contact["covers"])
    missing = [s for s, v in zip(contact["covers"], drawn, strict=True) if v is None]
    if missing:
        raise renders.UnmeasurableError(
            [
                f"has no element {s} for a cover of contact {contact['name']}"
                for s in missing
            ]
        )
    covers = [s for s, v in zip(contact["covers"], drawn, strict=True) if v]
    for ground, colour in GROUNDS.items():
        css = MATTE_CSS.format(
            ground=colour,
            shown=", ".join([contact["lower"], contact["upper"], *covers]),
        )
        page.evaluate(MATTE_JS, css)
        try:
            png = page.screenshot(
                clip=renders.square(point, renders.CONTACT_SIZE),
                full_page=full_page,
            )
        finally:
            page.evaluate(UNMATTE_JS)
        out[ground] = png
    return out


def pixels(png):
    return np.asarray(Image.open(io.BytesIO(png)).convert("RGB"), dtype=float)


def measure(drawn, mattes, tangent, scale, *, reach):
    black, white = mattes["black"], mattes["white"]
    norm = math.hypot(*tangent)
    if norm == 0:
        return None
    tx, ty = tangent[0] / norm, tangent[1] / norm
    nx, ny = -ty, tx
    share = np.clip(((white - black) / 255).mean(axis=2), 0, 1)
    size = share.shape[0]
    mid = size / 2
    reach *= scale

    def at(x, y):
        i, j = int(math.floor(y)), int(math.floor(x))
        return (i, j) if 0 <= i < size and 0 <= j < size else None

    def fill(x, y, sign):
        for k in range(reach):
            step = sign * (k + 0.5)
            p = at(x + step * nx, y + step * ny)
            if p and share[p] <= NOISE:
                return black[p], step
        return None

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
            yc = colour_space.luminance(np.clip(clean, 0, 255))
            weber += abs(colour_space.luminance(drawn[i, j]) - yc) / max(yc, DARK)
    return weber / len(sides) * ARCSEC[scale]


def matte_name(shot, ground):
    return shot["file"].replace(".png", f"-{ground}.png")


def judge(contact, shots, out, *, reach):
    seen, lost = {}, []
    for shot in shots:
        mats = {}
        for ground in GROUNDS:
            with open(os.path.join(out, matte_name(shot, ground)), "wb") as fh:
                fh.write(shot[ground])
            mats[ground] = pixels(shot[ground])
        drawn = pixels(shot["drawn"])
        wc = measure(drawn, mats, shot["tangent"], shot["scale"], reach=reach)
        where = f"{frames.ms(shot['ms'])} ms {shot['scale']}x"
        if wc is None:
            lost.append(where)
        else:
            seen[where] = wc
    name, cls = contact["name"], contact["cls"]
    over = [w for w, v in seen.items() if v >= THRESHOLD_ARCSEC]
    figures = ", ".join(f"{w} {v:.2g}″" for w, v in seen.items())
    lines = []
    if over:
        cover = ", or paint its cover opaque" if contact["covers"] else ""
        lines.append(
            f"FAIL {name} ({cls}): the ground shows along the contact, width x contrast {figures}, "
            f"at or over {THRESHOLD_ARCSEC}″ at {', '.join(over)}; make the two fills one path, or run one "
            f"on under the other by at least {UNDERLAP_CSS_PX} CSS px{cover}. --contact {shlex.quote(contact['word'])}"
        )
    if lost:
        lines.append(
            f"NOT MEASURED {name} at {', '.join(lost)}: no opaque fill on each side of the contact within "
            f"{reach} CSS px of its crop's centre; a translucent fill reads as ground. Judge it under "
            "vault.contacts-look."
        )
    elif not over:
        lines.append(f"pass {name} ({cls}): width x contrast {figures}")
    return lines, bool(over), bool(lost)


def main(argv):
    args = parse(argv)
    try:
        listed = list_contacts(args.file)
    except UnlistedError as err:
        print(err, file=sys.stderr)
        sys.exit(err.code)
    reach = listed["contactPx"] + REACH_PAST_CONTACT_PX
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
            with runner.chromium(frames.HASH_ARGS) as browser:
                return renders.render_contacts(browser, look, also=shoot_mattes)

        result, code = runner.run_browser(
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
                c,
                [s for s in result["shots"] if s["contact"] == c["name"]],
                look.out,
                reach=reach,
            )
            lines += said
            faults += failed
            unmeasured += lost
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
    sys.exit(main(sys.argv[1:]))
