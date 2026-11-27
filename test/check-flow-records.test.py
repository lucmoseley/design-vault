import concurrent.futures
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402

FLOW = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-flow.py"
)
ACCESS = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-access.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "flow")
LATE_INPUT = os.path.join(HERE, "late-input.py")


SCRIPTS = os.path.dirname(FLOW)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

records = siblings.load(SCRIPTS, "motion-records.py")
flow = siblings.load(SCRIPTS, os.path.basename(FLOW))
with open(flow.TABLE, encoding="utf8") as fh:
    LINES = records.parse_table(fh.read())
V = {line.mode: line.value for line in LINES}


# guess, #477
SHADOWED_TIMEOUT_S = 60


class Table(unittest.TestCase):
    def test_every_check_has_a_line_and_a_run_318(self):
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

    def test_a_check_given_two_values_is_refused_unlike_one_value_twice(self):  # #553
        with self.assertRaisesRegex(records.TableError, r"line 2: frequent .* line 1"):
            records.parse_table(
                "vault.a | frequent | under 150\nvault.b | frequent | under 400"
            )

    def test_a_check_named_twice_at_one_value_is_kept(self):  # #553
        got = records.parse_table(
            "vault.a | frequent | under 150\nvault.b | frequent | under 150"
        )
        self.assertEqual([line.id for line in got], ["vault.a", "vault.b"])

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
        for package in ("numpy", "PIL"):
            with self.subTest(package=package):
                done = self.shadowed(package)
                self.assertEqual(done.returncode, 3, done.stderr)
                self.assertIn(
                    f"{package} is missing — python3 -m pip install -r", done.stderr
                )

    def shadowed(self, package):
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

    def test_release_velocity_is_along_its_axis_and_zero_over_no_time(self):
        release = {"at": 60, "moves": [[0, 10, 50], [50, 30, 40]]}
        self.assertEqual(records.release_velocity(release, "left", 100), 400)
        self.assertEqual(records.release_velocity(release, "top", 100), -200)
        still = {"at": 5, "moves": [[5, 0, 0], [5, 9, 9]]}
        self.assertEqual(records.release_velocity(still, "top", 100), 0)

    def test_release_velocity_reads_only_the_horizon_before_the_release(self):
        release = {"at": 460, "moves": [[0, 0, 0], [400, 0, 0], [450, 50, 0]]}
        self.assertEqual(records.release_velocity(release, "left", 100), 1000)
        late = {"at": 650, "moves": release["moves"]}
        self.assertEqual(records.release_velocity(late, "left", 100), 0)

    def test_a_fling_serves_only_where_its_projection_picks_another_snap(self):
        fast = {"at": 260, "velocity": -1000}
        slow = {"at": 260, "velocity": -10}
        self.assertTrue(records.picks_another_snap([0, 300], fast, 0.998))
        self.assertFalse(records.picks_another_snap([0, 300], slow, 0.998))
        self.assertTrue(records.picks_another_snap([300], slow, 0.998))

    def test_a_slow_fling_still_names_a_bounce_but_not_where_it_settles(self):
        self.assertEqual(self.drag(0, [260, 200, 0], velocity=-10), [])
        bounce = self.drag(300, [260, 320, 300], velocity=10)
        self.assertEqual(len(bounce), 1)
        self.assertIn("bounce", bounce[0]["detail"])

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


# guess, #318
RUN_TIMEOUT_S = 240


def run(page, out, *extra, script=FLOW, parts="tier01-parts.json"):
    done = child.run(
        [
            sys.executable,
            script,
            page,
            "--out",
            out,
            "--records",
            "--parts",
            os.path.join(FIXTURES, parts),
            *extra,
        ],
        timeout=RUN_TIMEOUT_S,
    )
    with open(os.path.join(out, "motion.json"), encoding="utf8") as fh:
        return done.returncode, json.load(fh)["records"], done.stdout


PLANTS = {
    "vault.native-scroll": ["the page"],
    "vault.parallax": ["h2.drift", "div.layer.reveal"],
    "vault.carousel-timing": [".carousel"],
    "vault.flash-limit": ["div.strobe"],
    "vault.drag-release": [".card"],
    "vault.motion-frequency": ["button.buy"],
    "vault.slow-update": [".note"],
}


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
    "vault.drag-release": [],
    "vault.motion-frequency": ["end it under 150 ms, or drop it"],
    "vault.slow-update": ["move it inside @media (update: fast)"],
}


