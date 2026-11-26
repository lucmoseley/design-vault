"""Pins check-state.py (#312): python3 test/check-state.test.py

Loosen the driven-state checks and a page whose tooltip shows on hover
alone, whose slider stops when the pointer leaves it, whose form clears its
answers on an error, or whose toast steals focus passes the gate unseen, as
no static read of a page reaches the states only a visitor drives it into.
"""

import concurrent.futures
import contextlib
import io
import json
import os
import pathlib
import re
import sys
import tempfile
import types
import unittest
from unittest import mock

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-state.py"
)


SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

state = siblings.load(SCRIPTS, "check-state.py")
FIXTURES = pathlib.Path(HERE, "fixtures", "state").resolve()
FAULT = FIXTURES / "tier01-fault.html"
CLEAN = FIXTURES / "tier01-clean.html"
EXEMPT = FIXTURES / "tier01-exempt.html"
with open(state.TABLE, encoding="utf8") as fh:
    TABLE = state.parse(fh.read())
RECORDS = list(dict.fromkeys(line.id for line in TABLE))
PARTS = {
    "editable-value": ".editable",
    "video": ".player",
    "zoomable": ".zoomable",
    "select-all": ".select-all",
    "toast": ".toast",
}
# The record whose fault is the page's own: its timer leaves the page, so its
# miss names no part.
PAGE_FAULTS = {"vault.time-limit"}
# How long one whole-table run may take, in s: a guess, about three times
# the fault page's run on this machine.
CLI_TIMEOUT_S = 2400
RUNS = {}
OPEN = contextlib.ExitStack()


def command(page, out, *extra):
    argv = [sys.executable, SCRIPT, str(page), "--out", str(out), *map(str, extra)]
    for name, selector in PARTS.items():
        argv += ["--part", f"{name}={selector}"]
    return argv


def setUpModule():
    # Each a process of its own, as the command is what a design round runs.
    folder = pathlib.Path(OPEN.enter_context(tempfile.TemporaryDirectory()))
    stale = folder / "fault" / "state.json"
    stale.parent.mkdir()
    stale.write_text("{}")

    def go(name, page):
        done = child.run(command(page, folder / name), timeout=CLI_TIMEOUT_S)
        written = json.loads((folder / name / "state.json").read_text())
        return name, (done.returncode, done.stdout, done.stderr, written)

    with concurrent.futures.ThreadPoolExecutor(2) as pool:
        RUNS.update(pool.map(lambda a: go(*a), (("fault", FAULT), ("clean", CLEAN))))


def tearDownModule():
    OPEN.close()


def found(name):
    return {f["id"]: f for f in RUNS[name][3]["findings"]}


def marked(page):
    return set(re.findall(r'data-fault="([^"]+)"', page.read_text()))


class TheFixtures(unittest.TestCase):
    def test_the_fault_page_plants_one_fault_for_each_record_the_table_checks(self):
        self.assertEqual(marked(FAULT), set(RECORDS))
        self.assertEqual(marked(CLEAN), set())

    def test_every_record_fails_on_the_fault_page_naming_its_own_plant(self):
        got = found("fault")
        for record in RECORDS:
            with self.subTest(record):
                f = got[record]
                self.assertEqual(f["answer"], "fail", f)
                own = record if record not in PAGE_FAULTS else None
                self.assertIn(own, [m["fault"] for m in f["misses"]], f["misses"])

    def test_an_undo_that_restores_nothing_fails_the_press_it_follows(self):
        # #423
        misses = found("fault")["vault.act-on-release"]["misses"]
        self.assertIn(
            'pressing the button "Undo" it shows does not undo it',
            " ".join(m["what"] for m in misses if "#discard" in str(m["where"])),
            misses,
        )

    def test_the_page_s_own_timer_fails_with_no_warning(self):
        (miss,) = found("fault")["vault.time-limit"]["misses"]
        self.assertEqual(miss["where"], None)
        self.assertRegex(
            miss["what"], r"leaves itself 1800 s after load, with no warning"
        )

    def test_the_clean_page_passes_every_record(self):
        got = found("clean")
        self.assertEqual(
            {r: f["answer"] for r, f in got.items()}, dict.fromkeys(RECORDS, "pass")
        )
        for f in got.values():
            self.assertEqual((f["misses"], f["unjudged"]), ([], []), f["id"])
            # axe hands some checks to a person on any page, as aria-controls
            # on a menu trigger; that is review, never a finding (#307).
            for r in f["review"]:
                self.assertRegex(r["what"], r"^axe \S+ could not decide: ", f["id"])

    def test_what_axe_cannot_decide_is_put_to_review_and_the_answer_stays_pass(self):
        f = found("clean")["vault.expanded-state"]
        self.assertEqual(f["answer"], "pass")
        self.assertIn(
            "axe aria-valid-attr-value could not decide",
            " ".join(r["what"] for r in f["review"]),
        )


