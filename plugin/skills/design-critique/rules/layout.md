# Rule records: layout

Where things sit on the page: reflow across widths and the first screen. The form is [rules.md](../rules.md)'s.

### vault.reflow
- applies-when: web-surface; the page at every width
- question: At every width, is there no sideways scroll, no text cut off at the screen's edge, and no text crossing other text or an image's edge or hidden under an image, and at phone widths does the viewport meta let a phone lay the page out at its own width and zoom it to 200%, save a fault the brief chose and names?
- answered-by: script
- writes: reflow
- yields-to: none
- source: WCAG 2.2 success criteria 1.4.10 Reflow, content at 320 px wide with no scrolling both ways and no loss, and 1.4.12 Text Spacing, no loss of content; the sweep holds every width from 320 to 1920 px, and 2560 px (design-vault#197), to them, stricter than 1.4.10's one width, by design-vault#78's option (A), and does not apply 1.4.12's spacing overrides (design-vault#183, #218); the viewport meta is judged as a phone reads it, for 1.4.10's 320 px, and its zoom limit by 1.4.4 Resize Text as W3C ACT rule b4f0c3 tests it, user-scalable=no or a maximum-scale under 2 failing (design-vault#229); MDN, Responsive design, "The viewport meta tag" (as read Oct 2026): without `width=device-width` a phone lays the page out about 980 px wide and shows it zoomed out; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: value
- script: check-layout.py
- reasons: design-round/SKILL.md#4-judging
- ledger: IMG-129, IMG-131, LAY-42, LAY-63, LAY-64, LAY-65, PAG-49, PAG-151, TXL-27, TYS-53
- status: live

### vault.layout
- applies-when: web-surface and has-cta; the call to action the brief names, at every width
- question: At every width, is the call to action the brief names wholly on the first screen?
- answered-by: script
- writes: first screen
- yields-to: level 2
- source: NN/g, "Scrolling and Attention" (2018); the width sweep is design-vault#78's, whose option (A) the founder accepted on the agent's recommendation; a call to action below the first screen at phone heights stays a failure, his ruling on design-vault#169 Q2 (A); strength: accepted agent recommendation, on NN/g, and founder ruling for phone heights
- era: timeless
- owner: vault
- stage: role
- target: Place the brief's call to action wholly on the first screen at every width.
- script: check-layout.py --cta <selector>
- reasons: design-critique/SKILL.md#2-the-added-lenses
- ledger: BTN-30, FRM-32, LAY-94, PAG-1, PAG-44, PAG-46
- status: live

### vault.weight-order
- applies-when: web-surface; every part of each view
- question: Ranked by visual weight at a squint, do the parts fall in the order of their task priority for this page?
- answered-by: whole-page
- writes: visual weight order
- yields-to: vault.primary-action
- source: Apple HIG and GOV.UK Button, on prominence by task priority; NN/g, "Imagery in Visual Design", on ranking images that inform above decorative ones; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Give each part visual weight in the order of its task priority for the page, the main action heaviest.
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: BTN-16, BTN-17, IMG-120, NEW3-75, PAG-68, TXL-90, TYF-68
- status: live

### vault.grouping
- applies-when: any; every group of related content
- question: Is related content grouped by space first, then a fill step, then a border, never by a shadow, with every border or divider grouping the parts as the spacing already does?
- answered-by: whole-page
- writes: grouping
- yields-to: none
- source: Gestalt proximity and common region, Wagemans et al. 2012, Palmer 1992; Polaris and Atlassian; strength: published research and design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Group by space first; add a fill step or a border only where space is short; never group with a shadow; where a line and the spacing disagree, fix the spacing.
- reasons: design-critique/references/surface-styling.md#dividers-against-space-and-fill
- ledger: FRM-5, FRM-6, IMG-122, LAY-6, SUR-8, SUR-10, SUR-39, SUR-40, SUR-42, SUR-76, SUR-77
- status: live

### vault.spacing-step
- applies-when: web-surface; every space, padding and gap
- question: Does every space, padding and gap come from the project's spacing scale, built on a 4 px step?
- answered-by: script
- writes: spacing step
- yields-to: level 2
- source: Material, Carbon and Atlassian spacing scales; strength: design-system guidance
- era: timeless
- owner: vault
- stage: value
- target: Take every space from one scale on a 4 px step.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: LAY-1, OTH-11
- status: live

### vault.breakpoints
- applies-when: web-surface; every breakpoint and every component that changes with width
- question: Does each breakpoint sit where the content breaks rather than at a device's width, with components sized by container queries?
- answered-by: whole-page
- writes: breakpoints
- yields-to: level 2
- source: web.dev Learn Design; Every Layout; strength: expert guidance
- era: dated 2027-10-14
- owner: vault
- stage: treatment
- target: Add a breakpoint where the layout breaks, and size components with container queries.
- reasons: design-round/references/impeccable.md#struck-or-corrected
- ledger: LAY-37, LAY-53, LAY-54, NEW2-73
- status: live

### vault.space-emphasis
- applies-when: web-surface; each view's most important part, as the function walk ranks it
- question: Does each view's most important part have more open space around it than the parts near it, the space adding to its size, weight and tone, save in a dense working view where those alone carry its rank?
- answered-by: whole-page
- writes: space around the most important part
- yields-to: vault.weight-order
- source: NN/g, Gordon, "Visual Hierarchy in UX: Definition" (2021): "Consider emphasizing the most important aspect of your design by giving it more space"; NN/g, Harley, "Proximity Principle in Visual Design" (2020), whitespace that makes a search box stand out; strength: domain evidence
- era: timeless
- owner: vault
- stage: role
- target: Give each view's most important part more open space than its neighbours, on top of its size, weight and tone; in a dense working view let those carry it.
- reasons: design-critique/references/layout-and-data.md#space-marks-the-most-important-part
- ledger: LAY-9
- status: live

### vault.visual-order
- applies-when: web-surface; every part a visitor reads or tabs to, at desktop and phone width
- question: Do the parts a visitor reads or tabs to appear in their source order, with no `order`, grid placement, `row-reverse`, absolute position or positive `tabindex` moving one out of its sequence?
- answered-by: script
- writes: visual order
- yields-to: none
- source: WCAG 2.2 success criteria 1.3.2 Meaningful Sequence (failure F1, technique C27, "Making the DOM order match the visual order") and 2.4.3 Focus Order (failure F44); MDN, Flexbox, "Ordering flex items" (as read Oct 2026): `order` leaves the tab order in source order; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Write the source in the order a visitor reads and tabs; move parts by changing the source, never by `order`, grid placement, reversed rows or a positive `tabindex`.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/layout-and-data.md#source-order-is-visual-order
- ledger: PAG-4
- status: staged

### vault.safe-centre
- applies-when: web-surface; centred content that can grow wider or taller than its box: a flex or grid row centring a fixed-size item at narrow widths
- question: Where centred content can outgrow its box, is it centred with `safe`, so the overflow falls past the end and none is cut off out of scroll reach at the start?
- answered-by: script
- writes: overflow alignment
- yields-to: none
- source: MDN, Box alignment, "Overflow alignment" (as read Oct 2026): `safe` aligns to start when the item overflows, "to avoid data loss"; measured on design-vault#278 (docs/research/layout-data-defaults.md): in Chromium 149 a 300 px item centred in a 200 px scrolling flex row began at −50 px, out of scroll reach, and at 0 with `safe center`; strength: web platform documentation and a measurement
- era: dated 2027-10-16
- owner: vault
- stage: treatment
- target: Centre content that may outgrow its box with `safe center`, never plain `center`.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/layout-and-data.md#safe-centring
- ledger: LAY-83
- status: live

### vault.scroller-input
- applies-when: web-surface; every horizontal scroller: a carousel, a row of cards, a wide table's scrolling box
- question: Is each horizontal scroller built on the browser's own overflow scrolling, with no script cancelling its wheel or touch events, so a trackpad's sideways swipe and Shift with a mouse wheel both move it, and does a carousel show its previous and next controls inside it for a mouse with only a vertical wheel?
- answered-by: script
- writes: scroller input
- yields-to: none
- source: measured on design-vault#278 (docs/research/layout-data-defaults.md): in Chromium 149 an `overflow-x: auto` row moved 200 px for a sideways wheel delta and for Shift with a vertical one, not at all for a plain vertical one, and not at all for any once a `wheel` listener called `preventDefault`, Firefox and Safari unmeasured; NN/g, Pernice, "Carousel Usability" (2013, reviewed Aug 2026): "Ensure that navigation controls appear inside the carousel"; strength: a measurement, and domain evidence for the controls
- era: dated 2027-10-16
- owner: vault
- stage: treatment
- target: Build a horizontal scroller on `overflow-x: auto` and never cancel its wheel or touch events; give a carousel previous and next controls inside it.
- script: check-state.py, its wheel line
- reasons: design-critique/references/layout-and-data.md#horizontal-scrollers
- ledger: NEW3-32
- status: live

### vault.one-site
- applies-when: web-surface; the whole site
- question: Does the site serve one responsive page on one URL to every device, with no separate mobile site or user-agent redirect?
- answered-by: script
- writes: site per device
- yields-to: level 2
- source: Google Search Central, "Mobile site and mobile-first indexing best practices" (updated 10 Dec 2025, as read Oct 2026): "Google recommends Responsive Web Design because it's the easiest design pattern to implement and maintain"; web.dev Learn Design, "Separate sites" (2021): a mobile subdomain means "two separate codebases and designs" and "there's no clear line between mobile and not-mobile"; strength: platform guidance
- era: timeless
- owner: vault
- stage: function
- target: Build one responsive site on one URL for every device; no m-dot subdomain and no redirect by user agent.
- script: check-cross.py <home page>
- reasons: design-critique/references/layout-and-data.md#one-site
- ledger: LAY-66
- status: live

### vault.false-floor
- applies-when: web-surface; a page longer than one screen, at every width
- question: Does the first screen show the visitor that more lies below, by content cut off at its foot or a part of the next section in view, rather than ending on a full-height band that looks finished?
- answered-by: script
- writes: fold cue
- yields-to: none
- source: NN/g, Fessenden, "Scrolling and Attention" (15 Apr 2018, as read Oct 2026): "Beware of false floors, which are increasingly common with modern minimalist designs" and "Include signifiers (such as cut-off text) to tell people that there is content below the fold"; Apple HIG Scroll views (as read Oct 2026): "displaying partial content at the edge of a view indicates that there's more content in that direction"; strength: domain evidence
- era: timeless
- owner: vault
- stage: role
- target: Let the first screen end mid-content, with the next section's top or cut-off text in view, at every width; never size a hero to end exactly at the screen's foot with nothing below it showing.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/layout-and-data.md#no-false-floor
- ledger: LAY-93
- status: staged

### vault.native-scroll
- applies-when: web-surface; every page and scroll container
- question: Does the page keep the browser's own scroll speed and direction, with no script that cancels wheel, touch or key scrolling to drive the page itself?
- answered-by: script
- writes: scroll rate
- yields-to: none
- source: NN/g, Paul, "Scrolljacking 101" (6 Aug 2023, as read Oct 2026): scrolljacking "changes the speed and, sometimes, the direction of scrolling", "Users expect a consistent scroll rate", and it "leads to more user pain than benefits"; Apple HIG Scroll views (as read Oct 2026): "Support default scrolling gestures and keyboard shortcuts"; strength: domain evidence
- era: timeless
- owner: vault
- stage: function
- target: Leave scrolling to the browser: no smooth-scroll library, no `wheel` or `touchmove` handler that calls `preventDefault()` to move the page, no scroll that changes direction; animate content on scroll only by scroll-driven animation that leaves the rate alone.
- script: check-flow.py <page> --out <dir> --records [--parts <declaration>]
- reasons: design-critique/references/page-behaviour.md#native-scrolling
- ledger: LAY-116
- status: live

### vault.top-tasks
- applies-when: web-surface; a site's homepage
- question: Does the homepage give a clear starting point for each of the visitor's main tasks, about one to four, ranked by prominence and named in the visitor's words, rather than one action alone where visitors come for several?
- answered-by: whole-page
- writes: homepage task entry points
- yields-to: vault.primary-action
- source: NN/g, Nielsen, "Top 10 Guidelines for Homepage Usability" (2002), guideline 4: "clear starting points for the main 1–4 tasks they'll undertake when visiting your site"; McGovern, "What Really Matters: Focusing on Top Tasks", A List Apart (2015): top tasks are "usually less than 10, often less than five"; strength: domain evidence
- era: timeless
- owner: vault
- stage: function
- target: On the homepage give each of the visitor's top tasks, one to four, a clear starting point in their words, the first as the main action and the rest quieter.
- reasons: design-critique/references/house-principles.md#top-tasks-on-the-homepage
- ledger: PAG-56
- status: live

### vault.content-width
- applies-when: web-surface; the page's content container, and each container whose width a role below sets
- question: At wide viewports, is each content container capped at the maximum width its role gives: a reading page's about 864 px, a default page's about 1020–1300 px, a canvas or board uncapped, stacked footer bands one shared width, an empty state's text 304–464 px?
- answered-by: script
- writes: content max-width
- yields-to: level 2
- source: Atlassian Design System, "Grid" (as read Oct 2026): "Fixed-wide has a maximum width of 1296px (including margins). Use this as the default", for "Dashboards, directories, search results"; "Fixed-narrow has a maximum width of 864px (including margins). Use this for long-form content such as blogs and articles"; fluid, "No maximum", for "Kanban boards, whiteboards", and "Use sparingly"; GOV.UK Design System, "Layout": "The default maximum page width is 1020px", main content "always be in a two-thirds column"; USWDS layout grid (updated Nov 2024): `grid-container` "maximum width of desktop (1024px)"; USWDS identifier (updated Nov 2024): "Use the same max-width as your site footer"; Atlassian, Empty state usage (as read Oct 2026): text "464px", narrow "304px"; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: role
- inputs: the container's role (reading page, default page or app view, canvas or board, footer band, empty state), the viewport width
- output: reading page (articles, docs, blog): 864 px at most, margins included, or the main text in a two-thirds column (2/3) of a wider page; default page (dashboard, directory, search results, and any page no other role names): 1020–1300 px, margins included; canvas or board: no cap; each stacked footer band (footer, identifier, sub-footer): the site footer's one max-width; empty state text: 464 px, or 304 px in a container narrower than 464 px
- target: Cap each container by its role: about 864 px for a reading page, 1020–1300 px for the default page, none for a canvas; give every footer band the footer's one max-width and an empty state's text 464 px (304 px in a narrow container).
- script: check-layout.py <page> --out <dir> --records --parts <declaration> [--brief page=<reading, default or canvas>]
- reasons: design-critique/references/alignment-and-width.md#content-width-by-role
- ledger: LAY-43, LAY-45, LAY-49
- status: staged

### vault.capped-centre
- applies-when: web-surface; the page's width-capped content container, the one `vault.content-width` caps, in a wider viewport; not a text column inside it, which `vault.alignment-lines` places
- question: Where the viewport is wider than a capped container, does the container sit centred, its left and right gaps equal?
- answered-by: script
- writes: capped container placement
- yields-to: level 2
- source: Atlassian Design System, "Grid" (as read Oct 2026): "Fixed grids have a maximum width and sit centered in the main content area"; USWDS layout grid (updated Nov 2024): "grid-container centers the container"; govuk-frontend `_width-container.scss` (main, read Oct 2026): "just centre the content", `margin-left: auto`, `margin-right: auto`; MDN, Box alignment in block layout (modified Nov 2025): auto side margins "push a block into the center"; Apple HIG, Layout (updated Sep 2026), for visionOS windows: "keep content horizontally centered at very large sizes"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Centre each capped container with `margin-inline: auto`.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/alignment-and-width.md#capped-blocks-sit-centred
- ledger: LAY-44
- status: staged

### vault.alignment-lines
- applies-when: web-surface; every top-level content container (text block, card, image, table, form) in a CSS grid of the main content area, and each section's main text edge; a container placed without a CSS grid is `vault.alignment-lines-look`'s
- question: Does each top-level content container in the main content's CSS grid start and end on one of its column lines, never in a gutter or margin, with the main text edge on one line in every section of a column, sections set side by side each keeping their own column's line, but a full-bleed part (header, hero, image band) or a centred section?
- answered-by: script
- writes: grid alignment
- yields-to: level 2
- source: Atlassian Design System, "Grid" (as read Oct 2026): "align content containers to the grid columns. Examples include cards, images, text blocks, tables, and forms", "Only top-level containers need to align to the grid", "Small elements, like buttons and icons, do not need to align", "Don't allow content to overflow into gutters or margins"; NN/g, "Why Does a Design Look Good?" (2021, modified Nov 2025): "keep alignment consistent across your different pages and elements. Any alignment inconsistencies should be purposeful"; Wagemans et al. 2012, Psychological Bulletin 138(6), good continuation and parallelism among the classical grouping principles; Butterick, Practical Typography, "Grids": "Not everything needs to go on the grid", "the eye must always be the final judge"; the main text edge repeating between sections is the house's reading of NN/g's consistency line, which no source read states for sections; strength: design-system guidance on a peer-reviewed grouping principle, with a house application
- era: timeless
- owner: vault
- stage: treatment
- target: Lay the main content on one column grid: each text block, card, image, table and form starts and ends on its column lines, and the main text edge stays on one line through every section of a column.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/alignment-and-width.md#alignment-lines-between-sections
- ledger: LAY-24
- status: staged

### vault.alignment-lines-look
- applies-when: web-surface; every top-level content container (text block, card, image, table, form) in the main content area that no CSS grid places
- question: Where the main content is laid on columns with no CSS grid, does each top-level content container start and end on a shared column line, never in a gutter or margin?
- answered-by: look
- writes: grid alignment without a CSS grid
- yields-to: vault.alignment-lines, level 2
- source: Atlassian Design System, "Grid" (as read Oct 2026): "align content containers to the grid columns. Examples include cards, images, text blocks, tables, and forms", "Only top-level containers need to align to the grid", "Don't allow content to overflow into gutters or margins"; Butterick, Practical Typography, "Grids": "the eye must always be the final judge"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Where the page's columns come from flex, widths or margins rather than a CSS grid, start and end each top-level container on one of those shared column lines.
- reasons: design-critique/references/alignment-and-width.md#alignment-lines-between-sections
- ledger: LAY-24
- status: staged

### vault.alignment-break
- applies-when: web-surface; a full-bleed part or centred section among sections that share the page's alignment lines
- question: Does each part or section that leaves the page's shared alignment lines show why it does: it leads the page, sets one block apart, or is an image band?
- answered-by: look
- writes: grid break
- yields-to: vault.alignment-lines
- source: NN/g, "Using Grids in Interface Designs" (2022, modified Jun 2025): "It is okay to break the grid every so often, as long as you have a valid reason for it", and "Breaking the grid produces a chaotic browsing experience"; NN/g, "Why Does a Design Look Good?" (2021, modified Nov 2025): "Any alignment inconsistencies should be purposeful"; Atlassian Design System, "Grid" (as read Oct 2026): headers "may break out of the grid to span across the page"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Break the page's alignment lines only where the break carries meaning: the leading part, a block set apart, an image band.
- reasons: design-critique/references/alignment-and-width.md#alignment-lines-between-sections
- ledger: LAY-24
- status: staged

### vault.optical-alignment
- applies-when: web-surface; text inside an unpainted padded column beside an unpadded one; not an icon beside text, which `vault.optical-icon` judges
- question: Where a padded column's text sits beside an unpadded neighbour's, is the text aligned with the neighbour's text, not the column's box with its box?
- answered-by: script
- writes: optical alignment
- yields-to: level 2
- source: Wathan and Schoger, Refactoring UI, "Redesigning Laravel.io" (Oct 2017), a sidebar button aligned to the top of a padded list's box "feels a bit 'off'", moved down to the list's content; Krehel, "Optical Alignment" (jakub.kr, archived Oct 2025): "there are instances where it just looks off. When that happens, it is best to align items optically instead", less padding on a button's icon side; Butterick, Practical Typography, "Grids": "the eye must always be the final judge"; impeccable 4.5.0, layout.md: "Make optical corrections only after inspecting the rendered result"; strength: expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Line up a padded column's text with its neighbour's text, not its box with the neighbour's box.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/alignment-and-width.md#optical-alignment
- ledger: LAY-88
- status: staged

### vault.optical-icon
- applies-when: web-surface; an icon beside text: in a button, a link, a list item or a label
- question: Does each icon beside text look aligned with it, its drawn shape centred on the text's line and balanced in its box, the padding on a button's icon side trimmed, rather than aligned by its box alone?
- answered-by: look
- writes: optical alignment of icons
- yields-to: vault.optical-alignment, level 2
- source: Krehel, "Optical Alignment" (jakub.kr, archived Oct 2025): "there are instances where it just looks off. When that happens, it is best to align items optically instead", less padding on a button's icon side; Butterick, Practical Typography, "Grids": "the eye must always be the final judge"; impeccable 4.5.0, layout.md: "Make optical corrections only after inspecting the rendered result"; strength: expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Trim the padding on a button's icon side and fix an icon's drawn offset in the SVG so it sits centred on its text; check it on the render.
- parts: icon
- reasons: design-critique/references/alignment-and-width.md#optical-alignment
- ledger: LAY-88
- status: staged

### vault.tone-space
- applies-when: any; the whole asset, every view, against the tone the brief or direction card states in its tone line
- question: Does the amount of white space match the stated energy and order, more for a calmer or more ordered tone and less for a louder one, without so much that the page looks empty of content or so little that it looks disorganised, with a working view's information density left to vault.busy-density?
- answered-by: whole-page
- writes: amount of white space
- yields-to: vault.space-emphasis, vault.brand-layer, vault.busy-density, level 2
- source: Tuch et al. 2012, IJHCS 70(11), low complexity liked within 50 ms; Reinecke and Gajos, CHI 2014, complexity's cost past its peak; CXL, "Visual hierarchy" (updated Dec 2022), too much and too little white space; Ström-Awn, "UI density" (20 May 2024); Pracejus, O'Guinn and Olsen 2013, IJRM 30(3), white space meanings differing across cultures; strength: published research and expert guidance
- era: timeless
- owner: vault
- stage: treatment
- inputs: the stated energy (calm, middle, loud); the stated order (ordered, middle, rich); the visitor mode (operate or read, persuade or experience)
- output: the more open of the energy and order positions wins: calm or ordered, generous space between groups and around the leading part; loud or rich, tighter space and more parts a screen; middle, between; every tone stops short of a page that looks empty of content
- target: Give a calmer or more ordered tone more white space and a louder one less.
- reasons: design-critique/references/tone.md#white-space
- ledger: LAY-4
- status: live

### vault.tone-symmetry
- applies-when: any; the layout of each view and of each text block, against the tone the brief or direction card states in its tone line
- question: Does the layout's symmetry match the stated tone, symmetric for a stable, quiet one and asymmetric for an energetic one, with any asymmetry balanced by weight and plain enough to read as chosen?
- answered-by: whole-page
- writes: symmetry
- yields-to: vault.brand-layer, level 2
- source: NN/g, "5 Principles of Visual Design in UX" (Mar 2020), asymmetry dynamic and symmetry "quiet and static"; Wu 2025, PLoS ONE 20(1) e0317229, symmetric logos raising perceived quality through stability under low load; Butterick, Practical Typography, "Page margins", asymmetry made obvious; strength: published research and expert guidance
- era: timeless
- owner: vault
- stage: role
- target: Lay a stable, quiet tone out symmetrically and an energetic one asymmetrically, balancing an asymmetric layout by weight and making its offset plainly deliberate.
- reasons: design-critique/references/tone.md#symmetry
- ledger: LAY-27
- status: live

### vault.panes-by-width
- applies-when: web-surface; the page's top-level regions (header, navigation, main content, supporting or detail panes, footer) at each width the round renders
- question: As the window narrows, does the page restructure its regions rather than show a scaled-down copy of its wide layout, with the side-by-side panes its window allows: one pane under 840 px wide or under 480 px tall (a list or its detail, the main content with its supporting pane moved by `vault.side-pane`), and up to two from 840 px, the main pane about 70% and a supporting pane about 30%?
- answered-by: script
- writes: pane count and region placement by width
- yields-to: vault.reflow, level 2
- source: Android Developers, "Use window size classes" (as read Nov 2026; no page date): compact "width < 600dp", medium "600dp ≤ width < 840dp", expanded "840dp ≤ width < 1200dp"; "Use window size classes to make high-level application layout decisions"; compact height "height < 480dp", "99.78% of phones in landscape"; a landscape phone's "window height is compact, in which case two pane layouts are not practical"; Android Developers, "Adaptive apps" overview (as read Nov 2026): "On compact and medium window size classes, apps display a single pane", two panes in expanded; "Canonical layouts" (as read Nov 2026): list-detail "Medium- and compact-width displays show either the list or the detail"; supporting pane "For expanded width, give 70% of the space to the main content, 30% to the supporting content"; Apple HIG, Layout (updated 9 Sep 2026): "Determine layout based on size classes, not device type or orientation"; Apple HIG, Split views (updated 9 Jun 2025): "it's difficult to display multiple panes without wrapping or truncating the content"; web.dev Learn Design, "Macro layouts" (as read Nov 2026): header, main and footer in that order, `main` alone made a two-column grid at a breakpoint; strength: platform guidance
- era: dated 2027-11-13
- owner: vault
- stage: role
- inputs: viewport width, viewport height, the page's pattern (list-detail, main with supporting pane, single pane), each pane's minimum content width
- output: width < 840 px or height < 480 px: one pane; list-detail shows the list, then the detail in its place; main with supporting pane shows the main pane and hands the supporting pane to `vault.side-pane`; width ≥ 840 px and height ≥ 480 px: list-detail shows both side by side, main with supporting pane splits about 70/30, each only where both panes keep their minimum content width, else one pane; a single-pane page keeps one pane at every width; at every width the header spans the top and the footer the bottom, the panes between them
- target: Restructure by window width: one pane under 840 px wide or 480 px tall, two side by side from 840 px (main about 70%, supporting about 30%), never a zoomed-out copy of the wide layout.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#panes-by-window-width
- ledger: LAY-38, LAY-59, PAG-28
- status: staged
### vault.pane-split
- applies-when: web-surface; a page whose main and supporting panes sit side by side, at each width from 840 px the round renders
- question: Where two panes sit side by side, does the main pane take about 70% and the supporting pane about 30%, and does each keep its minimum content width, the page showing one pane wherever both cannot?
- answered-by: look
- writes: pane split
- yields-to: vault.panes-by-width, level 2
- source: Android Developers, "Canonical layouts" (as read Nov 2026): supporting pane "For expanded width, give 70% of the space to the main content, 30% to the supporting content"; Apple HIG, Split views (updated 9 Jun 2025): "it's difficult to display multiple panes without wrapping or truncating the content"; strength: platform guidance
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Split side-by-side panes about 70/30, main first, and fall to one pane wherever either would drop below its minimum content width.
- reasons: design-critique/references/responsive-structure.md#panes-by-window-width
- ledger: PAG-28
- status: staged

### vault.content-columns
- applies-when: web-surface; every grid of like items (cards, tiles, a feed, a product or category grid); not the page's main and side columns, which `vault.panes-by-width` and `vault.pane-split` place
- question: Does each grid of like items take as many columns as fit its items' minimum width, fluidly or by breakpoints set where its content breaks, falling to one column of cards at phone width and two of category tiles, one where two would cut a tile's label?
- answered-by: script
- writes: content column count by width
- yields-to: level 2
- source: MDN, CSS grid layout, "As many columns as will fit" (modified 20 Jul 2026): "create as many columns as will fit into the container", `repeat(auto-fit, minmax(230px, 1fr))`; web.dev Learn Design, "Macro layouts" (as read Nov 2026): "You might not always need to use a media query", cards via `repeat(auto-fill, minmax(15em, 1fr))`; "This single column default ordering is what smaller screens will get"; Android Developers, "Canonical layouts", Feed (as read Nov 2026): "The grid then displays as many columns as can fit in the available space", `GridCells.Adaptive(minSize = 180.dp)`; MDN, Media queries (modified 4 Sep 2026): mobile first, "a simple single column of content", "change the design at the size where the content starts to break"; Baymard, "Ecommerce Category Page" (17 Apr 2026): "Subcategory tiles adapt to a two-column or single-column layout", "On mobile, a large desktop tile grid will typically reflow to two columns"; one column where two would cut a tile's label is the house's; strength: platform guidance and domain evidence
- era: dated 2027-11-13
- owner: vault
- stage: role
- inputs: the container's width, the item kind, the item's minimum width, the gap
- output: columns = max(1, floor((container width + gap) ÷ (item minimum width + gap))); item minimum width: a card about 15em, a feed tile about 180 px, unless the project sets its own; category or subcategory tiles at phone width (under 600 px): 2 columns, or 1 where 2 would cut a tile's label
- target: Lay item grids out with `repeat(auto-fill, minmax(<item min>, 1fr))` or breakpoints where the content breaks: one column of cards and two of category tiles on a phone.
- script: check-layout.py <page> --out <dir> --records --parts <declaration>
- reasons: design-critique/references/responsive-structure.md#columns-by-width
- ledger: LAY-37, LAY-60, LAY-61
- status: staged

### vault.side-pane
- applies-when: web-surface; each supporting or side pane (filters, details, a table of contents, a tool panel) at a width `vault.panes-by-width` gives one pane
- question: Where a side pane no longer fits beside the main content, does it move below the main content or into a sheet or overlay opened by a labelled control, rather than being squeezed beside the main content or dropped with no way to reach it?
- answered-by: script
- writes: side pane behaviour at narrow widths
- yields-to: vault.nav-by-width, level 2
- source: Android Developers, "Canonical layouts", Supporting pane (as read Nov 2026): "For compact-width displays, place the supporting content below the main content or inside a bottom sheet"; it "can be initially hidden in a bottom or side sheet accessible by means of a control such as a menu or button"; Atlassian Design System, Layout usage (as read Nov 2026): "On small viewports (1024px and below), the panel becomes an overlay"; Apple HIG, Split views (updated 9 Jun 2025): "ensure that it's possible to navigate between the various panes in a logical way"; strength: platform and design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: When a side pane cannot sit beside the main content, put it below the main content if it is read in flow, or in a sheet or overlay behind a labelled button if it is a tool.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#side-panes-move-below-or-into-a-sheet
- ledger: LAY-62, PAG-2
- status: staged

### vault.stack-order
- applies-when: web-surface; the page at each width where it falls to one column, at phone width and at 200% text
- question: When the page falls to one column, do its parts come in the page's priority order (the brief's ranking of the visitor's tasks, the main content before its supporting pane), with no group's members pushed apart by the stacking?
- answered-by: look
- writes: one-column part order
- yields-to: vault.side-pane, vault.visual-order, level 2
- source: Sparkbox, "Content Priority Guide" (dated 11-11-13, read as 13 Nov 2011 or 11 Nov 2013; as read Nov 2026): it "puts them all in their priority order using only text", saying nothing of small screens, so taking its order as the one-column order is the house's; web.dev Learn Design, "Macro layouts" (as read Nov 2026): "This single column default ordering is what smaller screens will get"; MDN, Media queries (modified 4 Sep 2026): "order your source well and you will have a readable layout by default"; NN/g, "Proximity Principle in Visual Design" (2 Aug 2020): groupings "may change as they adapt to varying screen sizes", stacking "can push elements farther apart, destroying grouping relationships"; Apple HIG, Typography (16 Dec 2025): "keep primary elements toward the top of a view even when the font size is very large"; strength: expert and platform guidance, with a house link from priority to stacking order
- era: timeless
- owner: vault
- stage: function
- target: Write the source in the page's priority order, main content before its supporting pane, so the one-column page reads in that order and each group stays together.
- reasons: design-critique/references/responsive-structure.md#one-column-order
- ledger: PAG-2
- status: staged

### vault.component-swap
- applies-when: web-surface; each part that changes component as the window narrows or widens
- question: Where a part changes component with width, is it swapped only for one doing the same job with the same items in the same order: a bottom navigation bar for a rail, tabs for stacked sections, a wide table for stacked rows, a side pane for a sheet?
- answered-by: look
- writes: component swap by width
- yields-to: vault.popover-sheet, vault.nav-by-width, vault.tabs-narrow, vault.table-narrow, vault.side-pane, level 2
- source: Android Developers, "Adaptive apps" overview (as read Nov 2026): "adaptive apps replace layout components and show or hide content", "a bottom navigation bar, but on large screens, a navigation rail"; GOV.UK Design System, Tabs (changed Aug 2024): on small screens the tabbed content shows "on a single page, in order from first to last"; the same items in the same order is the house's (#208's research question 8); strength: platform guidance with a house condition
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Swap a part for another only where both do the same job: a bottom bar for a rail, tabs for stacked sections, a popover for a sheet; keep the same items and the same order.
- reasons: design-critique/references/responsive-structure.md#swap-parts-only-for-the-same-job
- ledger: LAY-67
- status: staged

