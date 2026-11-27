import contextlib
import itertools
import os
import pathlib
import re
import signal
import sys
import threading
import time
import traceback
import typing

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from fail_open import expected  # noqa: E402

PLAY_TIMEOUT_MS = 60000  # guess, #141
LOAD_TIMEOUT_MS = 30000  # measured: Playwright's own default, #141
RENDERER_GONE_S = 10  # guess, #432
UNTIMED_CALLS = frozenset({"Page.set_viewport_size", "CDPSession.send"})
UNANSWERED_S = 30  # guess above a measured 72 ms worst resize, #459
WATCH_POLL_S = 0.25  # guess, #432
KILLED_GONE_S = 10  # guess, #464

REQUIREMENTS = pathlib.Path(__file__).resolve().parents[3] / "requirements.txt"
PIP_INSTALL = f"python3 -m pip install --only-binary :all: -r {REQUIREMENTS}"
INSTALL_HINT = (
    "Playwright is a Python package installed once per machine, at the\n"
    "versions the plugin pins:\n"
    f"    {PIP_INSTALL}\n"
    "    python3 -m playwright install chromium"
)


def missing(err):
    script = os.path.basename(sys.argv[0])
    print(
        f"{script}: {err.name or err} is missing — {PIP_INSTALL}",
        file=sys.stderr,
    )
    return 3


def first_line(exc):
    for line in str(exc).splitlines():
        if line.strip():
            return line.strip()
    return exc.__class__.__name__


class PageTimeoutError(Exception):
    pass


class NoBrowserError(Exception):
    pass


class RefusedError(Exception):
    pass


class UnmeasurableError(Exception):
    pass


class HungCallError(Exception):
    pass


def page_url(p, url):
    if re.match(r"^[a-z]+://", url):
        return url
    path = pathlib.Path(url)
    if not path.is_file():
        p.error(f"no such file: {url}")
    return path.resolve().as_uri()


def descendants(pid):
    found, todo = [], [pid]
    while todo:
        parent = todo.pop()
        try:
            tasks = os.listdir(f"/proc/{parent}/task")
        except FileNotFoundError as exc:  # #432
            expected(exc, "no children")
            continue
        for task in tasks:
            try:
                with open(f"/proc/{parent}/task/{task}/children") as f:
                    kids = [int(k) for k in f.read().split()]
            except (FileNotFoundError, ProcessLookupError) as exc:  # #432
                expected(exc, "no children")
                continue
            found += kids
            todo += kids
    return found


def process_args(pid):
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            return f.read().decode(errors="replace").replace("\0", " ").split()
    except (FileNotFoundError, ProcessLookupError) as exc:  # #432
        expected(exc, "no command line")
        return []


def parent_pid(pid):
    try:
        with open(f"/proc/{pid}/stat") as f:
            # comm may hold spaces: https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html
            return int(f.read().rsplit(")", 1)[1].split()[1])
    except (FileNotFoundError, ProcessLookupError) as exc:  # #464
        expected(exc, "no parent")
        return None


def browser_pids(pids):
    found = [
        pid
        for pid in pids
        if "--remote-debugging-pipe" in (args := process_args(pid))
        and not any(a.startswith("--type=") for a in args)
    ]
    # #662
    return [pid for pid in found if parent_pid(pid) not in found]


def driver_pid(browser):
    parent = parent_pid(browser)
    if parent is None:
        return None
    return parent if "run-driver" in process_args(parent) else None


class WaitingCall(typing.NamedTuple):
    name: str
    where: str
    frame: object


def playwright_call(stack, package_dir):
    for (caller, line), (frame, _) in itertools.pairwise(stack):
        if frame.f_code.co_filename.startswith(package_dir):
            owner = frame.f_locals.get("self")
            name = frame.f_code.co_name
            if owner is not None:
                name = f"{type(owner).__name__}.{name}"
            return WaitingCall(
                name, f"{os.path.basename(caller.f_code.co_filename)}:{line}", frame
            )
    return None


def waiting_call(main, package_dir):
    stack = []
    frame = main.gr_frame
    while frame is not None:
        stack.append((frame, frame.f_lineno))
        frame = frame.f_back
    stack.reverse()
    return playwright_call(stack, package_dir)


def raising_call(exc, package_dir):
    return playwright_call(list(traceback.walk_tb(exc.__traceback__)), package_dir)


