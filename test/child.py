"""Runs a script as a gate suite's child, catches where it stalls (#430), and runs
it once more when earlyoom killed one of its renderers and its browser crashed (#431).
main() runs a Chromium gate suite's tests, and runs once more a test that crashed after
earlyoom killed one of its renderers (#438).

A stalled child's stacks come from test/child-site/sitecustomize.py, which
PYTHONPATH loads into it.
"""

import contextlib
import functools
import os
import re
import signal
import subprocess
import sys
import threading
import time
import traceback
import unittest

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "child-site")
# How long a stalled child has to write its stacks, and the tree to close its
# pipes once killed, in s. Guesses, unmeasured.
DUMP_S, GRACE_S = 2, 10
# How often a running child's process tree is read, in s. A guess, unmeasured. A renderer killed sooner after its
# birth is missed, and its run fails; a kill that early hangs instead, which is #432's.
WATCH_S = 0.1
# How far, in s, a journal timestamp may fall outside the span a renderer was seen alive and still be its kill:
# earlyoom stamps its line just after the signal, and the watcher sees a death up to a read late. A guess, unmeasured.
# A pid ended and reused by another session's renderer inside that span is mistaken for this run's.
SLACK_S = 1
# How long the journal read may take, in s. A guess, unmeasured.
JOURNAL_S = 10
# What Playwright says when a page's renderer dies under it.
CRASHED = "Target crashed"
# Chromium's flag on each renderer it starts.
RENDERER = b"--type=renderer"
EARLYOOM = "earlyoom"
# A journal line, as `journalctl -o short-unix` prints it, for each process earlyoom v1.7 signals.
KILL_LINE = re.compile(
    r"^(\d+\.\d+) \S+ [^:]+: sending SIG(?:TERM|KILL) to process (\d+) ", re.MULTILINE
)


class StallError(subprocess.TimeoutExpired):
    def __init__(self, cmd, timeout, output, stderr, *, tree):
        super().__init__(cmd, timeout, output, stderr)
        self.tree = tree

    def __str__(self):
        return (
            f"{super().__str__()}\n"
            f"--- its stderr, ending in its stacks ---\n{self.stderr or ''}\n"
            f"--- its process tree when it stalled ---\n{self.tree}"
        )


def listed():
    return (int(name) for name in os.listdir("/proc") if name.isdigit())


def stat(pid):
    """/proc/<pid>/stat's fields after the command name, from state on; OSError once the process has gone."""
    with open(f"/proc/{pid}/stat", encoding="utf8") as fh:
        # The command name, in parentheses, may hold spaces; the fields after it are fixed.
        return fh.read().rsplit(")", 1)[1].split()


def proc(pid):
    try:
        fields = stat(pid)
        with open(f"/proc/{pid}/wchan", encoding="utf8") as fh:
            wchan = fh.read() or "-"
        with open(f"/proc/{pid}/cmdline", "rb") as fh:
            args = fh.read().replace(b"\0", b" ").decode(errors="replace").strip()
    except OSError:
        return None
    state, ppid, cpu, rss = (
        fields[0],
        int(fields[1]),
        int(fields[11]) + int(fields[12]),
        fields[21],
    )
    return ppid, f"{pid} {ppid} {state} {cpu} {rss} {wchan} {args}"


def subtree(root, ppid_of):
    """root and every pid under it, from a {pid: ppid} reading of /proc."""
    under, grew = {root}, True
    while grew:
        more = {pid for pid, ppid in ppid_of.items() if ppid in under} - under
        under |= more
        grew = bool(more)
    return under


def ppids():
    got = {}
    for pid in listed():
        with contextlib.suppress(OSError):  # it ended between the listing and the read
            got[pid] = int(stat(pid)[1])
    return got


def renderer(pid):
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as fh:
            # Chromium rewrites its helpers' argv as one string, so the flag is no argument of its own.
            return RENDERER in fh.read()
    except OSError:
        return False


