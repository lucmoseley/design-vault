#!/usr/bin/env python3
"""Measures how a candidate's motion flows: whether it keeps one continuous
pace, or changes speed with what is happening, and never strings long pauses
between sudden jolts.

USAGE
  python3 check-flow.py <url or file> --out DIR [--fps N] [--pause-ms MS]
        [--jolt-ratio R] [--view-cm CM] [--quiet MS] [--wait SEL]
        [--timeout MS] [--viewport WxH] [--reduced-motion]
  python3 check-flow.py <url or file> --out DIR --records [--parts FILE]
        [--table FILE] [--timeout MS] [--viewport WxH]

It opens the page in the machine-wide Python Playwright. It lets the page play
until every animation has finished, every script timer (setTimeout) has fired
and nothing new has started for --quiet ms since its first frame, then scrolls
the page through once. Then it pauses every Web Animations API animation the
page made, seeks them all to each frame in turn, and reads the box and the
animated properties of each moving element. It prints:

- the pauses: spells over --pause-ms (250) after the first move where nothing
  on the page moves. A box is still below the lower of 1% of its top speed and
  1 minute of arc a second seen from --view-cm (60) cm;
- the jolts: a move from rest whose first or last frame runs at or over its
  jolt line, the share of the move's top speed JOLT_BAND sets, lower for a
  longer move and absent for one under 200 ms; --jolt-ratio R sets one line at
  every length. A move that turns back, still for no longer than --pause-ms,
  starts from the speed it turned at, and one still for two frames or fewer
  has not stopped;
- the jumps: a move from rest whose first frame carries its box 0.26° of
  visual angle or more seen from --view-cm, about 10 px at 60 cm, whatever its
  share. A start or stop the viewer never sees at rest, outside the viewport,
  outside a box that clips it or at zero opacity, is judged neither way, and
  is listed where it would have been a jolt or jump;
- the speed steps: a move that holds one speed for three frames, then within
  one to three frames changes 1.3-fold or more beyond the trend of the frames
  either side, at a fifth or more of its top speed, carrying on the same way;
- the length of the motion: from its first move to the last animation's end.

and writes DIR/speed.svg, a speed-over-time chart for each element, and
DIR/flow.json, every sample behind it.

IT MEASURES WEB ANIMATIONS API MOTION: `element.animate()`, CSS animations and
CSS transitions. It also measures a morph, a path whose `d` a script rewrites
frame by frame: it records the `d` written at each frame while the page plays,
measures the morph's speed only between the frames the browser drew it in, and
writes every frame's `d` to DIR/morph.svg for check-curves.js. Where the
browser drops two or more of a morph's frames in a row, the page is loaded
again, up to ATTEMPTS times in all, and then the stretch is listed as not
measured and no jolt, jump or step rests on it. A page that also moves another
way gets no list of findings. It says it cannot measure, and names why: a
canvas, a video, an embedded document, SVG SMIL, shadow DOM, a scroll-driven
timeline, an animation played in reverse or seeked by hand from a script, one
CSS animation-play-state holds paused, an element other than a path's `d` that
a script rewrites frame by frame, a morph that scrolling drives, whose command
structure changes or whose frame loop never stops, or animations that start, or
are released, when the page is scrolled, or keep starting. An animated GIF is
not detected.

Time zero is the page's first frame.

--records answers the motion rule records instead: each line of
check-flow.table, or --table FILE, names a record, a check of
motion-records.py and the value from that record, and each check runs on a
load of its own at --viewport, the carousel's also at check-layout.py's phone
width. A wheel turn over the window's middle must move the page by the turn,
and a Page Down and a touch drag must move it, none cancelled
(vault.native-scroll). The page is scrolled down a step at a time, back up and
down again: an element moving at a rate neither the page's nor none for the
table's run of steps is parallax, a fault on text or a control, and a parallax
layer whose animation or transition runs again on the second way down replays,
unless it also runs with the page at rest (vault.parallax). The declared
carousel is watched on the page's clock: it must not advance at phone width,
under the record's, and at --viewport, which must be no narrower than that,
each frame must hold the record's time for its words and stay put while
hovered, while focused and after its next or previous control is clicked
(vault.carousel-timing). Each screen is filmed by Chromium's screencast at the
table's screen size, and a one-second window fails where the cells holding
more than three flashes' transitions, general or red, cover more than a
quarter of some 10° field (vault.flash-limit, WCAG 2.2's 2.3.1 thresholds).
Each declared bottom sheet and card is dragged slowly to find where it rests,
then flung: it must settle on the rest its projection picks, set off the way
it was thrown and not overshoot (vault.drag-release). Each link, button and
menu item is hovered and pressed, and the motion it starts must end inside the
record's time (vault.motion-frequency). Every animation and transition rule
must sit inside @media (update: fast), and no script animation may run once
matchMedia says the screen updates slowly (vault.slow-update). A record whose
part the declaration does not give is not judged. It prints each fault with
its fix, writes DIR/motion.json and exits 0 with no fault, 1 with one.

EXITS 0 measured, no pause, jolt, jump or step / 1 measured, one or more (each
printed) / 2 the arguments are wrong / 3 Playwright or its browser is missing,
or, for --records, numpy or Pillow / 4 the page did not render in time / 5 the
browser refused the page / 6 the page cannot be measured / 7 a call hung that
would never return, or its renderer died. Exits 0, 1 and 6 are results and
print on stdout; the rest print on stderr.
An exception it does not handle once loaded exits 2, its traceback on stderr.
"""

import argparse
import base64
import importlib
import io
import itertools
import json
import math
import os
import pathlib
import re
import sys
import time

QUIET_MS = 2000  # guess, #141
POLL_MS = 100  # guess, #182
REWRITE_FRAMES = 5  # guess, #60
REWRITE_SPAN_MS = 250  # guess, #60
REWRITE_CHAIN = 2  # guess, #617
ATTEMPTS = 3  # guess, #126
NAMES_SHOWN = 3  # guess, #182

