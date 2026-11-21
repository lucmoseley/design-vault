# design-vault#247 (map #243): open-source CSS, token, colour and font-metric linters against the house's styling value rules

Date: 15 Oct 2026.

Question: Which open-source linters and measurement libraries can check the house's styling value rules (CSS, design tokens, colour, type) on a rendered candidate? For each rule that the survey (`.claude/tmp/inventory-deterministic.md` §3) lists as measurable but unscripted: can a source-file linter judge it at all, when the vault judges a candidate as rendered, after the cascade, at several widths? Or does the rule need a computed-style read in the browser? Licence, maintenance and weekly downloads for each tool.

Method: primary sources only. npm registry API (`registry.npmjs.org/<pkg>`), npm downloads API (`api.npmjs.org/downloads/point/last-week/<pkg>`, which on 15 Oct 2026 returned the week 6–12 Oct 2026), PyPI JSON API, the repos and rule docs.

## Findings

### F1. Registry facts (npm week 6–12 Oct 2026; "stable 12 m" counts versions without a `-` pre-release tag, published 15 Oct 2025 to 15 Oct 2026)

Source: `registry.npmjs.org/<pkg>` and `api.npmjs.org/downloads/point/last-week/<pkg>`, read 15 Oct 2026. Repo state from `gh api repos/<owner>/<repo>` (archived flag, last push).

| Package | Licence | Latest (date) | Stable releases 12 m | Downloads / week | Repo state |
|---|---|---|---|---|---|
| stylelint | MIT | 17.16.0 (2026-10-01) | 23 | 10,917,750 | active, push 2026-10-15 |
| stylelint-config-standard | MIT | 40.0.0 (2026-01-15) | 1 | 6,385,006 | active |
| stylelint-declaration-strict-value | MIT | 1.12.1 (2026-08-24) | 5 | 596,070 | active, push 2026-08-24 |
| @double-great/stylelint-a11y | MIT | 3.8.1 (2026-10-11) | 26 | 25,621 | active, 12 stars |
| stylelint-a11y (YozhikM, the original) | MIT | 1.2.3 (2020-02-13) | 0 | 14,559 | not archived; last push 2023-10-02. Dead. |
| stylelint-no-indistinguishable-colors | MIT | 2.3.1 (2025-03-14) | 0 | 3,407 | last push 2025-03-14. |
| colorguard-processor (its engine) | Apache-2.0 | 2.0.105 (2025-04-05) | 0 | 2,446 | last push 2025-04-28 |
| colorguard (original) | MIT | 1.2.1 (2017-12-17) | 0 | 35,772 | dead |
| color-diff (the ΔE00 under colorguard) | BSD-3-Clause | 1.4.0 (2023-05-31) | 0 | 253,121 | last push 2024-09-26 |
| stylelint-scales | MIT | 5.0.0 (2024-08-28) | 0 | 1,676 | push 2026-10-13, no release in 12 m |
| stylelint-high-performance-animation | MIT | 2.0.0 (2026-01-25) | 1 | 43,649 | active |
| stylelint-value-no-unknown-custom-properties | CC0-1.0 | 6.1.1 (2026-01-21) | 2 | 180,646 | active |
| stylelint-gamut | MIT | 2.0.1 (2026-05-10) | 2 | 3,108 | active |
| @primer/stylelint-config | MIT | 13.6.0 (2026-03-17) | 4 (150 with pre-releases) | 3,305 | active |
| stylelint-plugin-carbon-tokens | MIT on npm; Apache-2.0 on GitHub (mismatch) | 5.0.6 (2026-06-03) | 14 | 2,816 | active |

### F2. The stylelint ecosystem: what each rule reads

Source: each repo README (`gh api repos/<r>/readme`), stylelint `docs/user-guide/rules.md`, read 15 Oct 2026.

