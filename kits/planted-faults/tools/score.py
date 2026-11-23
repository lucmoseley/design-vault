#!/usr/bin/env python3
"""score.py — the planted-fault kit's blinded scorers and tally (built for #224, moved into the repo by #238).

  score.py match  [--jobs 3]   three text-only scorers per (candidate, run): which findings name each known fault
  score.py judge  [--jobs 3]   two scorers per clean candidate, run and page version: real, invented or out of scope
  score.py third  [--jobs 3]   a third scorer, on only the findings the two judges split on
  score.py tally               the shapes' numbers, to results.json and stdout
  each takes --critics (the critics that ran), --runs (default 1,2,3), --cands (candidate names, default all) and
  --passes (the gate passes that ran, default all)

The gate trio's loads (runner.py GATE, #415) are critics here too: their findings are the questions, or under
vault.affordance the parts, that at least two of the three critics of a pass failed (see gate_findings()). Its recall
counts the gate set of the key, the faults gate-plants.py planted for it, and the critic set besides.

A scorer sees findings under shuffled ids, with no critic, shape or severity; the map back sits outside its folder.
Known faults are the planted ones (fixtures/key.json) and the founder's verdicts on these candidates
(past-design-rejections.md Part B).
"""

import argparse
import json
import random
import sys
import pathlib
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import runner

ROOT, WORK = runner.ROOT, runner.WORK
RUNS = [1, 2, 3]
# {gate load: the passes scored}, from --passes as runner.py gate takes it.
PASSES = None
CRITICS = [
    "W",
    "W2",
    "W3",
    "T-function",
    "T-type",
    "T-colour",
    "T-layout",
    "T-trust",
    "C1",
    "C2",
    "C3",
]
SHAPES = {
    "1 one whole-page": ["W"],
    "2 three whole-page": ["W", "W2", "W3"],
    "3 topics + whole-page": [
        "W",
        "T-function",
        "T-type",
        "T-colour",
        "T-layout",
        "T-trust",
    ],
    "4 chain": ["C1", "C2", "C3"],
}
for t in ("T-function", "T-type", "T-colour", "T-layout", "T-trust"):
    SHAPES[f"1 + {t}"] = ["W", t]
SHAPES["1 + W2"] = ["W", "W2"]
SHAPES["1 + W3"] = ["W", "W3"]
SHAPES["1 + T-type + T-layout"] = ["W", "T-type", "T-layout"]
SHAPES["1 + T-type + T-colour"] = ["W", "T-type", "T-colour"]
SHAPES["1 + T-type + T-layout + T-colour"] = ["W", "T-type", "T-layout", "T-colour"]
# #268's load-change test: the whole-page critic's load before the restructure, and after it with the type critic.
SHAPES["268 old"] = ["W0"]
SHAPES["268 new"] = ["W1", "TT1"]
SHAPES["268 new, whole-page alone"] = ["W1"]
# #292's: tier 0's staged records made live, against the live load.
SHAPES["292 live"] = ["WL", "TT1"]
SHAPES["292 live, whole-page alone"] = ["WL"]
SHAPES["292 tier 0 live"] = ["WS", "TS"]
SHAPES["292 tier 0 live, whole-page alone"] = ["WS"]
# #293's: tier 1's staged whole-page records made live, against the live load (#292's new one).
SHAPES["293 tier 1 live"] = ["WT", "TS"]
SHAPES["293 tier 1 live, whole-page alone"] = ["WT"]
# #294's: the tone lens and tone lines, against #293's live load.
SHAPES["294 tone line"] = ["WN", "TN"]
SHAPES["294 tone line, whole-page alone"] = ["WN"]
SHAPES["294 lean tone lens"] = ["WM", "TN"]
SHAPES["294 lean tone lens, whole-page alone"] = ["WM"]
# #502's: vault.visible-nav answered by script, against the store with it answered by the whole-page critic.
SHAPES["502 visible-nav whole-page"] = ["WV0"]
SHAPES["502 visible-nav script"] = ["WV1"]
# #415's: the gate trio on the live look records, and on the live and held ones in passes of at most 20.
SHAPES["415 gate, live"] = ["G-old"]
SHAPES["415 gate, live and held"] = ["G-new"]
# The kit runs no settle critic, which in a round settles every split: two No of three is the nearest stand-in.
GATE_VOTES = 2
KEY = json.load(open(ROOT / "fixtures/key.json"))
B8 = (
    "B8",
    "The page is not built with careful, fitting intention: the exact colours and shades, how busy or loud the "
    "background feels, and the borders are wrong for this client; the page is too busy.",
)
FOUNDER = {
    "r1-v1": [
        (
            "B1",
            "The page has a childish feel, the opposite of what a trusted senior lawyer wants to project, and "
            "it looks ugly.",
        ),
        B8,
    ],
    "r1-v2": [
        (
            "B2",
            "The page feels too 'in-your-face techy': it reads as an engineer's or architect's practice, but "
            "Mark is a legal advisor, not an engineer.",
        ),
        B8,
    ],
    "r1-v3": [
        ("B3", "The font and the phrasing of the text box are childish."),
        (
            "B4",
            "The page's colours do not mesh with the colours of Mark's own logo (blue, and black or grey).",
        ),
    ],
    "r1-v5": [
        ("B6", "The whole page feels boring, as if it would put a visitor to sleep.")
    ],
    "r2-v1": [
        (
            "B9",
            "The thin line around the edge of the page reads as a strange box for no reason.",
        )
    ],
    "r2-v7": [
        ("B10", "The photograph of Mark looks poorly cut out from its background.")
    ],
}
FOUNDER["r2-v1p"] = FOUNDER["r2-v1"]
FOUNDER["r2-v7p"] = FOUNDER["r2-v7"]
CLEAN = ["r1-v1", "r1-v2", "r1-v3", "r1-v5", "r2-v1", "r2-v7", "manta-rank"]
CANDS = sorted(runner.CID)


