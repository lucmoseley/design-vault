"""conditions.py — opens a page under the conditions a rule record loads it in
(#304), one way for every family script. Each value of the `conditions`
column of docs/data/script-families-tier01-2026-10-15.csv has an argument:

    forcedcolours  forced_colours=True
    colorscheme    scheme="light" or "dark"
    print          print_media=True
    locale         locale="de-DE", any BCP 47 tag
    rtl            rtl=True
    pointer        pointer="coarse" or "fine"
    block          block=("script",) or ("image",); scripts_off=True

A row that compares, as COL-53's each theme or STA-49's coarse against fine,
opens the page once under each.

A family script opens one page under a set of conditions:

    with flow.chromium() as browser:
        with conditions.open_page(browser, url, scheme="dark", rtl=True) as page:
            ...

Right-to-left sets `dir="rtl"` on the root element before
the page's own scripts run, so a page that reads its direction at load reads
rtl. An inner element's authored `dir` stands.

A block aborts each request of that Playwright resource type: the page as it
is when its script or image files fail to load. An inline script still
runs and `<noscript>` stays hidden. scripts_off turns scripting off instead,
so no script runs and `<noscript>` shows (LAY-74: with script blocked every
panel shows).
"""

import contextlib

SCHEMES = ("light", "dark")
POINTERS = ("coarse", "fine")
# Playwright's resource types the tier 0 and 1 rows block: script (LAY-74)
# and image (COL-12).
BLOCKABLE = ("script", "image")

# The root element does not exist yet; the observer sets its direction once
# the parser inserts it.
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
    **context_options,
):
    """The page at `url`, loaded, under the conditions given, in a context of
    its own that is closed on leaving. With none given it loads as Playwright's
    default: no forced colours, a light scheme, screen media, the machine's
    locale, the page's own direction, a fine pointer and every request let
    through.

    A value it cannot emulate raises ValueError before the browser is touched.
    `init_scripts` run before the page's own, after the right-to-left one, as
    check-flow.py's collector does. `context_options` go to
    browser.new_context() as they are (viewport, reduced_motion…); a condition
    named here wins over the same option there."""
    if scheme is not None:
        one_of("scheme", scheme, SCHEMES)
    if pointer is not None:
        one_of("pointer", pointer, POINTERS)
    if locale is not None and not locale:
        raise ValueError("locale must be a BCP 47 tag such as de-DE, not empty")
    for kind in block:
        one_of("block", kind, BLOCKABLE)
    options = dict(context_options)
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
