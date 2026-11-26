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
Answer = collections.namedtuple("Answer", "faults seen unmet")


def _none(_m):
    return None


def _numbers(*keys):
    return lambda m: dict(zip(keys, (float(g) for g in m.groups()), strict=True))


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

DRAG_PARTS = ("bottom-sheet", "card")


TableError = rule_table.TableError


def parse_value(mode, value):
    m = re.fullmatch(CHECKS[mode].pattern, value)
    if m is None:
        raise ValueError(
            f"{mode} wants a value like {CHECKS[mode].pattern!r}, got {value!r}"
        )
    return CHECKS[mode].parse(m)


def parse_table(text):
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
    for name in CHECKS[mode].needs:
        if not parts.get(name):
            return f"no {name} part declared with a selector (--parts)"
    return None


def fault(mode, subject, detail, fix):
    return {"kind": mode, "subject": subject, "detail": detail, "fix": fix}


SCROLL_INPUTS = {"wheel": "wheel turn", "key": "Page Down", "touch": "touch drag"}


def native_scroll_faults(got, v):
    out, judged = [], False
    for name, read in got.items():
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
    return "native" if abs(rate + 1) <= slack or abs(rate) <= slack else None


def parallax_faults(track, v):
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
    idle = set(ran.get("idle", {}))
    first = {k: n for k, n in ran["down"].items() if k not in idle}
    again = {k: n for k, n in ran["again"].items() if k not in idle}
    return first, again


SCROLL_MOVED = frozenset({"transform", "translate", "top"})


def replay_faults(first, again, layers):
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
    if phone >= v["phone"]:
        return f"the phone load is {phone} px wide, not under {v['phone']:.0f}"
    if wide < v["phone"]:
        return f"the viewport is {wide} px wide, under the {v['phone']:.0f} px the wide load needs (--viewport)"
    return None


def carousel_faults(got, v, slack):
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


# Apple's release projection: https://developer.apple.com/videos/play/wwdc2018/803/
def projected(position, velocity, rate):
    return position + velocity / 1000 * rate / (1 - rate)


def snap_points(rests, slack):
    out = []
    for r in sorted(rests):
        if not out or r - out[-1] > slack:
            out.append(r)
    return out


def fling_way(snaps, here):
    return 1 if max(snaps) - here > here - min(snaps) else -1


def release_velocity(release, axis, horizon):
    k = 2 if axis == "top" else 1
    recent = [m for m in release["moves"] if m[0] > release["at"] - horizon]
    span = recent[-1][0] - recent[0][0] if len(recent) > 1 else 0
    return (recent[-1][k] - recent[0][k]) / span * 1000 if span > 0 else 0


def nearest(snaps, x):
    return min(snaps, key=lambda s: abs(s - x))


def picks_another_snap(snaps, fling, rate):
    if len(snaps) < 2:
        return True
    aim = projected(fling["at"], fling["velocity"], rate)
    return nearest(snaps, aim) != nearest(snaps, fling["at"])


def drag_faults(got, v):
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


# #477
def _linear(rgb):
    import numpy as np

    return np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)


# WCAG weighs linear sRGB as 0.2126 R + 0.7152 G + 0.0722 B: https://www.w3.org/TR/WCAG22/#dfn-relative-luminance
def relative_luminance(rgb):
    import numpy as np

    return _linear(rgb) @ np.array([0.2126, 0.7152, 0.0722])


def chromaticity(rgb):
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


# A general flash is a pair of opposing 10% luminance changes with the darker below 0.80: https://www.w3.org/TR/WCAG22/#dfn-general-flash-and-red-flash-thresholds
def luminance_transitions(lum, v):
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
        hi, lo = np.where(hit, x, hi), np.where(hit, x, lo)
    return out


def red_transitions(uv, share, v):
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
    import numpy as np

    s = np.pad(mask.astype(np.int64).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    h, w = min(h, mask.shape[0]), min(w, mask.shape[1])
    return s[h:, w:] - s[:-h, w:] - s[h:, :-w] + s[:-h, :-w]


def flash_faults(rgb, times, px, v):
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


def with_label(js, label_js):
    return js.replace("LABEL", label_js, 1)


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

PANS_ITSELF_JS = r"""
([x, y]) => {
  for (let el = document.elementFromPoint(x, y); el; el = el.parentElement) {
    const t = getComputedStyle(el).touchAction;
    if (t !== 'auto' && t !== 'manipulation' && !/pan-(y|up|down)/.test(t)) return true;
  }
  return false;
}
"""

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

TOPS_JS = r"""
() => {
  return window.__tracked.map(({ el }) => {
    const r = el.getBoundingClientRect();
    return r.bottom > 0 && r.top < innerHeight && r.height ? r.top : null;
  });
}
"""

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

FINISH_JS = r"""
() => document.getAnimations().forEach((a) => {
  if (Number.isFinite(a.effect.getComputedTiming().endTime)) a.finish();
})
"""

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

CONTROL_AT_JS = r"""
(i) => {
  const el = window.__controls[i];
  el.scrollIntoView({ block: 'center', behavior: 'instant' });
  document.getAnimations().forEach((a) => window.__before.add(a));
  const r = el.getBoundingClientRect();
  return [r.left + r.width / 2, r.top + r.height / 2];
}
"""

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

CENTRE_JS = r"""
([sel, show]) => {
  const e = document.querySelector(sel);
  if (show) e.scrollIntoView({ block: 'center', behavior: 'instant' });
  const r = e.getBoundingClientRect();
  return [r.left + r.width / 2, r.top + r.height / 2];
}
"""

POINT_JS = (
    "([x, y]) => {"
    + "LABEL"
    + r"""
  const el = document.elementFromPoint(x, y);
  return el ? label(el) : 'the screen';
}
"""
)

AT_JS = "const at = (el, axis) => el.getBoundingClientRect()[axis] + (axis === 'top' ? scrollY : scrollX);"
WHERE_JS = (
    "([sel, axis]) => {" + AT_JS + " return at(document.querySelector(sel), axis); }"
)

PATH_STILL_PX = 0.5  # guess, #501
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
    if (Math.abs(p - path[path.length - 1]) > """
    + str(PATH_STILL_PX)
    + r""") last = now;
    path.push(p);
    if (now - last >= still || now - t0 >= cap) window.__path = path;
    else requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}
"""
)

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


def answers(lines, got):
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
