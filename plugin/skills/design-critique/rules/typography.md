# Rule records: typography

Typefaces and type settings: sizes, weights, line height, line length and font loading. The form is [rules.md](../rules.md)'s.

### vault.measure
- applies-when: web-surface; every full line of running text, at every width the page's breakpoints make
- question: Does every full line of running text hold 50–75 characters, spaces included, counted as the page sets them rather than worked out from a CSS width?
- answered-by: type
- writes: measure
- yields-to: level 2
- source: Baymard Institute, "Readability: The Optimal Line Length" (2022), 50–75 for body text; WCAG 2.2 SC 1.4.8 Visual Presentation (AAA), 80 at most; strength: expert guidance under a WCAG 2.2 AAA ceiling
- era: timeless
- owner: vault
- stage: value
- reasons: design-round/references/impeccable.md#conditions-added
- ledger: LAY-46, LAY-50, TYS-41
- status: live

### vault.body-size
- applies-when: web-surface; body text, and all text at phone widths
- question: Is body text 16 px or larger, smaller only in a dense role that justifies it, and is text at phone widths 16 px or larger?
- answered-by: type
- writes: body size
- yields-to: level 2
- source: Butterick, Practical Typography, 15–25 px; IBM Carbon's productive and expressive type sets; strength: expert craft range
- era: timeless
- owner: vault
- stage: value
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: FRM-77, TYS-7, TYS-8, TYS-9, TYS-41
- status: live

### vault.dna-caps-label
- applies-when: web-surface; every label of under one line set in capitals, on a project that takes the House DNA
- question: Was each label the candidate sets in capitals asked for by the brief or the rules file?
- answered-by: type
- writes: label case
- yields-to: level 2
- source: House DNA `never` line 7, from Anthropic `frontend-design` SKILL.md (anthropics/skills 41bbe19, 3 Sep 2026), "Using all caps for labels"; Butterick, Practical Typography, capitals for short strings; Arditi and Cho 2007, Vision Research 47(19):2499–2505, on reading speed in capitals; strength: model maker's AI-look calibration for the tell, published research for the reading cost
- era: dated 2027-04-14
- owner: vault
- stage: treatment
- target: Leave labels in their written case unless the brief or the rules file asks for capitals; keep any label in capitals under one line.
- reasons: design-critique/references/text-presentation.md#capitals-on-labels-and-the-house-dna
- ledger: none
- status: live

### vault.leading
- applies-when: web-surface; body text
- question: Does body text take a line height of 1.3 or more that opens up as its line lengthens, with only headings and display type set tighter?
- answered-by: type
- writes: line height
- yields-to: vault.dark-text-weight, level 2
- source: Butterick, Practical Typography, 120–145% for most text and leading set by line length; strength: expert craft range
- era: timeless
- owner: vault
- stage: value
- inputs: the text's role (body, heading, display), its measure in characters
- output: body 1.3 or more, higher as the measure lengthens toward 75; headings and display may run under 1.3
- reasons: design-round/references/impeccable.md#conditions-added
- ledger: TYS-39, TYS-40, TYS-41, TYS-42
- status: live

### vault.heading-step
- applies-when: web-surface; every heading against the body text below it
- question: Does each heading stand apart from its body text by a step in size, weight, space or tone, any one of them carrying the step on its own?
- answered-by: type
- writes: heading step
- yields-to: level 2
- source: IBM Carbon type sets, where `heading-01` and `body-01` share a size; impeccable `typeset`; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Set each heading apart from its body by size, weight, space or tone; a size step under 1.25× is fine where another of these carries it.
- reasons: design-round/references/impeccable.md#conditions-added
- ledger: TYF-68, TYS-19
- status: live

### vault.dark-text-weight
- applies-when: web-surface; light text on a dark ground
- question: Does light text on a dark ground keep its weight at small sizes, large text being free to go one step lighter, while taking the extra line height and tracking impeccable `typeset` gives it?
- answered-by: type
- writes: weight on dark
- yields-to: level 2
- source: Material Design, "Adjusting Grade for Mode" (2022, 184 people; docs/research/house-audit-method.md, override 5); strength: design-system research
- era: timeless
- owner: vault
- stage: treatment
- target: On a dark ground keep small text's weight and add a little line height and tracking; large text may go one weight lighter.
- reasons: design-round/references/impeccable.md#struck-or-corrected
- ledger: TYF-54, TYS-46
- status: live

### vault.font-display
- applies-when: web-surface; every web font the page loads
- question: Does every web font load with `font-display: swap` or `optional`?
- answered-by: whole-page
- writes: font loading
- yields-to: level 2
- source: web.dev font best practices; strength: platform guidance
- era: dated 2027-10-14
- owner: vault
- stage: value
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: TYF-47, TYF-48
- status: live

### vault.heading-space
- applies-when: web-surface; every heading with content above it in its container
- question: Does each heading have at least 1.5 times as much space above it as below it, so it sits nearer the text it introduces?
- answered-by: script
- writes: space above and below a heading
- yields-to: level 2
- source: USWDS Typography, "Use at least 1.5 times the amount of whitespace above the heading as below it" (as read Oct 2026); Butterick, Practical Typography, "Space above and below": headings "relate to the text that follows, not the text before"; NN/g, Harley, "Proximity Principle in Visual Design" (2020); strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Put at least 1.5 times as much space above each heading as below it.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/text-presentation.md#space-above-a-heading
- ledger: LAY-15
- status: staged

### vault.type-size
- applies-when: web-surface; running body text, and text in a dense working role (tables, tool panels)
- question: Is running body text at least 16 px × 0.52 ÷ the body face's x-height, and never under 16 px, and dense-role text at least 14 px × 0.52 ÷ its face's x-height, and never under 14 px?
- answered-by: script
- writes: body size
- yields-to: level 2
- source: Legge and Bigelow 2011, Journal of Vision 11(5):8, critical print size 0.2° of x-height; Google Fonts Knowledge, "The complications of typographic size" (2024), size by x-height; APCA reference x-height 0.52 (Helvetica, Myndex 2021); USWDS typesetting normalization and its 16 px effective body (as read Oct 2026); MDN `font-size-adjust`, Baseline July 2024; x-heights measured Oct 2026 (docs/research/typeface-traits.md R5); strength: peer-reviewed review and design-system guidance, the 0.52 reference and the up-only clamp the house's derivation from them
- era: dated 2027-10-16
- owner: vault
- stage: value
- inputs: the face's x-height (face-profile.py `xheight`), the text's role (running text or a dense working role)
- output: running text max(16, 16 × 0.52 ÷ xheight) px, rounded; dense role max(14, 14 × 0.52 ÷ xheight) px, rounded, never under `vault.type-floor`; a fallback face matched to the primary by `font-size-adjust: from-font` on the primary
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#size-from-x-height
- ledger: TYS-7, TYS-10, TYF-19
- status: staged

