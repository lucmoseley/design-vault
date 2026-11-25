#!/usr/bin/env python3
"""check-layout.py — sweeps a web candidate across every width from 320 to
1920 px, and at 2560 px, for the layout faults a critic would otherwise find one width at a
time (design-vault#78), answering gate questions vault.reflow and vault.layout,
with --text spacing vault.text-spacing (#305), with --records the tier 0
and 1 layout records (#311) and with --focal vault.focal-crop (#334), and
takes the screenshots the critic is given.

USAGE
  python3 check-layout.py <url or file> --out DIR [--cta SELECTOR] [--step PX]
        [--widths LOW-HIGH] [--heights PHONE,TABLET,DESKTOP] [--timeout MS]
        [--text spacing|zoom|size]… [--table FILE]
        [--records [--parts FILE] [--brief kind=app|site] [--brief page=reading|default|canvas]]
        [--focal SELECTOR=X,Y,W,H]…

It loads the page afresh at each width, every --step px (5) from 320 to 1920
and once at 2560, lets its fonts load and its animations finish, and reports each fault as the
range of widths it holds over:

- sideways scroll: the page is wider than the screen, naming the outermost
  element past its right edge, how far, and the innermost one inside it;
- text cut off: text past the screen's edge that no one can scroll to, because
  the page hides its sideways overflow or the text sits off the left edge;
- overlap: a text block's lines crossing another text block's, crossing an
  image's edge, or lying under an image. Text wholly inside an image's box and
  drawn on top of it is a caption or a hero overlay, and is not reported. An
  image is an img, svg, video, canvas, object or embed, or a box with a
  background image; text is never checked against its own box's background.
  Lines are trimmed to their line-height, and a crossing under 2 px either way
  is not counted;
- the viewport, at phone widths: the page's last viewport meta must have a
  phone lay the page out at the phone's own width and show it at scale 1, as
  Chromium reads it on a page loaded as a phone (Playwright's is_mobile),
  which with no meta lays it out 980 px wide and shrinks it to fit. Nor may
  any viewport meta keep a visitor from zooming to 200%: user-scalable=no, or
  a maximum-scale under 2, fails, as W3C ACT rule b4f0c3 reads WCAG 1.4.4. A
  page that fails the first is shown on a phone at a width the other phone
  findings were not measured at;
- the first screen, with --cta: no element the selector matches lies wholly
  within the first screen at that width;
- the art's focal box, with --focal SELECTOR=X,Y,W,H, the box the art's brief
  declares in the art file's own pixels (#334): the part of it the page shows
  is less than all of it. That part is worked out from an <img>'s object-fit
  and object-position within its content box, or from a box's one background
  image's background-size, -position, -origin and -clip, then cut to the
  element's clipping ancestors and the screen's sides. The page scrolls down
  to any of it, never above its top, and a fixed box's art never leaves the
  first screen. Each shown element the selector matches is judged, and one it
  matches but the page does not show is listed and fails nothing. Art drawn
  over the focal box is not seen. An art it cannot model (a transform, more
  than one background image, a fixed or canvas background, a position it
  cannot read, an art file whose size changes between widths, a focal box
  past the file's edge, or an art shown at no swept width) is listed as not
  measured.

The first five answer vault.reflow, the cta check vault.layout and the
focal check vault.focal-crop: the report gives each question pass or fail,
with its faults under it, vault.layout not checked with no --cta,
vault.focal-crop not checked with no --focal or "cannot measure" where an art
was not measured and none failed, and layout.json's "answers" the same, null
for not checked.

Each --text also loads the page at every width enlarged or spaced, and
reports what it shows there that the page at 100% at that width does not:
text cut off at the screen's edge, overlap, and text a box hides past its
edge (overflow hidden or clip), the text's own box included, more than at
100%. Text a scroller between it and that box can scroll to is not
hidden, nor is an SVG's text, an image of text. Hidden text in a link or in
a box holding a control (a button, summary, aria-expanded or aria-controls)
fails nothing: it is listed for vault.text-spacing-reveal's look critics,
since the link's page or the control may show it.

- --text spacing sets WCAG 1.4.12's line height, spacing after paragraphs
  (on <p>), letter spacing and word spacing, as inline !important on every
  element, which outranks the page's own !important, and answers
  vault.text-spacing, failing on any loss but text listed for the look;
- --text zoom emulates browser zoom: a screen W px wide is laid out W/zoom
  CSS px wide at a device scale of the zoom, on screens no narrower than
  the zoom times 320 px, reflow's floor;
- --text size raises the browser's default text sizes, proportional and
  monospace, by the factor (Chromium's Page.setFontSizes), so rem, em and
  keyword sizes grow and px sizes do not.

Zoom and size also list each text that grows less than the factor, beside
its size at 100%, for the records that judge text size; it fails nothing.
The values come from THE TABLE, check-layout.table beside this script or
--table FILE: lines of record id | mode | value, read with --text and
--records.
layout.json's "text" holds each mode's record, value and findings, and
for size the default text sizes set, proportional and monospace, in px.

--records runs each table line whose mode is a check of layout-records.py
(its CHECKS), at every width and on loads of its own: zoomed and with a larger
default text size, script off, an emulated safe-area inset and each popover
or menu opened. --parts is the round's parts declaration, which names the
card, the logo, the empty state and the category tile; --brief gives the brief's facts a check reads. A record
answers fail where any of its checks found a fault at any width, not judged
where a check lacks a part or fact, pass where a check found something it
applies to, else no match; layout.json's "records" holds the answers, what
each not-judged record lacks and the fault ranges.

The screen is --heights px tall: 664 at phone widths (320–767 px), 921 at
tablet (768–1023) and 633 at desktop (1024–2560), each a common screen less
the browser's own bars (HEIGHTS says which). Pass the project's own where it
has them. At phone widths the browser has a touch screen, so a page's
`(pointer: coarse)` and `(hover: none)` rules apply there.

--widths sweeps part of that span, to re-check a range after a fix. A partial
sweep, or one with a step over 5 px, prints NOT A GATING SWEEP and writes
"gating": false; a critic is given only a gating sweep's folder. A looping
animation cannot finish, so the page is measured mid-loop and the report says
how many loop.

It writes full-page screenshots at 320, 390, 768, 1024, 1536, 1920 and 2560 px, those
in the swept span, to DIR/layout-<width>-<run time>.png, and DIR/layout.json,
every width's findings, deleting any an earlier run left there. The run time in
each name, UTC, is what a critic compares with the candidate's last change
(design-round §4).

A fault the brief chose, such as a heading set across an image's edge, is
still reported: say so beside it in the round folder.

EXITS 0 no fault at any width / 1 a fault (each printed) / 2 the arguments are
wrong, the selectors and the table included / 3 Playwright or its browser is
missing / 4 the page did not render in time / 5 the browser refused the page / 6
no fault, but a --focal art was not measured (each printed) / 7 a call hung that
would never return. Exits 0, 1 and 6 print on stdout; the rest print on stderr.
"""

import argparse
import collections
import datetime
import importlib.util
import json
import os
import pathlib
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "check_flow", os.path.join(HERE, "check-flow.py")
)
flow = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(flow)


