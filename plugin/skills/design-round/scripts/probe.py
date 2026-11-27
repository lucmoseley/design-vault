#!/usr/bin/env python3
"""USAGE
  python3 probe.py <url or file> --table FILE --out DIR [--parts FILE]
        [--part NAME=SELECTOR]… [--step PX] [--widths LOW-HIGH]
        [--heights PHONE,TABLET,DESKTOP] [--timeout MS]

A table line is four fields split by " | ", the record id first; blank lines
and lines starting with # are skipped. Several lines may share an id.

    TYS-61 | css:.caps | style:letter-spacing | >= 0.05em

SELECTS, the elements a line reads, only those the page draws unless it
starts "all ": not hidden by display, visibility or opacity, not clipped to
nothing as visually-hidden text is, and not placed wholly before the page's
top or left edge as a parked skip link is:
  css:<selector>   a CSS selector, reaching into shadow roots
  role:<role>      an ARIA role, explicit or implicit
  part:<name>      a part the round declares, by its name: the selector the
                   building session's parts declaration gives it (--parts,
                   design-round §1c), or --part's, which wins
  fonts            the page's font faces, document.fonts
  sheet            the page's own style rules and @font-face rules, each
                   with the @media and @supports conditions it sits in
Any of them may end in filters, `where <read> <must>` each, which keep the
elements whose value meets it: css:p where lines >= 3.

READS, one value per element:
  style:<property>     the computed value, var() resolved; a custom property too.
                       style:a+b reads several, joined " / "; `of ::marker`
                       reads a pseudo-element's
  authored:<property>  what the page's own CSS sets it to on the element, as
                       written (var(--gap), clamp(…)): the winning
                       declaration, inline style included and the browser's
                       defaults not; empty where the element only inherits or
                       takes the initial value. !important in a cascade layer
                       is not ranked against other layers
  attr:<name>          an attribute, absent where unset; a number where it is one
  xheight              the font's x-height over its size, by the ex unit
  face:<descriptor>    with fonts: a FontFace descriptor by its CSS name,
                       display, size-adjust, ascent-override and the rest
  decl:<property>, media, selector  with sheet: a rule's declaration, its
                       conditions, and its selector
  text, tag, lang      the element's text, its tag name, the nearest lang
  lines, measure, hyphen-run  its line boxes: how many, the characters on its
                       median full line, the longest run of lines ending in a
                       word broken across two
  height, screens      its drawn height in px, and in screen heights
  over-image           1 where an image is painted under its centre, else 0
  ground, backdrop     the colour painted behind its text, every ancestor's
                       fill blended down to the white canvas; backdrop is its
                       parent's. ground-set is 1 where any of them is filled
  contrast             WCAG contrast of its text over its ground
  page-contrast, fill-contrast, fill-distance  its ground against the
                       body's in WCAG contrast, against its parent's in WCAG
                       contrast, and against its parent's in CIEDE2000
  edge-contrast        the higher contrast of its fill or its top border
                       against its backdrop
  webfont, synthesised 1 where its first family is a loaded web face, and
                       where that face lacks its weight or style
  pixels:chroma-share C  the share of its drawn pixels of OKLCH chroma C or more
  count                one value for the whole selection: how many it holds
  distinct <read> [except V or V…] [within parent|column|ground|css:<sel>]
                       how many different values <read> gives across the
                       selection, exactly, or in each group `within` names:
                       grouping near values, as designlang buckets shadows,
                       is the calling rule's
A read may start parent, prev, next, body or root to read that element
instead, prev and next the element siblings either side, and two
reads may be joined by per, minus or times: style:line-height per
style:font-size. Two decl: colours may be joined by on, the first's WCAG
contrast over the second; a translucent second is composited onto both black
and white, and the lower ratio kept: decl:color on decl:background-color. A
style, ground, backdrop or decl read may end "as oklch-l", "as
oklch-c", "as oklch-h", "as alpha" or "as luminance", read off the colour by
colour_space.py.

MUST, what each value must meet:
  = V, != V                 equal as text, or as numbers where V is one
  in V or V…, not in V or V…
  matches REGEX, not matches REGEX   Python's re.search
  >= N, <= N, > N, < N, between N and M
                            N in px, em (the element's font size), rem, ms, s,
                            % or no unit; computed letter- and word-spacing
                            "normal" is 0
  multiple of N             a whole number of N
  present, absent
A comparison may take a read in place of V or N: parent style:font-size, or
`all of (<SELECTS>) <read>`, which must hold against every element of that
selection but the one judged. `within N% of <read>` holds where the value is
that close to it.

A value the rule cannot compare, a length against a unitless number or
"normal" line-height against px, is not judged, and listed as such.

It loads the page afresh at check-layout.py's widths, every --step px (5)
from 320 to 1920 and once at 2560, at check-layout.py's screen heights, and
settles it as check-layout.py does: fonts loaded, entrance animations
finished. Each record id's finding is fail where any line misses at any
width, else not judged where any value could not be compared, else pass, or
no match where no line found anything. Each miss is reported as the range of
widths it holds over. DIR/probe.json holds every width's values; an earlier
run's is deleted. A partial sweep, or one with a step over 5 px, prints NOT A
GATING SWEEP and writes "gating": false.

A family script loads it by path and calls the library:

    rules = probe.parse(TABLE)
    swept, looping = probe.sweep(browser, url, rules, scheme="dark")
    answers = probe.findings(rules, swept)

or reads a page it has already driven (an overlay open, a field hovered):

    results = probe.read(page, rules, parts={"hero": ".hero"})

EXITS 0 no miss / 1 a miss (each printed) / 2 the arguments or the table are
wrong, a selector or part included / 3 Playwright or its browser is missing / 4
the page did not render in time / 5 the browser refused the page / 7 a call hung
that would never return. Exits 0 and 1 print on stdout; the rest print on
stderr.
"""

import argparse
import collections
import contextlib
import datetime
import io
import json
import os
import re
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402
from fail_open import expected  # noqa: E402


flow = siblings.load(HERE, "check-flow.py")
runner = siblings.load(HERE, "runner.py")
layout = siblings.load(HERE, "check-layout.py")
conditions = siblings.load(HERE, "conditions.py")
rule_table = siblings.load(HERE, "rule-table.py")
colour_space = siblings.load(
    HERE, os.path.join("..", "..", "design-project", "scripts", "colour_space.py")
)

