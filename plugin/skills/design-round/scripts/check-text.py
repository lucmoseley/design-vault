#!/usr/bin/env python3
"""Reads a rendered page's words, characters, case, number and date formats
against the rule records its table names.

USAGE
  python3 check-text.py <page> --out DIR [--parts FILE] [--part NAME=SELECTOR]…
        [--words FILE]… [--own-case] [--table FILE] [--timeout MS]

The page loads at phone and desktop width, as check-layout.py loads it, and
every text check runs at both. It loads again at desktop width right to
left (conditions.py's rtl) for vault.rtl-digit-order, and under each
browser locale vault.locale-numbers and vault.week-hour name. Each text's
locale is its nearest lang attribute's, else the browser's; vault.week-hour
also takes the browser's as the visitor's choice. The checks themselves are
text-checks.py's.

Text inside code, pre, kbd and samp is code: only vault.code-quotes reads it.
Text in script, style, svg and hidden elements is read by none. Alt, title,
aria-label and placeholder text, and an input button's value, are read as
text of their element; a title as a tooltip.

THE TABLE, by default check-text.table beside this script, gives each line
as `<record id> | <key> | <value>`; blank lines and lines starting with #
are skipped. Each record id is one check the script holds, and its lines
give every key that check reads: a missing key, an unknown record or key,
or a repeated key is refused before any page loads.

THE WORD LISTS, by default check-text.words beside this script, give a
`[list]` header and one entry a line.

--parts is the building session's parts declaration (design-round §1c);
--part gives one part's selector and wins. vault.offer-end-date reads
the part its table line names: a part the declaration does not name is
absent, so the record has no match; one declared with no selector is not
judged. --own-case says the project's rules file names a case other than
sentence case: vault.label-case is then not judged.

Each record id's finding is fail where any check misses under any load,
else not judged where it could not be read, else pass where it found
anything to judge, else no match. DIR/text.json holds every finding; an
earlier run's is deleted.

EXITS 0 no miss / 1 a miss / 2 the arguments, the table or the word lists are
wrong / 3 Playwright or its browser is missing / 4 the page did not render in
time / 5 the browser refused the page / 7 a call hung that would never return.
Exits 0 and 1 print on stdout; the rest print on stderr.
An exception it does not handle once loaded exits 2, its traceback on stderr.
"""

import argparse
import contextlib
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402
from crash_exit import run_main  # noqa: E402


runner = siblings.load(HERE, "runner.py")
layout = siblings.load(HERE, "check-layout.py")
probe = siblings.load(HERE, "probe.py")
conditions = siblings.load(HERE, "conditions.py")

checks = siblings.load(HERE, "text-checks.py")

TABLE = os.path.join(HERE, "check-text.table")
WORDS = os.path.join(HERE, "check-text.words")
WIDTHS = (layout.PHONE_WIDTH, layout.DESKTOP_WIDTH)
PAGE, RTL, Load = checks.PAGE, checks.RTL, checks.Load


PRELUDE = r"""
const SKIP = 'script, style, noscript, template, svg, math, textarea, select';
const CODE = 'code, pre, kbd, samp';
const CONTROL = 'button, [role=button], input[type=submit], input[type=button], input[type=reset]';
const drawn = (el) => {
  if (!el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) return false;
  const r = el.getBoundingClientRect();
  return r.width > 0 && r.height > 0;
};
const place = (el) => {
  const parts = [];
  for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
    if (e.id) { parts.unshift('#' + e.id); break; }
    if (e === document.body) { parts.unshift('body'); break; }
    const tag = e.tagName.toLowerCase();
    const same = [...e.parentElement.children].filter((c) => c.tagName === e.tagName);
    parts.unshift(same.length > 1 ? `${tag}:nth-of-type(${same.indexOf(e) + 1})` : tag);
  }
  return parts.join(' > ');
};
const langOf = (el) => (el.closest('[lang]') || {}).lang || '';
const lines = (el) => {
  const range = document.createRange();
  range.selectNodeContents(el);
  const rows = [];
  const rects = [...range.getClientRects()].filter((r) => r.width > 0 && r.height > 0);
  for (const r of rects.sort((a, b) => a.top - b.top)) {
    const mid = (r.top + r.bottom) / 2;
    if (!rows.some((row) => mid >= row.top && mid <= row.bottom)) rows.push({ top: r.top, bottom: r.bottom });
  }
  return rows.length;
};
const textNodes = function* () {
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = walk.nextNode()); ) {
    const p = n.parentElement;
    if (p && !p.closest(SKIP) && drawn(p)) yield [n, p];
  }
};
"""

