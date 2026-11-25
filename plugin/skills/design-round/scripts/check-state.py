#!/usr/bin/env python3
"""check-state.py — the driven-state checks (#312): drives a candidate page
into the states only a visitor reaches, hover, press, a key, focus, a
submit, an open overlay, a drag, a wheel, a pinch, the passing of time, and
answers the rule records about what each state shows (#250).

USAGE
  python3 check-state.py <page> --out DIR [--parts FILE] [--part NAME=SELECTOR]…
        [--handover SELECTOR]… [--table FILE] [--timeout MS]

The page is a URL or a local HTML file. Every check opens it afresh at the
desktop viewport, under any condition its rule names (no hover, right to
left), so one check's state never reaches another. Forms are really filled
and submitted, so run it on a candidate, never a live site.

--parts is the building session's parts declaration, {"declared": {<part>:
<its CSS selector, or null>}} (design-round §1c, #274); --part gives one
part by hand. A line that reads a part is not judged where the part is not
declared, and has no match where it is declared null. --handover names a
link the project's rules file keeps a handover notice for, which the exit
line passes (vault.exit-warning).

THE TABLE, by default check-state.table beside this script, gives each line
as fields split by " | ": the record id, the check, and its value where it
reads one; a value's items are split by "; ". Blank lines and lines
starting with # are skipped.

  reveal          what resting the pointer on a part draws is drawn too when
                  the part, or the first focusable part inside it, takes
                  focus, and is drawn at load where no input can hover
  persist         stays ms >= N: what hover draws closes on Escape with the
                  pointer still, stays as the pointer moves onto it, and is
                  still drawn N ms later
  click-opens     every overlay a navigation landmark holds opens on a click
                  and on Enter, and nothing hover opens there lacks one
  editable        part NAME: each declared editable value changes its look,
                  or draws a cue, on hover and on focus
  reflow          shift px <= N: hover, focus and a tab's selection move no
                  text part's box, nor its neighbours', by more than N px
  states          the computed style of hover, focus and, for buttons and
                  links, :active differs from rest and from one another; a
                  disabled control's differs from an enabled one's
  inverse         split luminance N: a tooltip or toast a hover or a button
                  draws sits on the other side of luminance N from the page,
                  and its text's luminance crosses N again against it
  default         not WORD, …: the button a dialog focuses, or else its
                  form's Return button, is not named one of the words
  toggle          pressing an aria-pressed button flips it, and its on and
                  off states differ by more than colour
  release         undone by WORDS: pressing a button or link down, before
                  release, acts on nothing (no markup change, submit, window
                  or page load) that sliding off it and releasing leaves in
                  place; a control named with a word in WORDS that the press
                  shows is put to review, as an undo the rule allows
  single-key      turned off by WORDS: with focus on the page, no printable
                  key acts or moves focus; where a control named with a word
                  in WORDS is on the page, an acting key is put to review, as
                  a setting that may turn it off or remap it
  on-focus        focusing each part the Tab key reaches loads no page, opens
                  no window or dialog, submits nothing and keeps focus there
  space           part NAME: Space toggles each player whose media or play
                  button has focus, and toggles none with focus elsewhere;
                  a native player with controls needs no declaring
  slider-keys     each slider rises on Right and Up, falls on Left and Down,
                  goes to its ends on Home and End, and moves on a track click
  direction       each slider's lowest value sits at the reading start, left
                  to right and right to left, and Left raises it right to left
  drag            a drawn slider dragged past its end and off its track keeps
                  following to its top value, passes no pointerover to
                  another part and selects no text
  wheel           each horizontal scroller moves on a sideways wheel and on
                  Shift with the wheel, and a carousel holds a previous and a
                  next control that move it
  whole           inset px N: a composite part with one control and a drawn
                  extent hits that control at its corners and edge middles,
                  N px in
  pinch           part NAME; zoom ratio >= Z; drift px <= N: a two-finger
                  spread on a declared zoomable part keeps the point between
                  the fingers within N px; a part it grows by less than Z
                  times is not judged
  target          fill contrast <= N: a fragment link's target takes a side
                  mark, or a fill other than its ground at N:1 or less
  visited         contrast >= N: a link in a list in main, once visited,
                  draws less saturated and at N:1 on its ground; a navigation
                  link draws the same (Playwright's full Chromium)
  timing          a checked field shows no error while a first entry is typed,
                  one on leaving it in a form of several fields and none till
                  submit on a one-question page, and clears on the fixing key
  paste           each field outside sign-in takes a paste and a drop
  auth-paste      each sign-in field takes a paste and a drop, a split code
                  box takes the whole code on one paste, and no password
                  field turns autocomplete off
  on-input        choosing or entering a value loads no page, opens no
                  window, submits nothing, moves no focus and hides the
                  control, save where the control has a description
  enter           Enter in a form's single-line field submits it
  kept            the fields keep their values through an error submit,
                  and all but password fields keep them after history Back
  summary-focus   a submit with every field wrong focuses a part in main,
                  below any breadcrumbs or back link, above the h1, linking
                  to a field
  suggest         type TEXT; axe RULE …: a field that draws suggestions as
                  TEXT is typed is a combobox, expanded, controlling a listbox
                  whose option ArrowDown makes active, with a status region
                  saying how many, and the axe rules find nothing
  mixed           part NAME: a group checkbox shows mixed when some of its
                  group are checked, checked when all are, clear when none
  submenu         closing a menu leaves no submenu it opened open
  interrupt       shut ms >= N: each overlay open with nothing opening it has
                  a control that shuts it, and it is still shut N ms later
  dialog-name     axe RULE …: each dialog is a dialog element or role, holds
                  aria-modal where it blocks the page, and has a name
  ellipsis        a menu item ending in "…" opens a dialog that asks for
                  more, one that does not ends without it, and no label
                  writes three full stops or a busy button "…"
  expanded        axe RULE …: each overlay trigger reads aria-expanded false
                  shut and true open, a menu trigger aria-haspopup, and no
                  other button shows and hides a panel
  live-region     after each button and each failed submit, no live region
                  shows a message it held hidden at load, and none but
                  role=alert arrives with its message
  toast           part NAME; stays ms >= N: a toast a button draws leaves
                  focus on the button, sits in a live region, and where it
                  holds an action stays N ms and has that action elsewhere
  exit            a link to another site goes there, no dialog asking first
  time-limit      warn ms >= N; horizon ms H: under a fake clock, a page that
                  leaves itself within H warns N ms or more before, and one
                  button in the warning restarts the limit

Each record id's finding is fail where any check misses, else not judged
where a check could not run, else pass, or no match where nothing applied.
A described control on-input finds a change on goes under review, which
never changes an answer. DIR/state.json holds every finding; an earlier
run's is deleted.

EXITS 0 no miss / 1 a miss (each printed) / 2 the arguments or the table are
wrong / 3 Playwright or its browser is missing / 4 the page did not load in time
/ 5 the browser refused the page / 7 a call hung that would never return. Exits
0 and 1 print on stdout; the rest print on stderr.
"""

import argparse
import colorsys
import contextlib
import datetime
import io
import json
import math
import os
import re
import shutil
import sys
import tempfile
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402


flow = siblings.load(HERE, "check-flow.py")
form = siblings.load(HERE, "drive-form.py")
pointer = siblings.load(HERE, "drive-pointer.py")
overlay = siblings.load(HERE, "drive-overlay.py")
rule_table = siblings.load(HERE, "rule-table.py")
conditions = siblings.load(HERE, "conditions.py")
markup = siblings.load(HERE, "check-markup.py")
probe = siblings.load(HERE, "probe.py")

TABLE = os.path.join(HERE, "check-state.table")
ITEMS = "; "
VIEWPORT = dict(
    zip(("width", "height"), map(int, flow.DESKTOP.split("x")), strict=True)
)
# How the checks drive a page, not what they judge: each a guess, stated as
# one, at the gesture a visitor makes.
TRACK_CLICK = 0.25  # a click a quarter along a slider's track
TRACK_ENDS = (0.03, 0.97)  # clicks just inside a track's two ends
DRAG_PAST = (40, 60)  # px a drag runs past the track's end, and below it
WHEEL_MIN = 40  # px, the smallest sideways wheel turn
PINCH_AT = 0.3  # where the fingers meet, as a share of the part's box
PINCH_SPREAD = 0.25  # how far each finger moves, as a share of its shorter side
PINCH_START, PINCH_STEPS = 10, 10  # px apart the fingers start; moves they take
# Each check and the shape of its value: None for no value. A group named
# n_… is read as a number, words as a comma list, rules as axe rule ids.
NUM = r"(?P<n_{}>\d+(?:\.\d+)?)"
PART = r"part (?P<part>[a-z][a-z-]*)"
AXE = r"axe (?P<rules>[a-z][a-z-]*(?: [a-z][a-z-]*)*)"
CHECKS = {
    "reveal": None,
    "persist": r"stays ms >= " + NUM.format("ms"),
    "click-opens": None,
    "editable": PART,
    "reflow": r"shift px <= " + NUM.format("px"),
    "states": None,
    "inverse": r"split luminance " + NUM.format("lum"),
    "default": r"not (?P<words>\S.*)",
    "toggle": None,
    "release": r"undone by (?P<words>\S.*)",
    "single-key": r"turned off by (?P<words>\S.*)",
    "on-focus": None,
    "space": PART,
    "slider-keys": None,
    "direction": None,
    "drag": None,
    "wheel": None,
    "whole": r"inset px " + NUM.format("px"),
    "pinch": PART
    + ITEMS
    + r"zoom ratio >= "
    + NUM.format("zoom")
    + ITEMS
    + r"drift px <= "
    + NUM.format("px"),
    "target": r"fill contrast <= " + NUM.format("ratio"),
    "visited": r"contrast >= " + NUM.format("ratio"),
    "timing": None,
    "paste": None,
    "auth-paste": None,
    "on-input": None,
    "enter": None,
    "kept": None,
    "summary-focus": None,
    "suggest": r"type (?P<text>\S+)" + ITEMS + AXE,
    "mixed": PART,
    "submenu": None,
    "interrupt": r"shut ms >= " + NUM.format("ms"),
    "dialog-name": AXE,
    "ellipsis": None,
    "expanded": AXE,
    "live-region": None,
    "toast": PART + ITEMS + r"stays ms >= " + NUM.format("ms"),
    "exit": None,
    "time-limit": r"warn ms >= "
    + NUM.format("warn")
    + ITEMS
    + r"horizon ms "
    + NUM.format("horizon"),
}

# The text a paste check writes to the clipboard: digits, so a number, phone
# or code field takes it as readily as a text field.
PASTED = "4242"
# The keys single-key presses: every printable ASCII character and Space.
KEYS = [chr(c) for c in range(0x21, 0x7F)] + [" "]
# The words that name a control which shuts a dialog without acting: the
# overlay driver's close words, for telling a toast's action from its close.
SHUT_WORDS = ("close", "cancel", "dismiss", "done", "hide", "×")
# The properties that show a state's look, and of them those that are not
# colour, for a toggle whose on and off must differ by more than colour.
SHAPE_PROPS = [
    *(
        f"border-{s}-{p}"
        for s in ("top", "right", "bottom", "left")
        for p in ("width", "style")
    ),
    "outline-style",
    "outline-width",
    "box-shadow",
    "font-weight",
    "font-style",
    "text-decoration-line",
    "background-image",
    "transform",
]
LOOK_PROPS = SHAPE_PROPS + [
    *(f"border-{s}-color" for s in ("top", "right", "bottom", "left")),
    "background-color",
    "color",
    "outline-color",
    "text-decoration-color",
    "opacity",
    "filter",
]
TARGET_PROPS = [
    "background-color",
    "background-image",
    "box-shadow",
    *(f"border-{s}-width" for s in ("top", "right", "bottom", "left")),
]

