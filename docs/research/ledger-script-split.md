# design-vault#248 (map #243): the 574 script-routed ledger rows, split by how deterministic they are

Date: 15 Oct 2026.

Question: Of the 574 rows in `docs/coverage-ledger.json` that #216 ruled to fill (`ruling.fill` true) and routed to `script` (`tag.route`), how many are (1) fully deterministic, (2) deterministic in part, (3) judgement that was routed to script by mistake? Which measurement primitives do the deterministic rows need, and which of these primitives do the vault's scripts implement now?

## 1. Population count

Command: `jq '[.rows[]|select(.tag.route=="script" and .ruling.fill==true)]|length' docs/coverage-ledger.json` gives 574. Without the `ruling.fill` filter the count is 578 (4 script rows are accepted out). The 574 by area: typography 73, text 56, forms 52, navigation 51, data 37, interaction 36, layout 36, buttons 33, colour 31, overlays 30, motion 30, imagery 28, feedback 27, surfaces 21, content 20, system 13. 

All filled rows by route: gate 990, script 574, builder 169, whole-page 43 (1,776 in total). 185 of the 574 script rows have a `tag.why`.

## 2. Coding rubric (written before any row was coded)

Each row is one decision (for example "How much padding sits inside a button?"). Code it as the check that the house rule will become, when a house value exists (a threshold, a range, a required or forbidden state).

- **Code 1, fully deterministic.** Measurements on the rendered page decide pass or fail, with no eye. The measurement can use the DOM, computed style, the authored CSS, pixels, text, motion sampling, a scripted interaction, the network, or more than one page. The parts that the rule applies to can be found from the DOM, ARIA roles or a fact that the round declares (as `--cta` does for `check-layout.py`).
- **Code 2, deterministic in part.** One half is a measurement, as in code 1. The other half needs the eye. Typical forms: (a) the measurement is mechanical, but to find the parts that the rule applies to needs judgement ("the main image", "a decorative icon", "an important message"); (b) the rule has a value half (size, count, timing) and a fit half (does it look balanced, does it suit the content). gate.md line 16 makes such a rule two questions.
- **Code 3, judgement.** No measurement decides the decision. Typical forms: a choice between patterns that depends on the content or the task ("a tab bar or a side menu?"), writing quality or tone, a fit with brand or audience, a selection of a typeface or an image. A presence check that is trivial but that does not decide the real question does not make the row code 1 or 2.

Tie rules:
- A "when should X be used" decision is code 3 if the "when" needs the content's meaning; code 2 if the "when" is a judgement but the "how" has a measurable value; code 1 if the "when" is a DOM fact (for example "a form with more than 5 fields").
- A row about the source code (CSS units, `font-display`, logical properties) is code 1 if the authored CSS or the DOM shows it.
- A row about an asset file outside the page (image format, font file subset) is code 1, primitive network/load, when the file that the page loads shows it.
- If the row is a question of value that only a person can see (for example "is the icon optically centred"), it is code 2 or 3, not code 1, because the pixel half alone cannot decide it.

Primitives (for codes 1 and 2, the measurable half): `style` (computed style or authored CSS), `pixel` (render, screenshot, colour maths), `dom` (structure, roles, attributes, counts, geometry boxes), `text` (text content: length, words, case, characters), `motion` (animation sampling, timing curves), `interact` (drive an event such as hover, focus, input, submit, resize, then read the DOM or style), `net` (network, load timing, file sizes and formats), `cross` (more than one page or one state of the site). A row can need more than one.

Blindness: the coding list holds only `key`, `area`, `decision`, `element`, `property` and `context`, in a shuffled order. It also holds a check sample of rows that #216 routed to gate, builder or whole-page, so that the coder does not know the route of a row while coding. `tag.why` and `tag.route` are joined only after all codes are written.

## 3. Sample

Script: `.claude/tmp/research-ledger-script-split-sample.py` (seed 248). It draws n_h = max(6, round(0.28 × N_h)) rows from each area of the 574: 163 rows in total. It also draws a check sample of 64 rows at random from the 1,202 filled rows that are not script-routed (57 gate, 7 builder, 0 whole-page by chance). The 227 rows go into one shuffled list without route or why (`research-ledger-script-split-blind.csv`). I coded the 227 rows in that list order, one line each, in `research-ledger-script-split-codes.tsv`. Then `research-ledger-script-split-analyse.py` joined the codes to `tag.route`, `tag.fill` and `tag.why`. The joined file is `docs/data/ledger-script-split-2026-10-15.csv` (columns: key, area, decision, element, property, context, sample, code, alt, prims, reason, first_route, first_fill, first_why, target).

