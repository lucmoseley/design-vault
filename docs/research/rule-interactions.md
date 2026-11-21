# Rule conditions and known interactions in the house references (design-vault#206)

Status: complete (15 Oct 2026). 

Question (#206, child of map #202, founder note N19): Do the house's design references record the conditions and interactions their rules depend on? Which interactions that design and typography research knows do they miss?

Scope. Part 1 audits every rule with a value in `plugin/skills/design-critique/references/*.md` (five files) and `plugin/skills/design-round/references/impeccable.md`.  Part 3 gives the gaps and a verdict on the rule form of #121 (`docs/research/principle-interactions.md` §5, cut to nine fields by #103: `id`, `applies-when`, check question, answerer, `writes`, `yields-to`, `source` with strength, `era`, `owner`).

Not re-reported here (#121 holds them): the dependency order, P1-P42, and the clash table. Where a #121 row or a #123 finding already holds an interaction but the reference does not carry it, this file says "held in research, not carried" and gives the research line.

Strength codes. P = primary (standard, spec, first-party documentation, peer-reviewed study read). D = design-system documentation. E = expert or strong secondary (Butterick, Bringhurst, a foundry's documentation of its own face). W = weak. "second-hand" = read through a search snippet or a quotation in another text. Era: T = timeless (perception, geometry); E = era-bound, with the date.

## Part 1. Audit of the rules that have a value

### 1.1 Method

A "rule with a value" sets a number or a fixed relation (a ratio, a size, a count, a range, a formula). A rule that only names a property ("a small part changes colour, never shadow") is not counted. Each rule gets one class:

- **C (conditioned).** The rule names what its value depends on, and what changes when that factor changes.
- **Pt (partly conditioned).** The rule names a factor, but not how far the value moves, or it leaves out a main factor that research names.
- **S (scope only).** The rule names where it applies (a text role, a project override), but no factor that moves the value inside that scope.
- **U (unconditioned).** The rule gives a value and no condition.
- **F (fixed, no condition needed).** A definition, or a standard figure that does not change with design context.

### 1.2 The rules

| # | File:line | Rule (value) | Class | What it names / what it leaves out |
|---|---|---|---|---|
| 1 | `text-presentation.md:11` | Text tint OKLCH C 0.01-0.03, up to 0.05 for a blue-grey | C | Names the dominant hue, the ground hue, lightness ("falls toward white"). Leaves out the ground's temperature (see Part 2, I-12) |
| 2 | `text-presentation.md:20` | Prose link 3:1 against the text around it | C | Prose against nav, list or card |
| 3 | `surface-styling.md:11` | Control edge ≥3:1 | C | Function; fill as an alternative; `:12` names rendering: "anti-aliasing makes a thin line fainter than its token" |
| 4 | `surface-styling.md:31` | About three shadow levels | C | No drag, no nested overlays |
| 5 | `surface-styling.md:48` | Inner radius = max(R − p, fallback) | C | Padding |
| 6 | `surface-styling.md:66` | Focus ring 3:1 per ground; input ring 2 px outside or border ≥2 px | C | Ground; field against row; AAA status (a project may relax) |
| 7 | `surface-styling.md:66` | `scroll-padding` = sticky bar height | C | Bar height |
| 8 | `surface-styling.md:75` | Scrim 32-70% | C | Busy or bright backdrop → darker end; strong modal edge → lighter |
| 9 | `surface-styling.md:94` | Fill step under about 1.1:1 keeps the border | C | Fill step; "a poor screen" named as the reason |
| 10 | `surface-styling.md:103` | Borders and icon strokes in one band, thinner than the focus ring; lower grade for a light icon on dark | C | Weight of the text beside it; polarity |
| 11 | `brand-palette.md:23` | ΔE00 under 2 = one colour | C | Shares a view |
| 12 | `brand-palette.md:24` | Near-miss line ΔE00 10 | Pt | Names kind (hue or strength, greys far from the ground). Puts "text, a logo, icons, small marks, areas that do not touch" in one class, while `:26` gives small marks 20. Leaves out mark size, which research shows moves ΔE perception most (I-14) |
| 13 | `brand-palette.md:25` | Large greys sharing an edge: line 3 | C | Area, shared edge, nearness to the ground |
| 14 | `brand-palette.md:25` | A tint up to OKLCH C 0.05 counts as a grey | F | Definition |
| 15 | `brand-palette.md:26` | Two meanings: ≥10 large, ≥20 small marks | C | Mark size |
| 16 | `brand-palette.md:36` | Logo colours 3:1 against each ground | C | Ground lightness; keyline |
| 17 | `brand-palette.md:54` | Hue shift ≤15° toward the main hue | C | Interface colour, never the logo file |
| 18 | `first-visit-trust.md:23` | Task-text sentences ≤25 words | C | Task text against an argument in the owner's voice |
| 19 | `first-visit-trust.md:34` | Name, email, message; ≤1-2 optional fields | C | Plain enquiry; each extra field names its action |
| 20 | `house-principles.md:72-75`, `:81` | Carriers at 3:1 (link against text, action edge, input edge, selected state) | C | A label alone identifies a button, so no edge |
| 21 | `impeccable.md:74` | Light text on dark: small keeps weight, large may go one step lighter; keep extra line height and tracking | Pt | Names size and polarity. Leaves out where "small" ends, rendering (greyscale anti-aliasing thins small light text, I-9), and grade as the tool. #123 B4.2 and B5 hold these; the reference does not carry them |
| 22 | `impeccable.md:76` | A loop over 5 s needs a pause | C | Starts by itself; beside other content; not essential |
| 23 | `impeccable.md:83` | Body measure 45-75 characters | S | Body text only. Leaves out type size, leading, the face's width and x-height, the reading mode, the language (I-6, I-7). Held in research, not carried: #121 i1 ("Read pages target 60-75; dense UI may go shorter", `principle-interactions.md:156`). The same unconditioned range is enforced line by line by `design-critique/SKILL.md:65` and `design-round/scripts/check-measure.py:19` |
| 24 | `impeccable.md:84` | Line height under 1.3 is a finding on body text only (Butterick 120-145%) | S | Text role only. Leaves out measure, x-height, weight, size and script (I-5) |
| 25 | `impeccable.md:85` | Flat hierarchy: heading under 1.25× body is no finding where weight, space or tone carry the step | C | Other hierarchy cues |
| 26 | `impeccable.md:86` | Display ≤6rem; tracking no tighter than −0.04em | U | The project's type scale replaces both. The house states no relation of tracking to size or case (I-2, I-3) |
| 27 | `impeccable.md:88` | Touch target floor 24 px; 44 px a project may adopt | S | Project only. Held in research, not carried: #121 P35 (device: touch 44, pointer ≥24) |
| 28 | `impeccable.md:89` | ≤4 nav links stay visible | C | Link count |
| 29 | `impeccable.md:104` | 16 px body floor unless a dense role justifies less | S | Role. Leaves out x-height and width of the face (I-1). Held in research, not carried: #121 P29 (body size by mode) |
| 30 | `impeccable.md:104` | Leading set by measure | Pt | Names the factor, not the direction or amount; leaves out x-height and weight (I-5) |
| 31 | `impeccable.md:104` | 16 px or more for phone text | U | No condition. Held in research, not carried: #121 P30 (input text on touch, iOS zoom) is a separate reason |
| 32 | `impeccable.md:105` | Contrast 4.5:1 body, 3:1 large text, controls, icons, focus | Pt | "Large" is not defined here (it is in `gate.md:202` and `check-access.py:122`). Leaves out weight below bold, thin strokes, and polarity (I-10, I-11) |
| 33 | `impeccable.md:105` | Less chroma near white and black | C | Lightness |
| 34 | `impeccable.md:106` | A 4 px spacing step | U | No condition (density or type size could set the step) |
| 35 | `impeccable.md:107` | Motion 100-500 ms; longer for an authored focal entrance; exits faster | Pt | Names role. Leaves out the distance moved and the element's size, which Material 3 ties duration to (not researched further here; outside N19's type focus) |
| 36 | `impeccable.md:109` | LCP 2.5 s, INP 200 ms, CLS 0.1 | F | Fixed standard (75th percentile) |

### 1.3 Count

- Rules with a value: **36**.
- With a condition: **27** (C 22, Pt 5).
- Without a condition that moves the value: **7** (S 4: rows 23, 24, 27, 29; U 3: rows 26, 31, 34).
- Fixed, no condition needed: **2** (rows 14, 36).



### 1.4 What the count shows

1. **The gap sits in type.** Six of the seven unconditioned rules, and four of the five partly conditioned rules, set type: size, measure, leading, tracking, weight, contrast by size. The surface, palette and trust rules (#117, #143, #144) carry their conditions well. 
2. **The research holds more than the references carry.** #123 (`docs/research/text-presentation.md`) found irradiation against greyscale anti-aliasing (B4.2, `:206`-`:209`), optical size and grade (B5.2, `:229`-`:232`), caps tracking 5-12% (B2.3, `:159`-`:163`) and APCA's size-and-weight levels (B6, `:242`). #121 holds body size by mode (P29), measure by mode (i1) and caps tracking (P25). The reference `text-presentation.md` carries only the tint rule and the link rule (29 lines). #123's bound note (`:3`) put the rest out of the gate because they cannot fail a candidate; nothing then carried them into a reference a builder reads.
3. **The house has no input for the typeface.** No rule reads a font metric: x-height, width, stroke contrast, the `opsz` range, whether the face has `GRAD`. #121's `applies-when` predicates (`principle-interactions.md:253`) are function, zone, mode, ground, device, state and floats. So the house cannot say "this 16 px is too small for this face".
4. **Two enforced figures are unconditioned.** The 45-75 measure is a gate-like finding in `design-critique/SKILL.md:65` (each out-of-range line is a finding) and `check-measure.py`. The large-text threshold in `check-access.py:122` uses WCAG's two points (24 px, 18.66 px at 700) and no other weight. Both are correct to their sources.

## Part 2. Known interactions

### Source note S1: Apple HIG Typography (read 15 Oct 2026, JSON of the page, P/D)

URL: https://developer.apple.com/design/human-interface-guidelines/typography (JSON: `developer.apple.com/tutorials/data/design/human-interface-guidelines/typography.json`). This closes #123's open item "tracking table not read" (`docs/research/text-presentation.md:347`).

- **Tracking against size is a curve, and its shape depends on the face.** SF Pro (1/1000 em): 6 pt +41, 10 pt +12, 12 pt 0, 14 pt −11, 16 pt −20, 17 pt −26, 20 pt −23, 22 pt −12, 24 pt +3, 28 pt +14, 40 pt +10, 64 pt +4, 80 pt 0. New York (serif): 6 pt +40, 15 pt 0, 17 pt −4, 24 pt −11, 48 pt −14, 96 pt −16, 260 pt −18. SF Pro Rounded: 6 pt +87, 17 pt +22, 28 pt +13, 80 pt 0.
  - Small text always takes positive tracking (all three faces).
  - SF Pro turns back to positive at 24 pt. The page says the system font "dynamically adjusts tracking at every point size" and merges "discrete optical sizes (like Text and Display)". So the turn at about 20-24 pt is the switch to the Display design, which is drawn tighter. A face whose display cut is already tight needs no negative tracking at display sizes; a face with one design for all sizes (New York's curve) goes steadily tighter as it grows.
  - The rounded face takes about +48/1000 em more than SF Pro at 17 pt. Rounded terminals need more space between letters.
- **Leading falls as size grows.** iOS default sizes: Caption 2 11/13 (1.18), Body 17/22 (1.29), Title 1 28/34 (1.21), Large Title 34/41 (1.21). macOS Body 13/16 (1.23). Apple's own body leading is under the 1.3 that the house's detector condition (`impeccable.md:84`) calls a finding on body text. Apple sets UI body text, not long prose.
- **Leading against measure and line count.** "When you display text in wide columns or long passages, more space between lines (loose leading) can make it easier for people to keep their place." "If you need to display three or more lines of text, avoid tight leading even in areas where height is limited."
- **Weight against size.** "Avoid Ultralight, Thin, and Light font weights, which can be difficult to see, especially when text is small." "If you use a custom font with a thin weight, aim for larger than the recommended sizes."
- **Minimum sizes by platform** (default / minimum): iOS 17/11 pt; macOS 13/10 pt; visionOS 17/12; watchOS 16/12; tvOS 29/23. Size depends on viewing distance (tvOS) and device.
- Strength: D (first-party documentation of Apple's own faces). Era: the numbers are E (SF, 2015 on; dynamic optical sizes 2020 on); the direction (small text looser, large text tighter, rounded faces looser) is T.

### Source note S2: Material 3 type scale tokens (read 15 Oct 2026, D)

File: `material-components-android/lib/java/com/google/android/material/typography/res/values/tokens.xml` (raw GitHub, master). The m3.material.io pages are script-rendered; this is the shipped token file.

- **Tracking against size (Roboto):** Display Large 57/64, −0.0044 em; Display Medium 45, 0; Headline and Title Large 22-32, 0; Title Medium 16, +0.009 em; Body Large 16/24, +0.031 em; Body Medium 14/20, +0.018 em; Body Small 12/16, +0.033 em; Label Medium 12/16, +0.042 em; Label Small 11/16, +0.045 em.
  - Same direction as Apple: small text and labels take positive tracking, display takes slightly negative.
  - Labels (short UI strings) take more tracking than body text of the same size (12 sp: label +0.042, body +0.033). So tracking depends on role as well as size.
- **Leading ratio falls with size:** Label Small 11/16 (1.45), Body Large 16/24 (1.5), Body Medium 14/20 (1.43), Title Large 22/28 (1.27), Display Large 57/64 (1.12).
- **The two systems disagree on body leading:** Material body 1.43-1.5; Apple body 1.23-1.29 (S1). Both are first-party values for their own faces. So "the right line height" for 16 px body is not one number: it moves with the face (Roboto against SF Pro) and with the role (UI label against reading text).
- Strength D. Era E (M3, 2021 on; values unchanged at master, Oct 2026).

### Source note S3: Google Fonts Knowledge (read 15 Oct 2026, D/E)

Source text: `google/fonts` repo, `cc-by-sa/knowledge/modules/…/content.md` (the text behind fonts.google.com/knowledge, which is script-rendered). Lessons read in full: choosing_a_suitable_line_height, track_carefully_or_not_at_all, understanding_measure_line_length, exploring_x_height_the_em_square, choosing_typefaces_that_have_optical_sizes, exploring_width_in_type, exploring_typefaces_with_multiple_weights_or_grades, the_complications_of_typographic_size, how_type_influences_readability.

- **x-height sets apparent size.** "Verdana's x-height takes up about 55% of the font's em. But Baskerville's x-height only takes up about 40% … To achieve a similar visual size as Verdana, Baskerville must actually be set to a larger font size." So a 16 px floor means about 8.8 px of x-height in Verdana and about 6.4 px in Baskerville: a 27% smaller lowercase at the same CSS size.
- **x-height sets line height.** "As x-heights become taller, white space is redistributed from outside the letters to inside letters … it's usually a good idea to increase the line height." "Long ascenders and descenders … don't contribute to the overall perceived size — although they do require more generous line height settings."
- **Line height depends on size, measure, script and device.** "Between 115% and 150% is where the optimum value sits … for type set in a Latin script. Languages that use plentiful diacritics will usually need more generous leading." "The smaller the type, the more generous we should be with our line height … for display type, a line height smaller than the type size will usually look better. Consider 72px type with a line height of between 90% and 100%." "As our measure grows wider, so too should our line height become more open." "A value such as 150% for wide viewports might instead be 130% at mobile sizes." "There's no secret formula … It'll depend on the font, the size it's set at, the length of the line, and the overall reading context."
- **Measure depends on size and character width.** Recommendations "will depend on the actual size of the font (and specifically the width of the characters, including spaces)". Bringhurst's 45-75 is quoted with its own conditions: "for a single-column page set in a serifed text face in a text size". Material is quoted at "40 to 60 characters" for body text on screen. Cyrus Highsmith (*Inside Paragraphs*): word space depends on line height and measure, "a dependancy for all three".
- **Tracking depends on size and case.** "Add a more open … tracking value to all-caps or small caps type, especially at smaller (i.e., body) sizes." "Display sizes often benefit from a little negative tracking and very small text often benefits from positive tracking." Wichary (quoted): "Letter spacing gets tighter much faster than the font size gets bigger." Tracking interacts with ligatures (disable them when tracking opens) and numerals.
- **Optical size bundles the metric changes.** "Small (body or caption) optical sizes tend to have less stroke contrast, larger x-heights, wider characters, and more open spacing. Their large (or display) counterparts have refined features and tighter spacing." Viewing distance changes the right optical size: a TV at sitting-room distance takes a body optical size.
- **Weight against polarity (halation).** "Light type on a dark background appears to glare and its letterforms become bloated … we need to counter this halation problem … by selecting different weights so that both versions of the type feel the same." Example: Lato Regular against Lato Semibold "optically … appear the same". Grade is the better tool: it "alters only the thickness of the stroke without changing the width".
- **Weight step for emphasis.** "Avoid using semibold for emphasis in regular text. Use bold or extrabold to ensure a clearly visible difference."
- **Width and weight.** "Bold fonts are typically designed to be somewhat wider than light fonts"; a uniwidth face changes weight without reflow. "Condensed typefaces may benefit from a slight increase in size compared to wider counterparts, and typefaces with open apertures can perform better."
- **Crowding.** "Tighter kerning and letter spacing will increase problems with crowding." People differ in how much crowding they have. Glance reading takes "larger text size in non-condensed formats".
- **Size is angular.** Perceived size depends on viewing distance; the CSS reference pixel is an angle (about 0.0213° at 28 in), but devices vary.
- Strength: D/E (Google's own type education, written by type designers; it cites research but is not research). Era: T for the perceptual directions; E for the variable-font tools (2016 on).

### Source note S4: CSS specs (read 15 Oct 2026, P)

- **CSS Fonts 4 §8.1 `font-optical-sizing`** (https://www.w3.org/TR/css-fonts-4/#font-optical-sizing-def): "to aid reading at small text sizes, strokes are often thicker with larger serifs. Larger text often has a more delicate figure with more contrast between thicker and thinner strokes." With `auto`, "The user agent may modify the shape of glyphs based on the font-size and the pixel density of the screen", "often … by using the 'opsz' font variation". "User agents are expected to supply a value for the 'opsz' axis which is close to the used value for font-size." "User agents must not synthesize optical sizing when it is not performed by the font directly" and must clamp to the font's range. "font-optical-sizing interacts with font-size-adjust": the UA applies the optical size for the adjusted size. This closes #123's open item on the px mapping (`text-presentation.md:347`): the spec says "close to the used value for font-size", that is, CSS px. Optical size is a font trait: only a face with an `opsz` axis has it.
- **CSS Fonts 5 `font-size-adjust`** (https://www.w3.org/TR/css-fonts-5/): it "provides a way to preserve the readability and apparent size of text when font fallback occurs … by adjusting the used font size so that the specified metric is the same regardless of the font used." Metrics: `ex-height` (default), `cap-height`, `ch-width`, `ic-width`, `ic-height`; `from-font` reads the metric from the first available font. The spec: "the relative height of lowercase letters compared to their uppercase counterparts is a determining factor of legibility", and for text with diacritics "too large an x-height will actually decrease legibility". So CSS already exposes x-height as an input, and can set size by it.
- **CSS Text 4 §5.4 `text-wrap-style`** (https://www.w3.org/TR/css-text-4/#text-wrap-style): `balance` evens out the empty space in each line; it "must not change" the line count for 5 or fewer lines; "UAs may treat this value as auto if there are more than ten lines to balance". `pretty` biases "for better layout over speed", may "avoid excessively short last lines", reduce variation in line length and avoid rivers; "The necessary computations may be expensive … use it selectively". `avoid-short-last-line` fixes the orphan without making the previous line too short. So the choice depends on line count: `balance` for headings and short blocks, `pretty` or `avoid-short-last-line` for paragraphs. N1's orphan question has a conditioned answer. The house holds no rule on it (grep of the six files for `text-wrap`, `balance`, `orphan`: no hit).
- Era: E (CSS Fonts 4 `opsz` mapping, 2018 on; `font-size-adjust` in all major engines since 2024, from knowledge, not verified today; `text-wrap: balance` and `pretty` shipping 2023-2025, from knowledge, not verified today).

### Source note S5: WCAG 2.2 Understanding 1.4.3 and 1.4.8 (read 15 Oct 2026, P)

- **1.4.3, large text.** "Text that is larger and has wider character strokes is easier to read at lower contrast." "18 point text or 14 point bold text is judged to be large enough to require a lower contrast ratio", "approximately 18.5px and 24px". The sizes are "taken from the minimum size for large print (14pt)".
- **1.4.3 names the face as a condition.** "Fonts with extraordinarily thin strokes or unusual features" are "harder to read, especially at lower contrast levels." "Due to anti-aliasing, particularly thin or unusual fonts may be rendered by user agents with a much fainter color … best practice would be for authors to choose a font with stronger/thicker lines." "For many mainstream body text fonts, 14 and 18 point is roughly equivalent to 1.2 and 1.5 em", and authors "would need to check this for the particular fonts in use." WCAG states no rule for weights between regular and bold.
- **1.4.8 (AAA), visual presentation.** "Width is no more than 80 characters or glyphs (40 if CJK)." "Line spacing (leading) is at least space-and-a-half within paragraphs, and paragraph spacing is at least 1.5 times larger than the line spacing." "Text is not justified." Rationale: readers with some reading or vision disabilities "have trouble keeping their place". So the measure ceiling depends on script (80 Latin, 40 CJK), and WCAG ties a 1.5 leading floor to readers who need it.
- What the house holds: `gate.md:202` and `check-access.py:120-122` encode the two large-text points (24 px; 18.66 px at ≥700). Neither the gate nor any reference carries WCAG's own thin-stroke and anti-aliasing caveat, or the instruction to check the size equivalence for the face in use.
- Era: T for the need; the numbers are WCAG 2.x (2008-2023), current.

### Source note S6: APCA font lookup table (read 15 Oct 2026, W-E: the method's own author; contested as a standard)

Source: `apca-w3@0.1.9`, `src/apca-w3.js:449-546` (`fontLookupAPCA`, "Public Beta 0.1.7 (G) • MAY 28 2022"); GitHub discussion Myndex/SAPC-APCA #28 (the author on reference fonts).

- **Contrast, size and weight trade continuously.** Minimum px size at each weight (100-900) for a given Lc:
  - Lc 60: 300 → 42 px; 400 → 24 px; 500 → 21; 600 → 18; 700 → 16.
  - Lc 75: 300 → 24 px; 400 → 18; 500 → 16; 600 → 15; 700 → 14.
  - Lc 90: 200 → 32 px; 300 → 21; 400 → 16; 700 → 14.
  - Lc 45: 400 → 42 px; 700 → 24 px. Under Lc 30, weights 100-300 are "non-text" only.
  - "Lc values under 70 should have Lc 15 ADDED if used for body text."
  - Reading: at one contrast, one weight step (400 → 500) buys about 2-3 px of size; 300 against 400 costs 6-18 px. WCAG has two points (regular, bold) on this surface.
- **The table assumes a reference face.** The code says "reference font is Barlow"; the author's discussion names "Helvetica Neue, Helvetica, Fira Sans, Kanit, and Arial" and says "Values shown are for common sans-serif fonts". To adjust, divide the reference x-height by the face's x-height: Helvetica's x-height is about 0.52 em; a face at 0.45 needs 52/45 = 115.5%, so 16 px becomes about 18.5 px. Weight is adjusted by eye ("Raleway 400 as equivalent to 300").
- **Polarity.** APCA gives light-on-dark a different (signed) Lc from dark-on-light at the same WCAG ratio; #123 B6 measured this on Manta (`docs/research/text-presentation.md:242`-`:261`).
- Status: WCAG 3's contrast method is "yet to be determined" (#123 B6, `text-presentation.md:242`). So the table is a design aid, not a floor; WCAG 2 stays the floor (`house-principles.md` level 1).
- Era: E (2021 on, unsettled). The direction (thinner and smaller text needs more contrast) is T and agrees with WCAG's own rationale.

### Source note S7: legibility and reading research (read 15 Oct 2026, P unless marked)

- **Legge and Bigelow 2011**, "Does print size matter for reading?", *Journal of Vision* 11(5):8, doi:10.1167/11.5.8 (abstract read through Europe PMC; full text blocked). "The fluent range extends over a factor of 10 in angular print size (x-height) from approximately 0.2° to 2°. Assuming a standard reading distance of 40 cm … the corresponding physical x-heights are 1.4 mm (4 points) and 14 mm (40 points)." The unit that reading speed follows is the angular **x-height**, not the font size.
  - My calculation (not in the source): the CSS reference pixel is about 0.0213° (CSS Values 3, quoted in S3). At 16 px, an x-height of 0.484 em (Nunito Sans, measured below) is 7.7 px ≈ 0.165°; 0.40 em (Baskerville, S3) is 6.4 px ≈ 0.136°; 0.545 em (Verdana, S3) is 8.7 px ≈ 0.186°. So a 16 px body sits near the lower end of the fluent range at the reference distance, and the face's x-height decides how near. Real pixel angles vary by device (S3). Treat these as rough.
- **Legge, Rubin and Luebker 1987**, "Psychophysics of reading V. The role of contrast in normal vision", *Vision Research* 27(7), doi:10.1016/0042-6989(87)90028-9 (abstract). "Reading rates were highest … for letters ranging in size from 0.25 degree to 2 degrees. Within this range, reading was very tolerant to contrast reduction … Reading rate declined more rapidly for very small (less than 0.25 degree) and very large … letters." "The results were very similar for white-on-black and black-on-white text." So contrast need rises as size falls toward the lower edge: the interaction that WCAG's large-text rule and APCA's table encode.
- **Legge et al. 1997**, "Psychophysics of reading XVI. The visual span in normal and low vision", *Vision Research*, doi:10.1016/s0042-6989(97)00017-5 (abstract). Visual span "ranged from about 10 characters for high-contrast text to less than two characters for low-contrast text". Low contrast slows reading through fewer letters per glance.
- **Legge, Parish, Luebker and Wurm 1990**, "Psychophysics of reading XI. Comparing color contrast and luminance contrast", *JOSA A* 7, doi:10.1364/josaa.7.002002 (abstract). "When color contrast is high, normal subjects can read as rapidly as with high luminance contrast"; with both present, "performance is determined by the form of contrast yielding the highest reading rate". For low-vision readers, luminance contrast beat colour contrast. So hue on its own does not change reading speed when luminance contrast is held; #183 found the same (`docs/research/house-audit-visual.md:59`, Legge and Rubin 1986).
- **Dyson 2004**, "How physical text layout affects reading from screen", *Behaviour & Information Technology* 23(6) (review, PDF read in full through a course mirror).
  - "Many typographers would maintain that typographical variables cannot be considered individually." "Long line lengths are said to need more interlinear spacing to ensure that the eyes locate the next line down accurately" (Bouma 1980). Lund: holding leading fixed while line length grows changes their ratio, a confound.
  - Line length on screen: 100 characters per line read faster than 25 (Dyson and Kipping 1998); Dyson and Haselgrove 2001 found "55 characters per line producing better comprehension scores than the longest line length (100 characters per line)". "There is a range of line lengths within which changes to the number of characters have little effect." Print guidance: Spencer about 70; Tinker's work implies 52.
  - Preference and performance diverge: "Although longer line lengths may be read faster, people prefer a more moderate length."
  - "We tend to sit further away from the screen than from printed matter … a longer physical line length on screen subtends a smaller visual angle." So the right measure depends on viewing distance as well as characters.
  - Strength: P (peer-reviewed review); the studies are 1998-2004 on CRT and early LCD screens. Era: the trade-off (fixations per line against return sweeps) is T; the screen numbers are E (old screens, scrolling by scroll bar).
- **Chung 2002**, "The effect of letter spacing on reading speed in central and peripheral vision", *IOVS* (abstract). Reading speed rose with letter spacing "up to a critical letter spacing", which "was very close to the standard letter spacing and did not depend on eccentricity or print size". Wider than standard did not help normal readers.
- **Zorzi et al. 2012**, "Extra-large letter spacing improves reading in dyslexia", *PNAS*, doi:10.1073/pnas.1205566109 (abstract). Extra-large spacing improved reading "on the fly" in dyslexic children, "because dyslexics are abnormally affected by crowding".
- **Pelli and Tillman 2008**, "The uncrowded window of object recognition", *Nature Neuroscience*, doi:10.1038/nn.2187 (abstract). "Vision is usually limited by object spacing rather than size." Critical spacing "is proportional to object distance from fixation"; the uncrowded window "limits the speed of reading and search".
- **Palmén, Gilbert and Crossland 2023**, "How bold can we be? The impact of adjusting font grade on readability in light and dark polarities", CHI 2023, doi:10.1145/3544548.3581552. Read second-hand only (Readability Matters summary quoting the abstract; ACM returned 403). "Two studies with a total of 459 participants"; "Dark text on a light background (Light Mode) is read reliably faster than its polar opposite (Dark Mode)"; a grade effect was found "for LM with heavier, increased grade levels"; designers "can vary grade … to influence design aesthetics" without reducing reading fluency; "further research is needed to determine the optimal grade settings". Note: `impeccable.md:74` cites the Material blog "Adjusting Grade for Mode" (2022, 184 people). I could not open that blog (m3.material.io failed) to check the 184 figure; the CHI paper's total is 459. Its claim (no readability need to change grade between modes) agrees with the CHI summary. Legge 1987 (above) also found polarity "very similar" for normal readers.
- **Font metrics, measured (my script `/tmp/r206scripts/metrics.py`, OS/2 and fvar tables, default instance):** Quicksand: x-height 0.503 em, cap 0.700, average width 0.541, axes wght 300-700. Nunito Sans: x-height 0.484 em, cap 0.705, average width 0.567, axes wght 200-1000, wdth 75-125, opsz 6-12, **YTLC 440-540** (a parametric lowercase-height axis). These are Manta's faces (read-only here), used only to show that the metrics the interactions need can be read from the font file with no dependency.

### Source note S8: crowding, clutter and colour appearance (read 15 Oct 2026)

- **Rosenholtz, Li and Nakano 2007**, "Measuring visual clutter", *Journal of Vision* 7(2):17, doi:10.1167/7.2.17 (abstract, P). Clutter causes "crowding, masking, decreased recognition performance … greater difficulty at both segmenting a scene and performing visual search". The Feature Congestion measure "is based on the analogy that the more cluttered a display or scene is, the more difficult it would be to add a new item that would reliably draw attention". Three image measures (Feature Congestion, Subband Entropy, Edge Density) "correlate well with search performance".
- **Duncan and Humphreys 1989**, "Visual search and stimulus similarity", *Psychological Review* 96(3), doi:10.1037/0033-295x.96.3.433 (abstract not returned; finding from knowledge, not re-read): search gets harder as the target grows more like the non-targets and as the non-targets grow less like each other.
- **Simultaneous colour contrast (Kirschmann's laws; Ekroll and Faul; Bosten et al. 2012).** Read through search results only (second-hand). A neutral target tends to look tinted away from its surround's hue (the "complementarity law"; Ekroll and Faul dispute the exact direction). Kirschmann's third law: the effect is greatest when target and surround have equal luminance, and weakens as their luminance contrast grows (a 2020 *Scientific Reports* thin-line study contests it for thin lines with white flanks). Strength: P but contested in detail; the main direction is T.
- **Helmholtz-Kohlrausch effect.** Read through search results only (second-hand: NTNU 2022 thesis, SPIE 2015, CIE 2025 paper). Saturated colours look brighter than achromatic colours of the same luminance; the effect depends on hue ("red and magenta as compared to yellow"). WCAG 2's ratio uses luminance only, so it does not model this. No source found that measures the effect on text contrast; applying it to coloured text is my inference.

### Source note S9: Butterick and Inter (read 15 Oct 2026, E)

- **Butterick, *Practical Typography*** (practicaltypography.com, pages line-spacing, line-length, point-size, letterspacing). "For most text, the optimal line spacing is between 120% and 145% of the point size." Line length: "45–90 characters, including spaces"; characters per line "works at any point size". Point size: web "15–25 pixels"; "different fonts set at the same point size won't necessarily appear the same … let your eyes be the judge." Letterspacing: "always add 5–12% extra letterspacing to text in all caps or small caps. This is particularly important at small sizes." "Fonts intended for body text have spacing optimized for body-text point sizes (approximately 9–13 point). But typographers will often add letterspacing to lowercase text smaller than 9 point."
- **Inter v3 "dynamic metrics"** (rsms, archived at d.rsms.me/inter-website/v3/dynmetrics/; the live page is gone). Tracking = a + b·e^(c·z), a = −0.0223, b = 0.185, c = −0.1745, z = size in px. My evaluation: 8 px +0.024 em; 12 px 0.000; 16 px −0.011; 24 px −0.019; 32 px −0.022. A face's designer gives a size-to-tracking curve for that face only. From knowledge, not verified today: Inter 4.0 (2023) added an `opsz` axis with a Display design, which explains why the formula page was retired: the optical size now does part of the work.

## Part 2 synthesis: the interactions

Columns:  **House** says whether the six reference files hold it, with file:line; "research only" means #121 or #123 holds it and no reference carries it.

| # | Interaction | Effect (direction, rough size) | Source, strength | Era | House |
|---|---|---|---|---|---|
| I-1 | **x-height × font size** (the size floor) | At one CSS size, apparent size follows x-height: 0.40 em (Baskerville) against 0.55 em (Verdana) is 27% less lowercase height. To match a 0.52 em reference, scale size by 0.52 / x-height (0.45 → ×1.155). At 16 px and arm's length, body text sits near the 0.2° lower edge of the fluent range, so x-height decides whether it is inside | S3 (D/E), S6 (author, W-E), S7 Legge and Bigelow 2011 (P), S4 `font-size-adjust` (P) | T | **No.** `impeccable.md:104` sets 16 px with a role condition only; #121 P29 conditions by mode only |
| I-2 | **Tracking × size** | Small text looser, large text tighter. SF Pro: 6 pt +4.1%, 12 pt 0, 17 pt −2.6%. M3: 11 sp +4.5%, 16 sp body +3.1%, 57 sp −0.4%. Inter v3: 8 px +2.4%, 32 px −2.2%. The curve is the face's own: SF Pro returns to +0.3% to +1.4% from 24 pt (its Display design), New York reaches −1.8% at 260 pt, SF Pro Rounded is about 5% looser than SF Pro at 17 pt | S1 (D), S2 (D), S3 (D/E), S9 Inter (E), Butterick under 9 pt (E) | T (direction); E (values) | **No.** `impeccable.md:86` hands the −0.04em floor to the project scale; no rule relates tracking to size or face |
| I-3 | **Tracking × case and role** | Caps +5 to +12%, "particularly important at small sizes"; short UI labels take more than body text at one size (M3 12 sp: label +4.2%, body +3.3%) | S9 Butterick (E), S3 (D/E), S2 (D) | T | Research only: #123 B2.3 (`text-presentation.md:159`-`:163`), #121 P25 |
| I-4 | **Tracking × crowding and reader** | Tighter spacing "will increase problems with crowding". For typical readers, reading speed peaks at the face's standard spacing; wider spacing gains nothing. For dyslexic readers, extra-large spacing helps. WCAG 1.4.12: layout must survive 0.12 em | S3 (D/E), S7 Chung 2002 (P), Zorzi 2012 (P), Pelli and Tillman 2008 (P), WCAG 1.4.12 (P, via #123) | T | **No** (negative tracking on body text is not addressed; #123 notes impeccable's "crushed letter spacing" detector, `text-presentation.md:45`) |
| I-5 | **Leading × size, x-height, measure, script, line count** | Smaller text needs more leading; display can run 0.9-1.0 at 72 px. Larger x-height needs more. Longer measure needs more (150% wide, 130% on a phone). Diacritic-rich scripts need more. Three or more lines: avoid tight leading. Shipped body values differ by face and role: Apple 1.23-1.29 (UI body), M3 1.43-1.5. Latin range 1.15-1.5 (Google), 1.2-1.45 (Butterick); WCAG AAA 1.5 | S1 (D), S2 (D), S3 (D/E), S5 WCAG 1.4.8 (P), S7 Dyson (P), S9 (E) | T (directions); E (values) | **Partly.** `impeccable.md:84` (role only), `:104` (measure named, no direction or size). x-height, size and script: no |
| I-6 | **Measure × size, character width, leading, viewing distance, script, reading task** | Bringhurst's 45-75 is for "a single-column page set in a serifed text face in a text size". Ranges: Butterick 45-90; Material 40-60; WCAG AAA ≤80 (≤40 CJK). Screen research: 55 characters best for comprehension, 100 fastest, a flat middle range; readers prefer moderate. Leading must rise with measure | S3 (D/E), S5 (P), S7 Dyson 2004 (P), S9 (E) | T (trade-off); E (screen numbers) | **No condition.** `impeccable.md:83`, `design-critique/SKILL.md:65`, `check-measure.py:19` apply 45-75 to every width and face. Research only: #121 i1 (`principle-interactions.md:156`) conditions by mode |
| I-7 | **Optical size × size** (stroke contrast, x-height, width, spacing together) | Small optical sizes: less stroke contrast, larger x-height, wider, looser. Display: finer, tighter. CSS `auto` sets `opsz` near the used font size (px) and clamps to the font's range; only faces with `opsz`. Viewing distance changes the right optical size (TV: body size). A face with `opsz` needs less manual tracking at display sizes (SF Pro, I-2) | S4 CSS Fonts 4 (P), S3 (D/E), S1 (D) | T (practice); E (variable fonts, 2016 on) | Research only: #123 B5.2 (`text-presentation.md:229`-`:232`) |
| I-8 | **Weight × polarity** (light text on dark) | Light text on dark looks heavier (irradiation, halation): Lato Regular on dark ≈ Semibold on light; grade −25 to −50 offsets it without reflow. But: dark mode is read slower than light mode (CHI 2023, 459 people), grade changes did not cost fluency, and Legge 1987 found polarity "very similar" for normal readers. So the weight change is a look choice, and small light text must not get thinner (I-9) | S3 (D/E), #123 B4.2 (E/W), S7 CHI 2023 (P, second-hand), S7 Legge 1987 (P) | T | **Partly.** `impeccable.md:74`: size and polarity held; the size threshold, grade and rendering not |
| I-9 | **Weight × rendering and size** | Anti-aliasing makes thin or unusual fonts render "with a much fainter color"; greyscale anti-aliasing makes light-on-dark text "look lighter". Apple: avoid Ultralight, Thin and Light, "especially when text is small"; with a thin custom font, "aim for larger than the recommended sizes" | S5 WCAG 1.4.3 Understanding (P), S1 (D), #123 B5.1 (MDN) | T (perception); E (rendering stacks) | **Partly**, for lines only: `surface-styling.md:12`. For text: research only (#123 B5, `text-presentation.md:223`-`:226`) |
| I-10 | **Contrast × size × weight** | Continuous trade: at APCA Lc 60, 400 needs 24 px, 700 needs 16 px; at Lc 75, 300 needs 24 px, 400 needs 18 px. One weight step buys about 2-3 px; 300 against 400 costs 6-18 px. Add Lc 15 for body text under Lc 70. WCAG 2 has two points (24 px; 18.66 px at 700) | S5 (P), S6 (W-E), S7 Legge 1987 (P) | T (direction); E (APCA values, unsettled) | **Partly.** `impeccable.md:105` (large text undefined there); `gate.md:202` and `check-access.py:120`-`:122` encode WCAG's two points. Research only: #123 B6 (APCA levels) |
| I-11 | **Contrast × typeface** (stroke weight, x-height, unusual forms) | WCAG: thin or unusual fonts are "harder to read, especially at lower contrast levels"; the 14/18 pt to em equivalence must be checked "for the particular fonts in use". APCA's table assumes a reference face with x-height about 0.52; scale size by the ratio and judge weight by eye against Helvetica | S5 (P), S6 (W-E) | T | **No** |
| I-12 | **Text tint and temperature × ground** | A near-neutral grey reads tinted away from its ground's hue. The shift is largest where text and ground are near in luminance and small at body-text contrast. So it matters for muted text, placeholders, disabled text and borders, and little for body text. Hue alone does not change reading speed when luminance contrast is held. No source found that a warm or cool tint changes the best weight | S8 (P, contested detail, second-hand), S7 Legge 1990 (P) | T | **Partly.** `text-presentation.md:12` gives secondary text on a coloured ground "that ground's own hue at another lightness". The induction direction and its luminance dependence: no |
| I-13 | **Chroma × perceived contrast** (Helmholtz-Kohlrausch) | Saturated colours look brighter than their luminance says, more for red and magenta than yellow. Inference, no text study found: coloured text on a light ground reads weaker than its WCAG ratio; on a dark ground, stronger | S8 (P for the effect; the text application is my inference) | T | **No** |
| I-14 | **Colour difference × mark size** | Small marks need a larger ΔE to read as different | Szafir 2018, via #178 (P) | T | **Partly.** `brand-palette.md:26` holds it for two meanings; `:24`'s near-miss line 10 puts small marks and large separated areas in one class |
| I-15 | **Density and clutter × hierarchy cue strength** | The more cluttered the area, the harder it is "to add a new item that would reliably draw attention"; search slows as the target grows more like its neighbours and the neighbours less like each other. So a heading or primary action in a crowded section needs a larger step (size, weight, colour, space) than in a sparse one. No design source gives the size of the step: a gap | S8 Rosenholtz 2007 (P), Duncan and Humphreys 1989 (P, from knowledge) | T | **No.** `impeccable.md:85` (flat hierarchy) lets weight, space or tone carry a step, with no density condition |
| I-16 | **Weight step × emphasis and the ground weight** | One step (400 → 500/600) is often too small to see as emphasis: "Avoid using semibold for emphasis in regular text. Use bold or extrabold." The visible step also shrinks on dark (I-8) and at small sizes (I-9) | S3 (D/E) | T | **No.** `surface-styling.md:100` and `house-principles.md:75` accept "a weight change" as the second cue for a selected state, with no step size; #121's rewrite of B20 says "weight +1 step" (`principle-interactions.md:284`) |
| I-17 | **Width × size and reflow** | Condensed faces "may benefit from a slight increase in size"; glance reading wants "larger text size in non-condensed formats". Bold is wider than light, so a weight change on hover or selection reflows text unless the face is uniwidth or the change uses grade | S3 (D/E) | T | **No** |
| I-18 | **Viewing distance × size** | Perceived size is angular; the right size grows with distance (tvOS default 29 pt against iOS 17 pt; a TV takes a body optical size). On the web the px is only roughly angular | S1 (D), S3 (D/E), S7 (P) | T | **No** (the house conditions by touch against pointer only: #121 P30, P35) |
| I-19 | **Line breaking × line count** (`text-wrap`) | `balance` suits headings and short blocks (it must not change the line count up to 5 lines; a UA may ignore it over 10). `pretty` and `avoid-short-last-line` suit paragraphs; `pretty` costs layout time on long text | S4 CSS Text 4 (P) | E (2023 on) | **No** (N1's orphan question) |

## Part 3. What the house should hold, and the rule form

### 3.1 N19's examples, answered

- **"The best weight for the same text may depend on the palette."** Yes, through luminance contrast: weight, size and contrast trade continuously (I-10), polarity changes apparent weight (I-8), and saturated text may read weaker than its ratio (I-13, inference). The palette moves weight only through these routes.
- **"… how crowded the section is."** Yes: in a crowded section a hierarchy step must be larger to draw the eye (I-15), and a one-step weight change is often invisible (I-16). Tight tracking adds letter crowding (I-4). 
- **"… whether the text is warm or cool."** Not directly: no source found that tint temperature changes the best weight. A tint changes how a grey reads beside its ground, mostly for low-contrast text (I-12). Saturation, not temperature, changes perceived contrast (I-13).
- **"The best size or spacing may depend on the typeface's own traits."** Yes, strongly: x-height sets the size floor and leading (I-1, I-5); the face's own tracking curve and optical sizes set tracking (I-2, I-7); width sets size and measure (I-6, I-17); stroke weight sets the contrast need (I-11).

### 3.2 Interactions the house should hold and does not

In order of reach (how many pages each touches) and evidence strength:

1. **x-height sets the size floor (I-1), and stroke weight and x-height set the contrast need (I-11).** Every text rule with a px value assumes a typical face. Carry: "16 px for a face whose x-height is about 0.52 em; scale by 0.52 / x-height", read from the font file or CSS `font-size-adjust: from-font`. 
2. **Leading and measure are one decision with size and face (I-5, I-6).** Replace the unconditioned 45-75 (`impeccable.md:83`, `design-critique/SKILL.md:65`, `check-measure.py:19`) and the role-only 1.3 floor (`impeccable.md:84`) with conditioned ranges: measure by reading task (#121 i1 already says Read 60-75, dense UI shorter), by script (WCAG ≤80, ≤40 CJK) and by the face's width; leading up as measure, x-height or script diacritics go up, and down as size goes up. 
3. **Tracking follows size, case and the face (I-2, I-3, I-7).** Carry the direction (small looser, display tighter, caps +5-12%) and "use the face's own curve where its designer publishes one (SF, Inter v3), and expect less manual tracking where the face has `opsz`". Carry #123 B2.3 and B5.2 into the reference.
4. **Contrast, size and weight trade (I-10), and polarity and rendering move weight (I-8, I-9).** Keep WCAG 2 as the floor; add the APCA table as a design aid above it (#123 B6 already measured Manta pairs). Consolidate `impeccable.md:74` with #123 B4.2 and B5: on dark, large text may go lighter by grade; small light text never goes thinner; no weight under 400 at body size.
5. **A weight step must be visible (I-16).** "A weight change" as a selected-state or emphasis cue needs at least two steps (400 → 700), more on dark and at small sizes.
6. **Density raises the step a hierarchy cue needs (I-15).** Carry the direction now.
7. **Tint against ground and chroma against contrast (I-12, I-13).** Low reach for body text. Carry: judge muted text, placeholder and border greys on their real ground; check saturated text by eye beyond its ratio.
8. **Width, viewing distance and line breaking (I-17, I-18, I-19).** Lower reach. `text-wrap: balance` for headings and `pretty` for paragraphs answers N1's orphan question directly.

### 3.3 Can #121's rule form carry them?

**Verdict: not as cut by #103. It needs two fields back and one new input class.**

- **#103 cut the two fields these interactions need.** #121's §5 form had `inputs` (the measured properties a rule reads) and `output` (the value or constraint). #103 dropped both and kept nine fields "for gate questions only" (`principle-interactions.md:3`). An interaction rule is mostly not a gate question: it sets a value from several inputs, and only its WCAG floor can fail a candidate. So the builder-facing reference needs a form the gate form does not give.
- **`applies-when` holds categories; interactions need continuous inputs.** Its predicates (function, zone, mode, ground, device, state, floats; `principle-interactions.md:253`) select a rule. Size, x-height, measure in characters, Lc, line count and clutter are numbers that move the value inside the rule. A predicate "size 12-20 px" would split one curve into many rules.
- **`yields-to` resolves clashes; interactions compose.** Leading set by size, x-height and measure is not three rules where one wins. It is one value from three inputs. Two rules that write `type.leading` would be reported as a clash, wrongly.
- **A font-metric input class is new.** No current predicate or input names the face. The face profile (x-height, cap height, average width, stroke weight class, axes present with their ranges, rounded or not) is a property of the project's fonts, measured once per face and recorded in the project's rules file. My script read it from the OS/2 and fvar tables in about 30 lines (S7); CSS `font-size-adjust: from-font` reads x-height at render time (S4).

**The form that carries them (proposal for the spec, not a ruling):**

| Field | Holds | New or kept |
|---|---|---|
| `id`, `applies-when`, `source`, `era`, `owner` | As #121/#103 | Kept |
| `writes` | One property; **one owner rule per typographic property** (size, leading, tracking, measure, weight) | Kept, with the owner constraint |
| `inputs` | The numbers the value depends on, each with its own source strength and era: `face.x-height`, `face.width`, `face.axes`, `text.size`, `text.weight`, `text.case`, `measure.chars`, `contrast.wcag`, `contrast.apca`, `ground.luminance`, `block.lines`, `area.clutter` | Restored from #121 |
| `output` | A function or lookup table over the inputs, with its domain, its direction stated in words, and the numbers marked as source values or house picks | Restored, widened to a function |
| `floor` | The WCAG term that can fail a candidate; only this part becomes a gate question with `yields-to` | New split |
| `check` | Who measures each input (font file script, `check-measure.py`, `check-access.py`, render) | Kept (#103 "answerer") |

Worked example (illustrative numbers from the sources above; not a proposed house value):

- id: `vault.type-size-body`
- applies-when: R, running text; mode Read
- writes: `type.size` (owner)
- inputs: `face.x-height` (T, S3/S7), `text.weight` and `contrast.apca` (E, S6), viewing class (T, S3)
- output: size ≥ 16 px × 0.52 / `face.x-height`, and ≥ the APCA lookup for (Lc + 15 where Lc < 70, weight); the larger wins
- floor: WCAG 1.4.3 at the used size and weight (gate question; level 1)
- check: x-height from the font file; Lc and size from `check-access.py`

The same shape takes leading (inputs size, x-height, measure, script, lines), tracking (size, case, face curve, `opsz`), and measure (task, script, face width). Under the coarse-to-fine idea in map #202's notes, these owner rules sit at #121's value step (4), after function, role and treatment; their inputs are fixed by then.

### 3.4 What no source settles (research gaps, by kind)

- **I-15 step size against clutter:** a point on a measured curve; no design study gives it.
- **I-12 temperature against weight:** no evidence found either way; the house should state it as unsourced, not invent a rule.
- **Body leading for a given face** inside 1.2-1.5: a taste between sourced ranges (Apple and Material differ for their own faces).
- **Measure on screen:** a trade between reading speed (longer) and comprehension and preference (about 55); which the house serves is a taste per reading task.
- **The 0.52 reference x-height:** APCA's only; whether 16 px was set against such a face (impeccable, Butterick) is unknown.

## Bound

**Read in full:** issues #206 and #202 (bodies); `docs/research/principle-interactions.md` (#121); the six reference files in scope (`design-critique/references/brand-palette.md`, `first-visit-trust.md`, `house-principles.md`, `surface-styling.md`, `text-presentation.md`; `design-round/references/impeccable.md`); Google Fonts Knowledge lessons (nine, listed in S3, from the `google/fonts` repo source); Apple HIG Typography (JSON, all tables); Material 3 typography tokens (`material-components-android` tokens.xml); CSS Fonts 4 §8.1; CSS Text 4 §5.4; WCAG 2.2 Understanding 1.4.3 and 1.4.8 (through the fetch tool's summary, with quotes); APCA `apca-w3@0.1.9` font lookup code; Dyson 2004 (PDF text); Butterick's line-spacing, line-length, point-size and letterspacing pages.

**Sampled (grep or part read):** `docs/research/text-presentation.md` (#123, grep for type terms and lines 3-347 around the hits); `docs/research/house-audit-visual.md`, `house-audit-craft.md`, `house-audit-constants.md` (grep); `design-critique/SKILL.md:60-70`; `gate.md:198-266` (grep); `check-access.py` and `check-measure.py` (grep).

**Abstract only:** Legge and Bigelow 2011; Legge et al. 1987, 1990, 1997; Chung 2002; Zorzi 2012; Pelli and Tillman 2008; Rosenholtz 2007. CSS Fonts 5 `font-size-adjust` (fetch tool summary with quotes).

**Second-hand (search results or a summary):** CHI 2023 grade study (Readability Matters summary; ACM 403); simultaneous contrast and Kirschmann's laws; Helmholtz-Kohlrausch effect; Dyson and Haselgrove 2001 and Dyson and Kipping 1998 (through Dyson 2004); APCA author's x-height method (GitHub discussion #28, fetch summary); Inter v3 formula (archived page, fetch summary).

**From knowledge, not verified today:** Duncan and Humphreys 1989's finding; Inter 4.0's `opsz` axis; browser support dates for `font-size-adjust` and `text-wrap`.

**Not opened:** Bringhurst's book (only the 2.2.1 rule title, through webtypography.net; its list of factors needing more lead was not verified, so it is not cited); the Material blog "Adjusting Grade for Mode" (m3.material.io failed); m3.material.io type-scale pages (script-rendered; the token file used instead); Szafir 2018 (cited through #178 only).

**Measured by me:** font metrics of Quicksand and Nunito Sans (`/tmp/r206scripts/metrics.py`); angular x-heights at the CSS reference pixel; Inter v3 tracking at five sizes; leading ratios from the Apple and Material tables.

**Not done:** no render test of any interaction; no clutter measure run on a page; no check of whether a gate script could read a face profile at run time. The rule count in Part 1 rests on my reading of "a rule with a value"; a second reader may split rows 6, 10 and 32 differently (±3).
