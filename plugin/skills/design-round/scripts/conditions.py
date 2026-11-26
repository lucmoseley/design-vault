import contextlib

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
