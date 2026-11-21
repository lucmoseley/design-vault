# Rule records: forms

Collecting input: fields, choice controls, and the step where a visitor pays or books. The form is [rules.md](../rules.md)'s.

### vault.high-stakes
- applies-when: has-payment-control; every control at the step where a visitor pays or books, its error states included
- question: At the step where a visitor pays or books, does every control keep its conventional look: a field an edged box with its label outside it, a button a filled or edged shape with a verb on it, a link underlined or in the link colour, a checkbox or radio close to the browser's own?
- answered-by: look
- writes: high-stakes signifier
- yields-to: none
- source: Norman, "Emotion and design" (2002), on use under stress; Google's M3 Expressive research (2025); strength: published research and design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: role
- target: Where a visitor pays or books, keep every control, its error states included, in its conventional look.
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: BTN-55, FRM-65, FRM-83, OTH-12
- status: live

### vault.control-edges
- applies-when: web-surface; every text field, text area and select box, and every checkbox or radio the page draws itself, at desktop and phone width
- question: Where a control's edge or fill is what shows it is there, does that edge or fill reach 3:1 contrast against the colour around it?
- answered-by: script
- writes: control edge
- yields-to: none
- source: WCAG 2.2 success criterion 1.4.11 Non-text Contrast; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: value
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/surface-styling.md#two-border-roles
- ledger: COL-2, COL-65, COL-94, FRM-50, FRM-82, FRM-83, SUR-5, SUR-51
- status: live

### vault.carry-input
- applies-when: web-surface; every text field and search box, and every box drawn like one
- question: Does each text input show itself by an edge or fill at 3:1, a visible label outside the field and a focus ring, and is no static content, such as a summary box or a banner that is a link, drawn as an empty edged box?
- answered-by: whole-page
- writes: input signifier
- yields-to: vault.control-edges, vault.borrowing
- source: W3C Understanding SC 1.4.11; GOV.UK Design System text input; NN/g 2014, on placeholders in place of labels; #127 B7.2's carrier table; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Draw each text field as an edged or filled box at 3:1 with a visible label outside it and a focus ring; never draw static content as an empty edged box.
- reasons: design-critique/references/house-principles.md#carriers-and-reserved-properties
- ledger: FCH-26, FFB-20, FRM-50, FRM-61, FRM-65, FRM-90, OTH-20
- status: live

