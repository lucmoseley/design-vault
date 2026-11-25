"""Tests plugin/skills/design-round/scripts/check-flow.py (#60): python3 test/check-flow.test.py

`analyse`, `sample_times` and `numbers` are tested on synthetic input, so each
threshold is pinned without a browser; so are a morph's interpolation and
structure check (#72), the speed step (#69), when a page has finished
playing (#135) and the exit ladder the browser scripts share (#131).
"""

import contextlib
import http.server
import importlib.util
import io
import itertools
import json
import math
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import types
import unittest
from unittest import mock

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-flow.py"
)
FALL = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "fall.js"
)
FALL_MOTION = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "fall-motion.js"
)
CURVES = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-curves.js"
)
FIXTURES = os.path.join(HERE, "fixtures", "flow")
REQUIREMENTS = os.path.join(HERE, "..", "plugin", "requirements.txt")
SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

flow = siblings.load(SCRIPTS, "check-flow.py")

STEP = 1000 / flow.FPS


def ease_in_out(p):
    return 3 * p * p - 2 * p * p * p


def linear(p):
    return p


def sample(*moves, until, times=None):
    """One element per move, each (start ms, end ms, easing), travelling 300 px."""
    times = times or [k * STEP for k in range(round(until / STEP) + 1)]
    elements = []
    for n, (start, end, easing) in enumerate(moves):
        xs = []
        for t in times:
            p = min(1, max(0, (t - start) / (end - start)))
            xs.append([300 * easing(p), 0])
        elements.append({"label": f"el{n}", "channels": {"position": xs}})
    return {"times": times, "elements": elements}


# These moves run 100-450 ms, where the line spans 0.8 to under 0.5: a jolt
# line of one share at every length pins what is judged, not where the line is.
FIXED_LINE = 0.5


def jolts_at(speeds, dropped=()):
    """(edge, frame) of each jolt in a move along x at `speeds`, px per frame at
    60 fps, with the frame indices `dropped` undrawn, on FIXED_LINE."""
    xs = [[sum(speeds[:k]), 0] for k in range(len(speeds) + 1)]
    times = [k * STEP for k in range(len(xs))]
    el = {
        "label": "el0",
        "channels": {"position": xs},
        "dropped": {"position": [(k * STEP, (k + 1) * STEP) for k in dropped]},
    }
    return [
        (j["edge"], round(j["at"] / STEP))
        for j in flow.analyse(
            {"times": times, "elements": [el]}, jolt_ratio=FIXED_LINE
        )["jolts"]
    ]


# Speeds px per frame of a move easing in and out to 3% of its top speed.
EASED = [1, 3, 6, 10, 10, 6, 3, 1, 0.3]


def run_records_layout(subject):
    """The check-layout module `subject.run_records` loads, stopped before any browser starts."""
    loaded = []
    real = siblings.load

    def spy(here, file):
        module = real(here, file)
        if file == "check-layout.py":
            loaded.append(module)
        return module

    class StopError(Exception):
        pass

    with (
        mock.patch.object(siblings, "load", spy),
        mock.patch.object(subject, "chromium", side_effect=StopError),
        contextlib.suppress(StopError),
    ):
        subject.run_records(types.SimpleNamespace(lines=[]))
    (layout,) = loaded
    return layout


class OneCopy(unittest.TestCase):
    def test_run_records_check_layout_shares_this_copy_paired_with_a_private_load(
        self,
    ):  # #562
        self.assertIs(run_records_layout(flow).flow, flow)

    def test_a_private_load_s_run_records_reaches_a_second_copy(self):  # #562
        spec = importlib.util.spec_from_file_location("private_check_flow", SCRIPT)
        private = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(private)
        self.assertIsNot(run_records_layout(private).flow, private)

    def test_the_probe_parse_loads_shares_this_copy(self):  # #562
        self.assertIs(siblings.load(SCRIPTS, "probe.py").flow, flow)


class Pauses(unittest.TestCase):
    def test_a_still_spell_over_the_threshold_is_a_pause(self):
        r = flow.analyse(
            sample((0, 500, ease_in_out), (800, 1300, ease_in_out), until=1300)
        )
        self.assertEqual(len(r["pauses"]), 1)
        p = r["pauses"][0]
        self.assertAlmostEqual(p["start"], 500, delta=2 * STEP)
        self.assertAlmostEqual(p["end"], 800, delta=2 * STEP)
        self.assertIsNone(p["where"])

    def test_a_still_spell_under_the_threshold_is_not(self):
        r = flow.analyse(
            sample((0, 500, ease_in_out), (700, 1200, ease_in_out), until=1200)
        )
        self.assertEqual(r["pauses"], [])

    def test_the_threshold_is_the_callers(self):
        r = flow.analyse(
            sample((0, 500, ease_in_out), (700, 1200, ease_in_out), until=1200),
            pause_ms=150,
        )
        self.assertEqual(len(r["pauses"]), 1)

    def test_a_still_start_before_smooth_motion_is_no_pause(self):  # #220
        r = flow.analyse(sample((400, 900, ease_in_out), until=900))
        self.assertEqual(
            (r["pauses"], r["jolts"], r["jumps"], r["steps"]), ([], [], [], [])
        )


def creep(px_s, channel="position", view_cm=flow.VIEW_CM):
    """check-flow's pauses for a 300 px move at about 900 px/s at its top that then
    creeps on at `px_s` a second for 400 ms, as a settle's tail does, on `channel`."""
    times = [k * STEP for k in range(round(1000 / STEP) + 1)]
    values = []
    for t in times:
        x = 300 * ease_in_out(min(1, t / 500)) + px_s * min(400, max(0, t - 500)) / 1000
        values.append([x, 0] if channel == "position" else str(x))
    el = {"label": "el0", "channels": {channel: values}}
    r = flow.analyse({"times": times, "elements": [el]}, view_cm=view_cm)
    return [(p["start"], p["end"]) for p in r["pauses"]]


class Still(unittest.TestCase):
    def test_a_creep_seen_as_motion_is_no_pause_though_under_1_percent_of_top_speed(
        self,
    ):
        # 3 px/s, about 4.5 minutes of arc a second at 60 cm: visible (#196).
        self.assertLess(3, flow.STILL_FRACTION * 900)
        self.assertEqual(creep(3), [])

    def test_a_creep_under_the_still_floor_is_still(self):
        # One CSS px is 1.5 minutes of arc from 60 cm, so 1 a minute is 0.66 px/s:
        # test/fall.test.js holds fall.js to the same figure.
        [(start, _)] = creep(0.6)
        self.assertAlmostEqual(start, 500, delta=2 * STEP)
        self.assertEqual(creep(0.72), [])

    def test_the_still_floor_grows_with_the_viewing_distance(self):
        # One px a second is 1.5 minutes of arc from 60 cm and 0.75 from 120 cm.
        self.assertEqual(creep(1, view_cm=60), [])
        self.assertEqual(len(creep(1, view_cm=120)), 1)

    def test_a_channel_that_is_not_a_box_is_still_under_its_share_alone(self):
        # A custom property's number has no visual angle, so 3 a second is still.
        self.assertEqual(len(creep(3, channel="--travel")), 1)


