"""Tests check-flow.py --records and motion-records.py (#318): python3 test/check-flow-records.test.py

Each record check's judgement and the flash analysis are tested on synthetic
readings, so each threshold is pinned without a browser; then one run over
test/fixtures/flow/tier01-fault.html names every planted fault, one per
record, and one over tier01-clean.html names none. vault.pause, which
check-access.py answers, is run on both pages through its own pause_answer.
--records with numpy or Pillow shadowed by a package that will not import
exits 3 before any browser starts, naming it.
A break here means a design round's motion records answer wrongly: a page
that scrolljacks, strobes or replays its parallax passes, or a clean one fails.
"""

import concurrent.futures
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

import numpy as np

HERE = os.path.dirname(__file__)
CHILD = importlib.util.spec_from_file_location("child", os.path.join(HERE, "child.py"))
child = importlib.util.module_from_spec(CHILD)
CHILD.loader.exec_module(child)
RECORDS = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "motion-records.py"
)
FLOW = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-flow.py"
)
ACCESS = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-access.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "flow")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


records = load("motion_records", RECORDS)
flow = load("check_flow", FLOW)
with open(flow.TABLE, encoding="utf8") as fh:
    LINES = records.parse_table(fh.read())
V = {line.mode: line.value for line in LINES}


# How long a --records run that exits before any browser starts may take, in
# s: a guess, far past the under 1 s it takes on this machine (2026-11-20).
SHADOWED_TIMEOUT_S = 60


class Table(unittest.TestCase):
    def test_every_check_has_a_line_and_a_run(self):
        self.assertEqual({line.mode for line in LINES}, set(records.CHECKS))
        self.assertEqual(set(flow.RUNS), set(records.CHECKS))

    def test_values_are_the_records_figures(self):
        self.assertEqual(V["frequent"], {"under": 150})
        self.assertEqual(V["carousel"]["least"], 5)
        self.assertEqual(V["carousel"]["wps"], 3)
        self.assertEqual(V["carousel"]["phone"], 600)
        self.assertEqual(
            (V["flash"]["field_w"], V["flash"]["field_h"], V["flash"]["share"]),
            (341, 256, 0.25),
        )

    def test_a_malformed_line_is_refused(self):
        for bad in (
            "vault.x | frequent | over 150",
            "vault.x | nosuch | none",
            "vault.x | frequent",
            "vault.parallax | replay | none",
        ):
            with self.subTest(bad=bad), self.assertRaises(records.TableError):
                records.parse_table(bad)

    def test_a_bad_parts_or_table_flag_is_a_usage_error(self):
        bad = os.path.join(FIXTURES, "nosuch.table")
        for argv in (
            ["page.html", "--out", "o", "--parts", "p.json"],
            ["page.html", "--out", "o", "--records", "--table", bad],
        ):
            with (
                self.subTest(argv=argv),
                contextlib.redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit) as caught,
            ):
                flow.parse(argv)
            self.assertEqual(caught.exception.code, 2)

    def test_records_without_numpy_or_pillow_exit_3_naming_it_and_its_install_477(
        self,
    ):
        # #477 (run_browser() read the ImportError as Playwright's); its
        # positive pair is the Pages runs, which find both installed.
        for package in ("numpy", "PIL"):
            with self.subTest(package=package):
                done = self.shadowed(package)
                self.assertEqual(done.returncode, 3, done.stderr)
                self.assertIn(
                    f"{package} is missing — python3 -m pip install -r", done.stderr
                )

    def shadowed(self, package):
        """check-flow.py --records run with `package` shadowed on PYTHONPATH by
        one that will not import: an installed package cannot be removed for
        one test, so the shadow stands in for its absence."""
        with tempfile.TemporaryDirectory() as shadow:
            os.mkdir(os.path.join(shadow, package))
            with open(os.path.join(shadow, package, "__init__.py"), "w") as fh:
                fh.write(f"raise ImportError('shadowed', name={package!r})\n")
            return subprocess.run(
                [
                    sys.executable,
                    FLOW,
                    os.path.join(FIXTURES, "tier01-clean.html"),
                    "--out",
                    shadow,
                    "--records",
                ],
                capture_output=True,
                check=False,
                text=True,
                timeout=SHADOWED_TIMEOUT_S,
                env={**os.environ, "PYTHONPATH": shadow},
            )

    def test_a_check_needing_a_part_is_unmet_without_it(self):
        self.assertIn("carousel", records.missing("carousel", {}))
        self.assertIsNone(records.missing("carousel", {"carousel": ".c"}))