### vault.row-wrap
- applies-when: web-surface; every row of inline items (tags, chips, links, metadata items, buttons other than a button group) that may not fit one line
- question: Does each row of inline items that cannot fit one line wrap onto new lines, never overflowing its container or squeezing items below their content's width, save a row `vault.nav-strip` or `vault.scroller-input` makes a one-line scroller?
- answered-by: script
- writes: inline row wrapping
- yields-to: vault.nav-strip, vault.button-group-stack, level 2
- source: MDN, Flexbox, "Wrapping" (modified 14 Jul 2026): without it "your flexbox children will overflow their container, breaking the layout"; with `flex-wrap: wrap` "Any overflow is moved down to the next line"; web.dev Learn CSS, Flexbox (as read Nov 2026): "The initial value of the `flex-wrap` property is `nowrap`"; strength: platform documentation
- era: timeless
- owner: vault
- stage: treatment
- target: Give every row of inline items `flex-wrap: wrap` (or a wrapping grid), so items drop to a new line rather than overflow or shrink.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#rows-wrap
- ledger: NEW3-72
- status: staged

### vault.label-value-stack
- applies-when: web-surface; every label beside its value (a definition or metadata list, a key-value row, a price beside its label) and every text beside a secondary item (an icon, a timestamp)
- question: Where a label sits beside its value, or text beside a secondary item, does the value or item move below the label when the container is narrower than both need or the text is enlarged to 200%, rather than either being cut off or overlapping?
- answered-by: script
- writes: inline or stacked label-value layout
- yields-to: level 2
- source: Josh W. Comeau, "Container Queries Unleashed" (27 Jan 2025): "show the key/value pairs in a single row. Otherwise, the values should move to a new line", by `@container (min-width: 19rem)`; Apple HIG, Typography, Supporting Dynamic Type (16 Dec 2025): inline items "can crowd text and cause truncation or overlapping", "consider using a stacked layout where text appears above secondary items"; WCAG 2.2 SC 1.4.4 Resize Text, 200% with no loss of content; strength: expert and platform guidance, on WCAG 2.2 AA's no-loss floor
- era: timeless
- owner: vault
- stage: treatment
- target: Let a value drop below its label by a container query (or a wrapping flex row) once the pair no longer fits one line or the text is enlarged.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#label-and-value-stack
- ledger: NEW3-70
- status: staged

