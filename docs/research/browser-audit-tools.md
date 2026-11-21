# design-vault#246 (map #243): open-source browser audit tools against the gate — 15 Oct 2026

**Question.** Which open-source browser audit tools (axe-core, pa11y, IBM Equal Access, Nu HTML Checker (vnu), Lighthouse / Lighthouse CI, web-vitals) measure the accessibility, load and SEO rules that the gate holds, and the rules that it leaves out? For each tool: the WCAG 2.2 AA criteria it automates, against the eight Access questions in `plugin/skills/design-critique/gate.md` and the seven criteria that #103 Q2 (A) left out (1.1.1, 1.3.1, 2.4.2, 3.1.1, 3.3.2, 4.1.2, 1.4.12); published false-positive and coverage figures; CLS and INP (`check-load.py` measures LCP only); the SEO items of design-critique §2 (heading outline, title, meta description); licence, maintenance, weekly downloads, runtime shape; configurable thresholds. End: a list per criterion, set beside the vault script that answers it today.

 Sources: primary only (tool repos, rule docs, release pages, npm registry API, W3C ACT). No package was installed.

## Findings (appended as they land)

### F1. Licence, maintenance, downloads (read 15 Oct 2026)

Sources: `https://registry.npmjs.org/<pkg>` (`dist-tags.latest`, `time`, `license`), `https://api.npmjs.org/downloads/point/last-week/<pkg>` (week 6–12 Oct 2026), GitHub REST `repos/<r>` and `search/issues` (read-only `gh api`). "Stable releases" counts only `x.y.z` versions published since 15 Oct 2025. "Issues opened / closed" counts issues (not PRs) in the same 12 months.

| Tool (npm package) | Licence | Latest (date) | Stable releases, 12 months | Weekly downloads | Issues opened / closed, 12 months; open now | Runtime shape |
|---|---|---|---|---|---|---|
| axe-core | MPL-2.0 | 4.14.0 (5 Oct 2026) | 8 (4.11.1 → 4.14.0) | 79,734,817 | 193 / 201; 404 open | One JS file (`axe.js` / `axe.min.js`), no dependencies (`dependencies: null`). You inject it into the page and call `axe.run()`. |
| @axe-core/playwright | MPL-2.0 | 4.13.0 (11 Aug 2026) | 6 | 14,281,826 | (same repo family, dequelabs/axe-core-npm) | Node wrapper for Playwright **JS**; the vault uses Python Playwright, so the vault does not need it (inject axe.min.js directly). |
| pa11y | **LGPL-3.0-only** | 10.0.0 (28 Aug 2026) | 3 | 257,460 | 13 / 16; 39 open | Node CLI/library. It drives its own **Puppeteer** (`puppeteer ^25.9.0`) and runs two runners: `axe-core ~4.13.0` and `@pa11y/html_codesniffer ^2.6.0`. Node `^22.13.0 || >=24`. |
| pa11y-ci | LGPL-3.0-only | 5.0.0 (5 Oct 2026) | 3 | 121,613 | — | Node CLI over pa11y, many URLs, CI exit codes. |
| accessibility-checker (IBM Equal Access) | Apache-2.0 | 4.0.34 (8 Sep 2026) | 20 | 29,855 | 80 / 78; 143 open | Node package; drives Puppeteer or plugs into Playwright/Selenium/Cypress. |
| accessibility-checker-engine | Apache-2.0 | 4.0.34 (8 Sep 2026) | 19 | 21,671 | (same repo) | Injectable engine script (`ace.js` family); 426 files, 25.6 MB unpacked (locale and help files), no npm dependencies. |
| vnu-jar (Nu HTML Checker) | MIT | 26.10.12 (12 Oct 2026) | 122 (almost daily builds) | 142,999 | 128 / 428; 0 open (backlog cleared) | **Java jar** (32 MB unpacked) with a small Node launcher (`bin: vnu`). Needs a Java runtime. Also runs as a web service (`validator.w3.org/nu`). Checks markup only; it does not render the page. |
| lighthouse | Apache-2.0 | 13.5.0 (18 Sep 2026) | 9 | 5,404,521 | 136 / 186; 423 open | Node CLI/library (28 dependencies, 19 MB unpacked). Drives Chrome over CDP. Uses `axe-core ^4.13.0` for its accessibility category. Node `>=22.19`. |
| @lhci/cli (Lighthouse CI) | Apache-2.0 | **0.15.1 (25 Jun 2025)** | **0** | 1,856,318 | 17 / **3**; 217 open; repo last push 27 Mar 2026 | Node CLI; **pins `lighthouse 12.6.1`** (one major version behind). Optional server (Express + DB) for history. |
| web-vitals | Apache-2.0 | 6.2.3 (5 Oct 2026) | 10 | 51,520,299 | 38 / 38; 11 open | One small JS module (1.2 MB unpacked across builds, no dependencies), runs inside the page. |

Readings:
- axe-core, Lighthouse, web-vitals, vnu and IBM Equal Access are all active (releases inside the last month or two; issues closed at about the rate they open).
- **Lighthouse CI is stalled**: no release in 16 months, it pins Lighthouse 12.6.1, 17 issues opened against 3 closed. Do not adopt it; if the vault wants Lighthouse, call `lighthouse` itself.
- **pa11y is LGPL-3.0.** Calling it as a separate CLI process is plain use. Bundling or changing its code puts LGPL duties on the plugin. It adds nothing the vault cannot get from axe-core directly, except the HTML_CodeSniffer runner (the pa11y fork `pa11y/HTML_CodeSniffer`, BSD-3-Clause; the upstream `squizlabs/HTML_CodeSniffer` had its last push in Jan 2024).
- axe-core is MPL-2.0: file-level copyleft. The plugin can ship `axe.min.js` unchanged beside its own code; only changes to axe's own files must stay MPL and public.