COLLECTOR_JS = r"""
(() => {
  const seen = new Map();
  const rewrites = new Map();
  const morphs = new Map();
  const pending = new Map();
  const state = { seen, rewrites, morphs, pending, frame: 0, firstFrame: null, frameAt: null, prevFrameAt: null,
    lastNew: 0, lastPageFrame: -1, stopped: false, link: null, links: 0 };
  window.__flow = state;
  const setT = window.setTimeout;
  const clearT = window.clearTimeout;
  window.setTimeout = function (fn, ms, ...args) {
    const id = setT.call(this, function (...a) {
      pending.delete(id);
      state.lastNew = performance.now();
      return typeof fn === 'function' ? fn.apply(this, a) : (0, eval)(String(fn));
    }, ms, ...args);
    pending.set(id, performance.now() + (Number(ms) || 0));
    return id;
  };
  window.clearTimeout = function (id) { pending.delete(id); return clearT.call(this, id); };
  // #135 #326
  const raf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function (cb) {
    state.lastPageFrame = state.frame;
    if (typeof cb !== 'function') return raf(cb);
    // #617
    const link = { id: ++state.links, from: state.link && state.link.id, cb };
    return raf((t) => {
      state.link = link;
      try { return cb(t); } finally { state.link = null; state.take(link); state.scan(t); }
    });
  };
  state.raf = raf;
  state.neverStarted = () => [...seen].filter(([a, rec]) => a.startTime === null && rec.start === null && a.playState === 'paused').map(([a]) => a);
  state.markSweep = () => {
    state.scan();
    state.sweptFrom = performance.now();
    state.pausedAtSweep = state.neverStarted();
    return seen.size;
  };
  // #368
  const keep = (a) => {
    if (!seen.has(a)) {
      const rec = { start: null, held: null, ended: false };
      seen.set(a, rec);
      a.addEventListener('finish', () => { rec.ended = true; });
      state.lastNew = performance.now();
    }
    return seen.get(a);
  };
  // #326
  state.scan = (at) => {
    for (const a of document.getAnimations()) {
      const rec = keep(a);
      if (a.startTime !== null) rec.start = a.startTime;
      else if (at !== undefined && rec.held === null && a.pending && a.playState === 'running') rec.held = at;
    }
  };
  // #359
  const rev = Animation.prototype.reverse;
  Animation.prototype.reverse = function () {
    rev.call(this);
    const el = this.effect && this.effect.target;
    if (el && el.isConnected) keep(this);
  };
  // #369
  const afterPaint = new MessageChannel();
  afterPaint.port1.onmessage = () => state.scan();
  const collect = (now) => {
    if (state.firstFrame === null) state.firstFrame = now;
    state.prevFrameAt = state.frameAt;
    state.frameAt = now;
    state.frame++;
    state.scan(now);
    afterPaint.port2.postMessage(null);
    if (!state.stopped) raf(collect);
  };
  raf(collect);
  const WATCHED = ['style', 'class', 'transform', 'd', 'points', 'x', 'y', 'cx', 'cy', 'r',
    'rx', 'ry', 'x1', 'y1', 'x2', 'y2', 'width', 'height', 'opacity', 'offset', 'fill',
    'stroke', 'stroke-width', 'stroke-dasharray', 'stroke-dashoffset', 'viewBox', 'href', 'src'];
  const observer = new MutationObserver((records) => record(records, null));
  const record = (records, link) => {
    if (state.stopped) return;
    for (const m of records) {
      const value = m.target.getAttribute(m.attributeName);
      if (m.oldValue === value) continue;
      if (m.attributeName === 'd') {
        const log = morphs.get(m.target) || [];
        const last = log[log.length - 1];
        if (last && last.frame === state.frame) last.value = value;
        else log.push({ frame: state.frame, at: performance.now(), frameAt: state.frameAt, prevFrameAt: state.prevFrameAt, old: m.oldValue, value });
        morphs.set(m.target, log);
        state.lastNew = performance.now();
        continue;
      }
      const log = rewrites.get(m.target) || [];
      const last = log[log.length - 1];
      if (!last || last.frame !== state.frame) {
        const prior = last && last.link;
        const chained = link && prior && link.from === prior.id && link.cb === prior.cb;
        log.push({ frame: state.frame, at: performance.now(), frameAt: state.frameAt, link, chain: chained ? last.chain + 1 : 1 });
      }
      rewrites.set(m.target, log);
    }
  };
  state.take = (link) => record(observer.takeRecords(), link);
  observer.observe(document, { subtree: true, attributes: true, attributeOldValue: true,
    attributeFilter: WATCHED });
})();
"""

LABEL_JS = r"""
const label = (el, pseudo) => {
  const one = (e) => {
    let s = e.localName;
    if (e.id) return s + '#' + e.id;
    const cls = [...e.classList].slice(0, 2);
    if (cls.length) s += '.' + cls.join('.');
    const same = e.parentElement ? [...e.parentElement.children].filter((c) => c.localName === e.localName) : [];
    if (same.length > 1) s += ':nth-of-type(' + (same.indexOf(e) + 1) + ')';
    return s;
  };
  const parts = [one(el)];
  // guess, #501
  for (let p = el.parentElement; p && parts.length < 3 && !el.id; p = p.parentElement) {
    if (p.localName === 'body' || p.localName === 'html') break;
    parts.unshift(one(p));
    if (p.id) break;
  }
  return parts.join(' > ') + (pseudo || '');
};
"""

# #610
CSS_PAUSED_JS = r"""
const cssPaused = (a) => {
  if (!(a instanceof CSSAnimation) || !a.effect || !a.effect.target) return false;
  const { target, pseudoElement } = a.effect;
  const style = getComputedStyle(target, pseudoElement);
  const splitList = (v) => v.split(',').map((x) => x.trim());
  const states = splitList(style.animationPlayState);
  const twins = target.getAnimations({ subtree: true }).filter((b) => b instanceof CSSAnimation && b.effect.target === target && b.effect.pseudoElement === pseudoElement && b.animationName === a.animationName);
  let nth = twins.indexOf(a);
  const entry = splitList(style.animationName).findIndex((n) => n === a.animationName && nth-- === 0);
  return entry >= 0 && states[entry % states.length] === 'paused';
};
"""

LOOP_JS = (
    f"const LOOP = {json.dumps({'frames': REWRITE_FRAMES, 'span': REWRITE_SPAN_MS, 'chain': REWRITE_CHAIN})};"
    + r"""
const loop = (log) => log.some((w, i) => {
  if (w.chain >= LOOP.chain) return true;
  const run = log.slice(i, i + LOOP.frames);
  const last = run[LOOP.frames - 1];
  // #617
  const close = run.every((x, k) => k === 0 || x.frameAt - run[k - 1].frameAt < LOOP.span);
  return last && (last.at - w.at <= LOOP.span || (last.frame - w.frame === LOOP.frames - 1 && close));
});
"""
)

STATUS_JS = (
    r"""
() => {
  """
    + LOOP_JS
    + r"""
  const f = window.__flow;
  f.scan();
  let running = 0;
  for (const a of f.seen.keys()) {
    const t = a.effect && a.effect.getComputedTiming();
    if (a.playState === 'running' && a.timeline === document.timeline && t && t.endTime !== Infinity) running++;
  }
  const now = performance.now();
  const timers = [...f.pending.values()].map((due) => Math.max(0, due - now));
  const morphed = [...f.morphs.values()].some(loop);
  // #469
  const logs = [...f.rewrites.values()];
  const looped = logs.some(loop);
  const rewriting = logs.some((log) => {
    const [last, prev] = log.slice(-2).reverse();
    return last.frame === f.frame && (!prev || prev.frame === last.frame - 1);
  });
  return { now, firstFrame: f.firstFrame, lastNew: f.lastNew, running, timer: timers.length ? Math.max(...timers) : null,
    framing: morphed && f.lastPageFrame >= f.frame, looped, rewriting };
}
"""
)

DRAWN_JS = r"""
const listed = (names, shown) => names.slice(0, shown).join(', ') + (names.length > shown ? ', …' : '');
const listing = (els, shown) => listed(els.map((e) => label(e)), shown);
const looping = (logs) => [...logs].filter(([, log]) => loop(log)).map(([e]) => e);
const drawn = (f, { shown, morphs }) => {
  const reasons = [];
  const visible = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const kinds = [
    ['canvas', 'draws on a canvas', true],
    ['video', 'plays a video', true],
    ['iframe, object, embed', 'embeds another document', true],
    ['animate, animateTransform, animateMotion, set', 'animates SVG with SMIL', false],
  ];
  for (const [sel, why, onlyVisible] of kinds) {
    const els = [...document.querySelectorAll(sel)].filter((e) => !onlyVisible || visible(e));
    if (els.length) reasons.push(why + ' (' + listing(els, shown) + ')');
  }
  const shadowed = [...document.querySelectorAll('*')].filter((e) => e.shadowRoot);
  if (shadowed.length) reasons.push('has shadow DOM (' + listing(shadowed, shown) + ')');
  const rewritten = looping(f.rewrites);
  if (rewritten.length) reasons.push('moves ' + rewritten.length + ' element(s) by rewriting their style or attributes from a script, frame by frame (' + listing(rewritten, shown) + ')');
  const morphed = morphs ? looping(f.morphs) : [];
  if (morphed.length) reasons.push('morphs ' + morphed.length + ' path(s) by rewriting their d from a script, frame by frame (' + listing(morphed, shown) + ')');
  return reasons;
};
"""

