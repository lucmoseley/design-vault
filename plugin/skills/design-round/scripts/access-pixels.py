import collections

import numpy as np

Floors = collections.namedtuple("Floors", "body large large_px large_bold_px bold")
# guess, #163
PX_SLACK = 0.05
# WCAG F83 leaves no pixel behind a letter short: https://www.w3.org/WAI/WCAG22/Techniques/failures/F83
WORST_SHARE = 0
# guess, #257
STROKE_PX = 3
# guess, #257
BLEND_PX = 1
# guess, #164
PAINT_NOISE = 8
# guess, #257
OWN_COLOUR = 8
# guess, #163
EDGE_LINES = range(-2, 3)
# guess, #197
DRAWN = 1.02
# guess, #163
FILL_INSET = 4
# WCAG 1.4.11 asks a focus indicator for 3:1: https://www.w3.org/TR/WCAG22/#non-text-contrast
FOCUS_RATIO = 3.0
# measured 50 of 600 tries passed at 1 px and none at 2 px, #222
STILL_MARGIN = 2


def luminance(rgb):
    # https://www.w3.org/TR/WCAG22/#dfn-relative-luminance
    c = np.asarray(rgb, dtype=float) / 255
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return lin @ np.array([0.2126, 0.7152, 0.0722])


def large(size, weight, floors):
    return size >= floors.large_px - PX_SLACK or (
        size >= floors.large_bold_px - PX_SLACK and weight >= floors.bold
    )


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (np.maximum(la, lb) + 0.05) / (np.minimum(la, lb) + 0.05)


def hexed(rgb):
    return "#" + "".join(f"{round(float(c)):02x}" for c in rgb)


def _bounds(image, rect):
    h, w = image.shape[:2]
    left, top = max(int(round(rect[0])), 0), max(int(round(rect[1])), 0)
    right, bottom = min(int(round(rect[2])), w), min(int(round(rect[3])), h)
    return left, top, max(right, left), max(bottom, top)


def _window(image, rect):
    left, top, right, bottom = _bounds(image, rect)
    return image[top:bottom, left:right]


def _slide(padded, k, test):
    return test(np.lib.stride_tricks.sliding_window_view(padded, (k, k)), axis=(-2, -1))


def _strokes(shot, rect, rgb):
    k = STROKE_PX + 1
    left, top, right, bottom = _bounds(shot, rect)
    if right == left or bottom == top:
        return np.zeros((bottom - top, right - left), dtype=bool)
    outer = _bounds(shot, [left - k, top - k, right + k, bottom + k])
    outer_left, outer_top = outer[:2]
    own = (np.abs(_window(shot, outer).astype(int) - rgb) <= OWN_COLOUR).all(axis=-1)
    fits = _slide(np.pad(own, ((0, k - 1), (0, k - 1))), k, np.all)
    patch = _slide(np.pad(fits, ((k - 1, 0), (k - 1, 0))), k, np.any)
    near = _slide(np.pad(own & ~patch, BLEND_PX), 2 * BLEND_PX + 1, np.any)
    return near[
        top - outer_top : bottom - outer_top, left - outer_left : right - outer_left
    ]


def pixels(shot, rect):
    return _window(shot, rect).reshape(-1, 3).astype(float)


def ink_mask(back, black, white):
    if not back.shape == black.shape == white.shape:
        return np.ones(back.shape[:2], dtype=bool)
    return (black != white).any(axis=-1)


