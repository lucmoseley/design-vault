# Forms and overlays

Why a form asks one thing at a time, and why menus, dialogs and content shown on hover behave as their records say (#279). The source checks behind the records are `docs/research/forms-overlays-colour-defaults.md` in the design vault.

A project's rules file wins over every record here except a floor WCAG or the law sets ([source precedence](house-principles.md#source-precedence)). A dated record is reviewed a year after writing, or sooner when browsers change the behaviour it rests on.

## Principles

### One thing per page

Records: `vault.one-thing-per-page`, `vault.questions-per-page`.

- **Why.** A page that asks one thing tells the visitor exactly what is wanted, lets them recover from an error on that one answer, and fits a phone. GOV.UK starts every form this way.
- **Trade-off.** More pages mean more clicks; GOV.UK's one named case for merging is staff who repeat and switch between tasks quickly. Page count is not the main cost: Baymard finds a one-page checkout with 30 fields often worse than three steps with well-designed forms, so fields come out before steps go in.
- **Clash.** `vault.field-budget` decides which fields are asked at all; these records decide how the ones left are paged.
- **Why no script answers it.** A script counts a page's questions, and `vault.questions-per-page` does; whether a page holds one thing, and whether its steps suit the task, turns on what the questions mean.

### The question is the heading

Record: `vault.question-heading`.

- **Why.** Where a page asks one question, a heading above a label that repeats it is read twice by a screen reader. Making the label or legend the h1 says it once and still gives the page its heading.
- **Trade-off.** The question must read well as a page title, which rules out a terse label such as "Email".
- **Clash.** None known.

### Focus on the error summary

Record: `vault.error-summary-focus`.

- **Why.** After a failed submit, a visitor using a keyboard or screen reader would otherwise stay at the submit button with no news that anything went wrong. Moving focus to a summary at the top tells them at once and lists what to fix.
- **Trade-off.** The jump moves the page away from where the visitor was; on a short form with one error, the field itself is near.
- **Clash.** None known.

### Menus close together

Record: `vault.submenu-close`.

- **Why.** A submenu left open after its parent closes floats over the page with nothing to anchor it, and a keyboard visitor cannot reach it.
- **Trade-off.** None worth naming.
- **Clash.** None known.

### Interruptions

Record: `vault.interruptions`.

- **Why.** An offer modal, a chat prompt or a live update breaks a visitor's task. WCAG 2.2 SC 2.2.4 asks that the visitor can put such interruptions off or turn them off.
- **Trade-off.** 2.2.4 is level AAA, above the house's AA floor (`vault.wcag-aa`). The house holds to it for interruptions because a returning pop-up is the kind of pressure the house does not use. WCAG's own example is a setting that postpones all updates; a close that brings the pop-up back on the next page postpones it by one page at most.
- **Clash.** An emergency, such as data about to be lost, is the one exception, by the criterion's own terms.

### Dialog role and name

Record: `vault.dialog-name`.

- **Why.** Assistive technology reads a dialog out by its role and name, which the APG pattern requires.
- **Trade-off.** None worth naming. The `<dialog>` element opened by `showModal()` gives the role and modality itself, so only the name is left to the page.
- **Clash.** None known.

### Repeated navigation keeps its order

Record: `vault.nav-order`.

- **Why.** A visitor who has learned where a link sits, by sight or by the number of Tab presses, finds it again on the next page. WCAG 2.2 SC 3.2.3 holds repeated navigation to one relative order at level AA.
- **Trade-off.** A page cannot lift its most relevant link to the front of the menu; it can add a secondary navigation instead.
- **Clash.** WCAG's, so it beats every layout preference.

### Ellipses on menu items

Record: `vault.menu-ellipsis`.

- **Why.** An ellipsis tells a visitor that choosing the item asks for more before anything happens. On an item that acts at once, or opens a submenu whose arrow already says so, it misleads. On a progress label it says the action is still going.
- **Trade-off.** The convention comes from desktop platforms and many web visitors never notice it, so a label that needs more input still says what it does.
- **Clash.** None known.
