"""drive-overlay.py — opens and closes a page's menus, dialogs and popovers for the
check scripts that read a page with one open (design-vault#303).

A module, not a command. A check loads it by path, as the others load check-flow.py:

    spec = importlib.util.spec_from_file_location("drive_overlay", os.path.join(HERE, "drive-overlay.py"))
    overlay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(overlay)

and drives a Playwright page it has loaded and settled:

    for ov in overlay.find(page):
        state = overlay.open(page, ov, by="keyboard")   # the overlay is open here: read the page
        ...
        state = overlay.close(page, ov, by="escape")

find() lists, as Overlays, first the visible triggers in document order:
  - a <summary>, opening its <details>;
  - a popovertarget, or a commandfor whose command shows a popover or a dialog, opening the element it names;
  - an aria-haspopup or aria-expanded element, opening what its aria-controls names, or else whatever its first
    open draws;
then the opener of each <dialog> no trigger above names, found by trial; then each dialog or popover already
open with no trigger, as a script opens one unprompted, whose `trigger` is None. The trial runs on a page of
its own in the caller's browser, reloaded from the caller's URL at the caller's viewport before each click, so the
caller's page is never clicked: each visible button, [role=button] or menu item that would not submit a form
or leave the page is clicked, top-level ones first and then those each trigger's overlay draws, until every
such dialog has its opener. A trial is kept per URL and viewport. It reads the page as it loads, so it misses
an opener that only the caller's own steps draw, and it cannot load a page set by set_content. A
[role=dialog] that no markup names is not tried for, as nothing generic tells a trial it opened. Text fields
are never triggers: a combobox opens by typing, which the form driver (#302) does.

open(by="click" | "keyboard") clicks the trigger, or focuses it and presses `key` (Enter by default; Space and
ArrowDown also open an APG menu button). close(by="escape") presses Escape wherever focus is; close(by="click" |
"keyboard") activates the overlay's close control: one inside it that commands it shut, a dialog form's button
(one named as closing first), or a button named close, cancel, dismiss, done or hide, or × alone, and else
the trigger itself, except for a dialog, which a check should see has no close control. Each returns once the
page has settled, with what read() reads:

    {"open": bool, "expanded": "true" | "false" | None, "modal": bool, "focus_inside": bool,
     "focus": str | None, "control": str | None, "settled": bool}

`open` is the overlay's own state where it has one (a <details>'s or a <dialog>'s open, :popover-open), else
whether the element is drawn: visible, not see-through, at least 2 px each way, and not placed off the page.
`expanded` is the trigger's aria-expanded, read apart from `open` so a check can catch the two disagreeing.
`focus_inside` is focus in the overlay but not on its trigger; `focus` describes the focused element, None on
the body. `control` names what close() activated, or is None. `settled` is False where the page was still
moving at SETTLE_CAP_MS and was read as it stood. A page that does not open or close as asked is a reading,
never an error: open() and close() raise ValueError only for an unknown `by` or an overlay with no trigger to
open, else only Playwright's own failures raise, and a trial click Playwright refuses skips that button.
"""

import dataclasses

# A click or keypress waits this long for its element before Playwright raises: a working figure, a tenth of
# Playwright's own 30 s default, since an element on a loaded local page is ready at once or never.
ACTION_TIMEOUT_MS = 2000
# Settled means the overlay's state, box and opacity unchanged, and none of its finite animations running, for
# QUIET_MS, read once a frame; a page still moving after SETTLE_CAP_MS is read as it stands. Both are working
# figures: the wait already outlasts the overlay's own transitions, which impeccable.md's motion override keeps
# to 500 ms, and the quiet catches a script that shows or hides a few frames late.
QUIET_MS = 100
SETTLE_CAP_MS = 3000

