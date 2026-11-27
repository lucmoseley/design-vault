#!/usr/bin/env python3
"""look-renders.py — the renders vault.contacts-look and vault.curves-look ask
for.

USAGE
  python3 look-renders.py contacts <url or file> --contact NAME=[SELECTOR@]X,Y
        [--contact …] --out DIR [--times MS,MS,…] [--width W] [--height H]
        [--wait SEL] [--timeout MS]
  python3 look-renders.py bends <url or file> --out DIR [--width W]
        [--height H] [--wait SEL] [--timeout MS]

`contacts`: at device scales 1, 2 and 3, and at each frame check-frames.py
hash renders (time zero, every key frame and the end, or --times), it loads
the page fresh, seeks the frame, and shoots a CONTACT_SIZE CSS px square
centred on each contact. Each shot is then magnified 4x by repeating pixels,
never drawn again. A contact is X,Y in page CSS px, or SELECTOR@X,Y in the user
space of the first element SELECTOR matches: through its getScreenCTM() for an
SVG element, followed frame by frame; from its border box's top left for any other. Take the contacts from
vault.contacts-code's answer. It writes DIR/<name>-<ms>ms-<n>x.png, and one
sheet a frame, DIR/sheet-<ms>ms-<k>.png, of at most 2 x CONTACT_ROWS contacts,
each a labelled run of its 1x, 2x and 3x crops. A contact whose crops are the
same as on the last sheet it is on is left off a later frame's sheet.

`bends`: at the end frame, it reads every path, polygon, polyline, circle,
ellipse and rounded rect from the DOM, a shape a script draws among them, with
the transform each is drawn through. check-curves.js --bends finds each
subpath's tightest bend on the page as drawn, exact under any stretch or skew,
and each run of straight segments that stands in for a curve, at its sharpest
vertex in the shape's own units. A BEND_SIZE CSS px square around each is shot
at device scale 8. It writes DIR/bend-<k>.png and sheets DIR/sheet-<k>.png of
at most BEND_COLUMNS x BEND_ROWS bends. A curve an <img> draws is not in the
DOM: run bends on its SVG file too. One CSS or a canvas draws has no path data:
shoot its tightest bend by eye with look.py zoom --scale 8, at the --width and
--height bends ran at, which its report prints.

Both write DIR/renders.json naming every render, after deleting the renders an
earlier run's renders.json in DIR names, and refuse a page check-frames.py hash
refuses. --width and --height frame the page as the motion scripts do
(1920x945 unless given); a bare SVG
file larger than that is framed at its drawn size, which the report and
renders.json give. A sheet fits the standard image tier.

EXITS 0 written / 2 the arguments are wrong / 3 Playwright, its browser, numpy
or Pillow is missing / 4 the page did not render in time / 5 the browser refused
the page / 6 the page cannot be rendered frame by frame, a contact is not on it,
or a shape's path data cannot be read (the rest are still written) / 7 a call
hung that would never return. Exits 0 and 6 print on stdout; the rest print on
stderr.
"""

import argparse
import dataclasses
import hashlib
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402
from fail_open import expected  # noqa: E402


frames = siblings.load(HERE, "check-frames.py")
look = siblings.load(HERE, "look.py")
flow = frames.flow
runner = siblings.load(HERE, "runner.py")
conditions = siblings.load(HERE, "conditions.py")
try:
    from PIL import Image, ImageDraw
except ImportError as err:
    sys.exit(runner.missing(err))
UnmeasurableError = runner.UnmeasurableError

SCALES = (1, 2, 3)
MAGNIFY = 4
ZOOM = 8
CONTACT_SIZE = 16  # guess, #228
BEND_SIZE = 32  # guess, #228
GAP = 8  # guess, #228
LABEL = 14  # guess, #228
# Claude's standard image tier: at most 1568 px a long edge and 1568 tokens of 28x28 px,
# https://platform.claude.com/docs/en/build-with-claude/vision
CONTACT_ROWS = 6
BEND_COLUMNS, BEND_ROWS = 5, 3
LABEL_CHARS = 24  # guess, #228

