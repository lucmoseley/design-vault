"""Pins check-layout.py's detectors to exact width ranges (#78): python3 test/check-layout.test.py

`ranges`, the sweep's widths and the viewport meta's faults are tested on
synthetic input. Each detector is
run end to end on a fixture whose fault holds over a known range of widths,
swept over a window around it so the suite stays quick. It is a suite of the
commit gate (test/all.sh): loosening a range or a message here lets a builder's
sweep pass a layout fault to the critic again.

The --text modes (#305) are pinned the same way: `text_faults`, `zoomed` and
the table on synthetic input, then text-spacing-fault.html, whose every plant
names the record it fails, and text-spacing-clean.html, which must report
nothing.

The --records checks (#311) are pinned on synthetic input where they merge
widths or judge numbers, then end to end: tier01-fault.html, where each plant
carries the records it fails and the run must fail each on its plant, and
tier01-clean.html, where every record must pass with no fault.
"""

import argparse
import concurrent.futures
import datetime
import functools
import html.parser
import importlib.util
import json
import os
import pathlib
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-layout.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "layout")
spec = importlib.util.spec_from_file_location("check_layout", SCRIPT)
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)

SCRATCH = tempfile.TemporaryDirectory()
TEXT = ["--widths", "620-700", "--step", "40"]
ALL_MODES = ["--text", "spacing", "--text", "zoom", "--text", "size"]
# A table whose values change nothing on the fault page (no plant there sets a
# line height under 1): every mode must then report nothing.
NO_CHANGE = os.path.join(SCRATCH.name, "no-change.table")
pathlib.Path(NO_CHANGE).write_text(
    "vault.text-spacing | spacing | line-height 1, after-paragraph 0, letter-spacing 0, word-spacing 0\n"
    "vault.fluid-type | zoom | 1\n"
    "vault.fluid-type | size | 1\n"
)
# #515
TABLE_WITH_VISIBLE_NAV = os.path.join(SCRATCH.name, "records.table")
pathlib.Path(TABLE_WITH_VISIBLE_NAV).write_text(
    pathlib.Path(layout.TABLE).read_text()
    + "vault.visible-nav | visible-nav | at most 4 links\n"
)
# Five widths across the phone, tablet and desktop bands, both sides of each
# record's bounds on the tier01 pages.
RECORDS = [
    "--widths",
    "390-1400",
    "--step",
    "310",
    "--records",
    "--table",
    TABLE_WITH_VISIBLE_NAV,
]
RECORD_FACTS = [
    "--parts",
    os.path.join(FIXTURES, "tier01-parts.json"),
    "--brief",
    "kind=site",
]
# The focal box focal-art.svg draws, in its own pixels.
FOCAL_BOX = "1100,350,200,200"
# name: (fixture, extra arguments)
RUNS = {
    "overflow": ("overflow.html", ["--widths", "320-620"]),
    "nested": ("nested.html", ["--widths", "320-620"]),
    "probe": ("probe.html", ["--widths", "420-430"]),
    "cut": ("cut.html", ["--widths", "320-520"]),
    "slide": ("slide.html", ["--widths", "1080-1360"]),
    "under": ("under.html", ["--widths", "780-920"]),
    "crowd": ("crowd.html", ["--widths", "1480-1620"]),
    "sronly": ("sronly.html", ["--widths", "600-610"]),
    "details-closed": ("details-closed.html", ["--widths", "600-610"]),
    "details-open": ("details-open.html", ["--widths", "600-610"]),
    "touch": ("touch.html", ["--widths", "760-775", "--step", "1"]),
    "nometa": ("nometa.html", ["--widths", "763-772", "--step", "1"]),
    "fixed": ("fixed.html", ["--widths", "595-605"]),
    "fold": ("fold.html", ["--widths", "320-800", "--cta", ".book"]),
    "wide": ("wide.html", ["--widths", "1900-2560"]),
    "missing": (
        "fold.html",
        ["--widths", "320-320", "--cta", ".nowhere", "--focal", ".nowhere=1,1,2,2"],
    ),
    "hidden": ("fold.html", ["--widths", "320-320", "--cta", ".gone"]),
    "clean": ("clean.html", ["--cta", ".book", "--step", "20"]),
    "shots": ("clean.html", ["--step", "400"]),
    "spacing-fault": ("text-spacing-fault.html", [*TEXT, *ALL_MODES]),
    "spacing-clean": ("text-spacing-clean.html", [*TEXT, *ALL_MODES]),
    "spacing-table": (
        "text-spacing-fault.html",
        [*TEXT, *ALL_MODES, "--table", NO_CHANGE],
    ),
    "size-only": ("text-spacing-fault.html", [*TEXT, "--text", "size"]),
    "records-fault": ("tier01-fault.html", [*RECORDS, *RECORD_FACTS]),
    "records-clean": ("tier01-clean.html", [*RECORDS, *RECORD_FACTS]),
    "records-bare": ("tier01-fault.html", ["--widths", "390-390", "--records"]),
    "records-site": ("tier01-real-site.html", [*RECORDS, "--brief", "kind=site"]),
    "records-app": ("tier01-real-app.html", [*RECORDS, "--brief", "kind=app"]),
    "records-overlay": ("tier01-real-overlay.html", [*RECORDS, "--brief", "kind=site"]),
    "columns-clean": ("tier01-columns-clean.html", RECORDS),
    "columns-fault": ("tier01-columns-fault.html", RECORDS),
    "columns-beside": ("tier01-columns-beside.html", RECORDS),
    "records-gaps": (
        "tier01-gaps.html",
        [*RECORDS, "--parts", os.path.join(FIXTURES, "tier01-gaps-parts.json")],
    ),
    "main-grid": ("tier01-main-grid.html", ["--widths", "700-700", "--records"]),
    "reading-column": (
        "tier01-reading-column.html",
        ["--widths", "1400-1400", "--records", "--brief", "page=reading"],
    ),
    "reading-wide": (
        "tier01-reading-wide.html",
        ["--widths", "1400-1400", "--records", "--brief", "page=reading"],
    ),
    "records-narrow": (
        "tier01-fault.html",
        ["--widths", "400-500", "--step", "100", "--records", *RECORD_FACTS],
    ),
    "records-wide": (
        "tier01-fault.html",
        ["--widths", "700-900", "--step", "200", "--records", *RECORD_FACTS],
    ),
    "focal-cover": (
        "focal-cover.html",
        [
            "--widths",
            "430-450",
            "--step",
            "1",
            "--focal",
            f".hero={FOCAL_BOX}",
            "--focal",
            f".inset={FOCAL_BOX}",
            "--focal",
            f".dense={FOCAL_BOX}",
        ],
    ),
    "focal-position": (
        "focal-position.html",
        [
            "--widths",
            "560-590",
            "--step",
            "1",
            "--focal",
            f".hero={FOCAL_BOX}",
            "--focal",
            f".wide={FOCAL_BOX}",
            "--focal",
            f".over={FOCAL_BOX}",
            "--focal",
            f".near={FOCAL_BOX}",
            "--focal",
            f".sized={FOCAL_BOX}",
        ],
    ),
    "focal-kept": (
        "focal-kept.html",
        [
            "--step",
            "20",
            "--focal",
            f".hero={FOCAL_BOX}",
            "--focal",
            f".band={FOCAL_BOX}",
            "--focal",
            f".edge={FOCAL_BOX}",
        ],
    ),
    "focal-unmeasured": (
        "focal-unmeasured.html",
        [
            "--widths",
            "400-420",
            "--step",
            "20",
            "--focal",
            f".turned={FOCAL_BOX}",
            "--focal",
            ".two=1,1,2,2",
            "--focal",
            ".gone=1,1,2,2",
            "--focal",
            ".round=1,1,2,2",
            "--focal",
            ".swap=1,1,2,2",
        ],
    ),
}
# Each run is a browser; four at once keeps the commit gate quick on a shared machine.
PARALLEL = 4
DONE = {}


