# Rule records: feedback

Telling the visitor what happened or is happening: status, errors, loading, confirmation and undo. The form is [rules.md](../rules.md)'s.

### vault.carry-status
- applies-when: web-surface; every status a part shows: availability, loading, saved, an error
- question: Is each status shown in its semantic colour with text or an icon, beside the thing it describes, in one colour per status across the site and none near the action colour, announced by an ARIA live region where it changes, never pulsing or blinking, and never in a brand tint standing in for the status colour?
- answered-by: whole-page
- writes: status signifier
- yields-to: vault.colour-look, vault.borrowing
- source: GOV.UK Tag; Apple HIG Color; WAI-ARIA 1.2 live regions; #127 B7.2's carrier table; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Give each status its own semantic colour, kept far from the action colour and the same everywhere, with text or an icon, beside what it describes; announce a change in a live region; never pulse it.
- reasons: design-critique/references/house-principles.md#carriers-and-reserved-properties
- ledger: BTN-13, BTN-78, COL-4, COL-10, COL-62, COL-63, FFB-5, FFB-7, IMG-31, IMG-32, MOT-89, MOT-90, NAV-4, NAV-8, NAV-11, NAV-13, NAV-44, NAV-70, NEW1-49, NEW2-55, OTH-24, PAG-123, SUR-84
- status: live

### vault.undo
- applies-when: web-surface; every action that deletes, sends or changes something a visitor may want back
- question: Where an action can be undone, does the page offer undo after it rather than a confirmation before it, keeping a confirmation for what cannot be undone?
- answered-by: whole-page
- writes: undo
- yields-to: none
- source: NN/g 2018, on confirmation dialogs and undo; strength: domain evidence
- era: timeless
- owner: vault
- stage: function
- target: Let a visitor undo a reversible action after it happens; ask for confirmation only before one that cannot be undone.
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: BTN-113, NAV-134, OTH-42
- status: live

### vault.data-states
- applies-when: web-surface; every part that shows data the page loads or a visitor's search or filter returns: a list, a table, a card grid, a results view, a dashboard tile
- question: Does each part that shows loaded data have a designed loading state (a skeleton for a container on first load, kept to a few seconds; a progress indicator for a longer wait), an empty state that says why it is empty and offers the next step, and an error state that says what failed and how to retry?
- answered-by: whole-page
- writes: data states
- yields-to: vault.carry-status
- source: NN/g, Kaplan, "Designing Empty States in Complex Applications: 3 Guidelines" (2021): "Totally empty states cause confusion about how and whether the system is working", and empty states that teach and "Provide direct pathways"; IBM Carbon, Loading pattern (as read Oct 2026): skeletons only on container components "for only a few seconds", a progress indicator when a process takes "more than a moment or two"; impeccable `craft-floor.md` §Verify, loading, error and empty for every element; strength: domain evidence
- era: timeless
- owner: vault
- stage: function
- target: Design a loading, an empty and an error state for every part that shows loaded data: a skeleton or progress indicator, an empty state with its reason and next step, an error with a retry.
- reasons: design-critique/references/interaction-and-forms.md#data-has-three-more-states
- ledger: OTH-20
- status: live

### vault.missing-page
- applies-when: web-surface; every site served over HTTP
- question: Does an address the site does not have answer with status 404 and a page holding a link to the home page?
- answered-by: script
- writes: missing page status and route home
- yields-to: none
- source: RFC 9110 HTTP Semantics §15.5.5, 404 Not Found: the server "did not find a current representation for the target resource"; GOV.UK Design System, Page not found pages (as read Oct 2026): a link onward; strength: web standard and design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Answer a missing address with status 404 and a page linking to the home page.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/interaction-and-forms.md#error-pages-are-plain
- ledger: NEW1-5
- status: staged

### vault.error-page
- applies-when: web-surface; every whole-page error: page not found, a server error, planned downtime
- question: Does each error page name the problem plainly in its heading ("Page not found", "Sorry, there is a problem with the service", "Sorry, the service is unavailable"), with no error code, no "oops" or joke, no red warning text and no breadcrumbs, and say what to do next: when the service returns, what happened to the visitor's answers, a contact route where one helps, and a link onward?
- answered-by: whole-page
- writes: error page content
- yields-to: vault.missing-page, level 2
- source: GOV.UK Design System, Page not found pages, Problem with the service pages and Service unavailable pages (as read Oct 2026): do not use "technical jargon like 404", "informal or humorous words like oops" or "red text to warn people"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Head an error page with the plain problem, then give when it will work again, what happened to the visitor's answers, a contact route and a link onward; no code, no joke, no red text.
- reasons: design-critique/references/interaction-and-forms.md#error-pages-are-plain
- ledger: NEW1-5
- status: live

