# Surface styling

How a web surface's borders, shadows, corners, dividers, fills, focus rings, scrims and glass follow from what each part does (#117, #154). Decide a part's function first; its styling follows from that, and a styling finding against the function is reported, never dropped. The research behind every line is `docs/research/surface-styling.md` in the design vault, Parts B and E.

A project's rules file wins over every principle here except a floor WCAG or the law sets, and, on behaviour, a principle resting on domain evidence, which it departs from only on evidence of its own ([source precedence](house-principles.md#source-precedence)). A dated principle is reviewed a year after writing, or sooner when a platform ships a new design language or WCAG a new version. A figure marked unsourced is an inference no source states. `docs/research/house-audit-visual.md` in the design vault measures the figures here against shipped design systems.

## Principles

### Two border roles

- **Rule.** Keep two border colours. A **control edge**, at 3:1 or more against what is next to it, for an edge that is a control's only identifier: a text input, select, checkbox, radio, toggle track or empty rating unit. A **decorative edge**, any weak colour, for cards, dividers and labelled buttons.
- **When.** The role follows the part's function, not its look. A button with a text label or a clear icon needs no 3:1 edge; a card needs one only where its edge is the only cue that it is a control. A text input shown by a fill alone needs that fill at 3:1. Disabled controls are exempt. Measure the colour the browser renders: anti-aliasing makes a thin line fainter than its token.
- **Trade-off.** One border token for everything is too strong for a dense list of cards or too weak for inputs.
- **Clash.** The control edge is WCAG 2.2 SC 1.4.11 and beats every brand rule.
- **Era.** Timeless.
- **Source.** W3C Understanding SC 1.4.11 (primary standard); Material 3 `Outline` and `OutlineVariant`, Carbon, GOV.UK `input-border` and `border` (design systems).

### Hover signals

- **Rule.** On hover, change the surface tint, the elevation, or both, whichever the project's rules file picks; where it picks none, the critic faults neither and puts the choice to the founder until the project rules on it (#183 Q4). A small part (chip, checkbox, small button) changes colour, never shadow. A press goes down (smaller shadow, darker, or scaled down), never up.
- **When.** Elevation change is for large surfaces at the rest or raised level, never an overlay, which does not rise further.
- **Trade-off.** One signal is calm and suits a dense tool; two are stronger, but double the motion and can read as noise.
- **Clash.** Atlassian says one signal; Material 3 combines a raise with an 8% colour layer. The vault picks neither; the project does.
- **Era.** Dated, current; review by 2027-10-14.
- **Source.** Atlassian Elevation, Polaris depth, Material 3 `ElevatedCardTokens` and `StateTokens` (design systems).

### Depth only for what floats or acts

- **Rule.** A shadow means "above other content" or "you can act on this". Never give one to a static part. Group static content by space first, then a fill step, then a border; a shadow never groups.
- **When.** Anything floating over content takes a shadow, since nothing else says "above": a menu, popover, dialog, toast, tooltip, nav panel, or a sticky bar over scrolling content. In a dense list of equal clickable rows, keep the rows on one layer and show clickability on hover and in the row's own controls. One card that must look pressable among static content may take a small rest shadow.
- **Levels.** Name each level by its role (rest, hover, overlay), pair each with its surface colour, and keep one level per role the page uses: a page with no drag and no nested overlays uses about three (Atlassian ships three shadows). A shadow with no named level is a defect. A shadow has an offset and a soft blur; a zero-offset coloured glow is decoration, and a hard offset shadow belongs only to a neobrutalist brand.
- **Trade-off.** A rest shadow on every clickable card makes the cue strong, then worthless once everything has it.
- **Clash.** Polaris gives a clickable card depth at rest; Atlassian only a movable one. The project's brand decides: a tactile brand may take Polaris's, a dense working tool takes Atlassian's.
- **Era.** Timeless as affordance. Shadow on every card (Material 1–2, 2014–2020) is dated.
- **Source.** Polaris, Atlassian, Material 3 tokens (design systems); impeccable craft-floor (weak).