class Jolts(unittest.TestCase):
    def test_a_linear_move_from_rest_jolts_at_both_ends(self):
        r = flow.analyse(sample((100, 600, linear), until=800))
        edges = [(j["edge"], j["at"]) for j in r["jolts"]]
        self.assertEqual(edges, [("starts", 100), ("stops", 600)])
        self.assertEqual(r["jolts"][0]["share"], 1)

    def test_an_eased_move_does_not_jolt(self):
        r = flow.analyse(sample((100, 600, ease_in_out), until=800))
        self.assertEqual(r["jolts"], [])

    def test_ease_out_starts_at_full_speed_so_it_jolts_at_its_start_only(self):
        r = flow.analyse(sample((100, 600, lambda p: 1 - (1 - p) ** 3), until=800))
        self.assertEqual([j["edge"] for j in r["jolts"]], ["starts"])

    def test_a_move_starting_mid_frame_is_sampled_at_its_exact_start_and_end(self):
        times = flow.sample_times(800, [110, 610], 60)
        self.assertIn(110, times)
        self.assertIn(610, times)
        r = flow.analyse(sample((110, 610, linear), until=800, times=times))
        self.assertEqual(
            [(j["edge"], j["at"]) for j in r["jolts"]],
            [("starts", 110), ("stops", 610)],
        )

    def test_a_move_starting_mid_frame_has_a_whole_first_frame(self):
        # A loaded machine starts one 1.5 ms before a frame, where a part
        # frame would carry its box 3 px and hide its jump (#326).
        times = flow.sample_times(800, [48.5, 448.5], 60, [48.5])
        self.assertEqual(times[times.index(48.5) + 1], 48.5 + STEP)
        move = (48.5, 448.5, lambda p: 1 - (1 - p) ** 3)
        r = flow.analyse(sample(move, until=800, times=times))
        self.assertEqual([round(j["px"]) for j in r["jumps"]], [36])

    def test_no_two_sample_times_fall_within_1_ms(self):
        times = flow.sample_times(100, [16.9, 50, 99.5], 60)
        self.assertTrue(all(b - a >= 1 for a, b in itertools.pairwise(times)))
        self.assertEqual(times[-1], 100)

    def test_an_exact_time_within_1_ms_of_a_frame_takes_its_place(self):
        # The frame would run 0.17 ms past the keyframe into its next speed (#126).
        times = flow.sample_times(800, [416.5], 60)
        self.assertIn(416.5, times)
        self.assertFalse(any(abs(t - 1000 / 60 * 25) < 1e-9 for t in times))

    def test_a_start_within_1_ms_of_the_first_frame_takes_its_place(self):
        # A load-time animation starts 0.09 ms after it; at 0 it reads as not
        # started, so its first keyframe went unseen (#297).
        times = flow.sample_times(400.09, [0.09, 0.4, 400.09], 60)
        self.assertEqual((times[0], times[1]), (0.4, 1000 / 60))
        self.assertEqual(flow.sample_times(400, [1.5], 60)[:2], [0, 1.5])

    def test_the_sample_times_run_from_zero_to_the_exact_end(self):
        for end in (2401, 2400.5, 2416.9, 0.5):
            times = flow.sample_times(end, [], 60)
            self.assertEqual((times[0], times[-1]), (0, end))
            self.assertTrue(
                all(b - a >= 0.5 for a, b in itertools.pairwise(times)), end
            )

    def test_only_an_endless_loop_is_excused_its_stop_at_the_window_end(self):
        s = sample((100, 600, linear), (100, 600, linear), until=400)
        self.assertEqual(
            [j["edge"] for j in flow.analyse(s)["jolts"]],
            ["starts", "starts", "stops", "stops"],
        )
        s["elements"][0]["loops"] = True
        got = [(j["element"], j["edge"]) for j in flow.analyse(s)["jolts"]]
        self.assertEqual(got, [("el0", "starts"), ("el1", "starts"), ("el1", "stops")])

    def test_float_noise_is_not_motion(self):
        s = sample((100, 600, ease_in_out), until=800)
        s["elements"][0]["channels"]["size"] = [
            [40 + (k % 3) * 1e-5, 40] for k in range(len(s["times"]))
        ]
        r = flow.analyse(s)
        self.assertNotIn("size", r["elements"][0]["channels"])
        self.assertEqual(r["jolts"], [])

    def test_a_turn_inside_a_frame_is_not_a_stop_and_a_start(self):
        # A stiff landing's sink turns within a frame, which reads as still (#151).
        def run(between, back=-1):
            return jolts_at(
                [1, 3, 6, 10, 10, 10, *between, *(back * v for v in (8, 8, 8, 6, 3, 1))]
            )

        self.assertEqual(run([0.01]), [])
        self.assertEqual(run([0.01, -0.01]), [])
        # A rest of three frames is a stop and a start; going on the same way is no turn.
        self.assertEqual(run([0, 0, 0]), [("stops", 6), ("starts", 9)])
        self.assertEqual(run([0.01], back=1), [("stops", 6), ("starts", 7)])

    def test_a_start_out_of_a_turn_is_judged_from_the_speed_it_turned_at(self):
        # A small rebound after a big fall turns still for several frames under
        # the fall's floor and starts back at 60% of its own top speed, no
        # faster than it turned (#150).
        self.assertEqual(
            jolts_at([*EASED, *[0.005] * 4, -0.3, -0.5, -0.4, -0.2, -0.1]), []
        )

    def test_a_move_that_starts_back_at_full_speed_after_turning_slowly_jolts(self):
        # However short the still spell between (#150).
        for still in (1, 2, 4):
            self.assertEqual(
                jolts_at([*EASED, *[0.005] * still, -8, -8, -8, -6, -3, -1]),
                [("starts", 9 + still)],
                still,
            )

    def test_a_still_spell_longer_than_a_pause_is_a_rest_not_a_turn(self):
        # It eases to 40% of its top speed, then rests 333 ms (#150).
        self.assertEqual(
            jolts_at([1, 3, 6, 10, 10, 6, 4, *[0] * 20, -3, -3, -2, -1, -0.3]),
            [("starts", 27)],
        )

    def test_a_dropped_frame_a_move_turned_at_hides_the_start_after_it_but_an_earlier_one_does_not(
        self,
    ):
        # The speed it turned at is unknown, so its gain is too (#150).
        speeds = [*EASED, 0.005, -8, -8, -8, -6, -3, -1]
        self.assertEqual(jolts_at(speeds, dropped=[8]), [])
        self.assertEqual(jolts_at(speeds, dropped=[7]), [("starts", 10)])

    def test_a_turns_gain_and_another_channels_start_from_rest_are_told_apart(self):
        # In one frame, its position turns back fast and its opacity starts from rest (#150 review).
        speeds = [*EASED, 0.005, -8, -8, -8, -6, -3, -1]
        xs = [[sum(speeds[:k]), 0] for k in range(len(speeds) + 1)]
        fade = [[min(1, max(0, (k - 10) / 4))] for k in range(len(xs))]
        times = [k * STEP for k in range(len(xs))]
        r = flow.analyse(
            {
                "times": times,
                "elements": [
                    {"label": "el0", "channels": {"position": xs, "opacity": fade}}
                ],
            },
            jolt_ratio=FIXED_LINE,
        )
        got = [
            (round(j["at"] / STEP), j["channels"], j.get("turn", False), j["share"])
            for j in r["jolts"]
            if j["edge"] == "starts"
        ]
        self.assertCountEqual(
            got, [(10, ["position"], True, 0.96), (10, ["opacity"], False, 1)]
        )

    def test_a_box_change_under_the_px_floor_is_not_motion_over_however_short_a_gap(
        self,
    ):
        # mmm-infra#35's still piece: its box wobbled by float32 steps of
        # 6.1e-5 and 1.2e-4 px across a 1.9 ms gap, a rate over the noise floor (#149).
        times = [0, 100, 101.9, 200]
        for name in ("size", "position"):
            for wobble in (6.1e-5, 1.2e-4):
                s = {
                    "times": times,
                    "elements": [
                        {
                            "label": "piece",
                            "channels": {
                                name: [
                                    [40, 40],
                                    [40, 40],
                                    [40 + wobble, 40],
                                    [40 + wobble, 40],
                                ]
                            },
                        }
                    ],
                }
                self.assertEqual(
                    flow.analyse(s)["elements"][0]["channels"], {}, (name, wobble)
                )

    def test_a_1_px_move_is_still_measured_from_its_start(self):
        for fps in (30, 60, 120):
            times = flow.sample_times(1400, [100, 1100], fps)
            s = sample((100, 1100, ease_in_out), until=0, times=times)
            s["elements"][0]["channels"]["position"] = [
                [x / 300, y] for x, y in s["elements"][0]["channels"]["position"]
            ]
            r = flow.analyse(s)
            self.assertEqual(
                (r["jolts"], r["steps"], [p["where"] for p in r["pauses"]]),
                ([], [], ["at the end"]),
                fps,
            )
            moving = r["elements"][0]["channels"]["position"]["moving"]
            # At 120 fps its first frame, 2e-4 px, falls under the floor.
            self.assertAlmostEqual(
                times[moving.index(True)], 100, delta=2 * 1000 / fps, msg=fps
            )


def blend(c):
    """A move with `c` of a linear move mixed into an ease-in-out one: its first
    frame runs near c / (c + 1.5(1 - c)) of its top speed at any length."""
    return lambda p: c * p + (1 - c) * ease_in_out(p)


def first_share(easing, ms):
    """check-flow's first-frame share for one move of `ms`, on no line."""
    r = flow.analyse(sample((100, 100 + ms, easing), until=ms + 300), jolt_ratio=1e-9)
    return next(j["share"] for j in r["jolts"] if j["edge"] == "starts")


class JoltLine(unittest.TestCase):
    def test_the_line_is_the_middle_of_the_band_221_set(self):
        for ms, want in ((300, 0.5), (500, 0.37), (1000, 0.29)):
            self.assertAlmostEqual(flow.jolt_line(ms), want, delta=0.02, msg=ms)
        self.assertAlmostEqual(flow.jolt_line(200), 0.8)
        self.assertAlmostEqual(flow.jolt_line(5000), 0.26)

    def test_a_move_under_200_ms_has_no_line(self):
        self.assertIsNone(flow.jolt_line(199.9))
        self.assertIsNone(flow.jolt_line(0))

    def test_the_line_falls_as_a_move_lengthens(self):
        lines = [flow.jolt_line(ms) for ms in range(200, 2400, 50)]
        self.assertTrue(all(a >= b for a, b in itertools.pairwise(lines)))

    def test_material_3s_standard_curve_crosses_a_fixed_half_only_when_short_and_never_its_line(
        self,
    ):
        # One frame's share of one curve falls as the move lengthens
        # (docs/research/jolt-onset.md F7).
        m3 = bezier(0.2, 0, 0, 1)
        short, long = first_share(m3, 150), first_share(m3, 300)
        self.assertGreaterEqual(short, 0.5)
        self.assertLess(long, 0.5)
        for ms in (150, 200, 300, 1000):
            r = flow.analyse(sample((100, 100 + ms, m3), until=ms + 300))
            self.assertEqual([j["edge"] for j in r["jolts"]], [], ms)

    def test_one_start_share_passes_in_a_300_ms_move_and_jolts_in_a_1_s_one(self):
        # The old fixed line, 0.5, passed both.
        for ms, want in ((300, []), (1000, ["starts"])):
            self.assertLess(first_share(blend(0.4), ms), 0.5)
            r = flow.analyse(sample((100, 100 + ms, blend(0.4)), until=ms + 300))
            self.assertEqual(
                [j["edge"] for j in r["jolts"] if j["edge"] == "starts"], want, ms
            )

    def test_each_jolt_names_its_line_and_a_fixed_ratio_overrides_it(self):
        [j] = [
            j
            for j in flow.analyse(sample((100, 1100, blend(0.4)), until=1300))["jolts"]
            if j["edge"] == "starts"
        ]
        self.assertEqual(j["line"], round(flow.jolt_line(1000), 2))
        r = flow.analyse(sample((100, 1100, blend(0.4)), until=1300), jolt_ratio=0.5)
        self.assertEqual(r["jolts"], [])
        r = flow.analyse(sample((100, 250, linear), until=500), jolt_ratio=0.5)
        self.assertEqual([j["line"] for j in r["jolts"]], [0.5, 0.5])

    def test_a_short_linear_move_starts_and_stops_unjudged_by_share(self):
        r = flow.analyse(sample((100, 250, linear), until=500))
        self.assertEqual(r["jolts"], [])


def first_frame(px, view_cm=flow.VIEW_CM, channel="position"):
    """check-flow's verdict on a 1 s move along x whose first frame carries it
    `px`, eased in from there."""
    speeds = [px, *[px * 4] * 50, *[px * 2, px, px / 2, px / 4]]
    xs = [[sum(speeds[:k]), 0] for k in range(len(speeds) + 1)]
    times = [k * STEP for k in range(len(xs))]
    el = {"label": "el0", "channels": {channel: xs}}
    return flow.analyse({"times": times, "elements": [el]}, view_cm=view_cm)


class Jumps(unittest.TestCase):
    def test_the_jump_is_026_degrees_about_10_px_at_60_cm(self):
        self.assertAlmostEqual(flow.jump_px(60), 10.3, delta=0.05)
        self.assertAlmostEqual(flow.jump_px(30), flow.jump_px(60) / 2, delta=1e-6)

    def test_a_first_frame_over_the_jump_is_flagged_whatever_its_share(self):
        # A quarter of its top speed, under the 1 s line.
        r = first_frame(11)
        self.assertEqual(r["jolts"], [])
        self.assertEqual(
            [(j["element"], j["at"], j["px"]) for j in r["jumps"]], [("el0", 0, 11)]
        )
        self.assertEqual(first_frame(10)["jumps"], [])

    def test_the_jump_shrinks_with_the_viewing_distance(self):
        self.assertEqual(len(first_frame(6, view_cm=30)["jumps"]), 1)
        self.assertEqual(first_frame(6, view_cm=60)["jumps"], [])

    def test_a_short_move_jumps_though_it_has_no_line(self):
        # 300 px in 150 ms is 33 px a frame.
        r = flow.analyse(sample((100, 250, linear), until=500))
        self.assertEqual((r["jolts"], [j["at"] for j in r["jumps"]]), ([], [100]))

    def test_only_a_boxs_start_from_rest_jumps(self):
        # Not a stop, not a start out of a turn, and not a channel with no px.
        self.assertEqual(first_frame(40, channel="--travel")["jumps"], [])
        speeds = [*EASED, 0.005, -40, -40, -30, -20, -10, -3, -1]
        xs = [[sum(speeds[:k]), 0] for k in range(len(speeds) + 1)]
        times = [k * STEP for k in range(len(xs))]
        r = flow.analyse(
            {
                "times": times,
                "elements": [{"label": "el0", "channels": {"position": xs}}],
            }
        )
        self.assertEqual(r["jumps"], [])
        r = flow.analyse(
            sample((100, 250, lambda p: 1 - (1 - p) ** 2 if p < 1 else 1), until=500)
        )
        self.assertEqual([j["at"] for j in r["jumps"]], [100])


def hidden(sample_, element, frames):
    """`sample_` with `element` unseen at the frame indices `frames`."""
    el = sample_["elements"][element]
    el["seen"] = [k not in frames for k in range(len(sample_["times"]))]
    return sample_


