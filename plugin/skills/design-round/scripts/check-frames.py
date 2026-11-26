#!/usr/bin/env python3
"""Proves a motion candidate's frames, two ways.

USAGE
  python3 check-frames.py last <url or file> --at SELECTOR --asset SVG [--asset SVG]
        --out DIR [--background CSS] [--margin PX] [--wait SEL] [--timeout MS]
        [--viewport WxH]
  python3 check-frames.py hash <url or file> --out DIR [--times MS,MS,…]
        [--scale N] [--save FILE | --check FILE] [--wait SEL] [--timeout MS]
        [--viewport WxH]

`last`: the last frame of a build is the asset's own end frame. At device scale
1 and then 2, it finishes every animation, as the build ends for a visitor, so
the page's own end handlers run, and screenshots the asset's region. It then
covers the page with the bare asset files drawn in one layer at the same
transform, on --background, and screenshots that. Any pixel difference fails.
--at names the one element whose user space is the asset files' own
coordinates: an SVG element (its getScreenCTM() is the transform), or an HTML
box the first asset's viewBox is stretched to fill. Each --asset is drawn in
that space, the mark first and then any wordmark; a wordmark file must share
the mark's coordinates. The background defaults to the first opaque background
colour behind --at; pass --background for a gradient or an image ground. A
hand-over a timer starts after the build ends is not waited for: the frame
checked is the one before it. The page's web fonts reach a wordmark set as
text. It writes DIR/last-<n>x.png, DIR/asset-<n>x.png and DIR/diff-<n>x.png,
each difference in red.

`hash`: renders each key frame from a fresh load, then seeks one more load
backwards through them all, and fails a frame whose two renders differ. Key
frames default to every keyframe's time, every animation's start and end, and
time zero; --times names them in ms, `end` for the last. --save FILE stores
each frame's SHA-256; --check FILE renders the frames FILE names, at its
viewport and scale, and fails each whose hash changed. It writes
DIR/frame-<ms>.png. A hash is of the PNG Chromium encodes, so a frame can
change with the browser; --check names a browser change.

Both modes read the Web Animations API animations the page has made once it has
loaded, its fonts are ready, --wait has matched and no new one has started for
QUIET_MS: `element.animate()`, CSS animations and CSS transitions. Time zero is
the earliest animation's start. They refuse a page whose animations never end,
run off a scroll timeline or play in reverse, or that keeps starting them for
SETTLE_CAP_MS. `hash` also refuses one that starts animations after that
point, or when one finishes; `last` finishes those too, and refuses a page that
keeps starting them. `hash` renders every frame on the timeline its first load
timed, and --save keeps that timeline for --check, which names any start its
own load put more than STAGE_JITTER_MS away. Both refuse,
naming it, a page holding what that list does not: a visible canvas, video or
embedded document, SMIL or shadow DOM, moving or not; a script rewriting an
element or a path's d frame by frame; or an animation a script paused, which
a seek would move. One such part refuses the whole page, its listed animations
included. An animation CSS animation-play-state holds paused is seeked as it
plays from when it is first seen, so one a script seeks by hand through CSS, a
custom property in its animation-delay, is drawn as if playing.

EXITS 0 every frame matches / 1 a frame differs (each printed) / 2 the arguments
are wrong / 3 Playwright or its browser is missing / 4 the page did not render
in time / 5 the browser refused the page / 6 the page cannot be checked / 7 a
call hung that would never return. Exits 0, 1 and 6 are results and print on
stdout; the rest print on stderr.
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402

flow = siblings.load(HERE, "check-flow.py")
runner = siblings.load(HERE, "runner.py")
UnmeasurableError = runner.UnmeasurableError

NAME_JS = (
    flow.LABEL_JS
    + r"""
const name = (a) => a.effect && a.effect.target ? label(a.effect.target, a.effect.pseudoElement) : 'an animation with no target';
"""
)
FINISH_ROUNDS = 20  # guess, #501
QUIET_MS = 500  # guess, #240
SETTLE_CAP_MS = 5000  # guess, #240
STAGE_JITTER_MS = 50  # guess over a measured 17 ms quiet and 150 ms loaded jitter, #259

PREPARE_JS = (
    r"""
