# #183 audit: the critic panel and process numbers in spec #154

Ticket: lucmoseley/design-vault#183 (parent #154). Date: 14 Oct 2026.

Scope: seven values.

Source labels: **read** (full text read), **read in part**, **abstract** (abstract or listing only), **snippet** (search summary only).

## Lineage that applies to items 1, 2, 3 and 5

All four values came to design work from the correspondence check in lucmoseley/mantahostels. The chain:

1. An agent wrote mantahostels `docs/research/correspondence-draft-quality.md` (10 Oct 2026). Its recommendation 3: "Run three fresh reviewers in parallel ... A rule passes only 3/3; any split or 'Unsure' goes to the founder". Its recommendation 5: "Give the reviewers the last 5–10 as quoted negatives. Every 10 drafts, re-run a reviewer over logged accepted and rejected sentences". Its only panel source is Verga et al. 2024, and it says: "The gain comes from **mixing families**, which a Claude-only repo cannot do."
2. mantahostels#3668 (the founder's ticket) lists "Changes 1–5 from `docs/research/correspondence-draft-quality.md`". Change 3 is "Three independent reviewers ... a rule passes only 3/3". The founder took the agent's recommendation.
3. design-vault#100 round 1, Q3 (A) and Q9 (B), and Q7 (A) ("Critics get the project's last ten entries"), copied the correspondence shape to design. The resolution comment says: "The founder accepted every recommendation in round 1 (13 Oct 2026)". Q3's own reason: "you chose this shape for correspondence".

The narrow re-check of item 2b comes from the same note's recommendation 1 ("After a fix, a fresh reviewer is asked one question"). Each is an agent recommendation that he accepted, two steps removed from its research.

## Item 1. Three fresh critics per look question; pass on three Yes; three No is a fault; a split or any Unsure goes to the founder

**Value and location.**
- Spec #154 §"The critics and the round" and §"The gate list" (`tally`).
- `plugin/skills/design-round/scripts/gate.js:56` (`const CRITICS = 3;`), `gate.js:55` (`["yes", "no", "unsure"]`), `gate.js:335` (`all("yes") ? "pass" : all("no") ? "fault" : "founder"`).

**Ruling.** Yes, on design-vault#100 Q3 (A), 13 Oct 2026. The resolution comment says: "The founder accepted every recommendation in round 1 (13 Oct 2026): Q1 (A), Q2 (A), Q3 (A) ...". **He took the agent's recommendation.** In correspondence (mantahostels#3668, change 3), he also took an agent's recommendation (`correspondence-draft-quality.md` rec. 3, confidence 70 %). No line from him gives his own reason for three, for unanimity or for Unsure. Searches: design-vault "three critics", "unsure", "unanimous", "3/3"; mantahostels "three independent reviewers", "Unsure"; workflow-core "three reviewers". The hits are #100, #154, #160, mantahostels#3668 and #3669. No hit holds a reason from him.

**What the sources say.**

