#!/usr/bin/env python3
"""look.py — a gate critic's view tools: zoom into a page, scrub its motion,
and measure a part or two pixels.

USAGE
  python3 look.py zoom <url or file> --clip X,Y,W,H --out FILE.png [--scale 4]
        [--width W] [--height H] [--after MS]
      The settled page, the clip (CSS px, page coordinates) shot at --scale
      times its pixels: 4, or 8 for the tightest bend of a curve. --after
      waits MS in place of SETTLE_MS, for motion a seek cannot reach (a
      canvas, a script's frames) that runs longer.
  python3 look.py scrub <url or file> --out DIR [--step 50] [--until 2500]
        [--wait SEL] [--width W] [--height H]
      The first screen, every --step ms of the page's timeline to --until, one
      PNG a frame, each named by its time, in place of an earlier scrub's.
      The timeline is read and seeked as check-frames.py hash reads and seeks
      it: time zero is the first animation's start, an animation a timer
      starts after it sits at its own time since then, and the frames are the
      motion at any speed they are played. --wait waits for the element that
      marks a start later than check-frames.py's QUIET_MS. A page that starts
      an animation when another finishes, or after its timeline was read, is
      refused and its frames are not written.
  python3 look.py measure <url or file> --at X,Y [--width W] [--height H]
        [--after MS]
      The part under the point (CSS px, page coordinates) on the settled page:
      its element, box, font size and weight, and colour. --after waits MS in
      place of SETTLE_MS, as zoom's does.
  python3 look.py pixels <png> --at X,Y --against X,Y
      Two pixels of a screenshot, their colours and their WCAG contrast ratio.

--width is 1920 unless given. --height is the first screen at that width: for
zoom and measure the one check-layout.py shoots (633 at 1920); for scrub the
motion scripts' window (945 at 1920). The settled page is the page once its
fonts load and SETTLE_MS have passed.

EXITS 0 done / 2 the arguments are wrong / 3 Playwright, its browser, numpy or
Pillow is missing / 4 the page did not load in time / 5 the browser refused the
page / 6 scrub cannot seek the page (why, on stdout) / 7 a call hung that would
never return.
"""

import argparse
import json
import os
import pathlib
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402


layout = siblings.load(HERE, "check-layout.py")
frames = siblings.load(HERE, "check-frames.py")
runner = siblings.load(HERE, "runner.py")
try:
    maths = siblings.load(HERE, "access-pixels.py")
except ImportError as err:
    sys.exit(runner.missing(err))
colour_space = siblings.load(
    HERE, os.path.join("..", "..", "design-project", "scripts", "colour_space.py")
)

WIDTH = layout.DESKTOP_WIDTH
SETTLE_MS = 4000  # guess, #170
FIRST_SCREEN = {
    "zoom": ("check-layout.py's first screen", layout.HEIGHTS),
    "measure": ("check-layout.py's first screen", layout.HEIGHTS),
    "scrub": ("the motion scripts' window", layout.MOTION_HEIGHTS),
}

MEASURE_JS = r"""
([x, y]) => {
  window.scrollTo(0, Math.max(0, y - innerHeight / 2));
  const el = document.elementFromPoint(x - scrollX, y - scrollY);
  if (!el) return null;
  const r = el.getBoundingClientRect();
  const cs = getComputedStyle(el);
  let label = el.tagName.toLowerCase();
  if (el.id) label += '#' + el.id;
  else if (el.classList.length) label += '.' + [...el.classList].join('.');
  return { element: label, text: (el.innerText || '').trim().slice(0, 60),
    box: [r.left + scrollX, r.top + scrollY, r.width, r.height].map((n) => Math.round(n * 10) / 10),
    font: cs.fontSize + ' ' + cs.fontWeight + ' ' + cs.fontFamily.split(',')[0], colour: cs.color,
    background: cs.backgroundColor };
}
"""


def numbers(p, flag, value, count):
    wants = f"{flag} wants {count} numbers joined by commas — got {value!r}"
    try:
        out = [float(n) for n in value.split(",")]
    except ValueError:
        p.error(wants)
    if len(out) != count:
        p.error(wants)
    return out


