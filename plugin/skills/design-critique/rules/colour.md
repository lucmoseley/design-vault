# Rule records: colour

The palette and how colour is used: its roles and distances, logo anchors, tints, contrast minimums, colour as a signal and the theme. The form is [rules.md](../rules.md)'s.

### vault.contrast
- applies-when: web-surface; every line of text, at desktop and phone width
- question: Does all text, generated `::before` and `::after` text included, reach 4.5:1 contrast against what is drawn behind it, or 3:1 where it is large (24 px, or 18.66 px bold), save text in a disabled control, pure decoration, or a logotype the project's rules file names by its CSS selector in §4, which the script exempts and reports?
- answered-by: script
- writes: text contrast
- yields-to: none
- source: WCAG 2.2 success criterion 1.4.3 Contrast (Minimum); strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: value
- script: check-access.py <page> --out <dir>
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: BTN-8, BTN-95, COL-1, COL-2, COL-11, COL-14, COL-21, COL-53, COL-65, COL-66, COL-71, FRM-71, SUR-104, TXL-4, TYS-9, TYS-47
- status: live

### vault.colour-look
- applies-when: web-surface; every state, error, required field, selected option, chart series or other meaning shown in colour, links inside a line of text, a hover tint and a press's darker fill aside
- question: Is every meaning colour carries also carried by text, an icon, a shape or a position, so a visitor who cannot tell the colours apart still gets it?
- answered-by: look
- writes: colour signal
- yields-to: vault.colour-script
- source: WCAG 2.2 success criterion 1.4.1 Use of Color; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: treatment
- target: Carry every meaning shown in colour by text, an icon, a shape or a position as well.
- reasons: design-critique/references/brand-palette.md#colour-never-carries-meaning-alone
- ledger: BTN-74, COL-4, COL-36, COL-62, COL-106, FFB-1, FFB-7, IMG-31, IMG-32, IMG-59, NAV-114, NAV-262, OTH-21, OTH-24
- status: live

### vault.palette-roles
- applies-when: any; every colour in the palette
- question: Does every palette colour hold a job (the main action, text, ground, surface, border, a status), each job one hue family laid out as a ramp of lightness steps, the body of the palette in near hues with one contrasting hue given a single job as the figure, every colour picked in OKLCH or measured in CIELAB rather than HSL, and is a colour with no job dropped?
- answered-by: builder
- writes: palette
- yields-to: vault.logo-anchors, vault.contrast, level 2
- source: Schloss and Palmer 2011 (docs/research/brand-palette.md); Material 3, Radix Colors, Carbon, Apple HIG; W3C CSS Color 4; strength: published research and design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: role
- target: Name each colour by its job, give each job one hue family as a lightness ramp, keep most hues near each other with one contrasting figure hue for one job, work in OKLCH, and drop any colour with no job.
- reasons: design-critique/references/brand-palette.md#a-palette-is-roles
- ledger: BTN-13, COL-22, COL-23, COL-25, COL-32, COL-33, COL-34, COL-42, COL-43, COL-78, SUR-62
- status: live

### vault.render-palette-look
- applies-when: brand-art; every render whose brief rules a palette
- question: Leaving aside its shadows, its glints and the soft blends between two ruled colours, does the bulk of the render read as the colours the brief rules, and does every ruled colour appear in it?
- answered-by: look
- writes: palette
- yields-to: vault.palette-roles, level 2
- source: #338's research (docs/research/render-palette-plain-area.md §1): each pixel's distance to its nearest palette colour is the published measure (Lin & Hanrahan 2013), read in both directions, every image colour near a palette colour and every palette colour present (Aharoni et al. 2025); no study, standard or brand tool sets how much of a render may stray, and a render that kept its palette failed every strict line on its shading, so where the bulk ends is the critic's judgement, no number having been found (#339 closed not planned; #350 ruled no look test); strength: published research for what to look at, the critic's judgement for the line
- era: timeless
- owner: vault
- stage: treatment
- target: Prompt and pick renders whose broad areas sit in the brief's ruled colours, each of them used somewhere, with only shading, highlights and blends between them falling outside.
- reasons: design-round/references/prompts.md#art-direction--the-model-agnostic-template
- ledger: none
- status: live

### vault.colour-distance
- applies-when: any; every pair of colours that can share a view, a ramp's own steps aside
- question: Measured in ΔE00 (never ΔEOK scaled), is every pair of colours that can share a view either one token or as far apart as the lookup below asks, with two meanings in one view also carried by a label or an icon?
- answered-by: builder
- writes: colour difference
- yields-to: vault.logo-anchors, vault.contrast, level 2
- source: W3C CSS Color 4 §14.2.1 for under 2; Brychtová and Çöltekin 2016 for 10 between meanings; the founder's rulings on #178 for 20 on small marks, the near-miss line at 10 and 3 for surfaces; Williams, The Non-Designer's Design Book, and Apple HIG Color for the rule; strength: founder ruling for 20, 10 and 3, standard and peer-reviewed research for the rest
- era: timeless
- owner: vault
- stage: value
- inputs: ΔE00 between the pair; whether they are two large greys near the page ground sharing an edge (a grey tinted up to OKLCH chroma 0.05 counts as grey); whether they carry two meanings in one view; whether either is a small mark (a dot, a thin line, small text)
- output: under 2, one token; two large greys near the ground sharing an edge, 3 or more; two meanings, 10 or more on large areas and 20 or more on small marks; any other pair, 10 or more; a pair between 2 and its line is a near-miss to snap together or move apart
- target: Run design-project's palette.py over the palette and the logo colours, and snap together or move apart every pair it flags.
- reasons: design-critique/references/brand-palette.md#the-same-colour-or-clearly-different
- ledger: COL-4, COL-6, COL-34, COL-36, COL-62, COL-78, COL-106, SUR-62
- status: live

