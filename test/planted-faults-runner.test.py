import contextlib
import importlib.util
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "kits", "planted-faults", "tools", "runner.py")
SCORE = os.path.join(HERE, "..", "kits", "planted-faults", "tools", "score.py")
PARTIAL = '{"type":"system","subtype":"init"}\n'
# guess, #586
STUB_SLEEP_S = 30
# guess, #586
TIMEOUT_S = 1
STUB = (
    "#!/usr/bin/env python3\n"
    "import sys, time\n"
    f"sys.stdout.write({PARTIAL!r})\n"
    "sys.stdout.flush()\n"
    f"time.sleep({STUB_SLEEP_S})\n"
)


def load_runner(work):
    with mock.patch.dict(os.environ, {"KIT_WORK": work}):
        spec = importlib.util.spec_from_file_location("planted_faults_runner", SCRIPT)
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
    return runner


# #586
class ChildTimeout(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.work)
        self.runner = load_runner(self.work)
        stub = pathlib.Path(self.work, "claude-stub")
        stub.write_text(STUB)
        stub.chmod(0o755)
        self.env = mock.patch.dict(os.environ, {"WFC_CLAUDE_BIN": str(stub)})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.runner.TIMEOUT = TIMEOUT_S

    def test_a_child_outlasting_the_timeout_fails_open_and_keeps_its_partial_transcript(
        self,
    ):
        folder = pathlib.Path(self.runner.WORK, "runs/r1/W/c01")
        folder.mkdir(parents=True)
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            ok = self.runner.run_child(folder, "prompt", [], "findings")
        self.assertFalse(ok)
        self.assertIn(
            "fail-open: runs/r1/W/c01's partial transcript is read: TimeoutExpired: ",
            err.getvalue(),
        )
        self.assertEqual((folder / "transcript.jsonl").read_text(), PARTIAL)
        self.assertFalse((folder / "result.json").exists())


class ClaudeBin(unittest.TestCase):
    def test_the_bare_name_stands_where_the_var_is_unset(self):
        runner = load_runner(tempfile.gettempdir())
        with mock.patch.dict(os.environ):
            os.environ.pop("WFC_CLAUDE_BIN", None)
            self.assertEqual(runner.claude_bin(), "claude")

    def test_the_bare_name_stands_where_the_var_is_empty(self):
        runner = load_runner(tempfile.gettempdir())
        with mock.patch.dict(os.environ, {"WFC_CLAUDE_BIN": ""}):
            self.assertEqual(runner.claude_bin(), "claude")


# #672
class TallyWithoutCleanPage(unittest.TestCase):
    def test_a_run_cut_to_planted_pages_tallies_recall_and_no_clean_rate(self):
        work = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, work)
        for s in (1, 2, 3):
            folder = work / f"runs/score/match/r1-v5g-r1-s{s}"
            folder.mkdir(parents=True)
            (folder / "result.json").write_text(
                json.dumps({"parsed": {"matches": {"K1": ["f1"]}}})
            )
            pathlib.Path(f"{folder}.ids.json").write_text(
                json.dumps(
                    {
                        "faults": {"K1": "v5g-current"},
                        "findings": {"f1": "G-old#1:vault.colour-look"},
                    }
                )
            )
        p = subprocess.run(
            [sys.executable, SCORE, "tally", "--critics", "G-old", "--runs", "1"]
            + ["--cands", "r1-v5g"],
            env={**os.environ, "KIT_WORK": str(work)},
            capture_output=True,
            text=True,
        )
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("gate all=1 of 5", p.stdout)
        self.assertIn("no clean page in this run", p.stdout)
        res = json.loads((work / "results.json").read_text())
        self.assertEqual(res["judged"], {})


if __name__ == "__main__":
    sys.exit(unittest.main())
