# Surface styling: borders, shadows, radius, dividers, fills, scrims, focus, stroke (design-vault#117)

Status: complete (13 Oct 2026).
Language: ASD-STE100 Simplified Technical English (approximate).
Parent map: design-vault#96. Question: design-vault#117.

## How to read this file

- Each principle has these fields: Rule, Conditions, Trade-off, Resolution, Source (strength), Era.
- Source strength: P = primary standard (WCAG, W3C). D = design-system documentation. E = expert reference (book, NN/g). R = peer-reviewed research. W = weak.
- "Unconditioned in the source" means that the source gives no conditions. Do not use that rule as a universal rule.

## Part A. What the house holds

### A1. Manta (lucmoseley/mantahostels)

Sources: `DESIGN.md` (read in full, 241 lines), `docs/brand/brand-sheet.md` (grep, then sections §2, §3, §6, §7, §10 read), `docs/design-system/tokens/*.css`, `docs/design-system/components/**/*.jsx` (grep), `docs/design-system/guidelines/spacing-elevation.html`, `app/globals.css` (grep and read of nav, card, button, notice).


- **Elevation rule.** "Borders first. `sand-border` at 1–1.5px does the work almost everywhere; box-shadow is reserved for hover and popover states. Nothing sits at rest under a heavy shadow. White = elevated and tappable." (DESIGN.md:183; brand sheet §10 line 216). No source and no conditions are given for this rule. Census B46 says "no" research.
- **Measured: the card edge is very weak.** `sand-border #EDE6D6` on white = **1.24:1**. On `sand-page #FBF6EA` = **1.15:1**. A white card on sand-page = **1.08:1**. So the "borders first" card edge is a hairline at about 1.1–1.25:1. The fill step (white on sand) is smaller than the border step.
- **Shadow tokens.** `--shadow-card: 0 1px 2px rgba(10,53,66,.06)`, `--shadow-card-hover: 0 4px 14px rgba(10,53,66,.10)`, `--shadow-popover: 0 8px 24px rgba(10,53,66,.16)` (tokens/spacing.css:24-26 and app/globals.css:90-92). The shadow colour is tinted with `ink`, not black. Three levels exist. The levels are not given names that say what each level means (rest / raised / overlay).
- **Drift 1, shadow at rest.** `app/globals.css:626` says "no shadow at rest" and `.dest-card` has no rest shadow. But `components/hostel/HostelCard.jsx:78` uses `--shadow-card` at rest. The rest token `--shadow-card` exists, but DESIGN.md says shadow is "reserved for hover and popover". The rule and the corpus do not agree.
- **Drift 2, scrim colour.** The live mobile-nav scrim is `rgb(0 0 0 / .4)` and the panel shadow is `rgb(0 0 0 / .2)` (globals.css:387, 409). The corpus Dialog scrim is `rgba(10,53,66,.45)` (ink-tinted) (Dialog.jsx:7). No rule names a scrim colour or opacity.
- **Hover treatment.** `.dest-card:hover` changes the border to `lagoon` and adds `--shadow-card-hover` (globals.css:627-629). So hover uses two signals together: border colour and shadow. impeccable's detector has a rule "hairline border plus wide diffuse shadow" (design-vault `docs/research/impeccable-checks.md:76`). The Manta hover state can trigger it. This is an interaction that no Manta rule names.
- **Radius.** chip 6, control 8, card 10–12 (token 12), pill 999 (DESIGN.md:189; tokens/spacing.css:17-21). A 5px radius on the checkbox (Checkbox.jsx:9) and HostelCard compare box is outside the scale. No rule for nesting (inner radius against outer radius and padding). No rule says what the rounding expresses. The brand-sheet "parked" vibe strip note says "square-topped strip execution was disliked (must be inset/rounded if revived)" (brand sheet line 448). That is the only note on shape as taste.
- **Input and control boundaries.** Input and Select border = `1.5px sand-border` (Input.jsx:11, Select.jsx:13). Checkbox unchecked border = `1.5px sand-border` (Checkbox.jsx:10; HostelCard.jsx:62). Measured **1.24:1 on white**. WCAG 2.2 SC 1.4.11 asks 3:1 for the visual information that is necessary to identify a component. An unchecked checkbox has no other visual identifier, so this is a probable 1.4.11 failure. (The rating-unit history in brand sheet line 183 found the same fault: a `sand-border` outline at 1.2:1 "makes empty units invisible"; that fix was not carried to checkboxes.) The live `app/` has no inputs yet. The search, filter and compare screens will add them.
- **Outline button.** Secondary button = `1.5px solid ink` (Button.jsx:40; globals.css:583). 13.12:1. Strong.
- **Focus.** `outline: 2px solid var(--focus-ring)` with offset 2–3px (globals.css, many). `lagoon` 3.65:1 on white, 3.38:1 on sand, 3.59:1 on ink. On turquoise the ring is `ink` (5.73:1) (brand sheet line 218; globals.css:179-185). Census B47 = covered. But the corpus Input sets `outline: none` and shows focus only as a 1.5px border colour change sand-border → lagoon (Input.jsx:11, 24). Lagoon against sand-border = 2.94:1, so the focused-versus-unfocused change is under 3:1. That fails the change-of-contrast part of SC 2.4.13 (AAA), and the 1.5px perimeter is under the 2px perimeter that 2.4.13 asks. It passes 2.4.7 (AA). No Manta rule covers 2.4.11 (focus not obscured by the sticky compare bar) — design-vault#104 already found this gap.
- **Error.** Error border = `danger` (7.26:1 on white). Never colour alone (brand sheet §3 line 63).
- **Dividers.** `sand-border` is "card borders, dividers" (DESIGN.md colour table). No rule says when to use a divider, a space, or a fill change.
- **Fills and tints.** White = elevated and tappable "always". Tinted card grounds only for "genuinely special rows (partner spotlight), never list items" (B17). Semantic tints ~12–16% with text partners; lagoon wash `#E6F6F8` for hover and selected only, never a card ground (B20). These are the most conditioned rules that Manta has. Lagoon wash on white = 1.11:1, so a selected state that uses only the wash is a weak signal (it needs a second cue).
- **Transparency, blur, glass.** No Manta rule. "Gradients in UI" are banned; "UI is flat" (DESIGN.md Don'ts). The `--badge-verified-border` is lagoon at 45% alpha (colors.css:63). No rule names photo scrims for text on hero photos or card photos. Carousel dots on photos use white at 55% with a 2px ink halo (HostelCard.jsx:24) — an undocumented photo-legibility treatment.
- **Icon stroke.** "~1.75px stroke at 20px, rounded caps and joins, Tabler/Lucide-style" (DESIGN.md:191; B44). Rating-unit empty outline ~1.5px. Borders 1–1.5px. Outline buttons 1.5px. Focus ring 2px. There is no rule that relates icon stroke to border weight, but the values are near each other (1–2px band). No rule for how the 1.75px icon stroke scales at 16px or 24px.
- **Left rule on the testimonial.** "a single `lagoon` left rule" on the testimonial pull-quote (DESIGN.md Components). impeccable craft-floor refuses "a colored border-left ... above 1px on cards, list items, callouts". The design-rules census (#98) records this as an unrecorded override of impeccable. The pull-quote is a quotation, not a card, so the override is in the scope where the convention (a quotation rule) is old print practice. The width is not stated.

### A2. design-vault

Sources: `plugin/skills/design-critique/SKILL.md` (grep), `plugin/skills/design-round/SKILL.md` and `references/*.md` (grep), House DNA (`dna` in `data/gallery.json`, read in full).

- design-critique: no rule on borders, shadows, radius, dividers, fills, scrims or focus. It sends accessibility to `impeccable audit`.
- design-round: `references/prompts.md:166-167` asks a tuning panel for "button corners and relevant hover, focus and pressed treatments". `references/polish.md:11` names "consistent button/focus/pressed states". Both are prompts, not rules.
- House DNA `never`: "glow or neon borders; glassmorphism cards" (line 1), "Glossy 3D SaaS blobs" (line 2), "One rounding applied to everything by habit, as the friendliness signal" (line 10). `constants` is empty. These lines are bans with no conditions. The DNA states "Defaults, not absolute rules: the project's own brief lines win", which is a general condition only.

### A3. impeccable (4.5.0 read; 4.2.1 has the same rule names per design-vault `docs/research/impeccable-checks.md:77`)

Sources: `skills/impeccable/reference/craft-floor.md` (read in full), `colorize.md` lines 25-66, grep over `layout.md`, `polish.md`, `audit.md`, `critique.md`, `distill.md`, `quieter.md`, `harden.md`, `bolder.md`.

- craft-floor Verify: "Depth: shadows carry an offset and a soft blur. A zero-offset colored halo is decoration." Browser surfaces: "focus rings ... Theme them from the palette."
- craft-floor Refuse (conditioned: "the brief's own words can earn any of them"): cards as lazy container, "nested cards are always wrong"; "Glass and blur as decoration rather than as a specific effect"; "A colored border-left or border-right above 1px on cards, list items, callouts, or alerts"; "Hard offset shadows (box-shadow: 4px 4px 0) outside a world that is actually neobrutalist"; "soft-shadowed rounded rectangles standing in for content"; icons "in one consistent stroke and weight".
- colorize: build roles including "canvas and elevated surfaces", "action, focus, and selection", "borders and separators"; contrast table "controls, icons, focus indicators 3:1"; "In dark mode, design surface elevation and contrast explicitly; do not invert"; "Prefer explicit colors over chains of translucent overlays when alpha would make contrast context-dependent."
- layout: "Use proximity before adding containers or decoration"; "are containers compensating for weak proximity?"
- polish: "Keep icon families, stroke/weight, sizing, and optical alignment coherent"; "Verify text, control, and focus contrast in every state."
- distill and quieter: remove borders, shadows, backgrounds that do not serve hierarchy; "Reduce thickness, decrease opacity, or remove entirely"; "Reduce border radius extremes".
- audit: missing focus indicators; "unbounded blur/filter/shadow effects" as a performance fault.
- Detector (from impeccable-checks.md:73-76): side-tab accent border; thick accent border on a rounded card; nested cards; glowing shadow accents; raster under a wash; low contrast incl. 3:1; radius outside DESIGN.md; hairline border plus wide diffuse shadow; cream/beige page background.
- What impeccable does not hold: elevation levels and what each means; radius scale or nesting; when a divider beats a space; border colour and weight selection; scrim opacity for text on photos; WCAG 2.4.11 and 2.4.13; dark-mode borders; stroke-to-border matching.

## Part B. Principles from sources

### B1. Borders and outlines

**B1.1 The 3:1 floor applies only to an edge that is necessary to identify a control or its state.**
- Rule: "Visual information required to identify user interface components and states, except for inactive components" must have 3:1 against adjacent colours (WCAG 2.2 SC 1.4.11, AA). "Having a visual boundary indicating the hit area is only required when there is no other visual way to identify the presence of the control." If a control has visible content "(such as text or a sufficiently contrasting icon)", a border "is not required". A text input that is shown by a border or a bottom border: "that indicator must meet 3:1". A text input with no border, shown only by a fill: the fill "must have a 3:1 contrast ratio to the adjacent background". A checkbox border of #9D9D9D at 2.7:1 on white is a named failure (Figure 42).
- Conditions: the element function. A button with a text label does not need a 3:1 edge. A text input, a checkbox, a radio, a toggle track and an empty rating unit do need one, because the edge is the only identifier. A decorative card edge does not need 3:1 unless the card edge is the only cue that it is a control. Disabled controls are exempt. Hover treatments are not "required to identify", but a hover must not lower the component's own contrast.
- Limits of the SC: it does not compare the focused and unfocused states (that is 2.4.13). It does not set a line thickness. It says "best practice would be for authors to avoid particularly thin lines", because anti-aliasing makes thin lines fainter than the token colour. Measure the colour that the browser renders.
- Trade-off: a 3:1 grey edge on every card makes a dense list heavy (see B1.3). So keep 3:1 for the edges that identify controls, and let decorative edges go low.
- Resolution: given a control whose only identifier is its edge, use an edge of 3:1 or more, or a fill of 3:1 or more, and not a low decorative border. Given a labelled button or a card with text content, a low-contrast edge is permitted.
- Source: W3C, Understanding SC 1.4.11 (WCAG 2.2), https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html (P). Era: timeless as a rule of perception; the 3:1 number is a 2018 standard (WCAG 2.1), carried into 2.2 (Oct 2023).

**B1.2 Expert systems use two border roles: a strong "outline" for control edges and a weak "outline variant" for decoration.**
- Rule: Material 3 has two roles. `Outline` (neutral-variant tone 50 in light, 60 in dark) is the edge of an outlined text field (1dp, 2dp on focus, `Primary` on focus, `Error` on error). `OutlineVariant` (tone 80 light, 30 dark) is the edge of an outlined card, an outlined button and a divider (1dp).
- Conditions: the role follows the element function, not the element look. The outlined button can use the weak edge because its text label identifies it (this agrees with B1.1). The text field uses the strong edge because its edge identifies it.
- Trade-off: one border token for all edges forces a choice: too strong for cards and dividers, or too weak for inputs.
- Resolution: given one border token for everything, split it into two roles: a control edge at 3:1 or more, and a decorative edge for cards and dividers.
- Source: androidx Compose Material 3 tokens `OutlinedTextFieldTokens.kt`, `OutlinedCardTokens.kt`, `OutlinedButtonTokens.kt`, `DividerTokens.kt` (androidx-main, read 13 Oct 2026); material-components-android `docs/theming/Color.md` lines 79-80 (D). Era: current (M3, 2021 onward).

**B1.3 Border, shadow and fill are three ways to separate a card. Material 3 says that for a card the choice is style.**
- Rule: Material 3 has three card types. "Elevated cards have a drop shadow, providing more separation from the background than filled cards". "Filled cards provide subtle separation from the background." "Outlined cards have a visual boundary around the container" and "can provide greater emphasis than the other types." "Each provides the same legibility and functionality, so the type you use depends on style alone." Defaults: outlined and filled 0dp elevation, outline 1dp; elevated 1dp elevation, 2dp hover/drag. Card corner = CornerMedium 12dp.
- Conditions: for a non-control container the choice is brand and density, not usability. (B1.1 still applies if the card edge is the only cue for a control.)
- Trade-off: an outline gives "greater emphasis", so many outlined cards in a list add many lines. A filled card gives the lowest emphasis. A shadow separates more than a fill, and is the only one of the three that also says "above".
- Resolution: choose one card type per surface family and keep it. Use the type to match the brand tone (outline = crisp, drawn; fill = quiet, soft; shadow = physical, raised). Do not mix types inside one list.
- Source: material-components-android `docs/components/Card.md` (D); androidx `ElevatedCardTokens.kt`, `OutlinedCardTokens.kt` (D). Era: current.

### B2. Shadows, elevation and layering

**B2.1 Depth carries a meaning: "above other content" or "you can act on this". Do not give depth to a static element.**
- Rule: Polaris: "Depth indicates interactivity. Interactive elements, like buttons or cards, get more depth"; "Don't give static elements unnecessary depth, as this can mislead merchants to think they're interactive"; "The depth of an element should always be related to its importance or interactivity"; "Keep most elements on the same layer to establish a visual baseline"; "Don't rely solely on depth to create focus. Not all merchants perceive depth in the same way". Atlassian: the "raised" level is "Reserved for movable cards, such as Jira and Trello cards"; "Raised elevations can create visual noise, so don't use to group content when a border or white space would suffice"; flat cards = default surface + border; "overlay" is for UI over other UI (modals, dialogs, dropdown menus, floating toolbars).
- Conditions: depth means "interactive" (Polaris) or "movable / floating" (Atlassian). The two systems agree that a static group takes a border or space, not a shadow. They differ on a clickable card at rest: Polaris gives it depth (and bevels its buttons); Atlassian gives it depth only if it is movable. The difference follows the brand: Polaris (2023, "v12") is a merchant admin that chose a tactile, "realism" look; Atlassian is a dense work tool where noise has a high cost.
- Trade-off: a shadow at rest on every clickable card makes the clickable cue strong, but adds noise in a long list, and the cue loses its value when everything has it.
- Resolution: given a dense list of equal, clickable rows (a search-results list), keep the rows on one layer (border or fill), and show the cue on hover and with in-card affordances (an outline button). Given one card that must look pressable among static content, a small rest shadow is valid. Given a floating element (menu, popover, dialog, sticky bar over content), a shadow is necessary: it is the only cue that says "above".
- Source: Polaris `content/design/depth/index.mdx` and `creating-depth.mdx` (github.com/Shopify/polaris main, read 13 Oct 2026) (D); Atlassian Design System, Foundations > Elevation, https://atlassian.design/foundations/elevation (D). Era: the "depth = interactive" idea is timeless (affordance). Polaris bevels are a 2023 return of light skeuomorphism (era-bound, current in that system only).

**B2.2 Use a small fixed set of elevation levels, each with a named role, and pair each surface colour with its shadow.**
- Rule: Atlassian has four levels: sunken, default, raised, overlay (plus an overflow shadow for scrolled content). "Always pair elevation.surface.raised with elevation.shadow.raised." "Don't mix different shadow and surface elevation tokens." Material 3 has six levels: 0, 1, 3, 6, 8, 12 dp (androidx `ElevationTokens.kt`). Material maps: outlined and filled card 0; elevated card 1 (hover 2); menu 2; dialog 3; drag 4. Polaris: "Don't use too many layers in one screen".
- Conditions: the number of levels follows the product's stacking needs. A marketing site needs about three (rest, raised or hover, overlay). An app with drag and nested overlays needs more.
- Trade-off: many levels give fine control; few levels keep the meaning clear.
- Resolution: name each level by its role (rest, hover, overlay), not by size. A shadow that has no role level is a defect.
- Source: Atlassian (D); androidx Compose Material 3 tokens (D); Polaris (D). Era: current.

**B2.3 On hover, change the surface colour OR change the elevation. Do not do both. Do not use elevation change on very small UI.**
- Rule: Atlassian: "Don't combine elevation transitions and hovered and pressed tokens for interactive states. Use one or the other." Elevation transitions are an alternative "only for default and raised elevations (not overlays)". "This approach should be used sparingly to avoid excessive animation." "It should not be used for very small UI, as elevation changes are harder to see than surface color changes at this size." Polaris: on press, an element goes down and gets darker; "Don't apply unexpected changes to an element's perceived depth" (for example, a button that rises on press).
- Conditions: element size (small controls take a colour change, not a shadow change); element level (an overlay does not rise further).
- Trade-off: two signals at once (shadow + colour or border colour) are stronger, but they double the motion and can read as noise.
- Resolution: given a large card, a hover can raise it (shadow) with no colour change, or tint it with no shadow. Given a chip, a checkbox or a small button, change colour, not shadow. A press goes down (smaller shadow, darker or scale down), never up.
- Source: Atlassian Elevation > Interaction states (D); Polaris creating-depth (D). Era: current. Note: this is one system's rule; Material 3 tokens raise an elevated card from level 1 to level 2 on hover (`ElevatedCardTokens.kt`), and its hover state layer adds an 8% colour layer (`StateTokens.HoverStateLayerOpacity = 0.08`), so Material does combine the two. Material also raises a filled card 0→1 and a filled button 0→1 on hover. The systems disagree. Atlassian is a dense tool and wants less motion; Material is a general system.

**B2.4 In dark mode, shadows are weak, so elevation moves to surface lightness.**
- Rule: Atlassian: "Shadows can be harder to see in dark mode, so dark mode elevations also rely on different surface colors"; "the higher the elevation, the lighter the surface looks". Apple HIG: in Dark Mode iOS uses "base and elevated" background sets; "The base colors are dimmer, making background interfaces appear to recede, and the elevated colors are brighter"; "these colors aren't necessarily inversions of their light counterparts". Material 3 replaced its primary-tinted elevation overlays with tonal "surface container" roles (lowest, low, default, high, highest), "instead of elevation overlays" (material-components-android `docs/theming/Color.md` lines 102-147).
- Conditions: ground lightness. On a dark ground (Manta's `ink` night contexts: nav, footer, announcement block) a shadow has almost no visible effect.
- Resolution: given a dark ground, show a raised or overlay surface by a lighter surface tone, and if needed a light, low-alpha border. Do not use a heavier shadow.
- Source: Atlassian (D); Apple HIG Dark Mode (developer.apple.com, change log 6 Aug 2024) (D); material-components-android Color.md (D). Era: current (dark mode as a system setting since 2018–2019).

**B2.5 A shadow has an offset and a soft blur; a zero-offset coloured glow is decoration. A hard offset shadow belongs only to a neobrutalist world.**
- Rule: impeccable craft-floor (Verify: Depth; Refuse: "Hard offset shadows (box-shadow: 4px 4px 0) outside a world that is actually neobrutalist").
- Conditions: stated by the source: the brief "can earn any of them".
- Source: impeccable 4.5.0 (W: expert opinion in a tool; not a design-system rule). Era: the glow ban targets the 2020s "AI look"; the hard offset shadow is a 2020s neobrutalist convention (era-bound).

### B1 (continued). Borders: when to remove one, and what replaces it

**B1.4 Too many borders make a design busy. A border can be replaced by a shadow, a fill change or more space.**
- Rule: Refactoring UI: "Use fewer borders." Too many "can make your design feel busy and cluttered". "Instead, try adding a box shadow, using contrasting background colors, or simply adding more space between elements."
- Conditions: unconditioned in the source (the public text gives no conditions). Atlassian gives a condition from the other direction: use a border or white space, not a raised shadow, for grouping (B2.1). So the two sources agree that a border can go, but disagree on its first replacement: Refactoring UI lists a shadow first; Atlassian says a shadow is "noise" for grouping and keeps the border.
- Resolution (from B2.1 and B1.5): to group static content, first use space; then a fill change; then a border. Use a shadow only when the element floats or is interactive and the brand wants depth.
- Source: refactoringui.com (book by Adam Wathan and Steve Schoger, 2018) (E). Era: written in the post-flat period (2018); still current.

**B1.5 Perception: an enclosing edge (common region) and space (proximity) are both grouping cues. They add when they agree and cancel when they disagree.**
- Rule: Palmer (1992) found "common region": elements inside one bounded area group together (Cognitive Psychology 24, 436-447). Montoro and Luna (2015) tested common region (an extrinsic cue, for example a border) against proximity (an intrinsic cue, space): when the two are of similar strength, "the effect of conjoined cooperating principles was greater than that of either principle acting alone" and "the effect of conjoined competing principles was smaller than that of either principle operating alone"; when one is much stronger, the stronger one decides.
- Conditions: this is about grouping only. It is the base for the "border vs space" choice.
- Trade-off and resolution for UI: a border that agrees with the spacing is redundant (it adds a little grouping and adds a line). A border that disagrees with the spacing (for example a card border around items that the spacing groups in another way) makes the grouping ambiguous. So: given spacing that already makes the groups clear, a border adds only a surface or tap cue, and it can go if it has no other job. Given spacing that cannot be large (dense list, phone width), use a border or a fill so that the region does the grouping.
- Source: Palmer 1992 (R); Montoro and Luna, The Spanish Journal of Psychology 18 e33, 2015 (R, abstract read). Era: timeless (perception).

### B3. Corner radius and shape

**B3.1 Use a small radius scale and map it to element size and role.**
- Rule: Material 3 shape scale: none 0, extra-small 4, small 8, medium 12, large 16, large-increased 20, extra-large 28, extra-large-increased 32, extra-extra-large 48, full (material-components-android `docs/theming/Shape.md`; androidx `ShapeTokens.kt`). Component mapping in androidx tokens: outlined text field and menu = extra-small (4); filter chip = small (8); card (elevated and outlined) = medium (12); dialog = extra-large (28); bottom sheet = extra-large top; button = full (capsule). "Material Design encourages brand expression through shapes."
- Conditions: element size and role. The pattern is: small controls have small radii, big containers have big radii, and buttons are capsules (in M3). Brand: the scale itself is a brand choice.
- Trade-off: one radius for everything is simple but loses the size relation; House DNA bans "One rounding applied to everything by habit, as the friendliness signal".
- Resolution: a radius scale with three to five steps, each step tied to an element class. Larger elements take larger radii, so that the curve looks the same at each size.
- Source: androidx Compose Material 3 tokens (D); Material Shape.md (D). Era: the scale is current (M3 2021; increased steps added with M3 Expressive, 2025).

**B3.2 A nested shape is concentric: inner radius = outer radius minus the padding between them.**
- Rule: Apple WWDC25 session 356 "Get to know the new design system": "concentric shapes calculate their radius by subtracting padding from the parent's"; "keep an eye out for corners that feel too pinched— or flared. They can create tension and break the sense of balance"; "One place this often shows up in is nested containers—like artwork in a card." SwiftUI `ConcentricRectangle` (iOS 26) computes it.
- Conditions: applies when an inner shape sits inside an outer shape with even padding. If the padding is larger than the outer radius, the inner radius goes to 0 or to a fallback ("use a concentric shape with a fallback radius ... the fallback kicks in when the component stands alone").
- Trade-off: a fixed token radius on both parent and child gives an inner corner that looks too round (flared) when the padding is small.
- Resolution: given a photo flush in a card (zero padding), the photo takes the card's radius on the shared corners (or the card clips it). Given an inner element with padding p inside radius R, use max(R − p, small fallback).
- Source: Apple developer video, WWDC25 session 356 transcript (D). Era: the geometry is timeless; Apple made it a named system rule in June 2025.

**B3.3 Capsule versus rounded rectangle depends on density and pointer.**
- Rule: Apple WWDC25-356: "Capsules bring focus and clarity to touch-friendly layouts, but in dense desktop environments, they're best used for standout actions." On macOS, Mini, Small and Medium controls keep rounded rectangles for "compact, high-density layouts"; Large and X-Large use capsules. "For phone layouts, use a capsule with extra margin ... For iPad and Mac, use a concentric shape that aligns with the window edge."
- Conditions: density (dense → rounded rectangle), device and pointer (touch → capsule), emphasis (a standout action may be a capsule in a dense view).
- Resolution: given a dense desktop list, use rounded rectangles for row controls and save capsules for tags, status chips and one standout action.
- Source: Apple WWDC25-356 (D). Era: current (2025).

**B3.4 Rounded shapes read as softer and are liked more; sharp angles read as harder.**
- Rule: Bar and Neta (2006), Psychological Science: participants liked curved everyday objects more than sharp-angled versions; the authors propose that sharp contours signal threat. A 2007 fMRI follow-up found more amygdala activity for sharp objects. The threat account is disputed in later reviews; the preference for curvature itself is well replicated.
- Conditions: the studies use objects and abstract shapes, not UI corners. The transfer to a 4px versus 12px corner is an inference, not a finding.
- Trade-off: more rounding reads friendlier and softer, and less precise. Less rounding reads crisper, more serious, more "tool".
- Resolution: choose the radius scale from the brand tone. A playful, warm brand can take larger radii; a dense data tool can take smaller ones. Inside one product keep the scale fixed.
- Source: Bar and Neta 2006 (R, abstract); "The Curvature Effect" review (W, authors not verified). Era: timeless (perception), but the UI transfer is weak.

**B3.5 One radius "factor" for the brand, applied by component; some shapes carry meaning and must not change.**
- Rule: Radix Themes sets radius as one theme value (none, small, medium, large, full) that "manages the radius factor applied to the components"; "The resulting border-radius is contextual and differs depending on the component." With `full`, buttons become pills, but checkboxes do not become round, so that they are not confused with radio buttons.
- Conditions: a shape can carry meaning: a square box = checkbox (many choices), a circle = radio (one choice), a capsule = a tag or a status chip in many systems. A brand radius must not erase those meanings.
- Contrast with GOV.UK: inputs have `border-radius: 0` and a 2px black border (govuk-frontend `components/input/_mixin.scss` lines 17-19). GOV.UK is a plain, high-trust public service with a utilitarian brand; it uses no rounding at all. Material and Apple use large radii and capsules. This disagreement follows the brand tone, not usability.
- Source: Radix Themes docs, Theme > Radius (D); govuk-frontend source, main branch, 13 Oct 2026 (D). Era: current.

### B7. Focus rings and state outlines

**B7.1 Minimum (AA): focus is visible (2.4.7); an author focus indicator has 3:1 against its adjacent colours (1.4.11); a focused element is not fully hidden by author content (2.4.11). Enhanced (AAA): an area at least a 2px perimeter, with 3:1 change between focused and unfocused pixels (2.4.13).**
- Rule: see B1.1 for 1.4.11. SC 2.4.13 Focus Appearance (AAA): "an area of the focus indicator ... is at least as large as the area of a 2 CSS pixel thick perimeter of the unfocused component" and "has a contrast ratio of at least 3:1 between the same pixels in the focused and unfocused states." An inset indicator "would need to be at least 3px thick to pass." "If you need to use complex mathematics to work out if a focus indicator is large enough, it is probably a sign that you should use a larger indicator instead." SC 2.4.11 Focus Not Obscured (Minimum, AA, new in WCAG 2.2): a focused component is not entirely hidden by author-created content (sticky headers, footers, cookie bars).
- Conditions: ground. A single-colour ring that passes on white can fail on a coloured ground. Shape: an inset ring (inside a border) must be thicker than an outside ring. Sticky UI: 2.4.11 applies whenever there is a sticky bar.
- Trade-off: a strong ring (thick, two colours) is very visible but it is a large visual change that some brands dislike. A border-colour-only focus (1–1.5px colour swap) is quiet, but it usually fails 2.4.13 and is hard to see for low-vision users.
- Resolution: given a brand that uses more than one ground, use either a two-colour ring (W3C technique C40) or one ring colour per ground (Manta's rule: `ink` on turquoise). Given a text input, do not rely on a border-colour swap alone; add an outside 2px ring or make the border at least 2px and 3:1 different from the rest state. Given a sticky bar, add scroll padding so the focused element is not hidden.
- Source: W3C Understanding SC 2.4.13 https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html (P); WCAG 2.2 SC 2.4.11 (P; design-vault#104 research also covers it). Era: timeless need; numbers from WCAG 2.2 (Oct 2023).

**B7.2 Two-colour focus works on every ground. GOV.UK: yellow fill or outline plus a thick black edge.**
- Rule: GOV.UK: "Focus states in the GOV.UK Design System use a combination of yellow and black, along with a thick bottom border." Links: "a yellow background with a black bottom border." Inputs: "a yellow outline and a thick black border"; if the element has a border, "the border gets thicker". Reason: "The yellow has a high contrast with dark backgrounds," and "the thick black border has a high contrast against light backgrounds." Source code: `$govuk-focus-width: 3px`; input focus = `outline: 3px solid yellow; outline-offset: 0; box-shadow: inset 0 0 0 2px <input-border>` (helpers `_focused.scss`). The code also sets `outline: 3px solid transparent` where the visible ring is a box-shadow, so that the ring still shows in forced-colours (Windows high contrast) mode.
- Conditions: GOV.UK's brand puts accessibility first and accepts a loud focus state. A brand with a quieter tone can use a two-colour ring that is thinner, or one ring colour per ground.
- Source: GOV.UK Design System, Get started > Focus states (D); govuk-frontend source (D). Era: current (pattern since about 2018; restated for WCAG 2.2).

**B7.3 Use a ring for a field; use a highlight (fill) for a row in a list.**
- Rule: Apple HIG Focus and selection: "In general, use a focus ring for a text or search field, but use a highlight in a list or collection." "it's usually easier for people to view lists and collections when an entire row is highlighted." The ring follows the item's shape and corners ("refine it to match contours like rounded corners").
- Conditions: element function (field versus row), density (lists).
- Resolution: given a list of selectable rows, show the selected or focused row with a fill (a tint) plus a second cue (B5.2), not a ring on each row. Given a field, a ring.
- Source: Apple HIG, Focus and selection (developer.apple.com JSON, read 13 Oct 2026) (D). Era: current.

**B7.4 State outlines (error, selected) must not depend on colour alone.**
- Rule: Material 3 text field: error outline uses the `Error` role, focus outline is 2dp `Primary`, rest outline 1dp `Outline`, hover outline 1dp `OnSurface` (androidx `OutlinedTextFieldTokens.kt`). WCAG 1.4.1 (Use of Color) asks that colour is not the only visual means. Manta already asks a text label or icon with every error.
- Resolution: an error state = colour change + thickness or icon + text message. A selected state = colour + a check mark, a weight change or a fill.
- Source: androidx tokens (D); WCAG 2.2 SC 1.4.1 (P). Era: timeless.

### B4. Dividers and separators

**B4.1 A divider is a thin line that groups. Full-width dividers separate unrelated sections; inset dividers separate related items. The divider colour is the weak border role.**
- Rule: Material: "Dividers are thin lines that group content in lists or other containers." "Full width dividers separate larger sections of unrelated content. They also separate interactive areas from non-interactive areas." "Inset dividers separate related content within a section." Defaults: 1dp, `colorOutlineVariant` (a heavy divider is 8dp). GOV.UK: the functional colour `border` ("Used in for example borders, separators, rules and keylines") is `black tint-80`, while `input-border` is `black` (govuk-frontend `settings/_colours-functional.scss`). Apple HIG Layout: "Group related items ... you might use negative space, container shapes, or separator lines". Apple gives one separator vibrancy level that "works well on all materials".
- Conditions: the divider is a grouping cue, so B1.5 applies: when space already separates the groups, a divider is redundant. A divider does not identify a control, so it does not need 3:1 (B1.1).
- Trade-off: space against lines. Space needs room; on a phone or in a dense list there may be no room, so a line does the work at a cost of one pixel. A line in every gap of a list that already has generous padding is "busy" (B1.4).
- Resolution: given generous padding, separate with space and drop the divider. Given a dense list or a narrow screen, use an inset or full-width divider in the weak border colour. Given cards with their own edges, do not also put dividers between the cards. Inside a card, separate a footer or a secondary area with a fill change (Polaris: "Use a gray background to de-emphasize contained information") or a single divider, not both.
- Source: material-components-android `docs/components/Divider.md` (D); govuk-frontend (D); Apple HIG Layout and Materials (D); Polaris creating-depth (D). Era: timeless (print rules are centuries old); the values are current.

**B4.2 Zebra striping (alternating row fills) is optional; evidence for it is weak.**
- Rule: alternating fills are said to help the eye follow a row across a wide table. Jessica Enders' first online study (A List Apart, 2008) found no significant accuracy difference and one significant speed difference; her follow-up ("Zebra Striping: More Data for the Case", A List Apart; 2,276 sessions per a secondary summary) reported better accuracy on numerical look-up. Not peer-reviewed; I read only summaries, not the articles. I found no design-system rule that requires striping.
- Conditions: wide tabular data with many columns. Not for a card list (each card is already its own region).
- Source: A List Apart articles by Jessica Enders (W; summaries only). Era: era-neutral.

### B5. Fills, tints and surface tones

**B5.1 Separate by surface tone: a set of named surface levels, each one step apart.**
- Rule: Carbon: "There are four layers within a theme: base layer, layer 01, layer 02, and layer 03." In the White theme `background` = #ffffff, `layer-01` = #f4f4f4 ("Container color on $background"), `layer-02` = #ffffff ("Container color on $layer-01"), so layers alternate. "Border tokens however, pair with its same number" (`border-subtle-01` #c6c6c6 on layer-01). Material 3: five surface container tones (lowest, low, default, high, highest), used "instead of elevation overlays". Atlassian: "sunken" surface for a backdrop where grouped content sits (Kanban columns); "Only use sunken surfaces on the default surface level."
- Conditions: a tone step is a grouping and a hierarchy cue. A darker well recedes; a lighter (or white) card on a tinted page comes forward (Polaris: "Decrease the brightness of an element when it's being pushed down ... Increase the brightness ... when it's being pushed up").
- Trade-off: a fill step makes no line, so it is quieter than a border. But a very small step (near 1.05–1.1:1) can disappear on a poor screen, in bright light, or for low-vision users. Where the edge carries no meaning, that is acceptable.
- Resolution: given a tinted page ground and white cards, the fill step does the main work, and a border is a secondary edge. Given a fill step under about 1.1:1, keep a border (or a shadow) so that the edge survives poor screens.
- Source: Carbon Color > Usage and Tokens (D); androidx and Material Color.md (D); Atlassian Elevation (D); Polaris (D). Era: current; the alternating-layer model is 2020s.

**B5.2 A tinted fill for hover and selected states is a state indicator. If it is the only cue for "selected", it must meet 3:1.**
- Rule: WCAG 1.4.11 covers "any visual information necessary to indicate state, such as whether a component is selected". Hover is exempt ("additional author-supplied visual treatments for hover are not 'required to identify' the hover state"). Material uses an 8% state layer for hover, 10% for focus and press, 16% for drag (androidx `StateTokens.kt`). Atlassian uses hovered and pressed surface tokens.
- Conditions: hover (exempt) versus selected (not exempt). A pale wash is acceptable for hover. For selected, a pale wash needs a second cue (a check mark, a 3:1 border, a weight change, a strong left indicator).
- Resolution: given a selected row or chip, pair the tint with a non-tint cue of 3:1 or more.
- Source: W3C Understanding 1.4.11 (P); androidx tokens (D); Atlassian (D). Era: timeless rule; the state-layer numbers are current Material.

**B5.3 Do not use bright or contrasting fills or borders for containers; tint neutrals only for a reason.**
- Rule: Polaris: "Don't use bright or contrasting colors for container backgrounds or borders. This distracts merchants from the main content and creates a cluttered UI." "Don't use unique styles for surfaces, like inset shadows." impeccable colorize: "Tint neutrals only when the brand hue genuinely creates cohesion"; "Prefer explicit colors over chains of translucent overlays when alpha would make contrast context-dependent."
- Conditions: working areas (Polaris is an admin). A marketing hero can use a coloured ground on purpose.
- Source: Polaris (D); impeccable (W). Era: current.

### B6. Transparency, scrims and blur

**B6.1 A scrim dims what is behind a modal surface. Expert systems use 32% to 60% black.**
- Rule: Material 3 scrim: `Scrim` colour at `ContainerOpacity = 0.32` (androidx `ScrimTokens.kt`). Carbon `overlay`: "Background overlay" = rgba(0, 0, 0, 0.6). Apple: for clear Liquid Glass over bright content, "consider adding a dark dimming layer of 35% opacity"; no dimming layer if content is "sufficiently dark".
- Conditions: how bright and busy the content behind is; the surface's own contrast. A modal with a strong edge or shadow needs less scrim. A photo hero behind needs more.
- Trade-off: a dark scrim focuses attention and hides the context; a light scrim keeps context.
- Resolution: one scrim token for the product (colour and opacity), not one per component. Tint it with the brand dark (as Manta's corpus Dialog does with `ink`) or use neutral black, but use one.
- Source: androidx Compose Material 3 tokens (D); Carbon tokens (D); Apple HIG Materials (D). Era: current.

**B6.2 Text on a photo must meet the text contrast ratio against the real pixels behind it. A scrim, a gradient or a solid panel makes that true.**
- Rule: WCAG 1.4.3: "contrast is measured with respect to the specified background over which the text is rendered in normal usage." Failure F83: "using background images that do not provide sufficient contrast". A wide halo around letters "acts as a halo" and counts as the background. Apple: the regular glass variant "blurs and adjusts the luminosity of background content to maintain legibility"; use it "when components have a significant amount of text".
- Conditions: the photo changes (user or hostel photos), so the worst-case pixel decides. A scrim tuned for one photo fails on another.
- Resolution: given text over arbitrary photos, use a solid or near-solid panel, or a gradient scrim strong enough for a white photo, or move the text off the photo. Given a controlled photo (art-directed hero), measure at the worst point under the text.
- Source: W3C Understanding 1.4.3 (P); Apple HIG Materials (D). Era: timeless.

**B6.3 Glass and blur: use for a functional layer that floats above content, not for content cards. Use more blur, a simple background, and a solid fallback.**
- Rule: NN/g (Megan Brown, 7 June 2024): glassmorphism "utilizes different levels of translucency to create depth and contrast"; "One of the most significant issues with glassmorphism stems from text readability problems"; "More background blur is better, especially with intricate backgrounds"; "opt for simple or single-color backgrounds"; "best when utilized sparingly". Apple (Liquid Glass, introduced June 2025): it "forms a distinct functional layer for controls and navigation elements"; "Don't use Liquid Glass in the content layer"; "Use Liquid Glass effects sparingly"; "Only use clear Liquid Glass for components that appear over visually rich backgrounds". Apple also notes system settings "reduce transparency or increase contrast". impeccable: "Glass and blur as decoration rather than as a specific effect" is refused; audit flags "unbounded blur/filter/shadow effects" for performance. House DNA bans "glassmorphism cards".
- Conditions: layer (functional overlay versus content), background complexity, user settings (`prefers-reduced-transparency`, `prefers-contrast`), performance on low-end phones.
- Trade-off: glass keeps context and looks current; it risks text contrast and costs GPU.
- Resolution: given a sticky bar or a nav over scrolling content, translucency with strong blur is acceptable if text still meets contrast against the worst case and a solid fallback exists. Given a card in a list, no glass.
- Source: NN/g (E); Apple HIG Materials (D); impeccable (W). Era: glassmorphism as a web trend is 2020–2022 (era-bound, now a known "AI look"); Apple Liquid Glass is a 2025 platform material (current, Apple platforms; not a web convention).

### B8. Icon and illustration stroke weight against border weight

**B8.1 All interface icons use one stroke weight, and that weight matches the weight of the adjacent text.**
- Rule: Apple HIG Icons: "all interface icons in your app need to use a consistent size, level of detail, stroke thickness (or weight), and perspective"; "use the same stroke weight in every icon"; "In general, match the weights of interface icons and adjacent text. Unless you want to emphasize either the icons or the text". SF Symbols: "Each of the nine symbol weights ... corresponds to a weight of the San Francisco system font". Outline variant "works well in toolbars, lists, and other places where you display a symbol alongside text"; the fill variant can "indicate selection". Material Symbols: weight axis 100–700; "To reduce glare for a light symbol on a dark background, use a low grade"; "You can match grade levels between text and symbols"; optical size "automatically adjust[s] the stroke weight when you increase or decrease the symbol size". impeccable polish: "Keep icon families, stroke/weight, sizing, and optical alignment coherent."
- Conditions: adjacent text weight; ground (light on dark looks heavier, so use a lower grade on dark); icon size (stroke must change with optical size, not scale linearly).
- Source: Apple HIG Icons and SF Symbols (D); Google Fonts Material Symbols guide (D); impeccable (W). Era: timeless (type and icon weight harmony).

**B8.2 An SVG stroke scales with the icon unless it is set to non-scaling. Lucide default: 2px at 24px.**
- Rule: Lucide: "default stroke width of 2px"; "When adjusting the size prop the size of the stroke width will be relative to the size of the icon"; `nonScalingStroke` keeps it constant (lucide docs `guide/react/basics/stroke-width.md`).
- Measured consequence: Lucide at 20px = 1.67px stroke; at 16px = 1.33px; at 24px = 2px.
- Interaction with borders: a 1.33px icon next to a 1.5px border looks lighter than its frame; a 2px icon inside a 1px-bordered chip looks heavy. Sources do not give a rule that ties icon stroke to border width; this is an inference from the "match weights" rule above.
- Resolution (inference): pick one "line weight" band for the product (for example 1.5–2px), and keep borders, icon strokes, outline-button edges and rating outlines inside it, with the focus ring the one deliberate step above it.
- Source: Lucide docs (D for the library). Era: current.

### A1 (added). More Manta drift

- **Drift 3, button radius.** DESIGN.md front matter gives `button-primary` and `button-outline` `rounded: control` (8px). The live `.btn` (globals.css:553) uses `--radius-pill` (999px), so the live hero CTA is a capsule. The corpus compare-bar CTA is also a pill (SearchResults.jsx:179), and the corpus `Button.jsx` uses `--radius-control`. So the primary CTA has two shapes in the house and the rule names only one.
- **Sticky bars carry shadows that no rule names.** The sticky compare bar uses `--shadow-popover` (SearchResults.jsx:177) and the mobile detail sticky bar uses `0 -4px 14px rgba(10,53,66,.07)` (MobileHostelDetail.jsx:123). This agrees with B2.1 (a floating element needs a shadow), but DESIGN.md says shadow is for "hover and popover states" only and does not name sticky bars. The mobile bar's shadow is a fourth, untokenised value.
- **Filter pills.** The search filter pill uses `1.5px sand-border` and `--radius-pill` (SearchResults.jsx:163). It has a text label, so its edge does not need 3:1 (B1.1); its selected state does (B5.2). No rule says how a selected filter looks.

### B9. Dated conventions (era labels)

- **Heavy skeuomorphic shadow and bevel** (to about 2012; iOS 6 and earlier): real-material textures, deep drop shadows, glossy bevels. Era-bound. Polaris v12 (2023) brought back light bevels and inset shadows on buttons for "tactility" (B2.1); that is a current, system-specific choice, not a return of the full style.
- **Ultra-flat** (about 2013–2016; iOS 7, Windows Metro): no shadow, no border, text-only buttons. NN/g (Kate Moran, 3 Sep 2017; eyetracking, 71 users, 9 pages): weak signifiers cost "22% more time" and "25% more fixations"; flat works best where "information density is low", layouts are traditional and key targets stand out; content-heavy or unfamiliar layouts "should proceed with caution when adopting an ultraflat design" (E). Era-bound; the conditions are still valid.
- **Material "flat 2.0" with elevation shadows** (2014–2020, Material 1–2): shadow by dp level on most surfaces. Material 3 (2021 on) moved elevation to surface tone and made shadow optional for many components (B2.4, B5.1). The old "shadow on every card" is era-bound.
- **Neumorphism** (about 2019–2020, a Dribbble trend): a surface the same colour as the ground, shaped only by a light and a dark shadow. By B1.1 the shape edge is then near 1:1 against the ground, so a control drawn this way fails SC 1.4.11 unless it has a label or another cue. Era-bound; do not use. (Reasoning from WCAG 1.4.11, not from a source that names neumorphism.)
- **Glassmorphism** (about 2020–2022 on the web; macOS Big Sur 2020): translucent cards with background blur. Era-bound as a web card style; NN/g 2024 restricts it (B6.3). Apple Liquid Glass (June 2025) is a platform material for the functional layer only. House DNA bans glassmorphism cards; this agrees.
- **Neobrutalism hard offset shadow** (about 2021 on): `4px 4px 0` black shadows and thick black borders. Era-bound; impeccable allows it only "in a world that is actually neobrutalist".

## Part C. Is Manta's "borders first; shadow only on hover and popovers" supported?

- **Supported, with conditions.** Atlassian (static groups take a border or space, not a raised shadow), Polaris (no depth on static elements; most elements on one layer) and Material 3 (outlined, filled and elevated cards are equal in function; "style alone") all allow a border-first card system. NN/g's flat-design study does not argue against it, because Manta keeps strong signifiers (outline "View beds", coral CTA). So the rule is sound for **resting, static, light-ground content cards in a dense list**.
- **Where the rule breaks or is silent (the conditions the rule needs):**
  1. **Controls.** The rule's border colour `sand-border` is 1.24:1 on white. That is acceptable for a card (decorative edge) but fails SC 1.4.11 for an input, select, checkbox or toggle whose edge is the only identifier (B1.1; W3C Figure 42 fails a checkbox border at 2.7:1). The corpus uses `sand-border` for all of these. Manta needs a second border role for control edges at 3:1 or more (Material `Outline` vs `OutlineVariant`; Carbon `border-strong` 3:1 vs `border-subtle`; GOV.UK `input-border` black vs `border` tint-80). Measured example, not a proposal: a mix of `sand-border` and `ink` at 50% (#7C8E8C) is 3.44:1 on white and 3.19:1 on sand.
  2. **Floating elements.** Sticky compare bar, sticky mobile handover bar, nav panel, dialog, toast, tooltip: these float above content and need a shadow (B2.1, B2.2). The corpus already does this, but the rule says only "hover and popover". The rule needs the words "and anything that floats above content".
  3. **Night ground.** On `ink`, a shadow is almost invisible (B2.4). The rule does not say how a raised or overlay surface shows on ink (a lighter surface tone, or a light low-alpha edge).
  4. **Hover uses two signals.** `.dest-card:hover` changes the border to `lagoon` and adds a shadow. Atlassian says "Use one or the other"; Material combines them. impeccable's detector flags "hairline border plus wide diffuse shadow". The house has not chosen. A choice is needed, with the reason (the brand's "calm machine" working area argues for one signal).
  5. **Rest shadow drift.** `--shadow-card` exists and `HostelCard.jsx` uses it at rest; `globals.css` says "no shadow at rest". The rule must say whether a 0 1px 2px shadow at 6% is "heavy" (DESIGN.md bans only a "heavy" shadow at rest).
  6. **Fill step is weaker than the border.** White card on sand-page = 1.08:1; border 1.15–1.24:1. "White = elevated" depends on a step that poor screens and bright sun (a beach-travel audience on phones) can lose. The photo-led row helps because the photo defines the left edge. This is a risk to note, not a WCAG failure.

## Part D. House coverage per attribute

Key: C = covered; P = partly; G = gap; I = covered by impeccable. "Cond" = does the house rule state its conditions?

| Attribute | Manta | design-vault | impeccable | Cond | Notes |
|---|---|---|---|---|---|
| Border use (when, what replaces it) | P: "borders first" (B46), card spec | G | P: distill/quieter "remove borders that don't serve"; layout "proximity before containers" | No | No rule says border vs space vs fill per element function. |
| Border colour and contrast roles | P: one token `sand-border` for cards, dividers and controls | G | P: colorize "borders and separators" role; 3:1 for controls | No | No split of decorative edge vs control edge; corpus controls at 1.24:1. |
| Border thickness | P: 1–1.5px cards; 1.5px controls and outline buttons | G | G | No | No rule says when 1px vs 1.5px vs 2px. |
| Shadow and elevation levels | P: three tokens, rule "hover and popover" | G | P: craft-floor "offset and soft blur"; bans glow and hard offset | No | No named levels by role; sticky bars and night ground not covered. |
| Hover and press depth | P: "Hover lightens or tints a ground; press scales to 0.97" | G | P: craft-floor states | No | Live hover = border + shadow, against the stated "lightens or tints". |
| Corner radius scale | C: 6/8/12/999 | P: DNA bans "one rounding by habit" | I: detector "radius outside DESIGN.md"; quieter "reduce radius extremes" | No | No meaning per step; 5px checkbox off-scale; CTA pill vs 8px drift. |
| Radius nesting | G | G | P: "nested cards are always wrong" (avoids the case) | — | Flush photo in card relies on `overflow: hidden`; no concentric rule. |
| Shape as brand | G (one taste note on the vibe strip) | P: DNA line on rounding | G | No | Quicksand (rounded) display face and 12px cards fit a soft brand; not written. |
| Dividers | P: `sand-border` is the divider colour | G | P: proximity before containers | No | No rule on divider vs space vs fill. |
| Fills and tints (cards, wells) | C: white = elevated; tinted cards only for special rows (B17) | G | P: colorize roles | Yes (B17 names its condition) | Most conditioned rule in this category. |
| Selected and hover tints | P: lagoon wash for hover and selected (B20) | G | P: polish "every state" | Partly | Wash is 1.11:1; selected needs a second 3:1 cue (B5.2). |
| Scrims | G (two values in use: black 40%, ink 45%) | G | P: colorize "check overlays" | — | No token. |
| Text on photos | G | P: design-round prompts leave a clear area for headlines in generated art | P: craft-floor contrast; detector "raster under a wash" | — | Card photo dots use an undocumented halo. |
| Glass and blur | G (implicitly "UI is flat") | C: DNA bans glassmorphism cards | I: refuse "glass as decoration"; audit blur cost | No | Bans without the condition (functional layer vs content). |
| Focus ring | C: lagoon, ink on turquoise, never removed (B47) | G | I: audit and critique "visible focus" | Yes (ground) | Not covered: 2.4.11 (sticky bars), 2.4.13, forced-colours, corpus Input's border-only focus (2.94:1 change). |
| Error and state outlines | C: danger border, never colour alone | G | P | Yes | — |
| Icon stroke | C: ~1.75px at 20px, rounded caps (B44) | G | I: craft-floor "one consistent stroke and weight"; polish | No | No rule for other sizes or for matching border weight or text weight. |
| Stroke vs border weight | G | G | G | — | Values happen to sit in a 1–2px band. |
| Dark-mode surfaces | P: night pattern covers text and semantic colour, not elevation | G | P: colorize "design surface elevation explicitly" in dark mode | Partly | — |

## Part E. Interactions between attributes (given X, do Z)

1. **Border + shadow.** Given a resting static card, use a border OR a fill step, not a shadow (B2.1). Given hover, change one thing: a surface tint or an elevation, not both (Atlassian; Material disagrees). Given a floating element, use a shadow; a border on it is optional and should be the weak role. A hairline border plus a wide soft shadow on the same resting element reads as the 2024-era "generated UI" look (impeccable detector).
2. **Border + fill (tint).** Given a fill step that already separates the card (Carbon layer alternation, Polaris grey footer), drop the border or keep it in the weak role; do not use a strong border and a strong fill together. Given a fill step under about 1.1:1 (Manta's white on sand), keep the border.
3. **Border + space (proximity).** If the spacing already makes the groups, a border adds little (B1.5). If they disagree, the grouping becomes ambiguous; fix the spacing first.
4. **Divider + card.** Given cards with their own edges, no dividers between cards. Inside a card, use one separator type per card (a divider OR a fill band).
5. **Radius nesting.** Given an inner element with padding p inside radius R, inner radius = max(R − p, fallback). Given a flush photo, it shares the outer radius on the touching corners. Given a capsule outer, inner capsules stay concentric naturally (Apple).
6. **Radius + density + pointer.** Given dense desktop rows, rounded rectangles; capsules for touch layouts, tags and one standout action (Apple WWDC25-356).
7. **Radius + meaning.** Given a brand radius change, keep checkbox square-ish and radio round (Radix).
8. **Tint + state.** Given a pale tint for selected, add a check, weight or 3:1 edge (WCAG 1.4.11). Given hover only, the pale tint alone is fine.
9. **Focus ring + ground + border.** Given more than one ground colour, a two-colour ring or one ring colour per ground (GOV.UK; Manta's ink-on-turquoise exception). Given an input with a border, add an outside ring or thicken the border on focus (GOV.UK) rather than only recolouring a 1.5px border. Given a box-shadow ring, keep a transparent outline for forced-colours mode.
10. **Focus + sticky bars.** Given a sticky header or bottom bar, add `scroll-padding` so focus is not hidden (SC 2.4.11).
11. **Stroke weight matching.** Given text weight W next to an icon, match the icon weight to W (Apple, Material). Given borders at 1–1.5px and icons at ~1.75px, keep both in one band; use 2px+ only for the focus ring so it stands out from all other lines. Given a light icon on a dark ground, use a lower grade (lighter stroke) (Material Symbols).
12. **Scrim + photo + text.** Given text over a varied photo, measure against the worst pixel, or use a panel. Given a modal over content, one scrim token.
13. **Glass + layer.** Glass only for a floating functional layer with strong blur and a solid fallback; never on content cards.
14. **Dark ground + elevation.** Given an ink ground, raise by a lighter surface, not by a stronger shadow.

## Part F. Per-attribute summary

- **Borders and outlines.** Two roles: a control edge at 3:1 or more when the edge is the only identifier (inputs, checkboxes, radios, toggles, empty rating units), and a weak decorative edge for cards and dividers (P, D). Remove a border when space or a fill step already does its job; keep it when the fill step is tiny or space is short (E, R). Manta: one role only, so controls fail. **Partly covered, conditions not stated.**
- **Shadows and elevation.** Depth means "floats above" or "interactive". Static groups stay on one layer. Few named levels; pair surface and shadow; on dark grounds use surface lightness (D). Manta's border-first rule agrees for static cards; it is silent on sticky bars, night ground and the hover double signal. **Partly covered, conditions not stated.**
- **Corner radius and shape.** A small scale tied to element size; concentric nesting; capsule versus rounded rectangle by density and pointer; shape carries meaning (checkbox versus radio); radius is a brand lever (D, weak R). Manta has a scale with no meaning per step, no nesting rule, and a CTA shape drift. **Partly covered; nesting a gap.**
- **Dividers.** Thin, weak-role lines that group; full width for unrelated sections, inset for related items; prefer space where room exists (D). Manta names only the colour. **Gap in when-to-use.**
- **Fills and tints.** Layered surface tones; a darker well recedes, a lighter card comes forward; a selected tint needs a 3:1 second cue (P, D). Manta's B17 and B20 are the best-conditioned rules in this category, but the lagoon wash alone cannot carry "selected". **Covered for grounds; partly for states.**
- **Transparency, scrims and blur.** One scrim token (32–60% in expert systems); text on photos measured on real pixels; glass only for a functional floating layer, with strong blur and a fallback (P, D, E). Manta has no scrim token and two values. **Gap.**
- **Focus and state outlines.** AA: visible, 3:1 against adjacent, not hidden by sticky UI. AAA: 2px perimeter and 3:1 change. Two-colour or per-ground rings. Ring for fields, highlight for rows (P, D). Manta is strong on ring colour per ground; it lacks 2.4.11, the input focus treatment and forced-colours. **Covered for colour; partly for the rest.**
- **Icon stroke weight.** One stroke and weight family; match the adjacent text weight; adjust stroke with size; lighter grade on dark grounds (D). No source ties icon stroke to border width; that link is an inference. Manta has one size's value only. **Partly covered.**

## Part G. Gaps ranked by how often they affect the Manta site

Frequency basis: the working area (search results, filters, compare, detail, handover) is where users spend time; each results row repeats every card treatment. Live `app/` today has the homepage, destination pages and legal pages; the corpus `docs/design-system/ui_kits/` holds the planned search, compare, detail and handover screens.

1. **Control edges below 3:1** (inputs, selects, the compare checkbox on every results row, empty checkbox at 1.24:1). Every search and filter view; every row. A probable SC 1.4.11 (AA) failure as soon as the corpus is built. No house rule; impeccable's contrast lint may catch some.
2. **Card state model** (hover double signal border + shadow; rest-shadow drift between `HostelCard.jsx` and `globals.css`; selected tint 1.11:1 with no second cue). Every card on every list page and the homepage.
3. **Floating and sticky surfaces** (no rule names sticky bars; four shadow values; SC 2.4.11 focus hidden under the sticky compare bar and the mobile handover bar). Every search view and every mobile detail view.
4. **Input focus treatment** (corpus Input removes the outline and only recolours a 1.5px border; change contrast 2.94:1; no forced-colours fallback). Every form field, including the hero search box on marketing views.
5. **Radius meaning and nesting** (CTA capsule in live code versus 8px in DESIGN.md; 5px checkbox off-scale; no concentric rule for photo-in-card or chip-in-card). Every view has the one coral CTA; every results row nests a photo.
6. **Divider versus space versus fill** (no rule). Detail page sections, comparison table rows, handover module.
7. **Icon stroke at other sizes and its relation to borders and text weight** (only "~1.75px at 20px"). Amenity icons on every row, but current values sit near the border band, so the visible effect is small.
8. **Scrim and text-on-photo** (two scrim values; no rule for text or controls on hostel photos). Mobile nav, dialogs, card photo dots; hero grounds are flat turquoise, so lower frequency.
9. **Elevation on the night ground** (no rule). Nav panel, footer, announcement block; few raised items there.
10. **Glass and blur** (not used; DNA ban already holds). Rare.

Write scope: every fix above is in Manta's own files (`DESIGN.md`, brand sheet §10, `docs/design-system/`, `app/globals.css`). Owner: lucmoseley/mantahostels.

## Bound

**Read in full:** design-vault#117 and #96 (gh); Manta `DESIGN.md` (241 lines); House DNA (`dna` in `data/gallery.json`); impeccable 4.5.0 `reference/craft-floor.md`; W3C Understanding 1.4.11 and 2.4.13 (via WebFetch extraction, two passes on 1.4.11); Polaris `content/design/depth/index.mdx` and `creating-depth.mdx`; Apple HIG Materials and Dark Mode (JSON); Atlassian Elevation (two passes); WWDC25-356 transcript (extraction); NN/g glassmorphism (2024) and flat-UI (2017) articles (extraction).

**Sampled (grep or part read):** Manta `docs/brand/brand-sheet.md` (grep for border, shadow, radius, focus, tint, stroke, outline, overlay; lines 24-104, 161-218, 340-407, 445-448 seen in grep context); `docs/design-system/tokens/*.css`, `components/**/*.jsx`, `ui_kits/app/SearchResults.jsx`, `MobileHostelDetail.jsx`, `guidelines/spacing-elevation.html`; `app/globals.css` lines 85-185, 370-432, 546-640, 709-770 and a grep of class names. design-vault `plugin/skills/design-critique/SKILL.md`, `design-round/SKILL.md` and `references/*.md` (grep only); `docs/research/design-rules-census.md` rows B17, B20, B44, B46, B47 and lines 270, 358; `docs/research/design-coverage-gaps.md` and `impeccable-checks.md` (grep). impeccable 4.5.0 `colorize.md` lines 25-66, grep of `layout`, `polish`, `audit`, `critique`, `distill`, `quieter`, `harden`, `bolder`, `component-review`, `craft`, `shape`. impeccable 4.2.1 not read directly; rule parity taken from design-vault `impeccable-checks.md:77`. androidx Compose Material 3 token files (Dialog, ElevatedCard, OutlinedCard, FilledCard, FilledButton, OutlinedButton, OutlinedTextField, FilledTextField, SheetBottom, Menu, FilterChip, Elevation, Shape, Scrim, State, Divider, ButtonSmall); material-components-android `Card.md`, `Shape.md`, `Color.md` (grep), `Divider.md` (first 80 lines); Carbon Color Usage and Tokens pages (extraction); GOV.UK Focus states page and govuk-frontend `settings/_measurements.scss`, `components/input/_mixin.scss`, `helpers/_focused.scss`, `settings/_colours-functional.scss` (grep); Radix Themes Radius page; Apple HIG Layout, Color, Focus and selection, Icons, SF Symbols (JSON, grep); Lucide `stroke-width.md`; Google Fonts Material Symbols guide; W3C Understanding 1.4.3; refactoringui.com home page; Montoro and Luna 2015 abstract.

**Not read (claims from summaries or memory, marked in place):** Palmer 1992 full text; Bar and Neta 2006 full text; Enders zebra-striping articles; Refactoring UI book chapters other than "Use fewer borders"; m3.material.io pages (JavaScript-only; used androidx tokens and the Android docs instead); Polaris shadow-token values; Carbon's statement on where it uses shadows (not found).

**Searches run:** WebSearch: Material 3 elevation and surface container; Material 3 corner radius by component; Carbon shadow and floating elements; Polaris depth and bevels; Refactoring UI "use fewer borders"; Palmer 1992 common region; WWDC25 concentric corners; Bar and Neta curvature preference; zebra-striping evidence. Local: grep over Manta `DESIGN.md`, brand sheet, design-system tokens, components and ui_kits, `app/globals.css`; grep over design-vault skills and research; grep over impeccable references; GitHub tree listings for Shopify/polaris, alphagov/govuk-frontend and lucide-icons/lucide. Contrast ratios computed with the WCAG 2 relative-luminance formula in Python.
