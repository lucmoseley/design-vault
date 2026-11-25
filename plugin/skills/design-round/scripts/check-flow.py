#!/usr/bin/env python3
"""check-flow.py — measures how a candidate's motion flows: the craft rule that
motion keeps one continuous pace, or changes speed with what is happening, and
never strings long pauses between sudden jolts (lucmoseley/mmm-infra#16,
design-vault#60, #69).

USAGE
  python3 check-flow.py <url or file> --out DIR [--fps N] [--pause-ms MS]
        [--jolt-ratio R] [--view-cm CM] [--quiet MS] [--wait SEL]
        [--timeout MS] [--viewport WxH] [--reduced-motion]
  python3 check-flow.py <url or file> --out DIR --records [--parts FILE]
        [--table FILE] [--timeout MS] [--viewport WxH]

It opens the page in the machine-wide Python Playwright, the one the vault's
`scripts/browse.py` uses. It lets the page play until
every animation has finished, every script timer (setTimeout) has fired and
nothing new has started for --quiet ms since its first frame, then scrolls the
page through once, so a storyboard sequenced by timers is measured whole. Then
it pauses every Web Animations API animation the page made, seeks them all to
each frame in turn, and reads the box and the animated properties of each
moving element. It prints:

- the pauses: spells over --pause-ms (250) after the first move where nothing
  on the page moves. A box is still below the lower of 1% of its top speed and
  1 minute of arc a second seen from --view-cm (60) cm, the slowest speed seen
  as motion;
- the jolts: a move from rest whose first or last frame runs at or over its
  jolt line, the share of the move's top speed JOLT_BAND sets, lower for a
  longer move and absent for one under 200 ms; --jolt-ratio R sets one line at
  every length. A move that turns back,
  still for no longer than --pause-ms, starts from the speed it turned at, and
  one still for two frames or fewer has not stopped;
- the jumps: a move from rest whose first frame carries its box 0.26° of
  visual angle or more seen from --view-cm, about 10 px at 60 cm, whatever its
  share. A start or stop the viewer never sees at rest, outside the viewport,
  outside a box that clips it or at zero opacity, is judged neither way, and
  is listed where it would have been a jolt or jump;
- the speed steps: a move that holds one speed for three frames, then within
  one to three frames changes 1.3-fold or more beyond the trend of the frames
  either side, at a fifth or more of its top speed, carrying on the same way,
  as a crane arm that suddenly runs faster;
- the length of the motion: from its first move to the last animation's end
  (#169 Q3 (A)), so the wait for fonts before anything moves is not in it.
  That wait is check-load.py's to measure.

and writes DIR/speed.svg, a speed-over-time chart for each element, and
DIR/flow.json, every sample behind it.

IT MEASURES WEB ANIMATIONS API MOTION: `element.animate()`, CSS animations and
CSS transitions. It also measures a morph, a path whose `d` a script rewrites
frame by frame (design-round §6, design-vault#72): it records the `d` written
at each frame while the page plays, interpolates the numbers between frames as
the morph does, and writes every frame's `d` to DIR/morph.svg for
check-curves.js. A morph is known only at the frames the browser drew: where
it drops two or more in a row, as a busy machine makes it, the page is loaded
again, up to ATTEMPTS times in all, and then the stretch is listed as not measured and
no jolt, jump or step rests on it. A page that also moves another way gets no list of findings,
because an empty one would read as a pass. It says it cannot measure, and names
why: a canvas, a video, an embedded document, SVG SMIL, shadow DOM, a
scroll-driven timeline, an animation played in reverse or seeked by hand from a
script, an element other than a path's `d` that a script rewrites frame by
frame, a morph that scrolling drives, whose command structure changes or whose
frame loop never stops, or animations that start when the page is scrolled or
keep starting. An animated GIF is not detected.

Time zero is the page's first frame.

--records answers the motion rule records instead (#318): each line of
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
matchMedia says the screen updates slowly, which Chromium cannot emulate
(vault.slow-update). A record whose part the declaration does not give is not
judged. It prints each fault with its fix, writes DIR/motion.json and exits
0 with no fault, 1 with one.


EXITS 0 measured, no pause, jolt, jump or step / 1 measured, one or more (each
printed) / 2 the arguments are wrong / 3 Playwright or its browser is missing,
or, for --records, numpy or Pillow /
4 the page did not render in time / 5 the browser refused the page / 6 the page
cannot be measured / 7 a call hung that would never return, or its renderer
died. Exits 0, 1 and 6 are results and print on stdout; the rest print on stderr.
"""

import argparse
import base64
import bisect
import contextlib
import importlib.util
import io
import itertools
import json
import math
import os
import pathlib
import re
import signal
import statistics
import sys
import threading
import time
import traceback
import typing