READ_JS = (
    "({ fraction, feature, digits }) => {"
    + PRELUDE
    + r"""
  const isCaps = (cs) => cs.textTransform === 'uppercase'
    || ['small-caps', 'all-small-caps', 'petite-caps', 'all-petite-caps', 'unicase'].includes(cs.fontVariantCaps);
  const collapseOf = (cs) => cs.whiteSpaceCollapse
    || ({ pre: 'preserve', 'pre-wrap': 'preserve', 'break-spaces': 'break-spaces' }[cs.whiteSpace] ?? 'collapse');
  const blockOf = (el) => {
    for (let e = el; e && e !== document.body; e = e.parentElement) {
      const d = getComputedStyle(e).display;
      if (d !== 'inline' && d !== 'contents') return e;
    }
    return document.body;
  };
  const kindsOf = (el, text) => {
    const kinds = [];
    if (/^H[1-6]$/.test(el.tagName) || el.getAttribute('role') === 'heading') kinds.push('heading');
    const holds = (sel) => !!el.closest(sel)
      || [...el.querySelectorAll(sel)].some((e) => e.textContent.trim() === text);
    if (holds(CONTROL)) kinds.push('button');
    if (holds('a[href]')) kinds.push('link');
    if (el.matches('li')) kinds.push('list-item');
    if (holds('[role=menuitem], [role=menuitemradio], [role=menuitemcheckbox]')) kinds.push('menu-item');
    if (el.closest('[role=tooltip]')) kinds.push('tooltip');
    return kinds;
  };
  const run = (text, p, cs) => ({
    text, transform: cs.textTransform, caps: isCaps(cs), weight: parseFloat(cs.fontWeight),
    italic: cs.fontStyle !== 'normal', code: !!p.closest(CODE), cite: !!p.closest('cite, q'),
    plain: !!p.closest('time, a[href^="tel:"]'), link: !!p.closest('a[href]'),
  });
  const byBlock = new Map();
  const capsUnits = new Set();
  const fractions = [], rtl = [];
  const fractionRe = feature && new RegExp(fraction, 'g');
  const digitRe = digits && new RegExp(`\\p{Nd}{${digits},}`, 'gu');
  for (const [n, p] of textNodes()) {
    const block = blockOf(p);
    if (!byBlock.has(block)) byBlock.set(block, []);
    const cs = getComputedStyle(p);
    byBlock.get(block).push(run(n.data, p, cs));
    if (!n.data.trim() || p.closest(CODE)) continue;
    if (isCaps(cs) || (/\p{Lu}.*\p{Lu}/u.test(n.data) && !/\p{Ll}/u.test(n.data))) capsUnits.add(p);
    for (const m of fractionRe ? n.data.matchAll(fractionRe) : []) {
      const ruler = document.createElement('span');
      ruler.textContent = m[0];
      ruler.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;font-variant-numeric:normal';
      p.appendChild(ruler);
      const plain = ruler.getBoundingClientRect().width;
      ruler.style.fontVariantNumeric = feature;
      const set = ruler.getBoundingClientRect().width;
      ruler.remove();
      fractions.push({
        place: place(p), text: m[0], before: n.data.slice(0, m.index), numeric: cs.fontVariantNumeric,
        alone: p.textContent.trim() === m[0], drawsFeature: plain !== set,
      });
    }
    if (digitRe && cs.direction === 'rtl') {
      for (const m of n.data.matchAll(digitRe)) {
        const xs = [...m[0]].map((_, i) => {
          const r = document.createRange();
          r.setStart(n, m.index + i);
          r.setEnd(n, m.index + i + 1);
          return r.getBoundingClientRect().left;
        });
        rtl.push({ place: place(p), text: m[0], reversed: xs.some((x, i) => i && x < xs[i - 1]) });
      }
    }
  }
  const blocks = [];
  for (const [el, runs] of byBlock) {
    const text = runs.map((r) => r.text).join('');
    if (!text.trim()) continue;
    const cs = getComputedStyle(el);
    blocks.push({
      place: place(el), tag: el.tagName.toLowerCase(), kinds: kindsOf(el, text.trim()), lang: langOf(el),
      collapse: collapseOf(cs), weight: parseFloat(cs.fontWeight), italic: cs.fontStyle !== 'normal', runs,
    });
  }
  const ATTRS = [['title', 'tooltip'], ['alt', null], ['aria-label', null], ['placeholder', null], ['value', 'button']];
  for (const el of document.body.querySelectorAll('[title], img[alt], [aria-label], [placeholder], input[value]')) {
    if (el.closest(SKIP + ', ' + CODE) || !drawn(el)) continue;
    const cs = getComputedStyle(el);
    for (const [name, kind] of ATTRS) {
      if (name === 'value' && !el.matches(CONTROL)) continue;
      const v = el.getAttribute(name);
      if (!v || !v.trim()) continue;
      const r = run(v, el, cs);
      if (name !== 'value') Object.assign(r, { transform: 'none', caps: false });
      blocks.push({
        place: `${place(el)} [${name}]`, tag: el.tagName.toLowerCase(), kinds: kind ? [kind] : [], lang: langOf(el),
        collapse: 'collapse', weight: r.weight, italic: r.italic, runs: [r], attr: name,
      });
    }
  }
  const caps = [...capsUnits]
    .filter((el) => { for (let e = el.parentElement; e; e = e.parentElement) if (capsUnits.has(e)) return false; return true; })
    .map((el) => ({
      place: place(el), text: el.innerText, typed: el.textContent,
      styled: isCaps(getComputedStyle(el)), lines: lines(el),
    }));
  const calendars = [];
  const weekdays = new Map();
  const daysOf = (lang) => {
    if (!weekdays.has(lang)) {
      const names = new Map();
      for (const style of ['long', 'short']) {
        const f = new Intl.DateTimeFormat(lang || undefined, { weekday: style, timeZone: 'UTC' });
        for (let d = 1; d <= 7; d++) names.set(f.format(new Date(Date.UTC(2024, 0, d))).toLocaleLowerCase().replace(/\.$/, ''), d);
      }
      weekdays.set(lang, names);
    }
    return weekdays.get(lang);
  };
  for (const el of document.body.querySelectorAll('*')) {
    if (el.children.length < 7 || el.closest(SKIP) || !drawn(el)) continue;
    const lang = langOf(el);
    const names = daysOf(lang);
    const days = [...el.children].slice(0, 7).map((c) => names.get(c.textContent.trim().toLocaleLowerCase().replace(/\.$/, '')));
    if (days.some((d) => !d) || days.some((d, i) => i && d !== (days[i - 1] % 7) + 1)) continue;
    calendars.push({ place: place(el), lang, first: days[0] });
  }
  const info = (tag) => {
    const loc = new Intl.Locale(tag);
    const week = loc.getWeekInfo ? loc.getWeekInfo() : loc.weekInfo;
    const cycles = loc.getHourCycles ? loc.getHourCycles() : loc.hourCycles;
    const parts = new Intl.NumberFormat(loc.toString()).formatToParts(1234567.5);
    return {
      tag: loc.toString(),
      region: loc.region || null,
      firstDay: week ? week.firstDay : null,
      hourCycle: (cycles && cycles[0]) || new Intl.DateTimeFormat(loc.toString(), { hour: 'numeric' }).resolvedOptions().hourCycle || null,
      group: (parts.find((x) => x.type === 'group') || {}).value ?? null,
      decimal: (parts.find((x) => x.type === 'decimal') || {}).value ?? null,
    };
  };
  const safe = (tag) => { try { return info(tag); } catch { return null; } };
  const browser = safe(navigator.language.split('@')[0]);
  const locales = {};
  for (const lang of new Set([...blocks.map((b) => b.lang), ...calendars.map((c) => c.lang)])) {
    locales[lang] = lang ? safe(lang) : browser;
  }
  return { blocks, caps, fractions, rtl, calendars, locales, browser };
}
"""
)

