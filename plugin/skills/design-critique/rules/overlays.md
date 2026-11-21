# Rule records: overlays

Layers that open over the page: menus, dialogs, sheets and popovers, and the scrim behind them. The form is [rules.md](../rules.md)'s.

### vault.scrim
- applies-when: web-surface; every scrim behind a modal surface
- question: Does every modal in the product share one scrim colour and opacity, neutral black or the brand's dark at about 32–70% or a light grey for a light, low-drama brand, sitting at the darker end over a busy or bright backdrop and the lighter under a modal with a strong edge or shadow, and is the page behind only dimmed, never blurred or scaled back?
- answered-by: builder
- writes: scrim
- yields-to: level 2
- source: Material 3 `ScrimTokens` (0.32), Atlassian `blanket` (0.46), Carbon `overlay` (0.6), Polaris `backdrop-bg` (0.71), Primer `overlay-backdrop` (a light grey at 0.4), Apple HIG Materials; each of these web systems dims and none blurs or scales the page, and Apple HIG Sheets' scale-back is iOS's own sheet; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: treatment
- target: Define one scrim token for the product and use it behind every modal, dimming the page without blurring or scaling it.
- reasons: design-critique/references/surface-styling.md#one-scrim-token
- ledger: COL-11, COL-33, SUR-90
- status: live

### vault.grabber
- applies-when: web-surface; every resizable sheet the round declares
- question: Is the topmost thing drawn in each declared resizable sheet a button, its grabber?
- answered-by: script
- writes: sheet grabber presence
- yields-to: vault.drag-alternative, level 2
- source: Apple HIG Sheets (24 Mar 2026): "Include a grabber in a resizable sheet", which people "can also tap ... to cycle through the detents"; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: role
- target: Put a grabber button at the top edge of every resizable sheet.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/interaction-and-forms.md#every-drag-has-a-tap-path
- ledger: NEW3-48
- status: staged

### vault.sheet-grabber
- applies-when: web-surface; every bottom sheet or panel a visitor can resize by dragging
- question: Does each resizable sheet show a grabber at its top edge that a tap or click on cycles through its resting heights, a named button to screen readers, drawn at 3:1 against the sheet where it is the only sign the sheet resizes?
- answered-by: look
- writes: sheet grabber
- yields-to: vault.grabber, vault.drag-alternative, level 2
- source: Apple HIG Sheets (24 Mar 2026): "Include a grabber in a resizable sheet", which people "can also tap ... to cycle through the detents", and which "works with VoiceOver"; WCAG 2.2 (2023) SC 2.5.7 Dragging Movements, and SC 1.4.11 Non-text Contrast for a grabber that alone identifies the control; strength: design-system guidance over WCAG 2.2 AA
- era: dated 2027-10-19
- owner: vault
- stage: role
- target: Put a grabber on every resizable sheet, a button that cycles the sheet's heights on tap, at 3:1 against the sheet.
- reasons: design-critique/references/interaction-and-forms.md#every-drag-has-a-tap-path
- ledger: NEW3-48
- status: staged
### vault.dialog-default
- applies-when: web-surface; every dialog, alert or confirmation that offers two or more buttons
- question: In each dialog, is the default button (the one Return activates or that takes focus when the dialog opens) never Cancel, Close, Dismiss, No or Not now?
- answered-by: script
- writes: dialog default button
- yields-to: level 2
- source: Apple HIG Alerts (updated 2 Feb 2024, as read Oct 2026): "Always place the default button on the trailing side of a row or at the top of a stack", "you don't want to make a Cancel button the default button", and the destructive style for "a destructive action people didn't deliberately choose"; Apple HIG Buttons (16 Dec 2025): "Don't assign the primary role to a button that performs a destructive action, even if that action is the most likely choice"; W3C WAI-ARIA Authoring Practices, Dialog (Modal) pattern: for a step "not easily reversible" it "may be advisable" to set focus on the least destructive action; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Make a dialog's default and first-focused button the action the visitor came for, never Cancel; where the action destroys what the visitor did not choose to destroy, give it the danger style off the primary rung; where it cannot be undone, focus may open on the least destructive button.
- script: check-state.py, its default line
- reasons: design-critique/references/house-principles.md#the-default-button-in-a-dialog
- ledger: BTN-23
- status: live

