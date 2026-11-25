"""Tests plugin/skills/design-round/scripts/look-renders.py (#228): python3 test/look-renders.test.py

The gate critics answer vault.contacts-look and vault.curves-look from these
renders. Drop a scale, crop off the contact, or magnify by drawing again
rather than repeating pixels, and a critic judges a render the question did
not ask for; lose the bend and it judges the wrong part of the curve. Lose
#259's cases and a chained build is rendered only to its first link, and a
staged one at a different moment at each scale. Lose #331's round trip, on a
page or on a bare SVG file (#354), and check-curves.js --contacts hands this
script a contact it refuses or crops somewhere else.
"""

import json
import os
import shlex
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
    HERE, "..", "plugin", "skills", "design-round", "scripts", "look-renders.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "look-renders")
CURVES = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-curves.js"
)
REQUIREMENTS = os.path.realpath(os.path.join(HERE, "..", "plugin", "requirements.txt"))
WHITE = (255, 255, 255)
SIZE = 16


def run(*args):
    # A guess: the contacts run loads the fixture six times at three scales.
    return child.run([sys.executable, SCRIPT, *args], timeout=180)


# Runs argv[2:] as a script once argv[1] is made unimportable. Such a run stops
# before any browser starts; its timeout, in s, is a guess, unmeasured.
BLOCKED_RUN_S = 60
BLOCKED = (
    "import runpy, sys; sys.modules[sys.argv[1]] = None; sys.argv = sys.argv[2:]; "
    "runpy.run_path(sys.argv[0], run_name='__main__')"
)


def without(package, *args):
    """The script run with `package` unimportable, as on a machine that lacks it (#256)."""
    return subprocess.run(
        [sys.executable, "-c", BLOCKED, package, SCRIPT, *args],
        capture_output=True,
        text=True,
        timeout=BLOCKED_RUN_S,
        check=False,
    )


def pixels(path):
    with Image.open(path) as im:
        return np.asarray(im.convert("RGB"))


def size(path):
    with Image.open(path) as im:
        return im.size


def white_columns(img):
    return [x for x in range(img.shape[1]) if (img[:, x] == WHITE).all()]


class Contacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.TemporaryDirectory()
        cls.out = cls.dir.name
        cls.proc = run(
            "contacts",
            os.path.join(FIXTURES, "contacts.html"),
            "--contact", "gap=#gap-right@0,20",
            "--contact", "clean=#clean-left@50,20",
            "--contact", "round=120.3,310.3",
            "--contact", "moving=#piece@0,20",
            "--out", cls.out,
        )  # fmt: skip

    @classmethod
    def tearDownClass(cls):
        cls.dir.cleanup()

    def setUp(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)

    def test_every_contact_is_cropped_at_every_scale_and_frame_magnified_4x(self):
        for name in ("gap", "clean", "round", "moving"):
            for ms in ("0", "1000"):
                for scale in (1, 2, 3):
                    path = os.path.join(self.out, f"{name}-{ms}ms-{scale}x.png")
                    self.assertTrue(os.path.isfile(path), path)
                    side = SIZE * scale * 4
                    self.assertEqual(size(path), (side, side), path)

    def test_the_gap_shows_at_the_crops_centre_and_the_clean_joint_shows_none(self):
        for scale in (1, 2, 3):
            gap = pixels(os.path.join(self.out, f"gap-0ms-{scale}x.png"))
            centre = SIZE * scale * 4 // 2
            # The gap is the one CSS px left of the contact, so it ends at the centre.
            self.assertEqual(
                white_columns(gap), list(range(centre - scale * 4, centre)), scale
            )
            clean = pixels(os.path.join(self.out, f"clean-0ms-{scale}x.png"))
            self.assertEqual(white_columns(clean), [], scale)

    def test_magnifying_repeats_each_pixel_and_never_draws_again(self):
        for scale in (1, 2, 3):
            img = pixels(os.path.join(self.out, f"round-0ms-{scale}x.png")).astype(int)
            h, w, _ = img.shape
            blocks = img.reshape(h // 4, 4, w // 4, 4, 3)
            self.assertTrue((blocks == blocks[:, :1, :, :1]).all(), scale)
            # The circles' edges are anti-aliased, so a repeat is not a flat crop.
            self.assertGreater(
                len(np.unique(blocks[:, 0, :, 0].reshape(-1, 3), axis=0)), 4
            )

    def test_a_contact_on_a_moving_piece_is_followed_to_each_frame(self):
        for ms, colour in (("0", (204, 0, 0)), ("1000", (0, 170, 0))):
            img = pixels(os.path.join(self.out, f"moving-{ms}ms-1x.png"))
            left, right = img[:, : 8 * 4], img[:, 8 * 4 :]
            self.assertTrue((left == WHITE).all(), ms)
            self.assertTrue((right == colour).all(), ms)

    def test_an_unchanged_contact_is_left_off_a_later_frames_sheet(self):
        with open(os.path.join(self.out, "renders.json"), encoding="utf8") as fh:
            renders = json.load(fh)
        self.assertEqual(renders["times"], [0, 1000])
        self.assertEqual(
            sorted(n for n, _ in renders["unchanged"]), ["clean", "gap", "round"]
        )
        self.assertEqual(renders["sheets"], ["sheet-0ms-1.png", "sheet-1000ms-1.png"])

    def test_every_sheet_fits_the_standard_image_tier(self):
        for name in os.listdir(self.out):
            if name.startswith("sheet-"):
                w, h = size(os.path.join(self.out, name))
                self.assertLessEqual(max(w, h), 1568, name)
                self.assertLessEqual(-(-w // 28) * -(-h // 28), 1568, name)


# check-curves.js --contacts starts no browser; its timeout, in s, is a guess, unmeasured.
CURVES_RUN_S = 60


class ContactsFromCheckCurves(unittest.TestCase):
    def test_each_printed_contact_is_taken_unchanged_and_cropped_at_the_gap(self):
        self.round_trip(os.path.join(FIXTURES, "drawn-contacts.html"), 633)

    def test_a_contact_on_a_bare_svg_file_is_cropped_there_too(self):  # #354
        # The default 633 px viewport grown to the SVG's 900.
        self.round_trip(os.path.join(FIXTURES, "drawn-contacts.svg"), 900)

    def round_trip(self, page, height):
        listed = subprocess.run(
            ["node", CURVES, "--contacts", page],
            capture_output=True,
            text=True,
            timeout=CURVES_RUN_S,
            check=False,
        )
        self.assertEqual(listed.returncode, 1, listed.stdout + listed.stderr)
        # Each contact line ends with its --contact as one shell word.
        words = [
            shlex.split(line.rsplit(" --contact ", 1)[1])
            for line in listed.stdout.splitlines()
            if " --contact " in line
        ]
        self.assertEqual(len(words), 1, listed.stdout)
        (word,) = words[0]
        name = word.split("=", 1)[0]
        with tempfile.TemporaryDirectory() as out:
            proc = run("contacts", page, "--contact", word, "--out", out)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            with open(os.path.join(out, "renders.json"), encoding="utf8") as fh:
                self.assertEqual(json.load(fh)["viewport"]["height"], height)
            self.assertIn(f"x{height}\n", proc.stdout)
            for scale in (1, 2, 3):
                crop = pixels(os.path.join(out, f"{name}-0ms-{scale}x.png"))
                gap = white_columns(crop)
                # One CSS px of white, magnified 4x, within a CSS px of the centre:
                # the clip rounds a half-pixel centre at 1x.
                self.assertEqual(len(gap), 4 * scale, scale)
                self.assertEqual(gap, list(range(gap[0], gap[0] + 4 * scale)), scale)
                middle = (gap[0] + gap[-1] + 1) / 2
                self.assertLessEqual(abs(middle - crop.shape[1] / 2), 4 * scale, scale)


class Bends(unittest.TestCase):
    # The viewport asked for: --width 1024 and the desktop height check-layout.py gives it.
    WIDTH, HEIGHT = 1024, 633

    def test_a_bend_outside_the_viewport_on_a_bare_svg_file_is_shot_once_the_viewport_fits_it(
        self,
    ):  # #354
        with tempfile.TemporaryDirectory() as out:
            proc = run(
                "bends", os.path.join(FIXTURES, "drawn-contacts.svg"),
                "--width", str(self.WIDTH), "--out", out,
            )  # fmt: skip
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            with open(os.path.join(out, "renders.json"), encoding="utf8") as fh:
                renders = json.load(fh)
            self.assertEqual(renders["viewport"], {"width": 1200, "height": 900})
            (bend,) = [b for b in renders["bends"] if b["shape"] == "circle#dot"]
            self.assertAlmostEqual(bend["radius"], 10, delta=0.05)
            self.assertGreater(bend["at"][0], self.WIDTH)
            self.assertGreater(bend["at"][1], self.HEIGHT)
            self.assertLess(pixels(os.path.join(out, bend["file"])).min(), 64)

    def test_the_tightest_bend_is_shot_at_8x_where_the_curve_turns_hardest(self):
        with tempfile.TemporaryDirectory() as out:
            proc = run("bends", os.path.join(FIXTURES, "bend.html"), "--out", out)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            with open(os.path.join(out, "renders.json"), encoding="utf8") as fh:
                bends = json.load(fh)["bends"]
            self.assertEqual(len(bends), 1, bends)
            # Within 0.05 CSS px, a twentieth of the 1 px a gap at 1x is.
            self.assertAlmostEqual(bends[0]["at"][0], 160, delta=0.05)
            self.assertAlmostEqual(bends[0]["at"][1], 60, delta=0.05)
            self.assertAlmostEqual(bends[0]["radius"], 5, delta=0.05)
            shot = os.path.join(out, bends[0]["file"])
            self.assertEqual(size(shot), (32 * 8, 32 * 8))
            # The vertex's stroke crosses the shot's centre column.
            self.assertLess(pixels(shot)[:, 128].min(), 64)

    def test_every_shape_that_curves_gets_its_bend_where_the_page_draws_it(self):
        with tempfile.TemporaryDirectory() as out:
            proc = run("bends", os.path.join(FIXTURES, "shapes.html"), "--out", out)
            self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
            self.assertIn("path#broken: could not read the path", proc.stdout)
            self.assertNotIn("does not apply", proc.stdout)
            with open(os.path.join(out, "renders.json"), encoding="utf8") as fh:
                renders = json.load(fh)
            bends = {b["shape"]: b for b in renders["bends"]}
            self.assertEqual(
                sorted(bends),
                [
                    "circle#dot",
                    "ellipse#oval",
                    "path#parabola",
                    "polyline#run",
                    "rect#card",
                ],
            )
            for shape, radius in (
                ("circle#dot", 10), ("ellipse#oval", 5), ("rect#card", 8), ("path#parabola", 10),
            ):  # fmt: skip
                self.assertAlmostEqual(
                    bends[shape]["radius"], radius, delta=0.05, msg=shape
                )
            self.assertIn(bends["ellipse#oval"]["at"], ([130, 50], [170, 50]))
            # Stretched twice as far across as down: a uniform scale puts the
            # radius at 3.54.
            self.assertEqual(bends["path#parabola"]["at"], [410, 155])
            self.assertEqual(bends["polyline#run"]["at"], [79.5, 153.5])
            self.assertEqual(bends["polyline#run"]["segments"], 5)
            self.assertEqual(renders["unread"][0]["shape"], "path#broken")

    def test_a_page_with_no_curve_says_the_question_does_not_apply_and_names_the_route_for_css(
        self,
    ):
        with tempfile.TemporaryDirectory() as out:
            proc = run("bends", os.path.join(FIXTURES, "contacts.html"), "--out", out)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("vault.curves-look does not apply", proc.stdout)
            self.assertIn("look.py zoom --scale 8", proc.stdout)

    def test_a_second_run_deletes_the_renders_the_first_made(self):
        with tempfile.TemporaryDirectory() as out:
            run("bends", os.path.join(FIXTURES, "shapes.html"), "--out", out)
            stray = os.path.join(out, "notes.txt")
            with open(stray, "w", encoding="utf8") as fh:
                fh.write("not a render")
            proc = run("bends", os.path.join(FIXTURES, "bend.html"), "--out", out)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertEqual(
                sorted(os.listdir(out)),
                ["bend-1.png", "notes.txt", "renders.json", "sheet-1.png"],
            )


class Times(unittest.TestCase):
    def test_times_names_the_frames_rendered(self):
        with tempfile.TemporaryDirectory() as out:
            proc = run(
                "contacts", os.path.join(FIXTURES, "contacts.html"),
                "--contact", "moving=#piece@0,20", "--times", "500,end", "--out", out,
            )  # fmt: skip
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            with open(os.path.join(out, "renders.json"), encoding="utf8") as fh:
                self.assertEqual(json.load(fh)["times"], [500, 1000])
            self.assertTrue(os.path.isfile(os.path.join(out, "moving-500ms-3x.png")))


class StagedBuilds(unittest.TestCase):
    """#259: a build carried on by finish events, or started in stages."""

    FRAMES = os.path.join(HERE, "fixtures", "frames")

    def test_a_staggered_start_is_drawn_at_one_place_at_every_scale(self):
        with tempfile.TemporaryDirectory() as out:
            proc = run(
                "contacts", os.path.join(self.FRAMES, "staggered.html"),
                "--contact", "late=#bottom@0,0", "--times", "500", "--out", out,
            )  # fmt: skip
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            with open(os.path.join(out, "renders.json"), encoding="utf8") as fh:
                shots = json.load(fh)["shots"]
        self.assertEqual(len(shots), 3)
        self.assertEqual(len({tuple(s["at"]) for s in shots}), 1, shots)

    def test_a_chain_started_by_finish_events_cannot_be_rendered(self):
        for mode, extra in (("contacts", ["--contact", "top=#top@0,0"]), ("bends", [])):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as out:
                proc = run(
                    mode,
                    os.path.join(self.FRAMES, "chained.html"),
                    *extra,
                    "--out",
                    out,
                )
                self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
                self.assertIn(
                    "starts animations when others finish (div#bottom)", proc.stdout
                )


class Arguments(unittest.TestCase):
    def test_a_contact_without_a_point_is_a_usage_error(self):
        proc = run(
            "contacts", os.path.join(FIXTURES, "contacts.html"),
            "--contact", "gap=#a", "--out", "x",
        )  # fmt: skip
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("--contact wants NAME=X,Y", proc.stderr)

    def test_a_contact_whose_point_is_no_number_is_a_usage_error(self):
        proc = run(
            "contacts", os.path.join(FIXTURES, "contacts.html"),
            "--contact", "gap=1.2.3,4", "--out", "x",
        )  # fmt: skip
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("--contact wants NAME=X,Y", proc.stderr)

    def test_times_that_are_not_numbers_are_a_usage_error(self):
        proc = run(
            "contacts", os.path.join(FIXTURES, "contacts.html"),
            "--contact", "gap=0,0", "--times", "soon", "--out", "x",
        )  # fmt: skip
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("--times wants numbers of ms", proc.stderr)

    def test_a_contact_on_no_element_cannot_be_rendered(self):
        with tempfile.TemporaryDirectory() as out:
            proc = run(
                "contacts", os.path.join(FIXTURES, "contacts.html"),
                "--contact", "lost=#nowhere@0,0", "--out", out,
            )  # fmt: skip
            self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
            self.assertIn("#nowhere", proc.stdout)
            self.assertIn("Image.NEAREST", proc.stdout)


class MissingPackages(unittest.TestCase):
    def test_a_missing_package_exits_3_naming_the_pinned_requirements(self):  # #256
        for package in ("numpy", "PIL"):
            with self.subTest(package):
                proc = without(package)
                self.assertEqual(proc.returncode, 3, proc.stderr)
                self.assertIn(f"look-renders.py: {package}", proc.stderr)
                self.assertIn(f"-r {REQUIREMENTS}", proc.stderr)


if __name__ == "__main__":
    child.main()
