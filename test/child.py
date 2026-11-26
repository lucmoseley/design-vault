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
# guess, #430
DUMP_S, GRACE_S = 2, 10
# guess, #431
WATCH_S = 0.1
# guess, #431
SLACK_S = 1
# guess, #431
JOURNAL_S = 10
# What `playwright==1.61.0` raises once a page's renderer dies, SIGTERM or SIGKILL alike, measured in #439.
CRASHED = ("Target crashed", "Page crashed", "Navigation failed because page crashed!")
RENDERER = b"--type=renderer"
EARLYOOM = "earlyoom"
# earlyoom v1.7's kill line under `journalctl -o short-unix`: https://github.com/rfjakob/earlyoom
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
    with open(f"/proc/{pid}/stat", encoding="utf8") as fh:
        # comm may hold spaces and parentheses: https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html
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
    under, grew = {root}, True
    while grew:
        more = {pid for pid, ppid in ppid_of.items() if ppid in under} - under
        under |= more
        grew = bool(more)
    return under


def ppids():
    got = {}
    for pid in listed():
        with contextlib.suppress(OSError):
            got[pid] = int(stat(pid)[1])
    return got


def renderer(pid):
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as fh:
            # Chromium rewrites a helper's argv as one string: https://chromium.googlesource.com/chromium/src/+/main/base/process/set_process_title_linux.cc
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
        with contextlib.suppress(ProcessLookupError):
            os.kill(pid, signal.SIGKILL)


def text(got):
    return got.decode(errors="replace") if isinstance(got, bytes) else got or ""


def stalled(child, argv, timeout):
    pids = []
    try:
        pids, table = tree(child.pid)
        child.send_signal(signal.SIGUSR2)
        child.send_signal(signal.SIGUSR1)
        time.sleep(DUMP_S)
    finally:
        # #430
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


def crash(said):
    return next((wording for wording in CRASHED if wording in said), None)


def killed_renderers(lives, kills):
    return {
        pid
        for t, pid in kills
        if pid in lives and lives[pid][0] - SLACK_S <= t <= lives[pid][1] + SLACK_S
    }


RERUN_RENDERERS = set()


def run(argv, *, timeout, kills=earlyoom_kills):
    began = time.time()
    result, lives = once(argv, timeout=timeout)
    if (said := crash(result.stderr)) and (
        killed := killed_renderers(lives, kills(began))
    ):
        print(
            f"test/child.py: earlyoom killed renderer {', '.join(map(str, sorted(killed)))} of {argv}, "
            f"which then failed with {said!r}; running it once more (#431)",
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
    def __init__(self, result):
        self.result, self.told = result, []

    def __getattr__(self, name):
        got = getattr(self.result, name)
        if name not in REPORT_CALLS:
            return got
        return lambda *args: self.told.append((name, args))

    def crash(self):
        return next(
            (
                said
                for name, args in self.told
                if name in ("addError", "addFailure", "addSubTest")
                and args[-1] is not None
                if (said := crash("".join(traceback.format_exception(*args[-1]))))
            ),
            None,
        )

    def replay(self):
        for name, args in self.told:
            getattr(self.result, name)(*args)


def rerun(case, run_once, result=None, *, kills):
    if result is None:
        return run_once(result)
    began, held = time.time(), HeldResult(result)
    RERUN_RENDERERS.clear()
    with watching(os.getpid()) as lives:
        run_once(held)
    fresh = {pid: life for pid, life in lives.items() if pid not in RERUN_RENDERERS}
    if (said := held.crash()) and (killed := killed_renderers(fresh, kills(began))):
        print(
            f"test/child.py: earlyoom killed renderer {', '.join(map(str, sorted(killed)))} under {case.id()}, "
            f"which then failed with {said!r}; running it once more (#438)",
            file=sys.stderr,
        )
        return run_once(result)
    held.replay()
    return result


def raise_if_crashed(stderr):
    if crash(stderr):
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
    unittest.main(module="__main__", testRunner=Runner, **kwargs)