def _load(name, file):
    """A sibling script loaded by path."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


records = _load("layout_records", "layout-records.py")
rule_table = _load("rule_table", "rule-table.py")


# 320 is WCAG 1.4.10's reflow width, a 1280 px desktop at 400% zoom. 2560 is
# the widest common desktop (#197). Above STEPPED only HIGH is loaded: a page
# built for 1920 mostly fails wider by stretching, which shows widest. A fault
# held only between the two is not seen.
LOW, STEPPED, HIGH = 320, 1920, 2560
# The widest step that still finds a fault a few px wide (#78: "at most 5 px").
GATE_STEP = 5
# Bands split at Tailwind's md and lg breakpoints.
BANDS = (("phone", 320, 767), ("tablet", 768, 1023), ("desktop", 1024, HIGH))
PHONE_MAX = BANDS[0][2]
# Each band's first screen (#197). Phone: Safari on a 390x844 iPhone 13 or 14,
# 390x664 in Playwright's device list. Desktop: Chromium maximised on Windows
# 11 on a 1366x768 screen, its taskbar and bars measured. Tablet: a 768x1024
# iPad less 103 px of status bar and Safari's address and tab bars, as one
# developer read them on an iPad Air 3 under iPadOS 16.5.1
# (developer.apple.com/forums/thread/735055, #252). Unmeasured here or on
# iPadOS 26.
HEIGHTS = (664, 921, 768 - flow.DESKTOP_BARS)
MOTION_HEIGHTS = (*HEIGHTS[:2], flow.DESKTOP_WINDOW[1])
# A common phone's width and the commonest desktop's (StatCounter Sept 2026),
# the widths the other checks render a page at.
PHONE_WIDTH, DESKTOP_WIDTH = 390, flow.DESKTOP_SCREEN[0]
# The band edges, the widths above, the next commonest desktop and the widest.
SHOT_WIDTHS = (320, PHONE_WIDTH, 768, 1024, 1536, DESKTOP_WIDTH, HIGH)
# A phone's touch screen, through the phone band (#190). Not Playwright's
# is_mobile, which lays the page out by its viewport meta and swaps in
# DevTools' mobile theme. The meta is judged apart, on a page loaded as MOBILE
# (#229). A page a phone would zoom out is laid out wider than the phone, a
# viewport fault, or overflows it, a scroll fault, so the checks' shots at
# scale 1 misread only a page that already fails vault.reflow.
#
# The theme is left out, so vault.focus judges at phone width the ring Chrome
# on Android draws (#229). Chrome sets its focus ring to rgb(16, 16, 16) on
# every platform but the Mac (chrome/browser/renderer_preferences_util.cc), on
# the theme Blink has then. Android's own theme takes it. The mobile theme,
# switched on only by DevTools' emulation (core/inspector/dev_tools_emulator.cc),
# never gets it, so it draws Blink's fallback rgb(229, 151, 0), 2.40:1 on white
# (core/layout/layout_theme.cc). Read in Chromium's source, not on a device.
# Residuals: an app's in-app browser, Android WebView, sets no ring
# (android_webview/browser/aw_settings.cc) and so draws that fallback, which
# WCAG exempts from 3:1 as the browser's own (Understanding 1.4.11); and the
# tablet band is not laid out by the meta, though a tablet's browser may read it.
PHONE = {"has_touch": True}
MOBILE = {**PHONE, "is_mobile": True}
# W3C ACT rule b4f0c3: zoom must reach 200%. Values that are not numbers pass
# only as these.
ZOOM = 2
# A shown scale this far from 1 still counts as 1, for rounding. A guess.
SCALE_SLACK = 0.01
SCALABLE_WORDS = ("yes", "device-width", "device-height")
MAX_SCALE_WORDS = ("device-width", "device-height")
# `fails`: whether a finding of the kind fails its question.
Kind = collections.namedtuple("Kind", "key title question fails", defaults=(True,))
KINDS = (
    Kind("scroll", "sideways scroll", "vault.reflow"),
    Kind("cut", "text cut off at the screen's edge", "vault.reflow"),
    Kind("overlap", "overlap", "vault.reflow"),
    Kind("viewport", "not laid out at the phone's width", "vault.reflow"),
    Kind("zoom", "zoom blocked on a phone", "vault.reflow"),
    Kind("cta", "call to action off the first screen", "vault.layout"),
    # Wholly visible at every width: untraced, the plain reading of #262's
    # "keeps the focal element" (#334).
    Kind("crop", "focal box not wholly in view", "vault.focal-crop"),
    # An art the check cannot see is unjudged, neither passed nor failed
    # (#334): it exits 6, so a caller that reads only 0 as a pass does not
    # pass it.
    Kind("unshown", "art not shown, so not judged", "vault.focal-crop", False),
    Kind("unmeasured", "art not measured", "vault.focal-crop", False),
)
QUESTIONS = tuple(dict.fromkeys(k.question for k in KINDS))
CTA_QUESTION = next(k.question for k in KINDS if k.key == "cta")
FOCAL_QUESTION = next(k.question for k in KINDS if k.key == "crop")
# The flag a question is not checked without.
OPTIONAL = {CTA_QUESTION: "--cta", FOCAL_QUESTION: "--focal"}
# What a --text mode reports, beside the 100% page at the same width.
TEXT_KINDS = (
    Kind("cut", "text cut off at the screen's edge", None),
    Kind("overlap", "overlap", None),
    Kind("clip", "text a box hides past its edge", None),
    Kind("reveal", "text hidden in a link or beside a control", None, False),
    # A reading for the records that judge text size (#311), not a loss.
    Kind("grow", "text that grows less than the rest", None, False),
)
SPACING_QUESTION = "vault.text-spacing"
REVEAL_QUESTION = "vault.text-spacing-reveal"
# Hidden text counts as more hidden than at 100% only once this much more of
# its area is hidden. A guess: a 2 px sliver of a 16 px line is an eighth.
HIDDEN_MORE = 0.05
# A computed size this short of the factor still counts as grown, for px
# rounding. A guess.
GROW_SLACK = 0.01
TABLE = os.path.join(HERE, "check-layout.table")
SEP = " | "
NUMBER = r"(\d+(?:\.\d+)?)"
# --focal's value: a selector, then the focal box's left, top, width and height.
FOCAL_ARG = re.compile(rf"(.+)={NUMBER},{NUMBER},{NUMBER},{NUMBER}")
# Each --text mode and the shape of its table value.
MODES = {
    "spacing": re.compile(
        rf"line-height {NUMBER}, after-paragraph {NUMBER}, letter-spacing {NUMBER}, word-spacing {NUMBER}"
    ),
    "zoom": re.compile(NUMBER),
    "size": re.compile(NUMBER),
}
Mode = collections.namedtuple("Mode", "id name value")
RECORD_KINDS = tuple(Kind(name, name, None) for name in records.CHECKS)
# The record checks read on their own loads, not by records.READ_JS.
APART = ("fluid-zoom", "tabs-narrow", "popover-sheet", "line-length", "phone-width")
UNREAD = "a style sheet from another origin cannot be read"


class BadSelectorError(Exception):
    """A --cta or --focal selector the browser does not accept: exit 2. Its
    args are the flag, the selector and the browser's message."""


TableError = rule_table.TableError


def parse_table(text):
    """{mode: Mode} from the table's lines; a spacing value is its four
    numbers by property, a zoom or size value the factor text is enlarged by."""
    out = {}
    for n, line in rule_table.lines(text):
        fields = [f.strip() for f in line.split(SEP)]
        if len(fields) != 3 or fields[1] not in (*MODES, *records.CHECKS):
            raise TableError(
                f"line {n}: want ID | {' or '.join(MODES)} or a record check | VALUE, got {line!r}"
            )
        if fields[1] in out:
            raise TableError(f"line {n}: a second {fields[1]} line")
        if fields[1] in records.CHECKS:
            try:
                value = records.parse_value(fields[1], fields[2])
            except ValueError as exc:
                raise TableError(f"line {n}: {exc}") from None
            out[fields[1]] = Mode(fields[0], fields[1], value)
            continue
        m = MODES[fields[1]].fullmatch(fields[2])
        if not m:
            raise TableError(
                f"line {n}: {fields[1]} wants a value like {MODES[fields[1]].pattern!r}, got {fields[2]!r}"
            )
        numbers = [float(g) for g in m.groups()]
        if fields[1] != "spacing" and numbers[0] <= 0:
            raise TableError(
                f"line {n}: {fields[1]} wants a factor over 0, got {fields[2]!r}"
            )
        value = (
            dict(
                zip(
                    (
                        "line-height",
                        "after-paragraph",
                        "letter-spacing",
                        "word-spacing",
                    ),
                    numbers,
                    strict=True,
                )
            )
            if fields[1] == "spacing"
            else numbers[0]
        )
        out[fields[1]] = Mode(fields[0], fields[1], value)
    return out


# Lets the page finish arriving: its fonts, and its entrance animations run to
# their end state. A looping animation throws on finish() and is measured
# mid-loop, by design (#78).
SETTLE_JS = r"""
async () => {
  await document.fonts.ready;
  let looping = 0;
  for (const a of document.getAnimations()) { try { a.finish(); } catch (e) { looping++; } }
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  scrollTo({ top: 0, left: 0, behavior: 'instant' });
  return looping;
}
"""

