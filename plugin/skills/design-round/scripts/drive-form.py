"""drive-form.py — fills a candidate's form and submits it, for the checks
that judge what a form does with good and bad input (#302): where an error
shows, where focus goes, whether typed values survive. A library the check
scripts load; it judges nothing itself.

Its only I/O is the Playwright page it is handed, which the caller opens
and closes, as check-flow.py's chromium() does. A check loads it through siblings.py:

    form = siblings.load(HERE, "drive-form.py")

    form.fill(page, "#book", bad=["#email"])
    settled = form.submit(page, "#book")   # read settled.state: errors, focus, values

- fields(page, form) lists a form's fields: every input, select and textarea
  in `form.elements` a visitor can type into or choose. A field that is
  disabled, read-only, not drawn, or a hidden, file, range, colour or button
  input is left out, and a radio group is one field.
- fill(page, form, bad=…, values=…) gives each field a valid value, or a
  planted invalid one for each key in `bad`, chosen by its autocomplete token
  and its type, then its constraints. It types text key by key, so the page's
  input handlers see each key. A field it knows no valid value for is left as
  it is and reported; `values` gives such a field its own.
- submit(page, form, by=…) clicks the form's submit button, or presses Enter
  in its last single-line field, and returns once the page has settled: what
  the caller reads.
- after(page, action) runs any other action, a blur, a reload or Back, and
  returns read() once the page has settled, as submit() does.
- read(page) reads every field on the page, focus and live regions.

`form` is a CSS selector, and None takes the page's first <form>. A field's
key is a CSS selector for it: a radio group's `input[name="…"]`, else
`#id` where its id is unique, else `tag[name="…"]` where its name is, else
its path from the body. A form built without <form> is not driven.
"""

import collections
import contextlib
import time

# How long, in ms, the page's markup must go unchanged, with no request in
# flight, before a submit counts as settled: check-frames.py's quiet window
# for animations, a guess for forms. An error shown later than this after the
# last change is missed.
QUIET_MS = 500
# How often, in ms, an in-flight request is looked at again: a guess.
POLL_MS = 50
# The longest a submit may take to settle, in ms: Playwright's own default.
TIMEOUT_MS = 30000
# How many characters of the focused element's text read() keeps: a guess,
# enough to tell an error summary from a field.
FOCUS_TEXT_CHARS = 200
# `bad` for planting a bad value in every field.
ALL = "all"

Field = collections.namedtuple(
    "Field",
    "key tag type token value required pattern min_length max_length min max options",
)
# What fill() did to one field: `value` typed or chosen (True or False for a
# checkbox), None where nothing was; `planted` names how a bad value breaks
# the field; `valid` is the browser's own verdict after it, None where the
# page moved on; `note` says why a field was left, refused its good value,
# or ended the fill.
Filled = collections.namedtuple("Filled", "key value planted valid note")
# What submit() leaves: whether the page went to a new document (a history
# push is not one), the URL it settled on, how many submit events reached
# the page (none where the browser's own validation stopped the submit), and
# after()'s read.
Settled = collections.namedtuple("Settled", "navigated url submits state")


class FormError(Exception):
    """The page holds no such form or field, or the form has no way to
    submit. `what` holds the selector or keys at fault."""

    def __init__(self, message, what=()):
        super().__init__(message)
        self.what = tuple(what)


# Autocomplete tokens' detail words: the field name is the last word left
# once these are dropped (HTML's autofill detail tokens).
DETAIL_TOKENS = {
    "shipping",
    "billing",
    "home",
    "work",
    "mobile",
    "fax",
    "pager",
    "webauthn",
}

