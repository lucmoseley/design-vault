#!/usr/bin/env python3
"""check-render.py — the raster check for brand-art renders (design-vault#324),
answering gate questions vault.render-size (design-vault#328) and
vault.render-checkerboard (design-vault#332).

USAGE
  python3 check-render.py <render>… [--log <higgsfield-spend.jsonl>]
        [--model <endpoint id>] [--aspect <w:h>] [--transparent]

Each render's model and requested aspect ratio come from its spend-log line,
found as spend-log.py's header says, in --log or else the log beside each
render. --model and --aspect give either for a render made by hand, and
override the log's where both are given.

Size (vault.render-size): neither side may fall short of the same side of the
model's largest output at that aspect ratio, as references/render-sizes.json
records it with its source. A model or aspect with no size there is reported NOT JUDGED, never
passed.

Checkerboard (vault.render-checkerboard), with --transparent, for a brief that
asked for a transparent background: the render, read over white where it has
real alpha, at most 1920 px on its long side, is cut into tiles. A tile is a
painted grid where shifting it one cell sideways inverts it and one cell
diagonally repeats it (its autocorrelation), and its pixels sit on two flat
tones. Two such tiles fail the render. A render smaller than one tile is NOT
JUDGED. Cells under about 5 px at that scale blur past two tones and are not
found.

EXITS 0 every render passes / 1 a render fails / 2 the arguments are wrong, or
a render, the log or render-sizes.json cannot be read / 3 Pillow, or numpy for
--transparent, is missing / 6 no render fails but one cannot be judged. Exits 0, 1 and 6 are results and print on stdout; the
rest print on stderr.
"""

import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import siblings  # noqa: E402

SIZES = HERE.parent / "references" / "render-sizes.json"
REQUIREMENTS = HERE.parents[2] / "requirements.txt"


spend_log = siblings.load(HERE, "spend-log.py")
UnreadableError = spend_log.UnreadableError

PASS, FAIL, UNJUDGED = "PASS", "FAIL", "NOT JUDGED"

