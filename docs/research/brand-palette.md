# Brand palette: colour interaction, minimum difference, logo grounds, client logo colours (design-vault#143)

Status: complete (14 Oct 2026).
Language: ASD-STE100 Simplified Technical English (approximate).
Parent map: design-vault#96. Ledger items: C6, C9, L1, L2, L3, L4 (`docs/research/manta-design-migration.md`).

## Short answer

- **Judge a colour where it sits, and measure it in a perceptual space.** A colour moves toward the complement of its neighbour (Chevreul). An edge vibrates when the hues contrast and the lightness is near-equal (Albers, Spectrum). Measure hue and lightness in OKLCH or CIELAB, never in HSL. Manta's 166°/176° shimmer argument is in HSL. When I measure it, coral and rose-coral are both near-equal in lightness to turquoise (1.33:1 and 1.45:1). Rose-coral's rejection still holds, but for other reasons (Part 1).
- **Harmony: near hues for the body of the palette, one contrasting hue as the figure.** Schloss & Palmer 2011 found that harmony rises with hue similarity, and that people like a figure colour more as its hue contrast with the ground grows. Current systems (Material 3, Radix, Carbon, Apple) agree: colours are roles, one hue family does the action, and families are lightness ramps (Part 1).
- **Two palette colours are the same token or decisively different.** This applies to identities and meanings, not to steps of one ramp. Sources fix the lower bound: one JND is ΔE00 2 (CSS Color 4), and print tolerance is 2-4. Szafir shows that small marks need a larger difference. **No source gives the upper number.** Manta's ~7 is supported in kind, not in number. Manta's own data show two thresholds, ~10 for a near-miss and ~15 for two meanings in one view, so its "10-20 safe" is wrong (Part 2).
- **ΔEOK ranks pairs differently from ΔE00.** Do not divide a ΔE00 threshold by 100. Use ΔE00, or ΔEOK2 (Part 2.3).
- **A logo's grounds come from its lightness band.** A ground inside the band is banned. On every other ground, use the 3:1 point. Ship a small set of named versions (full colour, reversed, one-colour, keyline where needed), each with its own grounds. Change the version or the ground; never recolour for one page (Spotify, GOV.UK, Aramco, CSU Chico). WCAG's logo exemption does not cover a low-contrast placement that the designer chose, so the 3:1 check is what keeps a placement inside the exemption (Part 3).
- **A client's logo colours are fixed anchors unless the client opens them.** Give each one a job or make it logo-only. Build the other colours by relation to them in OKLCH. Check every palette colour against them by Part 2. Only the side the house owns may move (Part 4).
- **mmm-infra, measured.** The blue `#0070C0` needs grounds at L\* ≥ 79.7. No dark ground works for the full-colour logo, so slate needs a reversed white logo, and mist (2.83:1) is banned. Round 2's slate is the blue's own OKLCH hue (252° against 250°), which explains why that pairing works. Round 1's rejected v3 put a near-miss grey (ΔE00 7.9) on the logo. The site's `#3F3F3F` is the logo grey (ΔE00 0.3), so they are one token (4.3).
- **The founder must rule on:** the house numbers 10 and 15, and the fit-gate "clash" test in 4.3 step 5. Step 2's Colour and Logo questions are drafted below.

## How to read this file

