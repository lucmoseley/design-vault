# Critic shape on planted faults (#224)

Question: which critic shape finds the most real faults without inventing more? The four shapes: one whole-page critic; it plus two deliberately different whole-page critics; topic critics plus the whole-page critic; or a coarse-to-fine chain of critics.

## Answer

- **The whole-page critic plus one type critic.** It finds more real faults of some kind with no rise in invented faults beyond the run-to-run spread, the test #212 Q1 (A) and Q8 (A) set. On planted faults it catches every type fault and every global fault in all 3 runs, where the whole-page critic alone caught 5 or 6 of 6. On the clean pages, as blind judges score them (§Blind re-judge), it finds 9.4 real faults a page against 7.8, and invents 1.76 a page against 1.43. The rise of 0.33 sits inside the whole-page critic's own spread of 0.43.
- **Shapes 2, 3 and 4 each invent more beyond the spread.** Three whole-page critics and the topic shape catch all 30 planted faults in every run, but invent 3.6 and 5.7 faults a clean page. The chain catches 29 or 30 and invents 2.1.
- **A layout critic alone sits on the bar, and not together with the type critic.** Whole-page plus layout finds 9.6 real faults a page and invents 1.86 (+0.43). Type plus layout together invent 2.19 (+0.76), beyond the spread. The type critic is the one to keep: it adds planted-fault catches (type and global) that the layout critic does not, it invents fewer, and half its extra real faults are P2 (17 of 34) against under a third of the layout critic's (12 of 39).
- **The whole-page critic's misses are scattered, apart from two type-led plants.** It missed 2 or 3 of the 30 planted faults a run, mostly a different one each run. The two it missed in 2 of 3 runs were an article title set louder than the hero, and a subhead set bigger than its title. The type critic caught both in every run.
- **The whole-page critic's remaining function misses are a script's job.** It missed a planted button pointing at `#` in one run. In two of three runs it also missed a real dead link on Manta's how-we-rank page ('Destinations' points at `#destinations`, which the page does not have). `parts-map.py` records each link's `href` but does not check that an in-page target exists. Under #212 Q1 a checkable fault belongs to a script: #236.
- **No shape matches the founder's verdicts well.** Of the 9 verdicts on these pages, the whole-page critic and the chosen set each match 3 or 4 a run, and the best set matches 6. No critic in any run named B3 (a childish font and phrasing) or B6 (a boring page). Of the 33 critic runs on each page, B1 (a childish feel) was named in 2, and B9 (a thin border reads as a strange box) in 1 of the 66 on its two pages. These are judgements of tone, which the brief does not yet state (#204).

## Method

- **Candidates.** 13 pages. 6 carry planted faults: mmm-infra round-2 v1, v3, v5 and v7, and Manta's home and Canggu pages, each with 5 faults, one of each kind: function, global, type, colour and surface, treatment. That is 30 faults. 7 pages have none planted: mmm-infra round-1 v1, v2, v3 and v5, round-2 v1 and v7, and Manta's how-we-rank page. The round-1 pages and round-2 v1 and v7 carry the founder's verdicts B1 to B10 from `docs/research/past-design-rejections.md` Part B. Each page was rendered at 1440 px and 390 px in slices, with an overview image and a parts list from `parts-map.py`. Folders were named by neutral ids, and the plant markers were stripped from the HTML the chain's fixer saw.
- **Critics.** Each critic was a confined headless `claude -p` (claude-opus-5-5) with `calibration-critic.js`'s flags, read-only, given the brief, the renders, the parts list and its own rules. W: the whole-page critic with every rule, reading coarse to fine. W2: another reading order and persona. W3: the full page at once (the overview) against the slices. Topic critics: function, type, colour and surface, layout, and conversion and trust, each with only its topic's references. Chain: C1 (function), C2 (what stands out) and C3 (treatment), with a fixer between passes. The fixer was read-only and replied with edits, which the runner applied before the page was rendered again. Each later pass saw the earlier passes' findings as settled. Every critic ran 3 times on every page: 429 critic runs and 78 fixer runs.
- **Shapes scored.** A shape's findings are the pooled findings of its critics in the same run: shape 1 is W; shape 2 is W, W2 and W3; shape 3 is W plus the five topic critics; shape 4 is C1, C2 and C3. W plus each single extra critic, and W plus pairs of topic critics, were scored from the same runs.
- **Recall.** Three text-only scorers per page and run saw the known faults and every finding, shuffled and with no critic, shape or severity. A fault counts as found by a finding where at least two of the three matched them. The scorers agreed unanimously on 98.2% of fault-by-shape cells.
- **Clean pages.** Two scorers per page, run and page version saw the renders, the parts list and the shuffled findings. They gave each finding a verdict, real, invented or out of scope, and grouped findings that name the same fault. A third scorer judged only the findings the two disagreed on (they agreed on 90.4%). Counts are distinct groups a page. The chain's C2 and C3 were judged on the fixed pages they saw, so their groups are not merged with C1's. This can count one fault twice for shape 4.
- **Spread.** The range across the 3 runs. A set passes where its mean invented count is no more than the whole-page critic's mean plus that critic's range (0.43 a page), and its real catches of some kind rise beyond the spread.
- **Cost.** About 72.5M tokens over 848 child sessions, most of them cache reads, against #224's 7M estimate. That count includes the scorers and the discarded runs of an earlier fixer that edited files. A whole-page critic run used about 130k tokens, a topic critic run about 90k, a chain pass about 100k to 120k and a fixer run about 40k.