class Judgements(unittest.TestCase):
    def scrolls(self, **over):
        still = {"before": 0, "after": 0, "room": 500, "cancelled": ""}
        got = {
            "wheel": {**still, "after": 100},
            "key": {**still, "after": 400},
            "touch": {**still, "after": 120},
        }
        for name, read in over.items():
            got[name] = {**got[name], **read}
        return records.native_scroll_faults(got, V["native-scroll"])

    def test_a_native_scroll_by_wheel_key_and_touch_passes(self):
        self.assertEqual(self.scrolls(), [])
        self.assertEqual(self.scrolls(wheel={"after": 101}), [])

    def test_a_cancelled_or_misjudged_scroll_fails_naming_the_way_out(self):
        cancel = "drop the handler's preventDefault()"
        for name, read, words, fix in (
            (
                "wheel",
                {"after": 160},
                "moves the page 160 px",
                "by the wheel's own distance",
            ),
            ("wheel", {"cancelled": "wheel"}, "cancels the wheel turn", cancel),
            ("key", {"cancelled": "keydown PageDown"}, "cancels the Page Down", cancel),
            ("touch", {"cancelled": "touchmove"}, "cancels the touch drag", cancel),
            (
                "key",
                {"after": 0},
                "Page Down does not scroll",
                "let the browser scroll",
            ),
            (
                "touch",
                {"after": 0},
                "touch drag does not scroll",
                "let the browser scroll",
            ),
        ):
            with self.subTest(name=name, read=read):
                faults = self.scrolls(**{name: read})
                self.assertEqual(len(faults), 1)
                self.assertIn(words, faults[0]["detail"])
                self.assertIn(fix, faults[0]["fix"])

    def test_a_page_with_no_room_to_scroll_is_not_judged(self):
        none = {"room": 0, "after": 0}
        self.assertIsNone(self.scrolls(wheel=none, key=none, touch=none))

    def test_a_key_or_touch_scroll_is_judged_where_a_wheel_turn_has_no_room(self):
        self.assertEqual(self.scrolls(wheel={"room": 50, "after": 0}), [])
        short = {"room": 50, "after": 0}
        self.assertEqual(len(self.scrolls(wheel=short, key=short, touch=short)), 2)

    def track(self, kind, rate, steps):
        scrolls = [k * 100 for k in range(steps + 1)]
        return {
            "scrolls": scrolls,
            "elements": [
                {"label": "x", "kind": kind, "tops": [500 + rate * s for s in scrolls]}
            ],
        }

    def test_parallax_text_fails_and_an_image_passes(self):
        v = V["parallax"]
        need = int(v["steps"])
        faults, seen = records.parallax_faults(self.track("text", -0.6, need), v)
        self.assertEqual((len(faults), seen), (1, ["x"]))
        faults, seen = records.parallax_faults(self.track("image", -0.6, need), v)
        self.assertEqual((faults, seen), ([], ["x"]))

    def test_parallax_needs_its_run_of_steps(self):
        v = V["parallax"]
        faults, seen = records.parallax_faults(
            self.track("text", -0.6, int(v["steps"]) - 1), v
        )
        self.assertEqual((faults, seen), ([], []))
        for rate in (-1, 0, -1 + v["slack"] / 2):
            with self.subTest(rate=rate):
                self.assertEqual(
                    records.parallax_faults(self.track("text", rate, 10), v), ([], [])
                )

    def test_a_parallax_layer_that_animates_on_a_second_pass_replays(self):
        first = {"a": ["opacity"], "b": ["x"], "c": ["y"]}
        again = {"a": ["opacity"], "c": ["y"]}
        faults = records.replay_faults(first, again, ["a", "b"])
        self.assertEqual([f["subject"] for f in faults], ["a"])
        self.assertEqual(records.replay_faults({"a": ["opacity"]}, {}, ["a"]), [])

    def test_a_layer_smoothing_its_own_scroll_motion_is_no_replay(self):
        both = {"a": ["transform", "translate", "top"]}
        self.assertEqual(records.replay_faults(both, both, ["a"]), [])
        # An opacity first run on the second sweep is no replay of the first.
        later = {"a": ["transform", "opacity"]}
        self.assertEqual(records.replay_faults(both, later, ["a"]), [])

    def test_motion_the_clock_starts_is_no_replay(self):
        ran = {
            "down": {"a": ["opacity"], "tick": ["opacity"]},
            "idle": {"tick": ["opacity"]},
            "again": {"a": ["opacity"], "tick": ["opacity"]},
        }
        self.assertEqual(records.replays(ran), ({"a": ["opacity"]}, {"a": ["opacity"]}))

    def carousel(self, **over):
        got = {
            "label": ".c",
            "phone_advances": False,
            "phone_width": 390,
            "frames": [
                {"from": 0, "words": 2},
                {"from": 5000, "words": 30},
                {"from": 15000, "words": 2},
            ],
            "hovered": False,
            "focused": False,
            "after_change": False,
            "control": "button",
        }
        return records.carousel_faults({**got, **over}, V["carousel"], 0.1)

    def test_a_frame_held_under_its_words_time_fails(self):
        self.assertEqual(self.carousel(), [])
        short = [
            {"from": 0, "words": 2},
            {"from": 5000, "words": 30},
            {"from": 14000, "words": 2},
        ]
        self.assertIn("30-word", self.carousel(frames=short)[0]["detail"])
        self.assertIn(
            "2-word",
            self.carousel(frames=[{"from": 0, "words": 2}, {"from": 4800, "words": 2}])[
                0
            ]["detail"],
        )

    def test_a_carousel_advancing_on_a_phone_hovered_focused_or_after_a_change_fails_once_each(
        self,
    ):
        for key in ("phone_advances", "hovered", "focused", "after_change"):
            with self.subTest(key=key):
                self.assertEqual(len(self.carousel(**{key: True})), 1)

    def test_the_loads_must_sit_either_side_of_the_phone_width(self):
        v = V["carousel"]
        self.assertIsNone(records.carousel_widths(390, 1920, v))
        self.assertIn("phone load", records.carousel_widths(600, 1920, v))
        self.assertIn("--viewport", records.carousel_widths(390, 599, v))

    def test_a_carousel_that_never_advances_has_only_its_phone_fault(self):
        self.assertEqual(
            self.carousel(frames=[{"from": 0, "words": 2}], hovered=True), []
        )

    def drag(self, end, path=None, velocity=-1000):
        got = {
            "label": "card",
            "snaps": [0, 300],
            "fling": {
                "at": 260,
                "velocity": velocity,
                "path": path or [260, 200, 100, end],
            },
        }
        return records.drag_faults(got, V["drag-release"])

    def test_drag_settles_where_its_projection_picks(self):
        self.assertAlmostEqual(records.projected(260, -1000, 0.998), 260 - 499)
        self.assertEqual(self.drag(0), [])
        missed = self.drag(300, [260, 280, 300])[0]
        self.assertIn("projection", missed["detail"])
        self.assertEqual(
            missed["fix"], "settle on the snap point nearest its projection, 0 px"
        )

    def test_rests_within_slack_count_as_one_snap_point(self):
        self.assertEqual(
            records.snap_points([300, 0, 1, 299.5, 150], 2), [0, 150, 299.5]
        )

    def test_a_fling_heads_for_the_farther_snap_point(self):
        self.assertEqual(records.fling_way([0, 300], 40), 1)
        self.assertEqual(records.fling_way([0, 300], 260), -1)

    def test_pointer_velocity_is_along_its_axis_and_zero_over_no_time(self):
        moves = [[0, 10, 50], [50, 30, 40]]
        self.assertEqual(records.pointer_velocity(moves, "left"), 400)
        self.assertEqual(records.pointer_velocity(moves, "top"), -200)
        self.assertEqual(records.pointer_velocity([[5, 0, 0], [5, 9, 9]], "top"), 0)

    def test_a_release_that_overshoots_or_turns_back_fails_naming_the_bounce_or_the_turn(
        self,
    ):
        bounce = self.drag(0, [260, 100, -20, 0])[0]
        self.assertIn("bounce", bounce["detail"])
        self.assertIn("no bounce", bounce["fix"])
        turned = self.drag(300, [260, 260, 290, 300], velocity=1000)
        self.assertEqual(turned, [])
        back = self.drag(0, [260, 260, 290, 150, 0])[0]
        self.assertIn("turns back", back["detail"])
        self.assertEqual(back["fix"], "start the settle from the release velocity")

    def test_hover_or_press_motion_of_150_ms_or_more_fails(self):
        v = V["frequent"]
        faults = records.frequent_faults(
            [
                {"label": "a", "state": "hover", "motion": records.ENDS, "ms": 149},
                {"label": "b", "state": "press", "motion": records.ENDS, "ms": 150},
                {"label": "c", "state": "hover", "motion": records.ENDLESS},
            ],
            v,
        )
        self.assertEqual([f["subject"] for f in faults], ["b", "c"])

    def test_each_rule_and_script_animation_outside_update_fast_fails(self):
        got = {
            "rules": [{"where": "s: .a", "sets": "transition opacity"}],
            "scripted": [{"label": "div"}],
        }
        self.assertEqual(len(records.slow_update_faults(got)), 2)

    def test_a_fault_outranks_not_judged_which_outranks_a_pass(self):
        lines = [
            records.Line("r1", "frequent", None),
            records.Line("r2", "carousel", None),
            records.Line("r3", "flash", None),
            records.Line("r4", "slow-update", None),
        ]
        answer = records.Answer
        got = records.answers(
            lines,
            {
                "frequent": answer([1], True, None),
                "carousel": answer(None, False, "why"),
                "flash": answer([], True, None),
                "slow-update": answer([], False, None),
            },
        )
        self.assertEqual(
            got, {"r1": "fail", "r2": "not judged", "r3": "pass", "r4": "no match"}
        )
        # A record with one check seen and one that could not judge is not judged.
        both = [
            records.Line("r5", "parallax", None),
            records.Line("r5", "replay", None),
        ]
        self.assertEqual(
            records.answers(
                both,
                {
                    "parallax": answer([], True, None),
                    "replay": answer(None, False, "why"),
                },
            ),
            {"r5": "not judged"},
        )


