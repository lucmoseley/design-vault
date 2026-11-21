"""Tests plugin/skills/design-round/scripts/check-clip.py (#336): python3 test/check-clip.test.py

Drives the check from outside, by exit code and printed lines, on MP4 headers
the test builds into a scratch round folder `r1` beside its spend log. Broken,
it lets a clip that runs long or short pass vault.length, a loop never asked
for pass vault.clip-loop, or a model it cannot read pass unjudged.
"""

import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-clip.py"
)
SPEND_LOG = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "spend-log.py"
)
FIELDS = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "references", "loop-fields.json"
)
ROSTER = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "references", "roster.md"
)

KLING = "kling-video/v3.0/std/image-to-video"
WAN = "wan/v2.7/image-to-video"
STILL = "https://example.test/r1/v1-still.png"


def box(kind, payload, large=False, to_end=False):
    if to_end:
        return struct.pack(">I4s", 0, kind) + payload
    if large:
        return struct.pack(">I4sQ", 1, kind, 16 + len(payload)) + payload
    return struct.pack(">I4s", 8 + len(payload), kind) + payload


def mvhd(timescale, duration, version=0):
    if version == 0:
        times = struct.pack(">IIII", 1, 2, timescale, duration)
    else:
        times = struct.pack(">QQIQ", 1, 2, timescale, duration)
    # The rest of a real mvhd: rate, volume, matrix, pre-defined, next track id.
    return box(b"mvhd", bytes([version, 0, 0, 0]) + times + bytes(80))


def mp4(timescale, duration, *, version=0, moov_last=False, large_mdat=False):
    ftyp = box(b"ftyp", b"isom\x00\x00\x02\x00isomiso2avc1mp41")
    moov = box(b"moov", mvhd(timescale, duration, version) + box(b"trak", bytes(8)))
    mdat = box(b"mdat", bytes(64), large=large_mdat)
    return ftyp + (mdat + moov if moov_last else moov + mdat)


def run(*args):
    out = subprocess.run(
        [sys.executable, SCRIPT, *args], capture_output=True, text=True
    )
    return out.returncode, out.stdout, out.stderr