SEP = " | "
SOURCES = ("css", "role", "part")
NAMED_READS = ("style", "authored", "attr", "face", "decl", "pixels")
KEYWORD_READS = (
    "count",
    "xheight",
    "text",
    "tag",
    "lang",
    "lines",
    "measure",
    "hyphen-run",
    "screens",
    "height",
    "over-image",
    "ground",
    "backdrop",
    "ground-set",
    "contrast",
    "fill-contrast",
    "fill-distance",
    "page-contrast",
    "edge-contrast",
    "webfont",
    "synthesised",
    "media",
    "selector",
)
READ_FORMS = "style:, authored:, attr:, face:, decl:, pixels: or one of " + ", ".join(
    KEYWORD_READS
)
COLOUR_READS = ("style", "ground", "backdrop", "decl")
TEXT_READS = ("authored", "face", "text", "tag", "lang", "media", "selector", "decl")
SHEET_READS = {"decl", "media", "selector"}
SCOPES = ("self", "parent", "prev", "next", "body", "root")
COMBINE = ("per", "minus", "times", "on")
WITHIN = ("parent", "column", "ground")
PIXEL_STATS = ("chroma-share",)
MUST_FORMS = "=, !=, in, not in, matches, not matches, >=, <=, >, <, between, within N% of, multiple of, present or absent"
EPS = 1e-6  # guess, #501
PLACES = 4  # guess, #501
BASE_UNIT = {"length": "px", "time": "ms", "percent": "%"}
# FontFace's attributes by their CSS descriptor names:
# https://www.w3.org/TR/css-font-loading-3/#fontface-interface
FACE_DESCRIPTORS = (
    "display",
    "status",
    "family",
    "weight",
    "style",
    "stretch",
    "unicode-range",
    "size-adjust",
    "ascent-override",
    "descent-override",
    "line-gap-override",
)
LENSES = ("oklch-l", "oklch-c", "oklch-h", "alpha", "luminance")
COMPARE = (">=", "<=", "!=", ">", "<", "=")
NUMERIC = (">=", "<=", ">", "<", "between")
# Computed "normal" letter- and word-spacing is no added space:
# https://www.w3.org/TR/css-text-3/#letter-spacing-property
NORMAL_IS_ZERO = ("letter-spacing", "word-spacing")
NUMBER = re.compile(r"(-?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?)(px|em|rem|ms|s|%)?", re.I)
UNITS = {
    "px": ("length", 1),
    "em": ("length", None),
    "rem": ("length", None),
    "ms": ("time", 1),
    "s": ("time", 1000),
    "%": ("percent", 1),
    "": ("number", 1),
}
STASH = "__vaultProbe"

Select = collections.namedtuple("Select", "source value all text where")
Read = collections.namedtuple(
    "Read", "kind name lens distinct excepts text scope pseudo op other within arg"
)
Must = collections.namedtuple("Must", "op values text ref")
Ref = collections.namedtuple("Ref", "select read text")
Rule = collections.namedtuple("Rule", "id select read must line")
Subject = collections.namedtuple("Subject", "subject value verdict why")
Result = collections.namedtuple("Result", "rule subjects")


TableError = rule_table.TableError


class DeclarationError(Exception):
    pass


class ProbeError(Exception):
    pass


def parse(text):
    rules = []
    for n, line in rule_table.lines(text):
        try:
            rules.append(_rule(line))
        except TableError as exc:
            raise TableError(f"line {n}: {exc}: {line}") from None
    if not rules:
        raise TableError("the table holds no rule")
    return rules


def _rule(line):
    fields = [f.strip() for f in line.split(SEP)]
    if len(fields) != 4 or not all(fields):
        raise TableError("a line wants ID | SELECTS | READS | MUST")
    rid, select, read, must = fields
    select, read, must = _select(select), _read(read), _must(must)
    _fits(select, read)
    if must.op in NUMERIC and not read.distinct and _textual(read):
        raise TableError(f"{must.op} compares numbers, which {read.text} never gives")
    return Rule(rid, select, read, must, line)


def _fits(select, read):
    kinds = {r.kind for r in _simple_reads(read)}
    if (select.source == "fonts") != ("face" in kinds):
        raise TableError("face: reads go with fonts, and fonts takes only face:")
    if select.source == "sheet" and not kinds <= SHEET_READS:
        raise TableError(f"sheet takes only {', '.join(sorted(SHEET_READS))}")
    if select.source != "sheet" and kinds & SHEET_READS:
        raise TableError(
            "decl:, media and selector read the sheet's rules: select sheet"
        )
    if read.op == "on" and kinds != {"decl"}:
        raise TableError(
            "on sets one decl: colour on another: decl:color on decl:background-color"
        )


def _textual(read):
    if read.op or read.lens:
        return False
    return read.kind in TEXT_READS or (read.kind == "style" and "+" in read.name)


def _select(text):
    body, *filters = text.split(" where ")
    every = body.startswith("all ")
    body = body[4:].strip() if every else body.strip()
    where = tuple(_filter(f) for f in filters)
    if body in ("fonts", "sheet"):
        if every:
            raise TableError(f"{body} is read whether drawn or not; drop all")
        return Select(body, None, True, text, where)
    source, _, value = body.partition(":")
    if source not in SOURCES or not value.strip():
        raise TableError("SELECTS wants css:, role:, part:, fonts or sheet")
    if source == "role" and not re.fullmatch(r"[a-z]+", value.strip()):
        raise TableError(f"{value.strip()!r} is not an ARIA role")
    return Select(source, value.strip(), every, text, where)


def _filter(text):
    words = text.split()
    for k in range(1, len(words)):
        try:
            read = _read(" ".join(words[:k]))
            must = _must(" ".join(words[k:]))
        except TableError as exc:
            expected(exc, "the next split is tried")
            continue
        if read.distinct or read.kind == "count":
            raise TableError("a where reads each element, not distinct or count")
        if must.ref and must.ref.select:
            raise TableError("a where compares within its element, not all of")
        return read, must
    raise TableError(f"where wants a read and a MUST: {text!r}")


def _read(text):
    body, distinct, excepts, within = text, False, (), None
    if body.startswith("distinct "):
        distinct = True
        body, _, within = body[len("distinct ") :].partition(" within ")
        within = within.strip() or None
        if within and within not in WITHIN and not within.startswith("css:"):
            raise TableError("within wants parent, column, ground or css:<selector>")
        body, _, rest = body.partition(" except ")
        excepts = tuple(v.strip() for v in rest.split(" or ")) if rest else ()
    for op in COMBINE:
        left, sep, right = body.partition(f" {op} ")
        if sep:
            first, second = _simple(left), _simple(right)
            if "face" in (first.kind, second.kind) or "count" in (
                first.kind,
                second.kind,
            ):
                raise TableError(f"{op} combines two reads of an element")
            return first._replace(
                distinct=distinct,
                excepts=excepts,
                text=text,
                op=op,
                other=second,
                within=within,
            )
    read = _simple(body)
    if read.kind == "count" and distinct:
        raise TableError("distinct wants a read of each element, not count")
    return read._replace(distinct=distinct, excepts=excepts, text=text, within=within)


def _scope_led(text):
    first, _, rest = text.partition(" ")
    return first in SCOPES and bool(rest)


