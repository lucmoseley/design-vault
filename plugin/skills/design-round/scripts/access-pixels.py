"""access-pixels.py — the pixel maths check-access.py measures a screenshot
with. A module of its own so its tests call what check-access.py calls, not
the script's insides (#198).

A screenshot is an array of rows of 0–255 RGB; an ink mask, of rows of
booleans, True where a glyph covers the pixel; a box is [left, top, right,
bottom] in their pixels.
"""

import collections

import numpy as np

# The figures a text is held to: its ratio as body or large text, and where large
# text starts, `large_px`, or `large_bold_px` at weight `bold` or more. Each
# comes from check-access-contrast.table's line for its record (#316).
Floors = collections.namedtuple("Floors", "body large large_px large_bold_px bold")
# Computed sizes carry float rounding: this much under a figure meets it. A
# guess, unmeasured.
PX_SLACK = 0.05
# The share of the pixels behind a text's glyphs allowed to fall below the
# needed contrast: none, as WCAG F83 allows none behind a letter (#197). Its
# whole line box is no measure: a glyph box overhangs a tight button or band.
WORST_SHARE = 0
# The thickest line drawn in the text's own colour that is read as a stroke
# crossing its glyphs, a rule or an underline, rather than as their ground: it
# and the pixels its edge blends into are left out (#257). A patch thicker than
# this hides the letters under it and is read. A guess, unmeasured.
STROKE_PX = 3
# How far past such a line its edge blends into the ground, in px: one pixel of
# antialiasing. A guess, unmeasured; a line tilted at a shallow angle blends
# wider.
BLEND_PX = 1
# A pixel whose channels move more than this between two screenshots has
# changed. A guess, unmeasured: above a codec's or a resampler's jitter.
PAINT_NOISE = 8
# How far a pixel may sit from the text's colour, on each 0–255 channel, and be
# that colour. A guess, unmeasured.
OWN_COLOUR = 8
# The lines read as a control's edge: 2 px outside the box to 3 px inside it.
EDGE_LINES = range(-2, 3)
# Below this change against what is behind it a box draws no edge or fill at
# all, and the next box out is read instead (#197). A guess, unmeasured
# (house-audit-constants.md A1).
DRAWN = 1.02
# How far inside a control its fill is read, past its border. A guess,
# unmeasured: the fill is a median, so a thin border inside it barely moves it.
FILL_INSET = 4
# WCAG 1.4.11 asks a focus indicator for 3:1 against the colours next to it.
# Measured as 2.4.13 (AAA) measures it, by the change between the unfocused
# and focused states: a pixel the focus changes by this much counts.
FOCUS_RATIO = 3.0
# How far from a pixel that moves by itself a pixel is not still either, in px.
# Noise can match itself across both pairs of shots, so a pixel counts as still
# only where its neighbours match too. At 1 px, a pixel on a flickering
# canvas's edge passed as still in 50 of 600 tries; at 2 px, in none (#222).
# Residual: a corner pixel's 5x5 holds only 9 of a canvas's noise pixels, so
# its four corners still pass one about once in 130,000 tries; and a ring
# within 2 px of moving content is not counted there.
STILL_MARGIN = 2


def luminance(rgb):
    """WCAG's relative luminance of sRGB values 0–255, over the last axis."""
    c = np.asarray(rgb, dtype=float) / 255
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return lin @ np.array([0.2126, 0.7152, 0.0722])


def large(size, weight, floors):
    """Large text by `floors`, WCAG 1.4.3's 18 pt, or 14 pt bold, in vault.contrast's."""
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
    """`test` (np.all or np.any) over each k x k square of `padded`, by its top left."""
    return test(np.lib.stride_tricks.sliding_window_view(padded, (k, k)), axis=(-2, -1))


def _strokes(shot, rect, rgb):
    """Which of the pixels in `rect` lie on, or BLEND_PX beside, a line in
    colour `rgb` no thicker than STROKE_PX. Read from a margin around the box, so a
    patch the box cuts to a thin strip is still a patch."""
    k = STROKE_PX + 1
    left, top, right, bottom = _bounds(shot, rect)
    if right == left or bottom == top:
        return np.zeros((bottom - top, right - left), dtype=bool)
    outer = _bounds(shot, [left - k, top - k, right + k, bottom + k])
    outer_left, outer_top = outer[:2]
    own = (np.abs(_window(shot, outer).astype(int) - rgb) <= OWN_COLOUR).all(axis=-1)
    # A patch is the union of the k x k squares that fit wholly in the colour.
    fits = _slide(np.pad(own, ((0, k - 1), (0, k - 1))), k, np.all)
    patch = _slide(np.pad(fits, ((k - 1, 0), (k - 1, 0))), k, np.any)
    near = _slide(np.pad(own & ~patch, BLEND_PX), 2 * BLEND_PX + 1, np.any)
    return near[
        top - outer_top : bottom - outer_top, left - outer_left : right - outer_left
    ]


def pixels(shot, rect):
    """The screenshot's pixels inside a [left, top, right, bottom] box, as rows of RGB."""
    return _window(shot, rect).reshape(-1, 3).astype(float)


