# Text presentation

Why text is tinted and links are marked as their records say, and how two House DNA lines weigh against the tint and case rules (#123, #154, #272, #270, #275, #287). The records are `vault.text-tint`, `vault.link-style`, `vault.colour-script`, `vault.dna-near-black`, `vault.dna-caps-label`, `vault.heading-space`, `vault.body-ink`, `vault.text-steps`, `vault.text-on-dark`, `vault.dark-ground`, `vault.controls-on-photo`, `vault.visited-links`, `vault.prose-emphasis`, `vault.sibling-emphasis`, `vault.emphasis-cues`, `vault.text-case`, `vault.caps-extent` and `vault.name-case`, in [rules/](../rules/). The research behind every line is `docs/research/text-presentation.md` in the design vault, #275's source checks are `docs/research/carry-source-checks.md`, and design-vault#287's source checks are (https://github.com/lucmoseley/design-vault/issues/287#issuecomment-6842731457); `docs/research/house-audit-visual.md` measures the tint figures against shipped design systems.

A project's rules file wins over every record here except a floor WCAG or the law sets, and, on behaviour, a record resting on domain evidence, which it departs from only on evidence of its own ([source precedence](house-principles.md#source-precedence)). A dated record is reviewed a year after writing, or sooner when a platform ships a new design language or WCAG a new version.

## Principles

### The tint rule

Record: `vault.text-tint`.

- **Why.** HSL's lightness and Sass's `darken()` shift with hue, so only OKLCH or HCT holds lightness while the tint moves. Chroma falls toward white because pale tints read as coloured long before dark ones do. A spot accent is a figure, and greys tinted toward it compete with it. Where a page has several strong hues or many photographs and the rules file picks neither the dominant hue nor pure grey, the critic faults neither and puts the choice to the founder (#183 Q4).
- **Trade-off.** A tint buys cohesion and warmth, not readability: at the same OKLCH lightness it moves contrast very little. Pure grey is an equal choice, for a neutral or functional feel.
- **Clash.** The text-contrast floor (WCAG 2.2 SC 1.4.3) beats any tint. impeccable `quieter`'s "use tinted grays instead of pure gray" gives way: pure grey stays an equal choice.

### The link rule

Records: `vault.colour-script`, `vault.link-style`, `vault.carry-navigate`.

- **Why.** A dark link beside dark body text rarely reaches 3:1, and is hard to tell apart even when it does, so the underline is the default. Where navigation, a link list or a card that links as a whole holds it, the context already says "link". A hover that changes only colour fails the visitor who cannot see the colour.
- **Trade-off.** Underlines add noise in a dense list of links; colour alone fails colour-blind readers and, with dark colours, everyone.
- **Clash.** WCAG 2.2 SC 1.4.1 beats any brand rule. Butterick's "underlines are dying" is typographer's taste and gives way. Colour-only prose links are a dated 2010s flat-design trend.

### Near-black and the House DNA

Record: `vault.dna-near-black`.

- **Why.** Anthropic's `frontend-design` counts "tinted near-black (#0B0B0B, #111) standing in for black" as template chrome that turns up whatever the subject (3 Sep 2026). Both values carry no hue, so "tinted" there reads as black lightened, not a hue: the tell is a stock dark nobody chose.
- **Trade-off.** A dark tinted toward the main hue ties the page to its brand, at the cost of one more token to keep in step.
- **Clash.** On a dark ground, and for near-black text, the tint rule wins over House DNA `never` line 5. A near-black ground is one of the neutral greys `vault.text-tint` tints, and `vault.logo-anchors` tints dark grounds toward a logo's hue. The line still catches a near-black standing in for black that nothing chose, a hue-less stock value above all, reported at P2 at most like every DNA miss.

### Capitals on labels and the House DNA

Record: `vault.dna-caps-label`.

- **Why.** Anthropic's `frontend-design` names "using all caps for labels" among the commonest tells of a generated page (3 Sep 2026): capitals reached for by habit, not for the content.
- **Trade-off.** Typographers set short strings in capitals, headers, captions and labels among them, with 5–12% added tracking (Butterick). The reading cost is weaker than assumed: Arditi and Cho (2007) found capitals read faster than mixed case near the acuity limit, and no slower at larger sizes.
- **Clash.** House DNA `never` line 7 against the case research (`docs/research/text-presentation.md` B2.3): a label in capitals that nothing asked for is weighed as the DNA's tell alone, at P2 at most, and one the brief or the rules file asks for passes. Neither is a legibility fault while it stays under one line. Capitals running longer are impeccable's "all-caps body text" finding. `vault.ai-look` decides whether a decorative eyebrow belongs at all, never its case.

### Space above a heading

Record: `vault.heading-space`.

- **Why.** A heading belongs to the text after it, and nearness is how the eye groups (NN/g on proximity), so it sits closer to what follows than to what came before.
- **Trade-off.** Generous space above a heading lengthens the page, and too much above a heading near a screen's foot pushes it below the fold.
- **Clash.** None known.

### Near-black body text

Record: `vault.body-ink`.

- **Why.** Reading speed holds steady over a wide range of contrast, so a dark grey near 12:1 reads as well as black, and on a screen that glows it is gentler; USWDS adds that pure black on white troubles some readers with dyslexia or light sensitivity.
- **Trade-off.** A grey too light becomes the fashionable low-contrast grey that NN/g calls illegible; below 7:1 small text suffers for readers with weaker sight.
- **Clash.** The contrast floor (WCAG 2.2 SC 1.4.3) beats it. `vault.text-tint` sets the grey's hue; this record sets only its darkness.

### Two text colours per ground

Record: `vault.text-steps`.

- **Why.** Each step of grey down costs contrast, and neighbouring greys are hard to tell apart, so the web systems stop at two readable steps (Radix's 11 and 12) and rank further with size, weight and space. A colour picked for one ground is measured on that ground; a see-through grey changes with what lies under it.
- **Trade-off.** Two steps is a coarse ladder for dense screens; Apple's four labels serve native lists, at the cost of the lower steps' legibility.
- **Clash.** WCAG wins: placeholder text is held to 4.5:1 like any text, and only disabled controls are exempt.

### Text on a dark ground

Record: `vault.text-on-dark`.

- **Why.** Pure white on near-black glares and makes letters seem to bloom, so off-white near 10:1 reads more calmly; colour in thin small text is hard to see, so status rides on a border, icon or chip.
- **Trade-off.** Off-white gives up the last bit of contrast some low-vision readers want; a platform's increased-contrast setting can restore it.
- **Clash.** `vault.dark-text-weight` and `vault.type-weight` set weight on dark; this record sets only colour.

### Controls on photos

Record: `vault.controls-on-photo`.

- **Why.** A photo has light and dark parts, so a dot or arrow that shows on one slide vanishes on the next; its own backdrop or shadow carries it over any image. A faint change of opacity is too weak to show which slide is current.
- **Trade-off.** A backdrop adds a small shape on top of the photo; a shadow is quieter but weaker on busy images.
- **Clash.** `vault.text-on-photo` handles text over images; this record handles the controls.

### Visited links

Record: `vault.visited-links`.

- **Why.** In a list of articles a reader comes back to, a visited colour shows what they have already read. In navigation, cards and tools it only adds noise.
- **Trade-off.** One more link colour to keep apart from the others, and browsers only let it change colour.
- **Clash.** The text-contrast floor still applies to visited links; WCAG does not fault a colour-only visited state.

### Emphasis in running text

Record: `vault.prose-emphasis`.

- **Why.** Bold and italic stand out because they are rare; used often, nothing stands out. A sans serif's italic barely slants, so bold does the job there. Underline belongs to links.
- **Trade-off.** In an interface already full of semibold labels, bold in prose loses some force.
- **Clash.** `vault.link-style` owns the underline.

### One among equals

Record: `vault.sibling-emphasis`.

- **Why.** Semibold beside regular is too small a step to see; bold, a fill on the item, size or position are seen at a glance. A link or action colour on a static item makes it look clickable, and a tag beside buttons gets pressed.
- **Trade-off.** A fill on the item adds colour to a calm list; weight alone is quieter but can be missed.
- **Clash.** `vault.primary-action` wins: the item set apart must not outweigh the view's main action.

### Ranking text

Record: `vault.emphasis-cues`.

- **Why.** Weight and a second text colour rank text without breaking the type scale; size steps add up quickly, so they stay small. Text made both lighter and smaller than body text loses legibility twice. Three levels of contrast are enough for a complex view (NN/g).
- **Trade-off.** Ranking by weight adds visual noise if many things are bold.
- **Clash.** `vault.heading-step` sets the step between a heading and its body, and `vault.text-steps` holds text colour to two readable steps, so the third level of contrast comes from weight or size.

### A dark ground is near-black

Record: `vault.dark-ground`.

- **Why.** Light text on pure black glows at its edges and tires the eye over a long read, and shadows cannot show on black (Material; Typography Handbook).
- **Trade-off.** Near-black looks less deep than true black on an OLED screen. A slide or a film watched in a dark room is the exception: there black sends the least light (Butterick).
- **Clash.** `vault.dna-near-black` decides the hue of the near-black (tinted toward the brand or pure grey); this record decides only how dark it is.

### Sentence case by element

Record: `vault.text-case`.

- **Why.** Every design system checked sets headings, buttons, tags and list items in sentence case (GOV.UK, Atlassian, USWDS), and GOV.UK moved its tags off uppercase in 2023 because capitals read worse in longer tags. Title case marks words as a title when a heading is a statement (Butterick). An odd case among its siblings reads as emphasis nobody meant (NN/g).
- **Trade-off.** Title case reads as formal and sentence case as casual (Apple), so a brand that wants a formal voice gives up a little of it.
- **Clash.** Apple leaves the case to each app, so long as each kind of element keeps one; the house takes the design systems' sentence case and a project's rules file may name another. Atlassian's typography page lists capitals for the lozenge and its lozenge page sentence case; the house follows the component page.

### How much in capitals

Record: `vault.caps-extent`.

- **Why.** Capitals suit short strings, a heading under one line, headers, captions and labels, and only with added tracking (Butterick, Latin). Longer runs read worse by convention, whose older studies the house has not read, and every design system checked limits capitals to a few words or to acronyms (USWDS, Atlassian, GOV.UK).
- **Trade-off.** Capitals separate a label from the text below it without bold or colour; holding them to a few words limits that tool to eyebrows and headers.
- **Clash.** The measured reading cost is small (Arditi and Cho, under the House DNA section above), so this record bounds length for habit and texture, not legibility. Whether a label should be in capitals at all, on a project taking the House DNA, is `vault.dna-caps-label`'s question; this record sets how long a capitals run may be.

### Names as typed

Record: `vault.name-case`.

- **Why.** In some names the case is part of the name, McNamara and van der Waals among them, so a transform that capitalises each word or the whole name misspells them (USWDS, W3C).
- **Trade-off.** A list styled in capitals shows names mixed in with it in their own case, which looks less even.
- **Clash.** `vault.typed-case` sets capitals in CSS; on a name, this record wins and no transform applies.

### List markers

Record: `vault.list-marker`.

- **Why.** A bullet's job is to mark where an item starts and no more; a small geometric mark does that at any size, where a pictorial one blurs. A screen reader can read an emoji bullet by name before every item, "white heavy check mark", where a `ul` is announced as a list.
- **Trade-off.** A plain marker gives no hint of each item's kind; an icon list does, at the cost of icons to choose and keep consistent.
- **Clash.** `vault.list-markup` sets the list's markup and that bullets are never typed; this record sets only the marker's shape. The House DNA `never` line on emoji bullets says the same.

## Interaction

**Tint and links.** The nearer the body text's tint sits to the link's hue, the less colour can mark a link, which is why `vault.link-style` leans on the underline wherever the text is tinted.
