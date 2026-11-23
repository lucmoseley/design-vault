"""layout-records.py — the record checks check-layout.py --records runs over
its width sweep (#311): what each table line reads on the page at one width,
and how the sweep's widths give each record one answer.

It does no I/O. check-layout.py loads it by path, runs READ_JS on
the loaded page at each width of its sweep and the other scripts here on loads
of its own, and passes what they find to the functions below. The checks and
the value each takes are in CHECKS; each table line names its record, its
check and the value from that record:

    vault.line-length | line-length | body 50-75, columns 40-50, large 75, short 80

Each record's answer is fail where any of its checks found a fault at any
width, else not judged where a check needs a part or a brief fact the round
did not give, else pass where a check found something the record applies to,
else no match.
"""

import collections
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "rule_table", os.path.join(HERE, "rule-table.py")
)
rule_table = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rule_table)

NUMBER = r"(\d+(?:\.\d+)?)"
Check = collections.namedtuple("Check", "pattern parse needs")


def _none(_m):
    return None


def _numbers(*keys):
    return lambda m: dict(zip(keys, (float(g) for g in m.groups()), strict=True))


# Each check: the shape of its table value, what it reads from the match, and
# what the round must give before it can judge: a part (part:<name>) or a
# brief fact (brief:<key>).
CHECKS = {
    "fold": Check(r"none", _none, ()),
    "nav-place": Check(rf"under {NUMBER}", _numbers("under"), ("brief:kind",)),
    "nav-wide": Check(rf"from {NUMBER}", _numbers("from"), ()),
    "visible-nav": Check(rf"at most {NUMBER} links", _numbers("most"), ()),
    "rtl-order": Check(r"none", _none, ()),
    "fluid-zoom": Check(rf"zoom {NUMBER}, grow {NUMBER}", _numbers("zoom", "grow"), ()),
    "seams": Check(
        rf"scales {NUMBER}(?:, {NUMBER})*",
        lambda m: [float(n) for n in re.findall(NUMBER, m[0])],
        (),
    ),
    "safe-centre": Check(r"none", _none, ()),
    "card-rows": Check(r"none", _none, ("part:card",)),
    "safe-bottom": Check(rf"inset {NUMBER}", _numbers("inset"), ()),
    "text-edge": Check(r"none", _none, ()),
    "content-width": Check(
        rf"reading {NUMBER}, default {NUMBER}", _numbers("reading", "default"), ()
    ),
    "footer-bands": Check(r"none", _none, ()),
    "capped-centre": Check(r"none", _none, ()),
    "line-length": Check(
        rf"body {NUMBER}-{NUMBER}, columns {NUMBER}-{NUMBER}, large {NUMBER}, short {NUMBER}",
        _numbers("body_lo", "body_hi", "columns_lo", "columns_hi", "large", "short"),
        (),
    ),
    "optical": Check(r"none", _none, ()),
    "table-width": Check(r"none", _none, ()),
    "table-narrow": Check(r"none", _none, ()),
    "button-stack": Check(r"none", _none, ()),
    "card-columns": Check(
        rf"one under {NUMBER}, minimum {NUMBER}em",
        _numbers("under", "minimum"),
        ("part:card",),
    ),
    "panes": Check(
        rf"one under {NUMBER} or under {NUMBER} tall", _numbers("wide", "tall"), ()
    ),
    "side-pane": Check(
        rf"one under {NUMBER} or under {NUMBER} tall", _numbers("wide", "tall"), ()
    ),
    "popover-sheet": Check(rf"under {NUMBER}", _numbers("under"), ()),
    "bar-fit": Check(r"none", _none, ()),
    "breadcrumb": Check(r"label (\S.*)", lambda m: m[1], ()),
    "nav-strip": Check(r"none", _none, ()),
    "tabs-narrow": Check(r"none", _none, ()),
    "footer-narrow": Check(
        rf"toggles under {NUMBER}, {NUMBER} columns from {NUMBER}, {NUMBER} columns from {NUMBER}",
        _numbers("toggles", "mid_columns", "mid", "wide_columns", "wide"),
        (),
    ),
    "card-media": Check(rf"{NUMBER}em", _numbers("threshold"), ("part:card",)),
    "label-value": Check(rf"size {NUMBER}", _numbers("size"), ()),
    "row-wrap": Check(r"none", _none, ()),
    # No check of its own: the width under which the phone-only checks judge.
    "phone-width": Check(rf"under {NUMBER}", _numbers("under"), ()),
    "logo-version": Check(r"none", _none, ("part:logo",)),
}
BRIEF = {"kind": ("app", "site"), "page": ("reading", "default", "canvas")}
# A box edge within this many px of another counts as on it: rounding, as
# check-layout.py's own EDGE.
EDGE = 1
# Blink lays boxes out in 64ths of a px, so an edge this close to a whole
# device pixel lands on it.
SNAP = 1 / 64
# A passage of this many lines or fewer is short, as vault.line-length's
# applies-when gives it.
SHORT_LINES = 3
# How far the line-length read widens the page: any width well past EDGE
# serves.
FILL_PROBE = 16


def parse_value(mode, value):
    """A table value for `mode`, as its check reads it. Raises ValueError
    where it does not fit the check's shape."""
    m = re.fullmatch(CHECKS[mode].pattern, value)
    if m is None:
        raise ValueError(
            f"{mode} wants a value like {CHECKS[mode].pattern!r}, got {value!r}"
        )
    return CHECKS[mode].parse(m)


def missing(mode, parts, brief):
    """What the round must still give before `mode` can judge, in words, or
    None. `parts` maps a declared part to its selector or None."""
    for need in CHECKS[mode].needs:
        kind, _, name = need.partition(":")
        if kind == "part" and not parts.get(name):
            return f"no {name} part declared with a selector (--parts)"
        if kind == "brief" and name not in brief:
            return f"no --brief {name}= given"
    return None


