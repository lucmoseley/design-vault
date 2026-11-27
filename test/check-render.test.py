import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

HERE = os.path.dirname(__file__)
SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-render.py"
)
SPEND_LOG = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "spend-log.py"
)
SIBLINGS = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "siblings.py"
)
CRASH_EXIT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "crash_exit.py"
)
RUNNER = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "runner.py"
)
FAIL_OPEN = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "fail_open.py"
)
SIZES = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "references", "render-sizes.json"
)
ROSTER = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "references", "roster.md"
)


GROK = "xai/grok-imagine-image-2.0"
QWEN = "alibaba/qwen-image-3/text-to-image"
IDEOGRAM = "ideogram/v4.0"
CELL_SLACK_PX = 1  # guess, #332
CELL_SLACK_SHARE = 0.15  # guess, #332


def largest(model, aspect="16:9"):
    with open(SIZES, encoding="utf8") as f:
        size = json.load(f)["models"][model]["sizes"][aspect]["size"]
    return tuple(int(n) for n in size.split("x"))


def run(*args):
    out = subprocess.run(
        [sys.executable, SCRIPT, *args], capture_output=True, text=True
    )
    return out.returncode, out.stdout, out.stderr


class Size(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.round = os.path.join(self.tmp.name, "r1")
        os.mkdir(self.round)
        self.log = os.path.join(self.round, "higgsfield-spend.jsonl")

    def tearDown(self):
        self.tmp.cleanup()

    def render(self, stem, size, folder=None):
        path = os.path.join(folder or self.round, f"{stem}.png")
        Image.new("RGB", size, (40, 90, 150)).save(path)
        return path

    def logged(self, *lines):
        with open(self.log, "w", encoding="utf8") as f:
            for candidate, model, aspect in lines:
                f.write(
                    json.dumps(
                        {
                            "candidate": candidate,
                            "model": model,
                            "input": {"prompt": "x", "aspect_ratio": aspect},
                        }
                    )
                    + "\n"
                )

    def test_a_render_at_its_models_largest_size_passes(self):
        self.logged(("r1/v1-grok", GROK, "16:9"))
        code, out, _ = run(self.render("v1-grok", largest(GROK)))
        self.assertEqual(code, 0, out)
        self.assertRegex(out, rf"{re.escape(GROK)} at 16:9 .*line for r1/v1-grok")
        self.assertRegex(
            out, r"size: PASS — 2816x1584 against the largest, 2816x1584 \(measured"
        )

    def test_a_render_below_its_models_largest_size_fails_by_either_side_328(self):
        w, h = largest(GROK)
        self.logged(
            ("r1/v1-half", GROK, "16:9"),
            ("r1/v2-narrow", GROK, "16:9"),
            ("r1/v3-short", GROK, "16:9"),
        )
        for stem, size in (
            ("v1-half", (w // 2, h // 2)),
            ("v2-narrow", (w - 1, h)),
            ("v3-short", (w, h - 1)),
        ):
            code, out, _ = run(self.render(stem, size))
            self.assertEqual(code, 1, out)
            self.assertIn(
                f"size: FAIL — {size[0]}x{size[1]} against the largest, {w}x{h}", out
            )
            self.assertIn("render it again at the model's largest size", out)

    def test_an_aspect_past_16_9_fails_a_render_one_pixel_short_542(self):
        for aspect, (w, h) in (("3:2", (2496, 1664)), ("9:16", (1440, 2560))):
            stem = f"v-{aspect.replace(':', '-')}"
            self.logged(
                *((f"r1/{stem}{s}", IDEOGRAM, aspect) for s in ("", "-n", "-s"))
            )
            code, out, _ = run(self.render(stem, (w, h)))
            self.assertEqual(code, 0, out)
            for suffix, size in (("-n", (w - 1, h)), ("-s", (w, h - 1))):
                code, out, _ = run(self.render(stem + suffix, size))
                self.assertEqual(code, 1, out)
                self.assertIn(
                    f"size: FAIL — {size[0]}x{size[1]} against the largest, {w}x{h}",
                    out,
                )
                self.assertIn("render it again at the model's largest size", out)

    def test_a_render_over_its_models_largest_size_passes(self):
        w, h = largest(GROK)
        self.logged(("r1/v1-up", GROK, "16:9"))
        code, out, _ = run(self.render("v1-up", (w * 2, h * 2)))
        self.assertEqual(code, 0, out)

    def test_a_model_or_aspect_with_no_size_row_is_not_judged_with_exit_6(self):
        self.logged(
            ("r1/v1-new", "made-up/model", "16:9"),
            ("r1/v2-web", "nano_banana_2", "16:9"),
            ("r1/v3-square", GROK, "1:1"),
            ("r1/v4-mj", "midjourney/v8.2", "21:9"),
        )
        for stem, why in (
            ("v1-new", "made-up/model has no row in render-sizes.json"),
            ("v2-web", "no largest size on record for nano_banana_2 at 16:9"),
            ("v3-square", f"no largest size on record for {GROK} at 1:1"),
            ("v4-mj", "no largest size on record for midjourney/v8.2 at 21:9"),
        ):
            code, out, _ = run(self.render(stem, (8000, 8000)))
            self.assertEqual(code, 6, out)
            self.assertIn(f"size: NOT JUDGED — {why}", out)
            self.assertNotIn("PASS", out)

    def test_the_model_and_aspect_are_read_from_the_line_whose_candidate_matches(self):
        self.logged(("r1/v1-grok", GROK, "16:9"), ("r1/v2-qwen", QWEN, "16:9"))
        size = largest(QWEN)
        code, out, _ = run(self.render("v1-grok", size), self.render("v2-qwen", size))
        self.assertEqual(code, 1, out)
        lines = out.splitlines()
        self.assertIn(GROK, lines[0])
        self.assertIn("size: FAIL", lines[1])
        self.assertIn(QWEN, lines[2])
        self.assertIn("size: PASS", lines[3])

    def test_a_later_log_line_for_a_candidate_replaces_an_earlier_one(self):
        self.logged(("r1/v1-a", QWEN, "16:9"), ("r1/v1-a", GROK, "16:9"))
        code, out, _ = run(self.render("v1-a", largest(QWEN)))
        self.assertEqual(code, 1, out)
        self.assertIn(GROK, out)

    def test_a_requests_submitted_line_and_its_outcome_read_as_its_one_request(self):
        # #571
        line = {
            "candidate": "r1/v1-a",
            "idempotency_key": "k-1",
            "request_id": "req-1",
            "usd": 0.2,
            "input": {"prompt": "x", "aspect_ratio": "16:9"},
        }
        with open(self.log, "w", encoding="utf8") as f:
            f.write(
                json.dumps({**line, "model": QWEN, "status": "submitted", "files": []})
                + "\n"
            )
            f.write(
                json.dumps(
                    {
                        **line,
                        "model": GROK,
                        "status": "completed",
                        "urls": ["https://cdn.example.com/a.png"],
                    }
                )
                + "\n"
            )
        code, out, _ = run(self.render("v1-a", largest(QWEN)))
        self.assertEqual(code, 1, out)
        self.assertIn(GROK, out)
        self.assertIn("line for r1/v1-a", out)

    def test_log_names_the_spend_log_for_a_render_elsewhere(self):
        self.logged(("r1/v1-grok", GROK, "16:9"))
        elsewhere = os.path.join(self.tmp.name, "out", "r1")
        os.makedirs(elsewhere)
        render = self.render("v1-grok", largest(GROK), folder=elsewhere)
        self.assertEqual(run(render)[0], 6)
        code, out, _ = run(render, "--log", self.log)
        self.assertEqual(code, 0, out)

    def test_model_and_aspect_judge_a_render_with_no_log(self):
        render = self.render("v1-midjourney", largest(GROK))
        code, out, _ = run(render)
        self.assertEqual(code, 6, out)
        self.assertIn("size: NOT JUDGED — no model: give --model", out)
        self.assertEqual(run(render, "--model", GROK)[0], 6)
        code, out, _ = run(render, "--model", GROK, "--aspect", "16:9")
        self.assertEqual(code, 0, out)
        self.assertIn("(no spend log)", out)

    def test_model_and_aspect_override_the_logs(self):
        self.logged(("r1/v1-grok", GROK, "16:9"))
        render = self.render("v1-grok", largest(QWEN))
        self.assertEqual(run(render)[0], 1)
        code, out, _ = run(render, "--model", QWEN)
        self.assertEqual(code, 0, out)
        self.assertIn(f"{QWEN} at 16:9", out)
        code, out, _ = run(render, "--aspect", "1:1")
        self.assertEqual(code, 6, out)
        self.assertIn(f"no largest size on record for {GROK} at 1:1", out)

    def test_a_requests_later_output_reads_its_first_outputs_line(self):
        self.logged(("r1/v1-grok", GROK, "16:9"))
        code, out, _ = run(self.render("v1-grok-2", largest(GROK)))
        self.assertEqual(code, 0, out)
        self.assertIn("line for r1/v1-grok)", out)

    def test_a_log_line_whose_input_is_not_an_object_is_not_judged(self):
        with open(self.log, "w", encoding="utf8") as f:
            f.write(
                json.dumps({"candidate": "r1/v1-a", "model": GROK, "input": "16:9"})
                + "\n"
            )
        code, out, _ = run(self.render("v1-a", largest(GROK)))
        self.assertEqual(code, 6, out)
        self.assertIn("no requested aspect ratio: give --aspect", out)

    def test_a_fault_beside_an_unjudged_render_exits_1(self):
        self.logged(
            ("r1/v1-small", GROK, "16:9"), ("r1/v2-new", "made-up/model", "16:9")
        )
        code, out, _ = run(
            self.render("v1-small", (100, 100)), self.render("v2-new", (100, 100))
        )
        self.assertEqual(code, 1, out)
        self.assertIn("NOT JUDGED", out)

    def test_bad_usage_and_unreadable_files_exit_2(self):
        code, _, err = run()
        self.assertEqual(code, 2)
        self.assertIn("usage: check-render.py", err)
        code, _, err = run(os.path.join(self.round, "missing.png"))
        self.assertEqual(code, 2)
        self.assertIn("cannot read", err)
        self.assertIn("missing.png", err)
        with open(self.log, "w", encoding="utf8") as f:
            f.write("{not json\n")
        code, _, err = run(self.render("v1-a", (10, 10)))
        self.assertEqual(code, 2)
        self.assertIn("higgsfield-spend.jsonl:1 is not JSON", err)
        code, _, err = run(
            self.render("v2-a", (10, 10)),
            "--log",
            os.path.join(self.round, "none.jsonl"),
        )
        self.assertEqual(code, 2)
        self.assertIn("none.jsonl", err)

    def test_a_missing_or_broken_sizes_file_exits_2_not_1(self):
        scripts = os.path.join(self.tmp.name, "plugin", "scripts")
        references = os.path.join(self.tmp.name, "plugin", "references")
        os.makedirs(scripts)
        os.makedirs(references)
        copy = shutil.copy(SCRIPT, scripts)
        shutil.copy(SPEND_LOG, scripts)
        shutil.copy(SIBLINGS, scripts)
        shutil.copy(CRASH_EXIT, scripts)
        shutil.copy(RUNNER, scripts)
        shutil.copy(FAIL_OPEN, scripts)
        render = self.render("v1-a", (10, 10))
        for broken in (
            None,
            "{not json",
            '{"models": {"m": {"sizes": {"16:9": {"size": "big", "source": "docs: x"}}}}}',
        ):
            sizes = os.path.join(references, "render-sizes.json")
            if broken is None:
                shutil.rmtree(references, ignore_errors=True)
            else:
                os.makedirs(references, exist_ok=True)
                with open(sizes, "w", encoding="utf8") as f:
                    f.write(broken)
            out = subprocess.run(
                [sys.executable, copy, render, "--model", "m", "--aspect", "16:9"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(out.returncode, 2, (broken, out.stderr))
            self.assertIn("cannot read", out.stderr)
            self.assertIn("render-sizes.json", out.stderr)


def checkerboard(size, cell=20, tones=((255, 255, 255), (204, 204, 204))):
    import numpy as np

    w, h = size
    ys, xs = np.mgrid[0:h, 0:w]
    grid = ((xs // cell + ys // cell) % 2).astype(bool)
    pixels = np.where(grid[..., None], tones[1], tones[0]).astype(np.uint8)
    image = Image.fromarray(pixels)
    ImageDraw.Draw(image).ellipse(
        [w // 3, h // 4, 2 * w // 3, 3 * h // 4], fill=(200, 30, 30)
    )
    return image


REMEDY = r"checkerboard: FAIL — .*: render it again on one loud plain colour and cut it out with cutout\.py"


class Checkerboard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scaled = tempfile.TemporaryDirectory()
        cls.reals = {}

    @classmethod
    def tearDownClass(cls):
        cls.scaled.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def save(self, name, image):
        path = os.path.join(self.tmp.name, name)
        image.save(path)
        return path

    def check(self, path, *flags):
        return run(path, "--model", GROK, "--aspect", "16:9", *flags)

    def real(self, fixture):
        if fixture not in self.reals:
            w, h = largest(GROK)
            with Image.open(os.path.join(HERE, fixture)) as image:
                size = (w, w) if image.width == image.height else (w, h)
                path = os.path.join(self.scaled.name, os.path.basename(fixture))
                image.convert("RGB").resize(size).save(path)
            self.reals[fixture] = path
        return self.reals[fixture]

    def flat(self):
        image = Image.new("RGB", largest(GROK), (246, 238, 220))
        ImageDraw.Draw(image).ellipse([900, 300, 1900, 1300], fill=(20, 50, 110))
        return self.save("v1-flat.png", image)

    def test_a_painted_checkerboard_fails_332(self):
        for cell in (8, 20, 40):
            render = self.save(f"v{cell}.png", checkerboard(largest(GROK), cell))
            code, out, _ = self.check(render, "--transparent")
            self.assertEqual(code, 1, out)
            self.assertIn("size: PASS", out)
            found = re.search(
                r"checkerboard: FAIL — \d+ of \d+ tiles hold a painted two-tone grid "
                r"of about (\d+) px cells, within \d+,\d+ to \d+,\d+: render it again "
                r"on one loud plain colour and cut it out with cutout.py",
                out,
            )
            self.assertIsNotNone(found, out)
            self.assertLessEqual(
                abs(int(found[1]) - cell), CELL_SLACK_PX + cell * CELL_SLACK_SHARE, out
            )

    def test_a_dark_checkerboard_fails_too(self):
        dark = checkerboard(largest(GROK), 16, ((40, 40, 40), (90, 90, 90)))
        code, out, _ = self.check(self.save("v1.png", dark), "--transparent")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, REMEDY)

    def test_a_clean_flat_ground_passes(self):
        code, out, _ = self.check(self.flat(), "--transparent")
        self.assertEqual(code, 0, out)
        self.assertRegex(
            out, r"checkerboard: PASS — 0 of \d+ tiles hold a two-tone grid"
        )

    def test_a_grid_too_faint_to_see_passes(self):
        faint = checkerboard(largest(GROK), 20, ((255, 255, 255), (254, 254, 254)))
        code, out, _ = self.check(self.save("v1.png", faint), "--transparent")
        self.assertEqual(code, 0, out)

    def test_real_grok_renders_that_painted_a_checkerboard_fail(self):
        for name in (
            "fixtures/render/grok-checker-mascot.png",
            "fixtures/render/grok-checker-palm.png",
        ):
            code, out, _ = self.check(self.real(name), "--transparent")
            self.assertEqual(code, 1, (name, out))
            self.assertRegex(out, REMEDY)

    def test_real_grok_renders_with_no_checkerboard_pass(self):
        for name in (
            "fixtures/render/grok-cream-mascot.png",
            "fixtures/render/grok-courtyard.png",
        ):
            code, out, _ = self.check(self.real(name), "--transparent")
            self.assertEqual(code, 0, (name, out))
            self.assertIn("checkerboard: PASS", out)

    def test_without_transparent_no_checkerboard_finding_is_printed(self):
        for render in (
            self.save("v1.png", checkerboard(largest(GROK))),
            self.real("fixtures/render/grok-checker-mascot.png"),
        ):
            code, out, _ = self.check(render)
            self.assertEqual(code, 0, out)
            self.assertNotIn("checkerboard", out)

    def test_grid_lookalikes_pass(self):
        import numpy as np

        w, h = largest(GROK)
        ys, xs = np.mgrid[0:h, 0:w]
        for name, grey in (
            ("dots", 128 + 100 * np.cos(xs / 6) * np.cos(ys / 6)),
            ("stripes", np.where((ys // 24) % 2, 230, 180)),
            ("noise", np.random.default_rng(2).integers(0, 255, (h, w))),
        ):
            render = self.save(f"{name}.png", Image.fromarray(grey.astype(np.uint8)))
            code, out, _ = self.check(render, "--transparent")
            self.assertEqual(code, 0, (name, out))

    def test_a_render_with_real_alpha_is_read_over_white(self):
        painted = checkerboard(largest(GROK)).convert("RGBA")
        code, out, _ = self.check(self.save("opaque.png", painted), "--transparent")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, REMEDY)
        painted.putalpha(0)
        code, out, _ = self.check(self.save("alpha.png", painted), "--transparent")
        self.assertEqual(code, 0, out)

    def test_a_render_smaller_than_a_tile_is_not_judged(self):
        render = self.save("v1.png", checkerboard((100, 100), 10))
        code, out, _ = run(
            render, "--model", "made-up/model", "--aspect", "1:1", "--transparent"
        )
        self.assertEqual(code, 6, out)
        self.assertIn("checkerboard: NOT JUDGED — under 192 px a side", out)

    def test_a_checkerboard_beside_an_unjudged_size_exits_1(self):
        render = self.save("v1.png", checkerboard((1200, 800)))
        code, out, _ = run(
            render, "--model", "made-up/model", "--aspect", "3:2", "--transparent"
        )
        self.assertEqual(code, 1, out)
        self.assertIn("size: NOT JUDGED", out)
        self.assertRegex(out, REMEDY)

    def test_missing_numpy_exits_3_only_with_transparent(self):
        render = self.flat()
        hide_numpy = (
            "import runpy, sys; sys.modules['numpy'] = None; "
            "sys.argv = sys.argv[1:]; runpy.run_path(sys.argv[0], run_name='__main__')"
        )
        for flags, code in (([], 0), (["--transparent"], 3)):
            out = subprocess.run(
                [sys.executable, "-c", hide_numpy, SCRIPT, render]
                + ["--model", GROK, "--aspect", "16:9", *flags],
                capture_output=True,
                text=True,
            )
            self.assertEqual(out.returncode, code, out.stderr)
        self.assertIn(
            "numpy is missing — python3 -m pip install --only-binary :all: -r",
            out.stderr,
        )

    def test_a_package_present_but_unimportable_exits_3_naming_it_501_paired_with_missing_numpy(
        self,
    ):
        render = self.flat()
        for package in ("PIL", "numpy"):
            with self.subTest(package=package), tempfile.TemporaryDirectory() as shadow:
                os.mkdir(os.path.join(shadow, package))
                with open(os.path.join(shadow, package, "__init__.py"), "w") as fh:
                    fh.write(f"raise ImportError('shadowed', name={package!r})\n")
                done = subprocess.run(
                    [sys.executable, SCRIPT, render, "--model", GROK]
                    + ["--aspect", "16:9", "--transparent"],
                    capture_output=True,
                    text=True,
                    env={**os.environ, "PYTHONPATH": shadow},
                )
                self.assertEqual(done.returncode, 3, done.stderr)
                self.assertIn(
                    f"check-render.py: {package} is missing — python3 -m pip install --only-binary :all: -r",
                    done.stderr,
                )


class Data(unittest.TestCase):
    def test_every_image_model_on_the_roster_has_a_row_and_every_size_a_source(self):
        with open(SIZES, encoding="utf8") as f:
            models = json.load(f)["models"]
        with open(ROSTER, encoding="utf8") as f:
            roster = f.read()
        section = roster.split("## Image generation")[1].split("\n## ")[0]
        ids = {
            t
            for t in re.findall(r"`([^`\s]+)`", section)
            if re.fullmatch(r"[a-z0-9-]+(/[a-z0-9.\-]+)+", t) and not t.endswith(".js")
        }
        ids |= {"nano_banana_2", "seedream_v4_5", "midjourney/v7"}
        self.assertTrue(
            {GROK, QWEN, "ideogram/v4.0", "marketing-studio/image/sunburst"} <= ids, ids
        )
        self.assertEqual(sorted(ids - set(models)), [])
        self.assertIn("render-sizes.json", section)
        for model, row in models.items():
            self.assertTrue(
                row.get("sizes") or row.get("note"),
                f"{model}: no size and no note saying why",
            )
            for aspect, entry in row["sizes"].items():
                self.assertRegex(aspect, r"^\d+:\d+$", model)
                self.assertRegex(entry["size"], r"^\d+x\d+$", f"{model} {aspect}")
                self.assertRegex(
                    entry["source"], r"^(measured|docs): ", f"{model} {aspect}"
                )


if __name__ == "__main__":
    unittest.main()
