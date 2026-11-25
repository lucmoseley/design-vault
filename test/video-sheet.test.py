"""Tests plugin/skills/design-round/scripts/video-sheet.py: python3 test/video-sheet.test.py"""

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

# The clip: 30 frames a second for 2 s, frame n's red 4n, a hard cut at frame 30 (1.00 s).
FPS, FRAMES, CUT = 30, 60, 30
RED_STEP = 4
RED_SLACK = (
    1  # guess, #408: PNG frames are lossless, so a tile's resample alone moves red
)
TIMEOUT_S = 120  # guess, #408: one run takes seconds here


def make_clip(path):
    with av.open(path, "w") as out:
        stream = out.add_stream("png", rate=FPS)
        stream.width, stream.height, stream.pix_fmt = 128, 72, "rgb24"
        for n in range(FRAMES):
            pixels = np.zeros((72, 128, 3), np.uint8)
            pixels[..., 0] = RED_STEP * n
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
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        text=True,
        timeout=TIMEOUT_S,
    )


TEN_A_SECOND = set(range(0, FRAMES, FPS // 10))
AROUND_CUT = set(range(CUT - 6, CUT + 7))
KEPT = sorted(TEN_A_SECOND | AROUND_CUT | {FRAMES - 1})
PER_SHEET = 10


class Clip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.TemporaryDirectory()
        cls.clip = os.path.join(cls.dir.name, "ramp.mov")
        make_clip(cls.clip)
        cls.out = os.path.join(cls.dir.name, "study")
        cls.proc = run(cls.clip, "--out", cls.out, "--per-sheet", str(PER_SHEET))
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
            self.assertLessEqual(
                abs(red - RED_STEP * n), RED_SLACK, f"{t['label']}: red {red}"
            )

    def test_the_tiles_run_per_sheet_to_a_sheet_in_time_order(self):
        self.assertEqual(
            [t["sheet"] for t in self.record["tiles"]],
            [n // PER_SHEET + 1 for n in range(len(KEPT))],
        )
        self.assertEqual(len(self.record["sheets"]), -(-len(KEPT) // PER_SHEET))

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
        self.assertIn(f"cannot sheet {path}, because cannot open it", proc.stderr)

    def test_a_missing_file_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "gone.mp4")
            proc = run(path, "--out", d)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn(f"no file at {path}", proc.stderr)

    def test_a_missing_package_names_the_install_step(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "av.py"), "w") as fh:
                fh.write("raise ImportError('no av here', name='av')\n")
            proc = subprocess.run(
                [sys.executable, SCRIPT, "clip.mp4", "--out", d],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_S,
                env={**os.environ, "PYTHONPATH": d},
            )
        self.assertEqual(proc.returncode, 3, proc.stdout + proc.stderr)
        self.assertIn("video-sheet.py needs av: python3 -m pip install", proc.stderr)
        self.assertIn("requirements.txt", proc.stderr)

    def test_an_out_dir_that_cannot_be_written_exits_5(self):
        with tempfile.TemporaryDirectory() as d:
            clip = os.path.join(d, "ramp.mov")
            make_clip(clip)
            blocker = os.path.join(d, "file")
            open(blocker, "w").close()
            proc = run(clip, "--out", os.path.join(blocker, "out"))
        self.assertEqual(proc.returncode, 5, proc.stdout + proc.stderr)
        self.assertIn("cannot write the sheets under", proc.stderr)


class Scores(unittest.TestCase):
    def test_steady_change_scores_low_and_a_jump_high_as_scdet_scores(self):
        self.assertEqual(sheet.scores([None, 1, 1, 50, 1]), [0, 1, 0, 49, 1])

    def test_a_score_stays_within_0_and_100(self):
        self.assertEqual(sheet.scores([None, 140]), [0, 100])


class Keep(unittest.TestCase):
    def test_it_keeps_the_first_frame_at_or_after_each_step(self):
        times = [n / 25 for n in range(10)]
        self.assertEqual(sheet.keep(times, [], 10, 0.2), [0, 3, 5, 8, 9])

    def test_it_keeps_every_frame_within_around_of_a_cut(self):
        times = [n / 25 for n in range(30)]
        self.assertEqual(
            sheet.keep(times, [20], 1, 0.08), [0, 18, 19, 20, 21, 22, 25, 29]
        )


if __name__ == "__main__":
    unittest.main()
