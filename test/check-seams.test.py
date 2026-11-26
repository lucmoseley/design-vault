"""Tests plugin/skills/design-round/scripts/check-seams.py (#341): python3 test/check-seams.test.py

vault.contacts-seam rests on this script: the critic answering
vault.contacts-look yields to it. Loosen the threshold, drop a device pixel
ratio, or let the art's own ground into the mattes, and a seam the eye sees
at one ratio passes; read a translucent fill's matte as a seam, or a missing
tool as a clean contact, and a contact no script measured reads as a pass.
"""

import csv
import re

import os
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-seams.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "check-seams")
# The #340 instrument's figures for gap.html's contact.
RESEARCH = os.path.join(HERE, "..", "docs", "data", "contact-seams-2026-10-16.csv")
GAP_ROW = "blue-orange-on-white.gap-v.1"
# How far a figure may stray from the instrument's: a guess, past the one length step check-seams.py may differ by.
GAP_TOLERANCE = 0.05
REQUIREMENTS = os.path.realpath(os.path.join(HERE, "..", "plugin", "requirements.txt"))
# A guess: a run loads the fixture once a scale, after look-renders.py's two loads to fit and time it.
RUN_S = 180
# A run missing a dependency stops before any browser starts; its timeout, in s, is a guess, unmeasured.
BLOCKED_RUN_S = 60
# Runs argv[2:] as a script once argv[1] is made unimportable.
BLOCKED = (
    "import runpy, sys; sys.modules[sys.argv[1]] = None; sys.argv = sys.argv[2:]; "
    "runpy.run_path(sys.argv[0], run_name='__main__')"
)


def run(page, out):
    return child.run([sys.executable, SCRIPT, page, "--out", out], timeout=RUN_S)


def blocked(argv, env=None):
    # Never through child.run: it takes no env, and such a run starts no browser for earlyoom to break.
    return subprocess.run(
        [sys.executable, *argv],
        capture_output=True,
        text=True,
        timeout=BLOCKED_RUN_S,
        check=False,
        env=env,
    )


def fixture(name):
    return os.path.join(FIXTURES, name if "." in name else f"{name}.html")


def figures(out, name):
    """The width x contrast figures a run printed for a contact, by scale."""
    line = next(said for said in out.splitlines() if f" {name} (" in said)
    return {int(s): float(v) for s, v in re.findall(r"0 ms (\d)x ([\d.e+]+)″", line)}


