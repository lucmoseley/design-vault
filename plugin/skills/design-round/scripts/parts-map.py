#!/usr/bin/env python3
"""Maps what each part of a web candidate does, for the function records in
design-critique's rules/: whether a visitor can act on it, read from the DOM.

USAGE
  python3 parts-map.py <url or file> --out DIR [--timeout MS]

It loads the page at conditions.py's desktop and phone widths, the phone's
with a touch screen, lets it settle as conditions.py does, and lists each
part:

- every part a visitor can act on: a link, button, form control, summary, an
  element with an ARIA widget role, an inline `onclick`, a click listener the
  page added (`addEventListener`, React's `onClick` or Vue's), and an iframe,
  whose own parts are not read. A disabled control cannot be acted on. A
  listener on the root, or on an element holding every other part a visitor
  can act on, is a framework delegating the whole page's clicks and makes
  nothing actable;
- every part a visitor cannot act on that could look as if they can: an
  element holding text and no actable part that sets `cursor: pointer`, draws
  its own box (a fill unlike what is behind it, an edge on all four sides, or
  a shadow) narrower than the page, is underlined, is matched by a `:hover`
  rule, or sets text in a colour a link on the page has that is not the
  page's commonest text colour.

For each it gives its role, `href`, box and hit area at each width (the share
of its box where a click lands on it, and what takes the rest), the part it
is nested in, the part whose click area surrounds it, and the `:hover` and
`:focus` rules that select it. Rules in a stylesheet the browser will not let
a page read are listed as unread.

A link that goes nowhere is marked `dead` with its target:
one to `#` alone, or to a fragment of this page that no element carries as
its id, nor an `a` as its name. `#top` goes to the page's top by the HTML
standard, and a link given a click of its own may act through `#`, so neither
is dead; a click the page handles from an outer element is not seen. gate.js
tally fails vault.affordance on each dead part, whatever it looks like.

It answers vault.one-target. A part fails it where it sits in another
actable part: in the markup, or with that part's click area on two or more
of its sides, as for a button flush in a card's corner.

Each part gets an id, p1 onwards in document order, that says nothing of what
it does; gate.js tally compares the critics' vault.affordance answers with it.

It writes DIR/parts.json (every part and the answer, for the building session
and the tally), DIR/key.txt (each id and its text, for the critics) and
DIR/key-desktop.png and DIR/key-phone.png (the page with each part outlined
and its id beside it), deleting any an earlier run left there.

EXITS 0 vault.one-target passes / 1 it fails (each fault printed) / 2 the
arguments are wrong / 3 Playwright, its browser, numpy or Pillow is missing / 4
the page did not render in time / 5 the browser refused the page / 7 a call hung
that would never return. Exits 0 and 1 print on stdout; the rest print on
stderr.
"""

import argparse
import contextlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402

conditions = siblings.load(HERE, "conditions.py")
prelude = siblings.load(HERE, "access-page.py")
flow = siblings.load(HERE, "check-flow.py")
runner = siblings.load(HERE, "runner.py")
answers_file = siblings.load(HERE, "answers-file.py")

KEYS = (
    "key.txt",
    *(f"key-{name}.png" for name, _, _ in conditions.VIEWPORTS),
)
# guess, #501
KEY_TEXT = 40

LISTEN_JS = r"""
(() => {
  const TYPES = new Set(ACT_EVENTS_JSON);
  const add = EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener = function (type, ...rest) {
    if (TYPES.has(type) && this instanceof Element) this.__partsMapClick = true;
    return add.call(this, type, ...rest);
  };
})();
""".replace("ACT_EVENTS_JSON", json.dumps(prelude.ACT_EVENTS))