def tree(root):
    rows = {}
    for pid in listed():
        if row := proc(pid):
            rows[pid] = row
    under = subtree(root, {pid: ppid for pid, (ppid, _) in rows.items()})
    pids = sorted(pid for pid in under if pid in rows)
    return pids, "PID PPID STATE CPU_TICKS RSS_PAGES WCHAN ARGS\n" + "\n".join(
        rows[p][1] for p in pids
    )


def kill(pids):
    for pid in pids:
        with contextlib.suppress(ProcessLookupError):  # it ended on its own
            os.kill(pid, signal.SIGKILL)


def text(got):
    """A pipe's capture as text: a timed-out communicate() hands back bytes, or None."""
    return got.decode(errors="replace") if isinstance(got, bytes) else got or ""


def stalled(child, argv, timeout):
    pids = []
    try:
        pids, table = tree(child.pid)
        child.send_signal(signal.SIGUSR2)
        child.send_signal(signal.SIGUSR1)
        # The greenlet stacks come once the interpreter next runs; nothing says when they are done.
        time.sleep(DUMP_S)
    finally:
        # Chromium leads a process group of its own, so the tree is killed by pid, not by group (#430). Residual: a
        # process started after the tree was read escapes the kill, and one that ended in the wait and whose pid was
        # reused is killed in its stead. The child's own pid is safe: Popen signals it only while it is unreaped.
        kill(pid for pid in pids if pid != child.pid)
        child.kill()
    try:
        out, err = child.communicate(timeout=GRACE_S)
    except subprocess.TimeoutExpired as late:
        out, err = (
            text(late.output),
            f"{text(late.stderr)}\n(its pipes stayed open past the kill)",
        )
    return StallError(argv, timeout, out, err, tree=table)


def watch(root, lives, done):
    """Records in `lives`, as {pid: [first seen, first seen gone]}, each renderer under root, read each WATCH_S
    until `done` is set. One still running then is gone at that moment."""
    while True:
        now = time.time()
        here = {pid for pid in subtree(root, ppids()) if renderer(pid)}
        for pid in here:
            lives.setdefault(pid, [now, None])
        for pid, life in lives.items():
            if life[1] is None and pid not in here:
                life[1] = now
        if done.wait(WATCH_S):
            break
    for life in lives.values():
        if life[1] is None:
            life[1] = time.time()


