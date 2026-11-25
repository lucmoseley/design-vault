"""Tests plugin/skills/design-round/scripts/check-measure.py (#86): python3 test/check-measure.test.py

The pages are synthetic, in test/fixtures/measure/: monospace, set in `ch`, of
four-letter words, so a line of N ch holds a known count. Loosen one and a
critic's Measure lens (design-critique §2) passes body text set too wide or too
narrow, or fails a page for its headings and last lines.
"""

import argparse
import contextlib
import importlib.util
import io
import os
import pathlib
import re
import sys
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-measure.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "measure")
spec = importlib.util.spec_from_file_location("check_measure", SCRIPT)
measure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(measure)


def run(page, *args):
    # A guess for check-measure.py alone, not taken from the other tests' timeouts: one run takes seconds here.
    return child.run(
        [sys.executable, SCRIPT, os.path.join(FIXTURES, page), *args],
        timeout=180,
    )


class Lines(unittest.TestCase):
    def test_full_lines_in_range_pass_and_the_rest_is_not_running_text(self):
        # Headings, nav, tables, pre, hidden and clipped text, last lines, a
        # line a <br> ends and a one-line block would each add a count outside
        # 59; inline code left out would set one short.
        proc = run("ok.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(
            "\n320px: 59 characters, 25 full lines in 5 block(s) — all in range",
            proc.stdout,
        )
        self.assertIn(
            "\n2560px: 59 characters, 25 full lines in 5 block(s) — all in range",
            proc.stdout,
        )

    def test_a_line_that_is_not_full_still_fails_over_the_maximum(self):
        proc = run("one-line.html", "--widths", "1920")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(
            "\n1920px: no full line of running text — 2 block(s) out of range\n"
            "  p:nth-of-type(1) (16px): 1 line(s) at 99 characters",
            proc.stdout,
        )

    def test_lines_too_long_fail_and_are_quoted(self):
        proc = run("wide.html")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(
            "\n320px: 89 characters, 3 full lines in 1 block(s) — 1 block(s) out of range\n  p (16px): 3 line(s) at 89 characters\n    89: “abcd abcd",
            proc.stdout,
        )

    def test_lines_too_short_fail_and_the_rest_are_counted(self):
        proc = run("narrow.html")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("  p (16px): 10 line(s) at 29 characters\n", proc.stdout)
        self.assertIn("\n    and 7 more\n", proc.stdout)

    def test_the_range_is_set_by_min_and_max(self):
        proc = run("wide.html", "--max", "90")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("range 50–90 characters", proc.stdout)

    def test_a_soft_hyphen_within_a_line_is_not_a_character(self):
        proc = run("shy-within.html", "--widths", "1440")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(
            "\n1440px: 59 characters, 5 full lines in 1 block(s)", proc.stdout
        )

    def test_a_line_broken_at_a_soft_hyphen_ends_with_it_and_keeps_its_letters(self):
        proc = run("shy-break.html", "--widths", "1440", "--max", "63")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(
            "\n1440px: 62–63 characters, 4 full lines in 1 block(s)", proc.stdout
        )

    def test_phone_widths_count_the_lines_a_touch_screen_sets(self):
        # The text doubles under (pointer: coarse): 29 characters through the
        # phone band, 59 from 768 px, where the touch screen ends (#230).
        proc = run("touch.html")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("breakpoints: 768px\n", proc.stdout)
        for w in (320, 767):
            self.assertIn(
                f"\n{w}px: 29 characters, 10 full lines in 1 block(s) — 1 block(s) out of range\n"
                "  div > p (32px): 10 line(s) at 29 characters\n",
                proc.stdout,
            )
        for w in (768, 2560):
            self.assertIn(
                f"\n{w}px: 59 characters, 5 full lines in 1 block(s) — all in range",
                proc.stdout,
            )

    def test_a_page_with_no_running_text_says_to_skip_the_lens(self):
        proc = run("none.html")
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(
            "\n320px: no full line of running text\n2560px: no full line of running text\n",
            proc.stdout,
        )
        self.assertIn("skip the Measure lens, and say so", proc.stdout)


