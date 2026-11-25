"""Tests plugin/skills/design-round/scripts/video-sheet.py (#408): python3 test/video-sheet.test.py

The clip is made here, lossless, 30 frames a second for 2 s: frame n's red is 4n,
so each tile's time is read back from its pixels, and its green and blue jump
at frame 30, a hard cut at 1.00 s. Loosen it and a study's sheet names moments
its frames are not, or skips the frames either side of a cut where a technique
study reads how one shot hands over to the next.
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

import av
import numpy as np
from PIL import Image

HERE = os.path.dirname(__file__)
SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "video-sheet.py"
)
spec = importlib.util.spec_from_file_location("video_sheet", SCRIPT)
sheet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sheet)

FPS, FRAMES, CUT = 30, 60, 30


def make_clip(path):
    with av.open(path, "w") as out:
        stream = out.add_stream("png", rate=FPS)
        stream.width, stream.height, stream.pix_fmt = 128, 72, "rgb24"
        for n in range(FRAMES):
            pixels = np.zeros((72, 128, 3), np.uint8)
            pixels[..., 0] = 4 * n
            if n >= CUT:
                pixels[..., 1], pixels[..., 2] = 200, 255
            frame = av.VideoFrame.from_ndarray(pixels, format="rgb24")
            frame.pts = n
            for packet in stream.encode(frame):
                out.mux(packet)
        for packet in stream.encode():
            out.mux(packet)


def run(*args):
    return subprocess.run(
        [sys.executable, SCRIPT, *args], capture_output=True, text=True, timeout=120
    )


# Every third frame (ten a second), every frame within 0.2 s of the cut, and the last.
KEPT = sorted(set(range(0, FRAMES, 3)) | set(range(CUT - 6, CUT + 7)) | {FRAMES - 1})


class Clip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.TemporaryDirectory()
        cls.clip = os.path.join(cls.dir.name, "ramp.mov")
        make_clip(cls.clip)
        cls.out = os.path.join(cls.dir.name, "study")
        cls.proc = run(cls.clip, "--out", cls.out)
        if cls.proc.returncode != 0:
            cls.dir.cleanup()
            raise AssertionError(
                f"exit {cls.proc.returncode}: {cls.proc.stdout}{cls.proc.stderr}"
            )
        with open(os.path.join(cls.out, "sheet.json"), encoding="utf8") as fh:
            cls.record = json.load(fh)

    @classmethod
    def tearDownClass(cls):
        cls.dir.cleanup()

    def test_it_finds_the_one_cut_and_says_so(self):
        self.assertEqual(self.record["cuts_ms"], [1000])
        self.assertIn("1 cut(s), at 1.00 s", self.proc.stdout)

    def test_it_keeps_ten_a_second_every_frame_around_the_cut_and_the_last(self):
        self.assertEqual(
            [t["ms"] for t in self.record["tiles"]],
            [round(n * 1000 / FPS) for n in KEPT],
        )

    def test_the_cut_and_the_end_are_labelled(self):
        labels = {t["ms"]: t["label"] for t in self.record["tiles"]}
        self.assertEqual(labels[1000], "1.00 s (cut)")
        self.assertEqual(labels[967], "0.97 s")
        self.assertEqual(labels[1967], "1.97 s (end)")

    def test_each_tile_is_the_frame_its_label_names(self):
        images = {}
        for t in self.record["tiles"]:
            n = round(t["ms"] * FPS / 1000)
            path = self.record["sheets"][t["sheet"] - 1]
            if path not in images:
                with Image.open(path) as png:
                    images[path] = png.convert("RGB")
            red = images[path].getpixel(
                (t["x"] + t["width"] // 2, t["y"] + t["height"] // 2)
            )[0]
            self.assertLessEqual(abs(red - 4 * n), 1, f"{t['label']}: red {red}")

    def test_the_tiles_run_thirty_to_a_sheet(self):
        self.assertEqual(len(self.record["sheets"]), -(-len(KEPT) // 30))
        self.assertEqual([t["sheet"] for t in self.record["tiles"]][29:31], [1, 2])

    def test_each_frame_is_kept_at_full_size(self):
        names = os.listdir(os.path.join(self.out, "frames"))
        self.assertEqual(len(names), len(KEPT))
        with Image.open(os.path.join(self.out, "frames", "frame-1000.png")) as png:
            self.assertEqual(png.size, (128, 72))


class Refusals(unittest.TestCase):
    def test_a_file_that_is_no_clip_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "notes.mp4")
            with open(path, "w") as fh:
                fh.write("not a video")
            proc = run(path, "--out", os.path.join(d, "out"))
        self.assertEqual(proc.returncode, 4, proc.stdout + proc.stderr)
        self.assertIn("cannot sheet", proc.stderr)

    def test_a_missing_file_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as d:
            proc = run(os.path.join(d, "gone.mp4"), "--out", d)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("no file at", proc.stderr)


class Scores(unittest.TestCase):
    def test_steady_change_scores_low_and_a_jump_high_as_scdet_scores(self):
        self.assertEqual(sheet.scores([None, 1, 1, 50, 1]), [0, 1, 0, 49, 1])

    def test_a_score_stays_within_0_and_100(self):
        self.assertEqual(sheet.scores([None, 140]), [0, 100])


class Keep(unittest.TestCase):
    def test_the_first_frame_at_or_after_each_step(self):
        times = [n * 0.04 for n in range(10)]  # 25 a second
        self.assertEqual(sheet.keep(times, [], 10, 0.2), [0, 3, 5, 8, 9])

    def test_every_frame_within_around_of_a_cut(self):
        times = [n * 0.04 for n in range(30)]
        self.assertEqual(
            sheet.keep(times, [20], 1, 0.08), [0, 18, 19, 20, 21, 22, 25, 29]
        )


if __name__ == "__main__":
    unittest.main()
