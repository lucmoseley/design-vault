#!/usr/bin/env python3
"""Answers the rule records whose answer is a DOM fact (a count, an
attribute, an element's presence or place, a head tag), one table line or
more per record, through probe.py.

USAGE
  python3 check-dom.py <page> --out DIR [--table FILE] [--parts FILE]
        [--part NAME=SELECTOR]… [--timeout MS]

The page is a URL or a local HTML file. It is loaded afresh at phone and
desktop width, as check-markup.py loads it.

THE TABLE, by default check-dom.table beside this script, holds probe.py's
lines (its docstring gives their form) in blocks. A block runs from its
header to the next header or `end`; lines before any header run on the page
as it loads:

  when SELECTS       only at a width where SELECTS, in probe.py's form,
                     finds an element; elsewhere its lines find nothing
  under rtl          on the page loaded right to left (conditions.py)
  on missing page    on what the page's site serves for an address it does
                     not have; a local file has no site, and its lines are
                     not judged

`define $NAME = TEXT` lines name text the lines below use as $NAME.

Before any line is read, the page's DOM facts that probe.py has no read for
are written onto it as attributes, for attr: lines to read:

  data-vault-listens     on an element, and on the root for the window and
                         the document: the events it listens for, by
                         addEventListener or an on- handler, space-joined
  data-vault-paste       on an input or textarea: blocked where a paste
                         event dispatched on it is cancelled
  data-vault-value       on an input: its current value, where not empty
  data-vault-href        on a link: its address, resolved
  data-vault-name        on a button: its aria-label, else its text or value
  data-vault-field       on a single-line field of a form: next, or last on
                         the form's last
  data-vault-questions   on the root: the questions the page's forms ask, a
                         fieldset or a field outside one each, a radio or
                         checkbox group once, a search form none
  data-vault-links       on a form: the names and addresses of the links and
                         buttons it holds, " / "-joined
  data-vault-icon-name   on an icon (an outer svg, an image or a font icon
                         in a control): the words naming it, from its class,
                         data-icon, aria-label, title, use reference, image
                         address or ligature
  data-vault-mirrored    on an icon: 1 where it and its ancestors' transforms
                         draw it mirrored, else 0
  data-vault-stroke-scale on an outer svg with stroked shapes: the median
                         factor its drawing scales their stroke by, 1 for a
                         non-scaling stroke
  data-vault-ink-want    on an outer svg in a nav or tab list: 1, marking
                         it for the ink shot
  data-vault-ink         on an outer svg in a nav or tab list: the share of
                         its box its drawing covers, by its pixels' distance
                         from the box's commonest colour
  data-vault-ink-lead    on the icon of a current or selected item: its ink
                         over the median of its set's other icons'
  data-vault-side        on a button holding one icon and text: before or
                         after, where the icon sits in the reading direction
  data-vault-side-icon   on that button: its icon's data-vault-icon-name
  data-vault-loaded      on a link to an icon: 1 where the file loads as an
                         image, else 0
  data-vault-size        on that link: the image's WIDTHxHEIGHT in px
  data-vault-label       on a progress element: its name from a label,
                         aria-labelledby or aria-label, where it has one
  data-vault-counter     on an element in a pre or code block that is not
                         aria-hidden: the computed content of a ::before or
                         ::after that draws a counter
  data-vault-spaced-text on the outermost element of each run whose
                         white-space keeps spaces (pre, pre-wrap or
                         break-spaces): its text as written, each space,
                         tab and line break shown as ␠, ␉ and ␤
  data-vault-heads       on a div or span drawn as a block, holding phrasing
                         text alone, outside a heading, label, control,
                         nav or element with a role, and followed by a
                         sibling holding text: 1
  data-vault-size-ratio  on that element: its font size over its sibling's
  data-vault-next-weight on that element: its sibling's font weight
  data-vault-next-style  on that element: its sibling's font style
  data-vault-buttons     on a declared part's element: the drawn buttons it
                         holds
  data-vault-top-control on a declared part's element: 1 where its topmost
                         drawn descendant is a button, else 0
  data-vault-said        on a declared part's element: the accessible name
                         of the link or button holding it, else its own
  data-vault-link-name   on a declared part's element in or holding a link:
                         that link's accessible name
  data-vault-link-href   on that element: that link's address, resolved
  data-vault-link-site   on that element: 1 where that link's name holds the
                         site's name, from og:site_name or application-name,
                         else the title before its first separator; else 0
  data-vault-head-cols   on a declared part's table: its thead's th cells
                         with scope="col"; 0 with no thead
  data-vault-head-loose  on that table: its thead's td cells and th cells
                         without scope="col"
  data-vault-row-loose   on that table: its tbody th cells without
                         scope="row"
  data-vault-button-names on the root: every drawn button's name, " / "-joined
  data-vault-status      on the root, on the missing page: the HTTP status

--parts is the building session's parts declaration, {"declared": {<part>:
<its CSS selector, or null>}} (design-round §1c); --part gives one
part's selector and wins. A part the declaration does not name selects
nothing, so a count of it is 0; a line reading a part declared with no
selector is not judged, and goes to the look critics.

Each record id's finding is fail where any line misses in any block, else
not judged where any could not be compared, else pass, else no match. Each
miss names its block and width. DIR/dom.json holds every finding; an earlier
run's is deleted.

EXITS 0 no miss / 1 a miss (each printed) / 2 the arguments, the table or a
selector is wrong / 3 Playwright or its browser is missing / 4 a page did not
render in time / 5 the browser refused the page / 7 a call hung that would never
return. Exits 0 and 1 print on stdout; the rest print on stderr.
"""

