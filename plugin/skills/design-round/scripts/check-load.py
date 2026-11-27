#!/usr/bin/env python3
"""Times how long a web candidate makes a phone visitor wait for its main
content, answering gate question vault.load.

USAGE
  python3 check-load.py <url or file> [--runs N] [--limit MS] [--timeout MS]

It loads the page --runs times (3), each in a fresh browser context on Lighthouse's
throttled phone (below), and reads Largest Contentful Paint (LCP): the moment
the largest text block or image in the first screen is drawn, timed from
navigation. It prints each run's LCP and the element drawn, and passes when the
median is at most --limit ms (2500, web.dev's "good" LCP). A local file is
served over HTTP from its own folder.

The phone is Lighthouse's default mobile run, applied to a real load
(Lighthouse's "devtools" throttling), so its LCP can differ from a Lighthouse
report's, which is simulated.

The last LCP entry counts: the browser reports a larger element as it is
drawn, so a page that hides its headline behind a fade or a font wait reports
it when it shows. A run ends once no new entry has come for QUIET_MS after
load.

EXITS 0 the median LCP is within --limit / 1 it is over / 2 the arguments are
wrong / 3 Playwright or its browser is missing / 4 the page did not load in time
/ 5 the browser refused the page / 6 the page drew no LCP element / 7 a call
hung that would never return.
An exception it does not handle once loaded exits 2, its traceback on stderr.

FILES MODE
  python3 check-load.py <url or file> --files --out DIR [--parts FILE]
        [--table FILE] [--timeout MS]

It loads the page once, unthrottled, reads every font, image, stylesheet and
script file the page fetches, and answers the rule records that turn on what
those files hold (font-file.py reads the fonts). Which face draws each text
is the browser's own answer (CDP CSS.getPlatformFontsForNode), matched to a
loaded file by its PostScript name. --parts is the building session's parts
declaration: it names the cookie-banner, without which vault.cookie-banner
is not judged, and any icon parts beyond those found by size.

THE TABLE, by default check-load.table beside this script, gives each line as
fields split by " | ": the record id, the check, and the value it reads,
where it reads one. Blank lines and lines starting with # are skipped.

  coverage            each text's first family draws every character of it:
                      none falls to a later family or the browser's
                      installed fallback, save a later family the page loads
                      as a web font or one named for emoji
  distinct >= D       I, l and 1, each scaled to one height, differ pairwise
                      by D or more of their ink, in every face that sets text
  small-caps          small-caps text is drawn from a file carrying smcp
                      (all-small-caps: and c2sc), with
                      font-synthesis-small-caps none, and italic only from
                      an italic file
  features            every feature font-feature-settings switches on is in
                      the drawing file's GSUB or GPOS and has no font-variant
                      or font-kerning property; no font-feature-settings or
                      font-variant declaration precedes a font shorthand in
                      one rule
  tabular             numbers in table cells, live regions and outputs are in
                      a face whose figures share one advance under
                      tabular-nums
  variable weights >= N
                      a variable file draws N or more weights, an in-between
                      weight, a width other than 100% or a GRAD setting
  opsz display >= Mpx a file with an opsz axis draws text both under M px
                      and at M px or over
  vector icon <= Npx  every icon is SVG, inline or a file read by its bytes;
                      an icon is a declared icon part, or an image (img, an
                      image input, a CSS background or mask) in a link,
                      button, navigation, list item or label at most N px
                      each way
  banner A, B, …      the declared cookie-banner shows where, and only where,
                      the page needs consent: it sets a cookie or storage key
                      beginning with a listed name, sets a cookie for another
                      site, or requests or names in a script a listed host
                      (a value holding a dot)
  cookies-page RE     a link in the footer matches RE by its text or address

Each record id's finding is fail where any check misses, else not judged
where a check could not run, else pass, or no match where nothing on the page
fell under a check. DIR/files.json holds every finding and each file read; an
earlier run's is deleted. The files mode exits as the timing does, 1 meaning
a miss and 2 also a table or declaration it cannot read; it never exits 6.
"""

import argparse
import base64
import collections
import contextlib
import functools
import http.server
import os
import re
import statistics
import sys
import threading
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402
from crash_exit import run_main  # noqa: E402
from fail_open import expected  # noqa: E402


runner = siblings.load(HERE, "runner.py")
answers_file = siblings.load(HERE, "answers-file.py")
fontfile = siblings.load(HERE, "font-file.py")
probe = siblings.load(HERE, "probe.py")
rule_table = siblings.load(HERE, "rule-table.py")