def setUpModule():
    stale = pathlib.Path(SCRATCH.name, "shots", "layout-320-20200101T000000Z.png")
    stale.parent.mkdir(parents=True)
    stale.write_bytes(b"")
    with concurrent.futures.ThreadPoolExecutor(PARALLEL) as pool:
        DONE.update(zip(RUNS, pool.map(sweep, RUNS), strict=True))


def sweep(name):
    fixture, extra = RUNS[name]
    out = os.path.join(SCRATCH.name, name)
    # A guess at the slowest sweep, with room to spare: it loads the page once per viewport.
    r = child.run(
        [sys.executable, SCRIPT, os.path.join(FIXTURES, fixture), "--out", out, *extra],
        timeout=600,
    )
    found = None
    if os.path.exists(os.path.join(out, "layout.json")):
        with open(os.path.join(out, "layout.json"), encoding="utf8") as fh:
            found = json.load(fh)
    return r.returncode, r.stdout, r.stderr, found, out


def tearDownModule():
    SCRATCH.cleanup()


def spans(name, kind):
    return [
        (r["from"], r["to"], r["subject"], r["detail"])
        for r in DONE[name][3]["ranges"]
        if r["kind"] == kind
    ]


class Ranges(unittest.TestCase):
    def fault(self, kind, subject, detail="d"):
        return {"kind": kind, "subject": subject, "detail": detail}

    def test_consecutive_widths_join_and_a_gap_splits(self):
        a = self.fault("scroll", "div.a")
        found = [(320, [a]), (325, [a]), (330, []), (335, [a])]
        self.assertEqual(
            [(r["from"], r["to"]) for r in layout.ranges(found)],
            [(320, 325), (335, 335)],
        )

    def test_the_detail_is_the_first_widths(self):
        found = [
            (320, [self.fault("cta", ".b", "first")]),
            (325, [self.fault("cta", ".b", "second")]),
        ]
        self.assertEqual(layout.ranges(found)[0]["detail"], "first")

    def test_subjects_and_kinds_are_apart(self):
        found = [
            (
                320,
                [
                    self.fault("overlap", "x"),
                    self.fault("scroll", "x"),
                    self.fault("scroll", "y"),
                ],
            )
        ]
        self.assertEqual(
            [(r["kind"], r["subject"]) for r in layout.ranges(found)],
            [("scroll", "x"), ("scroll", "y"), ("overlap", "x")],
        )

    def test_the_sweep_steps_to_1920_and_ends_on_2560(self):
        self.assertEqual(layout.sweep_widths(5)[:2], [320, 325])
        self.assertEqual(layout.sweep_widths(5)[-2:], [1920, 2560])
        self.assertEqual(len(layout.sweep_widths(5)), 322)
        self.assertEqual(layout.sweep_widths(400, 320, 1000), [320, 720, 1000])
        self.assertEqual(layout.sweep_widths(5, 2000, 2560), [2000, 2560])
        self.assertEqual(layout.sweep_widths(3)[-3:], [1919, 1920, 2560])

    def test_each_band_has_its_height(self):
        self.assertEqual(
            [layout.height_at(w, (1, 2, 3)) for w in (320, 767, 768, 1023, 1024, 2560)],
            [1, 1, 2, 2, 3, 3],
        )


class Zoom(unittest.TestCase):
    """What keeps a phone from zooming, read from the viewport meta as W3C ACT rule b4f0c3 reads it."""

    def test_each_value_is_judged_as_the_act_rule_judges_it(self):
        cases = {
            None: [],
            "": [],
            "width=device-width, initial-scale=1": [],
            "user-scalable=no": ["user-scalable=no"],
            "user-scalable=0": ["user-scalable=0"],
            "user-scalable=0.5": ["user-scalable=0.5"],
            "user-scalable=1": [],
            "user-scalable=-1": [],
            "user-scalable=yes": [],
            "user-scalable=device-width": [],
            "maximum-scale=1.9": ["maximum-scale=1.9"],
            "maximum-scale=2": [],
            "maximum-scale=-1": [],
            "maximum-scale=yes": ["maximum-scale=yes"],
            "maximum-scale=device-height": [],
            "Width=device-width; MAXIMUM-SCALE = 1": ["maximum-scale=1"],
            "initial-scale=1 maximum-scale=1 user-scalable=no": [
                "maximum-scale=1",
                "user-scalable=no",
            ],
        }
        for content, want in cases.items():
            self.assertEqual(layout.zoom_blocks(content), want, content)


class Scale(unittest.TestCase):
    def test_a_page_laid_out_at_the_phones_width_but_shown_zoomed_is_a_fault(self):
        got = {
            "metas": ["width=device-width, initial-scale=2"],
            "laidWidth": 390,
            "scale": 2,
        }
        [fault] = layout.viewport_faults(390, got)
        self.assertEqual(fault["kind"], "viewport")
        self.assertIn(
            "lay the page out 390 px wide and show it at 200%", fault["detail"]
        )

    def test_a_scale_within_rounding_of_1_is_not(self):
        got = {"metas": ["width=device-width"], "laidWidth": 390, "scale": 1.004}
        self.assertEqual(layout.viewport_faults(390, got), [])


def run_it(*args):
    # A guess, with room to spare: a refused argument exits before any browser starts.
    return child.run([sys.executable, SCRIPT, *map(str, args)], timeout=120)