class Unseen(unittest.TestCase):
    def test_a_start_the_viewer_never_sees_at_rest_is_listed_not_judged(self):
        # 300 px in 400 ms, ease-out: a jolt and a jump at its start (#297).
        s = sample((100, 500, lambda p: 1 - (1 - p) ** 3), until=700)
        rest = s["times"].index(100)
        r = flow.analyse(hidden(s, 0, {rest}))
        self.assertEqual((r["jolts"], r["jumps"]), ([], []))
        self.assertEqual(
            [
                (u["element"], u["edge"], u["at"], u["would_be"], u["channels"])
                for u in r["unseen"]
            ],
            [("el0", "starts", 100, ["jolt", "jump"], ["position"])],
        )

    def test_seen_at_rest_it_is_judged_though_unseen_once_it_moves(self):
        s = sample((100, 500, lambda p: 1 - (1 - p) ** 3), until=700)
        rest = s["times"].index(100)
        r = flow.analyse(hidden(s, 0, set(range(rest + 1, rest + 5))))
        self.assertEqual((len(r["jolts"]), len(r["jumps"]), r["unseen"]), (1, 1, []))

    def test_a_stop_the_viewer_never_sees_is_not_judged(self):
        # It exits at full speed.
        s = sample((100, 500, lambda p: p**3), until=700)
        end = round(500 / STEP)
        self.assertEqual([j["edge"] for j in flow.analyse(s)["jolts"]], ["stops"])
        r = flow.analyse(hidden(s, 0, set(range(end, len(s["times"])))))
        self.assertEqual(r["jolts"], [])
        self.assertEqual(
            [(u["edge"], u["would_be"]) for u in r["unseen"]], [("stops", ["jolt"])]
        )

    def test_an_unseen_start_that_would_be_nothing_is_not_listed(self):
        s = sample((100, 500, ease_in_out), until=700)
        r = flow.analyse(hidden(s, 0, set(range(len(s["times"])))))
        self.assertEqual(r["unseen"], [])