# web.dev's "good" LCP, at the 75th percentile of page loads: https://web.dev/articles/lcp
LIMIT_MS = 2500
# guess, #501
RUNS = 3
# Lighthouse's mobileSlow4G, devtools-scaled, in the bytes per second CDP takes:
# https://github.com/GoogleChrome/lighthouse/blob/main/core/config/constants.js
LATENCY_MS = 150 * 3.75
DOWN_BYTES = 1.6 * 1024 * 0.9 * 1024 / 8
UP_BYTES = 750 * 0.9 * 1024 / 8
CPU_SLOWDOWN = 4
# Lighthouse's mobile screen and user agent: https://github.com/GoogleChrome/lighthouse/blob/main/core/config/constants.js
SCREEN = {"width": 412, "height": 823}
SCALE = 1.75
USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 11; moto g power (2022)) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36"
)
# guess, #501
QUIET_MS = 5000
# guess, #501
TIMEOUT_MS = 60000
# guess, #501
POLL_MS = 250

OBSERVE_JS = r"""
window.__lcp = null;
new PerformanceObserver((list) => {
  for (const e of list.getEntries()) {
    const el = e.element;
    let label = el ? el.tagName.toLowerCase() : '(removed)';
    if (el && el.id) label += '#' + el.id;
    window.__lcp = { ms: e.startTime, element: label, at: performance.now() };
  }
}).observe({ type: 'largest-contentful-paint', buffered: true });
"""


def parse(argv):
    p = argparse.ArgumentParser(
        prog="check-load.py", description=__doc__.split("\n\n")[0]
    )
    p.add_argument("page")
    p.add_argument("--runs", type=int, default=RUNS)
    p.add_argument("--limit", type=int, default=LIMIT_MS)
    p.add_argument("--timeout", type=int, default=TIMEOUT_MS)
    p.add_argument("--files", action="store_true", help="read the files the page loads")
    p.add_argument("--out", metavar="DIR", help="--files: where files.json goes")
    p.add_argument(
        "--parts",
        metavar="FILE",
        help=f"--files: the building session's parts declaration, {probe.DECLARATION}",
    )
    p.add_argument(
        "--table", default=TABLE, metavar="FILE", help="--files: the check table"
    )
    at = p.parse_args(argv)
    if at.runs < 1:
        p.error(f"--runs wants 1 or more — got {at.runs}")
    at.url = runner.page_url(p, at.page)
    if not at.files:
        return at
    if not at.out:
        p.error("--files wants --out DIR")
    try:
        with open(at.table, encoding="utf8") as fh:
            at.lines = parse_table(fh.read())
    except OSError as exc:
        p.error(f"cannot read --table {at.table}: {exc.strerror}")
    except TableError as exc:
        p.error(f"--table {at.table}: {exc}")
    at.declared, at.undeclared = {}, set()
    if at.parts:
        try:
            with open(at.parts, encoding="utf8") as fh:
                at.declared, at.undeclared = probe.declared_parts(fh.read())
        except OSError as exc:
            p.error(f"cannot read --parts {at.parts}: {exc.strerror}")
        except probe.DeclarationError as exc:
            p.error(f"--parts {at.parts} {exc}")
    return at


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(url):
    parts = urllib.parse.urlparse(url)
    if parts.scheme != "file":
        return None, url
    path = urllib.parse.unquote(parts.path)
    handler = functools.partial(Quiet, directory=os.path.dirname(path))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    name = urllib.parse.quote(os.path.basename(path))
    return server, f"http://127.0.0.1:{server.server_address[1]}/{name}"


def one_run(browser, url, timeout):
    context = browser.new_context(
        viewport=SCREEN,
        device_scale_factor=SCALE,
        is_mobile=True,
        has_touch=True,
        user_agent=USER_AGENT,
    )
    try:
        page = context.new_page()
        page.set_default_timeout(timeout)
        page.add_init_script(OBSERVE_JS)
        cdp = context.new_cdp_session(page)
        cdp.send("Network.enable")
        cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
        cdp.send(
            "Network.emulateNetworkConditions",
            {
                "offline": False,
                "latency": LATENCY_MS,
                "downloadThroughput": DOWN_BYTES,
                "uploadThroughput": UP_BYTES,
            },
        )
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": CPU_SLOWDOWN})
        page.goto(url, wait_until="load")
        loaded = page.evaluate("performance.now()")
        waited = 0
        while True:
            lcp = page.evaluate("window.__lcp")
            now = page.evaluate("performance.now()")
            since = now - max(lcp["at"] if lcp else 0, loaded)
            if since >= QUIET_MS:
                return lcp
            if waited >= timeout:
                raise runner.PageTimeoutError(
                    "a new LCP entry kept coming for the whole --timeout"
                )
            page.wait_for_timeout(POLL_MS)
            waited += POLL_MS
    finally:
        context.close()