def _simple(text):
    body, scope = text.strip(), "self"
    if _scope_led(body):
        scope, _, body = body.partition(" ")
    body, _, lens = body.partition(" as ")
    lens = lens.strip() or None
    body, _, pseudo = body.partition(" of ")
    pseudo = pseudo.strip() or None
    kind, colon, name = body.strip().partition(":")
    name, arg = name.strip(), None
    if not colon:
        kind, name = body.strip(), None
        if kind not in KEYWORD_READS:
            raise TableError(f"READS wants {READ_FORMS}")
    elif kind == "pixels":
        name, _, given = name.partition(" ")
        if name not in PIXEL_STATS:
            raise TableError(f"pixels: reads {', '.join(PIXEL_STATS)}")
        try:
            arg = float(given)
        except ValueError:
            raise TableError(f"pixels:{name} wants a number, e.g. 0.05") from None
    elif kind not in NAMED_READS or not name:
        raise TableError(f"READS wants {READ_FORMS}")
    if kind == "face" and name not in FACE_DESCRIPTORS:
        raise TableError(f"face: reads {', '.join(FACE_DESCRIPTORS)}")
    if lens is not None and (kind not in COLOUR_READS or lens not in LENSES):
        raise TableError(f"only {', '.join(COLOUR_READS)} take as {' / '.join(LENSES)}")
    if pseudo is not None and (
        kind != "style" or not re.fullmatch(r"::[a-z-]+", pseudo)
    ):
        raise TableError("of ::<pseudo-element> goes with a style: read")
    if scope != "self" and kind in ("authored", "count", "face", "pixels"):
        raise TableError(f"{scope} reads another element, which {kind} cannot")
    return Read(
        kind, name, lens, False, (), text.strip(), scope, pseudo, None, None, None, arg
    )


def _simple_reads(read):
    return [read, read.other] if read.op else [read]


def _must(text):
    for word in ("present", "absent"):
        if text == word:
            return Must(word, (), text, None)
    m = re.fullmatch(r"multiple of\s+(\S+)", text)
    if m:
        return Must("multiple", (_quantity(m[1]),), text, None)
    m = re.fullmatch(r"within\s+(\S+)%\s+of\s+(.+)", text)
    if m:
        try:
            share = float(m[1]) / 100
        except ValueError:
            raise TableError(f"within wants a share in %, not {m[1]!r}") from None
        return Must("within", (share,), text, _ref(m[2], required=True))
    m = re.fullmatch(r"between\s+(\S+)\s+and\s+(\S+)", text)
    if m:
        return Must("between", (_quantity(m[1]), _quantity(m[2])), text, None)
    for word in ("not in", "in"):
        if text.startswith(word + " "):
            values = tuple(v.strip() for v in text[len(word) :].split(" or "))
            return Must(word, values, text, None)
    for word in ("not matches", "matches"):
        if text.startswith(word + " "):
            pattern = text[len(word) :].strip()
            try:
                re.compile(pattern)
            except re.error as exc:
                raise TableError(
                    f"{pattern!r} is not a regular expression: {exc}"
                ) from None
            return Must(word, (pattern,), text, None)
    for op in COMPARE:
        if text.startswith(op):
            value = text[len(op) :].strip()
            if not value:
                break
            ref = _ref(value)
            if ref:
                return Must(op, (), text, ref)
            if op in NUMERIC:
                return Must(op, (_quantity(value),), text, None)
            return Must(op, (value,), text, None)
    raise TableError(f"MUST wants {MUST_FORMS}")


def _ref(text, required=False):
    if text.startswith("all of ("):
        depth = 0
        for i, ch in enumerate(text[len("all of ") :], len("all of ")):
            depth += {"(": 1, ")": -1}.get(ch, 0)
            if depth == 0:
                select = _select(text[len("all of (") : i])
                read = _read(text[i + 1 :].strip())
                _fits(select, read)
                if read.distinct or read.kind == "count":
                    raise TableError("all of reads each element, not distinct or count")
                return Ref(select, read, text)
        raise TableError("all of ( wants its closing )")
    if _scope_led(text):
        read = _read(text)
        if read.distinct or read.kind == "count":
            raise TableError("a compared read is one element's, not distinct or count")
        return Ref(None, read, text)
    if required:
        raise TableError(
            "within N% of wants a read: self, parent, prev, next, body, root or all of (…)"
        )
    return None


def _quantity(text):
    m = NUMBER.fullmatch(text)
    if not m:
        raise TableError(f"{text!r} is not a number with px, em, rem, ms, s or %")
    return float(m[1]), (m[2] or "").lower()


RGBA_JS = r"""
const rgba = (() => {
  let paint = null;
  return (v) => {
    if (!v || !CSS.supports('color', v)) return null;
    paint ??= document.createElement('canvas').getContext('2d', { willReadFrequently: true });
    // Setting fillStyle to a value the canvas cannot parse leaves it as it was:
    // https://html.spec.whatwg.org/multipage/canvas.html#dom-context-2d-fillstyle
    paint.fillStyle = '#000';
    paint.fillStyle = v;
    const onBlack = paint.fillStyle;
    paint.fillStyle = '#fff';
    paint.fillStyle = v;
    if (paint.fillStyle !== onBlack) return null;
    paint.clearRect(0, 0, 1, 1);
    paint.fillRect(0, 0, 1, 1);
    return [...paint.getImageData(0, 0, 1, 1).data];
  };
})();
"""