### vault.logo-anchors
- applies-when: any; a project with a client logo or a brand colour the client chose, against every palette colour
- question: Is each logo colour held fixed unless the client opens it, either joining the palette as a token with a job or declared logo-only, with neutrals and dark grounds taking an anchor's hue at low chroma, every other hue a figure with one job, the palette moved to the anchor and never the anchor to the palette, any hue shift toward the main hue (at most 15°) made to interface colours only, an anchor that fails 4.5:1 as text given a text-safe partner, and every ground drawn from an anchor's hue clearing 3:1 against every logo colour?
- answered-by: builder
- writes: palette anchors
- yields-to: vault.contrast, level 2
- source: W3C Understanding SC 1.4.3 and 1.4.11, on logo colours fixed by brand guidelines; GOV.UK's palette drawn from its wordmark, Material 3's fidelity scheme and harmonize, Spotify's logo kept apart from its interface colours; impeccable `colorize` (weak); the house, from Manta's and mmm-infra's measured cases, for measuring against anchors and who moves; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: role
- target: Ask whether the logo's colours are fixed; build the palette around them in OKLCH, tinting neutrals and dark grounds toward an anchor's hue, and snap any near-miss palette colour to the anchor, never the logo file to the palette.
- reasons: design-critique/references/brand-palette.md#fixed-logo-colours-are-anchors
- ledger: COL-14, COL-21, COL-28, COL-32, COL-35, COL-78
- status: live

### vault.text-tint
- applies-when: web-surface; every text colour and neutral grey
- question: Is any tint on text and neutral greys toward the brand's main hue alone, never toward a spot accent, at about OKLCH chroma 0.01–0.03 (up to 0.05 for a deliberate blue-grey) falling toward white, made in OKLCH or HCT rather than HSL or Sass `darken()` and `lighten()`; on a page of several strong hues or many photographs, the dominant hue or pure grey as the project's rules file picks; and secondary text on a coloured ground in that ground's own hue at another lightness?
- answered-by: builder
- writes: text tint
- yields-to: vault.contrast, level 2
- source: Material 3 `material-color-utilities`, Radix Colors, Tailwind v4 neutrals; Evil Martians on OKLCH, Sitnik and Turner 2025; impeccable `colorize` (weak); strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: treatment
- target: Tint text and greys toward the main hue at low chroma in OKLCH, or keep them pure grey; on a coloured ground, take that ground's hue for secondary text; measure contrast after tinting on every ground.
- reasons: design-critique/references/text-presentation.md#the-tint-rule
- ledger: COL-15, COL-40, COL-41, COL-42, COL-43, COL-53
- status: live

### vault.dna-near-black
- applies-when: web-surface; every near-black ground and text colour, on a project that takes the House DNA
- question: Is each near-black either tinted toward the brand's main hue as `vault.text-tint` sets, or a pure grey that the rules file or the brief picks?
- answered-by: whole-page
- writes: near-black
- yields-to: vault.text-tint, vault.logo-anchors, level 2
- source: House DNA `never` line 5, from Anthropic `frontend-design` SKILL.md (anthropics/skills 41bbe19, 3 Sep 2026), trait 5, template chrome; strength: model maker's AI-look calibration
- era: dated 2027-04-14
- owner: vault
- stage: treatment
- target: Take every near-black from the palette, tinted toward the main hue at low chroma, or pure grey only where the brief or the rules file picks it.
- reasons: design-critique/references/text-presentation.md#near-black-and-the-house-dna
- ledger: none
- status: live

### vault.chroma-ends
- applies-when: any; every colour near white or near black
- question: Does each colour's chroma fall as its lightness nears white or black, staying inside the gamut there?
- answered-by: whole-page
- writes: chroma at the ends
- yields-to: vault.text-tint, level 2
- source: W3C CSS Color 4 gamut mapping; strength: standard
- era: timeless
- owner: vault
- stage: treatment
- target: Lower chroma on the lightest and darkest steps of every ramp.
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: COL-40
- status: live

### vault.theme
- applies-when: web-surface; the page's light and dark themes
- question: Does a project with both themes follow the visitor's system setting, one with a single theme ship light unless its rules file rules dark, and is any dark theme designed for its own grounds rather than the light one inverted?
- answered-by: whole-page
- writes: theme
- yields-to: level 2
- source: Apple HIG Dark Mode; NN/g 2020, on dark mode; strength: domain evidence
- era: dated 2027-10-14
- owner: vault
- stage: function
- target: Follow `prefers-color-scheme` where both themes exist; ship light for reading where one does, unless the rules file rules dark; design a dark theme's grounds, text and elevation for dark.
- reasons: design-round/references/impeccable.md#conditions-added
- ledger: COL-46, COL-47, COL-49, COL-78, OTH-47, SUR-65
- status: live

