import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402

flow = siblings.load(HERE, "check-flow.py")
maths = siblings.load(HERE, "access-pixels.py")

# G183 asks 3:1 contrast between a link and the text around it:
# https://www.w3.org/WAI/WCAG22/Techniques/general/G183
LINK_RATIO = 3.0
# WCAG 2.5.8 sets a pointer target's minimum at 24 by 24 CSS px:
# https://www.w3.org/TR/WCAG22/#target-size-minimum
MIN_TARGET = 24
BOLD_CUE = 600  # guess, #501
WRAP, WRAPPERS = 12, 3  # guess, #501
FOCUS_REACH = 8  # guess, #501
OPAQUE = 0.9  # guess, #501
# WCAG 2.2.2 covers moving content that starts automatically and lasts more than five seconds:
# https://www.w3.org/TR/WCAG22/#pause-stop-hide
LONG_MS = 5000
PAUSE_TRIES = 6  # guess, #501
# Frames a pause control has to hold still in before it counts as moving (#536): a guess.
PAUSE_FRAMES = 10
# Frames since the page last asked for one in which its frame loop counts as running (#545): a guess.
PAGE_LOOP_FRAMES = 2
ACT_EVENTS = (
    "click",
    "dblclick",
    "mousedown",
    "mouseup",
    "pointerdown",
    "pointerup",
    "touchstart",
    "touchend",
)
REACT_PROPS = (
    "onClick",
    "onDoubleClick",
    "onMouseDown",
    "onMouseUp",
    "onPointerDown",
    "onPointerUp",
    "onTouchStart",
    "onTouchEnd",
)
DATE_PARTS = 6  # measured 6 Tab stops in a datetime-local, #501