def fall_js(*args):
    """fall.js's --json result for one command line."""
    out = subprocess.run(
        ["node", FALL, *map(str, args), "--json"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return json.loads(out)


def landing(drop=240, scale=800, sink=4):
    """fall.js's result for one drop, with its easing. The defaults are any plausible
    drop."""
    return fall_js("--drop", drop, "--scale", scale, "--sink", sink)


def played(easing, p):
    """Where a CSS `linear()` easing puts progress p, as a browser plays it."""
    parts = [x.split(" ") for x in easing[len("linear(") : -1].split(", ")]
    pts = [
        (
            float(x[1].rstrip("%")) / 100 if len(x) > 1 else 0 if i == 0 else 1,
            float(x[0]),
        )
        for i, x in enumerate(parts)
    ]
    for (pa, va), (pb, vb) in itertools.pairwise(pts):
        if p <= pb:
            return vb if pb == pa else va + (vb - va) * (p - pa) / (pb - pa)
    return pts[-1][1]


class Landing(unittest.TestCase):
    def test_a_bare_gravity_fall_stops_at_full_speed(self):
        r = flow.analyse(sample((100, 347, lambda p: p * p), until=600))
        self.assertEqual([j["edge"] for j in r["jolts"]], ["stops"])

    def test_the_fall_into_its_landing_does_not_jolt_or_step(self):
        # The landing's sink stops a full-speed fall within a frame or two. One
        # fall.js warns is shorter than a frame stops at full speed: 600 px with
        # a 1 px sink stops at 0.48 of its top speed, over its 400 ms line (#297).
        for drop, sink in itertools.product((60, 240, 600), (1, 4, 12)):
            f = landing(drop=drop, sink=sink)
            r = flow.analyse(
                sample(
                    (100, 100 + f["ms"], lambda p, e=f["easing"]: played(e, p)),
                    until=f["ms"] + 300,
                )
            )
            want = ["stops"] if (drop, sink) == (600, 1) else []
            if want:
                self.assertLess(f["landMs"], flow.BROWSER_FRAME_MS)
            self.assertEqual(
                ([j["edge"] for j in r["jolts"]], r["steps"]), (want, []), (drop, sink)
            )


def settled(distance=300, ms=900, damping=1):
    """fall.js's result for one heavy settle (#105), with its easing. The defaults are
    any plausible settle."""
    return fall_js("--settle", distance, "--ms", ms, "--damping", damping)


def settle_flow(f):
    """check-flow's verdict on one settle, played from 100 ms with 300 ms still after."""
    return flow.analyse(
        sample(
            (100, 100 + f["ms"], lambda p: played(f["easing"], p)), until=f["ms"] + 400
        )
    )


def settle_then(f, fps=flow.FPS, then=None):
    """check-flow's verdict on one settle played from 100 ms at `fps`, over its own
    distance: the window ends where it does or, given `then`, where a 500 ms move
    that starts `then` ms after its printed end does."""
    step, start = 1000 / fps, 100
    until = start + f["ms"] + (0 if then is None else then + 500)
    times = [k * step for k in range(int(until / step) + 1)]
    times += [until] if times[-1] < until else []

    def at(p):
        return [f["distance"] * played(f["easing"], min(1, max(0, p))), 0]

    elements = [
        {
            "label": "settle",
            "channels": {"position": [at((t - start) / f["ms"]) for t in times]},
        }
    ]
    if then is not None:
        nxt = start + f["ms"] + then
        elements.append(
            {
                "label": "next",
                "channels": {
                    "position": [
                        [300 * ease_in_out(min(1, max(0, (t - nxt) / 500))), 0]
                        for t in times
                    ]
                },
            }
        )
    return flow.analyse({"times": times, "elements": elements})


class Settle(unittest.TestCase):
    def test_a_settle_ending_the_page_has_no_pause_or_step(self):
        # Cases #132's grid found failing (#142).
        cases = [
            (300, 1600, 60),
            (1200, 900, 60),
            (1200, 1600, 60),
            (40, 1600, 60),
            (300, 3000, 120),
        ]
        cases += [
            (10, ms, fps) for ms in (400, 600, 900, 1600, 3000) for fps in (30, 120)
        ]
        for distance, ms, fps in cases:
            r = settle_then(settled(distance, ms), fps)
            self.assertEqual((r["pauses"], r["steps"]), ([], []), (distance, ms, fps))

    def test_a_move_that_starts_at_a_settles_printed_end_follows_it_with_no_pause(self):
        for distance, ms in ((300, 1600), (1200, 900), (1200, 1600)):
            self.assertEqual(
                settle_then(settled(distance, ms), then=0)["pauses"], [], (distance, ms)
            )
        # The harness sees a pause where there is one: the move 400 ms late.
        [pause] = settle_then(settled(300, 1600), then=400)["pauses"]
        self.assertAlmostEqual(pause["ms"], 400, delta=2 * STEP)

    def test_a_critically_damped_settle_has_no_jolt_or_step(self):
        # At 600 ms, 300 px and more start over the line, and fall.js warns (#297).
        for distance, ms in itertools.product((100, 300, 1200), (900, 1600)):
            r = settle_flow(settled(distance, ms))
            self.assertEqual((r["jolts"], r["steps"]), ([], []), (distance, ms))

    def test_fall_js_warns_of_a_settle_exactly_where_its_start_jolts_or_jumps(self):
        warned = set()
        for distance, ms, damping in itertools.product(
            (10, 100, 300, 1200), (200, 600, 900, 1600), (1, 1.5)
        ):
            f = settled(distance, ms, damping)
            jolts = f["startShare"] >= f["joltLine"]
            jumps = f["firstPx"] >= flow.jump_px(flow.VIEW_CM)
            warned |= {"jolt"} if jolts else set()
            warned |= {"jump"} if jumps else set()
            r = settle_then(f)
            self.assertEqual(
                ([j["edge"] for j in r["jolts"]], len(r["jumps"])),
                (["starts"] if jolts else [], int(jumps)),
                (distance, ms, damping),
            )
        self.assertEqual(warned, {"jolt", "jump"})

    def test_fall_motion_holds_the_jolt_line_and_jump_of_check_flow(self):
        got = json.loads(
            subprocess.run(
                [
                    "node",
                    "-e",
                    f"const f = require({json.dumps(FALL_MOTION)}); console.log(JSON.stringify("
                    "[[150, 200, 220, 300, 640, 1000, 1700, 5000].map(f.joltLine), [30, 60, 90].map(f.jumpPx)]))",
                ],
                capture_output=True,
                text=True,
                check=True,
            ).stdout
        )
        lines = [
            flow.jolt_line(ms) for ms in (150, 200, 220, 300, 640, 1000, 1700, 5000)
        ]
        self.assertEqual(got[0][0], lines[0])
        for a, b in zip(got[0][1:], lines[1:], strict=True):
            self.assertAlmostEqual(a, b, places=9)
        for a, cm in zip(got[1], (30, 60, 90), strict=True):
            self.assertAlmostEqual(a, flow.jump_px(cm), places=9)


def each_frame_phase(f):
    """(share, fps, check-flow's verdict) for a fall.js result played over its own
    distance from 100 ms plus each quarter of a frame, at 30, 60 and 120 fps,
    sampled as check-flow does."""
    size = f.get("drop") or f["distance"]
    for share, fps in itertools.product((0, 0.25, 0.5, 0.75), (30, 60, 120)):
        start = 100 + share * 1000 / fps
        times = flow.sample_times(start + f["ms"] + 300, [start, start + f["ms"]], fps)
        s = sample(
            (
                start,
                start + f["ms"],
                lambda p, e=f["easing"]: size * played(e, p) / 300,
            ),
            until=0,
            times=times,
        )
        yield share, fps, flow.analyse(s)


class Defaults(unittest.TestCase):
    def test_fall_js_defaults_pass_the_step_check(self):
        # mmm-infra#35's stone and slab first (#151), and the 5 px drop at 800 px/m
        # with a 1 px sink (#196).
        falls = [
            (24, 10, 3, 1),
            (30, 10, 3, 1),
            (240, 800, 4, 1),
            (240, 800, 4, 2),
            (600, 800, 12, 1),
            (2400, 3, 12, 1),
            (24, 3000, 1, 2),
            (5, 3, 1, 2),
            (5, 800, 1, 1),
        ]
        settles = [(300, 900, 1), (300, 900, 2), (10, 3000, 1), (2400, 5000, 1)]
        made = [
            fall_js("--drop", d, "--scale", sc, "--sink", sk, "--damping", z)
            for d, sc, sk, z in falls
        ]
        made += [
            fall_js("--settle", d, "--ms", ms, "--damping", z) for d, ms, z in settles
        ]
        for f, case in zip(made, falls + settles, strict=True):
            for share, fps, r in each_frame_phase(f):
                self.assertEqual(r["steps"], [], (case, share, fps))

    def test_a_soft_landing_stops_without_a_jolt(self):
        # It arrives at rest at the still speed (#152); ended short of rest, its
        # last span snapped there as a jolt (#151).
        for case in ((24, 10, 1), (5, 3, 1), (24, 3, 1)):
            f = landing(*case)
            for share, fps, r in each_frame_phase(f):
                self.assertEqual(r["jolts"], [], (case, share, fps))


def bezier(x1, y1, x2, y2):
    """A CSS cubic-bezier() easing."""

    def at(p):
        lo, hi = 0.0, 1.0
        for _ in range(50):
            t = (lo + hi) / 2
            if 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t * t * x2 + t**3 < p:
                lo = t
            else:
                hi = t
        return 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t * t * y2 + t**3

    return at


def stepped(ratio, at):
    """A move eased in and out over its first and last fifth whose speed steps
    `ratio`-fold at progress `at`, as a crane arm that suddenly runs faster."""
    n = 2000  # A guess at a lookup table fine enough to play smoothly.
    speed = []
    for k in range(n):
        p = (k + 0.5) / n
        v = 1 if p < at else ratio
        edge = min(p, 1 - p) / 0.2
        speed.append(v * (ease_in_out(edge) if edge < 1 else 1))
    done = list(itertools.accumulate(speed))
    return lambda p: done[min(n - 1, int(p * n))] / done[-1]


def phased(easing, ms, share, fps=flow.FPS):
    """(check-flow's verdict, start) on one move of ms from 100 ms plus `share` of
    a frame, sampled at fps as check-flow does, to 300 ms past its end."""
    start = 100 + share * 1000 / fps
    times = flow.sample_times(start + ms + 300, [start, start + ms], fps)
    return flow.analyse(
        sample((start, start + ms, easing), until=0, times=times)
    ), start


class Steps(unittest.TestCase):
    def test_a_4x_speed_step_mid_move_is_flagged_wherever_it_falls_in_a_frame(self):
        # The step lands at 400 ms plus a share of a frame, so the frame
        # straddling it reads any speed between the two.
        for share in (0, 0.25, 0.5, 0.75):
            r = flow.analyse(
                sample(
                    (100 + share * STEP, 700 + share * STEP, stepped(4, 0.5)), until=900
                )
            )
            [st] = r["steps"]
            self.assertEqual(
                (st["element"], st["way"], st["channels"]),
                ("el0", "up", ["position"]),
                share,
            )
            self.assertAlmostEqual(st["at"], 400 + share * STEP, delta=STEP)
            self.assertEqual(r["jolts"], [], share)

    def test_a_4x_slowdown_mid_move_is_flagged_from_fast_to_slow(self):
        r = flow.analyse(sample((100, 700, stepped(1 / 4, 0.5)), until=900))
        [st] = r["steps"]
        self.assertEqual((st["way"], st["to"]), ("down", 0.25))
        self.assertAlmostEqual(st["from"], 1, delta=0.02)

    def test_a_4x_step_spread_over_two_frames_is_flagged(self):
        speeds = [10] * 8 + [19, 35] + [40] * 8
        xs = [[sum(speeds[:k]) * STEP / 1000, 0] for k in range(len(speeds) + 1)]
        r = flow.analyse(
            {
                "times": [k * STEP for k in range(len(xs))],
                "elements": [{"label": "el", "channels": {"position": xs}}],
            }
        )
        [st] = r["steps"]
        self.assertEqual((st["way"], st["from"], st["to"]), ("up", 0.25, 1))
        self.assertAlmostEqual(st["at"], 9 * STEP, delta=STEP)

    def test_a_frame_reading_the_slower_speed_but_for_noise_is_not_between(self):
        # As a frame ending on the keyframe reads, from a 6-digit computed value (#126).
        speeds = [10] * 8 + [10.001] + [40] * 8
        xs = [[sum(speeds[:k]) * STEP / 1000, 0] for k in range(len(speeds) + 1)]
        r = flow.analyse(
            {
                "times": [k * STEP for k in range(len(xs))],
                "elements": [{"label": "el", "channels": {"position": xs}}],
            }
        )
        [st] = r["steps"]
        self.assertEqual((st["at"], st["channels"]), (round(9 * STEP), ["position"]))

    def test_a_step_under_a_fifth_of_top_speed_is_not_a_step(self):
        # A 1.5x step at 1.5 of a top of 20, then a smooth climb to that top.
        speeds = (
            [1] * 8 + [1.5] * 8 + [1.5 + 18.5 * k / 40 for k in range(1, 41)] + [20] * 8
        )
        xs = [[sum(speeds[:k]) * STEP / 1000, 0] for k in range(len(speeds) + 1)]
        r = flow.analyse(
            {
                "times": [k * STEP for k in range(len(xs))],
                "elements": [{"label": "el", "channels": {"position": xs}}],
            }
        )
        self.assertEqual(r["steps"], [])

    def test_a_1_35x_step_up_or_down_is_flagged_at_60_fps_wherever_it_falls(self):
        # Visible inside one motion at about 1.3x (#196).
        for ratio, at, share in itertools.product(
            (1.35, 1 / 1.35), (0.3, 0.5, 0.7), (0, 0.25, 0.5, 0.75)
        ):
            r, start = phased(stepped(ratio, at), 600, share)
            [st] = r["steps"]
            self.assertEqual(st["way"], "up" if ratio > 1 else "down", (ratio, at))
            self.assertAlmostEqual(st["at"], start + 600 * at, delta=STEP)

    def test_a_speed_change_under_the_step_line_is_not_a_step(self):
        for fps, share in itertools.product((30, 60, 120), (0, 0.25, 0.5, 0.75)):
            r, _ = phased(stepped(1.25, 0.5), 600, share, fps)
            self.assertEqual(r["steps"], [], (fps, share))

    def test_smooth_easings_and_overshoots_have_no_step(self):
        easings = {
            "ease": bezier(0.25, 0.1, 0.25, 1),
            "ease-in": bezier(0.42, 0, 1, 1),
            "ease-out": bezier(0, 0, 0.58, 1),
            "ease-in-out": bezier(0.42, 0, 0.58, 1),
            "smoothstep": ease_in_out,
            "quint in": lambda p: p**5,
            "overshoot": bezier(0.34, 1.56, 0.64, 1),
            "sine": lambda p: (1 - math.cos(math.pi * p)) / 2,
            # Steep, so they changed speed 2-4x in a frame or three
            # under a looser hold (#69 review).
            "expo in-out": bezier(0.87, 0, 0.13, 1),
            "Material decelerate": bezier(0.05, 0.7, 0.1, 1),
            "Material emphasized": bezier(0.2, 0, 0, 1),
            "Material standard decelerate": bezier(0, 0, 0, 1),
            "circ in-out": lambda p: (
                (1 - math.sqrt(1 - (2 * p) ** 2)) / 2
                if p < 0.5
                else (1 + math.sqrt(1 - (2 - 2 * p) ** 2)) / 2
            ),
        }
        for fps, (name, easing), ms, share in itertools.product(
            (30, 60, 120),
            easings.items(),
            (100, 150, 300, 500, 1000, 2000),
            (0, 0.25, 0.5, 0.75),
        ):
            r, _ = phased(easing, ms, share, fps)
            self.assertEqual(r["steps"], [], (fps, name, ms, share))

    def test_a_turn_in_a_bounce_or_an_overshoot_is_not_a_step(self):
        def bounce(p):
            for edge, top in (
                (1 / 2.75, 0),
                (2 / 2.75, 0.75),
                (2.5 / 2.75, 0.9375),
                (1, 0.984375),
            ):
                if p <= edge:
                    mid = {0: 0, 0.75: 1.5, 0.9375: 2.25, 0.984375: 2.625}[top] / 2.75
                    return 7.5625 * (p - mid) ** 2 + top
            return 1

        # Penner's easeInOutBack, whose overshoot constant this is.
        def back_in_out(p, c=1.70158 * 1.525):
            q = 2 * p
            return (
                q * q * ((c + 1) * q - c) / 2
                if p < 0.5
                else ((q - 2) ** 2 * ((c + 1) * (q - 2) + c) + 2) / 2
            )

        # Each changes speed 2-fold or more around a turn, so only the
        # same-way test keeps it out.
        for easing, ms in ((bounce, 600), (back_in_out, 150)):
            self.assertEqual(
                flow.analyse(sample((100, 100 + ms, easing), until=ms + 300))["steps"],
                [],
                ms,
            )


class Values(unittest.TestCase):
    """Computed values whose short and long forms must read as the same point."""

    def fade(self, prop, values):
        times = [k * STEP for k in range(len(values))]
        return flow.analyse(
            {"times": times, "elements": [{"label": "el", "channels": {prop: values}}]}
        )

    def test_an_opaque_colour_and_a_nearly_opaque_one_are_close(self):
        self.assertEqual(flow.numbers("color", "rgb(0, 0, 0)"), [0, 0, 0, 1])
        alphas = [1 - ease_in_out(k / 30) for k in range(31)]
        values = [
            "rgb(0, 0, 0)" if a == 1 else f"rgba(0, 0, 0, {a:.4f})" for a in alphas
        ]
        self.assertEqual(self.fade("color", values)["jolts"], [])

    def test_a_flat_transform_and_a_3d_one_are_one_kind_of_number(self):
        self.assertEqual(
            flow.numbers("transform", "none"),
            flow.numbers("transform", "matrix(1, 0, 0, 1, 0, 0)"),
        )
        self.assertEqual(len(flow.numbers("transform", "matrix(1, 0, 0, 1, 5, 6)")), 16)
        self.assertEqual(
            flow.numbers(
                "transform", "matrix3d(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)"
            ),
            flow.IDENTITY_3D,
        )
        angles = [60 * ease_in_out(k / 30) for k in range(31)]
        values = []
        for a in angles:
            c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
            values.append(
                "none"
                if a == 0
                else f"matrix3d({c}, 0, {-s}, 0, 0, 1, 0, 0, {s}, 0, {c}, 0, 0, 0, 0, 1)"
            )
        self.assertEqual(self.fade("transform", values)["jolts"], [])

    def test_scale_none_is_one(self):
        self.assertEqual(flow.numbers("scale", "none"), flow.numbers("scale", "1"))
        self.assertEqual(flow.numbers("scale", "1.5"), [1.5, 1.5, 1])
        self.assertEqual(flow.numbers("scale", "1.5 2"), [1.5, 2, 1])


class PageQuiet(unittest.TestCase):
    """When the page counts as done playing, from its status (#135)."""

    def status(self, **over):
        return {
            "now": 400,
            "firstFrame": 20,
            "lastNew": 0,
            "running": 0,
            "timer": None,
            "framing": False,
            **over,
        }

    def test_the_quiet_window_runs_from_the_first_frame(self):
        # A busy machine delayed this page's first frame past the window, and
        # its frame loop had written nothing yet.
        self.assertFalse(flow.settled(self.status(firstFrame=350), 300))
        self.assertTrue(flow.settled(self.status(now=650, firstFrame=350), 300))

    def test_a_page_with_no_frame_drawn_has_not_settled(self):
        self.assertFalse(flow.settled(self.status(now=5000, firstFrame=None), 300))

    def test_a_page_that_never_draws_a_frame_times_out(self):
        page = types.SimpleNamespace(
            evaluate=lambda *a: self.status(now=99999, firstFrame=None),
            wait_for_timeout=lambda ms: None,
        )
        with self.assertRaisesRegex(flow.PageTimeoutError, "no frame drawn"):
            # Any quiet and timeout: the fake page's clock already reads past both.
            flow.settle(page, types.SimpleNamespace(quiet=300, timeout=1000))


def run(page, *extra, out=None):
    """Runs the script on a fixture page; returns its process and, where it
    measured, its flow.json and speed.svg. Given `out`, it writes there and
    leaves the files for the caller."""
    with tempfile.TemporaryDirectory() as scratch:
        out = out or scratch
        # A guess for check-flow.py alone, not taken from the other tests' timeouts: one run takes seconds here.
        proc = child.run(
            [
                sys.executable,
                SCRIPT,
                os.path.join(FIXTURES, page),
                "--out",
                out,
                "--quiet",
                "300",
                *extra,
            ],
            timeout=120,
        )
        if not os.path.exists(os.path.join(out, "flow.json")):
            return proc, None, None
        with open(os.path.join(out, "flow.json"), encoding="utf8") as fh:
            data = json.load(fh)
        with open(os.path.join(out, "speed.svg"), encoding="utf8") as fh:
            return proc, data, fh.read()


def run_page(html):
    """Runs the script on a page written from `html`; returns its process and flow.json."""
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "page.html")
        with open(path, "w", encoding="utf8") as fh:
            fh.write(html)
        proc, data, _ = run(path)
    return proc, data


class Measured(unittest.TestCase):
    # Time zero is the page's first frame, which the animations can follow by
    # several frames on a busy machine (#126), so times are taken from their
    # own start: both are made by one script.
    @classmethod
    def setUpClass(cls):
        cls.proc, cls.data, cls.svg = run("pause-and-jolt.html")
        cls.start = cls.data["edges_ms"][0]

    def test_it_exits_1_on_a_pause_or_jolt(self):
        self.assertEqual(self.proc.returncode, 1, self.proc.stdout + self.proc.stderr)

    def test_the_known_pause_is_found(self):
        self.assertEqual(len(self.data["pauses"]), 1)
        p = self.data["pauses"][0]
        self.assertAlmostEqual(p["start"] - self.start, 1000, delta=2 * STEP)
        self.assertAlmostEqual(p["end"] - self.start, 1600, delta=2 * STEP)
        self.assertIn(
            f"\n  {p['start']}–{p['end']} ms ({p['ms']} ms)\n", self.proc.stdout
        )

    def test_the_known_jolts_are_found_and_nothing_else(self):
        got = [(j["element"], j["edge"], j["share"]) for j in self.data["jolts"]]
        self.assertEqual(got, [("div#dash", "starts", 1), ("div#dash", "stops", 1)])
        self.assertAlmostEqual(self.data["jolts"][0]["at"] - self.start, 1600, delta=1)
        self.assertAlmostEqual(self.data["jolts"][1]["at"] - self.start, 2400, delta=1)

    def test_the_length_runs_from_the_first_move_to_the_last_animation_end(self):
        # From the first move, not the first frame, so a font wait before it is
        # not counted (#169 Q3 (A)).
        self.assertEqual(self.data["first_move_ms"], self.start)
        self.assertAlmostEqual(self.data["length_ms"], 2400, delta=1)
        self.assertIn(
            f"\nlength: {self.data['length_ms']:.0f} ms, from the first move at {self.start:.0f} ms\n",
            self.proc.stdout,
        )

    def test_a_finished_fill_none_animation_is_still_measured(self):
        self.assertIn("div#glide", [e["label"] for e in self.data["elements"]])

    def test_it_writes_the_chart(self):
        self.assertIn("div#dash", self.svg)
        self.assertEqual(self.svg.count("<circle"), 2)


class UnseenPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc, cls.data, cls.svg = run("unseen.html")

    def test_only_starts_seen_at_rest_are_judged(self):
        self.assertEqual(self.proc.returncode, 1, self.proc.stdout + self.proc.stderr)
        seen = ["div#drop", "div#escape", "div#pinned", "div#shown", "div#wrap"]
        self.assertEqual(
            [(j["element"], j["edge"]) for j in self.data["jolts"]],
            [(label, "starts") for label in seen],
        )
        self.assertEqual([j["element"] for j in self.data["jumps"]], seen)

    def test_each_unseen_start_is_listed_with_what_it_would_be(self):
        got = {u["element"]: (u["edge"], u["would_be"]) for u in self.data["unseen"]}
        self.assertEqual(
            got,
            {
                label: ("starts", ["jolt", "jump"])
                for label in (
                    "div#enter",
                    "div#flush",
                    "div#word",
                    "div#reveal",
                    "div#fade",
                )
            },
        )
        self.assertIn(
            "not judged, where the viewer never sees the element at rest",
            self.proc.stdout,
        )
        self.assertIn("  div#fade starts at ", self.proc.stdout)

    def test_the_jumps_are_printed_and_drawn(self):
        # A start a fraction of a ms past the first frame can round to 36 px (#326).
        self.assertRegex(
            self.proc.stdout,
            r"\njumps, a move from rest whose first frame carries its box 10 px \(0\.26° from 60 cm\) or more: 5\n"
            r"  div#drop starts at \d+ ms, 3\d(\.\d)? px in its first frame\n",
        )
        self.assertIn("Red triangle: a jump.", self.svg)
        self.assertEqual(self.svg.count("<path d="), 5)


# Holds the frame it runs in 50 ms, three frames.
HOLD_MS = "const end = performance.now() + 50; while (performance.now() < end);"
HOLD_FIRST_FRAME = "requestAnimationFrame(() => { " + HOLD_MS + " });\n"


class UnseenPageHeld(UnseenPage):
    # The first frame is held, so every animation starts after it, as a loaded
    # machine starts them, and waits there at its first keyframe (#326).
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(FIXTURES, "unseen.html"), encoding="utf8") as fh:
            html = fh.read().replace("</script>", HOLD_FIRST_FRAME + "</script>")
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "unseen-held.html")
            with open(path, "w", encoding="utf8") as fh:
                fh.write(html)
            cls.proc, cls.data, cls.svg = run(path)


