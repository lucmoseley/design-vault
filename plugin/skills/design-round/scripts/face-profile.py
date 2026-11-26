#!/usr/bin/env python3
"""USAGE
  python3 face-profile.py <url or file> --out DIR [--widths W,W,…] [--wait SEL]
        [--timeout MS]

It loads the page at check-layout.py's phone and desktop widths (--widths
names others), the phone with a touch screen, and lets its fonts load and its
animations finish as check-layout.py does. Each element drawing text of its
own is put under a setting: its font family, weight, style, stretch, size,
font-size-adjust, font-variation-settings and font-optical-sizing. A setting
is read once, through a ruler element given those properties and no
letter-spacing, word-spacing or text-transform:

  x-height  the ex unit over the font size, so font-size-adjust counts
  width     a pangram's width over its characters and the font size: the
            average character, spaces included, as check-measure.py counts
            characters
  weight    the computed font-weight, and the stem: the thickness of an
            upright stroke, a lowercase l's middle row of ink, over the size,
            drawn at 200 px with the optical size pinned to the text's own
  axes      which of wght, wdth, opsz and GRAD the font varies on: present
            where pushing the axis past both ends of any range moves the
            pangram's width or the stem
  opsz      with an opsz axis, the value in use (font-optical-sizing: auto
            sets it to the used size in px; an opsz in
            font-variation-settings overrides it) and the range the font
            clamps it to, read off a ladder of values by where the width
            stops moving; null where opsz moves the ink alone

Each setting also gives the faces DevTools says drew its first element's
text (`rendered`, a fallback face showing where a web font failed) and its
characters by role: heading (h1–h6, role=heading), code (code, kbd, samp,
pre), control (button, input, select, textarea, label) and body, the rest.
The body setting is the one holding the most body characters at a width; a
setting under its size is small text.

DIR/face-profile.json holds every width's settings; an earlier run's is
deleted first, so a failed run leaves none. A family script reads a page it has loaded and settled with
profile(page).

EXITS 0 the profile is written / 2 the arguments are wrong / 3 Playwright or its
browser is missing / 4 the page did not render in time / 5 the browser refused
the page / 6 the page draws no text at any width / 7 a call hung that would never
return. Exits 0 and 6 print on stdout; the rest on stderr.
"""

import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402

layout = siblings.load(HERE, "check-layout.py")
flow = layout.flow

AXES = ("wght", "wdth", "opsz", "GRAD")
BEYOND = {  # guess, #501
    "wght": (1, 1000),
    "wdth": (1, 1000),
    "opsz": (0.1, 1000),
    "GRAD": (-1000, 1000),
}
LADDER = (  # guess, #501
    1,
    5,
    6,
    8,
    10,
    12,
    14,
    16,
    18,
    20,
    24,
    28,
    32,
    40,
    48,
    60,
    72,
    96,
    120,
    144,
    200,
    288,
    1000,
)
STEM_PX = 200  # guess, #501
WIDTH_PX = 1000  # measured 1% rounding at 100 px, #501
MOVED_PX = 0.5  # guess, #501
AT_END_PX = MOVED_PX / 10  # guess, #501
INKED = 0.5  # guess, #501
PANGRAM = "the quick brown fox jumps over the lazy dog"
ROLES = ("body", "heading", "code", "control")

TEXT_JS = r"""
() => {
  const SETTING = ['font-family', 'font-weight', 'font-style', 'font-stretch', 'font-size',
    'font-size-adjust', 'font-variation-settings', 'font-optical-sizing'];
  const out = [];
  let mark = 0;
  for (const el of document.body.querySelectorAll('*')) {
    if (el.closest('script, style, noscript, template, svg, math')) continue;
    let chars = 0;
    for (const n of el.childNodes) if (n.nodeType === 3) chars += n.data.replace(/\s+/g, '').length;
    const field = el.matches('input:not([type=hidden]), textarea') ? (el.value || el.placeholder || '').replace(/\s+/g, '').length : 0;
    if (!chars && !field) continue;
    if (!el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) continue;
    const r = el.getBoundingClientRect();
    if (r.width <= 1 && r.height <= 1) continue;
    const cs = getComputedStyle(el);
    const role = el.closest('h1, h2, h3, h4, h5, h6, [role=heading]') ? 'heading'
      : el.closest('code, kbd, samp, pre') ? 'code'
      : el.closest('button, input, select, textarea, label, [role=button]') ? 'control' : 'body';
    el.setAttribute('data-face-profile', String(mark));
    out.push({ mark: mark++, role, chars: chars + field,
      setting: Object.fromEntries(SETTING.map((p) => [p, cs.getPropertyValue(p)])) });
  }
  return out;
}
"""

