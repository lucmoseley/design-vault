# Research: what impeccable checks when it builds and critiques a candidate (design-vault#97, map #96)

Date: 13 Oct 2026.

Source: the plugin files in `~/.claude/plugins/cache/impeccable/impeccable/4.2.1/` and `.../4.5.0/`. In this file, `4.2.1:` and `4.5.0:` are short for `skills/impeccable/` in that version, unless the path starts with `agents/` or `hooks/`.

## Findings

### F1. `critique`: a holistic score plus fixed sub-checklists and persona questions (4.2.1 and 4.5.0 are identical)

Source: `4.2.1: reference/critique.md` (807 lines, read in full).

- **Two assessments in isolation.** Assessment A (design review, "Think like a design director") and Assessment B (detector plus browser overlay) "MUST run as two isolated sub-agents whenever a sub-agent/Task tool is exposed" (lines 7-8). "Assessment A must finish before detector findings enter the parent synthesis context" (line 10). Thus there are two reviewers, but they look at different things: one is an LLM, one is a deterministic scan.
- **Assessment A checks these items** (line 47-54):
  - Design specificity: "could an unrelated product use it unchanged?" One verdict, free text.
  - "Holistic design: hierarchy, IA, emotional fit, discoverability, composition, typography, color, accessibility, states, copy, and edge cases." This is a list of topics, not check questions.
  - Cognitive load: a fixed 8-item checklist (lines 321-332): single focus, chunking (≤4 per group), grouping, visual hierarchy, one thing at a time, minimal choices (≤4 options), working memory, progressive disclosure. The score is the count of failures: "0–1 failures = low ... 2–3 = moderate ... 4+ = high".
  - Emotional journey: peak-end rule, emotional valleys, reassurance. Free text.
  - Nielsen's 10 heuristics, each scored 0-4 against a 5-row grade table (lines 394-594). Each heuristic has 5 "Check for" bullets (50 bullets in total). A heuristic can be `n/a` with a one-line reason on Persuade or Experience surfaces (line 120). Total out of 40 (or the applicable maximum), mapped to 5 bands: Excellent 36-40, Good 28-35, Acceptable 20-27, Poor 12-19, Critical 0-11 (lines 602-610).
- **Issue grades.** Each priority issue gets a P0-P3 grade (lines 616-625). The tie-break for the grade: "Would a user contact support about this?"
- **Personas.** Five fixed personas (Alex power user, Jordan first-timer, Sam accessibility, Riley stress tester, Casey mobile), each with 5 test questions and 5-6 red flags (lines 637-770). The table selects 2-3 personas by interface type (lines 777-784). A landing page gets Jordan, Riley and Casey, not Sam. "If `CLAUDE.md` contains a `## Design Context` section from `impeccable init`", the agent makes 1-2 project personas (line 150, 790).
- **Output shape.** Health-score table, specificity verdict, overall impression, "What's Working" (2-3 strengths), "Priority Issues" (3-5, each with What, Why it matters, Fix, Suggested command), persona red flags, minor observations, provocative questions (lines 97-167).
- **Prior-run input.** "Read `.impeccable/critique/ignore.md` if it exists. Drop matching findings silently; it is the only prior-run input critique consumes" (line 29). The snapshot persists to `.impeccable/critique/`, and a trend line shows the last 5 scores (lines 185-217). The trend is a score history for one target. It does not record why the user rejected anything.
- **Re-check after a fix.** No automatic re-check. The text only tells the user: "Re-run `/impeccable critique` after fixes to see your score improve" (line 273). A re-run is a full critique, not a one-question re-check.
- **Ask the user.** After the report, 2-4 questions with concrete options (priority direction, design intent, scope, constraints). Required when there are 3 or more priority issues (lines 225-245).

Judgement: `critique` is a holistic, scored review with fixed sub-checklists. It is not a rule-by-rule check of a draft against a rulebook. Confidence 0.95.

### F2. `audit`: 5 scored dimensions with "Check for" topic lists; one verdict is pass/fail

Source: `4.2.1: reference/audit.md` and `4.5.0: reference/audit.md` (read in full, and diffed).

