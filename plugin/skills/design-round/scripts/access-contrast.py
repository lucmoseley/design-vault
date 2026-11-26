import collections
import functools
import io
import os
import sys
import re

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402


answering = siblings.load(HERE, "access-answers.py")
keys = siblings.load(HERE, "access-keys.py")
maths = siblings.load(HERE, "access-pixels.py")
face = siblings.load(HERE, "face-profile.py")
rule_table = siblings.load(HERE, "rule-table.py")

TABLE = os.path.join(HERE, "check-access-contrast.table")
SEP = "|"
LINES = {
    ("vault.contrast", "text"): 2,
    ("vault.contrast", "large"): 3,
    ("vault.control-edges", "edge"): 1,
    ("vault.contrast-ladder", "icon"): 1,
    ("vault.contrast-ladder", "state"): 1,
    ("vault.contrast-ladder", "thin"): 2,
    ("vault.contrast-ladder", "aim"): 2,
    ("vault.contrast-ladder", "more"): 1,
    ("vault.controls-on-photo", "edge"): 1,
    ("vault.fill-text", "split"): 1,
    ("vault.fill-text", "gap"): 2,
    ("vault.chart-contrast", "mark"): 1,
    ("vault.text-tint", "hued"): 1,
}
NUMBER = re.compile(r"\d+(?:\.\d+)?")

Table = collections.namedtuple(
    "Table",
    "floors edge icon state thin_stem thin_weight aim more photo split gap gap_large mark hued",
)

QUESTIONS = (
    "vault.controls-on-photo",
    "vault.contrast-ladder",
    "vault.fill-text",
    "vault.chart-contrast",
    "vault.forced-colours-edge",
)
SCHEMES = (("dark", {"color_scheme": "dark"}), ("more contrast", {"contrast": "more"}))

RING_PX = 3  # guess, #501
MAX_SLIDES = 12  # guess, #427
HUE_SAME = 30  # guess, #501
ADJ_PX = 2  # guess, #501
ID_BLUE = 167  # guess, #501


TableError = rule_table.TableError


def parse_table(text):
    got = {}
    for n, line in rule_table.lines(text):
        fields = [f.strip() for f in line.split(SEP)]
        key = tuple(fields[:2])
        if len(fields) != 3 or key not in LINES:
            known = ", ".join(f"{r} | {name}" for r, name in LINES)
            raise TableError(
                f"line {n}: want one of {known}, then | numbers, got {line!r}"
            )
        if key in got:
            raise TableError(f"line {n}: a second {key[0]} | {key[1]} line")
        values = [v.strip() for v in fields[2].split(",")]
        if len(values) != LINES[key] or not all(NUMBER.fullmatch(v) for v in values):
            raise TableError(
                f"line {n}: {key[0]} | {key[1]} wants {LINES[key]} number(s) over 0, got {fields[2]!r}"
            )
        numbers = [float(v) for v in values]
        if min(numbers) <= 0:
            raise TableError(
                f"line {n}: {key[0]} | {key[1]} wants numbers over 0, got {fields[2]!r}"
            )
        got[key] = numbers
    missing = [f"{r} | {name}" for r, name in LINES if (r, name) not in got]
    if missing:
        raise TableError(f"no {', '.join(missing)} line")
    body, large = got["vault.contrast", "text"]
    large_px, large_bold_px, bold = got["vault.contrast", "large"]
    gap, gap_large = got["vault.fill-text", "gap"]
    stem, weight = got["vault.contrast-ladder", "thin"]
    return Table(
        maths.Floors(body, large, large_px, large_bold_px, bold),
        got["vault.control-edges", "edge"][0],
        got["vault.contrast-ladder", "icon"][0],
        got["vault.contrast-ladder", "state"][0],
        stem,
        weight,
        maths.Floors(
            *got["vault.contrast-ladder", "aim"], large_px, large_bold_px, bold
        ),
        got["vault.contrast-ladder", "more"][0],
        got["vault.controls-on-photo", "edge"][0],
        got["vault.fill-text", "split"][0],
        gap,
        gap_large,
        got["vault.chart-contrast", "mark"][0],
        got["vault.text-tint", "hued"][0],
    )


def scheme_table(name, table):
    if name == "more contrast":
        more = table.more
        return table._replace(
            floors=table.aim, edge=more, icon=more, state=more, photo=more, mark=more
        )
    return table


Reading = collections.namedtuple("Reading", "subject role ratio")
_ROLES = (
    "text",
    "large text",
    "control edge",
    "icon",
    "state mark",
    "control on a photo",
    "chart mark",
)


def _role_rungs(role, table):
    return {
        "text": (table.floors.body, table.aim.body),
        "large text": (table.floors.large, table.aim.large),
        "control edge": (table.edge, table.more),
        "icon": (table.icon, table.more),
        "state mark": (table.state, table.more),
        "control on a photo": (table.photo, table.more),
        "chart mark": (table.mark, table.more),
    }[role]


def rung(ratio, role, table):
    floor, top = _role_rungs(role, table)
    ladder = {r for each in _ROLES for r in _role_rungs(each, table)}
    cleared = [r for r in ladder if floor <= r <= ratio]
    return min(max(cleared), top) if cleared else None


def _worst(readings):
    out = {}
    for r in readings:
        key = r.subject, r.role
        out[key] = min(out.get(key, r.ratio), r.ratio)
    return out


def rung_drops(light, dark, table):
    lit, dim = _worst(light), _worst(dark)
    out = []
    for key, was in lit.items():
        if key not in dim:
            continue
        now = dim[key]
        held, onto = rung(was, key[1], table), rung(now, key[1], table)
        if onto < held:
            out.append(
                {
                    "subject": key[0],
                    "detail": f"in the dark scheme, is {now:.2f}:1, down from {was:.2f}:1 on the light page: off the "
                    f"{held:g}:1 rung it holds there, onto {onto:g}:1 (vault.contrast-ladder)",
                }
            )
    return out


