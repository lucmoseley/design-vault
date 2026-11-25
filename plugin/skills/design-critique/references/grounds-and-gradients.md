# Grounds and gradients

Why a section, region, bar or footer takes its own background, how far apart neighbouring grounds sit, and when a gradient, a wash or a frame does a job (#284). The research behind every line is on design-vault#284's research comment.

Where a project's rules file and a record here disagree, [source precedence](house-principles.md#source-precedence) decides. A dated record is reviewed a year after writing, or sooner when CSS changes how gradients blend or a design system cited here changes its surface model.

## Principles

### The step between neighbouring grounds

Record: `vault.ground-step`.

The levels themselves are `vault.surface-layers`'s, in [named surface levels](surface-styling.md#named-surface-levels).

- **Why.** The systems that publish their surface tones keep the steps small. Material's light containers span tones 100 to 90, about 1.29:1 in all. Carbon's first layer, #f4f4f4 on white, is 1.10:1, and its next layer returns to white, so the set alternates rather than darkening. A step that small groups without drawing a line. The house asks more per step than either: the founder's 3 ΔE00 for large greys that meet (`vault.colour-distance`), about 1.14:1 near white, against Carbon's 2.2 ΔE00 and Material's 1.2. Two such steps reach the 1.3:1 span, so a third level alternates.
- **Trade-off.** A small step can vanish on a poor screen or in sunlight, which is where `vault.border-fill` keeps a border. A bigger span makes the page look striped.
- **Clash.** Where the step is the only sign of a control or a state, `vault.control-edges`' 3:1 applies. The 1.3:1 span is read off these systems, not a measured threshold.

### Regions in an app

Records: `vault.region-ground`, `vault.region-fill`.

- **Why.** Polaris lets several backgrounds share a view "only if they exist side by side", as the admin and its side navigation do. In Material, the navigation rail on a wide screen sits on the same surface as the content, and the bottom bar that replaces it on a phone takes a container tone. A drawer takes a tone of its own. So a region's ground follows the component it is, not the screen width. impeccable gives sidebars, toolbars and panels "a second neutral layer". Polaris bans bright or contrasting container fills in working areas because they pull the eye from the work.
- **Trade-off.** A region on the content's own ground behind a divider looks calmer but reads less as a separate place. A second neutral layer marks the shell but adds one more tone to keep in step across themes.
- **Clash.** A site header that carries the brand colour is `vault.bar-ground`'s to decide, and this record gives way to it.

### Bars

Record: `vault.bar-ground`.

- **Why.** GOV.UK puts its site-wide header on a strong blue and the service's own bar under it on a light blue, the most general bar on top. Two bars of the same strength would not show which belongs to whom. USWDS asks a banner on every page not to "draw excessive attention". impeccable's working-product mode lets the shell carry a committed colour, a coloured rail or header, so one bar may be loud.
- **Trade-off.** A brand-coloured header spends the page's one strong ground at its top, so a hero below it may need a quieter ground.
- **Clash.** How much novelty the bar carries at all is `vault.brand-layer`'s.

### Section grounds

Record: `vault.section-ground`.

- **Why.** A band of colour is a common region (Palmer 1992), so it groups what sits inside it and splits it from what is outside. That makes it a statement that the function has changed. GOV.UK keeps its strong full-width panel for confirmation and interruption pages and "never" for anything else. Polaris keeps working areas free of bright fills. Butterick lists "layouts built with large blocks of color" among the '90s habits. NN/g found that a full-width line or a large gap can read as the end of the page. A band edge is the same kind of break (an inference), so a sliver of the next section should show past it.
- **Trade-off.** Alternating bands make a long marketing page easy to chunk, but they add no information once every section has one, and each edge risks a false floor.
- **Clash.** How much of the page is in colour at all is `vault.tone-colour-share`'s. A project's own zone rule, such as Manta's loud marketing and calm working zones, sits in its rules file and wins.

### The last footer block

Record: `vault.footer-ground`.

- **Why.** USWDS darkens the identifier, the block naming the site's owner and its required links, past the footer's own ground ("grade 80 or higher, or black"), anchoring the page's end.
- **Trade-off.** A dark last block adds one more ground. A short footer with no separate block needs none.
- **Clash.** Which logo version a ground takes is `vault.logo-ground`'s.

### Section headers in long lists

Record: `vault.list-header-fill`.

- **Why.** Rauno found a border-heavy list hard to split into its sections. A grey fill on each section header made it "so much easier to scan and jump between sections". Polaris gives a grouped table's subheader rows the header's own look. The fill makes each header a region that starts its group (common region), without a border around each group.
- **Trade-off.** A filled header is one more tone in a dense view. A short list needs only space.

### The section a link reached

Record: `vault.target-highlight`.

- **Why.** web.dev and MDN both give `:target` for this job: showing which part of a page a link, a table of contents or a skip link reached. On a long page the jump can leave the visitor unsure where they are.
- **Trade-off.** A strong highlight stays while the fragment is in the address, so a quiet one is safer.

### Prices

Record: `vault.price-ground`.

- **Why.** The one source found, a CXL summary, says studies found prices on light grounds look dearer, but it names no study. That is too weak to set a ground by. The house's high-stakes line already keeps a price plain: type, colour role and voice only (`vault.brand-layer`).
- **Trade-off.** A dark price band can still be right as a section ground. It is then `vault.section-ground`'s call, made for the section's function, not the price.

### A card tinted from its image

Record: `vault.card-image-tint`.

- **Why.** Material builds a colour scheme from content, such as "album artwork, a brand logo, or a video tile". It takes one source colour from the image and maps its tones to roles, so text keeps its contrast. On a set of media or place cards, the tint ties each card to its picture.
- **Trade-off.** A grid of differently tinted cards is busier than one tone. Polaris bans bright container fills, so the tint stays at low chroma. A tint can also read as a category or status it does not mean. Keeping it off such sets is the house's call, not a source's.

### When a gradient has a function

Records: `vault.gradient-function`, `vault.gradient-kind`, `vault.gradient-place`.

- **Why.** A gradient does a job when it is a scrim under text on a photo (NN/g's fade), a light cue on a surface (Krehel's "depth lighting"), the brand's colour where the page may go committed (`vault.tone-colour-share`), an ambient pattern on a promotion (Atlassian), or a chart or ring (conic). Each kind suits one of these jobs. impeccable's detector flags the radial halo and spotlight glow behind a hero, and its quieter pass removes any gradient "that don't serve purpose".
- **Clash.** A gradient behind a working region is `vault.decoration-place`'s to refuse. Where one is earned back, `vault.ai-look` decides.

### Gradient text

Record: `vault.gradient-text`.

- **Why.** impeccable bans gradient text: emphasis comes from weight or size. It is also fragile. Forced colours removes a gradient `background-image`, so text clipped to one may vanish. A letter crossing a gradient must clear the floor at the stop behind it (G18), so the weakest stop decides.
- **Trade-off.** A single display word in a gradient can be the brand's signature. The record allows it where the brief earns it, under the two checks.

### How a gradient blends

Records: `vault.gradient-space`, `vault.gradient-stops`.

- **Why.** CSS still blends hex, `rgb()` and `hsl()` stops in gamma sRGB unless a space is named. That gives a too-dark, greyish middle (the spec's own examples; Comeau's "gray dead zone"). Oklab removes the muddy middle and the purple cast toward blue. Oklch keeps the middle's chroma where hues sit far apart, but it can pass through colours no stop names (Krehel). The `in` syntax has been Baseline since June 2024, so a plain declaration first covers older browsers. A colour hint or eased stops moves where the blend happens, without new colours.
- **Trade-off.** Oklch's curved path can leave the sRGB gamut, and the browser then maps it back, so check it on screen. Precomputed stops (Comeau's fallback) match old browsers but are longer to write.

### Washes over a background image

Record: `vault.image-wash`.

- **Why.** impeccable flags a wash at 0.9 alpha or more over an image as a buried raster: the page shows the wash, not the image. Text on the image sets the floor. The worst image the slot can hold must clear the text's contrast (F83). Where the floor needs 0.9 or more, the text moves off the image (`vault.photo-text-fix`).
- **Trade-off.** A strong wash makes any photo safe but flattens it. A light one keeps the photo but limits which photos the slot can take.
- **Clash.** The text floor itself is `vault.contrast`'s. The 0.9 ceiling is impeccable's figure alone.

### Page frames and grid marks

Record: `vault.grid-ornament`.

- **Why.** Vercel's frame earns its place: it is the brand's metaphor, "Having a consistent grid position across all pages" lets a visitor sees what changes, and its crosshairs mark chosen points. impeccable's calibration names "broadsheet-editorial hairlines" as a look generated interfaces cluster on, and its detector flags a grid-line background.
- **Trade-off.** A frame held on every page constrains every layout to its columns.
- **Clash.** Whether the frame is the site's one signature move is `vault.brand-layer`'s, and `vault.ai-look` holds the dated ban.