# A valid value for each autocomplete field name the house's forms use.
TOKEN_GOOD = {
    "name": "Ada Lovelace",
    "honorific-prefix": "Dr",
    "given-name": "Ada",
    "additional-name": "King",
    "family-name": "Lovelace",
    "nickname": "Ada",
    "username": "ada.lovelace",
    "new-password": "Correct-Horse-Battery-9",
    "current-password": "Correct-Horse-Battery-9",
    "one-time-code": "123456",
    "organization-title": "Engineer",
    "organization": "Example Ltd",
    "street-address": "12 Example Street",
    "address-line1": "12 Example Street",
    "address-line2": "Flat 3",
    "address-level2": "London",
    "address-level1": "Greater London",
    "country": "GB",
    "country-name": "United Kingdom",
    "postal-code": "SW1A 1AA",
    "bday": "1990-12-10",
    "bday-day": "10",
    "bday-month": "12",
    "bday-year": "1990",
    "language": "en",
    "url": "https://example.com",
    "email": "ada.lovelace@example.com",
    "tel": "+44 20 7946 0958",
    "tel-national": "020 7946 0958",
    "tel-local": "7946 0958",
}
# A malformed value for each field name a page can tell malformed: what a
# visitor's slip looks like, not a value no visitor would type.
TOKEN_BAD = {
    "email": "ada.lovelace@",
    "url": "example com",
    "tel": "call me",
    "tel-national": "call me",
    "tel-local": "call me",
    "postal-code": "SW1A",
    "one-time-code": "12",
    "new-password": "abc",
    "bday-year": "19",
}
# A valid value for each input type a token does not settle.
TYPE_GOOD = {
    "text": "Example text",
    "search": "dorm bed",
    "password": "Correct-Horse-Battery-9",
    "email": TOKEN_GOOD["email"],
    "tel": TOKEN_GOOD["tel"],
    "url": TOKEN_GOOD["url"],
    "date": "2030-06-15",
    "time": "10:30",
    "datetime-local": "2030-06-15T10:30",
    "month": "2030-06",
    "week": "2030-W24",
    "textarea": "A short message for the form.",
}
TYPE_BAD = {
    "email": TOKEN_BAD["email"],
    "url": TOKEN_BAD["url"],
    "tel": TOKEN_BAD["tel"],
}
# Types whose value is set whole, as their picker sets it, never typed.
PICKED = {"date", "time", "datetime-local", "month", "week"}
# Types the browser holds to a syntax of their own, which a token's value
# need not meet (`username` on an email field): the type's value wins.
SYNTAX = PICKED | {"email", "url"}
# A value no pattern a page sets for names, numbers or codes accepts.
OFF_PATTERN = "!!"

# keyOf(el): a field's key, as the module docstring gives it.
KEY_JS = r"""
const keyOf = (el) => {
  const unique = (sel) => document.querySelectorAll(sel).length === 1;
  const tag = el.tagName.toLowerCase();
  const named = el.name && `${tag}[name="${CSS.escape(el.name)}"]`;
  if (named && el.type === "radio") return named;
  if (el.id && unique(`#${CSS.escape(el.id)}`)) return `#${CSS.escape(el.id)}`;
  if (named && unique(named)) return named;
  const path = [];
  for (let at = el; at !== document.body; at = at.parentElement) {
    const same = [...at.parentElement.children].filter((c) => c.tagName === at.tagName);
    path.unshift(`${at.tagName.toLowerCase()}:nth-of-type(${same.indexOf(at) + 1})`);
  }
  return `body > ${path.join(" > ")}`;
};
"""

# formOf(form): the form a selector names, or why there is none.
FORM_JS = r"""
const formOf = (form) => {
  const root = form === null ? document.querySelector("form") : document.querySelector(form);
  if (!root) return form === null ? "the page has no form" : `no element matches ${form}`;
  return root.tagName === "FORM" ? root : `${form} is not a form`;
};
"""

# valueOf(el): a checkbox's checked state, a radio group's chosen value or
# null, else the value. BUTTONS: the input types that act rather than hold.
VALUE_JS = r"""
const valueOf = (el) => {
  if (el.type === "checkbox") return el.checked;
  if (el.type !== "radio") return el.value;
  const scope = el.form ? [...el.form.elements] : [...document.querySelectorAll("input")];
  const on = scope.find((r) => r.type === "radio" && r.name === el.name && r.checked);
  return on ? on.value : null;
};
const BUTTONS = ["submit", "reset", "button", "image"];
"""


def _script(params, *helpers, body):
    """A JavaScript arrow function of `params` holding the helper snippets
    above, then `body`."""
    return f"({params}) => {{\n{''.join(helpers)}{body}}}"


