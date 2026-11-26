"""Usage, from a scratch environment after `pip install fonttools brotli`:

  python make-net-fonts.py <this directory>

Writes good.woff2, plain.ttf and flex.woff into that directory.
"""

import pathlib
import sys

from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

UPM = 1000
CAPS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
NAMES = {
    **{c: c for c in CAPS + LOWER},
    **{
        d: n
        for d, n in zip(
            DIGITS,
            "zero one two three four five six seven eight nine".split(),
            strict=True,
        )
    },
    " ": "space",
    ".": "period",
    ",": "comma",
    "-": "hyphen",
    ":": "colon",
    "'": "quotesingle",
    "é": "eacute",
}
STEM = 90


def shape(*rects):
    pen = TTGlyphPen(None)
    for x0, y0, x1, y1 in rects:
        pen.moveTo((x0, y0))
        pen.lineTo((x0, y1))
        pen.lineTo((x1, y1))
        pen.lineTo((x1, y0))
        pen.closePath()
    return pen.glyph()


def bar(advance, height, left=None):
    x = (advance - STEM) // 2 if left is None else left
    return (x, 0, x + STEM, height)


def outlines(*, distinct, tabular, accent):
    out = {".notdef": (500, []), "space": (250, [])}
    for i, c in enumerate(CAPS):
        w = 560 + (i % 4) * 40
        out[c] = (w, [bar(w, 700), (60, 0, w - 60, 80)])
    for i, c in enumerate(LOWER):
        w = 460 + (i % 3) * 40
        out[c] = (w, [bar(w, 500), (60, 420, w - 60, 500)])
    for d in DIGITS:
        w = 550 if tabular or d != "1" else 300
        out[NAMES[d]] = (w, [bar(w, 700), (60, 620, w - 60, 700), (60, 0, w - 60, 80)])
    if distinct:
        out["I"] = (400, [bar(400, 700), (80, 0, 320, 70), (80, 630, 320, 700)])
        out["l"] = (360, [bar(360, 750, 100), (100, 0, 300, 70)])
        out["one"] = (550, [bar(550, 700), (130, 560, 230, 640), (130, 0, 420, 70)])
    else:
        out["I"] = (360, [bar(360, 700)])
        out["l"] = (360, [bar(360, 700)])
        out["one"] = (out["one"][0], [bar(out["one"][0], 700), (60, 560, 160, 640)])
    for name, rects in (
        ("period", [(100, 0, 200, 100)]),
        ("comma", [(100, -100, 200, 100)]),
        ("hyphen", [(60, 300, 290, 380)]),
        ("colon", [(100, 0, 200, 100), (100, 400, 200, 500)]),
        ("quotesingle", [(100, 500, 190, 700)]),
    ):
        out[name] = (300, rects)
    if accent:
        out["eacute"] = (
            500,
            [bar(500, 500), (60, 420, 440, 500), (200, 560, 300, 680)],
        )
    return out


def build(path, family, *, distinct, tabular, accent, features, axes=None):
    glyphs = outlines(distinct=distinct, tabular=tabular, accent=accent)
    if "smcp" in features:
        for c in LOWER:
            glyphs[f"{c}.sc"] = (520, [bar(520, 560), (60, 480, 460, 560)])
    if "ss01" in features:
        glyphs["a.ss01"] = (480, [bar(480, 500), (60, 0, 420, 80)])
    order = list(glyphs)
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({ord(ch): n for ch, n in NAMES.items() if n in glyphs})
    fb.setupGlyf({n: shape(*glyphs[n][1]) for n in order})
    fb.setupHorizontalMetrics(
        {n: (glyphs[n][0], min((r[0] for r in glyphs[n][1]), default=0)) for n in order}
    )
    fb.setupHorizontalHeader(ascent=900, descent=-250)
    fb.setupNameTable(
        {
            "familyName": family,
            "styleName": "Regular",
            "psName": family.replace(" ", "") + "-Regular",
        }
    )
    fb.setupOS2(
        version=4,
        sTypoAscender=900,
        sTypoDescender=-250,
        usWinAscent=900,
        usWinDescent=250,
        sxHeight=500,
        sCapHeight=700,
    )
    fb.setupPost()
    if axes:
        fb.setupFvar([(tag, lo, default, hi, tag) for tag, lo, default, hi in axes], [])
        fb.setupGvar({n: [] for n in order})
    fea = []
    if "smcp" in features:
        fea.append(
            "feature smcp { "
            + " ".join(f"sub {c} by {c}.sc;" for c in LOWER)
            + " } smcp;"
        )
    if "c2sc" in features:
        fea.append(
            "feature c2sc { "
            + " ".join(f"sub {c} by {c.lower()}.sc;" for c in CAPS)
            + " } c2sc;"
        )
    if "ss01" in features:
        fea.append("feature ss01 { sub a by a.ss01; } ss01;")
    if fea:
        addOpenTypeFeaturesFromString(fb.font, "\n".join(fea))
    suffix = pathlib.Path(path).suffix
    if suffix in (".woff", ".woff2"):
        fb.font.flavor = suffix[1:]
    fb.save(path)


def main(where):
    here = pathlib.Path(where)
    build(
        str(here / "good.woff2"),
        "Net Good",
        distinct=True,
        tabular=True,
        accent=True,
        features=("smcp", "c2sc", "ss01"),
    )
    build(
        str(here / "plain.ttf"),
        "Net Plain",
        distinct=False,
        tabular=False,
        accent=False,
        features=(),
    )
    build(
        str(here / "flex.woff"),
        "Net Flex",
        distinct=True,
        tabular=True,
        accent=True,
        features=(),
        axes=[("wght", 100, 400, 900), ("opsz", 8, 14, 144)],
    )


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent)