STRIP_JS = """
() => document.querySelectorAll('[data-contrast-glyph], [data-contrast-box], [data-contrast-chart]').forEach(
  (el) => ['data-contrast-glyph', 'data-contrast-box', 'data-contrast-chart'].forEach((a) => el.removeAttribute(a)))
"""

STAY_ON_PAGE_JS = """
() => {
  addEventListener('click', (e) => {
    const a = e.target.closest && e.target.closest('a[href]');
    if (a && a.href.split('#')[0] !== location.href.split('#')[0]) e.preventDefault();
  }, true);
  addEventListener('submit', (e) => e.preventDefault(), true);
}
"""
KEEP_DECKS_JS = "() => { window.__contrastDecks = window.__contrastCarousels; }"
PRESS_JS = """
([n, k]) => {
  const c = window.__contrastDecks[n], el = k === null ? c.next : c.dots[k];
  if (!el.isConnected || !shown(el) || disabled(el)) return null;
  const at = [scrollX, scrollY];
  el.click();
  return at;
}
"""
BACK_JS = "([x, y]) => scrollTo({ left: x, top: y, behavior: 'instant' })"
SLIDE_SHOWN_JS = r"""
(e, limit) => {
  const o = e.getBoundingClientRect();
  return [e, ...e.querySelectorAll('*')].slice(0, limit).map((d) => {
    const r = d.getBoundingClientRect(), s = getComputedStyle(d);
    return [r.left - o.left, r.top - o.top, r.width, r.height].map(Math.round).join(',')
      + `,${s.opacity},${s.visibility},${d.currentSrc || ''},${s.backgroundImage}`;
  }).join(';');
}
"""

STRAY_CHART_PX = 48  # guess, #501
STRAY_CHART_MARKS = 3  # guess, #501