### vault.trust-form
- applies-when: web-surface; a small business's or a solo advisor's site, and its contact route
- question: Does the site carry an enquiry form only where the reply needs facts people forget to give in an email (a trade's postcode and job type) or the owner wants no public email?
- answered-by: whole-page
- writes: enquiry form
- yields-to: none
- source: GOV.UK Service Manual, question protocol; NN/g 2016; strength: domain evidence
- era: timeless
- owner: vault
- stage: function
- target: Offer an email address as the route by default; add a form only where the reply needs facts an email would miss or the owner keeps no public email.
- reasons: design-critique/references/first-visit-trust.md#the-checklist
- ledger: FRM-32, FRM-36, PAG-39
- status: live

### vault.field-budget
- applies-when: web-surface; every enquiry form
- question: Is every required field one the first reply needs, by the question protocol (for a plain enquiry, name, email and message), does each other field name the action its answer changes before the reply, and are there at most one or two optional fields, each labelled optional?
- answered-by: whole-page
- writes: field count
- yields-to: none
- source: GOV.UK Service Manual, "Structuring forms"; NN/g, Whitenton 2016 (a heuristic, not a measured curve); Seckler et al., CHI 2014; strength: domain evidence
- era: timeless
- owner: vault
- stage: function
- target: Ask for name, email and message, plus only fields whose answer changes what happens before the reply, and at most one or two optional ones, labelled optional.
- reasons: design-critique/references/first-visit-trust.md#the-field-budget
- ledger: FFB-1, FFB-2, FRM-1, FRM-32, FRM-36, PAG-39
- status: live

### vault.trust-privacy
- applies-when: web-surface; every form that collects personal data under UK or EU GDPR
- question: Does the form carry a privacy note at the form itself?
- answered-by: whole-page
- writes: privacy note
- yields-to: none
- source: ICO guidance and UK GDPR Article 13; strength: law
- era: dated 2027-10-14
- owner: vault
- stage: function
- target: Put a short privacy note, linked to the full notice, beside any form that collects personal data.
- reasons: design-critique/references/first-visit-trust.md#the-checklist
- ledger: FRM-30, FRM-31
- status: live

### vault.validation-timing
- applies-when: web-surface; every form field the page checks before it is sent
- question: Does no field show an error while the visitor is still typing a first entry, save a live limit such as a character count, does a field already in error clear on the keystroke that fixes it, and is the first check on leaving the field on a form of several fields and on submit on a one-question page, every error kept with the entered data on submit?
- answered-by: script
- writes: validation timing
- yields-to: none
- source: Baymard, "Usability Testing of Inline Form Validation" (9 Jan 2024): validity "checked when the user leaves the field", never before the user "has had a chance to fully type", and the error "disappearing the moment users enter a valid input"; Baymard, "Checkout Flow UX Optimization" (23 Apr 2026); NN/g, Krause, "10 Design Guidelines for Reporting Errors in Forms" (2019, reviewed Dec 2024), guideline 7; GOV.UK Design System, Validation (as read Oct 2026): "Do not validate when the user moves away from a field" on a service's question pages, with the character count the exception; strength: domain evidence
- era: timeless
- owner: vault
- stage: function
- target: Check a field when the visitor leaves it on a form of several fields, or on submit on a one-question page; never while a first entry is typed, save a character count; clear an error on the keystroke that fixes it; on submit keep every entry and move to the first error.
- script: check-state.py, its timing line
- reasons: design-critique/references/page-behaviour.md#validation-timing
- ledger: FFB-3
- status: live

### vault.choice-control
- applies-when: web-surface; every set of options a visitor chooses from
- question: Where a visitor may pick only one option, is the set a radio group (or a select box), and where they may pick several, a set of checkboxes, with a single checkbox only for one option toggled on or off?
- answered-by: look
- writes: choice control type
- yields-to: none
- source: GOV.UK Design System, Checkboxes (as read Oct 2026): "Do not use the checkboxes component if users can only choose one option from a selection"; USWDS, Checkbox: "If a user can only select one option from a list of many, use radio buttons instead"; Atlassian, Checkbox; WHATWG HTML §4.10.5.1.16, a radio button group, "only one control can have its checkedness state set to true"; strength: domain evidence
- era: timeless
- owner: vault
- stage: role
- target: Give a one-answer question radios or a select box, a several-answer question checkboxes, and a single on-or-off choice one checkbox.
- reasons: design-critique/references/platform-defaults.md#one-answer-or-several
- ledger: FCH-1
- status: staged

### vault.mixed-check
- applies-when: web-surface; every checkbox that selects or clears a group of other checkboxes
- question: When some but not all of its group are checked, does the group's checkbox show the mixed state, set by the `indeterminate` property on a native checkbox or by `aria-checked="mixed"` on a drawn one, and checked when all are and clear when none are?
- answered-by: script
- writes: group checkbox state
- yields-to: none
- source: WHATWG HTML §4.10.5 (as read Oct 2026): indeterminateness "only has an effect on checkbox controls, including their rendering and accessibility semantics", and the control's "selection should be obscured"; MDN, `<input type="checkbox">`, Indeterminate state checkboxes: set only from JavaScript, "purely a visual change"; Atlassian, Checkbox, Behavior; Apple HIG, Toggles: "show a mixed state when the subordinate checkboxes have different states"; strength: domain evidence
- era: timeless
- owner: vault
- stage: role
- target: Set a group checkbox's `indeterminate` property whenever its group is partly checked, checked when all are, clear when none are, and update it on every change.
- script: check-state.py, its mixed line
- reasons: design-critique/references/platform-defaults.md#a-partly-checked-group
- ledger: FCH-32
- status: staged

### vault.auth-paste
- applies-when: web-surface; every field in a sign-in, sign-up or verification step: username, email, password and one-time code
- question: Can a visitor paste into and drop into every authentication field, a one-time code pasted whole filling all of its boxes, with no `autocomplete="off"` on a password?
- answered-by: script
- writes: paste into authentication fields
- yields-to: vault.sign-in
- source: WCAG 2.2 success criterion 3.3.8 Accessible Authentication (Minimum); W3C Understanding SC 3.3.8 (as read Oct 2026): a login form fails where "user agents and password managers are actively blocked from filling in the fields" or "users are prevented from copy and paste operations", unless an alternative is provided; "A service that requires manual transcription of a verification code is not compliant"; asking for chosen characters of a password, as "Enter the 1st, 3rd, and 5th character of your password", fails unless another method is available; failure F109; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: function
- target: Leave paste and password-manager fill working in every sign-in, sign-up and code field, and make a split code box take the whole code on one paste.
- script: check-state.py, its auth-paste line
- reasons: design-critique/references/platform-defaults.md#paste-is-never-blocked
- ledger: FRM-18
- status: staged

### vault.auth-paste-look
- applies-when: web-surface; every sign-in, sign-up or verification step
- question: Does no step ask for chosen characters of a password, and where a step blocks paste or a password manager, does it offer another way to sign in that needs no remembering or transcription?
- answered-by: look
- writes: authentication recall
- yields-to: vault.auth-paste
- source: WCAG 2.2 success criterion 3.3.8 Accessible Authentication (Minimum); W3C Understanding SC 3.3.8 (as read Oct 2026): a login form fails where "user agents and password managers are actively blocked from filling in the fields" or "users are prevented from copy and paste operations", unless an alternative is provided; "A service that requires manual transcription of a verification code is not compliant"; asking for chosen characters of a password, as "Enter the 1st, 3rd, and 5th character of your password", fails unless another method is available; failure F109; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: function
- target: Ask for a whole password, never chosen characters of it; where a field cannot take paste, offer a sign-in needing no remembering.
- reasons: design-critique/references/platform-defaults.md#paste-is-never-blocked
- ledger: FRM-18
- status: staged

### vault.field-paste
- applies-when: web-surface; every text field and text area outside an authentication step, a confirm-email field included
- question: Can a visitor paste into every field, with no handler cancelling `paste` or `drop`?
- answered-by: script
- writes: paste into fields
- yields-to: vault.auth-paste
- source: GOV.UK Design System, Text input, "Do not disable copy and paste" (as read Oct 2026): "Users often need to copy and paste information into a text input, so do not stop them from doing this"; USWDS, Email address pattern: "Do allow users to paste their email address"; web.dev, Learn Forms, "Identity": "Allow pasting into password fields"; strength: domain evidence
- era: timeless
- owner: vault
- stage: function
- target: Never cancel `paste` or `drop` on a field.
- script: check-state.py, its paste line
- reasons: design-critique/references/platform-defaults.md#paste-is-never-blocked
- ledger: FRM-18
- status: staged

### vault.password-empty
- applies-when: web-surface; every password field
- question: Does every password field load empty, with no `value` attribute and no script setting one, leaving filling to the visitor or their password manager?
- answered-by: script
- writes: password default value
- yields-to: none
- source: Apple HIG, Entering data (as read Oct 2026): "Never prepopulate a password field. Always ask people to enter their password or use biometric or keychain authentication"; WHATWG HTML, Password state: the value is obscured on screen; strength: domain evidence
- era: timeless
- owner: vault
- stage: function
- target: Render every password field with no value and leave filling to the visitor's password manager.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#password-fields-load-empty
- ledger: FRM-23
- status: staged

### vault.on-input
- applies-when: web-surface; every radio, checkbox, select box, slider and text field, and every quiz or step that moves on
- question: Does choosing or entering a value leave the visitor where they are, with no form submitted, page loaded, window opened, focus moved or step advanced until they press a button, save a behaviour the page describes before the control?
- answered-by: script
- writes: change of context on input
- yields-to: none
- source: WCAG 2.2 success criterion 3.2.2 On Input; W3C Understanding SC 3.2.2 (as read Oct 2026): sufficient techniques G80 (a submit button) and G13 (describe the change beforehand), failures F36 (auto-submitting a form when a field is given a value) and F37; USWDS, Combo box: "Don't use JavaScript to automatically submit the form (or do anything else) when an option is selected"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Make a button submit, navigate or advance; let a change of value only update what is shown, or say before the control what choosing will do.
- script: check-state.py, its on-input line
- reasons: design-critique/references/platform-defaults.md#a-choice-never-moves-the-visitor-on
- ledger: FRM-38
- status: live

### vault.control-font
- applies-when: web-surface; every `input`, `button`, `select` and `textarea`
- question: Does every form control take the page's typeface and text size, by `font: inherit` or a declared font?
- answered-by: script
- writes: control font
- yields-to: level 2
- source: MDN, Learn web development, "Images, media, and form elements", Inheritance and form elements (as read Oct 2026): "In some browsers, form elements do not inherit font styling by default"; Comeau, "A Modern CSS Reset" (2021, updated Jun 2026), §7, `font: inherit`, the browser's small default making mobile browsers zoom on focus; measured on design-vault#276 (docs/research/platform-defaults.md), Chromium 149 only; Firefox and Safari unmeasured; strength: web platform documentation and a measurement
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Set `font: inherit` on `input`, `button`, `select` and `textarea` in the reset.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: textbox, combobox, button, form
- reasons: design-critique/references/platform-defaults.md#controls-take-the-page-font
- ledger: FRM-78
- status: staged

### vault.caret-shape
- applies-when: web-surface; every text field, text area and editable region
- question: Is `caret-shape` left at `auto`, the platform's caret, save a terminal or console surface that imitates one?
- answered-by: script
- writes: caret shape
- yields-to: level 2
- source: MDN, `caret-shape` (as read Oct 2026): initial `auto`, "The browser determines the caret shape. This typically follows platform conventions"; limited availability, experimental; MDN browser-compat-data (as read Oct 2026): Chrome 144, not Firefox or Safari; strength: web platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Leave the caret to the browser; set `block` or `underscore` only on a surface that imitates a terminal.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: textbox
- reasons: design-critique/references/platform-defaults.md#the-platform-caret
- ledger: FRM-80
- status: live

### vault.textarea-resize
- applies-when: web-surface; every `textarea` and other multi-line text box
- question: Can the visitor resize every multi-line text box at least in the block direction, with no `resize: none`, save a box that grows with its text?
- answered-by: script
- writes: text area resize
- yields-to: level 2
- source: web.dev, Learn Forms, "Fields" (as read Oct 2026): "A `<textarea>` is resizable by default"; disabling it "is a bad user experience"; "Use `resize: vertical`"; MDN browser-compat-data: `resize` unsupported on Safari iOS; strength: web platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Leave a text area resizable, `resize: block` (or `vertical`) where sideways resizing would break the layout.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: textbox
- reasons: design-critique/references/platform-defaults.md#text-areas-stay-resizable
- ledger: FRM-96
- status: staged

### vault.edit-wrap
- applies-when: web-surface; every `textarea` and `contenteditable` region, where a `text-wrap` of `pretty` or `balance` is set on it or an ancestor
- question: Does every editable region use `text-wrap: stable` (or `auto`), so the lines above the one being edited do not re-wrap, rather than inherit `pretty` or `balance`?
- answered-by: script
- writes: editable text wrap
- yields-to: level 2
- source: MDN, `text-wrap` (as read Oct 2026): with `stable`, "the lines that come before the lines they are editing remain static"; Baseline since March 2024; CSS Text Module Level 4 (editor's draft, as read Oct 2026): "stable is intended for sections that are, or are likely become toggled as, editable", the property inherited; measured on design-vault#276 (docs/research/platform-defaults.md), Chromium 149 only; strength: web platform specification and a measurement
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Where `pretty` or `balance` is set page-wide, set `text-wrap: stable` on `textarea` and `[contenteditable]`.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: textbox
- reasons: design-critique/references/platform-defaults.md#editing-does-not-re-wrap
- ledger: FRM-97
- status: live

### vault.field-keyboard
- applies-when: web-surface; every text field, at phone width
- question: Does each field's `type` or `inputmode` match its data, `email`, `tel`, `url` and `search` by `type`, whole numbers and codes by `inputmode="numeric"` on a text input, amounts by `inputmode="decimal"`, and is `type="number"` kept to values a visitor steps through?
- answered-by: script
- writes: field keyboard
- yields-to: none
- source: WHATWG HTML §6.8.9, `inputmode`; MDN, `inputmode` (as read Oct 2026, Baseline since December 2021): inputs that require a telephone number, email or URL "should typically use" that `type`; GOV.UK Design System, Text input: `inputmode="numeric"` for whole numbers, "Do not use `<input type="number">` unless your user research shows that there's a need for it"; strength: domain evidence
- era: dated 2027-10-19
- owner: vault
- stage: function
- target: Give email, phone, web address and search fields their `type`, whole numbers and codes `inputmode="numeric"` on a text input, prices `inputmode="decimal"`, and every other field plain text.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#each-field-brings-up-its-keyboard
- ledger: FRM-99
- status: staged

### vault.autocomplete
- applies-when: web-surface; every field collecting information about the visitor whose purpose WCAG 2.2 §7 lists: name, email, phone, address, birthday, card and account fields
- question: Does each such field carry the `autocomplete` token for its purpose (`name`, `email`, `tel`, `street-address`, `postal-code`, `bday-day`, `cc-number`, `new-password`, `current-password` and the like), and no wrong one?
- answered-by: script
- writes: autocomplete token
- yields-to: none
- source: WCAG 2.2 success criterion 1.3.5 Identify Input Purpose; W3C Understanding SC 1.3.5 (as read Oct 2026): technique H98, failure F107, fields collecting other information out of scope; GOV.UK Design System, Date input, `bday-day`, `bday-month`, `bday-year` "to meet WCAG 2.2 success criterion 1.3.5"; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: function
- target: Give every field about the visitor the `autocomplete` token for its purpose from the HTML autofill list.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#fields-name-their-purpose
- ledger: FRM-102
- status: staged

### vault.enter-key
- applies-when: web-surface; every single-line field in a form of several fields or a search box, at phone width
- question: Does the on-screen Enter key say what pressing it does, by `enterkeyhint` (`next` on a field that moves on to another, `done` or `go` or `send` on the last, `search` on a search box) or a `type` that implies it?
- answered-by: script
- writes: enter key label
- yields-to: level 2
- source: WHATWG HTML §6.8.10, `enterkeyhint`: "what action label (or icon) to present for the enter key on virtual keyboards"; MDN, `enterkeyhint` (as read Oct 2026, Baseline since November 2021): without it the browser "might use contextual information from the `inputmode`, `type`, or `pattern` attributes"; web.dev, Learn Forms, "Address": "Use `enterkeyhint="done"` for the last form control, and `enterkeyhint="next"` for the other form controls"; strength: web platform specification and guidance
- era: dated 2027-10-19
- owner: vault
- stage: function
- target: Set `enterkeyhint="next"` on fields followed by another and `done`, `go`, `send` or `search` on the last.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#the-enter-key-names-its-action
- ledger: NEW1-33
- status: staged

### vault.slider-direction
- applies-when: web-surface; every horizontal slider, in left-to-right and right-to-left layouts
- question: Does each slider hold its lowest value at the reading start, the left in a left-to-right page and the right in a right-to-left one, as a native `input type="range"` does, with a drawn slider's fill and arrow keys following `dir`?
- answered-by: script
- writes: slider direction
- yields-to: none
- source: WHATWG HTML rendering §15.5.8 (as read Oct 2026): a horizontal range's "lowest value is on the right if the 'direction' property has a computed value of 'rtl', and on the left otherwise"; Atlassian, Range: lowest on the left for left-to-right interfaces, on the right for right-to-left; Apple HIG, Sliders: minimum on the leading side; strength: domain evidence
- era: timeless
- owner: vault
- stage: treatment
- target: Use a native range, or mirror a drawn slider's track, fill and arrow keys with `dir`, so the lowest value sits at the reading start.
- script: check-state.py, its direction line
- parts: slider
- reasons: design-critique/references/platform-defaults.md#sliders-start-where-reading-starts
- ledger: NEW1-37
- status: live

### vault.enter-submits
- applies-when: web-surface; every `form` a visitor submits from a single-line text field
- question: Does pressing Enter in a single-line field submit the form, by a submit button in the form that is not disabled, or by the form having only one text-like field and no button?
- answered-by: script
- writes: implicit submission
- yields-to: level 2
- source: WHATWG HTML §4.10.22.2 Implicit submission (as read Oct 2026): Enter fires a click at the form's default button, "the first submit button in tree order", if it "is not disabled"; with no submit button, "If the form has more than one field that blocks implicit submission, then return"; strength: web platform specification
- era: timeless
- owner: vault
- stage: function
- target: Build each form as a `form` with a real submit button that stays enabled, and validate on submit rather than disabling the button.
- script: check-state.py, its enter line
- reasons: design-critique/references/platform-defaults.md#enter-submits-the-form
- ledger: VG-NEW-8
- status: staged

### vault.prefilled-repeat
- applies-when: web-surface; every process of more than one step where a later step asks again for an answer an earlier step took
- question: Within one process, does a field that asks again for an answer an earlier step took, by the same autocomplete token, arrive holding that answer?
- answered-by: script
- writes: repeated answer filled in
- yields-to: none
- source: WCAG 2.2 (2023) SC 3.3.7 Redundant Entry (A) and its Understanding page: information previously entered "is either auto-populated, or available for the user to select", and browser autocomplete "is not considered sufficient"; GOV.UK Design System, Question pages, "pre-populating the relevant fields" (as read Oct 2026); strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Fill in any later field that asks again for an answer the visitor gave earlier in the same process.
- script: check-cross.py <home page> --flow <first step> [--form <selector>]
- reasons: design-critique/references/interaction-and-forms.md#answers-are-asked-once-and-kept
- ledger: FRM-21
- status: staged

### vault.same-address
- applies-when: web-surface; every form asking for a delivery and a billing address
- question: Does the form offer a checkbox to reuse the first address for the second ("same as")?
- answered-by: script
- writes: second address reuse
- yields-to: none
- source: WCAG 2.2 (2023) SC 3.3.7 Redundant Entry (A) and its Understanding page: browser autocomplete "is not considered sufficient", and the reusable answer must be on the same page; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Give a second address a "same as" checkbox.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/interaction-and-forms.md#answers-are-asked-once-and-kept
- ledger: FCH-19
- status: staged

### vault.redundant-entry
- applies-when: web-surface; every process that asks a visitor for the same information twice: a second address, a repeated upload, a later step needing an earlier answer
- question: Within one process, is every answer the visitor already gave that is not filled in for them offered to pick (a "same as" checkbox, a carried-forward answer, an earlier upload to reuse), save where re-entry is essential, needed for security, or the earlier answer no longer valid?
- answered-by: look
- writes: answer reuse
- yields-to: vault.prefilled-repeat, vault.same-address
- source: WCAG 2.2 (2023) SC 3.3.7 Redundant Entry (A) and its Understanding page: browser autocomplete "is not considered sufficient", and the reusable answer must be on the same page; GOV.UK Design System, Question pages, "pre-populating the relevant fields" or "showing carried-forward responses as an option", and File upload, "Let users reuse uploaded files" (as read Oct 2026); strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Fill in, or offer to pick, any answer a visitor already gave in the same process: a "same as" checkbox for a second address, a list of earlier uploads.
- reasons: design-critique/references/interaction-and-forms.md#answers-are-asked-once-and-kept
- ledger: FCH-19, FRM-21
- status: staged

### vault.keep-answers
- applies-when: web-surface; every form, above all a long or multi-step one
- question: Where a form is long, can the visitor save and resume it, and does a problem page say what happened to their answers?
- answered-by: look
- writes: answer retention
- yields-to: vault.answers-kept
- source: GOV.UK Design System, Error message: "Do not clear any form fields ... Keep both passing and failing answers", and Question pages: the back button returns a visitor to the previous page "in the state they last saw it", and Problem with the service pages: "Store previously entered information for a reasonable amount of time" (as read Oct 2026); USWDS, "Complete a complex form", "Allow the users to save and resume" (as read Oct 2026); strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Give a long form save and resume, and say on a problem page what happened to the answers.
- reasons: design-critique/references/interaction-and-forms.md#answers-are-asked-once-and-kept
- ledger: FFB-12, FRM-11
- status: staged

### vault.answers-kept
- applies-when: web-surface; every form
- question: Does the form keep every answer, passing and failing, when it shows its errors, and every answer but a password when the visitor goes Back to it?
- answered-by: script
- writes: answer retention on error and Back
- yields-to: level 2
- source: GOV.UK Design System, Error message: "Do not clear any form fields ... Keep both passing and failing answers", and Question pages: the back button returns a visitor to the previous page "in the state they last saw it", and Problem with the service pages: "Store previously entered information for a reasonable amount of time" (as read Oct 2026); USWDS, "Complete a complex form", "Allow the users to save and resume" (as read Oct 2026); strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Never clear an answer on error or on going back.
- script: check-state.py, its kept line
- reasons: design-critique/references/interaction-and-forms.md#answers-are-asked-once-and-kept
- ledger: FFB-12, FRM-11
- status: staged

### vault.form-help-link
- applies-when: web-surface; every form taller than one screen
- question: Does each form taller than one screen hold a help route inside it: a help, contact, support or chat link, a phone number or an email address?
- answered-by: script
- writes: form help route
- yields-to: vault.consistent-help, level 2
- source: USWDS, "Complete a complex form": "Do provide users with an option to get help (a phone number or chat, for example)" (as read Oct 2026); strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Put a help route inside every long form.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/interaction-and-forms.md#long-forms-offer-help-in-place
- ledger: FFB-33
- status: staged

### vault.form-help
- applies-when: web-surface; every long or complex form
- question: Does a long or complex form offer a way to get help that keeps the visitor on the form, with more help offered where they hit the same error again?
- answered-by: look
- writes: form help
- yields-to: vault.form-help-link, vault.consistent-help, level 2
- source: USWDS, "Complete a complex form": "Do provide users with an option to get help (a phone number or chat, for example)" (as read Oct 2026); NN/g, Krause, "10 Design Guidelines for Reporting Errors in Forms" (2019, reviewed Dec 2024), guideline 10, extra help after an error repeats; WCAG 2.2 (2023) SC 3.2.6, which "is not ... to require authors to provide help"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Give a long form a help route that opens beside it, and more help where the same error comes back.
- reasons: design-critique/references/interaction-and-forms.md#long-forms-offer-help-in-place
- ledger: FFB-33
- status: staged

### vault.paste-allowed
- applies-when: web-surface; every username, password and one-time code field
- question: Does every sign-in field accept a paste?
- answered-by: script
- writes: sign-in paste
- yields-to: none
- source: WCAG 2.2 (2023) SC 3.3.8 Accessible Authentication (Minimum) (AA) and its Understanding page: blocking paste "would force the user to transcribe information and therefore fail"; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: function
- target: Let paste fill every sign-in field.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/interaction-and-forms.md#signing-in-takes-no-memory-test
- ledger: FRM-16
- status: staged

### vault.sign-in
- applies-when: web-surface; every sign-in, sign-up and verification step
- question: Can every sign-in step be passed without remembering, transcribing or solving anything, save recognising objects or the visitor's own pictures: paste and password-manager autofill allowed (`autocomplete="username"`, `current-password`, `one-time-code`), the password showable, and a passkey, an email link or a third-party sign-in offered beside any puzzle or code to retype?
- answered-by: look
- writes: authentication method
- yields-to: vault.paste-allowed
- source: WCAG 2.2 (2023) SC 3.3.8 Accessible Authentication (Minimum) (AA) and its Understanding page: blocking paste "would force the user to transcribe information and therefore fail", WebAuthn and OAuth as alternatives, technique G218 email link; USWDS, Sign-in form: "Allow users to unmask the password field" (as read Oct 2026); Apple HIG Managing accounts, "prefer using a passkey" (as read Oct 2026); strength: design-system guidance over WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: function
- target: Let password managers and paste fill every sign-in field, offer show-password, and offer a passkey, an email link or a third-party sign-in beside any puzzle or retyped code.
- reasons: design-critique/references/interaction-and-forms.md#signing-in-takes-no-memory-test
- ledger: FRM-16
- status: staged

### vault.time-limit
- applies-when: web-surface; every time limit the page sets: a session timeout, an automatic redirect, a timed step
- question: Where the page leaves itself on a timer within 20 hours of load, does it warn at least 20 seconds before, with one button in the warning that restarts the limit?
- answered-by: script
- writes: time limit
- yields-to: none
- source: WCAG 2.2 (2023) SC 2.2.1 Timing Adjustable (A) and its Understanding page: timed redirects are covered, failures F40 and F58; USWDS, Sign-in form: "Don't automatically sign out a user without giving them 20 seconds' advance notice to request more time" (as read Oct 2026); strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Warn at least 20 seconds before any time limit ends with a one-tap "More time".
- script: check-state.py, its time-limit line
- reasons: design-critique/references/interaction-and-forms.md#time-limits-can-be-stopped
- ledger: NAV-154
- status: staged

### vault.time-limit-look
- applies-when: web-surface; every time limit the page sets: a session timeout, an automatic redirect, a timed step
- question: Where a time limit gives no warning with one action to extend it, can the visitor turn it off or set it to at least ten times its length, or is it a real-time event, an essential limit or one over 20 hours, and does an automatic redirect give "Go now" and "Stay" controls?
- answered-by: look
- writes: time limit choice
- yields-to: vault.time-limit
- source: WCAG 2.2 (2023) SC 2.2.1 Timing Adjustable (A) and its Understanding page: timed redirects are covered, failures F40 and F58; USWDS, Sign-in form: "Don't automatically sign out a user without giving them 20 seconds' advance notice to request more time" (as read Oct 2026); strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Give an automatic redirect "Go now" and "Stay" buttons; where a limit cannot warn, let the visitor turn it off or lengthen it.
- reasons: design-critique/references/interaction-and-forms.md#time-limits-can-be-stopped
- ledger: NAV-154
- status: staged

### vault.one-thing-per-page
- applies-when: web-surface; every form longer than one screen of questions, checkout included
- question: Is a long form split across pages that each hold one thing (one piece of information, one decision or one question), with pages merged only where user research shows the visitors answer them together, and is no page cut down by spreading the same fields over more steps rather than dropping the fields the task does not need?
- answered-by: look
- writes: form step count
- yields-to: level 2
- source: GOV.UK Service Manual, "Structuring forms": "Start by splitting the form across multiple pages with each page containing just one thing", and "User research will tell you when you can merge pages together"; USWDS, "Complete a complex form", Progress easily: "Only show questions on one micro-topic at a time"; Baymard, "Reasons for cart abandonment": "a one-page checkout with 30 form fields is often worse than a three-step checkout with well-designed forms" (all as read Oct 2026); strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Split a long form into pages of one thing each, one question, decision or piece of information; merge pages only where research shows visitors answer them together, and cut needless fields before adding steps.
- reasons: design-critique/references/forms-and-overlays.md#one-thing-per-page
- ledger: FRM-7
- status: staged

### vault.questions-per-page
- applies-when: web-surface; every page of a form that runs over several pages
- question: Does each page of a multi-page form ask one question, a fieldset or a label with its control counting as one, unless its h1 is a statement naming the related things the page groups rather than a question?
- answered-by: script
- writes: questions per page
- yields-to: vault.one-thing-per-page, level 2
- source: GOV.UK Design System, Question pages: "Start by asking one question per page", and "If you need to ask for multiple related things on a page, use a statement as the heading" (as read Oct 2026); strength: design-system guidance
- era: timeless
- owner: vault
- stage: value
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/forms-and-overlays.md#one-thing-per-page
- ledger: FRM-8
- status: staged

### vault.question-heading
- applies-when: web-surface; every form page that asks one question
- question: On a form page that asks one question, is that question's label or legend the page's h1 (the h1 inside the label or legend), with no separate heading repeating it, and on one that asks more than one, is no label or legend the h1?
- answered-by: script
- writes: question as page heading
- yields-to: level 2
- source: GOV.UK Design System, "Labels, legends and headings": "When you're asking just one question on a page, you can make the question the page's heading", setting "the contents of the `<label>` or `<legend>` as the page heading (except if you're asking more than one question on the page)" (as read Oct 2026); strength: design-system guidance
- era: timeless
- owner: vault
- stage: value
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/forms-and-overlays.md#the-question-is-the-heading
- ledger: FRM-29
- status: staged

### vault.error-summary-focus
- applies-when: web-surface; every form that checks its answers on submit
- question: When a form is submitted with errors, does an error summary appear at the top of the main content, below any breadcrumbs or back link and above the h1, and does keyboard focus move to it?
- answered-by: script
- writes: focus placement on submit with errors
- yields-to: level 2
- source: GOV.UK Design System, Error summary: "Put the error summary at the top of the `main` container", below breadcrumbs or a back link "but above the `<h1>`", and "move keyboard focus to the error summary" (as read Oct 2026); strength: design-system guidance
- era: timeless
- owner: vault
- stage: value
- script: check-state.py, its summary-focus line
- reasons: design-critique/references/forms-and-overlays.md#focus-on-the-error-summary
- ledger: STA-63
- status: staged

### vault.disabled-legibility
- applies-when: web-surface; every control a visitor cannot use right now, not content shown as unavailable, such as a full hostel's row, which keeps `vault.contrast`
- question: Does a disabled control look muted, a grey or desaturated fill and label at lower contrast than its live state, yet stay legible, and does one a visitor must learn the reason for stay focusable with `aria-disabled`?
- answered-by: look
- writes: disabled contrast
- yields-to: vault.disabled-dim, vault.disabled-look, level 2
- source: W3C Understanding SC 1.4.3 and 1.4.11, inactive components exempt and no one-size fix found (WCAG 2.2, 2023); NN/g, "Button States: Communicate Interaction" (25 Apr 2025, updated 18 Mar 2026), disabled labels "don't need to be as high-contrast" but readable, and not so high they look live; USWDS `u-disabled`, solid grey tokens kept at 5.8:1, no opacity, GrayText in forced colours (as read Oct 2026); Material 3 Compose tokens, OnSurface at 0.38 for content (2.3:1 light, 3.0:1 dark); Atlassian disabled tokens, 2.0:1; strength: design-system guidance, the 3:1 aim the house's guess between them
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Give disabled controls their own solid grey fill, edge and label tokens, the label near 3:1 and below the live state, keep a control whose reason the visitor needs focusable with `aria-disabled`, and never grey out content that is only unavailable.
- reasons: design-critique/references/edges-and-contrast.md#disabled-controls
- ledger: COL-65
- status: staged

### vault.disabled-dim
- applies-when: web-surface; every control a visitor cannot use right now, not content shown as unavailable, such as a full hostel's row, which keeps `vault.contrast`
- question: Is each disabled control drawn at full opacity, and each disabled button in a fill unlike every live button's?
- answered-by: script
- writes: disabled fill
- yields-to: none
- source: W3C Understanding SC 1.4.3 and 1.4.11, inactive components exempt and no one-size fix found (WCAG 2.2, 2023); NN/g, "Button States: Communicate Interaction" (25 Apr 2025, updated 18 Mar 2026), disabled labels "don't need to be as high-contrast" but readable, and not so high they look live; USWDS `u-disabled`, solid grey tokens kept at 5.8:1, no opacity, GrayText in forced colours (as read Oct 2026); Material 3 Compose tokens, OnSurface at 0.38 for content (2.3:1 light, 3.0:1 dark); Atlassian disabled tokens, 2.0:1; strength: design-system guidance, the 3:1 aim the house's guess between them
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Draw disabled controls in their own solid fill at full opacity, never an opacity over the live style.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/edges-and-contrast.md#disabled-controls
- ledger: COL-65
- status: staged
