"""extras.py — on clean pages, the judged groups an added critic finds that W does not, with severity and text."""

import json
import sys
import pathlib
import random
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import score

WORK = score.WORK
add = sys.argv[1]
want = sys.argv[2] if len(sys.argv) > 2 else "real"
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
for r in rows[: int(sys.argv[3]) if len(sys.argv) > 3 else 12]:
    print(r)