- Each principle has these fields: **Rule**, **Era** (T = timeless; E = era-bound, with its date), **Applies when**, **Trades off against**, **Yields to / clash resolution**, **Source (strength)**.
- Strength: **P** = primary (standard, paper, official first-party document that I read). **Pr** = practitioner (named designer, studio, book, blog). **M** = my own measurement (method under §Measurements; the scripts were session scratch, not kept in git). **None** = no source found.
- Read status of a source is in the Bound section at the end.
- The house writes a rule only where no source gives it (ruling #119). Where a source gives the rule, the rule cites it and the house adds only the condition.

## Local findings (read first)

- **impeccable 4.5.0 `colorize.md` (read in full, 86 lines).** It covers: roles, not "a bag of swatches" (canvas, text, action, focus, borders, semantics, data); OKLCH for a new web palette; "vary lightness and reduce chroma near white and black"; the WCAG AA table; CVD simulation; "Preserve confirmed brand and semantic conventions" and "Additional context needed: existing brand colors". `new-work.md:65` gives four colour strategies (Restrained, Committed 30-60%, Full palette 3-4 named roles, Drenched). `distill.md:51`: "Use 1-2 colors plus neutrals, not 5-7 colors". **It is silent on:** colour interaction (simultaneous contrast, complement vibration, analogous ramps, a ground that shifts a hue), a minimum distance between two palette colours, the grounds a logo may sit on, keylines, the WCAG logotype exemption, and how a client's logo colours meet a new palette. A grep of all `reference/*.md` for logo and wordmark finds only `init.md` and `document.md:395` ("A binding logo, identity asset … carry only durable product constraints"). `new-work.md:69-71` also tells the model that a warm cream ground plus a serif is its own default look, which bears on mmm-infra (both round-2 leaders are warm off-white plus serif).
- **design-vault `design-project/SKILL.md` step 2** asks for "the client's colours with hex values" (§2) and "where the files live" (§4). It asks nothing about the roles of the colours, the grounds of the logo, or whether the logo colours are fixed. **`fit-gate.md` §2** fails a candidate "where its colours clash with the mark's or replace the client's own", but "clash" has no test.
- **mmm-infra.** The logo colours are `#0070C0` (wordmark) and `#404040` (arches). `#0070C0` is Microsoft Office's standard "Blue" (a brand-sheet line said so until commit e5b6918 cut it, 4 Oct 2026), so the logo colours were probably Office defaults, not a designed palette. Round 1 (5 Oct): the founder rejected v3 Inscription ("wrong palette": minium `#86230f`, granite `#b8b5ad`, lime `#ecebe6`, cut `#2a2925`; the logo was recoloured to `#2a2925` and the blue was dropped) and v4 Water ("muted green: no link to Mark's colours"; the logo recoloured to foam `#f1f6f3`). The critics called the recolour "Mark's call … not a defect" (critic-v3 L97, L178; critic-v4 L112, tag `rounds/site-look-r1-v1e`). Round 2's brief then bound "The house colours: blue `#0070C0` and grey `#404040`. The founder likes them, and every tile is built in or around them" (`r2/README.md`, branch `rounds/site-look`). The two leaders (6 Oct): v1 Counsel's paper (paper `#F8F6F0`, pad `#F4ECB0`, blue, ink `#404040`) and v7 Mark at work (paper `#F7F5F0`, slate `#223448`, mist `#B8C1CB`, hair `#D8D4CB`, blue, ink). So mmm-infra already moved, by the founder's ruling, from "palette free, logo recoloured" to "logo colours fixed, palette built around them". No file states this as a rule; `docs/brand/brand-sheet.md` §2 still says "open".

## Part 1. Colour interaction and harmony (ledger C9)

### 1.1 Simultaneous contrast: a colour takes on the complement of its neighbour

- **Rule.** Two colours that touch look as different as possible, in hue and in lightness. Each colour moves toward the complement of the colour next to it. A dark colour beside a light one looks darker, and the light one lighter. Thus judge a palette colour on the real ground and beside the real neighbours that it will have, never as a swatch on white.
- **Era.** T.
- **Applies when.** Two colours share an edge, or a figure sits on a ground. The effect is largest for a small figure on a large, saturated ground (Albers' plates use this; Chevreul's stripes "if the stripes are not too wide").
- **Trades off against.** Approval of tokens from a swatch sheet.
- **Yields to / clash.** Nothing overrides it; it is perception. Where a token must work on several grounds, the token is checked on each ground (this is the same discipline as the text-safe partner rule, C3, for contrast).
- **Manta check.** Sheet §3 says the warm cream ground makes a 10° hue nudge "land pinker". The direction agrees with Chevreul: a yellowish ground adds its complement (blue-violet) to the figure, so a red moves toward pink-magenta. The size of the shift is not measured. `sand-page` has low chroma (C\* 6.4), so the shift is probably small.
- **Source.** Chevreul, *The Principles of Harmony and Contrast of Colours* (1839; English translation 1854, archive.org `principlesofharm00chev`), §16 and the Introduction: "In the case where the eye sees at the same time two contiguous colours, they will appear as dissimilar as possible, both in their optical composition and in the height of their tone"; "The contiguous colours are modified in hue, as if the complementary of the neighbouring colour was added to each"; and (§19) "that which is deep appears deeper, and that which is light, lighter". **P** (primary text, key passages read).

### 1.2 Vibrating boundaries: contrasting hues at near-equal lightness

- **Rule.** An edge between two colours vibrates, or seems to float at a different depth, when the two colours have a large hue difference **and** near-equal lightness (and usually high chroma). The cause is the lightness difference, not an exact complement. A pair with a large lightness difference does not vibrate, whatever the hue angle.
- **Era.** T (perception). The measurement tools are E (2020s: OKLCH, CAM16).
- **Applies when.** Two saturated colours touch: a saturated CTA on a saturated hero ground, coloured text on a coloured field, a logo colour on a brand field.
- **Check.** Measure ΔL\* (or OKLCH L) and the WCAG contrast ratio of the pair, and both chroma values. Albers' own vibrating plates measure ΔL\* 0.1 to 3.4 (Sadoughi 2024, Table 1). **No source gives a safe ΔL.** A pair at 3:1 or more (WCAG 1.4.11 level) has a clear lightness edge; under about 1.5:1 with high chroma on both sides, look at it rendered.
- **Trades off against.** Energy. A high-chroma, contrasting-hue figure on its ground is the strongest "look here" signal (see 1.3, figural preference).
- **Yields to / clash.** WCAG wins where the figure is text or a control boundary (#123; 1.4.3, 1.4.11). Otherwise the resolution is Spectrum's: separate the two in lightness, or put a neutral between them ("Use static white or static black components instead of colored components on top of color or image backgrounds"). A white label on a coral button is this kind of neutral.
- **Manta check (measured).** Sheet §3 rejects rose-coral `#FA4F52` because "at 176° from turquoise it is a near-exact complement, producing edge shimmer … that coral's off-complement 166° avoids". **The 166° and 176° are HSL hue angles** (HSL hues: turquoise 175.0°, coral 10.7°, rose-coral 358.9°). In perceptual spaces the gaps are smaller and neither colour is a near-exact complement: CIELAB 145° (coral) and 157° (rose-coral); OKLCH 152° and 162°. On the axis that causes vibration, both pairs are near-equal in lightness: coral on turquoise ΔL\* 8.9, 1.33:1; rose-coral on turquoise ΔL\* 11.5, 1.45:1. So the measurement does **not** support "coral avoids shimmer, rose-coral produces it". Both are in the same risk zone, and coral is slightly nearer equal lightness. Rose-coral's rejection still holds on two other grounds that measure: it is only ΔE00 8.9 from coral (a near-miss of the token it was to replace, see Part 2), and it moves toward `danger` (CIELAB hue 29° against danger 19°; ΔE00 22.6 against coral's 28.5), which weakens the coral/danger hue separation the sheet requires. Whether coral shimmers on the turquoise hero is a look test that I did not do.
- **Sources.** Sadoughi, "Translating Albers to CAM16", AIC 2024 (PDF read in full): "For vibrating and vanishing boundaries, Albers states colors must be equally light but from differing hues, a task impossible to execute in HSB & HSL"; measured Albers 1964 first-edition plates XXII-1 to XXIII-3. **P** (peer-reviewed conference paper measuring the primary). Albers, *Interaction of Color* (1963), chapters "Vibrating boundaries: enforced contours" and "Equal light intensity: vanishing boundaries": **not opened** (titles from catalogue records; content through Sadoughi). Adobe Spectrum, "Color system", section "Hue and saturation contrast": "Avoid placing colors directly on top of or adjacent to other colors that have a high degree of hue contrast with near-equal saturation or lightness. These scenarios create a visual illusion of depth or vibration (chromostereopsis)" (spectrum.adobe.com/page/color-system, read 14 Oct 2026). **P** (first-party design system), **E** (current). Livingstone & Hubel 1987, *J Neurosci* 7(11):3416 (abstract only: separate pathways for colour and for form, movement and depth) and Livingstone, *Vision and Art* (2002), through Harvard Gazette, 17 May 2002 ("a disconnect between the color and luminance pathways" makes a sunset "shimmer"). **Pr / secondary** for the mechanism.

### 1.3 Harmony: similar hues for the palette body, a contrasting hue only for the figure

- **Rule.** People judge colour pairs as more harmonious, and like them more, as the hues get more similar. Lightness contrast raises liking. Pairs of strongly contrasting hues are judged neither harmonious nor preferred as pairs. **But** a figure colour is liked more as its hue contrast with its background grows. So: build the body of the palette from near hues (an analogous family) with steps in lightness; let a contrasting hue appear only as a figure (the one action, a badge), never as a second field of equal weight.
- **Era.** T (empirical, 2011).
- **Applies when.** Choosing the hue families of a palette and which colour may sit on which.
- **Trades off against.** Recognition and energy. A palette of one hue family can read as dull (mmm-infra round 1 v5, "boring"). The contrasting figure is where energy comes from.
- **Yields to / clash.** Against the colour-wheel schemes (complementary, triadic) taught by Itten and in most palette generators: the measured preference data do not support "complementary = harmonious" as a pair; they support complementary as figure on ground. Use the data. Against one-job colour (C1): agrees, because the figure colour is the one action.
- **Manta check.** Manta's structure fits this: a warm, near-hue family (sand CIELAB h 93° and 92°, amber 81°) with coral at the hot end (41°) as the single figure; turquoise as the ground family. The sheet's "a hue nudge that leaves the warm analogous ramp becomes an unrelated second accent" agrees with the data in direction. In CIELAB, rose-coral (29°) does not leave the arc; it extends it past coral toward danger (19°). So the rejection's measurable reason is the danger collision, not the ramp (1.2).
- **Source.** Schloss & Palmer, "Aesthetic response to color combinations: preference, harmony, and similarity", *Atten Percept Psychophys* 73(2):551-571, 2011: "pair preference and harmony both increase as hue similarity increases, but preference relies more strongly on component color preference and lightness contrast. Although pairs with highly contrastive hues are generally judged to be neither preferable nor harmonious, figural color preference ratings increase as hue contrast with the background increases." **P** (abstract read; full text not read). Ou & Luo 2006 (two-colour harmony model, *Color Res Appl* 31(3)): **could not open**.

### 1.4 What current design systems do: roles, one action colour, ramps by lightness

- **Rule (the shared core, 2021-2026).** (a) A palette is a set of **roles**, not swatches: grounds and surfaces, text (two steps), action, focus, borders, semantics. (b) **One** hue family carries action. Up to two more accent families are allowed where each has its own job. (c) The neutrals are a family of their own, often tinted toward the main hue (#123 B1.1 covers this). (d) Each family is a **lightness ramp**, and contrast is designed by lightness step, never by hue. (e) The semantics (error, success, warning) take conventional hues, apart from the brand hues.
- **Era.** E (current, 2021-2026).
- **Per system.**
  - Material 3: three accent groups (primary, secondary, tertiary), each with 4-5 roles, plus neutral, neutral variant and error (material-components-android `docs/theming/Color.md`). Tone is CIELAB L\*; "a difference of 40 in tone guarantees a WCAG contrast ratio ≥ 3.0; a difference of 50 in tone guarantees a contrast ratio ≥ 4.5" (material-color-utilities `concepts/contrast_for_accessibility.md`). **P.**
  - Radix Colors: a 12-step scale per hue, each step a fixed role (1-2 backgrounds, 3-5 component grounds, 6-8 borders, 9-10 solid fills, 11-12 text); "choose the gray scale which is saturated with the hue closest to your accent hue"; "Radix Colors are not intended to be customised … we recommend adding custom scales alongside Radix scales" (radix-ui.com/colors/docs, read 14 Oct 2026). **P.**
  - IBM Carbon: "The neutral gray family is dominant"; "The core blue family serves as the primary action color"; "Additional colors are used sparingly and purposefully"; ten grades per hue, with a table of the minimum grade steps for 3:1 and 4.5:1 (carbondesignsystem.com/elements/color/overview). **P.**
  - Apple HIG, Color: "Avoid using the same color to mean different things … if you use your brand color to indicate that a borderless button is interactive, using the same or similar color to stylize noninteractive text is confusing"; in "apps with primarily monochromatic content or backgrounds, choosing your brand color as the app accent color can be an effective way"; with colourful content, "prefer a monochromatic appearance for toolbars" (developer.apple.com HIG JSON, read 14 Oct 2026). **P.**
  - Adobe Spectrum: colours generated in Leonardo "by plugging in hues and hue ranges through key colors … combined with target contrast ratios"; brand key colours may "shift the actual hue in order to keep colors bright or recognizable". **P.**
  - impeccable 4.5.0: roles; OKLCH; four strategies (Restrained, Committed, Full palette 3-4 roles, Drenched); `distill.md` "1-2 colors plus neutrals, not 5-7". **Pr** (house tool).
- **Accent count.** No source gives one number for a brand palette. The sources agree on **one action colour** (Carbon, Apple, Material primary, Manta coral). Material allows three accent families; impeccable's Full palette allows 3-4 roles. The house rule that follows from the sources: one action family; every other hue has one named job (Apple "same color … different things"; Manta C1); a hue with no job is cut.
- **Trades off against.** Expression. Persuade and Experience surfaces may carry more colour (impeccable's Committed and Drenched strategies). The role rule still holds there: a colour field is a ground role, not a free accent.
- **Yields to / clash.** WCAG first, then the project's rules file (#119 F5 precedence).

### 1.5 Measure hue and lightness in a perceptual space, never in HSL

- **Rule.** Record and compare palette colours in OKLCH (or CIELAB L\*/HCT for lightness, and OKLCH for hue). HSL lightness and hue are not perceptual: HSL cannot set two colours to equal lightness (Sadoughi 2024), and CIELAB bends blue hues toward purple ("Between chroma of 25 and 75, the hue is visibly purple", CSS Color 4 §9, of a constant CIELAB hue at sRGB blue; OKLCH keeps the hue constant).
- **Era.** E (CSS Color 4 and OKLCH tooling, 2020s).
- **Why it matters here.** Manta's hue arguments (166°, 176°, "sand 44° → amber 40° → coral 9°", "danger 346° against coral 9°") are HSL numbers (measured: HSL hues sand 42.4°, amber 40.1°, coral 10.7°, danger 347.5°). Their conclusions must be re-read in a perceptual space (1.2). For mmm-infra, the logo blue `#0070C0` is CIELAB h 275° but OKLCH h 250°; round 2's slate `#223448` is OKLCH h 252°, so in OKLCH slate is the logo's own hue, darker and greyer (Part 4).
- **Source.** W3C CSS Color Module Level 4 (Candidate Recommendation Draft, fetched 14 Oct 2026), §9 and §20. **P.** Sadoughi 2024. **P.**

## Part 2. A minimum difference between two palette colours (ledger C6)

### 2.1 Decisively the same or decisively different, by job

- **Rule.** Two palette colours that can appear in one view are either **the same token** or **decisively different**. A pair that is only a little different reads as a mistake: the eye sees a difference and finds no reason for it. This binds where the two colours are **separate identities or meanings** (two accents; a brand colour and a semantic colour; a logo colour and the token beside it). It does **not** bind steps of one lightness ramp (ground, surface, border), which are meant to be small; for those, the smallest step that is still visible is the aim (Tufte), and its check is contrast (#117 P8: a fill step under 1.1:1 needs a border).
- **Era.** T.
- **Applies when.** A new token is added; a client colour or a logo colour meets the palette; two meanings share a hue family.
- **Trades off against.** Richness. A palette that keeps all its colours far apart has fewer colours, or colours far from the brand's hue. Tufte's "smallest effective difference" pulls the other way for hierarchy.
- **Yields to / clash.** Between Williams (make different things really different) and Tufte (make distinctions as subtle as possible, but still clear): the job decides. A difference of **identity or meaning** takes Williams. A difference of **rank inside one family** takes Tufte, with WCAG as the floor where the step carries information.
- **Sources.** Apple HIG, Color: "using the same or similar color to stylize noninteractive text is confusing" (similar colours are read as the same meaning). **P**, E (2025-2026). Williams, *The Non-Designer's Design Book*, ch. 5 Contrast: "If two items are not exactly the same, then make them different. Really different"; a difference that is "sort of different, but not really" gives "conflict" (wording from search excerpts of the 3rd edition; the O'Reilly page returned 403; **Pr, wording unverified**). Tufte, *Visual Explanations* (1997), ch. 4 "The smallest effective difference": "make all visual distinctions as subtle as possible, but still clear and effective" (p. 73, through Boxes and Arrows and IFTF quotations; **Pr, not read in the book**). Manta's sheet §3, "Colour relationships must be decisively identical or decisively different; near-misses read as mistakes": **F + M**.
- **Manta check (measured).** Manta's nearest token pairs are its neutral steps: `sand-border`/`sand-page` ΔE00 3.7, `sand-page`/`surface` 5.8, `sand-border`/`surface` 8.8. These are inside Manta's own "error" band, and they are correct, because they are ramp steps, not identities. Every other pair is ≥ 12.9.

### 2.2 The numbers: what the sources give

| Band (ΔE00) | What it means | Source | Strength |
|---|---|---|---|
| ~1-2 | One just noticeable difference. CSS Color 4: "using deltaE2000, one JND is 2"; "For the OkLCh color space, one JND is … 0.02" (deltaEOK). | W3C CSS Color 4 §14.2.1 (CRD, fetched 14 Oct 2026) | P |
| 2.0 | A brand owner's tolerance for one corporate colour in premium print. | ChromaChecker "Realistic ΔE values" (vendor manual) | Pr |
| 2.5-4.0 | Spot-colour production tolerance (premium+ 2.5-2.8, premium 2.8-3.5, typical 3.5-4.0). | ChromaChecker | Pr |
| 3.5 / 5 | ISO 12647-2:2013 solids tolerance, CMY / black, ΔE00 (informative; "no justification" found for the values). | Yu, Chung & Myers, TAGA 2015 (abstract) | P (abstract) |
| ~5-7 (CIELAB units) | For small marks, the difference that 50% of viewers notice. Perceived difference "varies inversely with size": small, thin parts need a larger ΔE to be seen as different. | Szafir, "Modeling Color Difference for Visualization Design", IEEE TVCG 2018 (VIS 2017 slides read; abstract through search); Stone, Szafir & Setlur 2014 (abstract) | P |
| >5 | Outside CIEDE2000's range: "the CIEDE2000 color-difference equations are only applicable for small color differences". | Sharma, Wu & Dalal 2005, *Color Res Appl* 30(1) (read: note 5 and the discontinuity section) | P |
| ~7 reads as an error; 10-20 safe | Manta's thresholds. | Manta sheet §3, §14 | F + M, **no source** |

- **What the evidence supports.** Industry calls a pair at about ΔE00 ≤ 2-4 "the same colour" (it accepts that much drift between a print and its target). At small sizes, about half of viewers do not see a difference of about 5-7 CIELAB units. So a pair at **ΔE00 ~4-10** is above "the same" and below "clearly meant": some viewers see two colours, some see one, and no one sees a reason. **The ~7 figure is supported in kind, not in number.** No source names a ΔE at which a difference "reads as deliberate"; I searched design systems (Material, Radix, Carbon, Spectrum, Apple HIG: none publishes a minimum ΔE between palette colours) and categorical-palette tools (qualpal, palettecore, Colorgorical, iWantHue: they maximise the smallest pairwise distance and set no fixed floor).
- **The upper number ("10-20 safe") contradicts Manta's own data.** Manta withdrew `warning-night` at ΔE00 12.4 from `amber`, `success-night` at 13.5 from `turquoise` and `lagoon-night` at 13.4 from `turquoise`, and moved `blush` at 10.3 from `danger-night`, because each "collided" with a token of a different meaning in the same view. It called 15.7 (`warning`/`amber`) and 20.3 (`success`/`turquoise`) adequate. So Manta's practice has **two** thresholds, not one: about 10 for a near-miss of the same intended colour, and about 15 for two **meanings** in one view. All twelve ΔE00 values in sheet §3 and §14 re-measure exactly (script, §Measurements).
- **Large differences are an extrapolation.** CIEDE2000 was fitted on small differences (Sharma 2005), so ΔE00 10 against 15 is a rank, not a calibrated perceptual step. A 2023 test of 17 formulae over 28 data sets found CAM16-UCS best across small and large differences (Luo et al. 2023, through a search summary; **not opened**). For a palette check the rank is enough; the numbers stay house numbers.

### 2.3 ΔEOK (OKLab) in current tooling

- CSS Color 4 defines deltaEOK as plain Euclidean distance in OKLab, one JND = 0.02, and says it "under-estimates differences in colorfulness, compared to differences in lightness"; it adds ΔEOK2 (a and b scaled by 2) and ΔEOKr2 (plus a lightness toe), which "agrees significantly better with ΔE2000" (§20.3-20.5). **P**, E (2025).
- **Measured consequence.** ΔEOK ranks Manta's pairs differently from ΔE00. `peach`/`danger-night`: ΔE00 20.4, ΔEOK 0.081; `warning-night`/`amber`: ΔE00 12.4, ΔEOK 0.139. ΔEOK2 puts them back in ΔE00's order (0.153, 0.142). So a ΔE00 threshold must **not** be converted to ΔEOK by dividing by 100. Use ΔE00, or ΔEOK2 with its own calibration.
- Design-system generators do not use ΔE to space a palette: Material spaces by HCT tone (contrast), Radix and Leonardo by contrast ratio, Carbon by grade steps. ΔE is used only in gamut mapping (CSS) and in categorical-palette tools.

### 2.4 The rule, in the house form (only the numbers are house)

- **applies-when:** a new colour (token, client colour, logo colour) can appear in the same view as an existing token.
- **check:** ΔE00 to every token of the palette, on the screen.
- **writes:** the token list.
- **output:** ΔE00 < ~2: the same colour; use the existing token. ~2 to ~10, and the two can be seen together: a near-miss; snap to the token or move it apart. ≥ ~10 with the same intended meaning: separate colours. Two **meanings** in one view: ≥ ~15, and the meaning also carried by a label or icon (WCAG 1.4.1; Manta C7). Ramp steps of one family: exempt; check contrast instead.
- **yields-to:** WCAG contrast where the colour carries text or a control boundary; a client's fixed logo colours (Part 4).
- **conditions on the numbers:** small or thin parts (a 19px wordmark, a keyline, an icon) need the larger end (Szafir). Two colours that never share a view may sit closer (Manta keeps the mark's `#2BA6CE` at 9.0 from `lagoon` because they are never adjacent).
- **source:** the rule P/Pr (2.1); the lower bound P/Pr (JND, print tolerance); 10 and 15 **house, from Manta's measured cases**, flagged for the founder.
- **era:** T.

## Part 3. Which grounds a logo may sit on (ledger L1, L3, L4)

### 3.1 The mark's lightness band decides its grounds, not its hue

- **Rule.** Measure the mark's lightness: the L\* range of its fills and its area-weighted mean. A ground whose lightness lies inside that band is banned for the full-colour mark: figure and ground merge. For each ground, find the fill lightness it needs (the 3:1 point, below). Where no single fill clears every ground the project needs, the answer is **deployment rules** (which version on which ground, or a bounded ground under the mark), not a recolour.
- **Era.** T (figure-ground is perception; the 3:1 number is WCAG 2.x, 2008-2023).
- **Applies when.** The mark, or a lockup, is placed on any ground: page, hero field, photograph, dark band.
- **The number.** Established guidelines state the rule without a number: "too close in tone to the logo's colors" (Aramco), "low-contrast areas where legibility is compromised" (Spotify), "Do not use the wordmark on overly busy or low-contrast backgrounds" (GOV.UK). The **3:1** that Manta uses is WCAG's level for graphical objects, borrowed as an engineering proxy, because the logo itself is exempt (3.4). Measure it on the fill **and** on any keyline; the mark passes on a ground where one of them clears 3:1 all around the shape.
- **Trades off against.** Colour fidelity of the mark and freedom of the page grounds. The more grounds a site wants (a brand field, a dark band, photographs), the more versions the mark needs.
- **Yields to / clash.** A client's brand guidelines win (they are the reason the exemption exists). Between "keep the full-colour mark" and "use this ground": change the version or the ground, never recolour the mark for one page (Spotify: "Its orientation, color, and composition should remain as indicated"; GOV.UK: "Do not alter colour balance within the wordmark").
- **Manta check (measured).** I rendered `mark-final.svg` in Chromium and measured all opaque pixels (keyline, eyes and catchlights included, so slightly darker than the sheet's fill-only figure): L\* mean 65.7 (sheet: fill mean 66.6), p5-p95 42.4-82.0. Fill contrast by mean luminance: ink 5.18:1 (sheet 4.91), white 2.53 (2.64), sand 2.35 (2.48), turquoise 1.11 (1.20). Every verdict in sheet §6 holds. The fill limits re-compute exactly (ink needs L\* ≥ 50.7; turquoise needs L\* ≤ 38.3). The "ground at L\* 103.6" in §3 re-computes as L\* 106.7 from the mean L\*; both are above white, so the conclusion holds.
- **Sources.** Spotify for Developers, Design guidelines (developer.spotify.com/documentation/design, read 14 Oct 2026): "The Spotify green logo should only be used on a black or white background"; black logo on light grounds, white on dark; "Don't place the logo in a busy area, or in low-contrast areas where legibility is compromised." **P** (first-party), E (current). GOV.UK brand, Logo elements (brand.design-system.service.gov.uk, read 14 Oct 2026): on Primary blue, white and Accent teal; on a light background, black and Primary blue; white or black "against a busy background or in print situations where colour is not possible". **P**, E (2025). Aramco brand, Brandmark system (brand.aramco.com, read 14 Oct 2026): "avoid placing it on backgrounds—solid, patterned, or photographic—that are too close in tone to the logo's colors". **Pr** (corporate guideline). NHS England identity (through a search excerpt; the page did not load): blue-on-white is the core version; white, NHS Blue or pale grey grounds; reversed white only out of 100% NHS Blue, never a tint. **Pr, not read directly.** Mastercard Brand Center (403 on fetch; through search excerpts): full-colour required on screen; grayscale or solid one-colour versions where full colour is not possible, with "sufficient contrast"; clear space a quarter of one circle's width. **Not read directly.**

### 3.2 A small, named set of versions, each with its grounds

- **Rule.** A mark ships as a few named versions, and each version names the grounds it may sit on: (1) full colour, on the neutral or approved grounds; (2) reversed (white, or white plus one accent), on one or a few named dark brand grounds; (3) one-colour (black, white, or `currentColor`), on photographs, busy grounds, other colours and colourless print; (4) where needed, a keyline version (3.3). Clear space is set in units of the mark itself (Spotify half the icon height; GOV.UK the wordmark's dot; Mastercard a quarter circle; Aramco 100% of the logo height), so it scales with the mark.
- **Era.** T (print-era practice, current in every guideline read).
- **Applies when.** Set-up of any project with a mark; any new ground.
- **Trades off against.** Simplicity (one file everywhere). One version everywhere works only where all grounds are in one lightness class.
- **Yields to / clash.** Client guidelines win where they exist. Where none exist (most small clients, mmm-infra included), the round proposes the set and the founder rules.
- **Manta check.** Manta has three versions by **size** (primary, nav, flat) and one set of ground rules; its full-colour mark covers ink, white and sand, and the flat `currentColor` version covers the rest. This fits practice. Manta has no reversed version because ink is already the mark's best ground.
- **Source.** As 3.1. **P/Pr.** Minimum size and small-size variants are out of scope here (L6, L7; #112 holds the lockup's minimum size).

### 3.3 Keyline: a fix for a ground in the mark's tone range, used only where needed

- **Rule.** A keyline (an outline around the mark) is the version for a ground that matches part of the mark's tone, where the mark would "blend in, disappear, or vibrate". Practice makes it a **separate version used only where the primary is not legible**, usually a white keyline.
- **Era.** T.
- **Applies when.** A ground inside or near the mark's lightness band cannot be avoided (a photograph, a brand field).
- **Trades off against.** The keyline changes the read of the mark: it looks like a sticker (Manta rejected an `ink` keyline for "the outlined-sticker read"). It also adds a colour to the mark, which must itself pass the near-miss check (Part 2) against the ground and the fill.
- **Yields to / clash.** Against a bounded ground (Manta's ink wave): a bounded ground keeps the mark in full colour and needs no keyline; prefer it on hero surfaces where the layout allows. Against "no recolour": a keyline is an addition, not a recolour, so practice allows it as a supplied version.
- **Manta check.** Manta builds the keyline into the primary on every ground (`lagoon-text`, 5.47:1 on sand, 5.90:1 on white, 2.22:1 on ink as an "atmospheric" edge). This differs from practice (a separate version), and it is a defensible choice for a light mass that must sit on light grounds: on those grounds the keyline is what clears 3:1. How Manta chose the keyline colour (contrast to the light grounds, plus separation from the fill) has **no external source**; the sources only show white keylines.
- **Sources.** CSU Chico brand, Logo color versions (csuchico.edu, read 14 Oct 2026): use the keyline version when "the color of the background matches parts of a logomark and causes them to blend in, disappear, or vibrate", and "We do not place a color logo version on a dark background because low contrast severely impacts readability". Aramco: "The keyline logo features a white outline to improve visibility over busy or low-contrast backgrounds. Use only when primary logo versions are not sufficiently legible." **Pr** (institutional guidelines).

### 3.4 The WCAG logotype exemption: what it covers and what it does not

- **Rule.** WCAG 1.4.3: "Logotypes: Text that is part of a logo or brand name has no contrast requirement." Understanding 1.4.11 extends this to logos as graphics: "Logos are exempted from contrast requirements, under the assumption that they must comply with stricter color choices mandated by corporate identity or brand guidelines." Three limits, from the Understanding documents:
  1. **An author's choice is not exempt.** "If logos normally have sufficient contrast but are presented with an insufficient contrast as an author choice, rather than because of corporate identity or brand guidelines, then that particular low contrast presentation is not exempt" (1.4.3 and 1.4.11). Logos greyed until hover fail.
  2. **A logo that is a control** (the nav home link) is "problematic"; authors "should consider choosing a variant of the logo or logotype that has sufficient text contrast, if allowed by the corporate identity or brand guidelines", or provide an equivalent control that meets contrast.
  3. **Brand colour on ordinary text is not exempt**: "text that has insufficient contrast due to corporate identity or brand guidelines is not exempted".
- **Era.** E (WCAG 2.2, 2023; the logotype text is unchanged since 2.0, 2008).
- **Applies when.** Any check of a mark's contrast.
- **Consequence for the house rule.** The exemption is not a free pass for a ground the designer picks. Where the site's own designer chooses the ground (as in every round), the 3:1 check of 3.1 is what keeps the placement out of the "author choice" case.
- **Manta check.** Every Manta placement has some part of the mark at ≥ 3:1 to its ground: the fill on ink (4.91), the keyline on white and sand (5.90, 5.47). So Manta passes without the exemption. Its nav lockup is a link on ink, where the fill clears 3:1, so limit 2 is met.
- **Source.** W3C, Understanding SC 1.4.3 Contrast (Minimum) and Understanding SC 1.4.11 Non-text Contrast, WCAG 2.2 (w3.org/WAI/WCAG22/Understanding, read 14 Oct 2026). **P.**

## Part 4. How a client's existing logo colours meet a new palette (ledger L2)

### 4.1 What the sources do

| Approach | Who does it | What it says |
|---|---|---|
| **Derive the palette from the mark's colours** | GOV.UK (2025) | "Our core brand colours are Primary blue and Accent teal"; the wordmark is drawn in them; "We lead with the Primary blue and Accent teal across all GOV.UK channels"; "Do not create new colours". **P.** |
| **Keep the brand colour exact as one role; derive the rest from it** | Material 3, Fidelity and Content schemes | "places the source color in `Scheme.primaryContainer` … adjusted for color relativity" (about ±5 tone per mode); tertiary is "the complement to the source color" (material-color-utilities `scheme_fidelity.ts`). **P**, E (2023-). |
| **Bounded hue shift for colours whose identity must survive** | Material 3 harmonization | A "Reserved color (eg. those used for semantic or brand)" is shifted toward the primary hue "while still meaningfully" keeping it "recognizable"; the code rotates hue by half the difference, at most 15° (`blend.ts` `harmonize`). A colour can be marked not to harmonize. **P.** |
| **Brand key colours feed the generator, hue may shift** | Adobe Spectrum / Leonardo | "some key colors shift the actual hue in order to keep colors bright or recognizable". **P.** |
| **Treat the logo as a separate layer** | Spotify | The green logo only on black or white; the logo colour does not become the UI's grounds. **P.** |
| **The logo's colours are fixed by its owner** | W3C Understanding 1.4.3 and 1.4.11 | The logo exemption rests on colours "mandated by corporate identity or brand guidelines". **P.** |
| **Snap house artwork onto the palette where it sits beside a token** | Manta "Artwork leeway" | Near-miss (ΔE00 < ~10) of a token the mark sits beside: snap; a decisive difference or no adjacency: keep. **F + M**, no external source. |
| **Do not replace a visual world** | impeccable `colorize.md` | "Preserve confirmed brand and semantic conventions; do not replace a visual world under the guise of colorizing it." **Pr.** |

No source found says "ignore the client's logo colours when choosing a site palette". No source found gives a numeric rule for when a palette colour clashes with a logo colour.

### 4.2 The rule: who owns the asset decides which side moves

- **Rule.**
  1. **Ask first whether the logo's colours are fixed.** A client's logo is the client's asset; its colours are fixed unless the client opens them. (Opening them is a logo refresh, which is out of this ticket.)
  2. **Fixed logo colours become palette anchors.** Each logo colour either enters the palette as a token with a named job (GOV.UK, Material Fidelity), or is declared logo-only (Spotify). Either is valid. A palette that ignores them is not: it is the case the founder rejected in mmm-infra round 1.
  3. **Build the other colours by relation to the anchors, in OKLCH.** Neutrals and dark grounds take the anchor's hue at low chroma (Radix gray pairing; #123 tint rule). Any extra hue is a figure with one job (Part 1.3), never a second field of equal weight.
  4. **Check every palette colour against every logo colour** by Part 2: identical, or ΔE00 ≥ ~10; two meanings in one view, ≥ ~15.
  5. **Only the side the house owns moves.** Where the logo is the client's and fixed, the palette snaps to it (a site grey at ΔE00 0.3 from the logo grey becomes the logo grey). Where the house owns the artwork (Manta's mark), the artwork may snap to the palette, which is Manta's leeway rule. A bounded hue shift of a fixed brand colour (Material, ≤ 15°) is for UI colours, never for the logo file.
  6. **Then run Part 3 on the logo:** its lightness band, its versions, and its grounds in the new palette.
- **Era.** T (asset ownership and perception); the OKLCH method is E (2020s).
- **Applies when.** A project has a client logo, or a brand colour the client chose.
- **Trades off against.** Freedom of direction. A fixed blue and grey narrow the palette, and a narrow palette risks "boring" (mmm-infra round 1 v5). The remedy that keeps the anchors is energy from lightness, scale, type and photographs, not from a new hue (mmm-infra `docs/research/site-look-precedent.md` §(c) reaches the same conclusion from precedent).
- **Yields to / clash.** WCAG for text and controls (an anchor that fails 4.5:1 as text gets a text-safe partner, C3). The client's ruling over the house's taste. A distinctive-asset method (fame and uniqueness, #104 W13) would also argue for keeping colours that people already link to the client; that method is not researched here.
- **Strength.** Steps 1, 2 and 6: P (W3C, GOV.UK, Spotify, Material). Step 3: P for the mechanism (Schloss & Palmer, Radix), house for its use here. Steps 4 and 5: house, with Manta's measured cases.

### 4.3 mmm-infra, measured, and how the method resolves it

Logo colours: blue `#0070C0` (L\* 46.2, OKLCH 0.536 0.150 250°), grey `#404040` (L\* 27.1, neutral). Blue against grey: ΔE00 28.4, 2.01:1, so blue text never sits on the grey.

**Round 1 (rejected).**

| Tile | What happened to the logo colours | Measured | Method verdict |
|---|---|---|---|
| v3 Inscription | Arches recoloured to `cut #2a2925`; blue dropped; field colour minium `#86230f` | `cut` is **ΔE00 7.9** from `#404040`: a near-miss of the client's own grey. Blue's nearest token is 36.0 away: an orphan. Minium (CIELAB h 41°) is a contrasting hue with no relation to either anchor. | FAIL (recolour; near-miss of a fixed colour). |
| v4 Water | Logo shown in `foam #f1f6f3` on dark; greens | Palette hues 158-190° (CIELAB); blue's nearest token 28.1 away | FAIL (recolour); FIT RISK (no relation to the anchors) |
| v5 House colours | Logo colours kept | `quiet #5c5c5c` is **ΔE00 9.6** from `#404040` | Near-miss band; check whether the two greys are separate roles side by side |

**Round 2 leaders (the founder's choice).**

- v7 slate `#223448` has OKLCH hue 252°, the logo blue's own hue (250°), at much lower lightness and chroma (L\* 21.1, C\* 14.7). It is a tonal relative of the logo blue: same hue family, decisively different (ΔE00 23.6). `mist #B8C1CB` is the same hue (251°). This is step 3 of the rule, and Schloss & Palmer's hue-similarity finding predicts the harmony the founder saw ("Love the slate and warm white pairing").
- Light grounds: the full-colour logo needs a ground at **L\* ≥ 79.7** (3:1 against the blue; the grey needs only L\* ≥ 57.4). Paper `#F7F5F0`/`#F8F6F0`: blue 4.73-4.76:1, grey 9.5-9.6:1, pass. Pad `#F4ECB0`: blue 4.28, grey 8.63, pass. Hair `#D8D4CB`: blue 3.48, pass. **Mist `#B8C1CB` (L\* 77.7): blue 2.83, fail**: no full-colour logo on mist.
- Dark grounds: **no dark ground works for the full-colour logo**. The grey would need a ground darker than black (Y < 0), and the blue needs L\* ≤ 14.4. On slate: blue 2.47, grey 1.23. So any slate band, footer or hero needs a **reversed version** (white, 12.71:1 on slate; a light element needs L\* ≥ 51.6 on slate). mmm-infra holds only the full-colour logo (`docs/brand-assets/mmm-infra-full-logo.jpg`) and a grey-only mark SVG. The logo is also the nav home link, so WCAG's "variant with sufficient contrast" limit (3.4) applies wherever the nav is dark.
- Current site colours: site text `#3F3F3F` is ΔE00 0.3 from the logo grey: the same colour, so one token (snap the site's to the logo's). Panel grey `#595959` is ΔE00 8.6 from it: in the near-miss band if the two sit side by side as separate roles.

**Resolution for mmm-infra, in order.**
1. Record in `docs/brand/brand-sheet.md` §2 what the founder ruled in round 2: the logo's blue and grey are fixed anchors, and every direction is built in or around them. Ask Mark (#10) only what is still his: whether he chose the blue on purpose or took Office's default, and whether he will accept a reversed (white) logo for dark grounds.
2. Give the anchors jobs: grey `#404040` = text ink and the arches; blue `#0070C0` = wordmark, links, at most one accent role (5.15:1 on white, 4.73 on paper; never on slate or on the grey).
3. Derive grounds and neutrals at OKLCH hue ~250° (slate, mist) or warm paper; check each against both anchors by Part 2.
4. Write the logo's ground table: full colour on grounds at L\* ≥ 79.7; reversed white on slate and any dark ground; one-colour on photographs; banned on mist and any mid ground (L\* ~15-80 for the blue).
5. In the fit gate's §2, replace "clash" with the measured test: a recolour or a near-miss (ΔE00 ~2-10) of a logo colour FAILS; a palette with no colour related to the anchors is a FIT RISK.

## Measurements: method

- Script: `.claude/tmp/brand-palette-measure.py` (session scratch, gitignored, not kept). sRGB (IEC 61966-2-1) → linear → XYZ (D65) → CIELAB; CIEDE2000 per Sharma, Wu & Dalal 2005 (kL = kC = kH = 1); OKLab per Ottosson; ΔEOK and ΔEOK2 per CSS Color 4 §20.3-20.4; WCAG 2.x contrast from relative luminance.
- Self-test: 8 of Sharma's published pairs (1, 7, 13, 17, 19, 25, 31, 34) agree to 1e-4; OKLab white = (1, 0, 0); black on white = 21:1. Mutation run: the T-term coefficient 0.17 changed to 0.18 made the self-test fail on pair 1 (2.0378 against 2.0425).
- Mark render: `.claude/tmp/bp-render.py` (scratch, as above) renders Manta's `mark-final.svg` at 800 px in headless Chromium (Playwright) on a transparent ground and measures every opaque pixel (alpha > 0.99, 185,397 px). Keyline, eyes and catchlights are included, so the mean is a little darker than a fill-only mean.
- Colour sources: Manta `docs/brand/brand-sheet.md` §3 tokens and §3/§14 claim pairs; mmm-infra `docs/brand/brand-sheet.md` §2; round tiles' CSS custom properties on branch `rounds/site-look` (`r1/craft/*.html`, `r2/craft/v1-counsels-paper.html`, `r2/craft/v7-mark-at-work.html`).
- Not measured: anything on a real screen or by eye; the look tests named in 1.1 and 1.2.
- Results: Manta in 1.2 (hue angles, ΔL\*), 2.1 (nearest pairs), 2.2 (the twelve claims), 2.3 (ΔEOK), 3.1 (mark render); mmm-infra in 4.3.

## design-project step 2: the Colour and Logo questions

Step 2 writes §2 Colour and §4 Logo and marks. The set-up session asks these in step 1's one plain message (the founder reads them; he answers for the client or says "ask the client"). Then it measures and writes, as below.

**Colour**

1. Which colours does the client use now, and where? Give the hex values from the logo, the current site and any printed material.
2. For each colour: must we keep it exactly, may we adjust it a little, or is it free to change?
3. What is each colour for? For example the brand's main colour, text, a background, a button. A colour with no job may be dropped.
4. Which colour, if any, should mean "click here"? Only one colour does that job.
5. Are there colours the client dislikes, or that belong to a rival or to a different kind of business?
6. Light pages, dark sections, or both? Which backgrounds does the client picture: white, warm paper, a strong colour, photographs?

**Logo**

7. Which logo files exist, and is there an original (vector) file? Which versions exist: full colour, white for dark backgrounds, one colour, a small icon?
8. Does the client have written rules for the logo, such as a guidelines PDF with approved backgrounds, clear space or a minimum size?
9. Did the client choose the logo's colours on purpose, or did they come from a program's standard colours?
10. If a version is missing (for example a white logo for a dark band), may we make it, or must the logo stay exactly as it is?
11. Which backgrounds must the logo sit on in the new site: a light page, a dark band or footer, a photograph, a coloured header?
12. May the site's other colours differ from the logo's, as long as they go well with them, or must the site use only the logo's colours?

**What the session then measures and writes** (no question to the founder):

- §2: each colour with its hex, its job, and its status (fixed / may adjust / free); a ΔE00 table of every colour against every other, with any pair at ~2-10 marked as a near-miss to settle; each text colour's contrast on each ground (C3).
- §4: the logo's colours and its lightness band (L\* range and mean); for each planned ground, pass or fail at 3:1 and the version to use there; the versions held and the versions missing; any ground banned.
- `fit-gate.md` §2: the fixed logo colours, the near-miss test (a recolour or a ΔE00 ~2-10 near-miss of a fixed logo colour FAILS), and the logo's ground table.

## Gaps and open questions

1. **The thresholds ~10 and ~15 have no external source.** The lower bound (~2-4 = "the same") has one (JND, print tolerance); the fact that ~4-10 is ambiguous is supported in kind (Szafir: size-dependent noticeability). The numbers 10 and 15 are house numbers from Manta's measured cases. A founder ruling is needed to adopt them. A test that could source them: show the founder pairs at ΔE00 4, 7, 10, 13, 16 beside each other at small and large size, and record where "same, by mistake" turns into "different, on purpose". Owner: map #96's spec, with this file's other house pieces.
2. **No safe lightness gap against vibration.** Albers' plates vibrate at ΔL\* ≤ 3.4; no source gives where it stops. Coral on Manta's turquoise hero needs a look test (1.2). Owner: lucmoseley/mantahostels.
3. **Manta's §3 hue arguments are HSL numbers.** The rose-coral rejection holds on other measured grounds (near-miss of coral; moves toward danger), but its stated reason does not. Owner: lucmoseley/mantahostels (out of write scope here).
4. **Manta L4 wording.** "WCAG 1.4.11 exempts logotypes; 3:1 is only an engineering proxy" should read: 1.4.3 exempts logotype text and Understanding 1.4.11 exempts logos, on the assumption that brand guidelines fix their colours; a low-contrast placement chosen by the designer is not exempt. Owner: mantahostels.
5. **Keyline colour choice** (contrast to the light grounds plus separation from the fill) has no external source; the guidelines read only use white keylines.
6. **mmm-infra** has no reversed logo, and its brand sheet §2 still says "open" after the founder's round-2 ruling. Owner: lucmoseley/mmm-infra.
7. The fit gate's word "clash" (`plugin/skills/design-project/references/fit-gate.md` §2) has no test today; Part 4.3 step 5 gives one. Owner: map #96's spec, in #103's gate-question form.

## Bound

**Read in full:** design-vault `docs/research/manta-design-migration.md` (#115); `docs/research/principle-interactions.md` (#121); impeccable 4.5.0 `reference/colorize.md`; `plugin/skills/design-project/SKILL.md` steps 1-4 and `references/fit-gate.md`; Manta `docs/brand/brand-sheet.md` §2, §3, §5, §6, §7, §8, §14, §15; mmm-infra `docs/brand/brand-sheet.md`, `docs/brand-assets/mmm-infra-mark.svg`, `r2/README.md` (round-2 brief, branch `rounds/site-look`); Sadoughi, AIC 2024 (PDF); Sharma, Wu & Dalal 2005 (PDF: abstract, implementation notes, discontinuity section); W3C Understanding 1.4.3 and 1.4.11 (logo passages); CSS Color 4 §14.2.1 and §20 (text extracted); material-color-utilities `concepts/contrast_for_accessibility.md`, `concepts/scheme_generation.md`, `blend.ts harmonize`, `scheme_fidelity.ts` header; material-components-android `docs/theming/Color.md` (role tables, harmonization); GOV.UK brand "Logo elements" and "GOV.UK blue"; Spotify design guidelines; CSU Chico and Aramco logo pages.

**Sampled:** `docs/research/text-presentation.md` (#123: summary, Part A, B1, B6, D; cited, not redone); `docs/research/past-design-rejections.md` row B4 and Part B; `docs/research/mmm-infra-site-look-round.md` (S1, S2); `docs/research/design-coverage-gaps.md` (not opened beyond #115's summary of it); impeccable `new-work.md:63-72`, grep of all `reference/*.md`; mmm-infra `PRODUCT.md` (grep), `docs/research/site-look-precedent.md` (grep for palette and the two colours), round-1 critic reports critic-v3 and critic-v4 (the cited lines), tile CSS (custom properties only), issue #8 (last four comments); Chevreul 1854 translation (archive.org text, §8, §16-§19 and the Introduction); Apple HIG Color (JSON, searched passages); Radix Colors "Understanding the scale" and "Composing a palette"; Carbon Color overview; Spectrum Color system; Szafir VIS 2017 slides (PDF) and TVCG abstract (through search); Schloss & Palmer 2011 and Livingstone & Hubel 1987 (PubMed abstracts); Yu, Chung & Myers TAGA 2015 (abstract page); ChromaChecker "Realistic ΔE values".

**Through search summaries only (not opened):** NHS England logo page (fetch empty); Mastercard Brand Center (403); Williams, *Non-Designer's Design Book* ch. 5 (O'Reilly 403); Tufte, *Visual Explanations* ch. 4; Livingstone, *Vision and Art* (Harvard Gazette, 17 May 2002); Luo et al. 2023 CAM16-UCS test; Stone, Szafir & Setlur 2014.

**Could not open:** Albers, *Interaction of Color* (book; chapter titles from catalogues, content via Sadoughi); Ou & Luo 2006 harmony model; CIE 142-2001 (only the CIE abstract page, which gives no scope); Slack brand center ("under construction"); m3.material.io pages (not tried; Google's code and Android docs used instead).

**Not done:** no look tests on a screen; no read of claude.ai chat history.

## Later research (#178)

A deeper search, `docs/research/de00-thresholds.md`, overtakes Part 2's "no source gives the upper number" and Gaps item 1. The two-meanings line has a published floor of ΔE00 10 (Brychtová & Çöltekin 2016), and no source sets 15. For the near-miss line, four independent proxies land near ΔE00 10, but none measures it directly. Read that file before using Part 2's numbers.

## Founder ruling on the two lines (#178)

On 14 Oct 2026 the founder ruled on the figures from `docs/research/de00-thresholds.md`:
- **Two meanings in one view:** at least ΔE00 10 for large areas, and at least 20 for small marks (dots, thin lines, small text). In both cases a label or icon also carries the meaning. This replaces 15.
- **Near-miss, for colours that differ in hue or strength:** ΔE00 10 stands. It is now backed by four independent proxies, though no source measures a near-miss directly.
- **Near-miss, for two greys (lightness only):** set by the founder's look test under #178, because the sources contradict each other here.

## The grey near-miss line (#178)

The look test of greys was withdrawn: the founder had no basis to judge it, and grey-specific research settled the line instead (`docs/research/de00-greys.md`). For two greys (lightness only), where they sit against the ground decides the line:
- **Greys far from the ground** (text, a logo, icons, small marks, or areas that do not touch): a near-miss is below ΔE00 10, the same as for hues. No design system found ships two text greys on purpose below 9.6.
- **Large greys near the ground that share an edge** (page, panel, card, layer): a near-miss is below ΔE00 3. Every design system with documented pairs layers such surfaces at ΔE00 0.6-4, so 10 does not apply to them.

For mmm-infra, all three greys in the table above are dark greys on paper, so the first line applies: `#2a2925` (7.9), `#595959` (8.6) and `#5c5c5c` (9.6) are near-misses of `#404040`.
