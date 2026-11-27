import bisect
import itertools
import json
import math
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402
from fail_open import expected  # noqa: E402

runner = siblings.load(HERE, "runner.py")

with open(os.path.join(HERE, "flow-pace.json"), encoding="utf8") as f:
    SHARED = {k: v["value"] for k, v in json.load(f).items()}

PAUSE_MS = 250  # guess, #60
JOLT_BAND = tuple(tuple(row) for row in SHARED["joltBand"])
JUMP_DEG = SHARED["jumpDeg"]
FPS = 60  # guess, #141
MIN_GAP_MS = 1  # guess, #126
MERGE_FRAMES = 1  # guess, #632
FRAME_SLACK = 1e-9  # guess, #632
STILL_FRACTION = SHARED["stillFraction"]
STILL_ARCMIN_S = SHARED["stillArcminS"]
VIEW_CM = SHARED["viewCm"]
CSS_PX_CM = 2.54 / 96
NOISE = 0.02  # guess, #60
PX_NOISE = 5e-4  # measured 1.2e-4 px float wobble, 1e-3 px least move, #149
PX_CHANNELS = ("position", "size")
IDENTITY_3D = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
STEP_RATIO = 1.3  # measured: a Weber fraction of 0.2-0.3, #196
STEP_SPREAD = 3  # guess, #196
STEP_SIDE_FRAMES = 3  # guess, #196
STEP_HOLD = 1.3  # guess, #196
STEP_FAST_HOLD = 1.5  # guess, #196
STEP_FLOOR = 0.2  # guess, #196
TURN_FRAMES = 2  # guess, #151
DROPPED_FRAMES = 2  # guess, #126
BROWSER_FRAME_MS = 1000 / 60
NUMBER = re.compile(r"(?<![A-Za-z_])[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")
PATH_NUMBER = re.compile(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")
PATH_COMMAND = re.compile(r"[MmZzLlHhVvCcSsQqTtAa]")


def sample_times(end, edges, fps, starts=()):
    # #126 #297 #326 #411
    step = 1000 / fps
    first = max((e for e in edges if 0 <= e < min(MIN_GAP_MS, end)), default=0)
    exact = [first] + ([end] if end > 0 else [])
    spans = []
    for start, moves_at in starts:
        moving = start + (math.floor((moves_at - start) / step) + 1) * step
        if moving - moves_at < MIN_GAP_MS:
            moving += step
        if 0 <= moves_at and moving < end:
            spans.append((moves_at, moving))
    for e in sorted(edges) + [b for _, b in spans]:
        if 0 < e < end and all(abs(e - t) >= MIN_GAP_MS for t in exact):
            exact.append(e)
    frames = [k * step for k in range(1, int(end // step) + 1)]
    return sorted(
        exact
        + [
            t
            for t in frames
            if all(abs(t - x) >= MIN_GAP_MS for x in exact)
            and 0 < t < end
            and not any(a < t < b for a, b in spans)
        ]
    )


def path_structure(d):
    return "".join(PATH_COMMAND.findall(d)), len(PATH_NUMBER.findall(d))


def path_numbers(d):
    return [float(n) for n in PATH_NUMBER.findall(d)]


def morph_points(writes):
    points, structure = [], None
    for i, w in enumerate(writes):
        new = path_structure(w["value"])
        if structure is not None and new != structure:
            raise ValueError(f"{structure[0]!r} then {new[0]!r}")
        held = (
            w["prev_ms"] is not None
            and w["old"] is not None
            and (not points or w["prev_ms"] > points[-1][0])
        )
        if held and (i > 0 or path_structure(w["old"]) == new):
            points.append((w["prev_ms"], path_numbers(w["old"])))
        points.append((w["ms"], path_numbers(w["value"])))
        structure = new
    return points


def morph_at(points, t):
    i = bisect.bisect_right([p[0] for p in points], t)
    if i == 0:
        return points[0][1]
    if i == len(points):
        return points[-1][1]
    (ta, a), (tb, b) = points[i - 1], points[i]
    k = (t - ta) / (tb - ta)
    return [x + (y - x) * k for x, y in zip(a, b, strict=True)]


def is_dropped_gap(gap, frame):
    # guess, #126
    return gap > (DROPPED_FRAMES + 0.5) * frame


def dropped_frames(writes):
    gaps = [w["ms"] - w["prev_ms"] for w in writes if w["prev_ms"] is not None]
    try:
        points = morph_points(writes)
    except ValueError as exc:
        expected(exc, "no dropped frames")
        return []
    if not gaps:
        return []
    frame = min(statistics.median(gaps), BROWSER_FRAME_MS)
    out = []
    for (ta, a), (tb, b) in itertools.pairwise(points):
        if a != b and is_dropped_gap(tb - ta, frame):
            if out and out[-1][1] == ta:
                out[-1] = (out[-1][0], tb)
            else:
                out.append((ta, tb))
    return out


def add_morphs(sample):
    by_label = {e["label"]: e for e in sample["elements"]}
    for m in sample["morphs"]:
        try:
            points = morph_points(m["writes"])
        except ValueError as exc:
            raise runner.UnmeasurableError(
                [
                    f"rewrites the d of {m['label']} with a different command structure from frame to frame "
                    f"({exc}), so its numbers cannot be paired to measure"
                ]
            ) from exc
        el = by_label.get(m["label"])
        if el is None:
            el = by_label[m["label"]] = {
                "label": m["label"],
                "loops": False,
                "channels": {},
            }
            sample["elements"].append(el)
        # #624
        lo, hi = sample["times"][0], sample["times"][-1]
        own = (
            [lo]
            + [t for t, _ in points if lo + MIN_GAP_MS <= t <= hi - MIN_GAP_MS]
            + [hi]
        )
        el.setdefault("times", {})["d"] = own
        el["channels"]["d"] = [morph_at(points, t) for t in own]
        el.setdefault("dropped", {})["d"] = dropped_frames(m["writes"])


def numbers(prop, value):
    if isinstance(value, list):
        return [float(v) for v in value]
    if value is None:
        return []
    v = value.strip()
    n = [float(x) for x in NUMBER.findall(v)]
    if prop == "transform":
        if v == "none":
            return list(IDENTITY_3D)
        if v.startswith("matrix(") and len(n) == 6:
            a, b, c, d, e, f = n
            return [a, b, 0, 0, c, d, 0, 0, 0, 0, 1, 0, e, f, 0, 1]
    if prop == "scale":
        n = [1.0] if v == "none" else n
        if len(n) == 1:
            n = n * 2
        if len(n) == 2:
            n = n + [1.0]
        return n
    if v.startswith("rgb(") and len(n) == 3:
        return n + [1.0]
    return n


def deltas(series):
    out = []
    for a, b in itertools.pairwise(series):
        n = max(len(a), len(b))
        out.append(
            [
                y - x
                for x, y in zip(
                    a + [0.0] * (n - len(a)), b + [0.0] * (n - len(b)), strict=True
                )
            ]
        )
    return out


def rates(changes, times, floor=0.0):
    out = []
    for d, (ta, tb) in zip(changes, itertools.pairwise(times), strict=True):
        dt = (tb - ta) / 1000
        size = math.hypot(*d)
        v = size / dt if dt > 0 and size >= floor else 0.0
        out.append(v if v >= NOISE else 0.0)
    return out


def same_way(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True)) > 0


def line_at(ts, vs, t):
    mt, mv = statistics.fmean(ts), statistics.fmean(vs)
    sxx = sum((x - mt) ** 2 for x in ts)
    return mv + sum((x - mt) * (y - mv) for x, y in zip(ts, vs, strict=True)) / sxx * (
        t - mt
    )


def steps_in(r, changes, times, *, s, e):
    top = max(r[s : e + 1])
    k = STEP_SIDE_FRAMES
    mids = [(a + b) / 2 for a, b in itertools.pairwise(times)]

    def step_at(i, n):
        if i + n + k - 1 > e or not all(
            same_way(changes[j], changes[j + 1]) for j in range(i - k, i + n + k - 1)
        ):
            return None
        before, after = r[i - k : i], r[i + n : i + n + k]
        last, first = before[-1], after[0]
        ahead = line_at(mids[i - k : i], before, mids[i + n])
        back = line_at(mids[i + n : i + n + k], after, mids[i - 1])
        if ahead <= 0 or back <= 0:
            return None
        gains = (first / ahead, back / last)
        slow, fast = sorted((before, after), key=statistics.fmean)
        if (
            max(slow) > STEP_HOLD * min(slow)
            or max(fast) > STEP_FAST_HOLD * min(fast)
            or max(last, first) < STEP_RATIO * min(last, first)
            or not (min(gains) >= STEP_RATIO or max(gains) <= 1 / STEP_RATIO)
            or max(fast) < STEP_FLOOR * top
            or not all(max(slow) < v < min(fast) for v in r[i : i + n])
        ):
            return None
        up = first > last
        return (
            i,
            n,
            last / top,
            (max(after) if up else min(after)) / top,
            "up" if up else "down",
        )

    def first(tries):
        return next(filter(None, (step_at(i, n) for i, n in tries)), None)

    out = []
    i = s + k
    while i < e:
        found = first((i, n) for n in range(STEP_SPREAD))
        # #126, #612
        while found and (
            later := first((found[0] + j, found[1] - j) for j in range(1, found[1] + 1))
        ):
            found = later
        out += [found] if found else []
        i = found[0] + found[1] + 1 if found else i + 1
    return out


# #623
def merged_steps(label, found):
    out, reach = [], None
    for way, lo, hi, _, name, at, before, after in sorted(found):
        if out and out[-1]["way"] == way and lo <= reach:
            out[-1]["channels"].append(name)
            reach = max(reach, hi)
            continue
        out.append(
            {
                "element": label,
                "way": way,
                "at": at,
                "from": round(before, 2),
                "to": round(after, 2),
                "channels": [name],
            }
        )
        reach = hi
    return out


# #632
def merged_edges(found, fps):
    near = MERGE_FRAMES * 1000 / fps * (1 - FRAME_SLACK)
    out, first, start = [], None, None
    for key, t, edge in sorted(found, key=lambda f: (f[0], f[1])):
        if (
            first == key
            and t - start < near
            and not set(edge["channels"]) & set(out[-1]["channels"])
        ):
            merged = out[-1]
            merged["channels"] += edge["channels"]
            if edge.get("share", 0) > merged.get("share", 0):
                merged["share"], merged["line"] = edge["share"], edge["line"]
            if "would_be" in edge:
                merged["would_be"] = sorted({*merged["would_be"], *edge["would_be"]})
        else:
            out.append({**edge, "channels": list(edge["channels"])})
            first, start = key, t
    return out


def runs(flags):
    out, start = [], None
    for i, f in enumerate(flags + [False]):
        if f and start is None:
            start = i
        elif not f and start is not None:
            out.append((start, i - 1))
            start = None
    return out


def still_px(view_cm):
    return STILL_ARCMIN_S / math.degrees(60 * math.atan(CSS_PX_CM / view_cm))


def jump_px(view_cm):
    return 2 * view_cm * math.tan(math.radians(JUMP_DEG) / 2) / CSS_PX_CM


def jolt_line(ms):
    if ms < JOLT_BAND[0][0]:
        return None
    for (a, lo_a, hi_a), (b, lo_b, hi_b) in itertools.pairwise(JOLT_BAND):
        if ms <= b:
            k = (ms - a) / (b - a)
            return ((lo_a + hi_a) + k * (lo_b + hi_b - lo_a - hi_a)) / 2
    return (JOLT_BAND[-1][1] + JOLT_BAND[-1][2]) / 2


def nearest(ts, t):
    i = bisect.bisect_left(ts, t)
    return min(
        (j for j in (i - 1, i) if 0 <= j < len(ts)), key=lambda j: abs(ts[j] - t)
    )


def analyse(sample, pause_ms=PAUSE_MS, jolt_ratio=None, view_cm=VIEW_CM, *, fps=FPS):
    shared = sample["times"]
    moved = []
    elements = []
    steps = []
    for el in sample["elements"]:
        channels = {}
        seen_at = el.get("seen") or [True] * len(shared)
        found = []
        for name, values in el["channels"].items():
            times = el.get("times", {}).get(name, shared)
            seen = (
                seen_at
                if times is shared
                else [seen_at[nearest(shared, t)] for t in times]
            )
            changes = deltas([numbers(name, v) for v in values])
            r = rates(changes, times, PX_NOISE if name in PX_CHANNELS else 0.0)
            peak = max(r, default=0.0)
            if peak <= 0:
                continue
            floor = STILL_FRACTION * peak
            if name in PX_CHANNELS:
                floor = min(floor, still_px(view_cm))
            moving = [v > floor for v in r]
            stretches = el.get("dropped", {}).get(name, [])
            unknown = [
                any(ta < b and tb > a for a, b in stretches)
                for ta, tb in itertools.pairwise(times)
            ]
            # #150
            turns = {}
            for (_, e), (s, _) in itertools.pairwise(runs(moving)):
                if times[s] - times[e + 1] <= pause_ms and same_way(
                    changes[e], [-x for x in changes[s]]
                ):
                    turns[s] = e
            channels[name] = {
                "times": times,
                "seen": seen,
                "rates": r,
                "peak": peak,
                "moving": moving,
                "unknown": unknown,
                "turns": turns,
            }
            moved += [(times[s], times[e + 1]) for s, e in runs(moving)]
            for s, e in runs(moving):
                for i, n, before, after, way in steps_in(r, changes, times, s=s, e=e):
                    if any(unknown[i - STEP_SIDE_FRAMES : i + n + STEP_SIDE_FRAMES]):
                        continue
                    # #624
                    found.append(
                        (
                            way,
                            times[i - 1],
                            times[i + n],
                            len(channels),
                            name,
                            round((times[i] + times[i + n]) / 2),
                            before,
                            after,
                        )
                    )
        steps += merged_steps(el["label"], found)
        elements.append(
            {
                "label": el["label"],
                "loops": el.get("loops", False),
                "channels": channels,
            }
        )

    # #220
    pauses = []
    still, reach = [], shared[0]
    for a, b in sorted(moved) + [(shared[-1], shared[-1])]:
        if a > reach:
            still.append((reach, a))
        reach = max(reach, b)
    for start, end in still:
        if start > shared[0] and end - start > pause_ms:
            where = "at the end" if end == shared[-1] else None
            pauses.append(
                {
                    "start": round(start),
                    "end": round(end),
                    "ms": round(end - start),
                    "where": where,
                }
            )

    jolts, jumps, unseen = [], {}, []
    jump_min = jump_px(view_cm)
    for el in elements:
        for name, ch in el["channels"].items():
            times, seen = ch["times"], ch["seen"]
            r, turns, unknown = ch["rates"], ch["turns"], ch["unknown"]
            gaps = len(times) - 1
            in_frame = {e for s, e in turns.items() if s - e - 1 <= TURN_FRAMES}
            jolted = set()
            for s, e in runs(ch["moving"]):
                top = max(r[s : e + 1])
                line = (
                    jolt_ratio
                    if jolt_ratio is not None
                    else jolt_line(times[e + 1] - times[s])
                )
                # #150
                before = turns.get(s)
                turned = before is not None and before not in jolted
                edges = [
                    (
                        "starts",
                        s,
                        times[s],
                        r[s] - r[before] if turned else r[s],
                        turned,
                        s,
                    )
                ]
                if not (el["loops"] and e == gaps - 1) and e not in in_frame:
                    edges.append(("stops", e, times[e + 1], r[e], False, e + 1))
                for edge, i, t, gain, turn, rest in edges:
                    if unknown[i] or (turn and unknown[before]):
                        continue
                    jolt = line is not None and gain >= line * top
                    moved = r[i] * (times[i + 1] - times[i]) / 1000
                    jump = (
                        edge == "starts"
                        and not turn
                        and name == "position"
                        and moved >= jump_min
                    )
                    if jolt and edge == "stops":
                        jolted.add(i)
                    if not (jolt or jump):
                        continue
                    if not seen[rest]:
                        unseen.append(
                            (
                                (el["label"], edge),
                                t,
                                {
                                    "element": el["label"],
                                    "edge": edge,
                                    "at": round(t),
                                    "would_be": [
                                        k
                                        for k, f in (("jolt", jolt), ("jump", jump))
                                        if f
                                    ],
                                    "channels": [name],
                                },
                            )
                        )
                        continue
                    if jolt:
                        jolts.append(
                            (
                                (el["label"], edge, turn),
                                t,
                                {
                                    "element": el["label"],
                                    "edge": edge,
                                    "at": round(t),
                                    "share": round(gain / top, 2),
                                    "line": round(line, 2),
                                    "channels": [name],
                                }
                                | ({"turn": True} if turn else {}),
                            )
                        )
                    if jump:
                        jumps[(el["label"], round(t))] = {
                            "element": el["label"],
                            "at": round(t),
                            "px": round(moved, 1),
                        }

    def by_time(found):
        return sorted(found, key=lambda x: (x["at"], x["element"]))

    return {
        "pauses": pauses,
        "jolts": by_time(merged_edges(jolts, fps)),
        "jumps": by_time(jumps.values()),
        "unseen": by_time(merged_edges(unseen, fps)),
        "steps": by_time(steps),
        "elements": elements,
    }


def settled(s, quiet):
    return s["looped"] or (
        s["firstFrame"] is not None
        and s["running"] == 0
        and s["timer"] is None
        and not s["framing"]
        and not s["rewriting"]
        and s["now"] - max(s["lastNew"], s["firstFrame"]) >= quiet
    )