### vault.type-floor
- applies-when: web-surface; fine print, captions, helper text and short labels of one to three words
- question: Is fine print, caption and helper text at least 12 px × 0.52 ÷ its face's x-height, a short label at least 11 px × 0.52 ÷ its face's x-height?
- answered-by: script
- writes: smallest text size
- yields-to: level 2
- source: Apple HIG Typography, iOS minimum 11 pt and thin weights "larger than the recommended sizes" (change log 16 Dec 2025); Material 3 type scale tokens, Label Small 11 sp, Body Small 12 sp (6 Mar 2026); Atlassian typography, 12 px the smallest token, for fine print (as read Oct 2026); GOV.UK Frontend v6.0.0, 16 px smallest (9 Feb 2026); strength: design-system guidance
- era: dated 2027-10-16
- owner: vault
- stage: value
- inputs: the face's x-height (face-profile.py `xheight`) and stem, the text's role
- output: fine print, captions, helper text max(12, 12 × 0.52 ÷ xheight) px rounded up; short labels max(11, 11 × 0.52 ÷ xheight) px with the positive tracking `vault.type-tracking` gives; a face whose stem is under 0.06 em, thinner than a regular text weight draws, 1 px larger (the house's reading of Apple's "larger than the recommended sizes", a first guess, not measured); a public-service surface 16 px
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#size-from-x-height
- ledger: TYS-8
- status: staged

### vault.type-weight
- applies-when: web-surface; all text, and light text on a dark ground
- question: Is text at body size and under weight 400 or more, black and ultra weights (800–900) kept to display sizes, and does light text on a dark ground under 24 px (18.66 px bold) keep its light-ground weight?
- answered-by: script
- writes: font weight
- yields-to: level 2
- source: Apple HIG Typography, avoid Ultralight, Thin and Light "especially when text is small" (16 Dec 2025); WCAG 2.2 Understanding 1.4.3, thin fonts render "much fainter" (2023); Material 3 typography, Editorial treatments, weight and grade (28 Aug 2026); Palmén, Gilbert and Crossland, CHI 2023, 459 readers, grade changed without loss of fluency; Material Design, "Adjusting Grade for Mode" (2022, 184 readers); Argyle, web.dev 2023 and nerdy.dev 2025, GRAD −25 to −50 on dark; Butterick, black and ultra for headlines; Refactoring UI, no weight under 400 for UI; Butterick, "Responsive web design", serving Windows a heavier body weight than Mac by script, read Oct 2026 as the counter-view; strength: design-system guidance and published studies, the size split at WCAG's large-text sizes the house's mapping
- era: dated 2027-10-16
- owner: vault
- stage: value
- inputs: the text's size, its computed weight (face-profile.py `weight`), the face's GRAD axis (`axes`), the ground's polarity
- output: at body size and under, weight 400 or more and 700 or less at 14 px and under; 300 only from 18 px in a face drawing 300 as a text weight; 800–900 at display sizes alone; on a dark ground under 24 px (18.66 px bold) the light-ground weight; at or above it, GRAD −25 to −50 where the face has it, else wght −50, as a look choice; one weight on every platform, the 400 floor absorbing a lighter rendering, with no per-platform weight swap
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#weight-by-size-and-ground
- ledger: TYF-13, TYF-54, TYF-55
- status: staged

### vault.type-leading
- applies-when: web-surface; running text, short UI copy, headings and display text, on light and dark grounds
- question: Does each text take the line height its role, size, face and measure give, the same on a dark ground as on a light one, and never under 1.3 for running text?
- answered-by: script
- writes: line height
- yields-to: level 2
- source: Material 3 typography, body about 1.5 and headings 1.2, and type scale tokens (28 Aug 2026; tokens 6 Mar 2026); USWDS line-height guidance and tokens (as read Oct 2026); IBM Carbon type sets, long and short body (30 Jul 2026); Google Fonts Knowledge, line height by x-height, size and measure; Butterick, "fonts that run small will need less line spacing"; Latin, Better Web Typography (2019, 2023); Typography Handbook, +0.1 per 10 characters past 65 (2026); Refactoring UI, 1.5 narrow to 2 wide; WCAG 2.2 SC 1.4.8 and 1.4.12; Apple HIG Typography, tight leading for a height-limited list row but "avoid tight leading" for three or more lines (16 Dec 2025); USWDS line-height token 1 for text "not meant to break over a line" and token 3 (1.35) for captions and text under a paragraph (as read Oct 2026); web.dev, Learn Design, "Internationalization", line height that accommodates diacritics (2021); Latin, "8 more tips", tip 8, more line height for long compound words (Sep 2023); strength: design-system guidance, the measure step from expert writing
- era: dated 2027-10-16
- owner: vault
- stage: value
- inputs: the text's role and size, the face's x-height (face-profile.py `xheight`), the measure in characters (check-measure.py), the number of lines, the text's language and script (`lang`)
- output: running text 1.4–1.6 at 45–65 characters, 1.5 at a middling x-height; past 65 plus 0.01 a character up to +0.1; under 45 down toward 1.3; never under 1.3; short UI copy of one or two lines and captions or text under a paragraph 1.3–1.43, 1.35 at a middling x-height; text set to stay on one line (a button, a nav item, a one-line list row) 1.0–1.25, a height-limited row of two lines at the band's lower end and of three or more never under its band; headings 20 px and under 1.25–1.4, 24–40 px 1.15–1.3, 48 px and over 1.0–1.15, 72 px and over 0.9–1.05, the upper end from three lines; within a band, x-height 0.53 or more the upper half and 0.49 or less the lower; text in a script with stacked diacritics or tall glyphs (Vietnamese, Thai, Devanagari) or a language of long compound words (German) the band's top, through a `:lang()` rule; unchanged by the ground's polarity
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#line-height-by-role-face-and-measure
- ledger: TYS-11, TYS-39, TYS-40, TYS-41, TYS-42, TYS-45, TYS-48, TYS-50
- status: staged

### vault.type-tracking
- applies-when: web-surface; all text, headings and capitals included
- question: Does each text's letter-spacing follow its face's own size curve where the maker publishes one, else USWDS's, with capitals, acronyms and long strings of digits opened 0.05–0.10 em, no negative tracking where an optical size or display cut is active or the face is bold or condensed, and nothing tighter than −0.03 em?
- answered-by: script
- writes: letter spacing
- yields-to: level 2
- source: Apple HIG Typography tracking tables (16 Dec 2025); Material 3 type scale tokens (6 Mar 2026); IBM Carbon type tokens for Plex (30 Jul 2026); Inter v3 dynamic metrics and Inter 4.0's opsz axis (20 Nov 2023); USWDS letterspacing guidance and tokens (as read Oct 2026); Butterick and Bringhurst via Rutter, capitals 5–12% and lowercase bold condensed; Rutter, Web Typography 2.1.6, Bringhurst, letterspace "all long strings of digits" such as serial numbers (as read Oct 2026); Material 3, "heavier fonts may require wider letter spacing"; strength: type makers' and design-system guidance
- era: dated 2027-10-16
- owner: vault
- stage: value
- inputs: the text's size and case, the face's published curve if any, its opsz in use, weight and stretch (face-profile.py `opsz`, `weight`, `stretch`)
- output: the maker's curve; else 12 px and under +0.025 em, 13–21 px 0, 22–31 px −0.01, 32–63 px −0.02, 64 px and over −0.03; capitals, small capitals, acronyms and long digit strings (serials, references) +0.05 to +0.10 em; short labels the upper end; no negative value where opsz or a display cut is active, or at weight 700 and over, or in a condensed width; floor −0.03 em
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#tracking-by-size-and-face
- ledger: TYS-61, TYS-62, TYS-63, TYS-64, TYS-65, TYS-66, TYS-67
- status: staged