TABLE = os.path.join(HERE, "check-load.table")
CHECKS = {
    "coverage": None,
    "distinct": re.compile(r">=\s*(0?\.\d+|[01])"),
    "small-caps": None,
    "features": None,
    "tabular": None,
    "variable": re.compile(r"weights\s*>=\s*(\d+)"),
    "opsz": re.compile(r"display\s*>=\s*(\d+(?:\.\d+)?)px"),
    "vector": re.compile(r"icon\s*<=\s*(\d+(?:\.\d+)?)px"),
    "banner": re.compile(r"(\S.*)"),
    "cookies-page": re.compile(r"(\S.*)"),
}
# CSS Fonts 4's generic families, and two vendor system-font keywords:
# https://www.w3.org/TR/css-fonts-4/#generic-font-families
GENERIC = {
    "serif",
    "sans-serif",
    "monospace",
    "cursive",
    "fantasy",
    "system-ui",
    "ui-serif",
    "ui-sans-serif",
    "ui-monospace",
    "ui-rounded",
    "emoji",
    "math",
    "fangsong",
    "-apple-system",
    "blinkmacsystemfont",
}
# The feature tag each CSS font-variant property switches on: https://www.w3.org/TR/css-fonts-4/
EQUIVALENT = {
    **dict.fromkeys(("kern",), "font-kerning"),
    **dict.fromkeys(("liga", "clig", "dlig", "hlig", "calt"), "font-variant-ligatures"),
    **dict.fromkeys(("subs", "sups"), "font-variant-position"),
    **dict.fromkeys(
        ("smcp", "c2sc", "pcap", "c2pc", "unic", "titl"), "font-variant-caps"
    ),
    **dict.fromkeys(
        ("lnum", "onum", "pnum", "tnum", "frac", "afrc", "ordn", "zero"),
        "font-variant-numeric",
    ),
    **dict.fromkeys(("hist",), "font-variant-alternates"),
    **dict.fromkeys(
        ("jp78", "jp83", "jp90", "jp04", "smpl", "trad", "fwid", "pwid", "ruby"),
        "font-variant-east-asian",
    ),
}
FEATURE_PROPERTY = re.compile(r"font-feature-settings|font-variant(-[a-z-]+)?")
PAIRS = (("I", "l"), ("I", "1"), ("l", "1"))
SMALL_CAPS = {"small-caps": ("smcp",), "all-small-caps": ("smcp", "c2sc")}
# Image file signatures: https://mimesniff.spec.whatwg.org/#matching-an-image-type-pattern
RASTER = (
    (b"\x89PNG\r\n\x1a\n", "PNG"),
    (b"\xff\xd8\xff", "JPEG"),
    (b"GIF87a", "GIF"),
    (b"GIF89a", "GIF"),
    (b"BM", "BMP"),
    (b"\x00\x00\x01\x00", "ICO"),
)


TableError = rule_table.TableError


def parse_table(text):
    return rule_table.parse(text, CHECKS, _line_value)


def _line_value(n, check, m):
    if m is None:
        return None
    raw = m[1]
    if check in ("distinct", "opsz", "vector"):
        return float(raw)
    if check == "variable":
        return int(raw)
    if check == "banner":
        return [t.strip() for t in raw.split(",") if t.strip()]
    try:
        return re.compile(raw)
    except re.error as exc:
        raise TableError(
            f"line {n}: cookies-page wants a regular expression: {exc}"
        ) from exc


