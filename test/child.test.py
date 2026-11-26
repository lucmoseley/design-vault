import contextlib
import io
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402

# guess, #430
STALL_S = 3
FOREVER_S = STALL_S + 3 * child.GRACE_S
STALLS = f"""
import subprocess, time, greenlet
subprocess.Popen(["sh", "-c", "sleep {FOREVER_S} & echo $!; wait"], start_new_session=True)
def dispatches():
    time.sleep({FOREVER_S})
loop = greenlet.greenlet(dispatches)
def waits_on_the_browser():
    loop.switch()
waits_on_the_browser()
"""


def alive(pid):
    try:
        with open(f"/proc/{pid}/stat", encoding="utf8") as fh:
            return fh.read().rsplit(")", 1)[1].split()[0] != "Z"
    except OSError:
        return False


# guess, #438
RENDERER_S, HELD_S = 30, 10 * child.WATCH_S
# What `playwright==1.61.0` raised for a killed renderer, measured in #439; the trailing space is its own.
SAID = {
    "Page.evaluate: Target crashed ": "Target crashed",
    "Page.goto: Page crashed": "Page crashed",
    "Navigation failed because page crashed!": "Navigation failed because page crashed!",
}
DEFAULT_SAID = next(iter(SAID))
OTHER_SAID = {said: wording for said, wording in SAID.items() if said != DEFAULT_SAID}
CRASHES = f"""
import subprocess, sys, time
runs, crash_on, kind, said = sys.argv[1], sys.argv[2].split(","), sys.argv[3], sys.argv[4]
flag = ["headless_shell " + {child.RENDERER.decode()!r}] if kind == "renderer" else []
grandchild = subprocess.Popen([sys.executable, "-c", "import time; time.sleep({RENDERER_S})", *flag])
time.sleep({HELD_S})
with open(runs, "a") as fh:
    print(grandchild.pid, time.time(), file=fh)
grandchild.kill()
with open(runs) as fh:
    n = len(fh.read().splitlines())
if str(n) in crash_on:
    sys.exit(said)
print("passed on run", n)
"""


class Kills:
    def setUp(self):
        fd, self.runs = tempfile.mkstemp()
        os.close(fd)
        self.addCleanup(os.unlink, self.runs)

    def forget(self):
        open(self.runs, "w", encoding="utf8").close()

    def killed(self):
        with open(self.runs, encoding="utf8") as fh:
            return [(float(t), int(pid)) for pid, t in map(str.split, fh)]


