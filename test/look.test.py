import os
import re
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
CHECK_FRAMES = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-frames.py"
)
CONTACT_SHEET = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "contact-sheet.py"
)
LOOK_RENDERS = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "look-renders.py"
)
PAGE = os.path.join(HERE, "fixtures", "look", "page.html")
STAGGERED = os.path.join(HERE, "fixtures", "look", "staggered.html")
LATE = os.path.join(HERE, "fixtures", "look", "late.html")
STILL = os.path.join(HERE, "fixtures", "look", "still.html")
SLOW_CANVAS = os.path.join(HERE, "fixtures", "look", "slow-canvas.html")
SLOW_MOVE = os.path.join(HERE, "fixtures", "look", "slow-move.html")


def end_ms(fixture):
    with open(fixture, encoding="utf8") as fh:
        return int(re.search(r"const END_MS = (\d+);", fh.read())[1])


SLOW_CANVAS_END_MS = end_ms(SLOW_CANVAS)
REQUIREMENTS = os.path.realpath(os.path.join(HERE, "..", "plugin", "requirements.txt"))
SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

look = siblings.load(SCRIPTS, "look.py")


def run(*args):
    # guess, #501
    return child.run([sys.executable, SCRIPT, *args], timeout=120)


BLOCKED_RUN_S = 60  # guess, #501
BLOCKED = (
    "import runpy, sys; sys.modules[sys.argv[1]] = None; sys.argv = sys.argv[2:]; "
    "runpy.run_path(sys.argv[0], run_name='__main__')"
)


def without(package, *args):
    return subprocess.run(
        [sys.executable, "-c", BLOCKED, package, SCRIPT, *args],
        capture_output=True,
        text=True,
        timeout=BLOCKED_RUN_S,
        check=False,
    )


class Siblings(unittest.TestCase):  # #558
    def test_check_layout_and_check_frames_share_one_check_flow(self):
        self.assertIs(look.layout.flow, look.frames.flow)


class Height(unittest.TestCase):
    def test_a_zoom_or_measure_frames_check_layouts_first_screen_at_that_width_169(
        self,
    ):
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

    def test_a_scrub_frames_the_motion_scripts_window_where_a_zoom_or_measure_frames_check_layouts(
        self,
    ):  # #548
        for width, tall in ((375, 664), (800, 921), (1536, 945), (1920, 945)):
            at = look.parse(["scrub", PAGE, "--out", "x", "--width", str(width)])
            self.assertEqual(at.height, tall, width)

    def test_scrub_and_look_renders_default_to_the_window_check_frames_and_the_contact_sheet_render(
        self,
    ):  # #548
        with tempfile.TemporaryDirectory() as out:
            _, frames = look.siblings.load(look.HERE, CHECK_FRAMES).parse(
                ["hash", PAGE, "--out", out]
            )
            sheet = look.siblings.load(look.HERE, CONTACT_SHEET).parse(
                [PAGE, "--out", out]
            )
            renders = look.siblings.load(look.HERE, LOOK_RENDERS)
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

    def test_a_phone_scrub_frames_the_contact_sheets_phone(self):  # #548
        with tempfile.TemporaryDirectory() as out:
            sheet = look.siblings.load(look.HERE, CONTACT_SHEET).parse(
                [PAGE, "--out", out]
            )
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

    def test_a_step_scale_or_until_below_its_least_is_a_usage_error(self):  # #154
        for args, message in (
            (("scrub", PAGE, "--out", "x", "--step", "0"), "--step wants 1 or more"),
            (("scrub", PAGE, "--out", "x", "--until", "-1"), "--until wants 0 or more"),
            (
                ("scrub", PAGE, "--out", "x", "--height", "0"),
                "--height wants 1 or more",
            ),
            (
                ("zoom", PAGE, "--clip", "1,2,3,4", "--out", "x.png", "--scale", "0"),
                "--scale wants 1 or more",
            ),
        ):
            proc = run(*args)
            self.assertEqual(proc.returncode, 2, proc.stderr)
            self.assertIn(message, proc.stderr)

    def test_pixels_on_a_missing_image_is_a_usage_error(self):  # #154
        proc = run("pixels", "no-such.png", "--at", "1,1", "--against", "2,2")
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("no-such.png is no image it can read", proc.stderr)