FIELDS_JS = _script(
    "form",
    KEY_JS,
    FORM_JS,
    VALUE_JS,
    body=r"""
  const root = formOf(form);
  if (typeof root === "string") return { error: root };
  const skip = new Set(["hidden", "file", "range", "color", ...BUTTONS]);
  const num = (v) => (v === "" ? null : Number(v));
  const out = [];
  const groups = new Set();
  for (const el of root.elements) {
    if (!["INPUT", "SELECT", "TEXTAREA"].includes(el.tagName)) continue;
    const type = el.tagName === "INPUT" ? el.type : el.tagName.toLowerCase();
    if (skip.has(type) || el.disabled || el.readOnly || !el.getClientRects().length) continue;
    if (type === "radio") {
      if (!el.name || groups.has(el.name)) continue;
      groups.add(el.name);
    }
    const group = type === "radio"
      ? [...root.elements].filter((r) => r.type === "radio" && r.name === el.name && !r.disabled)
      : [];
    out.push({
      key: keyOf(el),
      tag: el.tagName.toLowerCase(),
      type,
      token: el.getAttribute("autocomplete") || "",
      value: valueOf(el),
      required: el.required || group.some((r) => r.required),
      pattern: el.getAttribute("pattern"),
      min_length: el.minLength >= 0 ? el.minLength : null,
      max_length: el.maxLength >= 0 ? el.maxLength : null,
      min: type === "number" ? num(el.min) : el.min || null,
      max: type === "number" ? num(el.max) : el.max || null,
      options: type === "select"
        ? [...el.options].filter((o) => !o.disabled).map((o) => o.value)
        : group.map((r) => r.value),
    });
  }
  return { fields: out };
""",
)

MATCHES_JS = r"""
([pattern, value]) => {
  try { return new RegExp(`^(?:${pattern})$`, "v").test(value); } catch { return null; }
}
"""

# The form's first submit button's key, null where it has none.
BUTTON_JS = _script(
    "form",
    KEY_JS,
    FORM_JS,
    body=r"""
  const root = formOf(form);
  if (typeof root === "string") return { error: root };
  const button = [...root.elements].find(
    (el) => (el.tagName === "BUTTON" && el.type === "submit") ||
      (el.tagName === "INPUT" && (el.type === "submit" || el.type === "image")));
  return { key: button ? keyOf(button) : null };
""",
)

# Reports each submit event: a capture listener on window hears it before
# any handler of the page's can stop it.
ARM_JS = r"""
() => {
  if (window.__driveFormArmed) return;
  window.__driveFormArmed = true;
  addEventListener("submit", () => window.__driveFormSubmit(), true);
}
"""

# Marks the document an action starts in, so a later look can tell a new
# document (unmarked) from a history push in the same one.
MARK_JS = "() => { window.__driveFormMark = true; }"
MARKED_JS = "() => window.__driveFormMark === true"

# Resolves true once the markup has gone `quiet` ms without a change, or false
# at `limit` ms with it still changing.
QUIET_JS = r"""
([quiet, limit]) => new Promise((done) => {
  let last = performance.now();
  const start = last;
  const watch = new MutationObserver(() => { last = performance.now(); });
  watch.observe(document, { subtree: true, childList: true, attributes: true, characterData: true });
  const look = () => {
    const now = performance.now();
    if (now - last >= quiet) { watch.disconnect(); done(true); }
    else if (now - start >= limit) { watch.disconnect(); done(false); }
    else setTimeout(look, Math.min(quiet - (now - last), limit - (now - start)) + 1);
  };
  look();
})
"""

