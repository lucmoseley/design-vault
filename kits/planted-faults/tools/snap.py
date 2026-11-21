#!/usr/bin/env python3
"""snap.py — fixture capture for the #224 critic-shape test.
snap.py save  <url> <out.html> <base>   static, script-free DOM snapshot with <base href>
snap.py shots <url-or-file> <outdir>    desktop 1440x900 slices (900 px) and phone 390x844 slices (1688 px)
"""

import sys
import re
import pathlib
from playwright.sync_api import sync_playwright
from PIL import Image


def url_of(x):
    p = pathlib.Path(x)
    return p.resolve().as_uri() if p.exists() else x


def save(url, out, base):
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_timeout(1500)
        html = pg.content()
        b.close()
    html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(
        r"<link[^>]+rel=\"(?:preload|modulepreload)\"[^>]*as=\"script\"[^>]*/?>",
        "",
        html,
    )
    html = html.replace("<head>", f'<head><base href="{base}">', 1)
    pathlib.Path(out).write_text(html)


def shots(src, outdir):
    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for name, vw, vh, tile in (
            ("desktop", 1440, 900, 900),
            ("phone", 390, 844, 1688),
        ):
            pg = b.new_page(viewport={"width": vw, "height": vh})
            pg.goto(url_of(src), wait_until="networkidle")
            pg.wait_for_timeout(5000)
            full = out / f"_{name}-full.png"
            pg.screenshot(path=str(full), full_page=True)
            pg.close()
            im = Image.open(full)
            h = im.height
            n = 0
            for top in range(0, h, tile):
                n += 1
                im.crop((0, top, im.width, min(h, top + tile))).save(
                    out / f"{name}-{n:02d}.png"
                )
            full.unlink()
            print(name, im.width, "x", h, "->", n, "slices")
        b.close()


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "save":
        save(*sys.argv[2:5])
    elif cmd == "shots":
        shots(*sys.argv[2:4])
