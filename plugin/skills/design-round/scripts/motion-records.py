"""motion-records.py — the record checks check-flow.py --records runs (#318):
how each reading becomes a record's faults, and how a record's checks give it
one answer. It does no I/O: check-flow.py loads it by path, drives the page
and passes what it reads to the functions below. The checks and the value
each takes are in CHECKS; each table line names its record, its check and the
value from that record:

    vault.motion-frequency | frequent | under 150

A record's answer is fail where any of its checks found a fault, else not
judged where a check needs a part the round did not declare or could not
read the page, else pass where a check found something the record applies
to, else no match.
"""

import collections
import itertools
import math
import os
import sys
import re

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402

rule_table = siblings.load(HERE, "rule-table.py")

NUMBER = r"(\d+(?:\.\d+)?)"
Check = collections.namedtuple("Check", "pattern parse needs")
Line = collections.namedtuple("Line", "id mode value")
# One check's reading: its faults (None where it could not judge), whether it
# found anything its record applies to, and why it could not judge, if so.
Answer = collections.namedtuple("Answer", "faults seen unmet")


def _none(_m):
    return None


def _numbers(*keys):
    return lambda m: dict(zip(keys, (float(g) for g in m.groups()), strict=True))


# Each check: the shape of its table value, what it reads from the match, and
# the part the round must declare before it can judge.
CHECKS = {
    "native-scroll": Check(
        rf"wheel {NUMBER}, slack {NUMBER}", _numbers("wheel", "slack"), ()
    ),
    "parallax": Check(
        rf"steps {NUMBER}, step {NUMBER}, slack {NUMBER}",
        _numbers("steps", "step", "slack"),
        (),
    ),
    "replay": Check(r"none", _none, ()),
    "carousel": Check(
        rf"phone under {NUMBER}, at least {NUMBER} s, words per second {NUMBER}, watch {NUMBER} s",
        _numbers("phone", "least", "wps", "watch"),
        ("carousel",),
    ),
    "flash": Check(
        rf"flashes {NUMBER}, luminance {NUMBER}, darker {NUMBER}, red {NUMBER}, chroma {NUMBER}, "
        rf"screen {NUMBER}x{NUMBER}, field {NUMBER}x{NUMBER}, share {NUMBER}, watch {NUMBER} s",
        _numbers(
            "flashes",
            "luminance",
            "darker",
            "red",
            "chroma",
            "screen_w",
            "screen_h",
            "field_w",
            "field_h",
            "share",
            "watch",
        ),
        (),
    ),
    "drag-release": Check(
        rf"deceleration {NUMBER}, slack {NUMBER}", _numbers("rate", "slack"), ()
    ),
    "frequent": Check(rf"under {NUMBER}", _numbers("under"), ()),
    "slow-update": Check(r"none", _none, ()),
}

# The parts drag-release reads, by the record's `parts`.
DRAG_PARTS = ("bottom-sheet", "card")


TableError = rule_table.TableError


def parse_value(mode, value):
    """A table value for `mode`, as its check reads it. Raises ValueError
    where it does not fit the check's shape."""
    m = re.fullmatch(CHECKS[mode].pattern, value)
    if m is None:
        raise ValueError(
            f"{mode} wants a value like {CHECKS[mode].pattern!r}, got {value!r}"
        )
    return CHECKS[mode].parse(m)


def parse_table(text):
    """The table's lines, each a Line; `#` lines and blank ones are skipped."""
    lines, first_by_check = [], {}
    for n, line in rule_table.lines(text):
        fields = [f.strip() for f in line.split("|")]
        if len(fields) != 3 or fields[1] not in CHECKS:
            raise TableError(
                f"line {n}: wants `record id | check | value`, the check one of {', '.join(CHECKS)}: {line!r}"
            )
        try:
            value = parse_value(fields[1], fields[2])
        except ValueError as exc:
            raise TableError(f"line {n}: {exc}") from None
        first_n, first_value = first_by_check.setdefault(fields[1], (n, value))
        if first_value != value:
            raise TableError(
                f"line {n}: {fields[1]} is already given a different value on line {first_n}, "
                "and a check runs once, at one value"
            )
        lines.append(Line(fields[0], fields[1], value))
    modes = {line.mode for line in lines}
    if "replay" in modes and "parallax" not in modes:
        raise TableError(
            "a replay line reads parallax's sweep, so it needs a parallax line"
        )
    return lines


def missing(mode, parts):
    """What the round must still declare before `mode` can judge, in words,
    or None. `parts` maps a declared part to its selector."""
    for name in CHECKS[mode].needs:
        if not parts.get(name):
            return f"no {name} part declared with a selector (--parts)"
    return None


