# Research: ledger job typeface-traits (ticket #282)

Date: 16 Oct 2026.

Job question: How do body size, minimum size, weight, line height and tracking follow the x-height, width, weight and optical size of the face? When does a variable font pay?

Rows (22): TYF-13, TYF-15, TYF-19, TYF-51, TYF-52, TYF-53, TYF-54, TYS-7, TYS-8, TYS-10, TYS-11, TYS-13, TYS-39, TYS-40, TYS-41, TYS-42, TYS-46, TYS-63, TYS-64, TYS-65, TYS-66, NEW2-15.

Key to strength: P = standard, peer-reviewed or measured. D = design system or type maker document. E = expert writing.
Key to check result: CONFIRMED = the quote is on the page today. DIFFERS = the page says a different thing (the entry tells how). UNREACHABLE = I could not open the page.

## Part 1. Source re-checks

### R1. Apple HIG Typography (D)
- URL: https://developer.apple.com/design/human-interface-guidelines/typography, read through its JSON (developer.apple.com/tutorials/data/design/human-interface-guidelines/typography.json). Read 16 Oct 2026. Page change log: last entry 16 Dec 2025 ("Added emphasized weights to the Dynamic Type style specifications"); earlier entries 7 Mar 2025, 10 Jun 2024, 12 Sep 2023, 21 Jun 2023.
- "avoid Ultralight, Thin, and Light font weights, which can be difficult to see, especially when text is small." CONFIRMED.
- "If you use a custom font with a thin weight, aim for larger than the recommended sizes to increase legibility." CONFIRMED.
- "Follow the recommended default and minimum text sizes for each platform — for both custom and system fonts". Table: iOS/iPadOS 17 pt default / 11 pt minimum; macOS 13/10; tvOS 29/23; visionOS 17/12; watchOS 16/12. CONFIRMED.
- "In a running app, the system font dynamically adjusts tracking at every point size." CONFIRMED.
- "dynamic optical sizes ... merge discrete optical sizes (like Text and Display) and weights into a single continuous design". CONFIRMED.
- "when you display text in wide columns or long passages, more space between lines (loose leading) can make it easier for people to keep their place"; "If you need to display three or more lines of text, avoid tight leading even in areas where height is limited." CONFIRMED.
- Tracking tables, iOS (1/1000 em), size in pt. CONFIRMED against the notes (S1), with these exact values:
  - SF Pro: 6 +41, 8 +26, 10 +12, 11 +6, 12 0, 13 −6, 14 −11, 16 −20, 17 −26, 20 −23, 24 +3, 28 +14, 32 +13, 40 +10, 48 +8, 56 +6, 64 +4, 72 +2, 80 0.
  - SF Pro Rounded: 6 +87, 11 +52, 12 +46, 14 +35, 16 +26, 17 +22, 24 +15, 32 +12, 48 +8, 72 +2, 80 0.
  - New York (serif, no display switch in the curve): 6 +40, 11 +11, 12 +6, 14 +2, 16 −2, 17 −4, 20 −10, 24 −11, 32 −13, 48 −14, 72 −16, 96 −16.
- Reading: all three faces take positive tracking at small size. The curve shape is the face's own. SF Pro turns back to positive at 24 pt, where its Display design starts.

### R2. Material 3 type scale tokens (D)
- URL: https://raw.githubusercontent.com/material-components/material-components-android/master/lib/java/com/google/android/material/typography/res/values/tokens.xml. Read 16 Oct 2026. File last changed 6 Mar 2026 (commit "[Tokens] Upgraded to 34.0.0").
- Values (size sp / line height sp / letterSpacing em). CONFIRMED against the notes (S2):
  - Display Large 57/64/−0.00439 (lh 1.12). Display Medium 45/52/0 (1.16). Display Small 36/44/0 (1.22).
  - Headline Large 32/40/0 (1.25). Headline Medium 28/36/0 (1.29). Headline Small 24/32/0 (1.33).
  - Title Large 22/28/0 (1.27). Title Medium 16/24/+0.0094 (medium weight). Title Small 14/20/+0.0071 (medium).
  - Body Large 16/24/+0.03125 (1.5). Body Medium 14/20/+0.0179 (1.43). Body Small 12/16/+0.0333 (1.33).
  - Label Large 14/20/+0.0071 (medium). Label Medium 12/16/+0.0417 (medium). Label Small 11/16/+0.0455 (medium, 1.45).
- Small correction to S2: Body Small line height ratio is 1.33, not given in S2. Headline line heights rise from 1.25 at 32 sp to 1.33 at 24 sp, so the ratio falls as size grows.
- Material 3 tracking is NOT monotonic with size: Body Large 16 sp (+0.031) is looser than Body Medium 14 sp (+0.018). Role and weight change the value as well as size. Roboto is the face.

### R3. IBM Carbon type sets: the maker curve for IBM Plex (D)
- URL: https://github.com/carbon-design-system/carbon/blob/main/packages/type/src/styles.ts and scale.ts (raw files). Read 16 Oct 2026. styles.ts last changed 30 Jul 2026 (commit "fix: improve tree shaking ..."); the package moved to TypeScript 1 Jun 2026. Carbon sets IBM Plex; IBM makes both, so these tokens are the maker's own curve for Plex.
- Not in the notes before. New source. Values (size px, line height, letter-spacing px → em, weight):
  - 12 px (caption-01, label-01, helper-text-01, code-01, legal-01): lh 1.333, +0.32 px = **+0.0267 em**, regular.
  - 14 px (body-short-01, body-long-01, label-02, heading-01): lh 1.286 (short) / 1.429 (long), +0.16 px = **+0.0114 em**. code-02 (14 px mono): +0.32 px = +0.0229 em.
  - 16 px (body-short-02, body-long-02, heading-02): lh 1.375 (short) / 1.5 (long), **0 em**.
  - 20–42 px (productive headings 03–06, expressive headings): 0 em; lh 1.4 at 20 px, 1.286 at 28, 1.25 at 32, 1.199 at 42 (light weight at 42+).
  - Display (light weight): display-03 at 60 px −0.64 px = **−0.0107 em**, at 84 px −0.96 px = **−0.0114 em**; display-04 at 92 px −0.64 px = −0.0070 em, 122 px −0.0052 em, 156 px −0.96 px = −0.0062 em. Display lh falls from 1.19 at 42 px to 1.05 at 156 px.
