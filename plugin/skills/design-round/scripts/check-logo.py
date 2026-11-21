#!/usr/bin/env python3
"""check-logo.py — compares a placed client logo with the client's logo file
(design-vault#324), answering gate questions vault.logo-unchanged and
vault.logo-ground-script (design-vault#330). It exists because a recolour of
about 1 ΔE00 gets past an eye and past pixelmatch and looks-same at their
defaults, and palette.py never reads the ground a logo was rendered on (#262).

USAGE
  python3 check-logo.py --logo <logo file> <page> --at SELECTOR
        [--scale N] [--viewport WxH] [--wait SEL] [--timeout MS] [--out DIR]
  python3 check-logo.py --logo <logo file> <image> --box X,Y,W,H [--out DIR]

The logo file is the client's lockup the project's rules file names, an SVG or a
raster with a transparent ground. On a page, --at names the one element the
logo fills, drawn at --scale device pixels per CSS pixel; on an artboard image,
a lossless export, --box gives the logo's box in its pixels. An SVG logo is
drawn by Playwright's Chromium at the placed size, a raster one resampled to it
by Pillow's Lanczos filter.

Unchanged (vault.logo-unchanged): every placed pixel at least the edge band
inside the resampled logo's alpha edges and its colour edges (neighbours
SAME_COLOUR_DE00 or more apart) is within CHANNEL_STEP of the resampled file on
each channel and under SAME_COLOUR_DE00 from it. Each pixel past it is a fault; the worst is printed with its ΔE00.

Ground (vault.logo-ground-script): the file's colours that border its
transparent areas, read at its own resolution, are each held to GROUND_RATIO
against all the rendered ground: the box's pixels where the file is clear, and
a ring outside the box, both past the edge band.

A translucent part of the logo, under full alpha, is never compared and never
judged against its ground. An embedded ICC profile is not read: Chromium applies
it on a page and Pillow does not, so a profiled raster can fail against itself.

A logo file with no transparent pixel is refused: its own ground would be
compared as logo. palette.py keeps the check on declared colours.

--out DIR writes expected.png (the resampled logo), unchanged.png and
ground.png (the placed region, faults in red).

EXITS 0 both pass / 1 a check fails / 2 the arguments are wrong, a file cannot
be read, or the logo file is refused / 3 Pillow, or Playwright or its browser
where one is needed, is missing / 4 the page did not render in time / 5 the
browser refused the page / 6 nothing fails but a check cannot be judged / 7 a
call hung that would never return. Exits 0, 1 and 6 are results and print on
stdout; the rest print on stderr.
"""

import argparse
import base64
import importlib.util
import math
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REQUIREMENTS = HERE.parents[2] / "requirements.txt"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


flow = _load("check_flow", HERE / "check-flow.py")
colour_space = _load(
    "colour_space",
    HERE.parent.parent / "design-project" / "scripts" / "colour_space.py",
)