UNSEEKABLE_JS = (
    r"""
({ before, shown }) => {
  """
    + LABEL_JS
    + LOOP_JS
    + DRAWN_JS
    + CSS_PAUSED_JS
    + r"""
  const f = window.__flow;
  f.scan();
  f.stopped = true;
  const reasons = drawn(f, { shown, morphs: false });
  const scrolled = [...f.seen.keys()].filter((a) => a.timeline !== document.timeline);
  if (scrolled.length) reasons.push('drives ' + scrolled.length + ' animation(s) by scroll position, not time');
  const reversed = [...f.seen.keys()].filter((a) => a.playbackRate <= 0);
  if (reversed.length) reasons.push('plays ' + reversed.length + ' animation(s) in reverse or at zero speed');
  const paused = f.neverStarted();
  const held = paused.filter(cssPaused);
  const seeked = paused.filter((a) => !held.includes(a));
  if (seeked.length) reasons.push('holds ' + seeked.length + ' paused animation(s) that a script seeks by hand');
  if (held.length) reasons.push('holds ' + held.length + ' animation(s) CSS animation-play-state keeps paused (' + listed([...new Set(held.map((a) => label(a.effect.target, a.effect.pseudoElement)))].sort(), shown) + '), which play only once something such as a scroll or a click releases them');
  f.morphing = looping(f.morphs);
  const scrollMorphed = f.morphing.filter((e) => f.morphs.get(e).some((w) => w.at >= f.sweptFrom));
  if (scrollMorphed.length) reasons.push('rewrites the d of ' + scrollMorphed.length + ' path(s) when the page is scrolled (' + listing(scrollMorphed, shown) + ')');
  const started = before === null ? 0 : f.seen.size - before + f.pausedAtSweep.filter((a) => a.playState !== 'paused' || f.seen.get(a).start !== null).length;
  if (started) reasons.push('starts ' + started + ' animation(s) when the page is scrolled');
  return reasons;
}
"""
)

PREPARE_JS = (
    r"""
() => {
  """
    + LABEL_JS
    + r"""
  const f = window.__flow;
  const anims = [];
  for (const [a, rec] of f.seen) {
    const start = a.startTime !== null ? a.startTime : rec.start;
    if (start === null || !a.effect) continue;
    anims.push({ a, start, held: rec.held, rate: a.playbackRate });
  }
  // #72
  const morphs = f.morphing.map((el) => ({ el, writes: f.morphs.get(el).filter((w) => w.frameAt !== null) }));
  if (!anims.length && !morphs.length) return { anims: 0, morphs: [] };
  const t0 = Math.min(f.firstFrame === null ? Infinity : f.firstFrame, ...anims.map((x) => x.start),
    ...morphs.map((m) => m.writes[0].frameAt));
  let end = 0;
  let infinite = false;
  let first = Infinity;
  const edges = [];
  const starts = [];
  for (const m of morphs) {
    const w0 = m.writes[0];
    first = Math.min(first, (w0.prevFrameAt === null ? w0.frameAt : w0.prevFrameAt) - t0);
    end = Math.max(end, m.writes[m.writes.length - 1].frameAt - t0);
  }
  for (const x of anims) {
    x.a.pause();
    const t = x.a.effect.getComputedTiming();
    const off = x.start - t0;
    const movesAt = off + Math.max(0, t.delay) / x.rate;
    starts.push([off, movesAt]);
    first = Math.min(first, movesAt);
    x.loops = t.endTime === Infinity;
    if (x.loops) {
      infinite = true;
      end = Math.max(end, off + (t.delay + t.duration) / x.rate);
    } else {
      end = Math.max(end, off + t.endTime / x.rate);
      edges.push(off + (t.delay + t.activeDuration) / x.rate);
    }
    edges.push(off + t.delay / x.rate);
    if (t.easing === 'linear' && t.duration > 0) {
      const offsets = x.a.effect.getKeyframes().map((k) => k.computedOffset);
      // guess, #501
      const passes = Math.min(x.loops ? 1 : t.iterations, 100);
      for (let i = 0; i < passes; i++) {
        const back = t.direction === 'reverse' || (t.direction === 'alternate' && i % 2 === 1) ||
          (t.direction === 'alternate-reverse' && i % 2 === 0);
        for (const o of offsets) edges.push(off + (t.delay + t.duration * (i + (back ? 1 - o : o))) / x.rate);
      }
    }
    x.off = off;
    x.heldOff = x.held === null ? Infinity : x.held - t0;
  }
  const length = infinite ? null : end - first;
  const SKIP = new Set(['offset', 'computedOffset', 'easing', 'composite']);
  const byEl = new Map();
  for (const x of anims) {
    const el = x.a.effect.target;
    if (!el) continue;
    const pseudo = x.a.effect.pseudoElement || null;
    if (!byEl.has(el)) byEl.set(el, new Map());
    const entry = byEl.get(el);
    if (!entry.has(pseudo)) entry.set(pseudo, { props: new Set(), loops: false });
    const slot = entry.get(pseudo);
    slot.loops = slot.loops || x.loops;
    for (const kf of x.a.effect.getKeyframes()) for (const p of Object.keys(kf)) if (!SKIP.has(p)) slot.props.add(p);
  }
  const elements = [];
  for (const [el, entry] of byEl) for (const [pseudo, slot] of entry) {
    elements.push({ el, pseudo, props: [...slot.props], loops: slot.loops, label: label(el, pseudo), channels: {}, seen: [] });
  }
  f.sampling = { anims, elements };
  const rel = (t) => (t === null ? null : t - t0);
  return { anims: anims.length, first, length, infinite, end, edges, starts, morphs: morphs.map((m) => ({
    label: label(m.el), writes: m.writes.map((w) => ({ ms: rel(w.frameAt), prev_ms: rel(w.prevFrameAt), old: w.old, value: w.value })),
  })) };
}
"""
)