def _meet(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def text_contrast(shot, ink, text, floors, *, held=()):
    return text_reading(shot, ink, text, floors, held=held)[:2]


def text_reading(shot, ink, text, floors, *, held=()):
    if text["why"]:
        return None, f"{text['subject']} {text['why']}", None
    if any(_meet(r, h) for r in text["rects"] for h in held):
        return (
            None,
            f"{text['subject']} holds its own fill, which the check cannot take off",
            None,
        )
    *rgb, alpha = text["color"]
    masks = [_window(ink, r).reshape(-1) for r in text["rects"]]
    kept = [
        m & ~_strokes(shot, r, rgb).reshape(-1)
        for r, m in zip(text["rects"], masks, strict=True)
    ]
    if any(k.any() for k in kept):
        masks = kept
    if not any(m.size for m in masks):
        return None, f"{text['subject']} lies off the screenshot", None
    behind = np.concatenate(
        [pixels(shot, r)[m] for r, m in zip(text["rects"], masks, strict=True)]
    )
    if not len(behind):
        return None, None, None
    seen = alpha * np.array(rgb, dtype=float) + (1 - alpha) * behind
    ratios = contrast(seen, behind)
    worst = float(np.percentile(ratios, WORST_SHARE))
    need = floors.large if large(text["size"], text["weight"], floors) else floors.body
    if worst >= need:
        return None, None, worst
    i = int(np.argmin(np.abs(ratios - worst)))
    size = f"{text['size']:g} px{' bold' if text['weight'] >= floors.bold else ''}"
    return (
        f"is {worst:.2f}:1 against {hexed(behind[i])} behind it; {need:g}:1 needed ({hexed(seen[i])} text, {size})",
        None,
        None,
    )


def side_lines(rect, side, offset):
    left, top, right, bottom = (int(round(v)) for v in rect)
    qw, qh = (right - left) // 4, (bottom - top) // 4
    if side == "top":
        y = top + offset
        return [left + qw, y, right - qw, y + 1]
    if side == "bottom":
        y = bottom - 1 - offset
        return [left + qw, y, right - qw, y + 1]
    if side == "left":
        x = left + offset
        return [x, top + qh, x + 1, bottom - qh]
    x = right - 1 - offset
    return [x, top + qh, x + 1, bottom - qh]


Reading = collections.namedtuple("Reading", "ratio behind")


def edge_contrast(shot, behind, rect):
    left, top, right, bottom = rect
    regions = [
        side_lines(rect, side, d)
        for side in ("top", "right", "bottom", "left")
        for d in EDGE_LINES
    ]
    regions.append(
        [left + FILL_INSET, top + FILL_INSET, right - FILL_INSET, bottom - FILL_INSET]
    )
    best = None
    for region in regions:
        drawn, under = pixels(shot, region), pixels(behind, region)
        if not len(drawn) or not len(under):
            continue
        ground = np.median(under, axis=0)
        ratio = float(contrast(np.median(drawn, axis=0), ground))
        if best is None or ratio > best.ratio:
            best = Reading(ratio, ground)
    return best


def reach(rect):
    out = -min(EDGE_LINES)
    return [rect[0] - out, rect[1] - out, rect[2] + out, rect[3] + out]


def hide_groups(controls):
    groups = []
    for i, boxes in enumerate(controls):
        taken = {
            groups[j]
            for j in range(i)
            if _meet(reach(boxes[-1]["rect"]), reach(controls[j][-1]["rect"]))
        }
        groups.append(next(g for g in range(len(controls)) if g not in taken))
    return groups


def moved(shot, again, rect):
    a, b = _window(shot, rect), _window(again, rect)
    h, w = min(a.shape[0], b.shape[0]), min(a.shape[1], b.shape[1])
    return bool((a[:h, :w] != b[:h, :w]).any())


Edge = collections.namedtuple("Edge", "box ratio behind")


def control_edge(shot, behind, boxes):
    for i, b in enumerate(boxes):
        best = edge_contrast(shot, behind[i], b["rect"])
        if best is None and i == 0:
            return None
        if best is not None and best.ratio >= DRAWN:
            return Edge(b, best.ratio, best.behind)
    return Edge(None, None, None)


def focus_changed(on, off, region, still):
    a, b = pixels(on, region), pixels(off, region)
    if not len(a):
        return 0
    keep = pixels(np.repeat(still[..., None], 3, axis=-1), region)[:, 0].astype(bool)
    return int(np.count_nonzero((contrast(a, b) >= FOCUS_RATIO) & keep))


def still_pixels(on, off, on_again, off_again):
    mask = (on == on_again).all(axis=-1) & (off == off_again).all(axis=-1)
    for _ in range(STILL_MARGIN):
        mask = _shrunk(mask)
    return mask


def _shrunk(mask):
    edged = np.pad(mask, 1, constant_values=True)
    h, w = mask.shape
    return np.logical_and.reduce(
        [edged[y : y + h, x : x + w] for y in range(3) for x in range(3)]
    )