- "This is a code-level audit, not a design critique. Check what's measurable and verifiable in the implementation." "Don't fix issues; document them."
- 5 dimensions, each scored 0-4 with a one-line grade scale: (1) Accessibility, 7 check topics (contrast < 4.5:1, reduced motion, ARIA, keyboard, semantic HTML, alt text, forms); (2) Performance, 6 topics (layout thrashing, expensive animations, lazy loading, `will-change`, bundle size, re-renders); (3) Theming, 4 topics (hard-coded colours, dark mode, tokens, theme switching); (4) Responsive, 5 topics in 4.2.1 and 6 in 4.5.0 (fixed widths, touch targets < 44x44 px, horizontal scroll, text scaling, breakpoints; 4.5.0 adds "Broken touch interaction"); (5) Implementation Integrity: run the detector, verify each finding in context, look for "design-system drift, misleading or decorative content, and structure that is interchangeable with an unrelated product".
- Total out of 20, 5 bands (18-20 Excellent ... 0-5 Critical). The "Implementation Integrity Verdict" is the only explicit **pass/fail** item in audit.
- Each issue: P0-P3, location, category, impact, WCAG standard, recommendation, suggested command. "Positive Findings" is required ("Skip positive findings" is on the NEVER list).
- Re-check: only "Re-run `/impeccable audit` after fixes to see your score improve." No targeted re-check.
- **The only change in 4.5.0**: the touch-gesture check in Responsive. The 4.5.0 text also requires the agent to say "what produced the evidence (emulated viewport, synthesized touch, which engine, physical device) and what stayed untested".

### F3. new-work §7 "Inspect and finish": a bounded self-inspection, then the detector once, then a fresh finish reviewer

Source: `4.5.0: reference/new-work.md` (155 lines, read in full); a word-level diff against 4.2.1.

- **Self-inspection.** "Inspect the surface's target sizes in one batched screenshot round ... Critique the render against the user's request and the direction contract, fix material gaps, and confirm with one final round; two rounds is the ceiling" (§7 line 138). The SKILL.md core principle says the same: "Verify in bounded passes, not a loop ... confirm with at most one more round, and stop polishing."
- The self-critique has **no checklist**. It is "against the user's request and the direction contract" (six blocks: THESIS, OWN-WORLD, STORY, FIRST VIEWPORT, FORM, FINISH, §5 line 75). On a comp-led build, `comp-diff` scores each measured region `match`/`drift`/`missing`/`contradicted` against the approved comp; "a region it scores missing or contradicted is a fix whatever the page looks like from memory". On a Persuade surface it adds one test: "a first-time visitor should know what this is, why it matters, and what to do within seconds".
- **Capture validity before review** (line 140): settle entrance motion, capture from the document top, open each file and confirm "no black or blank regions, no wrong section behind a right filename".
- **Detector once.** "On the web, where this harness runs no design hook, run `impeccable detect --json` on the changed targets once here, fix what is mechanical, and pass the remaining findings to the reviewer" (line 142). Native platforms skip the detector.
- **Fresh reviewer, not a fork.** "spawn the reviewer fresh, with no forked conversation history ... a reviewer that inherits your transcript inherits your framing, your optimism, and your abstractions" (line 144). One reviewer, not several.
- **Fix loop with a targeted re-check.** On `fix`: "apply the material fixes in one batch, rebuild once, and recapture ... send the recaptured screenshots back to the same reviewer for a verdict scoring every material fix resolved, partial, or unresolved" (line 146). Note: the **same** reviewer (by agent continuation), not a fresh one. Only without continuation does a fresh pass run from `degraded/finish-reviewer.md`.
- **Stop rules** (line 146): "Two rounds is the budget an unattended run ends at"; in an attended session "put the table in front of them and let them choose"; "stop the moment a round resolves nothing"; "Consult the user only on a second rebuild directive". "The reviewer's findings are the only list you work from, never your own re-opened hunt."
- **User evidence wins** (line 150): "When the user answers a ship with evidence against it ... that evidence outranks every capture you made ... spawn a fresh reviewer for a new full review. Patching inline and self-certifying is how a rejected page ships twice."
- **What changed by 4.5.0 in §7**: (a) the two-round ceiling "never closes an open build-phase gate"; (b) on a comp-led build each fix batch reruns `build-phase advance`, and a final `build-phase finish --disposition ship` "rechecks the page and reopens responsive when it no longer holds"; (c) the documenter step must produce "token-bearing DESIGN.md **and** `.impeccable/design.json`, not prose alone". Confidence 0.9.

### F4. The finish reviewer: a fixed, ordered check list with a derived four-word verdict

Source: `4.5.0: agents/impeccable-finish-reviewer.md` (read in full); identical body in `reference/degraded/finish-reviewer.md` apart from a header for inline use.

