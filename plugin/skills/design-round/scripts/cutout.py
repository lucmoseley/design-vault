#!/usr/bin/env python3
"""Cuts a render's plain background out to transparency: the colour key
(design-vault#54, design-vault#56).

Usage:
  python3 cutout.py <render> [--out <path.png>]

Writes the cut as a PNG, by default `<render stem>-cut.png` beside the render,
and beside it the same cut laid on a dark and on a bright backdrop
(`-cut-on-dark.png`, `-cut-on-bright.png`) for the by-eye check.

The render asks for one loud plain background colour the subject doesn't use.
The method:
  1. The key colour is the median of an 8 px border.
  2. The background is the pixels within Euclidean RGB distance 14 of the key
     that connect to the image's edge. A key-coloured part enclosed by the
     subject stays opaque; one that reaches the frame's edge is cut.
  3. In a 4 px ring around the background, each pixel C is un-mixed against the
     key B and the nearest solid subject colour F:
     alpha = (C-B).(F-B) / |F-B|^2, and its colour becomes F. Detail thinner
     than the ring takes the colour of the nearest solid pixel.

Needs numpy, Pillow and scipy. Exits 0 cut / 1 no background or no subject
found / 2 the arguments are wrong, or a file cannot be read or written / 3 a
package is missing.
"""

import argparse
import os
import pathlib
import sys

REQUIREMENTS = pathlib.Path(__file__).resolve().parents[3] / "requirements.txt"

# KEY_DISTANCE, BORDER and RING are the #54 prototype's, which cut three of its
# four r3 renders clean; guesses, not tuned further. MIN_REGION, the px under
# which a kept key-coloured hole is only counted, and the dark backdrop's grey
# are new here, picked by eye.
KEY_DISTANCE = 14.0
BORDER = 8
RING = 4
MIN_REGION = 16
BACKDROPS = {"dark": (24, 24, 24), "bright": (255, 255, 255)}


def cut(rgb):
    """Takes an HxWx3 array; returns the HxWx4 uint8 cut and the report's figures."""
    import numpy as np
    from scipy import ndimage

    a = rgb.astype(np.float32)
    border = np.concatenate(
        [
            a[:BORDER].reshape(-1, 3),
            a[-BORDER:].reshape(-1, 3),
            a[:, :BORDER].reshape(-1, 3),
            a[:, -BORDER:].reshape(-1, 3),
        ]
    )
    key = np.median(border, 0)
    near_key = np.sqrt(((a - key) ** 2).sum(2)) < KEY_DISTANCE
    labels, _ = ndimage.label(near_key)
    edge = np.unique(
        np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]])
    )
    edge = edge[edge > 0]
    outside = np.isin(labels, edge)
    ring = ndimage.binary_dilation(outside, iterations=RING) & ~outside
    solid = ~outside & ~ring
    if not outside.any():
        return None, {"key": key, "failure": "no background touches the frame's edge"}
    if not solid.any():
        return None, {"key": key, "failure": "no subject found"}

    iy, ix = ndimage.distance_transform_edt(
        ~solid, return_distances=False, return_indices=True
    )
    fill = a[iy, ix]
    fb = fill - key
    alpha = np.clip(((a - key) * fb).sum(2) / np.maximum((fb**2).sum(2), 1.0), 0, 1)
    alpha = np.where(outside, 0.0, np.where(solid, 1.0, alpha))
    colour = np.where(solid[..., None], a, fill)
    rgba = np.dstack([colour, alpha * 255]).round().astype(np.uint8)

    kept = rgba[..., 3] > 0
    partial = kept & (rgba[..., 3] < 255)
    holes = []
    small = 0
    boxes = ndimage.find_objects(labels)
    for n in np.unique(labels[near_key & ~outside]):
        box = boxes[n - 1]
        size = int((labels[box] == n).sum())
        if size < MIN_REGION:
            small += 1
            continue
        holes.append(
            (size, box[1].start, box[0].start, box[1].stop - 1, box[0].stop - 1)
        )
    holes.sort(reverse=True)
    return rgba, {
        "key": key,
        "partial_share": partial.sum() / max(kept.sum(), 1),
        "holes": holes,
        "small_holes": small,
    }


def on_backdrop(rgba, colour):
    import numpy as np

    alpha = rgba[..., 3:4].astype(np.float32) / 255
    mixed = rgba[..., :3] * alpha + np.array(colour, np.float32) * (1 - alpha)
    return mixed.round().astype(np.uint8)


def main(argv):
    parser = argparse.ArgumentParser(
        prog="cutout.py",
        description="Cut a render's plain background out to transparency.",
    )
    parser.add_argument("render")
    parser.add_argument(
        "--out", help="the cut's path, a .png; default <render stem>-cut.png"
    )
    args = parser.parse_args(argv)
    try:
        import numpy as np
        from PIL import Image
        import scipy  # noqa: F401
    except ImportError as err:
        print(
            f"cutout: {err.name} is missing — python3 -m pip install -r {REQUIREMENTS}",
            file=sys.stderr,
        )
        return 3

    out = args.out or os.path.splitext(args.render)[0] + "-cut.png"
    if not out.lower().endswith(".png"):
        print("cutout: --out must be a .png", file=sys.stderr)
        return 2
    try:
        rgb = np.asarray(Image.open(args.render).convert("RGB"))
    except OSError as err:
        print(f"cutout: cannot read {args.render}: {err}", file=sys.stderr)
        return 2

    rgba, report = cut(rgb)
    key = "#%02x%02x%02x" % tuple(int(round(c)) for c in report["key"])
    if rgba is None:
        print(
            f"cutout: nothing cut — key {key}, and {report['failure']}", file=sys.stderr
        )
        return 1

    stem = os.path.splitext(out)[0]
    backdrops = {f"{stem}-on-{name}.png": colour for name, colour in BACKDROPS.items()}
    try:
        Image.fromarray(rgba, "RGBA").save(out)
        for path, colour in backdrops.items():
            Image.fromarray(on_backdrop(rgba, colour), "RGB").save(path)
    except OSError as err:
        print(f"cutout: cannot write the cut: {err}", file=sys.stderr)
        return 2

    print(f"cut: {out} (key {key})")
    print(f"backdrops: {', '.join(backdrops)}")
    print(
        f"partly transparent: {report['partial_share']:.1%} of kept pixels — more than a few percent is likely a shadow or a soft edge"
    )
    holes = report["holes"]
    if holes:
        print(
            "key-coloured regions kept inside the subject — each is a hole the key could not reach, or a part that shares the key colour:"
        )
        for size, x0, y0, x1, y1 in holes:
            print(f"  {size} px, x {x0}–{x1}, y {y0}–{y1}")
    else:
        print("key-coloured regions kept inside the subject: none")
    if report["small_holes"]:
        print(f"  and {report['small_holes']} under {MIN_REGION} px, not listed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
