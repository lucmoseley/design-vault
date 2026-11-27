import datetime
import json
import os
import pathlib
import shutil
import sys
import tempfile
import unittest

SCRIPT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "plugin",
    "skills",
    "design-round",
    "scripts",
    "answers-file.py",
)
SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

answers_file = siblings.load(SCRIPTS, "answers-file.py")


class Start(unittest.TestCase):
    def setUp(self):
        self.out = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.out)

    def test_an_earlier_runs_answers_file_and_glob_matches_are_gone(self):
        for name in ("run.json", "shot-320-old.png", "shot-640-old.png", "keep.png"):
            (self.out / name).write_text("{}")
        _, path = answers_file.start(self.out, "run.json", "shot-*-*.png")
        self.assertEqual(path, str(self.out / "run.json"))
        self.assertEqual(sorted(p.name for p in self.out.iterdir()), ["keep.png"])

    def test_a_missing_folder_is_made_and_the_stamp_is_utc_to_the_second(self):
        out = self.out / "new" / "deeper"
        when, _ = answers_file.start(out, "run.json")
        self.assertTrue(out.is_dir())
        self.assertEqual(when.tzinfo, datetime.timezone.utc)
        self.assertEqual(when.microsecond, 0)


class Write(unittest.TestCase):
    def test_url_and_run_at_come_first_then_the_fields_in_the_order_given(self):
        with tempfile.TemporaryDirectory() as out:
            when, path = answers_file.start(out, "run.json")
            answers_file.write(
                path, "file:///p.html", when, parts={"é": ".a"}, answers={"x": "pass"}
            )
            text = pathlib.Path(path).read_text(encoding="utf8")
        got = json.loads(text)
        self.assertEqual(list(got), ["url", "run_at", "parts", "answers"])
        self.assertEqual(datetime.datetime.fromisoformat(got["run_at"]), when)
        self.assertIn('"é"', text)
        self.assertTrue(text.endswith("}\n"))

    def test_a_write_with_no_answers_is_refused(self):
        with tempfile.TemporaryDirectory() as out:
            when, path = answers_file.start(out, "run.json")
            with self.assertRaises(TypeError):
                answers_file.write(path, "u", when, findings=[])
            self.assertFalse(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
