"""access-keys.py — check-access.py's keyboard and focus questions past reach and the ring's pixels (#315),
read from its Tab walk and, for what needs keys pressed or a pointer, from a page of their own. A library
check-access.py loads; check-access.py's docstring says what each question asks of a page.

check-access.py calls, at each width:

    keys.mark(page, js, carousels)            # before the walk: what each declared carousel shows at rest
    keys.ring(frame, js, i)                   # at each forward stop, focused and then blurred
    keys.walked(page, js, readings, unseen)   # after the walk: the answers it settles
    keys.driven(context, url, js, carousels, mouse=...)  # a fresh load: the answers that press keys or the mouse,
                                                         # and each carousel's slide span, which vault.pause reads

`js` wraps a page-side body with check-access.py's helpers (label, shown, TARGET, visiblePart and the rest);
`carousels` are the CSS selectors the parts declaration gives the carousel part. Each answer is a
{question id: access-answers.py's Judged}.

Its I/O is the Playwright page or context it is handed: driven() opens a page of its own in that context and
loads the URL there. Carousels are timed by the wall clock, time.monotonic, as the page's own timers rotate its
slides: Playwright's page.clock would stand in for those timers, and time the stand-in.
"""

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402


answering = siblings.load(HERE, "access-answers.py")
overlay = siblings.load(HERE, "drive-overlay.py")
pointer = siblings.load(HERE, "drive-pointer.py")

WALKED = (
    "vault.skip-link",
    "vault.visual-order",
    "vault.scroller-focus",
    "vault.roving-focus",
    "vault.carousel-focus",
    "vault.ring-outline",
    "vault.focus-colour-kept",
    "vault.focus-visible",
)
DRIVEN = (
    "vault.roving-focus",
    "vault.menu-focus",
    "vault.carousel-focus",
    "vault.focus-visible",
)

# How long a carousel is watched for a change of slide, and how long, past one slide's span, a paused one must
# hold still. Guesses, unmeasured: the APG's example rotates every 5 s.
ROTATE_MS = 6000
STILL_SLACK_MS = 500
# How often a watched carousel is shot. A guess, unmeasured: a slide's transition is longer.
ROTATE_POLL_MS = 250
# A pixel whose channels move more than this between two shots of a carousel has changed: check-access.py's
# PAINT_NOISE, a codec's or a resampler's jitter.
ROTATE_NOISE = 8
# How many buttons and text fields, one of each class list, are clicked with the mouse: each click and move
# off waits on the pointer driver's settle, about 1.6 s a part. A guess, unmeasured.
PRESS_TRIES = 4
FIELD_TRIES = 2
# A ring colour is the focus colour, not a neutral paired with it, where its channels spread by more than
# this. A guess, unmeasured: the grey of a hairline spreads by a few, a muted brand hue by dozens.
CHROMA = 24
# A box joins a row of boxes it overlaps by at least this share of its height or the row's: half, so two
# boxes of one line join and two stacked lines do not. A guess, unmeasured.
ROW_SHARE = 0.5
# How many of a widget's stops, or a slide's hidden parts, a finding names before it says "…". A guess: enough
# to find them, short enough to read.
EXAMPLES = 3

# The composite widgets the APG keeps to one Tab stop, each with the items arrows move between, and the arrow
# that moves to the next item where aria-orientation does not say.
COMPOSITES_JS = r"""
const COMPOSITE = {
  tablist: ['[role=tab]', 'ArrowRight'],
  radiogroup: ['[role=radio], input[type=radio]', 'ArrowDown'],
  toolbar: ['button, [role=button], a[href], input, select, [tabindex]', 'ArrowRight'],
  listbox: ['[role=option]', 'ArrowDown'],
  grid: ['[role=gridcell], [role=columnheader], [role=rowheader]', 'ArrowRight'],
  treegrid: ['[role=row]', 'ArrowDown'],
  tree: ['[role=treeitem]', 'ArrowDown'],
  menubar: ['[role=menuitem], [role=menuitemcheckbox], [role=menuitemradio]', 'ArrowRight'],
};
const groups = () => [...document.querySelectorAll(Object.keys(COMPOSITE).map((r) => `[role=${r}]`).join(', '))]
  .filter((g) => shown(g) && !g.closest('[inert]') && !empty(box(g.getBoundingClientRect())));
const itemsOf = (g) => [...g.querySelectorAll(COMPOSITE[g.getAttribute('role')][0])]
  .filter((e) => shown(e) && !disabled(e) && !empty(box(e.getBoundingClientRect())));
const arrowOf = (g) => {
  const o = g.getAttribute('aria-orientation');
  return o === 'vertical' ? 'ArrowDown' : o === 'horizontal' ? 'ArrowRight' : COMPOSITE[g.getAttribute('role')][1];
};
// Where focus stands inside a widget: the item aria-activedescendant names, else the focused element.
const current = () => {
  const f = focused();
  const id = f && f.getAttribute('aria-activedescendant');
  return (id && f.ownerDocument.getElementById(id)) || f;
};
const tabbable = (e) => e.tabIndex >= 0 && shown(e) && !disabled(e) && !e.closest('[inert]') && !empty(box(e.getBoundingClientRect()));
const rotation = /\b(pause|stop|play|start|resume)\b/i;
const nameOf = (e) => [e.getAttribute('aria-label'), e.textContent, e.title].filter(Boolean).join(' ');
"""