async ({ quiet, cap, shown, timeline }) => {
  """
    + NAME_JS
    + flow.CSS_PAUSED_JS
    + r"""
  await document.fonts.ready;
  // pause() nulls an animation's startTime: https://www.w3.org/TR/web-animations-1/#pausing-an-animation-section
  const starts = new Map();
  const began = performance.now();
  let lastNew = began;
  let latest = [];
  let quietNow = false;
  const held = [];
  for (;;) {
    const fresh = document.getAnimations().filter((a) => !starts.has(a));
    // A cancelled pending animation rejects its ready promise: https://www.w3.org/TR/web-animations-1/#canceling-an-animation-section
    await Promise.all(fresh.map((a) => a.ready.catch(() => null)));
    const now = document.timeline.currentTime;
    for (const a of fresh) {
      if (a.playState === 'paused' && !cssPaused(a)) held.push(a);
      starts.set(a, a.startTime !== null ? a.startTime : now - a.currentTime / a.playbackRate);
      a.pause();
    }
    const at = performance.now();
    if (fresh.length) [lastNew, latest] = [at, fresh];
    quietNow = at - lastNew >= quiet;
    if (quietNow || at - began >= cap) break;
    await new Promise((next) => requestAnimationFrame(next));
  }
  const reasons = [];
  const names = (as) => [...new Set(as.map(name))].sort().slice(0, shown).join(', ');
  if (!quietNow) reasons.push('is still starting animations ' + cap + ' ms after it loaded and its fonts were ready (' + names(latest) + '), so its frames have no fixed timeline; start its motion once and let it end');
  if (held.length) reasons.push('holds ' + held.length + ' animation(s) a script paused (' + names(held) + '), which a seek would move as if playing');
  const anims = [...starts.keys()];
  const rows = [];
  for (const a of anims) {
    const who = ' (' + name(a) + ')';
    const t = a.effect ? a.effect.getComputedTiming() : null;
    if (a.timeline !== document.timeline) reasons.push('drives an animation by scroll position, not time' + who);
    else if (a.playbackRate <= 0) reasons.push('plays an animation in reverse' + who);
    else if (t && t.endTime === Infinity) reasons.push('runs an animation that never ends' + who);
    else rows.push({ a, t, rate: a.playbackRate, start: starts.get(a) });
  }
  const t0 = rows.reduce((m, r) => Math.min(m, r.start), rows.length ? Infinity : 0);
  // #619
  const listed = new Map(document.getAnimations().map((a, i) => [a, i]));
  const unlisted = new Map(anims.map((a, i) => [a, listed.size + i]));
  const place = (r) => (listed.has(r.a) ? listed.get(r.a) : unlisted.get(r.a));
  rows.sort((p, q) => place(p) - place(q));
  if (timeline && !reasons.length) {
    const keyed = (names) => { const seen = {}; return names.map((n) => n + ' ' + (seen[n] = (seen[n] || 0) + 1)); };
    const was = new Map(keyed(timeline.map((s) => s.name)).map((k, i) => [k, timeline[i].ms]));
    const own = keyed(rows.map((r) => name(r.a)));
    const extra = own.find((k) => !was.has(k));
    const lost = [...was.keys()].find((k) => !own.includes(k));
    const bare = (k) => k.replace(/ \d+$/, '');
    if (extra || lost) reasons.push('makes different animations from one load to the next (' + (extra ? bare(extra) + ', which an earlier load did not make' : 'no ' + bare(lost) + ', which an earlier load made') + '), so its frames have no fixed timeline');
    else rows.forEach((r, i) => { r.start = t0 + was.get(own[i]); });
  }
  let end = 0;
  const keys = [0];
  for (const r of rows) {
    const off = r.start - t0;
    if (!r.t) continue;
    end = Math.max(end, off + r.t.endTime / r.rate);
    keys.push(off + r.t.delay / r.rate, off + (r.t.delay + r.t.activeDuration) / r.rate);
    if (r.t.easing === 'linear' && r.t.duration > 0) {
      for (const k of r.a.effect.getKeyframes()) keys.push(off + (r.t.delay + r.t.duration * k.computedOffset) / r.rate);
    }
  }
  window.__frames = { anims: new Set(anims), rows, t0 };
  return { reasons, end, keys, timeline: rows.map((r) => ({ name: name(r.a), ms: r.start - t0 })) };
}
"""
)

SCRIPTED_JS = (
    r"""