To recheck: run `research-ledger-script-split-sample.py`, then `research-ledger-script-split-analyse.py`, then `research-ledger-script-split-cost.py` (it adds the `target` column), each with the repo root as its argument and `python3 -I`.

For 14 of the 163 main rows I was not sure. Each of them has a second code in the `alt` column. 

## 4. Result: the split of the 574

Per area (main sample; Wilson 95% interval for each share):

| Area | N | n | Code 1 | Code 2 | Code 3 | Share code 1 | Share code 2 | Share code 3 |
|---|---|---|---|---|---|---|---|---|
| buttons | 33 | 9 | 8 | 1 | 0 | 89% (56–98%) | 11% (2–44%) | 0% (0–30%) |
| colour | 31 | 9 | 8 | 1 | 0 | 89% (56–98%) | 11% (2–44%) | 0% (0–30%) |
| content | 20 | 6 | 5 | 1 | 0 | 83% (44–97%) | 17% (3–56%) | 0% (0–39%) |
| data | 37 | 10 | 10 | 0 | 0 | 100% (72–100%) | 0% (0–28%) | 0% (0–28%) |
| feedback | 27 | 8 | 8 | 0 | 0 | 100% (68–100%) | 0% (0–32%) | 0% (0–32%) |
| forms | 52 | 15 | 14 | 1 | 0 | 93% (70–99%) | 7% (1–30%) | 0% (0–20%) |
| imagery | 28 | 8 | 7 | 1 | 0 | 88% (53–98%) | 12% (2–47%) | 0% (0–32%) |
| interaction | 36 | 10 | 10 | 0 | 0 | 100% (72–100%) | 0% (0–28%) | 0% (0–28%) |
| layout | 36 | 10 | 10 | 0 | 0 | 100% (72–100%) | 0% (0–28%) | 0% (0–28%) |
| motion | 30 | 8 | 8 | 0 | 0 | 100% (68–100%) | 0% (0–32%) | 0% (0–32%) |
| navigation | 51 | 14 | 13 | 1 | 0 | 93% (69–99%) | 7% (1–31%) | 0% (0–22%) |
| overlays | 30 | 8 | 8 | 0 | 0 | 100% (68–100%) | 0% (0–32%) | 0% (0–32%) |
| surfaces | 21 | 6 | 6 | 0 | 0 | 100% (61–100%) | 0% (0–39%) | 0% (0–39%) |
| system | 13 | 6 | 4 | 2 | 0 | 67% (30–90%) | 33% (10–70%) | 0% (0–39%) |
| text | 56 | 16 | 15 | 1 | 0 | 94% (72–99%) | 6% (1–28%) | 0% (0–19%) |
| typography | 73 | 20 | 19 | 1 | 0 | 95% (76–99%) | 5% (1–24%) | 0% (0–16%) |
| **all** | 574 | 163 | 153 | 10 | 0 | | | |

Totals over the 574 (stratified estimate, 95% interval with finite-population correction):

- **Code 1, fully deterministic: 94.3% (91.4–97.3%), about 541 rows (524–558).**
- **Code 2, deterministic in part: 5.7% (2.7–8.6%), about 33 rows (16–50).** These become two questions each by gate.md line 16: about 33 script questions and 33 look questions.
- **Code 3, judgement routed to script by mistake: 0 of 163.** The stratified interval is 0–0 because no stratum has a code 3, which is not a real bound. A Wilson bound on 0/163 gives at most 2.3%, about 13 rows.

The ten code-2 rows have two forms of look half:
- **The eye finds the parts that the rule applies to (6 rows):** IMG-143 (which image is pixel art or a code), COL-35 (which image is an illustration), BTN-13 (which kind of action a button is), TXL-33 (which words are foreign), TYS-27 (which text is secondary), NEW2-35 (which generated content is decorative). If the building session declares these parts, as `--cta` does now, these rows become code 1.
- **The eye judges the result (4 rows):** FRM-8 ("one topic" a page), FRM-50 and FRM-32 (how much a part stands out), PAG-19 (how a page with no script looks).

