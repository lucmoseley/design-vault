#!/usr/bin/env python3
"""contact-sheet.py — one view of a whole motion candidate: its frames every
0.25 s, tiled and labelled, at desktop and phone size
(lucmoseley/mmm-infra#28, design-vault#71).

USAGE
  python3 contact-sheet.py <url or file> --out DIR [--step MS] [--desktop WxH]
        [--phone WxH] [--wait SEL] [--timeout MS]

At each size it loads the page, seeks its timeline from time zero to the build's
end every --step ms (250 by default), and the end itself where the steps miss
it, and screenshots the viewport at each. It then tiles those frames in order
into one sheet, each labelled with its time in seconds, the last marked `end`.
The timeline is read and seeked as check-frames.py reads and seeks it: the Web
Animations API animations the page has made once it has loaded, its fonts are
ready, --wait has matched and none has started for check-frames.py's QUIET_MS.
Time zero is the earliest animation's start. A build that starts animations
when others finish is refused, as check-frames.py refuses it.

The phone size is a viewport width only: no touch, no mobile user agent, device
scale 1. It writes DIR/sheet-desktop.png and DIR/sheet-phone.png, drawn at
device scale 2 so a desktop tile keeps half its frame's pixels and a phone tile
nearly all, each frame at full size
as DIR/<size>/frame-<ms>.png, and DIR/sheet.json naming every tile's time,
label and box in its sheet's pixels.

EXITS 0 the sheets are written / 2 the arguments are wrong / 3 Playwright or its
browser is missing / 4 the page did not render in time / 5 the browser refused
the page / 6 the page has no timeline a seek can reach / 7 a call hung that would
never return. Exits 0 and 6 print on stdout; the rest print on stderr.
"""

import argparse
import base64
import html
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "check_frames", os.path.join(HERE, "check-frames.py")
)
frames = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(frames)
flow = frames.flow
_spec = importlib.util.spec_from_file_location(
    "check_layout", os.path.join(HERE, "check-layout.py")
)
layout = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(layout)
UnmeasurableError = flow.UnmeasurableError

# A tile's width in CSS px, by size, and the sheet's width it wraps at. A first
# guess: a quarter of a desktop frame, near half of a phone's.
TILE = {"desktop": 320, "phone": 180}
SHEET_WIDTH = 1680
# The space between tiles and around the sheet: one line of its 13 px captions
# and a little more, so neighbouring frames read as separate.
GAP = PAD = 16
SHEET_SCALE = 2

# The sheet's type sizes, margins and outline: picked by eye.
SHEET_CSS = f"""
body {{ margin: 0; padding: {PAD}px; background: #fff; color: #111; font: 13px/1.3 system-ui, sans-serif; }}
h1 {{ margin: 0 0 12px; font-size: 14px; font-weight: 600; }}
.grid {{ display: grid; gap: {GAP}px; }}
figure {{ margin: 0; }}
img {{ display: block; width: 100%; outline: 1px solid #bbb; }}
figcaption {{ padding-top: 4px; font-variant-numeric: tabular-nums; }}
"""