def strobe(hz, *, seconds=2, size=(48, 64), fps=60, colours=((0, 0, 0), (1, 1, 1))):
    t = np.arange(0, seconds, 1 / fps)
    on = (t * hz * 2).astype(int) % 2
    rgb = np.empty((len(t), *size, 3))
    rgb[on == 0], rgb[on == 1] = colours
    return rgb, t


class Flash(unittest.TestCase):
    v = V["flash"]

    def test_three_flashes_a_second_pass_and_more_fail(self):
        # 3.5 a second is seven transitions in each window: the first count over three flashes.
        for hz, fails in ((3, False), (3.5, True), (10, True)):
            with self.subTest(hz=hz):
                self.assertEqual(
                    bool(records.flash_faults(*strobe(hz), 16, self.v)), fails
                )

    def test_a_small_change_is_no_transition(self):
        rgb, t = strobe(10, colours=((0.5, 0.5, 0.5), (0.55, 0.55, 0.55)))
        self.assertEqual(records.flash_faults(rgb, t, 16, self.v), [])

    def test_a_flash_between_two_bright_states_is_none(self):
        rgb, t = strobe(10, colours=((0.92, 0.92, 0.92), (1, 1, 1)))
        self.assertEqual(records.flash_faults(rgb, t, 16, self.v), [])

    def test_a_saturated_red_flash_with_little_luminance_change_fails_as_a_red_flash(
        self,
    ):
        # Red and blue: far apart in u′v′, under 0.1 apart in luminance.
        rgb, t = strobe(10, colours=((0.8, 0, 0), (0, 0, 0.8)))
        self.assertEqual(
            {f["kind"] for f in records.flash_faults(rgb, t, 16, self.v)}, {"red"}
        )

    def test_a_flash_under_a_quarter_of_the_field_passes(self):
        px = 4
        fh, fw = round(self.v["field_h"] / px), round(self.v["field_w"] / px)
        side = int((self.v["share"] * fh * fw) ** 0.5)
        for n, fails in ((side - 1, False), (side + 2, True)):
            rgb, t = strobe(10, size=(fh, fw))
            rgb[:, n:, :] = 0
            rgb[:, :, n:] = 0
            with self.subTest(n=n):
                self.assertEqual(bool(records.flash_faults(rgb, t, px, self.v)), fails)