## Results

### Planted faults found, per run (of 6 per kind, 30 in all)

| Set | Type | Global | Function | Colour and surface | Treatment | All |
|---|---|---|---|---|---|---|
| 1: whole-page (W) | 6/5/5 | 5/6/5 | 5/6/5 | 6/6/6 | 6/5/6 | 28/28/27 |
| 2: W, W2, W3 | 6/6/6 | 6/6/6 | 6/6/6 | 6/6/6 | 6/6/6 | 30/30/30 |
| 3: W plus five topic critics | 6/6/6 | 6/6/6 | 6/6/6 | 6/6/6 | 6/6/6 | 30/30/30 |
| 4: chain C1, C2, C3 | 6/6/6 | 5/6/5 | 6/6/6 | 6/6/6 | 6/6/6 | 29/30/29 |
| W plus type | 6/6/6 | 6/6/6 | 5/6/5 | 6/6/6 | 6/5/6 | 29/29/29 |
| W plus layout | 6/5/5 | 5/6/5 | 5/6/5 | 6/6/6 | 6/5/6 | 28/28/27 |
| W plus W2 | 6/6/6 | 6/6/6 | 6/6/6 | 6/6/6 | 6/6/6 | 30/30/30 |

### The 7 clean pages, per page (mean over 3 runs, lowest–highest run)

These are the first judges' counts. They could see which critic made each finding; §Blind re-judge scores the same findings blind, and its counts are the ones the answer uses.

| Set | Real faults | Invented | Findings | Founder verdicts matched (of 9) |
|---|---|---|---|---|
| 1: whole-page (W) | 8.3 (7.7–8.9) | 0.90 (0.71–1.14) | 9.2 | 3/3/4 |
| 2: W, W2, W3 | 13.6 (13.3–14.0) | 2.62 (2.00–3.57) | 29.6 | 3/4/6 |
| 3: W plus five topic critics | 14.7 (13.9–15.4) | 4.48 (4.00–4.86) | 29.1 | 6/4/5 |
| 4: chain C1, C2, C3 | 10.1 (9.6–10.4) | 2.10 (1.86–2.29) | 12.3 | 3/3/4 |
| W plus type | 10.2 (9.7–11.0) | 1.10 (0.86–1.29) | 12.8 | 3/3/4 |
| W plus layout | 10.7 (10.1–11.3) | 1.24 (1.14–1.29) | 13.7 | 3/3/4 |
| W plus colour and surface | 9.0 (8.3–9.6) | 1.33 (1.14–1.57) | 11.9 | 5/4/5 |
| W plus function | 8.9 (8.6–9.3) | 1.33 (1.00–1.57) | 12.9 | 3/3/4 |
| W plus conversion and trust | 9.6 (9.1–10.1) | 3.10 (2.57–3.43) | 14.8 | 4/3/4 |
| W plus W2 | 11.8 (11.4–12.3) | 1.95 (1.43–2.57) | 19.7 | 3/4/5 |
| W plus W3 | 11.4 (11.1–11.6) | 1.72 (1.43–2.29) | 19.1 | 3/4/6 |
| W plus type and layout | 12.2 (11.9–13.0) | 1.43 (1.29–1.57) | 17.2 | 3/3/4 |
| W plus type and colour | 10.8 (10.1–11.7) | 1.52 (1.43–1.71) | 15.5 | 5/4/5 |

The whole-page critic's 0.43 spread sets the bar: a set may invent at most 1.33 a page. W plus colour (1.33) and W plus function (1.33) sit at the bar, and their real faults overlap W's range. Every other set is over the bar.

### What the extra critics add on the clean pages (distinct faults W did not name, 21 page-runs)

| Added critic | Real (P1 / P2 / P3) | Invented |
|---|---|---|
| Type | 40 (0 / 20 / 20) | 4 |
| Layout | 50 (0 / 13 / 37) | 7 |
| Colour and surface | 14 (0 / 9 / 5) | 9 |
| Function | 13 (1 / 4 / 8) | 9 |
| Conversion and trust | 28 (0 / 20 / 8) | 46 |
| W2 | 73 (5 / 27 / 41) | 22 |
| W3 | 65 (4 / 29 / 32) | 17 |

The type critic's additions are concrete type faults: a page that breaks its own stated type rules, a name and job title set alike so the title outranks the name, light reading text reversed out of a patterned ground, and straight quotes beside curly ones. W2's and W3's P1 additions are the Manta dead link (above), the round-1 v2 page giving no place to Mark's face, round-1 v1's email never shown as text, round-2 v7's cut-out photograph, and the how-we-rank page never saying what ranks one hostel above another.