class Rerun(Kills, unittest.TestCase):
    def run_with(self, crash_on, kills, kind="renderer", said=DEFAULT_SAID):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            r = child.run(
                [sys.executable, "-c", CRASHES, self.runs, crash_on, kind, said],
                timeout=FOREVER_S,
                kills=kills,
            )
        return r, err.getvalue()

    def test_a_crash_after_earlyoom_killed_its_renderer_is_run_once_more_431(self):
        r, err = self.run_with("1", lambda since: self.killed()[:1])
        self.assertEqual((r.returncode, r.stdout), (0, "passed on run 2\n"))
        self.assertEqual(len(self.killed()), 2)
        self.assertRegex(
            err, rf"earlyoom killed renderer {self.killed()[0][1]} of .*once more"
        )
        self.assertIn(self.killed()[0][1], child.RERUN_RENDERERS)

    def test_each_wording_playwright_gives_a_killed_renderer_is_run_once_more(self):
        for said, wording in OTHER_SAID.items():
            with self.subTest(said=said):
                self.forget()
                r, err = self.run_with("1", lambda since: self.killed()[:1], said=said)
                self.assertEqual((r.returncode, len(self.killed())), (0, 2))
                self.assertIn(f"failed with {wording!r}", err)

    def test_a_crash_of_another_wording_is_not_run_again(self):
        r, _ = self.run_with(
            "1", lambda since: self.killed(), said="Page.goto: net::ERR_ABORTED"
        )
        self.assertEqual((r.returncode, len(self.killed())), (1, 1))

    def test_it_is_run_once_more_only_once(self):
        r, _ = self.run_with("1,2", lambda since: self.killed())
        self.assertIn(DEFAULT_SAID, r.stderr)
        self.assertEqual(len(self.killed()), 2)

    def test_a_crash_with_no_kill_of_its_own_tree_is_not_run_again(self):
        r, err = self.run_with("1", lambda since: [(time.time(), os.getpid())])
        self.assertIn(DEFAULT_SAID, r.stderr)
        self.assertEqual((len(self.killed()), err), (1, ""))

    def test_a_kill_of_a_process_that_is_no_renderer_is_not_run_again(self):
        r, _ = self.run_with("1", lambda since: self.killed(), kind="gpu")
        self.assertIn(DEFAULT_SAID, r.stderr)
        self.assertEqual(len(self.killed()), 1)

    def test_a_kill_of_its_pid_after_the_renderer_ended_is_not_run_again(self):
        r, _ = self.run_with(
            "1", lambda since: [(t + 60, pid) for t, pid in self.killed()]
        )
        self.assertIn(DEFAULT_SAID, r.stderr)
        self.assertEqual(len(self.killed()), 1)

    def test_a_kill_with_no_crash_is_not_run_again(self):
        r, _ = self.run_with("", lambda since: self.killed())
        self.assertEqual((r.returncode, len(self.killed())), (0, 1))

    def test_the_kills_are_read_from_the_run_start_on(self):
        asked = []
        before = time.time()
        self.run_with("1", lambda since: asked.append(since) or [])
        self.assertEqual(len(asked), 1)
        self.assertTrue(before <= asked[0] <= self.killed()[0][0])

    def test_earlyooms_own_lines_give_the_time_and_pid_it_signalled(self):
        journal = (
            "1794788743.103118 Luctop earlyoom[167]: low memory! at or below SIGTERM limits: mem  8.00%\n"
            '1794788743.103118 Luctop earlyoom[167]: sending SIGTERM to process 3823486 uid 1000 "headless_shell": '
            "badness 806, VmRSS 123 MiB\n"
            '1794788743.361809 Luctop earlyoom[167]: sending SIGKILL to process 3824121 uid 1000 "headless_shell": '
            "badness 806, VmRSS 120 MiB\n"
        )
        self.assertEqual(
            [(float(t), int(p)) for t, p in child.KILL_LINE.findall(journal)],
            [(1794788743.103118, 3823486), (1794788743.361809, 3824121)],
        )

    @unittest.skipUnless(
        shutil.which("journalctl") and shutil.which("logger"), "no journal here"
    )
    def test_the_journal_is_read_as_earlyoom_writes_it(self):
        tag, since = f"child-test-{os.getpid()}", time.time()
        line = 'sending SIGTERM to process 42 uid 1000 "headless_shell": badness 1, VmRSS 1 MiB'
        subprocess.run(["logger", "-t", tag, line], check=True)
        deadline, got = time.monotonic() + child.JOURNAL_S, []
        while not got and time.monotonic() < deadline:
            got = child.earlyoom_kills(since, tag)
            time.sleep(0.2)
        self.assertEqual([pid for _, pid in got], [42])
        self.assertTrue(since - child.SLACK_S <= got[0][0] <= time.time())


class Run(unittest.TestCase):
    def test_a_finished_child_returns_as_subprocess_run_does(self):
        r = child.run(
            [
                sys.executable,
                "-c",
                "import sys; print('out'); print('err', file=sys.stderr); sys.exit(3)",
            ],
            timeout=FOREVER_S,
        )
        self.assertEqual((r.returncode, r.stdout, r.stderr), (3, "out\n", "err\n"))

    def test_a_stall_leaves_with_its_stack_and_tree_and_the_tree_killed_430(self):
        with self.assertRaises(child.StallError) as caught:
            child.run([sys.executable, "-c", STALLS], timeout=STALL_S)
        stall = caught.exception
        self.assertTrue(stall.output, "the child printed no grandchild pid")
        grandchild = int(stall.output.split()[0])
        self.assertRegex(stall.stderr, r"Current thread.*\n(.*\n)*.*dispatches")
        self.assertRegex(
            stall.stderr, r"suspended greenlet .*\n(.*\n)*.*waits_on_the_browser"
        )
        self.assertRegex(stall.tree, rf"(?m)^{grandchild} .*sleep {FOREVER_S}")
        self.assertIn("waits_on_the_browser", str(stall))
        deadline = time.monotonic() + child.GRACE_S
        while alive(grandchild) and time.monotonic() < deadline:
            time.sleep(0.1)
        self.assertFalse(alive(grandchild), "the grandchild outlived the stall")

    def test_a_stall_is_a_timeout_to_code_that_catches_one(self):
        self.assertTrue(issubclass(child.StallError, child.subprocess.TimeoutExpired))


class RaiseIfCrashed(unittest.TestCase):
    def test_a_captured_crash_is_raised_with_its_stderr(self):
        for said in SAID:
            with self.subTest(said=said):
                with self.assertRaises(RuntimeError) as raised:
                    child.raise_if_crashed(f"Traceback:\n{said}\n")
                self.assertIn(said, str(raised.exception))

    def test_each_wording_is_found_in_what_playwright_raised(self):
        for said, wording in SAID.items():
            with self.subTest(said=said):
                self.assertEqual(child.crash(f"Traceback:\n{said}\n"), wording)

    def test_a_capture_with_no_crash_is_kept(self):
        self.assertIsNone(child.raise_if_crashed("Traceback: a fault of its own"))