SEEN_JS = r"""
const shown = (el) => {
  const r = el.getBoundingClientRect();
  let [l, t, rt, b] = [Math.max(r.left, 0), Math.max(r.top, 0), Math.min(r.right, innerWidth), Math.min(r.bottom, innerHeight)];
  let pos = getComputedStyle(el).position;
  for (let p = el.parentElement; p && p !== document.body && p !== document.documentElement; p = p.parentElement) {
    const cs = getComputedStyle(p);
    const holds = pos === 'fixed' ? cs.transform !== 'none'
      : pos === 'absolute' ? cs.position !== 'static' || cs.transform !== 'none' : true;
    const all = cs.clipPath !== 'none' || (cs.maskImage || cs.webkitMaskImage || 'none') !== 'none' ||
      /paint|strict|content/.test(cs.contain);
    const cx = all || (holds && cs.overflowX !== 'visible');
    const cy = all || (holds && cs.overflowY !== 'visible');
    if (cx || cy) {
      const c = p.getBoundingClientRect();
      if (cx) { l = Math.max(l, c.left); rt = Math.min(rt, c.right); }
      if (cy) { t = Math.max(t, c.top); b = Math.min(b, c.bottom); }
    }
    if (holds) pos = cs.position;
  }
  // #297
  return (rt > l || (r.width === 0 && rt === l)) && (b > t || (r.height === 0 && b === t));
};
const seen = (el) => {
  if (getComputedStyle(el).visibility !== 'visible') return false;
  if (el instanceof HTMLElement && !el.getClientRects().length) return false;
  for (let p = el; p; p = p.parentElement) if (Number(getComputedStyle(p).opacity) === 0) return false;
  return shown(el) || [...el.querySelectorAll('*')].some(shown);
};
"""

SAMPLE_JS = (
    r"""
(times) => {
  """
    + SEEN_JS
    + r"""
  const { anims, elements } = window.__flow.sampling;
  for (const t of times) {
    // #326
    for (const x of anims) x.a.currentTime = (t >= x.heldOff ? Math.max(0, t - x.off) : t - x.off) * x.rate;
    for (const e of elements) {
      const push = (n, v) => (e.channels[n] = e.channels[n] || []).push(v);
      if (!e.pseudo) {
        const r = e.el.getBoundingClientRect();
        push('position', [r.x + r.width / 2, r.y + r.height / 2]);
        push('size', [r.width, r.height]);
      }
      const cs = getComputedStyle(e.el, e.pseudo);
      for (const p of e.props) push(p, p.startsWith('--') ? cs.getPropertyValue(p) : cs[p]);
      e.seen.push(seen(e.el));
    }
  }
  return elements.map((e) => ({ label: e.label, loops: e.loops, channels: e.channels, seen: e.seen }));
}
"""
)


def morph_svg(morphs):
    out = ['<svg xmlns="http://www.w3.org/2000/svg">']
    for m in morphs:
        slug = re.sub(r"[^A-Za-z0-9_-]+", "-", m["label"]).strip("-")
        shapes = [("before", m["writes"][0]["old"])] if m["writes"][0]["old"] else []
        shapes += [(f"at-{w['ms']:.0f}ms", w["value"]) for w in m["writes"]]
        for when, d in shapes:
            out.append(f'<path id="{slug}-{when}" d="{esc(d)}"/>')
    out.append("</svg>")
    return "\n".join(out)


PALETTE = ["#2563eb", "#d97706", "#059669", "#db2777", "#7c3aed", "#0891b2", "#65a30d"]


def chart(sample, result, pause_ms):
    times = sample["times"]
    span = max(times[-1], 1)
    # guess, #501
    w, left, right, panel, gap, top = 960, 230, 20, 90, 18, 40
    plot_w = w - left - right
    els = result["elements"]
    h = top + len(els) * (panel + gap) + 30

    def x(t):
        return left + plot_w * t / span

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" font-family="sans-serif" font-size="11">',
        f'<rect width="{w}" height="{h}" fill="#fff"/>',
        f'<text x="{left}" y="18" font-size="13">Speed over time, each line scaled to its own top speed. '
        f"Grey: a pause over {pause_ms} ms. Red circle: a jolt. Red triangle: a jump. Red square: a speed step.</text>",
    ]
    for p in result["pauses"]:
        out.append(
            f'<rect x="{x(p["start"]):.1f}" y="{top - 6}" width="{x(p["end"]) - x(p["start"]):.1f}" '
            f'height="{h - top - 24}" fill="#9ca3af" fill-opacity="0.25"/>'
        )
    for n, el in enumerate(els):
        y0 = top + n * (panel + gap)
        base = y0 + panel
        out.append(
            f'<text x="8" y="{y0 + 12}" font-weight="bold">{esc(el["label"][:34])}</text>'
        )
        out.append(
            f'<line x1="{left}" y1="{base}" x2="{w - right}" y2="{base}" stroke="#d1d5db"/>'
        )
        for c, (name, ch) in enumerate(el["channels"].items()):
            colour = PALETTE[c % len(PALETTE)]
            pts = " ".join(
                f"{x(t):.1f},{base - panel * v / ch['peak']:.1f}"
                for t, v in zip(
                    [(a + b) / 2 for a, b in itertools.pairwise(ch["times"])],
                    ch["rates"],
                    strict=True,
                )
            )
            out.append(
                f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="1.5"/>'
            )
            unit = " px/s" if name in pace.PX_CHANNELS else "/s"
            out.append(
                f'<text x="8" y="{y0 + 28 + 13 * c}" fill="{colour}">{esc(name[:18])}: top {ch["peak"]:.0f}{unit}</text>'
            )
        for j in result["jolts"]:
            if j["element"] == el["label"]:
                out.append(
                    f'<circle cx="{x(j["at"]):.1f}" cy="{base - panel / 2}" r="5" fill="none" stroke="#dc2626" stroke-width="2"/>'
                )
        for j in result["jumps"]:
            if j["element"] == el["label"]:
                cx, cy = x(j["at"]), base - panel / 2
                out.append(
                    f'<path d="M{cx:.1f} {cy - 6:.1f}L{cx + 6:.1f} {cy + 5:.1f}H{cx - 6:.1f}Z" fill="none" stroke="#dc2626" stroke-width="2"/>'
                )
        for st in result["steps"]:
            if st["element"] == el["label"]:
                out.append(
                    f'<rect x="{x(st["at"]) - 5:.1f}" y="{base - panel / 2 - 5}" width="10" height="10" fill="none" stroke="#dc2626" stroke-width="2"/>'
                )
    step = nice_step(span)
    t = 0
    while t <= span + 1e-6:
        out.append(
            f'<text x="{x(t):.1f}" y="{h - 10}" text-anchor="middle" fill="#6b7280">{t / 1000:g} s</text>'
        )
        t += step
    out.append("</svg>")
    return "\n".join(out)


def nice_step(span):
    # guess, #501
    for s in (100, 250, 500, 1000, 2000, 5000, 10000, 30000, 60000):
        if span / s <= 12:
            return s
    return span / 10


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def settle(page, at):
    waited = 0
    while True:
        s = page.evaluate(STATUS_JS)
        if pace.settled(s, at.quiet):
            return s
        if waited >= at.timeout and s["firstFrame"] is None:
            raise runner.PageTimeoutError("no frame drawn")
        if s["timer"] is not None and waited + s["timer"] > at.timeout:
            raise runner.UnmeasurableError(
                [
                    f"sets a script timer that fires {s['timer']:.0f} ms from now, past --timeout; "
                    "raise --timeout to measure what it starts"
                ]
            )
        if waited >= at.timeout and s["framing"]:
            raise runner.UnmeasurableError(
                [
                    f"keeps the frame loop that morphs a path running after {at.timeout} ms, "
                    "so its morph has no end to measure"
                ]
            )
        if waited >= at.timeout:
            raise runner.UnmeasurableError(
                [
                    f"keeps starting or running animations, or rewriting a path's d, after {at.timeout} ms, "
                    "so its motion has no end to measure"
                ]
            )
        page.wait_for_timeout(POLL_MS)
        waited += POLL_MS


# #135
SWEEP_JS = r"""
async (stops) => {
  for (const y of stops) {
    scrollTo(0, y);
    await new Promise((done) => window.__flow.raf(done));
  }
}
"""