import argparse
import collections
import contextlib
import datetime
import io
import json
import os
import re
import secrets
import sys
import urllib.parse

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402


probe = siblings.load(HERE, "probe.py")
conditions = siblings.load(HERE, "conditions.py")
rule_table = siblings.load(HERE, "rule-table.py")
flow, layout = probe.flow, probe.layout

TABLE = os.path.join(HERE, "check-dom.table")
WIDTHS = (layout.PHONE_WIDTH, layout.DESKTOP_WIDTH)
PAGE, RTL, MISSING = "page", "under rtl", "on missing page"
DEFINE = re.compile(r"define (\$[\w-]+) = (.+)")
NAME = re.compile(r"\$[\w-]+")
NOTHING = ":not(*)"

Block = collections.namedtuple("Block", "load when rules")


TableError = rule_table.TableError


def parse(text):
    blocks, names = [], {}
    load, when, pending = PAGE, None, []

    def close():
        if pending:
            try:
                rules = probe.parse("\n".join(line for _, line in pending))
            except probe.TableError as exc:
                raise TableError(f"near line {pending[0][0]}: {exc}") from None
            blocks.append(Block(load, when, rules))
        pending.clear()

    for n, line in rule_table.lines(text):
        if line.startswith("define "):
            m = DEFINE.fullmatch(line)
            if not m:
                raise TableError(f"line {n}: define wants $NAME = TEXT: {line}")
            names[m.group(1)] = _expand(n, m.group(2), names)
            continue
        line = _expand(n, line, names)
        if line in (RTL, MISSING, "end") or line.startswith("when "):
            close()
            load, when = (line if line in (RTL, MISSING) else PAGE), None
            if line.startswith("when "):
                when = _when(n, line[5:])
            continue
        pending.append((n, line))
    close()
    if not blocks:
        raise TableError("the table holds no rule")
    return blocks


def _expand(n, text, names):
    def name(m):
        if m.group(0) not in names:
            raise TableError(f"line {n}: {m.group(0)} is not defined above it")
        return names[m.group(0)]

    return NAME.sub(name, text)


def _when(n, text):
    try:
        return probe.parse(f"when | {text} | count | >= 1")[0]
    except probe.TableError as exc:
        raise TableError(f"line {n}: when wants a SELECTS: {exc}") from None


def part_names(rule):
    selects = [rule.select]
    if rule.must.ref and rule.must.ref.select:
        selects.append(rule.must.ref.select)
    return {s.value for s in selects if s.source == "part"}


LISTEN_JS = r"""
(() => {
  const heard = new WeakMap();
  const add = EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener = function (type, ...rest) {
    if (!heard.has(this)) heard.set(this, new Set());
    heard.get(this).add(String(type));
    return add.call(this, type, ...rest);
  };
  const read = (target, key) => {
    try { return target[key]; } catch (e) { return null; }
  };
  window.__vaultHeard = (target) => {
    const types = new Set(heard.get(target) || []);
    for (const key in target) {
      if (key.startsWith('on') && typeof read(target, key) === 'function') types.add(key.slice(2));
    }
    return [...types].sort().join(' ');
  };
})();
"""