class Page(unittest.TestCase):
    def test_measure_names_the_part_its_font_and_colour_170(self):
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
            self.assertEqual(shot.convert("RGB").getpixel((100, 50)), (0, 0, 0))

    def test_zoom_after_waits_out_a_canvas_build_longer_than_the_settle_613(self):
        with tempfile.TemporaryDirectory() as d:
            shots = {}
            for name, extra in (
                ("default", ()),
                ("after", ("--after", str(SLOW_CANVAS_END_MS + 1000))),
            ):
                out = os.path.join(d, f"{name}.png")
                proc = run(
                    "zoom",
                    SLOW_CANVAS,
                    "--clip",
                    "0,0,100,100",
                    "--scale",
                    "1",
                    "--out",
                    out,
                    *extra,
                )
                self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                shots[name] = Image.open(out).convert("RGB").getpixel((50, 50))
            self.assertEqual(shots, {"default": (255, 255, 255), "after": (0, 0, 0)})

    def test_measure_after_finds_a_part_a_script_moves_later_than_the_settle_154(self):
        found = {}
        for name, extra in (
            ("default", ()),
            ("after", ("--after", str(end_ms(SLOW_MOVE) + 1000))),
        ):
            proc = run("measure", SLOW_MOVE, "--at", "350,50", *extra)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            found[name] = proc.stdout
        self.assertNotIn("div#mover", found["default"])
        self.assertIn('"element": "div#mover"', found["after"])

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
            self.assertAlmostEqual(int(grey[1]), 128, delta=3)
            self.assertEqual(grey[2], 0)


def first_dark_x(png, row) -> int | None:
    dark = np.flatnonzero(np.asarray(Image.open(png).convert("L"))[row] < 128)
    return int(dark[0]) if dark.size else None


ROW_A, ROW_B = 60, 140
# 100 ms of staggered.html's half-px-a-ms move, a guess at a timer's lateness, #547.
STAGGER_PX = 50


def timer_ms(fixture):
    with open(fixture, encoding="utf8") as fh:
        return int(re.search(r"setTimeout\(.*, (\d+)\)", fh.read()).group(1))


class Staggered(unittest.TestCase):  # #547
    def test_the_fixtures_timers_sit_either_side_of_quiet_ms_and_inside_twice_it(self):
        quiet = look.frames.QUIET_MS
        self.assertLess(timer_ms(STAGGERED), quiet)
        self.assertLess(quiet, timer_ms(LATE))
        self.assertLess(timer_ms(LATE), 2 * quiet)

    def test_a_move_a_timer_starts_sits_at_its_own_time_since_load(self):
        with tempfile.TemporaryDirectory() as d:
            proc = run(
                "scrub", STAGGERED, "--out", d, "--step", "200", "--until", "1000"
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

            def edge(t, row):
                return first_dark_x(os.path.join(d, f"t{t:05d}.png"), row)

            self.assertEqual((edge(200, ROW_A), edge(1000, ROW_A)), (100, 500))
            self.assertEqual(edge(200, ROW_B), 0)
            self.assertAlmostEqual(edge(1000, ROW_B), 350, delta=STAGGER_PX)

    def test_a_move_started_after_the_timeline_was_read_is_refused_unwritten(self):
        with tempfile.TemporaryDirectory() as d:
            Image.new("RGB", (1, 1)).save(os.path.join(d, "t00000.png"))
            proc = run("scrub", LATE, "--out", d, "--step", "500", "--until", "1000")
            self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
            self.assertIn("starts animations after its frames were read", proc.stdout)
            self.assertIn("Scrub it by eye", proc.stdout)
            self.assertEqual(os.listdir(d), [])

    def test_a_page_with_no_motion_is_named_still(self):
        with tempfile.TemporaryDirectory() as d:
            proc = run("scrub", STILL, "--out", d, "--step", "500", "--until", "500")
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("is read as still", proc.stdout)


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