# Each fault is {kind: <check>, subject, detail}; `seen` names the
# checks that found something their record applies to.
READ_JS = (
    r"""
(args) => {
"""
    + "  const label = "
    + "%LABEL%"
    + r""";
  const { lines, parts, brief, phone, edge: EDGE, snap: SNAP } = args;
  const vw = document.documentElement.clientWidth, vh = innerHeight;
  const css = (el) => getComputedStyle(el);
  const box = (el) => el.getBoundingClientRect();
  const drawn = (el) => {
    if (!el || !el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) return false;
    const r = box(el);
    return r.width > 0 && r.height > 0;
  };
  const inView = (el) => { const r = box(el); return drawn(el) && r.right > EDGE && r.left < vw - EDGE; };
  const all = [...document.body.querySelectorAll('*')];
  const place = new Map(all.map((e, i) => [e, i]));
  const faults = [], seen = new Set(), notes = {}, unread = new Set();
  const fault = (kind, subject, detail) => faults.push({ kind, subject, detail });
  const on = (mode) => mode in lines;
  const px = (n) => `${Math.round(n)} px`;
  const pinned = (el) => {
    for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
      const p = css(e).position;
      if (p === 'fixed' || p === 'sticky') return e;
    }
    return null;
  };
  // The boxes of an element's set text, each line's.
  const range = document.createRange();
  const textBoxes = (el, free) => {
    const out = [];
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      if (!/\S/.test(n.data) || !n.parentElement || !drawn(n.parentElement) || n.parentElement.closest('svg') || (free && pinned(n.parentElement))) continue;
      range.selectNodeContents(n);
      for (const r of range.getClientRects()) if (r.width > 0 && r.height > 0) out.push(r);
    }
    return out;
  };
  const textLeft = (el) => { const b = textBoxes(el); return b.length ? Math.min(...b.map((r) => r.left)) : null; };
  const union = (rects) => rects.length ? { left: Math.min(...rects.map((r) => r.left)), right: Math.max(...rects.map((r) => r.right)),
    top: Math.min(...rects.map((r) => r.top)), bottom: Math.max(...rects.map((r) => r.bottom)) } : null;
  const vOverlap = (a, b) => Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > EDGE;
  const beside = (a, b) => vOverlap(a, b) && (a.right <= b.left + EDGE || b.right <= a.left + EDGE);
  // Elements grouped into rows by their top edge, top to bottom.
  const rowsOf = (els) => {
    const rows = [];
    for (const el of els.slice().sort((a, b) => box(a).top - box(b).top)) {
      const row = rows.find((r) => Math.abs(box(r[0]).top - box(el).top) <= EDGE);
      if (row) row.push(el); else rows.push([el]);
    }
    return rows;
  };
  const named = (el) => (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ');
  const IMAGE = 'img, picture, video, canvas, svg';
  const BUTTON = 'button, input[type="button"], input[type="submit"], input[type="reset"], [role="button"]';
  const TOGGLE = 'summary, button[aria-expanded], [role="button"][aria-expanded]';
  const banner = document.querySelector('[role="banner"]') ||
    [...document.querySelectorAll('header')].find((h) => !h.parentElement.closest('article, aside, main, nav, section'));
  const crumbs = (el) => /breadcrumb/i.test(`${el.getAttribute('aria-label') || ''} ${el.className || ''}`);
  const mainNav = () => {
    if (parts.nav) return document.querySelector(parts.nav);
    const navs = [...document.querySelectorAll('nav, [role="navigation"]')].filter((n) => !crumbs(n));
    return navs.find((n) => banner && banner.contains(n)) || navs[0] || null;
  };
  // A nav's top-level links: its first list's items' own links, else every link.
  const topLinks = (nav) => {
    const list = nav.querySelector('ul, ol');
    const links = list ? [...list.children].map((li) => li.querySelector(':scope > a[href], :scope > * > a[href]')).filter(Boolean)
      : [...nav.querySelectorAll('a[href]')];
    return links;
  };
  const toggleFor = (el) => {
    const ids = [el, ...el.querySelectorAll('[id]')].map((e) => e.id).filter(Boolean);
    return [...document.querySelectorAll('[aria-controls]')].find((t) => t.getAttribute('aria-controls').split(/\s+/).some((id) => ids.includes(id)))
      || (banner && el !== banner && banner.contains(el) ? banner.querySelector('button[aria-expanded]') : null);
  };
  // The outermost elements capped by a max-width, where it holds their width: a page's capped containers.
  const capped = (within) => {
    const out = [];
    const walk = (el) => {
      for (const c of el.children) {
        const cs = css(c), cap = parseFloat(cs.maxWidth);
        const text = c.matches('p, h1, h2, h3, h4, h5, h6, li, blockquote, figcaption, a, button, img, svg');
        if (cs.maxWidth.endsWith('px') && !text) { if (drawn(c) && box(c).width >= cap - EDGE && c.querySelector('*')) out.push(c); }
        else walk(c);
      }
    };
    walk(within);
    return out;
  };

  // vault.false-floor: a full-width band ends at the first screen's foot and nothing runs past it.
  if (on('fold') && document.documentElement.scrollHeight > vh + EDGE) {
    seen.add('fold');
    const content = [];
    for (const el of all) {
      if (pinned(el) || !drawn(el)) continue;
      if (el.matches(IMAGE) && !el.parentElement.closest('svg')) content.push(box(el));
      else if (/url\(/.test(css(el).backgroundImage)) content.push(box(el));
    }
    content.push(...textBoxes(document.body, true));
    const crosses = content.some((r) => r.top < vh - EDGE && r.bottom > vh + EDGE);
    const paints = (el) => { const s = css(el); return s.backgroundColor !== 'rgba(0, 0, 0, 0)' || s.backgroundImage !== 'none'; };
    const band = all.find((el) => !pinned(el) && drawn(el) && paints(el) && Math.abs(box(el).bottom - vh) <= EDGE);
    if (!crosses && band) fault('fold', label(band), `ends at the first screen's foot, ${vh} px down, and no text or image runs past it`);
  }

  // vault.safe-centre: centred content past its scrolling or clipping box's start edge.
  if (on('safe-centre')) {
    for (const el of all) {
      const cs = css(el);
      if (!/flex|grid/.test(cs.display) || !drawn(el)) continue;
      const ways = [cs.justifyContent, cs.alignItems, cs.alignContent, cs.justifyItems].filter((v) => /(^|\s)center/.test(v));
      if (!ways.length) continue;
      seen.add('safe-centre');
      if (cs.overflowX === 'visible' && cs.overflowY === 'visible') continue;
      const r = box(el), left = r.left + el.clientLeft, top = r.top + el.clientTop;
      for (const c of el.children) {
        if (!drawn(c)) continue;
        const by = Math.max(left - box(c).left, top - box(c).top);
        if (by > EDGE) { fault('safe-centre', label(el), `centres ${label(c)} without safe, so its first ${px(by)} sit before the box's start, out of scroll reach`); break; }
      }
    }
  }

  // vault.joined-fills: adjacent boxes of one opaque fill that meet off a whole device pixel.
  if (on('seams')) {
    const opaque = (c) => { const m = /rgba\([^)]*,\s*([\d.]+)\)/.exec(c); return c !== 'transparent' && (!m || parseFloat(m[1]) === 1); };
    const under = (el) => { for (let e = el; e; e = e.parentElement) { const c = css(e).backgroundColor; if (opaque(c)) return c; } return 'rgb(255, 255, 255)'; };
    for (const p of all) {
      const kids = [...p.children].filter(drawn);
      for (let i = 0; i + 1 < kids.length; i++) {
        const a = kids[i], b = kids[i + 1], fill = css(a).backgroundColor;
        if (!opaque(fill) || css(b).backgroundColor !== fill || [a, b].some((e) => e.matches(`${BUTTON}, a[href], input, select, textarea`))) continue;
        const ra = box(a), rb = box(b);
        const side = Math.abs(ra.right - rb.left) <= SNAP && vOverlap(ra, rb);
        const stack = Math.abs(ra.bottom - rb.top) <= SNAP && Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left) > EDGE;
        if (!side && !stack) continue;
        const edges = side ? [css(a).borderRightWidth, css(b).borderLeftWidth] : [css(a).borderBottomWidth, css(b).borderTopWidth];
        if (edges.some((w) => parseFloat(w) > 0)) continue;
        seen.add('seams');
        if (under(p) === fill) continue;
        const at = side ? ra.right + scrollX : ra.bottom + scrollY;
        const off = lines.seams.filter((s) => Math.abs(at * s - Math.round(at * s)) > SNAP);
        if (off.length) fault('seams', `${label(a)} and ${label(b)}`, `meet at ${+at.toFixed(2)} px, off a whole device pixel at ${off.map((s) => `${s * 100}%`).join(', ')} display scale, with their shared fill not on their container`);
      }
    }
  }

  // vault.capped-centre: a capped container off centre in its wider parent.
  if (on('capped-centre')) {
    for (const c of capped(document.body)) {
      const p = c.parentElement, pr = box(p), ps = css(p);
      const left = pr.left + p.clientLeft + parseFloat(ps.paddingLeft), right = pr.left + p.clientLeft + p.clientWidth - parseFloat(ps.paddingRight);
      const r = box(c);
      if (right - left <= r.width + EDGE) continue;
      seen.add('capped-centre');
      const gl = r.left - left, gr = right - r.right;
      if (Math.abs(gl - gr) > EDGE) fault('capped-centre', label(c), `sits ${px(gl)} from its space's left and ${px(gr)} from its right, not centred`);
    }
  }

  // vault.content-width: the main content's text and images wider than its role's cap.
  if (on('content-width') && brief.page !== 'canvas') {
    const cap = brief.page === 'reading' ? lines['content-width'].reading : lines['content-width'].default;
    if (vw > cap + EDGE) {
      const main = document.querySelector('main, [role="main"]') || document.body;
      const items = [...main.querySelectorAll('*')].filter((e) => drawn(e) && !e.parentElement.closest('svg') &&
        (e.matches(IMAGE) || [...e.childNodes].some((n) => n.nodeType === 3 && /\S/.test(n.data))))
        .map((e) => [e, e.matches(IMAGE) ? box(e) : union(textBoxes(e))]).filter(([, r]) => r && r.right - r.left < vw - EDGE);
      const u = union(items.map(([, r]) => r));
      if (u) {
        seen.add('content-width');
        const widest = items.reduce((a, b) => (b[1].right - b[1].left > a[1].right - a[1].left ? b : a))[0];
        if (u.right - u.left > cap + EDGE) fault('content-width', label(widest), `spreads the main content ${px(u.right - u.left)} wide, past the ${cap} px a ${brief.page || 'default'} page is capped at`);
      }
    }
  }

  // vault.content-width, footer bands: each band's content edges against the first's.
  if (on('footer-bands')) {
    const foot = document.querySelector('[role="contentinfo"]') ||
      [...document.querySelectorAll('footer')].reverse().find((f) => !f.parentElement.closest('article, aside, main, section'));
    const bands = foot ? [...foot.children].filter((b) => drawn(b) && box(b).width >= box(foot).width - EDGE) : [];
    if (bands.length >= 2) {
      seen.add('footer-bands');
      // A band's content box: down through each lone block child to the box that holds its content.
      const inner = (b) => {
        let c = b;
        for (let k = [...c.children].filter(drawn); k.length === 1 && !/^inline/.test(css(k[0]).display); k = [...c.children].filter(drawn)) c = k[0];
        const r = box(c), s = css(c);
        return { left: r.left + c.clientLeft + parseFloat(s.paddingLeft), right: r.right - parseFloat(s.borderRightWidth) - parseFloat(s.paddingRight) };
      };
      const first = inner(bands[0]);
      for (const b of bands.slice(1)) {
        const r = inner(b);
        if (Math.abs(r.left - first.left) > EDGE || Math.abs(r.right - first.right) > EDGE)
          fault('footer-bands', label(b), `holds its content ${px(r.left)}–${px(r.right)} across, not the ${px(first.left)}–${px(first.right)} of ${label(bands[0])}`);
      }
    }
  }

  // vault.alignment-lines: each section's main text edge against the edge most sections share.
  if (on('text-edge')) {
    const main = document.querySelector('main, [role="main"]') || document.body;
    const edges = [];
    for (const s of main.children) {
      if (!drawn(s) || s.matches('header, footer, nav, aside, [role="banner"], [role="contentinfo"]') || (parts.hero && s.matches(parts.hero))) continue;
      const t = s.querySelector('h1, h2, h3, h4, h5, h6, p, li');
      if (!t || !drawn(t) || css(t).textAlign === 'center') continue;
      const tl = textLeft(t);
      if (tl === null) continue;
      const sr = box(s), tr = box(t);
      if (Math.abs((tr.left - sr.left) - (sr.right - tr.right)) <= EDGE && tr.width < sr.width - EDGE && css(t).textAlign !== 'start' && css(t).textAlign !== 'left') continue;
      edges.push([s, Math.round(tl)]);
    }
    if (edges.length >= 2) {
      seen.add('text-edge');
      const count = new Map();
      for (const [, e] of edges) count.set(e, (count.get(e) || 0) + 1);
      const common = [...count].sort((a, b) => b[1] - a[1] || a[0] - b[0])[0][0];
      for (const [s, e] of edges) if (Math.abs(e - common) > EDGE) fault('text-edge', label(s), `starts its text at ${px(e)}, off the ${px(common)} edge the page's other sections share`);
    }
  }

  // vault.optical-alignment: an unpainted padded box aligned with its neighbour by its box, not its text.
  if (on('optical')) {
    const paints = (el) => { const s = css(el); return s.backgroundColor !== 'rgba(0, 0, 0, 0)' || s.backgroundImage !== 'none' || s.boxShadow !== 'none' ||
      ['Top', 'Right', 'Bottom', 'Left'].some((k) => parseFloat(s[`border${k}Width`]) > 0); };
    for (const p of all) {
      const kids = [...p.children].filter((c) => drawn(c) && textLeft(c) !== null);
      for (let i = 0; i + 1 < kids.length; i++) {
        for (const [a, b] of [[kids[i], kids[i + 1]], [kids[i + 1], kids[i]]]) {
          if (!a.matches('div, section, article, aside, header, footer') || paints(a) || parseFloat(css(a).paddingLeft) <= EDGE) continue;
          if (Math.abs(box(a).left - box(b).left) > EDGE) continue;
          if (![a, b].every((e) => /^(start|left|justify)$/.test(css(e).textAlign) && css(e).direction === 'ltr')) continue;
          seen.add('optical');
          const by = textLeft(a) - textLeft(b);
          if (Math.abs(by) > EDGE) fault('optical', label(a), `lines its box up with ${label(b)}'s, so its text sits ${px(Math.abs(by))} off ${label(b)}'s, its padding showing nothing`);
        }
      }
    }
  }

  // The width a table's columns need, read by setting it to max-content.
  const needs = (t) => {
    const was = [t.style.width, t.style.maxWidth];
    t.style.setProperty('width', 'max-content', 'important');
    t.style.setProperty('max-width', 'none', 'important');
    const w = box(t).width;
    t.style.width = was[0]; t.style.maxWidth = was[1];
    return w;
  };
  const scroller = (el) => { for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) if (/auto|scroll/.test(css(e).overflowX)) return e; return null; };

  // vault.table-width: a table held under the width its columns need, or widening the page.
  if (on('table-width')) {
    for (const t of document.querySelectorAll('table')) {
      if (!drawn(t)) continue;
      seen.add('table-width');
      const r = box(t), p = t.parentElement, room = p.clientWidth - parseFloat(css(p).paddingLeft) - parseFloat(css(p).paddingRight);
      const need = needs(t);
      if (!scroller(t) && r.right > vw + EDGE) fault('table-width', label(t), `runs ${px(r.right - vw)} past the screen's edge, widening the page, with no scrolling box of its own`);
      else if (r.width < need - EDGE && room > r.width + EDGE) fault('table-width', label(t), `is held to ${px(r.width)}, under the ${px(need)} its columns need, with ${px(room)} free`);
    }
  }

  // vault.table-narrow: at phone width, a table too wide for the screen neither scrolls in a focusable box nor stacks.
  if (on('table-narrow') && phone) {
    for (const t of document.querySelectorAll('table')) {
      if (!drawn(t)) continue;
      const row = t.querySelector('tr');
      const stacked = row && css(row).display !== 'table-row';
      if (!stacked && needs(t) <= vw + EDGE) continue;
      seen.add('table-narrow');
      if (stacked) continue;
      const s = scroller(t);
      if (!s) fault('table-narrow', label(t), `is too wide for the screen and neither scrolls in a box of its own nor stacks its rows`);
      else if (!s.hasAttribute('tabindex') || s.tabIndex < 0) fault('table-narrow', label(t), `scrolls in ${label(s)}, which a keyboard cannot focus to scroll`);
    }
  }

  // vault.button-group-stack: at phone width, a group of buttons that wraps ragged, overflows, or stacks short of full width.
  const buttonLike = (c) => c.matches(BUTTON) || (c.querySelectorAll(BUTTON).length === 1 && !c.querySelector('p, h1, h2, h3, h4, h5, h6'));
  const groups = () => all.filter((g) => { const k = [...g.children].filter(drawn); return k.length >= 2 && k.every(buttonLike); });
  if (on('button-stack') && phone) {
    for (const g of groups()) {
      seen.add('button-stack');
      const k = [...g.children].filter(drawn), rows = rowsOf(k), gr = box(g);
      const inner = gr.width - parseFloat(css(g).paddingLeft) - parseFloat(css(g).paddingRight);
      if (k.some((c) => box(c).right > Math.min(gr.right, vw) + EDGE)) fault('button-stack', label(g), `runs its buttons past its edge`);
      else if (rows.length > 1 && rows.some((r) => r.length > 1)) fault('button-stack', label(g), `wraps its ${k.length} buttons into a ragged ${rows.length}-row block`);
      else if (rows.length > 1 && rows.every((r) => r.length === 1) && k.some((c) => box(c).width < inner - EDGE)) fault('button-stack', label(g), `stacks its buttons, but not each the group's full width`);
    }
  }

  // vault.row-wrap: a one-line row of like inline items that overflows or squeezes them.
  if (on('row-wrap')) {
    for (const r of all) {
      const cs = css(r);
      if (!/flex/.test(cs.display) || !/^row/.test(cs.flexDirection) || cs.flexWrap !== 'nowrap' || /auto|scroll/.test(cs.overflowX) || !drawn(r)) continue;
      const k = [...r.children].filter(drawn);
      if (k.length < 2 || new Set(k.map((c) => c.localName)).size > 1 || r.closest('nav, [role="navigation"], [role="toolbar"]') || k.every(buttonLike)) continue;
      if (k.some((c) => c.matches('div, section, article, aside, main, header, footer, form, ul, ol, table') || c.querySelector('p, h1, h2, h3, h4, h5, h6, ul, ol, div'))) continue;
      seen.add('row-wrap');
      const rr = box(r), end = rr.right - parseFloat(cs.paddingRight) - r.clientLeft;
      const natural = (c) => { const was = c.style.cssText; c.style.setProperty('flex', 'none', 'important'); c.style.setProperty('width', 'max-content', 'important');
        const w = box(c).width; c.style.cssText = was; return w; };
      const squeezed = k.find((c) => box(c).width < natural(c) - EDGE);
      if (box(k[k.length - 1]).right > end + EDGE) fault('row-wrap', label(r), `runs its items ${px(box(k[k.length - 1]).right - end)} past its edge on one line`);
      else if (squeezed) fault('row-wrap', label(r), `squeezes ${label(squeezed)} below its content's width on one line`);
    }
  }

  // vault.nav-strip: at phone width, a row of nav links on many rows, past the page, or scrolling with no link cut by its edge.
  if (on('nav-strip') && phone) {
    for (const nav of document.querySelectorAll('nav, [role="navigation"]')) {
      if (crumbs(nav)) continue;
      const links = [...nav.querySelectorAll('a[href]')].filter(drawn);
      if (links.length < 2) continue;
      seen.add('nav-strip');
      const rows = rowsOf(links), s = scroller(links[0]);
      if (rows.every((r) => r.length === 1)) continue;
      if (rows.length > 1) { fault('nav-strip', label(nav), `spills its ${links.length} links onto ${rows.length} rows`); continue; }
      if (!s || !nav.contains(s)) { if (links.some((l) => box(l).right > vw + EDGE)) fault('nav-strip', label(nav), `runs its links past the screen's edge with no sideways scroll`); continue; }
      if (s.scrollWidth <= s.clientWidth + EDGE) continue;
      const edge = box(s).left + s.clientLeft + s.clientWidth;
      if (!links.some((l) => box(l).left < edge - EDGE && box(l).right > edge + EDGE)) fault('nav-strip', label(nav), `scrolls sideways, but its edge cuts no link, so nothing shows more follows`);
    }
  }

  // vault.breadcrumb-narrow: at phone width, a trail hidden, wrapping, overflowing, or collapsed other than to its first and last.
  if (on('breadcrumb') && phone) {
    for (const nav of [...document.querySelectorAll('nav, [role="navigation"], ol, ul')].filter((e) => crumbs(e) && !e.parentElement.closest('nav, [role="navigation"], ol, ul'))) {
      seen.add('breadcrumb');
      const items = [...nav.querySelectorAll('li')];
      const shown = items.filter(drawn);
      if (!drawn(nav) || !shown.length) { fault('breadcrumb', label(nav), `is not shown`); continue; }
      const rows = rowsOf(shown), nr = box(nav);
      if (rows.length > 1) fault('breadcrumb', label(nav), `wraps onto ${rows.length} lines`);
      else if (shown.some((i) => box(i).right > Math.min(nr.right, vw) + EDGE)) fault('breadcrumb', label(nav), `runs past its edge`);
      else if (shown.length < items.length) {
        const more = [...nav.querySelectorAll(BUTTON)].find((b) => drawn(b) && named(b) === lines.breadcrumb);
        const ends = drawn(items[0]) && drawn(items[items.length - 1]);
        if (!ends || !more) fault('breadcrumb', label(nav), `hides ${items.length - shown.length} of its ${items.length} items ${!ends ? 'other than the middle ones' : `with no "${lines.breadcrumb}" button to show them`}`);
      }
    }
  }

  // vault.footer-narrow: the footer's link groups, toggled on a phone and in columns wider.
  if (on('footer-narrow')) {
    const v = lines['footer-narrow'];
    const foot = document.querySelector('[role="contentinfo"]') || [...document.querySelectorAll('footer')].pop();
    const allHeads = foot ? [...foot.querySelectorAll('h2, h3, h4, h5, h6, [role="heading"], summary')] : [];
    const heads = allHeads.filter((h) => !allHeads.some((o) => o !== h && o.contains(h)));
    const groupsOf = heads.map((h) => { let g = h.parentElement; while (g !== foot && g.querySelectorAll('a[href]').length < 2) g = g.parentElement; return [h, g]; })
      .filter(([, g]) => g !== foot && heads.filter((h) => g.contains(h)).length === 1);
    if (groupsOf.length >= 2) {
      seen.add('footer-narrow');
      if (vw < v.toggles) {
        for (const [h, g] of groupsOf) {
          const open = [...g.querySelectorAll('a[href]')].filter(drawn).length;
          if (open || !(h.matches(TOGGLE) || h.querySelector(TOGGLE) || h.closest(TOGGLE))) fault('footer-narrow', label(g), `shows its ${open} links${h.matches(TOGGLE) || h.querySelector(TOGGLE) ? '' : ' under a heading that is no toggle'}, not its heading alone`);
        }
      } else {
        const want = vw >= v.wide ? v.wide_columns : vw >= v.mid ? v.mid_columns : 1;
        const rows = rowsOf(groupsOf.map(([, g]) => g).filter(drawn));
        const across = rows.length ? rows[0].length : 0;
        if (across !== Math.min(want, groupsOf.length)) fault('footer-narrow', label(foot), `sets its link groups ${across} across, not ${Math.min(want, groupsOf.length)}`);
      }
    }
  }

  const nav = mainNav();
  // vault.nav-wide: at desktop width, a main nav link hidden behind a menu.
  if (on('nav-wide') && nav && vw >= lines['nav-wide'].from) {
    const links = topLinks(nav);
    if (links.length) {
      seen.add('nav-wide');
      const hid = links.filter((l) => !inView(l));
      if (hid.length) fault('nav-wide', label(nav), `hides ${hid.length} of its ${links.length} top-level links behind a menu`);
    }
  }

  // vault.visible-nav: at phone width, a main nav of few links that hides them.
  if (on('visible-nav') && nav && phone) {
    const links = topLinks(nav);
    if (links.length) {
      seen.add('visible-nav');
      const hid = links.filter((l) => !inView(l));
      if (links.length <= lines['visible-nav'].most && hid.length) fault('visible-nav', label(nav), `hides ${hid.length} of its ${links.length} links behind a menu, though ${lines['visible-nav'].most} or fewer stay in view`);
    }
  }

  // vault.nav-by-width: where the main nav sits, by the brief's kind and the width.
  if (on('nav-place') && nav && brief.kind) {
    const shown = drawn(nav) && topLinks(nav).some(inView) ? nav : toggleFor(nav);
    if (shown && drawn(shown)) {
      seen.add('nav-place');
      const r = box(shown), narrow = vw < lines['nav-place'].under;
      const inHeader = banner && banner.contains(shown) && box(banner).top + scrollY < vh;
      let want = null;
      if (brief.kind === 'site' && !inHeader) want = 'in the top header';
      if (brief.kind === 'app' && narrow && !(Math.abs(r.bottom - vh) <= EDGE && r.width >= vw - EDGE)) want = 'in a bar along the bottom';
      if (brief.kind === 'app' && !narrow && !((r.left <= EDGE || r.right >= vw - EDGE) && r.height > r.width)) want = 'in a rail beside the content';
      if (want) fault('nav-place', label(shown), `sits at ${px(r.left)}, ${px(r.top)}, not ${want} ${brief.kind === 'app' ? 'an app' : 'a site'}'s nav takes ${narrow ? 'under' : 'from'} ${lines['nav-place'].under} px`);
    }
  }

  // The page's panes: its main content, and each supporting pane outside it or a child of it.
  const mainEl = document.querySelector('main, [role="main"]');
  const asides = [...document.querySelectorAll('aside, [role="complementary"]')]
    .filter((a) => !a.parentElement.closest('article, aside, [role="complementary"]') && (!mainEl || !mainEl.contains(a) || a.parentElement === mainEl));
  const mainBox = () => {
    if (!mainEl || !drawn(mainEl)) return null;
    const own = [...mainEl.children].filter((c) => drawn(c) && !asides.includes(c));
    return asides.some((a) => a.parentElement === mainEl) ? union(own.map(box)) : box(mainEl);
  };
  const oneUnder = (v) => vw < v.wide || vh < v.tall;
  // vault.panes-by-width: panes side by side past what the window allows, or the header and footer not around them.
  if (on('panes') && mainEl) {
    const m = mainBox();
    if (m) {
      seen.add('panes');
      const side = asides.filter((a) => drawn(a) && beside(box(a), m));
      const most = oneUnder(lines.panes) ? 1 : 2;
      if (side.length + 1 > most) fault('panes', label(mainEl), `sets ${side.length + 1} panes side by side, where a ${vw} by ${vh} px window allows ${most}`);
      const head = banner && drawn(banner) && !/absolute|fixed/.test(css(banner).position) ? box(banner) : null;
      const foot = document.querySelector('[role="contentinfo"]') || [...document.querySelectorAll('footer')].find((f) => !f.parentElement.closest('article, aside, main, section'));
      if (head && head.bottom > m.top + EDGE) fault('panes', label(banner), `does not span the top above the panes`);
      if (foot && drawn(foot) && box(foot).top < m.bottom - EDGE) fault('panes', label(foot), `does not span the bottom below the panes`);
    }
  }

  // vault.side-pane: where one pane fits, a side pane squeezed beside the main content, above it, or dropped with nothing to open it.
  if (on('side-pane') && mainEl && oneUnder(lines['side-pane'])) {
    const m = mainBox();
    for (const a of asides) {
      if (!m) break;
      seen.add('side-pane');
      if (!drawn(a)) {
        const opener = a.id && [...document.querySelectorAll(`[aria-controls~="${a.id}"], a[href="#${a.id}"], [popovertarget="${a.id}"], [commandfor="${a.id}"]`)].find((o) => drawn(o) && named(o));
        if (!opener) fault('side-pane', label(a), `is hidden with no labelled control to open it`);
        continue;
      }
      const r = box(a);
      if (beside(r, m)) fault('side-pane', label(a), `is squeezed beside the main content, ${px(r.width)} wide`);
      else if (!pinned(a) && r.top < m.top - EDGE) fault('side-pane', label(a), `sits above the main content, not below it`);
    }
  }

  // vault.bar-fit: a bar's actions past the screen or past the bar's own edge.
  if (on('bar-fit')) {
    for (const bar of document.querySelectorAll('[role="toolbar"], [role="menubar"]')) {
      if (!drawn(bar)) continue;
      seen.add('bar-fit');
      const br = box(bar), s = css(bar), clips = s.overflowX !== 'visible';
      const right = clips ? Math.min(vw, br.left + bar.clientLeft + bar.clientWidth) : vw;
      const out = [...bar.querySelectorAll(`${BUTTON}, a[href], [role="menuitem"]`)].filter((a) => drawn(a) && (box(a).right > right + EDGE || box(a).left < -EDGE));
      if (out.length) fault('bar-fit', label(bar), `has ${out.length} of its actions past ${clips ? 'its own edge' : "the screen's edge"}, ${out.map((a) => label(a)).join(', ')}`);
    }
  }

  // vault.bottom-safe-area: a control pinned to the bottom that a large viewport unit places.
  if (on('safe-bottom') && phone) {
    const LVH = /\d(lvh|lvb)\b/;
    const PLACING = ['top', 'bottom', 'height', 'min-height', 'max-height', 'inset', 'inset-block', 'inset-block-start', 'inset-block-end', 'translate', 'transform', 'block-size', 'min-block-size', 'max-block-size'];
    const rules = [];
    const collect = (list) => { for (const r of list) { if (r.cssRules && !(r instanceof CSSStyleRule)) { if (!r.media || matchMedia(r.media.mediaText).matches) collect(r.cssRules); } else if (r.selectorText) rules.push(r); } };
    for (const sh of document.styleSheets) { try { collect(sh.cssRules); } catch (e) { unread.add('safe-bottom'); } }
    for (const el of all) {
      const p = pinned(el);
      if (p !== el || !drawn(el) || Math.abs(box(el).bottom - vh) > EDGE) continue;
      seen.add('safe-bottom');
      const decl = rules.filter((r) => { try { return el.matches(r.selectorText); } catch (e) { return false; } }).map((r) => r.style).concat([el.style]);
      const by = PLACING.find((k) => decl.some((d) => LVH.test(d.getPropertyValue(k))));
      if (by) fault('safe-bottom', label(el), `is placed by ${by} in lvh, which a browser's toolbar can cover`);
    }
  }

  // vault.rtl-image-order: a row of images in right-to-left text that runs left to right.
  if (on('rtl-order')) {
    for (const p of all) {
      if (css(p).direction !== 'rtl') continue;
      const k = [...p.children].filter((c) => drawn(c) && (c.matches(IMAGE) || c.querySelector(IMAGE)));
      if (k.length < 2 || rowsOf(k).length !== 1) continue;
      seen.add('rtl-order');
      if (k.some((c, i) => i && box(c).right > box(k[i - 1]).left + EDGE)) fault('rtl-order', label(p), `runs its ${k.length} images left to right in right-to-left text, its first at the left`);
    }
  }

  // vault.label-value-stack: a label beside its value, one cut off or the two overlapping.
  if (on('label-value')) {
    const pairs = [];
    for (const dt of document.querySelectorAll('dt')) { const dd = dt.nextElementSibling; if (dd && dd.localName === 'dd') pairs.push([dt, dd]); }
    for (const r of all) {
      const k = [...r.children];
      if (k.length === 2 && /flex/.test(css(r).display) && /^row/.test(css(r).flexDirection) && k.every((c) => c.textContent.trim() && !c.querySelector('div, p, ul, ol'))) pairs.push(k);
    }
    for (const [a, b] of pairs) {
      if (!drawn(a) || !drawn(b)) continue;
      seen.add('label-value');
      const cut = [a, b].find((c) => css(c).overflowX !== 'visible' && c.scrollWidth > c.clientWidth + EDGE);
      const ra = box(a), rb = box(b);
      const cross = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left) > EDGE && vOverlap(ra, rb);
      if (cut) fault('label-value', label(cut), `cuts off ${px(cut.scrollWidth - cut.clientWidth)} of its text beside ${label(cut === a ? b : a)}`);
      else if (cross) fault('label-value', `${label(a)} and ${label(b)}`, `overlap`);
    }
  }

  // vault.card-alignment: matching inner parts of a row of sibling cards at different heights.
  if (on('card-rows') && parts.card) {
    const cards = [...document.querySelectorAll(parts.card)].filter(drawn);
    const byParent = new Map();
    for (const c of cards) { if (!byParent.has(c.parentElement)) byParent.set(c.parentElement, []); byParent.get(c.parentElement).push(c); }
    const key = (card, el) => { const path = []; for (let e = el; e !== card; e = e.parentElement) path.unshift(`${e.localName}:${[...e.parentElement.children].filter((s) => s.localName === e.localName).indexOf(e)}`); return path.join('/'); };
    for (const sibs of byParent.values()) {
      for (const row of rowsOf(sibs).filter((r) => r.length >= 2)) {
        seen.add('card-rows');
        const maps = row.map((c) => new Map([...c.querySelectorAll('*')].filter((e) => drawn(e) && !/^inline|contents/.test(css(e).display)).map((e) => [key(c, e), e])));
        const bad = [];
        for (const k of maps[0].keys()) {
          if (!maps.every((m) => m.has(k)) || bad.some((b) => k.startsWith(`${b}/`))) continue;
          const tops = maps.map((m) => box(m.get(k)).top);
          if (Math.max(...tops) - Math.min(...tops) > EDGE) bad.push(k);
        }
        for (const k of bad) {
          const tops = maps.map((m) => box(m.get(k)).top);
          fault('card-rows', label(maps[0].get(k)), `starts ${px(Math.max(...tops) - Math.min(...tops))} apart across the ${row.length} cards of its row`);
        }
      }
    }
  }

  // vault.content-columns: a grid of cards in more than one column on a phone, or squeezing its cards under their minimum.
  if (on('card-columns') && parts.card) {
    const v = lines['card-columns'];
    const byParent = new Map();
    for (const c of [...document.querySelectorAll(parts.card)].filter(drawn)) { if (!byParent.has(c.parentElement)) byParent.set(c.parentElement, []); byParent.get(c.parentElement).push(c); }
    for (const [p, sibs] of byParent) {
      if (sibs.length < 2) continue;
      seen.add('card-columns');
      const across = rowsOf(sibs)[0].length, c = sibs[0], min = v.minimum * parseFloat(css(c).fontSize);
      if (vw < v.under && across > 1) fault('card-columns', label(p), `sets its cards ${across} across under ${v.under} px, not in one column`);
      else if (across > 1 && box(c).width < min - EDGE) fault('card-columns', label(p), `squeezes its ${across} columns of cards to ${px(box(c).width)}, under their ${v.minimum}em minimum of ${px(min)}`);
    }
  }

  // vault.card-media-stack and vault.logo-version read across widths: each card's media placement, and the logo shown.
  if (on('card-media') && parts.card) {
    notes.cards = [];
    for (const c of [...document.querySelectorAll(parts.card)].filter(drawn)) {
      const media = [...c.querySelectorAll(IMAGE)].find(drawn), text = textBoxes(c);
      if (!media || !text.length) continue;
      const m = box(media), t = union(text);
      notes.cards.push({ at: place.get(c), label: label(c), em: box(c).width / parseFloat(css(c).fontSize), beside: beside(m, t) });
    }
  }
  if (on('logo-version') && parts.logo) {
    const logo = [...document.querySelectorAll(parts.logo)].map((l) => [l, ...l.querySelectorAll(IMAGE)].filter(drawn)).flat()
      .find((e) => e.matches(IMAGE)) || [...document.querySelectorAll(parts.logo)].find(drawn);
    if (logo) {
      const r = box(logo);
      notes.logo = { variant: `${place.get(logo)} ${logo.currentSrc || logo.getAttribute('href') || ''}`, label: label(logo), aspect: r.width / r.height };
    }
  }
  return { faults, seen: [...seen], notes, unread: [...unread] };
}
"""
)