TAP_JS = r"""
(() => {
  if (window.__st) return;
  const seen = new WeakMap();
  const add = EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener = function (type, fn, options) {
    let types = seen.get(this);
    if (!types) seen.set(this, (types = new Set()));
    types.add(type);
    return add.call(this, type, fn, options);
  };
  const drawn = (el) => {
    if (!el || !el.isConnected || el.nodeType !== 1) return false;
    if (!el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) return false;
    const r = el.getBoundingClientRect();
    return r.width >= 2 && r.height >= 2;  // a guess, stated as one: under 2 px no one sees it
  };
  const text = (el) => (el ? (el.innerText ?? el.textContent ?? "") : "").replace(/\s+/g, " ").trim();
  // The accessible name's sources in their order: aria-labelledby, aria-label,
  // a <label>, the content, title; a value last, for a button input.
  const nameOf = (el) => ((el.getAttribute("aria-labelledby") || "").split(/\s+/)
      .map((id) => document.getElementById(id)).filter(Boolean).map(text).join(" ") ||
    el.getAttribute("aria-label") || [...(el.labels || [])].map(text).join(" ") ||
    text(el) || el.getAttribute("title") || el.value || "").trim();
  const describe = (el) => {
    if (!el || el.nodeType !== 1) return null;
    const n = nameOf(el).slice(0, 40);
    return el.localName + (el.id ? "#" + el.id : "") + (n ? ` "${n}"` : "");
  };
  const pathOf = (el) => {
    const parts = [];
    for (let e = el; e && e.nodeType === 1 && e !== document.documentElement; e = e.parentElement) {
      let i = 1;
      for (let s = e.previousElementSibling; s; s = s.previousElementSibling) if (s.localName === e.localName) i++;
      parts.unshift(`${e.localName}:nth-of-type(${i})`);
    }
    return ["html", ...parts].join(" > ");
  };
  const fault = (el) => el?.closest?.("[data-fault]")?.getAttribute("data-fault") ?? null;
  const listens = (el, types) => types.some((t) => seen.get(el)?.has(t) || el.hasAttribute?.("on" + t));
  const all = () => [...document.querySelectorAll("body *")];
  const LIVE = '[role="alert"], [role="status"], [role="log"], [aria-live]:not([aria-live="off"])';
  const DIALOGS = 'dialog[open], [role="dialog"], [role="alertdialog"]';
  let log = null, skip = null, observer = null, marked = null, live0 = null, overs = null;
  const note = (kind, what) => { if (log) log.push({ kind, what }); };
  const take = (records) => {
    for (const r of records) {
      if (r.type === "attributes" && skip && (skip.contains(r.target) || r.target.contains(skip))) continue;
      note("markup", r.type === "childList" ? `changed what ${describe(r.target)} holds`
        : r.type === "characterData" ? `changed the text of ${describe(r.target.parentElement)}`
        : `set ${r.attributeName} on ${describe(r.target)}`);
    }
  };
  const open = window.open;
  window.open = function (...args) { note("window", "opened a window"); return open.apply(this, args); };
  add.call(document, "submit", (e) => note("submit", `submitted ${describe(e.target)}`), true);
  add.call(document, "pointerover", (e) => overs?.push(e.target), true);
  const hoverSelectors = () => {
    const out = new Set();
    const split = (s) => {
      const parts = []; let depth = 0, start = 0;
      for (let i = 0; i < s.length; i++) {
        if (s[i] === "(") depth++;
        else if (s[i] === ")") depth--;
        else if (s[i] === "," && !depth) { parts.push(s.slice(start, i)); start = i + 1; }
      }
      return [...parts, s.slice(start)].map((p) => p.trim());
    };
    const walk = (rules) => {
      for (const r of rules) {
        if (r.selectorText) {
          for (const s of split(r.selectorText)) {
            const i = s.indexOf(":hover");
            const head = s.slice(0, i);
            // Only a rule that goes on past :hover to another element can
            // show something; `a:hover` alone restyles the link itself.
            const reaches = /^(:[\w-]+(\([^)]*\))?)*\s*[\s>+~]\s*\S/.test(s.slice(i + 6));
            if (i > 0 && reaches && (head.split("(").length === head.split(")").length)) {
              out.add(head.replace(/:(focus-visible|focus-within|focus|active|visited|link)\b/g, ""));
            }
          }
        }
        if (r.cssRules) walk(r.cssRules);
      }
    };
    // The sheet texts read through the browser's CSS domain, which a file
    // page's own cssRules refuse; else the sheets the page lets script read.
    if (window.__stSheets) {
      for (const text of window.__stSheets) {
        const sheet = new CSSStyleSheet();
        try { sheet.replaceSync(text); walk(sheet.cssRules); } catch {}
      }
    } else for (const sheet of document.styleSheets) { try { walk(sheet.cssRules); } catch {} }
    return out;
  };
  window.__st = {
    drawn, text, nameOf, describe, pathOf, fault, LIVE, DIALOGS,
    info: (el) => ({ where: describe(el), fault: fault(el), path: pathOf(el) }),
    background(el) {
      for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
        const c = getComputedStyle(e).backgroundColor;
        if (c !== "transparent" && !/^rgba\(.*,\s*0\)$/.test(c)) return c;
      }
      return "rgb(255, 255, 255)";
    },
    style: (el, props) => {
      const cs = getComputedStyle(el);
      return Object.fromEntries(props.map((p) => [p, cs.getPropertyValue(p)]));
    },
    // A part drawn apart from its ground: its own fill, a shadow or a border.
    edged(el) {
      const cs = getComputedStyle(el);
      if (this.background(el) !== this.background(el.parentElement)) return true;
      if (cs.boxShadow !== "none") return true;
      return ["Top", "Right", "Bottom", "Left"].some((s) =>
        parseFloat(cs[`border${s}Width`]) > 0 && cs[`border${s}Style`] !== "none" && !/,\s*0\)$/.test(cs[`border${s}Color`]));
    },
    // One element per markup signature: its tag, type, role and classes,
    // and its parent's, which share their styles on a styled page.
    distinct(els) {
      const seen = new Set();
      const sig = (e) => [e.localName, e.type, e.getAttribute("role"), e.className, e.getAttribute("aria-pressed") !== null].join("|");
      return els.filter((e) => {
        const key = sig(e) + "/" + (e.parentElement ? sig(e.parentElement) : "");
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    },
    shown: (el) => [...el.querySelectorAll("*")].filter(drawn).map(pathOf),
    watch(el) {
      log = []; skip = el || null;
      observer?.disconnect();
      observer = new MutationObserver(take);
      observer.observe(document, { subtree: true, childList: true, characterData: true, attributes: true });
    },
    acts(kinds) {
      if (observer) take(observer.takeRecords());
      return [...new Set((log || []).filter((e) => !kinds || kinds.includes(e.kind)).map((e) => e.what))];
    },
    dialogs: () => [...document.querySelectorAll(DIALOGS)].filter(drawn).length,
    mark() { marked = new WeakSet(all().filter(drawn)); },
    revealed() {
      const fresh = new Set(all().filter((el) => drawn(el) && !marked.has(el)));
      return [...fresh].filter((el) => !fresh.has(el.parentElement));
    },
    hoverTargets() {
      const found = new Set();
      for (const s of hoverSelectors()) {
        try { document.querySelectorAll(s).forEach((el) => found.add(el)); } catch {}
      }
      for (const el of all()) {
        if (listens(el, ["mouseenter", "mouseover", "pointerenter", "pointerover"])) found.add(el);
        const ids = (el.getAttribute("aria-describedby") || "").split(/\s+/).filter(Boolean);
        if (ids.some((id) => document.getElementById(id)?.getAttribute("role") === "tooltip")) found.add(el);
      }
      return [...found].filter((el) => el !== document.body && drawn(el));
    },
    focusable: (el) => (el.tabIndex >= 0 && !el.disabled) ? el
      : el.querySelector('a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])'),
    tabbables() {
      const sel = 'a[href], button, input, select, textarea, summary, [tabindex], audio[controls], video[controls], [contenteditable="true"]';
      const els = [...document.querySelectorAll(sel)].filter((el) =>
        el.tabIndex >= 0 && !el.disabled && el.type !== "hidden" && drawn(el) && !el.closest("[inert]"));
      return [...els.filter((el) => el.tabIndex > 0).sort((a, b) => a.tabIndex - b.tabIndex),
        ...els.filter((el) => el.tabIndex === 0)];
    },
    controls(kinds) {
      const sel = {
        button: 'button, [role="button"], input[type="button"], input[type="submit"], input[type="reset"]',
        link: 'a[href], [role="link"]',
        box: 'input[type="checkbox"], [role="checkbox"], [role="switch"]',
        field: 'input:not([type="hidden"]):not([type="button"]):not([type="submit"]):not([type="reset"]):not([type="checkbox"]):not([type="radio"]):not([type="range"]):not([type="file"]):not([type="color"]), select, textarea',
      };
      return [...document.querySelectorAll(kinds.map((k) => sel[k]).join(", "))].filter(drawn);
    },
    sliders: () => [...document.querySelectorAll('input[type="range"], [role="slider"]')].filter(drawn),
    sliderValue: (el) => el.localName === "input" ? +el.value : +el.getAttribute("aria-valuenow"),
    sliderEnds: (el) => el.localName === "input"
      ? [el.min === "" ? 0 : +el.min, el.max === "" ? 100 : +el.max]
      : [+el.getAttribute("aria-valuemin"), +el.getAttribute("aria-valuemax")],
    track(el) {
      if (el.localName === "input") return el;
      const r = el.getBoundingClientRect();
      // A guess, stated as one: a box under three heights wide is a thumb.
      return r.width < 3 * r.height ? el.parentElement : el;
    },
    liveOf: (el) => el.closest(LIVE),
    snapLive() {
      live0 = new Map([...document.querySelectorAll(LIVE)].map((el) => [el, { text: text(el), drawn: drawn(el) }]));
    },
    liveFaults() {
      const out = [];
      for (const el of document.querySelectorAll(LIVE)) {
        const now = text(el);
        if (!drawn(el) || !now) continue;
        const was = live0.get(el);
        if (!was) {
          if (el.getAttribute("role") !== "alert") out.push([el, "arrives with its message, not written into a live region the first markup holds"]);
        } else if (!was.drawn && was.text && was.text === now) {
          out.push([el, "held its message hidden at load and showed it later"]);
        }
      }
      return out;
    },
    oversStart() { overs = []; },
    oversStop() { const got = overs || []; overs = null; return got; },
  };
})();
"""


TableError = rule_table.TableError


def parse(text):
    """The table's lines as Line records, in order, each value a dict."""
    return rule_table.parse(text, CHECKS, _line_value)


def _line_value(n, check, m):
    value = {}
    for key, got in (m.groupdict() if m else {}).items():
        if key.startswith("n_"):
            value[key[2:]] = float(got)
        elif key == "words":
            value[key] = [w.strip().lower() for w in got.split(",") if w.strip()]
        elif key == "rules":
            value[key] = tuple(got.split())
        else:
            value[key] = got
    return value


def _off_site(page_url, href):
    u, p = urllib.parse.urlsplit(href), urllib.parse.urlsplit(page_url)
    return u.scheme in ("http", "https") and (u.scheme, u.netloc) != (
        p.scheme,
        p.netloc,
    )


def guard(context, start):
    """Answers every page load off `start`'s site in `context` with a blank
    page, so no check reaches a live site; what a page loads from elsewhere
    to draw itself still loads."""

    def answer(route):
        if route.request.is_navigation_request():
            route.fulfill(
                status=200, content_type="text/html", body="<title>outside</title>"
            )
        else:
            route.continue_()

    context.route(lambda url: _off_site(start, url), answer)


class Run:
    def __init__(self, browser, url, *, parts, absent, handover, timeout):
        self.browser = browser
        self.url = url
        self.parts = parts
        self.absent = absent
        self.handover = handover
        self.timeout = timeout
        self.popups = []

    @contextlib.contextmanager
    def page(self, url=None, **cond):
        """The page loaded afresh under `cond` (conditions.open_page's), the
        tap loaded before its own scripts, and settled."""
        with conditions.open_page(
            self.browser,
            url or self.url,
            init_scripts=(pointer.WATCH_JS, TAP_JS),
            viewport=VIEWPORT,
            **cond,
        ) as page:
            page.set_default_timeout(overlay.ACTION_TIMEOUT_MS)
            page.set_default_navigation_timeout(self.timeout)
            page.context.on("page", lambda p: self.popups.append(p))
            guard(page.context, self.url)
            pointer.settle(page)
            sheets(page)
            yield page

    def part(self, line, ans):
        name = line.value["part"]
        if name in self.parts:
            return self.parts[name]
        if name not in self.absent:
            ans.unjudged(
                line, None, f"no selector for the part {name}: declare it in --parts"
            )
        return None


def _items(handle):
    props = handle.get_properties()
    return [props[str(i)] for i in range(len(props))]


def elements(page, js, arg=None):
    """The elements an in-page expression returns, as ElementHandles."""
    return [h.as_element() for h in _items(page.evaluate_handle(js, arg))]


def info(page, el):
    return page.evaluate("(el) => __st.info(el)", el)


def drawn(page, el):
    return page.evaluate("(el) => __st.drawn(el)", el)


def style(page, el, props=LOOK_PROPS):
    return page.evaluate("([el, props]) => __st.style(el, props)", [el, props])


def quick(page):
    """Two animation frames: long enough for a handler and its re-render."""
    page.evaluate(
        "() => new Promise((f) => requestAnimationFrame(() => requestAnimationFrame(f)))"
    )


def blur(page):
    page.evaluate("() => document.activeElement?.blur()")