def sweep(page):
    height = page.evaluate("() => document.documentElement.scrollHeight - innerHeight")
    if height <= 0:
        return
    # guess, #501
    step = max(100, height / 40)
    stops = [min(height, step * k) for k in range(1, math.ceil(height / step) + 1)]
    page.evaluate(SWEEP_JS, stops + stops[-2::-1] + [0])
    page.wait_for_timeout(300)


def measure(at):
    with runner.chromium() as browser:
        context = browser.new_context(
            viewport=at.viewport_size,
            reduced_motion="reduce" if at.reduced_motion else "no-preference",
        )
        context.set_default_timeout(at.timeout)
        context.add_init_script(COLLECTOR_JS)
        for attempt in range(ATTEMPTS):
            page = context.new_page()
            page.goto(at.url, wait_until="load")
            if at.wait:
                page.wait_for_selector(at.wait)
            looped = settle(page, at)["looped"]
            before = None
            if not looped:
                before = page.evaluate("() => window.__flow.markSweep()")
                sweep(page)
            reasons = page.evaluate(
                UNSEEKABLE_JS,
                {
                    "before": before,
                    "shown": NAMES_SHOWN,
                },
            )
            if reasons:
                raise runner.UnmeasurableError(reasons)
            sample = page.evaluate(PREPARE_JS)
            if attempt == ATTEMPTS - 1 or not any(
                pace.dropped_frames(m["writes"]) for m in sample["morphs"]
            ):
                break
            page.close()
        if sample["anims"] or sample["morphs"]:
            sample["times"] = pace.sample_times(
                sample["end"],
                sample["edges"],
                at.fps,
                sample["starts"],
            )
            sample["elements"] = page.evaluate(SAMPLE_JS, sample["times"])
    if not sample["anims"] and not sample["morphs"]:
        raise runner.UnmeasurableError(
            ["has no Web Animations API animation and no path a script morphs"]
        )
    pace.add_morphs(sample)
    return sample


def report(at, sample, result, *, svg_path, json_path, morph_path):
    lines = [f"check-flow: {at.url}"]
    n = len(sample["elements"])
    lines.append(
        f"measured {sample['end']:.0f} ms at {at.fps} fps: {n} moving element(s), {sample['anims']} animation(s), "
        f"{len(sample['morphs'])} morph(s)"
    )
    if sample["infinite"]:
        lines.append(
            f"length: loops forever; one pass of every loop ends at {sample['end']:.0f} ms"
        )
    else:
        lines.append(
            f"length: {sample['length']:.0f} ms, from the first move at {sample['first']:.0f} ms"
        )
    pauses, jolts = result["pauses"], result["jolts"]
    lines.append(
        f"pauses, nothing moving for over {at.pause_ms} ms: {len(pauses) or 'none'}"
    )
    for p in pauses:
        lines.append(
            f"  {p['start']}–{p['end']} ms ({p['ms']} ms)"
            + (f", {p['where']}" if p["where"] else "")
        )
    line_text = (
        f"{at.jolt_ratio:.0%}"
        if at.jolt_ratio is not None
        else "its line, a share that falls as the move lengthens"
    )
    lines.append(
        f"jolts, a move from rest, or out of a turn, that starts or stops at {line_text} or more of its top speed: {len(jolts) or 'none'}"
    )
    for j in jolts:
        if j.get("turn"):
            lines.append(
                f"  {j['element']} turns and starts back at {j['at']} ms {j['share']:.0%} of its top speed faster than it turned, "
                f"line {j['line']:.0%} ({', '.join(j['channels'])})"
            )
        else:
            lines.append(
                f"  {j['element']} {j['edge']} at {j['at']} ms at {j['share']:.0%} of its top speed, line {j['line']:.0%} ({', '.join(j['channels'])})"
            )
    jumps = result["jumps"]
    lines.append(
        f"jumps, a move from rest whose first frame carries its box {pace.jump_px(at.view_cm):.0f} px ({pace.JUMP_DEG}° from {at.view_cm:g} cm) or more: {len(jumps) or 'none'}"
    )
    for j in jumps:
        lines.append(
            f"  {j['element']} starts at {j['at']} ms, {j['px']:g} px in its first frame"
        )
    unseen = result["unseen"]
    if unseen:
        lines.append(
            "not judged, where the viewer never sees the element at rest (outside the viewport, clipped or at zero opacity):"
        )
        for u in unseen:
            lines.append(
                f"  {u['element']} {u['edge']} at {u['at']} ms, which would be a {' and a '.join(u['would_be'])} ({', '.join(u['channels'])})"
            )
    steps = result["steps"]
    lines.append(
        f"speed steps, a move whose held speed changes {pace.STEP_RATIO:g}-fold or more within {pace.STEP_SPREAD} frames, beyond the trend either side: {len(steps) or 'none'}"
    )
    for st in steps:
        lines.append(
            f"  {st['element']} steps {st['way']} at {st['at']} ms, from {st['from']:.0%} to {st['to']:.0%} of its top speed ({', '.join(st['channels'])})"
        )
    dropped = [
        (e["label"], name, a, b)
        for e in sample["elements"]
        for name, stretches in e.get("dropped", {}).items()
        for a, b in stretches
    ]
    if dropped:
        lines.append(
            f"not measured, where the browser dropped frames on the last of {ATTEMPTS} loads, each of which dropped some; "
            "a busy machine drops frames, so measure again when it is quieter:"
        )
        for label, name, a, b in dropped:
            lines.append(f"  {label} {a:.0f}–{b:.0f} ms ({name})")
    lines.append(f"chart: {svg_path}  samples: {json_path}")
    if morph_path:
        lines.append(
            f"every frame's d of each morph: {morph_path}; run check-curves.js on it"
        )
    return "\n".join(lines)


HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402
from crash_exit import run_main  # noqa: E402

TABLE = os.path.join(HERE, "check-flow.table")


pace = siblings.load(HERE, "flow-pace.py")
records = siblings.load(HERE, "motion-records.py")
pointer = siblings.load(HERE, "drive-pointer.py")
runner = siblings.load(HERE, "runner.py")
conditions = siblings.load(HERE, "conditions.py")

TRACK_CAP = 400  # guess, #318
STOP_CAP = 80  # guess, #318
CONTROL_CAP = 30  # guess, #318
SCREEN_CAP = 6  # guess, #318
CELL_PX = 4  # guess under WCAG's 0.1° fine-pattern limit, about 4 px at 60 cm, #318
SETTLE_MS = 3000  # guess, #318
CLOCK_STEP_MS = 100  # guess, #318
STILL_MS = 300  # guess, #318
SLOW_DRAGS = (-200, -80, 80, 200)  # guess, #318
PROBE_DRAG = -80
PATH_CAP_MS = 3000  # guess, #318
FLING_PX = 40  # guess, #318
FLING_FRAMES = 3
TOUCH_MOVES = 10  # guess, #318
DRAG_FRAME_MS = 16  # guess, #318
RELEASE_HORIZON_MS = 100  # measured: Android VelocityTracker's 100 ms HORIZON, #478
FLING_TRIES = 3  # guess, #478


