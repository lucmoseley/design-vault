"""check-flow.py, with each pointer press taking LATE_PRESS_MS to reach the
page's next move, as on a loaded machine: python3 test/late-press.py <check-flow args>

check-flow-records.test.py runs the clean page's drag-release through it
(#478), where a release velocity read from the moves alone ran the press's
delay into the fling and named a fault the page did not have.
"""

import importlib.util
import os
import sys
import time

from playwright.sync_api import Mouse

# The pause after a press, in ms: the 400 ms that reproduced #478's fault
# line; a guess at what a load average of 17 cost.
LATE_PRESS_MS = 400

FLOW = os.path.join(
    os.path.dirname(__file__),
    "..",
    "plugin",
    "skills",
    "design-round",
    "scripts",
    "check-flow.py",
)


def late_down(down):
    def pressed(self, **kw):
        down(self, **kw)
        time.sleep(LATE_PRESS_MS / 1000)

    return pressed


if __name__ == "__main__":
    Mouse.down = late_down(Mouse.down)
    spec = importlib.util.spec_from_file_location("check_flow", FLOW)
    flow = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(flow)
    sys.exit(flow.main(sys.argv[1:]))
