# Census of the house design rules (design-vault#98, map #96)

Question: where do the house design rules live, how many are there, and what form are they in?

Each finding cites its source as `file:line`.

## Key to the columns

- **Scope.** `P` = portable (any project). `M` = Manta only. `I` = mmm-infra only.
- **Form.** `mech` = a script can check it. `y/n` = a reviewer can answer yes or no from a render or from the code. `hol` = holistic taste; two reviewers can disagree.
- **Src.** `R` = the rule cites research or a measured test. `T` = the rule cites a ticket or a founder ruling, but no research. `-` = no source.
- **Time.** `TL` = timeless (perception, physics, colour theory, Gestalt, type fundamentals, ethics). `EB` = era-bound (a web or tool convention of a period). `BR` = a brand choice for one project: neither a perception law nor a period convention. `proc` = a process rule, not a property of the candidate.
- **Src (Manta).** `S` = the rule gives a measured value (contrast ratio, L*, ΔE) or a standard's threshold (WCAG). This is measurement, not a study.
- **Asked.** Which critic prompt asks the rule today. `DC` = design-critique (the vault). `DR` = Manta's design-review. `IC` = impeccable critique or audit, or its craft floor. `brief` = the rule reaches the critic only as a line of the brief. `none` = no critic prompt asks it.

A "rule a candidate answers to" is a rule that a render, a build or its record can pass or fail. Pure workflow rules (where a branch lives, who posts a comment) are counted at the end of each section, but not listed one by one.

---

## 1. design-vault: `plugin/skills/design-critique/SKILL.md`

The critic's own file. 69 lines. It says it holds "no brand rules, only the craft gate (§1a)" (`design-critique/SKILL.md:8`).

### 1a. The craft gate (six rules)

Source of the gate: founder ruling, lucmoseley/mmm-infra#9, made permanent on lucmoseley/mmm-infra#16 (`:22`). One breach fails the candidate (`:22`).

| # | Rule | Where | Scope | Form | Src | Time | Asked |
|---|---|---|---|---|---|---|---|
| G1 | Curves are exact and smooth at any zoom; no polygon corners; edge within 0.5 px of the source | `design-critique/SKILL.md:24` | P | mech (`check-curves.js`) + y/n (overlay, 8x zoom) | T | TL (geometry) | DC |
| G2 | Every element lines up with what it touches; one shared curve or an offset of it; no gap or overlap at 4x | `:25` | P | y/n | T | TL (good continuation) | DC |
| G3 | Motion flows: no pause over 250 ms that the brief does not name; no move from rest at full speed; a fall is ballistic, y = ½gt², and lands on a damped spring | `:26` | P | mech (`check-flow.py`) + y/n (timeline table, 0.25x scrub) | T (physics stated, not cited; the 250 ms number has no source) | TL (physics, perception) | DC |
| G4 | Length is chosen: the motion brief gives a length range with a research source; the measured length is inside it | `:27` | P | mech (measure) + y/n (a source is present) | requires R in the brief | TL (rule form); the range itself is era-bound | DC |
| G5 | Drafts are never deleted: a tag for every earlier round; old drafts' frames unchanged | `:28` | P | mech (`git ls-remote`, `check-frames.py hash`) | T | proc | DC |
| G6 | The last frame is the asset's own end frame | `:29` | P | mech (`check-frames.py last`) | T | TL | DC |

### 1b. The added lenses (§2) and the change standard (§3)

Source of §2: "the gaps lucmoseley/mantahostels#926 measured in `impeccable critique`" (`:33`). This is a measured gap analysis of one tool. It is not research on the rules themselves.

| # | Rule | Where | Scope | Form | Src | Time | Asked |
|---|---|---|---|---|---|---|---|
| L1 | Gestalt, all six by name: proximity, similarity, closure, continuity, common region, figure/ground | `:35` | P | hol (each one answered, but the finding is judgement) | - (Gestalt not cited) | TL | DC |
| L2 | 5-second test: above the fold, what it is, who it is for, why care | `:38` | P (pages) | y/n | - | EB (web landing page) | DC |
| L3 | CTA count and the friction budget | `:39` | P (pages) | hol (no number given) | - | EB | DC |
| L4 | Risk-reversal microcopy | `:40` | P (pages) | y/n | - | EB (conversion practice) | DC |
| L5 | Objection handling | `:41` | P (pages) | hol | - | EB | DC |
| L6 | Credibility; who is behind the product | `:42` | P (pages) | y/n | - | TL (trust) | DC |
| L7 | Never invent proof: no invented testimonials, logos, counts, press, usage figures | `:44` | P | y/n | - | TL (ethics) | DC; also IC (craft floor "real content") |
| L8 | SEO: title, meta description, heading outline, internal links | `:46` | P (pages) | mech (all four are in the HTML) | - | EB (search engines of the period) | DC |
| L9 | The `h1`'s promise matches what the page contains | `:46` | P (pages) | y/n | - | EB/TL | DC |
| L10 | An edit needs a real deficiency, named in plain user terms | `:50` | P | y/n (can the critic finish the sentence) | - | TL | DC |
| L11 | A project rule is not a deficiency to design around | `:52` | P | y/n | - | proc | DC |
| L12 | Consistency with an existing surface beats a local improvement | `:53` | P | hol | - (close to Nielsen heuristic 4, not cited) | TL | DC; IC (Nielsen 4) |

### 1c. Process rules in this file, not listed

Fresh critic, never the same draft twice (`:12`); run impeccable `critique` and `audit`, always include the accessibility persona (`:16`); do not write a substitute critique when impeccable is off (`:18`); the report order and the review strip (`:57`-`:69`); keep every screenshot as a file (`:64`). Count: 6.

**Count for design-critique: 18 candidate rules** (6 craft gate + 12 lenses and standards), plus 6 process rules.

- Form: mech 6 (G1, G3, G4, G5, G6, L8); y/n 8 (G2, L2, L4, L6, L7, L9, L10, L11); hol 4 (L1, L3, L5, L12).
- Source: research cited 0. Ticket or ruling cited 6 (the craft gate). No source 12.
- Time: timeless 10 (G1, G2, G3, G4, G6, L1, L6, L7, L10, L12); era-bound 5 (L2, L3, L4, L5, L8); mixed 1 (L9); process 2 (G5, L11).

---

## 2. design-vault: `plugin/skills/design-round/SKILL.md` and `references/`

`design-round/SKILL.md` is 169 lines. Most of it is method (stages, rounds, branches).

### 2a. `design-round/SKILL.md`

