# Rule records: surfaces

How boxes and layers look: borders and dividers, corner radius, shadows and elevation, surface tones, glass. The form is [rules.md](../rules.md)'s.

### vault.border-roles
- applies-when: web-surface; every border and divider, at desktop and phone width
- question: Does the page hold two border colours, a control edge for an edge that is a control's only identifier and a weaker decorative edge for cards, dividers and labelled buttons, each part taking the one its function calls for rather than its look?
- answered-by: builder
- writes: border colour role
- yields-to: vault.control-edges
- source: W3C Understanding SC 1.4.11 Non-text Contrast; Material 3 `Outline` and `OutlineVariant`, Carbon, GOV.UK `input-border` and `border`; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Keep two border tokens: a control edge at 3:1 for a text input, select, checkbox, radio, toggle track or empty rating unit, and a weak decorative edge for cards, dividers and buttons with a text label or clear icon; give a field shown by a fill alone that fill at 3:1, and measure the line as the browser renders it, not its token.
- reasons: design-critique/references/surface-styling.md#two-border-roles
- ledger: BTN-7, BTN-8, COL-2, COL-65, COL-94, FRM-82, FRM-83, FRM-90, SUR-5, SUR-11, SUR-51
- status: live

### vault.carry-contain
- applies-when: web-surface; every card, tile and other container
- question: Is a container look the site uses to mean "you can tap this" given only to containers a visitor can tap?
- answered-by: whole-page
- writes: container signifier
- yields-to: vault.borrowing
- source: Gaver, CHI '91, on false affordance; Polaris and Atlassian cards; #127 B7.2's carrier table; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Give tappable containers a look no static container on the site shares.
- reasons: design-critique/references/house-principles.md#carriers-and-reserved-properties
- ledger: FRM-5, SUR-76, SUR-77
- status: live

### vault.depth
- applies-when: web-surface; every shadow, and every part that floats over content
- question: Does a shadow sit only on a part that floats over content (a menu, popover, dialog, toast, tooltip, nav panel, or a sticky bar, which takes its shadow or a tone step once content scrolls under it) or one a visitor acts on, with every floating part taking one, no static part any, and the rows of a dense clickable list kept on one layer?
- answered-by: builder
- writes: shadow use
- yields-to: vault.surface-shadow, level 2
- source: Polaris depth, Atlassian Elevation and Material 3 elevation tokens; for the sticky bar, Material 3 top app bars on scroll and Chrome's scroll-state queries (2025); strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Give a shadow to every part that floats over content and to no static part, a sticky bar taking its shadow or tone step only once content scrolls under it; keep a dense list's clickable rows flat and show they are clickable on hover and in their own controls; one card that must look pressable among static content may take a small rest shadow where the brand is tactile.
- reasons: design-critique/references/surface-styling.md#depth-only-for-what-floats-or-acts
- ledger: SUR-34, SUR-35, SUR-39, SUR-40, SUR-42, SUR-44, SUR-47, SUR-53, SUR-54, SUR-76
- status: live

### vault.surface-shadow
- applies-when: web-surface; every shadow, and every part that floats over content
- question: Does no static part take a shadow, only a dialog, menu, tooltip, alert, popover, list box, button, link, or a fixed or sticky bar?
- answered-by: script
- writes: shadow use
- yields-to: none
- source: Polaris depth, Atlassian Elevation and Material 3 elevation tokens; for the sticky bar, Material 3 top app bars on scroll and Chrome's scroll-state queries (2025); strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Give no shadow to a static part.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#depth-only-for-what-floats-or-acts
- ledger: SUR-40
- status: live

### vault.shadow-levels
- applies-when: web-surface; every shadow
- question: Does every shadow belong to a level named by its role (rest, hover, overlay) and paired with its surface colour, one level per role the page uses, each drawn with an offset and a soft blur, with no zero-offset coloured glow and no hard offset shadow outside a neobrutalist brand?
- answered-by: builder
- writes: shadow level
- yields-to: level 2
- source: Atlassian Elevation (three shadows), Material 3 elevation tokens; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Name one shadow level for each role the page uses, about three where it has no drag and no nested overlays, each paired with its surface colour and drawn with an offset and a soft blur.
- reasons: design-critique/references/surface-styling.md#depth-only-for-what-floats-or-acts
- ledger: COL-80, SUR-34, SUR-35, SUR-39, SUR-40, SUR-47, SUR-48, SUR-62, SUR-68
- status: live

### vault.border-shadow
- applies-when: web-surface; every resting card and every floating part
- question: Does no resting element pair a hairline border with a wide soft shadow, and is any border on a floating part a decorative edge?
- answered-by: script
- writes: border and shadow pairing
- yields-to: vault.depth, level 2
- source: Polaris, Atlassian and Material 3 card and overlay tokens (`docs/research/surface-styling.md` Part E); strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Give a resting static card a border or a fill step; give a floating part its shadow, with any border on it in the decorative colour.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#interactions
- ledger: SUR-42
- status: live

### vault.border-fill
- applies-when: web-surface; every card or panel that a fill step sets apart from its ground
- question: Where a fill step sets a card apart, is its border dropped or kept decorative, never a strong border with a strong fill, and is a border kept wherever that fill step is under about 1.1:1 against the ground?
- answered-by: builder
- writes: border and fill pairing
- yields-to: vault.border-roles, level 2
- source: Carbon's tile, 1.10:1 on white, the lowest fill-only step a major design system ships; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- inputs: the fill step's contrast against the ground
- output: under about 1.1:1, keep a decorative border; at or above it, drop the border or keep it decorative
- target: Separate a card by a fill step or a decorative border, not a strong one of each; below about 1.1:1, keep the border.
- reasons: design-critique/references/surface-styling.md#interactions
- ledger: COL-78, COL-109, SUR-42
- status: live