class Arguments(unittest.TestCase):
    def run_it(self, *args):
        return run_it(*args)

    def test_a_span_outside_the_sweep_is_refused(self):
        with tempfile.TemporaryDirectory() as out:
            r = self.run_it(
                os.path.join(FIXTURES, "clean.html"),
                "--out",
                out,
                "--widths",
                "200-900",
            )
        self.assertEqual(r.returncode, 2)
        self.assertIn("--widths", r.stderr)

    def test_a_selector_the_browser_refuses_exits_2_and_leaves_no_earlier_report(self):
        with tempfile.TemporaryDirectory() as out:
            for stale in ("layout.json", "layout-320-20200101T000000Z.png"):
                pathlib.Path(out, stale).write_text("{}")
            r = self.run_it(
                os.path.join(FIXTURES, "clean.html"),
                "--out",
                out,
                "--widths",
                "320-320",
                "--cta",
                "[[",
            )
            left = os.listdir(out)
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn("--cta '[['", r.stderr)
        self.assertEqual(left, [])

    def test_a_brief_fact_or_parts_declaration_it_cannot_read_exits_2(self):
        with tempfile.TemporaryDirectory() as out:
            bad = pathlib.Path(out, "bad.json")
            bad.write_text("not json")
            for args, said in (
                (["--brief", "kind=shop"], "--brief wants kind=app|site"),
                (["--brief", "page=wide"], "got 'page=wide'"),
                (["--parts", pathlib.Path(out, "absent.json")], "cannot read --parts"),
                (["--parts", bad], f"--parts {bad}"),
            ):
                r = self.run_it(
                    os.path.join(FIXTURES, "tier01-clean.html"),
                    "--out",
                    out,
                    "--records",
                    *args,
                )
                self.assertEqual(r.returncode, 2, (args, r.stderr))
                self.assertIn(said, r.stderr, args)

    def test_only_a_whole_sweep_at_5_px_or_finer_gates(self):
        self.assertTrue(layout.gating(argparse.Namespace(step=5, span=(320, 2560))))
        self.assertFalse(layout.gating(argparse.Namespace(step=6, span=(320, 2560))))
        self.assertFalse(layout.gating(argparse.Namespace(step=5, span=(320, 1920))))
        self.assertFalse(layout.gating(argparse.Namespace(step=1, span=(320, 1919))))
        _, stdout, _, found, _ = DONE["clean"]
        self.assertIn("NOT A GATING SWEEP", stdout)
        self.assertFalse(found["gating"])


class Detectors(unittest.TestCase):
    def fault(self, name, kind):
        """The run's one range of this kind, once the run exited 1 and printed it."""
        code, stdout, stderr, found, _ = DONE[name]
        self.assertEqual(code, 1, stdout + stderr)
        [held] = [r for r in found["ranges"] if r["kind"] == kind]
        self.assertIn(
            f"{layout.span(held)}: {held['subject']} {held['detail']}", stdout
        )
        return held["from"], held["to"], held["subject"], held["detail"]

    def test_a_fixed_width_strip_scrolls_the_page_below_its_width(self):
        low, high, subject, detail = self.fault("overflow", "scroll")
        self.assertEqual((low, high, subject), (320, 595, "div.strip:nth-of-type(1)"))
        self.assertIn("280 px past", detail)

    def test_a_strip_widened_for_a_coarse_pointer_scrolls_up_to_the_phone_bands_edge(
        self,
    ):
        low, high, subject, detail = self.fault("touch", "scroll")
        self.assertEqual((low, high, subject), (760, 767, "div.strip"))
        self.assertIn("140 px past", detail)

    def test_a_page_with_no_viewport_meta_is_laid_out_980_px_wide_up_to_the_phone_bands_edge(
        self,
    ):
        low, high, subject, detail = self.fault("nometa", "viewport")
        self.assertEqual((low, high, subject), (763, 767, "the viewport meta"))
        self.assertEqual(
            detail,
            "is missing, so a phone 763 px wide lays the page out 980 px wide and shows it at 78%",
        )
        self.assertEqual({r["kind"] for r in DONE["nometa"][3]["ranges"]}, {"viewport"})

    def test_the_last_viewport_meta_fixing_the_width_is_caught_either_side_of_it(self):
        meta = '"width=600, maximum-scale=1.5"'
        self.assertEqual(
            spans("fixed", "viewport"),
            [
                (
                    595,
                    595,
                    "the viewport meta",
                    f"{meta} makes a phone 595 px wide lay the page out 600 px wide and show it at 99%",
                ),
                (
                    605,
                    605,
                    "the viewport meta",
                    f"{meta} makes a phone 605 px wide lay the page out 600 px wide and show it at 101%",
                ),
            ],
        )

    def test_a_viewport_meta_blocking_zoom_is_caught_through_the_phone_band(self):
        low, high, subject, detail = self.fault("fixed", "zoom")
        self.assertEqual((low, high, subject), (595, 605, "the viewport meta"))
        self.assertEqual(
            detail,
            "user-scalable=no and maximum-scale=1.5 keep a phone from zooming to 200%, as WCAG 1.4.4 asks",
        )

    def test_the_cause_inside_a_stretched_flex_item_is_named(self):
        low, high, subject, detail = self.fault("nested", "scroll")
        self.assertEqual((low, high, subject), (320, 595, "div.row > div.card"))
        self.assertIn("with div.row > div.card > div.wide inside it", detail)

    def test_a_fixed_boxs_text_past_the_edge_is_cut_off_though_a_box_around_it_clips(
        self,
    ):
        low, high, subject, _ = self.fault("overflow", "cut")
        self.assertEqual((low, high), (320, 415))
        self.assertIn("p.badge", subject)

    def test_text_past_a_hidden_edge_is_cut_off_inside_a_clipping_box_escaping_one_and_off_the_left(
        self,
    ):
        code, stdout, _, _, _ = DONE["cut"]
        self.assertEqual(code, 1)
        self.assertEqual(spans("cut", "scroll"), [])
        self.assertEqual(
            [(low, high, subject) for low, high, subject, _ in spans("cut", "cut")],
            [
                (320, 475, "div.box:nth-of-type(2) > p.tag"),
                (320, 445, "div.wrap:nth-of-type(1) > p.note"),
                (320, 495, "p.address:nth-of-type(1)"),
                (320, 520, "p.lead:nth-of-type(2)"),
            ],
        )
        self.assertIn(
            "320–520 px: p.lead:nth-of-type(2) runs 40 px past the screen's edge",
            stdout,
        )

    def test_text_sliding_over_a_photos_edge_overlaps_at_that_range(self):
        low, high, subject, detail = self.fault("slide", "overlap")
        self.assertEqual((low, high), (1100, 1340))
        self.assertIn("img.photo", subject)
        self.assertIn("crosses the image's edge", detail)

    def test_text_drawn_under_a_photo_overlaps_at_that_range(self):
        low, high, _, detail = self.fault("under", "overlap")
        self.assertEqual((low, high), (800, 900))
        self.assertIn("hidden under", detail)

    def test_hidden_text_is_found_below_the_first_screen_after_it_and_through_pointer_events_none(
        self,
    ):
        code, stdout, _, _, _ = DONE["probe"]
        self.assertEqual(code, 1)
        found = spans("probe", "overlap")
        self.assertEqual(
            [(low, high) for low, high, _, _ in found], [(420, 430), (420, 430)]
        )
        self.assertEqual(
            sorted(s.split(" > ")[1].split(" ")[0] for _, _, s, _ in found),
            ["p.caption", "p.heading"],
        )
        self.assertTrue(all("hidden under" in d for _, _, _, d in found))
        self.assertIn("p.caption text and", stdout)

    def test_captions_hidden_for_a_screen_reader_over_a_photo_do_not_overlap_it(
        self,
    ):  # #220
        code, stdout, stderr, found, _ = DONE["sronly"]
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual(found["ranges"], [])

    def test_links_in_a_closed_details_are_not_drawn_so_text_over_them_overlaps_nothing(
        self,
    ):  # #418
        code, stdout, stderr, found, _ = DONE["details-closed"]
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual(found["ranges"], [])
        low, high, subject, _ = self.fault("details-open", "overlap")
        self.assertEqual((low, high), (600, 610))
        self.assertIn("div.group > ul", subject)
        self.assertIn("p.note", subject)

    def test_two_text_blocks_crossing_overlap_at_that_range(self):
        low, high, subject, _ = self.fault("crowd", "overlap")
        self.assertEqual((low, high), (1500, 1600))
        self.assertIn("p.lead", subject)
        self.assertIn("p.note", subject)

    def test_a_call_to_action_below_the_phone_screen_is_reported(self):
        low, high, subject, detail = self.fault("fold", "cta")
        self.assertEqual((low, high, subject), (320, 765, ".book"))
        self.assertIn("664 px tall", detail)

    def test_a_page_wider_than_1920_px_is_swept_at_2560(self):
        low, high, subject, _ = self.fault("wide", "scroll")
        self.assertEqual((low, high, subject), (2560, 2560, "div.rail"))

    def test_a_call_to_action_that_matches_nothing_or_is_never_shown_is_reported(self):
        self.assertEqual(self.fault("missing", "cta")[3], "matches nothing")
        self.assertEqual(self.fault("hidden", "cta")[3], "is not shown")

    def test_a_clean_page_exits_0(self):
        code, stdout, stderr, found, _ = DONE["clean"]
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual(found["ranges"], [])
        self.assertIn("call to action off the first screen: none", stdout)

    def test_each_gate_question_gets_its_own_answer_from_its_own_faults(self):
        cases = (
            ("overflow", {"vault.reflow": "fail", "vault.layout": None}),
            ("nometa", {"vault.reflow": "fail", "vault.layout": None}),
            ("fold", {"vault.reflow": "pass", "vault.layout": "fail"}),
            ("clean", {"vault.reflow": "pass", "vault.layout": "pass"}),
        )
        for name, want in cases:
            _, stdout, _, found, _ = DONE[name]
            for question, answer in want.items():
                self.assertEqual(found["answers"][question], answer, name)
                printed = "not checked, no --cta given" if answer is None else answer
                self.assertIn(f"\n{question}: {printed}\n", stdout, name)


