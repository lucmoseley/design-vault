# The planted-fault kit

The candidate pages, critic prompts, runner and blinded scorers that #224's critic-shape test built (`docs/research/critic-shape-test.md`). #212 Q8 (A) ships a change in what a critic loads only after a planted-fault test of the old load against the new one, 3 runs each, and this kit is what each such test runs on (#238).

## What it holds

- `fixtures/`: 16 candidate pages. Six are planted copies (`r2-v1p`, `r2-v3p`, `r2-v5p`, `r2-v7p`, `manta-home-p`, `manta-canggu-p`), each with 5 faults, one of each kind: function, global, type, colour-surface and treatment. Seven are clean: round-1 v1, v2, v3 and v5, round-2 v1 and v7, and Manta's `manta-rank`. Three are the gate trio's planted copies of clean pages (`r1-v5g`, `r2-v7g`, `manta-rank-g`, #415), with 14 faults between them, each one a held gate record asks about and no live look question does, over all four stages, ten areas and every pass of the held list.
- `fixtures/key.json`: every planted fault. The gate trio's carry `"set": "gate"`, the held record each breaks, and its stage and area; the critic tests score only the rest.
- `packets/`: each candidate's `brief.md` and `parts.txt` as #224's critics read them, and `meta.json`, the neutral ids (`c01`…`c16`) and personas.
- `prompts/`: `common-head.md` and `common-tail.md` wrap every critic prompt. The critics are `W`, `W2` and `W3` (whole-page), `T-*` (topic), and `C1`–`C3` plus `fixer.md` (the chain). `refs/` holds the rule files as #224 loaded them. `gate.md` is the gate critic's prompt, gate-check.md §3's, and `gate-415/` the two look lists it answers, frozen.
- `tools/`: `runner.py` and `score.py` (below), `snap.py` (renders), `parts-txt.py`, and `misses.py` and `extras.py` (readouts). `plants.py` and `build-packets.py` record how the fixtures and briefs were made. They read sources the kit does not keep. `gate-plants.py` makes the gate trio's copies from the kit's own clean pages, and reruns.
- `baseline-224/runs/`: every #224 critic's and scorer's parsed reply. The chain's fixed-page renders are not kept.
- `results-224.json`: #224's tally. `score.py tally` over `baseline-224/runs/` reproduces it exactly.
- `canary-224.json`: the confinement canary, held on Claude Code 2.1.300.

## The private half

The plant key (`fixtures/key.json`, `tools/plants.py`, `tools/gate-plants.py`), the founder's verdicts B1–B10 and the scorer prompts (`tools/score.py`), and each scorer's id map (`*.ids.json`) never enter a critic's or a scorer's folder. Each child runs confined to its own folder, `<work>/runs/…`. A critic sees only renders, `parts.txt`, `brief.md` and its rules, never the fixture HTML, whose comments name each plant. The chain's fixer gets the HTML with those comments stripped.

#224 kept each scorer's id map inside the scorer's folder, so its clean-page judges could see which critic made each finding.

## Running a test

Everything a run writes goes to the work folder: `$KIT_WORK`, or `.claude/tmp/planted-faults/`, which the scratch sweep clears 24 hours after the last write. Tally before then. `runner.py critics` and `chain` and the scorers refuse to start until `<work>/canary.json` held on the installed Claude Code. `--critics` names the critics that ran (default: all 11 and the chain). It needs the `claude` CLI, and Python with Playwright, Chromium and Pillow. `CRITIC_MODEL` picks the model (default `claude-opus-5-5`).

```sh
node calibration-critic.js --canary --model claude-opus-5-5 --out .claude/tmp/planted-faults/canary.json
python3 kits/planted-faults/tools/runner.py packets                                      # render the 13 packets
python3 kits/planted-faults/tools/runner.py critics --runs 1,2,3 --critics W,T-type      # resumable; stops at a usage limit
python3 kits/planted-faults/tools/runner.py chain --runs 1,2,3                           # shape 4 only
python3 kits/planted-faults/tools/score.py match --critics W,T-type   # 3 text-only scorers per page and run: which findings name each known fault
python3 kits/planted-faults/tools/score.py judge --critics W,T-type   # 2 scorers per clean page, run and version: real, invented or out of scope
python3 kits/planted-faults/tools/score.py third --critics W,T-type   # a third scorer, only where the two split
python3 kits/planted-faults/tools/score.py tally --critics W,T-type   # the numbers of every shape those critics make, to <work>/results.json
python3 kits/planted-faults/tools/runner.py usage    # tokens per child
```

To test a load change, add the new load as a critic: a prompt in `prompts/<name>.md` (or an existing one named in `PROMPT` in `runner.py`), and its rule files' folder in `REFS`, with `None` in `RULES`. Add both loads to `SHAPES` in `score.py`, and name every critic they use in each `--critics`. Run both loads, then score and tally. Refresh `prompts/refs/` from the plugin's references first where the old load is today's rules rather than #224's. Reuse `baseline-224/runs/` as the old load's runs only where its prompts, refs and model are unchanged since #224. Copy it into the work folder, and the runner skips every child already answered.

#268's loads were cut from the rule store with `tools/store-refs.py`, the old one from the skills before the change (73ad55a), the new ones from after it, then compared with `--critics W0,W1,TT1`:

```sh
python3 kits/planted-faults/tools/store-refs.py <skills before> whole-page kits/planted-faults/prompts/refs-268/old
python3 kits/planted-faults/tools/store-refs.py <skills after> whole-page kits/planted-faults/prompts/refs-268/new-w
python3 kits/planted-faults/tools/store-refs.py <skills after> type kits/planted-faults/prompts/refs-268/new-t
```

#292 (tier 0 made live) set its old load, `WL` and TT1, as W1 with today's `house-principles.md` in `refs-292/old-w`, and cut the new one, `WS` and `TS`, from the store with tier 0's records flipped to `live`, then compared with `--critics TT1,WL,WS,TS`:

```sh
python3 kits/planted-faults/tools/store-refs.py plugin/skills whole-page kits/planted-faults/prompts/refs-292/new-w
python3 kits/planted-faults/tools/store-refs.py plugin/skills type kits/planted-faults/prompts/refs-292/new-t
```

Then copy `house-principles.md` and `first-visit-trust.md` from `plugin/skills/design-critique/references/`, and `prompts/refs/lenses.md`, into `new-w`.

#293 (tier 1 made live) took #292's new load, `WS` and `TS`, as its old one. It cut `WT` into `refs-293/new-w` the same way, from a copy of `plugin/skills` with tier 1's whole-page records flipped to `live`, with the same three whole files beside it. The type cut did not change, so `TS` serves both loads. Compared with `--critics WS,WT,TS`.

#294 (the tone line) took `WT` and `TS` as its old load. Its new one reads `brief-tone.md`, which `runner.py packets` writes beside each `brief.md` from `packets/tone-294.json`: a tone line in the dispatch, and for a round's brief a Tone range and one on every direction card. `refs-294/new-w` was cut from #293's store (d22ce0e) with #294's record wording applied, with `tone.md` and the same three whole files beside it. `WN` ran the first lens, which walks every scale and failed the recall bar. `WM` runs the lens that ships, naming only the scales a candidate sits off; `TN` is `TS` on the new briefs. Compared with `--critics WT,TS,WM,TN` in a work folder of its own, since a match scorer keeps the findings it first saw.

#502 (`vault.visible-nav` answered by script) tested a single record leaving the whole-page load, so the type load and the tone briefs serve both sides. `refs-502/old-w` is the `whole-page` cut with the record answered by the whole-page critic, `refs-502/new-w` the same cut with it answered by script (as #311 left it), the two differing by that record alone. Each holds today's `house-principles.md`, `first-visit-trust.md` and `tone.md`, and `prompts/refs/lenses.md`. `WV0` and `WV1` run under `WM`'s prompt and briefs. Compared with `--critics WV0,WV1`. #515 added runs 4–6 of both in a fresh work folder (`--runs 4,5,6` on every tool) and pooled them with #502's.

On #224's runs, a whole-page critic child took about 130k tokens, cache reads included, a topic critic 83k–103k, a judge 84k and a match scorer 32k.

## Testing the gate trio

#415 built this to measure #271's question: do the held gate records catch more once live? The trio runs as gate-check.md has it: each pass of the look list to three fresh critics, each dispatch at most 6 of one project's candidates, each critic given `look.txt` and, per candidate, `brief.md`, `shots/` and parts-map.py's key, never `parts.json` or `parts.txt`. The kit makes no look sheets, so `vault.contacts-look` and `vault.curves-look` go unshown to both loads alike. `G-old` is the list cut from the store's live records, 10 questions in one pass; `G-new` adds the held records with `--staged`, 70 questions in 4 passes. Both are frozen in `prompts/gate-415/` by `gate-lists`; refresh them only where the old load is meant to be today's store.

The kit runs no settle critic. A question is a finding where at least two of a pass's three critics answer No, its wording and their evidence what the scorers read. Under `vault.affordance` a part is a finding where two or more critics agree on its look and the look disagrees with whether the parts map found it actable, or where its link goes nowhere. The match scorers take the gate set and the critic set's faults; the founder's verdicts are not scored, since no gate question asks after them.

```sh
python3 kits/planted-faults/tools/gate-plants.py                 # only after changing a plant: the copies, packets, ids and key's gate set
python3 kits/planted-faults/tools/runner.py gate-lists           # only to re-cut the frozen lists from the store
python3 kits/planted-faults/tools/runner.py packets              # renders the gate pages' packets beside the rest
python3 kits/planted-faults/tools/runner.py gate --runs 1,2,3    # both loads, every pass, all 16 candidates; resumable
python3 kits/planted-faults/tools/score.py match --critics G-old,G-new
python3 kits/planted-faults/tools/score.py judge --critics G-old,G-new
python3 kits/planted-faults/tools/score.py third --critics G-old,G-new
python3 kits/planted-faults/tools/score.py tally --critics G-old,G-new   # recall on the gate set by stage, on the critic set by kind, invented on clean pages
```

Run it in a work folder of its own, `KIT_WORK=<folder>` with `canary.json` copied in: the scorers refuse a folder another test left with other findings. `--loads`, `--passes` (`G-new:3,G-new:4`; a load it does not name runs every pass) and `--cands` (names or ids) cut a run down; give `score.py` the same `--runs`, `--passes` and `--cands` (names) as the run. The full run is 3 runs × (1 + 4 passes) × 3 critics × 7 dispatches, 315 gate children of about 150–170k tokens each on #415's two-candidate dry run, then 27 match scorers per run and 2–3 judges per clean page and run.