### vault.body-ink
- applies-when: web-surface; body text on a light ground
- question: Is body text on a light ground a near-black or dark grey at 7:1 or more against its ground, about 12:1 where the brand allows, rather than a mid grey?
- answered-by: script
- writes: body text colour
- yields-to: level 2
- source: Apple HIG Dark Mode, "no lower than 4.5:1 … strive for a contrast ratio of 7:1, especially in small text" (6 Aug 2024); USWDS Color, "Avoiding pure black text on a white background helps dyslexia, Irlen Syndrome, light sensitivity, and autism" (as read Oct 2026); Butterick, Practical Typography, "Color", "on screen, dark-gray text can be more comfortable to read than black text"; Typography Handbook (2026), "#161616 or #333 is easier to read at length with no accessibility cost"; the 12:1 aim is #333 on white (12.6:1), the house's reading of that example and of Legge (1987) read second-hand in research B1.2; strength: design-system guidance
- era: timeless
- owner: vault
- stage: value
- target: Set body text on a light ground in a dark grey or tinted near-black at about 12:1, never under 7:1; pure black is allowed but not the default.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/text-presentation.md#near-black-body-text
- ledger: COL-17
- status: staged

### vault.text-steps
- applies-when: web-surface; every ground that holds text
- question: Does each ground hold at most two readable text colours, primary about 12:1 and secondary 4.5:1 or more, each a solid colour measured on that ground, plus a defined placeholder colour at 4.5:1 and a defined disabled colour, with further rank carried by weight, size and space rather than a third grey?
- answered-by: script
- writes: text colour steps
- yields-to: level 2
- source: Radix Colors, "Understanding the scale", steps 11 and 12 "designed for text", low- and high-contrast (as read Oct 2026); Apple HIG Color, label and secondary label (16 Dec 2025); W3C Understanding SC 1.4.3, which "applies to … placeholder text" and exempts disabled controls; NN/g, Gordon, "Visual Hierarchy in UX" (2021); the primary's 12:1 is the house's figure, as in `vault.body-ink`; strength: design-system guidance
- era: timeless
- owner: vault
- stage: value
- inputs: the grounds that hold text, the text's role (primary, secondary, placeholder, disabled)
- output: per ground, primary about 12:1 and secondary 4.5:1 or more, both solid; placeholder 4.5:1 or more; disabled defined, free of the contrast floor and may be an opacity; a third readable grey is refused, and its rank goes to weight, size or space
- target: Give each ground two text colours, primary near 12:1 and secondary at least 4.5:1, plus a placeholder at 4.5:1 and a disabled colour; rank anything further by weight, size and space.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/text-presentation.md#two-text-colours-per-ground
- ledger: COL-18, TYS-27
- status: staged