# One width's faults, as {kind, subject, detail}, and the --focal arts'
# files and placement. Geometry is read at scroll 0.
MEASURE_JS = (
    flow.LABEL_JS
    + r"""
async ({ cta, focal }) => {
  // Guesses, unmeasured: 1 px of slack at an edge for rounding, an overlap only
  // past 2 px each way, text hidden by a box only past 2 px, as glyphs'
  // side bearings and rounding reach about that far, a text box under half a px empty, and an image under
  // 4 px a side a rule or spacer, not a picture.
  const EDGE = 1, CROSS = 2, HIDDEN = 2, EMPTY = 0.5, MIN_IMAGE = 4;
  const vw = document.documentElement.clientWidth, vh = innerHeight;
  const css = (el) => getComputedStyle(el);
  const faults = [];
  const add = (kind, subject, detail) => faults.push({ kind, subject, detail });
  const clips = (cs) => cs.overflowX !== 'visible' || cs.overflowY !== 'visible';
  const html = css(document.documentElement), body = css(document.body);
  const hides = (v) => v === 'hidden' || v === 'clip';
  const visible = (v) => v === 'visible';
  // Body's overflow clips the page whether it reaches the viewport or not.
  const rootClips = hides(html.overflowX) || hides(body.overflowX);
  const rootHidesY = hides(html.overflowY) || hides(body.overflowY);

  // A box clipped to nothing, by clip or an inset clip-path, or 1x1 px or
  // smaller with its overflow clipped: the visually-hidden pattern, text kept
  // for a screen reader alone (#220).
  const toPx = (v, size) => (v.endsWith('%') ? (parseFloat(v) / 100) * size : parseFloat(v));
  const clipRectGone = (cs, box) => {
    const m = /^rect\((.*)\)$/.exec(cs.clip);
    if (!m || (cs.position !== 'absolute' && cs.position !== 'fixed')) return false;
    const [top, right, bottom, left] = m[1].split(/[\s,]+/)
      .map((v, i) => (v === 'auto' ? [0, box.width, box.height, 0][i] : parseFloat(v)));
    return bottom <= top || right <= left;
  };
  const insetGone = (cs, box) => {
    const m = /^inset\(\s*(.*?)(?:\s+round\b.*)?\)$/.exec(cs.clipPath);
    if (!m) return false;
    const v = m[1].split(/\s+/);
    const [top, right, bottom, left] = [v[0], v[1] ?? v[0], v[2] ?? v[0], v[3] ?? v[1] ?? v[0]];
    return toPx(top, box.height) + toPx(bottom, box.height) >= box.height
      || toPx(left, box.width) + toPx(right, box.width) >= box.width;
  };
  const clippedAway = (el, cs) => {
    const box = el.getBoundingClientRect();
    return (box.width <= 1 && box.height <= 1 && clips(cs)) || clipRectGone(cs, box) || insetGone(cs, box);
  };
  const shownCache = new Map();
  const shown = (el) => {
    if (!el || el.nodeType !== 1) return true;
    if (shownCache.has(el)) return shownCache.get(el);
    const cs = css(el);
    // checkVisibility() is false under a content-visibility: hidden ancestor,
    // which is how Chromium hides a closed <details>' content (#418), and for
    // display: contents, which has no box but draws its children.
    // Residual: content-visibility: auto content off screen still counts as shown.
    const seen = cs.display === 'contents' || el.checkVisibility({ opacityProperty: true, visibilityProperty: true });
    const v = seen && !clippedAway(el, cs) && shown(el.parentElement);
    shownCache.set(el, v);
    return v;
  };
  const rect = (r) => ({ left: r.left, top: r.top, right: r.right, bottom: r.bottom });
  // The elements a selector matches, or the browser's message refusing it.
  const matching = (selector) => { try { return [...document.querySelectorAll(selector)]; } catch (e) { return String(e.message || e); } };
  const intersect = (a, b) => ({ left: Math.max(a.left, b.left), top: Math.max(a.top, b.top),
    right: Math.min(a.right, b.right), bottom: Math.min(a.bottom, b.bottom) });
  // The part of the viewport an element's ancestors let it paint in, below
  // body: a scroll container or a clipping box. Null where none clips it. A
  // fixed box escapes every ancestor's clip, and an absolute one those below
  // its positioned ancestor; a transform's containing block is not modelled.
  const isRoot = (e) => !e || e === document.body || e === document.documentElement;
  const clipCache = new Map();
  const clipOf = (el) => {
    const pos = css(el).position;
    if (pos === 'fixed') return null;
    let p = el.parentElement;
    if (pos === 'absolute') while (!isRoot(p) && css(p).position === 'static') p = p.parentElement;
    return isRoot(p) ? null : clipFrom(p);
  };
  const clipFrom = (p) => {
    if (clipCache.has(p)) return clipCache.get(p);
    let box = clipOf(p);
    if (clips(css(p))) box = box ? intersect(box, p.getBoundingClientRect()) : rect(p.getBoundingClientRect());
    clipCache.set(p, box);
    return box;
  };
  // The boxes that hide an element's overflow rather than scroll it, each
  // with the padding box it shows, unbounded on an axis it does not hide or
  // on which a box between them scrolls.
  // The containing-block walk is clipOf's.
  const hiderCache = new Map();
  const hidersOf = (el) => {
    const pos = css(el).position;
    if (pos === 'fixed') return [];
    let p = el.parentElement;
    if (pos === 'absolute') while (!isRoot(p) && css(p).position === 'static') p = p.parentElement;
    return isRoot(p) ? [] : hidersFrom(p);
  };
  const hidersFrom = (p) => {
    if (hiderCache.has(p)) return hiderCache.get(p);
    const cs = css(p), x = hides(cs.overflowX), y = hides(cs.overflowY);
    const own = [];
    if (x || y) {
      const r = p.getBoundingClientRect(), left = r.left + p.clientLeft, top = r.top + p.clientTop;
      own.push({ el: p, left: x ? left : -Infinity, right: x ? left + p.clientWidth : Infinity,
        top: y ? top : -Infinity, bottom: y ? top + p.clientHeight : Infinity });
    }
    const sx = !visible(cs.overflowX) && !x, sy = !visible(cs.overflowY) && !y;
    const up = hidersOf(p).map((o) => ({ ...o, left: sx ? -Infinity : o.left, right: sx ? Infinity : o.right,
      top: sy ? -Infinity : o.top, bottom: sy ? Infinity : o.bottom }));
    const v = own.concat(up.filter((o) => o.left > -Infinity || o.right < Infinity || o.top > -Infinity || o.bottom < Infinity));
    hiderCache.set(p, v);
    return v;
  };
  const w = (r) => r.right - r.left, h = (r) => r.bottom - r.top;
  const fixedCache = new Map();
  const fixed = (el) => {
    if (!el || el === document.documentElement) return false;
    if (fixedCache.has(el)) return fixedCache.get(el);
    const v = css(el).position === 'fixed' || fixed(el.parentElement);
    fixedCache.set(el, v);
    return v;
  };

  // Sideways scroll, by the outermost elements past the right edge.
  const all = [...document.body.querySelectorAll('*')];
  const place = new Map(all.map((e, i) => [e, i]));
  if (!rootClips && document.documentElement.scrollWidth > vw + EDGE) {
    const past = new Set();
    for (const el of all) {
      if (clipOf(el) || fixed(el) || !shown(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.height > 0 && r.right > vw + EDGE) past.add(el);
    }
    // The outermost is the subject; a flex or grid item stretched by its
    // content is outermost, so the innermost inside it names the likely cause.
    const outer = [...past].filter((el) => { for (let p = el.parentElement; p; p = p.parentElement) if (past.has(p)) return false; return true; });
    const innermost = (el) => [...past].find((e) => el.contains(e) && ![...e.children].some((c) => past.has(c)));
    const by = document.documentElement.scrollWidth - vw;
    if (!outer.length) add('scroll', 'the page', `scrolls ${by} px sideways`);
    for (const el of outer) {
      const inner = innermost(el);
      add('scroll', label(el), `reaches ${Math.round(el.getBoundingClientRect().right - vw)} px past the screen's right edge` +
        (inner && inner !== el ? `, with ${label(inner)} inside it` : '') + `; the page scrolls ${by} px sideways`);
    }
  }

  // Every visible line of text, trimmed to its line-height and to what its
  // clipping ancestors show.
  const blockOf = (el) => {
    for (let e = el; e; e = e.parentElement) { const d = css(e).display; if (d !== 'inline' && d !== 'contents') return e; }
    return document.body;
  };
  const texts = [];
  // Each text's element by its place among body's elements, its label and font size in px.
  const sizes = new Map();
  // Text a box hides past its edge, by block: the most px hidden, the box,
  // and the block's text area in all and shown.
  const hidden = new Map(), area_ = new Map();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const range = document.createRange();
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const el = n.parentElement;
    if (!/\S/.test(n.data) || !el || !shown(el) || ['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE'].includes(el.tagName)) continue;
    const image = el.closest('svg');
    if (!image && !sizes.has(el)) sizes.set(el, [place.get(el), label(el), parseFloat(css(el).fontSize)]);
    const hiders = image ? [] : hidersFrom(el);
    const shows = hiders.length ? hiders.reduce(intersect) : null;
    const lh = parseFloat(css(el).lineHeight);
    const box = clipOf(el);
    range.selectNodeContents(n);
    for (const raw of range.getClientRects()) {
      const r = rect(raw);
      if (lh && h(r) > lh) { const mid = (r.top + r.bottom) / 2; r.top = mid - lh / 2; r.bottom = mid + lh / 2; }
      if (w(r) < EMPTY || h(r) < EMPTY) continue;
      const block = blockOf(el);
      const area = area_.get(block) || { all: 0, shown: 0 };
      const part = shows ? intersect(r, shows) : r;
      area.all += w(r) * h(r);
      area.shown += Math.max(0, w(part)) * Math.max(0, h(part));
      area_.set(block, area);
      for (const hider of hiders) {
        const by = Math.max(hider.left - r.left, r.right - hider.right, hider.top - r.top, r.bottom - hider.bottom);
        if (by <= HIDDEN) continue;
        const was = hidden.get(block);
        if (!was || by > was.by) hidden.set(block, { by, hider: hider.el });
        break;
      }
      const seen = box ? intersect(r, box) : r;
      if (w(seen) <= 0 || h(seen) <= 0) continue;
      texts.push({ el, block: blockOf(el), r: seen, fixed: fixed(el) });
    }
  }

  // Text past an edge no one can scroll to, by the part its ancestors show.
  const cutOff = new Map();
  for (const t of texts) {
    const right = t.r.right - vw, left = -t.r.left;
    const unreachable = left > EDGE || (right > EDGE && (rootClips || t.fixed));
    if (unreachable) cutOff.set(t.block, Math.max(cutOff.get(t.block) || 0, Math.round(Math.max(left, right))));
  }
  for (const [block, by] of cutOff) add('cut', label(block), `runs ${by} px past the screen's edge`);
  const CONTROL = 'button, summary, [role="button"], [aria-expanded], [aria-controls]';
  for (const [block, { by, hider }] of hidden) {
    const where = hider === block ? 'its own edge, as it hides its overflow' : `the edge of ${label(hider)}, which hides its overflow`;
    const kind = block.closest('a[href]') || hider.querySelector(CONTROL) ? 'reveal' : 'clip';
    const { all, shown: seen } = area_.get(block);
    faults.push({ kind, subject: label(block), detail: `has ${Math.round(by)} px of its text hidden past ${where}`,
      place: place.get(block), share: all ? 1 - seen / all : 0 });
  }

  // Images: replaced elements and boxes with a background image.
  const images = [];
  for (const el of all) {
    const tag = el.localName;
    const replaced = ['img', 'video', 'canvas', 'object', 'embed'].includes(tag) || (tag === 'svg' && !el.parentElement.closest('svg'));
    if (!replaced && !/url\(/.test(css(el).backgroundImage)) continue;
    if (!shown(el)) continue;
    const raw = el.getBoundingClientRect();
    const box = clipOf(el);
    const r = box ? intersect(raw, box) : rect(raw);
    if (w(r) >= MIN_IMAGE && h(r) >= MIN_IMAGE) images.push({ el, r });
  }

  const crosses = (a, b) => { const c = intersect(a, b); return w(c) > CROSS && h(c) > CROSS; };
  const within = (a, b) => a.left >= b.left - EDGE && a.right <= b.right + EDGE && a.top >= b.top - EDGE && a.bottom <= b.bottom + EDGE;
  const pairs = new Map();
  const note = (subject, detail) => { if (!pairs.has(subject) || detail.startsWith('hidden')) pairs.set(subject, detail); };

  // Text over text, between different blocks.
  const sorted = texts.slice().sort((a, b) => a.r.top - b.r.top);
  for (let i = 0; i < sorted.length; i++) {
    const a = sorted[i];
    for (let j = i + 1; j < sorted.length && sorted[j].r.top < a.r.bottom - CROSS; j++) {
      const b = sorted[j];
      if (a.block === b.block || !crosses(a.r, b.r)) continue;
      const names = [label(a.block), label(b.block)].sort();
      note(`${names[0]} and ${names[1]}`, 'text lines cross');
    }
  }

  // Text against images: crossing an edge always; wholly inside, only when
  // the image is drawn over it, which the stack at that point shows.
  const stackCheck = [];
  for (const t of texts) {
    for (const im of images) {
      if (im.el.contains(t.el) || t.el.contains(im.el) || !crosses(t.r, im.r)) continue;
      const subject = `${label(t.block)} text and ${label(im.el)}`;
      if (!within(t.r, im.r)) note(subject, 'the text crosses the image\'s edge');
      else stackCheck.push({ t, im, subject });
    }
  }
  // elementsFromPoint skips pointer-events: none, common on decorative
  // layers, so every element takes pointer events while the stack is read.
  // A point off the screen's side cannot be read; that text is cut off anyway.
  const probe = document.createElement('style');
  probe.textContent = '* { pointer-events: auto !important }';
  document.head.append(probe);
  for (const { t, im, subject } of stackCheck) {
    const c = intersect(t.r, im.r);
    const x = (c.left + c.right) / 2, y = (c.top + c.bottom) / 2;
    if (x < 0 || x >= vw || y < 0) continue;
    // Rects were read at scroll 0; a fixed box's stay put as the page scrolls.
    const top = t.fixed || y < vh ? 0 : y - vh / 2;
    scrollTo({ top, left: 0, behavior: 'instant' });
    const stack = document.elementsFromPoint(x, y - scrollY).filter((e) => !fixed(e) || t.fixed);
    const i = stack.findIndex((e) => e === im.el || im.el.contains(e));
    const j = stack.indexOf(t.el);
    if (i >= 0 && j >= 0 && i < j) note(subject, 'the text is hidden under the image');
  }
  probe.remove();
  scrollTo({ top: 0, left: 0, behavior: 'instant' });
  for (const [subject, detail] of pairs) add('overlap', subject, detail);

  // The first screen.
  if (cta !== null) {
    const matched = matching(cta);
    if (typeof matched === 'string') return { badSelector: ['--cta', cta, matched] };
    const boxes = matched.filter(shown).map((el) => el.getBoundingClientRect()).filter((r) => r.width > 0 && r.height > 0);
    const fits = boxes.some((r) => r.top >= -EDGE && r.bottom <= vh + EDGE && r.left >= -EDGE && r.right <= vw + EDGE);
    if (!matched.length) add('cta', cta, 'matches nothing');
    else if (!boxes.length) add('cta', cta, 'is not shown');
    else if (!fits) {
      const r = boxes.reduce((a, b) => (a.top <= b.top ? a : b));
      add('cta', cta, r.bottom > vh + EDGE ? `ends ${Math.round(r.bottom)} px down; the first screen is ${vh} px tall` : 'sits past the screen\'s side');
    }
  }

  // The art's focal boxes (#334). A layer that repeats is judged by the one
  // tile its position places.
  const layers = (v) => v.split(/,(?![^(]*\))/).map((s) => s.trim());
  // One axis of a computed position, as px from the area's start, where
  // `free` is the area less the art; null for a form it cannot read.
  // Chromium computes a keyword, and a keyword with an offset, to a
  // percentage or calc(P% ± Npx).
  const along = (v, free) => {
    let m;
    if ((m = /^(-?[\d.]+)%$/.exec(v))) return (m[1] / 100) * free;
    if ((m = /^(-?[\d.]+)px$/.exec(v))) return +m[1];
    if ((m = /^calc\((-?[\d.]+)% ([+-]) ([\d.]+)px\)$/.exec(v))) return (m[1] / 100) * free + (m[2] === '-' ? -m[3] : +m[3]);
    return null;
  };
  // object-position's two axes, x first.
  const axes = (v) => {
    const t = v.match(/(?:[^\s(]+|\([^)]*\))+/g) || [];
    return t.length === 2 ? t : [null, null];
  };
  const boxesOf = (cs, r) => {
    const sides = (k) => ['Top', 'Right', 'Bottom', 'Left'].map((s) => parseFloat(cs[k(s)]) || 0);
    const inset = (o, [t, rt, b, l]) => ({ left: o.left + l, top: o.top + t, right: o.right - rt, bottom: o.bottom - b });
    const border = rect(r), padding = inset(border, sides((s) => `border${s}Width`));
    return { 'border-box': border, 'padding-box': padding, 'content-box': inset(padding, sides((s) => `padding${s}`)) };
  };
  const everywhere = { left: -Infinity, top: -Infinity, right: Infinity, bottom: Infinity };
  // An art file's own size in px. An img's natural size is divided by its
  // srcset density, and its w descriptor's density follows the width, so
  // the file is loaded afresh.
  const fileSize = async (src) => {
    const file = new Image();
    file.src = src;
    try { await file.decode(); } catch (e) { return null; }
    return file.naturalWidth && file.naturalHeight ? [file.naturalWidth, file.naturalHeight] : null;
  };
  // The art's file size, where it is placed and the part of the page it may
  // paint, or why it cannot be measured.
  const artOf = async (el) => {
    const cs = css(el);
    if (cs.transform !== 'none') return { unmeasured: `is transformed (${cs.transform}), which this check does not model` };
    const b = boxesOf(cs, el.getBoundingClientRect());
    if (el.localName === 'img') {
      const size = el.complete && el.naturalWidth && el.naturalHeight && (await fileSize(el.currentSrc));
      if (!size) return { unmeasured: 'has not loaded its art' };
      // Its natural size, not the file's, sets how object-fit scales it.
      const iw = el.naturalWidth, ih = el.naturalHeight, c = b['content-box'];
      const cw = w(c), ch = h(c), contain = Math.min(cw / iw, ch / ih);
      const s = { fill: null, contain, cover: Math.max(cw / iw, ch / ih), none: 1, 'scale-down': Math.min(1, contain) }[cs.objectFit];
      if (s === undefined) return { unmeasured: `has an object-fit, ${cs.objectFit}, this check cannot read` };
      const pw = s === null ? cw : iw * s, ph = s === null ? ch : ih * s;
      const [ax, ay] = axes(cs.objectPosition);
      const ox = ax === null ? null : along(ax, cw - pw), oy = ay === null ? null : along(ay, ch - ph);
      if (ox === null || oy === null) return { unmeasured: `has an object-position, ${cs.objectPosition}, this check cannot read` };
      // Chromium's own stylesheet clips an img to its content box.
      const paint = visible(cs.overflowX) && visible(cs.overflowY) ? everywhere : rect(c);
      return { natural: size, placed: { left: c.left + ox, top: c.top + oy, width: pw, height: ph }, paint };
    }
    if (el === document.documentElement || el === document.body) return { unmeasured: 'paints its background on the whole canvas, which this check does not model' };
    const images = layers(cs.backgroundImage);
    const urls = images.flatMap((v, i) => (/^url\(/.test(v) ? [i] : []));
    if (urls.length !== 1) return { unmeasured: urls.length ? `has ${urls.length} background images, so which is the art is not known` : 'is neither an img nor a box with a background image' };
    const i = urls[0], pick = (v) => { const l = layers(v); return l[i % l.length]; };
    if (pick(cs.backgroundAttachment) === 'fixed') return { unmeasured: 'has a fixed background, which moves against its box as the page scrolls' };
    if (/round|space/.test(pick(cs.backgroundRepeat))) return { unmeasured: `repeats its background as ${pick(cs.backgroundRepeat)}, which rescales or moves the tile` };
    const area = b[pick(cs.backgroundOrigin)], paint = b[pick(cs.backgroundClip)];
    if (!paint) return { unmeasured: `clips its background to ${pick(cs.backgroundClip)}, which this check does not model` };
    const size = await fileSize(/^url\("?(.*?)"?\)$/.exec(images[i])[1]);
    if (!size) return { unmeasured: 'has a background image that did not load or has no size of its own' };
    const [iw, ih] = size;
    const aw = w(area), ah = h(area), scale = pick(cs.backgroundSize);
    let pw, ph;
    if (scale === 'cover' || scale === 'contain') {
      const s = (scale === 'cover' ? Math.max : Math.min)(aw / iw, ah / ih);
      [pw, ph] = [iw * s, ih * s];
    } else {
      const [sw, sh = 'auto'] = scale.split(' ');
      [pw, ph] = [sw === 'auto' ? null : along(sw, aw), sh === 'auto' ? null : along(sh, ah)];
      if ((sw !== 'auto' && pw === null) || (sh !== 'auto' && ph === null)) return { unmeasured: `has a background-size, ${scale}, this check cannot read` };
      if (pw === null && ph === null) [pw, ph] = [iw, ih];
      else if (pw === null) pw = (ph * iw) / ih;
      else if (ph === null) ph = (pw * ih) / iw;
    }
    const ox = along(pick(cs.backgroundPositionX), aw - pw), oy = along(pick(cs.backgroundPositionY), ah - ph);
    if (ox === null || oy === null) return { unmeasured: `has a background-position, ${pick(cs.backgroundPositionX)} ${pick(cs.backgroundPositionY)}, this check cannot read` };
    return { natural: [iw, ih], placed: { left: area.left + ox, top: area.top + oy, width: pw, height: ph }, paint: rect(paint) };
  };
  const arts = [];
  for (const { selector, box } of focal) {
    const matched = matching(selector);
    if (typeof matched === 'string') return { badSelector: ['--focal', selector, matched] };
    if (!matched.length) { add('crop', selector, 'matches nothing'); continue; }
    const seen = matched.filter(shown);
    if (!seen.length) add('unshown', selector, 'is not shown at this width');
    for (const el of seen) {
      const subject = matched.length > 1 ? `${selector} (${label(el)})` : selector;
      const art = await artOf(el);
      if (art.unmeasured) { add('unmeasured', subject, art.unmeasured); continue; }
      arts.push({ subject, natural: art.natural });
      const [x, y, fw, fh] = box, [iw, ih] = art.natural, p = art.placed;
      if (x + fw > iw || y + fh > ih) { add('unmeasured', subject, `has a focal box reaching past the ${iw}x${ih} px art file the page loads`); continue; }
      const sx = p.width / iw, sy = p.height / ih;
      const f = { left: p.left + x * sx, top: p.top + y * sy, right: p.left + (x + fw) * sx, bottom: p.top + (y + fh) * sy };
      if (w(f) <= 0 || h(f) <= 0) { add('crop', subject, 'draws its art at no size'); continue; }
      // A box that scrolls lets the visitor reach its art; one that hides its
      // overflow does not.
      const screen = { left: 0, top: 0, right: vw, bottom: fixed(el) || rootHidesY ? vh : Infinity };
      const v = [art.paint, screen, ...hidersOf(el)].reduce(intersect, f);
      const cut = [['left', v.left - f.left, sx], ['right', f.right - v.right, sx], ['top', v.top - f.top, sy], ['bottom', f.bottom - v.bottom, sy]]
        .filter(([, by]) => by > EDGE);
      if (!cut.length) continue;
      const share = (Math.max(0, w(v)) * Math.max(0, h(v))) / (w(f) * h(f));
      add('crop', subject, share <= 0 ? 'shows none of the focal box'
        : `cuts the focal box ${cut.map(([side, by, s]) => `${Math.round(by / s)} px on its ${side}`).join(' and ')}, in the art's pixels, showing ${Math.floor(share * 100)}% of it`);
    }
  }
  return { faults, arts, sizes: [...sizes.values()], scrollWidth: document.documentElement.scrollWidth, height: vh };
}
"""
)


