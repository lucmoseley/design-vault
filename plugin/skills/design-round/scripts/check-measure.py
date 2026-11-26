#!/usr/bin/env python3
"""USAGE
  python3 check-measure.py <url or file> [--min N] [--max N] [--widths W,W,…]
        [--height PX] [--wait SEL] [--timeout MS]

It reads the width breakpoints in the page's media queries, splits 320–2560 px
at them, and renders both ends of each range. --widths names the
widths instead. At each width it counts the characters on every full line of
running text, spaces included: real characters as the browser set them, never
a CSS width.
Phone widths, 320–767 px, render with a touch screen, as check-layout.py's do,
so text a page sets for `(pointer: coarse)` or `(hover: none)` is counted there
at the size a phone sets it. Where its media rules test the pointer or
hover, the touch screen's end is a breakpoint too, so 767 and 768 px are
rendered.
A paragraph's last line, a line a <br> ends and a block of one line are not
full, so only --max binds them. Headings, navigation, buttons, forms, tables,
preformatted text and hidden text, a screen reader's clipped text included, are
not running text. A line outside the range, 50–75 as the record vault.measure
sets, is printed with its block and its first words.

A stylesheet the browser will not let a page script read, from another origin,
is fetched from its address and its @media rules read; one that cannot be
fetched is named, since its breakpoints are unknown: pass its widths by hand.

EXITS 0 every line in range / 1 a line out of range (each printed) / 2 the
arguments are wrong / 3 Playwright or its browser is missing / 4 the page did
not render in time / 5 the browser refused the page / 6 no running text sets a
full line at any width, and no line runs over --max / 7 a call hung that would
never return. Exits 0, 1 and 6 are results and print on stdout; the rest
print on stderr.
"""

import argparse
import math
import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402
from fail_open import fail_open  # noqa: E402

layout = siblings.load(HERE, "check-layout.py")
flow = layout.flow
runner = siblings.load(HERE, "runner.py")

DEFAULT_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)
NARROWEST, WIDEST = layout.LOW, layout.HIGH
SHOWN = 3  # guess, #501

MEDIA_JS = r"""
() => {
  const media = [];
  const unread = [];
  const walk = (sheet) => {
    if (sheet.media && sheet.media.mediaText) media.push(sheet.media.mediaText);
    let rules;
    try { rules = sheet.cssRules; } catch (e) { unread.push(sheet.href); return; }
    const each = (list) => {
      for (const r of list) {
        if (r.media && r.media.mediaText) media.push(r.media.mediaText);
        if (r.styleSheet) walk(r.styleSheet);
        else if (r.cssRules) each(r.cssRules);
      }
    };
    each(rules);
  };
  for (const s of document.styleSheets) walk(s);
  return { media, unread };
}
"""

LINES_JS = (
    r"""
async () => {
  """
    + flow.LABEL_JS
    + r"""
  await document.fonts.ready;
  const NOT_RUNNING = 'h1, h2, h3, h4, h5, h6, [role="heading"], nav, button, label, select, textarea, input, table, pre';
  const NOT_SET = 'script, style, noscript, template, svg, math, [aria-hidden="true"]';
  const INLINE = new Set(['inline', 'contents', 'ruby']);
  const blockOf = (node) => {
    let e = node.parentElement;
    while (e && INLINE.has(getComputedStyle(e).display)) e = e.parentElement;
    return e;
  };
  const clipped = new Map();
  const isClipped = (e) => {
    if (!e || e === document.body) return false;
    if (clipped.has(e)) return clipped.get(e);
    const s = getComputedStyle(e);
    let own = /^(absolute|fixed)$/.test(s.position) && (s.clip !== 'auto' || s.clipPath !== 'none');
    if (!own && (s.overflowX !== 'visible' || s.overflowY !== 'visible')) {
      const r = e.getBoundingClientRect();
      own = r.width <= 1 || r.height <= 1;
    }
    const v = own || isClipped(e.parentElement);
    clipped.set(e, v);
    return v;
  };
  const blocks = new Map();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const el = n.nodeType === 1 ? n : n.parentElement;
    if ((n.nodeType === 1 && n.localName !== 'br') || el.closest(NOT_SET) || isClipped(el)) continue;
    const b = blockOf(n);
    if (!b || b.closest(NOT_RUNNING) || !b.checkVisibility({ visibilityProperty: true, opacityProperty: false })) continue;
    if (/^(pre|nowrap)/.test(getComputedStyle(b).whiteSpace)) continue;
    if (!blocks.has(b)) blocks.set(b, []);
    blocks.get(b).push(n);
  }
  const range = document.createRange();
  const out = [];
  const order = new Map([...document.body.querySelectorAll('*')].map((e, i) => [e, i]));
  for (const [b, nodes] of blocks) {
    const lines = [];
    let line = null;
    let prev = null;
    for (const n of nodes) {
      if (n.nodeType === 1) {
        if (line) line.ended = true;
        line = null;
        continue;
      }
      for (let i = 0; i < n.data.length; ) {
        const end = i + (n.data.codePointAt(i) > 0xffff ? 2 : 1);
        range.setStart(n, i);
        range.setEnd(n, end);
        const boxes = range.getClientRects();
        const r = boxes[boxes.length - 1];
        const ch = n.data.slice(i, end);
        i = end;
        if (!r || r.width === 0) continue;
        if (!line || r.top >= prev.bottom - 1 || (r.left < prev.left - 1 && r.top > prev.top + 1)) {
          line = { text: '', ended: false };
          lines.push(line);
        }
        line.text += /\s/.test(ch) ? ' ' : ch === '­' ? '-' : ch;
        prev = r;
      }
    }
    const set = lines.map((l, k) => ({ text: l.text.replace(/\s+/g, ' ').trim(), full: k < lines.length - 1 && !l.ended }))
      .filter((l) => l.text);
    if (set.length) out.push({ block: label(b), at: order.get(b), size: parseFloat(getComputedStyle(b).fontSize), lines: set });
  }
  return out;
}
"""
)