# Before the walk: each declared carousel's tab stops, and the elements holding text a screen reader reads,
# that lie outside its box at rest, as on a slide out of view.
MARK_JS = (
    COMPOSITES_JS
    + r"""
(selectors) => {
  const k = window.__keys = { carousels: [] };
  for (const sel of selectors) for (const c of document.querySelectorAll(sel)) {
    const frame = box(c.getBoundingClientRect());
    const out = (e) => empty(meet(visiblePart(e, box(e.getBoundingClientRect())), frame));
    const unseen = new Set([...c.querySelectorAll(TARGET)].filter((e) => tabbable(e) && out(e)));
    const heard = [...c.querySelectorAll('*')].filter((e) => [...e.childNodes].some((n) => n.nodeType === 3 && /\S/.test(n.data)) &&
      shown(e) && !empty(box(e.getBoundingClientRect())) && out(e) && !e.closest('[inert], [aria-hidden=true]')).map((e) => label(e));
    k.carousels.push({ el: c, unseen, heard });
  }
}
"""
)

# At a forward stop, focused or blurred: whether the stop shows whole in the window, and how it and what stands
# for it are drawn (its labels, and up to WRAPPERS wrappers holding no other tab stop, as STOP_JS reads).
RING_JS = r"""
(i) => {
  const el = window.__walk.els[i];
  const stands = [el, ...(el.labels || [])];
  for (let p = el.parentElement, n = 0; p && p !== document.body && n < WRAPPERS; p = p.parentElement, n++) {
    if ([...p.querySelectorAll(TARGET)].some((t) => t !== el && !el.contains(t))) break;
    stands.push(p);
  }
  const r = box(el.getBoundingClientRect());
  const part = meet(visiblePart(el, r), [0, 0, document.documentElement.clientWidth, innerHeight]);
  const colours = (s) => (s.match(/(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\([^)]*\)|#[0-9a-f]{3,8}\b/gi) || []).map(rgba);
  return {
    subject: label(el),
    full: !empty(r) && part.every((v, k) => Math.abs(v - r[k]) <= 1),
    looks: stands.map((e) => {
      const cs = css(e);
      const sides = ['Top', 'Right', 'Bottom', 'Left'];
      return {
        outline: [cs.outlineStyle, cs.outlineWidth, cs.outlineColor, cs.outlineOffset].join(' '),
        outlined: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0,
        outlineColour: rgba(cs.outlineColor),
        auto: cs.outlineStyle === 'auto',
        shadow: cs.boxShadow,
        shadowColours: cs.boxShadow === 'none' ? [] : colours(cs.boxShadow),
        border: sides.map((s) => `${cs['border' + s + 'Style']} ${cs['border' + s + 'Width']} ${cs['border' + s + 'Color']}`).join(', '),
        borderColours: sides.map((s) => rgba(cs['border' + s + 'Color'])),
        background: cs.backgroundColor,
      };
    }),
  };
}
"""