- Tools `Read, Bash, Glob, Grep`; "You have no browser"; `maxTurns: 30`; "by roughly the tenth turn stop reading and write". It reviews screenshots and files only.
- **Anti-anchoring.** "inventory the comp's salient elements in your own words before reading the direction contract or any builder-authored summary: a review anchored on the contract inherits whatever the builder's abstraction dropped."
- **Seven checks, in order** (0-6): 0 Evidence (captures exist and are valid, else `disposition: recapture` and stop); 1 Persistence (PRODUCT.md, build state, approval records); 2 Fidelity (element matrix, each element `match`, `acceptable adaptation`, `missing`, `contradicted`, or `added without approval`; three mandatory rows TYPE, MATERIAL, GROUND); 3 Ceiling (against the QUALITY BAR card); 4 Contract, "promise by promise", for each block of the direction contract, plus the seed-key check and the memory test; 5 Truth (synthetic data labelled, no invented claims, every plate shipped); 6 Floor (the craft floor's Refuse list held against the screenshots).
- **Check 4 is the closest thing in impeccable to a rule-by-rule check of a draft**: it walks the direction contract block by block. But the contract is the build's own six-block brief, not a rulebook of yes/no questions. Confidence 0.85.
- **No "unsure" answer.** The verdict is "derived, never felt": `recapture`, `rebuild`, `fix`, or `ship`; "These four words are the whole vocabulary; never invent another." The one place the reviewer may decline to judge: GROUND with no comp and no named colour, where "the review says so in place of a verdict, because a target the reviewer invents turns the check into taste." The matrix row grades are categories, not ranks.
- **Output**: disposition line, then exactly five sections: `persistence`, `fidelity`, `ceiling`, `material_fixes` (ordered, at most eight), `keep` ("one line naming what must not be diluted while fixing"). "No praise, no summary prose."
- **Verdict pass (re-check).** After a fix batch: "you are scoring, not re-hunting ... For each material fix from your review, one line: resolved, partial, or unresolved"; "name at most three regressions the fix batch itself introduced"; "Unresolved or partial material findings can never recompute to ship". It re-checks every listed fix, not one question, and it is the same reviewer, not a fresh one.
- **Rule conflict.** The reviewer has a fixed precedence, not a stop: "A banned element is a material fix even when it matches nothing in the comp ... fidelity to a comp cannot authorize what the floor refuses"; "fidelity failures ahead of craft". It does not ask the reviewer to name conflicts between rules, and a conflict does not stop the run.

### F5. The `hooks on` detector: a mechanical lint of about 61 fixed rules, in two tiers, with an "Unsure" triage

Sources: `4.5.0: reference/hooks.md` (read in full; diffed against 4.2.1); `hooks/hooks.json` (both versions); `detect --help` from the engine binary; the rule table read out of the compiled engine binaries `~/.impeccable/bin/0.1.2/impeccable` (pinned by 4.2.1 `scripts/VERSION`) and `~/.impeccable/bin/0.1.11/impeccable` (pinned by 4.5.0). The engine is a compiled binary, so the rule list comes from its embedded strings, not from source. Confidence in the count: 0.8 (one name is inferred from its description; the table can hold rules whose names I did not separate).

- **What it is.** A deterministic scan. "HTML files: Static HTML/CSS analysis ... Non-HTML files: Regex pattern matching (CSS, JSX, TSX, etc.) ... URLs: Puppeteer full browser rendering". Exit 0 = clean, 2 = findings. Some rules are "advisory: detected and listed in a separate section, but never counted as failures" (em-dash overuse is the named one).
- **The rules, about 61, grouped as the engine groups them:**
  - *AI-tell ("slop") rules, 29:* side-tab accent border; thick accent border on a rounded card; overused font (Inter, Roboto, Fraunces, Geist, Plus Jakarta Sans, Space Grotesk and others); flat type hierarchy (steps under 1.25x); gradient text; purple/violet gradients and cyan-on-dark; cream/beige page background; nested cards; monotonous spacing; bounce or elastic easing; pulsing status dot; decorative blinking cursor; shape-assembled SVG illustration; organic contour drawn as `clip-path`; raster buried under a wash or opacity; glowing shadow accents; radial-gradient halo; radial spotlight glow; auto-scrolling marquee; icon tile above heading; italic serif display headline; hero eyebrow / pill chip; kicker or eyebrow above a heading; tiny numbered section labels; em-dash overuse (advisory); marketing buzzwords; aphoristic-cadence copy; oversized hero headline; crushed letter spacing.
  - *Quality rules, 23:* broken or placeholder image; uncaught script error; content invisible at rest; cards flush against a scroller edge; text occluded by an overlapping element; one column stretching the first viewport; gray text on a coloured background; low contrast (WCAG AA 4.5:1 and 3:1); layout-property animation; line length over ~80 characters; cramped padding; body text flush to the viewport edge; line height under 1.3; skipped heading level; heading closer to the block above than to its own content; justified text; body text under 12 px; functional text under 11 px; all-caps body text; wide tracking on body text; content overflowing its container; the same text three or more times in one container; positioned child clipped by an overflow container.
  - *Design-system rules, 4:* font, colour, radius and font size outside DESIGN.md (they read `DESIGN.md` / `.impeccable/design.json`; `--no-design-system` turns them off).
  - *Later "generated-UI signature" rules, 5:* hairline border plus wide diffuse shadow; repeating-gradient stripes; decorative grid-line background; "theater" framing copy; image scale or rotate on hover.
- **4.2.1 against 4.5.0.** All 61 rule names are in both engines (string check). The only rule text that differs is the cramped-padding description (reworded). Confidence 0.8.
- **Two tiers.** "The per-edit hook surfaces only the immediate tier: mechanical, unambiguous problems ... broken images, overflowing or clipped content, contrast and legibility failures, gradient text, glow shadows, and design-system drift. Everything else (copy cadence, palette and typography taste, layout rhythm) is deferred to a deep pass on the `Stop` hook event, which runs the full rule set over every UI file touched in the session". `hooks.json` wires `PostToolUse` on `Edit|Write` (timeout 5 s) and `Stop` (timeout 30 s, "Design deep pass"); 4.5.0 adds a `SessionStart` hook ("Preparing build session").
- **Re-check after a fix.** The per-edit hook re-runs on every edit, so a fix is re-checked mechanically: "findings get a correction prompt, pending issues get a re-nudge". The binary also says: "Findings marked attribution unknown may predate this session; do not treat them as regressions". On Claude Code the hook does not block; on Cursor it blocks the write, and after repeated denials of the same finding it lets the write through "to avoid a loop".
- **"Unsure" exists here, and only here.** Triage has three outcomes: "Real design problem: fix it"; "Confident false positive or sanctioned exception: persist the narrowest ignore yourself and disclose it"; "**Unsure**: leave the finding standing and ask the user in one line." It is for the builder's triage of a lint finding, not for a reviewer's verdict.
- **Exceptions carry a reason.** `ignore-value <rule> <value> --reason "<who decided: evidence>"`; "write 'user confirmed' only when the user actually did". `ignore-file` and `ignore-rule` need the user's approval. The exceptions live in `.impeccable/config.json` under `detector`. This is a log of accepted exceptions to lint rules. It is not a log of the founder's rejections of a design. Confidence 0.85.
- **The craft floor (`reference/craft-floor.md`, read in full, same in both versions)** is the human-judged partner of the detector: 9 "Verify" items (contrast, depth, spacing, type, motion, states, browser surfaces, copy, coverage) and 15 "Refuse" items (5 page scaffolds, 10 surface habits). Only the kicker/eyebrow is "a ban, not a default: no brief earns it back"; all other Refuse items are "the category's defaults, not bans: the brief's own words can earn any of them". The skill loads it "immediately before any UI edit".

### F6. impeccable does not read the project's own rules file; it reads PRODUCT.md, DESIGN.md, a surface brief, and its own config

Sources: `4.5.0: SKILL.md` Setup step 1; `reference/init.md`; `reference/critique.md` lines 29, 150, 790; a live run of `impeccable context` (engine 0.1.11) in a scratch project that held a `CLAUDE.md` and a `PRODUCT.md`; a string search of the engine binary.

- SKILL.md: `impeccable context` "loads PRODUCT.md, DESIGN.md, the matching surface brief, and native-platform guidance when applicable". The live run printed PRODUCT.md and a `RESOLVED_CONTEXT` block with `productPath`, `designPath`, `surfaceBriefPath`. It did **not** print or name the scratch `CLAUDE.md`. The engine binary holds no `CLAUDE.md` or `AGENTS.md` string.
- Other inputs that critique and the detector read: `.impeccable/critique/ignore.md` ("the only prior-run input critique consumes"); `.impeccable/config.json` and `.impeccable/config.local.json` (detector ignores, `buildPath`, hook settings); `DESIGN.md` / `.impeccable/design.json` for the 4 design-system rules; the direction contract inside the surface brief (finish reviewer).
- **One stale exception.** critique.md still says: "If `CLAUDE.md` contains a `## Design Context` section from `impeccable init`, also generate 1-2 project-specific personas". But init now writes PRODUCT.md only ("`init` captures durable product truth in PRODUCT.md"), and nothing in init.md writes a `## Design Context` section. So this path is dead on a project that init set up now. Confidence 0.85.
- Claude Code itself loads CLAUDE.md into each agent's context, so an agent that runs impeccable can see CLAUDE.md. But no impeccable step tells it to check the draft against CLAUDE.md or any other rules file. Confidence 0.8.
- Consequence for the house: `references/impeccable.md` is right that "the project's rules file wins over PRODUCT.md and DESIGN.md", and right that the rules file reaches impeccable only through those two files. A rule that is not copied into PRODUCT.md (for example under its "Product Principles" section, which the 4.5.0 product record adds) or into DESIGN.md is invisible to `critique`, `audit`, the finish reviewer and the detector. design-critique §1a and the project gate are the only places that check the rules file. Confidence 0.85.
- Side fact from the live run: the engine reports "installed v4.5.0, latest v4.5.2". This research did not read 4.5.1 or 4.5.2.

### F7. The axis commands `typeset` and `layout` also run two isolated assessments and a yes/no "Verify" list

Source: `4.5.0: reference/typeset.md`, `layout.md`, `colorize.md`, `animate.md`, `polish.md` (read in full). 16 reference files have a `## Verify` section.

- `typeset` and `layout` (the only two with "Two isolated assessments") run a design assessment and a `detect --scope type|layout` scan "independently"; "Do not let detector findings anchor the design assessment." The assessment has a fixed question list: 6 questions for type (authority and fit, hierarchy, scale and consistency, reading, stress, delivery), 7 for layout (reading order with "the squint test", grouping, rhythm, structure, density, adaptation, extremes). Each must be answered "with a file, selector, or computed value" / "rendered or source evidence".
- Their Verify lists end with: "Answer each item with rendered or source evidence, then rerun the scan. Do not substitute a bare 'yes' for verification." This is the nearest thing in impeccable to a yes/no rulebook with a re-check. It is run by the builder on its own work, not by a fresh reviewer. Confidence 0.85.
- `polish` reads the latest critique snapshot ("incorporate relevant P0/P1 findings ... Perform an independent pass either way"), triages in a fixed 5-level order (broken tasks first, cleanup last), and closes the snapshot only "when this pass clears every Priority Issue it took from a snapshot". This is the only cross-command re-check of critique findings.

### F8. Answers to the six yes/no questions in the brief

| Question | Answer | Where |
|---|---|---|
| Does it check a draft rule by rule? | **Partly.** The finish reviewer checks the direction contract "promise by promise" and classifies every salient element. Nielsen scores each heuristic; cognitive load counts 8 items; typeset/layout answer each question with evidence. None of these walks the project's own rulebook. | F1, F4, F7 |
| Does it re-check after a fix? | **Yes, in three places.** The finish reviewer's verdict pass scores each listed fix resolved/partial/unresolved and names up to 3 regressions. The hook re-scans every edit. typeset/layout "rerun the scan". `critique` and `audit` only tell the user to re-run. | F3, F4, F5, F7 |
| More than one reviewer? | **Two, of different kinds; never several of the same kind.** critique: Assessment A (LLM) and B (detector + browser) in isolated sub-agents. typeset/layout: same split. The finish reviewer is one fresh agent. | F1, F3, F7 |
| An "unsure" answer? | **Only for lint triage.** Hook triage: "Unsure: leave the finding standing and ask the user in one line." Reviewers have none: the finish reviewer's verdict has "exactly four" words; Nielsen allows `n/a` (does not apply), which is not "unsure"; the finish reviewer may say there is "no GROUND authority" instead of a verdict. | F4, F5 |
| Stop on a rule conflict? | **No.** It resolves conflicts by fixed precedence and continues: the brief beats a saturated-pattern warning ("Honor pinned aesthetics ... even when they conflict"); MODE RULES "win" over shared guidance; the floor beats the comp; "fidelity failures ahead of craft"; pinned constraints are kept "field by field" and the direction's material is translated "and name[d] ... in the presented direction". | SKILL.md, new-work §3, F4 |
| Calibrate to one person's taste? | **No persistent calibration.** It calibrates to the approved comp, the QUALITY BAR card ("never against the effort visible in the build"), and a model-bias "rendition prior" (cream/serif/lamplight). Taste enters per run through questions (critique's "Design intent", new-work §2) and the decision page. Durable carriers: a "standing preference as a brand commitment in PRODUCT.md", `buildPath` in config, `ignore.md`. "Redirecting a clear brief toward your taste is failure" refers to the model's own taste. | new-work §3-4, F4 |