STAMP_JS = r"""
({ parts, places }) => {
  const round = (x) => Math.round(x * 10 ** places) / 10 ** places;
  const CONTROLS = 'button, [role=button], input[type=button], input[type=submit]';
  const drawn = (el) => {
    if (!el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const root = document.documentElement;
  const set = (el, name, value) => el.setAttribute(`data-vault-${name}`, String(value));
  const squash = (text) => text.replace(/\s+/g, ' ').trim();
  const labelOf = (el) => {
    const by = el.getAttribute('aria-labelledby');
    if (by) return squash(by.split(/\s+/).map((id) => (document.getElementById(id) || {}).textContent || '').join(' '));
    const label = squash(el.getAttribute('aria-label') || '');
    if (label) return label;
    return el.labels ? squash([...el.labels].map((l) => l.textContent).join(' ')) : '';
  };
  const accessible = (el) => {
    const label = labelOf(el);
    if (label) return label;
    const said = [];
    const walk = (n) => {
      if (n.nodeType === Node.TEXT_NODE) return said.push(n.textContent);
      if (n.nodeType !== Node.ELEMENT_NODE || n.getAttribute('aria-hidden') === 'true') return;
      if (n.tagName === 'IMG') return said.push(n.getAttribute('alt') || '');
      if (n.tagName.toLowerCase() === 'svg') return said.push(n.getAttribute('aria-label') || (n.querySelector('title') || {}).textContent || '');
      n.childNodes.forEach(walk);
    };
    walk(el);
    return squash(said.join(' '));
  };
  const name = (el) => accessible(el) || squash(el.value || '');

  const heard = window.__vaultHeard;
  if (heard) {
    const page = [heard(window), heard(document), heard(root)].join(' ').split(' ').filter(Boolean);
    if (page.length) set(root, 'listens', [...new Set(page)].sort().join(' '));
    for (const el of document.body.querySelectorAll('*')) {
      const types = heard(el);
      if (types) set(el, 'listens', types);
    }
  }

  for (const el of document.querySelectorAll('input, textarea')) {
    const paste = new ClipboardEvent('paste', { bubbles: true, cancelable: true, clipboardData: new DataTransfer() });
    if (!el.dispatchEvent(paste)) set(el, 'paste', 'blocked');
    if (el.value) set(el, 'value', el.value);
  }
  for (const a of document.querySelectorAll('a[href]')) set(a, 'href', a.href);
  for (const c of document.querySelectorAll(CONTROLS)) set(c, 'name', name(c));

  const SINGLE = new Set(['text', 'email', 'tel', 'url', 'search', 'password', 'number']);
  const single = (el) => el.tagName === 'INPUT' && SINGLE.has(el.type) && drawn(el);
  const asking = (el) => {
    if (el.tagName === 'SELECT' || el.tagName === 'TEXTAREA') return true;
    return el.tagName === 'INPUT' && !['hidden', 'submit', 'button', 'reset', 'image'].includes(el.type);
  };
  const searchForm = (form) => {
    if (form.getAttribute('role') === 'search' || form.closest('[role=search], search')) return true;
    const fields = [...form.elements].filter((f) => asking(f) && drawn(f));
    return fields.length > 0 && fields.every((f) => f.type === 'search');
  };
  let questions = 0;
  for (const form of document.querySelectorAll('form')) {
    const fields = [...form.querySelectorAll('input, select, textarea')].filter(single);
    fields.forEach((f, i) => set(f, 'field', i === fields.length - 1 ? 'last' : 'next'));
    const links = [...form.querySelectorAll('a, button')].filter(drawn).map((a) => [name(a), a.href || ''].filter(Boolean).join(' '));
    set(form, 'links', links.join(' / '));
    if (searchForm(form)) continue;
    const groups = new Set();
    for (const f of form.querySelectorAll('fieldset, input, select, textarea')) {
      if (!drawn(f)) continue;
      const outer = f.parentElement && f.parentElement.closest('fieldset');
      if (outer && form.contains(outer)) continue;
      if (f.tagName === 'FIELDSET') { questions += 1; continue; }
      if (!asking(f)) continue;
      if ((f.type === 'radio' || f.type === 'checkbox') && f.name) {
        if (groups.has(f.name)) continue;
        groups.add(f.name);
      }
      questions += 1;
    }
  }
  set(root, 'questions', questions);

  const words = (...texts) => texts.filter(Boolean).join(' ').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  const fontIcon = (el) => el.children.length === 0 && /icon|symbol/i.test(el.className && el.className.baseVal === undefined ? el.className : '') && el.closest('a, button, [role=button], [role=tab], label, li');
  const icons = [];
  for (const el of document.querySelectorAll('svg, img, [data-icon], [class*=icon], [class*=symbol]')) {
    if (el.tagName.toLowerCase() === 'svg') {
      if (el.parentElement && el.parentElement.closest('svg')) continue;
    } else if (el.tagName === 'IMG') {
      if (!el.closest('a, button, [role=button], [role=tab]')) continue;
    } else if (!el.hasAttribute('data-icon') && !fontIcon(el)) continue;
    if (!drawn(el)) continue;
    const svg = el.tagName.toLowerCase() === 'svg';
    const use = svg ? [...el.querySelectorAll('use')].map((u) => u.getAttribute('href') || u.getAttribute('xlink:href')).join(' ') : '';
    const title = svg ? (el.querySelector('title') || {}).textContent : '';
    const cls = typeof el.className === 'string' ? el.className : el.getAttribute('class');
    const text = !svg && el.tagName !== 'IMG' ? el.textContent : '';
    set(el, 'icon-name', words(cls, el.getAttribute('data-icon'), el.getAttribute('aria-label'), title, use, el.getAttribute('src'), el.getAttribute('alt'), text));
    let m = new DOMMatrix(), flipped = false;
    for (let at = el; at && at !== root; at = at.parentElement) {
      const cs = getComputedStyle(at);
      if (cs.transform && cs.transform !== 'none') m = new DOMMatrix(cs.transform).multiply(m);
      if (cs.scale && cs.scale !== 'none') {
        const [sx, sy = sx] = cs.scale.split(/\s+/).map(Number);
        if (sx * sy < 0) flipped = !flipped;
      }
    }
    if (m.a * m.d - m.b * m.c < 0) flipped = !flipped;
    set(el, 'mirrored', flipped ? 1 : 0);
    if (svg) {
      const scales = [];
      for (const shape of el.querySelectorAll('path, circle, rect, line, polyline, polygon, ellipse, use')) {
        const cs = getComputedStyle(shape);
        if (cs.stroke === 'none' || parseFloat(cs.strokeWidth) === 0 || parseFloat(cs.strokeOpacity) === 0) continue;
        const ctm = shape.getCTM && shape.getCTM();
        scales.push(cs.vectorEffect === 'non-scaling-stroke' || !ctm ? 1 : Math.sqrt(Math.abs(ctm.a * ctm.d - ctm.b * ctm.c)));
      }
      if (scales.length) {
        scales.sort((x, y) => x - y);
        set(el, 'stroke-scale', round(scales[Math.floor(scales.length / 2)]));
      }
      if (el.closest('nav, [role=navigation], [role=tablist]')) set(el, 'ink-want', 1);
    }
    icons.push(el);
  }
  for (const button of document.querySelectorAll(CONTROLS)) {
    if (!drawn(button)) continue;
    const held = icons.filter((i) => button.contains(i) && i !== button);
    if (held.length !== 1) continue;
    const icon = held[0];
    const range = document.createRange();
    const boxes = [];
    const walk = document.createTreeWalker(button, NodeFilter.SHOW_TEXT);
    for (let t = walk.nextNode(); t; t = walk.nextNode()) {
      if (!t.textContent.trim() || icon.contains(t)) continue;
      range.selectNodeContents(t);
      boxes.push(...range.getClientRects());
    }
    if (!boxes.length) continue;
    const textX = boxes.reduce((s, b) => s + b.left + b.width / 2, 0) / boxes.length;
    const r = icon.getBoundingClientRect();
    const left = r.left + r.width / 2 < textX;
    const rtl = getComputedStyle(button).direction === 'rtl';
    set(button, 'side', left !== rtl ? 'before' : 'after');
    set(button, 'side-icon', icon.getAttribute('data-vault-icon-name'));
  }

  for (const p of document.querySelectorAll('progress')) {
    const label = labelOf(p);
    if (label) set(p, 'label', label);
  }
  for (const el of document.querySelectorAll('pre, pre *, code, code *')) {
    if (el.closest('[aria-hidden=true]')) continue;
    for (const pseudo of ['::before', '::after']) {
      const content = getComputedStyle(el, pseudo).content;
      if (/counter\(/.test(content)) set(el, 'counter', content);
    }
  }

  const KEEPS = new Set(['pre', 'pre-wrap', 'break-spaces']);
  const shown = { ' ': '\u2420', '\t': '\u2409', '\n': '\u2424' };
  for (const el of document.body.querySelectorAll('*')) {
    if (!KEEPS.has(getComputedStyle(el).whiteSpace)) continue;
    const outer = el.parentElement && KEEPS.has(getComputedStyle(el.parentElement).whiteSpace);
    if (!outer && el.textContent.trim()) set(el, 'spaced-text', el.textContent.replace(/[ \t\n]/g, (c) => shown[c]));
  }

  const PHRASING = 'br, b, strong, i, em, span, a, small, sup, sub, abbr, cite, q, mark';
  const HOLDERS = 'h1, h2, h3, h4, h5, h6, [role], label, legend, caption, summary, th, dt, button, a, nav, pre, code';
  for (const el of document.body.querySelectorAll('div, span')) {
    if (el.closest(HOLDERS) || !drawn(el) || !/block|flex|grid/.test(getComputedStyle(el).display)) continue;
    if (!el.textContent.trim() || [...el.querySelectorAll('*')].some((d) => !d.matches(PHRASING))) continue;
    const next = el.nextElementSibling;
    if (!next || !drawn(next) || !next.textContent.trim()) continue;
    const own = getComputedStyle(el), after = getComputedStyle(next);
    set(el, 'heads', 1);
    set(el, 'size-ratio', round(parseFloat(own.fontSize) / parseFloat(after.fontSize)));
    set(el, 'next-weight', after.fontWeight);
    set(el, 'next-style', after.fontStyle);
  }

  const meta = document.querySelector('meta[property="og:site_name" i], meta[name=application-name i]');
  const site = squash((meta && meta.content) || document.title.split(/\s+[|\u2013\u2014-]\s+|:\s/)[0] || '');
  const controls = (el) => [...el.querySelectorAll(CONTROLS)].filter(drawn);
  for (const selector of parts) {
    for (const part of document.querySelectorAll(selector)) {
      set(part, 'buttons', controls(part).length);
      let top = null;
      for (const d of part.querySelectorAll('*')) {
        if (!drawn(d) || d.children.length && !d.matches('button, [role=button]')) continue;
        const y = d.getBoundingClientRect().top;
        if (!top || y < top.y) top = { el: d, y };
      }
      set(part, 'top-control', top && top.el.closest('button, [role=button]') && part.contains(top.el.closest('button, [role=button]')) ? 1 : 0);
      set(part, 'said', accessible(part.closest('a[href], button, [role=button]') || part));
      const link = part.closest('a[href]') || part.querySelector('a[href]');
      if (link) {
        const said = accessible(link);
        set(part, 'link-name', said);
        set(part, 'link-href', link.href);
        set(part, 'link-site', site && said.toLowerCase().includes(site.toLowerCase()) ? 1 : 0);
      }
      if (part.tagName === 'TABLE') {
        const head = part.tHead;
        set(part, 'head-cols', head ? head.querySelectorAll('th[scope=col i]').length : 0);
        set(part, 'head-loose', head ? head.querySelectorAll('td, th:not([scope=col i])').length : 0);
        set(part, 'row-loose', [...part.tBodies].reduce((n, b) => n + b.querySelectorAll('th:not([scope=row i])').length, 0));
      }
    }
  }
  set(root, 'button-names', controls(document.body).map(name).join(' / '));
}
"""

