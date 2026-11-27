# #183 audit: visual and page "house" values (surface styling, text tint, first-visit trust)

Status: complete (14 Oct 2026).
Question: design-vault#183. Parent spec: design-vault#154.
Scope: the house values in `plugin/skills/design-critique/references/surface-styling.md`, `plugin/skills/design-critique/references/text-presentation.md`, `docs/research/surface-styling.md`, `docs/research/text-presentation.md`, `docs/research/first-visit-trust.md`, and spec #154 §"The house method, written once".
Not in scope: the ΔE00 lines (2/10/20; greys 10/3). The founder ruled on them in #178. This audit does not research them again.

Dispositions: SOURCED, CONFLICTS, GAP (kind: curve point, taste, or business fact), NOT A DESIGN CLAIM.

## 0. Inventory (grep for "unsourced", "house", "guess", "judgement")

| # | Value | Where |
|---|---|---|
| V1 | Text tint chroma: about OKLCH C 0.01–0.05, falling toward black and white | `references/text-presentation.md:11`; #154 body (Text presentation); `docs/research/text-presentation.md:99` |
| V2 | "Pure grey is an equal choice" | `references/text-presentation.md:13-14`; #154 |
| V3 | About three elevation levels on a marketing site (marked unsourced) | `references/surface-styling.md:31`; `docs/research/surface-styling.md:96` |
| V4 | Fill step under about 1.1:1 keeps the border (marked unsourced) | `references/surface-styling.md:94`; `docs/research/surface-styling.md:212-213,318` |
| V5 | Borders and icon strokes in one line-weight band, thinner than the focus ring (marked unsourced) | `references/surface-styling.md:103`; `docs/research/surface-styling.md:259-260,327` |
| V6 | One hover signal; "the house takes Atlassian's" | `references/surface-styling.md:18-25`; #154 |
| V7 | Radius nesting: inner = max(outer − padding, small fallback) | `references/surface-styling.md:46-53,97` |
| V8 | One scrim token at about 32–60% | `references/surface-styling.md:73-80` |
| V9 | Review dates "a year after writing, a guess" (2027-10-14) | `references/surface-styling.md:5`, `references/text-presentation.md:5` |
| V10 | Form field budget 3 required + 2 optional ("a house judgement") | `docs/research/first-visit-trust.md:43,83`; #154 (First-visit trust); #144 resolution |
| V11 | Booking link (Calendly) on a senior advisor's site ("house judgement, not evidence") | `docs/research/first-visit-trust.md:41,187` |


## 1. Text tint (V1, V2)

### Measurements (shipped values, converted to OKLCH by script)

Method: I downloaded each system's shipped token file. A Python script converted each hex to OKLCH (Björn Ottosson's matrices). For Material, I ran Google's own library (`@material/material-color-utilities` 0.4.0, npm, published 21 Jan 2026) to make a `SchemeTonalSpot` scheme from eight seed colours, specs 2021 and 2025, light and dark.

