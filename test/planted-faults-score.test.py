import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCORE = os.path.join(HERE, "..", "kits/planted-faults/tools/score.py")
KEY = os.path.join(HERE, "..", "kits/planted-faults/fixtures/key.json")


def tally(work, cands):
    return subprocess.run(
        [sys.executable, SCORE, "tally", "--critics", "G-old", "--runs", "1"]
        + ["--cands", cands],
        env={**os.environ, "KIT_WORK": str(work)},
        capture_output=True,
        text=True,
    )


def seed(folder, result, ids):
    folder.mkdir(parents=True)
    (folder / "result.json").write_text(json.dumps({"parsed": result}))
    pathlib.Path(f"{folder}.ids.json").write_text(json.dumps(ids))


# #672
class Tally(unittest.TestCase):
    def setUp(self):
        self.work = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.work)

    def test_a_run_cut_to_planted_pages_tallies_recall_and_no_clean_rate(self):
        for s in (1, 2, 3):
            seed(
                self.work / f"runs/score/match/r1-v5g-r1-s{s}",
                {"matches": {"K1": ["f1"]}},
                {
                    "faults": {"K1": "v5g-current"},
                    "findings": {"f1": "G-old#1:vault.colour-look"},
                },
            )
        plants = sum(
            1
            for k in json.load(open(KEY))
            if k["candidate"] == "r1-v5g" and k.get("set") == "gate"
        )
        p = tally(self.work, "r1-v5g")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn(f"gate all=1 of {plants}", p.stdout)
        self.assertIn("no clean page in this run", p.stdout)
        res = json.loads((self.work / "results.json").read_text())
        self.assertEqual(res["judged"], {})

    def test_a_run_with_a_clean_page_tallies_its_judged_rate(self):
        for s in (1, 2):
            seed(
                self.work / f"runs/score/judge/r1-v5-r1-orig-s{s}",
                {"verdicts": {"f1": {"verdict": "invented", "group": "g1"}}},
                {"findings": {"f1": "G-old#1:vault.borrowing"}},
            )
        p = tally(self.work, "r1-v5")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertNotIn("no clean page in this run", p.stdout)
        res = json.loads((self.work / "results.json").read_text())
        self.assertEqual(res["judged"]["415 gate, live"]["invented"], [1.0])


if __name__ == "__main__":
    sys.exit(unittest.main())