class TheCommandLine(unittest.TestCase):
    def test_the_fault_page_exits_1_and_replaces_an_earlier_run_s_findings(self):
        code, printed, _, written = RUNS["fault"]
        self.assertEqual(code, 1)
        self.assertEqual(written["answers"], dict.fromkeys(RECORDS, "fail"))
        self.assertEqual(written["url"], FAULT.as_uri())
        for record in RECORDS:
            self.assertIn(f"{record}: fail", printed)

    def test_the_clean_page_exits_0(self):
        code, printed, err, _ = RUNS["clean"]
        self.assertEqual(code, 0, printed + err)

    def run_line(self, page, line, *extra):
        with tempfile.TemporaryDirectory() as out:
            table = pathlib.Path(out, "one.table")
            table.write_text(line + "\n")
            done = child.run(
                command(page, out, "--table", table, *extra),
                timeout=CLI_TIMEOUT_S,
            )
            return done.returncode, done.stdout, done.stderr

    def test_a_bad_table_exits_2(self):
        code, _, err = self.run_line(CLEAN, "vault.a | hover")
        self.assertEqual(code, 2)
        self.assertIn("no check 'hover'; the checks are reveal, persist,", err)

    def test_a_check_given_a_value_it_does_not_read_exits_2(self):
        code, _, err = self.run_line(CLEAN, "vault.a | toggle | 3")
        self.assertEqual(code, 2)
        self.assertIn("toggle reads no value, got '3'", err)

    def test_a_missing_page_exits_2(self):
        code, _, err = self.run_line(FIXTURES / "nowhere.html", "vault.a | toggle")
        self.assertEqual(code, 2)
        self.assertIn("no such file", err)

    def test_an_undeclared_part_leaves_its_record_not_judged(self):
        with tempfile.TemporaryDirectory() as out:
            table = pathlib.Path(out, "one.table")
            table.write_text("vault.editable-cue | editable | part editable-value\n")
            done = child.run(
                [
                    sys.executable,
                    SCRIPT,
                    str(FAULT),
                    "--out",
                    out,
                    "--table",
                    str(table),
                ],
                timeout=CLI_TIMEOUT_S,
            )
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            self.assertIn("vault.editable-cue: not judged", done.stdout)
            self.assertIn(
                "no selector for the part editable-value: declare it in --parts",
                done.stdout,
            )


class TheTableGivesTheValues(unittest.TestCase):
    run_line = TheCommandLine.run_line

    def test_a_looser_target_fill_passes_the_loud_highlight(self):
        code, printed, _ = self.run_line(
            FAULT, "vault.target-highlight | target | fill contrast <= 1.5"
        )
        self.assertEqual(code, 0, printed)
        self.assertIn("vault.target-highlight: pass", printed)

    def test_a_longer_warning_fails_the_minute_s_notice(self):
        code, printed, _ = self.run_line(
            CLEAN,
            "vault.time-limit | time-limit | warn ms >= 70000; horizon ms 72000000",
        )
        self.assertEqual(code, 1, printed)
        self.assertIn("warning only 60 s before", printed)

    def test_a_shorter_horizon_leaves_the_half_hour_limit_unchecked(self):
        code, printed, _ = self.run_line(
            FAULT, "vault.time-limit | time-limit | warn ms >= 20000; horizon ms 60000"
        )
        self.assertEqual(code, 0, printed)
        self.assertIn("vault.time-limit: no match", printed)

    def test_a_zoom_ratio_no_spread_reaches_leaves_the_pinch_not_judged(self):
        code, printed, _ = self.run_line(
            FAULT,
            "vault.pinch-anchor | pinch | part zoomable; zoom ratio >= 100; drift px <= 8",
        )
        self.assertEqual(code, 0, printed)
        self.assertIn("a two-finger spread did not zoom it", printed)

    def test_a_dialog_word_list_without_cancel_passes_the_cancel_default(self):
        code, printed, _ = self.run_line(
            FAULT, "vault.dialog-default | default | not close, no"
        )
        self.assertEqual(code, 0, printed)

    def test_a_record_with_no_line_in_the_table_is_not_checked(self):
        code, printed, _ = self.run_line(FAULT, "vault.toggle-state | toggle")
        self.assertEqual(code, 1, printed)
        self.assertEqual(
            re.findall(r"^(vault\.\S+):", printed, re.M), ["vault.toggle-state"]
        )


