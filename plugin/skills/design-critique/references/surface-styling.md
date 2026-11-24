# Surface styling

Why a web surface's borders, shadows, corners, dividers, fills, focus rings, scrims and glass follow from what each part does (#117, #154). Decide a part's function first; its styling follows from that, and a styling finding against the function is reported, never dropped. The research behind every line is `docs/research/surface-styling.md` in the design vault, Parts B and E, and `docs/research/house-audit-visual.md` measures the figures against shipped design systems.

A project's rules file wins over every record here except a floor WCAG or the law sets, and, on behaviour, a record resting on domain evidence, which it departs from only on evidence of its own ([source precedence](house-principles.md#source-precedence)). A dated record is reviewed a year after writing, or sooner when a platform ships a new design language or WCAG a new version.

## Principles

### Two border roles

Records: `vault.border-roles`, `vault.control-edges`.

- **Why.** WCAG 2.2 SC 1.4.11 asks 3:1 only of an edge a visitor needs to find the control; a button with a text label or a clear icon is found by its label, and a card needs a strong edge only where that edge is its only cue that it acts. Disabled controls are exempt. Anti-aliasing makes a thin line fainter than its token.
- **Trade-off.** One border token for everything is too strong for a dense list of cards or too weak for inputs.
- **Clash.** The control edge is WCAG's and beats every brand rule.

### Hover signals

Records: `vault.hover-signal`, `vault.press-state`, `vault.control-states`.