# #word in a line that clips it, moved up into it from below as unseen.html's.
WORD_PAGE = """<!doctype html><style>body { margin: 0; }
#line { position: absolute; top: 200px; width: 200px; height: 40px; overflow: hidden; }
#word { width: 40px; height: 40px; background: #333; }</style>
<div id="line"><div id="word"></div></div><script>
const move = () => word.animate([{ transform: "translateY(300px)" }, { transform: "translateY(0)" }],
  { duration: 400, easing: "cubic-bezier(0.33, 1, 0.68, 1)", fill: "forwards" });
"""


class WaitingStart(unittest.TestCase):
    def test_an_animation_made_in_a_frame_waits_there_at_its_first_keyframe(self):
        page = (
            WORD_PAGE
            + "requestAnimationFrame(() => { move(); "
            + HOLD_MS
            + " });\n</script>"
        )
        proc, data = run_page(page)
        self.assertEqual(
            [u["element"] for u in data["unseen"]],
            ["div#word"],
            proc.stdout + proc.stderr,
        )
        self.assertEqual(data["jumps"], [])

    def test_an_animation_made_later_shows_the_style_before_it_until_then(self):
        # #word shows in its line until a timer starts it from below the line,
        # 500 ms in, well after the first frames, so it jumps out of sight from
        # a seen rest (#326).
        proc, data = run_page(WORD_PAGE + "setTimeout(move, 500);\n</script>")
        self.assertEqual(data["unseen"], [], proc.stdout + proc.stderr)
        self.assertEqual([j["element"] for j in data["jumps"]], ["div#word"])

    def test_a_delay_ending_mid_frame_moves_part_of_a_frame_first(self):
        # 300 px over 450 ms, linear: a whole frame's 11.1 px would be a jump,
        # but the delay ends 25 ms in, so the frame drawn next carries 5.6 px.
        page = """<!doctype html><div id="box" style="width:40px;height:40px;background:#333"></div><script>
box.animate([{ transform: "translateX(0)" }, { transform: "translateX(300px)" }],
  { duration: 450, delay: 25, fill: "forwards" });
</script>"""
        proc, data = run_page(page)
        self.assertEqual(data["jumps"], [], proc.stdout + proc.stderr)


class Pages(unittest.TestCase):
    def test_eased_moves_placed_at_their_real_starts_pass(self):
        proc, data, _ = run("smooth.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(data["pauses"], [])
        self.assertEqual(data["jolts"], [])
        # A busy machine fires the timer late, never early (#135).
        self.assertGreaterEqual(data["length_ms"], 2000 - 3 * STEP)

    def test_a_wait_before_the_first_move_is_not_in_the_length(self):
        # A headline held still 800 ms, as a font wait holds one, then a 1000 ms
        # fade: the length is the fade's (#169 Q3 (A)).
        page = """<!doctype html><h1 id="title">Wait</h1><script>
title.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 1000, delay: 800, easing: "ease-in-out", fill: "both" });
</script>"""
        proc, data = run_page(page)
        # It exits 1 on the still start, which is #220's to rule on.
        self.assertIn(proc.returncode, (0, 1), proc.stdout + proc.stderr)
        self.assertAlmostEqual(data["length_ms"], 1000, delta=1)
        self.assertGreaterEqual(data["first_move_ms"], 800)

    def test_a_reversed_animation_on_no_element_of_the_page_is_not_refused(self):
        # One on a detached element and one with no target (#359 review).
        page = """<!doctype html><h1 id="title">Off</h1><script>
document.createElement("div").animate([{ opacity: 0 }, { opacity: 1 }], 400).reverse();
new Animation(new KeyframeEffect(null, [{ opacity: 0 }, { opacity: 1 }], 400)).reverse();
title.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, fill: "forwards" });
</script>"""
        proc, data = run_page(page)
        self.assertNotIn("in reverse", proc.stdout)
        self.assertIsNotNone(data, proc.stdout + proc.stderr)

    def test_forward_animations_that_end_between_two_frames_are_measured(self):
        # Each is started after its frame's scans and ended by the next frame (#369).
        proc, data, _ = run("forward-gap.html")
        self.assertIsNotNone(data, proc.stdout + proc.stderr)
        self.assertEqual(
            sorted(e["label"] for e in data["elements"]),
            ["div#a1", "div#a2", "div#box", "div#c1", "div#c2", "div#late"],
        )

    def test_a_storyboard_on_a_starved_browser_is_not_a_script_loop(self):
        # Five colour changes 300 ms apart, while every frame is held 80 ms:
        # three frames apart, not consecutive, so not a loop (#135).
        page = """<!doctype html><h1 id="title">Story</h1><div id="box" style="width:40px;height:40px;background:#000"></div>
<script>
box.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 1800, easing: "ease-in-out", fill: "forwards" });
for (let k = 1; k <= 5; k++) setTimeout(() => { title.style.color = "#" + k + k + k; }, 300 * k);
let first = null;
requestAnimationFrame(function tick(now) {
  if (first === null) first = now;
  const held = performance.now();
  while (performance.now() - held < 80);
  if (now - first < 1800) requestAnimationFrame(tick);
});
</script>"""
        proc, data = run_page(page)
        self.assertNotEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertEqual([e["label"] for e in data["elements"]], ["div#box"])

    def test_a_storyboard_sequenced_by_a_long_timer_is_measured_whole(self):
        proc, data, _ = run("late.html")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        # The timer starts counting before the page's first frame, which a busy
        # machine delays, and fires late there too, as on a real page, so the
        # second beat's start is read from its own end, 500 ms before the
        # length (#135). Missed, the length would be the first beat's 500 ms;
        # 2500 allows a first frame up to 500 ms late.
        second = data["first_move_ms"] + data["length_ms"] - 500
        self.assertGreaterEqual(second, 2500)
        [p] = data["pauses"]
        self.assertAlmostEqual(p["start"], 500, delta=2 * STEP)
        self.assertAlmostEqual(p["end"], second, delta=2 * STEP)
        self.assertEqual(
            [(j["element"], j["edge"]) for j in data["jolts"]],
            [("div#second", "starts"), ("div#second", "stops")],
        )

    def test_a_fall_into_its_landing_passes_where_a_bare_fall_jolts(self):
        f = landing()
        page = f"""<!doctype html><style>div {{ position: absolute; top: 0; width: 40px; height: 40px; background: #000; }}</style>
<div id="bare" style="left: 0"></div><div id="landed" style="left: 100px"></div>
<script>
const drop = [{{ transform: "none" }}, {{ transform: "translateY({f["drop"]}px)" }}];
const fill = "forwards";
bare.animate(drop, {{ duration: {f["fallMs"]}, easing: "cubic-bezier(0.333333, 0, 0.666667, 0.333333)", fill }});
landed.animate(drop, {{ duration: {f["ms"]}, easing: "{f["easing"]}", fill }});
</script>"""
        proc, data = run_page(page)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("div#landed", [e["label"] for e in data["elements"]])
        self.assertEqual(
            {(j["element"], j["edge"]) for j in data["jolts"]}, {("div#bare", "stops")}
        )

    def test_a_heavy_settle_plays_without_a_jolt(self):
        f = settled(300, 900)
        page = f"""<!doctype html><style>div {{ position: absolute; top: 0; width: 40px; height: 40px; background: #000; }}</style>
<div id="settled"></div>
<script>
settled.animate([{{ transform: "none" }}, {{ transform: "translateX({f["distance"]}px)" }}], {{ duration: {f["ms"]}, easing: "{f["easing"]}", fill: "forwards" }});
</script>"""
        proc, data = run_page(page)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual([e["label"] for e in data["elements"]], ["div#settled"])
        self.assertEqual((data["jolts"], data["steps"]), ([], []))

    def test_a_jump_alone_exits_1(self):
        # 300 px in 150 ms, too short for a jolt line (#297).
        page = """<!doctype html><style>div { position: absolute; top: 0; width: 40px; height: 40px; background: #000; }</style>
<div id="dash"></div>
<script>
dash.animate([{ transform: "none" }, { transform: "translateX(300px)" }], { duration: 150, easing: "linear", fill: "forwards" });
</script>"""
        proc, data = run_page(page)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertEqual((data["jolts"], len(data["jumps"])), ([], 1))
        # A start a fraction of a ms past the first frame can round to 36 px (#326).
        self.assertRegex(
            proc.stdout,
            r"\n  div#dash starts at \d+ ms, 3\d(\.\d)? px in its first frame\n",
        )

    def test_a_crane_arm_that_suddenly_turns_4x_faster_is_a_step_and_exits_1(self):
        # It starts at a quarter of its top speed and eases out of it, so the
        # step is its only finding. Its delays put its keyframes 0.67-7 ms off
        # a frame (#126).
        for delay in (5.5, 7, 16):
            with self.subTest(delay=delay):
                self.crane_arm(delay)

    def crane_arm(self, delay):
        page = """<!doctype html><style>div { position: absolute; left: 100px; top: 100px; width: 200px; height: 10px; background: #000; }</style>
<div id="arm"></div>
<script>
arm.animate([{ transform: "rotate(0deg)" }, { transform: "rotate(10deg)", offset: 0.4 },
  { transform: "rotate(50deg)", offset: 0.8, easing: "cubic-bezier(0.333333, 0.666667, 0.666667, 1)" }, { transform: "rotate(60deg)" }],
  { duration: 1000, delay: DELAY, fill: "forwards" });
</script>""".replace("DELAY", str(delay))
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "arm.html")
            with open(path, "w", encoding="utf8") as fh:
                fh.write(page)
            proc, data, svg = run(path)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertEqual((data["pauses"], data["jolts"]), ([], []))
        [st] = data["steps"]
        self.assertEqual(
            (st["element"], st["way"], st["from"], st["to"]), ("div#arm", "up", 0.25, 1)
        )
        self.assertIn("transform", st["channels"])
        self.assertAlmostEqual(st["at"] - data["edges_ms"][0], 400, delta=1)
        self.assertRegex(
            proc.stdout,
            r"\n  div#arm steps up at \d+ ms, from 25% to 100% of its top speed \(",
        )
        self.assertEqual(svg.count('width="10" height="10"'), 1)

    def test_each_keyframe_inside_an_animation_is_sampled_at_its_exact_time(self):
        _, data, _ = run("keyframe-hold.html")
        # Measured from the animation's own start, which time zero can precede.
        start = data["edges_ms"][0]
        self.assertEqual(
            [round(e - start, 3) for e in data["edges_ms"]],
            [0, 0, 377, 1000, 1000, 1623, 2000, 2000],
        )
        for e in data["edges_ms"]:
            self.assertTrue(any(abs(t - e) < 1 for t in data["times"]), e)