### vault.dark-elevation
- applies-when: web-surface; every raised or overlay surface on a dark ground or in dark mode
- question: On a dark ground, does each raised or overlay surface show its level by a lighter surface tone, with a light low-alpha edge where one is needed, rather than a heavier shadow?
- answered-by: builder
- writes: dark elevation
- yields-to: vault.dark-raise, level 2
- source: Atlassian Elevation (atlassian.design, as read Oct 2026), on a higher surface looking lighter in dark mode; Apple HIG Dark Mode, Material 3 surface containers; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: treatment
- target: Raise a surface on a dark ground with a lighter surface token per level, adding a light low-alpha edge where needed, never a stronger shadow.
- reasons: design-critique/references/surface-styling.md#elevation-on-a-dark-ground
- ledger: COL-49, SUR-40, SUR-49, SUR-62, SUR-65, SUR-68
- status: live

### vault.dark-raise
- applies-when: web-surface; every raised or overlay surface on a dark ground or in dark mode
- question: On a dark ground, is each dialog, menu, list box and popover drawn on a lighter surface than the ground behind it?
- answered-by: script
- writes: dark elevation
- yields-to: none
- source: Atlassian Elevation (atlassian.design, as read Oct 2026), on a higher surface looking lighter in dark mode; Apple HIG Dark Mode, Material 3 surface containers; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: treatment
- target: Raise an overlay on a dark ground with a lighter surface tone.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#elevation-on-a-dark-ground
- ledger: SUR-40
- status: live

### vault.radius-nesting
- applies-when: web-surface; every shape nested in a rounded shape: a photo, chip or button inside a card
- question: Does each inner shape take the radius the formula below gives, a photo flush in a card sharing the card's radius on the corners it touches, and a capsule inside a capsule staying concentric?
- answered-by: builder
- writes: inner radius
- yields-to: level 2
- source: Apple WWDC25 session 356 and SwiftUI `concentric(minimum:)`; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- inputs: the outer radius R, the even padding p between the shapes, the project's small fallback radius
- output: inner radius = max(R − p, fallback); a corner flush with the outer shape takes R
- target: Set each nested shape's radius from its parent's radius and padding, never one fixed token on parent and child.
- reasons: design-critique/references/surface-styling.md#radius-nesting
- ledger: SUR-26, SUR-30
- status: live

### vault.radius-density
- applies-when: web-surface; every rounded control, row, tag and chip
- question: Do dense desktop rows and their controls take rounded rectangles, with capsules kept for touch layouts and status chips?
- answered-by: builder
- writes: corner shape
- yields-to: vault.tag-shape, vault.key-action, level 2
- source: Apple WWDC25 session 356 on capsules against rounded rectangles by density and pointer; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: treatment
- target: Use rounded rectangles in dense desktop rows; save capsules for touch layouts, tags, status chips and one standout action.
- reasons: design-critique/references/surface-styling.md#interactions
- ledger: BTN-3, BTN-20, SUR-23, SUR-25, SUR-26
- status: live

### vault.key-action
- applies-when: web-surface and has-cta; the part the building session declares the main action
- question: Is the view's main action a capsule, its corner radius at least half its height, and taller than every other button on the page?
- answered-by: script
- writes: main action shape
- yields-to: none
- source: Apple WWDC25 session 356 on capsules against rounded rectangles by density and pointer; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: treatment
- target: Draw the main action as a capsule, one size step above every other button.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#interactions
- ledger: BTN-20
- status: live

### vault.tag-shape
- applies-when: web-surface; every tag the building session declares, at phone width
- question: At phone width, is each tag fully rounded, with a radius no less than half its height?
- answered-by: script
- writes: tag shape
- yields-to: none
- source: Apple WWDC25 session 356 on capsules against rounded rectangles by density and pointer; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: treatment
- target: Draw each tag as a capsule in a touch layout.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#interactions
- ledger: SUR-25
- status: live

### vault.radius-meaning
- applies-when: web-surface; every checkbox and radio
- question: Whatever the brand radius, does the checkbox stay square-ish and the radio round?
- answered-by: builder
- writes: control shape
- yields-to: none
- source: Material 3 and Apple HIG selection controls, where the square box means many choices and the circle one (`docs/research/surface-styling.md` B3); strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Keep checkboxes square-ish and radios round under any brand radius.
- reasons: design-critique/references/surface-styling.md#interactions
- ledger: FCH-9, NEW2-45, SUR-24
- status: live

### vault.dividers
- applies-when: web-surface; every divider, and every gap between groups
- question: Are groups that padding already separates left without a divider, a divider used only where room is short (full width between unrelated sections, inset between related items) in the decorative edge colour, cards that have their own edges given none between them, and a card's secondary area set apart by a fill band or one divider but never both?
- answered-by: builder
- writes: divider
- yields-to: vault.grouping
- source: Material dividers, GOV.UK, Apple HIG Layout, Polaris; Palmer 1992 and Montoro and Luna 2015 on common region against proximity; jakub.kr notes (11 Oct 2026) on a card's toolbar or footer; strength: design-system guidance and published research
- era: timeless
- owner: vault
- stage: treatment
- target: Separate groups by space where there is room; where room is short, use a decorative divider, full width between unrelated sections and inset between related items; inside a card use one separator kind.
- reasons: design-critique/references/surface-styling.md#dividers-against-space-and-fill
- ledger: COL-94, FRM-5, LAY-6, SUR-8, SUR-9, SUR-10, SUR-11, SUR-76, SUR-83, TXL-79
- status: live