MARK_JS = r"""
({ charts, carousels, undeclared, STRAY_CHART_PX, STRAY_CHART_MARKS }) => {
  const bad = [...charts, ...carousels].filter((s) => { try { document.querySelector(s); return false; } catch (e) { return true; } });
  if (bad.length) return { bad };
  const CONTROL = 'a[href], button, summary, input[type=button], input[type=submit], input[type=reset], [role=button], [role=link], [role=tab]';
  const SIDES = ['Top', 'Right', 'Bottom', 'Left'];
  const drawnSide = (cs, s) => parseFloat(cs[`border${s}Width`]) > 0 && !/none|hidden/.test(cs[`border${s}Style`]);
  const rectOf = (el) => visiblePart(el, box(el.getBoundingClientRect()));
  const range = document.createRange();
  const drawsText = (el) => {
    if (el.localName === 'input') return /\S/.test(el.value || '');
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      if (!/\S/.test(n.data) || !shown(n.parentElement)) continue;
      range.selectNodeContents(n);
      if ([...range.getClientRects()].some((r) => !empty(visiblePart(n.parentElement, box(r))))) return true;
    }
    return false;
  };
  const icons = (el) => [...el.querySelectorAll('svg, img')].filter((e) => !e.parentElement.closest('svg') && shown(e) && !empty(rectOf(e)));
  const under = (el) => {
    const r = el.getBoundingClientRect(), x = (r.left + r.right) / 2, y = (r.top + r.bottom) / 2;
    const holds = (e) => { const q = e.getBoundingClientRect(); return q.left <= x && x <= q.right && q.top <= y && y <= q.bottom; };
    for (let a = el.parentElement; a; a = a.parentElement) {
      const media = [...a.querySelectorAll('img, video, canvas')].find((m) => !el.contains(m) && !m.contains(el) && shown(m) && holds(m));
      if (media) return media.localName === 'img' ? 'image' : media.localName;
      const cs = css(a);
      if (/url\(/.test(cs.backgroundImage)) return 'image';
      if (rgba(cs.backgroundColor)[3] >= OPAQUE) return null;
    }
    return null;
  };

  const photo = [], iconOnly = [];
  for (const el of document.querySelectorAll(CONTROL)) {
    if (!shown(el) || disabled(el)) continue;
    const rect = rectOf(el);
    if (empty(rect)) continue;
    const ground = under(el);
    const bare = !drawsText(el) && icons(el).length > 0;
    if (bare) {
      el.setAttribute('data-contrast-glyph', '');
      iconOnly.push({ subject: label(el), rect });
    }
    if (!ground) continue;
    if (ground !== 'image') {
      photo.push({ subject: label(el), why: `lies over a ${ground}, which a script draws` });
      continue;
    }
    const cs = css(el);
    const kind = painted(cs.backgroundColor) || cs.backgroundImage !== 'none' ? 'fill'
      : SIDES.some((s) => drawnSide(cs, s) && painted(cs[`border${s}Color`])) ? 'border' : null;
    el.setAttribute('data-contrast-glyph', '');
    if (kind) el.setAttribute('data-contrast-box', kind);
    photo.push({ subject: label(el), rect, box: !!kind, why: null });
  }

  const dotRows = (root) => {
    const rows = new Map();
    for (const el of root.querySelectorAll(CONTROL)) {
      if (!shown(el) || empty(rectOf(el)) || drawsText(el) || icons(el).length) continue;
      const up = el.parentElement, row = up.children.length === 1 && up.parentElement ? up.parentElement : up;
      if (!rows.has(row)) rows.set(row, []);
      rows.get(row).push(el);
    }
    return [...rows].filter(([, row]) => row.length >= 2);
  };
  const dots = [];
  const KEYS = ['backgroundColor', 'backgroundImage', 'width', 'height', 'borderTopLeftRadius', 'borderTopColor', 'borderTopWidth', 'borderTopStyle', 'boxShadow', 'transform', 'outlineStyle'];
  for (const sel of carousels) for (const c of document.querySelectorAll(sel)) {
    for (const [parent, row] of dotRows(c)) {
      const looks = row.map((el) => { const cs = css(el); return KEYS.map((k) => cs[k]).join('|'); });
      if (new Set(looks).size > 1) continue;
      const faded = new Set(row.map((el) => opacity(el))).size > 1;
      dots.push({ subject: label(parent), detail: faded
        ? `holds ${row.length} page dots that differ by opacity alone, so the current one is a faint change; mark it by fill, size or shape`
        : `holds ${row.length} page dots drawn alike, so none shows the current page; mark it by fill, size or shape` });
    }
  }
  const unnumbered = (el) => (el.getAttribute('aria-label') || el.title || '').replace(/\d+/g, '').trim().toLowerCase();
  const glyph = (el) => ['::before', '::after'].some((p) => !/^(none|normal|""|'')$/.test(getComputedStyle(el, p).content));
  const strayDots = !undeclared.carousel ? [] : dotRows(document)
    .filter(([, row]) => new Set(row.map(unnumbered)).size === 1 && !row.some(glyph))
    .map(([parent, row]) => ({ subject: label(parent), count: row.length }));
  const nameOf = (el) => (el.getAttribute('aria-label') || el.title || el.textContent || el.value || '').trim();
  const step = /\b(prev|previous|next|back|forward)\b|^\s*[‹›←→<>]\s*$/i, ahead = /\b(next|forward)\b|^\s*[›→>]\s*$/i;
  window.__contrastCarousels = [];
  const slides = [];
  for (const sel of carousels) for (const c of document.querySelectorAll(sel)) {
    const row = dotRows(c).map(([, r]) => r).find((r) => !r.some((e) => step.test(nameOf(e)))) || [];
    const next = row.length ? null : [...c.querySelectorAll(CONTROL)].find((e) => shown(e) && !disabled(e) && ahead.test(nameOf(e))) || null;
    window.__contrastCarousels.push({ el: c, dots: row, next });
    const media = [c, ...c.querySelectorAll('*')].some((e) => ['img', 'video', 'canvas'].includes(e.localName)
      || /url\(/.test(getComputedStyle(e).backgroundImage));
    slides.push({ subject: label(c), dots: row.length, next: !!next, media });
  }

  const states = [];
  window.__contrastStates = [];
  for (const el of document.querySelectorAll('input[type=checkbox], input[type=radio], [role=checkbox], [role=radio], [role=switch]')) {
    if (disabled(el)) continue;
    const native = el.localName === 'input';
    if (native && el.type === 'radio' && !el.checked) continue;
    const own = rectOf(el);
    const drawn = shown(el) && !empty(own);
    let rect = null;
    if (drawn && (!native || css(el).appearance === 'none')) rect = own;
    else if (native && !drawn) {
      const ls = [...(el.labels || [])].filter(shown).map(rectOf).filter((r) => !empty(r));
      if (ls.length) rect = ls.reduce((a, b) => [Math.min(a[0], b[0]), Math.min(a[1], b[1]), Math.max(a[2], b[2]), Math.max(a[3], b[3])]);
    }
    if (!rect) continue;
    states.push({ subject: label(el), rect });
    window.__contrastStates.push({ el, checked: native ? el.checked : el.getAttribute('aria-checked') });
  }

  const fillOf = (el) => {
    for (let e = el; e; e = e.parentElement) {
      const cs = css(e);
      if (cs.backgroundImage !== 'none') return null;
      const c = rgba(cs.backgroundColor);
      if (c[3] > 0) return c[3] >= OPAQUE ? { el: e, c } : null;
    }
    return null;
  };
  const SHAPES = 'path, rect, circle, ellipse, line, polyline, polygon';
  const solid = (p) => p !== 'none' && !/url\(/.test(p);
  const fills = [];
  for (const el of document.body.querySelectorAll('*')) {
    if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'TITLE', 'OPTION'].includes(el.tagName)) continue;
    const icon = el.localName === 'svg' && !el.parentElement.closest('svg');
    if (charts.some((sel) => el.closest(sel))) continue;
    if (!icon && (el.closest('svg') || ![...el.childNodes].some((n) => n.nodeType === 3 && /\S/.test(n.data)))) continue;
    if (!shown(el) || disabled(el) || empty(rectOf(el))) continue;
    const f = fillOf(el);
    if (!f) continue;
    const cs = css(el);
    let paint;
    if (icon) {
      const ground = f.c.slice(0, 3).join();
      paint = [...el.querySelectorAll(SHAPES)].map(css).flatMap((s) => [s.fill, s.stroke]).filter(solid).map(rgba)
        .find((c) => c[3] > 0 && c.slice(0, 3).join() !== ground);
      if (!paint) continue;
    } else paint = rgba(rgba(cs.webkitTextFillColor)[3] > 0 ? cs.webkitTextFillColor : cs.color);
    fills.push({ subject: label(el), text: [...paint.slice(0, 3), paint[3] * opacity(el) / opacity(f.el)], fill: f.c.slice(0, 3),
      size: parseFloat(cs.fontSize), weight: parseInt(cs.fontWeight, 10), icon, rect: rectOf(el) });
  }

  const chartsOut = [];
  window.__contrastMarks = [];
  const withAlpha = (c, a) => [...c.slice(0, 3), c[3] * a];
  for (const sel of charts) for (const c of document.querySelectorAll(sel)) {
    if (!shown(c)) continue;
    if (c.matches('canvas, img') || c.querySelector('canvas, img')) {
      chartsOut.push({ subject: label(c), why: 'is drawn on a canvas or as an image, so its marks have no paint to read', marks: [] });
      continue;
    }
    const marks = [], patterned = [];
    for (const m of c.querySelectorAll('*')) {
      if (!shown(m)) continue;
      const cs = css(m), o = opacity(m);
      let fill = null, stroke = null;
      if (m.closest('svg')) {
        if (!m.matches(SHAPES) || m.closest('defs, clipPath, mask, marker, pattern, symbol')) continue;
        if (cs.fill !== 'none') fill = solid(cs.fill) ? withAlpha(rgba(cs.fill), parseFloat(cs.fillOpacity) * o) : 'pattern';
        if (cs.stroke !== 'none' && parseFloat(cs.strokeWidth) > 0) stroke = solid(cs.stroke) ? withAlpha(rgba(cs.stroke), parseFloat(cs.strokeOpacity) * o) : 'pattern';
      } else {
        if (m.children.length || /\S/.test(m.textContent)) continue;
        if (cs.backgroundImage !== 'none') fill = 'pattern';
        else if (painted(cs.backgroundColor)) fill = withAlpha(rgba(cs.backgroundColor), o);
        const side = SIDES.find((s) => drawnSide(cs, s) && painted(cs[`border${s}Color`]));
        if (side) stroke = withAlpha(rgba(cs[`border${side}Color`]), o);
      }
      if (!fill && !stroke) continue;
      if (fill === 'pattern' || stroke === 'pattern') { patterned.push(label(m)); continue; }
      marks.push({ el: m, subject: label(m), fill, stroke, rect: box(m.getBoundingClientRect()) });
    }
    const holdsAll = (k) => marks.length > 1 && marks.every((o, j) => j === k ||
      (marks[k].rect[0] <= o.rect[0] && marks[k].rect[1] <= o.rect[1] && marks[k].rect[2] >= o.rect[2] && marks[k].rect[3] >= o.rect[3]));
    const kept = marks.filter((_, k) => !holdsAll(k));
    c.setAttribute('data-contrast-chart', '');
    const first = window.__contrastMarks.length;
    window.__contrastMarks.push(...kept.map((m) => ({ el: m.el, fill: !!m.fill, stroke: !!m.stroke })));
    chartsOut.push({ subject: label(c), why: null, rect: box(c.getBoundingClientRect()), patterned,
      marks: kept.map((m, k) => ({ index: first + k, subject: m.subject, fill: m.fill, stroke: m.stroke })) });
  }
  const strayCharts = [];
  if (undeclared.chart) for (const el of document.querySelectorAll('canvas, svg')) {
    if (el.parentElement.closest('svg') || !shown(el) || el.closest('[aria-hidden=true], [role=presentation], [role=none]')) continue;
    const r = rectOf(el);
    if (Math.max(r[2] - r[0], r[3] - r[1]) <= STRAY_CHART_PX) continue;
    const drawn = (q) => [...el.querySelectorAll(q)].filter((m) => !m.closest('defs, clipPath, mask, marker, pattern, symbol'));
    if (el.localName === 'canvas' || drawn('polyline').length || drawn('path, rect, line, circle, ellipse, polygon').length >= STRAY_CHART_MARKS) strayCharts.push(label(el));
  }

  const resting = restingStops();
  const forced = [];
  window.__contrastForced = [];
  for (const el of document.querySelectorAll(CONTROL + ', [role=switch], [role=option]')) {
    if (!shown(el) || disabled(el) || empty(rectOf(el)) || resting.some((r) => r.contains(el))) continue;
    const cs = css(el);
    if (SIDES.every((s) => drawnSide(cs, s) && painted(cs[`border${s}Color`]))) continue;
    const ground = backdrop(el.parentElement).slice(0, 3).join();
    const by = shadowed(cs.boxShadow) ? 'a shadow' : /gradient\(/.test(cs.backgroundImage) ? 'a gradient'
      : painted(cs.backgroundColor) && rgba(cs.backgroundColor).slice(0, 3).join() !== ground ? 'its fill' : null;
    if (!by) continue;
    forced.push({ subject: label(el), by });
    window.__contrastForced.push(el);
  }
  return { photo, iconOnly, dots, strayDots, slides, states, fills, charts: chartsOut, strayCharts, forced };
}
"""