### F2. axe-core 4.14.0: rules per WCAG 2.2 criterion

Source: `https://raw.githubusercontent.com/dequelabs/axe-core/v4.14.0/doc/rule-descriptions.md` (generated from the rule JSON); check options from `lib/checks/<cat>/<check>.json` at tag v4.14.0; messages from `locales/_template.json`. Each rule carries `wcag<nnn>` tags. "Issue type" is `failure`, `needs review` (axe calls the result `incomplete`), or both.

axe-core has 105 rules in the doc: 61 under WCAG 2.0 A/AA, 3 under WCAG 2.1 A/AA, 1 under WCAG 2.2 A/AA, 26 best-practice, 3 AAA, 6 experimental, 5 deprecated.

Rules on the criteria in scope (tag → rules):

| WCAG criterion | axe-core rules | Issue type |
|---|---|---|
| 1.1.1 Non-text Content | `image-alt`, `input-image-alt`, `role-img-alt`, `svg-img-alt`, `object-alt`, `area-alt` (2.4.4/4.1.2), `aria-meter-name`, `aria-progressbar-name` | failure + needs review |
| 1.3.1 Info and Relationships | `list`, `listitem`, `definition-list`, `dlitem`, `td-headers-attr`, `th-has-data-cells`, `aria-required-children`, `aria-required-parent`, `aria-hidden-body`; experimental `p-as-heading`, `table-fake-caption`, `td-has-header` | mostly failure; some needs review |
| 1.4.1 Use of Color | `link-in-text-block` only (links in a text block) | failure + needs review |
| 1.4.3 Contrast (Minimum) | `color-contrast` | failure + needs review |
| 1.4.4 Resize Text / 1.4.10 Reflow | `meta-viewport` (tag wcag144, ACT b4f0c3: zoom not blocked). **No 1.4.10 reflow rule.** | failure |
| 1.4.11 Non-text Contrast | **none** | — |
| 1.4.12 Text Spacing | `avoid-inline-spacing`: fails only an inline `style` that sets letter/word spacing or line height with `!important` | failure |
| 2.1.1 Keyboard | `scrollable-region-focusable`, `frame-focusable-content`, `server-side-image-map`. **No rule that Tabs through the page.** | failure + needs review |
| 2.2.2 Pause, Stop, Hide | `blink`, `marquee` (obsolete elements only). **No rule for CSS, JS, video or canvas motion.** | failure |
| 2.4.2 Page Titled | `document-title` (title present and not empty; it cannot judge if the title describes the page) | failure |
| 2.4.7 Focus Visible | **none** | — |
| 2.4.11 Focus Not Obscured (Minimum) | **none** | — |
| 2.5.8 Target Size (Minimum) | `target-size` (checks `target-size` 24 px and `target-offset` 24 px; skips inline links) | failure + needs review |
| 3.1.1 Language of Page | `html-has-lang`, `html-lang-valid`, `html-xml-lang-mismatch` | failure |
| 3.3.2 Labels or Instructions | `form-field-multiple-labels` only (needs review). The `label` rule is tagged **4.1.2**, not 3.3.2. | needs review |
| 4.1.2 Name, Role, Value | `button-name`, `link-name`, `input-button-name`, `label`, `select-name`, `aria-*-name` (command, input-field, toggle-field, tab, tooltip), `aria-allowed-attr`, `aria-required-attr`, `aria-roles`, `aria-valid-attr(-value)`, `aria-prohibited-attr`, `aria-conditional-attr`, `aria-deprecated-role`, `aria-hidden-focus`, `nested-interactive`, `frame-title`, `frame-title-unique`, `summary-name`, `duplicate-id-aria`, `aria-braille-equivalent` | mostly failure + needs review |

SEO-type rules in axe (best-practice, not WCAG): `heading-order` ("Heading levels should only increase by one"), `page-has-heading-one`, `empty-heading`. **No meta-description rule.** `document-title` gives the title.

Thresholds and options (from the check JSON at v4.14.0). axe-core lets the caller change them per run with `axe.configure({checks:[{id, options}]})` or `axe.run(..., {checks: {...}})`:
- `color-contrast`: `contrastRatio.normal.expected 4.5`, `contrastRatio.large.expected 3`, `largeTextPt 18`, `boldTextPt 14`, `boldValue 700`, `pseudoSizeThreshold 0.25`, `ignorePseudo false`, `ignoreUnicode true`, `shadowOutlineEmMax 0.2`, `textStrokeEmMin 0.03`.
- `link-in-text-block`: `requiredContrastRatio 3`, `allowSameColor true`.
- `target-size`: `minSize 24`; `target-offset`: `minOffset 24`.

**How axe decides contrast.** axe reads computed CSS colours and stacks the elements under the text (`getBackgroundColor`). It does not read pixels. Where it cannot find one background colour it returns `incomplete` ("needs review"), not pass or fail. The `incomplete` reasons in the locale file are: `bgImage` (background image), `bgGradient` (background gradient), `imgNode` (element contains an image), `bgOverlap` (another element overlaps it), `complexTextShadows`, `fgAlpha` (text colour has alpha), `elmPartiallyObscured`, `elmPartiallyObscuring`, `outsideViewport`, `equalRatio` (1:1), `shortTextContent`, `emptyValue`, `nonBmp` (icon-font glyphs), `pseudoContent` (a `::before`/`::after` background), `colorParse`.
- `link-in-text-block` uses the same colour reading. It passes a link that has an underline, border, other font weight or style or a different background (`elementIsDistinct`), or text contrast of 3:1 against the text around it. It returns `incomplete` for a link with `::before`/`::after` content, and over background images, gradients, image nodes and overlap.

