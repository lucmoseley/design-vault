"""drive-pointer.py — hovers, presses, clicks, drags and wheel-scrolls a page with the mouse, for the check
scripts that read a page in a state only a pointer reaches (design-vault#301): a hover-only tooltip, a held
button, where a dragged element comes to rest, a layer that moves with the scroll. A library the check
scripts load; it judges nothing itself.

Its only I/O is the Playwright page it is handed, which the caller opens and closes. A check loads it by
path, as the others load check-flow.py:

    spec = importlib.util.spec_from_file_location("drive_pointer", os.path.join(HERE, "drive-pointer.py"))
    pointer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pointer)

and drives a Playwright page it has loaded:

    pointer.hover(page, "#info")            # the tooltip is up here: read the page
    pointer.leave(page, "#info")
    pointer.press(page, "#buy")             # held down: read its pressed style, whether it acted yet
    pointer.release(page)
    pointer.drag(page, "#knob", (130, 0))   # let go and settled: read where it came to rest
    pointer.wheel(page, "#gallery", dx=200)

A `target` is a CSS selector or an ElementHandle. The pointer goes to the point `at` within its box, as
fractions of its width and height (the centre by default), taken once its box has held still for STILL_FRAMES
frames with no animation of it waiting to start, and scrolled into view first where that point is off the screen. A
target still moving at SETTLE_CAP_MS, as one animated forever, is pointed at where it stands then, and its Pointer reads `settled` False. A target the page lacks, one with no box, or one
another element covers at that point is refused with PointerError, its `cover` naming what lies over the
target: the move would drive the cover, so there is no state of the target's to read.

Each call returns a Pointer once the page has settled: no change to the markup, no scroll anywhere, and no
finite animation running, for QUIET_MS; a page still changing at SETTLE_CAP_MS is read as it stands, with
`settled` False. A page given WATCH_JS before its own scripts ends that wait once it has queued nothing that
could change it inside QUIET_MS. An animation driven by the scroll, or one that repeats forever, never holds
that wait. Its siblings settle on other signals: drive-form.py on markup and requests in flight, drive-overlay.py on one
overlay's box; a pointer moves things none of those see, a scroll and a transition on any element.
"""

import collections
import time

# The quiet a settle waits for, in ms. Radix UI's Tooltip shows 700 ms after the pointer arrives by default
# (its delayDuration, radix-ui.com, read 16 Oct 2026), the longest default found, so a shorter window reads
# such a tooltip as never shown; the 100 ms past it is a working margin.
QUIET_MS = 800
# A page still changing after this long is read as it stands: a working figure, several quiet windows. It
# also bounds the wait for a target to hold still (#458), so one call may wait up to twice this.
SETTLE_CAP_MS = 5000
# The frames a target's box must hold to read still: Playwright's "stable" takes two
# (playwright.dev/docs/actionability); Chromium can pass a frame without advancing an animation that has just
# started, which read a moving target still in 2 of 300 runs at two and 0 of 250 at three (#532).
STILL_FRAMES = 3
# One frame at 60 Hz, the pace drag() moves at.
FRAME_MS = 16
# How long a drag takes by default: a working figure for a deliberate drag, not a flick.
DRAG_MS = 300
CENTRE = (0.5, 0.5)

# Where the pointer rests, in px from the viewport's top left, and whether each target held still and the page
# settled after the move.
Pointer = collections.namedtuple("Pointer", "x y settled")


class PointerError(Exception):
    """The pointer cannot reach the target. `target` is the selector or handle at fault; `cover` describes
    the element over it, None where it is not covered."""

    def __init__(self, message, target=None, cover=None):
        super().__init__(message)
        self.target = target
        self.cover = cover


DESCRIBE_JS = r"""
const describe = (el) => el.localName + (el.id ? `#${el.id}` : "") +
  (el.classList.length ? `.${[...el.classList].join(".")}` : "");
"""

