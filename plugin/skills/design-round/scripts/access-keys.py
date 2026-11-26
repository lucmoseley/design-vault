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

ROTATE_MS = 6000  # guess, #501
STILL_SLACK_MS = 500  # guess, #501
ROTATE_POLL_MS = 250  # guess, #501
ROTATE_NOISE = 8  # guess, #501
PRESS_TRIES = 4  # guess, #501
FIELD_TRIES = 2  # guess, #501
CHROMA = 24  # guess, #501
ROW_SHARE = 0.5  # guess, #501
EXAMPLES = 3  # guess, #501

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
const current = () => {
  const f = focused();
  const id = f && f.getAttribute('aria-activedescendant');
  return (id && f.ownerDocument.getElementById(id)) || f;
};
const tabbable = (e) => e.tabIndex >= 0 && shown(e) && !disabled(e) && !e.closest('[inert]') && !empty(box(e.getBoundingClientRect()));
const rotation = /\b(pause|stop|play|start|resume)\b/i;
const nameOf = (e) => [e.getAttribute('aria-label'), e.textContent, e.title].filter(Boolean).join(' ');
"""

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

  const main = document.querySelector('main, [role=main]');
  const banner = (e) => !!e.closest('[role=dialog], [role=alertdialog], [aria-modal=true]') ||
    ancestorsOf(e).concat([e]).some((a) => ['fixed', 'sticky'].includes(css(a).position) && /cookie|consent/i.test(a.textContent));
  const first = order.find((e) => !banner(e));
  if (first && !main && order.some((e) => e.closest('nav, header, [role=navigation], [role=banner]'))) {
    out.skip.unmeasured.push('the page has navigation but no main element, so where its main content starts cannot be found');
  } else if (first && main && !inside(main, first)) {
    const hash = first.localName === 'a' && first.getAttribute('href') && first.getAttribute('href').startsWith('#') ? first.getAttribute('href').slice(1) : null;
    let to = null;
    try { to = hash && document.getElementById(decodeURIComponent(hash)); } catch (e) {}
    if (!hash) out.skip.faults.push({ subject: label(first), detail: `is the page's first Tab stop, and is no link to its main content` });
    else if (!to || !(inside(main, to) || to.contains(main))) out.skip.faults.push({ subject: label(first), detail: `is the page's first Tab stop, and links to #${hash}, which is not the main content` });
    else if (!full[w.els.indexOf(first)]) out.skip.faults.push({ subject: label(first), detail: 'links to the main content first, and is not shown whole in the window when it takes focus' });
  }

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

  for (const { el, unseen, heard } of (k && k.carousels) || []) {
    if (heard.length) out.carousel.push({ subject: label(el), detail: `keeps ${heard.slice(0, EXAMPLES).join(', ')}, on a slide out of view, in the accessibility tree, with no inert or aria-hidden` });
    const landed = order.filter((e) => unseen.has(e));
    if (landed.length) out.carousel.push({ subject: label(el), detail: `lets the Tab key land on ${landed.slice(0, EXAMPLES).map((e) => label(e)).join(', ')}, on a slide out of view` });
    const control = [...el.querySelectorAll(TARGET)].find((e) => tabbable(e) && rotation.test(nameOf(e)));
    const firstIn = order.find((e) => inside(el, e));
    if (control && firstIn && firstIn !== control) out.carousel.push({ subject: label(el), detail: `puts ${label(firstIn)} before its rotation control ${label(control)} in the Tab order` });
  }

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

DRIVE_JS = (
    COMPOSITES_JS
    + r"""
(selectors) => {
  const d = window.__drive = { groups: groups(), carousels: selectors.flatMap((s) => [...document.querySelectorAll(s)]) };
  document.addEventListener('submit', (e) => e.preventDefault(), true);
  const step = /\b(prev|previous|next|back|forward)\b|^\s*[‹›←→<>]\s*$/i;
  d.steps = d.carousels.map((c) => [...c.querySelectorAll(TARGET)].filter((e) => tabbable(e) && !rotation.test(nameOf(e)) && step.test(nameOf(e))));
  return {
    groups: d.groups.map((g) => ({ subject: label(g), items: itemsOf(g).length, arrow: arrowOf(g) })),
    carousels: d.carousels.map((c, n) => ({ subject: label(c), steps: d.steps[n].length })),
  };
}
"""
)

FOCUS_IN_JS = (
    COMPOSITES_JS
    + "(n) => { const c = window.__drive.carousels[n]; ([...c.querySelectorAll(TARGET)].find(tabbable) || c).focus({ preventScroll: true }); }"
)
STEP_JS = (
    "([n, k]) => { const e = window.__drive.steps[n][k]; e.focus(); return label(e); }"
)
MOVED_JS = (
    "([n, k]) => { const e = window.__drive.steps[n][k], f = focused(); "
    "return e === f ? null : f && f !== document.body ? label(f) : 'the page'; }"
)

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
    page.evaluate(js(MARK_JS), list(carousels))


def ring(frame, js, i):
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


SIG_JS = r"""
  const sig = () => {
    const o = e.getBoundingClientRect();
    return [...e.querySelectorAll('*')].slice(0, limit).map((d) => {
      const r = d.getBoundingClientRect(), s = getComputedStyle(d);
      return [r.left - o.left, r.top - o.top, r.width, r.height].map(Math.round).join(',') + ',' + s.opacity + ',' + s.visibility;
    }).join(';');
  };
"""
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
    return handle.evaluate(STILL_JS, [WATCH_LIMIT, ROTATE_POLL_MS, ROTATE_MS])


def _carousels(page, js, carousels):
    faults, unmeasured, spans = [], [], []
    for n, c in enumerate(carousels):
        handle = page.evaluate_handle(
            "(n) => window.__drive.carousels[n]", n
        ).as_element()
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
    if change(page, handle, ROTATE_MS) is None:
        return None
    if not still(handle):
        return f"never holds still for {ROTATE_POLL_MS} ms within {ROTATE_MS} ms, so its rotation cannot be timed"
    span = change(page, handle, ROTATE_MS)
    if span is None:
        return f"changed once and then held for {ROTATE_MS} ms, so its rotation cannot be timed"
    still(handle)
    return span


BLOCK_JS = r"""
(on) => {
  if (on) {
    window.__block = (e) => { e.stopImmediatePropagation(); e.preventDefault(); };
    addEventListener('click', window.__block, true);
  } else removeEventListener('click', window.__block, true);
}
"""


def _presses(page, js):
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
    out["vault.menu-focus"].faults.extend(_menus(page, js))
    page.close()
    return out, spans