### vault.type-axes
- applies-when: web-surface; every web font the page loads
- question: Does the page load a variable file only where it uses three or more weights, an in-between weight, or a grade or width axis, add opsz only where one face runs at text and display sizes?
- answered-by: script
- writes: font files and axes
- yields-to: vault.axis-properties, level 2
- source: HTTP Archive Web Almanac 2024 and 2025, Fonts, manual opsz "out-dated advice"; MDN Variable fonts guide (27 Feb 2026), `font-optical-sizing` (17 Sep 2026) and `font-variation-settings` (10 Sep 2026); CSS Fonts 4 §8.1 (13 Sep 2026); Google Fonts Knowledge, opsz adds 1.2–2.6× to the file; woff2 bytes measured Oct 2026 (docs/research/typeface-traits.md R21); strength: platform documentation and a crawl measurement
- era: dated 2027-10-16
- owner: vault
- stage: treatment
- target: Load static files for one or two weights and a variable file from three; add opsz only for a face used at both text and display sizes; leave optical sizing on auto; set weight, width and optical size by their own properties and keep `font-variation-settings` for grade and custom axes, driven by custom properties.
- script: check-load.py <page> --files --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#variable-fonts-and-axes
- ledger: TYF-14, TYF-15, TYF-51, TYF-52, TYF-53
- status: live

### vault.axis-properties
- applies-when: web-surface; every web font the page loads
- question: Is `font-optical-sizing` left on auto, and are weight, width, slant, italic and optical size set by their own properties, never in `font-variation-settings`?
- answered-by: script
- writes: font axes
- yields-to: none
- source: HTTP Archive Web Almanac 2024 and 2025, Fonts, manual opsz "out-dated advice"; MDN Variable fonts guide (27 Feb 2026), `font-optical-sizing` (17 Sep 2026) and `font-variation-settings` (10 Sep 2026); CSS Fonts 4 §8.1 (13 Sep 2026); strength: platform documentation and a crawl measurement
- era: dated 2027-10-16
- owner: vault
- stage: treatment
- target: Leave optical sizing on auto; set weight, width and optical size by their own properties and keep `font-variation-settings` for grade and custom axes.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#variable-fonts-and-axes
- ledger: TYF-15, TYF-52, TYF-53
- status: live

### vault.type-width
- applies-when: web-surface; every face with a width axis or width cuts
- question: Is a narrow width kept to labels and dense cells, no condensed width in text read at a glance, and a wide width only in short headings and pull quotes with room for it?
- answered-by: look
- writes: font width
- yields-to: vault.prose-width, level 2
- source: Material 3 typography, Editorial treatments, width (28 Aug 2026); Google Fonts Knowledge, "Exploring width in type" and "How type influences readability" (2025); strength: design-system guidance
- era: dated 2027-10-16
- owner: vault
- stage: treatment
- target: Set body text at normal width; use a narrow width for labels and dense cells, a wide one for a short heading with room; keep text read at a glance out of condensed widths.
- reasons: design-critique/references/typeface-traits.md#width-by-role
- ledger: NEW2-15
- status: staged

### vault.prose-width
- applies-when: web-surface; running text
- question: Is running text set at the face's normal width (`font-stretch: 100%`)?
- answered-by: script
- writes: body font width
- yields-to: none
- source: Material 3 typography, Editorial treatments, width (28 Aug 2026); Google Fonts Knowledge, "Exploring width in type" and "How type influences readability" (2025); strength: design-system guidance
- era: dated 2027-10-16
- owner: vault
- stage: treatment
- target: Set body text at the face's normal width.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#width-by-role
- ledger: NEW2-15
- status: staged

### vault.code-size
- applies-when: web-surface; inline code, keyboard and sample text inside running text
- question: Is inline code sized so its x-height matches the surrounding text's, body size × the body face's x-height ÷ the code face's, within 3% (a guessed tolerance, not measured)?
- answered-by: script
- writes: inline code size
- yields-to: level 2
- source: Latin, "8 more tips for remarkably better typography" (23 Sep 2023), JetBrains Mono 12 px in 14 px Meta Serif; Atlassian typography, inline code 0.875 em (as read Oct 2026); MDN `font-size-adjust`, Baseline July 2024; x-heights measured Oct 2026 (docs/research/typeface-traits.md R5); strength: expert and design-system practice, the x-height match measured
- era: dated 2027-10-16
- owner: vault
- stage: value
- inputs: the body face's and the code face's x-heights (face-profile.py `xheight`)
- output: code size = body size × body xheight ÷ code xheight, in em, or `font-size-adjust` on the code set to the body face's x-height; a padded code box raises its line's height
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#inline-code-beside-body-text
- ledger: TYS-13
- status: staged

### vault.emphasis-cues
- applies-when: web-surface; any text ranked above or below the text around it: a key figure, an emphasised phrase, metadata, secondary lines, and the text styles of each view
- question: Is text ranked first by weight and a colour step and by size only in small steps (a key figure in a tile or chart free to take a display size), does each emphasised run take one cue, de-emphasised text never both a lighter colour and a size under the body floor?
- answered-by: type
- writes: emphasis cues
- yields-to: vault.emphasis-cue, vault.text-steps, vault.heading-step, level 2
- source: Atlassian, Applying typography, "Use text styles and font weights to draw attention … Use text size and color to differentiate between primary and secondary level content", and metric styles for a number in tiles (as read Oct 2026); Butterick, Practical Typography, "Point size", "use the subtlety that point-size adjustments offer … Start with a smaller increase"; NN/g, "Low-Contrast Text" (2015), size, position and padding before low contrast; NN/g, Gordon, "Visual Hierarchy in UX: Definition" (2021), "Use no more than 3 contrast variations for complex designs"; Butterick, Practical Typography, "Bold or italic", "if everything is emphasized, then nothing is emphasized"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Rank text by weight and a second colour first, then by small size steps; let a key figure in a tile take a display size; give emphasised text one cue, and never make text both lighter and smaller than body text; keep each view to three levels of text contrast.
- reasons: design-critique/references/text-presentation.md#ranking-text
- ledger: TXL-85, TYS-26, TYS-27
- status: live