CUE_JS = r"""
const css = (el) => getComputedStyle(el);
const badSelectors = (list) => list.filter((s) => { try { document.querySelector(s); return false; } catch (e) { return true; } });
const ink = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
const rgbaCache = new Map();
const rgba = (c) => {
  if (!rgbaCache.has(c)) {
    ink.clearRect(0, 0, 1, 1);
    ink.fillStyle = '#000';
    ink.fillStyle = c;
    ink.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = ink.getImageData(0, 0, 1, 1).data;
    rgbaCache.set(c, [r, g, b, a / 255]);
  }
  return rgbaCache.get(c);
};
const painted = (c) => rgba(c)[3] > 0;
const backdrop = (el) => {
  for (let e = el; e; e = e.parentElement) if (painted(css(e).backgroundColor)) return rgba(css(e).backgroundColor);
  return [255, 255, 255, 1];
};
const shadowed = (s) => s !== 'none' && s.split(/,(?![^(]*\))/).some((layer) => {
  const c = (layer.match(/rgba?\([^)]*\)/) || ['transparent'])[0];
  return painted(c) && /[1-9]/.test(layer.replace(c, ''));
});
const bold = (cs) => parseInt(cs.fontWeight, 10) >= BOLD_CUE;
const italic = (cs) => cs.fontStyle !== 'normal';
const textBesideOf = (a) => {
  const block = blockOf(a);
  for (let e = a.parentElement; e && e !== block; e = e.parentElement)
    if ([...e.childNodes].some((n) => n.nodeType === Node.TEXT_NODE && /\S/.test(n.data))) return e;
  return block;
};
const cued = (a) => {
  const parent = css(textBesideOf(a));
  return [a, ...a.querySelectorAll('*')].some((e) => {
    const cs = css(e);
    return (/underline|overline/.test(cs.textDecorationLine) && painted(cs.textDecorationColor)) ||
      (parseFloat(cs.borderBottomWidth) > 0 && !/none|hidden/.test(cs.borderBottomStyle) && painted(cs.borderBottomColor)) ||
      (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0 && painted(cs.outlineColor)) || shadowed(cs.boxShadow) ||
      (painted(cs.backgroundColor) && backdrop(e).join() !== backdrop(e.parentElement).join()) || cs.backgroundImage !== 'none' ||
      bold(cs) !== bold(parent) || italic(cs) !== italic(parent);
  });
};
const lum = ([r, g, b]) => {
  const lin = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
};
const contrast = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
const DATED = /^(date|datetime-local|month|week|time)$/;
const TARGET = 'a[href], button, input:not([type=hidden]), select, textarea, summary, [onclick], ' +
  '[role=button], [role=link], [role=checkbox], [role=radio], [role=switch], [role=tab], [role=menuitem], ' +
  '[role=option], [tabindex]:not([tabindex="-1"])';
const shown = (el) => {
  for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
    const cs = css(e);
    if (cs.visibility === 'hidden' || cs.visibility === 'collapse' || cs.opacity === '0') return false;
  }
  return true;
};
const opacity = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) o *= parseFloat(css(e).opacity); return o; };
const ancestorsOf = (el) => { const out = []; for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) out.push(e); return out; };
const disabled = (el) => !!el.closest(':disabled, [aria-disabled="true"]');
const box = (r) => [r.left, r.top, r.right, r.bottom];
const meet = (a, b) => [Math.max(a[0], b[0]), Math.max(a[1], b[1]), Math.min(a[2], b[2]), Math.min(a[3], b[3])];
// guess, #501
const DRAWN_PX = 2;
const empty = (r) => r[2] - r[0] < DRAWN_PX || r[3] - r[1] < DRAWN_PX;
const onScreen = (el) => shown(el) && !empty(box(el.getBoundingClientRect()));
const clips = (cs) => cs.overflowX !== 'visible' || cs.overflowY !== 'visible' || cs.clipPath !== 'none' || cs.clip !== 'auto';
const contentBox = (el) => {
  const r = el.getBoundingClientRect(), cs = css(el), px = (k) => parseFloat(cs[k]);
  return [r.left + px('borderLeftWidth') + px('paddingLeft'), r.top + px('borderTopWidth') + px('paddingTop'),
    r.right - px('borderRightWidth') - px('paddingRight'), r.bottom - px('borderBottomWidth') - px('paddingBottom')];
};
const focused = () => {
  let el = document.activeElement;
  while (el && el.shadowRoot && el.shadowRoot.activeElement) el = el.shadowRoot.activeElement;
  return el;
};
const finished = (animations) => {
  for (const a of animations) {
    try { if (a.effect.getComputedTiming().endTime !== Infinity) a.finish(); } catch (e) {}
  }
};
const settled = async () => {
  finished(document.getAnimations());
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
};
const blockOf = (el) => {
  for (let e = el; e; e = e.parentElement) { const d = css(e).display; if (d !== 'inline' && d !== 'contents') return e; }
  return document.body;
};
const inText = (el) => {
  if (css(el).display !== 'inline') return false;
  const block = blockOf(el);
  const around = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
  for (let n = around.nextNode(); n; n = around.nextNode()) {
    if (/\S/.test(n.data) && !n.parentElement.closest(TARGET) && blockOf(n.parentElement) === block) return true;
  }
  return false;
};
// guess, #501
const FINDABLE = 0.5;
const pointerTargets = (skip) => [...document.querySelectorAll(TARGET)].filter((el) => {
  if (!shown(el) || disabled(el) || skip(el)) return false;
  const r = el.getBoundingClientRect();
  return r.width >= FINDABLE && r.height >= FINDABLE && r.right > 0 && r.bottom > 0;
});
// #421
const restingStops = () => {
  const root = document.documentElement;
  const onPage = [-scrollX, -scrollY, root.scrollWidth - scrollX, root.scrollHeight - scrollY];
  const drawnOnPage = (el) => !empty(meet(box(el.getBoundingClientRect()), onPage));
  const shownByFocus = (el) => {
    el.focus({ preventScroll: true });
    finished(el.getAnimations({ subtree: true }));
    const on = drawnOnPage(el);
    el.blur();
    finished(el.getAnimations({ subtree: true }));
    return on;
  };
  const atRest = (el) => {
    const r = box(el.getBoundingClientRect());
    return (r[2] - r[0] < DRAWN_PX && r[3] - r[1] < DRAWN_PX) || (!drawnOnPage(el) && shownByFocus(el));
  };
  return [...document.querySelectorAll(TARGET)]
    .filter((el) => el.tabIndex >= 0 && el.getClientRects().length && shown(el) && !disabled(el) && atRest(el));
};
const visiblePart = (el, r) => {
  for (let e = el; e && e !== document.body && e !== document.documentElement;) {
    const cs = css(e);
    if (clips(cs)) r = meet(r, box(e.getBoundingClientRect()));
    if (cs.position === 'fixed') break;
    let p = e.parentElement;
    if (cs.position === 'absolute') while (p && p !== document.body && css(p).position === 'static') p = p.parentElement;
    e = p;
  }
  return r;
};
"""


def page_js(body):
    consts = (
        f"const MIN_TARGET = {MIN_TARGET}, PX_SLACK = {maths.PX_SLACK}, BOLD_CUE = {BOLD_CUE}, WRAP = {WRAP}, "
        f"LINK_RATIO = {LINK_RATIO}, WRAPPERS = {WRAPPERS}, FOCUS_REACH = {FOCUS_REACH}, LONG_MS = {LONG_MS}, "
        f"REWRITE_FRAMES = {flow.REWRITE_FRAMES}, REWRITE_SPAN_MS = {flow.REWRITE_SPAN_MS}, PAUSE_TRIES = {PAUSE_TRIES}, PAUSE_FRAMES = {PAUSE_FRAMES}, PAGE_LOOP_FRAMES = {PAGE_LOOP_FRAMES}, "
        f"OPAQUE = {OPAQUE}, DATE_PARTS = {DATE_PARTS}, ACT_EVENTS = {json.dumps(ACT_EVENTS)}, REACT_PROPS = {json.dumps(REACT_PROPS)};\n"
    )
    return consts + CUE_JS + body


def labelled_js(body):
    return page_js(flow.LABEL_JS + body)
