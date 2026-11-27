#!/usr/bin/env python3
"""Usage: python3 kits/planted-faults/tools/runner.py <mode> …

  runner.py packets                                           render each candidate's packet into the work folder
  runner.py critics --runs 1,2,3 --critics W,W2,... [--cands c05,...] [--jobs 3]
  runner.py chain   --runs 1,2,3 [--cands ...] [--jobs 3]     shape 4: C1, fix, render, C2, fix, render, C3
  runner.py gate-lists                                        freeze the gate trio's two look lists, cut from the rule store
  runner.py gate    --runs 1,2,3 [--loads G-old,G-new] [--passes G-new:3,...] [--cands ...] [--jobs 3]
  runner.py usage                                             token totals of every finished child

Inputs come from the kit (fixtures/, prompts/, packets/); everything a run writes goes to the work folder, $KIT_WORK
or .claude/tmp/planted-faults/. Each critic runs in its own folder, runs/r<k>/<critic>/<cid>/; a gate critic answers
for up to 6 candidates at once, in runs/r<k>/<load>/p<pass>-<a|b|c>/g-<ids>/. Finished children are skipped, so a
rerun resumes. A usage-limit reply stops the run.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import pathlib
import time
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parent.parent
VAULT = ROOT.parents[1]
sys.path.append(str(VAULT / "plugin/skills/design-round/scripts"))
from fail_open import expected, fail_open  # noqa: E402

WORK = pathlib.Path(
    os.environ.get("KIT_WORK") or VAULT / ".claude/tmp/planted-faults"
).resolve()
MODEL = os.environ.get("CRITIC_MODEL", "claude-opus-5-5")
CONFINED = [
    "--print",
    "--restricted",
    "--safe-mode",
    "--strict-mcp-config",
    "--permission-prompts",
    "none",
    "--no-session-persistence",
    "--output-format",
    "stream-json",
    "--verbose",
]
READ_ONLY = ["--tools", "Read,Glob,Grep", "--permission-mode", "dontAsk"]
TIMEOUT = 40 * 60
# #238
FIXROOT = WORK / "chain-work"
META = json.load(open(ROOT / "packets/meta.json"))
CID = META["ids"]
NAME = {v: k for k, v in CID.items()}
RULES = {
    "W": None,
    "W2": None,
    "W3": None,
    "T-function": ["house-principles.md"],
    "T-type": ["text-presentation.md"],
    "T-colour": ["brand-palette.md", "surface-styling.md"],
    "T-layout": ["lenses.md"],
    "T-trust": ["first-visit-trust.md", "lenses.md"],
    "C1": ["house-principles.md"],
    "C2": ["house-principles.md", "lenses.md", "first-visit-trust.md"],
    "C3": ["brand-palette.md", "surface-styling.md", "text-presentation.md"],
    "W0": None,
    "W1": None,
    "TT1": None,
    "WL": None,
    "WS": None,
    "TS": None,
    "WT": None,
    "WN": None,
    "TN": None,
    "WM": None,
    "WV0": None,
    "WV1": None,
}
REFS = {
    "W0": "refs-268/old",
    "W1": "refs-268/new-w",
    "TT1": "refs-268/new-t",
    "WL": "refs-292/old-w",
    "WS": "refs-292/new-w",
    "TS": "refs-292/new-t",
    "WT": "refs-293/new-w",
    "WN": "refs-294/new-w",
    "TN": "refs-292/new-t",
    "WM": "refs-294/new-w",
    "WV0": "refs-502/old-w",
    "WV1": "refs-502/new-w",
}
PROMPT = {
    "WL": "W1",
    "WS": "W1",
    "TS": "TT1",
    "WT": "W1",
    "TN": "TT1",
    "WV0": "WM",
    "WV1": "WM",
}
BRIEF = {c: "brief-tone.md" for c in ("WN", "TN", "WM", "WV0", "WV1")}
# #415
GATE = {"G-old": [], "G-new": ["--staged"]}
GATE_FACTS = ["has-cta"]
GATE_LISTS = ROOT / "prompts/gate-415"
GATE_CRITICS = ("a", "b", "c")
LOOK_LIMIT = 20
# guess, #415
RENDER_TIMEOUT = 300
GATE_GROUP = 6
GATE_SCRIPTS = VAULT / "plugin/skills/design-round/scripts"
STORE = VAULT / "plugin/skills/design-critique/rules"
PARTS_QUESTION = "vault.affordance"
LOOKED = ("yes", "no", "unsure")
QUESTION = re.compile(r"^\d+\. (vault\.[\w-]+)(?: \(script owed\))?: (.+)$", re.M)
EXTRA = {
    "W3": "- `overview.png`: the whole desktop page at once, scaled down.\n",
    "C2": "- `settled.md`: the earlier passes' findings, fixed and settled.\n",
    "C3": "- `settled.md`: the earlier passes' findings, fixed and settled.\n",
}
STOP = threading.Event()
LOG = threading.Lock()


def claude_bin():
    return os.environ.get("WFC_CLAUDE_BIN") or "claude"


def log(*a):
    with LOG:
        print(time.strftime("%H:%M:%S"), *a, flush=True)


def prompt_for(critic, cand):
    head = (
        (ROOT / "prompts/common-head.md")
        .read_text()
        .replace("{EXTRA_FILES}\n", EXTRA.get(critic, ""))
    )
    task = (
        (ROOT / f"prompts/{PROMPT.get(critic, critic)}.md")
        .read_text()
        .replace("{PERSONA}", META["persona"][META["project"][cand]])
    )
    return head + task + (ROOT / "prompts/common-tail.md").read_text()


def fill(folder, critic, packet):
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copy(packet / BRIEF.get(critic, "brief.md"), folder / "brief.md")
    shutil.copy(packet / "parts.txt", folder / "parts.txt")
    shutil.copytree(packet / "shots", folder / "shots", dirs_exist_ok=True)
    if critic == "W3":
        shutil.copy(packet / "overview.png", folder / "overview.png")
    rules = folder / "rules"
    rules.mkdir(exist_ok=True)
    refs = ROOT / "prompts" / REFS.get(critic, "refs")
    for f in RULES[critic] or sorted(os.listdir(refs)):
        shutil.copy(refs / f, rules / f)


def fence(text):
    m = re.findall(r"```json\s*(\{.*?\})\s*```", text or "", re.S)
    if not m:
        m = re.findall(r"(\{.*\})", text or "", re.S)
    for cand in reversed(m):
        try:
            return json.loads(cand)
        except json.JSONDecodeError as e:
            expected(e, "the next candidate is read")
            continue
    return None


def run_child(folder, prompt, flags, expect, *, valid=None):
    done = folder / "result.json"
    if done.exists() and json.load(open(done)).get("parsed") is not None:
        return True
    for attempt in (1, 2):
        if STOP.is_set():
            return False
        t0 = time.time()
        try:
            p = subprocess.run(
                [claude_bin(), *CONFINED, *flags, "--model", MODEL],
                cwd=folder,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=TIMEOUT,
            )
            out = p.stdout
        except subprocess.TimeoutExpired as e:
            fail_open(e, f"{folder.relative_to(WORK)}'s partial transcript is read")
            out = (
                (e.stdout or b"").decode()
                if isinstance(e.stdout, bytes)
                else (e.stdout or "")
            )
        (folder / "transcript.jsonl").write_text(out)
        final = None
        for line in out.splitlines():
            try:
                ev = json.loads(line)
            except json.JSONDecodeError as e:
                expected(e, "the line is skipped")
                continue
            if ev.get("type") == "result":
                final = ev
        if final and final.get("api_error") == "usage_limit_reached":
            log("USAGE LIMIT:", final.get("result"))
            STOP.set()
            return False
        parsed = fence(final.get("result")) if final else None
        missing = (
            valid(parsed) if valid and parsed is not None and expect in parsed else []
        )
        if missing:
            log(
                "incomplete reply",
                folder.relative_to(WORK),
                "attempt",
                attempt,
                missing[:5],
            )
            continue
        if parsed is not None and expect in parsed:
            json.dump(
                {
                    "parsed": parsed,
                    "usage": final.get("usage"),
                    "cost": final.get("total_cost_usd"),
                    "turns": final.get("num_turns"),
                    "secs": round(time.time() - t0),
                    "model": MODEL,
                    "attempt": attempt,
                },
                open(done, "w"),
                indent=1,
            )
            return True
        log(
            "unparsed reply",
            folder.relative_to(WORK),
            "attempt",
            attempt,
            (final or {}).get("result", "")[:200] if final else "no result event",
        )
    return False


def critic_job(run, critic, cid, *, packet=None, settled=None):
    folder = WORK / f"runs/r{run}/{critic}/{cid}"
    if not (folder / "result.json").exists():
        fill(folder, critic, packet or WORK / "packets" / NAME[cid])
        if settled is not None:
            (folder / "settled.md").write_text(settled)
    ok = run_child(folder, prompt_for(critic, NAME[cid]), READ_ONLY, "findings")
    log("done" if ok else "FAILED", f"r{run} {critic} {cid}")
    return ok


def findings_of(run, critic, cid):
    return json.load(open(WORK / f"runs/r{run}/{critic}/{cid}/result.json"))["parsed"][
        "findings"
    ]


def render(page_dir, packet, parts=True):
    packet.mkdir(parents=True, exist_ok=True)
    if (packet / "overview.png").exists():
        return
    idx = page_dir / "index.html"
    shots = packet / "shots"
    if shots.exists():
        shutil.rmtree(shots)
    subprocess.run(
        [sys.executable, str(ROOT / "tools/snap.py"), "shots", str(idx), str(shots)],
        check=True,
        capture_output=True,
        cwd=ROOT,
        timeout=RENDER_TIMEOUT,
    )
    if parts:
        subprocess.run(
            [
                sys.executable,
                str(VAULT / "plugin/skills/design-round/scripts/parts-map.py"),
                str(idx),
                "--out",
                str(packet / "pm"),
            ],
            capture_output=True,
            cwd=VAULT,
            timeout=RENDER_TIMEOUT,
        )
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools/parts-txt.py"),
                str(packet / "pm/parts.json"),
                str(packet / "parts.txt"),
            ],
            check=True,
            cwd=ROOT,
        )
    from PIL import Image
    import glob

    ims = [Image.open(f) for f in sorted(glob.glob(str(shots / "desktop-*.png")))]
    full = Image.new("RGB", (1440, sum(i.height for i in ims)), "white")
    y = 0
    for i in ims:
        full.paste(i, (0, y))
        y += i.height
    full.thumbnail((1568, 1568))
    full.save(packet / "overview.png")


def require_canary():
    f = WORK / "canary.json"
    installed = subprocess.run(
        [claude_bin(), "--version"], capture_output=True, text=True
    ).stdout.split()[:1]
    held = json.load(open(f)) if f.exists() else {}
    if not held.get("held") or [held.get("claude_code")] != installed:
        sys.exit(
            f"no canary held on Claude Code {' '.join(installed) or '?'} in {f}: "
            f"run node calibration-critic.js --canary --model {MODEL} --out {f} first"
        )


def tone_brief(name):
    tone = json.load(open(ROOT / "packets/tone-294.json"))
    brief = (ROOT / "packets" / name / "brief.md").read_text()
    project = tone[META["project"][name]]
    if "cards" not in project:
        line = "(the project's, from its rules file) " + project["line"]
    else:
        card = tone["candidates"][name]
        line = f"(direction card {card}'s Tone) " + project["cards"][card]
        if "\n**Reference** —" not in brief:
            raise ValueError(f"{name}: brief.md has no Reference field")
        brief = brief.replace(
            "\n**Reference** —",
            f"\n**Tone** — {project['brief']}\n\n**Reference** —",
            1,
        )
        for title, tl in project["cards"].items():
            head = f"### {title}\n"
            at = brief.index(head) + len(head)
            evidence = brief.index("\n", brief.index("- **Evidence** —", at)) + 1
            brief = brief[:evidence] + f"- **Tone** — {tl}\n" + brief[evidence:]
    first = brief.index("\n\nStand-ins:")
    return brief[:first] + f"\n\nTone line: {line}" + brief[first:]


def render_packets():
    for name in sorted(CID):
        packet = WORK / "packets" / name
        packet.mkdir(parents=True, exist_ok=True)
        for f in ("brief.md", "parts.txt"):
            shutil.copy(ROOT / "packets" / name / f, packet / f)
        (packet / "brief-tone.md").write_text(tone_brief(name))
        render(ROOT / "fixtures" / name, packet, parts=False)
        log("packet", name)


def settled_text(passes):
    out = ["# Settled by the earlier passes\n"]
    for name, findings, fixes in passes:
        out.append(f"\n## {name}\n")
        by = {f.get("finding"): f for f in fixes}
        if not findings:
            out.append("\nNo faults found.\n")
        for i, f in enumerate(findings):
            fx = by.get(i, {})
            state = "fixed" if fx.get("fixed") else "left as it is"
            out.append(
                f"\n{i + 1}. {f.get('where')}: {f.get('fault')} ({f.get('severity')}). "
                f"Settled, {state}: {fx.get('change', 'no change recorded')}\n"
            )
    return "".join(out)


def fix_job(chain, step, findings):
    folder = chain / f"fix{step}"
    page = folder / "page"
    if not (folder / "result.json").exists():
        page.mkdir(parents=True, exist_ok=True)
        src = chain / (f"fix{step - 1}/page/index.html" if step > 1 else "start.html")
        shutil.copy(src, page / "index.html")
        for d in ("shared", "assets", "manta-assets"):
            if not (folder / d).exists():
                os.symlink(ROOT / "fixtures" / d, folder / d)
        json.dump(findings, open(folder / "findings.json", "w"), indent=1)
    if not findings:
        json.dump(
            {
                "parsed": {"fixes": []},
                "usage": None,
                "note": "no findings, nothing to fix",
            },
            open(folder / "result.json", "w"),
        )
        return True, []
    ok = run_child(folder, (ROOT / "prompts/fixer.md").read_text(), READ_ONLY, "fixes")
    if ok:
        res = json.load(open(folder / "result.json"))
        if "applied" not in res:
            html = (page / "index.html").read_text()
            applied = []
            for e in res["parsed"].get("edits") or []:
                old, new = e.get("old", ""), e.get("new", "")
                n = html.count(old) if old else 0
                if n == 1:
                    html = html.replace(old, new, 1)
                applied.append(n == 1)
            (page / "index.html").write_text(html)
            res["applied"] = applied
            json.dump(res, open(folder / "result.json", "w"), indent=1)
    return ok, (
        json.load(open(folder / "result.json"))["parsed"]["fixes"] if ok else None
    )


def chain_job(run, cid):
    name = NAME[cid]
    chain = FIXROOT / f"r{run}/{cid}"
    keep = WORK / f"runs/r{run}/chain/{cid}"
    chain.mkdir(parents=True, exist_ok=True)
    start = chain / "start.html"
    if not start.exists():
        html = (ROOT / "fixtures" / name / "index.html").read_text()
        start.write_text(
            re.sub(r"/\*\s*(?:v1p|v3p|v5p|v7p|mhp|mcp)-[FGTCR]\s*\*/\s*", "", html)
        )
    passes = []
    packet = WORK / "packets" / name
    for step, critic in enumerate(("C1", "C2", "C3"), 1):
        if not critic_job(
            run,
            critic,
            cid,
            packet=packet,
            settled=settled_text(passes) if passes else None,
        ):
            return False
        found = findings_of(run, critic, cid)
        if step == 3:
            break
        ok, fixes = fix_job(chain, step, found)
        if not ok:
            log("FAILED fix", f"r{run} {cid} step {step}")
            return False
        passes.append(
            (
                f"Pass {step}: {'function' if step == 1 else 'what stands out'}",
                found,
                fixes,
            )
        )
        packet = keep / f"packet{step}"
        render(chain / f"fix{step}/page", packet)
        shutil.copy(WORK / "packets" / name / "brief.md", packet / "brief.md")
        log("rendered", f"r{run} {cid} after fix {step}")
    shutil.copytree(chain, keep, symlinks=True, dirs_exist_ok=True)
    log("chain done", f"r{run} {cid}")
    return True


def gate_lists():
    for load, flags in GATE.items():
        out = GATE_LISTS / load
        out.mkdir(parents=True, exist_ok=True)
        for f in out.glob("look-*.txt"):
            f.unlink()
        cmd = ["node", str(GATE_SCRIPTS / "gate.js"), "list", "--asset", "web-surface"]
        cmd += [x for fact in GATE_FACTS for x in ("--fact", fact)] + flags + ["--look"]
        whole = subprocess.run(
            [*cmd, str(STORE)], capture_output=True, text=True, check=True
        ).stdout
        m = re.search(r"in (\d+) passes of at most", whole)
        if not m and len(QUESTION.findall(whole)) > LOOK_LIMIT:
            sys.exit(
                f"gate.js printed {load}'s list of over {LOOK_LIMIT} questions with no pass count this reads"
            )
        passes = int(m.group(1)) if m else 1
        for n in range(1, passes + 1):
            text = whole
            if passes > 1:
                text = subprocess.run(
                    [*cmd, "--pass", str(n), str(STORE)],
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout
            (out / f"look-{n}.txt").write_text(text)
        log(load, passes, "pass(es),", len(QUESTION.findall(whole)), "questions")


def gate_passes(load):
    return sorted(
        int(f.stem.split("-")[1]) for f in (GATE_LISTS / load).glob("look-*.txt")
    )


def pass_plan(loads, spec):
    plan = {load: gate_passes(load) for load in loads}
    for load in loads:
        if load not in GATE:
            raise ValueError(f"no gate load {load}: one of {', '.join(GATE)}")
    named = {}
    for item in (spec or "").split(",") if spec else []:
        load, _, n = item.partition(":")
        if load not in plan or not n.isdigit() or int(n) not in plan[load]:
            have = "; ".join(f"{k}:1 to {k}:{len(v)}" for k, v in plan.items())
            raise ValueError(f"--passes {item}: not a pass of the loads run ({have})")
        named.setdefault(load, []).append(int(n))
    return {load: sorted(named.get(load, plan[load])) for load in loads}


def gate_questions(look):
    return dict(QUESTION.findall(look.read_text()))


def source(name):
    return META.get("sources", {}).get(name) or re.sub(r"-?p$", "", name)


def gate_groups(cids):
    by = {}
    for cid in sorted(cids):
        by.setdefault(META["project"][NAME[cid]], {}).setdefault(
            source(NAME[cid]), []
        ).append(cid)
    groups = []
    for _, families in sorted(by.items()):
        size = sum(len(f) for f in families.values())
        mine = [
            []
            for _ in range(
                max(-(-size // GATE_GROUP), *(len(f) for f in families.values()))
            )
        ]
        for family in sorted(families.values(), key=lambda f: (-len(f), f)):
            for cid in family:
                min(mine, key=len).append(cid)
        groups += [sorted(g) for g in mine]
    for g in groups:
        if len({source(NAME[c]) for c in g}) < len(g):
            sys.exit(f"gate_groups put two copies of one page in {g}")
    return groups


def parts_key(name):
    pm = WORK / "packets" / name / "pm"
    if not (pm / "key.txt").exists():
        subprocess.run(
            [
                sys.executable,
                str(GATE_SCRIPTS / "parts-map.py"),
                str(ROOT / "fixtures" / name / "index.html"),
                "--out",
                str(pm),
            ],
            check=True,
            capture_output=True,
            cwd=VAULT,
        )
    return pm


def part_ids(name):
    return [
        p["id"]
        for p in json.load(open(WORK / "packets" / name / "pm/parts.json"))["parts"]
    ]


def gate_unanswered(parsed, group, qids):
    answers = parsed.get("answers") if isinstance(parsed.get("answers"), dict) else {}
    missing = []
    for cid in group:
        mine = answers.get(cid) if isinstance(answers.get(cid), dict) else {}
        for q in qids:
            a = mine.get(q)
            if q == PARTS_QUESTION:
                rows = a.get("parts") if isinstance(a, dict) else None
                ok = isinstance(rows, dict) and all(
                    isinstance(rows.get(p), dict)
                    and str(rows[p].get("answer", "")).lower() in LOOKED
                    for p in part_ids(NAME[cid])
                )
            else:
                ok = isinstance(a, dict) and str(a.get("answer", "")).lower() in LOOKED
            if not ok:
                missing.append(f"{cid} {q}")
    return missing


def gate_folder(run, load, n, *, critic, group):
    return WORK / f"runs/r{run}/{load}/p{n}-{critic}/g-{'-'.join(group)}"


def gate_job(run, load, n, *, critic, group):
    folder = gate_folder(run, load, n, critic=critic, group=group)
    if not (folder / "result.json").exists():
        folder.mkdir(parents=True, exist_ok=True)
        shutil.copy(GATE_LISTS / load / f"look-{n}.txt", folder / "look.txt")
        for cid in group:
            packet = WORK / "packets" / NAME[cid]
            (folder / cid).mkdir(exist_ok=True)
            shutil.copy(packet / "brief.md", folder / cid / "brief.md")
            shutil.copytree(
                packet / "shots", folder / cid / "shots", dirs_exist_ok=True
            )
            for f in (packet / "pm").glob("key*"):
                shutil.copy(f, folder / cid / f.name)
    qids = list(gate_questions(folder / "look.txt"))
    ok = run_child(
        folder,
        (ROOT / "prompts/gate.md").read_text(),
        READ_ONLY,
        "answers",
        valid=lambda parsed: gate_unanswered(parsed, group, qids),
    )
    log(
        "done" if ok else "FAILED",
        f"r{run} {load} pass {n} critic {critic} {'-'.join(group)}",
    )
    return ok


def usage():
    tot = {}
    for f in WORK.glob("runs/**/result.json"):
        r = json.load(open(f))
        u = r.get("usage") or {}
        key = f.relative_to(WORK / "runs").parts[1]
        if key == "chain":
            key = "fix"
        t = tot.setdefault(
            key,
            {"n": 0, "in": 0, "cache_read": 0, "cache_write": 0, "out": 0, "secs": 0},
        )
        t["n"] += 1
        t["in"] += u.get("input_tokens", 0)
        t["out"] += u.get("output_tokens", 0)
        t["cache_read"] += u.get("cache_read_input_tokens", 0)
        t["cache_write"] += u.get("cache_creation_input_tokens", 0)
        t["secs"] += r.get("secs", 0)
    for k, t in sorted(tot.items()):
        total = t["in"] + t["cache_read"] + t["cache_write"] + t["out"]
        print(
            f"{k:12} n={t['n']:3}  total/child={total // max(t['n'], 1):>8,}  out/child={t['out'] // max(t['n'], 1):>7,}  "
            f"secs/child={t['secs'] // max(t['n'], 1)}"
        )


def add_runs(ap):
    ap.add_argument(
        "--runs", type=lambda s: [int(r) for r in s.split(",")], default="1,2,3"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "mode", choices=["packets", "critics", "chain", "gate-lists", "gate", "usage"]
    )
    add_runs(ap)
    ap.add_argument(
        "--critics", default="W,W2,W3,T-function,T-type,T-colour,T-layout,T-trust"
    )
    ap.add_argument(
        "--cands",
        help="candidate names or neutral ids; default every candidate, the gate pages only for gate",
    )
    ap.add_argument("--loads", default=",".join(GATE))
    ap.add_argument(
        "--passes", help="<load>:<pass>,...; default every pass of each load"
    )
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    if a.mode == "usage":
        return usage()
    if a.mode == "gate-lists":
        return gate_lists()
    if a.mode == "packets":
        return render_packets()
    require_canary()
    gate_pages = {CID[n] for n in META["gate_pages"]}
    cands = (
        [c if c in NAME else CID.get(c, c) for c in a.cands.split(",")]
        if a.cands
        else []
    )
    if any(c not in NAME for c in cands):
        ap.error(
            f"--cands: no candidate {', '.join(c for c in cands if c not in NAME)}"
        )
    cands = cands or [
        c for c in sorted(NAME) if a.mode == "gate" or c not in gate_pages
    ]
    if a.mode == "gate":
        try:
            plan = pass_plan(a.loads.split(","), a.passes)
        except ValueError as e:
            ap.error(str(e))
    with ThreadPoolExecutor(a.jobs) as ex:
        if a.mode == "critics":
            jobs = [
                ex.submit(critic_job, r, c, cid)
                for r in a.runs
                for c in a.critics.split(",")
                for cid in cands
            ]
        elif a.mode == "gate":
            for cid in cands:
                parts_key(NAME[cid])
            jobs = [
                ex.submit(gate_job, r, load, n, critic=critic, group=group)
                for r in a.runs
                for load, passes in plan.items()
                for n in passes
                for critic in GATE_CRITICS
                for group in gate_groups(cands)
            ]
        else:
            jobs = [ex.submit(chain_job, r, cid) for r in a.runs for cid in cands]
        results = [j.result() for j in jobs]
    print(
        f"{sum(results)} of {len(results)} finished"
        + ("; stopped at the usage limit" if STOP.is_set() else "")
    )
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