### F3. IBM Equal Access (accessibility-checker-engine 4.0.34): rules per WCAG 2.2 criterion

Source: every rule file under `IBMa/equal-access/accessibility-checker-engine/src/v4/rules/*.ts` on `master` (170 rules, read 15 Oct 2026), parsed by each rule's `rulesets` field for the `WCAG_2_2` policy; level V = `eRulePolicy.VIOLATION`, R = `RECOMMENDATION`. Messages from each rule's `messages` block. Config from the npm README of `accessibility-checker` 4.0.34.

164 rules belong to the `WCAG_2_2` policy. **64 of 170 rules never call `RuleFail`**: they can only pass or ask a person (`RulePotential`, `RuleManual`). Rules on the criteria in scope:

| WCAG criterion | IBM rules (count) | Can it fail by itself? |
|---|---|---|
| 1.1.1 | 26 (`img_alt_valid`, `img_alt_misuse`, `svg_graphics_labelled`, `img_alt_redundant`, …) | yes for most |
| 1.3.1 | 26 (tables, lists, fieldsets, `heading_markup_misuse`, `text_block_heading`, …) | yes for most |
| 1.4.1 | `style_color_misuse`, `form_font_color` | **no**: both only "Verify color is not used as the only visual means" |
| 1.4.3 | `text_contrast_sufficient` | yes; "potential" for a graphic background, a text shadow, or the same colour on both sides |
| 1.4.10 | `style_viewport_resizable` (viewport meta only) | **no** (potential only) |
| 1.4.11 | `style_highcontrast_visible` (Windows high-contrast mode) | **no** (manual); it does not measure 3:1 |
| 1.4.12 | `text_spacing_valid` (inline `!important` letter/word spacing, line height) | yes |
| 2.1.1 | 14 (`widget_tabbable_exists`, `element_scrollable_tabbable`, `iframe_interactive_tabbable`, `aria_keyboard_handler_exists`, `script_onclick_misuse`, …) | some; no rule Tabs through the page |
| 2.2.2 | `blink_css_review`, `blink_elem_deprecated`, `marquee_elem_avoid` | blink/marquee only |
| 2.4.2 | `page_title_exists`, `page_title_valid` | yes |
| 2.4.7 | `style_focus_visible`, `element_tabbable_visible`, `script_focus_blur_review` | **no**: "Check the keyboard focus indicator is visible when using CSS declaration for 'border' or 'outline'" |
| 2.4.11 | `element_tabbable_unobscured` | **no**: "Confirm that when the element receives focus, it is not covered" |
| 2.5.8 | `target_spacing_sufficient` | yes (`violation_spacing`); "potential" for an overlapped target |
| 3.1.1 | `html_lang_exists`, `element_lang_valid` | yes |
| 3.3.2 | 6 (`input_label_before`, `input_label_after`, `input_label_visible`, `input_placeholder_label_visible`, `fieldset_label_valid`, `element_accesskey_labelled`) | mixed |
| 4.1.2 | 30 (`input_label_exists`, `aria_*`, `combobox_*`, `frame_title_exists`, …) | yes for most |

IBM is the only one of the six tools with a rule for each of 2.4.7, 2.4.11, 1.4.11 and 1.4.10, but each of these four rules returns only "potential" or "manual".

Thresholds: **not configurable per rule**. `.achecker.yml` sets `ruleArchive` (`latest`, `versioned`, or a dated archive id), `policies` (`IBM_Accessibility`, `WCAG_2_2`, …), `failLevels` and `reportLevels` (violation, potentialviolation, recommendation, potentialrecommendation, manual). The default `ruleArchive: latest` fetches the rules at run time from a rule server (the README names `cdn.jsdelivr.net` and `able.ibm.com/rules`) and caches `ace-node.js` and `archive.json` in `cacheFolder`. For a repeatable gate, pin a dated archive or inject the engine file from `accessibility-checker-engine` directly.

### F4. pa11y 10.0.0 and its HTML_CodeSniffer runner

Sources: pa11y README in the npm registry entry for 10.0.0; `pa11y/HTML_CodeSniffer` repo (the fork pa11y uses, `@pa11y/html_codesniffer ^2.6.0`, last commit 14 Jan 2026), sniff files under `Standards/WCAG2AAA/Sniffs/`, counted for `HTMLCS.ERROR` / `WARNING` / `NOTICE` calls.

- pa11y is a wrapper. It runs `htmlcs` (default) or `axe` (or both) in its own Puppeteer browser. It adds no rule of its own. With `--runner axe` its verdicts are axe-core 4.13's verdicts (F2).
- **pa11y ignores warnings and notices by default** (`includeWarnings: false`, `includeNotices: false`). Only `error` results fail a run.
- `--threshold <n>` is an **error count** ("permit this number of errors, warnings, or notices"), not a measurement threshold. `ignore` takes rule codes. `--level-cap-when-needs-review` (axe runner only, default `error`) sets what axe's "incomplete" becomes. **No option changes a contrast ratio or a target size.**
- HTML_CodeSniffer has a sniff file for each WCAG 2.0/2.1 criterion, but **no file for 2.4.11 or 2.5.8** (WCAG 2.2). On the criteria in scope, the sniff can raise an ERROR only on 1.1.1 (13 call sites), 1.3.1 (20), 1.4.3 (1), 2.2.2 (1), 2.4.2 (3), 3.1.1 (3) and 4.1.2 (3). 1.4.1, 1.4.11, 1.4.12, 2.4.7 and 3.3.2 raise only a NOTICE ("check this by hand"); 1.4.10 and 2.1.1 raise only WARNINGs.
- HTMLCS 1.4.3 also reads computed CSS colours. It raises a WARNING, not an ERROR, where the text has a background image (`.BgImage`), alpha (`.Alpha`) or absolute position (`.Abs`).