def rest(page):
    """The pointer off the page and focus on its body, so no part shows hover or focus."""
    page.mouse.move(0, 0)
    blur(page)
    quick(page)


def sheets(page):
    """Hands the page the text of every style sheet it holds, read through
    Chromium's CSS domain, for the tap to find its :hover rules in."""
    cdp = page.context.new_cdp_session(page)
    ids = []
    cdp.on("CSS.styleSheetAdded", lambda e: ids.append(e["header"]["styleSheetId"]))
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    texts = [
        cdp.send("CSS.getStyleSheetText", {"styleSheetId": i})["text"] for i in ids
    ]
    cdp.detach()
    page.evaluate("(texts) => { window.__stSheets = texts; }", texts)


def reload(run, page):
    """The page loaded afresh from the run's URL, wherever the last step left it."""
    page.goto(run.url)
    pointer.settle(page)
    sheets(page)


def gone(page, url0):
    """Whether the page has left the document it was on."""
    from playwright.sync_api import Error as PlaywrightError

    try:
        return page.url != url0 or not page.evaluate("() => !!window.__st")
    except PlaywrightError:
        # An evaluate the page's own navigation cut short is it leaving (#312).
        return True


def rgb(css):
    """A computed colour as (r, g, b) in 0–255."""
    nums = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", css)]
    if "srgb" in css:
        return tuple(round(n * 255) for n in nums[:3])
    return tuple(nums[:3])


def luminance(c):
    def lin(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = c
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def reveals(page, el):
    """What resting the pointer on `el` draws that was not drawn before."""
    pointer.leave(page, el)
    page.evaluate("() => __st.mark()")
    pointer.hover(page, el)
    return elements(page, "() => __st.revealed()")


def names(page, els):
    return ", ".join(page.evaluate("(els) => els.map(__st.describe)", els))


def undrawn(page, els):
    return page.evaluate(
        "(els) => els.filter((e) => !__st.drawn(e)).map(__st.describe)", els
    )


def trial(run, page, keep=None, before=None):
    """Clicks each visible button that would not submit a form, on the page
    reloaded before each, and yields (button, its info, what the click drew).
    `keep` filters the buttons in the page; `before` runs before each click."""
    find = (
        "(keep) => __st.controls(['button']).filter((b) => b.type !== 'submit' && !b.disabled"
        " && b.getAttribute('aria-disabled') !== 'true' && !b.closest('[inert]')"
        " && (!keep || b.matches(keep)))"
    )
    count = len(elements(page, find, keep))
    for i in range(count):
        reload(run, page)
        found = elements(page, find, keep)
        if i >= len(found):
            break
        button = found[i]
        if before:
            before(page)
        page.evaluate("() => __st.mark()")
        try:
            pointer.click(page, button)
        except pointer.PointerError:
            # A button no visitor can reach shows them nothing to judge (#312).
            continue
        yield button, info(page, button), elements(page, "() => __st.revealed()")


# ---- hover --------------------------------------------------------------


def check_reveal(run, line, ans):
    found = []
    with run.page() as page:
        for el in elements(page, "() => __st.hoverTargets()"):
            try:
                shown = reveals(page, el)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, el, exc=exc)
                continue
            if not shown:
                continue
            at, what = info(page, el), names(page, shown)
            pointer.leave(page, el)
            target = page.evaluate_handle("(el) => __st.focusable(el)", el).as_element()
            if target is None:
                ans.miss(
                    line,
                    at,
                    f"hover shows {what}, and nothing there takes focus to show it",
                )
            else:
                page.keyboard.press("Shift")
                target.focus()
                pointer.settle(page)
                missing = undrawn(page, shown)
                if missing:
                    ans.miss(
                        line,
                        at,
                        f"focus does not show {', '.join(missing)}, which hover shows",
                    )
                blur(page)
            found.append((at, [info(page, s)["path"] for s in shown]))
    if not found:
        return
    with run.page(pointer="coarse") as touch:
        for at, paths in found:
            hidden = touch.evaluate(
                "(ps) => ps.filter((p) => !__st.drawn(document.querySelector(p)))",
                paths,
            )
            if hidden:
                ans.miss(
                    line,
                    at,
                    f"where no input can hover, {len(hidden)} part(s) hover shows are not shown",
                )
            ans.met(line)


def check_persist(run, line, ans):
    ms = line.value["ms"]
    with run.page() as page:
        for el in elements(page, "() => __st.hoverTargets()"):
            try:
                shown = reveals(page, el)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, el, exc=exc)
                continue
            if not shown:
                continue
            at = info(page, el)
            page.keyboard.press("Escape")
            pointer.settle(page)
            if not undrawn(page, shown):
                ans.miss(line, at, f"Escape leaves {names(page, shown)} up")
            shown = reveals(page, el)
            if shown:
                try:
                    pointer.hover(page, shown[0])
                    if undrawn(page, shown[:1]):
                        ans.miss(
                            line,
                            at,
                            "what hover shows goes as the pointer moves onto it",
                        )
                except pointer.PointerError as exc:
                    # Content hover shows that the pointer cannot reach is the fault (#312).
                    ans.miss(
                        line, at, f"the pointer cannot reach what hover shows: {exc}"
                    )
            shown = reveals(page, el)
            page.wait_for_timeout(ms)
            if undrawn(page, shown):
                ans.miss(
                    line,
                    at,
                    f"what hover shows goes within {ms:.0f} ms with the pointer still on it",
                )
            ans.met(line)


def _shut(page, ov):
    if overlay.close(page, ov, by="escape")["open"]:
        overlay.close(page, ov, by="click")


def check_click_opens(run, line, ans):
    with run.page() as page:
        for nav in elements(
            page,
            "() => [...document.querySelectorAll('nav, [role=navigation]')].filter(__st.drawn)",
        ):
            ovs = [
                o
                for o in overlay.find(page, within=nav)
                if o.trigger is not None and o.kind != "dialog"
            ]
            for ov in ovs:
                at = info(page, ov.trigger)
                if not overlay.open(page, ov, by="click")["open"]:
                    ans.miss(line, at, "a click does not open it")
                _shut(page, ov)
                if not overlay.open(page, ov, by="keyboard")["open"]:
                    ans.miss(line, at, "Enter does not open it")
                _shut(page, ov)
                ans.met(line)
            targets = elements(
                page, "(nav) => __st.hoverTargets().filter((e) => nav.contains(e))", nav
            )
            for el in targets:
                try:
                    shown = reveals(page, el)
                except pointer.PointerError as exc:
                    # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                    unreached(page, line, ans, el, exc=exc)
                    continue
                if not shown:
                    continue
                at = info(page, el)
                pointer.leave(page, el)
                opened = False
                for ov in ovs:
                    overlay.open(page, ov, by="click")
                    opened = not undrawn(page, shown[:1])
                    _shut(page, ov)
                    if opened:
                        break
                if not opened:
                    ans.miss(
                        line,
                        at,
                        f"hover alone opens {names(page, shown[:1])}: no click or key does",
                    )
                ans.met(line)


def _differs(page, el, rest, kids):
    return (
        style(page, el) != rest or page.evaluate("(el) => __st.shown(el)", el) != kids
    )


def check_editable(run, line, ans):
    sel = run.part(line, ans)
    if sel is None:
        return
    with run.page() as page:
        for el in page.query_selector_all(sel):
            if not drawn(page, el):
                continue
            at = info(page, el)
            pointer.leave(page, el)
            rest, kids = style(page, el), page.evaluate("(el) => __st.shown(el)", el)
            pointer.hover(page, el)
            if not _differs(page, el, rest, kids):
                ans.miss(line, at, "hover leaves its look as it was")
            pointer.leave(page, el)
            target = page.evaluate_handle("(el) => __st.focusable(el)", el).as_element()
            if target is None:
                ans.miss(line, at, "nothing in it takes focus")
            else:
                page.keyboard.press("Shift")
                own = style(page, target)
                target.focus()
                pointer.settle(page)
                if not (_differs(page, el, rest, kids) or style(page, target) != own):
                    ans.miss(line, at, "focus leaves its look as it was")
                blur(page)
            ans.met(line)


BOX_JS = r"""(el) => {
  const box = (e) => { const r = e.getBoundingClientRect(); return [r.left + scrollX, r.top + scrollY, r.width, r.height]; };
  return [el, el.previousElementSibling, el.nextElementSibling].filter(Boolean).map(box);
}"""


def _moved(before, after, px):
    """The largest change in any box's place or size, where above `px`."""
    worst = max(
        (
            abs(a - b)
            for bs, as_ in zip(before, after, strict=False)
            for a, b in zip(bs, as_, strict=False)
        ),
        default=0,
    )
    return worst if worst > px else None


def check_reflow(run, line, ans):
    px = line.value["px"]
    find = (
        "() => __st.distinct([...new Set([...__st.hoverTargets(), ...__st.controls(['button', 'link']),"
        " ...document.querySelectorAll('[role=tab]')])].filter((e) => __st.drawn(e) && __st.text(e)))"
    )
    with run.page() as page:
        for el in elements(page, find):
            at = info(page, el)
            el.scroll_into_view_if_needed()
            try:
                pointer.leave(page, el)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, el, exc=exc)
                continue
            before = page.evaluate(BOX_JS, el)
            try:
                pointer.hover(page, el)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, el, exc=exc)
                continue
            worst = _moved(before, page.evaluate(BOX_JS, el), px)
            if worst:
                ans.miss(
                    line, at, f"hover moves it or its neighbours by {worst:.1f} px"
                )
            pointer.leave(page, el)
            page.keyboard.press("Shift")
            el.focus()
            pointer.settle(page)
            worst = _moved(before, page.evaluate(BOX_JS, el), px)
            if worst:
                ans.miss(
                    line, at, f"focus moves it or its neighbours by {worst:.1f} px"
                )
            blur(page)
            if page.evaluate(
                "(el) => el.getAttribute('role') === 'tab' && el.getAttribute('aria-selected') !== 'true'",
                el,
            ):
                pointer.click(page, el)
                pointer.leave(page, el)
                worst = _moved(before[:1], page.evaluate(BOX_JS, el)[:1], px)
                if worst:
                    ans.miss(
                        line, at, f"selecting it changes its box by {worst:.1f} px"
                    )
            ans.met(line)


def check_states(run, line, ans):
    with run.page() as page:
        count = len(
            elements(
                page, "() => __st.distinct(__st.controls(['button', 'link', 'field']))"
            )
        )
        for i in range(count):
            el = elements(
                page, "() => __st.distinct(__st.controls(['button', 'link', 'field']))"
            )[i]
            at = info(page, el)
            kind = page.evaluate(
                "(el) => el.matches('a[href], [role=link]') ? 'link' : el.matches('input, select, textarea') ? 'field' : 'button'",
                el,
            )
            disabled = page.evaluate(
                "(el) => el.disabled || el.getAttribute('aria-disabled') === 'true'", el
            )
            el.scroll_into_view_if_needed()
            try:
                pointer.leave(page, el)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, el, exc=exc)
                continue
            rest = style(page, el)
            if disabled:
                page.evaluate(
                    "(el) => { el.disabled = false; el.removeAttribute('aria-disabled'); }",
                    el,
                )
                pointer.settle(page)
                if style(page, el) == rest:
                    ans.miss(line, at, "its disabled look is its live look")
                reload(run, page)
                ans.met(line)
                continue
            seen = {}
            try:
                pointer.hover(page, el)
                seen["hover"] = style(page, el)
                pointer.leave(page, el)
                page.keyboard.press("Shift")
                el.focus()
                pointer.settle(page)
                seen["focus"] = style(page, el)
                blur(page)
                if kind != "field":
                    pointer.hover(page, el)
                    pointer.press(page, el)
                    seen["press"] = style(page, el)
                    pointer.leave(page, el)
                    pointer.release(page)
                    blur(page)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, el, exc=exc)
                continue
            same = [k for k, s in seen.items() if s == rest]
            if (
                "press" in seen
                and seen["press"] == seen["hover"]
                and "hover" not in same
            ):
                same.append("press, as hover")
            if same:
                ans.miss(
                    line, at, f"its {', '.join(same)} state looks as its rest state"
                )
            if gone(page, page.url):
                reload(run, page)
            ans.met(line)


def _inverse(page, el, lum):
    """What is wrong with `el`'s surface, as an inverse surface, or None."""
    surface = rgb(page.evaluate("(el) => __st.background(el)", el))
    ground = rgb(page.evaluate("(el) => __st.background(el.parentElement)", el))
    ink = rgb(page.evaluate("(el) => getComputedStyle(el).color", el))
    if (luminance(surface) > lum) == (luminance(ground) > lum):
        return "sits on a surface of the page's own lightness, not the inverse"
    if (luminance(ink) > lum) == (luminance(surface) > lum):
        return "its text is not the inverse text"
    return None