MAP_JS = (
    flow.LABEL_JS
    + r"""
() => {
  const ACTION = 'a[href], button, input:not([type=hidden]), select, textarea, summary, [onclick], ' +
    '[role=button], [role=link], [role=checkbox], [role=radio], [role=switch], [role=tab], [role=menuitem], ' +
    '[role=option], [role=combobox], [role=slider], [role=textbox], iframe';
  const CLICKS = REACT_PROPS_JSON;
  const EVENTS = ACT_EVENTS_JSON;
  const css = (el) => getComputedStyle(el);
  const shown = (el) => {
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      const cs = css(e);
      if (cs.display === 'none' || cs.visibility === 'hidden' || cs.visibility === 'collapse' || cs.opacity === '0') return false;
    }
    const r = el.getBoundingClientRect();
    return r.width >= 1 && r.height >= 1;
  };
  const disabled = (el) => !!el.closest(':disabled, [aria-disabled="true"]');
  const frameworkClick = (el) => {
    const react = Object.keys(el).find((k) => k.startsWith('__reactProps$'));
    if (react && el[react] && CLICKS.some((k) => typeof el[react][k] === 'function')) return true;
    return !!(el._vei && CLICKS.some((k) => el._vei[k]));
  };
  const all = [...document.body.querySelectorAll('*')].filter((el) => !el.closest('svg') || el.localName === 'svg');
  const listened = (el) => el !== document.body && (el.__partsMapClick || frameworkClick(el) || EVENTS.some((k) => typeof el['on' + k] === 'function'));
  const marked = all.filter((el) => (el.matches(ACTION) || listened(el)) && !disabled(el) && shown(el));
  const actable = new Set(marked.filter((el) => el.matches(ACTION) || marked.some((o) => o !== el && !el.contains(o))));
  const actableOf = (el) => { for (let e = el; e; e = e.parentElement) if (actable.has(e)) return e; return null; };

  // A fragment indicates the element with that id, else an <a> with that name, else the top for `top`: https://html.spec.whatwg.org/multipage/browsing-the-web.html#the-indicated-part-of-the-document
  const here = location.href.split('#')[0];
  const deadOf = (el) => {
    if (el.localName !== 'a' || !el.hasAttribute('href') || listened(el) || !el.href.includes('#') || el.href.split('#')[0] !== here) return null;
    // What follows `:~:` is the fragment directive, not part of the fragment: https://wicg.github.io/scroll-to-text-fragment/#fragment-directive
    const [fragment, directive] = el.href.slice(el.href.indexOf('#') + 1).split(':~:');
    if (!fragment) return directive === undefined ? '#' : null;
    let decoded = fragment;
    try { decoded = decodeURIComponent(fragment); } catch (e) { decoded = fragment; }
    const carried = (name) => document.getElementById(name) || [...document.getElementsByName(name)].some((n) => n.localName === 'a');
    return carried(fragment) || carried(decoded) || decoded.toLowerCase() === 'top' ? null : '#' + fragment;
  };

  const roleOf = (el) => {
    if (el.getAttribute('role')) return el.getAttribute('role');
    const t = el.localName;
    if (t === 'a') return el.hasAttribute('href') ? 'link' : 'a';
    if (t === 'input') return { checkbox: 'checkbox', radio: 'radio', range: 'slider', button: 'button', submit: 'button', reset: 'button', image: 'button' }[el.type] || 'textbox';
    return { button: 'button', select: 'combobox', textarea: 'textbox', summary: 'button', iframe: 'iframe' }[t] ||
      (actable.has(el) ? 'click handler on ' + t : t);
  };
  const textOf = (el) => (el.getAttribute('aria-label') || (el.labels?.length ? el.labels[0].innerText : '') || el.innerText ||
    el.getAttribute('alt') || el.getAttribute('placeholder') || el.getAttribute('title') ||
    (/^(button|submit|reset)$/.test(el.type) ? el.value : '') || '').replace(/\s+/g, ' ').trim();
  const ownText = (el) => [...el.childNodes].some((n) => n.nodeType === 3 && /\S/.test(n.data));

  const rules = new Map();
  const unread = [];
  const STATES = /:(hover|focus-visible|focus)(?![\w-])/;
  const note = (el, state, text) => {
    if (!rules.has(el)) rules.set(el, { hover: [], focus: [] });
    const got = rules.get(el)[state === 'hover' ? 'hover' : 'focus'];
    if (!got.includes(text)) got.push(text);
  };
  const read = (list) => {
    for (const r of list) {
      if (r.selectorText !== undefined) {
        for (const s of r.selectorText.split(/,(?![^(]*\))/)) {
          const m = s.match(STATES);
          if (!m) continue;
          const rest = s.slice(m.index).search(/[\s>+~]/);
          const subject = (rest < 0 ? s : s.slice(0, m.index + rest))
            .replace(/:(hover|focus-visible|focus-within|focus|active)(?![\w-])/g, '').replace(/::?(before|after)\b/g, '').trim();
          try {
            for (const el of document.querySelectorAll(subject)) note(el, m[1], s.trim());
          } catch (e) { continue; }
        }
      }
      if (r.cssRules) read(r.cssRules);
    }
  };
  for (const sheet of document.styleSheets) {
    try { read(sheet.cssRules); } catch (e) { unread.push(sheet.href || 'an inline sheet'); }
  }

  const linkColours = new Set([...actable].filter((el) => el.matches('a[href]')).map((el) => css(el).color));
  const counts = new Map();
  for (const el of all) if (ownText(el) && shown(el)) counts.set(css(el).color, (counts.get(css(el).color) || 0) + el.textContent.length);
  const body = [...counts].sort((a, b) => b[1] - a[1])[0]?.[0];

  const paint = (c) => c && !/^rgba\(.*, 0\)$/.test(c) && c !== 'transparent';
  const fillOf = (el) => { for (let e = el; e; e = e.parentElement) if (paint(css(e).backgroundColor)) return css(e).backgroundColor; return 'rgb(255, 255, 255)'; };
  const edged = (cs) => ['Top', 'Right', 'Bottom', 'Left'].every((s) =>
    parseFloat(cs['border' + s + 'Width']) > 0 && !/none|hidden/.test(cs['border' + s + 'Style']) && paint(cs['border' + s + 'Color']));
  const pageWidth = document.documentElement.clientWidth;
  const whyListed = (el) => {
    const cs = css(el), why = [];
    if (cs.cursor === 'pointer' && (!el.parentElement || css(el.parentElement).cursor !== 'pointer')) why.push('cursor: pointer');
    const ownFill = paint(cs.backgroundColor) && cs.backgroundColor !== fillOf(el.parentElement);
    if ((ownFill || edged(cs) || cs.boxShadow !== 'none') && el.getBoundingClientRect().width < pageWidth - 1) why.push('draws its own box');
    if (/underline/.test(cs.textDecorationLine)) why.push('underlined');
    if (rules.get(el)?.hover.length) why.push('a :hover rule selects it');
    if (ownText(el) && cs.color !== body && linkColours.has(cs.color)) why.push("a link's colour");
    return why;
  };

  const parts = [];
  const pathOf = (el) => { const p = []; for (let e = el; e.parentElement; e = e.parentElement) p.unshift([...e.parentElement.children].indexOf(e)); return p; };
  for (const el of all) {
    let listed = null;
    if (actable.has(el)) listed = [];
    else if (shown(el) && textOf(el) && !actableOf(el) && ![...actable].some((a) => el.contains(a)) && !(el.localName === 'label' && el.control)) {
      const why = whyListed(el);
      if (why.length) listed = why;
    }
    if (!listed) continue;
    const r = el.getBoundingClientRect();
    parts.push({
      el, path: pathOf(el), actable: actable.has(el), role: roleOf(el), text: textOf(el), selector: label(el),
      href: el.href && typeof el.href === 'string' ? el.href : null, dead: actable.has(el) ? deadOf(el) : null, listed, cursor: css(el).cursor,
      hover: rules.get(el)?.hover || [], focus: rules.get(el)?.focus || [],
      box: [r.left + scrollX, r.top + scrollY, r.width, r.height].map(Math.round),
    });
  }

  const index = new Map(parts.map((p, i) => [p.el, i]));
  const landing = (x, y) => {
    const hit = document.elementFromPoint(x, y);
    if (!hit) return null;
    const a = actableOf(hit);
    return a ? { part: index.get(a) } : { other: label(hit) };
  };
  // guess, #501
  const GRID = 5;
  // guess, #501
  const BESIDE_PX = 4;
  for (const [i, p] of parts.entries()) {
    const outer = actableOf(p.el.parentElement);
    p.inside = outer ? index.get(outer) : null;
    p.hit = null;
    p.takenBy = [];
    p.enclosedBy = null;
    if (!p.actable) continue;
    p.el.scrollIntoView({ block: 'center', inline: 'center', behavior: 'instant' });
    const r = p.el.getBoundingClientRect();
    const others = new Map();
    let mine = 0, seen = 0;
    for (let gx = 0; gx < GRID; gx++) for (let gy = 0; gy < GRID; gy++) {
      const x = r.left + (gx + 0.5) * r.width / GRID, y = r.top + (gy + 0.5) * r.height / GRID;
      if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) continue;
      seen++;
      const at = landing(x, y);
      if (at && at.part === i) { mine++; continue; }
      const who = !at ? 'nothing' : at.part !== undefined ? at.part : at.other;
      others.set(who, (others.get(who) || 0) + 1);
    }
    p.hit = seen ? Math.round((100 * mine) / seen) : null;
    p.takenBy = [...others].sort((a, b) => b[1] - a[1]).map(([who]) => who);
    const around = new Map();
    for (const [x, y] of [[r.left - BESIDE_PX, r.top + r.height / 2], [r.right + BESIDE_PX, r.top + r.height / 2], [r.left + r.width / 2, r.top - BESIDE_PX], [r.left + r.width / 2, r.bottom + BESIDE_PX]]) {
      const by = landing(x, y)?.part;
      if (by !== undefined && by !== i) around.set(by, (around.get(by) || 0) + 1);
    }
    p.enclosedBy = [...around].find(([, sides]) => sides >= 2)?.[0] ?? null;
  }
  scrollTo({ top: 0, left: 0, behavior: 'instant' });
  return { unread, parts: parts.map(({ el, ...p }) => p) };
}
""".replace("REACT_PROPS_JSON", json.dumps(prelude.REACT_PROPS)).replace(
        "ACT_EVENTS_JSON", json.dumps(prelude.ACT_EVENTS)
    )
)