# The craft gate's pause limit: a still spell longer than this, in ms, is a pause
# (design-critique's motion-flow check, #60).
PAUSE_MS = 250
# A move's first or last 60 fps frame at the middle of this band, as a share of
# its top speed, or more starts or stops with a jolt (#221 Q1 (B), #297): (ms,
# low, high) at each move length, the band in which the eye first tells a start
# from an eased one (docs/research/jolt-onset.md, derivation). Straight between
# the lengths, held past the last; a move shorter than the first has no line.
# Residual: the shares are 60 fps frames', so at another --fps the line is off.
JOLT_BAND = (
    (200, 0.80, 0.80),
    (250, 0.54, 0.67),
    (300, 0.43, 0.60),
    (500, 0.27, 0.47),
    (1000, 0.19, 0.39),
    (2000, 0.17, 0.35),
)
# A move from rest whose first frame carries its box this many degrees of visual
# angle or more jumps, whatever its share: the lower end of the jumps that drew
# attention, where the two studies disagree (docs/research/jolt-onset.md F10).
# Read on its box's position only, as the studies moved a whole object. Residual:
# a path morph's first frame is never checked for a jump.
JUMP_DEG = 0.26
# A common display's refresh rate, so the sample holds the frames a viewer sees.
FPS = 60
# How long, in ms, nothing new may start before the page counts as done starting
# things. A guess, unmeasured.
QUIET_MS = 2000
# How often, in ms, the page is asked whether it has settled: a guess, well
# under QUIET_MS.
POLL_MS = 100
# The wait for a whole page, in ms: loaded and, where it moves, played out.
# A guess, unmeasured.
PLAY_TIMEOUT_MS = 60000
# The wait for one load or draw, in ms: Playwright's own default.
LOAD_TIMEOUT_MS = 30000
# The commonest desktop screen (#183's audit §2.1), and the height Windows 11's
# taskbar and Chromium's bars take from it, measured on one machine (#197).
DESKTOP_SCREEN = (1920, 1080)
DESKTOP_BARS = 135
# The desktop viewport every design-round script renders at unless told: that
# screen less its bars (#252). A project whose own visitors differ records its
# screen as `projects.<key>.desktop` in the library (#196).
DESKTOP_WINDOW = (DESKTOP_SCREEN[0], DESKTOP_SCREEN[1] - DESKTOP_BARS)
DESKTOP = f"{DESKTOP_WINDOW[0]}x{DESKTOP_WINDOW[1]}"
# A channel slower than this share of its own top speed counts as still, so an
# easing's long tail does not hide the pause after it. A box channel counts as
# still only below the lower of this and STILL_ARCMIN_S (#196).
STILL_FRACTION = 0.01
# The slowest speed people see as motion, in minutes of arc a second: about 1-2
# with something still in view (Leibowitz 1955, through secondary sources; #183's
# audit §2.1). The band's lower end, a guess.
STILL_ARCMIN_S = 1
# The viewer's distance from the screen, in cm: a desktop's, about 60 (#183's
# audit §2.1). A CSS px is 1/96 inch on a desktop. A phone's is smaller but seen
# nearer, so there the floor reads a little over 1; pass --view-cm to hold 1.
VIEW_CM = 60
CSS_PX_CM = 2.54 / 96
# A speed under this, in the channel's units per second, is float noise (#60).
# Set for a box's 1e-5 px wobble over a gap of 1 ms or more; #149 found gaps
# shorter and wobbles larger, which PX_NOISE now takes. For other channels a guess.
NOISE = 0.02
# A box change under this many px is float noise whatever the rate (#149): a
# still box's size wobbled by float32 steps of up to 1.2e-4 px across a 1.9 ms
# gap on mmm-infra#35's page, whose smallest real move in a frame was 1e-3 px.
# A guess between the two, tuned on that one page; it drops the first frame of
# a 1 px ease-in-out at 120 fps.
PX_NOISE = 5e-4
PX_CHANNELS = ("position", "size")
IDENTITY_3D = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
# A speed step mid-move (#69, #196): a change of STEP_RATIO or more within
# STEP_SPREAD frames, which is visible inside one motion (a Weber fraction of
# 0.2-0.3: Snowden and Braddick 1991, Mateeff et al. 2000, abstracts only; #183's
# audit 1.7). A smooth easing changes speed by 2x a frame near rest, so the
# change is measured against the trend: the line through STEP_SIDE_FRAMES
# frames each side, carried across to the other side's nearest frame, must miss
# it by STEP_RATIO, both lines the same way. The slower side holds within
# STEP_HOLD and the faster within STEP_FAST_HOLD, as the speeds behind the Weber
# fraction were held: a speed peak as sharp as expo's or circ's changes more on
# each side. A turn, as in an overshoot, a bounce or a landing's sink, reverses;
# the floor keeps out a landing's last wobbles.
# Missed: a change ramped over more than 3 frames, and a step within 3 frames
# of a move's start or end, where the slower speed has no three frames to hold,
# which at 30 fps is 100 ms.
STEP_RATIO = 1.3
STEP_SPREAD = 3
STEP_SIDE_FRAMES = 3
STEP_HOLD = 1.3
STEP_FAST_HOLD = 1.5
STEP_FLOOR = 0.2
# A still spell of at most this many frames between two moves going opposite
# ways is a turn inside a frame, not a stop: a stiff landing's sink turns within
# a frame, which reads as still in the frame or two it straddles (#151). A guess.
# Residual: a move that stops at full speed, rests that short and goes back no
# faster is not called a jolt.
TURN_FRAMES = 2
# A script rewriting one element's style in this many distinct frames, within
# REWRITE_SPAN_MS or in consecutive frames however far apart a starved browser
# draws them (#135), is moving it frame by frame. A framework's few setup
# writes and a storyboard's class changes a beat apart stay under it.
# Residual: where frames come a beat or more apart, changes a beat apart land
# in consecutive frames and are refused as a loop.
REWRITE_FRAMES = 5
REWRITE_SPAN_MS = 250
# Across two or more dropped frames in a row, as a busy machine or a page's
# first frames leave, the straight line between the frames either side fakes a
# jolt or step (#126). A frame is the median time between the browser's frames,
# or headless Chromium's 60 Hz frame where that is shorter.
DROPPED_FRAMES = 2
BROWSER_FRAME_MS = 1000 / 60
# The most loads, in all, of a page whose morph keeps dropping DROPPED_FRAMES or
# more frames in a row. A guess.
ATTEMPTS = 3
# How long, in seconds, a Playwright call may wait while its browser runs no
# renderer before the call is taken as hung (#432). A renderer killed as it
# starts can leave the call waiting for ever with nothing raised. Above the few
# seconds a starved machine may take to start one: a guess, unmeasured.
RENDERER_GONE_S = 10
# Playwright calls that take no timeout and return once the renderer answers:
# a renderer alive but never answering leaves one waiting for ever (#459).
# Other calls with no timeout of their own, as evaluate, are not watched: a
# page's own script can rightly keep one waiting. Residual: a CDP send that
# awaits a page's promise, as Runtime.evaluate with awaitPromise, can rightly
# wait past UNANSWERED_S and is killed as hung.
UNTIMED_CALLS = frozenset({"Page.set_viewport_size", "CDPSession.send"})
# How long, in seconds, one of UNTIMED_CALLS may wait before it is taken as hung.
# 3,600 resizes six browsers at once, at a load average of 5 to 11, took 72 ms
# at worst (#459); a guess far above that, and for a CDP send unmeasured (#464).
UNANSWERED_S = 30
# How often, in seconds, the watch reads the browser's processes: a guess, well
# under RENDERER_GONE_S.
WATCH_POLL_S = 0.25
# How long, in seconds, the watch waits for the processes it killed to exit: a
# guess, far over the moment a killed browser takes on a loaded machine.
KILLED_GONE_S = 10
# Elements or animations a message names before it elides the rest: a guess at
# enough to find them.
NAMES_SHOWN = 3
# Not a digit that is part of a name, such as the 3 in `matrix3d(`.
NUMBER = re.compile(r"(?<![A-Za-z_])[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")
# In path data a number follows its command letter directly: `M0 0`.
PATH_NUMBER = re.compile(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")
PATH_COMMAND = re.compile(r"[MmZzLlHhVvCcSsQqTtAa]")

# first_line, the exception classes and size_arg follow the vault's
# scripts/browse.py, which workflow-core owns and the plugin cannot import: keep
# them in step with it. chromium() departs from it: an error while a script
# builds its page is a refusal too (#131), and INSTALL_HINT names the plugin's
# pinned requirements.txt (#254). Every design-round browser script calls
# chromium(), run_browser() and, but check-overlay.py, page_url() from here.
REQUIREMENTS = pathlib.Path(__file__).resolve().parents[3] / "requirements.txt"
INSTALL_HINT = (
    "Playwright is a Python package installed once per machine, at the\n"
    "versions the plugin pins:\n"
    f"    python3 -m pip install -r {REQUIREMENTS}\n"
    "    python3 -m playwright install chromium"
)


def missing(err):
    """Exit code 3, having named the package the ImportError `err` found missing
    and the pinned install (#256). A script calls it where it imports numpy,
    Pillow or scipy, before any browser starts: run_browser() reads any
    ImportError as Playwright's."""
    script = os.path.basename(sys.argv[0])
    print(
        f"{script}: {err.name or err} is missing — python3 -m pip install -r {REQUIREMENTS}",
        file=sys.stderr,
    )
    return 3


# Runs before the page's own scripts. It keeps every animation the page makes,
# because a finished fill-none animation drops out of getAnimations() but can
# still be seeked through a held reference. It records the frames in which a
# script rewrote a style or geometry attribute, the trace motion driven by a
# script loop leaves where WAAPI leaves none. A path's `d` it records apart,
# with each value written and its frame's time, so a morph can be measured; a
# `d` write restarts the quiet window. And it tracks every pending setTimeout;
# a timer firing restarts the quiet window, as a new animation does.
COLLECTOR_JS = r"""
(() => {
  const seen = new Map();
  const rewrites = new Map();
  const morphs = new Map();
  const pending = new Map();
  const state = { seen, rewrites, morphs, pending, frame: 0, firstFrame: null, frameAt: null, prevFrameAt: null,
    lastNew: 0, lastPageFrame: -1, stopped: false };
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
  // A frame loop that writes nothing, as a morph holding a shape does, is still
  // running: settle() waits for it. It is known by the frame it last asked in,
  // not a time: a tick that asks for its next frame and then holds the browser
  // read as stopped by the clock (#135). An animation the callback makes waits
  // in this frame, so the frame is scanned again after it (#326).
  const raf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function (cb) {
    state.lastPageFrame = state.frame;
    if (typeof cb !== 'function') return raf(cb);
    return raf((t) => { try { return cb(t); } finally { state.scan(t); } });
  };
  state.raf = raf;
  // `ended` is set once an animation reaches its end, so one the page then
  // cancels, as on animationend, is still known to have run its course (#368).
  const keep = (a) => {
    if (!seen.has(a)) {
      const rec = { start: null, held: null, ended: false };
      seen.set(a, rec);
      a.addEventListener('finish', () => { rec.ended = true; });
      state.lastNew = performance.now();
    }
    return seen.get(a);
  };
  // Also run after each frame's paint and by every read from Python, so an
  // animation a timer started since the last frame is never missed. An animation still waiting to start in a
  // frame is drawn at its first keyframe there, held at time 0: `held` is the
  // first such frame's time. A loaded machine can start the page's animations
  // a frame after its first, and seeked before its start one would show its
  // unanimated style instead (#326).
  state.scan = (at) => {
    for (const a of document.getAnimations()) {
      const rec = keep(a);
      if (a.startTime !== null) rec.start = a.startTime;
      else if (at !== undefined && rec.held === null && a.pending && a.playState === 'running') rec.held = at;
    }
  };
  // An animation reverse() was called on is missing from getAnimations() until
  // it starts, and a frame that runs late keeps the time it was due, so one
  // queued behind a long task can start it there and the next, stamped the real
  // time, find it ended: no scan sees a short one (#359). play(), animate() and
  // updatePlaybackRate() leave an animation listed while it waits, so a frame's
  // scan finds it. One on no element of the page, which no scan would list, is
  // not the page's.
  const rev = Animation.prototype.reverse;
  Animation.prototype.reverse = function () {
    rev.call(this);
    const el = this.effect && this.effect.target;
    if (el && el.isConnected) keep(this);
  };
  // A task posted in a frame runs after its paint. An animation a
  // ResizeObserver or a style change starts after the frame's scans is drawn
  // in that frame, and can end before the next (#369). Residual: it passes no
  // frame time, as a page task may run before it and start an animation that
  // frame never drew, so one still waiting is held from the next frame's scan.
  const afterPaint = new MessageChannel();
  afterPaint.port1.onmessage = () => state.scan();
  const collect = (now) => {
    if (state.firstFrame === null) state.firstFrame = now;
    // Registered before any page script, so it runs first in every frame.
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
  new MutationObserver((records) => {
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
      if (!log.length || log[log.length - 1].frame !== state.frame) log.push({ frame: state.frame, at: performance.now() });
      rewrites.set(m.target, log);
    }
  }).observe(document, { subtree: true, attributes: true, attributeOldValue: true,
    attributeFilter: WATCHED });
})();
"""

# Shared by the page-side calls: a readable name for an element, from it and at
# most two ancestors, each by at most two classes: a guess at enough to tell
# elements apart in a report.
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
  for (let p = el.parentElement; p && parts.length < 3 && !el.id; p = p.parentElement) {
    if (p.localName === 'body' || p.localName === 'html') break;
    parts.unshift(one(p));
    if (p.id) break;
  }
  return parts.join(' > ') + (pseudo || '');
};
"""

# Whether a rewrite log shows a script moving its element frame by frame.
LOOP_JS = r"""
const loop = (log, frames, span) => log.some((w, i) => {
  const last = log[i + frames - 1];
  return last && (last.at - w.at <= span || last.frame - w.frame === frames - 1);
});
"""

STATUS_JS = (
    r"""