def ink_mask(back, black, white):
    """Which of `back`'s pixels a glyph covers: those that differ with the text drawn black and then white. A shot
    that came out another size counts every pixel, so the text's whole box is read."""
    if not back.shape == black.shape == white.shape:
        return np.ones(back.shape[:2], dtype=bool)
    return (black != white).any(axis=-1)


def _meet(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def text_contrast(shot, ink, text, floors, *, held=()):
    """(fault detail or None, reason it cannot be measured or None) for one text entry, held to `floors`. `held` are
    the boxes of text whose fill the page holds with its own !important rule: the screenshots cannot take it off or
    recolour it."""
    if text["why"]:
        return None, f"{text['subject']} {text['why']}"
    if any(_meet(r, h) for r in text["rects"] for h in held):
        return (
            None,
            f"{text['subject']} holds its own fill, which the check cannot take off",
        )
    *rgb, alpha = text["color"]
    masks = [_window(ink, r).reshape(-1) for r in text["rects"]]
    # A stroke in the text's own colour reads 1:1 wherever it crosses a glyph,
    # yet the glyph still reads against the ground either side of it. Where
    # such lines lie under every glyph pixel, a hatch or a close ruling, there
    # is no ground beside them, and all of it is read.
    kept = [
        m & ~_strokes(shot, r, rgb).reshape(-1)
        for r, m in zip(text["rects"], masks, strict=True)
    ]
    if any(k.any() for k in kept):
        masks = kept
    if not any(m.size for m in masks):
        return None, f"{text['subject']} lies off the screenshot"
    behind = np.concatenate(
        [pixels(shot, r)[m] for r, m in zip(text["rects"], masks, strict=True)]
    )
    if not len(behind):
        return None, None  # covered or clipped: no glyph shows, so none to read
    seen = alpha * np.array(rgb, dtype=float) + (1 - alpha) * behind
    ratios = contrast(seen, behind)
    worst = float(np.percentile(ratios, WORST_SHARE))
    need = floors.large if large(text["size"], text["weight"], floors) else floors.body
    if worst >= need:
        return None, None
    i = int(np.argmin(np.abs(ratios - worst)))
    size = f"{text['size']:g} px{' bold' if text['weight'] >= floors.bold else ''}"
    return (
        f"is {worst:.2f}:1 against {hexed(behind[i])} behind it; {need:g}:1 needed ({hexed(seen[i])} text, {size})",
        None,
    )


def side_lines(rect, side, offset):
    """One line of pixels along a side of a box, `offset` px inward (negative is
    outside), over the middle half of that side so a rounded corner is skipped."""
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
    """The Reading of a box: the best contrast a line along its edge, or its fill, shows against the same pixels in
    `behind`, a shot with the box hidden, with that colour; or None where none of them lies on both shots."""
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
    """A box grown to the furthest line read outside it as its edge."""
    out = -min(EDGE_LINES)
    return [rect[0] - out, rect[1] - out, rect[2] + out, rect[3] + out]


def hide_groups(controls):
    """A group number for each control, its boxes outermost last, so no two controls whose boxes' reach() meet share
    one: each group is hidden in a shot of its own, and a control flush against another reads that one's edge in
    both shots, not as its own (#220)."""
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
    """Whether any pixel inside `rect` differs between two shots of the page in one state, read where both reach."""
    a, b = _window(shot, rect), _window(again, rect)
    h, w = min(a.shape[0], b.shape[0]), min(a.shape[1], b.shape[1])
    return bool((a[:h, :w] != b[:h, :w]).any())


Edge = collections.namedtuple("Edge", "box ratio behind")


def control_edge(shot, behind, boxes):
    """The Edge of the innermost box around a control that draws one, box i read against behind[i], a shot with that
    box hidden; an Edge of Nones where no box draws an edge or fill; None where the control lies off the screenshot."""
    for i, b in enumerate(boxes):
        best = edge_contrast(shot, behind[i], b["rect"])
        if best is None and i == 0:
            return None
        if best is not None and best.ratio >= DRAWN:
            return Edge(b, best.ratio, best.behind)
    return Edge(None, None, None)


def focus_changed(on, off, region, still):
    """How many pixels in a [left, top, right, bottom] box changed by
    FOCUS_RATIO or more between two shots, of those `still` marks True."""
    a, b = pixels(on, region), pixels(off, region)
    if not len(a):
        return 0
    keep = pixels(np.repeat(still[..., None], 3, axis=-1), region)[:, 0].astype(bool)
    return int(np.count_nonzero((contrast(a, b) >= FOCUS_RATIO) & keep))


def still_pixels(on, off, on_again, off_again):
    """Which pixels hold still across two shots of each state: the same in
    both, with none within STILL_MARGIN px that differs."""
    mask = (on == on_again).all(axis=-1) & (off == off_again).all(axis=-1)
    for _ in range(STILL_MARGIN):
        mask = _shrunk(mask)
    return mask


def _shrunk(mask):
    """`mask` with every pixel next to a False one made False too."""
    edged = np.pad(mask, 1, constant_values=True)
    h, w = mask.shape
    return np.logical_and.reduce(
        [edged[y : y + h, x : x + w] for y in range(3) for x in range(3)]
    )