RULER_JS = r"""
() => {
  const base = 'position:absolute;left:0;top:0;margin:0;padding:0;border:0;letter-spacing:normal;' +
    'word-spacing:normal;text-transform:none;line-height:normal;white-space:pre;';
  const box = document.createElement('div');
  const line = document.createElement('span');
  box.style.cssText = base + 'visibility:hidden;height:0;width:1000ex';
  line.style.cssText = base + 'visibility:hidden';
  document.body.append(box, line);
  const apply = (el, setting, extra) => {
    for (const [p, v] of Object.entries(setting)) el.style.setProperty(p, v);
    for (const [p, v] of Object.entries(extra || {})) el.style.setProperty(p, v);
  };
  window.__faceRuler = (setting, extra) => {
    apply(box, setting, extra);
    apply(line, setting, extra);
    line.textContent = __PANGRAM__;
    return { ex: box.getBoundingClientRect().width / 1000, line: line.getBoundingClientRect().width };
  };
  window.__faceShow = (setting, extra) => {
    let shot = document.getElementById('__face-shot');
    if (!shot) {
      shot = document.createElement('div');
      shot.id = '__face-shot';
      document.body.append(shot);
    }
    shot.style.cssText = base + 'position:fixed;z-index:2147483647;background:#fff;color:#000;' +
      'text-shadow:none;-webkit-text-stroke:0;filter:none;transform:none;opacity:1;padding:8px 40px'; // guess, #501
    apply(shot, setting, extra);
    shot.textContent = 'l';
    const r = shot.getBoundingClientRect();
    return { x: r.left, y: r.top, width: r.width, height: r.height };
  };
  window.__faceDone = () => {
    box.remove();
    line.remove();
    document.getElementById('__face-shot')?.remove();
  };
}
""".replace("__PANGRAM__", json.dumps(PANGRAM))


def variations(setting):
    held = {}
    text = setting.get("font-variation-settings", "normal").strip()
    if text != "normal":
        for part in text.split(","):
            tag, _, value = part.strip().partition(" ")
            held[tag.strip("\"'")] = float(value)
    return held


def variation(setting, **axes):
    held = {**variations(setting), **axes}
    return ", ".join(f'"{tag}" {value:g}' for tag, value in held.items()) or "normal"