### vault.glass
- applies-when: web-surface; every translucent or blurred layer
- question: Is translucency with blur used only on a layer that floats over content and holds controls or navigation, never on a content card, with strong blur, its text at the contrast floor against the worst backdrop, and a solid fallback under `prefers-reduced-transparency` and `prefers-contrast`?
- answered-by: builder
- writes: glass
- yields-to: vault.contrast, level 2
- source: NN/g, Brown 2024; Apple HIG Materials; impeccable 4.5.0 (weak); strength: domain evidence
- era: dated 2027-10-14
- owner: vault
- stage: treatment
- target: Put glass only on a sticky bar or nav floating over content, with strong blur, text at its contrast floor against the busiest backdrop, and a solid layer under reduced transparency or more contrast.
- reasons: design-critique/references/surface-styling.md#glass-only-on-a-floating-functional-layer
- ledger: COL-16, COL-57, COL-59, COL-70, COL-85, COL-87, OTH-46, PAG-19, SUR-53, SUR-57, SUR-90
- status: live

### vault.tag-fill
- applies-when: web-surface; every tag, badge and lozenge that labels a status or category and is not a control
- question: Does each tag or badge take a light tint with darker text of its own hue, a bold dark fill kept for the few a visitor must not miss, such as an unread count?
- answered-by: script
- writes: tag fill strength
- yields-to: level 2
- source: GOV.UK Design System, Tag: white text on a dark fill was changed to "a lighter background colour and darker text" after research from several teams found users took the tags for buttons (Dec 2023 change); Atlassian Design System, Badge, "Only use bold semantic badges for elements of high importance" (both as read Oct 2026); strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Give a tag or badge a light tint with darker text in the same hue; keep a bold dark fill for the rare badge a visitor must not miss, such as an unread count.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: badge
- reasons: design-critique/references/surface-styling.md#tag-fills
- ledger: SUR-85
- status: staged

### vault.inverse-surface
- applies-when: web-surface; every snackbar, toast and plain tooltip: a short message laid over the page
- question: Does each toast and plain tooltip sit on the other side of mid lightness from the page, dark on a light theme and light on a dark one, with its text on the other side from its surface?
- answered-by: script
- writes: passing message surface
- yields-to: level 2
- source: Material 3: the snackbar's container `colorSurfaceInverse`, label `colorOnSurfaceInverse` and action `colorPrimaryInverse` (material-components-android, docs/components/Snackbar.md), and the plain tooltip's `InverseSurface` container with `InverseOnSurface` text (androidx Compose Material 3, PlainTooltipTokens), both as read Oct 2026; strength: design-system guidance
- era: dated 2027-10-16
- owner: vault
- stage: treatment
- target: Set a snackbar, toast or plain tooltip on the inverse surface, dark on a light theme and light on a dark one, with inverse text and any action in the inverse primary.
- script: check-state.py, its inverse line
- reasons: design-critique/references/surface-styling.md#inverse-surfaces-for-passing-messages
- ledger: SUR-69
- status: staged

### vault.inverse-surface-look
- applies-when: web-surface; every snackbar and toast that holds an action
- question: Is the action in each snackbar or toast set in the inverse primary, the theme's primary as it reads on the inverse surface?
- answered-by: look
- writes: passing message action colour
- yields-to: vault.inverse-surface
- source: Material 3: the snackbar's container `colorSurfaceInverse`, label `colorOnSurfaceInverse` and action `colorPrimaryInverse` (material-components-android, docs/components/Snackbar.md), and the plain tooltip's `InverseSurface` container with `InverseOnSurface` text (androidx Compose Material 3, PlainTooltipTokens), both as read Oct 2026; strength: design-system guidance
- era: dated 2027-10-16
- owner: vault
- stage: treatment
- target: Set a snackbar's or toast's action in the inverse primary.
- reasons: design-critique/references/surface-styling.md#inverse-surfaces-for-passing-messages
- ledger: SUR-69
- status: staged

### vault.joined-fills
- applies-when: web-surface; adjacent columns, stripes or cells whose fills must read as one unbroken surface, at every display scale
- question: Where adjacent columns or stripes must read as one unbroken fill, does the shared colour sit on their container, or does each width land on a whole device pixel at every display scale, so no hairline seam shows between them?
- answered-by: script
- writes: seams between joined fills
- yields-to: none
- source: Josh W. Comeau, "Pride flags" (2023, updated 2025), whole-pixel column widths against gaps in Firefox and Safari; measured on design-vault#278 (docs/research/layout-data-defaults.md): Chromium 149 drew a seam between equal black columns wherever a width times the display scale missed a whole device pixel, whole CSS-pixel widths at 125, 150 and 175% included, and none at any scale with the colour on the container, Firefox and Safari unmeasured; strength: practitioner writing and a measurement
- era: dated 2027-10-16
- owner: vault
- stage: treatment
- target: Paint a fill that adjacent columns or stripes share on their container, so the parts' edges never show; where each part must keep its own colour, size it to whole pixels.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/surface-styling.md#seams-between-joined-fills
- ledger: LAY-36
- status: live