### vault.dialog-default-look
- applies-when: web-surface; every dialog, alert or confirmation whose action destroys something
- question: Is an action that destroys something the visitor did not deliberately choose to destroy neither the dialog's default button nor in the primary style, and is the default otherwise the action the visitor most likely came to take?
- answered-by: look
- writes: dialog destructive style
- yields-to: vault.dialog-default
- source: Apple HIG Alerts (updated 2 Feb 2024, as read Oct 2026): "Always place the default button on the trailing side of a row or at the top of a stack", "you don't want to make a Cancel button the default button", and the destructive style for "a destructive action people didn't deliberately choose"; Apple HIG Buttons (16 Dec 2025): "Don't assign the primary role to a button that performs a destructive action, even if that action is the most likely choice"; W3C WAI-ARIA Authoring Practices, Dialog (Modal) pattern: for a step "not easily reversible" it "may be advisable" to set focus on the least destructive action; strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Give an action that destroys what the visitor did not choose to destroy the danger style off the primary rung; where it cannot be undone, focus may open on the least destructive button.
- reasons: design-critique/references/house-principles.md#the-default-button-in-a-dialog
- ledger: BTN-23
- status: live

### vault.menu-click
- applies-when: web-surface; every navigation dropdown or submenu
- question: Does every navigation dropdown open on click, tap or the keyboard, and never on hover alone?
- answered-by: script
- writes: menu open trigger
- yields-to: level 2
- source: USWDS Header, accessibility (as read Oct 2026; its latest listed update 23 May 2025): "Avoid using hover to expand dropdown lists. Dropdowns should expand on click or with keyboard navigation."; strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Open a navigation dropdown from a button on click, tap, Enter or Space; never from hover alone.
- script: check-state.py, its click-opens line
- reasons: design-critique/references/page-behaviour.md#menus-open-on-click
- ledger: NAV-103
- status: live

### vault.dialog-name
- applies-when: web-surface; every dialog
- question: Is every dialog a native dialog element, or an element with role="dialog" and aria-modal="true" where it blocks the page, and does each have an accessible name, from aria-labelledby pointing at its visible title or from aria-label?
- answered-by: script
- writes: dialog role and name
- yields-to: none
- source: WAI-ARIA APG, Dialog (Modal) pattern: "The element that serves as the dialog container has a role of dialog", aria-modal true, and a name from "aria-labelledby ... that refers to a visible dialog title" or "aria-label"; MDN, `<dialog>` (last modified 2 Oct 2026): implicit role dialog, and `showModal()` gives aria-modal true (both as read Oct 2026); strength: W3C authoring practice and platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: value
- script: check-state.py, its dialog-name line
- reasons: design-critique/references/forms-and-overlays.md#dialog-role-and-name
- ledger: NAV-151
- status: staged

### vault.submenu-close
- applies-when: web-surface; every menu that opens a submenu or a nested popover
- question: Does closing a menu, by Tab or by closing its parent, also close every submenu it opened?
- answered-by: script
- writes: submenu closing
- yields-to: none
- source: WAI-ARIA APG, Menu and Menubar pattern: Tab will "close all menus and submenus"; web.dev, Learn CSS, "Popover and dialog", Nested popovers: "Closing a popover also closes all popovers after it in the stack" (both as read Oct 2026); strength: W3C authoring practice and platform documentation
- era: timeless
- owner: vault
- stage: function
- target: Close every submenu with the menu that opened it; built from nested auto popovers, the browser does this.
- script: check-state.py, its submenu line
- reasons: design-critique/references/forms-and-overlays.md#menus-close-together
- ledger: NAV-115
- status: live

### vault.interruptions
- applies-when: web-surface; every pop-up, banner or update the page shows that the visitor did not ask for: an offer or sign-up modal, a live update, a chat prompt
- question: Can the visitor postpone or turn off every interruption the page shows unasked, an emergency alone excepted?
- answered-by: script
- writes: interruption control
- yields-to: level 2
- source: WCAG 2.2 SC 2.2.4 Interruptions (AAA): "Interruptions can be postponed or suppressed by the user, except interruptions involving an emergency" (as read Oct 2026); strength: house rule over WCAG 2.2 AAA
- era: timeless
- owner: vault
- stage: function
- target: Give every pop-up, banner or update the visitor did not ask for a way to put it off or turn it off, unless it reports an emergency.
- script: check-state.py, its interrupt line
- reasons: design-critique/references/forms-and-overlays.md#interruptions
- ledger: NAV-139
- status: live

