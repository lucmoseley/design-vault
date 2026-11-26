# Page behaviour

Why a page's parts answer hover, scrolling, time and typing as their records say (#275). The source checks behind the records are `docs/research/carry-source-checks.md` in the design vault.

Where a project's rules file and a record here disagree, [source precedence](house-principles.md#source-precedence) decides. A dated record is reviewed a year after writing, or sooner when browsers change the behaviour it rests on.

## Principles

### Help in one place

Records: `vault.consistent-help`, `vault.help-button`, `vault.help-button-target`.

- **Why.** A visitor who needs help looks where they found it last time; help that moves between pages is found again only by searching (WCAG 2.2 SC 3.2.6). Two help buttons in one view leave the visitor guessing which help each opens.
- **Trade-off.** A help route fixed in the shared template cannot be moved up on the one page where it matters most; a second, page-specific route can be added, as long as the repeated one keeps its place.
- **Clash.** `vault.consistent-help` is WCAG's, so it beats every layout preference, and it never asks a site to add help it lacks; the one-button limit is Apple's, and a project's rules file may set another.

### Nothing on hover alone

Records: `vault.hover-reveal`, `vault.hover-content`, `vault.editable-cue`.

- **Why.** A phone, a tablet and a keyboard cannot hover, and a touch laptop's visitor may never move a pointer, so what only hover shows is missing for them (web.dev, MDN). A tooltip a keyboard cannot open, or one that vanishes as the pointer moves onto it, fails the same visitors (WCAG 2.2 SC 1.4.13).
- **Trade-off.** Showing a card's actions by default where no input hovers makes the card busier on a phone; fewer actions per card is the way out, not hiding them.
- **Clash.** `vault.affordance` says an actable part must look actable.

### Menus open on click

Record: `vault.menu-click`.

- **Why.** A menu that opens on hover opens by accident as the pointer crosses it, closes as the pointer leaves for a submenu, and never opens for touch or keyboard (USWDS).
- **Trade-off.** A click costs one more action than a hover for a mouse visitor scanning menus.
- **Clash.** None known.

### Validation timing

Record: `vault.validation-timing`.

- **Why.** An error flagged while a visitor is still typing scolds them for an answer they have not finished, and slow typists see it most (GOV.UK, NN/g). An error caught while the visitor is still at the field is fixed there, and one that disappears as soon as it is fixed tells them so (Baymard testing).
- **Trade-off.** GOV.UK's question pages hold one or two fields, and checking them at submit costs nothing; on a long checkout, waiting for submit sends the visitor back up the form.
- **Clash.** None known.

### Native scrolling

Record: `vault.native-scroll`.

- **Why.** Visitors expect one scroll rate on every page of every app; a page that changes it makes them miss content or tire, and takes control of their device away (NN/g 2023).
- **Trade-off.** Scroll-driven storytelling loses its pinned, stepped sections; scroll-driven animation that leaves the rate alone keeps most of the effect.
- **Clash.** None known.

### Parallax

Record: `vault.parallax`.

- **Why.** Parallax is decoration that moves as the visitor scrolls; on text it is hard to read and can make people dizzy or sick, and WCAG names it the common non-essential animation behind vestibular reactions (NN/g; WCAG 2.2 SC 2.3.3).
- **Trade-off.** Kept to a background image, parallax gives depth to a leisure or brand page at little cost; on a page where the visitor has a task, it is better left out.
- **Clash.** `vault.reduced-motion` turns it off under reduced motion.

### Carousels

Records: `vault.carousel-use`, `vault.carousel-timing`.

- **Why.** A carousel hides every frame but one, and visitors seldom see the rest; static sections perform as well and are simpler (Baymard, NN/g, web.dev). Where frames advance by themselves, a frame that leaves before it is read is lost, so its time follows its words (3 a second, NN/g), and a phone visitor scrolls past before it changes.
- **Trade-off.** A grid of every item takes more room than one rotating slot; on a phone a swipeable row can be the better fit for a set of like items.
- **Clash.** `vault.pause` still asks a pause control for any carousel that moves for more than 5 s.