| System | Text roles measured | OKLCH chroma of text greys | Toward white | Toward black |
|---|---|---|---|---|
| Tailwind v4 (`packages/tailwindcss/theme.css`, main, read 14 Oct 2026) | steps 500–950 of the 9 tinted scales | 0.004–0.046 (slate 0.041–0.046; gray 0.027–0.034; zinc, stone, mist, taupe, olive, mauve 0.004–0.034) | falls in all (50–100: 0–0.007) | falls in 7 scales; **does not fall in slate (950 = 0.042) or gray (950 = 0.028)** |
| Radix Colors 3.0.0 (`@radix-ui/colors`, light and dark files) | steps 11 (secondary text) and 12 (primary text) | light 0.008–0.016; dark step 11 0.009–0.014; pure `gray` 0 | dark step 12 = 0.003 | light step 12 = 0.008–0.013; sage rises from 0.008 (11) to 0.012 (12) |
| Material 3, Tonal Spot (the default scheme), library run | `onSurface`, `onSurfaceVariant`, `outline` | 0.010–0.030, set by the seed hue: cool hues (blue, teal, Manta ink) 0.010–0.016, warm hues (red, orange, yellow) 0.016–0.030 | `surface` 0.004–0.013 | `onSurface` (L 22) is about 0.002–0.008 lower than `onSurfaceVariant` (L 40) |
| Apple HIG Color (iOS system grays, RGB from the page's image alt text) | `systemGray` 1–6, light and dark | 0.004–0.007 at one fixed hue (286, cool), the same for every app | — | — (`label` is black, chroma 0) |
| Evil Martians, OKLCH palette (in `docs/research/text-presentation.md` B1.1, not re-fetched) | text | 0 | — | — |

### V1. Chroma band "about OKLCH C 0.01–0.05, falling toward black and white"

- **Where.** `plugin/skills/design-critique/references/text-presentation.md:11`; #154 body ("about OKLCH 0.01–0.05, less near black and white"); `docs/research/text-presentation.md:99`.
- **Founder ruling.** Yes, indirectly. #101 Q5 (A), 14 Oct 2026: "Accept recommendations", (A) on every question. Q5 (A) put "#123's text-tint rule" into the spec. The agent recommended (A) at 75%. He did not rule on the numbers 0.01–0.05; the band came from the #123 research and went into #154 with the rule.
- **Disposition: SOURCED, with two corrections.**
  - The band is the envelope of shipped systems: lowest tinted text grey 0.004 (Apple, Tailwind 950s), highest 0.046 (Tailwind `slate`). So 0.05 is the extreme of one blue-grey scale, not a typical value. Typical shipped text greys sit at 0.008–0.03 (Radix all, Material all, Tailwind `gray`, `zinc`, `stone`, `mist`, `taupe`, `olive`, `mauve`).
  - **Correction A (toward black).** "Falling toward black" is only partly true. Toward white, chroma falls in every system. Toward black, it falls in most Tailwind scales, but not in `slate` and `gray`; in Material it falls only a little; Radix `sage` rises. The rule should say "falls toward white; may stay level toward black".
  - **Correction B (upper end).** A text grey at 0.04–0.05 matches only Tailwind `slate`, a deliberate blue-grey. Material, the only system that tints toward the brand hue by code, never goes above 0.030 for text, and stays at 0.010–0.016 for cool hues. Manta's `ink` (0.051) is above every brand-hue-tinted system measured.
- **Sources.** Tailwind `theme.css`: https://raw.githubusercontent.com/tailwindlabs/tailwindcss/main/packages/tailwindcss/theme.css (e.g. `--color-slate-950: oklch(12.9% 0.042 264.695)`). Radix: https://unpkg.com/@radix-ui/colors@3.0.0/slate.css and siblings. Material: `dynamic_scheme.js` in `@material/material-color-utilities` 0.4.0: `case Variant.TONAL_SPOT: return TonalPalette.fromHueAndChroma(sourceColorHct.hue, 6.0);` (neutral, 2021) and `8.0` (neutral variant); 2025 spec: `platform === 'phone' ? 5 : 10` and `× 1.7`. Apple: https://developer.apple.com/design/human-interface-guidelines/color (image alt text "R-142,G-142,B-147" for `systemGray`).
- **Confidence.** 0.85 that the band is sourced as an envelope. It would move if a widely used system ships text greys above 0.05 (none found), or if the band is read as a target rather than a limit.

### V2. "Pure grey is an equal choice"

- **Where.** `plugin/skills/design-critique/references/text-presentation.md:13-14`; #154.
- **Founder ruling.** Same as V1 (#101 Q5 (A), agent recommendation taken). No separate ruling on "equal".
- **Disposition: SOURCED.**
  - Radix: "Radix Colors provides a pure gray and a few tinted gray scales … If you want a neutral vibe, or you want to keep things simple, gray will work well with any hue or palette. … Alternatively, choose the gray scale which is saturated with the hue closest to your accent hue. The difference is subtle" (https://www.radix-ui.com/colors/docs/palette-composition/composing-a-palette, fetched 14 Oct 2026).
  - Material ships a chroma-0 neutral in its `MONOCHROME` and `RAINBOW` variants (library code above). Tailwind ships `neutral` (chroma 0). Apple's `label` is black.
  - No readability difference: Legge and Rubin 1986 (Psychophysics of reading IV), luminance-matched grey, red, green and blue text: reading rate of normal readers was "independent of wavelength" under photopic light (abstract and search summary only; https://legge.dl8.umn.edu/sites/legge.psych.umn.edu/files/files/media/legge86_psychophysics_of_reading._iv._wavelength_effects_in_normal_and_low_vision.pdf). So the choice is taste, not function.
  - Note: "equal" is a fair reading of Radix, but the default in Material (Tonal Spot) and Tailwind (`gray`) is tinted. "Equal in function; tinted is the more common default" is the exact statement.
- **Confidence.** 0.85. It would move if a study found a preference or trust effect of tinted against neutral grey text (none found; I did not search aesthetics studies deeply).

## 2. Surface styling (V3–V9)

### Founder rulings that cover this group

- #101 Q5 (A), 14 Oct 2026: "Accept recommendations", (A) on every question. Q5 (A) put "#117's surface-styling method" into the spec. The agent recommended (A) at 75%.
- #101 Q6 (A), same reply: "icon line weight at other sizes" and "glass effects" accepted as gaps. Agent recommendation taken.
- #154, comment of 14 Oct 2026: "The founder accepted both recommendations … Q2 (A), the 22 tickets as drafted." The spec body names "one hover signal" and "radius nesting (inner = outer − padding)".
- No ruling of his names any figure in this group (three levels, 1.1:1, the line-weight band, 32–60%). #174 marked three figures "unsourced" for this audit. #174's heads-up from #178 says: "name it as unsourced rather than as a founder decision."
- The hover choice ("the house takes Atlassian's", `references/surface-styling.md:23`) is **not** a founder ruling. `docs/research/principle-interactions.md:69` says of it: "**Not decided by a source**: Atlassian and Material disagree. Founder ruling R2". R2 is a Manta ruling, still open under lucmoseley/mantahostels#3793.

### Shipped values measured (token files fetched 14 Oct 2026)

| System | Shadow or elevation tokens | Fill-only card step (contrast ratio vs page) | Border / focus width | Scrim |
|---|---|---|---|---|
| Atlassian (`@atlaskit/tokens` 20.6.0) | 3 shadows: `raised`, `overlay`, `overflow`; 4 surfaces: sunken, default, raised, overlay | `surface-sunken` #F8F8F8 on white = 1.06 (a backdrop well, not a card) | border 1 px; `border-width-selected` 2 px; `border-width-focused` 2 px | `blanket` #050C1F at 46% |
| Material 3 (androidx tokens via #117; material-web `_md-comp-focus-ring.scss`) | 6 levels (0, 1, 3, 6, 8, 12 dp) | filled card `surfaceContainerHighest` on `surface` = 1.23 (purple seed) | outline 1 dp, text-field focus 2 dp; focus ring `width: 3px`, `outward-offset: 2px` | 32% (`ScrimTokens`) |
| Carbon (`@carbon/themes` 11.83.0; `styles/scss/components/tile/_tile.scss`) | (not measured) | tile `$layer` #f4f4f4 on white = **1.10**, no border by default | border 1 px; focus 2 px | `overlay = 'rgba(0, 0, 0, 0.6)'` |
| Polaris (`@shopify/polaris-tokens` latest) | 7 levels `shadow-0`…`shadow-600` plus bevel and inset | `bg-surface` white on `bg` #f1f1f1 = 1.13, with `shadow-bevel-100` | `border-width-025` 1 px; `border-width-050` 2 px | `backdrop-bg` black at **71%** |
| Primer (`@primer/primitives` 11.10.0) | 3 resting (`xsmall`, `small`, `medium`) + 4 floating | (not measured) | (not measured) | `overlay-backdrop` #c8d1da at 40% (a **light** scrim) |
| Tailwind v4 | 7 shadows (`2xs`…`2xl`) | — | — | — |
| GOV.UK (govuk-frontend main) | none | `light-grey` #f3f2f1 on white = 1.12 | input border 2 px; focus 3 px | — |

### V3. "About three elevation levels on a marketing site" (marked unsourced)

- **Where.** `references/surface-styling.md:31`; `docs/research/surface-styling.md:96`.
- **Founder ruling.** None on the number (see above).
- **Disposition: SOURCED, as a count of roles, not of sizes.** Atlassian, the system whose rule the reference follows, ships exactly three shadow tokens (`raised`, `overlay`, `overflow`) and says "There are four basic elevation levels" (sunken, default, raised, overlay; https://atlassian.design/foundations/elevation, fetched 14 Oct 2026). The house's three (rest, hover or raised, overlay) are Atlassian's roles minus the scroll-edge `overflow` shadow. App systems ship more (Material 6, Polaris 7, Primer 7, Tailwind 7) for drag and nested overlays. No source names a count for a marketing site (search: "how many shadow elevation levels"; the results give 3 to 9, all for apps; https://cieden.com/book/sub-atomic/shadows/how-many-shadows-to-have, a practitioner guide, says three; search summary only).
- **Suggested wording.** "One level per role the page uses; a page with no drag and no nested overlays uses about three (Atlassian ships three shadows)."
- **Confidence.** 0.7. It would move if a page needs a sticky bar shadow separate from the overlay shadow (Manta has a fourth, untokenised one: `docs/research/surface-styling.md:266`).

### V4. "A fill step under about 1.1:1 keeps the border" (marked unsourced)

- **Where.** `references/surface-styling.md:94`; `docs/research/surface-styling.md:212-213,318`.
- **Founder ruling.** None.
- **Disposition: GAP, kind: a point to pick on a curve that no source has measured.** No perception study or design system states a minimum fill step for a borderless card. The shipped values bound the point:
  - The smallest fill-only card step a major system ships is Carbon's tile: `background-color: $layer` (#f4f4f4) on white = 1.10:1, no border (`_tile.scss`, `.cds--tile`). GOV.UK's grey panel is 1.12. Polaris puts a white card on 1.13 and adds a bevel shadow. Material's filled card is 1.23.
  - Carbon is adding a border to its **operable** tiles: "A border has been added to the clickable, selectable, and expandable variants of tile to visually indicate they are operable", and "these feature flags will become the default" in v12 (https://carbondesignsystem.com/components/tile/usage/, fetched 14 Oct 2026). That is a function cue, not a fill-step rule, but it shows Carbon found 1.10 alone too weak for an operable card.
 -
- **What the founder would need.** A view on which screens and light his visitors use (phone in sun against office monitor). That is a business fact, plus a pick on the curve. A cheaper close: cite "1.10, the lowest fill-only step a major system ships (Carbon)" and drop "unsourced". Manta's white card on `sand-page` is 1.08, under the line, so the rule's present effect is to keep Manta's border.
- **Confidence.** 0.6 that 1.1 is a defensible line. It would move with a measurement of edge visibility under glare (none found; I did not search display-engineering literature deeply).

### V5. "Borders and icon strokes in one line-weight band, all thinner than the focus ring" (marked unsourced)

- **Where.** `references/surface-styling.md:103`; `docs/research/surface-styling.md:259-260,327`.
- **Founder ruling.** #101 Q6 (A) accepted "icon line weight at other sizes" as a gap (agent recommendation taken). No ruling on the band.
- **Disposition: split.**
  - **"Focus ring thicker than other lines": SOURCED.** Every system measured makes the focus ring the widest line: Material ring 3 px against 1 dp outline and 2 dp focused field; GOV.UK 3 px against a 2 px input border; Carbon 2 px against 1 px; Atlassian 2 px against 1 px. One exception: Atlassian's `border-width-selected` is also 2 px, equal to its focus width. WCAG 2.4.13 (AAA) asks a focus area of at least a 2 px perimeter.
  - **"Borders and icon strokes in one band": GAP, kind: taste.** No source ties icon stroke to border width; #117 said so. Apple ties icon weight to **text** weight: "In general, match the weights of interface icons and adjacent text" (HIG Icons, via `docs/research/surface-styling.md:252`). With bold text beside an icon, Apple's rule asks a heavier icon than a 1 px border, so the band can clash with the first sentence of the same interaction. The reference already puts the text match first; the band is a secondary preference.
- **What the founder would need.** Nothing now: #101 Q6 already accepted the gap. If it returns, the pick is a taste: whether icon strokes may be heavier than borders.
- **Confidence.** 0.8 for the focus-ring part; 0.7 that the band part has no source (one search round, plus #117's).

### V6. One hover signal; "the house takes Atlassian's"

- **Where.** `references/surface-styling.md:18-25`; #154 ("one hover signal").
- **Founder ruling.** Only through #101 Q5 (A) and #154 Q2 (A), both "accept recommendations". The choice between Atlassian and Material was never put to him for the vault. For Manta it is R2, open under mantahostels#3793.
- **Disposition: GAP, kind: taste between two sourced conventions.** Atlassian: "Don't combine elevation transitions and hovered and pressed tokens for interactive states. Use one or the other." and "It should not be used for very small UI, as elevation changes are harder to see than surface color changes at this size." (https://atlassian.design/foundations/elevation, fetched 14 Oct 2026). Material 3 raises an elevated card 1→2 on hover **and** adds an 8% state layer (`ElevatedCardTokens.kt`, `StateTokens.HoverStateLayerOpacity = 0.08`, via #117). No study measures one signal against two. impeccable's detector flags one specific pair (hairline border plus wide diffuse shadow), which supports Atlassian for that pair only.
  - The "small part changes colour, never shadow" half is SOURCED (Atlassian, quote above). The "press goes down, never up" half is SOURCED (Polaris, `docs/research/surface-styling.md:102`).
- **What the founder would need.** A taste pick: calm and dense (Atlassian) or more emphatic (Material). The reference should say "the house default is Atlassian's (an agent choice, #174)" until he picks.
- **Confidence.** 0.85 that no source settles it.

### V7. Radius nesting: inner = max(outer − padding, small fallback)

- **Where.** `references/surface-styling.md:46-53,97`.
- **Founder ruling.** #154 Q2 (A) (spec names it); agent recommendation.
- **Disposition: SOURCED.** Apple WWDC25 session 356: "concentric shapes calculate their radius by subtracting padding from the parent's" (https://developer.apple.com/videos/play/wwdc2025/356/, fetched 14 Oct 2026). SwiftUI `concentric(minimum:)`: "the system calculates the corner radius to equal the container shape's corner radius minus the distance between corners. If the radius that the system calculates is less than the minimum radius you provide, the system uses the minimum radius. When the system calculates a zero radius, the corner is square." (https://developer.apple.com/documentation/swiftui/edge/corner/style/concentric(minimum:), fetched 14 Oct 2026). This is exactly max(R − p, minimum). The size of the "small fallback" is not given by Apple (it is the author's choice), so the reference is right to leave it open.
- **Confidence.** 0.95.

### V8. One scrim token, "about 32–60%"

- **Where.** `references/surface-styling.md:73-80`.
- **Founder ruling.** None on the range.
- **Disposition: SOURCED for "one token"; the range is narrow by one system.** Each system ships one product scrim: Material 32% black, Atlassian `blanket` navy at 46%, Carbon `overlay = 'rgba(0, 0, 0, 0.6)'`, Polaris `--p-color-backdrop-bg: rgba(0, 0, 0, 0.71)`, Primer `--overlay-backdrop-bgColor: #c8d1da66` (a light grey at 40%). So the shipped dark range is 32–71%, and one system uses a light scrim. The house "32–60%" leaves out Polaris. The departure is small, and the reference says "about".
- **Correction.** "about 32–70%" covers every dark scrim measured. Add that a light scrim exists (Primer) for a light, low-drama brand.
- **Confidence.** 0.85.

### V9. Review dates "a year after writing, a guess"

- **Where.** `references/surface-styling.md:5`; `references/text-presentation.md:5`; `house-principles.md:5` (uncommitted file of another session).
- **Disposition: NOT A DESIGN CLAIM.** It is a maintenance interval. It is honestly labelled a guess. No source can set it.

### V12a. Focus on a text input: "an outside 2 px ring, or a border at least 2 px thick and 3:1 different from its rest state"

- **Where.** `references/surface-styling.md:66`.
- **Disposition: SOURCED, but from an AAA criterion.** The 2 px perimeter and the 3:1 change are SC 2.4.13 Focus Appearance, level AAA (W3C Understanding 2.4.13). The reference's Clash line names only the AA floors (2.4.7, 1.4.11, 2.4.11). So the rule asks more than the legal AA floor. That is a defensible house strictness (GOV.UK does it), but the reference should say "AAA" so a reader knows it can be relaxed. No founder ruling on AAA found.
- **Confidence.** 0.9.

### V12b. Link underline: "thin and with an offset clear of descenders"; hover changes "the underline's offset or thickness"

- **Where.** `references/text-presentation.md:20`.
- **Disposition: SOURCED.** govuk-frontend `settings/_links.scss`: `$govuk-link-underline-thickness: max(1px, .0625rem)`, `$govuk-link-underline-offset: 0.1578em`, `$govuk-link-hover-underline-thickness: max(3px, .1875rem, .12em)` (main, fetched 14 Oct 2026).
- **Confidence.** 0.9.

### V12c. "A dark link beside dark body text rarely reaches 3:1"

- **Where.** `references/text-presentation.md:20`.
- **Disposition: SOURCED by measurement** (WCAG 2 contrast formula, my script). Common link colours against body text:
  - against pure black: browser default #0000EE 2.23, Google #1a0dab 1.69, Material #0B57D0 3.29, Polaris #005bd3 3.44, Tailwind blue-600 4.00, GOV.UK #1d70b8 4.06;
  - against a softened dark text (Polaris #303030): every one is 1.06–2.55, so none reaches 3:1.
 - So the default to the underline follows from the measurement and G183.
- **Confidence.** 0.9.

## 3. First-visit trust (V10, V11)

### V10. Form field budget "3 required + 2 optional" ("a house judgement")

- **Where.** `docs/research/first-visit-trust.md:43,83,104`; #154 body ("the form field budget (3 required + 2 optional), labelled a house judgement"); #176 body (open; it will write the budget into a plugin reference). An older line, `docs/research/adopt-or-build.md:182`, says "Add a field budget from Baymard (#104 W11)"; #144 later found that Baymard's figure is for checkout and does not transfer.
- **Founder ruling.** No ruling on the numbers. #101 Q2 (A) ("Accept recommendations", agent's (A)) asked for the research. #154 Q2 (A) accepted the spec's 22 tickets as drafted, which carry the budget "labelled a house judgement".
- **Disposition: split in three.**
  - **"+ 2 optional": SOURCED.** NN/g, Kathryn Whitenton, 1 May 2016: "Limit the form to only 1 or 2 optional fields, and clearly label them as optional." and "eliminate as many optional fields as possible" (https://www.nngroup.com/articles/web-form-design/, fetched 14 Oct 2026). This is a heuristic from usability practice, not a measured curve.
  - **"3 required" (name, email, message): SOURCED as a derivation, not as a number.** It is the smallest set that lets the owner reply. GOV.UK's question protocol asks a question only where "you need the information to deliver the service" (via `docs/research/first-visit-trust.md:43`; not re-fetched). The research's own rule is a test, not a count: "Each other field must name the action its answer changes before the reply." So "3" is the outcome of the test for a plain enquiry. The figure needs no house label if the reference says "the required fields are the ones the reply needs: for a plain enquiry, name, email and message".
 - **The total as a fixed budget: GAP, kind: a business fact.** No source can set a field count for a contact form, and the one peer-reviewed form study that could have tested it deliberately did not. Seckler, Heinz, Bargas-Avila, Opwis and Tuch, CHI 2014 (N = 65, eye tracking, 20 form guidelines on real company forms): "We refrained from applying guideline 3 ('Keep the form as short and simple as possible and do not ask for unnecessary input') in this study, as this would have required in-depth knowledge of the companies' business strategies and goals." (full text read: https://research.google.com/pubs/archive/42513.pdf).
  - Practitioner data stays weak and points both ways. HubSpot (Dan Zarrella, 40,000 customer landing pages, undated, updated 6 Jun 2025): "as the number of form fields increases, conversion rates decrease slightly, but not as steeply as I expected"; "there is very little decrease in conversion rate as the number of single line text fields increases"; "multiple textareas have a powerful depressing effect on conversion rates" (https://blog.hubspot.com/blog/tabid/6307/bid/6746/which-types-of-form-fields-lower-landing-page-conversions.aspx, fetched; the curve itself is an image I could not read). Marketo/MarketingExperiments: 5 fields 13.4% against 9 fields 10%, with "less qualifying data" (search summary). Aagaard: 9 → 6 fields lost 14.23% of leads (in #144, read there). Eloqua: flat to rising between 4 and 7 fields (search summary). Unbounce 2026 "3 fields 10.1% against 9 fields 3.6%" appears only in a third-party blog (digitalapplied.com); I did not find it in Unbounce's own pages, so it is unverified. All are single-vendor, correlational or single-site, and count submissions, not lead quality.
- **What the founder would need (only if a site has a form).** The business fact: which facts the owner needs before the first reply, and whether more qualified leads are worth fewer leads. That belongs to each client (mmm-infra has no form, so nothing is owed now). For the vault, the gap closes by wording, not by a pick: "required = what the reply needs (the question protocol); optional ≤ 2 (NN/g 2016)".
- **Confidence.** 0.85 that no source sets the total. It would move if a peer-reviewed field experiment on contact-form length exists; one extended search and one academic search found none.

### V11. Booking link (for example Calendly) on a senior advisor's site ("house judgement, not evidence")

- **Where.** `docs/research/first-visit-trust.md:41,187`. The research says "no source found; for a senior advisor it is a house judgement". It does not say which way the judgement goes, and the checklist (§1) leaves the booking link out. #154 and #176 do not carry it.
- **Founder ruling.** None found. Searched "Calendly", "booking link" in all three trackers: no hits on a ruling.
- **Disposition: GAP, kind: a business fact.** Evidence found is vendor-only and about software sales teams: TimeTrade (a scheduling vendor) says that its own sales team, after swapping lead forms for a booking link, got about 4× more confirmed appointments (vendor press release, search summary only); RevenueHero (a scheduling vendor) gives benchmarks with no comparison group. No source tests a booking link on an advisor's or consultant's site, and none tests whether a public calendar changes how senior a person looks. Whether a booking link fits depends on facts only the owner has: does he want strangers to take his time, does he have open time to show, and do his readers (development-bank staff, per #144) book meetings that way.
- **What the founder would need.** Nothing for the vault: the item is not in the checklist. For mmm-infra, the question goes to Mark with the other contact questions (mmm-infra#10, out of this repo's write scope). The research's phrase "house judgement" should become "no source; the owner decides".
- **Confidence.** 0.8 that no independent evidence exists (one search round; vendor results only).

## 4. Other lines labelled inference, house or guess (V12d–V12g)

### V12d. Tint "toward the main hue only, never toward an accent the page uses as a spot"; "a page with several strong hues or many photographs takes the dominant colour's hue or pure grey"

- **Where.** `references/text-presentation.md:12`; `docs/research/text-presentation.md:101`.
- **Founder ruling.** Through #101 Q5 (A) only.
- **Disposition: partly SOURCED, rest GAP (taste).** "Toward the main hue" is sourced: Material tints neutrals at `sourceColorHct.hue` (code above); Radix: "choose the gray scale which is saturated with the hue closest to your accent hue". The photograph and several-hues condition, and "a tinted grey next to a different strong hue can look dirty", are the researcher's inference: `docs/research/text-presentation.md:100` says "(my inference, no source measured it)". Radix's dark-mode caution ("Colorful UI components may clash with your saturated gray background color") supports it for grounds only.
- **Confidence.** 0.6 for the inferred part. A look test could settle it, but it is a taste, and #101 Q6 already accepted "taste for colour and busy layouts by audience" as a gap.

### V12e. "On a coloured ground, secondary text takes that ground's own hue at another lightness, never … a plain grey"

- **Where.** `references/text-presentation.md:12`; `docs/research/text-presentation.md:113`.
- **Disposition: SOURCED, but only second-hand and weak.** Refactoring UI ("7 practical tips for cheating at design", 2017) was read through a copy because Medium returned 403; impeccable `craft-floor.md:9` is an uncited plugin. The rule is a taste convention with no legibility claim (contrast is still measured).
- **Confidence.** 0.6. It would rise if the Refactoring UI original is read first-hand.

### V12f. First-visit trust: the "feel the CV" pattern, and "a date or title that differs from LinkedIn is a reason to doubt"

- **Where.** `docs/research/first-visit-trust.md:64,67`; #154 (First-visit trust).
- **Founder ruling.** #101 Q2 (A) commissioned the research; he added the fact that Mark's visitors come from LinkedIn and want to "know and feel his qualifications". No ruling on the pattern.
- **Disposition: GAP, kind: a business fact.** The research marks both as inference: "No study tests 'felt' against 'listed' credentials directly." Only Mark's readers can answer; the question "what did recent clients ask before getting in touch?" already goes to Mark on mmm-infra#10. Not a design number.
- **Confidence.** 0.7 that no study exists (from #144's search; I did not search again).


## 5. Summary

| # | Value | Disposition | Founder ruled? | Departs from research? |
|---|---|---|---|---|
| V1 | Tint chroma 0.01–0.05, falling toward black and white | SOURCED (envelope), 2 corrections | Only via #101 Q5 (A), agent's advice | **Yes, a little** |
| V2 | Pure grey an equal choice | SOURCED (Radix; Legge and Rubin 1986) | via #101 Q5 (A) | No |
| V3 | About three elevation levels | SOURCED as roles (Atlassian ships 3 shadows) | No | No |
| V4 | Fill step under 1.1:1 keeps the border | GAP, curve point (1.10 = Carbon's lowest fill-only step) | No | No |
| V5 | One line-weight band under the focus ring | Focus part SOURCED; band GAP (taste) | #101 Q6 (A) accepted the icon-weight gap | No |
| V6 | One hover signal, "the house takes Atlassian's" | GAP, taste (Atlassian against Material) | Only via #101 Q5 (A) and #154 Q2 (A) | **Yes: written as settled, research leaves it open** |
| V7 | Radius max(R − p, fallback) | SOURCED (Apple WWDC25-356; SwiftUI `concentric(minimum:)`) | via #154 Q2 (A) | No |
| V8 | One scrim, 32–60% | SOURCED; range should be about 32–70% | via #101 Q5 (A) | **Yes, a little** |
| V9 | Review dates a year on | NOT A DESIGN CLAIM | No | — |
| V10 | Field budget 3 + 2 | +2 SOURCED (NN/g 2016); 3 derived (question protocol); fixed total GAP, business fact | Only via #154 Q2 (A), agent's advice | **Yes: a fixed cap where research gives a test** |
| V11 | Booking link on an advisor's site | GAP, business fact | No | No |
| V12a | Input focus 2 px / 3:1 change | SOURCED (SC 2.4.13, AAA, not labelled AAA) | No | No |
| V12b | Link underline thin, offset; hover thickens | SOURCED (govuk-frontend) | No | No |
| V12c | Dark link rarely 3:1 against dark text | SOURCED by measurement | No | No |
| V12d | Main hue only; photos or many hues take grey | partly SOURCED; rest GAP (taste) | via #101 Q5 (A) | No |
| V12e | Coloured ground: secondary text in its own hue | SOURCED, second-hand only | No | No |
| V12f | "Feel the CV" pattern | GAP, business fact (Mark) | No | No |

### Places where a value the founder ruled on departs from research

All four rulings below are "accept recommendations" rulings (#101, #154), so each value was the agent's advice.

1. **V1, text tint band (#101 Q5 (A)).** "Falling toward black" does not hold for Tailwind `slate` (950 = 0.042) or `gray` (950 = 0.028), and Radix `sage` rises at step 12. And 0.05 is reached only by Tailwind `slate`; Material, the one system that tints toward the brand hue in code, keeps text at 0.010–0.030 (0.010–0.016 for cool hues). Research supports "about 0.01–0.03 typical, up to 0.05 for a deliberate blue-grey; falls toward white". Manta's `ink` (0.051) is above every brand-hue-tinted text colour measured. The mantahostels audit (mantahostels#3793) owns that point.
2. **V6, one hover signal (#101 Q5 (A); #154 Q2 (A)).** The reference says "The house takes Atlassian's", which reads as a decision. No source calls one signal better than two; Material combines them; the choice was never put to him.
3. **V8, scrim range (#101 Q5 (A), as part of #117's method).** 32–60% leaves out Polaris (71%), and every system ships exactly one scrim token. Small departure; widen to about 32–70%.
4. **V10, form field budget (#154 Q2 (A)).** A fixed "3 + 2" cap. Research gives a test, not a count: ask only what the reply needs (GOV.UK question protocol) and at most 1–2 optional fields (NN/g). The only peer-reviewed form study left field count out on purpose, as a business matter (Seckler et al., CHI 2014). Restate it as the test plus NN/g's optional cap, and drop "house judgement".

### Genuine gaps for the founder (and what each needs)

- **V6 (taste).** One hover signal or two, house-wide. Needs a pick between Atlassian's calm signal and Material's stronger one; a look test of the two on one card would show the difference.
- **V4 (curve point, business fact).** Only if he wants a line other than Carbon's 1.10; needs a view on his visitors' screens and light. Cheaper close: cite Carbon and keep 1.1.
- **V10 and V11 (business facts)** belong to each client (mmm-infra: Mark, mmm-infra#10), not to the vault.
- **V5 (band) and V12d (photos and many hues)** are tastes that #101 Q6 (A) already accepted as gaps; nothing new to ask.

Bound: Read in full: #183, #117, #123, #144, #174 (all with comments); #101 resolution and round 1 re-send; #103 resolution; both plugin reference files; `docs/research/surface-styling.md`; Seckler et al. 2014 (PDF text). Read in part or by grep: #154 body (house-method section and grep) and comments; #121 (grep); `docs/research/text-presentation.md` (B1.1 and grep); `docs/research/first-visit-trust.md` (grep and §§7–8, F7, bound); `docs/research/principle-interactions.md` (grep for hover); `house-principles.md` (grep; another session's uncommitted file). Shipped values measured from token files: Tailwind v4 `theme.css`; Radix Colors 3.0.0 (6 grey scales, light and dark); `@material/material-color-utilities` 0.4.0 run as code (Tonal Spot, 8 seeds, specs 2021 and 2025); Apple HIG Color (image alt text); `@atlaskit/tokens` 20.6.0; `@shopify/polaris-tokens` latest; `@primer/primitives` 11.10.0; `@carbon/themes` 11.83.0 and Carbon `_tile.scss`; material-web focus-ring tokens; govuk-frontend `settings/_links.scss`. Fetched pages (through a model's extract): Radix "composing a palette", Atlassian Elevation, WWDC25-356, SwiftUI `concentric(minimum:)` (raw), Carbon tile usage, NN/g web-form design (2016), HubSpot 40,000-page post. Search summaries only: Legge and Rubin 1986; the Marketo, Eloqua, Unbounce and Formstack field counts; TimeTrade and RevenueHero booking-link claims; the elevation-count survey. Not re-checked at source: Material's `ElevatedCardTokens` hover and `StateTokens` values, Apple's text-weight icon rule, GOV.UK question protocol, Refactoring UI (all taken from #117, #123 and #144). Not searched: display-engineering literature on edge visibility under glare (V4); aesthetics studies of tinted against neutral text (V2). Tracker searches: "tint", "hover signal", "field budget", "Calendly", "elevation", "house judgement", "pure grey", "3 required" in all three trackers; "R2 hover", "principle-interactions", "rest shadow" in mantahostels.

## Owners

Corrections V1, V3, V7, V8 and the form budget, and the fill-step citation: #194. The hover choice: #183's question to the founder. The booking link and "feel the CV": client facts for each project's set-up (#177).
