# Text presentation

How to tint text and how to mark a link (#123, #154). The research behind every line is `docs/research/text-presentation.md` in the design vault; `docs/research/house-audit-visual.md` measures the tint figures against shipped design systems.

A project's rules file wins over every principle here except a floor WCAG or the law sets, and, on behaviour, a principle resting on domain evidence, which it departs from only on evidence of its own ([source precedence](house-principles.md#source-precedence)). A dated principle is reviewed a year after writing, or sooner when a platform ships a new design language or WCAG a new version.

## Principles

### The tint rule

- **Rule.** Text and its neutral greys may be tinted toward the brand's main hue, at low chroma: about OKLCH C 0.01–0.03, and up to about 0.05 only for a deliberate blue-grey. Chroma falls toward white; toward black it may stay level. Make the tint in OKLCH or HCT, never HSL or Sass `darken()`/`lighten()`, whose lightness shifts with hue. Measure contrast after tinting, on every ground the text sits on.
- **When.** One clear dominant hue and a calm surface. Tint toward the main hue only, never toward an accent the page uses as a spot. A page with several strong hues or many photographs takes the dominant colour's hue or pure grey, whichever the project's rules file picks; where it picks neither, the critic faults neither and puts the choice to the founder until the project rules on it (#183 Q4). On a coloured ground, secondary text takes that ground's own hue at another lightness, never the brand neutral and never a plain grey.
- **Trade-off.** A tint buys cohesion and warmth, not readability: at the same OKLCH lightness it moves contrast very little. Pure grey is an equal choice, for a neutral or functional feel.
- **Clash.** The text-contrast floor (WCAG 2.2 SC 1.4.3) beats any tint. impeccable `quieter`'s "use tinted grays instead of pure gray" gives way to this rule: pure grey stays an equal choice.
- **Era.** Dated, current since about 2018 and mainstream since Material You (2021); review by 2027-10-14.
- **Source.** Material 3 `material-color-utilities`, Radix Colors, Tailwind v4 neutrals (design systems); Evil Martians on OKLCH, Sitnik and Turner 2025 (expert); impeccable `colorize` (weak).

### The link rule

- **Rule.** A link inside running text is marked at rest by an underline, thin and with an offset clear of descenders, or by a colour at 3:1 against the text around it, which WCAG technique G183 pairs with a non-colour cue on hover and focus. Default to the underline: a dark link beside dark body text rarely reaches 3:1, and is hard to tell apart even when it does. A link in a nav bar, a list of links or a whole-card target may drop the underline: the context marks it. On hover, change a non-colour property too, such as the underline's offset or thickness.
- **When.** Running text versus standalone links. A colour that marks links or actions never colours non-link text.
- **Trade-off.** Underlines add noise in a dense list of links; colour alone fails colour-blind readers and, with dark colours, everyone.
- **Clash.** WCAG 2.2 SC 1.4.1 beats any brand rule: a prose link with neither an underline nor 3:1 against its text fails it. Butterick's "underlines are dying" is typographer's taste and gives way.
- **Era.** The need for a non-colour cue is timeless. Colour-only prose links are a dated 2010s flat-design trend.
- **Source.** W3C Understanding SC 1.4.1 and technique G183 (primary standard); GOV.UK Design System links (design system); NN/g, Nielsen 2004 (expert); Apple HIG Color (design system).

## Interaction

**Tint and links.** The nearer the body text's tint sits to the link's hue, the less colour can mark a link: with tinted dark text, underline links in prose.