def check_inverse(run, line, ans):
    lum = line.value["lum"]
    with run.page() as page:
        for el in elements(page, "() => __st.hoverTargets()"):
            try:
                shown = reveals(page, el)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, el, exc=exc)
                continue
            tips = elements(
                page,
                "(els) => els.flatMap((e) => [e, ...e.querySelectorAll('[role=tooltip]')]).filter((e) => e.getAttribute('role') === 'tooltip')",
                shown,
            )
            for tip in tips:
                wrong = _inverse(page, tip, lum)
                if wrong:
                    ans.miss(line, info(page, tip), f"a tooltip {wrong}")
                ans.met(line)
        toast = run.parts.get("toast")
        for _, _at, shown in trial(run, page):
            toasts = elements(
                page,
                "([els, sel]) => els.filter((e) => (sel && e.matches(sel)) || __st.liveOf(e))",
                [shown, toast],
            )
            for t in toasts:
                if not page.evaluate("(e) => __st.text(e)", t):
                    continue
                wrong = _inverse(page, t, lum)
                if wrong:
                    ans.miss(line, info(page, t), f"a toast {wrong}")
                ans.met(line)


# ---- press, keys and focus ---------------------------------------------

DEFAULT_JS = r"""(dialog) => {
  const buttons = [...dialog.querySelectorAll('button, input[type=submit], input[type=button], [role=button]')].filter(__st.drawn);
  if (buttons.length < 2) return null;
  const active = document.activeElement;
  if (active && dialog.contains(active) && buttons.includes(active)) return active;
  const f = dialog.querySelector('form');
  return f ? f.querySelector('button:not([type=button]):not([type=reset]), input[type=submit]') : null;
}"""


def check_default(run, line, ans):
    words = line.value["words"]
    with run.page() as page:
        for ov in overlay.find(page):
            if ov.kind != "dialog":
                continue
            if (
                ov.trigger is not None
                and not overlay.open(page, ov, by="click")["open"]
            ):
                continue
            got = page.evaluate_handle(DEFAULT_JS, ov.target).as_element()
            if got is not None:
                name = page.evaluate("(el) => __st.nameOf(el)", got).lower().strip(" ×")
                if name in words:
                    ans.miss(
                        line,
                        info(page, got),
                        f"the button the dialog opens on, or Return presses, is {name}",
                    )
                ans.met(line)
            _shut(page, ov)


SHAPE_JS = r"""([el, props]) => ({
  pressed: el.getAttribute("aria-pressed"),
  shape: Object.fromEntries(Object.entries(__st.style(el, props)).map(([k, v]) =>
    [k, v.replace(/rgba?\([^)]*\)|color\([^)]*\)/g, "")])),
  text: __st.text(el),
  shown: __st.shown(el),
})"""


def check_toggle(run, line, ans):
    with run.page() as page:
        for el in elements(
            page,
            "() => [...document.querySelectorAll('[aria-pressed]')].filter(__st.drawn)",
        ):
            at = info(page, el)
            try:
                pointer.leave(page, el)
                blur(page)
                off = page.evaluate(SHAPE_JS, [el, SHAPE_PROPS])
                pointer.click(page, el)
                pointer.leave(page, el)
                blur(page)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, el, exc=exc)
                continue
            on = page.evaluate(SHAPE_JS, [el, SHAPE_PROPS])
            if on["pressed"] == off["pressed"]:
                ans.miss(
                    line, at, f"pressing it leaves aria-pressed at {off['pressed']}"
                )
            elif {k: on[k] for k in ("shape", "text", "shown")} == {
                k: off[k] for k in ("shape", "text", "shown")
            }:
                ans.miss(line, at, "its on and off states differ only in colour")
            pointer.click(page, el)
            ans.met(line)


PRESSABLE = (
    "() => [...document.querySelectorAll('button, a[href], [role=button], [role=link], [role=tab],"
    " [role=menuitem], [role=option], summary, input[type=submit], input[type=button]')]"
    ".filter((e) => __st.drawn(e) && !e.disabled)"
)


def check_release(run, line, ans):
    words = line.value["words"]
    with run.page() as page:
        count = len(elements(page, PRESSABLE))
        for i in range(count):
            found = elements(page, PRESSABLE)
            if i >= len(found):
                break
            el, url0 = found[i], page.url
            at = info(page, el)
            run.popups.clear()
            try:
                pointer.hover(page, el)
                # Focused first, so what a focus or blur handler writes is not
                # read as the press acting.
                el.focus()
                quick(page)
                was, undo0 = page.evaluate(SEEN_JS), _named(page, words)
                page.evaluate("(el) => __st.watch(el)", el)
                pointer.press(page, el)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, el, exc=exc)
                continue
            acted = (
                ["loaded another page"]
                if gone(page, url0)
                else page.evaluate("() => __st.acts()")
            )
            acted += ["opened a window"] * bool(run.popups)
            undo = acted and not gone(page, url0) and not undo0 and _named(page, words)
            if not gone(page, url0):
                pointer.leave(page, el)
            pointer.release(page)
            quick(page)
            if acted and (gone(page, url0) or page.evaluate(SEEN_JS) != was):
                (ans.review if undo else ans.miss)(
                    line,
                    at,
                    f"acts on the press, before release: {'; '.join(acted[:3])}"
                    + (f", and shows {undo}" if undo else ""),
                )
            if acted:
                page.goto(run.url)
                pointer.settle(page)
            ans.met(line)


# What a press could leave changed: the page's text and every state attribute.
SEEN_JS = r"""() => [document.body.innerText,
  ...[...document.querySelectorAll('[aria-pressed], [aria-expanded], [aria-checked], [aria-selected], input')]
    .map((el) => [el.getAttribute('aria-pressed'), el.getAttribute('aria-expanded'),
      el.getAttribute('aria-checked'), el.getAttribute('aria-selected'), el.checked, el.value].join())]"""


def _named(page, words):
    """The first drawn button, link or box named with one of `words`, or None."""
    return page.evaluate(
        """(words) => { const el = __st.controls(['button', 'link', 'box'])
          .find((c) => words.some((w) => __st.nameOf(c).toLowerCase().includes(w)));
          return el ? __st.describe(el) : null; }""",
        words,
    )


def check_single_key(run, line, ans):
    words = line.value["words"]
    with run.page() as page:
        url0 = page.url
        for key in KEYS:
            blur(page)
            page.evaluate("() => __st.watch()")
            run.popups.clear()
            page.keyboard.press(key)
            quick(page)
            if gone(page, url0):
                ans.miss(line, None, f"the key {key!r} loads another page")
                page.goto(run.url)
                pointer.settle(page)
                continue
            acted = page.evaluate("() => __st.acts()")
            moved = page.evaluate(
                "() => document.activeElement !== document.body && __st.info(document.activeElement)"
            )
            if run.popups:
                acted.append("opened a window")
            if moved:
                acted.append(f"moved focus to {moved['where']}")
            if acted:
                at = moved or None
                setting = _named(page, words)
                (ans.review if setting else ans.miss)(
                    line,
                    at,
                    f"the key {key!r}, pressed with focus on the page, {'; '.join(acted[:3])}"
                    + (f"; {setting} may turn it off" if setting else ""),
                )
                reload(run, page)
        ans.met(line)


def check_on_focus(run, line, ans):
    with run.page() as page:
        count = len(elements(page, "() => __st.tabbables()"))
        for i in range(count):
            found = elements(page, "() => __st.tabbables()")
            if i >= len(found):
                break
            el, url0 = found[i], page.url
            at = info(page, el)
            dialogs = page.evaluate("() => __st.dialogs()")
            page.evaluate("(el) => __st.watch(el)", el)
            run.popups.clear()
            el.focus()
            quick(page)
            if gone(page, url0):
                ans.miss(line, at, "taking focus loads another page")
                page.goto(run.url)
                pointer.settle(page)
                continue
            changed = page.evaluate("() => __st.acts(['submit', 'window'])")
            if run.popups and not changed:
                changed.append("opened a window")
            if page.evaluate("() => __st.dialogs()") > dialogs:
                changed.append("opened a dialog")
            if not page.evaluate("(el) => document.activeElement === el", el):
                moved = page.evaluate("() => __st.describe(document.activeElement)")
                changed.append(f"moved focus to {moved}")
            if changed:
                ans.miss(line, at, f"taking focus {'; '.join(changed)}")
                reload(run, page)
            ans.met(line)


PLAYERS_JS = r"""(sel) => {
  const out = [];
  for (const m of document.querySelectorAll("video[controls], audio[controls]")) if (__st.drawn(m)) out.push([m, m]);
  for (const box of sel ? document.querySelectorAll(sel) : []) {
    const m = box.matches("video, audio") ? box : box.querySelector("video, audio");
    if (!m || m.controls) continue;
    const buttons = [...box.querySelectorAll('button, [role=button]')].filter(__st.drawn);
    const play = buttons.find((b) => /play|pause/i.test(__st.nameOf(b))) || buttons[0];
    if (play) out.push([m, play]);
  }
  return out;
}"""


def check_space(run, line, ans):
    sel = run.parts.get(line.value["part"])
    with run.page() as page:
        pairs = [
            [h.as_element() for h in _items(p)]
            for p in _items(page.evaluate_handle(PLAYERS_JS, sel))
        ]
        for media, control in pairs:
            at = info(page, control)
            paused = page.evaluate("(m) => m.paused", media)
            control.focus()
            page.keyboard.press(" ")
            pointer.settle(page)
            if page.evaluate("(m) => m.paused", media) == paused:
                ans.miss(
                    line,
                    at,
                    "Space with the player focused neither plays nor pauses it",
                )
            page.evaluate("(m) => m.pause()", media)
            ans.met(line)
        if pairs:
            blur(page)
            before = [page.evaluate("(m) => m.paused", m) for m, _ in pairs]
            page.keyboard.press(" ")
            pointer.settle(page)
            for (media, _), was in zip(pairs, before, strict=True):
                if page.evaluate("(m) => m.paused", media) != was:
                    ans.miss(
                        line,
                        info(page, media),
                        "Space with focus elsewhere plays or pauses it",
                    )
    if sel is None and line.value["part"] not in run.absent and not pairs:
        ans.unjudged(
            line,
            None,
            f"no native player, and no selector for the part {line.value['part']}",
        )


def _value(page, el):
    return page.evaluate("(el) => __st.sliderValue(el)", el)


def _click_track(page, el, fraction):
    track = page.evaluate_handle("(el) => __st.track(el)", el).as_element()
    pointer.click(page, track, at=(fraction, 0.5))


def check_slider_keys(run, line, ans):
    find = "() => __st.sliders()"
    with run.page() as page:
        url0 = page.url
        for i in range(len(elements(page, find))):
            # A track click that left the page leaves the next slider's handle in the old one (#458).
            if gone(page, url0):
                reload(run, page)
            found = elements(page, find)
            if i >= len(found):
                break
            el = found[i]
            at = info(page, el)
            low, high = page.evaluate("(el) => __st.sliderEnds(el)", el)
            wrong = []

            def key(name, el=el):
                page.keyboard.press(name)
                quick(page)
                return _value(page, el)

            el.focus()
            if key("Home") != low:
                wrong.append("Home")
            if key("End") != high:
                wrong.append("End")
            key("Home")
            last = low
            for name, rises in (
                ("ArrowRight", True),
                ("ArrowUp", True),
                ("ArrowLeft", False),
                ("ArrowDown", False),
            ):
                now = key(name)
                if (now > last) != rises or now == last:
                    wrong.append(name)
                last = now
            key("End")
            try:
                _click_track(page, el, TRACK_CLICK)
                if gone(page, url0):
                    wrong.append("a click on its track (leaves the page)")
                elif _value(page, el) >= high:
                    wrong.append("a click on its track")
            except pointer.PointerError:
                # A track the pointer cannot click is the fault (#312).
                wrong.append("a click on its track (covered)")
            if wrong:
                ans.miss(
                    line,
                    at,
                    f"{', '.join(wrong)} does not move it as the slider keys do",
                )
            ans.met(line)


def check_direction(run, line, ans):
    for rtl in (False, True):
        with run.page(rtl=rtl) as page:
            for el in elements(page, "() => __st.sliders()"):
                at = info(page, el)
                start, end = TRACK_ENDS[::-1] if rtl else TRACK_ENDS
                try:
                    _click_track(page, el, start)
                    at_start = _value(page, el)
                    _click_track(page, el, end)
                    at_end = _value(page, el)
                except pointer.PointerError as exc:
                    # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                    unreached(page, line, ans, el, exc=exc)
                    continue
                side = "right to left" if rtl else "left to right"
                if not at_start < at_end:
                    ans.miss(
                        line,
                        at,
                        f"in a {side} page its lowest value is not at the reading start",
                    )
                if rtl:
                    el.focus()
                    page.keyboard.press("Home")
                    low = _value(page, el)
                    page.keyboard.press("ArrowLeft")
                    quick(page)
                    if not _value(page, el) > low:
                        ans.miss(
                            line,
                            at,
                            "in a right to left page ArrowLeft does not raise it",
                        )
                ans.met(line)


