# Rule records: data

Sets of data and repeated items: lists, tables, filters and sets of options. The form is [rules.md](../rules.md)'s.

### vault.option-sets
- applies-when: web-surface; every set of options, filters or menu items shown together
- question: Is every set of options grouped and easy to scan, whatever its count, and does a search or filter task show its relevant filters with the important ones promoted?
- answered-by: whole-page
- writes: option set
- yields-to: none
- source: NN/g, Nielsen 2009, on short-term memory and web usability; Baymard Institute, accommodation search; strength: domain evidence
- era: timeless
- owner: vault
- stage: role
- target: Group a long set of options so it scans; in a search or filter task show the relevant filters and put the important ones first.
- reasons: design-round/references/impeccable.md#struck-or-corrected
- ledger: BTN-84, FCH-8, FRM-57, LAY-187, NAV-100, NAV-169, NEW2-60, OTH-25, TXL-77, TXL-78
- status: live

### vault.table-use
- applies-when: web-surface; every `table` element on the page
- question: Does every `table` hold data a visitor reads across and down, none placing page content, save an email's layout table marked `role="presentation"` with no `th` or `caption`?
- answered-by: script
- writes: table use
- yields-to: none
- source: WCAG 2.2 success criterion 1.3.1 Info and Relationships; web.dev, Learn Accessibility, "Structure", layout tables (as read Oct 2026): they "must not use structural elements" and are hidden from assistive technology; GOV.UK Design System, Table, "Never use the table component to layout content on a page"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Use a `table` for data alone and place page content with grid or flex.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/layout-and-data.md#tables-hold-data
- ledger: NAV-268
- status: staged

### vault.table-markup
- applies-when: web-surface; text aligned into columns, in a `pre` or in running text
- question: Is no content aligned into columns by runs of spaces or tab stops?
- answered-by: script
- writes: column alignment by spaces
- yields-to: none
- source: WCAG 2.2 success criterion 1.3.1 Info and Relationships, technique H51, "Using table markup to present tabular information", whose test checks for `table`, `tr`, `th` and `td`; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Never align columns with spaces or tab stops; build them as a `table`.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/layout-and-data.md#tables-hold-data
- ledger: LAY-191
- status: staged

### vault.table-markup-look
- applies-when: web-surface; content set in rows and columns a visitor reads across and down
- question: Is content set in rows and columns built as a `table` of `tr`, `th` and `td`, or with the ARIA table roles, never as a grid of plain `div`s?
- answered-by: look
- writes: tabular markup
- yields-to: vault.table-markup
- source: WCAG 2.2 success criterion 1.3.1 Info and Relationships, technique H51, "Using table markup to present tabular information", whose test checks for `table`, `tr`, `th` and `td`; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Build anything read across and down as a `table` of `tr`, `th` and `td`.
- reasons: design-critique/references/layout-and-data.md#tables-hold-data
- ledger: LAY-191
- status: staged

### vault.table-headers
- applies-when: web-surface; every data table
- question: Does every non-empty data cell of a table larger than 3 by 3 have a header cell, does every `th` head data cells and hold text, and does every `headers` and `scope` attribute name its cells validly?
- answered-by: script
- writes: table header links
- yields-to: none
- source: WCAG 2.2 success criterion 1.3.1, technique H51; web.dev, Learn Accessibility, "Structure", data tables: "mark up header cells with" `th` (as read Oct 2026); GOV.UK Design System, Table, on `scope`; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: treatment
- target: Give every data cell a header cell, and point `headers` and `scope` only at cells the table has.
- script: check-markup.py
- parts: table
- reasons: design-critique/references/layout-and-data.md#table-headers
- ledger: NAV-253
- status: staged

### vault.table-header-cells
- applies-when: web-surface; every data table
- question: Does each data table mark its header cells as `th`, the column headings in `thead` with `scope="col"` and any row heading with `scope="row"`?
- answered-by: script
- writes: table header cells
- yields-to: none
- source: WCAG 2.2 success criterion 1.3.1, technique H51; web.dev, Learn Accessibility, "Structure", data tables: "mark up header cells with" `th` (as read Oct 2026); GOV.UK Design System, Table, on `scope`; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: treatment
- target: Mark a data table's column headings as `th` with `scope="col"` inside `thead`, and any row heading as `th` with `scope="row"`.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- parts: table
- reasons: design-critique/references/layout-and-data.md#table-headers
- ledger: NAV-253
- status: staged