# After the walk, with nothing focused: every answer the walk settles but the rings', and the colours links,
# buttons and selected items are drawn in, for the focus colour's. `full` maps a main-frame stop's index to
# whether it showed whole when focused.
WALKED_JS = (
    COMPOSITES_JS
    + f"const ROW_SHARE = {ROW_SHARE}, EXAMPLES = {EXAMPLES};\n"
    + r"""
(full) => {
  const w = window.__walk, k = window.__keys;
  const order = [...w.forward].filter((e) => e.ownerDocument === document);
  const out = { skip: { faults: [], unmeasured: [] }, visual: [], scroller: [], roving: [], carousel: [], colours: [] };
  const inside = (outer, e) => outer === e || outer.contains(e);
  const W = document.documentElement.scrollWidth, H = document.documentElement.scrollHeight;
  const onPage = (r) => !empty(box(r)) && r.right + scrollX > 0 && r.bottom + scrollY > 0 && r.left + scrollX < W && r.top + scrollY < H;

  // vault.skip-link: the first stop, past a cookie banner's, links to the main content and shows whole when focused.
  const main = document.querySelector('main, [role=main]');
  const banner = (e) => !!e.closest('[role=dialog], [role=alertdialog], [aria-modal=true]') ||
    ancestorsOf(e).concat([e]).some((a) => ['fixed', 'sticky'].includes(css(a).position) && /cookie|consent/i.test(a.textContent));
  const first = order.find((e) => !banner(e));
  if (first && !main && order.some((e) => e.closest('nav, header, [role=navigation], [role=banner]'))) {
    out.skip.unmeasured.push('the page has navigation but no main element, so where its main content starts cannot be found');
  } else if (first && main && !inside(main, first)) {
    const hash = first.localName === 'a' && first.getAttribute('href') && first.getAttribute('href').startsWith('#') ? first.getAttribute('href').slice(1) : null;
    let to = null;
    // A hash that is not valid percent-encoding names no element.
    try { to = hash && document.getElementById(decodeURIComponent(hash)); } catch (e) {}
    if (!hash) out.skip.faults.push({ subject: label(first), detail: `is the page's first Tab stop, and is no link to its main content` });
    else if (!to || !(inside(main, to) || to.contains(main))) out.skip.faults.push({ subject: label(first), detail: `is the page's first Tab stop, and links to #${hash}, which is not the main content` });
    else if (!full[w.els.indexOf(first)]) out.skip.faults.push({ subject: label(first), detail: 'links to the main content first, and is not shown whole in the window when it takes focus' });
  }

  // vault.visual-order: a positive tabindex, and boxes shown out of their source order.
  for (const e of document.querySelectorAll('[tabindex]')) {
    if (e.tabIndex > 0 && order.includes(e)) out.visual.push({ subject: label(e), detail: `has tabindex="${e.getAttribute('tabindex')}", which takes it out of the page's order` });
  }
  const stop = (c) => order.some((e) => inside(c, e));
  const text = (c) => /\S/.test(c.innerText || '');
  for (const p of document.body.querySelectorAll('*')) {
    const cs = css(p);
    if (!shown(p) || cs.display === 'contents') continue;
    const kids = [...p.children].filter((c) => shown(c) && !['fixed', 'sticky'].includes(css(c).position) && onPage(c.getBoundingClientRect()));
    if (kids.length < 2) continue;
    const flex = /flex/.test(cs.display), grid = /grid/.test(cs.display);
    const placed = (c) => { const s = css(c); return [s.gridRowStart, s.gridColumnStart].some((v) => v !== 'auto' && !v.startsWith('span')); };
    const why = [];
    if (flex && /reverse/.test(cs.flexDirection)) why.push(`flex-direction: ${cs.flexDirection}`);
    if (flex && cs.flexWrap === 'wrap-reverse') why.push('flex-wrap: wrap-reverse');
    if ((flex || grid) && kids.some((c) => css(c).order !== '0')) why.push('order');
    if (grid && kids.some(placed)) why.push('grid placement');
    if (grid && /dense/.test(cs.gridAutoFlow)) why.push('grid-auto-flow: dense');
    const lifted = kids.filter((c) => css(c).position === 'absolute' && stop(c));
    if (lifted.length) why.push('position: absolute');
    if (!why.length) continue;
    const items = kids.filter((c) => stop(c) || (why.some((y) => y !== 'position: absolute') && text(c)))
      .map((el) => ({ el, r: el.getBoundingClientRect() }));
    if (items.length < 2) continue;
    const rows = [];
    for (const it of [...items].sort((a, b) => a.r.top - b.r.top)) {
      const row = rows[rows.length - 1];
      const overlap = row && Math.min(row.bottom, it.r.bottom) - Math.max(row.top, it.r.top);
      if (row && overlap >= Math.min(row.bottom - row.top, it.r.height) * ROW_SHARE) {
        row.items.push(it);
        row.bottom = Math.max(row.bottom, it.r.bottom);
      } else rows.push({ top: it.r.top, bottom: it.r.bottom, items: [it] });
    }
    const rtl = cs.direction === 'rtl';
    const seen = rows.flatMap((row) => row.items.sort((a, b) => (rtl ? b.r.right - a.r.right : a.r.left - b.r.left)));
    const at = seen.findIndex((it, n) => it !== items[n]);
    if (at < 0) continue;
    out.visual.push({ subject: label(seen[at].el), detail: `shows before ${label(items[at].el)} but follows it in the source, moved by ${why.join(' and ')} on ${label(p)}` });
  }

  // vault.scroller-focus: a box that scrolls with nothing in it the Tab key reaches takes a stop, a region role and a name.
  for (const e of document.body.querySelectorAll('*')) {
    const cs = css(e);
    const scrolls = (/auto|scroll/.test(cs.overflowX) && e.scrollWidth > e.clientWidth + 1) || (/auto|scroll/.test(cs.overflowY) && e.scrollHeight > e.clientHeight + 1);
    if (!scrolls || !shown(e) || e.closest('[inert]') || empty(box(e.getBoundingClientRect()))) continue;
    if ([...e.querySelectorAll(TARGET)].some(tabbable)) continue;
    const named = (e.getAttribute('aria-labelledby') || '').split(/\s+/).some((id) => id && document.getElementById(id) && /\S/.test(document.getElementById(id).textContent)) ||
      /\S/.test(e.getAttribute('aria-label') || '');
    const lacks = [];
    if (!(e.hasAttribute('tabindex') && e.tabIndex >= 0)) lacks.push('tabindex="0"');
    if (e.getAttribute('role') !== 'region') lacks.push('role="region"');
    if (!named) lacks.push('name');
    if (lacks.length) out.scroller.push({ subject: label(e), detail: `scrolls, holds nothing the Tab key reaches, and has no ${lacks.join(', no ')}` });
  }

  // vault.roving-focus: a composite widget is one stop, entered on its selected item, else its first.
  groups().forEach((g, n) => {
    const stops = order.filter((e) => inside(g, e));
    if (!stops.length) return;
    if (stops.length > 1) {
      out.roving.push({ subject: label(g), detail: `takes ${stops.length} Tab stops (${stops.slice(0, EXAMPLES).map((e) => label(e)).join(', ')}${stops.length > EXAMPLES ? ', …' : ''}), not one with arrow keys inside` });
      return;
    }
    const items = itemsOf(g);
    if (stops[0] === g || !items.length) return;
    const chosen = items.find((e) => ['aria-selected', 'aria-checked', 'aria-pressed'].some((a) => e.getAttribute(a) === 'true') || e.checked);
    const want = chosen || items[0];
    if (!inside(want, stops[0]) && !stops[0].contains(want)) {
      out.roving.push({ subject: label(g), detail: `takes focus on ${label(stops[0])}, not its ${chosen ? 'selected' : 'first'} item ${label(want)}` });
    }
  });

  // vault.carousel-focus: no stop on a slide out of view, and its rotation control its first stop.
  for (const { el, unseen, heard } of (k && k.carousels) || []) {
    if (heard.length) out.carousel.push({ subject: label(el), detail: `keeps ${heard.slice(0, EXAMPLES).join(', ')}, on a slide out of view, in the accessibility tree, with no inert or aria-hidden` });
    const landed = order.filter((e) => unseen.has(e));
    if (landed.length) out.carousel.push({ subject: label(el), detail: `lets the Tab key land on ${landed.slice(0, EXAMPLES).map((e) => label(e)).join(', ')}, on a slide out of view` });
    const control = [...el.querySelectorAll(TARGET)].find((e) => tabbable(e) && rotation.test(nameOf(e)));
    const firstIn = order.find((e) => inside(el, e));
    if (control && firstIn && firstIn !== control) out.carousel.push({ subject: label(el), detail: `puts ${label(firstIn)} before its rotation control ${label(control)} in the Tab order` });
  }

  // The colours links, buttons and selected items are drawn in, for vault.focus-colour-kept.
  const use = (e, what, c) => { const v = rgba(c); if (v[3] > 0) out.colours.push({ subject: label(e), what, rgb: v.slice(0, 3) }); };
  for (const a of document.querySelectorAll('a[href]')) if (shown(a)) use(a, 'its text', css(a).color);
  for (const b of document.querySelectorAll('button, [role=button], input[type=button], input[type=submit], input[type=reset], ' +
    '[aria-selected=true], [aria-current]:not([aria-current=false]), [aria-pressed=true], [aria-checked=true]')) {
    if (!shown(b)) continue;
    const cs = css(b), what = b.matches('button, [role=button], input') && !b.matches('[aria-pressed=true], [aria-checked=true]') ? 'its' : 'its selected';
    use(b, `${what} fill`, cs.backgroundColor);
    for (const s of ['Top', 'Right', 'Bottom', 'Left']) if (parseFloat(cs['border' + s + 'Width']) > 0) use(b, `${what} edge`, cs['border' + s + 'Color']);
  }
  return out;
}
"""
)

