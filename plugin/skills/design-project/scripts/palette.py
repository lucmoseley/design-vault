#!/usr/bin/env python3
"""palette.py — measures a palette against a client's fixed colours: the ΔE00
between every pair of colours, each logo colour's lightness, and which grounds
the full-colour logo clears at 3:1 (design-vault#175). design-project step 2
writes its tables into a project's rules file, and the client-fit gate's
`<key>.colours-script` question is answered by its exit code.

USAGE
  python3 palette.py [--logo NAME=#HEX]… [--fixed NAME=#HEX]…
        [--colour NAME=#HEX]… [--surface NAME]… [--ground NAME=#HEX]…

--logo is a colour of the client's logo, fixed unless the client opened it;
--fixed any other colour the client fixed; --colour any other colour of the
palette, or of a candidate. --surface marks a --fixed or --colour colour as a
large area near the page ground that shares an edge with another (a page,
panel, card or layer); a logo colour never is one. --ground is a ground the
logo must sit on.

Each pair of colours is the same colour under ΔE00 2, a near-miss from 2 up to
its line, and apart from the line up. The line is 10, or 3 where both colours
are greys and both are surfaces (design-critique's vault.colour-distance record,
and the founder's rulings on #178). A full-colour logo clears a ground where
every logo colour reaches 3:1 against it.

EXITS 0 every --colour is a fixed colour exactly or past the line from each /
1 one is not, each printed with the way out / 2 the arguments are wrong.
Exits 0 and 1 print Markdown on stdout.
"""

import argparse
import os
import re
import sys
from collections import namedtuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from colour_space import (
    contrast,
    de2000,
    l_star_of_luminance,
    lab,
    luminance,
    oklch,
)

# CSS Color 4 §14.2.1: "using deltaE2000, one JND is 2".
SAME = 2.0
# The near-miss lines, founder rulings on #178 (docs/research/de00-thresholds.md, de00-greys.md).
NEAR_MISS = 10.0
NEAR_MISS_SURFACES = 3.0
# Two meanings in one view, founder ruling on #178: 10 for large areas, 20 for small marks.
MEANINGS_LARGE, MEANINGS_SMALL = 10.0, 20.0
# Borrowed, unmeasured: the top of the house text-tint range (design-critique's vault.text-tint record), so a
# grey tinted by that rule still takes the grey line. No source sets where a tinted grey stops being a grey.
GREY_CHROMA = 0.05
# WCAG's level for graphical objects, borrowed for a logo on its ground (vault.logo-ground).
LOGO_CONTRAST = 3.0

HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
ANCHORS = ("logo", "fixed")

Colour = namedtuple("Colour", "name hex source")


def is_grey(h):
    return oklch(h)[1] <= GREY_CHROMA


def pair_verdict(de, line):
    if de < SAME:
        return "same colour"
    return "near-miss" if de < line else "apart"


def meanings(de):
    if de >= MEANINGS_SMALL:
        return "large and small"
    return "large only" if de >= MEANINGS_LARGE else "neither"


def anchor_and_other(a, b):
    """(the fixed colour, the palette colour) where the pair is one of each, else None."""
    if a.source in ANCHORS and b.source == "palette":
        return a, b
    if b.source in ANCHORS and a.source == "palette":
        return b, a
    return None


def pairs(colours, surfaces):
    """Every pair of Colours in the order given, each { a, b, de, line, verdict, miss }; miss is the way out, or None."""
    out = []
    for i, a in enumerate(colours):
        for b in colours[i + 1 :]:
            both_surface_greys = all(
                c.name in surfaces and is_grey(c.hex) for c in (a, b)
            )
            line = NEAR_MISS_SURFACES if both_surface_greys else NEAR_MISS
            de = de2000(lab(a.hex), lab(b.hex))
            verdict = pair_verdict(de, line)
            anchored = anchor_and_other(a, b)
            miss = None
            if anchored and a.hex != b.hex and verdict != "apart":
                fixed, other = anchored
                miss = f"take {fixed.name}'s hex {fixed.hex}, or move {other.name} to ΔE00 {line:g} or more from it"
                if verdict == "same colour":
                    verdict += f": take {fixed.name}'s hex"
            out.append(
                {
                    "a": a,
                    "b": b,
                    "de": de,
                    "line": line,
                    "verdict": verdict,
                    "miss": miss,
                }
            )
    return out


def ground_limits(logo_hexes):
    """(lightest L* a dark ground may have, darkest L* a light ground may have) for every logo colour to reach 3:1; None where no ground can."""
    ys = [luminance(h) for h in logo_hexes]
    light = LOGO_CONTRAST * (max(ys) + 0.05) - 0.05
    dark = (min(ys) + 0.05) / LOGO_CONTRAST - 0.05
    return (
        l_star_of_luminance(dark) if dark >= 0 else None,
        l_star_of_luminance(light) if light <= 1 else None,
    )


