import logging
import os
import sys

CANNOT_RUN = 2  # #543


def run_main(main):
    try:
        code = main(sys.argv[1:])
    except Exception:
        logging.exception("%s: cannot run", os.path.basename(sys.argv[0]))
        sys.exit(CANNOT_RUN)
    sys.exit(code)
