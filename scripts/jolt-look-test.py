#!/usr/bin/env python3
"""jolt-look-test.py — the jolt look test's review page data (#196).

check-flow.py called a move from rest a jolt when its first or last frame ran
at 0.5 or more of its top speed, #60's builder's guess: no source gives the
share of top speed at which a start looks abrupt, and measured limits of the
eye put it lower for longer moves (docs/research/jolt-onset.md), so the founder
was to set it by eye. #221 Q1 (B) set it from that research instead, as
check-flow.py's JOLT_BAND (#297), and this test was retired unmarked. This
script builds that look: one move, played over and over, that starts from rest
already going at each share in SHARES of its top speed and always stops
smoothly, one lane per share and per move length in SETS, in a single picture
above the cards, all on one clock (#221).

USAGE
  python3 scripts/jolt-look-test.py OUT_DIR
Writes OUT_DIR/items.json and OUT_DIR/img/lanes.svg for plugin/review-page, and
prints each card's measured start share and the key from card id to share,
which the page withholds. Exits 1 if a card's share lands more than TOLERANCE
from its target, and 2 on a usage error.
"""

import collections
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "check_flow",
    os.path.join(
        HERE, "..", "plugin", "skills", "design-round", "scripts", "check-flow.py"
    ),
)
flow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flow)

# The start speeds #196 names, as shares of the move's top speed, either side of check-flow's 0.5.
SHARES = (0, 0.1, 0.25, 0.5, 0.75)
# A first frame averages the speed over 1/60 s, so it reads a little over the start speed, and further over in a
# shorter move, where that 1/60 s is more of the move: TOLERANCE at a 1 s move, scaled inversely with length; a guess.
TOLERANCE = 0.04
# The move's distance in px, and the share of its time spent gaining speed: picked by eye as one plain move across
# a lane.
DISTANCE = 520
RISE = 0.35
# The two sets: a heading, the move's length in ms, and the lane order from the top, lettered, so neither the page
# nor a card id tells him which share he is marking. Two lengths because the share a viewer can tell from a smooth
# start falls as a move lengthens (docs/research/jolt-onset.md, derivation): 1 s and 0.4 s span a brand piece's
# moves, picked from that table, not measured.
Set = collections.namedtuple("Set", "heading move_ms letters shown")
SETS = (
    Set("Slower move, 1 second", 1000, "ABCDE", (0.25, 0, 0.75, 0.1, 0.5)),
    Set("Quicker move, 0.4 seconds", 400, "FGHIJ", (0.5, 0.1, 0, 0.75, 0.25)),
)
# Still before the move and after it, a fade out and back, and a blank gap, in ms: picked by eye so each start
# is seen from a clear rest.
REST_MS, HOLD_MS, FADE_MS, GAP_MS = 600, 800, 200, 400
# Keyframe stops across the move: a guess at enough that the linear steps between them never show.
STOPS = 240
# The picture's width, each lane's height, the space above and below the lanes, the dots' start line and radius,
# the track's gap below a dot, and each set's heading row, in px: picked by eye.
WIDTH, LANE, PAD, LEFT, R, TRACK_GAP, HEAD = 640, 64, 16, 60, 14, 5, 40
# Each lane's letter: its size and weight, and how far left of the gutter's middle it sits, in px: picked by eye.
LETTER_PX, LETTER_WEIGHT, LETTER_NUDGE = 20, 600, 4
# A set's heading size, and the start line's width, in px: picked by eye, the line fainter than the tracks.
HEAD_PX = 15
START_LINE_PX = 1


def speed(share, u):
    """The move's speed at progress u of its time, as a share of its top: it
    starts at `share`, gains to 1 over RISE on a quarter sine, and eases to 0."""
    if u < RISE:
        return share + (1 - share) * math.sin(math.pi / 2 * u / RISE)
    return (1 + math.cos(math.pi * (u - RISE) / (1 - RISE))) / 2


def travel(share):
    """Progress 0..1 of distance at each of STOPS + 1 even times, by Simpson's rule on speed()."""
    n = 64  # Simpson steps per stop: a guess, far finer than the stops.
    done = [0.0]
    for k in range(STOPS):
        a, b = k / STOPS, (k + 1) / STOPS
        h = (b - a) / n
        s = speed(share, a) + speed(share, b)
        s += sum((4 if i % 2 else 2) * speed(share, a + i * h) for i in range(1, n))
        done.append(done[-1] + s * h / 3)
    return [d / done[-1] for d in done]


def measured(share, move_ms):
    """check-flow's share of top speed at the move's first frame, at 60 fps from rest."""
    progress = travel(share)
    step = 1000 / flow.FPS
    times = [k * step for k in range(round((REST_MS + move_ms + HOLD_MS) / step) + 1)]

    def at(t):
        u = min(1, max(0, (t - REST_MS) / move_ms)) * STOPS
        i = min(int(u), STOPS - 1)
        return [DISTANCE * (progress[i] + (progress[i + 1] - progress[i]) * (u - i)), 0]

    el = {"label": "dot", "channels": {"position": [at(t) for t in times]}}
    # With the jolt line at nothing, every start from rest reports its share.
    r = flow.analyse({"times": times, "elements": [el]}, jolt_ratio=1e-9)
    return next(j["share"] for j in r["jolts"] if j["edge"] == "starts")