class Refused(unittest.TestCase):
    def refuses(self, page, why, *extra):
        proc, data, _ = run(page, *extra)
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn("cannot measure", proc.stdout)
        self.assertIn(why, proc.stdout)
        self.assertNotIn("pauses,", proc.stdout)
        self.assertIsNone(data)

    def test_a_canvas(self):
        self.refuses("canvas.html", "canvas#stage")

    def test_a_video(self):
        self.refuses("video.html", "plays a video (video#clip)")

    def test_a_frame_and_an_object(self):
        self.refuses("embed.html", "embeds another document (iframe#frame, object#doc)")

    def test_svg_smil(self):
        self.refuses("smil.html", "animates SVG with SMIL")

    def test_shadow_dom(self):
        self.refuses("shadow.html", "has shadow DOM")

    def test_a_scroll_driven_timeline(self):
        self.refuses("scroll-timeline.html", "by scroll position, not time")

    def test_an_animation_played_in_reverse(self):
        self.refuses("reverse.html", "in reverse")

    def test_a_reversed_animation_that_ends_between_two_frames(self):
        # A reversed animation is missing from getAnimations() until it starts (#359).
        self.refuses("reverse-gap.html", "in reverse")

    def test_an_animation_a_script_seeks_by_hand(self):
        self.refuses("hand-seek.html", "seeks by hand")

    def test_a_script_moving_an_element_frame_by_frame(self):
        self.refuses("script-loop.html", "from a script, frame by frame (div#loop)")

    def test_a_script_moving_an_element_frame_by_frame_at_11_fps(self):
        self.refuses(
            "script-loop-starved.html", "from a script, frame by frame (div#loop)"
        )

    def test_a_scroll_handler_on_a_short_page(self):
        self.refuses(
            "scroll-handler.html", "from a script, frame by frame (div#follow)"
        )

    def test_a_script_stepping_an_element_by_class_frame_by_frame(self):
        self.refuses("class-loop.html", "from a script, frame by frame (div#sprite)")

    def test_a_transition_that_starts_on_scroll(self):
        self.refuses("scroll-reveal.html", "when the page is scrolled")

    def test_a_timer_due_past_the_timeout(self):
        self.refuses("long-timer.html", "past --timeout", "--timeout", "3000")

    def test_a_morph_scrolling_drives(self):
        self.refuses(
            "morph-scroll.html",
            "rewrites the d of 1 path(s) when the page is scrolled (path#arch)",
        )

    def test_a_page_with_no_animation(self):
        self.refuses("still.html", "no Web Animations API animation")


class GoneProcess(unittest.TestCase):
    """A process that exits between being listed and being read has no
    command line, children or driver (#432, #464)."""

    def test_an_exited_process_reads_as_empty(self):
        gone = subprocess.Popen(["true"])
        gone.wait()
        self.assertEqual(flow.process_args(gone.pid), [])
        self.assertEqual(flow.descendants(gone.pid), [])
        self.assertIsNone(flow.driver_pid(gone.pid))


class Arguments(unittest.TestCase):
    def test_a_viewport_that_is_not_w_by_h_is_a_usage_error(self):
        proc, data, _ = run("still.html", "--viewport", "1280")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("--viewport wants WxH, e.g. 1920x945 — got '1280'", proc.stderr)
        self.assertIsNone(data)


def raises(exc):
    def work():
        raise exc

    return work


