# Text presentation: colour, tint, emphasis, links, grounds, rendering (design-vault#123)

Status: complete (13 Oct 2026).
Language: ASD-STE100 Simplified Technical English (approximate).
Parent map: design-vault#96. Question: design-vault#123. Parallel ticket: design-vault#117 (surface styling, `.claude/tmp/research-surface-styling.md`).

## How to read this file

- Each principle has these fields: Rule, Conditions, Trade-off, Resolution ("given X, do Z, not Y"), Source (strength), Era.
- Source strength: P = primary standard (WCAG, W3C, CSS spec). D = design-system documentation (Material, Apple HIG, Radix, Tailwind). E = expert reference (book, NN/g article, named practitioner). R = peer-reviewed research. W = weak (blog, opinion).
- Era: T = timeless. E = era-bound (date given). "Dated" = a convention that current practice does not use.
- House coverage key: C = covered, P = partly, G = gap, IMP = covered by impeccable. "+cond" = the house rule states conditions. "-cond" = the house rule states no conditions.

## Part A. What the house holds

### A1. design-vault

Sources: `plugin/skills/design-critique/SKILL.md` (91 lines, read in full), `plugin/skills/design-round/SKILL.md` and `references/*.md` (grep for text, tint, grey, link, caps, weight, contrast, font), House DNA (`dna` in `data/gallery.json`, read in full).

- design-critique: no rule on text colour, emphasis, links, text on grounds or rendering. It sends contrast and theming to `impeccable audit` (§1). §2 Gestalt "similarity" is the only lens that touches a text-colour hierarchy, and only by implication.
- design-round: `references/prompts.md:37`, `:61` ask an image model to leave "the upper half … plain and open for a headline". This is the only house rule that prepares a ground for text over art. It is a composition rule for the image. It does not say how the text sits on that ground (colour, scrim, measured contrast). `references/prompts.md:158-161` (tuning panel) exposes "headline weight, scale, line height and letter spacing" and says "Keep text and controls independent of image adjustments." `references/polish.md:29`: "only expose weights that the loaded fonts support".
- House DNA `never`: "gradient text" (line 1); "The default font stack (Inter, the system sans) as the only voice" (line 11); "Several colours at equal weight, none dominant" (line 12). No line on text colour, tint or links. `constants` is empty.
- Coverage: **G** for every area of this ticket, except the gradient-text ban and the headline area the design-round prompts leave on art (**P** for text on photos, B4.3).

### A2. impeccable 4.5.0

Sources: `reference/craft-floor.md`, `typeset.md`, `colorize.md` (read in full); grep over all other `reference/*.md` for tint, neutral, grey/gray, chroma, underline, emphasis, scrim, overlay, uppercase, caps, letter-spacing, tracking, tabular, smoothing, optical, grade, visited, text-shadow, italic, opacity; the detector rule list in design-vault `docs/research/impeccable-checks.md:73-76`.

Text colour and tint:
- craft-floor.md:9: "On colored surfaces tint secondary text from that hue or the foreground; never gray." Condition: "on colored surfaces". **+cond (ground only).**
- colorize.md:168: "Tint neutrals only when the brand hue genuinely creates cohesion. Neutral gray is valid when it serves the world." **+cond, but the condition ("genuinely creates cohesion") is not testable.**
- colorize.md:169: "On colored surfaces, derive secondary text from the foreground or surface hue rather than using washed-out generic gray."
- colorize.md:189: "When deriving OKLCH ramps, vary lightness and reduce chroma near white and black." and "Prefer explicit colors over chains of translucent overlays when alpha would make contrast context-dependent." This is the only impeccable line that bears on opacity greys against solid greys. **+cond ("when alpha would make contrast context-dependent").**
- colorize.md:162: "For a new web palette, prefer OKLCH".
- new-work.md:65: colour strategy "Restrained (neutrals tinted from the world plus one accent; common on screens people operate or read …)". Here tinted neutrals are the default of one strategy.
- quieter.md:56-57: "**Tinted grays**: Use warm or cool tinted grays instead of pure gray. Adds depth without loudness" and "**Never gray on color**: … use a darker shade of that color or transparency instead". **-cond.** quieter.md:56 is in tension with colorize.md:168 ("Neutral gray is valid when it serves the world"). quieter.md:57 advises "transparency", and colorize.md:189 advises against alpha when it makes contrast context-dependent. **Two internal conflicts in impeccable, with no resolution in its text.**
- Detector quality rule: "gray text on a coloured background" (impeccable-checks.md:74). A mechanical check of craft-floor.md:9.

Hierarchy and emphasis:
- typeset.md:86: "Combine size, weight, space, and tone deliberately instead of asking size alone to do all the work." craft-floor.md:12: "obvious scale and weight steps". Detector: "flat type hierarchy (steps under 1.25x)".
- craft-floor.md:33: "Gradient text. Emphasis comes from weight or size." (Ban, with the general condition that "the brief's own words can earn any of them", craft-floor.md:21.)
- quieter.md: "Hierarchy through subtlety: Use weight, size, and space instead of color and boldness".
- Detector: "all-caps body text"; "wide tracking on body text"; "crushed letter spacing"; craft-floor.md:12 "tracking floor -0.04em". Detector "italic serif display headline" and new-work.md:69 "small tracked mono labels" are AI-tell rules (era-bound taste).
- craft-floor.md:27: kicker or eyebrow above a heading is "a ban, not a default: no brief earns it back". This is about a text role (a small uppercase label above a heading).
- typeset.md:95: "Use numeric, tabular, code, and label features when their content benefits." craft-floor.md:15: "the numerals in tabular data … ship with browser defaults … Theme them". **+cond ("when their content benefits"), but no rule says which content.**

Links:
- craft-floor.md:15 names "underline offset" as a browser surface to theme. clarify.md:65: "Link text must make sense out of context". adapt.md:122: "Large, obvious CTAs (buttons not text links)" on mobile.
- No rule on whether an inline link is underlined, on link colour, on visited links, or on text buttons. grep "visited": 0 files. **G (by impeccable).**

Text on grounds:
- colorize.md:187: "Check interactive states, overlays, text on images, disabled content, and both themes." This is a check, not a method. grep "scrim": 0 files; "text-shadow": 0 files. Detector: "raster buried under a wash or opacity" (an AI-tell rule against a wash over a photo), and "text occluded by an overlapping element".
- typeset.md:92: "Compensate light text on dark surfaces on all three perceptual axes: slightly more line height, a touch more tracking, and one step more weight when the face needs it." **+cond ("when the face needs it"); no source.**
- colorize.md:172, :196: dark mode composed, not inverted.

Rendering:
- grep "smoothing", "antialias": only document.md:313, which lists `-webkit-font-smoothing` as a "universal reset" to skip when extracting a component. No rule. grep "optical": only optical alignment (polish.md:59, layout.md:57). grep "opsz", "grade": 0 files. typeset.md:67 asks whether "variable-font settings avoid invisible text and disruptive reflow" (delivery, not rendering). **G (by impeccable).**

### A3. Manta (lucmoseley/mantahostels)

Sources: `DESIGN.md` (read in full, 241 lines); `docs/brand/brand-sheet.md` §2–§4 (lines 15–139, read in full) and grep of the rest; `app/globals.css` (grep, then the token block lines 100–200 and the body, link, nav, card and label rules); `app/_fonts.ts`; the two font files (my own table parse, `/tmp/fontprobe/probe.py`, `digits.py`).

Measured by me (WCAG 2 relative luminance; OKLCH by the Ottosson matrices; script `/tmp/fontprobe/oklch.py`):

