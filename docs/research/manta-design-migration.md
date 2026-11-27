# Research: Manta design research that did not cross into design-vault (#115)

Ticket: lucmoseley/design-vault#115, child of map #96.
Question: Which design research from Manta's brand and design-system work did not go into design-vault? Does any of it fill a gap, or show a gap, that #104 does not cover?
Date of reads: 13 October 2026.

Key to the columns:

- **Strength**: P = primary standard (WCAG, CIE, a specification). S = strong secondary (a measured value in the repo, a named practitioner source). W = weak (no source given). F = founder decision.
- **Era**: T = timeless. E = era-bound (date given).
- **Sort**: a = portable principle or method. b = Manta-only decision. c = Manta decision that carries a portable method.

## 1. Inventory — where Manta's design research lives

The research is not in `docs/research/`. Of the 266 files there, no file has a brand colour, contrast, type-scale or spacing topic. The design research lives in four places:

1. `docs/brand/brand-sheet.md` (v2.37, 462 lines). This is the main store. It keeps the measured values (contrast ratios, CIELAB L\*, ΔE00) and the rejected options with their reasons.
2. `DESIGN.md` (241 lines). This is a derived restatement of the brand sheet for tools.
3. `docs/design-system/` (Claude Design export: tokens, `guidelines/*.html`, components).
4. GitHub issues on lucmoseley/mantahostels (see §1.5).

`docs/brand/design-process.md` and `.claude/skills/design-review/SKILL.md` already point to the design-vault plugin. Manta keeps only its values there.

### 1.1 How the research was made

