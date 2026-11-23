#!/usr/bin/env python3
"""check-access.py — measures a web candidate against the access rule records
in design-critique's rules/ that a script answers (design-vault#163, #164, #189, #200, #315, #316):
WCAG 2.2 AA text contrast (1.4.3), control edges (1.4.11), target size
(2.5.8), links told apart by colour alone (1.4.1, by technique G183), reach
by keyboard (2.1.1), focus shown and not hidden (2.4.7, 2.4.11), a pause
for long motion (2.2.2), the contrast questions access-contrast.py reads:
the contrast ladder, controls on a photo, text on a fill, chart marks, edges
under forced colours, and each colour scheme the page ships, and the keyboard
and focus questions access-keys.py reads: a skip link, source order,
scrolling boxes, composite widgets, menus, a declared carousel, and how focus
rings are drawn, coloured and triggered.

USAGE
  python3 check-access.py <url or file> --out DIR [--logotype SELECTOR]… [--parts FILE]
        [--contrast-table FILE] [--timeout MS]
  python3 check-access.py <url or file> --out DIR --pointer [--pointer-table FILE] [--timeout MS]

It loads the page at check-layout.py's desktop and phone widths, the latter
with a touch screen, lets its fonts load and its animations finish as
check-layout.py does, and measures each question at both:

- vault.contrast: every line of text, each ::before and ::after whose content
  holds text, and each form control's value, button label, chosen option or
  placeholder, against what is drawn behind it, read
  from a screenshot taken with the text made invisible, so a photo, gradient
  or overlapping box counts as it is drawn. Only the pixels a glyph covers are
  read, found by drawing the text black and then white, and the worst of them
  is the figure, as WCAG F83 asks of the background behind each letter. On a
  page whose size changes between those shots, even when they are taken
  again, each text's whole box is read, and a note says so. A
  line in the text's own colour crossing it, up to 3 px thick, such as a rule
  or an underline drawn under the letters, is left out of that background.
  Text a fixed or sticky box shorter than the window lies over at load, a
  header or booking bar, is read from shots with each such box hidden, as a
  visitor scrolls it clear, and a note names it, where some scroll shows it
  clear of the box; a video or canvas inside such a box does not stop it being
  read. Text no scroll clears, such as a header's first lines or a short page's
  last under a bottom bar, and text inside a fixed or sticky box are read as
  drawn. Text in a Tab stop hidden at rest, as a skip link is, in a box under
  2 px each way or laid off the page until focus brings it on, is read as it
  shows once focused, from window shots with the window scrolled to it; its
  generated text cannot be measured (#421).
  4.5:1 is needed, or 3:1 for large text, 24 px or 18.66 px bold (WCAG's
  18 pt and 14 pt). Text in a disabled control is exempt, and text under a
  --logotype selector, a logotype the project's rules file names, which WCAG
  exempts: it is reported as exempt where it would fail or go unmeasured.
  Text over a video or canvas, text filled with a background image, text whose
  fill the page holds with its own !important rule, SVG text and generated
  text whose box the browser does not give cannot be measured;
- vault.control-edges: each text field, text area and select box, and each
  checkbox, radio or switch the page draws itself (`appearance: none`, or an
  ARIA role), must show its edge at 3:1 against what is behind it, read from a
  shot with the control hidden, so a neighbour's edge flush against it does
  not count as its own. Its edge is read one side at a time, the 2 px outside
  the box and the 3 px inside it, a line at a time, and its fill too; the best
  of these is the figure. Where the control draws no edge or fill, a box drawn
  close around it, holding no other control, is read as its edge. A control
  with no edge drawn at all passes, since WCAG asks 3:1 only of an edge that
  is drawn: whether it looks like a field is a function question's. A disabled
  control is exempt. A control on or beside something a script moves, such
  as a video or canvas, cannot be measured;
- vault.target-size: every link, button, form control or element with a
  click handler or a tab stop is measured. One under 24x24 px passes only by
  WCAG's spacing exception: no other target within 12 px of its centre, and no
  other undersized one's centre within 24 px. Exempt are links set in running
  text, a Tab stop hidden at rest in a box under 2 px each way or off the
  page until focus brings it on, and, by WCAG's user-agent exception, a
  form control at the size the browser gives a copy of it in a blank frame;
- vault.colour-script: a link inside a block of text that holds text of its
  own, outside any block nested in it, must differ from that text by more than
  colour (an underline or overline, a bottom border, an outline or shadow in a
  colour that shows, a background other than the one behind it, bold against
  regular, italic against upright) or reach 3:1 against it. No cue on hover or
  focus is asked: G183 dropped that step in 2021 (w3c/wcag#1553), and a phone
  has no hover;
- vault.contrast-ladder: a link or button named by its icon alone, drawing
  no text, must show the icon at the table's icon figure against the colours
  next to it, read up to access-contrast.py's RING_PX px past its antialiased edge in a shot as
  drawn, the icon found by drawing it black and then white; a checkbox, radio
  or switch the page draws itself (or its label, where the input is hidden)
  must change by the state figure between checked and unchecked, the median
  over the pixels that change. Text in a thin face, a weight or a stem
  (face-profile.py) under the table's, that passes vault.contrast but not the
  ladder's aim is noted, not failed;
- vault.controls-on-photo: a link or button drawn over a photo, an <img> or a
  url() background with no opaque box between, must show its glyph (its text
  and icons) against the colours next to it, or its own fill or border against
  those outside it, at the table's figure, so its own backdrop, halo or shadow
  counts and the image's worst pixel beside it decides. One over a video or
  canvas cannot be measured. In the declared carousel, a row of two or more
  controls drawing no text or icon, its page dots, must hold one that differs
  by more than opacity. With no carousel declared, each such row on the page
  whose names match but for a number ("Slide 1", "Slide 2", or none) cannot
  be measured, and its reason says no carousel was declared;
- vault.fill-text: text and icons on an opaque fill of one colour take a light
  colour on a fill under the table's luminance split and a dark one at or
  above it, and a partner in the fill's own hue (both at the table's OKLCH chroma
  for a hue or more, within its HUE_SAME degrees) sits the table's gap apart in OKLCH
  lightness, its large gap for large text and icons;
- vault.chart-contrast: in the declared chart, each SVG shape or childless
  HTML box painted with a fill or a stroke is read in a shot painting each in
  colours of its own: a filled mark against the ground, the stroke round it
  and every filled mark beside it, a line only against the ground, at the
  table's figure. The box holding every other mark is the plot's ground. A
  chart on a canvas or image, or a mark painted with a gradient or pattern,
  cannot be measured. With no chart declared, each canvas, and each outermost
  SVG holding a polyline or three or more paths, rects, lines, circles,
  ellipses or polygons, longer than an icon and not hidden as decoration,
  cannot be measured, and its reason says no chart was declared; which marks a visitor needs is vault.chart-carried's;
- vault.forced-colours-edge: a control told from its ground by nothing but a
  shadow, a gradient or a fill, drawing no border on all four sides,
  must draw a border all round or an outline once forced colours are on;
- vault.theme-contrast: the page is loaded again in a dark scheme and under
  prefers-contrast: more, and each one that changes any colour the page draws
  is measured as the light page is, for vault.contrast, vault.control-edges
  and the questions above, text held to the ladder's aim line under more
  contrast; each fault there is this question's;
- vault.keyboard: Tab walks the page from its top to its end, then Shift+Tab
  walks it back. Every part a pointer can work must take
  focus: a link, button, form control or ARIA widget, or an element with a
  click, press or touch handler of its own (React's included). A part counts
  as reached when it, a part it holds or the control holding it took focus,
  or one of its radio group or composite widget did, or another link to the
  same address did. A handler a page sets on the document for many parts is
  not seen;
- vault.focus: at each forward stop, once its transitions end, the window is
  shot focused, then blurred, twice over; a pixel that differs between the two
  shots of one state moves by itself and is left out, with every pixel within
  STILL_MARGIN px of it. Pixels on the part and on up to WRAPPERS wrappers
  holding no other tab stop, or FOCUS_REACH px around any of them, that change
  by 3:1 or more are its indicator, which must cover a 1 px line along the
  part's longer side. A control hidden for a screen reader is judged on its
  label, or else the nearest wrapper that shows. A part with something opaque
  over it at every one of nine points is hidden under that, named by its fixed
  or sticky box, whatever its ring shows. Back with Shift+Tab, only that is
  judged, as a sticky header hides a part scrolled to the window's top. A
  change of colour alone counts: whether colour is the only signal is the
  colour questions'. Focus inside a frame whose page this one can read is
  walked there and judged where the frame shows it; inside one it cannot
  read, another site's, it is judged only at the frame, which must show and
  lie under nothing, as a page cannot style a frame that holds focus;
- vault.pause: on a fresh load, each animation running from the start whose
  active span is over 5 s, and each video playing that loops or runs over
  5 s without its own controls, fails unless a button, switch or checkbox
  named for pausing, stopping or hiding it stops it when clicked. Such an
  animation that ends before the check could try a control, or while it
  tries them, an element
  a script moves frame by frame, and a canvas, image or SVG whose pixels
  change across WATCH_MS without an animation the browser lists, cannot be
  measured; nor can a carousel that changes slides less often than that;
- vault.skip-link: where a Tab stop outside the main element comes before it,
  the first stop, past any in a dialog or a fixed or sticky cookie or consent
  banner, must link to the main element or something in it, and show whole in
  the window when focused. A page with navigation and no main element cannot
  be measured;
- vault.visual-order: no tab stop has a positive tabindex, and where a box's
  children are moved by `order`, a reversed flex direction or wrap, grid
  placement, dense grid flow, or a child holding a tab stop positioned
  absolutely, those holding a tab stop or text (only a tab stop for an
  absolute child) must show in rows, read in the page's direction, in their
  source order. A fixed or sticky child, or one off the page, is left out;
- vault.scroller-focus: a box that scrolls and holds nothing the Tab key
  reaches must have tabindex="0", role="region" and a name. Chrome makes such
  a box focusable by itself; other browsers do not, so the markup is read;
- vault.roving-focus: a tab list, radio group, toolbar, listbox, grid, tree
  grid, tree or menu bar takes one Tab stop, entered on its selected, checked
  or pressed item, else its first, unless the widget itself takes focus; on a
  fresh load, its arrow key (Right, or Down for a listbox, radio group, tree
  or tree grid, or as aria-orientation says) must move focus, or
  aria-activedescendant, to another of its items. A chip set or segmented
  control with none of these roles is not found;
- vault.menu-focus: each menu drive-overlay.py finds a button opening, on a
  fresh load: Enter opens it with focus on its first item, Down Arrow moves to
  the next, Escape shuts it and gives focus back to the button, Tab shuts it,
  and Up Arrow, where it opens it, opens it on its last item;
- vault.carousel-focus: for each carousel the --parts declaration names, no
  Tab stop, and no text outside inert or aria-hidden, lies outside the
  carousel's box at load, as on a slide out of view, and its rotation control, a button named pause, stop, play, start or resume,
  is its first stop. On a fresh load, a carousel whose pixels change within
  ROTATE_MS, timed from one slide to the next, must hold still for that span
  and STILL_SLACK_MS more while focus is in it and while the pointer is over
  it, and focus must stay on its previous and next buttons when Enter presses
  them. One that never holds still between slides cannot be measured. With
  no carousel declared, each row of page dots vault.controls-on-photo finds
  cannot be measured, and its reason says no carousel was declared;
- vault.ring-outline: at each forward stop, where focus changes how the part,
  its label or a wrapper is drawn, an outline must be among the changes, or a
  transparent outline drawn on focus behind a shadow ring; a change of
  box-shadow, border or background alone fails;
- vault.focus-colour-kept: every focus ring is drawn in one colour, and no
  link's text, nor any button's or selected, current, pressed or checked
  item's fill or edge, is drawn in it, black, white and greys (channels
  within CHROMA of each other) aside. Its hover and brand colours are
  vault.focus-colour's;
- vault.focus-visible: a stop vault.focus finds showing nothing whose outline
  is none had the browser's ring taken off. At desktop width, on a fresh
  load, a button a rule styles on :focus, one for each set of such rules (one
  for each class list where a style sheet cannot be read), clicked with the
  mouse with its click kept from the page, must draw no outline or shadow it
  did not draw at rest, and a text field, one of each class list, clicked into
  must draw some change.

The walked questions read the page's own Tab stops, not those inside a frame,
and a note says where focus entered one.

--pointer answers vault.coarse-target alone, into DIR/pointer.json: each
target's size under a coarse and a fine pointer at both widths, by
access-pointer.py, with its coarse floor read from check-access-pointer.table
beside this script or --pointer-table FILE. It reads neither --parts nor
--contrast-table.

Each question's answer is "pass", "fail" or "cannot measure"; a question
that cannot be measured goes to the look critics (#154). Pure decoration is
exempt from contrast but still reported: say so beside it in the round folder.

It writes DIR/access.json, every question's answer with each finding,
exemption and note and the widths it holds at, deleting any an earlier run left there.

--parts is the building session's parts declaration, {"declared": {<part>:
<its CSS selector, or null>}}, naming the declared chart and carousel; null
declares the page has none. Its carousel is also the one vault.carousel-focus judges.
--contrast-table, check-access-contrast.table by default, gives every contrast
figure.

EXITS 0 every question passes / 1 a fault (each printed) / 2 the arguments are
wrong, a --logotype or --parts selector that is no CSS selector, a --parts file
that is not a declaration and a --contrast-table or --pointer-table line it
cannot run included / 3 Playwright, its browser, numpy or Pillow is missing / 4
the page did not render in time / 5 the browser refused the page / 6 no fault,
but a question cannot be measured / 7 a call hung that would never return. Exits
0, 1 and 6 print on stdout; the rest print on stderr.
"""

