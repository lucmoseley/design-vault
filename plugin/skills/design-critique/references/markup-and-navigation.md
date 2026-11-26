# Markup and navigation

Why a page is built from native elements and landmarks, names its controls by what they show, and gives a visitor more than one way in and a working way back (#280). The source checks behind this file's records are `docs/research/markup-navigation-defaults.md` in the design vault.

Where a project's rules file and a record here disagree, [source precedence](house-principles.md#source-precedence) decides. A dated record is reviewed a year after writing, or sooner when browsers change the behaviour it rests on.

## Principles

### Native elements carry their role

Records: `vault.native-html`, `vault.landmarks`, `vault.landmark-elements`.

- **Why.** A `button`, a link or a `main` element brings its role, its keyboard behaviour and its place in a screen reader's list of regions for free; a `div` given the role by ARIA brings the role alone, and the rest must be written and kept working by hand (W3C, Using ARIA).
- **Trade-off.** A native control is harder to restyle than a `div`, so a custom look costs more CSS.
- **Clash.** WCAG's for landmarks, so it beats every layout preference.

### Names match what is shown

Records: `vault.label-in-name`, `vault.logo-link-name`, `vault.logo-link-words`.

- **Why.** A visitor who controls the page by voice says the words they see; a control whose accessible name does not hold its visible label cannot be reached that way (WCAG 2.2 SC 2.5.3). A logo that links home is a link, so its name says where it goes, not that it is a logo (W3C WAI Images Tutorial).
- **Trade-off.** Words added to a name to make it clearer must come after the visible label, which limits how the name can be phrased.
- **Clash.** WCAG's, so it beats every naming preference.

### Decorative generated content

Records: `vault.generated-content`, `vault.generated-content-look`.

- **Why.** A screen reader reads most text CSS adds, so a decorative arrow or a column of line numbers is read aloud as noise; text that carries information must not live in CSS alone, which some readers skip (WCAG 2.2 F87).
- **Trade-off.** The empty alternative after `/` reaches only browsers from 2024 on (Firefox 128, Safari 17.4); an older one reads the symbol, so a symbol that must stay silent everywhere goes on an `aria-hidden` element instead.
- **Clash.** None known.

### The skip link

Record: `vault.skip-link`.

- **Why.** A keyboard visitor otherwise tabs through the whole header on every page before reaching its content (WCAG 2.2 SC 2.4.1).
- **Trade-off.** WCAG prefers a skip link always visible; most sites hide it until focus, which passes but helps only visitors who already know to press Tab.
- **Clash.** `vault.focus` sets how the link shows focus.

### More than one way to a page

Record: `vault.multiple-ways`.

- **Why.** Visitors look for a page in different ways: some browse the navigation, some search, some scan a list of everything (WCAG 2.2 SC 2.4.5).
- **Trade-off.** A search or a site map is more to build and maintain; a small site meets the rule by linking every page from its home page.
- **Clash.** None known.

### Back works in a flow

Records: `vault.flow-back`, `vault.once-only-back`.

- **Why.** A visitor filling in several steps expects Back to undo one step; a flow that loses their answers, or leaves the site, fails them (GOV.UK, Question pages).
- **Trade-off.** Each step needs its own URL or history entry and its answers held, which a single-page form does not give for free.
- **Clash.** None known.

### Suggestions are announced

Record: `vault.suggestions-announced`.

- **Why.** Suggestions that appear under a field are invisible to a screen reader user unless the field is a combobox and a status region says how many there are (WCAG 2.2 SC 4.1.3).
- **Trade-off.** A count announced on every keystroke can talk over the visitor's typing.
- **Clash.** None known.
