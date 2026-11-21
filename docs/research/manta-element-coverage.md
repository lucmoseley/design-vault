# Manta site: element coverage by design rule and research (design-vault#118)

⚠ **Bound 14 Oct 2026 (#103): the rule form is #103's nine-field form, for gate questions only.**

⚠ **Bound 13 Oct 2026 (#121): every §4 conflict K1–K27 is resolved or put to the founder in `docs/research/principle-interactions.md` §3. All K rows are Manta-only (owner lucmoseley/mantahostels); the founder rulings R1–R11 there are Manta's to put. The rule form that carries conditions goes to #103.**

Question: What is every element that the Manta site shows or will show? Which elements have no design rule or research behind them, held or planned?

Status: complete (13 Oct 2026).


## Key

- **Status.** `B` = built in `~/mantahostels/app/` (the live site). `S` = specified: a Manta rules file (`brand-sheet.md`, `DESIGN.md`, `PRODUCT.md`) or the design-system corpus (`docs/design-system/`) gives the element a visual form. `P` = planned only: a roadmap card or an open issue names the element, but no file gives it a visual form. `X` = ruled out by a decision.
- **Corpus** = `~/mantahostels/docs/design-system/` (the Claude Design export, reconciled to brand sheet v2.18). It is reference only. The brand sheet wins on every conflict (`docs/design-system/README.md`).
- **Sheet** = `~/mantahostels/docs/brand/brand-sheet.md` v2.37. Rule numbers `B1`-`B53` and `X1`-`X12` are the rows of the #98 census (`docs/research/design-rules-census.md` §4b, §4c). `G`, `L`, `R`, `F`, `D` numbers are the census rows for the vault files.
- **What counts as research.** (1) A measured value against a standard, for example a contrast ratio against WCAG 2 (census Src `S`). (2) A study or primary source in a house research file: #104 (`docs/research/design-coverage-gaps.md`), #115 (`docs/research/manta-design-migration.md`), or a Manta research file. A ticket ruling or a founder decision is not research. A reasoned argument in the sheet with no source is not research.

## 1. Inventory: every element that the Manta site has or plans

Finding 1.0. The live site (`app/`) is small. It has 6 routes: `/` (home), `/best-hostels-in/[place]` (destination guide), `/how-we-rank`, `/privacy`, `/terms`, `/report`. It has 7 components: `Nav`, `SiteFooter`, `Ground`, `HeroWave`, `Mark`, `Wordmark`, `icons` (`app/_components/`). The CSS classes in `app/globals.css` are: `btn` (`--primary`, `--secondary`), `chips`, `dest-card`, `hero` (`__eyebrow`, `__headline`, `__body`, `__cta`, `__wave`), `notice`, `page` (`__region`, `__lede`, `__meta`), `prose`, `section`, `site-nav` (`__toggle`, `__links`, `__backdrop`), `site-footer`, `wordmark`. Most of the planned product (search, listing, detail, handover, map, account, reviews, rewards) exists only as the corpus `ui_kits/` and `components/`, or only as a roadmap card.

Finding 1.0b. No open issue on lucmoseley/mantahostels has the label `kind:spec`. The open design issues are #2988 (gesture settle for the map bottom sheet), #2989 (scroll reveal in the hero), and #3057/#3059/#3060 (page background art in the working area).

### 1.1 Global chrome (every page)

| # | Element | Status | Where |
|---|---|---|---|
| E1 | Nav bar, desktop (ink, 72 px, wordmark lockup, inline links, current link semibold) | B, S | `app/_components/Nav.tsx`; sheet §2 (B7, B8) |
| E2 | Nav, mobile (56 px; "Menu" toggle; panel opens below the row; pointer-only scrim) | B, S | `Nav.tsx:34-71`; `DESIGN.md` §Layout |
| E3 | Wordmark and nav lockup | B, S | `Wordmark.tsx`; sheet §5 (B31) |
| E4 | Mark (primary, nav variant, flat variant) | B (primary, flat); P (nav variant, §15) | `Mark.tsx`; sheet §6 (B5, B32-B34) |
| E5 | "Sign in" control in the nav | S | sheet §3 (B25 "Sign in is always an outline"); corpus `MarketingNav.jsx` |
| E6 | Site footer (ink; columns of underlined white links; muted-night secondary copy; "All prices include taxes") | B, S | `SiteFooter.tsx`; corpus `SiteFooter.jsx`; sheet §2, §3 night pattern (B6, B23) |
| E7 | Favicon, app icon, Open Graph image | B | `app/icon.png` from `mark-flat.svg` (sheet §6) |
| E8 | Language switch (review-language toggle first, then site language) | P | roadmap `i18n` |
| E9 | Currency switch | none found | grep of corpus and roadmap: only "Rp" prices |
| E10 | Cookie or consent notice | X | `member-account` card: "#478 cut the consent banner on the ground that analytics is disclosed and not consented to"; `event-schema` card: PostHog `cookieless_mode: 'always'` |
| E11 | Skip link | none | grep "skip" in `app/globals.css`: one comment, no skip link |
| E12 | 404 page | P | sheet §6 names "404" as a personality surface; §9 "errors" are illustration-led. `app/` has no `not-found.tsx`, so Next.js shows its default |
| E13 | Error page (server error, offline) | P | sheet §9 "errors"; roadmap `mobile-app` (offline caching) |
| E14 | Focus ring (all controls) | B, S | `globals.css` `:focus-visible` rules; sheet §10 (B47) |

### 1.2 Marketing zone

| # | Element | Status | Where |
|---|---|---|---|
| E15 | Hero on a turquoise ground (home) | B, S | `app/page.tsx`; sheet §2 (B1, B4, B5) |
| E16 | Hero eyebrow | B, S | `.hero__eyebrow`; sheet §2 line 26 ("Hero eyebrows ... take ink") |
| E17 | Hero headline and body | B, S | `.hero__headline`, `.hero__body`; sheet §4 |
| E18 | Hero CTA pair (coral primary, outline secondary) | B, S | `.btn--primary`, `.btn--secondary`; sheet §3, §4 (B12, B29) |
| E19 | Hero search box (destination input + coral "Search") | S, P | corpus `Homepage.jsx`; sheet §3 ("on a marketing view it is the hero search button"); roadmap `search-core` |
| E20 | Hero wave with the mascot | B, S | `HeroWave.tsx`; sheet §8 (B42) |
| E21 | Destination card grid (home, "Where we're starting") | B | `.dest-card`; no sheet clause names it |
| E22 | "Popular right now" hostel tiles (home) | S (corpus only) | corpus `Homepage.jsx` |
| E23 | Destination hero (turquoise, 150 px wave) | S | corpus `DestinationHero.jsx`; sheet §8 (150 px wave). The built guide page has no hero |
| E24 | Destination guide body (region label, h1, lede, Surf/Vibe/Good for/What to look for sections) | B | `app/best-hostels-in/[place]/page.tsx` |
| E25 | "Good for" chips (static) | B | `.chips` |
| E26 | Interior announcement block ("coming soon" notice, ink) | B, S | `.notice` in an ink `Ground`; sheet §2 (B3) |
| E27 | Destination preview: filter chips, 3 preview rows, coral "See all N hostels" | S | corpus `DestinationHero.jsx`; corpus `readme.md` "Destination pages hand off, never dead-end" |
| E28 | Founding-reviewer email box beside a guide list | P | roadmap `guide-pages` (copy on mantahostels#2976; "no tick, no 'I agree'") |
| E29 | Rewards screen (ink; tier headline; stat tiles; amber progress pill) | S, P | corpus `RewardsScreen.jsx`, `MobileRewards.jsx`; roadmap `rewards-engine` |
| E30 | Partner spotlight page | P | roadmap `partner-spotlight` |
| E31 | Prose pages (how-we-rank, privacy, terms, bilingual report) with "Last updated" meta | B | `.prose`, `.page__meta`, `.page__lede` |
| E32 | Travel-insurance guide or footer section | P | roadmap `insurance` |
| E33 | Illustration: guide-page hero art, empty-state art, 404 art, onboarding art | P | sheet §8, §9; roadmap `seo` |
| E34 | Page background art in the working area | P (research open) | mantahostels#3057, #3059, #3060 |
| E35 | Emails (review solicitation, launch announcement, partner volume report) | P | sheet §2 puts emails in the marketing zone; roadmap `review-solicit-email`, `launch-announce`, `partner-volume-report` |
| E36 | Social tiles | P | sheet §2 (night ground context); roadmap `owned-social` |

### 1.3 Working area: search and results

| # | Element | Status | Where |
|---|---|---|---|
| E37 | Destination search input (working area) | S, P | corpus `components/forms/Input.jsx`; roadmap `search-core` |
| E38 | Search autocomplete or suggestions | none | no file names it |
| E39 | Results header ("42 hostels in Canggu · all prices include taxes") | S | corpus `SearchResults.jsx`; sheet §7 (B40) |
| E40 | Sort control (native select) and the "how we rank" link beside it | S | corpus `Select.jsx`, `SearchResults.jsx`; roadmap `search-core` ("never review count as default"; "one link to how-we-rank, beside sort") |
| E41 | Map toggle button | S | corpus `SearchResults.jsx` (pill, map icon) |
| E42 | Filter panel, desktop (240 px sidebar; sections; checkbox rows with counts; budget inputs; room-type radios; rating floor) | S | corpus `readme.md` "Filter panel"; `SearchResults.jsx` |
| E43 | Filter chip (selectable, removable) | S | corpus `Tag.jsx` ("Selected state uses lagoon") |
| E44 | Mobile filters (horizontal chip rail; no sheet specified) | S (corpus only) | corpus `ui_kits/marketing/mobile.html` ("horizontal-scroll card rail and chips") |
| E45 | Listing card (row, desktop; stacked, mobile) | S | sheet §7 (B38, B39); `DESIGN.md`; corpus `HostelCard.jsx` |
| E46 | Card photo with carousel dots | S | sheet §7 ("carousel dots") |
| E47 | Compound rating line (score chip · word · count) | S | sheet §7 (B36, B24); corpus `ScoreChip.jsx` |
| E48 | "No reviews yet" in the score slot | S | sheet §7 (B36) |
| E49 | Price block ("Dorms from / Rp 145k / night") | S | sheet §7 (B40) |
| E50 | Facts line and flavour line | S | sheet §7 (B38) |
| E51 | Amenity icons (row on card; tooltip by `title`) | S | sheet §10 (B44); corpus `icons.jsx` |
| E52 | Compare checkbox (4-maximum, quiet disabled state) | S | corpus `readme.md` "Comparison rules"; `SearchResults.jsx` |
| E53 | "View beds" row button (quiet outline) | S | sheet §3 (B25) |
| E54 | Sticky compare bar (the one coral object of a search view) | S | sheet §3 (B25); corpus `SearchResults.jsx` |
| E55 | Comparison view (separate cards, sticky label rail, aligned rows, best-value tint) | S | corpus `readme.md`, `Comparison.jsx` |
| E56 | Mobile comparison (2-up swipe) | S (corpus only) | corpus `MobileComparison.jsx` |
| E57 | Empty compare state | S (corpus only) | corpus `Comparison.jsx` ("Tick a couple of hostels ...") |
| E58 | Empty results (no hostel matches the filters) | none | no file |
| E59 | Loading state of results (skeleton or spinner) | none | no file |
| E60 | Pagination, "load more" or infinite scroll | none | no file |
| E61 | Map view (map, pins, clusters, selected-pin card) | P | roadmap `map-view` (tiles only: MapLibre, PMTiles) |
| E62 | Map bottom sheet, mobile (drag to settle) | P | mantahostels#2988 |
| E63 | Availability section ("no space for your dates", greyed; "availability not shown - check with the hostel") | S, P | `DESIGN.md` Do's (X3); `PRODUCT.md` principle 2; roadmap `avail` (consent-gated) |
| E64 | Demand signal ("often books out ~3 days ahead") | P | roadmap `sell-out` |
| E65 | Partner filter and partner badge (opt-in, reward-labelled) | P | roadmap `search-core`; `PRODUCT.md` ("Status-gated features - badge") |
| E66 | Review-keyword search | P | roadmap `search-core` |
| E67 | Date picker (dates for the handover) | P | sheet §12a ("Dates and guests prefill the outbound links"); corpus handover shows only a date row with "Edit" |
| E68 | Guest stepper (44 px minus and plus) | S (corpus only) | corpus `BookingHandover.jsx` |

### 1.4 Working area: hostel detail and handover

| # | Element | Status | Where |
|---|---|---|---|
| E69 | Back link | S (corpus only) | corpus `HostelDetail.jsx` |
| E70 | Photo gallery (arrows, dots, count pill over the photo) | S (corpus only) | corpus `HostelDetail.jsx` `Gallery` |
| E71 | "Photos coming soon" fallback | S, P | corpus `HostelDetail.jsx`; roadmap `seed-listings` (photo fallback) |
| E72 | Detail header (h1, manta row, score chip, word, count, link to reviews) | S | corpus `DetailHeader`; sheet §7 |
| E73 | Rating unit (five mantas) | S | sheet §7 (B35); corpus `RatingMantas.jsx` (diamond placeholder) |
| E74 | Rating-unit "full rating" animation | P | roadmap `review-ux` ("the last manta pops larger and the row shifts colour") |
| E75 | Quick-facts tags and "Dorms from" | S (corpus only) | corpus `QuickFacts` |
| E76 | Rooms and beds rows | S | sheet §12a ("Rooms and beds render as rows") |
| E77 | Availability chip (available / no space + adjust dates / not shown + check with hostel) | S | sheet §12a; corpus `AvailChip` |
| E78 | Source line (dated, under each asserted fact) | S | sheet §11 "The source line"; corpus `SourceLine.jsx` |
| E79 | Category sub-score bars | S | sheet §7 (detail and comparison only); corpus `Reviews` |
| E80 | Review card (name · country, month, score chip, verified badge, sub-score, text, disclosure) | S | sheet §7 "Review-card elements" (B37); corpus `Reviews` |
| E81 | "Verified stay" badge | S | sheet §7 (B37); corpus `VerifiedStayBadge.jsx` |
| E82 | "Reviewer earns rewards" disclosure | S | sheet §7 (B37), §15 (placement open) |
| E83 | Most-recent stay month beside the review count | P | roadmap `review-ux` (#979) |
| E84 | Hostel testimonial pull-quote | S | `DESIGN.md` §Components (X1) |
| E85 | Location block (address, map thumbnail, "Open in maps") | S (corpus only) | corpus `PageFooter` |
| E86 | Full amenities checklist | S (corpus only) | corpus `PageFooter` |
| E87 | "Own this hostel?" claim link | S, P | corpus `PageFooter`; roadmap `seed-listings` (claim CTA) |
| E88 | Handover module, desktop (sticky right sidebar) | S | sheet §12a (B53); corpus `BookingHandover.jsx` |
| E89 | Handover bar, mobile (sticky bottom bar that expands into a sheet) | S | sheet §12a; corpus `MobileHostelDetail.jsx` |
| E90 | Coral exit "Book direct with the hostel" | S | sheet §12a |
| E91 | OTA exit buttons (ink outline, plain-text name, no price) | S | sheet §12a |
| E92 | Honesty line ("MantaHostels doesn't take payment ...") | S | sheet §12a |
| E93 | Email capture and "Save this trip" (logged out; one field) | S, P | sheet §12a; roadmap `redirect` (optional check-out date field; collection notice) |
| E94 | Exit interstitial (modal with a 2.2 s progress bar and "Stay here") | S | sheet §12a ("At most one interstitial"); corpus `HandoverInterstitial` |
| E95 | Toast ("Saved to your trips"; exit confirmation) | S | sheet §12a; corpus `Toast.jsx` and `HandoverToast` (ink pill) |
| E96 | Share control | none | no file specifies it |
| E97 | Save or wishlist heart | P (parked) | corpus `IconButton.prompt.md` example; roadmap `hostel-wishlist` (parked) |

### 1.5 Member and owner surfaces

| # | Element | Status | Where |
|---|---|---|---|
| E98 | Sign-in and sign-up screens | P | roadmap `db-auth-setup`, `member-account` (logged-out redirect) |
| E99 | Member account page (two progress bars, join control, accepted-documents list, email, sign-out, empty states) | P | roadmap `member-account`, `review-ux` |
| E100 | Points progress bars (review points unlock scan points) | P | roadmap `review-ux` |
| E101 | Reviewer badges and flair | P | roadmap `review-ux` |
| E102 | Review submission form | P | roadmap `review-ux`, `review-gates`; sheet §11 (warm register for review prompts) |
| E103 | Reward code and redemption confirmation | P | roadmap `rewards-engine`, `reward-codes` |
| E104 | Owner claim and verify flow | P | roadmap `owner-claim-verify` |
| E105 | Owner listing editor (photo upload, amenities, events) | P | roadmap `listing-editor` |
| E106 | Owner analytics dashboard (graphs) | P | roadmap `analytics-dash` |
| E107 | Partner sign-up, founding-partner rate, agreement screens | P | sheet §11 ("commitment surfaces" take the warm register) |
| E108 | PWA install prompt, offline state, push notice | P | roadmap `mobile-app` |

### 1.6 Primitives in the corpus, not yet placed on a live page

| # | Element | Status | Where |
|---|---|---|---|
| E109 | Button (primary, secondary, ghost, night-primary; sm, md, lg) | S | corpus `Button.jsx` |
| E110 | Icon button (ghost, filled, outline) | S | corpus `IconButton.jsx` |
| E111 | Status badge (success, warning, danger, rewards) | S | corpus `Badge.jsx`; sheet §3 (B20) |
| E112 | Text input (label, icon, focus, error) | S | corpus `Input.jsx`; sheet §10 (B47) |
| E113 | Select | S | corpus `Select.jsx` |
| E114 | Checkbox | S | corpus `Checkbox.jsx` |
| E115 | Radio | S | corpus `Radio.jsx` |
| E116 | Switch | S | corpus `Switch.jsx`; sheet §10 ("toggles and switch thumbs slide at the standard duration") |
| E117 | Tabs (underline) | S | corpus `Tabs.jsx` |
| E118 | Dialog (with scrim `rgba(10,53,66,0.45)`) | S | corpus `Dialog.jsx`; corpus `readme.md` "Transparency/blur" |
| E119 | Tooltip (ink) | S | corpus `Tooltip.jsx` |

Count: 119 elements. Built (B, first status): 17. Specified in a rules file or the corpus, not built (S first): 64. Planned only (P first): 30. Ruled out (X): 1. No file names it: 7 (E9 currency switch, E11 skip link, E38 autocomplete, E58 empty results, E59 loading state, E60 pagination, E96 share). Of the 64 `S` elements, 11 are marked "corpus only", and E41, E42 and E55 also get their form only from the corpus `readme.md`.

## 2. The rules that reach elements, by area

A rule that reaches every element of its class is a **site-wide rule** (suffix `g` in §3). A rule that names the element or its class is an **element rule**.

Finding 2.0. design-vault's own skills give **no element rule** for a web page. `design-critique` holds the craft gate (geometry and brand motion, G1-G6), page-level lenses (Gestalt, 5-second test, CTA count, credibility, SEO) and the change standard (`plugin/skills/design-critique/SKILL.md` §1a-§3). `design-round` holds process and brand-motion physics (census R1-R36). The House DNA is a ban list (D1-D12), and Manta does not take it (`design-round/SKILL.md:37-39`; Manta `design-process.md:13`). So for every Manta element, the element rules come from Manta's files only, and the fallback is impeccable.

### 2.1 Anatomy and structure

- Element rules: card anatomy (B38, B39), handover (B53), score display (B36), rating unit (B35), testimonial (X1), interior announcement (B3), nav (B7), hero wave (B42), review-card elements (B37), source line (sheet §11), availability states (X3, §12a). Research: none for B38, B39, B53, B36, X1, B3 (all `T` or `-` in the census). B7's mobile collapse agrees with NN/g 2016 (#104 W3: "Manta's `DESIGN.md` ... agrees with NN/g"). B40 (total price, declared once) agrees with the FTC fees rule and Baymard's fee finding (#104 W8: "Covered for Manta"). B49 (no urgency theatre) agrees with the FTC dark-patterns report (#104 W8).
- Corpus-only anatomy (`Rc` in §3): filter panel, comparison, gallery, rooms list detail, mobile card, mobile comparison, location block, toast, tooltip, dialog, tabs, form controls.
- Research that exists and that no house rule adopts: Baymard 2022 on accommodation search (#104 W7): "always show results in a split view, list beside an interactive map"; "vertical filter sidebars that crowd the list" are a pitfall, "horizontal filter and sort bars performed well"; users want room or bed-type filters. #104 ranks this gap 1.
- impeccable fallback: `operate.md` (skeletons, "empty states that teach the interface", "modal as first thought" is laziness), `onboard.md` (empty-state types, tooltips), `adapt.md` (bottom sheets, drawers, sticky headers), `harden.md` (empty, pagination, skip links, i18n, currency).

### 2.2 States

- Site-wide rules: hover "lightens or tints a ground", press 0.97 (B48, `R`); lagoon wash `#E6F6F8` for hover and selected only (B20, measured 5.3:1 and 11.8:1, `C`); error border `danger` (B47); error and sold-out never by colour alone (B19, CVD reasoning and WCAG 1.4.1 in #115 A2, `C`); "Design the failure states" (X3, `R`).
- Element rules: coral hover `#E64A28` and active `#CC3F1F` (sheet §3); zero reviews "No reviews yet" (B36); full room greyed, not hidden (X3, §12a); compare checkboxes "disable quietly" at 4 (corpus `readme.md`).
- Research: B19 only. No house rule covers loading, skeleton, empty-result or offline states. impeccable's craft floor asks "hover, disabled, loading, error, empty" for every element (`craft-floor.md` §Verify).

### 2.3 Surface styling (borders, shadows, radius, fills)

- Site-wide rules: "Borders first. `sand-border` at 1-1.5px ... box-shadow is reserved for hover and popover states" (B46, `R`, census Src `-`); radii 8 / 10-12 / 6 / 999 (B45, `R`); "UI is flat", gradients only in the mark (B18, `R`); tinted card grounds only for special rows (B17, `R`); "white means elevated and tappable, always" (`DESIGN.md` colour table, `R`).
- Element rules: card (white, `sand-border`, 10-12px), testimonial (no card chrome, one lagoon left rule, X1), verified-stay badge (lagoon edge at low alpha, B37), semantic chips (tinted fills, B20, contrast measured), hero wave (ink band, B42), nav (ink, B7), dialog scrim `rgba(10,53,66,0.45)` and "No frosted-glass/blur panels" (corpus `readme.md`).
- Research: none. #117 researches this area now.

### 2.4 Type

- Site-wide rules: Quicksand 700/600 display, Nunito Sans 400/600-700 body, body 14-15.5px at line-height ~1.6 (B28, `R`); sentence case, uppercase only for badges and filter labels (B30, `R`); no em dash in website copy (sheet §11 item 11, copy). The type scale in `docs/design-system/tokens/typography.css` has "No ratio and no derivation" (#115 T3).
- Element rules: primary coral CTA label Nunito Sans 700 at 19px or more (B29, measured against WCAG large text, `C`); disclosure at 12.5px minimum (B37); outline, ghost and row controls 13-16px (B29).
- Research against the house rule: Butterick, "body text of 15-25 pixels", and impeccable's "1rem / 16px as the ordinary web body floor" (#104 W5). #104 calls Manta's 14-15.5px body "a Manta rule on a dated convention". The built site sets the hero body and page meta at 14px (`app/globals.css:64`, `--text-body-sm: 400 0.875rem / 1.6`).
- Measure: 60-75 characters, and the `ch` pitfall (#115 T4, mantahostels#3429, measured, `C` for prose surfaces).

### 2.5 Colour

- Site-wide rules: one job per colour (B10, `R`); text-safe partner rule, every type colour measured against its grounds (B21, measured against WCAG AA, `C`); night pattern (B6, B22, measured, `C`); text on turquoise is ink (B4, measured 2.3:1 against 5.7:1, `C`); warm = act, cool = read (B16, `R`, no source, #115 C2).
- Element rules: coral for the one CTA (B12, `R`); amber for rewards only (B13, `R`); score chip ink on turquoise (B24, measured, `C`); rating unit lagoon, never on turquoise (B35, measured 1.59:1, `C`); mark grounds (B5, measured, `C`); links on ink white plus underline (B23, `R`); semantic chips (B20, measured, `C`).
- Research: the measured ratios count as research (Key, What counts as research). Colour harmony and near-miss rules (B26, B27) have no source (#115 C6, C9).

### 2.6 Spacing

- Site-wide rules: "8px spacing grid" (`DESIGN.md` §Layout; tokens 4-80px). "No derivation is recorded" (#115 S1). `R`.
- Element rules: nav heights 72/56 derived from the mark and the grid (B7, #115 S2, `R`); card padding `spacing.md`, button padding 12px 24px, chip padding 2px 8px, badge padding 2px 10px (`DESIGN.md` front matter, `R`); comparison rows at fixed shared heights (corpus, `Rc`); hero wave sizes and offsets (B42, acceptance-tested, `C`).
- Research: none. impeccable `layout.md` gives the general method (squint test, proximity, rhythm).

### 2.7 Motion

- Site-wide rules: "Fast 120ms, standard 180ms, easing `cubic-bezier(0.2, 0, 0, 1)` ... press scales to 0.97 ... no bounce or spring theatre ... Motion never announces itself" (B48, `R`). #104 W9 finds the no-bounce choice "consistent with M3's 'standard' (low-bounce) scheme for utilitarian UI" and "not dated". No source sets the 120 and 180 ms values. So §3 keeps `Rg`.
- Element rules: "toggles and switch thumbs slide at the standard duration" (sheet §10).
- Brand motion (hero wave, mark, illustration): the craft gate G3 (flow, ballistic fall, damped landing) and R32-R35 (`design-critique/SKILL.md` §1a; `design-round/SKILL.md:154-161`). Physics stated, not cited (census G3).
- Open: gesture settle for a drag (mantahostels#2988); scroll reveal in the hero (mantahostels#2989).
- Research that no Manta rule adopts: WCAG 2.3.3 and 2.2.2 for motion (#104 W9). Manta's sheet has no reduced-motion rule. The built CSS has one (`app/globals.css:865`, `@media (prefers-reduced-motion: reduce)`).

### 2.8 Accessibility

- Site-wide rules: WCAG AA text floor (X6, `C`); focus ring lagoon, ink on turquoise, never removed without a replacement (B47, measured 3:1, `C`); never colour alone (B19, `C`).
- Element rules: `aria-current="page"` on the nav (B8, `R`); 44px hit targets on the mobile card and the guest stepper (corpus `HostelCard.prompt.md`, `BookingHandover.jsx`, `Rc`).
- Research that no house rule adopts: WCAG 2.2 AA criteria 2.4.11 Focus Not Obscured, 2.5.7 Dragging Movements, 2.5.8 Target Size, 3.2.6 Consistent Help, 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication (#104 W1). #104: "Manta has a sticky compare bar and a sticky mobile handover bar (brand sheet §12a), so 2.4.11 applies directly. **Gap for Manta.**"
- impeccable fallback: `audit.md` (44px targets, keyboard), `harden.md` (focus management in modals, skip links), `critique.md` (Esc to dismiss a modal).

### 2.9 Responsive behaviour

- Element rules: nav collapse below 768px (`DESIGN.md` §Layout, agrees with NN/g, `C`); hero wave below 800 design units, zero mark pixels outside ink at 320-1920px (B42, `C`); mobile card stacked, photo 170px on top, 44px controls (corpus, `Rc`); mobile handover bar expanding into a sheet, honesty line always visible (§12a, `R`); 2-up mobile comparison (corpus, `Rc`).
- Process rule: render desktop, one intermediate width and mobile (census R12). This checks a candidate. It does not say how an element behaves.
- Research: #104 W10 (content-driven breakpoints, container queries, mobile-first indexing; "dated: device breakpoints"). No Manta rule adopts it. impeccable `adapt.md` is the fallback for every other element.


## 3. Matrix: element by area

How to read this table:

- `C` = house rule and research. `R` = house rule for this element, no research. `Rg` = site-wide rule only (no rule names this element). `Rc` = rule only in the corpus (`docs/design-system`, reference only; the sheet wins). `Cg` = site-wide rule with research (for example the WCAG AA text floor, X6). `I` = impeccable default only. `—` = nothing. `·` = the area does not apply.
- `+117` on a Surf cell: the surface-styling research in #117 covers this area for the element class (borders, shadows, radius, scrims, focus). No Manta rule adopts that research yet. See §6.
- Freq: how often a visitor meets the element. 5 = every page view. 4 = every search or every guide page view. 3 = every hostel detail view or a frequent action. 2 = a minority of visitors. 1 = owners and partners only. 0 = not shown.
- Context: function · zone · ground · density · device.
  - Function: N navigate, A act, I input, T trust or status, R read, D decorate or brand.
  - Zone: M marketing, W working (B1).
  - Ground: ink (night), tq (turquoise), sand, white, photo, map, scrim, ? (not decided).
  - Density: 1 = one on the view, n = repeated in a list.
  - Device: all, desk (desktop only), mob (mobile only).
- Rules and sources: the rule rows (B, X, R, G, F from census #98) and the files that hold element rules. `see Kn` points to §4.

| # | Element | St | Freq | Context | Anat | State | Surf | Type | Col | Space | Mot | A11y | Resp | Rules and sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1 | Nav, desktop | B,S | 5 | N·M+W·ink·1·desk | C | R | R+117 | Rg | C | R | Rg | C | C | B7, B8, B23, B47; NN/g 2016 via #104 W3; built guide h1 title case, see K8 |
| E2 | Nav, mobile (Menu, panel, scrim) | B,S | 5 | N·M+W·ink·1·mob | R | Rg | R+117 | Rg | C | R | Rg | C | R | DESIGN.md §Layout; B7; NN/g 2016 (#104 W3) says show 4 or fewer links, see K14 |
| E3 | Wordmark and lockup | B,S | 5 | D·M+W·ink/tq·1·all | R | · | · | R | C | · | · | C | R | B31, B4 exemption, B23 exemption; #115 L10 |
| E4 | Mark | B,S | 4 | D·M·ink/white/sand·1·all | C | · | · | · | C | · | R | C | C | B5, B32-B34 (px arithmetic, L*), B42; WCAG 1.4.11 logotype exemption (#115 L4); craft gate G1-G3 if animated |
| E5 | Sign in (outline) | S | 5 | A·M+W·ink·1·all | R | Rg | R+117 | R | R | R | Rg | C | R | B25; DESIGN.md button-outline; see K11 |
| E6 | Site footer | B,S | 5 | N/T·M+W·ink·1·all | Rc | Rg | R+117 | Rg | C | Rg | Rg | C | I | B2, B6, B23; corpus SiteFooter.jsx |
| E7 | Favicon, app icon, OG image | B | 3 | D·—·any·1·all | R | · | · | · | R | · | · | · | · | B33 (flat variant); no rule for the OG image |
| E8 | Language switch | P | 3 | I·M+W·ink?·1·all | — | I | Rg+117 | Rg | Cg | Rg | Rg | I | I | roadmap i18n only |
| E9 | Currency switch | none | 3 | I·W·?·1·all | — | — | Rg+117 | Rg | Cg | Rg | · | I | I | no file; impeccable harden.md (currency formats) |
| E10 | Cookie or consent notice | X | 0 | T·—·—·1·all | · | · | · | · | · | · | · | · | · | cut by #478 (cookieless analytics); not scored |
| E11 | Skip link | none | 5 | N·—·any·1·all | I | I | Rg+117 | Rg | Cg | · | · | I | · | no house rule; impeccable harden.md |
| E12 | 404 page | P | 2 | D/N·?·?·1·all | R | · | Rg+117 | Rg | Cg | Rg | · | Cg | I | sheet §6 (404 is a personality surface), §9, §11 (errors never witty), see K16 |
| E13 | Error and offline page | P | 2 | T·?·?·1·all | R | I | Rg+117 | Rg | Cg | Rg | · | Cg | I | sheet §9, §11; roadmap mobile-app |
| E14 | Focus ring | B,S | 5 | —·M+W·all grounds·n·all | · | C | R+117 | · | C | · | · | C | · | B47 (3:1 measured; ink on turquoise); WCAG 2.4.11 not adopted (#104 W1) |
| E15 | Hero (turquoise ground) | B,S | 4 | D/A·M·tq·1·all | R | · | R+117 | R | C | R | R | C | C | B1, B4, B5, B18, B42; mantahostels#2989 open, see K1 |
| E16 | Hero eyebrow; guide region label | B,S | 4 | R·M·tq/sand·1·all | R | · | · | R | C | Rg | · | C | I | sheet §2 line 26; see K3 |
| E17 | Hero headline and body | B,S | 4 | R·M·tq·1·all | R | · | · | R | C | Rg | R | C | I | B28, B50; built body 14px, see K9 |
| E18 | Hero CTA pair | B,S | 4 | A·M·tq·1·all | R | R | R+117 | C | C | R | Rg | C | I | B12, B25, B29; built pill radius, see K10 |
| E19 | Hero search box | S,P | 4 | A/I·M·tq·1·all | R | Rg | R+117 | C | C | Rc | Rg | I | Rc | sheet §3; corpus Homepage.jsx; Baymard (#104 W7) not adopted, see K19 |
| E20 | Hero wave with mascot | B,S | 4 | D·M·tq+ink·1·all | C | · | C | · | C | C | R | C | C | B42 (measured, acceptance-tested); B5 |
| E21 | Destination card grid (home) | B | 4 | N·M·sand/white·n·all | — | Rg | Rg+117 | Rg | Cg | Rg | Rg | Cg | I | site-wide B46, B45, B48 only |
| E22 | 'Popular right now' tiles | S | 3 | N·M·white·n·all | Rc | Rg | Rg+117 | Rg | C | Rc | · | Cg | Rc | corpus Homepage.jsx; B36 (breached by the corpus, see K12) |
| E23 | Destination hero | S | 4 | D·M·tq+ink·1·all | R | · | R+117 | R | C | C | R | C | C | B1, B42 (150 px) |
| E24 | Guide page body | B | 4 | R·M·sand·1·all | R | · | · | R | Cg | Rg | · | Cg | I | roadmap guide-pages; B28; measure #115 T4; see K9 |
| E25 | 'Good for' chips (static) | B | 4 | R·M·sand·n·all | Rg | · | Rg+117 | Rg | Cg | Rg | · | Cg | I | B45 (pill for tags); see K18 |
| E26 | Interior announcement block | B,S | 4 | T·M+W·ink·1·all | R | · | R+117 | Rg | C | Rg | · | C | I | B3, B2, B6 |
| E27 | Destination preview and 'See all N' | S | 4 | N/A·M·sand/white·n·all | Rc | Rg | Rg+117 | C | C | Rc | Rg | Cg | Rc | corpus readme 'never dead-end'; B29; see K6, K12 |
| E28 | Founding-reviewer email box | P | 4 | I·M·sand·1·all | R | I | Rg+117 | Rg | Cg | Rg | Rg | I | I | roadmap guide-pages ('no tick, no I agree'); Baymard validation (#104 W11) not adopted |
| E29 | Rewards screen | S,P | 2 | D·M·ink·1·all | Rc | · | Rc+117 | Rg | C | Rc | Rg | C | Rc | B2, B13; corpus RewardsScreen.jsx; see K7 |
| E30 | Partner spotlight page | P | 1 | T·M?·?·n·all | — | Rg | R+117 | Rg | Cg | Rg | · | Cg | I | B17 (tinted rows for partner spotlight); see K20 |
| E31 | Prose pages | B | 2 | R·?·sand·1·all | — | Rg | · | R | Cg | Rg | · | Cg | I | B28; measure #115 T4; see K9 |
| E32 | Insurance section | P | 1 | R·?·?·1·all | — | I | Rg+117 | Rg | Cg | Rg | · | Cg | I | roadmap insurance only |
| E33 | Illustration (guide hero, empty, 404, onboarding) | P | 3 | D·M·tq/sand·1·all | R | · | · | · | R | · | R | I | R | B41, B43, B14; vault F4, R17; #104 W6 (evidence rule not written), see K17 |
| E34 | Page background art (working area) | P | 4 | D·W·sand·1·desk | R | · | R+117 | · | R | · | · | C | R | mantahostels#3057-#3060; X9, R17; pass bar text-muted 4.5:1 (#3058); see K4 |
| E35 | Emails | P | 3 | N/T·M·?·1·all | Rg | · | Rg+117 | Rg | Cg | Rg | · | I | I | B1 (emails are a marketing zone); no email rule |
| E36 | Social tiles | P | 2 | D·M·ink·1·— | R | · | R+117 | Rg | C | — | R | I | · | B2, B6 |
| E37 | Destination search input (working) | S,P | 4 | I·W·white·1·all | Rc | R | Rg+117 | Rg | C | Rc | Rg | I | I | corpus Input.jsx; B47; see K13 |
| E38 | Search autocomplete | none | 4 | I·M+W·white·n·all | I | I | R+117 | Rg | Cg | Rg | Rg | I | I | no house rule; impeccable critique.md heuristic |
| E39 | Results header and price declaration | S | 4 | T·W·sand·1·all | C | · | · | Rg | Cg | Rc | · | Cg | I | B40 (FTC fees rule, Baymard, #104 W8); roadmap search-core |
| E40 | Sort control and 'how we rank' link | S | 4 | I·W·sand·1·all | R | Rg | Rg+117 | Rg | Cg | Rc | · | I | I | roadmap search-core; corpus Select.jsx; Baymard horizontal bars (#104 W7) |
| E41 | Map toggle | S | 4 | N·W·sand·1·all | Rc | Rg | Rg+117 | Rg | Cg | Rc | · | Cg | I | corpus SearchResults.jsx; Baymard split view (#104 W7) not adopted, see K19 |
| E42 | Filter panel, desktop | S | 4 | I·W·white·1·desk | Rc | Rc | Rc+117 | R | R | Rc | Rc | I | Rc | corpus readme 'Filter panel'; search-core; B30; Baymard (#104 W7), see K19 |
| E43 | Filter chip (Tag) | S | 4 | I·W·white·n·all | Rc | Rc | R+117 | Rg | C | Rc | Rg | I | Rc | corpus Tag.jsx; B45, B20 |
| E44 | Mobile filters | S | 4 | I·W·sand·1·mob | Rc | Rc | Rg+117 | Rg | Cg | Rc | — | I | Rc | corpus mobile.html (chip rail); Baymard does not cover mobile (#104 W7) |
| E45 | Listing card (row / stacked) | S | 4 | N/R·W·white on sand·n·all | R | R | R+117 | R | C | R | Rg | Cg | Rc | B38, B39, B46, B17, B36; corpus HostelCard; see K6 |
| E46 | Card photo with carousel dots | S | 4 | D/N·W·photo·n·all | R | I | —+117 | · | — | · | I | I | Rc | B38; no rule for controls on a photo; see K15 |
| E47 | Compound rating line | S | 4 | T/R·W·white·n·all | R | R | R+117 | R | C | R | · | C | Rc | B36, B39, B24, B45 |
| E48 | 'No reviews yet' | S | 3 | T·W·white·n·all | R | R | · | Rg | Cg | · | · | Cg | · | B36 (#373) |
| E49 | Price block | S | 4 | T/R·W·white·n·all | C | · | · | Rc | Cg | Rc | · | Cg | Rc | B40 (#104 W8); B38 |
| E50 | Facts line, flavour line | S | 4 | R·W·white·n·all | R | · | · | R | Cg | Rc | · | Cg | Rc | B38 |
| E51 | Amenity icons | S | 4 | R·W·white·n·all | R | I | · | · | C | Rc | · | I | Rc | B38, B44; tooltip by title only |
| E52 | Compare checkbox (max 4) | S | 4 | I·W·white·n·all | C | Rc | Rc+117 | Rg | R | Rc | · | I | Rc | corpus readme (Cowan 2001 via impeccable critique.md, #115 S5) |
| E53 | 'View beds' row button | S | 4 | A·W·white·n·all | R | Rg | R+117 | R | R | R | Rg | Cg | Rc | B25, B29; DESIGN.md button-outline |
| E54 | Sticky compare bar | S | 4 | A·W·sand·1·all | R | Rc | Rc+117 | C | C | Rc | Rg | — | I | B25, B29; WCAG 2.4.11 (#104 W1) not adopted; see K24 |
| E55 | Comparison view | S | 3 | R·W·sand/white·n·all | Rc | Rc | Rc+117 | Rc | R | Rc | · | I | Rc | corpus readme 'Comparison rules'; #115 S5, S6; see K5, K8 |
| E56 | Mobile comparison (2-up swipe) | S | 3 | R·W·sand·n·mob | Rc | I | Rg+117 | Rg | Cg | Rc | I | I | Rc | corpus MobileComparison.jsx; WCAG 2.5.7 (#104 W1) not adopted |
| E57 | Empty compare state | S | 2 | T·W·sand·1·all | Rc | Rc | · | Rg | Cg | Rc | · | Cg | I | corpus Comparison.jsx; impeccable onboard.md |
| E58 | Empty results | none | 3 | T·W·sand·1·all | Rg | I | Rg+117 | Rg | Cg | Rg | · | I | I | X3 (site-wide); impeccable clarify.md, onboard.md |
| E59 | Loading state of results | none | 4 | T·W·sand·n·all | I | I | Rg+117 | · | Cg | · | Rg | I | I | no house rule; impeccable operate.md (skeletons); PRODUCT.md 'poor connectivity' |
| E60 | Pagination or load more | none | 3 | N·W·sand·1·all | I | I | Rg+117 | Rg | Cg | Rg | · | I | I | no house rule; impeccable harden.md |
| E61 | Map view (map, pins, clusters, pin card) | P | 4 | N/R·W·map·n·all | — | — | —+117 | Rg | Rg | — | — | — | — | roadmap map-view (tiles only); Baymard (#104 W7), WCAG 2.5.7 (#104 W1) not adopted |
| E62 | Map bottom sheet, mobile | P | 4 | N·W·white·1·mob | I | I | Rg+117 | Rg | Cg | Rg | R | — | I | mantahostels#2988; B48; see K1 |
| E63 | Availability section | S,P | 3 | T·W·white·n·all | R | R | Rg+117 | Rg | C | Rg | · | C | I | X3, B19, B20; roadmap avail; see K21 |
| E64 | Demand signal ('often books out') | P | 3 | T·W·white·n·all | R | · | Rg+117 | Rg | R | Rg | · | Cg | I | roadmap sell-out; B49, B13; see K2 |
| E65 | Partner filter and partner badge | P | 3 | I/T·W·white·n·all | R | Rg | R+117 | R | R | R | · | Cg | I | roadmap search-core; PRODUCT.md merit ranking; B17, B30, B13 |
| E66 | Review-keyword search | P | 3 | I·W·white·1·all | — | I | Rg+117 | Rg | Cg | Rg | · | I | I | roadmap search-core only |
| E67 | Date picker | P | 3 | I·W·white·1·all | Rc | I | Rg+117 | Rg | Cg | Rg | Rg | I | I | sheet §12a (dates prefill exits); Baymard (#104 W7), WCAG 3.3.7 (#104 W1) not adopted; see K19 |
| E68 | Guest stepper | S | 3 | I·W·white·1·all | Rc | Rc | Rc+117 | Rg | Cg | Rc | · | Rc | Rc | corpus BookingHandover.jsx (44 px) |
| E69 | Back link | S | 3 | N·W·sand·1·all | Rc | Rg | · | Rg | C | Rg | · | Cg | I | corpus HostelDetail.jsx; B21 (lagoon-text) |
| E70 | Photo gallery | S | 3 | D/R·W·photo·1·all | Rc | I | —+117 | Rg | — | Rc | Rc | I | Rc | corpus Gallery (HostelDetail.jsx:33, 220 ms); no rule for controls on a photo; see K15 |
| E71 | 'Photos coming soon' | S,P | 2 | T·W·sand·1·all | Rc | R | · | Rg | Cg | · | · | Cg | · | corpus; roadmap seed-listings; X3 |
| E72 | Detail header | S | 3 | R/T·W·sand·1·all | R | R | · | R | C | Rc | · | Cg | Rc | B36, B35; corpus DetailHeader |
| E73 | Rating unit (five mantas) | S | 3 | T·W·white/sand/ink·n·all | C | R | · | · | C | R | · | C | · | B35 (measured; revised v2.2 on 1.2:1) |
| E74 | Rating-unit 'full rating' animation | P | 2 | D·W·white·1·all | R | · | · | · | R | · | R | I | · | roadmap review-ux; B35, B48; see K1 |
| E75 | Quick-facts tags | S | 3 | R·W·sand·n·all | Rc | · | Rg+117 | Rg | Cg | Rc | · | Cg | Rc | corpus QuickFacts; see K18 |
| E76 | Rooms and beds rows | S | 3 | R/T·W·white·n·all | R | R | Rc+117 | Rc | C | Rc | · | C | Rc | sheet §12a; X3; see K21 |
| E77 | Availability chip | S | 3 | T·W·white·n·all | R | R | R+117 | Rg | C | Rc | · | C | Rc | sheet §12a, B20, B19; see K5 |
| E78 | Source line | S | 3 | T·W·white·n·all | C | · | · | Rc | Cg | · | · | Cg | · | sheet §11 'The source line'; #104 W8 |
| E79 | Category sub-score bars | S | 3 | R·W·white·n·all | R | · | Rc+117 | Rc | R | Rc | · | Cg | Rc | B36; corpus Reviews |
| E80 | Review card | S | 3 | R/T·W·white·n·all | R | R | Rc+117 | Rc | C | Rc | · | Cg | Rc | B37, X1, B24; roadmap review-ux; see K23 |
| E81 | 'Verified stay' badge | S | 3 | T·W·white·n·all | R | · | R+117 | Rc | C | Rc | · | Cg | · | B37 |
| E82 | 'Reviewer earns rewards' disclosure | S | 3 | T·W·white·n·all | R | · | · | R | Cg | · | · | Cg | · | B37; §15 placement open |
| E83 | Most-recent stay month | P | 3 | T·W·white·1·all | R | · | · | Rg | Cg | · | · | Cg | · | roadmap review-ux (#979) |
| E84 | Hostel testimonial pull-quote | S | 2 | T·W·sand·1·all | R | · | R+117 | R | Cg | Rg | · | Cg | I | X1; see K3 |
| E85 | Location block | S | 3 | R/N·W·white·1·all | Rc | Rg | Rc+117 | Rg | C | Rc | · | Cg | I | corpus PageFooter; Baymard 'location is primary' (#104 W7) |
| E86 | Full amenities checklist | S | 3 | R·W·white·1·all | Rc | · | · | Rc | C | Rc | · | Cg | I | corpus PageFooter; B30; see K8 |
| E87 | 'Own this hostel?' claim link | S,P | 3 | A·W·sand·1·all | Rc | Rg | · | Rg | C | · | · | Cg | I | corpus; roadmap seed-listings |
| E88 | Handover module, desktop | S | 3 | A/T·W·white·1·desk | R | R | Rc+117 | C | C | Rc | · | Cg | R | B53 (§12a); #104 W7, W8 support parts |
| E89 | Handover bar and sheet, mobile | S | 3 | A/T·W·white·1·mob | R | R | Rc+117 | C | C | Rc | Rg | — | R | B53; WCAG 2.4.11 (#104 W1) not adopted; see K24 |
| E90 | Coral exit 'Book direct with the hostel' | S | 3 | A·W·white·1·all | R | R | R+117 | C | C | R | Rg | C | R | B53, B12, B29 |
| E91 | OTA exit buttons | S | 3 | A·W·white·n·all | R | Rg | R+117 | Rc | R | Rc | · | Cg | R | B53; X4 |
| E92 | Honesty line | S | 3 | T·W·white·1·all | C | · | · | Rc | Cg | · | · | Cg | R | B53; NN/g upfront disclosure (#104 W8) |
| E93 | Email capture, 'Save this trip' | S,P | 3 | I·W·white·1·all | R | I | Rc+117 | Rg | C | Rc | · | I | I | sheet §12a; roadmap redirect; see K13 |
| E94 | Exit interstitial | S | 3 | T·W·scrim·1·all | R | Rc | Rc+117 | Rg | R | Rc | Rc | I | I | sheet §12a; corpus HandoverInterstitial; see K22 |
| E95 | Toast | S | 3 | T·W·ink/white·1·all | R | Rc | Rc+117 | Rg | R | Rc | Rg | I | I | sheet §12a; corpus Toast.jsx and HandoverToast; see K5 |
| E96 | Share control | none | 3 | A·W·white·1·all | — | — | Rg+117 | Rg | Cg | Rg | · | I | I | no file |
| E97 | Save (heart) | P | 2 | A·W·white·n·all | Rc | I | Rc+117 | · | R | Rc | Rg | Rc | I | corpus IconButton; roadmap hostel-wishlist (parked) |
| E98 | Sign-in and sign-up | P | 2 | I·?·?·1·all | — | I | Rg+117 | Rg | Cg | Rg | Rg | — | I | roadmap db-auth-setup; WCAG 3.3.8 (#104 W1) not adopted |
| E99 | Member account page | P | 2 | R·?·?·1·all | R | I | Rg+117 | Rg | Cg | Rg | · | I | I | roadmap member-account; consent banner cut (#478) |
| E100 | Points progress bars | P | 2 | R·?·?·n·all | R | R | —+117 | Rg | R | — | Rg | I | I | roadmap review-ux; B13 |
| E101 | Reviewer badges and flair | P | 2 | D/T·W·white·n·all | R | · | R+117 | R | R | · | · | Cg | · | roadmap review-ux; B13, B30, B45 |
| E102 | Review submission form (incl. rating input) | P | 2 | I·?·?·1·all | — | I | Rg+117 | Rg | Cg | Rg | Rg | I | I | roadmap review-ux, review-gates; sheet §11 (warm register) |
| E103 | Reward code and redemption confirmation | P | 2 | T·M?·ink?·1·mob | R | R | Rg+117 | Rg | C | Rg | — | I | I | roadmap rewards-engine; B2, B13 |
| E104 | Owner claim and verify flow | P | 1 | I·—·?·1·all | — | I | Rg+117 | Rg | Cg | Rg | · | I | I | roadmap owner-claim-verify |
| E105 | Owner listing editor | P | 1 | I·—·?·1·all | — | I | Rg+117 | Rg | Cg | Rg | Rg | I | I | roadmap listing-editor |
| E106 | Owner analytics dashboard | P | 1 | R·—·?·n·desk | — | I | Rg+117 | Rg | Cg | Rg | · | I | I | roadmap analytics-dash; impeccable hero-metric refusal applies, see K7 |
| E107 | Partner sign-up and agreement screens | P | 1 | I·—·?·1·all | — | I | Rg+117 | Rg | Cg | Rg | · | I | I | sheet §11 (commitment surfaces: warm register) |
| E108 | PWA install, offline, push | P | 2 | T·—·?·1·mob | — | I | Rg+117 | Rg | Cg | Rg | Rg | I | I | roadmap mobile-app |
| E109 | Button (all variants) | S | 5 | A·M+W·any·n·all | R | R | R+117 | C | C | R | R | C | I | DESIGN.md button tokens; B12, B25, B29, B48; see K10 |
| E110 | Icon button | S | 3 | A·W·white·n·all | Rc | I | Rc+117 | · | R | Rc | Rg | Rc | I | corpus IconButton.jsx; B12 |
| E111 | Status badge | S | 3 | T·W·white·n·all | R | · | R+117 | R | C | R | · | C | · | B20, B30, B45; corpus Badge.jsx |
| E112 | Text input | S | 3 | I·W·white·1·all | Rc | R | Rg+117 | Rg | C | Rc | Rg | I | I | corpus Input.jsx; B47; see K13 |
| E113 | Select | S | 3 | I·W·white·1·all | Rc | R | Rg+117 | Rg | Cg | Rc | · | I | I | corpus Select.jsx; B47; see K13 |
| E114 | Checkbox | S | 4 | I·W·white·n·all | Rc | R | Rc+117 | Rg | R | Rc | · | I | I | corpus Checkbox.jsx; see K13 |
| E115 | Radio | S | 3 | I·W·white·n·all | Rc | R | Rc+117 | Rg | R | Rc | Rc | I | I | corpus Radio.jsx; see K13 |
| E116 | Switch | S | 2 | I·W·white·1·all | Rc | R | Rc+117 | Rg | R | Rc | R | I | I | corpus Switch.jsx; sheet §10 (thumb slides at standard duration) |
| E117 | Tabs | S | 2 | N·W·sand·1·all | Rc | Rc | Rc+117 | Rg | Cg | Rc | Rg | I | I | corpus Tabs.jsx |
| E118 | Dialog | S | 2 | T·W·scrim·1·all | Rc | Rc | Rc+117 | Rg | R | Rc | Rg | I | I | corpus Dialog.jsx, readme 'Transparency/blur'; see K22 |
| E119 | Tooltip | S | 3 | T·W·ink·1·all | Rc | I | Rc+117 | Rg | R | Rc | Rg | I | I | corpus Tooltip.jsx; see K5 |

### 3.1 Totals by area (119 rows; `+117` not counted as a code)

| Area | C | Cg | R | Rc | Rg | I | — | · |
|---|---|---|---|---|---|---|---|---|
| Anatomy | 9 | 0 | 53 | 31 | 3 | 5 | 16 | 2 |
| States | 1 | 0 | 24 | 12 | 17 | 28 | 3 | 34 |
| Surface | 1 | 0 | 27 | 23 | 38 | 0 | 4 | 26 |
| Type | 8 | 0 | 19 | 10 | 68 | 0 | 0 | 14 |
| Colour | 43 | 48 | 24 | 0 | 1 | 0 | 2 | 1 |
| Spacing | 2 | 0 | 13 | 46 | 36 | 0 | 3 | 19 |
| Motion | 0 | 0 | 11 | 4 | 33 | 2 | 3 | 66 |
| Accessibility | 24 | 38 | 0 | 3 | 0 | 47 | 5 | 2 |
| Responsive | 5 | 0 | 10 | 25 | 0 | 63 | 1 | 15 |

Findings from the totals:

1. Colour and accessibility contrast have the most research. The text-safe colour rule (B11, B47, X6) has measured values. Most elements get `C` or `Cg` there.
2. Type and spacing are almost all `Rg` or `Rc`. A site-wide scale exists. No research supports the scale (#115 T2-T4, S1). Only the CTA label rule (B29: white on coral at 19px/700, measured) gives a type `C`.
3. Motion has no `C`. The only motion research (#104 W9) supports "no bounce". It does not support the 120/180 ms values or the easing (B48).
4. Accessibility beyond contrast is the largest `I` group (47 rows). WCAG 2.2 AA criteria (2.4.11, 2.5.7, 2.5.8, 3.3.7, 3.3.8) are researched in #104 W1, but no Manta rule adopts them. Every input, every sticky bar and every drag control is in this group.
5. Responsive behaviour is `I` for 63 rows. Element rules exist only for the nav, the hero wave, the mobile card, the handover bar and mobile comparison.
6. States are `I` for 28 rows. Most are inputs and planned surfaces. The corpus holds hover and selected states for some controls. The sheet holds states only for buttons, focus, the rating unit and availability.

## 4. Conflicts between house rules (input for #121)

Scope: a conflict is two held rules that cannot both be true for one element, or a held rule that a built or specced element breaks, or a held rule that research contradicts.

### 4.1 Rule against rule

- **K1. Spring and announced motion against B48.** B48: "no bounce or spring; motion never announces itself". (a) mantahostels#2988 (open) asks a drag settle for the map bottom sheet (E62). (b) The `review-ux` roadmap card: "the last manta pops larger and the row shifts colour with a small animation" (E74). This also touches B35 (the rating unit has fixed colours) and B10 (turquoise has three jobs). (c) mantahostels#2989 (open) asks a hero scroll reveal (E15). B1 lets the marketing zone be loud; B48 says no motion announces itself. No rule says which wins in the marketing zone. Census #98 holds the vault side of this (vault R34, R35, G3 permit spring). Research: #104 W9 supports "no bounce" only.
- **K2. Demand signals against B49.** The `sell-out` roadmap card plans "often books out ~3 days ahead" and "high interest for your dates" (E64). B49 bans urgency. The FTC dark-patterns research in #104 W8 supports B49. The card text and the rule cannot both ship as written. A neutral, true, dated fact may satisfy both; no rule says so.
- **K3. impeccable refusals that Manta overrides with no recorded ruling.** (a) Eyebrow: impeccable craft-floor refuses the eyebrow. Sheet §2 permits "hero eyebrows". Built: the home hero eyebrow and the guide region label (E16). Corpus: "Indonesia · Bali" (DestinationHero). (b) Coloured left rule: craft-floor refuses a coloured border-left above 1px on cards and callouts. DESIGN.md gives the testimonial pull-quote "a single lagoon left rule" (X1, E84). The width is not stated. #117 A1 notes that a quotation rule is an old print convention, so the override may be in scope. Census #98 records both as unrecorded overrides.
- **K4. Page background art in the working zone.** B1 keeps the working zone quiet. mantahostels#3057-#3060 (open) plan background art in the working area (E34). The founder's principles in #3057 (haze, low detail, type has priority) and the pass bar in #3058 (text-muted 4.5:1 over the art) are the proposed resolution. No sheet rule holds them yet.
- **K5. Turquoise and ink outside their named jobs.** B10 gives turquoise three jobs. B2 names the night (ink) contexts. Sheet §3 says success is "leafier than turquoise", so turquoise is not a success colour. Elements that break this: (a) corpus AvailChip "yes" = turquoise tint with lagoon-text, and "no" = sand-border fill (E77). These are not the success or danger tokens (B20). (b) Comparison "best score" and "best price" rows in turquoise tint (E55). B17 also limits tinted rows to the partner spotlight. (c) Ink Toast (corpus HandoverToast), ink Tooltip (corpus Tooltip.jsx), and an ink photo-count pill on the gallery (E95, E119, E70). B2 does not name these as night contexts. The corpus Toast.jsx is white with a coloured border, so the corpus has two toast styles.
- **K6. Shadow at rest against B46.** B46 and DESIGN.md:183: "box-shadow is reserved for hover and popover states. Nothing sits at rest under a heavy shadow." Corpus elements with a rest shadow: search result rows and HostelCard.jsx:78 (`--shadow-card`, E45), destination preview rows (E27), the homepage hero search box (`--shadow-popover`, E19). The built `.dest-card` has no rest shadow (globals.css:626). #117 B2.1 (Polaris, Atlassian) supports B46 for dense lists, and permits a small rest shadow for one pressable card among static content. "Heavy" in B46 is not defined, so `--shadow-card` (0 1px 2px) may be in or out of the rule.
- **K7. Big-number stat tiles.** impeccable craft-floor refuses the "hero-metric" template. Corpus RewardsScreen (E29) has stat tiles. The planned owner analytics dashboard (E106) will meet the same refusal. No Manta rule rules on it.
- **K8. Case rules (B30).** B30: sentence case; uppercase only for badges and filter labels. Breaches: uppercase column headings in the corpus SiteFooter (E6), uppercase row labels in the corpus Comparison (E55), the uppercase location and amenities labels in the corpus HostelDetail PageFooter (E85, E86). The built guide page h1 "Best Hostels in {name}" is title case (`app/best-hostels-in/[place]/page.tsx`), against B30 and sheet §11 item 9.
- **K10. Button shape.** B45 and corpus Button: controls take `radius-control` 8px. The built `.btn` has a pill radius (globals.css:553). The hero CTA pair (E18) and the generic button (E109) differ between the build and the rule. #117 B3.3 (Apple WWDC25) says capsules suit touch layouts and standout actions, and rounded rectangles suit dense desktop rows, so both shapes have a place. No rule says which goes where.
- **K11. Outline button on a night ground.** DESIGN.md button-outline is 1.5px ink. The nav (E1, E5) and footer are ink. No rule gives the outline colour on ink. This is a gap more than a conflict. It becomes a conflict when Sign in (E5) is built.
- **K12. Score and proof rules.** B36: a score always shows with its review count and a word. The corpus Homepage "Popular right now" tiles (E22) show score and count with no word. The corpus readme still says preview rows carry a "Top Rated pill" (E27). B51 removed that pill. The Manta design-review gate checks B36 in each review, so a build from the corpus would fail the gate.
- **K16. The 404 page tone.** Sheet §6 names the 404 as a personality surface. Sheet §11 says error messages are never witty. A 404 is an error state. The two lines may conflict for E12. No line says which wins.
- **K17. Illustration as filler.** B41 and B43 permit illustration on the guide hero, empty states, the 404 and onboarding (E33). #104 W6 finds that the evidence rule ("an image earns its place by carrying information or a deliberate feeling, else it is filler") is not written down. Sheet §14 item 6 logs a hypothesis that an illustration hero on SEO pages may convert worse than a photo. No test result is held.
- **K18. Static chips that look like filter chips.** The 'Good for' chips (E25) and the quick-facts tags (E75) use the pill shape of the selectable Tag (E43). B45 gives the pill to tags without a split by function. #104 W3 (NN/g flat signifiers) says a static item that looks interactive costs the user. No rule tells a static chip from a selectable chip.
- **K20. Paid partners against merit ranking.** PRODUCT.md: ranking is never bought. B17 permits a tinted row for the partner spotlight. The `search-core` card plans a partner filter and the roadmap plans a partner badge (E65, E30). No rule says how a paid relationship is marked in results. The FTC endorsement-disclosure research is not held in #104 or #115.
- **K21. Availability exits.** The `avail` card plans a date-prefilled "Book" deep-link per hostel (E63, E76). B25 and the design-review gate ban "Book" as a row CTA. The card also plans greyed full hostels. B19 says never colour alone, and WCAG exempts only disabled controls from contrast. A greyed row is content, not a disabled control.
- **K22. The exit interstitial.** Sheet §12a and the corpus HandoverInterstitial (E94) show a modal with a 2.2 s progress bar (BookingHandover.jsx:10) and then leave the site. (a) impeccable refuses a modal without need. (b) WCAG 2.2.1 (Timing Adjustable) is not researched for this auto-redirect. (c) The corpus copy "Leave a review afterwards to earn rewards" conflicts with sheet §13, which says the handover carries no invitation to review. (d) The 2.2 s bar is far longer than the B48 durations, but it shows progress, not UI motion, so B48 may not apply.
- **K23. Review card left accent.** X1 (from DESIGN.md only) and the craft-floor refusal of a coloured left border meet again if the review card (E80) takes the testimonial style. The corpus review card does not. No rule keeps the two apart.

### 4.2 Rule against research

- **K9. Body size.** The built hero body and page meta use `--text-body-sm` 14px. The sheet type scale has body text at 14-15.5px. #104 W5: Butterick gives 15-25px for body text; impeccable sets a 16px floor; #104 labels Manta's 14-15.5px "dated". Elements: E17, E24, E31, and every reading surface in the `Rg` type cells.
- **K13. Form control edges and focus (from #117 A1).** The corpus Input, Select and Checkbox borders are 1.5px sand-border, measured at 1.24:1 on white. WCAG 1.4.11 asks 3:1 when the edge is the only identifier (#117 B1.1). This is a probable failure for E37, E112, E113, E114, E52 and the unchecked compare box. The corpus Input sets `outline: none` and shows focus as a border change to lagoon. B47 says the ring is "never removed without a replacement". The replacement changes by 2.94:1 at 1.5px, so it passes 2.4.7 (AA) but fails 2.4.13 (AAA) (#117 B7.1). The checkbox radius (5px) is outside the B45 scale.
- **K14. Mobile nav collapse.** DESIGN.md §Layout collapses the nav behind "Menu" below 768px (E2). The built nav has two links (`app/_components/Nav.tsx`, NAV_LINKS: "Destinations", "How we rank"). #104 W3 (NN/g 2016) says that on mobile, 4 or fewer links show better than a hidden menu. #104 says the Manta rule "agrees" with NN/g. For a 2-link nav it does not.
- **K15. Controls on photographs.** No rule covers a control on a photo. The corpus uses white dots at 55% with a 2px ink halo on card photos (HostelCard.jsx:24, E46) and an ink count pill plus arrows on the gallery (E70). The gallery changes photo with a 220 ms background transition (HostelDetail.jsx:33, MobileHostelDetail.jsx:26), which is longer than the B48 180 ms. #104 W3 (NN/g) says a carousel must not auto-rotate. No rule says so. WCAG 2.5.7 (drag alternative) applies to a swipe gallery; no rule adopts it.
- **K19. Search, filter and map layout.** The corpus SearchResults has a 240px vertical filter panel and a map toggle (E41, E42). #104 W7 (Baymard) finds that a split list-and-map view and horizontal filter bars perform better on accommodation sites. No Manta rule adopts the research. The roadmap `map-view` card names only the tile stack (MapLibre, PMTiles). The date picker (E67) and hero search box (E19) have the same position: research exists, no rule.
- **K24. Sticky bars and hidden focus.** The sticky compare bar (E54) and the sticky mobile handover bar (E89) can hide a focused element. WCAG 2.4.11 (AA, new in 2.2) is researched in #104 W1 and #117 B7.1. No Manta rule adopts it. #117 B7.1 gives a resolution (scroll padding).

### 4.3 Drift between the files that hold the rules

- **K25. Scrim colour (from #117 A1).** The built mobile-nav scrim is `rgb(0 0 0 / .4)` with a panel shadow `rgb(0 0 0 / .2)` (globals.css:387, 409). The corpus Dialog scrim is `rgba(10,53,66,.45)`, tinted with ink (Dialog.jsx:7). No rule names a scrim. Elements: E2, E94, E118.
- **K26. Stale version pointers.** DESIGN.md and PRODUCT.md name sheet v2.32; the sheet is v2.37. The corpus is reconciled to v2.18. X1-X3 live only in DESIGN.md. A rule in the corpus (`Rc`) can be 19 sheet versions old. Census #98 holds the same drift.
- **K27. Hover with two signals (from #117 A1, B2.3).** The built `.dest-card:hover` changes the border to lagoon and adds a shadow (globals.css:627-629). Atlassian says use one or the other; Material combines them. The impeccable detector flags "hairline border plus wide diffuse shadow". No Manta rule covers it. Elements: E21, E45.


## 5. Least-covered elements, ranked by how often a visitor meets them

Method:

- Each applicable cell gets a weight: `C` 4, `Cg` 3, `R` 3, `Rc` 2, `Rg` 1.5, `I` 1, `—` 0. `·` cells are not counted. These weights are my choice. They put a corpus-only rule below a sheet rule because the corpus is reference only and can be 19 versions old (K26).
- Gap = 4 minus the mean weight of the element's cells. Rank score = Freq × gap.
- A different weight set can change the order. The ranking was not tested against other weights.

| Rank | # | Element | St | Freq | Mean weight | Cells `I` or `—` | Main missing areas |
|---|---|---|---|---|---|---|---|
| 1 | E61 | Map view (map, pins, clusters, pin card) | P | 4 | 0.33 | 7 of 9 | all except type and colour; Baymard research (#104 W7) held but not adopted |
| 2 | E11 | Skip link | none | 5 | 1.50 | 3 of 6 | anatomy, states, a11y; not in the build |
| 3 | E46 | Card photo with carousel dots | S | 4 | 1.14 | 5 of 7 | colour and surface on a photo, states, a11y (K15) |
| 4 | E59 | Loading state of results | none | 4 | 1.43 | 4 of 7 | all; PRODUCT.md names poor connectivity |
| 5 | E62 | Map bottom sheet, mobile | P | 4 | 1.50 | 4 of 9 | anatomy, states, a11y (WCAG 2.5.7), motion conflict K1 |
| 6 | E38 | Search autocomplete | none | 4 | 1.61 | 4 of 9 | anatomy, states, a11y, responsive |
| 7 | E21 | Destination card grid (home) | B | 4 | 1.61 | 2 of 9 | no element rule at all; built (K27) |
| 8 | E44 | Mobile filters | S | 4 | 1.67 | 2 of 9 | motion, a11y; Baymard does not cover mobile |
| 9 | E28 | Founding-reviewer email box | P | 4 | 1.67 | 3 of 9 | states, a11y, responsive |
| 10 | E6 | Site footer | B,S | 5 | 2.22 | 1 of 9 | responsive; element rules only in the corpus (K8) |
| 11 | E40 | Sort control and 'how we rank' link | S | 4 | 1.81 | 2 of 8 | a11y, responsive |
| 12 | E25 | 'Good for' chips (static) | B | 4 | 1.86 | 1 of 7 | static-versus-selectable cue (K18) |
| 13 | E96 | Share control | none | 3 | 1.19 | 4 of 8 | all |
| 14 | E9 | Currency switch | none | 3 | 1.19 | 4 of 8 | all; prices show only "Rp" |
| 15 | E41 | Map toggle | S | 4 | 1.94 | 1 of 8 | layout ruled only by the corpus (K19) |
| 16 | E114 | Checkbox | S | 4 | 1.94 | 2 of 8 | a11y edge 1.24:1 (K13) |
| 17 | E37 | Destination search input (working) | S,P | 4 | 1.94 | 2 of 9 | a11y, focus (K13) |
| 18 | E70 | Photo gallery | S | 3 | 1.28 | 4 of 9 | colour, states, a11y on a photo (K15) |
| 19 | E66 | Review-keyword search | P | 3 | 1.31 | 4 of 8 | anatomy and every state |
| 20 | E8 | Language switch | P | 3 | 1.33 | 4 of 9 | anatomy, states, a11y, responsive |
| 21 | E60 | Pagination or load more | none | 3 | 1.44 | 4 of 8 | all |
| 22 | E43 | Filter chip (Tag) | S | 4 | 2.11 | 1 of 9 | a11y |
| 23 | E42 | Filter panel, desktop | S | 4 | 2.11 | 1 of 9 | layout conflict with research (K19) |
| 24 | E58 | Empty results | none | 3 | 1.50 | 3 of 8 | states, a11y, responsive |
| 25 | E67 | Date picker | P | 3 | 1.56 | 3 of 9 | states, a11y (WCAG 3.3.7), responsive |

Ranks 26 to 118, in order (element, rank score): E54 7.3; E51 7.3; E35 7.3; E52 7.2; E56 7.0; E119 7.0; E110 6.6; E27 6.4; E2 6.4; E113 6.4; E95 6.3; E39 6.3; E24 6.3; E19 6.2; E93 6.2; E94 6.2; E115 6.2; E112 6.2; E5 6.1; E55 6.0; E68 5.8; E69 5.8; E64 5.8; E53 5.8; E26 5.7; E85 5.6; E75 5.6; E98 5.6; E87 5.5; E22 5.4; E50 5.3; E49 5.3; E108 5.3; E102 5.3; E86 5.0; E16 5.0; E100 4.9; E17 4.9; E79 4.7; E63 4.7; E45 4.7; E99 4.6; E89 4.5; E118 4.4; E117 4.4; E109 4.4; E1 4.4; E97 4.4; E103 4.3; E91 4.3; E65 4.3; E31 4.3; E18 4.2; E33 4.2; E83 4.1; E80 4.1; E13 4.1; E48 3.9; E116 3.9; E57 3.9; E12 3.9; E76 3.8; E36 3.6; E77 3.6; E47 3.5; E81 3.5; E72 3.4; E29 3.2; E34 3.2; E3 3.0; E92 3.0; E88 3.0; E84 3.0; E82 3.0; E78 3.0; E74 3.0; E71 3.0; E7 3.0; E107 2.7; E106 2.7; E104 2.7; E105 2.7; E90 2.5; E15 2.5; E32 2.4; E30 2.2; E23 2.0; E101 2.0; E111 2.0; E14 1.2; E73 1.2; E4 0.8; E20 0.6. E10 (cookie notice) is cut and not ranked. The order below rank 35 changes with the weights.

Findings from the ranking:

1. **The search results page is the least-covered zone.** Of the top 25, 15 are on the search and results page (E61, E46, E59, E62, E38, E44, E40, E41, E37, E66, E60, E43, E42, E58, E67), and the checkbox (E114) is mostly met there. Research exists for its layout (Baymard, #104 W7). No Manta rule adopts it, and the corpus layout goes against it (K19).
2. **Two elements meet every visitor and are thin.** The skip link (E11) is not built and no house file names it. The site footer (E6) is built, and its only element rules are in the corpus, which breaks B30 (K8).
3. **States that every list needs have no file at all.** Loading (E59), empty results (E58) and pagination (E60) are absent from the sheet, the corpus and the roadmap. impeccable `operate.md`, `clarify.md` and `harden.md` are the only cover.
4. **Elements on a photograph have no colour or surface rule.** E46 and E70 carry controls on a photo. The colour and surface areas are `—` for them.
5. **Inputs fail the 3:1 edge rule as specified.** Every corpus text field, select and checkbox has a 1.24:1 edge (K13). The live app has no inputs yet, so the fault is in the spec, not the build.
6. **Built elements with no element rule:** E21 (destination card grid) and E25 ('Good for' chips). These are on the live site today.

## 6. What the #117 surface-styling research changes

Source: `.claude/tmp/research-surface-styling.md` (design-vault#117), read in full at 194 lines on 13 Oct 2026. That file says "Status: in progress", so it can still grow. It had Part A (house holdings) and Part B sections B1 (borders), B2 (shadows and elevation), B3 (radius), B7 (focus). It had no sections on dividers, fills, scrims or stroke at the time of the read. The finished #117 (`docs/research/surface-styling.md`) adds B4 dividers, B5 fills, B6 scrims and text on photos, and B8 stroke; this section does not reflect them.

Effect on this matrix:

- When a Manta rule adopts a #117 principle, the matching `R` cells become `C`.
- #117 measured faults that add rows to §4: K13 (control edges 1.24:1, focus by border change only), K25 (scrim drift), K27 (hover with two signals), and the rest-shadow drift in K6.
- #117 gives principles that would resolve some conflicts in §4, if adopted:
  - K13: #117 B1.1 and B1.2 (two border roles: a 3:1 control edge and a low decorative edge); #117 B7.1 (a 2px outside ring on fields).
  - K5 (dark grounds) in part: #117 B2.4 (on a dark ground, show elevation by a lighter surface, not a shadow).
- Open at the 194-line read: controls and scrims on a photograph (E46, E70, K15), which the finished #117 addresses in B6; the map surface and pins (E61); a Manta rule for the bottom sheet's radius (E62), where #117 B3.1 gives only Material's extra-large top radius.

## Bound

- **Read in full:** Manta `DESIGN.md`, `PRODUCT.md`, `docs/brand/brand-sheet.md` v2.37; `docs/design-system/README.md`; every `docs/design-system/components/*.prompt.md`; ui_kits Homepage, DestinationHero, RewardsScreen, SiteFooter, SearchResults, BookingHandover, HostelDetail, Comparison (long lines cut at 200-260 characters); `tokens/spacing.css`; `Tag.jsx`; `app/page.tsx`; `app/best-hostels-in/[place]/page.tsx`; design-vault census #98 (`docs/research/design-rules-census.md`); impeccable 4.5.0 `reference/craft-floor.md`; design-vault `plugin/skills/design-critique/SKILL.md`; #117 artefact (194 lines, in progress); issues design-vault #118, #96, #117 and mantahostels #2988, #2989, #3057.
- **Read in part:** `docs/design-system/readme.md` (first about 287 lines); #104 (`docs/research/design-coverage-gaps.md`: W1-W14, frame, ranking; not L1-L2 in full); #115 (`.claude/tmp/research-manta-design-migration.md` §1.4-§3); `app/_components/Nav.tsx` lines 1-33; `app/globals.css` (greps, and lines 470-535, 540-640, 800-815); Manta design-review skill lines 28-66 and its prefill; the roadmap cards (`docs/reference-roadmap.html`, parsed; UI cards' action text only); Manta `competitor-teardown.md` §B-C; `seeded-review-conversion.md` header.
- **Searched, not read:** `gh issue list` on mantahostels for `kind:spec` (run twice, both empty); the open mantahostels issue list (37 issues, titles only); greps of ui_kits and templates for element terms; greps of impeccable `reference/` for element terms (operate, onboard, clarify, harden, adapt, critique, audit); greps of `globals.css` for skip, reduced-motion, shadow and radius; a grep of `docs/research` file names; a grep of the corpus for the 220 ms and 2.2 s durations.
- **Not read:** ui_kits `MobileSearch.jsx`, `MobileHostelDetail.jsx` (one grep line only), `mobile.html`; `docs/design-system/guidelines/*.html`; the rest of impeccable in full; design-vault `design-round` skill (seen only through census #98).
- **Limits of the result:**
  - Visitor frequency (Freq) is my estimate from page structure. No analytics were read.
  - The rank weights are my choice (§5 Method).
  - Absence claims ("no file", "no rule") rest on the greps named above and on the files read in full. An element rule in a file not read (the guidelines HTML, the mobile ui_kits) can change an `I` or `—` cell to `Rc`.