ELEMENTS_JS = (
    flow.LABEL_JS
    + RGBA_JS
    + r"""
(els, { reads, groups, all, stash, places }) => {
  const clipped = (el, cs, r) => {
    if (r.width <= 1 && r.height <= 1 && (cs.overflowX !== 'visible' || cs.overflowY !== 'visible')) return true;
    const rc = /^rect\((.*)\)$/.exec(cs.clip);
    if (rc && (cs.position === 'absolute' || cs.position === 'fixed')) {
      const [t, ri, b, l] = rc[1].split(/[\s,]+/).map((v, i) => (v === 'auto' ? [0, r.width, r.height, 0][i] : parseFloat(v)));
      if (b <= t || ri <= l) return true;
    }
    const inset = /^inset\(\s*([\d.]+)%/.exec(cs.clipPath);
    return !!inset && parseFloat(inset[1]) >= 50;
  };
  const drawn = (el) => {
    if (!el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) return false;
    const r = el.getBoundingClientRect();
    if (r.right + scrollX <= 0 || r.bottom + scrollY <= 0) return false;
    return !clipped(el, getComputedStyle(el), r);
  };
  const kept = all ? els : els.filter(drawn);
  if (stash) window[stash] = kept;
  const uid = (el) => {
    if (!el) return null;
    if (!el.__vaultUid) el.__vaultUid = window.__vaultUids = (window.__vaultUids || 0) + 1;
    return el.__vaultUid;
  };
  const rootSize = parseFloat(getComputedStyle(document.documentElement).fontSize);
  let ruler = null;
  const fixed = (n) => Math.round(n * 10 ** places) / 10 ** places;
  const xheight = (cs) => {
    if (!ruler) {
      ruler = document.createElement('div');
      ruler.style.cssText = 'position:absolute;visibility:hidden;height:0;padding:0;border:0;width:100ex;font-size:100px';
      document.body.append(ruler);
    }
    for (const p of ['font-family', 'font-weight', 'font-style', 'font-stretch', 'font-size-adjust', 'font-variation-settings', 'font-optical-sizing'])
      ruler.style.setProperty(p, cs.getPropertyValue(p));
    return Math.round(ruler.getBoundingClientRect().width) / 10000;
  };
  const over = (top, under) => {
    const a = top[3] / 255;
    return [0, 1, 2].map((i) => Math.round(top[i] * a + under[i] * (1 - a))).concat(255);
  };
  const layered = (el) => {
    const fills = [];
    for (let at = el; at; at = at.parentElement) {
      const c = rgba(getComputedStyle(at).backgroundColor);
      if (c && c[3] > 0) fills.push(c);
      if (c && c[3] === 255) break;
    }
    return { colour: fills.reverse().reduce((under, top) => over(top, under), [255, 255, 255, 255]), set: fills.length > 0 };
  };
  const ground = (el) => (el ? layered(el).colour : [255, 255, 255, 255]);
  const shown = (c) => `rgb(${c[0]}, ${c[1]}, ${c[2]})`;
  const IMAGE_TAGS = new Set(['IMG', 'PICTURE', 'VIDEO', 'CANVAS', 'svg']);
  const overImage = (el) => {
    const r = el.getBoundingClientRect();
    const x = r.left + r.width / 2, y = r.top + r.height / 2;
    if (x < 0 || y < 0 || x > innerWidth || y > innerHeight) {
      el.scrollIntoView({ block: 'center', inline: 'center' });
      return overImage(el);
    }
    const stack = document.elementsFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    const below = stack.slice(stack.indexOf(el) + 1).filter((u) => !u.contains(el) || u !== el);
    return below.some((u) => IMAGE_TAGS.has(u.tagName) || (!u.contains(el) && /url\(/.test(getComputedStyle(u).backgroundImage))
      || (u !== el && u.contains(el) && /url\(/.test(getComputedStyle(u).backgroundImage))) ? 1 : 0;
  };
  const lineInfo = (el) => {
    const lines = new Map();
    const breaks = new Set();
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const range = document.createRange();
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const words = node.data.matchAll(/\S+\s*/g);
      for (const w of words) {
        range.setStart(node, w.index);
        range.setEnd(node, w.index + w[0].length);
        const boxes = [...range.getClientRects()].filter((b) => b.width > 0);
        if (!boxes.length) continue;
        const tops = [...new Set(boxes.map((b) => Math.round(b.top)))];
        for (const t of tops) if (!lines.has(t)) lines.set(t, 0);
        lines.set(tops[0], lines.get(tops[0]) + w[0].length);
        for (const t of tops.slice(0, -1)) breaks.add(t);
      }
    }
    const half = parseFloat(getComputedStyle(el).fontSize) / 2;
    const merged = [];
    for (const t of [...lines.keys()].sort((a, b) => a - b)) {
      const last = merged[merged.length - 1];
      if (last && t - last.top < half) { last.chars += lines.get(t); last.broken ||= breaks.has(t); }
      else merged.push({ top: t, chars: lines.get(t), broken: breaks.has(t) });
    }
    const full = merged.length > 1 ? merged.slice(0, -1) : merged;
    const counts = full.map((l) => l.chars).sort((a, b) => a - b);
    let run = 0, best = 0;
    for (const l of merged) { run = l.broken ? run + 1 : 0; best = Math.max(best, run); }
    return { lines: merged.length, measure: counts.length ? counts[Math.floor(counts.length / 2)] : 0, run: best };
  };
  const loadedFaces = () => [...document.fonts].filter((f) => f.status === 'loaded');
  const family = (cs) => cs.fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, '');
  const covers = (range, want) => {
    const [lo, hi = lo] = String(range).split(/\s+/).map(parseFloat);
    return want >= lo && want <= hi;
  };
  const one = (el, read, cs, info) => {
    const target = { parent: el.parentElement, prev: el.previousElementSibling, next: el.nextElementSibling, body: document.body, root: document.documentElement }[read.scope] ?? (read.scope === 'self' ? el : null);
    if (!target) return { value: null };
    const tcs = target === el ? cs : getComputedStyle(target);
    const lines = () => (info.lines ??= lineInfo(target));
    switch (read.kind) {
      case 'style': {
        const s = read.pseudo ? getComputedStyle(target, read.pseudo) : tcs;
        const value = read.name.split('+').map((p) => s.getPropertyValue(p).trim()).join(' / ');
        return { value, rgba: read.lens ? rgba(value) : null };
      }
      case 'attr': return { value: target.getAttribute(read.name) };
      case 'xheight': return { value: xheight(tcs) };
      case 'text': return { value: (target.innerText ?? target.textContent ?? '').replace(/\s+/g, ' ').trim() };
      case 'tag': return { value: target.tagName.toLowerCase() };
      case 'lang': return { value: target.closest('[lang]')?.getAttribute('lang') ?? null };
      case 'lines': return { value: lines().lines };
      case 'measure': return { value: lines().measure };
      case 'hyphen-run': return { value: lines().run };
      case 'screens': return { value: fixed(target.getBoundingClientRect().height / innerHeight) };
      case 'height': return { value: `${fixed(target.getBoundingClientRect().height)}px` };
      case 'over-image': return { value: overImage(target) };
      case 'ground': { const c = ground(target); return { value: shown(c), rgba: c }; }
      case 'backdrop': { const c = ground(target.parentElement); return { value: shown(c), rgba: c }; }
      case 'ground-set': return { value: layered(target).set ? 1 : 0 };
      case 'contrast': { const g = ground(target); return { pair: [over(rgba(tcs.color) ?? [0, 0, 0, 255], g), g] }; }
      case 'fill-contrast':
      case 'fill-distance': return { pair: [ground(target), ground(target.parentElement)] };
      case 'page-contrast': return { pair: [ground(target), ground(document.body)] };
      case 'edge-contrast': {
        const back = ground(target.parentElement);
        const pairs = [[ground(target), back]];
        const edge = rgba(tcs.borderTopColor);
        if (edge && parseFloat(tcs.borderTopWidth) > 0 && tcs.borderTopStyle !== 'none') pairs.push([over(edge, back), back]);
        return { pairs };
      }
      case 'webfont': return { value: loadedFaces().some((f) => f.family.replace(/^["']|["']$/g, '') === family(tcs)) ? 1 : 0 };
      case 'synthesised': {
        if (tcs.fontSynthesisWeight === 'none' && tcs.fontSynthesisStyle === 'none') return { value: 0 };
        const faces = loadedFaces().filter((f) => f.family.replace(/^["']|["']$/g, '') === family(tcs));
        if (!faces.length) return { value: 0 };
        const italic = tcs.fontStyle !== 'normal';
        const met = faces.some((f) => covers(f.weight, parseFloat(tcs.fontWeight)) && (f.style !== 'normal') === italic);
        return { value: met ? 0 : 1 };
      }
      case 'pixels': {
        const r = target.getBoundingClientRect();
        return { rect: [r.left + scrollX, r.top + scrollY, r.width, r.height] };
      }
    }
    return { value: null };
  };
  const groupOf = (el, within) => {
    if (within === 'parent') return el.parentElement ? [uid(el.parentElement), label(el.parentElement)] : [null, '(none)'];
    if (within === 'column') {
      const cell = el.closest('td, th');
      const table = el.closest('table');
      return cell && table ? [`${uid(table)}:${cell.cellIndex}`, `${label(table)} column ${cell.cellIndex + 1}`] : [null, '(none)'];
    }
    if (within === 'ground') { const c = ground(el); return [shown(c), `ground ${shown(c)}`]; }
    const at = el.closest(within.slice(4));
    return at ? [uid(at), label(at)] : [null, '(none)'];
  };
  const rows = kept.map((el) => {
    const cs = getComputedStyle(el);
    const info = {};
    return {
      subject: label(el), uid: uid(el),
      values: reads.map((read) => one(el, read, cs, info)),
      groups: groups.map((g) => groupOf(el, g)),
      fontSize: parseFloat(cs.fontSize), rootSize,
    };
  });
  ruler?.remove();
  return rows;
}
"""
)