class Opener:
    def __init__(self, browser, at):
        self.browser, self.at, self.contexts = browser, at, []

    def __call__(self, viewport, *, extra=None, init=(), clock=False):
        ctx = self.browser.new_context(viewport=viewport, **(extra or {}))
        self.contexts.append(ctx)
        for js in init:
            ctx.add_init_script(js)
        if clock:
            ctx.clock.install()
        page = ctx.new_page()
        page.set_default_timeout(self.at.timeout)
        page.goto(self.at.url, wait_until="load", timeout=runner.LOAD_TIMEOUT_MS)
        page.evaluate("document.fonts.ready.then(() => 0)")
        return page

    def close(self):
        for ctx in self.contexts:
            ctx.close()
        self.contexts = []


def _settle(page):
    page.evaluate(records.SETTLE_JS, SETTLE_MS)


def _touch_point(page, v):
    size = page.viewport_size
    return size["width"] / 2, size["height"] / 2 + v["wheel"] / 2


def _scroll_once(page, name, v):
    if name == "wheel":
        pointer.wheel(page, None, dy=v["wheel"])
    elif name == "key":
        page.keyboard.press("PageDown")
    else:
        x, y = _touch_point(page, v)
        cdp = page.context.new_cdp_session(page)

        def touch(kind, at):
            cdp.send("Input.dispatchTouchEvent", {"type": kind, "touchPoints": at})

        touch("touchStart", [{"x": x, "y": y}])
        for i in range(1, TOUCH_MOVES + 1):
            page.wait_for_timeout(DRAG_FRAME_MS)
            touch("touchMove", [{"x": x, "y": y - v["wheel"] * i / TOUCH_MOVES}])
        touch("touchEnd", [])
    page.evaluate(records.SCROLLED_JS, [STILL_MS, SETTLE_MS])


def native_scroll_check(open_page, at, values, phone):
    v = values["native-scroll"]
    got = {}
    for name in records.SCROLL_INPUTS:
        extra = {"has_touch": True} if name == "touch" else None
        page = open_page(at.viewport_size, extra=extra, init=[records.CANCEL_INIT])
        _settle(page)
        before = page.evaluate(records.ROOM_JS)
        if before["nested"]:
            why = f"the window's middle lies over {before['nested']}, which scrolls itself"
            return {"native-scroll": records.Answer(None, False, why)}
        if name == "touch" and page.evaluate(
            records.PANS_ITSELF_JS, _touch_point(page, v)
        ):
            continue
        _scroll_once(page, name, v)
        after = page.evaluate(records.ROOM_JS)
        got[name] = {
            "before": before["y"],
            "after": after["y"],
            "room": before["room"],
            "cancelled": after["cancelled"],
        }
    found = records.native_scroll_faults(got, v)
    return {"native-scroll": records.Answer(found or [], found is not None, None)}


def parallax_check(open_page, at, values, phone):
    v = values["parallax"]
    page = open_page(at.viewport_size)
    _settle(page)
    els = page.evaluate(records.with_label(records.TRACK_JS, LABEL_JS), TRACK_CAP)
    height = page.evaluate("() => document.scrollingElement.scrollHeight - innerHeight")
    if height <= 0 or not els:
        none = records.Answer([], False, None)
        return {"parallax": none, "replay": none}
    step = v["step"]
    stops = sorted(
        {min(height, k * step) for k in range(math.ceil(height / step) + 1)}
    )[:STOP_CAP]

    def sweep(ys, phase):
        page.evaluate("(p) => { window.__phase = p; }", phase)
        tops = []
        for y in ys:
            page.evaluate("(y) => scrollTo({ top: y, behavior: 'instant' })", y)
            _settle(page)
            tops.append(page.evaluate(records.TOPS_JS))
        return tops

    started = time_ms()
    tops = sweep(stops, "down")
    page.evaluate("(p) => { window.__phase = p; window.__ran.idle = {}; }", "idle")
    page.wait_for_timeout(time_ms() - started)
    sweep(stops[::-1], "up")
    sweep(stops, "again")
    first, again = records.replays(page.evaluate("() => window.__ran"))
    track = {
        "scrolls": stops,
        "elements": [{**el, "tops": [t[i] for t in tops]} for i, el in enumerate(els)],
    }
    faults, layers = records.parallax_faults(track, v)
    return {
        "parallax": records.Answer(faults, bool(layers), None),
        "replay": records.Answer(
            records.replay_faults(first, again, layers),
            bool(set(first) & set(layers)),
            None,
        ),
    }


def time_ms():
    return time.monotonic() * 1000


def _watch(page, sel, ms):
    changes, last = [], page.evaluate(records.FRAME_JS, sel)
    for _ in range(math.ceil(ms / CLOCK_STEP_MS)):
        page.clock.run_for(CLOCK_STEP_MS)
        page.evaluate(records.FINISH_JS)
        now = page.evaluate(records.FRAME_JS, sel)
        if now["at"] != last["at"]:
            changes.append((page.evaluate("performance.now()"), now))
        last = now
    return changes


def carousel_check(open_page, at, values, phone):
    v = values["carousel"]
    sel = at.parts["carousel"]
    width, height, touch = phone
    why = records.carousel_widths(width, at.viewport_size["width"], v)
    if why:
        return {"carousel": records.Answer(None, False, why)}
    page = open_page({"width": width, "height": height}, extra=touch, clock=True)
    first = page.evaluate(records.FRAME_JS, sel)
    if first is None:
        why = f"the carousel part's selector {sel} matches nothing"
        return {"carousel": records.Answer(None, False, why)}
    if first["slides"] < 2:
        return {"carousel": records.Answer([], False, None)}
    watch = v["watch"] * 1000
    phone_advances = bool(_watch(page, sel, watch))
    page = open_page(at.viewport_size, clock=True)
    first = page.evaluate(records.FRAME_JS, sel)
    frames = [{"from": 0, "words": first["words"]}] + [
        {"from": t, "words": f["words"]} for t, f in _watch(page, sel, watch)
    ]
    got = {
        "label": sel,
        "phone_advances": phone_advances,
        "phone_width": width,
        "frames": frames,
        "hovered": False,
        "focused": False,
        "after_change": False,
        "control": None,
    }
    if len(frames) > 1:
        page.mouse.move(*page.evaluate(records.CENTRE_JS, [sel, True]))
        got["hovered"] = bool(_watch(page, sel, watch))
        page.mouse.move(0, 0)
        if page.evaluate(records.FOCUS_JS, sel):
            got["focused"] = bool(_watch(page, sel, watch))
            page.evaluate(
                "() => document.activeElement && document.activeElement.blur()"
            )
        got["control"] = page.evaluate(
            records.with_label(records.CHANGE_JS, LABEL_JS), sel
        )
        if got["control"]:
            page.evaluate(records.FINISH_JS)
            got["after_change"] = bool(_watch(page, sel, watch))
    faults = records.carousel_faults(got, v, CLOCK_STEP_MS / 1000)
    return {"carousel": records.Answer(faults, True, None)}