({ frames, span }) => {
  """
    + LOOP_JS
    + r"""
  const f = window.__flow;
  f.scan();
  let running = 0;
  for (const a of f.seen.keys()) {
    const t = a.effect && a.effect.getComputedTiming();
    // A scroll-driven animation never finishes on time; the blockers name it.
    if (a.playState === 'running' && a.timeline === document.timeline && t && t.endTime !== Infinity) running++;
  }
  const now = performance.now();
  const timers = [...f.pending.values()].map((due) => Math.max(0, due - now));
  const morphed = [...f.morphs.values()].some((log) => loop(log, frames, span));
  return { now, firstFrame: f.firstFrame, lastNew: f.lastNew, running, timer: timers.length ? Math.max(...timers) : null,
    framing: morphed && f.lastPageFrame >= f.frame };
}
"""
)

# Everything that moves the page some way this sampler cannot seek.
BLOCKERS_JS = (
    r"""
({ before, frames, span, shown }) => {
  """
    + LABEL_JS
    + LOOP_JS
    + r"""
  const f = window.__flow;
  f.scan();
  f.stopped = true;
  const reasons = [];
  const visible = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const name = (els) => els.slice(0, shown).map((e) => label(e)).join(', ') + (els.length > shown ? ', …' : '');
  // [selector, why, whether only a visible one counts]
  const kinds = [
    ['canvas', 'draws on a canvas', true],
    ['video', 'plays a video', true],
    ['iframe, object, embed', 'embeds another document', true],
    ['animate, animateTransform, animateMotion, set', 'animates SVG with SMIL', false],
  ];
  for (const [sel, why, onlyVisible] of kinds) {
    const els = [...document.querySelectorAll(sel)].filter((e) => !onlyVisible || visible(e));
    if (els.length) reasons.push(why + ' (' + name(els) + ')');
  }
  const shadowed = [...document.querySelectorAll('*')].filter((e) => e.shadowRoot);
  if (shadowed.length) reasons.push('has shadow DOM (' + name(shadowed) + ')');
  const scrolled = [...f.seen.keys()].filter((a) => a.timeline !== document.timeline);
  if (scrolled.length) reasons.push('drives ' + scrolled.length + ' animation(s) by scroll position, not time');
  const reversed = [...f.seen.keys()].filter((a) => a.playbackRate <= 0);
  if (reversed.length) reasons.push('plays ' + reversed.length + ' animation(s) in reverse or at zero speed');
  const seeked = [...f.seen].filter(([a, rec]) => a.startTime === null && rec.start === null && a.playState === 'paused');
  if (seeked.length) reasons.push('holds ' + seeked.length + ' paused animation(s) that a script seeks by hand');
  const rewritten = [...f.rewrites].filter(([, log]) => loop(log, frames, span)).map(([e]) => e);
  if (rewritten.length) reasons.push('moves ' + rewritten.length + ' element(s) by rewriting their style or attributes from a script, frame by frame (' + name(rewritten) + ')');
  f.morphing = [...f.morphs].filter(([, log]) => loop(log, frames, span)).map(([e]) => e);
  const scrollMorphed = f.morphing.filter((e) => f.morphs.get(e).some((w) => w.at >= f.sweptFrom));
  if (scrollMorphed.length) reasons.push('rewrites the d of ' + scrollMorphed.length + ' path(s) when the page is scrolled (' + name(scrollMorphed) + ')');
  if (f.seen.size > before) reasons.push('starts ' + (f.seen.size - before) + ' animation(s) when the page is scrolled');
  return reasons;
}
"""
)

# Pauses every animation and works out where each, and each morph's recorded
# frames, sits on one timeline. Offsets keep each animation's real start.
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
  // A write before the page's first frame has no frame time to place it on
  // the timeline, so it counts as setup and its shape goes unmeasured (#72).
  const morphs = f.morphing.map((el) => ({ el, writes: f.morphs.get(el).filter((w) => w.frameAt !== null) }));
  if (!anims.length && !morphs.length) return { anims: 0, morphs: [] };
  const t0 = Math.min(f.firstFrame === null ? Infinity : f.firstFrame, ...anims.map((x) => x.start),
    ...morphs.map((m) => m.writes[0].frameAt));
  let end = 0;
  let infinite = false;
  // A morph moves from the frame before its first write; an animation once
  // its delay is over, or at once where the delay is negative.
  let first = Infinity;
  const edges = [];
  const starts = [];
  for (const m of morphs) {
    const w0 = m.writes[0];
    first = Math.min(first, (w0.prevFrameAt === null ? w0.frameAt : w0.prevFrameAt) - t0);
    for (const w of m.writes) {
      edges.push(w.frameAt - t0);
      if (w.prevFrameAt !== null) edges.push(w.prevFrameAt - t0);
    }
    end = Math.max(end, m.writes[m.writes.length - 1].frameAt - t0);
  }
  for (const x of anims) {
    x.a.pause();
    const t = x.a.effect.getComputedTiming();
    const off = x.start - t0;
    // Played on a frame; a delay can end mid-frame.
    starts.push(off);
    first = Math.min(first, off + Math.max(0, t.delay) / x.rate);
    x.loops = t.endTime === Infinity;
    if (x.loops) {
      infinite = true;
      end = Math.max(end, off + (t.delay + t.duration) / x.rate);
    } else {
      end = Math.max(end, off + t.endTime / x.rate);
      edges.push(off + (t.delay + t.activeDuration) / x.rate);
    }
    edges.push(off + t.delay / x.rate);
    // Each keyframe's time in each pass, where a move can resume mid-frame. A
    // keyframe's offset maps straight to time only under linear effect easing,
    // which CSS animations and most element.animate() calls use.
    if (t.easing === 'linear' && t.duration > 0) {
      const offsets = x.a.effect.getKeyframes().map((k) => k.computedOffset);
      // At most 100 passes, a guess at a bound no finite animation a candidate plays nears.
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

# Whether the viewer sees an element at rest (#297): its box, or a descendant's,
# inside the viewport and every box that clips it, with nothing from it up at
# zero opacity. An ancestor's overflow clips only what its containing block
# chain runs through; a clip-path, a mask or paint containment clips all it
# holds, here to its whole box. <body> and <html> clip at the viewport.
# Residual: a clip-path or mask is read as its box, so a start it hides inside
# its box is still judged.
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
  // A box with no width or height shows on an edge; one with both shows only
  // where it overlaps (#297).
  return (rt > l || (r.width === 0 && rt === l)) && (b > t || (r.height === 0 && b === t));
};
const seen = (el) => {
  if (getComputedStyle(el).visibility !== 'visible') return false;
  if (el instanceof HTMLElement && !el.getClientRects().length) return false;
  for (let p = el; p; p = p.parentElement) if (Number(getComputedStyle(p).opacity) === 0) return false;
  return shown(el) || [...el.querySelectorAll('*')].some(shown);
};
"""

