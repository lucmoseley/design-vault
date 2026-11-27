import csv
import json
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
import child  # noqa: E402

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-seams.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "check-seams")
CURVES = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-curves.js"
)
RESEARCH = os.path.join(HERE, "..", "docs", "data", "contact-seams-2026-10-16.csv")
GAP_ROW = "blue-orange-on-white.gap-v.1"
# guess, #341
GAP_TOLERANCE = 0.05
REQUIREMENTS = os.path.realpath(os.path.join(HERE, "..", "plugin", "requirements.txt"))
# guess, #341
RUN_S = 180
# guess, #341
BLOCKED_RUN_S = 60
BLOCKED = (
    "import runpy, sys; sys.modules[sys.argv[1]] = None; sys.argv = sys.argv[2:]; "
    "runpy.run_path(sys.argv[0], run_name='__main__')"
)


def run(page, out):
    return child.run([sys.executable, SCRIPT, page, "--out", out], timeout=RUN_S)


def blocked(argv, env=None):
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
                "covers",
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

    def test_341_a_gap_fails_at_every_scale(self):
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
            self.assertEqual(mattes[ground].shape, (16, 16, 3))
            self.assertEqual(tuple(mattes[ground][8, 0]), (0x1A, 0x4D, 0x8F))
            self.assertEqual(tuple(mattes[ground][8, 15]), (0xE0, 0xA0, 0x30))
        share = (mattes["white"] - mattes["black"]).mean(axis=2) / 255
        self.assertAlmostEqual(share.max(), 0.25, delta=0.01)

    def test_a_translucent_fill_cannot_be_measured(self):
        proc = self.runs["translucent"]
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(
            "NOT MEASURED under.2-over.4 at 0 ms 1x, 0 ms 2x, 0 ms 3x", proc.stdout
        )
        self.assertIn("within 3 CSS px of its crop's centre", proc.stdout)
        self.assertIn("Judge it under vault.contacts-look", proc.stdout)

    def test_585_a_gap_is_measured_through_its_covers_paint_whatever_sets_it(self):
        proc = self.runs["covers"]
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        with open(fixture("covers")) as fh:
            rows = re.findall(r"<!-- row (\d+): (.+?) -->", fh.read())
        self.assertEqual(len(rows), 24)
        opaque = {"0", "21", "22", "23"}
        for row, what in rows:
            name = f"a{row}.2-b{row}.4 (covered)"
            with self.subTest(row=what):
                if row in opaque:
                    self.assertIn(
                        f"pass {name}: width x contrast 0 ms 1x 0″, 0 ms 2x 0″, 0 ms 3x 0″",
                        proc.stdout,
                    )
                else:
                    self.assertIn(
                        f"FAIL {name}: the ground shows along the contact", proc.stdout
                    )
        self.assertIn(
            "or paint its cover opaque. --contact 'a1.2-b1.4=#b1@", proc.stdout
        )
        self.assertNotIn("NOT MEASURED", proc.stdout)

    def test_585_a_covered_contacts_mattes_draw_its_covers_too(self):
        out = os.path.join(self.tmp.name, "covers")
        for ground in ("black", "white"):
            with Image.open(os.path.join(out, f"a0.2-b0.4-0ms-1x-{ground}.png")) as im:
                matte = np.asarray(im.convert("RGB")).astype(int)
            self.assertEqual(tuple(matte[8, 8]), (0, 0xCC, 0), ground)


# #668
TREE_PAGES = (
    ("tbody", "<table><tr><td>{svg}</td></tr></table>"),
    ("p-closed-by-div", "<p>x<div>{svg}</div>"),
    ("sibling-li", "<ul><li>a<li>{svg}</ul>"),
    ("foster-parented", "<table>{svg}</table>"),
)