def check_drag(run, line, ans):
    find = "() => __st.sliders().filter((e) => e.localName !== 'input')"
    with run.page() as page:
        for i in range(len(elements(page, find))):
            reload(run, page)
            el = elements(page, find)[i]
            at = info(page, el)
            track = page.evaluate_handle("(el) => __st.track(el)", el).as_element()
            t, b = track.bounding_box(), el.bounding_box()
            if not t or not b:
                continue
            dx = t["x"] + t["width"] + DRAG_PAST[0] - (b["x"] + b["width"] / 2)
            dy = t["height"] + DRAG_PAST[1]
            _, high = page.evaluate("(el) => __st.sliderEnds(el)", el)
            page.evaluate(
                "() => { getSelection().removeAllRanges(); __st.oversStart(); }"
            )
            try:
                pointer.drag(page, el, (dx, dy), hold=True)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, el, exc=exc)
                continue
            value = _value(page, el)
            others = page.evaluate(
                "(track) => [...new Set(__st.oversStop().filter((e) => !track.contains(e) && !e.contains(track)))].map(__st.describe)",
                track,
            )
            selected = page.evaluate("() => getSelection().toString().trim()")
            page.mouse.up()
            if value != high:
                ans.miss(
                    line,
                    at,
                    "it stops following the pointer once the pointer leaves it",
                )
            if others:
                ans.miss(
                    line,
                    at,
                    f"while dragged, the pointer passes over {', '.join(others[:3])}",
                )
            if selected:
                ans.miss(line, at, "dragging it selects text")
            ans.met(line)


SCROLLERS_JS = r"""() => [...document.querySelectorAll("body *")].filter((el) => {
  const cs = getComputedStyle(el);
  return /auto|scroll/.test(cs.overflowX) && el.scrollWidth > el.clientWidth + 1 && __st.drawn(el);
})"""

CAROUSEL_JS = r"""(el) => {
  const named = el.closest('[aria-roledescription="carousel"]');
  if (named) return named;
  return /x|both|inline/.test(getComputedStyle(el).scrollSnapType) ? el.parentElement : null;
}"""


def check_wheel(run, line, ans):
    with run.page() as page:
        for el in elements(page, SCROLLERS_JS):
            at = info(page, el)
            half = max(WHEEL_MIN, page.evaluate("(el) => el.clientWidth / 2", el))

            def moved(shift, el=el, half=half):
                page.evaluate("(el) => { el.scrollLeft = 0; }", el)
                if shift:
                    page.keyboard.down("Shift")
                try:
                    pointer.wheel(page, el, dy=half) if shift else pointer.wheel(
                        page, el, dx=half
                    )
                finally:
                    if shift:
                        page.keyboard.up("Shift")
                return page.evaluate("(el) => el.scrollLeft", el) > 0

            try:
                if not moved(False):
                    ans.miss(
                        line, at, "a sideways wheel or trackpad swipe does not move it"
                    )
                if not moved(True):
                    ans.miss(line, at, "Shift with the wheel does not move it")
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, el, exc=exc)
                continue
            box = page.evaluate_handle(CAROUSEL_JS, el).as_element()
            if box is not None:
                ways = set()
                for b in elements(
                    page,
                    "(box) => [...box.querySelectorAll('button, [role=button]')].filter(__st.drawn)",
                    box,
                ):
                    for start, way in (("0", "next"), ("el.scrollWidth", "previous")):
                        page.evaluate(
                            f"(el) => {{ el.scrollTo({{ left: {start}, behavior: 'instant' }}); }}",
                            el,
                        )
                        left = page.evaluate("(el) => el.scrollLeft", el)
                        try:
                            pointer.click(page, b)
                        except pointer.PointerError:
                            # A control no pointer reaches is no way to move it (#312).
                            continue
                        now = page.evaluate("(el) => el.scrollLeft", el)
                        if (now > left and way == "next") or (
                            now < left and way == "previous"
                        ):
                            ways.add(way)
                if ways != {"next", "previous"}:
                    ans.miss(
                        line,
                        at,
                        "a carousel with no previous and next controls inside it that move it",
                    )
            ans.met(line)


WHOLE_JS = r"""(inset) => {
  const ACT = 'a[href], button, [role=button], [role=link], summary, input, select, textarea';
  const out = [];
  for (const c of document.querySelectorAll('li, tr, [role=row], [role=listitem], [role=option], article')) {
    if (!__st.drawn(c) || c.matches(ACT)) continue;
    const acts = [...c.querySelectorAll(ACT)].filter(__st.drawn);
    if (acts.length !== 1 || !__st.edged(c)) continue;
    const t = acts[0];
    c.scrollIntoView({ block: "center" });
    const r = c.getBoundingClientRect();
    const xs = [r.left + inset, (r.left + r.right) / 2, r.right - inset];
    const ys = [r.top + inset, (r.top + r.bottom) / 2, r.bottom - inset];
    const off = [];
    for (const x of xs) for (const y of ys) {
      const hit = document.elementFromPoint(x, y);
      if (!hit || !(hit === t || t.contains(hit))) off.push(`${Math.round(x - r.left)},${Math.round(y - r.top)}`);
    }
    out.push({ at: __st.info(c), target: __st.describe(t), off });
  }
  return out;
}"""


def check_whole(run, line, ans):
    with run.page() as page:
        for got in page.evaluate(WHOLE_JS, line.value["px"]):
            if got["off"]:
                ans.miss(
                    line,
                    got["at"],
                    f"only part of it reaches {got['target']}: not at {'; '.join(got['off'][:4])}",
                )
            ans.met(line)


RECT_JS = r"""(el) => {
  const c = el.querySelector("img, svg, canvas, video") || el;
  const r = c.getBoundingClientRect();
  return [r.left, r.top, r.width, r.height];
}"""


def check_pinch(run, line, ans):
    sel = run.part(line, ans)
    if sel is None:
        return
    with run.page(pointer="coarse") as page:
        cdp = page.context.new_cdp_session(page)
        for i in range(len(page.query_selector_all(sel))):
            reload(run, page)
            el = page.query_selector_all(sel)[i]
            if not drawn(page, el):
                continue
            at = info(page, el)
            el.scroll_into_view_if_needed()
            box = el.bounding_box()
            mx = box["x"] + PINCH_AT * box["width"]
            my = box["y"] + PINCH_AT * box["height"]
            x0, y0, w0, h0 = page.evaluate(RECT_JS, el)
            spread = min(box["width"], box["height"]) * PINCH_SPREAD

            def touch(kind, d, mx=mx, my=my):
                points = (
                    []
                    if d is None
                    else [
                        {"x": mx - d, "y": my, "id": 1},
                        {"x": mx + d, "y": my, "id": 2},
                    ]
                )
                cdp.send(
                    "Input.dispatchTouchEvent", {"type": kind, "touchPoints": points}
                )

            touch("touchStart", PINCH_START)
            for step in range(1, PINCH_STEPS + 1):
                touch("touchMove", PINCH_START + spread * step / PINCH_STEPS)
            quick(page)
            x1, y1, w1, h1 = page.evaluate(RECT_JS, el)
            touch("touchEnd", None)
            if w1 / w0 < line.value["zoom"]:
                ans.unjudged(line, at, "a two-finger spread did not zoom it")
                continue
            px = x1 + (mx - x0) / w0 * w1
            py = y1 + (my - y0) / h0 * h1
            drift = math.hypot(px - mx, py - my)
            if drift > line.value["px"]:
                ans.miss(
                    line,
                    at,
                    f"the point between the fingers drifts {drift:.0f} px as they spread",
                )
            ans.met(line)


FRAGMENTS_JS = r"""() => [...document.querySelectorAll('a[href^="#"]')].filter((a) => {
  if (!__st.drawn(a) || a.getAttribute("href").length < 2) return false;
  const t = document.getElementById(decodeURIComponent(a.hash.slice(1)));
  return t && !t.matches("main, body, html");
})"""


def check_target(run, line, ans):
    ratio = line.value["ratio"]
    with run.page() as page:
        count = len(elements(page, FRAGMENTS_JS))
        for i in range(count):
            page.goto(run.url)
            pointer.settle(page)
            link = elements(page, FRAGMENTS_JS)[i]
            target = page.evaluate_handle(
                "(a) => document.getElementById(decodeURIComponent(a.hash.slice(1)))",
                link,
            ).as_element()
            at = info(page, target)
            before = style(page, target, TARGET_PROPS)
            try:
                pointer.click(page, link)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, link, exc=exc)
                continue
            after = style(page, target, TARGET_PROPS)
            sides = [
                p
                for p in TARGET_PROPS
                if p.startswith("border") and after[p] != before[p]
            ]
            if sides or after["box-shadow"] != before["box-shadow"]:
                ans.met(line)
                continue
            if (
                after["background-color"] == before["background-color"]
                and after["background-image"] == before["background-image"]
            ):
                ans.miss(
                    line, at, "the part a fragment link lands on takes no highlight"
                )
            else:
                fill = rgb(page.evaluate("(el) => __st.background(el)", target))
                ground = rgb(
                    page.evaluate("(el) => __st.background(el.parentElement)", target)
                )
                got = contrast(fill, ground)
                if got > ratio:
                    ans.miss(
                        line,
                        at,
                        f"its :target fill is {got:.2f}:1 on its ground, louder than {ratio}:1",
                    )
            ans.met(line)


VISITED_JS = r"""() => {
  const page = location.href.split("#")[0];
  const ok = (a) => __st.drawn(a) && !a.getAttribute("href").startsWith("#") && a.href.split("#")[0] !== page;
  const chrome = 'nav, [role=navigation], header, footer';
  const content = [...document.querySelectorAll("main li a[href]")]
    .filter((a) => ok(a) && !a.closest(chrome) && !a.querySelector("h1, h2, h3, h4, h5, h6, img, p") && !__st.edged(a.closest("li")));
  const nav = [...document.querySelectorAll(`:is(${chrome}) a[href]`)].filter(ok);
  return [...content.map((a) => ["content", __st.pathOf(a), a.href]), ...nav.map((a) => ["nav", __st.pathOf(a), a.href])];
}"""


def _ink(png):
    """The background and the ink of a link's picture: the commonest colour,
    and the one that contrasts with it most."""
    from PIL import Image

    img = Image.open(io.BytesIO(png)).convert("RGB")
    counts = img.getcolors(img.width * img.height)
    ground = max(counts)[1]
    ink = max((c for _, c in counts), key=lambda c: contrast(c, ground))
    return ground, ink


def _saturation(c):
    return colorsys.rgb_to_hsv(*(v / 255 for v in c))[1]


def check_visited(run, line, ans):
    from playwright.sync_api import Error as PlaywrightError

    ratio = line.value["ratio"]
    folder = tempfile.mkdtemp(prefix="check-state-")
    try:
        try:
            context = run.browser.browser_type.launch_persistent_context(
                folder, channel="chromium", viewport=VIEWPORT
            )
        except PlaywrightError as exc:
            # A browser that will not launch leaves visited colours unread, said as not judged (#312).
            ans.unjudged(
                line,
                None,
                f":visited needs Playwright's full Chromium, which did not start: {flow.first_line(exc)}",
            )
            return
        try:
            guard(context, run.url)
            context.add_init_script(pointer.WATCH_JS)
            context.add_init_script(TAP_JS)
            page = context.new_page()
            page.set_default_timeout(overlay.ACTION_TIMEOUT_MS)
            page.goto(run.url)
            pointer.settle(page)
            links, seen = [], set()
            for kind, path, href in page.evaluate(VISITED_JS):
                if href not in seen:
                    seen.add(href)
                    links.append((kind, path))
            rest(page)
            before = {path: page.query_selector(path).screenshot() for _, path in links}
            for _, path in links:
                page.query_selector(path).click()
                page.wait_for_load_state()
                page.go_back()
                pointer.settle(page)
            rest(page)
            for kind, path in links:
                el = page.query_selector(path)
                at, after = info(page, el), el.screenshot()
                if kind == "nav":
                    if after != before[path]:
                        ans.miss(line, at, "a navigation link shows a visited colour")
                elif after == before[path]:
                    ans.miss(line, at, "once visited it looks as it did")
                else:
                    ground, was = _ink(before[path])
                    _, now = _ink(after)
                    if not _saturation(now) < _saturation(was):
                        ans.miss(
                            line,
                            at,
                            "its visited colour is no less saturated than its link colour",
                        )
                    if contrast(now, ground) < ratio:
                        ans.miss(
                            line,
                            at,
                            f"its visited colour is {contrast(now, ground):.2f}:1 on its ground, under {ratio}:1",
                        )
                ans.met(line)
        finally:
            context.close()
    finally:
        shutil.rmtree(folder, ignore_errors=True)


