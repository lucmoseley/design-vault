"""The coverage ledger's stop numbers per area, by docs/coverage-ledger-method.md §5. Run: python3 ledger-stop-numbers.py

Prints one line per area: area, rows, observed over Chao2 estimate, saturation median, sample coverage.
"""

import json
import random
from collections import defaultdict
from pathlib import Path


def chao2(rows, t):
    q1 = sum(len(s) == 1 for s in rows)
    q2 = sum(len(s) == 2 for s in rows)
    k = (t - 1) / t
    return len(rows) + (k * q1 * q1 / (2 * q2) if q2 else k * q1 * (q1 - 1) / 2)


def saturation(rows, units, rng, trials=2000):
    shares = []
    for _ in range(trials):
        order = units[:]
        rng.shuffle(order)
        before, last = set(order[:-2]), set(order[-2:])
        found = sum(1 for s in rows if s & before)
        new = sum(1 for s in rows if not s & before and s & last)
        shares.append(new / found if found else 1.0)
    return sorted(shares)[trials // 2]


def coverage(rows, t):
    q1 = sum(len(s) == 1 for s in rows)
    q2 = sum(len(s) == 2 for s in rows)
    u = sum(len(s) for s in rows)
    return 1 - q1 / u * ((t - 1) * q1 / ((t - 1) * q1 + 2 * q2))


ledger = json.load(open(Path(__file__).parent / "docs/coverage-ledger.json"))
# #215
rng = random.Random(215)
by_area = defaultdict(list)
for r in ledger["rows"]:
    if not r["key"].startswith("VG-NEW"):
        by_area[r["area"]].append(set(r["incidence"]))
for area, rows in sorted(by_area.items()):
    units = sorted(set().union(*rows))
    print(
        area,
        len(rows),
        round(len(rows) / chao2(rows, len(units)), 3),
        round(saturation(rows, units, rng), 3),
        round(coverage(rows, len(units)), 3),
    )
