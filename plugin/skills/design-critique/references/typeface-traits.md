# Typeface traits

Why type size, weight, line height, tracking, axes and width follow the face rather than a fixed number, and how faces, figures, features and smoothing are chosen (#282, #275). The records are `vault.type-size`, `vault.type-floor`, `vault.type-weight`, `vault.type-leading`, `vault.type-tracking`, `vault.type-axes`, `vault.type-width`, `vault.code-size`, `vault.weight-count`, `vault.glyph-distinct`, `vault.figure-face`, `vault.figures`, `vault.font-features`, `vault.font-smoothing`, `vault.face-roles` and `vault.fluid-type`, in [rules/](../rules/). The research behind #282's lines is `docs/research/typeface-traits.md` in the design vault, and behind #275's `docs/research/carry-source-checks.md`.

A project's rules file wins over every record here except a floor WCAG or the law sets ([source precedence](house-principles.md#source-precedence)). A dated record is reviewed a year after writing, or sooner when a platform ships a new type scale.

## The face profile

`python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/face-profile.py <page> --out <dir>` reads, for each typeface setting the page draws text in, the inputs these records name: `xheight` (the ex unit over the size), `width` (a pangram's average character over the size), `weight` and `stem` (an upright stroke's thickness over the size), `axes` (which of wght, wdth, opsz and GRAD the font varies on) and `opsz` (the optical size in use and the font's range). It reads the font the browser drew, so a web font that failed to load is read as its fallback, and `rendered` names it.

## Principles

### Size from x-height

Records: `vault.type-size`, `vault.type-floor`.

- **Why.** Apparent size follows x-height, not the CSS size: Verdana's x-height is about 55% of its em and Baskerville's about 40%, so Baskerville must be set larger to look the same size (Google Fonts Knowledge, 2024). Reading slows below a critical print size of about 0.2° of x-height (Legge and Bigelow 2011). 16 px at x-height 0.52, the sans faces the 16 px floor was set with (Arial, Roboto, Helvetica; APCA's reference), already gives about 0.18° at the CSS reference distance, so a smaller x-height is scaled up by 0.52 over it and a larger one is never scaled down.
- **Trade-off.** A face scaled up by x-height sets fewer characters a line at one column width, so the column widens with it (`vault.type-leading`'s order). Too large an x-height crowds accents (CSS Fonts 4 on `font-size-adjust`).
- **Clash.** USWDS normalizes by cap height and lets a face go under 16 px (Roboto Mono 0.95); the house scales by x-height, which reading speed follows, and only up. `vault.body-size` asks for 16 px on all phone text; Apple (11 pt), Material 3 (11–12 sp) and Atlassian (12 px fine print) allow smaller labels and fine print, and only GOV.UK (16 px smallest) backs the phone floor. The founder ruled for the platforms (#362): `vault.type-floor` sets 11–12 px for labels and fine print, and `vault.body-size`'s phone clause retires when its successor goes live (#416).

### Weight by size and ground

Record: `vault.type-weight`.

- **Why.** Thin strokes render fainter and are hard to see at small sizes (WCAG 2.2 Understanding 1.4.3; Apple HIG: avoid Ultralight, Thin and Light "especially when text is small"); black and ultra weights are for headlines (Butterick), and excess weight at small sizes hurts too (Material 3). The stem measures what the weight number does not: a 400 in a light design draws a thin stroke, and `vault.type-floor` sets such a face larger. On a dark ground, light text looks heavier (irradiation), but no study finds a reading need to change weight or grade by mode (Material 2022; Palmén, Gilbert and Crossland, CHI 2023, 459 readers), so a lighter weight or grade there is a look choice for large text only. Some platforms render thin strokes lighter than others; Butterick serves Windows a heavier body weight by script, but the 400 floor already keeps text above the weights that fade, so one weight serves every platform without detecting the device.
- **Trade-off.** Lowering grade on dark keeps line breaks, as grade leaves widths alone; lowering wght reflows. Below 400, de-emphasis costs legibility; a lighter colour or smaller size does that job instead (Refactoring UI).
- **Clash.** The Typography Handbook (2026, uncited) takes weight up on dark; Material, Argyle and Google Fonts Knowledge take it down. Both sides agree small light text must not get thinner. Supersedes the live `vault.dark-text-weight`'s extra line height and tracking, which no source backs, when this record goes live (#416). The size split at WCAG's large-text sizes is the house's mapping, not a finding.

### Line height by role, face and measure

Record: `vault.type-leading`.

- **Why.** Body text takes about 1.5 (Material 3, USWDS, Atlassian), headings about 1.2, and display under 1 at 72 px (Google Fonts Knowledge). A face that runs large, by x-height or weight, needs more line height and one that runs small less (Butterick; Latin; Google Fonts Knowledge). Longer lines need more: the Typography Handbook gives about 0.1 per 10 characters past 65, and Refactoring UI 1.5 narrow to 2 wide. Size, measure and line height are set in that order, since each follows the one before (Latin).
- **Trade-off.** More line height keeps a reader's place on long lines and costs height; short UI copy of one or two lines takes 1.3–1.43 (Carbon, Atlassian). Diacritic-rich and non-Latin scripts need more (Material 3 language height; web.dev, Internationalization), and so does a language of long compound words such as German (Latin 2023). A one-line label or row may run tight, but three or more lines never do, even where height is short (Apple HIG Typography); captions and text under a paragraph take about 1.35 (USWDS token 3).
- **Clash.** `vault.leading` cites Butterick for leading set by line length; his pages do not say it, and impeccable's "inversely with measure" contradicts its own "wider lines need more". No design system changes line height between light and dark mode, and the one source that does calls it minor and cites nothing, so line height stays the same on both. WCAG 1.4.8 (AAA) asks 1.5 in paragraphs and 1.4.12 that text survive 1.5; the 1.3 floor is AA practice.

### Tracking by size and face

Record: `vault.type-tracking`.

- **Why.** Every maker's curve is looser at 11–12 px than at 16 px, and tighter, or level where an optical size takes over, at display sizes (Apple SF Pro and New York, Material 3 Roboto, IBM Carbon for Plex, Inter v3). At 16 px the curves span −0.020 em (SF Pro) to +0.031 em (Roboto body), so tracking at text sizes belongs to the face: the maker's curve first, USWDS's face-independent curve where none is published. Capitals take 5–12% (Butterick; Bringhurst via Rutter).
- **Trade-off.** Tighter tracking increases crowding (Google Fonts Knowledge, 2025); wider tracking past the face's own gains a typical reader nothing.
- **Clash.** impeccable's −0.04 em display floor (`design-round/references/impeccable.md`) is outside every maker's curve, whose tightest is −0.022 em; the record sets −0.03 em, USWDS's tightest. A face with an active opsz axis or a display cut takes no negative tail, as SF Pro's curve turns positive where its Display design begins. Heavy or condensed lowercase may take a little positive tracking (Bringhurst; Material 3 "heavier fonts may require wider letter spacing"); no source gives the amount.

### Variable fonts and axes

Record: `vault.type-axes`.

- **Why.** A weight-axis variable file weighs about two static weights (measured, #282), so it pays once a page uses three weights, a weight between two named ones, or grade or width. An opsz axis adds 1.5–2.4× more and pays where the face is used at both text and display sizes. Optical sizing is on by default and the browser sets opsz to the used size; setting it by hand is outdated advice (Web Almanac 2024).
- **Trade-off.** A variable file is one request and many styles; at one or two weights it costs bytes. A variable file's default instance may not be 400 (Fira Code ships at 300), so the weight is always set.
- **Clash.** The Typography Handbook makes variable fonts the default whatever the count; the byte measurement does not bear that out at one or two weights. A `font` shorthand resets `font-optical-sizing`, `font-size-adjust` and `font-variation-settings` (MDN), so they are set after it.

### Width by role

Record: `vault.type-width`.

- **Why.** A narrow width fits more characters in a label or a dense cell, and a wide one carries personality in a short heading (Material 3; Google Fonts Knowledge). Text read at a glance reads best in a non-condensed width at a larger size (Google Fonts Knowledge, 2025).
- **Trade-off.** A condensed face may need a slightly larger size; a wide one costs space a top bar lacks.
- **Clash.** None known.

### Inline code beside body text

Record: `vault.code-size`.

- **Why.** Monospace faces run large: JetBrains Mono's x-height is 0.550 against Source Serif 4's 0.475, so at one size the code looks louder than its sentence. Matching x-heights gives 0.864 em, beside Latin's 0.857 em (12 px in 14 px) and Atlassian's fixed 0.875 em.
- **Trade-off.** A code box with padding pushes its line apart unless the line height rises with it (Latin).
- **Clash.** None known.

### Emphasis takes bold

Record: `vault.emphasis-weight`.

- **Why.** One step from regular to semibold is often too small to read as emphasis, and the visible step shrinks further at small sizes and on dark grounds (Google Fonts Knowledge; [Weight by size and ground](#weight-by-size-and-ground)). The same holds for a selected state shown by weight: it must be obvious (Apple HIG Toggles).
- **Trade-off.** Butterick allows semibold, which reads a little more easily than bold; the house takes Google's clearly visible difference. A face drawn without a 700 takes its next weight past +300.
- **Clash.** `vault.type-weight` caps text at 14 px and under at 700, which bold meets. `vault.weight-count` lets 600 serve emphasis, which this record allows only over a 300 body; `vault.sibling-emphasis` and `vault.prose-emphasis` say when weight is the cue and that it never pairs with italic.

### Fallback faces match the web font

Record: `vault.fallback-metrics`.

- **Why.** With `font-display: swap` the page first draws a system face, then swaps in the web font; where the two differ in size and line metrics, every line rewraps and the page jumps (web.dev, Typography). `size-adjust` and the metric overrides on a fallback `@font-face`, or `font-size-adjust`, make the fallback take the web font's measurements (MDN).
- **Trade-off.** `font-size-adjust` is Baseline only since 2024, so older browsers still jump.
- **Clash.** `vault.font-display` chooses how the font loads; this record makes the swap it allows shift nothing.

### How many weights

Record: `vault.weight-count`.

- **Why.** Each weight is another file to load and another step for a reader to tell apart; regular and bold cover most needs, and design systems stop at two to four.
- **Trade-off.** A medium beside icons or a display weight for big headings each earn their place only with a named job.
- **Clash.** `vault.type-weight` sets which weight each size takes; `vault.type-axes` says when a variable file pays.

### Telling characters apart

Record: `vault.glyph-distinct`.

- **Why.** Readers with dyslexia and others confuse I, l and 1, and O and 0; in a reference number or code there are no words around them to help.
- **Trade-off.** A slashed zero looks technical in running prose, so it is kept to codes and data.
- **Clash.** None known.

### Figures

Records: `vault.figure-face`, `vault.figures`.

- **Why.** Numbers line up in a column only when every digit is the same width; in a sentence, proportional digits space more evenly; lining digits sit at capital height, so they match capitals. A face without tabular digits cannot be fixed by CSS.
- **Trade-off.** USWDS sets table amounts in a monospace face; the text face's tabular digits keep one typeface and do the same alignment, so the monospace face is the fallback.
- **Clash.** `vault.face-roles` keeps a monospace face for code; it sets compared numbers only where the text face has no tabular figures.

### OpenType features

Record: `vault.font-features`.

- **Why.** A feature works only where the font has the glyphs and the browser supports it; the `font-variant-*` properties say what is wanted, while `font-feature-settings` switches raw tags on and off together. The `font` shorthand resets every feature to its default.
- **Trade-off.** A few features (stylistic sets, some alternates) have no `font-variant` property, so they still need `font-feature-settings`.
- **Clash.** None known.

### Font smoothing

Record: `vault.font-smoothing`.

- **Why.** On a Mac, light text on a dark ground looks too bold with subpixel smoothing; greyscale smoothing thins it back. On a light ground it only makes thin text fainter.
- **Trade-off.** Whether a site-wide setting changes anything on current Macs is disputed (Comeau 2026 says browsers still use subpixel; others say Mojave ended it), and it was not measured, so the rules file decides.
- **Clash.** None known.

### One job per face

Record: `vault.face-roles`.

- **Why.** A second face works when each face keeps one job, body or headings; a third rarely works, and four almost never (Butterick). Too many faces blur the hierarchy and make an interface look inconsistent (Apple). Code needs a monospace face, because its dense punctuation reads better there. Design systems split the faces the same way: USWDS by role tokens, Atlassian with a brand face for marketing and a plain one for the app.
- **Trade-off.** One family is lighter to load and always consistent; a second face adds voice and file weight.
- **Clash.** `vault.brand-layer` says where expressive display type belongs; this record says how many faces there are and which job each holds.

### Fluid size

Record: `vault.fluid-type`.

- **Why.** A size set in `vw` follows the window, not the visitor's zoom or text-size setting, so it fails WCAG 2.2 SC 1.4.4 (MDN, WCAG F94).
- **Trade-off.** Fluid headings remove the jumps between breakpoints but are harder to predict at a given width; stepped sizes are simpler and pass by construction.
- **Clash.** `vault.type-size` sets body text's size; this record governs only how a size changes with width.