# A media query's em is the initial font size, whatever the page sets:
# https://www.w3.org/TR/mediaqueries-4/#units
LENGTH = r"([\d.]+)(px|r?em)\b"
NAMED = re.compile(r"(min|max)-(?:device-)?width\s*:\s*" + LENGTH)
AFTER = re.compile(r"\bwidth\s*(>=|<=|>|<)\s*" + LENGTH)
BEFORE = re.compile(LENGTH + r"\s*(>=|<=|>|<)\s*width\b")
AT_MEDIA = re.compile(r"@media\b([^{;]*)\{")
INPUT = re.compile(r"\b(?:any-)?(?:pointer|hover)\b")


def px(n, unit):
    return float(n) * (1 if unit == "px" else 16)


def range_starts(media):
    out = set()
    for text in media:
        for kind, n, unit in NAMED.findall(text):
            v = px(n, unit)
            out.add(math.ceil(v) if kind == "min" else math.floor(v) + 1)
        for op, n, unit in AFTER.findall(text):
            v = px(n, unit)
            out.add(math.ceil(v) if op in (">=", "<") else math.floor(v) + 1)
        for n, unit, op in BEFORE.findall(text):
            v = px(n, unit)
            out.add(math.ceil(v) if op in ("<=", ">") else math.floor(v) + 1)
    return out


def edges(starts):
    return sorted({s for s in starts if NARROWEST < s <= WIDEST})


def widths(starts):
    inner = edges(starts)
    lows = [NARROWEST, *inner]
    highs = [e - 1 for e in inner] + [WIDEST]
    return sorted({w for pair in zip(lows, highs, strict=True) for w in pair})


def judge(blocks, lo, hi):
    counts = [len(line["text"]) for b in blocks for line in b["lines"] if line["full"]]
    out = []
    for b in blocks:
        bad = [
            line["text"]
            for line in b["lines"]
            if len(line["text"]) > hi or (line["full"] and len(line["text"]) < lo)
        ]
        if bad:
            out.append({"block": b["block"], "size": b["size"], "bad": bad})
    return {
        "lines": len(counts),
        "blocks": sum(any(line["full"] for line in b["lines"]) for b in blocks),
        "range": (min(counts), max(counts)) if counts else None,
        "out": out,
    }


def span(lo, hi):
    return f"{lo}" if lo == hi else f"{lo}–{hi}"


def words(text, n=8):  # guess, #501
    head = " ".join(text.split(" ")[:n])
    return head if head == text else head + " …"


def report(at, breaks, results):
    lines = [
        f"check-measure: {at.url}",
        f"  range {at.min}–{at.max} characters a line, spaces included",
    ]
    if at.widths:
        lines.append(f"  widths given: {', '.join(str(w) for w in at.widths)}")
    else:
        lines.append(
            f"  breakpoints: {', '.join(f'{e}px' for e in edges(breaks['starts'])) or 'none'}"
        )
        for sheet in breaks["unread"]:
            lines.append(
                f"  UNREAD stylesheet {sheet}: its breakpoints are unknown; add its widths with --widths"
            )
    for w, r in results:
        verdict = (
            f"{len(r['out'])} block(s) out of range" if r["out"] else "all in range"
        )
        if r["range"] is None:
            lines.append(
                f"{w}px: no full line of running text"
                + (f" — {verdict}" if r["out"] else "")
            )
        else:
            lines.append(
                f"{w}px: {span(*r['range'])} characters, {r['lines']} full lines in {r['blocks']} block(s) — {verdict}"
            )
        for b in r["out"]:
            counts = sorted(len(t) for t in b["bad"])
            lines.append(
                f"  {b['block']} ({b['size']:g}px): {len(b['bad'])} line(s) at {span(counts[0], counts[-1])} characters"
            )
            for t in b["bad"][:SHOWN]:
                lines.append(f"    {len(t)}: “{words(t)}”")
            if len(b["bad"]) > SHOWN:
                lines.append(f"    and {len(b['bad']) - SHOWN} more")
    return "\n".join(lines)


