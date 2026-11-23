# Rule records: buttons

Action controls: emphasis, size, labels, and how many a view holds. The form is [rules.md](../rules.md)'s.

### vault.primary-action
- applies-when: web-surface and has-cta; each view: the first screen and every screen below it, at desktop and phone width
- question: Does each view hold at most one part that looks like its main action, with no other part matching or outweighing it?
- answered-by: look
- writes: primary action
- yields-to: vault.action-colour
- source: Apple HIG, Buttons; GOV.UK Design System, Button; NN/g, "Visual Hierarchy in UX" (2021); the function walk's question 6; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Give each view one main action, and no other part its weight.
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: BTN-13, BTN-15, BTN-16, BTN-17, BTN-18, BTN-24, BTN-55, BTN-63, BTN-65, BTN-70, COL-23, FRM-32, IMG-105, IMG-120, NEW1-49, NEW3-75, OTH-20, PAG-38, PAG-68, STA-18, TXL-90, TYF-68
- status: live

### vault.action-colour
- applies-when: web-surface; every button with a coloured fill
- question: Do the page's buttons take two coloured fills at most (OKLCH chroma 0.05 or more), the one action colour and the danger hue?
- answered-by: script
- writes: action colour
- yields-to: none
- source: Apple HIG, Buttons; GOV.UK Design System, Button; NN/g, "Visual Hierarchy in UX" (2021); the function walk's question 6; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Give buttons one reserved action colour, with the danger hue the only other coloured fill.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: BTN-13
- status: live

### vault.carry-act
- applies-when: web-surface; every button and other part that acts on the page
- question: Does each button show that it acts by a fill or an edge (3:1 only where the edge is its one cue, the text rung taking none), a label that names its action or, on an icon-only button, a glyph at 3:1, a rung on one emphasis ladder (filled, tonal, outlined, text) and hover and press states, the primary action holding the view's strongest colour, and does no static tag, eyebrow or decorative pill take the button's shape, fill or type?
- answered-by: whole-page
- writes: act signifier
- yields-to: vault.primary-action, vault.borrowing, vault.border-roles
- source: Material 3 buttons, for the emphasis ladder; Apple HIG Color; W3C Understanding SC 1.4.11, for the edge that is a control's one cue and an icon's 3:1; NN/g 2018, on labels that name the action; #127 B7.2's carrier table; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: role
- target: Draw every button with a fill or an edge, 3:1 where nothing else shows it, and a label naming its action or an icon glyph at 3:1, on one emphasis ladder, the primary action in the view's strongest colour, with hover and press states; keep that shape and type off tags, eyebrows and pills.
- reasons: design-critique/references/house-principles.md#carriers-and-reserved-properties
- ledger: BTN-7, BTN-8, BTN-13, BTN-15, BTN-16, BTN-17, BTN-55, BTN-63, BTN-64, BTN-65, BTN-70, COL-23, COL-67, FCH-28, NEW1-49, NEW3-75, OTH-20, STA-18, STA-20
- status: live

### vault.action-on-dark
- applies-when: web-surface; every button on a dark or brand-coloured ground: a night section, a dark nav or footer, a brand-colour hero
- question: On a dark or brand-coloured ground, does each button take the inverse treatment, a light fill or a light edge and label, its fill or edge at 3:1 against the ground where that is its one cue?
- answered-by: script
- writes: button colour on a dark ground
- yields-to: level 2
- source: GOV.UK Design System, Button, the inverse modifier, "white buttons on dark backgrounds", and USWDS Button, the inverse and outline-inverse variants, "light color button for dark backgrounds" (both as read Oct 2026); W3C Understanding SC 1.4.11, for the edge that is a control's one cue; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: On a dark or brand-coloured ground, draw buttons light: a light fill, or a light edge and label for the secondary rung, 3:1 against the ground where the edge is the only cue.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: button
- reasons: design-critique/references/surface-styling.md#buttons-on-a-dark-ground
- ledger: BTN-9
- status: staged

### vault.disabled-look
- applies-when: web-surface; every control that can be unavailable
- question: Does each control that can be unavailable have its own disabled look, plainly unlike its default, hover and every rung of the emphasis ladder and with no hover or press change, and does the page say why it is unavailable and how to make it available?
- answered-by: look
- writes: disabled look
- yields-to: level 2
- source: USWDS Button, a Disabled state on every variant and "Keep unavailable actions understandable. Explain why an action is unavailable and how to make it available" (as read Oct 2026); web.dev, Learn Accessibility, "Design and UX", "identify default, hover, active, focus, and disabled states" (2022); W3C Understanding SC 1.4.3, disabled controls exempt from contrast; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Draw a disabled state for every control that can be unavailable, unlike every live state, and say beside it why and how to unlock it.
- parts: button, textbox, combobox, checkbox, radio, switch, slider
- reasons: design-critique/references/surface-styling.md#disabled-controls
- ledger: BTN-70
- status: staged