def _film(page, cdp, seconds):
    import numpy as np
    from PIL import Image

    frames = []

    def got(e):
        frames.append((e["metadata"]["timestamp"], e["data"]))
        cdp.send("Page.screencastFrameAck", {"sessionId": e["sessionId"]})

    size = page.viewport_size
    cdp.on("Page.screencastFrame", got)
    cdp.send(
        "Page.startScreencast",
        {
            "format": "png",
            "everyNthFrame": 1,
            "maxWidth": size["width"],
            "maxHeight": size["height"],
        },
    )
    page.wait_for_timeout(seconds * 1000)
    cdp.send("Page.stopScreencast")
    cdp.remove_listener("Page.screencastFrame", got)
    if not frames:
        return np.zeros((0,)), []
    cells = (size["width"] // CELL_PX, size["height"] // CELL_PX)
    rgb = np.stack(
        [
            np.asarray(
                Image.open(io.BytesIO(base64.b64decode(d)))
                .convert("RGB")
                .resize(cells, Image.BOX),
                dtype=np.float64,
            )
            / 255
            for _, d in frames
        ]
    )
    t0 = frames[0][0]
    return rgb, [t - t0 for t, _ in frames]


def flash_check(open_page, at, values, phone):
    v = values["flash"]
    page = open_page({"width": int(v["screen_w"]), "height": int(v["screen_h"])})
    cdp = page.context.new_cdp_session(page)
    screens = min(
        SCREEN_CAP,
        page.evaluate(
            "() => Math.ceil(document.scrollingElement.scrollHeight / innerHeight)"
        ),
    )
    point = records.with_label(records.POINT_JS, LABEL_JS)
    faults, moved = [], False
    for k in range(screens):
        page.evaluate(
            "(k) => scrollTo({ top: k * innerHeight, behavior: 'instant' })", k
        )
        rgb, times = _film(page, cdp, v["watch"])
        if len(times) < 2:
            continue
        if float(abs(rgb[1:] - rgb[:-1]).max()) > 0:
            moved = True
        for f in records.flash_faults(rgb, times, CELL_PX, v):
            x, y, w, h = f["box"]
            faults.append(
                records.fault(
                    "flash",
                    page.evaluate(point, [x + w / 2, y + h / 2]),
                    f"{f['kind']} flashing: {f['transitions']} transitions within one second from "
                    f"{f['from_s']:.1f} s, over {f['share']:.0%} of the {v['field_w']:.0f}x{v['field_h']:.0f} px field at {x},{y} "
                    f"(screen {k + 1})",
                    f"flash at most {v['flashes']:.0f} times in any second, or keep the flashing under "
                    f"{v['share']:.0%} of a {v['field_w']:.0f}x{v['field_h']:.0f} px field",
                )
            )
    return {"flash": records.Answer(faults, moved, None)}


def _rest(page, sel, axis):
    page.evaluate(records.PATH_JS, [sel, axis, STILL_MS, PATH_CAP_MS])
    page.wait_for_function("() => window.__path")
    return page.evaluate("() => window.__path")


def _fling(page, sel, axis, *, way, along):
    dx, dy = along
    x0, y0 = page.evaluate(records.CENTRE_JS, [sel, False])
    page.evaluate(
        "(w) => { window.__watch = w; window.__path = null; }",
        [sel, axis, STILL_MS, PATH_CAP_MS],
    )
    cdp = page.context.new_cdp_session(page)
    frame = DRAG_FRAME_MS / 1000
    t0 = time.time() - (FLING_FRAMES + 1) * frame

    def send(kind, i, buttons):
        cdp.send(
            "Input.dispatchMouseEvent",
            {
                "type": kind,
                "x": x0 + dx * way * FLING_PX * min(i, FLING_FRAMES) / FLING_FRAMES,
                "y": y0 + dy * way * FLING_PX * min(i, FLING_FRAMES) / FLING_FRAMES,
                "button": "left",
                "buttons": buttons,
                "clickCount": 1,
                "timestamp": t0 + i * frame,
            },
        )

    send("mouseMoved", 0, 0)
    send("mousePressed", 0, 1)
    for i in range(1, FLING_FRAMES + 1):
        send("mouseMoved", i, 1)
    send("mouseReleased", FLING_FRAMES + 1, 0)
    cdp.detach()
    page.wait_for_function("() => window.__path")
    path, release = page.evaluate("() => [window.__path, window.__release]")
    return {
        "at": path[0],
        "velocity": records.release_velocity(release, axis, RELEASE_HORIZON_MS),
        "path": path,
    }


def drag_check(open_page, at, values, phone):
    v = values["drag-release"]
    parts = [(n, at.parts[n]) for n in records.DRAG_PARTS if at.parts.get(n)]
    if not parts:
        why = "no bottom-sheet or card part declared with a selector (--parts)"
        return {"drag-release": records.Answer(None, False, why)}
    faults, seen, too_slow = [], False, []
    for name, sel in parts:
        for axis, along in (("top", (0, 1)), ("left", (1, 0))):
            dx, dy = along
            page = open_page(at.viewport_size, init=[records.RELEASE_INIT])
            if not page.query_selector(sel):
                continue
            start = page.evaluate(records.WHERE_JS, [sel, axis])
            pointer.drag(page, sel, (dx * PROBE_DRAG, dy * PROBE_DRAG), hold=True)
            held = page.evaluate(records.WHERE_JS, [sel, axis])
            page.mouse.up()
            if abs(held - start) <= v["slack"]:
                continue
            seen = True
            rests = [start, _rest(page, sel, axis)[-1]]
            for off in SLOW_DRAGS:
                pointer.drag(page, sel, (dx * off, dy * off), hold=True)
                page.mouse.up()
                rests.append(_rest(page, sel, axis)[-1])
            snaps = records.snap_points(rests, v["slack"])
            label = f"{name} {sel}, dragged along its {'height' if axis == 'top' else 'width'}"
            for _ in range(FLING_TRIES):
                here = page.evaluate(records.WHERE_JS, [sel, axis])
                fling = _fling(
                    page, sel, axis, way=records.fling_way(snaps, here), along=along
                )
                if records.picks_another_snap(snaps, fling, v["rate"]):
                    break
            else:
                too_slow.append(label)
            faults += records.drag_faults(
                {"label": label, "snaps": snaps, "fling": fling}, v
            )
    why = (
        f"no fling of {', '.join(too_slow)} was let go fast enough to pick another snap point"
        if too_slow
        else None
    )
    return {"drag-release": records.Answer(faults, seen, why)}


def frequent_check(open_page, at, values, phone):
    v = values["frequent"]
    page = open_page(at.viewport_size)
    _settle(page)
    labels = page.evaluate(
        records.with_label(records.CONTROLS_JS, LABEL_JS), CONTROL_CAP
    )
    changes = []
    for i, name in enumerate(labels):
        for state in ("hover", "press"):
            x, y = page.evaluate(records.CONTROL_AT_JS, i)
            if state == "hover":
                page.mouse.move(x, y)
            else:
                page.mouse.down()
            started = page.evaluate(records.STARTED_JS, i)
            if state == "press":
                page.mouse.move(0, 0)
                page.mouse.up()
            if started["motion"] != records.NO_MOTION:
                changes.append({"label": name, "state": state, **started})
        page.mouse.move(0, 0)
        _settle(page)
    faults = records.frequent_faults(changes, v)
    return {"frequent": records.Answer(faults, bool(changes), None)}


def slow_update_check(open_page, at, values, phone):
    page = open_page(at.viewport_size, init=[records.SLOW_INIT])
    _settle(page)
    got = page.evaluate(records.with_label(records.SLOW_JS, LABEL_JS))
    faults = records.slow_update_faults(got)
    if got["unread"] and not faults:
        why = f"cannot read the stylesheet(s) {', '.join(got['unread'])}"
        return {"slow-update": records.Answer(None, False, why)}
    return {"slow-update": records.Answer(faults, got["any"], None)}


RUNS = {
    "native-scroll": native_scroll_check,
    "parallax": parallax_check,
    "replay": parallax_check,
    "carousel": carousel_check,
    "flash": flash_check,
    "drag-release": drag_check,
    "frequent": frequent_check,
    "slow-update": slow_update_check,
}


def run_records(at):
    phone = (conditions.PHONE_WIDTH, conditions.HEIGHTS[0], conditions.PHONE)
    values = {line.mode: line.value for line in at.lines}
    out = {}
    with runner.chromium() as browser:
        open_page = Opener(browser, at)
        try:
            for mode in values:
                if mode in out:
                    continue
                why = records.missing(mode, at.parts)
                if why:
                    out[mode] = records.Answer(None, False, why)
                    continue
                out.update(RUNS[mode](open_page, at, values, phone))
                open_page.close()
        finally:
            open_page.close()
    return out


def records_main(at):
    try:
        importlib.import_module("numpy")
        importlib.import_module("PIL")
    except ImportError as err:
        sys.exit(runner.missing(err))
    got, code = runner.run_browser(lambda: run_records(at), at.timeout, at.url)
    if code:
        return code
    answer = records.answers(at.lines, got)
    os.makedirs(at.out, exist_ok=True)
    json_path = os.path.join(at.out, "motion.json")
    by_record = {}
    for line in at.lines:
        rec = by_record.setdefault(
            line.id, {"answer": answer[line.id], "faults": [], "not_judged": []}
        )
        mode_answer = got[line.mode]
        rec["faults"] += mode_answer.faults or []
        if mode_answer.unmet:
            rec["not_judged"].append(f"{line.mode}: {mode_answer.unmet}")
    with open(json_path, "w", encoding="utf8") as fh:
        json.dump(
            {"url": at.url, "table": at.table, "records": by_record}, fh, indent=1
        )
    lines = [f"motion records, by {at.table}'s lines:"]
    for rid, rec in by_record.items():
        lines.append(f"  {rid}: {rec['answer']}")
        lines += [
            f"    - {f['subject']}: {f['detail']}. Fix: {f['fix']}."
            for f in rec["faults"]
        ]
        lines += [f"    - not judged, {why}" for why in rec["not_judged"]]
    lines.append(f"wrote {json_path}")
    print("\n".join(lines))
    return 1 if any(a.faults for a in got.values()) else 0


def parse(argv):
    p = argparse.ArgumentParser(
        prog="check-flow.py",
        description="Measure the pauses, jolts, jumps and speed steps in a page's WAAPI motion and path morphs.",
    )
    p.add_argument("url", help="an http(s) URL, or a local HTML file")
    p.add_argument(
        "--out",
        required=True,
        metavar="DIR",
        help="where speed.svg, flow.json and any morph.svg go",
    )
    p.add_argument("--fps", type=int, default=pace.FPS)
    p.add_argument("--pause-ms", type=int, default=pace.PAUSE_MS, metavar="MS")
    p.add_argument(
        "--jolt-ratio",
        type=float,
        metavar="R",
        help="one jolt line at every move length, in place of the line that falls as a move lengthens",
    )
    p.add_argument(
        "--view-cm",
        type=float,
        default=pace.VIEW_CM,
        metavar="CM",
        help="the viewer's distance from the screen, which sets the slowest box speed that counts as motion",
    )
    p.add_argument(
        "--quiet",
        type=int,
        default=QUIET_MS,
        metavar="MS",
        help="how long nothing new must start, from the page's first frame, before measuring",
    )
    p.add_argument("--wait", metavar="SELECTOR")
    p.add_argument("--timeout", type=int, default=runner.PLAY_TIMEOUT_MS, metavar="MS")
    p.add_argument("--viewport", default=conditions.DESKTOP, metavar="WxH")
    p.add_argument(
        "--reduced-motion",
        action="store_true",
        help="measure the page's reduced-motion version",
    )
    p.add_argument(
        "--records",
        action="store_true",
        help="answer the motion rule records check-flow.table names, in place of the flow measures",
    )
    p.add_argument(
        "--parts",
        dest="parts_file",
        metavar="FILE",
        help="with --records: the building session's parts declaration, for the records that read a part",
    )
    p.add_argument(
        "--table", default=TABLE, metavar="FILE", help="with --records: the rule table"
    )
    at = p.parse_args(argv)
    if (
        at.fps < 1
        or not (at.jolt_ratio is None or 0 < at.jolt_ratio <= 1)
        or not at.view_cm > 0
    ):
        p.error(
            "--fps wants 1 or more, --jolt-ratio a number in (0, 1], --view-cm a number above 0"
        )
    at.viewport_size = conditions.size_arg(p, "--viewport", at.viewport)
    at.url = runner.page_url(p, at.url)
    if at.parts_file and not at.records:
        p.error("--parts goes with --records")
    if at.records:
        try:
            with open(at.table, encoding="utf8") as fh:
                at.lines = records.parse_table(fh.read())
        except (OSError, records.TableError) as exc:
            p.error(f"{at.table}: {exc}")
        at.parts = {}
        if at.parts_file:
            probe = siblings.load(HERE, "probe.py")
            try:
                with open(at.parts_file, encoding="utf8") as fh:
                    at.parts = probe.declared_parts(fh.read())[0]
            except (OSError, probe.DeclarationError) as exc:
                p.error(f"--parts {at.parts_file}: {exc}")
    return at


def main(argv):
    at = parse(argv)
    if at.records:
        return records_main(at)
    sample, code = runner.run_browser(
        lambda: measure(at),
        at.timeout,
        at.url,
        (
            f"cannot measure {at.url}. It measures Web Animations API motion and path morphs only, and this page:",
            "Check this page's flow by hand: the timeline table and a scrub at 0.25x.",
        ),
    )
    if code:
        return code
    result = pace.analyse(sample, at.pause_ms, at.jolt_ratio, at.view_cm, fps=at.fps)
    os.makedirs(at.out, exist_ok=True)
    svg_path = os.path.join(at.out, "speed.svg")
    json_path = os.path.join(at.out, "flow.json")
    with open(svg_path, "w", encoding="utf8") as fh:
        fh.write(chart(sample, result, at.pause_ms))
    with open(json_path, "w", encoding="utf8") as fh:
        json.dump(
            {
                "url": at.url,
                "fps": at.fps,
                "pause_ms": at.pause_ms,
                "jolt_ratio": at.jolt_ratio,
                "view_cm": at.view_cm,
                "first_move_ms": sample["first"],
                "length_ms": sample["length"],
                "end_ms": sample["end"],
                "edges_ms": sorted(sample["edges"]),
                "pauses": result["pauses"],
                "jolts": result["jolts"],
                "jumps": result["jumps"],
                "unseen": result["unseen"],
                "steps": result["steps"],
                "times": sample["times"],
                "elements": sample["elements"],
            },
            fh,
        )
    morph_path = os.path.join(at.out, "morph.svg")
    if sample["morphs"]:
        with open(morph_path, "w", encoding="utf8") as fh:
            fh.write(morph_svg(sample["morphs"]))
    else:
        pathlib.Path(morph_path).unlink(missing_ok=True)
        morph_path = None
    print(
        report(
            at,
            sample,
            result,
            svg_path=svg_path,
            json_path=json_path,
            morph_path=morph_path,
        )
    )
    return (
        1
        if result["pauses"] or result["jolts"] or result["jumps"] or result["steps"]
        else 0
    )


if __name__ == "__main__":
    run_main(main)