FONTS_JS = r"""
(names) => [...document.fonts].map((f) => ({
  subject: [f.family, f.weight, f.style].join(' '), uid: null, groups: [],
  values: names.map((name) => ({ value: f[name.replace(/-(.)/g, (_, c) => c.toUpperCase())] ?? null })),
  fontSize: 0, rootSize: 0,
}))
"""

SHEET_JS = (
    RGBA_JS
    + r"""
(reads) => {
  const out = [];
  const walk = (rules, conditions) => {
    for (const rule of rules) {
      const here = rule.conditionText ? [...conditions, rule.conditionText] : conditions;
      if (rule.style && (rule.selectorText || rule.constructor.name === 'CSSFontFaceRule')) {
        const subject = rule.selectorText ?? `@font-face ${rule.style.getPropertyValue('font-family')}`;
        out.push({
          subject: here.length ? `${subject} @ ${here.join(' and ')}` : subject, uid: null, groups: [],
          values: reads.map((r) => {
            if (r.kind === 'media') return { value: here.join(' and ') || null };
            if (r.kind === 'selector') return { value: rule.selectorText ?? null };
            const value = rule.style.getPropertyValue(r.name).trim() || null;
            return { value, rgba: rgba(value) };
          }),
          fontSize: 0, rootSize: 0,
        });
      }
      if (rule.cssRules) walk(rule.cssRules, here);
    }
  };
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch { continue; }
    walk(rules, []);
  }
  return out;
}
"""
)

SELECTOR_ERROR_JS = r"""
(s) => { try { document.querySelector(s); return null; } catch (e) { return e.message; } }
"""


def read(page, rules, parts=None):
    return [Result(rule, _judge(page, rule, parts or {})) for rule in rules]


def values(page, rule, parts=None):
    out = []
    found = _rows(page, rule.select, rule.read, rule.must, parts=parts or {})
    for row in _kept(rule.select, rule.read, rule.must, found):
        value, why = _value(rule.read, row)
        group = row["groups"][0][1] if rule.read.within else rule.select.text
        out.append((row["subject"], group, value, why))
    return out


def meet(rule, subject, value):
    if rule.must.ref:
        raise ProbeError(f"{rule.must.text!r} compares with a read on the page")
    return _meet(
        rule.must, subject, value, {}, read=None if rule.read.distinct else rule.read
    )


def _locator(page, select, parts):
    if select.source == "role":
        return page.get_by_role(select.value, include_hidden=select.all)
    selector = select.value
    if select.source == "part":
        if select.value not in parts:
            raise ProbeError(f"no part named {select.value!r} was declared")
        selector = parts[select.value]
    problem = page.evaluate(SELECTOR_ERROR_JS, selector)
    if problem:
        raise ProbeError(
            f"{selector!r} is not a selector the browser accepts: {problem}"
        )
    return page.locator(f"css={selector}")


def wanted(rule):
    return _wanted(rule.select, rule.read, rule.must)


def _wanted(select, read, must):
    reads = [*_simple_reads(read)]
    for f_read, f_must in select.where:
        reads += _simple_reads(f_read)
        if f_must.ref:
            reads += _simple_reads(f_must.ref.read)
    if must is not None and must.ref and must.ref.select is None:
        reads += _simple_reads(must.ref.read)
    return list(dict.fromkeys(_spec(r) for r in reads))


def _spec(read):
    return (read.kind, read.name, read.scope, read.pseudo, read.lens)


def _rows(page, select, read, must, *, parts):
    specs = _wanted(select, read, must)
    groups = [read.within] if read.within else []
    if select.source == "fonts":
        rows = page.evaluate(FONTS_JS, [s[1] for s in specs])
    elif select.source == "sheet":
        rows = page.evaluate(SHEET_JS, [{"kind": s[0], "name": s[1]} for s in specs])
    else:
        authored = [s for s in specs if s[0] == "authored"]
        rows = _locator(page, select, parts).evaluate_all(
            ELEMENTS_JS,
            {
                "reads": [
                    {
                        "kind": s[0],
                        "name": s[1],
                        "scope": s[2],
                        "pseudo": s[3],
                        "lens": s[4],
                    }
                    for s in specs
                ],
                "groups": groups,
                "all": select.all,
                "stash": STASH if authored else None,
                "places": PLACES,
            },
        )
        if authored:
            try:
                for spec in authored:
                    at = specs.index(spec)
                    got = _authored(page, spec[1])
                    for row, value in zip(rows, got, strict=True):
                        row["values"][at] = {"value": value}
            finally:
                page.evaluate(f"delete window.{STASH}")
        for at, spec in enumerate(specs):
            if spec[0] == "pixels":
                for row in rows:
                    row["values"][at] = {"shot": _shot(page, row["values"][at]["rect"])}
    return rows


def _kept(select, read, must, rows):
    specs = _wanted(select, read, must)
    for row in rows:
        row["by"] = dict(zip(specs, row.pop("values"), strict=True))
    for f_read, f_must in select.where:
        rows = [r for r in rows if _passes(f_read, f_must, r)]
    return rows


def _passes(read, must, row):
    value, why = _value(read, row)
    return not why and _meet(must, "", value, row, read=read).verdict == "pass"


def _shot(page, rect):
    x, y, w, h = rect
    if w < 1 or h < 1:
        return None
    png = page.screenshot(
        clip={"x": x, "y": y, "width": w, "height": h}, full_page=True
    )
    with Image.open(io.BytesIO(png)) as im:
        return np.asarray(im.convert("RGB"))


def _authored(page, name):
    devtools = page.context.new_cdp_session(page)
    try:
        devtools.send("DOM.enable")
        devtools.send("CSS.enable")
        devtools.send("DOM.getDocument", {"depth": 0})
        kept = devtools.send("Runtime.evaluate", {"expression": f"window.{STASH}"})
        items = devtools.send(
            "Runtime.getProperties",
            {"objectId": kept["result"]["objectId"], "ownProperties": True},
        )["result"]
        handles = sorted(
            (int(p["name"]), p["value"]["objectId"])
            for p in items
            if p["name"].isdigit()
        )
        values = []
        for _, handle in handles:
            node = devtools.send("DOM.requestNode", {"objectId": handle})["nodeId"]
            values.append(
                _winning(
                    devtools.send("CSS.getMatchedStylesForNode", {"nodeId": node}), name
                )
            )
        return values
    finally:
        devtools.detach()