# The facts the line-length check needs about each block check-measure.py's
# LINES_JS counted, by its place among body's elements: whether it sits in
# several columns, and whether its width tracks the page's as the page widens
# by FILL_PROBE, as a column filling the viewport less its gutters does.
LINE_FACTS_JS = r"""
([at, grow, EDGE]) => {
  const all = [...document.body.querySelectorAll('*')];
  const els = at.map((i) => (i == null ? document.body : all[i]));
  const multi = (el) => { for (let e = el; e && e !== document.body; e = e.parentElement) { const s = getComputedStyle(e); if ((s.columnCount !== 'auto' && +s.columnCount > 1) || s.columnWidth !== 'auto') return true; } return false; };
  const before = els.map((e) => e.getBoundingClientRect().width);
  const root = document.documentElement, was = root.style.width;
  root.style.setProperty('width', `${root.clientWidth + grow}px`, 'important');
  const after = els.map((e) => e.getBoundingClientRect().width);
  root.style.width = was;
  return els.map((e, i) => ({ columns: multi(e), fills: after[i] - before[i] >= grow - EDGE }));
}
"""


def with_label(js, label_js):
    """`js` with check-flow.py's label() in it, LABEL_JS."""
    body = label_js.strip().removeprefix("const label = ").rstrip(";")
    return js.replace("%LABEL%", body)