- The brand sheet started on 15 Jul 2026 as v2.0 (commit `2516ff137`). It says "Compiled 14 July 2026 from the second-pass brand interview" and "Supersedes v1.0 entirely". The two interview passes and v1.0 are not in the repo. They were chat sessions. Thus the raw reasoning of the first brand work is lost to both repos. Only the outcomes and the "rejected with reasons" lines are in git.
- The sheet then grew to v2.37 over 48 commits. The measurements (L\*, ΔE00, contrast ratios) came in v2.4 to v2.7 (logo final, 23 Jul 2026, `57756cdbb`) and v2.17 to v2.36 (issues #3011, #3021, #3023, #3220, #3401, #3459).
- `git log -S` gave no hit for "contrast ratio", "APCA", "logo colour", "CIELAB" or "modular scale". "OKLCH" hit one commit only (`5e146b6eb`, a research note about tools). "Gestalt" hits trace to the design-review skill (#926). "type scale" and "spacing scale" hit only the Claude Design export (`ba817e38a`). Thus Manta never researched a type scale, a spacing scale, OKLCH or APCA. It chose values.

### 1.2 Colour (brand sheet §2, §3; DESIGN.md §Colors)

| # | Finding | Where | Strength | Era | Sort |
|---|---|---|---|---|---|
| C1 | Each colour has one job. Colour that carries no information does not appear in the working area. | sheet §3 | F | T | c |
| C2 | Warm = act, cool = read. | sheet §3 | F (no source) | T | c |
| C3 | **Text-safe partner rule.** A colour picked as a fill is not cleared for type until you measure it against each ground it sits on. Under 4.5:1 it gets a named darker partner, and the parent is marked fill-only. Fill choice optimises chroma; text choice optimises luminance contrast. "Assume the next colour added will need one too." | sheet §3 | P (WCAG 1.4.3) + method | T | c |
| C4 | Use the WCAG large-text limit on purpose: white on coral is 3.0:1, so the one CTA label is ≥19px at 700 (large text = ≥18.66px bold). "A type fix, not a colour fix": darkening coral to 4.5:1 (about `#C43F1B`) loses the brightness that makes it read as pressable. | sheet §4 | P (WCAG 1.4.3 large text) | T | c |
| C5 | **Night pattern.** On a dark ground, text is white. The semantic goes on a border, icon or chip fill. Do not invent light text partners: white already gives 13.12:1, and a light partner moves to L\* ~74 and collides with other tokens. A three-tier table per ground: clears AA text (≥4.5) / component only (3–4.5) / fails both. | sheet §3 | P (WCAG 1.4.3, 1.4.11) + measured | T | c |
| C6 | **Near-miss rule.** Two colour relationships must be decisively identical or decisively different. ΔE00 ~7 between two colours meant to match reads as a production error. Manta moved tokens to clear ΔE 10.3 → 20.4, and withdrew tokens at ΔE 12.4–13.5 from a neighbour. | sheet §3, §14 item 8 | P (CIEDE2000) + measured; thresholds are W | T | c |
| C7 | Separate two reds by hue as well as lightness (danger 346° against coral 9°). Under protanopia and deuteranopia both still collapse to one dark yellow-brown, so a label or icon must carry the meaning. | sheet §3, PRODUCT.md | P (WCAG 1.4.1) + S | T | c |
| C8 | Semantic states are tinted chips with a dark text partner (~12–16% tint), or a border or icon. Never coloured body copy. | sheet §3 | F + measured | T | c |
| C9 | **Hue geometry.** A CTA hue 176° from the main hue is a near-exact complement and gives edge shimmer on saturated grounds; coral at 166° (off-complement) does not. A hue nudge that leaves the warm analogous ramp (sand 44° → amber 40° → coral 9°) becomes an unrelated second accent. A warm cream ground shifts a hue's look (the nominal 10° nudge looks pinker). | sheet §3 rejections (22 Jul 2026) | W (practitioner colour theory; no source cited) | T | c |
| C10 | Chroma is affordance: a desaturated (blush) CTA stops reading as pressable. A colour carries genre (pink CTA reads cosmetics). A colour borrowed from a filtered photo is dishonest for an honest brand. | sheet §3 rejections | W | T | c |
| C11 | **Competitor colour firewall.** Keep the main competitor's brand-field colour out of all grounds. The role rule (CTA-only) does the firewall work, not the hue angle. | sheet §12 | F | E (Hostelworld identity, verified Jul 2026) | c |
| C12 | Palette values and jobs (ink, lagoon, turquoise, sand, coral, amber, peach, semantics, night tokens). | sheet §3 | F | — | b |
| C13 | A recorded falsifiable prediction for a colour fix ("danger-night should stop reading 'between error and decorative'; if not, reopen"). | sheet §14 item 8 | method | T | a |

### 1.3 Logo and mark (brand sheet §5, §6, §8; issues #3220, #3401, #3435)

| # | Finding | Where | Strength | Era | Sort |
|---|---|---|---|---|---|
| L1 | **Value structure, not hue, sets where a mark can sit.** Measure the mark's fill L\* range and area-weighted mean (Manta: 61.8–87.1, mean 66.6). A ground inside the mark's own value band is prohibited (turquoise L\* 70.1 → 1.20:1). Find the fill limits each ground demands (ink needs L\* ≥ 50.7, turquoise ≤ 38.3); when no single fill meets both, the answer is deployment rules, not a recolour. | sheet §2, §6 | P (CIELAB, WCAG relative luminance) + measured | T | c |
| L2 | **How the logo colours were derived from the palette.** Artwork may use off-palette colours. Exception: a near-miss (ΔE00 < ~10) of a token the mark sits beside is snapped to that token; a colour ΔE ≥ ~9 that never sits beside its near token is kept. A full recolour onto palette stops was measured and withdrawn (lightened 73.5% of the mark's area, sand contrast 2.45 → 2.17). | sheet §3 "Artwork leeway", §14 item 4 | measured + F | T | c |
| L3 | Keyline choice: one keyline colour on every ground, chosen by contrast to the light grounds (load-bearing at 5.47–5.90:1) and by separation from the fill. On a dark ground it becomes an "atmospheric" edge. | sheet §6 | measured + F | T | c |
| L4 | WCAG 1.4.11 exempts logotypes; 3:1 is only an engineering proxy for a mark. | sheet §6 | P (WCAG 1.4.11) | T | a |
| L5 | **Size variants.** Three only: primary; small-size variant with features redrawn (eye ~2.85×), not scaled, because at 48px the eye is 1.4px and the catchlight 0.5px; flat silhouette in `currentColor` for favicon, rating unit, mono print. A thin tail vanishes below ~32px. | sheet §6 | measured | T | c |
| L6 | **Logo audit and exploration brief.** Audit aspect ratio in square crops, small-size survival, symmetry, dark-ground fallback. Render each candidate at full size, 32px and 16px on every ground. Render variants that isolate one anatomical feature each, so the founder judges features on real art. | sheet v2.0 §6 (`2516ff137`) | method | T | a |
| L7 | The nav is a recognition surface, not a personality surface. Put personality where the mark is large (hero, empty states, 404, email, social). | sheet §6 | S (reasoned from L5) | T | c |
| L8 | Carry a mark across a forbidden ground on a bounded dark form (the ink hero wave). Acceptance test: zero mark pixels outside the ink fill at 320–1920px. | sheet §8, #3401, #3435 | measured | T | c |
| L9 | **Make a figure-ground hard rule a build error.** A `Ground` publishes its tone; `Mark` throws on turquoise in dev and test. Mutation-tested. | #3220 | method | T | c |
| L10 | Two-tone wordmark: a dark anchor plus a mid-tone. A mid-tone/mid-tone split blurs at 19px ("verified in context testing"). | sheet §5 | S (in-context test) | T | c |

### 1.4 Type, spacing, layout, zones, motion, accessibility, process

| # | Finding | Where | Strength | Era | Sort |
|---|---|---|---|---|---|
| T1 | Typeface choice by fit to the north star, with the runner-up and each reject's reason kept (Fraunces "reads boutique-editorial next to a turquoise hero"; Baloo 2 "trust tax on serious surfaces"; Nunito display "characterless"). | sheet §4 | F | T | c |
| T2 | Body 14–15.5px, line-height ~1.6. | sheet §4 | W (no source) | E (screen-era convention, 2010s+) | b |
| T3 | Type scale: hero `clamp(2.5rem, 5vw, 4rem)`, h1 2.25rem, h2 1.75, h3 1.25, card 1.0625, body 0.9375, label 0.8125, caption 0.75. **No ratio and no derivation is recorded.** | `docs/design-system/tokens/typography.css` | W (Claude Design export) | — | b |
| T4 | **Line length.** Target 60–75 real characters (45–75 norm). The CSS `ch` unit is the width of "0"; most prose letters are narrower, so `68ch` gave ~85 characters. `ch` grows with font size, so a larger lede set in `ch` is wider than the body. Fix: a fixed `rem` measure, checked in the real font. | #3429, #3224 | S (measured) + 45–75 norm (Bringhurst-era print convention) | T | c |
| T5 | Sentence case for body and buttons. Uppercase only for badges and filter labels. | sheet §4 | F | T | c |
| S1 | Spacing: 4px base scale 4–80 (`--space-1`…`--space-20`); "8px spacing grid". **No derivation is recorded.** | tokens/spacing.css, sheet §2 | W | E (4/8pt grid convention, 2016+ Material era) | b |
| S2 | Nav heights derived, not chosen: 72px = grid multiple that fits a 48px mark + 12px padding; 56px mobile = platform convention. "Bar height is a layout decision, not a legibility one." | sheet §2 | S | T | c |
| S3 | Borders first; shadow only on hover and popover; "white = elevated and tappable". | sheet §10 | F | E (flat-UI era, 2013+) | c |
| S4 | Radii 8/10–12/6/999. | sheet §10 | F | — | b |
| S5 | Compare at most 4 items: "working-memory limit". | `docs/design-system/readme.md` | S (Cowan 2001 ~4 chunks; source not cited) | T | c |
| S6 | **Scan columns.** The score sits at a fixed left position so it forms a vertical column row to row; the price forms the matching right-edge column; the score is met before the price. A comparison table aligns values at fixed shared row heights across cards. | sheet §7, readme | S (reasoned; Gestalt alignment/continuity) | T | c |
| Z1 | **Zone and volume system.** Every surface belongs to exactly one zone. A marketing zone runs at "volume" 6–7 (feeling); a working zone at 4–5 (speed). "Energy is localised, not uniform." | sheet §1, §2 | F | T | c |
| Z2 | A dark ground appears only in named, bounded contexts, never per page on whim. Same hues, same type; only the ground flips. | sheet §2 | F | T | c |
| Z3 | One focal (coral) action per view. | sheet §3 | S (common UX practice) | T | a |
| Z4 | "Loud claim, calm mechanics": a loud line is credible only with flat, specific terms right under it. | sheet §11, DESIGN.md | F | T | c |
| M1 | UI motion 120/180 ms, `cubic-bezier(0.2,0,0,1)`, press 0.97, no bounce; "motion never announces itself". | sheet §10 | F | T | b |
| A1 | A focus ring is never removed without a replacement. The ring colour must clear 3:1 on every ground it can sit on (lagoon is 1.59:1 on turquoise, so the ring is ink there). | sheet §10, #3459, #3404 | P (WCAG 2.4.7, 1.4.11) | T | c |
| A2 | Never colour alone for a state (C7). | sheet §3 | P (WCAG 1.4.1) | T | a |
| P1 | **Brand sheet form.** North star line; feeling hierarchy (first, tied second, beneath); a named enemy; "the most acceptable failure mode"; each section's status (LOCKED / CARRIED / PARKED with its dependency / IN EXPLORATION); a paste block for prompts. Made from a two-pass brand interview. | sheet v2.0 (`2516ff137`), sheet §1, §13 | method | T | c |
| P2 | Record each rejected option with its reason, "so they don't return". | sheet throughout | method | T | a |
| P3 | **Colour-count measurement.** Median-cut to 32 colours, merge near-duplicates, count colours at ≥2% coverage. Used to judge a "≤5 colours per scene" rule against references. | #3148 | method (S) | T | a |
| P4 | One source of truth (the sheet); derived files (DESIGN.md, the export) are cut to match on each bump, density as well as fact. | #3069, DESIGN.md header | method | T | a |
| P5 | **Manta's design-review gate (#926).** A baseline run showed `impeccable critique` never names a Gestalt principle, has no conversion/trust/SEO lens, no brand lens, and no "should anything change" standard. The skill added: six Gestalt lenses by name (proximity, similarity, closure, continuity, common region, figure/ground); the 5-second test; measure 45–75; "force Sam" (the accessibility persona) into every run; "no change for change's sake". | `git show 71b36d144` | S (observed baseline) | T | a |
| P6 | **Eye-training research (#3769, 13 Oct 2026).** Untrained people judge website appeal in 50 ms, stably (Lindgaard 2006). Prototypicality and visual complexity drive first impressions, and prototypes are category-specific (Tuch 2012). Preferences for colourfulness and complexity differ by audience (Reinecke & Gajos 2014). Novices pick the better of two designs almost as well as experts (76.5% against 81.2%), and "keep the best" comparison beats a tournament (83.6% against 74.1%) (Tanner & Landay 2019). A verdict read first anchors a judge (Kirk 2009; Hesslinger 2017). | #3769 comment | P (peer-reviewed studies; some read as abstract only) | T | a |
| V1 | Website-copy banned tells (14 families) and a three-question review pass ("so what", "prove it", "specificity"). | sheet §11 | S (from MIT `unslop`, `stop-slop`, `copy-editing` skills) | E (AI-writing tells, 2024–2026) | c |

### 1.5 Issues read on lucmoseley/mantahostels

Read in full or in part: #926 (via commit), #3023, #3069, #3148, #3220, #3429, #3768, #3769, #3772. Titles only (from search results): #2996, #3011, #3021, #3057, #3059, #3060, #3224, #3240, #3401, #3404, #3435, #3459, #3539. Search terms are in the Bound section.

## 2. Check against design-vault, impeccable and the planned research

Columns:

- **Vault**: is the item in `plugin/` (skills, references), House DNA, `docs/research/`, `GLOSSARY.md` or `docs/reference-to-design.md`? Y = present, P = partly present, N = absent. A mention inside the #98 census or #104 audit (both in `docs/research/`) is an index of Manta's rule, not a portable statement. I count it as N for "Vault" and record it under "Planned".
- **imp**: is the item covered by impeccable 4.5.0 (`colorize.md`, `typeset.md`, `layout.md`, `critique.md`)?
- **Planned**: the ticket or section on map #96 (or a sibling ticket) that already covers it.

Context for the read: the second project, mmm-infra, shows the transfer. Its rules file `~/mmm-infra/docs/brand/brand-sheet.md` §2 holds only hex values ("measured on the current site and logo"). It has no contrast pairs, no text-safe partners and no grounds rule for the logo. `design-project/SKILL.md:31` asks only for "the client's colours with hex values". In round one the founder said "Mark has chosen certain colours for his logos (blues and blacks/greys) that don't seem to mesh too well with the colour palette chosen here"; #102 records "No rule" for it (`docs/research/past-design-rejections.md:54`, unit B4).

### 2.1 Colour items (sort a or c)

| # | Item | Vault | imp | Planned | Result |
|---|---|---|---|---|---|
| C1 | One job per colour; no information-free colour in a working zone | N (DNA line 12 "several colours at equal weight, none dominant" is near, but not the same) | P: "Decoration without a relationship to hierarchy, state, content … is not a color strategy"; "do not spend [the primary action's] color on decoration" (`colorize.md`) | #98 B10 "portable in principle"; #103 decides where portable rules live | Covered by impeccable in substance. It stays with impeccable, not a gate question (#103). |
| C2 | Warm = act, cool = read | N | N | #98 B16 "maybe" | Gap, but unsourced (W). Not worth research alone. |
| C3 | Text-safe partner rule (measure each fill on each ground; named darker partner; parent marked fill-only) | N | P: "Verify computed foreground/background pairs" with the AA table. No token discipline (named partner, fill-only mark). | #98 B21 portable; #104 colour row "C for Manta; P for others" | **Absent from vault.** Its measured contrast is a vault gate question, WCAG 2.2 AA (#103). No ticket writes the method into the setup or identity round. |
| C4 | Large-text limit used on purpose for a CTA label | N | Y: large text 3:1 in the AA table | #104 W1 (APCA cross-check, "not a gap to fill now") | Covered by impeccable. |
| C5 | Night pattern (white text on a dark ground; semantic on border/icon; do not make light text partners) | N | P: "In dark mode, design surface elevation and contrast explicitly; do not invert"; light-on-dark type compensation (`typeset.md`) | #98 B6, B22 "partly"; #117 asks how each attribute "behaves in dark mode"; #104 W5 dark mode | Partly covered by impeccable; partly planned (#117 for fills, borders, focus). The "no light partner" collision reason is in no plan. |
| C6 | Near-miss rule (two colours decisively identical or decisively different; ΔE00 thresholds) | N | N | #98 B26 portable, "none" asks it | **Gap no ticket fills.** The thresholds (~7 bad, 10–20 safe) have no source. CIEDE2000 itself is a CIE standard. |
| C7 | Separate by hue and lightness; CVD; never colour alone | N | Y: "Simulate common vision deficiencies. Information conveyed by color also needs text, shape …" | #98 B19 | Covered by impeccable. |
| C8 | Semantic states as tinted chips with a text partner | N | P: semantic tokens | #117 "Fills, tints and surface tones (… selected and hover grounds)" | Planned (#117). |
| C9 | Hue geometry: complement shimmer, analogous ramp, ground shifts perceived hue | N | N (no "complement", "analogous", "vibrat" in colour sense; grep) | #98 B27 portable, "none" asks it. #104 colour row says theory is covered ("T (theory, contrast)", imp "Yes (colorize)"), but `colorize.md` holds contrast and OKLCH ramps, not harmony or chromatic interaction. | **Gap no ticket fills.** #104 counts it as covered; it is not. |
| C10 | Chroma is affordance; colour carries genre | N | N | none | Gap; weak source. Low. |
| C11 | Competitor colour firewall | N | N | #104 W13, gap rank 9 (distinctive-asset method: fame and uniqueness); #101 rules it | Accepted as a gap (#101). Manta's §12 is a worked example #104 already names. |
| C13 | Falsifiable prediction for a colour fix | N | N | none | Process habit. Low. Not a gap worth a ticket. |

### 2.2 Logo and mark items

`design-round/SKILL.md` §6 has no logo asset class. Its Identity round sets "palette, type and motion". The only logo lines in the vault are the craft gate's curve rules for a traced mark and #112's planned lockup file (ratio, clear space, minimum size). impeccable has no logo guidance (grep "logo|wordmark|favicon" hits only `document.md`, `init.md`, a browser script).

| # | Item | Vault | imp | Planned | Result |
|---|---|---|---|---|---|
| L1 | Value structure sets where a mark can sit (fill L\* band; prohibited grounds; deployment rules over recolour) | N | N | #98 B5 marks it "not portable" (it reads the Manta rule as written) | **Gap no ticket fills.** |
| L2 | Derive logo colours against the palette by adjacency (snap near-misses, keep decisive differences) | N | N | none. #112 item 2 only keeps a ruled palette; it does not say how a client's logo colours and a new palette are reconciled. | **Gap no ticket fills.** mmm-infra round one hit it (#102 unit B4). |
| L3 | Keyline choice by ground contrast and fill separation | N | N | #98 B32 "no" | Gap; lower frequency. Folds into L1. |
| L4 | WCAG 1.4.11 exempts logotypes | N | N | none | Gap (one fact). Folds into L1. |
| L5 | Size variants: redraw features for small sizes, flat `currentColor` silhouette, thin parts vanish below ~32px | N | N | #112 item 3: lockup "minimum size" | Partly planned (#112 gives a minimum size, not variants). |
| L6 | Logo audit; render each candidate at full, 32px and 16px on every ground; isolate one feature per variant | N | N | none | **Gap no ticket fills.** |
| L7 | Small chrome is a recognition surface; personality goes where the mark is large | N | N | none | Gap; folds into L5. |
| L8 | A bounded ground carries the mark across a forbidden ground; pixel acceptance test across widths | N | N | #78 width-sweep check (overflow, overlap) | Partly planned (#78 checks widths, not mark-on-ground pixels). |
| L9 | A figure-ground hard rule enforced as a build error | N | N | #100 (lint mechanism), #98 counts 50 mechanical rules | Stays Manta's own code: not a gate question (#103), and #100 adds no lint, since impeccable's detector already runs in the build. |
| L10 | Two-tone wordmark: dark anchor plus mid-tone | N | N | #98 B31 "no" | Gap; single in-context test, low strength. Low. |

### 2.3 Type, spacing, layout, zones, accessibility, process, perception

| # | Item | Vault | imp | Planned | Result |
|---|---|---|---|---|---|
| T1 | Typeface choice: fit, runner-up and rejects with reasons | P: Identity round tiles carry "a type pair" | P: typeset "Authority and fit" | none needed | Partly present. Not a gap. |
| T3, S1 | Type scale and spacing scale **method** | N | P: "a deliberate role scale"; "a documented spacing scale … a 4-unit base" (no ratio method) | #104 typography and layout rows | **Nothing to migrate.** Manta chose values and recorded no derivation (§1.1). |
| T4 | Line length 60–75; the `ch` unit overruns real characters and grows with font size | N | Y for 45–75ch; N for the `ch` pitfall | #86 (Measure lens, open) | Planned (#86). Add the `ch` pitfall to #86's check. |
| S3 | Borders first; shadow on hover and popover only | N | P | #117 (whole ticket) | Planned (#117). |
| S5 | Compare at most 4 (working memory) | N | Y: "≤4 items in working memory (… Cowan, 2001)" (`critique.md`) | — | Covered by impeccable. |
| S6 | Scan columns: a key value at a fixed position forms a column row to row | N | N (no "scan column"; layout has squint test, proximity) | #98 B39 portable; #104 W7 (search results, gap rank 1) | Planned in part (#104 W7 → #101), for Manta only. The portable form (alignment across repeated rows) is in no plan. |
| S2 | Size chrome from its content on the grid (72 = 48 mark + 2×12) | N | N | none | Low. Not a gap worth a ticket. |
| Z1 | Zone and volume: each surface has one register | N | Y in another form: impeccable's modes (Persuade, Operate, Read, Experience) set the register per surface | #104 W4 (Persuade against Operate) | Covered by impeccable. Manta's "volume" number is extra. |
| Z3 | One focal action per view | N (design-critique: "CTA count") | Y | — | Covered. |
| Z4 | Loud claim, calm mechanics | N | N | #98 B50 portable | A critique point, not a gate question (#103). No research gap. |
| A1 | Focus ring clears 3:1 on each ground it can sit on | N | Y: focus indicators 3:1 | #117 (focus rings); #104 W1 (2.4.11) | Covered by impeccable; planned (#117). |
| A2 | Never colour alone | N | Y | — | Covered by impeccable. |
| P1 | Brand-sheet form: north star, feeling hierarchy, named enemy, acceptable failure mode, section status (LOCKED / PARKED with its dependency …) | P: `design-project/SKILL.md:28-39` makes six sections (who, colour, type, logo, voice, standing rules) and marks "open" items | P: `init.md` writes PRODUCT.md (voice, personality) | #113 (client-fit gate at set-up) | Partly present. The feeling hierarchy and named enemy are absent; #113 is near but does not name them. |
| P2 | Record rejected options with reasons | P: the design record; #102 | — | #100 ("a corrections log", "a precedents file") | Adopted as a corrections log in the vault (#100). |
| P3 | Colour-count measurement (median-cut, merge, ≥2% coverage) | N | N | none | **Gap no ticket fills**, but small. It could make DNA line 12 ("several colours at equal weight") and any "≤N colours" rule mechanical. |
| P4 | One source of truth; derived files cut to match | Y: `references/impeccable.md` "The project's rules file wins" | — | — | Present. |
| P5 | Manta's design-review lenses (#926) | Y: design-critique §1 (accessibility persona forced), §2 (six Gestalt, conversion, SEO), §3 (no change for change's sake). **The "Measure 45–75" lens was dropped at the hand-over (#3536).** | — | #86 restores Measure; #104 W4 adds common fate, synchrony, connectedness | Present, except Measure (planned #86). |
| P6 | Perception research from #3769: Lindgaard 2006, Tuch 2012, Reinecke & Gajos 2014, Tanner & Landay 2019 (keep-the-best beats tournament), anchoring | P: Tuch in #104 W4; judge-first in #95 | — | #104 W4 (prototypicality, gap rank 3); #95 (judge first) | Mostly planned. **Two parts are in no plan:** Reinecke & Gajos (preference for colourfulness and complexity differs by audience, which bears on client fit) and Tanner & Landay's comparison mode (keep-the-best 83.6% against tournament 74.1%, which bears on how the founder narrows a round). |
| V1 | Website-copy banned tells (14 families) and the three-question copy pass | P: DNA line 7 names three words; #98 found that pointer false | P: `clarify.md` | #104 W11 (content: "no readability target") | Partly present. No ticket ports the list. Copy, so outside this ticket's visual scope; noted only. |

Two portable items not in the tables above: T5 (sentence case; Vault N; low) and Z2 (a dark ground only in named contexts; Vault N; it folds into C5).

## 3. Summary

### 3.1 Counts

48 items in the inventory (§1.2–§1.4):

- (a) portable principle or method: **10** (C13, L4, L6, Z3, A2, P2, P3, P4, P5, P6).
- (b) Manta-only value: **6** (C12, T2, T3, S1, S4, M1).
- (c) Manta decision that carries a portable method: **32**.

Of the 42 portable items (a + c), design-vault holds **2 in full** (P4, P5) and **5 in part** (T1, P1, P2, P6, V1). The other **35 are absent** from the vault. Of those 35, impeccable covers **9** in substance (C1, C4, C7, S5, Z1, Z3, A1, A2, and T4's 45–75 range). Map #96 or a sibling ticket plans **10 more** in whole or part (C3 and Z4 as rules via #98 → #103; C5, C8, S3 via #117; C11 via #104 W13; L5 via #112; L8 via #78; L9 via #100; S6 via #104 W7). That leaves **16** that nothing covers: C2, C6, C9, C10, C13, L1, L2, L3, L4, L6, L7, L10, S2, T5, Z2, P3 (ranked in §3.3), plus two parts of P6.

### 3.2 The answer

**Did it cross?** Partly. The **process** crossed: the design-review lenses (#926: Gestalt by name, conversion, SEO, the forced accessibility persona, no change for change's sake) are now design-critique §1–§3, and the design round is the vault's skill (#3536). The **colour and logo method** did not cross. It lives only inside Manta's brand sheet, written as Manta's values.

**What the founder recalls that is not in either repo.** Spacing and type scales were never researched: Manta took the 4/8px grid and the type ramp from the Claude Design export and recorded no derivation. The brand interview that made brand sheet v2.0 ("second-pass brand interview", 14 Jul 2026) and the v1.0 it replaced are not in git. If that reasoning matters, it is in claude.ai chat history, which this session did not search.

**Does it expose a gap #104 does not?** Yes, three:

1. **#104 counts Manta's sheet as house coverage.** Its colour row reads "C for Manta (measured pairs, text-safe partners); P for others (House DNA one line)", and its answer says timeless colour foundations are "mostly covered, through impeccable and Manta's sheet". But Manta's methods do not reach a second project (mmm-infra evidence above). For any project but Manta, the house's colour method is impeccable's `colorize.md` alone.
2. **#104's frame has no logo or mark row.** "Brand expression" in #104 is distinctiveness (fame and uniqueness) only. Manta's richest research (L1–L10: value structure, palette derivation, keyline, size variants, ground deployment) has no row in the frame, no plugin home, and no impeccable cover. #112 adds a lockup file (ratio, clear space, minimum size) for a logo the client already has. Nothing covers choosing grounds for a mark, reconciling its colours with a palette, or exploring a new mark.
3. **#104 marks colour theory as covered by impeccable, and it is not.** `colorize.md` holds the AA table, CVD simulation, OKLCH ramps and dark-mode composition. It holds no colour harmony or colour interaction (complement, analogous ramp, simultaneous contrast, vibrating edges) and no rule for two colours that are almost the same (C6, C9). #98 found both rules (B26, B27) and noted that no critic asks them.

### 3.3 Portable items no planned research covers, ranked by how often they affect a project the founder designs

| Rank | Item | Affects | Why this rank |
|---|---|---|---|
| 1 | **C9 Colour interaction and harmony** (complement shimmer, analogous ramp, a ground that shifts a hue's look) | Every website palette, brand art, logo colour; every identity round | Every project chooses a palette. Timeless (sources to read: Albers, *Interaction of Color*, 1963; Chevreul, 1839). |
| 2 | **C6 Near-miss rule with ΔE00 thresholds** | Every palette with more than a few colours; every logo placed beside a palette | Each new token or each client colour meets it. The rule exists in Manta with measured cases, but its thresholds have no source. CIEDE2000 is a CIE standard (CIE 142-2001). |
| 3 | **P6 parts: comparison mode and audience preference** (Tanner & Landay 2019: keep-the-best 83.6% against tournament 74.1%; Reinecke & Gajos 2014: preference for colourfulness and complexity differs by audience) | Every round the founder narrows (mode); every client project (audience) | Found by Manta's #3769 on 13 Oct 2026. #95 took "judge first" from it but not the comparison mode. #104 took Tuch 2012 but not the audience finding. |
| 4 | **L1 + L3 + L4 Mark-on-ground analysis** (fill L\* band; prohibited grounds; keyline; the 1.4.11 logotype exemption) | Every project with a logo (every client has one), on every page that shows it | Each new page ground is a new placement. |
| 5 | **L2 Reconcile a client's logo colours with a palette** | Every client project with an existing logo | mmm-infra hit it in round one (#102 B4). #112 keeps a ruled palette but does not say how the two meet. |
| 6 | **L6 (+ L7) Logo exploration and small-size protocol** (audit; full, 32px, 16px on every ground; one feature per variant; redraw, do not scale) | An identity round that makes or refreshes a mark: less often, high impact | |
| 7 | **P3 Colour-count measurement** | Brand art and any "≤N colours" or "one colour dominant" rule (DNA line 12) | Small; it turns a holistic DNA line into a mechanical check. |
| 8 | C2 warm = act; C10 chroma is affordance | Websites | Weak sources; research only if rank 1 runs and finds them. |
| 9 | L10 two-tone wordmark; S2 chrome sized from its content; C13 falsifiable prediction; T5 sentence case | Rare or low | Not worth a ticket alone. |

Ranks 1, 2, 4 and 5 are researched together in `docs/research/brand-palette.md` (#143, "How is a brand palette built and checked against its grounds and its logo?"). Ranks 3, 6, 7, 8 and 9 are accepted as gaps (#101).

## Bound

**Read in full:** Manta `DESIGN.md`; `docs/brand/brand-sheet.md` v2.37 (all 462 lines); `docs/brand/design-process.md`; `docs/rulings.md`; `PRODUCT.md`; `.claude/skills/design-review/SKILL.md` (current) and its first version (`git show 71b36d144`); brand sheet v2.0 (`git show 2516ff137`); `docs/design-system/tokens/spacing.css`, `tokens/typography.css`; design-vault `plugin/skills/design-critique/SKILL.md`, `design-round/references/impeccable.md`, `design-round/references/polish.md`; `GLOSSARY.md`; House DNA (`dna` in `data/gallery.json`); `docs/research/design-coverage-gaps.md` (#104); mmm-infra `docs/brand/brand-sheet.md` §1–§5.

**Read in part:** `docs/design-system/README.md` (first 60 lines), `readme.md` (grep for scale, spacing, contrast, ratio), `guidelines/type-scale.html`, `spacing-scale.html`, `colors-brand.html`, `brand-zones.html` (tags stripped, first 30 lines each); `docs/research/design-rules-census.md` (#98; lines 1–40, 195–314, 364–400); `design-round/SKILL.md` (lines 23, 60–83, 130–150 by grep); `design-project/SKILL.md` (lines 26–40); `docs/research/past-design-rejections.md` (lines 54, 61, by grep); impeccable 4.5.0 `colorize.md` (lines 1–86 by grep and lines 36–66 in full), `typeset.md` and `layout.md` (grep), `critique.md` (grep).

**Searched only:** Manta `docs/research/` (266 files: file names filtered by design terms; contents grepped for "contrast ratio|APCA|OKLCH|Gestalt|spacing scale|type scale|ΔE|CIELAB|L\*|modular scale|figure.ground|WCAG 1.4"; heads of 6 files). `docs/archive/` (file names only: 10 manual-sync reports and proposals, none on design). `docs/inspiration/catalogue.json` and `docs/notes/` (file names only; the notes are Running Lean and Mom Test, not design). `docs/adr/` (file names only; none on design). `docs/brand-assets/manta-inkscape-walkthrough.md` not opened (a drawing method for the mark, named in sheet §6). Git history: `git log --all --diff-filter=D` on brand, design, logo, palette, colour, contrast, typography, Gestalt and spacing paths; `git log --all -S` for "contrast ratio", "APCA", "OKLCH", "Gestalt", "spacing scale", "type scale", "logo colour", "CIELAB", "ΔE00", "modular scale". design-vault `plugin/`, `GLOSSARY.md`, `docs/reference-to-design.md`, `docs/research/` grepped for 21 term groups (listed by item in §2).

**Issues, lucmoseley/mantahostels** (`gh search issues`, each run once). Closed, limit 50: "brand colour" (0 results), "logo colour" (0), "palette", "contrast", "spacing", "typography", "Gestalt", "design system", "design tokens" (0), "type scale" (0), "font", "figure ground" (0), "ΔE" (0), "night ground", "wordmark", "illustration". Closed, limit 20: "lightness", "protanopia", "line length", "hierarchy", "colour blind" (0), "grid", "keyline", "mark legibility" (0), "favicon". Open, limit 30: "contrast", "palette", "Gestalt" (0), "typography", "spacing", "design system", "logo", "colour". The 0-result searches were not re-run; their absence claims are weaker. Read: #3023, #3069, #3148, #3220, #3429, #3768, #3769 (last comment, grep), #3772.

**Issues, lucmoseley/design-vault:** read #96, #101, #103, #112, #115, #117 (bodies); the issue list from #78 to #117 (titles).

**Not done:** claude.ai chat history (the brand interview that made sheet v2.0); `docs/design-system/` components and `ui_kits/`; Manta research notes on process and tools (`round-shape-literature.md`, `candidate-design-skills.md`, `visual-tweaking.md` and peers), which #104 already sampled; any web source (this was a repo-to-repo audit; the sources named in §3.3 rank 1 and 2 are pointers, not read).