def earlyoom_kills(since, tag=EARLYOOM):
    """(time, pid) for each process the journal says `tag` signalled since the epoch time `since`. Where the
    journal cannot be read, none, said on stderr: the run then fails. `tag` is
    earlyoom's own but in test/child.test.py."""
    try:
        got = subprocess.run(
            ["journalctl", "-t", tag, "--since", f"@{int(since)}"]
            + ["-o", "short-unix", "--no-pager"],
            capture_output=True,
            text=True,
            timeout=JOURNAL_S,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(
            f"test/child.py: no re-run, earlyoom's journal unread: {exc}",
            file=sys.stderr,
        )
        return []
    if got.returncode or got.stderr.strip():
        print(
            f"test/child.py: earlyoom's journal read with exit {got.returncode}: {got.stderr.strip()}",
            file=sys.stderr,
        )
    return [(float(t), int(pid)) for t, pid in KILL_LINE.findall(got.stdout)]


def killed_renderers(lives, kills):
    """The renderers in `lives` that a (time, pid) in `kills` signalled while it was alive."""
    return {
        pid
        for t, pid in kills
        if pid in lives and lives[pid][0] - SLACK_S <= t <= lives[pid][1] + SLACK_S
    }


# The renderers of each run that run() ran once more, since the test it ran under started: rerun() does not run
# that test again for them.
RERUN_RENDERERS = set()


def run(argv, *, timeout, kills=earlyoom_kills):
    """subprocess.run(argv, capture_output=True, text=True, timeout=timeout), but a
    stall raises StallError with the child's stacks and tree, and a run that failed with
    CRASHED after earlyoom killed one of its renderers is run once more, said on stderr.
    A re-run takes up to `timeout` again, and the first run's output is dropped but for
    that line. `kills` stands in for earlyoom's journal in test/child.test.py."""
    began = time.time()
    result, lives = once(argv, timeout=timeout)
    if CRASHED in result.stderr and (killed := killed_renderers(lives, kills(began))):
        print(
            f"test/child.py: earlyoom killed renderer {', '.join(map(str, sorted(killed)))} of {argv}, "
            f"which then failed with {CRASHED!r}; running it once more (#431)",
            file=sys.stderr,
        )
        result, again = once(argv, timeout=timeout)
        RERUN_RENDERERS.update(lives, again)
    return result


def once(argv, *, timeout):
    env = {
        **os.environ,
        "PYTHONPATH": os.pathsep.join(
            filter(None, [SITE, os.environ.get("PYTHONPATH")])
        ),
    }
    with (
        subprocess.Popen(
            argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env
        ) as child,
        watching(child.pid) as lives,
    ):
        try:
            out, err = child.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            raise stalled(child, argv, timeout) from None
        except BaseException:
            child.kill()
            raise
    return subprocess.CompletedProcess(argv, child.returncode, out, err), lives


# The unittest result calls that report on a test, held until the test's outcome is known.
REPORT_CALLS = {
    "startTest",
    "stopTest",
    "addSuccess",
    "addError",
    "addFailure",
    "addSkip",
    "addExpectedFailure",
    "addUnexpectedSuccess",
    "addSubTest",
    "addDuration",
}


@contextlib.contextmanager
def watching(root):
    lives, done = {}, threading.Event()
    watcher = threading.Thread(target=watch, args=(root, lives, done), daemon=True)
    watcher.start()
    try:
        yield lives
    finally:
        done.set()
        watcher.join()


class HeldResult:
    """A unittest result that holds what a test tells it until replay(); everything else is the result's own."""

    def __init__(self, result):
        self.result, self.told = result, []

    def __getattr__(self, name):
        got = getattr(self.result, name)
        if name not in REPORT_CALLS:
            return got
        return lambda *args: self.told.append((name, args))

    def crashed(self):
        return any(
            CRASHED in "".join(traceback.format_exception(*args[-1]))
            for name, args in self.told
            if name in ("addError", "addFailure", "addSubTest") and args[-1] is not None
        )

    def replay(self):
        for name, args in self.told:
            getattr(self.result, name)(*args)


def rerun(case, run_once, result=None, *, kills):
    """case.run(result), where `run_once` is the case's own run(), but a test that failed with CRASHED after earlyoom
    killed a renderer of this process's tree is run once more, said on stderr, and the first run's outcome dropped.
    Residual: the result is told nothing until the test ends, so a test that hangs leaves no name in a verbose log.
    A module's or class's fixture runs outside this: launching Chromium starts no renderer until its first page,
    and a fixture's child is re-run by run(), but a page a fixture opens in this process is not run again."""
    if result is None:
        return run_once(result)
    began, held = time.time(), HeldResult(result)
    RERUN_RENDERERS.clear()
    with watching(os.getpid()) as lives:
        run_once(held)
    fresh = {pid: life for pid, life in lives.items() if pid not in RERUN_RENDERERS}
    if held.crashed() and (killed := killed_renderers(fresh, kills(began))):
        print(
            f"test/child.py: earlyoom killed renderer {', '.join(map(str, sorted(killed)))} under {case.id()}, "
            f"which then failed with {CRASHED!r}; running it once more (#438)",
            file=sys.stderr,
        )
        return run_once(result)
    held.replay()
    return result


def raise_if_crashed(stderr):
    """Raises a captured run's stderr where it says CRASHED, so main() can run the test once more rather than keep
    the run's outcome."""
    if CRASHED in stderr:
        raise RuntimeError(stderr)


def rerunning(tests, kills=earlyoom_kills):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            rerunning(test, kills)
        elif isinstance(test, unittest.TestCase):
            test.run = functools.partial(rerun, test, test.run, kills=kills)
    return tests


class Runner(unittest.TextTestRunner):
    def run(self, test):
        return super().run(rerunning(test))


def main(**kwargs):
    """unittest.main() for a Chromium gate suite: a test earlyoom broke is run once more (#438)."""
    unittest.main(module="__main__", testRunner=Runner, **kwargs)
