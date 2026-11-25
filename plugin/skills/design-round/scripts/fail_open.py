"""The reporters a caught error is handed to when the program keeps working
past it (workflow-core base §N5): the core's own scripts/lib/fail_open.py,
held here because the plugin ships without the core. The core's pre-commit
refuses an `except` in a program that neither raises, exits nor hands the
error it binds to one of these."""

import sys


def fail_open(error, instead):
    """Print `error` and what the program does `instead` to stderr."""
    sys.stderr.write(f"fail-open: {instead}: {type(error).__name__}: {error}\n")
    sys.stderr.flush()


def expected(error, outcome):
    """Nothing: `error` is the program's normal path, which leads to
    `outcome`, so it is no fault and is not printed. The gate takes it only
    under a specific caught type."""