class Breakpoints(unittest.TestCase):
    def test_both_sides_of_a_min_width_breakpoint_are_rendered(self):
        proc = run("breakpoint.html")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("breakpoints: 1000px\n", proc.stdout)
        self.assertIn(
            "\n999px: 59 characters, 5 full lines in 1 block(s) — all in range",
            proc.stdout,
        )
        self.assertIn(
            "\n1000px: 89 characters, 3 full lines in 1 block(s) — 1 block(s) out of range",
            proc.stdout,
        )

    def test_a_range_query_in_em_is_read(self):
        proc = run("range.html")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("breakpoints: 640px\n", proc.stdout)
        self.assertIn("\n639px: 29 characters", proc.stdout)
        self.assertIn("\n640px: 59 characters", proc.stdout)

    def test_a_linked_stylesheets_breakpoints_are_read(self):
        proc = run("linked.html")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("breakpoints: 800px\n", proc.stdout)
        self.assertNotIn("UNREAD", proc.stdout)
        self.assertIn("\n799px: 29 characters", proc.stdout)

    def test_widths_given_replace_the_breakpoints(self):
        proc = run("breakpoint.html", "--widths", "1440,390")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("widths given: 390, 1440\n", proc.stdout)
        self.assertIn("\n390px: 59 characters", proc.stdout)
        self.assertNotIn("\n320px", proc.stdout)

    def test_each_query_form_starts_its_range_where_it_applies(self):
        self.assertEqual(
            measure.range_starts(
                [
                    "(min-width: 600px)",
                    "(max-width: 799.98px)",
                    "screen and (min-width: 62.5em)",
                    "(width >= 300px)",
                    "(width > 400px)",
                    "(width < 500px)",
                    "(width <= 700px)",
                    "(900px <= width)",
                    "(1100px < width)",
                    "(1200px > width)",
                    "(1300px >= width)",
                    "(min-width: 30rem)",
                    "print",
                    "(min-height: 999px)",
                    "(max-width: 1023px)",
                    "(min-device-width: 1400px)",
                ]
            ),
            {
                600,
                800,
                1000,
                300,
                401,
                500,
                701,
                900,
                1101,
                1200,
                1301,
                480,
                1024,
                1400,
            },
        )

    def test_widths_are_both_ends_of_each_range_within_320_to_2560(self):
        self.assertEqual(
            measure.widths({1000, 640, 200, 2600, 2560}),
            [320, 639, 640, 999, 1000, 2559, 2560],
        )
        self.assertEqual(measure.widths(set()), [320, 2560])

    def test_a_sheets_own_text_yields_its_media_conditions(self):
        css = "p{x:y} @media (min-width: 40em) { p { a: b } } @media print{} @import url(x.css) screen;"
        self.assertEqual(
            [m.strip() for m in measure.AT_MEDIA.findall(css)],
            ["(min-width: 40em)", "print"],
        )

    def test_a_sheet_that_cannot_be_fetched_is_named_with_the_way_round_it(self):
        # Unverified end to end: no fixture makes a sheet both unreadable to the
        # page and unfetchable, so fetch() and report() are checked apart.
        missing = pathlib.Path(FIXTURES, "missing.css").resolve().as_uri()
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertIsNone(measure.fetch(None, missing))
        self.assertRegex(
            err.getvalue(),
            rf"^fail-open: {re.escape(missing)} is left unread: FileNotFoundError: ",
        )
        at = argparse.Namespace(url="u", min=50, max=75, widths=None)
        out = measure.report(
            at, {"starts": set(), "unread": ["https://cdn.example/site.css"]}, []
        )
        self.assertIn(
            "\n  UNREAD stylesheet https://cdn.example/site.css: its breakpoints are unknown; add its widths with --widths",
            out,
        )


class Arguments(unittest.TestCase):
    def usage(self, *args):
        proc = run(*args)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        return proc.stderr

    def test_a_missing_file_and_a_bad_range_are_usage_errors_that_name_the_fault(self):
        self.assertIn("no such file: ", self.usage("nothing.html"))
        self.assertIn(
            "--min 80 and --max 70 make no range",
            self.usage("ok.html", "--min", "80", "--max", "70"),
        )
        self.assertIn(
            "--widths wants whole px, e.g. 390,1440 — got 'wide'",
            self.usage("ok.html", "--widths", "wide"),
        )
        self.assertIn(
            "--widths wants widths above 0", self.usage("ok.html", "--widths", "0,390")
        )


if __name__ == "__main__":
    child.main()