# The driven page's widgets, menus and carousels, kept in window.__drive by index.
DRIVE_JS = (
    COMPOSITES_JS
    + r"""
(selectors) => {
  const d = window.__drive = { groups: groups(), carousels: selectors.flatMap((s) => [...document.querySelectorAll(s)]) };
  document.addEventListener('submit', (e) => e.preventDefault(), true);
  // Each carousel's previous and next buttons, by their names or an arrow alone.
  const step = /\b(prev|previous|next|back|forward)\b|^\s*[‹›←→<>]\s*$/i;
  d.steps = d.carousels.map((c) => [...c.querySelectorAll(TARGET)].filter((e) => tabbable(e) && !rotation.test(nameOf(e)) && step.test(nameOf(e))));
  return {
    groups: d.groups.map((g) => ({ subject: label(g), items: itemsOf(g).length, arrow: arrowOf(g) })),
    carousels: d.carousels.map((c, n) => ({ subject: label(c), steps: d.steps[n].length })),
  };
}
"""
)

# Puts focus on carousel n's first tab stop, else on the carousel.
FOCUS_IN_JS = (
    COMPOSITES_JS
    + "(n) => { const c = window.__drive.carousels[n]; ([...c.querySelectorAll(TARGET)].find(tabbable) || c).focus({ preventScroll: true }); }"
)
# Focuses carousel n's step button k, by its label; then what focus moved to once it is pressed, or null.
STEP_JS = (
    "([n, k]) => { const e = window.__drive.steps[n][k]; e.focus(); return label(e); }"
)
MOVED_JS = (
    "([n, k]) => { const e = window.__drive.steps[n][k], f = focused(); "
    "return e === f ? null : f && f !== document.body ? label(f) : 'the page'; }"
)

# Focuses widget n's tab stop and reads where focus stands, by its label.
ENTER_JS = (
    COMPOSITES_JS
    + r"""
(n) => {
  const g = window.__drive.groups[n];
  const start = [g, ...g.querySelectorAll('*')].find(tabbable);
  if (!start) return null;
  start.focus();
  return label(current());
}
"""
)

WHERE_JS = (
    COMPOSITES_JS
    + "(n) => { const c = current(); return { at: c ? label(c) : null, inside: !!c && window.__drive.groups[n].contains(c) }; }"
)

FRAMES_JS = (
    "() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))"
)