def _winning(matched, name):
    declared = []
    for match in matched.get("matchedCSSRules", []):
        if match["rule"].get("origin") == "regular":
            declared += _declarations(match["rule"]["style"], name)
    if matched.get("inlineStyle"):
        declared += _declarations(matched["inlineStyle"], name)
    if not declared:
        return ""
    return sorted(declared, key=lambda d: d[0])[-1][1]


def _declarations(style, name):
    out, shorthand = [], None
    for p in style.get("cssProperties", []):
        if p.get("disabled") or p.get("parsedOk") is False:
            continue
        value = re.sub(r"\s*!\s*important\s*$", "", p.get("value", ""))
        if p["name"] != name:
            covers = {lp["name"] for lp in p.get("longhandProperties", [])}
            if value and (name in covers or name.startswith(p["name"] + "-")):
                shorthand = value
            continue
        if not value and shorthand:
            value = shorthand
        if value:
            out.append((bool(p.get("important")), value))
    return out


def _judge(page, rule, parts):
    rows = _rows(page, rule.select, rule.read, rule.must, parts=parts)
    refs = None
    if rule.must.ref and rule.must.ref.select:
        ref = rule.must.ref
        refs = []
        found = _rows(page, ref.select, ref.read, None, parts=parts)
        for row in _kept(ref.select, ref.read, None, found):
            value, why = _value(ref.read, row)
            if not why:
                refs.append((row["uid"], value, row))
    return judged(rule, rows, refs)


def judged(rule, rows, refs=None):
    rows = _kept(rule.select, rule.read, rule.must, rows)
    if rule.read.kind == "count":
        return [_meet(rule.must, rule.select.text, len(rows), {})]
    if rule.read.distinct:
        groups = collections.defaultdict(list)
        for row in rows:
            key, label = (
                row["groups"][0] if rule.read.within else (None, rule.select.text)
            )
            groups[(key, label)].append(row)
        out = []
        for (_, label), members in groups.items():
            values = {_value(rule.read, row)[0] for row in members}
            values -= {None, *rule.read.excepts}
            out.append(_meet(rule.must, label, len(values), {}))
        return out
    out = []
    for row in rows:
        value, why = _value(rule.read, row)
        if why:
            out.append(Subject(row["subject"], value, "unjudged", why))
        else:
            out.append(
                _meet(rule.must, row["subject"], value, row, refs=refs, read=rule.read)
            )
    return out


def _value(read, row):
    if read.op == "on":
        return _on(row["by"][_spec(read)], row["by"][_spec(read.other)])
    first, why = _one(read, row)
    if why or not read.op:
        return first, why
    second, why = _one(read.other, row)
    if why:
        return None, why
    a, b = _actual(read, first, row), _actual(read.other, second, row)
    if a is None or b is None:
        bad = first if a is None else second
        return None, f"not one number: {bad!r}"
    if read.op == "per":
        if b[0] == 0:
            return None, f"{read.other.text} is 0"
        if a[1] != b[1] and "number" not in (a[1], b[1]):
            return None, f"units differ: {a[1]} against {b[1]}"
        return round(a[0] / b[0], PLACES), None
    if read.op == "times":
        kinds = {a[1], b[1]} - {"number"}
        if len(kinds) > 1:
            return None, f"units differ: {' against '.join(sorted(kinds))}"
        n = round(a[0] * b[0], PLACES)
        return (f"{n}{BASE_UNIT[kinds.pop()]}" if kinds else n), None
    if a[1] != b[1]:
        return None, f"units differ: {a[1]} against {b[1]}"
    n = round(a[0] - b[0], PLACES)
    return (f"{n}{BASE_UNIT[a[1]]}" if a[1] != "number" else n), None


def _on(text, under):
    for got in (text, under):
        if got.get("rgba") is None:
            return None, f"not a colour: {got['value']!r}"
    worst = None
    for canvas in ((0, 0, 0), (255, 255, 255)):
        box = _over(under["rgba"], canvas)
        ratio = colour_space.contrast(_hex(_over(text["rgba"], box)), _hex(box))
        worst = ratio if worst is None else min(worst, ratio)
    return round(worst, PLACES), None


def _over(top, under):
    a = top[3] / 255
    return tuple(
        round(t * a + u * (1 - a)) for t, u in zip(top[:3], under[:3], strict=True)
    )


def _one(read, row):
    got = row["by"][_spec(read)]
    if read.kind in ("contrast", "fill-contrast", "page-contrast"):
        a, b = got["pair"]
        return round(colour_space.contrast(_hex(a), _hex(b)), PLACES), None
    if read.kind == "fill-distance":
        a, b = got["pair"]
        return round(
            colour_space.de2000(colour_space.lab(_hex(a)), colour_space.lab(_hex(b))), 4
        ), None
    if read.kind == "edge-contrast":
        return round(
            max(colour_space.contrast(_hex(a), _hex(b)) for a, b in got["pairs"]),
            PLACES,
        ), None
    if read.kind == "pixels":
        return _pixels(read, got["shot"])
    value = got["value"]
    if not read.lens:
        return value, None
    if got.get("rgba") is None:
        return None, f"not a colour: {value!r}"
    r, g, b, a = got["rgba"]
    hex_ = f"#{r:02x}{g:02x}{b:02x}"
    if read.lens == "alpha":
        return round(a / 255, PLACES), None
    if read.lens == "luminance":
        return round(colour_space.luminance(hex_), PLACES), None
    lch = colour_space.oklch(hex_)
    return round(lch[LENSES.index(read.lens)], PLACES), None


def _hex(rgba):
    return "#{:02x}{:02x}{:02x}".format(*rgba[:3])


def _pixels(read, shot):
    if shot is None:
        return None, "drawn at no size"
    colours, counts = np.unique(shot.reshape(-1, 3), axis=0, return_counts=True)
    chromatic = sum(
        int(n)
        for c, n in zip(colours, counts, strict=True)
        if colour_space.oklch(_hex(c))[1] >= read.arg
    )
    return round(chromatic / int(counts.sum()), PLACES), None


