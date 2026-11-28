# #616
import json
import os
import pathlib
import re
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-frames.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "frames")
MARK = os.path.join(FIXTURES, "mark.svg")
SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

frames = siblings.load(SCRIPTS, "check-frames.py")
runner = siblings.load(SCRIPTS, "runner.py")
conditions = siblings.load(SCRIPTS, "conditions.py")
NUDGE_UNDER_JITTER_OFF_FRAME_GRID_MS = 10
MID_BOTTOM_MS = 1000
RUN_TIMEOUT_S = 180  # guess, #501


def load_of(path):
    width, height = conditions.DESKTOP_WINDOW
    return frames.Load(
        pathlib.Path(path).resolve().as_uri(),
        {"width": width, "height": height},
        runner.PLAY_TIMEOUT_MS,
    )


def run(*args):
    return child.run([sys.executable, SCRIPT, *args], timeout=RUN_TIMEOUT_S)


def last(page, *extra):
    with tempfile.TemporaryDirectory() as out:
        proc = run(
            "last",
            os.path.join(FIXTURES, page),
            "--at",
            "#logo",
            "--asset",
            MARK,
            "--out",
            out,
            *extra,
        )
        return proc, sorted(os.listdir(out))


def hash_page(page, *extra):
    with tempfile.TemporaryDirectory() as out:
        return run("hash", page, "--out", out, *extra)