# Every viewport meta's content, the last being the one Chromium obeys, and the
# width it lays the page out at with the scale it shows it at.
VIEWPORT_JS = r"""
() => ({
  metas: [...document.querySelectorAll('meta[name="viewport" i]')].map((m) => m.getAttribute('content') || ''),
  laidWidth: document.documentElement.clientWidth, scale: visualViewport.scale,
})
"""

# WCAG 1.4.12's overrides, set on every element as inline !important, which
# outranks the page's own !important in any stylesheet or cascade layer. The
# spacing after paragraphs goes on <p>, as Understanding 1.4.12 names it.
SPACING_JS = r"""
(v) => {
  for (const el of [document.documentElement, ...document.querySelectorAll('body, body *')]) {
    el.style.setProperty('line-height', String(v['line-height']), 'important');
    el.style.setProperty('letter-spacing', `${v['letter-spacing']}em`, 'important');
    el.style.setProperty('word-spacing', `${v['word-spacing']}em`, 'important');
  }
  for (const p of document.querySelectorAll('p')) p.style.setProperty('margin-block-end', `${v['after-paragraph']}em`, 'important');
}
"""

# The browser's default text sizes in px, proportional and monospace.
DEFAULT_SIZES_JS = r"""
() => {
  const code = document.createElement('code');
  document.documentElement.append(code);
  const sizes = [document.documentElement, code].map((e) => parseFloat(getComputedStyle(e).fontSize));
  code.remove();
  return sizes;
}
"""