### vault.emphasis-cue
- applies-when: web-surface; any text ranked above or below the text around it: a key figure, an emphasised phrase, metadata, secondary lines, and the text styles of each view
- question: Does emphasised text keep its surrounding text's size and colour, and does each ground hold three levels of text contrast at most?
- answered-by: script
- writes: emphasis cues
- yields-to: none
- source: Atlassian, Applying typography, "Use text styles and font weights to draw attention … Use text size and color to differentiate between primary and secondary level content", and metric styles for a number in tiles (as read Oct 2026); Butterick, Practical Typography, "Point size", "use the subtlety that point-size adjustments offer … Start with a smaller increase"; NN/g, "Low-Contrast Text" (2015), size, position and padding before low contrast; NN/g, Gordon, "Visual Hierarchy in UX: Definition" (2021), "Use no more than 3 contrast variations for complex designs"; Butterick, Practical Typography, "Bold or italic", "if everything is emphasized, then nothing is emphasized"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Give emphasised text one cue, weight or slant, at its surroundings' size and colour; keep each view to three levels of text contrast.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/text-presentation.md#ranking-text
- ledger: TXL-85, TYS-26, TYS-27
- status: live

### vault.weight-count
- applies-when: web-surface; all text on the page
- question: Does the page's text use two to four weights, a regular for body text and a heavier weight at 600–700 for emphasis and headings, with any third or fourth weight held to a named job such as text beside icons or display type?
- answered-by: script
- writes: weight set
- yields-to: vault.type-weight, level 2
- source: Atlassian, Applying typography, four weights, bold "sparingly", semibold "with caution" (as read Oct 2026); USWDS Font weight, "Most projects will use only 2-4 of these tokens"; GOV.UK font override classes, regular and bold only; Google Fonts Knowledge, semibold too weak for emphasis; strength: design-system guidance
- era: timeless
- owner: vault
- stage: value
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#how-many-weights
- ledger: TYF-14
- status: staged

### vault.glyph-distinct
- applies-when: web-surface; every face that sets text
- question: Does each face that sets text draw I, l and 1 as three distinct shapes?
- answered-by: script
- writes: glyph distinctness
- yields-to: level 2
- source: web.dev, Learn Accessibility, Typography, "every letter and number must be clearly defined … Common readability offenders are the uppercase I (India), lowercase l (lettuce), and the number 1" (2022); Atlassian, Product typefaces, upper-case I with serif "Use always", slashed zero "To be used selectively with data points" (as read Oct 2026); strength: platform guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Pick a text face whose I, l and 1 differ.
- script: check-load.py <page> --files --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#telling-characters-apart
- ledger: TYF-16
- status: live

### vault.zero-distinct
- applies-when: web-surface; text holding codes, references or data a visitor reads character by character, copies or types
- question: Is 0 told from O in that text by a slashed or dotted zero or a clearly different shape?
- answered-by: type
- writes: zero distinctness
- yields-to: vault.glyph-distinct, level 2
- source: web.dev, Learn Accessibility, Typography, "every letter and number must be clearly defined … Common readability offenders are the uppercase I (India), lowercase l (lettuce), and the number 1" (2022); Atlassian, Product typefaces, upper-case I with serif "Use always", slashed zero "To be used selectively with data points" (as read Oct 2026); strength: platform guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Set codes and references with a slashed zero (`font-variant-numeric: slashed-zero`) where the face has one.
- reasons: design-critique/references/typeface-traits.md#telling-characters-apart
- ledger: TYF-16
- status: live

### vault.figure-face
- applies-when: web-surface; a face that sets numbers compared down a column or list, or updating in place
- question: Does the face that sets compared or updating numbers have tabular figures, by default or by `tnum`?
- answered-by: script
- writes: face for numbers
- yields-to: level 2
- source: Butterick, Practical Typography, "Grids of numbers", figures "will only line up with each other if they're tabular figures"; GOV.UK font override classes, Tabular numbers, for comparison and counters (as read Oct 2026); Atlassian, Product typefaces, tabular figures "For use in tables and lists"; strength: expert craft range and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Before compared numbers go in a face, check it has tabular figures; if not, set them in the body face or a monospace face that has them.
- script: check-load.py <page> --files --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#figures
- ledger: TYF-20, TYF-24, TYF-40
- status: live