# A placed pixel is unchanged within one 8-bit step a resample rounds to on each
# channel. No ΔE00 line can stand in: one step reaches 1.22 ΔE00 at #191919,
# more than the 1.03 of the smallest recolour #262 found two diff tools miss,
# and brand guidelines fix a logo's colours exactly (vault.logo-colour's
# sources). Measured: colour_space.de2000 over a ±1 step at every 5th sRGB value.
# A step on all three channels at once reaches 2.34 ΔE00 there, so a pixel must
# also lie under SAME_COLOUR_DE00.
CHANNEL_STEP = 1
# Two colours under this are one colour (W3C CSS Color 4 §14.2.1, as
# design-critique's brand-palette.md cites it): neighbours this far apart make
# a colour edge, and the ground check takes the logo's colours this far apart.
SAME_COLOUR_DE00 = 2
# WCAG 2.2 SC 1.4.11's level for graphical objects, borrowed for a logo on its
# ground, as brand-palette.md cites it; WCAG's Understanding docs take a
# background image at its point of least contrast, so every ground pixel counts.
GROUND_RATIO = 3
# The edge band, in device pixels. Pillow's LANCZOS is Lanczos-3, a support of
# 3 source pixels, so a resampled edge spreads over 3 pixels times the scale
# when enlarged and 3 when reduced; a vector edge's anti-aliasing shades the
# one pixel it crosses. Placing the logo off the pixel grid moves an edge under
# one more. Untraced: no source measures how far a browser's own filter spreads.
LANCZOS_SUPPORT = 3
ANTIALIAS_PX = 1
OFFSET_PX = 1
# The ring of ground read outside the box, past the edge band. Untraced.
RING_PX = 4
# A logo colour meets the ground where an alpha-0 pixel lies this near. Untraced.
BORDER_REACH_PX = 2
# A colour making less of that border than this, and lying on the mix of two
# colours that make more, is the blend where they meet at the outline, not a
# colour of the logo. Untraced.
MIN_SHARE = 0.02
# How far, on each channel, a blend may sit off the straight mix. Untraced.
BLEND_STEPS = 2
# An SVG's own resolution is its placed size times this. Untraced.
SVG_READ_SCALE = 4
# The default device scale on a page: a 2x screen draws the logo at twice its
# CSS size, so more of it lies past the edge band. Untraced.
PAGE_SCALE = 2
# An SVG's root opens within its prolog, which this head of the file covers. Untraced.
SNIFF_BYTES = 512

PASS, FAIL, UNJUDGED = "PASS", "FAIL", "NOT JUDGED"
FAULT_RED = (255, 0, 0)

# An animation that never ends throws on finish() (Web Animations 1 §4.4.12),
# and is counted, so the logo is never read mid-motion unsaid.
FINISH_JS = """async () => {
  await document.fonts.ready;
  let endless = 0;
  for (const a of document.getAnimations()) { try { a.finish(); } catch (e) { endless++; } }
  return endless;
}"""
RECT_JS = """(el) => {
  const r = el.getBoundingClientRect();
  return { x: r.left + scrollX, y: r.top + scrollY, width: r.width, height: r.height };
}"""


class RefusedLogoError(Exception):
    pass


class UsageError(Exception):
    pass


def hexof(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb[:3])


class Colours:
    """ΔE00 and contrast by colour, each colour's CIELAB worked out once."""

    def __init__(self):
        self.labs = {}

    def lab(self, rgb):
        if rgb not in self.labs:
            self.labs[rgb] = colour_space.lab(hexof(rgb))
        return self.labs[rgb]

    def de(self, a, b):
        return 0.0 if a == b else colour_space.de2000(self.lab(a), self.lab(b))

    def ratio(self, a, b):
        return colour_space.contrast(hexof(a), hexof(b))


def read_logo(path):
    """("svg", text) or ("raster", an RGBA image)."""
    from PIL import Image

    try:
        data = pathlib.Path(path).read_bytes()
    except OSError as err:
        raise UsageError(f"cannot read {path}: {err.strerror}") from err
    head = data[:SNIFF_BYTES].lstrip().lower()
    if path.lower().endswith(".svg") or head.startswith((b"<svg", b"<?xml")):
        return "svg", data.decode("utf8", "replace")
    try:
        with Image.open(path) as image:
            return "raster", image.convert("RGBA")
    except OSError as err:
        raise UsageError(f"cannot read {path}: {err}") from err


def refuse_opaque(image, path):
    if image.getchannel("A").getextrema()[0] > 0:
        raise RefusedLogoError(
            f"{path} has no transparent pixel, so its own ground would be compared as "
            "logo: supply the version with a transparent ground"
        )


def render_svg(browser, text, size, scale):
    """The SVG drawn by Chromium into a box of `size` device pixels at `scale`."""
    from PIL import Image
    import io

    w, h = size
    page = browser.new_page(
        viewport={
            # One spare CSS pixel, so the clip never runs past the viewport.
            "width": math.ceil(w / scale) + 1,
            "height": math.ceil(h / scale) + 1,
        },
        device_scale_factor=scale,
    )
    try:
        src = "data:image/svg+xml;base64," + base64.b64encode(text.encode()).decode()
        page.set_content(
            "<html><body style='margin:0;background:transparent'>"
            f"<img src='{src}' style='display:block;width:{w / scale}px;height:{h / scale}px'>"
            "</body></html>"
        )
        page.evaluate("document.querySelector('img').decode()")
        png = page.screenshot(
            clip={"x": 0, "y": 0, "width": w / scale, "height": h / scale},
            omit_background=True,
        )
    finally:
        page.close()
    image = Image.open(io.BytesIO(png)).convert("RGBA")
    return image if image.size == size else image.resize(size, Image.LANCZOS)


