# Research #203: why #104's coverage audit and #101's rulings missed the gaps in the founder's notes (map #202)

Status: complete (15 Oct 2026).
Language: ASD-STE100 Simplified Technical English.
Question (#203): Why did #104's coverage audit, and #101's rulings on it, miss the gaps that the founder's 15 Oct 2026 notes found? What in the method let them through?

Method: a post-mortem from local evidence. I read the issue bodies, the resolution comments, the research notes and `git log`. I test each candidate cause against each gap that #205 found.

Abbreviations:
- **G1 / G2 / G3**: the granularity key of #207 (`docs/research/topic-taxonomies.md:12-15`). G1 = a whole subject ("Typography"). G2 = a group of decisions ("Type scale"). G3 = one decision ("tracking of headings").
- **C1 … C12**: the causes in this file (candidates 1–8 from the dispatch, plus causes that the evidence added).
- **Ref**: a house reference that reaches a critic or a builder by default (`plugin/skills/design-critique/references/*.md`, `SKILL.md`, `gate.md`, `design-round/references/impeccable.md`). **Res**: `docs/research/` only.

## Finding 1. The timeline (from issue timestamps and `git log`)

| Time (UTC) | Event | Evidence |
|---|---|---|
| 13 Oct 08:47 | Map #96 filed. The founder's coverage words are one side question on a map about a critic check | `gh issue view 96`, Notes, first bullet |
| 13 Oct 08:48–09:02 | #97, #98, #99, #102 and #104 filed, five tickets in 15 minutes | `createdAt` of each issue |
| 13 Oct 09:02:10 | #104 filed, with its 14 areas already listed in the body | `gh issue view 104` body |
| 13 Oct 09:26:42 | #104's note lands in one commit with #98's and #99's notes | `git log 8e242c1` (17:26:42 +0800) |
| 13 Oct 09:33:11 | #104 closed: 31 minutes after it was filed | `closedAt` |
| 13 Oct 09:36 | #117 filed. Its body says #104's frame "has no row for the visual attributes every component is drawn with" | `gh issue view 117` body |
| 13 Oct 09:59 | #123 filed. Its body says "#104's frame covers type size and measure and colour contrast, but not how text is drawn" | `gh issue view 123` body |
| 13 Oct 10:32 | #119 closes: the house "writ[es] only what no outside source covers" | #119 resolution |
| 13 Oct 18:14 / 18:34 (+0800) | #117 and #123 research notes land | `05c074f`, `3b96fcf` |
| 14 Oct 05:44 | #101 closes. The founder answered "Accept recommendations", (A) on every question | #101 resolution |
| 14 Oct 13:47 | #174 closes. The text reference carries "the tint rule and the link rule" only | #174 body; `6cfa8d8` (29 lines) |
| 14 Oct 15:25 / 15:42 | #183 audits the values that the references hold; #194 corrects them | #183, #194 resolutions |
| 15 Oct | The founder's notes N1–N19 (map #202); #205 finds 6 gaps | `docs/research/notes-coverage.md:384` |

The fact from the timeline that matters most: #104 was open for 31 minutes. It was one of five tickets that ran in the same window, and its note landed in a shared commit. A G3 extraction over 12–15 sources costs about 2–4 sessions (#207, `topic-taxonomies.md:186`). One 31-minute pass cannot reach G3.

## Finding 2. The candidate causes, one at a time

### C1. The question's author chose the frame's areas; the areas did not come from outside sources — CONFIRMED

- #104's body lists the areas before any research: "Build a current coverage frame for website design from authoritative sources: perception and Gestalt, visual hierarchy, typography, colour, layout and spacing, imagery, motion, interaction and feedback, content and microcopy, conversion and trust, accessibility, performance, responsive design, brand expression" (`gh issue view 104` body). The ticket says "from authoritative sources", but it gives the list.
- The frame in the note (`docs/research/design-coverage-gaps.md:186-208`) has 21 rows: the 14 areas of the ticket, plus 7 that the researcher added (first impression, forms, navigation, accommodation search, dark mode, SEO, accessibility law). Each added row came from a finding on a gap in a site (Manta, a small-business site). No added row came from a source's table of contents.
- #104's Bound lists no source taxonomy. It read no design-system tree, no book table of contents and no curriculum (`design-coverage-gaps.md:251`). It says that Refactoring UI and Bringhurst were "Not opened … their points enter only through impeccable's rules" (`design-coverage-gaps.md:253`). These are two of the three sources that #207 found name single decisions (`topic-taxonomies.md:244`).
- The same pattern repeats one level down. #117 and #123 also got scope lists that their author chose:
  - #117: "Borders and outlines (component edges, input fields, outline buttons) … Fills, tints and surface tones (cards, wells, selected and hover grounds) … Focus rings and state outlines" (`gh issue view 117` body). A ring appears only as focus. A fill appears only at component level. Page sections and gradients are not in the list.
  - #123: "Text colour … Emphasis and hierarchy … Links … Text on grounds … Rendering: font smoothing, optical sizes, variable-font grades" (`gh issue view 123` body). Line breaking, choice of a variable font, and the typeface's metrics are not in the list.
- Gaps that C1 explains: N2a, N2b, N5 (the #117 list), N1g, N4 choice, N19b (the #123 list). All six.

### C2. Rows were whole subjects, so a single decision had no row — CONFIRMED

- The frame rows are G1: "Typography", "Colour", "Layout, grid, spacing" (`design-coverage-gaps.md:191-193`). #207 says: "#104 drew its ~20 areas at the curricula's level (G1), so it could not see decision-level gaps" (`topic-taxonomies.md:244`).
- A G1 row takes one label (C, P or G) for the whole subject. The Typography row is "P" because of one value, Manta's 14–15.5 px body text (`design-coverage-gaps.md:191`). The label says nothing about tracking, case, line breaking, variable fonts or font metrics.
- No row exists for surfaces. #117's body states this fault on the same day: the frame "is cut by discipline (colour, typography, layout, …). It has no row for the visual attributes every component is drawn with" (`gh issue view 117` body).
- All six gaps are G3 decisions (`notes-coverage.md:357-380`). None of them can show as a separate row in a G1 frame.
- Gaps that C2 explains: all six.

### C3. "Covered" meant that impeccable (or Manta) mentions the subject; it did not mean sourced, conditioned and carried — CONFIRMED

- The frame's key gives no definition of "covered". It gives only the letters: "House: C = covered, P = partly covered, G = gap. imp = does impeccable fill it when design mode is on" (`design-coverage-gaps.md:182`).
- In use, a mention by impeccable counts as coverage: "Visual hierarchy | … | C: impeccable `layout`, `typeset`" and "Layout, grid, spacing | … | C: impeccable `layout`; Manta 8px grid" (`design-coverage-gaps.md:190`, `:195`). The note's answer says: "Timeless foundations (Gestalt, hierarchy, colour, typographic measure) are mostly covered, through impeccable and Manta's sheet" (`design-coverage-gaps.md:243`).
- The same note also says that impeccable "cite[s] no source" (`design-coverage-gaps.md:177`), and impeccable reaches a critic only with design mode on (`notes-coverage.md:347`). Thus the frame counted as "covered" a rule with no source, which the default critic does not read.
- "The house" included Manta's values (#104 body: "Map the frame against … Manta's rules files"). #115 then found that Manta's work does not reach a second project (#96 decision line for #115). A Manta value counted as house coverage.
- A ban counted as coverage. Brand expression is "C as taste (House DNA, Manta §12, impeccable concept-seed)" (`design-coverage-gaps.md:207`), and #104 W13 calls the bans "Covered as taste, well beyond the published evidence" (`:170`). For N2b, the house holds only bans on gradients; it never says when a gradient is right (`notes-coverage.md:93`).
- The impeccable lines for three gaps exist, and #104 read them:
  - N1g: `craft-floor.md:12` "balanced headings" (impeccable 4.5.0; no condition, no source).
  - N4: `typeset.md:23` "variable-font settings avoid invisible text and disruptive reflow" (delivery only).
  - N19b: `typeset.md:21` "tracking tuned to the actual face" (no rule for how).
  #104 read both files in full (`design-coverage-gaps.md:247`). Under a "mention = covered" test, these lines made Typography look held.
- #205 later applied the stricter test: "covered: the house has a rule. The rule has a source, a condition and a trade-off, and it gets to a skill or a critic" (`notes-coverage.md:6`). Under that test the 19 notes give 6 gaps and 19 partial verdicts (`notes-coverage.md:384`).
- Gaps that C3 explains: N1g, N2b, N4, N19b directly; N2a and N5 through the Layout and Colour rows that impeccable or Manta "covered".

### C4. The ranking weighed how often a gap hit Manta, and this pushed visual-craft questions down — PARTLY CONFIRMED (not at #104; yes at #117, #123 and #101 Q6)

- At #104, rejected for the six gaps. The six gaps had no row (C2), so the ranking never saw them. The ranking did not push them down; it had nothing to push. The one row that stood for all of web craft, rank 5 "A sourced house reference for web craft (L2)", affects "All web sites" (`design-coverage-gaps.md:227`). The frequency rule did not rank it low.
- At #117 and #123, confirmed. Each ticket ranked its gaps "by how often they affect the Manta site" (`gh issue view 117`, `gh issue view 123` bodies). #123 rated optical size and grade "Low" because Manta's two fonts have no `GRAD` axis (`docs/research/text-presentation.md:282`, `:327`). That is the root of N4's rendering part. Most #123 gap rows end "Owner: mantahostels" (`text-presentation.md:316-326`), and the resolution sent "the tint rule, text tokens, numerals and caps tracking" to Manta's out-of-scope list (#123 resolution). A portable principle found as a Manta fault left the vault's write scope as a Manta fix. Example: "Row 8 (caps tracking, the eyebrow conflict) is Manta's" ([`text-presentation.md:3`](https://github.com/lucmoseley/design-vault/blob/88e3428e1/docs/research/text-presentation.md#L3)); this is part of N14 and N16.
- At #101, confirmed for the partial notes. Q6 accepted as gaps "sentence case (T5)", "icon line weight at other sizes" and "taste for colour and busy layouts by audience", because "Each one is rarely needed, poorly sourced, or a single line" (#101 resolution, Q6). These are parts of N16 and N7. They were not missed; they were ranked out on reach.
- Gaps that C4 explains: N4 (rendering part, through #123's Manta ranking). Partial notes: N14, N16, N7.

### C5. #101 accepted ranks as filled by later research, and nobody re-checked the research against the frame — CONFIRMED

- #101 Q4 (A) accepted as filled: "A sourced craft reference: impeccable pinned, plus a house override file … Type and spacing scales: one source per project … Surface styling (#117), text colour (#123)" with "Confidence: 80% … Each one already has a sourced answer on this map" (#101 comments, round 1 re-post, Q4).
- The ruling session did not read the research it accepted. Its Bound says: "The gap lists themselves come from round 1 as the 13 Oct session gathered them from #104, #115, #117, #118, #119, #123, #127 and #130; this session did not re-read those tickets" (#101 resolution, Bound).
- Rank 5 (a sourced craft reference) was accepted as filled by "impeccable pinned with a house override file". The override file corrects the rules that impeccable has (#119: "26 right … 11 right but stated without conditions … 3 wrong"; #119 resolution). It does not add the decisions that impeccable does not have. Thus the acceptance closed the one row that stood for all of web craft without a check of what that row held.
- #115 had found that "spacing and type scales were never researched" (map #96, decision line for #115). #101 Q4 then accepted "type and spacing scales from one source per project" as filled. This assigned the value to the project, and it removed the question of how a project sets size, leading and tracking from its typeface. That question is N19b.
- The founder's answer was "Accept recommendations", (A) on every question (#101 resolution, heading). #194 records the result: "The founder ruled on these only through 'accept recommendations' … so each figure was an agent's" (`gh issue view 194` body). The round's options were "fill" or "accept" per gap. No option asked whether the frame was complete.
- Later audits checked values, not coverage. #183's method is "a grep over `docs/research/` and #154's body" for items labelled "house" (`gh issue view 183` body, step 1). A grep for what a file holds cannot find what no file holds. #194 corrected the figures in the two references; it added no topic.
- Gaps that C5 explains: N19b directly; all six indirectly, because the acceptance closed rank 5 and no later step re-tested the frame.

### C6. The audit read impeccable's commands but not every reference file — REJECTED for the six gaps

- #104 read in full impeccable 4.5.0 `SKILL.md`, `craft-floor.md`, `mode-operate.md`, `mode-persuade.md`, `mode-read.md`, `audit.md`, `typeset.md`, `colorize.md`, `layout.md`, `animate.md` and `clarify.md` (`design-coverage-gaps.md:247`). It sampled `critique`, `adapt`, `optimize`, `harden`, `polish` and `new-work` (`:249`).
- The impeccable lines that touch the gaps are in `craft-floor.md:12` (N1g) and `typeset.md:21`, `:23` (N4, N19b), which #104 read in full. The gap is not unread files. The gap is that a read line counted as coverage (C3), at G1 (C2).
- impeccable holds nothing on N2a, N5 resting rings, or a functional gradient (`notes-coverage.md:86`, `:96`, `:142-143`). More reading of impeccable could not find these.
- What #104 did not read is the outside G3 sources: Refactoring UI and Bringhurst "Not opened" (`design-coverage-gaps.md:253`). That is C1 and C10, not C6.

### C7. Loss between research and references: a ruling decided what crosses, and its test was "no outside source covers it" — CONFIRMED (this is the main cause of the "partly" verdicts)

The chain of rulings, in order:
1. #100 Q1 (A): "the critic asks yes/no questions only of the rules that can fail a candidate … Everything else stays impeccable's whole-page critique plus design-critique's lenses" (#103 comments, scope line). A principle that cannot fail a candidate goes to impeccable, which runs only with design mode on.
2. #103: "only rules that can fail a candidate become gate questions … Row 3's tint rule is not a gate question; whether it goes into #119's house override file is for map #96's spec" (banner, [`docs/research/text-presentation.md:3`](https://github.com/lucmoseley/design-vault/blob/88e3428e1/docs/research/text-presentation.md#L3)). #103 also cut `inputs`, `output` and `trades-off` from the rule form ([`docs/research/principle-interactions.md:3`](https://github.com/lucmoseley/design-vault/blob/88e3428e1/docs/research/principle-interactions.md#L3)).
3. #119: "the house writ[es] only what no outside source covers" (#119 resolution). Its per-area table sets Typography to "ENFORCE + EXTEND: Enforce impeccable `typeset`; cite Butterick per rule" and Layout to "ENFORCE: … no house writing needed" (`docs/research/adopt-or-build.md:175`, `:179`). These rows use #104's G1 areas.
4. #101 Q5 (A): the house-written pieces are "#123's text-tint rule" and "#117's surface-styling method", among others (#101 resolution, Q5). From #123, only the tint rule is named.
5. #154 (the spec): "A house principles reference in design-critique holds … only the pieces no outside source covers (#101 Q4–Q5, #119)", and for #123, the tint rule and the link rule (`gh issue view 154` body, §The house method, "Text presentation (#123)").
6. #174 builds exactly that: "text presentation (#123; `text-presentation.md`) — the tint rule and the link rule" (`gh issue view 174` body). The file is 29 lines (`6cfa8d8`).

The test at each step was "can it fail a candidate?" or "does an outside source cover it?". No step asked "does a builder or a critic need this principle, and will it reach them by default?". A principle that Butterick or Apple covers (caps tracking, weight floor, optical size) passed the "outside source covers it" test, so the house did not write it. But no file loads Butterick or Apple for the builder, and impeccable loads only with design mode on.

Result, from #205: "`docs/research/text-presentation.md` (#123) holds about 20 conditioned principles (B1.1–B6); `references/text-presentation.md` carries 2 (tint, links)" (`notes-coverage.md:342`). #206 gives the same cause: "#123's bound note (`:3`) put the rest out of the gate because they cannot fail a candidate; nothing then carried them into a reference a builder reads" (`docs/research/rule-interactions.md:78`).

- Gaps that C7 explains: N4 (rendering part; B5.2 in research only, `notes-coverage.md:130-131`) and N19b (pieces in `house-audit-method.md:71`, `text-presentation.md` B2.4, B5.2, B5.3, not carried; `notes-coverage.md:329-330`). Partial notes it explains: N1c, N1d (letter spacing), N1e (opacity, steps), N1i, N3b, N14, N16 (all "research only" in `notes-coverage.md`).

### C8. The question that #104 got, or the founder's words on map #96, framed the task narrowly — PARTLY CONFIRMED (the ticket text narrowed it; the founder's words did not)

- The founder's words on 13 Oct, as #96 records them: "is our research comprehensive for creating good website designs, or are there gaps that need filling?" (`gh issue view 96`, Notes, first bullet). The words are broad. They set no level, but they do not ask for subjects.
- Map #202 describes his ask as "a very thorough job of finding every concept worth applying to web design" (`gh issue view 202`, Notes). I found no record of that wording from 13 Oct. It is a later restatement. I do not use it as evidence of the 13 Oct ask.
- The narrowing came from the ticket text that the session wrote:
  - It listed the areas (C1).
  - It gave no definition of "covered" and no stopping test (C3, C11).
  - It set the output as a ranked list: "Rank each gap by how often it would affect a site the founder builds" (`gh issue view 104` body). A ranked list for a ruling round favours a few large gaps over many small decisions.
  - Map #96's destination was a ruling: "Every gap the coverage audit finds … has a ruling too: fill it (as research) or accept it" (`gh issue view 96`, Destination). The audit fed a six-question round (#101), not a ledger.
  - The coverage question was a side question on a map about a correspondence-style critic check (#96 title and Destination). It got one ticket among five, filed in 15 minutes and closed in 31 (Finding 1).
- Gaps that C8 explains: all six, through C1, C2 and C3. C8 is the root that let C1–C3 happen.

## Finding 3. Causes that the evidence adds

### C9. The first two signs of a frame failure were patched topic by topic; the method was not re-tested — CONFIRMED

- On 13 Oct the founder asked two questions that the frame did not hold: borders ("when to remove one, when to replace it with something else … 'and other things in a similar design category'", `gh issue view 117` body) and text colour ("what to do with, and how to present, text is part of all this", `gh issue view 123` body).
- Each ticket body names the frame's fault: #117 "has no row for the visual attributes every component is drawn with"; #123 "covers type size and measure and colour contrast, but not how text is drawn".
- The session filed a topic ticket for each. It did not ask what other parts the frame missed by the same fault, and it did not re-open #104. The founder's 15 Oct notes are the third instance of the same fault. In method terms, a lead from the founder was a recall failure (a known item that the search did not find), and it was treated as a new topic.
- Gaps that C9 explains: all six.

### C10. The source set had no family that names single decisions, and no current web-platform family — CONFIRMED

- #104's web sources were standards, studies and articles: W3C, web.dev Vitals and Baseline, NN/g, Baymard, Butterick "point-size", Apple HIG Dark Mode (`design-coverage-gaps.md:251`). These answer "what is the limit" or "what did a study find". They do not list the decisions a designer makes.
- #207 found that only craft books (Refactoring UI, Butterick, Bringhurst) and some design-system pages (Apple HIG, Atlassian border and elevation) name G3 decisions (`topic-taxonomies.md:244`). #104 did not open the craft books (`design-coverage-gaps.md:253`).
- Era-bound web-platform features are in no craft book. #207's test found the problem of a lone last word (Butterick) but not the CSS fix `text-wrap: pretty`/`balance` (2023–24): "the full run therefore needs one current web-platform source … as its own family" (`topic-taxonomies.md:239-240`). The same holds for `font-size-adjust` (Baseline 2024, `notes-coverage.md:332`) and the Tailwind-style resting ring (2020 on, `notes-coverage.md:145`).
- A side fact: the house's own code already uses `text-wrap: balance` on its review page headings (`plugin/review-page/index.html:22`, added in `9d523b1` on 13 Oct). A builder agent knows the practice from training. No rule records it, so no critic checks it and no audit counts it.
- Gaps that C10 explains: N1g, N5, N19b (the CSS tools); in part N4 (no source that discusses the choice of a variable font was read before #205). N2a: #205 and #207 found no design system that rules on page-section bands (`notes-coverage.md:87`). The source frame also needs landing-page and marketing-page sources for section-level decisions.

### C11. The audit had no completeness test and no stopping rule — CONFIRMED (by absence)

- #104's note has no statement of how it knew the frame was complete. Its Bound lists what it read and what it did not read (`design-coverage-gaps.md:245-253`). It has no saturation count, no estimate of missing rows, and no test against known items.
- #207 lists the checks that other fields use: saturation (Guest et al. 2020), a Chao2 lower bound, and recall of a held-out known-item set (Cochrane §4.4.11) (`topic-taxonomies.md:170-184`). #104 used none of them.
- #207's small test shows what a recall check would have shown: surfaces reached only 62% of the Chao2 lower bound with four sources (`topic-taxonomies.md:228`). A single check of that kind marks an area as unsaturated.
- Gaps that C11 explains: all six.

### C12. The condition list copied into every research ticket did not name the typeface, and the rule form had no slot for a measured input — CONFIRMED (for N19b, N4)

- Every research ticket on map #96 got the same condition list: "what it depends on (the element's function, the brand's tone, density, the treatments around it, light or dark ground)" (#117 and #123 bodies, §Conditions and conflicts; #121 body: "element function, brand tone, density, ground, surrounding treatments, device"). The typeface is not in the list. No ticket searched for conditions that depend on the face.
- #121's `applies-when` predicates "are function, zone, mode, ground, device, state and floats … So the house cannot say 'this 16 px is too small for this face'" (`docs/research/rule-interactions.md:79`).
- #103 cut `inputs` and `output` from the rule form ([`principle-interactions.md:3`](https://github.com/lucmoseley/design-vault/blob/88e3428e1/docs/research/principle-interactions.md#L3)). #206: "An interaction rule is mostly not a gate question: it sets a value from several inputs … So the builder-facing reference needs a form the gate form does not give" (`rule-interactions.md:240`).
- Thus a rule of the kind "size follows x-height" had no field to live in, and no ticket was told to look for one. N19 is the founder's own form of this point ("rules that characterise fonts and their knock-on effects", map #202 Notes).
- Gaps that C12 explains: N19b; N4 (axes as a face trait); partial notes N1b, N1d, N14 (#206 Part 1 rows 23, 24, 26, 29, 30).

## Finding 4. Cause-by-gap table

Key: **X** = the cause let this gap through (evidence in Finding 2 or 3). **(x)** = a contributing cause, weaker or indirect. **–** = not a cause for this gap. **R** = rejected for this gap with evidence.

| Gap (#205) | C1 author's areas | C2 G1 rows | C3 "mention = covered" | C4 Manta-reach ranking | C5 accepted without re-check | C6 unread impeccable files | C7 research not carried | C8 ticket framing | C9 patched, not re-tested | C10 no G3 / web-platform source | C11 no completeness test | C12 no face input |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **N1g** `text-wrap`, orphans | X (#123 list has no line breaking) | X | X (`craft-floor.md:12` "balanced headings" read, counted) | – | (x) | R (file read in full) | – (never researched) | (x) | X | X (CSS fix 2023–24 in no craft book) | X | – |
| **N2a** section grounds | X (#117 list: fills at component level only) | X (no surface or section row) | (x) (Layout "C: impeccable `layout`"; Manta zone rule) | (x) (Manta's zone rule went to Manta) | (x) | R (impeccable holds nothing on it) | – | (x) | X | X (no design system rules on bands) | X | – |
| **N2b** subtle gradients | X (#117 list: gradient only as scrim) | X | X (a ban counted as coverage: `design-coverage-gaps.md:207`) | – | (x) | R (impeccable holds only bans) | – | (x) | X | (x) (no source found even by #205) | X | – |
| **N4** variable fonts | X (#123 asked rendering "grades", not the choice) | X | X (`typeset.md:23` "variable-font settings" read, counted) | X (#123 B5.2 ranked "Low": Manta fonts lack `GRAD`) | (x) | R (file read in full) | X (B5.2, B5.3 stay in research) | (x) | X | (x) | X | (x) (axes are a face trait) |
| **N5** resting rings vs borders | X (#117 list: ring = focus only) | X (no surface row; #117 says so) | (x) | – | (x) | R (impeccable holds nothing on it) | – (focus ring carried; resting ring never researched) | (x) | X | X (Tailwind-era pattern, 2020 on) | X | – |
| **N19b** typeface traits | X (#123 list has no metrics) | X | X (`typeset.md:21` "tuned to the actual face" read, counted) | – | X (#101 Q4: type scale "one source per project") | R (file read in full) | X (pieces in `house-audit-method.md:71`, B2.4, B5.2, B5.3) | (x) | X | X (`font-size-adjust`, Baseline 2024) | X | X (no face input in any condition list or rule form) |

Count per cause (X only, six gaps): C1 6, C2 6, C3 4, C4 1, C5 1, C6 0 (rejected 6), C7 2, C8 0 direct (root of C1–C3), C9 6, C10 4, C11 6, C12 1.

The "partly" verdicts follow a different pattern. Of the 19 partial verdicts in `notes-coverage.md:384`:
- **Research only, not carried (C7):** N1c, N1d letter spacing, N1e opacity and steps, N1i, N3b, N14, N16 (caps rule).
- **impeccable only (C3):** N10, N12, N18, N7 (parts).
- **Ranked out or sent to Manta (C4):** N16 sentence case and N7 taste by audience (#101 Q6, accepted as gaps); N14 and N16 caps tracking ("Row 8 … is Manta's", [`text-presentation.md:3`](https://github.com/lucmoseley/design-vault/blob/88e3428e1/docs/research/text-presentation.md#L3)).
- **G1 frame, G3 question (C2):** N1f centred text, N1h block width, N3a destructive steps, N11 border alpha, N13 contrast ladder, N17 badge against icon. Each sits inside a "covered" subject row.

## Finding 5. Answer: the real reason

The six gaps did not slip through one hole. Three faults in #104 made the gaps invisible, and three later faults kept them invisible.

**Why #104 could not see them.**
1. The session that wrote #104 chose the areas, at subject level, before any research (C1, C2, C8).
2. The audit then marked a subject as covered when impeccable or Manta mentioned it, with no test for source, condition or delivery (C3).
3. The audit had no completeness test, and it read no source that names single decisions (C10, C11).

A subject frame plus "a mention is coverage" gives a "covered" label to almost any subject with a few lines in impeccable.

**Why later work did not find them.**
1. The founder's own questions on 13 Oct showed the frame's fault twice. Each time the session filed a topic ticket and left the method as it was (C9). The scope lists of those tickets repeated the fault one level down (C1).
2. #101's session accepted rows as "filled" from round-1 summaries, without a re-read (C5). The founder accepted every recommendation as a batch. The round offered no option to question the frame.
3. The rulings on what reaches a reference used two tests: "can it fail a candidate?" (#100, #103) and "does an outside source cover it?" (#119, #154). Neither test asked whether the builder or the critic would ever read the principle. Most of #123's conditioned principles were kept out by one test or the other and stayed in `docs/research/`, where no agent reads them (C7). The rule form lost the fields that a face-dependent rule needs, and the condition list never named the typeface (C12).

**Rejected.** C6 (unread impeccable files): the relevant impeccable files were read in full; the lines in them were the problem, not the reading. C4 at #104: the six gaps had no row to rank. C4 holds only at #117, #123 and #101 Q6, where ranking by Manta reach marked portable principles "Low" or "Manta's".

## Finding 6. Properties that a replacement method needs (adopted by #210)

The coverage ledger these properties define is `docs/coverage-ledger.json`, built in #215.

| # | Property | Stops | How a reader or a script checks it |
|---|---|---|---|
| P1 | The topic list comes from outside source trees, in at least three independent families: G3 craft books; design systems with G3 guidance; checklists and limits (WCAG 2.2, impeccable's rule list). Add a fourth family of **current web-platform docs** (MDN, web.dev CSS guides, Baseline), a fifth of **landing-page and marketing-page practice** for section-level decisions, and a sixth, **current practitioner writing** (2023 on). The question's author lists no areas. | C1, C10 | The ticket body names source families, not areas. Each row has at least one source citation from the extraction. |
| P2 | One row per decision: property × element × context (G3), as #207 B2 step 2 gives (`topic-taxonomies.md:181`). Subjects are only a grouping column. | C2 | No row label is a bare subject name. |
| P3 | A written test for "covered": sourced, conditioned, with a trade-off, **and carried into a file that a builder or a critic reads in a web round's configuration**, where impeccable loads (`plugin/skills/design-round/SKILL.md`, "A web-surface round runs impeccable at every stage"). So an impeccable line fails "covered" on source and condition, not on reach. #205's verdict words are a ready test (`notes-coverage.md:5-9`). These do not count as coverage: a line in impeccable alone; a project's value (Manta's); a ban alone (it says when a thing is wrong, not when it is right). | C3 | Each "covered" row cites a `Ref` file:line. A row that cites only impeccable, a project file or a ban is "partly" at best. |
| P4 | Completeness checks with a stopping rule: saturation (≤5% new rows per run of two sources), a Chao2 lower bound per area (stop at 90%), recall of a held-out known-item set (`topic-taxonomies.md:182-184`), and one held-out source coded blind. A session that has not seen the founder's notes codes the rows (`topic-taxonomies.md:197`). | C11 | The ledger states the four checks' results per area. |
| P5 | Every later lead from the founder is logged as a **known-item miss** of the method, and it starts a re-check of the source frame (which family would have named it?), not only a topic ticket. | C9 | A miss log with one line per lead and the family it exposed. |
| P6 | Inclusion and ranking are separate steps. Every decision enters the ledger first. Ranking by reach comes after, across all projects that the vault serves, not by one project's site. A portable principle found through a project's fault gives a vault rule **and** a project out-of-scope line, never only the project line. | C4 | No ledger row is absent because of rank. Each "Owner: <project>" row also names its vault rule, or states "no portable rule". |
| P7 | "Accepted as filled" needs a row-by-row trace: each ledger row names the file:line that fills it, and the ruling session reads those lines (not a summary). A ruling round shows the method's completeness numbers (P4) and offers one option that questions the frame. | C5, C8 | The resolution's Bound lists the fill files as read in full. |
| P8 | A carry-over rule for research: every conditioned principle in `docs/research/` gets one disposition — builder reference, critic gate question, project rules file, or "not carried" with a reason. "An outside source covers it" is not a disposition, unless the file that the agent loads points to that source. "It cannot fail a candidate" sends a principle to a builder reference, not to nowhere. | C7 | A script lists the principle ids in each research note (for example B1.1–B6) against the references' source lines, and prints each id that has no disposition. |
| P9 | The condition list in research tickets, and the rule form, include **the typeface's measured traits** (x-height, width, stroke weight, axes) and other continuous inputs. Whether the form for builder rules keeps `inputs` and `output` (#206 §3.3, `rule-interactions.md:236-265`) is #212's. | C12 | The ticket template and the rule form name a face input class. |
| P10 | The coverage question gets its own ticket budget at the depth it needs: #207 prices the full method at about 2–4 agent sessions plus about 30 minutes of the founder's time (`topic-taxonomies.md:186`). It does not run as one item among several in a shared half-hour window. | C8 | The ticket states its depth (G3) and its budget. |
| P11 | The ledger has a re-scan trigger for era-bound features: a new Baseline year, a new WCAG version, or a new major design-system release adds the web-platform family's new entries (for example `text-wrap` 2024, `font-size-adjust` 2024), and a yearly re-scan besides. | C10 | A dated re-scan line in the ledger's header. |

## Bound

**Read in full:** issues #203, #202 (bodies); #104 (body and resolution); #101 (body, all four round-1 comments, resolution); #96 (body); #117, #123, #121, #115 (bodies); #117, #123, #119, #121 (resolution comments); #174 (body); #183 (body, resolution, last round comment); #194 (body and all comments); `docs/research/notes-coverage.md`; `docs/research/design-coverage-gaps.md`; `docs/research/topic-taxonomies.md`; `plugin/skills/design-critique/references/text-presentation.md`.

**Read in part:** `docs/research/rule-interactions.md` (Part 1, Part 3, Bound); `docs/research/text-presentation.md` (lines 1–30, Part C table, Part D, Part E, B5, Part F); `docs/research/surface-styling.md` (grep for ring, gradient, section, band); `docs/research/adopt-or-build.md` (per-area table rows and the WRITE line, by grep); `docs/research/principle-interactions.md` (banner, line 3); #154 body (§The house method and the grep hits for tint, reference and #123); #103 comments (grep for the scope line); impeccable 4.5.0 `craft-floor.md:10-14`, `typeset.md:19-25` and a grep of `craft-floor.md` for gradient.

**From `git log`:** commit dates and file lists for `8e242c1`, `6cfa8d8`, `9d523b1`, and the history of both references and the #104, #117, #123 research notes; `git log -S` over `docs/research` and `plugin` for text-wrap, orphan, widow, variable font, x-height, font-size-adjust.

**Searched for an absence:** the wording "very thorough" or "every concept" in #96's comments and in the repo (no hit), and an issue search for "comprehensive" (hits #96 and #104 only). I did not search claude.ai chat history or session transcripts, so the 13 Oct wording may exist there.

**Not read:** the session transcripts that wrote #104, #101 and #117/#123 (so the "31 minutes" is the issue's open time, from `createdAt` to `closedAt`, not a measured work time; I also do not know if #104 ran in a subagent); #97, #98, #99, #100, #102, #118, #127, #130 resolutions; #192, #193, #195–#197; mantahostels files; #205's web sources (I use #205's verdicts as given and do not re-check its soundness findings).

**Judgement calls:** the X and (x) marks in the cause-by-gap table are my reading of the evidence. A second reader could move some (x) marks to X or to "–", mainly under C5 and C8, which act on all gaps through other causes. The rejection of C6 rests on #104's own Bound line, which says the two relevant impeccable files were read in full; I did not verify that the session read them, only that it says so.