FORMAT_JS = """(asks) => asks.map(([tag, digits]) => new Intl.NumberFormat(tag).format(BigInt(digits)))"""

PART_JS = (
    "(selector) => {"
    + PRELUDE
    + r"""
  return [...document.querySelectorAll(selector)].filter(drawn).map((el) => {
    const lang = langOf(el) || undefined;
    const months = [];
    for (const style of ['long', 'short']) {
      const f = new Intl.DateTimeFormat(lang, { month: style, timeZone: 'UTC' });
      for (let m = 0; m < 12; m++) months.push(f.format(new Date(Date.UTC(2024, m, 15))).replace(/\.$/, ''));
    }
    return { place: place(el), text: el.innerText, months };
  });
}
"""
)


def read_page(page, values):
    return page.evaluate(
        READ_JS,
        {
            "fraction": checks.FRACTION,
            "feature": values.get("vault.fractions", {}).get("feature"),
            "digits": int(values.get("vault.rtl-digit-order", {}).get("digits", 0)),
        },
    )


def sweep(browser, url, *, values, words, parts, nulls, timeout):
    loads = []

    def one(condition, width, **given):
        options = {
            "viewport": {
                "width": width,
                "height": layout.height_at(width, layout.HEIGHTS),
            }
        }
        with conditions.open_page(browser, url, **given, **options) as page:
            page.set_default_timeout(timeout)
            page.evaluate(layout.SETTLE_JS)
            data = read_page(page, values)
            if condition.startswith("locale="):
                asks = sorted(
                    {
                        (loc["tag"], "".join(shape[0]))
                        for _, _, _, shape, loc in checks.number_tokens(
                            Load(condition, width, data), words
                        )
                    }
                )
                data["formatted"] = (
                    dict(
                        zip(
                            asks,
                            page.evaluate(FORMAT_JS, [list(a) for a in asks]),
                            strict=True,
                        )
                    )
                    if asks
                    else {}
                )
            if (
                condition == PAGE
                and width == layout.DESKTOP_WIDTH
                and "vault.offer-end-date" in values
            ):
                data["offer"] = read_offer(
                    page, values["vault.offer-end-date"], parts, nulls
                )
            loads.append(Load(condition, width, data))

    for width in WIDTHS:
        one(PAGE, width)
    if "vault.rtl-digit-order" in values:
        one(RTL, layout.DESKTOP_WIDTH, rtl=True)
    locales = []
    for rid in ("vault.locale-numbers", "vault.week-hour"):
        for tag in values.get(rid, {}).get("locales", "").split():
            if tag not in locales:
                locales.append(tag)
    for tag in locales:
        one(f"locale={tag}", layout.DESKTOP_WIDTH, locale=tag)
    return loads