### vault.badge-name
- applies-when: web-surface; every count or unread badge: a number on a nav item, an inbox or a bell
- question: Does each count badge reach a screen reader as words naming what it counts ("4 unread messages"), in visually hidden text beside the number, rather than a bare number, save where the control's own label already says what is counted?
- answered-by: script
- writes: badge accessible name
- yields-to: level 2
- source: UK Ministry of Justice Design System, Notification badge (updated Oct 2025): `visuallyHiddenText` is required, a "Descriptor for screenreaders to give context to the number"; Bootstrap 5.3, Badge: without context badges "may seem like random additional words or numbers", with "unread messages" as visually hidden text after the count; material-components-android, BadgeDrawable, a plural-aware content description (both as read Oct 2026); W3C Understanding SC 4.1.2; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Give a count badge words a screen reader reads, "4 unread messages", as visually hidden text beside the number; leave them out only where the control's label already names what is counted.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- parts: badge
- reasons: design-critique/references/controls-and-feedback.md#counts-and-progress-are-named
- ledger: NAV-1
- status: staged

### vault.progress-name
- applies-when: web-surface; every `role="progressbar"`: a progress bar, or a loading indicator built as one
- question: Does each `role="progressbar"` have an accessible name saying what is progressing, from `aria-labelledby` or `aria-label`?
- answered-by: script
- writes: progress indicator name
- yields-to: none
- source: W3C, WAI-ARIA 1.2 (2023), progressbar: "Accessible Name Required: True", aria-valuenow omitted when the value is indeterminate; MDN, `<progress>` (as read Oct 2026): "Text placed between the element's tags is not an accessible label"; material-web, Progress: an aria-label such as "Download progress"; strength: WCAG 2.2 A (SC 4.1.2), by WAI-ARIA 1.2
- era: timeless
- owner: vault
- stage: treatment
- target: Name each `role="progressbar"` by what is progressing ("Upload progress") with `aria-labelledby` or `aria-label`.
- script: check-markup.py
- reasons: design-critique/references/controls-and-feedback.md#counts-and-progress-are-named
- ledger: NAV-48
- status: staged

### vault.progress-element-name
- applies-when: web-surface; every `progress` element
- question: Is every `progress` element labelled, by a `label`, `aria-labelledby` or `aria-label`, with words naming what it measures?
- answered-by: script
- writes: progress element name
- yields-to: none
- source: W3C, WAI-ARIA 1.2 (2023), progressbar: "Accessible Name Required: True", aria-valuenow omitted when the value is indeterminate; MDN, `<progress>` (as read Oct 2026): "Text placed between the element's tags is not an accessible label"; material-web, Progress: an aria-label such as "Download progress"; strength: WCAG 2.2 A (SC 4.1.2), by WAI-ARIA 1.2
- era: timeless
- owner: vault
- stage: treatment
- target: Name each progress indicator by what is progressing ("Upload progress") with a `label`, `aria-labelledby` or `aria-label`; give the amount in `value` or `aria-valuenow`, and none while the progress is indeterminate.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/controls-and-feedback.md#counts-and-progress-are-named
- ledger: NAV-48
- status: staged

### vault.live-region-ready
- applies-when: web-surface; every message the page shows after load in answer to a visitor or an event: an alert, a status line, an error summary, a toast
- question: Is each such message announced from a live region (`role="status"`, `role="alert"` or `aria-live`) that is in the page's first markup and empty until the message is written into it, or from a `role="alert"` inserted with its text, and never from a filled message hidden in the page and revealed later?
- answered-by: script
- writes: live region presence
- yields-to: level 2
- source: USWDS, Alert, Accessibility (guidance updated Aug 2026): "Don't visually hide alert messages and then make them visible when they are needed"; MDN, ARIA live regions (as read Oct 2026): "Start with an empty live region", "The most reliable way to ensure that live regions are registered is to include them in the initial markup", and `role="alert"` is announced even when injected; WAI-ARIA Authoring Practices, Alert pattern; strength: design-system guidance, under WCAG 2.2 SC 4.1.3
- era: dated 2027-10-19
- owner: vault
- stage: function
- target: Put an empty live region for each later message in the page's first markup, `role="status"` for advice and `role="alert"` for what is urgent, and write the message into it when it is due; never hide a written message to reveal it later.
- script: check-state.py, its live-region line
- reasons: design-critique/references/controls-and-feedback.md#live-regions-are-there-from-the-start
- ledger: NAV-75
- status: live

