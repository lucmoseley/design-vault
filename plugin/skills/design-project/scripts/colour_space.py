import math

D65_WHITE = (0.95047, 1.0, 1.08883)
SRGB_TO_XYZ = (
    (0.4124564, 0.3575761, 0.1804375),
    (0.2126729, 0.7151522, 0.0721750),
    (0.0193339, 0.1191920, 0.9503041),
)


# WCAG's relative luminance weights: https://www.w3.org/TR/WCAG22/#dfn-relative-luminance
WCAG_Y = (0.2126, 0.7152, 0.0722)
# WCAG's contrast ratio adds 0.05 to each luminance for viewing flare: https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio
FLARE = 0.05


def _pick(test, yes, no):
    if getattr(test, "ndim", 0) == 0:
        return yes if test else no
    import numpy as np

    return np.where(test, yes, no)


def _one(c):
    return isinstance(c, (tuple, list))


def hex_rgb(h):
    return tuple(int(h[i : i + 2], 16) for i in (1, 3, 5))


def _rgb(c):
    return hex_rgb(c) if isinstance(c, str) else c


def lin(c):
    return _pick(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_rgb(h):
    return [lin(v / 255) for v in hex_rgb(h)]


def linear_luminance(linear):
    if _one(linear):
        return sum(w * c for w, c in zip(WCAG_Y, linear, strict=True))
    import numpy as np

    return np.asarray(linear) @ np.array(WCAG_Y)


def luminance(c):
    c = _rgb(c)
    if _one(c):
        return linear_luminance([lin(v / 255) for v in c])
    import numpy as np

    return linear_luminance(lin(np.asarray(c, dtype=float) / 255))


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    lighter = la >= lb
    return (_pick(lighter, la, lb) + FLARE) / (_pick(lighter, lb, la) + FLARE)


def lighter_by(y, ratio):
    return ratio * (y + FLARE) - FLARE


def darker_by(y, ratio):
    return (y + FLARE) / ratio - FLARE


def f_lab(t):
    return t ** (1 / 3) if t > (6 / 29) ** 3 else t / (3 * (6 / 29) ** 2) + 4 / 29


def lab(h):
    rgb = linear_rgb(h)
    fx, fy, fz = (
        f_lab(sum(m * c for m, c in zip(row, rgb, strict=True)) / w)
        for row, w in zip(SRGB_TO_XYZ, D65_WHITE, strict=True)
    )
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def l_star_of_luminance(y):
    return 116 * f_lab(y) - 16


# OKLab's two matrices, as Ottosson publishes them: https://bottosson.github.io/posts/oklab/
def oklch(c):
    r, g, b = (lin(float(v) / 255) for v in _rgb(c))
    long_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    medium = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    short = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    lightness = 0.2104542553 * long_ + 0.7936177850 * medium - 0.0040720468 * short
    ok_a = 1.9779984951 * long_ - 2.4285922050 * medium + 0.4505937099 * short
    ok_b = 0.0259040371 * long_ + 0.7827717662 * medium - 0.8086757660 * short
    return (
        lightness,
        math.hypot(ok_a, ok_b),
        math.degrees(math.atan2(ok_b, ok_a)) % 360,
    )


# The CIEDE2000 difference, as Sharma, Wu and Dalal give it: https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/
def de2000(lab1, lab2):
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    c_bar = (math.hypot(a1, b1) + math.hypot(a2, b2)) / 2
    g = 0.5 * (1 - math.sqrt(c_bar**7 / (c_bar**7 + 25**7)))
    a1p, a2p = (1 + g) * a1, (1 + g) * a2
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = 0 if (a1p == 0 and b1 == 0) else math.degrees(math.atan2(b1, a1p)) % 360
    h2p = 0 if (a2p == 0 and b2 == 0) else math.degrees(math.atan2(b2, a2p)) % 360
    dlp, dcp = l2 - l1, c2p - c1p
    dh_angle = 0 if c1p * c2p == 0 else (h2p - h1p + 180) % 360 - 180
    d_hue = 2 * math.sqrt(c1p * c2p) * math.sin(math.radians(dh_angle / 2))
    lbp, cbp = (l1 + l2) / 2, (c1p + c2p) / 2
    if c1p * c2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    else:
        hbp = (h1p + h2p + (360 if h1p + h2p < 360 else -360)) / 2
    t_hue = (
        1
        - 0.17 * math.cos(math.radians(hbp - 30))
        + 0.24 * math.cos(math.radians(2 * hbp))
        + 0.32 * math.cos(math.radians(3 * hbp + 6))
        - 0.20 * math.cos(math.radians(4 * hbp - 63))
    )
    dth = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    rc = 2 * math.sqrt(cbp**7 / (cbp**7 + 25**7))
    sl = 1 + 0.015 * (lbp - 50) ** 2 / math.sqrt(20 + (lbp - 50) ** 2)
    sc = 1 + 0.045 * cbp
    sh = 1 + 0.015 * cbp * t_hue
    rt = -math.sin(math.radians(2 * dth)) * rc
    return math.sqrt(
        (dlp / sl) ** 2
        + (dcp / sc) ** 2
        + (d_hue / sh) ** 2
        + rt * (dcp / sc) * (d_hue / sh)
    )