def band_px(kind, source_size, box_size):
    if kind == "svg":
        return ANTIALIAS_PX + OFFSET_PX
    scale = max(b / s for b, s in zip(box_size, source_size, strict=True))
    return math.ceil(LANCZOS_SUPPORT * max(1.0, scale)) + OFFSET_PX


def dilate(mask, size, reach):
    """The pixels within `reach` (Chebyshev) of a set pixel in a flat 0/1 list."""
    from PIL import Image, ImageFilter

    if reach <= 0:
        return list(mask)
    image = Image.new("L", size)
    image.putdata([255 if m else 0 for m in mask])
    grown = image.filter(ImageFilter.MaxFilter(2 * reach + 1))
    return [v > 0 for v in grown.get_flattened_data()]


def neighbours(i, width, height):
    x, y = i % width, i // width
    if x:
        yield i - 1
    if x < width - 1:
        yield i + 1
    if y:
        yield i - width
    if y < height - 1:
        yield i + width


def check_unchanged(grid, colours, out_marks):
    """(verdict, detail). Compares the logo's opaque pixels past the edge band,
    adding each fault to the caller's `out_marks`."""
    w, h, band = grid["w"], grid["h"], grid["band"]
    alpha, logo, placed = grid["alpha"], grid["logo"], grid["placed"]
    edge = [a < 255 for a in alpha]
    for i, a in enumerate(alpha):
        if a == 255 and not edge[i]:
            for j in neighbours(i, w, h):
                if alpha[j] == 255 and colours.de(logo[i], logo[j]) >= SAME_COLOUR_DE00:
                    edge[i] = True
                    break
    near = dilate(edge, (w, h), band)
    compared = [
        i
        for i in range(w * h)
        if alpha[i] == 255 and not near[i] and placed[i] is not None
    ]
    if not compared:
        return UNJUDGED, (
            f"no logo pixel lies {band} px inside its edges at this size: check it by eye at 4× zoom"
        )
    faults = [
        i
        for i in compared
        if max(abs(p - q) for p, q in zip(placed[i], logo[i], strict=True))
        > CHANNEL_STEP
        or colours.de(placed[i], logo[i]) >= SAME_COLOUR_DE00
    ]
    if not faults:
        return (
            PASS,
            f"{len(compared)} pixels inside the {band} px edge band match the file",
        )
    worst = max(faults, key=lambda i: colours.de(placed[i], logo[i]))
    for i in faults:
        out_marks.add(i)
    x, y = grid["at"](worst)
    return FAIL, (
        f"{len(faults)} of {len(compared)} pixels differ from the file; worst at ({x},{y}): "
        f"{hexof(placed[worst])} where the file has {hexof(logo[worst])}, "
        f"ΔE00 {colours.de(placed[worst], logo[worst]):.2f}: place the logo file unchanged"
    )


def edge_colours(own, colours):
    """The logo file's colours that meet its transparent ground, as [(rgb, share)],
    and the blends set aside, as is_blend() finds them."""
    pixels = list(own.get_flattened_data())
    clear = [p[3] == 0 for p in pixels]
    near = dilate(clear, own.size, BORDER_REACH_PX)
    counts = {}
    for p, n in zip(pixels, near, strict=True):
        if n and p[3] == 255:
            counts[p[:3]] = counts.get(p[:3], 0) + 1
    total = sum(counts.values())
    groups = []
    for rgb, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        for g in groups:
            if colours.de(rgb, g[0]) < SAME_COLOUR_DE00:
                g[1] += n
                break
        else:
            groups.append([rgb, n])
    shares = [(rgb, n / total) for rgb, n in groups]
    main = [rgb for rgb, share in shares if share >= MIN_SHARE]
    blends = [
        (rgb, share)
        for rgb, share in shares
        if share < MIN_SHARE and is_blend(rgb, main)
    ]
    return [c for c in shares if c not in blends], blends


