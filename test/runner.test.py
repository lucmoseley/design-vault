# #432
import contextlib
import http.server
import importlib.util
import io
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402

RUNNER = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "runner.py"
)
SCRIPTS = os.path.dirname(RUNNER)
REQUIREMENTS = os.path.join(HERE, "..", "plugin", "requirements.txt")
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

runner = siblings.load(SCRIPTS, os.path.basename(RUNNER))


class GoneProcess(unittest.TestCase):
    def test_an_exited_process_reads_as_empty_432_464(self):
        gone = subprocess.Popen(["true"])
        gone.wait()
        self.assertEqual(runner.process_args(gone.pid), [])
        self.assertEqual(runner.descendants(gone.pid), [])
        self.assertIsNone(runner.driver_pid(gone.pid))


class BrowserPids(unittest.TestCase):
    def alive(self, script):
        proc = subprocess.Popen(
            [
                sys.executable,
                "-c",
                f"import os, time\n{script}print(flush=True)\ntime.sleep({CASE_LIMIT_S})\n",
                "--remote-debugging-pipe",
            ],
            stdout=subprocess.PIPE,
            start_new_session=True,
        )
        self.addCleanup(proc.wait)
        self.addCleanup(lambda: os.killpg(proc.pid, signal.SIGKILL))
        proc.stdout.readline()
        return proc.pid

    def test_a_fork_the_browser_has_not_yet_execd_is_not_a_second_browser_662(self):
        browser = self.alive(
            f"if os.fork() == 0:\n    time.sleep({CASE_LIMIT_S})\n    os._exit(0)\n"
        )
        (fork,) = runner.descendants(browser)
        self.assertIn("--remote-debugging-pipe", runner.process_args(fork))
        self.assertEqual(runner.browser_pids([browser, fork]), [browser])

    def test_two_browsers_neither_the_others_child_are_both_kept_662(self):
        browsers = [self.alive(""), self.alive("")]
        self.assertEqual(runner.browser_pids(browsers), browsers)


def raises(exc):
    def work():
        raise exc

    return work