READ_JS = _script(
    "",
    KEY_JS,
    VALUE_JS,
    f"const FOCUS_TEXT_CHARS = {FOCUS_TEXT_CHARS};\n",
    body=r"""
  const controls = [...document.querySelectorAll("input, select, textarea")];
  const text = (el) => (el ? (el.innerText ?? el.textContent).replace(/\s+/g, " ").trim() : "");
  const referenced = (el, attr) =>
    (el.getAttribute(attr) || "").split(/\s+/).filter(Boolean)
      .map((id) => text(document.getElementById(id))).filter(Boolean);
  const fields = [];
  const groups = new Set();
  for (const el of controls) {
    if (el.type === "hidden" || BUTTONS.includes(el.type)) continue;
    if (el.type === "radio") {
      if (groups.has(el.name)) continue;
      groups.add(el.name);
    }
    fields.push({
      key: keyOf(el),
      value: valueOf(el),
      valid: el.validity.valid,
      message: el.validationMessage,
      invalid: el.getAttribute("aria-invalid") === "true",
      described: [...referenced(el, "aria-describedby"), ...referenced(el, "aria-errormessage")],
    });
  }
  const active = document.activeElement;
  const focus = !active || active === document.body ? null : {
    key: controls.includes(active) ? keyOf(active) : null,
    tag: active.tagName.toLowerCase(),
    id: active.id || null,
    role: active.getAttribute("role"),
    text: text(active).slice(0, FOCUS_TEXT_CHARS),
  };
  const live = [...document.querySelectorAll('[role="alert"], [role="status"], [aria-live]')]
    .filter((el) => el.getAttribute("aria-live") !== "off" && el.getClientRects().length)
    .map(text).filter(Boolean);
  return { url: location.href, focus, fields, live };
""",
)


def fields(page, form=None):
    """The fields of `form` a visitor fills, as Field records in its order."""
    found = page.evaluate(FIELDS_JS, form)
    if "error" in found:
        raise FormError(found["error"], [form] if form else [])
    return [Field(**f) for f in found["fields"]]


def name_of(token):
    """An autocomplete attribute's field name: `section-a shipping email` is
    `email`, `username webauthn` is `username`, and `off`, `on` or a bare
    detail word is none."""
    words = [
        w
        for w in token.lower().split()
        if not w.startswith("section-") and w not in DETAIL_TOKENS
    ]
    return words[-1] if words and words[-1] not in ("on", "off") else None


def _good_value(field):
    """A value `field` should accept: its autocomplete token's, unless its
    type holds it to a syntax of its own, else its type's, fitted to its
    length limits; None where none is known. A checkbox is True, a radio
    group or select its first choice with a value, a number its minimum or
    else 1."""
    if field.type == "checkbox":
        return True
    if field.type in ("radio", "select"):
        return next((o for o in field.options if o), None)
    if field.type == "number":
        if field.min is not None:
            return str(field.min)
        return "1" if field.max is None or field.max >= 1 else str(field.max)
    name = name_of(field.token)
    value = (
        TOKEN_GOOD[name]
        if field.type not in SYNTAX and name in TOKEN_GOOD
        else TYPE_GOOD.get(field.type)
    )
    if value is None:
        return None
    if field.min_length and len(value) < field.min_length:
        value += "x" * (field.min_length - len(value))
    if field.max_length is not None:
        value = value[: field.max_length].rstrip()
    return value


def _bad_value(field):
    """A value `field` should refuse and how it breaks the field, as
    (value, how), or (None, why none is known). In order: a malformed value
    for its token or type, a value off its pattern, one under its minimum
    length, one past its numeric bound, and, where it is required, nothing.
    A required checkbox is False, a required radio group or select left
    unchosen."""
    if field.type in ("checkbox", "radio", "select"):
        if not field.required:
            return None, "it is optional, so no choice is wrong"
        if field.type == "radio" and field.value is not None:
            return None, "a radio is already chosen, and a visitor cannot unchoose it"
        if field.type == "select" and "" not in field.options and field.value != "":
            return None, "it has no empty choice to leave it on"
        return (False if field.type == "checkbox" else ""), "left unchosen"
    if field.type not in PICKED:
        name = name_of(field.token)
        if name in TOKEN_BAD:
            return TOKEN_BAD[name], f"malformed {name}"
        if field.type in TYPE_BAD:
            return TYPE_BAD[field.type], f"malformed {field.type}"
    if field.pattern is not None:
        return OFF_PATTERN, f"off its pattern {field.pattern}"
    # The browser checks a minimum length only on a value of one character or more.
    if field.min_length and field.min_length >= 2:
        short = "x" * (field.min_length - 1)
        return short, f"under its minimum length {field.min_length}"
    if field.type == "number" and field.max is not None:
        return str(field.max + 1), f"over its maximum {field.max}"
    if field.type == "number" and field.min is not None:
        return str(field.min - 1), f"under its minimum {field.min}"
    if field.required:
        return "", "left empty"
    return None, "it is optional and sets no constraint to break"


