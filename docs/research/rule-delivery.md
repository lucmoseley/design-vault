# How the researched design rules reach the builder and the critics (design-vault#211, map #202)

Question (#211, 15 Oct 2026): how must the house's researched design rules get to the agents that apply them, so that each agent applies all of its rules well when the number of rules increases? The options are: all rules at one time; rules split by part or by topic; or passes from coarse to fine. The agents are the building session (`design-round`), the critic (`design-critique`) and the three gate critics (`plugin/skills/design-round/references/gate-check.md`).

The founder (15 Oct 2026): "if we just dumped it all in, or even all the rules in, we'd get a very poorly functioning skill, because any agent reading it would be overloaded with information in a way that meant it wouldn't apply it all smoothly. Perhaps the skill works by reviewing at a coarse grain, apply those rules, then moving finer and finer. Perhaps that's a terrible idea."

Written in ASD-STE100 Simplified Technical English.

Evidence labels (the same as #99): **Strong** (peer-reviewed or first-party, read), **Moderate** (primary read in part, or a preprint read), **Weak** (abstract only, or one small study), **judgement**. Each model-specific result gives the model and the date. Token counts are characters divided by 4. This is approximate (English prose is about 3.5 to 4.5 characters for each Claude token).

## Part A. What each agent loads today (measured 15 Oct 2026)

### A1. The critique critic (design-round §4: one fresh critic; gate-check §3: the "critique critic")

Always loaded on a web page for a Manta round:

| File | Lines | ~Tokens |
|---|---|---|
| `plugin/skills/design-critique/SKILL.md` | 115 | 3,900 |
| `plugin/skills/design-critique/gate.md` (all 26 questions; the critic runs the craft gate) | 290 | 4,300 |
| `plugin/skills/design-critique/references/house-principles.md` (function walk, two orders) | 121 | 3,400 |
| `plugin/skills/design-round/references/impeccable.md` (the house overrides) | 109 | 3,200 |
| impeccable 4.5.0 `skills/impeccable/SKILL.md` | 86 | 3,000 |
| impeccable 4.5.0 `reference/critique.md` | 806 | 10,700 |
| impeccable 4.5.0 `reference/audit.md` | 137 | 2,100 |
| Manta `PRODUCT.md` and `DESIGN.md` (impeccable `context` loads them) | 325 | 6,100 |
| Manta gate (`.claude/skills/design-review/SKILL.md`) | 79 | 1,100 |
| **Total of instruction text** | **2,068** | **about 37,800** |

Conditional: `first-visit-trust.md` (80 lines, about 2,200 tokens) on a small-business site; Manta `docs/brand/brand-sheet.md` (462 lines, about 15,300 tokens) when the critic opens the project rules file. With both: about 55,000 tokens.

Not counted: the brief, the critic's examples (`critic-examples.js`), each script's output (`check-layout.py`, `check-measure.py`, `parts-map.py` and others), and the images. Each image costs about (width × height) / 750 tokens (Anthropic vision docs). A 1456 × 819 viewport image is about 1,600 tokens. On the high-resolution tier (long edge 2,576 px) one image can be about 4,800 tokens. Three candidates at two widths with crops can add 10,000 to 30,000 tokens.

Rule count in this load (approximate count of discrete checkable items): impeccable `critique.md` has 10 Nielsen heuristics (each with sub-checks), a cognitive-load checklist, 8 load violations and 5 personas (232 bullet lines, 104 table rows); `audit.md` 47 bullet lines; design-critique has 6 Gestalt principles, 5 conversion-and-trust checks, SEO, measure, the change standard and the function walk's questions; `gate.md` has 26 questions (about 9 to 14 apply to one web page). The census (#98, `docs/research/design-rules-census.md`) counted 84 vault rules and 53 Manta brand-sheet rules plus 12 more Manta rules, before #117, #123 and #127 added more. One critique critic therefore holds **well over 100 rules and checks in one context**.

### A2. The three gate critics (gate-check.md §3; not live, trial #169 only)

Each gate critic gets `gate/look.txt` (the look questions only, after the asset filter and after the script and code questions are answered), the parts key where `vault.affordance` is on the list, the fixed prompt in §3 (about 400 tokens), the brief, the candidates and its own examples.

Measured: `node gate.js list --asset web-surface --fact has-cta --look gate.md` prints **6 look questions, 16 lines, about 440 tokens**. For `brand-art` it prints 2 questions. So the gate critic's rule load is already small: **6 rules, one question each, yes / no / unsure**. Its total input is dominated by the images and the brief, not by rules.

### A3. The building session (design-round), round one of a web surface for Manta

| File | Lines | ~Tokens |
|---|---|---|
| `plugin/skills/design-round/SKILL.md` | 253 | 10,800 |
| `plugin/skills/design-round/references/impeccable.md` | 109 | 3,200 |
| impeccable `SKILL.md` | 86 | 3,000 |
| impeccable `reference/new-work.md` | 154 (long lines) | 14,700 |
| impeccable `reference/craft-floor.md` | 44 | 1,100 |
| impeccable `reference/mode-<mode>.md` and `region-map.md` | 45 | 1,700 |
| `design-critique/references/surface-styling.md`, `text-presentation.md`, `brand-palette.md` | 200 | 6,200 |
| `design-critique/SKILL.md` and `gate.md` (the builder runs the craft gate first, design-round §4) | 405 | 8,200 |
| Manta `PRODUCT.md`, `DESIGN.md`, `docs/brand/brand-sheet.md` | 787 | 21,400 |
| **Total** | **about 2,080** | **about 70,400** |

Conditional: `visualize.md`, `component-review.md`, `shape.md` (about 6,000 tokens); `prompts.md` and `roster.md` for brand art (about 8,700); `gate-check.md` (2,300). Later rounds load one or more axis commands (14 files, about 21,700 tokens if all are loaded; normally one to three).

The builder is also one **long** session. It holds every tool output, render, critic report and founder reply across rounds. Its context grows far above 70,000 tokens in a multi-round brief. Context-length effects (Part B2) therefore apply to the builder most of all.

### A4. Splits that already exist in the house and in impeccable

1. **Scripts take measured rules away from every agent.** `plugin/skills/design-round/scripts/` holds `check-curves.js`, `check-overlay.py`, `check-flow.py`, `check-frames.py`, `check-layout.py`, `check-measure.py`, `check-access.py` (contrast, keyboard, focus, motion, flicker; being extended in the working tree), `parts-map.py` and `gate.js`. In gate-check §2, the script and code questions are answered **once, before any critic**, and `gate.js list --look` gives the critics **only** the look questions.
2. **Gate questions are one rule, one question, one answerer** (`gate.md`, "The form"): `applies-when`, `answered-by` (`script`, `code` or `look`) and `writes`. `gate.js list --asset <class> --fact …` drops every question whose asset condition fails. This is **selection by applicability**, done by code before the agent sees the list.
3. **The gate check splits by role across sessions**: three gate critics answer the look list only ("no critique, no score, no leader"); one critique critic does the open critique. A re-check uses three more fresh critics.
4. **impeccable splits by concern and by stage.** One command per concern (`typeset`, `colorize`, `layout`, `animate`, `clarify` and others; `design-round/references/impeccable.md` "The axis command"). Its `SKILL.md` step 3 loads `craft-floor.md` "After resolving analysis and direction … immediately before any UI edit … Do not load it for planning-only work."
5. **impeccable critique splits into two isolated assessments.** `critique.md` "Hard Invariants": Assessment A (design review) and Assessment B (detector and browser evidence) "MUST run as two isolated sub-agents", because detector output "still anchors judgment". `new-work.md` §7 sends the build to a separate `impeccable-finish-reviewer` agent, "fresh eyes on a done artifact, outside the build thread's attention gravity" (`agents/impeccable-finish-reviewer.md`).
6. **Nested subagents.** design-round §4 runs the critic as a subagent, and impeccable `critique` inside it asks for two more subagents (A and B). Claude Code allows this: "By default, a subagent can spawn subagents of its own, up to three layers below the main conversation" (code.claude.com/docs/en/sub-agents, read 15 Oct 2026). But the workflow-core session rules say "A subagent does not spawn subagents". Where the critic obeys that rule, impeccable runs A and B inline in one context, which `critique.md` calls a degraded run that must print `⚠️ DEGRADED: single-context`. In 50 production runs the critic ran the two assessments in one context, with no degraded banner and the detector first ([critic-transcripts.md](https://github.com/lucmoseley/design-vault/blob/b4a0b43d5/docs/research/critic-transcripts.md)). #212 Q7 has the building session dispatch them as isolated subagents.
7. **#121's dependency order is a coarse-to-fine sequence already in force for the critic.** `house-principles.md` gives function → role → treatment → value, and design-critique §0a runs "the function walk, before beauty" before §1. The order exists as an order of **decisions**; the rules are not yet **loaded** in that order.

## Part B. Outside evidence

### B1. Instruction-following falls as the number of rules increases

- **IFScale** (Jaroslawicz et al., Distyl AI, arXiv:2507.11538 v1, 15 Jul 2025, NeurIPS 2025; read in part). One task: write a business report that includes N keywords, N = 10 to 500. Results (accuracy at N = 10 / 50 / 100 / 250 / 500):
  - claude-opus-4 (May 2025): 100 / 100 / 94.6 / 67.9 / 44.6 %.
  - claude-sonnet-4 (May 2025): 100 / 98.0 / 94.4 / 77.2 / 42.9 %.
  - gemini-2.5-pro: 100 / 99.6 / 98.4 / 84.8 / 68.9 %. o3 (high): 100 / 99.6 / 98.2 / 97.8 / 62.8 %.
  - Three decay shapes: threshold (reasoning models), linear (claude-3.7-sonnet, gpt-4.1), exponential (claude-3.5-haiku, gpt-4o).
  - **Primacy bias**: earlier instructions are followed more. The gap is largest at about 150 to 200 instructions; above 300 the failure becomes uniform.
  - As density increases, models mostly **omit** a rule, not modify it.
  - Thinking on Claude models gave "moderate gains" at high density.
  - Limit (the authors): one task type, simple keyword rules, English, business domain. **Moderate.**
- **Arize replication and extension** (Laurie Voss, Arize AI blog, May 2026; read in part, the charts were not readable as text). The same keyword task with a 10,000-word vocabulary. Claude Sonnet 4 reproduced the paper within 3 points at low density. **Claude Opus 4.7**: "still beginning to forget" at high N; "By N=5,000, it was only following about half of them." GPT 5.5 held 99 % to N = 5,000. The author: the point where models start to lose instructions moved from about 200 to 300 (2025) to "closer to 2,000" (2026), and the result is "not proof that every kind of instruction in them is followed". **Weak** (one blog, charts not read, keyword rules only).
- **ManyIFEval and StyleMBPP** (Harada et al., "When Instructions Multiply", EMNLP 2025 Findings, arXiv:2509.21051; read in part). Prompt-level accuracy (all rules met) against the count:
  - ManyIFEval, 1 → 10 text instructions: **Claude 3.5 Sonnet (Jun 2024) 0.95 → 0.48**; GPT-4o 0.94 → 0.21; o3-mini (high) 1.00 → 0.78.
  - StyleMBPP, 1 → 6 code-style instructions: **Claude 3.5 Sonnet 0.96 → 0.01**; GPT-4o 0.93 → 0.68. One rule ("characters per line") fell from 97 % alone to 2 % with five others.
  - Each single rule stays high (Claude instruction-level 0.95 → 0.93 on ManyIFEval). The **all-rules** rate falls. A logistic model on the count alone predicts the rate within about 10 %.
  - **A judge inflates compliance as the count increases**: GPT-4o as judge gave 0.657 against 0.213 rule-based at n = 10 (0.815 against 0.574 at n = 5). **Moderate.**
- **FollowBench** (ACL 2024; from #99 V8): GPT-4 all-constraints 84.7 % at one constraint, 61.9 % at five; style constraints held better. **Moderate**, 2023 models.
- **AGENTIF** (Qi et al., arXiv:2505.16944, May 2025; read in part). Real agent system prompts: average 1,723 words, 11.9 constraints. Best constraint success rate 59.8 % (o1-mini); Claude 3.5 Sonnet (Oct 2024) about 56.6 %. **Condition constraints** (a rule that applies only when X) are among the weakest; over 30 % of their errors are a wrong condition check. Above 6,000 words, instruction success is "nearly 0" for all models. **Moderate.**
- **RuleArena** (Zhou et al., ACL 2025, arXiv:2412.08972; read in part). Real rule sets (airline baggage, NBA trades, tax), about 360 to 400 tokens per rule. Claude 3.5 Sonnet 0-shot accuracy, airline levels 1/2/3: 0.04 / 0.00 / 0.01; o1-preview 0.54 / 0.37 / 0.21. Models "struggle to identify and apply the appropriate rules" and confuse "similar but distinct regulations". **Irrelevant rules added to the input "significantly degrade" every model; the same length of meaningless tokens gives only a "minor" drop** (Appendix D.2.4; numbers only in a figure, not read). **Moderate.** Remove them before the agent reads, not only shorten the file.
- **Order Matters** (Zeng et al., ACL 2025 Findings, arXiv:2502.17204; read in part). 7 constraints in one instruction. **Hard-to-easy order beats easy-to-hard**: about 7 points in one prompt (LLaMA3-8B), about 25 points when the constraints come over several turns. Models: LLaMA, Qwen, Mistral, GPT-4o-mini; no Claude. **Weak to Moderate** (small open models, 2024 to 2025).

**Transfer to current Claude models (judgement).** The keyword results moved by about ten times in one year (Arize, 2026). For **simple, independent, checkable** rules, a 2026 Claude model holds hundreds of rules. The house's rules are different in four ways that each lower the limit: they are **conditional** (AGENTIF: condition constraints are weakest), they **interact and clash** (#121), they are applied to **an image** (#99 V6: fine geometry near chance), and they are applied to **one's own work or by a judge** (ManyIFEval: a judge inflates compliance with the count; #99 V2: self-leniency). No study measures subjective design rules in one UI (#99 V8; searched again 15 Oct 2026, not found). The shape of the curve (each added rule lowers the chance that all hold; earlier rules win; omission, not error) probably transfers. The numbers do not.

### B2. Performance falls as the context gets longer, at fixed difficulty

- **Context Rot** (Hong, Troynikov, Huber, Chroma technical report, 14 Jul 2025; read in part). 18 models including Claude Opus 4, Sonnet 4, Sonnet 3.7, Sonnet 3.5, Haiku 3.5. Task difficulty held constant, length increased: performance "grows increasingly unreliable as input length grows". "Even a single distractor reduces performance relative to the baseline." Coherent text hurt more than shuffled text. **LongMemEval: about 300 focused tokens beat about 113,000 tokens "across all models"**; Claude showed the largest gap, much of it as abstention ("cannot find the answer"). **Moderate.**
- **Lost in the Middle** (Liu et al., TACL 2024, arXiv:2307.03172). Performance "is often highest when relevant information occurs at the beginning or end", and "significantly degrades" in the middle. **Strong** for 2023 models; the size of the effect is smaller in 2025 models (Context Rot found no needle-position effect in its simple task).
- **NoLiMa** (Modarressi et al., ICML 2025, arXiv:2502.05167; abstract read). Where the question and the answer share no literal words, 11 of 13 models fell below 50 % of their short-context score at 32K tokens; GPT-4o 99.3 → 69.7 %. **Moderate.** Judgement: a design rule ("a control's edge needs 3:1") and the part it applies to (a grey 1 px box in a render) share no words. Applying a rule is a non-literal match, the hard case.
- **Anthropic, "Effective context engineering for AI agents"** (29 Sep 2025; read in part). Context is "a finite resource with diminishing marginal returns"; LLMs "have an 'attention budget'"; "Every new token introduced depletes this budget"; "a performance gradient rather than a hard cliff". On prompts: teams "stuff a laundry list of edge cases into a prompt … We do not recommend this." Target the "right altitude": "specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics". "Just in time" loading "keeps the agent focused on relevant subsets". A subagent may use "tens of thousands of tokens or more" but returns "1,000-2,000 tokens". **Strong** (first-party practice; no figures).
- **Anthropic prompting best practices** (platform.claude.com, read 15 Oct 2026; covers current models including Opus 5.5). For inputs over 20,000 tokens, put long documents at the top and the query at the end: "Queries at the end can improve response quality by up to 30 percent in tests". Claude "maintains orientation across extended sessions by focusing on incremental progress, making steady advances on a few things at a time rather than attempting everything at once". Opus 4.5 and later "are also more responsive to the system prompt than previous models" (dial back "CRITICAL: You MUST"). **Strong.**

Meaning for the house (judgement): the critique critic's 38,000 to 55,000 tokens of rules plus images, and the builder's 70,000 tokens plus a long session, are in the range where every source above shows loss.

### B3. One pass against many: decomposed critique and checklists

For a judge, the evidence favours splitting the judgement:

- **Anthropic, "Demystifying evals for AI agents"** (9 Jan 2026; read): "grade each dimension with an isolated LLM-as-judge rather than using one to grade all dimensions"; allow "Unknown"; "run multiple trials". **Strong** (first-party practice).
- **Counter-example, Anthropic "How we built our multi-agent research system"** (13 Jun 2025; read in part): they "experimented with multiple judges to evaluate each component", but "a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade" with **five** rubric criteria "was the most consistent and aligned with human judgements". **Strong** as first-party practice. Judgement: with five broad criteria on text, one call won; the January 2026 advice is newer and general. The split pays as the criteria increase and as they need different evidence.
- **Branch-Solve-Merge** (Saha et al., NAACL 2024, arXiv:2310.15123; abstract read). Split an evaluation into criteria branches, judge each, merge: human-LLM agreement up "by up to 26%", length and position bias down "by up to 50%"; constraint satisfaction in generation +12 %. Models: Vicuna, LLaMA-2-chat, GPT-4 (2023). **Moderate.**
- **CheckEval** (Lee et al., EMNLP 2025, arXiv:2403.18771 v3; abstract read). Criteria decomposed into yes/no questions; agreement across 12 evaluator models up by 0.45 on average, lower variance. **Moderate.**
- **TICK** (Cook et al., arXiv:2410.03608, Oct 2024; abstract read). Generated checklists raised exact agreement with human preference from 46.4 % to 52.2 %; checklist self-refinement +7.8 % (LiveBench reasoning). **Moderate.**
- **Against a blanket checklist: Furuhashi et al.** (EMNLP 2025, arXiv:2508.15218; abstract read). "selective checklist use tends to improve evaluation performance in pairwise settings, while its benefits are less consistent in direct scoring". **Moderate.** Meaning: a checklist helps where items are selected for the case, not every item every time.
- **Visual judges** (from #99): a multi-dimension visual judge agreed with human votes 69.5 % against 48.5 % for a single score (V7, Claude 4.5 Sonnet as critic, 2026); a decomposed art critique took Claude 3.5 Sonnet from −0.26 to +0.61 rank correlation (V10, 2025); free "step by step" reasoning hurt 2024 visual judges (V5). **Moderate.**

### B4. Separate calls against steps in one prompt

- **Prompt chaining against a stepwise prompt** (Sun et al., ACL 2024 Findings, arXiv:2406.00507; abstract read). Draft, critique and refine as three separate prompts beat the same three steps in one prompt. The authors: the one-prompt version "might produce a simulated refinement process". **Moderate** (summarisation; 2024 models).
- **Anthropic prompting best practices** (read 15 Oct 2026): "Explicit prompt chaining … is still useful when you need to inspect intermediate outputs or enforce a specific pipeline structure"; the common chain is "generate a draft → have Claude review it against criteria → have Claude refine", "Each step is a separate API call". **Strong.**
- **writing-for-agents** (workflow-core 1.3.14): hiding later steps to stop premature completion "only works across a real context boundary (a hand-off or a subagent dispatch; an inline call leaves the later steps in context and clears nothing)". House doctrine, consistent with Sun et al.
- **impeccable 4.5.0** keeps its two critique assessments in isolated subagents because detector output "still anchors judgment", and sends a finished build to a separate finish reviewer "outside the build thread's attention gravity" (Part A4.5). Practitioner design, not a measurement.

Meaning (judgement): **a coarse-to-fine sequence inside one context is weaker than the same sequence across fresh contexts.** In one context, all the fine rules are already loaded at the coarse pass, and the passes after the first can be "simulated".

### B5. Splitting generation by part or by stage

- **DCGen** (Wan et al., FSE 2025, arXiv:2406.16386; abstract read). Screenshot-to-code: GPT-4o on a whole screenshot made three error types, "element omission, element distortion, and element misarrangement"; working segment by segment gave "up to a 15% improvement in visual similarity". **Moderate.** This is a split **by part** for a copy task (a reference image exists).
- **APD-Agents** (Chen et al., arXiv:2511.14101, Nov 2025; numbers from a search summary only, not read). Mobile page layout on RICO: coarse-to-fine placement against one-go: mIoU 0.471 against 0.407, placement accuracy 85.6 % against 65.8 %, but worse on two overlap metrics; one-go failed on 18 % of pages, "mostly because too many elements overwhelmed the model". **Weak.**
- **Anthropic, "Improving frontend design through Skills"** (12 Nov 2025; read in part): the frontend skill is "a ~400 token prompt – compact enough to load without bloating context", split into four dimensions (typography, colour and theme, motion, backgrounds), loaded "just-in-time". **Strong** as first-party practice; no measurement.
- **Anthropic, harness design** (24 Mar 2026; from #99 V2): generator and evaluator are separate agents; four named criteria. **Strong** as practice.
- No study found measures a generator given all design rules against the same rules in stages (searched 15 Oct 2026, "layout first then styling staged pipeline ablation", and #99 V8). The gap is open.

### B6. Anthropic's guidance on skills and progressive disclosure

- **Skill authoring best practices** (platform.claude.com, read 15 Oct 2026). "Keep SKILL.md body under 500 lines for optimal performance". "Pattern 2: Domain-specific organization … to avoid loading irrelevant context". "Keep references one level deep from SKILL.md": from nested references Claude "might use commands like `head -100` to preview content rather than reading entire files, resulting in incomplete information". Reference files over 100 lines need a table of contents. "Prefer scripts for deterministic operations"; utility scripts are "More reliable than generated code" and "Only the script's output consumes tokens". Feedback loops: "Run validator → fix errors → repeat". **Strong.**
- **"Equipping agents for the real world with Agent Skills"** (Zhang, Lazuka, Murag, 16 Oct 2025; read in part). Three levels: metadata, SKILL.md body, linked files. "If certain contexts are mutually exclusive or rarely used together, keeping the paths separate will reduce the token usage." **Strong.**

Checks against the house (measured in Part A): `design-round/SKILL.md` is 253 lines (inside 500) but about 10,800 tokens because of long lines. impeccable `critique.md` is 806 lines and is reached from impeccable `SKILL.md`, which design-critique reaches through `design-round/references/impeccable.md`: a **two-level chain** from the critic's own skill, the case where Claude may read only the first 100 lines. In production the critic read `critique.md` whole in about 14 of 18 reads ([critic-transcripts.md](https://github.com/lucmoseley/design-vault/blob/b4a0b43d5/docs/research/critic-transcripts.md)).

## Part C. The loading patterns, with evidence, cost and trade-offs

Cost terms used below (approximate, for one round of three web candidates):
- **D** = the fixed cost of one dispatch before it does work. The workflow-core session rules give about 26,000 tokens.
- **Images** = the renders one agent reads. Three candidates at two widths in viewport crops is about 18 images, about 29,000 tokens on the standard tier (1,600 each), more on the high-resolution tier.
- **Rules** = the instruction text in Part A.
- "Sessions" = fresh contexts dispatched. "Serial" = each waits for the one before it.

These are context sizes at the verdict, not billed tokens: a multi-turn agent re-reads its context every turn, and prompt caching changes the bill.

### C1. Pattern 1: all rules at once, in one context (the status quo)

- **Who uses it now.** The critique critic (about 38,000 to 55,000 tokens of rules, 100+ rules and checks) and the builder (about 70,000 tokens of rules, in a session that grows across rounds).
- **Evidence for.** It is the simplest. Every rule is in view, so the agent can see two rules clash (#121 needs both rules side by side to name a clash). Anthropic's research-system judge did best as one call with five criteria (B3, Jun 2025).
- **Evidence against.** Each added rule lowers the chance that all hold (B1: Claude 3.5 Sonnet 0.95 → 0.48 at 10 rules; 0.96 → 0.01 at 6 code-style rules). Earlier rules win (IFScale primacy). Rules that do not apply hurt more than length (RuleArena). A judge checking many rules at once over-reports compliance (ManyIFEval). Long context with distractors loses (Context Rot, NoLiMa). Anthropic advises against "a laundry list of edge cases" (B2).
- **Cost.** One session. Critic: D + 38,000 to 55,000 rules + images ≈ 95,000 to 110,000 tokens at the verdict by this sum; measured in production, about 170,000 ([critic-transcripts.md](https://github.com/lucmoseley/design-vault/blob/b4a0b43d5/docs/research/critic-transcripts.md)). Builder: 70,000 tokens of rules before any work.
- **Trade-off.** Lowest session count and wall time. Highest risk that a rule is silently omitted.

### C2. Pattern 2: take each measured rule away from the agent (a script answers it)

- **Who uses it now.** gate-check §2: script and code questions are answered once, before any critic; `gate.js list --look` gives the critics only what is left. Scripts exist for curves, contacts, flow, length, end frame, layout and overflow, measure, contrast and access (`check-access.py`), and one target (`parts-map.py`).
- **Evidence.** Anthropic skills guidance: "Prefer scripts for deterministic operations"; "Only the script's output consumes tokens" (B6, Strong). Pixel judgement of small faults is near chance; code reads them with near-zero error (#99 V3, V6, V11; recommendation 1 at 85 % confidence). RuleArena: tools gave "a significant performance boost".
- **Cost.** Zero rule tokens for the agent; the script's output only (a few hundred tokens each). Script run time (`check-layout.py` about 3 minutes a page). Build and test cost of each script, once.
- **Trade-off.** Only for rules a measurement can settle. A script answers only what it was built for; a fault outside its checks needs the look. The script is the rule: a wrong threshold is wrong every time (calibrate it, as #99 asks).
- **Builder.** The builder runs the same scripts as a feedback loop ("Run validator → fix errors → repeat", B6). It needs the rule's **positive target** (what to build) but not the check's wording.

### C3. Pattern 3: select the rules by applicability before the agent reads them

- **Who uses it now.** `gate.js list --asset <class> --fact …` drops each gate question whose asset condition fails (a web page with no motion gets no motion questions; brand art gets 2 look questions, a web page 6).
- **Evidence.** RuleArena: irrelevant rules "significantly degrade" performance; the same length of filler does not. AGENTIF: condition constraints are among the weakest, with over 30 % of their errors a wrong condition check. So code that resolves the condition removes the error class the agent is worst at. Anthropic "Pattern 2: Domain-specific organization … to avoid loading irrelevant context" (B6).
- **Cost.** Each rule needs a machine-readable `applies-when` (#121 §5 form; `gate.md` "The form" already has it). Agent tokens fall by the share of rules that do not apply. No added sessions.
- **Trade-off.** A wrong tag hides a rule from every agent with no trace. Mitigation (judgement): `gate.js list` prints what it dropped and why, so a reviewer can see it. Only the asset-level condition is resolved by code today; the part-level condition ("each control") is still read by the agent.

### C4. Pattern 4: split by concern, one fresh agent for each group of rules (parallel)

- **What it is.** Several critics at once, each with one group of rules and the evidence that group needs: for example function and affordance; text and type; colour and surfaces; layout and hierarchy; motion; conversion, trust and SEO. impeccable already splits its **generation** this way (one command for each concern).
- **Evidence for.** Anthropic: "grade each dimension with an isolated LLM-as-judge rather than using one to grade all dimensions" (Jan 2026, Strong). Branch-Solve-Merge: agreement up to +26 %, bias down up to 50 % (Moderate, 2023 models). CheckEval, TICK, the multi-dimension visual judge 69.5 % against 48.5 % (#99 V7). Parallel subagents keep separate context windows and "separation of concerns" (Anthropic multi-agent research system, Jun 2025).
- **Evidence against.** Anthropic's research judge with five criteria was most consistent as one call. Multi-agent systems are "not a good fit" where agents need shared context (Jun 2025). Coherence ("a coherent whole rather than a collection of parts", #99 V2) is a whole-page judgement that no single concern critic sees. More critics raise more findings, and late or narrow critics invent faults (#99 V11: accuracy 52 % → 39 % across rounds).
- **Cost.** k sessions in parallel. With k = 5: 5 × (D + 3,000 to 8,000 rules + 10,000 to 30,000 images) ≈ 200,000 to 300,000 tokens, against about 100,000 for one critic. Wall time about the same as one critic. Multi-agent work used "about 15× more tokens than chats" at Anthropic.
- **Trade-off.** Each critic carries few rules (inside the range where B1 shows near-full compliance). The cross-concern view is lost unless one holistic critic stays (gate-check's critique critic already is that one). Clashes between concerns become invisible to each critic; `gate.js`'s clash report covers only questions with a `writes` field. More splits and Unsure answers reach the founder (gate-check §4 sends every split to him).

### C5. Pattern 5: split by part (each section or component checked alone)

- **What it is.** The agent judges or builds one region at a time, from a crop of that region.
- **Evidence.** DCGen: whole-screenshot generation omits, distorts and misplaces elements; segment by segment gave up to +15 % visual similarity (Moderate, a copy task). Viewport crops beat a downscaled full page (#99 V9 and recommendation 2). The function walk is already one row per part.
- **Cost.** One agent with crops: no added sessions, more image tokens (more crops). One agent per part: n sessions, n × D.
- **Trade-off.** Good for treatment and value rules (a border, a label's tracking). Bad for page rules: one primary action per view, hierarchy across sections, rhythm, alignment between sections (founder note N12), how busy the page looks (N7). These need the whole view.

### C6. Pattern 6: coarse to fine, in passes (the founder's idea)

- **What it is.** Rules in order of #121's dependency order: function → role → treatment → value. Each pass gets only its rules. A later pass may not change an earlier pass's decision (#121 §1: "the earlier step wins").
- **Evidence for.** Hard-to-easy order beats easy-to-hard, by about 7 points in one prompt and about 25 points over turns (Order Matters, small open models, Weak to Moderate). Three separate prompts beat the same three steps in one prompt, which can be a "simulated" refinement (Sun et al., Moderate). Anthropic: chain prompts where you need "to inspect intermediate outputs or enforce a specific pipeline structure" (Strong); Claude works best "making steady advances on a few things at a time rather than attempting everything at once" (Strong). APD-Agents: coarse-to-fine layout beat one-go on placement, lost on overlap (Weak). impeccable already defers `craft-floor.md` until "after resolving analysis and direction" (Part A4.4). #99 recommendation 7 (stage the rules for a generation step; 50 % confidence).
- **Evidence against or missing.** No study tests staged against all-at-once **design** rules (B5). Each pass that changes the candidate can break an earlier pass's result (gate-check §5 already asks "Does the change leave every other question … no worse?"). Repeated critic passes on one candidate lose accuracy (#99 V11).
- **Cost.** Across fresh contexts: 4 serial sessions for four stages, each with a small rule load: 4 × (D + 2,000 to 10,000 rules + images) ≈ 200,000 to 250,000 tokens, and about four times the wall time of one pass. A coarse fail can stop the later passes on that candidate, which saves their cost. In one context (staged reading only): no added session, a small token saving, little of the evidenced gain.
- **Trade-off.** The best fit to the evidence on ordering and on separate calls. The slowest pattern. It needs a rule to be tagged with its stage, which #121's form gives (`writes` maps to role, treatment or value).

### C7. Coarse to the eye, fine to the code (a synthesis of C2 and C6)

| #121 stage | Typical house rules | Who can answer it | Evidence |
|---|---|---|---|
| Function | affordance, borrowing, one primary action, one target, high-stakes | look (a critic), with `parts-map.py` giving the facts | #127, gate `vault.affordance` and others |
| Role | prominence ladder, colour role, which signifier | look, partly code (counting coral objects per view) | #121 §5.2 B12/B25 check |
| Treatment | border or fill or shadow; tint; underline; tracking | part code (computed styles), part look | #117, #123 |
| Value | contrast ratio, size, measure, radius on the scale, tokens | **code** (scripts) | #99 S2, V3, V6 |

So the founder's coarse-to-fine sequence and the script route meet: **the agents keep the coarse passes, where few rules apply and judgement is needed; the scripts take the fine passes, where rules are many and numeric.** Confidence (judgement): 0.65 that this division removes most of the rule-count risk for the critic; the open part is treatment rules that need the eye (for example whether a divider is needed, founder note N6).

### C8. Builder against critic

| Need | Builder (design-round) | Critic (design-critique, gate critics) |
|---|---|---|
| What it does with a rule | composes many rules into one artefact at the same time | checks a finished artefact against rules |
| Can it split by concern? | Only in part: type, colour and layout interact in one page. impeccable splits by concern **for later-round refinements** (one axis command each), not for round one | Yes: judging one concern does not need the others' rules |
| Natural stages | direction → structure and function → content → treatment → values and polish (impeccable new-work §1–§7; craft-floor after direction) | function walk first (§0a), then gates, then lenses |
| Context | one long session across rounds: context-length loss grows over time (B2) | fresh each round, short |
| Self-check | weak: self-preference and "simulated" self-review (#99 V2, B4) | fresh, but inflates compliance as its rule count grows (ManyIFEval) |
| Best lever (judgement) | load rules by stage (just in time), as positive targets; run the scripts as a feedback loop; start each round from a fresh context with the brief, the delta and the round folder, rather than a long carried session | few rules per critic; scripts first; one holistic critic kept for coherence and the leader |

A note on the builder's load: about 21,400 of its 70,400 tokens are Manta's own `PRODUCT.md`, `DESIGN.md` and brand sheet, and about 14,700 are impeccable `new-work.md`. The house's own share is about 34,000. A change to the house's files alone cannot halve the builder's load.

### C9. Summary table

| Pattern | Rules per agent | Sessions (one round, critic step) | ~Tokens at verdict, total | Strongest evidence | Main risk |
|---|---|---|---|---|---|
| 1 All at once | 100+ | 1 | ~100,000 | Anthropic 5-criterion judge (Strong, for few criteria) | silent omission; judge inflation |
| 2 Scripts | 0 for measured rules | 0 added | script output only | Anthropic skills guidance (Strong); #99 V6 | covers only measurable rules |
| 3 Select by applicability | the share that applies | 0 added | less than 1 | RuleArena distractors (Moderate); AGENTIF conditions | a wrong tag hides a rule |
| 4 By concern, parallel | 5 to 20 each | k (5) in parallel | ~200,000 to 300,000 | Anthropic Jan 2026 isolated judges (Strong); BSM, CheckEval | lost coherence; more noise; more founder questions |
| 5 By part | page rules lost | 0 to n | more image tokens | DCGen (Moderate) | page-level rules unchecked |
| 6 Coarse to fine, fresh passes | 5 to 20 each | 4 serial | ~200,000 to 250,000; less on an early stop | Sun et al.; Order Matters; Anthropic chaining (Strong as practice) | slow; later fixes break earlier passes |
| 6b Coarse to fine, one context | 100+ (staged reading) | 1 | ~100,000 | skills progressive disclosure | "simulated" passes |

Patterns combine. The gate check (#169) already combines 2, 3 and a form of 4 (three look critics on one short list, one holistic critic). The critique critic is still pattern 1.

### C10. Optional pressure test: not run

The baseline-against-staged test on one candidate was **not run**. It needs two to eight headless `claude -p` critic sessions with images (about 100,000 tokens each). A cheap design, for #212 to rule on: take a seeded fixture page with known faults across all four stages (for example under `test/fixtures/gate/affordance/` and `test/fixtures/access/`); run critic A with design-critique's full load; run critics B1 to B4 fresh, one for each #121 stage with only that stage's rules; score each against the seeded fault list (recall, false positives, rules named as applied); repeat three times for run-to-run spread (#99 V5: 61 to 68 % majority agreement).

## Part D. What we do not know

- No study measures many **subjective, conditional design rules** in one generated UI or one visual critique (#99 V8; searched again 15 Oct 2026).
- No study compares staged against all-at-once design rules for a generator, or per-concern against single visual critics with Claude 4.5 or later.
- Current-model numbers (Claude Opus 4.7, 2026) exist only for keyword rules, from one blog.
- The Manta brand sheet's actual use by the critic (always opened or only on demand) is not measured.

## Bound

**Read in full or nearly in full:** the workflow-core `writing-for-agents` skill (`SKILL.md`, `SKILL-MECHANICS.md`, 1.3.14); `docs/research/visual-critic-reliability.md` (#99); `docs/research/principle-interactions.md` (#121); `plugin/skills/design-critique/SKILL.md`; `plugin/skills/design-round/references/gate-check.md`; Anthropic "Skill authoring best practices" (platform.claude.com); issues #211 and #202 (bodies).

**Read in part:** `plugin/skills/design-round/SKILL.md` (headings, §4, pointers); `design-critique/gate.md` (header, form, Craft); `design-round/references/impeccable.md` (pin, precedence, stages); impeccable 4.5.0 `SKILL.md`, `reference/critique.md` (lines 1–60 and headings), `reference/craft-floor.md`, `reference/new-work.md` (headings and loading lines), `agents/impeccable-finish-reviewer.md` (head); `docs/research/design-rules-census.md` (totals); Anthropic prompting best practices (long context, chaining, subagents, state tracking sections); Anthropic "Effective context engineering", "Equipping agents … Agent Skills", "multi-agent research system", "Demystifying evals" (quotes checked 15 Oct 2026), "Improving frontend design through Skills"; Claude Code subagents docs (nesting and context); IFScale v1; ManyIFEval (arXiv:2509.21051 v1); AGENTIF (first 100,000 characters); RuleArena (v2, main text and Appendix D.2.4 text, not its figure); Order Matters (v1); Context Rot; Arize May 2026 blog (text, not charts).

**Abstract or abstract page only:** Branch-Solve-Merge (2310.15123); TICK (2410.03608); CheckEval (2403.18771); Furuhashi et al. (2508.15218); Sun et al. (2406.00507); Lost in the Middle (2307.03172); NoLiMa (2502.05167); DCGen (2406.16386); APD-Agents (2511.14101; its comparison numbers come from a search summary only).

**Carried from #99 without re-reading the source:** FollowBench, DeCRIM, the multi-dimension visual judge (2604.05839), ArtCoT, Duan CHI 2024, Anthropic harness design (Mar 2026).

**Measured:** line and character counts of every file in Part A (`wc`, 15 Oct 2026, working tree with another session's uncommitted edits to `gate.md`, `design-critique/SKILL.md` and `gate-check.md`); `gate.js list` output for `web-surface` and `brand-art`.

**Not done:** the pressure test (C10); a tokenizer count; a transcript check of what a live critic actually reads; a search of the Manta and mmm-infra round records beyond a grep for "DEGRADED" (no round hit).