def leading_number(value):
    """The decimal number `value` starts with, or None. An exponent is not
    read, as no viewport meta value needs one."""
    m = re.match(r"[-+]?(\d+\.?\d*|\.\d+)", value)
    return float(m[0]) if m else None


def zoom_blocks(content):
    """The viewport meta's properties, as key=value, that keep a phone from
    zooming to ZOOM times: user-scalable off, or a maximum-scale under ZOOM."""
    pairs = re.sub(r"\s*=\s*", "=", (content or "").lower())
    blocks = []
    for item in re.split(r"[,;\s]+", pairs):
        key, _, value = item.partition("=")
        n = leading_number(value)
        if key == "user-scalable":
            ok = value in SCALABLE_WORDS if n is None else abs(n) >= 1
        elif key == "maximum-scale":
            ok = value in MAX_SCALE_WORDS if n is None else n < 0 or n >= ZOOM
        else:
            continue
        if value and not ok:
            blocks.append(item)
    return blocks


def viewport_faults(width, got):
    """The faults in a phone's reading of the page at `width`, from VIEWPORT_JS:
    a layout width or shown scale not the phone's, by the last meta, and a zoom
    limit in any meta, as the ACT rule tests each."""
    faults, subject = [], "the viewport meta"
    laid, scale = got["laidWidth"], got["scale"]
    if laid != width or abs(scale - 1) > SCALE_SLACK:
        shown = f"{round(scale * 100)}%"
        if not got["metas"]:
            detail = f"is missing, so a phone {width} px wide lays the page out {laid} px wide and shows it at {shown}"
        else:
            detail = f'"{got["metas"][-1]}" makes a phone {width} px wide lay the page out {laid} px wide and show it at {shown}'
        faults.append({"kind": "viewport", "subject": subject, "detail": detail})
    blocks = [b for content in got["metas"] for b in zoom_blocks(content)]
    if blocks:
        verb = "keeps" if len(blocks) == 1 else "keep"
        detail = f"{' and '.join(blocks)} {verb} a phone from zooming to {ZOOM * 100}%, as WCAG 1.4.4 asks"
        faults.append({"kind": "zoom", "subject": subject, "detail": detail})
    return faults


def sweep_widths(step, low=LOW, high=HIGH):
    """Every `step` px from `low` up to STEPPED, then STEPPED and `high`."""
    widths = list(range(low, min(high, STEPPED) + 1, step)) or [low]
    for end in (min(high, STEPPED), high):
        if widths[-1] < end:
            widths.append(end)
    return widths


def height_at(width, heights):
    for (_, low, high), tall in zip(BANDS, heights, strict=True):
        if low <= width <= high:
            return tall
    raise ValueError(f"{width} px is outside {LOW}–{HIGH}")


def is_phone(width):
    return width <= PHONE_MAX


def device(width):
    """The browser context options for a screen `width` px wide."""
    return PHONE if is_phone(width) else {}


def ranges(found, kinds=KINDS):
    """found: [(width, [fault…])] in sweep order. Each (kind, subject) held over
    consecutive widths becomes one range, with its detail at its first width,
    ordered by `kinds`."""
    out, open_ = [], {}
    for i, (width, faults) in enumerate(found):
        here = set()
        for f in faults:
            key = (f["kind"], f["subject"])
            if key in here:
                continue
            here.add(key)
            held = open_.get(key)
            if held and held["_last"] == i - 1:
                held["to"], held["_last"] = width, i
            else:
                held = {
                    "kind": f["kind"],
                    "subject": f["subject"],
                    "detail": f["detail"],
                    "from": width,
                    "to": width,
                    "_last": i,
                }
                open_[key] = held
                out.append(held)
    for held in out:
        del held["_last"]
    order = [k.key for k in kinds]
    return sorted(out, key=lambda r: (order.index(r["kind"]), r["from"], r["subject"]))


def span(held):
    return (
        f"{held['from']} px"
        if held["from"] == held["to"]
        else f"{held['from']}–{held['to']} px"
    )


def stamp(when):
    return when.strftime("%Y%m%dT%H%M%SZ")


def load(page, url, width, heights, *, view=None):
    """Loads the page afresh at one width, in a viewport of `view` (width,
    height) CSS px where given; returns how many animations loop."""
    w, h = view or (width, height_at(width, heights))
    page.set_viewport_size({"width": w, "height": h})
    page.goto(url, wait_until="load")
    return page.evaluate(SETTLE_JS)


