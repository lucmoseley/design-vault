# Tone

Why the feel a design aims at, its tone, is set as a position on five scales, and how each choice moves it (#288). The records are `vault.tone-direction`, `vault.tone-words`, `vault.tone-colour-share`, `vault.tone-saturation`, `vault.tone-space`, `vault.tone-symmetry`, `vault.tone-face` and `vault.tone-mix`, in [rules/](../rules/). The research behind every line is `docs/research/design-feel.md` (#204) and `docs/research/tone-sources.md` (#288) in the design vault.

Where a project sits on the scales is its own brief's call; nothing here says which tone is right. Where a project's rules file and a record here disagree, [source precedence](house-principles.md#source-precedence) decides, and the [brand-layer line](house-principles.md#the-brand-layer-line) says where expression may go before any of these says how much.

## The five scales

Tone is a position on each scale, never one named style. Evidence backs scales, not a list of feels: as #204 read it, a fixed set of fine feel buckets did not hold across cultures (Faiola et al. 2011), and a named style is a bundle of a position plus motifs, and dated.

| Scale | Low end ↔ high end | Choices that move it | Strength |
|---|---|---|---|
| Energy | calm ↔ loud | saturation, share of surface in colour, lightness and size jumps, motion speed and amount, density, asymmetry | strong for saturation and density; convention for contrast and size jumps |
| Weight | light ↔ heavy | type and line weight, darkness, size | strong for darkness; moderate for line and type weight |
| Warmth | cool and hard ↔ warm and soft | hue, corner radius and curvature, rounded or humanist type | strong for curvature; moderate for hue |
| Order ↔ richness | ordered, simple ↔ varied, inventive | grid and alignment, symmetry, density, variety of parts, effects, mixed aesthetics | strong as two separate axes people judge |
| Familiarity | typical of the category ↔ novel | layout structure against the category's usual one | moderate |

- **Why.** Three axes recur in each domain: colour gives colour activity, weight and heat (Ou et al. 2004); saturation raises arousal and brightness lowers dominance (Valdez and Mehrabian 1994); round shapes read soft and angular ones hard (Jiang et al. 2016; Bar and Neta 2006). #204 ties them to Osgood's activity and potency, and order and richness to VisAWI's simplicity and diversity and Lavie and Tractinsky's classical and expressive aesthetics; #288 did not re-open those. Low complexity and a typical layout are liked within 50 ms (Tuch et al. 2012).
- **Trade-off.** Too loud costs more than too quiet: past its peak, complexity's cost is large (Cohen's d 2.0) against a moderate one below it (0.6), and colourfulness's is milder both ways (0.8 above, 0.3 below; Reinecke and Gajos 2014). Expressive designs were rated more energetic, playful and friendly, but "a strong minority of users preferred calmer, less intense versions" (Google, M3 Expressive research, 2025).
- **Clash.** Craft (VisAWI's craftsmanship, the evaluation axis) is not a scale: every tone aims high on it. "Refined" in the founder's sense is a region, not an end: energy low to moderate, weight light, order high, craft high (design-feel.md §D1).
- **Era.** The axes are timeless; which choice reads where is partly cultural (hue, the meaning of white space).

## Setting the direction

Record: `vault.tone-direction`.

- **Why.** A direction that names its tone lets a critic check "is this as calm as asked" rather than read adjectives. Palette, face and corner shape each move the scales, so one picked without the others pulls the feel apart.
- **Trade-off.** A named style ("quiet luxury", neo-brutalism) carries fifty decisions in two words, and a dated look with them; it is placed on the scales and its motifs taken on purpose, never as the tone itself.
- **Clash.** impeccable's direction step chooses a world and a colour strategy (`new-work.md` §4); the scales say what feel that world must reach, and the brief's tone wins where the two disagree. A product's described behaviour ("calm coaching") does not set the surface's energy (impeccable `new-work.md`).

## Bolder, quieter, louder and calmer

Record: `vault.tone-words`.

These four words name moves along the scales: louder is more energy, bolder more weight and a stronger lead, quieter less energy, and calmer less energy with more order. The choices each moves are `vault.tone-words`' lookup. They never mean impeccable's familiarity register, whose "bolder" re-roll deals more unusual worlds; that move is asked for in its own words ("less like the usual site", "more unusual").

- **Why.** Each move is the direction the evidence gives: saturation raises arousal (Valdez and Mehrabian 1994; Wilms and Oberfeld 2018); symmetry "is quiet and static" and asymmetry gives "energy and movement" (NN/g, 2020); productive motion is subtle and expressive motion "vibrant, and highly visible" (IBM Carbon).
- **Trade-off.** "If every element got louder, the section got flatter" (impeccable `bolder`), so bolder strengthens what the design already leads with. Quieter is not plainer: impeccable keeps "refined", not generic, as its aim.
- **Clash.** impeccable reads "bolder" or "safer" said while its direction round is open as its register; in a house round the founder's words carry the house meaning even then, and only a request for more unusual directions goes to the register. No outside source defines the four words; the split between them is the house's mapping onto the scales, not a finding (tone-sources.md S10). Any move stops at a floor the records set elsewhere: contrast, size and the brand-layer line.

## Colour share

Records: `vault.tone-colour-share`, `vault.calm-colour-share`.

- **Why.** Neutrals carry "most backgrounds, text, and shapes" (Atlassian), and USWDS splits the non-neutral colour 60/30/10 with the neutral base usually "the predominant tone". More colour on the surface makes a page more colourful, and saturation raises arousal (below). A small accent share is what makes the accent stand out: the 10% "lifts the subject out from its background" (Rauno, "Novelty", 2026, who offers it as an observation, not a prescription).
- **Trade-off.** A restrained share keeps colour for meaning and action (Dannaway, 2026) and reads calm; a committed or drenched surface gives energy and brand presence and leaves colour less room to signal. The appeal curve peaks at moderate-to-high colourfulness and varies by audience, so the share is set for the audience, not by a fixed number.
- **Clash.** The House DNA's taste line bans several colours at equal weight with none dominant, which a share that names one leading hue meets. The bands take USWDS's 60/30/10 and impeccable's four strategies with its 30–60% for a committed surface, both convention; matching them to energy is the house's, not measured.

## Saturation

Record: `vault.tone-saturation`.

- **Why.** Saturation raises arousal ("Arousal = −.31B + .60S"; Valdez and Mehrabian 1994), and "saturated and bright colors were associated with higher arousal" (Wilms and Oberfeld 2018).
- **Trade-off.** High chroma carries energy and draws the eye, so it is spent where attention should go; neon "may distract users" (NN/g, 2025).
- **Clash.** A chroma past the display's gamut is clipped and changes look (jakub.kr), so a loud tone stays inside it. impeccable's 70–85% saturation for quieter is a convention with no source.

## White space

Record: `vault.tone-space`.

- **Why.** Density adds to a page's visual complexity, which people judge within 50 ms and like low (Tuch et al. 2012); past its peak, complexity costs appeal steeply (Reinecke and Gajos 2014). More space reads calmer and more ordered. "Some whitespace has meaning almost as salient as the darker pixels" (Ström-Awn, 2024).
- **Trade-off.** "Too much white space can be perceived as a lack of content and substance, whereas too little can come off as disorganized" (CXL). A working tool for skilled users earns density by the value per screen it gives (Ström-Awn's Bloomberg Terminal); how dense a working view goes is `vault.busy-density`'s ([busyness](busyness.md#how-busy-for-which-visitor)).
- **Clash.** What white space means in advertising comes from 20th-century North American art and rhetoric, and "its meanings are sufficiently different across cultures" (Pracejus, O'Guinn and Olsen 2013), so any reading of it beyond calm and order is cultural. `vault.space-emphasis` places space around the leading part; this record sets the page's total.

## Symmetry

Record: `vault.tone-symmetry`.

- **Why.** "Asymmetry is dynamic and engaging. It creates a sense of energy and movement. Symmetry is quiet and static" (NN/g, 2020). Symmetric logos raise perceived quality through perceived stability (Wu, PLoS ONE, 2025).
- **Trade-off.** Symmetry reads stable and trustworthy and can read static; asymmetry gives energy and needs balance by weight so it reads as chosen.
- **Clash.** Wu's effect holds only under low mental load and was measured on logos, so on a busy working page symmetry buys less. impeccable lets Persuade and Experience surfaces go asymmetric and keeps Operate and Read predictable (`layout.md`).

## Typeface by tone

Record: `vault.tone-face`.

- **Why.** "Different fonts convey different feelings, and you want a font that complements the tone of your text" (Typography Handbook, 2026). Readers "react to it in an emotional way before anything else", so a face is chosen for how it makes readers feel, then for how it works (Google Fonts Knowledge, "Emotive considerations").
- **Trade-off.** A face with a point of view carries the tone in display type; a neutral, readable body face lets it, and system faces suit tools and dashboards (Typography Handbook, 2026; Carbon's productive and expressive type sets). Size, weight and spacing then follow the face (`vault.type-size` and the other typeface-traits records).
- **Clash.** What a face evokes is cultural and moves with time: "these associations can change over time, too" (Google Fonts Knowledge). A subject association alone (books want a serif) is the default impeccable exists to break.

## Mixed aesthetics

Record: `vault.tone-mix`.

- **Why.** A deliberate mix of eras, such as bitmap type over a Renaissance painting, "creates a moment of curiosity", useful "for driving first impressions and establishing tone" and not "often in productivity software" (Rauno, "Contrasting Aesthetics", 2024). It works with "authoring intent", and by holding the rest of the part constant.
- **Trade-off.** A mix raises richness and novelty and costs consistency, the same patterns everywhere inside the system (NN/g, consistency and standards). Carbon allows a contrasting type moment where a visitor enters a product and the page "opens up", not inside a card or data table.
- **Clash.** Faces from different periods are mixed with care (Google Fonts Knowledge, pairing), and two faces are the usual limit, each with one role (Butterick). The mix stays in the brand layer: `vault.brand-layer` wins where a mix would touch a signifier.