### vault.text-on-dark
- applies-when: web-surface; text on a dark ground: a dark theme, a night section, a dark nav or footer
- question: On a dark ground, is primary text an off-white at about 10:1 rather than pure white on near-black, secondary text 7:1 or more where it is small, and is a status shown by a coloured border, icon or chip beside off-white text rather than by small coloured text?
- answered-by: script
- writes: text colour on dark
- yields-to: level 2
- source: Typography Handbook, "Dark mode typography" (2026), text #e0e0e0–#f0f0f0 on #121212–#1a1a1a, "around 10:1 rather than the maximum possible"; Apple HIG Dark Mode, 4.5:1 floor and "strive for … 7:1, especially in small text" (6 Aug 2024); Apple HIG Color, "Color in lightweight text or small areas can make them harder to see" (16 Dec 2025); strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: value
- inputs: the ground's colour, the text's role and size
- output: primary off-white at about 10:1 (never pure #FFF on #000); secondary 7:1 or more under 24 px (18.66 px bold), 4.5:1 at or above; status carried by a border, icon or chip with off-white text
- target: On a dark ground set text in an off-white near 10:1, secondary text at 7:1 when small, and show status by a coloured border, icon or chip, not coloured small text.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/text-presentation.md#text-on-a-dark-ground
- ledger: COL-52
- status: staged

### vault.controls-on-photo
- applies-when: web-surface; every control set over a photograph or video: carousel arrows and page dots, save and share buttons
- question: Does each control over a photo or video carry its own backdrop, halo or shadow so its glyph or edge holds 3:1 against the lightest and darkest image under it, and does the current page dot differ from the rest by fill, size or shape rather than a slight opacity change?
- answered-by: script
- writes: control contrast on images
- yields-to: level 2
- source: Baymard, "Page Control UI" (15 May 2026), "a light dot on a light sky or a dark dot on a dark product image can disappear entirely. A semi-transparent backdrop or subtle drop shadow behind the indicator group is an effective solution", and a faint opacity difference "can render the active state invisible"; NN/g, Pernice, "Carousel Usability" (2013, reviewed Aug 2026), buttons "on top of a busy background are not easy to notice or click"; Apple HIG Page controls, "A solid dot denotes the current page" (2023); W3C Understanding SC 1.4.11 and technique G18; strength: WCAG 2.2 AA for the 3:1, expert guidance for the rest
- era: timeless
- owner: vault
- stage: treatment
- target: Give every control on a photo or video its own backdrop or shadow, clearing 3:1 over the worst image under it, and mark the current dot by fill or size.
- script: check-access.py <page> --out <dir> [--parts <declaration>]
- parts: image, video
- reasons: design-critique/references/text-presentation.md#controls-on-photos
- ledger: COL-77, BTN-10
- status: staged

### vault.dark-ground
- applies-when: web-surface; the base ground of a dark theme or a dark section
- question: Is each dark base ground a near-black, OKLCH lightness about 0.18–0.22 (#121212 to #1a1a1a as a pure grey), rather than pure black, save a slide or media view watched in a dim room, which may take black?
- answered-by: script
- writes: dark ground lightness
- yields-to: level 2
- source: material-components-android `docs/theming/Dark.md` (16 May 2024, as read Oct 2026): background and surface "dark grey instead of black, which increases visibility for shadows and also reduces eye strain for light text"; Typography Handbook, "Dark mode typography" (updated for 2026): pure black under white text "causes halation", and "A background of #121212 – #1a1a1a"; Butterick, "Presentations": a slide in a dimmed room starts "with a black background. Not dark gray"; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Set a dark base ground near black, OKLCH L about 0.18–0.22 and tinted as `vault.dna-near-black` allows, never #000, unless it is a slide or media view meant for a dim room; raise surfaces above it per `vault.dark-elevation`.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/text-presentation.md#a-dark-ground-is-near-black
- ledger: COL-51
- status: staged

### vault.colour-pair
- applies-when: web-surface; every element whose text colour or background colour the page sets
- question: Wherever the page sets a text colour, does it or an ancestor also set a background colour, and wherever it sets a background colour, a text colour, so a visitor's own default colours never meet the page's half of the pair?
- answered-by: script
- writes: text and background colour pairing
- yields-to: none
- source: WCAG 2.2 failure F24, "Failure of Success Criterion 1.4.3, 1.4.6 and 1.4.8 due to specifying foreground colors without specifying background colors or vice versa" (as read Oct 2026); strength: WCAG 2.2 failure technique
- era: timeless
- owner: vault
- stage: value
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#colour-pairs
- ledger: COL-105
- status: staged

### vault.image-fallback-colour
- applies-when: web-surface; every element that sets text over a background image
- question: Does every element that sets text over a background image also set a background-color beneath the image that holds the text's contrast if the image does not load?
- answered-by: script
- writes: fallback colour under a background image
- yields-to: none
- source: MDN, "Backgrounds and borders", Accessibility considerations: "you should also specify a `background-color` that will allow the text to be legible if the image does not load"; WCAG 2.2 failure F24: background colour may be set by a background image, whose contrast is checked in case images are not displayed (both as read Oct 2026); strength: platform documentation and WCAG failure technique
- era: timeless
- owner: vault
- stage: value
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#colour-pairs
- ledger: COL-12
- status: staged

### vault.color-scheme
- applies-when: web-surface; the page's root and head
- question: Does the page declare `color-scheme` on `:root`, naming each scheme it styles (`light`, `dark` or both), with a matching color-scheme meta tag in the head before any CSS?
- answered-by: script
- writes: color-scheme
- yields-to: vault.theme
- source: MDN, `color-scheme` (last modified 21 Jul 2026, as read Oct 2026): the browser matches "The color of the canvas surface", scrollbars, form controls and "other browser-provided UI"; declare it on `:root` and in a `<meta name="color-scheme">` before the CSS to avoid "unwanted screen flashes"; strength: platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: value
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#browser-drawn-parts-follow-the-scheme
- ledger: COL-99
- status: staged

### vault.caption-colours
- applies-when: web-surface and has-motion; every video with captions
- question: Do captions keep the WebVTT default, white text on black at 80% opacity, or an author `::cue` style that holds 4.5:1 against its own background, and does a custom player leave the viewer able to change caption colour, opacity, size and background?
- answered-by: builder
- writes: caption colours
- yields-to: none
- source: W3C WebVTT §7, CSS rendering: cue `color` "rgba(255,255,255,1)" and cue background "rgba(0,0,0,0.8)"; 47 CFR 79.103(c): US video apparatus lets the viewer set caption character colour, opacity, size, background colour and opacity, and edges; WCAG 2.2 SC 1.4.3, 4.5:1 for text (all as read Oct 2026); strength: web standard and US regulation
- era: timeless
- owner: vault
- stage: treatment
- target: Leave captions white on 80% black, or style `::cue` with a background that holds 4.5:1; in a custom player, keep the viewer's caption colour, size and background settings.
- parts: video
- reasons: design-critique/references/surface-styling.md#caption-colours
- ledger: COL-104
- status: live

### vault.colour-in-place
- applies-when: any; every palette colour, while it is chosen
- question: Was each palette colour judged rendered on every ground it will sit on and beside the neighbours it will touch, rather than as a swatch on white?
- answered-by: builder
- writes: where a colour is judged
- yields-to: level 2
- source: Chevreul, The Principles of Harmony and Contrast of Colours, tr. Martel, §16: two contiguous colours "will appear as dissimilar as possible, both in their optical composition and in the height of their tone"; Butterick, Practical Typography, "Presentations": a pale grey reads as grey beside white and as white on its own, "an optical phenomenon known as simultaneous contrast"; strength: published research
- era: timeless
- owner: vault
- stage: role
- target: Judge and adjust each palette colour rendered on every ground it will sit on and beside each neighbour it will touch, never as a swatch on white.
- reasons: design-critique/references/colour-interaction.md#a-colour-is-judged-in-place
- ledger: COL-108
- status: live

### vault.vibrating-edge
- applies-when: any; every edge where two saturated colours of strongly different hue touch: a coloured button on a coloured ground, coloured text on a coloured field, a logo colour on a brand field
- question: Where two saturated colours of strongly different hue touch below a contrast ratio of 3:1, with no white or black between them, does their edge, seen rendered, hold still rather than shimmer or seem to float?
- answered-by: look
- writes: adjacent saturated pair
- yields-to: level 2
- source: MDN, "Colors and luminance", working with blue (as read Oct 2026): "a pure red and a pure blue color that are immediately adjacent and touching may 'shimmer'"; Adobe Spectrum, "Using color": colours with "a high degree of hue contrast with near-equal saturation or lightness" create "a visual illusion of depth or vibration (chromostereopsis)", and "Use static white or static black components instead of colored components on top of color or image backgrounds"; a pair at 3:1 or more has a clear lightness edge and is not judged, and below it the pair is looked at rendered, as docs/research/brand-palette.md §1.2 says, since no source gives the gap where vibration stops (its Gaps 2); strength: platform documentation and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Where two saturated colours of strongly different hue must touch, separate them in lightness to a contrast ratio of 3:1 or more, or set white or black between them.
- reasons: design-critique/references/colour-interaction.md#vibrating-edges
- ledger: COL-107
- status: staged

### vault.imagery-colour
- applies-when: web-surface; every part on or beside a photograph or artwork: a hero's text and buttons, a card over its image, a section beside its illustration
- question: Do the colours of parts near a photograph or artwork sit with it, accents drawn from the image or checked beside it, while controls over a colourful image stay neutral or clearly apart from its colours?
- answered-by: look
- writes: colour near imagery
- yields-to: vault.logo-anchors, vault.palette-roles, level 2
- source: Apple Human Interface Guidelines, Color, best practices (changed Dec 2025): "Consider how artwork and translucency affect nearby colors", and "Avoid using similar colors in control labels if your app has a colorful background"; material-components-android, Color, content-based dynamic colour (as read Oct 2026): a scheme derived from in-app content "such as album artwork, a brand logo, or a video tile"; the founder on lucmoseley/mmm-infra#8, "it's hard to choose the right colors before having the right photograph ... it's also hard to choose the right photo before having the right colour palette" (docs/research/past-design-rejections.md B11); strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: role
- target: Choose the palette with the key photograph or artwork in view, drawing accents from it or checking them beside it, and keep controls over a colourful image neutral or clearly apart from its colours.
- reasons: design-critique/references/colour-interaction.md#colour-from-imagery
- ledger: COL-55
- status: staged

### vault.contrast-ladder
- applies-when: web-surface; every line of text, every icon and every edge, at desktop and phone width
- question: Does each part keep the contrast its role takes in the lookup below, against what is drawn next to it?
- answered-by: script
- writes: contrast by role
- yields-to: vault.contrast, vault.control-edges, vault.focus
- source: W3C Understanding SC 1.4.3, 1.4.6 and 1.4.11 (WCAG 2.2, 2023; pages updated 6 Sep 2026), thin strokes harder to read at low contrast, an icon that identifies a control at 3:1, a boundary needed only where nothing else shows the control, and thin lines rendered fainter than their colour; Apple HIG Dark Mode, "strive for a contrast ratio of 7:1, especially in small text" (6 Aug 2024); decorative edges in @atlaskit/tokens 20.6.1 `color.border` (1.35:1 light, 1.39:1 dark), Material 3 `outlineVariant` (1.6:1 light, 2.0:1 dark, Compose tokens v0_210) and GOV.UK `border` (1.6:1), all as read Oct 2026; strength: design-system guidance over WCAG 2.2 AA, the 7:1 aim for thin faces and the 4.5:1 aim for 1 px lines the house's mapping
- era: timeless
- owner: vault
- stage: value
- inputs: the part's role; for text, its size and weight and the face's stem (face-profile.py `stem`)
- output: body and secondary text 4.5:1, aiming at 7:1 (SC 1.4.6) where the face's stem is under 0.06 em or the weight is under 400; large text (24 px, or 18.66 px at 700) 3:1, aiming at 4.5:1 on the same thin-face terms; an icon or edge that is a control's only identifier, a state mark and a chart mark 3:1, a 1 px line aiming at 4.5:1 because anti-aliasing fades it; an icon beside its own text label, no floor; a decorative edge or divider about 1.3–2:1 and no floor; focus, as `vault.focus` measures it; disabled, as `vault.disabled-legibility` sets it
- target: Pick each colour pair by the part's role: body text at 4.5:1 or more and 7:1 for a thin face, large text at 3:1, an edge or icon that alone shows a control at 3:1, and 4.5:1 for a 1 px line, and a decorative edge at about 1.3–2:1.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/edges-and-contrast.md#contrast-by-role
- ledger: COL-1, COL-2
- status: staged

### vault.theme-contrast
- applies-when: web-surface; every colour scheme the page ships: light, dark, and `prefers-contrast: more` where the page styles it
- question: Measured in each colour scheme the page ships, separately, does every part reach the contrast `vault.contrast-ladder` gives its role, on the same rung in light and dark and a higher rung under more contrast?
- answered-by: script
- writes: contrast per colour scheme
- yields-to: vault.contrast-ladder
- source: Atlassian Elevation, "Don't assume that because UI is accessible in light mode, it will be in dark mode", and its increased-contrast themes (@atlaskit/tokens 20.6.1, as read Oct 2026); Apple HIG Accessibility, "check the minimum contrast in both light and dark appearances" (9 Jun 2025), and Color, an increased-contrast variant of each custom colour (16 Dec 2025); Material 3 contrast curves, one minimum per role in light and dark, rising with the contrast level (material-color-utilities, 20 Jan 2026); strength: design-system guidance over WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: value
- target: Give each role the same contrast in light and dark and more under `prefers-contrast: more`, and measure each scheme separately.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/edges-and-contrast.md#contrast-by-role
- ledger: COL-53
- status: staged

### vault.fill-text
- applies-when: web-surface; every piece of text and every icon on a coloured or dark fill: a button, badge, banner, band or section ground
- question: Does text on a fill take the polarity the lookup below gives, a mid-tone fill that fails 4.5:1 both ways moved lighter or darker rather than given a size workaround, and a same-hue text partner at least 50 USWDS grades from its fill?
- answered-by: script
- writes: text polarity on a fill
- yields-to: vault.contrast, vault.logo-anchors
- source: MDN `contrast-color()`, white or black by the greater contrast, mid-tones failing both (22 Apr 2026), Baseline 2026-04-10; USWDS magic number, a grade gap of 40 for AA large text, 50 for AA, 70 for AAA (as read Oct 2026); Atlassian inverse tokens on bold fills, with yellow's own warning.inverse; Radix Colors step 9, white text but for Sky, Mint, Lime, Yellow and Amber; Chrome, "CSS relative color syntax" (2023), an L* gap of about 50 for medium contrast; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- inputs: the fill's relative luminance Y; for a same-hue partner, the two colours' USWDS grades or their OKLCH lightness
- output: white text where Y is under 0.179, where white and black tie at 4.58:1, black or the near-black text colour above it; a fill that leaves the chosen polarity under 4.5:1 moves away from Y 0.179; a same-hue partner 50 grades or more away (40 for large text and icons), about 0.5 OKLCH lightness (0.4 for large text and icons)
- target: Set white text on a fill whose luminance is under 0.179 and near-black text above it, and move a mid-tone fill until one of them clears 4.5:1.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/edges-and-contrast.md#text-on-a-fill
- ledger: COL-14
- status: staged

### vault.tone-colour-share
- applies-when: any; the whole asset, every view, against the tone the brief or direction card states in its tone line
- question: Does the share of the surface in colour match the stated energy and the visitor mode by the lookup in `output`, with neutrals carrying the rest and one hue leading rather than several at equal weight?
- answered-by: whole-page
- writes: share of surface in colour
- yields-to: vault.calm-colour-share, vault.brand-layer, level 2
- source: Atlassian Design, Color, neutrals on "most backgrounds, text, and shapes"; USWDS theme tokens, 60/30/10 across the non-neutral families with the neutral base predominant; Reinecke and Gajos, CHI 2014, colourfulness appeal peaking moderate-to-high and varying by audience; Rauno, "Novelty" (Feb 2026), the small accent share; impeccable 4.5.0 `new-work.md` §4 colour strategies (as read Oct 2026); the bands are the house's lookup; strength: published research and design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: role
- inputs: the stated energy (calm, middle, loud); the visitor mode of the view or zone (operate or read, persuade or experience), a hero or marketing zone of a working product counting as persuade
- output: calm, or an operate or read view: restrained, neutrals carry the surface and colour sits on actions, status and one accent, about a tenth; middle: full palette, the neutral base predominant and the colour split about 60/30/10 across its families; loud on a persuade or experience surface: committed, one hue carrying 30–60% of the surface, or drenched, the surface in that hue; an operate or read surface never goes past full palette
- target: Set how much of the surface is in colour from the tone's energy and the visitor mode by the lookup, let one hue lead, and keep neutrals on the rest.
- reasons: design-critique/references/tone.md#colour-share
- ledger: COL-24
- status: live

### vault.calm-colour-share
- applies-when: any; the whole asset, every view, against the tone the brief or direction card states in its tone line
- question: Where the brief's energy is calm, is a tenth of the page or less in colour (OKLCH chroma 0.05 or more)?
- answered-by: script
- writes: share of surface in colour
- yields-to: none
- source: Atlassian Design, Color, neutrals on "most backgrounds, text, and shapes"; USWDS theme tokens, 60/30/10 across the non-neutral families with the neutral base predominant; Reinecke and Gajos, CHI 2014, colourfulness appeal peaking moderate-to-high and varying by audience; Rauno, "Novelty" (Feb 2026), the small accent share; impeccable 4.5.0 `new-work.md` §4 colour strategies (as read Oct 2026); the bands are the house's lookup; strength: published research and design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: role
- target: Keep a calm page to about a tenth of its surface in colour.
- script: check-style.py <page> --out <dir> --brief energy=<calm, middle or loud> [--parts <declaration>]
- reasons: design-critique/references/tone.md#colour-share
- ledger: COL-24
- status: live

### vault.tone-saturation
- applies-when: any; every palette colour, against the tone the brief or direction card states in its tone line
- question: Does the palette's chroma sit at the stated energy, higher for a louder tone and lower for a calmer one, with the highest chroma spent where attention should go, no neon outside it, and every colour inside the display's gamut?
- answered-by: whole-page
- writes: saturation
- yields-to: vault.contrast, vault.logo-anchors, vault.brand-layer, level 2
- source: Valdez and Mehrabian 1994, J Exp Psych: General 123(4), "Arousal = -.31B + .60S"; Wilms and Oberfeld 2018, Psychological Research 82(5), saturated and bright colours with higher arousal; NN/g, Gordon, "Good Visual Design" (14 Nov 2025), one site's greens "neither too bright nor overly saturated" and caution with neon; jakub.kr, "OKLCH colors" (2025), maximum chroma by gamut; strength: published research and expert guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Raise chroma for a louder tone and lower it for a calmer one, keep the most saturated colour for what should draw the eye, and keep every colour inside the gamut.
- reasons: design-critique/references/tone.md#saturation
- ledger: COL-27
- status: live

### vault.image-wash
- applies-when: web-surface; every wash, tint or gradient laid over a background image
- question: Is a wash over a background image the lightest that lets the worst image the slot can hold clear the text floor where text sits on it, and under 0.9 alpha so the image still shows, with the text moved off the image or onto a panel wherever only 0.9 or more would clear it?
- answered-by: script
- writes: wash opacity
- yields-to: vault.photo-text-fix, vault.contrast
- source: impeccable engine 0.1.11 rule `buried-raster`, "Let the material show (a tint under 0.9 alpha, a blend mode, an opacity you can see) or remove the file" (as read Nov 2026); NN/g, "Text Over Images" (updated 13 Jan 2026), a box raised from 30% to 50% to pass; W3C failure F83, measured at the lightest or darkest part of the image under the text (WCAG 2.2, 2023); strength: WCAG 2.2 AA and domain evidence for the floor; impeccable alone for the 0.9 ceiling
- era: timeless
- owner: vault
- stage: value
- inputs: whether text sits on the image; the wash alpha at which the worst image the slot can hold clears the text floor under the text
- output: no text: any alpha under 0.9; text: that clearing alpha where it is under 0.9; 0.9 or more needed: move the text off the image or set it on a panel per vault.photo-text-fix
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/grounds-and-gradients.md#washes-over-a-background-image
- ledger: COL-13
- status: staged

### vault.gradient-function
- applies-when: web-surface; every gradient, glow or pattern drawn behind content
- question: Does every gradient, glow or pattern behind content do one job (a scrim under text on an image, a light or depth cue on a raised surface, a brand ground where vault.tone-colour-share lets the surface go committed, an ambient pattern on a message or promotional area, a chart or progress ring), with none behind a region visitors work in, per vault.decoration-place?
- answered-by: look
- writes: gradient use
- yields-to: vault.gradient-place, vault.decoration-place, vault.brand-layer, vault.ai-look
- source: Atlassian Design, Illustrations, Ambient pattern, "Use patterns for messages or promotional areas that need visual interest but don't require a specific conceptual image" (as read Nov 2026); Krehel, "Understanding gradients" (as read Nov 2026), radial "for glows, backgrounds or depth lighting", conic "for charts, rings"; NN/g, "Text Over Images" (updated 13 Jan 2026), a fade under text; impeccable 4.5.0 `quieter.md`, "Remove decorative elements: Gradients, shadows, patterns, textures that don't serve purpose", and engine 0.1.11 rules radial-halo and radial-spotlight-glow; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Give every gradient, glow or pattern one job (a text scrim, a light cue, a brand ground where colour may lead, an ambient pattern on a promotion, a chart), and keep all of them out of working regions.
- reasons: design-critique/references/grounds-and-gradients.md#when-a-gradient-has-a-function
- ledger: COL-80
- status: staged

### vault.gradient-place
- applies-when: web-surface; every gradient, glow or pattern drawn behind content
- question: Is no gradient drawn behind a form, table, grid, list box or field, no radial gradient behind the hero, and no text given a glow?
- answered-by: script
- writes: gradient use
- yields-to: none
- source: Atlassian Design, Illustrations, Ambient pattern, "Use patterns for messages or promotional areas that need visual interest but don't require a specific conceptual image" (as read Nov 2026); Krehel, "Understanding gradients" (as read Nov 2026), radial "for glows, backgrounds or depth lighting", conic "for charts, rings"; NN/g, "Text Over Images" (updated 13 Jan 2026), a fade under text; impeccable 4.5.0 `quieter.md`, "Remove decorative elements: Gradients, shadows, patterns, textures that don't serve purpose", and engine 0.1.11 rules radial-halo and radial-spotlight-glow; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Keep gradients out of the parts visitors work in, radial halos off the hero, and glows off text.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/grounds-and-gradients.md#when-a-gradient-has-a-function
- ledger: COL-80
- status: staged

### vault.gradient-text
- applies-when: web-surface; every heading or run of text filled with a gradient through `background-clip: text`
- question: Is text given emphasis by weight, size or one solid colour rather than a gradient fill, save a display word in the brand layer that the brief or a direction card earns back, which then clears the text floor at its weakest stop against the ground and keeps a solid `color` under forced colours?
- answered-by: script
- writes: gradient text fill
- yields-to: vault.ai-look, vault.contrast
- source: impeccable 4.5.0 `craft-floor.md`, "Gradient text. Emphasis comes from weight or size."; MDN `forced-colors` (source changed 20 Apr 2026), "background-image is forced to 'none' for values that are not url-based"; W3C technique G18, each letter meeting the ratio against the background immediately behind it (WCAG 2.2, 2023); strength: impeccable "AI look" ban checked against WCAG 2.2 AA and platform documentation
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Emphasise text by weight, size or one solid colour; where the brief earns a gradient word, check its weakest stop against the ground and give it a solid colour under forced colours.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/grounds-and-gradients.md#gradient-text
- ledger: COL-84
- status: staged

### vault.gradient-space
- applies-when: web-surface; every CSS gradient between two or more colours
- question: Does every gradient whose stops differ enough to show a muddy middle, and whose stops are written in hex, rgb() or hsl(), name its interpolation space (oklab() and oklch() stops already blend in Oklab), `in oklab` for stops in one hue family or toward white or black and `in oklch` (shorter hue) where the hues sit far apart and the middle must keep its chroma, never the gamma-sRGB or HSL blend, with `longer hue` kept for a spectrum on purpose and a plain declaration before it for browsers without the `in` syntax?
- answered-by: script
- writes: gradient interpolation space
- yields-to: level 2
- source: W3C CSS Color 4 §13, hex, rgb() and hsl() stops interpolating "in gamma-encoded sRGB space" unless a space is named, and Oklab the default otherwise; CSS Images 4 §3.1.1, sRGB "too dark at the midpoint", Oklab "with no purple cast at all", polar spaces "chroma-preserving" (Editor's Drafts, as read Nov 2026); web-features gradient-interpolation, Baseline 2024-06-11; Comeau, "Make Beautiful Gradients" (updated 28 Oct 2025), the "gray dead zone" and HSL "overly bright and vivid"; Krehel, "Understanding gradients", oklch showing "colors that you've never defined"; strength: standard and platform documentation
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- inputs: the hue difference between the stops; whether the middle must keep its chroma; whether a browser older than Baseline 2024 must see the same blend
- output: one hue family, or toward white or black: `in oklab`; hues far apart with a vivid middle: `in oklch`, checked for colours no stop names; a spectrum on purpose: `in oklch longer hue`; any `in` gradient: the same gradient declared first without `in`, or with in-between stops computed in Oklab where an older browser must match
- target: Write each gradient `in oklab`, or `in oklch` where its hues sit far apart, after a plain fallback declaration.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/grounds-and-gradients.md#how-a-gradient-blends
- ledger: COL-82
- status: live

### vault.gradient-stops
- applies-when: web-surface; every gradient with a visible transition
- question: Is a blend's midpoint moved with a colour hint, or its stops eased along the gradient, wherever the even blend shows a band or a muddy middle, with two stops at one position used only for a hard edge on purpose, such as a stripe?
- answered-by: builder
- writes: gradient colour distribution
- yields-to: vault.gradient-space
- source: MDN, "Using CSS gradients" (as read Nov 2026), a color hint location to "control the interpolation, or progression, between two color stops"; Krehel, "Understanding gradients", hints "change the rate of interpolation, not the endpoints", and two stops at one position "create a sharp edge"; Comeau, "Make Beautiful Gradients" (updated 28 Oct 2025), an easing curve over the stops; strength: platform documentation and expert writing
- era: timeless
- owner: vault
- stage: treatment
- target: Move a gradient's midpoint with a colour hint or ease its stops until the blend reads smooth; put two stops at one position only for a hard edge you want.
- reasons: design-critique/references/grounds-and-gradients.md#how-a-gradient-blends
- ledger: COL-83
- status: live

### vault.gradient-kind
- applies-when: web-surface; every gradient background
- question: Does each gradient's kind follow its job, linear for a scrim (running toward where the text sits), radial for one light source or depth on a surface, conic for a chart, ring or progress mark, and repeating only for a stripe or pattern the brand owns?
- answered-by: script
- writes: gradient kind
- yields-to: vault.gradient-function
- source: Krehel, "Understanding gradients" (as read Nov 2026), linear "the most common type", radial "for glows, backgrounds or depth lighting", conic "for charts, rings, animated borders", repeating for "a pattern or a texture"; web.dev Learn CSS, Gradients (as read Nov 2026), conic for "pie charts", repeating-linear for stripes; impeccable engine 0.1.11 rules radial-halo and repeating-stripes-gradient; strength: platform documentation and expert writing
- era: timeless
- owner: vault
- stage: treatment
- target: Pick the gradient kind by its job: linear for a scrim, radial for one light source, conic for a chart or ring, repeating only for a brand pattern.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/grounds-and-gradients.md#when-a-gradient-has-a-function
- ledger: SUR-98
- status: live

### vault.box-fills
- applies-when: web-surface; every filled or bordered container, card, section heading and coloured box; the large-container clause binds working (operate) views, and a persuade or experience hero or band may take a coloured ground on purpose
- question: Is bright or contrasting colour kept to small elements that must draw the eye (a button, a badge), with large containers in a working view neutral or a muted grey that recedes, no label given a filled box that makes it look like a button, and no page holding many coloured boxes of different sizes that compete with its controls?
- answered-by: whole-page
- writes: container fill colour and count
- yields-to: vault.heading-fill, vault.palette-roles, vault.tone-colour-share, level 2
- source: NN/g, Loranger, "Beyond Blue Links" (2015), "Avoid having many colorful boxes of different sizes on a page" and "giving headings a background color will make them resemble buttons"; Polaris, Creating depth (2024), bright or contrasting container colours "creates a cluttered UI", a grey background "visually recedes"; Polaris, Using color (2024), fills "on smaller surface areas", never "on large components"; strength: expert usability guidance and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Keep bright fills for buttons and badges, give a working view's large containers a neutral or muted ground, and never fill a heading or label so it looks pressable.
- reasons: design-critique/references/busyness.md#coloured-boxes
- ledger: COL-26
- status: live

### vault.heading-fill
- applies-when: web-surface; every heading
- question: Is every heading drawn with no background fill?
- answered-by: script
- writes: heading fill
- yields-to: none
- source: NN/g, Loranger, "Beyond Blue Links" (2015), "Avoid having many colorful boxes of different sizes on a page" and "giving headings a background color will make them resemble buttons"; Polaris, Creating depth (2024), bright or contrasting container colours "creates a cluttered UI", a grey background "visually recedes"; Polaris, Using color (2024), fills "on smaller surface areas", never "on large components"; strength: expert usability guidance and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Never fill a heading's box.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/busyness.md#coloured-boxes
- ledger: COL-26
- status: live
