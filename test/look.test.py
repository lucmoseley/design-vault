"""Tests plugin/skills/design-round/scripts/look.py (#170): python3 test/look.test.py

A settle critic answers a split by zooming, scrubbing and measuring (#169
Q1 (A)). Break the default height and its zooms frame a different first
screen than the packet's shots (#169's 720 against 900); break measure or
pixels and it settles on a wrong number.
"""

import importlib.util
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
    HERE, "..", "plugin", "skills", "design-round", "scripts", "look.py"
)
PAGE = os.path.join(HERE, "fixtures", "look", "page.html")
REQUIREMENTS = os.path.realpath(os.path.join(HERE, "..", "plugin", "requirements.txt"))
spec = importlib.util.spec_from_file_location("look", SCRIPT)
look = importlib.util.module_from_spec(spec)
spec.loader.exec_module(look)


def run(*args):
    # A guess for look.py alone: a run here takes about SETTLE_MS plus a launch.
    return child.run([sys.executable, SCRIPT, *args], timeout=120)


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


def script(name):
    path = os.path.join(os.path.dirname(SCRIPT), name)
    spec = importlib.util.spec_from_file_location(name.replace("-", "_")[:-3], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Height(unittest.TestCase):
    def test_a_zoom_or_measure_frames_check_layouts_first_screen_at_that_width(self):
        for cmd in (
            ["measure", PAGE, "--at", "1,1"],
            ["zoom", PAGE, "--clip", "0,0,1,1", "--out", "x.png"],
        ):
            for width, tall in ((375, 664), (800, 921), (1920, 633)):
                at = look.parse([*cmd, "--width", str(width)])
                self.assertEqual(at.height, tall, (cmd[0], width))

    def test_with_no_width_the_commonest_desktop_and_its_first_screen_are_framed(self):
        at = look.parse(["measure", PAGE, "--at", "1,1"])
        self.assertEqual((at.width, at.height), (1920, 633))

    def test_a_scrub_frames_the_motion_scripts_window(self):  # #548
        for width, tall in ((375, 664), (800, 921), (1536, 945), (1920, 945)):
            at = look.parse(["scrub", PAGE, "--out", "x", "--width", str(width)])
            self.assertEqual(at.height, tall, width)

    def test_scrub_and_look_renders_default_to_the_window_check_frames_and_the_contact_sheet_render(
        self,
    ):  # #548
        with tempfile.TemporaryDirectory() as out:
            _, frames = script("check-frames.py").parse(["hash", PAGE, "--out", out])
            sheet = script("contact-sheet.py").parse([PAGE, "--out", out])
            renders = script("look-renders.py")
            shots = {
                mode: renders.parse([mode, PAGE, "--out", out, *extra]).viewport_size
                for mode, extra in (("contacts", ["--contact", "a=1,1"]), ("bends", []))
            }
        scrub = look.parse(["scrub", PAGE, "--out", "x"])
        motion = {"width": scrub.width, "height": scrub.height}
        self.assertEqual(motion, {"width": 1920, "height": 945})
        self.assertEqual(motion, sheet.desktop)
        self.assertEqual(motion, frames.viewport_size)
        self.assertEqual(shots, {"contacts": motion, "bends": motion})
        # The phone, too: a 390 px scrub or crop frames the contact sheet's phone.
        phone = look.parse(["scrub", PAGE, "--out", "x", "--width", "390"])
        self.assertEqual({"width": 390, "height": phone.height}, sheet.phone)

    def test_a_given_height_wins(self):
        self.assertEqual(
            look.parse(["measure", PAGE, "--at", "1,1", "--height", "823"]).height, 823
        )


class Arguments(unittest.TestCase):
    def test_a_clip_short_of_four_numbers_is_a_usage_error(self):
        proc = run("zoom", PAGE, "--clip", "1,2,3", "--out", "x.png")
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("--clip wants 4 numbers", proc.stderr)

    def test_a_width_outside_the_sweep_is_a_usage_error(self):
        proc = run("measure", PAGE, "--at", "1,1", "--width", "200")
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("--width 200 is outside", proc.stderr)


class Page(unittest.TestCase):
    def test_measure_names_the_part_its_font_and_colour(self):
        proc = run("measure", PAGE, "--at", "50,50")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn('"element": "h1#title"', proc.stdout)
        self.assertIn('"font": "32px 700 monospace"', proc.stdout)
        self.assertIn('"colour": "rgb(0, 0, 0)"', proc.stdout)

    def test_a_phone_width_has_a_touch_screen_as_the_packets_phone_shots_do(self):
        proc = run("measure", PAGE, "--at", "50,50", "--width", "390")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn('"font": "40px 700 monospace"', proc.stdout)

    def test_zoom_shoots_the_clip_at_its_scale(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "z.png")
            proc = run(
                "zoom", PAGE, "--clip", "0,200,50,25", "--scale", "4", "--out", out
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            shot = Image.open(out)
            self.assertEqual(shot.size, (200, 100))
            # The fade has finished: the box is black.
            self.assertEqual(shot.convert("RGB").getpixel((100, 50)), (0, 0, 0))

    def test_scrub_stops_the_fade_at_each_frame(self):
        with tempfile.TemporaryDirectory() as d:
            proc = run("scrub", PAGE, "--out", d, "--step", "500", "--until", "1000")
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertEqual(
                sorted(os.listdir(d)), ["t00000.png", "t00500.png", "t01000.png"]
            )
            grey = [
                np.asarray(Image.open(os.path.join(d, f)).convert("L"))[250, 100]
                for f in sorted(os.listdir(d))
            ]
            self.assertEqual(grey[0], 255)
            # Half of a linear fade, give or take the rounding of an 8-bit grey.
            self.assertAlmostEqual(int(grey[1]), 128, delta=3)
            self.assertEqual(grey[2], 0)


class Pixels(unittest.TestCase):
    def test_black_against_white_is_21_to_1(self):
        with tempfile.TemporaryDirectory() as d:
            png = os.path.join(d, "p.png")
            shot = np.full((10, 10, 3), 255, dtype=np.uint8)
            shot[:, :5] = 0
            Image.fromarray(shot).save(png)
            proc = run("pixels", png, "--at", "1,1", "--against", "8,8")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(proc.stdout.strip(), "#000000 against #ffffff: 21.00:1")
            proc = run("pixels", png, "--at", "1,1", "--against", "10,1")
            self.assertEqual(proc.returncode, 2, proc.stderr)
            self.assertIn("outside the 10x10 image", proc.stderr)


class MissingPackages(unittest.TestCase):
    def test_a_missing_package_exits_3_naming_the_pinned_requirements(self):  # #256
        for package in ("numpy", "PIL"):
            with self.subTest(package):
                proc = without(
                    package, "pixels", "a.png", "--at", "0,0", "--against", "1,1"
                )
                self.assertEqual(proc.returncode, 3, proc.stderr)
                self.assertIn(f"look.py: {package}", proc.stderr)
                self.assertIn(f"-r {REQUIREMENTS}", proc.stderr)


if __name__ == "__main__":
    child.main()