class Last(unittest.TestCase):
    def test_the_mark_faded_in_over_its_pieces_fails_at_both_scales_67(self):
        proc, written = last("twice.html")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertRegex(
            proc.stdout, r"\n  1x: [\d,]+ pixels differ, by up to \d+ levels"
        )
        self.assertRegex(
            proc.stdout, r"\n  2x: [\d,]+ pixels differ, by up to \d+ levels"
        )
        self.assertIn("at 20000 ms", proc.stdout)
        self.assertEqual(
            written,
            [
                "asset-1x.png",
                "asset-2x.png",
                "diff-1x.png",
                "diff-2x.png",
                "last-1x.png",
                "last-2x.png",
            ],
        )

    def test_the_mark_alone_with_its_pieces_hidden_passes(self):
        proc, _ = last("alone.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("\n  1x: identical\n  2x: identical", proc.stdout)

    def test_a_build_whose_animations_still_hold_their_end_state_fails_and_names_them_67(
        self,
    ):
        proc, _ = last("held.html")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(
            "4 animation(s) still hold their end state (g#finished, g#pieces, path#arch, …)",
            proc.stdout,
        )

    def test_a_mark_and_its_wordmark_as_two_files_draw_as_one(self):
        ring, arch = (os.path.join(FIXTURES, n) for n in ("ring.svg", "arch.svg"))
        with tempfile.TemporaryDirectory() as out:
            proc = run(
                "last",
                os.path.join(FIXTURES, "alone.html"),
                "--at",
                "#logo",
                "--asset",
                ring,
                "--asset",
                arch,
                "--out",
                out,
            )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("(ring.svg + arch.svg)", proc.stdout)
        self.assertIn("\n  1x: identical\n  2x: identical", proc.stdout)

    def test_an_html_box_at_a_fractional_origin_takes_the_assets_viewbox_67(self):
        proc, _ = last("box.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("\n  1x: identical\n  2x: identical", proc.stdout)

    def test_an_at_that_matches_nothing_cannot_be_checked(self):
        proc, _ = last("alone.html", "--at", "#nothing")
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn("--at #nothing matches 0 elements, not one", proc.stdout)

    def test_an_asset_that_is_not_well_formed_is_a_usage_error_67(self):
        with tempfile.TemporaryDirectory() as out:
            broken = os.path.join(out, "broken.svg")
            with open(broken, "w", encoding="utf8") as fh:
                fh.write(
                    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><!-- a -- b --></svg>'
                )
            proc = run(
                "last",
                os.path.join(FIXTURES, "alone.html"),
                "--at",
                "#logo",
                "--asset",
                MARK,
                "--asset",
                broken,
                "--out",
                out,
            )
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("broken.svg is not well-formed XML", proc.stderr)

    def test_an_asset_with_no_viewbox_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as out:
            bare = os.path.join(out, "bare.svg")
            with open(bare, "w", encoding="utf8") as fh:
                fh.write(
                    '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"/>'
                )
            proc = run(
                "last",
                os.path.join(FIXTURES, "alone.html"),
                "--at",
                "#logo",
                "--asset",
                bare,
                "--out",
                out,
            )
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("has no viewBox", proc.stderr)

    def test_a_viewport_that_is_not_w_by_h_is_a_usage_error(self):
        proc, _ = last("alone.html", "--viewport", "wide")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("--viewport wants WxH, e.g. 1920x945 — got 'wide'", proc.stderr)


class Hash(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp()
        cls.draft = os.path.join(cls.dir, "draft")
        shutil.copytree(os.path.join(FIXTURES, "draft"), cls.draft)
        cls.page = os.path.join(cls.draft, "index.html")
        cls.hashes = os.path.join(cls.dir, "hashes.json")
        cls.saved = run(
            "hash",
            cls.page,
            "--out",
            os.path.join(cls.dir, "saved"),
            "--save",
            cls.hashes,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir)

    def edit_engine(self, old, new):
        path = os.path.join(self.draft, "engine.js")
        with open(path, encoding="utf8") as fh:
            text = fh.read()
        self.assertIn(old, text)
        with open(path, "w", encoding="utf8") as fh:
            fh.write(text.replace(old, new))
        self.addCleanup(lambda: open(path, "w", encoding="utf8").write(text))

    def check(self):
        return run(
            "hash",
            self.page,
            "--out",
            os.path.join(self.dir, "checked"),
            "--check",
            self.hashes,
        )

    def test_a_steady_draft_renders_every_key_frame_the_same_twice(self):
        self.assertEqual(
            self.saved.returncode, 0, self.saved.stdout + self.saved.stderr
        )
        self.assertIn(
            "4 key frame(s) at 1920x945, scale 1: 0, 1000, 1200, 1800 ms",
            self.saved.stdout,
        )
        self.assertIn(
            "fresh and then seeked backwards through one page: every frame the same",
            self.saved.stdout,
        )

    def test_a_no_op_engine_edit_changes_no_frame(self):
        self.edit_engine("function build", "// a comment only\nfunction build")
        proc = self.check()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("every frame unchanged", proc.stdout)

    def test_an_engine_edit_names_the_key_frame_it_changed(self):
        self.edit_engine("scale(0.6)", "scale(0.5)")
        proc = self.check()
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("1 frame(s) changed\n  1200 ms: see ", proc.stdout)

    def test_a_page_that_draws_one_moment_two_ways_fails_67(self):
        proc = hash_page(os.path.join(FIXTURES, "unstable.html"))
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertRegex(
            proc.stdout, r"2 frame\(s\) differ\n  0 ms: [\d,]+ pixels differ"
        )

    def test_a_frame_that_depends_on_the_frame_before_it_fails_67_621(self):
        proc = hash_page(os.path.join(FIXTURES, "trail.html"))
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertRegex(
            proc.stdout, r"1 frame\(s\) differ\n  0 ms: [\d,]+ pixels differ"
        )

    def test_check_refuses_times_because_its_frames_come_from_the_file(self):
        proc = run(
            "hash", self.page, "--out", self.dir, "--check", self.hashes, "--times", "0"
        )
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn(
            "--check renders the frames its file names; drop --times", proc.stderr
        )

    def test_check_refuses_a_file_that_is_not_saved_hashes_rather_than_report_a_changed_frame(
        self,
    ):
        bad = os.path.join(self.dir, "not-hashes.json")
        with open(bad, "w", encoding="utf8") as fh:
            fh.write('{"frames": []}')
        proc = run("hash", self.page, "--out", self.dir, "--check", bad)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("is not a file of saved hashes", proc.stderr)


class LateStart(unittest.TestCase):
    """#240"""

    def test_a_build_that_starts_after_load_is_read_to_its_end(self):
        proc = hash_page(os.path.join(FIXTURES, "late.html"))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("2 key frame(s) at 1920x945, scale 1: 0, 1000 ms", proc.stdout)

    def test_a_page_that_never_stops_starting_animations_cannot_be_checked(self):
        proc = hash_page(os.path.join(FIXTURES, "restless.html"))
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(
            f"is still starting animations {frames.SETTLE_CAP_MS} ms after it loaded and its fonts were ready "
            "(div#dot), so its frames have no fixed timeline; start its motion once and let it end",
            proc.stdout,
        )

    def test_a_page_read_as_still_names_wait_for_motion_that_starts_later(self):
        proc = hash_page(os.path.join(HERE, "fixtures", "sheet", "still.html"))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(
            f"no animation started in the {frames.QUIET_MS} ms after the page loaded, so it is read as still; "
            "if its motion starts later, pass --wait",
            proc.stdout,
        )


class Scripted(unittest.TestCase):  # #546
    TRAILER = "\nCheck its frames by eye.\n"

    def refused(self, proc, why):
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(f"because this page:\n  - {why}\n", proc.stdout)
        self.assertTrue(proc.stdout.endswith(self.TRAILER), proc.stdout)

    def test_a_frame_loop_build_cannot_be_hashed_naming_it_unlike_a_steady_draft(self):
        self.refused(
            hash_page(os.path.join(FIXTURES, "raf.html")),
            "moves 1 element(s) by rewriting their style or attributes from a script, "
            "frame by frame (div#box)",
        )

    def test_a_canvas_build_cannot_be_hashed_naming_it_unlike_a_steady_draft(self):
        self.refused(
            hash_page(os.path.join(FIXTURES, "canvas.html")),
            "draws on a canvas (canvas#stage)",
        )

    def test_a_smil_build_cannot_be_hashed_naming_it_unlike_a_steady_draft(self):
        self.refused(
            hash_page(os.path.join(FIXTURES, "smil.html")),
            "animates SVG with SMIL (rect#slab > animate)",
        )

    def test_a_path_a_frame_loop_morphs_cannot_be_hashed_naming_it_unlike_a_steady_draft(
        self,
    ):
        self.refused(
            hash_page(os.path.join(FIXTURES, "morph.html")),
            "morphs 1 path(s) by rewriting their d from a script, frame by frame (path#wave)",
        )

    def test_an_animation_a_script_seeks_by_hand_cannot_be_hashed_naming_it_unlike_a_steady_draft(
        self,
    ):
        self.refused(
            hash_page(os.path.join(FIXTURES, "seeked.html")),
            "holds 1 animation(s) a script paused (div#box), which a seek would move as if playing",
        )

    def test_a_reveal_css_holds_paused_is_hashed_as_it_plays_once_released_unlike_a_script_seeked_one(
        self,
    ):
        """#610"""
        with tempfile.TemporaryDirectory() as out:
            proc = run(
                "hash",
                os.path.join(FIXTURES, "revealed.html"),
                "--out",
                out,
                "--times",
                "0,1200",
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            shots = [
                open(os.path.join(out, f"frame-{ms}.png"), "rb").read()
                for ms in (0, 1200)
            ]
            self.assertNotEqual(
                *shots, "the reveal did not move between its start and end"
            )

    def test_a_frame_loop_build_ending_on_its_asset_cannot_be_checked_beside_listed_animations_unlike_the_mark_alone(
        self,
    ):
        why = (
            "moves 1 element(s) by rewriting their style or attributes from a script, "
            "frame by frame (path#arch)"
        )
        proc, written = last("raf-asset.html")
        self.refused(proc, why)
        self.assertEqual(written, [])
        self.refused(hash_page(os.path.join(FIXTURES, "raf-asset.html")), why)


def bottom_of(record):
    return next(s for s in record["timeline"] if s["name"] == "div#bottom")


class StagedBuilds(unittest.TestCase):
    """#259"""

    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp()
        cls.page = os.path.join(FIXTURES, "staggered.html")
        cls.hashes = os.path.join(cls.dir, "hashes.json")
        cls.saved = run(
            "hash", cls.page, "--out", os.path.join(cls.dir, "saved"), "--save", cls.hashes
        )  # fmt: skip

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir)

    def check_against(self, edit, at_ms):
        with open(self.hashes, encoding="utf8") as fh:
            record = json.load(fh)
        edit(record)
        record["frames"] = [f for f in record["frames"] if f["ms"] == at_ms]
        self.assertEqual(len(record["frames"]), 1, at_ms)
        edited = os.path.join(self.dir, "edited.json")
        with open(edited, "w", encoding="utf8") as fh:
            json.dump(record, fh)
        return run(
            "hash", self.page, "--out", os.path.join(self.dir, "checked"), "--check", edited
        )  # fmt: skip

    def test_a_chain_started_by_finish_events_cannot_be_checked(self):
        proc = hash_page(os.path.join(FIXTURES, "chained.html"))
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(
            "starts animations when others finish (div#bottom), so a seek draws its build only to "
            "where the first link ends; start every link when the page loads, held back by its delay",
            proc.stdout,
        )

    def test_both_links_of_a_chain_a_timer_carries_past_quiet_ms_are_found_unlike_a_staggered_start_686(
        self,
    ):
        with runner.chromium(frames.HASH_ARGS) as browser:
            context, page, prep = frames.open_page(
                browser, load_of(os.path.join(FIXTURES, "timed-chain.html")), 1
            )
            try:
                with self.assertRaises(frames.UnmeasurableError) as caught:
                    frames.refuse_chain(page)
            finally:
                context.close()
        self.assertEqual([s["name"] for s in prep["timeline"]], ["div#mark"])
        self.assertIn(
            "starts animations when others finish (div#tagline)", str(caught.exception)
        )

    def test_a_timer_past_the_cap_is_refused_naming_its_delay_unlike_a_staggered_start_686(
        self,
    ):
        proc = hash_page(os.path.join(FIXTURES, "long-timer.html"))
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(
            f"sets a script timer for 6000 ms, past the {frames.SETTLE_CAP_MS} ms it waits for one, "
            "so a link of its motion that a timer starts goes unseen",
            proc.stdout,
        )

    def test_a_repeating_timer_is_refused_naming_its_period_unlike_a_staggered_start_686(
        self,
    ):
        proc = hash_page(os.path.join(FIXTURES, "ticking.html"))
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(
            "repeats a script timer every 250 ms, which never stops pending",
            proc.stdout,
        )

    def test_a_page_setting_timers_past_the_cap_is_refused_unlike_a_staggered_start_686(
        self,
    ):
        proc = hash_page(os.path.join(FIXTURES, "polling.html"))
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(
            f"keeps setting script timers, one of 100 ms due past the {frames.SETTLE_CAP_MS} ms it waits for them",
            proc.stdout,
        )

    def test_the_timer_fixtures_sit_past_quiet_ms_and_either_side_of_the_cap_686(self):
        def delay(page):
            with open(os.path.join(FIXTURES, page), encoding="utf8") as fh:
                return int(re.search(r"setTimeout\(.*, (\d+)\);", fh.read()).group(1))

        self.assertLess(frames.QUIET_MS, delay("timed-chain.html"))
        self.assertLess(delay("timed-chain.html"), frames.SETTLE_CAP_MS)
        self.assertLess(frames.SETTLE_CAP_MS, delay("long-timer.html"))

    def test_a_late_start_no_finish_made_is_not_called_a_chain(self):
        proc = hash_page(os.path.join(FIXTURES, "afterward.html"))
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(
            "starts animations after its frames were read (div#dot), so a seek cannot fix its frames; "
            "make them when the page loads, or pass --wait",
            proc.stdout,
        )

    def test_a_staggered_start_renders_every_frame_the_same_twice(self):
        self.assertEqual(
            self.saved.returncode, 0, self.saved.stdout + self.saved.stderr
        )
        self.assertRegex(
            self.saved.stdout,
            r"its animations start at 2 moments, 0, [\d.]+ ms, as one load timed them",
        )
        self.assertIn("every frame the same", self.saved.stdout)

    def test_a_later_stage_the_page_lists_first_is_timed_from_the_earliest_start(
        self,
    ):
        proc = hash_page(
            self.page, "--wait", "body.play #bottom", "--times", str(MID_BOTTOM_MS)
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertRegex(proc.stdout, r"start at 2 moments, 0, [1-9][\d.]* ms")

    def test_check_renders_the_saved_timeline_not_its_own(self):
        nudged = {}

        def nudge(record):
            bottom = bottom_of(record)
            bottom["ms"] += NUDGE_UNDER_JITTER_OFF_FRAME_GRID_MS
            nudged["ms"] = bottom["ms"]

        proc = self.check_against(nudge, MID_BOTTOM_MS)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(
            f"start at 2 moments, 0, {frames.ms(round(nudged['ms'], 3))} ms, as the saved run timed them",
            proc.stdout,
        )
        self.assertIn("every frame the same", proc.stdout)
        self.assertRegex(proc.stdout, r"[1-9] frame\(s\) changed")

    def test_check_names_a_start_the_page_moved(self):
        def moved(record):
            bottom_of(record)["ms"] += 300

        proc = self.check_against(moved, 0)
        self.assertRegex(
            proc.stdout,
            r"  this load started animations away from the file's moments \(div#bottom [\d.]+ ms then, "
            r"[\d.]+ ms now\); every frame is drawn at the file's, so a start the page moved shows only here",
        )
        self.assertIn("as the saved run timed them", proc.stdout)

    def test_check_times_a_page_whose_animations_changed_itself_and_says_so(self):
        def renamed(record):
            bottom_of(record)["name"] = "div#gone"

        proc = self.check_against(renamed, 0)
        self.assertIn(
            "  the page makes different animations from the ones the file saved, so this load timed them",
            proc.stdout,
        )
        self.assertIn("as one load timed them", proc.stdout)

    def test_check_against_a_file_saved_with_no_timeline_times_the_page_itself(self):
        proc = self.check_against(lambda record: record.pop("timeline"), 0)
        self.assertIn(
            "  the file saves no timeline, so this load timed them", proc.stdout
        )
        self.assertIn("as one load timed them", proc.stdout)

    def open_with(self, timeline):
        with runner.chromium() as browser:
            context, _, prep = frames.open_page(
                browser, load_of(self.page), 1, timeline=timeline
            )
            context.close()
        return prep

    def test_a_load_that_makes_other_animations_than_the_timeline_cannot_be_checked(
        self,
    ):
        with self.assertRaises(frames.UnmeasurableError) as caught:
            self.open_with([{"name": "div#top", "ms": 0}])
        self.assertEqual(
            caught.exception.args[0],
            [
                "makes different animations from one load to the next (div#bottom, which an "
                "earlier load did not make), so its frames have no fixed timeline"
            ],
        )

    def test_animations_one_frame_starts_match_whichever_order_they_list_in(self):
        prep = self.open_with(
            [{"name": "div#bottom", "ms": 150}, {"name": "div#top", "ms": 0}]
        )
        self.assertEqual(
            sorted((s["name"], s["ms"]) for s in prep["timeline"]),
            [("div#bottom", 150), ("div#top", 0)],
        )

    def test_two_animations_on_one_element_keep_their_starts_whichever_load_tied_them(
        self,
    ):
        """#619"""
        timeline = [
            {"name": "div#box", "ms": 0},
            {"name": "div#twin", "ms": 0},
            {"name": "div#twin", "ms": 50},
        ]
        with runner.chromium() as browser:
            context, page, _ = frames.open_page(
                browser,
                load_of(os.path.join(FIXTURES, "revealed.html")),
                1,
                timeline=timeline,
            )
            try:
                frames.seek(page, 50)
                shown = page.evaluate("getComputedStyle(twin).transform")
            finally:
                context.close()
        self.assertEqual(shown, "matrix(1, 0, 0, 1, 0, 0)")


class WaitingStart(unittest.TestCase):
    def test_an_animation_made_in_a_held_frame_starts_in_it_so_no_frame_draws_it_waiting_346(
        self,
    ):
        with runner.chromium(frames.HASH_ARGS) as browser:
            context, page, prep = frames.open_page(
                browser, load_of(os.path.join(FIXTURES, "waiting.html")), 1
            )
            try:
                waited = page.evaluate(
                    "Object.fromEntries(Object.entries(window.waited)"
                    ".map(([id, t]) => ['div#' + id, t - window.__frames.t0]))"
                )
                starts = {s["name"]: s["ms"] for s in prep["timeline"]}
                for name in ("div#word", "div#bar", "div#note"):
                    self.assertAlmostEqual(
                        starts[name],
                        waited[name],
                        delta=1,
                        msg=name,
                    )
                start = starts["div#word"]
                shown = []
                for t in (start - 1, start):
                    frames.seek(page, t)
                    shown.append(page.evaluate("getComputedStyle(word).transform"))
                self.assertEqual(shown, ["none", "matrix(1, 0, 0, 1, 0, 300)"])
            finally:
                context.close()


class KeyTimes(unittest.TestCase):
    PREP = {"keys": [0, 1000, 400.0004, 400, 1200], "end": 1800}

    def test_the_default_is_every_key_and_the_end_a_frame_apart(self):
        self.assertEqual(frames.key_times(self.PREP, None), [0, 400, 1000, 1200, 1800])

    def test_asked_times_are_clamped_to_the_build_and_end_is_its_end(self):
        self.assertEqual(
            frames.key_times(self.PREP, [5000, "end", -3, 250.5]), [0, 250.5, 1800]
        )


if __name__ == "__main__":
    child.main()
