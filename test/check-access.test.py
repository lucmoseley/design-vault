"""Pins check-access.py's access questions (#163, #164, #189, #315, #316, #545): python3 test/check-access.test.py

Each question is run end to end on a fixture that fails it, and on a clean
page that passes every question check-access.py asks; the keyboard-tier01 fixtures plant one fault for each
of #315's questions, and each branch of them besides. access-pixels.py, access-answers.py and
access-boxes.py are libraries, so the pixel maths, the answer merging and the
reading of generated text's boxes check-access.py imports from them are called
in-process. It is a suite of the
commit gate (test/all.sh): loosening a figure here lets a page a visitor
cannot read or use reach the critic as a pass.
"""

import concurrent.futures
import importlib.util
import json
import os
import pathlib
import sys
import tempfile
import unittest

import numpy as np

HERE = os.path.dirname(__file__)
SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-access.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "access")
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

REQUIREMENTS = os.path.realpath(os.path.join(HERE, "..", "plugin", "requirements.txt"))


def library(name):
    spec = importlib.util.spec_from_file_location(
        name[:-3].replace("-", "_"), os.path.join(os.path.dirname(SCRIPT), name)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


maths = library("access-pixels.py")
answering = library("access-answers.py")
boxes = library("access-boxes.py")
contrasts = library("access-contrast.py")
with open(contrasts.TABLE) as table:
    FLOORS = contrasts.parse_table(table.read()).floors

RUNS = (
    "contrast",
    "edge",
    "flush",
    "target",
    "link",
    "keyboard",
    "focus",
    "frames",
    "flicker",
    "motion",
    "loop",
    "clean",
    "dates",
    "unmeasurable",
    "touch",
    "noise",
    "held",
    "dusk",
    "faint",
    "logotype",
    "strokes",
    "growing",
    "covered",
    "trapped",
    "resting",
    "resting-faint",
    "resting-strip",
    "keyboard-tier01-fault",
    "keyboard-tier01-clean",
    "keyboard-tier01-more",
    "keyboard-tier01-skip",
    "keyboard-tier01-spin",
)
PARTS = os.path.join(FIXTURES, "keyboard-tier01-parts.json")
# Arguments a run takes beyond its fixture and --out.
ARGS = {
    "logotype": ["--logotype", "header .brand", "--logotype", "svg.mark"],
    **{
        f"keyboard-tier01-{n}": ["--parts", PARTS]
        for n in ("fault", "clean", "more", "skip", "spin")
    },
}
# #315's questions, each with the id its plant on keyboard-tier01-fault.html carries. The fixtures built before
# #315 are judged on every question but these, as the keyboard-tier01 pages judge them.
KEYS = {
    "vault.skip-link": "#skip-link",
    "vault.visual-order": "#visual-order",
    "vault.scroller-focus": "#scroller-focus",
    "vault.roving-focus": "#roving-focus",
    "vault.menu-focus": "#menu-focus",
    "vault.carousel-focus": "#carousel-focus",
    "vault.ring-outline": "#ring-outline",
    "vault.focus-colour-kept": "#focus-colour-kept",
    "vault.focus-visible": "#focus-visible",
}
# Each run is a browser; four at once keeps the commit gate quick on a shared
# machine. A guess, unmeasured.
PARALLEL = 4
SCRATCH = tempfile.TemporaryDirectory()
DONE = {}


def setUpModule():
    with concurrent.futures.ThreadPoolExecutor(PARALLEL) as pool:
        DONE.update(zip(RUNS, pool.map(check, RUNS), strict=True))


# How long one run of the script may take, in s: a fixture's whole check, or
# one that stops on its arguments or a refused load. Guesses, unmeasured.
RUN_S, ARGUMENT_RUN_S = 600, 120


def script(*args, timeout):
    return child.run([sys.executable, SCRIPT, *args], timeout=timeout)


def check(name):
    out = os.path.join(SCRATCH.name, name)
    r = script(
        os.path.join(FIXTURES, f"{name}.html"),
        "--out",
        out,
        *ARGS.get(name, []),
        timeout=RUN_S,
    )
    found = None
    if os.path.exists(os.path.join(out, "access.json")):
        with open(os.path.join(out, "access.json"), encoding="utf8") as fh:
            found = json.load(fh)
    return r.returncode, r.stdout, r.stderr, found


# Runs argv[2:] as a script once argv[1] is made unimportable.
BLOCKED = (
    "import runpy, sys; sys.modules[sys.argv[1]] = None; sys.argv = sys.argv[2:]; "
    "runpy.run_path(sys.argv[0], run_name='__main__')"
)


def without(package, *args):
    """The script run with `package` unimportable, as on a machine that lacks it (#256)."""
    return child.run(
        [sys.executable, "-c", BLOCKED, package, SCRIPT, *args], timeout=ARGUMENT_RUN_S
    )


def tearDownModule():
    SCRATCH.cleanup()


def solid(rgb, w=40, h=20):
    return np.full((h, w, 3), rgb, dtype=np.uint8)


class Arithmetic(unittest.TestCase):
    def test_contrast_matches_wcags_published_pairs(self):
        self.assertAlmostEqual(
            float(maths.contrast([0, 0, 0], [255, 255, 255])), 21.0, places=3
        )
        self.assertAlmostEqual(
            float(maths.contrast([0x76] * 3, [255] * 3)), 4.54, places=2
        )
        self.assertAlmostEqual(
            float(maths.contrast([0x77] * 3, [255] * 3)), 4.48, places=2
        )

    def text(self, rgb, size=16, weight=400, alpha=1.0):
        return {
            "subject": "p",
            "why": None,
            "color": [*rgb, alpha],
            "size": size,
            "weight": weight,
            "rects": [[0, 0, 40, 20]],
        }

    def read(self, shot, text):
        """text_contrast with a glyph on every pixel."""
        return maths.text_contrast(
            shot, np.ones(shot.shape[:2], dtype=bool), text, FLOORS
        )

    def test_large_text_is_24_px_or_18_66_px_bold(self):
        self.assertTrue(maths.large(24, 400, FLOORS))
        self.assertTrue(maths.large(23.99, 400, FLOORS))
        self.assertFalse(maths.large(23.9, 699, FLOORS))
        self.assertTrue(maths.large(18.66, 700, FLOORS))
        self.assertFalse(maths.large(18.66, 600, FLOORS))
        self.assertFalse(maths.large(18.5, 700, FLOORS))

    def test_large_text_needs_3_to_1_and_body_text_4_5(self):
        grey = [0x94] * 3  # 3.03:1 on white
        fault, _ = self.read(solid(255), self.text(grey))
        self.assertIn("3.03:1 against #ffffff behind it; 4.5:1 needed", fault)
        self.assertEqual(self.read(solid(255), self.text(grey, size=24)), (None, None))
        self.assertEqual(
            self.read(solid(255), self.text(grey, size=19, weight=700)),
            (None, None),
        )
        self.assertIsNotNone(self.read(solid(255), self.text(grey, size=19))[0])

    def test_see_through_text_is_blended_with_what_is_behind_it(self):
        self.assertEqual(self.read(solid(255), self.text([0, 0, 0])), (None, None))
        fault, _ = self.read(solid(255), self.text([0, 0, 0], alpha=0.4))
        self.assertIn("#999999 text", fault)

    def test_text_with_nothing_behind_it_in_the_screenshot_cannot_be_measured(self):
        text = self.text((0, 0, 0)) | {"rects": [[50, 50, 90, 70]]}
        self.assertEqual(
            self.read(solid((255, 255, 255)), text),
            (None, "p lies off the screenshot"),
        )

    def test_one_dark_pixel_behind_a_glyph_fails_its_text_but_one_beside_the_glyphs_does_not(
        self,
    ):
        shot = solid(255)
        shot[5, 10] = 30  # black text on near-black, 1 of a stroke's 48 pixels
        ink = np.zeros((20, 40), dtype=bool)
        ink[4:16, 8:12] = True
        black = self.text([0, 0, 0])
        self.assertIsNotNone(maths.text_contrast(shot, ink, black, FLOORS)[0])
        ink[:] = False
        ink[4:16, 20:24] = True  # the stroke moved off it
        self.assertEqual(maths.text_contrast(shot, ink, black, FLOORS), (None, None))
        ink[:] = False  # no glyph shows: covered or clipped
        self.assertEqual(maths.text_contrast(shot, ink, black, FLOORS), (None, None))

    def test_a_line_in_the_texts_own_colour_across_its_glyphs_is_not_read_but_a_band_is(
        self,
    ):  # #257
        black = self.text([0, 0, 0])
        shot = solid(255)
        shot[9] = shot[12] = 0x60  # its edge, blended into the ground: 3.3:1
        shot[10:12] = 0  # a 2 px underline in the text's own black
        self.assertEqual(self.read(shot, black), (None, None))
        shot[6:14] = 0
        fault, _ = self.read(shot, black)
        self.assertIn("1.00:1 against #000000 behind it", fault)

    def test_a_band_the_texts_box_cuts_to_2_px_is_still_a_band(self):  # #257
        black = self.text([0, 0, 0]) | {"rects": [[0, 10, 40, 30]]}
        shot = solid(255, h=40)
        shot[4:12] = 0
        fault, _ = self.read(shot, black)
        self.assertIn("1.00:1 against #000000 behind it", fault)

    def test_a_1_px_line_in_another_colour_across_the_glyphs_is_read(self):  # #257
        shot = solid(255)
        shot[10] = 0x44
        fault, _ = self.read(shot, self.text([0x11] * 3))
        self.assertIn("1.94:1 against #444444 behind it", fault)

    def test_lines_in_the_texts_own_colour_under_every_glyph_pixel_are_read(
        self,
    ):  # #257
        black = self.text([0, 0, 0])
        shot = solid(0x30)
        shot[::3] = 0  # a close ruling: no ground left beside its lines
        fault, _ = self.read(shot, black)
        self.assertIn("1.00:1 against #000000 behind it", fault)
        shot = solid(0x30)
        shot[::4] = 0  # one row between each two lines' blended edges
        fault, _ = self.read(shot, black)
        self.assertIn("1.59:1 against #303030 behind it", fault)

    def test_a_control_edge_is_its_best_side_line_or_its_fill(self):
        page = solid(255, 100, 60)
        shot = page.copy()
        shot[20, 20:80] = 0x76  # a top border only, 4.54:1
        best = maths.edge_contrast(shot, page, [20, 20, 80, 50]).ratio
        self.assertAlmostEqual(best, 4.54, places=2)
        shot = page.copy()
        shot[24:46, 24:76] = 0x76  # a fill inside a 4 px border the colour of the page
        self.assertAlmostEqual(
            maths.edge_contrast(shot, page, [20, 20, 80, 50])[0], 4.54, places=2
        )
        self.assertAlmostEqual(
            maths.edge_contrast(page, page, [20, 20, 80, 50])[0], 1.0
        )

    def test_a_control_off_the_screenshot_cannot_be_measured(self):
        page = solid(255, 60, 30)
        self.assertIsNone(maths.edge_contrast(page, page, [-90, -40, -30, -10]))
        self.assertIsNone(
            maths.control_edge(
                page, [page], [{"subject": "input", "rect": [-90, -40, -30, -10]}]
            )
        )

    def test_a_neighbours_edge_flush_against_a_control_is_not_its_own(self):  # #220
        page = solid(255, 140, 100)
        page[60:62, 20:120] = 0x22  # a dark rule flush under the field
        shot = page.copy()
        shot[30, 30:110] = shot[59, 30:110] = 0xE7  # the field's own edge, 1.24:1
        shot[30:60, 30] = shot[30:60, 109] = 0xE7
        field = {"subject": "input", "rect": [30, 30, 110, 60]}
        box, ratio, behind = maths.control_edge(shot, [page], [field])
        self.assertIs(box, field)
        self.assertAlmostEqual(ratio, 1.24, places=2)
        self.assertEqual(maths.hexed(behind), "#ffffff")

    def test_controls_whose_edges_meet_are_hidden_in_shots_apart(self):  # #220
        def control(*rect):
            return [{"subject": "input", "rect": list(rect)}]

        flush = [control(0, 0, 48, 36), control(48, 0, 96, 36), control(96, 0, 144, 36)]
        self.assertEqual(maths.hide_groups(flush), [0, 1, 0])
        apart = [control(0, 0, 48, 36), control(0, 41, 48, 77)]
        self.assertEqual(maths.hide_groups(apart), [0, 0])

    def test_a_pixel_that_differs_between_two_shots_of_one_state_has_moved(self):
        shot = solid(255, 40, 20)
        again = shot.copy()
        again[10, 30] = 0
        self.assertTrue(maths.moved(shot, again, [28, 8, 34, 14]))
        self.assertFalse(maths.moved(shot, again, [0, 0, 20, 20]))

    def test_the_innermost_box_that_draws_an_edge_is_the_controls_edge(self):
        page = solid(255, 140, 100)
        shot = page.copy()
        shot[20, 10:130] = 0xE7  # the wrapper's top edge, 1.24:1
        field = {"subject": "input", "rect": [30, 30, 110, 60]}
        wrapper = {"subject": "label", "rect": [10, 20, 130, 70]}
        box, ratio, _ = maths.control_edge(shot, [shot, page], [field, wrapper])
        self.assertIs(box, wrapper)
        self.assertAlmostEqual(ratio, 1.24, places=2)
        without = shot.copy()
        shot[30, 30:110] = 0x76  # the field's own edge, 4.54:1, now drawn
        self.assertIs(
            maths.control_edge(shot, [without, page], [field, wrapper])[0], field
        )

    def test_a_focus_indicator_is_the_pixels_focus_changes_by_3_to_1_or_more(self):
        off = solid(255, 100, 60)
        on = off.copy()
        on[20, 20:80] = 0x76  # a 60 px line, 4.54:1 against white
        on[30, 20:80] = 0xE7  # and one at 1.24:1, which does not count
        still = np.ones((60, 100), dtype=bool)
        self.assertEqual(maths.focus_changed(on, off, [0, 0, 100, 60], still), 60)
        self.assertEqual(maths.focus_changed(on, off, [0, 25, 100, 60], still), 0)
        still[20, 20:50] = False  # a video's or canvas's pixels, moving by themselves
        self.assertEqual(maths.focus_changed(on, off, [0, 0, 100, 60], still), 30)

    def test_a_pixel_within_2_px_of_one_that_moves_by_itself_is_not_still(self):
        shot = solid(255, 9, 9)
        moved = shot.copy()
        moved[4, 4] = 0
        kept = np.ones((9, 9), dtype=bool)
        kept[2:7, 2:7] = False
        self.assertTrue((maths.still_pixels(shot, shot, moved, shot) == kept).all())

    def test_a_canvas_pixel_whose_near_neighbours_match_by_chance_is_not_still(self):
        # The canvas fills columns 4-11; each pair of shots differs on it except
        # in the 3x3 around its edge pixel at row 5, column 4, as noise did in #222.
        on = solid(255, 12, 12)
        on[:, 4:] = 0
        off = solid(255, 12, 12)
        on_again, off_again = off.copy(), on.copy()
        on_again[4:7, 3:6], off_again[4:7, 3:6] = on[4:7, 3:6], off[4:7, 3:6]
        on[5, 1] = on_again[5, 1] = 0  # a ring's pixel, 3 px from the canvas
        still = maths.still_pixels(on, off, on_again, off_again)
        self.assertEqual(maths.focus_changed(on, off, [0, 0, 12, 12], still), 1)

    def test_glyphs_are_the_pixels_black_and_white_text_differ_on(self):
        back, black, white = solid(255), solid(255), solid(255)
        black[5, 10] = 0
        self.assertEqual(int(maths.ink_mask(back, black, white).sum()), 1)
        self.assertTrue(maths.ink_mask(back, black, solid(255, h=21)).all())

    def test_text_whose_page_holds_its_fill_cannot_be_measured(self):
        ink = np.ones((20, 40), dtype=bool)
        self.assertEqual(
            maths.text_contrast(
                solid(255), ink, self.text([0, 0, 0]), FLOORS, held=[[30, 15, 50, 30]]
            ),
            (None, "p holds its own fill, which the check cannot take off"),
        )
        self.assertEqual(
            maths.text_contrast(
                solid(255), ink, self.text([0, 0, 0]), FLOORS, held=[[40, 0, 60, 20]]
            ),
            (None, None),
        )

    def test_a_field_filled_in_tailwinds_gray_50_on_white_draws_its_edge(self):
        page = solid(255, 140, 100)
        shot = page.copy()
        shot[30:60, 30:110] = (0xF9, 0xFA, 0xFB)
        field = {"subject": "input", "rect": [30, 30, 110, 60]}
        box, ratio, _ = maths.control_edge(shot, [page], [field])
        self.assertIs(box, field)
        self.assertAlmostEqual(ratio, 1.045, places=3)

    def test_a_field_that_draws_nothing_on_a_gradient_draws_no_edge(self):
        # White to #e5e5e5 down the page: its fill reads 1.05:1 against the page
        # above it, but nothing against the page behind it.
        column = np.linspace(255, 0xE5, 100).round().astype(np.uint8)
        shot = np.repeat(column[:, None, None], 140 * 3).reshape(100, 140, 3)
        field = {"subject": "input", "rect": [30, 30, 110, 70]}
        self.assertEqual(maths.control_edge(shot, [shot], [field]), (None, None, None))

    def test_a_control_that_draws_no_edge_anywhere_has_none_to_judge(self):
        field = {"subject": "select", "rect": [30, 30, 110, 60]}
        page = solid(255, 140, 100)
        self.assertEqual(maths.control_edge(page, [page], [field]), (None, None, None))


class Answers(unittest.TestCase):
    def judged(self, **faults):
        return {
            qid: answering.Judged(
                faults.get(qid.split(".")[1].replace("-", "_"), []), [], [], []
            )
            for qid, _ in answering.QUESTIONS
        }

    def test_a_fault_at_both_widths_is_one_finding_held_at_both(self):
        f = {"subject": "p.x", "detail": "d"}
        result = answering.answers(
            [
                ("desktop", self.judged(contrast=[f])),
                ("phone", self.judged(contrast=[f])),
            ]
        )
        self.assertEqual(result["vault.contrast"]["answer"], "fail")
        self.assertEqual(
            result["vault.contrast"]["faults"],
            [{"subject": "p.x", "detail": "d", "at": ["desktop", "phone"]}],
        )
        self.assertEqual(
            {r["answer"] for q, r in result.items() if q != "vault.contrast"}, {"pass"}
        )

    def test_a_fault_wins_over_cannot_measure_and_cannot_measure_over_pass(self):
        judged = self.judged(target_size=[{"subject": "b", "detail": "d"}])
        judged["vault.target-size"].unmeasured.append("why")
        judged["vault.contrast"].unmeasured.append("why")
        result = answering.answers([("phone", judged)])
        self.assertEqual(result["vault.target-size"]["answer"], "fail")
        self.assertEqual(result["vault.contrast"]["answer"], "cannot measure")
        self.assertEqual(
            result["vault.contrast"]["unmeasured"], [{"reason": "why", "at": ["phone"]}]
        )

    def test_an_exemption_at_both_widths_is_one_held_at_both_and_fails_nothing(self):
        e = {"subject": "div.brand", "detail": "d"}
        desktop, phone = self.judged(), self.judged()
        desktop["vault.contrast"].exempt.append(e)
        phone["vault.contrast"].exempt.append(e)
        result = answering.answers([("desktop", desktop), ("phone", phone)])
        self.assertEqual(result["vault.contrast"]["answer"], "pass")
        self.assertEqual(
            result["vault.contrast"]["exempt"],
            [{"subject": "div.brand", "detail": "d", "at": ["desktop", "phone"]}],
        )

    def test_two_findings_on_one_subject_at_one_width_join_and_the_first_widths_detail_stands(
        self,
    ):  # #315
        desktop, phone = self.judged(), self.judged()
        desktop["vault.menu-focus"].faults.extend(
            [
                {"subject": "b", "detail": "x"},
                {"subject": "b", "detail": "y"},
                {"subject": "b", "detail": "x"},
            ]
        )
        phone["vault.menu-focus"].faults.extend(
            [{"subject": "b", "detail": "x"}, {"subject": "b", "detail": "z"}]
        )
        result = answering.answers([("desktop", desktop), ("phone", phone)])
        self.assertEqual(
            result["vault.menu-focus"]["faults"],
            [{"subject": "b", "detail": "x; y", "at": ["desktop", "phone"]}],
        )

    def test_a_note_at_both_widths_is_one_held_at_both_and_changes_no_answer(self):
        desktop, phone = self.judged(), self.judged()
        desktop["vault.contrast"].notes.append("n")
        phone["vault.contrast"].notes.append("n")
        result = answering.answers([("desktop", desktop), ("phone", phone)])
        self.assertEqual(result["vault.contrast"]["answer"], "pass")
        self.assertEqual(
            result["vault.contrast"]["notes"],
            [{"note": "n", "at": ["desktop", "phone"]}],
        )


class GeneratedBoxes(unittest.TestCase):
    """access-boxes.py against a stand-in for Chromium's DevTools."""

    def devtools(self, pseudos, quads=(), fails=None):
        def send(method, params):
            if method == fails:
                from playwright.sync_api import Error

                raise Error("No node with given id found")
            if method == "Runtime.evaluate":
                return {
                    "result": {"objectId": "1"} if params["expression"] == "el" else {}
                }
            if method == "DOM.describeNode":
                return {
                    "node": {
                        "pseudoElements": [
                            {"pseudoType": p, "backendNodeId": 7} for p in pseudos
                        ]
                    }
                }
            return {"quads": [list(q) for q in quads]}

        return send

    def test_each_line_of_a_pseudo_element_is_a_box_round_its_quad(self):
        send = self.devtools(
            ["before", "after"],
            [(10, 5, 50, 6, 49, 20, 9, 19), (0, 30, 20, 30, 20, 44, 0, 44)],
        )
        self.assertEqual(
            boxes.generated_boxes(send, [("el", "after")]),
            [[[9, 5, 50, 20], [0, 30, 20, 44]]],
        )

    def test_a_pseudo_element_the_browser_lists_none_of_or_no_quads_for_draws_nothing(
        self,
    ):
        self.assertEqual(
            boxes.generated_boxes(self.devtools(["after"]), [("el", "before")]), [[]]
        )
        self.assertEqual(
            boxes.generated_boxes(self.devtools(["before"]), [("el", "before")]), [[]]
        )

    def test_a_box_devtools_refuses_cannot_be_found(self):
        for method in ("Runtime.evaluate", "DOM.describeNode", "DOM.getContentQuads"):
            send = self.devtools(["before"], [(0, 0, 9, 0, 9, 9, 0, 9)], fails=method)
            self.assertEqual(
                boxes.generated_boxes(send, [("el", "before")]), [None], method
            )

    def test_an_expression_that_names_no_element_cannot_be_found(self):
        send = self.devtools(["before"], [(0, 0, 9, 0, 9, 9, 0, 9)])
        self.assertEqual(boxes.generated_boxes(send, [("nothing", "before")]), [None])


class CarouselWatch(unittest.TestCase):
    """access-keys.py's carousel timing where a loaded machine's screenshots mislead: every shot showing the
    same slide, as a two-slide carousel shot once a cycle, or every shot unlike the last (#315). It runs on
    the real clock, as the fixture's own setInterval turns its slides."""

    def test_a_carousel_is_timed_in_the_page_whatever_its_shots_show(self):
        from playwright.sync_api import sync_playwright

        keys = library("access-keys.py")
        same = np.zeros((4, 4, 3), int)
        shot, keys._shot = keys._shot, lambda handle: same
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                try:
                    page = browser.new_page()
                    page.goto(
                        pathlib.Path(FIXTURES, "keyboard-tier01-spin.html")
                        .resolve()
                        .as_uri()
                    )
                    on, held = (
                        page.query_selector("#spin-on"),
                        page.query_selector("#spin-held"),
                    )
                    self.assertIsNotNone(keys._change(page, on, 2000))
                    held.query_selector("button.pause").focus()
                    page.wait_for_timeout(100)
                    self.assertIsNone(keys._change(page, held, 1500))
                    # Every shot unlike the last, as when one shot outlasts the gap between turns.
                    count = iter(range(10**6))
                    keys._shot = lambda handle: np.full((4, 4, 3), next(count) % 2 * 99)
                    self.assertIsInstance(keys._span(page, on), float)
                finally:
                    browser.close()
        finally:
            keys._shot = shot


class Browsed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright

        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def pause_answer(self, fixture, watch_ms=None, init=None, carousels=()):
        access = library("check-access.py")
        if watch_ms is not None:
            access.WATCH_MS = watch_ms
        context = self.browser.new_context()
        try:
            if init:
                context.add_init_script(init)
            return access.pause_answer(
                context, pathlib.Path(FIXTURES, fixture).resolve().as_uri(), carousels
            )
        finally:
            context.close()


class LateMotionRead(Browsed):
    """check-access.py's vault.pause read where a long animation ends before a control can be tried on it, as on a
    busy machine (#368). Their pair, a long animation still running at the read, is
    Questions.test_a_looping_and_a_long_animation_whose_pause_button_does_not_stop_them_fail."""

    def test_a_long_animation_that_ended_before_the_read_cannot_be_measured(self):
        # A real late read, as only one reproduces the busy machine's: past ended.html's 6 s slides, by #364's
        # 10 s stand-in delay.
        faults, unmeasured = self.pause_answer("ended.html", 10_000)
        self.assertEqual(faults, [])
        ended = "runs 6.0 s from the page's load and ended before a control could be tried on it"
        self.assertEqual(
            unmeasured, [f'div.slide "slide" {ended}', f'p.intro "slide" {ended}']
        )

    def test_a_long_animation_that_ends_while_its_controls_are_tried_cannot_be_measured(
        self,
    ):
        faults, unmeasured = self.pause_answer("ended-tried.html", 1000)
        self.assertEqual(faults, [])
        self.assertEqual(
            unmeasured,
            [
                'div.slide "slide" runs 60.0 s from the page\'s load and ended while the controls named for pausing it were tried'
            ],
        )


class Hold(unittest.TestCase):
    """How long vault.pause waits for a change a control may have stopped (#545): a declared carousel's
    slide span as vault.carousel-focus timed it, else access-keys.py's ROTATE_MS, and STILL_SLACK_MS more."""

    def test_a_declared_carousel_holds_for_its_timed_span_and_anything_else_for_rotate_ms(
        self,
    ):
        access = library("check-access.py")
        slack, rotate = access.keys.STILL_SLACK_MS, access.keys.ROTATE_MS
        spans = [3000.0, "never holds still", None]
        for rotation, want in (
            ({"declared": True, "index": 0}, 3000 + slack),
            ({"declared": True, "index": 1}, rotate + slack),
            ({"declared": True, "index": 2}, rotate + slack),
            ({"declared": True, "index": 3}, rotate + slack),
            ({"declared": False, "index": -1}, rotate + slack),
        ):
            with self.subTest(rotation):
                self.assertEqual(access.hold_ms(rotation, spans), want)


class TimedChange(Browsed):
    """vault.pause on a page that changes what it shows on a timer past 5 s, as a carousel's slides do, told
    apart from an entrance that ends sooner (#545)."""

    LATER = "main > div.slides changes what it shows more than 5 s after the page's load, and no control on the page is named for pausing, stopping or hiding it"

    def test_a_declared_carousel_with_no_pause_control_fails(self):
        self.assertEqual(
            self.pause_answer("carousel.html", carousels=[".slides"]),
            (
                [
                    {
                        "subject": "main > div.slides",
                        "detail": self.LATER.removeprefix("main > div.slides "),
                    }
                ],
                [],
            ),
        )

    def test_an_undeclared_carousel_with_no_pause_control_cannot_be_measured(self):
        self.assertEqual(
            self.pause_answer("carousel.html"),
            (
                [],
                [
                    f"{self.LATER}; no carousel was declared, so whether the change shows cannot be told"
                ],
            ),
        )

    def test_a_carousel_a_pause_button_stops_passes_declared_or_not(self):
        for carousels in ([".slides"], []):
            with self.subTest(carousels=carousels):
                self.assertEqual(
                    self.pause_answer("carousel-paused.html", carousels=carousels),
                    ([], []),
                )

    def test_an_entrance_that_ends_within_5_s_beside_a_running_interval_passes(self):
        self.assertEqual(self.pause_answer("entrance.html"), ([], []))


class PauseClick(Browsed):
    """Whether vault.pause's click on a control named for pausing lands, read the same on a busy machine (#536)."""

    def test_a_clean_page_passes_when_every_actionability_wait_outruns_its_budget(self):
        from playwright.sync_api import ElementHandle, TimeoutError

        click = ElementHandle.click

        def actionability_wait_times_out(handle, *args, force=False, **kwargs):
            if not force:
                raise TimeoutError("stand-in: the actionability wait outran its budget")
            return click(handle, *args, force=force, **kwargs)

        ElementHandle.click = actionability_wait_times_out
        try:
            self.assertEqual(self.pause_answer("clean.html"), ([], []))
        finally:
            ElementHandle.click = click

    def test_a_clean_page_passes_when_each_frame_comes_late(self):
        late_frames = """
        const frame = window.requestAnimationFrame.bind(window);
        window.requestAnimationFrame = (step) => frame(() => setTimeout(() => frame(step), 300));
        """
        self.assertEqual(self.pause_answer("clean.html", init=late_frames), ([], []))

    def test_a_control_that_shifts_once_as_it_is_scrolled_to_is_clicked(self):
        self.assertEqual(self.pause_answer("settling.html"), ([], []))

    def test_a_covered_control_a_moving_one_and_one_disabled_once_scrolled_to_cannot_be_clicked(
        self,
    ):
        faults, unmeasured = self.pause_answer("unclickable.html")
        self.assertEqual(unmeasured, [])
        tried = "none of the 3 control(s) named for pausing it stops it, clicked (3 could not be clicked)"
        self.assertEqual(
            faults,
            [
                {
                    "subject": "div.spin:nth-of-type(1)",
                    "detail": f'"spin" loops forever from the page\'s load, and {tried}',
                },
                {
                    "subject": "button.drift",
                    "detail": f'"drift" loops forever from the page\'s load, and {tried}',
                },
            ],
        )


class Questions(unittest.TestCase):
    def only_fault(self, name, qid, also=()):
        """The run's findings under qid, once it exited 1 with every question but qid and `also` passing."""
        code, stdout, stderr, found = DONE[name]
        self.assertEqual(code, 1, stdout + stderr)
        answers = found["answers"]
        self.assertEqual(
            {
                q: a["answer"]
                for q, a in answers.items()
                if a["answer"] != "pass" and q not in KEYS
            },
            {q: "fail" for q in (qid, *also)},
        )
        for f in answers[qid]["faults"]:
            self.assertEqual(f["at"], ["desktop", "phone"])
            self.assertIn(f"desktop, phone: {f['subject']} {f['detail']}", stdout)
        return [(f["subject"], f["detail"]) for f in answers[qid]["faults"]]

    def test_grey_body_text_and_a_grey_generated_label_fail_and_large_or_bold_text_at_3_to_1_passes(
        self,
    ):
        found = self.only_fault("contrast", "vault.contrast")
        self.assertEqual(
            [s for s, _ in found],
            [
                "p.faint:nth-of-type(2)",
                "input#q placeholder",
                "p.new:nth-of-type(5)::before",
            ],
        )
        for _, detail in found:
            self.assertIn(
                "2.32:1 against #ffffff behind it; 4.5:1 needed (#aaaaaa text, 16 px)",
                detail,
            )

    def test_a_field_edged_at_1_24_to_1_fails_and_so_do_one_in_a_box_and_an_aria_checkbox_edged_so(
        self,
    ):
        [own, boxed, aria] = self.only_fault("edge", "vault.control-edges")
        self.assertEqual(
            own,
            (
                "input#name",
                "shows its edge at 1.24:1 at best against #ffffff behind that; 3:1 needed",
            ),
        )
        self.assertEqual(boxed[0], "input#find")
        self.assertIn(
            "shows the edge of label.box:nth-of-type(2) around it at 1.24:1", boxed[1]
        )
        self.assertEqual(aria[0], "span#news")
        self.assertIn("shows its edge at 1.24:1", aria[1])

    def test_near_white_fields_flush_on_a_dark_rule_or_block_fail_on_their_own_edge(
        self,
    ):  # #220
        self.assertEqual(
            self.only_fault("flush", "vault.control-edges", ("vault.focus",)),
            [
                (
                    f"input#{name}",
                    "shows its edge at 1.24:1 at best against #ffffff behind that; 3:1 needed",
                )
                for name in ("rule", "block", "light")
            ],
        )
        [ring] = self.only_fault("flush", "vault.focus", ("vault.control-edges",))
        self.assertEqual(ring[0], "input#edged")

    def test_two_20_px_targets_whose_circles_cross_both_fail_and_so_do_links_above_a_paragraph_and_restyled_native_controls(
        self,
    ):
        found = self.only_fault("target", "vault.target-size")
        self.assertEqual(
            [s.split(" > ")[1].split(":")[0] for s, _ in found],
            [
                "button.bold",
                "button.italic",
                "a.in",
                "a.out",
                "select.sort",
                "button.go",
                "input.day",
                "input.one",
            ],
        )
        self.assertTrue(
            all(
                d.startswith("is 20x20 px, and a 24 px circle on it reaches")
                for _, d in found[:2]
            )
        )

    def test_targets_grown_for_a_coarse_pointer_fail_at_desktop_width_only(self):
        code, stdout, stderr, found = DONE["touch"]
        self.assertEqual(code, 1, stdout + stderr)
        answers = found["answers"]
        self.assertEqual(
            {
                q: a["answer"]
                for q, a in answers.items()
                if a["answer"] != "pass" and q not in KEYS
            },
            {"vault.target-size": "fail"},
        )
        self.assertEqual(
            [
                (f["subject"].split(" > ")[1], f["at"])
                for f in answers["vault.target-size"]["faults"]
            ],
            [
                ("button.bold:nth-of-type(1)", ["desktop"]),
                ("button.italic:nth-of-type(2)", ["desktop"]),
            ],
        )
        self.assertTrue(
            answers["vault.target-size"]["faults"][0]["detail"].startswith(
                "is 20x20 px, and a 24 px circle on it reaches"
            )
        )

    def test_a_link_told_by_colour_alone_fails_below_3_to_1_and_passes_at_it_with_no_cue_on_hover_or_focus(
        self,
    ):
        [bare, samebg, clear] = self.only_fault(
            "link", "vault.colour-script", also=("vault.focus",)
        )
        self.assertEqual(
            bare,
            (
                "p:nth-of-type(1) > a.bare",
                "is told from the text around it by colour alone, at 2.44:1; 3:1 or an underline is needed",
            ),
        )
        self.assertEqual(samebg[0], "p:nth-of-type(2) > a.samebg")
        self.assertEqual(clear[0], "p:nth-of-type(3) > a.clear")

    def test_two_links_whose_outline_is_taken_off_show_no_focus(self):
        self.only_fault("link", "vault.colour-script", also=("vault.focus",))
        self.assertEqual(
            [f["subject"] for f in DONE["link"][3]["answers"]["vault.focus"]["faults"]],
            [
                "p:nth-of-type(3) > a.clear",
                "p.grey:nth-of-type(4) > a.nofocus:nth-of-type(2)",
            ],
        )

    def test_a_div_button_a_span_and_a_react_div_acting_on_a_click_and_a_link_out_of_the_tab_order_fail(
        self,
    ):
        found = self.only_fault("keyboard", "vault.keyboard")
        self.assertEqual(
            found,
            [
                (
                    "div.fake.book:nth-of-type(1)",
                    "acts on a click, and the Tab key never reaches it",
                ),
                ("span.fake.menu", "acts on a click, and the Tab key never reaches it"),
                (
                    "div.fake.save:nth-of-type(2)",
                    "acts on a click, and the Tab key never reaches it",
                ),
                ("p:nth-of-type(2) > a", "is a link, and the Tab key never reaches it"),
            ],
        )

    def test_buttons_with_no_outline_or_whose_fill_hides_the_ring_show_no_focus_and_ones_shut_away_or_under_a_fixed_bar_and_header_cannot_be_seen(
        self,
    ):
        [plain, shut, dark, under, hours] = self.only_fault("focus", "vault.focus")
        self.assertEqual(plain[0], "button.plain:nth-of-type(1)")
        self.assertIn(
            "shows no focus indicator: 0 px around it change by 3:1 or more", plain[1]
        )
        self.assertEqual(
            shut,
            (
                "div.shut:nth-of-type(1) > button",
                "takes focus outside the window or its clipping box, where its focus cannot be seen",
            ),
        )
        # #424
        self.assertEqual(
            dark,
            (
                "button.dark:nth-of-type(2)",
                "shows no focus indicator: 12 px around it change by 3:1 or more when it takes focus, "
                "and a 1 px line along its longer side is 115 px",
            ),
        )
        self.assertEqual(
            under,
            (
                "a.under:nth-of-type(2)",
                "is hidden under div.bar:nth-of-type(2) when Tab brings focus to it",
            ),
        )
        self.assertEqual(
            hours,
            (
                "a.hours:nth-of-type(3)",
                "is hidden under header when Shift+Tab brings focus to it",
            ),
        )

    def test_focus_is_walked_inside_the_pages_own_frame_and_judged_at_another_sites(
        self,
    ):  # #199
        self.assertEqual(
            self.only_fault("frames", "vault.focus"),
            [
                (
                    "a.bare:nth-of-type(2) in div.slot:nth-of-type(1) > iframe.booking",
                    "shows no focus indicator: 0 px around it change by 3:1 or more when it takes focus, "
                    "and a 1 px line along its longer side is 42 px",
                ),
                (
                    "a.low:nth-of-type(3) in div.slot:nth-of-type(1) > iframe.booking",
                    "is hidden under div.slot:nth-of-type(1) > div.lid when Tab brings focus to it",
                ),
                (
                    "a in iframe.rooms:nth-of-type(1)",
                    "is hidden under div.bar when Tab brings focus to it",
                ),
                (
                    "a.tall:nth-of-type(1) in div.cut:nth-of-type(2) > iframe.menu",
                    "shows no focus indicator: 0 px around it change by 3:1 or more when it takes focus, "
                    "and a 1 px line along its longer side is 60 px",
                ),
                (
                    "a.far:nth-of-type(2) in div.cut:nth-of-type(2) > iframe.menu",
                    "takes focus outside the window or its clipping box, where its focus cannot be seen",
                ),
                (
                    "div.slot.shut:nth-of-type(3) > iframe.kiosk",
                    "is hidden under div.slot.shut:nth-of-type(3) > div.lid when Tab brings focus to it",
                ),
                (
                    "a.bare:nth-of-type(2)",
                    "shows no focus indicator: 0 px around it change by 3:1 or more when it takes focus, "
                    "and a 1 px line along its longer side is 55 px",
                ),
            ],
        )
        focus = DONE["frames"][3]["answers"]["vault.focus"]
        self.assertEqual(focus["unmeasured"], [])
        judged = "was judged at the frame alone: whether it shows and what lies over it, not the indicator that page draws"
        self.assertEqual(
            focus["notes"],
            [
                {
                    "note": f"focus inside {frame}, whose page this one cannot read, {judged}",
                    "at": ["desktop", "phone"],
                }
                for frame in (
                    "iframe.map:nth-of-type(2)",
                    "div.slot.shut:nth-of-type(3) > iframe.kiosk",
                )
            ],
        )

    def test_a_looping_and_a_long_animation_whose_pause_button_does_not_stop_them_fail(
        self,
    ):
        found = self.only_fault("motion", "vault.pause")
        tried = "from the page's load, and none of the 1 control(s) named for pausing it stops it, clicked"
        self.assertEqual(
            found,
            [
                ("svg.spin", f'"spin" loops forever {tried}'),
                ("div.slide", f'"slide" runs 60.0 s {tried}'),
            ],
        )
        self.assertEqual(DONE["motion"][3]["answers"]["vault.pause"]["unmeasured"], [])

    def test_a_button_beside_a_flickering_canvas_shows_no_focus(self):
        code, stdout, stderr, found = DONE["flicker"]
        self.assertEqual(code, 1, stdout + stderr)
        answers = found["answers"]
        self.assertEqual(
            {
                q: a["answer"]
                for q, a in answers.items()
                if a["answer"] != "pass" and q not in KEYS
            },
            {
                "vault.focus": "fail",
                "vault.pause": "cannot measure",
                "vault.control-edges": "cannot measure",
                "vault.chart-contrast": "cannot measure",  # an undeclared canvas (#429)
            },
        )
        self.assertEqual(
            answers["vault.control-edges"]["unmeasured"],
            [
                {
                    "reason": "input.below lies on or beside something that moves by itself, so what is behind it cannot be read",
                    "at": ["desktop", "phone"],
                }
            ],
        )
        [fault] = answers["vault.focus"]["faults"]
        self.assertEqual(fault["subject"], "section.hero > button.cta")
        self.assertIn(
            "indicator: 0 px around it change by 3:1 or more", fault["detail"]
        )

    def test_a_loop_with_no_control_on_the_page_fails(self):
        self.assertEqual(
            self.only_fault("loop", "vault.pause"),
            [
                (
                    "div.pulse",
                    '"pulse" loops forever from the page\'s load, and no control on the page is named for pausing, stopping or hiding it',
                )
            ],
        )

    def test_skip_links_hidden_at_rest_off_the_page_or_clipped_pass_every_question(
        self,
    ):  # #421
        _, stdout, stderr, found = DONE["resting"]
        self.assertEqual(
            {a["answer"] for q, a in found["answers"].items() if q not in KEYS},
            {"pass"},
            stdout + stderr,
        )

    def test_skip_links_hidden_at_rest_are_read_for_contrast_as_they_show_focused(
        self,
    ):  # #421
        self.assertEqual(
            [s for s, _ in self.only_fault("resting-faint", "vault.contrast")],
            ["a.clip:nth-of-type(1)", "a.away:nth-of-type(2)"],
        )
        self.assertEqual(
            [
                u["reason"]
                for u in DONE["resting-faint"][3]["answers"]["vault.contrast"][
                    "unmeasured"
                ]
            ],
            [
                "a.away:nth-of-type(2)::after is generated text in a Tab stop hidden at rest, which is read only "
                "focused, and generated text is not read there"
            ],
        )

    def test_links_off_the_page_in_a_scrolling_strip_are_still_measured_for_target_size(
        self,
    ):  # #421
        self.assertEqual(
            [s for s, _ in self.only_fault("resting-strip", "vault.target-size")],
            [
                "main > div.strip > a.tiny:nth-of-type(2)",
                "main > div.strip > a.tiny:nth-of-type(3)",
            ],
        )

    def faults(self, name, qid):
        """{subject: detail} of the run's faults under qid."""
        return {
            f["subject"]: f["detail"] for f in DONE[name][3]["answers"][qid]["faults"]
        }

    def test_the_keyboard_fault_page_names_one_plant_for_each_of_315s_questions(self):
        code, stdout, stderr, found = DONE["keyboard-tier01-fault"]
        self.assertEqual(code, 1, stdout + stderr)
        failing = {q for q, a in found["answers"].items() if a["answer"] != "pass"}
        self.assertEqual(failing, set(KEYS))
        for qid, mark in KEYS.items():
            with self.subTest(qid):
                faults = found["answers"][qid]["faults"]
                self.assertEqual(len(faults), 1, faults)
                self.assertIn(mark, faults[0]["subject"])
                at = (
                    ["desktop"]
                    if qid == "vault.focus-visible"
                    else ["desktop", "phone"]
                )
                self.assertEqual(faults[0]["at"], at)

    def test_the_keyboard_fault_pages_findings_say_what_is_wrong(self):
        details = {
            q: next(iter(self.faults("keyboard-tier01-fault", q).values()))
            for q in KEYS
        }
        for qid, said in (
            ("vault.skip-link", "links to #rooms, which is not the main content"),
            ("vault.visual-order", "follows it in the source, moved by order"),
            ("vault.scroller-focus", 'no tabindex="0", no role="region", no name'),
            ("vault.roving-focus", "takes 2 Tab stops"),
            (
                "vault.roving-focus",
                "keeps focus on div#roving-focus > button:nth-of-type(1) when ArrowRight is pressed",
            ),
            (
                "vault.menu-focus",
                "opening it by Enter leaves focus on button#menu-focus, not its first item",
            ),
            ("vault.menu-focus", "Tab leaves it open"),
            (
                "vault.carousel-focus",
                "lets the Tab key land on div.slide:nth-of-type(2) > p > a",
            ),
            (
                "vault.carousel-focus",
                "in the accessibility tree, with no inert or aria-hidden",
            ),
            ("vault.ring-outline", "by its box-shadow alone"),
            (
                "vault.focus-colour-kept",
                "draws its text in #b3261e, the colour focus rings are drawn in",
            ),
            ("vault.focus-visible", "set on :focus, not :focus-visible"),
        ):
            with self.subTest(qid, said=said):
                self.assertIn(said, details[qid])

    def test_the_keyboard_clean_page_passes_every_question(self):
        code, stdout, stderr, found = DONE["keyboard-tier01-clean"]
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual({a["answer"] for a in found["answers"].values()}, {"pass"})

    def test_each_further_branch_of_315s_questions_is_named(self):
        for name, qid, subject, said in (
            (
                "more",
                "vault.skip-link",
                "a#skip-elsewhere",
                "links to #nowhere, which is not the main content",
            ),
            (
                "more",
                "vault.visual-order",
                "div#grid-order > a:nth-of-type(2)",
                "moved by grid placement on div#grid-order",
            ),
            (
                "more",
                "vault.roving-focus",
                "div#roving-arrows",
                "keeps focus on div#roving-arrows > button:nth-of-type(1) when ArrowRight is pressed",
            ),
            (
                "more",
                "vault.roving-focus",
                "div#roving-entry",
                "not its selected item div#roving-entry > span:nth-of-type(2)",
            ),
            (
                "more",
                "vault.menu-focus",
                'button#menu-escape "Actions"',
                "Escape leaves focus on the page, not the button that opened it",
            ),
            (
                "more",
                "vault.menu-focus",
                'button#menu-escape "Actions"',
                "Tab leaves it open",
            ),
            (
                "more",
                "vault.menu-focus",
                'button#menu-escape "Actions"',
                "opening it by Up Arrow leaves focus on ul#actions > li:nth-of-type(1), not its last item",
            ),
            ("more", "vault.ring-outline", "a#ring-border", "by its border alone"),
            (
                "more",
                "vault.focus-colour-kept",
                "a#ring-second",
                "draws its focus ring in #1f6feb, a second focus colour beside #b3261e",
            ),
            (
                "more",
                "vault.focus-visible",
                "button#ring-removed",
                "takes the browser's focus ring off",
            ),
            (
                "more",
                "vault.focus-visible",
                "input#field-plain",
                "shows no focus when clicked into",
            ),
            (
                "skip",
                "vault.skip-link",
                "a#skip-hidden",
                "is not shown whole in the window when it takes focus",
            ),
            ("skip", "vault.visual-order", "a#skip-hidden", 'has tabindex="1"'),
            (
                "spin",
                "vault.carousel-focus",
                "div#spin-on",
                "puts div#spin-on > button.next:nth-of-type(1) before its rotation control",
            ),
            (
                "spin",
                "vault.carousel-focus",
                "div#spin-on",
                "keeps rotating while focus is inside it",
            ),
            (
                "spin",
                "vault.carousel-focus",
                "div#spin-on",
                "keeps rotating while the pointer is over it",
            ),
            (
                "spin",
                "vault.carousel-focus",
                "div#spin-on",
                "moves focus from div#spin-on > button.next:nth-of-type(1) to",
            ),
        ):
            with self.subTest(name, qid=qid, said=said):
                faults = self.faults(f"keyboard-tier01-{name}", qid)
                self.assertIn(subject, faults)
                self.assertIn(said, faults[subject])

    def test_a_carousel_that_holds_still_for_focus_and_the_pointer_passes_beside_one_that_does_not(
        self,
    ):
        self.assertEqual(
            list(self.faults("keyboard-tier01-spin", "vault.carousel-focus")),
            ["div#spin-on"],
        )
        self.assertEqual(
            {
                q
                for q, a in DONE["keyboard-tier01-spin"][3]["answers"].items()
                if a["answer"] != "pass"
            },
            {"vault.carousel-focus"},
        )

    def test_a_clean_page_passes_every_question(self):
        code, stdout, stderr, found = DONE["clean"]
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual({a["answer"] for a in found["answers"].values()}, {"pass"})
        self.assertEqual(list(found["answers"]), [q for q, _ in answering.QUESTIONS])
        self.assertEqual(
            found["viewports"], {"desktop": [1920, 633], "phone": [390, 664]}
        )

    def test_text_and_fields_that_draw_nothing_pass_on_flat_gradient_grain_and_photo_grounds(
        self,
    ):
        code, stdout, stderr, _ = DONE["noise"]
        self.assertEqual(code, 0, stdout + stderr)

    def test_text_an_endless_loop_darkens_the_ground_of_passes_read_without_it_and_fails_on_that_ground_held_still(
        self,
    ):  # #252
        code, stdout, stderr, _ = DONE["held"]
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual(
            [
                s
                for s, _ in self.only_fault(
                    "dusk", "vault.contrast", also=("vault.fill-text",)
                )
            ],
            ["p#dusk"],
        )

    def test_a_patch_behind_a_few_letters_fails_and_so_do_fields_filled_in_faint_greys(
        self,
    ):
        found = self.only_fault("faint", "vault.contrast", ("vault.control-edges",))
        self.assertEqual(
            found,
            [
                (
                    s,
                    "is 1.94:1 against #444444 behind it; 4.5:1 needed (#111111 text, 16 px)",
                )
                for s in ("span#short", "span#line", "span#para", "span#one")
            ],
        )
        self.assertEqual(
            DONE["faint"][3]["answers"]["vault.contrast"]["unmeasured"],
            [
                {
                    "reason": f"span#kept{after} holds its own fill, which the check cannot take off",
                    "at": ["desktop", "phone"],
                }
                for after in ("", "::after")
            ],
        )
        edges = DONE["faint"][3]["answers"]["vault.control-edges"]["faults"]
        self.assertEqual(
            [(f["subject"], f["detail"][:30]) for f in edges],
            [
                ("input#gray50", "shows its edge at 1.05:1 at be"),
                ("input#radix", "shows its edge at 1.03:1 at be"),
            ],
        )

    def test_text_over_lines_in_its_own_colour_passes_on_a_page_the_first_shot_grows_and_a_band_of_it_or_a_rule_in_another_colour_fails(
        self,
    ):  # #257
        found = self.only_fault("strokes", "vault.contrast")
        self.assertEqual(
            found,
            [
                (
                    "p#band > span",
                    "is 1.00:1 against #1b2a6b behind it; 4.5:1 needed (#1b2a6b text, 16 px)",
                ),
                (
                    "p#other",
                    "is 2.03:1 against #4a5a9b behind it; 4.5:1 needed (#1b2a6b text, 16 px)",
                ),
            ],
        )

    def test_a_page_that_grows_on_every_shot_passes_with_a_note_at_each_width_that_whole_boxes_were_read(
        self,
    ):  # #290
        code, stdout, stderr, found = DONE["growing"]
        self.assertEqual(code, 0, stdout + stderr)
        notes = found["answers"]["vault.contrast"]["notes"]
        self.assertEqual([n["at"] for n in notes], [["desktop"], ["phone"]])
        for n in notes:
            self.assertIn("each text's whole box was read", n["note"])
            self.assertIn(f"  note, {n['at'][0]}: {n['note']}", stdout)
        # strokes.html grows on its first shot only, so its retake matches.
        self.assertEqual(DONE["strokes"][3]["answers"]["vault.contrast"]["notes"], [])

    def test_text_under_a_fixed_or_sticky_bar_at_load_is_read_clear_of_it_where_pale_text_still_fails(
        self,
    ):  # #200
        self.assertEqual(
            self.only_fault("covered", "vault.contrast", also=("vault.fill-text",)),
            [
                (
                    "header > a.rates",
                    "is 1.68:1 against #0a3542 behind it; 4.5:1 needed (#2c5866 text, 16 px)",
                ),
                (
                    "main > p.quiet:nth-of-type(3)",
                    "is 1.67:1 against #ffffff behind it; 4.5:1 needed (#c8c8c8 text, 16 px)",
                ),
                (
                    "div.bar:nth-of-type(6) > span.desk:nth-of-type(2)",
                    "is 1.68:1 against #0a3542 behind it; 4.5:1 needed (#2c5866 text, 16 px)",
                ),
                (
                    "main > p.quiet:nth-of-type(3)::after",
                    "is 1.67:1 against #ffffff behind it; 4.5:1 needed (#c8c8c8 text, 16 px)",
                ),
            ],
        )
        self.assertEqual(
            [
                n["note"]
                for n in DONE["covered"][3]["answers"]["vault.contrast"]["notes"]
            ],
            [
                "main > p.welcome:nth-of-type(1) lay under div.chat:nth-of-type(2) at load, so was read with it hidden, "
                "as a visitor scrolls clear of it",
                "main > p.breakfast:nth-of-type(2), main > p.quiet:nth-of-type(3), main > p.quiet:nth-of-type(3)::after "
                "lay under div.bar:nth-of-type(6) at load, so were read with it hidden, as a visitor scrolls clear of it",
            ],
        )

    def test_text_a_bar_covers_that_no_scroll_takes_clear_is_read_as_drawn_under_it_unnoted(
        self,
    ):  # #345
        code, stdout, stderr, found = DONE["trapped"]
        self.assertEqual(code, 0, stdout + stderr)
        contrast = found["answers"]["vault.contrast"]
        self.assertEqual(
            (contrast["answer"], contrast["notes"], contrast["unmeasured"]),
            ("pass", [], []),
        )

    def test_a_logotype_named_by_its_selector_is_exempt_and_reported_and_other_grey_text_still_fails(
        self,
    ):
        found = self.only_fault("logotype", "vault.contrast")
        self.assertEqual(
            found,
            [
                (
                    "p.faint",
                    "is 2.32:1 against #ffffff behind it; 4.5:1 needed (#aaaaaa text, 16 px)",
                )
            ],
        )
        contrast = DONE["logotype"][3]["answers"]["vault.contrast"]
        self.assertEqual(contrast["unmeasured"], [])
        faint = (
            "is 1.61:1 against #ffffff behind it; 4.5:1 needed (#cccccc text, 20 px)"
        )
        self.assertEqual(
            [(e["subject"], e["detail"], e["at"]) for e in contrast["exempt"]],
            [
                (
                    "header > div.brand",
                    f"is exempt as a logotype by --logotype 'header .brand', and {faint}",
                    ["desktop", "phone"],
                ),
                (
                    "svg.mark > text",
                    "is exempt as a logotype by --logotype 'svg.mark', and is SVG text",
                    ["desktop", "phone"],
                ),
                (
                    "header > div.brand::after",
                    f"is exempt as a logotype by --logotype 'header .brand', and {faint}",
                    ["desktop", "phone"],
                ),
            ],
        )
        self.assertIn(
            f"exempt, desktop, phone: header > div.brand is exempt as a logotype by --logotype 'header .brand', and {faint}",
            DONE["logotype"][1],
        )

    def test_eight_datetime_inputs_whose_parts_each_take_a_tab_are_walked_to_the_end(
        self,
    ):
        code, stdout, stderr, found = DONE["dates"]
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual({a["answer"] for a in found["answers"].values()}, {"pass"})

    def test_gradient_text_and_text_over_a_canvas_cannot_be_measured_and_exit_6(
        self,
    ):
        code, stdout, stderr, found = DONE["unmeasurable"]
        self.assertEqual(code, 6, stdout + stderr)
        answers = found["answers"]
        self.assertEqual(answers["vault.contrast"]["answer"], "cannot measure")
        self.assertEqual(
            [u["reason"] for u in answers["vault.contrast"]["unmeasured"]],
            [
                "h1.shine is filled with a background",
                "div.stage > p.over lies over a video or canvas",
            ],
        )
        self.assertEqual(answers["vault.pause"]["answer"], "cannot measure")
        self.assertEqual(
            [u["reason"] for u in answers["vault.pause"]["unmeasured"]],
            [
                "span.drift is moved frame by frame by a script, which this check cannot time",
                "div.stage > canvas changes as it is drawn, which this check cannot time",
            ],
        )
        self.assertIn(
            "vault.contrast, text contrast (WCAG 1.4.3): CANNOT MEASURE", stdout
        )


class Arguments(unittest.TestCase):
    def test_a_missing_file_exits_2(self):
        with tempfile.TemporaryDirectory() as out:
            r = script(
                os.path.join(FIXTURES, "nowhere.html"),
                "--out",
                out,
                timeout=ARGUMENT_RUN_S,
            )
        self.assertEqual(r.returncode, 2)
        self.assertIn("no such file", r.stderr)

    def test_a_logotype_that_is_no_css_selector_exits_2_naming_it(self):
        with tempfile.TemporaryDirectory() as out:
            r = script(
                os.path.join(FIXTURES, "logotype.html"),
                "--out",
                out,
                "--logotype",
                ".brand",
                "--logotype",
                "[[",
                timeout=ARGUMENT_RUN_S,
            )
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("--logotype is not a CSS selector: [[", r.stderr)

    def test_a_parts_declaration_that_is_not_one_or_names_no_css_selector_exits_2(
        self,
    ):  # #315
        with tempfile.TemporaryDirectory() as out:
            bad = pathlib.Path(out, "parts.json")
            for text, said in (
                ("not json", "is not JSON ("),
                (
                    '{"declared": {"carousel": "[["}}',
                    "--parts is not a CSS selector: [[",
                ),
            ):
                with self.subTest(text):
                    bad.write_text(text)
                    r = script(
                        os.path.join(FIXTURES, "keyboard-tier01-skip.html"),
                        "--out",
                        out,
                        "--parts",
                        str(bad),
                        timeout=ARGUMENT_RUN_S,
                    )
                    self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
                    self.assertIn(said, r.stderr)

    def test_a_refused_page_exits_5_and_leaves_no_earlier_report(self):
        with tempfile.TemporaryDirectory() as out:
            pathlib.Path(out, "access.json").write_text("{}")
            # Port 9, discard, has no listener here, so the browser is refused at once.
            r = script("http://127.0.0.1:9/", "--out", out, timeout=ARGUMENT_RUN_S)
            left = os.listdir(out)
        self.assertEqual(r.returncode, 5, r.stdout + r.stderr)
        self.assertIn("the browser could not load http://127.0.0.1:9/", r.stderr)
        self.assertEqual(left, [])


class MissingPackages(unittest.TestCase):
    def test_a_missing_package_exits_3_naming_the_pinned_requirements(self):  # #256
        for package in ("numpy", "PIL"):
            with self.subTest(package):
                proc = without(package)
                self.assertEqual(proc.returncode, 3, proc.stderr)
                self.assertIn(f"check-access.py: {package}", proc.stderr)
                self.assertIn(f"-r {REQUIREMENTS}", proc.stderr)


if __name__ == "__main__":
    child.main()
