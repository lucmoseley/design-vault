# Research #205: the founder's notes N1–N19 against the house

Question (#205, map #202): for each note N1–N19, what do the house references and research hold? Is the note sound design theory? Is it covered, partly covered, or a gap?

Language: ASD-STE100 Simplified Technical English.

Verdict words:
- **covered**: the house has a rule. The rule has a source, a condition and a trade-off, and it gets to a skill or a critic.
- **partly**: the house has some of the rule, or it has the rule in research only, or the rule has no condition or no source.
- **gap**: the house has nothing on it.
- **not worth covering**: the question does not need a house rule.

"House reference" = a file under `plugin/skills/design-critique/references/`, `plugin/skills/design-critique/SKILL.md`, `gate.md`, or `plugin/skills/design-round/references/impeccable.md`. These files get to the critic. A file under `docs/research/` does not get to a critic by itself.

Era words: **timeless**, or **era-bound** (tied to a period, which the entry dates; current practice means 2023 on).

## Findings, note by note

### N1. Text for comfortable reading

**N1a. Characters per line ("70–80 is good — true? only in some cases?")**
- House: `plugin/skills/design-critique/SKILL.md:65` (the Measure lens: 45–75 characters, spaces included; the critic counts set characters; `check-measure.py` measures each width). `plugin/skills/design-round/references/impeccable.md:83` (override: 45–75, "Source: Butterick, 45–90"). Research: `docs/research/adopt-or-build.md:38-39`, `docs/research/principle-interactions.md:154` (i1: "Read pages target 60-75; dense UI may go shorter"). Closed #86 added the lens and its script.
- Sourced: yes (Butterick). Conditioned: partly. The lens applies to "body text" and skips headings, nav, forms and tables. The research condition "dense UI may go shorter" (i1) is not in the lens. Reaches a critic: yes, with a script.
- Verdict: **covered**, because the lens has a condition (body text only).
- Is the note sound? **Partly.** 70–80 is inside the accepted envelope only at its top:
  - Butterick: "Aim for an average line length of 45–90 characters, including spaces" (practicaltypography.com/line-length.html, read 15 Oct 2026). Strong secondary.
  - Baymard: "50–75 characters per line"; Ruder 50–60; Baymard's own tests found fatigue at 100+ characters (baymard.com/blog/line-length-readability, read). Domain evidence.
  - WCAG 2.2 SC 1.4.8 (AAA): "Width is no more than 80 characters or glyphs (40 if CJK)" (W3C Understanding 1.4.8, read). 80 is a ceiling, not a target.
  - Reading studies: Dyson and Haselgrove 2001 (*IJHCS* 54:585–612) report 55 characters a line as best for speed and comprehension together; Shaikh and Chaparro found 95 characters a line read fastest, but readers prefer shorter lines (both read second-hand through search summaries, not the papers).
  - So: 70–80 is acceptable for a single wide column of prose, at the top of the range. The middle of the expert range is about 55–66. 80 is the accessibility ceiling. Narrow columns (cards, multi-column, phone) run shorter (Butterick: newspaper columns "have to be very narrow").
- Finding on a house value: the lens fails a line at 76–90 characters. Butterick, the source the override names, allows up to 90; WCAG allows 80. The 75 cap now cites Baymard and WCAG 1.4.8 (`plugin/skills/design-round/references/impeccable.md`), a house error #208 ruled fixed.
- Era: **timeless** (perception of line return).

**N1b. Font size**
- House: `impeccable.md:104` ("a 16 px body floor, unless a dense role justifies less (Butterick 15–25 px; IBM Carbon)"). Research: `principle-interactions.md:88` P29 (16 px+ on Read pages; 14–15 px secondary lines on dense results), `design-coverage-gaps.md` W5.
- Sourced, conditioned (by mode and density), reaches the builder through the override list. A critic gets it only through impeccable `typeset`/`audit` (design mode on). No gate question.
- Verdict: **covered** for body size. **Not worth covering** as a house rule for a type scale (how sizes step from body to display): #101 Q4 accepted "type and spacing scales from one source per project" as filled, so the scale is the project's value (level 2), not a house rule.
- Sound: yes. Butterick: web body "15–25 pixels" (via `design-coverage-gaps.md` W5). Era: **era-bound** (16 px+ is current; 12–14 px body is a dated 1990s–2000s habit).

**N1c. Font weight for body text**
- House: research only. `docs/research/text-presentation.md` B5.3 ("weight ≥ 400" at or under body size; Apple HIG avoids Light weights "especially when text is small"; WCAG Understanding 1.4.3 on thin fonts). Override `impeccable.md:74` on weight on dark grounds (sourced: Material "Adjusting Grade for Mode", 2022).
- Not in a house reference except the dark-ground override. Verdict: **partly**.
- Sound: yes, as a floor. Era: timeless.

**N1d. Letter spacing of body text and line spacing**
- Letter spacing: research only, `text-presentation.md` B2.3 ("Lowercase does not normally take letterspacing", Butterick; WCAG 1.4.12 at 0.12 em user spacing). impeccable detector "wide tracking on body text", "crushed letter spacing". Verdict: **partly** (detector, no house reference).
- Line spacing: `impeccable.md:84` (detector finding under 1.3 on body only; Butterick 120–145%), `impeccable.md:104` ("leading set by measure"); impeccable `typeset.md:47` ("Tune line height inversely with measure"). WCAG 1.4.8 (AAA) asks 1.5. Verdict: **covered** (sourced, conditioned by role).
- Sound: yes. Era: timeless.

**N1e. Text opacity and hue by context**
- House: `plugin/skills/design-critique/references/text-presentation.md:9-16` (the tint rule: hue, chroma band, when, trade-off, clash; secondary text on a coloured ground takes that ground's hue). Research: `text-presentation.md` B1.3 (grey on a coloured ground), B1.4 (solid against opacity greys: solid per ground on the web; alpha only for disabled), B1.5 (two readable text steps per ground, plus disabled and placeholder).
- The tint rule is sourced, conditioned and reaches the critic. B1.4 and B1.5 (opacity, number of text steps) are in research only.
- Verdict: **covered** for hue; **partly** for opacity and for the number of text-colour steps.
- Sound: yes. Era: the tint is era-bound (current since about 2018, Material You 2021); solid tone roles are current (Material 3); alpha text emphasis is era-bound to Material 2 (2014–2021).

**N1f. Left, right and centre alignment**
- House: `impeccable.md:104` ("no justified text (Butterick; WCAG 1.4.8)"); impeccable detector "justified text". No house line on centred or right-aligned text.
- Verdict: **partly** (justified covered; centred and right alignment a gap).
- Sound: yes. WCAG 1.4.8 (AAA): "Text is not justified"; Understanding 1.4.8 does not name centred text (read). Butterick: centred text is "acceptable when used for short phrases or titles"; "Whole text blocks should not be centered" (practicaltypography.com/centered-text.html, read). Right-aligned text: numbers in table columns, by convention; no source read in this session.
- Era: timeless.
- Research question for the gap: *When does a web page centre or right-align text (headings, hero lines, short marketing blocks, numbers in tables), and at what line count or measure does centred text start to cost reading?*

**N1g. Single words orphaned on a line (`text-wrap: balance`, `pretty`)**
- House: none in the house references or research. impeccable `craft-floor.md:12` says "balanced headings", with no condition and no source. No closed issue found (search "orphan", "text-wrap": no design hit).
- Verdict: **gap** (one unconditioned impeccable line).
- Sound: yes, as a polish rule. MDN (`text-wrap`, read): `balance` balances characters per line and is limited to short blocks ("six or less for Chromium and ten or less for Firefox"); `pretty` uses "a slower algorithm that favors better layout over speed", for body copy, for example to keep orphans to a minimum, and "has a negative effect on performance". `text-wrap` is Baseline; `pretty` is not yet Baseline (Firefox support unclear; search snippets only). Both degrade safely to normal wrapping.
- Era: **era-bound** (CSS features from 2023–2024; the typographic aim, no single word on the last line, is timeless).
- Research question: *Which text roles take `balance`, which take `pretty`, which take neither, and what does each cost (performance, ragged widths in multi-column cards, interaction with the measure check)?*

**N1h. How much of a page's or section's width text takes**
- House: the Measure lens limits the line, not the block. No rule on the text block's width against its section (for example a 60-character column in a 1440 px section, left-aligned or centred), or on hero lines.
- Verdict: **partly** (line length covered; block width and its placement in a wide section a gap).
- Research question: fold into N1f and N12: *How does a wide section place a measure-limited text column (left on the grid, centred, offset), and what decides it?*

**N1i. When and how much to bold, italicise, resize or recolour**
- House: research only, `text-presentation.md` B2.1 (rank by weight first, then a colour step, then size; one cue down is enough), B2.2 (Butterick: bold or italic, never both, rarely; with a sans, bold). `principle-interactions.md:83` P24 (working-area emphasis by weight, size, position, not colour). impeccable `typeset.md:42` ("Combine size, weight, space, and tone"). Override `impeccable.md:85` (flat-type-hierarchy).
- Not in a house reference. Verdict: **partly**.
- Sound: yes. Era: timeless.

### N2. Section background colours, and a subtle gradient against a solid fill

**N2a. When sections take different background colours**
- House: no rule for page sections. Nearest holdings:
  - `plugin/skills/design-critique/references/surface-styling.md:57-62` ("Dividers against space and fill": space first, then a fill or one divider; a border that groups against the spacing makes grouping ambiguous). This is for cards and lists, not for page bands.
  - `plugin/skills/design-critique/references/brand-palette.md:11-16` ("A palette is roles": ground and surface are roles; one contrasting hue as the figure).
  - Research `docs/research/surface-styling.md` B5.1 (Carbon layers alternate `background` #ffffff and `layer-01` #f4f4f4; Atlassian "sunken" surfaces), B5.3 (Polaris: "Don't use bright or contrasting colors for container backgrounds or borders"), B1.5 (common region, Palmer 1992; Montoro and Luna 2015).
  - Manta's own zone rule: hero/marketing zone loud, working area calm (`docs/research/design-rules-census.md:209`, B1). Owner: mantahostels.
- Verdict: **gap** for page sections (the principle exists for containers; nothing says when a band of colour is the right section break, how many bands a page takes, or how bands alternate).
- Sound: yes, as a question. A colour band is a common-region cue (Palmer 1992, peer-reviewed, via #117 B1.5), so it groups and separates. One cost has a source: NN/g, Flaherty, 17 Jan 2016, "The Illusion of Completeness": "a horizontal line that spans the width of the page can create a visual barrier", and a large gap "can signal the end of a page" (read 15 Oct 2026). The article does not name a colour change; a full-width band edge is the same kind of horizontal break (inference). No design system read gives a rule for marketing-page bands.
- Era: the grouping is **timeless**; alternating full-width bands on landing pages is **era-bound** practice.
- Research question: *When does a page section take its own ground colour (a change of zone, of function, of reading mode), how far apart may two adjacent grounds sit (ΔE00, contrast of the edge), and when does a band edge act as a false floor?* It can reuse the ΔE00 thresholds in `brand-palette.md:21-28` (line 3 for adjacent large greys).

**N2b. A subtle gradient against a solid fill**
- House: bans only. House DNA `never` line 4: "gradient washes as decoration" (AI look); impeccable `craft-floor.md:33` (gradient text), detector "purple/violet gradients", "radial-gradient halo", "repeating-gradient stripes"; `impeccable.md:94` (the "AI look" bans, dated, review by 14 Apr 2027); Manta's "UI is flat" and its open scrim question (`principle-interactions.md` R6). Research `text-presentation.md` B4.3: a gradient scrim behind text on a photo.
- Verdict: **gap**. The house says when a gradient is a tell; it never says when a gradient is right (depth, light, a scrim for text, a brand ground).
- Sound: the note asks the right question. No primary or strong secondary source on "subtle gradient ground against solid ground" was found in this session. Known technical cost (my knowledge, not re-read): a low-contrast gradient over a wide area can show visible banding on 8-bit displays, so it needs dithering or noise.
- Era: **era-bound**. What counts as a tell moves fast: Anthropic's `frontend-design` skill suggested "gradient meshes" on 4 Dec 2025 and banned "gradient washes" by 3 Sep 2026 (`docs/research/house-audit-method.md:120`).
- Research question: *Where does a gradient carry a function (a light source, depth, a text scrim, a ground change) rather than decoration, how strong may it be before it reads as a tell or shows banding, and what does current practice (2023 on) ship?*

### N3. Button and element colour: hierarchy against semantics; size by purpose

**N3a. Does the hierarchy of importance "always beat" semantic colour?**
- House:
  - `plugin/skills/design-critique/references/house-principles.md:16` (dependency order, step 2 Role: "prominence by task priority"); `:73` (carrier A: "The primary action holds the view's strongest colour"; reserved: "The primary action's colour"); `:76` (carrier T: "Semantic colour with text or an icon … one colour per status everywhere"; reserved: "The semantic colours, and none near the action colour"); `:95` (function walk Q6: rank by visual weight against task priority, one primary action).
  - Gate: `gate.md` `vault.primary-action` (look question, from walk Q6).
  - Research: `docs/research/function-fit.md:110-125` (B3.1, B3.2: Apple HIG Buttons, Material 3 emphasis ladder, GOV.UK Button, NN/g 2021; condition (2): "Given a destructive most-likely action, do not give it the primary style"); `principle-interactions.md:63` (P4: "the CTA keeps the strongest colour, rather than the brand mark"), `:166` (C7: status takes its semantic token).
  - House DNA `never` line 13 (`data/gallery.json:25`): "several colours at equal weight, none dominant".
- Sourced: yes (primary). Conditioned: yes (task priority is the visitor's; destructive actions; count per view; patterned grounds). Reaches the critic: yes (walk and gate).
- Verdict: **covered**. One part is **partly**: no house line says what a destructive action looks like at each step (the list view, then the confirmation step).
- Is the note sound? **Partly. "Always" is too strong.** The claim most likely comes from Refactoring UI's "Semantics are secondary" (Wathan and Schoger 2018: do not make a destructive action big and red only because it is destructive; give it the treatment its rank earns, and keep the bold red button for the confirmation step; from memory, not re-read). The primary sources agree with the core and add the limit:
  - Apple HIG Buttons: "Don't assign the primary role to a button that performs a destructive action, even if that action is the most likely choice" (via `function-fit.md:112`). Here a semantic fact (destructive) changes the hierarchy, so semantics wins over "most likely".
  - Carbon Button usage (read 15 Oct 2026): the danger button is "used for actions that could have destructive effects"; danger *primary* "for destructive actions that are a required or primary step in a workflow"; danger *tertiary or ghost* when the destructive action "is one of several options". So the hierarchy picks the emphasis rung, and the semantic picks the colour on that rung. Neither "always beats" the other.
  - GOV.UK Button: warning buttons "Only … for actions with serious destructive consequences" (via `function-fit.md:114`).
  - WCAG 1.4.1: a status shown by colour must also show by text or an icon, so semantic colour never carries meaning alone (house carrier T already says this).
- Resolution the sources support: hierarchy decides *prominence* (fill, outline, text; one primary per view). Semantics decides *hue* inside the rung it is given, and it reserves its hues (a status colour never marks the main action; the action colour never marks a status). A destructive action is never the prominent default; at a confirmation step it may be the primary, in the danger hue.
- Era: **timeless** (principle); the rung names (filled, tonal, outlined, text) are era-bound (Material 3, 2021 on).
- Research question for the part that is open: *What does a destructive or irreversible action look like at each step (in a list, in a confirmation), and how does the house's carrier table name the danger rung?* Small; can sit with N17.

**N3b. Buttons sized by purpose and by where the eye should go**
- House: none on size. Research `function-fit.md:112` quotes Apple: "Use style — not size — to visually distinguish the preferred choice among multiple options." `impeccable.md:88` covers target size (24 px floor, 44 px option), not size as emphasis.
- Verdict: **partly** (the source is in research; no house rule on size as an emphasis tool).
- Sound: **partly.** Sources split by context:
  - Apple HIG: style, not size, to mark the preferred choice in a group.
  - Carbon Button usage (read): "We do not recommend mixing different button sizes in button groups"; sizes are chosen by context (Large productive the common size; Extra large where a button bleeds to a modal's edge).
  - Google M3 Expressive research (via `function-fit.md:164`): a larger Send button, placed above the keyboard, helped people find key elements "up to four times faster". Size raised prominence on the one key action.
  - So: inside a group, one size and the emphasis rung carry rank; a standalone key action (a hero call to action, a floating action) may take a larger size. Target size has its own floor (WCAG 2.5.8).
- Era: the group rule is **timeless** (similarity); the larger-key-action pattern is **era-bound** (M3 Expressive, 2025).
- Research question: *When does size, rather than the emphasis rung, mark the key action, and what size steps does a button set need by context (group, hero, dense row, touch)?*

### N4. Variable fonts where available and fitting

- House: no house reference line. Research only: `docs/research/text-presentation.md` B5.2 (optical size: leave `font-optical-sizing: auto`; grade changes apparent weight without reflow; MDN), B4.2 (lower `GRAD` on dark, weak sources), B5.3 (Nunito Sans' variable file defaults to `wght` 200, so a missing `font-weight` renders at 200). `docs/research/house-audit-method.md:65` (Material "Adjusting Grade for Mode", 2022: no readability need to change grade between modes). impeccable `typeset.md:23` asks only whether "variable-font settings avoid invisible text and disruptive reflow" (delivery). Closed issue hit: #123 only (search "variable font").
- Verdict: **gap** for the choice (when to pick a variable font, which axes to use); **partly** for its rendering details (research, not a reference).
- Is the note sound? **Yes, with a condition.** web.dev, "Introduction to variable fonts on the web" (Crossland, Kurtuldu, Nieskens, Steiner; updated 19 Feb 2018; read 15 Oct 2026): one file can replace many ("48 individual fonts in a single variable font file meant a 88% reduction in file size"), but "if you are using a single font such as Roboto Regular and nothing else, you might not see a net gain"; animating between settings "may cause performance issues". Five registered axes (`wght`, `wdth`, `opsz`, `slnt`, `ital`); grade "changes the weight of the font without changing the widths, so line breaks do not change". So "use a variable font where available" holds when a site uses three or more styles of one family, or wants optical size, width or grade; it does not hold for a site that uses one or two static weights.
- Era: **era-bound** (OpenType 1.8, 2016; broad browser support about 2018–2020; current).
- Research question: *When does a variable font beat static files (styles used, file size, subsetting), which axes does a site set (weight steps, `opsz` auto, `wdth` for narrow screens, `GRAD` for dark grounds), and what defaults trap a build (a variable file's default instance, `font` shorthand resets)?*

### N5. Outer rings against borders on buttons and other elements

Reading of the note: a "ring" is an edge drawn outside (or inside) the box with a zero-blur `box-shadow` spread (Tailwind `ring`, `inset-ring`) or an `outline`, in place of a CSS `border`. It is a common edge for cards, images, avatars and inputs in current practice.
- House: only for focus. `plugin/skills/design-critique/references/surface-styling.md:64-71` (focus rings: two-colour or per ground; an outside 2 px ring on inputs; a `box-shadow` ring "keeps `outline: <width> solid transparent`, so forced-colours mode still shows it"); `:101` (interaction 9). Two border roles at `:9-16` (control edge 3:1, decorative edge). impeccable detector "hairline border plus wide diffuse shadow" (`docs/research/impeccable-checks.md:76`). No rule says when a resting edge is a border, a ring or an outline.
- Verdict: **gap** (for resting edges); **covered** (for focus rings).
- Is the note sound? **Yes; it is a real build choice with a known accessibility trade-off.**
  - What a ring is: Tailwind `ring` = `box-shadow: 0 0 0 1px`; `inset-ring` = `inset 0 0 0 1px` (tailwindcss.com/docs/box-shadow, class table read 15 Oct 2026). A shadow takes no layout space, so a ring can change width (hover, focus, selected) with no shift of the content; a border changes the box size unless `box-sizing` and widths are planned. (Layout fact: CSS box model; the Tailwind page states no reason.)
  - The trade-off: MDN `forced-colors` (read): "`box-shadow` is forced to `'none'`"; `border-color` and `outline-color` only change to system colours. So a ring vanishes in Windows high-contrast mode, and a border or outline stays. For a *control edge* (house role, WCAG 1.4.11), a ring alone fails forced-colours users; for a *decorative edge* (cards, images), losing it is acceptable.
  - Inset ring on images: a low-alpha inset ring gives an image an edge against a ground of the same lightness (common practice; no primary source read).
- Era: **era-bound** (rings as resting edges spread with Tailwind v2, 2020 on; current). The forced-colours rule is **timeless** as an accessibility need.
- Research question: *For each edge role (control edge, decorative edge, image edge, selected or hover state), which mechanism draws it (border, outline, outer ring, inset ring), and what does each cost (layout shift, forced-colours, corner radius, overlap with neighbours, stacking with a shadow)?* It extends `surface-styling.md` "Two border roles".

### N6. When dividers are needed inside sections and cards

- House: `plugin/skills/design-critique/references/surface-styling.md:55-62` ("Dividers against space and fill": where padding already separates, no divider; where room is short, a divider in the decorative edge colour, full width between unrelated sections, inset between related items; inside a card, a fill band or one divider, never both; "fix the spacing first, never add a line to override it"); `:93-96` (interactions 1–4, "Divider and card": cards with their own edges take no dividers between them). Research `docs/research/surface-styling.md` B4.1, B1.4, B1.5, B4.2 (zebra striping: weak evidence).
- Sourced: yes (Material Divider, GOV.UK `border`, Apple HIG Layout, Polaris; Palmer 1992, Montoro and Luna 2015). Conditioned: yes (room, density, relation of the groups). Reaches the critic: yes (reference; Gestalt lens "common region" in `SKILL.md:52`).
- Verdict: **covered**.
- Sound: yes. One addition from this session: NN/g (Flaherty 2016, read) warns that a full-width horizontal line "can create a visual barrier" that reads as the end of the page. The house rule does not name this false-floor cost for a full-width divider near the fold. Small; add as a condition, no new research.
- Era: **timeless** (print practice); the values are current.

### N7. How busy a page looks

- House:
  - Research `docs/research/design-coverage-gaps.md` W4 (Tuch et al. 2012, *IJHCS* 70(11): low visual complexity and high prototypicality rated most appealing, judged within 17–50 ms; rank 3 gap, "Prototypical structure vs distinctive look").
  - `plugin/skills/design-critique/references/house-principles.md:116-121` (brand-layer line: "A dense list takes less novelty than a hero"); `:105-112` (beauty guard).
  - `surface-styling.md:57-60` and research B1.4 ("Too many borders make a design busy", Refactoring UI); `function-fit.md:103` ("strong signifiers on everything make a busy page").
  - impeccable `layout.md:22` (Density question: "Does the amount of information per region fit use frequency, decision complexity, and visitor mode?"), `layout.md:62` (squint test), `quieter`, `distill` commands; override `impeccable.md:79` (strikes the "≤4 visible options" count; judge grouping and scannability).
  - Closed #101 Q4 accepted the distinctive-against-familiar trade-off as filled by #127.
- Sourced: partly (Tuch is in research; the brand-layer line cites #127 sources). Conditioned: partly (density by visitor mode in impeccable; the house names hero against dense list). Reaches the critic: through impeccable `critique`/`layout` (design mode on) and the brand-layer line. No measure of busyness reaches a critic.
- Verdict: **partly**. No house rule says how to judge or measure visual complexity, or what level fits which page type.
- Is the note sound? **Yes.** Evidence that perceived complexity drives first impressions is peer-reviewed: Tuch et al. 2012 (via #104 W4); Reinecke et al., CHI 2013, "Predicting Users' First Impressions of Website Aesthetics with a Quantification of Perceived Visual Complexity and Colorfulness" (548 people, 450 sites; computed complexity and colourfulness, with age and education, explain about half the variance in appeal at 500 ms; abstract read, 15 Oct 2026).
- Era: the mechanism is **timeless**; what reads as busy for a category is **era-bound**.
- Research question: *Which measurable page features make a page read as busy (element count, edges, colours, type sizes, alignment lines), what level suits each visitor mode (persuade, operate, read), and can a script measure it the way `check-measure.py` measures lines?*

### N8. When the page container takes borders

Reading of the note: a visible frame on the page's main column or page box (side rules at the content column's edges, a bordered page panel on a ground, grid lines that draw the layout).
- House: no rule. Nearest:
  - `surface-styling.md:9-16` (two border roles: a page frame is a decorative edge, so any weak colour; no 3:1).
  - `house-principles.md:57-58`, `:78-79` (function codes C contain and D decorate; a frame that groups is C, a frame that styles is D).
  - Bans: House DNA `never` line 3 (`data/gallery.json:15`): "a broadsheet layout of hairline rules, square corners and dense newspaper-like columns" (AI look); impeccable detector "decorative grid-line background" (a later "generated-UI signature" rule, `docs/research/impeccable-checks.md:76`).
- Verdict: **partly, by method only.** The dependency order gives a frame a function and an edge role, so a critic can judge it; no line says when a page frame helps (holding a column on a very wide screen, a document or app-shell look) or hurts.
- Is the note sound? As a question, yes; as a topic it is narrow. No primary or strong secondary source was found or read in this session on page-frame borders. The perception basis is common region (Palmer 1992, via #117 B1.5).
- Era: **era-bound** (visible layout rules are a 2023–2026 look, and current bans name them as an AI tell).
- Recommendation: **likely not worth its own research ticket.** Fold it into the N2 question (section grounds) or N5 (edge mechanisms) as one sub-question: *When does the page's own frame (column rules, page panel, grid lines) carry a function, and when is it the dated hairline look?*

### N9. Cool, neutral or warm greys: when each

- House:
  - `plugin/skills/design-critique/references/text-presentation.md:11-16` (the tint rule: greys for text tinted toward the brand's main hue at OKLCH C about 0.01–0.03, up to 0.05 for a deliberate blue-grey; pure grey "an equal choice, for a neutral or functional feel"; a page with several strong hues or many photographs takes the dominant hue or pure grey, by the project's rules file).
  - `plugin/skills/design-critique/references/brand-palette.md:54` ("neutrals and dark grounds take an anchor's hue at low chroma"); `:25` (large greys near the page ground that share an edge: ΔE00 line 3; a tinted grey up to C 0.05 counts as a grey).
  - Research `docs/research/text-presentation.md` B1.1 (Material 3 neutral palettes carry the source hue; Radix "choose the gray scale … saturated with the hue closest to your accent hue" or pure gray for "a neutral vibe"; Tailwind v4 neutrals; Refactoring UI frames greys as colour temperature: blue for cool, yellow or orange for warm, read second-hand); `docs/research/house-audit-visual.md` V1–V2 (chroma band and pure grey SOURCED against shipped systems); `docs/research/de00-greys.md`.
  - Override: `impeccable.md:105` points text tints to the tint rule; the rule overrides impeccable `quieter`'s "tinted grays instead of pure gray".
- Sourced: yes. Conditioned: yes (dominant hue, several hues, coloured grounds). Reaches the critic: yes (reference).
- Verdict: **covered** for *which hue* a grey takes (the brand's main hue, or none). **Partly** for *temperature as a feel* (warm or cool chosen for the mood, apart from the brand hue): only Refactoring UI, second-hand, in research.
- A tension the house does not resolve: House DNA `never` line 5 (`data/gallery.json:17`) names "tinted near-black (#0B0B0B, #111) standing in for black" as an AI-look tell, while the tint rule and research B1.2 support near-black, tinted text. The two hex values in the DNA line are neutral, not tinted, so the line probably means a near-black *ground*. The DNA line is a dated default (review by 14 Apr 2027 for the matching impeccable bans); the tint rule is the conditioned rule. The house should say which wins on a dark ground.
- Is the note sound? **Yes.** Colour temperature is a measured colour emotion: Ou, Luo, Woodcock and Wright, "A study of colour emotion and colour preference. Part I", *Color Research and Application* 29(3):232–240, 2004 (warm–cool is one of four colour-emotion factors, found stable across cultures; abstract level, read through search). No source read measures warm against cool *greys* on a web page; the design-system practice (tint toward the brand hue) is the stronger source.
- Era: tinted neutrals are **era-bound** (current since about 2018); colour temperature as perception is **timeless**.
- Research question (only for the partly part): *When does a grey's temperature come from the brand hue, and when from the feel the site aims at (see N15); how does a warm or cool neutral interact with photographs and with a warm or cool accent?* Best handled inside #204 (N15).

### N10. How many fonts a site needs, by site size and function

- House: no house reference line. Holdings:
  - impeccable `typeset.md:42` ("Use the fewest roles and families that make the hierarchy unmistakable"), `:57` ("do not … introduce a second family without a clear role it alone can perform"), `typeset.md:8` (Operate and Read: "A single well-tuned family … often right"), `operate.md:13` ("One family is often right. Product UIs don't need display/body pairing"), `distill.md:52` ("One font family, 3-4 sizes maximum, 2-3 weights"), `new-work.md:67` (Persuade and Experience "want faces with a point of view"; a list of overused faces).
  - Override `impeccable.md:94-95` (the detector's `overused-font` is an AI-look ban, level 6, dated). `docs/research/adopt-or-build.md:46` (overused-font is "era-bound taste").
  - House DNA: no line on font count now; the 13 Oct research quotes an older DNA line "The default font stack (Inter, the system sans) as the only voice" (`text-presentation.md:22`), not in today's DNA.
- Sourced: no (impeccable cites none). Conditioned: yes, by visitor mode (impeccable). Reaches the critic: only through impeccable with design mode on.
- Verdict: **partly** (impeccable holds a conditioned rule; the house holds no sourced one).
- Is the note sound? **Yes.** Butterick, "Mixing fonts" (practicaltypography.com/mixing-fonts.html, read 15 Oct 2026): "Most documents can tolerate a second font. Few can tolerate a third. Almost none can tolerate four or more"; give each font a consistent job ("one font for body text and one font for headings"). Design systems ship one family with roles (Carbon: IBM Plex; Apple: SF, with New York as a serif option; GOV.UK: one) (my knowledge, not re-read). Each family adds font files to load (web.dev font guidance, not re-read). So the count follows roles and mode, not site size: an operate or read surface rarely needs more than one family; a persuade page may add a display face; a third face needs a role no other face can do (for example monospace for code or data).
- Era: **timeless** (role-based count); which faces read as default is **era-bound**.
- Research question: *How many families and styles does each site type need (a solo advisor's site, a booking site, a brand page), what job justifies each extra face, and what does each extra face cost in loading?* Small; Butterick and design systems likely answer it without new primary research.

### N11. When borders take opacity, and how much

- House: no rule on alpha borders. Holdings:
  - `surface-styling.md:11` (decorative edge: "any weak colour"; control edge: 3:1, "Measure the colour the browser renders"); `:39` (on a dark ground, "a light low-alpha edge where needed").
  - Research `docs/research/text-presentation.md` B1.4 (solid against opacity for *text*: solid tokens per ground on the web, alpha only for disabled); impeccable `colorize.md:189` ("Prefer explicit colors over chains of translucent overlays when alpha would make contrast context-dependent"); `docs/research/surface-styling.md:33` (Manta's badge border is lagoon at 45% alpha); `docs/research/house-audit-constants.md` A1 (the access script treats a step under 1.05:1 as no edge; four systems ship surface steps at 1.03–1.05).
- Verdict: **partly** (the principle for text and the dark-ground case exist; no rule for border alpha in general).
- Is the note sound? **Yes; it is a real trade-off.**
  - Alpha borders adapt to any ground (one token on white, a tint or a photo); solid borders give a fixed, measured contrast. For a *control edge*, WCAG 1.4.11's 3:1 must hold on every ground, so an alpha edge must be measured per ground (W3C Understanding 1.4.11, via #117 B1.1).
  - A CSS trap (CSS Backgrounds: `background-clip` defaults to `border-box`; my knowledge, not re-read): an alpha border on an element with its own background shows that background through it, not the page ground, unless `background-clip: padding-box`.
  - Design systems: Radix step 6 "subtle borders on components which are not interactive", step 7 "on interactive components", step 8 "stronger borders … and focus rings" (radix-ui.com, read 15 Oct 2026); Radix ships an alpha twin of each scale, but the pages read give no rule for choosing alpha over solid.
- Era: **era-bound** (alpha tokens per scale, 2021 on).
- Research question: *When does a border take an alpha colour (a varied or unknown ground, a dark theme, an image edge) and when a solid one (a known ground, a control edge), and what alpha range do current design systems ship for each edge role?* Fits with N5 and N13 in one edge-and-contrast ticket.

### N12. How and when to align content and icons between sections

- House: no house rule. Holdings:
  - `plugin/skills/design-critique/SKILL.md:52` (Gestalt lens "continuity", by name; no rule on what to align).
  - impeccable `polish.md:59` ("Align to the project's grid and spacing scale; fix optical as well as mathematical alignment"), `polish.md:68` (icon "optical alignment"), `quieter.md:80` ("Align to grid"), `layout.md:93` (4-unit spacing scale), `layout.md:101` (optical corrections after the render).
  - Override `impeccable.md:106` (proximity before containers; 4 px step). #101 Q4 accepted "type and spacing scales from one source per project" as filled.
  - Research `docs/research/design-coverage-gaps.md` W4 (Wagemans et al. 2012: good continuation, parallelism, connectedness; abstract read there).
- Sourced: the Gestalt basis is sourced; the alignment practice is impeccable's, unsourced. Reaches the critic: through the Gestalt lens and impeccable (design mode on).
- Verdict: **partly**. No rule says which edges and axes repeat between sections (a shared left text edge, the icon column lined up with the text column, centred against left-aligned sections), or when a break in alignment is right.
- Is the note sound? **Yes.** Good continuation and parallelism are among the classical grouping principles (Wagemans et al. 2012, *Psychological Bulletin* 138(6), peer-reviewed review, via #104 W4). Grid systems (Müller-Brockmann; Material and GOV.UK layout grids) put this into practice (not re-read in this session).
- Era: **timeless**.
- Research question: *Which alignment lines must hold across a page's sections (text edge, content column, icon column, media edges), how does a centred section sit beside left-aligned ones, and when is optical alignment (icons, punctuation, round shapes) needed?* Joins N1h.

### N13. How alike or different element contrast is across a site

Reading of the note: whether parts with the same role keep the same contrast level everywhere, and whether parts of different rank keep clearly different levels.
- House:
  - `house-principles.md:93-94` (function walk Q5: "Does each look on the page and the site mean one function? List every distinct treatment and its functions"), `:68-85` (carriers); research `function-fit.md:129-141` (B4.1: WCAG 3.2.4 Consistent Identification; same function, same look).
  - `brand-palette.md:19-33` ("The same colour or clearly different": ΔE00 bands; "Steps of one colour's ramp: exempt. Their check is contrast"; Tufte's subtle difference for rank).
  - `surface-styling.md:9-16` (two border roles with fixed contrast meaning).
  - Research `text-presentation.md` B1.5 (two readable text steps per ground; Radix Lc 60 and Lc 90), B6 (APCA levels by use).
  - Gate: `vault.contrast`, `vault.control-edges` (floors only).
- Verdict: **partly**. Consistency of *treatment* per function is covered (walk Q5, sourced, reaches the critic). A *contrast ladder* per role (text primary and secondary, control edge, decorative edge, surface step) is held only in pieces (border roles in a reference; text steps in research), not as one table a critic can check.
- Is the note sound? **Yes.** WCAG 3.2.4 (AA) asks consistent identification of same-function parts (via #127 B4.1); Radix assigns each scale step one role (step 6 non-interactive borders, step 7 interactive borders, step 8 strong borders and focus rings, steps 11–12 text; read 15 Oct 2026), which fixes a contrast level per role across a product.
- Era: the principle is **timeless**; the step-per-role systems are **era-bound** (2020s design systems).
- Research question: *What contrast level does each role take across a site (text ranks, control and decorative edges, surface steps, icons, disabled), how far apart must adjacent ranks sit to read as different, and how does the ladder change on dark and coloured grounds?* Joins N11.

### N14. Letter spacing (tracking) of headings

- House:
  - `plugin/skills/design-round/references/impeccable.md:86` (override: impeccable's "tracking no tighter than -0.04em" is "One author's numbers with no source found: the project's type scale replaces them").
  - Research `docs/research/house-audit-method.md:71` (item 11: "Tracking is set per typeface by its maker"; Apple SF Pro and New York tracking tables; Inter Dynamic Metrics, about -0.022 em at display sizes; "The hand-over to the project's type scale is SOURCED"; "no source found" is "partly wrong"). Closed #183 accepted the hand-over.
  - Research `text-presentation.md` B2.3 (caps headings and labels: +5–12% tracking; Butterick, Bringhurst second-hand); `principle-interactions.md:84` P25.
  - impeccable detector "crushed letter spacing", "wide tracking on body text".
- Sourced: yes. Conditioned: the value goes to the project; no condition says how tracking follows size or case. Reaches the critic: the override does; the caps rule and the size rule stay in research.
- Verdict: **partly**. The house hands the value to the project but gives the project no rule to set it by.
- Is the note sound? **Yes.** Type makers set tracking by size: Apple's system font "dynamically adjusts tracking at every point size" (HIG Typography, via `house-audit-method.md:71`); Inter's dynamic metrics tighten tracking as size grows (about -0.022 em at display sizes); a variable font with an `opsz` axis does part of this itself (`text-presentation.md` B5.2). Capitals need added tracking (Butterick: "Always add letterspacing to caps", 5–12%, via #123 B2.3). So: large lowercase headings take slight negative tracking, set from the face's own metrics; caps headings take positive tracking; body text takes none.
- Era: **timeless** (optical spacing by size and case); fixed numbers per face are the face's own.
- Research question: *How does a project set heading tracking from its typeface (maker metrics, `opsz`, size steps), and what limits apply by case (lowercase tighter at size, caps +5–12%)?* Small: the sources are already in house research; the gap is moving them into a reference.

### N15. The feel a design aims at (the founder's "energy"): buckets, the design term, the choices that go with each

Note: sibling ticket #204 asks this question in full ("What do designers call a design's intended feel … and which choices does evidence tie to each feel?").
- House:
  - `house-principles.md:16` (dependency order step 2 reads "Brand tone and the zone's energy"); `:116-121` (brand-layer line: distinctive in ground colour, illustration, display type, voice, motion character, one signature move; relaxed against high-stakes moments; Lavie and Tractinsky 2004 on classical against expressive beauty).
  - `brand-palette.md:15` ("Few hues with one job each read calm and clear, but can read plain. Energy then comes from lightness, scale, type and photographs, not from another hue").
  - The library: 16 collections in `data/gallery.json` (`collections`), each a named look with a plain-English `description`, a technical `vocabulary`, `risk`, `accent` and `imageStyle` (for example "Huge Type, Gallery Layout"). These are look buckets by visual family, not by feel.
  - design-round §2 direction cards (`plugin/skills/design-round/SKILL.md:84-100`): Evidence, Carry over, Invent; no field names the feel.
  - Manta's zone rule: "Energy is localised: hero/marketing zone loud (volume 6-7), working area calm (4-5)" (`docs/research/design-rules-census.md:209`, B1; owner mantahostels).
  - impeccable: colour strategies "Restrained … Committed … Full palette … Drenched" (`new-work.md:65`); "Energy is not the enemy of trust" (`new-work.md:69`); visitor modes Persuade, Operate, Read, Experience; `bolder` and `quieter` as axis commands (`impeccable.md:44-45`); `critique.md:233` asks about "tonal mismatch" ("clinical and corporate … warmer/bolder/more playful").
  - Closed #24 (library collections) flagged "Crafted-document energy" as jargon for the founder to read.
- Verdict: **partly**. The house uses "energy" and "tone" as inputs (step 2) and holds one lever list (brand-palette `:15`) and one two-level scale (Manta's loud and calm zones), but defines no buckets, no term, and no map from a feel to choices (line weight, colour strategy, type, density, motion, corners).
- Is the note sound? **Yes; it names a real design variable.** Terms in use: "tone" or "visual tone", "brand personality", "aesthetic", "mood". Evidence that feel has measurable dimensions:
  - Colour emotion: Ou et al. 2004, *Color Research and Application* 29 (warm–cool, heavy–light, active–passive, hard–soft for single colours; "colour activity", "colour weight", "colour heat" for pairs; abstracts read through search, 15 Oct 2026).
  - Web aesthetics: Lavie and Tractinsky 2004 split "classical" (clean, clear, orderly) from "expressive" (creative, original, sophisticated) aesthetics (cited in `house-principles.md:121`; not re-read).
  - Brand personality: Aaker 1997, *Journal of Marketing Research* (sincerity, excitement, competence, sophistication, ruggedness) (my knowledge; not read in this session).
  - Visual complexity and colourfulness drive first impressions (Reinecke et al. 2013; see N7).
  - The founder's example ("refined" = thin lines and restrained colour; "loud" = other choices) matches impeccable's colour strategies and Manta's volume scale in kind, but no source read here ties "thin lines" to "refined" by measurement.
- Era: the dimensions of feel are **timeless**; the choices that signal a feel are **era-bound** (what reads as "premium" or "refined" in 2026 differs from 2016).
- Research question: #204's, as written. Add to it: *How does one site hold two feels (a loud hero and a calm working area), and which choices are shared across zones so the site stays one system?*

### N16. Uppercase against lowercase

- House:
  - No house reference line. Research `docs/research/text-presentation.md` B2.3 ("Caps suit 'headings shorter than one line … headers, footers, captions, and other labels'"; "Always add letterspacing to caps", 5–12%; Butterick; Bringhurst second-hand; WCAG 1.4.12), Part D item 5; `principle-interactions.md:84` P25. The research's bound line says row 8 (caps tracking, the eyebrow) is Manta's.
  - Override `impeccable.md:75` (an eyebrow that names the section, place or category is no finding; GOV.UK caption above a heading).
  - House DNA `never` line 5 (`data/gallery.json:17`: "a tracked-out all-caps eyebrow above every heading") and line 7 (`:19`: "all caps for labels") as AI-look tells.
  - impeccable detector "all-caps body text".
- Verdict: **partly**. The typographic rule (short strings only, tracked) is researched but stays in `docs/research/`. Two house sources pull against each other with no clash line: research B2.3 accepts caps for labels; DNA line 7 calls "all caps for labels" an AI tell; #208 rules the clash a house error to fix. The DNA is a dated default and a brief can earn it back; no reference says how a critic weighs a caps label.
- Is the note sound? **Yes, with a correction to the common belief.**
  - Convention: caps for short strings, with added tracking (Butterick, via #123 B2.3; strong secondary).
  - Evidence on reading cost is weaker than the convention suggests: Arditi and Cho 2007, *Vision Research* 47(19):2499–2505, found uppercase read *faster* than mixed case near the acuity limit, and the advantage disappeared at larger sizes; they argue uppercase helps low-vision readers (abstract via PMC2016788, read through search, 15 Oct 2026). Older studies (Tinker, 1950s–60s) report slower reading for long all-caps text (not read). So "caps cost reading speed in long text" is a convention with old evidence; "caps are illegible" is not supported.
  - Sentence case against title case for headings and buttons: not researched in the house; GOV.UK and Material use sentence case (my knowledge, not re-read).
- Era: the short-string rule is **timeless**; caps labels as an AI tell is **era-bound** (2025–2026 model output).
- Research question: *Where do caps fit (labels, buttons, eyebrows, navigation, headings) and where sentence case or title case, on what evidence, and how does the house resolve the DNA's "all caps for labels" tell against the typographic rule?*

### N17. Badges and pills against icons

- House:
  - `house-principles.md:74-76` (carriers: S "the chip shape for filters" reserved; T "Semantic colour with text or an icon, beside the thing it describes"); `:73` ("Static tags, eyebrows in the button's type, decorative pills" borrow the button look); `:75` ("Static facts as chips" borrow the selectable chip); function walk Q4–Q5 (`:93-94`); gate `vault.borrowing`, `vault.affordance`.
  - `surface-styling.md:98` (interaction 6: "Capsules go to touch layouts, tags, status chips and one standout action").
  - Research `function-fit.md` B7.2 (GOV.UK Tag: "Tags are only used to indicate a status"; T row); `principle-interactions.md` P2, P13; `docs/research/surface-styling.md` B8.1 (icon stroke matches text weight).
  - impeccable `clarify.md:76` ("Do not rely on … iconography to carry the message alone"), `craft-floor.md:40` (icons from a real library, one stroke and weight); detector "hero eyebrow / pill chip".
- Verdict: **partly**. The house covers when a pill *must not* be used (a static fact must not look like a filter or a button) and that status needs text or an icon. It does not say how to show a fact or a status: as a badge, an icon with a label, an icon alone, or plain text.
- Is the note sound? **Yes.** NN/g, Harley, 27 Jul 2014, "Icon Usability" (read 15 Oct 2026): "a text label must be present alongside an icon to clarify its meaning in that particular context"; "Icon labels should be visible at all times"; only a few icons have near-universal recognition (home, print, search). GOV.UK Tag reserves the tag for status (via #127 B7.2). So: an icon alone carries meaning only for the few universal icons; a badge is for a status or a category, not for a decoration or an action.
- Era: icon recognition is **era-bound** (the set of known icons moves); the label rule is **timeless**.
- Research question: *For a fact, a category, a status and a count, when is the right form a badge, an icon with a label, an icon alone or plain text, and how many badges can one card carry before they stop being read?*

### N18. Responsive behaviour on resize: when sidebars collapse, what other elements do

- House:
  - Gate `vault.layout` (`plugin/skills/design-critique/gate.md:132-140`; `check-layout.py`): at every width, no sideways scroll, no cut or overlapping text, the call to action on the first screen. `check-measure.py` checks line length at both ends of each breakpoint range.
  - Overrides `impeccable.md:77` (device-width breakpoints struck: break where content breaks, container queries; web.dev Learn Design, Every Layout), `:89` (four nav links or fewer stay visible; NN/g 2016), `:88` (target sizes).
  - design-round renders desktop, one intermediate width and mobile (`docs/research/design-coverage-gaps.md:20`).
  - impeccable `adapt.md` and `layout.md:23` ("what reorders, collapses, wraps, scrolls, or remains fixed?"), `layout.md:96` ("Make responsive behavior structural: reorder, collapse, reflow, or reveal based on what remains important").
  - Research `docs/research/design-coverage-gaps.md` W10 (judged **covered** by impeccable); `docs/research/manta-element-coverage.md:230-234` (§2.9: responsive behaviour falls back to impeccable on 63 of 119 Manta elements; "No Manta rule adopts" #104 W10); Baymard on filter sidebars against horizontal filter bars (`manta-element-coverage.md:181`). Closed #101 Q3 sent accommodation search layout to mantahostels.
- Verdict: **partly**. The house checks the *result* at each width (no overflow, measure, nav count) and holds the *method* (content breakpoints). It holds no pattern table for what each kind of part does as the window narrows: a sidebar (filters, table of contents, handover) collapsing to a drawer, a sheet or a top bar; a grid dropping columns; a table becoming cards; images re-cropping.
- Is the note sound? **Yes.** Primary sources treat this as a layout decision by window size: Android's window size classes (developer.android.com, read 15 Oct 2026): Compact under 600 dp, Medium 600–840, Expanded 840–1200, Large 1200–1600, Extra-large 1600 and over; "Use window size classes to make high-level application layout decisions"; a phone in landscape has medium width and compact height, "in which case two pane layouts are not practical". WCAG 2.2 SC 1.4.10 Reflow (AA) requires content at 320 CSS px without two-way scrolling (the gate's sideways-scroll check). Size classes do not conflict with the struck device-width override: classes decide page-level structure (navigation form, number of panes); content breakpoints and container queries decide components.
- Era: reflow is **timeless** as a need; the patterns (rail, drawer, container queries, size classes) are **era-bound** (current, 2023 on).
- Research question: *For each part that changes structure with width (navigation, sidebars and filter panels, multi-column grids, tables, sticky action bars, media), what does it become at each window class, at what content-driven point, and which parts keep their place so a returning visitor still finds them?*

### N19. Across all notes: the best answer changes with other factors (palette, crowding, warm or cool text, the typeface's own traits)

**N19a. Does the house's rule form record context?**
- House: every house reference writes each principle as Rule, When, Trade-off, Clash, Era, Source (`house-principles.md`, `surface-styling.md`, `text-presentation.md`, `brand-palette.md`, `first-visit-trust.md`); the dependency order names what each step reads (`house-principles.md:11-18`: ground, neighbouring treatments, device, density, zone energy); `surface-styling.md:91-106` and `text-presentation.md:26-27` list "given X, do Z" interactions; research `docs/research/principle-interactions.md` §2 maps 42 interactions and §3 resolves 49 clashes. Sibling ticket #206 audits whether these conditions are complete.
- Verdict: **covered** as a form; whether each rule's conditions are complete is #206's question.

**N19b. Rules that characterise a typeface and their knock-on effects**
- House: none in a reference. Pieces: impeccable `typeset.md:21` ("line height, paragraph rhythm, contrast, and tracking tuned to the actual face, width, language, and surface"), `:49` ("Tune line height to the face … not a universal ratio"); `house-audit-method.md:71` (tracking set per face by its maker); `text-presentation.md` B2.4 (which faces have tabular figures), B5.2 (optical size axis), B5.3 (a variable file's default weight). The Measure lens counts set characters, so a wide or narrow face is measured as it renders (`SKILL.md:65`).
- Verdict: **gap**. No rule tells a session to read a face's traits (x-height, width, stroke contrast, axes, figure styles) and set size, line height, tracking and weight from them.
- Is the note sound? **Yes.** Two primary or strong sources say size depends on the face:
  - MDN `font-size-adjust` (read 15 Oct 2026): "Legibility of fonts, especially at small font sizes, is determined more by the size of lowercase letters than by the size of uppercase letters"; the property scales a font to a chosen x-height ratio. Baseline 2024 (since July 2024).
  - Legge and Bigelow 2011, "Does print size matter for reading?", *Journal of Vision* 11(5):8 (peer-reviewed review): the fluent range is described in *x-height* (about 0.2° to 2° of visual angle), not in point size (abstract level, through search). So two faces at the same `font-size` can sit at different points on that range.
- Era: **timeless** (perception); the CSS tools are **era-bound** (2024 on).

**N19c. Weight depending on palette, crowding, and warm or cool text**
- House: weight against ground lightness is covered: override `impeccable.md:74` (no weight change needed between light and dark; Material "Adjusting Grade for Mode", 2022, 184 people). Weight against crowding: research `text-presentation.md` B2.1 ("one cue down is enough"; weight noise when used widely). Weight against text *hue* (warm or cool): nothing.
- Verdict: **partly** (lightness covered; crowding in research; hue a gap with no evidence found).
- Sound: the lightness effect is real but small (irradiation; the Material study found no readability change). No source read in this session ties the best weight to a text colour's *temperature*; the founder's example may be true by look but is unsourced. It is a fair research sub-question, at low priority.

**N19d. The founder's worry ("our research doesn't oversimplify the questions it asks or the answers it finds")**
- Finding from this audit: the main loss is not in the research but between research and the references. `docs/research/text-presentation.md` (#123) holds about 20 conditioned principles (B1.1–B6); `references/text-presentation.md` carries 2 (tint, links). Weight, letter spacing, opacity, text steps, emphasis, caps and numerals stay where no critic reads them. The same holds in smaller measure for `surface-styling.md` (#117): B1.3 (one card type per surface family), B4.2 (zebra striping), B5.1 (named surface levels; only its 1.1:1 border threshold reached interaction 2) and B5.3 (no bright or contrasting container fills) are research only (checked by grep of the reference, 15 Oct 2026). This is input for #203 (why #104 and #101 missed gaps) and #211/#212 (how rules reach the critics).
- Research question for #206 and #211: *Which conditioned principles in `docs/research/` never reached a reference, and should each reach the builder, the critic, or neither?*

## Summary table

"Ref" = a house reference (reaches a critic). "Res" = `docs/research/` only. "imp" = impeccable 4.5.0 only (reaches a critic only with design mode on). T = timeless, E = era-bound.

| Note | Sub-question | Verdict | House location | Soundness of the note's claim | Era |
|---|---|---|---|---|---|
| N1a | Characters per line (70–80?) | covered | Ref `design-critique/SKILL.md:65`; `impeccable.md:83` | Partly: 70–80 is the top of the range; core 45–75 (Baymard 50–75, Butterick 45–90), WCAG AAA ceiling 80. House cites Butterick 45–90 for a 75 cap | T |
| N1b | Font size | covered (body); scale is the project's | `impeccable.md:104`; Res P29 | Sound (Butterick 15–25 px) | E |
| N1c | Body weight | partly | Res #123 B5.3; `impeccable.md:74` | Sound | T |
| N1d | Letter and line spacing | partly / covered | Res B2.3; `impeccable.md:84,104` | Sound | T |
| N1e | Text hue / opacity by context | covered (hue) / partly (opacity, steps) | Ref `text-presentation.md:9-16`; Res B1.3–B1.5 | Sound | E |
| N1f | Left, right, centre alignment | partly (justified only) | `impeccable.md:104` | Sound (WCAG 1.4.8; Butterick: centre short phrases only) | T |
| N1g | Orphans, `text-wrap` | gap | imp `craft-floor.md:12` ("balanced headings") | Sound; `pretty` not Baseline | E |
| N1h | Width text takes in a section | partly | Ref Measure lens (line only) | Sound | T |
| N1i | Bold, italic, resize, recolour | partly | Res B2.1–B2.2; P24 | Sound | T |
| N2a | Section background colours | gap | nearest Ref `surface-styling.md:55-62`; Res B5.1 | Sound; false-floor cost (NN/g 2016) | T / E |
| N2b | Subtle gradient vs solid | gap (bans only) | DNA line 4; imp bans | Sound as a question; no source found | E |
| N3a | Hierarchy "always" beats semantics | covered (destructive steps partly) | Ref `house-principles.md:16,73,76,95`; gate `vault.primary-action`; Res #127 B3 | Partly: "always" too strong; hierarchy sets the rung, semantics the hue (Carbon danger primary/tertiary; Apple: destructive never primary) | T |
| N3b | Buttons sized by purpose | partly | Res `function-fit.md:112` | Partly: Apple "style not size" in groups; Carbon one size per group; M3 Expressive larger key action | T / E |
| N4 | Variable fonts | gap (choice) / partly (rendering) | Res #123 B5.2 | Sound when 3+ styles or axes used (web.dev) | E |
| N5 | Outer rings vs borders | gap (resting edges); covered (focus) | Ref `surface-styling.md:64-71` | Sound; ring = box-shadow, removed in forced-colours (MDN) | E |
| N6 | Dividers in sections and cards | covered | Ref `surface-styling.md:55-62, 93-96` | Sound; add NN/g false-floor condition | T |
| N7 | How busy a page looks | partly | Res #104 W4; Ref brand-layer line; imp `layout.md` | Sound (Tuch 2012; Reinecke 2013) | T / E |
| N8 | Page container borders | partly, by method only | Ref border roles; DNA line 3 | Narrow; no source; fold into N2 or N5 | E |
| N9 | Cool, neutral, warm greys | covered (hue) / partly (temperature as feel) | Ref `text-presentation.md:11-16`; `brand-palette.md:54`; Res B1.1 | Sound (Ou et al. 2004; design systems). Tension: DNA line 5 vs tint rule, a house error #208 rules fixed | E / T |
| N10 | How many fonts | partly | imp `typeset.md:42,57`, `operate.md:13` | Sound (Butterick: a second font usually, a third rarely) | T |
| N11 | Border opacity | partly | Ref `surface-styling.md:11,39`; Res B1.4 | Sound; alpha makes contrast ground-dependent | E |
| N12 | Alignment between sections | partly | Ref Gestalt lens `SKILL.md:52`; imp `polish.md:59` | Sound (good continuation, Wagemans 2012) | T |
| N13 | Contrast alike or different across a site | partly | Ref walk Q5 `house-principles.md:94`; border roles; Res B1.5 | Sound (WCAG 3.2.4; Radix step roles) | T / E |
| N14 | Heading tracking | partly | `impeccable.md:86`; Res `house-audit-method.md:71`, B2.3 | Sound (maker metrics; caps +5–12%) | T |
| N15 | The feel ("energy"): buckets, term, choices | partly | Ref `house-principles.md:16`, `brand-palette.md:15`; library collections; Manta B1 | Sound; term "tone" / "brand personality"; #204 owns it | T / E |
| N16 | Uppercase vs lowercase | partly | Res B2.3; DNA lines 5, 7; `impeccable.md:75` | Sound for short labels; reading-cost belief weaker than assumed (Arditi and Cho 2007) | T / E |
| N17 | Badges and pills vs icons | partly | Ref carriers `house-principles.md:73-76`; gate `vault.borrowing` | Sound (NN/g 2014: icons need labels) | E / T |
| N18 | Responsive: sidebars collapse | partly | gate `vault.layout`; `impeccable.md:77,89`; imp `adapt.md` | Sound (Android window size classes; WCAG 1.4.10) | E |
| N19a | Rules record context | covered (form) | every Ref; Res principle-interactions | Sound; completeness is #206 | T |
| N19b | Typeface traits drive size, spacing | gap | imp `typeset.md:21,49` | Sound (MDN font-size-adjust; Legge and Bigelow 2011) | T |
| N19c | Weight by palette, crowding, warm/cool | partly (hue: gap, no evidence) | `impeccable.md:74`; Res B2.1 | Lightness: small effect; temperature: unsourced, so ruled out (#208) | T |
| N19d | Research oversimplified? | finding | — | Main loss is research not carried into references (#123: ~20 principles researched, 2 in the reference) | — |

Counts: covered 4 (N1a, N3a, N6, N19a) plus covered halves of N1b, N1d, N1e, N5, N9; partly 19; gap 6 (N1g, N2a, N2b, N4, N5 resting edges, N19b); not worth its own ticket: N8 (fold in).

## Research questions named for the gaps

#208 fills 1 to 9, with 7 one combined job and 9 without the optional mood-word scale positions; 10 is #210's P8. Order: 5 first, then 4 before 3; the coverage ledger (`docs/coverage-ledger.json`, #215) ranks the rest.

1. Alignment and block width (N1f, N1h, N12): when a page centres, left- or right-aligns text, how a measure-limited column sits in a wide section, which alignment lines hold across sections.
2. `text-wrap` (N1g): which roles take `balance` or `pretty`, and the cost.
3. Section grounds and gradients (N2a, N2b, N8): when a section takes its own ground, how far apart adjacent grounds sit, when a band edge is a false floor, when a gradient has a function, and when a page frame is right.
4. Edges and contrast ladder (N5, N11, N13): border, outline or ring per edge role; alpha against solid; the contrast level per role across a site.
5. Variable fonts and typeface traits (N4, N14, N19b): when a variable font pays, which axes to set, and how size, line height and tracking follow x-height, width and maker metrics.
6. Busyness (N7): measurable features of a busy page and the level per visitor mode.
7. Font count (N10), caps and case (N16), badges and icons (N17), button size and destructive actions (N3): small, likely answered from existing sources.
8. Responsive pattern table (N18): what each structural part becomes at each window class.
9. The feel (N15): #204, plus how one site holds two feels.
10. Carry-over (N19d): which conditioned principles in `docs/research/` never reached a reference, and whether each should.

## Bound

**Read in full:** #205 and #202 bodies; `plugin/skills/design-critique/references/house-principles.md`, `text-presentation.md`, `surface-styling.md`, `brand-palette.md`, `first-visit-trust.md`; `plugin/skills/design-critique/SKILL.md`; `plugin/skills/design-round/references/impeccable.md`; `docs/research/text-presentation.md`; `docs/research/design-coverage-gaps.md` (except W1–W3, W6–W9, W11–W12, W14 bodies, which I skipped as off-topic); impeccable 4.5.0 `reference/typeset.md`, `craft-floor.md`, `layout.md`; House DNA (`dna` in `data/gallery.json`); the issue resolutions of #86, #192 (comments), #101 (resolution lines).

**Sampled (headings, grep, or named sections):** `plugin/skills/design-critique/gate.md` (ids and grep); `plugin/skills/design-round/SKILL.md` §2 (lines 84–100); `docs/research/surface-styling.md` (headings; B1.1–B1.5, B4, B5, B9 read; grep for rings, opacity, gradient); `docs/research/principle-interactions.md` (summary, §1, §2 read; §3–§5 by grep); `docs/research/function-fit.md` (headings; B3, B4.1 read; grep); `docs/research/house-audit-*.md` (headings and summary tables; house-audit-method items 3 and 4 by grep); `docs/research/adopt-or-build.md` (grep for type); `docs/research/manta-element-coverage.md` (grep; §2.9); `docs/research/design-rules-census.md` (grep for energy); `docs/research/manta-design-migration.md` (grep); `docs/research/impeccable-checks.md:70-76` (detector rule list); impeccable 4.5.0 all `reference/*.md` and `SKILL.md` by grep for each note's terms, plus `new-work.md:40-75`; `data/gallery.json` collections (names, first entry) and `design_words` (first 3); closed issues found by `gh issue list --state all --search` for 35 terms (titles), with #118, #183 and #24 grepped.

**Web sources read (fetch tool, 15 Oct 2026):** Butterick line-length, centered-text, mixing-fonts; W3C Understanding 1.4.8; Baymard line-length-readability; MDN `text-wrap`, `@media/forced-colors`, `font-size-adjust`; NN/g "Illusion of Completeness" (2016), "Icon Usability" (2014); Carbon Button usage; web.dev "Introduction to variable fonts on the web"; Tailwind box-shadow (class table only); Radix "Understanding the scale", "Aliasing"; Android window size classes; Reinecke et al. 2013 abstract page.

**Search-snippet level only (not opened at source):** Dyson and Haselgrove 2001; Shaikh and Chaparro (line length); `text-wrap: pretty` browser support; Ou et al. 2004; Arditi and Cho 2007; Legge and Bigelow 2011; Radix alpha scales.

**From my own knowledge, marked in place, not verified this session:** Refactoring UI "Semantics are secondary"; Aaker 1997; Lavie and Tractinsky 2004 (cited by the house, not re-read); Tinker's caps studies; CSS `background-clip` default; design-system font families (Carbon, Apple, GOV.UK); GOV.UK and Material sentence case; banding of subtle gradients on 8-bit displays.

**Not opened:** Manta's own files (owner mantahostels); `docs/research/first-visit-trust.md`, `brand-palette.md`, `de00-*.md`, `function-questions.md`, `visual-critic-reliability.md`, `past-design-rejections.md` and the image-model and library research files; design-round `references/prompts.md`, `polish.md`, `comparison.md`, `gate-check.md`, `calibration.md`, `roster.md`; impeccable 4.2.1; impeccable's detector source (the rule list came from `impeccable-checks.md`); open sibling tickets' bodies (#203, #204, #206–#212: titles only); m3.material.io pages; the full texts of every paper named above.
