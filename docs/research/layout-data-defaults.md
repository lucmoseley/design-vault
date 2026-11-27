# Layout and data defaults: source checks and measurements (#278)

The source checks and browser measurements behind tier 0 jobs ranks 13–16 of the coverage ledger: carry-function-fit, data-defaults, layout-defaults and carry-impeccable-checks. Read 16 Oct 2026.

## 1. Sources checked

| Row | Record | Source opened, and what it says |
|---|---|---|
| BTN-9 | `vault.action-on-dark` | GOV.UK Button: the inverse modifier shows "white buttons on dark backgrounds". USWDS Button: inverse is a "light color button for dark backgrounds", with an outline-inverse example. Checks `function-fit.md:118` (B3.1, the action's colour on a brand ground) and closes `manta-element-coverage.md:413` (K11, no rule for an outline button on ink). |
| SUR-85 | `vault.tag-fill` | GOV.UK Tag: white text on a dark fill was changed to "a lighter background colour and darker text" after "some users perceived these as buttons"; Dec 2023, lighter variants "to make tags easier to distinguish from buttons". Atlassian Badge: "Only use bold semantic badges for elements of high importance". Checks `function-fit.md:151` (B5.1) and `manta-design-migration.md:41` (C8). Refactoring UI's article returned 403 and is not cited. |
| SUR-69 | `vault.inverse-surface` | material-components-android `Snackbar.md`: container `colorSurfaceInverse`, label `colorOnSurfaceInverse`, action `colorPrimaryInverse`. androidx Compose Material 3 `PlainTooltipTokens.kt`: container `InverseSurface`, text `InverseOnSurface`. This replaces `function-fit.md:263`'s "from knowledge, not re-read". m3.material.io renders only by script, so its colour-roles page could not be read. |
| STA-52 | `vault.whole-target` | GOV.UK Accordion: "the user can interact anywhere in the heading button". GOV.UK Task list: "The whole row is linked", after users tried to select task statuses. NN/g, Loranger 2015, "Clickable Elements": make associated picture, icon and text clickable together, which "increases the target size". Checks `function-fit.md:240` (B8.1). |
| LAY-9 | `vault.space-emphasis` | NN/g, Gordon 2021: "Consider emphasizing the most important aspect of your design by giving it more space." NN/g, Harley 2020: the whitespace that makes a search function stand out. Checks `impeccable-checks.md:142`. |
| LAY-15 | `vault.heading-space` | USWDS Typography: "Use at least 1.5 times the amount of whitespace above the heading as below it." Butterick, "Space above and below": headings "relate to the text that follows"; the amount "is a judgment call". NN/g, Harley 2020: section text sits closer to its heading than to the section before. Checks `impeccable-checks.md:145`. |
| COL-3 | `vault.chart-contrast` | W3C Understanding SC 1.4.11: each line in a graph and the gridlines needed to read values take 3:1 against adjacent colours; lines "do not need to contrast with each other"; pie slices need 3:1 between them unless labels and values carry the data, and a border may supply it. |
| LAY-191 | `vault.table-markup` | WCAG technique H51: table markup with `table`, `tr`, `th` and `td`; its test checks tabular information for them. |
| NAV-253 | `vault.table-headers` | H51 as above. web.dev, Learn Accessibility, "Structure": "mark up header cells with" `th`; `scope` and `caption` for complex tables. GOV.UK Table: "Use the `scope` attribute". |
| NAV-268 | `vault.table-use` | web.dev "Structure": layout tables "must not use structural elements" and are hidden from assistive technology; still found in emails. GOV.UK Table: "Never use the table component to layout content on a page." |
| NAV-255 | `vault.table-print-header` | USWDS "Keep a record": "Print table headers on every page." CSS 2.1 §17.2: print user agents "may" repeat header rows. MDN `thead` does not say browsers repeat it. Measurement 2.1. |
| NEW3-32 | `vault.scroller-input` | Material 3 Inputs, the row's source, renders only by script and was not read; material-components-android `Carousel.md` says nothing on wheel input. NN/g, Pernice, "Carousel Usability" (2013, reviewed Aug 2026): "Ensure that navigation controls appear inside the carousel". Measurement 2.3. |
| LAY-36 | `vault.joined-fills` | Comeau, "Pride flags" (6 Jun 2023, updated 6 May 2025): fractional column widths leave gaps in Firefox and Safari, while "Chrome handles this gracefully"; his fix is whole-pixel columns. Measurement 2.2 finds Chromium does not, at fractional display scales. |
| LAY-65 | `vault.reflow` | MDN, Responsive design, "The viewport meta tag": without `width=device-width` a phone lays the page out about 980 px wide; "always include the viewport meta tag". check-layout.py already fails a phone viewport not at the phone's width (#229). |
| LAY-83 | `vault.safe-centre` | MDN Box alignment, "Overflow alignment": `safe` aligns to start when the item overflows, to avoid "data loss"; MDN `<overflow-position>`: with neither keyword the default is "a blend of `safe` and `unsafe`". Measurement 2.4. |
| PAG-4 | `vault.visual-order` | W3C Understanding SC 1.3.2 (level A): failure F1, positioning with CSS; technique C27, DOM order matching visual order. SC 2.4.3 (level A): failure F44, `tabindex`; "make sure the focus order reinforces the reading order". MDN Flexbox: with `order`, "the tabbing order remains the same as the code order". |

## 2. Measurements

Headless Chromium 149.0.7827.0 under Playwright for Python, on this machine (WSL2). Firefox and Safari were not run: Playwright's builds of them are not installed here. The scripts are on #278.

### 2.1 Printed table headers

A 200-row, two-column table printed to an A4 PDF with `page.pdf()`, its header row once in `thead` as `th` cells and once as a first row of `td` cells with no `thead`. Text read per page with pypdf.

| Header row | Pages | Pages showing it |
|---|---|---|
| in `thead` | 5 | 5 |
| first `td` row | 4 | 1 |

### 2.2 Seams between adjacent fills

Black flex columns (`flex: 1`, 40 px tall) on a white page, screenshot at each device scale, one pixel row read across the band; a seam is a non-black pixel between the first and last black ones. Each seam pixel read 47 or 63 of 255.

| Container width ÷ columns | 100% | 125% | 150% | 175% | 200% |
|---|---|---|---|---|---|
| 99 px ÷ 3 (33 px, whole) | 0 | 2 | 1 | 2 | 0 |
| 102 px ÷ 3 (34 px, whole) | 0 | 1 | 0 | 1 | 0 |
| 100 px ÷ 4 (25 px, whole) | 0 | 3 | 2 | 3 | 0 |
| 100.5 px ÷ 3 (33.5 px) | 0 | 2 | 1 | 2 | 0 |
| 101 px ÷ 3 (33.667 px) | 0 | 2 | 1 | 2 | 0 |

Whole CSS pixels avoid a seam only where width × scale is a whole number of device pixels. With the same black on the container as well, every case at 125%, 150% and 175% had none.

### 2.3 Wheel input on a horizontal scroller

A 300 px `overflow-x: auto` row of six 200 px blocks. Mouse placed over it, `mouse.wheel` sent once, `scrollLeft` read 400 ms later. Then a copy with a `wheel` listener calling `preventDefault()` (`passive: false`).

| Input | Native row | Wheel cancelled |
|---|---|---|
| sideways, deltaX 200 (a trackpad swipe) | 200 | 0 |
| vertical, deltaY 200 | 0 | 0 |
| Shift + vertical, deltaY 200 | 200 | 0 |

### 2.4 Centred overflow

A 300 px item in a 200 px `display: flex; overflow: auto` row. Item's left edge from `getBoundingClientRect()`: −50 px with `justify-content: center`, out of scroll reach; 0 with `safe center`.