def text_faults(base, got, *, grow=None):
    """The faults `got` holds, of TEXT_KINDS, that the 100% page `base` at the
    same width does not: hidden text by its element, a share of its area
    hidden more than HIDDEN_MORE over base's, the rest by kind and subject. With `grow` the factor,
    each text that grows by less, read against base's size. A zoomed page's
    sizes are given already multiplied by the zoom."""
    kinds = {k.key for k in TEXT_KINDS}
    seen = {(f["kind"], f["subject"]) for f in base["faults"]}
    hid = {f["place"]: f["share"] for f in base["faults"] if "place" in f}
    out = []
    for f in got["faults"]:
        if f["kind"] not in kinds:
            continue
        if "place" in f:
            if f["share"] - hid.get(f["place"], 0) <= HIDDEN_MORE:
                continue
        elif (f["kind"], f["subject"]) in seen:
            continue
        out.append({k: v for k, v in f.items() if k not in ("place", "share")})
    if grow is not None:
        before = {place: px for place, _, px in base["sizes"]}
        for place, subject, px in got["sizes"]:
            was = before.get(place)
            if was and px / was < grow * (1 - GROW_SLACK):
                out.append(
                    {
                        "kind": "grow",
                        "subject": subject,
                        "detail": f"grows to {round(px / was * 100)}% ({was:g} to {px:g} px), short of {grow * 100:g}%",
                    }
                )
    return out


def zoomed(width, height, factor):
    """The CSS viewport browser zoom by `factor` gives a screen `width` by
    `height` px, or None where it is narrower than LOW, reflow's own floor."""
    w, h = round(width / factor), round(height / factor)
    return (w, h) if w >= LOW else None


def measure(page, cta, focal=()):
    got = page.evaluate(MEASURE_JS, {"cta": cta, "focal": list(focal)})
    if "badSelector" in got:
        raise BadSelectorError(*got["badSelector"])
    return got


def spaced_at(page, at, width, base):
    """--text spacing's faults at `width`, on the page the base was read on."""
    load(page, at.url, width, at.heights)
    page.evaluate(SPACING_JS, at.modes["spacing"].value)
    page.evaluate(SETTLE_JS)
    return text_faults(base, measure(page, None))


def zoomed_at(page_as, at, width, base):
    """--text zoom's faults at `width`, or None on a screen under its floor."""
    factor = at.modes["zoom"].value
    view = zoomed(width, height_at(width, at.heights), factor)
    if not view:
        return None
    page = page_as({**device(width), "device_scale_factor": factor})
    load(page, at.url, width, at.heights, view=view)
    got = measure(page, None)
    got["sizes"] = [[i, s, px * factor] for i, s, px in got["sizes"]]
    return text_faults(base, got, grow=factor)


def sized_at(page_as, at, width, base, *, raised):
    """--text size's faults at `width`, the default sizes `raised`."""
    page = page_as(device(width), raised)
    load(page, at.url, width, at.heights)
    return text_faults(base, measure(page, None), grow=at.modes["size"].value)


class Records:
    """--records' scripts and what the sweep gathers for them: each width's
    faults by width, the checks that found something, and the notes the
    checks read across widths."""

    def __init__(self, at):
        self.checks = at.checks
        self.read = records.with_label(records.READ_JS, flow.LABEL_JS)
        self.fluid = records.with_label(records.FLUID_JS, flow.LABEL_JS)
        self.inset = records.with_label(records.INSET_JS, flow.LABEL_JS)
        self.sheet = records.with_label(records.SHEET_JS, flow.LABEL_JS)
        self.measure = (
            _load("check_measure", "check-measure.py")
            if "line-length" in self.checks
            else None
        )
        self.found = collections.defaultdict(list)
        self.seen = set()
        self.notes = []
        # Checks the page itself kept from judging, and why.
        self.unmet = {}
        self.phone_under = at.checks["phone-width"].value["under"]

    def phone(self, width):
        """Whether the phone-only checks judge at `width`: under the records'
        phone bound, the table's phone-width line."""
        return width < self.phone_under

    def add(self, width, faults, seen=()):
        self.found[width].extend(faults)
        self.seen.update(seen)

    def lines(self, only=None):
        """The table values READ_JS takes, `only` those named."""
        return {
            name: m.value
            for name, m in self.checks.items()
            if name not in APART and (only is None or name in only)
        }


def read_records(page, at, width, rec, *, page_as, raised, safe):
    """--records' reads at `width`, on the sweep's page and the loads its
    checks need: zoomed and with the default text size raised for
    vault.fluid-zoom, raised for vault.label-value-stack, and with a bottom
    inset on a phone for vault.bottom-safe-area. Adds what it finds to `rec`,
    the sweep's accumulator."""
    args = {
        "parts": at.parts,
        "brief": at.brief,
        "phone": rec.phone(width),
        "edge": records.EDGE,
        "snap": records.SNAP,
    }
    got = page.evaluate(rec.read, {**args, "lines": rec.lines()})
    rec.add(width, got["faults"], got["seen"])
    rec.notes.append((width, got["notes"]))
    for mode in got["unread"]:
        rec.unmet[mode] = UNREAD
    checks = rec.checks
    if "line-length" in checks:
        blocks = page.evaluate(rec.measure.LINES_JS)
        facts = page.evaluate(
            records.LINE_FACTS_JS,
            [[b["at"] for b in blocks], records.FILL_PROBE, records.EDGE],
        )
        rec.add(
            width,
            records.line_faults(blocks, facts, checks["line-length"].value),
            ["line-length"] if blocks else [],
        )
    if "fluid-zoom" in checks:
        fluid = page.evaluate(rec.fluid)
        if fluid["unread"]:
            rec.unmet["fluid-zoom"] = UNREAD
        base = {int(k): v for k, v in fluid["sizes"].items()}
        if base:
            v = checks["fluid-zoom"].value
            tall = height_at(width, at.heights)
            zoom = page_as({**device(width), "device_scale_factor": v["zoom"]})
            load(
                zoom,
                at.url,
                width,
                at.heights,
                view=(round(width / v["zoom"]), round(tall / v["zoom"])),
            )
            zoomed_px = {
                int(k): [None, px * v["zoom"]]
                for k, (_, px) in zoom.evaluate(records.SIZES_JS, list(base)).items()
            }
            sized = page_as(device(width), raised["fluid-zoom"])
            load(sized, at.url, width, at.heights)
            sized_px = {
                int(k): val
                for k, val in sized.evaluate(records.SIZES_JS, list(base)).items()
            }
            rec.add(
                width,
                records.fluid_faults(base, zoomed_px, sized_px, v, slack=GROW_SLACK),
                ["fluid-zoom"],
            )
    if "label-value" in checks and "label-value" in got["seen"]:
        sized = page_as(device(width), raised["label-value"])
        load(sized, at.url, width, at.heights)
        more = sized.evaluate(rec.read, {**args, "lines": rec.lines(("label-value",))})
        size = checks["label-value"].value["size"]
        rec.add(
            width,
            [
                {**f, "detail": f"{f['detail']}, with text at {size * 100:g}%"}
                for f in more["faults"]
            ],
        )
    if "safe-bottom" in checks and rec.phone(width):
        load(safe, at.url, width, at.heights)
        got = safe.evaluate(
            rec.inset, [checks["safe-bottom"].value["inset"], records.EDGE]
        )
        rec.add(width, got["faults"], ["safe-bottom"] if got["seen"] else [])


def records_after(browser, at, rec, page_as):
    """The record checks read once the sweep ends: across its widths
    (vault.card-media-stack, vault.logo-version), and at narrow widths the
    tab panels with script on and off (vault.tabs-narrow) and each popover
    and menu opened (vault.popover-sheet). Adds what it finds to `rec`."""
    checks = rec.checks
    widths = [w for w, _ in rec.notes]

    def narrow(under, mode):
        held = [w for w in widths if w < under]
        if not held:
            rec.unmet[mode] = f"the sweep holds no width under {under:g} px"
        return [w for w in SHOT_WIDTHS if w in held] or held[:1]

    if "card-media" in checks:
        cards = [(w, n.get("cards", [])) for w, n in rec.notes]
        if any(c for _, c in cards):
            rec.seen.add("card-media")
        for w, faults in records.card_media_faults(
            cards, checks["card-media"].value["threshold"]
        ):
            rec.add(w, faults)
    if "logo-version" in checks:
        logos = [(w, n.get("logo")) for w, n in rec.notes]
        if any(n for _, n in logos):
            rec.seen.add("logo-version")
        for w, faults in records.logo_faults(logos):
            rec.add(w, faults)
    if "tabs-narrow" in checks:
        off = browser.new_context(java_script_enabled=False, **PHONE)
        off.set_default_timeout(at.timeout)
        bare = off.new_page()
        for w in narrow(rec.phone_under, "tabs-narrow"):
            page = page_as(device(w))
            load(page, at.url, w, at.heights)
            panels = page.evaluate(records.TABS_JS, None)
            if not panels:
                continue
            rec.seen.add("tabs-narrow")
            faults = records.tab_faults(panels, True)
            ids = [p["id"] for p in panels if p["id"]]
            if ids:
                bare.set_viewport_size({"width": w, "height": height_at(w, at.heights)})
                bare.goto(at.url, wait_until="load")
                faults += records.tab_faults(bare.evaluate(records.TABS_JS, ids), False)
            rec.add(w, faults)
        off.close()
    if "popover-sheet" in checks:
        overlay = _load("drive_overlay", "drive-overlay.py")
        under = checks["popover-sheet"].value["under"]
        for w in narrow(under, "popover-sheet"):
            page = page_as(device(w))
            load(page, at.url, w, at.heights)
            faults = []
            for ov in overlay.find(page):
                if ov.kind not in ("popover", "menu") or ov.trigger is None:
                    continue
                state = overlay.open(page, ov)
                if state["open"] and ov.target:
                    rec.seen.add("popover-sheet")
                    got = page.evaluate(rec.sheet, [ov.target, records.EDGE])
                    if not got["sheet"]:
                        faults.append(
                            {
                                "kind": "popover-sheet",
                                "subject": got["label"],
                                "detail": f"opens a floating box {round(got['width'])} by {round(got['height'])} px, not a bottom or full-screen sheet, under {under:g} px",
                            }
                        )
                overlay.close(page, ov)
            rec.add(w, faults)