class Focal(unittest.TestCase):
    def crops(self, name):
        code, stdout, stderr, found, _ = DONE[name]
        self.assertEqual(code, 1, stdout + stderr)
        self.assertEqual(found["answers"]["vault.focal-crop"], "fail")
        self.assertIn("\nvault.focal-crop: fail\n", stdout)
        got = {}
        for r in found["ranges"]:
            if r["kind"] == "crop":
                self.assertIn(f"{layout.span(r)}: {r['subject']} {r['detail']}", stdout)
                got[r["subject"]] = (r["from"], r["to"], r["detail"])
        return got

    def test_a_cover_image_loses_the_focal_box_off_a_phone_up_to_442_px_and_to_its_own_box(
        self,
    ):
        self.assertEqual(
            self.crops("focal-cover"),
            {
                ".hero": (
                    430,
                    442,
                    "cuts the focal box 16 px on its right, in the art's pixels, showing 91% of it",
                ),
                ".dense": (
                    430,
                    442,
                    "cuts the focal box 16 px on its right, in the art's pixels, showing 91% of it",
                ),
                ".inset": (
                    430,
                    450,
                    "cuts the focal box 162 px on its right, in the art's pixels, showing 18% of it",
                ),
            },
        )

    def test_a_background_pinned_left_loses_it_up_to_576_px_and_a_clipping_frame_at_every_width(
        self,
    ):
        self.assertEqual(
            self.crops("focal-position"),
            {
                ".hero": (
                    560,
                    576,
                    "cuts the focal box 40 px on its right, in the art's pixels, showing 80% of it",
                ),
                ".wide": (560, 590, "shows none of the focal box"),
                ".sized": (
                    560,
                    576,
                    "cuts the focal box 40 px on its right, in the art's pixels, showing 80% of it",
                ),
                ".near": (
                    560,
                    561,
                    "cuts the focal box 5 px on its left, in the art's pixels, showing 97% of it",
                ),
                ".over": (
                    560,
                    576,
                    "cuts the focal box 40 px on its right, in the art's pixels, showing 80% of it",
                ),
            },
        )

    def test_art_that_keeps_its_focal_box_passes_at_every_width(self):
        code, stdout, stderr, found, _ = DONE["focal-kept"]
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual(found["ranges"], [])
        self.assertEqual(found["answers"]["vault.focal-crop"], "pass")
        self.assertEqual(
            [f["selector"] for f in found["focal"]], [".hero", ".band", ".edge"]
        )

    def test_art_it_cannot_model_exits_6_naming_each(self):
        code, stdout, stderr, found, _ = DONE["focal-unmeasured"]
        self.assertEqual(code, 6, stdout + stderr)
        self.assertEqual(found["answers"]["vault.focal-crop"], "cannot measure")
        self.assertIn("\nvault.focal-crop: cannot measure\n", stdout)
        got = {
            subject: detail
            for _, _, subject, detail in spans("focal-unmeasured", "unmeasured")
        }
        self.assertEqual(sorted(got), [".gone", ".round", ".swap", ".turned", ".two"])
        self.assertIn("is transformed", got[".turned"])
        self.assertEqual(
            got[".two"], "has 2 background images, so which is the art is not known"
        )
        self.assertEqual(got[".gone"], "is shown at no swept width")
        self.assertEqual(
            got[".round"],
            "repeats its background as round, which rescales or moves the tile",
        )
        self.assertEqual(
            got[".swap"],
            "loads art files of different sizes (800x450 px at 400 px, 1600x900 px at 420 px), so the focal box's pixels name no one file",
        )
        self.assertIn(
            "\n  judge each art not measured by eye, in the screenshots below\n", stdout
        )
        self.assertEqual(spans("focal-unmeasured", "unshown"), [])

    def test_a_selector_matching_nothing_fails(self):
        self.assertEqual(
            self.crops("missing"), {".nowhere": (320, 320, "matches nothing")}
        )

    def test_with_no_focal_the_question_is_not_checked(self):
        _, stdout, _, found, _ = DONE["clean"]
        self.assertIsNone(found["answers"]["vault.focal-crop"])
        self.assertIn("\nvault.focal-crop: not checked, no --focal given\n", stdout)

    def test_a_focal_box_with_no_area_or_a_selector_the_browser_refuses_exits_2(self):
        with tempfile.TemporaryDirectory() as out:
            page = os.path.join(FIXTURES, "clean.html")
            flat = run_it(page, "--out", out, "--focal", ".hero=1,1,0,2")
            bad = run_it(
                page, "--out", out, "--widths", "320-320", "--focal", "[[=1,1,2,2"
            )
        self.assertEqual(flat.returncode, 2, flat.stderr)
        self.assertIn("--focal wants SELECTOR=X,Y,W,H", flat.stderr)
        self.assertEqual(bad.returncode, 2, bad.stderr)
        self.assertIn("--focal '[[' is not a selector", bad.stderr)


