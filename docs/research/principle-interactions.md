# Design principles: how they interact and how each clash is resolved (design-vault#121)

⚠ **Bound 14 Oct 2026 (#103): §5's form is cut to nine fields, for gate questions only: `id`, `applies-when`, the check question, who answers it (script, code or look), `writes`, `yields-to`, `source` with its strength, `era` and `owner`. `function`, `inputs`, `output` and `trades-off` are dropped. Map #96's spec builds it.**

Question: Where the design principles from map #96 depend on context or pull against each other, how is each resolved, so that the house rules work as one system?

Abbreviations. Vault = the portable method (design-vault `plugin/`, `data/gallery.json`). Manta = lucmoseley/mantahostels (read-only here; out of write scope). Rule ids: B1-B53 and X1-X9 are Manta rules, G and R are vault rules, all from the census `docs/research/design-rules-census.md` §1-§4. K1-K27 are from `docs/research/manta-element-coverage.md` §4 (#118). C1-C10, B7.x and D1-D3 are from `docs/research/function-fit.md` (#127). F5 is `docs/research/adopt-or-build.md:141`-`:160` (#119). "#117 E<n>" is `docs/research/surface-styling.md` Part E (`:315`-`:331`). "#123 D<n>" is `docs/research/text-presentation.md` Part D (`:289`-`:301`). Era: T = timeless; E = era-bound, current as of the date given.

## Summary

**Key findings**

1. **Two orders, not one, make the rules a system.** A *dependency order* decides which choice comes first: function → role → treatment → value. A *precedence order* (#119 F5: law/WCAG → project rules file → domain evidence → expert craft ranges → impeccable craft → AI-look bans) decides which source wins inside one step. A later step never changes an earlier one: a value never changes a role, and a treatment never borrows another function's signifier (#127 B7.2). With both orders and the conditions that #117, #119, #123 and #127 already found, 36 of the 49 design conflicts in section 3 have one answer. 4 more have an answer in principle but need a number or wording from the founder (K1b, K2, K6, b2). 9 rest wholly on a founder ruling (11 rulings, R1-R11).
2. **Most conflicts are a missing condition, not a true clash.** Examples: eyebrow (K3a), left rule (K3b, K23), body size (K9), button shape (K10), spring (K1a, census b1) and the 2-link nav (K14). The fix is to write the condition (applies-when) on the rule. Nothing has to be deleted.
3. **The vault side holds 9 conflicts and all resolve without a ruling, except the scope half of b2 (R5).** Vault: census b1, b2, b6, b7, b9 and impeccable's internal i1-i4. The root vault fault is that the critic does not know which rule yields (section 5). Every K and C row is Manta-only and goes to lucmoseley/mantahostels as Out of scope.
4. **Walks of three Manta elements: the rules give one answer for about half the properties.**
   - Listing card (E45): 6 of 12.
   - Search bar (E19, E37, E112): 9 of 12.
   - Bottom sheet (E62): 6 of 12 now, 7 after mantahostels#2988.

   Every remaining property is a double-allowed answer (K6 rest shadow, K10 shape, numerals), a gap (sheet radius, scrim, placeholder token, nesting fallback, focus under a sheet) or a Manta fault the rules already decide (control edge 1.24:1, hero input with `outline:none` and no replacement, a compare "checkbox" that a keyboard cannot reach).
5. **Rule form.** A rule that names applies-when (function code plus context), the property it writes and what it yields to lets the critic detect a clash mechanically. A clash is two matching rules that write one property of one part with different outputs, where neither yields to the other. Section 5 gives the schema, three rewritten rules and a worked detection.

**Recommended answer to #121.** Adopt the dependency order function → role → treatment → value, with #119 F5 precedence inside each step. Write every house rule in the section 5 form, with its applies-when condition. Resolve the conflicts as in the section 3 table. Put the 11 rulings below to the founder. Send the Manta-only fixes to lucmoseley/mantahostels.

Confidence: 0.7 that this order and form remove the conflicts without a new clash.
- Most risk: the critic may not code element parts reliably from a render. #127 D2 calls a model's Q4/Q5 answers unverified.
- Would raise it: a seeded test in which the critic finds a static pill that copies a button and the K6/K27 shadow clash on one render.
- Would lower it: the founder ruling that one look must hold across functions (for example one pill for all, C1). The function-first order would then not decide shape.

**Founder rulings (plain questions)**

- R1. **White surface (C2).** Does white mean "you can tap this" or only "this is a card"? If it means "tap", the static white blocks need another container. These are the guide chips, quick facts, rooms table, sub-scores, review cards and location block.
- R2. **Hover (K27, #117 E1).** Does a hover change one thing (a shadow OR a border colour, as Atlassian does) or two (as Material does)? The live destination card changes two. The corpus listing card changes one.
- R3. **Shadow at rest (K6).** What is a "heavy" shadow (B46)? The hero search box rests under the popover shadow (0 8px 24px, 16%). The listing card rests under a 2px shadow at 6%.
- R4. **Button and chip shape (K10, C1, K18).** May the shape follow the function and the device? Pill for one standout action and for chips you can select. 8px for buttons in dense desktop rows. No pill on static facts. Or must it be one shape everywhere?
- R5. **Motion outside the user interface (K1b, K1c, census b2).** Do the "no spring" and 120/180 ms rules cover the marketing hero reveal and the "manta pop" on reviews? Or do they cover only interface transitions, so that a brand motion brief sets the rest?
- R6. **Scrims and photo text (#123 D8, K25).** May a dim layer or gradient go behind text on a hero photo or video, against "UI is flat" (B18)? Which one scrim colour does the site use: black at 40% (live) or ink at 45% (corpus)?
- R7. **404 tone (K16).** Is the 404 page a personality surface (sheet §6) or an error message that is never witty (§11)?
- R8. **Demand signals (K2).** May a dated, true fact show? An example is "this hostel was fully booked 3 days ahead on average last month". Or is any demand line banned?
- R9. **Paid partners (K20).** How must a paid partner look in results so that rank is never bought? A label, no special position, or no partner mark at all?
- R10. **Big-number tiles (K7).** May the rewards screen and the owner dashboard use big-number stat tiles, against impeccable's refusal?
- R11. **Exit interstitial (K22c).** May "Leave a review afterwards to earn rewards" stay in the 2.2 s exit screen? Sheet §13 says the handover carries no rewards pitch.

## 1. Dependency order and context factors

| Step | Question | Reads (context factors, in this order) | Decided by | Output |
|---|---|---|---|---|
| 1 Function | What does this part do? N, A, I, S, T, R (R-trust), C or D. | The part, not the component (#127 B7.1). The task priority of the page (#127 B3). The client brief or an inference, by the ask-or-infer rule (`docs/research/function-questions.md:233`-`:242`). | ARIA / M3 / HIG categories (#127 B7.1) | One code per part |
| 2 Role | Which signifier and which token role carry this function here? | Brand tone and zone energy (B1). Density and mode, Operate or Read (#119 table, `adopt-or-build.md:199`). | #127 B7.2 carriers and never-borrowed set; B3 prominence ladder | A role, for example primary action, control edge, link, status chip, card edge |
| 3 Treatment | Which property expresses the role: border, fill, shadow, shape, weight, motion? | Ground (sand, white, turquoise, ink, photo). Surrounding treatments (#117 E1-E4: neighbours, existing separators). Device and input (#117 E6; WCAG 2.5.7, 2.5.8). | WCAG (level 1), domain evidence (level 3), #117 Part E, #123 Part D | A treatment per property |
| 4 Value | Which number? | The project's one value system (#119 F5 kind 3) | The project rules file (level 2) | A token value |

If a later step and an earlier step disagree, the earlier step wins. Example: if the brand radius (value) makes a static chip look like a filter chip (role), then the chip takes another shape (#127 B7.2 row S).

## 2. Interaction map

"If X, then Z rather than Y" is the resolution.

| # | Principle (cite) | Reads | Trades off against | If X, then Z rather than Y | Resolution source | Era |
|---|---|---|---|---|---|---|
| P1 | Code function per part before beauty (#127 D1, D3) | part, task | Holistic beauty first (#127 B1.4) | If the critic likes a candidate, run the function walk on it first, rather than scoring it first | #127 B1.4 (Tractinsky, NN/g) | T |
| P2 | Same function, same look; different function, different look (#127 B4.1) | site-wide treatments | Brand consistency of one shape (C1) | If a static fact and a filter chip share a pill, give the static fact no edge and no fill, rather than the same pill | WCAG 3.2.4; GOV.UK Tag (#127 B7.2 row S) | T |
| P3 | One target per clickable surface (#127 B8.1) | nesting | Whole-card link convenience | If a card holds controls, either make one link (the name) plus separate controls, or make the whole card a link with no inner controls, rather than both | HTML `a` content model; NN/g (#127 B8.1) | T |
| P4 | Prominence follows task priority; one primary action (#127 B3.1; B12; X2) | page task | Brand expression (#127 B6.1) | If brand weight and a CTA compete, the CTA keeps the strongest colour, rather than the brand mark | Apple HIG, GOV.UK (#127 B3.1) | T |
| P5 | Warm = act, cool = read (B16) | function | Links are interactive and cool (#127 C, item 4) | If the part is N in running text, it takes cool colour plus underline, rather than warm | #127 C item 4; WCAG 1.4.1 | E (2026) |
| P6 | Never colour alone (B19; WCAG 1.4.1) | state, link | Clean flat style | If a link is in light-ground prose, underline it, rather than colour only (C4) | WCAG 1.4.1 G183 (#123 B3.1) | T |
| P7 | Control edge ≥3:1 when the edge is the only identifier (#117 B1.1) | function I/S, ground | Soft sand borders (B46 "borders first" in sand-border) | If an empty field or checkbox shows only by its edge, the edge takes ≥3:1, rather than sand-border 1.24:1 | WCAG 1.4.11 (level 1) | T |
| P8 | Separate a static card by border OR fill step, not shadow (#117 B2.1, E1, E2) | fill step ratio | Borders-first minimalism (B46) | If the fill step is under 1.1:1 (white on sand 1.08), keep a weak border, rather than drop it | #117 E2 (Carbon, Polaris) | E (2026) |
| P9 | Depth means "floats above" or "you can act" (#117 B2.1) | function C, floats? | B46 "shadow only on hover and popovers" | If the surface floats (sheet, sticky bar, menu), give it a shadow even at rest, rather than a border only | M3, Atlassian (#117 B2.1) | T (meaning); E (recipe) |
| P10 | One hover signal (#117 B2.3) | neighbours | Material's combined signal | **Not decided by a source**: Atlassian and Material disagree. Founder ruling R2 | none; R2 | E (2026) |
| P11 | Radius by density and pointer (#117 E6; Apple WWDC25-356) | device, density | One-shape brand (B45, built pill `.btn`) | If touch or one standout action or a selectable chip, use a capsule; if dense desktop rows, use 8px, rather than one shape everywhere | Apple (level 4) as condition; value at level 2; R4 | E (2025-) |
| P12 | Nested radius concentric: inner = max(R − p, fallback) (#117 E5) | padding | Uniform token use | If R − p ≤ 0, use the fallback, rather than repeat the outer radius | Apple (#117 B3.2) | T |
| P13 | Checkbox square-ish, radio round, whatever the brand radius (#117 E7) | function S | Brand radius factor | If the brand radius changes, a checkbox keeps a small radius on the scale, rather than an off-scale 5px | Radix (#117 B3.5) | T |
| P14 | A tint as "selected" needs a second ≥3:1 cue (#117 E8, B5.2) | state | Quiet working area (B10) | If a wash marks selected, add a check, weight or a 3:1 edge, rather than the wash alone | WCAG 1.4.11 | T |
| P15 | Focus ring visible, two-colour or per ground (#117 E9; B47) | ground | `outline:none` for a clean field | If more than one ground, the ring is lagoon on light and ink on turquoise, rather than one colour; if a field has a border, add a ring or a thicker border, rather than only a recoloured 1.5px border | WCAG 2.4.7 / 2.4.11; GOV.UK; mantahostels#3459 ruling 2 | T |
| P16 | Focus not obscured by sticky bars (#117 E10) | layout | Sticky compare bar (E54), sheet (E62) | If a bar is sticky, set `scroll-padding`, rather than let it cover focus | WCAG 2.4.11 (AA) | T |
| P17 | One stroke band; the focus ring alone is thicker (#117 E11; B44) | text weight | Icon set default 2px | If borders are 1-1.5px and icons 1.75px, keep both in one band, and use 2px+ only for focus | Apple, Material | T |
| P18 | One scrim token (#117 E12, B6.1) | modal | Drift (K25) | **Value not decided**: M3 32%, Carbon 60%, both in range; Manta must pick one. R6 | #117 B6.1 range; R6 | E |
| P19 | Glass only on a floating functional layer (#117 E13) | layer | Decorative glass on cards | If content card, solid fill, rather than blur | #117 B6.3 | E (2025-) |
| P20 | On ink, raise elevation by lighter surface, not stronger shadow (#117 E14, B2.4) | ground | Light-ground shadow recipe | If night ground, lighten the surface | M3 dark theme | T |
| P21 | Tint text toward the dominant hue only (#123 D1) | palette | Neutral greys | If a new colour sits near the text hue, check ΔE00 against ink and text-muted (B26), rather than add it | #123 B1.1 | E (2026) |
| P22 | Tinted dark text forces underlined links (#123 D2) | link | Colour-only links (C4) | If link vs body ink < 3:1 (lagoon-text vs ink 2.22), underline, rather than colour | WCAG 1.4.1 | T |
| P23 | Every text-holding fill has measured primary and secondary text (#123 D3; B21) | ground | "Looks fine" | If a new fill holds text, measure both text colours before use | WCAG 1.4.3 | T |
| P24 | Working-area emphasis by weight, size, position, not colour (#123 D4; B10, B12) | zone | Coloured emphasis | If working area, use weight and space, rather than a new colour | #123 D4 from B10/B12 | E (2026) |
| P25 | Caps only for short labels, tracked 5-12% (#123 D5; B30) | case | Eyebrow ban | If an uppercase label stays, track it 5-12%, rather than 2% | Butterick (#123 B2.3) | T |
| P26 | Tabular numerals for compared numbers (#123 D6) | typeface | Display face for scores (Quicksand has no `tnum`) | If numbers are compared down a column, use tabular digits (Nunito Sans) or a fixed-width chip, rather than proportional Quicksand in a free-width chip | Butterick (#123 B2.4) | T |
| P27 | On ink, raise muted-night lightness before weight (#123 D7) | ground | Weight bump | If small secondary text on ink is weak (4.51:1, Lc −40.9), lighten the colour, rather than bolden | #123 B4.2, B5.3 | T |
| P28 | Coral label ≥19px/700 sets the label ceiling (#123 D9; B29) | view | Other labels' emphasis | If a coral CTA is on the view, no other label exceeds it in weight × size | WCAG large text (B29) | T |
| P29 | Body size by mode (#119 table) | mode | impeccable 16px floor; Manta 14-15.5 (K9) | If a Read page (guide, hostel), 16px+; if a dense results list (Operate), 14-15px for secondary lines, rather than one size | Butterick, Carbon (#119) | E (2026) |
| P30 | Input text ≥16px on touch | device | 15.5px body token | If a text field is on a touch device, set its text at 16px, rather than 15.5px. iOS Safari zooms the page on focus under 16px | WebKit behaviour; unverified here | E (2026) |
| P31 | UI motion short, standard ease, no overshoot (B48; #119 "Manta for UI transitions") | motion kind | Spring for real drag (#119 table; mantahostels#2988); vault R34/R35 springs for brand landings | If a UI transition, 120/180 ms standard ease; if a drag the user releases, a critically damped spring with no overshoot; if brand motion, the motion brief (design-round:161), rather than one rule for all | #119 table; M3 motion (level 4); vault `design-round/SKILL.md:161` | T (physics) / E (tokens) |
| P32 | Respect reduced motion (WCAG 2.3.3 AAA; `prefers-reduced-motion`) | user setting | Brand motion | If the user asks for reduced motion, cross-fade or snap, rather than move | WCAG; X7 | T |
| P33 | Pause control for loops (WCAG 2.2.2) | loop length | impeccable "stop offscreen" | If motion loops over 5 s, a pause control, rather than only offscreen stop | WCAG (level A) (#119 table) | T |
| P34 | Drag has a single-pointer path (WCAG 2.5.7 AA) | input | Gesture-only sheets | If a sheet resizes by drag, a tap on the handle (or a List/Map button) does the same, rather than drag only | https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html (read 13 Oct 2026) | T |
| P35 | Target 44px for Manta; 24px WCAG floor (#119 table) | device | Dense desktop rows | If touch, 44px; if desktop pointer, ≥24px or the spacing exception, rather than 44 everywhere | WCAG 2.5.8; #119 | E (2026) |
| P36 | Visible nav for ≤4 items on mobile (#119 table; NN/g) | item count | Space for the mark (C6) | If the nav has ≤4 links, show them, rather than a Menu | NN/g (level 3) | E (2026) |
| P37 | Filters visible for search-and-compare; split list and map (#119 table; Baymard) | task | impeccable ≤4 options | If accommodation results, show filters and promote the important ones, rather than cap at 4 | Baymard (level 3) | E (2026) |
| P38 | No urgency theatre (B49); proof stays plain (#127 B7.2 row R) | content | Conversion lens "risk-reversal" (DC:40) and demand signals (K2) | If a claim is true, dated and sourced, show it plain, with no countdown and no scarcity styling, rather than ban all facts or style them as urgency | FTC dark patterns (#104 W8). Wording: R8 | T |
| P39 | Ranking never bought; paid marked (PRODUCT.md) | content | Partner badge (K20) | If paid, the mark is a plain label and the position is not changed. The form: R9 | FTC endorsement guidance: not held in the vault (#118 K20) | E |
| P40 | Eyebrow / left rule only when they carry information (#119 table; GOV.UK caption, inset text) | content | impeccable absolute ban (level 6) | If the label names a section, place or category, keep it, recorded with its condition in Manta's file, rather than ban or allow freely | #119 table (level 3 over level 6) | E (2026) |
| P41 | Decoration never takes a signifier; the brand layer is free (#127 B6.3) | function D | Brand expression | If brand art enters the working area, haze, low detail, type priority, text-muted ≥4.5:1 over it (mantahostels#3057, #3058), rather than full art | Founder principles #3057 (proposed; not yet in the sheet) | E (2026) |
| P42 | High-stakes moments use conventional signifiers (#127 D1 Q9) | stakes | Brand experiments | If booking, handover or error, use conventional controls and copy, rather than playful ones | Norman 2002; M3 Expressive (#127 B6.2) | T |

## 3. Every conflict resolved

"Side": V = vault (the method; in write scope); M = Manta-only (owner lucmoseley/mantahostels; out of write scope). "By": S = a named source, O = the dependency order, R = a founder ruling.

| Id | Conflict (short) | Side | Resolution | By |
|---|---|---|---|---|
| K1a | Bottom-sheet drag settle vs B48 "no spring" | M | Critically damped spring, no overshoot, for a drag the user releases. B48 stays for UI transitions. A clause goes in sheet §10. Owner mantahostels#2988 | S (#119 table; M3 motion) |
| K1b | Review "manta pop" (E74) vs B48 | M | It is status feedback on a rating control, so it is UI motion: 180 ms, standard ease, scale ≤ press 0.97 equivalent, no overshoot. A bigger "pop" needs R5 | O (function T first) + R5 |
| K1c | Hero scroll reveal (E15) vs B48 | M | Marketing-zone brand motion. Scope: R5 | R5 |
| K2 | Demand signals vs B49 | M | A true, dated, sourced fact in plain text passes B49. "High interest for your dates" fails (no source, an urgency cue). Exact wording: R8 | S (FTC via #104 W8) + R8 |
| K3a | Eyebrow vs impeccable ban | M (+V: vault must let a project override with its condition) | Allowed when it names a section, place or category. Manta records the condition. C9: it must not use the CTA type token | S (#119 table; GOV.UK caption) + O (C9: role step) |
| K3b | Coloured left rule (X1) vs impeccable | M | Allowed on the testimonial with its condition (one per view, not on review cards). Record the width | S (GOV.UK inset text, #119 table) |
| K4 | Background art in the working area vs B1 | M | The founder's #3057 principles plus #3058's 4.5:1 bar, judged behind the real results layout (X9). Write them into the sheet | Founder principles #3057 |
| K5a | AvailChip "yes" in a turquoise tint (C8) | M | Status takes the success token with its text partner; turquoise stays brand | S (GOV.UK Tag; sheet §3 own rule) + O |
| K5b | Comparison "best" tint in turquoise | M | Same as K5a. Also B51 bans "best" strings; the cue is a check icon plus a label, not a brand tint | O + B51 |
| K5c | Ink toast, tooltip and count pill | M | Not a fault: an inverse surface for a transient message is a platform convention (#127 C, "Not a fault"). Add them to the §2 night-context list | S (Material snackbar; from knowledge in #127) |
| K6 | Rest shadow (card, hero search) vs B46 "heavy" | M | Floating or interactive → a shadow is allowed (P9). Static → none. "Heavy" must get a number: R3 | S (#117 B2.1) + R3 |
| K7 | Stat tiles vs impeccable hero-metric refusal | M | Level 6 is a default that a brief can earn back (F5). Not decided by a source: R10 | R10 |
| K8 | Uppercase headings and title-case h1 vs B30 | M | B30 wins (level 2, own rule). Fix the corpus labels to sentence case or reclassify them as filter labels | O (project rule; no clash with a higher level) |
| K9 | 14px body vs 16px | M | By mode: 16px+ on Read pages, 14-15px on dense results (P29). Inputs on touch ≥16px (P30) | S (#119 table) |
| K10 | Pill vs 8px control | M | Shape by function and device (P11). Which way is R4 | S (Apple) + R4 |
| K11 | Outline button on ink | M | White 1.5px outline and white label on ink (13.12:1), the night pattern B6 by analogy. Not stated by a source; it is the B6 inference | O (B6 on the role step) |
| K12 | Score without word; Top Rated pill | M | B36 and B51 win; fix the corpus | O (project rule) |
| K13 | Control edges 1.24:1; border-only focus; checkbox radius 5 | M | Edge ≥3:1 (P7, level 1). Focus: ring or thicker border (P15). Checkbox: a value on the scale (6 = chip) (P13) | S (WCAG 1.4.11, 2.4.7; GOV.UK; Radix) |
| K14 | Two-link nav hidden on mobile | M | Show both links (P36). The mark's room is a value choice that yields to function | S (NN/g level 3 over a level-2 rule that gives no reason) |
| K15 | Controls on photos; 220 ms gallery; carousel | M | Controls on photos take a solid backing that meets 3:1 against the real pixels (#117 B6.2). No auto-rotate (NN/g). Swipe has a button path (2.5.7). 220 ms → 180 ms (B48 token) | S (WCAG 1.4.11, 2.5.7; NN/g) + O |
| K16 | 404 tone | M | R7 | R7 |
| K17 | Illustration as filler | M | An image earns its place by carrying information or a deliberate feeling (#104 W6). Not a clash. The hypothesis in sheet §14 needs a test | S (#104 W6) |
| K18 | Static chips look like filter chips | M | Static facts lose edge and fill (plain text with a separator, or an icon plus a label) (P2) | S (GOV.UK Tag; WCAG 3.2.4) |
| K19 | Results layout vs Baymard | M | Split list and map; horizontal filter bar for important filters (P37) | S (Baymard level 3) |
| K20 | Paid partners vs merit | M | R9 | R9 |
| K21a | "Book" deep-link vs B25 | M | B25 wins: the label says where it goes ("Check dates on {hostel site}") | O (project rule; honest label, P42) |
| K21b | Greyed full hostels | M | A full row is content. Text keeps 4.5:1 and a "Full for these dates" label (B19, X3) | S (WCAG 1.4.3, 1.4.1) |
| K22a | Modal interstitial vs impeccable | M | A handover that leaves the site is a real need to warn (sheet §12a). Keep it; not a decoration modal | O (function A, high stakes) |
| K22b | 2.2 s auto-redirect vs WCAG 2.2.1 | M | An auto-redirect is a time limit. Give a "Go now" and a "Stay" control. The 20-hour, essential and real-time exceptions do not fit; the user must be able to turn off, adjust or extend it | S (WCAG 2.2.1, level A; from knowledge, not re-read) |
| K22c | Review-invite copy vs sheet §13 | M | R11 | R11 |
| K23 | Review card left accent | M | The left rule belongs to the testimonial only (K3b condition). Review cards take none | O (P2: different function, different look) |
| K24 | Sticky bars and focus | M | `scroll-padding` (P16) | S (WCAG 2.4.11) |
| K25 | Scrim drift | M | One token (P18); which value is R6 | R6 |
| K26 | Stale version pointers | M | A drift fault, not a design clash. Check by the census §7(c) proposal (one home per rule) | O (no design question) |
| K27 | Hover with two signals | M | R2 | R2 |
| b1 | Spring (vault R34/R35/G3) vs Manta "no spring" | V + M | Words only: a critically damped spring has no overshoot. B48 should ban overshoot and bounce, not the spring model. The vault keeps its springs for brand landings (design-round:161 scope) | S (physics; #119 table) |
| b2 | Motion tokens with no UI scope in the prefill | M (prefill) + V (critic must read the scope) | The tokens apply to UI motion only (design-process.md:68). The prefill line takes the same scope. The vault's critic applies brief length to brand motion | O (function: UI vs D) + R5 for scope |
| b3 | Eyebrows | = K3a | | |
| b4 | Left rule | = K3b | | |
| b5 | Grey secondary on ink vs impeccable "never gray" | M (weak) | muted-night is tinted (#8f999e, a cool grey near the ink hue) and meets 4.51:1. Raise its lightness (P27). No breach of intent | S (#123 B1.3, D7) |
| b6 | Conversion lens "risk-reversal" vs Manta urgency ban | V | Give the vault's conversion lens a yields-to: a project's honesty or urgency rule wins (level 2 over level 5). design-critique §3 states it, but the lens does not see the copy section. Fix: the lens reads the project's copy bans | O (precedence) |
| b7 | One ban at two strengths (DNA "defaults" vs Manta "reject on sight") | V | Not a clash: the project copy is stricter and wins for that project (level 2). The vault must say that the DNA never relaxes a project's stricter copy | O (precedence) |
| b8 | Tool roster drift | V | Tool rule, not design; the vault accepts it (census §7(b)8) | none needed |
| b9 | impeccable ease-out vs G3 for brand motion | V | G3 applies to brand motion; impeccable ease-out applies to UI. The critic must receive the motion kind (UI or brand) as an input | O (function: UI vs D) |
| c1-c4 | Version, DNA list, mmm-infra length, X1-X3 drift | M, V (c2) | Drift faults. One home per rule; others point to it (census §7(c)) | not a design clash |
| i1 | impeccable measure 45-75 vs 65-75 | V | Butterick 45-90 characters (level 4) holds both. Read pages target 60-75; dense UI may go shorter | S (Butterick) |
| i2 | impeccable colorize vs quieter, on tint and opacity | V | The function decides: colour for T and N signals only, quieter for C and D (P24) | O |
| i3 | impeccable detector's size-only hierarchy | V | Hierarchy by several cues (#123 B2.1); the detector is a hint, not a gate | S (#123 B2.1) |
| i4 | "One step more weight on dark" vs irradiation | V | On ink, raise lightness first (P27); add weight only on display sizes | S (#123 D7) |
| C1 | One pill for button, chip, fact | M | = K10 + K18: R4 | R4 |
| C2 | White = tappable vs static white blocks | M | R1 | R1 |
| C3 | Controls nested in a card | M | P3: two allowed shapes; Manta picks one (a value-level choice, not a principle) | S (#127 B8.1) |
| C4 | Links by colour only | M | Underline in prose (P6, P22) | S (WCAG 1.4.1) |
| C5 | Proof and urgency looks | M | = K2, K12, K20 | |
| C6 | Two-link nav hidden | = K14 | | |
| C7 | Status in the link colour | M | Status takes its semantic token; lagoon-text stays for links (P2) | O + S (GOV.UK Tag) |
| C8 | Status in turquoise | = K5a | | |
| C9 | Eyebrow in the CTA type token | M | A label must not exceed the CTA (P28). Use the label token, tracked 5-12% | O (role) + S (#123 D9) |
| C10 | Decoration in the working area | = K4 | | |

Count: 49 design conflicts after merging duplicates (K26, c1-c4 and b8 are drift or tool rules, not design, and are not counted). 36 are resolved by a source or by the order. 4 are resolved in principle and need a number or wording (K1b, K2, K6, b2). 9 rest wholly on a ruling (K1c, K7, K10/C1, K16, K20, K22c, K25, K27, C2). The rulings are R1-R11.

## 4. Walks

### 4.1 Listing card (E45, corpus `HostelCard.jsx`; `ui_kits/app/SearchResults.jsx:109`-`:160`; mobile `ui_kits/app/MobileSearch.jsx:4`-`:41`)

Parts and function codes:
- Card: C. Whole-card target: unknown. It is a `div` with `onMouseEnter`, with no `href` and no `onClick` (SearchResults.jsx:111).
- Photo: R (evidence, B43).
- Dots: T (position) or D. They are spans, not buttons.
- Name: R. Score chip, word and count: R-trust.
- Facts and flavour: R. Price: R.
- Amenity icons: R.
- Compare: S.
- "View beds": N. It goes to the detail page, but it is styled as a button (ARIA: a link takes the visitor somewhere, #127 B7.1).

| Property | Rules applied (in order) | One answer? | Finding |
|---|---|---|---|
| Role | P1, P3, P4 | **No** | Two parts navigate to the same place (an unclear card target and "View beds"), and S sits inside. P3 allows (a) the name as the link plus separate controls or (b) the whole card as the link with no inner controls. Manta-only choice (C3) |
| Border | P8 (white on sand 1.08 < 1.1 → keep a weak border), P7 does not apply (a card is not a control edge) | **Yes** | 1px sand-border (1.24 on white, 1.15 on sand) is right as a weak role |
| Shadow | P9 (interactive → allowed), B46 ("heavy" undefined), P10 (one hover signal) | **No** | Rest 0 1px 2px 6%; hover 0 4px 14px 10%. Allowed if the card is a link, and not allowed if it is not. K6 → R3; K27 → R2. The live `.dest-card` uses border plus shadow; the corpus card uses shadow only. Two treatments for one function: a P2 fault whatever R2 says |
| Radius | P12 (photo flush at outer 12; button inside 14-18px padding → R − p < 0 → fallback 8), P11, P13 | **No** | Card 12 and button 8 follow. Checkbox 5px is off the B45 scale (K13). "View beds" 8px here vs live `.btn` pill: K10 → R4. On stacked mobile (touch), P11 suggests a capsule; on desktop rows, 8px |
| Fill | P8, C2 | **Depends on R1** | White is right if white means "card", or if the card is tappable. Score chip turquoise fill with ink text: B24 |
| Text colour | P23 | **Yes** | Name and price ink on white 13.12:1. Count, flavour, "Dorms from" and "/ night" in text-muted 5.52:1. Chip ink on turquoise 5.73:1. All pass 1.4.3 |
| Type | P26, P28, P29 | **No (numerals)** | Score and price are Quicksand 700 with no `tnum`. The chip is min-width 32 but grows (15px digits + 18px padding > 32). B39 wants a score column, so P26 asks tabular digits: R4 does not cover this; Manta-only value choice (Nunito Sans digits or a fixed chip width). Name 17/600 and price 17/700 are the same size; the order of task priority (score before price, B39) is carried by position, which is allowed (P24). Secondary 11-13px in an Operate list: P29 sets 14-15 for secondary lines, so 11px "Dorms from" and "/ night" are below the mode range. Manta-only (K9) |
| Spacing | none found that binds | **Gap** | The census holds no spacing-scale rule that reaches this card (#118 §2.6 lists spacing coverage; not walked further). Proximity is consistent (gaps 4/8/16) |
| States | P14, P15, P16 | **Yes (rules decide), Manta fails** | Compare is a `label` with `onClick` on spans, with no `input` (SearchResults.jsx:144-151). A keyboard cannot reach it and it has no role → WCAG 2.1.1 and 4.1.2 fail. Disabled state by opacity 0.4 plus a `title` tooltip only: the reason does not show on touch. "View beds" sets no focus style; the browser default shows, but B47 asks lagoon (live `.btn:focus-visible`, globals.css:563, is not used by the corpus) |
| Motion | P31 | **Yes** | Box-shadow 180 ms; SearchResults uses the default ease, not `--ease-standard` (SearchResults.jsx:115). Token drift, Manta-only |
| Touch target | P35 | **Yes (rules decide), Manta partly fails** | Stacked: the button has min-height 44 (pass). The 20px compare box: the label row is about 20px high (inferred; not measured in a browser) → under 44. Desktop: the 16px box, if the label is the hit area, is about 18-20px → under the 24px WCAG floor unless the spacing exception holds. Not measured |
| Contrast (non-text) | P7, P14 | **Yes (rules decide), Manta fails** | Unchecked compare edge sand-border 1.24:1 on white → 1.4.11 fail (the edge is the only identifier). Checked lagoon fill 3.65:1 passes. Amenity icons lagoon 3.65:1 pass. Photo dots: white and 55% white with a 2px ink halo. On the placeholder they are 1.24:1 and 1.13:1. On real photos: unknown. If the dots tell the visitor which photo shows (T), 1.4.11 needs 3:1; if D, nothing applies. The function of the dots must be decided first (step 1) |

Result: 6 of 12 properties get one answer from the rules (border, text colour, motion, and the rule side of states, touch target and contrast, where the rules decide but the corpus fails them). Fill depends on R1. Contradictions: shadow (K6, K27), shape (K10), numerals (P26 vs the display face), target structure (C3). Gaps: spacing. Faults the rules decide: compare not reachable by keyboard, edge 1.24:1, small secondary type, no lagoon focus.

### 4.2 Search bar (E19 hero box, `ui_kits/marketing/Homepage.jsx:28`-`:41`; E37 and E112 `components/forms/Input.jsx:3`-`:27`; mobile summary field `ui_kits/app/MobileSearch.jsx:66`-`:67`)

Function: I (where to) plus A (Search). On the home page this is the primary task (Baymard via #104 W7; P4). The hero box is C, and its white fill is the input's identifier on the turquoise ground.

| Property | Rules applied | One answer? | Finding |
|---|---|---|---|
| Role | P4, B25 | **Yes** | The coral Search is the one coral object on the view (B25 names hero search). Correct |
| Border / boundary | P7, #127 B7.2 row I | **Yes (rules decide), Manta partly fails** | Hero: no border; white box on turquoise 2.29:1. WCAG 1.4.11 does not require a visible boundary for a field (Understanding 1.4.11; from knowledge, not re-read), so level 1 passes. #127 B7.2 (house synthesis) asks for a ≥3:1 edge or fill: white vs turquoise fails it, and the popover shadow does the work. Working-area Input: 1.5px sand-border 1.24:1 → 1.4.11 fail (K13). One answer: an edge ≥3:1 (for example #7C8E8C, 3.44 on white, 3.19 on sand, #117) |
| Shadow | P9, B46 | **No** | Hero box rests under `--shadow-popover`. The box is interactive, so P9 allows depth. B46 forbids a "heavy" rest shadow. The rules allow both: R3. Alternative without shadow: a 1.5px ink edge on turquoise (5.73:1) |
| Radius | P11, P12 | **No** | Box 8, inner button 8 at 8px padding → P12 gives max(0, fallback); the fallback is not defined (a gap). Pill is also allowed for a standout touch action (P11). R4 |
| Fill | C2, P23 | **Yes** | White box is interactive → consistent with "white = tappable". Mobile summary field (MobileSearch.jsx:66): sand-page fill with a 1px sand-border. If it opens the search, it is a tappable part that is not white → C2 in reverse (R1). Whether it is tappable: unknown (the kit gives no handler) |
| Text colour | P23 | **Gap** | Value ink on white 13.12:1. Placeholder: no token (#123). It falls to the browser default; Chrome's is about #757575 (4.61:1), but this is unknown and was not measured in a browser. A placeholder token is needed |
| Label | P1, NN/g persistent labels (#119 rule 31) | **Yes** | A single search field next to a "Search" button meets WCAG 3.3.2 by technique G167 (adjacent button labels the field; from knowledge, not re-read). It still needs an accessible name (`aria-label` or a hidden label); the kit gives none. NN/g's persistent-label finding is about multi-field forms, so it does not force a visible label here |
| Type | P29, P30, P28 | **Yes (rules decide), Manta fails** | Input text `--text-body` 15.5px → on iOS a focus zoom (P30; unverified here). Set 16px on touch. Button 19/700 white on coral 3.05:1 passes as large text (B29). Hover #e64a28 3.91:1 and active #cc3f1f 4.89:1 pass |
| States | P15, B47 | **Yes (rules decide), Manta fails** | Hero input: `outline:none` and the box has no focus style → B47 ("never removed without a replacement") and WCAG 2.4.7 fail. Input.jsx: focus = border recoloured to lagoon (2.94:1 against the rest state, 3.65:1 on white) → passes 2.4.7, fails 2.4.13 AAA, and P15 asks for a ring or a thicker border. A ring drawn outside the box onto turquoise must be ink (5.73:1; lagoon is 1.59:1) → mantahostels#3459 ruling 2 gives one answer. Error: danger border plus 12px danger text (passes B19 by the text) |
| Motion | P31 | **Yes** | Border colour 120 ms, standard ease |
| Touch target | P35 | **Yes (probably passes)** | Hero input: 10px padding + 15.5 × 1.6 line ≈ 45px (computed, not measured). Search button: about 43-45px (computed). Mobile filter button 44 × 44 and summary min-height 44 pass |
| Contrast (non-text) | P7, P14 | **Yes** | Mobile filter icon lagoon-text 5.90:1 passes. Selected sort chip (MobileSearch.jsx:73): 8% lagoon wash plus a lagoon edge 3.65:1 plus lagoon-text 5.37:1 on the wash → P14 met (an edge ≥3:1 as the second cue) |

Result: 9 of 12 properties get one answer. Contradictions: shadow (K6), radius (K10 plus no nesting fallback). Gaps: placeholder token, nesting fallback, accessible name. Faults the rules decide: hero focus removed, 1.24:1 edge, 15.5px input on touch.

### 4.3 Map bottom sheet (E62; planned only; mantahostels#2988 OPEN, "write the clause when map-view builds its bottom sheet", read 13 Oct 2026)

Parts: sheet surface C; drag handle A (it changes the sheet height); list rows = the stacked listing card (4.1 applies); map behind it, with markers (N/S) and map controls (A). A non-modal sheet beside a live map has no scrim. A modal sheet (for example filters) has one ("Modal bottom sheets are above a scrim while standard bottom sheets don't have a scrim": https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/BottomSheet.md, read 13 Oct 2026).

| Property | Rules applied | One answer? | Finding |
|---|---|---|---|
| Role | P1, P9 | **Yes** | A standard (non-modal) sheet for results; a modal sheet only for filters |
| Border | P9, P8 | **Yes** | Floats → shadow; a border is optional and weak |
| Shadow | P9 vs B46 | **Yes by source** | B46 names "hover and popovers" only; a sheet is not named. #117 B2.1 (floats above) decides: a shadow. B46 should name floating layers |
| Radius | P12, B45, #119 F5 kind 3 | **No: gap** | M3 gives the sheet the extra-large corner token (the BottomSheet doc above; 28dp per #117 B3.1). Manta's scale stops at 12 (B45). #119 F5 forbids importing one M3 value. Manta must name a sheet radius in its own scale (12 or a new top-corner token). Manta-only |
| Fill | C2 | **Depends on R1** | The sheet is a container, not tappable. White would contradict "white = tappable" unless R1 narrows it |
| Scrim | P18 | **No: R6** | None for the standard sheet. For the modal sheet: the one-token decision (black 40% → white sheet vs scrim 3.03:1 on sand; ink 45% → 2.76:1; both only decorative) |
| Handle (contrast) | P7 | **Yes (rules decide)** | If the handle is the only cue that the sheet moves, it is a graphical object that needs 3:1 (WCAG 1.4.11). Sand-border fails at 1.24:1; text-muted passes at 5.52:1 |
| Motion | P31, P32, b1 | **Yes after #2988** | Release: a critically damped spring from the release speed, with no overshoot (vault R34 has the same model). Under `prefers-reduced-motion`: snap or a short fade. B48 needs the gesture-settle clause (mantahostels#2988) |
| Input / device | P34 | **Yes** | WCAG 2.5.7 AA: "All functionality that uses a dragging movement for operation can be achieved by a single pointer without dragging" (W3C Understanding, read 13 Oct 2026). The handle is a button that steps the sheet through its heights (`aria-expanded`), and a "List / Map" toggle is a second path |
| Focus | P16 | **No: gap** | WCAG 2.4.11: a half-open sheet can cover a focused map marker. `scroll-padding` does not solve this for a map. No rule found. The likely shape: move the map so the focused marker shows, or lower the sheet. No source found; a ruling for the founder is not needed because WCAG sets the outcome, but Manta must design the mechanism |
| Touch target | P35 | **Yes** | The handle's hit area is at least 48dp (M3 `BottomSheetDragHandleView` minimum, same doc). This is over Manta's 44 |
| Contrast (map) | K15 | **Gap** | Map markers and controls sit on tiles, a varied ground like a photo. The rule from #117 B6.2 (meet the ratio against the real pixels, or use a solid backing) applies by analogy. Values: unknown (not built) |

Result: 6 of 12 properties get one answer today (role, border, shadow, handle, input path, touch target); motion is the seventh once mantahostels#2988 writes the clause. Gaps: radius token, scrim token, focus under the sheet, map contrast. Rulings: R1, R6.

## 5. Rule form (input to #103)

### 5.1 Schema

| Field | Holds | Why the critic needs it |
|---|---|---|
| `id` | Stable id (for example `manta.B46`) | Clash reports cite it |
| `applies-when` | Function codes (N A I S T R C D) **and** context predicates: zone (marketing / working), mode (Read / Operate), ground (sand / white / turquoise / ink / photo / map), device (touch / pointer), state (rest / hover / focus / selected / disabled), floats (yes / no) | The dependency root: a rule that names no function code fails a lint |
| `function` | The job the rule protects, in one line | Lets a reviewer judge whether an exception keeps the job |
| `inputs` | The measured properties it reads (ratio, px, neighbours' treatments) | Tells the critic what to measure from code or render (#127 D2) |
| `writes` | The property it sets: one of role, border, shadow, radius, fill, text-colour, type, spacing, state, motion, target, contrast | Two rules that write one property of one part can clash |
| `output` | The value or constraint | Compared between rules |
| `trades-off` | Rule ids it pulls against | Documents the known tension |
| `yields-to` | Rule ids, or a precedence level (F5 1-6) | Decides the clash with no human |
| `source` | Citation plus F5 level plus strength | Ranks it |
| `era` | T, or E with a date to review | Flags dated advice |
| `check` | One question, and whether a render or code answers it (#127 D2) | The critic runs it |
| `owner` | vault or a project | Write scope |

### 5.2 Three real rules rewritten

**manta.B46 (shadow).** Now: "Borders first; shadow only on hover and popovers; nothing at rest under a heavy shadow" (census `:254`, `brand-sheet.md:216`).
- applies-when: C or A; state rest or hover; floats any
- function: depth says "floats above" or "you can act"; it is not decoration
- inputs: floats?; interactive?; shadow blur and alpha
- writes: shadow
- output: floats → `--shadow-popover`; interactive and resting → none or ≤ `--shadow-card` (number by R3); static → none; hover → one signal (R2)
- trades-off: `manta.border-weak`, `vault.surface-E1`
- yields-to: level 1 (none apply); `#117 B2.1` for floating layers
- source: Manta level 2; condition from #117 B2.1 (M3, Atlassian)
- era: E (2026)
- check: "Does this part float or act? If neither, does it carry a shadow?" (render + code)

**manta.B20 + #117 E8 (selected wash).** Now: "lagoon wash for hover/selected only, never a card ground".
- applies-when: S, N (list row); state selected or hover
- function: show which item is chosen, not by colour alone
- inputs: wash ratio vs ground; presence of a second cue; that cue's ratio
- writes: fill, state
- output: hover → wash alone; selected → wash plus (check, or weight +1 step, or edge ≥3:1)
- trades-off: `manta.B10` (no information-free colour)
- yields-to: level 1 (WCAG 1.4.11, 1.4.1)
- source: Manta level 2; WCAG level 1
- era: T
- check: "Remove the hue: can you still see which item is selected?" (render, greyscale)

**manta.B12/B25 (coral).** Now: "coral is CTAs only, one per view"; "one coral object per view = sticky compare bar or hero search".
- applies-when: A; zone any; view-level count
- function: one primary action owns the strongest colour
- inputs: count of coral objects in the viewport; label size and weight
- writes: role, fill
- output: exactly one coral object per viewport; its label ≥19px/700 (B29); no other label above it in weight × size (P28)
- trades-off: `vault.conversion-lens` (more CTAs), `manta.eyebrow` (C9)
- yields-to: level 1 (contrast: 3.05:1 holds only at large text)
- source: Manta level 2; Apple HIG / GOV.UK level 3
- era: T (one primary); E (coral value)
- check: "Count the coral objects at each scroll position. Is it one?" (render at 3 widths)

### 5.3 How the critic detects a clash

1. For each part, take its function code and context. Select every rule whose `applies-when` matches.
2. Group the selected rules by `writes`. If one property has two outputs that differ and neither rule names the other in `yields-to`, apply F5. The lower level wins. If both are level 2 (two rules in one project file), report "unresolved clash; founder ruling" and name both ids.
3. Lint at write time: (a) every rule names a function code; (b) `trades-off` is mutual (A lists B → B lists A); (c) no `yields-to` cycle.

Worked example, hero search box (E19), property shadow:
- `manta.B46` matches (A, rest) and outputs "≤ `--shadow-card` at rest".
- `#117 B2.1` matches only if `floats = yes`. The hero box does not float, so it does not match.
- The box carries `--shadow-popover` → a breach of B46, not a clash.

The critic reports "B46 breach: rest shadow above the ceiling", and it can report this only after R3 sets the number. With the current text ("heavy" undefined) the output is not comparable, and the critic must report "rule not checkable".

## Bound

**Read in full:** `docs/research/manta-element-coverage.md` (#118), `surface-styling.md` (#117), `function-fit.md` (#127), `function-questions.md` (#130), `adopt-or-build.md` (#119), `text-presentation.md` (#123), `design-rules-census.md` (#98); issues #121 and #96 (bodies); mantahostels#2988 (body); Manta `docs/design-system/components/hostel/HostelCard.jsx`, `ui_kits/app/SearchResults.jsx` (189 lines).

**Sampled:**
- `docs/research/design-coverage-gaps.md` (#104: W7, W8, frame, answer).
- `manta-design-migration.md` (#115: §1.4, §2.3, §3).
- `past-design-rejections.md` (#102: Part C, answer).
- Closed-issue comments on #94, #95, #98, #102, #104, #115, #117, #118, #119, #123, #127, #130. They hold no founder ruling on any K conflict.
- Manta `app/globals.css` lines 1-215 and a grep of its focus rules.
- `ui_kits/marketing/Homepage.jsx:1`-`:45`.
- `ui_kits/app/MobileSearch.jsx` (grep of style lines).
- `components/forms/Input.jsx` (grep).

**Verified outside today:**
- WCAG 2.5.7 (W3C Understanding page).
- The M3 bottom-sheet scrim, shape token and drag-handle size (material-components-android BottomSheet.md).
- The m3.material.io spec page did not load.

**From knowledge, not re-read:**
- WCAG 1.4.11 boundary note, 2.2.1, G167.
- iOS 16px input zoom.
- Chrome placeholder colour.

**Not done:**
- No contrast was measured in a browser.
- Touch-target sizes are computed from styles, not measured.
- The brand sheet §7 and §10 text was not re-read.