KEY_JS = r"""
(boxes) => {
  const layer = document.createElement('div');
  layer.id = '__parts_map_key';
  layer.style.cssText = 'position:absolute;left:0;top:0;width:0;height:0;z-index:2147483647;pointer-events:none';
  for (const [id, [x, y, w, h]] of boxes) {
    const box = document.createElement('div');
    box.style.cssText = `position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;outline:2px solid #e0007a;outline-offset:1px`;
    const tag = document.createElement('div');
    tag.textContent = id;
    tag.style.cssText = `position:absolute;left:${x}px;top:${Math.max(0, y - 16)}px;font:bold 12px/14px sans-serif;color:#fff;background:#e0007a;padding:1px 3px`;
    layer.append(box, tag);
  }
  document.documentElement.append(layer);
}
"""
UNKEY_JS = "() => document.getElementById('__parts_map_key')?.remove()"


def run(at):
    with runner.chromium() as browser, contextlib.ExitStack() as opened:
        found = []
        for name, width, _ in conditions.VIEWPORTS:
            page = opened.enter_context(
                conditions.open_page(
                    browser,
                    at.url,
                    width=width,
                    timeout=at.timeout,
                    init_scripts=(LISTEN_JS,),
                )
            )
            conditions.settle(page)
            found.append((name, page, page.evaluate(MAP_JS)))
        parts = number(found)
        for name, page, got in found:
            boxes = [[parts_id, p["box"]] for parts_id, p in ids_at(parts, got)]
            page.evaluate(KEY_JS, boxes)
            page.screenshot(
                path=os.path.join(at.out, f"key-{name}.png"), full_page=True
            )
            page.evaluate(UNKEY_JS)
        return parts, sorted({u for _, _, got in found for u in got["unread"]})