# Seeks every animation to each time and reads each moving element, and
# whether it is seen; a pseudo-element by its element.
SAMPLE_JS = (
    r"""
(times) => {
  """
    + SEEN_JS
    + r"""
  const { anims, elements } = window.__flow.sampling;
  for (const t of times) {
    // Held at its first keyframe from the frame it waited in (#326).
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


def sample_times(end, edges, fps, starts=()):
    """Every frame, plus each animation's exact start, end and keyframes: a move
    that began mid-frame would otherwise show a part-speed first frame and hide
    its jolt. An exact time within 1 ms of a frame takes that frame's place, as
    a frame just past a keyframe reads part of the next speed (#126). The first
    frame's too: an animation started at load starts a fraction of a ms after
    it, and at 0 reads as not yet started, its first keyframe unshown (#297).
    An animation starts at its timeline's time when it is ready, which a
    document timeline advances once a frame (Web Animations Level 1, "Playing
    an animation", its pending play task), so each of `starts` is
    followed by a whole frame, with no frame sampled inside it: a loaded
    machine starts one off the sampled frames, and a part frame carries a jump
    too short (#326). Residual: an edge inside that frame still cuts it, and a
    move from rest after a delay, at a later keyframe or pass, keeps the
    sampled frames' phase.
    In a window of 1 ms or more, no two times fall within 1 ms of each other."""
    step = 1000 / fps
    first = max((e for e in edges if 0 <= e < min(1, end)), default=0)
    exact = [first] + ([end] if end > 0 else [])
    spans = [(s, s + step) for s in starts if 0 <= s and s + step < end]
    for e in sorted(edges) + [b for _, b in spans]:
        if 0 < e < end and all(abs(e - t) >= 1 for t in exact):
            exact.append(e)
    frames = [k * step for k in range(1, int(end // step) + 1)]
    return sorted(
        exact
        + [
            t
            for t in frames
            if all(abs(t - x) >= 1 for x in exact)
            and not any(a < t < b for a, b in spans)
        ]
    )


def path_structure(d):
    """A path's commands and its count of numbers: two paths with the same can
    be morphed number by number."""
    return "".join(PATH_COMMAND.findall(d)), len(PATH_NUMBER.findall(d))


def path_numbers(d):
    return [float(n) for n in PATH_NUMBER.findall(d)]


def morph_points(writes):
    """(time, numbers of d) at each frame a script wrote a path's `d`, from its
    writes: [{ms, prev_ms, old, value}], `prev_ms` being the frame before `ms`,
    or None. A write after frames with none holds the old `d` until the frame
    before it, so a held shape reads as still, not as a slow move. Raises
    ValueError where the command structure changes, so the numbers have no
    one-to-one pairing; the shape before the first write is setup and may
    differ."""
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
    """A morph's numbers at time t: each number interpolated between the frames
    either side, and held before the first and after the last."""
    i = bisect.bisect_right([p[0] for p in points], t)
    if i == 0:
        return points[0][1]
    if i == len(points):
        return points[-1][1]
    (ta, a), (tb, b) = points[i - 1], points[i]
    k = (t - ta) / (tb - ta)
    return [x + (y - x) * k for x, y in zip(a, b, strict=True)]


def dropped_frames(writes):
    """(from ms, to ms) of each stretch over which a morph's shape changed while
    the browser dropped DROPPED_FRAMES or more frames in a row, half a frame
    allowed for jitter (a guess), stretches that touch joined into one. A change of
    command structure finds none: add_morphs refuses it."""
    gaps = [w["ms"] - w["prev_ms"] for w in writes if w["prev_ms"] is not None]
    try:
        points = morph_points(writes)
    except ValueError:
        return []
    if not gaps:
        return []
    longest = (DROPPED_FRAMES + 0.5) * min(statistics.median(gaps), BROWSER_FRAME_MS)
    out = []
    for (ta, a), (tb, b) in itertools.pairwise(points):
        if a != b and tb - ta > longest:
            if out and out[-1][1] == ta:
                out[-1] = (out[-1][0], tb)
            else:
                out.append((ta, tb))
    return out


def add_morphs(sample):
    """Adds each morph's `d` channel, at every sample time, to the element of
    its label, with the stretches its browser dropped frames over as the
    element's `dropped["d"]`. Raises UnmeasurableError where a morph's structure
    changes. `sample` is the caller's accumulator for its `elements`, which this fills."""
    by_label = {e["label"]: e for e in sample["elements"]}
    for m in sample["morphs"]:
        try:
            points = morph_points(m["writes"])
        except ValueError as exc:
            raise UnmeasurableError(
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
        el["channels"]["d"] = [morph_at(points, t) for t in sample["times"]]
        el.setdefault("dropped", {})["d"] = dropped_frames(m["writes"])


def morph_svg(morphs):
    """Every `d` each morph's path took, one <path> per frame, for check-curves.js."""
    out = ['<svg xmlns="http://www.w3.org/2000/svg">']
    for m in morphs:
        slug = re.sub(r"[^A-Za-z0-9_-]+", "-", m["label"]).strip("-")
        shapes = [("before", m["writes"][0]["old"])] if m["writes"][0]["old"] else []
        shapes += [(f"at-{w['ms']:.0f}ms", w["value"]) for w in m["writes"]]
        for when, d in shapes:
            out.append(f'<path id="{slug}-{when}" d="{esc(d)}"/>')
    out.append("</svg>")
    return "\n".join(out)


def numbers(prop, value):
    """A computed value as a vector of its numbers, so a change is a distance.
    Forms that drop numbers are written out in full first: a missing number
    would count as 0, and `rgb(0, 0, 0)` to `rgba(0, 0, 0, 0.99)` would read as
    a jump of 0.99."""
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
    """The change between consecutive samples, each a vector of one length."""
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
    """Speed between consecutive samples, in the channel's units per second,
    from their deltas(); a change under `floor` is none."""
    out = []
    for d, (ta, tb) in zip(changes, itertools.pairwise(times), strict=True):
        dt = (tb - ta) / 1000
        size = math.hypot(*d)
        v = size / dt if dt > 0 and size >= floor else 0.0
        out.append(v if v >= NOISE else 0.0)
    return out


def same_way(a, b):
    """Whether two changes point the same way."""
    return sum(x * y for x, y in zip(a, b, strict=True)) > 0


def line_at(ts, vs, t):
    """The least-squares line through (ts, vs), at t."""
    mt, mv = statistics.fmean(ts), statistics.fmean(vs)
    sxx = sum((x - mt) ** 2 for x in ts)
    return mv + sum((x - mt) * (y - mv) for x, y in zip(ts, vs, strict=True)) / sxx * (
        t - mt
    )


def steps_in(r, changes, times, *, s, e):
    """(index, frames between, from share, to share, "up" or "down") of each
    speed step in the run of moving intervals s..e. The step starts at sample
    index i, the first frame off the slower speed, and the faster speed is
    reached n frames later, as the STEP constants' comment sets out. Each side
    holds; the faster reaches STEP_FLOOR of the run's top speed; every frame
    moves the same way. The shares, over the run's top speed, are the speed
    just before the step and the new speed it reaches."""
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
        # Curvature and a kink in a smooth easing miss the two ways at once.
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

    out = []
    i = s + k
    while i < e:
        found = next(filter(None, (step_at(i, n) for n in range(STEP_SPREAD))), None)
        # A frame between that reads the slower speed but for float noise, as
        # one ending on the keyframe does, would put the step a frame early
        # (#126). One between that reads the faster speed still does.
        while found and found[1] and (later := step_at(found[0] + 1, found[1] - 1)):
            found = later
        out += [found] if found else []
        i = found[0] + found[1] + 1 if found else i + 1
    return out


def runs(flags):
    """(start, end) index pairs, inclusive, of each run of True."""
    out, start = [], None
    for i, f in enumerate(flags + [False]):
        if f and start is None:
            start = i
        elif not f and start is not None:
            out.append((start, i - 1))
            start = None
    return out


def still_px(view_cm):
    """STILL_ARCMIN_S in CSS px a second, seen from view_cm."""
    return STILL_ARCMIN_S / math.degrees(60 * math.atan(CSS_PX_CM / view_cm))


def jump_px(view_cm):
    """JUMP_DEG in CSS px, seen from view_cm."""
    return 2 * view_cm * math.tan(math.radians(JUMP_DEG) / 2) / CSS_PX_CM


def jolt_line(ms):
    """The share of its top speed at which a move of `ms` starts or stops with
    a jolt, from JOLT_BAND; None for a move too short to have one."""
    if ms < JOLT_BAND[0][0]:
        return None
    for (a, lo_a, hi_a), (b, lo_b, hi_b) in itertools.pairwise(JOLT_BAND):
        if ms <= b:
            k = (ms - a) / (b - a)
            return ((lo_a + hi_a) + k * (lo_b + hi_b - lo_a - hi_a)) / 2
    return (JOLT_BAND[-1][1] + JOLT_BAND[-1][2]) / 2


def analyse(sample, pause_ms=PAUSE_MS, jolt_ratio=None, view_cm=VIEW_CM):
    """Pauses, jolts, jumps and speed steps from a sample: {times, elements:
    [{label, loops, channels: {name: [value per frame]}, dropped: {name: [(from
    ms, to ms)]}, seen: [bool per frame]}]}. Pure, so the thresholds are tested
    without a browser. An element that `loops` forever is still moving where the
    window cuts it, so its motion at the last frame is not a stop. No jolt, jump
    or step rests on a frame in a dropped stretch, whose motion is unknown. A
    move's line is jolt_line() of its length, or `jolt_ratio` at every length.
    A start or stop where `seen` is False, the viewer never sees the element at
    rest, so it is judged neither way and is listed `unseen` where it would have
    been a jolt or jump (#297); an element with no `seen` is seen."""
    times = sample["times"]
    gaps = len(times) - 1
    active = [False] * gaps
    elements = []
    steps = {}
    for el in sample["elements"]:
        channels = {}
        for name, values in el["channels"].items():
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
            # A move going back the other way after still for no longer than a
            # pause has turned: its start index maps to its last frame before
            # (#150). Residual: a move that eases to a stop, rests up to a pause
            # and starts back gaining under its jolt line over the speed it
            # stopped at is not called a jolt, though the same start from rest is.
            turns = {}
            for (_, e), (s, _) in itertools.pairwise(runs(moving)):
                if times[s] - times[e + 1] <= pause_ms and same_way(
                    changes[e], [-x for x in changes[s]]
                ):
                    turns[s] = e
            channels[name] = {
                "rates": r,
                "peak": peak,
                "moving": moving,
                "unknown": unknown,
                "turns": turns,
            }
            active = [x or y for x, y in zip(active, moving, strict=True)]
            for s, e in runs(moving):
                for i, n, before, after, way in steps_in(r, changes, times, s=s, e=e):
                    if any(unknown[i - STEP_SIDE_FRAMES : i + n + STEP_SIDE_FRAMES]):
                        continue
                    at = round((times[i] + times[i + n]) / 2)
                    steps.setdefault(
                        (el["label"], way, at),
                        {
                            "element": el["label"],
                            "way": way,
                            "at": at,
                            "from": round(before, 2),
                            "to": round(after, 2),
                            "channels": [],
                        },
                    )["channels"].append(name)
        elements.append(
            {
                "label": el["label"],
                "loops": el.get("loops", False),
                "seen": el.get("seen") or [True] * len(times),
                "channels": channels,
            }
        )

    # A still spell before the first move is no pause: the rule's sources
    # speak only of stills between moves (house-audit-craft.md §1.5, #220).
    pauses = []
    for s, e in runs([not a for a in active]):
        start, end = times[s], times[e + 1]
        if s > 0 and end - start > pause_ms:
            where = "at the end" if e == gaps - 1 else None
            pauses.append(
                {
                    "start": round(start),
                    "end": round(end),
                    "ms": round(end - start),
                    "where": where,
                }
            )

    jolts, jumps, unseen = {}, {}, {}
    jump_min = jump_px(view_cm)
    for el in elements:
        for name, ch in el["channels"].items():
            r, turns, unknown = ch["rates"], ch["turns"], ch["unknown"]
            in_frame = {e for s, e in turns.items() if s - e - 1 <= TURN_FRAMES}
            jolted = set()
            for s, e in runs(ch["moving"]):
                top = max(r[s : e + 1])
                line = (
                    jolt_ratio
                    if jolt_ratio is not None
                    else jolt_line(times[e + 1] - times[s])
                )
                # A start out of a turn gains speed from the speed just before
                # it, unless the move stopped there with a jolt (#150).
                before = turns.get(s)
                turned = before is not None and before not in jolted
                # (edge, interval, time, gain, out of a turn, the frame at rest)
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
                    # A stop jolts whether or not it is seen, so the start out
                    # of its turn is judged from rest.
                    if jolt and edge == "stops":
                        jolted.add(i)
                    if not (jolt or jump):
                        continue
                    if not el["seen"][rest]:
                        u = unseen.setdefault(
                            (el["label"], edge, round(t)),
                            {
                                "element": el["label"],
                                "edge": edge,
                                "at": round(t),
                                "would_be": [],
                                "channels": [],
                            },
                        )
                        u["would_be"] = sorted(
                            set(u["would_be"])
                            | {k for k, f in (("jolt", jolt), ("jump", jump)) if f}
                        )
                        u["channels"].append(name)
                        continue
                    if jolt:
                        j = jolts.setdefault(
                            (el["label"], edge, round(t), turn),
                            {
                                "element": el["label"],
                                "edge": edge,
                                "at": round(t),
                                "share": 0,
                                "line": round(line, 2),
                                "channels": [],
                            }
                            | ({"turn": True} if turn else {}),
                        )
                        j["share"] = max(j["share"], round(gain / top, 2))
                        j["channels"].append(name)
                    if jump:
                        jumps[(el["label"], round(t))] = {
                            "element": el["label"],
                            "at": round(t),
                            "px": round(moved, 1),
                        }

    def by_time(found):
        return sorted(found.values(), key=lambda x: (x["at"], x["element"]))

    return {
        "pauses": pauses,
        "jolts": by_time(jolts),
        "jumps": by_time(jumps),
        "unseen": by_time(unseen),
        "steps": by_time(steps),
        "elements": elements,
    }


PALETTE = ["#2563eb", "#d97706", "#059669", "#db2777", "#7c3aed", "#0891b2", "#65a30d"]


def chart(sample, result, pause_ms):
    """One panel per element: each channel's speed over time, scaled to its own
    top speed, which the legend gives. Pauses shaded, jolts, jumps and steps marked."""
    times = sample["times"]
    span = max(times[-1], 1)
    # The chart's width, margins, panel height and gaps, and the 30 px strip under the panels for the time axis,
    # in px: picked by eye for a legible chart, not measured, as are the offsets, font sizes, marker sizes and
    # label lengths below.
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
    mids = [(times[i] + times[i + 1]) / 2 for i in range(len(times) - 1)]
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
                for t, v in zip(mids, ch["rates"], strict=True)
            )
            out.append(
                f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="1.5"/>'
            )
            unit = " px/s" if name in PX_CHANNELS else "/s"
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
    # The first round step that gives at most 12 ticks, else a tenth of the span: picked by eye, not measured.
    for s in (100, 250, 500, 1000, 2000, 5000, 10000, 30000, 60000):
        if span / s <= 12:
            return s
    return span / 10


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def first_line(exc):
    for line in str(exc).splitlines():
        if line.strip():
            return line.strip()
    return exc.__class__.__name__


class PageTimeoutError(Exception):
    """The page did not render in time: exit 4."""


class NoBrowserError(Exception):
    """Playwright imported but its Chromium is not downloaded: exit 3, with the
    same install lines as an absent package."""


class RefusedError(Exception):
    """The browser reached the network and got nothing usable: exit 5."""


class UnmeasurableError(Exception):
    """The page moves some way this sampler cannot seek, or not at all: exit 6."""


class HungCallError(Exception):
    """A call the watch took as hung, or one that raised once its renderer died:
    exit 7."""


def size_arg(p, flag, value, *, number=int, example=DESKTOP):
    """A WxH argument as a width and height, or a usage error naming `flag`."""
    try:
        w, h = (number(n) for n in value.lower().split("x", 1))
    except ValueError:
        p.error(f"{flag} wants WxH, e.g. {example} — got {value!r}")
    return {"width": w, "height": h}


def page_url(p, url):
    """A URL as given, or a local file's file:// URL; a missing file is a usage error."""
    if re.match(r"^[a-z]+://", url):
        return url
    path = pathlib.Path(url)
    if not path.is_file():
        p.error(f"no such file: {url}")
    return path.resolve().as_uri()


def descendants(pid):
    """The pids under process `pid`, read from /proc; none where it has no /proc."""
    found, todo = [], [pid]
    while todo:
        parent = todo.pop()
        try:
            tasks = os.listdir(f"/proc/{parent}/task")
        except OSError:  # no /proc, or the process has exited: no children (#432)
            continue
        for task in tasks:
            try:
                with open(f"/proc/{parent}/task/{task}/children") as f:
                    kids = [int(k) for k in f.read().split()]
            except OSError:  # the thread has exited, or no children file: none (#432)
                continue
            found += kids
            todo += kids
    return found


def process_args(pid):
    """Process `pid`'s command line split on whitespace, empty once it has gone.
    Chromium rewrites its own as one string, so a NUL split would keep it whole."""
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            return f.read().decode(errors="replace").replace("\0", " ").split()
    except OSError:  # the process has exited, as its docstring says (#432)
        return []


def browser_pids(pids):
    """Those of `pids` that are a Chromium Playwright launched: its browser
    process, which talks to Playwright over a pipe and has no --type= of its own."""
    return [
        pid
        for pid in pids
        if "--remote-debugging-pipe" in (args := process_args(pid))
        and not any(a.startswith("--type=") for a in args)
    ]


def driver_pid(browser):
    """The Playwright driver that launched the browser at `browser`: its parent,
    the node process every Playwright call reaches it through. None once either
    has gone, as a browser whose driver died is the init process's child."""
    try:
        with open(f"/proc/{browser}/stat") as f:
            # The name in brackets may hold spaces; the parent follows the state.
            parent = int(f.read().rsplit(")", 1)[1].split()[1])
    except OSError:  # the browser has exited, as the docstring says (#464)
        return None
    return parent if "run-driver" in process_args(parent) else None


class WaitingCall(typing.NamedTuple):
    """A Playwright call a greenlet is suspended in: '<Class>.<method>', the
    '<file>:<line>' that made it, and its frame, which tells one call from the
    next at the same line."""

    name: str
    where: str
    frame: object


def playwright_call(stack, package_dir):
    """The WaitingCall `stack`, (frame, line) pairs outermost first, is inside:
    the first frame in `package_dir`, Playwright's own, and the line outside it
    that made the call; None where no frame is Playwright's."""
    for (caller, line), (frame, _) in itertools.pairwise(stack):
        if frame.f_code.co_filename.startswith(package_dir):
            owner = frame.f_locals.get("self")
            name = frame.f_code.co_name
            if owner is not None:
                name = f"{type(owner).__name__}.{name}"
            return WaitingCall(
                name, f"{os.path.basename(caller.f_code.co_filename)}:{line}", frame
            )
    return None


def waiting_call(main, package_dir):
    """The WaitingCall the greenlet `main` is suspended in; None while it runs or
    waits on nothing of Playwright's.
    Read from another thread: `gr_frame` and `f_locals` of a suspended greenlet
    are read, not changed, and a resume mid-walk at worst names the wrong call."""
    stack = []
    frame = main.gr_frame
    while frame is not None:
        stack.append((frame, frame.f_lineno))
        frame = frame.f_back
    stack.reverse()
    return playwright_call(stack, package_dir)


def raising_call(exc, package_dir):
    """The WaitingCall `exc` was raised from; None where it left no Playwright
    frame. A caller still handling it sits at its own `with` line, so each
    frame's line is the traceback's."""
    return playwright_call(list(traceback.walk_tb(exc.__traceback__)), package_dir)


class CallWatch:
    """Kills the browser at `browser` and its parent, the Playwright driver,
    once a call is taken as hung, so the call raises instead of waiting for ever;
    `fired` then says which call and why. Killing the browser alone leaves a
    CDPSession.send waiting (#464).
    A call is hung once it has waited RENDERER_GONE_S with no renderer under
    the browser (#432), or, being one of UNTIMED_CALLS, UNANSWERED_S in all
    (#459).
    Residual: a renderer that dies while another of the browser's lives, as
    with two pages open on different sites, is not seen. Residual: a call that
    waits RENDERER_GONE_S with no renderer for another reason, as new_page on a
    machine too starved to start one, is killed and reported the same way."""

    def __init__(self, browser, main, package_dir):
        self.browser, self.driver = browser, driver_pid(browser)
        self.main, self.package_dir = main, package_dir
        self.fired = None
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _rendering(self):
        return any(
            "--type=renderer" in process_args(p) for p in descendants(self.browser)
        )

    def _hung(self, call, since, began, now):
        """Why the waiting `call` is hung, or None: `since` is when the browser
        was last seen with no renderer, None while it has one, and `began` when
        the watch first saw this call."""
        name, where = call.name, call.where
        if since is not None and now - since >= RENDERER_GONE_S:
            return (
                f"{name} at {where} waited {RENDERER_GONE_S} s with the browser "
                "running no renderer, so it would never have returned; an "
                "out-of-memory kill of the page's renderer causes this (#430), "
                "so run it again once memory is free"
            )
        if name in UNTIMED_CALLS and now - began >= UNANSWERED_S:
            return (
                f"{name} at {where} waited {UNANSWERED_S} s for a renderer that is "
                "alive but never answered, and Playwright gives it no timeout, so "
                "it would never have returned (#459, #464); run it again"
            )
        return None

    def _run(self):
        since = held = began = None
        while not self._stop.wait(WATCH_POLL_S):
            call = waiting_call(self.main, self.package_dir)
            if call is None:
                since = held = None
                continue
            now = time.monotonic()
            if held is None or call.frame is not held:
                held, began = call.frame, now
            if self._rendering():
                since = None
            else:
                since = now if since is None else since
            if why := self._hung(call, since, began, now):
                self.fired = why
                driver = [self.driver] if self.driver else []
                killed = [self.browser, *descendants(self.browser), *driver]
                for p in killed:
                    # A process that exited since the read is already gone.
                    with contextlib.suppress(ProcessLookupError):
                        os.kill(p, signal.SIGKILL)
                # A browser still exiting is counted as new by the next launch
                # (#464). A gone or dead process has no args.
                end = time.monotonic() + KILLED_GONE_S
                while any(map(process_args, killed)) and time.monotonic() < end:
                    time.sleep(WATCH_POLL_S)
                return

    def renderer_death(self, exc, page_open):
        """Why the Playwright error `exc` came of a renderer's death, or None:
        the browser runs no renderer as it raises, and a page was open or the
        call was opening one. A renderer killed while new_page sets its page up
        makes it raise instead of wait (#472); a browser that died has closed
        its pages first.
        Residual: a call refused for another reason whose renderer then dies
        before this reads /proc is reported as the renderer's death. Residual:
        a call that opens a page under another name than new_page is not
        recognised as opening one."""
        call = raising_call(exc, self.package_dir)
        if call is None or self._rendering():
            return None
        if not page_open and not call.name.endswith(".new_page"):
            return None
        return (
            f"{call.name} at {call.where} raised {first_line(exc)!r} with the "
            "browser running no renderer; an out-of-memory kill of the page's "
            "renderer causes this (#430), so run it again once memory is free"
        )

    def stop(self):
        self._stop.set()
        self._thread.join()


@contextlib.contextmanager
def chromium(args=()):
    """A launched Chromium, closed on leaving. Playwright's failures leave as
    NoBrowserError at launch, and as PageTimeoutError or RefusedError after. A
    call CallWatch takes as hung, or a Playwright error it puts down to a dead
    renderer, leaves as HungCallError, whatever the script raised from it,
    where /proc shows exactly one new browser process.
    Residual: with no /proc, as on macOS, or with no task `children` file, as
    in some containers, no watch runs, which it says on stderr, and the call
    can wait for ever."""
    import greenlet
    import playwright
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import TimeoutError as PlaywrightTimeout
    from playwright.sync_api import sync_playwright

    with sync_playwright() as play:
        before = set(descendants(os.getpid()))
        try:
            browser = play.chromium.launch(args=list(args))
        except PlaywrightError as exc:
            raise NoBrowserError(first_line(exc)) from exc
        launched = browser_pids(set(descendants(os.getpid())) - before)
        watch = None
        if len(launched) == 1:
            watch = CallWatch(
                launched[0],
                greenlet.getcurrent(),
                os.path.dirname(playwright.__file__) + os.sep,
            )
        else:
            print(
                f"no call watch: /proc shows {len(launched)} new browser processes, "
                "not one, so a hung call can wait for ever (#432, #459)",
                file=sys.stderr,
            )
        try:
            yield browser
        except Exception as exc:
            if watch and watch.fired:
                raise HungCallError(watch.fired) from exc
            if (
                watch
                and isinstance(exc, PlaywrightError)
                and not isinstance(exc, PlaywrightTimeout)
                and (
                    why := watch.renderer_death(
                        exc, any(c.pages for c in browser.contexts)
                    )
                )
            ):
                raise HungCallError(why) from exc
            if isinstance(exc, PlaywrightTimeout):
                raise PageTimeoutError(first_line(exc)) from exc
            if isinstance(exc, PlaywrightError):
                raise RefusedError(first_line(exc)) from exc
            raise
        else:
            if watch and watch.fired:
                raise HungCallError(watch.fired)
        finally:
            if watch:
                watch.stop()
            # With its driver killed, close would hang or raise over the hung call (#464).
            if not (watch and watch.fired):
                browser.close()


def run_browser(work, timeout, url=None, unmeasurable=None):
    """work()'s result and None, or None and the exit code of the failure it
    raised, printed: 3 no Playwright or no Chromium, 5 a refused load, 4 a
    timeout, 7 a hung call or a dead renderer, and 6 an UnmeasurableError,
    its reasons on stdout between the two lines of `unmeasurable`. With no `url`, a refusal names what failed to draw."""
    try:
        return work(), None
    except ImportError:
        print(f"Playwright is not importable here.\n{INSTALL_HINT}", file=sys.stderr)
        return None, 3
    except NoBrowserError as exc:
        print(
            f"Playwright is installed but its browser is not: {exc}\n{INSTALL_HINT}",
            file=sys.stderr,
        )
        return None, 3
    except RefusedError as exc:
        print(
            f"the browser could not load {url}: {exc}"
            if url
            else f"the browser could not draw {exc}",
            file=sys.stderr,
        )
        return None, 5
    except PageTimeoutError as exc:
        print(
            f"timed out after {timeout}ms{f' on {url}' if url else ''}: {exc}",
            file=sys.stderr,
        )
        return None, 4
    except HungCallError as exc:
        # The watch already killed the browser and its driver, or the renderer
        # had died; its message names the call and why, and exit 7 is the
        # result (#432, #459, #464, #472).
        print(exc, file=sys.stderr)
        return None, 7
    except UnmeasurableError as exc:
        if unmeasurable is None:
            raise
        print(unmeasurable[0])
        for r in exc.args[0]:
            print(f"  - {r}")
        print(unmeasurable[1])
        return None, 6


def settled(s, quiet):
    """Whether a page's status shows its motion over. The quiet window runs from
    its first frame at the earliest: a busy machine can delay that frame past
    --quiet, and a frame loop has written nothing before it (#135)."""
    return (
        s["firstFrame"] is not None
        and s["running"] == 0
        and s["timer"] is None
        and not s["framing"]
        and s["now"] - max(s["lastNew"], s["firstFrame"]) >= quiet
    )


def settle(page, at):
    waited = 0
    while True:
        s = page.evaluate(
            STATUS_JS, {"frames": REWRITE_FRAMES, "span": REWRITE_SPAN_MS}
        )
        if settled(s, at.quiet):
            return
        if waited >= at.timeout and s["firstFrame"] is None:
            raise PageTimeoutError("no frame drawn")
        if s["timer"] is not None and waited + s["timer"] > at.timeout:
            raise UnmeasurableError(
                [
                    f"sets a script timer that fires {s['timer']:.0f} ms from now, past --timeout; "
                    "raise --timeout to measure what it starts"
                ]
            )
        if waited >= at.timeout and s["framing"]:
            raise UnmeasurableError(
                [
                    f"keeps the frame loop that morphs a path running after {at.timeout} ms, "
                    "so its morph has no end to measure"
                ]
            )
        if waited >= at.timeout:
            raise UnmeasurableError(
                [
                    f"keeps starting or running animations, or rewriting a path's d, after {at.timeout} ms, "
                    "so its motion has no end to measure"
                ]
            )
        page.wait_for_timeout(POLL_MS)
        waited += POLL_MS


# One scroll step a frame, so a scroll handler writes in consecutive frames
# however slowly a busy machine draws them (#135). Through the collector's own
# requestAnimationFrame, which the page's frame loop is not judged by.
SWEEP_JS = r"""
async (stops) => {
  for (const y of stops) {
    scrollTo(0, y);
    await new Promise((done) => window.__flow.raf(done));
  }
}
"""


def sweep(page):
    """Scroll to the bottom in small steps and back, so motion that starts on
    scroll, or that a scroll handler drives, shows itself before the sampler
    trusts the page."""
    height = page.evaluate("() => document.documentElement.scrollHeight - innerHeight")
    if height <= 0:
        return
    # At most forty steps of at least 100 px, and a 300 ms rest at the top for what the
    # sweep started: guesses, unmeasured.
    step = max(100, height / 40)
    stops = [min(height, step * k) for k in range(1, math.ceil(height / step) + 1)]
    page.evaluate(SWEEP_JS, stops + stops[-2::-1] + [0])
    page.wait_for_timeout(300)


def measure(at):
    with chromium() as browser:
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
            settle(page, at)
            before = page.evaluate(
                "() => { const f = window.__flow; f.scan(); f.sweptFrom = performance.now(); return f.seen.size; }"
            )
            sweep(page)
            reasons = page.evaluate(
                BLOCKERS_JS,
                {
                    "before": before,
                    "frames": REWRITE_FRAMES,
                    "span": REWRITE_SPAN_MS,
                    "shown": NAMES_SHOWN,
                },
            )
            if reasons:
                raise UnmeasurableError(reasons)
            sample = page.evaluate(PREPARE_JS)
            if attempt == ATTEMPTS - 1 or not any(
                dropped_frames(m["writes"]) for m in sample["morphs"]
            ):
                break
            page.close()
        if sample["anims"] or sample["morphs"]:
            sample["times"] = sample_times(
                sample["end"], sample["edges"], at.fps, sample["starts"]
            )
            sample["elements"] = page.evaluate(SAMPLE_JS, sample["times"])
    if not sample["anims"] and not sample["morphs"]:
        raise UnmeasurableError(
            ["has no Web Animations API animation and no path a script morphs"]
        )
    add_morphs(sample)
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
        f"jumps, a move from rest whose first frame carries its box {jump_px(at.view_cm):.0f} px ({JUMP_DEG}° from {at.view_cm:g} cm) or more: {len(jumps) or 'none'}"
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
        f"speed steps, a move whose held speed changes {STEP_RATIO:g}-fold or more within {STEP_SPREAD} frames, beyond the trend either side: {len(steps) or 'none'}"
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
TABLE = os.path.join(HERE, "check-flow.table")


def _sibling(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


records = _sibling("motion_records", "motion-records.py")
pointer = _sibling("drive_pointer", "drive-pointer.py")

# --records' working figures, none a record's value. No run has measured
# where any of the caps or waits below starts to miss a fault, so each is a
# guess unless its line gives a derivation; each cap bounds the run's length,
# and what lies past it is not read.
# The elements the parallax sweep reads: a guess, ample for a landing page.
TRACK_CAP = 400
# The parallax sweep's scroll stops: at the table's 100 px step, a page 8000 px
# tall; a guess.
STOP_CAP = 80
# The controls the hover and press reads take: a guess, a page's header,
# hero and first sections.
CONTROL_CAP = 30
# The screens the flash watch films: 6 at 768 px tall is 4608 px of page, and
# at the table's 2 s a screen, 12 s of film; a guess.
SCREEN_CAP = 6
# The CSS px a film cell averages: finer than WCAG's 0.1° fine-pattern limit
# at 96 ppi (about 4 px at 60 cm), so a fine pattern blurs out as WCAG
# exempts it.
CELL_PX = 4
# How long a page may take to end its finite animations, and a scroll to
# come to rest: a guess.
SETTLE_MS = 3000
# The clock step a carousel is read at, and so the slack its holds are read
# to: a guess.
CLOCK_STEP_MS = 100
# How long a scrolled page or released part must hold still to have settled:
# 18 frames at 60 Hz; a guess.
STILL_MS = 300
# The slow drags that find a part's snap points, in px: a short and a long
# one each way; and the short one first tried, to learn whether the part
# moves at all. Guesses.
SLOW_DRAGS = (-200, -80, 80, 200)
PROBE_DRAG = -80
# How long a released part may take to settle: a guess, six times the 0.5 s
# perceptual duration of a SwiftUI spring by default (WWDC 2023, "Animate
# with springs"), which settles fully somewhat later.
PATH_CAP_MS = 3000
# The fling: 40 px over 3 frames, about 830 px/s, which the record's 0.998
# deceleration projects about 415 px on, past the slow drags' 200 px reach;
# a guess.
FLING_PX = 40
FLING_FRAMES = 3
# The moves a touch scroll is sent in, 160 ms at a frame each: a guess.
TOUCH_MOVES = 10
# A frame's length: 16 ms at 60 Hz.
DRAG_FRAME_MS = 16
# The moves before a release its velocity is read from: Android's
# VelocityTracker reads the 100 ms before its newest sample (AOSP
# frameworks/native, include/input/VelocityTracker.h, HORIZON of its default
# least-squares strategy).
RELEASE_HORIZON_MS = 100
# How many flings a part gets before one is fast enough for its projection
# to pick another snap point than where it was let go: a guess.
FLING_TRIES = 3


class Opener:
    """Fresh loads of the page, each in its own context, closed together."""

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
        page.goto(self.at.url, wait_until="load", timeout=LOAD_TIMEOUT_MS)
        page.evaluate("document.fonts.ready.then(() => 0)")
        return page

    def close(self):
        for ctx in self.contexts:
            ctx.close()
        self.contexts = []


def _settle(page):
    page.evaluate(records.SETTLE_JS, SETTLE_MS)


def _touch_point(page, v):
    """Where the touch drag starts: the window's middle, half a drag low."""
    size = page.viewport_size
    return size["width"] / 2, size["height"] / 2 + v["wheel"] / 2


def _scroll_once(page, name, v):
    if name == "wheel":
        pointer.wheel(page, None, dy=v["wheel"])
    elif name == "key":
        page.keyboard.press("PageDown")
    else:
        # Chromium's synthesized scroll gesture scrolls nothing
        # headless, so the touches are sent one by one.
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
    """native-scroll's answer, from one scroll by each input. A touch drag is
    left out where the part under it pans itself, as a map does."""
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
    """parallax's and replay's answers, from one page swept down, up and down."""
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
    # As long again at rest, so motion that starts by the clock, not the
    # scroll, is known and left out of the replays.
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
    """The carousel's frame changes over `ms` of the page's clock, each the
    page's time of it in ms and the frame."""
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
    """The window's frames over `seconds`, from Chromium's screencast: each
    frame's time in s and its pixels averaged into CELL_PX cells, sRGB in [0, 1]."""
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
    """The part's path, one position a frame, until it holds still."""
    page.evaluate(records.PATH_JS, [sel, axis, STILL_MS, PATH_CAP_MS])
    page.wait_for_function("() => window.__path")
    return page.evaluate("() => window.__path")


def _fling(page, sel, axis, *, way, along):
    """Flings the part `way` along `axis` and lets go: where it was let go,
    the velocity the page was handed at the release, and its path after.
    Each event carries the time it would have had a frame apart, so the page
    is handed the same throw however late the machine sends it."""
    dx, dy = along
    x0, y0 = page.evaluate(records.CENTRE_JS, [sel, False])
    page.evaluate(
        "(w) => { window.__watch = w; window.__path = null; }",
        [sel, axis, STILL_MS, PATH_CAP_MS],
    )
    cdp = page.context.new_cdp_session(page)
    frame = DRAG_FRAME_MS / 1000
    # Stamped so the release's time is now, and no event is stamped later
    # than it is sent.
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
                # Let go off the control, so the press clicks nothing.
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


# Each check's run, taking every line's value and giving the answer of each
# check it reads: parallax's run answers replay too.
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
    """Each table line's check's Answer."""
    layout = _sibling("check_layout", "check-layout.py")
    phone = (layout.PHONE_WIDTH, layout.HEIGHTS[0], layout.PHONE)
    values = {line.mode: line.value for line in at.lines}
    out = {}
    with chromium() as browser:
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
    # The flash film needs numpy and Pillow; they are checked before the
    # browser starts, since run_browser() reads any ImportError as
    # Playwright's.
    try:
        import numpy  # noqa: F401 - imported only to learn it is installed
        import PIL  # noqa: F401 - imported only to learn it is installed
    except ImportError as err:
        # Exit 3, naming the package and its pinned install (#256, #477).
        return missing(err)
    got, code = run_browser(lambda: run_records(at), at.timeout, at.url)
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
    p.add_argument("--fps", type=int, default=FPS)
    p.add_argument("--pause-ms", type=int, default=PAUSE_MS, metavar="MS")
    p.add_argument(
        "--jolt-ratio",
        type=float,
        metavar="R",
        help="one jolt line at every move length, in place of the line that falls as a move lengthens",
    )
    p.add_argument(
        "--view-cm",
        type=float,
        default=VIEW_CM,
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
    p.add_argument("--timeout", type=int, default=PLAY_TIMEOUT_MS, metavar="MS")
    p.add_argument("--viewport", default=DESKTOP, metavar="WxH")
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
    at.viewport_size = size_arg(p, "--viewport", at.viewport)
    at.url = page_url(p, at.url)
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
            probe = _sibling("probe", "probe.py")
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
    sample, code = run_browser(
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
    result = analyse(sample, at.pause_ms, at.jolt_ratio, at.view_cm)
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
        # An earlier run's file would be checked as this page's.
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
    sys.exit(main(sys.argv[1:]))