def run(at, when):
    widths = sweep_widths(at.step, *at.span)
    found, arts, shots, looping = [], [], [], 0
    text = {name: [] for name in at.text}
    rec = Records(at) if at.records else None
    with flow.chromium() as browser:
        pages = {}

        def page_as(options, sizes=None):
            """One page per set of context options, as touch, is_mobile and
            the scale factor are fixed per context; `sizes` sets the
            browser's default text sizes, proportional and monospace, which
            hold for every later load in that page (docs/practice/browser-testing-and-accessibility.md)."""
            key = (tuple(sorted(options.items())), sizes)
            if key not in pages:
                context = browser.new_context(**options)
                context.set_default_timeout(at.timeout)
                page = context.new_page()
                if sizes:
                    standard, fixed = sizes
                    context.new_cdp_session(page).send(
                        "Page.setFontSizes",
                        {"fontSizes": {"standard": standard, "fixed": fixed}},
                    )
                pages[key] = page
            return pages[key]

        def page_at(width):
            return page_as(device(width))

        raised = None
        defaults = (
            page_at(LOW).evaluate(DEFAULT_SIZES_JS)
            if "size" in at.text
            or (rec and {"fluid-zoom", "label-value"} & set(at.checks))
            else None
        )
        if "size" in at.text:
            factor = at.modes["size"].value
            raised = tuple(round(px * factor) for px in defaults)
        safe, record_sizes = None, {}
        if rec:
            for name, key in (("fluid-zoom", "grow"), ("label-value", "size")):
                if name in at.checks:
                    factor = at.checks[name].value[key]
                    record_sizes[name] = tuple(round(px * factor) for px in defaults)
            if "safe-bottom" in at.checks:
                context = browser.new_context(**PHONE)
                context.set_default_timeout(at.timeout)
                safe = context.new_page()
                context.new_cdp_session(safe).send(
                    "Emulation.setSafeAreaInsetsOverride",
                    {"insets": {"bottom": at.checks["safe-bottom"].value["inset"]}},
                )

        for width in widths:
            page = page_at(width)
            looping = max(looping, load(page, at.url, width, at.heights))
            base = measure(page, at.cta, at.focal)
            arts.append((width, base["arts"]))
            # Text a box hides at 100% is a carousel's next slide or a
            # truncated label, a loss only once spacing or size hides more;
            # Residual: text cut off at 100% with no way to show it is
            # reported by nothing.
            faults = [f for f in base["faults"] if "place" not in f]
            if is_phone(width):
                mobile = page_as(MOBILE)
                load(mobile, at.url, width, at.heights)
                faults = faults + viewport_faults(width, mobile.evaluate(VIEWPORT_JS))
            found.append((width, faults))
            if rec:
                read_records(
                    page,
                    at,
                    width,
                    rec,
                    page_as=page_as,
                    raised=record_sizes,
                    safe=safe,
                )
            if "spacing" in at.text:
                text["spacing"].append((width, spaced_at(page, at, width, base)))
            if "zoom" in at.text:
                got = zoomed_at(page_as, at, width, base)
                if got is not None:
                    text["zoom"].append((width, got))
            if "size" in at.text:
                text["size"].append(
                    (width, sized_at(page_as, at, width, base, raised=raised))
                )
        if rec:
            records_after(browser, at, rec, page_as)
        for width in [w for w in SHOT_WIDTHS if at.span[0] <= w <= at.span[1]]:
            page = page_at(width)
            load(page, at.url, width, at.heights)
            path = os.path.join(at.out, f"layout-{width}-{stamp(when)}.png")
            page.screenshot(path=path, full_page=True)
            shots.append(path)
    return settle_focal(found, arts, at.focal), shots, looping, text, raised, rec


def settle_focal(found, arts, focal):
    """`found` with what one width cannot tell about a --focal art: one whose
    file's size changes between widths (a srcset or image-set) leaves the
    focal box's pixels naming no one file, so its crops give way to a not
    measured finding at every width; so do the readings of an art shown at
    no width."""
    sizes = collections.defaultdict(dict)
    for width, got in arts:
        for art in got:
            sizes[art["subject"]].setdefault(tuple(art["natural"]), width)
    unmeasured = {
        subject: "loads art files of different sizes ("
        + ", ".join(f"{fw}x{fh} px at {at} px" for (fw, fh), at in seen.items())
        + "), so the focal box's pixels name no one file"
        for subject, seen in sizes.items()
        if len(seen) > 1
    }
    for selector in dict.fromkeys(f["selector"] for f in focal):
        if found and all(
            any(f["kind"] == "unshown" and f["subject"] == selector for f in faults)
            for _, faults in found
        ):
            unmeasured[selector] = "is shown at no swept width"
    added = [
        {"kind": "unmeasured", "subject": subject, "detail": detail}
        for subject, detail in unmeasured.items()
    ]
    return [
        (
            width,
            [
                f
                for f in faults
                if f["kind"] not in ("crop", "unshown")
                or f["subject"] not in unmeasured
            ]
            + added,
        )
        for width, faults in found
    ]


def gating(at):
    return at.step <= GATE_STEP and at.span == (LOW, HIGH)


def answers(at, runs, text_runs):
    """Each gate question's answer, pass, fail or, for the focal box's,
    cannot measure, or None for one not checked."""
    failed = {
        k.question for k in KINDS if any(r["kind"] == k.key for r in failing(runs))
    }
    verdicts = {q: "fail" if q in failed else "pass" for q in QUESTIONS}
    if verdicts[FOCAL_QUESTION] == "pass" and any(
        r["kind"] == "unmeasured" for r in runs
    ):
        verdicts[FOCAL_QUESTION] = "cannot measure"
    if at.cta is None:
        verdicts[CTA_QUESTION] = None
    if not at.focal:
        verdicts[FOCAL_QUESTION] = None
    spaced = text_runs.get("spacing")
    verdicts[SPACING_QUESTION] = (
        None if spaced is None else "fail" if failing(spaced, TEXT_KINDS) else "pass"
    )
    return verdicts


def failing(runs, kinds=KINDS):
    """The ranges of a kind in `kinds` that fails its question."""
    passing = {k.key for k in kinds if not k.fails}
    return [r for r in runs if r["kind"] not in passing]


def condition(mode):
    """How a --text mode changes the page, in words."""
    if mode.name == "spacing":
        v = mode.value
        return (
            f"with line height {v['line-height']:g}, spacing after paragraphs {v['after-paragraph']:g}, "
            f"letter spacing {v['letter-spacing']:g} and word spacing {v['word-spacing']:g} times the font size"
        )
    if mode.name == "zoom":
        return f"at {mode.value * 100:g}% browser zoom, on screens {LOW * mode.value:g} px wide and wider"
    return f"with the browser's default text size raised to {mode.value * 100:g}%"


def report(at, widths, runs, shots, *, text_runs, verdicts, looping, when, json_path):
    bands = ", ".join(
        f"{tall} px tall at {low}–{high} px ({name})"
        for (name, low, high), tall in zip(BANDS, at.heights, strict=True)
    )
    lines = [
        f"check-layout: {at.url}",
        f"swept {len(widths)} widths, {at.span[0]}–{at.span[1]} px every {at.step} px{f' to {STEPPED}' if at.span[0] < STEPPED < at.span[1] else ''}; the first screen is {bands}",
    ]
    if not gating(at):
        lines.append(
            f"NOT A GATING SWEEP: the craft gate needs {LOW}–{HIGH} px every {GATE_STEP} px or finer to {STEPPED}"
        )
    if looping:
        lines.append(
            f"{looping} looping animation(s) never finish, so the layout was measured mid-loop"
        )
    for question in QUESTIONS:
        if verdicts[question] is None:
            lines.append(f"{question}: not checked, no {OPTIONAL[question]} given")
            continue
        lines.append(f"{question}: {verdicts[question]}")
        lines.extend(listed([k for k in KINDS if k.question == question], runs))
        if verdicts[question] == "cannot measure":
            lines.append(
                "  judge each art not measured by eye, in the screenshots below"
            )
    if verdicts[SPACING_QUESTION] is None:
        lines.append(f"{SPACING_QUESTION}: not checked, no --text spacing given")
    for name in at.text:
        mode = at.modes[name]
        if name == "spacing":
            lines.append(f"{SPACING_QUESTION}: {verdicts[SPACING_QUESTION]}")
        else:
            lines.append(f"text at {mode.value * 100:g}%, by {mode.id}'s value:")
        lines.append(f"  {condition(mode)}, beside the page at 100%:")
        kinds = [k for k in TEXT_KINDS if name != "spacing" or k.key != "grow"]
        lines.extend("  " + line for line in listed(kinds, text_runs[name]))
        if any(r["kind"] == "reveal" for r in text_runs[name]):
            lines.append(
                f"  text hidden in a link or beside a control fails nothing here: {REVEAL_QUESTION}'s look critics judge whether it can be shown"
            )
    lines.append(f"screenshots, run at {when.isoformat(timespec='seconds')} UTC:")
    lines.extend(f"  {s}" for s in shots)
    lines.append(f"every width's findings: {json_path}")
    return "\n".join(lines)


