# Edges and contrast

Why each edge (border, outline, ring, hairline) takes the form its role calls for, and why each role keeps its contrast in every theme (#283). The research behind every line is `docs/research/edges-contrast.md` in the design vault.

A project's rules file wins over every record here except a floor WCAG or the law sets ([source precedence](house-principles.md#source-precedence)). A dated record is reviewed a year after writing, or sooner when a platform ships a new design language or WCAG a new version.

## Principles

### Contrast by role

Records: `vault.contrast-ladder`, `vault.theme-contrast`.

- **Why.** WCAG sets floors by role: 4.5:1 for text, 3:1 for large text and for whatever alone shows a control or its state. A decorative edge has no floor, and the systems that publish one keep it faint: Atlassian's grouping border measures 1.35:1, Material's `outlineVariant` 1.6–2.0:1, GOV.UK's `border` 1.6:1. WCAG notes that thin strokes are harder to read at low contrast and that anti-aliasing draws a thin line fainter than its colour, so a thin face or a 1 px edge needs margin above the floor; Apple asks 7:1 for small text in custom colours. Material holds each role to one minimum in light and dark alike and raises it at higher contrast levels, and Atlassian warns that a light theme that passes says nothing about the dark one.
- **Trade-off.** 7:1 narrows the palette for a thin face; a heavier weight or a larger size buys the same legibility (`vault.type-weight`). A decorative edge strong enough to pass 3:1 competes with the control edges it should sit behind.
- **Clash.** The WCAG floors in `vault.contrast`, `vault.control-edges` and `vault.focus` beat every aim here. The 7:1 aim for thin faces, the 4.5:1 aim for 1 px lines and the 0.06 em stem line are the house's mapping, not a finding. APCA is not settled (`docs/research/text-presentation.md`), so the ladder is in WCAG 2 ratios.

### Text on a fill

Record: `vault.fill-text`.

- **Why.** White and black tie at 4.58:1 on a fill of relative luminance 0.179; below it white wins, above it black, which is what CSS `contrast-color()` computes (Baseline April 2026). Near the tie neither clears 4.5:1 with room, so the fill moves, not the text size. USWDS grades make a same-hue pair portable: 50 grades apart passes AA in either polarity, so the rule holds in light and dark.
- **Trade-off.** Dark text on a saturated mid-tone fill (yellow, lime, sky) looks heavier than the brand may want; moving the fill darker for white text changes the brand colour.
- **Clash.** A logo colour fixed by `vault.logo-anchors` is not moved; it takes a text-safe partner instead.

### Disabled controls

Record: `vault.disabled-legibility`.

- **Why.** WCAG exempts inactive controls, and W3C says no one fix suits everyone. Systems split: Atlassian's disabled text measures 2.0:1, Material's 2.3–3.0:1, USWDS keeps 5.8:1. NN/g asks for lower contrast that a visitor can still read, but not so high it looks live. Whole-control opacity lets the ground show through, so the result changes with the ground; solid tokens do not. A row shown as full or sold out is content, not a control, so it keeps the text floor.
- **Trade-off.** A legible disabled label invites a click on something that does nothing; a faint one hides what the control would do. A disabled control that stays focusable with `aria-disabled` can explain itself, at the cost of a stop in the Tab order.
- **Clash.** `vault.disabled-look` sets that each control has a disabled state of its own and says why it is unavailable; this record sets how faint that state is. The 3:1 aim is the house's guess between Material and USWDS, below any project rule.

### Edges in forced colours

Records: `vault.forced-colours-edge`, `vault.ring-outline`.

- **Why.** In Windows forced-colours mode the browser drops `box-shadow` and non-url background images and paints every background one system colour, but repaints borders and outlines in system colours. A button drawn by its fill alone becomes bare text; a transparent border or outline becomes visible there and stays invisible elsewhere. Outlines have followed `border-radius` in every engine since Safari 16.4 (March 2023), which removed the old reason for drawing rings with `box-shadow`.
- **Trade-off.** A transparent 1 px border adds a pixel to the box; set it on the resting state so nothing shifts. In a light colour scheme Chromium paints its own #101010 ring over the border, so a dark fill showing through the transparent border hides it, WCAG's failure F78; `background-clip: padding-box` puts the page back under the ring (#424). A transparent outline replaces the browser's ring outright, so it needs a focus style of its own. A shadow ring can stack two colours in one declaration, but needs the transparent outline beside it.
- **Clash.** Forced colours is the visitor's choice; `forced-color-adjust: none` to keep the brand look overrides it, and MDN says not to.

### One focus colour

Record: `vault.focus-colour`.

- **Why.** GOV.UK and Atlassian each reserve a focus colour, so focus never reads as selection or hover; GOV.UK pairs yellow with black so one ring passes on light and dark grounds. Chromium's own ring is already two colours, a dark ring with a thin white outline, drawn for light and dark grounds alike.
- **Trade-off.** A reserved colour is one hue the brand cannot use elsewhere. Material instead takes focus from its secondary palette role; that keeps the palette smaller but lets focus look like other uses of that colour.
- **Clash.** `vault.focus-ring` sets the ring's thickness and per-ground contrast; this record sets only which colour it takes.

### Solid or alpha edges

Record: `vault.edge-alpha`.

- **Why.** An alpha edge takes its contrast from the ground under it, so one token reads the same weight on white, a tint and a photo; Atlassian draws its grouping border so, and Apple ships a translucent separator beside an opaque one. An edge that must reach 3:1 cannot drift with the ground, so Atlassian draws every control and state edge solid.
- **Trade-off.** Material and GOV.UK draw every edge solid, which is simpler and safe on a single ground. An alpha edge must be measured on its worst ground before it may carry a control.
- **Clash.** Where a decorative edge must reach 3:1 because it alone shows a control, it is a control edge (`vault.border-roles`).

### Width and style of a line

Records: `vault.border-width`, `vault.border-style`, `vault.border-image`, `vault.heading-rule`.

- **Why.** Atlassian, Material, Apple and USWDS draw their default border and divider at 1 px (GOV.UK names no 1 px token) and steps to 2 px for a selected or focused state, so colour says what an edge is and width says what state it is in. A colour change between two states that never sit side by side is not held to 3:1, which is why the width step carries it too. Patterned and 3D borders render differently in each browser, and Butterick calls patterned borders "unnecessarily complicated". An image or gradient border ignores `border-radius`, and the layered backgrounds that stand in for it on a rounded box disappear in forced colours. A rule above a heading closes the section before it; one below cuts the heading off from its own text.
- **Trade-off.** GOV.UK draws form edges at 2 px for a bolder public-service look; a project may pick that. Space sets sections apart without any line but needs room.
- **Clash.** `vault.stroke-weight` keeps borders and icon strokes in one band; this record gives the band's sourced values. `vault.heading-space` sets the space around a heading; a rule sits in that space.

### Side accents

Record: `vault.side-accent`.

- **Why.** GOV.UK marks quotes, examples and asides with a wide side border, and Refactoring UI uses one on alerts and the active nav item. GOV.UK found visitors overlook such a block on a busy page, so it never carries what they must not miss.
- **Trade-off.** Used on every card, a side border becomes decoration that marks nothing.
- **Clash.** `vault.ai-look` bans the coloured side border as card decoration; this record names where a side border carries meaning, which is not that default.

### Edges and text over images

Records: `vault.photo-text-fix`, `vault.edge-over-image`, `vault.image-edge`.

- **Why.** A slot that takes any image will one day take its worst, so the fix is chosen for that image, not the one in the mockup; NN/g's panel failed at 30% and passed at 50%. A thin line takes its contrast from whatever pixels the photo puts next to it, so it cannot be relied on; an opaque backing carries its own. An image whose own edge matches its ground bleeds into the page; a faint inset hairline gives it an edge without a frame, as Primer and Polaris do; drawn as an outline it stays in forced colours, where their shadows vanish.
- **Trade-off.** A panel or scrim hides part of the image; a floor fade keeps the image but works only for text at the bottom. A hairline on every image is one more line on the page; it earns its place where images sit on a ground of their own lightness.
- **Clash.** `vault.text-on-photo` and `vault.contrast` set the floor; `vault.photo-text-fix` only picks how to reach it.
