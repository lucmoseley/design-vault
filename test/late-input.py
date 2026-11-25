"""check-flow.py, with each pointer event reaching the page late: a press
LATE_PRESS_MS, any other LATE_MOVE_MS; and with the page's main thread held
BUSY_RELEASE_MS at each release, before the page's own handler runs:
python3 test/late-input.py <check-flow args>

check-flow-records.test.py runs the clean page's drag-release through it.
Playwright's mouse and the DevTools protocol's mouse events are
both delayed here, in the driver, since what a load costs a fling is the
time between the events it sends; slowing the page's own CPU (DevTools'
CPU throttling) would delay its handlers, not when the throw reaches it.
"""

import os
import sys
import time

from playwright.sync_api import CDPSession, Mouse

# The pause after a press, in ms: the 400 ms that reproduced #478's fault
# line; a guess at what a load average of 17 cost.
LATE_PRESS_MS = 400
# The pause after any other pointer event, in ms: a guess.
LATE_MOVE_MS = 60
# measured: turned the clean card back in 10 of 10 flings before the fix (#510)
BUSY_RELEASE_MS = 40
BUSY_RELEASE_INIT = (
    "addEventListener('pointerup', () => {"
    " const s = performance.now(); while (performance.now() - s < %d); }, true);"
    % BUSY_RELEASE_MS
)

FLOW = os.path.join(
    os.path.dirname(__file__),
    "..",
    "plugin",
    "skills",
    "design-round",
    "scripts",
    "check-flow.py",
)
SCRIPTS = os.path.dirname(FLOW)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402


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
    flow = siblings.load(SCRIPTS, "check-flow.py")
    flow.records.RELEASE_INIT += BUSY_RELEASE_INIT
    sys.exit(flow.main(sys.argv[1:]))