({ frames, span, shown }) => {
  """
    + flow.LABEL_JS
    + flow.LOOP_JS
    + flow.DRAWN_JS
    + r"""
  const f = window.__flow;
  f.scan();
  f.stopped = true;
  return drawn(f, { frames, span, shown, morphs: true });
}
"""
)

CHAIN_JS = (
    r"""
async (quiet) => {
  """
    + NAME_JS
    + r"""
  const f = window.__frames;
  // A finished animation with no fill leaves getAnimations(): https://www.w3.org/TR/web-animations-1/#relevant-animations-section
  const watch = async () => {
    const found = new Set();
    const began = performance.now();
    for (;;) {
      for (const a of document.getAnimations()) if (!f.anims.has(a)) found.add(a);
      if (performance.now() - began >= quiet) break;
      await new Promise((next) => requestAnimationFrame(next));
    }
    return [...found].map(name);
  };
  const late = await watch();
  if (late.length) return { late, chained: [] };
  for (const r of f.rows) r.a.finish();
  return { late, chained: await watch() };
}
"""
)

SEEK_JS = (
    r"""
async (t) => {
  """
    + NAME_JS
    + r"""
  const f = window.__frames;
  for (const r of f.rows) r.a.currentTime = (t + f.t0 - r.start) * r.rate;
  await new Promise((done) => requestAnimationFrame(() => requestAnimationFrame(done)));
  return document.getAnimations().filter((a) => !f.anims.has(a))
    .map(name);
}
"""
)

FINISH_JS = (
    r"""