def fault(mode, subject, detail, fix):
    """One fault: what `subject` does wrong, and `fix`, the way out."""
    return {"kind": mode, "subject": subject, "detail": detail, "fix": fix}


# The ways a visitor scrolls that native-scroll drives, each with the words
# its faults use.
SCROLL_INPUTS = {"wheel": "wheel turn", "key": "Page Down", "touch": "touch drag"}


def native_scroll_faults(got, v):
    """vault.native-scroll's faults from one scroll by each of SCROLL_INPUTS,
    each on a fresh load: `got` maps an input to the window's scroll before
    and after, how far it could scroll, and the cancels a handler made. A
    cancelled input is a fault; so is a wheel turn that moves the page other
    than its own distance, or a key or touch scroll that does not move it
    down. None where the page has no room to scroll."""
    out, judged = [], False
    for name, read in got.items():
        # A wheel turn needs room for its whole distance; a key or touch
        # scroll, whose distance is the browser's, needs only some room.
        if read["room"] <= 0 or (name == "wheel" and read["room"] < v["wheel"]):
            continue
        judged = True
        moved = read["after"] - read["before"]
        words = SCROLL_INPUTS[name]
        if read["cancelled"]:
            out.append(
                fault(
                    "native-scroll",
                    "the page",
                    f"a handler cancels the {words} ({read['cancelled']}), so the page's own script "
                    f"moves it {moved:.0f} px",
                    "drop the handler's preventDefault() and let the browser scroll the page",
                )
            )
        elif name == "wheel" and abs(moved - v["wheel"]) > v["slack"]:
            out.append(
                fault(
                    "native-scroll",
                    "the page",
                    f"a {v['wheel']:.0f} px wheel turn moves the page {moved:.0f} px",
                    "let the browser scroll the page by the wheel's own distance",
                )
            )
        elif name != "wheel" and moved <= 0:
            out.append(
                fault(
                    "native-scroll",
                    "the page",
                    f"a {words} does not scroll the page",
                    "let the browser scroll the page",
                )
            )
    return out if judged else None


def _rate_kind(rate, slack):
    """'native' for a box that moves with the page or stays put, else None."""
    return "native" if abs(rate + 1) <= slack or abs(rate) <= slack else None


def parallax_faults(track, v):
    """vault.parallax's faults and the parallax layers seen, from `track`:
    the scroll offsets of each step and, for each element, its kind (text,
    control or image) and its top at each step, None where it was out of the
    window. A layer moving at a rate neither the page's nor none for `steps`
    steps in a row is parallax; text or a control moving so is a fault."""
    scrolls = track["scrolls"]
    faults, seen = [], []
    for el in track["elements"]:
        run, best = 0, None
        for i in range(1, len(scrolls)):
            a, b = el["tops"][i - 1], el["tops"][i]
            dy = scrolls[i] - scrolls[i - 1]
            if a is None or b is None or not dy:
                run = 0
                continue
            rate = (b - a) / dy
            run = 0 if _rate_kind(rate, v["slack"]) else run + 1
            if run >= v["steps"]:
                best = rate
        if best is None:
            continue
        speed = f"moves {-best:.2f}× the page's scroll"
        seen.append(el["label"])
        if el["kind"] in ("text", "control"):
            faults.append(
                fault(
                    "parallax",
                    el["label"],
                    f"{el['kind']} that {speed}; parallax is for background and edge images only",
                    f"scroll the {el['kind']} at the page's own speed, and move only a background or edge image",
                )
            )
    return faults, seen


def replays(ran):
    """The animations each element ran on the first sweep down and on the
    second, from `ran`, the page's log by phase, leaving out every element
    that also animated while the page sat still, since its motion is the
    clock's, not the scroll's."""
    idle = set(ran.get("idle", {}))
    first = {k: n for k, n in ran["down"].items() if k not in idle}
    again = {k: n for k, n in ran["again"].items() if k not in idle}
    return first, again


# The properties a parallax layer's scroll moves: a transition on them
# smooths the scroll's own motion, which runs on every sweep.
SCROLL_MOVED = frozenset({"transform", "translate", "top"})


def replay_faults(first, again, layers):
    """vault.parallax's replay faults: each parallax layer, by `layers`, whose
    animation or transition ran as the page scrolled down, `first`, and ran
    again when it was scrolled down a second time, `again`, each
    {label: [names]}, leaving out SCROLL_MOVED."""
    out = []
    for label in sorted(set(layers)):
        ran = set(first.get(label, ())) - SCROLL_MOVED
        rerun = set(again.get(label, ())) - SCROLL_MOVED
        if ran and rerun:
            out.append(
                fault(
                    "replay",
                    label,
                    f"replays {', '.join(sorted(rerun))} when scrolled back to, rather than resting at its end",
                    "run it once and leave it at its end state",
                )
            )
    return out