class RunBrowser(unittest.TestCase):
    """The exit ladder every design-round browser script shares (#131)."""

    def exits(self, work, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            got = flow.run_browser(work, 5000, *args)
        return got, out.getvalue(), err.getvalue()

    def test_a_result_returns_with_no_exit_code(self):
        self.assertEqual(self.exits(lambda: 7, "file:///p.html"), ((7, None), "", ""))

    def test_the_hint_names_the_plugins_pinned_requirements(self):
        self.assertEqual(
            os.path.realpath(flow.REQUIREMENTS), os.path.realpath(REQUIREMENTS)
        )
        self.assertIn(f"-r {flow.REQUIREMENTS}\n", flow.INSTALL_HINT)
        with open(REQUIREMENTS, encoding="utf-8") as f:
            pins = [
                line.split("==")
                for line in f
                if line.strip() and not line.startswith("#")
            ]
        self.assertEqual(
            sorted(name for name, _ in pins), ["Pillow", "numpy", "playwright", "scipy"]
        )

    def test_each_failure_exits_with_its_code_and_message(self):
        url = "file:///p.html"
        for exc, code, said in [
            (
                ImportError("no playwright"),
                3,
                "Playwright is not importable here.\n" + flow.INSTALL_HINT,
            ),
            (
                flow.NoBrowserError("no chromium"),
                3,
                "its browser is not: no chromium\n" + flow.INSTALL_HINT,
            ),
            (
                flow.RefusedError("net::ERR"),
                5,
                f"the browser could not load {url}: net::ERR",
            ),
            (
                flow.PageTimeoutError("goto"),
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
        _, _, err = self.exits(raises(flow.RefusedError("mark.svg: bad image")))
        self.assertEqual(err, "the browser could not draw mark.svg: bad image\n")
        _, _, err = self.exits(raises(flow.PageTimeoutError("decode")))
        self.assertEqual(err, "timed out after 5000ms: decode\n")

    def test_an_unmeasurable_page_prints_its_reasons_between_the_two_lines_on_stdout(
        self,
    ):
        got, out, err = self.exits(
            raises(flow.UnmeasurableError(["a", "b"])), "u", ("head", "tail")
        )
        self.assertEqual((got, out, err), ((None, 6), "head\n  - a\n  - b\ntail\n", ""))

    def test_an_unmeasurable_page_where_the_script_names_no_lines_is_not_swallowed(
        self,
    ):
        with self.assertRaises(flow.UnmeasurableError):
            self.exits(raises(flow.UnmeasurableError(["a"])), "u")


# These cases cross real processes and the real clock: the hang is Chromium's
# own, and the watch reads /proc. What is tested is that the watch fires, not
# when. The watch's windows, cut from RENDERER_GONE_S and UNANSWERED_S to keep
# each case short: a guess, four watch polls.
TEST_WINDOW_S = 1
# Over TEST_WINDOW_S and a poll, so a watch that misjudged would fire.
PAST_WINDOW_S = 2.5
# The killer's poll: a guess, a fifth of WATCH_POLL_S, so a renderer is killed
# before the watch's next read.
KILL_POLL_S = 0.05
# A case still running after this has hung: a guess, far over a browser start
# on a loaded machine.
CASE_LIMIT_S = 60
# Chromium's own flag: each renderer waits at start for a debugger's signal.
PAUSED_AT_START = ["--renderer-startup-dialog"]


def renderer_pids():
    """The renderers this process's browsers run, read from /proc."""
    return [
        pid
        for pid in flow.descendants(os.getpid())
        if "--type=renderer" in flow.process_args(pid)
    ]


@contextlib.contextmanager
def renderers_killed():
    """SIGTERMs each renderer this process's browsers start (#432). A browser launched with PAUSED_AT_START holds each
    renderer at its start, so the kill lands there."""
    stop = threading.Event()

    def kill():
        while not stop.wait(KILL_POLL_S):
            for pid in renderer_pids():
                # A renderer that exited since the read is already gone.
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
    """SIGTERMs each renderer this process's browsers run, and returns once /proc
    shows none."""
    end = time.monotonic() + CASE_LIMIT_S
    while running := renderer_pids():
        if time.monotonic() > end:
            raise AssertionError(f"renderers {running} still running")
        for pid in running:
            with contextlib.suppress(ProcessLookupError):
                os.kill(pid, signal.SIGTERM)
        time.sleep(KILL_POLL_S)


def renderers_frozen():
    """SIGSTOPs each renderer this process's browsers run, leaving it alive and
    never answering (#459)."""
    for pid in renderer_pids():
        os.kill(pid, signal.SIGSTOP)


class HungCalls(unittest.TestCase):
    """A call whose renderer dies as it starts (#432), or a resize (#459) or CDP
    send (#464) whose live renderer never answers, waits for ever with nothing raised; the
    launcher's watch ends it."""

    def exits(self, work):
        """run_browser(work)'s result and stderr."""
        done = {}

        def run():
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                done["got"] = flow.run_browser(work, flow.LOAD_TIMEOUT_MS)
            done["err"] = err.getvalue()

        runner = threading.Thread(target=run, daemon=True)
        with mock.patch.multiple(
            flow, RENDERER_GONE_S=TEST_WINDOW_S, UNANSWERED_S=TEST_WINDOW_S
        ):
            runner.start()
            runner.join(CASE_LIMIT_S)
        if runner.is_alive():
            self.fail(f"still waiting after {CASE_LIMIT_S} s: the watch did not fire")
        return done["got"], done["err"]

    def test_a_renderer_killed_as_it_starts_exits_7_naming_the_call(self):
        # With PAUSED_AT_START, the kill lands while new_page waits on the
        # renderer it starts. Landing after Playwright has sent the page's setup,
        # it leaves new_page waiting for the watch; landing before, as a loaded
        # machine slows the driver, it makes new_page raise (#472).
        def work():
            with flow.chromium(PAUSED_AT_START) as browser:
                browser.new_context().new_page()

        with renderers_killed():
            got, err = self.exits(work)
        self.assertEqual(got, (None, 7), err)
        self.assertRegex(
            err,
            r"^BrowserContext\.new_page at check-flow\.test\.py:\d+ "
            rf"(waited {TEST_WINDOW_S} s|raised .*) "
            "with the browser running no renderer",
        )

    def test_a_call_waiting_as_its_renderer_dies_exits_7_naming_the_call(self):
        # The kill waits for the page's script to fetch, so it lands while the
        # call is waiting in the renderer: nothing is raised (#432, #472).
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
            with flow.chromium() as browser:
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
            rf"^Page\.evaluate at check-flow\.test\.py:{call['line']} "
            rf"waited {TEST_WINDOW_S} s with the browser running no renderer",
        )

    def test_a_call_on_a_page_whose_renderer_died_exits_7_naming_the_call(self):
        # Made once Playwright has heard of the crash, the call raises (#472).
        def work():
            with flow.chromium() as browser:
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
            rf"^Page\.evaluate at check-flow\.test\.py:{call['line']} raised .* "
            "with the browser running no renderer",
        )

    def test_a_refused_load_with_its_renderer_alive_exits_5_naming_the_call(self):
        def work():
            with flow.chromium() as browser:
                # Port 1 has no listener: the load is refused at once.
                browser.new_page().goto("http://127.0.0.1:1/")

        got, err = self.exits(work)
        self.assertEqual(got, (None, 5), err)
        self.assertRegex(err, r"^the browser could not draw Page\.goto")

    def test_a_call_after_its_browser_died_exits_5_naming_the_call(self):
        # No renderer runs, but the browser died, closing its pages first.
        def work():
            with flow.chromium() as browser:
                page = browser.new_page()
                (pid,) = flow.browser_pids(flow.descendants(os.getpid()))
                os.kill(pid, signal.SIGKILL)
                end = time.monotonic() + CASE_LIMIT_S
                while flow.process_args(pid):
                    if time.monotonic() > end:
                        raise AssertionError(f"browser {pid} still running")
                    time.sleep(KILL_POLL_S)
                page.evaluate("1 + 1")

        got, err = self.exits(work)
        self.assertEqual(got, (None, 5), err)
        self.assertRegex(err, r"^the browser could not draw Page\.evaluate")

    def test_a_call_on_a_page_it_closed_exits_5_naming_the_call(self):
        # No renderer runs, but none died: the script closed its own page.
        def work():
            with flow.chromium() as browser:
                page = browser.new_page()
                page.close()
                renderers_ended()
                page.evaluate("1 + 1")

        got, err = self.exits(work)
        self.assertEqual(got, (None, 5), err)
        self.assertRegex(err, r"^the browser could not draw Page\.evaluate")

    def test_a_long_call_with_its_renderer_alive_is_left_to_finish(self):
        def work():
            with flow.chromium() as browser:
                page = browser.new_page()
                page.wait_for_timeout(PAST_WINDOW_S * 1000)
                return page.evaluate("1 + 1")

        self.assertEqual(self.exits(work), ((2, None), ""))

    def test_with_no_browser_found_in_proc_it_says_no_watch_runs(self):
        def work():
            with mock.patch.object(flow, "browser_pids", return_value=[]):
                with flow.chromium() as browser:
                    return browser.new_page().evaluate("1 + 1")

        got, err = self.exits(work)
        self.assertEqual(got, (2, None))
        self.assertRegex(err, r"^no call watch: /proc shows 0 new browser processes")

    def test_a_resize_its_live_renderer_never_answers_exits_7_naming_the_call(self):
        # The hang #459 saw: a renderer alive, never answering a resize.
        def work():
            with flow.chromium() as browser:
                page = browser.new_page()
                renderers_frozen()
                page.set_viewport_size({"width": 500, "height": 500})

        got, err = self.exits(work)
        self.assertEqual(got, (None, 7), err)
        self.assertRegex(
            err,
            r"^Page\.set_viewport_size at check-flow\.test\.py:\d+ "
            rf"waited {TEST_WINDOW_S} s for a renderer that is alive but never answered",
        )

    def test_resizes_one_after_another_past_the_window_are_left_to_finish(self):
        # Each resize at the one line is a new call, not one call waiting.
        def work():
            with flow.chromium() as browser:
                page = browser.new_page()
                end = time.monotonic() + PAST_WINDOW_S
                width = 400
                while time.monotonic() < end:
                    width = 900 - width
                    page.set_viewport_size({"width": width, "height": 500})
                return page.evaluate("1 + 1")

        self.assertEqual(self.exits(work), ((2, None), ""))

    def test_a_cdp_send_its_live_renderer_never_answers_exits_7_naming_the_call(self):
        # Its partner (#464) is the resize loop's case: both reach the watch
        # through UNTIMED_CALLS.
        def work():
            with flow.chromium() as browser:
                page = browser.new_page()
                cdp = page.context.new_cdp_session(page)
                renderers_frozen()
                cdp.send("Page.setFontSizes", {"fontSizes": {"standard": 20}})

        got, err = self.exits(work)
        self.assertEqual(got, (None, 7), err)
        self.assertRegex(
            err,
            r"^CDPSession\.send at check-flow\.test\.py:\d+ "
            rf"waited {TEST_WINDOW_S} s for a renderer that is alive but never answered",
        )

    def test_a_script_working_with_no_page_open_is_left_to_finish(self):
        def work():
            with flow.chromium() as browser:
                browser.new_page().close()
                time.sleep(PAST_WINDOW_S)
                return browser.new_page().evaluate("1 + 1")

        self.assertEqual(self.exits(work), ((2, None), ""))


class RendererDeath(unittest.TestCase):
    """CallWatch.renderer_death's verdict on an error raised from a stand-in
    Playwright package, with the browser alive and running no renderer (#472).
    A real new_page raises only where the kill beats Playwright's page setup,
    which no case can order."""

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
        spec = importlib.util.spec_from_file_location("api", path)
        api = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(api)
        # A live process with no children stands in for the browser.
        browser = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(60)"]
        )
        self.addCleanup(browser.wait)
        self.addCleanup(browser.kill)
        try:
            getattr(api.BrowserContext(), method)()
        except RuntimeError as exc:
            raised = exc
        watch = flow.CallWatch(browser.pid, greenlet.getcurrent(), package + os.sep)
        try:
            return watch.renderer_death(raised, page_open)
        finally:
            watch.stop()

    def test_new_page_raising_with_no_page_open_is_a_renderer_death(self):
        self.assertRegex(
            self.death("new_page", page_open=False) or "",
            r"^BrowserContext\.new_page at check-flow\.test\.py:\d+ raised "
            "'Target page, context or browser has been closed' with the browser running no renderer",
        )

    def test_another_call_raising_with_no_page_open_is_not(self):
        self.assertIsNone(self.death("new_cdp_session", page_open=False))

    def test_another_call_raising_with_a_page_open_is_a_renderer_death_naming_the_call(
        self,
    ):
        self.assertRegex(
            self.death("new_cdp_session", page_open=True) or "",
            r"^BrowserContext\.new_cdp_session at check-flow\.test\.py:\d+ raised ",
        )


class Sweep(unittest.TestCase):
    def test_a_scroll_handler_writes_in_consecutive_frames(self):
        from playwright.sync_api import sync_playwright

        with sync_playwright() as play:
            browser = play.chromium.launch()
            try:
                context = browser.new_context()
                context.add_init_script(flow.COLLECTOR_JS)
                page = context.new_page()
                page.goto(
                    "file://"
                    + os.path.abspath(os.path.join(FIXTURES, "scroll-handler.html"))
                )
                flow.sweep(page)
                [log] = page.evaluate(
                    "() => [...window.__flow.rewrites.values()].map((log) => log.map((w) => w.frame))"
                )
            finally:
                browser.close()
        self.assertGreaterEqual(len(log), 10)
        self.assertEqual(
            [b - a for a, b in itertools.pairwise(log)], [1] * (len(log) - 1)
        )


# A morph: a path whose d a script rewrites frame by frame (#72).
FROM = "M 0 300 C 0 233 0 167 0 100 C 0 45 45 0 100 0 C 155 0 200 45 200 100 Z"
TO = "M 0 300 C 0 283 0 267 0 250 C 0 167 67 100 150 100 C 233 100 300 167 300 250 Z"


def between(p):
    """FROM morphed toward TO by p, number by number, as a script writes it."""
    a, b = FROM.split(" "), TO.split(" ")
    return " ".join(
        x if x.isalpha() else f"{float(x) + (float(y) - float(x)) * p:.2f}"
        for x, y in zip(a, b, strict=True)
    )


def writes(progress, frame_times):
    """The writes a script makes at each frame time: progress(t) gives p, and a
    frame whose d is unchanged writes nothing, as the collector sees it."""
    out, d, prev = [], FROM, None
    for t in frame_times:
        new = between(progress(t))
        if new != d:
            out.append({"ms": t, "prev_ms": prev, "old": d, "value": new})
            d = new
        prev = t
    return out


def frames(until):
    return [k * STEP for k in range(round(until / STEP) + 1)]


def eased(start, ms):
    return lambda t: ease_in_out(min(1, max(0, (t - start) / ms)))


def morph_measured(w, until):
    """analyse()'s result for one morph's writes, sampled at 60 fps."""
    s = {
        "times": flow.sample_times(until, [], 60),
        "elements": [],
        "morphs": [{"label": "path#arch", "writes": w}],
    }
    flow.add_morphs(s)
    return flow.analyse(s)