import argparse
import collections
import datetime
import importlib.util
import io
import itertools
import json
import os
import pathlib
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sibling(name):
    """The module in the file `name` beside this script."""
    spec = importlib.util.spec_from_file_location(
        name[:-3].replace("-", "_"), os.path.join(HERE, name)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


layout = sibling("check-layout.py")
flow = layout.flow
try:
    import numpy as np
    from PIL import Image
except ImportError as err:
    sys.exit(flow.missing(err))
maths = sibling("access-pixels.py")
answering = sibling("access-answers.py")
pseudo_boxes = sibling("access-boxes.py")
keys = sibling("access-keys.py")
contrasts = sibling("access-contrast.py")
pointing = sibling("access-pointer.py")
conditions = sibling("conditions.py")

VIEWPORTS = tuple(
    (name, width, layout.height_at(width, layout.HEIGHTS))
    for name, width in (
        ("desktop", layout.DESKTOP_WIDTH),
        ("phone", layout.PHONE_WIDTH),
    )
)
# G183's 3:1 between a link and the text around it.
LINK_RATIO = 3.0
# WCAG 2.5.8's target, in px.
MIN_TARGET = 24
# The weight a link counts as bold at against regular text around it: G183
# names bold as a cue but gives no figure, and 600 is CSS's semibold.
BOLD_CUE = 600
# How much taller than a control, in px a side, a wrapper drawn around it as
# its field may be, and how many wrappers out are read. Guesses, unmeasured.
WRAP, WRAPPERS = 12, 3
# How far outside a focused element a ring drawn around it is read, in px. A
# guess, unmeasured: past a 2 px ring at a 3 px offset, with room to spare.
FOCUS_REACH = 8
# A cover whose background is at least this opaque hides what is under it; a
# lighter one is judged by the pixels. A guess, unmeasured.
OPAQUE = 0.9
# WCAG 2.2.2's five seconds.
LONG_MS = 5000
# How long the motion check watches a script's motion, and how many controls
# named for pausing it clicks. Guesses, unmeasured.
WATCH_MS = 1000
PAUSE_TRIES = 6
# How long a click on one of those controls may wait for it to take a click.
# A guess, unmeasured: a control that is there to be clicked takes one at once.
PAUSE_CLICK_MS = 2000
# Event types that make an element act on a pointer, and React's props for them.
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
# Tab stops a walk may take, past twice the focusable elements of the page
# and of each frame it enters, for the stops a shadow root adds. A guess,
# unmeasured.
WALK_SLACK = 20
# The Tab stops a date or time input takes, one a part, at most: a
# datetime-local's month, day, year, hour, minute and AM/PM (#188).
DATE_PARTS = 6

MEASURE_JS = (
    flow.LABEL_JS
    + r"""
(LOGOTYPES) => {
  const bad = badSelectors(LOGOTYPES);
  if (bad.length) return { bad };
  // The --logotype selector text sits under.
  const logotype = (el) => LOGOTYPES.find((s) => el.closest(s)) || null;
  const ancestors = (el) => { const out = []; for (let e = el; e; e = e.parentElement) out.push(e); return out; };
  // The colour a text's glyphs are filled with, its alpha times `opacity`.
  const fillOf = (cs, opacity) => {
    const color = rgba(cs.webkitTextFillColor && rgba(cs.webkitTextFillColor)[3] > 0 ? cs.webkitTextFillColor : cs.color);
    return [...color.slice(0, 3), color[3] * opacity];
  };
  // Whether any of these computed styles fills text with its background.
  const clipped = (styles) => styles.some((s) => /text/.test(s.backgroundClip || s.webkitBackgroundClip));
  const FIELD = /^(text|email|search|tel|url|password|number|date|datetime-local|month|week|time)$/;

  // FOCUSED_JS reads the text of the Tab stops hidden at rest.
  const resting = (window.__resting = restingStops());
  const restingIn = (el) => resting.some((r) => r.contains(el));

  // Text under `top`, one entry per element holding it, past those `skip` takes.
  const textsIn = (top, skip) => {
    const replaced = [...document.querySelectorAll('video, canvas')].filter(shown).map((e) => box(e.getBoundingClientRect()));
    const texts = new Map();
    const walker = document.createTreeWalker(top, NodeFilter.SHOW_TEXT);
    const range = document.createRange();
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const el = n.parentElement;
      if (!/\S/.test(n.data) || !el || ['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'TITLE', 'OPTION', 'TEXTAREA'].includes(el.tagName)) continue;
      if (!shown(el) || disabled(el) || skip(el)) continue;
      range.selectNodeContents(n);
      const rects = [...range.getClientRects()].map((r) => visiblePart(el, box(r))).filter((r) => !empty(r));
      if (!rects.length) continue;
      if (!texts.has(el)) {
        const cs = css(el);
        const size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight, 10);
        let why = null;
        if (el.closest('svg')) why = 'is SVG text';
        else if (clipped(ancestors(el).map(css))) why = 'is filled with a background';
        texts.set(el, { subject: label(el), color: fillOf(cs, opacity(el)), size, weight, why, logotype: logotype(el), rects: [] });
      }
      const t = texts.get(el);
      t.rects.push(...rects);
      if (!t.why && rects.some((r) => replaced.some((v) => !empty(meet(r, v))))) t.why = 'lies over a video or canvas';
    }

    // A form control's own text: its value, a button's label, a select's
    // choice, or else its placeholder, read across its content box.
    const OWN = 'input:not([type=hidden]), textarea, select';
    for (const el of [top, ...top.querySelectorAll(OWN)].filter((e) => e.matches(OWN))) {
      if (!shown(el) || disabled(el) || skip(el)) continue;
      const kind = el.localName === 'input' ? el.type : el.localName;
      if (el.localName === 'input' && !FIELD.test(kind) && !/^(submit|reset|button)$/.test(kind)) continue;
      const value = el.localName === 'select' ? (el.selectedOptions[0] || {}).text || '' : el.value;
      const hint = !/\S/.test(value) && /\S/.test(el.placeholder || '');
      if (!hint && !/\S/.test(value)) continue;
      const cs = css(el), ts = hint ? getComputedStyle(el, '::placeholder') : cs;
      const content = visiblePart(el, contentBox(el));
      if (empty(content)) continue;
      const color = rgba(ts.color);
      texts.set(el, { subject: label(el) + (hint ? ' placeholder' : ''), color: [...color.slice(0, 3), color[3] * opacity(el)],
        size: parseFloat(ts.fontSize), weight: parseInt(ts.fontWeight, 10), why: null, logotype: logotype(el), rects: [content] });
    }
    return texts;
  };
  const texts = textsIn(document.body, restingIn);
  window.__restingTexts = (i) => [...textsIn(resting[i], () => false).values()];
  window.__texts = [...texts].map(([el, t]) => ({ el, rects: t.rects }));

  // Generated text: a ::before or ::after whose content, up to any alt text
  // after a slash, holds a string that is not blank, a counter, an attribute
  // or a quote mark. Its boxes come from access-boxes.py, so it waits in
  // window.__generated for GENERATED_JS.
  const TOKEN = /"(?:[^"\\]|\\.)*"|[\w-]+\((?:[^()"]|"(?:[^"\\]|\\.)*")*\)|\/|[\w-]+/g;
  const holdsText = (content) => {
    for (const [t] of content.matchAll(TOKEN)) {
      if (t === '/') return false;
      if (t[0] === '"' ? /\S/.test(t.slice(1, -1)) : /^(counters?\(|attr\(|open-quote$|close-quote$)/.test(t)) return true;
    }
    return false;
  };
  window.__generated = [];
  // Generated text in a Tab stop hidden at rest, which FOCUSED_JS does not read.
  const unread = [];
  for (const el of [document.body, ...document.body.querySelectorAll('*')]) {
    if (el.closest('svg') || !shown(el) || disabled(el)) continue;
    for (const pseudo of ['::before', '::after']) {
      const cs = getComputedStyle(el, pseudo);
      if (!holdsText(cs.content) || cs.display === 'none' || cs.visibility !== 'visible' || cs.opacity === '0') continue;
      if (restingIn(el)) {
        unread.push(label(el, pseudo));
        continue;
      }
      window.__generated.push({ el, pseudo, text: { subject: label(el, pseudo), pseudo: pseudo.slice(2),
        color: fillOf(cs, parseFloat(cs.opacity) * opacity(el)), size: parseFloat(cs.fontSize), weight: parseInt(cs.fontWeight, 10),
        why: clipped([cs, ...ancestors(el).map(css)]) ? 'is filled with a background' : null, logotype: logotype(el), rects: [] } });
    }
  }

  // Controls whose edge identifies them, each with the boxes drawn around it
  // that could be its edge: its own, then up to WRAPPERS wrappers holding no other
  // control and no taller than it by more than WRAP px a side.
  const ROLES = '[role=checkbox], [role=radio], [role=switch]';
  const CONTROL = `input:not([type=hidden]), select, textarea, button, a[href], ${ROLES}`;
  const controls = [];
  // Each control's element and wrappers, box by box, for HIDE_JS.
  window.__boxEls = [];
  for (const el of document.querySelectorAll(`input, textarea, select, ${ROLES}`)) {
    if (!shown(el) || disabled(el)) continue;
    const kind = el.localName === 'input' ? el.type : el.localName;
    const own = (kind === 'checkbox' || kind === 'radio') && css(el).appearance === 'none';
    if (el.localName === 'input' && !FIELD.test(kind) && !own) continue;
    const r = box(el.getBoundingClientRect());
    if (empty(r)) continue;
    const boxes = [{ subject: label(el), rect: r }], els = [el];
    for (let w = el.parentElement; w && w !== document.body && boxes.length <= WRAPPERS; w = w.parentElement) {
      const wr = box(w.getBoundingClientRect());
      if (w.querySelectorAll(CONTROL).length > 1 || wr[3] - wr[1] > r[3] - r[1] + 2 * WRAP) break;
      boxes.push({ subject: label(w), rect: wr });
      els.push(w);
    }
    controls.push(boxes);
    window.__boxEls.push(els);
  }

  // WCAG 2.5.8's user-agent exception (#188): a form control at "the user
  // agent default size" (its Understanding page), the size a copy of it takes
  // in a blank frame, where no author style reaches it or what it holds, and
  // without the attributes that size it. Its computed `appearance` cannot
  // tell: a select given a border keeps `auto`.
  const blank = document.createElement('iframe');
  blank.style.cssText = 'position: absolute !important; display: block !important; visibility: hidden !important; left: 0 !important; ' +
    `top: 0 !important; width: ${document.documentElement.clientWidth}px !important; height: 0 !important; border: 0 !important`;
  document.documentElement.append(blank);
  const blankDoc = blank.contentDocument;
  blankDoc.open();
  blankDoc.write(document.compatMode === 'CSS1Compat' ? '<!doctype html>' : '');
  blankDoc.close();
  const uaSized = (el, r) => {
    if (!el.matches('button, input, select, textarea')) return false;
    const copy = blankDoc.importNode(el, true);
    for (const e of [copy, ...copy.querySelectorAll('*')]) e.removeAttribute('style');
    for (const a of ['size', 'cols', 'rows', 'width', 'height']) copy.removeAttribute(a);
    blankDoc.body.append(copy);
    const c = copy.getBoundingClientRect();
    copy.remove();
    return Math.abs(c.width - r.width) < PX_SLACK && Math.abs(c.height - r.height) < PX_SLACK;
  };

  // Targets and WCAG 2.5.8's spacing exception.
  const targets = [];
  for (const el of pointerTargets(restingIn)) {
    const r = el.getBoundingClientRect();
    const small = r.width < MIN_TARGET - PX_SLACK || r.height < MIN_TARGET - PX_SLACK;
    targets.push({ el, r, small, exempt: small && (uaSized(el, r) || inText(el)), cx: (r.left + r.right) / 2, cy: (r.top + r.bottom) / 2 });
  }
  blank.remove();
  const reach = (t, r) => Math.hypot(Math.max(r.left - t.cx, 0, t.cx - r.right), Math.max(r.top - t.cy, 0, t.cy - r.bottom));
  const targetFaults = [];
  for (const t of targets) {
    if (!t.small || t.exempt) continue;
    const near = targets.find((o) => o !== t && (reach(t, o.r) < MIN_TARGET / 2 || (o.small && Math.hypot(o.cx - t.cx, o.cy - t.cy) < MIN_TARGET)));
    if (near) targetFaults.push({ subject: label(t.el), detail: `is ${Math.round(t.r.width)}x${Math.round(t.r.height)} px, and a ${MIN_TARGET} px circle on it reaches ${label(near.el)}` });
  }

  // Links in a block of text, told from it by colour alone below 3:1.
  const linkFaults = [];
  document.querySelectorAll('a[href]').forEach((a) => {
    if (!shown(a) || !/\S/.test(a.textContent) || !inText(a) || cued(a)) return;
    const ratio = contrast(rgba(css(a).color), rgba(css(a.parentElement).color));
    if (ratio < LINK_RATIO) {
      linkFaults.push({ subject: label(a), detail: `is told from the text around it by colour alone, at ${ratio.toFixed(2)}:1; ${LINK_RATIO}:1 or an underline is needed` });
    }
  });

  return { texts: [...texts.values()], generated: window.__generated.map((g) => g.text.pseudo), controls, targetFaults, linkFaults,
    hiddenStops: resting.length, unread };
}
"""
)

# The generated text MEASURE_JS found, given access-boxes.py's boxes for it:
# one text entry each, its boxes clipped as a text node's are and kept on
# window.__generated for HELD_FILL_JS, and added to MEASURE_JS's
# window.__texts for UNDER_JS.
GENERATED_JS = r"""
(boxes) => {
  const replaced = [...document.querySelectorAll('video, canvas')].filter(shown).map((e) => box(e.getBoundingClientRect()));
  return window.__generated.flatMap((g, i) => {
    g.rects = boxes[i] === null ? [] : boxes[i].map((r) => visiblePart(g.el, r)).filter((r) => !empty(r));
    if (boxes[i] !== null && !g.rects.length) return [];
    window.__texts.push({ el: g.el, rects: g.rects });
    if (boxes[i] === null) return [{ ...g.text, why: g.text.why || 'is generated text whose box the browser does not give' }];
    const over = g.rects.some((r) => replaced.some((v) => !empty(meet(r, v))));
    return [{ ...g.text, why: g.text.why || (over ? 'lies over a video or canvas' : null), rects: g.rects }];
  });
}
"""

# For each of window.__texts, given its cannot-measure reason: [the fixed or
# sticky box drawn over it at load that a scroll takes it clear of, named, or
# null; that reason, dropped where it was a video or canvas inside such a box]
# (#200, #345). Such boxes, kept on window.__bars for HIDE_JS, are found by
# hit-testing three points across the middle of each of its rects, at a sixth,
# a half and five sixths along (a guess, unmeasured), through every box drawn
# above it there, with pointers let in everywhere so a box that lets them
# through is still found. A box as tall as the window, a side rail or a layer
# over the whole page, is no bar. Scrolling down only lifts text, so a line
# under a bar at load comes clear of it only above the bar's top where it
# sticks, its load top for a fixed bar or one stuck to the window's foot, its
# `top` for one stuck to the window's head: it must fit between that and the
# window's head, or the foot of a bar stuck above it there, within the page's
# greatest scroll. Residual: a sticky bar is taken as stuck at every scroll,
# though it lets go at its containing block's end; text in a sticky box not yet
# stuck, taken as fixed, does scroll with the page until it sticks; and a bar
# stuck above another is taken as drawn over the text, though it may lie
# beneath it.
UNDER_JS = (
    flow.LABEL_JS
    + r"""
(whys) => {
  const BAR = /^(fixed|sticky)$/;
  const style = document.createElement('style');
  style.textContent = '*, *::before, *::after { pointer-events: auto !important }';
  document.documentElement.append(style);
  const barOf = (hit, el) => {
    for (let e = hit; e && !e.contains(el); e = e.parentElement) {
      if (BAR.test(css(e).position) && e.getBoundingClientRect().height < innerHeight) return e;
    }
    return null;
  };
  const sticksAt = (bar) => {
    const s = css(bar), r = bar.getBoundingClientRect();
    if (s.position === 'fixed') return r.top;
    // Stuck at the foot at load: PX_SLACK's float rounding covers a box's edge too.
    if (s.bottom !== 'auto' && Math.abs(r.bottom - (innerHeight - parseFloat(s.bottom))) < PX_SLACK) return r.top;
    return s.top === 'auto' ? -Infinity : parseFloat(s.top);
  };
  const maxScroll = document.scrollingElement.scrollHeight - innerHeight;
  const stuck = [...document.querySelectorAll('*')].filter((e) => BAR.test(css(e).position) && shown(e))
    .map((e) => { const b = box(e.getBoundingClientRect()); return { e, b, foot: sticksAt(e) + b[3] - b[1] }; })
    .filter(({ b }) => b[3] - b[1] < innerHeight);
  // The lowest foot of any other bar stuck above `top` across r: the head of the window r can rise to.
  const headOf = (bar, r, top) =>
    Math.max(0, ...stuck.filter(({ e, b, foot }) => e !== bar && b[0] < r[2] && r[0] < b[2] && foot <= top + PX_SLACK).map(({ foot }) => foot));
  const clears = (bar, rects) => {
    const b = box(bar.getBoundingClientRect()), top = sticksAt(bar);
    return rects.every((r) => empty(meet(r, b)) || r[3] - top <= Math.min(maxScroll, r[1] - headOf(bar, r, top)));
  };
  const found = window.__texts.map(({ el, rects }) => {
    for (const r of rects) for (const fx of [1 / 6, 1 / 2, 5 / 6]) {
      for (const hit of document.elementsFromPoint(r[0] + fx * (r[2] - r[0]), (r[1] + r[3]) / 2)) {
        if (hit === el || el.contains(hit) || hit.contains(el)) break;
        const bar = barOf(hit, el);
        if (bar) return bar;
      }
    }
    return null;
  });
  style.remove();
  const scrollsWithPage = (el) => {
    for (let e = el; e; e = e.parentElement) if (BAR.test(css(e).position)) return false;
    return true;
  };
  const clearable = found.map((bar, i) => bar && scrollsWithPage(window.__texts[i].el) && clears(bar, window.__texts[i].rects) ? bar : null);
  const bars = (window.__bars = [...new Set(clearable.filter(Boolean))]);
  const replaced = [...document.querySelectorAll('video, canvas')].filter((v) => shown(v) && !bars.some((b) => b.contains(v)))
    .map((v) => box(v.getBoundingClientRect()));
  return clearable.map((bar, i) => {
    if (!bar) return [null, whys[i]];
    const over = window.__texts[i].rects.some((r) => replaced.some((v) => !empty(meet(r, v))));
    return [label(bar), whys[i] === 'lies over a video or canvas' && !over ? null : whys[i]];
  });
}
"""
)

# Shared by the page-side calls: WCAG's contrast, and whether a link shows a
# cue other than its colour against the text around it.
CUE_JS = r"""
const css = (el) => getComputedStyle(el);
// The selectors of a list that are not CSS selectors.
const badSelectors = (list) => list.filter((s) => { try { document.querySelector(s); return false; } catch (e) { return true; } });
// Any CSS colour as sRGB [r, g, b, a], whatever space the page wrote it in.
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
// The colour drawn behind an element: its nearest painted background, or the canvas's white.
const backdrop = (el) => {
  for (let e = el; e; e = e.parentElement) if (painted(css(e).backgroundColor)) return rgba(css(e).backgroundColor);
  return [255, 255, 255, 1];
};
// A shadow shows where one of its layers has a painted colour and a length that is not zero.
const shadowed = (s) => s !== 'none' && s.split(/,(?![^(]*\))/).some((layer) => {
  const c = (layer.match(/rgba?\([^)]*\)/) || ['transparent'])[0];
  return painted(c) && /[1-9]/.test(layer.replace(c, ''));
});
const bold = (cs) => parseInt(cs.fontWeight, 10) >= BOLD_CUE;
const italic = (cs) => cs.fontStyle !== 'normal';
const cued = (a) => {
  const parent = css(a.parentElement);
  return [a, ...a.querySelectorAll('*')].some((e) => {
    const cs = css(e);
    return (/underline|overline/.test(cs.textDecorationLine) && painted(cs.textDecorationColor)) ||
      (parseFloat(cs.borderBottomWidth) > 0 && !/none|hidden/.test(cs.borderBottomStyle) && painted(cs.borderBottomColor)) ||
      (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0 && painted(cs.outlineColor)) || shadowed(cs.boxShadow) ||
      (painted(cs.backgroundColor) && backdrop(e).join() !== backdrop(e.parentElement).join()) || cs.backgroundImage !== 'none' ||
      bold(cs) !== bold(parent) || italic(cs) !== italic(parent);
  });
};
// WCAG 2.2's relative luminance and contrast ratio, as access-pixels.py's `luminance` and `contrast`.
const lum = ([r, g, b]) => {
  const lin = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
};
const contrast = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
// The inputs whose parts each take a Tab stop while focus stays on the input.
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
// Under DRAWN px either way is a screen reader's clipped text, or nothing.
const DRAWN = 2;
const empty = (r) => r[2] - r[0] < DRAWN || r[3] - r[1] < DRAWN;
// What an element's own box and its ancestors let it paint in; a fixed box
// escapes every ancestor's clip and an absolute one those below its
// positioned ancestor.
const clips = (cs) => cs.overflowX !== 'visible' || cs.overflowY !== 'visible' || cs.clipPath !== 'none' || cs.clip !== 'auto';
// The box inside an element's border and padding, in the window.
const contentBox = (el) => {
  const r = el.getBoundingClientRect(), cs = css(el), px = (k) => parseFloat(cs[k]);
  return [r.left + px('borderLeftWidth') + px('paddingLeft'), r.top + px('borderTopWidth') + px('paddingTop'),
    r.right - px('borderRightWidth') - px('paddingRight'), r.bottom - px('borderBottomWidth') - px('paddingBottom')];
};
// The focused element, inside any shadow roots.
const focused = () => {
  let el = document.activeElement;
  while (el && el.shadowRoot && el.shadowRoot.activeElement) el = el.shadowRoot.activeElement;
  return el;
};
// Runs each finite animation to its end. finish() throws on one with no
// effect or played at rate 0 (Web Animations' InvalidStateError), which is
// left as drawn.
const finished = (animations) => {
  for (const a of animations) {
    try { if (a.effect.getComputedTiming().endTime !== Infinity) a.finish(); } catch (e) {}
  }
};
// A focus style that slides or fades in, as a skip link's does, is read
// where it ends.
const settled = async () => {
  finished(document.getAnimations());
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
};
const blockOf = (el) => {
  for (let e = el; e; e = e.parentElement) { const d = css(e).display; if (d !== 'inline' && d !== 'contents') return e; }
  return document.body;
};
// Whether an inline element sits in a line of text: its own block, not one
// nested in it, holds text in no target.
const inText = (el) => {
  if (css(el).display !== 'inline') return false;
  const block = blockOf(el);
  const around = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
  for (let n = around.nextNode(); n; n = around.nextNode()) {
    if (/\S/.test(n.data) && !n.parentElement.closest(TARGET) && blockOf(n.parentElement) === block) return true;
  }
  return false;
};
// Under FINDABLE px either way draws nothing a pointer can find: a guess.
const FINDABLE = 0.5;
// The targets 2.5.8 measures, shown, enabled and drawn on the page, past those `skip` takes.
const pointerTargets = (skip) => [...document.querySelectorAll(TARGET)].filter((el) => {
  if (!shown(el) || disabled(el) || skip(el)) return false;
  const r = el.getBoundingClientRect();
  return r.width >= FINDABLE && r.height >= FINDABLE && r.right > 0 && r.bottom > 0;
});
// Tab stops hidden at rest, a skip link's two ways, which no visitor sees
// or taps there: a box under DRAWN px each way, clipped to nothing, or one
// laid off the page that focus, without scrolling, brings onto it (#421).
// One off the page that only a scroll reaches, in a scrolling strip or an
// app shell's scrolling main, is a target like any other.
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
    return (r[2] - r[0] < DRAWN && r[3] - r[1] < DRAWN) || (!drawnOnPage(el) && shownByFocus(el));
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

# Run before any page script: marks each element given a listener for a
# click, a press or a touch, which no DOM property shows afterwards.
LISTEN_JS = r"""
((ACT_EVENTS) => {
  const acts = new WeakSet();
  window.__acts = acts;
  const KINDS = new Set(ACT_EVENTS);
  const add = EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener = function (type, ...rest) {
    if (KINDS.has(type) && this instanceof Element) acts.add(this);
    return add.call(this, type, ...rest);
  };
})(ACT_EVENTS_JSON);
""".replace("ACT_EVENTS_JSON", json.dumps(ACT_EVENTS))

# Every part a pointer can work, kept in window.__wanted for
# KEYBOARD_JS: a native control, an ARIA widget, or an element with a click,
# press or touch handler of its own, React's included (React 17 and later
# attach theirs to the root and keep them in the element's __reactProps$
# key). An element off the page, hidden, inert or disabled is left out.
# Narrower than TARGET, 2.5.8's list, which also holds every tab stop: an
# element with a tabindex acts on nothing for being one. Returns the Tab
# stops the page could hold, a date or time input's parts counted.
WANTED_JS = (
    flow.LABEL_JS
    + r"""
() => {
  const NATIVE = 'a[href], area[href], button, input:not([type=hidden]), select, textarea, summary, iframe, ' +
    'audio[controls], video[controls], [contenteditable=""], [contenteditable=true]';
  const ROLE = /^(button|link|checkbox|radio|switch|tab|menuitem|menuitemcheckbox|menuitemradio|option|slider|spinbutton|combobox|textbox|searchbox|treeitem)$/;
  const react = (el) => { const k = Object.keys(el).find((x) => x.startsWith('__reactProps$')); return !!k && REACT_PROPS.some((p) => el[k] && el[k][p]); };
  const NAMES = { a: 'is a link', area: 'is a link', button: 'is a button', summary: 'opens a disclosure', iframe: 'is a frame' };
  const what = (el) => {
    if (el.matches(NATIVE)) return NAMES[el.localName] || (el.isContentEditable ? 'is editable text' : `is a ${el.localName} control`);
    const role = el.getAttribute('role');
    if (role && ROLE.test(role)) return `has role=${role}`;
    if (ACT_EVENTS.some((k) => el['on' + k]) || window.__acts.has(el) || react(el)) return 'acts on a click';
    return null;
  };
  const W = document.documentElement.scrollWidth, H = document.documentElement.scrollHeight;
  const wanted = [];
  for (const el of document.body.querySelectorAll('*')) {
    const why = what(el);
    if (!why || !shown(el) || disabled(el) || el.closest('[inert]')) continue;
    const r = el.getBoundingClientRect();
    if (empty(box(r)) || r.right + scrollX <= 0 || r.bottom + scrollY <= 0 || r.left + scrollX >= W || r.top + scrollY >= H) continue;
    wanted.push({ el, why });
  }
  window.__wanted = wanted;
  window.__walk = { forward: new Set(), back: new Set(), reached: new Set(), els: [], last: null };
  const dated = [...document.querySelectorAll('input')].filter((e) => DATED.test(e.type)).length;
  return document.querySelectorAll(`${TARGET}, ${NATIVE}`).length + (DATE_PARTS - 1) * dated;
}
"""
)

# Whether something opaque other than `shows` lies on top of all of `part`,
# sampled at nine points, a 3x3 grid at the middles of its sixths (a guess,
# unmeasured); the cover is named by its fixed or sticky box where it has one.
COVER_JS = r"""
const coverOf = (shows, part) => {
  const own = (hit) => hit === shows || shows.contains(hit) || hit.contains(shows);
  const opaque = (hit) => {
    for (let e = hit; e && !e.contains(shows); e = e.parentElement) {
      const cs = css(e);
      if (rgba(cs.backgroundColor)[3] >= OPAQUE || cs.backgroundImage !== 'none' || /^(img|video|canvas|svg)$/.test(e.localName)) return true;
    }
    return false;
  };
  let cover = null, covered = true;
  for (const fx of [1 / 6, 1 / 2, 5 / 6]) for (const fy of [1 / 6, 1 / 2, 5 / 6]) {
    const hit = document.elementFromPoint(part[0] + fx * (part[2] - part[0]), part[1] + fy * (part[3] - part[1]));
    if (!hit || own(hit) || !opaque(hit)) { covered = false; continue; }
    cover = cover || hit;
  }
  if (!covered || !cover) return { covered: false, cover: null };
  let bar = cover;
  while (bar && !['fixed', 'sticky'].includes(css(bar).position)) bar = bar.parentElement;
  return { covered: true, cover: label(bar || cover) };
};
"""

# One stop of a Tab walk: the focused element, where it shows, and what covers
# it. Returns {end} once focus leaves the page or comes back to an element
# this walk already met, {frame} while focus is in a frame whose page this one
# can read, which the caller reads it in, {inside} while it moves within
# a frame it cannot read after the stop on the frame itself, and {datePart}
# while it moves between a date or time input's parts (#188).
STOP_JS = (
    flow.LABEL_JS
    + COVER_JS
    + r"""
async (back) => {
  await settled();
  const w = window.__walk;
  const el = focused();
  if (!el || el === document.body || el === document.documentElement) return { end: true };
  const frame = el.localName === 'iframe';
  // Null, not a throw, for a frame whose page this one cannot read.
  const open = frame && !!el.contentDocument;
  if (el === w.last && frame) return open ? { frame: true } : { inside: true };
  if (el === w.last && el.localName === 'input' && DATED.test(el.type)) return { datePart: true };
  w.last = el;
  const seen = back ? w.back : w.forward;
  if (seen.has(el)) return { end: true };
  seen.add(el);
  w.reached.add(el);
  if (open) return { frame: true };
  w.els.push(el);
  const stop = { i: w.els.length - 1, subject: label(el), unreadable: frame, part: null, region: null, cover: null, covered: false, need: 0 };
  const view = [0, 0, document.documentElement.clientWidth, innerHeight];
  const showing = (e) => meet(visiblePart(e, box(e.getBoundingClientRect())), view);
  // A control hidden for a screen reader shows its focus on what stands for
  // it: its label, or else the nearest wrapper that shows.
  let shows = el, part = showing(el);
  for (const stand of [...(el.labels || []), ...ancestorsOf(el)]) {
    if (!empty(part)) break;
    shows = stand;
    part = showing(stand);
  }
  if (empty(part)) return stop;
  stop.part = part;
  // The least indicator that counts: a 1 px line along its longer side. A
  // guess, unmeasured: 2.4.7 sets no area, and 2.4.13 (AAA) a 2 px perimeter.
  stop.need = Math.round(Math.max(part[2] - part[0], part[3] - part[1]));
  // The region read for its focus indicator: the part showing and up to
  // WRAPPERS wrappers holding no other tab stop, which a card's :focus-within
  // outline draws on, each with FOCUS_REACH px around it for a ring drawn
  // outside.
  const around = (r) => [r[0] - FOCUS_REACH, r[1] - FOCUS_REACH, r[2] + FOCUS_REACH, r[3] + FOCUS_REACH];
  let region = around(part);
  let n = 0;
  for (let p = shows.parentElement; p && p !== document.body && n < WRAPPERS; p = p.parentElement, n++) {
    if ([...p.querySelectorAll(TARGET)].some((t) => t !== el && !el.contains(t))) break;
    const r = around(box(p.getBoundingClientRect()));
    region = [Math.min(region[0], r[0]), Math.min(region[1], r[1]), Math.max(region[2], r[2]), Math.max(region[3], r[3])];
  }
  stop.region = meet(region, view).map(Math.round);
  return Object.assign(stop, coverOf(shows, part));
}
"""
)

# The focused element, for the frame it may be.
ACTIVE_JS = "() => focused()"

# A stop read in the focused frame's own window, moved out into this one: cut
# to where the frame's content box shows, its need taken from what is left,
# and checked for what lies over the frame there.
THROUGH_JS = (
    flow.LABEL_JS
    + COVER_JS
    + r"""
(stop) => {
  const f = focused();
  const out = { ...stop, subject: `${stop.subject} in ${label(f)}` };
  if (!stop.region || stop.covered) return out;
  const inner = contentBox(f), [x, y] = inner;
  const shows = meet(visiblePart(f, inner), [0, 0, document.documentElement.clientWidth, innerHeight]);
  const moved = (b) => meet([b[0] + x, b[1] + y, b[2] + x, b[3] + y], shows);
  const part = moved(stop.part);
  if (empty(part)) return { ...out, part: null, region: null };
  out.part = part;
  out.region = moved(stop.region).map(Math.round);
  out.need = Math.round(Math.max(part[2] - part[0], part[3] - part[1]));
  return Object.assign(out, coverOf(f, part));
}
"""
)

REFOCUS_JS = "(i) => window.__walk.els[i].focus({ preventScroll: true })"

# Every part in window.__wanted no Tab walk reached, where neither it, a part
# it holds or one holding it took focus. A radio, or an item of a composite
# widget, is reached when any of its group is, as arrow keys move inside the
# group; and a link when another link to the same address is.
KEYBOARD_JS = (
    flow.LABEL_JS
    + r"""
() => {
  const COMPOSITE = '[role=radiogroup], [role=tablist], [role=menu], [role=menubar], [role=listbox], [role=grid], ' +
    '[role=tree], [role=treegrid], [role=toolbar]';
  const { reached } = window.__walk;
  const got = [...reached];
  const wanted = new Set(window.__wanted.map((w) => w.el));
  const hrefs = new Set(got.map((e) => e.href).filter((h) => typeof h === 'string'));
  const radio = (e) => e.localName === 'input' && e.type === 'radio' && e.name;
  const by = (el) => {
    if (got.some((r) => el.contains(r) || (wanted.has(r) && r.contains(el)))) return true;
    if (el.localName === 'label' && el.control && reached.has(el.control)) return true;
    if (typeof el.href === 'string' && hrefs.has(el.href)) return true;
    if (radio(el) && got.some((r) => radio(r) && r.name === el.name && r.form === el.form)) return true;
    const group = el.closest(COMPOSITE);
    return !!group && got.some((r) => group.contains(r));
  };
  return window.__wanted.filter(({ el }) => !by(el)).map(({ el, why }) => ({ subject: label(el), detail: `${why}, and the Tab key never reaches it` }));
}
"""
)

# On the motion check's load, after its watch: the motions that run long and
# those that ran long and ended, the
# elements a script moves frame by frame, the canvases, images and SVGs whose
# pixels to compare, and how many controls are named for pausing.
MOTION_JS = (
    flow.LABEL_JS
    + flow.LOOP_JS
    + r"""
() => {
  const f = window.__flow;
  f.scan();
  const out = { long: [], ended: [], scripted: [], painted: [] };
  const motions = [];
  const on = (el) => shown(el) && !empty(box(el.getBoundingClientRect()));
  // Motion running more than LONG_MS from load: a CSS or Web
  // Animations animation on the document's clock, and a video playing that
  // loops or runs that long and has no controls of its own. The animations
  // are every one the collector kept from the first frame, so one that ended
  // before this late read is still found, as ended, even where the page then
  // cancelled it or hid its element (#368).
  for (const [a, rec] of f.seen) {
    const el = a.effect && a.effect.target;
    const running = a.playState === 'running';
    if (a.timeline !== document.timeline || !el || !(running ? on(el) : rec.ended)) continue;
    const span = a.effect.getComputedTiming().activeDuration / Math.abs(a.playbackRate || 1);
    if (!(span > LONG_MS)) continue;
    const name = a.animationName || a.id;
    const motion = { subject: label(el, a.effect.pseudoElement || ''),
      what: `${name ? `"${name}" ` : ''}${span === Infinity ? 'loops forever' : `runs ${(span / 1000).toFixed(1)} s`}` };
    if (!running) { out.ended.push(motion); continue; }
    // One that reaches its end while the controls are tried was stopped by
    // none of them: `ended` tells it apart from one a control paused.
    motions.push({ stopped: () => !rec.ended && (a.playState !== 'running' || !document.getAnimations().includes(a) || !on(el)),
      ended: () => rec.ended });
    out.long.push(motion);
  }
  for (const v of document.querySelectorAll('video')) {
    if (!on(v) || v.controls || (v.paused && !v.autoplay) || (!v.loop && v.duration <= LONG_MS / 1000)) continue;
    motions.push({ stopped: () => !v.ended && (v.paused || !on(v)), ended: () => v.ended });
    out.long.push({ subject: label(v), what: v.loop ? 'plays on a loop' : 'plays a video longer than 5 s' });
  }
  window.__motions = motions;
  // Motion the script cannot time: an element a script rewrites frame by
  // frame, and a canvas, image or SVG, compared across two screenshots.
  const animated = document.getAnimations().map((a) => a.effect && a.effect.target).filter(Boolean);
  for (const [el, log] of f.rewrites) if (el.isConnected && on(el) && loop(log, REWRITE_FRAMES, REWRITE_SPAN_MS)) out.scripted.push(label(el));
  for (const el of document.querySelectorAll('canvas, img, svg')) {
    if (!on(el) || el.parentElement.closest('svg') || animated.some((t) => t === el || el.contains(t) || t.contains(el))) continue;
    const r = el.getBoundingClientRect();
    out.painted.push({ subject: label(el), rect: [r.left + scrollX, r.top + scrollY, r.right + scrollX, r.bottom + scrollY].map(Math.round) });
  }
  // The controls that might pause it: a button, switch or checkbox whose
  // name says pause, stop, hide or play, or names the motion.
  const name = (el) => [el.getAttribute('aria-label'), el.textContent, el.title, el.value].filter(Boolean).join(' ');
  const PAUSE = /\b(pause|stop|hide|play|resume|freeze|motion|animations?)\b/i;
  window.__pauses = [...document.querySelectorAll('button, input[type=button], input[type=checkbox], [role=button], [role=switch], [role=checkbox], [aria-pressed]')]
    .filter((el) => on(el) && !disabled(el) && PAUSE.test(name(el))).slice(0, PAUSE_TRIES);
  document.addEventListener('submit', (e) => e.preventDefault(), true);
  out.pauses = window.__pauses.length;
  return out;
}
"""
)

# Which long motions are stopped now, and which have ended, by their index.
STOPPED_JS = "() => window.__motions.flatMap((m, i) => (m.stopped() ? [i] : []))"
ENDED_JS = "() => window.__motions.flatMap((m, i) => (m.ended() ? [i] : []))"

BLUR_JS = "() => document.activeElement && document.activeElement.blur()"


# Leaves every box as drawn and fills the text's glyphs with one colour, taking
# off its shadows and decorations, placeholders included; transparent takes the
# text off. `color` itself is kept, so a border drawn in currentColor stays.
def text_css(fill):
    return f"""
*, *::before, *::after, *::placeholder, *::marker {{
  -webkit-text-fill-color: {fill} !important; text-shadow: none !important;
  text-decoration-color: transparent !important; -webkit-text-stroke-width: 0 !important;
  caret-color: transparent !important;
}}
"""


def page_js(body):
    consts = (
        f"const MIN_TARGET = {MIN_TARGET}, PX_SLACK = {maths.PX_SLACK}, BOLD_CUE = {BOLD_CUE}, WRAP = {WRAP}, "
        f"LINK_RATIO = {LINK_RATIO}, WRAPPERS = {WRAPPERS}, FOCUS_REACH = {FOCUS_REACH}, LONG_MS = {LONG_MS}, "
        f"REWRITE_FRAMES = {flow.REWRITE_FRAMES}, REWRITE_SPAN_MS = {flow.REWRITE_SPAN_MS}, PAUSE_TRIES = {PAUSE_TRIES}, "
        f"OPAQUE = {OPAQUE}, DATE_PARTS = {DATE_PARTS}, ACT_EVENTS = {json.dumps(ACT_EVENTS)}, REACT_PROPS = {json.dumps(REACT_PROPS)};\n"
    )
    return consts + CUE_JS + body


def decoded(png):
    return np.asarray(Image.open(io.BytesIO(png)).convert("RGB"))


# The boxes of text whose fill the page holds with its own !important rule, so
# the injected fill did not take, with generated text's where `generated`:
# those GENERATED_JS kept at load, so this runs after it.
HELD_FILL_JS = r"""
({ fill, generated }) => {
  const out = [], range = document.createRange();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const el = n.parentElement;
    if (!el || !/\S/.test(n.data) || getComputedStyle(el).webkitTextFillColor === fill) continue;
    range.selectNodeContents(n);
    for (const r of range.getClientRects()) out.push([r.left, r.top, r.right, r.bottom]);
  }
  if (generated) for (const g of window.__generated) if (getComputedStyle(g.el, g.pseudo).webkitTextFillColor !== fill) out.push(...(g.rects || []));
  return out;
}
"""


# Hides box k of the controls MEASURE_JS found at the indices given, or with
# "bars" the boxes drawn over text UNDER_JS found, keeping each one's own
# visibility to put back; null puts them back.
HIDE_JS = r"""
(arg) => {
  if (arg === null) {
    for (const [el, v, p] of window.__hid) v ? el.style.setProperty('visibility', v, p) : el.style.removeProperty('visibility');
    return;
  }
  const els = arg === 'bars' ? window.__bars : arg[1].map((i) => window.__boxEls[i][arg[0]]);
  window.__hid = els.map((el) => [el, el.style.getPropertyValue('visibility'), el.style.getPropertyPriority('visibility')]);
  for (const [el] of window.__hid) el.style.setProperty('visibility', 'hidden', 'important');
}
"""

Shots = collections.namedtuple("Shots", "shot ink held sizes behind again clear")
# The text fills the contrast shots take: off, then black and white for the ink mask.
FILLS = ("rgba(0, 0, 0, 0)", "rgb(0, 0, 0)", "rgb(255, 255, 255)")


def screenshot(page, controls, covered):
    """The Shots: the full page with its text taken off, the ink mask
    access-pixels.py reads it with, the boxes of text the page keeps its own
    fill on, each text shot's (height, width); for each of `controls`, box by
    box, the page with its text off and that box hidden, beside those of the
    other controls in its hide_groups() group; the page with its text off
    shot again after those; and where `covered`, some text lying under a
    fixed or sticky box at load, that shot and its ink mask with every such box
    hidden, or else None. Each shot holds every CSS animation, so only the
    text's fill, or the hidden boxes, differ between them. An endless one is
    held by cancelling it, so text is read on the ground the page draws
    without it, and text that fails only while it runs is not seen, as
    held.html pins (#252). Motion a script
    draws still differs: under text more of the text's box is read, and
    `again` shows it behind a control. Shots of different sizes give no ink
    mask, and each text's whole box is read: a page the first full-page shot
    grows is shot again once, and one still growing is read so (#257)."""
    page.evaluate(BLUR_JS)
    groups = maths.hide_groups(controls)

    def shoot():
        return decoded(page.screenshot(full_page=True, animations="disabled"))

    def shoot_hidden(arg):
        page.evaluate(HIDE_JS, arg)
        shot = shoot()
        page.evaluate(HIDE_JS, None)
        return shot

    for _ in range(2):
        shots, clear, hidden = [], [], {}
        for fill in FILLS:
            style = page.add_style_tag(content=text_css(fill))
            shots.append(shoot())
            if covered:
                clear.append(shoot_hidden("bars"))
            if len(shots) == 1:
                held = page.evaluate(HELD_FILL_JS, {"fill": fill, "generated": True})
                for k, g in sorted(
                    {
                        (k, g)
                        for g, c in zip(groups, controls, strict=True)
                        for k in range(len(c))
                    }
                ):
                    which = [
                        i
                        for i, c in enumerate(controls)
                        if groups[i] == g and len(c) > k
                    ]
                    hidden[k, g] = shoot_hidden([k, which])
                again = shoot()
            style.evaluate("(el) => el.remove()")
        if len({s.shape for s in [*shots, *clear, *hidden.values(), again]}) == 1:
            break
    behind = [
        [hidden[k, g] for k in range(len(c))]
        for g, c in zip(groups, controls, strict=True)
    ]
    return Shots(
        shots[0],
        maths.ink_mask(*shots),
        held,
        [s.shape[:2] for s in [*shots, *clear]],
        behind,
        again,
        (clear[0], maths.ink_mask(*clear)) if clear else None,
    )


def viewport_shot(page):
    """The window as drawn, with every finite animation run to its end and
    every endless one held at its start, so two shots differ only by what
    changed between them."""
    return decoded(page.screenshot(animations="disabled"))


# Focuses MEASURE_JS's Tab stop i hidden at rest, its focus style run to its
# end, with the window scrolled to it where it shows above or below it, and
# gives its text as it then shows, read as MEASURE_JS reads text. Text still
# beside the window lies off its shot, and cannot be measured.
FOCUSED_JS = r"""
async (i) => {
  const el = window.__resting[i];
  el.focus({ preventScroll: true });
  await settled();
  const r = el.getBoundingClientRect();
  if (r.top < 0 || r.bottom > innerHeight) {
    scrollTo({ left: scrollX, top: scrollY + r.top, behavior: 'instant' });
    await settled();
  }
  return window.__restingTexts(i);
}
"""

# Blurs focus and moves the point the next Tab starts from, which a focused
# element's blur leaves where it was (HTML's sequential focus navigation
# starting point), back to the page's top at once, past any smooth scrolling,
# as at load, for tab_walk and the contrast shots (#421, #316).
TOP_JS = r"""
() => {
  const b = document.body, had = b.getAttribute('tabindex');
  b.tabIndex = -1;
  b.focus({ preventScroll: true });
  b.blur();
  had === null ? b.removeAttribute('tabindex') : b.setAttribute('tabindex', had);
  scrollTo({ left: 0, top: 0, behavior: 'instant' });
}
"""


def focused_texts(page, hidden_stops):
    """For each of MEASURE_JS's `hidden_stops` Tab stops hidden at rest, a skip
    link's two ways, each text it shows when focused with what it is read on:
    the window shot with the text's fill off and its ink mask, and the boxes
    of text holding its own fill, as screenshot() takes them (#421)."""
    found = []
    for i in range(hidden_stops):
        texts = page.evaluate(page_js(FOCUSED_JS), i)
        if not texts:
            continue
        shots = []
        for fill in FILLS:
            style = page.add_style_tag(content=text_css(fill))
            shots.append(viewport_shot(page))
            if len(shots) == 1:
                held = page.evaluate(HELD_FILL_JS, {"fill": fill, "generated": False})
            style.evaluate("(el) => el.remove()")
        found += [(t, (shots[0], maths.ink_mask(*shots)), held) for t in texts]
    page.evaluate(TOP_JS)
    return found


def focus_fault(page, stop, key):
    """Why a focused element's focus cannot be seen, or None where it can:
    the pixels around it focused, then blurred in its frame, then it is
    focused again so the walk goes on from it."""
    if stop["region"] is None:
        return (
            "takes focus outside the window or its clipping box, where its focus cannot be seen",
            False,
        )
    # 2.4.11 judges the part, not its indicator: a ring showing past a bar
    # that hides the whole part does not save it.
    if stop["covered"]:
        return f"is hidden under {stop['cover']} when {key} brings focus to it", False
    if stop["unreadable"]:
        return None, False
    # Each state shot twice: a pixel that moves while focus stays put, a
    # video's or a canvas's, is no indicator, nor is one near it.
    shots = []
    for _ in range(2):
        shots.append(viewport_shot(page))
        stop["at"].evaluate(BLUR_JS)
        shots.append(viewport_shot(page))
        stop["at"].evaluate(REFOCUS_JS, stop["i"])
    on, off, on_again, off_again = shots
    still = maths.still_pixels(on, off, on_again, off_again)
    changed = maths.focus_changed(on, off, stop["region"], still)
    if changed >= stop["need"]:
        return None, False
    return (
        f"shows no focus indicator: {changed} px around it change by {maths.FOCUS_RATIO:g}:1 or more when it takes focus, "
        f"and a 1 px line along its longer side is {stop['need']} px"
    ), True


def stop_at(frame, back, entered):
    """One stop's reading in `frame`, followed down into each frame holding
    focus whose page it can read and moved back out through each, with "at"
    the frame it was read in. `entered` is the caller's accumulator: each
    frame focus first enters, one it cannot read included, is put in it with
    its focusable elements' count."""
    stop = frame.evaluate(page_js(STOP_JS), back)
    if not (stop.get("frame") or stop.get("unreadable")):
        stop["at"] = frame
        return stop
    inner = frame.evaluate_handle(page_js(ACTIVE_JS)).as_element().content_frame()
    if inner not in entered:
        entered[inner] = inner.evaluate(page_js(WANTED_JS))
    if stop.get("unreadable"):
        stop["at"] = frame
        return stop
    got = stop_at(inner, back, entered)
    # A frame whose own page takes the stop, as an empty frame's does, or
    # whose walk comes round again, is passed through.
    if "subject" not in got:
        return {"inside": True} if got.get("end") else got
    at = got.pop("at")
    stop = frame.evaluate(page_js(THROUGH_JS), got)
    stop["at"] = at
    return stop


def keys_js(body):
    """A page-side body for access-keys.py, with this script's helpers."""
    return page_js(flow.LABEL_JS + body)


def tab_walk(page, carousels):
    """vault.keyboard's, vault.focus's and access-keys.py's walked
    questions' access-answers.py Judged, from a Tab walk forward, which
    judges every stop's focus and reads its ring, then a Shift+Tab walk back,
    which judges only a stop something lies over. `carousels` are the
    declared carousel's selectors."""
    page.add_style_tag(content="*, html { scroll-behavior: auto !important }")
    focusable = page.evaluate(page_js(WANTED_JS))
    keys.mark(page, keys_js, carousels)
    page.evaluate(BLUR_JS)
    page.evaluate("() => scrollTo(0, 0)")
    faults, notes, cut, entered, readings, unseen = {}, [], [], {}, [], set()
    for key in ("Tab", "Shift+Tab"):
        n = 0
        while n < 2 * (focusable + sum(entered.values())) + WALK_SLACK:
            n += 1
            page.keyboard.press(key)
            stop = stop_at(page.main_frame, key != "Tab", entered)
            if stop.get("end"):
                break
            if stop.get("inside") or stop.get("datePart"):
                continue
            if stop["unreadable"] and key == "Tab":
                note = (
                    f"focus inside {stop['subject']}, whose page this one cannot read, was judged at the frame alone: "
                    "whether it shows and what lies over it, not the indicator that page draws"
                )
                if note not in notes:
                    notes.append(note)
            if key == "Tab" and not stop["unreadable"]:
                reading = keys.ring(stop["at"], keys_js, stop["i"])
                reading.update(i=stop["i"], main=stop["at"] == page.main_frame)
                readings.append(reading)
            if stop["subject"] in faults or (key != "Tab" and not stop["covered"]):
                continue
            fault, undrawn = focus_fault(page, stop, key)
            if fault:
                faults[stop["subject"]] = {"subject": stop["subject"], "detail": fault}
            if undrawn:
                unseen.add(stop["subject"])
        else:
            cut.append(
                f"the {key} walk stopped after {n} stops, short of the page's end"
            )
    unreached = page.evaluate(page_js(KEYBOARD_JS))
    walked = keys.walked(page, keys_js, readings, unseen)
    for judged in walked.values():
        judged.unmeasured.extend(cut)
    return {
        "vault.keyboard": answering.Judged(unreached, cut, [], []),
        "vault.focus": answering.Judged(list(faults.values()), cut, [], notes),
        **walked,
    }


def pause_answer(context, url):
    """vault.pause's (faults, cannot-measure reasons), from a fresh load of the
    page: each motion running more than LONG_MS from load fails
    unless one of the controls named for pausing it, clicked, stops it.
    One that ends before the read or while its controls are tried, and
    motion a script draws, frame by frame or on a canvas, image or SVG,
    cannot be measured."""
    from playwright.sync_api import Error as PlaywrightError

    page = context.new_page()
    page.add_init_script(flow.COLLECTOR_JS)
    page.goto(url, wait_until="load")
    page.evaluate("() => document.fonts.ready")
    before = page.screenshot(full_page=True)
    page.wait_for_timeout(WATCH_MS)
    after = page.screenshot(full_page=True)
    got = page.evaluate(page_js(MOTION_JS))
    unmeasured = [
        f"{m['subject']} {m['what']} from the page's load and ended before a control could be tried on it"
        for m in got["ended"]
    ] + [
        f"{s} is moved frame by frame by a script, which this check cannot time"
        for s in got["scripted"]
    ]
    a, b = (decoded(png).astype(int) for png in (before, after))
    for painted in got["painted"]:
        x, y = maths.pixels(a, painted["rect"]), maths.pixels(b, painted["rect"])
        if len(x) and len(x) == len(y) and np.abs(x - y).max() > maths.PAINT_NOISE:
            unmeasured.append(
                f"{painted['subject']} changes as it is drawn, which this check cannot time"
            )
    stopped, unclickable = set(), 0
    for i in range(got["pauses"]):
        if len(stopped) == len(got["long"]):
            break
        try:
            page.evaluate_handle("(i) => window.__pauses[i]", i).as_element().click(
                timeout=PAUSE_CLICK_MS
            )
        except PlaywrightError:
            # Covered, moving or detached: a visitor could not click it either,
            # so it pauses nothing.
            unclickable += 1
            continue
        page.evaluate(
            "() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))"
        )
        stopped.update(page.evaluate(STOPPED_JS))
    ended = set(page.evaluate(ENDED_JS)) - stopped
    page.close()
    tried = (
        f"none of the {got['pauses']} control(s) named for pausing it stops it, clicked"
        + (f" ({unclickable} could not be clicked)" if unclickable else "")
        if got["pauses"]
        else "no control on the page is named for pausing, stopping or hiding it"
    )
    faults = {}
    for i, m in enumerate(got["long"]):
        if i in ended:
            unmeasured.append(
                f"{m['subject']} {m['what']} from the page's load and ended while the controls named for pausing it were tried"
            )
        elif i not in stopped:
            held = faults.setdefault(
                m["subject"], {"subject": m["subject"], "what": []}
            )
            held["what"].append(m["what"])
    return [
        {
            "subject": s,
            "detail": f"{' and '.join(f['what'])} from the page's load, and {tried}",
        }
        for s, f in faults.items()
    ], unmeasured


def judge(got, shots, measured, table):
    """One width's {question id: access-answers.py's Judged}, with `measured`
    holding those other calls' Judged."""
    out = {qid: answering.Judged([], [], [], []) for qid, _ in answering.QUESTIONS}
    shot, ink, held, sizes = shots.shot, shots.ink, shots.held, shots.sizes
    # A fault read over the whole box is otherwise taken for one under the letters (#290).
    if len(set(sizes)) > 1:
        shown = ", ".join(f"{w}x{h}" for h, w in sizes)
        out["vault.contrast"].notes.append(
            f"the page changed size between its contrast shots, taken twice ({shown} px the second time), "
            "so each text's whole box was read, not only the pixels under its letters: "
            "a fault may be a line beside the text, not behind it"
        )
    under = {}
    read = [
        (text, shots.clear if text["under"] else (shot, ink), held)
        for text in got["texts"]
    ]
    for text, read_on, held_on in read + got["focused"]:
        if text.get("under"):
            under.setdefault(text["under"], []).append(text["subject"])
        fault, why = maths.text_contrast(*read_on, text, table.floors, held=held_on)
        if text["logotype"]:
            if fault or why:
                out["vault.contrast"].exempt.append(
                    {
                        "subject": text["subject"],
                        "detail": f"is exempt as a logotype by --logotype {text['logotype']!r}, and "
                        + (fault or why.removeprefix(text["subject"]).strip()),
                    }
                )
            continue
        if fault:
            out["vault.contrast"].faults.append(
                {"subject": text["subject"], "detail": fault}
            )
        if why:
            out["vault.contrast"].unmeasured.append(why)
    out["vault.contrast"].unmeasured.extend(
        f"{subject} is generated text in a Tab stop hidden at rest, which is read only "
        "focused, and generated text is not read there"
        for subject in got["unread"]
    )
    for bar, subjects in under.items():
        out["vault.contrast"].notes.append(
            f"{', '.join(subjects)} lay under {bar} at load, so {'was' if len(subjects) == 1 else 'were'} "
            "read with it hidden, as a visitor scrolls clear of it"
        )
    if any(
        s.shape != shot.shape for s in [shots.again, *itertools.chain(*shots.behind)]
    ):
        out["vault.control-edges"].notes.append(
            "the page changed size between its edge shots, so each edge was read at the same place in shots of "
            "different sizes"
        )
    for boxes, behind in zip(got["controls"], shots.behind, strict=True):
        subject = boxes[0]["subject"]
        if maths.moved(shot, shots.again, maths.reach(boxes[-1]["rect"])):
            out["vault.control-edges"].unmeasured.append(
                f"{subject} lies on or beside something that moves by itself, so what is behind it cannot be read"
            )
            continue
        edge = maths.control_edge(shot, behind, boxes)
        if edge is None:
            out["vault.control-edges"].unmeasured.append(
                f"{subject} lies off the screenshot"
            )
        elif edge.box is not None and edge.ratio < table.edge:
            by = (
                "its edge"
                if edge.box is boxes[0]
                else f"the edge of {edge.box['subject']} around it"
            )
            out["vault.control-edges"].faults.append(
                {
                    "subject": subject,
                    "detail": f"shows {by} at {edge.ratio:.2f}:1 at best against {maths.hexed(edge.behind)} behind that; {table.edge:g}:1 needed",
                }
            )
    out["vault.target-size"].faults.extend(got["targetFaults"])
    out["vault.colour-script"].faults.extend(got["linkFaults"])
    for qid, judged in measured.items():
        for mine, theirs in zip(out[qid], judged, strict=True):
            mine.extend(theirs)
    return out


class BadSelectorError(Exception):
    """Selectors the browser cannot parse, given by `option`."""

    def __init__(self, option, selectors):
        super().__init__(selectors)
        self.option = option
        self.selectors = selectors


def contrast_js(body):
    return page_js(flow.LABEL_JS + body)


def open_page(browser, at, width, height, **scheme):
    """A context and page at one width, in `scheme`'s colour options, loaded
    and settled, with how many looping animations never finish."""
    context = browser.new_context(
        viewport={"width": width, "height": height}, **layout.device(width), **scheme
    )
    context.set_default_timeout(at.timeout)
    context.add_init_script(LISTEN_JS)
    page = context.new_page()
    page.goto(at.url, wait_until="load")
    return context, page, page.evaluate(layout.SETTLE_JS)


def read_texts(page, logotype):
    """MEASURE_JS's result for a settled page, its generated text, the bars
    over its text and its hidden Tab stops' focused text added, and the Shots
    it is judged on."""
    got = page.evaluate(page_js(MEASURE_JS), logotype)
    if "bad" in got:
        raise BadSelectorError("--logotype", got["bad"])
    devtools = page.context.new_cdp_session(page)
    generated = pseudo_boxes.generated_boxes(
        devtools.send,
        [
            (f"window.__generated[{i}].el", pseudo)
            for i, pseudo in enumerate(got["generated"])
        ],
    )
    devtools.detach()
    got["texts"] += page.evaluate(page_js(GENERATED_JS), generated)
    for text, (under, why) in zip(
        got["texts"],
        page.evaluate(page_js(UNDER_JS), [t["why"] for t in got["texts"]]),
        strict=True,
    ):
        text["under"], text["why"] = under, why
    shots = screenshot(page, got["controls"], any(t["under"] for t in got["texts"]))
    got["focused"] = focused_texts(page, got["hiddenStops"])
    return got, shots


def contrast_answers(page, at, texts):
    """access-contrast.py's {question id: Judged} for a settled page."""
    found = contrasts.measure(
        page, contrast_js, at.table, parts=at.parts, absent=at.absent, texts=texts
    )
    if "bad" in found:
        raise BadSelectorError("--parts", found["bad"])
    return found


def theme_answer(browser, at, width, height, *, light, answered):
    """vault.theme-contrast's Judged at one width: each scheme in contrasts.SCHEMES
    that changes a colour the `light` signature holds, measured as the light
    page is, past what the light page's `answered` already finds."""
    out, shipped = answering.unjudged(), []
    for name, options in contrasts.SCHEMES:
        context, page, _ = open_page(browser, at, width, height, **options)
        try:
            if contrasts.signature(page, contrast_js) == light:
                continue
            shipped.append(name)
            got, shots = read_texts(page, at.logotype)
            judged = judge(
                got,
                shots,
                {},
                at.table._replace(floors=contrasts.scheme_floors(name, at.table)),
            )
            found = contrasts.scheme(
                name, judged, contrast_answers(page, at, None), answered
            )
            for mine, theirs in zip(out, found, strict=True):
                mine.extend(theirs)
        finally:
            context.close()
    if not shipped:
        out.notes.append(
            "the page draws the same colours in a dark scheme and under more contrast, so it ships its light one alone"
        )
    return out


def merge(into, more):
    """Extends `into`, the caller's {question id: Judged}, by each of
    `more`'s findings, adding a Judged for a question it lacks."""
    for qid, judged in more.items():
        for mine, theirs in zip(
            into.setdefault(qid, answering.unjudged()), judged, strict=True
        ):
            mine.extend(theirs)


def run(at):
    found, looping = [], 0
    with flow.chromium() as browser:
        for name, width, height in VIEWPORTS:
            context, page, loops = open_page(browser, at, width, height)
            looping = max(looping, loops)
            got, shots = read_texts(page, at.logotype)
            measured = contrast_answers(page, at, (got, shots))
            light = contrasts.signature(page, contrast_js)
            merge(measured, tab_walk(page, at.carousels))
            measured["vault.pause"] = answering.Judged(
                *pause_answer(context, at.url), [], []
            )
            merge(
                measured,
                keys.driven(
                    context, at.url, keys_js, at.carousels, mouse=name == "desktop"
                ),
            )
            context.close()
            answered = judge(got, shots, measured, at.table)
            answered["vault.theme-contrast"] = theme_answer(
                browser, at, width, height, light=light, answered=answered
            )
            found.append((name, answered))
    return found, looping


def report(url, result, *, looping, json_path, questions):
    sizes = " and ".join(f"{w}x{h} ({name})" for name, w, h in VIEWPORTS)
    lines = [f"check-access: {url}", f"measured at {sizes}"]
    if looping:
        lines.append(
            f"{looping} looping animation(s) never finish, so the page was measured mid-loop"
        )
    for qid, title in questions:
        r = result[qid]
        lines.append(f"{qid}, {title}: {r['answer'].upper()}")
        for f in r["faults"]:
            lines.append(f"  {', '.join(f['at'])}: {f['subject']} {f['detail']}")
        for f in r["exempt"]:
            lines.append(
                f"  exempt, {', '.join(f['at'])}: {f['subject']} {f['detail']}"
            )
        for u in r["unmeasured"]:
            lines.append(f"  cannot measure, {', '.join(u['at'])}: {u['reason']}")
        for n in r["notes"]:
            lines.append(f"  note, {', '.join(n['at'])}: {n['note']}")
    lines.append(f"every finding: {json_path}")
    return "\n".join(lines)


def parse(argv):
    p = argparse.ArgumentParser(
        prog="check-access.py",
        description="Measure a page's text contrast, control edges, target sizes, colour-only links, keyboard reach, focus, long motion and keyboard and focus behaviour at desktop and phone width.",
    )
    p.add_argument("url", help="an http(s) URL, or a local HTML file")
    p.add_argument("--out", required=True, metavar="DIR", help="where access.json goes")
    p.add_argument(
        "--logotype",
        action="append",
        default=[],
        metavar="SELECTOR",
        help="a CSS selector for a logotype, whose text is exempt from contrast; repeatable",
    )
    p.add_argument(
        "--pointer",
        action="store_true",
        help="answer only vault.coarse-target, under a coarse and a fine pointer, into pointer.json",
    )
    p.add_argument(
        "--pointer-table",
        default=pointing.TABLE,
        metavar="FILE",
        help="the --pointer coarse floor, as a project's rules file sets it",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=flow.LOAD_TIMEOUT_MS,
        metavar="MS",
        help="for each load",
    )
    p.add_argument(
        "--parts",
        dest="parts_file",
        metavar="FILE",
        help="the building session's parts declaration, naming the chart and carousel, or null where the page has none; its carousel is also the one vault.carousel-focus judges",
    )
    p.add_argument(
        "--contrast-table",
        default=contrasts.TABLE,
        metavar="FILE",
        help="the contrast figures, one line per record value",
    )
    at = p.parse_args(argv)
    at.url = flow.page_url(p, at.url)
    if at.pointer:
        try:
            with open(at.pointer_table, encoding="utf8") as fh:
                at.pointer_floor = pointing.parse_table(fh.read(), MIN_TARGET)
        except OSError as exc:
            p.error(f"cannot read --pointer-table {at.pointer_table}: {exc.strerror}")
        except pointing.TableError as exc:
            p.error(f"--pointer-table {at.pointer_table}: {exc}")
        return at
    try:
        with open(at.contrast_table, encoding="utf8") as fh:
            at.table = contrasts.parse_table(fh.read())
    except OSError as exc:
        p.error(f"cannot read --contrast-table {at.contrast_table}: {exc.strerror}")
    except contrasts.TableError as exc:
        p.error(f"--contrast-table {at.contrast_table}: {exc}")
    at.parts, at.absent = {}, set()
    if at.parts_file:
        probe = sibling("probe.py")
        try:
            with open(at.parts_file, encoding="utf8") as fh:
                at.parts, at.absent = probe.declared_parts(fh.read())
        except OSError as exc:
            p.error(f"cannot read --parts {at.parts_file}: {exc.strerror}")
        except probe.DeclarationError as exc:
            p.error(f"--parts {at.parts_file}: {exc}")
    at.carousels = [at.parts["carousel"]] if "carousel" in at.parts else []
    return at


def pointer_run(at):
    # A local file's own style sheets are another origin's without it, and
    # their pointer rules could not be switched off (#317). It also lets the
    # page under test read other local files while the run lasts.
    with flow.chromium(("--allow-file-access-from-files",)) as browser:
        return pointing.run(
            browser,
            at,
            VIEWPORTS,
            conditions=conditions,
            layout=layout,
            page_js=page_js,
            answering=answering,
        )


# What a run answers and writes: the default run, or --pointer.
Mode = collections.namedtuple("Mode", "report run questions")
MODES = {
    False: Mode("access.json", run, answering.QUESTIONS),
    True: Mode("pointer.json", pointer_run, (pointing.QUESTION,)),
}


def main(argv):
    at = parse(argv)
    os.makedirs(at.out, exist_ok=True)
    mode = MODES[at.pointer]
    json_path = os.path.join(at.out, mode.report)
    # An earlier run's report would reach the critic as this run's.
    pathlib.Path(json_path).unlink(missing_ok=True)
    when = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    try:
        got, code = flow.run_browser(lambda: mode.run(at), at.timeout, at.url)
    except BadSelectorError as exc:
        print(
            f"check-access.py: {exc.option} is not a CSS selector: {', '.join(exc.selectors)}",
            file=sys.stderr,
        )
        return 2
    if code:
        return code
    found, looping = got
    result = answering.answers(found, mode.questions)
    with open(json_path, "w", encoding="utf8") as fh:
        json.dump(
            {
                "url": at.url,
                "run_at": when.isoformat(),
                "looping_animations": looping,
                "viewports": {name: [w, h] for name, w, h in VIEWPORTS},
                "answers": result,
            },
            fh,
            indent=1,
        )
    print(
        report(
            at.url,
            result,
            looping=looping,
            json_path=json_path,
            questions=mode.questions,
        )
    )

    verdicts = {r["answer"] for r in result.values()}
    return 1 if "fail" in verdicts else 6 if "cannot measure" in verdicts else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