GLYPH_CSS = """
[data-contrast-glyph], [data-contrast-glyph] *, [data-contrast-glyph] *::before, [data-contrast-glyph] *::after,
[data-contrast-glyph]::before, [data-contrast-glyph]::after {{
  -webkit-text-fill-color: {fill} !important; text-shadow: none !important;
}}
[data-contrast-glyph] svg, [data-contrast-glyph] img {{ filter: brightness(0){invert} !important; }}
"""
BOX_CSS = """
[data-contrast-box=fill] {{ background-color: {fill} !important; background-image: none !important; border-color: {fill} !important; }}
[data-contrast-box=border] {{ border-color: {fill} !important; }}
"""

STATE_JS = r"""
(back) => {
  for (const { el, checked } of window.__contrastStates) {
    if (el.localName === 'input') el.checked = back ? checked : !checked;
    else if (back) checked === null ? el.removeAttribute('aria-checked') : el.setAttribute('aria-checked', checked);
    else el.setAttribute('aria-checked', checked === 'true' ? 'false' : 'true');
  }
}
"""

MARKS_JS = r"""
(mode) => {
  const id = (n) => `rgb(${(n + 1) & 255}, ${((n + 1) >> 8) & 255}, ID_BLUE)`;
  window.__contrastMarks.forEach((m, k) => {
    if (mode === null) {
      m.style === undefined || m.style === null ? m.el.removeAttribute('style') : m.el.setAttribute('style', m.style);
      return;
    }
    m.style = m.el.getAttribute('style');
    const s = m.el.style, set = (p, v) => s.setProperty(p, v, 'important');
    if (mode === 'hide') return set('visibility', 'hidden');
    const svg = !!m.el.closest('svg');
    if (m.fill) set(svg ? 'fill' : 'background-color', id(2 * k));
    if (m.stroke) set(svg ? 'stroke' : 'border-color', id(2 * k + 1));
    for (const p of svg ? ['fill-opacity', 'stroke-opacity', 'opacity'] : ['opacity']) set(p, '1');
    set('filter', 'none');
    if (svg) set('shape-rendering', 'crispEdges');
    else { set('background-image', 'none'); set('box-shadow', 'none'); }
  });
}
""".replace("ID_BLUE", str(ID_BLUE))
CHART_CSS = "[data-contrast-chart], [data-contrast-chart] * { opacity: 1 !important; }"