- **stylelint core.** It parses source CSS (PostCSS). It never runs the cascade, never resolves `var()`, never knows the width. Value rules that touch the house: `declaration-property-value-allowed-list` / `-disallowed-list`, `declaration-property-unit-allowed-list`, `function-disallowed-list` (can ban `hsl()`, `darken()` in SCSS source only), `color-no-hex`, `color-named`, `time-min-milliseconds`. `time-min-milliseconds` sets a minimum only, on `transition-*` and `animation-*` durations and delays. No core rule sets a maximum duration.
- **stylelint-declaration-strict-value.** It forces a variable, function or listed keyword for the properties you name (regex allowed). It proves "this declaration uses a token". It does not prove which token, nor the value the token resolves to.
- **@double-great/stylelint-a11y** (active fork of YozhikM/stylelint-a11y). 12 rules. Relevant to the house: `font-size-is-readable` (forbids a declared font size under **15 px**; the house floor is 16 px), `no-text-align-justify`, `no-spread-text` (`max-width` between 45ch and 80ch; the house measure is 45–75 characters, and check-measure.py already measures it rendered), `media-prefers-reduced-motion` (a transition or animation needs a `prefers-reduced-motion` override), `no-outline-none` (no `outline: none` without an alternative), `selector-pseudo-class-focus` (a `:hover` rule needs a `:focus` companion). Each rule reads the declared value of one declaration.
- **stylelint-no-indistinguishable-colors.** It flags two colours in one stylesheet under a threshold (default **3**, range 0–100). The engine is colorguard-processor → postcss-colorguard → `color-diff`'s `diff()`, which is CIEDE2000 (color-diff README line 6). So it is the same metric as `colour_space.de2000`. It compares every pair it finds in the source, with no knowledge of which colours are adjacent on the page. Its threshold is one number; palette.py has three lines (same < 2, apart ≥ 10, grey surfaces ≥ 3).
- **stylelint-scales.** It forces numeric values onto a scale: `space`, `radii`, `font-sizes`, `border-widths`, `alpha-values`, `line-heights`, `sizes`, and more, each with units. This is the nearest linter to the "4 px spacing step": `scales/space` with a 4 px scale. It reads literals; it cannot judge `calc()`, `clamp()` at a width, or a value that arrives through `var()`.
- **stylelint-high-performance-animation.** It flags `transition`/`@keyframes` on layout (and optionally paint) properties. Matches impeccable.md's "no casual animation of layout properties", not a §3 rule.
- **Two limits in the a11y rules, from their own docs.** (a) `font-size-is-readable` checks only `px` and `pt` values of `font-size`. It ignores the `font` shorthand, `rem`, `em`, keyword sizes and preprocessor variables. Its threshold is configurable (`thresholdInPixels`), so 16 is possible, but a page that sets body text in `rem` passes unread. (b) `no-outline-none` checks only selectors with `:focus`. It reports `outline` set to `none`, `0` or a transparent colour, unless a visible `border` or `box-shadow` is in the same rule. So it accepts the house's `box-shadow` ring with `outline: 2px solid transparent`. It does not do the reverse: it never asks that a `box-shadow` ring keep a transparent outline for forced colours, which is the house rule.
- **stylelint-scales `space` takes an enumerated list** (`{scale: [16, 32], units: ["px"]}`), not a step. A 4 px step needs a list of every multiple of 4 the project allows. It checks `<length>` and `<percentage>` values on the properties you pair it with.

### F3. Design-token linters

Registry facts (same method as F1):