def gate_run():
    return any(c in runner.GATE for c in CRITICS)


def in_play(k):
    """Whether a key entry counts: the gate set only where a gate load is scored, as only its runs cover its pages."""
    return k["candidate"] in CANDS and (k.get("set") != "gate" or gate_run())


def planted():
    return sorted({k["candidate"] for k in KEY if in_play(k)})


def founder_scored():
    """The founder's verdicts are scored where a critic of #224's kind ran; no gate question asks after them."""
    return not all(c in runner.GATE for c in CRITICS)


def scored_cands():
    """The candidates the match scorers read: each with a planted fault, and each the founder judged."""
    founder = (
        [c for c in FOUNDER if c in CANDS and c not in planted()]
        if founder_scored()
        else []
    )
    return planted() + founder


def clean():
    return [c for c in CLEAN if c in CANDS]


def known(cand):
    return [
        (k["id"], k["what"], k.get("kind", k.get("stage")))
        for k in KEY
        if k["candidate"] == cand and in_play(k)
    ] + [(b, what, "founder") for b, what in FOUNDER.get(cand, []) if founder_scored()]


class NotReadyError(Exception):
    pass


def gate_answers(run, load, n, cid):
    """The three critics' answers for one candidate on one pass, each from the one dispatch that held it, and the
    look list that dispatch was given."""
    out, look = [], None
    for critic in runner.GATE_CRITICS:
        found = [
            f
            for f in (WORK / f"runs/r{run}/{load}/p{n}-{critic}").glob("g-*")
            if cid in f.name.split("-")[1:] and (f / "result.json").exists()
        ]
        if not found:
            raise NotReadyError(f"r{run} {load} pass {n} critic {critic} {cid}")
        if len(found) > 1:
            sys.exit(
                f"{cid} was answered in {len(found)} dispatches of r{run} {load} pass {n} critic {critic}: keep one"
            )
        out.append(json.load(open(found[0] / "result.json"))["parsed"]["answers"][cid])
        look = found[0] / "look.txt"
    return out, runner.gate_questions(look)


def said(rows, answer):
    return [r for r in rows if str(r.get("answer", "")).lower() == answer]


def affordance_findings(src, answers, parts):
    """vault.affordance's findings, as gate.js affordanceRow() reads the panel: a part whose look, by at least
    GATE_VOTES, disagrees with whether parts-map.py found it actable, or whose link goes nowhere. A part that acts but
    does not look it, where a part that does look actable goes to the same place, is a minor case and no finding.
    `unlisted` is not read: in a round only a settle critic rules on it."""
    rows = {p["id"]: [a["parts"].get(p["id"], {}) for a in answers] for p in parts}
    looks = {}
    for p in parts:
        r = rows[p["id"]]
        looks[p["id"]] = (
            True
            if len(said(r, "yes")) >= GATE_VOTES
            else False
            if len(said(r, "no")) >= GATE_VOTES
            else None
        )
    passing = {
        p["href"]
        for p in parts
        if p["actable"] and p["href"] and looks[p["id"]] is True
    }
    out = []
    for p in parts:
        if p["dead"]:
            fault = "is a link that goes nowhere"
        elif looks[p["id"]] is None or looks[p["id"]] == p["actable"]:
            continue
        elif p["actable"]:
            if p["href"] in passing:
                continue
            fault = "can be acted on but does not look it"
        else:
            fault = "looks actable but does nothing"
        evidence = " / ".join(
            r.get("evidence", "") for r in rows[p["id"]] if r.get("evidence")
        )
        out.append(
            {
                "src": f"{src}:{p['id']}",
                "where": f'the part "{p["text"]}"',
                "fault": f"It {fault}. {evidence}",
                "who_objects": "",
            }
        )
    return out