def parse(argv):
    p = argparse.ArgumentParser(prog="look.py", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    pages = {}
    for name in ("zoom", "scrub", "measure"):
        s = sub.add_parser(name)
        s.add_argument("page")
        s.add_argument("--width", type=int, default=WIDTH)
        s.add_argument(
            "--height",
            type=int,
            help=f"default: {FIRST_SCREEN[name][0]} at --width",
        )
        pages[name] = s
    pages["zoom"].add_argument("--clip", required=True)
    pages["zoom"].add_argument("--scale", type=int, default=4)  # guess, #501
    pages["zoom"].add_argument("--out", required=True)
    pages["scrub"].add_argument("--out", required=True)
    pages["scrub"].add_argument("--step", type=int, default=50)  # guess, #501
    pages["scrub"].add_argument("--until", type=int, default=2500)  # guess, #501
    pages["scrub"].add_argument("--wait")
    pages["measure"].add_argument("--at", required=True)
    for name in ("zoom", "measure"):
        pages[name].add_argument("--after", type=int, default=SETTLE_MS)
    px = sub.add_parser("pixels")
    px.add_argument("png")
    px.add_argument("--at", required=True)
    px.add_argument("--against", required=True)
    args = p.parse_args(argv)
    if args.cmd == "pixels":
        args.at, args.against = (
            numbers(p, f, getattr(args, f.strip("-")), 2) for f in ("--at", "--against")
        )
        return args
    if not layout.LOW <= args.width <= layout.HIGH:
        p.error(f"--width {args.width} is outside {layout.LOW}–{layout.HIGH}")
    for flag, least in (
        ("scale", 1),
        ("step", 1),
        ("until", 0),
        ("after", 0),
        ("height", 1),
        ("width", 1),
    ):
        value = getattr(args, flag, None)
        if value is not None and value < least:
            p.error(f"--{flag} wants {least} or more")
    if args.height is None:
        args.height = layout.height_at(args.width, FIRST_SCREEN[args.cmd][1])
    args.url = runner.page_url(p, args.page)
    if args.cmd == "zoom":
        args.clip = numbers(p, "--clip", args.clip, 4)
    if args.cmd == "measure":
        args.at = numbers(p, "--at", args.at, 2)
    return args


def settled_page(browser, args, scale=1):
    page = browser.new_page(
        viewport={"width": args.width, "height": args.height},
        device_scale_factor=scale,
        **layout.device(args.width),
    )
    page.set_default_timeout(runner.LOAD_TIMEOUT_MS)
    page.goto(args.url, wait_until="load")
    page.evaluate("document.fonts.ready")
    return page


def zoom(browser, args):
    page = settled_page(browser, args, args.scale)
    page.wait_for_timeout(args.after)
    x, y, w, h = args.clip
    page.screenshot(
        path=args.out, clip={"x": x, "y": y, "width": w, "height": h}, full_page=True
    )
    return f"wrote {args.out}: {w:g}x{h:g} CSS px at {args.scale}x, from a {args.width}x{args.height} screen"


def scrub(browser, args):
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("t[0-9][0-9][0-9][0-9][0-9].png"):
        old.unlink()
    at = frames.args_with(
        args,
        viewport_size={"width": args.width, "height": args.height},
        timeout=runner.LOAD_TIMEOUT_MS,
    )
    context, page, prep = frames.open_page(
        browser, at, 1, device=layout.device(args.width)
    )
    try:
        shots = frames.seek_shots(page, range(0, args.until + 1, args.step))
    finally:
        context.close()
    for t, png in shots:
        (out / f"t{t:05d}.png").write_bytes(png)
    return "\n".join(
        [
            f"wrote {len(shots)} frame(s) to {out}, every {args.step} ms to {args.until} ms, at {args.width}x{args.height}",
            *frames.still_note(prep["end"]),
        ]
    )


def measure(browser, args):
    page = settled_page(browser, args)
    page.wait_for_timeout(args.after)
    found = page.evaluate(MEASURE_JS, args.at)
    if found is None:
        return f"nothing is drawn at {args.at[0]:g},{args.at[1]:g}"
    return json.dumps(found, indent=1)


def pixels(args):
    try:
        from PIL import Image
    except ImportError as err:
        sys.exit(runner.missing(err))
    import numpy as np

    try:
        shot = np.asarray(Image.open(args.png).convert("RGB"))
    except OSError as err:
        print(f"look.py: {args.png} is no image it can read: {err}", file=sys.stderr)
        return 2
    h, w, _ = shot.shape
    colours = []
    for x, y in (args.at, args.against):
        if not (0 <= x < w and 0 <= y < h):
            print(f"look.py: {x:g},{y:g} is outside the {w}x{h} image", file=sys.stderr)
            return 2
        colours.append(shot[int(y), int(x)])
    ratio = float(colour_space.contrast(*colours))
    print(f"{maths.hexed(colours[0])} against {maths.hexed(colours[1])}: {ratio:.2f}:1")
    return 0


def main(argv):
    args = parse(argv)
    if args.cmd == "pixels":
        return pixels(args)
    work, flags = {
        "zoom": (zoom, []),
        "scrub": (scrub, frames.HASH_ARGS),
        "measure": (measure, []),
    }[args.cmd]

    def run():
        with runner.chromium(flags) as browser:
            return work(browser, args)

    said, code = runner.run_browser(
        run,
        runner.LOAD_TIMEOUT_MS,
        args.url,
        (
            f"cannot scrub {args.url}, because this page:",
            "Scrub it by eye: play it and watch, and say in the evidence that its frames went unseeked.",
        ),
    )
    if code:
        return code
    print(said)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