def read_offer(page, v, parts, nulls):
    name = v["part"]
    if name in nulls:
        return f"the part {name} is declared with no selector"
    if name not in parts:
        return None
    first = page.evaluate(PART_JS, parts[name])
    if not first:
        return f"the part {name}'s selector {parts[name]} selects nothing drawn"
    page.wait_for_timeout(int(v["watch"][:-2]))
    later = page.evaluate(PART_JS, parts[name])
    for x, y in zip(first, later, strict=True):
        x["later"] = y["text"]
    return first


def report(url, found):
    lines = [f"check-text: {url}"]
    for f in found:
        lines.append(f"{f['id']}: {f['answer']}")
        for m in f["misses"]:
            text = f" “{m['text']}”" if m["text"] else ""
            lines.append(f"  - {', '.join(m['under'])} {m['place']}: {m['what']}{text}")
        for m in f["unjudged"]:
            lines.append(f"  ? {m['place']} {m['what']}".replace("  ?  ", "  ? "))
    return "\n".join(lines)


def parse_args(argv):
    p = argparse.ArgumentParser(
        prog="check-text.py",
        description="Read a page's words, characters, case and number formats against the text records.",
    )
    p.add_argument("url", help="an http(s) URL, or a local HTML file")
    p.add_argument("--out", required=True, metavar="DIR", help="where text.json goes")
    p.add_argument(
        "--parts",
        dest="declaration",
        metavar="FILE",
        help=f"the building session's parts declaration, {probe.DECLARATION}",
    )
    p.add_argument(
        "--part",
        action="append",
        default=[],
        metavar="NAME=SELECTOR",
        help="a declared part's name and its CSS selector",
    )
    p.add_argument(
        "--words",
        action="append",
        default=[],
        metavar="FILE",
        help="a project's word lists, added to the vault's",
    )
    p.add_argument(
        "--own-case",
        action="store_true",
        help="the project's rules file names a case other than sentence case",
    )
    p.add_argument("--table", default=TABLE, metavar="FILE", help="the rule table")
    p.add_argument(
        "--timeout",
        type=int,
        default=runner.LOAD_TIMEOUT_MS,
        metavar="MS",
        help="for each load",
    )
    at = p.parse_args(argv)
    at.parts, at.nulls = {}, set()
    if at.declaration:
        try:
            with open(at.declaration, encoding="utf8") as fh:
                at.parts, nulls = probe.declared_parts(fh.read())
                at.nulls = set(nulls)
        except OSError as exc:
            p.error(f"cannot read --parts {at.declaration}: {exc.strerror}")
        except probe.DeclarationError as exc:
            p.error(f"--parts {at.declaration}: {exc}")
    for given in at.part:
        name, eq, selector = given.partition("=")
        if not eq or not name.strip() or not selector.strip():
            p.error(f"--part wants NAME=SELECTOR, got {given!r}")
        at.parts[name.strip()] = selector.strip()
        at.nulls.discard(name.strip())
    try:
        with open(at.table, encoding="utf8") as fh:
            at.values = checks.parse_table(fh.read())
        with open(WORDS, encoding="utf8") as fh:
            at.lists = checks.parse_words(fh.read())
        for path in at.words:
            with open(path, encoding="utf8") as fh:
                checks.parse_words(fh.read(), at.lists, path)
    except OSError as exc:
        p.error(f"cannot read {exc.filename}: {exc.strerror}")
    except (checks.TableError, checks.WordsError) as exc:
        p.error(str(exc))
    at.url = runner.page_url(p, at.url)
    return p, at


