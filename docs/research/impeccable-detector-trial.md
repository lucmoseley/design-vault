# impeccable's detector against #250's five adoption criteria (#263)

Ticket: design-vault #263, under map #243. Question: does impeccable's detector pass #250's criteria (a)–(e), so its findings can count in the gate's tally? Method: #249's method (docs/research/outside-checkers-trial.md).

## 0. Source and version

- Source checkout: `/home/lucmo/.claude/plugins/marketplaces/impeccable`, git HEAD 6e802bd (4 Oct 2026). `ENGINE_VERSION` is 0.1.11.
- Installed plugin: impeccable 4.5.0. Its launcher `skills/impeccable/scripts/impeccable` runs a cached binary, `~/.impeccable/bin/0.1.11/impeccable` (15.4 MB, sha256 a3036c5c…6e40a).
- The ticket says the detector is "a closed binary". That is not correct. The source is in the checkout above, and its licence is Apache-2.0 (`LICENSE`; npm `impeccable` 4.5.2 also says Apache-2.0). `docs/ENGINE.md` says: "Everything is in this repo, Apache-2.0, and builds offline from source." It is a Rust workspace: `crates/foundation` holds the rule registry (`src/registry.rs`), `crates/core` holds the rule logic, `crates/html` is the static HTML engine, `crates/browser` is the URL engine (Chrome through CDP), and `crates/wasm` plus `browser-bundle/` make the in-page bundle.
- The shipped form is a binary. The launcher runs a static binary for each platform. If the binary is not in the cache, the launcher downloads it from `github.com/pbakaus/impeccable/releases/download/engine-v<X>/` and checks its `.sha256` file. The npm package `impeccable` 4.5.2 is a JS shim with five `optionalDependencies` (`@impeccable/cli-<os>-<arch>` 0.1.14), one binary for each platform.
- The source also has one in-page bundle: `crates/live/assets/detect-antipatterns-browser.js` (2,239,454 bytes, sha256 ecc6063c…672192f at 6e802bd). It holds the rule core compiled to WebAssembly (base64) and the page JS. `cargo xtask bundle` makes it, and the build is deterministic (`docs/ENGINE.md`). The rule registry is `crates/live/assets/antipatterns.json`.

## 1. Inventory: the 61 rules

Counted from `crates/foundation/src/registry.rs` (`ANTIPATTERNS`) and from `antipatterns.json`. Both have 61 rows.

- By category: `slop` 32, `quality` 29.
- By level (`severity` in the registry): primary (warning) 47, error 2 (`script-error`, `content-hidden-at-rest`), advisory 12. An advisory finding never counts as a failure and never changes the exit code (`detect --help`).
- The 12 advisory rules: blinking-cursor, shape-assembled-illustration, numbered-section-labels, em-dash-overuse, design-system-color, design-system-radius, design-system-font-size, gpt-thin-border-wide-shadow, repeating-stripes-gradient, codex-grid-background, theater-slop-phrase, image-hover-transform.
- #97's F5 split (29 slop, 23 quality, 4 design-system, 5 later) came from strings in the binary. The registry gives 32 slop and 29 quality: #97 put `organic-clip-path` and `buried-raster` (both `quality` in the registry) in its slop list, and it counted the 5 later rules apart.

### What config can change

- **Numbers: almost none.** No config key sets a rule's threshold. The keys under `detector` are `ignoreRules`, `ignoreFiles`, `ignoreValues`, `designSystem` and `advisoryRules` (`crates/detect/src/config.rs:40-46`).
  - `ignoreRules` switches a whole rule off. `ignoreFiles` skips files.
  - `ignoreValues` waives one reported value of one rule, and only for 6 rules: overused-font, bounce-easing and the four design-system rules (`DIRECT_VALUE_RULES`, `config.rs`). For example, it can waive one font name.
  - `designSystem` (DESIGN.md or `.impeccable/design.json`) gives the allowed fonts, colours, radii and font sizes to the four `design-system-*` rules.