### vault.popover-sheet
- applies-when: web-surface; each popover, and each menu opened as a popover, at widths under 600 px
- question: Under 600 px wide, does each popover, a menu opened as one included, open as a bottom or full-screen sheet rather than a floating box?
- answered-by: script
- writes: popover form at compact widths
- yields-to: level 2
- source: Apple HIG, Popovers, iOS and iPadOS (as read Nov 2026): "Avoid displaying popovers in compact views", "Reserve popovers for wide views", "presenting information in a full-screen modal view like a sheet"; impeccable 4.5.0 adapt.md:48: "Bottom sheets instead of dropdowns", the one source read that names menus; Android Developers, "Use window size classes" (as read Nov 2026): compact "width < 600dp", the bound the house gives Apple's "compact views"; Material 3's menu guidance renders by script alone and was not read; strength: platform guidance, with a house width bound
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Under 600 px, open popovers and popover menus as a bottom or full-screen sheet.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#popovers-become-sheets
- ledger: LAY-68
- status: staged

### vault.grid-ornament
- applies-when: web-surface; every visible page frame, column rule, grid line or crosshair mark
- question: Is a visible page frame, grid line or crosshair mark the site's own signature, drawn in vault.border-roles' decorative edge and held at one position on every page, rather than a default ornament or the broadsheet-hairline look, and kept off working areas?
- answered-by: look
- writes: grid ornament
- yields-to: vault.brand-layer, vault.ai-look, vault.decoration-place
- source: Rauno Freiberg, "What will you ship?" (the Vercel homepage, October 2023), "showing a literal frame on every page", "a consistent grid position across all pages", crosshairs "to help guide the eye at certain points"; impeccable 4.5.0 `new-work.md`, generated interfaces clustering on "broadsheet-editorial hairlines", and engine 0.1.11 rule codex-grid-background; strength: expert writing and impeccable "AI look" ban
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Draw a page frame, grid lines or crosshairs only as the site's signature move, in the decorative edge vault.border-roles sets, at the same position on every page, and never over a working area.
- reasons: design-critique/references/grounds-and-gradients.md#page-frames-and-grid-marks
- ledger: LAY-34
- status: staged