### vault.status-no-focus
- applies-when: web-surface; every toast, snackbar and status message: a saved note, a sent confirmation, a count of results
- question: Does each toast or status message reach a screen reader through a live region without taking focus, and does one that carries an action stay until dismissed and offer that action somewhere else on the page too?
- answered-by: script
- writes: toast focus
- yields-to: none
- source: W3C, WCAG 2.2 SC 4.1.3 Status Messages (2024 edition): status messages are presented "without receiving focus"; Angular Material v12, Snackbar: it "does not move focus", the action needs "an alternative way to perform" it, and a snackbar with an action takes no duration; Flutter 3.37: a snackbar with an action now stays until used, which Flutter says matches Material 3 (m3.material.io renders only by script and was not read); strength: WCAG 2.2 AA for focus, framework guidance for a toast with an action
- era: timeless
- owner: vault
- stage: function
- target: Announce a toast through a live region and leave focus where it is; keep a toast with an action open until it is dismissed, and offer the action elsewhere on the page as well.
- script: check-state.py, its toast line
- reasons: design-critique/references/controls-and-feedback.md#toasts-never-take-focus
- ledger: NAV-77
- status: staged

### vault.badge-kind
- applies-when: web-surface; every small label beside or on an item: a count, a status, a category or other metadata
- question: Does each small label take the part its content asks for: a count or metric in a badge, a status or other attribute that changes what a visitor does in a status label, descriptive metadata that only classifies or filters in a tag, with none of them made a link or a button and each status label an adjective, not a verb?
- answered-by: look
- writes: small label kind
- yields-to: vault.function-code, level 2
- source: Atlassian Design System, Badge (as read Nov 2026): "Use badges to represent numerical data such as counts and metrics"; Atlassian Lozenge (as read Nov 2026): "Use lozenges for workflow status, system state, priority, permissions", "Don't use lozenges for descriptive metadata that only classifies or categorizes — use a tag instead", "For tallies or scores, use a badge"; GOV.UK Design System, Tag (updated Feb 2026): "Tags are only used to indicate a status. Do not make a tag interactive", "Use adjectives (descriptive words) and not verbs"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Put a count in a badge, a status a visitor acts on in a status label named by an adjective, and plain metadata in a tag; never make any of them a link or a button.
- reasons: design-critique/references/controls-and-feedback.md#badge-status-label-or-tag
- ledger: NAV-4
- status: staged

### vault.count-badge
- applies-when: web-surface; every mark of new or waiting items (unread, new, pending), and every count shown beside an item it describes (comments, replies, items)
- question: Does each mark of new or waiting items show a number where the visitor needs the count, and a plain dot only where the count does not matter and the control's label already says what the dot marks, and does a count that describes its item sit as a plain number beside an icon naming what it counts?
- answered-by: look
- writes: count indicator form
- yields-to: vault.tag-fill, level 2
- source: MUI, React Badge (as read Nov 2026): "A dot badge does not show text or a number, so use it only when the surrounding UI makes the state clear, such as Online or Unread"; Red Hat Design System, Badge guidelines (as read Nov 2026): "Use a badge to reflect counts like number of objects, events, or unread items"; Android Developers, Badges (updated 10 Nov 2026): a badge for "the number of unread notifications" and to "highlight new content", and material-components-android BadgeDrawable (updated 8 Aug 2025), a small badge with no label and a large badge carrying a number; Refactoring UI, "Redesigning Laravel.io" (4 Oct 2017): "de-emphasize the comment count a bit by removing the dark background, and … add an icon to make it a little more clear what the number means"; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Show a number where the count matters and a dot only where the label already says what it marks; set a count that describes its item as a plain number beside an icon naming what it counts.
- parts: badge, icon
- reasons: design-critique/references/controls-and-feedback.md#dot-number-or-plain-count
- ledger: NAV-5, SUR-87
- status: staged