def text_spans(name, mode):
    return [(r["kind"], r["subject"]) for r in DONE[name][3]["text"][mode]["ranges"]]


class TextFaults(unittest.TestCase):
    def fault(self, kind, subject, place=None, share=None):
        f = {"kind": kind, "subject": subject, "detail": "d"}
        return f if place is None else {**f, "place": place, "share": share}

    def test_only_what_the_100_percent_page_lacks_is_reported(self):
        base = {
            "faults": [
                self.fault("clip", "a", 1, 0.5),
                self.fault("clip", "b", 2, 0.1),
                self.fault("overlap", "b"),
            ],
            "sizes": [],
        }
        got = {
            "faults": [
                self.fault("clip", "a", 1, 0.53),
                self.fault("clip", "b", 2, 0.4),
                # The same label as a, but another element.
                self.fault("clip", "a", 3, 0.2),
                self.fault("reveal", "e", 4, 0.3),
                self.fault("overlap", "b"),
                self.fault("overlap", "c"),
                self.fault("scroll", "d"),
            ],
            "sizes": [],
        }
        found = layout.text_faults(base, got)
        self.assertEqual(
            [(f["kind"], f["subject"]) for f in found],
            [("clip", "b"), ("clip", "a"), ("reveal", "e"), ("overlap", "c")],
        )
        self.assertTrue(all(set(f) == {"kind", "subject", "detail"} for f in found))

    def test_text_short_of_the_factor_by_more_than_rounding_is_listed(self):
        base = {"faults": [], "sizes": [[1, "p.a", 16], [2, "p.b", 16], [3, "p.c", 10]]}
        got = {
            "faults": [],
            "sizes": [[1, "p.a", 31.8], [2, "p.b", 31.6], [4, "p.d", 1]],
        }
        found = layout.text_faults(base, got, grow=2)
        self.assertEqual([f["subject"] for f in found], ["p.b"])
        self.assertIn(
            "grows to 198% (16 to 31.6 px), short of 200%", found[0]["detail"]
        )
        self.assertEqual(layout.text_faults(base, got), [])

    def test_zoom_lays_a_screen_out_narrower_down_to_reflows_floor(self):
        self.assertEqual(layout.zoomed(1280, 633, 2), (640, 316))
        self.assertEqual(layout.zoomed(640, 664, 2), (320, 332))
        self.assertIsNone(layout.zoomed(638, 664, 2))

    def test_readings_fail_nothing(self):
        runs = [{"kind": k} for k in ("grow", "reveal", "clip", "overlap", "cut")]
        self.assertEqual(
            [r["kind"] for r in layout.failing(runs, layout.TEXT_KINDS)],
            ["clip", "overlap", "cut"],
        )


class Table(unittest.TestCase):
    def test_each_mode_reads_its_values(self):
        modes = layout.parse_table(pathlib.Path(layout.TABLE).read_text())
        self.assertEqual(modes["spacing"].id, "vault.text-spacing")
        self.assertEqual(
            modes["spacing"].value,
            {
                "line-height": 1.5,
                "after-paragraph": 2,
                "letter-spacing": 0.12,
                "word-spacing": 0.16,
            },
        )
        self.assertEqual((modes["zoom"].value, modes["size"].value), (2, 2))
        self.assertEqual({modes["zoom"].id, modes["size"].id}, {"vault.fluid-type"})

    def test_the_values_are_the_records(self):
        record = pathlib.Path(
            HERE, "..", "plugin", "skills", "design-critique", "rules", "typography.md"
        ).read_text()
        modes = layout.parse_table(pathlib.Path(layout.TABLE).read_text())
        inputs = re.search(
            r"### vault\.fluid-type\n(?:- .*\n)*?- inputs: (.*)", record
        )[1]
        self.assertIn(
            f"at {modes['zoom'].value * 100:g}% zoom (a viewport of W ÷ {modes['zoom'].value:g} CSS px",
            inputs,
        )
        self.assertEqual(modes["size"].value, 2)
        self.assertIn("the root size doubled", inputs)
        question = re.search(
            r"### vault\.text-spacing\n- applies-when: .*\n- question: (.*)", record
        )[1]
        v = layout.parse_table(pathlib.Path(layout.TABLE).read_text())["spacing"].value
        self.assertIn(
            f"line height set to {v['line-height']:g}, spacing after paragraphs to {v['after-paragraph']:g}, "
            f"letter spacing to {v['letter-spacing']:g} and word spacing to {v['word-spacing']:g} times the font size",
            question,
        )

    def test_a_line_the_probe_cannot_run_is_refused(self):
        for bad in (
            "vault.x | spacing | line-height 1.5",
            "vault.x | stretch | 2",
            "vault.x | zoom",
            "vault.x | zoom | twice",
            "vault.x | zoom | 1..2",
            "vault.x | size | 0",
            "vault.x | zoom | 2\nvault.y | zoom | 3",
        ):
            with self.assertRaises(layout.TableError, msg=bad):
                layout.parse_table(bad)

    def test_a_bad_or_short_table_exits_2_before_any_browser(self):
        with tempfile.TemporaryDirectory() as out:
            short = pathlib.Path(out, "short.table")
            short.write_text("vault.fluid-type | zoom | 2\n")
            for table, said in (
                (short, "no spacing line"),
                (pathlib.Path(out, "none"), "cannot read"),
            ):
                r = run_it(
                    os.path.join(FIXTURES, "clean.html"),
                    "--out",
                    out,
                    "--text",
                    "spacing",
                    "--table",
                    table,
                )
                self.assertEqual(r.returncode, 2, r.stderr)
                self.assertIn(said, r.stderr)