POINT_JS = r"""
({ sel, x, y }) => {
  if (!sel) return [x, y];
  const el = document.querySelector(sel);
  if (!el) return null;
  if (el instanceof SVGGraphicsElement) {
    const m = el.getScreenCTM();
    if (!m) return null;
    return [m.a * x + m.c * y + m.e + scrollX, m.b * x + m.d * y + m.f + scrollY];
  }
  const r = el.getBoundingClientRect();
  return [r.left + x + scrollX, r.top + y + scrollY];
}
"""

SHAPES_JS = r"""
() => {
  const out = [];
  const oval = (cx, cy, rx, ry) =>
    `M${cx - rx} ${cy}A${rx} ${ry} 0 1 0 ${cx + rx} ${cy}A${rx} ${ry} 0 1 0 ${cx - rx} ${cy}Z`;
  const corner = (rx, ry, x, y) => `A${rx} ${ry} 0 0 1 ${x} ${y}`;
  for (const el of document.querySelectorAll('path, polygon, polyline, circle, ellipse, rect')) {
    const m = el.getScreenCTM();
    const box = el.getBoundingClientRect();
    if (!m || (box.width === 0 && box.height === 0)) continue;
    const cs = getComputedStyle(el);
    const n = (p) => parseFloat(cs[p]);
    const tag = el.tagName.toLowerCase();
    let shape = null;
    if (tag === 'path') shape = { d: el.getAttribute('d') || '' };
    else if (tag === 'polygon' || tag === 'polyline')
      shape = { points: el.getAttribute('points') || '', closed: tag === 'polygon' };
    else if (tag === 'circle' && n('r') > 0) shape = { d: oval(n('cx'), n('cy'), n('r'), n('r')) };
    else if (tag === 'ellipse' && n('rx') > 0 && n('ry') > 0)
      shape = { d: oval(n('cx'), n('cy'), n('rx'), n('ry')) };
    else if (tag === 'rect') {
      const [x, y, w, h] = ['x', 'y', 'width', 'height'].map(n);
      let [rx, ry] = [n('rx'), n('ry')];
      if (isNaN(rx)) rx = ry;
      if (isNaN(ry)) ry = rx;
      [rx, ry] = [Math.min(rx || 0, w / 2), Math.min(ry || 0, h / 2)];
      if (rx > 0 && ry > 0)
        shape = { d: `M${x + rx} ${y}H${x + w - rx}${corner(rx, ry, x + w, y + ry)}V${y + h - ry}`
          + `${corner(rx, ry, x + w - rx, y + h)}H${x + rx}${corner(rx, ry, x, y + h - ry)}`
          + `V${y + ry}${corner(rx, ry, x + rx, y)}Z` };
    }
    if (!shape) continue;
    let label = tag;
    if (el.id) label += '#' + el.id;
    else if (el.classList.length) label += '.' + [...el.classList].join('.');
    out.push({ ...shape, label, matrix: [m.a, m.b, m.c, m.d, m.e + scrollX, m.f + scrollY] });
  }
  return out;
}
"""

SVG_ROOT_JS = r"""
() => {
  const root = document.documentElement;
  if (!(root instanceof SVGSVGElement)) return null;
  const r = root.getBoundingClientRect();
  return [Math.ceil(r.right), Math.ceil(r.bottom)];
}
"""

CONTACT = re.compile(
    r"^([\w.-]+)=(?:(.+)@)?(-?\d+(?:\.\d+)?|-?\.\d+),(-?\d+(?:\.\d+)?|-?\.\d+)$"
)


