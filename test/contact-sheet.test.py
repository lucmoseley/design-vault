import json
import os
import sys
import tempfile
import unittest

from PIL import Image

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "contact-sheet.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "sheet")
SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

sheet = siblings.load(SCRIPTS, "contact-sheet.py")

LABELS = ["0.00 s", "0.25 s", "0.50 s", "0.75 s", "1.00 s", "1.10 s (end)"]


def run(*args):
    # guess, #501
    return child.run([sys.executable, SCRIPT, *args], timeout=180)


class Ramp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.TemporaryDirectory()
        cls.proc = run(os.path.join(FIXTURES, "ramp.html"), "--out", cls.dir.name)
        if cls.proc.returncode != 0:
            cls.dir.cleanup()
            raise AssertionError(
                f"exit {cls.proc.returncode}: {cls.proc.stdout}{cls.proc.stderr}"
            )
        with open(os.path.join(cls.dir.name, "sheet.json"), encoding="utf8") as fh:
            cls.record = json.load(fh)

    @classmethod
    def tearDownClass(cls):
        cls.dir.cleanup()

    def test_it_writes_both_sheets_and_says_so_71(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)
        self.assertIn(
            "desktop 1920x945: 6 frames, 0 to 1100 ms every 250 ms", self.proc.stdout
        )
        self.assertIn(
            "phone 390x664: 6 frames, 0 to 1100 ms every 250 ms", self.proc.stdout
        )

    def test_each_tile_is_the_moment_its_label_names_at_both_sizes(self):
        for size, ratio in (("desktop", 1920 / 945), ("phone", 390 / 664)):
            with self.subTest(size=size):
                s = self.record["sheets"][size]
                self.assertEqual([t["label"] for t in s["tiles"]], LABELS)
                with Image.open(s["file"]) as png:
                    image = png.convert("RGB")
                reds = []
                for t in s["tiles"]:
                    self.assertAlmostEqual(t["width"] / t["height"], ratio, places=2)
                    reds.append(
                        image.getpixel(
                            (t["x"] + t["width"] // 2, t["y"] + t["height"] // 2)
                        )[0]
                    )
                for t, red in zip(s["tiles"], reds, strict=True):
                    self.assertLessEqual(
                        abs(red - t["ms"] / 5),
                        2,
                        f"{t['label']}: red {red}, so {red * 5} ms",
                    )

    def test_each_tile_has_its_label_drawn_under_it(self):
        s = self.record["sheets"]["desktop"]
        with Image.open(s["file"]) as png:
            image = png.convert("L")
        for t in s["tiles"]:
            strip = image.crop(
                (
                    t["x"],
                    t["y"] + t["height"] + 4,
                    t["x"] + t["width"],
                    t["y"] + t["height"] + 40,
                )
            )
            self.assertLess(
                strip.getextrema()[0], 128, f"no ink under the {t['label']} tile"
            )

    def test_each_frame_is_kept_at_full_size(self):
        self.assertEqual(
            sorted(os.listdir(os.path.join(self.dir.name, "phone"))),
            sorted(f"frame-{n}.png" for n in (0, 250, 500, 750, 1000, 1100)),
        )
        with Image.open(
            os.path.join(self.dir.name, "desktop", "frame-250.png")
        ) as frame:
            self.assertEqual(frame.size, (1920, 945))


class Refusals(unittest.TestCase):
    def test_a_page_with_no_timeline_cannot_be_sheeted(self):
        with tempfile.TemporaryDirectory() as out:
            proc = run(os.path.join(FIXTURES, "still.html"), "--out", out)
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn("has no timeline", proc.stdout)
        self.assertIn("Record it playing instead", proc.stdout)

    def test_a_chain_started_by_finish_events_cannot_be_sheeted_259(self):
        with tempfile.TemporaryDirectory() as out:
            proc = run(
                os.path.join(HERE, "fixtures", "frames", "chained.html"), "--out", out
            )
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        self.assertIn("starts animations when others finish (div#bottom)", proc.stdout)

    def test_a_viewport_that_is_not_w_by_h_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as out:
            proc = run(
                os.path.join(FIXTURES, "ramp.html"), "--out", out, "--phone", "390"
            )
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("--phone wants WxH", proc.stderr)


class Times(unittest.TestCase):
    def test_every_step_and_the_end_where_the_steps_miss_it(self):
        self.assertEqual(sheet.times(1100, 250), [0, 250, 500, 750, 1000, 1100])

    def test_an_end_on_a_step_is_not_drawn_twice(self):
        self.assertEqual(sheet.times(1000, 250), [0, 250, 500, 750, 1000])

    def test_a_step_just_short_of_the_end_moves_onto_it(self):
        self.assertEqual(sheet.times(1000.4, 250), [0, 250, 500, 750, 1000.4])

    def test_only_the_last_frame_is_labelled_the_end(self):
        self.assertEqual(
            sheet.labels([0, 250, 1000.4]), ["0.00 s", "0.25 s", "1.00 s (end)"]
        )


class SheetHtml(unittest.TestCase):
    def test_the_captions_run_in_frame_order_under_their_frames(self):
        doc = sheet.sheet_html("t", [("0.00 s", b"a"), ("0.25 s (end)", b"b")], 2, 320)
        self.assertRegex(
            doc,
            r'<img src="data:image/png;base64,YQ=="><figcaption>0\.00 s</figcaption>.*'
            r'<img src="data:image/png;base64,Yg=="><figcaption>0\.25 s \(end\)</figcaption>',
        )


if __name__ == "__main__":
    child.main()
