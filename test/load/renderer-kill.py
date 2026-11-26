"""Run by hand, never by the gate:
    python3 test/load/renderer-kill.py [runs=30] [busy=16]

Runs check-flow's renderer-killed-at-start case, new_page on a browser holding each renderer at its start, through check-overlay-shot.py's
loop(), SIGTERMing each renderer as /proc first shows it, every KILL_POLL_S. Each run's outcome is its exit and,
for an exit 7, the route: "waited", the watch's, or "raised", new_page raising once its renderer died. Runs
other than "7 waited" are printed.
"""

import contextlib
import importlib.util
import io
import os
import re
import signal
import sys
import threading
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))


# #606
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


shot = load("check_overlay_shot", os.path.join(HERE, "check-overlay-shot.py"))
FLOW = os.path.join(
    HERE, "..", "..", "plugin", "skills", "design-round", "scripts", "check-flow.py"
)
SCRIPTS = os.path.dirname(FLOW)  # #562
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

flow = siblings.load(SCRIPTS, "check-flow.py")

# guess, #472
KILL_POLL_S = 0.001


def run():
    stop = threading.Event()

    def kill():
        while not stop.wait(KILL_POLL_S):
            for pid in flow.descendants(os.getpid()):
                if "--type=renderer" in flow.process_args(pid):
                    with contextlib.suppress(ProcessLookupError):
                        os.kill(pid, signal.SIGTERM)

    def work():
        with flow.chromium(["--renderer-startup-dialog"]) as browser:
            browser.new_context().new_page()

    killer = threading.Thread(target=kill, daemon=True)
    err = io.StringIO()
    with mock.patch.multiple(flow, RENDERER_GONE_S=1, UNANSWERED_S=1):
        killer.start()
        with contextlib.redirect_stderr(err):
            _, code = flow.run_browser(work, flow.LOAD_TIMEOUT_MS)
    stop.set()
    killer.join()
    print(err.getvalue())
    route = re.search(r"^\S+ at \S+ (waited|raised)\b", err.getvalue())
    return f"{code} {route[1]}" if route else str(code)


def main(runs=shot.RUNS, busy=shot.BUSY):
    return shot.loop(run, "7 waited", runs, busy)


if __name__ == "__main__":
    sys.exit(main(*(int(a) for a in sys.argv[1:3])))