### vault.table-print-header
- applies-when: web-surface; every data table that can run past one printed page
- question: Does each data table long enough to print across pages hold its header row in `thead`, which Chromium repeats on each printed page?
- answered-by: script
- writes: printed table header
- yields-to: none
- source: USWDS, "Keep a record", "Print table headers on every page" (as read Oct 2026); CSS 2.1 §17.2: "Print user agents may repeat header rows on each page spanned by a table"; measured on design-vault#278 (docs/research/layout-data-defaults.md): Chromium 149 printed a 200-row table's `thead` row on all 5 pages, and a first row of `td` cells on 1 of 4; Firefox and Safari unmeasured; strength: design-system guidance and a measurement
- era: dated 2027-10-16
- owner: vault
- stage: treatment
- target: Put a long data table's header row in `thead`, never as a first `tbody` row.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: table
- reasons: design-critique/references/layout-and-data.md#table-headers
- ledger: NAV-255
- status: live

### vault.chart-contrast
- applies-when: web-surface; every mark in the chart the parts declaration names, drawn in SVG or HTML: each line, bar, point, slice and gridline
- question: Does each mark in the declared chart contrast 3:1 with the colours next to it: a filled mark with the chart's ground, its own border and each filled mark it touches, a line with the ground alone?
- answered-by: script
- writes: chart mark contrast
- yields-to: none
- source: WCAG 2.2 success criterion 1.4.11 Non-text Contrast and its Understanding page: each line in a graph, and any gridline values are read against, takes 3:1 against adjacent colours, lines need not contrast with each other, and pie slices need 3:1 between them unless labels and values carry the data; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: treatment
- target: Give every chart mark a visitor needs 3:1 against its adjacent colours, adding a border between slices where their fills fall short, or label the data on the chart.
- script: check-access.py <page> --out <dir> --parts <declaration>
- parts: chart
- reasons: design-critique/references/layout-and-data.md#chart-marks
- ledger: COL-3
- status: staged

### vault.chart-carried
- applies-when: web-surface; every chart mark `vault.chart-contrast` finds under 3:1
- question: Of the chart marks `vault.chart-contrast` finds under 3:1, does a visitor need each one to read the chart, a gridline only where values are read against it, and where one is needed, does a label, value or pattern on the chart carry the same information?
- answered-by: look
- writes: chart mark contrast
- yields-to: vault.chart-contrast
- source: WCAG 2.2 success criterion 1.4.11 Non-text Contrast and its Understanding page: each line in a graph, and any gridline values are read against, takes 3:1 against adjacent colours, and pie slices need 3:1 between them unless labels and values carry the data; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: treatment
- target: Label the data on the chart, or mark it with a pattern, wherever a mark a visitor needs stays under 3:1, and leave faint only the gridlines no value is read against.
- parts: chart
- reasons: design-critique/references/layout-and-data.md#chart-marks
- ledger: COL-3
- status: staged

### vault.zebra-rows
- applies-when: web-surface; every data table
- question: Are alternating row fills used only on a wide table of many columns, or a label-and-value spec table, where the eye must track along a row, each stripe a subtle tint in the direction of reading, and every other table read by alignment, space and rules alone?
- answered-by: look
- writes: row striping
- yields-to: vault.zebra-tint, vault.table-headers, level 2
- source: Apple HIG Lists and tables: "Consider using alternating row colors in a multicolumn table ... especially in a wide table"; USWDS Table, striped variant, "to help the eye track across table rows", paired "with the scrollable variant for tables with many columns"; Baymard, product spec sheets (2026): "alternating backgrounds or subtle borders ... to connect labels directly to their values"; Richard Rutter, Web Typography (2017), "Keep table furniture and fills to a minimum": "Avoid zebra striping ... Only use tints as a subtle means of guiding your reader's eyes, and then only if you cannot arrange the data to that end"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Stripe the rows of a wide many-column table or a spec sheet with a subtle tint; set narrower tables by alignment, space and light rules.
- parts: table
- reasons: design-critique/references/layout-and-data.md#striped-rows
- ledger: SUR-16
- status: staged