# ---- forms ----------------------------------------------------------------

FORMS_JS = (
    "() => [...document.querySelectorAll('form')].filter(__st.drawn).map(__st.pathOf)"
)


def _checked_fields(page, sel):
    """The text fields of the form at `sel` the browser checks, in order."""
    return [
        f
        for f in form.fields(page, sel)
        if (
            f.required
            or f.pattern
            or f.min_length
            or f.type in ("email", "url", "tel", "number")
        )
        and f.tag != "select"
        and f.type not in ("radio", "checkbox")
    ]


def _checked_field(page, sel):
    """The first field of the form at `sel` the browser checks, or None."""
    return next(iter(_checked_fields(page, sel)), None)


def _planted(page, sel, key, bad):
    """The value fill() gives the field `key`, a planted bad one where `bad`."""
    for f in form.fill(page, sel, bad=[key] if bad else ()):
        if f.key == key:
            return f.value if isinstance(f.value, str) else None
    return None


def _error(page, key, base):
    """Whether the field `key` shows an error: aria-invalid, or the text its
    aria-describedby or aria-errormessage names changed from `base`."""
    for f in form.read(page)["fields"]:
        if f["key"] == key:
            return f["invalid"] or f["described"] != base
    return False


def _described(page, key):
    for f in form.read(page)["fields"]:
        if f["key"] == key:
            return f["described"]
    return []


def check_timing(run, line, ans):
    with run.page() as page:
        for sel in page.evaluate(FORMS_JS):
            reload(run, page)
            for field in _checked_fields(page, sel):
                bad = _planted(page, sel, field.key, True)
                reload(run, page)
                good = _planted(page, sel, field.key, False)
                reload(run, page)
                if bad and good:
                    break
            else:
                continue
            at = info(page, page.query_selector(field.key))
            several = len(form.fields(page, sel)) > 1
            base = _described(page, field.key)
            page.focus(field.key)
            for ch in bad:
                page.keyboard.type(ch)
                quick(page)
                if _error(page, field.key, base):
                    ans.miss(
                        line, at, "shows an error while a first entry is still typed"
                    )
                    break
            page.keyboard.press("Tab")
            pointer.settle(page)
            shown = _error(page, field.key, base)
            if several and not shown:
                ans.miss(
                    line,
                    at,
                    "shows no error on leaving the field, in a form of several fields",
                )
            if not several:
                if shown:
                    ans.miss(
                        line,
                        at,
                        "a one-question page checks it on leaving the field, before submit",
                    )
                url0 = page.url
                if _submit(page, sel) is None or gone(page, url0):
                    ans.met(line)
                    continue
                if not _error(page, field.key, base):
                    ans.miss(line, at, "shows no error on submit")
            if _error(page, field.key, base):
                page.focus(field.key)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                for ch in good:
                    page.keyboard.type(ch)
                quick(page)
                if _error(page, field.key, base):
                    ans.miss(
                        line, at, "keeps its error after the keystroke that fixes it"
                    )
            ans.met(line)


AUTH_JS = r"""() => {
  const TOKENS = ["username", "current-password", "new-password", "one-time-code"];
  const text = 'input:not([type]), input[type=text], input[type=email], input[type=password], input[type=tel],'
    + ' input[type=number], input[type=url], input[type=search], textarea';
  const auth = (el) => el.type === "password" || TOKENS.some((t) => (el.autocomplete || "").split(/\s+/).includes(t))
    || !!el.form?.querySelector('input[type=password], [autocomplete~="one-time-code"]');
  const fields = [...document.querySelectorAll(text)].filter((el) => __st.drawn(el) && !el.disabled && !el.readOnly);
  const boxes = fields.filter((el) => el.maxLength === 1);
  const groups = [];
  for (const el of boxes) {
    const g = boxes.filter((b) => b.parentElement === el.parentElement);
    if (g.length > 1 && g[0] === el) groups.push(g);
  }
  return { fields: fields.filter((el) => el.maxLength !== 1).map((el) => [el, auth(el)]), groups };
}"""

DROP_JS = r"""([el, text]) => {
  const before = el.value;
  const data = new DataTransfer();
  data.setData("text/plain", text);
  const e = new DragEvent("drop", { bubbles: true, cancelable: true, dataTransfer: data });
  el.dispatchEvent(e);
  return e.defaultPrevented && el.value === before;
}"""

CLIPBOARD = ("clipboard-read", "clipboard-write")


def _paste(page, el, text):
    el.fill("")
    page.evaluate("(t) => navigator.clipboard.writeText(t)", text)
    el.focus()
    page.keyboard.press("Control+V")
    quick(page)


def _paste_check(run, line, ans, want_auth):
    with run.page(permissions=list(CLIPBOARD)) as page:
        got = page.evaluate_handle(AUTH_JS)
        for pair in _items(got.get_property("fields")):
            el, auth = (
                pair.get_property("0").as_element(),
                pair.get_property("1").json_value(),
            )
            if auth != want_auth:
                continue
            at = info(page, el)
            _paste(page, el, PASTED)
            if not el.input_value():
                ans.miss(line, at, "a paste into it is blocked")
            if page.evaluate(DROP_JS, [el, PASTED]):
                ans.miss(line, at, "a drop into it is cancelled")
            if want_auth and page.evaluate(
                "(el) => el.type === 'password' && el.autocomplete === 'off'", el
            ):
                ans.miss(
                    line, at, 'autocomplete="off" stops a password manager filling it'
                )
            ans.met(line)
        if want_auth:
            for group in _items(got.get_property("groups")):
                boxes = [b.as_element() for b in _items(group)]
                code = "".join(str((i % 9) + 1) for i in range(len(boxes)))
                _paste(page, boxes[0], code)
                if "".join(b.input_value() for b in boxes) != code:
                    ans.miss(
                        line,
                        info(page, boxes[0]),
                        "pasting the whole code fills only part of its boxes",
                    )
                ans.met(line)


def check_paste(run, line, ans):
    _paste_check(run, line, ans, False)


def check_auth_paste(run, line, ans):
    _paste_check(run, line, ans, True)


INPUTS_JS = r"""() => [...document.querySelectorAll(
  'select, input[type=radio], input[type=checkbox], input[type=range], textarea,'
  + ' input:not([type]), input[type=text], input[type=email], input[type=tel], input[type=number], input[type=search], input[type=url]')]
  .filter((el) => __st.drawn(el) && !el.disabled && !el.readOnly && !(el.type === "radio" && el.checked))"""


def check_on_input(run, line, ans):
    from playwright.sync_api import Error as PlaywrightError

    with run.page() as page:
        count = len(elements(page, INPUTS_JS))
        for i in range(count):
            reload(run, page)
            found = elements(page, INPUTS_JS)
            if i >= len(found):
                break
            el, url0 = found[i], page.url
            at = info(page, el)
            kind = page.evaluate(
                "(el) => el.localName === 'select' ? 'select' : el.type", el
            )
            text = kind not in ("select", "radio", "checkbox", "range")
            el.focus()
            page.evaluate("(el) => __st.watch(el)", el)
            run.popups.clear()
            if kind == "select":
                options = page.evaluate(
                    "(el) => [...el.options].map((o) => o.value)", el
                )
                current = el.input_value()
                other = next((o for o in options if o != current), None)
                if other is None:
                    continue
                el.select_option(other)
            elif kind in ("radio", "checkbox"):
                el.click()
            elif kind == "range":
                page.keyboard.press("ArrowRight")
            else:
                page.keyboard.type("4")
                page.evaluate("(el) => el.blur()", el)
            try:
                pointer.settle(page)
            except PlaywrightError:
                # The choice navigated mid-settle; gone() below reads it (#312).
                pass
            changed = []
            if gone(page, url0):
                changed.append("loads another page")
            else:
                changed += page.evaluate("() => __st.acts(['submit', 'window'])")
                if run.popups and "opened a window" not in changed:
                    changed.append("opened a window")
                if not drawn(page, el):
                    changed.append("moves on: the control is gone")
                elif not text and not page.evaluate(
                    "(el) => document.activeElement === el", el
                ):
                    changed.append(
                        f"moves focus to {page.evaluate('() => __st.describe(document.activeElement)')}"
                    )
            if changed:
                described = not gone(page, url0) and page.evaluate(
                    "(el) => !!el.getAttribute('aria-describedby')", el
                )
                what = f"choosing a value {'; '.join(changed)}"
                (ans.review if described else ans.miss)(line, at, what)
                page.goto(run.url)
                pointer.settle(page)
            ans.met(line)


def check_enter(run, line, ans):
    with run.page() as page:
        for sel in page.evaluate(FORMS_JS):
            reload(run, page)
            single = page.evaluate(
                "(sel) => [...document.querySelector(sel).elements].some((el) => el.localName === 'input'"
                " && /^(text|email|tel|number|search|url|password)$/.test(el.type) && __st.drawn(el))",
                sel,
            )
            if not single:
                continue
            at = info(page, page.query_selector(sel))
            form.fill(page, sel)
            try:
                got = form.submit(page, sel, by="enter")
            except form.FormError as exc:
                # A form Enter cannot submit is the fault (#312).
                ans.miss(line, at, f"Enter cannot submit it: {exc}")
                continue
            if not got.submits and not got.navigated:
                ans.miss(line, at, "Enter in its single-line field does not submit it")
            ans.met(line)


def unreached(page, line, ans, el, *, exc):
    """Records `el` not judged, as the pointer cannot reach it."""
    ans.unjudged(
        line, info(page, el), f"the pointer cannot reach it: {flow.first_line(exc)}"
    )


def _submit(page, sel):
    """The form at `sel` submitted by its button, or None where it has none."""
    try:
        return form.submit(page, sel)
    except form.FormError:
        # A form with no submit button leaves its caller nothing to read (#312).
        return None


def _values(state):
    return {f["key"]: f["value"] for f in state["fields"]}


def check_kept(run, line, ans):
    with run.page() as page:
        for sel in page.evaluate(FORMS_JS):
            reload(run, page)
            at = info(page, page.query_selector(sel))
            field = _checked_field(page, sel)
            if field is not None:
                typed = {
                    f.key: f.value
                    for f in form.fill(page, sel, bad=[field.key])
                    if f.value is not None
                }
                got = _submit(page, sel)
                now = _values(got.state) if got else {}
                lost = [k for k, v in typed.items() if k in now and now[k] != v]
                if lost:
                    ans.miss(
                        line, at, f"clears {', '.join(lost)} when it shows its errors"
                    )
                ans.met(line)
            reload(run, page)
            secret = set(
                page.evaluate(
                    "() => [...document.querySelectorAll('input[type=password]')].map((e) => e.id ? '#' + e.id : '')"
                )
            )
            typed = {
                f.key: f.value
                for f in form.fill(page, sel)
                if f.value is not None and f.key not in secret
            }
            page.goto("about:blank")
            page.go_back()
            pointer.settle(page)
            now = _values(form.read(page))
            lost = [k for k, v in typed.items() if now.get(k) != v]
            if lost:
                ans.miss(
                    line,
                    at,
                    f"loses {', '.join(lost)} when the visitor goes Back to it",
                )
            ans.met(line)


SUMMARY_JS = r"""() => {
  const a = document.activeElement;
  if (!a || a === document.body) return ["focus stays on the page"];
  if (a.matches("input, select, textarea, button")) return [`focus lands on ${__st.describe(a)}, not an error summary`];
  const out = [];
  const main = document.querySelector("main");
  if (main && !main.contains(a)) out.push("the summary is outside main");
  const h1 = (main || document).querySelector("h1");
  if (h1 && !(a.compareDocumentPosition(h1) & Node.DOCUMENT_POSITION_FOLLOWING)) out.push("the summary is not above the h1");
  const crumbs = [...document.querySelectorAll('nav[aria-label*="readcrumb" i], a[href]')]
    .filter((e) => e.localName === "nav" || /^back$/i.test(__st.text(e)));
  if (crumbs.some((c) => !(c.compareDocumentPosition(a) & Node.DOCUMENT_POSITION_FOLLOWING) && !c.contains(a)))
    out.push("the summary is above the breadcrumbs or back link");
  const fields = [...a.querySelectorAll('a[href^="#"]')].filter((l) =>
    document.getElementById(decodeURIComponent(l.hash.slice(1)))?.matches("input, select, textarea, fieldset"));
  if (!fields.length) out.push("the summary links to no field");
  return out.map((o) => `${o} (${__st.describe(a)})`);
}"""


