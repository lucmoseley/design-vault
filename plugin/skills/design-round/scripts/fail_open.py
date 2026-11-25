# workflow-core#5487
import sys


def fail_open(error, instead):
    sys.stderr.write(f"fail-open: {instead}: {type(error).__name__}: {error}\n")
    sys.stderr.flush()


def expected(error, outcome):
    # workflow-core#5503
    pass