ICON_FILES_JS = r"""
async () => {
  const links = [...document.querySelectorAll('link[rel~=icon i], link[rel~=apple-touch-icon i]')];
  await Promise.all(links.map((link) => new Promise((done) => {
    const img = new Image();
    img.onload = () => { link.setAttribute('data-vault-loaded', '1'); link.setAttribute('data-vault-size', `${img.naturalWidth}x${img.naturalHeight}`); done(); };
    img.onerror = () => { link.setAttribute('data-vault-loaded', '0'); done(); };
    img.src = link.href;
  })));
}
"""

INK_LEAD_JS = r"""
(places) => {
  const round = (x) => Math.round(x * 10 ** places) / 10 ** places;
  const current = '[aria-current]:not([aria-current=false i]), [role=tab][aria-selected=true i]';
  for (const icon of document.querySelectorAll('[data-vault-ink]')) {
    const item = icon.closest(current);
    const set = item && item.closest('nav, [role=navigation], [role=tablist]');
    if (!set) continue;
    const others = [...set.querySelectorAll('[data-vault-ink]')]
      .filter((o) => !o.closest(current))
      .map((o) => parseFloat(o.getAttribute('data-vault-ink')))
      .sort((x, y) => x - y);
    if (!others.length) continue;
    const mid = others.length % 2 ? others[(others.length - 1) / 2] : (others[others.length / 2 - 1] + others[others.length / 2]) / 2;
    if (mid > 0) icon.setAttribute('data-vault-ink-lead', round(parseFloat(icon.getAttribute('data-vault-ink')) / mid));
  }
}
"""