## 5. Sensitivity

14 of the 163 main rows have a second code. If every one of them takes its second code (the strictest reading): code 1 is 90.8% (87.0–94.5%), about 521 rows; code 2 is 7.4% (4.1–10.7%), about 43 rows; code 3 is 1.8% (0.1–3.6%), about 10 rows. Only three main rows have a code-3 reading: FRM-50 and FRM-32 (how much a search field or a lead form stands out) and TXL-33 (which words are foreign). The other doubts are between code 1 and code 2, for example BTN-21 (to find a destructive button by its verb) and IMG-133 (whether an aspect ratio suits the content).

Limit on independence: the second coder is also a Claude agent, as were the #216 taggers. The two codings share a model, so they can share a bias. 

## 6. Agreement with the first tagging (#216)

-  For the 57 main rows that have a `tag.why`, no why argues against a script. Where the why speaks to the route, it names the same measurement as my reason (for example TXL-21: "first focusable link to main is checkable"; LAY-149: "menu width against trigger width is measurable"). The other whys speak to the fill (for example TYS-7: "Missing condition is x-height").
- **The script route is precise, but it is not complete.** In the check sample of 64 rows that #216 sent to gate or builder, I coded 37 as code 1 (58%, Wilson 46–69%), 17 as code 2 and 10 as code 3. Gate rows: 31 of 57 code 1 (54%, 42–67%). Builder rows: 6 of 7 code 1. Scaled to the 1,202 filled rows that are not script-routed, about **695 more rows (548–830) are fully deterministic by the same rubric**, and about 1,014 (885–1,097) have a measurable half. Examples: NAV-140 "Does leaving the site trigger a warning modal?" (click an external link, look for a dialog), STA-13 (programmatic focus shows a ring), NAV-63 (same footer on every page: compare the footer across pages), LAY-95 and NEW2-8 (builder; one computed-style property each).
- **Why the two codings differ.** The #216 prompt (`.claude/tmp/0539697c-tag-prompt.md` line 35–39) defines `script` as "a measurable value or count … presence of an attribute" and `gate` as a yes/no question "that a script cannot settle". The taggers sent most yes/no rows about behaviour or presence (does X happen, may X and Y show together) to gate. My rubric codes these as code 1 when a scripted event and a DOM read decide them. So the split is by the form of the answer (a number against a yes/no), not by whether a script can settle it.
- **Cohen's kappa (script against not script, on all 227 coded rows):** unweighted κ = 0.21 (p_o 0.76) if "script" means code 1 or 2; κ = 0.41 (p_o 0.79) if it means code 1 alone. Weighted to the population (each main row stands for N_h/n_h rows, each check row for 1,202/64): κ = 0.11 and κ = 0.28. The kappa is low because of the gate rows above, not because of the script rows. It is not meaningful for the 574 alone: the first coder gives one value to all of them, so the expected agreement equals the observed agreement.
- Whole-page rows (43) did not come into the check sample, so this section says nothing about them.

## 7. Measurement primitives (code 1, and the measurable half of code 2)

A row can need more than one primitive (59 of the 163 main rows do), so the column does not add to 574. Stratified estimates over the 574, 95% interval:

| Primitive | Main-sample rows | Est. rows of the 574 | Vault scripts that do it now (`plugin/skills/design-round/scripts/`) |
|---|---|---|---|
| `dom` (structure, roles, attributes, counts, boxes) | 80 | 280 (250–310) | Yes: `check-layout.py` (boxes, overlap, clipping at each width), `parts-map.py` (actable parts, ARIA roles, listeners). No general count or presence probe. |
| `style` (computed style, authored CSS) | 63 | 224 (196–252) | Yes: `getComputedStyle` in 8 scripts; `parts-map.py` reads the `:hover` and `:focus` rules from the style sheets. No general property-against-value probe. |
| `interact` (drive an event, then read) | 33 | 118 (90–145) | In part: `check-access.py` presses Tab and Shift+Tab, reads focus and clicks a pause control; `check-layout.py` sweeps widths. No hover or press, no form submit, no overlay open, no scroll drive, no zoom or 1.4.12 text-spacing injection (gate.md `vault.reflow` source says the sweep does not apply 1.4.12's overrides). |
| `text` (length, words, characters, case) | 22 | 76 (53–99) | In part: `check-measure.py` counts characters a line; `check-layout.py` finds cut-off text. No word, sentence or glyph checks. |
| `pixel` (render, colour maths) | 11 | 38 (20–55) | Yes: `access-pixels.py` (contrast with glyph masks), `check-frames.py` (pixel compare), `check-overlay.py`; `colour_space.py` in design-project (ΔE00, OKLab). |
| `motion` (sample animations) | 10 | 37 (25–49) | Yes: `check-flow.py` seeks every Web Animations API animation frame by frame and has `--reduced-motion`. It is set up for brand motion only. No flash (WCAG 2.3.1) analysis. |
| `net` (load timing, block or throttle requests, file formats) | 2 | 7 (0–15) | In part: `check-load.py` throttles over CDP and reads LCP. No request blocking. |
| `cross` (more than one page or state of the site) | 1 | 4 (0–10) | No: each script opens one page. |

Emulation: reduced motion is used by `check-flow.py` only; no script emulates forced colours. Each script opens its own Playwright page (most borrow `flow.chromium()` from `check-flow.py`); there is no shared probe that many rules can call.

Shared primitives: `dom` and `style` together reach about 85% of the rows. A static render read for `dom` and `style` alone (no driven state, no pixels) reaches about 305 rows (272–337), 53% (47–59%).

### 7a. Cost proxies (added after the coding, by a second pass on the main sample)

Two flags, set per row in the CSV's `target` column and from the primitives:
- `target`: `native` if an HTML element, an ARIA role or an attribute finds the parts the rule applies to; `declared` if a script can find them only when the round names them (a toast, a hero, a testimonial, a bottom sheet, a card, a badge).
- `state`: `driven` if the row needs `interact`, `motion`, `net` or `cross`; else `static`.

| | Static | Driven |
|---|---|---|
| Native target | 331 (300–363), 58% | 100 (75–126), 17% |
| Declared target | 99 (73–125), 17% | 43 (24–63), 8% |

The house code to own, as an estimate and not a measurement: one shared page probe that reads `dom`, `style` and `text` against a rule table (the 58% native static cell is mostly one table line a rule); a small set of state drivers (hover and press, focus, submit with bad input, open and close an overlay, scroll, zoom and text spacing, block or throttle the network); and one way for the round to declare parts (as `--cta` does now), which also moves six of the ten code-2 rows to code 1. The pixel and motion rows can reuse `access-pixels.py` and `check-flow.py`. Also, 285 of the 574 rows have `fill` `research`: they have no house value yet, so their scripts cannot be written before their research job is filled.

## 8. Recommendation: does #212 Q6 (A) hold or flip?

Q6 (A) flips "if … most of these rules are too costly to script". The check does not find that.

- **Holds: 85% (75–92%).**  Even in the strictest reading, with no parts declaration and no driven state, the native static cell alone is 58% (52–63%) of the rows: most rows need one read of the DOM or computed style on one render.
- **Flips: 5% (2–12%).** Only if the house judges a shared DOM and style probe too costly to own, which the existing scripts (about 6,900 lines of measuring code on the same Playwright base) do not support.
- **Not settled by this check: 10% (4–20%).** The cost figures are proxies from primitives and target flags, not counted lines of code, and the coder shares a model with the first taggers.

A finding for the grilling ticket (#250), not a flip: the `script` route is precise but not complete.  Q6 (A) names "every value rule"; whether a presence or behaviour check that a script can settle also goes to a script is a question for the founder that this check does not answer.

**Bound.** Read in full: #248; #212 with its comments; gate.md lines 1–30; the #216 tag prompt's route lines (`.claude/tmp/0539697c-tag-prompt.md` lines 12–40); `.claude/tmp/inventory-deterministic.md` §1–3. Counted exhaustively by script: the 574 and every filled row's route, area and fill. Sampled only: 163 of the 574 rows (28%, stratified by area, seed 248) and 64 of the 1,202 filled rows not routed to script (0 whole-page rows in it). The vault's scripts were checked by grep for each primitive, not read whole. The cost split is a proxy from flags that I set after the coding, not a count of code. One coder (a Claude agent) coded every row; there is no third coder.