def table_of(where, *checks):
    """A table of check-flow.table's own lines for `checks` alone, so a test of
    one check runs only that one."""
    path = os.path.join(where, "-".join(checks) + ".table")
    with (
        open(flow.TABLE, encoding="utf8") as src,
        open(path, "w", encoding="utf8") as fh,
    ):
        for raw in src:
            fields = raw.split("|")
            if (
                not raw.lstrip().startswith("#")
                and len(fields) == 3
                and fields[1].strip() in checks
            ):
                fh.write(raw)
    return path


# How long one page's run may take, in s: a guess, about three times the
# fault page's whole-table run on this machine (81 s, 2026-11-19).
RUN_TIMEOUT_S = 240


def run(page, out, *extra):
    """check-flow.py --records on `page` as a child: its exit code, its
    records and its stdout."""
    done = child.run(
        [
            sys.executable,
            FLOW,
            page,
            "--out",
            out,
            "--records",
            "--parts",
            os.path.join(FIXTURES, "tier01-parts.json"),
            *extra,
        ],
        timeout=RUN_TIMEOUT_S,
    )
    with open(os.path.join(out, "motion.json"), encoding="utf8") as fh:
        return done.returncode, json.load(fh)["records"], done.stdout


# Each record's plant on the fault page, by the subject its fault names.
PLANTS = {
    "vault.native-scroll": ["the page"],
    "vault.parallax": ["h2.drift", "div.layer.reveal"],
    "vault.carousel-timing": [".carousel"],
    "vault.flash-limit": ["div.strobe"],
    "vault.drag-release": [".card"],
    "vault.motion-frequency": ["button.buy"],
    "vault.slow-update": [".note"],
}