def _meet(must, subject, value, row, *, refs=None, read=None):
    def verdict(ok, why=""):
        return Subject(
            subject,
            value,
            "pass" if ok else "miss",
            "" if ok else why or f"not {must.text}",
        )

    if must.op in ("present", "absent"):
        return verdict((value is not None) == (must.op == "present"))
    if value is None:
        return verdict(False, "absent")
    if must.ref:
        if must.ref.select is None:
            other, why = _value(must.ref.read, row)
            if why:
                return Subject(subject, value, "unjudged", f"{must.ref.text}: {why}")
            wanted = [(other, row)]
        else:
            wanted = [
                (v, r) for uid, v, r in refs if uid is None or uid != row.get("uid")
            ]
        for other, at in wanted:
            got = _against(must, value, row, other, at=at, read=read)
            if got is not True:
                if isinstance(got, str):
                    return Subject(subject, value, "unjudged", got)
                return verdict(False, f"not {must.op} {other!r} ({must.ref.text})")
        return verdict(True)
    if must.op == "multiple":
        got = _actual(read, value, row)
        step = _base(must.values[0], row)
        if got is None or got[1] != step[1] or step[0] == 0:
            return Subject(subject, value, "unjudged", f"not one {step[1]}: {value!r}")
        q = got[0] / step[0]
        return verdict(abs(q - round(q)) <= EPS * max(1, abs(q)))
    if must.op in NUMERIC or (
        must.op in ("=", "!=") and _numeric(must, value, read, row)
    ):
        return _compare(must, subject, value, row, read=read, verdict=verdict)
    text = plain(value)
    if must.op in ("matches", "not matches"):
        found = re.search(must.values[0], text) is not None
        return verdict(found == (must.op == "matches"))
    if must.op in ("=", "!="):
        return verdict((text == plain(must.values[0])) == (must.op == "="))
    inside = text in {plain(v) for v in must.values}
    return verdict(inside == (must.op == "in"))


def _numeric(must, value, read, row):
    if isinstance(value, (int, float)):
        return True
    try:
        _quantity(must.values[0])
    except TableError as exc:
        expected(exc, "compared as text")
        return False
    return _actual(read, value, row) is not None


def _against(must, value, row, other, *, at, read):
    a, b = _actual(read, value, row), _actual(must.ref.read, other, at)
    if a is None or b is None:
        if must.op not in ("=", "!="):
            return f"not one number: {(value if a is None else other)!r}"
        return (plain(value) == plain(other)) == (must.op == "=")
    if a[1] != b[1]:
        return f"units differ: {a[1]} against {b[1]}"
    n, m = a[0], b[0]
    if must.op == "within":
        return abs(n - m) <= must.values[0] * abs(m) + EPS
    return _holds(must.op, n, [m])


def _holds(op, n, bounds):
    return {
        ">=": lambda: n >= bounds[0] - EPS,
        "<=": lambda: n <= bounds[0] + EPS,
        ">": lambda: n > bounds[0] + EPS,
        "<": lambda: n < bounds[0] - EPS,
        "=": lambda: abs(n - bounds[0]) <= EPS,
        "!=": lambda: abs(n - bounds[0]) > EPS,
        "between": lambda: bounds[0] - EPS <= n <= bounds[1] + EPS,
    }[op]()


def _compare(must, subject, value, row, *, read, verdict):
    got = _actual(read, value, row)
    if got is None:
        return Subject(subject, value, "unjudged", f"not one number: {value!r}")
    wanted = []
    for raw in must.values:
        if isinstance(raw, str):
            try:
                raw = _quantity(raw)
            except TableError as exc:
                expected(exc, "unjudged")
                return Subject(subject, value, "unjudged", f"{raw!r} is not a number")
        wanted.append(_base(raw, row))
    kinds = {got[1], *(w[1] for w in wanted)}
    if len(kinds) > 1:
        return Subject(
            subject,
            value,
            "unjudged",
            f"units differ: {' against '.join(sorted(kinds))}",
        )
    return verdict(_holds(must.op, got[0], [w[0] for w in wanted]))


def _actual(read, value, row):
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value), "number"
    text = value.strip()
    name = read.name if read is not None and read.kind == "style" else None
    if text == "normal" and (name in NORMAL_IS_ZERO or read is None):
        return (0.0, "length") if name in NORMAL_IS_ZERO else None
    m = NUMBER.fullmatch(text)
    if not m:
        return None
    return _base((float(m[1]), (m[2] or "").lower()), row)


def _base(quantity, row):
    n, unit = quantity
    kind, factor = UNITS[unit]
    if unit == "em":
        factor = row.get("fontSize")
    elif unit == "rem":
        factor = row.get("rootSize")
    return n * (factor or 0), kind


def plain(value):
    return re.sub(r"\s+", " ", str(value)).strip()


def sweep(
    browser,
    url,
    rules,
    *,
    widths=None,
    heights=conditions.HEIGHTS,
    parts=None,
    timeout=runner.LOAD_TIMEOUT_MS,
    **given,
):
    widths = widths or layout.sweep_widths(layout.GATE_STEP)
    out, looping = [], 0
    for width, page, loops in pages(
        browser, url, widths=widths, heights=heights, timeout=timeout, given=given
    ):
        looping = max(looping, loops)
        out.append((width, read(page, rules, parts)))
    return out, looping


def pages(browser, url, *, widths, heights, timeout, given):
    with contextlib.ExitStack() as stack:
        open_ = {}
        for width in widths:
            options = conditions.device(width)
            key = tuple(sorted(options.items()))
            if key not in open_:
                page = stack.enter_context(
                    conditions.open_page(browser, url, **given, **options)
                )
                page.set_default_timeout(timeout)
                open_[key] = page
            loops = layout.load(open_[key], url, width, heights)
            yield width, open_[key], loops


def findings(rules, swept):
    ids = list(dict.fromkeys(r.id for r in rules))
    out = {
        i: {"id": i, "answer": "no match", "misses": [], "unjudged": []} for i in ids
    }
    open_ = {}
    for i, (width, results) in enumerate(swept):
        seen = set()
        for n, result in enumerate(results):
            for s in result.subjects:
                key = (n, s.subject, s.verdict)
                if s.verdict == "pass" or key in seen:
                    continue
                seen.add(key)
                held = open_.get(key)
                if held and held["_last"] == i - 1:
                    held["to"], held["_last"] = width, i
                    continue
                held = {
                    "line": result.rule.line,
                    "read": result.rule.read.text,
                    "subject": s.subject,
                    "value": s.value,
                    "why": s.why,
                    "from": width,
                    "to": width,
                    "_last": i,
                }
                open_[key] = held
                bucket = "misses" if s.verdict == "miss" else "unjudged"
                out[result.rule.id][bucket].append(held)
    answered = {r.rule.id for _, results in swept for r in results if r.subjects}
    for f in out.values():
        for held in f["misses"] + f["unjudged"]:
            held.pop("_last", None)
        f["answer"] = rule_table.answer(
            misses=f["misses"], unjudged=f["unjudged"], judged=f["id"] in answered
        )
    return list(out.values())


def shown(value):
    if value is None:
        return "(absent)"
    if value == "":
        return "(none)"
    return str(value)