def gate_findings(cand, run, load):
    """A gate load's findings on one candidate: each question at least GATE_VOTES of a pass's three critics answered
    No, and affordance_findings(). Each is { src, where, fault, who_objects }."""
    cid = runner.CID[cand]
    parts = json.load(open(WORK / "packets" / cand / "pm/parts.json"))["parts"]
    out = []
    for n in PASSES[load]:
        answers, questions = gate_answers(run, load, n, cid)
        for q, wording in questions.items():
            if q == runner.PARTS_QUESTION:
                out += affordance_findings(
                    f"{load}#{n}:{q}", [a[q] for a in answers], parts
                )
                continue
            no = said([a[q] for a in answers], "no")
            if len(no) >= GATE_VOTES:
                where = " / ".join(r.get("evidence", "") for r in no)
                out.append(
                    {
                        "src": f"{load}#{n}:{q}",
                        "where": where,
                        "fault": f"Answered No to: {wording}",
                        "who_objects": "",
                    }
                )
    return out


def gather(cand, run, critics):
    cid = runner.CID[cand]
    out = []
    for c in critics:
        if c in runner.GATE:
            out += gate_findings(cand, run, c)
            continue
        f = WORK / f"runs/r{run}/{c}/{cid}/result.json"
        if not f.exists():
            raise NotReadyError(str(f))
        for i, x in enumerate(json.load(open(f))["parsed"]["findings"]):
            out.append(
                {
                    "src": f"{c}#{i}",
                    "where": x.get("where", ""),
                    "fault": x.get("fault", ""),
                    "who_objects": x.get("who_objects", ""),
                }
            )
    return out


def ids_file(folder):
    """The map from a scorer's shuffled ids back to critics and faults, beside the scorer's folder so the scorer
    cannot read it (#238)."""
    return folder.parent / f"{folder.name}.ids.json"


def blind(findings, seed):
    random.Random(seed).shuffle(findings)
    ids = {f"f{i + 1}": f["src"] for i, f in enumerate(findings)}
    shown = [
        {"id": f"f{i + 1}", **{k: f[k] for k in ("where", "fault", "who_objects")}}
        for i, f in enumerate(findings)
    ]
    return ids, shown


MATCH_PROMPT = """You are scoring a test of design critics. Several critics judged one web page. The page holds some known faults. Your working folder holds `faults.json` (the known faults, each with an id) and `findings.json` (every finding the critics made, each with an id, in a shuffled order).

For each known fault, list every finding that names it: the same deficiency in the same part of the page, even where the finding words it differently, names more places, or explains the cause another way. A finding that only names the same part or area but a different deficiency does not count, and neither does one that only names a general quality the fault would also break. A broad judgement of the whole page (for example "too busy", "boring", "childish", "reads as an engineering firm") counts where the finding makes that same judgement in substance. One finding may name more than one known fault.

Read both files, then reply with only one JSON object in a ```json fence: {"matches": {"<fault id>": ["<finding id>", ...]}}, every fault id present, an empty list where no finding names it."""