READ_JS = r"""
({ icon, banner }) => {
  const drawn = (el) => el.getClientRects().length > 0
    && getComputedStyle(el).visibility !== "hidden";
  const where = (el) => {
    const parts = [];
    for (let e = el; e && e.nodeType === 1 && parts.length < 3; e = e.parentElement) {
      let s = e.tagName.toLowerCase();
      if (e.id) { parts.unshift(`${s}#${e.id}`); break; }
      const same = e.parentElement ? [...e.parentElement.children].filter((c) => c.tagName === e.tagName) : [];
      if (same.length > 1) s += `:nth-of-type(${same.indexOf(e) + 1})`;
      parts.unshift(s);
    }
    return parts.join(" > ");
  };
  const faces = [];
  const unquote = (v) => v.trim().replace(/^(["'])(.*)\1$/, "$2");
  const walk = (rules, base) => {
    for (const r of rules) {
      if (r instanceof CSSFontFaceRule) {
        const src = [...r.style.getPropertyValue("src").matchAll(/url\(\s*(["']?)(.*?)\1\s*\)/g)]
          .map((m) => new URL(m[2], base).href);
        faces.push({ family: unquote(r.style.getPropertyValue("font-family")),
          style: r.style.getPropertyValue("font-style") || "normal", src });
      } else if (r.cssRules) walk(r.cssRules, base);
    }
  };
  for (const sheet of document.styleSheets) {
    try { walk(sheet.cssRules, sheet.href || location.href); } catch (e) { continue; }
  }
  const SKIP = new Set(["SCRIPT", "STYLE", "NOSCRIPT", "TEMPLATE", "TITLE"]);
  const NUMBERS = 'td, th, output, [aria-live]:not([aria-live="off"]), [role="status"], [role="timer"], [role="log"], [role="marquee"]';
  const texts = [];
  for (const el of [document.body, ...document.body.querySelectorAll("*")]) {
    if (SKIP.has(el.tagName)) continue;
    const own = [...el.childNodes].filter((c) => c.nodeType === 3).map((c) => c.data)
      .join("").replace(/\s+/g, " ").trim();
    if (!own || !drawn(el)) continue;
    const cs = getComputedStyle(el);
    el.setAttribute("data-vault-net", texts.length);
    const read = { where: where(el), text: own, family: cs.fontFamily, weight: cs.fontWeight,
      style: cs.fontStyle, stretch: cs.fontStretch, size: parseFloat(cs.fontSize),
      caps: cs.fontVariantCaps, synthesis: cs.fontSynthesisSmallCaps,
      features: cs.fontFeatureSettings, variations: cs.fontVariationSettings,
      numbers: /\d/.test(own) && !!el.closest(NUMBERS) };
    if (read.numbers) {
      const probe = document.createElement("span");
      probe.style.cssText = "position:absolute;visibility:hidden;white-space:pre;font-size:100px;font-variant-numeric:tabular-nums";
      for (const p of ["fontFamily", "fontWeight", "fontStyle", "fontStretch"]) probe.style[p] = cs[p];
      document.body.append(probe);
      read.advances = [..."0123456789"].map((d) => { probe.textContent = d; return probe.getBoundingClientRect().width; });
      probe.remove();
    }
    texts.push(read);
  }
  const ACTION = 'a, button, nav, li, label, summary, [role="button"], [role="link"], [role="menuitem"], [role="tab"]';
  const declared = icon ? [...document.querySelectorAll(icon)] : [];
  const images = [];
  const urls = (v) => [...v.matchAll(/url\(\s*(["']?)(.*?)\1\s*\)/g)].map((m) => new URL(m[2], location.href).href);
  for (const el of document.body.querySelectorAll("*")) {
    if (!drawn(el)) continue;
    const cs = getComputedStyle(el);
    let src = [...urls(cs.backgroundImage), ...urls(cs.maskImage || cs.webkitMaskImage || "")];
    if (el.tagName === "IMG" && (el.currentSrc || el.src)) src.unshift(el.currentSrc || el.src);
    if (el.tagName === "INPUT" && el.type === "image" && el.src) src.unshift(el.src);
    if (!src.length) continue;
    const box = el.getBoundingClientRect();
    images.push({ where: where(el), src, width: box.width, height: box.height,
      action: !!el.closest(ACTION), declared: declared.some((d) => d === el || d.contains(el)) });
  }
  const keys = (store) => { try { return Object.keys(store()); } catch (e) { return null; } };
  const local = keys(() => localStorage), session = keys(() => sessionStorage);
  const footer = [...document.querySelectorAll('footer, [role="contentinfo"]')];
  return {
    faces, texts, images,
    stores: local && session ? [...local, ...session] : null,
    scripts: [...document.scripts].filter((s) => !s.src).map((s) => s.textContent),
    styles: [...document.querySelectorAll("style")].map((s) => s.textContent),
    inline: [...document.querySelectorAll("[style]")].map((e) => [where(e), e.getAttribute("style")]),
    footer: footer.length ? footer.flatMap((f) => [...f.querySelectorAll("a[href]")]
      .map((a) => [a.textContent.replace(/\s+/g, " ").trim(), a.getAttribute("href")])) : null,
    banner: banner ? [...document.querySelectorAll(banner)].some(drawn) : null,
  };
}
"""

DISTINCT_JS = r"""
async ({ family, weight, style }) => {
  const S = 200, N = 64;
  const font = `${style} ${weight} ${S}px ${family}`;
  await document.fonts.load(font, "Il1");
  const ink = (ch) => {
    const c = document.createElement("canvas"); c.width = S * 2; c.height = S * 2;
    const x = c.getContext("2d"); x.font = font; x.fillText(ch, S / 2, S * 1.5);
    const d = x.getImageData(0, 0, c.width, c.height).data;
    let t = Infinity, b = -1, l = Infinity, r = -1;
    for (let y = 0; y < c.height; y++) for (let i = 0; i < c.width; i++) {
      if (d[(y * c.width + i) * 4 + 3] > 127) { t = Math.min(t, y); b = Math.max(b, y); l = Math.min(l, i); r = Math.max(r, i); }
    }
    if (b < 0) return null;
    const o = document.createElement("canvas"); o.width = 2 * N; o.height = N;
    const w = (r - l + 1) * N / (b - t + 1);
    o.getContext("2d").drawImage(c, l, t, r - l + 1, b - t + 1, N - w / 2, 0, w, N);
    const od = o.getContext("2d").getImageData(0, 0, 2 * N, N).data;
    return Array.from({ length: 2 * N * N }, (_, i) => od[i * 4 + 3] > 127);
  };
  const glyphs = Object.fromEntries([..."Il1"].map((ch) => [ch, ink(ch)]));
  const apart = (a, b) => {
    if (!a || !b) return null;
    let only = 0, either = 0;
    for (let i = 0; i < a.length; i++) { if (a[i] || b[i]) either++; if (a[i] !== b[i]) only++; }
    return only / either;
  };
  return Object.fromEntries([["I", "l"], ["I", "1"], ["l", "1"]].map(([a, b]) => [a + b, apart(glyphs[a], glyphs[b])]));
}
"""

