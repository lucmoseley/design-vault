"""pip install fonttools
python make-fonts.py <this directory>
"""

import pathlib
import sys

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables.TupleVariation import TupleVariation

UPM = 1000
LETTERS = "abcdefghijklmnopqrstuvwxyz"
SPACE = 250


def bar(advance, stem, height):
    pen = TTGlyphPen(None)
    left = (advance - stem) / 2
    pen.moveTo((left, 0))
    pen.lineTo((left, height))
    pen.lineTo((left + stem, height))
    pen.lineTo((left + stem, 0))
    pen.closePath()
    return pen.glyph()


def empty():
    pen = TTGlyphPen(None)
    return pen.glyph()


def build(path, family, *, advance, stem, xheight, axes=None):
    names = [".notdef", "space", *LETTERS]
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap({32: "space", **{ord(c): c for c in LETTERS}})
    glyphs = {".notdef": empty(), "space": empty()}
    for c in LETTERS:
        glyphs[c] = bar(advance, stem, 700 if c == "l" else xheight)
    fb.setupGlyf(glyphs)
    metrics = {".notdef": (advance, 0), "space": (SPACE, 0)}
    for c in LETTERS:
        metrics[c] = (advance, (advance - stem) // 2)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": family, "styleName": "Regular"})
    fb.setupOS2(
        version=4,
        sTypoAscender=800,
        sTypoDescender=-200,
        usWinAscent=800,
        usWinDescent=200,
        sxHeight=xheight,
        sCapHeight=700,
    )
    fb.setupPost()
    if axes:
        fb.setupFvar([(tag, lo, default, hi, tag) for tag, lo, default, hi in axes], [])
        fb.setupGvar(variations())
    fb.save(path)


def deltas(wide, thick):
    left = (wide - thick) // 2
    right = (wide + thick) // 2
    return [
        (left, 0),
        (left, 0),
        (right, 0),
        (right, 0),
        (0, 0),
        (wide, 0),
        (0, 0),
        (0, 0),
    ]


def variations():
    moves = [
        ("wght", 1.0, 50, 100),
        ("wght", -1.0, 0, -60),
        ("wdth", 1.0, 100, 0),
        ("wdth", -1.0, -100, 0),
        ("opsz", -1.0, 60, 0),
        ("opsz", 1.0, -40, -20),
        ("GRAD", 1.0, 0, 40),
        ("GRAD", -1.0, 0, -40),
    ]
    out = {".notdef": [], "space": []}
    for c in LETTERS:
        out[c] = [
            TupleVariation(
                {axis: (min(0, peak), peak, max(0, peak))},
                deltas(wide, thick),
            )
            for axis, peak, wide, thick in moves
        ]
    return out


def main(where):
    here = pathlib.Path(where)
    build(
        str(here / "flex.ttf"),
        "Fixture Flex",
        advance=500,
        stem=100,
        xheight=500,
        axes=[
            ("wght", 100, 400, 900),
            ("wdth", 75, 100, 125),
            ("opsz", 8, 14, 144),
            ("GRAD", -200, 0, 150),
        ],
    )
    build(str(here / "plain.ttf"), "Fixture Plain", advance=450, stem=60, xheight=400)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent)