1. **An Unsure exit, and escalation of low-agreement cases to a human, are sourced.**
   - Jung, Brahman and Choi, "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement", ICLR 2025 oral (arXiv:2407.18370; read in part, HTML v1). The judge decides when to trust itself. Below a confidence threshold it gives no label, and the case goes to a stronger judge. Their confidence measure, "Simulated Annotators", is the agreement of N runs of one model, each with a different set of K in-context examples ("K-shot prompting the model for N times and ensembling the results"; K = N = 5 or 3). It had better calibration than the model's own probability or a verbalised confidence (AlpacaEval ECE 0.095 against 0.217 and 0.215). On ChatArena at a target of 85 % human agreement, it reached 85.8 % agreement and covered 63.2 % of cases; the other 36.8 % were escalated. https://arxiv.org/abs/2407.18370 ; https://iclr.cc/virtual/2025/oral/31838
   - Wang et al., "Self-Consistency Improves Chain of Thought Reasoning in Language Models", ICLR 2023 (arXiv:2203.11171; read in part). "the consistency (in terms of % of decodes agreeing with the final aggregated answer) is highly correlated with accuracy ... one can use low consistency as an indicator that the model has low confidence". https://arxiv.org/abs/2203.11171
   - Anthropic, "Demystifying evals for AI agents" (9 Jan 2026; read for #99, V9): allow "Unknown"; "run multiple trials". Strong (first-party).
   - Counter-evidence for humans only: Krosnick et al. 2002, Public Opinion Quarterly 66(3):371–403 (abstract and summaries only): a "no opinion" option did not improve data quality and drew satisficers. No study found tests this for an LLM judge. Judgement: for LLM judges, the Unsure exit stays sourced. The calibration run must count how often each critic says Unsure.

2. **"At least three independent judges" is sourced. "Three" as the best count is not.**
   - Nielsen, "The Theory Behind Heuristic Evaluations", NN/g, 1 Nov 1994 (read): "single evaluators found only 35 percent of the usability problems"; "My recommendation is normally to use three to five evaluators"; "certainly at least three". https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/ . Moran and Gordon, NN/g, 25 Jun 2023 (read): "three to five people should independently evaluate". These are human evaluators who find problems. The union of their findings is the result. The house tally keeps that logic for a pass: one No stops a pass.
   - Wang et al. 2023: the gain from more samples continues to 40, and "a small number of paths (e.g., 5 or 10)" gets "most of the gains". So three is under the starting point that the paper gives for majority voting. Three is enough to see a split. It is too few to settle one by vote.
   - Chen et al., "Are More LLM Calls All You Need?" (arXiv:2403.02419, 2024; abstract read): the accuracy of voting "can first increase but then decrease as a function of the number of LM calls". More calls help on easy queries and hurt on hard ones. So the best count depends on the task, and it can be estimated from a small sample.

3. **The only panel study in the lineage does not apply to a Claude-only panel.** (Correspondence rec. 3 itself cites CheckEval, MT-Bench, run-to-run variance, Pan et al. and Anthropic, and adds: "no evidence that this helps within one family". #99 S1 rates "Panels help by mixing model families" as **Unknown** for a Claude-only panel.)
   - Verga et al., "Replacing Judges with Juries" (arXiv:2404.18796, 2024; read in part, HTML v2). The panel is three models "drawn from three disparate model families (Command R, Haiku, and GPT-3.5)", with max voting on binary judgements. Cohen's κ against humans on NQ: panel 0.763, GPT-4 0.627, the best single small judge 0.749. On HotpotQA, Haiku alone (0.873) was better than the panel (0.867). The panel has "less intra-model bias due to its composition of disjoint model families". The paper tests no other panel size, no same-family panel and no unanimity rule ("a three judge panel often does not produce a clear majority decision"). https://arxiv.org/abs/2404.18796
   - Kim, Garg, Peng and Garg, "Correlated Errors in Large Language Models", ICML 2025 (arXiv:2506.07962; abstract read): models "agree 60% of the time when both models err"; shared provider and architecture drive the correlation. https://arxiv.org/abs/2506.07962
 - Consequence: three runs of one Claude model catch run-to-run noise (#99 V5: a judge repeats its majority verdict only 61–68 % of the time). They do not catch an error that the model makes every time.

4. **The unanimity threshold is not calibrated, and its cost in founder questions is not measured.**
   - Jung et al. set the escalation threshold from a target agreement with human labels, on a calibration set. The house fixes the threshold at 3 of 3 with no target and no calibration.
   - Arithmetic (independent critics; the real critics correlate, so the true split rate is lower than this): if each critic gives the majority answer with probability p, a question goes to the founder with probability 1 − p³ − (1 − p)³. At p = 0.68 (#99's figure) that is 65 %. At p = 0.9 it is 27 %. At p = 0.95 it is 14 %. A round of five candidates and ten look questions has 50 tallies. So the founder gets about 33, 14 or 7 split items per round. #154 does not state this load. The trial's split-rate figure (item 4) is the first measurement of it.

**Disposition: CONFLICTS (in part).**
- Sourced: an Unsure exit; escalation to the founder on low agreement; at least three independent critics; one No stops a pass.
- Conflicts: (a) research gets the panel gain from judges of different model families (Verga) or from different in-context example sets (Jung's Simulated Annotators). The house panel is three runs of one model with the same prompt. (b) Research sets the escalation threshold from a target agreement on labelled cases (Jung). The house fixes "unanimous" with no target. With #99's consistency figure, the rule sends most look tallies to the founder.
- Size of the departure: moderate. The structure stands. Two changes would bring it to the research: give each critic a different subset of the corrections-log examples (Jung's Simulated Annotators, possible with Claude only); and set the threshold, and the critic count, from the trial and the first calibration run against a target agreement that the founder picks. That target is a GAP of the kind "a point to pick on a measured curve": coverage (items the panel settles) against agreement with him. He needs the trial's curve to pick it.

**Bold finding.** **The founder ruled for this panel on #100 Q3 (A) by accepting an agent's recommendation. The only panel study behind it (Verga) got its gain from judges of different model families. The correspondence note said the gain "comes from mixing families, which a Claude-only repo cannot do" and found "no evidence that this helps within one family"; #99's own synthesis rated a Claude-only panel "Unknown". The #100 round told him none of this. The unanimity threshold has no source, and the round did not price its load of founder questions (about 14 per round at a critic consistency of 0.9; about 33 at #99's 0.68).**

**Confidence:** 0.7 that the disposition is right. It moves down if a study shows that same-model panels gain as much as cross-family panels on a visual judge. It moves down also if the trial shows a split rate under about 10 %. Then the unanimity rule costs little and the conflict is only theoretical.

## Item 2. The fix loop: stop after two re-checks; one fresh critic answers one narrow re-check question



**Value and location.**
- Cap: spec #154 §"Fix and re-check" ("stop at the first re-check with no P0 or P1, or after two re-checks"); `plugin/skills/design-round/SKILL.md:186` ("A candidate is done once a critic pass on it finds nothing serious, no P0 or P1 ..., or after two re-checks, whichever comes first").
- Narrow re-check: spec #154 §"Fix and re-check" ("one fresh critic answers only: 'Is this fault gone, and did the change break any other gate question?'"). Not yet in the plugin text that I read (it lands with #160 and #170).

**Ruling.**
- Cap: design-vault#94 Q2 (A), 13 Oct 2026, carried by #109. The founder's words (#94, session 27360c8b): "Accept recommendations, except: Q4 ... Q6 A ...". The cap was not in his exceptions, so **he took the agent's recommendation.** Its source is `docs/research/mmm-infra-site-look-round.md` S3 (agent-written): "Stop at the first such pass, or after two re-checks", confidence 75 % that a P1 floor "would have cut the re-checks by half". S3 records "Founder's words: none on the loop itself".
- Narrow re-check: design-vault#100 Q4 (A), "The founder accepted every recommendation in round 1". **He took the agent's recommendation.**

### 2a. The cap of two re-checks

**What the sources say.**
- Madaan et al., "Self-Refine", NeurIPS 2023 (arXiv:2303.17651; read in part). Score by iteration y0 → y1 → y2 → y3: code optimisation 22.0, 27.0, 27.9, 28.8; sentiment reversal 33.9, 34.9, 36.1, 36.8; constrained generation 29.0, 40.3, 46.7, 49.7. "Most gains(∆) are in the initial iterations"; "the marginal improvement naturally decreases with more iterations"; in multi-aspect tasks quality "can vary during iteration with improvement in one aspect but decline in another". https://arxiv.org/abs/2303.17651
- Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet", ICLR 2024 (arXiv:2310.01798; abstract read): "LLMs struggle to self-correct their responses without external feedback"; accuracy sometimes falls after self-correction. https://arxiv.org/abs/2310.01798
- Duan, Warner, Li and Hartmann, CHI 2024 (arXiv:2403.13139; read in part for #99, V11): a UI critic's accuracy fell from 52 % to 39 % across revision rounds while the design improved.
- arXiv:2604.05839 (read in part for #99, V7): judge score per cycle 5.24 → 5.56 → 5.64 → 5.69. The gain after the second cycle is small.
- Anthropic, "Harness design for long-running application development" (24 Mar 2026; read for #99, V2): "I preferred a middle iteration over the last one".
- House evidence: mmm-infra round two ran 27 re-checks; "Each new critic found smaller things" (`mmm-infra-site-look-round.md` S3).

No source gives "two" as the best number. All sources agree on the shape: most of the gain is in the first one or two passes, and later passes add little or make the critic worse.

**Disposition: SOURCED** (the direction and the order of size). Choosing two rather than one or three is an engineering knob. The measurement that settles it: in the round log, count re-checks that changed a P0 or P1 verdict, by re-check number. If re-check 2 almost never changes one, cut to one.

**Confidence:** 0.75. It moves down if a design-round log shows P0 or P1 faults found first at re-check 2 or later at a rate above about 1 in 10 candidates.

### 2b. One fresh critic answers the narrow re-check

**What the sources say.**
- The narrow form is sourced. Anthropic, "Demystifying evals for AI agents" (read for #99, V9): "grade each dimension with an isolated LLM-as-judge rather than using one to grade all dimensions". Duan CHI 2024: a critic that re-judges whole designs invents faults in later rounds (V11). Self-Refine's error analysis on dialogue (Table 12): of the refinement errors sampled, "ignoring feedback (25%), and introducing a new problem (20%)". Note: #100 Q4 quoted these as shares of all fixes ("ignored feedback 25% of the time"). They are shares of an error sample, so #100 overstated them.
- The single critic is not sourced, and it conflicts with item 1's own evidence. A fault reaches the fix loop only after three of three critics said No. Then one critic's Yes clears it. #99 V5 measured one judge's run-to-run consistency at 61–68 %. The re-check question is harder than the first one, because it also asks "did the change break any other gate question?", which is a whole-list judgement again. The spec gives three critics to every first answer for the reason that one critic's answer is not reliable (#154 user story 10: "so that one critic's leniency cannot pass a fault"). The re-check has the same risk with no guard.
- What research calls optimal: the clearing verdict has the same reliability as the verdict that raised the fault. Either three critics answer the narrow question with the same tally (Jung et al.; item 1), or the fix is checked by a script where a script answers the question. For "did the change break any other gate question", re-run the script and code questions (cheap and exact) and send only the look questions to critics.

**Disposition: CONFLICTS.** The narrow question is sourced. One critic to clear a fault that needed three to raise departs from the spec's own reliability evidence. Size of the departure: a single critic is about as reliable as the panel of one that #99 and #100 Q3 replaced.

**Bold finding.** **The founder ruled on #100 Q4 (A), by accepting an agent's recommendation, that one fresh critic clears a fixed fault. On Q3 (A) in the same round he ruled that three critics must agree before a look question passes, because one critic's answer repeats only 61–68 % of the time. The round did not tell him that Q4 (A) brings back the one-critic verdict that Q3 (A) removed. Q4's evidence line also overstated Self-Refine's 25 % and 20 % figures.**

**Confidence:** 0.7. It moves down if the trial shows that a narrow question gets much higher run-to-run agreement than the full look list (for example above 0.95). Then one critic is close to three.

## Item 3. A calibration run every ten logged rounds

**Value and location.** Spec #154 §"Calibration" ("Due every ten logged rounds since the last calibration run (#100 Q9 (B)). The round-log script prints 'calibration due' when ten rows have landed"). Tickets #167 and #168. Not yet in the plugin (a grep of `plugin/` for "calibration due" finds nothing).

**Ruling.** design-vault#100 Q9 (B), 13 Oct 2026: "The founder accepted every recommendation in round 1". **He took the agent's recommendation.** Its origin is mantahostels `correspondence-draft-quality.md` rec. 5 ("Every 10 drafts, re-run a reviewer"), which gives no source for ten. mantahostels#3680 then defined "Every 10 drafts" as drafts shown to the founder. Q9's priced reason for ten: "mmm-infra ran 4 rounds in about two weeks (#102), so ten logged rounds is weeks to months away". That is a statement of the wait, not a source.

**What the sources say.**
- Anthropic, "Demystifying evals for AI agents" (9 Jan 2026; read for #99): "LLM-based rubrics should be frequently calibrated". No interval is given.
- Shankar et al., "Who Validates the Validators?" (arXiv:2404.12272, 2024; abstract read; the page gives no venue): "users need criteria to grade outputs, but grading outputs helps users define criteria". The human's own criteria drift as he grades. So a calibration against his verdicts goes out of date as his taste and his rules move, not as a count of rounds passes.
- House evidence: the correspondence seeding run (mantahostels#3680) found that 3 of 5 disagreements "came from rule changes you had ruled that had not yet landed" (#100 Q9). So a rule change is a known cause of disagreement.
- No primary source found gives an evidence-based count of judged items or rounds between re-calibrations of an LLM judge. Search run: "LLM-as-a-judge recalibration frequency drift monitoring human agreement" (one search; results seen as a summary only, pages not opened). Vendor and blog pages (Galileo, futureagi, Arthur) give weekly or monthly checks against a labelled set, and re-calibration "on every provider model update". **Weak** (vendor practice, snippet only). The MedJUDGE scoping review (arXiv:2604.25933; snippet only) proposes alerts on a drift above 5 % from a baseline.

**Precision of one run (arithmetic, Wilson 95 % interval).** Ten rounds give about ten founder picks. At 7 of 10 picks agreed, the interval is 0.40–0.89. Per-question agreement has more items (for example 10 rounds × 5 candidates × 10 look questions), but the items cluster within a candidate and a round, so the true precision is between the two. A pick-level figure from one run cannot separate a good critic from a weak one.

**Disposition: NOT A DESIGN CLAIM.** "Ten" is an engineering cadence. It trades tokens (about 200k per run, #100 Q9) against how stale the agreement figure gets. The measurements that settle it:
1. the change in the agreement figure from one run to the next (if two runs in a row agree within their intervals, lengthen the interval);
2. the share of disagreements that turn on a rule change or a model change.
Research (Shankar et al.; the house's own #3680 result) points to two event triggers in addition to the count: a change of the critic's Claude model, and a landed change to a gate question or rules file. The spec has neither trigger. This is a gap in the spec's design, not a conflict with a source about the number ten.

**Confidence:** 0.75 that ten is a knob and not a claim any source can settle. It moves if a source is found that ties a re-calibration interval for LLM judges to a measured drift rate.

## Item 4. The trial: 12 pages of mmm-infra's two site-look rounds

**Value and location.** Spec #154 §"The trial" ("The 12 pages of mmm-infra's two site-look rounds ... round 1's 5 and round 2's 7"); scored on "Headline 1, false fails: a gate fails a page the founder kept or led" and "Headline 2, the rate at which the three critics split". Ticket #169 (acceptance criteria). Two flip tests: one planted fake button on a copy of one page; and the three critics without the joined list.

**Ruling.** design-vault#133, 14 Oct 2026. His first answer: "Accept recommendations", but for Q3 "he expected the trial to use 'the mmm-infra set of 7 design looks, and the animation rounds'". Q3 was re-priced, and he then answered "accept recommendation" on the re-priced Q3 (A), 12 pages. **He took the agent's recommendation, against his own first guess.** Neither round priced the sample size: the confidence lines discuss cost and coverage of fault types, not the precision of the two headline figures.

**How many pages can show a false fail.** The false-fail figure needs pages that he kept or led.
- Round 1 (5 pages): "No tile leads. Round 1 restarts" (mmm-infra#8, his reply of 5 Oct 2026). One follow-up keeps v5 "in play as a possible base".
- Round 2 (7 pages): "The founder chose v1 and v7" (`docs/research/mmm-infra-site-look-round.md` S3; mmm-infra#8 "His reaction to the leaders").
- So the false-fail headline has **2 pages** (3 if v5 of round 1 counts as kept). The other 9 or 10 pages can show splits and caught faults, but not false fails.

**What the sources say (statistics).**
- Brown, Cai and DasGupta, "Interval Estimation for a Binomial Proportion", Statistical Science 16(2):101–133, 2001 (abstract and summaries read): they recommend "the Wilson interval or the equal-tailed Jeffreys prior interval for small n". https://doi.org/10.1214/ss/1009213286
- Hanley and Lippman-Hand, "If nothing goes wrong, is everything all right? Interpreting zero numerators", JAMA 249:1743–1745, 1983 (abstract and summaries read): with 0 events in n trials, the 95 % upper limit is about 3/n. https://jamanetwork.com/journals/jama/article-abstract/389714
- Kish's design effect (Survey Sampling, 1965; textbook formula, not opened here): items that cluster in one page count as fewer independent items, deff = 1 + (m − 1)ρ.

**The intervals that this trial gives (Wilson 95 %, computed here).**

| Figure | n | Result | 95 % interval |
|---|---|---|---|
| False fails, per kept page | 2 | 0 of 2 | 0.00 – 0.66 |
| False fails, per kept page | 2 | 1 of 2 | 0.09 – 0.91 |
| False fails, if all 12 pages counted | 12 | 0 of 12 | 0.00 – 0.24 (rule of three: 0.25) |
| False fails, if all 12 pages counted | 12 | 1 of 12 | 0.01 – 0.35 |
| Split rate, per page | 12 | 4 of 12 | 0.14 – 0.61 |
| Split rate, per tally (12 pages × 4 look questions) | 48 | 16 of 48 | 0.22 – 0.47 (wider in truth, because tallies cluster in a page) |
| Split rate, per tally (12 pages × 10 look questions) | 120 | 40 of 120 | about 0.25 – 0.42 before clustering |

The vault gate has 4 look questions today (`plugin/skills/design-critique/gate.md`: 18 questions, 4 `answered-by: look`). The function questions (#162) add look halves, so 4–10 is the range.

**Sample needed for useful precision (normal approximation, 95 %).**
- To show a false-fail rate is under 10 % when none is seen: about 30 kept pages (3/n ≤ 0.10). Under 5 %: about 60.
- To estimate a split rate near 0.2 to ± 0.10: about 62 independent tallies; near 0.5: about 97. With 4–10 tallies per page and a within-page correlation of 0.2 (an assumption), the design effect is 1.6–2.8. Then 12 pages give about 17–43 effective tallies, which is less than needed for ± 0.10.
- The planted fake button is n = 1. One plant cannot estimate a detection rate. A hit gives an interval of 0.21–1.00 and a miss 0.00–0.79 (Wilson, 1 of 1 or 0 of 1). #154 lets this one result move the function questions to reported-not-failing.

**Disposition: CONFLICTS** for the use that #154 and #169 give the 12 pages: two "headline" figures and a flip rule. As a figure, the false-fail rate rests on 2 kept pages, and its interval is wider than the range of any decision it could change. The split rate is better, but only if counted per tally, with its interval reported. As a qualitative review (the founder reads every disagreement and rules which questions to fix, #133 Q4 (B)), 12 pages are adequate.

What research calls adequate: about 30 kept pages to bound a false-fail rate at 10 %; at least 3–5 planted faults per fault type to estimate a detection rate in any useful way. Ways to get there without new rounds: add pages he approved in other work (Manta pages he signed off; mmm-infra round 3 when it runs), and plant several faults (fake button, low-contrast edge, hidden focus) across several pages.

**Bold finding.** **The founder ruled on #133 Q3 (A), by accepting the re-priced agent recommendation, that 12 pages are the trial. Only 2 of the 12 are pages he kept or led, so the "false fails" headline figure has n = 2 (95 % interval 0–66 % at zero seen). The planted-fault flip test that can demote the function questions has n = 1. Neither round on #133 priced the precision of either figure.**

**Confidence:** 0.85 (arithmetic on counts read from mmm-infra#8). It moves if the trial counts false fails per question on kept pages and the founder accepts that unit. Then n grows, but the items still cluster in 2 pages, so the conclusion stays nearly the same.

## Item 5. Critics read the project's last ten corrections-log entries as quoted examples

**Value and location.** Spec #154 §"Critic inputs" ("the project's last ten corrections-log entries, quoted") and user story 42. `plugin/skills/design-round/SKILL.md:176`: "the project's last ten corrections, each one's `words` quoted beside its `principle` (`jq -c 'select(.project == "<key>")' ... | tail -n 10`)". `data/corrections-log.jsonl` has 0 rows today.

**Ruling.** design-vault#100 Q7 (A), 13 Oct 2026 ("Critics get the project's last ten entries as quoted examples"); "The founder accepted every recommendation in round 1". **He took the agent's recommendation.** Origin: mantahostels `correspondence-draft-quality.md` rec. 5, "Give the reviewers the last 5–10 as quoted negatives", which cites few-shot gains for judges (MT-Bench swap consistency 65.0 % → 77.5 %; Verga κ 0.518 → 0.627) and gives no source for the count or for the "last" rule. Q7's confidence line argues for the log, not for ten or for recency.

**What the sources say.**
- **Count.** No source gives ten.
  - Agarwal et al., "Many-Shot In-Context Learning", NeurIPS 2024 spotlight (arXiv:2404.11018; abstract read): going from few-shot to hundreds or thousands of examples gives "significant performance gains", and "can override pretraining biases". https://arxiv.org/abs/2404.11018
  - The opposite on one person's taste: GPT-4V predicting one rater's aesthetic rating (arXiv:2403.03594; read in part for #99, V10): "more than 3 per class did not help significantly".
  - Jung et al. 2025 (item 1): K = 3 or 5 examples per simulated annotator.
  - So the useful count depends on the task and is measurable. Ten is inside the tested range of every source, and no source says ten is best.
- **Selection by recency.** The sources favour selection by relevance.
  - Liu et al., "What Makes Good In-Context Examples for GPT-3?" (arXiv:2101.06804, DeeLIO 2022; abstract read): examples chosen for semantic closeness to the test input "consistently outperforms the random baseline". https://arxiv.org/abs/2101.06804
  - Jung et al. 2025: different example sets per run make the panel's agreement a calibrated confidence. The spec gives all three critics the same ten.
- **Balance of the examples.** Zhao et al., "Calibrate Before Use", ICML 2021 (arXiv:2102.09690; read in part): models "suffer from majority label bias, recency bias, and common token bias. The majority label and recency biases lead the model to predict training answers that appear frequently or near the end of the prompt"; "When the prompt is unbalanced, the predictions are unbalanced". https://arxiv.org/abs/2102.09690 . The log is written when the founder "rejects a candidate's trait, rewords a brief, or overrules a critic" (#154). Most entries are therefore rejections. Ten rejections in front of a Yes/No question can push the critics toward No. That raises false fails, which is the trial's first headline (item 4). The correspondence check had the same fault in practice: its review found reviewers handed ten entries under "The founder rejected these lines" when six of them were lines he kept (mantahostels#3669, review item 1).

**Disposition: CONFLICTS (in part).**
- The count of ten: an engineering knob (it trades context tokens and dilution against coverage). The calibration run (item 3) can measure it: agreement with 0, 5, 10 and 20 entries.
- The selection rule conflicts with the sources. Research calls for examples chosen by relevance to the candidate (same asset class, same principle or gate question), balanced between kept and rejected verdicts, and, for a panel, a different subset per critic. The house takes the last ten by date, one set for all three critics, with no balance. The departure is moderate: it costs nothing to change in the `jq` line, and the log has no rows yet.

**Bold finding.** **The founder ruled on #100 Q7 (A), by accepting an agent's recommendation, that critics read the last ten entries. The sources favour relevant, balanced examples and a different set per critic. A log of mostly rejections, given to a Yes/No critic, risks a bias toward No (Zhao et al.'s majority label bias). The correspondence check, which this rule copies, already had that fault in review (mantahostels#3669 item 1).**

**Confidence:** 0.65. It moves down if the calibration run shows no change in agreement between "last ten" and "ten most relevant". It moves up if the trial shows that critics who read the log fail kept pages more often than critics who do not.

## Item 6. The building session names 2–3 weakest parts per candidate

**Value and location.** Spec #154 §"Weakest parts" ("For each candidate, the building session names 2–3 parts it is least sure of, and why") and user stories 37–38. Ticket #161. Not yet in the plugin (a grep of `plugin/` for "weakest" and "least sure" finds only an unrelated comment in `check-overlay.py:79`).

**Ruling.** design-vault#100 Q6 (B), 13 Oct 2026: "The founder accepted every recommendation in round 1". The idea is his own: on mantahostels#3698 (11 Oct 2026) he asked for "a selection of sentence and phrase swap-outs for the ones you are least confident in, or where the research suggests multiple good approaches might fit". **The count "2–3" is the agent's** (#100 Q6 (B)); his words give no count. Q6's confidence line: "It matches what you asked for twice in correspondence ... Nothing measures it for design."

**What the sources say.**
- No source gives a count of self-named weak parts for a design candidate. impeccable's own critique lists "Priority Issues (3-5)" and "What's Working (2-3)" (`docs/research/impeccable-checks.md:128`); this is a vendor format, not evidence.
- Whether the maker's own doubt points at the right parts is the real question, and the sources doubt it:
  - Xiong et al., "Can LLMs Express Their Uncertainty?", ICLR 2024 (arXiv:2306.13063; abstract read): verbalised confidence tends "to be overconfident"; failure prediction stays weak (AUROC "0.522 to 0.605" across methods). https://arxiv.org/abs/2306.13063
  - Vasconcelos et al., "Generation Probabilities Are Not Enough: Uncertainty Highlighting in AI Code Completions", ACM TOCHI 2024 (arXiv:2302.07248; abstract read): highlighting the parts most likely to be edited, as learned from real edits, "leads to faster task completion and more targeted edits"; highlighting the model's own low-probability parts "does not provide any benefit over the baseline with no highlighting". https://arxiv.org/abs/2302.07248
  - Anthropic, "Harness design ..." (2026; read for #99): agents "reliably skew positive when grading their own work".
- Consequence: a maker's self-named weak parts may be no better than chance at finding what the founder will reject. A list built from his past edits (the corrections log's `principle` field) is the analogue of Vasconcelos's "likely to be edited" highlight, which did help.

**Disposition: NOT A DESIGN CLAIM.** "2–3" is a knob: a few lines per candidate, read at the reveal. The measurement that settles both the count and the worth of the step: per candidate, the share of the founder's rejected traits (corrections-log rows with that `candidate`) that fall in a named weakest part, against the share expected by chance (named parts ÷ all parts). If the hit rate is near chance after about ten rounds, change the source of the list from the maker's doubt to the corrections log's principles (Vasconcelos), or drop the step.

**Bold finding.** None for the count. Note for the founder: his ruling rests on his own ask, but the evidence above says a model's own doubt is a weak pointer.

**Confidence:** 0.7 that the count is a knob. It moves if a study of self-flagged weak parts in generated designs is found.

## Item 7. At most five function questions to a client per batch

**Value and location.**
- Spec #154 §"The house method" ("The set-up questions S1–S6 go into design-project's first step, in one relay batch with at most five function questions") and user story 59 ("batch at most five client questions per stage").
- `docs/research/function-questions.md:133` ("**at most five function questions** to a client per batch. Confidence 0.6; no source tests the number for this use") and `:238` (the ask-or-infer rule, step 4).
- Ticket #177 (acceptance: "the five-question batch cap"). Not yet in `plugin/skills/design-project/SKILL.md`.
- Note the wording differs: user story 59 says "five client questions", and §"The house method" says "five function questions" in a batch that also holds other items. The two readings give different caps.

**Ruling.** design-vault#101 Q5 (A), 14 Oct 2026: "Accept recommendations", (A) on every question. Q5 (A) put "#130's ask-or-infer rule and six set-up questions" into the spec. The Q5 text did not name the cap of five or say that it was an inference. **He took the agent's recommendation, and the round did not show him the number.** #130's resolution did say "(the five is an inference)" and "Not verified: ... that five is the right limit". Searches: design-vault "five questions", "batch"; mantahostels "questionnaire length"; workflow-core "question budget". No hit holds a ruling of his own on the count.

**What the sources say.**
- **Shorter is better for response, with a continuous cost.** Edwards et al., Cochrane review "Methods to increase response to postal and electronic questionnaires" (2009 version, abstract via the Queen's University Belfast record; not opened): shorter electronic questionnaires, odds ratio 1.73 (95 % CI 1.40–2.13); postal (earlier version), 1.86 (1.55–2.24). A 2023 update (MR000008.pub5) exists; its figures were not read. https://doi.org/10.1002/14651858.MR000008.pub4
- Rolstad, Adler and Rydén, "Response Burden and Questionnaire Length: Is Shorter Better?", Value in Health 14(8):1101–1108, 2011 (abstract read): response rate fell with length (P ≤ 0.0001), but "it is impossible to separate the impact of content from length"; choose on content, not length alone. https://doi.org/10.1016/j.jval.2011.06.003
- **Later answers get worse.** Galesic and Bosnjak, "Effects of questionnaire length on participation and indicators of response quality in a web survey", Public Opinion Quarterly 73(2):349–360, 2009 (summaries only; full text not read): stated lengths of 10, 20 and 30 minutes gave start rates of 75 %, 65 % and 62 %; answers to later questions were faster, shorter and less differentiated. https://doi.org/10.1093/poq/nfp031 .
- **Questions in one message.** Boomerang, "7 Tips for Getting More Responses to Your Emails (With Data!)", Feb 2016 (read; vendor, observational, no sample size given for this result): "emails that asked 1-3 questions are 50% more likely to get a response than emails asking no questions"; "an email with 3 questions is 20% more likely to get a response than an email with 8 or more". **Weak.** https://blog.boomerangapp.com/2016/02/7-tips-for-getting-more-responses-to-your-emails-with-data/
- impeccable 4.5.0 `shape`: "Ask two or three related questions per round" (for a live user in a session; `function-questions.md` F1.7).
- No source found tests a count of questions for a client intake relayed through a third person. All sources measure total length or total question count, never a sub-count of one kind of question.

**How large the batch is today.** design-project step 1 (`plugin/skills/design-project/SKILL.md:16-44`) already asks, in "one plain message", about six kinds of item plus "the twelve colour and logo questions" (which the founder answers or marks "ask the client"). #177 adds S1–S6. So one client-facing batch can hold up to 12 colour and logo questions, 6 set-up questions and several older items, about 20 in all.

**Disposition: CONFLICTS (in part).**
- What research supports: a limit on the **whole** batch's burden, with the most important questions first, because response and answer quality fall with total length and with position (Edwards; Galesic and Bosnjak). The house caps only the function questions. The same set-up step can still send the client about 20 questions, which the five-question cap was meant to prevent (F2.4: "the client's question budget is small").
- The number itself is not answerable from any source. It is a business fact per client: how much effort this client will give. For mmm-infra the record already holds one fact: "He doesn't want to do any effort here" (site-look S10).
- What the founder would need to pick: a total question budget per client batch (with a default, for example the 1–3 or "few" end of the Boomerang and impeccable shape), and the order rule (the questions that decide the most design, first). The colour and logo questions that the files or the current site answer must be skipped first, as design-project §1 and impeccable `init` already say ("scan first").

**Bold finding.** **The founder ruled on #101 Q5 (A), by accepting an agent's recommendation, a cap of five function questions that the round did not show him and that its own research rated 0.6 with "no source". The research on burden is about the total length of the message, and the same set-up step can send about 20 questions to the client (12 colour and logo, 6 set-up, others). **

**Confidence:** 0.7. It moves down if the founder answers most colour and logo questions himself in practice, so that the client sees few of them. A count of client-facing questions in the first two set-up batches would show this.

## Summary

| # | Value | Ruled by the founder? | Disposition | Confidence |
|---|---|---|---|---|
| 1 | Three critics; pass on 3 Yes; 3 No = fault; split or Unsure → founder | #100 Q3 (A), agent's recommendation accepted | CONFLICTS (in part): a same-model panel, where the only panel evidence is cross-family; unanimity threshold not calibrated; founder-question load not priced | 0.7 |
| 2a | Stop after two re-checks | #94 Q2 (A) → #109, agent's recommendation accepted | SOURCED (most gain in the first one or two passes) | 0.75 |
| 2b | One fresh critic answers the narrow re-check | #100 Q4 (A), agent's recommendation accepted | CONFLICTS: one critic clears a fault that three had to raise | 0.7 |
| 3 | Calibration every ten logged rounds | #100 Q9 (B), agent's recommendation accepted | NOT A DESIGN CLAIM; add event triggers (model change, rule change) | 0.75 |
| 4 | Trial on 12 mmm-infra pages | #133 Q3 (A), re-priced agent's recommendation accepted against his first guess | CONFLICTS for its use as two headline rates and a flip rule: 2 kept pages; 1 planted fault | 0.85 |
| 5 | Critics read the last ten corrections-log entries | #100 Q7 (A), agent's recommendation accepted | CONFLICTS (in part): count is a knob; recency, one shared set and an unbalanced (mostly rejected) set go against the sources | 0.65 |
| 6 | 2–3 weakest parts per candidate | #100 Q6 (B); the idea is his (mantahostels#3698), the count the agent's | NOT A DESIGN CLAIM; measure the hit rate against his rejections | 0.7 |
| 7 | At most five function questions per client batch | #101 Q5 (A), agent's recommendation accepted; the number was not shown in the round | CONFLICTS (in part): research bounds the whole batch, and the set-up batch can hold about 20 questions; the count is a business fact per client | 0.7 |

**Places where a value the founder ruled on departs from the research (the bold findings above):** items 1, 2b, 4, 5 and 7.

**Genuine gaps for the founder (only these):**
- Item 1: a target agreement with his verdicts, to set the escalation threshold. This is a point to pick on a measured curve (coverage against agreement); he can pick it only after the trial gives the curve.
- Item 7: a total question budget per client batch. This is a business fact per client.

**Corrections that need a ticket (not founder questions):** 2b (re-check by three critics, or by script where a script answers); 3 (event triggers); 4 (more kept pages and several planted faults, or the headline figures reported with their intervals); 5 (relevant, balanced, per-critic example sets); 6 (hit-rate count in the round log); 7 (a cap on the whole batch, wording of user story 59 against §"The house method").

Bound: read in full: issues #183, #154, #109 (body and comments), #130, #133 and #100 (all comments), the #94 rounds (by grep), mantahostels#3668 (body and comments) and #3734, the comments of mantahostels#3669 and #3698 (by grep), mmm-infra#8's round-1 reply, `docs/research/visual-critic-reliability.md`, `docs/research/function-questions.md`, `plugin/skills/design-project/SKILL.md` §1, `gate.js` lines 20–60 and 320–345. Read in part: mantahostels `correspondence-draft-quality.md` (by grep), `docs/research/mmm-infra-site-look-round.md` S3, Verga et al. (HTML), Jung et al. (HTML v1), Wang et al. (PDF text, sections on sample count and consistency), Madaan et al. (PDF text, iteration and error-analysis sections), Zhao et al. (PDF text, bias section). Abstract only: Kim et al. 2025, Chen et al. 2024, Huang et al. 2024, Shankar et al. 2024, Agarwal et al. 2024, Liu et al. 2022, Xiong et al. 2024, Vasconcelos et al. 2024, Rolstad et al. 2011, Brown, Cai and DasGupta 2001. Search summary only, not opened: Krosnick et al. 2002, Galesic and Bosnjak 2009, the Cochrane review's figures (2009 and 2007 versions; the 2023 update unread), Hanley and Lippman-Hand 1983, the vendor calibration pages, MedJUDGE. Read in full (web): Nielsen 1994 (NN/g), Moran and Gordon 2023 (NN/g), Boomerang 2016. Not read: Kish 1965 (textbook formula only). The split-rate and interval figures are computed here under stated assumptions (independent critics; a within-page correlation of 0.2); they are not measured.

## Owners

Item 4's fixes: the correction section on #169. Items 2b, 3, 5 and 6: #193. Item 7's budget and item 1's target agreement: #183's question to the founder and #169 step 5.