| # | Rule | Where | Scope | Form | Src | Time | Asked |
|---|---|---|---|---|---|---|---|
| R1 | A motion or brand-art brief renders nothing while the project's palette, type or look is marked open | `design-round/SKILL.md:23` | P | y/n | T (mmm-infra#16) | proc | none |
| R2 | Client values: every direction, candidate and critic verdict answers each line | `:35` | P | y/n per line | - | proc | brief (the critic gets the brief, `:108`) |
| R3 | Guardrails: Manta takes its own prefill and never the House DNA; any other project takes the DNA, then its rules file, which overrides the DNA | `:37`-`:39` | P | proc | - | proc | brief |
| R4 | Inspect the actual screenshots; filenames and summaries do not count | `:60` | P | y/n (the record names the images opened) | - | proc | none |
| R5 | Avoid repeating the source's signature combination of subject, placement, silhouette and layout; a swapped flower keeps the signature | `:69`, `:74` | P | hol | - | TL | none by name (the repair delta `:91` is the founder's) |
| R6 | Do not drop every observed trait and return a generic page | `:74` | P | hol | - | TL | IC ("design specificity", impeccable `critique.md:47`) |
| R7 | A motion direction's beats add up to a total inside the motion brief's length range | `:72` | P | mech (sum) | - | TL | DC (G4, indirectly) |
| R8 | A candidate that fails either gate cannot be the leader | `:120` | P | mech (follows the gate) | - | proc | DC |
| R9 | Identity round: style tiles with palette, type pair, texture, interface parts and a motion sketch; the winner writes 3-4 motion principles with easing and duration tokens into the rules file | `:136` | P | y/n | - | proc | none |
| R10 | Web: layouts first, flat CSS stand-ins sized for the future image; art later | `:137` | P | y/n | - | proc | none |
| R11 | Web: component structure from the project's primitives first, then the roster libraries; rewrite the style layer every time | `:137` | P | y/n | - | EB | none |
| R12 | Web: render desktop, one intermediate width and mobile | `:137` | P | mech (three renders exist) | - | EB (device classes) | IC (`adapt`, Casey persona) |
| R13 | Check family resemblance and independence from the source | `:137` | P | hol | - | TL | none |
| R14 | Brand art: ask for the tool's largest size | `:138` | P | mech (pixel size) | - | EB | none |
| R15 | Every animal render checked for anatomy by eye before the critic | `:138` | P | y/n | R (benchmark, `roster.md:50`) | EB (model ability, 2026) | none (the building session only) |
| R16 | A cut-out is viewed on the dark and bright backdrops `cutout.py` writes | `:138` | P | mech + y/n | T (design-vault#54) | proc | none |
| R17 | A background is judged behind the real layout at desktop and phone widths | `:138` | P | y/n | - | TL | none |
| R18 | No output ships until its tool's ownership clause has been read | `:138` | P | y/n | - | EB (licence terms) | none |
| R19 | Whether an asset may move at all is the project's ruling | `:139` | P | proc | - | proc | none |
| R20 | The motion brief answers eight fields before any render: goal, moment, how often, trigger, length cited from research, skip, reduced-motion version, exact last frame | `:140` | P | y/n per field | requires R for length | TL (form); reduced-motion is EB | DC (G4 asks only length) |
| R21 | Round one of motion gives style frames and a storyboard strip, no playable build | `:141` | P | y/n | - | proc | none |
| R22 | The strip stills are real frames sought from the timeline | `:142` | P | y/n | - | proc | none |
| R23 | A timeline names its cues and writes its own timeline table | `:143` | P | mech | - | proc | DC (G3 reads the table) |
| R24 | Build to the craft gate: fitted curves, shared geometry, a computed fall (restates G1-G3) | `:144` | P | see G1-G3 | T | TL | DC |
| R25 | A morph: both ends share one command structure; holes kept as subpaths; arcs as C; a script interpolates numbers; never resample to points | `:145` | P | mech (`check-flow.py` writes `morph.svg`, `check-curves.js` reads it) | T (mmm-infra#28) | TL (geometry) + EB (Safari cannot animate `d` in CSS) | DC (G1 via `morph.svg`) |
| R26 | A generated clip: start frame equals end frame; prompt describes motion only | `:146` | P | mech (frame diff) + y/n | - | EB (2026 video models) | none |
| R27 | UI motion goes through impeccable's `animate`, within the project's tokens | `:147` | P | proc | - | EB | IC |
| R28 | Print: any rights holder the project names signs off before print | `:148` | P | y/n | - | proc | none |
| R29 | Copy, controls and data stay live UI, never baked into an image | `:150` | P | y/n | - | TL (access, edit) | none (prompts forbid text in art) |
| R30 | Label artwork a viewer could mistake for product evidence | `:150` | P | y/n | - | TL (honesty) | none |
| R31 | Never invent logos, testimonials, counts or press | `:150` | P | y/n | - | TL | DC (L7) |
| R32 | Brand motion: a UI curve that starts at full speed is wrong for a build, fall, landing or settle | `:154` | P | mech | T (mmm-infra#26 F3) | TL (physics) | DC (G3) |
| R33 | A fall is `t²` = `cubic-bezier(1/3, 0, 2/3, 1/3)`, lasting √(2·drop/g), g = 9.80665 m/s² × px per metre; it hands its speed to a landing | `:156` | P | mech (`fall.js`) | physics (not cited, derivable) | TL | DC (G3) |
| R34 | A landing is a critically or highly damped spring from the impact speed | `:157` | P | mech (`fall.js`) | T | TL | DC (G3) |
| R35 | A heavy settle is a critically damped spring sampled to `linear()` at 41 stops | `:158` | P | mech | T (mmm-infra#26) | TL (spring) + EB (`linear()` CSS) | none by name |
| R36 | "Never ease-in" and the UI duration caps stay with UI motion; a brand piece's length comes from its brief | `:161` | P | proc (a precedence rule) | - | proc | none |

Process rules in this file not listed: stage detection §0 (6), branch, tag and worktree rules (`:98`-`:100`), round record format (`:104`), fresh critic (`:108`), craft gate runs twice and reports numbers (`:110`), keep the critic's evidence (`:112`), the review strip (`:114`-`:118`), tweak rungs (`:126`-`:128`), extract and document after a web win (`:132`), five-then-three (`:85`), repair shapes (`:89`-`:94`), references from the library (`:45`-`:56`). Count: about 20.

**Count for design-round/SKILL.md: 36 candidate rules.** Form: mech 12, y/n 17, hol 3, proc-only 4. Source: research 1 (R15, through the roster benchmark); ticket or ruling 7; none 28. Time: timeless 12, era-bound 7, mixed 3, process 14. Asked by a critic: 12 (DC 9: R7, R8, R23, R24, R25, R31-R34; IC 3: R6, R12, R27). Reach the critic only as the brief: 2 (R2, R3). Asked by no critic: 22.

### 2b. `design-round/references/`

Most of `references/` is tool use, not candidate rules.

| # | Rule | Where | Scope | Form | Src | Time | Asked |
|---|---|---|---|---|---|---|---|
| F1 | Never carry one project's colours into another project's prompt | `references/prompts.md:3` | P | y/n | - | proc | none |
| F2 | Artwork carries no website text, navigation, buttons, logos, dashboard or fabricated product data | `prompts.md:19`-`:21` | P | y/n | - | TL | none |
| F3 | Do not reproduce the source subjects or their arrangement (restates R5) | `prompts.md:19` | P | hol | - | TL | none |
| F4 | Mobile crop keeps the focal element | `prompts.md:17` | P | y/n | - | EB | none |
| F5 | Video from a still: same start and end frame; prompt describes motion only (restates R26) | `prompts.md:108` | P | y/n | - | EB | none |
| F6 | Repair "too close": a similar object in a different colour is not enough | `prompts.md:126`-`:127` | P | hol | - | TL | none |
| F7 | Repair "too generic": restore three concrete principles (image scale, type hierarchy, density, material) | `prompts.md:135`-`:137` | P | hol | - | TL | none |
| F8 | Design record carries viewport sizes, visual findings, interactions checked, remaining limits | `prompts.md:223`-`:224` | P | y/n | - | proc | none |
| F9 | Final: `polish` always; `adapt` always for the intermediate width and phone; `harden` where there is a form or live data; `optimize` where audit scores performance below 3 of 4 | `references/impeccable.md:25`-`:28` | P (web) | mech (audit score) + y/n | - | EB | IC |
| F10 | Precedence: the project's rules file wins over PRODUCT.md and DESIGN.md | `impeccable.md:8` | P | proc | - | proc | none |
| F11 | Comp-led route (`visualize`, `generate-image`) stays off | `impeccable.md:56` | P | y/n | - | proc | none |
| F12 | Original preset restores the baseline exactly | `references/polish.md:7` | P | y/n | - | proc | none |
| F13 | Static hierarchy, spacing and legibility carry the page with motion off | `polish.md:11` | P | y/n | - | TL | none |
| F14 | Tie expressive details to the brand or product narrative | `polish.md:13` | P | hol | - | TL | IC (design specificity) |
| F15 | No blocking preloader; continuous motion needs a reason; readable and operable with motion off, reduced motion, or no scripts | `polish.md:37` | P | y/n | - | EB (`prefers-reduced-motion`) | IC (Sam persona, partly) |
| F16 | Replay does not stack effects; pause off-screen work; respect reduced-motion changes live; off switch covers hover and scroll | `polish.md:41` | P | y/n | - | EB | none |
| F17 | Inspect desktop, intermediate and mobile; compare at the same width | `polish.md:45`-`:47` | P | y/n | - | EB | none |
| F18 | Every control in the tweak panel visibly changes its property; keyboard usable | `prompts.md:176`-`:180`, `polish.md:29`, `:45` | P | y/n | - | EB | none |

Tool and prompt rules in `references/` not listed as candidate rules: the per-tool dialects (`prompts.md:28`-`:114`, about 25 lines of rules: largest size, hex plus words, positive phrasing, transparency by plain colour, `enhance_prompt=false`, `quality=medium`, JSON caption for Ideogram and so on); the fact bar and dispositions (`roster.md:5`-`:22`, 9 rules); the model-selection rule (`roster.md:44`-`:61`, 6 rows plus 4 notes); the cut-out, video, component and tweak rows (`roster.md:63`-`:117`, 33 rows); the comparison method (`comparison.md`, about 8 rules). Count: about 85.

Two items in `roster.md` cite research or a measured test: the animal benchmark (42.6 of 100) and the ΔE 10 palette test (`roster.md:50`-`:51`, design-vault#51).

**Count for `references/`: 18 candidate rules** (2 restate rules from SKILL.md: F3 = R5, F5 = R26). Form: mech 1, y/n 12, hol 4, proc 1. Source: none cited for any of the 18. Time: timeless 6, era-bound 7, process 5. Asked by a critic: 3 (F9, F14, F15, all IC). Asked by none: 15.

---

## 3. design-vault: the House DNA (`data/gallery.json:8`-`:26`)

`constants` is empty (`data/gallery.json:11`). `never` has 12 lines (`:13`-`:24`). The DNA calls itself "defaults, not absolute rules: the project's own brief lines win", and says it "grows one line at a time from a real round; nothing here is inferred from saved references" (`:10`).

**Provenance finding.** `git log -S` shows that line 14 ("Glossy 3D SaaS blobs") came in the seed commit `910ab1d` (2026-07-20, "taste vault v1", from `cth9191/taste-vault`). The last four lines (`:21`-`:24`) and the description at `:10` came in `84bace6` (2026-09-29, "Bring Manta's 46 references into the vault"). No line has a round or a founder ruling as its source. The claim at `:10` ("grows one line at a time from a real round") does not describe how the twelve lines came in.

| # | Never line | Where | Scope | Form | Src | Time | Asked |
|---|---|---|---|---|---|---|---|
| D1 | Purple-to-blue or mesh gradient grounds; gradient text; glow or neon borders; glassmorphism cards | `gallery.json:13` | P (not Manta) | mech (CSS) + y/n | - | EB (2020s "AI SaaS" look) | brief; IC (craft floor bans gradient text and decorative glass, `craft-floor.md:33`-`:34`) |
| D2 | Glossy 3D SaaS blobs and floating blob shapes | `:14` | P | y/n | - | EB | brief |
| D3 | A centred hero with two pill buttons | `:15` | P | y/n | - | EB | brief |
| D4 | A three-column icon-in-circle feature grid, or any icon-grid feature row | `:16` | P | y/n | - | EB | brief; IC (`craft-floor.md:25`) |
| D5 | Uniform card heights with a decorative icon each | `:17` | P | y/n | - | EB | brief; IC (`craft-floor.md:25`) |
| D6 | A stock photo of a smiling group; placeholder avatars | `:18` | P | y/n | - | EB | brief |
| D7 | Emoji bullets; lorem ipsum; banned copy tells ("Unlock", "Elevate", "Seamless") | `:19` | P | mech (text search) | - | EB | brief; IC (emoji as icons, `craft-floor.md:40`) |
| D8 | Fabricated proof: invented testimonials, logos, counts or press | `:20` | P | y/n | - | TL (ethics) | brief; DC (L7) |
| D9 | A stock photo used as found, not chosen or treated for this page | `:21` | P | hol | - | TL | brief |
| D10 | One rounding applied to everything by habit, as the friendliness signal | `:22` | P | hol ("by habit" is intent) | - | EB | brief |
| D11 | The default font stack (Inter, the system sans) as the only voice, with no chosen display face | `:23` | P | mech (computed `font-family`) | - | EB | brief; IC (`craft-floor.md:39`) |
| D12 | Several colours at equal weight, none dominant | `:24` | P | hol (could be measured by pixel share) | - | TL (colour dominance) | brief |

**Count for the House DNA: 12 rules, all portable except to Manta.** Form: mech 3, y/n 6, hol 3. Source: 0 cite research, 0 cite a round. Time: timeless 3 (D8, D9, D12), era-bound 9. Asked: no critic prompt names the DNA. `design-critique` says it "carries no hard bans; a project's own gate does" (`design-critique/SKILL.md:3`). The DNA reaches the critic only as the brief's Guardrails block (`design-round/SKILL.md:39`, `:108`). Five lines (D1, D4, D5, D7, D11) overlap impeccable's craft-floor "Refuse" list, so impeccable asks them on its own terms.

### design-vault subtotal

| Source | Candidate rules | mech | y/n | hol | proc | research cited | timeless | era-bound | asked by DC/IC |
|---|---|---|---|---|---|---|---|---|---|
| design-critique | 18 | 6 | 8 | 4 | 0 | 0 | 10 (+1 mixed) | 5 | 18 |
| design-round SKILL.md | 36 | 12 | 17 | 3 | 4 | 1 | 12 (+3 mixed) | 7 | 12 |
| design-round references/ | 18 | 1 | 12 | 4 | 1 | 0 | 6 | 7 | 3 |
| House DNA | 12 | 3 | 6 | 3 | 0 | 0 | 3 | 9 | 6 (5 IC, 1 DC) |
| **Total** | **84** | **22** | **43** | **14** | **5** | **1** | **31 (+4 mixed)** | **28** | **39** |

The remaining 21 rules are process rules in the time column (they are not a property of the picture).

(Some rules count as mech in the form column but also need a y/n step. The table gives the leading form.)


---

## 4. Manta (`~/mantahostels`)

### 4a. Where the rules live, and which file wins

- `docs/brand/brand-sheet.md` (462 lines, header v2.37, `brand-sheet.md:1`) is the source of truth. `DESIGN.md:110` and `PRODUCT.md:52` both say so, and `design-vault`'s `projects.manta.rules` points at it (`data/gallery.json`, `projects.manta`).
- `DESIGN.md` (241 lines) calls itself "a derived, machine-readable restatement" (`DESIGN.md:110`). impeccable reads it on every run (`references/impeccable.md:8`).
- `PRODUCT.md` (84 lines) is impeccable's product file. It restates the hard constraints and the accessibility floor.
- `docs/brand/design-process.md` (117 lines, v2.5) holds the Guardrails prefill that goes verbatim into every Manta brief (`design-process.md:15`-`:45`). It says "Never the vault's House DNA" (`:13`).
- `.claude/skills/design-review/SKILL.md` (79 lines) is Manta's gate: 7 pass/fail checks (`design-review/SKILL.md:33`-`:48`) and one pre-launch check (`:50`-`:52`). Then it hands everything else to `design-vault:design-critique` with `DESIGN.md` and the brand sheet as context (`:59`-`:60`).
- The brand sheet also restates itself: §13 is a paste block of §§1-12a (`brand-sheet.md:325`-`:438`), and it says a change to a section "is carried to that prefill in the same edit" (`:327`).

### 4b. The brand sheet's design rules, with every other home

Key for "Asked": `DR gN` = design-review gate check N. `ctx` = the critic gets the file as context (`design-review/SKILL.md:59`), but no prompt asks the rule by name; design-critique even tells the critic that "a project rule is not a deficiency to design around" (`design-critique/SKILL.md:52`), which is not a check for conformance. `IC ...` = impeccable asks a general version of it (`craft-floor.md:9`-`:17`, `:33`-`:40`). 

Copy-only rules (§11 voice, the 14 banned tells, the guide review pass, the source-line grammar, `brand-sheet.md:222`-`:291`) are not listed. They are copy, and `docs/copy/` and `scripts/check-website-copy.js` own them. B49-B51 are kept because they change what a render shows.

| # | Rule | brand-sheet.md line | Form | Src | Time | Asked | Also stated in | Portable in principle |
|---|---|---|---|---|---|---|---|---|
| B1 | Energy is localised: hero/marketing zone loud (volume 6-7), working area calm (4-5); every surface in one zone | 13, 17-20 | hol | - | BR | ctx | DESIGN:116-119; PRODUCT:55; s13:333 | no |
| B2 | Night (ink) ground only in named bounded contexts; day is default | 22 | y/n | T | BR | ctx | DESIGN:121; DP:22-25; s13:334,367 | no |
| B3 | Interior announcement: Manta's own state, after the page's content, at most one per page | 24 | y/n | T (#3222) | BR | ctx | DESIGN:123; DP:23-25; s13:335 | no |
| B4 | Text on turquoise is ink, never white (only the wordmark's 'Hostels' is exempt) | 26, 146 | mech | S (2.3:1 measured) | TL | DR g5; IC contrast | DESIGN:149,218; DP:26,33; s13:344 | yes (as 'measure contrast') |
| B5 | Turquoise grounds carry type and badges only; mark, rating unit or creature sit on a bounded ink form | 28, 165, 183 | mech | S (L*, 1.20:1, 1.59:1) | TL (figure/ground) | DR g4; build error (s14:446) | DESIGN:197,217; DP:33; s13:413-415 | no |
| B6 | Night pattern: on ink, text white, semantic by border/icon/chip, muted-night secondary, links white + underline | 30, 73-99 | y/n | S (ratios) | TL | ctx | DESIGN:151,220; s13:367-383 | partly |
| B7 | Nav is ink on every page type; 72 px desktop, 56 px mobile | 32 | mech | S (1.00:1) + T | BR | ctx | DESIGN:171-173; s12:305; s13:411 | no |
| B8 | Current nav link: aria-current, semibold, no underline | 34 | mech | T (#3459) | EB | ctx | DESIGN:175 | no |
| B9 | Do not collapse day and night to one hero ground; lagoon and sunset-coral hero grounds rejected | 36 | y/n | - | BR | ctx | - | no |
| B10 | Every colour has one meaning; colour with no information does not appear in the working area | 40 | y/n | - | TL (signal over noise) | ctx | DESIGN:127,229 | yes |
| B11 | lagoon is for fills and strokes, never text | 45 | mech | S (3.6:1) | TL | IC contrast | DESIGN:132; s13:340 | via B21 |
| B12 | coral is CTAs only, one per view; never a ground, decoration or the wordmark | 52, 63 | y/n | - (reasoned) | BR + TL (one focal action) | DR g1 | DESIGN:138,205,215; DP:22,32; s12:301; s13:346 | partly ('one primary action per view') |
| B13 | amber is rewards only; never price urgency | 53 | y/n | T (#978) | BR | ctx | DESIGN:139; DP:21; s13:357 | no |
| B14 | peach is illustration and hero art only | 54 | y/n | S (dE) | BR | ctx | DESIGN:140; DP:21; s13:359 | no |
| B15 | success and warning are fill-only; text uses the named -text partner | 55-58 | mech | S (ratios) | TL | IC contrast | DESIGN:142; s13:362-364 | via B21 |
| B16 | Warm = act, cool = read | 63 | hol | - | TL? (colour temperature; not sourced) | ctx | DESIGN:127 | maybe |
| B17 | Tinted card grounds only for special rows, never list items | 63 | y/n | - | BR | ctx | DESIGN:207 | no |
| B18 | Gradients only in the logo mark; UI is flat | 63 | mech | - | EB (flat UI) | ctx; IC (gradient text only) | DESIGN:224; DP:36 | no |
| B19 | Error and sold-out never by colour alone; always a label or icon | 63 | y/n | S (CVD reasoning; WCAG 1.4.1 not named) | TL | ctx; IC (a11y persona) | DESIGN:223; PRODUCT:83; DP:35; s13:366 | yes |
| B20 | Semantics are tinted chips with text partners; never copy in a raw fill colour; lagoon wash for hover/selected only, never a card ground | 65 | mech | S (ratios), T (#3449) | TL | ctx | DESIGN:147,219; DP:34; s13:362-366 | partly |
| B21 | Text-safe partner rule: a colour is not cleared for type until measured; under 4.5:1 it gets a named darker partner, never a size workaround (coral excepted) | 67 | mech | S (WCAG AA) | TL | IC contrast | DESIGN:145; PRODUCT:79; s13:384-386 | yes |
| B22 | Do not invent light text partners for the night ground | 75 | y/n | S (13.12:1; dE 12.4) | TL | ctx | DESIGN:151,220; s13:369-372 | partly |
| B23 | Links on ink: white plus underline, never turquoise; the nav wordmark lockup exempt | 99 | mech | T (#3459) | BR | ctx | s13:378 | no |
| B24 | Fixed text-on-colour pairings; score chips take ink | 104 | mech | S (ratios) | TL | ctx; IC contrast | DESIGN:159; s13:345 | no |
| B25 | Row CTAs never coral and never say 'Book'; one coral object per view = sticky compare bar or hero search; Sign in is outline | 106 | y/n | - (honesty reasoning) | BR + TL (honest label) | DR g3 | DESIGN:205; DP:36; s13:350-352 | no |
| B26 | Artwork leeway, one limit: no near-miss of an adjacent token; colours decisively identical or decisively different (dE00 ~7 reads as an error) | 108 | mech (dE00) | S (measured dE) | TL (colour discrimination) | none | - | yes |
| B27 | CTA hue: no complement of the hero ground (edge shimmer at 176 deg); chroma is affordance | 123 | y/n | - (reasoned) | TL (colour theory) | none | - | yes |
| B28 | Quicksand 700/600 display; Nunito Sans 400/600-700 body; body 14-15.5 px, line-height ~1.6 | 129-132 | mech | - | BR + TL (line-height) | ctx | DESIGN:163; DP:25-26; s13:337 | no |
| B29 | Primary coral CTA label Nunito Sans 700 at >=19 px; other controls 13-16 px | 134 | mech | S (WCAG large text 18.66 px/700) | TL | DR g5 | DESIGN:165; s13:348 | partly |
| B30 | Sentence case for body and buttons; uppercase only for badges and filter labels; no emoji in product copy | 136 | mech | - | EB | ctx; IC (emoji icons) | DESIGN:167,225; PRODUCT:57; DP:26; s11:246-247; s13:404 | no |
| B31 | Wordmark: Quicksand 700, one word, ink + turquoise (white + turquoise on dark); never coral, mixed fonts, wide-hue splits | 142-146 | y/n | - (context test, unsourced) | BR | ctx | PRODUCT:56; s13:338 | no |
| B32 | Keyline lagoon-text on every ground; do not 'fix' the soft halo on ink | 169 | y/n | S (ratios) | BR | ctx | s13:408 | no |
| B33 | Three mark variants only: primary, nav (features ~2.85x, redrawn), flat (currentColor) | 171-175 | y/n | S (px arithmetic) | BR | ctx | s13:409-410 | no |
| B34 | Nav is a recognition surface; do not grow the nav to carry the face | 177 | y/n | S (px arithmetic) | BR | ctx | - | no |
| B35 | Rating unit: five mantas 13-17 px, lagoon solid/outline, half = clip, always with the number, never on turquoise | 183 | mech | S (1.2:1, 1.59:1) | BR | DR g4 (ground only) | DESIGN:197; s13:393-394 | no |
| B36 | A score never without its review count and fixed word (Loved/Great/Solid/Mixed); no count thresholds; sub-scores not in the results row; zero = 'No reviews yet' | 185 | mech | T (#376, #373, #3011) | TL (honesty) | DR g7 | DESIGN:199; PRODUCT:48; DP:30-31; s13:395-399 | partly |
| B37 | Verified-stay badge: visual only, lagoon edge at low alpha; 'Reviewer earns rewards' disclosure distinct, >=12.5 px | 187 | y/n | T (FTC via review-ux) | EB (FTC rules) | ctx | - | no |
| B38 | Card anatomy: photo-led, photo left ~35%, name top-left with no pill, rating line under name, price top-right, facts line, flavour line, action zone | 189 | y/n | T | BR | ctx | DESIGN:177; s13:387-391 | no |
| B39 | Score met early in the scan: left-aligned at a fixed position (a column row to row), ahead of price; price inside the card | 189-191 | y/n | - (reasoned) | TL (alignment, scan order) | ctx | DESIGN:179; s13:391 | yes |
| B40 | Prices tax-inclusive, declared once at list level; no strikethrough or discount theatre | 189, 226 | y/n | T | TL (honesty) | DR g6 (strikethrough) | DESIGN:209; PRODUCT:46; s13:391-392 | no |
| B41 | Illustration: organic curves, brand palette, crisp horizon, visible wave bands; flat colour and <=5 colours OPEN | 195 | hol | T (design-vault#2) | BR | ctx | DP:29-31; s13:416-420; gallery.json projects.manta.groups headers | no |
| B42 | Hero wave: ink band (never lagoon); locked geometry; path >= 800 units wide; zero mark pixels outside ink at 320-1920 px | 197-202 | mech | S (ratios) + T (#3021, #3401) | BR | ctx | s13:418-420 | no |
| B43 | Illustration-led on brand surfaces; photography on listings only | 208 | y/n | logged hypothesis, unvalidated | BR | ctx | PRODUCT:58; DP:56; s12:303 | no |
| B44 | Icons outline, rounded, ~1.75 px at 20 px, ink or lagoon; no emoji or unicode-glyph icons | 212 | mech | - | EB | ctx; IC (emoji icons) | DESIGN:189; DP:28,36; s13:405 | partly |
| B45 | Radii 8 / 10-12 / 6 / 999 px | 214 | mech | - | BR | ctx | DESIGN:187; DP:27; s13:400 | no |
| B46 | Borders first; shadow only on hover and popovers; nothing at rest under a heavy shadow | 216 | mech | - | EB | ctx | DESIGN:183; DP:27; s13:401 | no |
| B47 | Focus rings lagoon (ink on turquoise); never removed without a replacement; error borders danger | 218 | mech | S (3:1 component floor) | TL | ctx; IC (keyboard focus) | DESIGN:193; PRODUCT:84; s13:401-402 | yes |
| B48 | UI motion 120/180 ms, cubic-bezier(0.2,0,0,1); press 0.97; no bounce or spring; motion never announces itself | 220 | mech + hol | - | EB | ctx | DESIGN:191; DP:28,37,68; s13:402-403 | no |
| B49 | No urgency theatre: countdowns, flash prices, strikethroughs, scarcity; covers pricing presentation | 224, 226 | y/n | - (trust reasoning) | TL (dark patterns) | DR g6 | DESIGN:222; PRODUCT:47; DP:35; s13:423 | yes |
| B50 | Loud claim, calm mechanics: a loud line has plain specific terms directly beneath | 232 | hol | - | TL | ctx | DESIGN:230; s13:429-430 | yes |
| B51 | No superlative, ranking or 'best' string on any listing (incl. 'Top rated', 'paling', 'ter-') | 273 | mech | T (#978; EPI 1.2.2) | EB (legal) | ctx | DESIGN:139,177; s13:357 | no |
| B52 | Differentiation firewalls: never orange grounds; logo an animal, never a letterform; never brush-script; never 'meet people' framing | 300-306 | y/n | T (verified Jul 2026) | EB (competitor of the day) | DR g2 (orange only) | DESIGN:216; PRODUCT:25; DP:32,37; s13:431-437 | no |
| B53 | Booking handover, never checkout: one handover module; coral 'Book direct with the hostel'; OTA exits ink-outline, plain-text name, no OTA price; honesty line always visible; one value field; one interstitial; 'Saved to your trips' only; rooms as rows | 315-323 | y/n | T (#3011) + legal | BR (business + legal) | ctx; DR pre-launch check (partly) | DESIGN:201; PRODUCT:33,42-44; DP:35-36; s13:353-356 | no |


**Count for the brand sheet: 53 design rules**, all Manta-only as written.

- Form: mech 24, y/n 25, hol 4.
- Source: measured value or standard cited 20; ticket or ruling 13; logged hypothesis 1 (B43); none 19. No rule cites a peer-reviewed study.
- Time: timeless 21, brand choice 20, brand choice with a timeless reason 3, era-bound 9.
- Asked: design-review's gate asks 10 (B4, B5, B12, B25, B29, B35, B36, B40, B49, B52, the last only for orange). A build check also enforces B5 ("the turquoise-ground prohibition as a build error", `brand-sheet.md:446`; `app/_lib/ground-context.tsx:5` has a `turquoise` ground type, not opened in full). 41 reach the critic only as context. 2 (B26, B27) are not stated anywhere a critic reads except the sheet itself.
- Portable in principle: 10 rules would hold for any project (B4 as "measure contrast", B10, B19, B21, B26, B27, B39, B47, B49, B50). No portable file holds them today, except that impeccable asks contrast and focus in general terms.
- Homes: 5 rules have one home; 8 have two; 11 have three; 18 have four; 6 have five; 5 have six. (A home is a file or a self-restating section: §12, §13, DESIGN.md, PRODUCT.md, the Guardrails prefill, the design-review gate.)

Process rules in the sheet not listed: withdrawn tokens and rejected recolours, faces and approaches "do not re-propose" (`:36`, `:102`, `:121`, `:123`, `:138`, `:179`); the canonical mark files (`:150`-`:152`); the §13 sync rule (`:327`); the queued-edits ledger (`:456`). Count: about 10.

### 4c. Rules found outside the brand sheet


| # | Rule | Where | Form | Src | Time | Asked |
|---|---|---|---|---|---|---|
| X1 | Hostel testimonial is its own component: a pull-quote on sand, one lagoon left rule, italic, no rating, score, badge, name or avatar; attribution always shown; never interleaved with reviews | `DESIGN.md:203`, `:221` | y/n | T (#997) | TL (honesty) | ctx |
| X2 | Keep the working area calm: one focal action | `DESIGN.md:229` | hol | - | TL | ctx |
| X3 | Design the failure states: greyed out, not hidden; "availability not shown" rather than a guess | `DESIGN.md:231`; `PRODUCT.md:72` | y/n | - | TL | ctx |
| X4 | Never display, publish, cache or copy OTA prices, availability, scores, counts, text or photos | `PRODUCT.md:42`-`:44`; prefill `design-process.md:36` | y/n | legal (contract clauses) | EB (current contracts) | ctx; DR pre-launch check covers invented figures only |
| X5 | Pre-launch: no invented testimonials, partner logos, review counts, press or usage figures | `PRODUCT.md:67`; `design-review/SKILL.md:50`-`:52`; prefill `:37`-`:38` | y/n | - | TL | DR; DC (L7) |
| X6 | WCAG AA for text is the working floor | `PRODUCT.md:79` | mech | S | TL | IC contrast |
| X7 | Hero video page budget: poster is the LCP resource; video `preload="none"` after load; 250 kB target, 640 kB hard line; video only at >=1024 px with `prefers-reduced-motion: no-preference`; AV1, VP9, H.264; never HEVC | `design-process.md:66`-`:67` | mech | T (#3079), "calculated, not measured" | EB | none |
| X8 | Licence gates: no Seedream, Flux or Google image, and no clip, ships until its ownership clause is read and its gist is on #3092 | `design-process.md:58`, `:65` | y/n | T | EB | none |
| X9 | Page-background candidates are judged behind the real search-results layout | `design-process.md:59` | y/n | T (#3059) | TL | none (also vault R17) |
| X10 | Anything carrying the manta device goes through Marisha before print while `collab-ip` is unsigned | `design-process.md:73` | y/n | T | proc | none |
| X11 | AI-slop markers, "reject on sight": 13 items (purple-to-blue or mesh gradients, glassmorphism, glow borders, gradient text, centred hero with two pills, icon-in-circle grid, uniform icon cards, blobs, stock smiling group, placeholder avatars, emoji bullets, lorem ipsum, §11 tells "Unlock", "Elevate", "Seamless") | `design-process.md:39`-`:44` | mech + y/n | - | EB | brief only |
| X12 | Copy recommendations never name a competitor or anchor on fake-review policing or meet-people | `design-review/SKILL.md:61`-`:66` | y/n | T (#78, #3652) | EB | DR (as context for DC) |

**Count outside the sheet: 12 rules** (X11 holds 13 items). X1-X3 contradict `DESIGN.md:110`: the file says it is derived, but it is the only home of three rules.

**Finding: X11 is the House DNA under another name.** X11's 13 items are DNA lines D1-D7 almost word for word (`data/gallery.json:13`-`:19`). The prefill says "Never the vault's House DNA" (`design-process.md:13`), and `design-round/SKILL.md:38` says the same. So Manta takes the first seven DNA lines as a copy, and does not take D9-D12.

**Finding: the "§11's banned tells ('Unlock', 'Elevate', 'Seamless')" pointer is false.** `grep -i 'unlock\|elevate'` finds neither word in `brand-sheet.md` §11 (only "elevated" at `:50`, a different word) and finds neither in `scripts/check-website-copy.js`. "Seamless" is in §11's guide review pass as a word swap (`brand-sheet.md:265`), not in the banned list. The pointer is in `design-process.md:44` and DNA D7 (`data/gallery.json:19`). No script checks these three words for any project.

### 4d. Manta totals

| File | Rules held | of which unique to the file |
|---|---|---|
| brand-sheet.md | 53 design + ~10 process + copy rules (not counted) | 53 (it is the source) |
| DESIGN.md | ~46 statements | 3 (X1-X3) |
| PRODUCT.md | ~14 statements | 1 (X4), plus X5 and X6 shared |
| design-process.md | Guardrails prefill (~30 clauses) + X7-X11 | 4 (X7, X8, X10, X11) + X9 shared with the vault |
| design-review/SKILL.md | 7 gate checks + 1 pre-launch check + X12 | 1 (X12) |
| **Manta, distinct** | **65** (53 + 12) | |

Manta form split (65): mech 27, y/n 33, hol 5. A critic gate asks 11 of the 65 by name (the 10 in §4b and X5). Context alone carries 47 (41 in §4b, and X1-X4, X6, X12). The brief alone carries 1 (X11). Nothing carries 6 to a critic (B26, B27, X7, X8, X9, X10).


---

## 5. mmm-infra (`~/mmm-infra`)

The rules file is `docs/brand/brand-sheet.md` (56 lines). `data/gallery.json` `projects.mmm-infra.rules` and `~/mmm-infra/CLAUDE.md:39` both name it. `~/mmm-infra/PRODUCT.md:5` says the brand sheet is the authority and wins over PRODUCT.md. mmm-infra has no design gate of its own (no `design-review` skill; `ls ~/mmm-infra/.claude/skills` returns nothing). So design-critique writes "no gate" (`design-critique/SKILL.md:59`), and the House DNA and the craft gate are its whole standing rule set. 

Most of the sheet records facts and open questions, not rules: the palette, the type and the look are open (`brand-sheet.md:13`, `:26`; `PRODUCT.md:38`). `docs/brand/voice-guide.md` (161 lines, 14 rules) is copy and is not counted.

| # | Rule | Where | Form | Src | Time | Asked |
|---|---|---|---|---|---|---|
| I1 | Palette, type and look are open; a motion or brand-art round waits for the identity round (vault R1) | `brand-sheet.md:13`, `:26`; `PRODUCT.md:38` | y/n | T (#8, #10) | proc | none |
| I2 | A brochure site: no shop, no payments, no bespoke software | `brand-sheet.md:42`; `PRODUCT.md:35` | y/n | T (Mark) | BR | ctx |
| I3 | Angélique can update it easily, at least as easily as on Wix | `brand-sheet.md:43`; `PRODUCT.md:36`, `:57` | hol | T (Mark) | BR | ctx |
| I4 | Refresh the images, possibly from Mark's LinkedIn | `brand-sheet.md:44` | hol | T (Mark) | BR | ctx |
| I5 | Video is welcome; busyness and advocacy are not | `brand-sheet.md:45`; `PRODUCT.md:44` | hol | T (Mark) | BR | ctx |
| I6 | Not busy: no stacked panels, clocks, sign-in boxes or campaign slogans | `PRODUCT.md:56` | y/n | - | BR | ctx |
| I7 | Calm before asking: one quiet moment before any text asks for anything | `PRODUCT.md:55` | y/n | - | TL | ctx |
| I8 | Mark is the brand: every page feels like meeting him | `PRODUCT.md:54` | hol | T (Mark) | BR | ctx |
| I9 | Opening animation: the spirit of Mark's ideas, not the letter (aqueduct built in a realistic sequence, under a minute, no construction workers, a dissolve to the homepage) | `brand-sheet.md:46` | hol | T (#9) | BR | ctx |
| I10 | Opening animation 3-5 s, a Skip control, once per visitor; a reduced-motion version | `PRODUCT.md:31`, `:61` | mech | R (`docs/research/animation-length.md`, #13: NN/g, WCAG 2.2.2) | TL + EB | DC (G4) |
| I11 | A build that must end exactly on the logo stays hand-built SVG | `brand-sheet.md:56` | y/n | T (#5) | EB (2026 video models) | DC (G6, in effect) |
| I12 | Tools: GPT Image 2.5 for pictures; Seedance for scene films (overrides the vault's drop); Kling 3.0 for loops | `brand-sheet.md:51`-`:55` | y/n | T (#9) | EB | none |
| I13 | No testimonials, client logos, counts or press may be invented | `PRODUCT.md:50` | y/n | - | TL | DC (L7) |
| I14 | Body text comfortable at length, for office monitors and phones | `PRODUCT.md:61` | hol | - | TL | IC (type measure, `craft-floor.md:12`) |
| I15 | LoveFrom means only "smooth animation built around the aqueduct"; keep it out of the vault | `brand-sheet.md:47` | y/n | T (#1) | proc | none |

**Count for mmm-infra: 15 rules** (5 in the brand sheet alone, 6 in PRODUCT.md alone, 4 in both). Form: mech 1, y/n 8, hol 6. Source: research 1 (I10); ticket or client 10; none 4. Time: timeless 3 (I7, I13, I14), timeless + era-bound 1 (I10), brand choice 7, era-bound 2 (I11, I12), process 2. Asked by name: DC 3 (I10, I11, I13), IC 1 (I14). Context only: 8. None: 3.

**Finding: the ruled animation length is not in the rules file.** `PRODUCT.md:31` holds "3-5 s, Skip, once per visitor" (#13), with a research note behind it. The brand sheet, which `PRODUCT.md:5` makes the authority, still gives only Mark's "in under a minute" (`brand-sheet.md:46`), framed as a suggestion. `design-round/SKILL.md:23` tells a session to read "the project's rules file" before a motion round. A session that reads only the rules file does not see the ruled length.

**Nearest analogue to a rulebook, in mmm-infra.** `docs/research/photo-rubric-v4.md` (sampled, `:17`-`:28`) puts numbered vetoes (V1-V5, each a yes/no threshold per use, for example "the use's crop is enlarged more than 1.5x on a 1440 x 900 laptop") before a score, and versions them v4 to v4.3. It applies to photo choice only, and a script applies it (`private/photo-runs/...`, not opened).


---

## 6. Totals across the house

| Source | Rules | mech | y/n | hol | proc | Literature cited | Measured / standard cited | Timeless | Era-bound | Brand choice | Process (time) | Asked by name by a critic |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| design-vault (portable) | 84 | 22 | 43 | 14 | 5 | 1 | 0 | 31 (+4 mixed) | 28 | 0 | 21 | 39 (DC or IC) |
| Manta (one project) | 65 | 27 | 33 | 5 | 0 | 0 | 21 | 27 (+3 mixed) | 14 | 20 | 1 | 11 (DR gate) |
| mmm-infra (one project) | 15 | 1 | 8 | 6 | 0 | 1 | 0 | 3 (+1 mixed) | 2 | 7 | 2 | 4 (DC 3, IC 1) |
| **All** | **164** | **50 (30%)** | **84 (51%)** | **25 (15%)** | **5 (3%)** | **2 (1%)** | **21 (13%)** | **61 (+8 mixed)** | **44** | **27** | **24** | **54 (33%)** |

- **About 155 distinct rules.** Nine rows restate another row: R24 = G1-G3; F3 = R5; F5 = R26; R31, D8, X5 and I13 = L7; X11 = D1-D7; X9 = R17.
- **Portable: 84. One project's: 80** (Manta 65, mmm-infra 15). About 12 Manta rules would hold for any project but live only in Manta's files (B10, B19, B21, B26, B27, B39, B47, B49, B50, X2, X3, and B4 as "measure contrast").
- **Research.** Two rules cite literature or a benchmark: the animal benchmark behind R15 (`roster.md:50`) and the length research behind mmm-infra's I10 (`~/mmm-infra/docs/research/animation-length.md`). G4 and R20 *require* a research source in each motion brief, but the rule itself cites none. Manta's 21 "measured" rules cite contrast ratios, L* and ΔE that the sheet computed. They do not cite studies.
- **Asked.** A critic prompt asks 54 of 164 rules by name. 55 reach a critic only as context (a rules file handed over with "a project rule is not a deficiency"). 9 reach a critic only as a brief line (R2, R3, X11, and DNA D2, D3, D6, D9, D10, D12). 46 reach no critic at all.

---

## 7. Answers

### (a) Is there a design rulebook like business correspondence's?

**No.** No design file has the structure of `~/mantahostels/docs/copy/outbound-messaging.md`.

That file has: a header that states its scope and which file wins on what (`outbound-messaging.md:1`-`:5`); a grades table that ranks evidence strength, Strong, Moderate, Weak and Don't (`:9`-`:18`); a rule that every rule binds fully and a grade decides only a conflict (`:20`); a purpose test, "letter broken, purpose served" (`:22`); and Check questions that every reviewer answers Yes, No or Unsure, quoting the words behind a No (`:24`). Each rule has a title with its grade, a **Purpose** line, lettered sub-items that can carry their own grades, an Evidence link, and numbered Check questions that end with a Purpose question (rule 1 at `:54`-`:73`; rule 9 at `:207`-`:223`).

The design files have these parts of it:

| Rulebook part | Nearest design equivalent | Gap |
|---|---|---|
| Numbered rules with a check each | The craft gate: 6 numbered rules, each with a "Check:" and PASS / FAIL / does not apply (`design-critique/SKILL.md:22`-`:29`) | Geometry and motion only. No grade, no purpose line, no evidence link. |
| Pass/fail list | Manta's gate: 7 checks (`design-review/SKILL.md:33`-`:48`) | Statements, not questions. Reasons live in DESIGN.md. Covers 10 of Manta's 65 rules. |
| A ban list | House DNA `never` (12 lines) and Manta's AI-slop markers (13 items) | No check form, no source, no grade. They do not agree on strength: "defaults" in the DNA, "reject on sight" in the Manta copy. |
| Scored heuristics | impeccable critique: Nielsen's 10, scored 0-4 (`impeccable/.../reference/critique.md:97`-`:118`) | Vendor's; scores, not yes/no. Not the house's rules. |
| Vetoes before a score | mmm-infra photo rubric v4 (`~/mmm-infra/docs/research/photo-rubric-v4.md:17`-`:28`) | Photo choice only. |
| Evidence grades | None | 2 of 164 rules cite literature. |
| A rule for conflicts | File precedence only: "the project's guide wins" (`design-round/SKILL.md:10`), "the brand sheet wins" (`DESIGN.md:110`), "the project's rules file wins over PRODUCT.md and DESIGN.md" (`references/impeccable.md:8`) | Nothing ranks two rules by strength. Nothing ranks the house's rules against impeccable's own bans. |

**What can convert.** 50 rules (30%) are mechanical: a script can check them. 84 (51%) are yes/no: they can become Check questions as they are written. Only 25 (15%) are holistic taste. These are mostly the Gestalt walk, the conversion lenses, "avoid the source's signature" and Manta's zone volume. They need a scored or comparative instrument, not a yes/no.

### (b) Where rules conflict, or one project's rule overrides a portable one silently

1. **Spring motion.** Manta bans "bounce or spring" motion (`brand-sheet.md:220`, `:403`; the prefill's Never list, `design-process.md:37`). The vault requires a landing on "a critically or highly damped spring" and a heavy settle on a critically damped spring (`design-round/SKILL.md:157`-`:158`). Craft gate G3 fails a fall that does not land that way (`design-critique/SKILL.md:26`). A critically damped spring does not overshoot, so the conflict can be one of words only. But the prefill bans "spring motion" with no UI scope, and no file reconciles the two. Manta's hero motion is still open (#2989, `design-process.md:63`), so no round has hit it yet.
2. **Motion tokens with no scope.** The Manta prefill says "Motion 120/180 ms, cubic-bezier(0.2,0,0,1)" with no scope (`design-process.md:28`). The vault keeps UI caps for UI motion and takes a brand piece's length from its motion brief (`design-round/SKILL.md:161`). `design-process.md:68` scopes the tokens to UI motion, but the prefill that goes into the brief does not. (Manta's curve starts from rest, so it does not fail G3.)
3. **Eyebrows.** impeccable's craft floor bans a kicker or eyebrow above a heading: "a ban, not a default: no brief earns it back" (`craft-floor.md:27`). Manta's sheet specifies "Hero eyebrows" in ink (`brand-sheet.md:26`), and `~/mantahostels/app/globals.css` uses the word once (grep count; not opened in full). No house file says which wins. `references/impeccable.md:8` makes the rules file win over PRODUCT.md and DESIGN.md, not over impeccable's own bans.
4. **Coloured left rule.** impeccable refuses "a colored `border-left` ... above 1px on cards, list items, callouts" (`craft-floor.md:35`). Manta's hostel testimonial requires "a single `lagoon` left rule" (`DESIGN.md:203`), with no width given. impeccable's own precedence lets "the committed visual world" override it (`craft-floor.md:3`). This is a silent override: no file records it, and the impeccable detector can flag it on each edit.
5. **Grey secondary text.** impeccable: "On colored surfaces tint secondary text from that hue or the foreground; never gray" (`craft-floor.md:9`). Manta: `muted-night #8f999e`, a near-grey, for all secondary copy on the ink ground (`brand-sheet.md:60`). This conflicts by the letter. It is a weak conflict.
6. **Risk-reversal.** design-critique's conversion lens asks for "risk-reversal microcopy" (`design-critique/SKILL.md:40`). Manta's sheet put "risk-reversal guarantees" on "the wrong side of the urgency-theatre ban" (`brand-sheet.md:267`). That line is in the copy section, which the critic does not get as a design rule. design-critique §3 ("a project rule is not a deficiency") protects Manta only when the critic finds that line.
7. **The same ban at two strengths.** The DNA's never-lines are "defaults, not absolute rules" that a project's lines override (`data/gallery.json:10`; `design-round/SKILL.md:39`). Manta's copy of the same lines is "reject on sight" (`design-process.md:39`). The portable version is weaker than the project copy. Also, design-critique "carries no hard bans; a project's own gate does" (`design-critique/SKILL.md:3`). mmm-infra has no gate, so no gate checks the DNA for it. And when a project line overrides a DNA line, no file records which line it overrode.
8. **Tool roster (a tool rule, not a candidate rule).** The vault rates Ideogram 4.0 `use — as candidates` at 2560x1440 (`roster.md:32`). Manta drops it as "Below a 2K hero" (`design-process.md:87`), and the vault's measured size contradicts that reason. Recraft V4.1 is `drop` in the vault (`roster.md:36`) and `trial` in Manta (`design-process.md:83`). GPT Image is `use — first, always` in the vault (`roster.md:29`) and `use — as candidates` in Manta (`design-process.md:85`). Tweakpane is rung three in the vault (`roster.md:103`) and rung two in Manta (`design-process.md:97`). Manta's brand-art route is "Higgsfield Starter ... Web UI only, no MCP" (`design-process.md:57`), and the vault's route is the API through `higgsfield.js` (`design-round/SKILL.md:138`). The vault accepts this drift (`roster.md:3`). mmm-infra's Seedance override (`~/mmm-infra/docs/brand/brand-sheet.md:54`) is explicit, so it is not silent.
9. **Easing for brand motion.** impeccable's craft floor asks for "exponential ease-out from an already-visible default" (`craft-floor.md:13`). The vault flags a UI curve that "starts at full speed" on a brand piece (`design-round/SKILL.md:154`). The vault resolves this in its own text (UI motion only, `:161`). But impeccable's critique runs on the same candidate (`design-critique/SKILL.md:16`) and can recommend the curve that G3 fails. mmm-infra measured this: "our engine's ease-out fails our own check-flow.py jolt rule" (`~/mmm-infra/docs/doc-map.md:62`).

### (c) Rules stated in so many places that they can drift

Drift has already started in four of them:

1. **The brand-sheet version.** `DESIGN.md:110` and `PRODUCT.md:52` name v2.32. The sheet is v2.37 (`brand-sheet.md:1`).
2. **The DNA and Manta's AI-slop list.** The two lists have already diverged: DNA D2 "Glossy 3D SaaS blobs and floating blob shapes" against "floating blob shapes"; DNA D4 adds "or any icon-grid feature row". Both cite §11 tells that §11 does not hold (§4c).
3. **mmm-infra's animation length.** The ruled 3-5 s is in `PRODUCT.md:31`. The authority file still says "under a minute" (`brand-sheet.md:46`) (§5).
4. **Rules in a "derived" file only.** DESIGN.md holds three rules the sheet does not (X1-X3).

Rules with five or more homes:

| Rule | Homes |
|---|---|
| Never invent proof (testimonials, logos, counts, press, usage figures) | 8: `design-critique/SKILL.md:44`; `design-round/SKILL.md:150`; `prompts.md:21`; DNA `gallery.json:20`; Manta `PRODUCT.md:67`, `design-review/SKILL.md:50`-`:52`, `design-process.md:37`-`:38`; mmm-infra `PRODUCT.md:50`. The lists already differ: "usage figures" is in DC and Manta PRODUCT.md, not in the DNA or `design-round:150`. |
| coral CTA-only, one per view (B12) | 6: `brand-sheet.md:52`, `:63`, §12 `:301`, §13 `:346`; `DESIGN.md:138`, `:205`, `:215`; prefill `:22`, `:32`; design-review g1 |
| A score always with its count and word (B36) | 6: `brand-sheet.md:185`, §13 `:395`-`:399`; `DESIGN.md:199`; `PRODUCT.md:48`; prefill `:30`-`:31`; design-review g7 |
| No urgency theatre (B49) | 6: `brand-sheet.md:224`, `:226`, §13 `:423`; `DESIGN.md:222`; `PRODUCT.md:47`; prefill `:35`; design-review g6 |
| Sentence case, no emoji (B30) | 6: `brand-sheet.md:136`, §11 items 9-10 `:246`-`:247`, §13 `:404`; `DESIGN.md:167`, `:225`; `PRODUCT.md:57`; prefill `:26` |
| Differentiation firewalls (B52) | 6: `brand-sheet.md:300`-`:306`, §13 `:431`-`:437`; `DESIGN.md:216`; `PRODUCT.md:25`; prefill `:32`, `:37`; design-review g2 |
| Ink on turquoise; mark and rating unit off turquoise; white-on-coral size; colour alone; row CTA; prices; handover (B4, B5, B19, B25, B29, B40, B53) | 5 each (see §4b) |
| Manta UI motion tokens (B48) | 5: `brand-sheet.md:220`, §13 `:402`; `DESIGN.md:191`; prefill `:28`; `design-process.md:68` |
| Render three widths | 4: `design-round/SKILL.md:137`; `impeccable.md:26`; `polish.md:45`; `prompts.md:196` |
| The 250 ms pause limit | 4 places in 2 files: `design-critique/SKILL.md:26`; `check-flow.py:20`, `:501`, `:734` |
| Manta's open illustration rules (B41) | 4, across repos: `brand-sheet.md:195`, §13 `:417`; prefill `:29`-`:31`; the vault's own group headers `data/gallery.json:789`, `:799`, which restate Manta's palette rules although `design-critique/SKILL.md:8` says "never restate a project's palette" |

Manta has 40 of its 53 sheet rules in three or more homes. One mechanism exists against drift: §13 says a change to a section "is carried to that prefill in the same edit" (`brand-sheet.md:327`). No check enforces it. DESIGN.md is fixed "by correcting this file" (`DESIGN.md:110`), and the stale v2.32 shows that this has not happened since 2026-09-15.


---

## Bound

**Read in full:**
- `plugin/skills/design-critique/SKILL.md`; `plugin/skills/design-round/SKILL.md`; `references/prompts.md`, `roster.md`, `impeccable.md`, `polish.md`, `comparison.md`.
- `data/gallery.json` lines 1-30 (the `dna` block) and the `projects` block. The `git log -S` provenance of DNA lines 14 and 20-24, and of the description.
- `~/mantahostels/DESIGN.md`, `PRODUCT.md`, `docs/brand/design-process.md`, `.claude/skills/design-review/SKILL.md`.
- `~/mantahostels/docs/brand/brand-sheet.md`, all 462 lines, in three Read calls (1-150, 150-309, 310-463).
- `~/mmm-infra/docs/brand/brand-sheet.md`; `~/mmm-infra/PRODUCT.md` (all 61 lines).
- impeccable 4.5.0 `reference/craft-floor.md`. The installed versions in `~/.claude3/plugins/installed_plugins.json`: Manta's project scope has 4.2.1, the user scope has 4.5.0, and `references/impeccable.md:3` names 4.2.1.

**Sampled only:**
- `~/mantahostels/docs/copy/outbound-messaging.md`: the heading list, lines 1-40, rule 1 (`:54`-`:75`) and rule 9 (`:207`-`:225`).
- impeccable 4.5.0 `reference/critique.md`: headings, lines 1-60, lines 97-131.
- `~/mmm-infra/docs/brand/voice-guide.md`: headings only.
- `~/mmm-infra/docs/research/photo-rubric-v4.md`: headings and veto rows. `photo-rubric-v4-3.md`: lines 1-26. `animation-length.md`: lines 1-12 and its `doc-map.md` row.
- grep only: `check-flow.py` (the 250 ms default), `scripts/check-website-copy.js` (no "unlock", "elevate" or "seamless"), `app/_lib/ground-context.tsx:5`, `app/globals.css` (one "eyebrow").

**Not opened:**
- impeccable's other references (`audit.md`, `animate.md`, `polish.md` and the rest), its `SKILL.md` beyond a grep, its detector code (not found in `scripts/`; the bundled `impeccable` is a shell wrapper), and the 4.2.1 copy that Manta's project scope loads. The census reads 4.5.0's craft floor; 4.2.1's can differ.
- `~/mantahostels/docs/design-system/` (the Claude Design corpus and `guidelines/`), `docs/inspiration/catalogue.json`, `docs/research/*` behind the design process, `docs/copy/outbound-messaging-evidence.md`, Manta's `AGENTS.md` §Business invariants.
- `~/mmm-infra` `CLAUDE.md` and `AGENTS.md` (grep only), `docs/research/design-process-order.md`, `animate-vs-our-method.md`, `docs/copy/`.
- The vault's scripts other than a grep of `check-flow.py`: `check-curves.js`, `check-frames.py`, `fall.js`, `cutout.py`, `higgsfield.js`.
- No GitHub issue was read. The ticket numbers cited are as the files cite them.

**Method limits.** One reader classified every rule as mech, y/n or hol, as timeless, era-bound or brand, and decided where a rule splits into two. Another reader can split or merge rows in a different way, and the counts can move by about 10%. The "asked" column records what a prompt text asks by name. It does not record what a critic did in a real run.
