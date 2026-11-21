# Critic shape: one critic, topic critics or a chain (design-vault #212)

⚠ **Bound 15 Oct 2026 (#224): the Gaps on union recall and on topic critics against one critic are measured in-house for a 2026 Claude critic on rendered pages, in `docs/research/critic-shape-test.md`. The lock was tested only inside the chain, not alone. The whole-page critic plus a type critic is the shape; three whole-page critics, topic critics and the chain each invent more faults beyond the run-to-run spread.**

Question: which critic shape gives the best result (cost not a factor)?
- (A) One whole-page critic. Scripts and three blind gate critics answer the checkable rules.
- (B) About five topic critics in parallel, plus one whole-page critic.
- (C) Coarse to fine in series: function, then role, then treatment. A later pass cannot overturn an earlier pass.

Prior research: `docs/research/rule-delivery.md` (B3 to B5, C4, C6) and `docs/research/visual-critic-reliability.md` (V5, V7, V10, V11).

Evidence labels: Strong = peer-reviewed or first-party, read. Moderate = primary read in part, or preprint read. Weak = abstract or snippet only. Judgement = our inference.

## Findings

### P1. Anthropic's "isolated judge per dimension" advice: the full context

**P1.1. "Demystifying evals for AI agents"** (Anthropic engineering, 9 Jan 2026, https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents; read again 15 Oct 2026).
- The advice is in "Step 5: Design graders thoughtfully". The full paragraph: "Model grading often takes careful iteration to validate accuracy. LLM-as-judge graders should be closely calibrated with human experts to gain confidence that there is little divergence between the human grading and model grading. To avoid hallucinations, give the LLM a way out, like providing an instruction to return "Unknown" when it doesn't have enough information. It can also help to create clear, structured rubrics to grade each dimension of a task, and then grade each dimension with an isolated LLM-as-judge rather than using one to grade all dimensions. Once the system is robust, it's sufficient to use human review only occasionally."
- Kind of evaluation: graders that score **agent transcripts and outputs** against a rubric, in an eval suite. The suite tests an agent over many tasks and many trials.
- Reason for isolation: **the post gives no reason.** It gives **no data** for isolated against combined judges. The wording is soft: "It can also help".
- Related lines in the same post: "vague rubrics produce inconsistent judgments"; "LLM-based rubrics should be frequently calibrated against expert human judgment"; "it's often better to grade what the agent produced, not the path it took".
- Evidence: **Strong** that Anthropic gives this advice. **Judgement** for its effect size: no measurement exists in the source.

**P1.2. "How we built our multi-agent research system"** (Anthropic engineering, 13 Jun 2025, https://www.anthropic.com/engineering/multi-agent-research-system; read again 15 Oct 2026).
- What was judged: the final research outputs (free-form text). Five rubric criteria: "factual accuracy (do claims match sources?)", "citation accuracy", "completeness", "source quality", "tool efficiency".
- The result: "We experimented with multiple judges to evaluate each component, but found that a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements."
- Scope: "This method was especially effective when the eval test cases did have a clear answer" (their example: does the report list the right three pharma companies).
- Data: **none** given (no agreement figures).
- Also: "Human evaluation catches what automation misses."
- Evidence: **Strong** as first-party practice. No numbers.

**P1.3. "Harness design for long-running application development"** (Prithvi Rajasekaran, Anthropic Labs, 24 Mar 2026, https://www.anthropic.com/engineering/harness-design-long-running-apps; read again 15 Oct 2026).
- Evaluator structure for frontend design: **one evaluator agent scored all four criteria** (design quality, originality, craft, functionality). Quote: "I gave the evaluator the Playwright MCP, which let it interact with the live page directly before scoring each criterion and writing a detailed critique." The post does not compare one evaluator with one per criterion.
- In the full-stack QA loop, one evaluator checked many criteria per sprint ("27 criteria covering the level editor" in sprint 3): "Each criterion had a hard threshold, and if any one fell below it, the sprint failed."
- Results: no numbers. "the evaluator's assessments improved over iterations before plateauing, with headroom still remaining"; "I regularly saw cases where I preferred a middle iteration over the last one."
- Faults of the one evaluator: it "tended to test superficially, rather than probing edge cases"; it found issues and then approved the work. The post does **not** say it missed whole-page issues.
- Lesson on structure: separation of **generator from evaluator**, not separation of criteria: "tuning a standalone evaluator to be skeptical turns out to be far more tractable" than making a generator critical of its own work.
- Evidence: **Strong** as first-party practice, one author, no controlled comparison.

**P1 meaning (judgement).**
- Anthropic gives two opposite practices for text judges and no data for either.
- The isolation advice is about **eval suites that grade many agent runs on a fixed rubric**, where a dimension is a property of a transcript or output. It transfers to a design critic only in part. A design critic must also judge the whole page (design quality is "a coherent whole rather than a collection of parts"), and a per-dimension judge cannot see that.

### P2. The split judges in #99 and #211: one call or separate calls? Did the gain hold for strong models?

**P2.1. Vision-Guided Iterative Refinement (arXiv:2604.05839, 2026; read in part, html, 15 Oct 2026).**
- The multi-dimension judge had **two prompts, split by evidence, not by topic**: a "Visual Judge" (rendered page only: visual task accomplishment, aesthetic quality) and a "Code Judge" (code only: code task accomplishment, code quality). Each prompt scores **two** dimensions in one call. The overall score is the average of the four. Quote (§3.2): the judge "scores both modalities individually". The paper does not say in words that the two templates are separate calls; separate templates (Appendix B.5.1) make it likely.
- The baseline single-score judge saw page and code together and gave "a single overall score between 1 and 10 for each solution".
- Result (Table 1): 200 tasks with a clear human preference, ties excluded. Agreement 69.5 % against 48.5 %; draws 8.5 % against 28.5 %; disagreement 22.0 % against 23.0 %.
- Read this with care: **disagreement did not change** (22.0 against 23.0). Nearly all of the gain is draws that became correct picks. A finer score (four averaged numbers against one integer) breaks ties. The result shows **"sub-scores beat one coarse score"**. It does **not** show "isolated topic judges beat one judge that scores every topic".
- The paper does not name the judge model for this test (Claude 4.5 Sonnet is the critic in the loop).
- Evidence: **Moderate** (preprint, read in part).

**P2.2. Branch-Solve-Merge** (Saha et al., NAACL 2024, arXiv:2310.15123; read in part, html, 15 Oct 2026).
- Calls: "branch" is one call that writes the criteria. "Solve" is **one call per criterion** (Algorithm 1: "for each c_i ∈ C do … Solve for each of the criteria"). "Merge" in the reported results is a sum, not an LLM call.
- Results (Table 3, writing questions; agreement with humans, position bias, length bias; zero-shot → BSM):
  - LLaMA-2-7B: 0.39 → 0.41; PB 62.3 → 48.3.
  - Vicuna-33B: 0.51 → 0.56; PB 30.7 → 20.0.
  - LLaMA-2-70B: 0.43 → 0.55; PB 51.7 → 17.3; LB 54.9 → 39.1.
  - **GPT-4: 0.59 → 0.62; PB 17.33 → 17.00; LB 39.1 → 36.8.**
- The authors: BSM "significantly reduces position and length biases for all models except for GPT-4". For GPT-4, "applying BSM obtains a further improvement of 3%".
- Closest test of **separate calls against one call with all criteria**: Plan&Solve, which "solves all branches together in one LLM call". LLaMA-2-70B only, writing only: agreement 0.43 against BSM 0.55; PB 43.0 against 17.3. **No such test with GPT-4.**
- The headline "up to 26 %" is from weak models.
- Evidence: **Moderate** (peer-reviewed, read in part; 2023 models).

**P2.3. CheckEval** (Lee et al., EMNLP 2025, arXiv:2403.18771; read in part, html, 15 Oct 2026).
- Calls: **many checklist questions in one prompt**, grouped by sub-dimension. §3.3: "To improve efficiency, we ask multiple questions simultaneously rather than asking each question separately. We compared single-question and multi-question inference in our pilot experiments and found no noticeable difference in performance."
- So CheckEval's gain comes from **decomposition into yes/no questions**, not from isolation. Its own pilot found isolation per question gave nothing (no figures given).
- Gains for strong models (average Spearman, G-Eval → CheckEval; SummEval / Topical-Chat): GPT-4o 0.32 → 0.50 / 0.52 → 0.64; GPT-4-Turbo 0.51 → 0.52 / 0.59 → 0.63; Mistral-Large 0.52 → 0.55 / 0.64 → 0.65; Qwen2.5-72B 0.43 → 0.50 / 0.62 → 0.59. The gain holds for some strong models (GPT-4o) and is near zero for others. Claude was not an evaluator.
- Inter-evaluator agreement (large models, SummEval, Krippendorff α): G-Eval 0.05, CheckEval 0.67. The strongest finding is **consistency**, not accuracy.
- Evidence: **Moderate** (peer-reviewed; read in part, 100k of 135k characters).

**P2 meaning (judgement).** All three "split the judgement" results are, for a strong model, results for **decomposing the rubric into explicit sub-questions or sub-scores**. No source in this set shows that isolation (as against decomposition in one call) helps a GPT-4-class or Claude model.

### P3. Separate per-criterion calls against one call with all criteria (2024 to 2026)

**P3.1. Multi-Crit** (Xiong et al., Univ. of Maryland and Univ. of Waterloo, arXiv:2511.21662 v2, 12 Mar 2026; Appendix E.2 read, main text read in part, 15 Oct 2026).
- Task: **multimodal** judges (image plus text) judge pairs of responses on several criteria. Open-ended generation (captions, stories, visual chat) and verifiable reasoning. Not image or page design.
- Direct test: one inference per criterion ("standard") against all K criteria in one inference ("joint"; the prompt says "treat each criterion separately"). Criterion average accuracy, open-ended / reasoning:
  - **GPT-4o:** per-criterion 69.57 / 69.79; joint 64.91 / 63.15. The authors: a "clear performance drop across all metrics" when joint.
  - **GPT-5:** per-criterion 68.51 / 77.41; joint **70.43 / 79.58**. The authors: GPT-5 "benefits from the joint setting".
  - **o4-mini:** per-criterion 69.67 / 80.85; joint 68.82 / 75.61.
  - **Gemini-2.5-Pro:** per-criterion 63.67 / 73.06; joint **67.06** / 70.96.
- Trade-off and conflict cases (one response better on one criterion, worse on another): GPT-4o falls hard when joint (open-ended conflict 44.9 → 26.4; trade-off 66.0 → 38.8). GPT-5 holds (conflict 38.5 → 43.5).
- Authors' summary: "Joint judgment generally reduces the model's sensitivity to criterion-level trade-offs", with GPT-5 on reasoning as the exception.
- Claude was in the benchmark (Claude-3.7-Sonnet, open-ended pluralistic accuracy 31.77 %) but **not** in the joint test.
- Evidence: **Moderate** (preprint, the relevant appendix read in full).
- Meaning (judgement): this is the **only** direct comparison found with frontier models. **The gap shrinks, and for open-ended judgement it reverses, as the model gets stronger.** A 2026 Claude model is nearer the second group. The one place isolation still helps strong models is **criteria that pull in opposite directions** (conflicts), and only for some models.

**P3.2. Rubric interference** (Yu et al., "Mitigating Rubric Interference in LLM Judges via On-Policy Self-Distillation", arXiv:2608.14684, v1 5 Aug 2026; abstract page read, 15 Oct 2026).
- Definition (abstract): rubric interference is when "the verdict on one rubric shifts depending on which other rubrics are co-present". The abstract says that current methods usually score each rubric in a separate call, and that one joint pass is cheaper but brings this interference.
- Size: in a preliminary study, "only one-third of samples receive fully consistent verdicts when evaluated under rubric sets of varying composition".
- Models: Qwen3 and Llama-3.1 (open), GPT-4.1 as a reference judge. No Claude, no Gemini. No result by model strength on the abstract page.
- Evidence: **Weak** (abstract only; preprint).
- Meaning (judgement): a joint pass is **less stable**: change the other rules on the list and a verdict can change. This is a real cost of one critic with a long rule list. It is a weaker cost for a critic whose list is short and fixed (option A's whole-page critic).

**P3.3. Criteria confusion even with one aspect per call** (Hu et al., "Are LLM-based Evaluators Confusing NLG Quality Criteria?", ACL 2024, arXiv:2402.12055; read in part, 15 Oct 2026).
- The prompt template takes one "Evaluation Criterion" (one aspect per call, by the template; not said in words).
- Finding: "correlations between LLM-generated scores across different aspects are significantly higher than those between human judgments". For GPT-4: "its confusion issues seem to be more severe than GPT-3.5", although GPT-4 agreed with humans more overall (SummEval average Pearson 0.632 against 0.515).
- Evidence: **Moderate** (peer-reviewed; 2023 to 2024 models; text summaries).
- Meaning (judgement): **isolation does not stop halo.** A judge that sees the whole output scores one aspect partly from its overall impression. A "type critic" that sees the full page screenshot will be moved by the colour and the layout too. Isolation by topic narrows the **rules**, not the **evidence** the eye takes in.

**P3 summary (judgement).**
- With 2023 to 2024 models (GPT-4, GPT-4o), one call per criterion was a little better (BSM +3 points for GPT-4; Multi-Crit about +5 points for GPT-4o).
- With 2025 frontier models (GPT-5, Gemini-2.5-Pro), one joint call was as good or better on open-ended judgement (Multi-Crit). CheckEval's pilot found no difference.
- The costs of a joint call that remain: lower sensitivity to criteria that conflict, and verdicts that move when the rule set changes (rubric interference).

### P4. Does the order of judging matter?

**P4.1. Nielsen: two passes, whole first, then parts** (Jakob Nielsen, "The Theory Behind Heuristic Evaluations", nngroup.com, 1 Nov 1994, https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/; read 15 Oct 2026).
- Quote: "In principle, the evaluators decide on their own how they want to proceed with evaluating the interface. A general recommendation would be that they go through the interface at least twice, however. The first pass would be intended to get a feel for the flow of the interaction and the general scope of the system. The second pass then allows the evaluator to focus on specific interface elements while knowing how they fit into the larger whole."
- This is advice from practice. Nielsen gives **no measurement** of two passes against one, or of whole-first against parts-first.
- Important: it is **one evaluator doing both passes, in one mind**. The second pass keeps the first pass's view of the whole ("while knowing how they fit into the larger whole").
- The current NN/g how-to (Moran and Gordon, 25 Jun 2023, https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/) keeps the two-pass idea in a weaker form: first "go through the task once just to learn the system, without attempting to evaluate anything", then evaluate on the second pass.
- Evidence: **Strong** that this is the method's advice (primary, read). **Judgement** for its effect: unmeasured.
- Bearing: this supports **"see the whole first, then judge the parts in light of the whole"**. That is the shape of (A) (a whole-page critic) and of one critic that reads coarse to fine. It is not evidence for (C) as defined (separate fresh critics per stage, each blind to what comes later, with a lock on earlier decisions). In (C) the function critic never sees treatment, and the treatment critic gets the whole only as a fixed decision.

**P4.2. Heuristic walkthrough: a task pass, then a heuristic pass** (Sears, "Heuristic Walkthroughs: Finding the Problems Without the Noise", Int. J. Human-Computer Interaction 9(3):213–234, 1997; only secondary descriptions read: Usability Body of Knowledge, http://usabilitybok.org/heuristic-walkthrough/, Mar 2011).
- UsabilityBoK: "Participants in this method make two passes through a product. The first pass uses "thought-provoking" questions and requires the evaluators to work through a set of prioritized tasks. The second pass requires evaluators to use a set of heuristics to find additional problems."
- The title claims fewer false positives ("without the noise") than plain heuristic evaluation. I did not read the paper's figures.
- Evidence: **Weak** (secondary only).
- Bearing: a published human method that judges **purpose and use first, then rules**. It is the nearest human analogue to "function walk first, then the rule list" **inside one critic**.

**P4.3. Order inside one LLM call: later labels are worse** (Stureborg, Alikaniotis, Suhara, "Large Language Models are Inconsistent and Biased Evaluators", arXiv:2405.01724, 2 May 2024; read in part, 15 Oct 2026).
- GPT-4 scored four attributes (coherence, consistency, fluency, relevance) in one generation. Scores were strongly tied to each other: correlation between attributes r = 0.979 for GPT-4 against r = 0.315 for humans (Figure 4). The authors: "LLM evaluators tend to overrely on this adjustment of its priors—experiencing an anchoring effect."
- Position test (GPT-3.5-Turbo): coherence placed 1st to 4th in the output gave Kendall τ 0.400, 0.391, 0.359, 0.368. The authors: "labels predicted later in the LLM generation experience a degradation in correlation against expert annotators". Mitigation in their table: "Predict only one attribute per generation."
- Evidence: **Moderate** (preprint, read in part; 2023 to 2024 models). The position effect is small (about 0.03 to 0.04 τ) and is for GPT-3.5.
- Bearing: inside one call, **what is judged first anchors what comes after**. So in a single critic, the order of questions is a real choice. Put the questions whose answer should anchor (function, then hierarchy) first, and the fine ones after. It is also an argument for isolation of the checkable fine questions (A's gate critics), so that the coarse verdict does not set their answers.

**P4.4. Order of rubric parts, by search** (15 Oct 2026). "Evaluating Scoring Bias in LLM-as-a-Judge" (arXiv:2506.22316; search snippet only) found that the **order of score descriptions** in a rubric changes scores, with "varying sensitivity across different models". Rubric interference (P3.2) found reordering changes verdicts. **Weak.** I found **no study** that tests judging coarse aspects before fine aspects (or in separate sequential passes) against the reverse or against all at once, for an LLM or for a human design evaluator.

**P4.5. "Order of judging" against "order of fixing" (judgement).**
- **Order of fixing** (fix function before role before treatment) is a **building-process** question. The prior research (rule-delivery.md C6, B5) found one weak study for it (APD-Agents, coarse-to-fine layout) and no study for staged design rules. The logic for it is a dependency argument (#121): a treatment fix on an element that the function pass then removes is waste. That argument is about cost and rework, and it is sound, but it is not evidence that the **critic's accuracy** goes up.

### P5. More independent eyes on everything, or narrower eyes on one topic?

**P5.1. Nielsen: several independent evaluators find far more** (Nielsen, "The Theory Behind Heuristic Evaluations", 1 Nov 1994, nngroup.com; read 15 Oct 2026).
- "Averaged over six of my projects, single evaluators found only 35 percent of the usability problems in the interfaces."
- "different people find different usability problems"; "since different evaluators tend to find different problems, it is possible to achieve substantially better performance by aggregating the evaluations from several evaluators."
- "some of the hardest-to-find usability problems … are found by evaluators who do not otherwise find many usability problems."
- "It would seem reasonable to recommend the use of about five evaluators, but certainly at least three."
- Evaluators work alone; findings are pooled only after all are done (the 2023 NN/g how-to: team members "should not see each other's evaluations until their own evaluation is complete").
- Every evaluator in this method judges **the whole interface against the whole heuristic list**. The gain is from **independent eyes on everything**, not from a topic split.
- Evidence: **Strong** (primary, read; human evaluators, 1990s software).

**P5.2. Duan et al. CHI 2024: one GPT-4 equals about one human; a group of six humans finds far more** (arXiv:2403.13139 v1; read in part, 100k of 140k characters, 15 Oct 2026).
- How the guidelines were given: **all guidelines of one set in one prompt**, with the UI's JSON: "querying an LLM with the guidelines' text and a JSON representation of the UI". Reason: the context limit (guidelines "up to 2k tokens", UI JSON "around 3-5k tokens", 8.1k limit). **No per-guideline against all-at-once test.**
- An ablation with **no** guideline text gave fewer violations (50 against 63) and far fewer helpful ones (14 against 38). The rules in the prompt matter.
- Of 100 distinct violations: 62 found only by human experts, 29 by both, 9 only by GPT-4. Per evaluator: precision 0.829 (average human) against 0.603 (GPT-4); recall 0.336 against 0.380; F1 0.478 against 0.466. Six humans reviewed each UI. The authors: "GPT-4 is less comprehensive than a group of 6 human experts."
- Temperature 0, one run. No test of pooled runs.
- Evidence: **Moderate-to-Strong** (peer-reviewed, read in part; GPT-4, 2023).
- Meaning (judgement): one model critic is like **one** human evaluator (recall about 0.35 to 0.38). The large recall gain in this study came from the **group**, which is consistent with Nielsen's 35 % per evaluator.

**P5.3. Juries of different models** (Verga et al., Cohere, "Replacing Judges with Juries", arXiv:2404.18796 v2, 1 May 2024; read in part, 15 Oct 2026).
- A panel of three smaller models from **different families** (Command R, Claude 3 Haiku, GPT-3.5), each judging the **whole** output, beat one GPT-4 judge. Cohen's κ with humans: NQ 0.763 against 0.627; TriviaQA 0.906 against 0.841; HotpotQA 0.867 against 0.830. Chatbot Arena ranking, Pearson 0.917 against 0.817.
- The authors: "a PoLL composed of a larger number of smaller models outperforms a single large judge". The panel had less intra-model bias (score SD 2.2 against 6.1 for GPT-3.5).
- No test of a panel of repeat samples from **one** model. Tasks are QA correctness and chat preference, not design.
- Evidence: **Moderate** (preprint, read in part; 2024 models).

**P5.4. Against: judges share errors** (Kohli, "Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels", Apple Machine Learning Research, Jun 2026, https://machinelearning.apple.com/research/correlated-llm-evaluation-panels; summary page read, 15 Oct 2026).
- Nine frontier LLMs from seven families, on three NLI datasets (100 human labels per item) and RewardBench. The nine judges gave "about 2" independent votes' worth of information; about three-quarters of the nominal independence was lost. Panel accuracy was 8 to 22 points below independent voting. **"The best single judge matched or outperformed the full panel across all conditions."** Prompt variants, temperature and chain of thought did not remove the deficit.
- Evidence: **Weak-to-Moderate** (summary page, not the paper; models not named on the page).
- Meaning (judgement): independent model critics give less extra recall than independent humans do, because models fail on the same items. Copies of **one** model (the house's case: all critics are Claude) are likely to correlate more than a mixed panel. The recall gain from "more eyes" is real for humans (Nielsen) and smaller, perhaps near zero for accuracy, for same-model critics. It is **not measured** for fault-finding recall on a design (a union of findings, not a vote), where independent runs could still add different findings.

**P5.5. Synthetic heuristic evaluation: repeat runs of one model find the same issues** (Zhong, McDonald, Hsieh, Univ. of Washington, "Synthetic Heuristic Evaluation: A Comparison between AI- and Human-Powered Usability Evaluation", arXiv:2507.02306 v1, 3 Jul 2025; read in part, 100k of 113k characters, 15 Oct 2026).
- Set-up: screenshots (3 to 9 per task) of two mobile apps. GPT-4 main; Gemini-1.5-pro and Claude 3.5 Sonnet with the same prompt. The ten Nielsen heuristics were split into **two prompts of five** ("the first 5", then "the second 5"), because one pass hit the output token limit. No test of split against joint.
- Coverage of a master issue set: GPT-4 73 % (97/133) and 77 % (87/113); Claude 3.5 Sonnet 57 % (76/133) and 58 % (65/113); Gemini 59 %; the **five experts pooled** 57 % and 63 %; **one average expert** 18 % and 17 %.
- Repeat runs (Mar to Jun 2024): coverage-consistency against the first run **M = 93.86 % and 93.90 %**. "the same underlying issues recurred". So a second run of the same model adds about 6 % new issues; a second human adds many.
- What the model did well: "Aesthetic and minimalist design" coverage 86 % and 74 % (experts 38 % and 42 %); small layout and hierarchy differences (font size, whitespace).
- What it missed: **across-screen violations** 43 % (3/7) and 50 % (3/6), against experts 86 % and 83 %; consistency and standards 46 % and 40 %. Many severity-0 false positives (misread components, misjudged conventions).
- Evidence: **Moderate** (preprint, read in part; GPT-4, Claude 3.5 Sonnet, 2024).
- Meaning (judgement): (1) one strong model critic is now like a **pooled panel of a few humans**, not like one human. Different **framings** (different heuristic subsets, different instructions) are the more likely way to get new findings from the same model, but no study here measures that. (2) The weak area is **cross-context** faults (across screens), the nearest measured analogue to whole-page coherence.

**P5.6. Topic-specialist agents against one generalist: more findings, lower precision** (D'Arcy, Hope, Birnbaum, Downey, "MARG: Multi-Agent Review Generation for Scientific Papers", arXiv:2401.04259 v1, 8 Jan 2024; read in part, 100k of 146k characters, 15 Oct 2026).
- Task: peer review of scientific papers (text). Model: GPT-4, **8k context** (gpt-4-0613); each worker held one chunk of the paper.
- The only topic-split ablation found: MARG-S (specialist agents for experiments, clarity, impact) against MARG-TP (same multi-agent system, one generic task prompt, no specialists). Alignment with real reviews: recall **15.84 against 8.49**; precision **4.41 against 5.34**; comments per paper 19.8 against 8.5.
- User study: MARG-S 3.7 good comments per paper against 1.7 for the best single-agent baseline; generic comments 29 % against 60 %.
- Authors' reason: when the leader got the expert's instructions it "often ignores details of the instructions"; "refactoring the subtask to the separate expert model produces a much higher-quality result".
- Evidence: **Moderate** (preprint, read in part; GPT-4 8k, 2023).
- Meaning (judgement): this is the clearest evidence **for (B)'s mechanism**: a narrow agent follows its topic's instructions more fully and finds about twice as many faults, at the cost of more comments and lower precision. Two limits: (1) the 8k context forced the split, so part of the gain may be context length, not topic; (2) "ignores details of the instructions" is a 2023 GPT-4 failure. rule-delivery.md B1 shows instruction-following in 2025 to 2026 models stays near full at small rule counts, so the gap is likely smaller now. It is not measured for a 2026 Claude model.

### P6. Whole-page ("global") faults: do narrow critics miss them?

**P6.1. Duan et al. CHI 2024** (above, P5.2). Violations found only by humans were often "'global' (i.e., high-level) issues of the UI"; participants said GPT-4 was "missing the majority of the 'global' violations". The authors' reason: the JSON input ("GPT-4 cannot capture violations that would require processing the rendered image of a UI"). The paper does **not** blame a narrow focus. Its GPT-4 had **all** guidelines of a set in one prompt and still missed global faults. The model also "sometimes repeated the same feedback for every element of the same type", which is an element-by-element habit. **Moderate-to-Strong.**

**P6.2. Zhong et al. 2025** (above, P5.5). The model had all five heuristics of a set in one prompt and saw all the screens. **Moderate.**

**P6.4. Search for direct evidence** (15 Oct 2026). I found **no study** that compares topic-split critics with one whole-page critic on whole-page faults (coherence, hierarchy across sections, busyness), for a model or for humans. The searches "multi-agent specialized critics vs single generalist … holistic issues" and "LLM heuristic evaluation one heuristic at a time versus all" found only systems that **state** a per-heuristic design (Lubos et al., arXiv:2604.25420, Apr 2026, Gemini 2.0 Flash: per-heuristic prompting "helped to obtain more diverse and detailed issue descriptions", with redundancy, and no measured comparison; **Weak**).

**P6 meaning (judgement).**
- Model critics miss global and cross-context faults **even when they hold every rule at once** (P6.1, P6.2). So "one generalist critic sees the whole page" is **not** enough to catch global faults. The misses come from how the model reads the input (element by element, a JSON list, one screen at a time), not only from rule load.
- A topic critic (B) has no rule that names a global fault, so it is **less likely** to catch one than a whole-page critic with an explicit global question. This is logic, not measurement.
- What helps with global faults, from the evidence: give the critic the **rendered whole** (Duan: the JSON input was the cause), ask **explicit global questions** (hierarchy across sections, one primary action per view, rhythm), and use a **group** (Nielsen: hard problems are found by evaluators who find few others; Duan: six humans found 62 faults the model missed).

**P6.5. A human halo, for context** (Tractinsky, Katz, Ikar, "What is beautiful is usable", Interacting with Computers 13(2), 2000; and Tuch et al., Computers in Human Behavior, 2012; search summaries only). Tractinsky found that a system's look moved users' post-use usability ratings, and actual usability did not. Tuch et al. (80 participants) found the reverse direction. **Weak** (snippets; contested). Meaning: a global impression can colour detail judgements in humans too. It does not settle the order question.

## Bearing on A, B, C (result quality only)

**(A) One whole-page critic; checkable rules to scripts and blind yes/no gate critics.**
- For:
  - The decomposition gains that hold for strong models come from **explicit sub-questions**, not from separate calls (CheckEval: no difference single-question against batched; Multi-Crit: GPT-5 and Gemini-2.5-Pro as good or better joint on open-ended judgement). A keeps decomposition: scripts and yes/no gate critics for the checkable rules, and a structured question list for the whole-page critic.
  - Isolation helps most for **narrow checkable items** whose answer a global impression would otherwise move (Stureborg: anchoring and halo inside one call; Hu: halo even per aspect; rubric interference). A isolates exactly these in blind gate critics and scripts.
  - The only first-party design evaluator (Anthropic, Mar 2026) was one agent with four criteria, coherence first. Anthropic's research judge (Jun 2025) was one call after per-component judges were tried.
  - Nielsen's method: one evaluator sees the whole flow first, then parts "while knowing how they fit into the larger whole". Only a whole-page critic can do this.
  - Global faults need a critic that holds the whole page and is asked global questions (P6).
- Against:
  - One critic is one pair of eyes. A single evaluator finds a fraction of the faults a group finds (Nielsen 35 %; Duan: one GPT-4 ≈ one human, and six humans found 62 of 100 faults the model missed).
  - Model critics miss global and cross-context faults even with all rules loaded (Duan; Zhong: 43 to 50 % against experts' 83 to 86 %). A alone does not fix this.
  - A long judgement list in one critic has rubric interference and later-item decay (P3.2, P4.3), and a topic agent can follow its topic's instructions more fully (MARG, 2023).

**(B) About five topic critics in parallel, plus one whole-page critic.**
- For:
  - MARG (GPT-4, 2023): specialist agents doubled recall against real reviews (15.8 against 8.5) and halved generic comments. This is the best evidence for B's mechanism.
  - Per-criterion isolation helped GPT-4 (BSM, +3 points) and GPT-4o (Multi-Crit, about +5 points), and helps keep criteria that **conflict** apart (Multi-Crit trade-off cases).
  - Anthropic Jan 2026 advises it, without a reason or data.
  - B keeps one whole-page critic, so it does not lose coherence by design.
- Against:
  - For 2025 frontier models the per-criterion gain is gone or reversed on open-ended judgement (Multi-Crit, GPT-5, Gemini-2.5-Pro). A 2026 Claude critic is in that class. No Claude test exists.
  - MARG's gain came with **lower precision** (4.41 against 5.34) and 2.3 times more comments. In the house, more comments means more splits to the founder and more invented faults (V11).
  - Part of MARG's gain is a 2023 failure ("often ignores details of the instructions") and an 8k context limit. Both are smaller in 2026.
  - A topic critic still sees the whole screenshot, so halo still moves its verdict (Hu: confusion even per aspect).
  - Topic critics duplicate the gate critics where a topic's rules are checkable. Where a topic's rules are judgement (type, colour), the evidence for a separate judge with a strong model is the weak part.
  - Same-model critics share errors (Apple 2026: nine judges ≈ two votes; Zhong: repeat runs overlap 94 %). Five Claude topic critics give less independent coverage than their count suggests.

**(C) Coarse to fine in series, fresh critic per stage, later stage cannot overturn earlier.**
- For:
  - Order **inside a judgement** is real: the first verdict anchors later ones (Stureborg). Practice advises whole first, then parts (Nielsen; Sears's walkthrough).
  - Fixing in dependency order avoids rework (a treatment fix on a part that the function pass then removes). This is a **building** gain (#121's logic), not a judging gain.
  - The lock stops a later critic from re-raising a settled issue under a new name, which is one of V11's failure modes ("re-raised a dismissed issue under a different guideline").
  - Separate calls beat the same steps in one prompt for draft-critique-refine (Sun et al., rule-delivery.md B4).
- Against:
  - **No study** measures separate critics in series, with a lock, against one critic or parallel critics, for any task.
  - Nielsen's two passes are **one evaluator** keeping the whole in mind. C's later critics see the earlier stage only as a fixed decision, and the earlier critic never sees the fine stage. This splits the whole-page view that Nielsen's advice and the coherence criterion need.
  - The lock carries an early error to the end. With critic accuracy near 50 to 60 % on first findings (Duan: precision 0.60), a locked wrong function verdict is likely in some rounds.
  - Each stage is a new round on a changed candidate. V11 shows critic accuracy falls on later rounds of a design that got better (52 % → 39 %).
  - Each stage is one critic, so C has A's single-pair-of-eyes weakness three times, not a group.

## Plain answers

**(i) Does the evidence say order of judging matters?**
Yes, a little, **inside one critic**: what a judge decides first anchors what it decides after (Stureborg 2024: inter-attribute r 0.979 for GPT-4 against 0.315 for humans; later labels lose about 0.03 to 0.04 τ, GPT-3.5). Expert practice (Nielsen 1994, Sears 1997) says see the whole flow first, then the parts in light of the whole; neither measured it. **No evidence** says that judging in **separate critics in series, with a lock**, is more accurate than one critic. The order evidence speaks to **the question order inside one critic** (put function and whole-page questions first) and keeps the checkable fine questions **isolated** so the global impression does not set them. "Fix function before styling" is a **building-process** rule. It has a good rework argument (#121) and no accuracy evidence. So the founder's (C) intuition is right about **order of fixing** and about **order of reading**, but the evidence does not show that (C)'s **serial critics** judge better.

**(ii) Does Anthropic's isolation advice favour (B) over (A) here?**
No, not on the evidence.
1. The advice (Jan 2026) is one sentence in a guide to agent **eval suites** that grade transcripts and outputs against a fixed rubric. It gives no reason and no data, and it says "It can also help".
2. Anthropic's own research judge (Jun 2025) tried per-component judges and kept **one call**; Anthropic's own design evaluator (Mar 2026) was **one agent with four criteria**.
3. Outside studies show the per-criterion gain for 2023 to 2024 models (+3 to +5 points) and **no gain or a loss** for 2025 frontier models on open-ended judgement (Multi-Crit). CheckEval found batching equal to one question per call.
4. The useful core of the advice, a clear rubric per dimension, an "Unknown" exit, and an isolated judge for each **checkable** dimension, is what (A) already does with scripts and blind gate critics.
The one result that favours B's topic split (MARG: recall ×1.9) is from 2023 GPT-4 with an 8k context, and it cost precision. That is why (B) does not score higher than (A) here. It is **not** disproved for a 2026 Claude critic; it is untested.

**(iii) Shapes the evidence favours that are not A, B or C.**
1. **A plus several independent whole-page critics (a Nielsen panel).** The strongest single effect in this file is "more independent evaluators find more" (Nielsen 35 % for one; Duan, six humans against one model). Each whole-page critic judges the whole page, alone, blind to the others; the findings are pooled after. Limit: same-model critics overlap (Zhong 94 %; Apple 9 ≈ 2). So make them **differ on purpose**: a different lens order or persona, a different view (full page against viewport crops), or a different model family where the house allows. Evidence: Moderate for the panel effect in humans; Weak for its size with one model family.
2. **A with C's order inside the critic, and C's order for fixing.** The whole-page critic reads coarse to fine in one context: function walk first, then role and hierarchy, then treatment (Nielsen, Stureborg). The building session then fixes in dependency order (function, then role, then treatment), and the critic's next round may not reopen a settled function verdict without new evidence. This takes C's real gains (reading order, rework order, no re-raising) without its unmeasured cost (a split whole and locked early errors).
3. **A with one specialist only where a topic's judgement rules are many and not checkable.** MARG's gain came from a narrow agent following instructions the generalist skipped. If an in-house test shows the whole-page critic skips one topic's rules, add a specialist for **that** topic only. Do not add five by default.

## Gaps: what no source measures

- No study compares one critic, topic critics, and serial critics on **rendered web pages**, with any model.
- No study compares per-criterion against joint judging with a **Claude 4-class** model (Multi-Crit tested GPT-5, o4-mini, Gemini-2.5-Pro, GPT-4o; Claude-3.7-Sonnet was in the benchmark but not the joint test).
- No study measures the **union recall** of several same-model critics on design faults (Zhong measured run-to-run overlap, 94 %, for one prompt).
- No study measures whether a **lock** on earlier verdicts helps or harms.
- No study measures whether topic critics miss **whole-page** faults more than one critic does.

**An in-house planted-fault test could settle most of this** (judgement on design; the founder ruled it on #212, and #224 runs it):
1. Take 6 to 10 known-good candidates. Plant faults in each, tagged by kind: function (a dead or missing action), global (two primary actions in one view, broken hierarchy across sections, a busy section), type, colour and surface, treatment. Keep some candidates clean (to measure invented faults).
2. Run each shape on the same set: A; A plus 3 independent whole-page critics (differing lens order); B; C. Run each shape 3 times.
3. Score recall per fault kind, false findings per clean candidate, and run-to-run variance. Also score each shape against the founder's past verdicts (the calibration set).
4. Decide from the per-kind recall: if B beats A only on one topic, add that one specialist (iii.3). If A plus independent critics beats A on global faults, adopt iii.1.

## Bound

Read in part (html or summary page) for 2604.05839, BSM, CheckEval, Multi-Crit (its Appendix E.2 in full), Hu et al., Stureborg et al., Verga et al., Duan et al., Zhong et al., MARG, Lubos et al. Read in full: the three Anthropic posts (fetched through a summariser, with verbatim quotes checked) and Nielsen's 1994 theory page. Abstract or snippet only: rubric interference (arXiv:2608.14684), the Apple panel study, Sears 1997 (secondary), "Evaluating Scoring Bias" (arXiv:2506.22316), Tractinsky 2000 and Tuch 2012. 22 sources opened. Searched 15 Oct 2026.