- **One exception, in the in-page bundle only:** `window.__IMPECCABLE_CONFIG__.lineLengthMax` sets the line-length maximum (default 80; `crates/foundation/src/browser/mod.rs:156-180`). The CLI's URL engine sets it to `None`, so the CLI always uses 80 (`crates/browser/src/snapshot_engine.rs:200`). There is no minimum.
- In the bundle, `disabledRules` and `disabledValues` work only in extension mode (`mod.rs:137-147`). An adapter outside extension mode must filter the findings itself.
- A rule pack (`docs/ENGINE.md` §Rule packs) can add rules, but only in Rust, compiled into a new wasm or binary. It cannot change a built-in rule's number.

### The rules, with their thresholds and the vault's match

Key for the last column:
- **V-same**: a vault script answers the same question, with the same number. Cite the gate id.
- **V-diff**: a vault script answers the question, but with a different number or scope.
- **H-same**: a house rule has the same number or test, and no vault script checks it yet.
- **H-diff**: a house rule exists, with a different number or condition.
- **axe**: #250 gives this check to axe-core.
- **AI**: one of the house's "AI look" bans (`plugin/skills/design-round/references/impeccable.md` §The "AI look" bans). The house reports these at P2 at most. They "never fail a gate". So they can never go in the tally.
- **T**: a taste rule. The house has no rule with a number for it. Ledger rows are given where one exists (`docs/coverage-ledger.json`).

Thresholds: the main constant only. Paths are under `crates/`. "fs" is the font size.

