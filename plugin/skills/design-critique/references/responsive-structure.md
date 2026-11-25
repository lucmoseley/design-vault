# Responsive structure

Why each structural part of a page (panes, grids, side panes, navigation, tables, rows of items) takes the form its records give as the window narrows, and in what order parts stack (#291). The source checks behind the records are on design-vault#291: https://github.com/lucmoseley/design-vault/issues/291#issuecomment-6843543498.

Where a project's rules file and a record here disagree, [source precedence](house-principles.md#source-precedence) decides. Window size classes are written in CSS px, which Android's dp match one for one. Page structure follows the window's class; a component follows its own container, by `vault.breakpoints`.

## Principles

### Panes by window width

Records: `vault.panes-by-width`, `vault.pane-split`.

- **Why.** Android's window size classes are its tool for "high-level application layout decisions": one pane under 840 px, two from 840 px. A phone held sideways is wide but short, and two panes do not work there. Apple sizes by class, "not device type or orientation". A page shown as a zoomed-out copy of its desktop layout is what a phone does without the viewport meta (MDN).
- **Trade-off.** Android's canonical-layouts page also splits the medium class (600–839 px) evenly between main and supporting panes, against its overview's single pane. The house takes one pane, since Apple warns that panes in a narrow window wrap or truncate their content.
- **Clash.** Yields to `vault.reflow`, which sets the no-sideways-scroll floor at every width.

### Columns by width

Record: `vault.content-columns`.

- **Why.** A grid that fits as many columns as its items' minimum width allows changes its count without a media query (MDN, web.dev), and a feed does the same (Android). On a phone, cards fall to one column. Category tiles fall to two, or one, which Baymard found on the category pages it reviewed.
- **Trade-off.** A fluid grid leaves a row's last cards stretched or a gap, which only a breakpoint can control. A breakpoint is set where the content breaks, by `vault.breakpoints`, never at a device's width.
- **Clash.** None. `vault.breakpoints` says where a breakpoint goes; this record says how many columns a grid shows.

### Side panes move below or into a sheet

Record: `vault.side-pane`.

- **Why.** When a supporting pane no longer fits beside the main one, Android puts it below the main content or in a bottom sheet. Atlassian turns its side panel into an overlay at 1024 px and below. Content read in flow belongs below the main content. A tool used on demand, such as filters or details, belongs behind a labelled control, so it does not push the main content down.
- **Trade-off.** A pane behind a control is out of sight; Apple asks that each pane can still be reached "in a logical way".
- **Clash.** Navigation panes follow `vault.nav-by-width`.

### One-column order

Record: `vault.stack-order`.

- **Why.** On a small screen the page reads in its source order (web.dev, MDN), so the source order is the page's priority order. A content priority guide lists a page's parts in that order (Sparkbox), and the first view leads with the visitor's top task (`vault.top-tasks`). Stacking can push the members of a group far apart (NN/g, on proximity).
- **Trade-off.** One source order serves every width, so a part placed second on the desktop layout may come later on a phone.
- **Clash.** Yields to `vault.visual-order`: reorder the source, never the boxes by CSS.

### Swap parts only for the same job

Record: `vault.component-swap`.

- **Why.** Adaptive layouts "replace layout components" as the width changes (Android). A swap keeps the part's job.
- **Trade-off.** The house's condition that both forms hold the same items in the same order is its own, so a returning visitor finds an item where they left it.
- **Clash.** The swap each named part takes is its own record's: popovers `vault.popover-sheet`, navigation `vault.nav-by-width`, tabs `vault.tabs-narrow`, tables `vault.table-narrow`, side panes `vault.side-pane`.

### Popovers become sheets

Record: `vault.popover-sheet`.

- **Why.** Apple keeps popovers for wide views and presents their content as a sheet in compact ones, and impeccable swaps dropdowns for bottom sheets on a phone.
- **Trade-off.** A sheet covers more of the page than a popover, so the visitor loses sight of what opened it.
- **Clash.** The 600 px bound is Android's compact width, which the house gives Apple's "compact views".

### Rows wrap

Record: `vault.row-wrap`.

- **Why.** A flex row does not wrap by default, so its items overflow their container (MDN). With wrapping, items "drop to a new line".
- **Trade-off.** A wrapped row grows taller; a row meant to scroll is `vault.nav-strip`'s or `vault.scroller-input`'s.
- **Clash.** A button group is `vault.button-group-stack`'s.

### Label and value stack

Record: `vault.label-value-stack`.

- **Why.** A key and its value sit on one row only while both fit; otherwise the value moves to a new line (Comeau, by a container query). At large text sizes, inline items crowd text into truncation or overlap, and Apple stacks the text above them. WCAG 1.4.4 asks for no loss of content at 200% text.
- **Trade-off.** A stacked list is longer and harder to scan down one column of values.
- **Clash.** None.

### Desktop navigation stays in view

Record: `vault.nav-wide`.

- **Why.** In NN/g's 2016 study of 179 people, hidden navigation cut discoverability on desktop, and NN/g advises never hiding it there. Its 2024 homepage guideline still asks for the main navigation in a highly noticeable place.
- **Trade-off.** A long navigation does not fit a desktop header either; it is shortened, not hidden.
- **Clash.** At phone width `vault.visible-nav` governs, and NN/g says phones have "no hard-and-fast rule". Between 600 and 1023 px, `vault.nav-by-width` sets the form. The study is ten years old; no newer NN/g measurement was found.

### A long link row scrolls in one line

Record: `vault.nav-strip`.

- **Why.** web.dev keeps navigation in view by putting links on one line truncated at the screen's edge, and asks that the cut show more follows. Baymard finds horizontally scrolling subcategory strips efficient on mobile.
- **Trade-off.** Links past the edge are seen only by those who swipe; the cut link is the cue.
- **Clash.** Yields to `vault.visible-nav`, which may put the main links behind a menu past four.

### Long breadcrumbs keep first and last

Record: `vault.breadcrumb-narrow`.

- **Why.** GOV.UK keeps the first and last items on mobile, and Atlassian collapses the middle into one ellipsis item, "Show more breadcrumbs". The trail stays on small screens for context (impeccable).
- **Trade-off.** The middle levels take a tap to reach.
- **Clash.** None.

### Tabs become sections

Record: `vault.tabs-narrow`.

- **Why.** GOV.UK shows tab panels on one page, in order, with a contents list, both without JavaScript and on small screens, where a row of tabs would not fit.
- **Trade-off.** GOV.UK says the small-screen half needs more research; the record is reviewed when it publishes that.
- **Clash.** None.

### A big footer collapses

Record: `vault.footer-narrow`.

- **Why.** USWDS's big footer makes each link group collapsible on mobile and widens to more columns at its larger breakpoints.
- **Trade-off.** Collapsed links take a tap, and a visitor scanning for one link opens groups to find it.
- **Clash.** None.

### Bars move actions into More

Records: `vault.bar-overflow`, `vault.bar-fit`.

- **Why.** Apple has a toolbar's designer choose which items move into the overflow menu as the bar narrows, least important first, and Atlassian folds a header's end items into one "More" button under 768 px. On iOS only the most important items stay in the bar, with the rest in a More menu (Apple). One practitioner's demo stands a wide tool bar on a phone's left edge instead, since a phone has more height than width (Benji Taylor's Drawesome); the house allows that alternative but does not require it.
- **Trade-off.** A More menu saves space but "can also hinder discoverability" (Apple), so it is kept for actions that do not fit.
- **Clash.** Yields to `vault.reflow`, which a bar running off the screen fails. Which actions stay is judgement, so the record is a look question.

### Wide tables by purpose

Records: `vault.table-narrow`, `vault.table-narrow-form`.

- **Why.** Rutter has a table's phone form follow how its reader uses it. A table read across rows or columns scrolls sideways in its own container, which WCAG's reflow exception allows for data tables. A list of records linearises into blocks (Rutter, USWDS's stacked table). A comparison shows at most two items, or tabs (NN/g). A spec sheet becomes collapsible sections (Baymard).
- **Trade-off.** A scrolling table hides columns off screen; a stacked one loses comparison down a column.
- **Clash.** Yields to `vault.reflow`: the page itself never scrolls sideways. The scrolling container takes `vault.scroller-input`'s input rules.

### Stacked rows keep their labels

Record: `vault.stacked-row-header`.

- **Why.** USWDS's stacked table marks each row's first cell `th scope="row"` and labels every cell, so a block reads as a record with its title and its labelled values.
- **Trade-off.** Labels repeated in every block lengthen the page.
- **Clash.** None.

### Cards stack by their container

Record: `vault.card-media-stack`.

- **Why.** A card's layout follows the width of its own container, not the window's (web.dev's container query, at 25em; USWDS's flag card at a set width).
- **Trade-off.** 25em is web.dev's example, not a measured best; a project may set its own.
- **Clash.** Yields to `vault.breakpoints`, which sets where component queries go.

### Button groups stack

Record: `vault.button-group-stack`.

- **Why.** USWDS's button group becomes a column on small screens. Apple lets text buttons span the screen's width, allowing two short ones side by side.
- **Trade-off.** A column moves the second button down, out of a short screen's view.
- **Clash.** None.

### Table text on a phone

Record: `vault.table-text-narrow`.

- **Why.** Rutter fits a table to a phone with a condensed face or a slightly smaller size, never both. GOV.UK shrinks table text on small screens only for tables with a lot of data.
- **Trade-off.** Smaller text costs readability, which Rutter says "must remain paramount".
- **Clash.** Yields to `vault.type-size` (the dense role's size) and `vault.type-floor`.
