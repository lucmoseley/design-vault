"""check-flow.py, with each pointer event reaching the page late: a press
LATE_PRESS_MS, any other LATE_MOVE_MS; and with the page's main thread held
BUSY_RELEASE_MS at each release, before the page's own handler runs:
python3 test/late-input.py <check-flow args>
"""

import os
import sys
import time

from playwright.sync_api import CDPSession, Mouse

# measured: reproduced the fault line, #478
LATE_PRESS_MS = 400
# guess, #478
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
SCRIPTS = os.path.dirname(FLOW)  # #562
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