| # | Rule id | Cat. | Level | Main threshold (source) | Vault match |
|---|---|---|---|---|---|
| 1 | side-tab | slop | primary | border on one side ≥3 px (≤12 px in a tab context) (core/src/checks/rules.rs:77,85) | AI ("a coloured side border"; impeccable.md names `side-tab`) |
| 2 | border-accent-on-rounded | slop | primary | thick accent border plus radius (rules.rs) | AI (coloured side border) |
| 3 | overused-font | slop | primary | 17-name list `OVERUSED_FONTS` (foundation/src/constants.rs:85); `ignoreValues` can waive a name | AI (impeccable.md names `overused-font`) |
| 4 | flat-type-hierarchy | slop | primary | heading/body step <1.25× at every step, ≥3 roles (rules.rs:869-871) | H-diff: house adds "no finding where weight, space or tone carries the step" (impeccable.md:85); the detector reads size only. Ledger TYS-19 |
| 5 | gradient-text | slop | primary | `background-clip: text` with a gradient (rules.rs) | AI ("gradient text"); ledger COL-84 (gate) |
| 6 | ai-color-palette | slop | primary | purple hue 260–310 with chroma >50 on headings or text ≥20 px; cyan on dark (rules.rs) | T |
| 7 | cream-palette | slop | primary | warm cream page background (core/src/browser/page_checks.rs:516) | T |
| 8 | nested-cards | slop | primary | card-like box inside card-like box (page_checks.rs:259) | AI ("nested cards") |
| 9 | monotonous-spacing | slop | primary | one spacing value used everywhere (core/src/checks/html_patterns.rs) | T (the house's 4 px step is a different rule) |
| 10 | bounce-easing | slop | primary | `bounce`/`elastic` names, `animate-bounce`, overshoot curves (rules.rs:742-784) | H-same in kind, no number: house "decelerating curves" (impeccable.md:107); ledger MOT-24, MOT-29 (script). No vault script reads UI easing; check-flow reads brand motion only |
| 11 | pulsing-dot | slop | primary | small dot with an infinite pulse (core/src/checks/css_scan.rs) | T. vault.pause asks a different question (a pause control for motion over 5 s) |
| 12 | blinking-cursor | slop | advisory | caret-like blink in a hero (core/src/browser/element_checks.rs) | T |
| 13 | shape-assembled-illustration | slop | advisory | large inline SVG made of many primitives (html_patterns.rs) | T |
| 14 | organic-clip-path | quality | primary | `clip-path` polygon with many vertices, or `path()` (css_scan.rs) | T |
| 15 | buried-raster | quality | primary | raster at opacity <0.15 (core/src/browser/quality.rs:245); wash over an image at alpha ≥0.9 (css_scan.rs) | T |
| 16 | dark-glow | slop | primary | zero-offset chromatic shadow, or coloured blurred shadow on dark (rules.rs, element_checks.rs) | H (look, no number): surface-styling "depth only for what floats or acts"; ledger COL-80 (gate) |
| 17 | radial-halo | slop | primary | saturated radial gradient fading to transparent on a dark page (html_patterns.rs) | as 16 |
| 18 | radial-spotlight-glow | slop | primary | low-alpha accent radial gradient (core/src/checks/measures.rs) | as 16 |
| 19 | marquee | slop | primary | auto-scrolling content (css_scan.rs, page_checks.rs) | V-diff: vault.pause (check-access) asks for a pause control on motion over 5 s; the detector bans the marquee. Ledger NEW2-16 |
| 20 | icon-tile-stack | slop | primary | small rounded icon box above a heading (element_checks.rs) | AI ("same-size icon cards") |
| 21 | italic-serif-display | slop | primary | italic serif from `KNOWN_SERIF_FONTS` as hero headline (element_checks.rs) | T |
| 22 | hero-eyebrow-chip | slop | primary | small uppercase tracked label above a large hero heading (rules.rs) | AI, conditioned: the house struck the "ban"; an eyebrow that names the section is no finding (impeccable.md:75). The detector cannot tell which |
| 23 | kicker-above-heading | slop | primary | small tracked uppercase block above a heading, gap <28 px, ≤80 chars (page_checks.rs:373,380) | as 22 |
| 24 | numbered-section-labels | slop | advisory | small numeric labels repeated by section headings (core/src/checks/text_rules.rs) | AI ("section numbers") |
| 25 | em-dash-overuse | slop | advisory | ≥8 em-dashes at about one for each 500 chars (constants.rs:193-195) | T; the words script #250 rules (word bans as P2 warnings) |
| 26 | marketing-buzzword | slop | primary | word list (detect/src/regex_matchers.rs) | T; as 25 |
| 27 | aphoristic-cadence | slop | primary | ≥3 sections that end on "X. No Y." forms (regex_matchers.rs) | T; as 25 |
| 28 | oversized-h1 | slop | primary | h1 ≥72 px, ≥40 chars, ≥28% of viewport height or ≥25% of its area (measures.rs:140-144) | H-diff: house says the project's type scale sets display size (impeccable.md:86); ledger TYS-24 |
| 29 | extreme-negative-tracking | slop | primary | letter-spacing ≤ −0.05em on text >20 chars (quality.rs:738) | H-diff: house hands display tracking to the project's scale (impeccable.md:86); ledger TYS-63 |
| 30 | broken-image | quality | primary | `<img>` with empty, missing or placeholder `src` (html/src/adapters.rs) | No gate question. A DOM probe line |
| 31 | script-error | quality | error | any uncaught error or parse failure during load (browser/src/lib.rs) | No gate question, no vault script. No page error occurred on any of the 12 pages in this run. (#169's "two script errors" were check-layout misreads, not page errors.) |
| 32 | content-hidden-at-rest | quality | error | >30% of text hidden, with ≥200 chars in total and ≥150 hidden, after a reveal sweep (measures.rs:260-264) | No vault script. vault.load (check-load) fails a page whose LCP never shows, a near case |
| 33 | edge-flush-cards | quality | primary | card in a scroller with one gutter ≥6 px and the other <8 px (page_checks.rs:729-730) | No house number (ledger LAY-23 "impeccable-only") |
| 34 | text-occlusion | quality | primary | text under an opaque box or other text, by hit-test points inside the current viewport only (page_checks.rs:1017-1024) | V-same in kind: vault.reflow overlap (check-layout), at every width and over the whole page |
| 35 | first-viewport-column-overflow | quality | primary | in the first row, one column ends >0.25 viewport height below its sibling (page_checks.rs:1366) | T |
| 36 | gray-on-color | quality | primary | grey text on a chromatic background (Tailwind classes, or computed colours) (rules.rs:191,251) | H-same in kind, no number: the tint rule says secondary text on a coloured ground takes the ground's hue, "never a plain grey" (text-presentation.md). No gate question |
| 37 | low-contrast | quality | primary | 4.5:1, or 3:1 at ≥24 px or ≥18.67 px bold (rules.rs:266, core/src/browser/visual.rs:279, constants.rs WCAG_LARGE_*) | V-same: vault.contrast (check-access), same numbers and large-text sizes |
| 38 | layout-transition | quality | primary | `transition`/`animation` on width, height, padding or margin (rules.rs) | H-same: "no casual animation of layout properties" (impeccable.md:107); ledger MOT-34 (script). No vault script |
| 39 | line-length | quality | primary | >80 chars (+5 slack) on ≥2 rendered lines (quality.rs:303; default 80 at foundation/src/browser/mod.rs:170) | V-diff: check-measure.py holds 45–75 (workflow-core#1408; impeccable.md:83). The detector has no minimum and charges only above 85 |
| 40 | cramped-padding | quality | primary | inset < max(4, 0.3·fs) vertical or < max(8, 0.5·fs) horizontal; or children flush (≤2 px) to a visible edge (quality.rs:362-363,450) | No house number (ledger BTN-1: "No house rule sets padding inside a button") |
| 41 | body-text-viewport-edge | quality | primary | `<p>`/`<li>` over 40 chars, wider than 50% of the viewport, <16 px from its edge (quality.rs:601-603) | No house number (ledger LAY-23 "impeccable-only") |
| 42 | tight-leading | quality | primary | line-height < 1.3× on non-heading text over 50 chars (quality.rs:632) | H-same: the house keeps 1.3 on body text only (impeccable.md:84); the detector already skips headings. Ledger TYS-39. No vault script |
| 43 | skipped-heading | quality | primary | a heading level skipped (quality.rs:810) | axe (#250: "heading order come from axe") |
| 44 | heading-rhythm | quality | primary | space above a heading not more than space below, ≥2 cases, 12 px deficit (page_checks.rs:308-311) | No house number (proximity, Gestalt, is a look rule) |
| 45 | justified-text | quality | primary | `text-align: justify` without `hyphens: auto` (quality.rs) | H-diff: house says "no justified text" at all (impeccable.md:104); ledger TXL-44 |
| 46 | tiny-text | quality | primary | body text <12 px, >20 chars, not UI, not uppercase (quality.rs:661) | H-diff: house body floor 16 px, "unless a dense role justifies less" (impeccable.md:104); ledger TYS-7, TYS-8 |
| 47 | undersized-ui-text | quality | primary | functional text <11 px (10 px in small print) (quality.rs:683,693) | H-diff: house has only the 16 px body floor with a dense-role exception; no number for UI text |
| 48 | all-caps-body | quality | primary | `text-transform: uppercase` on >30 chars of non-heading text (quality.rs:711) | T: ledger TXL-98 is research only ("caps on short labels only"), not carried |
| 49 | wide-tracking | quality | primary | letter-spacing >0.05em on lowercase body >20 chars (quality.rs:723) | T: ledger TYS-62 research says no added tracking on body; not carried |
| 50 | text-overflow | quality | primary | an element's content ≥16 px wider than its box (element_checks.rs:1198,1235) | V-diff: vault.reflow (check-layout) fails sideways scroll and text cut off at the screen edge, at every width 320–2560; the detector reads element boxes at one width |
| 51 | repeated-container-text | quality | primary | same text ≥3 times in one card (core/src/browser/text_collectors.rs:462) | T |
| 52 | clipped-overflow-container | quality | primary | `overflow: hidden/clip` box that holds an absolutely positioned child it cuts (element_checks.rs:1106) | T |
| 53 | design-system-font | quality | primary | font not in DESIGN.md (detect/src/design_system.rs) | Project value system (house-principles dependency order step 4). Set by DESIGN.md, so the project sets it |
| 54 | design-system-color | quality | advisory | colour outside DESIGN.md palette | as 53 |
| 55 | design-system-radius | quality | advisory | radius outside DESIGN.md scale | as 53 |
| 56 | design-system-font-size | quality | advisory | font size outside DESIGN.md ramp | as 53 |
| 57 | gpt-thin-border-wide-shadow | slop | advisory | border ≤1.5 px at alpha ≥0.28 with a wide blur (measures.rs:192-200) | T |
| 58 | repeating-stripes-gradient | slop | advisory | `repeating-*-gradient` stripes (html_patterns.rs) | T |
| 59 | codex-grid-background | slop | advisory | hairline gradient grid tiled at a fixed cell (html_patterns.rs) | T |
| 60 | theater-slop-phrase | slop | advisory | the word "theater" used to dismiss (html_patterns.rs) | T |
| 61 | image-hover-transform | slop | advisory | scale or rotate on an image on hover (html_patterns.rs) | T |

### Summary of the map

- **V-same (2):** low-contrast (vault.contrast), text-occlusion (vault.reflow overlap).
- **V-diff (3):** line-length (check-measure, 45–75 against >80), text-overflow (vault.reflow), marquee (vault.pause asks a different question). Also, check-load's vault.load is near content-hidden-at-rest, but it does not ask the same question.
- **H-same, no vault script (8):** tight-leading (1.3, body only), layout-transition, bounce-easing (no number), gray-on-color (no number), and the four design-system rules, which take their values from the project.
- **H-diff (7):** flat-type-hierarchy, oversized-h1, extreme-negative-tracking, justified-text, tiny-text, undersized-ui-text, and the AI-conditioned eyebrow rules (22, 23).
- **axe (1):** skipped-heading.
- **AI (9):** side-tab, border-accent-on-rounded, overused-font, gradient-text, nested-cards, icon-tile-stack, hero-eyebrow-chip, kicker-above-heading, numbered-section-labels.
- **No house rule (T, or quality rules with no house number): the rest (about 30).** These include the four quality rules with no house number (cramped-padding, body-text-viewport-edge, heading-rhythm, edge-flush-cards), broken-image and script-error.

## 3. Runs

### Set-up

- Nothing was installed into the repo.
- Two routes ran. Route 1: the installed CLI binary 0.1.11 (`impeccable detect --json`), static on each file and as a URL engine on each page. Route 2: the in-page bundle (crates/live/assets/detect-antipatterns-browser.js) injected by Playwright into a page that check-layout's `load()` opened, with `bypass_csp`, then `impeccableDetectAsync()` with `autoScan:false`.
- Widths: desktop 1920×633 and phone 390×664 (touch), as check-layout's devices. Extra widths: the fault width of each layout fixture (crowd 1550, slide 1200, under 850, wide 2400, nested, overflow and cut 450).
- Input: 34 fixtures (access 18, including the new growing.html and strokes.html; layout 13; load 3) and #169's 12 pages (r1 v1–v5 from tag rounds/site-look-r1, r2 v1–v7 from tag rounds/site-look-r2), from `git archive` of the mmm-infra tags, served on 127.0.0.1.
- Key: the vault scripts' own results on the same input (check-access, check-layout), and each fixture's planted fault.

### Agreement of the two routes

The bundle and the CLI URL engine gave the same findings, with these CLI-only differences:
- motion.html: low-contrast on a fade in mid-animation (false positive).
- unmeasurable.html: low-contrast on a gradient heading, read from pixels at 1.7–1.8:1. The text passes on its gradient stops (false positive).
- r1 v2: 4 low-contrast findings on SVG text ("NTS", "EQ", "EQ", "±0.00") at 1.0:1. By eye, this is readable light text on a blue grid (false positives).
- r1 v4: clipped-overflow-container ×2 at desktop. r2 v2: line-length ×1 at desktop.

### Fixtures

| Fixture | Planted fault | Detector result |
|---|---|---|
| contrast.html | 3 low-contrast texts | 2 of 3. It missed the `::before` text "New" |
| faint.html | 4 faint patches | 0 of 4 |
| strokes.html | 2 true faults (#band 1.00:1, #other) | 1 of 2 (#other). Missed #band. 4 false positives: p.note>span, #rule, #pad, #beside, which pass under the vault's rule (#257) |
| logotype.html | p.faint | Found p.faint. Also flagged div.brand, a logotype the vault exempts (--logotype). Did not flag the SVG wordmark |
| unmeasurable.html | none to count (vault reports "unmeasurable") | low-contrast on p.over (#fff on #fff; the caption sits on a black canvas): false positive. gradient-text and ai-color-palette: AI look, never tallied |
| access/clean.html | none | none |
| noise.html | none for contrast | cramped-padding on div.band ×2: no house rule |
| edge, focus, keyboard, link, target, touch, loop, flicker, dates, growing | one fault each | nothing. The detector has no rule for these questions |
| layout/clean.html | none | low-contrast on p.over: a white caption over a #446688 photo, read as #fff on #fff. False positive on a clean page |
| cut.html, overflow.html | text cut at the edge; sideways scroll | clipped-overflow-container on div.box at every width, 2400 included. The cause it names is false (the box is not positioned; the child is position:fixed and escapes). It missed the cut text (lead at −40 px) and the sideways scroll |
| crowd, slide, under, wide, nested, probe (at their fault widths) | overlap or overflow | nothing. No overlap, overflow or cut text found |
| nested, touch, overflow at 390 | sideways scroll | nothing |
| fixed, nometa, fold, load fixtures | load and layout faults | nothing. No rule asks these questions |

### #169's 12 pages

Contrast. check-access finds 103 element-widths below the WCAG ratio (desktop 53, phone 50: r1 v1 2+1, r1 v2 50+45, r1 v4 1+0, r2 v2 0+4). It also marks SVG text unmeasurable on r1 v3, r2 v1, r2 v3 and r2 v7. The detector found 0 of the 103 (bundle 0; CLI 4, all false positives on r1 v2).

Layout. The detector found none of #169's layout faults at 1920 or 390. r1 v1's sideways scroll (about 525 px) shows at 390; the detector missed it. The overlaps #169 found at 765 px (r2 v1) and on r2 v7 were not run at their own widths (see Bound).

Other findings on the pages, judged by eye and against the house rules:
- r1 v3: text-overflow on a.tabula (26 px, "WRITE TO MARK"). Nothing is cut: false positive.
- r1 v4 p.inner.credit and r2 v6 p.cap: body-text-viewport-edge. Padding insets the text; the rule reads the box: false positive.
- r2 v1 phone: tight-leading on p.sheet-note, which is `display:none`: false positive.
- p.demo.enter (40 px) and r2 v7 p.demo-line (22 px): tight-leading on display text in a `<p>`. A false positive under the house's body-only condition (impeccable.md:84), but arguable.
- undersized-ui-text on the 9.6 px "MMM INFRA" brand span (r2 v2, v4, v5): a logotype, which the vault exempts.
- line-length on r2 v1 (4), r2 v3 (5), r2 v7 (2), r2 v2 (CLI only, 1). Not compared with check-measure in this run (see Bound). check-measure also charges lines of 76–85 characters and lines under 45, which the detector cannot charge.
- cream-palette, oversized-h1, italic-serif-display, cramped-padding: taste or no house number. Never tallied.

### Time

- CLI static: about 0.05 s a file. CLI URL engine: about 2.5–3 s a width, Chrome launch included.
- Bundle, after load: median 1.55 s on fixtures (1.16–3.12 s), 1.26 s on pages (1.11–1.73 s).
- Offline: the CLI static run worked under `unshare -rn` (no network). The bundle made 0 requests.

## 4. Verdicts on #250's criteria

**(a) Finds — fails.** On the questions it shares with the vault, it finds less and raises false positives:
- Contrast: 2 of 3 on contrast.html, 0 of 4 on faint.html, 1 of 2 on strokes.html, 0 of 103 element-widths on the pages. It raised false positives on two clean or passing fixtures (layout/clean.html, unmeasurable.html), 4 on strokes.html, 1 on a logotype, and 4 (CLI) on r1 v2.
- Layout: it found none of the planted overlaps, overflows, cut text or sideways scrolls, at any width. Its one layout finding on the fixtures (clipped-overflow-container) names a false cause.
- Its occlusion test uses `elementFromPoint` inside the current viewport only, so it cannot see a layer with `pointer-events:none` or text below the fold.
- Rules with no vault match found nothing to check on the fixtures, because the fixtures do not plant those faults. On the pages, 6 of 6 judged non-taste findings outside contrast were false positives or exempt (text-overflow, body-text-viewport-edge ×2, tight-leading on hidden text, logotype ×3 pages).

**(b) Threshold — fails.** All thresholds are constants in the Rust source (rules.rs, quality.rs, element_checks.rs). Config can switch a rule off (ignoreRules) or allow a value (ignoreValues, 6 rules only); it cannot change a number. The one exception, lineLengthMax, sets a maximum only (charged above max + 5), with no minimum, so it cannot hold 45–75. Where the detector's number equals the house's (contrast 4.5/3.0 and the large-text sizes; tight-leading 1.3 on non-headings), the tie lets no vault check retire, because (a) fails on those rules.

**(c) Upkeep — passes, with a note.** pbakaus/impeccable ships an engine release every few days (engine-v0.1.0 on 4 Sep 2026 to engine-v0.1.14 on 9 Oct 2026). npm `impeccable` has 190,836 downloads a week (6–12 Oct 2026). Note: the engine is pre-1.0 (0.1.x), so rules and numbers can change in any release; the pin-and-diff rule in impeccable.md:8 already applies. The bundle is not a release asset; it is a file tracked in the repo, so a pin must name a commit.

**(d) Licence — passes.** Apache-2.0 for the whole repo, engine included (LICENSE; ENGINE.md). A vendored copy must carry LICENSE and NOTICE.md.

**(e) Packaging — split.**
- CLI and npm route: fails. Both are per-platform binaries outside the vault's routes (#244).
- Bundle route: passes on form. detect-antipatterns-browser.js is one file, with the wasm embedded. It builds deterministically (`cargo xtask bundle`), runs offline inside the vault's Playwright page with `bypass_csp` (it needs `'wasm-unsafe-eval'`), and a test can pin its hash. But it does not carry the URL engine's rules: script-error, content-hidden-at-rest and screenshot contrast run only in the CLI.

**Result: no rule of the detector passes all five criteria.** (a) fails on every rule that the vault can compare, and (b) fails for every rule. The detector's findings must not count in the gate's tally. They can stay advice, as impeccable.md already uses them.

## 5. Input for the ruling: what the shared probe builds instead

Owner: #258 (the rule-records spec), whose script tickets start from #250's table.

The shared computed-style and DOM probe should build these checks itself, with the house's numbers. The detector's rule text and file:line (table in §1) are a useful start, under Apache-2.0:
- **Line height:** under 1.3 on body text only, with the display-text exemption that the detector does not make (impeccable.md:84; TYS-39). Skip hidden elements.
- **Layout-property motion:** `transition` or `animation` on width, height, padding or margin (impeccable.md:107; MOT-34).
- **Easing:** bounce, elastic and overshoot curves on UI motion (impeccable.md:107; MOT-24, MOT-29). A number needs research first.
- **Justified text:** any `text-align: justify` on body text (impeccable.md:104). The house bans all of it; the detector's rule is narrower.
- **Small text:** a 16 px body floor unless a dense role justifies less (impeccable.md:104), with the logotype exemption. Not the detector's 12 px and 11 px.
- **Broken image** and **script error:** a failed image load and a `pageerror` listener in the page the vault already opens.
- **Content hidden at rest:** content that stays hidden after load without a reveal. Compare with check-load's vault.load first.
- **Grey on colour:** the tint rule (text-presentation.md). A number needs research first.

Keep the vault's own scripts for the questions they answer better: check-access (contrast), check-layout (overlap, overflow, cut text, sideways scroll) and check-measure (45–75 measure). Give skipped headings to axe (#250).

Do not tally: the 9 AI-look rules and the taste rules (cream palette, italic serif display, buzzwords and other T rules). Their words can go to #250's text script as P2 advice. The quality rules with no house number (cramped-padding, body-text-viewport-edge, heading-rhythm, edge-flush-cards, wide-tracking, all-caps, oversized-h1, extreme-negative-tracking, flat-type-hierarchy) need a sourced number before any check counts.

## Bound

- Read in full: the rule registry (antipatterns.json and crates/foundation/src/registry.rs), the config code (ignoreRules, ignoreValues, designSystem, advisoryRules, lineLengthMax), the launcher script, the npm package metadata, LICENSE, NOTICE.md and ENGINE.md. Read at the cited lines only: the check code for each threshold in §1.
- Ran: all 34 fixtures and all 12 pages on both routes at 1920 and 390, and the layout fixtures at their fault widths.
- Not run: the bundle at #169's own overlap widths (r2 v1 at 765, r1 v3 at 320); the bundle with `visualContrast:true`; lineLengthMax set to another value; check-measure on the pages, so the line-length findings are not compared with the vault's. The contrast verdict uses check-access's numbers from this run, not #169's.
- Upkeep figures are from `gh release list` and the npm downloads API on 15 Oct 2026. The source read is a shallow clone; the newest engine is 0.1.15 (released 15 Oct 2026), and the rule changes after 0.1.11 were not read.
- "False positive" on the pages is a judgement by eye on screenshots and computed styles, one reader.