| Package | Licence | Latest (date) | Stable 12 m | Downloads / week | Notes |
|---|---|---|---|---|---|
| @terrazzo/cli / @terrazzo/parser | MIT | 2.9.0 (2026-10-14) | 15 | 121,061 / 128,055 | active; repo 475 stars |
| @cobalt-ui/cli (Terrazzo's old name) | MIT | 1.12.0 (2024-11-24) | 0 | 441 | npm marks it deprecated |
| @lapidist/design-lint | MIT | 8.0.0 (2026-05-12) | 10 | 210 | 4 stars; very small use |
| style-dictionary | Apache-2.0 | 5.6.1 (2026-10-10) | 20 | 2,163,280 | a token build tool, not a linter |
| @atlaskit/eslint-plugin-design-system | Apache-2.0 | 16.13.8 (2026-10-14) | 106 | 6,786 | Atlassian tokens in JSX only |

- **Terrazzo** lints a DTCG token *file*, not a page (`packages/parser/src/lint/plugin-core/rules/`). Rules near the house: `a11y-min-contrast` (WCAG 2.1 ratio via `colorjs.io/fn` `contrastWCAG21`, on token *pairs you list*), `a11y-min-font-size` (`minSizePx` / `minSizeRem` on font-size tokens), `duplicate-values`, `max-gamut`, `colorspace`, `valid-shadow`, `valid-duration`, `valid-transition`. It proves the token set is sound. It cannot prove the page uses the tokens, or which token a part takes.
- **@lapidist/design-lint** lints JS, TS, CSS, SCSS, Less and literal inline styles against a configured token set: `design-token/{colors,spacing,border-radius,box-shadow,duration,easing,font-size,outline,opacity,blur,...}` and `design-system/no-hardcoded-spacing` (README; `docs/rules/index.md`). It is the widest rule list of the token linters, but the README says "Dynamic inline style expressions remain unsupported", and its use is 210 downloads a week.
- **@primer/stylelint-config** and **stylelint-plugin-carbon-tokens** are the same idea bound to one design system: `primer/colors`, `primer/spacing`, `primer/typography`, `primer/borders`, `primer/box-shadow`, `primer/responsive-widths` (`width`/`min-width` over 320 px); `carbon/theme-use`, `carbon/layout-use`, `carbon/type-use`, `carbon/motion-duration-use`, `carbon/motion-easing-use`. `carbon/motion-duration-use` flags `transition: opacity 300ms` and wants `$duration-fast-02` or `var(--cds-duration-fast-02)`. That is the form of the house rule "project motion tokens", but for Carbon's tokens only.
- **Style Dictionary** builds tokens to platforms. It has no page or stylesheet lint.
- **Common limit.** Every token linter answers "is the value a token?" in source. None answers "is it the *right* token for this part's role", which is the house's function-first question (house-principles.md dependency order), and none reads the page as rendered. A vault candidate is an HTML page often with no token file, so a token linter needs a token list the candidate may not have.

### F4. Figma-side design-lint (destefanis/design-lint)

Source: repo README and `src/plugin/lintingFunctions.ts`, read 15 Oct 2026. MIT, 519 stars, not on npm (a Figma community plugin), last commit 2023-11-16, last push 2024-01-12. Not maintained in the last 12 months.

Its checks: "Missing fill style", "Missing stroke style", "Missing effects style", "Missing text style" on each layer, and `checkRadius` (each corner radius must be in a user list). The logic ports to a DOM directly as a **computed-style membership test**: for each visible element, is its computed `background-color`, `border-color`, `box-shadow`, font set and `border-radius` in the project's value list? That is a small loop over `getComputedStyle`; the plugin's code is Figma-API code and gives no reusable DOM code. Nothing else in it maps to a §3 rule.

### F5. Colour libraries against the vault's hand-rolled maths

Registry facts (npm as F1; PyPI JSON API and `pypistats.org/api/packages/<p>/recent`, read 15 Oct 2026):

| Package | Language | Licence | Latest (date) | Stable 12 m | Downloads / week | ΔE00 | OKLCH | WCAG 2 ratio | APCA |
|---|---|---|---|---|---|---|---|---|---|
| culori | JS | MIT | 4.0.2 (2025-06-27) | 0 | 3,752,662 | `differenceCiede2000` | yes | `wcagContrast` | no (not in `docs/api.md`) |
| colorjs.io | JS | MIT | 0.7.1 (2026-07-24) | 4 | 9,650,559 | `deltaE2000` (also `deltaEOK`, ITP, Jz, CMC, HCT) | yes | `contrastWCAG21` | `src/contrast/APCA.js`, header "APCA 0.0.98G" |
| apca-w3 | JS | "Limited W3 License" (not OSI) | 0.1.9 (2022-07-04) | 0 | 121,424 | — | — | — | the reference |
| chroma-js | JS | BSD-3-Clause AND Apache-2.0 | 3.2.0 (2025-11-28) | 2 | 3,695,236 | `deltaE` | yes | `contrast` | `src/utils/contrastAPCA.js` |
| coloraide | Python | MIT | 8.13 (2026-09-24) | 24 | 1,287,221 (pypistats; its last_month figure, 585,774, is lower, so this figure is not reliable) | `delta_e_2000` | yes | `wcag21` | no (contrast methods are `wcag21`, `lstar`) |
| colour-science | Python | BSD-3-Clause | 0.4.7 (2025-12-06) | 1 | 93,472 | `delta_E_CIE2000` | `models/oklab.py` | via luminance | no |
| colormath | Python | BSD | 3.0.0 (2017-12-27) | 0 | 37,768 | yes | no | — | no; dead |

Note on culori: no release in 12 months, but the repo had a push on 15 Oct 2026.

- **The vault's own maths is correct to the published data.** `colour_space.de2000` matched all **34** pairs of Sharma, Wu & Dalal's own test file (`hajim.rochester.edu/ece/sites/gsharma/ciede2000/dataNprograms/ciede2000testdata.txt`), in both argument orders, worst absolute error 0.000049 (run 15 Oct 2026, `python3 -I`, no install). `test/palette.test.py` tests 8 of the 34. The OKLab coefficients in `colour_space.oklch` are, digit for digit, the linear-sRGB matrices in Ottosson's post (`bottosson.github.io/posts/oklab/`, the 2021-01-25 update). So a library would replace 108 correct lines, not fix a fault.
- **What a library adds.** (a) Colour parsing: `colour_space` takes only `#RRGGBB`. A computed style gives `rgb()`/`rgba()`, `color(srgb …)`, `oklch()` and `color-mix()` results, and CSS Color 4 §"Serializing Oklab and OkLCh values" keeps an `oklch()` colour in its own syntax. A rendered-page palette check needs a parser for these; culori, colorjs.io and coloraide all parse CSS Color 4. (b) Alpha compositing for a scrim or a translucent fill over its ground. (c) Gamut mapping. (d) APCA, if the house ever wants it as a script (only colorjs.io among the MIT libraries has it).
- **APCA licence.** apca-w3's LICENSE.md: licensed to the W3C/AGWG "for use with WCAG accessibility guidelines for web-delivered and web-based content only", "Patent(s) pending", non-compliant code "shall be deemed in breech of license and a copyright violation", other uses under "AGPU v3" [sic]. It is not an OSI licence. colorjs.io ships its own APCA 0.0.98G under MIT; whether that is free of the apca-w3 terms is a legal question this note does not settle. The house uses APCA only as a design aid (`rule-interactions.md:230`), so no gate script needs it now.
- **Fit with the scripts.** The measuring scripts are Python. coloraide (pure Python, one optional dependency) or colour-science (needs numpy ≥ 2, which the image suites already need) fit; culori/colorjs.io need Node in the page (a Playwright `add_script_tag` of a vendored file) or in `check-curves.js`-style Node scripts.

### F6. Font-metric libraries for the x-height size rule (`rule-interactions.md` worked example: size ≥ 16 px × 0.52 / `face.x-height`)

| Package | Language | Licence | Latest (date) | Stable 12 m | Downloads / week | x-height read |
|---|---|---|---|---|---|---|
| fontkit | JS | MIT (npm); GitHub shows no licence file detected | 2.0.4 (2024-08-09) | 0 | 17,423,708 | `font.xHeight`, `unitsPerEm` (README l. 79–87) |
| opentype.js | JS | MIT | 2.0.0 (2026-05-06) | 2 | 2,561,070 | `font.tables.os2.sxHeight`; WOFF, OTF, TTF; **WOFF2 needs a separate decompressor** (README "Loading a WOFF2 font", suggests wawoff2) |
| @capsizecss/unpack | JS | MIT | 4.0.1 (2026-06-12) | 3 | 7,701,311 | `fromUrl` / `fromFile` / `fromBuffer` → `xHeight`, `capHeight`, `unitsPerEm`, `xWidthAvg`; runs on `fontkitten` (MIT, 1.0.3, 7,459,296 / week) |
| @capsizecss/metrics | JS | MIT | 4.4.0 (2026-10-15) | 9 | 337,529 | pre-computed metrics for Google Fonts and system fonts, by name; no file needed |
| fonttools | Python | MIT | 4.67.0 (2026-10-14) | 11 | 50,992,577 (pypistats) | `TTFont(...)["OS/2"].sxHeight` (OS/2 version ≥ 2); no runtime dependencies; WOFF2 needs `brotli` |

- **The browser already gives the x-height, with no library.** CSS Values 4 defines `ex` as "the used x-height of the first available font"; where the font has no reliable metric the UA may measure a lowercase glyph, and as a last resort "a value of 0.5em must be assumed" (`w3.org/TR/css-values-4/#ex`). So a script can set a probe element to `width: 1ex` inside the text's own `font` and read its width at the computed size: x-height in px, for the face Chromium actually used. The house formula needs x-height as a fraction of the em: `1ex / computed font-size`.
- **Two traps the library route must solve and the `ex` route avoids.** (a) Which file: a font stack falls back per glyph; the Chrome DevTools Protocol `CSS.getPlatformFontsForNode` returns, per text node, each font used with `familyName`, `postScriptName`, `isCustomFont` and `glyphCount` (`devtools-protocol/json/browser_protocol.json`, read 15 Oct 2026). The script would then still have to map that name back to a file. (b) Format: web fonts are mostly WOFF2; opentype.js needs a decompressor, fonttools needs `brotli`.
- **Where a library still earns its place.** The `ex` value is only as good as the font's OS/2 `sxHeight`. A fonttools read can compare `sxHeight` with the measured height of the `x` glyph's bounds, to catch a font with a wrong or missing metric (the fallback 0.5 em would silently hide it). That is a check on the font, once per face, not on the page.
- **Fit.** fonttools is Python and has no dependencies, so it fits the measuring scripts. @capsizecss/metrics is the cheapest route when the face is a Google or system font and no file is at hand.

### F7. The browser protocol already holds the primitives a computed-style check needs

Source: `ChromeDevTools/devtools-protocol` `json/browser_protocol.json`, CSS domain, read 15 Oct 2026. Python Playwright opens a CDP session on Chromium (`context.new_cdp_session(page)`).
- `CSS.forcePseudoState`: "Ensures that the given node will have specified pseudo-classes whenever its style is computed by the browser." With `getComputedStyle` before and after, this is the hover and press diff (`:hover`, `:active`, `:focus-visible`) with no pointer events and no timing.
- `CSS.getMatchedStylesForNode`: the matched rules and declarations for one node, after the cascade. This shows the *authored* value that won, such as `var(--shadow-overlay)`, not only its resolved value. So "this element's `box-shadow` came from a token" is answerable per rendered element, at each width.
- `CSS.getPlatformFontsForNode`: the fonts actually used (F6).

### F8. Open-source tools that read computed style in a browser

| Tool | Licence | Latest (date) | Stable 12 m | Downloads / week | What it reads |
|---|---|---|---|---|---|
| axe-core | MPL-2.0 | 4.14.0 (2026-10-05) | 8 (204 with pre-releases) | 79,734,817 | WCAG rules; `getComputedStyle` in `link-in-text-block`, `color-contrast`, `target-size`, `css-orientation-lock`, `avoid-inline-spacing` |
| @axe-core/playwright | MPL-2.0 | 4.13.0 (2026-08-11) | 6 | 14,281,826 | axe in Playwright (JS) |
| axe-playwright-python (PyPI) | MIT on GitHub; PyPI metadata empty | 0.1.8 (2026-07-24) | 3 | 162,584 (pypistats) | axe in Python Playwright |
| lighthouse | Apache-2.0 | 13.5.0 (2026-09-18) | 9 | 5,404,521 | trace and audits |
| @siteimprove/alfa-rules / alfa-playwright | MIT | 0.119.0 / 0.84.2 (2026-07-22) | 19 / 21 | 3,148 / 2,493 | own CSS cascade (`alfa-cascade`, `alfa-style`) over a page snapshot taken by Playwright |
| accessibility-checker (IBM Equal Access) | Apache-2.0 | 4.0.34 (2026-09-08) | 20 | 29,855 | WCAG rules, some `style_*` rules |
| pa11y | LGPL-3.0-only | 10.0.0 (2026-08-28) | 3 | 257,460 | runs axe or HTML_CodeSniffer |
| designlang (Manavarya09/design-extract) | MIT | 13.3.2 (2026-09-23) | 47 | 790 | Playwright + `getComputedStyle` extraction: colours, type, spacing, shadows, radii, hover/focus/active deltas, runtime motion via `document.getAnimations()` |
| @projectwallace/css-analyzer | MIT | 9.9.4 (2026-10-13) | 25 | 15,045 | source CSS only; counts unique `boxShadows`, `borderRadiuses`, `durations`, `timingFunctions`, `colors`, `fontSizes`, `lineHeights` |
| @evilmartians/design-lint | MIT | 0.2.0 (2026-10-13) | 5 | 991 | source only (Oxlint, Tailwind v4 token use: colour, type, radius); repo made 2026-09-16 |
| Galen Framework | no licence detected by GitHub | galen-2.4.4 (2019-03-15) | 0 | — (Java) | layout specs with `css` checks; dead (last push 2022-07-15) |
| ProjectVisBug | Apache-2.0 | — | — | — | archived (GitHub `archived: true`); an inspector, not a checker |

What each one checks that touches a §3 rule:
- **Lighthouse.** `core/audits/seo/font-size.js` (the "legible font sizes" computed-style audit) was **removed on 2025-09-25** (commit 12ef593a, "core: remove font-size audit (#16701)"). The `font-display-insight` audit wraps Chrome's trace insight `FontDisplay.ts` (devtools-frontend). That insight fails a remote font whose `font-display` matches `/^(block|fallback|auto)$/` **and** that wasted time on that load. The value test is exactly the house rule (`swap` or `optional`); the "wasted time > 0" gate means a fast or cached load passes a bad value. A direct read is simpler: each `FontFace` in `document.fonts` has a `display` attribute (CSS Font Loading IDL, `attribute CSSOMString display`).
- **axe-core `link-in-text-block`.** It passes a prose link that differs from its text by 3:1, or by a style (the `link-in-text-block-style` check reads computed style). It does not read the underline offset or test the offset against descenders. The vault's check-access.py already holds this criterion (`vault.colour-script`).
- **Alfa SIA-R75** "font-size-above-minimum": passes at computed `font-size` **≥ 9 px**. SIA-R62 links distinguishable (like axe's rule). SIA-R80 line height in relative units. So Alfa does run a cascade outside the browser, but its style rules are accessibility floors far below house values.
- **IBM `style_focus_visible`** compares the `:focus` rule's `outline`/`border` from stylesheets with the normal style: a source-plus-style heuristic. **`style_highcontrast_visible`** returns `Manual_1`, a manual check. Neither tests the house form rule.
- **designlang** is the only tool found that reads design values (not accessibility) off a live page in Playwright. Its `lint` reads a token *file* it wrote, with its own thresholds: `color-sprawl` (pairs "within 8 RGB units", not ΔE00), `shadow-sprawl` (more than **6** shadow tokens; the house says about 3, named by role), `radius-sprawl` (more than 4–6), `spacing-scale-inconsistent` (ratio variance). Its extractors (`src/extractors/shadows.js` buckets shadows into levels "within 25% of the previous bucket's weight"; `spacing.js` detects a base unit; `interaction-states.js` records hover deltas) show the method works. Risks: one author made 388 of the commits, the repo is six months old (created 2026-04-15), 47 releases in that time, 790 downloads a week, and it bundles an MCP SDK, pdf-lib and pixelmatch.
- **Search bound.** `gh search repos` for "design lint", "design-system-audit", "getComputedStyle design tokens", "computed style lint puppeteer design" and three more phrasings found nothing else above 13 stars that checks design values on computed style.

### F9. Why a source-file linter cannot judge most of these rules

Every linter in F2–F4 parses the authored source (PostCSS, a JS AST or a token file). The vault judges a candidate as rendered: the measuring scripts take `<url or file>` (`check-layout.py` USAGE) and load it in Chromium at many widths. Six facts set what a linter can see:
1. **No DOM, so no cascade.** A linter does not know which elements a selector matches, nor which declaration wins. A rule about "the element that floats" or "the card's child" has no subject in source.
2. **No `var()` resolution.** A custom property's value depends on where in the DOM it is set. Token linters prove "a variable is used", never its value on this element.
3. **No width.** A linter sees all `@media` and `@container` branches and every `clamp()`/`vw` value, but not which applies at 320 px or 1440 px.
4. **No state.** `:hover`, `:active`, `:focus-visible`, an open modal, a running transition exist only in the browser.
5. **No relation.** Radius nesting, fill step against the parent ground, status colour against the action colour, link against its text: each compares two rendered things.
6. **Not all style is in a stylesheet.** Inline `style`, utility classes in HTML, CSS-in-JS, JS animations (Web Animations API, GSAP), `FontFace` objects and third-party font CSS never reach a stylesheet linter. A candidate URL may be a project's dev server in any framework, so the source may not be at hand.

A linter still judges what leaves no trace in the render: **how a value was made** (never HSL or `darken()`), and **whether an authored fallback exists** (a `@media (prefers-reduced-motion)` override, a `font-display` descriptor in `@font-face`). For the rest, the browser primitives in F7 plus Playwright's `emulate_media` (`reduced_motion` since v1.12, `forced_colors` since v1.15, `contrast` since v1.51; Playwright Python API docs) and CDP `Emulation.setEmulatedMedia` (any `{name, value}` media feature, so also `prefers-reduced-transparency`) give a script each input. CSS Color Adjust 1 says that in forced-colours mode "box-shadow and text-shadow compute to none", so a `box-shadow` focus ring vanishes there: the forced-colours half of the focus rule is an **outcome** test (emulate `forced_colors="active"`, re-run the focus pixel delta check-access.py already has), not a form test.

## Per-rule list (rule → what can check it)

Key: **Linter** = a source-file linter can judge it. **Computed** = needs a computed-style (or DOM, geometry, state) read in the browser; no linter does it. **Judgement** = a part that needs an eye or a house value no source sets. "Method from" names code or logic worth borrowing, not a dependency.

1. **Radius nesting** (inner = max(R − p, fallback); flush photo shares the outer radius or the card clips) → **Computed.** Needs parent and child `border-radius`, the parent's padding resolved to px at each width, the child's inset from `getBoundingClientRect`, and the parent's `overflow`. No linter or token tool relates parent to child. Judgement: the fallback value is the project's. Tool: none; a short script.
2. **Shadow only on what floats or acts** (no shadow on a static part; offset and blur, never a zero-offset glow; never hairline border plus wide soft shadow at rest) → **Computed** for "static or floating" (`position`, top-layer/dialog/popover role, parts-map's actable map). **Linter, partial**: a zero-offset glow can be found in source by a value regex, but not on shorthands set through `var()`. Computed `box-shadow` serialises with explicit offsets, so the glow test is exact there. Judgement: "one card that must look pressable" exception.
3. **Shadow levels** (about three, each named by role, each a token) → **Computed** count of distinct computed `box-shadow` on visible elements at each width and in forced hover state. **Linter, partial**: Project Wallace counts unique `boxShadows` in source (counts unused rules, misses inline and JS); strict-value / `primer/box-shadow` / `design-token/box-shadow` prove a variable is used in source. "From a token" per rendered element: CDP `getMatchedStylesForNode` shows the authored `var()`. Judgement: mapping each level to a role (rest, hover, overlay). Method from: designlang `src/extractors/shadows.js` (buckets by weight).
4. **Hover and press** (small part changes colour, never shadow; press goes down, never up) → **Computed.** CDP `CSS.forcePseudoState` (`:hover`, `:active`) and a computed-style diff: shadow blur and offset, `transform` scale, lightness. No linter knows a part's rendered size. Judgement and research gap: no source sets the size below which a part is "small". Method from: designlang `interaction-states.js`.
5. **Focus ring form** (`box-shadow` ring keeps `outline: <w> solid transparent`; text input: outside 2 px ring or ≥ 2 px border 3:1 from rest, never only a recoloured thin border) → **Computed**, best as an outcome: Tab to each part (check-access.py already does), read computed `outline-*`, `box-shadow`, `border-width` against the rest state; then emulate `forced_colors="active"` and re-run the focus delta. **Linter, near miss**: @double-great `no-outline-none` accepts the house form but never requires the transparent outline; a custom stylelint rule could require it inside one `:focus` block only. Judgement: none; AAA half relaxable by the project.
6. **One scrim token** (one colour and alpha, 32–70%) → **Computed**, after opening each modal: read the scrim element's (or `dialog::backdrop`'s) computed background and alpha; all scrims equal, alpha in range. No linter can tell a scrim declaration from any other translucent fill. Needs the scripted opening of each modal (parts-map gives the controls).
7. **Glass with fallback** (`backdrop-filter` only on a fixed or sticky layer holding controls; solid under `prefers-reduced-transparency` and `prefers-contrast`) → **Computed**: computed `backdrop-filter` with `position` and contents (controls), then CDP `setEmulatedMedia` `prefers-reduced-transparency: reduce` and Playwright `contrast="more"`, and check `backdrop-filter: none` and an opaque background. **Linter, partial**: a custom rule could require a `@media (prefers-reduced-transparency)` override for each `backdrop-filter`, as @double-great `media-prefers-reduced-motion` does for motion; none exists. Judgement: "strong blur" has no number in the source.
8. **Fill step against border** (fill step under about 1.1:1 keeps its border; never strong border with strong fill) → **Computed**: the card's computed background composited over its parent's rendered ground, WCAG ratio (colour_space.contrast plus alpha compositing), and the border's width and colour. Judgement and research gap: "strong" border and "strong" fill have no number in surface-styling.md.
9. **Link underline offset** (offset clear of descenders; on hover a non-colour property changes) → **Computed** plus a **font metric**: computed `text-decoration-line`, `text-underline-offset`, `text-decoration-thickness`, `text-decoration-skip-ink`, the face's descender (fonttools `hhea`/`OS/2`, or `@capsizecss/unpack` `descent`) and `post.underlinePosition` for `auto`; hover half by `forcePseudoState` diff. axe-core `link-in-text-block` reads computed style but tests only presence of a non-colour cue or 3:1, not the offset.
10. **Tint chroma** (text and neutral greys at OKLCH C 0.01–0.03, up to 0.05, toward the main hue; never HSL or `darken()`) → **Computed** for the band and the hue: computed `color` of text and neutral fills, through a CSS colour parser, to `colour_space.oklch`. **Linter, full** for "never HSL": stylelint `function-disallowed-list: ["hsl", "hsla"]` (and SCSS `darken`/`lighten`) in a project repo; the render keeps no trace of how a colour was made. Judgement: the "main hue" comes from the project's rules file; the "neutral or colour" split is a chroma threshold.
11. **Status colours** (none near the action colour; one colour per status; pulse or blink only for status) → **Computed, partial**: where status is marked up (`role=status|alert`, `aria-live`), ΔE00 of its computed colour against the primary action's fill (colour_space.de2000), and `document.getAnimations()` for pulsing on non-status parts. stylelint-no-indistinguishable-colors flags every near pair in a file with no role, at ΔE00 3. **Judgement** for status parts with no markup and for "one colour per status" (meaning from text).
12. **4 px spacing step** → **Computed**: computed `margin`, `padding`, `gap` in px at each width, each a multiple of 4. **Linter, partial**: stylelint-scales `scales/space` with an enumerated list of multiples of 4 checks literals only (not `rem` at an unknown root size, `calc()`, `clamp()`, `var()`). Research gap for the founder: whether a fluid `clamp()`/`vw` space that passes through non-multiples fails the rule.
13. **16 px body floor** (unless a dense role justifies less) → **Computed**: computed `font-size` of running text at every width; check-measure.py already finds running-text lines. With the x-height variant (`rule-interactions.md`), read `1ex / font-size` in the browser (F6). Linters: @double-great `font-size-is-readable` (px/pt only, default 15), Terrazzo `a11y-min-font-size` (tokens only), Alfa SIA-R75 (computed, but ≥ 9 px). Judgement: the "dense role" exception.
14. **`font-display: swap | optional`** → **Computed, full and simplest**: `document.fonts` → each `FontFace.display` ∈ {swap, optional}. **Linter, partial**: stylelint `at-rule-property-required-list` (`{"font-face": ["font-display"]}`) plus `declaration-property-value-allowed-list` in the project repo; misses third-party font CSS and JS `FontFace`. Lighthouse `font-display-insight` uses the same value set but fails only fonts that wasted time on that load.
15. **Nav links at phone width** (four or fewer stay visible; a menu only past four) → **Computed** at a phone width: find `nav`/`role=navigation`, count its links, test each visible and in the viewport, and detect a menu toggle (`aria-expanded`). No linter sees the width or the DOM. Judgement: which nav is the primary one where markup does not say.
16. **Motion durations and tokens** (100–500 ms; exits faster than entrances; project tokens; a reduced-motion version) → **Computed**: `document.getAnimations()` after each trigger (check-flow.py already seeks Web Animations), durations in range; open then close each overlay to pair entrance and exit; `emulate_media(reduced_motion="reduce")` and re-read; tokens by CDP `getMatchedStylesForNode` on `transition-duration`. **Linter, partial**: stylelint `time-min-milliseconds` (minimum only), `carbon/motion-duration-use` and `design-token/duration` (token use in source), @double-great `media-prefers-reduced-motion` (an override exists). None sees JS animations or entrance against exit. Judgement: the "authored focal entrance" exception.

Tally: a source linter judges **one half-rule fully** (never HSL, in 10) and **8 rules partly** (2, 3, 5, 7, 12, 13, 14, 16), always on literals and only in a project repo. **All 16 need a computed-style, DOM, geometry or state read for the rendered verdict.** **12 carry a judgement, project-value or research-gap part** (1, 2, 3, 4, 7, 8, 10, 11, 12, 13, 15, 16); of these, 4, 7, 8 and 12 are research gaps (a missing number), not taste. **4 are wholly mechanical** once read in the browser (5, 6, 9, 14).

## Recommendation

Each item has a confidence range: the chance that the item is right as stated.

1. **Do not adopt a source-file linter (stylelint and its plugins, a token linter, Figma design-lint) as the answer to any gate question.** All 16 rules need the rendered page for their verdict (F9). Confidence **85–95 %**. The one place a linter earns its cost is a project repo's build lint (never HSL; `font-display` in `@font-face`; a `prefers-reduced-motion` override exists), which is project code, not the vault gate. A precedent: #103 Q2 (A) left Manta's build-time figure-ground lint (L9) to "Manta's own code" (survey §4).
2. **Build one computed-style script on the existing Playwright substrate, not adopt one.** It needs `getComputedStyle`, three CDP calls (`CSS.forcePseudoState`, `CSS.getMatchedStylesForNode`, `Emulation.setEmulatedMedia`) and Playwright's `emulate_media`, and it reuses parts-map.py (actable parts), check-measure.py (running text), check-access.py (focus walk) and check-flow.py (Web Animations). It can answer rules 5, 6, 9 and 14 wholly, and the numeric half of 1, 2, 3, 4, 7, 8, 10, 11, 12, 13, 15 and 16, under #212 Q6 (A)'s "script owed" route. Confidence **75–85 %** that this is the right substrate. No open-source tool does this for design values except designlang, which is six months old, has one main author, uses its own thresholds (6 shadow levels, 8 RGB units) and bundles unrelated parts: borrow its extractor method, not the package (confidence **70–85 %**).
3. **Keep `colour_space.py`.** Add a CSS colour parser and alpha compositing for computed colours. Adopt **coloraide** (MIT, pure Python, 24 releases in 12 months) only if candidates use `oklch()`, `color()` or `color-mix()`; otherwise about 20 lines of `rgb()`/`rgba()` parsing do. Confidence **60–75 %** (the share of candidates that use CSS Color 4 syntax is not measured).
4. **Read x-height in the browser with the `ex` unit; add no font library to the gate.** fonttools (MIT, no runtime dependencies, Python) is an optional once-per-face check that the font's `sxHeight` is real, and the source of the descender depth for rule 9. Confidence **80–90 %**.
5. **Check `font-display` by `document.fonts`, not Lighthouse.** Same value set as Lighthouse's insight, without its "wasted time on this load" condition. Confidence **85–95 %**.
6. **Add no APCA package.** apca-w3's licence is not OSI, restricts use to WCAG web content and claims patents pending; the house uses APCA only as a design aid. If the house ever scripts APCA, colorjs.io (MIT, APCA 0.0.98G) is the candidate, after a licence read. Confidence **75–90 %**.
7. **Before any script for rules 4, 7, 8 and 12, close their research gaps** (the size of a "small" part; "strong blur"; "strong" fill and border; whether fluid spacing may leave the 4 px grid). Owner: #250 names them in its table, for #202's spec to fill as research. Confidence **80–90 %** that scripting before the number exists produces a script that the gate cannot use.

Build-cost reference (from the survey §6.2, not measured here): the existing build averages about 430 script lines and 330 test lines per gate question.

## Bound

- **Read exhaustively:** the survey §3–§4; surface-styling.md and text-presentation.md in full; impeccable.md lines 60–109; house-principles.md carrier rows; colour_space.py in full; palette.py header; rule-interactions.md lines 51–58, 79, 113–152, 255–275; the npm registry and downloads records for every npm package named (week 6–12 Oct 2026); PyPI JSON for every Python package named; the README of each stylelint plugin named; the stylelint core rule list; Terrazzo's lint rule list; Lapidist's rule index; Figma design-lint's `lintingFunctions.ts` function list; Sharma's 34-pair test file (all run); the CDP `browser_protocol.json` CSS and Emulation entries used.
- **Sampled only:** rule internals (I read the files named, not every rule of axe-core, Alfa, IBM, Lighthouse, Carbon, Primer or Lapidist); designlang's README and four of its source files; Project Wallace's README metric list; colorjs.io, culori, chroma-js and coloraide by file tree and API docs, not by running them; Playwright docs for `emulate_media` and `new_cdp_session` only; the GitHub search for browser computed-style design linters used seven phrasings and stopped there.
- **Not done:** no package was installed or run against vault fixtures; no false-positive rate was measured; pypistats figures were taken as reported (coloraide's is inconsistent); the colorjs.io APCA licence question is left open.
