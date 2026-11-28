import logging
import os
import sys

import siblings

HERE = os.path.dirname(os.path.abspath(__file__))
CANNOT_RUN = 2  # #543


def guard(name):
    if name == "__main__":
        sys.excepthook = exit_for


def exit_for(kind, err, trace):
    if isinstance(err, ModuleNotFoundError):
        sys.exit(siblings.load(HERE, "runner.py").missing(err))
    if not isinstance(err, Exception):
        sys.__excepthook__(kind, err, trace)
        return
    logging.error(
        "%s: cannot run",
        os.path.basename(sys.argv[0]),
        exc_info=(kind, err, trace),
    )
    sys.exit(CANNOT_RUN)
