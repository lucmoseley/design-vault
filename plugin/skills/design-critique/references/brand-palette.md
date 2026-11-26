# Brand palette and logo

Why a palette is built around a client's logo as its records say, how far apart two colours must sit, and which grounds a logo may take (#143, #175, #272). The research behind every line is in the design vault: `docs/research/brand-palette.md`, and `docs/research/de00-thresholds.md` and `de00-greys.md` for the numbers.

Where a project's rules file and a record here disagree, [source precedence](house-principles.md#source-precedence) decides. A dated record is reviewed a year after writing, or sooner when a platform ships a new design language or WCAG a new version.

`python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-project/scripts/palette.py` measures the numbers the records set: ΔE00 between colours, the logo's lightness, and its grounds at 3:1.

## Principles

### A palette is roles

Record: `vault.palette-roles`.

- **Why.** Harmony rises as hues sit closer, and a figure is liked more the more its hue stands apart (Schloss and Palmer 2011), so most hues sit near each other and one stands out for one job. HSL's lightness and hue are not what the eye sees.
- **Trade-off.** Few hues with one job each read calm and clear, but can read plain. Energy then comes from lightness, scale, type and photographs, not from another hue.
- **Clash.** WCAG contrast beats any role choice. A client's fixed logo colours beat the house's harmony: they are [anchors](#fixed-logo-colours-are-anchors).

### Colour never carries meaning alone

Record: `vault.colour-look`.

- **Why.** A visitor who cannot tell two colours apart loses any meaning only colour carries (WCAG 2.2 SC 1.4.1): an error, a required field, a selected option, a chart series.
- **Trade-off.** The second cue costs room and ink: a dense chart grows direct labels, markers or dash patterns, a dense table an icon per state.
- **Clash.** SC 1.4.1 beats any brand or density preference. A hover tint or a press's darker fill is feedback on the visitor's own pointer, not a meaning to read, so neither needs a second cue; a selected tint does.

### The same colour or clearly different

Record: `vault.colour-distance`.

- **Why.** Under 2 is one just-noticeable difference, so two such colours are one colour with two names. Between 2 and the line, a pair reads as a mistake rather than a choice. Large grey surfaces near the ground that share an edge are judged side by side, so they part at a smaller gap than small marks, which need more. ΔEOK divided by 100 ranks pairs differently from ΔE00. Two colours that never share a view may sit closer, and a ramp's own steps are judged by contrast instead.
- **Trade-off.** Keeping every pair far apart costs richness: fewer colours, or colours further from the brand's hue.
- **Clash.** Against "make distinctions as subtle as possible" (Tufte), the job decides: a difference of identity or meaning takes this record, a difference of rank inside one family takes Tufte, with WCAG as its floor. Against a fixed logo colour, the logo never moves. No source measures the near-miss line directly: 10 is where four proxies meet (#178, `docs/research/de00-thresholds.md`).

### A logo's grounds follow its lightness

Records: `vault.logo-ground`, `vault.logo-ground-script`.

- **Why.** WCAG exempts a logo from contrast only where brand guidelines fix it; a ground the designer chooses is not exempt, so the 3:1 check binds in every round.
- **Trade-off.** The more grounds a site wants, the more versions the logo needs. A keyline reads as a sticker, and adds a colour that must itself pass the near-miss check.
- **Clash.** The client's own logo guidelines win.

### Never recolour a logo

Records: `vault.logo-colour`, `vault.logo-unchanged`.

- **Why.** The client owns the logo; its colours are part of the mark, as the brand guidelines of Spotify and GOV.UK both say.
- **Trade-off.** The page loses grounds it wanted, or waits for the client.
- **Clash.** A keyline is an addition, not a recolour, so it is allowed as a supplied version.

### A logo's version follows its width

Record: `vault.logo-version`.

- **Why.** A full logo squeezed into a phone header shrinks its name past reading. Atlassian shows the mark alone where space is tight and its context is clear.
- **Trade-off.** The mark alone is recognised only by visitors who already know it. How small a detailed mark may be drawn before it needs a redrawn version is the project's own measurement, as Manta's brand sheet §6 is.
- **Clash.** The client's own logo guidelines win.

### Fixed logo colours are anchors

Record: `vault.logo-anchors`.

- **Why.** Only the side the owner allows moves: the client's logo is fixed, artwork the house owns may snap to the palette. Material's hue shift toward the main hue is for interface colours, and applied to the logo file it would recolour it.
- **Trade-off.** Anchors narrow the palette, and a narrow palette risks reading plain.
- **Clash.** WCAG beats an anchor used as text. The client's ruling beats the house's taste.

## Interactions

**Anchors and the near-miss.** A palette colour that is a near-miss of a fixed logo colour is the commonest fault.

**Anchors and grounds.** A ground drawn from the anchor's hue is still a logo ground, so `vault.logo-anchors` and `vault.logo-ground` both bind it.