UNBROTLI_JS = r"""
async (url) => {
  const bytes = new Uint8Array(await (await fetch(url)).arrayBuffer());
  let s = "";
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(s);
}
"""


class _Brotli(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = self.server.blobs.get(self.path)
        self.send_response(200)
        if body is None:
            body = b"<!doctype html><title>unbrotli</title>"
            self.send_header("Content-Type", "text/html")
        else:
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Encoding", "br")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


@contextlib.contextmanager
def unbrotli(context):
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Brotli)
    server.blobs = {}
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    page = context.new_page()
    try:
        page.goto(base + "/")

        def decode(data):
            path = f"/{len(server.blobs)}"
            server.blobs[path] = bytes(data)
            return base64.b64decode(page.evaluate(UNBROTLI_JS, base + path))

        yield decode
    finally:
        page.close()
        server.shutdown()


def read_files(browser, url, *, declared, timeout):
    context = browser.new_context()
    try:
        page = context.new_page()
        page.set_default_timeout(timeout)
        responses, requested = [], []
        page.on("response", lambda r: responses.append(r))
        page.on("request", lambda r: requested.append(r.url))
        page.goto(url, wait_until="load")
        page.evaluate("document.fonts.ready.then(() => true)")
        read = page.evaluate(
            READ_JS,
            {"icon": declared.get("icon"), "banner": declared.get("cookie-banner")},
        )
        cdp = context.new_cdp_session(page)
        cdp.send("DOM.enable")
        cdp.send("CSS.enable")
        root = cdp.send("DOM.getDocument")["root"]["nodeId"]
        for n, text in enumerate(read["texts"]):
            node = cdp.send(
                "DOM.querySelector",
                {"nodeId": root, "selector": f'[data-vault-net="{n}"]'},
            )["nodeId"]
            text["fonts"] = cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node})[
                "fonts"
            ]
        from playwright.sync_api import Error as PlaywrightError

        bodies, unread = {}, []
        for r in responses:
            if r.request.resource_type in ("font", "image", "stylesheet", "script"):
                try:
                    bodies[r.url] = (r.request.resource_type, r.body())
                except PlaywrightError as exc:
                    expected(exc, "said as not judged")
                    unread.append(
                        (r.url, r.request.resource_type, runner.first_line(exc))
                    )
        fonts = {}
        with unbrotli(context) as decode:
            for src in {s for face in read["faces"] for s in face["src"]} | {
                u for u, (kind, _) in bodies.items() if kind == "font"
            }:
                data = bodies.get(src, (None, None))[1] or _data_url(src)
                if data is None:
                    why = next((w for u, _, w in unread if u == src), None)
                    if why:
                        fonts[src] = f"its body was not read: {why}"
                    continue
                try:
                    fonts[src] = fontfile.read(data, decode)
                except fontfile.FontError as exc:
                    expected(exc, "said as not judged")
                    fonts[src] = str(exc)
        faces = sorted(
            {
                (_stack(t["family"])[0], t["weight"], t["style"])
                for t in read["texts"]
                if _stack(t["family"])
            }
        )
        read["distinct"] = [
            [
                family,
                weight,
                style,
                page.evaluate(
                    DISTINCT_JS,
                    {"family": _css_family(family), "weight": weight, "style": style},
                ),
            ]
            for family, weight, style in faces
        ]
        read["cookies"] = context.cookies()
        read["requested"] = requested
        read["unread"] = unread
        read["bodies"] = {u: (kind, data) for u, (kind, data) in bodies.items()}
        read["fonts"] = fonts
        read["url"] = page.url
        return read
    finally:
        context.close()


def _data_url(src):
    if not src.startswith("data:"):
        return None
    head, _, payload = src[5:].partition(",")
    if head.endswith(";base64"):
        return base64.b64decode(payload)
    return urllib.parse.unquote_to_bytes(payload)


def _stack(value):
    return [
        f.strip().strip("\"'")
        for f in re.findall(r'"[^"]*"|\'[^\']*\'|[^,]+', value)
        if f.strip().strip("\"'")
    ]


def _css_family(family):
    return (
        family if family.lower() in GENERIC else '"' + family.replace('"', '\\"') + '"'
    )