def stem_of(png):
    import numpy as np
    from PIL import Image

    ink = 1 - np.asarray(Image.open(io.BytesIO(png)).convert("L"), dtype=float) / 255
    rows = np.flatnonzero(ink.max(axis=1) > INKED)
    if not len(rows):
        return 0.0
    return float(ink[(rows[0] + rows[-1]) // 2].sum())


class Ruler:
    def __init__(self, page):
        self.page = page

    def line(self, setting, **extra):
        return self.page.evaluate(
            "([s, e]) => window.__faceRuler(s, e)", [setting, extra]
        )

    def stem(self, setting, **extra):
        box = self.page.evaluate(
            "([s, e]) => window.__faceShow(s, e)",
            [setting, {"font-size": f"{STEM_PX}px", **extra}],
        )
        return stem_of(self.page.screenshot(clip=box, animations="disabled"))

    def width_at(self, setting, axes):
        return self.line(
            setting,
            **{
                "font-size": f"{WIDTH_PX}px",
                "font-variation-settings": variation(setting, **axes),
            },
        )["line"]

    def stem_at(self, setting, axes):
        return self.stem(
            setting, **{"font-variation-settings": variation(setting, **axes)}
        )

    def axes(self, setting):
        found = {}
        for tag in AXES:
            low, high = ({tag: v} for v in BEYOND[tag])
            moved_width = (
                abs(self.width_at(setting, low) - self.width_at(setting, high))
                > MOVED_PX
            )
            moved_ink = (
                abs(self.stem_at(setting, low) - self.stem_at(setting, high)) > MOVED_PX
            )
            found[tag] = moved_width or moved_ink
        return found

    def opsz_range(self, setting):
        widths = [self.width_at(setting, {"opsz": v}) for v in LADDER]
        low, high = widths[0], widths[-1]
        if abs(low - high) <= MOVED_PX:
            return None
        lo = max(
            v for v, w in zip(LADDER, widths, strict=True) if abs(w - low) <= AT_END_PX
        )
        hi = min(
            v for v, w in zip(LADDER, widths, strict=True) if abs(w - high) <= AT_END_PX
        )
        return [lo, hi]


def rendered(page, mark):
    devtools = page.context.new_cdp_session(page)
    try:
        devtools.send("DOM.enable")
        devtools.send("CSS.enable")
        root = devtools.send("DOM.getDocument", {"depth": 0})["root"]["nodeId"]
        node = devtools.send(
            "DOM.querySelector",
            {"nodeId": root, "selector": f'[data-face-profile="{mark}"]'},
        )["nodeId"]
        fonts = devtools.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]
        return [f["familyName"] for f in fonts]
    finally:
        devtools.detach()


def profile(page):
    texts = page.evaluate(TEXT_JS)
    groups = {}
    for t in texts:
        key = json.dumps(t["setting"], sort_keys=True)
        g = groups.setdefault(
            key,
            {"setting": t["setting"], "marks": [], "roles": dict.fromkeys(ROLES, 0)},
        )
        g["marks"].append(t["mark"])
        g["roles"][t["role"]] += t["chars"]
    page.evaluate(RULER_JS)
    ruler = Ruler(page)
    by_font = {}
    out = []
    try:
        for g in groups.values():
            s = g["setting"]
            size = float(s["font-size"].removesuffix("px"))
            font = json.dumps(
                {
                    k: s[k]
                    for k in (
                        "font-family",
                        "font-weight",
                        "font-style",
                        "font-stretch",
                    )
                }
            )
            if font not in by_font:
                axes = ruler.axes(s)
                by_font[font] = (axes, ruler.opsz_range(s) if axes["opsz"] else None)
            axes, span = by_font[font]
            opsz = variations(s).get("opsz")
            if opsz is None and axes["opsz"] and s["font-optical-sizing"] == "auto":
                opsz = size
            in_use = None
            if axes["opsz"] and opsz is not None:
                in_use = min(max(opsz, span[0]), span[1]) if span else opsz
            pin = {"font-optical-sizing": "none"}
            if in_use is not None:
                pin["font-variation-settings"] = variation(s, opsz=in_use)
            line = ruler.line(s)
            pangram = ruler.line(s, **{"font-size": f"{WIDTH_PX}px", **pin})["line"]
            out.append(
                {
                    "family": s["font-family"],
                    "rendered": rendered(page, g["marks"][0]),
                    "size": size,
                    "weight": float(s["font-weight"]),
                    "style": s["font-style"],
                    "stretch": s["font-stretch"],
                    "variation": s["font-variation-settings"],
                    "optical_sizing": s["font-optical-sizing"],
                    "size_adjust": s["font-size-adjust"],
                    "xheight": round(line["ex"] / size, 4),
                    "width": round(pangram / len(PANGRAM) / WIDTH_PX, 4),
                    "stem": round(ruler.stem(s, **pin) / STEM_PX, 4),
                    "axes": [tag for tag in AXES if axes[tag]],
                    "opsz": {"in_use": in_use, "range": span} if axes["opsz"] else None,
                    "roles": g["roles"],
                    "characters": sum(g["roles"].values()),
                    "elements": len(g["marks"]),
                }
            )
    finally:
        page.evaluate(
            "() => { window.__faceDone?.(); document.querySelectorAll('[data-face-profile]').forEach((e) => e.removeAttribute('data-face-profile')); }"
        )
    out.sort(key=lambda f: (-f["roles"]["body"], -f["characters"]))
    if out and out[0]["roles"]["body"]:
        body = out[0]["size"]
        for f in out:
            f["small"] = f["size"] < body
        out[0]["body"] = True
    return out


def describe(f):
    role = "body setting" if f.get("body") else max(ROLES, key=lambda r: f["roles"][r])
    if f.get("small"):
        role += ", small"
    axes = " ".join(f["axes"]) or "none"
    opsz = ""
    if f["opsz"]:
        span = f["opsz"]["range"]
        opsz = (
            f"  opsz {f['opsz']['in_use']:g}"
            if f["opsz"]["in_use"] is not None
            else "  opsz unset"
        )
        opsz += f" of {span[0]:g}–{span[1]:g}" if span else " (range unread)"
    used = ", ".join(f["rendered"]) or "unknown"
    return (
        f"  {role}: {f['size']:g}px {f['weight']:g} {f['style']} in {used} ({f['family']})\n"
        f"    x-height {f['xheight']:.3f}  width {f['width']:.3f}  stem {f['stem']:.3f}  axes {axes}{opsz}"
        f"  — {f['characters']} characters in {f['elements']} element(s)"
    )


def parse(argv):
    p = argparse.ArgumentParser(
        prog="face-profile.py",
        description="Read the x-height, width, weight and optical size of each typeface setting a page draws text in.",
    )
    p.add_argument("url", help="an http(s) URL, or a local HTML file")
    p.add_argument("--out", required=True, metavar="DIR")
    p.add_argument(
        "--widths",
        metavar="W,W,…",
        help=f"the viewport widths in px; {layout.PHONE_WIDTH} and {layout.DESKTOP_WIDTH} by default",
    )
    p.add_argument("--wait", metavar="SELECTOR")
    p.add_argument("--timeout", type=int, default=flow.PLAY_TIMEOUT_MS, metavar="MS")
    at = p.parse_args(argv)
    if at.widths:
        try:
            at.widths = sorted({int(w) for w in at.widths.split(",")})
        except ValueError:
            p.error(f"--widths wants whole px, e.g. 390,1440 — got {at.widths!r}")
        if not all(layout.LOW <= w <= layout.HIGH for w in at.widths):
            p.error(f"--widths wants widths from {layout.LOW} to {layout.HIGH}")
    else:
        at.widths = [layout.PHONE_WIDTH, layout.DESKTOP_WIDTH]
    at.url = flow.page_url(p, at.url)
    return at


def run(at):
    found = {}
    with flow.chromium() as browser:
        for w in at.widths:
            context = browser.new_context(
                viewport={"width": w, "height": layout.height_at(w, layout.HEIGHTS)},
                **layout.device(w),
            )
            context.set_default_timeout(at.timeout)
            page = context.new_page()
            page.goto(at.url, wait_until="load", timeout=at.timeout)
            if at.wait:
                page.wait_for_selector(at.wait, timeout=at.timeout)
            page.evaluate(layout.SETTLE_JS)
            found[w] = profile(page)
            context.close()
    return found


def main(argv):
    at = parse(argv)
    path = os.path.join(at.out, "face-profile.json")
    if os.path.exists(path):
        os.remove(path)
    found, code = flow.run_browser(lambda: run(at), at.timeout, at.url)
    if code:
        return code
    os.makedirs(at.out, exist_ok=True)
    with open(path, "w", encoding="utf8") as fh:
        json.dump(
            {"url": at.url, "widths": {str(w): faces for w, faces in found.items()}},
            fh,
            indent=2,
        )
    lines = [f"face-profile: {at.url}"]
    for w, faces in found.items():
        lines.append(
            f"{w}px: {len(faces)} setting(s)" if faces else f"{w}px: no text drawn"
        )
        lines += [describe(f) for f in faces]
    lines.append(f"written: {path}")
    print("\n".join(lines))
    return 0 if any(found.values()) else 6


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
