import faulthandler
import gc
import signal
import sys
import traceback

faulthandler.register(signal.SIGUSR2, all_threads=True)


def greenlets(_signum, frame):
    out = ["--- every greenlet's stack ---\nrunning:\n", *traceback.format_stack(frame)]
    for obj in gc.get_objects():
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
