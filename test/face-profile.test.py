"""Tests plugin/skills/design-round/scripts/face-profile.py (#282): python3 test/face-profile.test.py

The page, test/fixtures/face/faces.html, sets its text in two fixture fonts
whose every figure make-fonts.py fixes: a variable face (x-height 0.5, stem
0.1, axes wght, wdth, opsz 8–144 and GRAD) and a static one (x-height 0.4,
stem 0.06). Loosen one and the typeface-traits records read a wrong face:
a size floor scaled by the wrong x-height, tracking that ignores an opsz
axis, a weight floor that misses a thin stem.
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "face-profile.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "face")
# The fixture fonts' figures as make-fonts.py sets them, in em: a figure off by
# more than this is a misread, not sub-pixel drawing.
CLOSE = 0.002


# The pangram's average character at advance a (in units of 1000) with its
# 8 spaces of 250: (35 a + 8 × 250) / 43 / 1000.
def pangram(advance):
    return (35 * advance + 2000) / 43000


def run(page, *args):
    # A guess for face-profile.py alone: one run takes about 10 s here.
    return child.run(
        [sys.executable, SCRIPT, os.path.join(FIXTURES, page), *args],
        timeout=180,
    )


class Profile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = tempfile.mkdtemp()
        cls.addClassCleanup(shutil.rmtree, cls.out)
        stale = os.path.join(cls.out, "face-profile.json")
        with open(stale, "w", encoding="utf8") as fh:
            fh.write("{}")
        cls.proc = run("faces.html", "--out", cls.out)
        with open(stale, encoding="utf8") as fh:
            cls.got = json.load(fh)

    def faces(self, width):
        return self.got["widths"][str(width)]

    def one(self, width, **match):
        found = [
            f for f in self.faces(width) if all(f[k] == v for k, v in match.items())
        ]
        self.assertEqual(len(found), 1, f"{match} at {width}px: {found}")
        return found[0]

    def near(self, got, want):
        self.assertAlmostEqual(got, want, delta=CLOSE)

    def test_it_writes_the_profile_at_the_phone_and_desktop_widths(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)
        self.assertEqual(sorted(self.got["widths"]), ["1920", "390"])
        self.assertIn("written: ", self.proc.stdout)

    def test_the_body_setting_is_the_one_with_the_most_body_text(self):
        # The page's phone rule sets paragraphs at 18 px. The plain face holds more
        # characters, most of them inline code.
        for width, size in ((1920, 16), (390, 18)):
            body = self.faces(width)[0]
            self.assertTrue(body.get("body"), body)
            self.assertEqual(
                (body["family"], body["size"]), ('"Fixture Flex", serif', size)
            )
            self.assertEqual(sum(f.get("body", False) for f in self.faces(width)), 1)

    def test_x_height_is_the_ex_unit_over_the_size(self):
        self.near(self.faces(1920)[0]["xheight"], 0.5)
        self.near(self.one(1920, size=14)["xheight"], 0.4)
        # font-size-adjust: 0.6 scales the static face so its ex is 0.6 of the size.
        self.near(self.one(1920, size=16, size_adjust="0.6")["xheight"], 0.6)

    def test_width_is_the_face_own_without_the_page_spacing(self):
        # The body sets letter-spacing 0.3em and word-spacing 1em, which the ruler would
        # inherit as px; it drops both.
        # opsz 16 of 8–144 narrows the face's 500 by 40 × 2/130.
        self.near(self.faces(1920)[0]["width"], pangram(500 - 40 * 2 / 130))
        self.near(self.one(1920, size=14)["width"], pangram(450))
        # wght 700 widens by 50 × 300/500.
        self.near(self.one(1920, weight=700)["width"], pangram(530 - 40 * 2 / 130))

    def test_width_and_stem_are_read_at_the_optical_size_in_use(self):
        # At 48 px opsz is 48: 40 × 34/130 narrower, 20 × 34/130 thinner. With
        # font-optical-sizing: none the font's default, 14, is drawn.
        heading = self.one(1920, size=48, optical_sizing="auto")
        self.near(heading["width"], pangram(500 - 40 * 34 / 130))
        self.near(heading["stem"], (100 - 20 * 34 / 130) / 1000)
        held = self.one(1920, size=48, optical_sizing="none")
        self.near(held["width"], pangram(500))
        self.near(held["stem"], 0.1)

    def test_stem_follows_weight_and_grade(self):
        self.near(self.one(1920, size=14)["stem"], 0.06)
        self.near(self.one(1920, weight=700)["stem"], (160 - 20 * 2 / 130) / 1000)
        graded = self.one(1920, variation='"GRAD" 150')
        self.near(graded["stem"], (140 - 20 * 2 / 130) / 1000)
        self.near(graded["width"], self.faces(1920)[0]["width"])

    def test_axes_are_those_the_font_varies_on(self):
        self.assertEqual(self.faces(1920)[0]["axes"], ["wght", "wdth", "opsz", "GRAD"])
        plain = self.one(1920, size=14)
        self.assertEqual((plain["axes"], plain["opsz"]), ([], None))

    def test_opsz_in_use_is_the_size_unless_held_and_the_range_is_read(self):
        self.assertEqual(self.faces(1920)[0]["opsz"], {"in_use": 16, "range": [8, 144]})
        self.assertEqual(
            self.one(1920, size=12)["opsz"], {"in_use": 12, "range": [8, 144]}
        )
        self.assertEqual(
            self.one(1920, size=48, optical_sizing="none")["opsz"]["in_use"], None
        )
        # An explicit "opsz" 200 wins over the size and is clamped to the font's 144.
        pinned = self.one(1920, size=24)
        self.assertEqual(pinned["opsz"], {"in_use": 144, "range": [8, 144]})
        self.near(pinned["width"], pangram(460))

    def test_rendered_names_the_face_drawn_and_x_height_is_the_face_drawn(self):
        self.assertEqual(self.faces(1920)[0]["rendered"][0], "Fixture Flex")
        # "Not Here" never loads, so the first available face, the static one, draws.
        missing = self.one(1920, size=20)
        self.assertEqual(missing["rendered"], ["Fixture Plain"])
        self.near(missing["xheight"], 0.4)

    def test_headings_code_and_controls_are_told_apart_and_text_under_body_size_is_small(
        self,
    ):
        heading = self.one(1920, size=48, optical_sizing="auto")
        self.assertGreater(heading["roles"]["heading"], 0)
        self.assertEqual(heading["roles"]["body"], 0)
        plain = self.one(1920, size=14)
        self.assertEqual(plain["elements"], 2)
        self.assertGreater(plain["roles"]["code"], 0)
        self.assertGreater(plain["roles"]["control"], 0)
        self.assertTrue(plain["small"])
        self.assertTrue(self.one(1920, size=12)["small"])
        self.assertFalse(heading["small"])

    def test_hidden_and_clipped_text_are_not_read(self):
        sizes = {f["size"] for w in (390, 1920) for f in self.faces(w)}
        self.assertFalse(sizes & {30, 34, 36, 40}, sizes)


class Exits(unittest.TestCase):
    def test_a_page_with_no_text_exits_6(self):
        with tempfile.TemporaryDirectory() as out:
            proc = run("none.html", "--out", out, "--widths", "1920")
            self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
            self.assertIn("1920px: no text drawn", proc.stdout)

    def test_a_width_outside_the_sweep_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as out:
            proc = run("faces.html", "--out", out, "--widths", "100")
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            self.assertIn("--widths wants widths from 320 to 2560", proc.stderr)


if __name__ == "__main__":
    child.main()