## Limits

- **The judges are the critics' model.** "Real" and "invented" on the clean pages are Claude's verdicts, not the founder's. The founder's verdicts are the only human check, and there are 9 of them.
- **The planted faults sit near the ceiling.** With 27 to 30 of 30 caught, the planted set cannot rank the shapes. The clean pages carry most of the result.
- **Small counts.** The whole-page critic invented 19 faults over 21 page-runs, and W plus type 23. The spread rule is the founder's test, not a significance test.
- **One chain shape.** Shape 4 was tested with a read-only fixer and one pass order. A builder that fixes better could change its counts.

## Sources

- #212 Q1 (A) and Q8 (A): the test and its decision rule.
- [critic-shape.md](https://github.com/lucmoseley/design-vault/blob/b4a0b43d5/docs/research/critic-shape.md) (#212): why the published evidence could not decide.
- [look-list-length.md](https://github.com/lucmoseley/design-vault/blob/b4a0b43d5/docs/research/look-list-length.md) (#225): the sibling test on the gate critics.
- `docs/research/past-design-rejections.md` Part B: the founder's verdicts B1 to B10.
- The kit (fixtures, plant key, prompts, runner, scorers, every critic's and scorer's parsed reply) is in `kits/planted-faults/`; `score.py tally` over it reproduces this test's numbers exactly. The kit writes the map from shuffled finding ids back to critics outside the scorer's folder.

## Blind re-judge (#251)

The first clean-page judges were not blind to the critic: each judge's folder held the id map (`ids.json`, such as `T-type#3`), and 132 of the 153 opened it. None of the 108 match scorers opened theirs, so the recall counts stand as first scored. The 42 original-page judges and their third scorers ran again, and no judge could reach its id map: no map sat in any judge's folder, and none of the 63 transcripts names `ids.json`. Each judge saw the same findings, in the same shuffled order and under the same ids, as #224's judge did. Recall and the founder matches come out of `score.py tally` exactly as above. The chain's C2 and C3 verdicts on the fixed pages were not judged again, so only shape 4's C1 findings are blind.

**W plus type still stands.**

| Set | Real, #224 | Real, blind | Invented, #224 | Invented, blind | Over W, blind |
|---|---|---|---|---|---|
| 1: whole-page (W) | 8.3 | 7.8 (7.3–8.1) | 0.90 | 1.43 (1.29–1.71) | — |
| W plus type | 10.2 | 9.4 (8.9–9.7) | 1.10 | 1.76 (1.57–2.00) | +0.33 |
| W plus layout | 10.7 | 9.6 (9.3–9.9) | 1.24 | 1.86 (1.43–2.43) | +0.43 |
| W plus colour and surface | 9.0 | 8.3 (8.0–8.6) | 1.33 | 1.91 (1.43–2.29) | +0.48 |
| W plus function | 8.9 | 8.4 (8.3–8.4) | 1.33 | 1.91 (1.86–2.00) | +0.48 |
| W plus type and layout | 12.2 | 11.0 (10.6–11.1) | 1.43 | 2.19 (1.71–2.71) | +0.76 |
| 4: chain C1, C2, C3 | 10.1 | 10.0 (9.7–10.3) | 2.10 | 2.14 (2.00–2.29) | +0.71 |
| 2: W, W2, W3 | 13.6 | 12.5 (12.1–13.0) | 2.62 | 3.62 (2.57–4.29) | +2.19 |
| 3: W plus five topic critics | 14.7 | 12.9 (12.6–13.3) | 4.48 | 5.67 (5.43–6.00) | +4.24 |

- **The blind judges were stricter on every set.** Of 1,110 findings, 102 changed their final verdict: 73 went from real to invented, 15 from invented to real, and 14 to or from out of scope. The change was even across critics, 7% to 12% of each critic's findings. So knowing the critic did not favour W or the type critic over the others.
- **The bar.** W's spread is again 0.43 a page (3 invented faults over 7 pages), so a set may invent at most 1.86. W plus type invents 1.76 (+0.33). Its real count, 8.9 to 9.7 a run, sits clear of W's 7.3 to 8.1. W plus layout invents exactly 1.86, on the bar, and its real count also clears W's. W plus colour and W plus function now go over the bar. Shape 4 stays over it (+0.71), even with its C2 and C3 verdicts left as #224's judges gave them.
- **#224's reasons for type over layout hold.** Type still adds the planted type and global faults (recall is unchanged), and it invents fewer (1.76 against 1.86). The type critic adds 34 distinct real faults that W did not name, 17 of them P2; the layout critic adds 39, 12 of them P2. Their additions judged invented are 7 and 9.
- **Limits.** This run cannot separate blindness from a second draw of judges, because no judges ran again unblinded. The two blind judges agreed on 86.1% of findings (90.4% in #224), which shows how much one draw moves. The shift is one-sided (73 against 15), which chance alone would not give, but the fresh renders are a second cause: the pages were rendered again from the same fixtures, because #224's renders were not kept.
- **Cost.** 63 judge runs, 5.7M tokens with cache reads, 91k each.
