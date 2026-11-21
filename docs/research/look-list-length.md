# Look-list length and the gate critics (#225)

Question: at what length of look list do the three gate critics' answers get worse, and does a split into fresh passes by stage bring them back?

## Answer

- **Recall over all planted faults does not fall beyond the run-to-run spread at 40 questions.** By #212 Q8's test, the list holds to 40.
- **The subtle faults fall at 40 in one pass, and the stage split brings them back to the 20-question level.** For the three hardest plants, critics caught 20 of 27 at 20 questions, 13 of 27 at 40 in one pass, and 17 of 27 split (one-sided Fisher exact test, 40 against 20: p = 0.046). Per run, the 40-question catches (3, 5, 5 of 9) only touch the 20-question range (5, 6, 9 of 9), so this fall sits at the edge of the spread, not beyond it.
- **At 40 in one pass, a missed fault is mostly an Unsure, not a Yes.** The trio then calls the cell a split, so no planted fault passed the trio at any length. The cost is the split load, which reaches the founder (after one fresh critic, once #170 lands #169 Q1 (A)): split cells rose from 5 a round at 20 questions to 20 at 40 in one pass, and fell back to 13 when split (the two questions below that need missing renders are left out of these counts).
- **False No answers stay at or under 0.7% of clean cells at every length, split or not.**
- **Split point: above 20 questions.** 20 is the longest list measured with no sign of decline. Lengths from 21 to 39 were not run. Under #212 Q2 (A), a gate whose look list grows past 20 splits into passes by stage.

## Method

- **Candidates.** Six mmm-infra round-2 pages (`rounds/site-look-r2`): v1 counsel's paper and v2 night drawing left clean, and v3 annotated brief, v4 house dark, v5 house blue field and v6 house portrait with 22 faults planted by a script. Each page was rendered at 1440 px and 390 px wide in slices, with its parts key. Every critic saw the same renders.
- **Plants.** 10 on the six-question core list, 8 more on questions 7–20, and 4 more on questions 21–40. One mid-tier plant was ruled invalid after the runs (below), leaving 21.
- **Lists.** L6: the vault gate's six look questions for this page. L20 and L40: those six plus 14 and 34 questions drafted in `gate.md`'s form for this test only, from the house references. Split: the L40 list cut into a function-and-role pass and a treatment pass of 20 each, each pass a fresh critic.
- **Critics.** Three fresh gate critics a run, with gate-check §3's prompt and inputs, and 3 runs of each condition: 45 dispatches, plus one pilot. The model was claude-opus-5-5. Critics saw renders only, never code, `parts.json` or the plant key.
- **Scoring.** A plant counts as caught by a critic who answers No on its question (or, for `vault.affordance`, mis-reads a planted part). The trio verdict follows `gate.js tally`: three No fail, three Yes pass, anything else goes to the founder. Run-to-run spread is the range across the 3 runs.
- **The clean pages were not clean.** The test-only questions found faults the round-2 pages already had. Every unplanted cell a critic answered No was ruled by the dispatcher from the renders and the page source:
  - **23 faults the pages already had.** They count as faults, not false No answers. Examples: a lone word on the last line of a heading or paragraph on all six pages; article lines of about 86 characters on v1 and v2, against the 75 the question allows; the email address below the first phone screen on v1, v3 and v6; and v2's phone article header, whose paper ground cuts through the logo and hides the navigation.
  - **19 side effects of a plant on another question.** Example: v4's planted amber credential badge also fails `vault.borrowing`. They are excluded from recall and from false No.
  - **12 contested cells.** They are excluded from both counts.
- **Invalid plant.** v3's replay button relabelled 'Motion' renders as an underlined blue text link above a table, not as a button, so `vault.t-button-label` does not reach it. No critic caught it in any condition, and it is excluded.

## Results

### Recall per critic, mean over 3 runs (lowest–highest run)

| Questions asked | L6 | L20 | L40 | Split |
|---|---|---|---|---|
| Core 6: 10 plants | 92% (90–93) | 93% (87–100) | 90% (87–93) | 93% (90–100) |
| Questions 7–20: 7 plants | — | 98% (95–100) | 92% (90–95) | 94% (86–100) |
| Questions 21–40: 4 plants | — | — | 86% (83–92) | 92% (75–100) |
| The pages' own faults, questions 7–40 | — | 98% | 98% | 96% |

### The four plants critics missed (catches out of 9: 3 critics × 3 runs)

| Plant | L6 | L20 | L40 | Split |
|---|---|---|---|---|
| v4: the photo caption box moved 3 px in from the photo's edges (`vault.contacts-look`) | 5 | 5 | 1 | 5 |
| v4: a third type family in the motion notes (`vault.t-font-count`) | — | 8 | 4 | 5 |
| v5: contrast pass or fail shown only by green or red numbers (`vault.colour-look`) | 6 | 7 | 8 | 7 |
| v5: warm and cool greys beside the neutral house grey (`vault.t-grey-temperature`) | — | — | 4 | 6 |

Every other plant was caught by every critic in every condition. At L40 the eight misses on the 3 px caption gap were all Unsure. The other conditions hold four Unsure each.

### What reaches the founder

| | L6 | L20 | L40 | Split |
|---|---|---|---|---|
| Planted faults the trio passed, over 3 runs | 0 | 0 | 0 | 1 (v5 grey temperature, run 2) |
| The pages' own faults the trio passed | 0 | 0 | 0 | 2 (v2 phone navigation) |
| Cells sent to the founder per run, excluding the two ratio questions | 4 (3–5) | 5 (3–7) | 20 (15–24) | 13 (5–19) |
| Cells whose trio verdict changed between runs | 5 / 36 | 12 / 120 | 22 / 240 | 29 / 240 |

### Wrong answers on clean cells

| | L6 | L20 | L40 | Split |
|---|---|---|---|---|
| False No, share of clean cells | 0% | 0% | 0.2–0.3% | 0.1–0.7% |
| `vault.affordance` parts answered against the parts map, per run | 9–10% | 6–10% | 8–14% | 5–7% |

The affordance rate is highest at L40 and lowest split, but the run ranges overlap.

## Other findings

- **Two look questions go to the founder on almost every page, whatever the list length.** `vault.contacts-look` asks for renders at device pixel ratios 1, 2 and 3. `vault.curves-look` asks for an 8× zoom but does not name a render. Critics answered Unsure on most pages, citing one-ratio renders. That gave 10 founder cells a round in every condition, which the counts above leave out. No round script makes a 3× render: `check-frames.py` renders at 1× and 2× only. #228 holds it.
- **A planted-fault test cannot assume its clean pages are clean once questions are added.** A test of a load change (#212 Q8) or of critic shape (#224) has to rule every unplanted No before it counts false No answers.

## Limits

- One page type (one person's site), one model and 3 runs.
- The split ran its two passes in parallel, so the treatment pass never saw function fixes land, as #212 Q2 (A) intends.
- The 34 test-only questions were drafted for this test. A real L40 list from #216's gap-filling will differ.
- The dispatcher ruled the unplanted cells alone. The contested cells are excluded rather than ruled.

## Cost

The 45 dispatches used about 7.9M tokens of final critic context (an L6 critic about 160k, an L40 critic about 195k, a split pair about 335k), far above the ticket's 1–1.5M estimate. The cost comes from images: each critic reads about 80 slices.

## Evidence

Not preserved. It was kept only in gitignored scratch, swept after 24 hours, so the tables here are the record: the renders, lists and answers in `.claude/tmp/ll225/` (runs/, gates/, packet/), and the plant script, plant key, rulings (`native.json`) and scorers (`bin/score.py`, `bin/score2.py`) in `.claude/tmp/ll225-private-rescued/`.