### vault.button-group-size
- applies-when: web-surface; every group of two or more buttons offered together: a dialog's actions, a form's submit and cancel, a hero's pair, a segmented set
- question: Do the buttons in each group share one height and one corner shape, the preferred choice marked by its emphasis rung rather than by a larger size?
- answered-by: script
- writes: button size within a group
- yields-to: level 2
- source: Apple HIG Buttons (16 Dec 2025, as read Oct 2026): "Use style — not size — to visually distinguish the preferred choice among multiple options", as two sizes side by side "can make the interface look confusing and inconsistent"; IBM Carbon, Button usage (15 Oct 2026): "We do not recommend mixing different button sizes in button groups"; material-components-android `ButtonGroup.md` (as read Oct 2026): a group "Applies default shape to all buttons"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Give every button in a group the same height and corner shape, and mark the preferred one by a stronger rung on the emphasis ladder, never by size.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: button
- reasons: design-critique/references/surface-styling.md#one-size-in-a-button-group
- ledger: BTN-41
- status: staged

### vault.button-icon-side
- applies-when: web-surface; every button that carries one icon and a label
- question: Do the page's labelled buttons that carry an icon all put it on one side of the label, save a forward arrow, which sits after it?
- answered-by: script
- writes: button icon side
- yields-to: vault.carry-act, level 2
- source: Atlassian Button usage (as read Oct 2026): an icon "before or after the label"; material-components-android `CommonButton.md`: icons "on the leading side of the button, before the label text"; IBM Carbon Button usage (15 Oct 2026): icons in a labelled button are "right-aligned"; GOV.UK Design System, the start button's arrow after "Start now"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Put every button's icon on one side of its label, before it unless the design system says after, and a forward arrow after the label.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- parts: button
- reasons: design-critique/references/surface-styling.md#icons-on-buttons
- ledger: BTN-54
- status: staged

### vault.button-icon
- applies-when: web-surface; every button that carries an icon and a label
- question: Does each button carry an icon only where the icon's meaning is well established, always beside a visible label?
- answered-by: look
- writes: button icon meaning
- yields-to: vault.button-icon-side, vault.carry-act, level 2
- source: Atlassian Button usage (as read Oct 2026): an icon "before or after the label", and "Most buttons don't need an icon. Use an icon … where the icon has a clear and well-established meaning"; material-components-android `CommonButton.md`: icons "on the leading side of the button, before the label text"; IBM Carbon Button usage (15 Oct 2026): icons in a labelled button are "right-aligned"; GOV.UK Design System, the start button's arrow after "Start now"; NN/g, Harley, "Icon Usability" (2014): "a text label must be present alongside an icon"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Add an icon to a button only where its meaning is well established, and keep the label beside it.
- parts: button
- reasons: design-critique/references/surface-styling.md#icons-on-buttons
- ledger: BTN-54
- status: staged

### vault.consistent-help
- applies-when: web-surface; every help route a page repeats across the site's pages: contact details, a contact or help link, a chat, a self-help page or a help button
- question: Does each help route the site repeats sit in the same order relative to the other page content on every page?
- answered-by: code
- writes: help placement
- yields-to: none
- source: WCAG 2.2 success criterion 3.2.6 Consistent Help and its Understanding page (updated 9 Mar 2026, as read Oct 2026): help "repeated on multiple web pages" occurs "in the same order relative to other page content", which "does not require that a site provide a help mechanism"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: role
- target: Put each help route in the shared header, footer or layout template so it keeps one place in the source order on every page.
- reasons: design-critique/references/page-behaviour.md#help-in-one-place
- ledger: BTN-114
- status: live

### vault.help-button
- applies-when: web-surface; every view with a help button
- question: Does each view hold at most one help button?
- answered-by: script
- writes: help button count
- yields-to: vault.consistent-help, level 2
- source: Apple HIG Buttons, Help buttons (as read Oct 2026): "Include no more than one help button per window", and open "the help topic that's related to the current context"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Give a view at most one help button.
- parts: button
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/page-behaviour.md#help-in-one-place
- ledger: BTN-114
- status: staged