### vault.figures
- applies-when: web-surface; every number in text
- question: Do numbers compared down a column, row or list or updating in place take tabular lining figures, numbers in running text proportional figures, and numbers beside or in capitals lining figures, never old-style?
- answered-by: script
- writes: figure style
- yields-to: level 2
- source: Butterick, Practical Typography, "Alternate figures", tabular "essential for one purpose: vertically aligned columns", proportional "preferred" in body text, lining "always preferred for all caps text", and "Grids of numbers", lining in a grid; GOV.UK Tabular numbers (as read Oct 2026); USWDS Table, monospace for amounts (as read Oct 2026); MDN `font-variant-numeric`, Baseline January 2020; strength: expert craft range and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- inputs: where the number sits (a column, table or list compared down; a value updating in place; running text; beside or in capitals); the face's `tnum`, `lnum`, `pnum` and `onum`
- output: compared or updating: `tabular-nums lining-nums`; running text: proportional (the face's default if proportional); beside or in capitals: lining; old-style only in lowercase running text; a face with no `tnum`: `vault.figure-face`
- target: Set compared and updating numbers with `font-variant-numeric: tabular-nums lining-nums`, numbers in sentences proportional, and lining figures beside capitals.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#figures
- ledger: TYF-24, TYF-40, TYF-41, TYF-43, TYF-44
- status: staged

### vault.font-features
- applies-when: web-surface; every OpenType feature the page switches on
- question: Is each OpenType feature switched on by its `font-variant-*` property where one exists, `font-feature-settings` kept for features with none, only where the font file has the glyphs, and set after any `font` shorthand in the same rule?
- answered-by: script
- writes: OpenType features
- yields-to: level 2
- source: MDN `font-feature-settings`, "Whenever possible, Web authors should instead use the font-variant shorthand property or an associated longhand" (20 Apr 2026); MDN `font`, the shorthand "resets … font-feature-settings … font-variant-numeric" to initial values (17 Sep 2026); MDN `font-variant-numeric`, Baseline January 2020 (10 Sep 2026); Butterick, "OpenType features", usable only where "supported by both the font and the application"; strength: platform guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Switch features on with `font-variant-numeric`, `-caps` and `-ligatures`, falling back to `font-feature-settings` only where no property exists; check the font has the glyphs; set them after any `font` shorthand.
- script: check-load.py <page> --files --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#opentype-features
- ledger: TYF-36
- status: live

### vault.font-smoothing
- applies-when: web-surface; any `-webkit-font-smoothing` or `-moz-osx-font-smoothing` rule
- question: Is greyscale smoothing (`antialiased`, `grayscale`) set on light text on dark grounds, set site-wide only where the rules file picks it, and never used to make light-weight text on a light ground look thinner?
- answered-by: script
- writes: font smoothing
- yields-to: level 2
- source: MDN `font-smooth`, non-standard, macOS only, greyscale "for light text on dark backgrounds makes it look lighter" (20 Apr 2026); Latin, "5 keys to accessible web typography" (2019), "makes most sense for light text on a dark background … Don't misuse it just to make the text lighter"; Comeau, "A Modern CSS Reset" (3 Jun 2026), macOS Chrome and Safari "still use subpixel antialiasing by default", so site-wide; strength: platform guidance and practitioner writing
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Set `-webkit-font-smoothing: antialiased` and `-moz-osx-font-smoothing: grayscale` on dark grounds; set them site-wide only if the rules file says so; never to lighten thin text on light.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#font-smoothing
- ledger: NEW1-8
- status: live

### vault.face-roles
- applies-when: web-surface; every typeface the page loads
- question: Does each typeface hold one job kept across the site (body, headings or display, interface, code), a monospace face setting only code, sample text and the compared numbers `vault.figure-face` sends it, with an app's working surfaces in its interface face and a brand or display face kept to marketing and editorial surfaces?
- answered-by: type
- writes: typeface per text role
- yields-to: vault.face-count, vault.brand-layer, level 2
- source: Butterick, "Mixing fonts" (as read Oct 2026): "Most documents can tolerate a second font. Few can tolerate a third", "Font mixing is most successful when each font has a consistent role"; Butterick, "Monospaced fonts": code "is more legible when set in a monospaced font"; Apple HIG, Typography (as read Nov 2026): "Minimize the number of typefaces you use, even in a highly customized interface"; USWDS font-family role tokens "heading, body, ui, code, and alternate"; Atlassian Typography: Charlie Sans "such as in marketing", Atlassian Sans and Mono "For all in-app experiences"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Give each face one job across the site, body, headings, interface or code; use two families at most plus a monospace for code alone; set an app's working screens in the interface face and keep a brand or display face to marketing and editorial pages.
- reasons: design-critique/references/typeface-traits.md#one-job-per-face
- ledger: TYF-1, TYF-2, TYF-5, TYF-22
- status: live

### vault.face-count
- applies-when: web-surface; every typeface the page loads
- question: Does the page set its text in two families at most besides a monospace face, headings in one and running text in one, and its code, keys and sample output in a monospace face?
- answered-by: script
- writes: typeface count
- yields-to: none
- source: Butterick, "Mixing fonts" (as read Oct 2026): "Most documents can tolerate a second font. Few can tolerate a third", "Font mixing is most successful when each font has a consistent role"; Butterick, "Monospaced fonts": code "is more legible when set in a monospaced font"; Apple HIG, Typography (as read Nov 2026): "Minimize the number of typefaces you use, even in a highly customized interface"; USWDS font-family role tokens "heading, body, ui, code, and alternate"; Atlassian Typography: Charlie Sans "such as in marketing", Atlassian Sans and Mono "For all in-app experiences"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Use two families at most, one for headings and one for running text, plus a monospace for code alone.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#one-job-per-face
- ledger: TYF-1, TYF-2, TYF-22
- status: live

### vault.fluid-type
- applies-when: web-surface; every font size that changes with the viewport width
- question: Is every font size that scales with the viewport a `clamp()` whose bounds are in `rem` and whose preferred value mixes `rem` with `vw`, never `vw` alone?
- answered-by: script
- writes: fluid font size
- yields-to: none
- source: WCAG 2.2 success criterion 1.4.4 Resize Text and failure F94 (updated 9 Mar 2026, as read Oct 2026): viewport units on text "cannot be resized by zooming or adjusting text-size"; MDN `clamp()` (modified 12 Aug 2026): a clamped font size grows with the viewport between its bounds, the maximum a relative length "no less than twice the minimum" so text "can scale to at least 200%"; web.dev Learn Design, "Typography": "don't use the vw by itself in a font-size declaration", the minimum "1rem so as to not go below the user's preferred font size"; strength: WCAG 2.2 AA
- era: dated 2027-10-19
- owner: vault
- stage: value
- inputs: each text element's computed font size at a width W and 100% zoom, and at 200% zoom (a viewport of W ÷ 2 CSS px, the root size doubled)
- output: pass where the 200% size is at least 2 × the 100% size for every element; stepped sizes in `rem` pass by construction
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#fluid-size
- ledger: TYS-5
- status: staged

### vault.glyph-coverage
- applies-when: web-surface; all text, in every language and script the page carries
- question: Does the first family in each text's font stack hold a glyph for every character that text sets, no character falling through to a later family or to the browser's installed-font fallback save where the stack names a family for that script or for emoji on purpose?
- answered-by: script
- writes: glyph coverage
- yields-to: level 2
- source: CSS Fonts Level 4 §5.2 (W3C Working Draft 16 Oct 2026): a family whose face lacks a glyph for a character passes it to the next family, "Glyphs from other faces in the family are not considered", and past the list the installed-font fallback "can vary across user agents"; web.dev, Learn Design, "Internationalization" (2021): choose a face with "a range of characters broad enough to cover the languages"; strength: web platform standard
- era: timeless
- owner: vault
- stage: value
- script: check-load.py <page> --files --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#a-face-that-covers-the-text
- ledger: TYF-21
- status: staged

### vault.true-faces
- applies-when: web-surface; every weight and style of a web font the page sets
- question: Does every weight and italic the page sets come from a face the page loads, a static file or a variable file whose axes span it, so the browser never draws a synthesised bold or slanted face, with `font-synthesis-weight` and `font-synthesis-style` set to `none` on text in Chinese, Japanese, Korean and other scripts whose fonts lack them?
- answered-by: script
- writes: font synthesis
- yields-to: level 2
- source: CSS Fonts Level 4 §2.8 (16 Oct 2026): synthesis "does not meet the level of quality of a face designed for the purpose", and variable-font axes "do not count as font synthesis"; MDN, Variable fonts, "A note about font families, weights, and variants" (27 Feb 2026): load "the specific font files", since bold and italic designs "often include completely different characters"; MDN `font-synthesis` (27 Aug 2026): for logographic scripts synthesis "might impede the legibility or change the meaning of the text"; web-features `font-synthesis-weight` and `font-synthesis-style`, Baseline 2023, widely available 2025-09-27; strength: web platform standard and documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Load a true face for every weight and italic the page uses, or a variable file whose axes span them; turn synthesis off for CJK text.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#true-bold-and-italic
- ledger: TYF-31
- status: live

### vault.small-caps
- applies-when: web-surface; text set in small capitals: abbreviations in running text, labels
- question: Is small-caps formatting (`font-variant-caps: small-caps` or `all-small-caps`) used only in a face whose files carry `smcp`, and `c2sc` for `all-small-caps`, with `font-synthesis-small-caps: none` on it and no italic small capitals unless the face draws them?
- answered-by: script
- writes: small caps
- yields-to: level 2
- source: CSS Fonts Level 4 §2.8 and §6.6 (16 Oct 2026): synthesis renders "regular glyphs at a smaller size", and a font without small caps gets synthesised ones; Butterick, Practical Typography, "Small caps": fake small caps are "too tall, and their vertical strokes are too light"; Rutter, Web Typography 3.2.2, after Bringhurst, shrunken capitals "will only produce a parody", and few fonts provide italic small caps; Latin, "8 tips for remarkably better typography" (2 Sep 2023), tip 6, "don't use fake small caps"; web-features `font-synthesis-small-caps`, Baseline 2023, widely available 2025-09-27; strength: web platform standard and expert craft agreement
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Set small caps only in a face that draws them, checked in its feature list; where it has none, use full capitals with the tracking `vault.type-tracking` gives, or leave the text in its case.
- script: check-load.py <page> --files --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#true-small-caps
- ledger: TYF-32
- status: live

### vault.kerning
- applies-when: web-surface; all text in a proportionally spaced face
- question: Is the face's kerning left on at every size, `font-kerning` `auto` or `normal`, never `none` and never `text-rendering: optimizeSpeed`, on proportionally spaced text?
- answered-by: script
- writes: kerning
- yields-to: level 2
- source: CSS Fonts Level 4 §6.3 (16 Oct 2026): initial `auto` kerns "at the discretion of the user agent", and "Authors who want proper kerning should use normal"; kerning is "not intended to apply to fixed-width glyphs"; MDN `text-rendering` (20 Apr 2026): `optimizeSpeed` "disables kerning and ligatures"; Butterick, Practical Typography, "Kerning": "Always use kerning"; measured on design-vault#276 (docs/research/platform-defaults.md), Chromium 149 only; strength: web platform standard and a measurement
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Leave kerning on: `font-kerning` at its default or `normal`, never `none` or `optimizeSpeed`; no `text-rendering` value is needed to get it.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#kerning-stays-on
- ledger: TYF-39
- status: live

### vault.fractions
- applies-when: web-surface; fractions set in text: measures, recipes, sizes
- question: Is each fraction set with `font-variant-numeric: diagonal-fractions` on an element holding that fraction alone, in a face whose files carry `frac`?
- answered-by: script
- writes: fraction glyphs
- yields-to: level 2
- source: CSS Fonts Level 4 §6.7 (16 Oct 2026): `diagonal-fractions` enables the OpenType `frac` feature; OpenType 1.9.1 feature registry, `frac`: "Replaces figures (digits) separated by a slash" and "should be off by default"; strength: web platform standard and the font format's registry
- era: timeless
- owner: vault
- stage: treatment
- target: Wrap each fraction in its own element and give it `font-variant-numeric: diagonal-fractions` where the face has `frac`; leave dates and other slashed figures out of it.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#fractions
- ledger: TYF-45
- status: live

### vault.font-stack
- applies-when: web-surface; every `font-family` declaration
- question: Does every font stack end in a generic family of the face's own kind (`serif`, `sans-serif`, `monospace`, or a more specific one such as `system-ui` or `ui-monospace`), with any named fallback before it close to the chosen face in kind and width?
- answered-by: script
- writes: font fallback stack
- yields-to: level 2
- source: CSS Fonts Level 4 §2.1 (16 Oct 2026): "Authors are encouraged to append a generic font family as a last alternative for improved robustness, and to use a more specific generic font family, if applicable"; MDN, Text styling fundamentals, "Font stacks" (27 Aug 2026): with no generic, a sans face falls back to the default serif, "usually Times New Roman"; web.dev, Learn CSS, "Typography": the generic "should be similar to your preferred fonts"; Latin, "Preloading fonts" (2019): a dissimilar fallback made "a jarring transition"; strength: web platform standard
- era: timeless
- owner: vault
- stage: treatment
- target: End every stack with the generic family of the face's kind, and put a close system face before it.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#the-fallback-stack
- ledger: TYF-49
- status: live

### vault.fluid-zoom
- applies-when: web-surface; every text whose size varies with the viewport
- question: At every sweep width, can browser zoom up to 500% bring each viewport-scaled text to twice its size at 100%, its bounds in `rem` or `em` so a raised default text size moves it too?
- answered-by: script
- writes: fluid type bounds
- yields-to: vault.fluid-type
- source: WCAG 2.2 SC 1.4.4 Resize Text, text resizes to 200 percent without loss, and its failure F94, "incorrect use of viewport units to resize text"; MDN, Responsive design, "Using viewport units for responsive typography" (4 Sep 2026): "you should never set text using viewport units alone"; web.dev, "Baseline in action: fluid type" (16 Dec 2025), after Barvian: a maximum at most 2.5 times the minimum passes 1.4.4 in current browsers; strength: WCAG 2.2 AA
- era: dated 2027-10-19
- owner: vault
- stage: value
- inputs: the text's smallest and largest size in `rem`, and the narrowest and widest viewport widths the size grows between
- output: `clamp(<min>rem, <a>rem + <b>vw, <max>rem)`, with `a` and `b` solved so the size is the minimum at the narrowest width and the maximum at the widest, and the maximum no more than 2.5 times the minimum
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/platform-defaults.md#fluid-type-that-still-zooms
- ledger: TYS-6
- status: staged

### vault.leading-unitless
- applies-when: web-surface; every `line-height` declaration on text
- question: Is every `line-height` on text a unitless number or `normal`, none a length or a percentage?
- answered-by: script
- writes: line height unit
- yields-to: level 2
- source: MDN `line-height` (11 Aug 2026): unitless "is the preferred way to set line-height and avoid unexpected results due to inheritance", length and percentage line heights "have poor inheritance behavior", and on zoom a unitless value "ensures that the line height will scale proportionately"; web.dev, Learn Design, "Typography": "Use unitless values for your line-height declarations"; Butterick, Practical Typography, "Line spacing": "preferably without units"; strength: web platform documentation
- era: timeless
- owner: vault
- stage: value
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#line-height-without-units
- ledger: TYS-44
- status: staged

### vault.text-spacing
- applies-when: web-surface; all text in the page's markup, at every width the reflow sweep covers
- question: With line height set to 1.5, spacing after paragraphs to 2, letter spacing to 0.12 and word spacing to 0.16 times the font size on every element, and no other style changed, is no text cut off, overlapping other text or hidden by a box that hides its overflow, save text in a link or beside a control that vault.text-spacing-reveal judges?
- answered-by: script
- writes: text spacing tolerance
- yields-to: none
- source: WCAG 2.2 SC 1.4.12 Text Spacing and its Understanding document (as read Oct 2026): no loss of content or functionality with all four set, content "is not required to use these text spacing values", a language lacking a property conforms with the ones it has, and failure F104, "clipped or overlapped content when text spacing is adjusted"; truncation passes only where the hidden text can be shown; Baymard, "European Accessibility Act 2025" (26 Aug 2025), the same four values; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: value
- script: check-layout.py --text spacing
- reasons: design-critique/references/platform-defaults.md#text-spacing-overrides
- ledger: TYS-53
- status: staged

### vault.text-spacing-reveal
- applies-when: web-surface; each text `check-layout.py --text spacing` lists as hidden in a link or beside a control
- question: Once WCAG 1.4.12's four spacing values are set, can the visitor show the whole of each such text, by the control beside it or on the page its link opens?
- answered-by: look
- writes: revealable truncation
- yields-to: vault.text-spacing
- source: WCAG 2.2 SC 1.4.12 Text Spacing, its Understanding document (as read Nov 2026): truncation passes where "a mechanism is provided to reveal the truncated text on the page" or the full text is on a linked page, and "if there is no mechanism to show the truncated text, it fails"; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: value
- reasons: design-critique/references/platform-defaults.md#text-spacing-overrides
- ledger: TYS-53
- status: staged

### vault.sentence-space
- applies-when: web-surface; running text
- question: Is there one ordinary space between sentences, with no `&nbsp;` or wider Unicode space used to widen it?
- answered-by: script
- writes: sentence spacing
- yields-to: level 2
- source: Butterick, Practical Typography, "One space between sentences": "Always put exactly one space between sentences"; Rutter, Web Typography 2.1.4: HTML whitespace "is automatically collapsed to a single word space", and "Avoid the temptation to use a non-breaking space"; strength: expert craft agreement on a platform default
- era: timeless
- owner: vault
- stage: treatment
- target: Put one plain space between sentences and leave the browser's whitespace collapsing on in prose.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#one-space-between-sentences
- ledger: TYS-70
- status: live

### vault.text-stroke
- applies-when: web-surface; text drawn with an outline stroke (`-webkit-text-stroke`, or SVG `stroke` on text)
- question: Is outlined text drawn with `paint-order: stroke fill`, so the stroke sits behind the fill and the glyph keeps its drawn shape?
- answered-by: script
- writes: stroke order
- yields-to: level 2
- source: MDN `paint-order` (20 Apr 2026): default order fill, stroke, markers, and `paint-order: stroke fill` applies to HTML text with `-webkit-text-stroke`; web-features `paint-order`, Baseline 2024-03-22, widely available 2026-09-22; measured on design-vault#276 (docs/research/platform-defaults.md), Chromium 149 only; strength: web platform documentation and a measurement
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Set `paint-order: stroke fill` on outlined text and double the stroke width to get the outline you want, since half of it now hides behind the fill.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#outlined-text
- ledger: NEW2-49
- status: live

### vault.emphasis-weight
- applies-when: web-surface; bold or semibold emphasis inside running text, and every selected state shown by a weight change
- question: Is each emphasis by weight, and each selected state a weight change shows, at least 300 weight units over the text around it, 400 to 700 and never 400 to 500 or 600?
- answered-by: script
- writes: emphasis weight
- yields-to: vault.type-weight, level 2
- source: Google Fonts Knowledge, "Exploring typefaces with multiple weights or grades": "Avoid using semibold for emphasis in regular text. Use bold or extrabold", as checked on design-vault#282 (docs/research/typeface-traits.md, Oct 2026); Butterick, "Bold or italic" (as read Oct 2026): bold or italic "mutually exclusive", and with a sans serif "skip italic and use bold", semibold allowed; Apple HIG Toggles, "Make sure the visual differences in a toggle's state are obvious" (29 Mar 2024); strength: expert guidance
- era: timeless
- owner: vault
- stage: value
- inputs: the weight of the text around it, the face's weights or wght range
- output: emphasis or selected weight = surrounding weight + 300 or more (400 → 700, 300 → 600), the face's next drawn weight at or past it where the face is static
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#emphasis-takes-bold
- ledger: BTN-74, TYF-58
- status: staged

### vault.fallback-metrics
- applies-when: web-surface; every web font loaded with `font-display: swap` or `fallback`
- question: Does the fallback face the page shows before the web font arrives take the web font's metrics, by an `@font-face` fallback with `size-adjust` (and `ascent-override`, `descent-override`, `line-gap-override` where needed) or by `font-size-adjust`, so the swap shifts no line?
- answered-by: script
- writes: fallback metrics
- yields-to: vault.font-display, level 2
- source: web.dev, Learn Design, "Typography", font loading: "mitigate the jarring effect of text shifting around by using size-adjust in your @font-face rule" (2021); MDN `size-adjust` (Baseline widely available since Sep 2023; page of 20 Apr 2026), "Overriding metrics of a fallback font"; MDN `font-size-adjust` (Baseline 2024, since Jul 2024; page of 16 Sep 2026), "intended for adjusting fallback fonts to have similar metrics as the first-choice font"; strength: web platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: value
- inputs: the web font's metrics (average character width, ascent, descent, line gap), the fallback face's same metrics
- output: `size-adjust` the ratio of the web font's average width to the fallback's; `ascent-override`, `descent-override` and `line-gap-override` the web font's values over that size; or `font-size-adjust` the web font's x-height ratio
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/typeface-traits.md#fallback-faces-match-the-web-font
- ledger: TYF-50
- status: live

### vault.line-length
- applies-when: web-surface; every full line of text set in a paragraph or block: body text, large text above body size (intros, ledes, subheads set as paragraphs), short passages (captions, footnotes, alerts, helper text of three lines or fewer), and each column of multi-column text
- question: At each breakpoint width, does each line that fills its text block, its set characters and spaces tallied, fall within the range its role and column count give?
- answered-by: script
- writes: measure
- yields-to: level 2
- source: Baymard Institute, "Readability: The Optimal Line Length" (May 2022), body text 50–75, fatigue observed at 100+; WCAG 2.2 (2023) Understanding SC 1.4.8 (AAA, updated Sep 2026), "no more than 80 characters or glyphs"; Bringhurst via Rutter, webtypography.net 2.1.2, 45–75 "for a single-column page set in a serifed text face in a text size" and "For multiple column work, a better average is 40 to 50 characters"; Typography Handbook (updated for 2026), "For multi-column layouts, 40–50 CPL per column", and "On narrow viewports, let the measure reduce naturally with the viewport rather than enforcing a minimum"; USWDS Typography and measure tokens (updated May 2024), "Large text can have a shorter measure", measure 1 (about 45 characters) "for larger text (like a subheading or intro text)", and "Short passages can have measure outside the ideal range"; Butterick, Practical Typography, "Responsive web design": "Regardless of screen width, the optimal line length is still 45-90 characters"; strength: domain evidence under a WCAG 2.2 AAA ceiling
- era: timeless
- owner: vault
- stage: value
- inputs: the text's role (body, large, short passage), its column count, whether the column already fills the viewport less its side gutters, the characters on each full line as set (check-measure.py)
- output: body, one column: 50–75; body, one of several columns: 40–50; large text above body size: 75 at most, any shorter length allowed; short passage of three lines or fewer: WCAG's 80 at most, any shorter length allowed; any role whose column already fills the viewport less its gutters: the floor lifts, the ceiling holds
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/alignment-and-width.md#line-length-by-role
- ledger: LAY-46, LAY-47, LAY-48, TYS-56, TYS-60
- status: staged

### vault.measure-unit
- applies-when: web-surface; every text column whose line length the page caps
- question: Is the line length capped by a maximum width in a font-relative unit (rem, em, ex or ch), its value sized by counting the characters the face sets, rather than by a fixed width or a `ch` value taken as a character count?
- answered-by: script
- writes: measure unit
- yields-to: vault.line-length
- source: Butterick, Practical Typography, "Responsive web design": the `ch` unit "simply denotes the width of the zero in the font", "not a useful proxy for average characters per line", and "include a max-width CSS property on that element to ensure that the line length is bounded"; USWDS measure tokens (updated May 2024), measures in `ex`, measure 2 (60ex) for "a good target for long texts", 66 characters; Baymard (2022), "around 70ch or 34em (note that this value will need to be adjusted slightly up or down depending on the font used)"; Every Layout, "Axioms": fixed widths break zoom and cause horizontal scrolling, so cap with `max-inline-size`; Manta's measurement (design-vault docs/research/manta-design-migration.md T4): `68ch` set about 85 characters; strength: expert craft range and design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Cap each text column with `max-inline-size` in rem, em, ex or ch, never a fixed `width` or px; size the value by counting the characters the real font sets (check-measure.py), not by trusting a `ch` value.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/alignment-and-width.md#cap-the-measure-in-a-font-relative-unit
- ledger: TYS-59, TYS-60
- status: live

### vault.tone-face
- applies-when: any; every typeface the asset sets, against the tone the brief or direction card states in its tone line and the text's purpose
- question: Does each typeface fit the stated tone and its text's job, the display face carrying the tone and the body face readable first, chosen for the feel it gives this audience now and then checked for how it works, never for a subject association alone?
- answered-by: whole-page
- writes: typeface fit
- yields-to: vault.brand-layer, level 2
- source: Typography Handbook, "Choosing fonts" (updated for 2026), fonts that complement the tone and system fonts for interfaces; Google Fonts Knowledge, Stocks, "Emotive considerations for choosing typefaces" (as read Oct 2026), feel then function and associations changing over time; IBM Carbon, typography style strategies (Apr 2026), productive and expressive type; impeccable 4.5.0 `new-work.md` §4, subject associations (as read Oct 2026); strength: expert and design-system practice
- era: dated 2027-10-19
- owner: vault
- stage: role
- target: Pick the display face for the feel the tone names for this audience, keep the body face readable first, and test each against its job; never pick a face only because the subject usually gets one.
- reasons: design-critique/references/tone.md#typeface-by-tone
- ledger: TYF-7
- status: live

### vault.table-text-narrow
- applies-when: web-surface; a data table's text at phone width
- question: At phone width, does a table with a lot of data fit more by either a smaller size or a condensed width, never both, its size never under the dense role's from `vault.type-size` or `vault.type-floor`, while a table with little data keeps its usual size?
- answered-by: script
- writes: table text size and width at narrow widths
- yields-to: vault.type-size, vault.type-floor, level 2
- source: Rutter, Web Typography (2017), "Adapt tables to small screens" p. 139: "use either a condensed font or a slightly smaller size (but not both smaller and condensed)"; GOV.UK Design System, Table (changed Feb 2024), "Tables with a lot of data": `govuk-table--small-text-until-tablet` "reduces the size of the text on small screens", and "You should not use this class on tables unless your table has a lot of data"; strength: expert and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- inputs: the viewport width, whether the table at its usual size is wider than the viewport, the dense role's size from `vault.type-size`
- output: below GOV.UK's tablet width and wider than the viewport at its usual size: either the dense role's size or a condensed width (`vault.type-width`), not both, never under `vault.type-floor`; otherwise the table's usual size and width
- target: On a phone, set a data-heavy table one step smaller (at the dense size) or in a condensed width, not both; leave a light table at its usual size.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: table
- reasons: design-critique/references/responsive-structure.md#table-text-on-a-phone
- ledger: TYS-37
- status: staged

### vault.caps-extent
- applies-when: web-surface; every text shown in capitals, by `text-transform`, `font-variant-caps` or as typed
- question: Is each text in capitals a short label of at most four words on one line (an eyebrow, a column or section header, a caption label, an acronym), never a sentence, a paragraph, a body passage or a button or tag label that runs past a few words?
- answered-by: script
- writes: extent of capitals
- yields-to: vault.dna-caps-label, level 2
- source: Butterick, "All caps" (as read Nov 2026): "Fine for less than one line"; caps "are suitable for headings shorter than one line … headers, footers, captions, or other labels"; USWDS Typography (as read Nov 2026): "consider other type treatments for any uppercase text longer than just a few words"; Atlassian, Applying typography (as read Nov 2026): "avoid the use of all caps unless text is an acronym"; GOV.UK style guide, Capitalisation: "DO NOT USE BLOCK CAPITALS FOR LARGE AMOUNTS OF TEXT"; Latin, "8 tips for remarkably better typography" (2 Sep 2023), tip 4: "It's ok to use uppercase in small amounts", letter-spaced; Arditi and Cho 2007, Vision Research 47(19):2499–2505 (abstract, PMC2016788): capitals read faster than mixed case at twice acuity size, the advantage gone at larger sizes; impeccable detector rule `all-caps-body`; strength: expert craft and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Keep capitals to short one-line labels of a few words, eyebrows, column headers and acronyms; set every sentence, paragraph and longer button or tag label in its normal case.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/text-presentation.md#how-much-in-capitals
- ledger: TXL-98, BTN-51
- status: staged

### vault.text-style-count
- applies-when: web-surface; all visible text on the page
- question: Is every text style on the page (its face, size, weight and colour together) one of the site's named type-scale styles, with no one-off combination outside the scale and the lead or display sizes held to at most two elements a view?
- answered-by: script
- writes: text style set
- yields-to: vault.face-roles, vault.weight-count, vault.text-steps, vault.heading-step, level 2
- source: Apple HIG, Typography (alert date 16 Dec 2025), "Minimize the number of typefaces" and use the built-in text styles; GOV.UK Design System styles (as read Nov 2026), a fixed type scale, bold "sparingly", the lead paragraph "only use it once per page"; USWDS Typography (2024), other sizes "sparingly"; NN/g, Gordon, "Visual Hierarchy in UX" (2021), "Use no more than 3 sizes" and "Limit how many elements are big to a maximum of 2"; NN/g, Nielsen, homepage guideline 63 (2001), "Limit font styles and other text formatting"; Polaris, Using type (2024), the same body size everywhere hides key elements; strength: design-system and expert guidance, no study sets a count
- era: timeless
- owner: vault
- stage: value
- script: owed
- reasons: design-critique/references/busyness.md#text-styles
- ledger: NEW1-7
- status: staged