JUDGE_PROMPT = """You are scoring a test of design critics. Several critics judged one candidate web page, and you judge their findings. Your working folder holds `brief.md` (the brief and the project's rules), `shots/` (the page rendered: `desktop-NN.png` slices at 1440 px, `phone-NN.png` slices at 390 px), `parts.txt` (what each part of the page does, read from its DOM: trust it over the render for whether a part can be acted on) and `findings.json` (the critics' findings, each with an id, in a shuffled order).

Read every file and every image first. Then give each finding one verdict:
- "real": the deficiency is there in the render or the parts map, and a visitor to this page or the client the brief names would plausibly object to it, for the reason the finding gives or another sound one.
- "invented": it is not there (a misread render, a wrong claim about what acts or where a link goes, a part that does not exist), or it is there but is no deficiency: a matter of taste no one would object to, a trait every good page of its kind shares, or something the brief or the project's rules explicitly ask for.
- "out-of-scope": it is about something the critics were told not to judge: a measured value (contrast ratio, line length in characters, tap-target size, focus rings, keyboard use, overflow or reflow, motion timing), a build matter (fonts loading, hosting), or a stand-in photograph itself (its choice, crop or quality) where the brief names stand-ins.

Also group findings that name the same fault: give each finding a group label, the same label for findings that name the same deficiency in the same part, a new label otherwise.

Reply with only one JSON object in a ```json fence: {"verdicts": {"<finding id>": {"verdict": "real | invented | out-of-scope", "group": "g1", "why": "a few words"}}}, every finding id present."""


def match_folder(cand, run, scorer):
    return WORK / f"runs/score/match/{cand}-r{run}-s{scorer}"


def judge_folder(cand, run, version, scorer):
    return WORK / f"runs/score/judge/{cand}-r{run}-{version}-s{scorer}"


def same_findings(folder, found):
    """Refuses a scorer folder whose findings are not the ones gathered now: one a test with other critics left in
    the same work folder, whose answers would be scored as this test's."""
    f = ids_file(folder)
    if f.exists() and set(json.load(open(f))["findings"].values()) != {
        x["src"] for x in found
    }:
        raise NotReadyError(
            f"{folder} scored other findings: give this test its own KIT_WORK"
        )


def _match_job(cand, run, scorer):
    folder = match_folder(cand, run, scorer)
    found = gather(cand, run, CRITICS)
    same_findings(folder, found)
    if not (folder / "result.json").exists():
        folder.mkdir(parents=True, exist_ok=True)
        ids, shown = blind(found, f"{cand}{run}{scorer}")
        ks = known(cand)
        order = list(range(len(ks)))
        random.Random(f"k{cand}{run}{scorer}").shuffle(order)
        kid = {f"K{n + 1}": ks[i][0] for n, i in enumerate(order)}
        json.dump(
            [{"id": f"K{n + 1}", "fault": ks[i][1]} for n, i in enumerate(order)],
            open(folder / "faults.json", "w"),
            indent=1,
        )
        json.dump(shown, open(folder / "findings.json", "w"), indent=1)
        json.dump(
            {"findings": ids, "faults": kid}, open(ids_file(folder), "w"), indent=1
        )
    ok = runner.run_child(folder, MATCH_PROMPT, runner.READ_ONLY, "matches")
    runner.log("match", "ok" if ok else "FAILED", cand, run, scorer)
    return ok


def judge_sets(cand, run):
    """(version, packet, critics): the original page and, where the chain is scored, the two pages its fixes made."""
    chain = WORK / f"runs/r{run}/chain/{runner.CID[cand]}"
    sets = [
        ("orig", WORK / "packets" / cand, [c for c in CRITICS if c not in ("C2", "C3")])
    ]
    if "C2" in CRITICS:
        sets.append(("p1", chain / "packet1", ["C2"]))
    if "C3" in CRITICS:
        sets.append(("p2", chain / "packet2", ["C3"]))
    return sets


def scored_shapes():
    """The shapes whose every critic is scored."""
    return {s: crit for s, crit in SHAPES.items() if set(crit) <= set(CRITICS)}


def _judge_job(cand, run, jset, scorer, *, only=None):
    version, packet, critics = jset
    folder = judge_folder(cand, run, version, scorer)
    found = gather(cand, run, critics)
    if only is not None:
        found = [f for f in found if f["src"] in only]
    same_findings(folder, found)
    if not (folder / "result.json").exists():
        folder.mkdir(parents=True, exist_ok=True)
        import shutil

        # Where a load read the brief with its tone lines, every load's findings are judged against that brief (#294).
        # Residual: an old load's findings are then judged against tone lines its critics never read.
        brief = next(
            (runner.BRIEF[c] for c in critics if c in runner.BRIEF), "brief.md"
        )
        shutil.copy(packet / brief, folder / "brief.md")
        shutil.copy(packet / "parts.txt", folder / "parts.txt")
        shutil.copytree(packet / "shots", folder / "shots", dirs_exist_ok=True)
        ids, shown = blind(found, f"j{cand}{run}{version}{scorer}")
        json.dump(shown, open(folder / "findings.json", "w"), indent=1)
        json.dump({"findings": ids}, open(ids_file(folder), "w"), indent=1)
        if not shown:
            json.dump(
                {"parsed": {"verdicts": {}}, "usage": None},
                open(folder / "result.json", "w"),
            )
            return True
    ok = runner.run_child(folder, JUDGE_PROMPT, runner.READ_ONLY, "verdicts")
    runner.log("judge", "ok" if ok else "FAILED", cand, run, version, scorer)
    return ok


