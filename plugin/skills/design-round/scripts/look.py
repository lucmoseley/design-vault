#!/usr/bin/env python3
"""look.py — a gate critic's view tools: zoom into a page, scrub its motion,
and measure a part or two pixels, so a critic settles a question by looking
closer rather than guessing (design-vault#169 Q1 (A), #170).

USAGE
  python3 look.py zoom <url or file> --clip X,Y,W,H --out FILE.png [--scale 4]
        [--width W] [--height H]
      The settled page, the clip (CSS px, page coordinates) shot at --scale
      times its pixels: 4, or 8 for the tightest bend of a curve.
  python3 look.py scrub <url or file> --out DIR [--step 50] [--until 2500]
        [--width W] [--height H]
      The first screen from load, every --step ms of animation time to
      --until, one PNG a frame, each named by its time: every Web Animations
      API animation is paused and seeked, so the frames are the motion at any
      speed they are played.
  python3 look.py measure <url or file> --at X,Y [--width W] [--height H]
      The part under the point (CSS px, page coordinates) on the settled page:
      its element, box, font size and weight, and colour.
  python3 look.py pixels <png> --at X,Y --against X,Y
      Two pixels of a screenshot, their colours and their WCAG contrast ratio.

--width is 1920 unless given, and --height is the first screen check-layout.py
shoots at that width, so a zoom, scrub or measure frames the page as the
critic's screenshots do. The settled page is the page once its fonts load and
SETTLE_MS have passed.

EXITS 0 done / 2 the arguments are wrong / 3 Playwright, its browser, numpy or
Pillow is missing / 4 the page did not load in time / 5 the browser refused the
page / 7 a call hung that would never return.
"""

import argparse
import importlib.util
import json
import os
import pathlib
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sibling(name):
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_")[:-3], os.path.join(HERE, name)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


layout = sibling("check-layout.py")
flow = layout.flow
try:
    maths = sibling("access-pixels.py")
except ImportError as err:
    sys.exit(flow.missing(err))

# The width a critic's desktop screenshots are taken at (#197).
WIDTH = layout.DESKTOP_WIDTH
# How long a page is left to finish its entrance before a still is taken. A
# guess, unmeasured.
SETTLE_MS = 4000

# Every animation to time t; one that refuses the seek stays where it is, so the
# rest still move.
SEEK_JS = "(t) => document.getAnimations().forEach((a) => { try { a.currentTime = t; } catch (e) {} })"
# Every animation paused, then moved 1 ms and drawn: a pause that lands where
# the first seek goes makes that seek no change, and the compositor keeps its
# own frame of a fade unless a frame is drawn before the seek.
PAUSE_JS = """
async () => {
  document.getAnimations().forEach((a) => {
    a.pause();
    try { a.currentTime = (a.currentTime || 0) + 1; } catch (e) {}
  });
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
}
"""

# The part under a point, and the font and colour it is drawn in.
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
    try:
        out = [float(n) for n in value.split(",")]
    except ValueError:
        out = []
    if len(out) != count:
        p.error(f"{flag} wants {count} numbers joined by commas — got {value!r}")
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
            help="default: check-layout.py's first screen at --width",
        )
        pages[name] = s
    pages["zoom"].add_argument("--clip", required=True)
    # Guesses, unmeasured: 4x shows a joint a 1x shot hides, and 50 ms steps to
    # 2500 ms cover vault.length's 1.6 s of motion after a short wait.
    pages["zoom"].add_argument("--scale", type=int, default=4)
    pages["zoom"].add_argument("--out", required=True)
    pages["scrub"].add_argument("--out", required=True)
    pages["scrub"].add_argument("--step", type=int, default=50)
    pages["scrub"].add_argument("--until", type=int, default=2500)
    pages["measure"].add_argument("--at", required=True)
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
    for flag, least in (("scale", 1), ("step", 1), ("until", 0)):
        if getattr(args, flag, least) < least:
            p.error(f"--{flag} wants {least} or more")
    if args.height is None:
        args.height = layout.height_at(args.width, layout.HEIGHTS)
    args.url = flow.page_url(p, args.page)
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
    page.set_default_timeout(flow.LOAD_TIMEOUT_MS)
    page.goto(args.url, wait_until="load")
    page.evaluate("document.fonts.ready")
    return page


def zoom(browser, args):
    page = settled_page(browser, args, args.scale)
    page.wait_for_timeout(SETTLE_MS)
    x, y, w, h = args.clip
    page.screenshot(
        path=args.out, clip={"x": x, "y": y, "width": w, "height": h}, full_page=True
    )
    return f"wrote {args.out}: {w:g}x{h:g} CSS px at {args.scale}x, from a {args.width}x{args.height} screen"


def scrub(browser, args):
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    page = settled_page(browser, args)
    page.evaluate(PAUSE_JS)
    n = 0
    for t in range(0, args.until + 1, args.step):
        page.evaluate(SEEK_JS, t)
        page.screenshot(path=str(out / f"t{t:05d}.png"))
        n += 1
    return f"wrote {n} frame(s) to {out}, every {args.step} ms to {args.until} ms, at {args.width}x{args.height}"


def measure(browser, args):
    page = settled_page(browser, args)
    page.wait_for_timeout(SETTLE_MS)
    found = page.evaluate(MEASURE_JS, args.at)
    if found is None:
        return f"nothing is drawn at {args.at[0]:g},{args.at[1]:g}"
    return json.dumps(found, indent=1)


def pixels(args):
    try:
        from PIL import Image
    except ImportError as err:
        return flow.missing(err)
    import numpy as np  # loaded, guarded, with access-pixels.py

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
    ratio = float(maths.contrast(*colours))
    print(f"{maths.hexed(colours[0])} against {maths.hexed(colours[1])}: {ratio:.2f}:1")
    return 0


def main(argv):
    args = parse(argv)
    if args.cmd == "pixels":
        return pixels(args)
    work = {"zoom": zoom, "scrub": scrub, "measure": measure}[args.cmd]

    def run():
        with flow.chromium() as browser:
            return work(browser, args)

    said, code = flow.run_browser(run, flow.LOAD_TIMEOUT_MS, url=args.url)
    if code:
        return code
    print(said)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