def line_faults(blocks, facts, v):
    """vault.line-length's faults at one width: each block, by its role, with
    a full line under its floor or any line over its ceiling. `blocks` are
    check-measure.py LINES_JS's, `facts` LINE_FACTS_JS's for them."""
    if not blocks:
        return []
    weight = collections.Counter()
    for b in blocks:
        weight[b["size"]] += sum(len(line["text"]) for line in b["lines"])
    body = weight.most_common(1)[0][0]
    out = []
    for b, f in zip(blocks, facts, strict=True):
        if len(b["lines"]) <= SHORT_LINES:
            role, lo, hi = "a short passage", 0, v["short"]
        elif b["size"] > body + EDGE:
            role, lo, hi = "large text", 0, v["large"]
        elif f["columns"]:
            role, lo, hi = "body text in columns", v["columns_lo"], v["columns_hi"]
        else:
            role, lo, hi = "body text", v["body_lo"], v["body_hi"]
        if f["fills"]:
            lo = 0
        bad = [
            line["text"]
            for line in b["lines"]
            if len(line["text"]) > hi or (line["full"] and len(line["text"]) < lo)
        ]
        if bad:
            lengths = sorted({len(t) for t in bad})
            want = f"{lo:g}–{hi:g}" if lo else f"{hi:g} or fewer"
            out.append(
                {
                    "kind": "line-length",
                    "subject": b["block"],
                    "detail": f"sets lines of {', '.join(map(str, lengths))} characters as {role}, which wants {want}",
                }
            )
    return out


