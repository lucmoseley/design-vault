#!/usr/bin/env python3
"""video-sheet.py — a reference clip laid out for a technique study: ten frames
a second, every frame either side of each cut, tiled and labelled with their
times (design-vault#408).

USAGE
  python3 video-sheet.py <clip> --out DIR [--fps N] [--around S] [--cut PCT]
        [--per-sheet N]

It decodes the clip with PyAV, ffmpeg's own libraries, twice: once to find the
cuts, once to keep the frames. It keeps the first frame at or after every
1/--fps s (10 a second by default), every frame within --around s of each cut
(0.2 s), and the last frame. A cut is scored as ffmpeg's scdet filter scores
one: the mean absolute difference from the frame before, as a percentage of
full range, less its change from the previous difference, so steady motion
scores low and a hard change high. scdet sums every plane at full size; this
reads a greyscale copy 160 px wide, and a score at or over --cut (scdet's
default of 10) is a cut.

It writes every kept frame at full size as DIR/frames/frame-<ms>.png, the
tiles in time order as DIR/sheet-1.png, DIR/sheet-2.png and on, --per-sheet
(30) to a sheet, each labelled with its time in seconds, `cut` on the first
frame of a new shot and `end` on the last, and DIR/sheet.json naming the clip,
its length, its cuts and each tile's time, sheet and box in its sheet's pixels.

EXITS 0 the sheets are written / 2 the arguments are wrong / 3 PyAV, numpy or
Pillow is missing / 4 the file is no clip PyAV can decode. Exit 0 prints on
stdout; the rest print on stderr.
"""

import argparse
import json
import os
import sys

REQUIREMENTS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "requirements.txt"
)
try:
    import av
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(
        f"video-sheet.py needs {e.name}: python3 -m pip install --only-binary :all: "
        f"-r {os.path.normpath(REQUIREMENTS)}",
        file=sys.stderr,
    )
    sys.exit(3)

# The greyscale copy cuts are scored on: small enough to decode fast, wide
# enough that a cut between two shots of one palette still differs. A guess.
SCORE_WIDTH = 160
# A tile's width, the gaps between tiles and around a sheet, its columns and
# its label's size, in the sheet's pixels: picked by eye, five tiles to a row
# so a sheet stays under 1700 px wide.
TILE = 320
GAP = PAD = 16
COLUMNS = 5
LABEL = 16


class ClipError(Exception):
    pass


def open_clip(path):
    try:
        container = av.open(path)
    except (av.error.FFmpegError, OSError) as e:
        raise ClipError(f"cannot open it: {e}") from e
    if not container.streams.video:
        container.close()
        raise ClipError("it has no video stream")
    return container, container.streams.video[0]


def frame_time(frame, index, stream):
    if frame.time is not None:
        return float(frame.time)
    rate = stream.average_rate or 25
    return index / float(rate)


def decode(path, each):
    """Calls each(index, seconds, frame) for every frame in decode order."""
    container, stream = open_clip(path)
    try:
        for index, frame in enumerate(container.decode(stream)):
            each(index, frame_time(frame, index, stream), frame)
    except av.error.FFmpegError as e:
        raise ClipError(f"it stopped decoding: {e}") from e
    finally:
        container.close()


def scores(diffs):
    """scdet's score for each frame from its mean absolute difference (MAFD) from
    the frame before: min(MAFD, |MAFD - the previous MAFD|), within 0 to 100.
    The first frame has nothing before it and scores 0."""
    out, previous = [], None
    for mafd in diffs:
        if mafd is None:
            out.append(0.0)
        else:
            delta = abs(mafd - previous) if previous is not None else mafd
            out.append(max(0.0, min(100.0, min(mafd, delta))))
        previous = mafd
    return out


def survey(path):
    """Each frame's time and cut score, in decode order."""
    times, diffs, last = [], [], [None]

    def each(_, t, frame):
        height = max(1, round(frame.height * SCORE_WIDTH / frame.width))
        grey = (
            frame.reformat(width=SCORE_WIDTH, height=height, format="gray")
            .to_ndarray()
            .astype(np.int16)
        )
        times.append(t)
        diffs.append(
            None
            if last[0] is None
            else float(np.abs(grey - last[0]).mean() * 100 / 255)
        )
        last[0] = grey

    decode(path, each)
    if not times:
        raise ClipError("it has no frames")
    return times, scores(diffs)


def keep(times, cut_at, fps, around):
    """The indices of the frames to keep: the first at or after each 1/fps step,
    every one within `around` s of a cut, and the last."""
    kept = set()
    step, k = 1 / fps, 0
    for i, t in enumerate(times):
        # A step's time can land a hair past a frame's from float rounding.
        while k * step <= t + 1e-6:
            kept.add(i)
            k += 1
    cuts = [times[i] for i in cut_at]
    for i, t in enumerate(times):
        if any(abs(t - c) <= around + 1e-6 for c in cuts):
            kept.add(i)
    kept.add(len(times) - 1)
    return sorted(kept)


def label(t, *, cut, end):
    marks = [m for m, on in (("cut", cut), ("end", end)) if on]
    return f"{t:.2f} s" + (f" ({', '.join(marks)})" if marks else "")