def parse(argv):
    p = argparse.ArgumentParser(
        prog="look-renders.py", description=__doc__.split("\n\n")[0]
    )
    sub = p.add_subparsers(dest="mode", required=True)
    contacts = sub.add_parser("contacts")
    bends = sub.add_parser("bends")
    for s in (contacts, bends):
        s.add_argument("url")
        s.add_argument("--out", required=True, metavar="DIR")
        s.add_argument("--width", type=int, default=look.WIDTH)
        s.add_argument("--height", type=int)
        s.add_argument("--wait", metavar="SELECTOR")
        s.add_argument(
            "--timeout", type=int, default=runner.PLAY_TIMEOUT_MS, metavar="MS"
        )
    contacts.add_argument(
        "--contact", action="append", required=True, metavar="NAME=[SELECTOR@]X,Y"
    )
    contacts.add_argument("--times", metavar="MS,MS,…")
    args = p.parse_args(argv)
    if not conditions.LOW <= args.width <= conditions.HIGH:
        p.error(f"--width {args.width} is outside {conditions.LOW}–{conditions.HIGH}")
    args.viewport_size = {
        "width": args.width,
        "height": args.height
        or conditions.height_at(args.width, conditions.MOTION_HEIGHTS),
    }
    if args.mode == "contacts":
        found = []
        for c in args.contact:
            m = CONTACT.match(c)
            if not m:
                p.error(f"--contact wants NAME=X,Y or NAME=SELECTOR@X,Y — got {c!r}")
            name, sel, x, y = m.groups()
            if any(f["name"] == name for f in found):
                p.error(f"two contacts are named {name}")
            found.append({"name": name, "sel": sel, "x": float(x), "y": float(y)})
        args.contact = found
        try:
            args.times = args.times and [
                "end" if t.strip() == "end" else float(t) for t in args.times.split(",")
            ]
        except ValueError:
            p.error("--times wants numbers of ms, or `end`")
    args.url = runner.page_url(p, args.url)
    return args


def open_page(browser, load, scale, *, width, timeline=None):
    return frames.open_page(
        browser, load, scale, device=conditions.device(width), timeline=timeline
    )


def fit(browser, args):
    # #354
    load = frames.Load(args.url, args.viewport_size, args.timeout, args.wait)
    context, page, _ = open_page(browser, load, 1, width=args.width)
    try:
        drawn = page.evaluate(SVG_ROOT_JS)
    finally:
        context.close()
    if drawn is None:
        return load, True
    size = load.viewport
    viewport = {
        "width": max(size["width"], drawn[0]),
        "height": max(size["height"], drawn[1]),
    }
    return dataclasses.replace(load, viewport=viewport), False


def square(centre, size):
    return {
        "x": centre[0] - size / 2,
        "y": centre[1] - size / 2,
        "width": size,
        "height": size,
    }


def magnify(png):
    shot = Image.open(io.BytesIO(png))
    return shot.resize(
        (shot.width * MAGNIFY, shot.height * MAGNIFY), Image.Resampling.NEAREST
    )


def render_contacts(browser, args, also=None):
    load, full_page = fit(browser, args)
    prep = frames.read_timeline(browser, load, 1, conditions.device(args.width))
    times = frames.key_times(prep, args.times)
    shots = []
    for scale in SCALES:
        for t in times:
            context, page, _ = open_page(
                browser, load, scale, width=args.width, timeline=prep["timeline"]
            )
            try:
                frames.seek(page, t)
                taken = []
                for c in args.contact:
                    point = page.evaluate(POINT_JS, c)
                    if point is None:
                        raise UnmeasurableError(
                            [f"has no drawn element {c['sel']} for contact {c['name']}"]
                        )
                    png = page.screenshot(
                        clip=square(point, CONTACT_SIZE), full_page=full_page
                    )
                    name = f"{c['name']}-{frames.ms(t)}ms-{scale}x.png"
                    big = magnify(png)
                    big.save(os.path.join(args.out, name))
                    shot = {
                        "contact": c["name"],
                        "ms": t,
                        "scale": scale,
                        "at": [round(v, 2) for v in point],
                        "file": name,
                        "sha256": hashlib.sha256(big.tobytes()).hexdigest(),
                    }
                    taken.append((c, point, png, shot))
                    shots.append(shot)
                if also:
                    for c, point, png, shot in taken:
                        shot.update(
                            also(page, full_page, contact=c, point=point, png=png)
                        )
            finally:
                context.close()
    return {"viewport": load.viewport, "times": times, "shots": shots}