# The viewport point at fractions [fx, fy] of the element's box, scrolled into view where it is off the
# screen, and the element drawn there where that is not the target or inside it.
POINT_JS = (
    "async ([el, fx, fy, scroll, cap, frames]) => {"
    + DESCRIBE_JS
    + r"""
  const place = () => {
    const r = el.getBoundingClientRect();
    return { r, x: r.left + fx * (r.width - 1), y: r.top + fy * (r.height - 1) };
  };
  const seen = ({ x, y }) => x >= 0 && y >= 0 && x < innerWidth && y < innerHeight;
  // The same box over `frames` animation frames (#458), the first read in a frame too, with no timed animation
  // of the target or an ancestor waiting to start: one holds its first keyframe until it does (#532). A
  // scroll-driven one on a timeline that cannot scroll waits for ever, and is left out.
  const frame = () => new Promise((done) => requestAnimationFrame(() => done()));
  const box = () => { const r = el.getBoundingClientRect(); return [r.x, r.y, r.width, r.height].join(); };
  const starting = () => document.getAnimations().some((a) =>
    a.pending && a.timeline instanceof DocumentTimeline && a.effect?.target?.contains(el));
  const still = () => held >= frames - 1 && !starting();
  const start = performance.now();
  await frame();
  let held = 0, current = box();
  while (!still() && performance.now() - start < cap) {
    await frame();
    const next = box();
    held = next === current ? held + 1 : 0;
    current = next;
  }
  let at = place();
  if (!at.r.width || !at.r.height) return { error: `${describe(el)} has no box` };
  if (!seen(at) && scroll) {
    el.scrollIntoView({ block: "center", inline: "center", behavior: "instant" });
    at = place();
  }
  if (!seen(at)) return { error: `${describe(el)} is off the screen at (${Math.round(at.x)}, ${Math.round(at.y)})` };
  // Asked of the target's own root, so a target in a shadow tree is not taken to be covered by its host.
  const hit = el.getRootNode().elementFromPoint(at.x, at.y);
  return { x: at.x, y: at.y, still: still(), cover: hit && hit !== el && !el.contains(hit) ? describe(hit) : null };
}"""
)

# The viewport's corner pixel farthest from the element's centre.
AWAY_JS = r"""(el) => {
  const r = el.getBoundingClientRect();
  const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
  const right = innerWidth - 1, bottom = innerHeight - 1;
  const corners = [[0, 0], [right, 0], [0, bottom], [right, bottom]];
  return corners.sort(([ax, ay], [bx, by]) => Math.hypot(bx - cx, by - cy) - Math.hypot(ax - cx, ay - cy))[0];
}"""

# The least quiet a settle waits where WATCH_JS shows nothing queued: a working figure, six frames at 60 Hz, for
# the work the watch cannot see to show itself (its Residual below) before the wait ends on it.
QUIET_LEAST_MS = 100