def times(end, step):
    """Every step from 0 to the end, and the end itself: a step under 1 ms (a
    guess) short of the end moves onto it, so the last frame is always the end's."""
    out = [float(n * step) for n in range(int(end // step) + 1)]
    if end - out[-1] >= 1:
        out.append(round(end, 3))
    else:
        out[-1] = round(end, 3)
    return out


def labels(ts):
    return [
        f"{t / 1000:.2f} s" + (" (end)" if i == len(ts) - 1 else "")
        for i, t in enumerate(ts)
    ]


def sheet_html(title, shots, columns, width):
    tiles = "".join(
        f'<figure><img src="data:image/png;base64,{base64.b64encode(png).decode()}">'
        f"<figcaption>{html.escape(text)}</figcaption></figure>"
        for text, png in shots
    )
    return (
        f"<!doctype html><meta charset=utf-8><style>{SHEET_CSS}</style>"
        f"<h1>{html.escape(title)}</h1>"
        f'<div class="grid" style="grid-template-columns: repeat({columns}, {width}px)">{tiles}</div>'
    )


# Every tile's image box, in CSS px from the page's top left.
BOXES_JS = r"""
() => [...document.querySelectorAll('figure img')].map((img) => {
  const r = img.getBoundingClientRect();
  return { x: r.left, y: r.top, width: r.width, height: r.height };
})
"""


def shoot(browser, at, viewport):
    """The size's frames, as (ms, PNG) in time order, and the build's end."""
    at = frames.args_with(at, viewport_size=viewport)
    context, page, prep = frames.open_page(browser, at, 1)
    try:
        if prep["end"] <= 0:
            raise UnmeasurableError(
                [
                    "makes no Web Animations API animation that runs for any time, so it has no timeline to seek"
                ]
            )
        shots = []
        for t in times(prep["end"], at.step):
            frames.seek(page, t)
            shots.append((t, page.screenshot()))
        frames.refuse_chain(page)
        return shots, prep["end"]
    finally:
        context.close()


def tile(browser, at, size, viewport, *, shots, end):
    width = TILE[size]
    columns = max(1, min(len(shots), (SHEET_WIDTH + GAP) // (width + GAP)))
    title = (
        f"{at.url} — {size} {viewport['width']}x{viewport['height']}, "
        f"a frame every {frames.ms(at.step)} ms to the end at {frames.ms(end)} ms"
    )
    names = labels([t for t, _ in shots])
    doc = sheet_html(
        title,
        [(name, png) for name, (_, png) in zip(names, shots, strict=True)],
        columns,
        width,
    )
    context = browser.new_context(
        # Any height: the shot takes the full page.
        viewport={"width": columns * (width + GAP) - GAP + 2 * PAD, "height": 200},
        device_scale_factor=SHEET_SCALE,
    )
    try:
        page = context.new_page()
        page.set_content(doc, wait_until="load")
        boxes = page.evaluate(BOXES_JS)
        sheet = page.screenshot(full_page=True)
    finally:
        context.close()
    return sheet, [
        {"ms": t, "label": name, **{k: round(v * SHEET_SCALE) for k, v in box.items()}}
        for (t, _), name, box in zip(shots, names, boxes, strict=True)
    ]


def run(at):
    # Seeked as check-frames.py's hash is, on the main thread.
    with flow.chromium(frames.HASH_ARGS) as browser:
        record = {"page": at.url, "step_ms": at.step, "sheets": {}}
        for size, viewport in (("desktop", at.desktop), ("phone", at.phone)):
            shots, end = shoot(browser, at, viewport)
            folder = os.path.join(at.out, size)
            os.makedirs(folder, exist_ok=True)
            for t, png in shots:
                with open(
                    os.path.join(folder, f"frame-{frames.ms(t)}.png"), "wb"
                ) as fh:
                    fh.write(png)
            sheet, tiles = tile(browser, at, size, viewport, shots=shots, end=end)
            path = os.path.join(at.out, f"sheet-{size}.png")
            with open(path, "wb") as fh:
                fh.write(sheet)
            record["sheets"][size] = {
                "file": path,
                "viewport": viewport,
                "end_ms": end,
                "scale": SHEET_SCALE,
                "tiles": tiles,
            }
        with open(os.path.join(at.out, "sheet.json"), "w", encoding="utf8") as fh:
            json.dump(record, fh, indent=1)
            fh.write("\n")
        return record


def report(at, record):
    lines = [f"contact-sheet: {at.url}"]
    for size, s in record["sheets"].items():
        lines.append(
            f"  {size} {s['viewport']['width']}x{s['viewport']['height']}: {len(s['tiles'])} frames, "
            f"0 to {frames.ms(s['end_ms'])} ms every {frames.ms(at.step)} ms — {s['file']}"
        )
    lines.append(f"tiles listed in {os.path.join(at.out, 'sheet.json')}")
    return "\n".join(lines)


def parse(argv):
    p = argparse.ArgumentParser(
        prog="contact-sheet.py",
        description="Tile a motion candidate's frames, labelled with their times, at desktop and phone size.",
    )
    p.add_argument("url", help="an http(s) URL, or a local HTML file")
    p.add_argument(
        "--out", required=True, metavar="DIR", help="where the sheets and frames go"
    )
    p.add_argument(
        "--step",
        type=float,
        default=250,
        metavar="MS",
        help="time between frames; 250, as cth9191/animate's review sheets (mmm-infra#28)",
    )
    p.add_argument("--desktop", default=flow.DESKTOP, metavar="WxH")
    p.add_argument(
        "--phone",
        default=f"{layout.PHONE_WIDTH}x{layout.HEIGHTS[0]}",
        metavar="WxH",
        help="check-layout.py's phone first screen by default, Safari's on a 390x844 iPhone",
    )
    p.add_argument("--wait", metavar="SELECTOR")
    p.add_argument("--timeout", type=int, default=flow.PLAY_TIMEOUT_MS, metavar="MS")
    at = p.parse_args(argv)
    if at.step < 1:
        p.error("--step wants at least 1 ms")
    at.desktop, at.phone = (
        flow.size_arg(p, "--desktop", at.desktop),
        flow.size_arg(p, "--phone", at.phone),
    )
    at.url = flow.page_url(p, at.url)
    return at


def main(argv):
    at = parse(argv)
    os.makedirs(at.out, exist_ok=True)
    record, code = flow.run_browser(
        lambda: run(at),
        at.timeout,
        at.url,
        (
            f"cannot sheet {at.url}, because this page:",
            "Record it playing instead, or seek it to each frame by hand.",
        ),
    )
    if code:
        return code
    print(report(at, record))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