def card_media_faults(found, threshold):
    """vault.card-media-stack's faults at each width, from each width's card
    notes: [(width, [card…])]. A card whose media is beside its text at any
    width is a media object; it must stack under `threshold` em and sit beside
    from it."""
    objects = {c["at"] for _, cards in found for c in cards if c["beside"]}
    out = []
    for width, cards in found:
        faults = []
        for c in cards:
            if c["at"] not in objects:
                continue
            if c["beside"] and c["em"] < threshold:
                faults.append(
                    (
                        c,
                        f"sets its media beside its text at {c['em']:.1f}em wide, under {threshold:g}em",
                    )
                )
            elif not c["beside"] and c["em"] >= threshold:
                faults.append(
                    (
                        c,
                        f"stacks its media above its text at {c['em']:.1f}em wide, from {threshold:g}em it sits beside",
                    )
                )
        out.append(
            (
                width,
                [
                    {"kind": "card-media", "subject": c["label"], "detail": d}
                    for c, d in faults
                ],
            )
        )
    return out


def logo_faults(found):
    """vault.logo-version's faults at each width, from [(width, logo note or
    None)]: the variant with the widest shape is the full logo, and any other
    shown at a width wider than one the full logo is shown at is a fault."""
    shown = [(w, n) for w, n in found if n]
    if not shown:
        return [(w, []) for w, _ in found]
    full = max(shown, key=lambda wn: wn[1]["aspect"])[1]["variant"]
    narrowest = min((w for w, n in shown if n["variant"] == full), default=None)
    out = []
    for width, n in found:
        bad = n and n["variant"] != full and narrowest is not None and width > narrowest
        out.append(
            (
                width,
                [
                    {
                        "kind": "logo-version",
                        "subject": n["label"],
                        "detail": f"shows the mark alone, though the full logo shows at {narrowest} px",
                    }
                ]
                if bad
                else [],
            )
        )
    return out