def ids_at(parts, got):
    by_path = {tuple(p["path"]): p["id"] for p in parts}
    return [(by_path[tuple(p["path"])], p) for p in got["parts"]]


def number(found):
    merged = {}
    for name, _, got in found:
        listed = got["parts"]
        for p in listed:
            entry = merged.setdefault(
                tuple(p["path"]),
                {
                    k: p[k]
                    for k in (
                        "path",
                        "actable",
                        "role",
                        "text",
                        "selector",
                        "href",
                        "dead",
                        "cursor",
                        "hover",
                        "focus",
                    )
                }
                | {"listed": [], "at": {}},
            )
            entry["dead"] = entry["dead"] or p["dead"]
            for why in p["listed"]:
                if why not in entry["listed"]:
                    entry["listed"].append(why)
            entry["at"][name] = {
                "box": p["box"],
                "hit": p["hit"],
                "taken_by": [
                    w if isinstance(w, str) else listed[w]["path"] for w in p["takenBy"]
                ],
                "inside": None if p["inside"] is None else listed[p["inside"]]["path"],
                "enclosed_by": None
                if p["enclosedBy"] is None
                else listed[p["enclosedBy"]]["path"],
            }
    ordered = sorted(merged.values(), key=lambda e: e["path"])
    ids = {tuple(e["path"]): f"p{i}" for i, e in enumerate(ordered, 1)}

    def named(w):
        return ids[tuple(w)] if isinstance(w, list) else w

    for e in ordered:
        e["id"] = ids[tuple(e["path"])]
        for geo in e["at"].values():
            geo["taken_by"] = [named(w) for w in geo["taken_by"]]
            for k in ("inside", "enclosed_by"):
                geo[k] = None if geo[k] is None else named(geo[k])
    return [{"id": e.pop("id"), **e} for e in ordered]