LIB_JS = r"""
// Under 2 px a box is a hairline or a visually-hidden element, not an overlay drawn for the eye.
const drawn = (el) => {
  if (!el || !el.isConnected) return false;
  if (!el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) return false;
  const r = el.getBoundingClientRect();
  if (r.width < 2 || r.height < 2) return false;
  const x = r.left + scrollX, y = r.top + scrollY, page = document.documentElement;
  return x + r.width > 0 && y + r.height > 0 && x < page.scrollWidth && y < page.scrollHeight;
};
const isOpen = (el) => {
  if (!el || !el.isConnected) return false;
  if (el.localName === "details" || el.localName === "dialog") return el.open;
  if (el.hasAttribute("popover")) return el.matches(":popover-open");
  return drawn(el);
};
// 40 characters names a control in a report line without quoting a paragraph.
const describe = (el) => {
  if (!el) return null;
  const name = (el.getAttribute("aria-label") || el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 40);
  return el.localName + (el.id ? "#" + el.id : "") + (name ? ` "${name}"` : "");
};
const pathOf = (el) => {
  const parts = [];
  for (; el && el !== document.documentElement; el = el.parentElement) {
    if (el.id && document.querySelectorAll("#" + CSS.escape(el.id)).length === 1) {
      parts.unshift("#" + CSS.escape(el.id));
      return parts.join(" > ");
    }
    let n = 1;
    for (let s = el.previousElementSibling; s; s = s.previousElementSibling) n += s.localName === el.localName;
    parts.unshift(`${el.localName}:nth-of-type(${n})`);
  }
  return ["html", ...parts].join(" > ");
};
const CONTROLS = "button, [role=button], [role=menuitem], input[type=button], a";
const OVERLAY_ROLES = ["dialog", "alertdialog", "menu", "menubar", "listbox", "tree", "grid"];
const OVERLAYS = "dialog, [popover], " + OVERLAY_ROLES.map((r) => `[role=${r}]`).join(", ");
const leaves = (el) => (el.localName === "a" && el.hasAttribute("href") && !el.getAttribute("href").startsWith("#")) ||
  (el.form && el.form.getAttribute("method") !== "dialog" && (el.type === "submit" || el.type === "image"));
const byId = (id) => (id ? document.getElementById(id) : null);
const kindOf = (el, target) => {
  if (el.localName === "summary") return "details";
  if (target) {
    const role = target.getAttribute("role");
    if (target.localName === "dialog" || role === "dialog" || role === "alertdialog") return "dialog";
    if (target.hasAttribute("popover")) return "popover";
    if (role === "menu" || role === "menubar") return "menu";
    if (OVERLAY_ROLES.includes(role)) return role;
  }
  const popup = el.getAttribute("aria-haspopup");
  if (popup === "true" || popup === "menu") return "menu";
  if (OVERLAY_ROLES.includes(popup)) return popup;
  return "disclosure";
};
// Every trigger in the document, drawn or not, with the target its markup names, or null.
const triggers = () => {
  const shows = ["show-modal", "show-popover", "toggle-popover"];
  const out = [];
  const all = document.querySelectorAll(
    "summary, [popovertarget], [commandfor], [aria-haspopup]:not([aria-haspopup=false]), [aria-expanded]");
  for (const el of all) {
    if (el.matches("input:not([type=button]):not([type=submit]):not([type=reset]), textarea, [role=combobox]")) continue;
    let target = null;
    if (el.localName === "summary") {
      if (el.parentElement?.localName !== "details" || el.parentElement.querySelector(":scope > summary") !== el) continue;
      target = el.parentElement;
    } else if (el.hasAttribute("popovertarget")) {
      if (el.getAttribute("popovertargetaction") === "hide") continue;
      target = byId(el.getAttribute("popovertarget"));
    } else if (el.hasAttribute("commandfor")) {
      if (!shows.includes(el.getAttribute("command"))) continue;
      target = byId(el.getAttribute("commandfor"));
    } else if (el.hasAttribute("aria-haspopup") || el.hasAttribute("aria-expanded")) {
      target = byId((el.getAttribute("aria-controls") || "").split(/\s+/)[0]);
    } else continue;
    out.push({ el, target });
  }
  return out;
};
"""