class _Faces:
    def __init__(self, read):
        self.by_name = collections.defaultdict(list)
        self.families = collections.defaultdict(set)
        self.italic = collections.defaultdict(bool)
        for src, font in read["fonts"].items():
            if isinstance(font, fontfile.Font) and font.postscript:
                self.by_name[font.postscript].append((src, font))
        for face in read["faces"]:
            for src in face["src"]:
                self.families[src].add(face["family"].lower())
                if face["style"].startswith(("italic", "oblique")):
                    self.italic[src] = True
        self.web = {face["family"].lower() for face in read["faces"]}

    def files(self, used):
        return (
            self.by_name.get(used.get("postScriptName"), [])
            if used["isCustomFont"]
            else []
        )

    def is_family(self, used, family):
        family = family.lower()
        files = self.files(used)
        if files:
            return any(family in self.families[src] for src, _ in files)
        return used["familyName"].lower() == family

    def first(self, text):
        stack = _stack(text["family"])
        if not stack:
            return []
        if stack[0].lower() in GENERIC:
            return sorted(text["fonts"], key=lambda f: -f["glyphCount"])[:1]
        return [f for f in text["fonts"] if self.is_family(f, stack[0])]


def findings(table, read, *, declared, undeclared):
    answers = rule_table.Answers(table, "where")
    faces = _Faces(read)
    checks = {
        "coverage": _coverage,
        "distinct": _distinct,
        "small-caps": _small_caps,
        "features": _features,
        "tabular": _tabular,
        "variable": _variable,
        "opsz": _opsz,
        "vector": _vector,
        "banner": functools.partial(_banner, declared=declared, undeclared=undeclared),
        "cookies-page": _cookies_page,
    }
    for line in table:
        checks[line.check](answers, line, read, faces)
    return answers.done()


def _coverage(answers, line, read, faces):
    for t in read["texts"]:
        stack = _stack(t["family"])
        if not stack or not t["fonts"]:
            continue
        answers.met(line)
        first = faces.first(t)
        if not first:
            answers.miss(
                line, t["where"], f"{stack[0]} draws none of {_quote(t['text'])}"
            )
            continue
        missing = ""
        if stack[0].lower() in faces.web:
            held = set().union(*(f.chars for u in first for _, f in faces.files(u)))
            gone = dict.fromkeys(
                c for c in t["text"] if not c.isspace() and ord(c) not in held
            )
            missing = f" ({''.join(gone)})" if gone else ""
        for used in t["fonts"]:
            if used in first or _on_purpose(used, stack[1:], faces):
                continue
            how = (
                "a later family"
                if any(faces.is_family(used, f) for f in stack[1:])
                else "the browser's installed fallback"
            )
            answers.miss(
                line,
                t["where"],
                f"{used['glyphCount']} glyph(s){missing} of {_quote(t['text'])} fall to "
                f"{used['familyName']}, {how}, not {stack[0]}",
            )


def _on_purpose(used, later, faces):
    return any(
        faces.is_family(used, f) and (f.lower() in faces.web or "emoji" in f.lower())
        for f in later
    )


def _distinct(answers, line, read, faces):
    for family, weight, style, apart in read["distinct"]:
        for a, b in PAIRS:
            got = apart.get(a + b)
            if got is None:
                answers.unjudged(line, family, f"{family} draws no {a} or no {b}")
                continue
            answers.met(line)
            if got < line.value:
                answers.miss(
                    line,
                    f"{family} {weight} {style}",
                    f"{a} and {b} differ by {got:.3f} of their ink, under {line.value}",
                )


def _small_caps(answers, line, read, faces):
    for t in read["texts"]:
        wanted = SMALL_CAPS.get(t["caps"])
        if not wanted:
            continue
        files = [pair for used in faces.first(t) for pair in faces.files(used)]
        if not files:
            answers.unjudged(
                line,
                t["where"],
                f"{t['caps']} in an installed face, whose file the page does not load",
            )
            continue
        answers.met(line)
        held = set().union(*(f.features for _, f in files))
        for tag in wanted:
            if tag not in held:
                answers.miss(
                    line,
                    t["where"],
                    f"{t['caps']} from a face with no {tag}: synthesised",
                )
        if t["synthesis"] != "none":
            answers.miss(
                line,
                t["where"],
                f"font-synthesis-small-caps is {t['synthesis']}, not none",
            )
        if t["style"] != "normal" and not any(
            f.italic or faces.italic[src] for src, f in files
        ):
            answers.miss(
                line,
                t["where"],
                f"{t['style']} small capitals from an upright face: a synthesised slant",
            )