def colour_arg(text):
    name, sep, h = text.partition("=")
    if not sep or not name or not HEX.match(h):
        raise argparse.ArgumentTypeError(f"{text!r} is not NAME=#RRGGBB")
    return name, h.upper()


def colour_table(colours, surfaces):
    lines = [
        "## Colours",
        "",
        "| Colour | Hex | From | L* | OKLCH | Grey |",
        "|---|---|---|---|---|---|",
    ]
    for c in colours:
        ok_l, ok_c, ok_h = oklch(c.hex)
        kind = "yes" if is_grey(c.hex) else "no"
        if c.name in surfaces:
            kind += ", surface"
        lines.append(
            f"| {c.name} | {c.hex} | {c.source} | {lab(c.hex)[0]:.1f} | {ok_l:.3f} {ok_c:.3f} {ok_h:.0f} | {kind} |"
        )
    return lines


def pair_table(found):
    lines = [
        "",
        "## ΔE00 between every pair",
        "",
        "| Pair | ΔE00 | Near-miss line | Verdict | Two meanings may share a view as |",
        "|---|---|---|---|---|",
    ]
    for p in found:
        lines.append(
            f"| {p['a'].name} / {p['b'].name} | {p['de']:.1f} | {p['line']:g} | {p['verdict']} | {meanings(p['de'])} |"
        )
    return lines


def logo_section(logos, grounds):
    stars = [lab(c.hex)[0] for c in logos]
    dark, light = ground_limits([c.hex for c in logos])
    light_text = (
        f"L* {light:.1f} or above"
        if light is not None
        else "no lightness: none is light enough"
    )
    dark_text = (
        f"L* {dark:.1f} or below"
        if dark is not None
        else "no lightness: none is dark enough"
    )
    lines = [
        "",
        "## The logo's lightness and grounds",
        "",
        (
            f"Lightness band: L* {min(stars):.1f} to {max(stars):.1f}, unweighted mean {sum(stars) / len(stars):.1f}, "
            f"over {len(stars)} logo colour(s)."
        ),
        f"A full-colour logo clears 3:1 on a light ground at {light_text}, and on a dark ground at {dark_text}.",
    ]
    if grounds:
        head = " | ".join(c.name for c in logos)
        lines += [
            "",
            f"| Ground | Hex | L* | {head} | Full colour |",
            "|---" * (len(logos) + 4) + "|",
        ]
        for g in grounds:
            ratios = [contrast(c.hex, g.hex) for c in logos]
            fails = [
                c.name for c, r in zip(logos, ratios, strict=True) if r < LOGO_CONTRAST
            ]
            verdict = (
                "fails: " + ", ".join(fails) + " under 3:1" if fails else "clears 3:1"
            )
            cells = " | ".join(f"{r:.2f}:1" for r in ratios)
            lines.append(
                f"| {g.name} | {g.hex} | {lab(g.hex)[0]:.1f} | {cells} | {verdict} |"
            )
    return lines


def report(colours, surfaces, grounds):
    """(the Markdown report, whether any palette colour misses a fixed colour)."""
    found = pairs(colours, surfaces)
    lines = colour_table(colours, surfaces)
    if found:
        lines += pair_table(found)
    logos = [c for c in colours if c.source == "logo"]
    if logos:
        lines += logo_section(logos, grounds)
    misses = [p for p in found if p["miss"]]
    lines.append("")
    for p in misses:
        lines.append(
            f"NEAR-MISS of a fixed colour: {p['a'].name} / {p['b'].name}, ΔE00 {p['de']:.1f}: {p['miss']}."
        )
    if not misses:
        lines.append("No palette colour is a near-miss of a fixed colour.")
    return "\n".join(lines), bool(misses)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    for source in ("logo", "fixed", "colour"):
        ap.add_argument(f"--{source}", type=colour_arg, action="append", default=[])
    ap.add_argument("--surface", action="append", default=[])
    ap.add_argument("--ground", type=colour_arg, action="append", default=[])
    args = ap.parse_args(argv)
    colours = (
        [Colour(n, h, "logo") for n, h in args.logo]
        + [Colour(n, h, "fixed") for n, h in args.fixed]
        + [Colour(n, h, "palette") for n, h in args.colour]
    )
    names = [c.name for c in colours]
    if not names:
        ap.error("give at least one --logo, --fixed or --colour")
    if len(set(names)) != len(names):
        ap.error("each colour needs its own name")
    unknown = sorted(set(args.surface) - set(names))
    if unknown:
        ap.error("--surface names no --fixed or --colour: " + ", ".join(unknown))
    logo_surfaces = sorted(set(args.surface) & {n for n, _ in args.logo})
    if logo_surfaces:
        ap.error(
            "--surface names a logo colour, which is a mark, never a surface: "
            + ", ".join(logo_surfaces)
        )
    if args.ground and not args.logo:
        ap.error("--ground needs a --logo to measure against")
    grounds = [Colour(n, h, "ground") for n, h in args.ground]
    text, missed = report(colours, set(args.surface), grounds)
    print(text)
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