def is_blend(rgb, main):
    """Whether `rgb` lies within BLEND_STEPS of a straight mix of two of `main`."""
    for k, a in enumerate(main):
        for b in main[k + 1 :]:
            span = [q - p for p, q in zip(a, b, strict=True)]
            length = sum(d * d for d in span)
            t = sum((c - p) * d for c, p, d in zip(rgb, a, span, strict=True)) / length
            if 0 < t < 1 and all(
                abs(c - (p + t * d)) <= BLEND_STEPS
                for c, p, d in zip(rgb, a, span, strict=True)
            ):
                return True
    return False


def check_ground(grid, own, colours, out_marks):
    """(verdict, lines). Holds each edge colour of `own` to GROUND_RATIO against
    the ground pixels, adding each one under it to the caller's `out_marks`."""
    w, h, band = grid["w"], grid["h"], grid["band"]
    alpha, placed = grid["alpha"], grid["placed"]
    near = dilate([a > 0 for a in alpha], (w, h), band)
    ground = [
        i
        for i in range(w * h)
        if alpha[i] == 0 and not near[i] and placed[i] is not None
    ]
    edges, blends = edge_colours(own, colours)
    if not ground:
        return UNJUDGED, [
            f"no ground pixel lies {band} px clear of the logo: check it by eye"
        ]
    if not edges:
        return UNJUDGED, ["no opaque colour of the file meets its transparent ground"]
    seen = {}
    for i in ground:
        seen.setdefault(placed[i], []).append(i)
    lines, failed = [], False
    for rgb, share in edges:
        ratios = {g: colours.ratio(rgb, g) for g in seen}
        worst = min(ratios, key=ratios.get)
        under = [i for g, r in ratios.items() if r < GROUND_RATIO for i in seen[g]]
        head = f"{hexof(rgb)} ({share:.0%} of the logo's edge)"
        if not under:
            lines.append(
                f"{head} reaches {ratios[worst]:.2f}:1 at least, against {hexof(worst)}"
            )
            continue
        failed = True
        out_marks.update(under)
        x, y = grid["at"](seen[worst][0])
        lines.append(
            f"{head} reaches {ratios[worst]:.2f}:1 against {hexof(worst)} at ({x},{y}); "
            f"{len(under) / len(ground):.0%} of the ground is under {GROUND_RATIO}:1"
        )
    for rgb, share in blends:
        lines.append(
            f"{hexof(rgb)} ({share:.0%} of the logo's edge) set aside: under {MIN_SHARE:.0%}, "
            "and a blend where two logo colours meet"
        )
    if failed:
        lines.append("take another version of the logo, or another ground")
    return (FAIL if failed else PASS), lines


