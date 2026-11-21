"""Tests plugin/skills/design-round/scripts/check-frames.py (#67): python3 test/check-frames.test.py

The pages are synthetic, in test/fixtures/frames/. Each build runs 20 s, so a
last frame reached by waiting would time the tests out. Loosen one and a build
that ends on its asset drawn twice, a page that draws one moment two ways, or
an engine edit that moves a kept draft passes the craft gate (gate questions
vault.drafts-kept and vault.end-frame). Loosen #259's and a build a finish
event carries on is hashed only to its first link's end, and one started in
stages fails as drawn two ways. Loosen #346's and a hash taken with threaded
animation can render an animation waiting to start in its unanimated style.
"""

import importlib.util
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
CHILD = importlib.util.spec_from_file_location("child", os.path.join(HERE, "child.py"))
child = importlib.util.module_from_spec(CHILD)
CHILD.loader.exec_module(child)
SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-frames.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "frames")
MARK = os.path.join(FIXTURES, "mark.svg")
spec = importlib.util.spec_from_file_location("check_frames", SCRIPT)
frames = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frames)


def run(*args):
    # A guess for check-frames.py alone, not taken from the other tests' timeouts: one run takes seconds here.
    return child.run([sys.executable, SCRIPT, *args], timeout=180)


def last(page, *extra):
    """Runs `last` on a fixture page; returns its process and the PNG names it wrote."""
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
    def test_the_mark_faded_in_over_its_pieces_fails_at_both_scales(self):
        # lucmoseley/mmm-infra#9 round two's end state (mmm-infra#25 M1b).
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

    def test_a_build_whose_animations_still_hold_their_end_state_fails_and_names_them(
        self,
    ):
        # #67: a held fade drew the mark with other edges than the bare mark.
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

    def test_an_html_box_takes_the_assets_viewbox(self):
        # #67: at a fractional origin, Chrome's snap failed a correct page.
        proc, _ = last("box.html")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("\n  1x: identical\n  2x: identical", proc.stdout)

    def test_an_at_that_matches_nothing_cannot_be_checked(self):
        proc, _ = last("alone.html", "--at", "#nothing")
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn("--at #nothing matches 0 elements, not one", proc.stdout)

    def test_an_asset_that_is_not_well_formed_is_a_usage_error(self):
        # #67 review: a "--" in a comment made the browser draw nothing for the file.
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

    def test_a_page_that_draws_one_moment_two_ways_fails(self):
        # #67, cth9191/animate's two-pass check: unseeded randomness.
        proc = hash_page(os.path.join(FIXTURES, "unstable.html"))
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertRegex(
            proc.stdout, r"2 frame\(s\) differ\n  0 ms: [\d,]+ pixels differ"
        )

    def test_a_frame_that_depends_on_the_frame_before_it_fails(self):
        # #67 review: fresh loads alone cannot see order, which tile.mjs's reversal exists to catch.
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
    """#240: read at load, a page whose motion starts later passes as still."""

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


class StagedBuilds(unittest.TestCase):
    """#259: a build carried on by finish events, or started in stages."""

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

    def check_against(self, edit):
        with open(self.hashes, encoding="utf8") as fh:
            record = json.load(fh)
        edit(record)
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
        proc = hash_page(self.page, "--wait", "body.play #bottom")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertRegex(proc.stdout, r"start at 2 moments, 0, [1-9][\d.]* ms")

    def test_check_renders_the_saved_timeline_not_its_own(self):
        nudged = {}

        def nudge(record):
            # Within STAGE_JITTER_MS, so read as one load's clock; off the 16.7 ms frame grid, so no load times it.
            record["timeline"][1]["ms"] += 10
            nudged["ms"] = record["timeline"][1]["ms"]

        proc = self.check_against(nudge)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(
            f"start at 2 moments, 0, {frames.ms(round(nudged['ms'], 3))} ms, as the saved run timed them",
            proc.stdout,
        )
        self.assertIn("every frame the same", proc.stdout)
        self.assertRegex(proc.stdout, r"[1-9] frame\(s\) changed")

    def test_check_names_a_start_the_page_moved(self):
        def moved(record):
            record["timeline"][1]["ms"] += 300

        proc = self.check_against(moved)
        self.assertRegex(
            proc.stdout,
            r"  this load started animations away from the file's moments \(div#bottom [\d.]+ ms then, "
            r"[\d.]+ ms now\); every frame is drawn at the file's, so a start the page moved shows only here",
        )
        self.assertIn("as the saved run timed them", proc.stdout)

    def test_check_times_a_page_whose_animations_changed_itself_and_says_so(self):
        def renamed(record):
            record["timeline"][1]["name"] = "div#gone"

        proc = self.check_against(renamed)
        self.assertIn(
            "  the page makes different animations from the ones the file saved, so this load timed them",
            proc.stdout,
        )
        self.assertIn("as one load timed them", proc.stdout)

    def test_check_against_a_file_saved_with_no_timeline_times_the_page_itself(self):
        proc = self.check_against(lambda record: record.pop("timeline"))
        self.assertIn(
            "  the file saves no timeline, so this load timed them", proc.stdout
        )
        self.assertIn("as one load timed them", proc.stdout)

    def open_with(self, timeline):
        """The prep of one load of the staggered page placed on `timeline`."""
        _, at = frames.parse(["hash", self.page, "--out", self.dir])
        with frames.flow.chromium() as browser:
            context, _, prep = frames.open_page(browser, at, 1, timeline=timeline)
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
            prep["timeline"],
            [{"name": "div#top", "ms": 0}, {"name": "div#bottom", "ms": 150}],
        )


class WaitingStart(unittest.TestCase):
    def test_an_animation_made_in_a_held_frame_starts_in_it_so_no_frame_draws_it_waiting(
        self,
    ):
        # #346: hash mode's browser starts each animation in the first frame
        # it waits in, so the frame before #word's start rightly shows it in
        # its line, not yet made. Run in process: nothing check-frames prints
        # says which frame an animation waited in, or how one frame drew #word.
        _, at = frames.parse(
            ["hash", os.path.join(FIXTURES, "waiting.html"), "--out", "unused"]
        )
        with frames.flow.chromium(frames.HASH_ARGS) as browser:
            context, page, prep = frames.open_page(browser, at, 1)
            try:
                waited = page.evaluate(
                    "Object.fromEntries(Object.entries(window.waited)"
                    ".map(([id, t]) => ['div#' + id, t - window.__frames.t0]))"
                )
                starts = {s["name"]: s["ms"] for s in prep["timeline"]}
                # The frame's time and the start read the same frame a few
                # µs apart; 1 ms is the exact-time window check-flow uses (#126).
                for name in ("div#word", "div#bar", "div#note"):
                    self.assertAlmostEqual(
                        starts[name], waited[name], delta=1, msg=name
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
