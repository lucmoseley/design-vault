# design-vault document map

v1.0 · 28 September 2026

> The method this map is run by — authority classes, the rules for §A's register and §B's entries, the propagation pass and where a settled fact goes — is `.claude/workflow-core.doc-map.md`.

---

## Section A — document register

### Repo-root contracts

| Path | Role | Class | Update route | Consumes |
|---|---|---|---|---|
| `AGENTS.md` | AGENTS.md | `source-of-truth` | Direct | — |
| `CLAUDE.md` | CLAUDE.md | `source-of-truth` | Direct | — |
| `GLOSSARY.md` | Domain glossary — the vault's settled vocabulary, each term with its _Avoid_ list | `source-of-truth` | Direct, or through the `domain-modeling` skill when a term is contested | — |

### Governance & process docs

| Path | Role | Class | Update route | Consumes |
|---|---|---|---|---|
| `docs/clobber-reviewed.json` | the suspected issue-body overwrites workflow-core's check-clobbered-bodies.js accepts as deliberate rewrites, each keyed by `#N<TAB><edit time>` to why; the checker's header owns the shape (workflow-core#1700) | `source-of-truth` | Direct, one entry per reviewed SUSPECT; never delete one unread | — |
| `docs/code-standards.md` | This repo's local standards file beside the workflow-core plugin's shipped base (`docs/code-standards-base.md` under the plugin root, workflow-core#947): route rows for its root page scripts, its server and its derived data table, and its one risk path, the paid Higgsfield client. It changes no base rule (workflow-core#973). | `source-of-truth` | Direct | — |
| `docs/data/arch-scan-runs.jsonl` | Each architecture scan's scan and close line, one JSON line a run, which the scan-due counter reads for its window and threshold (workflow-core#1348) | `generated-only` | The architecture-scan skill's scan and close modes append; never hand-edited | — |
| `docs/data/outcome-signatures.jsonl` | Each fault-claiming ticket's fault signature, one JSON line a ticket, for the weekly outcome review (workflow-core#4796) | `generated-only` | <workflow-core>/scripts/file-issue.js --fault-signature or log-late-signature.js appends; never hand-edited | — |
| `docs/data/session-cost-table.json` | Per-session cost table the capped launch reads (workflow-core#371, #372): mean and 41 quantiles of what one of this repo's dispatched sessions spends. | `generated-only` | `node ~/workflow-core/scripts/measure-session-cost.js --write` run from this repo (not shipped in the plugin, workflow-core#1734); never hand-edited, never run at launch. | — |
| `docs/doc-map-admissions.json` | Doc map admissions — data file | `source-of-truth` | Direct | — |
| `docs/doc-map-classes.json` | Doc map classes — data file | `source-of-truth` | `node scripts/register-doc.js <path> --class <token> --section <name>` for a new key | — |
| `docs/doc-map-high-water.json` | Doc map high water — data file | `source-of-truth` | Direct | — |
| `docs/doc-map-restatements.json` | Doc map restatements — data file | `source-of-truth` | Direct | — |
| `docs/doc-map-retired-vocabulary.json` | Doc map retired vocabulary — data file | `source-of-truth` | Direct | — |
| `docs/doc-map-superseded.json` | Doc map superseded — data file | `source-of-truth` | Direct | — |
| `docs/doc-map.md` | Doc map | `source-of-truth` | Direct | — |
| `docs/test-read-edges.json` | Which test files read which tracked files; workflow-core keeps it fresh, and no selector here reads it (README §Validating the library) | `generated-only` | node <workflow-core>/scripts/generate-test-read-edges.js; never hand-edited | — |

### Skills & settings

| Path | Role | Class | Update route | Consumes |
|---|---|---|---|---|
| `.claude/guard-registry-anchors.json` | Guard registry anchors — data file | `generated-only` | `node scripts/check-guard-registry.js --review`, which re-anchors a guard whose annotation has been read | — |
| `.claude/implicit-behaviours.json` | Implicit behaviours — what each wired script of this repo's own does to a session unasked, why, and its escape | `source-of-truth` | Direct | — |
| `.claude/settings.json` | Settings — data file | `free-edit` | Direct | — |
| `.claude/workflow-core.json` | The adopter's config — contract, modules, commands, categories | `source-of-truth` | Direct | — |
| `.claude/workflow-core.md` | Workflow core | `generated-only` | workflow-core's `init` only, which rewrites it on every bump; override through `.claude/workflow-core.json` | — |
| `docs/pool-admission-ledger.json` | The admission ledger: one entry per top-level item in the always-loaded pool, keyed by file and headline, giving its removal claim and route — no-trigger, trigger with the ticket whose guard will print it, or pre-first-tool-call (#392). With `admissionGate` on, a commit adding a pool item with no entry is refused | `source-of-truth` | Direct, in the same commit that adds or rewords the pool item; a reworded headline moves its entry | — |

### Upstream taste-vault docs

| Path | Role | Class | Update route | Consumes |
|---|---|---|---|---|
| `docs/reference-to-design.md` | Reference to Design skill installation and usage, upstream cth9191/taste-vault's, kept verbatim | `source-of-truth` | Path-scoped cherry-pick from upstream only | — |

### Research notes

| Path | Role | Class | Update route | Consumes |
|---|---|---|---|---|
| `docs/coverage-ledger-method.md` | How docs/coverage-ledger.json is built and re-scanned: source families, blind extraction, merge grain, #210's covered test, the stop numbers and the script that computes them, the method-miss procedure and the refresh triggers (#215, #267) | `source-of-truth` | Direct, when #210's method changes | — |
| `docs/coverage-ledger.json` | The coverage ledger: every web design decision the outside sources name, its incidence per source, and whether the house covers it, by #210's covered test; three stop checks per area, a dated re-scan and the method misses. No ranking (#215, #267) | `source-of-truth` | Re-run #210's method at the re-scan date in its meta; a row's verdict changes when a ticket fills it, citing the ticket | — |
| `docs/data/baked-text-sweep-2026-10-16.csv` | The #327 threshold sweep: misses and flags at each pixel threshold and smallest blob tried, with and without the borderline labels, for docs/research/baked-text-trial.md | `free-edit` | Direct | — |
| `docs/data/baked-text-trial-2026-10-16.csv` | The #327 baked-text trial: each of 140 images' eye label, the PP-OCRv4 detector's blobs at #324's settings, and RapidOCR's detect and read cross-check, for docs/research/baked-text-trial.md | `free-edit` | Direct | — |
| `docs/data/contact-seams-2026-10-16.csv` | The #340 seam measurements: for 31 contacts on 5 grounds at DPR 1–3, the largest ground share, the equivalent ground width and width × contrast in arcsec, so docs/research/contact-seams.md's figures can be rechecked | `free-edit` | Direct | — |
| `docs/data/contact-seams-2026-10-16.py` | The #340 instrument: builds the contact fixtures, renders them through look-renders.py contacts as drawn and over black and white, and writes docs/data/contact-seams-2026-10-16.csv, for docs/research/contact-seams.md | `free-edit` | Direct | — |
| `docs/data/render-palette-kl2-2026-10-16.csv` | The #338 review rerun: the palette share for the 14 courtyard renders against the four-hex palette at CIEDE2000 lightness weight k_L 1 and 2, for docs/research/render-palette-plain-area.md's banner | `free-edit` | Direct | — |
| `docs/data/render-palette-kmeans-2026-10-16.csv` | The #338 quantised palette measurements: k-means (k 8 and 16) cluster area beyond ΔE00 2–20 of every palette colour, for docs/research/render-palette-plain-area.md | `free-edit` | Direct | — |
| `docs/data/render-palette-share-2026-10-16.csv` | The #338 palette measurements: for 39 real renders against each tested palette, the share of area beyond ΔE00 2–20 of the nearest palette colour and its percentiles, raw and blurred, so docs/research/render-palette-plain-area.md's figures can be rechecked | `free-edit` | Direct | — |
| `docs/data/render-plain-area-2026-10-16.csv` | The #338 plain-area measurements: local L* and chroma spread, RMS contrast, gradient, edge and band energy, and worst-pixel contrast over each headline box of the real renders, with the eye labels, for docs/research/render-palette-plain-area.md | `free-edit` | Direct | — |
| `docs/data/script-families-tier01-2026-10-15.csv` | The #295 coding: the 375 tier 0 and 1 ledger rows, coded blind by #248's rubric, with primitives, page conditions and the script ticket (#300–#318) answering each, so those tickets' row lists can be rechecked | `free-edit` | Direct | — |
| `docs/data/typeface-metrics-2026-10-16.py` | The #282 instrument: reads x-height, cap height, weight, lowercase advance and variable axes from font files, for docs/research/typeface-traits.md | `free-edit` | Direct | — |
| `docs/practice/browser-testing-and-accessibility.md` | The practice note for browser testing and accessibility checks: how leading practice checks rules that compare pages and the browser's Back button in a flow (#306) | `free-edit` | Direct; rewrite it when its Researched date passes six months | — |
| `docs/practice/design-critique-and-presentation.md` | The practice note for design critique and presenting work: breaking a verdict that names no part into the parts a client can point at (#406) | `free-edit` | Direct; rewrite it when its Researched date passes six months | — |
| `docs/practice/llm-evaluation.md` | The practice note for evaluating critics and benchmarks of model output: pooled keys, matching judges, paired arms and repeated runs, carried from workflow-core's note of the same date (#415) | `free-edit` | Direct; rewrite it when its Researched date passes six months | — |
| `docs/practice/node-and-python-cli-scripts.md` | The practice note for Node and Python command-line scripts: argument parsing, usage errors and exit codes, stdout and stderr, and checking a numeric option against a range known only once the data loads (#414) | `free-edit` | Direct; rewrite it when its Researched date passes six months | — |
| `docs/practice/test-design-and-reliability.md` | The practice note for test design and reliability: when a gate may run a failed test again, and that admission and re-runs answer different causes (#431) | `free-edit` | Direct; rewrite it when its Researched date passes six months | — |
| `docs/research/adopt-or-build.md` | Whether the house should adopt and enforce impeccable or other expert-built design guidance rather than write its own: 42 impeccable rules checked, sources surveyed, a precedence order and a verdict per area (#119) | `free-edit` | Direct | — |
| `docs/research/alignment-width.md` | The outside sources checked behind tier 1 ledger job alignment-width: line length by role and its unit, ragged and centred text, alignments a section, text columns, side indents, content width and centring, grid and optical alignment, table alignment and width (#285) | `free-edit` | Direct | — |
| `docs/research/baked-text-trial.md` | Whether PaddleOCR's PP-OCRv4 text detector finds text baked into real renders without false alarms: it fails, flagging 32 of 64 clean images at #324's settings and never fewer than 18 at a setting that passes #262's fixtures, so #329 and #335 close not planned and vault.baked-ui-look covers baked text (#327) | `free-edit` | Direct | — |
| `docs/research/brand-palette.md` | How a brand palette is built and checked against its grounds and its logo — colour interaction, a minimum ΔE00 between palette colours, which grounds a logo may sit on, how a client's logo colours meet a new palette — with mmm-infra measured (#143) | `free-edit` | Direct | — |
| `docs/research/carry-source-checks.md` | The outside sources checked behind tier 0 ledger jobs 1–4: text colour steps, figures and emphasis, dialog defaults, icons and face roles, radius scale, shadows and surface levels, hover, validation timing, scrolling and carousels (#275) | `free-edit` | Direct | — |
| `docs/research/contact-seams.md` | How large a gap or seam at a contact must be before it shows at device pixel ratios 1–3: width × luminance contrast of 0.5 arcsec (Hecht & Mintz 1939), measured from two-backing renders of look-renders.py contacts' crops, so #341 builds vault.contacts-seam at that line and overlaps stay with the critics (#340) | `free-edit` | Direct | — |
| `docs/research/control-feedback-defaults.md` | The outside sources checked behind tier 0 ledger jobs 25–30 and 32: menu and disclosure state, acting on release, phone safe areas, badge and progress names, live regions, toast focus, cookie banners, slow-refresh motion, homepage top tasks, list markers, and colour beside neighbours and imagery (#281) | `free-edit` | Direct | — |
| `docs/research/coverage-postmortem.md` | Why #104's coverage audit and #101's rulings missed the gaps the founder's 15 Oct notes found: each candidate cause tested against each gap, and the properties a replacement method needs (#203) | `free-edit` | Direct | — |
| `docs/research/critic-shape-test.md` | Which critic shape finds the most real faults without inventing more, on planted faults and clean pages: the whole-page critic plus a type critic (#224) | `free-edit` | Direct | — |
| `docs/research/de00-greys.md` | Where the near-miss line sits for two greys — design-system grey pairs by role, WCAG and APCA converted to ΔE00, lightness perception and near-duplicate tools — settled as ΔE00 10 for greys far from the ground and 3 for large surfaces near it (#178) | `free-edit` | Direct | — |
| `docs/research/de00-thresholds.md` | Whether published research sets the two palette lines — a near-miss below about ΔE00 10 and two meanings from about 15 — with each source's figure converted to ΔE00 and a verdict per line (#178) | `free-edit` | Direct | — |
| `docs/research/design-coverage-gaps.md` | What good website design today needs that the house's design rules and research do not cover, timeless against era-bound, gaps ranked (#104) | `free-edit` | Direct | — |
| `docs/research/design-feel.md` | The term for the feel a design aims at (tone), the scales evidence supports for it, which choices evidence ties to each scale with strength and era labels, and what the house holds (#204) | `free-edit` | Direct | — |
| `docs/research/design-rules-census.md` | Census of the 164 design rules a candidate answers to: where each lives, its form, its era, and whether a critic asks it (#98) | `free-edit` | Direct | — |
| `docs/research/edges-contrast.md` | Which edge each role takes, solid or alpha, and the contrast each role keeps in every theme: the 18 edges-contrast ledger rows' sources re-checked (#283) | `free-edit` | Direct | — |
| `docs/research/first-visit-trust.md` | What a first-time visitor to a solo advisor's or small-business site must see before getting in touch, when each item applies, how the items clash, and what a reader arriving from LinkedIn needs to feel a CV; mmm-infra the first case (#144) | `free-edit` | Direct | — |
| `docs/research/forms-overlays-colour-defaults.md` | The outside sources checked behind tier 0 ledger jobs 17–20 and 31: one question per form page, error-summary focus, dialogs, menus and hover content, colour pairs, color-scheme, captions, hr, and expression by frequency (#279) | `free-edit` | Direct | — |
| `docs/research/function-fit.md` | How each visual choice follows from an element's function: affordances, the aesthetic-usability effect, a function taxonomy, a per-element check for the critic, and where Manta's look and function pull apart (#127) | `free-edit` | Direct | — |
| `docs/research/function-questions.md` | #130 research: what function questions to ask a client and when to ask rather than infer; the ask-or-infer rule, a set-up batch and round triggers | `free-edit` | Direct | — |
| `docs/research/gate-trial-site-look.md` | What the gate check got right and wrong on mmm-infra's judged site-look pages, with planted faults (#169) | `free-edit` | Direct | — |
| `docs/research/house-audit-constants.md` | The check scripts' guessed constants against research — screen and viewport sizes, contrast cut-offs, typing pause, Higgsfield polling — each given a disposition (#183) | `free-edit` | Direct | — |
| `docs/research/house-audit-craft.md` | The craft gate's numbers against animation and perception research — trace tolerance, zoom checks, pause, jolt and speed-step lines, stillness, landings — each given a disposition (#183) | `free-edit` | Direct | — |
| `docs/research/house-audit-critic-panel.md` | The critic panel's numbers against research — three critics with unanimity, one-critic re-check, calibration every ten rounds, the 12-page trial's sample size, ten log examples, weakest parts, the client question cap — each given a disposition (#183) | `free-edit` | Direct | — |
| `docs/research/house-audit-method.md` | The house method's structure against research — dependency order, source precedence, the impeccable override reasons, House DNA bans and review dates — each given a disposition (#183) | `free-edit` | Direct | — |
| `docs/research/house-audit-visual.md` | The house references' visual figures against shipped design systems — text tint chroma, elevation levels, fill step, hover signals, scrim, radius nesting, form field budget — each given a disposition (#183) | `free-edit` | Direct | — |
| `docs/research/image-model-fact-bar.md` | Grok Image 2.0, Qwen Image 3 and Ideogram 4.0 on Higgsfield's API against the roster's fact bar: licence, watermark, deletion, ceiling, price (#44) | `free-edit` | Direct | — |
| `docs/research/image-model-profiles-a.md` | What rigorous sources find Grok Imagine 2.0, Qwen Image 3, Ideogram 4.0, Recraft V4.1, Z-Image Turbo and FLUX.2 best and worst at, per brand-art job (#51) | `free-edit` | Direct | — |
| `docs/research/impeccable-checks.md` | What impeccable's critique, audit, build reviewer and detector already check, against the business-correspondence check's mechanisms (#97) | `free-edit` | Direct | — |
| `docs/research/interaction-defaults.md` | The outside sources checked and the Chromium drag measurement behind tier 0 ledger jobs 9–12: drag alternatives and tracking, keyboard focus patterns, touch-action, redundant entry, sign-in, time limits, error pages, emphasis weight and line height by script (#277) | `free-edit` | Direct | — |
| `docs/research/jolt-onset.md` | Whether research gives the share of top speed at which a start from rest looks like a jolt: no direct source, a line derived from the eye's measured limits that falls as a move lengthens, and an absolute first-frame jump line (#221) | `free-edit` | Direct | — |
| `docs/research/layout-data-defaults.md` | The outside sources checked and the Chromium measurements behind tier 0 ledger jobs 13–16: table markup and print headers, chart contrast, visual order, safe centring, seams between fills, wheel input on scrollers (#278) | `free-edit` | Direct | — |
| `docs/research/manta-design-migration.md` | Which of Manta's brand and design-system research crossed into design-vault, what did not, and which portable items no planned research covers (#115) | `free-edit` | Direct | — |
| `docs/research/manta-element-coverage.md` | Every element of the Manta site against the house's rules and research by area, with 27 rule conflicts and the least-covered elements ranked (#118) | `free-edit` | Direct | — |
| `docs/research/markup-navigation-defaults.md` | The outside sources checked behind tier 0 ledger jobs 21–24: logo versions and home-link names, cards aligned by subgrid, native elements and landmarks, generated content, label in name, Back in a flow, multiple ways, the skip link, announced suggestions (#280) | `free-edit` | Direct | — |
| `docs/research/mmm-infra-logo-motion.md` | What mmm-infra's logo and animation work got wrong or redid, beyond #67–#73 and #75 (#88) | `free-edit` | Direct | — |
| `docs/research/mmm-infra-site-look-round.md` | What mmm-infra's site-look round (mmm-infra#8) got wrong or redid, beyond #77 and #78 (#91) | `free-edit` | Direct | — |
| `docs/research/notes-coverage.md` | The founder's 15 Oct 2026 design-topic notes N1-N19 checked one by one: where the house holds each, whether it is sourced, conditioned and reaches a critic, and whether the note's own claim holds (#205) | `free-edit` | Direct | — |
| `docs/research/past-design-rejections.md` | Whether the founder's past design rejections were breaches of a written rule or taste no rule held, with criteria drift (#102) | `free-edit` | Direct | — |
| `docs/research/platform-defaults.md` | The outside sources checked and the Chromium measurements behind tier 0 ledger jobs 5–8: font synthesis, kerning, fluid type and text spacing; paste, autofill, keyboards and implicit submission; quote, dash and number glyphs, lang and right-to-left text; icons, favicons, media alternatives and flashing (#276) | `free-edit` | Direct | — |
| `docs/research/plugin-dependency-route.md` | How the vault plugin ships and runs a third-party checker from its install folder: Claude Code's own npm install from a plugin lockfile, a vendored axe.min.js, npx rejected, and how the Python dependencies reach a user today (#244) | `free-edit` | Direct | — |
| `docs/research/principle-interactions.md` | #121 research: how the house's design principles depend on context and clash; a function → role → treatment → value order, every known conflict resolved or put to the founder, three Manta elements walked, and a rule form that carries its conditions | `free-edit` | Direct | — |
| `docs/research/render-palette-plain-area.md` | How far a painterly render may stray off its palette and how plain a headline area must be: each has a sourced measure (nearest-palette ΔE00; Scharff's masking index) but no defensible pass line, measured on 39 real renders, so #339 closes not planned and both rules go to critic look questions (#338, #344) | `free-edit` | Direct | — |
| `docs/research/rule-delivery.md` | How researched design rules reach the builder and the critics: what each loads today, rule-count and staging evidence, seven loading patterns with costs (#211) | `free-edit` | Direct | — |
| `docs/research/rule-interactions.md` | Which house rules with a value name their conditions, the type and contrast interactions research knows that the references miss, and the rule form they need (#206) | `free-edit` | Direct | — |
| `docs/research/surface-styling.md` | How borders, shadows, radius, dividers, fills, scrims, focus outlines and icon stroke are chosen, with conditions and conflicts, against what the house holds (#117) | `free-edit` | Direct | — |
| `docs/research/text-presentation.md` | How text is presented — colour and tint toward the brand, emphasis, links, numerals, text on every ground, rendering — with conditions and conflicts, against what the house holds (#123) | `free-edit` | Direct | — |
| `docs/research/tone-sources.md` | The outside sources checked behind the tone ledger job: saturation, colour share, white space, symmetry, typeface fit, the M3 Expressive study, mixed aesthetics and the four tone words, and where design-feel.md does not hold (#288) | `free-edit` | Direct | — |
| `docs/research/topic-taxonomies.md` | How design sources divide web design into topics, at what grain each names a decision, and a systematic-review method with stop checks for a complete topic list, tested on typography and surfaces (#207) | `free-edit` | Direct | — |
| `docs/research/typeface-traits.md` | How body size, minimum size, weight, line height and tracking follow a face's x-height, width, weight and optical size, and when a variable font pays: the 22 typeface-traits ledger rows' sources re-checked and 19 faces measured (#282) | `free-edit` | Direct | — |
| `docs/research/visual-critic-reliability.md` | How reliably a Claude critic judges a rendered design, and what structure makes it reliable (#99) | `free-edit` | Direct | — |

## Section B — load-bearing figure registry

None registered.

## Section C — question routes

None registered.
