import collections
import contextlib
import time

# guess, #501
QUIET_MS = 500
# guess, #501
POLL_MS = 50
# guess, #501
TIMEOUT_MS = 30000
# guess, #501
FOCUS_TEXT_CHARS = 200
ALL = "all"

Field = collections.namedtuple(
    "Field",
    "key tag type token value required pattern min_length max_length min max options",
)
Filled = collections.namedtuple("Filled", "key value planted valid note")
Settled = collections.namedtuple("Settled", "navigated url submits state")


class FormError(Exception):
    def __init__(self, message, what=()):
        super().__init__(message)
        self.what = tuple(what)


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
PICKED = {"date", "time", "datetime-local", "month", "week"}
SYNTAX = PICKED | {"email", "url"}
OFF_PATTERN = "!!"

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

FORM_JS = r"""
const formOf = (form) => {
  const root = form === null ? document.querySelector("form") : document.querySelector(form);
  if (!root) return form === null ? "the page has no form" : `no element matches ${form}`;
  return root.tagName === "FORM" ? root : `${form} is not a form`;
};
"""

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

ARM_JS = r"""
() => {
  if (window.__driveFormArmed) return;
  window.__driveFormArmed = true;
  addEventListener("submit", () => window.__driveFormSubmit(), true);
}
"""

MARK_JS = "() => { window.__driveFormMark = true; }"
MARKED_JS = "() => window.__driveFormMark === true"

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
    found = page.evaluate(FIELDS_JS, form)
    if "error" in found:
        raise FormError(found["error"], [form] if form else [])
    return [Field(**f) for f in found["fields"]]


def name_of(token):
    words = [
        w
        for w in token.lower().split()
        if not w.startswith("section-") and w not in DETAIL_TOKENS
    ]
    return words[-1] if words and words[-1] not in ("on", "off") else None


def _good_value(field):
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
    # The browser checks minlength only on a non-empty value:
    # https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#setting-minimum-input-length-requirements:-the-minlength-attribute
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
    return page.evaluate(MATCHES_JS, [field.pattern, value])


def _set_field(page, field, value):
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
    page.evaluate(MARK_JS)
    with _watch(page) as flying:
        action()
        return _settle(page, flying, timeout)


class _Submits:
    count = 0


def _arm(page):
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
    flying = set()

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
            if "context was destroyed" not in str(exc):
                raise
        if flying:
            page.wait_for_timeout(POLL_MS)


def read(page):
    return page.evaluate(READ_JS)
