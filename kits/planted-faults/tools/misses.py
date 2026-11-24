"""python3 kits/planted-faults/tools/misses.py [--runs 4,5,6] — per known fault, which critics found it in each run (2-of-3 scorer vote)."""

import argparse
import json
import sys
import pathlib
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import score

ap = argparse.ArgumentParser()
score.add_runs(ap)
score.use_runs(ap.parse_args().runs)
WORK = score.WORK
hit = {}
for cand in score.scored_cands():
    for run in score.RUNS:
        per = []
        for s in (1, 2, 3):
            f = score.match_folder(cand, run, s)
            ids = json.load(open(score.ids_file(f)))
            m = json.load(open(f / "result.json"))["parsed"]["matches"]
            per.append(
                {
                    (ids["faults"][k], ids["findings"][x])
                    for k, xs in m.items()
                    if k in ids["faults"]
                    for x in xs
                    if x in ids["findings"]
                }
            )
        for (fault, src), n in Counter(p for s in per for p in s).items():
            if n >= 2:
                hit.setdefault((cand, run, fault), set()).add(src.split("#")[0])
for cand in score.scored_cands():
    for fid, _what, kind in score.known(cand):
        row = []
        for run in score.RUNS:
            row.append(",".join(sorted(hit.get((cand, run, fid), set()))) or "-")
        print(f"{cand:14} {fid:8} {kind:14} | " + " | ".join(row))