Confidence 0.85 overall.

### F9. The eleven mechanisms of mantahostels' business-correspondence check, compared with impeccable


| # | Mechanism | impeccable | Evidence and gap |
|---|---|---|---|
| 1 | Rulebook as yes/no check questions with ranked grades | **Partly** | Generic fixed lists exist: cognitive load (8 items, scored by failure count), Nielsen (10 x 0-4 grade tables), craft floor (9 Verify, 15 Refuse), typeset (6) and layout (7) questions, P0-P3 ranks on every issue. They are impeccable's own, not the project's rulebook. The project's rules reach it only through PRODUCT.md / DESIGN.md (F6). |
| 2 | Mechanical lint | **Supplies** | `impeccable detect`, about 61 rules, two tiers, run per edit by the hook and once at finish (F5). It cannot see the house's geometry and motion rules; design-round's own scripts (`check-curves.js`, `check-flow.py`, `check-frames.py`) cover those. |
| 3 | Three blind reviewers in parallel, with an Unsure answer | **Not** | At most two isolated assessments of different kinds (critique, typeset, layout); one finish reviewer. "Unsure" exists only in the builder's lint triage. |
| 4 | Tally that passes only on unanimous Yes | **Partly** | No tally across reviewers. Inside one reviewer there is an all-rows rule: `ship` "only when the matrix holds no contradicted or missing row"; "Unresolved or partial material findings can never recompute to ship". The detector exits 0 only with no primary findings. |
| 5 | Fix, then a one-question re-check by a fresh reviewer | **Partly** | The verdict pass re-checks each fix, one line per fix, with a "resolved / partial / unresolved" answer. But it goes to the **same** reviewer by continuation; a fresh reviewer runs only without continuation, after a rebuild, or when the user's evidence contradicts a ship. |
| 6 | Stop signals | **Partly** | Has: two-round budget for an unattended run; "stop the moment a round resolves nothing"; a second rebuild directive goes to the user; three failed hero or responsive attempts go to a user review; Cursor lets a write through after repeated denial. Lacks: stop when a fix breaks another rule (it names up to 3 regressions and continues), stop when reviewers split (only one reviewer), stop on a named conflict. "Same rule fails again" is close to "a round resolves nothing" but is per round, not per rule. |
| 7 | Reviewers asked to name rule conflicts | **Not** | No reviewer prompt asks for conflicts. Conflicts are resolved by fixed precedence (F8). The one disclosure: a translated material must be named "in the presented direction". |
| 8 | Per-element rationale and "weakest parts" | **Largely** | Finish reviewer: per-element matrix, adaptations must cite "the user answer, surface brief, accessibility need, or product truth"; `material_fixes` ordered most material first (at most 8); `keep` line. critique: "What's Working" (2-3), "Priority Issues" (3-5) each with "Why it matters". Rationale is required for deviations and issues, not for every element. |
| 9 | Corrections log of the founder's rejections | **Not** | Adjacent only: `.impeccable/critique/ignore.md` (findings to drop silently); detector ignores with `--reason "<who decided: evidence>"`; the critique trend line (scores, not reasons). None records why the founder rejected a design. |
| 10 | Precedents file of approved finals | **Partly** | DESIGN.md and `.impeccable/design.json` are written by the documenter "from the shipped page"; approved comps carry `"approved": true`; critique snapshots persist. These record the system and approvals, not a set of approved finals that a reviewer compares against. The QUALITY BAR boards are catalog references, not the founder's finals. |
| 11 | Calibration against the founder's past verdicts | **Not** | No step reads past verdicts. Calibration is against the comp, the QUALITY BAR card and a model-bias prior. Inside one run, the user's own screenshot "outranks every capture" and forces a fresh full review. |