# A menu's items, and which the focus stands on: its index, or -1.
MENU_JS = (
    COMPOSITES_JS
    + r"""
(menu) => {
  let items = [...menu.querySelectorAll('[role=menuitem], [role=menuitemcheckbox], [role=menuitemradio]')];
  if (!items.length) items = [...menu.querySelectorAll(TARGET)];
  items = items.filter((e) => shown(e) && !disabled(e) && !empty(box(e.getBoundingClientRect())));
  const c = current();
  return { items: items.map(label), at: items.findIndex((e) => e === c || e.contains(c)), focus: c && c !== document.body ? label(c) : 'the page' };
}
"""
)

LOOK_JS = r"""
(el) => {
  const cs = getComputedStyle(el);
  return [cs.outlineStyle, cs.outlineWidth, cs.outlineColor, cs.boxShadow,
    ['Top', 'Right', 'Bottom', 'Left'].map((s) => cs['border' + s + 'Color'] + ' ' + cs['border' + s + 'Width']).join(), cs.backgroundColor];
}
"""

# The buttons and text fields to click with the mouse. A button is clicked only where a rule styles it on
# :focus, and one for each set of such rules, as no other rule draws a ring on a mouse focus; where a style
# sheet cannot be read, another site's, one for each class list too. A text field, one of each class list.
PRESSABLE_JS = (
    COMPOSITES_JS
    + r"""
([buttons, fields]) => {
  const focusOnly = /:focus(?![-\w])/g;
  const rules = [];
  let unread = false;
  const walk = (list) => {
    for (const r of list) {
      if (r.selectorText && focusOnly.test(r.selectorText)) rules.push(r.selectorText.replace(focusOnly, ''));
      focusOnly.lastIndex = 0;
      if (r.cssRules) walk(r.cssRules);
    }
  };
  for (const s of document.styleSheets) { try { walk(s.cssRules); } catch (e) { unread = true; } }
  const matching = (e) => rules.flatMap((sel, i) => { try { return e.matches(sel) ? [i] : []; } catch (x) { return []; } }).join();
  const pick = (sel, cap, kindOf) => {
    const kinds = new Set(), out = [];
    for (const e of document.querySelectorAll(sel)) {
      const kind = kindOf(e);
      if (kind === null || !tabbable(e) || kinds.has(kind) || e.closest('[role=menu], [role=dialog], dialog')) continue;
      kinds.add(kind);
      out.push(e);
      if (out.length === cap) break;
    }
    return out;
  };
  const byClass = (e) => `${e.localName} ${e.type || ''} ${e.className}`;
  const byRule = (e) => { const m = matching(e); return m ? m : unread ? byClass(e) : null; };
  const d = window.__drive;
  d.press = [
    ...pick('button, [role=button], input[type=button], input[type=submit], input[type=reset]', buttons, byRule).map((e) => ['button', e]),
    ...pick('textarea, input:not([type]), input[type=text], input[type=email], input[type=search], input[type=tel], input[type=url], input[type=number], input[type=password]', fields, byClass).map((e) => ['field', e]),
  ];
  return d.press.map(([kind, e]) => ({ kind, subject: label(e) }));
}
"""
)


BLUR_JS = "() => document.activeElement && document.activeElement.blur()"


def mark(page, js, carousels):
    """Stamps what each declared carousel shows at rest."""
    page.evaluate(js(MARK_JS), list(carousels))


def ring(frame, js, i):
    """A forward stop's reading: RING_JS focused, then blurred, then focus put back."""
    on = frame.evaluate(js(RING_JS), i)
    frame.evaluate(BLUR_JS)
    off = frame.evaluate(js(RING_JS), i)
    frame.evaluate("(i) => window.__walk.els[i].focus({ preventScroll: true })", i)
    return {
        "subject": on["subject"],
        "full": on["full"],
        "on": on["looks"],
        "off": off["looks"],
    }


def _chromatic(rgb):
    return max(rgb) - min(rgb) > CHROMA


def _hex(rgb):
    return "#" + "".join(f"{round(c):02x}" for c in rgb)


def rings(readings, unseen):
    """vault.ring-outline's, vault.focus-visible's and the ring colours' findings from each stop's reading,
    `unseen` the stops vault.focus found showing no indicator: ({qid: faults}, [(ring colour, subject)])."""
    outline, removed, colours = [], [], []
    for r in readings:
        changed = [
            (on, off) for on, off in zip(r["on"], r["off"], strict=True) if on != off
        ]
        if r["subject"] in unseen and not r["on"][0]["outlined"]:
            removed.append(
                {
                    "subject": r["subject"],
                    "detail": "takes the browser's focus ring off (outline: none) and draws none in its place",
                }
            )
        if not changed:
            continue
        lined = any(
            on["outline"] != off["outline"]
            and on["outlined"]
            or on["outlined"]
            and on["outlineColour"][3] == 0
            for on, off in changed
        )
        if not lined:
            by = sorted(
                {
                    what
                    for on, off in changed
                    for what, key in (
                        ("box-shadow", "shadow"),
                        ("border", "border"),
                        ("background", "background"),
                    )
                    if on[key] != off[key]
                }
            )
            if by:
                outline.append(
                    {
                        "subject": r["subject"],
                        "detail": f"shows focus by its {' and '.join(by)} alone, with no outline, which forced-colours mode takes off or recolours",
                    }
                )
        for on, off in changed:
            if (
                on["outline"] != off["outline"]
                and on["outlined"]
                and not on["auto"]
                and on["outlineColour"][3] > 0
            ):
                colours.append((tuple(on["outlineColour"][:3]), r["subject"]))
            if on["shadow"] != off["shadow"]:
                colours += [
                    (tuple(c[:3]), r["subject"])
                    for c in on["shadowColours"]
                    if c[3] > 0
                ]
            if on["border"] != off["border"]:
                colours += [
                    (tuple(c[:3]), r["subject"])
                    for c, was in zip(
                        on["borderColours"], off["borderColours"], strict=True
                    )
                    if c != was and c[3] > 0
                ]
    return {"vault.ring-outline": outline, "vault.focus-visible": removed}, colours