| Token | Hex | OKLCH (L C H) | on white | on sand-page | on ink |
|---|---|---|---|---|---|
| ink | #0A3542 | 30.7% 0.051 223 | 13.12 | 12.16 | — |
| text-muted | #5C6B72 | 51.8% 0.021 228 | 5.52 | 5.12 | 2.37 |
| muted-night | #8F999E | 67.6% 0.014 229 | 2.91 | 2.70 | 4.51 |
| lagoon-text | #08706F | 49.4% 0.083 194 | 5.90 | 5.47 | 2.22 |
| sand-page (ground) | #FBF6EA | 97.4% 0.017 88 | 1.08 | — | 12.16 |
| a neutral grey of equal L to text-muted | #6B6B6B | 52.8% 0 — | 5.33 | 4.94 | 2.46 |

- **Manta already tints its text toward the brand hue.** Body and heading text is `ink`, a dark brand teal (OKLCH chroma 0.051, hue 223), not black or a neutral grey. Secondary text `text-muted` is a grey tinted to the same hue (chroma 0.021, hue 228). `muted-night` is tinted to the same hue (chroma 0.014). So Manta's answer to the founder's example is "yes, tint", with the chroma falling as the colour moves from the dark end (0.051) to the mid greys (0.014–0.021). No Manta file states this as a rule, or records why. The brand sheet records "Rejected with reasons: cool grey neutrals (sterile)" (§3, line 123), but that line is in the amber discussion and does not say whether it means grounds or text.
- **The text is cool on a warm ground.** Text hue 223–229; page ground hue 88 (sand). No Manta rule names this temperature contrast, but it agrees with "warm = act, cool = read" (§3 line 63).
- **Text-colour hierarchy: two steps per ground**, primary (`ink` / white) and secondary (`text-muted` / `muted-night`). A disabled step and a placeholder step are not defined. "Design the failure states: greyed-out 'no space for your dates' rather than hidden" (DESIGN.md:231) uses a grey that has no token. Zero reviews shows "No reviews yet" "in muted grey" (DESIGN.md:199). All greys are solid hex; no opacity greys in text tokens. The semantic tints are alpha (`--tint-success: rgba(46,143,91,.15)` etc., globals.css), which is a ground, not text.
- **Coloured text.** Allowed only as named text-safe partners (`lagoon-text`, `success-text`, `warning-text`, `danger`, `danger-night`); "Never set copy in a raw fill colour" (DESIGN.md:147, :219). "Semantics are chips, not coloured type." This is the most conditioned colour rule in the house (it states the ground, the measured ratio and the reason: "Fill selection optimises for chroma; text selection optimises for luminance contrast").
- **Night pattern.** On ink: text white; secondary `muted-night` (4.51:1, 0.01 above the AA limit); semantics on a border, icon or chip; "Do not invent light text partners for the night ground" because a light partner "forces the token up to L\* ~74 where it collides" (brand sheet §3 lines 69–104). Links on ink: white plus underline.
- **Text on turquoise** is ink, never white (2.3:1); the wordmark half is the one exemption (§2).
- **Coral CTA label**: white at 3.0:1, so ≥19px at 700 (WCAG large text). "A type fix, not a colour fix" (§4). The label token `--text-cta` is 1.1875rem = 19px.
- **Links.** Light ground: `--text-link: lagoon-text`, hover `ink` (globals.css:132-133). The global rule is `a { color: inherit; text-decoration: none; }` (globals.css:223-226). Nav links: underline, `text-underline-offset: 3px`, hover offset 5px (globals.css:435-447). Current nav link: underline removed, weight 600, `aria-current` (§2 line 34). `.dest-card__cta` is lagoon-text label text with no underline, inside a card that is the link target. On ink: every `a` underlined (globals.css:231). **No rule for an inline link in running text on a light ground** (the base rule removes the underline; no file restores it for prose). No visited style.
- **Emphasis and case.** Sentence case for body and buttons; "Uppercase is reserved for badges and filter labels, used sparingly" (§4 line 136). Live code also uses uppercase for `.dest-card__region` and `.page__region` (a small label above a card title or page title) with `--letter-spacing-label: 0.02em` (globals.css:70, 642, 676). Headings `letter-spacing: -0.01em`. Quicksand 700/600 for headings and "UI emphasis"; Nunito Sans 600–700 for labels. Italic only for the hostel testimonial pull-quote (DESIGN.md:203). The listing card has "a bold comparable facts line … over a muted flavour line" (DESIGN.md:177): weight and colour together carry the fact-versus-voice split.
- **Numerals.** No `font-variant-numeric` and no `tabular` anywhere in `app/globals.css` (grep count 0). Font check (my parse of the shipped TTFs): **Nunito Sans default digits are already tabular** (all ten advance 600/1000 at the default instance) and it has no `tnum` or `lnum` feature, but has `onum`. So prices in Nunito Sans align by default. **Quicksand digits are proportional** ('1' = 363, '0' = 588 units) and Quicksand has no `tnum` feature. Score chips are Quicksand 700 (§4), and DESIGN.md:179 asks the score to "form a vertical column row-to-row". The score's figures cannot be made tabular in Quicksand.
- **Rendering.** `body { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }` site-wide (globals.css:215-216), with no comment or source. Nunito Sans (variable) has axes `wght` 200–1000, `wdth` 75–125, **`opsz` 6–12** and `YTLC` 440–540. With CSS `font-optical-sizing: auto` (the initial value), the browser sets `opsz` from the font size, so at 12px and above `opsz` sits at its maximum (12); only the text under 12px gets a different optical size (inferred from the axis range; the spec text was not read, B5.2). Quicksand has only `wght` 300–700.
- **Body size.** `body { font-size: 15.5px; line-height: 1.6 }`; `--text-body-sm` 14px; caption 12px (globals.css; #104 already flags this as below the 16px convention).
- **Text on photographs.** No rule. Carousel dots on the card photo use white at 55% with a 2px ink halo (HostelCard.jsx:24, per #117's file). The illustration hero leaves a plain area for type (design-round prompts). **G.**
- Coverage summary for Manta: text colour **C, +cond** on light, turquoise and ink grounds; tint **done but not stated**; hierarchy steps **P** (no disabled/placeholder); links **P** (night and nav ruled; inline prose not); emphasis/case **P, -cond** (one casing line); numerals **G** (font facts unknown to the files); photo grounds **G**; rendering **G** (one unexplained global smoothing rule).

## Part B. Principles from sources

### B1. Text colour: black, grey, tinted neutrals, coloured text

**B1.1 Tinting text and neutrals toward a hue (the founder's example).**
- Rule: Give the neutral scale (greys for text, borders and grounds) a small chroma at a chosen hue. The current design systems do this by default:
  - Material 3 (Google's own colour library, `material-color-utilities`, `dynamic_scheme.ts`): in the default "Tonal Spot" scheme, the neutral palette (`onSurface`, primary text) has the **source (brand) colour's hue** at HCT chroma 6 (2021 spec; 5 on phone in the 2025 spec), and the neutral-variant palette (`onSurfaceVariant`, lower-emphasis text and icons) has the same hue at chroma 8 (8.5 on phone, 2025). The "Monochrome" and "Rainbow" variants set the neutral chroma to 0. On Surface = `neutral10` (light) / `neutral90` (dark); On Surface Variant = `neutral_variant30` / `neutral_variant80` (material-components-android `docs/theming/Color.md`, auto-generated role table). Source: **D** (first-party code and docs, read 13 Oct 2026). So Material tints secondary text a little **more** than primary text.
  - Radix Colors: "choose the gray scale which is saturated with the hue closest to your accent hue … this will create a more colorful and harmonius vibe", or pure `gray`, which "will work well with any hue" for "a neutral vibe". Caveat: "be careful when using saturated grays for your app background, especially in dark mode." Source: radix-ui.com/colors/docs/palette-composition/composing-a-palette. **D.**
  - Tailwind v4: eight of its nine neutral scales carry chroma. Its default `gray` is blue-tinted: 500 = oklch(55.1% 0.027 264), 900 = oklch(21% 0.034 264). `slate` 500 = 0.046 chroma; `zinc` 0.016; `stone` 0.013; `mist` 500 = oklch(56% 0.021 213.5); only `neutral` is 0. Chroma falls toward the darkest step for most scales (mist 950 = 0.004). Source: tailwindcss.com/docs/colors. **D.**
  - Refactoring UI (Wathan and Schoger, 2018): saturate greys "with a bit of blue" to feel cool, or yellow/orange to feel warm, like the colour temperature of a light bulb. The frame is **temperature and mood**, not "match the brand hue". Source: the book, read only through an unofficial copy and summaries. **E, read second-hand.**
- Conditions (from the sources): (1) chroma stays low; in the systems above the mid greys sit at about OKLCH chroma 0.013–0.046, and chroma falls toward black and white (impeccable colorize.md:189 says the same: "reduce chroma near white and black"); (2) the hue is the brand's hue (Material, Radix) or a chosen temperature (Refactoring UI); (3) Radix gives a pure grey as an equal choice for a "neutral" or "functional" feel; (4) caution on saturated grey *grounds* in dark mode (Radix).
- Trade-off: Cohesion and warmth against neutrality. A tinted grey next to a different strong hue can look dirty or off (my inference, no source measured it). A tint at a hue far from the brand's accent makes a second, unrelated colour family. The contrast cost is **small when lightness is held**: my measurement — Manta's `text-muted` (OKLCH L 51.8%, chroma 0.021) gives 5.52:1 on white; a pure grey at L 52.8% gives 5.33:1. Contrast is a luminance measure, so a low tint barely moves it. The cost appears only when chroma is pushed high at the same nominal lightness in HSL (HSL lightness is not perceptual: "HSL lightness is not consistent across hue axes", Sitnik and Turner, Evil Martians, updated 17 Sep 2025, **E**), or when the tint makes text a colour that also means "link" (B3).
- Resolution: Given a brand with one clear dominant hue and a calm product, tint the neutral scale toward that hue at low chroma and lower the chroma at the dark and light ends. Given a page that carries several strong hues, or many photographs, use the hue of the dominant colour or a pure grey; do not tint toward an accent that the page uses only as a spot (one-job colour, Manta §3). Given a coloured ground, derive the text colour from that ground's hue (B1.3), not from the brand neutral. Define the tint in OKLCH (or HCT), not HSL.
- Disagreement: Evil Martians' worked palette uses chroma 0 for text and a tiny chroma (0.005) only for off-white surfaces. impeccable is split: colorize.md:168 ("Tint neutrals only when the brand hue genuinely creates cohesion. Neutral gray is valid") against quieter.md:56 ("Use warm or cool tinted grays instead of pure gray", no condition). The sources agree that the tint is a style choice with no measured legibility gain.
- Era: **E, current (about 2018 onward, mainstream from 2021 with Material You).** It is not a dated practice. The dated practice is the *method*: making tints by HSL saturation or by `darken()`/`lighten()` in Sass, which change perceived lightness and contrast when the hue changes (Sitnik).

**B1.2 Near-black, not pure black, for text on white.**
- Rule: Material's primary text on a light ground is `neutral10` (tone 10, tinted), not black; Tailwind's examples use `gray-950`/`gray-700`; Manta uses `ink` (13.12:1). Source: **D** (as B1.1). No source found that measures a legibility gain from near-black over black. Hall and Hanna (2004, *Behaviour & Information Technology*, 136 participants, four colour pairs): "Colours with greater contrast ratio generally lead to greater readability"; colour pair had no significant effect on retention; blue and other chromatic pairs got higher aesthetic and purchase-intent ratings (abstract only, Scholars' Mine). **R, abstract read.** Legge, Rubin and Luebker (1987, *Vision Research* 27(7)): for normal vision, reading rate stays near its peak over a wide range of contrast and falls fast only below about 10% contrast (abstract and later citations, read via search). **R, second-hand.**
- Conditions: The reader has normal vision and the text is at a comfortable size. WCAG 1.4.3's 4.5:1 exists to cover "moderately low visual acuity … approximately 20/40" (Understanding 1.4.3). **P.**
- Trade-off: Legge's result means that, for most readers, a drop from 21:1 to about 12:1 costs no reading speed; it is a style choice. For low-vision readers the reserve matters, so the floor is WCAG, not taste.
- Resolution: Given body text, any near-black at ≥ about 12:1 is free to choose by brand; do not go below 7:1 for small body text (Apple asks to "strive for … 7:1, especially in small text", HIG Dark Mode, **D**). Given the low-contrast-grey fashion, refuse it: NN/g, Sherwin, 7 Jun 2015: "Low-contrast text may be trendy, but it is also illegible, undiscoverable, and inaccessible" (no data in the article; **E**).
- Era: low contrast grey body text is a **dated 2010s minimalist trend** (NN/g 2015). Near-black text is **T**.

**B1.3 Grey text on a coloured ground: take the ground's hue.**
- Rule: Do not put a neutral grey on a coloured ground. Use a colour of the ground's hue with a different lightness (and adjusted chroma), or white or black at reduced opacity. Sources: Refactoring UI, "7 practical tips for cheating at design" (Medium, 2017; read via a copy, Medium returned 403): grey on white works by lowering contrast; on a colour, move the text toward the background colour; fix 1 white with reduced opacity, fix 2 "hand-pick a color" of the same hue, which is better when the background is an image or a pattern. **E, read second-hand.** impeccable craft-floor.md:9, colorize.md:169, and the detector rule "gray text on a coloured background". **W (uncited plugin) but consistent with E.**
- Conditions: the ground is a saturated or tinted colour (not white, not near-white).
- Trade-off: Opacity is quick and follows the ground, but it makes contrast depend on what is beneath (colorize.md:189). A hand-picked colour is exact but needs one token per ground.
- Resolution: Given a fixed set of brand grounds (Manta: white, sand, turquoise, ink), hand-pick one solid secondary-text token per ground and measure it (Manta's `muted-night` is this). Given a ground that varies (photo, gradient, user content), opacity white or black is acceptable only over a scrim that fixes the contrast (B4).
- Era: **T** (colour interaction).

**B1.4 Solid greys against opacity greys.**
- Rule A (alpha): Material 2 used alpha for text emphasis: high .87, medium .60, disabled .38 (Material Components Web theme package and Compose `ContentAlpha`; read via search). Apple's label colours (`secondaryLabel`, `tertiaryLabel`, `quaternaryLabel`) are dynamic colours that "adapt automatically" (HIG Color, Dark Mode). That they are alpha-based is my knowledge, not re-read here. **D, partly second-hand.**
- Rule B (solid): Material 3 dropped alpha emphasis for opaque tone-based roles (`onSurface`, `onSurfaceVariant`), and kept 0.38 alpha only for disabled content (community report, Kotlin Slack, **W**; the role table in material-components-android shows only opaque tones, **D**). impeccable colorize.md:189: "Prefer explicit colors over chains of translucent overlays when alpha would make contrast context-dependent."
- Conditions: Alpha suits a system where text must sit on many grounds that the designer does not control (OS materials, vibrancy). Solid suits a web palette with a known set of grounds.
- Trade-off: Alpha gives one token for every ground, but the contrast of the result is not known until the ground is known, and alpha text over a photo or over another alpha layer can fail. Solid gives a measured, fixed ratio, but needs one token per ground.
- Resolution: Given a website with named grounds, use solid tokens per ground and measure each (Manta does this). Given a disabled state, alpha is acceptable because WCAG exempts disabled controls ("User Interface Components that are not available for user interaction … are not required to meet contrast requirements", Understanding 1.4.3, **P**), but keep the disabled text above APCA Lc 30 so it is still readable (B6).
- Era: alpha emphasis for text is **era-bound, Material 2 (2014–2021)**; opaque roles are **current (M3, 2021 on)**.

**B1.5 How many steps in a text-colour hierarchy.**
- Rule: Two or three text colours, plus a disabled and a placeholder state. Sources: Refactoring UI: "stick to two or three colors": dark for primary, grey for secondary, lighter grey for ancillary (second-hand copy, **E**). Radix: two text steps (11 low-contrast, 12 high-contrast), guaranteed to "Lc 60 and Lc 90 APCA contrast ratio on top of a step 2 background" (**D**). Material 3: two (`onSurface`, `onSurfaceVariant`), plus disabled at 0.38. Apple: four labels plus placeholder (**D**). Tailwind examples: 950 / 700 / 500 (**D**).
- Conditions: Apple's four steps serve dense native UI (lists, metadata). Web systems use two plus states.
- Trade-off: More steps give finer hierarchy but adjacent steps become hard to tell apart and the lowest steps fall under readable contrast.
- Resolution: Given a website, use two readable text steps per ground (primary ≥ Lc 90 / about 12:1; secondary ≥ Lc 60 and ≥ 4.5:1), and carry further hierarchy with size, weight and space (B2), not with a third grey. Define disabled and placeholder explicitly.
- Era: **T** (the number); the APCA-indexed values are **E, 2021 on, unsettled**.

**B1.6 Coloured text (brand-coloured headings, accent words, semantic text).**
- Rule: Colour in text must not be the only signal of meaning, and a colour that marks links must not be used for non-link text. Apple HIG Color: "if you use your brand color to indicate that a borderless button is interactive, using the same or similar color to stylize noninteractive text is confusing." NN/g (2004, re-noted Mar 2026): "Don't use blue for non-link text, even if you don't use blue as your link color." Radix: using the accent scale for text gives "a more colorful vibe"; "You may want to experiment with using your accent scale for text in your marketing sites." **D / E.**
- Conditions: Apple visionOS: "Prefer using color in bold text and large areas"; "Color in lightweight text or small areas can make them harder to see". **D.** So coloured text is for headings and large or bold type, and for marketing surfaces more than working surfaces (Radix).
- Trade-off: Coloured headings add brand voice; they cost link affordance (if the hue is near the link hue) and contrast (saturated mid-lightness colours are rarely 4.5:1 on white — Manta measured this as its text-safe partner rule).
- Resolution: Given a brand colour that also marks links or actions, do not use it for non-interactive text. Given a heading in a brand colour, use a text-safe partner of that colour (darker), at heading size and weight, in the Persuade zone only.
- Era: **T.**

### B2. Emphasis and hierarchy: colour, weight, size, case, italic, tracking, numerals

**B2.1 Carry hierarchy with several cues together, and do not make size do all the work.**
- Rule: Use colour (lightness) and weight to rank text before you use size; combine size, weight, space and colour. Sources: Refactoring UI: two or three text colours, two weights ("a regular weight (400 or 500) and a heavier one (600 or 700)"), "Stay away from font weights under 400 for UI work" (second-hand copy, **E**). Apple HIG Typography: "Adjust font weight, size, and color as needed to emphasize important information"; "avoid light font weights … especially when text is small" (**D**). impeccable typeset.md:86 (same, uncited).
- Conditions: UI and dense pages (Refactoring UI's frame). On a reading page (long prose), Butterick's emphasis rules govern (B2.2). Apple: thin weights need "larger than the recommended sizes".
- Trade-off: De-emphasis by lighter colour lowers contrast (B1.5 floor); de-emphasis by smaller size lowers legibility (body floor, #104 W5). Weight emphasis costs nothing in contrast but adds visual noise if used widely.
- Resolution: Given a list row or card (Manta's working area), rank by weight first (name bold, facts semibold), then by colour step (secondary grey), and keep size steps few. Given a light text colour already in use for de-emphasis, do not also shrink that text below the body floor: one cue down is enough. Given a weight under 400, refuse it for text under about 18px.
- Era: **T.**

**B2.2 Emphasis inside running text: bold or italic, never both, rarely.**
- Rule: "Bold or italic—think of them as mutually exclusive"; "use bold and italic as little as possible"; with a sans serif, use bold, because sans italics "just have a gentle slant that doesn't stand out"; underlining for emphasis is a "terrible" idea. Source: Butterick, *Practical Typography*, "Bold or italic". **E.**
- Conditions: running text, short emphasised spans. Serif against sans changes the choice. (Manta's body face is a sans: Nunito Sans.)
- Trade-off: Bold in a UI already full of semibold labels loses force; italic in a rounded sans barely shows.
- Resolution: Given a sans body face and a UI that already uses 600–700 for labels, emphasise in prose with bold at one step above the body's weight, and keep italic for its semantic jobs (a quotation, a title), as Manta does with the testimonial. Do not underline for emphasis, because the underline is the link signal (B3).
- Era: **T** (print rule, holds on screen).

**B2.3 All caps and small caps: short strings only, with added tracking.**
- Rule: Caps suit "headings shorter than one line … headers, footers, captions, and other labels"; "Always add letterspacing to caps"; "5–12% extra letterspacing to text in all caps or small caps" (Butterick, "All caps", "Letterspacing", **E**). Bringhurst §2.1.6: "Letterspace all strings of capitals and small caps, and all long strings of digits", 5–10% of the type size (Rutter's *Web Typography* adaptation, read via search, **E second-hand**). Lowercase does not normally take letterspacing (Butterick). WCAG 1.4.12: layout must survive user letter spacing of 0.12 em (**P**). impeccable detector: "all-caps body text", "wide tracking on body text".
- Conditions: short labels; small sizes need more tracking than large.
- Trade-off: Caps add emphasis and a "label" register without colour; they cost reading speed in long strings and look shouted. Tracking aids caps but harms lowercase.
- Resolution: Given an uppercase label, track it +0.05 to +0.12 em and keep it to one short line. Given a sentence, never set it in caps. Given a label that is a small uppercase line directly above a heading, it is an eyebrow (impeccable craft-floor.md:27 bans it with no exception; Manta's brand sheet §2 specifies "Hero eyebrows"; #98 records this conflict). The typographic rule (tracking) holds whatever the ruling on eyebrows.
- Era: **T.**

**B2.4 Numerals: tabular for columns, lining with caps, slashed zero only where O and 0 confuse.**
- Rule: Tabular figures are "essential for one purpose: vertically aligned columns"; proportional figures read better in body text; lining figures are "always preferred for all caps text"; do not mix oldstyle figures with caps (Butterick, "Alternate figures", **E**). CSS: `font-variant-numeric: tabular-nums | lining-nums | proportional-nums | oldstyle-nums | slashed-zero` map to OpenType `tnum`, `lnum`, `pnum`, `onum`, `zero`; Baseline widely available since January 2020 (MDN, **P-level reference**). The `font` shorthand **resets `font-variant-numeric` and `font-optical-sizing`** to their initial values (MDN `font`). impeccable typeset.md:95, craft-floor.md:15 (numerals as a "browser surface").
- Conditions: the feature works only if the font has the glyphs; many fonts' default figures are already tabular lining (Butterick; and my parse: Nunito Sans default digits are all 600/1000 wide).
- Trade-off: Tabular figures in a sentence space unevenly ("1" sits in a wide cell). Proportional figures in a column or a changing number (a price that updates, a counter) jitter.
- Resolution: Given prices, scores and counts that stack in a column or update in place, use tabular lining figures; given numbers in a sentence, proportional. Given a face with no `tnum` (Quicksand), do not put column numbers in it, or accept the ragged column. Given a token that sets type with the `font` shorthand, set `font-variant-numeric` after it in the same rule, or the shorthand resets it.
- Era: **T.**

### B3. Links and interactive text

**B3.1 A link in running text needs a non-colour cue.**
- Rule: WCAG 1.4.1 (A) needs "a visible alternative to color"; failure F73 is "creating links that are not visually evident without color vision". Sufficient technique G183 allows colour alone only if the link text has ≥3:1 contrast against the surrounding text, and the technique notes "Especially for dark colors, it can be difficult to visually distinguish between differently colored text" even at 3:1, and suggests "an underline or bold text" (W3C Understanding 1.4.1 and G183, **P**). NN/g (Nielsen 2004, editor's note Mar 2026 says treat it "as a starting point rather than a rule"): underlines can go only in "navigation menus and other lists of links"; keep them where accessibility is a priority; "Reserve underlining for links" (**E**). GOV.UK Design System: "Links are blue and underlined by default"; remove the underline "Only … if the context tells the user that the text is a link" (**D**).
- Disagreement: Butterick says underlined links are "Dying? For sure." That is a typographer's taste; the accessibility and usability sources disagree with him for links in prose. Resolve for the standard (P), not the taste (E).
- Conditions: inline (in prose) against standalone (navigation, card, button). A dark link colour next to near-black body text rarely reaches 3:1 against the text (check below).
- Trade-off: An underline adds noise in a dense list of links; colour alone fails colour-blind readers and, for dark brand colours, also fails 3:1 against body text.
- Resolution: Given a link inside prose, underline it at rest (thin, with offset, so it does not cut descenders), whatever its colour. Given a list of links, a nav bar or a whole card as target, the context carries the affordance and the underline is optional (NN/g, GOV.UK). Given a ground where the brand colour would collide with the logo or with meaning (Manta's ink ground), use the text colour plus underline (Manta night pattern).
- Measured for Manta: `lagoon-text` link (#08706F) against `ink` body text (#0A3542) = **2.22:1**, and against `text-muted` = 1.07:1 (my calculation, WCAG 2 formula). So Manta's light-ground inline links **fail G183** if they have no underline. The base rule `a { text-decoration: none }` (globals.css:223-226) removes it, and no rule restores it in prose. Today the live pages have no inline prose links on light grounds that I could see (not checked page by page). Guide pages (Read mode) will add them.
- Era: **T** (the need for a cue); the "no underline, colour only" look is a **dated 2010s flat trend** for prose links.

**B3.2 Link colour, hover, visited.**
- Rule: Unvisited links are "more vivid, bright, and saturated" than visited ones (NN/g 2004, **E**, old). WCAG: colour-only visited distinction "does not result in a failure", but links must still meet contrast on the ground (Understanding 1.4.1, **P**). GOV.UK keeps visited state by default, and drops it "where it is not helpful … for example when linking to pages with frequently-changing content" (**D**). Apple: do not give a brand colour that marks interactivity to non-interactive text (**D**).
- Conditions: content sites where a reader returns to a list of articles (visited helps); app-like surfaces and nav (visited does not help).
- Resolution: Given a guide or article list, show visited. Given nav, cards and controls, no visited style. Given hover, change a non-colour property too (underline offset or thickness), so the hover cue does not rely on colour.
- Era: visited styling: **T** as a usability aid, rarely used in current brand sites (era-bound habit, no measured source after 2004 found).

**B3.3 Text buttons and "quiet" actions.**
- Rule: Mobile: "Large, obvious CTAs (buttons not text links)" (impeccable adapt.md:122, **W**). NN/g flat-design study (2017, cited in #104 W3): weak signifiers cost time. Apple: borderless buttons use the tint colour; do not reuse it on plain text (**D**).
- Resolution: Given a secondary action set as text (a "View all" link in a card), give it the link colour and a non-colour cue (arrow icon, underline on hover and focus) and a 44px target. Overlap with #117 (focus and state outlines).
- Era: **E, current** (flat 2.0, #104 W3).

### B4. Text on grounds: tinted, brand fills, dark and night, photographs and video

**B4.1 Text on a brand-colour fill (buttons, chips, hero grounds).**
- Rule: Measure each text/fill pair; use WCAG large-text 3:1 only when the text really is large ("18 point or 14 point bold", about 24px or 18.5px bold; Understanding 1.4.3, **P**). Radix: "Most step 9 colors are designed for white foreground text", but bright hues (Sky, Mint, Lime, Yellow, Amber) take dark text (**D**). Manta's text-safe partner rule and its coral ≥19px/700 rule apply this (A3).
- Conditions: the hue's lightness decides the polarity: a light, bright fill (turquoise, amber, yellow) takes dark text; a mid or dark fill takes white.
- Trade-off: A brighter fill reads as more pressable ("chroma is affordance", Manta §3, **W**) but forces dark text or a large label. Darkening the fill to pass with small white text dulls it (Manta §4).
- Resolution: Given a bright fill that must keep its brightness, choose the polarity by measurement, then fix the size (Manta's "type fix, not a colour fix"). Given a fill that cannot reach 3:1 with either polarity at the size needed, change the fill or the role, not the rule.
- Era: **T.**

**B4.2 Text on a dark (night) ground, and dark mode.**
- Rule A (colour): Do not make light "text partners" for every semantic colour on dark; use white text and carry meaning on a border, icon or chip (Manta night pattern, measured, house evidence, measured against WCAG). Apple: contrast "no lower than 4.5:1 … strive for … 7:1, especially in small text"; give each custom colour light, dark and increased-contrast variants (HIG Dark Mode, Color, **D**). Radix: be careful with saturated grey grounds in dark mode (**D**).
- Rule B (weight): Light text on dark looks heavier than dark text on light ("irradiation"): "The light text appears thicker than the dark text counterpart, even though the font weight is the same"; lower the variable-font grade (`GRAD`) in dark mode, for example −25 to −50, which changes weight without changing width (Argyle, web.dev, updated 27 Jul 2023; nerdy.dev, 29 Nov 2025, **E/W**). impeccable typeset.md:92 says the opposite: on dark, add "a touch more tracking, and one step more weight when the face needs it" (**W**, uncited).
- Rule C (polarity): dark text on light is generally more legible; the gap is small and is better called a "negative polarity disadvantage" (Dobres, Chahine and Reimer 2017, *Applied Ergonomics*, read via a 2022 arXiv citation, **R second-hand**). NN/g 2020 (#104 W5): light mode performs better for normal vision.
- Conditions that resolve Rule B against impeccable: irradiation dominates for medium and large text at normal weight; at small sizes and thin strokes, light text on dark loses strokes to anti-aliasing (MDN: switching to greyscale anti-aliasing "for light text on dark backgrounds makes it look lighter", B5), so small text on dark can need *more* weight.
- Resolution: Given headings and large text on dark, keep the weight or reduce it slightly (grade −25 to −50 where the face has `GRAD`; Nunito Sans and Quicksand do not). Given small body or label text on dark at a light weight, keep at least the light-ground weight and add line height; do not reduce it. Given a secondary text colour on dark, require more margin than on light (B6: Manta `muted-night` passes WCAG by 0.01 and APCA puts it under the level for body text).
- Era: dark mode as a choice the user makes: **E, 2019 on** (#104 W5). The irradiation effect: **T** (perception).

**B4.3 Text on photographs and video.**
- Rule: Contrast is measured against the pixels next to each letter: keep "a 4.5:1 contrast ratio with the background behind them", or "provide a halo around the text", or "a thin black outline (at least one pixel wide)" (WCAG technique G18; G145 for 3:1 at large size, **P**). Choose the fix for the "worst-case background image and text placement"; options: darken the image, a "semi-transparent black gradient", a semi-opaque text box (an REI example failed at 30% opacity and passed at 50%), blur, a "floor fade" on the lower part, a text shadow (Harley, NN/g, 18 Oct 2015, reviewed 13 Jan 2026, **E**; no ranking given). WCAG F83: "using background images that do not provide sufficient contrast" (**P**). impeccable: "Check … text on images" (no method). design-round prompts reserve a plain area in generated art for a headline.
- Conditions: (1) whether the image is fixed (one hero) or varies (listing photos, user content, a video); (2) the text's size; (3) whether the image must keep its colour (a listing photo is product evidence) or may be treated (a mood hero).
- Trade-off: A scrim or darkening fixes contrast for every image but dims the photo and, on a listing photo, changes the product evidence; a halo or shadow keeps the photo but looks dated if heavy; placing text off the image keeps both but costs space.
- Resolution: Given a listing or product photo (evidence), keep text off the photo; put only controls on it (carousel dots, a save button), each with its own halo or chip. Given a fixed hero image that the designer controls, compose a plain area for the text (design-round prompt) and measure the worst pixel under the text at every breakpoint, because the crop moves. Given a varying image or video, use a gradient scrim sized to the text block and measure against the lightest frame; for video also satisfy WCAG 2.2.2 (pause for loops over 5 s, #104 W9). Given a brand that bans gradients in UI (Manta: "UI is flat"), a scrim is a gradient: the ban needs a ruling for this case.
- Overlap: #117 researches the scrim as a surface (colour, opacity, tint). This item is about the text on it.
- Era: **T** (contrast); the heavy text-shadow look is **dated (2000s web)**; the full-bleed photo hero with white text over a dark overlay is a **2010s convention** still common.

### B5. Rendering: smoothing, optical size, grade, weight at small sizes

**B5.1 Font smoothing.**
- Rule: `-webkit-font-smoothing` and `-moz-osx-font-smoothing` are non-standard and "only work on macOS"; `antialiased` uses greyscale anti-aliasing, and for "light text on dark backgrounds makes it look lighter"; MDN: "We do not recommend using non-standard features in production" (MDN font-smooth, **P-level reference**). macOS turned subpixel anti-aliasing off by default in 10.14 Mojave (September 2018) (several technical blogs, **W**). So on current macOS the global `antialiased` setting usually changes nothing; on older macOS, or where a user turned subpixel rendering back on, it thins all text.
- Conditions: macOS only; matters only where subpixel anti-aliasing is on.
- Trade-off: The rule was used (about 2012–2018) to stop light-on-dark text looking bold under subpixel rendering; applied site-wide it also thins dark-on-light body text.
- Resolution: Given light text on a dark ground, `antialiased` on that ground only is acceptable. Given dark text on light, do not set it. Given an existing site-wide rule (Manta globals.css:215-216), the cost on current macOS is near zero, so this is low priority.
- Era: **era-bound, 2012–2018 habit**; mostly moot since 2018.

**B5.2 Optical size and grade.**
- Rule: `font-optical-sizing: auto` is the initial value; "small text sizes are often rendered with thicker strokes and larger serifs" (MDN, Baseline widely available since March 2020). Apple's system fonts use "dynamic optical sizes" and adjust tracking "at every point size" (HIG Typography, **D**). Grade (`GRAD`) changes apparent weight without changing width, so it does not reflow text (B4.2 sources).
- Conditions: only fonts with an `opsz` or `GRAD` axis. The `font` shorthand resets `font-optical-sizing` to `auto` (MDN), which is the wanted value.
- Resolution: Given a variable font with `opsz`, leave `font-optical-sizing: auto`. Given a font with a narrow `opsz` range (Nunito Sans: 6–12), it affects only text under 12px (my inference from the axis range, assuming the browser maps `opsz` to CSS px; the spec text was not read). Given a face without `GRAD`, adjust dark-mode weight with `wght` steps instead (B4.2).
- Era: **E, current (2020 on, variable fonts).**

**B5.3 Weight at small sizes.**
- Rule: Avoid Ultralight, Thin and Light "especially when text is small"; with a thin custom font, "aim for larger than the recommended sizes" (Apple HIG, **D**). Refactoring UI: no weight under 400 for UI (**E**). WCAG Understanding 1.4.3: thin fonts render "much fainter", so choose "a font with stronger/thicker lines" (**P**, advisory).
- Resolution: Given text at or under body size, weight ≥ 400 (and the face's real 400, not a variable default: Nunito Sans' variable file defaults to `wght` 200, so a missing `font-weight` would render at 200 — my parse of `fvar`; the site sets weights explicitly).
- Era: **T.**

### B6. Two contrast models, and what they say about Manta's pairs

- WCAG 2 (1.4.3 AA 4.5:1 / 3:1 large; 1.4.6 AAA 7:1 / 4.5:1) is the legal and current bar (**P**). APCA is not settled: the WCAG 3 editor's draft of 8 Apr 2026 says "The contrast algorithm used in WCAG 3 is yet to be determined"; APCA was "pulled" from the July 2023 draft; advice: "Choose colors that also conform to WCAG2 contrast requirements" (Roselli, Apr 2026, **E**, quoting W3C). APCA's own guidance: Lc 90 preferred for body text; Lc 75 minimum for body columns at 18px/400 or 16px/500; Lc 60 for other content text; Lc 45 for "larger, heavier text (36px normal weight or 24px bold)"; Lc 30 for placeholder and disabled text; and its author's claim that "WCAG 2.x contrast cannot be used for guidance designing 'dark mode'" (APCA in a Nutshell, **W–E: the method's own author; contested**).
- My APCA computation (constants verified against `apca-w3@0.1.9` source on unpkg; script `/tmp/fontprobe/apca.py`) for Manta's pairs:

| Pair | WCAG 2 | APCA Lc | Reading |
|---|---|---|---|
| ink on white | 13.12 | 99.2 | both: excellent |
| ink on sand-page | 12.16 | 93.9 | both: excellent |
| text-muted on white | 5.52 | 77.6 | both pass for body |
| text-muted on sand-page | 5.12 | 72.4 | WCAG pass; APCA: content text yes, body column slightly under Lc 75 |
| white on ink | 13.12 | −102.4 | both: excellent |
| **muted-night on ink** | **4.51** | **−40.9** | WCAG pass by 0.01; APCA: under Lc 45, so fit only for large or heavy text |
| **ink on turquoise** | 5.73 | 52.4 | WCAG pass; APCA: large text and short content only, not body |
| white on coral (CTA) | 3.05 | −61.7 | WCAG large-text only; APCA: passes for content text — **APCA judges this pair better than WCAG 2 does** |
| white on turquoise (banned) | 2.29 | −49.5 | both: no for body |
| danger-night on ink | 6.52 | −58.0 | WCAG pass; APCA: content text, not body |

- Correction to #104 W1: #104 inferred that APCA "would likely judge less kindly" white on coral. Measured, APCA judges it **more** kindly (Lc 61.7). The pairs that APCA flags are the light-on-dark secondary pair (`muted-night` on ink) and dark text on the mid-light turquoise.
- Conditions: APCA weights polarity and dark-mode pairs differently from WCAG 2; where they disagree, WCAG 2 is the legal floor and APCA is a design aid.
- Resolution: Given a pair that passes WCAG 2 by a small margin and fails APCA's level for its use (Manta `muted-night` for secondary copy), raise its lightness until both agree; this costs nothing legally and removes a known weak spot. Measured option (same hue 229 and chroma 0.014, only OKLCH L raised): L 72% = #9CA6AC, 5.29:1, Lc 47.5; L 78% = #AFB9BF, 6.57:1, Lc 57.5; Lc 60 needs about L 80%. A grey this light has low chroma, so the brand sheet's L\* ~74 collision reason (which was about coloured partners near turquoise and amber) needs a ΔE check before a ruling; I did not run it. Given a pair that passes APCA and fails WCAG 2 (white on coral below 19px), WCAG 2 wins.
- Era: WCAG 2: **E, current**; APCA: **E, unsettled, 2021 on**.

## Part C. House coverage per area

| Area | design-vault | impeccable | Manta | Note |
|---|---|---|---|---|
| Tinted neutrals for text (B1.1) | G | P, split: colorize +cond (untestable "genuinely creates cohesion"), quieter -cond (always tint); no chroma limit except "reduce chroma near white and black" | Done, not stated: ink C 0.051, text-muted 0.021, muted-night 0.014 at hue 223–229; "cool grey neutrals (sterile)" rejected, scope unclear | No house file gives the chroma band, the colour space for text, or the condition |
| Near-black body text (B1.2) | G | P (contrast floors only) | C (+cond: measured per ground) | — |
| Grey on a coloured ground (B1.3) | G | IMP (+cond: "on colored surfaces"; detector rule) | C (+cond: text-on-turquoise is ink; per-ground tokens) | — |
| Solid against opacity greys (B1.4) | G | P (+cond: colorize.md:189), contradicted by quieter.md:57 | C in practice (solid tokens), not stated | Disabled state has no token |
| Text-colour steps (B1.5) | G | P ("primary and secondary text" roles) | P: two steps per ground; no disabled, no placeholder | — |
| Coloured text (B1.6) | G | P (semantic colours not alone) | C (+cond: text-safe partners, "semantics are chips") | Strongest house rule in this ticket |
| Hierarchy cues combined (B2.1) | G | IMP (typeset.md:86, "obvious scale and weight steps"; detector "flat hierarchy") -cond | P (card anatomy: bold facts line over muted flavour line) | — |
| Bold/italic in prose (B2.2) | G | G | P (italic only for the testimonial) | — |
| Caps and tracking (B2.3) | G | P (detector: all-caps body, wide tracking body; eyebrow ban) -cond | P: "uppercase … sparingly"; live labels at +0.02 em, under the 5–12% rule | Eyebrow conflict (#98) |
| Numerals (B2.4) | G | P (+cond "when their content benefits", no list of content) | G (no `font-variant-numeric`; files do not know Quicksand has no `tnum`) | — |
| Inline links (B3.1) | G | G (no underline rule) | P: night links and nav ruled (+cond); prose links on light grounds have no underline by the base rule | Probable 1.4.1 failure once prose links ship |
| Visited, hover cue (B3.2) | G | G | P (hover moves underline offset in nav; no visited) | — |
| Text buttons (B3.3) | G | P (adapt.md:122) | P (outline "View beds"; `.dest-card__cta` text) | Overlap #117 (focus) |
| Text on brand fills (B4.1) | G | IMP (AA table) | C (+cond: coral ≥19px/700, ink on turquoise, fixed pairings) | APCA disagrees on ink-on-turquoise for body size |
| Text on dark ground, dark mode (B4.2) | G | P: "one step more weight" on dark (-cond source; conflicts with irradiation sources) | C for colour (night pattern, +cond); G for weight | No `prefers-color-scheme` decision (#104) |
| Text on photos and video (B4.3) | P (prompts leave a headline area) | P (check only) | G | Overlap #117 B6.2 |
| Font smoothing (B5.1) | G | G | Set site-wide, no reason given | Low cost today |
| Optical size, grade (B5.2) | G | G | G (opsz axis present, not mentioned) | Low |
| Weight at small sizes (B5.3) | G | P (detector: body under 12px) | P (weights set explicitly; no "no weight under 400" rule) | — |
| Contrast model (B6) | G | WCAG 2 only | WCAG 2 only, measured | APCA flags `muted-night` and ink-on-turquoise body text |

**Conditions in the house, in one line:** Manta's colour-on-ground rules are the only house rules in this area that state conditions (ground, measured ratio, reason). impeccable states a condition on about half its text rules, and two of its own lines contradict two others (tint, opacity). design-vault holds only the gradient-text ban and the prompts' headline area.

## Part D. Interactions: text treatments against the other choices

1. **Tint × brand palette (one job per colour).** Tint the text neutral toward the *dominant* hue only. Given Manta, text is cool (hue 223–229) on a warm ground (hue 88). This matches "warm = act, cool = read". Given a new brand colour added later near hue 225, it would collide with the text tint and with `lagoon`; check ΔE00 against `ink` and `text-muted` (Manta's near-miss rule, ΔE00 ~7 reads as an error).
2. **Tint × links.** A tinted dark text and a dark link colour are close in luminance (Manta: `lagoon-text` vs `ink` 2.22:1). Given tinted dark text, colour alone cannot mark a link; the underline must. The more the body text is tinted toward the link hue, the stronger this need.
3. **Text colour × surface fills (#117).** Every fill that can hold text (lagoon wash, semantic tints, the white card, sand, turquoise, ink, coral) needs its own measured primary and secondary text. Given a selected or hover wash (`#E6F6F8`), `lagoon-text` reads 5.3:1 and `ink` 11.8:1 (Manta §3); `text-muted` on the wash is 4.97:1, Lc 67.3 (my measurement): it passes WCAG, and APCA puts it under the body-column level. Given alpha tints (`--tint-success` 15%), the chip's text contrast depends on what is under the chip: on white and on sand it differs. Measure both.
4. **Emphasis × the colour budget.** Manta allows one coral object per view and no information-free colour in the working area. So emphasis in the working area must come from weight, size, position and the two greys, not from colour.
5. **Caps × eyebrow ban × tracking.** A small uppercase label above a heading is both an impeccable ban and a Manta specification. Whatever is ruled, if the label stays it needs 5–12% tracking (live: 2%).
6. **Numerals × typeface.** Scores are in Quicksand 700 (no `tnum`); the brand sheet wants a score column. Either accept proportional digits in a chip of fixed width (centre the number in the chip), or set the number in Nunito Sans (tabular by default). This is a typeface-role decision, not a CSS fix.
7. **Dark ground × weight × smoothing × contrast model.** On ink, light text looks heavier (irradiation) but greyscale anti-aliasing thins small text; `muted-night` is at the WCAG limit and under APCA's body level. Given small secondary text on ink (footer, announcement), the weakest point is the colour, not the weight: raise `muted-night`'s lightness before any weight change.
8. **Text over imagery × flat-UI ban × photo honesty.** A scrim is a gradient or a translucent layer; Manta bans gradients in UI and treats listing photos as evidence. Given a hero photo or video with text (Manta's image-to-video plan), the house has no rule that allows a scrim; given a listing photo, keep text off it.
9. **Brand fills × size.** Coral's label must be ≥19px/700; this fixes the CTA's size and weight, which then sets the ceiling for every other label's emphasis in the same view.
10. **Dark mode × tint.** If Manta answers `prefers-color-scheme` later, Radix warns about saturated grey grounds in dark mode, and Material lowers neutral tone, not chroma, for dark text. The night pattern already gives the dark-ground text rules for named contexts; a full dark theme would need the same table for every ground.

## Part E. Per-area summary

- **Hierarchy steps.** Two readable text steps per ground, plus defined disabled and placeholder states; carry more hierarchy with weight, size and space. Solid per-ground tokens for a web palette; alpha only for disabled.
- **Emphasis.** Rank with weight first, then a colour step, then size. In prose, bold or italic, never both, rarely; with a sans, bold. Caps only for short labels, tracked +5–12%. Tabular lining figures for columns and changing numbers; proportional in sentences.
- **Links.** In prose, an underline at rest whatever the colour (WCAG 1.4.1, G183's 3:1 is hard to meet with dark link and dark text). In nav, lists and whole-card targets, context is enough. Hover changes a non-colour property. Visited for content lists only.
- **Text on grounds.** Pick polarity by the fill's lightness, then fix size (WCAG large-text only when truly large). On dark, white text and meaning on borders and icons (Manta's night pattern is good, sourced-by-measurement practice); secondary text on dark needs more margin than WCAG gives. On photos and video, measure the pixels next to the letters at every crop; keep text off evidence photos; scrim or reserved plain area for heroes.
- **Rendering.** Global `-webkit-font-smoothing: antialiased` is a 2012–2018 habit with little effect on current macOS; scope it to dark grounds if kept. Leave `font-optical-sizing: auto`. No weights under 400 at body size. On dark, large text may go slightly lighter (irradiation), small text should not.
- **Answer to the founder's question.** "Saturate text in the direction of the brand colour" is a live practice, not an old mistake, under conditions: a small amount of chroma (the eye reads it as a warm or cool grey, not as a colour), toward the brand's *main* hue (not every brand colour on the page), more on mid greys than on near-black and white, in a perceptual colour space, never in a way that makes plain text look like a link, and always measured for contrast after. It buys cohesion, not readability. On a photo or a saturated fill the rule changes: text takes the ground's own hue or plain white or near-black. Manta already does this and should write it down.

## Part F. Gaps ranked by how often they affect the Manta site

Frequency key: how many Manta surfaces, and how often a session builds one.

| Rank | Gap | Where on Manta | impeccable fills it? | Note |
|---|---|---|---|---|
| 1 | **Inline links in prose have no underline on light grounds** (`a { text-decoration: none }`; `lagoon-text` vs `ink` 2.22:1, under G183's 3:1) | Every guide, destination and legal page with a link in a paragraph (Read mode; the SEO pages are the bulk of pages) | No | Likely WCAG 1.4.1 (A) failure as soon as prose links ship. A one-rule fix in the brand sheet plus CSS. Owner: mantahostels. |
| 2 | **Secondary text on ink at the WCAG limit** (`muted-night` 4.51:1; APCA Lc 40.9) | Footer (every page), nav, announcement block, reward screens, social tiles | No | Raise L (measured options in B6); check ΔE before a ruling. Owner: mantahostels. |
| 3 | **No written tint rule** (Manta tints; no file says chroma band, hue or space; "cool grey neutrals" rejection is ambiguous) | Every new token (search, filters, compare will add greys: disabled, placeholder, dividers) | Split (colorize vs quieter) | Low risk now; drift risk as the working area grows. A portable rule belongs in the vault, but not as a gate question (#103); whether it goes into #119's house override file is for map #96's spec. |
| 4 | **No disabled or placeholder text token** | Search form, filters, date and guest inputs, compare, "no space for your dates" rows | Partly (states listed, no values) | Comes with the search UI (#104 rank 1). |
| 5 | **Text on photos and video** (no rule; scrim vs "UI is flat") | Listing card photos (controls on photo), planned video hero, any future photo hero | Partly (check only) | Shared with #117 B6.2; needs one ruling for both. |
| 6 | **Numerals** (no `font-variant-numeric`; Quicksand score digits proportional, no `tnum`) | Every results row (price, score, review count), compare table | Partly | Nunito Sans is tabular by default, so prices are fine; scores in Quicksand are not. Low severity, high frequency. |
| 7 | **Ink on turquoise for body-size text** (WCAG 5.73:1 passes; APCA Lc 52.4, under the content-text level) | Hero subcopy on every marketing and destination banner | No | WCAG is the legal bar, so this is a design-margin note, not a failure. Keep hero subcopy large. |
| 8 | **Caps labels tracked at +0.02 em** (rule says 5–12%) | Destination card region labels, page region labels | Partly (detector checks wide tracking on body only) | Tied to the eyebrow conflict; Manta's (lucmoseley/mantahostels). |
| 9 | **Dark-ground weight rule** (impeccable "one step more weight" vs irradiation sources) | Night headings, footer | Conflicting | Low impact on Manta (Quicksand and Nunito Sans have no `GRAD`; weights are set). |
| 10 | **Global font smoothing** | All text, macOS with subpixel on only | No | Low; scope to `.ground--ink` if touched. |
| 11 | **Visited links and prose emphasis rules** | Guide lists (visited), guide prose (bold/italic) | No | Low. |

For the vault (portable, all projects): every area except text on art is a gap in design-vault itself; the critic reaches text presentation only through impeccable, which is uncited, split on tint and opacity, and silent on links, numerals in practice, photo text and rendering. Only a rule that can fail a candidate becomes a gate question (#103): text contrast is one (WCAG 2.2 AA, 4.5:1), in the vault.

## Bound

**Read in full:** design-vault `plugin/skills/design-critique/SKILL.md`; House DNA (`dna` in `data/gallery.json`); impeccable 4.5.0 `reference/craft-floor.md`, `typeset.md`, `colorize.md`; Manta `DESIGN.md`; Manta `docs/brand/brand-sheet.md` lines 15–139 (§2, §3 with the night pattern, §4); design-vault `docs/research/design-coverage-gaps.md` (#104); material-components-android `docs/theming/Color.md` role tables (lines 60–100, 455–475, 738–760); material-color-utilities `dynamic_scheme.ts` neutral-palette functions (lines 741–800, 932–990).

**Sampled (grep or part read):** design-vault `docs/research/design-rules-census.md` (#98, grep for text terms; rows B4–B53, X1–X12, conflict list lines 389–396); `docs/research/manta-design-migration.md` (#115, grep; items C3–C10, L1, L10, T3, Z2); `docs/research/impeccable-checks.md` (detector rule list lines 73–76); `.claude/tmp/research-surface-styling.md` (#117, headings, Part A, grep for scrim, text, link); design-round `SKILL.md` and `references/*.md` (grep); impeccable all `reference/*.md` (grep for tint, neutral, grey/gray, chroma, underline, emphasis, scrim, overlay, uppercase, caps, letter-spacing, tracking, tabular, lining, smoothing, antialias, optical, opsz, grade, visited, text-shadow, italic, opacity, link, contrast), `new-work.md:63-72`, `quieter.md:48-62`; Manta `docs/brand/brand-sheet.md` (grep for link, underline, caps, numer, italic, tracking, scrim, overlay, photo, muted, grey, weight, smoothing), `app/globals.css` (grep, then lines 10–30, 100–200, 205–260, 425–465, 636–682), `app/_fonts.ts`.

**Measured by me (scripts in `/tmp/fontprobe/`):** OKLCH and WCAG 2 contrast of Manta text tokens (`oklch.py`); APCA Lc (`apca.py`, constants checked against `apca-w3@0.1.9/src/apca-w3.js` from unpkg); `muted-night` lightness options (`find.py`); font axes and OpenType feature tags of Manta's `NunitoSans.ttf` and `Quicksand.ttf` (`probe.py`), default digit advance widths (`digits.py`, default instance only; HVAR not read).

**Web sources read through the fetch tool:** W3C Understanding 1.4.1, 1.4.3, 1.4.12; techniques G183, G18; GOV.UK Design System links; NN/g guidelines-for-visualizing-links (2004, note 2026), low-contrast (2015), text-over-images (2015, reviewed 2026); Butterick bold-or-italic, all-caps, underlining, letterspacing, alternate-figures; Radix understanding-the-scale, composing-a-palette; Tailwind colors; Evil Martians OKLCH article; Apple HIG Color (first 100k characters), Typography (first 100k), Dark Mode (JSON); MDN font-variant-numeric, font, font-smooth, font-optical-sizing; APCA in a Nutshell; Roselli WCAG3 contrast (Apr 2026); web.dev adapting-typography (Argyle); nerdy.dev irradiation post; Scholars' Mine abstract of Hall and Hanna 2004.

**Search-snippet level only:** Refactoring UI (Medium returned 403; read through a third-party copy and summaries, so its wording is second-hand); Material 2 alpha emphasis values (.87/.60/.38) and M3 dropping them; Bringhurst §2.1.6 (via Rutter's *Web Typography*); Legge, Rubin and Luebker 1987; Dobres, Chahine and Reimer 2017; macOS Mojave subpixel change (blogs).

**Searches run:** Refactoring UI grey text on coloured backgrounds; Refactoring UI "greys don't have to be grey"; Material text emphasis opacity; M3 on-surface-variant; Hall and Hanna 2004; Dobres 2017 polarity; Legge 1987 contrast; WCAG text over image G18/G145; Bringhurst letterspacing caps; Mojave subpixel antialiasing; variable font grade dark mode.

**Not opened:** the m3.material.io pages (script-rendered; Google's code and Android docs used instead); the CSS Fonts 4 spec text for `font-optical-sizing` (fetch truncated before §8.1, so the px mapping is inferred); Apple HIG Color and Typography after character 100,000 (tracking table not read); the Refactoring UI book itself; the full Hall and Hanna, Legge, and Dobres papers; Manta `docs/design-system/guidelines/colors-night.html` beyond its grep hit (a guideline page's own ratio labels use `tabular-nums` at 11.5px in `muted-night`; not the product); Manta page-by-page check for prose links on light grounds; ΔE00 check of a lighter `muted-night` against other tokens.
