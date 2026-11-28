#!/usr/bin/env python3
"""check-overlay.py — measures how far a candidate's mark strays from its source,
answering the trace half of gate question vault.curves-script.

USAGE
  python3 check-overlay.py <mark> <source> [--size WxH] [--scale N] [--out DIR]
        [--timeout MS]

Draws the candidate's mark and the source asset into one box at the source's
size, in Chromium at --scale times that size, and finds each one's edge: where
its ink meets its ground. Where both are see-through, ink is opacity; where
either is opaque, both are laid on that one's top-left colour and ink is
difference from it, so a white hole in a transparent mark matches the same
hole in a source on white. It then reports the largest
offset between the two edges, in the source's px, either way: a source edge
with no candidate edge near it, or a candidate edge with none of the source's.
Over 0.5 px fails against a raster source, and over 0.1 px against an SVG
source.

The source's size is its pixel size, or an SVG's width and height, or else its
viewBox; --size draws both at another. The mark is fitted to that box as an
<img> fits it: an SVG by its viewBox, centred, and a raster stretched. So a
mark framed differently from its source fails, and the report gives both ink
boxes to show it. --scale defaults to 8, or 4 for a source over 512 px; one
over 1024 px is refused (draw both smaller with --size). Each edge is placed
between pixels by its coverage, and the offset reads a little high: up to
0.05 px at 8x and 0.08 px at 4x. Only the outline against the ground is
compared: an edge between two of the mark's own colours is not.

It prints no overlap ratio.
With --out it writes DIR/overlay.png at the measured scale: both ink grey, the
source's alone red, the mark's alone blue.

EXITS 0 within the limit / 1 over it / 2 the arguments are wrong / 3 Playwright,
its browser, numpy, Pillow or scipy is missing / 4 the browser timed out / 5 the
browser could not draw a file / 6 a file draws no ink / 7 a call hung that would
never return. Exits 0, 1 and 6 are results and print on stdout; the rest
print on stderr.
An exception it does not handle exits 2, its traceback on stderr.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import crash_exit  # noqa: E402

crash_exit.guard(__name__)

import argparse  # noqa: E402
import base64  # noqa: E402
import io  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import xml.etree.ElementTree as ET  # noqa: E402

import siblings  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from scipy.ndimage import maximum_filter  # noqa: E402
from scipy.spatial import cKDTree  # noqa: E402

runner = siblings.load(HERE, "runner.py")
conditions = siblings.load(HERE, "conditions.py")
first_line, PageTimeoutError, RefusedError = (
    runner.first_line,
    runner.PageTimeoutError,
    runner.RefusedError,
)

LIMITS = {
    True: (0.1, "an SVG"),
    False: (0.5, "a raster"),
}  # measured 0.08 px read error at 4x; potrace's 0.5 px, #195
RASTER_TAGS = {"image", "feImage", "foreignObject"}
MAX_SCALE, MIN_SCALE = 8, 4  # measured 0.05 px high at 8x, 0.30 at 1x, #73
MAX_SIDE = 4096  # guess, #501
NEAR = 2  # guess, #501
FLOOR = 0.1  # guess, #501
SHOTS = 2  # guess, #136
UNCAPTURED = "Unable to capture screenshot"


def px(value):
    m = re.fullmatch(
        r"\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*(px)?\s*", value or ""
    )
    return float(m.group(1)) if m else None


def read(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if path.lower().endswith(".svg"):
        try:
            root = ET.fromstring(data)
        except ET.ParseError as exc:
            raise ValueError(f"{path} is not well-formed XML: {exc}") from exc
        box = None
        if root.get("viewBox"):
            box = [float(n) for n in re.split(r"[\s,]+", root.get("viewBox").strip())]
            if len(box) != 4 or box[2] <= 0 or box[3] <= 0:
                raise ValueError(
                    f"{path} has a viewBox that is not four numbers with a positive size"
                )
        w, h = px(root.get("width")), px(root.get("height"))
        size = (w, h) if w and h else (box[2], box[3]) if box else None
        if not size:
            raise ValueError(
                f"{path} has neither a viewBox nor a width and height in px"
            )
        return {
            "path": path,
            "data": data,
            "mime": "image/svg+xml",
            "size": size,
            "viewbox": box is not None,
            "vector": not any(
                e.tag.rpartition("}")[2] in RASTER_TAGS for e in root.iter()
            ),
        }
    try:
        image = Image.open(io.BytesIO(data))
    except OSError as exc:
        raise ValueError(
            f"{path} is neither an SVG nor an image Pillow reads: {exc}"
        ) from exc
    mime = Image.MIME.get(image.format)
    if mime not in ("image/png", "image/jpeg", "image/webp", "image/gif"):
        raise ValueError(
            f"{path} is a {image.format}, which a browser may not draw: give a PNG, JPEG, WebP or SVG"
        )
    return {
        "path": path,
        "data": data,
        "mime": mime,
        "size": image.size,
        "viewbox": True,
        "vector": False,
    }


def draw(page, f, box):
    from playwright.sync_api import Error as PlaywrightError

    src = f"data:{f['mime']};base64,{base64.b64encode(f['data']).decode()}"
    page.set_content(
        '<body style="margin:0;background:transparent">'
        f'<img style="display:block;width:{box[0]}px;height:{box[1]}px" src="{src}"></body>'
    )
    page.evaluate("document.images[0].decode()")
    for shot in range(1, SHOTS + 1):
        try:
            png = page.screenshot(omit_background=True)
            break
        except PlaywrightError as exc:
            if UNCAPTURED not in str(exc) or shot == SHOTS:
                raise
    return np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"))


def ink(drawn, scale):
    clear = {role: (rgba[..., 3] < 255).any() for role, rgba in drawn.items()}
    out = {}
    for role, rgba in drawn.items():
        if all(clear.values()):
            v = rgba[..., 3].astype(np.float32)
        else:
            ground = drawn["source" if not clear["source"] else "mark"][
                0, 0, :3
            ].astype(np.float32)
            a = rgba[..., 3:].astype(np.float32) / 255
            v = np.abs(rgba[..., :3] * a + ground * (1 - a) - ground).max(-1)
        top = v.max()
        if top == 0:
            out[role] = None
            continue
        near = maximum_filter(v, size=NEAR * scale + 1)
        out[role] = np.where(near >= FLOOR * top, v / np.maximum(near, 1e-6), 0)
    return out


def edge(cov):
    c = np.pad(cov, 1)
    points = []
    for c0, c1, step in ((c[:, :-1], c[:, 1:], (1, 0)), (c[:-1, :], c[1:, :], (0, 1))):
        ys, xs = np.nonzero((c0 >= 0.5) != (c1 >= 0.5))
        t = (0.5 - c0[ys, xs]) / (c1[ys, xs] - c0[ys, xs])
        points.append(np.column_stack([xs + step[0] * t, ys + step[1] * t]) - 0.5)
    return np.concatenate(points)


def stray(a, b):
    d, i = cKDTree(b).query(a, k=2)
    p, q = b[i[:, 0]], b[i[:, 1]]
    pq = q - p
    run = (pq**2).sum(1)
    t = np.clip(((a - p) * pq).sum(1) / np.maximum(run, 1e-12), 0, 1)
    seg = np.hypot(*(p + t[:, None] * pq - a).T)
    return np.where(run <= 2.01, np.minimum(seg, d[:, 0]), d[:, 0])


def ink_box(cov, scale):
    ys, xs = np.nonzero(cov >= 0.5)
    return [
        xs.min() / scale,
        ys.min() / scale,
        (xs.max() + 1 - xs.min()) / scale,
        (ys.max() + 1 - ys.min()) / scale,
    ]


def measure(mark, source, scale, limit):
    source_edge, mark_edge = edge(source), edge(mark)
    source_off = stray(source_edge, mark_edge) / scale
    mark_off = stray(mark_edge, source_edge) / scale
    i, j = int(source_off.argmax()), int(mark_off.argmax())
    if source_off[i] >= mark_off[j]:
        side, offset, at = "source", source_off[i], source_edge[i]
    else:
        side, offset, at = "mark", mark_off[j], mark_edge[j]
    return {
        "offset": float(offset),
        "side": side,
        "at": ((at + 0.5) / scale).tolist(),
        "source_over": float((source_off > limit).mean()),
        "mark_over": float((mark_off > limit).mean()),
    }


def overlay(mark, source):
    # guess, #501
    mark, source = mark >= 0.5, source >= 0.5
    out = np.full(mark.shape + (3,), 255, np.uint8)
    out[source & ~mark] = (220, 30, 30)
    out[mark & ~source] = (30, 80, 220)
    out[mark & source] = (110, 110, 110)
    return Image.fromarray(out)


def parse(argv):
    p = argparse.ArgumentParser(
        prog="check-overlay.py",
        description="Measure the largest edge offset between a mark and its source.",
    )
    p.add_argument("mark", help="the candidate's mark: an SVG, PNG, JPEG or WebP")
    p.add_argument("source", help="the source asset it must match")
    p.add_argument(
        "--size",
        metavar="WxH",
        help="draw both at this size in px, not the source's own",
    )
    p.add_argument(
        "--scale",
        type=int,
        metavar="N",
        help=f"device scale; default {MAX_SCALE}, less for a big source",
    )
    p.add_argument("--out", metavar="DIR", help="write overlay.png here")
    p.add_argument("--timeout", type=int, default=runner.LOAD_TIMEOUT_MS, metavar="MS")
    at = p.parse_args(argv)
    try:
        at.files = {"mark": read(at.mark), "source": read(at.source)}
    except (OSError, ValueError) as exc:
        p.error(str(exc))
    at.box = at.files["source"]["size"]
    at.limit, at.source_kind = LIMITS[at.files["source"]["vector"]]
    if at.size:
        size = conditions.size_arg(p, "--size", at.size, number=float, example="120x80")
        w, h = size["width"], size["height"]
        if not (0 < w < math.inf and 0 < h < math.inf):
            p.error(f"--size wants a positive width and height — got {at.size!r}")
        at.box = (w, h)
    for role, f in at.files.items():
        if not f["viewbox"] and tuple(f["size"]) != tuple(at.box):
            p.error(
                f"the {role} is an SVG with no viewBox, so it cannot be drawn at {at.box[0]:g}x{at.box[1]:g}: "
                f'add viewBox="0 0 {f["size"][0]:g} {f["size"][1]:g}"'
            )
    if at.scale is None:
        at.scale = min(MAX_SCALE, int(MAX_SIDE // max(at.box)))
    if at.scale < MIN_SCALE:
        p.error(
            f"a scale under {MIN_SCALE} reads the offset up to 0.3 px high: at {at.box[0]:g}x{at.box[1]:g} px "
            f"the scale is {at.scale}; pass --size to draw both no longer than {MAX_SIDE // MIN_SCALE} px"
        )
    if at.scale * max(at.box) > MAX_SIDE:
        p.error(
            f"--scale {at.scale} draws {at.scale * max(at.box):g} px, over {MAX_SIDE}: pass a lower --scale or --size"
        )
    return at


def run(at):
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import TimeoutError as PlaywrightTimeout

    with runner.chromium() as browser:
        context = browser.new_context(
            viewport={"width": math.ceil(at.box[0]), "height": math.ceil(at.box[1])},
            device_scale_factor=at.scale,
        )
        context.set_default_timeout(at.timeout)
        page = context.new_page()
        drawn = {}
        for role, f in at.files.items():
            try:
                drawn[role] = draw(page, f, at.box)
            except PlaywrightTimeout as exc:
                raise PageTimeoutError(first_line(exc)) from exc
            except PlaywrightError as exc:
                raise RefusedError(f"{f['path']}: {first_line(exc)}") from exc
        return drawn


def report(at, masks, m):
    w, h = at.box
    lines = [
        f"check-overlay: {at.mark} against {at.source}, at {w:g}x{h:g} px, measured at {at.scale}x"
    ]
    ar = [f["size"][0] / f["size"][1] for f in (at.files["mark"], at.files["source"])]
    # guess, #501
    if abs(ar[0] - ar[1]) > 1e-3 * ar[1]:
        lines.append(
            f"the mark's aspect ratio is {ar[0]:.4g} and the source's {ar[1]:.4g}, so the mark is fitted inside the box"
        )
    verdict = "FAIL" if m["offset"] > at.limit else "PASS"
    where = "the edges coincide"
    if m["offset"] > 0:
        where = (
            f"{'a source' if m['side'] == 'source' else 'a mark'} edge lies that far from the other's nearest, "
            f"at ({m['at'][0]:.2f}, {m['at'][1]:.2f}) px"
        )
    lines.append(
        f"largest edge offset: {m['offset']:.3f} px ({verdict}, the limit is {at.limit} px against {at.source_kind} source): {where}"
    )
    lines.append(
        f"edge over {at.limit} px away: {m['source_over']:.1%} of the source's, {m['mark_over']:.1%} of the mark's"
    )
    if verdict == "FAIL":
        boxes = {
            r: ", ".join(f"{n:.2f}" for n in ink_box(masks[r], at.scale))
            for r in ("source", "mark")
        }
        lines.append(
            f"ink boxes (x, y, w, h): source {boxes['source']}; mark {boxes['mark']}"
        )
    if at.out:
        lines.append(
            f"overlay: {os.path.join(at.out, 'overlay.png')} (both grey, the source alone red, the mark alone blue)"
        )
    return "\n".join(lines)


def main(argv):
    at = parse(argv)
    drawn, code = runner.run_browser(lambda: run(at), at.timeout)
    if code:
        return code
    masks = ink(drawn, at.scale)
    blank = [at.files[role]["path"] for role, mask in masks.items() if mask is None]
    if blank:
        print(
            f"cannot measure: {' and '.join(blank)} draw{'s' if len(blank) == 1 else ''} no ink at {at.box[0]:g}x{at.box[1]:g} px"
        )
        return 6
    m = measure(masks["mark"], masks["source"], at.scale, at.limit)
    if at.out:
        os.makedirs(at.out, exist_ok=True)
        overlay(masks["mark"], masks["source"]).save(
            os.path.join(at.out, "overlay.png")
        )
    print(report(at, masks, m))
    return 1 if m["offset"] > at.limit else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