class Pages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
            "late": (
                os.path.join(FIXTURES, "tier01-clean.html"),
                "--table",
                table_of(where, "drag-release"),
            ),
            "rest": (
                os.path.join(FIXTURES, "tier01-fault.html"),
                "--table",
                table_of(where, "drag-release"),
            ),
        }
        options = {
            "late": {"script": LATE_INPUT},
            "rest": {"parts": "tier01-rest-parts.json"},
        }

        def go(name):
            page, *extra = runs[name]
            return name, run(
                page, os.path.join(where, name), *extra, **options.get(name, {})
            )

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

    def test_scrolling_a_card_under_the_pointer_is_no_move_of_its_own_478_paired_with_the_clean_page_names_nothing(
        self,
    ):
        _, got, out = self.fault
        self.assertEqual(got["vault.drag-release"]["not_judged"], [], out)

    def test_late_input_is_not_read_into_the_clean_pages_fling_478_510_paired_with_the_fault_page_names_every_plant(
        self,
    ):
        code, got, out = self.runs["late"]
        self.assertEqual(code, 0, out)
        self.assertEqual(got["vault.drag-release"]["answer"], "pass", out)

    def test_a_settle_from_rest_on_the_projected_snap_passes_the_script_428_paired_with_the_fault_page_names_every_plant(
        self,
    ):
        code, got, out = self.runs["rest"]
        self.assertEqual(code, 0, out)
        self.assertEqual(got["vault.drag-release"]["answer"], "pass", out)

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
    PAST_MS = 500  # guess, #628
    DEBOUNCED = "addEventListener('resize', () => setTimeout(() => requestAnimationFrame(() => %s.setAttribute('data-w', String(Math.random()))), 50));"  # guess, #646
    TALL_PX = 3000  # guess, #647: past the 720 px window of a default context
    TRIED = "changes what it shows more than 5 s after the page's load, and none of the 1 control(s) named for pausing it stops it, clicked; no carousel was declared, so whether the change shows cannot be told"

    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright

        cls.access = siblings.load(SCRIPTS, os.path.basename(ACCESS))
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def pause_answer(self, name, init=None, logged=None, carousels=()):
        ctx = self.browser.new_context()
        if logged is not None:
            ctx.on("console", lambda m: logged.append(m.text))
        try:
            if init:
                ctx.add_init_script(init)
            url = "file://" + os.path.abspath(
                os.path.join(FIXTURES, f"tier01-{name}.html")
            )
            return self.access.pause_answer(ctx, url, list(carousels), [])
        finally:
            ctx.close()

    def late(self, past_ms=PAST_MS):
        return mock.patch.object(
            self.access, "WATCH_MS", self.access.prelude.LONG_MS + past_ms
        )

    def clean_answer(self):
        return (
            [],
            [
                f"section:nth-of-type(1) {self.TRIED}",
                f"section:nth-of-type(2) > div.carousel {self.TRIED}",
            ],
        )

    def test_check_access_answers_the_pause_plant_545(self):
        faults, _unmeasured = self.pause_answer("fault")
        self.assertEqual(
            [f["subject"] for f in faults],
            ["section:nth-of-type(1) > div.spinner:nth-of-type(1)"],
        )
        self.assertEqual(self.pause_answer("clean"), self.clean_answer())

    def test_a_read_reaching_5_s_late_still_sees_the_carousel_turn_628_paired_with_test_check_access_answers_the_pause_plant_545(
        self,
    ):
        with self.late():
            got = self.pause_answer("clean")
        self.assertEqual(got, self.clean_answer())

    def unwatched_after_5_s(self, script, past_ms=PAST_MS, logged=None):
        init = f"""
          addEventListener('DOMContentLoaded', () => {{
            document.querySelector('.pause').remove();
            {script}
          }});
        """
        with self.late(past_ms):
            faults, unmeasured = self.pause_answer("clean", init, logged)
        self.assertEqual(
            [f["subject"] for f in faults],
            ["section:nth-of-type(1) > div.spinner:nth-of-type(1)"],
        )
        self.assertEqual(
            [u.split(" changes ")[0] for u in unmeasured],
            [
                "section:nth-of-type(1)",
                "section:nth-of-type(2) > div.carousel",
                (
                    "the page still ran a timer that did not run in the 6 s watched past 5 s from its load, "
                    "and no control on the page is named for pausing, stopping or hiding it, so a slower change cannot be ruled out"
                ),
            ],
        )

    def test_a_change_a_debounced_resize_handler_makes_past_5_s_is_no_rotation_646_paired_with_test_check_access_answers_the_pause_plant_545(
        self,
    ):
        self.unwatched_after_5_s(self.DEBOUNCED % "document.querySelector('.lane')")

    def test_a_change_a_body_onresize_handler_makes_past_5_s_is_no_rotation_646_paired_with_test_check_access_answers_the_pause_plant_545(
        self,
    ):
        self.unwatched_after_5_s(
            "document.body.onresize = () => document.querySelector('.lane').setAttribute('data-w', String(Math.random()));"
        )

    def test_a_change_past_rotate_ms_from_5_s_is_not_read_628_paired_with_test_check_access_answers_the_pause_plant_545(
        self,
    ):
        window_ms = self.access.prelude.LONG_MS + self.access.keys.ROTATE_MS
        logged = []
        self.unwatched_after_5_s(
            f"setTimeout(() => {{ document.querySelector('.lane').setAttribute('data-late', 'on'); console.log('late'); }}, {window_ms + self.PAST_MS});",
            self.access.keys.ROTATE_MS + 4 * self.PAST_MS,
            logged,
        )
        self.assertIn("late", logged)

    def test_a_change_a_debounced_resize_handler_makes_past_5_s_beside_a_declared_carousel_taller_than_the_window_is_no_rotation_647_paired_with_test_check_access_answers_the_pause_plant_545(
        self,
    ):
        tall = f"document.head.insertAdjacentHTML('beforeend', '<style>.carousel {{ height: {self.TALL_PX}px; }}</style>');"
        handler = self.DEBOUNCED % "document.body"
        answers = [
            self.pause_answer(
                "clean",
                f"addEventListener('DOMContentLoaded', () => {{ document.querySelector('.pause').remove(); {script} }});",
                carousels=[".carousel"],
            )
            for script in (tall, tall + handler)
        ]
        self.assertIn(
            "section:nth-of-type(2) > div.carousel",
            [f["subject"] for f in answers[0][0]],
        )
        self.assertEqual(answers[1], answers[0])


if __name__ == "__main__":
    child.main()