FIND_JS = (
    "(within) => {"
    + LIB_JS
    + r"""
  const inScope = (el) => !within || within.contains(el);
  const all = triggers();
  const named = new Set(all.map((t) => t.target));
  const found = all.filter((t) => drawn(t.el) && inScope(t.el)).map(({ el, target }) =>
    ({ el, target, declared: Boolean(target), name: describe(el), kind: kindOf(el, target) }));
  const orphans = [...document.querySelectorAll("dialog")].filter((d) => !d.open && !named.has(d)).map(pathOf);
  const standing = [...document.querySelectorAll(OVERLAYS)].filter((el) =>
    el !== within && !named.has(el) && inScope(el) && !el.matches("[role=menu], [role=menubar], [role=listbox], [role=tree], [role=grid]") &&
    (el.localName === "dialog" || el.hasAttribute("popover") ? isOpen(el) : drawn(el)))
    .map((el) => ({ el, kind: el.hasAttribute("popover") ? "popover" : "dialog", name: describe(el) }));
  return { found, orphans, standing };
}"""
)

# The trial page's clickable controls that are no trigger, as paths, drawn and not leaving the page.
CANDIDATES_JS = (
    "() => {"
    + LIB_JS
    + r"""
  const isTrigger = new Set(triggers().map((t) => t.el));
  return [...document.querySelectorAll(CONTROLS)]
    .filter((el) => !isTrigger.has(el) && !el.disabled && !leaves(el) && drawn(el)).map(pathOf);
}"""
)

# The trial page's drawn triggers whose overlay may hold an opener, as paths.
PARENTS_JS = (
    "() => {"
    + LIB_JS
    + r"""
  return triggers().filter(({ el, target }) => drawn(el) && kindOf(el, target) !== "dialog").map(({ el }) => pathOf(el));
}"""
)

# An element the trial named, described for a report where it is drawn on the caller's page inside `within`, else null.
PLACED_JS = (
    "([el, within]) => {"
    + LIB_JS
    + "return drawn(el) && (!within || within.contains(el)) ? describe(el) : null; }"
)

READ_JS = (
    "([trigger, target]) => {"
    + LIB_JS
    + r"""
  const focus = document.activeElement;
  return {
    open: isOpen(target),
    expanded: trigger ? trigger.getAttribute("aria-expanded") : null,
    modal: Boolean(target && target.matches(":modal")),
    focus_inside: Boolean(target && focus && target.contains(focus) && !(trigger && trigger.contains(focus))),
    focus: describe(focus && focus !== document.body ? focus : null),
  };
}"""
)

SETTLE_JS = (
    "async ([target, quiet, cap]) => {"
    + LIB_JS
    + r"""
  const frame = () => new Promise((done) => requestAnimationFrame(() => done()));
  const moving = (scope) => scope.getAnimations({ subtree: true }).filter((a) => a.playState === "running" &&
    Number.isFinite(a.effect && a.effect.getComputedTiming ? a.effect.getComputedTiming().endTime : Infinity)).length;
  const signature = () => {
    if (!target) return String(moving(document));
    const r = target.getBoundingClientRect();
    return JSON.stringify([isOpen(target), r.x, r.y, r.width, r.height, getComputedStyle(target).opacity,
                           moving(target)]);
  };
  const start = performance.now();
  await frame();
  let last = signature(), since = performance.now();
  while (performance.now() - start < cap) {
    await frame();
    const now = signature();
    if (now !== last) { last = now; since = performance.now(); continue; }
    if ((target ? moving(target) : moving(document)) === 0 && performance.now() - since >= quiet) return true;
  }
  return false;
}"""
)

# Every element drawn now, as a Set, before a trigger with no named target is first opened.
DRAWN_JS = (
    "() => {"
    + LIB_JS
    + "return new Set([...document.querySelectorAll('*')].filter(drawn)); }"
)