def sheet(tiles, size):
    """One sheet of (label, image) tiles, and each tile's box."""
    w, h = size
    tile_h = round(TILE * h / w)
    rows = -(-len(tiles) // COLUMNS)
    columns = min(COLUMNS, len(tiles))
    cell_h = tile_h + LABEL + 12
    canvas = Image.new(
        "RGB",
        (columns * (TILE + GAP) - GAP + 2 * PAD, rows * (cell_h + GAP) - GAP + 2 * PAD),
        "white",
    )
    draw, face, boxes = ImageDraw.Draw(canvas), ImageFont.load_default(size=LABEL), []
    for n, (text, image) in enumerate(tiles):
        x = PAD + (n % COLUMNS) * (TILE + GAP)
        y = PAD + (n // COLUMNS) * (cell_h + GAP)
        canvas.paste(image.resize((TILE, tile_h), Image.LANCZOS), (x, y))
        draw.rectangle((x - 1, y - 1, x + TILE, y + tile_h), outline="#bbbbbb")
        draw.text((x, y + tile_h + 4), text, fill="#111111", font=face)
        boxes.append({"x": x, "y": y, "width": TILE, "height": tile_h})
    return canvas, boxes


def run(at):
    times, score = survey(at.clip)
    cut_at = [i for i, s in enumerate(score) if s >= at.cut]
    kept = keep(times, cut_at, at.fps, at.around)
    wanted, frames = set(kept), {}

    def each(i, _, frame):
        if i in wanted:
            frames[i] = frame.to_image().convert("RGB")

    decode(at.clip, each)
    os.makedirs(os.path.join(at.out, "frames"), exist_ok=True)
    cuts, last = set(cut_at), len(times) - 1
    tiles = []
    for i in kept:
        ms = round(times[i] * 1000)
        frames[i].save(os.path.join(at.out, "frames", f"frame-{ms}.png"))
        tiles.append(
            {
                "ms": ms,
                "label": label(times[i], cut=i in cuts, end=i == last),
                "cut": i in cuts,
            }
        )
    size = frames[kept[0]].size
    sheets = []
    for start in range(0, len(kept), at.per_sheet):
        group = list(range(start, min(start + at.per_sheet, len(kept))))
        canvas, boxes = sheet(
            [(tiles[n]["label"], frames[kept[n]]) for n in group], size
        )
        path = os.path.join(at.out, f"sheet-{len(sheets) + 1}.png")
        canvas.save(path)
        sheets.append(path)
        for n, box in zip(group, boxes, strict=True):
            tiles[n].update(sheet=len(sheets), **box)
    record = {
        "clip": at.clip,
        "width": size[0],
        "height": size[1],
        "frames": len(times),
        "end_ms": round(times[last] * 1000),
        "fps": at.fps,
        "around_s": at.around,
        "cut_threshold": at.cut,
        "cuts_ms": [round(times[i] * 1000) for i in cut_at],
        "sheets": sheets,
        "tiles": tiles,
    }
    with open(os.path.join(at.out, "sheet.json"), "w", encoding="utf8") as fh:
        json.dump(record, fh, indent=1)
        fh.write("\n")
    return record


def report(at, record):
    cuts = record["cuts_ms"]
    where = (
        f"and every frame within {at.around:g} s of {len(cuts)} cut(s), at "
        + ", ".join(f"{ms / 1000:.2f} s" for ms in cuts)
        if cuts
        else "and no cut found"
    )
    return "\n".join(
        [
            f"video-sheet: {record['clip']} — {record['width']}x{record['height']}, "
            f"{record['frames']} frames to {record['end_ms'] / 1000:.2f} s",
            f"  {len(record['tiles'])} kept: {at.fps:g} a second, {where}",
            f"  {len(record['sheets'])} sheet(s): " + ", ".join(record["sheets"]),
            f"tiles listed in {os.path.join(at.out, 'sheet.json')}",
        ]
    )


def parse(argv):
    p = argparse.ArgumentParser(
        prog="video-sheet.py",
        description="Tile a reference clip's frames, ten a second and every one around each cut, labelled with their times.",
    )
    p.add_argument("clip", help="a video file: MP4, WebM, MOV or any PyAV decodes")
    p.add_argument("--out", required=True, metavar="DIR")
    p.add_argument(
        "--fps",
        type=float,
        default=10,
        help="frames kept a second; 10, the rate design-vault#403 item 7 names",
    )
    p.add_argument(
        "--around",
        type=float,
        default=0.2,
        metavar="S",
        help="every frame this many seconds either side of a cut is kept; 0.2, two steps at 10 a second",
    )
    p.add_argument(
        "--cut",
        type=float,
        default=10,
        metavar="PCT",
        help="the score a cut reaches; 10, ffmpeg scdet's default (libavfilter/vf_scdet.c)",
    )
    p.add_argument(
        "--per-sheet",
        type=int,
        default=30,
        metavar="N",
        help="tiles to a sheet: 30, three seconds at 10 a second",
    )
    at = p.parse_args(argv)
    if at.fps <= 0:
        p.error("--fps wants a number above 0")
    if at.around < 0:
        p.error("--around wants 0 or more")
    if at.per_sheet < 1:
        p.error("--per-sheet wants at least 1")
    if not os.path.isfile(at.clip):
        p.error(f"no file at {at.clip}")
    return at


def main(argv):
    at = parse(argv)
    try:
        record = run(at)
    except ClipError as e:
        print(f"cannot sheet {at.clip}, because {e}", file=sys.stderr)
        return 4
    print(report(at, record))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
