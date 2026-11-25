# Line breaks

Why text hyphenates, wraps and holds word groups together where its records say (#286). The source checks behind the records are on design-vault#286 (https://github.com/lucmoseley/design-vault/issues/286#issuecomment-6842712602).

Where a project's rules file and a record here disagree, [source precedence](house-principles.md#source-precedence) decides. A dated record is reviewed a year after writing, or sooner when browsers change the behaviour it rests on.

## Principles

### Hyphenate by measure

Record: `vault.hyphens-body`.

- **Why.** Hyphenation exists to even out word spacing in justified text and the rag in narrow columns; at a normal measure a ragged edge stays uneven with or without it, so it adds breaks for no gain (Butterick). The shorter the line, the fewer break points it has and the deeper the rag, so narrow columns and table cells hyphenate (Butterick; Rutter). Languages with long compound words run out of break points sooner (web.dev).
- **Trade-off.** Browsers give almost no control over where they break, so some breaks look clumsy (Butterick), and a browser lacking the language's dictionary does not hyphenate at all (MDN).
- **Clash.** Butterick and Rutter give no number for "narrow". The house's 40 characters is the lower edge of Bringhurst's 40–50 for columns (webtypography.net 2.1.2), and 50 for long-word languages its upper edge: the house's mapping, not measured. `5 2 3` likewise joins CSS's word total to Bringhurst's limits. Justified text always hyphenates; `vault.justify-space` sets its word spacing.

### Hyphenation limits

Records: `vault.hyphen-chars`, `vault.hyphen-lines`.

- **Why.** Bringhurst's floor is two letters left behind a break and three carried forward, and no more than three hyphenated lines in a row; CSS's own suggested limits for `auto` are close (2, 2 and a five-letter word).
- **Trade-off.** Tighter limits leave fewer break points, so the rag deepens again; where it does, widen the column rather than loosen the limits.
- **Clash.** CSS suggests 2 before and after for `auto`; the house takes Bringhurst's 3 after. web-features lists no Safari support for `hyphenate-limit-chars` (caniuse lists Safari 27.3), and only Safari takes `hyphenate-limit-lines`, so both are set as enhancements and the script checks the render; `pretty` may also avoid long hyphen runs (CSS Text 4).

### Soft hyphens by hand

Record: `vault.soft-hyphens`.

- **Why.** The dictionary handles ordinary words; it fails on words it lacks, such as trade names, jargon and unusual names, and only those need a hand-placed break (Butterick). A soft hyphen shows only when the line breaks there (MDN), so it is safe to leave in.
- **Trade-off.** Hand-placed hyphens are lost when copy is rewritten.
- **Clash.** Butterick suggests a plugin that inserts soft hyphens throughout, since browsers supported them better than CSS hyphenation, and only where full justification is wanted; `hyphens` has been Baseline since 2023, so the house uses the dictionary and keeps `&shy;` to single words.

### Headings are not hyphenated

Record: `vault.heading-hyphens`.

- **Why.** A heading is short and read at a glance; a word split across its lines costs more than the rag it saves (Butterick).
- **Trade-off.** A long word in a large heading can overflow a phone screen; how it breaks there is the long-word rule's (ledger row TXL-27), not hyphenation's.
- **Clash.** A page-wide `hyphens: auto` for narrow columns reaches headings by inheritance unless they reset it.

### Balance headings, pretty paragraphs

Record: `vault.text-wrap`.

- **Why.** `balance` evens the lines of a short block, so a two-line heading does not leave one word alone on its second line; `pretty` looks ahead over a paragraph so its last line is not a single short word (MDN, Chrome, CSS Text 4). Both only choose among the existing break points and fall back to normal wrapping where unsupported, at no cost (Comeau). Pairing them replaces most hand-placed no-break spaces (Typography Handbook); the house also replaces the hand-placed `<br>` Butterick once used to even a heading, since it breaks wrongly at every other width.
- **Trade-off.** `pretty` costs layout time on long text (MDN; CSS Text 4), though Comeau measured no difference on ordinary pages; `balance` stops working past six lines in Chromium. A balanced heading keeps its box width, so in a bordered card its shortened lines leave an empty side that looks off (Chrome); the house uses `pretty` there instead.
- **Clash.** Editable text takes `stable`, by `vault.edit-wrap`, so typing does not re-wrap earlier lines. `pretty` is not Baseline (no Firefox), which is acceptable for an enhancement with no downside. Butterick's own fix for a last lone word is a no-break space; the house uses `pretty` and keeps `&nbsp;` for word groups (`vault.nonbreaking`).

### Groups that never split

Record: `vault.nonbreaking`.

- **Why.** A number cut from its unit, or a reference mark from its number, is read wrongly or not at all at the line end; narrow multi-column layouts make it more likely (Butterick; Bringhurst; NN/g).
- **Trade-off.** Every join removes a break point, so long joined runs overflow narrow boxes; join only short groups.
- **Clash.** A run of no-break spaces to widen a gap is a different misuse, ruled out by `vault.sentence-space`.