class TextModes(unittest.TestCase):
    def test_the_fault_page_names_every_plant_and_fails_text_spacing(self):
        code, stdout, stderr, found, _ = DONE["spacing-fault"]
        self.assertEqual(code, 1, stdout + stderr)
        page = pathlib.Path(FIXTURES, "text-spacing-fault.html").read_text()
        self.assertEqual(found["answers"]["vault.text-spacing"], "fail")
        self.assertIn("\nvault.text-spacing: fail\n", stdout)
        record = {"reveal": "vault.text-spacing-reveal"}
        self.assertEqual(
            sorted(
                (record.get(k, "vault.text-spacing"), s)
                for k, s in text_spans("spacing-fault", "spacing")
            ),
            [
                ("vault.text-spacing", "div.card:nth-of-type(1) > p:nth-of-type(2)"),
                ("vault.text-spacing", "div.line:nth-of-type(2)"),
                ("vault.text-spacing", "div.words:nth-of-type(3)"),
                (
                    "vault.text-spacing",
                    "div:nth-of-type(4) > h2.head and div:nth-of-type(4) > p.after",
                ),
                ("vault.text-spacing", "section:nth-of-type(1) > span.tag"),
                ("vault.text-spacing-reveal", "div:nth-of-type(5) > a.more"),
            ],
        )
        self.assertEqual(
            sorted(re.findall(r'data-record="([^"]+)"', page)),
            ["vault.text-spacing"] * 5 + ["vault.text-spacing-reveal"],
        )
        self.assertIn("vault.text-spacing-reveal's look critics judge", stdout)
        self.assertEqual(found["answers"]["vault.reflow"], "pass")
        for mode in ("zoom", "size"):
            planted = sorted(
                f"section:nth-of-type({n}) > p.{cls}"
                for n, (cls, modes) in enumerate(
                    re.findall(r'<section><p class="(\w+)" data-probe="([^"]+)"', page),
                    2,
                )
                if mode in modes.split()
            )
            self.assertEqual(
                sorted(s for k, s in text_spans("spacing-fault", mode) if k == "grow"),
                planted,
                mode,
            )
            self.assertEqual(
                [k for k, _ in text_spans("spacing-fault", mode)],
                ["grow"] * len(planted),
            )

    def test_the_spacing_clip_is_measured_past_the_texts_own_box(self):
        details = [
            r["detail"] for r in DONE["spacing-fault"][3]["text"]["spacing"]["ranges"]
        ]
        self.assertTrue(
            any(
                re.search(
                    r"past the edge of div\.card:nth-of-type\(1\), which hides its overflow$",
                    d,
                )
                for d in details
            )
        )
        self.assertTrue(
            any(
                re.search(r"^has 1\d px of its text hidden past its own edge", d)
                for d in details
            )
        )

    def test_zoom_skips_screens_under_its_floor(self):
        widths = [
            w["width"] for w in DONE["spacing-fault"][3]["text"]["zoom"]["widths"]
        ]
        self.assertEqual(widths, [660, 700])
        self.assertEqual(
            [
                (r["from"], r["to"])
                for r in DONE["spacing-fault"][3]["text"]["zoom"]["ranges"]
            ],
            [(660, 700)],
        )

    def test_the_clean_page_reports_nothing(self):
        code, stdout, stderr, found, _ = DONE["spacing-clean"]
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual(found["answers"]["vault.text-spacing"], "pass")
        self.assertEqual(found["answers"]["vault.reflow"], "pass")
        self.assertEqual(
            {m: v["ranges"] for m, v in found["text"].items()},
            {"spacing": [], "zoom": [], "size": []},
        )

    def test_text_that_only_grows_less_fails_nothing(self):
        code, stdout, stderr, found, _ = DONE["size-only"]
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual({k for k, _ in text_spans("size-only", "size")}, {"grow"})
        self.assertIsNone(found["answers"]["vault.text-spacing"])

    def test_the_values_come_from_the_table(self):
        code, stdout, stderr, found, _ = DONE["spacing-table"]
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual(
            {m: v["ranges"] for m, v in found["text"].items()},
            {"spacing": [], "zoom": [], "size": []},
        )
        self.assertIn("at 100% browser zoom", stdout)
        # Chromium's own defaults, 16 px and 13 px, times each table's factor.
        self.assertEqual(found["text"]["size"]["default_sizes"], [16, 13])
        self.assertEqual(
            DONE["spacing-fault"][3]["text"]["size"]["default_sizes"], [32, 26]
        )

    def test_a_run_without_text_leaves_text_spacing_unchecked(self):
        _, stdout, _, found, _ = DONE["clean"]
        self.assertIsNone(found["answers"]["vault.text-spacing"])
        self.assertEqual(found["text"], {})
        self.assertIn(
            "\nvault.text-spacing: not checked, no --text spacing given\n", stdout
        )


records = layout.records


def record_modes():
    """{record: [mode…]} from the table's record lines."""
    out = {}
    for m in layout.parse_table(
        pathlib.Path(TABLE_WITH_VISIBLE_NAV).read_text()
    ).values():
        if m.name in records.CHECKS:
            out.setdefault(m.id, []).append(m.name)
    return out


