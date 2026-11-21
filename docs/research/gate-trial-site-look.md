# Gate trial on mmm-infra's site-look pages (#169)

Ticket: design-vault #169, under spec #154, with the #183 correction. Question: run the gate check on the site-look pages the founder already judged. Does it fail pages he kept? Do its three critics agree? Does it catch the faults he named? Does it catch faults planted on purpose? The founder then rules what to fix before it goes live.

## Method

- **Pages.** 12 pages: mmm-infra round 1 v1–v5 and round 2 v1–v7, from the tags `rounds/site-look-r1` and `rounds/site-look-r2` in lucmoseley/mmm-infra, served locally. Each page was judged once as the founder judged it, plus 9 planted copies (below).
- **Gate.** The vault gate (`plugin/skills/design-critique/gate.md`) at commit c2adeb4, with no project gate, because mmm-infra has none (`projects.mmm-infra.gate` is null). Asset: `web-surface` with facts `has-motion`, `has-cta` and `has-traced-mark`. There were 25 questions per page.
- **Who answered.**
  - Every script question was run from c2adeb4's committed scripts, on all 21 pages.
  - One code reader answered the code questions for the 12 originals. A planted copy takes its source page's code answers.
  - Three fresh critics answered the look questions for each set, with gate-check §3's prompt word for word. Each got screenshots and the parts key (an image numbering every part of the page), never `parts.json`, the script's record of which parts can be clicked.
  - The tally is `gate.js tally --parts`. The critique critic and the fix loop were not run: this trial measures the gate, not a round.
- **Kept pages.** A kept page is one the founder took forward. #183 asks for about 30. Only 2 exist: r2 v1 and r2 v7, which he took forward as round 3's leads. r1 v5 was "in play as a possible base" and is counted as a third in a separate line. No other kept page set exists: searches of mantahostels issues for "founder approved", "signed off", "approved", "design round" and "go with this design" found only approved text (guides, letters), no approved page, the vault's round log holds no pick, and mmm-infra round 3 has not run.
- **Ranges.** Each range is a Wilson 95% interval on the count shown: the span the true rate lies in 19 times out of 20, which suits small counts (`house-audit-critic-panel.md` item 4). Faults cluster by page, so the true uncertainty is wider than shown.
- **Evidence.** The full tallies, critic answers and runs were kept only in the session's gitignored scratch folder and are not preserved. This note quotes the rows each finding rests on.

## Headline 1: kept pages the gate fails

**2 of 2 kept pages fail at least one question: 100% (34%–100%).** Counting r1 v5 as well, it is 3 of 3 (44%–100%).

Why each one fails:

