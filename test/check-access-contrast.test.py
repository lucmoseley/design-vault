"""Pins check-access.py's tier 0 and 1 contrast questions (#316): python3 test/check-access-contrast.test.py

contrast-tier01-fault.html marks each plant data-record with the record it
fails. It is a suite of the commit gate (test/all.sh): loosening a figure here lets a control
a visitor cannot see reach the critic as a pass.
"""

import concurrent.futures
import importlib.util
import json
import os
import re
import sys
import tempfile
import unittest

import numpy as np

HERE = os.path.dirname(__file__)
SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-access.py"
)
CHILD = importlib.util.spec_from_file_location("child", os.path.join(HERE, "child.py"))
child = importlib.util.module_from_spec(CHILD)
CHILD.loader.exec_module(child)
FIXTURES = os.path.join(HERE, "fixtures", "access")
PARTS = os.path.join(FIXTURES, "contrast-tier01-parts.json")
ABSENT = os.path.join(FIXTURES, "contrast-tier01-absent.json")


def library(name):
    spec = importlib.util.spec_from_file_location(
        name[:-3].replace("-", "_"), os.path.join(os.path.dirname(SCRIPT), name)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


contrasts = library("access-contrast.py")
with open(contrasts.TABLE, encoding="utf8") as fh:
    TABLE_TEXT = fh.read()
TABLE = contrasts.parse_table(TABLE_TEXT)

# How long one run may take, in s: a fixture's whole check, or one that stops
# on its arguments. Guesses, unmeasured.
RUN_S, ARGUMENT_RUN_S = 600, 120
SCRATCH = tempfile.TemporaryDirectory()
DONE = {}


def run(name, *args, parts=PARTS, key=None):
    out = os.path.join(SCRATCH.name, key or name)
    r = child.run(
        [
            sys.executable,
            SCRIPT,
            os.path.join(FIXTURES, f"contrast-tier01-{name}.html"),
            "--out",
            out,
            *(("--parts", parts) if parts else ()),
            *args,
        ],
        timeout=RUN_S,
    )
    found = None
    if os.path.exists(os.path.join(out, "access.json")):
        with open(os.path.join(out, "access.json"), encoding="utf8") as fh:
            found = json.load(fh)
    return r.returncode, r.stdout, r.stderr, found


def setUpModule():
    runs = {
        "fault": lambda: run("fault"),
        "clean": lambda: run("clean"),
        "undeclared": lambda: run("clean", parts=None, key="undeclared"),
        "absent": lambda: run("clean", parts=ABSENT, key="absent"),
    }
    with concurrent.futures.ThreadPoolExecutor(2) as pool:
        DONE.update(zip(runs, pool.map(lambda go: go(), runs.values()), strict=True))


def tearDownModule():
    SCRATCH.cleanup()


def solid(rgb, w=40, h=20):
    return np.full((h, w, 3), rgb, dtype=np.uint8)


class Table(unittest.TestCase):
    def test_every_figure_comes_from_its_line(self):
        self.assertEqual(TABLE.floors.body, 4.5)
        self.assertEqual(TABLE.icon, 3)
        self.assertEqual(TABLE.split, 0.179)
        self.assertEqual((TABLE.gap, TABLE.gap_large), (0.5, 0.4))
        self.assertEqual(TABLE.aim[:2], (7, 4.5))
        self.assertEqual(TABLE.hued, 0.05)

    def test_a_missing_doubled_or_malformed_line_is_refused(self):
        lines = TABLE_TEXT.splitlines()
        icon = next(line for line in lines if "| icon |" in line)
        cases = {
            "no vault.contrast-ladder | icon line": "\n".join(
                line for line in lines if line != icon
            ),
            "a second vault.contrast-ladder | icon": TABLE_TEXT + icon + "\n",
            "wants 1 number(s)": TABLE_TEXT.replace(icon, icon + ", 4"),
            "wants numbers over 0": TABLE_TEXT.replace(
                icon, icon.replace("| 3", "| 0")
            ),
            "want one of": TABLE_TEXT + "vault.contrast | made-up | 3\n",
        }
        for why, text in cases.items():
            with self.subTest(why), self.assertRaises(contrasts.TableError) as caught:
                contrasts.parse_table(text)
            self.assertIn(why, str(caught.exception))

    def test_more_contrast_raises_the_text_floors_alone(self):
        more = contrasts.scheme_floors("more contrast", TABLE)
        self.assertEqual((more.body, more.large), (7, 4.5))
        self.assertEqual(contrasts.scheme_floors("dark", TABLE), TABLE.floors)

    def test_a_bad_table_stops_the_run_with_exit_2(self):
        with tempfile.NamedTemporaryFile("w", suffix=".table", delete=False) as fh:
            fh.write(TABLE_TEXT.replace("| 0.179", "| x"))
        r = child.run(
            [
                sys.executable,
                SCRIPT,
                os.path.join(FIXTURES, "contrast-tier01-clean.html"),
                "--out",
                os.path.join(SCRATCH.name, "bad"),
                "--contrast-table",
                fh.name,
            ],
            timeout=ARGUMENT_RUN_S,
        )
        os.unlink(fh.name)
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn("vault.fill-text | split", r.stderr)


class Figures(unittest.TestCase):
    def test_a_glyph_is_read_against_the_ring_next_to_it(self):
        drawn = solid(255)
        drawn[5:15, 15:25] = 0xCC
        glyph = np.zeros((20, 40), dtype=bool)
        glyph[5:15, 15:25] = True
        got = contrasts.glyph_figure(drawn, glyph, [10, 0, 30, 20])
        self.assertAlmostEqual(got.ratio, 1.61, places=2)
        drawn[0:20, 10:30] = 0x22  # a dark backdrop of its own counts
        drawn[5:15, 15:25] = 0xCC
        self.assertGreater(
            contrasts.glyph_figure(drawn, glyph, [10, 0, 30, 20]).ratio, 3
        )
        self.assertIsNone(
            contrasts.glyph_figure(drawn, np.zeros_like(glyph), [10, 0, 30, 20])
        )

    def test_a_box_is_its_median_fill_against_the_ring_outside_it(self):
        drawn = solid(255, w=60, h=40)
        drawn[10:30, 20:40] = 0xEE
        painted = np.zeros((40, 60), dtype=bool)
        painted[10:30, 20:40] = True
        got = contrasts.box_figure(
            drawn, painted, np.zeros_like(painted), [20, 10, 40, 30]
        )
        self.assertLess(got.ratio, 1.2)
        drawn[10:30, 20:40] = 0x33
        got = contrasts.box_figure(
            drawn, painted, np.zeros_like(painted), [20, 10, 40, 30]
        )
        self.assertGreater(got.ratio, 10)

    def test_a_state_is_the_median_change_over_the_pixels_that_change(self):
        off, on = solid(255), solid(255)
        on[5:15, 5:15] = 0xEE
        self.assertAlmostEqual(
            contrasts.state_figure(on, off, [0, 0, 40, 20]), 1.16, places=2
        )
        self.assertIsNone(contrasts.state_figure(off, off, [0, 0, 40, 20]))

    def test_oklch_matches_published_values(self):
        lightness, c, _ = contrasts.oklch([255, 255, 255])
        self.assertAlmostEqual(lightness, 1.0, places=3)
        self.assertLess(c, 1e-3)
        lightness, c, h = contrasts.oklch([255, 0, 0])  # oklch(62.8% 0.2577 29.23)
        self.assertAlmostEqual(lightness, 0.628, places=3)
        self.assertAlmostEqual(c, 0.2577, places=3)
        self.assertAlmostEqual(h, 29.23, places=1)


class FillText(unittest.TestCase):
    def entry(self, text, fill, *, size=16, weight=400, icon=False):
        return {
            "text": [*text, 1],
            "fill": fill,
            "icon": icon,
            "size": size,
            "weight": weight,
        }

    def test_a_fill_under_the_split_takes_light_text_and_one_over_it_dark(self):
        self.assertIn(
            "a fill at 0.179 or over takes dark text",
            contrasts.fill_fault(self.entry([255] * 3, [0x8A] * 3), TABLE),
        )
        self.assertIsNone(
            contrasts.fill_fault(self.entry([0x11] * 3, [0x8A] * 3), TABLE)
        )
        self.assertIn(
            "a fill under 0.179 takes light text",
            contrasts.fill_fault(self.entry([0] * 3, [0x44] * 3), TABLE),
        )
        self.assertIsNone(
            contrasts.fill_fault(self.entry([255] * 3, [0x44] * 3), TABLE)
        )

    def test_text_in_its_fills_hue_sits_the_gap_apart_in_lightness(self):
        blue, pale = [0x1A, 0x5F, 0xB4], [0x6A, 0x9F, 0xE4]
        self.assertIn("0.5 needed", contrasts.fill_fault(self.entry(pale, blue), TABLE))
        self.assertIsNone(
            contrasts.fill_fault(self.entry([0xE8, 0xF0, 0xFF], blue), TABLE)
        )
        self.assertIn(
            "0.4 needed", contrasts.fill_fault(self.entry(pale, blue, size=24), TABLE)
        )


class Chart(unittest.TestCase):
    def chart(self, fill):
        ground = solid(255)
        ids = ground.copy()
        ids[5:15, 10:20] = (1, 0, contrasts.ID_BLUE)  # mark 0, its fill
        mark = {"index": 0, "subject": "rect#bar", "fill": [*fill, 1], "stroke": None}
        return contrasts.chart_faults(
            {"rect": [0, 0, 40, 20], "marks": [mark]}, ids, ground, TABLE
        )

    def test_a_filled_mark_takes_the_mark_figure_against_the_ground(self):
        (fault,) = self.chart([0xDD] * 3)
        self.assertEqual(fault["subject"], "rect#bar")
        self.assertIn("against the chart's ground (#ffffff)", fault["detail"])
        self.assertIn("3:1 needed", fault["detail"])
        self.assertEqual(self.chart([0x33] * 3), [])


PLANT = re.compile(
    r'id="([^"]+)" data-record="([^"]+)"|data-record="([^"]+)"[^>]*id="([^"]+)"'
)


class EndToEnd(unittest.TestCase):
    def test_every_plant_is_named_under_its_record(self):
        code, out, err, found = DONE["fault"]
        self.assertEqual(code, 1, out + err)
        with open(
            os.path.join(FIXTURES, "contrast-tier01-fault.html"), encoding="utf8"
        ) as fh:
            plants = [(m[0] or m[3], m[1] or m[2]) for m in PLANT.findall(fh.read())]
        self.assertEqual(len(plants), 11)
        for plant, record in plants:
            with self.subTest(plant):
                subjects = [f["subject"] for f in found["answers"][record]["faults"]]
                self.assertTrue(
                    any(s.endswith(f"#{plant}") for s in subjects), (record, subjects)
                )
        self.assertIn(
            "vault.controls-on-photo, controls on a photo and the current page dot: FAIL",
            out,
        )
        self.assertIn(
            "div#dots-plant holds 3 page dots that differ by opacity alone", out
        )
        self.assertIn("mark it by fill, size or shape", out)

    def test_a_thin_face_short_of_the_ladders_aim_is_a_note_not_a_fault(self):
        ladder = DONE["fault"][3]["answers"]["vault.contrast-ladder"]
        self.assertFalse(any("thin-note" in f["subject"] for f in ladder["faults"]))
        self.assertTrue(
            any(
                "p#thin-note" in n["note"] and "7:1 aimed at" in n["note"]
                for n in ladder["notes"]
            )
        )

    def test_a_schemes_own_faults_are_the_theme_questions_alone(self):
        answers = DONE["fault"][3]["answers"]
        theme = {
            f["subject"]: f["detail"] for f in answers["vault.theme-contrast"]["faults"]
        }
        self.assertIn("in the dark scheme, ", theme["p#theme-plant"])
        self.assertIn("in the more contrast scheme, ", theme["p#more-plant"])
        self.assertIn("7:1 needed", theme["p#more-plant"])
        self.assertNotIn("p#contrast-plant", theme)
        light = {f["subject"] for f in answers["vault.contrast"]["faults"]}
        self.assertFalse({"p#theme-plant", "p#more-plant"} & light)

    def test_the_clean_page_meets_every_record(self):
        code, out, err, found = DONE["clean"]
        self.assertEqual(code, 0, out + err)
        for qid in (
            *contrasts.QUESTIONS,
            "vault.contrast",
            "vault.control-edges",
            "vault.theme-contrast",
        ):
            with self.subTest(qid):
                answer = found["answers"][qid]
                self.assertEqual((answer["answer"], answer["unmeasured"]), ("pass", []))


class Undeclared(unittest.TestCase):  # #429
    def test_a_chart_and_page_dots_no_declaration_names_cannot_be_measured_and_say_so(
        self,
    ):
        code, out, err, found = DONE["undeclared"]
        self.assertEqual(code, 6, out + err)
        answers = found["answers"]
        for qid, part, subjects in (
            (
                "vault.chart-contrast",
                "no chart was declared",
                ["figure#chart > svg", "canvas#spark", "svg#bars", "svg#nest"],
            ),
            ("vault.controls-on-photo", "no carousel was declared", ["ul.dots"]),
        ):
            with self.subTest(qid):
                reasons = [u["reason"] for u in answers[qid]["unmeasured"]]
                self.assertEqual(answers[qid]["answer"], "cannot measure")
                self.assertEqual(len(reasons), len(subjects), reasons)
                for subject, reason in zip(subjects, reasons, strict=True):
                    self.assertIn(subject, reason)
                    self.assertIn(part, reason)
        for qid, answer in answers.items():
            if qid not in ("vault.chart-contrast", "vault.controls-on-photo"):
                with self.subTest(qid):
                    self.assertEqual(answer["answer"], "pass")

    def test_a_chart_and_carousel_declared_absent_are_not_looked_for(self):
        code, out, err, found = DONE["absent"]
        self.assertEqual(code, 0, out + err)
        for qid in ("vault.chart-contrast", "vault.controls-on-photo"):
            with self.subTest(qid):
                answer = found["answers"][qid]
                self.assertEqual((answer["answer"], answer["unmeasured"]), ("pass", []))


if __name__ == "__main__":
    child.main()
