# Rule records: navigation

Finding the way: the header, nav bars, menus and links that take a visitor somewhere. The form is [rules.md](../rules.md)'s.

### vault.carry-navigate
- applies-when: web-surface; every link and navigation item, the current page's item included
- question: Does each link show that it takes the visitor somewhere by its context's carrier (in prose, the cue `vault.colour-script` measures; in navigation, its place, as in a link list or a card that is one target; a chevron or arrow where its text is not plainly a link), does the current page's item carry a cue besides colour, and do the link colour and underline mark nothing but links?
- answered-by: whole-page
- writes: navigate signifier
- yields-to: vault.colour-script, vault.borrowing
- source: NN/g, "Beyond Blue Links" (2015); W3C Understanding SC 1.4.1 and technique G183 (WCAG 2.2, 2023); NN/g, "Clickable Elements", on arrows and chevrons; GOV.UK Design System links; #127 B7.2's carrier table; strength: domain evidence
- era: dated 2027-10-14
- owner: vault
- stage: role
- target: Mark prose links by an underline, nav and list links by their place, and a link whose text is not plainly one by a chevron or arrow; mark the current page by more than colour; keep the link colour and the underline off headings, labels, status text and emphasis.
- reasons: design-critique/references/house-principles.md#carriers-and-reserved-properties
- ledger: BTN-13, BTN-63, BTN-64, COL-20, COL-22, COL-76, FCH-27, IMG-35, IMG-186, NAV-158, OTH-9, OTH-20, TXL-1, TXL-2, TXL-3, TXL-7, TYF-57
- status: live

### vault.visible-nav
- applies-when: web-surface; the main navigation at phone width
- question: At phone width, do four main navigation links or fewer stay in view, a menu hiding them only where there are more than four?
- answered-by: whole-page
- writes: phone navigation
- yields-to: none
- source: NN/g 2016, "Hamburger Menus and Hidden Navigation Hurt UX Metrics"; strength: domain evidence
- era: dated 2027-10-14
- owner: vault
- stage: role
- target: Keep up to four main links in view on a phone; put them behind a menu only past four.
- reasons: design-round/references/impeccable.md#conditions-added
- ledger: LAY-70, NAV-169, NAV-211, NAV-212
- status: live

### vault.exit-warning
- applies-when: web-surface; every link or button that takes the visitor to another site
- question: Does each link that leaves the site go there with no warning modal or interstitial, save the one handover notice a project's rules file keeps for a task finished on another business's site?
- answered-by: script
- writes: leaving-site warning
- yields-to: level 2
- source: USWDS, Link, "What you shouldn't do" (as read Oct 2026): "Don't block external links with disruptive notifications", "Roadblock notices, such as modals and dialog boxes, result in a poor user experience", and "communicate about a link's destination through descriptive link text and external link indicators"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Let external links leave directly, named by their text and an external-link indicator; add a handover notice only where the project's rules file keeps one.
- script: check-state.py, its exit line
- reasons: design-critique/references/interaction-and-forms.md#leaving-the-site-is-not-interrupted
- ledger: NAV-140
- status: staged

### vault.exit-warning-look
- applies-when: web-surface; every link or button that takes the visitor to another site
- question: Does each link that leaves the site tell its destination by its link text and an external-link indicator?
- answered-by: look
- writes: leaving-site link text
- yields-to: vault.exit-warning
- source: USWDS, Link, "What you shouldn't do" (as read Oct 2026): "Don't block external links with disruptive notifications", "Roadblock notices, such as modals and dialog boxes, result in a poor user experience", and "communicate about a link's destination through descriptive link text and external link indicators"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Name an external link's destination in its text and mark it with an external-link indicator.
- reasons: design-critique/references/interaction-and-forms.md#leaving-the-site-is-not-interrupted
- ledger: NAV-140
- status: staged