def check_summary_focus(run, line, ans):
    with run.page() as page:
        for sel in page.evaluate(FORMS_JS):
            reload(run, page)
            if _checked_field(page, sel) is None:
                continue
            at = info(page, page.query_selector(sel))
            form.fill(page, sel, bad=form.ALL)
            url0 = page.url
            if _submit(page, sel) is None or gone(page, url0):
                continue
            for wrong in page.evaluate(SUMMARY_JS):
                ans.miss(line, at, f"after a submit with errors, {wrong}")
            ans.met(line)


SUGGEST_FIELDS_JS = r"""() => [...document.querySelectorAll(
  'input[type=search], input[role=combobox], input[list], input[aria-autocomplete], [role=search] input, search input')]
  .filter((el) => __st.drawn(el) && !el.disabled)"""

COMBO_JS = r"""(el) => {
  const out = [];
  if (el.getAttribute("role") !== "combobox") return ['it is not role="combobox"'];
  if (el.getAttribute("aria-expanded") !== "true") out.push('it is not aria-expanded="true" while its suggestions show');
  const list = document.getElementById(el.getAttribute("aria-controls") || "");
  if (!list || list.getAttribute("role") !== "listbox" || !__st.drawn(list)) out.push("its aria-controls names no listbox drawn");
  return out;
}"""

LIVE_TEXT_JS = (
    "() => [...document.querySelectorAll(__st.LIVE)].map((e) => __st.text(e))"
)


def _axe(page, line, ans, at, *, el):
    """axe's violations of the line's rules on `el`; what axe could not
    decide goes to review, as check-markup.py puts it (#307)."""
    got = (
        markup.axe_on(
            page, line.value["rules"], page.evaluate("(el) => __st.pathOf(el)", el)
        )
        or {}
    )
    for n in got.get("incomplete", []):
        ans.review(line, at, f"axe {n['rule']} could not decide: {n['why']}")
    return [f"axe {v['rule']}: {v['why']}" for v in got.get("violations", [])]


def check_suggest(run, line, ans):
    with run.page() as page:
        count = len(elements(page, SUGGEST_FIELDS_JS))
        for i in range(count):
            reload(run, page)
            el = elements(page, SUGGEST_FIELDS_JS)[i]
            at = info(page, el)
            status = page.evaluate(LIVE_TEXT_JS)
            el.focus()
            page.evaluate("() => __st.mark()")
            page.keyboard.type(line.value["text"])
            pointer.settle(page)
            shown = elements(page, "() => __st.revealed()")
            listed = page.evaluate(
                "(els) => els.some((e) => e.matches('[role=listbox], ul, ol, [role=option], li') || e.querySelector('[role=option], li'))",
                shown,
            )
            combo = page.evaluate("(el) => el.getAttribute('role') === 'combobox'", el)
            if not listed and not combo:
                continue
            wrong = page.evaluate(COMBO_JS, el)
            if combo:
                page.keyboard.press("ArrowDown")
                quick(page)
                if not page.evaluate(
                    "(el) => { const o = document.getElementById(el.getAttribute('aria-activedescendant') || '');"
                    " return !!o && o.getAttribute('role') === 'option'; }",
                    el,
                ):
                    wrong.append("ArrowDown makes no option its aria-activedescendant")
            now = page.evaluate(LIVE_TEXT_JS)
            if not any(
                t != was and re.search(r"\d|\bno\b", t, re.I)
                for t, was in zip(now, status + [""] * len(now), strict=False)
            ):
                wrong.append("no status region says how many suggestions there are")
            wrong += _axe(page, line, ans, at, el=el)
            if wrong:
                ans.miss(line, at, "; ".join(wrong))
            ans.met(line)


GROUP_JS = r"""([sel]) => {
  const boxes = 'input[type=checkbox], [role=checkbox]';
  const groups = new Set([...(sel ? document.querySelectorAll(sel) : []), ...document.querySelectorAll('input[type=checkbox][aria-controls]')]);
  return [...groups].filter(__st.drawn).map((g) => {
    const ids = (g.getAttribute("aria-controls") || "").split(/\s+/).filter(Boolean);
    let members = ids.flatMap((id) => {
      const el = document.getElementById(id);
      return !el ? [] : el.matches(boxes) ? [el] : [...el.querySelectorAll(boxes)];
    });
    if (!members.length) {
      const box = g.closest("fieldset, table, [role=group], ul, ol");
      members = box ? [...box.querySelectorAll(boxes)] : [];
    }
    return [g, ...members.filter((m) => m !== g && __st.drawn(m))];
  });
}"""

STATE_JS = r"""(el) => el.indeterminate || el.getAttribute("aria-checked") === "mixed" ? "mixed"
  : el.checked || el.getAttribute("aria-checked") === "true" ? "checked" : "clear" """


def check_mixed(run, line, ans):
    sel = run.parts.get(line.value["part"])
    with run.page() as page:
        groups = [
            [h.as_element() for h in _items(g)]
            for g in _items(page.evaluate_handle(GROUP_JS, [sel]))
        ]
        for group, *members in groups:
            if len(members) < 2:
                continue
            at = info(page, group)

            def state(el):
                return page.evaluate(STATE_JS, el)

            for m in members:
                if state(m) == "checked":
                    m.click()
            members[0].click()
            quick(page)
            if state(group) != "mixed":
                ans.miss(
                    line,
                    at,
                    f"with some of its group checked it shows {state(group)}, not mixed",
                )
            for m in members[1:]:
                m.click()
            quick(page)
            if state(group) != "checked":
                ans.miss(
                    line, at, f"with all its group checked it shows {state(group)}"
                )
            for m in members:
                m.click()
            quick(page)
            if state(group) != "clear":
                ans.miss(
                    line, at, f"with none of its group checked it shows {state(group)}"
                )
            ans.met(line)
    if sel is None and line.value["part"] not in run.absent and not groups:
        ans.unjudged(
            line,
            None,
            f"no group checkbox names its group, and no selector for the part {line.value['part']}",
        )


# ---- overlays and live regions -------------------------------------------


def check_submenu(run, line, ans):
    with run.page() as page:
        for ov in overlay.find(page):
            if ov.trigger is None or ov.kind == "dialog":
                continue
            if not overlay.open(page, ov, by="click")["open"]:
                continue
            subs = [
                s
                for s in overlay.find(page, within=ov.target)
                if s.trigger is not None and s.kind != "dialog"
            ]
            for sub in subs:
                if not overlay.open(page, sub, by="click")["open"]:
                    continue
                overlay.close(page, ov, by="click")
                if overlay.read(page, ov)["open"]:
                    overlay.close(page, ov, by="escape")
                overlay.open(page, ov, by="click")
                got = overlay.read(page, sub)
                if got["open"] or got["expanded"] == "true":
                    ans.miss(
                        line,
                        info(page, sub.trigger),
                        "closing its menu leaves this submenu open",
                    )
                ans.met(line)
            _shut(page, ov)


def check_interrupt(run, line, ans):
    ms = line.value["ms"]
    with run.page() as page:
        for ov in overlay.find(page):
            if ov.trigger is not None:
                continue
            at = info(page, ov.target)
            got = overlay.close(page, ov, by="click")
            if got["control"] is None or got["open"]:
                ans.miss(
                    line, at, "it opened by itself and has no control that puts it off"
                )
            else:
                page.wait_for_timeout(ms)
                if overlay.read(page, ov)["open"]:
                    ans.miss(line, at, f"it is back within {ms:.0f} ms of being shut")
            ans.met(line)


NAME_JS = r"""(el) => {
  const ids = (el.getAttribute("aria-labelledby") || "").split(/\s+/).filter(Boolean);
  return ids.map((id) => __st.text(document.getElementById(id))).join(" ").trim() || (el.getAttribute("aria-label") || "").trim();
}"""


def check_dialog_name(run, line, ans):
    with run.page() as page:
        for ov in overlay.find(page):
            if ov.kind != "dialog":
                continue
            state = (
                overlay.read(page, ov)
                if ov.trigger is None
                else overlay.open(page, ov, by="click")
            )
            if not state["open"] or ov.target is None:
                continue
            el, at = ov.target, info(page, ov.target)
            native, role, modal = page.evaluate(
                "(el) => [el.localName === 'dialog', el.getAttribute('role'), el.getAttribute('aria-modal')]",
                el,
            )
            wrong = []
            if not native and role not in ("dialog", "alertdialog"):
                wrong.append("it is neither a dialog element nor role=dialog")
            elif not native and state["modal"] and modal != "true":
                wrong.append('it blocks the page without aria-modal="true"')
            if native and not page.evaluate(NAME_JS, el):
                wrong.append("it has no accessible name")
            elif role in ("dialog", "alertdialog"):
                wrong += _axe(page, line, ans, at, el=el)
            if wrong:
                ans.miss(line, at, "; ".join(wrong))
            ans.met(line)
            if ov.trigger is not None:
                _shut(page, ov)


ITEMS_JS = r"""(menu) => [...menu.querySelectorAll('[role^=menuitem], button, a[href]')].filter(__st.drawn)"""

ASKS_JS = r"""() => {
  const open = [...document.querySelectorAll(__st.DIALOGS)].filter(__st.drawn);
  return open.some((d) => d.querySelector("input, select, textarea")
    || [...d.querySelectorAll("button, [role=button]")].filter(__st.drawn).length >= 2);
}"""

LABELS_JS = r"""() => {
  const out = [];
  const labels = [...document.querySelectorAll(`${__st.LIVE}, button, [role=button], [role^=menuitem]`)].filter(__st.drawn);
  for (const el of labels) {
    const t = __st.text(el);
    if (/\.\.\.$/.test(t)) out.push([__st.info(el), `"${t}" ends in three full stops, not the ellipsis character`]);
    else if (el.getAttribute("aria-busy") === "true" && /…$/.test(t)) out.push([__st.info(el), `a busy button "${t}" ends in an ellipsis`]);
    else if (el.matches(__st.LIVE) && /…$/.test(t) && !/\w+ing…$/.test(t)) out.push([__st.info(el), `an in-progress label "${t}" does not read as an -ing verb`]);
  }
  return out;
}"""


def check_ellipsis(run, line, ans):
    with run.page() as page:
        for at, what in page.evaluate(LABELS_JS):
            ans.miss(line, at, what)
        menus = [
            i
            for i, ov in enumerate(overlay.find(page))
            if ov.kind in ("menu", "popover") and ov.trigger
        ]
        for m in menus:
            reload(run, page)
            ov = overlay.find(page)[m]
            overlay.open(page, ov, by="click")
            count = len(elements(page, ITEMS_JS, ov.target))
            for i in range(count):
                reload(run, page)
                ov = overlay.find(page)[m]
                overlay.open(page, ov, by="click")
                item = elements(page, ITEMS_JS, ov.target)[i]
                at = info(page, item)
                label = page.evaluate("(el) => __st.text(el)", item)
                submenu = page.evaluate(
                    "(el) => el.hasAttribute('aria-haspopup') && el.getAttribute('aria-haspopup') !== 'dialog'",
                    item,
                )
                url0 = page.url
                try:
                    pointer.click(page, item)
                except pointer.PointerError as exc:
                    # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                    unreached(page, line, ans, item, exc=exc)
                    continue
                asks = not gone(page, url0) and not submenu and page.evaluate(ASKS_JS)
                if asks and not label.endswith("…"):
                    ans.miss(
                        line,
                        at,
                        f'"{label}" opens a dialog that asks for more, yet ends with no "…"',
                    )
                elif not asks and label.endswith("…"):
                    ans.miss(
                        line, at, f'"{label}" asks for nothing more, yet ends with "…"'
                    )
                for at2, what in [] if gone(page, url0) else page.evaluate(LABELS_JS):
                    ans.miss(line, at2, what)
                ans.met(line)


PLAIN_BUTTON = (
    "button:not([aria-expanded]):not([aria-haspopup]):not([popovertarget]):not([commandfor]):not([aria-pressed]),"
    " [role=button]:not([aria-expanded]):not([aria-haspopup]):not([aria-pressed])"
)


def check_expanded(run, line, ans):
    with run.page() as page:
        for ov in overlay.find(page):
            if ov.trigger is None or ov.kind == "dialog":
                continue
            native = page.evaluate(
                "(el) => el.localName === 'summary' || el.hasAttribute('popovertarget') || el.hasAttribute('commandfor')",
                ov.trigger,
            )
            if native:
                continue
            at = info(page, ov.trigger)
            shut = page.evaluate("(el) => el.getAttribute('aria-expanded')", ov.trigger)
            if shut != "false":
                ans.miss(
                    line, at, f'shut, it reads aria-expanded {shut!r}, not "false"'
                )
            got = overlay.open(page, ov, by="click")
            if got["open"] and got["expanded"] != "true":
                ans.miss(
                    line,
                    at,
                    f'open, it reads aria-expanded {got["expanded"]!r}, not "true"',
                )
            if ov.kind == "menu" and page.evaluate(
                "(el) => el.getAttribute('aria-haspopup')", ov.trigger
            ) not in ("menu", "true"):
                ans.miss(line, at, 'a menu trigger with no aria-haspopup="menu"')
            for wrong in _axe(page, line, ans, at, el=ov.trigger):
                ans.miss(line, at, wrong)
            _shut(page, ov)
            ans.met(line)
        for _, at, shown in trial(run, page, keep=PLAIN_BUTTON):
            panels = page.evaluate(
                "(els) => els.filter((e) => __st.text(e) && !e.closest(__st.DIALOGS) && !__st.liveOf(e)"
                " && !e.closest('[role=tooltip]')).map(__st.describe)",
                shown,
            )
            if panels:
                ans.miss(line, at, f"shows {panels[0]} with no aria-expanded")
            ans.met(line)


