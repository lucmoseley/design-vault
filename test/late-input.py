"""check-flow.py, with each pointer event reaching the page late, as on a
loaded machine: a press LATE_PRESS_MS, any other LATE_MOVE_MS:
python3 test/late-input.py <check-flow args>

check-flow-records.test.py runs the clean page's drag-release through it
(#478). Playwright's mouse and the DevTools protocol's mouse events are
both delayed here, in the driver, since what a load costs a fling is the
time between the events it sends; slowing the page's own CPU (DevTools'
CPU throttling) would delay its handlers, not when the throw reaches it.
"""

import importlib.util
import os
import sys
import time

from playwright.sync_api import CDPSession, Mouse

# The pause after a press, in ms: the 400 ms that reproduced #478's fault
# line; a guess at what a load average of 17 cost.
LATE_PRESS_MS = 400
# The pause after any other pointer event, in ms: four frames at 60 Hz, which
# once left a fling too few moves in its last 100 ms to read any velocity; a
# guess.
LATE_MOVE_MS = 60

FLOW = os.path.join(
    os.path.dirname(__file__),
    "..",
    "plugin",
    "skills",
    "design-round",
    "scripts",
    "check-flow.py",
)


def late(call, ms):
    def delayed(self, *args, **kw):
        out = call(self, *args, **kw)
        time.sleep(ms(*args, **kw) / 1000)
        return out

    return delayed


def cdp_ms(method, params=None):
    if method != "Input.dispatchMouseEvent":
        return 0
    return LATE_PRESS_MS if params["type"] == "mousePressed" else LATE_MOVE_MS


if __name__ == "__main__":
    Mouse.down = late(Mouse.down, lambda **_: LATE_PRESS_MS)
    Mouse.move = late(Mouse.move, lambda *_, **__: LATE_MOVE_MS)
    CDPSession.send = late(CDPSession.send, cdp_ms)
    spec = importlib.util.spec_from_file_location("check_flow", FLOW)
    flow = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(flow)
    sys.exit(flow.main(sys.argv[1:]))
