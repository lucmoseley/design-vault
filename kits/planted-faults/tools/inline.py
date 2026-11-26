#!/usr/bin/env python3
"""python3 kits/planted-faults/tools/inline.py <in.html> <out.html> <origin> <assets dir> — makes a snapshot stand alone: stylesheets inlined, fonts and images saved beside it."""

import hashlib
import os
import sys
import re
import mimetypes
import urllib.request
import urllib.parse

src, out, origin = sys.argv[1:4]
cache = {}


def fetch(u):
    if u not in cache:
        with urllib.request.urlopen(u) as r:
            cache[u] = (r.read(), r.headers.get_content_type())
    return cache[u]


ASSETS = sys.argv[4]


def data_uri(u):
    body, ct = fetch(u)
    name = os.path.basename(urllib.parse.urlparse(u).path) or "asset"
    if "." not in name:
        name += mimetypes.guess_extension(ct or "") or ""
    name = hashlib.sha1(u.encode()).hexdigest()[:8] + "-" + name
    os.makedirs(ASSETS, exist_ok=True)
    open(os.path.join(ASSETS, name), "wb").write(body)
    return f"../{os.path.basename(ASSETS.rstrip('/'))}/{name}"


html = open(src).read()
html = re.sub(r'<base href="[^"]*">', "", html)


def css_inline(m):
    href = urllib.parse.urljoin(origin, m.group(1))
    css = fetch(href)[0].decode()
    css = re.sub(
        r'url\((["\']?)([^)"\']+)\1\)',
        lambda k: (
            k.group(0)
            if k.group(2).startswith("data:")
            else f'url("{data_uri(urllib.parse.urljoin(href, k.group(2)))}")'
        ),
        css,
    )
    return f"<style>{css}</style>"


html = re.sub(r'<link rel="stylesheet" href="([^"]+)"[^>]*>', css_inline, html)
html = re.sub(r'<link rel="preload"[^>]*>', "", html)
html = re.sub(r'<link rel="(?:icon|apple-touch-icon)"[^>]*>', "", html)
html = re.sub(
    r'(<img[^>]*?\ssrc=")([^"]+)(")',
    lambda m: (
        m.group(1)
        + (
            m.group(2)
            if m.group(2).startswith("data:")
            else data_uri(urllib.parse.urljoin(origin, m.group(2)))
        )
        + m.group(3)
    ),
    html,
)
html = re.sub(r'\s(?:srcset|imageSrcSet)="[^"]*"', "", html)
open(out, "w").write(html)