STATUS_JS = "() => performance.getEntriesByType('navigation')[0]?.responseStatus ?? 0"


def stamp(page, parts):
    page.evaluate(STAMP_JS, {"parts": list(parts.values()), "places": probe.PLACES})
    page.evaluate(ICON_FILES_JS)
    shots = page.locator("[data-vault-ink-want]")
    for i in range(shots.count()):
        icon = shots.nth(i)
        icon.evaluate(
            "(el, ink) => el.setAttribute('data-vault-ink', ink)",
            ink(icon.screenshot(animations="disabled")),
        )
    page.evaluate(INK_LEAD_JS, probe.PLACES)


def ink(png):
    rgb = np.asarray(Image.open(io.BytesIO(png)).convert("RGB"), dtype=float)
    flat = rgb.reshape(-1, 3)
    colours, counts = np.unique(flat, axis=0, return_counts=True)
    distance = np.linalg.norm(flat - colours[counts.argmax()], axis=1)
    top = distance.max()
    return round(float(distance.mean() / top), probe.PLACES) if top else 0


def missing_url(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ("http", "https"):
        return None
    return urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, f"/vault-missing-{secrets.token_hex(8)}", "", "")
    )


def run(browser, url, blocks, *, parts, unset, timeout):
    named = {n for b in blocks for r in _rules(b) for n in part_names(r)}
    given = {**dict.fromkeys(named, NOTHING), **parts}
    loads = {PAGE: url, RTL: url, MISSING: missing_url(url)}
    read = collections.defaultdict(dict)
    for load in dict.fromkeys(b.load for b in blocks):
        target = loads[load]
        if target is None:
            continue
        with conditions.open_page(
            browser, target, rtl=load == RTL, init_scripts=(LISTEN_JS,)
        ) as page:
            page.set_default_timeout(timeout)
            for width in WIDTHS:
                layout.load(page, target, width, layout.HEIGHTS)
                stamp(page, parts)
                if load == MISSING:
                    page.evaluate(
                        "(s) => document.documentElement.setAttribute('data-vault-status', s)",
                        page.evaluate(STATUS_JS),
                    )
                for i, block in enumerate(blocks):
                    if block.load == load:
                        read[width][i] = _block(page, block, given, unset)
    swept = []
    for width in WIDTHS:
        results = []
        for i, block in enumerate(blocks):
            got = read[width].get(i)
            if got is None:
                got = [
                    probe.Result(
                        r,
                        [
                            _unjudged(
                                r,
                                "a local file has no site to ask for a missing address",
                            )
                        ],
                    )
                    for r in block.rules
                ]
            results += [
                probe.Result(block_line(block, r.rule), r.subjects) for r in got
            ]
        swept.append((width, results))
    return swept