### vault.nav-by-width
- applies-when: web-surface; the main navigation, at each window width the round renders
- question: Does the main navigation take its form from the window's width, under 600 px an app's top-level destinations in a bar along the bottom and a site's in the top header as `vault.visible-nav` sets, from 600 px an app's in a rail beside the content and a site's in the header bar, rather than one form at every width?
- answered-by: script
- writes: navigation form and place by width
- yields-to: vault.visible-nav, level 2
- source: Android Developers, "Use window size classes" (updated 22 Sep 2026, as read Oct 2026): compact width "< 600dp", "99.96% of phones in portrait"; Android Developers, "Build adaptive navigation" (22 Sep 2026): "In compact windows, such as a standard phone display, the destinations are typically displayed in a navigation bar at the bottom of the window", a navigation rail in larger windows; strength: platform guidance
- era: dated 2027-10-19
- owner: vault
- stage: role
- target: Below 600 px put an app's top-level destinations in a bottom bar and a site's in its header per `vault.visible-nav`; from 600 px move an app's to a side rail and keep a site's in the header bar.
- script: check-layout.py <page> --out <dir> --records --brief kind=<app or site>
- reasons: design-critique/references/layout-and-data.md#navigation-by-window-width
- ledger: LAY-70, NAV-196
- status: staged

