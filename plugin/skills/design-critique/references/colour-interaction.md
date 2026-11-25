# Colour interaction

Why a colour is judged where it will sit, why two saturated hues of near-equal lightness are kept apart, and why parts near a photograph take their colour with it in view (#281). The research behind this file's records is `docs/research/brand-palette.md` Part 1 in the design vault, and the source checks `docs/research/control-feedback-defaults.md`.

Where a project's rules file and a record here disagree, [source precedence](house-principles.md#source-precedence) decides. A dated record is reviewed a year after writing, or sooner when a platform ships a new design language.

## Principles

### A colour is judged in place

Record: `vault.colour-in-place`.

- **Why.** Two colours that touch look as different as possible, each pushed toward the complement of its neighbour, a dark one darker beside a light one (Chevreul's simultaneous contrast). A colour approved as a swatch on white is not the colour a visitor sees on a cream ground beside coral.
- **Clash.** None known. A token that sits on several grounds is checked on each, as `vault.contrast` checks text.

### Vibrating edges

Record: `vault.vibrating-edge`.

- **Why.** Two hues far apart at near-equal lightness make their shared edge shimmer or seem to float at another depth; red against blue is the strongest case, because the eye focuses the two at different depths. A lightness gap between them reduces it.
- **Trade-off.** Separating a saturated figure from a contrasting saturated ground in lightness spends some of its pull.
- **Clash.** Where the figure is text or a control's edge, `vault.contrast` sets the floor. No source says how large a lightness gap stops vibration, so a pair under 3:1 is judged rendered rather than failed.

### Colour from imagery

Record: `vault.imagery-colour`.

- **Why.** A palette fixed on swatches and a photograph chosen after it rarely agree; the founder found each hard to choose without the other (`docs/research/past-design-rejections.md` B11). Apple changes nearby colours as artwork changes, and Material derives a whole scheme from an image.
- **Trade-off.** A palette drawn from one photograph is tied to it; a new photograph can call for new accents.
- **Clash.** A client's fixed logo colours (`vault.logo-anchors`) and the palette's roles (`vault.palette-roles`) win: an accent from the image fills a role and never replaces a fixed colour.