class InProcess(Kills, unittest.TestCase):
    def outcome(
        self, crash_on, kills, *, said=None, how="raise", foreign=False, spent=False
    ):
        runs, flag = self.runs, ["headless_shell " + child.RENDERER.decode()]
        said = DEFAULT_SAID if said is None else said

        class Drives(unittest.TestCase):
            def test_it(self):
                argv = [
                    sys.executable,
                    "-c",
                    f"import time; time.sleep({RENDERER_S})",
                    *flag,
                ]
                started = None
                if foreign:
                    pid = int(
                        subprocess.run(
                            ["sh", "-c", '"$@" >/dev/null 2>&1 & echo $!', "sh", *argv],
                            capture_output=True,
                            text=True,
                            check=True,
                        ).stdout
                    )
                else:
                    started = subprocess.Popen(argv)
                    pid = started.pid
                time.sleep(HELD_S)
                with open(runs, "a", encoding="utf8") as fh:
                    print(pid, time.time(), file=fh)
                os.kill(pid, signal.SIGKILL)
                if started:
                    started.wait()
                if spent:
                    child.RERUN_RENDERERS.add(pid)
                with open(runs, encoding="utf8") as fh:
                    n = len(fh.read().splitlines())
                if n not in crash_on:
                    return
                if how == "skip":
                    self.skipTest(said)
                if how == "subtest":
                    with self.subTest(n=n):
                        raise RuntimeError(said)
                    return
                raise RuntimeError(said)

        stream, err = io.StringIO(), io.StringIO()
        suite = child.rerunning(
            unittest.TestLoader().loadTestsFromTestCase(Drives), kills
        )
        with contextlib.redirect_stderr(err):
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        return result, err.getvalue(), stream.getvalue()

    def test_a_crash_after_earlyoom_killed_its_renderer_is_run_once_more_438(self):
        result, err, shown = self.outcome({1}, lambda since: self.killed()[:1])
        self.assertTrue(result.wasSuccessful(), shown)
        self.assertEqual((result.testsRun, len(self.killed())), (1, 2))
        self.assertRegex(
            err,
            rf"earlyoom killed renderer {self.killed()[0][1]} under .*test_it.*once more",
        )
        self.assertEqual(shown.count(" ... "), 1, shown)

    def test_each_wording_playwright_gives_a_killed_renderer_is_run_once_more(self):
        for said, wording in OTHER_SAID.items():
            with self.subTest(said=said):
                self.forget()
                result, err, shown = self.outcome(
                    {1}, lambda since: self.killed()[:1], said=said
                )
                self.assertTrue(result.wasSuccessful(), shown)
                self.assertEqual(len(self.killed()), 2)
                self.assertIn(f"failed with {wording!r}", err)

    def test_a_crash_in_a_subtest_is_run_once_more(self):
        result, _, shown = self.outcome(
            {1}, lambda since: self.killed()[:1], how="subtest"
        )
        self.assertTrue(result.wasSuccessful(), shown)
        self.assertEqual(len(self.killed()), 2)

    def test_it_is_run_once_more_only_once(self):
        result, _, _ = self.outcome({1, 2}, lambda since: self.killed())
        self.assertEqual((len(result.errors), len(self.killed())), (1, 2))
        self.assertIn(DEFAULT_SAID, result.errors[0][1])

    def test_a_kill_child_run_already_ran_once_more_for_is_not_run_again(self):
        result, err, _ = self.outcome({1}, lambda since: self.killed(), spent=True)
        self.assertEqual((len(result.errors), len(self.killed()), err), (1, 1, ""))

    def test_a_kill_of_a_renderer_outside_its_tree_is_not_run_again(self):
        result, err, _ = self.outcome({1}, lambda since: self.killed(), foreign=True)
        self.assertEqual((len(result.errors), len(self.killed()), err), (1, 1, ""))

    def test_a_kill_with_a_failure_of_another_kind_is_not_run_again(self):
        result, _, _ = self.outcome(
            {1}, lambda since: self.killed(), said="a fault of its own"
        )
        self.assertEqual((len(result.errors), len(self.killed())), (1, 1))

    def test_a_passing_test_is_reported_once_as_it_ran(self):
        result, err, shown = self.outcome(set(), lambda since: self.killed())
        self.assertTrue(result.wasSuccessful())
        self.assertEqual((result.testsRun, len(self.killed()), err), (1, 1, ""))
        self.assertRegex(shown, r"test_it .*\.\.\. ok")

    def test_a_skip_is_reported_as_it_ran(self):
        result, _, shown = self.outcome({1}, lambda since: [], how="skip")
        self.assertEqual((len(result.skipped), len(self.killed())), (1, 1))
        self.assertRegex(shown, r"test_it .*\.\.\. skipped")
        self.assertEqual(shown.count(" ... "), 1, shown)


if __name__ == "__main__":
    unittest.main()
