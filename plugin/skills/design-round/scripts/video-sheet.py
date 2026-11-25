#!/usr/bin/env python3
"""video-sheet.py — a reference clip laid out for a technique study: ten frames
a second and every frame either side of each cut, tiled and labelled with their
times.

USAGE
  python3 video-sheet.py <clip> --out DIR [--fps N] [--around S] [--cut SCORE]
        [--per-sheet N]

It keeps the first frame at or after every 1/--fps s, every frame within
--around s of each cut, and the last frame. A cut is a frame whose score, as
ffmpeg's scdet filter scores one, reaches --cut; the score is read on a
greyscale copy SCORE_WIDTH px wide.

It writes every kept frame at full size as DIR/frames/frame-<ms>.png; the tiles
in time order as DIR/sheet-1.png, DIR/sheet-2.png and on, --per-sheet to a
sheet, each labelled with its time in seconds, `cut` on the first frame of a new
shot and `end` on the last; and DIR/sheet.json naming the clip, its length, its
cuts and each tile's time, sheet and box in its sheet's pixels.

EXITS 0 the sheets are written / 2 the arguments are wrong / 3 PyAV, numpy or
Pillow is missing / 4 the file is no clip PyAV can decode / 5 DIR cannot be
written. Exit 0 prints on stdout; the rest print on stderr.
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

SCORE_WIDTH = 160  # guess, #408
TILE = 320  # px; guess, #408
GAP = PAD = 16  # px; guess, #408
COLUMNS = 5  # guess, #408
LABEL = 16  # px; guess, #408
LABEL_GAP = 4  # px; guess, #408
CAPTION = LABEL_GAP + LABEL + 2 * LABEL_GAP  # one gap above the label, two below
EPS = 1e-6  # s; guess, #408


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


def decode(path, each):
    container, stream = open_clip(path)
    try:
        for index, frame in enumerate(container.decode(stream)):
            if frame.time is None:
                raise ClipError(f"frame {index} carries no timestamp")
            each(index, float(frame.time), frame)
    except av.error.FFmpegError as e:
        raise ClipError(f"it stopped decoding: {e}") from e
    finally:
        container.close()


def scores(diffs):
    # https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_scdet.c: MAFD is the
    # mean difference x 100 / 2^bitdepth; score min(MAFD, |MAFD - previous MAFD|), 0 to 100.
    out, previous = [], 0.0
    for mafd in diffs:
        if mafd is None:
            out.append(0.0)
            continue
        out.append(max(0.0, min(100.0, mafd, abs(mafd - previous))))
        previous = mafd
    return out


def survey(path):
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
            else float(np.abs(grey - last[0]).mean() * 100 / 256)
        )
        last[0] = grey

    decode(path, each)
    if not times:
        raise ClipError("it has no frames")
    return times, scores(diffs)


def keep(times, cut_at, fps, around):
    kept = set()
    step, k = 1 / fps, 0
    for i, t in enumerate(times):
        while k * step <= t + EPS:
            kept.add(i)
            k += 1
    cuts = [times[i] for i in cut_at]
    for i, t in enumerate(times):
        if any(abs(t - c) <= around + EPS for c in cuts):
            kept.add(i)
    kept.add(len(times) - 1)
    return sorted(kept)


def label(t, *, cut, end):
    marks = [m for m, on in (("cut", cut), ("end", end)) if on]
    return f"{t:.2f} s" + (f" ({', '.join(marks)})" if marks else "")


def sheet(tiles, tile_h):
    rows = -(-len(tiles) // COLUMNS)
    columns = min(COLUMNS, len(tiles))
    cell_h = tile_h + CAPTION
    canvas = Image.new(
        "RGB",
        (columns * (TILE + GAP) - GAP + 2 * PAD, rows * (cell_h + GAP) - GAP + 2 * PAD),
        "white",
    )
    draw, face, boxes = ImageDraw.Draw(canvas), ImageFont.load_default(size=LABEL), []
    for n, (text, thumb) in enumerate(tiles):
        x = PAD + (n % COLUMNS) * (TILE + GAP)
        y = PAD + (n // COLUMNS) * (cell_h + GAP)
        canvas.paste(thumb, (x, y))
        draw.rectangle((x - 1, y - 1, x + TILE, y + tile_h), outline="#bbbbbb")
        draw.text((x, y + tile_h + LABEL_GAP), text, fill="#111111", font=face)
        boxes.append({"x": x, "y": y, "width": TILE, "height": tile_h})
    return canvas, boxes


def run(args):
    times, score = survey(args.clip)
    cut_at = [i for i, s in enumerate(score) if s >= args.cut]
    kept = keep(times, cut_at, args.fps, args.around)
    wanted, thumbs, size = set(kept), {}, []
    folder = os.path.join(args.out, "frames")
    os.makedirs(folder, exist_ok=True)

    def each(i, t, frame):
        if i not in wanted:
            return
        image = frame.to_image().convert("RGB")
        image.save(os.path.join(folder, f"frame-{round(t * 1000)}.png"))
        if not size:
            size.extend(image.size)
        thumbs[i] = image.resize(
            (TILE, round(TILE * image.height / image.width)), Image.LANCZOS
        )

    decode(args.clip, each)
    cuts, last = set(cut_at), len(times) - 1
    tiles = [
        {
            "ms": round(times[i] * 1000),
            "label": label(times[i], cut=i in cuts, end=i == last),
            "cut": i in cuts,
        }
        for i in kept
    ]
    tile_h = thumbs[kept[0]].height
    sheets = []
    for start in range(0, len(kept), args.per_sheet):
        group = range(start, min(start + args.per_sheet, len(kept)))
        canvas, boxes = sheet(
            [(tiles[n]["label"], thumbs[kept[n]]) for n in group], tile_h
        )
        path = os.path.join(args.out, f"sheet-{len(sheets) + 1}.png")
        canvas.save(path)
        sheets.append(path)
        for n, box in zip(group, boxes, strict=True):
            tiles[n].update(sheet=len(sheets), **box)
    record = {
        "clip": args.clip,
        "width": size[0],
        "height": size[1],
        "frames": len(times),
        "end_ms": round(times[last] * 1000),
        "fps": args.fps,
        "around_s": args.around,
        "cut_threshold": args.cut,
        "cuts_ms": [round(times[i] * 1000) for i in cut_at],
        "sheets": sheets,
        "tiles": tiles,
    }
    with open(os.path.join(args.out, "sheet.json"), "w", encoding="utf8") as fh:
        json.dump(record, fh, indent=1)
        fh.write("\n")
    return record


def report(args, record):
    cuts = record["cuts_ms"]
    where = (
        f"and every frame within {args.around:g} s of {len(cuts)} cut(s), at "
        + ", ".join(f"{ms / 1000:.2f} s" for ms in cuts)
        if cuts
        else "and no cut found"
    )
    return "\n".join(
        [
            f"video-sheet: {record['clip']} — {record['width']}x{record['height']}, "
            f"{record['frames']} frames to {record['end_ms'] / 1000:.2f} s",
            f"  {len(record['tiles'])} kept: {args.fps:g} a second, {where}",
            f"  {len(record['sheets'])} sheet(s): " + ", ".join(record["sheets"]),
            f"tiles listed in {os.path.join(args.out, 'sheet.json')}",
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
        "--fps", type=float, default=10, help="frames kept a second; 10, set by #408"
    )
    p.add_argument(
        "--around",
        type=float,
        default=0.2,
        metavar="S",
        help="every frame this many seconds either side of a cut is kept; 0.2, guess, #408",
    )
    p.add_argument(
        "--cut",
        type=float,
        default=10,
        metavar="SCORE",
        help="the score a cut reaches; 10, ffmpeg scdet's default (libavfilter/vf_scdet.c)",
    )
    p.add_argument(
        "--per-sheet",
        type=int,
        default=30,
        metavar="N",
        help="tiles to a sheet; 30, guess, #408",
    )
    args = p.parse_args(argv)
    if args.fps <= 0:
        p.error("--fps wants a number above 0")
    if args.around < 0:
        p.error("--around wants 0 or more")
    if args.per_sheet < 1:
        p.error("--per-sheet wants at least 1")
    if not os.path.isfile(args.clip):
        p.error(f"no file at {args.clip}")
    return args


def main(argv):
    args = parse(argv)
    try:
        record = run(args)
    except ClipError as e:
        print(f"cannot sheet {args.clip}, because {e}", file=sys.stderr)
        return 4
    except OSError as e:
        print(f"cannot write the sheets under {args.out}: {e}", file=sys.stderr)
        return 5
    print(report(args, record))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
