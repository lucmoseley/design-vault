import os
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

SCRIPT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "plugin",
    "skills",
    "design-round",
    "scripts",
    "cutout.py",
)
SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

cutout = siblings.load(SCRIPTS, "cutout.py")
REQUIREMENTS = os.path.realpath(
    os.path.join(SCRIPTS, "..", "..", "..", "requirements.txt")
)

W, H, SS = 200, 160, 8
KEY = np.array([0, 177, 64], np.float32)
OUTLINE = np.array([40, 28, 36], np.float32)
FILL = np.array([240, 140, 40], np.float32)


def coverage(mask):
    return mask.reshape(H, SS, W, SS).mean((1, 3))


def fixture():
    y, x = np.mgrid[0 : H * SS, 0 : W * SS]
    x = (x + 0.5) / SS
    y = (y + 0.5) / SS
    r = np.hypot(x - 100, y - 110)
    disc = coverage(r < 70)
    fill = coverage(r < 62)
    hole = coverage(np.hypot(x - 100, y - 80) < 12)
    slot = coverage((x >= 94) & (x < 106) & (y >= 115))
    img = KEY * (1 - disc)[..., None] + OUTLINE * (disc - fill)[..., None]
    img = img + FILL * (fill - hole - slot)[..., None] + KEY * (hole + slot)[..., None]
    masks = {"disc": disc, "fill": fill, "hole": hole, "slot": slot}
    return img.round().astype(np.uint8), masks


