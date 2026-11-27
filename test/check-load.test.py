import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-load.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "load")


# guess, #170
RUN_TIMEOUT_S = 180
# Lighthouse's mobileSlow4G, devtools-scaled: https://github.com/GoogleChrome/lighthouse/blob/main/core/config/constants.js
ROUND_TRIP_MS = 150 * 3.75
DOWN_BYTES_S = 1.6 * 1024 * 0.9 * 1024 / 8
# guess: 40% past check-load.py's 5 s quiet window, #556
SLOW_LOAD_S = 7
SLOW_LOAD_BYTES = int(DOWN_BYTES_S * SLOW_LOAD_S)


def run(page, *args):
    return child.run(
        [sys.executable, SCRIPT, os.path.join(FIXTURES, page), *args],
        timeout=RUN_TIMEOUT_S,
    )


class Pages(unittest.TestCase):
    def test_content_shown_at_once_passes_after_the_throttled_round_trip_on_lighthouses_phone_170(
        self,
    ):
        proc = run("at-once.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("the median of 3 run(s); limit 2500 ms", proc.stdout)
        ms = [int(line.split()[0]) for line in proc.stdout.splitlines()[2:]]
        self.assertEqual(len(ms), 3)
        self.assertTrue(all(ROUND_TRIP_MS < m < 2500 for m in ms), ms)
        self.assertIn(" ms, h1#w412-h823-x175-moto", proc.stdout)

    def test_a_headline_revealed_3_s_in_fails(self):
        proc = run("late.html", "--runs", "1")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        ms = int(proc.stdout.splitlines()[2].split()[0])
        self.assertGreaterEqual(ms, 3000)
        self.assertIn(" ms, h1#title", proc.stdout)
        self.assertIn("\nover by ", proc.stdout)

    def test_a_headline_revealed_after_a_slow_load_fails(self):  # #154
        scratch = tempfile.mkdtemp(prefix="check-load-")
        self.addCleanup(shutil.rmtree, scratch)
        shutil.copy(os.path.join(FIXTURES, "after-load.html"), scratch)
        with open(os.path.join(scratch, "big.js"), "w") as f:
            f.write("//" + "x" * SLOW_LOAD_BYTES + "\n")
        proc = child.run(
            [
                sys.executable,
                SCRIPT,
                os.path.join(scratch, "after-load.html"),
                "--runs",
                "1",
            ],
            timeout=RUN_TIMEOUT_S,
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