class RecordUnits(unittest.TestCase):
    def test_each_value_is_read_by_its_checks_shape(self):
        self.assertEqual(
            records.parse_value(
                "line-length",
                "body 50-75, columns 40-50, large 75, short 80 to 3 lines",
            ),
            {
                "body_lo": 50,
                "body_hi": 75,
                "columns_lo": 40,
                "columns_hi": 50,
                "large": 75,
                "short": 80,
                "short_lines": 3,
            },
        )
        self.assertEqual(
            records.parse_value("panes", "1 under 840 or under 480 tall, else 2"),
            {"few": 1, "wide": 840, "tall": 480, "most": 2},
        )
        self.assertEqual(records.parse_value("seams", "scales 1.25, 1.5"), [1.25, 1.5])
        self.assertIsNone(records.parse_value("fold", "none"))
        for mode, bad in (
            ("fold", "1"),
            ("nav-place", "under"),
            ("card-media", "25px"),
        ):
            with self.assertRaises(ValueError, msg=bad):
                records.parse_value(mode, bad)

    def test_every_record_the_live_table_checks_is_answered_by_this_script(self):
        rules = "".join(
            f.read_text()
            for f in pathlib.Path(
                HERE, "..", "plugin", "skills", "design-critique", "rules"
            ).glob("*.md")
        )
        for m in layout.parse_table(pathlib.Path(layout.TABLE).read_text()).values():
            if m.name not in records.CHECKS:
                continue
            with self.subTest(m.id):
                record = re.search(rf"### {re.escape(m.id)}\n((?:- .*\n)*)", rules)[1]
                self.assertIn("- answered-by: script\n", record)
                self.assertRegex(record, r"- script: check-layout\.py .*--records")

    def test_each_record_lines_numbers_are_its_records(self):
        rules = "".join(
            f.read_text()
            for f in pathlib.Path(
                HERE, "..", "plugin", "skills", "design-critique", "rules"
            ).glob("*.md")
        )
        words = {1: "one", 2: "two", 3: "three", 4: "four"}
        for line in pathlib.Path(TABLE_WITH_VISIBLE_NAV).read_text().splitlines():
            fields = [f.strip() for f in line.split("|")]
            if len(fields) != 3 or fields[1] not in records.CHECKS:
                continue

            def text(rid):
                return re.search(rf"### {re.escape(rid)}\n((?:- .*\n)*)", rules)[1]

            # A record whose applies-when takes its widths from another, as
            # vault.side-pane from vault.panes-by-width, reads that one's too.
            record = text(fields[0])
            applies = re.search(r"- applies-when: (.*)", record)[1]
            record += "".join(text(r) for r in re.findall(r"vault\.[a-z-]+", applies))
            for n in map(float, re.findall(r"\d+(?:\.\d+)?", fields[2])):
                # As written, as a percentage (1.25 as 125), or in words.
                said = any(
                    re.search(rf"(?<![\d.]){re.escape(f'{x:g}')}(?![\d])", record)
                    for x in (n, n * 100)
                ) or any(
                    w in record
                    for w in (words.get(n), "twice" if n == 2 else None)
                    if w
                )
                self.assertTrue(said, f"{fields[0]}: {n:g}")

    def test_a_record_line_the_check_cannot_read_or_a_second_one_is_refused(self):
        for bad in (
            "vault.x | nav-place | under wide",
            "vault.x | fold | none\nvault.y | fold | none",
        ):
            with self.assertRaises(layout.TableError, msg=bad):
                layout.parse_table(bad)

    def test_a_check_lacking_a_part_or_a_brief_fact_says_which(self):
        self.assertEqual(
            records.missing("card-media", {}, {}),
            "no card part declared with a selector (--parts)",
        )
        self.assertEqual(records.missing("nav-place", {}, {}), "no --brief kind= given")
        self.assertIsNone(records.missing("card-media", {"card": ".card"}, {}))

    def test_each_record_takes_fail_then_not_judged_then_pass_then_no_match(self):
        mode = layout.Mode
        lines = {
            "fold": mode("vault.a", "fold", None),
            "seams": mode("vault.a", "seams", None),
            "card-media": mode("vault.b", "card-media", None),
            "row-wrap": mode("vault.c", "row-wrap", None),
            "rtl-order": mode("vault.d", "rtl-order", None),
        }
        self.assertEqual(
            records.answers(
                lines,
                {"seams": [{}]},
                {"card-media", "row-wrap", "fold"},
                {"card-media": "no card part"},
            ),
            {
                "vault.a": "fail",
                "vault.b": "not judged",
                "vault.c": "pass",
                "vault.d": "no match",
            },
        )

    def test_each_line_is_judged_by_its_blocks_role(self):
        v = records.parse_value(
            "line-length", "body 50-75, columns 40-50, large 75, short 80 to 3 lines"
        )

        def block(n, size, length, *, full=True, at=0):
            return {
                "block": f"p{n}",
                "size": size,
                "at": at,
                "lines": [{"text": "x" * length, "full": full}] * n,
            }

        blocks = [
            block(6, 16, 60),  # body, in range
            block(6, 16, 45),  # body, short of 50
            block(6, 16, 45),  # in columns: 40-50
            block(6, 16, 45),  # fills its screen: no floor
            block(4, 32, 76),  # large: 75 or fewer
            block(3, 16, 81),  # short passage: 80 or fewer
            block(6, 16, 30, full=False),  # a last line short is no fault
        ]
        facts = [
            {"columns": c, "fills": f}
            for c, f in ((0, 0), (0, 0), (1, 0), (0, 1), (0, 0), (0, 0), (0, 0))
        ]
        self.assertEqual(
            [
                (f["subject"], f["detail"])
                for f in records.line_faults(blocks, facts, v)
            ],
            [
                ("p6", "sets lines of 45 characters as body text, which wants 50–75"),
                (
                    "p4",
                    "sets lines of 76 characters as large text, which wants 75 or fewer",
                ),
                (
                    "p3",
                    "sets lines of 81 characters as a short passage, which wants 80 or fewer",
                ),
            ],
        )

    def test_a_card_set_beside_anywhere_must_stack_under_its_threshold_and_sit_beside_from_it(
        self,
    ):
        def card(at, em, beside):
            return {"at": at, "em": em, "beside": beside, "label": f"card {at}"}

        found = [
            (390, [card(1, 20, True), card(2, 20, False)]),
            (700, [card(1, 30, False), card(2, 30, False)]),
            (1010, [card(1, 30, True), card(2, 30, False)]),
        ]
        self.assertEqual(
            [
                (w, [f["subject"] for f in fs])
                for w, fs in records.card_media_faults(found, 25)
            ],
            [(390, ["card 1"]), (700, ["card 1"]), (1010, [])],
        )

    def test_the_mark_alone_is_a_fault_only_wider_than_the_full_logo_shows(self):
        full = {"variant": "a", "aspect": 4, "label": "a.logo"}
        mark = {"variant": "b", "aspect": 1, "label": "a.logo"}
        self.assertEqual(
            [
                (w, bool(fs))
                for w, fs in records.logo_faults(
                    [(390, mark), (700, full), (1010, mark), (1320, None)]
                )
            ],
            [(390, False), (700, False), (1010, True), (1320, False)],
        )
        self.assertEqual(records.logo_faults([(390, None)]), [(390, [])])

    def test_fluid_text_must_reach_the_factor_at_zoom_and_move_with_the_text_size(self):
        v = {"zoom": 5, "grow": 2}
        base = {1: ["h1", 20], 2: ["p", 20], 3: ["h2", 20]}
        zoomed = {1: ["h1", 40], 2: ["p", 39], 3: ["h2", 40]}
        sized = {1: ["h1", 30], 2: ["p", 30], 3: ["h2", 20]}
        self.assertEqual(
            [
                (f["subject"], f["detail"])
                for f in records.fluid_faults(
                    base, zoomed, sized, v, slack=layout.GROW_SLACK
                )
            ],
            [
                ("p", "reaches 195% of its 20 px at 500% zoom, short of 200%"),
                (
                    "h2",
                    "stays 20 px with the default text size at 200%: its bounds are not in rem or em",
                ),
            ],
        )

    def test_a_tab_panel_must_show_with_a_link_to_it(self):
        self.assertEqual(
            [
                f["detail"]
                for f in records.tab_faults(
                    [
                        {"id": "a", "shown": False, "linked": True},
                        {"id": "b", "shown": True, "linked": False},
                        {"id": "c", "shown": True, "linked": True},
                    ],
                    False,
                )
            ],
            [
                "is hidden at phone width, with script off, not shown as a section",
                "has no contents link to it, with script off",
            ],
        )


def plants(fixture):
    """{record: [plant id…]} from a fixture's data-record marks."""
    planted = {}

    class Plants(html.parser.HTMLParser):
        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            for record in a.get("data-record", "").split():
                planted.setdefault(record, []).append(a["id"])

    Plants().feed(pathlib.Path(FIXTURES, fixture).read_text())
    return planted