# The checkerboard's figures, all untraced: set on #262's fixtures and on three
# Grok Imagine 2.0 renders that painted one where transparency was asked
# (design-vault#332), against 47 opaque renders and the vault's 106 images.
# The long side the render is read at: at 960, cells under about 15 px on a
# 2816 px render blurred past two tones.
WORK_SIDE = 1920
# The square tile the render is cut into, at that scale.
TILE = 192
# The cell sizes, in px at that scale, a tile is searched for: from 3, the
# smallest whose one-cell shifts still differ, though cells under about 5 blur
# past two tones, to a quarter of the tile, so a tile holds four cells a side.
CELLS = range(3, TILE // 4 + 1)
# A tile flatter than this standard deviation, in 0-255 grey, holds no grid a
# viewer could see.
FLAT_SD = 2
# The autocorrelation score a grid tile reaches: Grok's painted grids 0.66-0.86,
# no opaque render's two-tone tile above 0.49.
GRID_SCORE = 0.65
# The tile's two tones are found by splitting its pixels around two seeds, the
# 10th and 90th percentiles, refined this many times.
TONE_SEEDS = (10, 90)
TONE_ROUNDS = 10
# A pixel sits on a tone within this fraction of the gap between the two.
TONE_BAND = 0.25
# The share of a grid tile's pixels on its two tones: Grok's 0.87 or more, and
# no opaque render's tile over GRID_SCORE.
TWO_TONE_SHARE = 0.8
# Grid tiles that fail a render.
GRID_TILES = 2


def read_sizes():
    """render-sizes.json's rows by model, each size checked for its form and source."""
    try:
        models = json.loads(SIZES.read_text(encoding="utf8"))["models"]
        for model, row in models.items():
            for aspect, largest in row.get("sizes", {}).items():
                if not (
                    re.fullmatch(r"\d+x\d+", largest["size"]) and largest["source"]
                ):
                    raise ValueError(
                        f"{model} at {aspect} is not WIDTHxHEIGHT with a source"
                    )
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as err:
        raise UnreadableError(f"cannot read {SIZES}: {err}") from err
    return models


def requested(render, args, logs):
    """(model, aspect, where they came from), either None where nothing gives it.
    logs is the caller's cache of the spend logs read so far, filled here."""
    entry, where = spend_log.find_line(render, args.log, logs)
    if entry is None:
        return args.model, args.aspect, where
    given = entry.get("input") if isinstance(entry.get("input"), dict) else {}
    return (
        args.model or entry.get("model"),
        args.aspect or given.get("aspect_ratio"),
        where,
    )


def check_size(size, model, aspect, sizes):
    width, height = size
    if model is None:
        return UNJUDGED, "no model: give --model"
    if aspect is None:
        return UNJUDGED, "no requested aspect ratio: give --aspect"
    row = sizes.get(model)
    if row is None:
        return UNJUDGED, f"{model} has no row in render-sizes.json"
    largest = row.get("sizes", {}).get(aspect)
    if largest is None:
        note = f" ({row['note']})" if row.get("note") else ""
        return UNJUDGED, f"no largest size on record for {model} at {aspect}{note}"
    w, h = (int(n) for n in largest["size"].split("x"))
    figures = f"{width}x{height} against the largest, {w}x{h} ({largest['source']})"
    if width >= w and height >= h:
        return PASS, figures
    return FAIL, f"{figures}: render it again at the model's largest size"


def read_grey(image):
    """The render in 0-255 grey over white, its long side at most WORK_SIDE, and that scale."""
    import numpy as np
    from PIL import Image

    if "A" in image.getbands() or "transparency" in image.info:
        rgba = image.convert("RGBA")
        image = Image.alpha_composite(Image.new("RGBA", rgba.size, "white"), rgba)
    grey = image.convert("L")
    scale = min(1.0, WORK_SIDE / max(grey.size))
    if scale < 1:
        grey = grey.resize(
            (round(grey.width * scale), round(grey.height * scale)),
            Image.Resampling.LANCZOS,
        )
    return np.asarray(grey, dtype=np.float64), scale


def grid_cell(tile):
    """The cell size of the painted two-tone grid the tile holds, or None."""
    import numpy as np

    tile = tile - tile.mean()
    if tile.std() < FLAT_SD:
        return None
    padded = np.fft.rfft2(tile, s=(2 * TILE, 2 * TILE))
    shifted = np.fft.irfft2(padded * np.conj(padded), s=(2 * TILE, 2 * TILE))
    shifted /= shifted[0, 0]
    score, cell = max(
        (
            (shifted[c, c] + shifted[c, -c] - shifted[c, 0] - shifted[0, c]) / 4,
            c,
        )
        for c in CELLS
    )
    if score < GRID_SCORE:
        return None
    low, high = (np.percentile(tile, q) for q in TONE_SEEDS)
    for _ in range(TONE_ROUNDS):
        nearer_low = (tile - low) ** 2 < (tile - high) ** 2
        if nearer_low.all() or not nearer_low.any():
            return None
        low, high = tile[nearer_low].mean(), tile[~nearer_low].mean()
    near = np.minimum(abs(tile - low), abs(tile - high)) <= (high - low) * TONE_BAND
    return cell if near.mean() >= TWO_TONE_SHARE else None


def tile_starts(length):
    """Tile origins along one side, the last flush with its end."""
    count = -(-length // TILE)
    return sorted(
        {round(i * (length - TILE) / max(count - 1, 1)) for i in range(count)}
    )


def check_checkerboard(image):
    grey, scale = read_grey(image)
    height, width = grey.shape
    if width < TILE or height < TILE:
        return UNJUDGED, f"under {TILE} px a side at the scale it is read at"
    grids = []
    tiles = 0
    for y in tile_starts(height):
        for x in tile_starts(width):
            tiles += 1
            cell = grid_cell(grey[y : y + TILE, x : x + TILE])
            if cell is not None:
                grids.append((x, y, cell))
    if len(grids) < GRID_TILES:
        return PASS, f"{len(grids)} of {tiles} tiles hold a two-tone grid"
    cells = sorted(round(c / scale) for _, _, c in grids)
    x0, y0 = (round(min(g[i] for g in grids) / scale) for i in (0, 1))
    x1, y1 = (round((max(g[i] for g in grids) + TILE) / scale) for i in (0, 1))
    return FAIL, (
        f"{len(grids)} of {tiles} tiles hold a painted two-tone grid of about "
        f"{cells[len(cells) // 2]} px cells, within {x0},{y0} to "
        f"{min(x1, image.width)},{min(y1, image.height)}: render it again on one "
        "loud plain colour and cut it out with cutout.py"
    )


def main(argv):
    parser = argparse.ArgumentParser(
        prog="check-render.py",
        description="Check brand-art renders: the size against the model's largest output, and with --transparent a painted checkerboard.",
    )
    parser.add_argument("renders", nargs="+", metavar="render")
    parser.add_argument(
        "--log",
        help=f"the round's spend log; default the {spend_log.LOG_NAME} beside each render",
    )
    parser.add_argument(
        "--model", help="the model's endpoint id, for a render with no log line"
    )
    parser.add_argument("--aspect", help="the requested aspect ratio, w:h")
    parser.add_argument(
        "--transparent",
        action="store_true",
        help="the brief asked for a transparent background: check for a painted checkerboard",
    )
    args = parser.parse_args(argv)
    try:
        from PIL import Image

        if args.transparent:
            import numpy  # noqa: F401 — the checkerboard needs it
    except ImportError as err:
        print(
            f"check-render: {err.name} is missing — python3 -m pip install -r {REQUIREMENTS}",
            file=sys.stderr,
        )
        return 3
    if args.aspect is not None:
        args.aspect = args.aspect.replace(" ", "")

    logs = {}
    results = []
    try:
        sizes = read_sizes()
    except UnreadableError as err:
        print(f"check-render: {err}", file=sys.stderr)
        return 2
    for render in args.renders:
        try:
            try:
                with Image.open(render) as image:
                    width, height = image.size
                    checkerboard = (
                        check_checkerboard(image) if args.transparent else None
                    )
            except OSError as err:
                raise UnreadableError(f"cannot read {render}: {err}") from err
            model, aspect, where = requested(render, args, logs)
        except UnreadableError as err:
            print(f"check-render: {err}", file=sys.stderr)
            return 2
        verdict, detail = check_size((width, height), model, aspect, sizes)
        results.append(verdict)
        print(
            f"{render} — {model or 'model unknown'} at {aspect or 'aspect unknown'} ({where})"
        )
        print(f"  size: {verdict} — {detail}")
        if checkerboard is not None:
            results.append(checkerboard[0])
            print(f"  checkerboard: {checkerboard[0]} — {checkerboard[1]}")

    if FAIL in results:
        return 1
    return 6 if UNJUDGED in results else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