class Cut(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rgb, cls.masks = fixture()
        cls.rgba, cls.report = cutout.cut(cls.rgb)
        cls.alpha = cls.rgba[..., 3] / 255

    def test_the_key_is_the_border_median_56(self):
        np.testing.assert_array_equal(self.report["key"], KEY)

    def test_the_background_is_clear(self):
        self.assertTrue((self.alpha[self.masks["disc"] == 0] == 0).all())

    def test_the_outline_edge_is_unmixed_to_its_coverage(self):
        m = self.masks
        edge = (m["disc"] > 0.1) & (m["disc"] < 0.9)
        self.assertGreater(edge.sum(), 100)
        np.testing.assert_allclose(self.alpha[edge], m["disc"][edge], atol=0.02)

    def test_the_outline_edge_keeps_no_key_fringe(self):
        edge = self.alpha > 0
        edge &= self.alpha < 1
        edge &= self.masks["fill"] == 0
        self.assertGreater(edge.sum(), 100)
        self.assertTrue((self.rgba[edge][:, :3] == OUTLINE).all())

    def test_the_solid_subject_is_untouched(self):
        inside = self.masks["fill"] == 1
        inside &= self.masks["hole"] == 0
        inside &= self.masks["slot"] == 0
        self.assertTrue((self.alpha[inside] == 1).all())
        np.testing.assert_array_equal(self.rgba[inside][:, :3], self.rgb[inside])

    def test_the_enclosed_hole_stays_opaque_and_is_reported(self):
        hole = self.masks["hole"] == 1
        self.assertTrue((self.alpha[hole] == 1).all())
        np.testing.assert_array_equal(self.rgba[hole][:, :3], self.rgb[hole])
        self.assertEqual(len(self.report["holes"]), 1)
        size, x0, y0, x1, y1 = self.report["holes"][0]
        self.assertAlmostEqual(size, hole.sum(), delta=hole.sum() * 0.2)
        self.assertTrue(x0 <= 90 and x1 >= 110 and y0 <= 70 and y1 >= 90)

    def test_the_key_coloured_part_reaching_the_frame_is_cut(self):
        self.assertTrue((self.alpha[self.masks["slot"] == 1] == 0).all())

    def test_an_edge_pixel_off_the_key_to_outline_line_is_projected_onto_it(self):
        fb = OUTLINE - KEY
        off = np.cross(fb, [1, 0, 0])
        off *= 30 / np.linalg.norm(off)
        edge = (self.masks["disc"] > 0) & (self.masks["disc"] < 1)
        rgb = self.rgb.astype(np.float32)
        rgb[edge] += off
        rgba, _ = cutout.cut(rgb.round().astype(np.uint8))
        band = (self.masks["disc"] > 0.1) & (self.masks["disc"] < 0.9)
        np.testing.assert_allclose(
            rgba[..., 3][band] / 255, self.masks["disc"][band], atol=0.02
        )

    def test_the_partial_share_counts_the_edge_band(self):
        kept = self.alpha > 0
        partial = kept & (self.alpha < 1)
        self.assertAlmostEqual(self.report["partial_share"], partial.sum() / kept.sum())
        self.assertGreater(self.report["partial_share"], 0)


class Cli(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run(
            [sys.executable, SCRIPT, *args], capture_output=True, text=True
        )

    def test_it_writes_the_cut_and_both_backdrops_and_prints_the_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            render = os.path.join(tmp, "v1-mascot.png")
            Image.fromarray(fixture()[0], "RGB").save(render)
            done = self.run_script(render)
            self.assertEqual(done.returncode, 0, done.stderr)
            cut = Image.open(os.path.join(tmp, "v1-mascot-cut.png"))
            self.assertEqual(cut.mode, "RGBA")
            for name in ("dark", "bright"):
                self.assertTrue(
                    os.path.exists(os.path.join(tmp, f"v1-mascot-cut-on-{name}.png"))
                )
            self.assertIn("key #00b140", done.stdout)
            self.assertIn("partly transparent:", done.stdout)
            self.assertRegex(
                done.stdout, r"inside the subject .*\n  \d+ px, x \d+–\d+, y \d+–\d+"
            )

    def refused(self, rgb):
        with tempfile.TemporaryDirectory() as tmp:
            render = os.path.join(tmp, "render.png")
            Image.fromarray(rgb, "RGB").save(render)
            done = self.run_script(render)
            self.assertFalse(os.path.exists(os.path.join(tmp, "render-cut.png")))
        self.assertEqual(done.returncode, 1)
        return done.stderr

    def test_a_render_of_nothing_but_the_key_is_refused_as_having_no_subject(self):
        stderr = self.refused(np.full((64, 64, 3), KEY, np.uint8))
        self.assertIn("nothing cut — key #00b140, and no subject found", stderr)

    def test_a_render_with_no_plain_border_is_refused_as_having_no_background(self):
        checks = (np.indices((64, 64)).sum(0) % 2 * 255).astype(np.uint8)
        stderr = self.refused(np.dstack([checks] * 3))
        self.assertIn("no background touches the frame's edge", stderr)

    def test_a_cut_that_cannot_be_written_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            render = os.path.join(tmp, "v1-mascot.png")
            Image.fromarray(fixture()[0], "RGB").save(render)
            done = self.run_script(
                render, "--out", os.path.join(tmp, "missing", "cut.png")
            )
        self.assertEqual(done.returncode, 2)
        self.assertIn("cannot write the cut", done.stderr)

    def test_a_package_present_but_unimportable_exits_3_naming_it_501_paired_with_it_writes_the_cut(
        self,
    ):
        for package in ("numpy", "PIL", "scipy"):
            with self.subTest(package=package), tempfile.TemporaryDirectory() as shadow:
                os.mkdir(os.path.join(shadow, package))
                with open(os.path.join(shadow, package, "__init__.py"), "w") as fh:
                    fh.write(f"raise ImportError('shadowed', name={package!r})\n")
                done = subprocess.run(
                    [sys.executable, SCRIPT, os.path.join(shadow, "render.png")],
                    capture_output=True,
                    text=True,
                    env={**os.environ, "PYTHONPATH": shadow},
                )
                self.assertEqual(done.returncode, 3, done.stderr)
                self.assertIn(
                    f"cutout.py: {package} is missing — python3 -m pip install -r {REQUIREMENTS}",
                    done.stderr,
                )

    def test_a_cut_not_saved_as_png_is_refused(self):
        done = self.run_script("any.png", "--out", "cut.webp")
        self.assertEqual(done.returncode, 2)


if __name__ == "__main__":
    unittest.main()