### vault.help-button-target
- applies-when: web-surface; every view with a help button
- question: Does each view's help button open the help for that view rather than a general help page, where such help exists?
- answered-by: look
- writes: help button target
- yields-to: vault.help-button, vault.consistent-help, level 2
- source: Apple HIG Buttons, Help buttons (as read Oct 2026): open "the help topic that's related to the current context"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Point a view's help button at the help for that view.
- parts: button
- reasons: design-critique/references/page-behaviour.md#help-in-one-place
- ledger: BTN-114
- status: staged

### vault.bottom-safe-area
- applies-when: web-surface; every control pinned to the bottom of a phone's viewport: a sticky call to action, a bottom nav, a bottom sheet's or a toast's buttons
- question: On a phone, does each control pinned to the viewport's bottom edge stay clear of the browser toolbar and the device's edges, padded by `env(safe-area-inset-bottom)` where the page sets `viewport-fit=cover`, and laid out against `svh` or `dvh` rather than `lvh` or plain `vh` where it is placed by the viewport's height?
- answered-by: script
- writes: bottom inset of a pinned control
- yields-to: level 2
- source: web.dev, Learn Forms, "Make sure form buttons aren't hidden" (2021): the submit button "may be behind the browser toolbar", and env() keeps it visible; MDN, env() (as read Oct 2026): the safe-area insets are above 0 where "toolbars or dynamic keyboards" take viewport space; MDN, the viewport meta tag: with `viewport-fit=cover` "It's highly recommended to use the safe area inset variables"; MDN, `<length>` (modified 8 Jul 2026): with large viewport units "the content might get hidden when browser interfaces expand", and "all default viewport units (vh, vw, etc.) are equivalent to their large viewport counterparts"; W3C, CSS Values and Units Level 4 (WD 12 Mar 2024) §6.1.2.1: "The large viewport-percentage units (lv*) and default viewport-percentage units (v*) are defined with respect to the large viewport size"; the 34 px inset the check emulates: Harrison, Use Your Loaf, "Supporting iPhone X" (18 Sep 2017): "our safe area now has a 34 point inset at the bottom", and "iPhone 16 Screen Sizes" (16 Sep 2024): "Safe Area Insets (portrait): top: 59, bottom: 34", one author's measurements, as no Apple page read (HIG Layout, UIKit safe-area docs, the 2017 iPhone X tech talk, WWDC18 session 235) states the figure; web-features: small, large and dynamic viewport units Baseline widely available since 2025-06-05; strength: platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Pad a control pinned to a phone's bottom edge by `env(safe-area-inset-bottom)` wherever the page sets `viewport-fit=cover`, and place anything sized by the screen's height in `svh` or `dvh`, never `lvh` or plain `vh`, so no browser toolbar covers it.
- script: check-layout.py <page> --out <dir> --records
- parts: button, nav, toast, bottom-sheet
- reasons: design-critique/references/controls-and-feedback.md#clear-of-the-phones-edges
- ledger: BTN-34
- status: staged

### vault.button-group-stack
- applies-when: web-surface; a group of two or more buttons side by side, at phone width
- question: At phone width, does a button group that cannot sit in one row stack into a column of full-width buttons, rather than wrapping into a ragged row or overflowing, two buttons with short labels staying side by side where both fit?
- answered-by: script
- writes: button group direction at narrow widths
- yields-to: level 2
- source: USWDS, Button group (updated 19 Dec 2024): "On mobile devices, the buttons are arranged vertically", "The default button group will display as a column on smaller screen sizes"; Apple HIG, Layout, watchOS (updated 9 Sep 2026): "it's usually better to let text buttons span the full width of the screen", "two side-by-side buttons with short text labels can also work well", written for watchOS, which the house applies to phone widths; strength: design-system guidance, with a house mapping from watchOS
- era: timeless
- owner: vault
- stage: treatment
- target: At phone width, stack a button group into full-width buttons in one column, unless two short-label buttons fit side by side.
- script: check-layout.py <page> --out <dir> --records
- parts: button
- reasons: design-critique/references/responsive-structure.md#button-groups-stack
- ledger: BTN-39
- status: staged

