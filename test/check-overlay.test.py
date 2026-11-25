"""Tests plugin/skills/design-round/scripts/check-overlay.py (#73): python3 test/check-overlay.test.py

Loosen the limit (0.5 px against a raster source, 0.1 px against an SVG one, #195) and a
traced mark shifted off its source, or a polygon chain passed off as a circle, passes the
craft gate (gate question vault.curves-script). Drop the
screenshot retry and a loaded machine turns the commit gate red (#136): those cases
run draw() in-process on a stand-in page, since only a stalled renderer makes a real
one fail (test/load/check-overlay-shot.py).
"""

import base64
import importlib.util
import io
import math
import os
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image, ImageDraw
from playwright.sync_api import Error

SCRIPT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "plugin",
    "skills",
    "design-round",
    "scripts",
    "check-overlay.py",
)
sys.path.insert(0, os.path.dirname(__file__))
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

REQUIREMENTS = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "..", "plugin", "requirements.txt")
)
spec = importlib.util.spec_from_file_location("check_overlay", SCRIPT)
overlay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(overlay)
ARCH = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80" width="120" height="80">'
    '<g transform="translate({dx} 0)"><path d="M20 70 C20 20 100 20 100 70 Z" fill="#222"/>'
    '<circle cx="60" cy="45" r="10" fill="#fff"/></g></svg>'
)

ELLIPSE = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80" width="120" height="80">'
    '<ellipse cx="{dx}" cy="40" rx="30" ry="25" transform="translate(60 0)" fill="#1e1e1e"/></svg>'
)


def run(*args):
    # A guess for check-overlay.py alone, not taken from the other tests' timeouts: one run takes seconds here.
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