### Elevation on a dark ground

- **Rule.** On a dark ground, show a raised or overlay surface with a lighter surface tone, adding a light low-alpha edge where needed. Never a heavier shadow.
- **When.** Any dark ground or dark mode: a shadow there has almost no visible effect.
- **Trade-off.** One more surface token per level on dark.
- **Clash.** Gives way to the project's dark-ground tokens.
- **Era.** Dated, current since dark mode became a system setting (2018–2019); review by 2027-10-14.
- **Source.** Atlassian, Apple HIG Dark Mode, Material 3 surface containers (design systems).

### Radius nesting

- **Rule.** An inner shape inside an outer one with even padding takes inner radius = max(outer radius − padding, a small fallback). A photo flush in a card shares the card's radius on the corners it touches, or the card clips it.
- **When.** Any nested shape: a photo, chip or button in a card. Where the padding exceeds the outer radius, the fallback applies.
- **Trade-off.** One fixed token on parent and child is simpler, but the inner corner looks flared when the padding is small.
- **Clash.** Gives way to a project radius token only where the project's rules file names the nested case.
- **Era.** Timeless geometry; Apple named it a system rule in June 2025.
- **Source.** Apple WWDC25 session 356 and SwiftUI `concentric(minimum:)`, which is max(R − p, fallback) with its `minimum` as the fallback (design system).

### Dividers against space and fill

- **Rule.** Where padding already separates the groups, use space and no divider. Where room is short (a dense list, a phone width), use a divider in the decorative edge colour: full width between unrelated sections, inset between related items. Inside a card, separate a secondary area with a fill band or one divider, never both.
- **When.** A divider only groups, so it needs no 3:1.
- **Trade-off.** Space needs room; a line costs a pixel but adds noise in every gap.
- **Clash.** A border or divider that groups differently from the spacing makes the grouping ambiguous: fix the spacing first, never add a line to override it.
- **Era.** Timeless.
- **Source.** Material dividers, GOV.UK, Apple HIG Layout, Polaris (design systems); Palmer 1992 and Montoro and Luna 2015 on common region against proximity (research).

### Focus rings per ground, clear of sticky bars

- **Rule.** Give every focusable part a visible ring at 3:1 against each ground it can sit on: a two-colour ring, or one ring colour per ground. A text input gets an outside 2 px ring, or a border at least 2 px thick and 3:1 different from its rest state; never only a recoloured thin border. A ring drawn with `box-shadow` keeps `outline: <width> solid transparent`, so forced-colours mode still shows it. Under a sticky header or bottom bar, set `scroll-padding` on the scroll container to the bar's height, so a focused part is never hidden behind it.
- **When.** A field takes a ring; a row in a list takes a fill highlight plus a non-colour cue.
- **Trade-off.** A thick two-colour ring is loud for a quiet brand; a colour-swap-only ring is quiet and hard to see.
- **Clash.** WCAG 2.2 SCs 2.4.7, 1.4.11 and 2.4.11 are floors no brand rule lowers. The input's 2 px and 3:1 figures are SC 2.4.13, level AAA: stricter than the floor, so a project's rules file may relax them.
- **Era.** Timeless need; the numbers are WCAG 2.2 (October 2023).
- **Source.** W3C Understanding SCs 2.4.11 and 2.4.13 (AAA) (primary standard); GOV.UK focus states, Apple HIG Focus and selection (design systems).

### One scrim token