def main(argv):
    _, at = parse_args(argv)
    when = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    os.makedirs(at.out, exist_ok=True)
    json_path = os.path.join(at.out, "text.json")
    with contextlib.suppress(FileNotFoundError):
        os.unlink(json_path)

    def run():
        with runner.chromium() as browser:
            return sweep(
                browser,
                at.url,
                values=at.values,
                words=at.lists,
                parts=at.parts,
                nulls=at.nulls,
                timeout=at.timeout,
            )

    loads, code_ = runner.run_browser(run, at.timeout, at.url)
    if code_:
        return code_
    unjudged = (
        {"vault.label-case": "the project's rules file names its own case"}
        if at.own_case
        else {}
    )
    found = checks.findings(
        at.values, loads, at.lists, layout.DESKTOP_WIDTH, unjudged=unjudged
    )
    with open(json_path, "w", encoding="utf8") as fh:
        json.dump(
            {
                "url": at.url,
                "run_at": when.isoformat(),
                "parts": at.parts,
                "answers": {f["id"]: f["answer"] for f in found},
                "findings": found,
            },
            fh,
            indent=1,
            ensure_ascii=False,
        )
    print(report(at.url, found))
    return 1 if any(f["misses"] for f in found) else 0


if __name__ == "__main__":
    run_main(main)