### vault.destructive-action
- applies-when: web-surface; every button that deletes data or does what a visitor cannot easily undo
- question: Does each destructive button take a secondary or text rung wherever it sits beside other actions, never the primary style even where it is the likeliest choice, with the danger hue on a filled button kept for the final confirmation of the loss, and a label naming that loss so the red is never its only cue?
- answered-by: look
- writes: destructive action style
- yields-to: vault.destructive-fill, vault.dialog-default, level 2
- source: Apple HIG, Buttons (updated 16 Dec 2025): "Don't assign the primary role to a button that performs a destructive action, even if that action is the most likely choice", since "people sometimes choose a primary button without reading it first", and "a destructive button uses the system red color"; GOV.UK Design System, Button, Warning buttons (as read Nov 2026): "Only use warning buttons for actions with serious destructive consequences that cannot be easily undone", "use another style of button for the initial call to action, and a warning button for the final confirmation", "Do not only rely on the red colour"; Refactoring UI, "7 Practical Tips for Cheating at Design" (20 Feb 2018), tip 7: a destructive action that is not the primary one takes "a secondary or tertiary button treatment", the "big, red, and bold styling" kept for a confirmation dialog; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Give a destructive action a secondary or text button beside other actions, never the primary style; use a filled danger-hue button only on the final confirmation, its label saying what is lost.
- reasons: design-critique/references/controls-and-feedback.md#destructive-actions
- ledger: BTN-13, BTN-16, BTN-21
- status: staged

### vault.destructive-fill
- applies-when: web-surface; every button that deletes data or does what a visitor cannot easily undo
- question: Does each destructive button take a fill other than the main action's?
- answered-by: script
- writes: destructive action style
- yields-to: none
- source: Apple HIG, Buttons (updated 16 Dec 2025): "Don't assign the primary role to a button that performs a destructive action, even if that action is the most likely choice", since "people sometimes choose a primary button without reading it first", and "a destructive button uses the system red color"; GOV.UK Design System, Button, Warning buttons (as read Nov 2026): "Only use warning buttons for actions with serious destructive consequences that cannot be easily undone", "use another style of button for the initial call to action, and a warning button for the final confirmation", "Do not only rely on the red colour"; Refactoring UI, "7 Practical Tips for Cheating at Design" (20 Feb 2018), tip 7: a destructive action that is not the primary one takes "a secondary or tertiary button treatment", the "big, red, and bold styling" kept for a confirmation dialog; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Never give a destructive button the main action's fill.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/controls-and-feedback.md#destructive-actions
- ledger: BTN-21
- status: staged

### vault.button-size
- applies-when: web-surface; every button, and every link styled as one
- question: Do the page's buttons take three heights at most: the compact, the ordinary and one step larger?
- answered-by: script
- writes: button size
- yields-to: vault.target-size, vault.button-group-size, level 2
- source: GOV.UK Design System, Button, Start buttons, "for the main call to action on your service's Start page", and govuk-frontend `button/_mixin.scss` (as read Nov 2026), the start button set at 24 px bold against the default 19 px; USWDS Button (as read Nov 2026): "Give an important action a distinctive style … Try using the usa-button--big variant"; Atlassian Button, "Consider button sizes in context" (as read Nov 2026): "large enough to interact with but not visually overwhelming. There is a compact button for tight spaces"; Material 3 Expressive buttons, five sizes from extra small to extra large (material-components-android CommonButton.md, as read Nov 2026); strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Size buttons by place: one step larger only for a standalone key action such as a start or hero call to action, compact only in dense rows, the ordinary size everywhere else.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: button, link
- reasons: design-critique/references/controls-and-feedback.md#button-size-by-place
- ledger: BTN-20, BTN-52
- status: staged

### vault.button-place
- applies-when: web-surface; every button, and every link styled as one
- question: Does each button take the size its place gives it: a larger size only for a standalone key action (a start or hero call to action, a floating action), and a compact size only in dense rows and tight spaces?
- answered-by: look
- writes: button size
- yields-to: vault.button-size, vault.target-size, vault.button-group-size, level 2
- source: GOV.UK Design System, Button, Start buttons, "for the main call to action on your service's Start page", and govuk-frontend `button/_mixin.scss` (as read Nov 2026), the start button set at 24 px bold against the default 19 px; USWDS Button (as read Nov 2026): "Give an important action a distinctive style … Try using the usa-button--big variant"; Atlassian Button, "Consider button sizes in context" (as read Nov 2026): "large enough to interact with but not visually overwhelming. There is a compact button for tight spaces"; Material 3 Expressive buttons, five sizes from extra small to extra large (material-components-android CommonButton.md, as read Nov 2026); strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Size buttons by place: one step larger only for a standalone key action such as a start or hero call to action, compact only in dense rows, the ordinary size everywhere else.
- inputs: its role (standalone key action, ordinary action, an action in a dense row or toolbar); the project's button size steps; the target floor from `vault.target-size`
- output: a standalone key action one step above the ordinary size (GOV.UK's start button 24 px type against 19 px); a dense row or toolbar the compact step; every other button the ordinary size; inside a group, the size `vault.button-group-size` gives
- reasons: design-critique/references/controls-and-feedback.md#button-size-by-place
- ledger: BTN-52
- status: staged
