import logging
import os
import pathlib
import re
import sys

REQUIREMENTS = pathlib.Path(__file__).resolve().parents[3] / "requirements.txt"
PIP_INSTALL = f"python3 -m pip install --only-binary :all: -r {REQUIREMENTS}"
CANNOT_RUN = 2  # #543
MISSING = 3
IMPORTED_AS = {"PIL": "pillow"}


def guard(name):
    if name == "__main__":
        sys.excepthook = exit_for


def missing(err):
    script = os.path.basename(sys.argv[0])
    print(
        f"{script}: {err.name or err} is missing — {PIP_INSTALL}",
        file=sys.stderr,
    )
    return MISSING


def pinned(name):
    top = (name or "").partition(".")[0]
    try:
        lines = REQUIREMENTS.read_text().splitlines()
    except OSError:
        return False
    wanted = IMPORTED_AS.get(top, top).lower()
    return any(
        re.split(r"[=<>~! ]", line, maxsplit=1)[0].lower() == wanted for line in lines
    )


def exit_for(kind, err, trace):
    if not isinstance(err, Exception):
        sys.__excepthook__(kind, err, trace)
        return
    if isinstance(err, ImportError) and pinned(err.name):
        sys.exit(missing(err))
    logging.error(
        "%s: cannot run",
        os.path.basename(sys.argv[0]),
        exc_info=(kind, err, trace),
    )
    sys.exit(CANNOT_RUN)
