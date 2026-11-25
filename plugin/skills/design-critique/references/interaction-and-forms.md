# Interaction and forms

Why controls answer every kind of input, why forms keep and reuse what a visitor gives them, and why errors, deadlines and exits stay plain (#277). The source checks and the Chromium measurement behind this file's records are `docs/research/interaction-defaults.md` in the design vault.

Where a project's rules file and a record here disagree, [source precedence](house-principles.md#source-precedence) decides; a record its `yields-to` names wins where both apply, as each Clash line says. A dated record is reviewed a year after writing, or sooner when browsers change the behaviour it rests on.

## Principles

### Every drag has a tap path

Records: `vault.drag-alternative`, `vault.slider-keys`, `vault.sheet-grabber`, `vault.motion-input`, `vault.drag-buttons`, `vault.motion-control`, `vault.grabber`.

- **Why.** Some visitors cannot press, hold and move at once (WCAG 2.2 SC 2.5.7) or use two fingers at once, as a pinch needs (SC 2.5.1), and some cannot shake or tilt a device (SC 2.5.4). Keyboard support answers none of them: a pointer user who cannot drag still needs something to tap. A slider's track tap, a sortable list's move buttons, a "Choose file" button and a sheet's grabber are the standard paths (W3C Understanding 2.5.7; GOV.UK File upload; Apple HIG Sheets).
- **Trade-off.** Each path adds a control, and on a small photo gallery or a sheet that costs room; a grabber and arrow buttons are the smallest that serve. Scrolling and pinching the browser itself handles need no path, so a native scroller is exempt.
- **Clash.** The drag path and motion path are WCAG's, so they beat a layout or brand preference; the slider keys and the sheet's grabber are design-system guidance a project may change, and the grabber yields to `vault.drag-alternative`.

### A drag holds its pointer

Records: `vault.drag-tracking`, `vault.drag-tracking-surface`.

- **Why.** A thumb covers a small slider and drifts off it; a drag that stops when the pointer leaves the control drops the visitor's value (Freiberg 2023). Pointer capture keeps the events on the dragged part. In Chromium 149 it did not stop the drag selecting text (the slider's own label, in the measurement), which only `user-select: none` or a cancelled `pointerdown` did.
- **Trade-off.** `user-select: none` on a card also stops a visitor copying its text; set it on the body only while a drag lasts, or on the drag surface alone. Safari needs `-webkit-user-select` beside it (MDN). Firefox and Safari were not measured.

### A released drag follows its throw

Records: `vault.drag-release`, `vault.drag-release-spring-code`.

- **Why.** Picking the snap point nearest the release position ignores the flick: a light throw toward a corner lands back where it started. Projecting the position from the release velocity, as scrolling decelerates, lands it where the visitor aimed (Apple, WWDC 2018). A spring starts at any velocity, so the motion picks up where the hand left off; with no bounce it is the general-purpose default (Apple, WWDC 2023).
- **Trade-off.** A swipe row should stop where the visitor puts it, not fling past its action, so it takes no momentum and snaps back short of its threshold (Krehel). Bounce suits brand motion, which the motion brief governs, not interface settling.
- **Clash.** `vault.motion-duration` times fixed transitions; a release spring runs as long as its velocity needs. `vault.reduced-motion` says what a visitor who asks for less motion sees, and a project's motion tokens win.
- **Why no script answers it.** `check-flow.py` judges the snap point, the set-off and the bounce, but not whether the settle starts at the release velocity. A path sampled a frame at a time cannot tell: on `tier01-clean.html` a critically damped spring that does start at the release velocity read 2.3 to 2.85 times it over its second frame, since a stiff spring pulled toward a far snap point speeds up within a frame. A spring driven from requestAnimationFrame is also read a frame late. Playwright's clock steps requestAnimationFrame a millisecond at a time but not the document timeline a CSS transition runs on.

### States change no widths

Record: `vault.hover-reflow`.

- **Why.** A heavier weight is wider, so bolding a word on hover or selection reflows its line and nudges its neighbours. Grade changes stroke thickness without changing width (MDN, Variable fonts), and colour, underline and fill change nothing.
- **Trade-off.** Few faces have a grade axis; without one, a state is shown by colour, underline or fill, or the face must be uniwidth.
- **Clash.** `vault.emphasis-weight` sets how large a weight step must be; this record forbids the step only where it would move a line.

### Targets by pointer

Record: `vault.coarse-target`.