### F5. Nu HTML Checker (vnu-jar 26.10.12)

Sources: `validator/validator` `src/nu/validator/client/SimpleCommandLineValidator.java` (flags), `src/nu/validator/checker/HeadingHierarchyChecker.java`, `TextContentChecker.java`, `LanguageDetectingChecker.java`, `schematronequiv/Assertions.java` on `main`; the vnu-jar npm README; GitHub commit history of `HeadingHierarchyChecker.java`.

- vnu checks markup against the HTML, ARIA-in-HTML, CSS and SVG specs. It parses the served source; **it does not render the page or run scripts**, so it checks no colour, size, focus, keyboard or motion criterion, and it does not see DOM that JavaScript builds.
- Messages on the criteria in scope:
  - 1.1.1: error "An “img” element must have an “alt” attribute, except under certain conditions" (presence only, not quality).
  - 2.4.2: an HTML document without `<title>` is a content-model error; `TextContentChecker` also errors "Element “title” must not be empty."
  - 3.1.1: `LanguageDetectingChecker` **warns** when `<html>` has no `lang`, or when its `lang` does not match the language it detects in the text ("This document appears to be written in …"). That is a check of the **value** of `lang`, which axe and IBM do not do. `--no-langdetect` turns it off.
  - 4.1.2 / 1.3.1 in part: ARIA role and attribute conformance errors (role allowed on element, required owned elements); table structure (`TableChecker`).
  - **Heading outline**: since 1 Jan 2026 (`HeadingHierarchyChecker`, "Add heading-hierarchy checker (for reporting “skipped” levels)") vnu **errors** on a heading that skips a level ("follows the heading … skipping N heading level(s)"), and since 8 May 2026 it **warns** when headings exist but none is at computed level 1. `TextContentChecker` warns "Empty heading."
  - No meta-description check (the HTML spec does not require one).
- Flags: `--errors-only`, `--Werror`, `--filterfile`, `--filterpattern`, `--skip-info-messages`, `--also-check-css`, `--also-check-svg`, `--no-langdetect`, `--format`, `--exit-zero-always`, and others. No measurement threshold exists to set; you filter messages by regex.
- Runtime: a Java jar. **The npm package's `postinstall` script installs a local Java runtime into `node_modules/.cache/vnu-jar/java/` when it finds no `java` command.** That is a large install-time download, which AGENTS.md's dependency check must weigh. Alternative: the public service `validator.w3.org/nu` (sends the page off the machine) or the Docker image.

### F6. Lighthouse 13.5.0 and Lighthouse CI 0.15.1

Sources: `GoogleChrome/lighthouse` at tag v13.5.0: `core/config/default-config.js`, `core/config/constants.js`, `core/gather/gatherers/accessibility.js`, `core/audits/accessibility/axe-audit.js`, `core/audits/metrics/{cumulative-layout-shift,interaction-to-next-paint,largest-contentful-paint}.js`, `core/audits/seo/meta-description.js`, `changelog.md`; `GoogleChrome/lighthouse-ci` `docs/configuration.md`.