### vault.zebra-tint
- applies-when: web-surface; every filled row or cell in a table body
- question: Does each striped row's or cell's fill hold within 1.32:1 WCAG contrast of the table's ground beneath it on a light ground, and 1.48:1 on a dark one, a tint that guides the eye rather than a band that cuts the table up?
- answered-by: script
- writes: row stripe tint
- yields-to: vault.ground-step, level 2
- source: design systems' stripe tokens against their plain rows, contrast computed from each (as read Nov 2026): USWDS `usa-table--striped`, gray-5 #f0f0f0 on white, 1.14:1; IBM Carbon `--data-table--zebra`, layer-accent on layer, 1.20:1 (White), 1.32:1 (g10), 1.31:1 (g100), 1.48:1 (g90); Bootstrap 5.3 `.table-striped`, 5% black, 1.12:1, and 5% white on #212529, 1.16:1; Shopify Polaris DataTable, #f7f7f7 on white, 1.07:1; GitHub Primer Markdown tables, #f6f8fa on white, 1.07:1; the ceilings are the highest of them on each ground, Carbon g10 on light and g90 on dark; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Tint a striped row no further than 1.32:1 from the table's ground on a light ground, or 1.48:1 on a dark one.
- parts: table
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/layout-and-data.md#striped-rows
- ledger: SUR-16
- status: staged

### vault.card-alignment
- applies-when: web-surface; a row of sibling cards that share inner parts (title, caption, attribute rows, footer)
- question: In a row of sibling cards side by side, does each matching inner part (title, caption, each attribute row, footer) start at the same height in every card?
- answered-by: script
- writes: cross-card alignment
- yields-to: level 2
- source: MDN, "Subgrid" (modified Nov 2025, read Oct 2026): nested grids "are independent of the parent grid", which "makes it difficult to line nested grid items up", and subgrid is Baseline widely available, across browsers since September 2023; Josh W. Comeau, CSS subgrid (Nov 2025, updated Apr 2026), side-by-side pricing cards whose feature lists line up through one shared grid; web.dev, Learn CSS, "Grid", subgrid; Manta's design-system readme (lucmoseley/mantahostels, docs/design-system/readme.md, read Oct 2026): comparison cards with "attribute rows at fixed shared heights so values align horizontally across cards"; strength: platform documentation and a project's design system
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Place a row of sibling cards on one grid and give each card `grid-row: span <n>` with `grid-template-rows: subgrid`, so titles, captions, attribute rows and footers line up across the row.
- script: check-layout.py <page> --out <dir> --records --parts <declaration>
- parts: card
- reasons: design-critique/references/layout-and-data.md#sibling-cards-share-their-rows
- ledger: NEW2-72
- status: staged

### vault.table-align
- applies-when: web-surface; every table
- question: Are a table's text cells left-aligned (start-aligned), never centred or justified, its compared or summed numbers right-aligned at one precision (decimal-aligned where precision must vary), its numbers that cannot be totalled (phone numbers, postcodes, dates) aligned as text, and each column heading aligned as its column's data?
- answered-by: script
- writes: table cell alignment
- yields-to: level 2
- source: Rutter, Web Typography, "Numerals and tables": "Align table text as you would anywhere else; that is, aligned left", "Right-align numbers", "you will need consistent precision", "align numbers to the decimal point" where it varies, "match the alignment of headings to the alignment of the data", "Use tabular lining numerals"; GOV.UK Design System, Table (updated Feb 2024): "align the numbers to the right in table cells", numeric headers and cells marked alike; USWDS Table (updated Aug 2026): "Right-align numerical data", no alignment for "phone numbers, zip codes, dates, or other number content that can't be totaled"; MDN, Styling tables (modified Aug 2026): "align text to the left and numbers to the right"; Butterick, Practical Typography, "Grids of numbers": tabular figures, "Zip codes are aligned left"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: In a table, left-align text cells; right-align numbers a visitor compares or totals, at one precision, in the figures `vault.figures` sets; align phone numbers, postcodes and dates as text; give each heading its column's alignment.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: table
- reasons: design-critique/references/alignment-and-width.md#table-alignment
- ledger: TXL-50, TXL-51, TXL-52
- status: staged

### vault.table-width
- applies-when: web-surface; every table and block of compact data
- question: Does a table take the width its columns need, free of the prose line length, and where that is wider than its container, scroll sideways inside its own box or stack its rows, never widening the page?
- answered-by: script
- writes: table width
- yields-to: vault.reflow
- source: Rutter, Web Typography, "Numerals and tables": "a typical table may need to be wider than the 45 – 75 characters we normally allow for paragraphs of text"; impeccable 4.5.0, operate.md: "tables at 120ch+ are fine"; USWDS Table (updated Aug 2026): numerical data "can be easier to understand if the table scrolls horizontally", directory lists in "a stacked layout", "apply a horizontal scrollbar if the columns exceed the available width"; MDN, Styling tables (modified Aug 2026): data given too much space "gets a bit lost"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Let a table run as wide as its columns need, past the prose measure; on a narrow screen wrap it in an `overflow-x: auto` box or stack its rows, so the page itself never scrolls sideways.
- script: check-layout.py <page> --out <dir> --records
- parts: table
- reasons: design-critique/references/alignment-and-width.md#table-width
- ledger: TYS-58
- status: staged