def kept(colours, uses):
    """vault.focus-colour-kept's faults: each focus ring drawn in a second chromatic colour, and each link's
    text, and each button's or selected item's fill or edge, drawn in a chromatic colour a focus ring is drawn
    in."""
    faults, said = [], set()
    ring_colours = {}
    for rgb, subject in colours:
        if _chromatic(rgb):
            rgb = tuple(round(c) for c in rgb)
            if ring_colours and rgb not in ring_colours:
                first, on = next(iter(ring_colours.items()))
                faults.append(
                    {
                        "subject": subject,
                        "detail": f"draws its focus ring in {_hex(rgb)}, a second focus colour beside {_hex(first)} on {on}",
                    }
                )
            ring_colours.setdefault(rgb, subject)
    for u in uses:
        rgb = tuple(u["rgb"])
        if rgb in ring_colours and (u["subject"], u["what"]) not in said:
            said.add((u["subject"], u["what"]))
            faults.append(
                {
                    "subject": u["subject"],
                    "detail": f"draws {u['what']} in {_hex(rgb)}, the colour focus rings are drawn in, as on {ring_colours[rgb]}",
                }
            )
    return faults


def walked(page, js, readings, unseen):
    """The answers the walk settles, from `readings`, each forward stop's ring() with its index `i` and
    whether it is in the `main` frame, and `unseen`, the subjects vault.focus found showing no indicator."""
    out = {qid: answering.unjudged() for qid in WALKED}
    full = {str(r["i"]): r["full"] for r in readings if r["main"]}
    page.evaluate(BLUR_JS)
    got = page.evaluate(js(WALKED_JS), full)
    out["vault.skip-link"].faults.extend(got["skip"]["faults"])
    out["vault.skip-link"].unmeasured.extend(got["skip"]["unmeasured"])
    for qid, key in (
        ("vault.visual-order", "visual"),
        ("vault.scroller-focus", "scroller"),
        ("vault.roving-focus", "roving"),
        ("vault.carousel-focus", "carousel"),
    ):
        out[qid].faults.extend(got[key])
    found, colours = rings(readings, unseen)
    for qid, faults in found.items():
        out[qid].faults.extend(faults)
    out["vault.focus-colour-kept"].faults.extend(kept(colours, got["colours"]))
    if any(not r["main"] for r in readings):
        for qid in WALKED:
            out[qid].notes.append(
                "focus inside a frame was judged for its ring alone, not for its order, widgets or skip link"
            )
    return out


def _frames(page):
    page.evaluate(FRAMES_JS)


def _arrows(page, js, groups):
    """vault.roving-focus's faults on the driven page: each widget of two items or more whose arrow key does
    not move focus to another of its items."""
    faults = []
    for n, g in enumerate(groups):
        if g["items"] < 2:
            continue
        was = page.evaluate(js(ENTER_JS), n)
        if was is None:
            continue
        page.keyboard.press(g["arrow"])
        _frames(page)
        now = page.evaluate(js(WHERE_JS), n)
        if not now["inside"]:
            faults.append(
                {
                    "subject": g["subject"],
                    "detail": f"loses focus to {now['at'] or 'the page'} on {g['arrow']}, which should move it to its next item",
                }
            )
        elif now["at"] == was:
            faults.append(
                {
                    "subject": g["subject"],
                    "detail": f"keeps focus on {was} when {g['arrow']} is pressed, which should move it to its next item",
                }
            )
    return faults


def _closed(page, ov):
    """Whether the menu `ov` shuts within the overlay driver's settle cap."""
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

    try:
        page.wait_for_function(
            "(el) => !el.isConnected || !el.checkVisibility({ opacityProperty: true, visibilityProperty: true })",
            arg=ov.target,
            timeout=overlay.SETTLE_CAP_MS,
        )
        return True
    except PlaywrightTimeoutError:
        return False