class Overlay(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)

    def file(self, name, text):
        path = os.path.join(self.dir.name, name)
        with open(path, "w", encoding="utf8") as fh:
            fh.write(text)
        return path

    def png(self, name, dx):
        image = Image.new("RGBA", (120, 80), (0, 0, 0, 0))
        ImageDraw.Draw(image).ellipse(
            (30 + dx, 15, 90 + dx, 65), fill=(30, 30, 30, 255)
        )
        path = os.path.join(self.dir.name, name)
        image.save(path)
        return path

    def smooth_png(self, name, dx):
        """ELLIPSE drawn at 8x and shrunk, so its edge carries a shift under a pixel."""
        image = Image.new("RGBA", (960, 640), (0, 0, 0, 0))
        ImageDraw.Draw(image).ellipse(
            ((30 + dx) * 8, 15 * 8, (90 + dx) * 8, 65 * 8), fill=(30, 30, 30, 255)
        )
        path = os.path.join(self.dir.name, name)
        image.resize((120, 80), Image.BOX).save(path)
        return path

    def test_a_copy_of_an_svg_source_passes(self):
        source = self.file("source.svg", ARCH.format(dx=0))
        proc = run(self.file("mark.svg", ARCH.format(dx=0)), source)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("largest edge offset: 0.000 px (PASS", proc.stdout)

    def test_the_same_shape_shifted_1_px_fails(self):
        source = self.file("source.svg", ARCH.format(dx=0))
        proc = run(self.file("mark.svg", ARCH.format(dx=1)), source)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("largest edge offset: 1.0", proc.stdout)
        self.assertIn("px (FAIL", proc.stdout)
        self.assertIn(
            "ink boxes (x, y, w, h): source 20.00, 32.50, 80.00, 37.50; mark 21.00,",
            proc.stdout,
        )

    def test_against_an_svg_source_a_shift_of_0_02_px_passes_and_0_2_px_fails(self):
        # The measure reads up to 0.05 px high at 8x, so 0.02 px reads under the 0.1 px limit.
        source = self.file("source.svg", ARCH.format(dx=0))
        self.assertEqual(
            run(self.file("near.svg", ARCH.format(dx=0.02)), source).returncode, 0
        )
        proc = run(self.file("far.svg", ARCH.format(dx=0.2)), source)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertRegex(
            proc.stdout,
            r"largest edge offset: 0\.2\d+ px \(FAIL, the limit is 0\.1 px against an SVG source\)",
        )

    def test_against_a_raster_source_a_shift_of_0_3_px_passes_and_0_7_px_fails(self):
        source = self.smooth_png("source.png", 0)
        proc = run(self.smooth_png("near.png", 0.3), source)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("the limit is 0.5 px against a raster source", proc.stdout)
        proc = run(self.smooth_png("far.png", 0.7), source)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertRegex(
            proc.stdout,
            r"px \(FAIL, the limit is 0\.5 px against a raster source\)",
        )

    def test_an_svg_that_only_wraps_a_raster_is_held_to_the_raster_limit(self):
        with open(self.smooth_png("source.png", 0), "rb") as fh:
            png = base64.b64encode(fh.read()).decode()
        source = self.file(
            "source.svg",
            '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 120 80" width="120" height="80">'
            f'<image width="120" height="80" xlink:href="data:image/png;base64,{png}"/></svg>',
        )
        proc = run(self.smooth_png("near.png", 0.3), source)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("the limit is 0.5 px against a raster source", proc.stdout)

    def test_the_0_3_px_shift_a_raster_source_allows_fails_against_an_svg_source(self):
        proc = run(
            self.file("near.svg", ELLIPSE.format(dx=0.3)),
            self.file("source.svg", ELLIPSE.format(dx=0)),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertRegex(
            proc.stdout,
            r"largest edge offset: 0\.3\d+ px \(FAIL, the limit is 0\.1 px against an SVG source\)",
        )

    def test_a_light_part_on_white_moved_5_px_fails(self):
        # #73 review: cut at half the darkest part's strength, a #bbb part on white had no edge, and passed.
        light = ARCH.format(dx=0).replace(
            "<g ", '<rect width="120" height="80" fill="#fff"/><g '
        )
        source = self.file(
            "source.svg",
            light.replace("</g>", '<circle cx="12" cy="12" r="6" fill="#bbb"/></g>'),
        )
        proc = run(
            self.file(
                "mark.svg",
                light.replace(
                    "</g>", '<circle cx="17" cy="12" r="6" fill="#bbb"/></g>'
                ),
            ),
            source,
        )
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("largest edge offset: 5.0", proc.stdout)

    def test_a_scale_under_4_is_refused(self):
        # check-overlay.py's MIN_SCALE floor, measured in #73's review.
        source = self.file("source.svg", ARCH.format(dx=0))
        proc = run(source, source, "--scale", "2")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("a scale under 4 reads the offset up to 0.3 px high", proc.stderr)

    def test_ink_the_mark_adds_beyond_the_source_fails(self):
        # Every source edge has a mark edge on it; only the mark's own dot strays.
        source = self.file("source.svg", ARCH.format(dx=0))
        proc = run(
            self.file(
                "mark.svg",
                ARCH.format(dx=0).replace(
                    "</g>", '<circle cx="110" cy="10" r="3"/></g>'
                ),
            ),
            source,
        )
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("a mark edge lies that far from the other's nearest", proc.stdout)

    def test_a_raster_source_and_its_copy_pass_and_a_1_px_shift_fails(self):
        source = self.png("source.png", 0)
        self.assertEqual(run(self.png("copy.png", 0), source).returncode, 0)
        proc = run(self.png("shifted.png", 1), source)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertRegex(proc.stdout, r"largest edge offset: 1\.\d+ px \(FAIL")

    def test_94_a_30_segment_chain_fails_against_its_circle_though_it_overlaps_above_0_9(
        self,
    ):
        # #94 (the builder's "mark overlap 0.90" and the critic's "IoU 0.96" both passed a faceted mark);
        # its positive pair is test_a_copy_of_an_svg_source_passes.
        r, c = 200, 220
        ring = " ".join(
            f"{c + r * math.cos(2 * math.pi * k / 30):.3f},{c + r * math.sin(2 * math.pi * k / 30):.3f}"
            for k in range(30)
        )
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440" width="440" height="440">{}</svg>'
        source = self.file(
            "circle.svg", svg.format(f'<circle cx="{c}" cy="{c}" r="{r}"/>')
        )
        mark = self.file("chain.svg", svg.format(f'<polygon points="{ring}"/>'))
        yy, xx = np.mgrid[0:880, 0:880] / 2 + 0.25
        disc = np.hypot(xx - c, yy - c) <= r
        chain = np.hypot(xx - c, yy - c) * np.cos(
            (np.arctan2(yy - c, xx - c) % (2 * math.pi / 30)) - math.pi / 30
        ) <= r * math.cos(math.pi / 30)
        self.assertGreater((disc & chain).sum() / (disc | chain).sum(), 0.9)
        proc = run(mark, source)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        # The chain's chords sit r(1 - cos 6°) = 1.10 px inside the circle at their middles.
        self.assertRegex(proc.stdout, r"largest edge offset: 1\.\d+ px \(FAIL")
        self.assertNotIn("IoU", proc.stdout)

    def test_overlay_png_is_written_at_the_measured_scale(self):
        source = self.file("source.svg", ARCH.format(dx=0))
        out = os.path.join(self.dir.name, "out")
        proc = run(self.file("mark.svg", ARCH.format(dx=1)), source, "--out", out)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        with Image.open(os.path.join(out, "overlay.png")) as image:
            self.assertEqual(image.size, (960, 640))

    def test_a_mark_framed_in_another_viewbox_is_drawn_into_the_source_box(self):
        # The same arch at twice the coordinates, viewBox scaled to match, lands on the source.
        source = self.file("source.svg", ARCH.format(dx=0))
        big = (
            ARCH.format(dx=0)
            .replace(
                'viewBox="0 0 120 80" width="120" height="80"', 'viewBox="0 0 240 160"'
            )
            .replace('<g transform="translate(0 0)">', '<g transform="scale(2)">')
        )
        proc = run(self.file("big.svg", big), source)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_a_transparent_mark_matches_its_source_drawn_on_white(self):
        # Guards against judging each file's ground alone (#73 review).
        source = self.file(
            "source.svg",
            ARCH.format(dx=0).replace(
                "<g ", '<rect width="120" height="80" fill="#fff"/><g '
            ),
        )
        proc = run(self.file("mark.svg", ARCH.format(dx=0)), source)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        # Laid on white and drawn on white round apart by a thousandth of a pixel.
        self.assertRegex(proc.stdout, r"largest edge offset: 0\.00\d px \(PASS")

    def test_a_transparent_mark_shifted_1_px_off_its_source_on_white_fails(self):
        source = self.file(
            "source.svg",
            ARCH.format(dx=0).replace(
                "<g ", '<rect width="120" height="80" fill="#fff"/><g '
            ),
        )
        proc = run(self.file("mark.svg", ARCH.format(dx=1)), source)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("largest edge offset: 1.0", proc.stdout)
        self.assertIn("px (FAIL", proc.stdout)

    def test_a_size_that_is_not_two_positive_numbers_is_refused(self):
        source = self.file("source.svg", ARCH.format(dx=0))
        for size, says in (
            ("120", "--size wants WxH"),
            ("0x0", "--size wants a positive"),
            ("-5x10", "--size wants a positive"),
        ):
            proc = run(source, source, f"--size={size}")
            self.assertEqual(proc.returncode, 2, size + proc.stdout + proc.stderr)
            self.assertIn(says, proc.stderr)

    def test_an_svg_with_no_viewbox_drawn_at_another_size_is_refused(self):
        source = self.file("source.svg", ARCH.format(dx=0))
        bare = self.file(
            "bare.svg",
            '<svg xmlns="http://www.w3.org/2000/svg" width="60" height="40"><rect width="60" height="40"/></svg>',
        )
        proc = run(bare, source)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn('add viewBox="0 0 60 40"', proc.stderr)

    def test_a_mark_with_no_ink_cannot_be_measured(self):
        source = self.file("source.svg", ARCH.format(dx=0))
        empty = self.file(
            "empty.svg",
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80"></svg>',
        )
        proc = run(empty, source)
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(f"cannot measure: {empty} draws no ink", proc.stdout)


class UncapturedScreenshots(unittest.TestCase):
    class Page:
        def __init__(
            self,
            fails,
            message="Protocol error (Page.captureScreenshot): Unable to capture screenshot",
        ):
            self.fails, self.message, self.shots = fails, message, 0

        def set_content(self, html):
            pass

        def evaluate(self, script):
            pass

        def screenshot(self, **kwargs):
            self.shots += 1
            if self.shots <= self.fails:
                raise Error(self.message)
            png = io.BytesIO()
            Image.new("RGBA", (2, 2), (0, 0, 0, 255)).save(png, "PNG")
            return png.getvalue()

    FILE = {"mime": "image/svg+xml", "data": b"<svg/>"}

    def test_a_screenshot_the_browser_could_not_capture_is_taken_again(self):
        page = self.Page(fails=1)
        self.assertEqual(overlay.draw(page, self.FILE, (2, 2)).shape, (2, 2, 4))
        self.assertEqual(page.shots, 2)

    def test_a_screenshot_never_captured_still_refuses(self):
        page = self.Page(fails=99)
        with self.assertRaisesRegex(Error, overlay.UNCAPTURED):
            overlay.draw(page, self.FILE, (2, 2))
        self.assertEqual(page.shots, overlay.SHOTS)

    def test_another_browser_error_is_not_retried(self):
        page = self.Page(
            fails=1, message="Target page, context or browser has been closed"
        )
        with self.assertRaisesRegex(Error, "has been closed"):
            overlay.draw(page, self.FILE, (2, 2))
        self.assertEqual(page.shots, 1)


class MissingPackages(unittest.TestCase):
    def test_a_missing_package_exits_3_naming_the_pinned_requirements(self):  # #256
        for package in ("numpy", "PIL", "scipy"):
            with self.subTest(package):
                proc = without(package)
                self.assertEqual(proc.returncode, 3, proc.stderr)
                self.assertIn(f"check-overlay.py: {package}", proc.stderr)
                self.assertIn(f"-r {REQUIREMENTS}", proc.stderr)


if __name__ == "__main__":
    child.main()