def parse(argv):
    p = argparse.ArgumentParser(
        prog="check-measure.py",
        description="Count the characters on each line of a page's running text, at every breakpoint.",
    )
    p.add_argument("url", help="an http(s) URL, or a local HTML file")
    p.add_argument(
        "--min",
        type=int,
        default=50,
        metavar="N",
        help="the fewest characters a full line may hold; 50, as vault.measure sets (#270)",
    )
    p.add_argument(
        "--max",
        type=int,
        default=75,
        metavar="N",
        help="the most characters a line may hold; 75, as vault.measure sets (#270)",
    )
    p.add_argument(
        "--widths",
        metavar="W,W,…",
        help="the viewport widths in px, in place of the page's breakpoints",
    )
    p.add_argument(
        "--height",
        type=int,
        default=900,
        metavar="PX",
        help="the viewport height; the default is a guess",
    )
    p.add_argument("--wait", metavar="SELECTOR")
    p.add_argument("--timeout", type=int, default=runner.PLAY_TIMEOUT_MS, metavar="MS")
    at = p.parse_args(argv)
    if not 0 < at.min <= at.max:
        p.error(f"--min {at.min} and --max {at.max} make no range")
    if at.widths:
        try:
            at.widths = sorted({int(w) for w in at.widths.split(",")})
        except ValueError:
            p.error(f"--widths wants whole px, e.g. 390,1440 — got {at.widths!r}")
        if at.widths[0] <= 0:
            p.error("--widths wants widths above 0")
    at.url = runner.page_url(p, at.url)
    return at


def fetch(page, href):
    if not href:
        return None
    from playwright.sync_api import Error as PlaywrightError

    try:
        if href.startswith("file://"):
            return pathlib.Path(
                urllib.request.url2pathname(urllib.parse.urlparse(href).path)
            ).read_text(encoding="utf8")
        r = page.request.get(href)
        return r.text() if r.ok else None
    except (OSError, UnicodeDecodeError, PlaywrightError) as exc:
        # #86
        fail_open(exc, f"{href} is left unread")
        return None


def run(at):
    with runner.chromium() as browser:
        page_if_phone = {}

        def page_at(width):
            phone = layout.is_phone(width)
            viewport = {"width": width, "height": at.height}
            if phone not in page_if_phone:
                context = browser.new_context(
                    viewport=viewport, user_agent=DEFAULT_UA, **layout.device(width)
                )
                context.set_default_timeout(at.timeout)
                page = context.new_page()
                page.goto(at.url, wait_until="load", timeout=at.timeout)
                if at.wait:
                    page.wait_for_selector(at.wait, timeout=at.timeout)
                page_if_phone[phone] = page
            page = page_if_phone[phone]
            page.set_viewport_size(viewport)
            return page

        page = page_at(WIDEST)
        sheets = page.evaluate(MEDIA_JS)
        media, unread = sheets["media"], []
        for href in sheets["unread"]:
            text = fetch(page, href)
            if text is None:
                unread.append(href or "an inline sheet")
            else:
                media += [m.strip() for m in AT_MEDIA.findall(text)]
        breaks = {"starts": range_starts(media), "unread": unread}
        if any(INPUT.search(m) for m in media):
            breaks["starts"].add(layout.PHONE_MAX + 1)
        results = []
        for w in at.widths or widths(breaks["starts"]):
            page = page_at(w)
            page.evaluate(
                "() => new Promise((done) => requestAnimationFrame(() => requestAnimationFrame(done)))"
            )
            results.append((w, judge(page.evaluate(LINES_JS), at.min, at.max)))
        return breaks, results


def main(argv):
    at = parse(argv)
    got, code = runner.run_browser(lambda: run(at), at.timeout, at.url)
    if code:
        return code
    breaks, results = got
    print(report(at, breaks, results))
    if all(r["range"] is None and not r["out"] for _, r in results):
        print(
            "No running text sets a full line at any width, and none runs over --max: skip the Measure lens, and say so."
        )
        return 6
    return 1 if any(r["out"] for _, r in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