def fluid_faults(base, zoomed, sized, v, *, slack):
    """vault.fluid-zoom's faults at one width: each viewport-scaled text, as
    {place: [label, px]} at 100%, that zoom by v["zoom"] (`zoomed`, sizes
    already multiplied by the zoom) does not bring to v["grow"] times, or that
    a default text size raised by v["grow"] (`sized`) does not move. `slack` is
    the share short of a factor that px rounding allows."""
    out = []
    for at, (subject, px) in base.items():
        z, s = zoomed.get(at), sized.get(at)
        if z is not None and z[1] / px < v["grow"] * (1 - slack):
            out.append(
                {
                    "kind": "fluid-zoom",
                    "subject": subject,
                    "detail": f"reaches {round(z[1] / px * 100)}% of its {px:g} px at {v['zoom'] * 100:g}% zoom, short of {v['grow'] * 100:g}%",
                }
            )
        elif s is not None and s[1] <= px * (1 + slack):
            out.append(
                {
                    "kind": "fluid-zoom",
                    "subject": subject,
                    "detail": f"stays {px:g} px with the default text size at {v['grow'] * 100:g}%: its bounds are not in rem or em",
                }
            )
    return out


# Each text element set in a viewport unit, or inheriting one, by its place
# among body's elements: [label, font size in px]. A rule's font-size, or a
# font shorthand, in a viewport unit, in a sheet the page can read, under
# media that holds now.
FLUID_JS = (
    r"""
() => {
"""
    + "  const label = "
    + "%LABEL%"
    + r""";
  const VIEW = /\d(?:[sld]?v[whib]|vmin|vmax)\b/;
  const rules = [];
  const collect = (list) => { for (const r of list) { if (r.cssRules && !(r instanceof CSSStyleRule)) { if (!r.media || matchMedia(r.media.mediaText).matches) collect(r.cssRules); } else if (r.selectorText && (VIEW.test(r.style.fontSize) || VIEW.test(r.style.font))) rules.push(r.selectorText); } };
  let unread = 0;
  for (const sh of document.styleSheets) { try { collect(sh.cssRules); } catch (e) { unread += 1; } }
  const all = [...document.body.querySelectorAll('*')];
  const scaled = new Set(rules.flatMap((s) => { try { return [...document.querySelectorAll(s)]; } catch (e) { return []; } }));
  for (const el of all) if (VIEW.test(el.style.fontSize)) scaled.add(el);
  const out = {};
  all.forEach((el, i) => {
    if (![...el.childNodes].some((n) => n.nodeType === 3 && /\S/.test(n.data))) return;
    for (let e = el; e && e !== document.documentElement; e = e.parentElement) if (scaled.has(e)) { out[i] = [label(el), parseFloat(getComputedStyle(el).fontSize)]; return; }
  });
  return { sizes: out, unread };
}
"""
)