- **Why.** An overlay is already at the top level, so it cannot rise further. A shadow on a small part is too small to read as a raise. A ripple is one design system's pressed-state value, and a value comes from the project ([dependency order](house-principles.md#dependency-order), step 4).
- **Trade-off.** One signal is calm and suits a dense tool; two are stronger, but double the motion and can read as noise.
- **Clash.** Atlassian says one signal; Material 3 combines a raise with an 8% colour layer. The vault picks neither; the project does (#183 Q4).

### Depth only for what floats or acts

Records: `vault.depth`, `vault.shadow-levels`, `vault.border-shadow`, `vault.grouping`, `vault.surface-shadow`.

- **Why.** A shadow means "above other content" or "you can act on this", and nothing else says "above". Atlassian ships three shadows, enough for a page with no drag and no nested overlays.
- **Trade-off.** A rest shadow on every clickable card makes the cue strong, then worthless once everything has it.
- **Clash.** Polaris gives a clickable card depth at rest; Atlassian only a movable one. The project's brand decides: a tactile brand may take Polaris's, a dense working tool takes Atlassian's. Shadow on every card (Material 1–2, 2014–2020) is dated.

### Elevation on a dark ground

Records: `vault.dark-elevation`, `vault.dark-raise`.

- **Why.** A shadow on a dark ground has almost no visible effect.
- **Trade-off.** One more surface token per level on dark.
- **Clash.** For a dialog, menu, list box or popover, `vault.dark-raise` sets the lighter surface.

### Radius nesting

Record: `vault.radius-nesting`.

- **Why.** With even padding, the inner corner that keeps the gap even is the outer radius less the padding; a padding larger than the radius needs the fallback.
- **Trade-off.** One fixed token on parent and child is simpler, but the inner corner looks flared when the padding is small.

### Dividers against space and fill

Records: `vault.dividers`, `vault.grouping`.

- **Why.** A divider only groups, so it needs no 3:1.
- **Trade-off.** Space needs room; a line costs a pixel but adds noise in every gap.
- **Clash.** A border or divider that groups differently from the spacing makes the grouping ambiguous, so the spacing is fixed first rather than a line added to override it.

### Focus rings per ground, clear of sticky bars

Records: `vault.focus`, `vault.focus-ring`, `vault.scroll-padding`.

- **Why.** A ring that clears one ground can vanish on another. Forced-colours mode drops `box-shadow` but draws an outline, so a transparent outline keeps the ring there. A transparent border over a dark fill hides Chromium's own ring unless the fill is clipped to the padding box (`edges-and-contrast.md#edges-in-forced-colours`, #424).
- **Trade-off.** A thick two-colour ring is loud for a quiet brand; a colour-swap-only ring is quiet and hard to see.
- **Clash.** WCAG 2.2 SCs 2.4.7, 1.4.11 and 2.4.11 are floors no brand rule lowers. The input's 2 px and 3:1 figures are SC 2.4.13, level AAA: stricter than the floor, so a project's rules file may relax them.

### One scrim token

Records: `vault.scrim`, `vault.text-on-photo`.

- **Why.** A scrim dims what is behind a modal surface; one token keeps every modal reading as the same kind of layer. The web systems that ship a scrim token dim the page and do not blur or scale it; a blur is glass, kept for a layer that holds controls.
- **Trade-off.** A dark scrim focuses the modal and hides the context; a light one keeps it.
- **Clash.** Text on a photo is the text-contrast floor's job, not the scrim token's.

### Glass only on a floating functional layer

Record: `vault.glass`.

- **Why.** Glass keeps the content behind a bar in view. Simple backdrops suit it; busy ones need more blur or a solid layer. Blur costs GPU on low-end phones.
- **Trade-off.** Glass looks current; it risks contrast and performance.
- **Clash.** impeccable's "decorative glass" default covers glass on content; glass on a floating functional layer does not breach it. Glassmorphism cards (web, 2020–2022) are dated; glass on a functional layer is current on Apple platforms since Liquid Glass (June 2025) and not yet a web convention.

### Buttons on a dark ground

Record: `vault.action-on-dark`.

- **Why.** The dark-on-light button a page uses elsewhere sinks into a dark ground, so GOV.UK and USWDS each ship a light, inverse variant for it. On a ground in the brand colour, a button in that colour disappears (`docs/research/function-fit.md` B3.1).
- **Trade-off.** An inverse button is one more variant to keep in step, and on a light-on-dark section it can outshine the heading.
- **Clash.** None known.

### Tag fills

Record: `vault.tag-fill`.

- **Why.** A dark fill with white text is a button's look, and GOV.UK's research found visitors pressing tags so drawn; a pale tint with dark text reads as a label.
- **Trade-off.** A pale tint is quieter, so a status that matters is easier to miss.
- **Clash.** `vault.carry-status` sets each status's colour; this record sets only how strongly the tag is filled.

### Inverse surfaces for passing messages

Records: `vault.inverse-surface`, `vault.inverse-surface-look`.

- **Why.** A message that floats briefly over the page must stand apart from every surface below it, whatever that surface is; the theme's opposite neutral does that on any page.
- **Trade-off.** A dark toast on a light page is loud for a routine confirmation; a light toast with a coloured edge is quieter but can merge with cards.
- **Clash.** None known.

### Seams between joined fills

Record: `vault.joined-fills`.

- **Why.** Where an edge falls between device pixels, the browser blends it with what lies behind, so two fills that meet there show a faint line. At 125–175% display scale, common on Windows laptops, even whole CSS-pixel widths can land between device pixels; a colour painted once on the container has no edge to blend (`docs/research/layout-data-defaults.md`).
- **Trade-off.** A container fill means the parts cannot each keep their own colour; parts that must, take whole-pixel widths and accept a seam at fractional scales.
- **Clash.** None known.

### Disabled controls

Record: `vault.disabled-look`.

- **Why.** A visitor must tell at a glance that a control cannot be used, and know what to do about it; a disabled look that resembles a lower rung of the ladder reads as a live, quieter button.
- **Trade-off.** Disabled controls are exempt from contrast, so they can become unreadable; keeping them readable makes them look more available.
- **Clash.** None known.

### One size in a button group

Record: `vault.button-group-size`.

- **Why.** Buttons of one size read as one set of choices; a bigger one beside a smaller one looks like a mistake (Apple HIG, Carbon).
- **Trade-off.** A single key action standing alone, such as a hero's main button, may be larger; the rule binds only buttons offered together. USWDS allows mixed sizes in a group.
- **Clash.** `vault.primary-action` and `vault.carry-act` decide which button is filled.

### Icons on buttons

Records: `vault.button-icon`, `vault.button-icon-side`.

- **Why.** Most buttons need no icon (Atlassian); one with a known meaning helps a visitor find the action faster. Design systems differ on the side (Material before the label, Carbon after), so what matters is one side across a site, with a forward arrow after the label, where reading goes.
- **Trade-off.** An icon on every button adds noise and weakens the ones that help.
- **Clash.** `vault.icon-use` decides whether the icon belongs at all.

### Edges that survive forced colours

Records: `vault.forced-colour-edges`, `vault.shadow-meaning`.

- **Why.** Windows high-contrast mode, and any forced-colours mode, removes every shadow but keeps borders and outlines in the user's colours (MDN). An edge drawn only as a shadow disappears there, and so does the meaning it carried.
- **Trade-off.** A shadow takes no layout space; a real border does, so a ring that thickens on hover needs its space set aside from the start.
- **Clash.** `vault.focus-ring` already backs a focus ring this way; this record extends it to resting edges and levels.

### A radius scale by element size

Record: `vault.radius-scale`.

- **Why.** One scale ties each corner to what the part is, so like parts match and a modal reads larger than a card. Atlassian and Material 3 both step radius up with element size.
- **Trade-off.** Five steps is a lot of tokens to keep in step. One radius everywhere is simpler but loses the size relation (House DNA bans "one rounding applied to everything by habit").
- **Clash.** `vault.radius-nesting` sets an inner shape's radius from its parent, and `vault.radius-meaning` keeps checkboxes square-ish and radios round; both win over the scale. The values are the project's.

### One shape family

Record: `vault.shape-family`.

- **Why.** Rounder shapes read softer and sharper ones harder (Bar and Neta 2006), so the rounding carries the brand's tone. Mixed corners at random read as unbalanced (Apple WWDC25).
- **Trade-off.** One fixed family is calm but can feel flat. Material 3 Expressive (2025) is said to invite tension between shapes, but its page could not be read; a brief that wants that tension says so in its rules file.
- **Clash.** The UI transfer from the curvature studies is an inference, not a finding; the brief's tone wins.

### One light source

Record: `vault.shadow-form`.

- **Why.** Shadows from one light, growing softer and fainter as a part rises, read as one physical scene; grey-black over a coloured ground looks dirty because it desaturates it (Comeau). Polaris finds inset surface shadows noisy.
- **Trade-off.** Hue-matched shadows need one value per ground; layered shadows cost rendering on cheap phones.
- **Clash.** `vault.shadow-levels` names the levels; this record only shapes each one. A pressed control may sink, by `vault.press-state`.

### Named surface levels

Record: `vault.surface-layers`.

- **Why.** A few named tones, each nesting one step up, show what sits inside what without a line or a shadow (Carbon, Material 3). A sunken well is the one level below the ground: Atlassian keeps it to the default level, as a backdrop for grouped content such as a board's columns, because a well inside a raised or overlay surface reads as a hole in it.
- **Trade-off.** A tone step is quiet and can vanish on a poor screen; below about 1.1:1 `vault.border-fill` keeps a border. A well adds a tone that must stay distinct in both themes; Atlassian's darkens in light and dark alike, so it cannot be an alpha fill.
- **Clash.** On a dark ground `vault.dark-elevation` decides the tones.

### One card type per set

Records: `vault.card-type`, `vault.card-treatment`.

- **Why.** Material 3 makes outline, fill and shadow equal in function, so the choice is style. Within one set, a card that looks different is read as a different kind (NN/g on similarity).
- **Trade-off.** One treatment across a long list can feel flat; emphasis then comes from content and size, not a second treatment.
- **Clash.** `vault.depth` decides whether a card may have a shadow at all, and `vault.carry-contain` keeps a tappable card's look apart from a static one.

### Dimming under clear glass

Record: `vault.glass-dimming`.

- **Why.** Clear glass shows the media under it, so over a bright photo its contents lose contrast; Apple's answer is a dark layer behind the glass.
- **Trade-off.** The layer darkens the media the clear glass was chosen to show.
- **Clash.** `vault.glass` decides whether glass belongs at all, and `vault.contrast` holds the text floor whatever the dimming.

### Outline and filled icons

Records: `vault.icon-fill`, `vault.current-icon`.

- **Why.** Outline icons sit lightly beside text; a filled one carries more weight, so filling the current tab marks it without colour alone (Apple SF Symbols, Material Symbols).
- **Trade-off.** Filling too many icons spends that weight (Atlassian). Some craft sites fill icons on dark mode to hold their weight there (Devouring Details); a project may choose that.
- **Clash.** `vault.carry-select` still asks for more than a tint on a selected item; the fill is one such cue.
- **Why no script answers it.** A script tells a current item's filled icon from its set's outlines by their ink, and `vault.current-icon` does; elsewhere outline against filled does not show in the markup, since an outline icon is often drawn as filled paths, and which places and statuses earn a filled icon is judgement.

### Icon stroke across sizes

Record: `vault.icon-optical-size`.

- **Why.** An SVG stroke scales with its icon by default, so a 48px icon of a 24px design draws a 4px line; optical size keeps the line looking the same (Material Symbols, Lucide).
- **Trade-off.** A non-scaling stroke at very small sizes can look heavy; a set with an optical-size axis does it better than one fixed stroke.
- **Clash.** `vault.stroke-weight` matches the stroke to the text beside it; this record keeps it there across sizes.

### Colour pairs

Records: `vault.colour-pair`, `vault.image-fallback-colour`.

- **Why.** A visitor can set their own default text and background colours. A page that sets only one of the pair can put its dark text on their dark background. A background image that fails to load leaves its text on whatever lies beneath, so a colour under the image keeps the text readable (WCAG 2.2 failure F24; MDN).
- **Trade-off.** None worth naming.
- **Clash.** WCAG's, so it beats a brand palette.

### Browser-drawn parts follow the scheme

Record: `vault.color-scheme`.

- **Why.** The browser draws the page canvas, scrollbars, native form controls and other parts of its own UI itself (MDN). Without `color-scheme` they stay light on a dark theme, and the canvas can flash white before the CSS loads.
- **Trade-off.** Native controls then take the browser's own dark style, which the page does not choose.
- **Clash.** `vault.theme` decides which schemes the page has; this record only declares them.

### Caption colours

Records: `vault.caption-colours`, `vault.caption-settings`.

- **Why.** White on 80% black is the WebVTT default. Viewers who need other colours set them in their player, a choice US rules require of video apparatus (47 CFR 79.103), so the page leaves those settings working.
- **Trade-off.** Brand-coloured captions lose to the default on legibility over a busy frame.
- **Clash.** None known.

### hr for a thematic break

Records: `vault.hr-break`, `vault.typed-rules`.

- **Why.** An `hr` means a thematic break in the HTML standard, so a decorative line drawn with it marks a break in the content that is not there. A line typed from dashes or underscores is text: it wraps or overflows at a narrow width, and Butterick rules it out.
- **Trade-off.** None worth naming.
- **Clash.** `vault.dividers` decides whether a line is drawn at all; this record only says how.

## Interactions

Where two of the treatments above meet, the record that settles it:

1. Border and shadow: `vault.border-shadow`. A hairline says the card sits on the page and a wide shadow that it floats above it; both at once say neither.
2. Border and fill: `vault.border-fill`. Below Carbon's tile step a fill alone does not survive a poor screen.
3. Border and space, divider and card: `vault.grouping`, `vault.dividers`.
4. Radius and nesting: `vault.radius-nesting`.
5. Radius, density and pointer: `vault.radius-density`. Capsules bring focus to touch layouts; in dense desktop rows they waste space (Apple WWDC25 session 356). The capsule for tags is Apple's convention: Atlassian's Radius gives tags 4 px and Material's filter chip a small rounded rectangle, so a project on either system may set tags that way.
6. Radius and meaning: `vault.radius-meaning`. A square box means many choices and a circle one; a brand radius must not erase that.
7. Tint and state: `vault.carry-select`, with the hover exemption in `vault.colour-look`. Hover is feedback on the visitor's own pointer; a selected state is a fact to read later.
8. Focus, ground, border and sticky bars: `vault.focus-ring`, `vault.scroll-padding`.
9. Stroke weights: `vault.stroke-weight`. No source ties stroke to border, so the band is the house's inference.
10. Scrim, photo and text: `vault.text-on-photo`, `vault.scrim`.
11. Glass and layer: `vault.glass`.
12. Dark ground and elevation: `vault.dark-elevation`.
13. Shape family and radius scale: `vault.radius-scale`, which yields to `vault.shape-family`.