FORCED_JS = r"""
() => window.__contrastForced.map((el) => {
  const cs = css(el);
  const sides = ['Top', 'Right', 'Bottom', 'Left'].every((s) => parseFloat(cs[`border${s}Width`]) > 0 && !/none|hidden/.test(cs[`border${s}Style`]));
  return sides || (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0);
})
"""

SETTINGS_JS = r"""
() => window.__texts.map(({ el }) => {
  const cs = css(el);
  return [cs.fontFamily, parseFloat(cs.fontSize), parseFloat(cs.fontWeight), cs.fontStyle, cs.fontStretch];
})
"""

SIGNATURE_JS = r"""
() => [document.documentElement, ...document.querySelectorAll('body, body *')].map((el) => {
  const s = css(el);
  return [s.color, s.backgroundColor, s.backgroundImage, s.borderTopColor, s.borderRightColor, s.borderBottomColor,
    s.borderLeftColor, s.outlineColor, s.fill, s.stroke, s.boxShadow].join(' ');
}).join('|')
"""


def _decoded(png):
    return np.asarray(Image.open(io.BytesIO(png)).convert("RGB"))


def _shoot(page):
    return _decoded(page.screenshot(full_page=True, animations="disabled"))


def _recoloured(page, css):
    out = []
    for fill, invert in (("rgb(0, 0, 0)", ""), ("rgb(255, 255, 255)", " invert(1)")):
        style = page.add_style_tag(content=css.format(fill=fill, invert=invert))
        out.append(_shoot(page))
        style.evaluate("(el) => el.remove()")
    black, white = out
    if black.shape != white.shape:
        return None
    return (black != white).any(axis=-1)


def _clip(shape, rect, pad=0):
    h, w = shape[:2]
    left, top = max(int(round(rect[0])) - pad, 0), max(int(round(rect[1])) - pad, 0)
    right, bottom = min(int(round(rect[2])) + pad, w), min(int(round(rect[3])) + pad, h)
    return left, top, max(right, left), max(bottom, top)


def _dilate(mask, r):
    if r <= 0:
        return mask
    view = np.lib.stride_tricks.sliding_window_view(
        np.pad(mask, r), (2 * r + 1, 2 * r + 1)
    )
    return view.any(axis=(-2, -1))


Figure = collections.namedtuple("Figure", "ratio colour next")


def glyph_figure(drawn, glyph, rect):
    pad = maths.BLEND_PX + RING_PX
    left, top, right, bottom = _clip(drawn.shape, rect, pad)
    inner = np.zeros((bottom - top, right - left), dtype=bool)
    il, it, ir, ib = _clip(drawn.shape, rect)
    inner[it - top : ib - top, il - left : ir - left] = True
    g = glyph[top:bottom, left:right] & inner
    if not g.any():
        return None
    ring = (
        _dilate(g, pad) & ~_dilate(g, maths.BLEND_PX) & ~glyph[top:bottom, left:right]
    )
    if not ring.any():
        return None
    window = drawn[top:bottom, left:right].astype(float)
    near, own = window[ring], window[g]
    colour = own[int(np.argmax(maths.contrast(own, np.median(near, axis=0))))]
    ratios = maths.contrast(colour, near)
    i = int(np.argmin(ratios))
    return Figure(float(ratios[i]), colour, near[i])


def box_figure(drawn, painted, taken, rect):
    pad = maths.BLEND_PX + RING_PX
    left, top, right, bottom = _clip(drawn.shape, rect, pad)
    il, it, ir, ib = _clip(drawn.shape, rect)
    near_box = np.zeros((bottom - top, right - left), dtype=bool)
    nl, nt, nr, nb = _clip(drawn.shape, rect, maths.BLEND_PX)
    near_box[nt - top : nb - top, nl - left : nr - left] = True
    inner = np.zeros_like(near_box)
    inner[it - top : ib - top, il - left : ir - left] = True
    own = painted[top:bottom, left:right] & inner
    ring = ~near_box & ~taken[top:bottom, left:right]
    if not own.any() or not ring.any():
        return None
    window = drawn[top:bottom, left:right].astype(float)
    colour = np.median(window[own], axis=0)
    near = window[ring]
    ratios = maths.contrast(colour, near)
    i = int(np.argmin(ratios))
    return Figure(float(ratios[i]), colour, near[i])


def state_figure(on, off, rect):
    left, top, right, bottom = _clip(on.shape, rect)
    a = on[top:bottom, left:right].astype(int)
    b = off[top:bottom, left:right].astype(int)
    changed = (np.abs(a - b) > maths.PAINT_NOISE).any(axis=-1)
    if not changed.any():
        return None
    return float(np.median(maths.contrast(a[changed], b[changed])))


def _linear(rgb):
    c = np.asarray(rgb, dtype=float) / 255
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def oklch(rgb):
    r, g, b = _linear(rgb)
    lms = np.cbrt(
        np.array(
            [
                0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b,
                0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b,
                0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b,
            ]
        )
    )
    lab = (
        np.array(
            [
                [0.2104542553, 0.7936177850, -0.0040720468],
                [1.9779984951, -2.4285922050, 0.4505937099],
                [0.0259040371, 0.7827717662, -0.8086757660],
            ]
        )
        @ lms
    )
    return (
        float(lab[0]),
        float(np.hypot(lab[1], lab[2])),
        float(np.degrees(np.arctan2(lab[2], lab[1])) % 360),
    )


def fill_drawn(shot, entry):
    left, top, right, bottom = _clip(shot.shape, entry["rect"])
    if right <= left or bottom <= top:
        return False
    median = np.median(
        shot[top:bottom, left:right].reshape(-1, 3).astype(float), axis=0
    )
    return bool(
        np.abs(median - np.array(entry["fill"], dtype=float)).max() <= maths.PAINT_NOISE
    )