# The sizes now of the elements at these places among body's elements.
SIZES_JS = r"""
(at) => { const all = [...document.body.querySelectorAll('*')];
  return Object.fromEntries(at.map((i) => [i, [null, all[i] ? parseFloat(getComputedStyle(all[i]).fontSize) : null]]).filter(([, v]) => v[1] !== null)); }
"""

# With a bottom inset set: each control in a box pinned to the screen's
# bottom that the inset still covers. Read only where the page sets
# viewport-fit=cover, as a phone keeps the page clear of the inset otherwise.
INSET_JS = (
    r"""
([inset, EDGE]) => {
"""
    + "  const label = "
    + "%LABEL%"
    + r""";
  const vh = innerHeight, out = [];
  const meta = [...document.querySelectorAll('meta[name="viewport" i]')].pop();
  if (!meta || !/viewport-fit\s*=\s*cover/i.test(meta.content)) return { seen: false, faults: out };
  let seen = false;
  for (const el of document.body.querySelectorAll('*')) {
    const s = getComputedStyle(el);
    if (s.position !== 'fixed' && s.position !== 'sticky') continue;
    const r = el.getBoundingClientRect();
    if (Math.abs(r.bottom - vh) > EDGE) continue;
    for (const c of el.querySelectorAll('a[href], button, input, select, textarea, [role="button"]')) {
      seen = true;
      const b = c.getBoundingClientRect();
      if (b.height && b.bottom > vh - inset + EDGE) out.push({ kind: 'safe-bottom', subject: label(c), detail: `ends ${Math.round(b.bottom - (vh - inset))} px into the ${inset} px a phone's bottom edge takes, as nothing pads it by env(safe-area-inset-bottom)` });
    }
  }
  return { seen, faults: out };
}
"""
)