def _menus(page, js):
    """vault.menu-focus's faults: each menu a button opens, opened by Enter and by Up Arrow, moved in by Down
    Arrow, and shut by Escape and by Tab."""
    faults = []
    for ov in overlay.find(page):
        if ov.kind != "menu" or ov.trigger is None:
            continue
        wrong = []
        state = overlay.open(page, ov, by="keyboard")
        if not state["open"] or ov.target is None:
            faults.append(
                {
                    "subject": ov.name,
                    "detail": "does not open its menu when Enter is pressed on it",
                }
            )
            continue
        got = page.evaluate(js(MENU_JS), ov.target)
        if got["items"] and got["at"] != 0:
            wrong.append(
                f"opening it by Enter leaves focus on {got['focus']}, not its first item"
            )
        if got["at"] == 0 and len(got["items"]) > 1:
            page.keyboard.press("ArrowDown")
            _frames(page)
            if page.evaluate(js(MENU_JS), ov.target)["at"] != 1:
                wrong.append("Down Arrow does not move focus to its next item")
        state = overlay.close(page, ov, by="escape")
        if state["open"]:
            wrong.append("Escape does not close it")
        elif not ov.trigger.evaluate(
            "(t) => t === document.activeElement || t.contains(document.activeElement)"
        ):
            wrong.append(
                f"Escape leaves focus on {state['focus'] or 'the page'}, not the button that opened it"
            )
        if not state["open"]:
            overlay.open(page, ov, by="keyboard")
            page.keyboard.press("Tab")
            if not _closed(page, ov):
                wrong.append("Tab leaves it open")
                overlay.close(page, ov, by="escape")
        state = overlay.open(page, ov, by="keyboard", key="ArrowUp")
        if state["open"]:
            got = page.evaluate(js(MENU_JS), ov.target)
            if got["items"] and got["at"] != len(got["items"]) - 1:
                wrong.append(
                    f"opening it by Up Arrow leaves focus on {got['focus']}, not its last item"
                )
            overlay.close(page, ov, by="escape")
        if wrong:
            faults.append({"subject": ov.name, "detail": "; ".join(wrong)})
    return faults


# The box, opacity and visibility of carousel e's first `limit` descendants, as one string: what a slide
# moving or fading changes, and a focus ring, a hover colour or the page scrolling does not. Boxes are read
# from the carousel's own corner.
SIG_JS = r"""
  const sig = () => {
    const o = e.getBoundingClientRect();
    return [...e.querySelectorAll('*')].slice(0, limit).map((d) => {
      const r = d.getBoundingClientRect(), s = getComputedStyle(d);
      return [r.left - o.left, r.top - o.top, r.width, r.height].map(Math.round).join(',') + ',' + s.opacity + ',' + s.visibility;
    }).join(';');
  };
"""
# Watches a carousel on every frame until told to stop, setting e.__watch.moved once SIG_JS differs from the
# first frame's.
WATCH_JS = (
    "(e, limit) => {"
    + SIG_JS
    + r"""
  const first = sig(), watch = { moved: false, on: true };
  e.__watch = watch;
  const tick = () => {
    if (!watch.on) return;
    if (sig() !== first) watch.moved = true;
    else requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}
"""
)
# True once SIG_JS has held for `ms` of frames, false at `within` ms.
STILL_JS = (
    "(e, [limit, ms, within]) => new Promise((done) => {"
    + SIG_JS
    + r"""
  let last = sig(), since = performance.now();
  const began = since;
  const tick = (now) => {
    const s = sig();
    if (s !== last) { last = s; since = now; }
    else if (now - since >= ms) return done(true);
    if (now - began >= within) return done(false);
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
})
"""
)
WATCH_LIMIT = 200


def _shot(handle):
    import io

    import numpy as np
    from PIL import Image

    return np.asarray(
        Image.open(io.BytesIO(handle.screenshot(animations="allow"))).convert("RGB")
    ).astype(int)


def _differs(a, b):
    return a.shape != b.shape or bool((abs(a - b) > ROTATE_NOISE).any())


def change(page, handle, within_ms):
    """How long, in ms, until the carousel changes, or None where it holds for `within_ms`. A change is its
    pixels differing from the first shot, or WATCH_JS seeing a box inside it move or fade on any frame: a
    two-slide carousel shot once a cycle, as on a loaded machine, shows the first slide every time."""
    handle.evaluate(WATCH_JS, WATCH_LIMIT)
    start, began = _shot(handle), time.monotonic()
    try:
        while (waited := (time.monotonic() - began) * 1000) < within_ms:
            page.wait_for_timeout(ROTATE_POLL_MS)
            if handle.evaluate("(e) => e.__watch.moved") or _differs(
                start, _shot(handle)
            ):
                return waited + ROTATE_POLL_MS
        return None
    finally:
        handle.evaluate("(e) => { e.__watch.on = false; }")


def still(handle):
    """Waits until no box inside the carousel has moved or faded for ROTATE_POLL_MS of frames, as after a
    slide's transition; False at ROTATE_MS. Read in the page, as two shots that far apart never match on a
    loaded machine, where one shot outlasts the gap between a fast carousel's turns."""
    return handle.evaluate(STILL_JS, [WATCH_LIMIT, ROTATE_POLL_MS, ROTATE_MS])