def fill_fault(entry, table):
    *rgb, alpha = entry["text"]
    fill = np.array(entry["fill"], dtype=float)
    seen = alpha * np.array(rgb, dtype=float) + (1 - alpha) * fill
    y_fill, y_text = float(maths.luminance(fill)), float(maths.luminance(seen))
    what = "icon" if entry["icon"] else "text"
    if y_fill < table.split and y_text <= y_fill:
        return (
            f"is dark {what} ({maths.hexed(seen)}) on a fill of luminance {y_fill:.3f} ({maths.hexed(fill)}); "
            f"a fill under {table.split:g} takes light {what}"
        )
    if y_fill >= table.split and y_text >= y_fill:
        return (
            f"is light {what} ({maths.hexed(seen)}) on a fill of luminance {y_fill:.3f} ({maths.hexed(fill)}); "
            f"a fill at {table.split:g} or over takes dark {what}"
        )
    (lt, ct, ht), (lf, cf, hf) = oklch(seen), oklch(fill)
    turn = abs(ht - hf) % 360
    if ct >= table.hued and cf >= table.hued and min(turn, 360 - turn) <= HUE_SAME:
        big = entry["icon"] or maths.large(entry["size"], entry["weight"], table.floors)
        need = table.gap_large if big else table.gap
        if abs(lt - lf) < need:
            return (
                f"is {what} in its fill's own hue ({maths.hexed(seen)} on {maths.hexed(fill)}) only "
                f"{abs(lt - lf):.2f} apart in OKLCH lightness; {need:g} needed"
            )
    return None


def _ids(shot):
    s = shot.astype(int)
    n = s[..., 0] + 256 * s[..., 1] - 1
    return np.where((s[..., 2] == ID_BLUE) & (n >= 0), n, -1)


def chart_faults(chart, ids_shot, ground, table):
    left, top, right, bottom = _clip(ids_shot.shape, chart["rect"], 1)
    ids = _ids(ids_shot[top:bottom, left:right])
    ground_px = ground[top:bottom, left:right].astype(float)
    ids[
        (ids_shot[top:bottom, left:right] == ground[top:bottom, left:right]).all(
            axis=-1
        )
    ] = -1
    marks = {m["index"]: m for m in chart["marks"]}
    owner, part = ids // 2, ids % 2
    owner[ids < 0] = -1
    out, readings = [], []
    for k, mark in marks.items():
        filled = mark["fill"] is not None
        region = (owner == k) & (part == (0 if filled else 1))
        if not region.any():
            continue
        paint = np.array(mark["fill"] if filled else mark["stroke"], dtype=float)
        behind = np.median(ground_px[region], axis=0)
        colour = paint[3] * paint[:3] + (1 - paint[3]) * behind
        edge = _dilate(region, 1) & ~region
        nexts = []
        bare = edge & (owner < 0)
        if bare.sum() >= ADJ_PX:
            ratios = maths.contrast(colour, ground_px[bare])
            i = int(np.argmin(ratios))
            nexts.append((float(ratios[i]), "the chart's ground", ground_px[bare][i]))
        if filled:
            for j in np.unique(owner[edge & (owner >= 0)]):
                other = marks.get(int(j))
                for p in (0, 1):
                    touch = edge & (owner == j) & (part == p)
                    if touch.sum() < ADJ_PX or other is None:
                        continue
                    if p == 0 and j != k and other["fill"] is not None:
                        paint_j, what = other["fill"], other["subject"]
                    elif p == 1 and (j == k or other["fill"] is not None):
                        paint_j = other["stroke"]
                        what = (
                            "its own border"
                            if j == k
                            else f"the border of {other['subject']}"
                        )
                    else:
                        continue
                    pj = np.array(paint_j, dtype=float)
                    seen = pj[3] * pj[:3] + (1 - pj[3]) * behind
                    nexts.append((float(maths.contrast(colour, seen)), what, seen))
        if not nexts:
            continue
        ratio, what, seen = min(nexts, key=lambda t: t[0])
        if ratio < table.mark:
            out.append(
                {
                    "subject": mark["subject"],
                    "detail": f"is {ratio:.2f}:1 ({maths.hexed(colour)}) against {what} ({maths.hexed(seen)}) next "
                    f"to it; {table.mark:g}:1 needed",
                }
            )
        else:
            readings.append(Reading(mark["subject"], "chart mark", ratio))
    return out, readings


def _thin_notes(page, js, table, texts):
    got, shots = texts
    readable = [t for t in got["texts"] if not t["logotype"] and not t["why"]]
    if not readable:
        return []
    stems = {}
    if any(t["weight"] >= table.thin_weight for t in readable):
        for s in face.profile(page):
            stems[s["family"], s["size"], s["weight"], s["style"], s["stretch"]] = s[
                "stem"
            ]
    settings = page.evaluate(js(SETTINGS_JS))
    notes = []
    for text, setting in zip(got["texts"], settings, strict=True):
        if text["logotype"] or text["why"]:
            continue
        stem = stems.get(tuple(setting))
        thin = text["weight"] < table.thin_weight or (
            stem is not None and stem < table.thin_stem
        )
        if not thin:
            continue
        shot, ink = shots.clear if text["under"] else (shots.shot, shots.ink)
        if maths.text_contrast(shot, ink, text, table.floors, held=shots.held)[0]:
            continue
        missed, _ = maths.text_contrast(shot, ink, text, table.aim, held=shots.held)
        if missed:
            why = (
                f"weight {text['weight']}"
                if text["weight"] < table.thin_weight
                else f"stem {stem:.3f} em"
            )
            notes.append(
                f"{text['subject']}, a thin face ({why}), aims higher: it {missed.replace('needed', 'aimed at')}"
            )
    return notes


def _mark(page, js, parts, absent):
    page.evaluate(STRIP_JS)
    return page.evaluate(
        js(MARK_JS),
        {
            "charts": [parts["chart"]] if "chart" in parts else [],
            "carousels": [parts["carousel"]] if "carousel" in parts else [],
            "undeclared": {
                p: p not in parts and p not in absent for p in ("chart", "carousel")
            },
            "STRAY_CHART_PX": STRAY_CHART_PX,
            "STRAY_CHART_MARKS": STRAY_CHART_MARKS,
        },
    )