def find_bends(shapes):
    proc = subprocess.run(
        ["node", os.path.join(HERE, "check-curves.js"), "--bends", "--json"],
        input=json.dumps(
            [{k: v for k, v in s.items() if k != "label"} for s in shapes]
        ),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise UnmeasurableError(
            [f"check-curves.js --bends failed: {proc.stderr.strip()}"]
        )
    bends, unread = [], []
    for shape, found in zip(shapes, json.loads(proc.stdout), strict=True):
        if isinstance(found, dict):
            unread.append({"shape": shape["label"], "error": found["error"]})
            continue
        for b in found:
            bend = {"shape": shape["label"], "at": [round(v, 2) for v in b["at"]]}
            if "segments" in b:
                bend["segments"] = b["segments"]
            else:
                bend["radius"] = round(b["radius"], 3)
            bends.append(bend)
    return bends, unread


def render_bends(browser, args):
    load, full_page = fit(browser, args)
    context, page, prep = open_page(browser, load, ZOOM, width=args.width)
    try:
        frames.seek(page, prep["end"])
        bends, unread = find_bends(page.evaluate(SHAPES_JS))
        for k, b in enumerate(bends, 1):
            b["file"] = f"bend-{k}.png"
            page.screenshot(
                path=os.path.join(args.out, b["file"]),
                clip=square(b["at"], BEND_SIZE),
                full_page=full_page,
            )
        frames.refuse_chain(page)
    finally:
        context.close()
    return {
        "viewport": load.viewport,
        "end_ms": prep["end"],
        "bends": bends,
        "unread": unread,
    }


def sheet(tiles, columns, out):
    rows = [tiles[i : i + columns] for i in range(0, len(tiles), columns)]
    width = max(sum(im.width for _, im in r) + GAP * (len(r) + 1) for r in rows)
    heights = [max(im.height for _, im in r) + LABEL + GAP for r in rows]
    board = Image.new("RGB", (width, sum(heights) + GAP), "white")
    draw = ImageDraw.Draw(board)
    y = GAP
    for r, tall in zip(rows, heights, strict=True):
        x = GAP
        for label, im in r:
            draw.text((x, y), label, fill="black")
            board.paste(im, (x, y + LABEL))
            draw.rectangle(
                (x - 1, y + LABEL - 1, x + im.width, y + LABEL + im.height),
                outline="magenta",
            )
            x += im.width + GAP
        y += tall
    board.save(out)


def tile(args, label, file):
    with Image.open(os.path.join(args.out, file)) as im:
        return label, im.copy()


def contact_sheets(args, result):
    sheets, unchanged, last = [], [], {}
    for t in result["times"]:
        due = []
        for c in args.contact:
            mine = [
                s for s in result["shots"] if s["ms"] == t and s["contact"] == c["name"]
            ]
            seen = tuple(s["sha256"] for s in mine)
            if last.get(c["name"]) == seen:
                unchanged.append([c["name"], t])
                continue
            last[c["name"]] = seen
            due.append(mine)
        per = 2 * CONTACT_ROWS
        for k in range(0, len(due), per):
            tiles = [
                tile(args, f"{s['contact']} {frames.ms(t)} ms {s['scale']}x", s["file"])
                for mine in due[k : k + per]
                for s in mine
            ]
            name = f"sheet-{frames.ms(t)}ms-{k // per + 1}.png"
            sheet(tiles, 2 * len(SCALES), os.path.join(args.out, name))
            sheets.append(name)
    result["unchanged"] = unchanged
    return sheets


def bend_sheets(args, result):
    per = BEND_COLUMNS * BEND_ROWS
    sheets = []
    for k in range(0, len(result["bends"]), per):
        tiles = [
            tile(args, f"{b['file'][:-4]} {b['shape'][:LABEL_CHARS]}", b["file"])
            for b in result["bends"][k : k + per]
        ]
        name = f"sheet-{k // per + 1}.png"
        sheet(tiles, BEND_COLUMNS, os.path.join(args.out, name))
        sheets.append(name)
    return sheets


def report_contacts(args, result):
    size = result["viewport"]
    lines = [
        f"look-renders contacts: {args.url} at {size['width']}x{size['height']}",
        f"{len(args.contact)} contact(s) x {len(result['times'])} frame(s) "
        f"({', '.join(frames.ms(t) for t in result['times'])} ms) x scales "
        f"{', '.join(f'{s}x' for s in SCALES)}: {len(result['shots'])} crop(s) of "
        f"{CONTACT_SIZE} CSS px, magnified {MAGNIFY}x, on {len(result['sheets'])} sheet(s) in {args.out}",
    ]
    left = result["unchanged"]
    if left:
        lines.append(
            f"{len(left)} contact frame(s) left off the sheets, the same as the last sheet's: "
            + ", ".join(
                f"{n} at {frames.ms(t)} ms" for n, t in left[: flow.NAMES_SHOWN]
            )
            + (", …" if len(left) > flow.NAMES_SHOWN else "")
        )
    return "\n".join(lines), 0


def zoom_flags(size):
    return f"--width {size['width']} --height {size['height']}"


def report_bends(args, result):
    size = result["viewport"]
    bends, unread = result["bends"], result["unread"]
    lines = [
        f"look-renders bends: {args.url} at {size['width']}x{size['height']}, the end frame ({frames.ms(result['end_ms'])} ms)",
        *frames.still_note(result["end_ms"]),
    ]
    if bends:
        lines.append(
            f"{len(bends)} bend(s) shot at {ZOOM}x, {BEND_SIZE} CSS px each, on {len(result['sheets'])} sheet(s) in {args.out}"
        )
    elif not unread:
        lines.append(
            "no SVG shape on the page draws a curve: vault.curves-look does not apply, "
            "unless CSS or a canvas draws one (shoot that by eye with look.py zoom --scale 8 "
            f"{zoom_flags(size)})"
        )
    for b in bends:
        what = (
            f"{b['segments']} straight segments bending like a curve"
            if "segments" in b
            else f"radius {b['radius']:g} px"
        )
        lines.append(
            f"  {b['file']}: {b['shape']} at ({b['at'][0]:g}, {b['at'][1]:g}) px, {what}"
        )
    for u in unread:
        lines.append(
            f"  {u['shape']}: could not read the path, so its bends are not shot: {u['error']}"
        )
    return "\n".join(lines), 6 if unread else 0


MODES = {
    "contacts": (render_contacts, contact_sheets, report_contacts),
    "bends": (render_bends, bend_sheets, report_bends),
}


def clear(out):
    path = os.path.join(out, "renders.json")
    try:
        with open(path, encoding="utf8") as fh:
            old = json.load(fh)
    except FileNotFoundError as exc:
        expected(exc, "no earlier run to clear")
        return
    except ValueError as exc:
        sys.exit(
            f"look-renders.py: {path} does not parse ({exc}); delete it and the renders beside it"
        )
    named = old.get("sheets", []) + [
        r["file"] for r in old.get("shots", []) + old.get("bends", []) if "file" in r
    ]
    for name in named + ["renders.json"]:
        path = os.path.join(out, os.path.basename(name))
        if os.path.isfile(path):
            os.remove(path)


def main(argv):
    args = parse(argv)
    render, lay_out, report = MODES[args.mode]
    os.makedirs(args.out, exist_ok=True)
    clear(args.out)

    def run():
        with runner.chromium(frames.HASH_ARGS) as browser:
            return render(browser, args)

    result, code = runner.run_browser(
        run,
        args.timeout,
        args.url,
        (
            f"cannot render {args.url}, because this page:",
            f"Shoot it by hand with look.py zoom {zoom_flags(args.viewport_size)}: each contact at --scale 1, 2 and 3, "
            "each shot magnified 4x with Pillow's Image.NEAREST; each bend at --scale 8.",
        ),
    )
    if code:
        return code
    result["sheets"] = lay_out(args, result)
    with open(os.path.join(args.out, "renders.json"), "w", encoding="utf8") as fh:
        json.dump({"page": args.url, **result}, fh, indent=1)
        fh.write("\n")
    said, code = report(args, result)
    print(said)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
