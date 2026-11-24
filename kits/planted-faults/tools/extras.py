"""python3 kits/planted-faults/tools/extras.py <critic> [real|invented|out-of-scope] [<rows>] [--runs 4,5,6] — on clean pages, the judged groups an added critic finds that W does not, with severity and text."""

import argparse
import json
import sys
import pathlib
import random
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import score

ap = argparse.ArgumentParser()
ap.add_argument("critic")
ap.add_argument("want", nargs="?", default="real")
ap.add_argument("rows", nargs="?", type=int, default=12)
score.add_runs(ap)
args = ap.parse_args()
score.use_runs(args.runs)
WORK = score.WORK
add, want = args.critic, args.want
rows = []
for cand in score.CLEAN:
    for run in score.RUNS:
        a, b = (
            score.verdicts(cand, run, "orig", 1),
            score.verdicts(cand, run, "orig", 2),
        )
        t = score.judge_folder(cand, run, "orig", 3)
        third = (
            score.verdicts(cand, run, "orig", 3) if (t / "result.json").exists() else {}
        )
        fin = {}
        for src in set(a) | set(b):
            va, vb = a.get(src, {}).get("verdict"), b.get(src, {}).get("verdict")
            fin[src] = (
                va if va == vb else third.get(src, {}).get("verdict"),
                a.get(src, b.get(src, {})).get("group"),
            )
        wg = {g for s, (v, g) in fin.items() if s.startswith("W#")}
        cid = score.runner.CID[cand]
        found = json.load(open(WORK / f"runs/r{run}/{add}/{cid}/result.json"))[
            "parsed"
        ]["findings"]
        seen = set()
        for s, (v, g) in fin.items():
            c, i = s.split("#")
            if c == add and v == want and g not in wg and g not in seen:
                seen.add(g)
                f = found[int(i)]
                rows.append(
                    (
                        cand,
                        run,
                        f.get("severity"),
                        f.get("where", "")[:50],
                        f.get("fault", "")[:170],
                    )
                )
print(len(rows), "groups;", Counter(r[2] for r in rows))
random.Random(1).shuffle(rows)
for r in rows[: args.rows]:
    print(r)