- Reading: the Plex curve has the same direction as Apple and Material: positive under 16 px, zero at 16–48 px, slightly negative at display. Carbon also ties line height to role: "long" body (paragraphs) takes 1.43–1.5, "short" body (one or two lines in UI) takes 1.29–1.375 at the same size.
- Carbon type sets page (https://carbondesignsystem.com/elements/typography/type-sets/) carries the productive (14 px base, dense product UI) and expressive (16 px base) sets. The notes (adopt-or-build.md:37, read 13 Oct 2026) quote it; I confirm the 14/16 base values in the source above.

### R4. Inter (rsms): v3 dynamic metrics and Inter 4 (D, the maker)
- v3 URL: https://d.rsms.me/inter-website/v3/dynmetrics/ (archived v3 site). Read 16 Oct 2026. Quote: "tracking = a + b × e(c × z)", "a = -0.0223", "b = 0.185", "c = -0.1745", "z = font size". "You simply provide the optical font size". CONFIRMED (formula and constants as in S9). The page gives no line-height formula in its text.
- Evaluation of the v3 formula (em; mine): 11 px +0.004, 12 px +0.000 (−0.0000), 14 px −0.007, 16 px −0.011, 24 px −0.019, 32 px −0.022, 48 px −0.022, 57 px −0.022.
- Inter 4.0 release: https://github.com/rsms/inter/releases/tag/v4.0, published 20 Nov 2023. Quote: "Six additional "Display" designs, assigned to an `opsz` variable-font axis, exposed as a second family "Inter Display" as static fonts." CONFIRMED the S9 "from knowledge" claim. v4.1 published 16 Nov 2024.
- rsms.me/inter (read 16 Oct 2026, first 100k characters): "Optical size ranges from "text" to "display""; "The smaller "text" optical-size designs features a tall x-height to aid in legibility of lower-case text"; "The larger "display" optical-size designs offers clean lines, smooth curves and delicate details". I found no tracking table or dynamic-metrics text for Inter 4 in the part I read. So for Inter 4 the maker's tracking advice is now the `opsz` axis itself; the v3 formula is for Inter 3.
- Measured from the Google Fonts file Inter[opsz,wght].ttf (see R5): `opsz` 14–32, default 14; `wght` 100–900.

### R5. Font metrics, measured today (P: a measurement anyone can rerun)
- Method: my script docs/data/typeface-metrics-2026-10-16.py reads OS/2 sxHeight, sCapHeight, usWeightClass, the mean advance width of a–z (hmtx through cmap), and fvar axes. Fonts: google/fonts main branch (downloaded 16 Oct 2026) and the Windows 11 fonts in C:\Windows\Fonts on this machine. Values are at the default instance, in em.

| Face | x-height | cap | a–z mean advance | axes |
|---|---|---|---|---|
| Verdana | 0.545 | 0.727 | 0.562 | – |
| Tahoma | 0.545 | 0.727 | 0.489 | – |
| JetBrains Mono | 0.550 | 0.730 | 0.600 | wght 100–800 |
| Inter 4 | 0.546 | 0.728 | 0.536 | opsz 14–32, wght 100–900 |
| Noto Sans | 0.536 | 0.714 | 0.530 | wght, wdth 62.5–100 |
| Open Sans | 0.535 | 0.714 | 0.522 | wght, wdth 75–100 |
| Roboto | 0.528 | 0.711 | 0.499 | wght, wdth 75–100 |
| Fira Code | 0.525 | 0.687 | 0.600 | wght 300–700, **default 300** |
| Arial | 0.519 | 0.716 | 0.490 | – |
| IBM Plex Sans | 0.516 | 0.698 | 0.505 | wght 100–700, wdth 75–100 |
| IBM Plex Mono | 0.516 | 0.698 | 0.600 | – |
| Roboto Flex | 0.514 | 0.711 | 0.495 | opsz 8–144, GRAD −200–150, wdth 25–151, wght 100–1000, and parametric axes |
| Lato | 0.506 | 0.717 | 0.493 | – |
| Segoe UI | 0.500 | 0.700 | 0.493 | – |
| Consolas | 0.490 | 0.638 | 0.550 | – |
| Georgia | 0.481 | 0.693 | 0.499 | – |
| Source Serif 4 | 0.475 | 0.670 | 0.510 | opsz 8–60, wght 200–900 |
| Calibri | 0.464 | 0.632 | 0.456 | – |
| Times New Roman | 0.447 | 0.662 | 0.459 | – |
| Courier New | 0.423 | 0.571 | 0.600 | – |

- Helvetica was not on this machine; Arial copies its metrics.
- Spread of common body faces: 0.447 (Times) to 0.550 (JetBrains Mono). The ratio 0.52 / x-height runs from 0.95 (Verdana, Inter) to 1.16 (Times). Courier New (0.423) gives 1.23.
- A trap the script found: Fira Code's variable file has default `wght` 300. A page that loads it with no `font-weight` gets Light text. Same trap as Nunito Sans (default 200) in text-presentation.md B5.3.

### R6. MDN `font-size-adjust` (P-level reference)
- URL: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-size-adjust. Read 16 Oct 2026. Page last modified 16 Sep 2026.
- "Legibility of fonts, especially at small font sizes, is determined more by the size of lowercase letters than by the size of uppercase letters." CONFIRMED (notes-coverage.md:334).
- "Baseline 2024 ... Newly available ... Since July 2024, this feature works across the latest devices and browser versions." CONFIRMED.
- `from-font`: "Uses the <number> value for the specified <font-metric> from the first available font." `ex-height`: "Uses the ratio of x-height ... to font size (aspect value) to adjust the font size. This keyword value is used to normalize lowercase letters across fonts." CONFIRMED.
- Example on the page: Verdana first, Times fallback, `font-size-adjust: 0.545` keeps Verdana's aspect in Times. The 0.545 agrees with my measurement of Verdana (R5).

### R7. MDN Variable fonts guide (P-level reference)
- URL: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fonts/Variable_fonts. Read 16 Oct 2026. Page last modified 27 Feb 2026.
- Size: "That file would be larger than a single font, but in most cases smaller or about the same size as the 4 you might load for body copy." CONFIRMED (the four-file comparison is the guide's own threshold).
- "The five currently registered axes are weight, width, slant, italic, and optical size." CONFIRMED.
- "wherever possible, the appropriate property should be used, with the lower-level syntax of font-variation-settings only being used to set values or axes not available otherwise." CONFIRMED.
- Optical size: "Optical size values are generally intended to be automatically applied corresponding to font-size"; "In most cases you would want to match the font-size ... with the opsz value (which is how optical sizing is intended to be applied when using auto)." CONFIRMED.
- Grade: "'grade' refers to the relative weight or density of the typeface design, but differs from traditional 'weight' in that the physical space the text occupies does not change ... it can be varied or animated without causing a reflow of the text itself." Grade is a custom axis ("Grade may become one of the more common custom axes"). CONFIRMED.
- Width: "`wdth` ... typically set in CSS using the font-stretch property ... far more likely that the range would fall closer to the 100% mark, such as 75%-125%." CONFIRMED. The guide gives NO advice on which width suits which role.

### R8. MDN `font-optical-sizing` (P-level reference)
- URL: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-optical-sizing. Read 16 Oct 2026. Last modified 17 Sep 2026.
- "Optical sizing is enabled by default for fonts that have an optical size variation axis." "small text sizes are often rendered with thicker strokes and larger serifs, whereas larger text is often rendered more delicately". "It's been available across browsers since March 2020." CONFIRMED (text-presentation.md:228).
- DIFFERS in location only: the note says the `font` shorthand resets `font-optical-sizing` "(MDN)". The font-optical-sizing page does not say it. The MDN `font` shorthand page does (last modified 17 Sep 2026): "the shorthand resets the following properties to their initial values", and the list includes `font-optical-sizing`, `font-size-adjust` and `font-variation-settings`. So the claim is CONFIRMED on the `font` page. Consequence for a builder: a later `font:` shorthand also resets `font-size-adjust` and any `GRAD` set in `font-variation-settings`.

### R9. MDN `font-variation-settings` (P-level reference)
- URL: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variation-settings. Read 16 Oct 2026. Last modified 10 Sep 2026. Baseline widely available since September 2018.
- Registered axes table: wght → font-weight, wdth → font-stretch, slnt → font-style oblique, ital → font-style italic, opsz → font-optical-sizing. "Custom axes can be anything the font designer wants to vary". "custom axes should be given upper-case tags". CONFIRMED.
- "This property is a low-level mechanism designed to set variable font features where no other way to enable or access those features exist. You should only use it when no basic properties exist". CONFIRMED. So GRAD (custom) can only be set here; wght, wdth, opsz go through their own properties.

### R10. CSS Fonts 4 §8.1 `font-optical-sizing` (P, W3C)
- URL: https://www.w3.org/TR/css-fonts-4/. Read 16 Oct 2026. Status: "W3C Working Draft, 13 September 2026".
- "User agents are expected to supply a value for the "opsz" axis which is close to the used value for font-size." "Experiments have shown, however, that disregarding these other ancillary factors and using only font-size might be the best way". "User agents must not synthesize optical sizing when it is not performed by the font directly." "This can be accomplished by clamping a chosen value to the range supported by the font." "font-optical-sizing interacts with font-size-adjust. When applying optical sizing, User agents must apply an optical sizing value appropriate for the adjusted font size". CONFIRMED (S4). So opsz follows CSS px, and is clamped to the face's range (Inter 14–32, Source Serif 4 8–60, Roboto Flex 8–144, R5).

### R11. USWDS (U.S. Web Design System): typography guidance, normalization and tokens (D, a public-sector standard)
- Pages: https://designsystem.digital.gov/components/typography/ (curl, read 16 Oct 2026; "Latest updates" newest entry 2024-03-20; header shows v3.14.0), https://designsystem.digital.gov/design-tokens/typesetting/overview/ (newest update entry 2024-05-15), .../line-height/, .../letterspacing/. Source: github.com/uswds/uswds develop, packages/uswds-core/src/styles (tokens/font/typefaces.scss last changed 9 Mar 2022; functions read 16 Oct 2026).
- Body size: "For most text, including body copy, use at least an effective size of 16px (font-size 5). Smaller and larger text can be used sparingly for special purposes (like headings, captions, photo credits, footnotes, data tables, or specialized UI elements)." "Use tokens smaller than font-size 5 more sparingly — for shorter companion text". CONFIRMED. Note "effective size": 16 px after normalization.
- Normalization, method (CONFIRMED from source, and it DIFFERS from what the notes imply): USWDS scales each face by its **cap height**, not its x-height. `normalize-type-scale($cap-height, $scale)` = 362 px × scale / cap-height. Each typeface token carries a measured `cap-height` (system 362, Georgia 346, Helvetica Neue 357, Tahoma 363, Verdana 364, Open Sans 357, Merriweather 371, Roboto Mono 380, Source Sans Pro 340, Public Sans 362). The page says: "Each supported typeface is normalized to a target value determined by the optical size of common system fonts ... specifically Apple's typeface San Francisco and Google's typeface Roboto." Size multipliers on the page: Georgia 1.05, Helvetica 1.01, Merriweather 0.98, Open Sans 1.01, Public Sans 1.0, Roboto Mono 0.95, Source Sans Pro 1.06, Tahoma 1.0, Verdana 0.99. So USWDS also lets a face go UNDER the nominal size (Verdana 0.99, Roboto Mono 0.95): the effective 16 px may render at 15.2 px in Roboto Mono. Compare: an x-height match would give Georgia 0.52/0.481 = 1.08 and Verdana 0.95; USWDS's cap-height match is milder (Georgia 1.05, Verdana 0.99).
- Normalization and line height (TYS-11): "Since we use normalization on font sizing, we must also normalize line height to hit the target line height". Source: `lh(face, token)` = target ÷ (362 / cap-height), rounded to 0.1. Effect: the PIXEL line height stays the same across faces (table: line-height 3 at size 10 gives 32.4 px for every face; Georgia 1.29, Verdana 1.36, Roboto Mono 1.42). CONFIRMED.
- Line-height tokens: page values 1, 1.15, 1.35, 1.5, 1.62, 1.75 with uses: "1 ... buttons, navigation, and text not meant to break over a line"; "2 ... headings, introductory (lead or dek) text"; "3 ... short text (under 1 paragraph), captions, text with a very short or very long measure"; "4 ... short (1-2 paragraphs) of running text, especially with a short measure"; "5 ... a good choice for most reading text, especially text meant for extended reading"; "6 ... pullquotes". DIFFERS slightly: the shipped sass token 2 is **1.2**, not 1.15 (tokens/font/line-height.scss: 1, 1.2, 1.35, 1.5, 1.62, 1.75).
- Line height guidance (components page): "Longer texts require more line height. Headings and other content elements no longer than a line or two can have a line height between 1 (line-height 1) and 1.35 (line-height 3). Longer texts should have a line height of at least 1.5 (line-height 4). Longer lines usually require more line height." Measure: "Most lines of text should be 45–90 characters ... A good target for long texts is 66 characters"; "text with more space between lines can have somewhat longer line length." CONFIRMED.
- Letterspacing guidance: "Typically, letterspacing is defined by the type designer and shouldn't be modified." "Consider using letterspacing 1 when using font size micro or font size 1." "Headings of font-size 9+ could use letterspacing -1. Headings of font-size 12+ could use letterspacing -2. Headings of font-size 17+ could use letterspacing -3." "Text set in uppercase or small caps should use looser letterspacing." CONFIRMED.
- Token values (source type-scale.scss and letterspacing page): font-size micro 10 px, 1 = 12, 5 = 16, 9 = 22, 12 = 32, 17 = 64 px. Letterspacing 1 = +0.025 em, −1 = −0.01 em, −2 = −0.02 em, −3 = −0.03 em, 2 = +0.1 em, 3 = +0.15 em.
- So USWDS gives a **face-independent default tracking curve**: 10–12 px +0.025 em; 13–21 px 0; 22–31 px −0.01 em; 32–63 px −0.02 em; 64 px and up −0.03 em. It is for faces whose maker gives no curve; the page itself says the designer's spacing comes first.

### R12. Butterick, Practical Typography (E)
- Read 16 Oct 2026 (WebFetch; bold-or-italic by curl). Pages have no visible date; the site is a living book (2nd ed.). Use for T directions only.
- point-size.html: "In print, the optimal point size for body text is 10–12 point." "On the web, the optimal size is 15–25 pixels." "different fonts set at the same point size won't necessarily appear the same on the page." "As you reduce point size, also reduce line spacing and line length." CONFIRMED. The page does not mention x-height.
- line-spacing.html: "For most text, the optimal line spacing is between 120% and 145% of the point size." "fonts that run small will need less line spacing, and vice versa." "Use the line-height property, preferably without units." CONFIRMED. The second quote is NEW to the notes and is a direct x-height → leading rule: a face that looks small at its point size (small x-height) needs less leading; a face that looks large needs more. The page does NOT discuss line length (the notes say "leading set by line length" in vault.leading's source line; that is not on this page — DIFFERS for that attribution).
- letterspacing.html: "Use 5–12% extra space with caps, but not with lowercase"; "Lowercase letters don't ordinarily need letterspacing." "Fonts intended for body text have spacing optimized for body-text point sizes (approximately 9–13 point)." "typographers will often add letterspacing to lowercase text smaller than 9 point"; "typographers will often remove letterspacing from lowercase text used at larger sizes (e.g., headlines)." CONFIRMED. No rule on weight or width.
- bold-or-italic.html: "Some fonts have styles that are heavier than bold, like black or ultra. These weights are usually intended for large sizes (for instance, headlines) and don't work well at body text sizes." Also: semibold is "a little easier to read" than bold. NEW; gives the UPPER weight limit at body size (TYF-13).

### R13. Bringhurst via Rutter, The Elements of Typographic Style Applied to the Web (E, quoting a standard craft text)
- https://webtypography.net/2.1.7, read 16 Oct 2026 (curl). Title: "Don't letterspace the lower case without a reason". Quote (Bringhurst): "The reason for not letterspacing lower case is that it hampers legibility. But there are some lowercase alphabets to which this principle doesn't apply. Moderate letterspacing can make a face such as lowercase Univers bold condensed more legible rather than less." Rutter: "only some faces actually benefit from the treatment"; his example sets a bold condensed heading at `letter-spacing: 0.1em`. CONFIRMED. This is the only source found that ties tracking to WEIGHT and WIDTH (TYS-66): heavy, condensed lowercase can take moderate positive tracking; regular-width lowercase takes none.
- https://webtypography.net/2.1.6: caps and small caps "5% to 10% of the type size"; long digit strings also. CONFIRMED.
- https://webtypography.net/2.2.1, "Choose a basic leading that suits the typeface, text and measure". Rutter: "Text on the web almost always benefits from an increase in line height, and figures upwards of 1.3 are common (this page has a line-height of 1.5 for example)." "Negative leading ... can be used on short pieces of text provided care is taken to ensure ascenders and descenders do not collide" (example line-height 0.85 at 1.5em). CONFIRMED. The rule TITLE names the typeface as an input; the page quotes no Bringhurst text on HOW the face changes leading (his book's list — dark faces, large x-height, vertical stress need more — is not on this page; I did not re-read it, so I do not use it).
- https://webtypography.net/2.1.2: 45–75 "for a single-column page set in a serifed text face in a text size", 66 ideal; "On average one character takes up 0.5 em". CONFIRMED. The 0.5 em is a width input: my measured a–z mean advance runs 0.456 (Calibri) to 0.562 (Verdana) (R5), so the same box width gives a measure that differs by 23% between faces.

### R14. Material Design 3, Typography page: Applying type, Customizing type styles, Editorial treatments (D)
- URL: https://m3.material.io/styles/typography (tabs). The page is script-rendered; I read its content JSON at https://m3.material.io/_dsm/content/m3/2026-10-13_06-10-19/f6a1d89a-1bbf-46d1-a177-f13b074897a5.json (the file the site loads). Read 16 Oct 2026. `updatedTimestamp` 2026-08-28; the page's own update list has an "Aug 2026" entry (language script height).
- Ensuring readability, line height: "For larger type legibility using styles like title, headline, and display, we recommend a line height ratio of 1.2 times the type size". "For smaller body copy using styles like body and label, we recommend a line height ratio around 1.5 times the type size. If your line height is too tight, you'll undermine the flow of the text. Too loose, and the lines won't feel cohesive." NEW to the notes (TYS-39, TYS-42).
- Line length: "For longer body text, the recommended line length is between 40 to 60 characters. For shorter lines of text, the ideal length is 20 to 40 characters." CONFIRMED (S3 quoted 40–60 second-hand through Google Fonts Knowledge).
- Language height: "Material's type scale can adapt line height automatically based on language script height category: small, medium, large, and extra large." "Ignoring language height can lead to overlapping text". (Script is an input to line height; out of this job's face-trait scope but noted.)
- Customizing type styles (TYS-66): "Adjust properties like line height and letter spacing to refine the appearance. Avoid changing the type size". "**Heavier fonts may require wider letter spacing, while fonts with long ascenders and descenders will require different line heights.**" CONFIRMED that this is the only Material sentence on tracking by weight. No number given.
- Letter spacing units: "(Tracking value in px / font size in sp) = letter spacing"; example ".2 tracking / 16sp font size = 0.0125 em".
- Brand and plain typefaces: "The brand typeface is used for larger type styles, like Headline and Display, to focus on expression. The plain typeface is used for smaller type styles, like Body and Label, to focus on readability." Body: "Avoid expressive or decorative fonts for body text because these can be harder to read at small sizes."
- Editorial treatments, Weight (TYF-13): "Be careful when using very light weight for body text. Lower-resolution displays can struggle to show thin typography, especially at small sizes. Instead, consider lighter weights at larger font sizes, such as display type." And: "Excessive weight at smaller sizes can make text harder to read" (caption under a bold navigation-bar label example). CONFIRMED; the second is NEW and gives the upper bound.
- Editorial treatments, Grade (TYF-52, TYF-54): "Both weight and grade axes affect a letter's thickness, but adjustments with grade are much more granular and don't change any letter widths or line breaks." "Roboto Flex offers a positive grade of 150 and a negative grade of 200". "When switching between dark and light mode, the same text may appear heavier despite having the same settings. Consider using a negative grade to counteract this." "Grade can change the emphasis without reflowing text" (selected filter chips). CONFIRMED. No grade VALUE is given for dark mode on this page.
- Editorial treatments, Width (NEW2-15): "A narrow width allows more characters to fit per line while a wider width may offer more personality." "A thinner width can allow for more characters to fit at small sizes, such as in a label" (bottom navigation labels). "Since wider styles take up more space, avoid using them for areas with limited space, such as in a top app bar". CONFIRMED.
- Editorial treatments, Optical size (TYF-15, TYF-53): "Small size designs focus on enhancing readability, while large size designs can show off the intricacies of the letter forms". "Use an optical size that matches your type size". "Don't use large optical type sizes at small sizes. Instead use a smaller optical size, if available." Display: "If available, set the appropriate optical size to your usage." CONFIRMED.
- Scope limit, stated on the page: "editorial treatments shouldn't be used in labels or just to give information." So Material's width and grade advice is for showcase text; the label-width line is the one functional use it gives.

### R15. Material Design blog, "Adjusting Grade for Mode" / readability-research (D, an in-house experiment)
- URL: https://m3.material.io/blog/readability-research, read through https://m3.material.io/page-data/Posts/5915993901367296.json. Read 16 Oct 2026 in full. published_date 2022-05-11. Authors: Michael Gilbert, Julia Feldman, Brenton Simpson, Sedeeq Al-khazraji (Material Design UX research).
- Method: two-word phrases (Dale-Chall words), read, remember, retype; "We launched the experiment with 184 users"; repeated-measures ANOVA with Bonferroni. Face: Roboto Flex grade axis (graph from −200 to 150). Text size: not stated in the text.
- Findings (CONFIRMED, quote): "we didn't find any impact of grade on readability for dark mode"; "for the contexts we tested, we'd suggest that design can select a value of grade they feel is most appealing". In light mode "higher values of grade result in text that is more readable"; "if you're considering adopting the minimum value of grade (i.e., -200 ...), you should be sensitive to the fact that this may have an adverse impact on the readability". "if you're using the default value of grade (0), our results suggest there is not a significant difference in readability between light and dark mode. So, in the context we tested, there is no need to modify grade between light and dark modes to achieve equivalent readability."
- DIFFERS from what the notes imply in one point: the blog's graph text says "readability in dark mode (the blue line, on top) appears to be consistently higher than readability in light mode". The CHI 2023 paper by an overlapping team (S7, second-hand) says light mode is read faster.
- Limits: two-word phrases, not paragraphs (the blog says so); one face; no size condition. So it says nothing about small vs large text; the house's "small text keeps its weight" size split is NOT from this study.

### R16. web.dev, "Introduction to variable fonts on the web" (D/E, Google)
- URL: https://web.dev/articles/variable-fonts. Read 16 Oct 2026. "Last updated 2018-02-19 UTC." So it is NOT a 2023+ source.
- "Storing 48 individual fonts in a single variable font file meant a 88% reduction in file size." "if you are using a single font such as Roboto Regular and nothing else, you might not see a net gain in font size if you were to switch to a variable font with many axes." "animating the font between settings may cause performance issues." "A Grade axis ... changes the weight of the font without changing the widths, so line breaks do not change." CONFIRMED (notes-coverage.md:134).

### R17. web.dev Learn CSS, Typography (D)
- URL: https://web.dev/learn/css/typography (curl). Read 16 Oct 2026. "Last updated 2021-11-23 UTC." Variable fonts: "fonts that can contain many different variants of a typeface in one file". line-height: "it's recommended to use a number instead of a length or percentage". No rule on when a variable font pays. CONFIRMED; adds nothing for this job.

### R18. Argyle, web.dev "Adapting typography to user preferences with CSS" (E, Chrome DevRel)
- URL: https://web.dev/articles/adapting-typography-to-user-preferences-with-css (curl). Read 16 Oct 2026. "Last updated 2023-07-27 UTC." CONFIRMED date.
- Code: default `--base-weight: 400; --base-grade: 0`; `prefers-contrast: more` → weight 700; `prefers-contrast: less` → weight 200; `prefers-color-scheme: dark` → `--base-grade: -25`. "Now the perceptual differences of light on dark vs dark on light have been accounted for." Face: Roboto Flex. CONFIRMED (−25).

### R19. Argyle, nerdy.dev "Using CSS to fix the irradiation illusion" (E)
- URL: https://nerdy.dev/adjust-perceived-typepace-weight-for-dark-mode-without-layout-shift (curl). Read 16 Oct 2026. Dated November 29, 2025 (datetime 2025-11-29). CONFIRMED date.
- "The light text appears thicker than the dark text counterpart, even though the font weight is the same." "when in dark mode, using a negative value for GRAD to reduce the perceived thickness." Code: dark → `--GRAD: -50`; dark + contrast more → 150; dark + contrast less → −150. Also: GRAD fixes "bold link hovers" layout shift. CONFIRMED (−50). A reader comment adds that some OS and browser stacks render light-on-dark glyphs thicker (not only an illusion); comment, not used.
- So the "−25 to −50" range is two demo values by one author on one face (Roboto Flex). No measurement stands behind the number. Strength E.

### R20. HTTP Archive Web Almanac, Fonts chapters 2024 and 2025 (P: a crawl measurement)
- 2024: https://almanac.httparchive.org/en/2024/fonts. Read 16 Oct 2026. Published 2024/11/11, updated 2025/01/02; Bram Stein and Charles Berret. Variable fonts on 33% desktop / 34% mobile pages (28/29% in 2022). Axes in variable files: wght 99%, slnt ~4–5%, wdth ~2–3%, opsz ~2–3%, GRAD ~0.5%. Quote: "variable fonts can also be a performance improvement if you use multiple styles from the same family. Internally variable fonts do not store outlines for each style, but a more efficient set of deltas and offsets, so a variable font can be many times smaller than their corresponding "static" styles." On opsz/wdth/slnt set through font-variation-settings: "While there are standard CSS properties for each of these axes, people are either not aware of how to use them or are following old out-dated advice." It gives no byte comparison of a variable file against its statics.
- 2025: https://almanac.httparchive.org/en/2025/fonts. Read 16 Oct 2026. Published 2026/01/15, updated 2026/02/10; Charles Berret. "39.4% of desktop websites and 41.3% of mobile websites used at least one variable font". "most people use variable fonts basically to have multiple weights in one file". "FILL and opsz (optical size) each appear on roughly 35-39% of variable font pages, while GRAD follows at about 27%. These correspond to the Material Symbols icon font ... So, a large portion of variable font usage is actually due to icons ... not for text." Median font file 35–36 KB; 90th percentile 115–116 KB, partly "full-featured variable fonts with many axes".
- So the 2024 Almanac's "many times smaller" is a general claim; the 2025 chapter says many-axis variable files sit in the heavy tail. Neither gives a break-even count.

### R21. Byte break-even, measured today (P: rerunnable)
- Method: Google Fonts CSS2 API with a Chrome 130 user agent, latin subset only, each unique woff2 URL downloaded once (the browser fetches a shared URL once). 16 Oct 2026. Command in this session's shell; the API serves a static instance for one weight and the variable file once two or more weights of a variable family are asked for.

| Request | Unique latin files | Bytes |
|---|---|---|
| Inter 400 | 1 | 23,664 |
| Inter 700 | 1 | 24,356 |
| Inter 400+700 (API serves variable) | 1 | 48,256 |
| Inter wght 100–900 | 1 | 48,256 |
| Inter opsz 14–32 + wght | 1 | 72,920 |
| Roboto Flex 400 | 1 | 14,184 |
| Roboto Flex wght 400+700 | 1 | 34,320 |
| Roboto Flex opsz + wght | 1 | 84,304 |
| Source Serif 4 400 | 1 | 20,088 |
| Source Serif 4 wght 400+700 | 1 | 50,936 |
| Source Serif 4 opsz 8–60 + wght | 1 | 122,360 |

- Reading: a weight-only variable file costs about 2.0 (Inter) to 2.5 (Source Serif 4, Roboto Flex) static weights. Adding `opsz` costs 1.5× (Inter) to 2.4× (Source Serif 4) more. So for bytes alone: 1 weight → static wins by ~2×; 2 weights → about equal (Inter) or static wins (Source Serif 4, Roboto Flex); 3 or more weights → variable wins. The `opsz` file pays only when the page uses the face at both text and display sizes (it replaces a second family such as Inter Display) — the byte cost is real (+25–70 KB latin).
- Limits: three families, latin subset, Google's own subsetting. Self-hosted full files differ. Italic not measured.

### R22. Google Fonts Knowledge (D/E, Google; written by type designers)
- Source text: github.com/google/fonts, `cc-by-sa/knowledge/modules/.../content.md` (the text behind fonts.google.com/knowledge). Read 16 Oct 2026 in full for the lessons below. Last commit per lesson: x-height 17 Nov 2022; line height 28 Mar 2022; tracking 28 Mar 2022; optical sizes 28 Apr 2022; width 1 Apr 2022; weights/grades 2 Jul 2022; typographic size 27 Aug 2024; readability 8 Apr 2025; vertical spacing 31 Mar 2023. So only "typographic size" and "readability" carry a 2023+ date.
- exploring_x_height_the_em_square: "X-height is an important factor in readability because, at any given font size, it determines how large or small the typeface actually looks. Put simply: When the x-height is large, the typeface will probably be easier to read at small sizes." "As x-heights become taller, white space is redistributed from outside the letters to inside letters ... it's usually a good idea to increase the line height." "Long ascenders and descenders ... don't contribute to the overall perceived size—although they do require more generous line height settings." CONFIRMED (S3).
- choosing_a_suitable_line_height: "between 115% and 150% is where the optimum value sits ... for type set in a Latin script. Languages that use plentiful diacritics will usually need more generous leading." "line height is affected by the x-height". "The smaller the type, the more generous we should be with our line height values." "for display type, a line height smaller than the type size will usually look better. Consider 72px type with a line height of between 90% and 100%." "as our measure grows wider, so too should our line height become more open". "A value such as 150% for wide viewports might instead be 130% at mobile sizes." "There's no secret formula". CONFIRMED (S3).
- track_carefully_or_not_at_all: rules "1. Add a more open ... tracking value to all-caps or small caps type, especially at smaller (i.e., body) sizes. 2. Never track too widely. 3. Display sizes often benefit from a little negative tracking and very small text often benefits from positive tracking." Wichary: "Letter spacing gets tighter much faster than the font size gets bigger" (his example: −30 at 50 px, −60 at 500 px, units not stated). "it's advisable to disable ligatures if we're applying a more open tracking." CONFIRMED (S3). No numbers per size.
- choosing_typefaces_that_have_optical_sizes: "small (body or caption) optical sizes tend to have less stroke contrast, larger x-heights, wider characters, and more open spacing. Their large (or display) counterparts have refined features and tighter spacing". NEW to the notes: "any time we add an Optical Size axis, the font file-size will typically double, although this depends on the family and the other axes used–it can range between 1.2× and 2.6×." My measurement (R21): 1.51× (Inter), 2.40× (Source Serif 4), 2.46× (Roboto Flex) — inside the range. TV: "use a body optical size for your type". CONFIRMED.
- exploring_width_in_type: "Try combining an extra condensed width for playful headings, a normal width for body text, and a wide width for small pull quotes." "Headings with very few words can be set in a wide variant and headings with lots of words in an extra condensed variant." "Bold fonts are typically designed to be somewhat wider than light fonts"; uniwidth faces change weight "without causing the text to reflow". CONFIRMED; the role suggestions are NEW to the notes (NEW2-15).
- exploring_typefaces_with_multiple_weights_or_grades: "Avoid using semibold for emphasis in regular text. Use bold or extrabold". "light type on a dark background appears to glare and its letterforms become bloated ... 'halation'"; "selecting different weights so that both versions of the type feel the same"; example "Regular weight of Lato ... Semibold weight—and yet, optically, they appear the same" (the text does not say which ground each sits on; S3's "Regular on dark ≈ Semibold on light" is read from the image — I could not check the image). "grade alters only the thickness of the stroke without changing the width of the glyph." CONFIRMED in substance; the ground assignment is UNVERIFIED (image only).
- the_complications_of_typographic_size (2024): "Verdana's x-height takes up about 55% of the font's em. But Baskerville's x-height only takes up about 40% ... To achieve a similar visual size as Verdana, Baskerville must actually be set to a larger font size." "Condensed typefaces may benefit from a slight increase in size compared to wider counterparts, and typefaces with open apertures can perform better". Advice: "Try setting font sizes according to internal font measurements like x-height". It also says doing so in CSS "would currently require access to each font's internal metadata" — DATED: `font-size-adjust: from-font` (Baseline July 2024, R6) now reads the metric from the font. CONFIRMED otherwise.
- how_type_influences_readability (2025): "Tighter kerning and letter spacing will increase problems with crowding." "Larger text size in non-condensed formats ... is better to support glanceable reading." "Some fonts are designed to have larger letter spacing, such as Lexend." CONFIRMED.

### R23. The Typography Handbook (typographyhandbook.com) (E, uncited)
- URL: https://typographyhandbook.com/ (curl). Read 16 Oct 2026. JSON-LD `dateModified` 2026-06-26 ("Updated for 2026"). Strength E: the page cites no study for its numbers.
- #dark-mode: "Light text on a dark background appears thinner and lighter than the same text on a white background"; "increase font weight slightly in dark mode"; "typically a shift of 20–50 units on a variable font weight axis, or one step up in a fixed weight scale. This is particularly noticeable at smaller sizes and lighter weights. Body text at 300 or 350 weight may feel too thin in dark mode." Spacing: "Dark backgrounds can make text feel more compressed. Slightly increased line-height or paragraph spacing can improve readability, though this is a minor consideration compared to contrast and weight." Example `line-height: 1.6; /* vs 1.5 in light mode */`. Also: dark ground #121212–#1a1a1a, text #e0e0e0–#f0f0f0, "around 10:1".
  - DIFFERS from Material (R14), Argyle (R18, R19) and Google Fonts Knowledge (R22) on direction: they say light-on-dark looks HEAVIER and take weight or grade DOWN; the Handbook says it looks THINNER and takes weight UP. Both sides agree on one case: small, light-weight text on dark must not get thinner (the Handbook "particularly noticeable at smaller sizes and lighter weights"; text-presentation.md B4.2 via MDN font-smooth: greyscale anti-aliasing makes light-on-dark "look lighter").
  - This is the only source found for extra line height on dark (TYS-46): +0.1 (1.5 → 1.6), called "a minor consideration". E, uncited.
- #reading-measure: "Longer lines need more leading ... A rough guide: increase line-height by roughly 0.1 for every 10 characters above 65 CPL." "UI text, captions, and footnotes often work better at 35–50 CPL." NEW to the notes: the only numeric measure → leading rule found. E, uncited.
- #font-sizing: body `clamp(1rem, 1.5vw + 0.5rem, 1.25rem)`: "Body text: 1rem minimum, never exceeds 1.25rem"; "Always set a rem minimum". No x-height condition.
- #variable-fonts: "A variable font with a weight axis from 100 to 900 replaces nine separate font files with one." "For a typeface with four weights and italics, that's 8 files reduced to 1 or 2." "Variable fonts should be the default choice when a font offers them." No byte figures. This DIFFERS from the byte measurement (R21) for one or two weights.
- #opentype-features: "font-optical-sizing: auto ... Enable it on everything." (It is already the initial value, R8/R10.)
- #choosing-fonts: "Some fonts were designed to be used as large-size headings, while others were designed for small-density screens. Use fonts in their intended roles." CONFIRMED (TYF-15's cited line).
- No letter-spacing or tracking section exists on the page today (section ids read: no tracking id).

### R24. Matej Latin, Better Web Typography (E)
- 5-keys-to-accessible-web-typography (https://betterwebtype.com/5-keys-to-accessible-web-typography/, curl, read 16 Oct 2026; published 16 Jun 2019): "The recommended line height for paragraphs of text is usually between 1.3 and 1.7." "If the font you chose looks quite light and its x-height is small, then the line height will need to be closer to the lower end of that recommendation. The opposite is true if it's a heavy or optically large font." "the longer the lines of text, the larger the line height should be". "don't decide on the line height, line length, and font size independently". "Light fonts are generally very hard to read and should be avoided for paragraph text." CONFIRMED; the x-height and weight → leading direction is NEW to the notes and agrees with Butterick (R12) and Google Fonts Knowledge (R22).
- Equilateral triangle (https://css-tricks.com/equilateral-triangle-perfect-paragraph/, read 16 Oct 2026; 9 Jun 2017): "The recommended size for today's screens is 16px for mobile and from 18 to 22px for desktop. This also depends on the typeface. Some typefaces set at 16px may seem larger than others". "ideal line-height is usually between 1.3 and 1.7. So a body text set at 16px should have a line-height from 21 to 26px." "Darker text should have larger line-height." "The longer the line of text, the larger the line-height required." "Typefaces that seem larger and heavier need more line-height." CONFIRMED. Era: 2017, so T directions only.
- 8 tips (https://betterwebtype.com/8-tips-for-remarkably-better-typography/, published 2 Sep 2023): tip 1 "light text on a dark background looks heavier"; "consider using a variable font and adjusting the font weight in dark mode. Reduce it by 50. So if the font is set to bold in light mode (bold equals 700), reduce it to 650". Its example is a HEADING (bold). Tip 2: "A line height of around 140% is recommended for body text"; "Reduce the line height of headings to somewhere between 110 and 120%." Tip 4: "I recommend letter spacing up to 5%. Always, ALWAYS letter-space uppercase." CONFIRMED; dated 2023 (usable for E rows).
- 8 more tips (https://betterwebtype.com/8-more-tips-for-remarkably-better-typography/, published 23 Sep 2023): tip 1 (TYS-13): "JetBrains is obviously larger than Meta Serif (when they're set at the same size) ... I reduced the size of JetBrains Mono from 14 pixels to 12 pixels." Tip 2: "increase the line height of your text if you use inline code snippets" (boxes clash). Tip 3: huge lowercase titles: "letter-spacing has been reduced by 2%"; "The letter-spacing should be reduced by 1 to 2% maximum." CONFIRMED. So Latin's display floor is −0.02 em, half of impeccable's −0.04 em floor.

### R25. Atlassian Design System, Typography (D)
- https://atlassian.design/foundations/typography and .../typography/applying-typography (curl). Read 16 Oct 2026 (live docs; no page date shown; "as read Oct 2026"). Faces: Atlassian Sans ("Charlie" family names in the page) and Atlassian Mono.
- Body tokens: font.body.large 16/24 ("Body L is the default size for long-form content"), font.body 14/20, font.body.small 12/16 ("Body S should be used sparingly and is for secondary level content such as fine print"). Headings: xxlarge 32/36 (1.125), xlarge 28/32, large 24/28 (1.17), medium 20/24 (1.2), small 16/20 (1.25), xsmall 14/20, xxsmall 12/16.
- Minimum: "The general guidance for comfortable reading is to use a minimum font size of 16px for long-form text such as blogs. The smallest font size available in the Atlassian Design System typography tokens is 12px. Avoid using this, except for in fine print." CONFIRMED. (The ledger row TYS-8 cites "11/12 px"; today the page says 12 px is the smallest token.)
- Code (TYS-13): font.code Regular 12 px / 20 px in the code block. "Code can also appear inline following the style settings of the block of text it sits within. In this context, this token is relative to its container's font size. Assuming a container font size of 14 px (0.875 rem), this token will have a font size of 12.25 px. The line height is equal to the font size." So inline code = **0.875 em** of the surrounding text, a fixed ratio for Atlassian Sans + Atlassian Mono; the page does not say how 0.875 was chosen. CONFIRMED.

### R26. GOV.UK Design System, type scale and paragraphs (D, a public-sector standard)
- https://design-system.service.gov.uk/get-started/new-type-scale/ and /styles/paragraphs/ (curl). Read 16 Oct 2026. GOV.UK Frontend v6.0.0 (which makes the new scale the only one) was released 9 Feb 2026 (GitHub release).
- "14 — Deprecated as a scale point and removed in GOV.UK Frontend version 6.0.0 and later". "16 — Now 16px across all screen sizes". "19 — Now 19px across all screen sizes". Headings 24 and 27 on small screens now 21 px (was 18), 36 now 27 px (was 24). CONFIRMED.
- Paragraphs: "The default paragraph font size is 19px." "You can use the govuk-body-s class sparingly to make your paragraph font size 16px instead of 19px." "updated the type scale to increase the size of text on small screens, improving legibility and accessibility." CONFIRMED.
- So GOV.UK's smallest text size is now **16 px** at all widths, body 19 px. Face: GDS Transport (x-height not measured here; the font is not on this machine). The reasons are in a 12 Dec 2022 blog post I did not open.

### R27. WCAG 2.2 Understanding documents (P, W3C)
- 1.4.3 Contrast (Minimum), https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum. Read 16 Oct 2026; "Updated 06 September 2026". "Fonts with extraordinarily thin strokes or unusual features" are harder to read "especially at lower contrast levels"; "particularly thin or unusual fonts may be rendered by user agents with a much fainter color"; authors should "choose a font with stronger/thicker lines". "14 and 18 point is roughly equivalent to 1.2 and 1.5 em" and "authors would need to check this for the particular fonts in use." "14pt and 18pt are equivalent to approximately 18.5px and 24px." The page sets NO minimum font size. CONFIRMED (S5).
- 1.4.8 Visual Presentation (AAA), https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation. "Updated 06 September 2026". "Width is no more than 80 characters or glyphs (40 if CJK)." "Line spacing (leading) is at least space-and-a-half within paragraphs, and paragraph spacing is at least 1.5 times larger than the line spacing." Reason: readers with some reading or vision disabilities "have trouble keeping their place". No typeface condition. CONFIRMED.
- 1.4.12 Text Spacing (AA), https://www.w3.org/WAI/WCAG22/Understanding/text-spacing. "Updated 01 October 2025". Content must survive user settings of line height 1.5, paragraph spacing 2, letter spacing 0.12, word spacing 0.16 (× font size). "a user may need to change to a wider font family than the author has set in order to effectively read text." CONFIRMED. This is a robustness test, not an author value.

### R28. Legge and Bigelow 2011, "Does print size matter for reading?" (P, peer-reviewed review)
- Journal of Vision 11(5):8, doi:10.1167/11.5.8, PMC3428264. Abstract read through the Europe PMC REST API; full text through https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/ (WebFetch, first 100k characters). Read 16 Oct 2026.
- Abstract: "The fluent range extends over a factor of 10 in angular print size (x-height) from approximately 0.2° to 2°. Assuming a standard reading distance of 40 cm (16 inches), the corresponding physical x-heights are 1.4 mm (4 points) and 14 mm (40 points)." CONFIRMED (S7).
- Full text, NEW to the notes: "a consensus value for the critical print size for normally sighted readers is 0.2° x-height." Karow's survey of 1049 roman typefaces: "the x-height fraction ranged from 0.28 to 0.58, with a mean of 0.46"; the authors' 51 serif text fonts averaged 0.45. x-height is "a more salient determinant of perceived type size than is body size" (stated as "not proven by rigorous laboratory studies"). Tinker: fastest at "an x-height of 0.21° (1.5 mm, 11 point body)", slower at "0.19° (x-height = 1.36 mm, 10 point body)".
- My arithmetic (not in the source): the CSS reference pixel subtends about 0.0213° (CSS Values; S3). The critical print size 0.2° ÷ 0.0213 = 9.4 px of x-height at the reference distance. A 16 px face at x-height 0.52 gives 8.3 px (0.177°); at 0.447 (Times) 7.2 px (0.152°); at 0.546 (Inter) 8.7 px (0.186°). So 16 px body sits just under the critical print size for every common face at the reference distance (phones are held nearer, which helps; real pixel angles vary). Consequence: making a large-x-height face SMALLER than 16 px moves it further under the critical size; making a small-x-height face larger moves it toward the critical size. This is the evidence for a one-way (up only) scaled floor.

### R29. APCA font lookup and the 0.52 reference x-height (E, the method's own author; not a standard)
- apca-w3@0.1.9 src/apca-w3.js (unpkg), read 16 Oct 2026: line 461 "All font sizes are in px and reference font is Barlow". CONFIRMED (S6).
- Myndex/SAPC-APCA discussion #28 "Fonts & APCA reference alignment" (GitHub API; opened 8 Nov 2021; author's answer 9 Nov 2021). Quotes the then WCAG 3 draft: "Reference fonts for comparison include Helvetica Neue, Helvetica, Fira Sans, Kanit, and Arial." "Values shown are for common sans-serif fonts (e.g., Helvetica, Arial, Verdana, Calibri, Trebuchet)." "Some fonts such as Times have a smaller than usual x-height. Such fonts should be compared to the reference and adjust the needed contrast accordingly." Author: "the Helvetica would measure an x-height of about 52px" at 100 px; "If your font is smaller, you need to determine the difference percentage by dividing the reference by your font ... 52/45 = 1.1555"; "lets say for a pair of colors the APCA lookup indicates a 16px font. Multiply by 1.1556 and you get an 18.5px font." CONFIRMED (S6, rule-interactions.md:194).
- Note: the method is stated only for faces SMALLER than the reference ("If your font is smaller"). The author gives no rule for scaling down a larger face. Era: 2021, and APCA is not in WCAG 3 today (text-presentation.md B6). Use it as an E source for the reference value only.
- Is 0.52 defensible? Yes, as a reference, on three grounds: (1) Arial 0.519 and Roboto 0.528 (R5), the default sans faces of Windows/web and Android, sit on it; Helvetica (APCA's measure) ~0.52. (2) The mean of the 15 proportional body faces I measured is 0.510 (range 0.447–0.546); 0.52 is the sans-serif centre, and serif text faces run lower (Karow mean 0.46; Georgia 0.481, Times 0.447). (3) USWDS normalizes to the "optical size of common system fonts ... San Francisco and Roboto" (R11), the same family of faces. The 16 px floor in the sources (USWDS, GOV.UK, Atlassian; Butterick's 15–25 px) was set with these default sans faces in view, so 0.52 is the x-height at which the 16 px floor was calibrated. Strength of the 0.52 itself: E (one author) supported by my measurement (P).

### R30. Refactoring UI (E)
- "7 Practical Tips for Cheating at Design", Adam Wathan and Steve Schoger, Medium, published 20 Feb 2018. Medium returned 403; read through the Wayback Machine copy (web.archive.org, 2024 snapshot) on 16 Oct 2026. Tip 1: "two font weights is usually enough for UI work: A normal font weight (400 or 500 depending on the font) for most text; A heavier font weight (600 or 700) for text you want to emphasize. Stay away from font weights under 400 for UI work; they can work for large headings but are too hard to read at smaller sizes. If you're considering using a lighter weight to de-emphasize some text, use a lighter color or smaller font size instead." CONFIRMED (text-presentation.md B5.3).
- Preview "Line-height is proportional" (https://www.refactoringui.com/previews/line-height-is-proportional, curl, 16 Oct 2026; from the 2018 book): "narrow content can use a shorter line-height like 1.5, but wide content might need a line-height as tall as 2." "for large headline text you might not need any extra line spacing, and a line-height of 1 is perfectly fine. Line-height and font size are inversely proportional". CONFIRMED (ledger TYS-40, TYS-42 incidence).

### R31. Smaller sources sampled
- MDN "Colors and Luminance" (https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Colors_and_Luminance; last modified 8 Oct 2026): "some fonts are so thin or fancy that they present accessibility problems on their own"; "'Normal' print is usually considered 11.5pt to 12pt, equivalent to 16px on screen. While smaller font may be legible — a user can make out letters at ~70% accuracy — that is not readable. A 16px font size is generally readable for people with normal vision. Someone with 20/40 needs twice that, about a 31px font." "Thin letters will be harder to read than thick ones". No x-height, no dark-ground text. CONFIRMED (TYF-13 incidence MD; TYS-7 incidence MD).
- Adham Dannaway, "UI design tips" (https://www.adhamdannaway.com/blog/ui-design/ui-design-tips, curl, 16 Oct 2026; no date read): tip 11 "Look for typefaces with taller lower case letters and greater letter spacing, as they're generally more legible at small sizes" (League Spartan → Inter). Tip 16 "ensure that line height is at least 1.5 (150%). Keeping line height between 1.5 and 2 generally works well." CONFIRMED (TYF-19, TYS-39 incidence PU). E.

### R32. Tracking by size: the maker curves side by side (computed from R1–R4, R11)
Values in em. SF Pro and New York: Apple iOS table, pt taken as CSS px, linear between table rows. M3: the token of the role nearest that size (Roboto). Carbon: IBM Plex tokens. Inter v3: the dynamic-metrics formula. USWDS: its face-independent guidance.

| px | SF Pro | New York | M3 (Roboto) | Carbon (Plex) | Inter v3 | USWDS default |
|---|---|---|---|---|---|---|
| 11 | +0.006 | +0.011 | +0.046 (Label S) | – | +0.005 | +0.025 |
| 12 | 0.000 | +0.006 | +0.033 (Body S); +0.042 (Label M) | +0.027 | 0.000 | +0.025 |
| 14 | −0.011 | +0.002 | +0.018 (Body M) | +0.011 | −0.006 | 0 |
| 16 | −0.020 | −0.002 | +0.031 (Body L); +0.009 (Title M) | 0 | −0.011 | 0 |
| 24 | +0.003 | −0.011 | 0 (Headline S) | 0 | −0.019 | −0.010 |
| 32 | +0.013 | −0.013 | 0 (Headline L) | 0 | −0.022 | −0.020 |
| 48 | +0.008 | −0.014 | 0 (Display M at 45) | 0 (display −0.011 at 60) | −0.022 | −0.020 |
| 57 | +0.006 | −0.015 | −0.004 (Display L) | −0.011 (60 px) | −0.022 | −0.020 |

- Agreement: every curve is looser at 11–12 px than at 16 px (direction T). Every curve at display size is between −0.022 and +0.013 em, so impeccable's −0.04 em floor is never reached by any maker (agrees with house-audit-method.md:71).
- Disagreement: at 16 px the curves span −0.020 (SF Pro) to +0.031 (Roboto Body L), a 0.05 em spread. So a tracking value at text sizes is a property of the FACE (and the role), not of the size alone.
- Optical size: SF Pro's curve turns positive from 24 pt, where its Display design takes over (Apple: dynamic optical sizes merge "Text and Display"). New York (one design) keeps tightening. So a face whose `opsz` axis or display cut is active needs no negative tracking at display sizes; a single-design face takes the negative tail.


### R33. Late additions (read Oct 2026)
- Palmén, Gilbert, Crossland, CHI 2023 (published 19 Apr 2023), Roboto Flex grade x mode, 459 participants. I read the abstract first-hand (Semantic Scholar). The full PDF was blocked. Findings: light mode was read reliably faster than dark mode. In light mode, heavier grades gave a reading benefit. Designers can change grade without a loss of reading fluency. This is the later and larger study by the same team as R15. Where R15 says dark mode read better, CHI 2023 supersedes it.
- Butterick, "Line length" page: 45–90 characters. It does not say that line height must follow measure. So the vault.leading source line ("leading set by line length") is not Butterick's. The claim comes from impeccable.
- impeccable 4.5.0 `reference/typeset.md`, read today: "Tune line height inversely with measure: wider lines generally need more leading." The two halves of this sentence disagree ("inversely" means wider lines get LESS). The intended rule is "wider lines get more". The same file has: "Compensate light text on dark surfaces on all three perceptual axes: slightly more line height, a touch more tracking, and one step more weight when the face needs it." It gives no source. This is the origin of TYS-46 and of the "extra line height and tracking" clause in vault.dark-text-weight.
- impeccable `harden.md` and the `undersized-ui-text` check: not read (see Bound).

## Part 2. Row verdicts

Key for each row: Decision. Rule (inputs, output). Conditions and clashes. Era. Sources (strength). Verdict.
Symbols: xh = the face's x-height in em (OS/2 sxHeight / unitsPerEm, measured as in R5). adv = mean a–z advance in em. CPL = characters per line.

### TYS-7. Body text size
- Decision: the size of running body text on a web surface.
- Rule: inputs xh of the body face, role (running text or dense working role). Output: running text body_px = max(16, ceil(16 × 0.52 / xh)). Dense working role (tables, tool panels): 14 px × 0.52 / xh, rounded up, never under the TYS-8 floor. Scale UP only. Never scale down below 16 px for a face with a large x-height.
- Worked values: Source Serif 4 (0.475) → 17.5 → 18 px. Georgia (0.481) → 17.3 → 18 px. Times (0.447) → 18.6 → 19 px. Inter (0.546), Verdana (0.545) → 16 px.
- Clash: USWDS (R11) normalizes by cap height and scales DOWN too (Merriweather and Roboto Mono get smaller). I reject the down step for running text with the R28 argument. USWDS uses cap height; I use x-height because reading speed follows x-height (R28, APCA R29).
- Clash: house vault.body-size says "all text at phone widths 16 px or more". No source supports this for labels and captions (see TYS-8).
- Era: principle T (R28, R12). The 16 px base is current: GOV.UK v6.0.0 (9 Feb 2026) body 19, smallest 16; Atlassian body 16 (as read Oct 2026); MDN and USWDS "effective size of 16px" (as read Oct 2026). Label E for the 16 px value.
- Sources: Legge and Bigelow 2011 (P); USWDS (D); Butterick 15–25 px (E); Carbon productive/expressive (D); Atlassian (D); GOV.UK (D); M3 Body M 14 / Body L 16 (D); APCA 0.52 reference (E).
- Verdict: COVERABLE. The 0.52 reference and the up-only clamp are my derivation from P and E sources; state them as such.

### TYS-8. Minimum text size
- Decision: the smallest size any text may take.
- Rule: inputs xh, role. Output: fine print, captions and form helper text: 12 px × 0.52 / xh, rounded up. Short labels of 1–3 words (tab labels, badges): 11 px × 0.52 / xh, with positive tracking from the maker curve or USWDS +0.025 em. No running text under the TYS-7 value.
- Conditions: thin and light weights need a larger floor (Apple HIG: thin weights only "larger than the recommended sizes", R1). A public-service surface follows GOV.UK: 16 px smallest (R26).
- Clash: house vault.body-size "all phone text 16 px". Apple (iOS 11 pt min, 17 default), M3 (Label S 11, Body S 12) and Atlassian (12 px fine print) all allow 11–12 px for short or secondary text on phones. Only GOV.UK asks for 16 px. The founder must choose: (a) GOV.UK floor for every phone text, or (b) the platform floors above.
- Era: E. Apple change log 16 Dec 2025; M3 tokens 6 Mar 2026; Atlassian and GOV.UK 2026.
- Sources: Apple HIG (D); M3 tokens (D); Atlassian (D); GOV.UK (D); WCAG 1.4.3 Understanding has no minimum size (P, R27).
- Verdict: COVERABLE, with one house decision flagged (phone floor).

### TYS-10. Size retuned per face
- Decision: whether the size tokens change when the face changes.
- Rule: inputs xh of each face in the stack (primary and fallbacks). Output: compute every size token from xh as in TYS-7 and TYS-8. For fallback faces, set `font-size-adjust: from-font` on the primary, so a fallback renders at the primary's x-height. If the primary has no xh in OS/2, measure the "x" glyph.
- Conditions: `font-size-adjust` is Baseline since July 2024 (R6). The `font` shorthand resets it (R8), so set it after any `font` shorthand. Too large an adjust can clip diacritics (CSS Fonts, R10).
- Era: E (MDN modified 16 Sep 2026; Baseline July 2024). GFK's older lesson that says CSS cannot read the font's metrics is now superseded (R22).
- Sources: MDN (D); CSS Fonts 4 WD 13 Sep 2026 (P, standard draft); USWDS normalization (D); my measurements R5 (P, rerunnable with docs/data/typeface-metrics-2026-10-16.py).
- Verdict: COVERABLE.

### TYS-11. Line height retuned per face
- Decision: whether line height changes with the face.
- Rule: inputs xh, role band from TYS-39 or TYS-42. Output: xh ≥ 0.53 → upper half of the band. xh ≤ 0.49 → lower half. Between → middle. Alternative (USWDS): keep the pixel line pitch fixed when the size is retuned, so the ratio falls as the size rises.
- Conditions: the band split is a lookup. The direction is sourced; the magnitude is my inference.
- Era: T (Butterick "fonts that run small will need less line spacing, and vice versa", R12; Latin 5-keys 2019: small x-height or light weight → lower end, R24).
- Sources: Butterick (E); Latin (E); USWDS (D).
- Verdict: COVERABLE (direction sourced, magnitude inference, say so).

### TYS-39. Body line height
- Decision: the line height of running text.
- Rule: inputs size, xh, measure (CPL). Output: base 1.5 at 65 CPL or less; band 1.4–1.6; floor 1.3; adjust per TYS-11 and TYS-40.
- Conditions: short body or UI copy of 1–2 lines may take 1.3–1.43 (Carbon short body, Atlassian 14/20, M3 Body S 1.33). WCAG 1.4.12: text must survive a user setting of 1.5 (R27). WCAG 1.4.8 (AAA) asks for at least 1.5 in paragraphs.
- Clash: the house record cites Butterick 120–145%. That band is for print-like settings. The web systems read today put body at 1.4–1.5 (M3 ~1.5, USWDS 1.5 default body, Atlassian 1.5, GOV.UK 1.32 at 19 px). The floor 1.3 stays; the base moves to 1.5.
- Era: T for the band; E for current system values (2026).
- Sources: Butterick (E); webtypography/Bringhurst ≥1.3 common (E); M3 typography 28 Aug 2026 (D); USWDS (D); Atlassian (D); WCAG 1.4.8, 1.4.12 (P).
- Verdict: COVERABLE.

### TYS-40. Line height against measure
- Decision: how line height changes with line length.
- Rule: inputs CPL. Output: +0.01 per character above 65 CPL, up to +0.1 (Handbook: +0.1 per 10 CPL above 65, R23). Under 45 CPL (phone) the line height may drop toward 1.3–1.4 (GFK, R22).
- Conditions: direction only is T. The +0.01/char figure is from one uncited source (E). Refactoring UI says 1.5 narrow up to 2 wide (R30), which agrees with the direction.
- Clash: the house record names Butterick as the source. Butterick's pages do not say this (R12, R33). Re-source to the Handbook, Refactoring UI and GFK.
- Era: E (Handbook dateModified 2026-06-26).
- Sources: Typography Handbook (E, uncited); Refactoring UI (E); GFK (D/E).
- Verdict: COVERABLE for direction; magnitude weak, state it.

### TYS-41. Size, line height and measure together
- Decision: the order in which the three are set.
- Rule: inputs xh, adv, container width. Output: (1) size from TYS-7. (2) measure: column width = CPL × size × adv (CPL target 66, band 45–75; R11, vault.measure); check the result with check-measure.py, not a `ch` width. (3) line height from TYS-39 + TYS-40 + TYS-11 for the CPL that results.
- Conditions: a wide face (adv 0.60, Verdana) needs a column about 30% wider than a narrow face (adv 0.456) for the same CPL (R5).
- Era: T (Latin triangle 2017; Butterick).
- Sources: Latin (E); USWDS 66 target (D); Baymard via vault.measure (E).
- Verdict: COVERABLE.

### TYS-42. Heading line height
- Decision: the line height of headings and display text.
- Rule: inputs size. Output: ≤ 20 px: 1.25–1.4. 24–40 px: 1.15–1.3. ≥ 48 px: 1.0–1.15. ≥ 72 px: 0.9–1.05.
- Conditions: a heading that wraps to 3 lines or more takes the upper end. Text with diacritics, or a script that is not Latin, takes more (M3 language height, R14). Never let ascenders and descenders collide.
- Era: E for the values (M3 tokens 6 Mar 2026: Display L 57/64 = 1.12, Headline L 32/40 = 1.25, Title M 16/24 = 1.5; Carbon 30 Jul 2026 display 1.17–1.19 down to ~1.05; Latin 2023 headings 110–120%). Direction T.
- Sources: M3 (D); Carbon (D); Latin (E); Refactoring UI headlines 1 (E); USWDS heading lh 1.2 token (D).
- Verdict: COVERABLE.

### TYS-46. Line spacing in dark mode
- Decision: whether dark mode adds line height.
- Rule found: only the Typography Handbook (+0.1, "minor", no source, R23) and impeccable typeset.md (no source, R33).
- Conditions: no design system read today (Apple, M3, Carbon, USWDS, Atlassian, GOV.UK) changes line height by mode. CHI 2023 studied grade, not line height.
- Era: none can be given (no dated sourced claim).
- Verdict: NOT COVERABLE. Recommend: drop the "extra line height and tracking" clause from vault.dark-text-weight, or mark it accepted-without-source.

### TYF-54. Weight on a dark ground
- Decision: whether light-on-dark text changes weight or grade.
- Rule: inputs size, weight, mode. Output: below WCAG large-text size (24 px regular, 18.66 px bold): keep the light-mode weight; never below 400. At or above that size: may reduce by GRAD −25 to −50, or wght −50, as a look choice, not a reading need.
- Conditions: the size threshold is my mapping from WCAG's large-text sizes (R27); no study gives a size split. CHI 2023 found that grade can change without a fluency loss and that heavier grades helped in light mode (R33). The 2022 blog found no reading need to change grade (R15). Argyle (2023, 2025) and Latin (2023) reduce weight on dark for the look of irradiation (R18, R19, R24). The Handbook says the opposite: +20–50 wght on dark (R23). The research shows neither direction helps reading; so the choice is look, and a small text keeps its weight.
- Clash: house vault.dark-text-weight says "small text keeps weight, large may go one step lighter". This agrees.
- Era: E (CHI Apr 2023; Argyle Jul 2023 and Nov 2025; Latin Sep 2023; M3 typography 28 Aug 2026).
- Sources: CHI 2023 abstract (P, read first-hand; full text not read); M3 grade blog 2022 (D, in-house test); M3 typography (D); Argyle (E); Latin (E); Handbook (E, contrary).
- Verdict: COVERABLE.

### TYF-13. Weight limits at small sizes
- Decision: which weights are allowed at small sizes.
- Rule: inputs size, weight, the face's default instance weight. Output: at body size and below: wght ≥ 400 (≥ 300 only for a face whose 300 is drawn as a text weight, and only at ≥ 18 px). At ≤ 14 px: wght ≤ 700. Black and ultra (800–900): display sizes only. Thin weights (100–200): only at sizes larger than the platform's recommended size.
- Conditions: a variable font's default instance may not be 400 (Fira Code's default is 300, R5). Set wght explicitly.
- Era: T (Apple HIG; Butterick; Refactoring UI 2018; M3 "light body bad, excessive weight at small sizes bad").
- Sources: Apple HIG (D); M3 typography (D); Butterick (E); Refactoring UI (E); WCAG 1.4.3 Understanding on thin fonts (P).
- Verdict: COVERABLE.

### TYF-15 and TYF-53. Display cut versus text cut; optical size automatic
- Decision: when to use a display cut or the opsz axis.
- Rule: inputs the face's opsz range or its named cuts, the used size. Output: if the face has an opsz axis, leave `font-optical-sizing: auto` (the default); do not set opsz by hand. If the face has static Text and Display cuts, use the maker's stated switch size (SF: 20 pt text to display, merged as dynamic sizes; Inter 4 opsz 14–32). With no maker figure, use the Text cut below 20 px and the Display cut at 32 px and above.
- Conditions: TV and far viewing take the body (text) optical size even at large px, because the angle is small. The `font` shorthand resets `font-optical-sizing` (R8). An opsz-active display face needs no negative tracking (R32).
- Era: E (Inter 4.0 Nov 2023; Web Almanac 2024 calls manual opsz outdated advice; MDN 17 Sep 2026; CSS Fonts 4 13 Sep 2026).
- Sources: CSS Fonts 4 §8.1 (P); MDN (D); Apple HIG (D); Inter release notes (E, maker); Web Almanac (P).
- Verdict: COVERABLE.

### TYF-52. Custom axes directly
- Decision: when to use `font-variation-settings`.
- Rule: inputs the axis tag. Output: use the high-level property for registered axes (wght → font-weight, wdth → font-stretch, opsz → font-optical-sizing, ital/slnt → font-style). Use `font-variation-settings` only for GRAD and custom axes. Drive each axis value from a CSS custom property, so one rule does not erase another (the property does not inherit per axis).
- Conditions: the `font` shorthand resets it (R8).
- Era: E (MDN 10 Sep 2026; CSS Fonts 4 13 Sep 2026).
- Sources: MDN (D); CSS Fonts 4 (P); web.dev (D, 2018).
- Verdict: COVERABLE.

### TYF-51. Variable or static font
- Decision: load a variable font or static files.
- Rule: inputs the number of weights/styles used, the axes needed. Output: 1–2 styles and no axis use → static. 3 or more weights, an intermediate weight, or GRAD/wdth use → variable wght. Add opsz only if the page uses both text and display sizes of the same face.
- Measured (R21): a wght variable file equals about 2 static weights (Inter 48,256 vs 23,664 + 24,356). Adding opsz costs ×1.5–2.4 more. GFK says opsz adds 1.2–2.6× (R22).
- Era: E (Web Almanac 2024, 2025; my measurement Oct 2026).
- Sources: my measurement (P, rerunnable); Web Almanac (P); GFK (D/E).
- Verdict: COVERABLE.

### TYF-19. Large x-height for small text
- Decision: whether small and dense text needs a large x-height face.
- Rule: inputs xh, role. Output: in dense roles (tables, labels, UI) prefer xh ≥ 0.52. A face with a smaller xh is allowed if its size is scaled by TYS-7/TYS-8. Avoid xh above ~0.56 where diacritics or mixed scripts are common.
- Conditions: the scaled floor compensates a small x-height, so this is a preference, not a ban. Too large an x-height crowds accents (CSS Fonts on font-size-adjust, R10).
- Era: T (Legge and Bigelow; Karow mean 0.46, R28).
- Sources: Legge and Bigelow (P); GFK (D/E); CSS Fonts (P).
- Verdict: COVERABLE.

### TYS-13. Inline code size
- Decision: the size of inline code beside body text.
- Rule: inputs xh_body, xh_code. Output: code size = body × xh_body / xh_code, in em. Or set `font-size-adjust` on the code element to the body face's aspect value. If code sits in a box with padding, raise the line height of that line or the box will push lines apart.
- Worked: Source Serif 4 (0.475) with JetBrains Mono (0.550) → 0.864 em. Latin sets JetBrains Mono at 12 px beside 14 px Meta Serif = 0.857 em (R24). Atlassian uses 0.875 em (R25).
- Era: E (Latin Sep 2023; Atlassian Oct 2026; font-size-adjust Baseline 2024).
- Sources: Latin (E); Atlassian (D); MDN (D); my measurements (P).
- Verdict: COVERABLE (was a gap).

### TYS-63, TYS-64, TYS-65, TYS-66. Tracking (one record)
- Decision: letter-spacing by size, case, weight and width.
- Rule: inputs size, the face's maker curve (if any), opsz active or not, case, weight, width. Output, in order: (1) use the maker's tracking table (Apple, M3, Carbon, Inter) if the face has one. (2) Else the USWDS default curve: ≤ 12 px +0.025 em; 13–21 px 0; 22–31 −0.01; 32–63 −0.02; ≥ 64 −0.03. (3) All caps and small caps: +0.05 to +0.10 em. (4) Short labels: the upper end of step 2. (5) opsz active or a Display cut in use: 0 at display sizes, no negative tail. (6) Weight ≥ 700 or a condensed width: no negative tail; a small positive value may be added (direction only, amount unsourced).
- Clash: impeccable's −0.04 em display floor (impeccable.md:86) is outside every maker curve (min −0.022, R32). Replace it with −0.03 (USWDS) as the floor.
- Conditions: at 16 px the makers spread from −0.020 to +0.031 em (R32), so a default curve is a fallback, not a truth.
- Era: E (Apple 2025, M3 2026, Carbon 2026, USWDS as read Oct 2026). TYS-66 direction T (Bringhurst via Rutter, M3 "Heavier fonts may require wider letter spacing").
- Sources: Apple, M3, Carbon, USWDS (D); Inter (E, maker); Butterick (E); Rutter/Bringhurst (E).
- Verdict: COVERABLE (TYS-66 for direction only).

### NEW2-15. Width by role
- Decision: which width (wdth) each role takes.
- Rule: inputs role, the face's wdth range, adv. Output: body: normal width (wdth 100). Labels, table cells, tight UI: narrow allowed (M3). Text read at a glance (signs, nav, alerts): no condensed. Short headings and pull quotes: wide allowed. Avoid wide in limited space.
- Conditions: a condensed face may need a slightly larger size to keep legible (GFK, R22). Measure adv per width to set column width (TYS-41).
- Era: E (M3 typography 28 Aug 2026; GFK).
- Sources: M3 (D); GFK (D/E).
- Verdict: COVERABLE.

## Part 3. Research-line dispositions (lines.txt, 26 lines)
- text-presentation.md:204 → TYF-54. impeccable's "one step heavier on dark" is superseded by CHI 2023 and M3, except as a look choice.
- text-presentation.md:228 → TYF-15, TYF-53.
- text-presentation.md:230 → TYF-52, TYF-53.
- text-presentation.md:234 → TYF-13.
- rule-interactions.md I-1 :194 → TYS-7, TYS-8, TYS-10, TYF-19.
- rule-interactions.md I-2 :195 → TYS-63–65.
- rule-interactions.md I-5 :198 → TYS-39, TYS-40, TYS-42, TYS-11.
- rule-interactions.md I-6 :199 → vault.measure, TYS-41 (adv as width input).
- rule-interactions.md I-7 :200 → TYF-15, TYF-53, TYS-63.
- rule-interactions.md I-8 :201 → TYF-54.
- rule-interactions.md I-9 :202 → TYF-13.
- rule-interactions.md I-17 :210 → NEW2-15, TYF-52.
- rule-interactions.md :272 → TYS-39 (resolved by the x-height band; "taste" not carried).
- notes-coverage :43 → TYF-13, TYF-54 (the Material study does not support a size split; the split is a WCAG mapping).
- notes-coverage :49 → TYS-39, TYS-40 ("covered" superseded: source was wrong).
- notes-coverage :137 → TYF-51.
- notes-coverage :262 → TYS-63, TYS-65.
- notes-coverage :337 → TYS-10.
- notes-coverage :344 → not carried (type "temperature" unsourced, out of scope).
- house-audit-method :65 → TYF-54, TYS-46.
- house-audit-method :71 → TYS-63, TYS-65 (confirmed by R32).
- principle-interactions :90 → TYS-7 dense role. Manta 14–15.5 px (K9) not carried: Manta fact.
- design-coverage-gaps :96 → not carried: Manta fact (impeccable 16 px part → TYS-7).
- adopt-or-build :39 → TYS-7.
- adopt-or-build :42 → TYS-40 (Butterick page lacks the measure claim).
- adopt-or-build :43 → TYS-39.

## Part 4. Suggested records
- vault.type-size: TYS-7, TYS-10, TYF-19.
- vault.type-floor: TYS-8 (house decision: phone floor).
- vault.type-weight: TYF-13, TYF-54.
- vault.type-leading: TYS-39, TYS-40, TYS-41, TYS-42, TYS-11. TYS-46 accepted-without-source or dropped.
- vault.type-tracking: TYS-63, TYS-64, TYS-65, TYS-66.
- vault.type-axes: TYF-15, TYF-51, TYF-52, TYF-53.
- vault.type-width: NEW2-15.
- vault.code-size: TYS-13.
- Changes to live records: vault.leading source (not Butterick for measure); vault.dark-text-weight (drop the unsourced line-height/tracking clause; replace the 2022 blog with CHI 2023 as lead source); vault.body-size (the phone clause needs a house decision; add x-height scaling).

## Bound
- Read in full: Apple HIG typography JSON; M3 tokens.xml, M3 typography content JSON, M3 grade blog; Carbon styles.ts; USWDS source and pages; Google Fonts Knowledge lessons named in R22; MDN pages R6–R9, R31; CSS Fonts 4 §8.1; Latin pages R24; Atlassian; GOV.UK; WCAG Understanding 1.4.3, 1.4.8, 1.4.12; typographyhandbook; Argyle pages; Butterick pages named; impeccable typeset.md (lines 40–50 read today); Web Almanac 2024 and 2025 fonts chapters (most sections).
- Sampled: Legge and Bigelow (first ~100k characters); rsms.me/inter (first ~100k); Dannaway; Refactoring UI (via Wayback); CHI 2023 (abstract only).
- Measured: x-heights and advances of 19 faces (R5) and woff2 bytes (R21), rerunnable with docs/data/typeface-metrics-2026-10-16.py over the same font files: google/fonts main and the Windows 11 fonts.
- Not reached: CHI 2023 full PDF; Bringhurst's book text on leading by face; GOV.UK 2022 blog; the Carbon type-sets HTML page (source code read instead); impeccable harden.md and the undersized-ui-text check; metrics of GDS Transport, Helvetica and SF Pro.