def build_grid(placed_image, box, logo_image, band):
    """The box and a ring RING_PX past the band, as flat lists: the logo's alpha
    and colour (alpha 0 outside the box), and the placed colour, None off the image."""
    bx, by, bw, bh = box
    pad = band + RING_PX
    w, h = bw + 2 * pad, bh + 2 * pad
    iw, ih = placed_image.size
    source = placed_image.load()
    drawn = logo_image.load()
    alpha, logo, placed = [0] * (w * h), [(0, 0, 0)] * (w * h), [None] * (w * h)
    for gy in range(h):
        for gx in range(w):
            i = gy * w + gx
            x, y = bx - pad + gx, by - pad + gy
            if 0 <= x < iw and 0 <= y < ih:
                placed[i] = source[x, y][:3]
            lx, ly = gx - pad, gy - pad
            if 0 <= lx < bw and 0 <= ly < bh:
                r, g, b, a = drawn[lx, ly]
                alpha[i], logo[i] = a, (r, g, b)
    return {
        "w": w,
        "h": h,
        "band": band,
        "alpha": alpha,
        "logo": logo,
        "placed": placed,
        "at": lambda i: (bx - pad + i % w, by - pad + i // w),
    }


def write_marks(grid, marks, path):
    from PIL import Image

    image = Image.new("RGB", (grid["w"], grid["h"]))
    image.putdata(
        [
            FAULT_RED if i in marks else (p or (0, 0, 0))
            for i, p in enumerate(grid["placed"])
        ]
    )
    image.save(path)


def parse_box(value):
    wrong = UsageError(
        f"--box wants X,Y,W,H in whole pixels, W and H above 0 — got {value!r}"
    )
    try:
        box = tuple(int(n) for n in value.split(","))
    except ValueError as error:
        raise wrong from error
    if len(box) != 4 or box[2] <= 0 or box[3] <= 0 or box[0] < 0 or box[1] < 0:
        raise wrong
    return box


def read_artboard(path, box):
    from PIL import Image

    try:
        with Image.open(path) as image:
            image.load()
            artboard = image.convert("RGBA")
    except OSError as err:
        raise UsageError(f"cannot read {path}: {err}") from err
    if image.format == "JPEG":
        raise UsageError(
            f"{path} is a JPEG, whose compression changes the logo's pixels: give a lossless export"
        )
    if artboard.getchannel("A").getextrema()[0] < 255:
        raise UsageError(f"{path} has transparent pixels: give its flattened export")
    x, y, w, h = box
    if x + w > artboard.width or y + h > artboard.height:
        raise UsageError(
            f"--box {x},{y},{w},{h} runs past {path}'s {artboard.width}x{artboard.height}"
        )
    return artboard.convert("RGB")


def read_page(browser, at):
    """The full page drawn at at.scale, and the --at element's box in its device pixels."""
    from PIL import Image
    import io

    context = browser.new_context(
        viewport=at.viewport_size, device_scale_factor=at.scale
    )
    context.set_default_timeout(at.timeout)
    try:
        page = context.new_page()
        page.goto(at.url, wait_until="load")
        if at.wait:
            page.wait_for_selector(at.wait)
        endless = page.evaluate(FINISH_JS)
        if endless:
            raise flow.UnmeasurableError(
                [
                    f"{endless} animation(s) never end, so the logo may be read mid-motion"
                ]
            )
        found = page.locator(at.at)
        if found.count() != 1:
            raise flow.UnmeasurableError(
                [f"--at {at.at} matches {found.count()} elements, not one"]
            )
        r = found.element_handle().evaluate(RECT_JS)
        png = page.screenshot(full_page=True)
    finally:
        context.close()
    s = at.scale
    box = (
        round(r["x"] * s),
        round(r["y"] * s),
        round((r["x"] + r["width"]) * s) - round(r["x"] * s),
        round((r["y"] + r["height"]) * s) - round(r["y"] * s),
    )
    if box[2] <= 0 or box[3] <= 0:
        raise flow.UnmeasurableError([f"--at {at.at} is not drawn: its box is empty"])
    return Image.open(io.BytesIO(png)).convert("RGB"), box


def drawn_logo(browser, kind, logo, size, *, scale):
    """The logo at the placed size, and at its own resolution."""
    from PIL import Image

    if kind == "svg":
        placed = render_svg(browser, logo, size, scale)
        own = render_svg(
            browser,
            logo,
            tuple(n * SVG_READ_SCALE for n in size),
            scale * SVG_READ_SCALE,
        )
        return placed, own
    return logo.resize(size, Image.LANCZOS), logo


def measure(at, kind, logo, browser):
    if at.box:
        placed_image, box = read_artboard(at.target, at.box), at.box
        scale = 1
    else:
        placed_image, box = read_page(browser, at)
        scale = at.scale
    size = box[2:]
    resampled, own = drawn_logo(browser, kind, logo, size, scale=scale)
    if kind == "svg":
        refuse_opaque(own, at.logo)
    band = band_px(kind, logo.size if kind == "raster" else size, size)
    if not at.box and (
        box[0] < 0
        or box[1] < 0
        or box[0] + box[2] > placed_image.width
        or box[1] + box[3] > placed_image.height
    ):
        raise flow.UnmeasurableError([f"--at {at.at} is drawn partly off the page"])
    grid = build_grid(placed_image, box, resampled, band)
    colours = Colours()
    unchanged_marks, ground_marks = set(), set()
    unchanged = check_unchanged(grid, colours, unchanged_marks)
    ground = check_ground(grid, own, colours, ground_marks)
    if at.out:
        os.makedirs(at.out, exist_ok=True)
        resampled.save(os.path.join(at.out, "expected.png"))
        write_marks(grid, unchanged_marks, os.path.join(at.out, "unchanged.png"))
        write_marks(grid, ground_marks, os.path.join(at.out, "ground.png"))
    return box, band, unchanged, ground


def parse(argv):
    p = argparse.ArgumentParser(
        prog="check-logo.py",
        description="Check a placed client logo against the logo file and its rendered ground.",
    )
    p.add_argument(
        "target",
        help="a page (an http(s) URL or a local HTML file) or an artboard image",
    )
    p.add_argument(
        "--logo", required=True, metavar="FILE", help="the client's logo file"
    )
    where = p.add_mutually_exclusive_group(required=True)
    where.add_argument(
        "--at", metavar="SELECTOR", help="on a page, the element the logo fills"
    )
    where.add_argument(
        "--box", metavar="X,Y,W,H", help="on an image, the logo's box in pixels"
    )
    p.add_argument(
        "--scale",
        type=float,
        default=PAGE_SCALE,
        metavar="N",
        help="device scale on a page",
    )
    p.add_argument("--viewport", default=flow.DESKTOP, metavar="WxH")
    p.add_argument("--wait", metavar="SELECTOR")
    p.add_argument("--timeout", type=int, default=flow.PLAY_TIMEOUT_MS, metavar="MS")
    p.add_argument("--out", metavar="DIR", help="where the marked PNGs go")
    at = p.parse_args(argv)
    try:
        if at.box:
            at.box = parse_box(at.box)
            if not os.path.isfile(at.target):
                raise UsageError(f"no such file: {at.target}")
        else:
            at.viewport_size = flow.size_arg(p, "--viewport", at.viewport)
            at.url = flow.page_url(p, at.target)
    except UsageError as err:
        p.error(str(err))
    return at


def main(argv):
    at = parse(argv)
    try:
        import PIL  # noqa: F401
    except ImportError as err:
        print(
            f"check-logo: {err.name} is missing — python3 -m pip install -r {REQUIREMENTS}",
            file=sys.stderr,
        )
        return 3
    try:
        kind, logo = read_logo(at.logo)
        if kind == "raster":
            refuse_opaque(logo, at.logo)
    except (UsageError, RefusedLogoError) as err:
        print(f"check-logo: {err}", file=sys.stderr)
        return 2

    def work():
        if kind == "raster" and at.box:
            return measure(at, kind, logo, None)
        with flow.chromium() as browser:
            return measure(at, kind, logo, browser)

    try:
        result, code = flow.run_browser(
            work,
            at.timeout,
            None if at.box else at.url,
            (
                f"cannot check the logo on {at.target}, because:",
                "Compare it with the file by eye.",
            ),
        )
    except (UsageError, RefusedLogoError) as err:
        print(f"check-logo: {err}", file=sys.stderr)
        return 2
    if code:
        return code
    box, band, (u_verdict, u_detail), (g_verdict, g_lines) = result
    where = f"--at {at.at}" if at.at else "--box"
    print(
        f"{at.target} — {at.logo} in {box[2]}x{box[3]} px at ({box[0]},{box[1]}) ({where}), "
        f"edge band {band} px"
    )
    print(f"  unchanged: {u_verdict} — {u_detail}")
    print(f"  ground: {g_verdict}" + (" — " + g_lines[0] if len(g_lines) == 1 else ""))
    if len(g_lines) > 1:
        for line in g_lines:
            print(f"    {line}")
    if at.out:
        print(f"  wrote {os.path.join(at.out, '')}{{expected,unchanged,ground}}.png")
    verdicts = (u_verdict, g_verdict)
    if FAIL in verdicts:
        return 1
    return 6 if UNJUDGED in verdicts else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
