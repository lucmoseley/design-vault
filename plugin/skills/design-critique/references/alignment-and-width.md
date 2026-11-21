# Alignment and width

Why text lines, columns and containers take the widths and alignments their records give (#285). The source checks behind the records are `docs/research/alignment-width.md` in the design vault.

A project's rules file wins over every record here except a floor WCAG or the law sets ([source precedence](house-principles.md#source-precedence)). A dated record is reviewed a year after writing, or sooner when browsers change the behaviour it rests on.

## Principles

### Line length by role

Record: `vault.line-length`.

- **Why.** Very long lines tire readers and make the next line hard to find; very short ones break the reading rhythm (Baymard 2022). The 45–75 range was set for a single column of a serif text face at text size (Bringhurst), so other roles take their own: columns narrower (40–50), large text shorter, since it fills the width with fewer characters (USWDS), and short passages are read too briefly for the range to matter (USWDS). The count is of characters as set, so a wide or narrow face is already in it; line height rises with the count by `vault.type-leading`.
- **Trade-off.** A phone column cannot reach 50 characters at a readable size; a short line beats sideways scrolling (Typography Handbook 2026), so the floor lifts there.
- **Clash.** Butterick allows 45–90 and WCAG's AAA ceiling is 80; the house holds body text to Baymard's 50–75, inside both. Typography Handbook wants captions at 35–50 where USWDS lets them run longer; the house sets only WCAG's 80 ceiling on them, and its three-line bound for a short passage follows USWDS's "captions of fewer than three lines" loosely. Butterick keeps the range on small screens by scaling size and width together; the house leaves size to `vault.type-size` and lets the phone line run short. Supersedes the live `vault.measure`'s one range for every role when tier 1 goes live (#293).

### Cap the measure in a font-relative unit

Record: `vault.measure-unit`.

- **Why.** A cap in rem, em or ex follows the visitor's text size; a px width does not, and a fixed width breaks zoom (Every Layout). `ch` is the width of a zero, wider than most letters: the unit is fine, but the number must come from counting the set characters.
- **Trade-off.** One em or ex value counts differently in each face, so a face change means re-measuring.
- **Clash.** Every Layout, web.dev and Baymard write the cap in `ch`, Butterick rejects `ch` and USWDS uses `ex`; the house allows any font-relative unit, `ch` included, and trusts only the count.

### Ragged, not justified

Record: `vault.text-align`.

- **Why.** Browsers justify by stretching word spaces line by line, which opens rivers of white that slow readers, those with some cognitive disabilities most (WCAG 2.2 F88); good justification needs hyphenation the web does unevenly (Butterick, Rutter). Narrow columns and sans faces look best ragged (Bringhurst).
- **Trade-off.** A ragged edge looks less formal than a justified block, which some editorial brands want.
- **Clash.** Butterick calls justification "personal preference"; GOV.UK, USWDS and WCAG 1.4.8 all set ragged text on the web, so the house does, and a project that wants a justified block names it in its rules file. Supersedes the live `vault.no-justify` when tier 1 goes live (#293).

### Where justification is allowed

Record: `vault.justify-space`.

- **Why.** In a language that spaces its words, space added between letters changes the texture line by line, which looks worse than wider word spaces (Butterick); `inter-character` is for languages like Japanese (MDN).
- **Trade-off.** `text-justify` is not Baseline, so a browser may ignore it; `auto` already justifies between words for English.
- **Clash.** None known.

### Centre only short text

Record: `vault.centred-text`.

- **Why.** A centred block has two ragged edges, so each line starts somewhere new and the eye hunts for it (Latin, Dannaway); centred blocks are also hard to align with the rest of the page (Butterick).
- **Trade-off.** Centring a short block gives a hero or empty state symmetry and a calm, formal look.
- **Clash.** None known.

### One alignment a section

Record: `vault.alignment-count`.

- **Why.** Each alignment adds an edge the eye must follow, and mixed alignments in one section look messy (Dannaway; impeccable distill). Left alignment gives the eye one fixed start (USWDS).
- **Trade-off.** A section with one centred heading over left text reads as two edges; the count allows it where the centred block is short.
- **Clash.** `vault.table-align`'s right-aligned numbers and `vault.centred-text`'s short centred blocks are content calling for a second alignment.

### Text in columns

Record: `vault.text-columns`.

- **Why.** A web page has no bottom edge, so a column that runs past the screen makes the reader scroll down, back up and down again (Butterick). A heading inside multi-column text that does not span sits at the top of one column and heads only that column's text; no source read says when a heading must span, so that half is the house's.
- **Trade-off.** Short lists of links or a short block fit one screen, and columns use a wide screen's room there.
- **Clash.** None known.

### Margins set the measure

Record: `vault.side-indent`.

- **Why.** The column's width sets the base line length; indenting every paragraph to shorten lines spends the indent, which then cannot set a quotation apart (Butterick).
- **Trade-off.** An indented block is shorter than the body, so the body must run long enough that the block's lines stay in range.
- **Clash.** `vault.line-length` sets the range the indented block keeps.

### Content width by role

Record: `vault.content-width`.

- **Why.** Uncapped content on a wide screen stretches text lines and pulls related parts apart (Atlassian). A reading page caps narrower to hold the line length; dashboards and directories need more room; a board or canvas needs all of it (Atlassian). Footer bands at one width read as one footer (USWDS). An empty state's text sits on six grid columns, or four in a narrow container (Atlassian).
- **Trade-off.** A cap leaves empty sides on a very wide screen; a page of wide data may need the cap raised, as GOV.UK allows.
- **Clash.** The house takes the range of design systems' values, not one system's number. A project's rules file may set its own.

### Capped blocks sit centred

Record: `vault.capped-centre`.

- **Why.** Centring splits a wide screen's spare room evenly, so the content stays where the eye lands, not pushed to one side (web.dev, Apple HIG).
- **Trade-off.** None beyond `vault.content-width`'s empty sides.
- **Clash.** A text column inside the container is placed by `vault.alignment-lines`, left or centred.

### Alignment lines between sections

Records: `vault.alignment-lines`, `vault.alignment-break`.

- **Why.** The eye follows a line and groups what sits on it (good continuation, Wagemans et al. 2012). A grid gives every section the same lines, so text, cards and images relate across the page; content in a gutter breaks them (Atlassian, NN/g). That the main text edge repeats from section to section is the house's reading of NN/g's "keep alignment consistent"; no source read states it for sections. Small parts (buttons, icons) sit by their spacing, not the grid (Atlassian).
- **Trade-off.** A strict grid can feel rigid; a break (a full-bleed header, a centred hero) draws the eye, which is why it needs a reason. No outside source decides whether a measure-capped text column in a wide section sits on the left grid line or centred; GOV.UK sets it left in two thirds, Atlassian centres a block of 8–12 columns. Either passes if the choice repeats from section to section.
- **Clash.** One 2023 preprint (Zelchenko et al.) finds aligned arrays of icons hurt location recall; it concerns object arrays, not text edges, and is not peer-reviewed.

### Optical alignment

Record: `vault.optical-alignment`.

- **Why.** The eye aligns what it sees, not the boxes: a padded column's text sits lower than its box, and an icon's shape rarely fills its frame (Refactoring UI, Krehel).
- **Trade-off.** Optical fixes are by eye, so no script can check them; this record is answered by look, on the render.
- **Clash.** None: `vault.alignment-lines` places top-level containers on the grid, and this record aligns the content inside them.

### Table alignment

Record: `vault.table-align`.

- **Why.** Right-aligned numbers at one precision put units under units, so magnitude can be compared down a column (Rutter, GOV.UK); `vault.figures` gives them the tabular figures that keep digits in line. Text reads best from a fixed left edge, in a table as anywhere. A heading aligned as its data sits over it. USWDS gives no right alignment to figures nobody adds up, such as a phone number or a date.
- **Trade-off.** Decimal alignment has no dependable CSS yet (Rutter); padding values to one precision does the same job.
- **Clash.** Butterick allows a heading aligned against its data where it looks better, and right-aligns invoice numbers; the house follows Rutter, GOV.UK and MDN for headings, and leaves IDs to the project.

### Table width

Record: `vault.table-width`.

- **Why.** A table is scanned down columns, not read along lines, so the prose line length does not bind it (Rutter). On a narrow screen, number tables read best scrolled sideways and directory lists stacked (USWDS).
- **Trade-off.** A sideways scroll hides columns; keeping columns few avoids it (USWDS).
- **Clash.** `vault.reflow` forbids page-level sideways scroll, so the table scrolls inside its own box.