async (rounds) => {
  """
    + NAME_JS
    + r"""
  const done = new Set();
  for (let round = 0; round < rounds; round++) {
    const todo = document.getAnimations().filter((a) => !done.has(a));
    if (!todo.length) break;
    for (const a of todo) { done.add(a); a.finish(); }
    await new Promise((next) => requestAnimationFrame(() => requestAnimationFrame(next)));
  }
  const late = document.getAnimations().filter((a) => !done.has(a)).map(name);
  const held = document.getAnimations().filter((a) => a.effect && a.effect.getComputedTiming().progress !== null).map(name);
  return { late, held };
}
"""
)

REGION_JS = r"""
({ sel, boxes, margin }) => {
  const els = document.querySelectorAll(sel);
  if (els.length !== 1) return { error: '--at ' + sel + ' matches ' + els.length + ' elements, not one' };
  const el = els[0];
  let m, origin;
  if (el instanceof SVGGraphicsElement) {
    let root = el;
    while (root.ownerSVGElement) root = root.ownerSVGElement;
    const r = root.getBoundingClientRect();
    const cs = getComputedStyle(root);
    origin = [r.left + parseFloat(cs.borderLeftWidth) + parseFloat(cs.paddingLeft),
      r.top + parseFloat(cs.borderTopWidth) + parseFloat(cs.paddingTop)];
    m = DOMMatrix.fromMatrix(el.getScreenCTM());
  } else {
    const r = el.getBoundingClientRect();
    const [x, y, w, h] = boxes[0];
    origin = [r.left, r.top];
    m = new DOMMatrix([r.width / w, 0, 0, r.height / h, r.left - x * r.width / w, r.top - y * r.height / h]);
  }
  const pts = boxes.flatMap(([x, y, w, h]) => [[x, y], [x + w, y], [x, y + h], [x + w, y + h]])
    .map(([x, y]) => m.transformPoint(new DOMPoint(x, y)));
  const left = Math.max(0, Math.floor(Math.min(...pts.map((p) => p.x)) - margin));
  const top = Math.max(0, Math.floor(Math.min(...pts.map((p) => p.y)) - margin));
  const right = Math.min(innerWidth, Math.ceil(Math.max(...pts.map((p) => p.x)) + margin));
  const bottom = Math.min(innerHeight, Math.ceil(Math.max(...pts.map((p) => p.y)) + margin));
  if (right <= left || bottom <= top) return { error: 'the asset at ' + sel + ' lies outside the viewport' };
  let background = 'white';
  for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
    const c = getComputedStyle(n).backgroundColor;
    if (!/^(transparent|rgba\(.*,\s*0\))$/.test(c)) { background = c; break; }
  }
  return { matrix: [m.a, m.b, m.c, m.d, m.e - origin[0], m.f - origin[1]], origin,
    clip: { x: left + scrollX, y: top + scrollY, width: right - left, height: bottom - top }, background };
}
"""

OVERLAY_JS = r"""
({ assets, matrix, origin, background }) => {
  const NS = 'http://www.w3.org/2000/svg';
  const host = document.createElement('div');
  host.style.cssText = 'all: initial; position: fixed; inset: 0; z-index: 2147483647;';
  const root = host.attachShadow({ mode: 'open' });
  const ground = document.createElement('div');
  ground.style.cssText = 'position: absolute; inset: 0;';
  ground.style.background = background;
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('width', 1);
  svg.setAttribute('height', 1);
  svg.style.cssText = 'position: absolute; overflow: visible; left: ' + origin[0] + 'px; top: ' + origin[1] + 'px;';
  const layer = document.createElementNS(NS, 'g');
  layer.setAttribute('transform', 'matrix(' + matrix.join(' ') + ')');
  const OWN = new Set(['xmlns', 'viewBox', 'width', 'height', 'x', 'y', 'preserveAspectRatio', 'version']);
  for (const text of assets) {
    const doc = new DOMParser().parseFromString(text, 'image/svg+xml').documentElement;
    const g = document.createElementNS(NS, 'g');
    for (const at of doc.attributes) if (!OWN.has(at.name) && !at.name.startsWith('xmlns:')) g.setAttribute(at.name, at.value);
    for (const n of [...doc.childNodes]) g.appendChild(document.importNode(n, true));
    layer.appendChild(g);
  }
  svg.appendChild(layer);
  root.append(ground, svg);
  document.documentElement.appendChild(host);
  return new Promise((done) => requestAnimationFrame(() => requestAnimationFrame(done)));
}
"""

COMPARE_JS = r"""
async ({ a, b }) => {
  const load = async (s) => {
    const bytes = Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
    const bmp = await createImageBitmap(new Blob([bytes], { type: 'image/png' }),
      { colorSpaceConversion: 'none', premultiplyAlpha: 'none' });
    const ctx = new OffscreenCanvas(bmp.width, bmp.height).getContext('2d');
    ctx.drawImage(bmp, 0, 0);
    return ctx.getImageData(0, 0, bmp.width, bmp.height);
  };
  const [A, B] = await Promise.all([load(a), load(b)]);
  if (A.width !== B.width || A.height !== B.height) return { size: [A.width, A.height, B.width, B.height] };
  const out = new ImageData(A.width, A.height);
  let count = 0, max = 0, at = null;
  for (let i = 0; i < A.data.length; i += 4) {
    let d = 0;
    for (let c = 0; c < 4; c++) d = Math.max(d, Math.abs(A.data[i + c] - B.data[i + c]));
    if (d > 0) {
      count++;
      if (d > max) { max = d; at = [(i / 4) % A.width, Math.floor(i / 4 / A.width)]; }
      out.data.set([255, 0, 0, 255], i);
    } else {
      const grey = 255 - (255 - (A.data[i] + A.data[i + 1] + A.data[i + 2]) / 3) / 4;
      out.data.set([grey, grey, grey, 255], i);
    }
  }
  const canvas = new OffscreenCanvas(A.width, A.height);
  canvas.getContext('2d').putImageData(out, 0, 0);
  const png = new Uint8Array(await (await canvas.convertToBlob({ type: 'image/png' })).arrayBuffer());
  let bin = '';
  // guess, #501
  const CHUNK = 0x8000;
  for (let i = 0; i < png.length; i += CHUNK) bin += String.fromCharCode(...png.subarray(i, i + CHUNK));
  return { count, max, at, diff: btoa(bin) };
}
"""


def viewbox(text, name):
    try:
        ET.fromstring(text)
    except ET.ParseError as exc:
        raise ValueError(f"{name} is not well-formed XML: {exc}") from exc
    m = re.search(r"<svg\b[^>]*?\bviewBox\s*=\s*[\"']([^\"']+)[\"']", text)
    if not m:
        raise ValueError(f"{name} has no viewBox on its <svg>")
    box = [float(n) for n in re.split(r"[\s,]+", m.group(1).strip())]
    if len(box) != 4 or box[2] <= 0 or box[3] <= 0:
        raise ValueError(
            f"{name} has a viewBox that is not four numbers with a positive size"
        )
    return box


def key_times(prep, asked):
    if asked:
        times = [prep["end"] if t == "end" else t for t in asked]
    else:
        times = prep["keys"] + [prep["end"]]
    out = []
    for t in sorted(max(0.0, min(t, prep["end"])) for t in times):
        if not out or t - out[-1] >= 1:
            out.append(round(t, 3))
    return out


def ms(t):
    return f"{t:.0f}" if t == int(t) else f"{t:.3f}".rstrip("0")


def compare(blank, a, b):
    return blank.evaluate(
        COMPARE_JS,
        {"a": base64.b64encode(a).decode(), "b": base64.b64encode(b).decode()},
    )


def open_page(browser, at, scale, *, device=None, timeline=None):
    context = browser.new_context(
        viewport=at.viewport_size, device_scale_factor=scale, **(device or {})
    )
    context.set_default_timeout(at.timeout)
    context.add_init_script(flow.COLLECTOR_JS)
    page = context.new_page()
    page.goto(at.url, wait_until="load")
    if at.wait:
        page.wait_for_selector(at.wait)
    prep = page.evaluate(
        PREPARE_JS,
        {
            "quiet": QUIET_MS,
            "cap": SETTLE_CAP_MS,
            "shown": flow.NAMES_SHOWN,
            "timeline": timeline,
        },
    )
    reasons = prep["reasons"] + page.evaluate(
        SCRIPTED_JS,
        {
            "frames": flow.REWRITE_FRAMES,
            "span": flow.REWRITE_SPAN_MS,
            "shown": flow.NAMES_SHOWN,
        },
    )
    if reasons:
        context.close()
        raise UnmeasurableError(sorted(set(reasons)))
    return context, page, prep


def keyed(timeline):
    seen, out = {}, {}
    for s in timeline:
        seen[s["name"]] = seen.get(s["name"], 0) + 1
        out[(s["name"], seen[s["name"]])] = s["ms"]
    return out


def read_timeline(browser, at, scale, device=None):
    context, page, prep = open_page(browser, at, scale, device=device)
    try:
        refuse_chain(page)
    finally:
        context.close()
    return prep


def refuse_chain(page):
    found = page.evaluate(CHAIN_JS, QUIET_MS)
    if found["late"]:
        raise late_error(found["late"])
    if found["chained"]:
        raise UnmeasurableError(
            [
                f"starts animations when others finish ({listed(found['chained'])}), "
                "so a seek draws its build only to where the first link ends; start every link "
                "when the page loads, held back by its delay"
            ]
        )


def listed(found):
    return ", ".join(sorted(set(found))[: flow.NAMES_SHOWN])


def late_error(found):
    return UnmeasurableError(
        [
            f"starts animations after its frames were read ({listed(found)}), "
            "so a seek cannot fix its frames; make them when the page loads, or pass --wait"
        ]
    )


def still_note(end):
    if end > 0:
        return []
    return [
        f"no animation started in the {QUIET_MS} ms after the page loaded, so it is read as still; "
        "if its motion starts later, pass --wait for the element that marks the start"
    ]


def seek(page, t):
    late = page.evaluate(SEEK_JS, t)
    if late:
        raise late_error(late)


def seek_shots(page, times):
    shots = []
    for t in times:
        seek(page, t)
        shots.append((t, page.screenshot()))
    refuse_chain(page)
    return shots


def check_last(browser, blank, at, assets):
    boxes = [viewbox(text, name) for name, text in assets]
    results = []
    for scale in (1, 2):
        context, page, prep = open_page(browser, at, scale)
        end = page.evaluate(FINISH_JS, FINISH_ROUNDS)
        if end["late"]:
            raise UnmeasurableError(
                [
                    f"keeps starting animations as its build ends ({listed(end['late'])}), "
                    "so it has no last frame"
                ]
            )
        region = page.evaluate(
            REGION_JS, {"sel": at.at, "boxes": boxes, "margin": at.margin}
        )
        if "error" in region:
            raise UnmeasurableError([region["error"]])
        background = at.background or region["background"]
        last = page.screenshot(clip=region["clip"])
        page.evaluate(
            OVERLAY_JS,
            {
                "assets": [text for _, text in assets],
                "matrix": region["matrix"],
                "origin": region["origin"],
                "background": background,
            },
        )
        bare = page.screenshot(clip=region["clip"])
        context.close()
        d = compare(blank, last, bare)
        for name, data in ((f"last-{scale}x.png", last), (f"asset-{scale}x.png", bare)):
            with open(os.path.join(at.out, name), "wb") as fh:
                fh.write(data)
        if d.get("diff"):
            with open(os.path.join(at.out, f"diff-{scale}x.png"), "wb") as fh:
                fh.write(base64.b64decode(d["diff"]))
        results.append(
            {
                "scale": scale,
                "end": prep["end"],
                "clip": region["clip"],
                "background": background,
                "held": sorted(set(end["held"])),
                **d,
            }
        )
    return results


def render(browser, at, t, timeline):
    context, page, _ = open_page(browser, at, at.scale, timeline=timeline)
    try:
        seek(page, t)
        return page.screenshot()
    finally:
        context.close()


def args_with(at, **fields):
    return argparse.Namespace(**{**vars(at), **fields})


def check_hash(browser, blank, at):
    stored = at.stored
    if stored:
        at = args_with(at, viewport_size=stored["viewport"], scale=stored["scale"])
    prep = read_timeline(browser, at, at.scale)
    timeline, timed_by, note = prep["timeline"], "one load", None
    saved_timeline = (stored or {}).get("timeline")
    if stored and saved_timeline is None:
        note = "the file saves no timeline, so this load timed them"
    elif saved_timeline is not None:
        was, now = keyed(saved_timeline), keyed(timeline)
        if was.keys() != now.keys():
            note = "the page makes different animations from the ones the file saved, so this load timed them"
        else:
            timeline, timed_by = saved_timeline, "the saved run"
            moved = [
                f"{k[0]} {ms(round(was[k], 3))} ms then, {ms(round(now[k], 3))} ms now"
                for k in sorted(was)
                if abs(was[k] - now[k]) > STAGE_JITTER_MS
            ]
            if moved:
                note = (
                    f"this load started animations away from the file's moments ({', '.join(moved[: flow.NAMES_SHOWN])}); "
                    "every frame is drawn at the file's, so a start the page moved shows only here"
                )
    times = [f["ms"] for f in stored["frames"]] if stored else key_times(prep, at.times)
    first = {t: render(browser, at, t, timeline) for t in times}
    for t in times:
        with open(os.path.join(at.out, f"frame-{ms(t)}.png"), "wb") as fh:
            fh.write(first[t])
    context, page, _ = open_page(browser, at, at.scale, timeline=timeline)
    second = {}
    for t in reversed(times):
        seek(page, t)
        second[t] = page.screenshot()
    context.close()
    unstable = []
    for t in times:
        if first[t] != second[t]:
            unstable.append(
                {
                    "ms": t,
                    **{
                        k: v
                        for k, v in compare(blank, first[t], second[t]).items()
                        if k != "diff"
                    },
                }
            )
    hashes = [{"ms": t, "sha256": hashlib.sha256(first[t]).hexdigest()} for t in times]
    changed = []
    if stored:
        was = {f["ms"]: f["sha256"] for f in stored["frames"]}
        changed = [h["ms"] for h in hashes if h["sha256"] != was[h["ms"]]]
    record = {
        "page": at.url,
        "viewport": at.viewport_size,
        "scale": at.scale,
        "browser": browser.version,
        "end_ms": prep["end"],
        "timeline": timeline,
        "frames": hashes,
    }
    if at.save:
        with open(at.save, "w", encoding="utf8") as fh:
            json.dump(record, fh, indent=1)
            fh.write("\n")
    return {
        "record": record,
        "stored": stored,
        "unstable": unstable,
        "changed": changed,
        "timed_by": timed_by,
        "note": note,
    }


def pixels(d):
    if "size" in d:
        return f"the two renders differ in size ({d['size'][0]}x{d['size'][1]} against {d['size'][2]}x{d['size'][3]})"
    return f"{d['count']:,} pixels differ, by up to {d['max']} levels"


def report_last(at, assets, results):
    names = " + ".join(os.path.basename(n) for n, _ in assets)
    clip = results[0]["clip"]
    lines = [
        f"check-frames last: {at.url}",
        f"the last frame, at {ms(results[0]['end'])} ms, against the bare asset ({names}) "
        f"on {results[0]['background']}, region {clip['width']}x{clip['height']} px at ({clip['x']}, {clip['y']}):",
    ]
    for r in results:
        if r.get("count") == 0:
            lines.append(f"  {r['scale']}x: identical")
            continue
        where = ""
        if r.get("at"):
            where = f", the largest at ({r['clip']['x'] + r['at'][0] / r['scale']:g}, {r['clip']['y'] + r['at'][1] / r['scale']:g}) px"
        lines.append(
            f"  {r['scale']}x: {pixels(r)}{where}; see {os.path.join(at.out, f'diff-{r["scale"]}x.png')}"
        )
    held = results[0]["held"]
    if held and any(r.get("count") != 0 for r in results):
        lines.append(
            f"{len(held)} animation(s) still hold their end state ({', '.join(held[: flow.NAMES_SHOWN])}{', …' if len(held) > flow.NAMES_SHOWN else ''}). "
            "Chrome draws an element an animation still holds on a layer of its own, with different edges: "
            "where the shapes are right, cancel every animation as the build ends and set each end state in "
            "the element's own style (not by commitStyles(), which can commit a fade's start at its exact end)."
        )
    return "\n".join(lines)


def report_hash(at, result):
    record, stored, unstable, changed = (
        result[k] for k in ("record", "stored", "unstable", "changed")
    )
    lines = [
        f"check-frames hash: {at.url}",
        f"{len(record['frames'])} key frame(s) at {record['viewport']['width']}x{record['viewport']['height']}, "
        f"scale {record['scale']}: {', '.join(ms(f['ms']) for f in record['frames'])} ms",
        *still_note(record["end_ms"]),
    ]
    starts = sorted({s["ms"] for s in record["timeline"]})
    if len(starts) > 1:
        lines.append(
            f"its animations start at {len(starts)} moments, {', '.join(ms(round(s, 3)) for s in starts)} ms, "
            f"as {result['timed_by']} timed them; every render puts them there"
        )
    lines.append(
        f"rendered twice, fresh and then seeked backwards through one page: {'every frame the same' if not unstable else f'{len(unstable)} frame(s) differ'}"
    )
    for u in unstable:
        lines.append(f"  {ms(u['ms'])} ms: {pixels(u)}")
    if stored:
        lines.append(
            f"against {at.check}: {'every frame unchanged' if not changed else f'{len(changed)} frame(s) changed'}"
        )
        if result["note"]:
            lines.append(f"  {result['note']}")
        for t in changed:
            lines.append(
                f"  {ms(t)} ms: see {os.path.join(at.out, f'frame-{ms(t)}.png')}"
            )
        if changed and stored.get("browser") != record["browser"]:
            lines.append(
                f"  the browser changed too, {stored.get('browser')} then and {record['browser']} now, "
                "so a change can be the browser's"
            )
    if at.save:
        lines.append(f"hashes saved to {at.save}")
    return "\n".join(lines)


def parse(argv):
    p = argparse.ArgumentParser(
        prog="check-frames.py",
        description="Check a motion candidate's last frame, or hash its key frames.",
    )
    sub = p.add_subparsers(dest="mode", required=True)
    last = sub.add_parser(
        "last", help="fail a last frame that is not exactly the asset"
    )
    hashed = sub.add_parser(
        "hash", help="render key frames twice, and save or re-check their hashes"
    )
    for s in (last, hashed):
        s.add_argument("url", help="an http(s) URL, or a local HTML file")
        s.add_argument("--out", required=True, metavar="DIR", help="where the PNGs go")
        s.add_argument("--wait", metavar="SELECTOR")
        s.add_argument(
            "--timeout", type=int, default=runner.PLAY_TIMEOUT_MS, metavar="MS"
        )
        s.add_argument("--viewport", default=flow.DESKTOP, metavar="WxH")
    last.add_argument(
        "--at",
        required=True,
        metavar="SELECTOR",
        help="the element whose user space is the asset's coordinates",
    )
    last.add_argument(
        "--asset",
        required=True,
        action="append",
        metavar="SVG",
        help="an asset file; repeat for a wordmark",
    )
    last.add_argument(
        "--background", metavar="CSS", help="the ground under the bare asset"
    )
    last.add_argument(
        "--margin",
        type=float,
        default=2,
        metavar="PX",
        help="CSS px around the asset's box; the default is a guess",
    )
    hashed.add_argument(
        "--times", metavar="MS,MS,…", help="the key frames, in ms; `end` is the last"
    )
    hashed.add_argument(
        "--scale", type=float, default=1, metavar="N", help="device scale"
    )
    once = hashed.add_mutually_exclusive_group()
    once.add_argument("--save", metavar="FILE", help="store the hashes here")
    once.add_argument(
        "--check",
        metavar="FILE",
        help="fail a frame whose hash differs from this file's",
    )
    at = p.parse_args(argv)
    at.viewport_size = flow.size_arg(p, "--viewport", at.viewport)
    if at.mode == "hash":
        if at.check and at.times:
            p.error("--check renders the frames its file names; drop --times")
        at.stored = None
        if at.check:
            try:
                with open(at.check, encoding="utf8") as fh:
                    at.stored = json.load(fh)
                ok = (
                    isinstance(at.stored["viewport"]["width"], int)
                    and isinstance(at.stored["viewport"]["height"], int)
                    and isinstance(at.stored["scale"], (int, float))
                    and all(
                        isinstance(f["ms"], (int, float))
                        and isinstance(f["sha256"], str)
                        for f in at.stored["frames"]
                    )
                    # #259
                    and all(
                        isinstance(s["name"], str) and isinstance(s["ms"], (int, float))
                        for s in at.stored.get("timeline") or []
                    )
                )
            except (OSError, ValueError, KeyError, TypeError) as exc:
                p.error(f"--check {at.check} is not a file of saved hashes: {exc}")
            if not ok:
                p.error(f"--check {at.check} is not a file of saved hashes")
        at.times = [t.strip() for t in at.times.split(",")] if at.times else None
        try:
            at.times = at.times and [
                "end" if t == "end" else float(t) for t in at.times
            ]
        except ValueError:
            p.error("--times wants numbers of ms, or `end`")
    else:
        for path in at.asset:
            if not os.path.isfile(path):
                p.error(f"no such file: {path}")
    at.url = runner.page_url(p, at.url)
    return p, at


# #326 #346
HASH_ARGS = ["--disable-threaded-animation"]


def run(at, assets):
    with runner.chromium(HASH_ARGS if at.mode == "hash" else []) as browser:
        blank = browser.new_page()
        if at.mode == "last":
            return check_last(browser, blank, at, assets)
        return check_hash(browser, blank, at)


def main(argv):
    p, at = parse(argv)
    assets = []
    if at.mode == "last":
        for path in at.asset:
            with open(path, encoding="utf8") as fh:
                assets.append((path, fh.read()))
        try:
            for name, text in assets:
                viewbox(text, name)
        except ValueError as exc:
            p.error(str(exc))
    os.makedirs(at.out, exist_ok=True)
    result, code = runner.run_browser(
        lambda: run(at, assets),
        at.timeout,
        at.url,
        (
            f"cannot check {at.url}, because this page:",
            "Check its frames by eye.",
        ),
    )
    if code:
        return code
    if at.mode == "last":
        print(report_last(at, assets, result))
        return 1 if any(r.get("count") != 0 for r in result) else 0
    print(report_hash(at, result))
    return 1 if result["unstable"] or result["changed"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
