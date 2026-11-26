import collections
import time

# guess, #301
QUIET_MS = 800
# guess, #301
SETTLE_CAP_MS = 5000
# measured 0 of 250 runs read a moving target still at three frames, #532
STILL_FRAMES = 3
FRAME_MS = 1000 // 60
# guess, #301
DRAG_MS = 300
CENTRE = (0.5, 0.5)

Pointer = collections.namedtuple("Pointer", "x y settled")


class PointerError(Exception):
    def __init__(self, message, target=None, cover=None):
        super().__init__(message)
        self.target = target
        self.cover = cover


DESCRIBE_JS = r"""
const describe = (el) => el.localName + (el.id ? `#${el.id}` : "") +
  (el.classList.length ? `.${[...el.classList].join(".")}` : "");
"""

POINT_JS = (
    "async ([el, fx, fy, scroll, cap, frames]) => {"
    + DESCRIBE_JS
    + r"""
  const place = () => {
    const r = el.getBoundingClientRect();
    return { r, x: r.left + fx * (r.width - 1), y: r.top + fy * (r.height - 1) };
  };
  const seen = ({ x, y }) => x >= 0 && y >= 0 && x < innerWidth && y < innerHeight;
  // #458, #532
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
  // Document.elementFromPoint retargets a hit inside a shadow tree to its host:
  // https://drafts.csswg.org/cssom-view/#dom-document-elementfrompoint
  const hit = el.getRootNode().elementFromPoint(at.x, at.y);
  return { x: at.x, y: at.y, still: still(), cover: hit && hit !== el && !el.contains(hit) ? describe(hit) : null };
}"""
)

AWAY_JS = r"""(el) => {
  const r = el.getBoundingClientRect();
  const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
  const right = innerWidth - 1, bottom = innerHeight - 1;
  const corners = [[0, 0], [right, 0], [0, bottom], [right, bottom]];
  return corners.sort(([ax, ay], [bx, by]) => Math.hypot(bx - cx, by - cy) - Math.hypot(ax - cx, ay - cy))[0];
}"""

# guess, #462
QUIET_LEAST_MS = 100

WATCH_JS = r"""(() => {
  if (window.__dpQueued) return;
  const due = new Map(), frames = new Set(), idles = new Set();
  let loads = 0;
  const [st, si, clear] = [setTimeout, setInterval, clearTimeout];
  const [raf, caf] = [requestAnimationFrame, cancelAnimationFrame];
  const at = (ms) => performance.now() + (Number(ms) || 0);
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
  // clearTimeout and clearInterval clear the same map of timers, either kind:
  // https://html.spec.whatwg.org/multipage/timers-and-user-prompts.html#dom-cleartimeout
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

SETTLE_JS = r"""async ([quiet, cap, least]) => {
  const frame = () => new Promise((done) => requestAnimationFrame(() => done()));
  const start = performance.now();
  let since = start;
  const touch = () => { since = performance.now(); };
  const watch = new MutationObserver(touch);
  watch.observe(document, { subtree: true, childList: true, attributes: true, characterData: true });
  addEventListener("scroll", touch, true);
  // A scroll-driven animation's times are percentages, not numbers:
  // https://drafts.csswg.org/scroll-animations-1/
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
    # Playwright does not say where its mouse is: https://playwright.dev/python/docs/api/class-mouse
    page._drive_pointer_at = (x, y)


def _resting(page):
    x, y = getattr(page, "_drive_pointer_at", (0, 0))
    still = page.__dict__.pop("_drive_pointer_still", True)
    return Pointer(x, y, settle(page) and still)


def hover(page, target, at=CENTRE):
    _move(page, *_point(page, target, at))
    return _resting(page)


def leave(page, target):
    _move(page, *page.evaluate(AWAY_JS, _element(page, target)))
    return _resting(page)


def press(page, target, at=CENTRE, button="left"):
    _move(page, *_point(page, target, at))
    page.mouse.down(button=button)
    return _resting(page)


def release(page, button="left"):
    page.mouse.up(button=button)
    return _resting(page)


def click(page, target, at=CENTRE, button="left"):
    _move(page, *_point(page, target, at))
    page.mouse.down(button=button)
    page.mouse.up(button=button)
    return _resting(page)


def drag(page, source, to, at=CENTRE, *, duration_ms=DRAG_MS, hold=False):
    x0, y0 = _point(page, source, at)
    if isinstance(to, tuple):
        x1, y1 = x0 + to[0], y0 + to[1]
    else:
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
    if not dx and not dy:
        raise ValueError("wheel needs a dx or a dy")
    if target is None:
        size = page.evaluate("() => [innerWidth, innerHeight]")
        _move(page, size[0] / 2, size[1] / 2)
    else:
        _move(page, *_point(page, target, at))
    page.mouse.wheel(dx, dy)
    return _resting(page)