Shots = collections.namedtuple("Shots", "drawn glyph boxed taken")


def _shots(page, photo):
    drawn = _shoot(page)
    glyph = _recoloured(page, GLYPH_CSS)
    boxed = _recoloured(page, BOX_CSS) if any(c.get("box") for c in photo) else None
    if (
        glyph is None
        or glyph.shape != drawn.shape[:2]
        or (boxed is not None and boxed.shape != drawn.shape[:2])
    ):
        return None
    return Shots(drawn, glyph, boxed, glyph | (boxed if boxed is not None else False))


def _photo_reading(c, shots):
    if c["why"]:
        return c["why"]
    figures = [
        f
        for f in (
            glyph_figure(shots.drawn, shots.glyph, c["rect"]),
            box_figure(shots.drawn, shots.boxed, shots.taken, c["rect"])
            if c["box"]
            else None,
        )
        if f
    ]
    if not figures:
        return "shows no glyph or edge the check can find"
    return max(figures, key=lambda f: f.ratio)


def _photo_readings(photo, shots):
    return [(c["subject"], _photo_reading(c, shots)) for c in photo]


def _press(page, js, handle, *, deck, dot):
    at = page.evaluate(js(PRESS_JS), [deck, dot])
    if at is None:
        return None
    settled = keys.still(handle)
    page.evaluate(BACK_JS, at)
    return settled


def _slide_pass(fresh, js, parts, absent):
    from playwright.sync_api import Error as PlaywrightError

    readings, unread = [], []
    deck_page = None
    try:
        deck_page = fresh()
        _slide_readings(
            deck_page,
            js,
            functools.partial(_mark, deck_page, js, parts, absent),
            readings=readings,
            unread=unread,
        )
    except PlaywrightError as err:
        first = (str(err).strip().splitlines() or [""])[0]
        unread.append(
            "the declared carousel's slides could not be stepped through, so its slides past those already read "
            f"were not read ({type(err).__name__}: {first})"
        )
    finally:
        if deck_page is not None:
            deck_page.close()
    return readings, unread


def _slide_readings(page, js, mark, *, readings, unread):
    page.evaluate(STAY_ON_PAGE_JS)

    def read(subject, where, held):
        if not held:
            unread.append(
                f"{subject} never held still {where}, so that slide was not read"
            )
            return
        photo = mark()["photo"]
        shots = _shots(page, photo) if photo else None
        if photo and shots is None:
            unread.append(
                f"the page changed size between its shots {where}, so its controls were not read"
            )
        else:
            readings.append((where, _photo_readings(photo, shots)))

    decks = mark()["slides"]
    page.evaluate(KEEP_DECKS_JS)
    for n, deck in enumerate(decks):
        if not deck["media"]:
            continue
        subject = deck["subject"]
        handle = page.evaluate_handle(
            "(n) => window.__contrastDecks[n].el", n
        ).as_element()
        if deck["dots"]:
            count = min(deck["dots"], MAX_SLIDES)
            for k in range(count):
                held = _press(page, js, handle, deck=n, dot=k)
                if held is None:
                    unread.append(
                        f"{subject}'s page dot {k + 1} was gone, hidden or disabled when pressed, so its slide was "
                        "not read"
                    )
                    continue
                read(subject, f"on {subject}'s slide {k + 1} of {deck['dots']}", held)
            if deck["dots"] > count:
                unread.append(
                    f"{subject} holds {deck['dots']} page dots, so its slides past {count} were not read"
                )
        elif deck["next"]:
            seen = {handle.evaluate(SLIDE_SHOWN_JS, keys.WATCH_LIMIT)}
            for pressed in range(1, MAX_SLIDES + 1):
                where = (
                    f"on {subject}'s slide {pressed + 1}, reached by its next button"
                )
                held = _press(page, js, handle, deck=n, dot=None)
                if held is None:
                    break
                if not held:
                    read(subject, where, False)
                    break
                shows = handle.evaluate(SLIDE_SHOWN_JS, keys.WATCH_LIMIT)
                if shows in seen:
                    if pressed == 1:
                        unread.append(
                            f"{subject} showed no new slide when its next button was pressed, so only the slide it "
                            "shows at load was read"
                        )
                    break
                seen.add(shows)
                read(subject, where, True)
            else:
                unread.append(
                    f"{subject} still showed a new slide after {MAX_SLIDES} presses of its next button, so its later "
                    "slides were not read"
                )
        else:
            unread.append(
                f"{subject} shows no page dots or next button the check can press, so only the slide it shows at load "
                "was read"
            )


def _photo_verdict(photo, readings, table):
    passed = []
    by = {}
    for where, got in readings:
        for subject, reading in got:
            by.setdefault(subject, []).append((where, reading))
    for subject, seen in by.items():
        reasons = {}
        for where, reading in seen:
            if isinstance(reading, str):
                reasons.setdefault(reading, where)
        photo.unmeasured.extend(
            f"{subject} {why}" + (f", {where}" if where else "")
            for why, where in reasons.items()
        )
        figures = [(where, r) for where, r in seen if isinstance(r, Figure)]
        if not figures:
            continue
        where, worst = min(figures, key=lambda wf: wf[1].ratio)
        if worst.ratio < table.photo:
            photo.faults.append(
                {
                    "subject": subject,
                    "detail": f"sits on a photo and shows {worst.ratio:.2f}:1 at best"
                    + (f" {where}" if where else "")
                    + f" ({maths.hexed(worst.colour)} against {maths.hexed(worst.next)} next to it); "
                    f"{table.photo:g}:1 needed, by a backdrop, halo or shadow of its own",
                }
            )
        else:
            passed.append(Reading(subject, "control on a photo", worst.ratio))
    return passed


