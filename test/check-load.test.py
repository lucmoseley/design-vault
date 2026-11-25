"""Tests plugin/skills/design-round/scripts/check-load.py (#170): python3 test/check-load.test.py

Lose the throttling and every local page passes in a few ms; stop waiting for
a later paint and a headline held back passes on whatever drew first.
"""

import importlib.util
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-load.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "load")
spec = importlib.util.spec_from_file_location("check_load", SCRIPT)
load = importlib.util.module_from_spec(spec)
spec.loader.exec_module(load)


def run(page, *args):
    # A guess for check-load.py alone: a run takes about QUIET_MS plus the load.
    return child.run(
        [sys.executable, SCRIPT, os.path.join(FIXTURES, page), *args],
        timeout=180,
    )


class Profile(unittest.TestCase):
    def test_the_network_is_lighthouses_scaled_slow_4g_in_bytes_per_second(self):
        self.assertEqual(load.LATENCY_MS, 562.5)
        self.assertAlmostEqual(load.DOWN_BYTES, 188743.68)
        self.assertAlmostEqual(load.UP_BYTES, 86400)
        self.assertEqual((load.CPU_SLOWDOWN, load.SCALE), (4, 1.75))
        self.assertEqual(load.SCREEN, {"width": 412, "height": 823})


class Pages(unittest.TestCase):
    def test_content_shown_at_once_passes_after_the_throttled_round_trip(self):
        proc = run("at-once.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("the median of 3 run(s); limit 2500 ms", proc.stdout)
        ms = [int(line.split()[0]) for line in proc.stdout.splitlines()[2:]]
        self.assertEqual(len(ms), 3)
        # One throttled round trip alone is 562.5 ms, so a lower LCP was not throttled.
        self.assertTrue(all(562 < m < 2500 for m in ms), ms)
        self.assertIn(" ms, h1#title", proc.stdout)

    def test_a_headline_revealed_3_s_in_fails(self):
        proc = run("late.html", "--runs", "1")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        ms = int(proc.stdout.splitlines()[2].split()[0])
        self.assertGreaterEqual(ms, 3000)
        self.assertIn(" ms, h1#title", proc.stdout)
        self.assertIn("\nover by ", proc.stdout)

    def test_a_headline_revealed_after_a_slow_load_fails(self):
        # The load ends past QUIET_MS on the throttled network, so the quiet
        # wait counts from the load, never from the early nav line.
        scratch = tempfile.mkdtemp(prefix="check-load-")
        self.addCleanup(shutil.rmtree, scratch)
        shutil.copy(os.path.join(FIXTURES, "after-load.html"), scratch)
        with open(os.path.join(scratch, "big.js"), "w") as f:
            f.write("//" + "x" * 1_300_000 + "\n")
        proc = child.run(
            [
                sys.executable,
                SCRIPT,
                os.path.join(scratch, "after-load.html"),
                "--runs",
                "1",
            ],
            timeout=180,
        )
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(" ms, h1#title", proc.stdout)

    def test_a_page_that_draws_nothing_is_unmeasurable(self):
        proc = run("blank.html", "--runs", "1")
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn("drew no LCP element", proc.stdout)

    def test_no_runs_is_a_usage_error(self):
        proc = run("at-once.html", "--runs", "0")
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("--runs wants 1 or more", proc.stderr)


if __name__ == "__main__":
    child.main()