# Run before a page's own scripts (an init script), it lets settle() end once the page has queued nothing that
# could change it before the quiet window closes: a timer or a scheduler task due inside the window, an
# animation-frame or idle callback, a fetch whose body is unread, a request, an image or a font still loading. A
# page change comes only from a task, so the rest of the window would see none; it is Angular's "stable", no
# macrotask pending (angular.dev/api/core/Testability) (#462). A timer due after the window closes, as a half-hour
# session limit, holds nothing, as the full window would not have seen it either. Unwatched, a settle waits the
# whole window. Residual: a WebSocket, worker or posted message, a dynamic import(), an inserted script or style
# sheet and a CSS background image are not seen, and are waited for by QUIET_LEAST_MS alone.
WATCH_JS = r"""(() => {
  if (window.__dpQueued) return;
  const due = new Map(), frames = new Set(), idles = new Set();
  let loads = 0;
  const [st, si, clear] = [setTimeout, setInterval, clearTimeout];
  const [raf, caf] = [requestAnimationFrame, cancelAnimationFrame];
  const at = (ms) => performance.now() + (Number(ms) || 0);
  // A string is run as the browser runs one, in the global scope.
  const callable = (fn) => (typeof fn === "function" ? fn : () => (0, eval)(String(fn)));
  window.setTimeout = function (fn, ms, ...rest) {
    const run = callable(fn);
    const id = st.call(window, (...a) => { due.delete(id); run.apply(window, a); }, ms, ...rest);
    due.set(id, at(ms));
    return id;
  };
  window.setInterval = function (fn, ms, ...rest) {
    const run = callable(fn);
    const id = si.call(window, (...a) => { due.set(id, at(ms)); run.apply(window, a); }, ms, ...rest);
    due.set(id, at(ms));
    return id;
  };
  // The two clears are one in browsers, each clearing either kind.
  window.clearTimeout = window.clearInterval = (id) => { due.delete(id); clear.call(window, id); };
  window.requestAnimationFrame = (fn) => {
    const id = raf.call(window, (t) => { frames.delete(id); fn(t); });
    frames.add(id);
    return id;
  };
  window.cancelAnimationFrame = (id) => { frames.delete(id); caf.call(window, id); };
  if (window.requestIdleCallback) {
    const [ric, cic] = [requestIdleCallback, cancelIdleCallback];
    window.requestIdleCallback = (fn, opts) => {
      const id = ric.call(window, (d) => { idles.delete(id); fn(d); }, opts);
      idles.add(id);
      return id;
    };
    window.cancelIdleCallback = (id) => { idles.delete(id); cic.call(window, id); };
  }
  // Held from the call until the promise settles; a scheduler task's delay is part of its wait.
  const held = (p) => {
    loads++;
    const done = () => { loads--; };
    p.then(done, done);
    return p;
  };
  if (window.scheduler?.postTask) {
    const post = scheduler.postTask.bind(scheduler);
    scheduler.postTask = (...args) => held(post(...args));
  }
  // A response is held until its body is read, as what the page draws from it comes after.
  const bodied = new WeakSet();
  for (const read of ["arrayBuffer", "blob", "bytes", "formData", "json", "text"]) {
    const own = Response.prototype[read];
    if (!own) continue;
    Response.prototype[read] = function (...args) {
      const got = own.apply(this, args);
      if (bodied.has(this)) {
        bodied.delete(this);
        const done = () => { loads--; };
        got.then(done, done);
      }
      return got;
    };
  }
  const go = fetch;
  window.fetch = function (...args) {
    loads++;
    const p = go.apply(this, args);
    p.then((r) => { bodied.add(r); }, () => { loads--; });
    return p;
  };
  const send = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.send = function (...args) {
    loads++;
    this.addEventListener("loadend", () => { loads--; }, { once: true });
    try {
      return send.apply(this, args);
    } catch (e) {
      loads--;
      throw e;
    }
  };
  const loading = () => document.fonts.status === "loading" || [...document.images].some((i) => !i.complete);
  window.__dpQueued = (until) => frames.size > 0 || idles.size > 0 || loads > 0 || loading() ||
    [...due.values()].some((t) => t <= until);
})();"""

# True once nothing has changed for `quiet` ms, or for `least` ms with WATCH_JS showing nothing queued that could
# fire before `quiet` ms; false at `cap` ms with the page still changing.
SETTLE_JS = r"""async ([quiet, cap, least]) => {
  const frame = () => new Promise((done) => requestAnimationFrame(() => done()));
  const start = performance.now();
  let since = start;
  const touch = () => { since = performance.now(); };
  const watch = new MutationObserver(touch);
  watch.observe(document, { subtree: true, childList: true, attributes: true, characterData: true });
  addEventListener("scroll", touch, true);
  // A scroll-driven animation's end time is a percentage, not a number, so the finite test leaves it out.
  const moving = () => document.getAnimations().some((a) => a.playState === "running" &&
    Number.isFinite(a.effect?.getComputedTiming().endTime));
  try {
    while (performance.now() - start < cap) {
      await frame();
      if (moving()) touch();
      else if (performance.now() - since >= quiet) return true;
      else if (window.__dpQueued && performance.now() - since >= least && !window.__dpQueued(since + quiet)) {
        return true;
      }
    }
    return false;
  } finally {
    watch.disconnect();
    removeEventListener("scroll", touch, true);
  }
}"""


def settle(page):
    """Whether the page went QUIET_MS without a change before SETTLE_CAP_MS, or QUIET_LEAST_MS with WATCH_JS
    showing nothing queued that could change it inside QUIET_MS. A navigation mid-wait is
    followed: the new document is waited for once it has loaded, inside the same cap."""
    from playwright.sync_api import Error as PlaywrightError

    deadline = time.monotonic() + SETTLE_CAP_MS / 1000
    while (left := (deadline - time.monotonic()) * 1000) > 0:
        try:
            return page.evaluate(SETTLE_JS, [QUIET_MS, left, QUIET_LEAST_MS])
        except PlaywrightError as exc:
            if "context was destroyed" not in str(exc):
                raise
            page.wait_for_load_state("load", timeout=left)
    return False