def carousel_widths(phone, wide, v):
    """Why the carousel check cannot judge at these load widths, or None: its
    phone load must sit under the record's phone width and its wide load at
    or over it."""
    if phone >= v["phone"]:
        return f"the phone load is {phone} px wide, not under {v['phone']:.0f}"
    if wide < v["phone"]:
        return f"the viewport is {wide} px wide, under the {v['phone']:.0f} px the wide load needs (--viewport)"
    return None


def carousel_faults(got, v, slack):
    """vault.carousel-timing's faults, from `got`: the phone load's advances,
    and the wide load's frames (each the time it showed from and its word
    count), whether it advanced while hovered, while focused and after the
    visitor changed frame, and the control used for that (None where none
    was found). A hold is read to within `slack` s, the clock step it was
    read at."""
    out = []
    label = got["label"]
    if got["phone_advances"]:
        out.append(
            fault(
                "carousel",
                label,
                f"advances by itself at phone width ({got['phone_width']} px, under {v['phone']:.0f})",
                f"turn auto-advance off under {v['phone']:.0f} px",
            )
        )
    frames = got["frames"]
    for here, after in itertools.pairwise(frames):
        held = (after["from"] - here["from"]) / 1000
        need = max(v["least"], math.ceil(here["words"] / v["wps"]))
        if held < need - slack:
            out.append(
                fault(
                    "carousel",
                    label,
                    f"holds a {here['words']}-word frame {held:.1f} s, under its {need:.0f} s",
                    f"hold each frame {v['least']:.0f} s or its words ÷ {v['wps']:.0f} s, whichever is longer",
                )
            )
            break
    advanced = len(frames) > 1
    for state in ("hovered", "focused"):
        if advanced and got[state]:
            out.append(
                fault(
                    "carousel",
                    label,
                    f"advances while {state}",
                    f"pause it while {state}",
                )
            )
    if advanced and got["after_change"]:
        out.append(
            fault(
                "carousel",
                label,
                f"advances again after the visitor changed frame by {got['control']}",
                "stop auto-advancing once the visitor changes frame",
            )
        )
    return out


def projected(position, velocity, rate):
    """Where a release at `velocity` px/s ends once it decays at `rate` a
    millisecond: Apple's projection, velocity / 1000 × rate / (1 − rate)."""
    return position + velocity / 1000 * rate / (1 - rate)


def snap_points(rests, slack):
    """The distinct places a part's releases came to rest, nearer than
    `slack` px counted as one."""
    out = []
    for r in sorted(rests):
        if not out or r - out[-1] > slack:
            out.append(r)
    return out


def fling_way(snaps, here):
    """+1 or -1: the way from `here` with more room before the farthest snap
    point, so a fling has somewhere to go."""
    return 1 if max(snaps) - here > here - min(snaps) else -1


def release_velocity(release, axis, horizon):
    """The release's velocity in px/s along `axis` (left or top), from
    `release`: its time and the pointer's moves, each [ms, x, y], since the
    press. Only the moves within `horizon` ms of the release count; 0 where
    fewer than two do, or they span no time."""
    k = 2 if axis == "top" else 1
    recent = [m for m in release["moves"] if m[0] > release["at"] - horizon]
    span = recent[-1][0] - recent[0][0] if len(recent) > 1 else 0
    return (recent[-1][k] - recent[0][k]) / span * 1000 if span > 0 else 0


def nearest(snaps, x):
    return min(snaps, key=lambda s: abs(s - x))


def picks_another_snap(snaps, fling, rate):
    """Whether the fling's projection picks a different snap point than the
    one nearest where it was let go, so a part that ignores its velocity
    would settle wrong. A part with one snap point has none to pick between,
    so any fling serves."""
    if len(snaps) < 2:
        return True
    aim = projected(fling["at"], fling["velocity"], rate)
    return nearest(snaps, aim) != nearest(snaps, fling["at"])