def verdicts(cand, run, version, scorer):
    folder = judge_folder(cand, run, version, scorer)
    ids = json.load(open(ids_file(folder)))["findings"]
    got = json.load(open(folder / "result.json"))["parsed"]["verdicts"]
    return {ids[k]: v for k, v in got.items() if k in ids}


def split_of(cand, run, version):
    a, b = verdicts(cand, run, version, 1), verdicts(cand, run, version, 2)
    return {s for s in a if s in b and a[s]["verdict"] != b[s]["verdict"]} | (
        set(a) ^ set(b)
    )


def tally():
    res = {"match_agreement": {}, "recall": {}, "founder": {}, "judged": {}}
    # Recall: a known fault counts as found by a finding where at least two of three scorers matched them.
    hit = {}  # (cand, run, fault) -> set of finding srcs
    pair_agree = []
    for cand in scored_cands():
        for run in RUNS:
            per = []
            for s in (1, 2, 3):
                folder = match_folder(cand, run, s)
                ids = json.load(open(ids_file(folder)))
                m = json.load(open(folder / "result.json"))["parsed"]["matches"]
                per.append(
                    {
                        (ids["faults"][k], ids["findings"][f])
                        for k, fs in m.items()
                        if k in ids["faults"]
                        for f in fs
                        if f in ids["findings"]
                    }
                )
            votes = Counter(p for s in per for p in s)
            for (fault, src), n in votes.items():
                if n >= 2:
                    hit.setdefault((cand, run, fault), set()).add(src)
            for fault, *_ in known(cand):
                # scorer agreement on "found by each shape's pooled findings", per fault
                for crit in scored_shapes().values():
                    says = [
                        any(f == fault and src.split("#")[0] in crit for f, src in s)
                        for s in per
                    ]
                    pair_agree.append(len(set(says)) == 1)
    res["match_agreement"] = {
        "unanimous_share": round(sum(pair_agree) / max(len(pair_agree), 1), 3),
        "n": len(pair_agree),
    }
    # The critic set's rows by kind, then the gate set's by stage, where it is scored.
    rows = {}
    for k in KEY:
        if in_play(k):
            gate = k.get("set") == "gate"
            for label in (
                (f"gate {k['stage']}", "gate all") if gate else (k["kind"], "all")
            ):
                rows.setdefault(label, []).append((k["candidate"], k["id"]))
    order = sorted(r for r in rows if r != "all" and not r.startswith("gate ")) + [
        "all"
    ]
    order += sorted(r for r in rows if r.startswith("gate ") and r != "gate all") + [
        "gate all"
    ]
    for shape, crit in scored_shapes().items():
        rec = {}
        for kind in [r for r in order if r in rows]:
            faults = rows[kind]
            per_run = [
                sum(
                    any(s.split("#")[0] in crit for s in hit.get((c, r, f), ()))
                    for c, f in faults
                )
                for r in RUNS
            ]
            rec[kind] = {"of": len(faults), "runs": per_run}
        res["recall"][shape] = rec
        fv = (
            [(c, b) for c in clean() for b, _ in FOUNDER.get(c, [])]
            if founder_scored()
            else []
        )
        res["founder"][shape] = {
            "of": len(fv),
            "runs": [
                sum(
                    any(s.split("#")[0] in crit for s in hit.get((c, r, b), ()))
                    for c, b in fv
                )
                for r in RUNS
            ],
            "items": {
                f"{c}:{b}": [
                    any(s.split("#")[0] in crit for s in hit.get((c, r, b), ()))
                    for r in RUNS
                ]
                for c, b in fv
            },
        }
    # Judged: on the clean candidates, a finding's verdict is the two scorers' where they agree, else the third's.
    final = {}  # (cand, run, src) -> (verdict, group)
    agree = [0, 0]
    for cand in clean():
        for run in RUNS:
            for version, _, _ in judge_sets(cand, run):
                a, b = verdicts(cand, run, version, 1), verdicts(cand, run, version, 2)
                third = {}
                t = judge_folder(cand, run, version, 3)
                if (t / "result.json").exists():
                    third = verdicts(cand, run, version, 3)
                for src in set(a) | set(b):
                    va, vb = (
                        a.get(src, {}).get("verdict"),
                        b.get(src, {}).get("verdict"),
                    )
                    agree[0] += va == vb
                    agree[1] += 1
                    v = (
                        va
                        if va == vb
                        else third.get(src, {}).get("verdict", "unresolved")
                    )
                    final[(cand, run, src)] = (
                        v,
                        f"{version}:{a.get(src, b.get(src, {})).get('group')}",
                    )
    res["judge_agreement"] = {
        "share": round(agree[0] / max(agree[1], 1), 3),
        "n": agree[1],
    }
    for shape, crit in scored_shapes().items():
        row = {}
        for v in ("real", "invented", "out-of-scope", "unresolved"):
            per_run = []
            for run in RUNS:
                groups = {
                    (c, g)
                    for (c, r, src), (vv, g) in final.items()
                    if r == run and vv == v and src.split("#")[0] in crit
                }
                per_run.append(round(len(groups) / len(clean()), 2))
            row[v] = per_run
        row["findings_per_clean"] = [
            round(
                sum(
                    1 for (c, r, src) in final if r == run and src.split("#")[0] in crit
                )
                / len(clean()),
                1,
            )
            for run in RUNS
        ]
        res["judged"][shape] = row
    json.dump(res, open(WORK / "results.json", "w"), indent=1)
    show(res)