class TheRulesExemptions(unittest.TestCase):
    run_line = TheCommandLine.run_line

    def test_a_press_the_release_undoes_or_an_undo_it_offers_restores_passes(self):
        code, printed, _ = self.run_line(
            EXEMPT, "vault.act-on-release | release | undone by undo"
        )
        self.assertEqual(code, 0, printed)
        self.assertIn("vault.act-on-release: pass", printed)
        self.assertNotIn("button#peek", printed)
        self.assertNotIn("button#delete", printed)

    def test_a_delete_whose_press_adds_an_undo_is_no_disclosure(self):
        # #423; pair: the fault page's "More about lists" in
        # test_every_record_fails_on_the_fault_page_naming_its_own_plant
        code, printed, _ = self.run_line(
            EXEMPT, "vault.expanded-state | expanded | axe aria-valid-attr-value"
        )
        self.assertEqual(code, 0, printed)
        self.assertIn("vault.expanded-state: pass", printed)

    def test_a_single_key_a_setting_may_turn_off_is_put_to_review(self):
        code, printed, _ = self.run_line(
            EXEMPT, "vault.key-shortcuts | single-key | turned off by shortcut"
        )
        self.assertEqual(code, 0, printed)
        self.assertIn("vault.key-shortcuts: pass", printed)
        self.assertIn('input#keys "Keyboard shortcuts" may turn it off', printed)

    def test_a_part_the_pointer_cannot_reach_is_not_judged_never_passed(self):
        code, printed, _ = self.run_line(EXEMPT, "vault.hover-reveal | reveal")
        self.assertEqual(code, 0, printed)
        self.assertIn("vault.hover-reveal: not judged", printed)
        self.assertIn('span#covered "Fees": the pointer cannot reach it', printed)

    def test_a_track_click_that_leaves_the_page_fails_and_the_next_slider_is_still_judged(
        self,
    ):
        # #458: the check goes on to the next slider on the page loaded afresh.
        code, printed, _ = self.run_line(EXEMPT, "vault.slider-keys | slider-keys")
        self.assertEqual(code, 1, printed)
        self.assertIn('span "Rooms": a click on its track (leaves the page)', printed)
        self.assertIn('div "Floors": Home, End, ArrowUp', printed)
        self.assertNotIn("the check stopped", printed)

    def test_without_the_setting_s_word_the_single_key_fails(self):
        code, printed, _ = self.run_line(
            EXEMPT, "vault.key-shortcuts | single-key | turned off by hotkey"
        )
        self.assertEqual(code, 1, printed)


class OneCheckStopping(unittest.TestCase):
    def test_a_check_that_stops_is_said_as_not_judged_and_printed(self):
        from playwright.sync_api import Error as PlaywrightError

        def stops(run, line, ans):
            raise PlaywrightError("Target closed")

        table = state.parse("vault.a | reveal\n")
        run = types.SimpleNamespace(popups=[])
        err = io.StringIO()
        with (
            mock.patch.dict(state.RUNS, {"reveal": stops}),
            contextlib.redirect_stderr(err),
        ):
            (found,) = state.findings(run, table)
        self.assertIn("the check stopped: Target closed", json.dumps(found))
        self.assertEqual(
            err.getvalue(),
            "fail-open: reveal is said as not judged: Error: Target closed\n",
        )


class TheTableForm(unittest.TestCase):
    def test_each_value_is_read_into_its_kind(self):
        (line,) = state.parse(
            "vault.a | pinch | part zoomable; zoom ratio >= 1.05; drift px <= 8"
        )
        self.assertEqual(line.value, {"part": "zoomable", "zoom": 1.05, "px": 8.0})
        (line,) = state.parse(
            "vault.a | suggest | type a; axe aria-required-attr aria-valid-attr-value"
        )
        self.assertEqual(
            line.value,
            {"text": "a", "rules": ("aria-required-attr", "aria-valid-attr-value")},
        )
        (line,) = state.parse("vault.a | default | not Cancel, not now")
        self.assertEqual(line.value, {"words": ["cancel", "not now"]})

    def test_a_malformed_line_is_refused(self):
        for text, why in (
            ("vault.a", "want ID | CHECK [| VALUE]"),
            ("vault.a | persist", "persist wants a value like"),
            ("vault.a | persist | stays ms > 3000", "persist wants a value like"),
            ("# only a comment", "the table has no lines"),
        ):
            with self.subTest(text):
                with self.assertRaisesRegex(state.TableError, re.escape(why)):
                    state.parse(text)


if __name__ == "__main__":
    child.main()
