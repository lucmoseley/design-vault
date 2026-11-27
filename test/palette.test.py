import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(__file__)
SCRIPTS = os.path.join(HERE, "..", "plugin", "skills", "design-project", "scripts")
SCRIPT = os.path.join(SCRIPTS, "palette.py")

LOGO = ["--logo", "blue=#0070C0", "--logo", "grey=#404040"]


def run(*args):
    # guess, #175
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def row(out, pair):
    for line in out.splitlines():
        if line.startswith(f"| {pair} |"):
            return [c.strip() for c in line.strip("|").split("|")][1:]
    raise AssertionError(f"no row for {pair} in:\n{out}")


class NearMiss(unittest.TestCase):
    def test_mmm_infra_round_one_greys_fail_as_near_misses_of_the_logo_grey_175(self):
        proc = run(
            *LOGO,
            "--colour",
            "cut=#2a2925",
            "--colour",
            "quiet=#5c5c5c",
            "--colour",
            "panel=#595959",
            "--colour",
            "slate=#223448",
        )
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertEqual(
            row(proc.stdout, "grey / cut"), ["7.9", "10", "near-miss", "neither"]
        )
        self.assertEqual(
            row(proc.stdout, "grey / quiet")[:3], ["9.6", "10", "near-miss"]
        )
        self.assertEqual(
            row(proc.stdout, "grey / panel")[:3], ["8.6", "10", "near-miss"]
        )
        self.assertEqual(
            row(proc.stdout, "blue / slate"), ["23.6", "10", "apart", "large and small"]
        )
        self.assertEqual(
            row(proc.stdout, "grey / slate"), ["11.9", "10", "apart", "large only"]
        )
        self.assertEqual(
            row(proc.stdout, "cut / quiet"), ["17.2", "10", "apart", "large only"]
        )
        self.assertEqual(row(proc.stdout, "blue / grey")[0], "28.4")
        self.assertIn(
            "NEAR-MISS of a fixed colour: grey / cut, ΔE00 7.9: take grey's hex #404040, "
            "or move cut to ΔE00 10 or more from it.",
            proc.stdout,
        )
        for pair in ("grey / quiet", "grey / panel"):
            self.assertIn(f"NEAR-MISS of a fixed colour: {pair},", proc.stdout)
        self.assertNotIn("slate, ΔE00", proc.stdout)

    def test_a_copy_under_one_jnd_of_a_logo_colour_fails_until_it_takes_the_logos_hex(
        self,
    ):
        proc = run(*LOGO, "--colour", "text=#3F3F3F")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertEqual(
            row(proc.stdout, "grey / text")[:3],
            ["0.3", "10", "same colour: take grey's hex"],
        )
        self.assertIn(
            "NEAR-MISS of a fixed colour: grey / text, ΔE00 0.3: take grey's hex #404040,",
            proc.stdout,
        )
        exact = run(*LOGO, "--colour", "text=#404040", "--colour", "slate=#223448")
        self.assertEqual(exact.returncode, 0, exact.stdout + exact.stderr)
        self.assertIn(
            "No palette colour is a near-miss of a fixed colour.", exact.stdout
        )

    def test_two_palette_colours_under_one_jnd_are_the_same_colour_and_a_palette_pair_never_fails(
        self,
    ):
        proc = run(
            "--colour",
            "quiet=#5c5c5c",
            "--colour",
            "panel=#595959",
            "--colour",
            "text=#404040",
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(
            row(proc.stdout, "quiet / panel")[:3], ["1.1", "10", "same colour"]
        )
        self.assertEqual(row(proc.stdout, "quiet / text")[2], "near-miss")
        self.assertIn(
            "No palette colour is a near-miss of a fixed colour.", proc.stdout
        )

    def test_a_fixed_colour_outside_the_logo_is_an_anchor_too(self):
        proc = run("--fixed", "brand=#0070C0", "--colour", "accent=#0A6FBF")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("| brand | #0070C0 | fixed |", proc.stdout)
        self.assertIn("NEAR-MISS of a fixed colour: brand / accent,", proc.stdout)
        self.assertNotIn("## The logo's lightness", proc.stdout)


class SurfaceGreys(unittest.TestCase):
    def test_two_grey_surfaces_take_the_line_at_3_and_one_surface_alone_does_not_178(
        self,
    ):
        args = ["--colour", "page=#FFFFFF", "--colour", "card=#E6E6E6"]
        self.assertEqual(
            row(run(*args).stdout, "page / card")[:3], ["5.2", "10", "near-miss"]
        )
        both = run(*args, "--surface", "page", "--surface", "card")
        self.assertEqual(row(both.stdout, "page / card")[:3], ["5.2", "3", "apart"])
        one = run(*args, "--surface", "page")
        self.assertEqual(row(one.stdout, "page / card")[1], "10")

    def test_a_grey_tinted_within_the_house_range_takes_the_grey_line_and_a_coloured_surface_does_not(
        self,
    ):
        tinted = run(
            "--colour",
            "a=#D6ECFF",
            "--colour",
            "b=#C8E3FC",
            "--surface",
            "a",
            "--surface",
            "b",
        )
        self.assertIn(
            "| b | #C8E3FC | palette | 89.0 | 0.904 0.045 246 | yes, surface |",
            tinted.stdout,
        )
        self.assertEqual(row(tinted.stdout, "a / b")[1], "3")
        coloured = run(
            "--colour",
            "a=#FFE3D1",
            "--colour",
            "b=#FFD2B5",
            "--surface",
            "a",
            "--surface",
            "b",
        )
        self.assertIn(
            "| b | #FFD2B5 | palette | 87.3 | 0.895 0.064 55 | no, surface |",
            coloured.stdout,
        )
        self.assertEqual(row(coloured.stdout, "a / b")[:3], ["6.1", "10", "near-miss"])


class Grounds(unittest.TestCase):
    def test_mmm_infra_full_colour_logo_clears_paper_and_fails_mist_and_slate(self):
        proc = run(
            *LOGO,
            "--ground",
            "paper=#F7F5F0",
            "--ground",
            "mist=#B8C1CB",
            "--ground",
            "slate=#223448",
        )
        out = proc.stdout
        self.assertIn(
            "Lightness band: L* 27.1 to 46.2, unweighted mean 36.6, over 2 logo colour(s).",
            out,
        )
        self.assertIn(
            "on a light ground at L* 79.7 or above, and on a dark ground at no lightness: none is dark enough.",
            out,
        )
        self.assertIn("| paper | #F7F5F0 | 96.6 | 4.73:1 | 9.52:1 | clears 3:1 |", out)
        self.assertIn(
            "| mist | #B8C1CB | 77.7 | 2.83:1 | 5.69:1 | fails: blue under 3:1 |", out
        )
        self.assertIn(
            "| slate | #223448 | 21.1 | 2.47:1 | 1.23:1 | fails: blue, grey under 3:1 |",
            out,
        )

    def test_a_white_logo_has_only_dark_grounds(self):
        out = run("--logo", "white=#FFFFFF").stdout
        self.assertIn("on a light ground at no lightness: none is light enough", out)
        self.assertRegex(out, r"on a dark ground at L\* 6\d\.\d or below\.")


class Usage(unittest.TestCase):
    def test_each_wrong_argument_exits_2_naming_its_fault(self):
        for args, message in (
            ([], "give at least one --logo, --fixed or --colour"),
            (["--colour", "a=0070C0"], "'a=0070C0' is not NAME=#RRGGBB"),
            (["--colour", "a=#0070C"], "'a=#0070C' is not NAME=#RRGGBB"),
            (["--colour", "=#0070C0"], "'=#0070C0' is not NAME=#RRGGBB"),
            (
                ["--colour", "a=#0070C0", "--logo", "a=#404040"],
                "each colour needs its own name",
            ),
            (
                ["--colour", "a=#0070C0", "--surface", "b"],
                "--surface names no --fixed or --colour: b",
            ),
            (
                [
                    "--logo",
                    "grey=#404040",
                    "--colour",
                    "cut=#2a2925",
                    "--surface",
                    "grey",
                    "--surface",
                    "cut",
                ],
                "--surface names a logo colour, which is a mark, never a surface: grey",
            ),
            (
                ["--colour", "a=#0070C0", "--ground", "g=#FFFFFF"],
                "--ground needs a --logo to measure against",
            ),
        ):
            with self.subTest(args=args):
                proc = run(*args)
                self.assertEqual(proc.returncode, 2)
                self.assertIn(message, proc.stderr)


if __name__ == "__main__":
    unittest.main()