def drag_faults(got, v):
    """vault.drag-release's faults for one part dragged along one axis, from
    `got`: the snap points its slow releases settled at, and its flung
    release: where it was let go, at what velocity, and the path it took
    after, one position a frame. It must settle where the release's
    projection picks, set off the way it was thrown and not overshoot."""
    snaps, fling, label = got["snaps"], got["fling"], got["label"]
    path = fling["path"]
    end = path[-1]
    aim = projected(fling["at"], fling["velocity"], v["rate"])
    want = nearest(snaps, aim)
    out = []
    if picks_another_snap(snaps, fling, v["rate"]) and abs(end - want) > v["slack"]:
        out.append(
            fault(
                "drag-release",
                label,
                f"flung at {fling['velocity']:.0f} px/s from {fling['at']:.0f} px, it settles at "
                f"{end:.0f} px, not the snap point {want:.0f} px its projection ({aim:.0f} px) picks",
                f"settle on the snap point nearest its projection, {want:.0f} px",
            )
        )
    # The path starts at the release, before the page's own handler runs, so
    # its first move is the release's.
    first = next(
        (b - a for a, b in itertools.pairwise(path) if abs(b - a) > v["slack"]), 0
    )
    if first * fling["velocity"] < 0:
        out.append(
            fault(
                "drag-release",
                label,
                "turns back the moment it is let go, so its settle does not start at the release velocity",
                "start the settle from the release velocity",
            )
        )

    way = 1 if end >= fling["at"] else -1
    past = max((p - end) * way for p in path)
    if past > v["slack"]:
        out.append(
            fault(
                "drag-release",
                label,
                f"overshoots its rest by {past:.0f} px and springs back: a bounce",
                "spring to the snap point with no bounce",
            )
        )
    return out


def frequent_faults(changes, v):
    """vault.motion-frequency's faults, from `changes`: each control's state
    change (hover or press) that started motion, and STARTED_JS's reading of
    it, ENDLESS or ENDS with its `ms`."""
    return [
        fault(
            "frequent",
            c["label"],
            f"its {c['state']} motion runs "
            + ("without end" if c["motion"] == ENDLESS else f"{c['ms']:.0f} ms")
            + f", not under {v['under']:.0f} ms",
            f"end it under {v['under']:.0f} ms, or drop it",
        )
        for c in changes
        if c["motion"] == ENDLESS or c["ms"] >= v["under"]
    ]


def slow_update_faults(got):
    """vault.slow-update's faults, from the page's authored animation and
    transition rules outside `@media (update: fast)`, its inline ones, and
    the script animations it runs when told the screen updates slowly."""
    out = [
        fault(
            "slow-update",
            r["where"],
            f"{r['sets']} runs outside @media (update: fast)",
            "move it inside @media (update: fast)",
        )
        for r in got["rules"]
    ]
    out += [
        fault(
            "slow-update",
            s["label"],
            "a script animation still runs where (update: slow) matches",
            "skip it where matchMedia('(update: slow)') matches",
        )
        for s in got["scripted"]
    ]
    return out


# --- the flash analysis (WCAG 2.3.1) -----------------------------------------
# Each function imports numpy itself: check-flow.py loads this module in every
# mode, and its brand-motion mode runs without numpy installed.


def _linear(rgb):
    """sRGB values in [0, 1] made linear, by WCAG's formula."""
    import numpy as np

    return np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)


def relative_luminance(rgb):
    """WCAG's relative luminance of sRGB values in [0, 1], last axis RGB."""
    import numpy as np

    return _linear(rgb) @ np.array([0.2126, 0.7152, 0.0722])