### vault.busy-cues
- applies-when: any; the whole asset, every view
- question: Does the squint test still show the primary part, the secondary part and the main groups in order, with no clutter source (a redundant link or item, a decorative icon or type flourish, an over-detailed or watermark image) beside them, few text groups and image areas for what the view must say, and borders, backgrounds and shadows used sparingly rather than to make up for weak spacing?
- answered-by: whole-page
- writes: visual complexity
- yields-to: vault.element-count, vault.busy-density, level 2
- source: Reinecke et al., CHI 2013, 450 sites and 548 people, perceived complexity R2 .65 from non-text area (β .515), text area (.407), text groups (.344) and image areas (.193), colour .079, symmetry and balance pruned; NN/g, Fessenden, "Aesthetic and Minimalist Design" (2021), "Every extra unit of information … competes"; NN/g, Nielsen, homepage guidelines 18, 46, 58 and 59 (2001), redundant items, decorative icons, detailed and watermark images "clutter the page"; NN/g, Whitenton, "Minimize Cognitive Load" (2013), "meaningless typography flourishes"; NN/g, Gordon, "Visual Hierarchy in UX" (2021), borders or backgrounds "can create visual clutter, so use them sparingly"; Polaris, Creating depth (2024), overused shadows "look cluttered"; impeccable 4.5.0 layout.md, the squint test (as read Nov 2026); strength: published research and expert guidance
- era: timeless
- owner: vault
- stage: role
- target: Cut what does not help the visitor's task, group by space before boxes, keep borders, fills and shadows few, and check that the squint test still shows the lead, the second part and the groups.
- reasons: design-critique/references/busyness.md#what-makes-a-page-busy
- ledger: LAY-5
- status: live