def _features(answers, line, read, faces):
    for t in read["texts"]:
        on = [
            tag
            for tag, value in re.findall(r'"(\w{4})"\s*(\w*)', t["features"])
            if value in ("", "on") or (value.isdigit() and int(value) > 0)
        ]
        if not on:
            continue
        files = [pair for used in faces.first(t) for pair in faces.files(used)]
        held = set().union(*(f.features for _, f in files)) if files else None
        answers.met(line)
        for tag in on:
            if tag in EQUIVALENT:
                answers.miss(
                    line,
                    t["where"],
                    f'font-feature-settings switches on "{tag}", which {EQUIVALENT[tag]} sets',
                )
            elif held is None:
                answers.unjudged(
                    line,
                    t["where"],
                    f'"{tag}" in an installed face, whose file the page does not load',
                )
            elif tag not in held:
                answers.miss(
                    line,
                    t["where"],
                    f'"{tag}" is switched on, and the face has no {tag}',
                )
    blocks = [
        (sel.strip(), body)
        for css in read["styles"]
        + [d for kind, d in read["bodies"].values() if kind == "stylesheet"]
        for sel, body in re.findall(
            r"([^{}]*)\{([^{}]*)\}", re.sub(r"/\*.*?\*/", "", _text(css), flags=re.S)
        )
    ] + [(where, style) for where, style in read["inline"]]
    for url, kind, why in read["unread"]:
        if kind == "stylesheet":
            answers.unjudged(
                line,
                _short(url),
                f"the stylesheet's body was not read, so its rules' order is not: {why}",
            )
    for where, body in blocks:
        names = [
            d.split(":", 1)[0].strip().lower() for d in body.split(";") if ":" in d
        ]
        if not any(FEATURE_PROPERTY.fullmatch(n) for n in names):
            continue
        answers.met(line)
        shorthand = max((i for i, n in enumerate(names) if n == "font"), default=0)
        for n in names[:shorthand]:
            if FEATURE_PROPERTY.fullmatch(n):
                answers.miss(
                    line, where, f"{n} comes before the font shorthand, which resets it"
                )


def _text(css):
    return css.decode("utf8", "replace") if isinstance(css, bytes) else css


def _tabular(answers, line, read, faces):
    for t in read["texts"]:
        if not t["numbers"]:
            continue
        answers.met(line)
        widths = sorted(set(t.get("advances", [])))
        if len(widths) > 1:
            answers.miss(
                line,
                t["where"],
                f"{_quote(t['text'])}: {_stack(t['family'])[0]} draws its figures at {len(widths)} advances, even with tabular-nums",
            )


def _drawn_by(read, faces):
    out = collections.defaultdict(list)
    for t in read["texts"]:
        for used in faces.first(t):
            for src, font in faces.files(used):
                if font.axes:
                    out[src].append(t)
    return [(src, read["fonts"][src], texts) for src, texts in out.items()]


def _variable(answers, line, read, faces):
    for src, font, texts in _drawn_by(read, faces):
        answers.met(line)
        weights = {float(t["weight"]) for t in texts}
        between = any(w % 100 for w in weights)
        width = any(t["stretch"] not in ("100%", "normal") for t in texts)
        grade = any("GRAD" in t["variations"] for t in texts)
        if len(weights) < line.value and not (between or width or grade):
            shown = ", ".join(f"{w:g}" for w in sorted(weights))
            answers.miss(
                line,
                _short(src),
                f"a variable file ({', '.join(font.axes)}) drawing weight {shown} alone, under {line.value} weights, with no in-between weight, width or grade",
            )


def _opsz(answers, line, read, faces):
    for src, font, texts in _drawn_by(read, faces):
        if "opsz" not in font.axes:
            continue
        answers.met(line)
        sizes = {t["size"] for t in texts}
        if not (min(sizes) < line.value <= max(sizes)):
            span = (
                f"{min(sizes):g}–{max(sizes):g} px"
                if len(sizes) > 1
                else f"{min(sizes):g} px"
            )
            answers.miss(
                line,
                _short(src),
                f"an opsz axis on a face drawn at {span} alone, not both under and from {line.value:g} px",
            )


def _vector(answers, line, read, faces):
    for img in read["images"]:
        small = img["width"] <= line.value and img["height"] <= line.value
        if not (img["declared"] or (img["action"] and small)):
            continue
        for src in img["src"]:
            data = read["bodies"].get(src, (None, None))[1] or _data_url(src)
            if data is None:
                answers.unjudged(line, img["where"], f"{_short(src)} was not fetched")
                continue
            answers.met(line)
            raster = _raster(data)
            if raster:
                answers.miss(
                    line, img["where"], f"an icon drawn from {raster}, {_short(src)}"
                )


def _raster(data):
    head = bytes(data[:64])
    for magic, name in RASTER:
        if head.startswith(magic):
            return f"a {name} file"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "a WebP file"
    if head[4:8] == b"ftyp" and head[8:12] in (b"avif", b"avis"):
        return "an AVIF file"
    text = bytes(data[:1024]).decode("utf8", "replace").lstrip("﻿ \t\r\n")
    if text.startswith(("<svg", "<?xml", "<!DOCTYPE svg", "<!--")) and "<svg" in text:
        return None
    return "a file of no format read here"


