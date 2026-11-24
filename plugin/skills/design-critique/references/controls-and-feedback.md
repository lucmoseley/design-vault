# Controls and feedback

Why a control says whether it is open, acts on release and stays clear of a phone's edges, why a passing message is announced without taking focus, when a cookie banner is owed, why motion waits for a screen fast enough to show it, and how small labels, destructive actions and button sizes are chosen (#281, #287). The source checks behind this file's records are `docs/research/control-feedback-defaults.md` in the design vault, and for small labels, destructive actions and button sizes they are design-vault#287's source checks (https://github.com/lucmoseley/design-vault/issues/287#issuecomment-6842731457).

A project's rules file wins over every record here except a floor WCAG or the law sets ([source precedence](house-principles.md#source-precedence)). A dated record is reviewed a year after writing, or sooner when browsers or the law change what it rests on.

## Principles

### Controls say whether they are open

Record: `vault.expanded-state`.

- **Why.** A screen reader user who presses a menu button hears nothing change on the button itself; `aria-expanded` tells them the menu opened, and where focus did not move, that is all they get.
- **Trade-off.** The state must be kept in step by script on every open and close, and a stale `true` misleads more than none.
- **Clash.** None known.

### Act on release

Record: `vault.act-on-release`.

- **Why.** A visitor who presses the wrong control can slide off it before letting go; an action fired on the press gives them no way out. A `click` fires on release and works for touch and keyboard too.
- **Trade-off.** A press-and-hold or a drag needs the press, so those keep it, with the release undoing what the press began.
- **Clash.** WCAG's, so it beats every preference for a snappier feel.

### Clear of the phone's edges

Record: `vault.bottom-safe-area`.

- **Why.** A phone's browser toolbar slides over the page's bottom edge, and on a phone with rounded corners or a home indicator the page can run under them; a submit button or bottom nav there is half covered. `svh` sizes to the screen with the toolbar shown, `dvh` follows it as it slides, and the safe-area insets measure the device's own edges.
- **Trade-off.** `dvh` resizes the layout while a visitor scrolls, which can jank; `svh` leaves a strip of space when the toolbar hides.
- **Clash.** None known.

### Counts and progress are named

Records: `vault.badge-name`, `vault.progress-name`, `vault.progress-element-name`.

- **Why.** A screen reader reads a badge's number with nothing to say what it counts, "Inbox 4", and a progress bar with no name as a bare percentage; the words a sighted visitor gets from the layout must be in the markup.
- **Trade-off.** Hidden words must be kept true as the count or task changes, and words added where the label already names the count are read twice.
- **Clash.** None known.

### Live regions are there from the start

Record: `vault.live-region-ready`.

- **Why.** A screen reader watches only the live regions it found when the page loaded, and a region inserted already holding its text is often never read. A message hidden in the page and shown later can instead be read out before it applies, by assistive technology that ignores the hiding.
- **Trade-off.** An empty region must sit in the page's markup for every place a later message can appear.
- **Clash.** `role="alert"` is the exception both sources name: it is read even when inserted with its text.

### Toasts never take focus

Record: `vault.status-no-focus`.

- **Why.** Moving focus to a toast pulls a visitor out of what they were doing, and leaves them stranded when it disappears. A toast that vanishes on a timer takes its action with it before a screen reader user can reach it.
- **Trade-off.** A toast that stays until dismissed is one more thing to close; the action offered elsewhere is one more control on the page.
- **Clash.** `vault.inverse-surface` sets how a toast looks; this record sets how it is announced.

### A cookie banner only for consent

Records: `vault.cookie-banner`, `vault.cookies-page`.

- **Why.** UK and EU law ask for consent before most storage on a visitor's device, and exempt what is strictly necessary for the service the visitor asked for; a banner where nothing needs consent asks a question with no answer. Since the Data (Use and Access) Act 2025, the UK also exempts storage for statistics and for remembering a visitor's chosen appearance, provided the site says what it does and lets visitors object; the EU does not, so a site serving EU visitors still asks for analytics.
- **Trade-off.** No banner leaves the cookies page as the only place a visitor learns what is stored.
- **Clash.** The law's, so it beats every look. This record is not legal advice; a project that sets advertising storage, or serves visitors under another law, reads that law.

### Motion on slow screens

Record: `vault.slow-update`.

- **Why.** An e-ink screen redraws too slowly to show a move, so an animation there is a stutter of frames and a transition a smear; print shows one frame, which must be the end state. The `update` feature tells the page which kind of screen it is on.
- **Trade-off.** An older browser that does not know `update` gets no motion.
- **Clash.** `vault.reduced-motion` answers a visitor's request for less motion; this record answers the screen's ability to show it.

### Badge, status label or tag

Record: `vault.badge-kind`.

- **Why.** Each small label carries a different kind of content: a count, a status that changes what a visitor does next, or metadata that only sorts things (Atlassian). A status label made a link or a verb is mistaken for a button (GOV.UK).
- **Trade-off.** Three similar parts take more design-system upkeep than one generic chip.
- **Clash.** `vault.function-code` gives each part its function; this record picks which small part carries that function. How a tag is filled is `vault.tag-fill`'s.

### Dot, number or plain count

Record: `vault.count-badge`.

- **Why.** A dot says only that something is new, so it works only where the label says what is new (MUI). A number says how many, which a visitor needs for unread messages or items waiting (Red Hat, Android). A count that describes its item, such as a post's comments, is supporting detail: a plain number with an icon naming it is quieter than a dark badge and clearer about what it counts (Refactoring UI).
- **Trade-off.** A number badge grows with the count and needs a cap such as 99+.
- **Clash.** `vault.tag-fill` gives which badges take a bold fill; this record says when a count needs a badge at all. `vault.badge-name` gives the count its words for a screen reader.

### Destructive actions

Records: `vault.destructive-action`, `vault.destructive-fill`.

- **Why.** People press a prominent button without reading it, so a destructive action given the primary style gets pressed by mistake (Apple). The danger hue warns only where the loss is the step's whole point, the final confirmation, and red alone is missed by some visitors, so the label names the loss (GOV.UK).
- **Trade-off.** A delete button kept quiet on its first appearance takes a second step to reach.
- **Clash.** Apple keeps the primary role off a destructive button even when confirming; GOV.UK and Refactoring UI make the confirming button the red, prominent one. The house follows GOV.UK and Refactoring UI at the confirmation step alone; `vault.dialog-default` keeps the danger style off the primary rung where the visitor did not choose the loss, and wins there. The confirming button is the one place the danger hue, which `vault.carry-status` otherwise keeps for status, fills an action. `vault.primary-action` and `vault.carry-act` set the one main action and its colour everywhere else.

### Button size by place

Records: `vault.button-size`, `vault.button-place`.

- **Why.** A standalone key action may be larger: GOV.UK gives its start button larger type, and USWDS offers a big button for the important action. Dense rows take a compact size (Atlassian).
- **Trade-off.** Few size steps are easy to keep consistent; a project that needs more names them in its rules file.
- **Clash.** `vault.button-group-size` keeps buttons in a group to one size, and wins inside a group; `vault.target-size` sets the floor every size keeps; `vault.radius-density` sets the capsule shape for one standout action, and this record its size.