def chromaticity(rgb):
    """CIE 1976 u′v′ of sRGB values in [0, 1], last axis RGB, and R/(R+G+B)."""
    import numpy as np

    lin = _linear(rgb)
    m = np.array(
        [[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]
    )
    xyz = lin @ m.T
    d = xyz[..., 0] + 15 * xyz[..., 1] + 3 * xyz[..., 2]
    d = np.where(d == 0, 1, d)
    uv = np.stack([4 * xyz[..., 0] / d, 9 * xyz[..., 1] / d], axis=-1)
    total = rgb.sum(axis=-1)
    share = np.where(total == 0, 0, rgb[..., 0] / np.where(total == 0, 1, total))
    return uv, share


def luminance_transitions(lum, v):
    """Per frame and pixel, whether a general-flash transition ends there:
    the luminance has moved `luminance` or more from the last peak or valley,
    the way opposite the last transition, and the darker of the two states is
    under `darker` (WCAG 2.2's general flash; Note 2's peaks and valleys)."""
    import numpy as np

    out = np.zeros(lum.shape, dtype=bool)
    hi, lo = lum[0].copy(), lum[0].copy()
    way = np.zeros(lum.shape[1:], dtype=np.int8)
    for t in range(1, lum.shape[0]):
        x = lum[t]
        hi, lo = np.maximum(hi, x), np.minimum(lo, x)
        up = (x - lo >= v["luminance"]) & (way != 1) & (lo < v["darker"])
        down = (hi - x >= v["luminance"]) & (way != -1) & (x < v["darker"])
        hit = up | down
        out[t] = hit
        way = np.where(up, 1, np.where(down, -1, way)).astype(np.int8)
        # The peak or valley to come is read from here on.
        hi, lo = np.where(hit, x, hi), np.where(hit, x, lo)
    return out


def red_transitions(uv, share, v):
    """Per frame and pixel, whether a red-flash transition ends there: the
    state differs from the last one by more than `chroma` in u′v′, and one of
    the two has R/(R+G+B) at `red` or more (WCAG 2.2's Note 3)."""
    import numpy as np

    n = uv.shape[0]
    out = np.zeros(uv.shape[:-1], dtype=bool)
    anchor_uv, anchor_red = uv[0].copy(), share[0] >= v["red"]
    for t in range(1, n):
        dist = np.sqrt(((uv[t] - anchor_uv) ** 2).sum(axis=-1))
        red = share[t] >= v["red"]
        hit = (dist > v["chroma"]) & (red | anchor_red)
        out[t] = hit
        anchor_uv = np.where(hit[..., None], uv[t], anchor_uv)
        anchor_red = np.where(hit, red, anchor_red)
    return out


def box_sum(mask, h, w):
    """The sum over every h × w window of a 2-D array, by a summed-area table."""
    import numpy as np

    s = np.pad(mask.astype(np.int64).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    h, w = min(h, mask.shape[0]), min(w, mask.shape[1])
    return s[h:, w:] - s[:-h, w:] - s[h:, :-w] + s[:-h, :-w]


def flash_faults(rgb, times, px, v):
    """vault.flash-limit's faults over one screen's frames: `rgb` (frames ×
    rows × columns × 3, sRGB in [0, 1]) sampled at `times` seconds, each cell
    `px` CSS px on a side. A cell flashes in a one-second window holding more
    than twice `flashes` transitions; a window fails where its flashing cells
    cover more than `share` of some field-sized box."""
    import numpy as np

    lum = relative_luminance(rgb)
    uv, share = chromaticity(rgb)
    kinds = {
        "general": luminance_transitions(lum, v),
        "red": red_transitions(uv, share, v),
    }
    fh = max(1, round(v["field_h"] / px))
    fw = max(1, round(v["field_w"] / px))
    limit = v["share"] * fh * fw
    times = np.asarray(times)
    out = []
    for kind, hits in kinds.items():
        cum = np.concatenate(
            [np.zeros((1, *hits.shape[1:]), dtype=np.int32), hits.cumsum(0)]
        )
        start = 0
        for end in range(len(times)):
            # A one-second window, open at its far end, to within a ms of
            # float error in the frame times.
            while times[end] - times[start] >= 1 - 1e-3:
                start += 1
            count = cum[end + 1] - cum[start]
            flashing = count > 2 * v["flashes"]
            if not flashing.any():
                continue
            area = box_sum(flashing, fh, fw)
            if area.max() > limit:
                y, x = np.unravel_index(area.argmax(), area.shape)
                out.append(
                    {
                        "kind": kind,
                        "from_s": float(times[start]),
                        "box": [int(x * px), int(y * px), int(fw * px), int(fh * px)],
                        "transitions": int(count.max()),
                        "share": float(area.max() / (fh * fw)),
                    }
                )
                break
    return out


# --- what the page is asked ----------------------------------------------------


def with_label(js, label_js):
    """`js` with check-flow.py's label() defined at its LABEL mark."""
    return js.replace("LABEL", label_js, 1)


# Before any page script: each cancelled wheel, touch or scrolling key, by
# its type and, for a key, the key.
CANCEL_INIT = r"""
window.__cancelled = [];
const prevent = Event.prototype.preventDefault;
const KEYS = /^(PageDown|PageUp|ArrowDown|ArrowUp| |Home|End)$/;
Event.prototype.preventDefault = function () {
  if (/^(wheel|mousewheel|touchstart|touchmove)$/.test(this.type)) window.__cancelled.push(this.type);
  else if (this.type === 'keydown' && KEYS.test(this.key)) window.__cancelled.push('keydown ' + this.key);
  return prevent.call(this);
};
"""

# Before any page script: matchMedia answers as a screen that updates slowly.
SLOW_INIT = r"""
const real = window.matchMedia.bind(window);
window.matchMedia = (q) => {
  const t = String(q).replace(/\s+/g, '');
  if (/^\(update:(slow|fast|none)\)$/.test(t) || /^\(update\)$/.test(t)) {
    const m = real('all');
    const yes = t === '(update:slow)' || t === '(update)';
    return Object.create(m, { matches: { value: yes }, media: { value: String(q) } });
  }
  return real(q);
};
"""

# How far the window can still scroll down, where it stands, the wheel
# handlers' cancels, and the scroll box of its own under the window's middle,
# if any, which a wheel there would scroll rather than the window.
ROOM_JS = r"""
() => {
  let nested = null;
  for (let el = document.elementFromPoint(innerWidth / 2, innerHeight / 2); el && el !== document.scrollingElement && el !== document.body; el = el.parentElement) {
    const o = getComputedStyle(el).overflowY;
    if (/(auto|scroll)/.test(o) && el.scrollHeight > el.clientHeight) { nested = el.localName + (el.id ? '#' + el.id : ''); break; }
  }
  return { y: scrollY, room: document.scrollingElement.scrollHeight - innerHeight - scrollY,
    cancelled: [...new Set(window.__cancelled)].join(', '), nested };
}
"""

# Whether the element under ([x, y]), or an ancestor, sets a touch-action
# that takes the vertical pan for itself, as a map or canvas does.
PANS_ITSELF_JS = r"""
([x, y]) => {
  for (let el = document.elementFromPoint(x, y); el; el = el.parentElement) {
    const t = getComputedStyle(el).touchAction;
    if (t !== 'auto' && t !== 'manipulation' && !/pan-(y|up|down)/.test(t)) return true;
  }
  return false;
}
"""

# Waits until the window's scroll has held still for `still` ms, up to `cap`
# ms, so a key's smooth scroll has ended before it is read.
SCROLLED_JS = r"""
async ([still, cap]) => {
  const t0 = performance.now();
  let y = scrollY, last = t0;
  while (performance.now() - t0 < cap) {
    await new Promise(requestAnimationFrame);
    const now = performance.now();
    if (scrollY !== y) { y = scrollY; last = now; }
    else if (now - last >= still) break;
  }
}
"""

# Waits for every finite animation the page runs off the document clock to
# end, up to `cap` ms, two frames at least.
SETTLE_JS = r"""
async (cap) => {
  const frame = () => new Promise((r) => requestAnimationFrame(() => r()));
  await frame(); await frame();
  const end = performance.now() + cap;
  while (performance.now() < end) {
    const busy = document.getAnimations().some((a) => a.playState === 'running' &&
      a.timeline === document.timeline && Number.isFinite(a.effect.getComputedTiming().endTime));
    if (!busy) break;
    await frame();
  }
}
"""

# The elements parallax is read on, each its label and kind: a control, text
# (an element holding text of its own) or an image (an img, svg, video,
# canvas or background image). Logs each animation and transition that starts.
TRACK_JS = (
    "(cap) => {"
    + "LABEL"
    + r"""
  const CONTROL = 'a[href], button, input, select, textarea, summary, [role=button], [role=link], [tabindex]';
  const kind = (el) => {
    if (el.matches(CONTROL)) return 'control';
    if ([...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) return 'text';
    if (/^(img|svg|video|canvas|picture)$/.test(el.localName) || getComputedStyle(el).backgroundImage !== 'none') return 'image';
    return null;
  };
  const els = [];
  for (const el of document.body.querySelectorAll('*')) {
    if (els.length >= cap) break;
    if (el.closest('svg') && el.localName !== 'svg') continue;
    const k = kind(el);
    const r = el.getBoundingClientRect();
    if (k && r.width && r.height) els.push({ el, kind: k, label: label(el) });
  }
  window.__tracked = els;
  window.__phase = 'load';
  window.__ran = { down: {}, again: {} };
  window.__names = new Map();
  const log = (e) => {
    const into = window.__ran[window.__phase];
    if (!into) return;
    // Named once, so a class the motion toggles does not rename it.
    if (!window.__names.has(e.target)) window.__names.set(e.target, label(e.target));
    const l = window.__names.get(e.target);
    (into[l] = into[l] || []).push(e.animationName || e.propertyName);
  };
  document.addEventListener('animationstart', log, true);
  document.addEventListener('transitionrun', log, true);
  return els.map(({ kind, label }) => ({ kind, label }));
}
"""
)

# Each tracked element's top, null where it is out of the window.
TOPS_JS = r"""
() => {
  return window.__tracked.map(({ el }) => {
    const r = el.getBoundingClientRect();
    return r.bottom > 0 && r.top < innerHeight && r.height ? r.top : null;
  });
}
"""

# A carousel's frame: its slides are the children of the descendant, itself
# included, with the most children each at least half the carousel's width;
# the frame shown is the slide covering most of the carousel, by its area in
# the carousel's box times its opacity.
FRAME_JS = r"""
(sel) => {
  const box = document.querySelector(sel);
  if (!box) return null;
  const b = box.getBoundingClientRect();
  let track = null, most = 1;
  for (const el of [box, ...box.querySelectorAll('*')]) {
    const wide = [...el.children].filter((c) => c.getBoundingClientRect().width >= b.width / 2);
    if (wide.length > most) { track = wide; most = wide.length; }
  }
  if (!track) return { slides: 0 };
  const opacity = (el) => { let o = 1; for (let e = el; e && e !== box.parentElement; e = e.parentElement) o *= +getComputedStyle(e).opacity; return o; };
  let best = -1, at = 0;
  track.forEach((s, i) => {
    const r = s.getBoundingClientRect();
    const w = Math.max(0, Math.min(r.right, b.right) - Math.max(r.left, b.left));
    const h = Math.max(0, Math.min(r.bottom, b.bottom) - Math.max(r.top, b.top));
    const shown = w * h * opacity(s) * (getComputedStyle(s).visibility === 'hidden' ? 0 : 1);
    if (shown > best) { best = shown; at = i; }
  });
  return { slides: track.length, at, words: (track[at].innerText.match(/\S+/g) || []).length };
}
"""

# Ends every finite animation now, so a frame is read at rest.
FINISH_JS = r"""
() => document.getAnimations().forEach((a) => {
  if (Number.isFinite(a.effect.getComputedTiming().endTime)) a.finish();
})
"""

# The carousel's control that changes frame: the first button, tab or link
# in it named for next, previous or a slide, else its first button.
CHANGE_JS = (
    "(sel) => {"
    + "LABEL"
    + r"""
  const box = document.querySelector(sel);
  const all = [...box.querySelectorAll('button, [role=button], [role=tab], a[href]')];
  const named = all.find((c) => /next|prev|previous|slide|go to|›|‹|→|←|»|«/i.test(
    (c.getAttribute('aria-label') || '') + ' ' + c.textContent));
  const c = named || all.find((c) => c.matches('button, [role=button]'));
  if (!c) return null;
  c.click();
  return label(c);
}
"""
)

# The carousel's first part that takes focus, focused, or null.
FOCUS_JS = r"""
(sel) => {
  const box = document.querySelector(sel);
  const c = [box, ...box.querySelectorAll('a[href], button, input, select, textarea, [tabindex]')]
    .find((e) => e.tabIndex >= 0 && e.getBoundingClientRect().width);
  if (!c) return null;
  c.focus();
  return document.activeElement === c;
}
"""

# The controls a visitor hovers and presses many times, up to `cap`: links,
# buttons and menu items.
CONTROLS_JS = (
    "(cap) => {"
    + "LABEL"
    + r"""
  const els = [...document.querySelectorAll('a[href], button, [role=button], [role=menuitem], summary, input[type=submit], input[type=button]')]
    .filter((e) => { const r = e.getBoundingClientRect(); return r.width && r.height && getComputedStyle(e).visibility !== 'hidden'; })
    .slice(0, cap);
  window.__controls = els;
  window.__before = new WeakSet();
  return els.map((e) => label(e));
}
"""
)

# The `i`th control's centre in the window, scrolled into view, with every
# animation now running marked as already there.
CONTROL_AT_JS = r"""
(i) => {
  const el = window.__controls[i];
  el.scrollIntoView({ block: 'center', behavior: 'instant' });
  document.getAnimations().forEach((a) => window.__before.add(a));
  const r = el.getBoundingClientRect();
  return [r.left + r.width / 2, r.top + r.height / 2];
}
"""

# The motion the `i`th control's state change started, from the animations
# on it or inside it begun since CONTROL_AT_JS: {motion: "none"} where there
# are none, {motion: "endless"} where one never ends, else {motion: "ends",
# ms} with the latest end, in ms.
NO_MOTION, ENDLESS, ENDS = "none", "endless", "ends"
STARTED_JS = r"""
async (i) => {
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  const el = window.__controls[i];
  const ends = [];
  for (const a of document.getAnimations()) {
    if (window.__before.has(a) || !a.effect || !a.effect.target || !el.contains(a.effect.target)) continue;
    const end = a.effect.getComputedTiming().endTime;
    if (!Number.isFinite(end)) return { motion: "endless" };
    ends.push(end);
  }
  return ends.length ? { motion: "ends", ms: Math.max(...ends) } : { motion: "none" };
}
"""

# The page's own animation and transition rules outside @media (update:
# fast), each where it is and what it sets; inline ones; the sheets it could
# not read; whether any rule animates at all; and the script animations
# running now, which SLOW_INIT has told the page's script a slow screen.
SLOW_JS = (
    "() => {"
    + "LABEL"
    + r"""
  const FAST = /\(\s*update\s*:\s*fast\s*\)/;
  const moves = (st) => {
    const sets = [];
    const names = st.getPropertyValue('animation-name');
    if (names && names.split(',').some((n) => n.trim() && n.trim() !== 'none')) sets.push('animation ' + names.trim());
    const ds = st.getPropertyValue('transition-duration');
    if (ds && ds.split(',').some((d) => parseFloat(d) > 0)) sets.push('transition ' + (st.getPropertyValue('transition-property') || 'all').trim());
    return sets;
  };
  const rules = [], unread = [];
  let any = false;
  const walk = (list, fast, where) => {
    for (const r of list) {
      if (r.type === CSSRule.MEDIA_RULE) { walk(r.cssRules, fast || (FAST.test(r.conditionText) && !/^\s*not\b/.test(r.conditionText)), where); continue; }
      if (r.type === CSSRule.IMPORT_RULE && r.styleSheet) { readSheet(r.styleSheet); continue; }
      if (r.style) {
        const sets = moves(r.style);
        if (sets.length) { any = true; if (!fast) rules.push({ where: `${where}: ${r.selectorText}`, sets: sets.join(', ') }); }
      }
      if (r.cssRules && r.type !== CSSRule.KEYFRAMES_RULE) walk(r.cssRules, fast, where);
    }
  };
  const readSheet = (sh) => {
    const where = sh.href ? sh.href.split('/').pop() : 'the page\'s <style>';
    try { walk(sh.cssRules, false, where); } catch (e) { unread.push(where); }
  };
  for (const sh of document.styleSheets) readSheet(sh);
  for (const el of document.querySelectorAll('[style]')) {
    const sets = moves(el.style);
    if (sets.length) { any = true; rules.push({ where: `${label(el)}'s style attribute`, sets: sets.join(', ') }); }
  }
  const scripted = document.getAnimations()
    .filter((a) => !(a instanceof CSSAnimation) && !(a instanceof CSSTransition) && a.effect && a.effect.target
      && a.effect.getComputedTiming().activeDuration > 0)
    .map((a) => ({ label: label(a.effect.target) }));
  return { rules, unread, scripted, any: any || scripted.length > 0 };
}
"""
)

# The centre of the element `sel` in the window, scrolled to the middle of
# the window first where `show` is set.
CENTRE_JS = r"""
([sel, show]) => {
  const e = document.querySelector(sel);
  if (show) e.scrollIntoView({ block: 'center', behavior: 'instant' });
  const r = e.getBoundingClientRect();
  return [r.left + r.width / 2, r.top + r.height / 2];
}
"""

# The label of the element drawn at the point [x, y], or 'the screen'.
POINT_JS = (
    "([x, y]) => {"
    + "LABEL"
    + r"""
  const el = document.elementFromPoint(x, y);
  return el ? label(el) : 'the screen';
}
"""
)

# The part's position along `axis` (left or top), in the page, so a scroll
# that brings it under the pointer is no move of its own.
AT_JS = "const at = (el, axis) => el.getBoundingClientRect()[axis] + (axis === 'top' ? scrollY : scrollX);"
WHERE_JS = (
    "([sel, axis]) => {" + AT_JS + " return at(document.querySelector(sel), axis); }"
)

# Records the part's position along `axis`, as AT_JS reads it, now and each
# frame after until it has not moved for `still` ms, or `cap` ms have passed,
# into window.__path. A move of half a CSS px or less is no move, so sub-pixel
# jitter at rest does not hold the path open: a guess, which reads a part
# creeping under half a px a frame, about 30 px/s at 60 Hz, as still.
PATH_JS = (
    "([sel, axis, still, cap]) => {"
    + AT_JS
    + r"""
  const el = document.querySelector(sel);
  const path = [at(el, axis)], t0 = performance.now();
  window.__path = null;
  let last = t0;
  const tick = (now) => {
    const p = at(el, axis);
    if (Math.abs(p - path[path.length - 1]) > 0.5) last = now;
    path.push(p);
    if (now - last >= still || now - t0 >= cap) window.__path = path;
    else requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}
"""
)

# The press and each pointer move since, timed by the events' own clock, and
# the release: its time and those moves into window.__release. Where
# window.__watch holds PATH_JS's arguments, the release starts that path
# before the page's own handler runs, so its first position is the one let
# go at.
RELEASE_INIT = (
    "const pathOf = ("
    + PATH_JS
    + ")"
    + r""";
window.__moves = [];
window.__release = null;
window.__watch = null;
addEventListener('pointerdown', (e) => { window.__moves = [[e.timeStamp, e.clientX, e.clientY]]; }, true);
addEventListener('pointermove', (e) => window.__moves.push([e.timeStamp, e.clientX, e.clientY]), true);
addEventListener('pointerup', (e) => {
  window.__release = { at: e.timeStamp, moves: window.__moves };
  if (window.__watch) pathOf(window.__watch);
  window.__watch = null;
}, true);
"""
)


# --- answers -------------------------------------------------------------------


def answers(lines, got):
    """Each record's answer, from `got`, which maps each of its lines' checks
    to its Answer."""
    by_record = collections.defaultdict(list)
    for line in lines:
        by_record[line.id].append(got[line.mode])
    out = {}
    for record, answers_of in by_record.items():
        out[record] = rule_table.answer(
            misses=any(a.faults for a in answers_of),
            unjudged=any(a.unmet for a in answers_of),
            judged=any(a.seen for a in answers_of),
        )
    return out