def _live_faults(page, found, by=None):
    """Adds each live region at fault to `found`, named by the control
    `by` (its info) that showed it where one did."""
    for h in _items(page.evaluate_handle("() => __st.liveFaults()")):
        region = info(page, h.get_property("0").as_element())
        what = h.get_property("1").json_value()
        at = by or region
        if by:
            what = f"the live region it shows, {region['where']}, {what}"
        found.setdefault((at["where"], region["where"]), (at, what))


def check_live_region(run, line, ans):
    found = {}
    with run.page() as page:
        snap = lambda p: p.evaluate("() => __st.snapLive()")  # noqa: E731
        for _, at, _ in trial(run, page, before=snap):
            _live_faults(page, found, at)
            ans.met(line)
        for sel in page.evaluate(FORMS_JS):
            reload(run, page)
            snap(page)
            form.fill(page, sel, bad=form.ALL)
            url0 = page.url
            if _submit(page, sel) is not None and not gone(page, url0):
                _live_faults(page, found)
            ans.met(line)
    for at, what in found.values():
        ans.miss(line, at, what)


def check_toast(run, line, ans):
    ms = line.value["ms"]
    sel = run.parts.get(line.value["part"])
    with run.page() as page:
        for button, at, shown in trial(run, page):
            toasts = elements(
                page,
                "([els, sel]) => els.filter((e) => __st.text(e) && ((sel && e.matches(sel)) || __st.liveOf(e)))",
                [shown, sel],
            )
            for t in toasts:
                where = info(page, t)
                if not page.evaluate(
                    "([b, t]) => document.activeElement === b || b.contains(document.activeElement)",
                    [button, t],
                ):
                    moved = page.evaluate("() => __st.describe(document.activeElement)")
                    ans.miss(
                        line, where, f"it moves focus from {at['where']} to {moved}"
                    )
                if not page.evaluate("(t) => !!__st.liveOf(t)", t):
                    ans.miss(line, where, "it sits in no live region")
                action = page.evaluate_handle(
                    "([t, shut]) => [...t.querySelectorAll('button, a[href]')].find((b) =>"
                    " !shut.includes(__st.nameOf(b).toLowerCase())) || null",
                    [t, list(SHUT_WORDS)],
                ).as_element()
                if action is not None:
                    page.wait_for_timeout(ms)
                    if not drawn(page, t):
                        ans.miss(
                            line,
                            where,
                            f"it holds an action, yet goes within {ms:.0f} ms, before it is dismissed",
                        )
                    if not page.evaluate(
                        "([t, a]) => __st.controls(['button', 'link']).some((c) => !t.contains(c) && __st.nameOf(c) === __st.nameOf(a))",
                        [t, action],
                    ):
                        ans.miss(
                            line,
                            where,
                            "its action is offered nowhere else on the page",
                        )
                ans.met(line)


def check_exit(run, line, ans):
    from playwright.sync_api import Error as PlaywrightError

    keep = ", ".join(run.handover) or None
    with run.page() as page:
        hrefs = page.evaluate(
            "(keep) => [...document.querySelectorAll('a[href]')].filter((a) => __st.drawn(a) && !(keep && a.matches(keep))).map((a) => a.href)",
            keep,
        )
    for href in hrefs:
        if not _off_site(run.url, href):
            continue
        with run.page() as page:
            asked = []
            page.on(
                "dialog", lambda d, asked=asked: (asked.append(d.type), d.dismiss())
            )
            link = page.query_selector_all("a[href]")[
                [
                    *page.evaluate(
                        "() => [...document.querySelectorAll('a[href]')].map((a) => a.href)"
                    )
                ].index(href)
            ]
            at = info(page, link)
            run.popups.clear()
            page.evaluate("() => __st.mark()")
            try:
                pointer.click(page, link)
            except pointer.PointerError as exc:
                # Not judged where the pointer cannot reach it, so it is never a pass (#312).
                unreached(page, line, ans, link, exc=exc)
                continue
            try:
                page.wait_for_load_state()
            except PlaywrightError:
                # A load the guard's blank answer cut short still names the page reached (#312).
                pass
            pages = [page, *run.popups]
            arrived = any(
                urllib.parse.urlsplit(p.url).netloc
                == urllib.parse.urlsplit(href).netloc
                for p in pages
            )
            if asked:
                ans.miss(line, at, f"leaving the site asks first: a {asked[0]} dialog")
            elif not arrived:
                warned = page.url.split("#")[0] == run.url.split("#")[
                    0
                ] and page.evaluate("() => __st.dialogs()")
                ans.miss(
                    line,
                    at,
                    "leaving the site opens a warning dialog"
                    if warned
                    else f"it goes to {page.url} first, not to {href}",
                )
            ans.met(line)


TIME_JS = r"""
(() => {
  const tell = (kind, extra) => window.__stTime?.(kind, Date.now(), extra || null);
  window.navigation?.addEventListener("navigate", () => tell("expire"));
  addEventListener("pagehide", () => tell("expire"));
  addEventListener("DOMContentLoaded", () => {
    tell("load");
    const find = () => [...document.querySelectorAll('dialog[open], [role=alertdialog], [role=alert]')]
      .find((el) => el.checkVisibility() && el.textContent.trim());
    new MutationObserver((_, ob) => {
      const w = find();
      if (!w) return;
      ob.disconnect();
      tell("warn", [...w.querySelectorAll("button, [role=button]")].map((b) => b.textContent.trim()));
    }).observe(document, { subtree: true, childList: true, attributes: true, characterData: true });
  });
})();
"""

PRESS_JS = r"""(name) => {
  const w = [...document.querySelectorAll('dialog[open], [role=alertdialog], [role=alert]')].find((el) => el.textContent.trim());
  const b = w && [...w.querySelectorAll("button, [role=button]")].find((x) => x.textContent.trim() === name);
  if (b) b.click();
  return !!b;
}"""


def _timed(run, run_for, press=None, then=0):
    """The {kind: (time, extra)} the fake clock saw, `run_for` ms after load,
    then pressing the warning's button `press` and running `then` ms more."""
    from playwright.sync_api import Error as PlaywrightError

    seen = {}
    with conditions.open_page(run.browser, "about:blank", viewport=VIEWPORT) as page:
        page.context.expose_binding(
            "__stTime", lambda _src, kind, t, extra: seen.setdefault(kind, (t, extra))
        )
        page.context.add_init_script(TIME_JS)
        guard(page.context, run.url)
        page.clock.install()
        page.goto(run.url)
        try:
            page.clock.run_for(int(run_for))
            if (
                press is not None
                and "expire" not in seen
                and page.evaluate(PRESS_JS, press)
            ):
                seen.pop("expire", None)
                page.clock.run_for(int(then))
        except PlaywrightError:
            # The page leaving itself as its limit ends cuts the clock short;
            # any other failure stops the check (#312).
            if "expire" not in seen:
                raise
    return seen


def check_time_limit(run, line, ans):
    warn, horizon = line.value["warn"], line.value["horizon"]
    seen = _timed(run, horizon)
    if "expire" not in seen or "load" not in seen:
        return
    load, ends = seen["load"][0], seen["expire"][0]
    ans.met(line)
    if "warn" not in seen or ends - seen["warn"][0] < warn:
        early = (ends - seen["warn"][0]) / 1000 if "warn" in seen else None
        ans.miss(
            line,
            None,
            f"the page leaves itself {(ends - load) / 1000:.0f} s after load, "
            + (
                f"warning only {early:.0f} s before"
                if early is not None
                else "with no warning"
            ),
        )
        return
    since = seen["warn"][0] - load
    for name in seen["warn"][1] or []:
        again = _timed(run, since + 1, press=name, then=ends - seen["warn"][0] + 1000)
        if "expire" not in again:
            return
    ans.miss(line, None, "no button in the time-limit warning restarts the limit")


RUNS = {name: globals()["check_" + name.replace("-", "_")] for name in CHECKS}


def findings(run, table):
    """One finding per record id, in table order: {"id", "answer", "misses",
    "unjudged", "review"}, each entry {"check", "where", "fault", "what"}."""
    from playwright.sync_api import Error as PlaywrightError

    ans = rule_table.Answers(table, "where", "fault", review=True)
    for line in table:
        run.popups.clear()
        try:
            RUNS[line.check](run, line, ans)
        except (PlaywrightError, form.FormError) as exc:
            # One check stopping leaves the others to run; it is said as not judged (#312).
            ans.unjudged(line, None, f"the check stopped: {flow.first_line(exc)}")
    return ans.done()


def report(url, found):
    lines = [f"check-state: {url}"]
    for f in found:
        lines.append(f"{f['id']}: {f['answer']}")
        for mark, key in (("-", "misses"), ("?", "unjudged"), ("~", "review")):
            for m in f[key]:
                lines.append(
                    f"  {mark} [{m['check']}] {m['where'] or 'the page'}: {m['what']}"
                )
    return "\n".join(lines)


def parse_args(argv):
    p = argparse.ArgumentParser(
        prog="check-state.py",
        description="Drive a page into the states a visitor reaches, and answer the rule records about what each shows.",
    )
    p.add_argument("url", help="the page: an http(s) URL, or a local HTML file")
    p.add_argument("--out", required=True, metavar="DIR", help="where state.json goes")
    p.add_argument(
        "--parts",
        dest="declaration",
        metavar="FILE",
        help="the building session's parts declaration",
    )
    p.add_argument(
        "--part",
        action="append",
        default=[],
        metavar="NAME=SELECTOR",
        help="a declared part's name and its CSS selector",
    )
    p.add_argument(
        "--handover",
        action="append",
        default=[],
        metavar="SELECTOR",
        help="a link the project keeps a handover notice for",
    )
    p.add_argument("--table", default=TABLE, metavar="FILE", help="the check table")
    p.add_argument(
        "--timeout",
        type=int,
        default=flow.LOAD_TIMEOUT_MS,
        metavar="MS",
        help="for each load",
    )
    at = p.parse_args(argv)
    at.parts, at.absent = {}, set()
    if at.declaration:
        try:
            with open(at.declaration, encoding="utf8") as fh:
                at.parts, at.absent = probe.declared_parts(fh.read())
        except OSError as exc:
            p.error(f"cannot read --parts {at.declaration}: {exc.strerror}")
        except probe.DeclarationError as exc:
            p.error(f"--parts {at.declaration}: {exc}")
    for given in at.part:
        name, eq, selector = given.partition("=")
        if not eq or not name.strip() or not selector.strip():
            p.error(f"--part wants NAME=SELECTOR, got {given!r}")
        at.parts[name.strip()] = selector.strip()
    try:
        with open(at.table, encoding="utf8") as fh:
            at.lines = parse(fh.read())
    except OSError as exc:
        p.error(f"cannot read --table {at.table}: {exc.strerror}")
    except TableError as exc:
        p.error(f"--table {at.table}: {exc}")
    at.url = flow.page_url(p, at.url)
    return p, at


def main(argv):
    _, at = parse_args(argv)
    when = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    os.makedirs(at.out, exist_ok=True)
    json_path = os.path.join(at.out, "state.json")
    with contextlib.suppress(FileNotFoundError):
        os.unlink(json_path)

    def work():
        with flow.chromium() as browser:
            with conditions.open_page(browser, at.url, viewport=VIEWPORT) as first:
                first.set_default_navigation_timeout(at.timeout)
            run = Run(
                browser,
                at.url,
                parts=at.parts,
                absent=at.absent,
                handover=at.handover,
                timeout=at.timeout,
            )
            return findings(run, at.lines)

    found, code = flow.run_browser(work, at.timeout, at.url)
    if code:
        return code
    with open(json_path, "w", encoding="utf8") as fh:
        json.dump(
            {
                "url": at.url,
                "run_at": when.isoformat(),
                "answers": {f["id"]: f["answer"] for f in found},
                "findings": found,
            },
            fh,
            indent=1,
        )
    print(report(at.url, found))
    return 1 if any(f["misses"] for f in found) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