def _element(page, target):
    if not isinstance(target, str):
        return target
    found = page.query_selector(target)
    if found is None:
        raise PointerError(f"no element matches {target}", target)
    return found


def _point(page, target, at, *, scroll=True, cover_ok=False):
    """The viewport point `at` within `target`, as (x, y)."""
    fx, fy = at
    if not (0 <= fx <= 1 and 0 <= fy <= 1):
        raise ValueError(f"at is two fractions of the box from 0 to 1, not {at!r}")
    found = page.evaluate(
        POINT_JS, [_element(page, target), fx, fy, scroll, SETTLE_CAP_MS, STILL_FRAMES]
    )
    if "error" in found:
        raise PointerError(found["error"], target)
    if found["cover"] and not cover_ok:
        raise PointerError(
            f"{target if isinstance(target, str) else 'the target'} is covered at "
            f"({round(found['x'])}, {round(found['y'])}) by {found['cover']}",
            target,
            found["cover"],
        )
    page._drive_pointer_still = (
        getattr(page, "_drive_pointer_still", True) and found["still"]
    )
    return found["x"], found["y"]


def _move(page, x, y):
    page.mouse.move(x, y)
    # Playwright does not say where its mouse is, so the page carries it; release() needs it.
    page._drive_pointer_at = (x, y)


def _resting(page):
    """The Pointer where the mouse is, once the page has settled."""
    x, y = getattr(page, "_drive_pointer_at", (0, 0))
    still = page.__dict__.pop("_drive_pointer_still", True)
    return Pointer(x, y, settle(page) and still)


def hover(page, target, at=CENTRE):
    """Rest the pointer on `target`."""
    _move(page, *_point(page, target, at))
    return _resting(page)


def leave(page, target):
    """Move the pointer to the corner of the screen farthest from `target`."""
    _move(page, *page.evaluate(AWAY_JS, _element(page, target)))
    return _resting(page)


def press(page, target, at=CENTRE, button="left"):
    """Press `button` down on `target` and hold it there; release() lets go."""
    _move(page, *_point(page, target, at))
    page.mouse.down(button=button)
    return _resting(page)


def release(page, button="left"):
    """Let go of `button` wherever the pointer is."""
    page.mouse.up(button=button)
    return _resting(page)


def click(page, target, at=CENTRE, button="left"):
    """Press and let go on `target`, settling only after both."""
    _move(page, *_point(page, target, at))
    page.mouse.down(button=button)
    page.mouse.up(button=button)
    return _resting(page)


def drag(page, source, to, at=CENTRE, *, duration_ms=DRAG_MS, hold=False):
    """Press on `source`, move to `to` over `duration_ms`, one move a frame, and let go unless `hold`. `to`
    is an element, whose centre is reached, or an (x, y) offset in px."""
    x0, y0 = _point(page, source, at)
    if isinstance(to, tuple):
        x1, y1 = x0 + to[0], y0 + to[1]
    else:
        # A drop zone is often covered by its own label or what was dropped before, and scrolling to it
        # now would move `source` from under the point just found.
        x1, y1 = _point(page, to, CENTRE, scroll=False, cover_ok=True)
    _move(page, x0, y0)
    page.mouse.down()
    steps = max(1, round(duration_ms / FRAME_MS))
    for i in range(1, steps + 1):
        page.wait_for_timeout(FRAME_MS)
        _move(page, x0 + (x1 - x0) * i / steps, y0 + (y1 - y0) * i / steps)
    if not hold:
        page.mouse.up()
    return _resting(page)


def wheel(page, target=None, *, dx=0, dy=0, at=CENTRE):
    """Turn the wheel by `dx` and `dy` px with the pointer over `target`, or with None over the middle of the
    screen, so the page scrolls from where it stands rather than from wherever `target` was scrolled to."""
    if not dx and not dy:
        raise ValueError("wheel needs a dx or a dy")
    if target is None:
        size = page.evaluate("() => [innerWidth, innerHeight]")
        _move(page, size[0] / 2, size[1] / 2)
    else:
        _move(page, *_point(page, target, at))
    page.mouse.wheel(dx, dy)
    return _resting(page)