### vault.carousel-use
- applies-when: web-surface; every hero, and every set of like items shown on the page
- question: Is a hero one static image or message and a set of items a grid or list, a carousel used only for a set the visitor browses one at a time that the page cannot lay out (a listing's photos)?
- answered-by: look
- writes: carousel use
- yields-to: none
- source: Baymard, Scott, "Homepage Carousels" (2019, updated 3 Apr 2025, as read Oct 2026): 46% of homepage carousels have UX performance issues, and "a well-performing and simpler alternative is to use static content sections"; NN/g, Pernice, "Designing Effective Carousels" (2013, reviewed 7 Aug 2026): "a static hero image may be less likely to distract users than a rotating element"; web.dev Learn Design, "UI patterns" (2021): a carousel risks that "your users will never discover the hidden content"; strength: domain evidence
- era: timeless
- owner: vault
- stage: function
- target: Lead with one static hero; show a set of items as a grid or list; keep a carousel for a set the visitor flicks through one at a time, such as a listing's photos.
- reasons: design-critique/references/page-behaviour.md#carousels
- ledger: NAV-88
- status: staged

### vault.filter-place
- applies-when: web-surface; a results or listing page with filters or sort, at desktop and phone width
- question: Beside a map, do filters and sort sit in a horizontal bar above the list and map, never a vertical sidebar; on a desktop listing with no map, do they stay visible in a persistent panel; on a phone, are they one fixed button opening a drawer, with the applied filters shown above the results?
- answered-by: look
- writes: filter placement
- yields-to: none
- source: Baymard, Collins, split-view results (8 Feb 2022): "Displaying filters in a vertical sidebar" crowded the list, and a "horizontal filtering and sorting bar" with a split view "performed very well"; Baymard, MacDonald, "Product Listing Page (PLP) UX" (20 Aug 2026, as read Oct 2026): "On desktop, keep filters visible in a persistent panel", a sticky drawer from a fixed button on mobile, applied filters above the list; strength: domain evidence
- era: dated 2027-10-19
- owner: vault
- stage: role
- target: With a map beside the list, put filters and sort in one horizontal bar above both; with no map, keep them in a persistent panel on desktop; on a phone, open them from one fixed button into a drawer; show applied filters above the results.
- reasons: design-critique/references/layout-and-data.md#filters-and-sort
- ledger: NAV-197
- status: staged

### vault.label-in-name
- applies-when: web-surface; every control with a visible text label: navigation items, links, buttons, tabs
- question: Does each control's accessible name contain its visible label's text?
- answered-by: script
- writes: accessible name
- yields-to: none
- source: WCAG 2.2 success criterion 2.5.3 Label in Name (level A), and its Understanding page: "A best practice is to have the text of the label at the start of the name"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: treatment
- target: Start each control's accessible name with its visible label, adding words after it only where the label alone is unclear.
- script: check-markup.py
- reasons: design-critique/references/markup-and-navigation.md#names-match-what-is-shown
- ledger: NAV-157
- status: staged

### vault.flow-back
- applies-when: web-surface; every flow of more than one step: a multi-page form, a booking, a sign-up
- question: In a flow of several steps, does the browser's Back button take the visitor to the previous step, at its own URL, with every answer they gave on it kept?
- answered-by: script
- writes: browser Back in a flow
- yields-to: level 2
- source: GOV.UK Design System, "Question pages" (as read Oct 2026): "do not break the browser back button. Make sure it takes users to the previous page they were on, in the state they last saw it"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Give each step of a flow its own URL or history entry, and restore its answers when the visitor comes back to it.
- script: check-cross.py <home page> --flow <first step> [--form <selector>]
- reasons: design-critique/references/markup-and-navigation.md#back-works-in-a-flow
- ledger: NAV-162
- status: staged

### vault.once-only-back
- applies-when: web-surface; every flow step that follows an action that must happen once: a payment taken, a booking or form sent
- question: After an action in a flow that must happen once, does the browser's Back button still work and show a sensible message, rather than repeat the action?
- answered-by: look
- writes: browser Back after a once-only action
- yields-to: vault.flow-back
- source: GOV.UK Design System, "Question pages" (as read Oct 2026): after an action done once "the browser back button should still work, but show the user a sensible message"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Answer Back after a once-only action with a message saying it is done.
- reasons: design-critique/references/markup-and-navigation.md#back-works-in-a-flow
- ledger: NAV-162
- status: staged

### vault.multiple-ways
- applies-when: web-surface; every page of a site of more than one page, save a page that is a step in a process
- question: Can each page be reached in two or more ways (the navigation, links from related pages, a search, a site map, a table of contents, or links from the home page to every page)?
- answered-by: script
- writes: ways to reach a page
- yields-to: none
- source: WCAG 2.2 success criterion 2.4.5 Multiple Ways (level AA), and its Understanding page: two or more of techniques G125, G64, G63, G161, G126 and G185, and a site of three or four pages may meet it by linking every page from its home page; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: function
- target: Give every page at least two routes to it, such as the navigation and a search or a site map; on a site of a few pages, link every page from the home page.
- script: check-cross.py <home page>
- reasons: design-critique/references/markup-and-navigation.md#more-than-one-way-to-a-page
- ledger: NAV-213
- status: staged

### vault.skip-link
- applies-when: web-surface; every page with navigation or another repeated block before its main content
- question: Is the first focusable element on the page, or the first after a cookie banner, a link to the main content that is either always visible, or hidden until it takes keyboard focus and then shown in full?
- answered-by: script
- writes: skip link
- yields-to: none
- source: WCAG 2.2 success criterion 2.4.1 Bypass Blocks (level A), technique G1: "links that are visible only when they have focus can meet this success criterion", links visible at all times preferred; success criterion 2.4.7 Focus Visible (level AA); GOV.UK Design System, "Skip link" (as read Oct 2026): "visually hidden until a keyboard press activates it", placed right after `<body>`, or after a cookie banner; web.dev, Learn Accessibility, "Focus", skip links; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: treatment
- target: Make the first focusable element a "Skip to main content" link to the `main` element, hidden until it takes focus and fully shown when it does.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/markup-and-navigation.md#the-skip-link
- ledger: TXL-22
- status: staged

### vault.suggestions-announced
- applies-when: web-surface; a search box or text field that shows suggestions as the visitor types
- question: Is a field that suggests as the visitor types built as an ARIA combobox (`role="combobox"`, `aria-expanded`, `aria-controls` naming a `listbox`, `aria-activedescendant` on the highlighted option), and is the number of suggestions, or that there are none, put in a status region a screen reader announces without moving focus?
- answered-by: script
- writes: suggestion announcement
- yields-to: none
- source: WAI-ARIA Authoring Practices Guide, Combobox pattern (as read Oct 2026); WCAG 2.2 success criterion 4.1.3 Status Messages (level AA), whose Understanding page gives "18 results returned" and "No results returned" as status messages; GOV.UK's accessible-autocomplete (alphagov), which puts the count of results in an `aria-live` status region; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: treatment
- target: Build a suggesting field as an ARIA combobox over a `listbox`, and write the number of suggestions, or "No results", into a `role="status"` region as they change.
- script: check-state.py, its suggest line
- parts: combobox, textbox
- reasons: design-critique/references/markup-and-navigation.md#suggestions-are-announced
- ledger: NEW3-59
- status: staged

### vault.nav-wide
- applies-when: web-surface; the main navigation at desktop width, 1024 px and over
- question: At desktop width, are all the main navigation's top-level links in view, none behind a menu button?
- answered-by: script
- writes: desktop navigation visibility
- yields-to: none
- source: Pernice and Budiu, NN/g, "Hamburger Menus and Hidden Navigation Hurt UX Metrics" (26 Jun 2016): "Do not use hidden navigation (such as hamburger icons) in desktop user interfaces"; NN/g, "Homepage Design: 5 Fundamental Principles" (15 Mar 2024), guideline 4.3, "Locate primary navigation in a highly noticeable place", a site that "concealed its global navigation behind the MENU link" as its failing example; USWDS layout grid (updated 6 Nov 2024): the desktop breakpoint, 1024px; strength: domain evidence
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Show every top-level link of the main navigation in the header at 1024 px and over; keep the menu button for narrower widths.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#desktop-navigation-stays-in-view
- ledger: LAY-70, NAV-211, NAV-212
- status: staged

### vault.nav-strip
- applies-when: web-surface; a row of navigation links shown in view at phone width (a secondary nav, subcategory links, or the main links `vault.visible-nav` keeps in view) that does not fit one line
- question: At phone width, does a row of navigation links too long for one line scroll sideways in that one line, the screen's edge cutting the last link in view so more is seen to follow, rather than overflowing the page or spilling onto many rows?
- answered-by: script
- writes: navigation row overflow
- yields-to: vault.visible-nav, level 2
- source: web.dev Learn Design, "UI patterns", Navigation (as read Nov 2026): "Try to find a strategy that avoids hiding your navigation"; "keep links on one line but truncate the list at the edge of the screen"; "make sure it's clear that the off-screen content is reachable"; Baymard, "Ecommerce Category Page" (17 Apr 2026): "Horizontal scrolling subcategory strips are an efficient mobile pattern"; strength: platform guidance and domain evidence
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Put a row of links too long for a phone's width in one sideways-scrolling line, sized so the edge cuts the last link in view.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#a-long-link-row-scrolls-in-one-line
- ledger: LAY-73
- status: staged

### vault.breadcrumb-narrow
- applies-when: web-surface; a breadcrumb trail, at phone width
- question: At phone width, is the breadcrumb trail still shown, and does a trail too long for one line collapse to its first and last items, the middle reached by an ellipsis button named "Show more breadcrumbs", rather than wrapping onto several lines or overflowing?
- answered-by: script
- writes: breadcrumb trail at narrow widths
- yields-to: level 2
- source: GOV.UK Design System, Breadcrumbs (changed Jul 2024), "Collapsing breadcrumbs on mobile devices": "configure the component to only show the first and last items on mobile devices", `govuk-breadcrumbs--collapse-on-mobile`; Atlassian Design System, Breadcrumbs usage (as read Nov 2026): "When additional breadcrumbs are collapsed into an ellipses, this is treated as a single list item", "The default label is 'Show more breadcrumbs'"; Apple HIG, Path controls (as read Nov 2026): "If the list is too long to fit within the control, it hides names between the first and last items"; impeccable 4.5.0 adapt.md:166: "Breadcrumbs on smaller screens for context"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Keep breadcrumbs on a phone; collapse a long trail to its first and last items behind a "Show more breadcrumbs" ellipsis button.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#long-breadcrumbs-keep-first-and-last
- ledger: LAY-72, NAV-160
- status: staged

### vault.tabs-narrow
- applies-when: web-surface; a set of tabs, at phone width and with script off
- question: At phone width, and wherever its script does not run, are the tabbed panels shown as sections in order on one page under a contents list linking to each?
- answered-by: script
- writes: tabs at narrow widths
- yields-to: level 2
- source: GOV.UK Design System, Tabs (changed Aug 2024), "How it works": without JavaScript "users will see the tabbed content on a single page, in order from first to last", "with a table of contents that links to each of the sections"; "This is also how the component currently behaves on small screens, though more research is needed on this"; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: On a phone, and with no script, show the tab panels as sections in order under a contents list.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#tabs-become-sections
- ledger: LAY-74
- status: staged

### vault.footer-narrow
- applies-when: web-surface; a large footer holding several groups of links
- question: At phone width, does each of the footer's link groups show only its heading, as a toggle opening its links, rather than one long column of every link, with the groups in two columns from 480 px and four from 1024 px?
- answered-by: script
- writes: footer link groups at narrow widths
- yields-to: level 2
- source: USWDS, Footer, big footer component code (3.14.0, 18 Aug 2026, as read Nov 2026): each link group `usa-footer__primary-content--collapsible`, columns `mobile-lg:grid-col-6 desktop:grid-col-3`; USWDS layout grid (updated 6 Nov 2024): mobile-lg 480px, desktop 1024px, "Columns are full-width until the narrowest breakpoint specified"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: On a phone, show a big footer's link groups as headings that toggle their links; set the groups two across from 480 px and four from 1024 px.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#a-big-footer-collapses
- ledger: LAY-75
- status: staged

### vault.bar-overflow
- applies-when: web-surface; each bar of actions or tools (the header's end items, a toolbar, a drawing or editing bar) as the window narrows
- question: As the window narrows, does each bar keep its most-used actions in view and move the rest, least used first, into one "More" menu at its trailing end, so that on a phone a wide toolbar never runs off the screen (standing on a side edge, as one practitioner's demo does, is allowed)?
- answered-by: look
- writes: bar actions at narrow widths
- yields-to: vault.bar-fit, vault.reflow, level 2
- source: Apple HIG, Toolbars (updated 16 Dec 2025): "define which items move to the overflow menu as the toolbar becomes narrower"; "Prioritize less important actions for inclusion in the More menu"; "Try to include all actions in the toolbar if possible"; for iOS, "Prioritize only the most important items for inclusion in the main toolbar area", "Create a More menu to include additional items"; Atlassian Design System, Top nav items examples (as read Nov 2026): "At `xs` breakpoints and below (less than 768px), these buttons collapse into a single 'More' button"; Apple HIG, Pull-down buttons (as read Nov 2026): a More button "can also hinder discoverability"; Benji Taylor, "Drawesome" (29 Jul 2026): on a phone "the default set runs off both sides of the screen", "under 680px the demo stands the bar up on the left edge and trims the toolset", the one source for the side-edge clause, a practitioner's demo; strength: platform and design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Rank a bar's actions; as width narrows move the least used into one trailing "More" menu, so a phone shows only the most important.
- reasons: design-critique/references/responsive-structure.md#bars-move-actions-into-more
- ledger: LAY-71, NAV-39
- status: staged
### vault.bar-fit
- applies-when: web-surface; each bar of actions or tools (the header's end items, a toolbar, a drawing or editing bar), at every width
- question: At each width, does each bar of actions fit the screen, none of its actions past its edge, save a bar standing on a side edge?
- answered-by: script
- writes: bar fit
- yields-to: vault.reflow, level 2
- source: Apple HIG, Toolbars (updated 16 Dec 2025): "Try to include all actions in the toolbar if possible", "Create a More menu to include additional items"; Benji Taylor, "Drawesome" (29 Jul 2026): on a phone "the default set runs off both sides of the screen", "under 680px the demo stands the bar up on the left edge and trims the toolset", the one source for the side-edge clause, a practitioner's demo; strength: platform guidance
- era: dated 2027-11-13
- owner: vault
- stage: role
- target: Keep every action of a bar on the screen at every width, moving the rest into a trailing "More" menu or standing the bar on a side edge.
- script: check-layout.py <page> --out <dir> --records
- reasons: design-critique/references/responsive-structure.md#bars-move-actions-into-more
- ledger: LAY-71, NAV-39
- status: staged