- **Why.** A finger is larger than a mouse pointer and hides the spot it touches (W3C Understanding 2.5.5). 24 px is WCAG's AA floor, which suits a mouse; 44 px is the AAA figure and the house's touch default (#119). Shrinking targets for a fine pointer gains little, since a larger target helps every pointer (web.dev, Interaction).
- **Trade-off.** 44 px rows cost density in a working view on a phone; a project rules file may set its own coarse value down to the 24 px floor.
- **Clash.** `vault.target-size` holds WCAG's 24 px floor for every pointer and wins; this record adds the house's touch value above it.

### Focus shows for the keyboard

Record: `vault.focus-visible`.

- **Why.** A ring on every mouse click is what led authors to delete focus styles, which leaves keyboard users lost (MDN `:focus-visible`). `:focus-visible` shows the ring when the visitor needs to know where focus is, and a focused text field always does.
- **Trade-off.** A mouse user clicking a custom button sees no ring, which the browser's heuristic decides; a script that moves focus may need `focusVisible: true` to show one.
- **Clash.** `vault.focus` and `vault.focus-ring` say how the ring looks; this record says when it shows.

### Keyboard paths the ARIA patterns fix

Records: `vault.roving-focus`, `vault.menu-focus`, `vault.carousel-focus`, `vault.scroller-focus`, `vault.on-focus`, `vault.key-shortcuts`.

- **Why.** Keyboard users learn one convention: Tab between components, arrows inside one (WAI-ARIA Authoring Practices). A tab list where every tab is a Tab stop, a menu that opens without moving focus, or an off-screen slide the Tab key lands on each breaks it. A scroller with nothing focusable inside cannot be scrolled from the keyboard unless it takes focus itself; Chrome now gives it focus by default, other browsers are not documented to (Chrome for Developers 2024). Focus that changes the page, and single-key shortcuts that speech input fires by accident, are WCAG failures (SC 3.2.1, 2.1.4).
- **Trade-off.** A scroll wheel or trackpad on a slider was not taken as a rule: the patterns name keys and the track, not scrolling, and a wheel over a slider fights page scroll. Roving `tabindex` scrolls the focused item into view by itself; `aria-activedescendant` keeps focus on the container and needs that scrolling done by script. Native radio groups and `<select>` already behave, so build on them where they fit.

### Pinch zoom stays on

Record: `vault.touch-action`.

- **Why.** `touch-action: none` on the page stops a low-vision visitor zooming to read (MDN). `manipulation` keeps pan and pinch but drops double-tap zoom, so quick repeat taps on a control do not zoom the page and the browser need not delay the click.
- **Trade-off.** A map or canvas that handles its own pinch needs `none` on itself, and then owes zoom buttons (`vault.drag-alternative`).
- **Clash.** `vault.reflow` checks the viewport meta's zoom limit; this record covers what CSS blocks.

### Answers are asked once and kept

Records: `vault.prefilled-repeat`, `vault.redundant-entry`, `vault.keep-answers`, `vault.same-address`, `vault.answers-kept`.

- **Why.** Asking again for what a visitor already typed makes them recall it, and some give up (W3C Understanding 3.3.7). An error that clears the fields, or a back button that loses a step, makes them type it all again (GOV.UK Error message, Question pages). A long form that cannot be paused assumes it is done in one sitting, which it often is not (USWDS).
- **Trade-off.** Keeping answers stores personal data longer; a public device and a security answer are the exceptions WCAG names. Across sessions WCAG asks nothing; save and resume is the house's ask for long forms only.

### Long forms offer help in place

Records: `vault.form-help`, `vault.form-help-link`.

- **Why.** A form that sends a visitor away for help loses their place (USWDS). An error met three times means the design, not the visitor, has failed, and earns extra help (NN/g, Krause).
- **Trade-off.** WCAG does not require help to exist; the record asks for it on long or complex forms only.
- **Clash.** `vault.consistent-help` keeps repeated help routes in one place across pages, and wins.

### Signing in takes no memory test

Records: `vault.sign-in`, `vault.paste-allowed`.

- **Why.** Remembering a password, retyping a code or solving a puzzle is a cognitive test some visitors cannot pass (WCAG 2.2 SC 3.3.8). Paste and password managers take the memory out of a password; a passkey or an email link takes the password away (Apple HIG; W3C technique G218).
- **Trade-off.** A one-time code sent by text still has to be read and typed; `autocomplete="one-time-code"` lets the phone fill it in.

### Time limits can be stopped

Records: `vault.time-limit`, `vault.time-limit-look`.

- **Why.** A visitor who reads slowly, or needs a break, loses their work to a silent timeout (WCAG 2.2 SC 2.2.1). A redirect that leaves after a few seconds is a time limit too, so it needs a way to go now and a way to stay.
- **Trade-off.** A held booking or ticket may be essential to the sale and is exempt; it still shows its end plainly (`vault.offer-deadline`).

### Deadlines are plain dates

Records: `vault.offer-deadline`, `vault.offer-end-date`.

- **Why.** A false "limited time" claim is banned in the UK (Digital Markets, Competition and Consumers Act 2024, Schedule 20). A true one still reads as pressure when it ticks or flashes, which the house's no-urgency-theatre line forbids.
- **Trade-off.** A countdown converts some visitors; the house trades that for trust.

### Leaving the site is not interrupted

Records: `vault.exit-warning`, `vault.exit-warning-look`.

- **Why.** A modal before every external link is a roadblock visitors learn to dismiss unread (USWDS, Link). The link text and an external-link indicator say where it goes before the click.
- **Trade-off.** A booking handed to another business's site is a real change of who serves the visitor; a project may keep one short notice there, as Manta's rules file does.

### Data has three more states

Record: `vault.data-states`.

- **Why.** An empty box reads as broken: the visitor cannot tell loading from failure from no results (NN/g, Kaplan 2021). A skeleton holds the layout for a short first load, and a progress indicator tells the truth about a long one (Carbon). An empty state is the place to say why and what to do next.
- **Clash.** `vault.carry-status` says how a status looks; this record says which states must exist.

### Error pages are plain

Records: `vault.error-page`, `vault.missing-page`.

- **Why.** A visitor on an error page is already let down; a code, a joke or red text adds confusion or blame (GOV.UK error page patterns). What they need is what happened, what became of their answers and where to go.
- **Trade-off.** A brand may want personality on a 404; the house keeps wit to low-stakes surfaces, and an error is not one.

### Illustrations stay simple

Record: `vault.illustration-detail`.

- **Why.** An illustration explains by leaving things out: the fewest elements, flat colour and no decorative shadow keep the message visible (GOV.UK, Images). One set of line widths and radii makes a set read as one family.
- **Trade-off.** A brand's illustration style may be richer; a project's rules file wins, and art kept out of the working zone (`vault.decoration-place`) can carry more detail.