- **Rule.** One scrim colour and opacity for the product, never one per component: neutral black or the brand's dark, at about 32–70%, or a light grey scrim for a light, low-drama brand.
- **When.** A scrim dims what is behind a modal surface. A busy or bright backdrop needs the darker end; a modal with a strong edge or shadow, the lighter.
- **Trade-off.** A dark scrim focuses the modal and hides the context; a light one keeps it.
- **Clash.** Text on a photo is the text-contrast floor's job, not the scrim token's: measure it against the worst pixel under the text, or use a panel.
- **Era.** Dated, current; review by 2027-10-14.
- **Source.** Material 3 `ScrimTokens` (0.32), Atlassian `blanket` (0.46), Carbon `overlay` (0.6), Polaris `backdrop-bg` (0.71), Primer `overlay-backdrop` (a light grey at 0.4), Apple HIG Materials (design systems); W3C Understanding SC 1.4.3 for text on photos (primary standard).

### Glass only on a floating functional layer

- **Rule.** Translucency and blur only on a layer that floats above content and holds controls or navigation: a sticky bar or a nav over scrolling content. Use strong blur, keep text at its contrast floor against the worst backdrop, and give a solid fallback under `prefers-reduced-transparency` and `prefers-contrast`. Never on content cards.
- **When.** Simple backdrops suit it; busy ones need more blur or a solid layer. Blur costs GPU on low-end phones.
- **Trade-off.** Glass keeps context and looks current; it risks contrast and performance.
- **Clash.** impeccable's "decorative glass" default covers glass on content; glass on a floating functional layer does not breach it.
- **Era.** Glassmorphism cards (web, 2020–2022) are dated. Glass on a functional layer is dated, current on Apple platforms since Liquid Glass (June 2025) and not yet a web convention; review by 2027-10-14.
- **Source.** NN/g, Brown 2024 (expert); Apple HIG Materials (design system); impeccable (weak).

## Interactions: given X, do Z

1. **Border and shadow.** A resting static card takes a border or a fill step, never a shadow. A floating element takes a shadow; any border on it is the decorative role. Never a hairline border with a wide soft shadow on one resting element.
2. **Border and fill.** Where a fill step already separates the card, drop the border or keep it decorative; never a strong border with a strong fill. Where the fill step is under about 1.1:1 (Carbon's tile, 1.10 on white, is the lowest fill-only step a major system ships), keep the border, so the edge survives a poor screen.
3. **Border and space.** Where the spacing already makes the groups, a border adds little. Where they disagree, fix the spacing first.
4. **Divider and card.** Cards with their own edges take no dividers between them. Inside a card, one separator kind: a divider or a fill band.
5. **Radius nesting.** An inner element with padding p inside radius R takes max(R − p, fallback). A flush photo shares the outer radius on the corners it touches. Capsules inside a capsule stay concentric on their own.
6. **Radius, density and pointer.** Dense desktop rows take rounded rectangles. Capsules go to touch layouts, tags, status chips and one standout action.
7. **Radius and meaning.** A brand radius change keeps the checkbox square-ish and the radio round, so neither reads as the other.
8. **Tint and state.** A pale tint for "selected" needs a check mark, a weight change or a 3:1 edge beside it. A pale tint for hover alone is enough.
9. **Focus, ground and border.** More than one ground: a two-colour ring or one ring colour per ground. An input with a border: an outside ring or a thicker border on focus, never only a recoloured thin border. A `box-shadow` ring keeps a transparent outline for forced-colours mode.
10. **Focus and sticky bars.** A sticky header or bottom bar: `scroll-padding` its height, so focus is never hidden under it.
11. **Stroke weights.** Match an icon's weight to the text beside it. Keep borders and icon strokes in one line-weight band, all thinner than the focus ring, the one deliberate step above them (unsourced: no source ties stroke to border). A light icon on a dark ground takes a lower grade (lighter stroke).
12. **Scrim, photo and text.** Text over a varied photo is measured against the worst pixel under it, or sits on a panel. A modal over content uses the one scrim token.
13. **Glass and layer.** Glass only on a floating functional layer, with strong blur and a solid fallback; never on a content card.
14. **Dark ground and elevation.** On a dark ground, raise by a lighter surface, never a stronger shadow.