class Records(unittest.TestCase):
    def assert_each_plant_fails(self, run, planted):
        code, stdout, stderr, found, _ = DONE[run]
        self.assertEqual(code, 1, stdout + stderr)
        modes = record_modes()
        got = found["records"]
        for record, ids in planted.items():
            self.assertEqual(got["answers"][record], "fail", record)
            for plant in ids:
                self.assertTrue(
                    any(
                        r["kind"] in modes[record] and f"#{plant}" in r["subject"]
                        for r in got["ranges"]
                    ),
                    f"{record} names no fault on #{plant}",
                )
            self.assertIn(f"\n{record}: fail\n", stdout)
        return got

    def test_the_fault_page_fails_every_record_on_its_plant(self):
        planted = plants("tier01-fault.html")
        self.assertEqual(sorted(planted), sorted(record_modes()))
        got = self.assert_each_plant_fails("records-fault", planted)
        self.assertEqual(got["answers"], {r: "fail" for r in record_modes()})
        # Phone-only checks judge under the records' 600 px, not the 767 px phone band.
        self.assertEqual(
            [(r["from"], r["to"]) for r in got["ranges"] if r["kind"] == "visible-nav"],
            [(390, 390)],
        )

    def test_the_gaps_page_fails_each_widened_check_on_its_plant(self):
        got = self.assert_each_plant_fails("records-gaps", plants("tier01-gaps.html"))
        self.assertEqual(got["answers"]["vault.false-floor"], "pass")
        self.assertEqual(
            [
                (r["from"], r["to"], r["detail"])
                for r in got["ranges"]
                if r["kind"] == "card-columns"
            ],
            [
                (390, 390, "sets its cards 2 across under 600 px, not in one column"),
                (
                    1010,
                    1400,
                    "sets its cards 2 across where 3 fit at their 15em minimum of 240 px",
                ),
            ],
        )
        self.assertIn(
            (390, "the 304 px an empty state's text takes in a container under 464 px"),
            [
                (r["from"], r["detail"].split("past ")[-1])
                for r in got["ranges"]
                if r["kind"] == "empty-width"
            ],
        )

    def test_a_main_element_laid_as_the_grid_has_its_children_held_to_its_lines(self):
        got = self.assert_each_plant_fails("main-grid", plants("tier01-main-grid.html"))
        self.assertIn(
            (
                "section#f-grid-lines",
                "runs 362 px–488 px across, off the column lines of main's grid",
            ),
            [
                (r["subject"], r["detail"])
                for r in got["ranges"]
                if r["kind"] == "grid-lines"
            ],
        )

    def test_a_reading_page_passes_wider_than_its_cap_only_with_its_text_in_two_thirds(
        self,
    ):
        def width(name):
            return [
                r["subject"]
                for r in DONE[name][3]["records"]["ranges"]
                if r["kind"] == "content-width"
            ]

        self.assertEqual(width("reading-column"), [])
        self.assertEqual(width("reading-wide"), ["main > img"])

    def test_the_narrow_checks_read_a_partial_sweeps_narrowest_width_or_say_they_cannot(
        self,
    ):
        got = DONE["records-narrow"][3]["records"]
        for kind in ("tabs-narrow", "popover-sheet"):
            self.assertEqual(
                {(r["from"], r["to"]) for r in got["ranges"] if r["kind"] == kind},
                {(400, 400)},
                kind,
            )
        got = DONE["records-wide"][3]["records"]
        for record in ("vault.tabs-narrow", "vault.popover-sheet"):
            self.assertEqual(got["answers"][record], "not judged", record)
        self.assertEqual(
            got["not_judged"]["vault.tabs-narrow"],
            "the sweep holds no width under 600 px",
        )

    def test_a_style_sheet_from_another_origin_leaves_its_readers_not_judged(self):
        import http.server
        import threading

        with tempfile.TemporaryDirectory() as out:
            pathlib.Path(out, "x.css").write_text("p { color: #333; }\n")
            handler = functools.partial(
                http.server.SimpleHTTPRequestHandler, directory=out
            )
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            try:
                page = pathlib.Path(out, "page.html")
                page.write_text(
                    pathlib.Path(FIXTURES, "tier01-clean.html")
                    .read_text()
                    .replace(
                        "</head>",
                        f'<link rel="stylesheet" href="http://127.0.0.1:{server.server_port}/x.css">\n</head>',
                    )
                )
                r = run_it(page, "--out", out, "--widths", "390-390", "--records")
            finally:
                server.shutdown()
            found = json.loads(pathlib.Path(out, "layout.json").read_text())
        for record in ("vault.fluid-zoom", "vault.bottom-safe-area"):
            self.assertEqual(
                found["records"]["answers"][record], "not judged", r.stdout
            )
            self.assertEqual(found["records"]["not_judged"][record], layout.UNREAD)

    def test_the_clean_page_passes_every_record_with_no_fault(self):
        code, stdout, stderr, found, _ = DONE["records-clean"]
        self.assertEqual(code, 0, stdout + stderr)
        got = found["records"]
        self.assertEqual(got["ranges"], [], stdout + stderr)
        self.assertEqual(got["answers"], {r: "pass" for r in record_modes()})

    def test_pages_built_as_sites_and_apps_are_faulted_only_where_they_break_a_record(
        self,
    ):
        for name, kinds in (
            ("records-site", {"line-length", "footer-narrow"}),
            ("records-app", {"safe-bottom"}),
            ("records-overlay", set()),
        ):
            got = DONE[name][3]["records"]
            self.assertEqual(
                {r["kind"] for r in got["ranges"]}, kinds, (name, got["ranges"])
            )
        self.assertEqual(
            DONE["records-overlay"][3]["records"]["answers"]["vault.footer-narrow"],
            "pass",
        )

    def test_side_by_side_columns_each_keep_their_own_text_edge(self):  # #508
        for name in ("columns-clean", "columns-beside"):
            clean = DONE[name][3]["records"]
            self.assertEqual(clean["answers"]["vault.alignment-lines"], "pass", name)
            self.assertEqual(
                [r for r in clean["ranges"] if r["kind"] == "text-edge"],
                [],
                (name, clean["ranges"]),
            )
        fault = DONE["columns-fault"][3]["records"]
        self.assertEqual(fault["answers"]["vault.alignment-lines"], "fail")
        self.assertEqual(
            {r["subject"] for r in fault["ranges"] if r["kind"] == "text-edge"},
            {"section#f-column-edge", "section#f-column-box"},
            fault["ranges"],
        )

    def test_a_record_table_with_no_phone_width_line_exits_2(self):
        with tempfile.TemporaryDirectory() as out:
            table = pathlib.Path(out, "t.table")
            table.write_text("vault.false-floor | fold | none\n")
            r = run_it(
                os.path.join(FIXTURES, "tier01-clean.html"),
                "--out",
                out,
                "--records",
                "--table",
                table,
            )
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn("no phone-width line", r.stderr)

    def test_a_check_lacking_its_part_or_brief_fact_is_not_judged_and_says_why(self):
        code, stdout, stderr, found, _ = DONE["records-bare"]
        self.assertEqual(code, 1, stdout + stderr)
        got = found["records"]
        self.assertEqual(got["answers"]["vault.card-media-stack"], "not judged")
        self.assertEqual(got["answers"]["vault.logo-version"], "not judged")
        self.assertEqual(got["answers"]["vault.nav-by-width"], "not judged")
        self.assertIn(
            "\nvault.card-media-stack: not judged (no card part declared with a selector (--parts))\n",
            stdout,
        )
        self.assertEqual(
            found["records"]["not_judged"]["vault.nav-by-width"],
            "no --brief kind= given",
        )

    def test_a_run_without_records_reports_none(self):
        _, stdout, _, found, _ = DONE["clean"]
        self.assertIsNone(found["records"])
        self.assertNotIn("records, by", stdout)


class Screenshots(unittest.TestCase):
    def test_each_shot_carries_the_run_time_and_an_earlier_runs_are_gone(self):
        code, stdout, stderr, found, out = DONE["shots"]
        self.assertEqual(code, 0, stdout + stderr)
        run_at = datetime.datetime.fromisoformat(found["run_at"])
        stamp = run_at.strftime("%Y%m%dT%H%M%SZ")
        names = sorted(p.name for p in pathlib.Path(out).glob("*.png"))
        self.assertEqual(
            names,
            sorted(
                f"layout-{w}-{stamp}.png"
                for w in (320, 390, 768, 1024, 1536, 1920, 2560)
            ),
        )
        self.assertTrue(
            all(re.search(r"layout-\d+-" + stamp, s) for s in found["screenshots"])
        )
        self.assertIn(run_at.isoformat(timespec="seconds"), stdout)


if __name__ == "__main__":
    child.main()