- **Accessibility category = a subset of axe-core.** The gatherer calls `axe.run` with `runOnly` tags `wcag2a`, `wcag2aa`, plus a list of rules turned on or off by hand (on: `heading-order`, `empty-heading`, `landmark-one-main`, `link-in-text-block`, `target-size`, …; off: `area-alt`, `blink`, `marquee`, `nested-interactive`, `scrollable-region-focusable`, `role-img-alt`, `summary-name`, `frame-focusable-content`, `server-side-image-map`, `no-autoplay-audio`, `aria-tab-name`, …). It adds **no WCAG check of its own**. 10 further accessibility items (`focusable-controls`, `logical-tab-order`, `focus-traps`, `visual-order-follows-dom`, …) are manual checklist items with weight 0.
- **Important verdict difference.** `axe-audit.js` builds failures from `violations` only (it adds `incomplete` only for informative-weight rules). It returns an axe `incomplete` with an `error` as an error. **For `color-contrast` and `link-in-text-block`, an axe "needs review" (text over an image or gradient, overlap, pseudo-element) is not a failure in Lighthouse**: the element does not show and the audit can pass.
- **Performance.** Navigation mode measures FCP, LCP, TBT, **CLS** (weight 25) and Speed Index. **INP is `supportedModes: ['timespan']`**: a normal page-load run gives no INP; you must script interactions in a user-flow timespan. Default `throttlingMethod: 'simulate'` (Lantern model); check-load.py applies the same constants as real "devtools" throttling instead (`check-load.py:15-18`). Score curves (log-normal p10 / median): LCP mobile 2500 / 4000 ms, CLS 0.1 / 0.25, INP 200 / 500 ms. The audit `options` (`p10`, `median`) can be overridden in a custom config, but these change only the 0–1 **score**, not a pass line.
- **SEO category** (navigation/snapshot): `is-crawlable`, `document-title`, **`meta-description`** (present and not empty; no length check), `http-status-code`, `link-text` (generic link text like "click here"), `crawlable-anchors`, `robots-txt`, `image-alt`, `hreflang`, `canonical`, `structured-data` (manual). **No heading-outline audit in SEO**; `heading-order` sits in the accessibility category (axe best-practice). No check that the `h1` matches the page.
- **Thresholds.** Lighthouse itself has **no pass/fail**: it gives scores. **Performance budgets were removed in Lighthouse 12.0.0 (22 Apr 2024, PR #15950).** Pass lines need Lighthouse CI assertions (`minScore`, `maxNumericValue`, `maxLength` per audit, e.g. `cumulative-layout-shift: ["error", {maxNumericValue: 0.1}]`) or the caller's own code reading `numericValue` from the JSON.

### F7. web-vitals 6.2.3

Sources: the web-vitals README in the npm registry entry for 6.2.3 (sections "Rating Thresholds", "Browser Support", "Limitations", "reportAllChanges").

- One small script, injectable as an IIFE (`dist/web-vitals.iife.js`) or ES module; no dependencies. Functions `onCLS`, `onINP`, `onLCP`, `onFCP`, `onTTFB`; an attribution build names the element behind each value.
- Exported rating thresholds: `CLSThresholds [0.1, 0.25]`, `INPThresholds [200, 500]` ms, `LCPThresholds [2500, 4000]` ms. The library gives each value a `rating`; the caller compares `value` to any line it wants, so **thresholds are the caller's**.
- **CLS: Chromium only** (`onCLS()`: Chromium). The vault's Playwright Chromium has it. **INP needs real input**: it reports only after an interaction, and CLS and INP report when the page's `visibilityState` changes to hidden (or with `reportAllChanges: true`). A lab script must click/tap/type and then hide the page or read with `reportAllChanges`.
- Limitation in the README: the APIs do not see into `<iframe>` content, even same-origin; with iframes, `onCLS` measures document CLS only.
- web-vitals measures **no accessibility or SEO item**.
- Fit with the vault: the Layout Instability and Event Timing APIs it wraps are browser APIs. check-load.py already reads LCP from `PerformanceObserver` in Python Playwright; CLS is the same `PerformanceObserver({type:'layout-shift'})` read, with session windows (a gap under 1 s, a window under 5 s: `web-vitals/src/lib/LayoutShiftManager.ts:38-39`; `check-load.py:77-84` reads LCP the same way). The library's value is the tested session-window and INP percentile logic, not access to the data.

### F8. Published coverage and false-positive figures

1. **Deque, "Automated accessibility testing coverage"** (`deque.com/automated-accessibility-testing-coverage/`, announced 10 Mar 2021). Sample: more than 2,000 first-time audits, 13,000+ pages or page states, 294,958 issues, WCAG 2.0/2.1 A and AA, HTML pages only, axe-core rules only (not Intelligent Guided Testing). **57.38% of issues** were found by the automated tests. By success criteria: issues found automatically on **16 of 50** WCAG 2.1 AA criteria (32%). The figure counts **issues**, and 1.4.3 is 30.08% of all issues, so contrast carries much of the 57%. The axe-core README (v4.14.0, line 19) repeats "on average 57% of WCAG issues automatically". Automated share by criterion (from Deque's Table 1, read through WebFetch; check against the page before quoting further):

   | Criterion | Share of all issues | Share found automatically |
   |---|---|---|
   | 1.4.3 Contrast | 30.08% | 83.11% |
   | 4.1.2 Name, Role, Value | 16.37% | 54.42% |
   | 1.3.1 Info and Relationships | 12.33% | 45.17% |
   | 1.1.1 Non-text Content | 8.04% | 67.57% |
   | 3.1.1 Language of Page | 0.74% | 91.81% |
   | 2.4.2 Page Titled | 0.75% | 11.26% |
   | 3.3.2 Labels or Instructions | 0.86% | 20.42% |
   | 1.4.1 Use of Color | 1.26% | 12.17% |
   | 2.1.1 Keyboard | 3.19% | 2.49% |
   | 1.4.11 Non-text Contrast | 1.54% | **0.00%** |
   | 2.4.7 Focus Visible | 2.48% | **0.00%** |
   | 1.4.12 Text Spacing | (672 issues) | 15 of 672 (≈2%) |

   This is a vendor study on its own metric, with no independent repeat. It shows the six criteria the vault measures by pixel or by Tab walk (1.4.11, 2.4.7, 2.1.1, 1.4.1, and 2.4.11/2.5.8, which postdate it) are the ones where axe finds almost nothing.
2. **False positives.** axe-core's manifesto (README v4.14.0, line 69): "It returns zero false positives (bugs notwithstanding)." axe gets this by sending doubtful cases to `incomplete` instead of `violations`. Deque's study "exclude[s] false positives" and incomplete results from its count. **No tool publishes a measured false-positive rate on real pages.**
3. **W3C ACT implementation reports** (`w3.org/WAI/standards-guidelines/act/implementations/`, read 15 Oct 2026; versions as the pages state them): axe-core 4.10.2 consistent on 26 WCAG ACT rules + 3 proposed; IBM Equal Access 3.1.42-rc.0 on 21 + 2 (its own page lists 27 rules, results updated 20 Jul 2026); Alfa 0.118.0 on 27 + 3; QualWeb 3.0.0 on 23 + 9. On the contrast rule `afw4f7` both axe and IBM are "consistent", but **each returns "cannot tell" on some test cases** (axe: 7 examples; IBM: 6 of 32). IBM is only "partially consistent" on `23a2a8` (image has accessible name: it marks one failed example inapplicable). In the parts read (axe page: first 100,000 of 140,616 characters; IBM page: all), neither report lists an ACT rule for 1.4.11, 2.4.7, 2.4.11 or 2.5.8.
4. **UK GDS tool audit** (`alphagov.github.io/accessibility-tool-audit/`, last updated 13 Apr 2018; 143 planted barriers): all 13 tools together found 71%; 29% were found by none. Barriers found: SortSite 40%, Tenon 34%, AChecker 31%, WAVE 30%, **aXe 29%**, Siteimprove 29%, **HTML_CodeSniffer 20%**, Google ADT 17%, **Nu Html Checker 13%**. Lighthouse, IBM and pa11y were not in it. Old versions; useful only as an order of size: one tool finds about a third of planted barriers.

### F9. Where a tool's verdict can differ from the vault script's

The vault scripts read **pixels** and **drive the keyboard**; axe, Lighthouse, pa11y/HTMLCS and IBM read **computed CSS** and the DOM. So:

| Gate question | Vault script (method) | Tool verdict that differs, and why |
|---|---|---|
| vault.contrast (1.4.3) | check-access.py: screenshot with text hidden, glyph mask, worst pixel (F83) | **Text over a photo, gradient, overlapping box or `::before` background**: axe → `incomplete` (`bgImage`, `bgGradient`, `bgOverlap`, `pseudoContent`); **Lighthouse → pass** (it drops axe's incomplete for this audit); pa11y/HTMLCS → WARNING, hidden by default → **pass**; IBM → "potential" (lightest/darkest of the background, by hand). The vault gives a number. **Text with `fgAlpha`** (semi-transparent text colour): axe incomplete; vault measures the blended pixels. **Thin or light-weight fonts, anti-aliasing**: axe uses the declared colour, so it can pass text whose drawn glyph pixels are lighter; the vault's worst-pixel reading can fail it — the vault is stricter here, and #197 tunes `WORST_SHARE`. **Icon fonts / non-BMP glyphs**: axe skips (`ignoreUnicode: true`, `nonBmp`); vault measures them as text. **Large-text line**: axe `largeTextPt 18` / `boldTextPt 14` with `boldValue 700` = the vault's 24 px / 18.66 px bold; the same. |
| vault.control-edges (1.4.11) | check-access.py: edge and fill pixels 2 px out / 3 px in | No tool measures it. IBM's only 1.4.11 rule is a manual Windows-high-contrast prompt. Deque: 0% automated. |
| vault.target-size (2.5.8) | check-access.py: 24 px, or 12 px circle spacing; inline-link and UA-default exceptions | axe `target-size` + `target-offset` use the same 24 px; skip inline (`widget-not-inline-matches`). axe returns `incomplete` for overflow content, negative-tabindex parts and `tooManyRects`; Lighthouse drops those as passes. Whether axe applies the user-agent-default exception was **not checked**. IBM `target_spacing_sufficient` has explicit `pass_default` (UA default) and `pass_inline`. Close agreement is likely; differences sit in overlap and obscured cases. |
| vault.colour-script (1.4.1, G183) | check-access.py: underline/overline, bottom border, outline or shadow **in a colour that shows**, a background **other than the one behind it**, bold vs regular, italic; else 3:1 against the text | axe `link-in-text-block-style` (`elementIsDistinct`) passes **any** `background-image` other than none, **any** top/bottom border or outline with width > 0 and alpha ≠ 0 (even if it matches the background), a different **first font family**, a different **font-size**, any `font-weight` difference (500 vs 400), and any `text-decoration-style` difference. axe's 3:1 text check matches (`requiredContrastRatio 3`). axe → incomplete for pseudo-content and background images. |
| vault.colour-look (1.4.1) | look critics | No tool. IBM `style_color_misuse` only prompts. Deque: 12% automated. |
| vault.keyboard (2.1.1) | check-access.py: Tab and Shift+Tab walk; every pointer-actable part (incl. React handlers) must be reached | axe has no Tab walk: only `scrollable-region-focusable` and `frame-focusable-content` (Lighthouse turns **both off**). A `<div onclick>` that Tab skips passes axe. IBM `script_onclick_misuse`, `aria_keyboard_handler_exists`, `widget_tabbable_exists` catch part of this from the DOM, without pressing Tab. Deque: 2.49% automated. |
| vault.focus (2.4.7, 2.4.11) | check-access.py: pixel change ≥3:1 between focused and blurred shots; 9-point opacity test for "obscured" | axe: no rule. IBM: `style_focus_visible` / `element_tabbable_visible` / `element_tabbable_unobscured` return only "potential". HTMLCS: notice. Deque: 0% automated (2.4.7). |
| vault.pause (2.2.2) | check-access.py: CSS/WAAPI animations and videos > 5 s need a named pause control | axe/IBM/HTMLCS check only `<blink>`/`<marquee>`/CSS `text-decoration: blink`; Lighthouse turns axe's `blink` and `marquee` off. No tool watches running motion. |
| vault.reflow (1.4.10) | check-layout.py: 320–2560 px sweep for sideways scroll, clipping, overlap; viewport meta and zoom (ACT b4f0c3) | axe `meta-viewport` (tag 1.4.4, ACT b4f0c3) = the vault's viewport-zoom half, same ACT rule. No tool sweeps widths. IBM `style_viewport_resizable` prompts only. |
| vault.load (LCP) | check-load.py: real load under Lighthouse's mobile constants, median of 3, ≤ 2500 ms | Lighthouse default `throttlingMethod: 'simulate'` estimates LCP from an unthrottled trace, so it can differ (check-load.py's own header says so). web-vitals `onLCP` = the same `PerformanceObserver` data check-load.py reads. |

### F10. Per-criterion list: which tool covers it, beside the vault script

Key: **Full** = the tool gives pass/fail on the mechanical test the gate (or the criterion) asks, with no person. **Part** = it gives pass/fail on part of the test, or sends the hard cases to "needs review". **Review** = it only prompts a person. **None** = no rule. pa11y is listed with its default runner (HTMLCS) and default levels; `pa11y --runner axe` = the axe column. Lighthouse = axe subset with incomplete dropped (F6).

**The gate's Access questions (gate.md) and vault.reflow:**

| Criterion (gate question) | axe-core | Lighthouse | pa11y (HTMLCS) | IBM Equal Access | vnu | web-vitals | Vault today |
|---|---|---|---|---|---|---|---|
| 1.4.3 Contrast (vault.contrast) | Part (CSS colours; incomplete over images, gradients, overlap, pseudo, alpha) | Part, weaker (incomplete = pass) | Part (bg-image cases are hidden warnings) | Part (graphic background → potential) | None | None | **check-access.py**, pixels, F83 worst pixel |
| 1.4.11 Non-text Contrast (vault.control-edges) | None | None | None (notice) | Review (high-contrast-mode prompt) | None | None | **check-access.py** |
| 2.5.8 Target Size (vault.target-size) | Full (24 px + offset 24; incomplete on overflow/obscured) | Full, weaker (incomplete = pass) | None (no 2.2 sniff) | Full/Part (`violation_spacing`; overlap → potential) | None | None | **check-access.py** |
| 1.4.1 Use of Color, links (vault.colour-script) | Part (looser cue list, F9) | Part | Review (notice) | Review | None | None | **check-access.py** (G183) |
| 1.4.1 Use of Color, other meaning (vault.colour-look) | None | None | Review | Review | None | None | look critics |
| 2.1.1 Keyboard (vault.keyboard) | Part (scroll regions, iframes, image maps; no Tab walk) | None (both rules off) | Review (warnings hidden) | Part (DOM handler and tabbable rules; no Tab walk) | None | None | **check-access.py**, Tab/Shift+Tab walk |
| 2.4.7 Focus Visible (vault.focus) | None | None | Review (notice) | Review (potential) | None | None | **check-access.py**, pixel delta ≥3:1 |
| 2.4.11 Focus Not Obscured (vault.focus) | None | None | None | Review (potential) | None | None | **check-access.py**, 9-point cover test |
| 2.2.2 Pause, Stop, Hide (vault.pause) | Part (`blink`, `marquee` only) | None (both off) | Part (blink only) | Part (blink, marquee only) | None | None | **check-access.py** (CSS/WAAPI/video) |
| 1.4.10 Reflow (vault.reflow) | None (`meta-viewport` is the 1.4.4 zoom half) | None | Review (warnings) | Review (viewport prompt) | None | None | **check-layout.py**, 320–2560 px sweep + ACT b4f0c3 |

**The seven criteria #103 Q2 (A) left out:**

| Criterion | axe-core | Lighthouse | pa11y (HTMLCS) | IBM Equal Access | vnu | Vault today |
|---|---|---|---|---|---|---|
| 1.1.1 Non-text Content | Part (name present: `image-alt`, `svg-img-alt`, `role-img-alt`, `input-image-alt`, `object-alt`; Deque 67.6% of issues) | Part | Part (13 error sites) | Part (26 rules, incl. decorative misuse) | Part (`alt` present) | **none** (no question; critic prose only) |
| 1.3.1 Info and Relationships | Part (lists, tables, ARIA parents/children; Deque 45.2%) | Part | Part (20 error sites) | Part (26 rules) | Part (tables, ARIA owned) | **none** |
| 2.4.2 Page Titled | Full for "present and not empty" (`document-title`); "describes the page" needs a person (Deque 11.3%) | Full (same) | Full (presence) | Full (`page_title_exists`, `page_title_valid`) | Full (presence, not empty) | **none** |
| 3.1.1 Language of Page | Full (`html-has-lang`, `html-lang-valid`, mismatch; Deque 91.8%) | Full | Full | Full | Full + **wrong-language detection** (warning) | **none** |
| 3.3.2 Labels or Instructions | Part, weak (`form-field-multiple-labels`, review only; `label` is filed under 4.1.2) | Part, weak | None (notice) | Part (visible label, placeholder-only label, label position: 6 rules) | None | **none** |
| 4.1.2 Name, Role, Value | Part (≈25 rules; Deque 54.4%) | Part (Lighthouse turns off `nested-interactive`, `summary-name`, `aria-tab-name`) | Part | Part (30 rules) | Part (ARIA conformance) | **none** (parts-map.py maps roles, answers vault.one-target only) |
| 1.4.12 Text Spacing | Part (inline `!important` only; ACT 24afc2/9e45ec/78fd32) | None (rule not in LH list) | None (notice) | Part (same three ACT rules) | None | **none** |

**Load and SEO:**

| Item | axe-core | Lighthouse | IBM / pa11y / vnu | web-vitals | Vault today |
|---|---|---|---|---|---|
| LCP ≤ 2.5 s (vault.load) | — | Full (simulated by default; score, no pass line) | — | Full (real; Chromium/Firefox/Safari) | **check-load.py** |
| CLS ≤ 0.1 | — | Full on page load (navigation mode) | — | Full (Chromium only; reports on hide or `reportAllChanges`) | **none** |
| INP ≤ 200 ms | — | Part (timespan/user-flow mode only) | — | Full only with scripted input | **none** |
| `<title>` present | `document-title` | `document-title` (a11y + SEO) | all three | — | **none** (critic, SKILL.md §2 SEO) |
| Meta description present | None | **`meta-description`** (present, not empty; no length check) | None | — | **none** |
| Heading outline: no skipped level | `heading-order` (best-practice) | `heading-order` (a11y category) | IBM `heading_markup_misuse` only asks a person to "Verify that the heading element is a genuine heading" (no order check); vnu **errors** on a skip (since 1 Jan 2026) | — | **none** |
| Heading outline: an `h1` exists | `page-has-heading-one` (best-practice; not in Lighthouse) | None | vnu warns if no level-1 heading (since 8 May 2026) | — | **none** |
| `h1` promise matches the page | None | None | None | — | critic (stays judgement) |

## Recommendation

Priced as the probability that each is right for the vault, from the evidence above.

1. **Keep every current Access script; no tool replaces one.** No tool measures 1.4.11, 2.4.7, 2.4.11, running motion (2.2.2), a Tab walk (2.1.1) or a width sweep (1.4.10); Deque's own figures put 1.4.11 and 2.4.7 at 0% automated. On 1.4.3 and 1.4.1 the CSS-reading tools send exactly the hard cases (images, gradients, overlap) to "needs review", or (Lighthouse, pa11y defaults) to a silent pass. **Confidence 85–95%.**
2. **Adopt axe-core for the left-out criteria: 1.1.1, 1.3.1, 2.4.2, 3.1.1, 4.1.2, plus the SEO items `document-title`, `heading-order`, `page-has-heading-one`.** Ship `axe.min.js` 4.14.0 (652,140 bytes, no dependencies, MPL-2.0, which allows shipping the file unchanged) in the plugin, and inject it through the Python Playwright the scripts already use. This removes #163's packaging blocker ("no `node_modules`"). Map `violations` → fail, `incomplete` → the look critics (the gate's existing "cannot measure" route), `passes`/`inapplicable` → pass. **Confidence 70–85%** that axe is the right engine (most active, most used, zero-false-positive policy, ACT-consistent on 26 rules). Risk: the AGENTS.md dependency check and pinning (axe ships 8 stable releases a year); rule behaviour changes per release, as with the impeccable pin.
3. **Shortlist for #249's side-by-side run: axe-core (direct), IBM Equal Access engine (`ace.js`, 685,148 bytes, Apache-2.0), and Lighthouse 13.5 for CLS and the SEO category only.** IBM is the only tool with real 3.3.2 rules (placeholder-only label, visible label: a house rule in `impeccable.md:101-110`) and broader 1.3.1 rules; pin a dated `ruleArchive` or inject the engine file, never `latest`. Run all three on #238's planted-fault kit and on the check-access fixtures (`test/fixtures/access/`), and count where each disagrees with check-access.py (F9 lists the expected disagreements). **Confidence 65–80%** that this shortlist is enough.
4. **Do not adopt pa11y, Lighthouse CI or vnu as gate engines.** pa11y adds only HTMLCS (WCAG 2.0/2.1 sniffs, no 2.2, errors overlap axe) under LGPL-3.0, and its defaults hide warnings. Lighthouse CI is stalled (last release Jun 2025, pins Lighthouse 12.6.1). vnu reads source only, needs Java (its postinstall downloads a runtime), and adds just heading-skip errors and wrong-`lang` detection; a vault script can do the heading part with one DOM walk. **Confidence 70–85%.**
5. **Build CLS into check-load.py; do not adopt Lighthouse for it.** check-load.py already reads LCP from `PerformanceObserver`; CLS is the `layout-shift` entry type with the session-window rule in `web-vitals/src/lib/LayoutShiftManager.ts:38-39` (or inject `web-vitals.iife.js`, 8,991 bytes, Apache-2.0). Line 0.1, as web-vitals and Lighthouse use. **Confidence 75–85%.** INP needs scripted taps on each actable part (parts-map.py already lists them); worth it only for a candidate with real interaction. **Confidence 40–60%**; leave it to #250.
6. **Meta description: a three-line DOM check in a vault script, not Lighthouse.** Lighthouse's audit checks presence and non-empty only. **Confidence 75–90%.**
7. **1.4.12 Text Spacing: build, not adopt.** axe and IBM check only inline `!important` spacing. The real test is to inject WCAG 1.4.12's spacing (line height 1.5, paragraph spacing 2× font size, letter spacing 0.12×, word spacing 0.16×) and re-run check-layout.py's clipping and overlap detection. **Confidence 65–80%** that this reuse works without a new detector.

Gap for the founder: none from this research. Whether axe's `incomplete` goes to the look critics or fails the page is a rule choice for #250, not a fact this research can settle.

**Bound.** Read exhaustively: the npm registry entries and last-week downloads of all 11 packages; GitHub repo state and 12-month issue counts for 7 repos; axe-core 4.14.0 `doc/rule-descriptions.md` (all 105 rules), `locales/_template.json` for 4 checks, the check JSON of 5 checks, `link-in-text-block(-style)-evaluate.js` and `element-is-distinct.js`; all 170 IBM rule files (parsed by script for `WCAG_2_2` ruleset mapping and `RuleFail` use) and the `accessibility-checker` README config; 15 HTML_CodeSniffer sniff files (counted ERROR/WARNING/NOTICE calls only, not read line by line); vnu CLI flags and 3 checker files; Lighthouse 13.5.0 `default-config.js` categories, the accessibility gatherer and `axe-audit.js`, 4 audit files and the changelog (grep for budgets and axe); the web-vitals README sections cited; check-access.py's header. Sampled or second-hand: Deque's coverage page and the GDS audit and the W3C ACT implementation pages were read through WebFetch summaries (numbers quoted as returned; the axe ACT page only to character 100,000 of 140,616); the ACT "consistent" definition was not found in a primary source; IBM rule bodies beyond the 8 in-scope rules' messages were not read; whether axe applies 2.5.8's user-agent exception was not checked; no tool was run on any page.