# Each record's way out for its plants on the fault page, as its output
# prints it.
FIXES = {
    "vault.native-scroll": ["drop the handler's preventDefault()"],
    "vault.parallax": [
        "scroll the text at the page's own speed",
        "run it once and leave it at its end state",
    ],
    "vault.carousel-timing": [
        "turn auto-advance off under 600 px",
        "hold each frame 5 s or its words ÷ 3 s",
        "pause it while hovered",
        "pause it while focused",
        "stop auto-advancing once the visitor changes frame",
    ],
    "vault.flash-limit": ["flash at most 3 times in any second"],
    # Which of the card's faults its fling meets turns on the fling's speed,
    # so their fixes are pinned in Judgements.
    "vault.drag-release": [],
    "vault.motion-frequency": ["end it under 150 ms, or drop it"],
    "vault.slow-update": ["move it inside @media (update: fast)"],
}


class Pages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Every page's run, two at a time: each spends most of its time
        waiting on the page's own clock, not on the machine."""
        cls.tmp = tempfile.TemporaryDirectory()
        where = cls.tmp.name
        runs = {
            "fault": (os.path.join(FIXTURES, "tier01-fault.html"),),
            "clean": (os.path.join(FIXTURES, "tier01-clean.html"),),
            "keys": (
                os.path.join(FIXTURES, "scrolljack-keys.html"),
                "--table",
                table_of(where, "native-scroll"),
            ),
            "map": (
                os.path.join(FIXTURES, "touch-map.html"),
                "--table",
                table_of(where, "native-scroll"),
            ),
            "narrow": (
                os.path.join(FIXTURES, "tier01-clean.html"),
                "--viewport",
                "500x800",
                "--table",
                table_of(where, "carousel"),
            ),
            "slow": (
                os.path.join(FIXTURES, "slow-script.html"),
                "--table",
                table_of(where, "slow-update"),
            ),
        }

        def go(name):
            page, *extra = runs[name]
            return name, run(page, os.path.join(where, name), *extra)

        with concurrent.futures.ThreadPoolExecutor(2) as pool:
            cls.runs = dict(pool.map(go, runs))
        cls.fault, cls.clean = cls.runs["fault"], cls.runs["clean"]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_the_fault_page_names_every_plant(self):
        code, got, out = self.fault
        self.assertEqual(code, 1, out)
        self.assertEqual(set(got), set(PLANTS))
        for rid, subjects in PLANTS.items():
            with self.subTest(record=rid):
                self.assertEqual(got[rid]["answer"], "fail", out)
                for s in subjects:
                    self.assertTrue(
                        any(s in f["subject"] for f in got[rid]["faults"]),
                        f"{rid} missed {s}: {out}",
                    )

    def test_the_fault_page_prints_each_fault_with_its_way_out(self):
        _, got, out = self.fault
        for rid, fixes in FIXES.items():
            with self.subTest(record=rid):
                printed = [
                    f"{f['subject']}: {f['detail']}. Fix: {f['fix']}."
                    for f in got[rid]["faults"]
                ]
                for line in printed:
                    self.assertIn(line, out)
                for fix in fixes:
                    self.assertTrue(
                        any(f"Fix: {fix}" in line for line in printed),
                        f"{rid} printed no {fix!r}: {out}",
                    )

    def test_the_fault_page_names_each_carousel_fault(self):
        details = " | ".join(
            f["detail"] for f in self.fault[1]["vault.carousel-timing"]["faults"]
        )
        for part in (
            "at phone width",
            "holds a",
            "while hovered",
            "while focused",
            "after the visitor",
        ):
            with self.subTest(part=part):
                self.assertIn(part, details)

    def test_the_clean_page_names_nothing(self):
        code, got, out = self.clean
        self.assertEqual(code, 0, out)
        for rid in PLANTS:
            with self.subTest(record=rid):
                self.assertEqual(got[rid]["answer"], "pass", out)

    def test_a_part_record_without_parts_is_not_judged(self):
        tmp = os.path.join(self.tmp.name, "bare")
        table = os.path.join(self.tmp.name, "parts.table")
        with open(table, "w", encoding="utf8") as fh:
            fh.write(
                "vault.carousel-timing | carousel | "
                + "phone under 600, at least 5 s, words per second 3, watch 30 s\n"
            )
            fh.write(
                "vault.drag-release | drag-release | deceleration 0.998, slack 2\n"
            )
        with contextlib.redirect_stdout(io.StringIO()):
            code = flow.main(
                [
                    os.path.join(FIXTURES, "tier01-fault.html"),
                    "--out",
                    tmp,
                    "--records",
                    "--table",
                    table,
                ]
            )
        with open(os.path.join(tmp, "motion.json"), encoding="utf8") as fh:
            got = json.load(fh)["records"]
        self.assertEqual(code, 0)
        self.assertEqual({r["answer"] for r in got.values()}, {"not judged"})
        self.assertEqual(
            got["vault.carousel-timing"]["not_judged"],
            ["carousel: no carousel part declared with a selector (--parts)"],
        )
        self.assertEqual(
            got["vault.drag-release"]["not_judged"],
            [
                "drag-release: no bottom-sheet or card part declared with a selector (--parts)"
            ],
        )

    def test_a_cancelled_key_and_touch_scroll_fail(self):
        code, got, out = self.runs["keys"]
        self.assertEqual(code, 1, out)
        details = " | ".join(f["detail"] for f in got["vault.native-scroll"]["faults"])
        self.assertIn("cancels the Page Down (keydown PageDown)", details)
        self.assertIn("cancels the touch drag (touchmove)", details)
        self.assertNotIn("wheel", details)

    def test_a_touch_on_a_part_that_pans_itself_is_not_judged(self):
        code, got, out = self.runs["map"]
        self.assertEqual(code, 0, out)
        self.assertEqual(got["vault.native-scroll"]["faults"], [])

    def test_a_carousel_read_narrower_than_its_phone_width_is_not_judged(self):
        _, got, out = self.runs["narrow"]
        self.assertEqual(
            got["vault.carousel-timing"]["not_judged"],
            [
                "carousel: the viewport is 500 px wide, under the 600 px the wide load needs (--viewport)"
            ],
            out,
        )

    def test_a_script_animation_a_slow_screen_still_runs_fails(self):
        code, got, out = self.runs["slow"]
        self.assertEqual(code, 1, out)
        self.assertEqual(
            [f["subject"] for f in got["vault.slow-update"]["faults"]], ["div.pulse"]
        )
        self.assertIn("Fix: skip it where matchMedia('(update: slow)') matches.", out)


class Pause(unittest.TestCase):
    def test_check_access_answers_the_pause_plant(self):
        access = load("check_access", ACCESS)
        from playwright.sync_api import sync_playwright

        with sync_playwright() as play:
            browser = play.chromium.launch()
            try:
                got = {}
                for name in ("fault", "clean"):
                    ctx = browser.new_context()
                    url = "file://" + os.path.abspath(
                        os.path.join(FIXTURES, f"tier01-{name}.html")
                    )
                    got[name] = access.pause_answer(ctx, url)
                    ctx.close()
            finally:
                browser.close()
        faults, _unmeasured = got["fault"]
        self.assertEqual(
            [f["subject"] for f in faults],
            ["section:nth-of-type(1) > div.spinner:nth-of-type(1)"],
        )
        self.assertEqual(got["clean"], ([], []))


if __name__ == "__main__":
    child.main()