def show(res):
    print(
        "scorer agreement: match",
        res["match_agreement"],
        " judge",
        res["judge_agreement"],
    )
    for shape in res["recall"]:
        r = res["recall"][shape]
        cells = "  ".join(
            f"{k}={'/'.join(map(str, v['runs']))} of {v['of']}" for k, v in r.items()
        )
        print(f"\n{shape}\n  recall: {cells}")
        f = res["founder"][shape]
        print(f"  founder verdicts: {'/'.join(map(str, f['runs']))} of {f['of']}")
        j = res["judged"][shape]
        print(
            "  clean, per candidate (distinct): "
            + "  ".join(f"{k}={'/'.join(map(str, v))}" for k, v in j.items())
        )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["match", "judge", "third", "tally"])
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--critics", default=",".join(CRITICS), help="the critics that ran")
    ap.add_argument("--runs", default="1,2,3")
    ap.add_argument("--cands", help="candidate names; default all")
    ap.add_argument("--passes", help="the gate passes that ran; default every pass")
    a = ap.parse_args()
    CRITICS[:] = a.critics.split(",")
    RUNS[:] = [int(r) for r in a.runs.split(",")]
    if a.cands:
        CANDS[:] = a.cands.split(",")
    unknown = [c for c in CANDS if c not in runner.CID]
    if unknown:
        ap.error(f"--cands: no candidate {', '.join(unknown)}")
    loads = [c for c in CRITICS if c in runner.GATE]
    global PASSES
    try:
        PASSES = runner.pass_plan(loads, a.passes)
    except ValueError as e:
        ap.error(str(e))
    if a.mode == "tally":
        return tally()
    runner.require_canary()
    with ThreadPoolExecutor(a.jobs) as ex:
        if a.mode == "match":
            jobs = [
                ex.submit(match_job, c, r, s)
                for c in scored_cands()
                for r in RUNS
                for s in (1, 2, 3)
            ]
        elif a.mode == "judge":
            jobs = [
                ex.submit(judge_job, c, r, jset, s)
                for c in clean()
                for r in RUNS
                for jset in judge_sets(c, r)
                for s in (1, 2)
            ]
        else:
            jobs = []
            for c in clean():
                for r in RUNS:
                    for jset in judge_sets(c, r):
                        split = split_of(c, r, jset[0])
                        if split:
                            jobs.append(ex.submit(judge_job, c, r, jset, 3, only=split))
        ok = [j.result() for j in jobs]
    print(f"{sum(ok)} of {len(ok)} finished")


def match_job(cand, run, scorer):
    try:
        return _match_job(cand, run, scorer)
    except (NotReadyError, FileNotFoundError) as e:
        runner.log("not ready", e)
        return False


def judge_job(cand, run, jset, scorer, *, only=None):
    try:
        return _judge_job(cand, run, jset, scorer, only=only)
    except (NotReadyError, FileNotFoundError) as e:
        runner.log("not ready", e)
        return False


if __name__ == "__main__":
    main()
