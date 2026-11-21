# Visual critic reliability: can a Claude critic judge a rendered design?

Question (design-vault#99, on map #96, 13 Oct 2026). How reliably can a Claude critic judge a rendered design (a screenshot, a web page, an artwork) against design principles? What structure makes the judgement reliable? Does the text-judge evidence in mantahostels `docs/research/correspondence-draft-quality.md` (F1–F7) transfer to visual judging?

Written in ASD-STE100 Simplified Technical English.

Evidence labels: **Strong** (peer-reviewed or first-party, paper read), **Moderate** (primary read in part, or a preprint read), **Weak** (abstract only, or one small study), **judgement**. Each source also says "read", "read in part" or "abstract read".

Era labels: **timeless** (perception, colour, contrast, Gestalt grouping, legibility) or **era-bound** (a style or a standard that changed with the web: for example flat design, mobile-first layout, a 2010s app convention).

## Findings

### V1. A VLM critic of a UI screen: agreement with designers and with users

- **UICrit** (Duan, Chen, Li, Hartmann, Li; UIST 2024; arXiv:2407.08850; read in part, about 100k of 119k characters). Seven designers wrote 3,059 critiques of 983 Android screens. The critiques use the Nielsen Norman heuristics, the CrowdCrit visual design critiques and the Apple Human Interface Guidelines. The topic clusters are layout (696), colour contrast (655), text readability (591), button usability (601) and learnability (601). Findings:
  - Zero-shot Gemini Pro Vision critique quality was 0.31. Few-shot examples plus visual prompting gave 0.48 (the "55 % gain", p = 5e-4). Human designer critiques got 0.75. Raters preferred the few-shot set to the zero-shot set 67 % of the time.
  - Of 5,927 comments that Gemini made, only 776 (13.1 %) passed the authors' validity filter.
  - The model could not find the location of a fault on the screen. The bounding-box overlap (IoU) from a screenshot only was 0.004. A grid overlay made it worse. Image patches (0.222) and coordinate prompts (0.186) helped.
  - Raters said the zero-shot critiques "made too many assumptions" and that some were hallucinations.
  - **Human experts agreed only fairly with each other**: six experts who rated critiques got Fleiss' kappa 0.29; on rankings, 0.55. So the target that a critic must hit is itself noisy.
  - Each UI had one annotator only.
  - Era: the screens come from RICO (published 2017; Android apps of about 2016–2017) through its CLAY subset. The guidelines (Nielsen heuristics) are mostly timeless. The screens are **era-bound and dated** (Material Design 1 era). The models are 2024 models; a 2026 model can be better.
  - **Moderate** (peer-reviewed; one model family; a critic, not a pass/fail judge).

- **MLLM as a UI Judge** (Luera et al., Adobe / UC Berkeley / Georgia Tech, arXiv:2510.08783, Oct 2025; read). Claude 3.5 Sonnet, GPT-4o and Llama-3.2-11B-Vision rated 30 UIs on nine 1–7 factors. About 9,300 valid MTurk responses gave the human mean per UI. Findings:
  - The model is close to the **average user** on mean ratings: Claude ±1 accuracy 0.77, exact 0.38, MAE 0.51, Pearson 0.69 overall.
  - Pairwise choice ("which of two UIs is better"): Claude 60.0 %, GPT-4o 59.6 %, Llama about 52–53 %. Chance is 50 %.
  - The result depends on the factor. "Interesting" was best (Claude pairwise 78.5 %, Pearson 0.85). **"Ease of use" was at chance** (Claude pairwise 47.0 %, Pearson −0.05); the models over-rated it (Claude 6.89 against human 6.21).
  - Pairwise accuracy rose to about 93 % (Claude) when the human gap between the two UIs was large. It was near chance when the gap was small.
  - No test of position bias, prompt variants or run-to-run flips.
  - The paper itself has inconsistent figures (section 5.1 against Table 4).
  - The UIs are email templates from reallygoodemails.com, mostly professional, to "Western design standards". The authors say an MLLM must "supplement, rather than fully replace" human testing, and must not be used for late-stage validation.
  - Era: undated screens, recent professional email design (probably 2020s). Factors are perception and emotion (mostly timeless as concepts; the taste behind "aesthetic" is era-bound).
  - **Moderate** (preprint, read; 30 UIs only).

Meaning for the design round (judgement): a model predicts the **crowd's average** reaction well when two designs are far apart. It is close to a coin flip when two good designs are near each other. That is the exact case in a design round, where the founder narrows close candidates.

### V2. Anthropic's own design-critic loop (first-party, March 2026)

- **"Harness design for long-running application development"** (Prithvi Rajasekaran, Anthropic Labs, anthropic.com/engineering, 24 Mar 2026; read). A generator agent builds a frontend; a separate evaluator agent uses Playwright to open the page, take screenshots and score it. Findings:
  - When a model judges its own output it tends to be "confidently praising the work"; agents "reliably skew positive when grading their own work". A separate evaluator helps, but it "is still an LLM that is inclined to be generous towards LLM-generated outputs". This agrees with text finding F3 (self-preference).
  - The subjective judgement became gradable through four named criteria: **design quality** ("a coherent whole rather than a collection of parts"), **originality** (custom decisions, not template layouts, library defaults or "AI-generated patterns"), **craft** ("a competence check rather than a creativity check") and **functionality** (usability apart from aesthetics). The author weighted design quality and originality more than craft and functionality.
  - **Calibration to one person**: "I calibrated the evaluator using few-shot examples with detailed score breakdowns". This "aligned with my preferences, and reduced score drift across iterations". For the full-stack QA evaluator, the loop was to "find examples where its judgment diverged from mine" and change the prompt; "It took several rounds".
  - **Iteration**: 5 to 15 rounds. Evaluator scores "improved over iterations before plateauing". The trend was "not always cleanly linear"; the author "regularly saw cases where I preferred a middle iteration over the last one". This is the visual case of text finding F2 (judge score rises; the human does not always agree that the last round is best).
  - Evaluator faults: it found real problems and then "talk[ed] itself into deciding they weren't a big deal"; it "tended to test superficially"; small layout issues remained.
  - **Strong** as first-party practice by one author with his own taste as the reference. It is not a controlled study and gives no agreement figures.

### V3. Pixel judgement of fine layout: good for large faults, poor for small ones

- **Haraguchi et al., "Can GPTs Evaluate Graphic Design Based on Design Principles?"** (CyberAgent / Kyushu University, SIGGRAPH Asia 2024 technical communications, arXiv:2410.08885; read in part, the figures with the r values were not in the text I could read). GPT-4o scored 700 banner and poster designs (100 VistaCreate templates and 600 copies with the text moved or resized by a small, medium or large amount) for **alignment, overlap and white space**. 60 crowd raters gave five ratings per design.
  - GPT-4o correlated with the humans better than the O'Donovan (2014) rule-based metrics, at all perturbation levels.
  - In pairwise tests, **GPT-4o was worse than the rule metrics for small alignment and small white-space faults**. Its accuracy rose with the size of the fault. The rule metrics read the vector coordinates; the model reads pixels.
  - GPT-4o scores varied less than human scores (five runs at temperature 1, averaged).
  - One model, one prompt, synthetic faults, crowd raters with unknown skill.
  - Era: alignment, overlap and white space are **timeless** (Gestalt and legibility). The templates are 2020s stock social banners.
  - **Moderate.**

Meaning (judgement, on a fair base): a fault that a measurement can find (a 4 px misalignment, an overlap, a margin) is found better from the code or the coordinates than from a screenshot. A VLM is better than a rule metric at the overall "does this look right" question.

### V4. Screenshots plus code beat code alone; a per-task checklist judge can rank models like humans do

- **ArtifactsBench** (Tencent Hunyuan, arXiv:2507.04952v2, 2025; read in part). 1,825 tasks; the judge sees the code and three screenshots taken during interaction, and scores a **10-item per-task checklist** (5 visual: layout, visual fidelity, motion timing, feedback, UX clarity; 5 code). The checklists were drafted by an LLM and refined by humans. Each item is scored 0–10, so this is **not** a yes/no checklist.
  - Pairwise agreement with front-end engineers (280 queries, 6 models; median rating as truth): Gemini-2.5-Pro **79.1 % from code only, 87.1 % with one screenshot, 91.0 % with several screenshots**. The same order held for o4-mini (72.4 → 76.3 → 79.4 %) and Qwen2.5-VL-72B (61.8 → 68.1 → 71.3 %).
  - The model ranking agreed 94.4 % with WebDev Arena (human votes). This is ranking consistency over many tasks, not agreement on one page.
  - **Not tested**: checklist against holistic, one judge against two, position bias, self-preference (Gemini judged Gemini outputs). Inter-annotator agreement was not reported.
  - The judgement is mostly "does it work and look finished", not taste. Screens were 1024×768.
  - Era: interactive web artifacts of 2025 (era-bound conventions; layout and feedback principles mostly timeless).
  - **Moderate** (preprint, large, but the human check is small and the ablations that matter most here are missing).

Meaning (judgement): a judge that sees the rendered page **and** its code is better than one that sees only one of the two.

### V5. Biases of a VLM judge: the text-judge biases are present, and some are new

- **MLLM-as-a-Judge** (Chen et al., ICML 2024, arXiv:2402.04788; read in part, about 100k of 127k characters). 14 datasets, about 4,400 image–instruction pairs, including AesBench (aesthetic perception) and Mind2Web (web pages). Claude was not tested.
  - **Pair comparison agrees with humans best; absolute scores agree worst.** GPT-4V: pair accuracy 0.773 without ties (0.636 with ties); scoring Pearson 0.490; batch ranking was weakest.
  - **Run-to-run inconsistency**: over six repeat runs, GPT-4V gave the majority verdict only 61 % of the time on scores and 68 % on pairs.
  - **Length bias**: a longer answer with the same meaning got +0.6 points (GPT-4V) on the score.
  - Egocentric (self-preference) bias: "a slight degree" in GPT-4V; no figure.
  - **Step-by-step reasoning (CoT) made agreement worse** for scoring (GPT-4V 0.557 → 0.299) and for pairs (0.683 → 0.563), but it cut hallucinations by 33–49 %. This differs from the text advice "reasoning before the verdict" (F7). Judgement: the 2024 models drifted from the image as they wrote; a 2026 reasoning model may differ. Treat as unresolved.
  - **Moderate** (peer-reviewed; 2024 models; tasks are general, not design).

- **"Fooling the LVLM Judges"** (arXiv:2505.15249, ACL 2025; abstract read). Visual edits that do not change the content (for example added text or decoration) made "all tested LVLM judges" give **inflated scores**, in all domains. Several biases together were worse. Pairwise judging was also open to it. **Prompt-based mitigation did not remove it.** **Weak** (abstract only). Judgement: a design candidate with more decoration, more polish or more text can win a VLM verdict for that reason only. This is the visual form of length bias.

- **MM-JudgeBias** (Lee, Park, Im; ACL 2026; arXiv:2604.18164; abstract read). 26 MLLMs show "systematic modality neglect": a judge can decide from the text and not look at the image. **Weak** (abstract only). See also "When Vision-Language Models Judge Without Seeing" (arXiv:2604.17768; title only, not opened).

- **Self-preference for a model's own visual output**: no study measures it directly (searched; not found). The first-party Anthropic note (V2) says the evaluator is "inclined to be generous towards LLM-generated outputs". Text evidence (F3) shows self-preference for text. Judgement: assume it transfers.

### V6. Blind spots: fine geometry, overflow and overlap are near chance from pixels

- **BlindTest, "Vision language models are blind"** (Rahmanzadehgervi, Bolton, Taesiri, Nguyen; ACCV 2024; arXiv:2407.06581v6; abstract read). Seven tasks that are trivial for a human (do two circles overlap, how many times do two lines cross, which letter is circled). Four VLMs averaged 58.07 %; **Claude 3.5 Sonnet was best at 77.84 %**; humans 100 %. Models fail when shapes **overlap or are close together**, and reach near 100 % when the shapes are far apart. The fault stays with higher resolution and with reasoning models. Linear probes show that the image encoder has the information; the language model does not put it into words. A September 2026 Auburn University news item reports a sequel with eight VLMs at about 46 % (news item only; not opened). **Moderate** (peer-reviewed; abstract read). Era: **timeless** (basic perception).

- **UI-Lens** (Xiang et al., CVPR 2026; abstract read from the CVPR poster page; the full paper returned HTTP 403). 4,759 Chinese-language UI pages, labelled by design experts in six display-fault categories; 10 models (8 closed). Task-average F1: **text overflow 20.36 %, container overlap 31.21 %, text inconsistency 10.61 %**. The authors call fine element-boundary tasks "near random". Models tested are not named in the abstract. **Moderate** (peer-reviewed; abstract only). Era: **timeless** fault types (a clipped label is a fault in any era).

- **UXBench** (arXiv:2606.13192, 2026; abstract read). 2,000 questions on 8 UX tasks from real screenshots (layout relations, visual hierarchy, content consistency). **Claude 4.5 Sonnet: 0.655 accuracy**; a small model trained for the task: 0.796. No human baseline. **Weak.**

- **PDF accessibility benchmark** (arXiv:2509.18965; seen only as a search snippet, not opened): reports GPT-4o perfect on colour contrast in PDFs and Claude 3.5 at 63 % on visual criteria. **Weak**; not verified.

Meaning (judgement on a fair base): text overflow, clipping, overlap, small misalignment, uneven spacing and colour contrast ratios are **measurement questions**. A script reads them from the DOM (element boxes, `scrollWidth > clientWidth`, computed colours and the WCAG ratio formula) with near-zero error. A VLM reads them from pixels at or near chance for small faults. Give these to code; give the VLM the questions only a viewer can answer (hierarchy, mood, coherence, "does it look like a template").

### V7. Iterating a design against a model critic: what is measured, and by whom

No study found runs Pan et al.'s test (F2) on visual design: an author iterating against a VLM judge, with humans rating each round. The evidence is indirect.

- **Design2Code** (Si et al., NAACL 2025, arXiv:2403.03163; read in part). Task: copy a reference web page into HTML. "Self-revision" shows the model its own render beside the reference. GPT-4V: block match 87.6 → 88.8, position 80.2 → 81.1, colour 73.0 → 72.9; human "win + tie" 82 % → 85 %. Gemini 1.0 Pro Vision: no gain (61 % → 60 %); most metrics went down a little. The authors: self-revision gives "minor improvement" for GPT-4V and Claude 3, none for Gemini. **Moderate.** Note: here the critic has a **reference image**, which is an outside signal. Huang et al. (F1) say self-correction works when there is an outside signal. Taste work has no reference.

- **Vision-Guided Iterative Refinement for Frontend Code Generation** (arXiv:2604.05839, 2026; read in part). Claude 4.5 Sonnet is the visual critic of rendered pages from WebDev Arena prompts; the generator is Distill-Qwen-14B, Claude 4.5 Haiku or Claude 4.5 Sonnet; the **best** of the cycles is kept.
  - A **multi-dimension judge** (task accomplishment and aesthetics, visual and code) agreed with human preference votes **69.5 %**; a **single-score judge 48.5 %**; draws fell from 28.5 % to 8.5 %. This is the visual form of CheckEval (F3): split the judgement and it agrees better.
  - Gains over the first draft: +17.8 % (14B), +9.8 % (Haiku), +10.8 % (Sonnet). Per cycle: 5.24 → 5.56 → 5.64 → 5.69 (diminishing). Refinement **without** a critique: +1.5 %. Code quality went **down** 1.7–3.2 % per cycle.
  - **The gains are measured by the same family of VLM judge, not by humans.** Pan et al. found exactly this setting inflates the judge's score. The critic (Sonnet) and the generator (Sonnet) were the same model in one arm. **Weak** for "iteration improves design as humans see it"; **Moderate** for the 69.5 % against 48.5 % judge result.


- **Image generation optimised against a learned aesthetic or preference reward** (Hong et al., "Understanding Reward Hacking in Text-to-Image RL", CVPR 2026 Findings, arXiv:2601.03468; search snippet only, not opened): "a universal pattern of reward hacking: the generation of unrealistic visual artifacts that nevertheless receive high reward scores"; an ensemble of rewards "can only partially mitigate" it. arXiv:2509.07027 (snippet only): held-out aesthetic scores **fall** while the training reward rises. **Weak** (snippets; RL training, not a prompt loop). It is the visual form of Gao et al. (F2): pressure on a proxy for taste first helps, then hurts.

- **Visual Prompting with Iterative Refinement for Design Critique Generation** (Duan et al., arXiv:2412.16829; read in part). The authors use **different models to generate and to refine** critiques, to avoid self-bias (they cite Xu et al. 2024, F1). The pipeline removed most generic comments ("test with users", "make it responsive"). Expert-rated comment quality: baseline 0.45, pipeline 0.47, human designers 0.56. Experts agreed only fairly (Fleiss' kappa 0.22 and 0.29). **Moderate.**

Meaning (judgement): the transfer of F1–F2 to visual work is **likely, not shown**. Where the target is objective (copy a reference, fix a clipped label, pass a contrast ratio), a render-and-critique loop helps a little. Where the target is taste, every published gain is a gain on a model judge; the only human-anchored report (Anthropic, V2) found the last round was often not the best. Keep the best round, cap the rounds, and let a human pick.

### V8. Many rules in one generation: each added rule lowers the chance that all hold

- **IFScale, "How Many Instructions Can LLMs Follow at Once?"** (Jaroslawicz et al., Distyl AI, NeurIPS 2025, arXiv:2507.11538; read in part). Each instruction is "include this keyword" in a business report; 10 to 500 instructions. Claude Sonnet 4: 100 % at 10, 98.0 % at 50, 94.4 % at 100, 77.2 % at 250, 42.9 % at 500. Claude Opus 4 is similar. Reasoning models (o3, Gemini 2.5 Pro) stay near perfect to about 150, then fall. As density rises, models mostly **omit** instructions (Sonnet 4 omission-to-modification ratio 1.4 at 100, 6.1 at 500) and favour earlier instructions. **Moderate.** Limit: keyword rules are easy, checkable and independent. The paper says it does not test style or subjective rules.

- **FollowBench** (Jiang et al., ACL 2024, arXiv:2310.20410; read in part). Each level adds one constraint. GPT-4 (1106) satisfied all constraints in 84.7 % of cases at one constraint and 61.9 % at five. **Style** constraints held up better (GPT-4: 96.7 % → 90.0 %); a weaker open model fell from 90.0 % to 56.7 %. **Moderate** (2023 models).

- **ManyIFEval / StyleMBPP** (arXiv:2509.21051, 2025; abstract read). Ten LLMs; up to 10 text instructions and up to 6 **code-style** instructions. Performance "consistently degrades" as the count rises; a logistic regression on the count alone predicts it within about 10 %. **Weak** (abstract).

- **DeCRIM** (from F1, Ferraz et al. 2024): decompose the request into a checklist, then check and fix one constraint at a time. The gain depends on the critic: a model as its own critic made it worse (−1.6 points); an ideal critic gave +16.9.

- **Visual design rules: no study found.** No benchmark found measures how many subjective design rules (for example "one focal point", "no template hero", "warm palette", "8 px grid") a model keeps at once in a generated UI. Searched; not found. WebGen-V (arXiv:2510.15306, abstract) evaluates design per section, which is a related idea, but gives no numbers in its abstract.

Meaning (judgement, arithmetic): if each rule holds alone with probability 0.95 and the rules are independent, 10 rules all hold with 0.60, 20 rules with 0.36. Subjective rules also **conflict** (F5): "bold and original" pulls against "calm and familiar". The founder's report (Claude struggles to satisfy many subjective rules in one cohesive draft) matches the shape of this evidence. Structures that help in the text studies: fewer rules active per step (split by stage, for example layout first, then type, then colour), a checklist per rule, a fix aimed at one finding at a time, and measured rules taken out of the model's load (V6).

### V9. Anthropic's first-party guidance that applies to a screenshot judge

- **Vision docs** (platform.claude.com/docs/en/build-with-claude/vision; read 13 Oct 2026). **Strong** (first-party, current).
  - Claude sees an image as 28×28-pixel patches. An image larger than the model's limit is **downscaled** before Claude sees it: long edge 1,568 px on the standard tier; 2,576 px on "Claude 4.7 and later models". A 1920×1080 screenshot goes to 1456×819 on the standard tier.
  - Consequence (arithmetic): a full-page screenshot 1440 × 6000 px is reduced to about 618 × 2576 px on the high-resolution tier (to 376 × 1568 on standard). A 16 px body font becomes about 7 px (standard: about 4 px). Fine spacing and small text are then not visible. **Crop the page into viewport-size sections, or zoom to the part under review.** The docs say: "Consider pre-resizing your images, cropping them, or both."
  - Put the image **before** the question ("Claude works best when images come before text"). For several images, label each ("Image 1:", "Image 2:").
  - Limitations named: "Spatial reasoning: Claude's coordinate and localization outputs are approximate"; counting is approximate; "Do not use Claude for tasks requiring perfect precision ... without human oversight."
  - Heavy JPEG compression can damage text; use PNG for UI screenshots.

- **"Demystifying evals for AI agents"** (anthropic.com/engineering, 9 Jan 2026; read; also cited in F7). For a judge: "closely calibrated with human experts"; "grade each dimension with an isolated LLM-as-judge rather than using one to grade all dimensions"; allow "Unknown"; "run multiple trials"; "read the transcripts"; for subjective quality, "LLM-based rubrics should be frequently calibrated". No text on images or design. **Strong** as stated practice.


### V10. Artwork and image aesthetics; one person's taste

- **ArtCoT, "Multimodal LLMs Can Reason about Aesthetics in Zero-Shot"** (arXiv:2501.09012, Jan 2025; read in part). Pairwise "which stylised image is more beautiful". 12 experts with art knowledge gave 21k preferences. Rank correlation (Spearman, per method, Elo/BT):
  - Plain prompt: GPT-4o 0.25/0.28; Gemini 1.5 Flash 0.47/0.55; **Claude 3.5 Sonnet −0.26/−0.32 (it ranked the opposite way to the experts)**.
  - Plain "think step by step" made per-instance agreement worse for all three (Claude 0.31 → 0.11). The model wrote "feels" and "appears" and invented interpretations.
  - A decomposed prompt (describe content and style → critique as an art critic → summarise) raised agreement: Claude 0.61/0.60, Gemini 0.70/0.78, GPT-4o 0.58/0.72. Removing the critic stage cost most.
  - **Moderate** (preprint; one task type; 2024 models). Era: stylisation of photos and paintings; the experts' taste is of 2024.
  - Meaning: structure decides the result more than the model. Concrete, staged questions beat both a bare verdict and free "reasoning".

- **GPT-4V and one person's aesthetic rating** (arXiv:2403.03594, 2024; read in part). PARA dataset (438 raters, 31,220 images). Predict one rater's low/middle/high rating from a few of that rater's examples. **Personal accuracy 0.557**; group-average accuracy 0.708; chance 0.333. Examples helped (0 against 3 per class); more than 3 per class did not help significantly. Judgements of beauty were more reliable than judgements of ugliness. **Moderate** (one model, 2024). Agrees with Dong et al. (F6): a model predicts a crowd better than one person.

- **AesBench** (Huang et al., 2024, arXiv:2401.08276; abstract only). 2,800 images labelled by people with an aesthetics background; 15 MLLMs including GPT-4V: "only rudimentary aesthetic perception". **Weak** (abstract; 2024 models).


Meaning (judgement): the founder's own verdicts are the only target that matters, and one person is the hardest target. The mantahostels calibration run (0 of 15 past verdicts) is consistent with this literature, not an outlier.

### V11. A UI critic in a revision loop: critic accuracy fell while the design got better

- **Duan, Warner, Li, Hartmann, "Generating Automatic Feedback on UI Mockups with Large Language Models"** (CHI 2024, arXiv:2403.13139; read in part, about 100k of 140k characters). A Figma plugin sent GPT-4 a **JSON layer tree** (text, type, position, size, colour), not pixels. A screenshot model of 2023 was "considerably worse" (no figures). 51 UIs; three guideline sets (Nielsen, CrowdCrit, others).
  - One-shot: 52 % of suggestions accurate, 19 % partly, 29 % not. Against human experts on 12 UIs: precision 0.60 (humans 0.83), recall 0.38 (humans 0.34), F1 0.47 (humans 0.48). **62 % of the violations were found only by humans; 9 % only by GPT-4.** Raters agreed only slightly with each other (Fleiss' kappa 0.11).
  - **Iteration (12 designers):** first round 52 % accurate, 47 % helpful; later rounds 39 % accurate, 33 % helpful, while "the UI's visual design improved each round". The critic kept finding faults in better designs, repeated one comment for every element of a type, and re-raised a dismissed issue under a different guideline. The authors call it "unsuitable as an iterative tool". Seven of 12 designers preferred one-shot checks.
  - Best guidelines: consistency and standards (misalignment, size inconsistency), recognition, match to the real world. Designers valued catches of misalignment, uneven spacing, poor colour contrast and unlabelled icons, all read from the **numbers in the JSON**. Worst: "aesthetic and minimalist design" (mostly inaccurate and unhelpful) and semantic grouping. It missed "global" issues that humans saw.
  - Era: 2023 model; Nielsen heuristics **timeless**; the mockups are 2023 designs.
  - **Moderate-to-Strong** (peer-reviewed, read in part, 12-person study).

Meaning: this is the closest published design analogue to F1–F2, and it shows a **different failure** from Pan et al. In the text study, the judge's score rose while quality fell (leniency). Here, the critic's **advice got worse** as the design got better (it invents faults to have something to say). Both mean: a critic's verdict on a late-round candidate is less trustworthy than on a first draft. A critic must be allowed to say "nothing to fix" (the "Unknown" exit, V9), and the loop must stop.

Addition to V5: **Judge Anything** (arXiv:2503.17489, 2025; abstract read). Five MLLM judges (GPT-4o, Gemini 2.0 Flash and three others) agreed with humans less on **generated** outputs (pairwise 53.4 %, score 30.1 %) than on understanding tasks (66.6 %, 42.8 %). Pairwise beat absolute scores in both. **Weak** (abstract).

### V12. Era: what counts as good design changed, and a model's sense of "good" is its training era's average

- **Goree, Crandall, Doosti, Su, "Investigating the Homogenization of Web Design"** (CHI 2021; abstract seen through a search result only; the PDF link redirected and was not read). Websites of 2003–2019 became "significantly more similar since 2007"; the mean layout distance fell by more than 30 %. Designers named shared libraries, standard colour schemes and mobile support as causes. **Weak** (abstract via search; pre-2023, but it measures the change itself).
- **Anthropic, "Improving frontend design through Skills"** (claude.com/blog, 12 Nov 2025; read). "Safe design choices ... dominate web training data", which gives "what users call the 'AI slop' aesthetic": "purple gradients on white backgrounds", "Inter, Roboto, Arial, system fonts", "predictable layouts". Models "still tend to converge on common choices (Space Grotesk, for example)". No measured evaluation. **Strong** as a first-party statement of the generator's default; it is an era-bound marker of 2024–2025.

Era flags on the sources in this file:

| Source | Principles tested | Era label | Dated? |
|---|---|---|---|
| UICrit (V1) | Nielsen heuristics, contrast, readability, layout | Heuristics timeless; screens era-bound | **Yes**: RICO Android screens, about 2016–2017 (Material 1) |
| MLLM as a UI Judge (V1) | ease of use, trust, aesthetic, interest | Perception timeless; "aesthetic" era-bound | Recent email designs; undated |
| Haraguchi (V3) | alignment, overlap, white space | Timeless (Gestalt, legibility) | 2020s templates; rule metrics from 2014 |
| ArtifactsBench (V4) | layout, fidelity, motion, feedback | Mostly timeless; "polish" era-bound | 2025 |
| BlindTest, UI-Lens (V6) | overlap, overflow, geometry | Timeless | No |
| Duan CHI 2024 (V11) | Nielsen (1994), CrowdCrit (2015) | Mostly timeless; "aesthetic and minimalist" era-bound | Guideline sets are old; the study is 2023–2024 |
| ArtCoT (V10) | artwork beauty | Era-bound (2024 experts) | No |
| Anthropic blog (V12) | typography, colour, backgrounds | Era-bound (anti-2024 defaults) | Will date |

Meaning (judgement): a VLM judge with no reference prefers the **average** of what it saw in training. That average is the convergent "template" look that the founder and Anthropic both reject. So a generic "is this good design?" question pulls toward the era's average. Questions about timeless principles (contrast, grouping, hierarchy, legibility) are safer to give a model. Questions about taste and novelty must be anchored in the founder's own references (the vault) and his verdicts.

## Synthesis

### S1. Does F1–F7 transfer to visual judging?

| Text finding | Visual evidence | Verdict |
|---|---|---|
| F1. Critique-then-revise helps only as far as the critic is right | The visual critic is right less often on fine detail (V3, V6). Its accuracy **fell** across revision rounds while the design improved (V11). With a reference image, self-revision gives a small gain (V7, Design2Code). | **Transfers, and stronger.** |
| F2. Iterating against a judge: judge score rises, human score falls; worst with shared context | No visual replication of Pan et al. Anthropic: scores plateau; a middle round often preferred (V2). Image RL against aesthetic rewards hacks them (V7, snippets). Published "iteration gains" on UI are all measured by a VLM judge (V7). | **Probably transfers; not shown.** The shared-context result has no visual test. Practitioners separate the critic (Duan 2024 uses different models; Anthropic uses a separate evaluator). |
| F3. One judge is noisy, self-preferring | Repeat runs agree 61–68 % (V5). Self-leniency on LLM output (V2). Decoration and polish inflate scores; prompts do not remove it (V5). Judges can ignore the image (V5). | **Transfers, and adds a visual bias.** |
| F3. Yes/no checklists beat holistic scores | Split dimensions: 69.5 % against 48.5 % agreement (V7). Decomposed art critique turned Claude 3.5 from −0.26 to +0.61 (V10). Pairwise beats absolute scores (V5). But **free "step by step" reasoning hurt** 2024 VLM judges (V5, V10). | **Transfers**, with one difference: ask concrete, staged questions; do not ask for open reasoning. |
| F3. Panels help by mixing model families | One summary says an ensemble aligned best (Judge Anything); no Claude-only panel study. | **Unknown.** |
| F5. Rule conflicts | No visual study. | Judgement: same shape. |
| F6. Calibration to one person | Personal aesthetic prediction 0.557 against group 0.708 (chance 0.333) (V10). Few-shot calibration aligned Anthropic's evaluator to its author (V2). | **Transfers.** One person is harder than the crowd. |
| F7. Anthropic guidance | Same guidance, plus vision rules: crop, image before text, PNG, check the downscale (V9). | **Transfers, with additions.** |

**New in visual work (no text equivalent):**
1. **Pixel blind spots.** Small misalignment, overlap, overflow and close geometry are near chance from pixels (V3, V6).
2. **Downscaling.** A full-page screenshot is reduced until small text and spacing are not visible (V9).
3. **Code plus screenshot beats either alone** (V4: 79 % code only, 87 % one screenshot, 91 % several).
4. **Close candidates are near chance.** A model separates a good UI from a weak one (about 93 % on large gaps), but not two good ones (V1).
5. **Late-round critics invent faults** (V11) as well as passing too easily (V2).

### S2. Which principles: pixels, code or a person

| Principle | Best route | Era | Evidence |
|---|---|---|---|
| Text overflow, clipping, truncation | **Code**: DOM `scrollWidth > clientWidth`, rendered at each target width | Timeless | V6 (F1 20 % from pixels) |
| Overlap of elements | **Code**: element boxes; pixels only for overlap of drawn content | Timeless | V6, V11 (JSON boxes give false overlaps on transparent images) |
| Small misalignment, spacing grid, consistent gaps | **Code**: computed positions and margins | Timeless | V3, V11 |
| Colour contrast | **Code**: computed colours and the WCAG ratio; pixels sample for text on images | Timeless need; WCAG 2.x thresholds are a 2008–2023 standard | V6, V11 |
| Font sizes, tap-target sizes, line length | **Code** | Thresholds partly era-bound (mobile era) | judgement |
| Ease of use | **Interaction** (Playwright run) or a person; a static screenshot is at chance | Timeless | V1 (Claude −0.05), V2 |
| Large misalignment, gross clutter, broken layout | **Pixels** (VLM) | Timeless | V3 (good on large faults) |
| Visual hierarchy, focal point, Gestalt grouping at page scale | **Pixels**, as concrete yes/no questions | Timeless | V1, V11 (mixed) |
| Coherence ("a whole, not parts"), "looks like a template" | **Pixels**, against named references | Era-bound | V2, V12 |
| Mood, brand fit, "interesting" | **Pixels** for a first filter; the founder for the choice | Era-bound | V1 (interest best), V10 |
| Choice between two good candidates | **The founder** | Era-bound | V1 (near chance on small gaps), V10 |

## Recommendations, ranked

Confidence is my estimate that the step improves agreement with the founder's verdicts, or removes the named fault. The design round already has a fresh critic per round, the founder narrowing five to three, and scripts that measure motion and curves (`plugin/skills/design-critique/SKILL.md`, `plugin/skills/design-round/SKILL.md`).

1. **Take measurable principles away from the VLM.** Add DOM checks, at each target viewport width, for overflow and clipping, element overlap, contrast ratio, alignment and spacing to a grid, and minimum sizes. The critic reports their output and never judges these from a screenshot. Evidence: V3, V6, V11 (Moderate); V9 (Strong). **Confidence 85 % (75–92 %).**

2. **Show the critic what it can see.** Viewport-size PNG crops (one per section, plus key states), the image before the question, and the page code or a DOM summary beside it. Never a single full-page screenshot. Evidence: V4 (Moderate), V9 (Strong). **Confidence 80 % (65–90 %).**

3. **Ask concrete yes/no questions per principle, with an "Unsure" exit, in a fresh context; compare candidates pairwise, not by a score.** One question per principle ("Is there exactly one element the eye lands on first? Name it."); stages: describe, then critique, then verdict; no open "think step by step". Swap the order of each pair and count a flip as "Unsure". Do not show the critic earlier rounds, the generator's transcript or its own past verdicts (the round already does this). Treat `impeccable critique`'s numeric score as information, never as a target. Evidence: V5, V7, V10 (Moderate); F3, F7 (Strong/Moderate). **Confidence 70 % (55–80 %).**

4. **No revise-until-pass loop. One targeted fix and one re-check, keep the best version, and the founder chooses among different candidates.** The critic is a filter for gross faults and broken rules, not a judge of taste. "Nothing to fix" is a valid answer and must be in the prompt. Evidence: V11 (critic worse in late rounds), V2 (middle round often best), V7, F2. **Confidence 75 % (60–85 %).**

5. **Escalate splits, flips, "Unsure" and rule conflicts to the founder** as one plain question each (the business-correspondence pattern). Evidence: F3, F5, V5 (run-to-run 61–68 %). **Confidence 65 % (50–78 %).**

6. **Calibrate the critic on the founder's past design verdicts before trusting it, and report the agreement.** Use the vault's references and his round decisions as few-shot examples with the reason he gave. Expect low agreement on close pairs; report it rather than hide it. Evidence: V10, V2, F6. **Confidence 55 % (40–70 %)** that it raises agreement measurably; 85 % that the first calibration run shows agreement well below his own consistency, as the mantahostels run did.

7. **Give a generation step fewer subjective rules.** Stage the rules (structure and hierarchy, then type, then colour and detail), and keep measurable rules out of the prompt because a check enforces them. Evidence: V8 (Moderate, on text and code rules, not design). **Confidence 50 % (35–65 %).**

Not recommended: a single holistic "design score" to climb; more rounds of the same critic; a full-page screenshot as the only input; asking the critic for taste between two close, good candidates.

## What we do not know

- No study runs Pan et al.'s design (iterate against a VLM judge, humans rate each round, shared against separate context) on visual design.
- No study measures a VLM's preference for its own visual output.
- No study measures how many subjective design rules a model keeps in one generated UI.
- Whether a Claude-only panel (several fresh Claude critics) gains anything over one; whether current models (Claude 4.7 and later, high-resolution tier) close the BlindTest and UI-Lens gaps. Most numbers here are for 2023–2025 models.
- Whether step-by-step reasoning still hurts current reasoning-model judges (V5, V10 are 2024 models).

## Bound

**Read in full or nearly in full (main text):** Anthropic "Harness design for long-running application development" (2026); Anthropic Vision docs; Anthropic "Demystifying evals for AI agents" (relevant passages); Anthropic "Improving frontend design through Skills"; MLLM as a UI Judge (arXiv:2510.08783).

**Read in part (main results; truncated pages):** UICrit (2407.08850, about 85 %); Duan CHI 2024 (2403.13139, about 70 %); MLLM-as-a-Judge (2402.04788, about 80 %); Visual Prompting with Iterative Refinement (2412.16829, about 80 %); Haraguchi (2410.08885; figures with r values not in text); ArtifactsBench (2507.04952); Design2Code (2403.03163); Vision-Guided Iterative Refinement (2604.05839); IFScale (2507.11538); FollowBench (2310.20410, tables only); ArtCoT (2501.09012); GPT-4V personal aesthetics (2403.03594).

**Abstract only:** BlindTest (2407.06581); UI-Lens (CVPR 2026, poster page; paper returned 403); UXBench (2606.13192); Fooling the LVLM Judges (2505.15249); MM-JudgeBias (2604.18164); Judge Anything (2503.17489); ManyIFEval (2509.21051); WebGen-V (2510.15306); AesBench (2401.08276, via search summary); 1D-Bench (2602.18548).

**Search snippet only, not opened:** Goree et al. CHI 2021 homogenisation (PDF redirected); reward hacking in T2I RL (2601.03468, 2509.07027); PDF accessibility benchmark (2509.18965); "Can Multimodal LLMs Model Expert Ratings in Mobile UI Usability Evaluation?" (Springer chapter; claims kappa ≥ 0.81 on visual dimensions for GPT-5, Claude 4 and Qwen-3; **not verified**, and it conflicts with V1, so do not rely on it without reading it); BlindTest sequel (Auburn news item).

**Not found after search:** a visual replication of Pan et al.; VLM self-preference on visual output; a Claude-only panel study; a many-subjective-design-rules generation benchmark; a VLM colour-contrast benchmark on web screenshots.

The evidence base in mantahostels `docs/research/correspondence-draft-quality.md` was read in full; its sources were not re-read.