def _rules(block):
    return [block.when, *block.rules] if block.when else block.rules


def _block(page, block, parts, unset):
    empty = block.when and part_names(block.when) & unset
    if empty:
        return [probe.Result(r, [_no_selector(r, empty)]) for r in block.rules]
    if block.when is not None:
        (held,) = probe.read(page, [block.when], parts)[0].subjects
        if held.verdict != "pass":
            return [probe.Result(r, []) for r in block.rules]
    out = []
    for rule in block.rules:
        empty = part_names(rule) & unset
        if empty:
            out.append(probe.Result(rule, [_no_selector(rule, empty)]))
        else:
            out.extend(probe.read(page, [rule], parts))
    return out


def _no_selector(rule, parts):
    return _unjudged(
        rule, f"the declaration gives {', '.join(sorted(parts))} no selector"
    )


def _unjudged(rule, why):
    return probe.Subject(rule.select.text, None, "unjudged", why)


def block_line(block, rule):
    where = (
        block.load
        if block.when is None
        else f"{block.load}, when {block.when.select.text}"
    )
    return rule._replace(line=f"[{where}] {rule.line}")


def report(url, found):
    lines = [f"check-dom: {url}"]
    for f in found:
        lines.append(f"{f['id']}: {f['answer']}")
        for bucket, title in (("misses", "miss"), ("unjudged", "not judged")):
            for held in f[bucket]:
                lines.append(
                    f"  {title}, {_widths(held)}: {held['line']}: {held['subject']} {probe.shown(held['value'])}: {held['why']}"
                )
    return "\n".join(lines)