class Seams(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.runs = {
            name: run(fixture(name), os.path.join(cls.tmp.name, name))
            for name in (
                "closed",
                "gap",
                "seam",
                "translucent",
                "thin",
                "transition",
                "seam.svg",
            )
        }

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_a_closed_contact_passes_at_every_scale(self):
        proc = self.runs["closed"]
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(
            "pass under.2-over.4 (underlap): width x contrast 0 ms 1x 0″, 0 ms 2x 0″, 0 ms 3x 0″",
            proc.stdout,
        )
        self.assertNotIn("FAIL", proc.stdout)

    def test_a_coincident_pair_passes_unmeasured_as_no_ground_lies_inside_it(self):
        self.assertIn(
            "pass under.1-over.1 (coincident): both fills lie on one side of one edge",
            self.runs["closed"].stdout,
        )

    def test_a_gap_fails_at_every_scale(self):
        proc = self.runs["gap"]
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("FAIL left.2-right.4 (separate)", proc.stdout)
        self.assertIn("at or over 0.5″ at 0 ms 1x, 0 ms 2x, 0 ms 3x;", proc.stdout)
        self.assertIn("run one on under the other by at least 1 CSS px", proc.stdout)
        self.assertIn("--contact 'left.2-right.4=#right@40.87,50.125'", proc.stdout)

    def test_a_gaps_figures_match_the_research_instrument_at_every_scale(self):
        with open(RESEARCH, newline="") as fh:
            want = {
                int(r["dpr"]): float(r["wc_arcsec"])
                for r in csv.DictReader(fh)
                if r["contact"] == GAP_ROW
            }
        got = figures(self.runs["gap"].stdout, "left.2-right.4")
        self.assertEqual(sorted(got), [1, 2, 3])
        for scale, value in want.items():
            self.assertAlmostEqual(
                got[scale] / value, 1, delta=GAP_TOLERANCE, msg=f"{scale}x"
            )

    def test_ground_past_a_thin_fills_far_side_is_not_a_seam(self):
        proc = self.runs["thin"]
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(
            "pass under.2-over.4 (underlap): width x contrast 0 ms 1x 0″, 0 ms 2x 0″, 0 ms 3x 0″",
            proc.stdout,
        )

    def test_a_page_that_eases_every_change_shows_each_seam_as_drawn(self):
        # Two like seams on the page's own dark ground measure alike: a matte shot before the second's crop would
        # leave that crop easing back from white.
        proc = self.runs["transition"]
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertEqual(
            proc.stdout.count("0 ms 1x 43″, 0 ms 2x 0″, 0 ms 3x 14″"), 2, proc.stdout
        )

    def test_a_bare_svg_files_seam_is_measured_as_on_a_page(self):
        proc = self.runs["seam.svg"]
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("0 ms 1x 59″, 0 ms 2x 0″, 0 ms 3x 19″", proc.stdout)

    def test_a_ground_coloured_seam_fails_at_the_scales_where_it_shows_and_only_those(
        self,
    ):
        # docs/research/contact-seams.md §2: an edge at x + 0.5 is seamed at DPR 1 and 3, clean at 2.
        proc = self.runs["seam"]
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("FAIL left.2-right.4 (shared edge, no underlap)", proc.stdout)
        self.assertIn("0 ms 1x 59″, 0 ms 2x 0″, 0 ms 3x 19″", proc.stdout)
        self.assertIn("at or over 0.5″ at 0 ms 1x, 0 ms 3x;", proc.stdout)

    def test_the_mattes_draw_only_the_two_shapes_over_black_and_over_white(self):
        out = os.path.join(self.tmp.name, "seam")
        mattes = {}
        for ground in ("black", "white"):
            with Image.open(
                os.path.join(out, f"left.2-right.4-0ms-1x-{ground}.png")
            ) as im:
                mattes[ground] = np.asarray(im.convert("RGB")).astype(int)
            # At device size, the fills unchanged either side of the seam.
            self.assertEqual(mattes[ground].shape, (16, 16, 3))
            self.assertEqual(tuple(mattes[ground][8, 0]), (0x1A, 0x4D, 0x8F))
            self.assertEqual(tuple(mattes[ground][8, 15]), (0xE0, 0xA0, 0x30))
        # The seam's pixels let a quarter of the ground through (§1.4): a(1 - a) at a = 0.5.
        share = (mattes["white"] - mattes["black"]).mean(axis=2) / 255
        self.assertAlmostEqual(share.max(), 0.25, delta=0.01)

    def test_a_translucent_fill_cannot_be_measured(self):
        proc = self.runs["translucent"]
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(
            "NOT MEASURED under.2-over.4 at 0 ms 1x, 0 ms 2x, 0 ms 3x", proc.stdout
        )
        self.assertIn("Judge it under vault.contacts-look", proc.stdout)


class Edges(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def page(self, body):
        path = os.path.join(self.tmp.name, "page.svg")
        with open(path, "w") as fh:
            fh.write(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">{body}</svg>'
            )
        return path

    def test_a_file_with_no_contact_says_the_question_does_not_apply(self):
        proc = run(
            self.page('<rect width="20" height="20" fill="#000"/>'), self.tmp.name
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(
            "no contact to measure: vault.contacts-seam does not apply", proc.stdout
        )

    def test_a_shape_check_curves_cannot_read_is_unmeasured(self):
        proc = run(self.page('<path d="M10 10 L"/>'), self.tmp.name)
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn("could not read the shape", proc.stdout)
        self.assertIn("judge them under vault.contacts-code", proc.stdout)

    def test_541_an_unproved_cover_is_unmeasured_and_a_proved_one_passes(self):
        shapes = (
            '<path id="a" fill="#c00" d="M10 10 H49 V50 H10 Z"/>'
            '<path id="b" fill="#00c" d="M51 10 H90 V50 H51 Z"/>'
            '<path id="strip" fill="#0c0" d="M46 10 H54 V50 H46 Z"/>'
        )
        proc = run(self.page("<style>.t{opacity:.5}</style>" + shapes), self.tmp.name)
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn("NOT MEASURED a.2-b.4 (covered): ", proc.stdout)
        self.assertIn("judge it under vault.contacts-code.", proc.stdout)
        self.assertNotIn("pass a.2-b.4", proc.stdout)
        proved = run(self.page(shapes), self.tmp.name)
        self.assertEqual(proved.returncode, 0, proved.stdout + proved.stderr)
        self.assertIn("pass a.2-b.4 (covered): ", proved.stdout)
        self.assertNotIn("NOT MEASURED", proved.stdout)

    def test_a_missing_file_or_a_url_is_a_usage_error(self):
        for page in (os.path.join(self.tmp.name, "none.html"), "https://example.com/"):
            proc = run(page, self.tmp.name)
            self.assertEqual(proc.returncode, 2, proc.stderr)
            self.assertIn("check-curves.js reads a file, never a URL", proc.stderr)

    def test_no_node_exits_3_naming_it(self):
        proc = blocked(
            [SCRIPT, fixture("closed"), "--out", self.tmp.name],
            {**os.environ, "PATH": ""},
        )
        self.assertEqual(proc.returncode, 3, proc.stderr)
        self.assertIn("Node is not on PATH", proc.stderr)
        self.assertIn("Install Node.", proc.stderr)

    def test_a_missing_package_exits_3_naming_the_pinned_requirements(
        self,
    ):  # #256; pairs with test_a_closed_contact_passes_at_every_scale
        for package in ("numpy", "PIL"):
            with self.subTest(package=package):
                proc = blocked(
                    [
                        "-c",
                        BLOCKED,
                        package,
                        SCRIPT,
                        fixture("closed"),
                        "--out",
                        self.tmp.name,
                    ]
                )
                self.assertEqual(proc.returncode, 3, proc.stderr)
                self.assertIn(f"-r {REQUIREMENTS}", proc.stderr)


if __name__ == "__main__":
    child.main()