def one_target(parts):
    names = {p["id"]: p for p in parts}
    faults = {}
    for p in parts:
        for name, geo in p["at"].items():
            for k, how in (
                ("inside", "is nested inside"),
                ("enclosed_by", "sits inside the click area of"),
            ):
                outer = geo[k]
                if outer is None:
                    continue
                key = (p["id"], outer)
                held = faults.setdefault(
                    key,
                    {
                        "subject": f'{p["id"]} ({p["role"]}, "{short(p["text"])}")',
                        "detail": f'{how} {outer} ({names[outer]["role"]}, "{short(names[outer]["text"])}")',
                        "at": [],
                    },
                )
                if name not in held["at"]:
                    held["at"].append(name)
    found = list(faults.values())
    return {"answer": "fail" if found else "pass", "faults": found}


def short(text):
    return text if len(text) <= KEY_TEXT else text[: KEY_TEXT - 1] + "…"


def key(parts):
    lines = [
        "Each part of the page, outlined with its id in key-<width>.png. Say for each whether it looks",
        "as if a visitor can act on it.",
        "",
    ]
    for p in parts:
        where = "; ".join(
            f"{name} at {g['box'][0]},{g['box'][1]}, {g['box'][2]}x{g['box'][3]} px"
            for name, g in p["at"].items()
        )
        lines.append(f'{p["id"]}  "{short(p["text"])}"  {where}')
    return "\n".join(lines) + "\n"


def report(found, out):
    parts, answer = found["parts"], found["answers"]["vault.one-target"]
    actable = sum(p["actable"] for p in parts)
    lines = [
        f"parts-map: {found['url']}",
        f"{len(parts)} part(s): {actable} a visitor can act on, {len(parts) - actable} that could look as if they can",
        f"vault.one-target, one action per tap target: {answer['answer'].upper()}",
    ]
    for f in answer["faults"]:
        lines.append(f"  {', '.join(f['at'])}: {f['subject']} {f['detail']}")
    dead = [p for p in parts if p["dead"]]
    if dead:
        lines.append(
            f"{len(dead)} link(s) going nowhere, each failing vault.affordance at the tally:"
        )
    for p in dead:
        where = (
            "# alone"
            if p["dead"] == "#"
            else f"{p['dead']}, which nothing on the page carries"
        )
        lines.append(f'  {p["id"]} ("{short(p["text"])}") goes to {where}')
    for u in found["unread_stylesheets"]:
        lines.append(f"unread stylesheet, its :hover and :focus rules not listed: {u}")
    lines.append(
        f"every part: {os.path.join(out, 'parts.json')}; the critics' key: {os.path.join(out, 'key.txt')}"
    )
    return "\n".join(lines)


def parse(argv):
    p = argparse.ArgumentParser(
        prog="parts-map.py",
        description="List what each part of a page does, at desktop and phone width, and whether any tap target carries two actions.",
    )
    p.add_argument("url", help="an http(s) URL, or a local HTML file")
    p.add_argument(
        "--out", required=True, metavar="DIR", help="where parts.json and the key go"
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=runner.LOAD_TIMEOUT_MS,
        metavar="MS",
        help="for each load",
    )
    at = p.parse_args(argv)
    at.url = runner.page_url(p, at.url)
    return at


def main(argv):
    at = parse(argv)
    when, json_path = answers_file.start(at.out, "parts.json", *KEYS)
    got, code = runner.run_browser(lambda: run(at), at.timeout, at.url)
    if code:
        return code
    parts, unread = got
    answer = one_target(parts)
    for p in parts:
        del p["path"]
    found = {
        "viewports": {name: [w, h] for name, w, h in conditions.VIEWPORTS},
        "unread_stylesheets": unread,
        "answers": {"vault.one-target": answer},
        "parts": parts,
    }
    answers_file.write(json_path, at.url, when, **found)
    with open(os.path.join(at.out, "key.txt"), "w", encoding="utf8") as fh:
        fh.write(key(parts))
    print(report({"url": at.url, **found}, at.out))
    return 1 if answer["answer"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
