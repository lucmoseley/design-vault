import os
import subprocess
import sys
import unittest

import numpy as np

HERE = os.path.dirname(__file__)
SCRIPTS = os.path.join(HERE, "..", "plugin", "skills", "design-project", "scripts")
sys.path.insert(0, SCRIPTS)
import colour_space  # noqa: E402

GREYS = [(v, v, v) for v in (0, 10, 11, 0x76, 0x77, 128, 255)]
PRIMARIES = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]


class ColourSpace(unittest.TestCase):
    def test_de2000_matches_every_published_pair_to_four_places(self):
        # Sharma, Wu & Dalal 2005, Table 1: https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/
        cases = [
            ((50, 2.6772, -79.7751), (50, 0, -82.7485), 2.0425),
            ((50, 0, 0), (50, -1, 2), 2.3669),
            ((50, 2.4900, -0.0010), (50, -2.4900, 0.0011), 7.2195),
            ((50, 2.5, 0), (73, 25, -18), 27.1492),
            ((50, 2.5, 0), (50, 3.1736, 0.5854), 1.0000),
            ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
            ((90.8027, -2.0831, 1.4410), (91.1528, -1.6435, 0.0447), 1.4441),
            ((2.0776, 0.0795, -1.1350), (0.9033, -0.0636, -0.5514), 0.9082),
        ]
        for p, q, want in cases:
            self.assertAlmostEqual(colour_space.de2000(p, q), want, places=4)

    def test_white_is_lab_100_0_0_black_is_lab_0_0_0_and_white_is_oklch_lightness_1_with_no_chroma(
        self,
    ):
        for h, want in (("#FFFFFF", (100, 0, 0)), ("#000000", (0, 0, 0))):
            for got, w in zip(colour_space.lab(h), want, strict=True):
                self.assertAlmostEqual(got, w, places=2)
        lightness, chroma, _ = colour_space.oklch("#FFFFFF")
        self.assertAlmostEqual(lightness, 1, places=4)
        self.assertAlmostEqual(chroma, 0, places=4)

    def test_black_on_white_is_21_to_1(self):
        self.assertAlmostEqual(
            colour_space.contrast("#000000", "#FFFFFF"), 21, places=6
        )

    def test_a_mid_grey_on_white_is_4_54_to_1_and_one_step_lighter_falls_under(self):
        # WCAG's #767676 on white sits just over the 4.5:1 floor: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum
        self.assertAlmostEqual(
            colour_space.contrast("#767676", "#FFFFFF"), 4.54, places=2
        )
        self.assertAlmostEqual(
            colour_space.contrast("#777777", "#FFFFFF"), 4.48, places=2
        )

    def test_oklch_matches_the_published_primaries(self):
        # CSS Color 4 gives these sRGB colours in OKLCH from Ottosson's matrices: https://www.w3.org/TR/css-color-4/#ok-lab
        for h, want in (
            ("#FF0000", (0.62796, 0.25768, 29.2339)),
            ("#00FF00", (0.86644, 0.29483, 142.4953)),
            ("#0000FF", (0.45201, 0.31321, 264.0520)),
        ):
            for got, w in zip(colour_space.oklch(h), want, strict=True):
                self.assertAlmostEqual(got, w, places=3)

    def test_hex_and_rgb_name_the_same_colour(self):
        self.assertEqual(colour_space.oklch("#FF0000"), colour_space.oklch((255, 0, 0)))
        self.assertEqual(
            colour_space.luminance("#767676"), colour_space.luminance((0x76,) * 3)
        )

    def test_a_luminance_the_ratio_away_is_that_ratio_off(self):
        for y in (0.0, 0.2, 0.9):
            self.assertAlmostEqual(
                (colour_space.lighter_by(y, 4.5) + 0.05) / (y + 0.05), 4.5, places=9
            )
            self.assertAlmostEqual(
                (y + 0.05) / (colour_space.darker_by(y, 4.5) + 0.05), 4.5, places=9
            )


class ScalarAndArray(unittest.TestCase):
    def test_lin_gives_one_figure_on_each_side_of_the_knee(self):
        c = np.array([0.0, 0.04, 0.04045, 0.0405, 0.5, 1.0])
        for got, v in zip(colour_space.lin(c), c, strict=True):
            self.assertEqual(got, colour_space.lin(float(v)))

    def test_luminance_and_contrast_give_one_figure_per_colour_in_an_array(self):
        colours = GREYS + PRIMARIES
        many = np.array(colours, dtype=float)
        for got, c in zip(colour_space.luminance(many), colours, strict=True):
            self.assertAlmostEqual(float(got), colour_space.luminance(c), places=12)
        against = (255, 255, 255)
        for got, c in zip(colour_space.contrast(many, against), colours, strict=True):
            self.assertAlmostEqual(
                float(got), colour_space.contrast(c, against), places=12
            )
        for got, c in zip(
            colour_space.contrast(np.array(against), many), colours, strict=True
        ):
            self.assertAlmostEqual(
                float(got), colour_space.contrast(against, c), places=12
            )

    def test_oklch_takes_one_colour_as_an_array(self):
        self.assertEqual(
            colour_space.oklch(np.array([10.0, 200.0, 30.0])),
            colour_space.oklch((10, 200, 30)),
        )


class WithoutNumpy(unittest.TestCase):
    def test_palette_runs_with_numpy_blocked(self):
        script = os.path.join(SCRIPTS, "palette.py")
        proc = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import runpy, sys; sys.modules['numpy'] = None; "
                    "sys.argv = sys.argv[1:]; runpy.run_path(sys.argv[0], run_name='__main__')"
                ),
                script,
                "--logo",
                "grey=#404040",
                "--colour",
                "text=#3F3F3F",
            ],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertNotIn("numpy", proc.stderr)
        self.assertIn("| grey / text |", proc.stdout)


if __name__ == "__main__":
    unittest.main()
