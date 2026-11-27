import contextlib

DESKTOP_SCREEN = (1920, 1080)  # measured: the commonest desktop screen, #183
DESKTOP_BARS = 135  # measured on Windows 11 with Chromium, #197
DESKTOP_WINDOW = (DESKTOP_SCREEN[0], DESKTOP_SCREEN[1] - DESKTOP_BARS)
DESKTOP = f"{DESKTOP_WINDOW[0]}x{DESKTOP_WINDOW[1]}"
# WCAG 2.2 reflow is judged at 320 CSS px wide: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
LOW = 320
HIGH = 2560  # guess, #197
BANDS = (
    ("phone", 320, 767),
    ("tablet", 768, 1023),
    ("desktop", 1024, HIGH),
)  # guess, #501
PHONE_MAX = BANDS[0][2]
HEIGHTS = (664, 921, 768 - DESKTOP_BARS)  # measured 390x664, 768x921, #252
MOTION_HEIGHTS = (*HEIGHTS[:2], DESKTOP_WINDOW[1])
PHONE_WIDTH, DESKTOP_WIDTH = 390, DESKTOP_SCREEN[0]  # guess, #197
PHONE = {"has_touch": True}  # #229
MOBILE = {**PHONE, "is_mobile": True}

SETTLE_JS = r"""
async () => {
  await document.fonts.ready;
  let looping = 0;
  for (const a of document.getAnimations()) { try { a.finish(); } catch (e) { looping++; } }
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  scrollTo({ top: 0, left: 0, behavior: 'instant' });
  return looping;
}
"""

SCHEMES = ("light", "dark")
POINTERS = ("coarse", "fine")
BLOCKABLE = ("script", "image")

RTL_JS = r"""
(() => {
  const set = () => document.documentElement.setAttribute('dir', 'rtl');
  if (document.documentElement) return set();
  new MutationObserver((_, observer) => {
    if (!document.documentElement) return;
    set();
    observer.disconnect();
  }).observe(document, { childList: true });
})();
"""


def height_at(width, heights):
    for (_, low, high), tall in zip(BANDS, heights, strict=True):
        if low <= width <= high:
            return tall
    raise ValueError(f"{width} px is outside {LOW}–{HIGH}")


def is_phone(width):
    return width <= PHONE_MAX


def device(width):
    return PHONE if is_phone(width) else {}


VIEWPORTS = tuple(
    (name, width, height_at(width, HEIGHTS))
    for name, width in (
        ("desktop", DESKTOP_WIDTH),
        ("phone", PHONE_WIDTH),
    )
)


def size_arg(p, flag, value, *, number=int, example=DESKTOP):
    try:
        w, h = (number(n) for n in value.lower().split("x", 1))
    except ValueError:
        p.error(f"{flag} wants WxH, e.g. {example} — got {value!r}")
    return {"width": w, "height": h}


def one_of(name, value, allowed):
    if value not in allowed:
        raise ValueError(f"{name} must be one of {', '.join(allowed)}, not {value!r}")


@contextlib.contextmanager
def open_page(
    browser,
    url,
    *,
    forced_colours=False,
    scheme=None,
    print_media=False,
    locale=None,
    rtl=False,
    pointer=None,
    block=(),
    scripts_off=False,
    init_scripts=(),
    width=None,
    timeout=None,
    **context_options,
):
    if scheme is not None:
        one_of("scheme", scheme, SCHEMES)
    if pointer is not None:
        one_of("pointer", pointer, POINTERS)
    if locale is not None and not locale:
        raise ValueError("locale must be a BCP 47 tag such as de-DE, not empty")
    for kind in block:
        one_of("block", kind, BLOCKABLE)
    options = {}
    if width is not None:
        options.update(device(width))
        if "viewport" not in context_options:
            options["viewport"] = {"width": width, "height": height_at(width, HEIGHTS)}
    options.update(context_options)
    if forced_colours:
        options["forced_colors"] = "active"
    if scheme:
        options["color_scheme"] = scheme
    if locale:
        options["locale"] = locale
    if pointer:
        options["has_touch"] = pointer == "coarse"
    if scripts_off:
        options["java_script_enabled"] = False
    context = browser.new_context(**options)
    try:
        if timeout is not None:
            context.set_default_timeout(timeout)
        if rtl:
            context.add_init_script(RTL_JS)
        for script in init_scripts:
            context.add_init_script(script)
        if block:
            blocked = frozenset(block)
            context.route(
                "**/*",
                lambda route: (
                    route.abort()
                    if route.request.resource_type in blocked
                    else route.continue_()
                ),
            )
        page = context.new_page()
        if print_media:
            page.emulate_media(media="print")
        page.goto(url, wait_until="load")
        yield page
    finally:
        context.close()


def settle(page):
    return page.evaluate(SETTLE_JS)
