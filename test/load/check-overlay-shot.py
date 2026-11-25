"""#136's loop: check-overlay's screenshot under induced load. Run by hand, never by the gate:
    python3 test/load/check-overlay-shot.py [runs=30] [busy=16]

Runs check-overlay's own main() in-process on the arch pair (a mark shifted 1 px off its source on white,
which exits 1), beside <busy> CPU busy loops at the lowest priority. During every page.screenshot() call it
stops the page's renderer once, for 1.5 s, starting 0 to 120 ms into the call. The stall is the hypothesis,
a renderer descheduled on a loaded machine; nothing ties the 13 Oct gate's reds to it beyond their message
and their falling on the first file drawn. Prints the exit counts (5 is the bug) and each screenshot's outcome.

With the retry removed (SHOTS = 1), 1 of 60 runs exited 5 on 14 Oct, so a batch of 30 can show none; #147
has the counts. With the loops at normal priority it was 1 run in 8 to 1 in 4 (#136).
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
spec = importlib.util.spec_from_file_location(
    "overlay_test", os.path.join(HERE, "..", "check-overlay.test.py")
)
tests = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tests)

# s. On 13 Oct 2026 an unstalled screenshot took 39-149 ms, and only a stall starting inside one gave the
# message. Stalls of 0.3 to 4 s each gave it at times, so STALL is a first guess among them.
STALL, EARLIEST, LATEST = 1.5, 0, 0.12
# s each run may take before the busy loops end themselves, so a run killed past its finally leaves none
# spinning beyond runs * RUN_CEILING. A first guess: on 14 Oct a run here took 4.5 s, and sibling-shots.py's
# sheet, the slower of the two of its targets timed, about 20 s. Residual: a batch that outlasts it runs on
# unloaded, which loop() prints.
RUN_CEILING = 60
# The default batch, kept from #136, where it first reproduced the stall (7 of 30 runs without the retry): a
# first guess, 16 busy loops being twice this machine's 8 cores.
RUNS, BUSY = 30, 16


def renderers():
    """This process's Chromium renderers. Chromium rewrites its argv as one string."""
    kids = {}
    for pid in filter(str.isdigit, os.listdir("/proc")):
        try:
            with open(f"/proc/{pid}/stat") as fh:
                kids.setdefault(int(fh.read().rsplit(")", 1)[1].split()[1]), []).append(
                    int(pid)
                )
        except OSError:  # the process exited after listdir
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
    """page.screenshot() with the stall, counted by its caller's line, by whether it is the page's first
    shot, and by whether the stall landed: a shot done inside the 0-120 ms wait is never stalled."""
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
                with contextlib.suppress(
                    ProcessLookupError
                ):  # a closed context's renderer, gone since listed
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
    """Calls call() <runs> times beside <busy> busy loops with every screenshot stalled, and prints each run
    that did not exit <expected> with the tail of its output, then the exit and screenshot counts."""
    Page.screenshot = stalled
    ceiling = runs * RUN_CEILING
    print(
        f"Starting {busy} busy loops at the lowest CPU priority for at most {ceiling / 60:g} min "
        f"({runs} runs); other sessions' suites and commits run slower meanwhile.",
        flush=True,
    )
    # nice 19, so other sessions' commits keep the CPU (#147).
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