### vault.busy-density
- applies-when: web-surface; the whole page, every view, against its visitor mode and audience
- question: Does each view carry as much information per screen as its visitor mode and audience need, dense for a working view of lists, tables or long forms used by repeat, skilled people, lower in complexity for a page judged at first sight, and never so sparse that content spreads across many screens or a gap looks like the end of the page?
- answered-by: whole-page
- writes: information density
- yields-to: vault.element-count, vault.top-tasks, level 2
- source: Polaris, Density (2024), "The admin is high density by default", low density for "focused editing interfaces"; @material/density 14.0.0 README, high density "when it improves the user experience", for "List, tables, and long forms"; Ström-Awn, "UI density" (undated page, as read Nov 2026), value over time and space; Reinecke et al., CHI 2013, appeal falls strongly at high complexity and slightly at low, and people over 45 like low complexity more; NN/g, Flaherty, Neusesser and Chitale, "content dispersion" (13 Oct 2023), "a clear preference for a condensed layout"; NN/g, Fessenden, "Scrolling and Attention" (2018), 57% of viewing time above the fold and pages "too sparse"; NN/g, Moran (2017), flat signifiers only at low information density; NN/g, Cheng and Nielsen (2016, 12 users), Chinese users prefer "fairly high information density"; web.dev, Learn Accessibility, "Why" (as read Nov 2026), "Busy interfaces" and "big walls of words with little whitespace" as cognitive barriers; the one-step moves for age and culture are the house's; strength: design-system guidance and published research
- era: dated 2027-11-13
- owner: vault
- stage: function
- inputs: the visitor mode (operate, persuade or experience, read); whether the view serves repeat, skilled people; the content type (list, table, long form, editing view, marketing section, long text); the audience's age and culture where the brief states them; the signifier strength (strong edges and fills, or flat)
- output: operate with repeat, skilled people and a list, table or long form: high density, one density held within a component, sections parted by dividers or muted surfaces; operate on a focused editing view: low density, larger targets; persuade or experience: low to moderate complexity, the priority content and main action in the first screen; read: text in paragraphs with white space and nothing competing beside it; an audience stated as over 45 moves one step lower and one whose culture prefers dense pages may go one step higher; flat signifiers only at low density
- target: Set each view's density by its visitor mode: dense and steady for repeat users of lists, tables and long forms, lower for a page judged at first sight, and never so sparse that the content scatters across screens.
- reasons: design-critique/references/busyness.md#how-busy-for-which-visitor
- ledger: LAY-5
- status: live