### vault.nav-order
- applies-when: web-surface; every navigation menu or bar repeated on more than one page of the site
- question: Does each navigation repeated across the site's pages keep its items in the same relative order on every page, items added or removed aside, unless the visitor changed it?
- answered-by: script
- writes: navigation order across pages
- yields-to: none
- source: WCAG 2.2 SC 3.2.3 Consistent Navigation (AA): repeated navigation occurs "in the same relative order each time" (as read Oct 2026); strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: value
- script: check-cross.py <home page>
- reasons: design-critique/references/forms-and-overlays.md#repeated-navigation-keeps-its-order
- ledger: NAV-106
- status: staged

### vault.menu-ellipsis
- applies-when: web-surface; every menu item, and every label showing an action in progress
- question: Does each menu item whose command asks for more input or a confirmation before it completes (Print…, Save as…) end with the ellipsis character "…", while an item that acts at once, opens a submenu or only shows a window (About) takes none, and does a status label showing an action in progress read as an -ing verb and the same character (Saving…), a button with a spinner changing its verb with none?
- answered-by: script
- writes: label ellipsis
- yields-to: level 2
- source: Apple HIG, Menus: "Append an ellipsis to a menu item's label when the action requires more information before it can complete"; Microsoft Windows UX guidelines, Menus, Using ellipses: a command "that needs additional information (including a confirmation)", and "Menu items that display submenus never have an ellipsis"; Siemens iX, Progress updates: "Use horizontal ellipses (…) after the verb without a space", none for time remaining, and "Change verb form without ellipses when possible in buttons with loading spinners" (all as read Oct 2026); strength: platform convention
- era: timeless
- owner: vault
- stage: value
- script: check-state.py, its ellipsis line
- reasons: design-critique/references/forms-and-overlays.md#ellipses-on-menu-items
- ledger: VG-NEW-1
- status: staged

### vault.cookie-banner
- applies-when: web-surface; the whole site: every cookie, local storage entry and other store it sets on a visitor's device, analytics and advertising storage counted as needing consent, as it does for EU visitors
- question: Does the site show a cookie banner only where it sets storage that needs consent, leaving it out where it sets only strictly necessary storage, and does a footer link reach a cookies page?
- answered-by: script
- writes: cookie banner presence
- yields-to: none
- source: UK PECR as amended by the Data (Use and Access) Act 2025, per the ICO, "Guidance on the use of storage and access technologies" (finalised 29 Apr 2026), "What are the exceptions?": strictly necessary storage needs no consent, and the new statistical and appearance exceptions need "clear and comprehensive information" and "an easy way to object"; EU ePrivacy Directive art. 5(3): strictly necessary storage exempt, with no exception for analytics; GOV.UK Design System, Cookie banner, Option 1: no banner for essential cookies alone, "However, you must tell users that you set essential cookies ... with a cookies page – link to this page in the footer"; strength: law for when consent is owed, design-system guidance for leaving the banner out and for the cookies page
- era: dated 2027-10-19
- owner: vault
- stage: function
- target: Show a cookie banner only if the site sets storage needing consent, analytics included; with strictly necessary storage alone, leave the banner out; always link a cookies page from the footer.
- script: check-load.py <page> --files --out <dir> [--parts <declaration>]
- reasons: design-critique/references/controls-and-feedback.md#a-cookie-banner-only-for-consent
- ledger: NAV-144
- status: live

### vault.cookies-page
- applies-when: web-surface; the cookies page, and a UK-only site's statistics and appearance storage
- question: Does the cookies page say what the site sets and why, and where a UK-only site sets statistics or appearance storage with no banner, does it give clear information and an easy way to object?
- answered-by: code
- writes: cookies page content
- yields-to: none
- source: UK PECR as amended by the Data (Use and Access) Act 2025, per the ICO, "Guidance on the use of storage and access technologies" (finalised 29 Apr 2026), "What are the exceptions?": strictly necessary storage needs no consent, and the new statistical and appearance exceptions need "clear and comprehensive information" and "an easy way to object"; EU ePrivacy Directive art. 5(3): strictly necessary storage exempt, with no exception for analytics; GOV.UK Design System, Cookie banner, Option 1: no banner for essential cookies alone, "However, you must tell users that you set essential cookies ... with a cookies page – link to this page in the footer"; strength: law for when consent is owed, design-system guidance for leaving the banner out and for the cookies page
- era: dated 2027-10-19
- owner: vault
- stage: function
- target: Say on the cookies page what each store is and why it is set; on a UK-only site that sets statistics or appearance storage without a banner, explain it there with an easy way to object.
- reasons: design-critique/references/controls-and-feedback.md#a-cookie-banner-only-for-consent
- ledger: NAV-144
- status: live