def _banner(answers, line, read, faces, *, declared, undeclared):
    if "cookie-banner" not in declared:
        why = (
            "the declaration names the cookie-banner with no selector"
            if "cookie-banner" in undeclared
            else "no parts declaration names the cookie-banner"
        )
        answers.unjudged(line, "page", why)
        return
    answers.met(line)
    names = [t for t in line.value if "." not in t]
    hosts = [t for t in line.value if "." in t]
    site = urllib.parse.urlsplit(read["url"]).hostname or ""
    why = []
    for c in read["cookies"]:
        domain = c["domain"].lstrip(".")
        if any(c["name"].startswith(n) for n in names):
            why.append(f"cookie {c['name']}")
        elif not (site.endswith(domain) or domain.endswith(site)):
            why.append(f"cookie {c['name']} for {domain}, another site")
    why += [
        f"storage key {k}"
        for k in read["stores"] or ()
        if any(k.startswith(n) for n in names)
    ]
    scripts = read["scripts"] + [
        _text(d) for kind, d in read["bodies"].values() if kind == "script"
    ]
    for h in hosts:
        if any(h in urllib.parse.urlsplit(u).netloc for u in read["requested"]):
            why.append(f"a request to {h}")
        elif any(h in s for s in scripts):
            why.append(f"a script naming {h}")
    if why and not read["banner"]:
        answers.miss(
            line,
            "page",
            f"needs consent ({'; '.join(why)}), and no cookie-banner shows",
        )
    elif why:
        return
    elif blind := [
        f"{kind} {_short(url)}" for url, kind, _ in read["unread"] if kind == "script"
    ] + (["the page's storage"] if read["stores"] is None else []):
        answers.unjudged(
            line,
            "page",
            f"{', '.join(blind)} could not be read, so consent is not ruled out",
        )
    elif read["banner"]:
        answers.miss(
            line,
            "page",
            "a cookie-banner shows, and the page sets only strictly necessary storage",
        )


def _cookies_page(answers, line, read, faces):
    answers.met(line)
    if read["footer"] is None:
        answers.miss(line, "page", "no footer, so no footer link to a cookies page")
    elif not any(
        line.value.search(text) or line.value.search(href)
        for text, href in read["footer"]
    ):
        answers.miss(line, "footer", f"no footer link matches {line.value.pattern}")


# guess, #313
def _quote(text):
    return repr(text if len(text) <= 40 else text[:39] + "…")


def _short(src):
    return src if not src.startswith("data:") else src[:40] + "…"


def files_report(url, found, read):
    lines = [f"check-load --files: {url}"]
    for src, kind, why in read["unread"]:
        lines.append(f"  {kind} not read: {_short(src)}: {why}")
    for src, font in read["fonts"].items():
        if not isinstance(font, fontfile.Font):
            lines.append(f"  font not read: {_short(src)}: {font}")
    for f in found:
        lines.append(f"{f['id']}: {f['answer']}")
        for m in f["misses"]:
            lines.append(f"  - [{m['check']}] {m['where']}: {m['what']}")
        for m in f["unjudged"]:
            lines.append(f"  ? [{m['check']}] {m['where']}: {m['what']}")
    return "\n".join(lines)


def files_main(at):
    when, json_path = answers_file.start(at.out, "files.json")
    server, url = serve(at.url)

    def run():
        with runner.chromium() as browser:
            return read_files(browser, url, declared=at.declared, timeout=at.timeout)

    try:
        read, code = runner.run_browser(run, at.timeout, url=at.url)
    finally:
        if server:
            server.shutdown()
    if code:
        return code
    found = findings(at.lines, read, declared=at.declared, undeclared=at.undeclared)
    answers_file.write(
        json_path,
        at.url,
        when,
        answers={f["id"]: f["answer"] for f in found},
        findings=found,
        fonts={
            _short(src): font._replace(
                chars=len(font.chars), features=sorted(font.features)
            )._asdict()
            if isinstance(font, fontfile.Font)
            else {"error": font}
            for src, font in read["fonts"].items()
        },
    )
    print(files_report(at.url, found, read))
    return 1 if any(f["misses"] for f in found) else 0


def main(argv):
    at = parse(argv)
    if at.files:
        return files_main(at)
    server, url = serve(at.url)

    def run():
        with runner.chromium() as browser:
            return [one_run(browser, url, at.timeout) for _ in range(at.runs)]

    try:
        runs, code = runner.run_browser(run, at.timeout, url=at.url)
    finally:
        if server:
            server.shutdown()
    if code:
        return code
    print(f"check-load: {at.url}")
    if any(r is None for r in runs):
        print(
            f"the page drew no LCP element in {sum(r is None for r in runs)} of {len(runs)} run(s): no text or image showed"
        )
        return 6
    median = statistics.median(r["ms"] for r in runs)
    print(
        f"LCP on Lighthouse's throttled phone: {median:.0f} ms, the median of {len(runs)} run(s); limit {at.limit} ms"
    )
    for r in runs:
        print(f"  {r['ms']:.0f} ms, {r['element']}")
    if median > at.limit:
        print(f"over by {median - at.limit:.0f} ms")
        return 1
    return 0


if __name__ == "__main__":
    run_main(main)