def svg():
    """Every lane in one picture, each set under its heading, each lane a dot resting on a track, moving across,
    resting, fading, and again. One picture keeps one clock, so all set off together from one start line to compare
    (#221). Residual: seen side by side, a mark may rank a lane against the others rather than judge it alone."""
    longest = max(s.move_ms for s in SETS)
    loop = FADE_MS + REST_MS + longest + HOLD_MS + FADE_MS + GAP_MS

    def pct(ms):
        return f"{100 * ms / loop:.4f}%"

    start = FADE_MS + REST_MS
    end = start + longest + HOLD_MS
    fades = [
        "0% { opacity: 0 }",
        f"{pct(FADE_MS)} {{ opacity: 1 }}",
        f"{pct(end)} {{ opacity: 1 }}",
        f"{pct(end + FADE_MS)} {{ opacity: 0 }}",
        "100% { opacity: 0 }",
    ]
    styles, parts, y0, n = [f"@keyframes fade {{ {' '.join(fades)} }}"], [], PAD, 0
    for s in SETS:
        parts.append(
            f'<text x="{LEFT}" y="{y0 + HEAD / 2}" dominant-baseline="central" font-family="system-ui, sans-serif" '
            f'font-size="{HEAD_PX}" font-weight="{LETTER_WEIGHT}" fill="#4b5563">{s.heading}</text>'
        )
        y0 += HEAD
        for letter, share in zip(s.letters, s.shown, strict=True):
            moves = [
                "0% { transform: translateX(0) }",
                f"{pct(start)} {{ transform: translateX(0) }}",
            ]
            for k, p in enumerate(travel(share)):
                moves.append(
                    f"{pct(start + s.move_ms * k / STOPS)} {{ transform: translateX({DISTANCE * p:.3f}px) }}"
                )
            moves.append(f"100% {{ transform: translateX({DISTANCE}px) }}")
            styles.append(f"@keyframes move-{n} {{ {' '.join(moves)} }}")
            styles.append(
                f".dot-{n} {{ animation: move-{n} {loop}ms linear infinite, fade {loop}ms linear infinite; }}"
            )
            y = y0 + LANE / 2
            track = y + R + TRACK_GAP
            parts.append(
                f"""<text x="{LEFT / 2 - LETTER_NUDGE}" y="{y}" dominant-baseline="central" text-anchor="middle" font-family="system-ui, sans-serif" font-size="{LETTER_PX}" font-weight="{LETTER_WEIGHT}" fill="#1f2937">{letter}</text>
<line x1="{LEFT}" y1="{track}" x2="{LEFT + DISTANCE}" y2="{track}" stroke="#d4d4cf" stroke-width="2"/>
<line x1="{LEFT}" y1="{y0}" x2="{LEFT}" y2="{y0 + LANE}" stroke="#e4e4df" stroke-width="{START_LINE_PX}"/>
<circle class="dot-{n}" cx="{LEFT}" cy="{y}" r="{R}" fill="#1f2937"/>"""
            )
            y0 += LANE
            n += 1
    height = y0 + PAD
    nl = "\n"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" width="{WIDTH}" height="{height}">
<style>
{nl.join(styles)}
</style>
<rect width="{WIDTH}" height="{height}" fill="#fafaf7"/>
{nl.join(parts)}
</svg>
"""


def main(argv):
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    out = argv[0]
    os.makedirs(os.path.join(out, "img"), exist_ok=True)
    got, failed = {}, False
    for s in SETS:
        for share in SHARES:
            got[s.move_ms, share] = measured(share, s.move_ms)
            failed |= abs(got[s.move_ms, share] - share) > TOLERANCE * 1000 / s.move_ms
            print(
                f"{s.move_ms} ms, start {share:.0%} of top speed: measured {got[s.move_ms, share]:.0%}"
            )
    if failed:
        print(
            "a card's start landed further from its target than TOLERANCE allows",
            file=sys.stderr,
        )
        return 1

    with open(os.path.join(out, "img", "lanes.svg"), "w") as f:
        f.write(svg())
    items = []
    for s in SETS:
        for letter, share in zip(s.letters, s.shown, strict=True):
            iid = f"start-{letter.lower()}"
            items.append({"id": iid, "name": f"Start {letter}", "line": s.heading})
            print(
                f"key: {iid}, {s.move_ms} ms, starts at {got[s.move_ms, share]:.0%} of its top speed"
            )
    data = {
        "title": "When does a start look like a jolt?",
        "intro": (
            "Ten dots play over and over, all together from one start line: each rests, sets off across, and comes "
            "to a smooth stop. A to E make one slower move, F to J one quicker move. Within a set, every dot "
            "crosses the same distance in the same time; they differ only in how fast the dot is already going at "
            "the moment it sets off. Each set is shuffled, and the page does not say which is which.\n\n"
            "The motion check called a start a jolt when the first moment of a move ran at half its top speed or "
            "more. Half was a builder's guess. No study gives the line, but measured limits of the eye suggest a "
            "fast start shows more in a slower move than in a quicker one, hence the two sets.\n\n"
            "Watch a few starts, then mark each lane's card below by how its start looks to you."
        ),
        "figure": "img/lanes.svg",
        "figureAlt": "Ten dots in two sets, lettered A to J, each moving across its own lane from one start line.",
        "marks": [
            {"id": "smooth", "label": "Smooth start", "tone": "yes"},
            {"id": "brisk", "label": "Brisk, but fine"},
            {"id": "jolt", "label": "A jolt", "tone": "no"},
        ],
        "pageNote": "Anything about the set as a whole? Once every card is marked, Claude shows you how fast each "
        "card starts and proposes the line from your marks.",
        "items": items,
    }
    with open(os.path.join(out, "items.json"), "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