### vault.table-narrow
- applies-when: web-surface; each data table wider than the screen at phone width
- question: At phone width, does each data table too wide for the screen take the form its use needs: a table read to compare across rows or columns scrolling sideways in its own keyboard-focusable container with its headers kept, a list of records stacking each row into a block of label-value lines, a comparison of items showing at most two at a time or one tab each, a spec sheet becoming one column of collapsible sections, and never the whole table shrunk to fit?
- answered-by: script
- writes: data table form at narrow widths
- yields-to: vault.reflow, level 2
- source: Rutter, Web Typography (2017), "Numerals and tables" pp. 140–143: "Let the browser handle tables with horizontal scrolling", "Linearise simple tables into lists", "Make tables responsive according to their purpose"; W3C, Understanding SC 1.4.10 Reflow (as read Nov 2026): the exception for "data tables (not individual cells)", "presenting the table in its own scrollable container"; web.dev Learn Design, "UI patterns", Data tables (as read Nov 2026): "You can apply the overflow pattern to tables"; USWDS, Table (3.14.0, 18 Aug 2026): "A responsive stacked table collapses at narrow widths", "A scrollable table is ideal for dense data", the container `tabindex="0"`; NN/g, "Comparison Tables for Products, Services, and Features" (9 Feb 2024): "unlikely that you'll be able to show more than 2 items at a time", "converting the table to tabs or lists for small screens"; Baymard, "Product Spec Sheet UX" (24 Sep 2026): "consider using vertically collapsible sections or truncation rather than compressing the layout"; strength: expert and design-system guidance, within WCAG 2.2 AA's data-table exception
- era: timeless
- owner: vault
- stage: role
- target: Pick each wide table's phone form by its use: a scrolling, focusable container for tables read across rows or columns; stacked label-value blocks for a list of records; two items or one tab each for a comparison; collapsible single-column sections for a spec sheet.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#wide-tables-by-purpose
- ledger: LAY-76
- status: staged

### vault.stacked-row-header
- applies-when: web-surface; a table stacked into blocks at a narrow width
- question: In a table stacked for a narrow screen, is each row's first cell a row header (`th scope="row"`) set apart as its block's title, and does every other cell show its column's label beside its value?
- answered-by: script
- writes: stacked table row header and cell labels
- yields-to: level 2
- source: USWDS, Table (3.14.0, 18 Aug 2026, as read Nov 2026), responsive stacked table code: each first cell `<th data-label="…" scope="row">`, every cell a `data-label`; Rutter, Web Typography (2017), "Linearise simple tables into lists" p. 142: "a data-title attribute on each cell enabling us to repeat the label in the list view"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: When a table stacks, make each row's first cell a `th scope="row"` styled as the block's title, and print each other cell's column label before its value from a `data-label`.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: table
- reasons: design-critique/references/responsive-structure.md#stacked-rows-keep-their-labels
- ledger: NAV-247
- status: staged

### vault.card-media-stack
- applies-when: web-surface; each card or media object with an image beside its text
- question: Does each card with media beside text switch by its own container's width, by a container query, the media above the text below the threshold and beside it at or above it?
- answered-by: script
- writes: card media placement by container width
- yields-to: vault.breakpoints, level 2
- source: web.dev Learn Design, "Micro layouts", Container queries (as read Nov 2026): "If a media object is inside a container that's narrower than `25em`, the flexbox styles aren't applied", "The image and text appear are ordered vertically"; USWDS, Card (updated 14 Feb 2025): `usa-card--flag` sets media beside text "at a specified width (`$theme-card-flag-min-width`)"; Josh W. Comeau, "Container Queries Unleashed" (27 Jan 2025): container widths "the actual size that we've chosen for the flip", against media-query "magic numbers"; 25em, web.dev's example, is the house's default where a project sets none; strength: platform and design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- inputs: the card's container width, the threshold
- output: threshold = the project's own, else 25em; container width < threshold: media above text; ≥ threshold: media beside text
- target: Give the card's container `container-type: inline-size` and set media beside text only `@container (min-width: 25em)`, or the project's own threshold.
- script: check-layout.py <page> --out <dir> --records --parts <declaration>
- parts: card
- reasons: design-critique/references/responsive-structure.md#cards-stack-by-their-container
- ledger: NEW2-73
- status: staged