def measure(page, js, table, *, parts, absent, texts, fresh):
    readings, on_photo = [], []
    out = {qid: answering.unjudged() for qid in (*QUESTIONS, "vault.carousel-focus")}
    got = _mark(page, js, parts, absent)
    if "bad" in got:
        return got, readings
    photo, ladder, fills, chart_q, forced = (
        out[q]
        for q in (
            "vault.controls-on-photo",
            "vault.contrast-ladder",
            "vault.fill-text",
            "vault.chart-contrast",
            "vault.forced-colours-edge",
        )
    )
    photo.faults.extend(got["dots"])
    for d in got["strayDots"]:
        for q, left in (
            (photo, "its current dot was"),
            (
                out["vault.carousel-focus"],
                "its rotation, Tab order, slides out of view and previous and next buttons were",
            ),
        ):
            q.unmeasured.append(
                f"{d['subject']} holds {d['count']} controls that draw no text or icon, which may be a carousel's "
                f"page dots, but no carousel was declared, so {left} not judged; name it as carousel in --parts, "
                "or as null where the page has none"
            )
    chart_q.unmeasured.extend(
        f"{s} may be a chart, but no chart was declared, so its marks were not read; name it as chart in --parts, or "
        "as null where the page has none"
        for s in got["strayCharts"]
    )

    glyphs = got["photo"] + got["iconOnly"]
    if glyphs:
        shots = _shots(page, got["photo"])
        if shots is None:
            for q in (photo, ladder):
                q.unmeasured.append(
                    "the page changed size between its shots of controls, so their glyphs were not read"
                )
        else:
            on_photo.append((None, _photo_readings(got["photo"], shots)))
            for c in got["iconOnly"]:
                f = glyph_figure(shots.drawn, shots.glyph, c["rect"])
                if f is None:
                    ladder.unmeasured.append(
                        f"{c['subject']} shows no icon the check can find"
                    )
                elif f.ratio < table.icon:
                    ladder.faults.append(
                        {
                            "subject": c["subject"],
                            "detail": f"is named by its icon alone, at {f.ratio:.2f}:1 ({maths.hexed(f.colour)} against "
                            f"{maths.hexed(f.next)} next to it); {table.icon:g}:1 needed",
                        }
                    )
                else:
                    readings.append(Reading(c["subject"], "icon", f.ratio))

    if got["states"]:
        on = _shoot(page)
        page.evaluate(js(STATE_JS), False)
        off = _shoot(page)
        page.evaluate(js(STATE_JS), True)
        for s in got["states"]:
            ratio = state_figure(on, off, s["rect"]) if on.shape == off.shape else None
            if ratio is None:
                ladder.unmeasured.append(
                    f"{s['subject']} drew no change when its state was flipped, so its state mark was not found"
                )
            elif ratio < table.state:
                ladder.faults.append(
                    {
                        "subject": s["subject"],
                        "detail": f"marks its state by a change of {ratio:.2f}:1 between checked and unchecked; "
                        f"{table.state:g}:1 needed",
                    }
                )
            else:
                readings.append(Reading(s["subject"], "state mark", ratio))

    if texts is not None:
        ladder.notes.extend(_thin_notes(page, js, table, texts))

    ground = _shoot(page) if got["fills"] else None
    for entry in got["fills"]:
        if not fill_drawn(ground, entry):
            continue
        detail = fill_fault(entry, table)
        if detail:
            fills.faults.append({"subject": entry["subject"], "detail": detail})

    measured_charts = [c for c in got["charts"] if not c["why"]]
    for c in got["charts"]:
        if c["why"]:
            chart_q.unmeasured.append(f"{c['subject']} {c['why']}")
        for m in c.get("patterned", []):
            chart_q.unmeasured.append(
                f"{m} in {c['subject']} is painted with a gradient or pattern, so its colour is not one"
            )
    if any(c["marks"] for c in measured_charts):
        style = page.add_style_tag(content=CHART_CSS)
        page.evaluate(js(MARKS_JS), "id")
        ids_shot = _shoot(page)
        page.evaluate(js(MARKS_JS), None)
        style.evaluate("(el) => el.remove()")
        page.evaluate(js(MARKS_JS), "hide")
        ground = _shoot(page)
        page.evaluate(js(MARKS_JS), None)
        for c in measured_charts:
            if ids_shot.shape != ground.shape:
                chart_q.unmeasured.append(
                    f"{c['subject']} changed size between its shots"
                )
                continue
            faults, read = chart_faults(c, ids_shot, ground, table)
            chart_q.faults.extend(faults)
            readings.extend(read)

    if got["forced"]:
        page.emulate_media(forced_colors="active")
        try:
            edged = page.evaluate(js(FORCED_JS))
        finally:
            page.emulate_media(forced_colors="none")
        for c, ok in zip(got["forced"], edged, strict=True):
            if not ok:
                forced.faults.append(
                    {
                        "subject": c["subject"],
                        "detail": f"shows its edge by {c['by']} alone, which forced colours take off, and draws no "
                        "border all round or outline for them to paint; give it a transparent one",
                    }
                )
    page.evaluate(STRIP_JS)

    if any(d["media"] for d in got["slides"]):
        more, unread = _slide_pass(fresh, js, parts, absent)
        on_photo += more
        photo.unmeasured.extend(unread)
    readings += _photo_verdict(photo, on_photo, table)
    return out, readings


def signature(page, js):
    return page.evaluate(js(SIGNATURE_JS))


def scheme(name, judged, measured, light):
    out = answering.unjudged()
    for qid in ("vault.contrast", "vault.control-edges", *QUESTIONS):
        found = measured[qid] if qid in QUESTIONS else judged[qid]
        known = {f["subject"] for f in light[qid].faults}
        out.faults.extend(
            {
                "subject": f["subject"],
                "detail": f"in the {name} scheme, {f['detail']} ({qid})",
            }
            for f in found.faults
            if f["subject"] not in known
        )
        out.unmeasured.extend(
            f"in the {name} scheme, {u}"
            for u in found.unmeasured
            if u not in light[qid].unmeasured
        )
    return out
