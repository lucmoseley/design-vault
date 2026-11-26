"""check-overlay's screenshot under induced load. Run by hand, never by the gate:
    python3 test/load/check-overlay-shot.py [runs=30] [busy=16]

Runs check-overlay's own main() in-process on the arch pair (a mark shifted 1 px off its source on white,
which exits 1), beside <busy> CPU busy loops at the lowest priority. During every page.screenshot() call it
stops the page's renderer once, for 1.5 s, starting 0 to 120 ms into the call. Prints the exit counts (5 is
the bug) and each screenshot's outcome.
"""

import collections
import contextlib
import importlib.util
import io
import os
import random
import signal
import subprocess
import sys
import tempfile
import threading
import time
import weakref

from playwright.sync_api import Error, Page

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(
    HERE, "..", "..", "plugin", "skills", "design-round", "scripts", "check-overlay.py"
)
SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

overlay = siblings.load(SCRIPTS, "check-overlay.py")
# #606
spec = importlib.util.spec_from_file_location(
    "overlay_test", os.path.join(HERE, "..", "check-overlay.test.py")
)
tests = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tests)

# guess, #136
STALL, EARLIEST, LATEST = 1.5, 0, 0.12
# guess, #147
RUN_CEILING = 60
# guess, #136
RUNS, BUSY = 30, 16


def renderers():
    kids = {}
    for pid in filter(str.isdigit, os.listdir("/proc")):
        try:
            with open(f"/proc/{pid}/stat") as fh:
                kids.setdefault(int(fh.read().rsplit(")", 1)[1].split()[1]), []).append(
                    int(pid)
                )
        except OSError:
            continue
    found, todo = [], [os.getpid()]
    while todo:
        for pid in kids.get(todo.pop(), []):
            todo.append(pid)
            try:
                with open(f"/proc/{pid}/cmdline", "rb") as fh:
                    if (
                        "--type=renderer"
                        in fh.read().decode(errors="replace").replace("\0", " ").split()
                    ):
                        found.append(pid)
            except OSError:
                continue
    return found


calls = collections.Counter()
shot_pages = weakref.WeakSet()
real_screenshot = Page.screenshot


def stalled(self, *args, **kwargs):
    caller = sys._getframe(1)
    where = f"{os.path.basename(caller.f_code.co_filename)}:{caller.f_lineno}"
    first = self not in shot_pages
    shot_pages.add(self)
    pids, done, stopped = renderers(), threading.Event(), []

    def stall():
        if done.wait(random.uniform(EARLIEST, LATEST)):
            return
        try:
            for pid in pids:
                with contextlib.suppress(ProcessLookupError):
                    os.kill(pid, signal.SIGSTOP)
                    stopped.append(pid)
            time.sleep(STALL)
        finally:
            for pid in stopped:
                with contextlib.suppress(ProcessLookupError):
                    os.kill(pid, signal.SIGCONT)

    thread = threading.Thread(target=stall)
    thread.start()
    outcome = "drawn"
    try:
        return real_screenshot(self, *args, **kwargs)
    except Error as exc:
        outcome = f"failed: {overlay.first_line(exc)[-40:]}"
        raise
    finally:
        done.set()
        thread.join()
        calls[
            f"{where}, {'first' if first else 'repeat'} shot, {'stalled' if stopped else 'not stalled'}: {outcome}"
        ] += 1


def loop(call, expected, runs, busy):
    Page.screenshot = stalled
    ceiling = runs * RUN_CEILING
    print(
        f"Starting {busy} busy loops at the lowest CPU priority for at most {ceiling / 60:g} min "
        f"({runs} runs); other sessions' suites and commits run slower meanwhile.",
        flush=True,
    )
    loops = [
        subprocess.Popen(
            [
                "nice",
                "-n",
                "19",
                "bash",
                "-c",
                f"while ((SECONDS < {ceiling})); do :; done",
            ]
        )
        for _ in range(busy)
    ]
    codes, loaded = collections.Counter(), bool(loops)
    try:
        for i in range(runs):
            if loaded and loops[0].poll() is not None:
                print(
                    f"run {i}: busy loops past their {ceiling} s ceiling; this run and later ones go unloaded",
                    flush=True,
                )
                loaded = False
            out = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                code = call()
            codes[code] += 1
            if code != expected:
                print(
                    f"run {i}: exit {code}: {' '.join(out.getvalue().split())[-240:]}",
                    flush=True,
                )
    finally:
        for busy_loop in loops:
            busy_loop.kill()
    print("exits", dict(sorted(codes.items())), "| screenshots:")
    for key, n in sorted(calls.items()):
        print(f"  {n:4}  {key}")
    return 1 if set(codes) - {expected} else 0


def main(runs=RUNS, busy=BUSY):
    with tempfile.TemporaryDirectory() as tmp:
        on_white = tests.ARCH.format(dx=0).replace(
            "<g ", '<rect width="120" height="80" fill="#fff"/><g '
        )
        pair = [os.path.join(tmp, "mark.svg"), os.path.join(tmp, "source.svg")]
        for path, svg in zip(pair, (tests.ARCH.format(dx=1), on_white), strict=True):
            with open(path, "w", encoding="utf8") as fh:
                fh.write(svg)
        return loop(lambda: overlay.main(pair), 1, runs, busy)


if __name__ == "__main__":
    sys.exit(main(*(int(a) for a in sys.argv[1:3])))