class Round(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.round = os.path.join(self.tmp.name, "r1")
        os.mkdir(self.round)
        self.log = os.path.join(self.round, "higgsfield-spend.jsonl")

    def tearDown(self):
        self.tmp.cleanup()

    def clip(self, stem, data=None):
        path = os.path.join(self.round, f"{stem}.mp4")
        with open(path, "wb") as f:
            f.write(mp4(1000, 5000) if data is None else data)
        return path

    def logged(self, *lines):
        """Writes the round's spend log afresh: one line per (candidate, model, input)."""
        with open(self.log, "w", encoding="utf8") as f:
            for candidate, model, given in lines:
                f.write(
                    json.dumps({"candidate": candidate, "model": model, "input": given})
                    + "\n"
                )

    def looped(self, *stems, model=KLING, end="last_image_url"):
        """Writes the spend log afresh with a line per stem sending STILL as both frames."""
        self.logged(
            *((f"r1/{s}", model, {"image_url": STILL, end: STILL}) for s in stems)
        )


class Length(Round):
    def test_a_length_inside_the_range_passes_in_mvhd_versions_0_and_1(self):
        self.looped("v1-zero", "v2-one")
        for stem, version in (("v1-zero", 0), ("v2-one", 1)):
            path = self.clip(stem, mp4(12800, 64000, version=version))
            code, out, _ = run(path, "--range", "4-6")
            self.assertEqual(code, 0, out)
            self.assertIn("length: PASS — 5.000 s, inside 4-6 s", out)

    def test_a_length_below_or_above_the_range_fails_in_both_versions_saying_render_again(
        self,
    ):
        self.looped("v1-short", "v2-long", "v3-short", "v4-long")
        for stem, version, duration, side in (
            ("v1-short", 0, 3999, "shorter"),
            ("v2-long", 0, 6001, "longer"),
            ("v3-short", 1, 3999, "shorter"),
            ("v4-long", 1, 6001, "longer"),
        ):
            path = self.clip(stem, mp4(1000, duration, version=version))
            code, out, _ = run(path, "--range", "4-6")
            self.assertEqual(code, 1, f"{stem}: {out}")
            self.assertRegex(
                out,
                rf"length: FAIL — \d\.\d{{3}} s, {side} than the brief's 4-6 s: "
                "render it again with a duration inside the range",
            )

    def test_the_ranges_ends_pass(self):
        self.looped("v1-low", "v2-high")
        for stem, duration in (("v1-low", 4000), ("v2-high", 6000)):
            code, out, _ = run(self.clip(stem, mp4(1000, duration)), "--range", "4-6")
            self.assertEqual(code, 0, out)

    def test_a_64_bit_duration_past_32_bits_is_read_whole(self):
        self.looped("v1-wide")
        # 2^32 + 5000 ticks at a timescale of 2^30: 4.0000047 s, where its low 32 bits alone give 0.0000047 s.
        path = self.clip("v1-wide", mp4(2**30, 2**32 + 5000, version=1))
        code, out, _ = run(path, "--range", "4.000001-4.1")
        self.assertEqual(code, 0, out)

    def test_moov_after_a_64_bit_mdat_is_found(self):
        self.looped("v1-tail")
        path = self.clip("v1-tail", mp4(1000, 5000, moov_last=True, large_mdat=True))
        code, out, _ = run(path, "--range", "4-6")
        self.assertEqual(code, 0, out)
        self.assertIn("5.000 s", out)

    def test_no_range_prints_the_length_not_judged_with_exit_6(self):
        self.looped("v1-free")
        code, out, _ = run(self.clip("v1-free"))
        self.assertEqual(code, 6, out)
        self.assertIn("length: NOT JUDGED — 5.000 s; no range: give --range", out)

    def test_a_header_with_no_duration_or_timescale_is_not_judged(self):
        self.looped("v1-zero", "v2-unknown", "v3-unknown", "v4-timeless")
        for stem, data in (
            ("v1-zero", mp4(1000, 0)),
            ("v2-unknown", mp4(1000, 0xFFFFFFFF)),
            ("v3-unknown", mp4(1000, 0xFFFFFFFFFFFFFFFF, version=1)),
            ("v4-timeless", mp4(0, 5000)),
        ):
            code, out, _ = run(self.clip(stem, data), "--range", "4-6")
            self.assertEqual(code, 6, f"{stem}: {out}")
            self.assertIn("length: NOT JUDGED — the header gives no duration", out)

    def test_a_last_box_running_to_the_files_end_is_read(self):
        self.looped("v1-open")
        mdat = box(b"mdat", bytes(64))
        data = (
            box(b"ftyp", b"isom") + mdat + box(b"moov", mvhd(1000, 5000), to_end=True)
        )
        code, out, _ = run(self.clip("v1-open", data), "--range", "4-6")
        self.assertEqual(code, 0, out)
        self.assertIn("5.000 s", out)

    def test_a_file_with_no_moov_is_bad_input_naming_it(self):
        self.looped("v1-bare")
        data = box(b"ftyp", b"isom") + box(b"mdat", bytes(64))
        code, _, err = run(self.clip("v1-bare", data))
        self.assertEqual(code, 2)
        self.assertRegex(err, r"check-clip: \S*v1-bare\.mp4 has no moov box")

    def test_a_box_running_past_the_file_is_bad_input_naming_it(self):
        self.looped("v1-cut", "v2-png")
        cut = box(b"ftyp", b"isom") + struct.pack(">I4s", 4096, b"mdat") + bytes(64)
        png = b"\x89PNG\r\n\x1a\n" + bytes(64)
        for stem, data in (("v1-cut", cut), ("v2-png", png)):
            code, _, err = run(self.clip(stem, data))
            self.assertEqual(code, 2, stem)
            self.assertRegex(
                err, r"check-clip: a '\S+' box at byte \d+ runs past its parent"
            )

    def test_an_mvhd_of_another_version_or_cut_short_is_bad_input(self):
        self.looped("v1-two", "v2-short")
        two = box(b"mvhd", bytes([2, 0, 0, 0]) + bytes(96))
        short = box(b"mvhd", bytes([1, 0, 0, 0]) + bytes(20))
        for stem, inner, why in (
            ("v1-two", two, "mvhd is version 2, not 0 or 1"),
            ("v2-short", short, "mvhd is too short for version 1"),
        ):
            data = box(b"ftyp", b"isom") + box(b"moov", inner)
            code, _, err = run(self.clip(stem, data))
            self.assertEqual(code, 2, stem)
            self.assertIn(why, err)

    def test_a_moov_with_no_mvhd_is_bad_input(self):
        self.looped("v1-bare")
        data = box(b"ftyp", b"isom") + box(b"moov", box(b"trak", bytes(8)))
        code, _, err = run(self.clip("v1-bare", data))
        self.assertEqual(code, 2)
        self.assertIn("no mvhd box", err)

    def test_a_malformed_range_is_bad_usage(self):
        path = self.clip("v1-x")
        for text in ("6-4", "five", "4"):
            code, _, err = run(path, "--range", text)
            self.assertEqual(code, 2, text)
            self.assertIn("MIN-MAX", err)


class Loop(Round):
    def test_one_still_as_both_frames_passes_for_each_roster_model(self):
        for stem, model, end in (
            ("v1-kling", KLING, "last_image_url"),
            ("v2-wan", WAN, "end_image_url"),
        ):
            self.looped(stem, model=model, end=end)
            code, out, _ = run(self.clip(stem), "--range", "4-6")
            self.assertEqual(code, 0, out)
            self.assertIn(f"loop: PASS — image_url and {end} both send {STILL}", out)
            self.assertRegex(out, rf"{re.escape(model)} \(.*line for r1/{stem}\)")

    def test_differing_stills_fail_naming_both_urls(self):
        for stem, model, end in (
            ("v1-kling", KLING, "last_image_url"),
            ("v2-wan", WAN, "end_image_url"),
        ):
            self.logged(
                (f"r1/{stem}", model, {"image_url": STILL, end: STILL + "?v=2"})
            )
            code, out, _ = run(self.clip(stem), "--range", "4-6")
            self.assertEqual(code, 1, out)
            self.assertIn(
                f"loop: FAIL — image_url {STILL} and {end} {STILL}?v=2 differ", out
            )

    def test_a_request_with_no_end_frame_fails_naming_the_models_end_field(self):
        self.logged(("r1/v1-open", KLING, {"image_url": STILL}))
        code, out, _ = run(self.clip("v1-open"), "--range", "4-6")
        self.assertEqual(code, 1, out)
        self.assertIn("loop: FAIL — the request sent no end frame, last_image_url", out)

    def test_another_models_end_field_is_not_read_as_this_ones(self):
        self.logged(
            ("r1/v1-mixed", KLING, {"image_url": STILL, "end_image_url": STILL})
        )
        code, out, _ = run(self.clip("v1-mixed"), "--range", "4-6")
        self.assertEqual(code, 1, out)
        self.assertIn("loop: FAIL — the request sent no end frame, last_image_url", out)

    def test_a_request_with_no_start_frame_fails_naming_the_field_and_the_way_out(self):
        self.logged(("r1/v1-text", WAN, {"end_image_url": STILL}))
        code, out, _ = run(self.clip("v1-text"), "--range", "4-6")
        self.assertEqual(code, 1, out)
        self.assertIn(
            "loop: FAIL — the request sent no start frame, image_url: render it again "
            "with the still as both image_url and end_image_url",
            out,
        )

    def test_an_unknown_model_is_not_judged_with_exit_6(self):
        self.logged(
            ("r1/v1-luma", "luma/ray-3.2", {"image_url": STILL, "frame1": STILL})
        )
        code, out, _ = run(self.clip("v1-luma"), "--range", "4-6")
        self.assertEqual(code, 6, out)
        self.assertIn(
            "loop: NOT JUDGED — luma/ray-3.2 has no row in loop-fields.json",
            out,
        )

    def test_a_clip_with_no_log_line_or_no_log_is_not_judged(self):
        code, out, _ = run(self.clip("v1-alone"), "--range", "4-6")
        self.assertEqual(code, 6, out)
        self.assertIn("loop: NOT JUDGED — no spend log", out)
        self.looped("v9-other")
        code, out, _ = run(self.clip("v1-alone"), "--range", "4-6")
        self.assertEqual(code, 6, out)
        self.assertIn("loop: NOT JUDGED — no line for r1/v1-alone", out)

    def test_a_requests_later_output_takes_its_first_line(self):
        self.looped("v1-pair")
        code, out, _ = run(self.clip("v1-pair-2"), "--range", "4-6")
        self.assertEqual(code, 0, out)
        self.assertIn("line for r1/v1-pair)", out)

    def test_a_fail_outranks_a_not_judged_across_clips(self):
        self.logged(
            ("r1/v1-luma", "luma/ray-3.2", {}),
            ("r1/v2-open", KLING, {"image_url": STILL}),
        )
        code, _, _ = run(self.clip("v1-luma"), self.clip("v2-open"), "--range", "4-6")
        self.assertEqual(code, 1)

    def test_a_named_log_elsewhere_is_read(self):
        other = os.path.join(self.tmp.name, "spend.jsonl")
        with open(other, "w", encoding="utf8") as f:
            f.write(
                json.dumps(
                    {
                        "candidate": "r1/v1-far",
                        "model": WAN,
                        "input": {"image_url": STILL, "end_image_url": STILL},
                    }
                )
                + "\n"
            )
        code, out, _ = run(self.clip("v1-far"), "--range", "4-6", "--log", other)
        self.assertEqual(code, 0, out)
        code, _, err = run(self.clip("v1-far"), "--log", other + ".missing")
        self.assertEqual(code, 2)
        self.assertIn(f"cannot read {other}.missing", err)

    def test_a_missing_or_broken_fields_file_exits_2(self):
        # A copy of the check in a scratch plugin tree, so loop-fields.json beside it can be broken.
        scripts = os.path.join(self.tmp.name, "plugin", "scripts")
        references = os.path.join(self.tmp.name, "plugin", "references")
        os.makedirs(scripts)
        copy = shutil.copy(SCRIPT, scripts)
        shutil.copy(SPEND_LOG, scripts)
        clip = self.clip("v1-a")
        for broken in (None, "{not json", '{"models": {"m": {"start": "image_url"}}}'):
            if broken is not None:
                os.makedirs(references, exist_ok=True)
                with open(
                    os.path.join(references, "loop-fields.json"), "w", encoding="utf8"
                ) as f:
                    f.write(broken)
            out = subprocess.run(
                [sys.executable, copy, clip], capture_output=True, text=True
            )
            self.assertEqual(out.returncode, 2, (broken, out.stderr))
            self.assertIn("cannot read", out.stderr)
            self.assertIn("loop-fields.json", out.stderr)


class Fields(unittest.TestCase):
    def test_every_roster_video_model_has_fields_citing_its_request_schema(self):
        with open(ROSTER, encoding="utf8") as f:
            roster = f.read()
        section = roster.split("## Image to video", 1)[1].split("\n## ", 1)[0]
        endpoints = set(
            re.findall(r"`([a-z0-9.-]+(?:/[a-z0-9.-]+)+/image-to-video)`", section)
        )
        self.assertEqual(endpoints, {KLING, WAN})
        self.assertIn("loop-fields.json", section)
        with open(FIELDS, encoding="utf8") as f:
            models = json.load(f)["models"]
        self.assertEqual(set(models), endpoints)
        for endpoint, row in models.items():
            self.assertRegex(row["start"], r"^[a-z_]+$", endpoint)
            self.assertRegex(row["end"], r"^[a-z_]+$", endpoint)
            self.assertRegex(
                row["source"],
                r"^docs: https://docs\.higgsfield\.ai/docs/models/[a-z0-9-]+/[a-z0-9-]+, Input schema, read \d{4}-\d{2}-\d{2}$",
                endpoint,
            )


if __name__ == "__main__":
    unittest.main()
