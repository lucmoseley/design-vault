# Research: the near-miss line for two greys (lightness-only ΔE00) — design-vault#178

Question: two greys in one design differ in lightness only (a\* and b\* near 0). From which CIEDE2000 (ΔE00) gap does the pair stop to look like an accidental near-copy of one token, and start to look like two greys chosen on purpose? The line for colours that differ in hue or chroma is set at ΔE00 10.

Earlier work: `docs/research/de00-thresholds.md` (F3, F5, "Conflict for lightness-only pairs"); `docs/research/brand-palette.md` (v3 `#2a2925` at 7.9, v5 `#5c5c5c` at 9.6, site `#595959` at 8.6, each against `#404040`).

Grades: **P** peer-reviewed; **S** standard; **I** industry practice; **T** tool. Measures: discrimination, harmony, intent, practice.
Figure labels: **quoted** (the source gives it), **computed** (I calculated it from the source's published values), **converted** (I changed a figure from another unit into ΔE00).
Access labels: **opened** (I read the file or text); **cited only** (I saw it only in another source or a search summary).

CIEDE2000: `lab`, `de2000` from `scripts/de00-look-test.py` (Sharma, Wu & Dalal 2005). Scripts: `.claude/tmp/de00-grey-tools/`. Downloaded files: `.claude/tmp/de00-grey-src/`.

## Findings log

### G1. Practice census: ΔE00 between greys that design systems pair on purpose — opened (package files); computed

- Grade: **I** (industry practice). Measures: **practice** (which grey pairs a design team ships to sit together, each with a stated role).
- Script: `.claude/tmp/de00-grey-tools/census.py` (output also in `census.json`). All ΔE00 values are **computed** by me from published hex values. An alpha token is composited over the ground that it sits on.
- Sources (all **opened**, downloaded from the npm registry or the vendor site on 14 Oct 2026):
  - IBM Carbon: `@carbon/colors` 11.60.0 `es/index.js`; `@carbon/themes` 11.83.0 `js/generated/themes/{white,g10,g90,g100}.js`.
  - Radix Colors: `@radix-ui/colors` 3.0.0 `gray.css`, `gray-dark.css`, `slate.css`, `sand.css`. Step roles: Radix docs (step 1 app background, 2 subtle background, 3-5 element background and its hover and active, 6-8 borders, 11-12 text).
  - Tailwind: `tailwindcss` 3.4.17 `lib/public/colors.js` (4.3.3 `theme.css` gives the same steps in OKLCH).
  - GitHub Primer: `@primer/primitives` 11.10.0 `src/tokens/base/color/{light,dark}/*.json5` and `dist/css/functional/themes/{light,dark}.css`.
  - Microsoft Fluent 2 (v9): `@fluentui/tokens` 1.0.0-alpha.24 `lib/global/colors.js`, `lib/alias/{lightColor,darkColor}.js`.
  - Atlassian: `@atlaskit/tokens` 20.6.0 `dist/esm/artifacts/themes/atlassian-{light,dark}.js`.
  - GOV.UK: `govuk-frontend` 6.5.1 `dist/govuk/settings/_colours-palette--internal.scss`, `_colours-functional.scss`.
  - Apple: HIG "Color" page JSON (`developer.apple.com/tutorials/data/design/human-interface-guidelines/color.json`), alt text of the swatches `ios-default-systemgray*.png` (for example "R-242,G-242,B-247" for Gray 6).
  - Material 3: `@material/material-color-utilities` 0.3.0, `SchemeTonalSpot` with the baseline seed `#6750A4`; script `.claude/tmp/de00-grey-tools/m3.mjs`. The neutral palette has chroma 6 (HCT), so M3 greys are slightly violet.

**Adjacent steps of each neutral ramp (ΔE00, computed):**

| Ramp | Adjacent-step ΔE00, light end → dark end | Smallest | Largest |
|---|---|---|---|
| Carbon gray 10-100 | 4.3 6.1 8.1 8.6 11.6 10.6 8.4 6.1 5.0 | 4.3 | 11.6 |
| Radix gray 1-12 (light) | 0.6 1.8 1.7 1.8 1.6 2.6 4.8 13.8 3.6 12.3 22.6 | 0.6 | 22.6 |
| Radix gray 1-12 (dark) | 2.2 2.8 2.5 2.2 2.9 4.6 8.4 5.3 5.2 18.4 13.8 | 2.2 | 18.4 |
| Tailwind neutral 50-950 | 1.0 3.4 3.9 13.0 16.9 12.2 6.1 8.4 4.7 3.0 | 1.0 | 16.9 |
| Tailwind gray 50-950 | 1.3 2.9 4.3 13.6 17.3 11.0 6.9 7.8 5.7 5.9 | 1.3 | 17.3 |
| Primer neutral light 0-13 | 1.9 1.4 2.0 1.3 1.6 1.9 2.1 20.1 16.0 8.1 4.3 7.1 1.9 | 1.3 | 20.1 |
| Primer neutral dark 0-13 | 2.9 3.3 4.1 2.1 1.6 2.0 4.4 14.2 16.6 10.9 6.5 6.9 4.0 | 1.6 | 16.6 |
| Fluent grey 98 → 80 (every 2) | 1.0-1.3 each | 1.0 | 1.3 |
| GOV.UK black tints (white, 95, 80, 50, 25, primary) | 2.4 8.2 21.0 23.0 18.6 | 2.4 | 23.0 |
| Apple systemGray 6 → 1 (light) | 2.8 4.6 2.4 6.7 9.9 | 2.4 | 9.9 |
| Apple systemGray 6 → 1 (dark) | 5.0 4.5 4.6 9.6 17.1 | 4.5 | 17.1 |
| M3 neutral tones 100 → 0 | 3.2 2.3 1.0 0.6 0.6 1.3 1.4 1.9 4.7 7.5 8.2 9.3 9.6 8.1 7.5 6.4 7.4 | 0.6 | 9.6 |

- A ramp step is not a pairing. A ramp is a menu; most systems do not intend every neighbour to sit together. The pairs below are the ones the token names assign to sit together.

**Documented grey pairs, by role (ΔE00, computed; full table in G1a):**

| Role class | n | Smallest | Median | Largest |
|---|---|---|---|---|
| Surface on surface (page ground against a panel, layer, card, sunken or raised area) | 38 | 0.6 | 2.7 | 7.9 |
| State change of one element (rest against hover or pressed) | 13 | 1.4 | 2.5 | 6.5 |
| Border or divider against its ground | 22 | 3.0 | 9.9 | 35.5 |
| Two text greys (primary against secondary, secondary against helper) | 10 | 9.6 | 13.9 | 22.6 |

- Read:
  1. **Every system that names its pairs (all but Tailwind) ships surface pairs far below ΔE00 10, as deliberate roles.** The page ground against a panel or layer is ΔE00 0.6-3.6 at the light end (Radix 1/2 0.6; Fluent Background1/2 1.0; Atlassian surface/sunken 1.4; Primer default/muted 1.9; Fluent 1/3 2.0; Carbon background/layer01 2.2; GOV.UK white/light-grey 2.4; Apple white/Gray 6 3.6). At the dark end it is ΔE00 2.0-6.4 (Atlassian dark elevation steps 2.0-2.2; Carbon g100 5.0 and 6.1).
  2. **Text greys never pair below about ΔE00 9.6.** The smallest documented pair of two text greys is Fluent Foreground1/Foreground2 (`#242424`/`#424242`) at 9.6, then Atlassian text.subtle/text.subtlest 10.3, Carbon textSecondary/textHelper 10.6 and Fluent Foreground2/Foreground3 10.8. The median is 13.9.
  3. **Borders sit between.** A border that must be seen against its ground is ΔE00 6.5-16 (median 9.9). The faint "subtle" borders are ΔE00 3.0-7.7; the "strong" or input borders that must pass WCAG 1.4.11 are ΔE00 28-36 (see G2).
  4. So practice has **no single grey line**. The gap that a system uses on purpose depends on the **role and the area**: large flat areas that tile edge to edge go as low as ΔE00 1-3; text and small marks start at about ΔE00 10.
- Limit: this shows what teams ship, not what viewers judge. It is evidence that a small gap between **two large areas** does not read as an error to these teams. It is not evidence about two **small marks** (text, a logo, an icon) in one grey family.

### G1a. Table of documented grey pairs (computed)

ΔL\* is the CIELAB lightness gap; contrast is the WCAG 2 ratio. M3 `surface / surfaceContainerLowest` is 5.4 because of hue (M3 surface is tinted violet, the lowest container is pure white), not lightness.

| System | Role | Pair | Hex | ΔE00 | ΔL\* | Mean L\* | Contrast |
|---|---|---|---|---|---|---|---|
| carbon | surface | white: background / layer01 | `#ffffff` / `#f4f4f4` | 2.2 | 3.8 | 98 | 1.10 |
| carbon | surface | white: layer01 / layerAccent01 | `#f4f4f4` / `#e0e0e0` | 4.3 | 7.0 | 93 | 1.20 |
| carbon | state | white: layer01 / layerHover01 | `#f4f4f4` / `#e8e8e8` | 2.5 | 4.2 | 94 | 1.11 |
| carbon | state | white: background / backgroundHover (alpha .12) | `#ffffff` / `#f1f1f1` | 2.8 | 4.9 | 98 | 1.13 |
| carbon | border | white: background / borderSubtle00 | `#ffffff` / `#e0e0e0` | 6.5 | 10.8 | 95 | 1.32 |
| carbon | border | white: layer01 / borderSubtle01 | `#f4f4f4` / `#c6c6c6` | 10.4 | 16.3 | 88 | 1.55 |
| carbon | border | white: background / borderStrong01 | `#ffffff` / `#8d8d8d` | 28.8 | 41.4 | 79 | 3.32 |
| carbon | surface | white: skeletonBackground / skeletonElement | `#e8e8e8` / `#c6c6c6` | 7.9 | 12.1 | 86 | 1.39 |
| carbon | text | white: textPrimary / textSecondary | `#161616` / `#525252` | 19.3 | 27.6 | 21 | 2.32 |
| carbon | text | white: textSecondary / textHelper | `#525252` / `#6f6f6f` | 10.6 | 12.0 | 41 | 1.56 |
| carbon | surface | g100: background / layer01 | `#161616` / `#262626` | 5.0 | 7.9 | 11 | 1.20 |
| carbon | surface | g100: layer01 / layer02 | `#262626` / `#393939` | 6.1 | 8.8 | 20 | 1.31 |
| carbon | state | g100: layer01 / layerHover01 | `#262626` / `#333333` | 4.1 | 6.1 | 18 | 1.20 |
| carbon | border | g100: layer01 / borderSubtle01 | `#262626` / `#525252` | 14.4 | 19.7 | 25 | 1.94 |
| carbon | surface | g90: background / layer01 | `#262626` / `#393939` | 6.1 | 8.8 | 20 | 1.31 |
| radix | surface | gray: 1 app bg / 2 subtle bg | `#fcfcfc` / `#f9f9f9` | 0.6 | 1.0 | 98 | 1.03 |
| radix | surface | gray: 1 app bg / 3 element bg | `#fcfcfc` / `#f0f0f0` | 2.5 | 4.2 | 97 | 1.11 |
| radix | state | gray: 3 / 4 hover | `#f0f0f0` / `#e8e8e8` | 1.7 | 2.8 | 93 | 1.08 |
| radix | state | gray: 4 hover / 5 active | `#e8e8e8` / `#e0e0e0` | 1.8 | 2.8 | 91 | 1.08 |
| radix | border | gray: 1 / 6 subtle border | `#fcfcfc` / `#d9d9d9` | 7.5 | 12.3 | 93 | 1.38 |
| radix | border | gray: 2 / 6 subtle border | `#f9f9f9` / `#d9d9d9` | 6.9 | 11.2 | 92 | 1.34 |
| radix | border | gray: 3 element bg / 7 element border | `#f0f0f0` / `#cecece` | 7.6 | 12.0 | 89 | 1.38 |
| radix | state | gray: 7 border / 8 hover border | `#cecece` / `#bbbbbb` | 4.8 | 6.9 | 79 | 1.22 |
| radix | text | gray: 11 / 12 text | `#646464` / `#202020` | 22.6 | 30.1 | 27 | 2.75 |
| radix | surface | gray-dark: 1 / 2 | `#111111` / `#191919` | 2.2 | 3.7 | 7 | 1.07 |
| radix | surface | gray-dark: 1 / 3 | `#111111` / `#222222` | 5.1 | 8.2 | 9 | 1.19 |
| radix | border | gray-dark: 1 / 6 | `#111111` / `#3a3a3a` | 12.7 | 19.4 | 15 | 1.66 |
| fluent | surface | light: Background1 / Background2 | `#ffffff` / `#fafafa` | 1.0 | 1.7 | 99 | 1.04 |
| fluent | surface | light: Background1 / Background3 | `#ffffff` / `#f5f5f5` | 2.0 | 3.5 | 98 | 1.09 |
| fluent | surface | light: Background2 / Background3 | `#fafafa` / `#f5f5f5` | 1.0 | 1.7 | 97 | 1.04 |
| fluent | state | light: Background1 / Background1Hover | `#ffffff` / `#f5f5f5` | 2.0 | 3.5 | 98 | 1.09 |
| fluent | state | light: Background1 / Background1Pressed | `#ffffff` / `#e0e0e0` | 6.5 | 10.8 | 95 | 1.32 |
| fluent | border | light: Background1 / Stroke3 | `#ffffff` / `#f0f0f0` | 3.0 | 5.2 | 97 | 1.14 |
| fluent | border | light: Background1 / Stroke2 | `#ffffff` / `#e0e0e0` | 6.5 | 10.8 | 95 | 1.32 |
| fluent | border | light: Background1 / Stroke1 | `#ffffff` / `#d1d1d1` | 9.9 | 16.2 | 92 | 1.53 |
| fluent | text | light: Foreground1 / Foreground2 | `#242424` / `#424242` | 9.6 | 13.8 | 21 | 1.54 |
| fluent | text | light: Foreground2 / Foreground3 | `#424242` / `#616161` | 10.8 | 13.2 | 35 | 1.62 |
| fluent | surface | dark: Background1 / Background2 | `#292929` / `#1f1f1f` | 3.2 | 4.8 | 14 | 1.13 |
| fluent | surface | dark: Background2 / Background3 | `#1f1f1f` / `#141414` | 3.4 | 5.4 | 9 | 1.12 |
| fluent | border | dark: Background1 / Stroke2 | `#292929` / `#525252` | 13.5 | 18.3 | 26 | 1.86 |
| atlassian | surface | light: surface / surface.sunken | `#ffffff` / `#f8f8f8` | 1.4 | 2.4 | 99 | 1.06 |
| atlassian | state | light: surface / surface.hovered | `#ffffff` / `#f0f1f2` | 2.9 | 4.9 | 98 | 1.13 |
| atlassian | state | light: surface.hovered / surface.pressed | `#f0f1f2` / `#dddee1` | 4.2 | 6.6 | 92 | 1.19 |
| atlassian | border | light: surface / border (alpha) | `#ffffff` / `#dddedd` | 7.1 | 11.6 | 94 | 1.35 |
| atlassian | border | light: surface / border.input | `#ffffff` / `#8c8f97` | 28.5 | 40.6 | 80 | 3.24 |
| atlassian | surface | light: surface / background.neutral (alpha) | `#ffffff` / `#f0f1f2` | 2.9 | 4.9 | 98 | 1.13 |
| atlassian | text | light: text / text.subtle | `#292a2e` / `#505258` | 13.2 | 17.8 | 26 | 1.84 |
| atlassian | text | light: text.subtle / text.subtlest | `#505258` / `#6b6e76` | 10.3 | 11.5 | 41 | 1.53 |
| atlassian | surface | dark: surface.sunken / surface | `#18191a` / `#1f1f21` | 2.3 | 3.1 | 10 | 1.07 |
| atlassian | surface | dark: surface / surface.raised | `#1f1f21` / `#242528` | 2.0 | 2.9 | 13 | 1.07 |
| atlassian | surface | dark: surface.raised / surface.overlay | `#242528` / `#2b2c2f` | 2.2 | 3.3 | 16 | 1.10 |
| atlassian | surface | dark: surface / surface.overlay | `#1f1f21` / `#2b2c2f` | 4.1 | 6.2 | 15 | 1.18 |
| atlassian | border | dark: surface / border (alpha) | `#1f1f21` / `#37373a` | 7.7 | 11.3 | 18 | 1.39 |
| primer | surface | light: bgColor.default / bgColor.muted | `#ffffff` / `#f6f8fa` | 1.9 | 2.5 | 99 | 1.06 |
| primer | state | light: control rest / hover | `#f6f8fa` / `#eff2f5` | 1.4 | 2.1 | 96 | 1.06 |
| primer | state | light: control hover / active | `#eff2f5` / `#e6eaef` | 2.0 | 2.8 | 94 | 1.08 |
| primer | border | light: bgColor.default / borderColor.default | `#ffffff` / `#d1d9e0` | 9.4 | 13.7 | 93 | 1.43 |
| primer | border | light: bgColor.default / borderColor.muted (alpha .70) | `#ffffff` / `#dfe4e9` | 6.5 | 9.7 | 95 | 1.28 |
| primer | border | light: bgColor.muted / borderColor.default | `#f6f8fa` / `#d1d9e0` | 7.6 | 11.2 | 92 | 1.34 |
| primer | text | light: fgColor.default / fgColor.muted | `#1f2328` / `#59636e` | 21.2 | 28.0 | 28 | 2.58 |
| primer | surface | dark: bgColor.inset / bgColor.default | `#010409` / `#0d1117` | 2.9 | 3.9 | 3 | 1.09 |
| primer | surface | dark: bgColor.default / bgColor.muted | `#0d1117` / `#151b23` | 3.3 | 4.6 | 7 | 1.09 |
| primer | state | dark: control rest / hover | `#212830` / `#262c36` | 2.1 | 2.1 | 17 | 1.06 |
| primer | border | dark: bgColor.default / borderColor.default | `#0d1117` / `#3d444d` | 15.9 | 23.6 | 17 | 1.92 |
| m3 | surface | light: surface / surfaceContainerLowest | `#fdf7ff` / `#ffffff` | 5.4 | 2.1 | 99 | 1.05 |
| m3 | surface | light: surface / surfaceContainerLow | `#fdf7ff` / `#f8f2fa` | 1.0 | 1.7 | 97 | 1.04 |
| m3 | surface | light: surfaceContainerLow / Container | `#f8f2fa` / `#f2ecf4` | 1.3 | 2.1 | 95 | 1.05 |
| m3 | surface | light: surfaceContainer / High | `#f2ecf4` / `#ece6ee` | 1.3 | 2.1 | 93 | 1.06 |
| m3 | surface | light: surfaceContainerHigh / Highest | `#ece6ee` / `#e6e0e9` | 1.4 | 2.1 | 91 | 1.06 |
| m3 | surface | light: surface / surfaceContainer | `#fdf7ff` / `#f2ecf4` | 2.3 | 3.8 | 96 | 1.10 |
| m3 | surface | light: surface / surfaceContainerHighest | `#fdf7ff` / `#e6e0e9` | 4.9 | 8.0 | 94 | 1.23 |
| m3 | border | light: surface / outlineVariant | `#fdf7ff` / `#cac4cf` | 11.5 | 18.0 | 89 | 1.62 |
| m3 | border | light: surface / outline | `#fdf7ff` / `#7a757f` | 35.5 | 47.9 | 74 | 4.26 |
| m3 | text | light: onSurface / onSurfaceVariant | `#1d1b20` / `#49454e` | 13.9 | 19.8 | 20 | 1.83 |
| m3 | surface | dark: surface / surfaceContainerLow | `#141218` / `#1d1b20` | 2.7 | 4.3 | 8 | 1.09 |
| m3 | surface | dark: surfaceContainerLow / Container | `#1d1b20` / `#211f24` | 1.3 | 2.0 | 11 | 1.05 |
| m3 | surface | dark: surfaceContainer / High | `#211f24` / `#2b292f` | 3.2 | 4.9 | 15 | 1.14 |
| m3 | surface | dark: surfaceContainerHigh / Highest | `#2b292f` / `#36343a` | 3.5 | 5.1 | 20 | 1.17 |
| govuk | surface | body-background / black tint-95 (light-grey panel) | `#ffffff` / `#f3f3f3` | 2.4 | 4.2 | 98 | 1.11 |
| govuk | border | body-background / border (tint-80) | `#ffffff` / `#cecece` | 10.7 | 17.2 | 91 | 1.57 |
| govuk | text | text / secondary-text (tint-25) | `#0b0c0c` / `#484949` | 18.6 | 27.7 | 17 | 2.17 |
| apple | surface | white / systemGray6 | `#ffffff` / `#f2f2f7` | 3.6 | 4.4 | 98 | 1.12 |
| apple | surface | dark: black / systemGray6 dark | `#000000` / `#1c1c1e` | 6.4 | 10.3 | 5 | 1.23 |

### G2. Standards: WCAG 2.2 SC 1.4.11 and APCA non-text levels, converted to ΔE00 for greys — opened; converted

- **WCAG 2.2 SC 1.4.11 Non-text Contrast** — grade **S**; measures **discrimination** (visibility for people with moderately low vision). Opened: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html (14 Oct 2026).
  - Quoted: "Visual information required to identify user interface components and states … a contrast ratio of at least 3:1 against adjacent color(s)".
  - Quoted: "This success criterion does not require that controls have a visual boundary indicating the hit area. If a control has visible content (such as text or a sufficiently contrasting icon) … a border or other indication of the overall boundary of the hit area is not required".
  - Quoted: "if the focus state relies on a change of color (e.g., changing only the background color of a button), this success criterion does not define any requirement for the difference in contrast between the two states."
  - So 1.4.11 sets a floor only for a grey that **alone** identifies a component or its state. It sets **no** floor for a surface layer, a card ground or a decorative divider.
- **APCA "in a nutshell"** (A. Somers, APCA-W3) — grade **T/S-draft** (a candidate method, not a W3C standard); measures **discrimination** (visibility). Opened: https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html.
  - Quoted: "consider Lc 15 the point of invisibility for many users". Quoted: "Lc 15 • The absolute minimum for any non-semantic non-text that needs to be discernible, and is no less than 5px (solid) in its smallest dimension. This may include dividers … Designers should treat anything below this level as invisible". Quoted: "Lc 30 … the minimum for large/solid semantic & understandable non-text elements such as 'mostly solid' icons".
- Script: `.claude/tmp/de00-grey-tools/greycurve.py`. For two pure greys CIEDE2000 reduces to ΔL\*/S_L, with S_L = 1 + 0.015(L̄−50)²/√(20+(L̄−50)²). The script checks this closed form against `de2000` (largest error < 1e-9). APCA: the APCA-W3 0.0.98G-4g constants, coded by me from the published formula. **Approximate** for APCA.

**S_L, the CIEDE2000 lightness weight, for greys (computed):** at mean L\* 50 it is 1.00; at L\* 27 (the logo grey `#404040`) 1.34; at L\* 85 1.52; at L\* 95 1.67. So ΔE00 10 between two greys is ΔL\* 10 at mid-grey, ΔL\* 13.4 near `#404040`, ΔL\* 16-17 near white or black.

**Contrast ratios converted to ΔE00 for greys (converted):**

| Base grey | 1.1:1 | 1.2:1 | 1.3:1 | 1.5:1 | 2:1 | 3:1 (SC 1.4.11) | 4.5:1 |
|---|---|---|---|---|---|---|---|
| White `#ffffff` | 2.4 | 4.3 | 6.3 | 9.7 | 16.5 | **26.6** | 36.9 |
| Pale `#d9d9d9` | 2.4 | 4.6 | 6.3 | 9.8 | 17.2 | **27.8** | 38.9 |
| Logo grey `#404040` | 2.3 | 3.9 | 5.7 | 8.9 | 15.9 | **27.6** | 42.6 |
| Black `#000000` | 2.7 | 5.5 | 7.7 | 11.2 | 17.6 | **26.2** | 35.8 |

- Read: **ΔE00 10 between two greys is about 1.5:1** at every lightness (1.42-1.57:1, computed). **SC 1.4.11's 3:1 is about ΔE00 26-28** for greys. So the 3:1 line is far above any near-miss line.

**APCA Lc 15 ("point of invisibility") converted to ΔE00 (converted, approximate):**

| Base grey | Nearest grey at \|Lc\| ≥ 15 | ΔE00 | WCAG ratio |
|---|---|---|---|
| White, darker side | `#e4e4e4` | 5.6 | 1.27 |
| Pale `#d9d9d9`, lighter side | `#f4f4f4` | 5.9 | 1.28 |
| Pale `#d9d9d9`, darker side | `#bdbdbd` | 6.9 | 1.33 |
| Logo grey `#404040`, lighter side | `#6a6a6a` | **14.8** | 1.92 |
| Black, lighter side | `#4e4e4e` | 22.2 | 2.52 |

- Read: APCA models the eye as **less sensitive to differences between dark greys** than CIEDE2000 does. At the light end, Lc 15 is about ΔE00 6. Near `#404040`, Lc 15 needs ΔE00 about 15. The three mmm-infra pairs against `#404040` (`#2a2925` 7.9, `#595959` 8.6, `#5c5c5c` 9.6) have APCA \|Lc\| about 0-10. By APCA's rule that is "invisible for many users" as a non-text difference. (APCA clips any result below about Lc 7 to 0, so the dark-side pair reads 0.)
- What this gives the grey near-miss line: no direct figure. Both standards measure visibility. But APCA gives a **lightness-dependent** visibility floor: if many users cannot see a difference, then the difference cannot read as deliberate to them. For dark greys that floor (ΔE00 about 15) is **above** 10; for light greys (ΔE00 about 6) it is **below** 10.
- Mismatch to note: APCA's levels come from its author's readability work on text and are not peer-reviewed as a non-text threshold. CIEDE2000 and APCA disagree most at the dark end.

### G3. Is ΔE00 valid for lightness-only pairs? The S_L term, dark greys and the ground — opened (two full texts), abstracts (three)

- **Berns 2016, "Modification of CIEDE2000 for Assessing Color Quality of Image Archives"** — IS&T Archiving 2016, pp. 181-185. **Opened** (full text, https://www.rit.edu/science/sites/rit.edu.science/files/2019-03/ModificationImageArchives.pdf). Grade **P** (conference). Measures: re-analysis of the **discrimination** data sets that CIEDE2000 was fitted on.
  - Method: from the CIEDE2000 "COM" data (BFD, Leeds, Witt, RIT-DuPont), 454 pairs that differ mainly in lightness (|ΔL\*|/ΔE\*ab ≥ 0.9).
  - Quoted: "The R² between the visual data and S_L was 0.135 and for the line fit, 0.142. Clearly, the lightness data are poorly fit in either case questioning both the precision of this type of visual data and TC 1-47's decision to include a S_L function other than unity."
  - Quoted: "The Leeds' datasets, used to derive S_L, do not contain the range of lightness common to image archives. Its minimum L\* is only near 30. Datasets with darker colors, RIT-DuPont and BFD D, tend to flatten out rather than increase." The same result held for near-neutral pairs only ("average C\*ab ≤ 5.0").
  - Quoted: "CIEDE2000's S_L function is a parametric function for the Leeds' datasets … It is not a weighting function that accounts for a fundamental limitation in CIELAB's ΔE\*ab."
- **Melgosa et al. 2018, "Is it possible to improve the weighting function for lightness in the CIEDE2000 color-difference formula?"** — Color Culture and Science Journal 10. **Abstract opened** (https://jcolore.gruppodelcolore.it/ojs/index.php/CCSJ/article/view/ccsj.i102018.07). Grade **P**. Measures: discrimination (13 CIE 217:2016 data sets, STRESS).
  - Quoted: "None of the three mentioned CIEDE2000-modified formulas performed statistically significantly better than the original ΔE00 … Therefore, the replacement of the S_L function in ΔE00 by S_L = 1 is not recommended." And: "for eight of the thirteen visual datasets there were no color pairs with average L\* values below 25, which claims for future studies using darker color pairs."
  - The same group's 2017 Coloration Technology paper (doi 10.1111/cote.12294) has the same title stem; **cited only** (search summary).
- **Whittle 1992, "Brightness, discriminability and the 'crispening effect'"** — Vision Research 32(8):1493-1507. **Abstract opened** (PubMed 1455722). Grade **P**. Measures: suprathreshold **lightness scaling** (equal-interval grey series on black, white or grey grounds).
  - Quoted: the steps "showed a sharp minimum at the background luminance … the 'Crispening Effect'. They followed Weber's Law with respect to L when L was small, but with respect to ΔL … near Lb. The Crispening Effect was abolished by a thin outline or a hue difference between circles and background."
- **Xin, Lam & Luo 2004, "Evaluation of the crispening effect using CRT-displayed colour samples"** — Color Res. Appl. 29(5):374-380, doi 10.1002/col.20045. **Abstract opened** (PolyU record). Grade **P**. Measures: suprathreshold **lightness difference** of grey pairs (38 neutral pairs, each 5.0 CIELAB units, L\* 0-100, five neutral grounds).
  - Quoted: "The colour differences of the same pair assessed under different backgrounds could differ by a factor of up to 8 for a sample pair with low lightness. The perceived colour difference was enlarged when the lightness of a sample pair was similar to that of the background."

- Read for the grey line:
  1. **ΔE00 is weakest on exactly our case.** For pairs that differ in lightness, its S_L term explains about 14% of the variance in its own data. There are almost no fitted pairs with mean L\* below 25-30. The mmm-infra greys sit at L\* 17-39 (`#2a2925` L\* 17, `#404040` 27, `#595959`/`#5c5c5c` 37-39). So "ΔE00 7.9 / 8.6 / 9.6" carries a wide error for these pairs. With S_L = 1 (Berns), the same pairs are 10.5, 10.7 and 12.0 (their ΔL\*).
  2. **The ground changes the answer by a large factor, and ΔE00 has no term for the ground.** CIEDE2000 was fitted mostly on mid-grey surrounds. On a white page, two dark greys are far from the ground, so their difference looks smaller (up to 8× for dark pairs between grounds, Xin et al.). Two near-white greys on a white page sit at the crispening point, so their difference looks larger. This explains G1: systems pair near-white surfaces at ΔE00 1-3 and they read clearly, but no system pairs two dark text greys below about ΔE00 10.
  3. Whittle: an **outline or a hue difference abolishes** crispening. A border between two surfaces or a tint changes the result again.
- Consequence: **one ΔE00 number cannot be the grey line for all lightness levels and grounds.** A line for greys must say which ground (white page or dark band) and which lightness band (near the ground, or far from it).

### G4. Names along the grey axis: the naming proxy does not work for greys — computed from Heer & Stone's c3 model

- Data: c3 model `c3_data.json` (Heer & Stone 2012; XKCD survey; copy in `.claude/tmp/de00-src/c3/`). Grade: **derived from P data**. Measures: **naming** (single colours, free names, uncalibrated screens).
- Script: `.claude/tmp/de00-grey-tools/c3-greys.py`. It takes the 21 bins with a\* = b\* = 0 (L\* 0-100 in steps of 5) and compares their name distributions.
- Result (computed): the name "grey" holds from about **L\* 25 to L\* 90** (36-84% of names; "dark grey" 5-27%, "light grey" 2-14%). The most frequent name changes only near the ends: black → grey at L\* 20-25, grey → white at L\* 90-95.
  - Two greys **ΔL\* 20 apart** in the middle (for example L\* 40 and 60, ΔE00 20.0) have name distance 0.02: the same name.
  - For pairs 10 L\* apart, the most frequent name differs for only 4 of 19 pairs, all at the black end (L\* 15-30) or the white end (L\* 85-100).
- Read: for hues, the earlier pass found that most pairs below ΔE00 6-10 share a name and that names split at about ΔE00 12-18 (`de00-thresholds.md` F12). **For greys this proxy does not exist.** A mid grey and another mid grey stay "grey" at any gap up to about ΔE00 20. The cue for intent must come from the size of the step that the viewer sees, or from the role (G1).
- Limits: XKCD names are of one colour alone; "darkgrey" and "lightgrey" are separate terms in the model, so the "grey" share is a lower bound on the "some kind of grey" share.

### G5. How many greys a viewer can tell apart from memory, and grey classes meant to be told apart — opened; computed

- **Miller 1956, "The magical number seven, plus or minus two"** — Psychological Review 63(2):81-97. **Opened** (http://psychclassics.yorku.ca/Miller/). Grade **P** (review). Measures: **absolute identification** (name which level, one stimulus at a time).
  - Quoted: "In a separate experiment Eriksen (5) found 2.8 bits for size, 3.1 bits for hue, and 2.3 bits for brightness." 2.3 bits = about **5 levels**. Eriksen's paper itself: **cited only**.
  - Read (my reading, not Miller's): seen **one at a time** (from memory), a viewer can place a grey in only about 5 levels from black to white. Five levels over L\* 0-100 are about ΔL\* 20-25 apart, about ΔE00 15-25 for greys (converted with the S_L of G2). Two greys closer than that cannot be told apart **from memory**; the viewer must see them side by side. This is an upper reference for greys that sit far apart on a page (a logo grey at the top, a text grey in a footer), not a near-miss line.
- **ColorBrewer "Greys"** (Brewer, Harrower; axismaps/colorbrewer `colorbrewer_schemes.js`, **opened**, raw GitHub). Grade **I/T** (the standard tool for map class colours; Brewer's schemes were tested on maps). Measures: **practice** for grey classes that a reader must tell apart, with a legend.
  - Adjacent-class ΔE00 (computed): 5 classes: 9.5, 15.1, 19.9, 20.7. 7 classes: 6.5, 6.9, 11.3, 12.9, 12.2, 14.7. 9 classes: 3.0, 5.0, 6.9, 11.3, 12.9, 12.2, 14.7, 9.0.
  - Read: grey classes meant as **different values** are about ΔE00 11-15 apart in the middle and dark part of the scale, and only ΔE00 3-7 apart near white (the crispening zone on a white map ground, G3).

### G6. Tools that flag near-duplicate colours, and their thresholds — opened (code and READMEs)

All grade **T**. All measure **intent by proxy**: the tool assumes that two colours closer than its threshold are one colour that slipped. No tool gives a separate line for greys.

| Tool | Metric | Flags a pair as a near-duplicate when | Stated basis | Access |
|---|---|---|---|---|
| CSS Colorguard (Alex Sexton, built at Stripe; SlexAxton/css-colorguard, 2.4k stars; npm `colorguard` 1.2.1) | CIEDE2000 (`color-diff` 0.1.7, `ciede2000()` with kL = 1, read) | ΔE00 < **3** (`threshold: 3` in `lib/colorguard.js`) | Quoted: "the default is `3` but that's mostly personal opinion." Purpose, quoted: "one too many people eye-dropper colors into nooks and crannies … warns you when colors you've added are too similar to ones that already exist." | opened (package and README) |
| `stylelint-no-indistinguishable-colors` 2.3.1 (via `colorguard-processor`) | CIEDE2000 | ΔE00 < **3** by default | Quoted: "Defaults to Colorguard's threshold of 3." | opened (package) |
| Alike Color Finder (donatj, PHP CLI for CI) | CIEDE2000 (default) | ΔE00 ≤ **4** | Quoted: "detects nearly identical colors before they become visual drift"; "The default `ciede2000` strategy reports colors whose difference is at most `4`." No basis given. | opened (README via GitHub API) |
| Color Cluster Merger (Figma plugin, 2026, 1 install) | "Delta E" on LAB (formula not named) | user threshold | Quoted: "2 = very strict, almost identical colors; 5 = good default for cleaning near-duplicate colors; 10 = more aggressive grouping; 20 = broad color-family grouping, review carefully". No basis given. | opened (Figma plugin API JSON) |
| Color Cleaner; Find & Merge Similar Colors (Figma plugins, 121 and 19 installs) | not stated | slider ("Level of cleanup") | Quoted: "minimizing subtle variations of the same shade". No number. | opened (Figma plugin API JSON) |
| plumb `color/palette-conformance` rule (aram-devdocs/plumb PR #112) | CIEDE2000 | a page colour is **off-palette** if ΔE00 > **2** from every token (so within 2 = treated as the token) | none | opened (PR body via GitHub API) |

- Read: tools that hunt near-duplicates set the line at **ΔE00 2-5**, and one author calls his number "personal opinion". They aim to catch slips (eye-droppered copies), and they accept a miss above the line. They do not claim that a pair above 3-5 reads as deliberate. So the tool route gives a **lower bound** for the near-miss band (under about ΔE00 3-5, a pair is almost surely a slip), not its upper edge.
- Searched and not found: a design-token linter (Style Dictionary, Tokens Studio, Figma Variables) with a near-duplicate check and a published threshold; any tool with a grey-specific threshold.

### G7. Brychtová & Çöltekin 2016 against Moon & Spencer 1944: which one fits two greys on a screen — opened (B&C full text, again); M&S as in `de00-thresholds.md` F3; computed

- **Moon & Spencer 1944** (grade **P, theory**; measures **intent**, by definition). Its "first ambiguity" zone is the exact near-miss idea: colours so close "that there is doubt as to whether they were intended to be identical or only similar" (quoted through arXiv 1709.02252; body text **cited only**). For value (lightness) the zone ends at ½ Munsell value step.
  - Converted at the mmm-infra greys (script inline, ASTM D1535 value function, S_L of G2; **approximate**): near `#404040` (Munsell V 2.7), ½ value step = ΔE00 3.7-4.0; the "similarity" zone runs to 1½ steps = ΔE00 10.3 (darker) to 12.7 (lighter). The three mmm-infra pairs are each about **1 value step** from `#404040` (`#2a2925` V 1.6, `#595959` V 3.7, `#5c5c5c` V 3.8). So M&S put all three in "similarity" (two related greys, chosen), **not** in "ambiguity".
  - Method: no observers. The zones come from classical harmony writing. Chuang & Ou 2001 measured harmony against ΔE\*ab and rejected per-attribute zones (`de00-thresholds.md` F4). Fit to our case: the **question** fits exactly; the **evidence** is nil.
- **Brychtová & Çöltekin 2016** (grade **P**; measures **discrimination**, same/different). Re-read for this question:
  - The "lightness-only" pairs were **not greys**. Quoted Table 1: six greens at a\* −30, b\* +30 (C\*ab 42), L\* 33-95; "we kept values a and b stable, while alternating value L (lightness)".
  - The extra need of lightness pairs comes from **spatial separation**. Quoted: "spatial distance has bigger impact on distinguishing the quantities (shades of sequential schemes) rather than qualities (different hues)". For adjacent areas, the response-time test of sequential against qualitative was not significant (Table 4, "Sequential S ~ Qualitative S … 0.41"). Quoted: "Accuracy at ΔE00 = 10 is particularly high (more than 90%) at all spatial distances."
  - ΔE00 10 was the largest value tested.
  - Fit to our case: screens and real layouts, yes; ΔE00 native, yes; greys, no; intent, no.
- **The two do not conflict once the task is named.** M&S's ½ step (about ΔE00 4) is where two **touching** samples stop looking identical. B&C show that lightness pairs that sit **apart** need about ΔE00 10 before nearly all viewers tell them apart. A near-miss needs both: the viewer sees the difference, and the difference is too small to look chosen. So the near-miss band for greys starts near M&S's ΔE00 4 and its top is set by what B&C and the other routes say about "clearly different".
- **Which the evidence favours, for our case:** B&C, on method (measured, screen, ΔE00). Two further measured sources agree that lightness is not easier than hue at large sizes: Szafir 2018 converted (`de00-thresholds.md` F1a) gives 50% detection at 50 px for ΔL\* steps at ΔE00 5.0 against 4.0-4.2 for a\* and b\*. But at 6 px dots the order flips (ΔL\* 7.4 against 9.5-10.4), so for **small marks and text, lightness is the easier axis**. Net: the evidence does not support a grey line **below** 10 for marks apart on a page. It supports a grey line at or above 10 for large areas apart, and it gives M&S's ΔE00 4 only as the **bottom** of the band.

## Synthesis

### What each route says

| Route | What it measures | What it says about the grey line | Strength |
|---|---|---|---|
| 1. Practice census (G1, G5) | Practice | Two **text or mark greys** that systems ship as separate roles are never below ΔE00 **9.6** (Fluent 9.6, Atlassian 10.3, Carbon 10.6, Fluent 10.8; median of 10 text pairs 13.9). ColorBrewer grey classes in the mid and dark range are ΔE00 11-15 apart. **Surfaces** near the page ground are paired on purpose at ΔE00 **0.6-3.6** (light) and 2.0-6.4 (dark); ColorBrewer's light classes are 3-7 apart. | I; computed from opened files |
| 2. Standards (G2) | Discrimination | WCAG 1.4.11's 3:1 = ΔE00 26-28 for greys and binds only a grey that alone identifies a control; no floor for surfaces. APCA's Lc 15 "point of invisibility" = ΔE00 **5.6-6.9** near white and **14.8** near `#404040` (converted). | S, T; converted |
| 3. Perception (G3, G4, G5, G7) | Discrimination, naming, scaling | ΔE00's lightness term has weak support (R² 0.135) and almost no data below L\* 25-30. The ground changes perceived grey differences by up to 8× (crispening); near the ground, small steps look large; far from it, they look small. Greys keep the one name "grey" from L\* 25 to 90, so a name never marks a second grey as deliberate. From memory, viewers place greys in about 5 levels (ΔE00 15-25 apart). M&S's ambiguity zone ends at ΔE00 about 4; B&C's lightness pairs reach > 90% discrimination at ΔE00 10. | P; quoted, computed, converted |
| 4. Tools (G6) | Intent by proxy | Near-duplicate finders flag pairs under ΔE00 **3-5** (Colorguard 3, "mostly personal opinion"; Alike 4; a Figma plugin's "good default" 5). This is the bottom of the band, not its top. | T; quoted from code |

### Best-supported grey near-miss figure

**There is no single grey line. The evidence gives two lines, set by where the two greys sit against the page ground.**

1. **Greys far from the ground** (dark greys on a light page, light greys on a dark band; text, a logo, icons, small marks, or areas that do not touch): near-miss band **ΔE00 ~4 to 10-15**. The floor of deliberate practice is **10** (9.6-10.8 in three systems). The points where APCA, ColorBrewer and the median of practice meet are **13-15**. So for this case, **10 holds as the minimum, and the evidence leans higher (about 13-15)**. It does **not** support a line below 10.
2. **Greys near the ground and large** (page against panel, card, layer or sunken area, with a shared edge): pairs are deliberate from about **ΔE00 2-4** (every one of the eight systems with documented pairs ships such a pair below 4; Tailwind documents no pairs). Here a line at 10 is wrong. It would flag every system's surface layering as a near-miss. The near-miss band in this case is about **ΔE00 1-3** (the tools' range; Radix 1/2 at 0.6 and Fluent 1/2 at 1.0 are the only shipped pairs below it).

**Does it differ from 10?** For case 1, no in direction: 10 is the sourced floor, with a lean upwards. For case 2, yes: the line is far lower (about 3).

**The mmm-infra pairs (all case 1, dark greys on paper):** `#2a2925` 7.9 and `#595959` 8.6 sit below every deliberate dark-grey pair found; they are near-misses on all routes except M&S (theory). `#5c5c5c` at 9.6 equals the smallest shipped pair (Fluent `#242424`/`#424242`) and is below the 13-15 meeting point. With S_L = 1 (Berns), the pairs are ΔL\* 10.5, 10.7 and 12.0; Carbon's textSecondary/textHelper is ΔL\* 12.0. So `#5c5c5c` is a borderline case on any metric.

### Remaining gap

- **No source measures intent for greys.** Every route is a proxy: practice, visibility, naming, detection.
- **The narrowest open question:** for two greys **far from the page ground** (case 1), where between **ΔE00 10** (the smallest gap that design systems ship) and **ΔE00 13-15** (where APCA's visibility floor, ColorBrewer's dark classes and the median shipped text pair meet) does the founder want the line? This is a point to pick on a sourced range, not a new research question.
- The look test of #178 can answer it. Its "dark" row (`#404040` moved lighter, cards at 4, 7, 10, 13, 16 on white) is case 1. Its "pale" row (`#D9D9D9` moved darker on white, L\* 87) is nearer to case 2. **Prediction from this research:** the founder's line on the pale row will come out lower than on the dark row. If it does not, the ground effect (G3) is weaker in his eye than the literature says.
- A rule needs one extra input that the hue rule does not: whether the pair is near the ground and large (case 2) or far from it (case 1).

### How the gap was settled (#178)

The founder said he has no basis to judge the look test, so the line comes from the sources. A near-miss line marks the gap **below which** a pair is likely a mistake. So it sits at the **floor** of deliberate practice, not at its median. Three systems ship two text greys on purpose at ΔE00 9.6-10.8 (G1), so a line at 13-15 would call that work a mistake. APCA's Lc 15 is a visibility floor against the ground, not a measure of intent between two greys, and 13.9 is a median. Result:

- **Greys far from the ground** (text, a logo, icons, small marks, or areas that do not touch): near-miss below **ΔE00 10**, the same as for hues.
- **Large greys near the ground that share an edge** (page, panel, card, layer): near-miss below **ΔE00 3**. ΔE00 10 does not apply to them.

## Bound

**Opened (full text or file):** design-system packages and files listed in G1 (Carbon colors and themes, Radix Colors, Tailwind 3.4.17 and 4.3.3, Primer primitives, Fluent tokens, Atlassian tokens, govuk-frontend, Apple HIG Color JSON, material-color-utilities 0.3.0); ColorBrewer `colorbrewer_schemes.js`; WCAG 2.2 Understanding 1.4.11; APCA "in a nutshell"; Berns 2016 (full text); Miller 1956 (full text); Brychtová & Çöltekin 2016 (full text, from `.claude/tmp/de00-src/`); Colorguard 1.2.1 source and README, `color-diff` 0.1.7 `diff.js`, `stylelint-no-indistinguishable-colors` 2.3.1, `colorguard-processor` README; Alike Color Finder README; plumb PR #112 body; three Figma plugin descriptions (Figma plugin API JSON).

**Abstract only:** Melgosa et al. 2018 (CCSJ); Whittle 1992 (PubMed); Xin, Lam & Luo 2004 (PolyU record).

**Cited only (not opened):** Moon & Spencer 1944 body text (through arXiv 1709.02252); Melgosa et al. 2017 Coloration Technology; Eriksen 1954/1955 (through Miller).

**Scripts:** in `.claude/tmp/de00-grey-tools/`: `census.py` (+ `census.json`), `m3.mjs`, `greycurve.py`, `c3-greys.py`, `pdf2txt.py`.

**Not done:** Adobe Spectrum and Material 2 dark-elevation overlays (not added to the census); no full text of Xin et al. 2004 (Wiley) for the per-background figures; no search of Figma plugins beyond three; no new observer data.