### vault.forced-colour-edges
- applies-when: web-surface; every form control and button
- question: Is each form control's and button's edge drawn by a `border` or `outline`, or a `box-shadow` backed by a border of some width, so it survives forced-colours mode?
- answered-by: script
- writes: meaningful edge mechanism
- yields-to: level 2
- source: MDN, `forced-colors` (last modified 20 Apr 2026, as read Oct 2026): in forced colors mode "box-shadow is forced to 'none'", while `border-color` and `outline-color` take system colours; Josh Comeau, "Introducing Shadow Palette Generator" (16 Nov 2021): "Shadows can be thought of as a progressive enhancement; the product should still be fully usable even without shadows"; strength: platform guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Draw every edge that carries meaning with a border or outline, or back a box-shadow ring or level with a transparent outline, or a transparent border with the fill clipped by `background-clip: padding-box` (#424), and let no meaning rest on a shadow alone.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#edges-that-survive-forced-colours
- ledger: SUR-49
- status: live

### vault.shadow-meaning
- applies-when: web-surface; every edge or level outside the controls that carries meaning: a selected or current state, the edge of a menu, dialog, popover or card that must stand apart from what lies under it
- question: Is each edge outside the controls that carries meaning drawn as a `border` or `outline`, or as a `box-shadow` over a transparent `border` or `outline` of equal width, so no meaning rests on a shadow that forced-colours mode drops?
- answered-by: look
- writes: meaningful edge mechanism
- yields-to: vault.forced-colour-edges, level 2
- source: MDN, `forced-colors` (last modified 20 Apr 2026, as read Oct 2026): in forced colors mode "box-shadow is forced to 'none'", while `border-color` and `outline-color` take system colours; Josh Comeau, "Introducing Shadow Palette Generator" (16 Nov 2021): "Shadows can be thought of as a progressive enhancement; the product should still be fully usable even without shadows"; strength: platform guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Draw every edge that carries meaning with a border or outline, or back a box-shadow ring or level with a transparent border or outline, and let no meaning rest on a shadow alone.
- reasons: design-critique/references/surface-styling.md#edges-that-survive-forced-colours
- ledger: SUR-49
- status: live

### vault.radius-scale
- applies-when: web-surface; every corner radius on the page
- question: Does every corner radius come from one scale of three to five steps, each step tied to an element class and no larger class taking a smaller step than a smaller one: small detail parts (checkbox, badge) and tags at the low steps, controls above them, cards, menus and popovers above controls, and modals, sheets and page-size containers at the largest, with the capsule kept to the classes the project names?
- answered-by: script
- writes: radius step
- yields-to: vault.radius-nesting, vault.radius-meaning, vault.shape-family, level 2
- source: Atlassian Design System, Foundations, Radius (as read Oct 2026): tokens tied to classes, "badges, checkboxes" 2px, "labels, lozenges ... tags" 4px, "buttons, inputs" 6px, "cards, in-page containers, floating UI, dropdown menus" 8px, "modals, Kanban columns, tables" 12px, to ensure "consistency and cohesion"; Material 3 shape scale, material-components-android Shape.md and androidx ShapeTokens (as read Oct 2026), text field extra-small, filter chip small, card medium, dialog extra-large, "Material Design encourages brand expression through shapes"; USWDS border utilities, radius 0, sm, md, lg, pill; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: value
- inputs: the element's class (detail part, tag, control, container, large container or modal), the project's radius scale
- output: each class one step of a 3–5 step scale, the step never falling as the class grows; the values are the project's
- target: Keep one radius scale of three to five steps and give each element class one step, larger elements never a smaller step than smaller ones.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#a-radius-scale-by-element-size
- ledger: OTH-11, SUR-22, SUR-27, SUR-28
- status: staged

### vault.shadow-form
- applies-when: web-surface; every box shadow
- question: Do all shadows cast from one light source, offset in the same direction with the vertical offset the larger, their offset and blur growing and their opacity falling as the level rises, each tinted a dark of the ground's hue rather than grey-black, and does no surface take an inset shadow?
- answered-by: script
- writes: shadow form
- yields-to: vault.shadow-levels, level 2
- source: Josh W. Comeau, "Designing Beautiful Shadows in CSS" (updated Apr 2026): "a single light source for all elements on the page"; as an element rises "The blur radius gets larger. The shadow becomes less opaque"; transparent black "desaturates" the ground, so match the shadow's hue; Polaris, Depth, Creating depth (github.com/Shopify/polaris, 2024): "Use unique styles for surfaces, like inset shadows" is a don't, and "Use consistent shadow and bevel styles across your interface"; strength: practitioner writing and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- inputs: the shadow's level, the ground's hue
- output: offset (same direction for every shadow, vertical larger) and blur rising with the level, opacity falling with it; colour a dark of the ground's hue at low alpha; spread left at 0 unless the project sets it
- target: Cast every shadow from one light above, growing offset and blur and lowering opacity as the level rises, tint it with the ground's hue, and set no inset shadow on a surface.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#one-light-source
- ledger: SUR-35
- status: staged

### vault.surface-layers
- applies-when: web-surface; every container fill: page ground, card, panel, well
- question: Does every container fill come from a small set of named surface levels (page ground, container, nested container, and a sunken well where one is used), a container nested in another taking the next level rather than its parent's tone, a sunken well used only on the default level as a backdrop that groups content such as a board's columns and never inside a raised or overlay surface, and any border on a level taking the border paired with that level?
- answered-by: look
- writes: surface tone level
- yields-to: vault.surface-shadow, vault.dark-raise, vault.dark-elevation, vault.border-fill, level 2
- source: Carbon Design System, Color, Usage (updated Sep 2026): "There are four layers within a theme: base layer, layer 01, layer 02, and layer 03. Layers stack one on top of the other in a set order"; "Border tokens however, pair with its same number"; Material 3 tonal surface container roles, five from lowest to highest, used "instead of elevation overlays" (material-components-android Color.md, as read Oct 2026); Atlassian Design, Elevation (as read Nov 2026), sunken "creates a backdrop (or well) where other content sits", "Only use sunken surfaces on the default surface level. Don't apply sunken elevations on raised or overlay elevations"; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Name a few surface levels (ground, container, nested container, well), give each nested container the next level, put a sunken well only on the default level as a backdrop for grouped content, and pair each level with its own border.
- reasons: design-critique/references/surface-styling.md#named-surface-levels
- ledger: SUR-40, SUR-52, SUR-62, COL-78
- status: staged

### vault.card-type
- applies-when: web-surface; every set of like cards: one list, grid or carousel
- question: Does a card take a treatment unlike the rest of its set only where it is a different kind of thing?
- answered-by: look
- writes: card treatment
- yields-to: vault.card-treatment, vault.depth, vault.carry-contain, level 2
- source: Material 3 Cards (material-components-android Card.md, as read Oct 2026): elevated, filled and outlined cards provide "the same legibility and functionality, so the type you use depends on style alone"; NN/g, Harley, "Similarity Principle in Visual Design" (2020): elements that look similar "are perceived as related, while elements that appear dissimilar are perceived as belonging to separate groups"; Polaris, Creating depth: "Use consistent shadow and bevel styles across your interface"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Pick one card treatment, outline, fill or raised, for each set of like cards and keep it; give another treatment only to a card of another kind.
- parts: card
- reasons: design-critique/references/surface-styling.md#one-card-type-per-set
- ledger: SUR-42
- status: staged

### vault.card-treatment
- applies-when: web-surface; every set of like cards: one list, grid or carousel
- question: Do the cards of one set, sharing a parent, take one edge and shadow treatment?
- answered-by: script
- writes: card treatment
- yields-to: none
- source: Material 3 Cards (material-components-android Card.md, as read Oct 2026): elevated, filled and outlined cards provide "the same legibility and functionality, so the type you use depends on style alone"; NN/g, Harley, "Similarity Principle in Visual Design" (2020): elements that look similar "are perceived as related, while elements that appear dissimilar are perceived as belonging to separate groups"; Polaris, Creating depth: "Use consistent shadow and bevel styles across your interface"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Give each set of like cards one treatment.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#one-card-type-per-set
- ledger: SUR-42
- status: staged

### vault.glass-dimming
- applies-when: web-surface; every clear, highly translucent glass layer over photos, video or other bright media
- question: Where a clear glass layer floats over bright media, does a dark dimming layer of about 35% opacity sit behind it, and is none added over media already dark or with its own dimming?
- answered-by: script
- writes: glass dimming layer
- yields-to: vault.contrast, vault.glass, level 2
- source: Apple HIG Materials, Liquid Glass (page updated Sep 2025, as read Oct 2026): for the clear variant, "If the underlying content is bright, consider adding a dark dimming layer of 35% opacity"; "If the underlying content is sufficiently dark ... you don't need to apply a dimming layer"; strength: platform guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- inputs: the luminance of the media under the glass
- output: bright media, a dark dimming layer at about 35% opacity; dark media or media with its own dimming, none
- target: Put a dark layer of about 35% opacity under clear glass that floats over bright media; leave it out over dark media.
- script: owed
- reasons: design-critique/references/surface-styling.md#dimming-under-clear-glass
- ledger: SUR-59
- status: staged

### vault.hr-break
- applies-when: web-surface; every separating line
- question: Is an `hr` used only for a thematic break between paragraphs (a scene change, a change of topic within a section) or between option groups in a select, with every other separating line drawn by a CSS border and none built from repeated characters?
- answered-by: builder
- writes: divider construction
- yields-to: vault.dividers
- source: HTML Living Standard, the `hr` element: "a paragraph-level thematic break", and "There is no need for an hr element between the sections themselves"; Butterick, Practical Typography, "Rules and borders": "Never make rules and borders out of repeated typographic characters" (both as read Oct 2026); strength: web standard and craft book
- era: timeless
- owner: vault
- stage: treatment
- target: Mark a change of topic between paragraphs with `hr`; draw every other line with a CSS border, never with repeated characters.
- reasons: design-critique/references/surface-styling.md#hr-for-a-thematic-break
- ledger: SUR-3
- status: live

### vault.typed-rules
- applies-when: web-surface; every separating line
- question: Is no line on the page typed from five or more repeated characters: dashes, underscores, equals signs, box-drawing rules, tildes, asterisks, bullets or dots?
- answered-by: script
- writes: typed rule
- yields-to: none
- source: Butterick, Practical Typography, "Rules and borders": "Never make rules and borders out of repeated typographic characters" (as read Oct 2026); strength: craft book
- era: timeless
- owner: vault
- stage: treatment
- target: Draw every separating line with a CSS border or `hr`, never with repeated characters.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#hr-for-a-thematic-break
- ledger: SUR-3
- status: staged

### vault.forced-colours-edge
- applies-when: web-surface; every control, card or chip whose edge or shape shows only by a `box-shadow`, a fill different from its ground, or a gradient
- question: Under `forced-colors: active`, does every control whose edge shows only by a shadow, a fill or a gradient keep a visible edge, because it carries a real border or outline, transparent where the normal design shows none?
- answered-by: script
- writes: forced-colours edge
- yields-to: none
- source: MDN `forced-colors` (source 20 Apr 2026, as read Oct 2026): `box-shadow` forced to none, `background-color` forced to a system colour, and a non-url `background-image` to none, while `border-color` and `outline-color` take system colours, with its button example given `border: 2px ButtonText solid`; govuk-frontend v6.6.0 `_focused.scss`, a transparent outline "which will be set to a visible colour"; USWDS buttons' GrayText border in forced colours; WCAG 2.2 failure F78 (as read Nov 2026) and the measurement on design-vault#424, Chromium 149's own ring hidden by a dark fill under a transparent border until `background-clip: padding-box`; strength: browser documentation and design-system guidance over WCAG 2.2 SC 1.4.11
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Give every button, chip or acting card drawn by a fill or shadow alone a `1px solid transparent` border, its fill clipped with `background-clip: padding-box` where it keeps the browser's focus ring, or a transparent outline beside a focus ring of its own, so forced colours paints its edge.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/edges-and-contrast.md#edges-in-forced-colours
- ledger: BTN-11
- status: staged

### vault.edge-alpha
- applies-when: web-surface; every border, divider and hairline
- question: Is an edge that must clear 3:1, a control edge, a state mark or a focus ring, drawn in a solid colour, or measured on each ground it lands on, and a decorative edge that lands on more than one ground drawn in the text colour at low alpha so it adapts to each?
- answered-by: script
- writes: edge opacity
- yields-to: vault.control-edges, vault.border-roles
- source: @atlaskit/tokens 20.6.1, `color.border` an alpha grouping edge, "Transparency helps UI adapt to different background colors", and every input, bold, focused and selected edge solid (as read Oct 2026); Apple UIKit `separator`, "may be partially transparent", against `opaqueSeparator`, "always opaque"; W3C Understanding SC 1.4.11 (WCAG 2.2, 2023), 3:1 against each adjacent colour; Krehel, "Details that make interfaces feel better" (on or before Mar 2026), alpha edges adapting to any ground; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- inputs: the edge's role; how many grounds it lands on
- output: control edge, state mark, focus ring: solid, or alpha measured at 3:1 on every ground; decorative edge on one ground: solid or alpha; decorative edge on several grounds, a photo included: the text colour at low alpha
- target: Draw control edges, state marks and focus rings in solid colours; draw a decorative edge that crosses several grounds in the text colour at low alpha.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/edges-and-contrast.md#solid-or-alpha-edges
- ledger: COL-86
- status: live

### vault.border-width
- applies-when: web-surface; every border, divider and keyline
- question: Is every border and divider 1 px, with width kept to show a state (2 px for selected, the focus ring at least 2 px) and colour to show what the edge is, a control's edge 1–2 px, and a thicker divider used only where strong lines on both sides would hide a 1 px one?
- answered-by: script
- writes: border width
- yields-to: vault.focus-ring, level 2
- source: Atlassian Border, `border.width` 1px "for all standard component borders and dividers", 2px selected and focused, "width tokens to control how thick and visible your border appears; color tokens to show what the border means" (as read Oct 2026); Material 3 Compose tokens v0_210, outlines and dividers 1dp, focus 2dp (5 Aug 2026); Apple HIG Split views, the one-point thin divider (9 Jun 2025); USWDS border utilities, 1px by default; GOV.UK form edges 2px; Butterick, borders half a point to one point; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- inputs: the edge's role and state
- output: decorative border or divider 1 px; control edge 1 px, or 2 px where the project's rules file picks it; selected 2 px with the selected colour; focus at least 2 px (`vault.focus-ring`); a divider between parts with strong lines of their own 2 px, the house's guess where Apple gives no figure
- target: Draw borders and dividers at 1 px, and show selection or focus by a 2 px width with its own colour.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/edges-and-contrast.md#width-and-style-of-a-line
- ledger: SUR-1, SUR-5
- status: live

### vault.border-style
- applies-when: web-surface; every border and rule
- question: Is every border a single solid line, a dotted or dashed line kept to a rule or grid line, used sparingly and drawn as a gradient where its dash must be exact, and no double, groove, ridge, inset or outset style used?
- answered-by: script
- writes: border style
- yields-to: level 2
- source: Butterick, Practical Typography, "Rules & borders": "don't use patterned borders", while thick or patterned rules "wear out their welcome faster" (as read Oct 2026); web.dev Learn CSS Borders, dotted, dashed and 3D styles drawn differently by each browser (2021); Freiberg, "Crafting the Next.js Website" (2023), a dotted grid line as a repeating gradient on a 1 px element; strength: expert writing
- era: timeless
- owner: vault
- stage: treatment
- target: Draw borders as one solid line; keep any dotted or dashed line to a rule or grid line, drawn as a gradient when the dash length matters.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/edges-and-contrast.md#width-and-style-of-a-line
- ledger: SUR-2
- status: staged

### vault.border-image
- applies-when: web-surface; every border drawn from an image or a gradient
- question: Is an image or gradient border kept to decoration, never a control edge or focus ring, drawn as two layered backgrounds where its corners are rounded, and backed by a plain `border-style` for when the image fails to load, or forced colours removes the layered backgrounds?
- answered-by: script
- writes: border image
- yields-to: vault.forced-colours-edge, level 2
- source: MDN `border-image` (27 Aug 2026): it "replaces the element's regular border", "border-radius has no effect on the border image", a gradient on a rounded box drawn "as the background instead", and a separate `border-style` "in case the border image fails to load"; MDN `forced-colors`, a non-url `background-image` forced to none (20 Apr 2026); strength: browser documentation
- era: timeless
- owner: vault
- stage: treatment
- target: Keep image and gradient borders to decoration; on a rounded box, draw the gradient edge as two layered backgrounds, with a plain border behind it.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/edges-and-contrast.md#width-and-style-of-a-line
- ledger: SUR-4
- status: staged

### vault.heading-rule
- applies-when: web-surface; every heading that carries a rule
- question: Where space alone does not set a section apart and its heading carries a rule, does the rule sit above the heading, or on both sides of a centred one, rather than below it?
- answered-by: script
- writes: heading rule
- yields-to: vault.heading-space, level 2
- source: Butterick, Practical Typography, "Rules & borders": rules are "best used sparingly", space tried first, and a heading rule put "above the heading (rather than below …)" so it separates the previous section, not the heading from its own (as read Oct 2026); web.dev Learn Design, Micro-layouts, rules either side of a heading by grid (2021); strength: expert writing
- era: timeless
- owner: vault
- stage: treatment
- target: Try space before a rule; where a heading takes one, put it above the heading, or on both sides of a centred heading.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/edges-and-contrast.md#width-and-style-of-a-line
- ledger: SUR-12
- status: staged

### vault.side-accent
- applies-when: web-surface; every block marked by a border on one side
- question: Is a side border kept to a block that is a distinct kind of content (a quote, an example, an aside, an alert) or to the active item of a navigation list, used sparingly, and never the only cue for information a visitor must not miss?
- answered-by: script
- writes: side border
- yields-to: level 2
- source: GOV.UK Design System, Inset text: a 10px left border for "quotes, examples, additional information", "Use inset text very sparingly", and not for "very important information" (govuk-frontend v6.6.0, as read Oct 2026); Refactoring UI, "Use accent borders to add color to a bland design", alerts and active navigation (Wathan and Schoger, 2018); strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Use a side border only to mark a quote, example, aside, alert or the active nav item, sparingly, and never as the only sign of something important.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/edges-and-contrast.md#side-accents
- ledger: SUR-15
- status: staged

### vault.ground-step
- applies-when: web-surface; every pair of neighbouring grounds: the page ground, surface levels, a section band, a region
- question: Does each pair of neighbouring neutral grounds keep the gap vault.colour-distance sets for large greys sharing an edge, and does the whole neutral set span no more than about 1.3:1 from the page ground, deeper levels alternating or reusing tones rather than darkening past it?
- answered-by: script
- writes: ground step size
- yields-to: vault.colour-distance, vault.border-fill, vault.control-edges
- source: Material 3 surface tones (material-components-android Color.md, changed 26 Aug 2024), light containers at tones 100 to 90, the span about 1.29:1; Carbon Color, Usage (updated 25 Sep 2026), `layer-01` #f4f4f4 on #ffffff and `layer-02` back to #ffffff, layers alternating; the gap per step is vault.colour-distance's founder ruling (#178), wider than Carbon's 2.2 ΔE00 or Material's 1.2; strength: design-system guidance
- era: timeless
- owner: vault
- stage: value
- inputs: the contrast ratio of each neutral level against the page ground; the gap between neighbouring levels
- output: each neighbouring gap at vault.colour-distance's floor for large greys (near white, about 1.14:1); the set within about 1.3:1 of the page ground, so near white two steps reach the span and a third level alternates back toward the ground
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/grounds-and-gradients.md#the-step-between-neighbouring-grounds
- ledger: COL-78, SUR-62
- status: staged

### vault.region-ground
- applies-when: web-surface; every persistent region of an app or signed-in tool: sidebar, rail, toolbar, panel, and the frame around the content
- question: Does the content sit on the default surface, each persistent sidebar, rail, toolbar or panel either sharing it behind a divider or one neutral level apart, and does a region change its ground across screen widths only where it becomes another component, such as a rail turning into a bottom bar or a docked panel into a drawer?
- answered-by: look
- writes: region ground
- yields-to: vault.region-fill, vault.bar-ground, vault.surface-layers, level 2
- source: material-components-android component docs (as read Nov 2026), NavigationRail on `colorSurface`, BottomNavigation on `colorSurfaceContainer`, NavigationDrawer on `colorSurfaceContainerLow`; impeccable 4.5.0 `operate.md`, "A second neutral layer for sidebars, toolbars, and panels"; Shopify Polaris, Creating depth (changed 15 Jan 2024), "Don't use bright or contrasting colors for container backgrounds or borders"; Polaris, Using color, "Multiple background colors can exist in the same viewport only if they exist side by side"; the breakpoint clause is the house's reading of these component colours; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Put content on the default surface; give each persistent sidebar, rail, toolbar or panel the same ground behind a divider or one neutral level apart; change a region's ground at a breakpoint only where it becomes a different component.
- reasons: design-critique/references/grounds-and-gradients.md#regions-in-an-app
- ledger: SUR-63, SUR-64
- status: staged

### vault.region-fill
- applies-when: web-surface; every persistent region of an app or signed-in tool: sidebar, rail, toolbar, panel, and the frame around the content
- question: Does each navigation region and aside sit on a neutral ground (OKLCH chroma under 0.05)?
- answered-by: script
- writes: region ground
- yields-to: none
- source: material-components-android component docs (as read Nov 2026), NavigationRail on `colorSurface`, BottomNavigation on `colorSurfaceContainer`, NavigationDrawer on `colorSurfaceContainerLow`; impeccable 4.5.0 `operate.md`, "A second neutral layer for sidebars, toolbars, and panels"; Shopify Polaris, Creating depth (changed 15 Jan 2024), "Don't use bright or contrasting colors for container backgrounds or borders"; Polaris, Using color, "Multiple background colors can exist in the same viewport only if they exist side by side"; the breakpoint clause is the house's reading of these component colours; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Keep navigation regions and asides on a neutral ground.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/grounds-and-gradients.md#regions-in-an-app
- ledger: SUR-63
- status: staged

### vault.bar-ground
- applies-when: web-surface; every bar: the site header, a service or section bar, a toolbar, a banner
- question: Does at most one bar on a page take a strong ground, the site's own header carrying the brand colour where the brief wants it, any bar beneath it that names the service or section on a light tint of the same hue (the general bar above, the specific below), and every banner and working toolbar on a quiet ground that draws no more attention than the content?
- answered-by: script
- writes: bar ground
- yields-to: vault.brand-layer, level 2
- source: GOV.UK Design System, Navigate a service (as read Nov 2026), the GOV.UK header on a "blue background" and the Service navigation on a "light blue background", "start with the most general (GOV.UK-wide) elements at the top"; USWDS Banner, "avoid color combinations that draw excessive attention to the banner"; impeccable 4.5.0 `mode-operate.md`, "a committed palette for the shell (a coloured rail or header, a tinted ground)"; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Give at most one bar a strong ground, the site header in the brand colour if the brief wants it; set a service or section bar under it on a light tint of the same hue; keep banners and working toolbars quiet.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/grounds-and-gradients.md#bars
- ledger: SUR-66, SUR-67
- status: staged

### vault.section-ground
- applies-when: web-surface; every page section and full-width band
- question: Does a section take its own ground only where its function, zone or reading mode changes (a persuade zone beside a working one, a confirmation or interruption, the footer), never as bands alternated for variety, with strong colour areas kept to confirmations, interruptions and the surfaces vault.tone-colour-share lets go committed, working areas on neutral grounds, and any band edge near the foot of the first screen leaving a sliver of the next section in view?
- answered-by: whole-page
- writes: section ground
- yields-to: vault.tone-colour-share, vault.brand-layer, level 2
- source: GOV.UK Panel (as read Nov 2026), a strong panel for "Confirmation pages" and "Interruption pages", "Never use the Panel component to highlight any other information"; NN/g, Flaherty, "The Illusion of Completeness" (2016), "a horizontal line that spans the width of the page can create a visual barrier", and a sliver of the next sections inviting the scroll, a band edge read as the same break by inference; Butterick, "Websites", "Layouts built with large blocks of color" among the '90s habits, and "less color is more effective"; Shopify Polaris, Creating depth (changed 15 Jan 2024), "Don't use bright or contrasting colors for container backgrounds or borders"; Palmer 1992, common region; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Change a section's ground only where its function, zone or reading mode changes; keep strong colour areas for confirmations, interruptions and the surfaces vault.tone-colour-share lets go committed, keep working areas neutral, and let the first screen show a sliver of the next section past any band edge.
- reasons: design-critique/references/grounds-and-gradients.md#section-grounds
- ledger: COL-79
- status: live

### vault.footer-ground
- applies-when: web-surface; a footer with a last block naming the site's owner, its legal and required links
- question: Does the footer's last block sit on a ground darker than the footer above it, a dark neutral or the brand's darkest, with the logo version made for dark grounds and colours that draw no more attention than the footer?
- answered-by: script
- writes: footer base ground
- yields-to: vault.logo-ground, level 2
- source: USWDS Identifier (as read Nov 2026), "Use a background color darker than that of the footer … Use primary or base family background colors of grade 80 or higher, or black", "Use logos intended for dark backgrounds if possible", "avoid color combinations that draw excessive attention to the identifier"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Set the footer's last block on a ground darker than the footer, use the logo version for dark grounds, and keep its colours quiet.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/grounds-and-gradients.md#the-last-footer-block
- ledger: SUR-70
- status: staged

### vault.card-image-tint
- applies-when: web-surface; every set of repeated cards that each carry an image
- question: Where repeated cards each take a tint from their own image, is the tint a low-chroma container tone drawn from the image's source colour with the card's text measured on it, used only where the image is the item's identity (an album, a place, a video), and never where a tint could read as a status or a category?
- answered-by: look
- writes: card tint from image
- yields-to: vault.colour-distance, vault.contrast, vault.surface-layers
- source: material-components-android Color.md (changed 26 Aug 2024), content-based colour from "album artwork, a brand logo, or a video tile", "Specific tones are mapped into specific color roles"; Shopify Polaris, Creating depth (changed 15 Jan 2024), "Don't use bright or contrasting colors for container backgrounds or borders"; the status and category exclusion is the house's; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- parts: card, image
- target: Tint a card from its image only where the image is the item's identity: take its source colour at low chroma as a container tone, measure the text on it, and keep tints off anything that could read as a status.
- reasons: design-critique/references/grounds-and-gradients.md#a-card-tinted-from-its-image
- ledger: SUR-71
- status: staged

### vault.list-header-fill
- applies-when: web-surface; every long list or table grouped under section headers
- question: Does each section header in a long grouped list take a quiet fill one neutral level from its rows, in place of a border around each group?
- answered-by: script
- writes: list section header fill
- yields-to: vault.surface-layers, vault.ground-step
- source: Rauno Freiberg, Notes 4 (as read Nov 2026), "If we throw the gray highlight on top of the section header it becomes so much easier to scan and jump between sections", after sections that were "very border heavy"; Shopify Polaris IndexTable (as read Nov 2026), a subheader row that "looks and behaves the same as the table header", to present "resources grouped by a relevant data value"; Palmer 1992, common region; strength: design-system guidance and published research
- era: timeless
- owner: vault
- stage: treatment
- target: Give each section header in a long grouped list a quiet fill one neutral level from its rows, in place of borders around the groups.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/grounds-and-gradients.md#section-headers-in-long-lists
- ledger: SUR-72
- status: staged

### vault.target-highlight
- applies-when: web-surface; every section or element a fragment link reaches on a long page
- question: Does the element a fragment link lands on take a quiet `:target` highlight, a fill one step from its ground or a side mark?
- answered-by: script
- writes: target highlight
- yields-to: vault.ground-step
- source: web.dev Learn CSS, Pseudo-classes (as read Nov 2026), `:target` "useful for highlighting areas that might have been specifically linked to"; MDN `:target`, used "to highlight the portion of a page that has been linked to from a table of contents"; strength: platform documentation
- era: timeless
- owner: vault
- stage: treatment
- target: Style `:target` with a quiet fill one step from its ground or a side mark.
- script: check-state.py, its target line
- reasons: design-critique/references/grounds-and-gradients.md#the-section-a-link-reached
- ledger: SUR-74
- status: staged

### vault.price-ground
- applies-when: web-surface; every price and the ground behind it
- question: Does each price sit on its section's own ground at full text contrast, with no band or panel of another lightness set behind the prices alone?
- answered-by: script
- writes: price ground
- yields-to: vault.brand-layer, vault.contrast
- source: CXL, "Which Color Converts the Best?" (2025 capture, read Nov 2026), unnamed "studies" finding prices on light grounds look dearer, no study named or linked; vault.brand-layer's high-stakes line (Norman 2002), which keeps a price plain; strength: published research on high-stakes moments; the CXL claim is unchecked and sets nothing
- era: timeless
- owner: vault
- stage: treatment
- target: Set each price on its section's own ground at full text contrast, with no band or panel behind the prices alone.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/grounds-and-gradients.md#prices
- ledger: SUR-75
- status: staged