# What the open drew that was not drawn before: the outermost new element outside the trigger, preferring one
# that is or holds an overlay, else the largest.
DREW_JS = (
    "([before, trigger]) => {"
    + LIB_JS
    + r"""
  const fresh = new Set([...document.querySelectorAll("*")].filter((el) => !before.has(el) && !trigger.contains(el) && drawn(el)));
  const roots = [...fresh].filter((el) => !fresh.has(el.parentElement));
  const holds = (el) => el.matches(OVERLAYS) || Boolean(el.querySelector(OVERLAYS));
  const area = (el) => { const r = el.getBoundingClientRect(); return r.width * r.height; };
  return roots.sort((a, b) => holds(b) - holds(a) || area(b) - area(a))[0] || null;
}"""
)

# The control inside an open overlay that shuts it, else (for any kind but a dialog) the trigger.
CONTROL_JS = (
    "([trigger, target, kind]) => {"
    + LIB_JS
    + r"""
  const inside = target ? [...target.querySelectorAll(CONTROLS)].filter((el) => drawn(el) && !leaves(el)) : [];
  const id = target && target.id;
  const shuts = (el) =>
    (id && el.getAttribute("commandfor") === id && ["close", "request-close", "hide-popover", "toggle-popover"].includes(el.getAttribute("command"))) ||
    (id && el.getAttribute("popovertarget") === id && el.getAttribute("popovertargetaction") !== "show");
  const inDialogForm = (el) => el.form && el.form.getAttribute("method") === "dialog" && el.type !== "button";
  const named = (el) => /\b(close|cancel|dismiss|done|hide)\b|^\s*[×✕✖xX]\s*$/i.test(
    [el.getAttribute("aria-label"), el.getAttribute("title"), el.textContent].filter(Boolean).join(" "));
  return inside.find(shuts) || inside.find((el) => inDialogForm(el) && named(el)) ||
    inside.find(inDialogForm) || inside.find(named) || (kind === "dialog" ? null : trigger);
}"""
)


@dataclasses.dataclass
class Overlay:
    """One trigger and what it opens. `trigger` is None for an overlay already open with nothing to open it;
    `target` is None until the first open of a trigger whose markup names nothing; `declared` is whether
    markup names the target; `name` describes the trigger, or the overlay with no trigger, for a report."""

    trigger: object
    target: object
    kind: str
    name: str
    declared: bool


# Trial results, {(url, viewport): {opener path: dialog path}}.
_trials = {}


def _items(handle):
    """A page array's JSHandle as a list of JSHandles."""
    props = handle.get_properties()
    return [props[str(i)] for i in range(len(props))]


def _settle(page, target=None):
    """Wait until the overlay is still, or the document's animations are with no target. False if it never was."""
    return page.evaluate(SETTLE_JS, [target, QUIET_MS, SETTLE_CAP_MS])


def _openers(page, orphans):
    """{opener path: dialog path} for the closed dialogs at `orphans` (paths), tried on a second page."""
    from playwright.sync_api import Error as PlaywrightError

    if not page.url.startswith(("http:", "https:", "file:")):
        return {}
    key = (page.url, tuple(sorted((page.viewport_size or {}).items())))
    if key in _trials:
        return {p: d for p, d in _trials[key].items() if d in orphans}
    context = page.context.browser.new_context(viewport=page.viewport_size)
    trial = context.new_page()
    try:

        def fresh(parent=None):
            trial.goto(page.url)
            trial.evaluate(
                "() => document.querySelectorAll('dialog[open]').forEach((d) => d.close())"
            )
            _settle(trial)
            if parent:
                trial.click(parent, timeout=ACTION_TIMEOUT_MS)
                _settle(trial)

        fresh()
        top = trial.evaluate(CANDIDATES_JS)
        plan = [(None, path) for path in top]
        for parent in trial.evaluate(PARENTS_JS):
            try:
                fresh(parent)
            except PlaywrightError:
                continue
            plan += [
                (parent, p)
                for p in trial.evaluate(CANDIDATES_JS)
                if p not in top and (parent, p) not in plan
            ]
        found, left = {}, set(orphans)
        for parent, path in plan:
            if not left:
                break
            try:
                fresh(parent)
                trial.click(path, timeout=ACTION_TIMEOUT_MS)
            except PlaywrightError:
                continue
            _settle(trial)
            hit = next(
                (
                    d
                    for d in sorted(left)
                    if trial.evaluate(
                        "p => Boolean(document.querySelector(p)?.open)", d
                    )
                ),
                None,
            )
            if hit:
                found[path] = hit
                left.discard(hit)
        _trials[key] = found
        return found
    finally:
        context.close()