def record_report(at, runs, verdicts):
    """--records' report lines: each record's answer, and its checks' faults
    by the ranges of widths they hold over."""
    lines = [f"records, by {at.table}'s lines:"]
    modes = {**at.checks, **{n: at.modes[n] for n in at.unmet}}
    for record, verdict in verdicts.items():
        mine = [name for name, m in modes.items() if m.id == record]
        why = [at.unmet[n] for n in mine if n in at.unmet]
        lines.append(
            f"{record}: {verdict}{f' ({why[0]})' if verdict == 'not judged' else ''}"
        )
        for r in runs:
            if r["kind"] in mine:
                lines.append(
                    f"    {span(r)}: {r['subject']} {r['detail']} (at {r['from']} px)"
                )
    return "\n".join(lines)


def listed(kinds, runs):
    """Each kind's count and its ranges, as report lines."""
    lines = []
    for kind in kinds:
        mine = [r for r in runs if r["kind"] == kind.key]
        lines.append(f"  {kind.title}: {len(mine) or 'none'}")
        for r in mine:
            lines.append(
                f"    {span(r)}: {r['subject']} {r['detail']} (at {r['from']} px)"
            )
    return lines


def parse(argv):
    p = argparse.ArgumentParser(
        prog="check-layout.py",
        description="Sweep a page from 320 to 1920 px, and at 2560, for sideways scroll, cut-off text, overlap, a phone viewport not at the phone's width or blocking zoom, a call to action off the first screen, and an art's focal box out of view.",
    )
    p.add_argument("url", help="an http(s) URL, or a local HTML file")
    p.add_argument(
        "--out",
        required=True,
        metavar="DIR",
        help="where the screenshots and layout.json go",
    )
    p.add_argument(
        "--cta",
        metavar="SELECTOR",
        help="the call to action that must sit wholly in the first screen",
    )
    p.add_argument("--step", type=int, default=GATE_STEP, metavar="PX")
    p.add_argument(
        "--widths",
        default=f"{LOW}-{HIGH}",
        metavar="LOW-HIGH",
        help=f"part of {LOW}–{HIGH} px to sweep",
    )
    p.add_argument(
        "--heights",
        default=",".join(map(str, HEIGHTS)),
        metavar="PHONE,TABLET,DESKTOP",
        help="the first screen's height in each band",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=flow.LOAD_TIMEOUT_MS,
        metavar="MS",
        help="for each load",
    )
    p.add_argument(
        "--text",
        action="append",
        default=[],
        choices=tuple(MODES),
        help="also sweep with WCAG 1.4.12's spacing, at browser zoom, or with a raised default text size",
    )
    p.add_argument(
        "--records",
        action="store_true",
        help="also answer every record the table gives a check line",
    )
    p.add_argument(
        "--parts",
        dest="parts_file",
        metavar="FILE",
        help="the building session's parts declaration, for the records that read a part",
    )
    p.add_argument(
        "--brief",
        dest="facts",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help=f"a fact from the brief: {'; '.join(f'{k}={chr(124).join(v)}' for k, v in records.BRIEF.items())}",
    )
    p.add_argument(
        "--table", default=TABLE, metavar="FILE", help="the --text and --records values"
    )
    p.add_argument(
        "--focal",
        action="append",
        default=[],
        metavar="SELECTOR=X,Y,W,H",
        help="an art's element and the focal box its brief declares, in the art file's pixels, that must stay wholly in view",
    )
    at = p.parse_args(argv)
    focal = []
    for value in at.focal:
        m = FOCAL_ARG.fullmatch(value)
        if not m or not m[1].strip() or float(m[4]) <= 0 or float(m[5]) <= 0:
            p.error(
                f"--focal wants SELECTOR=X,Y,W,H, the focal box in the art's pixels with a width and height over 0, e.g. .hero=1100,350,200,200 — got {value!r}"
            )
        focal.append(
            {"selector": m[1].strip(), "box": [float(n) for n in m.groups()[1:]]}
        )
    at.focal = focal
    at.text = list(dict.fromkeys(at.text))
    at.modes = {}
    try:
        if at.text or at.records:
            with open(at.table, encoding="utf8") as fh:
                at.modes = parse_table(fh.read())
    except OSError as exc:
        p.error(f"cannot read --table {at.table}: {exc.strerror}")
    except TableError as exc:
        p.error(f"--table {at.table}: {exc}")
    missing = [name for name in at.text if name not in at.modes]
    if missing:
        p.error(f"--table {at.table} has no {' or '.join(missing)} line")
    at.brief = {}
    for fact in at.facts:
        key, _, value = fact.partition("=")
        if value not in records.BRIEF.get(key, ()):
            p.error(
                f"--brief wants {' or '.join(f'{k}={chr(124).join(v)}' for k, v in records.BRIEF.items())}, got {fact!r}"
            )
        at.brief[key] = value
    at.parts = {}
    if at.parts_file:
        probe = _load("probe", "probe.py")
        try:
            with open(at.parts_file, encoding="utf8") as fh:
                at.parts = probe.declared_parts(fh.read())[0]
        except OSError as exc:
            p.error(f"cannot read --parts {at.parts_file}: {exc.strerror}")
        except probe.DeclarationError as exc:
            p.error(f"--parts {at.parts_file} {exc}")
    # Each record check the table gives, less those the round has not given
    # what they need, which answer not judged.
    at.checks, at.unmet = {}, {}
    if at.records:
        for name, mode in at.modes.items():
            if name in records.CHECKS:
                why = records.missing(name, at.parts, at.brief)
                if why:
                    at.unmet[name] = why
                else:
                    at.checks[name] = mode
        if "phone-width" not in at.checks:
            p.error(f"{at.table} has no phone-width line, which --records needs")
    if at.step < 1:
        p.error("--step wants 1 or more")
    try:
        at.heights = tuple(int(n) for n in at.heights.split(","))
    except ValueError:
        at.heights = ()
    if len(at.heights) != 3 or min(at.heights) < 1:
        p.error(
            f"--heights wants three heights in px, e.g. {','.join(map(str, HEIGHTS))}"
        )
    m = re.fullmatch(r"(\d+)-(\d+)", at.widths)
    at.span = (int(m[1]), int(m[2])) if m else ()
    if not at.span or not LOW <= at.span[0] <= at.span[1] <= HIGH:
        p.error(
            f"--widths wants LOW-HIGH within {LOW}-{HIGH}, e.g. 1100-1340 — got {at.widths!r}"
        )
    at.url = flow.page_url(p, at.url)
    return p, at


def main(argv):
    p, at = parse(argv)
    when = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    os.makedirs(at.out, exist_ok=True)
    # An earlier run's screenshots or report would reach the critic as this run's.
    for old in [
        *pathlib.Path(at.out).glob("layout-*-*.png"),
        pathlib.Path(at.out, "layout.json"),
    ]:
        old.unlink(missing_ok=True)
    try:
        got, code = flow.run_browser(lambda: run(at, when), at.timeout, at.url)
    except BadSelectorError as exc:
        flag, selector, message = exc.args
        p.print_usage(sys.stderr)
        print(
            f"check-layout.py: error: {flag} {selector!r} is not a selector the browser accepts: {message}",
            file=sys.stderr,
        )
        return 2
    if code:
        return code
    found, shots, looping, text, raised, rec = got
    runs = ranges(found)
    text_runs = {name: ranges(text[name], TEXT_KINDS) for name in at.text}
    verdicts = answers(at, runs, text_runs)
    record_runs, record_answers = [], {}
    if at.records:
        at.unmet.update(rec.unmet)
        swept = [(w, rec.found.get(w, [])) for w in sorted(rec.found)]
        record_runs = ranges(swept, RECORD_KINDS)
        by_mode = collections.defaultdict(list)
        for r in record_runs:
            by_mode[r["kind"]].append(r)
        named = {**at.checks, **{n: at.modes[n] for n in at.unmet}}
        record_answers = records.answers(named, by_mode, rec.seen, at.unmet)
    widths = [w for w, _ in found]
    json_path = os.path.join(at.out, "layout.json")
    with open(json_path, "w", encoding="utf8") as fh:
        json.dump(
            {
                "url": at.url,
                "run_at": when.isoformat(),
                "gating": gating(at),
                "step": at.step,
                "span": at.span,
                "looping_animations": looping,
                "heights": dict(zip([b[0] for b in BANDS], at.heights, strict=True)),
                "cta": at.cta,
                "focal": at.focal,
                "answers": verdicts,
                "ranges": runs,
                "screenshots": shots,
                "widths": [{"width": w, "faults": f} for w, f in found],
                "records": {
                    "answers": record_answers,
                    "not_judged": {at.modes[n].id: why for n, why in at.unmet.items()},
                    "ranges": record_runs,
                }
                if at.records
                else None,
                "text": {
                    name: {
                        "record": at.modes[name].id,
                        "value": at.modes[name].value,
                        "ranges": text_runs[name],
                        **({"default_sizes": raised} if name == "size" else {}),
                        "widths": [{"width": w, "faults": f} for w, f in text[name]],
                    }
                    for name in at.text
                },
            },
            fh,
            indent=1,
        )
    print(
        report(
            at,
            widths,
            runs,
            shots,
            text_runs=text_runs,
            verdicts=verdicts,
            looping=looping,
            when=when,
            json_path=json_path,
        )
    )
    if at.records:
        print(record_report(at, record_runs, record_answers))
    lost = [r for rs in text_runs.values() for r in failing(rs, TEXT_KINDS)]
    if failing(runs) or lost or record_runs:
        return 1
    return 6 if verdicts[FOCAL_QUESTION] == "cannot measure" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
