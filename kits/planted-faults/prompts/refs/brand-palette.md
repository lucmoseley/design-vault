# Brand palette and logo

How a palette is built around a client's logo, how far apart two colours must sit, and which grounds a logo may take (#143, #175). The research behind every line is in the design vault: `docs/research/brand-palette.md`, and `docs/research/de00-thresholds.md` and `de00-greys.md` for the numbers.

A project's rules file wins over every principle here except a floor WCAG or the law sets, and, on behaviour, a principle resting on domain evidence, which it departs from only on evidence of its own ([source precedence](house-principles.md#source-precedence)). A dated principle is reviewed a year after writing, or sooner when a platform ships a new design language or WCAG a new version.

`python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-project/scripts/palette.py` measures the numbers below: ΔE00 between colours, the logo's lightness, and its grounds at 3:1.

## Principles

### A palette is roles

- **Rule.** Name each colour by its job: the main action, text, ground, surface, border, a status. Each job gets one hue family, and a family is a ramp of lightness steps. Keep the body of the palette in near hues, and give one contrasting hue a single job as the figure. Pick and adjust colours in OKLCH, or measure them in CIELAB; never in HSL, whose lightness and hue are not what the eye sees.
- **When.** Every palette, new or inherited. A colour with no job is dropped.
- **Trade-off.** Few hues with one job each read calm and clear, but can read plain. Energy then comes from lightness, scale, type and photographs, not from another hue.
- **Clash.** WCAG contrast beats any role choice. A client's fixed logo colours beat the house's harmony: they are [anchors](#fixed-logo-colours-are-anchors).
- **Era.** Roles and hue harmony are timeless. OKLCH as the working space is dated, current since the 2020s; review by 2027-10-14.
- **Source.** Schloss and Palmer 2011, harmony rising with hue similarity and a figure liked more as its hue contrast grows (peer-reviewed); Material 3, Radix Colors, Carbon, Apple HIG (design systems); W3C CSS Color 4 (standard).

### The same colour or clearly different

- **Rule.** Two colours that can share a view are one token or clearly different. Measure the gap in ΔE00 (CIEDE2000); never divide a ΔE00 figure by 100 to use ΔEOK, which ranks pairs differently.
  - **Under 2:** the same colour. Use one token.
  - **2 up to the near-miss line:** a near-miss, which reads as a mistake. Snap one to the other, or move them apart. The line is **10**, for colours that differ in hue or strength, and for greys far from the page ground: text, a logo, icons, small marks, areas that do not touch.
  - **Two large greys near the page ground that share an edge** (page, panel, card, layer): the line is **3**. A tinted grey, up to OKLCH chroma 0.05, counts as a grey.
  - **Two meanings in one view** (two statuses, a brand colour and a warning): at least **10** apart for large areas and **20** for small marks (dots, thin lines, small text), and a label or icon carries the meaning too.
  - **Steps of one colour's ramp:** exempt. Their check is contrast.
- **When.** A new colour (a token, a client colour, a logo colour) can appear in the same view as an existing one. Two colours that never share a view may sit closer.
- **Trade-off.** Keeping every pair far apart costs richness: fewer colours, or colours further from the brand's hue.
- **Clash.** Against "make distinctions as subtle as possible" (Tufte), the job decides: a difference of identity or meaning takes this rule, a difference of rank inside one family takes Tufte, with WCAG as its floor. Against a fixed logo colour, the logo never moves.
- **Era.** Timeless.
- **Source.** Under 2: W3C CSS Color 4 §14.2.1, one just-noticeable difference (standard). Two meanings at 10: Brychtová and Çöltekin 2016 (peer-reviewed); 20 for small marks, the founder's ruling on #178 over Szafir 2018 (peer-reviewed) and Colorgorical's floor. The near-miss line at 10: the founder's ruling on #178 over four proxies that meet near it (Moon and Spencer 1944, shared colour names in Heer and Stone 2012, Mylonas 2020, Szafir 2018); no source measures it directly. The line at 3 for surfaces: the founder's ruling on #178 over the eight design systems with documented pairs, which layer such surfaces 0.6–4 apart. Williams, *The Non-Designer's Design Book*, and Apple HIG Color for the rule itself (expert, design system).

### A logo's grounds follow its lightness

- **Rule.** Measure the lightness of the logo's colours. A ground takes the full-colour logo only where every logo colour reaches 3:1 against it, or a keyline around the mark does. A ground inside the logo's lightness band takes another version or nothing. The logo ships as a few named versions, each naming its grounds: full colour on the neutral grounds; reversed (white) on named dark grounds; one colour on photographs, busy grounds and other colours; a keyline version only where no other works. Clear space is measured in units of the mark.
- **When.** The logo, or a lockup holding it, is placed on any ground: page, hero, dark band, footer, photograph.
- **Trade-off.** The more grounds a site wants, the more versions the logo needs. A keyline reads as a sticker, and adds a colour that must itself pass the near-miss check.
- **Clash.** The client's own logo guidelines win. WCAG exempts a logo from contrast only where brand guidelines fix it; a ground the designer chooses is not exempt, so the 3:1 check binds in every round. A logo that is also a link, such as the nav's home link, takes a version that clears 3:1.
- **Era.** Figure and ground are timeless; 3:1 is WCAG 2.x's level for graphics (2008–2023).
- **Source.** W3C Understanding SC 1.4.3 and 1.4.11 (standard); Spotify and GOV.UK brand guidelines (first-party); Aramco and CSU Chico brand guidelines (institutional).

### Never recolour a logo

- **Rule.** Where the logo does not work on a ground, change its version or change the ground, never its colours. A version the client does not hold, such as a white logo for a dark band, is made only with the client's yes.
- **When.** Any placement, on every page.
- **Trade-off.** The page loses grounds it wanted, or waits for the client.
- **Clash.** A keyline is an addition, not a recolour, so it is allowed as a supplied version.
- **Era.** Timeless.
- **Source.** Spotify ("Its orientation, color, and composition should remain as indicated") and GOV.UK ("Do not alter colour balance within the wordmark") brand guidelines (first-party).

### Fixed logo colours are anchors

- **Rule.** Ask whether the logo's colours are fixed; they are, unless the client opens them. Each fixed colour either joins the palette as a token with a job, or is declared logo-only. Build the rest around the anchors in OKLCH: neutrals and dark grounds take an anchor's hue at low chroma, and any other hue is a figure with one job. Measure every palette colour against every logo colour by the rule above. Only the side the owner allows moves: against a client's fixed logo, the palette snaps to it; artwork the house owns may snap to the palette. A small hue shift toward the main hue (Material's at most 15°) is for interface colours, never for the logo file.
- **When.** A project with a client logo, or a brand colour the client chose.
- **Trade-off.** Anchors narrow the palette, and a narrow palette risks reading plain.
- **Clash.** WCAG beats an anchor used as text: an anchor that fails 4.5:1 gets a text-safe partner. The client's ruling beats the house's taste.
- **Era.** Asset ownership is timeless; building in OKLCH is dated as above.
- **Source.** W3C Understanding SC 1.4.3 and 1.4.11, on logo colours fixed by brand guidelines (standard); GOV.UK's palette drawn from its wordmark, Material 3's fidelity scheme and harmonize, Spotify's logo kept apart from its interface colours (design systems); impeccable `colorize`, "do not replace a visual world" (weak). Measuring against the anchors and who moves: house, from Manta's and mmm-infra's measured cases.

## Interactions

**Anchors and the near-miss.** A palette colour that is a near-miss of a fixed logo colour is the commonest fault.

**Anchors and grounds.** A ground drawn from the anchor's hue must still clear 3:1 against every logo colour.