- **r2 v1 (counsel's paper).**
  - Layout fails because the email link falls below the first screen at phone heights. The link is the call to action.
  - Layout also finds one overlap at 765 px.
  - The motion script fails it: the page holds still for 267 ms before its first move, and check-flow counts a still start as a pause "at the start". The code reader passed the same wait.
  - Two look questions go to the founder. On affordance (whether each part looks clickable exactly when it is), one critic named a part the key does not list. On contrast, one critic answered Unsure.
- **r2 v7 (Mark at work).**
  - vault.length fails: 1617 ms measured against the brief's limit of 1.6 s, for a page whose own timeline is about 1050 ms.
  - Layout fails on three counts:
    - The email link is off the first screen at phone heights.
    - The script flags the photo caption that is hidden from sight for screen readers as overlapping, which is a script error.
    - The script flags the heading crossing the photo's edge. The brief chose that overlap, but the script cannot read a brief.
  - Affordance fails because the name "Mark M. Moseley" (p1) looks like a home link but is static (3 Yes).
  - Two questions go to the founder. On contacts, the heading sits over his chin and collar at phone width. On contrast, one critic measured 1.75:1 at phone width.
- **r1 v5.**
  - The motion script fails it for the still start.
  - Borrowing fails because the pull quote is set in the link blue (3 No).

By cause, the 2 kept pages carry 5 failing answers:

- 2 rest only on how a script reads time: the still-start pause on r2 v1 and the length clock on r2 v7.
- 3 have a real cause: both layout fails (the email link below the first screen at phone heights, plus r2 v1's overlap at 765 px) and r2 v7's unlinked name. r2 v7's layout fail also carries two script errors, the hidden caption and the brief-chosen overlap, but its email link fails it without them.

## Headline 2: how often the three critics split

A split, or any Unsure, sends a look question to the founder:

- **Originals:** 14 of 90 look tallies, 16% (9%–24%).
  - Round 1: 10 of 37 (27%, 15%–43%), which is 10 questions to the founder for 5 pages.
  - Round 2: 4 of 53 (8%, 3%–18%), which is 4 questions for 7 pages.
- **Planted copies:** 9 of 67, 13% (7%–24%).
- **All 21 pages:** 23 of 157, 15% (10%–21%).

So under the three-Yes rule (a look question passes only when all three critics answer Yes, and fails only on three No), a round puts about 0.6 to 2 look questions per page to the founder: 4 to 10 a round at this round size.

Under a 2-of-3 rule instead (two matching answers decide; two Unsure, a three-way split or a part off the key still go to him), the same tallies send:

- **Originals:** 3 of 90, 3% (1%–9%). Round 1: 2 of 37 (5%, 1%–18%). Round 2: 1 of 53 (2%, 0%–10%).
- **Planted copies:** 2 of 67, 3% (1%–10%).
- **All 21 pages:** 5 of 157, 3% (1%–7%).

The 2-of-3 rule also fails four questions on two No without his eye: r1 v1 contacts-look and borrowing, r1 v3 curves-look, k5 borrowing. Those two points are the curve he sets the target agreement on.

What sends most of them:

- Affordance, part by part, is the commonest. Often one critic names an extra part or answers Unsure on a label, as on r1 v1, r1 v2, r1 v3, r2 v1 and k3.
- Contacts-look is second, mostly a phone-width view one critic zoomed into and the others did not.

Every look question sent to him, with the vote (Y Yes, N No, U Unsure):

- r1 v1: contacts-look 1Y 2N; affordance, p9 talk title 1Y 2U; borrowing 1Y 2N.
- r1 v2: contacts-look 2Y 1N; affordance, one critic names a part off the key (the ruled lecture box).
- r1 v3: curves-look 1Y 2N; contacts-look 2Y 1N; affordance, p7 "AA" swatch 2Y 1U and p9 "STAND-IN" 2N 1U; primary-action 2Y 1N.
- r1 v5: affordance, p26 pull quote 2N 1U.
- r2 v1: affordance, one critic names "Mark M. Moseley" off the key; contrast (script cannot measure) 2Y 1U.
- r2 v7: contacts-look 2Y 1N; contrast 2Y 1N.
- k3: flow-look 2Y 1U; affordance, p6 "Write to me" 2Y 1U and p9 talk title 2U 1N.
- k5: contacts-look 2Y 1N; borrowing 1Y 2N.
- k7: primary-action 2Y 1N.
- k8: borrowing 2Y 1N.
- k9: curves-look 2Y 1N; affordance, p7 "AA" swatch 1Y 1N 1U and p9 "STAND-IN" 2N 1U; primary-action 2Y 1N.

## Faults the founder named that the gate catches

**0 of 10, 0% (0%–28%).** The 10 are B1–B10 of `past-design-rejections.md` Part B. B11 is a process point, not a fault on a page.

This share is flattered: the critics answered on the very pages the faults were named on, and still caught none.

The vault gate asks no question on tone, audience, colour fit with his existing brand, or the advisor test:

- B1–B3 are "childish" and "too techy".
- B4–B6 and B8 are colour fit, "boring" and busyness.
- B7 is the advisor test.
- B9 is "a strange box".

Those are project questions, and the fit-gate template's (the vault's starter for a project's own questions) audience and advisor questions would aim at B1–B3 and B7.

B10 is the cut-out photo on r2 v7. One critic saw it as Minor, but the gate prompt let it pass as a labelled stand-in.

## Flip test 1: planted faults

Three faults of each type were planted, each on a different source page:

- **Fake button.** A `<span class="btn">` drawn like the page's button, with no link, on k2 (r1 v4), k4 (r2 v5) and k7 (r2 v3).
- **Low-contrast control edge.** An email field with a near-paper border, on k1 (r2 v4), k5 (r1 v2) and k8 (r2 v6).
- **Hidden focus ring.** `outline: none` on the links, on k3 (r1 v1), k6 (r2 v2) and k9 (r1 v3).

Results:

| Plant | Caught | Rate | By |
|---|---|---|---|
| Fake button | 3 of 3 | 100% (44%–100%) | vault.affordance "false" (3 Yes) on k2 p16, k4 p14, k7 p16–p17. One critic also gave k7's primary-action a No, for two identical buttons in one desktop view. |
| Control edge | 3 of 3 | 100% (44%–100%) | vault.control-edges, at 1.21:1 |
| Focus ring | 3 of 3 | 100% (44%–100%) | vault.focus. k9's source was clean. k3 and k6's sources already failed focus, but each plant fails on links its source passed: k3's nav on phone and two body links, k6's brand and nav on desktop. |

For the control edges, "3 of 3" holds only after re-placement. As first placed, only 1 of 3 failed (33%, 6%–79%). On k1 and k5, the field sat flush against a dark or ruled neighbour, and check-access, which reads a field's edge from whichever side contrasts most, took that neighbour's edge as the field's own. With 40 px of space below, all three fail.

The flip rule acts only on this count. The blind count, before any plant was moved, is fake button 3 of 3, focus 3 of 3 and control edge 1 of 3. The two edge misses are a script fault (#220), not a look question missing a fake part, so the function questions stay failing. The edge count is re-taken once #220 lands.

## Flip test 2: critics join the lists without the join script

Three critics got the vault gate, a filled mmm-infra trial gate and three assets: A, a web page; B, still brand art; C, a 12-second canvas logo animation. Each built the question list by hand, and their lists were compared with the join script's: 31, 9 and 16 questions.

- **Critic c** matched all three lists exactly.
- **Critic a** missed 4, 3 and 1 questions: 8 of 56.
- **Critic b** missed 2, 2 and 1: 5 of 56.
- Neither added a question.
- Every miss was a question that applies only when the asset has a certain part:
  - vault.proof, missed by both on every asset;
  - vault.pause;
  - vault.control-edges;
  - vault.end-frame;
  - mmm-infra.marks;
  - mmm-infra.colours-look.

**Exact lists: 3 of 9 critic–asset pairs, 33% (12%–65%).** The join step stays a script.

Two gaps came out of the gate files themselves:

- **A clash in the gate files.** All three critics found mmm-infra.audience at odds with mmm-infra.advisor on tone, and the join script reports the same clash.
- **A gap no question covers.** All three found that vault.pause never reaches a motion asset playing beside page text, such as asset C set into a page.

## Clashes the critics named

- **r1 v3, k9: the brief against vault.borrowing.** The brief asks for "a tabula ansata panel … as the button and the pull quote". vault.borrowing wants each look to mean one function. All three critics named it on r1 v3. Two named it on k9, a copy of r1 v3.
- **r2 v7: the page against its own note.** One critic found the list numbers set in blue, against the page's own note "blue only where clickable".

## Script findings

| # | Finding | Effect in this trial |
|---|---|---|
| 1 | check-flow counts a still start before the first move as a pause. The code reader does not. | Failed 6 of 12 originals, r2 v1 among them. The rule's sources speak only of stills between moves: his "long pauses interspersed with rapid jolts" and Disney's still after which "the flow of action was broken" (`house-audit-craft.md` §1.5). So the script misreads the rule. Fix: #220. |
| 2 | vault.length times from page load, including the font wait. | Failed r1 v3 (1783 ms, own timeline 1400 ms) and r2 v7 (1617 ms, own timeline about 1050 ms) against the brief's 1.6 s. |
| 3 | check-layout counts text hidden from sight for screen readers as overlapping. | A false fail on r2 v7. Fix: #220. |
| 4 | check-layout cannot pass an overlap the brief chose. | A false fail on r2 v7's heading. |
| 5 | check-access reads a control's edge from its best side, so a dark neighbour stands in for the border. | 2 of 3 planted edges were missed at first placement. Fix: #220. |
| 6 | Contrast cannot measure SVG text or logotypes (#189). | Contrast could not be measured on 5 of 12 originals. |
| 7 | At phone width, r2 v2's article nav wraps off its navy band: white on paper, 1.01:1. | A real fault that round 2's critics missed. Script and critics both caught it here. |

Two findings on how the trial ran:

- **9 pages is too many for one critic.** 2 of the 3 planted-set critics ran out of context after 6 pages. Fresh critics did k7–k9, and each critic's two halves were merged.
- **A critic wrote outside its folder.** One round-2 critic wrote a script to `/tmp/still-check-b.py`, outside its scratch folder.

The packet's 1440 shots are 720 px tall, but `look.py` defaults to 900 px. Critics noticed the difference.