def fill(page, form=None, *, bad=(), values=None):
    """Fills each field of `form`: a planted invalid value for each key in
    `bad` (ALL for every field), `values[key]` where given, else a valid
    one. Returns a Filled record for each field, in the form's order. A good
    value off the field's own pattern is not typed, nor is a bad one on it.
    A key in `bad` or `values` the form does not have is refused. Where
    setting a field submits the form or leaves the page, its record says so
    and is the last."""
    if isinstance(bad, str) and bad != ALL:
        raise TypeError(f"bad is a list of keys or ALL, not the string {bad!r}")
    found = fields(page, form)
    keys = {f.key for f in found}
    values = values or {}
    asked = set(keys if bad == ALL else bad) | set(values)
    if asked - keys:
        missing = sorted(asked - keys)
        raise FormError(f"the form has no field {', '.join(missing)}", missing)
    submits = _arm(page)
    page.evaluate(MARK_JS)
    out = []
    with _watch(page) as flying:
        for field in found:
            value, planted, note = _choose(page, field, bad, values)
            before = submits.count
            if value is not None:
                _set_field(page, field, value)
            moved = _moved(page, submits.count > before, flying)
            if moved:
                out.append(Filled(field.key, value, planted, None, moved))
                break
            valid, message = page.locator(field.key).first.evaluate(
                "(el) => [el.validity.valid, el.validationMessage]"
            )
            if not valid and value is not None and planted is None and note is None:
                note = f"the browser refuses this value: {message}"
            out.append(Filled(field.key, value, planted, valid, note))
    return out


def _choose(page, field, bad, values):
    """What fill() sets `field` to, as (value, planted, note)."""
    if field.key in values:
        return values[field.key], None, None
    if bad == ALL or field.key in bad:
        value, how = _bad_value(field)
        if value is None:
            return None, None, f"nothing to plant: {how}"
        if field.pattern is not None and value != "" and _matches(page, field, value):
            accepts = f"its pattern {field.pattern} accepts {value!r}"
            return None, None, f"nothing to plant: {accepts}"
        return value, how, None
    value = _good_value(field)
    if (
        value is not None
        and field.pattern is not None
        and _matches(page, field, value) is False
    ):
        value = None
    if value is None:
        return None, None, "no valid value known for it; pass one in values"
    return value, None, None


def _moved(page, submitted, flying):
    """Why setting a field ended the fill, None where it did not: it fired a
    submit event, or set the page loading another document. The round trip
    to the page first hands over the events the set raised."""
    from playwright.sync_api import Error as PlaywrightError

    try:
        marked = page.evaluate(MARKED_JS)
    except PlaywrightError as exc:
        if "context was destroyed" not in str(exc):
            raise
        marked = False
    if submitted:
        return "setting it submitted the form"
    if not marked or any(r.is_navigation_request() for r in flying):
        return "setting it left the page"
    return None


def _matches(page, field, value):
    """Whether `value` meets `field`'s pattern as the browser reads it (a
    JavaScript regular expression with the v flag), or None where the browser
    cannot read the pattern."""
    return page.evaluate(MATCHES_JS, [field.pattern, value])


def _set_field(page, field, value):
    """Sets one field as a visitor would: checks or unchecks a box, picks a
    radio or option, sets a picker's value whole, or clears a text field and
    types the value key by key. A radio group left unchosen, or a select
    left on the choice it holds, is not touched."""
    if (field.type == "radio" and value == "") or (
        field.type == "select" and value == field.value
    ):
        return
    element = page.locator(field.key).first
    if field.type == "checkbox":
        element.set_checked(value, force=True)
    elif field.type == "radio":
        quoted = value.replace("\\", "\\\\").replace('"', '\\"')
        page.locator(f'{field.key}[value="{quoted}"]').set_checked(True, force=True)
    elif field.type == "select":
        element.select_option(value=value)
    elif field.type in PICKED:
        element.fill(value)
    else:
        element.fill("")
        element.press_sequentially(value)


