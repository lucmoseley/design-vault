# Layout and data

Why a page's parts keep their source order and their space, and why tables and charts are built as their records say (#278). The source checks and measurements behind the records are `docs/research/layout-data-defaults.md` in the design vault.

Where a project's rules file and a record here disagree, [source precedence](house-principles.md#source-precedence) decides. A dated record is reviewed a year after writing, or sooner when browsers change the behaviour it rests on.

## Principles

### Space marks the most important part

Record: `vault.space-emphasis`.

- **Why.** Open space around a part sets it apart as its own group, and a part set apart draws the eye (NN/g, Gordon 2021; Harley 2020). Space ranks a part without adding colour or weight.
- **Trade-off.** Space costs room: a dense working view, a table or a dashboard, cannot spare it and ranks by size, weight and tone.
- **Clash.** `vault.weight-order` settles which part leads; this record only says how space serves it.

### Source order is visual order

Record: `vault.visual-order`.

- **Why.** A screen reader reads, and the Tab key moves, in source order. A part that CSS moves elsewhere is met out of sequence by those visitors, and a sighted keyboard user sees focus jump about the page (WCAG 2.2 SC 1.3.2, 2.4.3).
- **Trade-off.** Reordering by CSS lets one source serve a phone and a desktop layout; keeping the order means choosing a source order that suits both, or two pieces of markup.
- **Clash.** WCAG's, so it beats every layout preference.

### Safe centring

Record: `vault.safe-centre`.

- **Why.** Plain centring splits an overflow between both ends, and the part pushed past the start cannot be scrolled to.
- **Trade-off.** Content that overflows sits at the start rather than the centre, which can look lopsided at the widths where it overflows.
- **Clash.** None known.

### Horizontal scrollers

Record: `vault.scroller-input`.

- **Why.** Native scrolling already answers a sideways swipe on a trackpad, and a wheel turned while Shift is held; a script that cancels the wheel to drive the row itself takes those away.
- **Trade-off.** A plain vertical wheel does not move a native sideways row; a carousel's controls serve that mouse, and a row of cards leaves it the scrollbar.
- **Clash.** None known.

### Tables hold data

Records: `vault.table-use`, `vault.table-markup`, `vault.table-markup-look`.

- **Why.** Table markup tells a screen reader which row and column each cell belongs to; data in a grid of plain boxes loses that, and a layout table claims relationships its content does not have (WCAG 2.2 SC 1.3.1).
- **Trade-off.** A table reflows poorly on a phone, which is why data is sometimes laid out as cards; cards then carry each value's label themselves.
- **Clash.** WCAG's, so it beats every layout preference.

### Table headers

Records: `vault.table-headers`, `vault.table-print-header`, `vault.table-header-cells`.

- **Why.** A header cell names what each column or row holds; marked as one, it is read out with every cell and, in `thead`, printed again at the top of each page.
- **Trade-off.** A table component that emits no `th` or `thead` must be configured or replaced.
- **Clash.** None known.

### Sibling cards share their rows

Record: `vault.card-alignment`.

- **Why.** Cards set side by side are read across as well as down; when one card's longer title pushes its price lower, the eye has to hunt for the matching value (Manta's comparison cards, #280). Each card sized on its own grid cannot line up with its neighbours; `subgrid` lets them share the row's tracks (MDN).
- **Trade-off.** Every card takes the height of the tallest one's part, so a short card shows blank space.

### Chart marks

Records: `vault.chart-contrast`, `vault.chart-carried`.

- **Why.** A visitor who cannot make out a line or tell two slices apart cannot read the chart, so WCAG 2.2 SC 1.4.11 holds each mark needed for that to 3:1.
- **Trade-off.** A palette of series colours that each clear 3:1 against the ground and their neighbours is narrower; labels on the chart free it.
- **Clash.** WCAG's, so it beats a brand palette.

### Navigation by window width

Record: `vault.nav-by-width`.

- **Why.** A phone window under 600 px wide has room for a few destinations along one edge, and a tablet or desktop window has room beside the content (Android window size classes). Apps put their main destinations at the bottom on a phone, where the thumb reaches, and in a side rail on wider windows.
- **Trade-off.** A web site's visitors look for its navigation in the top header, so a site keeps it there and follows `vault.visible-nav`'s four-link rule.
- **Clash.** None beyond `vault.visible-nav`, which it yields to.

### Striped rows

Records: `vault.zebra-rows`, `vault.zebra-tint`.

- **Why.** In a wide table the eye can slip to the next row on its way across; a stripe holds it there (Apple HIG, USWDS). The design systems that stripe keep the tint between 1.07:1 and 1.32:1 of the plain row on a light ground, and up to 1.48:1 on a dark one (USWDS, Carbon, Bootstrap, Polaris, Primer).
- **Trade-off.** Stripes add fill to every other row and can suggest those rows matter more (Rutter); measured evidence for them is weak (Enders, A List Apart, summaries only).
- **Clash.** None known.

### One site

Record: `vault.one-site`.

- **Why.** A separate mobile site doubles the code and the design to keep in step, and has to guess which device is a phone; one responsive site on one URL is what Google recommends and indexes.
- **Trade-off.** One page must serve every width, so a layout cannot be tuned for one device without its breakpoints.
- **Clash.** None known.

### No false floor

Record: `vault.false-floor`.

- **Why.** A first screen that looks finished stops visitors scrolling; most viewing time is already spent on the first two screens (NN/g 2018).
- **Trade-off.** A hero that fills the screen exactly is a strong frame; letting the next section show takes a little of its height.
- **Clash.** `vault.layout` puts the call to action on the first screen.

### List beside map

Record: `vault.map-list`.

- **Why.** Where a place is chosen by location, visitors judge results on the map as much as in the list; when the map sat behind a toggle most never opened it, and beside the list nearly all used it (Baymard 2022).
- **Trade-off.** The split halves the list's width, so each result shows less; Baymard did not test phones, where the record does not apply.
- **Clash.** None known.

### Filters and sort

Record: `vault.filter-place`.

- **Why.** Beside a map, a filter sidebar squeezes the list; a bar above both left room and tested well (Baymard 2022). Without a map, filters kept in view on desktop are used more than filters behind a button (Baymard 2026).
- **Trade-off.** A horizontal bar holds fewer filters at once than a sidebar; the rest go behind a "More filters" control.
- **Clash.** `vault.option-sets` decides which filters show and which are promoted; this record decides where they sit.