def report(at, widths, found, *, looping, json_path):
    lines = [
        f"probe: {at.url}",
        f"read {len(at.rules)} rule line(s) for {len(found)} record(s) at {len(widths)} widths, {at.span[0]}–{at.span[1]} px every {at.step} px",
    ]
    if not layout.gating(at.step, at.span):
        lines.append(
            f"NOT A GATING SWEEP: the craft gate needs {conditions.LOW}–{conditions.HIGH} px every {layout.GATE_STEP} px or finer to {layout.STEPPED}"
        )
    if looping:
        lines.append(
            f"{looping} looping animation(s) never finish, so the page was read mid-loop"
        )
    for f in found:
        lines.append(f"{f['id']}: {f['answer']}")
        for bucket, title in (("misses", "miss"), ("unjudged", "not judged")):
            for held in f[bucket]:
                lines.append(
                    f"  {title}, {layout.span(held)}: {held['subject']} {held['read']} {shown(held['value'])}: {held['why']} (at {held['from']} px)"
                )
    lines.append(f"every width's values: {json_path}")
    return "\n".join(lines)


DECLARATION = '{"declared": {<part>: <its CSS selector, or null>}}'


def declared_parts(text):
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise DeclarationError(f"is not JSON ({exc}), not {DECLARATION}") from None
    declared = data.get("declared") if isinstance(data, dict) else None
    if not isinstance(declared, dict):
        raise DeclarationError(f'has no "declared" object of part names: {DECLARATION}')
    bad = [
        n
        for n, sel in declared.items()
        if not (sel is None or (isinstance(sel, str) and sel.strip()))
    ]
    if bad:
        raise DeclarationError(
            f"declares {', '.join(bad)} with neither a CSS selector nor null: {DECLARATION}"
        )
    return (
        {n: sel.strip() for n, sel in declared.items() if sel is not None},
        {n for n, sel in declared.items() if sel is None},
    )


def part_arguments(p):
    p.add_argument(
        "--parts",
        dest="declaration",
        metavar="FILE",
        help=f"the building session's parts declaration, {DECLARATION}",
    )
    p.add_argument(
        "--part",
        action="append",
        default=[],
        metavar="NAME=SELECTOR",
        help="a declared part's name and its CSS selector, for part: lines",
    )


def part_options(p, at):
    parts, unselected = {}, set()
    if at.declaration:
        try:
            with open(at.declaration, encoding="utf8") as fh:
                parts, unselected = declared_parts(fh.read())
        except OSError as exc:
            p.error(f"cannot read --parts {at.declaration}: {exc.strerror}")
        except DeclarationError as exc:
            p.error(f"--parts {at.declaration}: {exc}")
    for given in at.part:
        name, eq, selector = given.partition("=")
        if not eq or not name.strip() or not selector.strip():
            p.error(f"--part wants NAME=SELECTOR, got {given!r}")
        parts[name.strip()] = selector.strip()
        unselected.discard(name.strip())
    return parts, unselected


def parse_args(argv):
    p = argparse.ArgumentParser(
        prog="probe.py",
        description="Read a page's DOM and computed style against a rule table, at check-layout.py's widths, one finding per record id.",
    )
    p.add_argument("--table", required=True, metavar="FILE", help="the rule table")
    page_arguments(p, "probe.json")
    p.add_argument(
        "--heights",
        default=",".join(map(str, conditions.HEIGHTS)),
        metavar="PHONE,TABLET,DESKTOP",
        help="the screen's height in each band",
    )
    at = p.parse_args(argv)
    unselected = page_options(p, at)
    heights_usage = f"--heights wants three heights in px, e.g. {','.join(map(str, conditions.HEIGHTS))}"
    try:
        at.heights = tuple(int(n) for n in at.heights.split(","))
    except ValueError:
        p.error(heights_usage)
    if len(at.heights) != 3 or min(at.heights) < 1:
        p.error(heights_usage)
    try:
        with open(at.table, encoding="utf8") as fh:
            at.rules = parse(fh.read())
    except OSError as exc:
        p.error(f"cannot read --table {at.table}: {exc.strerror}")
    except TableError as exc:
        p.error(f"--table {at.table}: {exc}")
    named = {r.select.value for r in at.rules if r.select.source == "part"}
    if named & unselected:
        p.error(
            f"--parts {at.declaration} declares {', '.join(sorted(named & unselected))} with no selector, which a part: line reads; give one with --part"
        )
    at.url = runner.page_url(p, at.url)
    return p, at


def page_arguments(p, out_file):
    p.add_argument("url", help="an http(s) URL, or a local HTML file")
    p.add_argument("--out", required=True, metavar="DIR", help=f"where {out_file} goes")
    part_arguments(p)
    p.add_argument("--step", type=int, default=layout.GATE_STEP, metavar="PX")
    p.add_argument(
        "--widths",
        default=f"{conditions.LOW}-{conditions.HIGH}",
        metavar="LOW-HIGH",
        help=f"part of {conditions.LOW}–{conditions.HIGH} px to read",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=runner.LOAD_TIMEOUT_MS,
        metavar="MS",
        help="for each load",
    )


def page_options(p, at):
    if at.step < 1:
        p.error("--step wants 1 or more")
    m = re.fullmatch(r"(\d+)-(\d+)", at.widths)
    at.span = (int(m[1]), int(m[2])) if m else ()
    if not at.span or not conditions.LOW <= at.span[0] <= at.span[1] <= conditions.HIGH:
        p.error(
            f"--widths wants LOW-HIGH within {conditions.LOW}-{conditions.HIGH}, e.g. 1100-1340 — got {at.widths!r}"
        )
    at.parts, unselected = part_options(p, at)
    return unselected


def main(argv):
    p, at = parse_args(argv)
    when = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    os.makedirs(at.out, exist_ok=True)
    json_path = os.path.join(at.out, "probe.json")
    with contextlib.suppress(FileNotFoundError):
        os.unlink(json_path)
    widths = layout.sweep_widths(at.step, *at.span)

    def run():
        with runner.chromium() as browser:
            return sweep(
                browser,
                at.url,
                at.rules,
                widths=widths,
                heights=at.heights,
                parts=at.parts,
                timeout=at.timeout,
            )

    try:
        got, code = runner.run_browser(run, at.timeout, at.url)
    except ProbeError as exc:
        p.print_usage(sys.stderr)
        print(f"probe.py: error: {exc}", file=sys.stderr)
        return 2
    if code:
        return code
    swept, looping = got
    found = findings(at.rules, swept)
    with open(json_path, "w", encoding="utf8") as fh:
        json.dump(
            {
                "url": at.url,
                "run_at": when.isoformat(),
                "gating": layout.gating(at.step, at.span),
                "step": at.step,
                "span": at.span,
                "heights": dict(
                    zip([b[0] for b in conditions.BANDS], at.heights, strict=True)
                ),
                "parts": at.parts,
                "looping_animations": looping,
                "answers": {f["id"]: f["answer"] for f in found},
                "findings": found,
                "widths": [
                    {
                        "width": w,
                        "lines": [
                            {
                                "id": r.rule.id,
                                "line": r.rule.line,
                                "subjects": [s._asdict() for s in r.subjects],
                            }
                            for r in results
                        ],
                    }
                    for w, results in swept
                ],
            },
            fh,
            indent=1,
        )
    print(report(at, widths, found, looping=looping, json_path=json_path))
    return 1 if any(f["misses"] for f in found) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