def matches_in_chromium(page):
    listed = subprocess.run(
        ["node", CURVES, "--contacts", "--json", page],
        capture_output=True,
        text=True,
        timeout=RUN_S,
        check=False,
    )
    contacts = json.loads(listed.stdout)["contacts"]
    selectors = [s for c in contacts for s in (c["lower"], c["upper"], *c["covers"])]
    assert any(c["covers"] for c in contacts), listed.stdout
    from playwright.sync_api import sync_playwright

    with sync_playwright() as play:
        browser = play.chromium.launch()
        try:
            tab = browser.new_page()
            tab.goto("file://" + os.path.abspath(page))
            return [
                tab.eval_on_selector_all(s, "found => found.length") for s in selectors
            ]
        finally:
            browser.close()


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

    def test_585_a_cover_a_stylesheet_thins_or_hides_fails_in_an_svg_file(self):
        shapes = (
            '<path id="a" fill="#c00" d="M10 10 H49 V50 H10 Z"/>'
            '<path id="b" fill="#00c" d="M51 10 H90 V50 H51 Z"/>'
            '<path id="strip" fill="#0c0" d="M46 6 H54 V54 H46 Z"/>'
        )
        for css in ("#strip{opacity:.3}", "#strip{visibility:hidden}"):
            with self.subTest(css=css):
                proc = run(self.page(f"<style>{css}</style>" + shapes), self.tmp.name)
                self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
                self.assertIn("FAIL a.2-b.4 (covered): ", proc.stdout)
        opaque = run(self.page(shapes), self.tmp.name)
        self.assertEqual(opaque.returncode, 0, opaque.stdout + opaque.stderr)
        self.assertIn("pass a.2-b.4 (covered): ", opaque.stdout)

    def test_585_a_cover_whose_selector_names_no_element_is_unmeasured(self):
        path = os.path.join(self.tmp.name, "bare.html")
        with open(path, "w") as fh:
            fh.write(
                '<!doctype html><svg width="100" height="100">'
                '<path id="a" fill="#c00" d="M10 10 H49 V50 H10 Z"/>'
                '<path id="b" fill="#00c" d="M51 10 H90 V50 H51 Z"/>'
                '<g><path fill="#0c0" d="M46 6 H54 V54 H46 Z"/></g></svg>'
                "<script>document.querySelector('g').remove()</script>"
            )
        proc = run(path, self.tmp.name)
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn(
            "has no element :root>body:nth-of-type(1)>svg:nth-of-type(1)>g:nth-of-type(1)>path:nth-of-type(1)"
            " for a cover of contact a.2-b.4",
            proc.stdout + proc.stderr,
        )
        self.assertNotIn("FAIL a.2-b.4", proc.stdout)

    def test_585_a_cover_smil_animates_leaves_the_page_unmeasured_never_passed(self):
        shapes = (
            '<defs><linearGradient id="solid"><stop stop-color="#0c0"/></linearGradient>'
            '<linearGradient id="thin"><stop stop-color="#0c0" stop-opacity=".3"/></linearGradient>'
            '<linearGradient id="moved" href="#solid"><set attributeName="href" to="#thin"/></linearGradient></defs>'
            '<path id="a" fill="#c00" d="M10 10 H49 V50 H10 Z"/>'
            '<path id="b" fill="#00c" d="M51 10 H90 V50 H51 Z"/>'
            '<path id="strip" fill="url(#moved)" d="M46 6 H54 V54 H46 Z"/>'
        )
        proc = run(self.page(shapes), self.tmp.name)
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn("animates SVG with SMIL", proc.stdout + proc.stderr)
        self.assertNotIn("pass a.2-b.4", proc.stdout)

    def test_663_a_no_id_cover_on_a_page_with_no_html_or_body_tag_passes_covered(self):
        path = os.path.join(self.tmp.name, "bare.html")
        with open(path, "w") as fh:
            fh.write(
                "<!doctype html><style>body { margin: 0; background: #fff; }</style>"
                '<svg width="100" height="100">'
                '<path id="a" fill="#c00" d="M10 10 H49 V50 H10 Z"/>'
                '<path id="b" fill="#00c" d="M51 10 H90 V50 H51 Z"/>'
                '<g><path fill="#0c0" d="M46 10 H54 V50 H46 Z"/></g></svg>'
            )
        proc = run(path, self.tmp.name)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("pass a.2-b.4 (covered): ", proc.stdout)

    def test_668_a_no_id_cover_whose_svg_the_html_parser_moves_passes_covered_named_in_chromium(
        self,
    ):
        svg = (
            '<svg width="100" height="100">'
            '<path id="a" fill="#c00" d="M10 10 H49 V50 H10 Z"/>'
            '<path id="b" fill="#00c" d="M51 10 H90 V50 H51 Z"/>'
            '<g><path fill="#0c0" d="M46 10 H54 V50 H46 Z"/></g></svg>'
        )
        for name, body in TREE_PAGES:
            path = os.path.join(self.tmp.name, f"{name}.html")
            with open(path, "w") as fh:
                fh.write(
                    "<!doctype html><style>body { margin: 0; background: #fff; }</style>"
                    + body.format(svg=svg)
                )
            with self.subTest(name):
                proc = run(path, os.path.join(self.tmp.name, name))
                self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                self.assertIn("pass a.2-b.4 (covered): ", proc.stdout)
                self.assertEqual(set(matches_in_chromium(path)), {1}, name)

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

    def test_a_missing_package_exits_3_naming_the_pinned_requirements_256_paired_with_a_closed_contact_passes_at_every_scale(
        self,
    ):
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