def submit(page, form=None, *, by="button", timeout=TIMEOUT_MS):
    """Submits `form` and returns a Settled once the page has. `by="button"`
    clicks the form's first submit button, the one Enter would press;
    `by="enter"` presses Enter in its last single-line text field. Raises
    FormError where the form has neither, and Playwright's TimeoutError where
    the page has not settled in `timeout` ms."""
    at = [form] if form else []
    if by == "button":
        found = page.evaluate(BUTTON_JS, form)
        if "error" in found:
            raise FormError(found["error"], at)
        if found["key"] is None:
            raise FormError("the form has no submit button", at)
        key = found["key"]
    elif by == "enter":
        lines = [
            f
            for f in fields(page, form)
            if f.tag == "input" and f.type not in ("checkbox", "radio")
        ]
        if not lines:
            raise FormError(
                "the form has no single-line text field to press Enter in", at
            )
        key = lines[-1].key
    else:
        raise ValueError(f"by is 'button' or 'enter', not {by!r}")
    submits = _arm(page)
    before = submits.count
    target = page.locator(key).first
    state = after(
        page,
        lambda: target.click(force=True) if by == "button" else target.press("Enter"),
        timeout=timeout,
    )
    return Settled(not state["kept"], state["url"], submits.count - before, state)


def after(page, action, *, timeout=TIMEOUT_MS):
    """Runs `action()` and returns read() once the page has settled after it:
    loaded, its markup QUIET_MS without a change, and no request in flight,
    across any document it goes to. The read adds `kept`, whether the page
    still holds the document the action started in. Raises Playwright's
    TimeoutError where the page has not settled in `timeout` ms."""
    page.evaluate(MARK_JS)
    # Watched from before the action: a request it starts is announced while
    # the action is still under way.
    with _watch(page) as flying:
        action()
        return _settle(page, flying, timeout)


class _Submits:
    """How many submit events a page has heard since _arm() set it up."""

    count = 0


def _arm(page):
    """The _Submits each submit event on `page` adds one to, from now on and
    in every document it goes on to load; set up on the page's first use."""
    if not hasattr(page, "_drive_form_submits"):
        submits = _Submits()

        def heard():
            submits.count += 1

        page.expose_function("__driveFormSubmit", heard)
        page.add_init_script(f"({ARM_JS})()")
        page.evaluate(ARM_JS)
        page._drive_form_submits = submits
    return page._drive_form_submits


@contextlib.contextmanager
def _watch(page):
    """While open, the set it yields holds `page`'s requests not yet
    answered."""
    flying = set()

    # Playwright takes a Python function as a handler, never a built-in.
    def started(request):
        flying.add(request)

    def ended(request):
        flying.discard(request)

    handlers = [
        ("request", started),
        ("requestfinished", ended),
        ("requestfailed", ended),
    ]
    for event, handler in handlers:
        page.on(event, handler)
    try:
        yield flying
    finally:
        for event, handler in handlers:
            page.remove_listener(event, handler)


def _settle(page, flying, timeout):
    """after()'s wait and read; `flying` is _watch()'s requests in flight."""
    # Imported here, not at the top, so a machine without Playwright reaches
    # check-flow.py's run_browser(), which names the install, before this runs.
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import TimeoutError as PlaywrightTimeout

    deadline = time.monotonic() + timeout / 1000
    while True:
        left = (deadline - time.monotonic()) * 1000
        if left <= 0:
            raise PlaywrightTimeout(f"the page did not settle in {timeout} ms")
        try:
            page.wait_for_load_state("load", timeout=left)
            if page.evaluate(QUIET_JS, [QUIET_MS, left]) and not flying:
                return {**read(page), "kept": page.evaluate(MARKED_JS)}
        except PlaywrightError as exc:
            # A navigation mid-read destroys the document the read ran in:
            # read the new one once it has loaded.
            if "context was destroyed" not in str(exc):
                raise
        if flying:
            page.wait_for_timeout(POLL_MS)


def read(page):
    """Every field on the page with its value (a checkbox's checked state, a
    radio group's chosen value or None), the browser's validity and message,
    its aria-invalid and the text its aria-describedby and aria-errormessage
    name; where focus is (None on the body); and the text of each drawn live
    region (role alert or status, or aria-live). Keys as fields() gives them."""
    return page.evaluate(READ_JS)