class MorphPoints(unittest.TestCase):
    def test_a_write_every_frame_is_one_point_per_frame(self):
        w = writes(eased(0, 500), frames(500))
        self.assertEqual(
            flow.morph_points(w), [(x["ms"], flow.path_numbers(x["value"])) for x in w]
        )

    def test_a_held_shape_is_still_until_the_frame_before_the_next_write(self):
        w = [
            {"ms": 0, "prev_ms": None, "old": FROM, "value": between(0.5)},
            {
                "ms": 400,
                "prev_ms": 400 - STEP,
                "old": between(0.5),
                "value": between(1),
            },
        ]
        pts = flow.morph_points(w)
        self.assertEqual([t for t, _ in pts], [0, 400 - STEP, 400])
        self.assertEqual(flow.morph_at(pts, 200), flow.morph_at(pts, 0))

    def test_numbers_are_interpolated_one_by_one_and_held_at_either_end(self):
        pts = [(100, [0, 0, 10, 0, 20, 0, 30, 0]), (200, [10, 0, 20, 0, 40, 0, 50, 0])]
        self.assertEqual(flow.morph_at(pts, 150), [5, 0, 15, 0, 30, 0, 40, 0])
        self.assertEqual(flow.morph_at(pts, 0), [0, 0, 10, 0, 20, 0, 30, 0])
        self.assertEqual(flow.morph_at(pts, 900), [10, 0, 20, 0, 40, 0, 50, 0])

    def test_compact_path_data_reads_every_number(self):
        self.assertEqual(flow.path_structure("M0,0C10-5 20,0 30 0z"), ("MCz", 8))

    def test_a_change_of_command_structure_is_refused(self):
        w = [
            {"ms": 0, "prev_ms": None, "old": FROM, "value": between(0.5)},
            {
                "ms": STEP,
                "prev_ms": 0,
                "old": between(0.5),
                "value": "M 0 300 L 10 10 L 20 20 Z",
            },
        ]
        with self.assertRaises(flow.UnmeasurableError) as caught:
            flow.add_morphs(
                {
                    "times": [0, STEP],
                    "elements": [],
                    "morphs": [{"label": "path#arch", "writes": w}],
                }
            )
        self.assertIn(
            "path#arch with a different command structure", caught.exception.args[0][0]
        )

    def test_a_first_shape_of_another_structure_is_setup(self):
        w = [
            {
                "ms": 100,
                "prev_ms": 100 - STEP,
                "old": "M 0 300 A 100 100 0 0 1 200 300 Z",
                "value": FROM,
            },
            {"ms": 100 + STEP, "prev_ms": 100, "old": FROM, "value": between(0.1)},
        ]
        self.assertEqual([t for t, _ in flow.morph_points(w)], [100, 100 + STEP])


def without(*gone):
    """An eased morph's writes with the frames `gone`, by index, never drawn."""
    return writes(
        eased(0, 1000), [f for k, f in enumerate(frames(1000)) if k not in gone]
    )


class DroppedFrames(unittest.TestCase):
    def test_one_dropped_frame_is_tolerated(self):
        self.assertEqual(flow.dropped_frames(without(30)), [])

    def test_two_dropped_frames_in_a_row_are_found(self):
        got = flow.dropped_frames(without(30, 31))
        self.assertEqual(
            [(round(a), round(b)) for a, b in got],
            [(round(29 * STEP), round(32 * STEP))],
        )

    def test_no_step_rests_on_frames_dropped_at_a_morphs_start(self):
        # Frames 1 and 2 go undrawn, as a page's first frames do (#126).
        s = {
            "times": flow.sample_times(1100, [], 60),
            "elements": [],
            "morphs": [{"label": "path#arch", "writes": without(1, 2)}],
        }
        flow.add_morphs(s)
        self.assertEqual(flow.analyse(s)["steps"], [])
        del s["elements"][0]["dropped"]
        self.assertTrue(flow.analyse(s)["steps"])

    def test_no_jolt_rests_on_a_dropped_frame(self):
        s = sample((100, 600, linear), until=800)
        s["elements"][0]["dropped"] = {"position": [(100, 100 + STEP)]}
        self.assertEqual(
            [(j["edge"], j["at"]) for j in flow.analyse(s)["jolts"]], [("stops", 600)]
        )

    def test_a_jolt_outside_a_dropped_stretch_is_still_found(self):
        kept = [f for k, f in enumerate(frames(800)) if k not in (20, 21, 22)]
        w = writes(lambda t: min(1, max(0, (t - 100) / 500)), kept)
        got = [(j["edge"], j["at"]) for j in morph_measured(w, 800)["jolts"]]
        self.assertEqual(got, [("starts", 100), ("stops", 600)])

    def test_a_morph_drawn_at_a_steady_20_fps_is_found(self):
        # Its median gap is 50 ms, so it reads as dropped against Chromium's
        # 60 Hz frame (#126 review).
        w = writes(eased(0, 1000), [k * 3 * STEP for k in range(21)])
        # Every stretch touches the next, so they read as one (#135).
        self.assertEqual(flow.dropped_frames(w), [(w[0]["ms"], w[-1]["ms"])])
        self.assertEqual(
            flow.dropped_frames(
                writes(eased(0, 1000), [k * 2 * STEP for k in range(31)])
            ),
            [],
        )

    def test_a_shape_held_while_frames_are_dropped_is_not_found(self):
        w = [
            {"ms": 0, "prev_ms": None, "old": FROM, "value": between(0.5)},
            {
                "ms": 400,
                "prev_ms": 400 - STEP,
                "old": between(0.5),
                "value": between(1),
            },
            {
                "ms": 400 + STEP,
                "prev_ms": 400,
                "old": between(1),
                "value": between(0.9),
            },
        ]
        self.assertEqual(flow.dropped_frames(w), [])


class MorphFlow(unittest.TestCase):
    def test_an_eased_morph_has_no_pause_or_jolt(self):
        r = morph_measured(writes(eased(0, 1000), frames(1000)), 1000)
        self.assertIn("d", r["elements"][0]["channels"])
        self.assertEqual((r["pauses"], r["jolts"]), ([], []))

    def test_a_linear_morph_jolts_at_both_ends(self):
        w = writes(lambda t: min(1, max(0, (t - 100) / 500)), frames(800))
        got = [
            (j["edge"], j["at"], j["channels"]) for j in morph_measured(w, 800)["jolts"]
        ]
        self.assertEqual(got, [("starts", 100, ["d"]), ("stops", 600, ["d"])])

    def test_a_morph_held_halfway_shows_the_pause(self):
        first, second = eased(0, 400), eased(800, 400)
        w = writes(
            lambda t: first(t) / 2 if t < 800 else 0.5 + second(t) / 2, frames(1200)
        )
        [p] = morph_measured(w, 1200)["pauses"]
        self.assertAlmostEqual(p["start"], 400, delta=2 * STEP)
        self.assertAlmostEqual(p["end"], 800, delta=2 * STEP)

    def test_a_morph_joins_its_elements_other_channels(self):
        s = {
            "times": [0, 10],
            "elements": [{"label": "path#arch", "channels": {"opacity": ["0", "1"]}}],
            "morphs": [
                {"label": "path#arch", "writes": writes(eased(0, 10), [0, 5, 10])}
            ],
        }
        flow.add_morphs(s)
        self.assertEqual(len(s["elements"]), 1)
        self.assertEqual(sorted(s["elements"][0]["channels"]), ["d", "opacity"])


def run_morph(page):
    """check-flow.py's process and flow.json on a morph fixture, and
    check-curves.js's process on the morph.svg it wrote."""
    with tempfile.TemporaryDirectory() as out:
        proc, data, _ = run(page, out=out)
        # A guess, with room to spare: check-curves.js only reads one SVG.
        curves = subprocess.run(
            ["node", CURVES, os.path.join(out, "morph.svg")],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        return proc, data, curves


def covers_stall(data):
    """Whether a dropped stretch is morph-stall.html's 200 ms hold, 180 ms or
    more over 450–600 ms from the morph's first frame, where p = 0.4 falls."""
    start = data["edges_ms"][0]
    return any(
        b - a >= 180 and a - start < 600 and b - start > 450
        for a, b in data["elements"][0]["dropped"]["d"]
    )


class MorphPages(unittest.TestCase):
    def test_a_morph_between_matched_paths_passes_both_checkers(self):
        proc, data, curves = run_morph("morph.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(
            [(e["label"], list(e["channels"])) for e in data["elements"]],
            [("path#arch", ["d"])],
        )
        # A busy machine can draw the last frame late (#135), and a frame up to
        # 3.3 ms early already draws the final shape (#148).
        self.assertGreaterEqual(data["length_ms"], 1000 - 3 * STEP)
        self.assertIn("run check-curves.js on it", proc.stdout)
        self.assertEqual(curves.returncode, 0, curves.stdout + curves.stderr)

    def test_a_morph_held_longer_than_the_quiet_window_is_measured_whole(self):
        proc, data, curves = run_morph("morph-hold.html")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        [p] = data["pauses"]
        self.assertAlmostEqual(p["start"], 300, delta=3 * STEP)
        self.assertAlmostEqual(p["end"], 1300, delta=3 * STEP)
        self.assertAlmostEqual(data["length_ms"], 1600, delta=3 * STEP)
        self.assertEqual(curves.returncode, 0, curves.stdout + curves.stderr)

    def test_a_stretch_the_browser_drops_frames_over_on_every_load_is_named_not_measured(
        self,
    ):
        proc, data, _ = run("morph-stall.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        # A busy machine can add stretches, as at the morph's first frames, and
        # join one to the stall's, so it is found by the time it covers (#135).
        self.assertRegex(
            proc.stdout,
            r"\nnot measured, where the browser dropped frames on the last of 3 loads, each of which dropped some; a busy machine drops frames, "
            r"so measure again when it is quieter:(\n  path#arch \d+–\d+ ms \(d\))+\n",
        )
        self.assertTrue(covers_stall(data), data["elements"][0]["dropped"]["d"])

    def test_a_morph_the_browser_draws_at_11_fps_is_measured_and_named_not_measured(
        self,
    ):
        proc, data, _ = run("morph-starved.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(
            [(e["label"], list(e["channels"])) for e in data["elements"]],
            [("path#arch", ["d"])],
        )
        # A frame within 3.3 ms of 1000 ms already draws the final shape to two
        # decimals, so the last frame that changes it can land that far short (#148).
        self.assertGreaterEqual(data["length_ms"], 1000 - 4)
        # Every frame is dropped, so one stretch covers the morph's 1000 ms.
        [(a, b)] = data["elements"][0]["dropped"]["d"]
        self.assertGreater(b - a, 900)
        self.assertEqual((data["jolts"], data["steps"]), ([], []))

    def test_a_morph_held_while_the_browser_is_starved_is_measured_whole(self):
        # Its ticks ask for the next frame, then hold the browser 110 ms (#135).
        proc, data, _ = run("morph-hold-starved.html")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        [p] = data["pauses"]
        self.assertAlmostEqual(p["start"] - data["edges_ms"][0], 800, delta=250)
        self.assertAlmostEqual(p["end"] - data["edges_ms"][0], 1800, delta=250)
        # Its last frame falls within one held frame, 110 ms, of 2600 ms.
        self.assertGreaterEqual(data["length_ms"], 2600 - 120)

    def test_a_load_that_drops_frames_is_measured_again(self):
        proc, data, _ = run("morph-stall-once.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        # A busy machine can still drop frames at the morph's start.
        self.assertFalse(covers_stall(data), proc.stdout)

    def test_a_morph_through_a_polygon_resample_fails_check_curves(self):
        proc, _, curves = run_morph("morph-polygon.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(curves.returncode, 1, curves.stdout + curves.stderr)
        self.assertNotIn('id="path-arch-before"', curves.stdout)
        self.assertRegex(
            curves.stdout, r'id="path-arch-at-\d+ms">: \d+ straight segments'
        )


if __name__ == "__main__":
    child.main()