class CallWatch:
    def __init__(self, browser, main, package_dir):
        self.browser, self.driver = browser, driver_pid(browser)
        self.main, self.package_dir = main, package_dir
        self.fired = None
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _rendering(self):
        return any(
            "--type=renderer" in process_args(p) for p in descendants(self.browser)
        )

    def _hung(self, call, since, began, now):
        name, where = call.name, call.where
        if since is not None and now - since >= RENDERER_GONE_S:
            return (
                f"{name} at {where} waited {RENDERER_GONE_S} s with the browser "
                "running no renderer, so it would never have returned; an "
                "out-of-memory kill of the page's renderer causes this (#430), "
                "so run it again once memory is free"
            )
        if name in UNTIMED_CALLS and now - began >= UNANSWERED_S:
            return (
                f"{name} at {where} waited {UNANSWERED_S} s for a renderer that is "
                "alive but never answered, and Playwright gives it no timeout, so "
                "it would never have returned (#459, #464); run it again"
            )
        return None

    def _run(self):
        since = held = began = None
        while not self._stop.wait(WATCH_POLL_S):
            call = waiting_call(self.main, self.package_dir)
            if call is None:
                since = held = None
                continue
            now = time.monotonic()
            if held is None or call.frame is not held:
                held, began = call.frame, now
            if self._rendering():
                since = None
            else:
                since = now if since is None else since
            if why := self._hung(call, since, began, now):
                self.fired = why
                driver = [self.driver] if self.driver else []
                killed = [self.browser, *descendants(self.browser), *driver]
                for p in killed:
                    with contextlib.suppress(ProcessLookupError):
                        os.kill(p, signal.SIGKILL)
                # #464
                end = time.monotonic() + KILLED_GONE_S
                while any(map(process_args, killed)) and time.monotonic() < end:
                    time.sleep(WATCH_POLL_S)
                return

    def renderer_death(self, exc, page_open):
        call = raising_call(exc, self.package_dir)
        if call is None or self._rendering():
            return None
        if not page_open and not call.name.endswith(".new_page"):
            return None
        return (
            f"{call.name} at {call.where} raised {first_line(exc)!r} with the "
            "browser running no renderer; an out-of-memory kill of the page's "
            "renderer causes this (#430), so run it again once memory is free"
        )

    def stop(self):
        self._stop.set()
        self._thread.join()


@contextlib.contextmanager
def chromium(args=()):
    import greenlet
    import playwright
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import TimeoutError as PlaywrightTimeout
    from playwright.sync_api import sync_playwright

    with sync_playwright() as play:
        before = set(descendants(os.getpid()))
        try:
            browser = play.chromium.launch(args=list(args))
        except PlaywrightError as exc:
            raise NoBrowserError(first_line(exc)) from exc
        launched = browser_pids(set(descendants(os.getpid())) - before)
        watch = None
        if len(launched) == 1:
            watch = CallWatch(
                launched[0],
                greenlet.getcurrent(),
                os.path.dirname(playwright.__file__) + os.sep,
            )
        else:
            print(
                f"no call watch: /proc shows {len(launched)} new browser processes, "
                "not one, so a hung call can wait for ever (#432, #459)",
                file=sys.stderr,
            )
        try:
            yield browser
        except Exception as exc:
            if watch and watch.fired:
                raise HungCallError(watch.fired) from exc
            if (
                watch
                and isinstance(exc, PlaywrightError)
                and not isinstance(exc, PlaywrightTimeout)
                and (
                    why := watch.renderer_death(
                        exc, any(c.pages for c in browser.contexts)
                    )
                )
            ):
                raise HungCallError(why) from exc
            if isinstance(exc, PlaywrightTimeout):
                raise PageTimeoutError(first_line(exc)) from exc
            if isinstance(exc, PlaywrightError):
                raise RefusedError(first_line(exc)) from exc
            raise
        else:
            if watch and watch.fired:
                raise HungCallError(watch.fired)
        finally:
            if watch:
                watch.stop()
            # #464
            if not (watch and watch.fired):
                browser.close()


def run_browser(work, timeout, url=None, unmeasurable=None):
    try:
        return work(), None
    except ImportError:
        print(f"Playwright is not importable here.\n{INSTALL_HINT}", file=sys.stderr)
        return None, 3
    except NoBrowserError as exc:
        print(
            f"Playwright is installed but its browser is not: {exc}\n{INSTALL_HINT}",
            file=sys.stderr,
        )
        return None, 3
    except RefusedError as exc:
        print(
            f"the browser could not load {url}: {exc}"
            if url
            else f"the browser could not draw {exc}",
            file=sys.stderr,
        )
        return None, 5
    except PageTimeoutError as exc:
        print(
            f"timed out after {timeout}ms{f' on {url}' if url else ''}: {exc}",
            file=sys.stderr,
        )
        return None, 4
    except HungCallError as exc:
        print(exc, file=sys.stderr)
        return None, 7
    except UnmeasurableError as exc:
        if unmeasurable is None:
            raise
        print(unmeasurable[0])
        for r in exc.args[0]:
            print(f"  - {r}")
        print(unmeasurable[1])
        return None, 6