# Each tab panel, by its id where it has one, and whether it is drawn with a
# drawn link to it. Script off, it reads the ids it is given.
TABS_JS = r"""
(ids) => {
  const drawn = (el) => el && el.checkVisibility({ opacityProperty: true, visibilityProperty: true }) && el.getBoundingClientRect().height > 0;
  const panels = ids ? ids.map((id) => document.getElementById(id)).filter(Boolean) : [...document.querySelectorAll('[role="tabpanel"]')];
  return panels.map((p) => ({ id: p.id, shown: drawn(p),
    linked: Boolean(p.id) && [...document.querySelectorAll('a[href]')].some((a) => a.getAttribute('href') === `#${p.id}` && drawn(a)) }));
}
"""


def tab_faults(panels, script):
    """vault.tabs-narrow's faults from TABS_JS's panels, read with script on
    or off."""
    out = []
    for p in panels:
        name = f"tab panel #{p['id']}" if p["id"] else "a tab panel"
        why = None if script else ", with script off"
        if not p["shown"]:
            out.append(
                {
                    "kind": "tabs-narrow",
                    "subject": name,
                    "detail": f"is hidden at phone width{why or ''}, not shown as a section",
                }
            )
        elif not p["linked"]:
            out.append(
                {
                    "kind": "tabs-narrow",
                    "subject": name,
                    "detail": f"has no contents link to it{why or ''}",
                }
            )
    return out


# An open overlay's box against the screen: a sheet spans the screen's width
# along its bottom, or fills it.
SHEET_JS = (
    r"""
([el, EDGE]) => {
"""
    + "  const label = "
    + "%LABEL%"
    + r""";
  const r = el.getBoundingClientRect(), vw = document.documentElement.clientWidth, vh = innerHeight;
  return { label: label(el), width: r.width, height: r.height, sheet: r.width >= vw - EDGE && (Math.abs(r.bottom - vh) <= EDGE || r.height >= vh - EDGE) };
}
"""
)


def answers(lines, faults_by_mode, seen, unmet):
    """Each record's answer: fail, not judged, pass or no match, by the
    module docstring. `lines` maps a mode to its Mode, `faults_by_mode` a mode
    to its ranges, `seen` holds the modes that found something, `unmet` maps a
    mode to what the round has not given."""
    by_record = collections.defaultdict(list)
    for mode in lines.values():
        by_record[mode.id].append(mode.name)
    out = {}
    for record, modes in by_record.items():
        out[record] = rule_table.answer(
            any(faults_by_mode.get(m) for m in modes),
            any(m in unmet for m in modes),
            any(m in seen for m in modes),
        )
    return out