Confidence 0.8 (the comparison depends on my reading of each mechanism's name; I did not read the correspondence check itself).

### F10. Timeless principles and era-bound conventions

Sources: critique.md, audit.md, craft-floor.md, typeset.md, colorize.md, layout.md, animate.md, mode-persuade.md, new-work.md §4, and the detector rule table (F5).

**Timeless (perception, cognition, colour, typography tradition).** Confidence 0.85.
- Working memory: "Humans can hold ≤4 items in working memory at once (Miller's Law revised by Cowan, 2001)"; chunking, progressive disclosure (critique.md).
- Peak-end rule and emotional journey (critique.md).
- Hierarchy by contrast of size, weight, space and tone; "the squint test" (layout.md, typeset.md).
- Gestalt in practice, **never by name**. A search of all reference files for "gestalt" finds nothing. Proximity ("Use proximity before adding containers"), common region ("Grouping: ... proximity, borders, shared background") and similarity ("Same type of action = same type of UI") appear as advice. Closure, continuity and figure/ground do not appear. The house's design-critique §2 adds all six by name for this reason; that addition is still needed in 4.5.0.
- Colour perception: OKLCH "because lightness and chroma can be adjusted predictably"; "reduce chroma near white and black"; dark mode "not mechanically inverted"; colour never the only code; light text on dark needs "slightly more line height, a touch more tracking, and one step more weight" (colorize.md, typeset.md).
- Reading measure 45-75 ch (typeset) / 65-75 ch (craft floor), leading tuned to measure, "more space above a heading than below it" (typography tradition).
- Motion: easing that decelerates, "Exit faster than entrance", duration scaled to distance (animate.md).
- Nielsen's 10 heuristics (1994): old but still the standard heuristic set. Confidence 0.8.

**Era-bound web conventions, and how current they are.**
- *The AI-tell list* (craft floor Refuse list, about 29 detector "slop" rules, new-work §4 font ban list and "Calibration" looks): purple/cyan gradients, cream + serif + terracotta, near-black + neon, kicker/eyebrow labels, icon tiles, hero metrics, glass, Inter/Geist/Space Grotesk/Fraunces, em-dash cadence, "theater" copy, rules named for model families (`codex-grid-background`, `gpt-thin-border-wide-shadow`). This is the most current part: it names what LLM-generated UIs looked like in roughly 2024-2026, and 4.5.0's "rendition prior" paragraph is a measurement of the model's own bias. It is also the part that will date fastest, because it is a list of fashions to avoid, not principles. Confidence 0.8.
- *Web platform features*: OKLCH, `color-mix`, container queries, View Transitions, scroll-driven animation, `@starting-style`, `:has()`. These are current, mostly 2023-2025 platform additions. Confidence 0.75 (from my own knowledge of the platform; not checked against a source here).
- *Accessibility numbers*: WCAG AA 4.5:1 / 3:1 (WCAG 2.x, current); `prefers-reduced-motion` with "an intentional alternative" rather than a global 0.01 ms kill (current practice). **Partly dated**: touch targets "≥44x44" everywhere. From my own knowledge (not verified in this session, confidence 0.8), WCAG 2.2 (2023) added a 24x24 CSS px AA minimum and kept 44x44 at AAA; impeccable does not mention the 24 px AA level, and audit's grade scale says "WCAG AA fully met" without naming 2.1 or 2.2. No mention of APCA or WCAG 3.
- *Dated details*: the Casey persona asks "Does it work on slow connections (3G)?" (critique.md, unchanged in 4.5.0). Body text "below 12px" and the "16px" body floor are long-standing conventions, not perception facts. "Bounce and elastic easing feel dated and tacky" is a taste call of this era.
- *Detector font list drift*: the `overused-font` rule names Inter, Roboto, Fraunces, Geist, Plus Jakarta Sans and Space Grotesk; new-work §4's ban list is longer (adds Playfair Display, Cormorant, Lora, Crimson, Newsreader, Syne, Space Mono, IBM Plex, DM Sans/Serif, Outfit, Instrument Sans). The two lists do not match, so the detector does not enforce the whole §4 list. The literal list next to the rule in engine 0.1.11 is: roboto, open sans, montserrat, arial, helvetica, instrument sans, geist, geist sans, geist mono, mona sans, plus jakarta sans, space grotesk (Inter is probably matched elsewhere; its name is too short to find by string search). `syne`, `outfit` and `dm sans` do not occur in the binary at all. Thus Syne, Outfit, DM Sans/Serif, Cormorant, Lora, Crimson and IBM Plex in a build pass the detector; only the builder's own reading of §4 and the finish reviewer stop them. Confidence 0.75 (string evidence; I did not run the rule on a test file).

### F11. What changed from 4.2.1 to 4.5.0, for the checks only

Source: `diff -rq` of the two caches and word-level diffs of each changed checking file.

- **Unchanged**: `critique.md` (byte-identical), `craft-floor.md`, the detector's rule set (F5), `polish.md`.
- **audit**: adds the "Broken touch interaction" check and an evidence statement for gestures. `harden` and `adapt` add the same gesture checks ("Interrupted gestures").
- **new-work**: adds `component-review.md` (the user approves plates and the code/raster plan before page code, and later the first viewport); "three failed attempts" routes at the hero and responsive gates; self-hosted fonts for the hero capture; `mode-*.md` files carry per-mode rules; §7 makes the inspection ceiling unable to close an open gate and adds `build-phase finish --disposition`.
- **finish reviewer**: one line (check 1 fails any open or failed phase, not only the four named ones).
- **hooks**: a `SessionStart` hook; Gemini support.
- **New commands**: `generate` (variants of one element in the live browser). `live` refuses deployed production sites.
- Most of the 4.5.0 change is in the comp-led path. The house builds code-first, so most of it does not touch the house's rounds. Confidence 0.85.
- Installed state: mantahostels has impeccable 4.2.1 at project scope (`installed_plugins.json`, `projectPath: /home/lucmo/mantahostels`); every other project gets 4.5.0 at user scope.

### F12. How the house uses it: points to correct

Source: `plugin/skills/design-round/references/impeccable.md` and `plugin/skills/design-critique/SKILL.md` in this repo (both read in full).

1. design-critique §1 names audit's "accessibility, performance, responsive and theming scores". Audit has a fifth dimension, **Implementation Integrity**, marked "(CRITICAL)" with its own pass/fail verdict ("Start here"). The house text omits it. Confidence 0.9.
2. `references/impeccable.md` names 4.2.1 only. Projects other than mantahostels now run 4.5.0 (F11). Confidence 0.9.
3. design-critique §1 adds the Sam persona because "a marketing page is not routed to it". This is still true in 4.5.0 (the selection table is unchanged). Confidence 0.95.
4. design-critique §0 gives its critic "never an earlier round" and says "A critic never sees the same draft twice". impeccable's verdict pass sends the post-fix draft back to the **same** reviewer, which has seen the draft before the fix. If the house wants a fresh one-question re-check, it must say so; impeccable will not supply it. Confidence 0.8.
5. The house's precedence line "the project's rules file wins over PRODUCT.md and DESIGN.md" holds only if the rules reach those files: impeccable never reads the rules file (F6). Confidence 0.85.

## Bound

**Read in full.**
- This repo: `plugin/skills/design-round/references/impeccable.md`, `plugin/skills/design-critique/SKILL.md`.
- impeccable 4.2.1: `reference/critique.md`.
- impeccable 4.5.0: `SKILL.md`, `reference/audit.md`, `reference/new-work.md`, `agents/impeccable-finish-reviewer.md`, `reference/craft-floor.md`, `reference/hooks.md`, `hooks/hooks.json`, `reference/typeset.md`, `reference/colorize.md`, `reference/layout.md`, `reference/animate.md`, `reference/polish.md`, `reference/mode-persuade.md`, `reference/component-review.md` (lines cut at 500 characters), `scripts/impeccable` (launcher, first 150 lines, which is the whole decision logic).
- Diffs 4.2.1 → 4.5.0: full `diff -rq`; full line diffs of `SKILL.md`, `audit.md`, `hooks.md`, `hooks.json`, the finish reviewer, and §7 of `new-work.md`; word-level diffs of `new-work.md`, `harden.md`, `adapt.md`, `routing.md`, `visualize.md`, `live.md`, the documenter and asset-producer agents. `degraded/finish-reviewer.md` diffed against the agent file (same body).
- Caches: `~/.claude2` and `~/.claude3` copies diffed against `~/.claude` (identical).

**Sampled only.**
- `reference/init.md` (grep for PRODUCT.md, CLAUDE.md and writes).
- The engine binaries `~/.impeccable/bin/0.1.2/impeccable` and `0.1.11/impeccable`: `--help`, `detect --help`, one `context` run in a scratch directory, and string extraction of the rule table (about 40 KB around it). The engine is compiled; I did not read its source, so the rule count (61) and the tier split are from strings, not code.
- A grep of all 4.5.0 reference files for principle terms (Gestalt, OKLCH, WCAG, Miller, view transitions, and others).

**Not opened.**
- `reference/` files: `adapt.native.md`, `audit.native.md`, `android.md`, `ios.md`, `bolder.md`, `quieter.md`, `distill.md`, `delight.md`, `clarify.md`, `onboard.md`, `optimize.md`, `overdrive.md`, `harden.md` and `adapt.md` (diffs only), `document.md`, `extract.md`, `doctor.md`, `live.md` and `live-setup.md` (diff only), `visualize.md` (diff only), `generate.md`, `region-map.md`, `mode-operate.md`, `mode-read.md`, `operate.md`, `shape.md`, `routing.md` (diff only), `craft.md`.
- `agents/impeccable-documenter.md`, `impeccable-asset-producer.md`, `impeccable-manual-edit-applier.md` (diffs only for the first two).
- `scripts/live-browser*.js`, `modern-screenshot.umd.js`, `command-metadata.json`, the font index.
- impeccable 4.5.1 and 4.5.2 (not in any cache).
- The upstream repository `pbakaus/impeccable` and its README.
- mantahostels' business-correspondence check: I compared against the eleven mechanism names in the brief only.
- WCAG 2.2 and other outside standards: claims about them in F10 are from my own knowledge and are marked.