def _widths(held):
    if held["from"] == held["to"]:
        return f"{held['from']} px"
    return " and ".join(str(w) for w in WIDTHS) + " px"


def parse_args(argv):
    p = argparse.ArgumentParser(
        prog="check-dom.py",
        description="Answer the DOM records in check-dom.table: counts, attributes, presence and head tags.",
    )
    p.add_argument("url", help="an http(s) URL, or a local HTML file")
    p.add_argument("--out", required=True, metavar="DIR", help="where dom.json goes")
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
        help="a declared part's name and its CSS selector, for part: lines",
    )
    p.add_argument("--table", default=TABLE, metavar="FILE", help="the rule table")
    p.add_argument(
        "--timeout",
        type=int,
        default=flow.LOAD_TIMEOUT_MS,
        metavar="MS",
        help="for each load",
    )
    at = p.parse_args(argv)
    at.parts, at.unset = {}, set()
    if at.declaration:
        try:
            with open(at.declaration, encoding="utf8") as fh:
                at.parts, at.unset = probe.declared_parts(fh.read())
        except OSError as exc:
            p.error(f"cannot read --parts {at.declaration}: {exc.strerror}")
        except probe.DeclarationError as exc:
            p.error(f"--parts {at.declaration}: {exc}")
    for given in at.part:
        name, eq, selector = given.partition("=")
        if not eq or not name.strip() or not selector.strip():
            p.error(f"--part wants NAME=SELECTOR, got {given!r}")
        at.parts[name.strip()] = selector.strip()
        at.unset.discard(name.strip())
    try:
        with open(at.table, encoding="utf8") as fh:
            at.blocks = parse(fh.read())
    except OSError as exc:
        p.error(f"cannot read --table {at.table}: {exc.strerror}")
    except TableError as exc:
        p.error(f"--table {at.table}: {exc}")
    at.url = flow.page_url(p, at.url)
    return p, at


def main(argv):
    p, at = parse_args(argv)
    when = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    os.makedirs(at.out, exist_ok=True)
    json_path = os.path.join(at.out, "dom.json")
    with contextlib.suppress(FileNotFoundError):
        os.unlink(json_path)

    def go():
        with flow.chromium() as browser:
            return run(
                browser,
                at.url,
                at.blocks,
                parts=at.parts,
                unset=at.unset,
                timeout=at.timeout,
            )

    try:
        swept, code = flow.run_browser(go, at.timeout, at.url)
    except probe.ProbeError as exc:
        p.print_usage(sys.stderr)
        print(f"check-dom.py: error: --table: {exc}", file=sys.stderr)
        return 2
    if code:
        return code
    rules = [r for _, results in swept[:1] for r in (x.rule for x in results)]
    found = probe.findings(rules, swept)
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
            indent=2,
        )
        fh.write("\n")
    print(report(at.url, found))
    print(f"every finding: {json_path}")
    return 1 if any(f["answer"] == "fail" for f in found) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
