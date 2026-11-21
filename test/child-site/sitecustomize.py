"""Loaded into every child test/child.py starts, by its PYTHONPATH (#430), to say where a stalled run is stuck.

SIGUSR2 writes every thread's Python stack to stderr, from C, so it answers even
while the interpreter is stuck. SIGUSR1 writes every greenlet's: Playwright's
sync API waits on the browser in a greenlet of its own, so the thread stack
shows only its event loop, and the caller's frames are left suspended in another.
"""

import faulthandler
import gc
import signal
import sys
import traceback

faulthandler.register(signal.SIGUSR2, all_threads=True)


def greenlets(_signum, frame):
    out = ["--- every greenlet's stack ---\nrunning:\n", *traceback.format_stack(frame)]
    for obj in gc.get_objects():
        # By name, so a child that never loads greenlet does not load it here.
        if (
            type(obj).__name__ == "greenlet"
            and getattr(obj, "gr_frame", None) is not None
        ):
            out += [
                f"suspended greenlet {id(obj):#x}:\n",
                *traceback.format_stack(obj.gr_frame),
            ]
    sys.stderr.write("".join(out))
    sys.stderr.flush()


signal.signal(signal.SIGUSR1, greenlets)