class RunBrowser(unittest.TestCase):
    def exits(self, work, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            got = runner.run_browser(work, 5000, *args)
        return got, out.getvalue(), err.getvalue()

    def test_a_result_returns_with_no_exit_code(self):
        self.assertEqual(self.exits(lambda: 7, "file:///p.html"), ((7, None), "", ""))

    def test_the_hint_names_the_plugins_pinned_requirements(self):
        self.assertEqual(
            os.path.realpath(runner.REQUIREMENTS), os.path.realpath(REQUIREMENTS)
        )
        self.assertIn(f"-r {runner.REQUIREMENTS}\n", runner.INSTALL_HINT)
        with open(REQUIREMENTS, encoding="utf-8") as f:
            pins = [
                line.split("==")
                for line in f
                if line.strip() and not line.startswith("#")
            ]
        self.assertEqual(
            sorted(name for name, _ in pins),
            ["Pillow", "av", "numpy", "playwright", "scipy"],
        )

    def test_each_failure_exits_with_its_code_and_message_131(self):
        url = "file:///p.html"
        for exc, code, said in [
            (
                ImportError("no playwright"),
                3,
                "Playwright is not importable here.\n" + runner.INSTALL_HINT,
            ),
            (
                runner.NoBrowserError("no chromium"),
                3,
                "its browser is not: no chromium\n" + runner.INSTALL_HINT,
            ),
            (
                runner.RefusedError("net::ERR"),
                5,
                f"the browser could not load {url}: net::ERR",
            ),
            (
                runner.PageTimeoutError("goto"),
                4,
                f"timed out after 5000ms on {url}: goto",
            ),
        ]:
            with self.subTest(exc=exc):
                got, out, err = self.exits(raises(exc), url)
                self.assertEqual(got, (None, code))
                self.assertIn(said, err)
                self.assertEqual(out, "")

    def test_with_no_url_a_refusal_and_a_timeout_name_none(self):
        _, _, err = self.exits(raises(runner.RefusedError("mark.svg: bad image")))
        self.assertEqual(err, "the browser could not draw mark.svg: bad image\n")
        _, _, err = self.exits(raises(runner.PageTimeoutError("decode")))
        self.assertEqual(err, "timed out after 5000ms: decode\n")

    def test_an_unmeasurable_page_prints_its_reasons_between_the_two_lines_on_stdout(
        self,
    ):
        got, out, err = self.exits(
            raises(runner.UnmeasurableError(["a", "b"])), "u", ("head", "tail")
        )
        self.assertEqual((got, out, err), ((None, 6), "head\n  - a\n  - b\ntail\n", ""))

    def test_an_unmeasurable_page_where_the_script_names_no_lines_is_not_swallowed(
        self,
    ):
        with self.assertRaises(runner.UnmeasurableError):
            self.exits(raises(runner.UnmeasurableError(["a"])), "u")


TEST_WINDOW_S = 1  # guess, #459
PAST_WINDOW_S = 2.5  # guess, #432
KILL_POLL_S = 0.05  # guess, #432
CASE_LIMIT_S = 60  # guess, #432
PAUSED_AT_START = ["--renderer-startup-dialog"]


def renderer_pids():
    return [
        pid
        for pid in runner.descendants(os.getpid())
        if "--type=renderer" in runner.process_args(pid)
    ]


@contextlib.contextmanager
def renderers_killed():
    stop = threading.Event()

    def kill():
        while not stop.wait(KILL_POLL_S):
            for pid in renderer_pids():
                with contextlib.suppress(ProcessLookupError):
                    os.kill(pid, signal.SIGTERM)

    killer = threading.Thread(target=kill, daemon=True)
    killer.start()
    try:
        yield
    finally:
        stop.set()
        killer.join()


def renderers_ended():
    end = time.monotonic() + CASE_LIMIT_S
    while running := renderer_pids():
        if time.monotonic() > end:
            raise AssertionError(f"renderers {running} still running")
        for pid in running:
            with contextlib.suppress(ProcessLookupError):
                os.kill(pid, signal.SIGTERM)
        time.sleep(KILL_POLL_S)


def renderers_frozen():
    for pid in renderer_pids():
        os.kill(pid, signal.SIGSTOP)


class HungCalls(unittest.TestCase):
    def exits(self, work):
        done = {}

        def run():
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                done["got"] = runner.run_browser(work, runner.LOAD_TIMEOUT_MS)
            done["err"] = err.getvalue()

        thread = threading.Thread(target=run, daemon=True)
        with mock.patch.multiple(
            runner, RENDERER_GONE_S=TEST_WINDOW_S, UNANSWERED_S=TEST_WINDOW_S
        ):
            thread.start()
            thread.join(CASE_LIMIT_S)
        if thread.is_alive():
            self.fail(f"still waiting after {CASE_LIMIT_S} s: the watch did not fire")
        return done["got"], done["err"]

    def test_a_renderer_killed_as_it_starts_exits_7_naming_the_call_432_472(self):
        def work():
            with runner.chromium(PAUSED_AT_START) as browser:
                browser.new_context().new_page()

        with renderers_killed():
            got, err = self.exits(work)
        self.assertEqual(got, (None, 7), err)
        self.assertRegex(
            err,
            r"^BrowserContext\.new_page at runner\.test\.py:\d+ "
            rf"(waited {TEST_WINDOW_S} s|raised .*) "
            "with the browser running no renderer",
        )

    def test_a_call_waiting_as_its_renderer_dies_exits_7_naming_the_call_432_472(self):
        ran = threading.Event()

        class Seen(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/ran":
                    ran.set()
                self.send_response(200)
                self.end_headers()

            def log_message(self, *args):
                pass

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Seen)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        url = f"http://127.0.0.1:{server.server_port}"

        def kill():
            if ran.wait(CASE_LIMIT_S):
                renderers_ended()

        def work():
            with runner.chromium() as browser:
                page = browser.new_page()
                page.goto(f"{url}/")
                threading.Thread(target=kill, daemon=True).start()
                call["line"] = sys._getframe().f_lineno + 1
                page.evaluate(f"fetch('{url}/ran'); new Promise(() => {{}})")

        call = {}
        got, err = self.exits(work)
        self.assertEqual(got, (None, 7), err)
        self.assertRegex(
            err,
            rf"^Page\.evaluate at runner\.test\.py:{call['line']} "
            rf"waited {TEST_WINDOW_S} s with the browser running no renderer",
        )

    def test_a_call_on_a_page_whose_renderer_died_exits_7_naming_the_call_472(self):
        def work():
            with runner.chromium() as browser:
                page = browser.new_page()
                with page.expect_event("crash"):
                    renderers_ended()
                call["line"] = sys._getframe().f_lineno + 1
                page.evaluate("1 + 1")

        call = {}
        got, err = self.exits(work)
        self.assertEqual(got, (None, 7), err)
        self.assertRegex(
            err,
            rf"^Page\.evaluate at runner\.test\.py:{call['line']} raised .* "
            "with the browser running no renderer",
        )

    def test_a_refused_load_with_its_renderer_alive_exits_5_naming_the_call(self):
        def work():
            with runner.chromium() as browser:
                browser.new_page().goto("http://127.0.0.1:1/")

        got, err = self.exits(work)
        self.assertEqual(got, (None, 5), err)
        self.assertRegex(err, r"^the browser could not draw Page\.goto")

    def test_a_call_after_its_browser_died_exits_5_naming_the_call(self):
        def work():
            with runner.chromium() as browser:
                page = browser.new_page()
                (pid,) = runner.browser_pids(runner.descendants(os.getpid()))
                os.kill(pid, signal.SIGKILL)
                end = time.monotonic() + CASE_LIMIT_S
                while runner.process_args(pid):
                    if time.monotonic() > end:
                        raise AssertionError(f"browser {pid} still running")
                    time.sleep(KILL_POLL_S)
                page.evaluate("1 + 1")

        got, err = self.exits(work)
        self.assertEqual(got, (None, 5), err)
        self.assertRegex(err, r"^the browser could not draw Page\.evaluate")

    def test_a_call_on_a_page_it_closed_exits_5_naming_the_call(self):
        def work():
            with runner.chromium() as browser:
                page = browser.new_page()
                page.close()
                renderers_ended()
                page.evaluate("1 + 1")

        got, err = self.exits(work)
        self.assertEqual(got, (None, 5), err)
        self.assertRegex(err, r"^the browser could not draw Page\.evaluate")

    def test_a_long_call_with_its_renderer_alive_is_left_to_finish(self):
        def work():
            with runner.chromium() as browser:
                page = browser.new_page()
                page.wait_for_timeout(PAST_WINDOW_S * 1000)
                return page.evaluate("1 + 1")

        self.assertEqual(self.exits(work), ((2, None), ""))

    def test_with_no_browser_found_in_proc_it_says_no_watch_runs(self):
        def work():
            with mock.patch.object(runner, "browser_pids", return_value=[]):
                with runner.chromium() as browser:
                    return browser.new_page().evaluate("1 + 1")

        got, err = self.exits(work)
        self.assertEqual(got, (2, None))
        self.assertRegex(err, r"^no call watch: /proc shows 0 new browser processes")

    def test_a_resize_its_live_renderer_never_answers_exits_7_naming_the_call_459(self):
        def work():
            with runner.chromium() as browser:
                page = browser.new_page()
                renderers_frozen()
                page.set_viewport_size({"width": 500, "height": 500})

        got, err = self.exits(work)
        self.assertEqual(got, (None, 7), err)
        self.assertRegex(
            err,
            r"^Page\.set_viewport_size at runner\.test\.py:\d+ "
            rf"waited {TEST_WINDOW_S} s for a renderer that is alive but never answered",
        )

    def test_resizes_one_after_another_past_the_window_are_left_to_finish(self):
        def work():
            with runner.chromium() as browser:
                page = browser.new_page()
                end = time.monotonic() + PAST_WINDOW_S
                width = 400
                while time.monotonic() < end:
                    width = 900 - width
                    page.set_viewport_size({"width": width, "height": 500})
                return page.evaluate("1 + 1")

        self.assertEqual(self.exits(work), ((2, None), ""))

    def test_a_cdp_send_its_live_renderer_never_answers_exits_7_naming_the_call_464(
        self,
    ):
        def work():
            with runner.chromium() as browser:
                page = browser.new_page()
                cdp = page.context.new_cdp_session(page)
                renderers_frozen()
                cdp.send("Page.setFontSizes", {"fontSizes": {"standard": 20}})

        got, err = self.exits(work)
        self.assertEqual(got, (None, 7), err)
        self.assertRegex(
            err,
            r"^CDPSession\.send at runner\.test\.py:\d+ "
            rf"waited {TEST_WINDOW_S} s for a renderer that is alive but never answered",
        )

    def test_a_script_working_with_no_page_open_is_left_to_finish(self):
        def work():
            with runner.chromium() as browser:
                browser.new_page().close()
                time.sleep(PAST_WINDOW_S)
                return browser.new_page().evaluate("1 + 1")

        self.assertEqual(self.exits(work), ((2, None), ""))


class RendererDeath(unittest.TestCase):
    def death(self, method, page_open):
        import greenlet

        package = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, package)
        path = os.path.join(package, "api.py")
        with open(path, "w") as f:
            f.write(
                f"class BrowserContext:\n    def {method}(self):\n"
                "        raise RuntimeError('Target page, context or browser has been closed')\n"
            )
        # #606
        spec = importlib.util.spec_from_file_location("api", path)
        api = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(api)
        browser = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(60)"]
        )
        self.addCleanup(browser.wait)
        self.addCleanup(browser.kill)
        try:
            getattr(api.BrowserContext(), method)()
        except RuntimeError as exc:
            raised = exc
        watch = runner.CallWatch(browser.pid, greenlet.getcurrent(), package + os.sep)
        try:
            return watch.renderer_death(raised, page_open)
        finally:
            watch.stop()

    def test_new_page_raising_with_no_page_open_is_a_renderer_death_472(self):
        self.assertRegex(
            self.death("new_page", page_open=False) or "",
            r"^BrowserContext\.new_page at runner\.test\.py:\d+ raised "
            "'Target page, context or browser has been closed' with the browser running no renderer",
        )

    def test_another_call_raising_with_no_page_open_is_not(self):
        self.assertIsNone(self.death("new_cdp_session", page_open=False))

    def test_another_call_raising_with_a_page_open_is_a_renderer_death_naming_the_call(
        self,
    ):
        self.assertRegex(
            self.death("new_cdp_session", page_open=True) or "",
            r"^BrowserContext\.new_cdp_session at runner\.test\.py:\d+ raised ",
        )


if __name__ == "__main__":
    child.main()