def read(page, ov):
    """The overlay's state now, as the module docstring lists it, with `control` None and `settled` True."""
    return {
        **page.evaluate(READ_JS, [ov.trigger, ov.target]),
        "control": None,
        "settled": True,
    }


def find(page, within=None):
    """Every overlay in `within` (an element handle; the whole page by default), each an Overlay."""
    listing = page.evaluate_handle(FIND_JS, within)

    def field(item, key):
        return item.get_property(key).json_value()

    found = [
        Overlay(
            item.get_property("el").as_element(),
            item.get_property("target").as_element(),
            field(item, "kind"),
            field(item, "name"),
            field(item, "declared"),
        )
        for item in _items(listing.get_property("found"))
    ]
    orphans = field(listing, "orphans")
    for opener, dialog in (_openers(page, orphans) if orphans else {}).items():
        button = page.query_selector(opener)
        name = button and page.evaluate(PLACED_JS, [button, within])
        if name:
            found.append(
                Overlay(button, page.query_selector(dialog), "dialog", name, False)
            )
    found += [
        Overlay(
            None,
            item.get_property("el").as_element(),
            field(item, "kind"),
            field(item, "name"),
            False,
        )
        for item in _items(listing.get_property("standing"))
    ]
    return found


def open(page, ov, by="click", key="Enter"):
    """Open `ov` by clicking its trigger, or by focusing it and pressing `key`; its state once settled."""
    if ov.trigger is None:
        raise ValueError(f"{ov.name} has no trigger: it opened by itself")
    before = None if ov.target else page.evaluate_handle(DRAWN_JS)
    if by == "click":
        ov.trigger.click(timeout=ACTION_TIMEOUT_MS)
    elif by == "keyboard":
        ov.trigger.focus()
        page.keyboard.press(key)
    else:
        raise ValueError(f"open by 'click' or 'keyboard', not {by!r}")
    settled = _settle(page, ov.target)
    if before is not None:
        ov.target = page.evaluate_handle(DREW_JS, [before, ov.trigger]).as_element()
        if ov.target:
            settled = _settle(page, ov.target)
    return {**read(page, ov), "settled": settled}


def close(page, ov, by="escape"):
    """Close `ov` by Escape, or by clicking or keying Enter on its close control; its state once settled. With no
    control found, nothing is pressed and `control` is None."""
    control = None
    if by == "escape":
        page.keyboard.press("Escape")
    elif by in ("click", "keyboard"):
        control = page.evaluate_handle(
            CONTROL_JS, [ov.trigger, ov.target, ov.kind]
        ).as_element()
        if control is None:
            return read(page, ov)
        if by == "click":
            control.click(timeout=ACTION_TIMEOUT_MS)
        else:
            control.focus()
            page.keyboard.press("Enter")
    else:
        raise ValueError(f"close by 'escape', 'click' or 'keyboard', not {by!r}")
    settled = _settle(page, ov.target)
    state = {**read(page, ov), "settled": settled}
    if control is not None:
        state["control"] = control.evaluate(
            "el => {" + LIB_JS + "return describe(el); }"
        )
    return state
