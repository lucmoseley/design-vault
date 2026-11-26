import base64
import dataclasses
import inspect
import json

ACTION_TIMEOUT_MS = 2000  # guess, #501
QUIET_MS = 100  # guess, #501
SETTLE_CAP_MS = 3000  # guess, #501

LIB_JS = r"""
// guess, #501
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
// guess, #501
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

CANDIDATES_JS = (
    "() => {"
    + LIB_JS
    + r"""
  const isTrigger = new Set(triggers().map((t) => t.el));
  return [...document.querySelectorAll(CONTROLS)]
    .filter((el) => !isTrigger.has(el) && !el.disabled && !leaves(el) && drawn(el)).map(pathOf);
}"""
)

PARENTS_JS = (
    "() => {"
    + LIB_JS
    + r"""
  return triggers().filter(({ el, target }) => drawn(el) && kindOf(el, target) !== "dialog").map(({ el }) => pathOf(el));
}"""
)

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

DRAWN_JS = (
    "() => {"
    + LIB_JS
    + "return new Set([...document.querySelectorAll('*')].filter(drawn)); }"
)

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
    trigger: object
    target: object
    kind: str
    name: str
    declared: bool


_trials: dict[tuple[str, str], dict[str, str]] = {}
TRIAL_LEAVES_OUT = ("accept_downloads",)


def _items(handle):
    props = handle.get_properties()
    return [props[str(i)] for i in range(len(props))]


def _settle(page, target=None):
    return page.evaluate(SETTLE_JS, [target, QUIET_MS, SETTLE_CAP_MS])


def _trial_options(page):
    # Playwright's BrowserContext has no public getter for the options it was made with:
    # https://playwright.dev/python/docs/api/class-browsercontext
    from playwright.sync_api import Browser

    names = {
        n.replace("_", ""): n for n in inspect.signature(Browser.new_context).parameters
    }
    protocol = dict(page.context._impl_obj._options)
    if protocol.pop("noDefaultViewport", False):
        protocol["noViewport"] = True
    if "extraHTTPHeaders" in protocol:
        protocol["extraHTTPHeaders"] = {
            h["name"]: h["value"] for h in protocol["extraHTTPHeaders"]
        }
    if "clientCertificates" in protocol:
        protocol["clientCertificates"] = [
            {
                k: base64.b64decode(v) if k in ("cert", "key", "pfx") else v
                for k, v in c.items()
            }
            for c in protocol["clientCertificates"]
        ]
    options = {
        names[k.lower()]: v
        for k, v in protocol.items()
        if k.lower() in names and names[k.lower()] not in TRIAL_LEAVES_OUT
    }
    if page.viewport_size:
        options["viewport"] = page.viewport_size
    return options


def _openers(page, orphans):
    from playwright.sync_api import Error as PlaywrightError

    if not page.url.startswith(("http:", "https:", "file:")):
        return {}
    options = _trial_options(page)
    key = (page.url, json.dumps(options, sort_keys=True, default=str))
    if key in _trials:
        return {p: d for p, d in _trials[key].items() if d in orphans}
    context = page.context.browser.new_context(**options)
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
    return {
        **page.evaluate(READ_JS, [ov.trigger, ov.target]),
        "control": None,
        "settled": True,
    }


def find(page, within=None):
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