def _carousels(page, js, carousels):
    """vault.carousel-focus's driven faults and cannot-measure reasons: a rotating carousel holds still while
    focus or the pointer is in it, and its previous and next buttons keep focus when pressed; and each
    carousel's _span."""
    faults, unmeasured, spans = [], [], []
    for n, c in enumerate(carousels):
        handle = page.evaluate_handle(
            "(n) => window.__drive.carousels[n]", n
        ).as_element()
        # The pointer has not moved on a fresh load, so it is over nothing yet.
        span = _span(page, handle)
        spans.append(span)
        if isinstance(span, str):
            unmeasured.append(f"{c['subject']} {span}")
        elif span is not None:
            hold = span + STILL_SLACK_MS
            page.evaluate(js(FOCUS_IN_JS), n)
            if change(page, handle, hold) is not None:
                faults.append(
                    {
                        "subject": c["subject"],
                        "detail": "keeps rotating while focus is inside it",
                    }
                )
            page.evaluate(BLUR_JS)
            still(handle)
            try:
                pointer.hover(page, handle)
                if change(page, handle, hold) is not None:
                    faults.append(
                        {
                            "subject": c["subject"],
                            "detail": "keeps rotating while the pointer is over it",
                        }
                    )
            except pointer.PointerError as exc:
                unmeasured.append(f"{c['subject']} cannot be hovered: {exc}")
        for k in range(c["steps"]):
            name = page.evaluate(js(STEP_JS), [n, k])
            page.keyboard.press("Enter")
            _frames(page)
            moved = page.evaluate(js(MOVED_JS), [n, k])
            if moved:
                faults.append(
                    {
                        "subject": c["subject"],
                        "detail": f"moves focus from {name} to {moved} when it is pressed",
                    }
                )
    return faults, unmeasured, spans


def _span(page, handle):
    """A carousel's time from one slide to the next in ms, None where it does not change within ROTATE_MS, or
    why it cannot be timed."""
    if change(page, handle, ROTATE_MS) is None:
        return None
    if not still(handle):
        return f"never holds still for {ROTATE_POLL_MS} ms within {ROTATE_MS} ms, so its rotation cannot be timed"
    span = change(page, handle, ROTATE_MS)
    if span is None:
        return f"changed once and then held for {ROTATE_MS} ms, so its rotation cannot be timed"
    still(handle)
    return span


# Swallows every click before the page's own handlers see it, so a press reads focus without acting; None
# takes the swallower off.
BLOCK_JS = r"""
(on) => {
  if (on) {
    window.__block = (e) => { e.stopImmediatePropagation(); e.preventDefault(); };
    addEventListener('click', window.__block, true);
  } else removeEventListener('click', window.__block, true);
}
"""


def _presses(page, js):
    """vault.focus-visible's driven faults: a button clicked with the mouse draws no ring, and a text field
    clicked into shows focus, and the cannot-measure reasons."""
    faults, unmeasured = [], []
    pressed = page.evaluate(js(PRESSABLE_JS), [PRESS_TRIES, FIELD_TRIES])
    page.evaluate(BLOCK_JS, True)
    away = False
    for n, p in enumerate(pressed):
        el = page.evaluate_handle("(n) => window.__drive.press[n][1]", n).as_element()
        page.evaluate(BLUR_JS)
        try:
            if not away:
                pointer.leave(page, el)
                away = True
            rest = el.evaluate(LOOK_JS)
            pointer.click(page, el)
            # Off it again, so a hover style is not taken for a ring.
            pointer.leave(page, el)
        except pointer.PointerError as exc:
            unmeasured.append(f"{p['subject']} cannot be clicked: {exc}")
            continue
        if not el.evaluate("(e) => e === document.activeElement"):
            continue
        now = el.evaluate(LOOK_JS)
        if p["kind"] == "button" and now[:4] != rest[:4]:
            faults.append(
                {
                    "subject": p["subject"],
                    "detail": "draws a focus ring when clicked with the mouse: its focus style is set on :focus, not :focus-visible",
                }
            )
        elif p["kind"] == "field" and now == rest:
            faults.append(
                {"subject": p["subject"], "detail": "shows no focus when clicked into"}
            )
    page.evaluate(BLUR_JS)
    page.evaluate(BLOCK_JS, False)
    return faults, unmeasured


def driven(context, url, js, carousels, *, mouse):
    """The answers that press keys or the mouse, from a fresh load of the page, and each declared carousel's
    time from one slide to the next, as _span gives it; the mouse presses only where `mouse`, as a press at one
    width settles the :focus rule every width shares."""
    out = {qid: answering.unjudged() for qid in DRIVEN}
    page = context.new_page()
    page.add_init_script(pointer.WATCH_JS)
    page.goto(url, wait_until="load")
    page.evaluate("() => document.fonts.ready")
    got = page.evaluate(js(DRIVE_JS), list(carousels))
    out["vault.roving-focus"].faults.extend(_arrows(page, js, got["groups"]))
    faults, unmeasured, spans = _carousels(page, js, got["carousels"])
    out["vault.carousel-focus"].faults.extend(faults)
    out["vault.carousel-focus"].unmeasured.extend(unmeasured)
    if mouse:
        faults, unmeasured = _presses(page, js)
        out["vault.focus-visible"].faults.extend(faults)
        out["vault.focus-visible"].unmeasured.extend(unmeasured)
    # Menus last: a menu item may act when its menu is shut by Tab.
    out["vault.menu-focus"].faults.extend(_menus(page, js))
    page.close()
    return out, spans
