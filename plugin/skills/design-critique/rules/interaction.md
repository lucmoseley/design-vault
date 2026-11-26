# Rule records: interaction

How controls answer the user: what looks actable, targets, keyboard and focus. The form is [rules.md](../rules.md)'s.

### vault.affordance
- applies-when: web-surface; each part on the parts map's key, at desktop and phone width, answered part by part
- question: Does every part a visitor can act on look as if they can, and every part they cannot look as if they cannot, save a hidden link that goes where a part that does look actable also goes, which is reported and does not fail?
- answered-by: look
- writes: affordance
- yields-to: none
- source: Gaver, "Technology Affordances" (CHI '91), on hidden and false affordances; NN/g, "Beyond Blue Links" (2015); the function walk's question 2; strength: peer-reviewed research and NN/g guidance
- era: timeless
- owner: vault
- stage: function
- target: Make every part a visitor can act on look actable, and every part they cannot look static.
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: BTN-7, FRM-87, FRM-90, FRM-92, IMG-104, NAV-16, STA-19
- status: live

### vault.one-target
- applies-when: web-surface; every part a visitor can act on, at desktop and phone width
- question: Does every tap target carry one action, with no target nested inside a link, button or other clickable part, or set inside the area where one takes the click?
- answered-by: script
- writes: tap target
- yields-to: none
- source: the HTML Living Standard's content model for `a` and `button`; NN/g, "Beyond Blue Links" (2015); the function walk's question 8; strength: HTML standard
- era: timeless
- owner: vault
- stage: function
- target: Give each tap target one action, with no clickable part nested in another or in its click area.
- script: parts-map.py
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: IMG-104, IMG-105, NAV-99, NEW3-11
- status: live

### vault.target-size
- applies-when: web-surface; every link, button and form control, and every other part a visitor clicks or tabs to, a chart mark included, at desktop and phone width
- question: Is every target at least 24 by 24 px, a chart mark's hit area counting where it reaches past the mark, or spaced so that a 24 px circle on its centre reaches no other target and no other small target's circle, save a link inside a line of text and a form control left at the size the browser gives it?
- answered-by: script
- writes: target size
- yields-to: none
- source: WCAG 2.2 success criterion 2.5.8 Target Size (Minimum); strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: value
- script: check-access.py
- reasons: design-round/references/impeccable.md#conditions-added
- ledger: BTN-52, BTN-95, IMG-65, LAY-163, NEW1-44, NEW1-68, STA-47, TXL-18
- status: live

### vault.keyboard
- applies-when: web-surface; every link, button, form control and part that acts on a click or tap, at desktop and phone width
- question: Does the Tab key reach every part a visitor can act on with a pointer, or a part that does the same thing?
- answered-by: script
- writes: keyboard reach
- yields-to: none
- source: WCAG 2.2 success criterion 2.1.1 Keyboard; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Put every part a pointer can act on, or a twin that does the same, in the Tab order.
- script: check-access.py
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: BTN-81, NAV-20, NEW1-68, NEW2-34, NEW3-12, OTH-27
- status: live

### vault.focus
- applies-when: web-surface; every part the Tab key reaches, walking forward and back, at desktop and phone width
- question: When a part takes focus, do pixels on or around it change by 3:1 or more to show it, and is the part not wholly hidden under a sticky bar or anything else the page draws?
- answered-by: script
- writes: focus indicator
- yields-to: none
- source: WCAG 2.2 (2023) success criteria 2.4.7 Focus Visible and 2.4.11 Focus Not Obscured (Minimum), and 1.4.11 Non-text Contrast for the indicator's 3:1, read as the change from unfocused to focused, the measure of 2.4.13 Focus Appearance (AAA); WCAG 2.2 failure F78 (as read Nov 2026), the browser's own indicator "rendered non-visible by other styling on the page", its Example 3 a border that hides it; measured on design-vault#424: in a light colour scheme Chromium 149 paints its 2 px #101010 ring over a button's border, so a transparent border shows the fill beneath it, a 1.45:1 change on #0a3542, while a button with no border has 1 px of the ring outside it; strength: WCAG 2.2 AA and a measurement
- era: timeless
- owner: vault
- stage: treatment
- target: Give every part the Tab key reaches a focus indicator whose pixels change by 3:1, kept clear of sticky bars.
- script: check-access.py
- reasons: design-critique/references/surface-styling.md#focus-rings-per-ground-clear-of-sticky-bars
- ledger: BTN-11, BTN-70, COL-2, COL-53, COL-58, LAY-107, STA-1, STA-2, STA-3, STA-4, STA-5, STA-7, STA-8, STA-11, SUR-1, SUR-49
- status: live

### vault.findable-action
- applies-when: web-surface; every action the page's task needs, at desktop and phone width
- question: Will a visitor who wants each action the page's task needs see that it is here, and connect the part that does it with that action?
- answered-by: whole-page
- writes: action discoverability
- yields-to: vault.affordance
- source: the cognitive walkthrough, Wharton et al. 1994; strength: published research
- era: timeless
- owner: vault
- stage: function
- target: Put each action the task needs where a visitor looks for it, labelled in the words they would use for it.
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: BTN-44
- status: live

### vault.carry-select
- applies-when: web-surface; every checkbox, radio, filter chip, switch and sort control, and every selected state
- question: Does each selectable control show its selected state by more than colour (a check, a dot, a 3:1 edge or a weight change, any pale selected tint paired with one of them), filters taking the chip shape, and does no static fact take the selectable chip's shape, fill or edge, no row the selected tint, and no list a column of check marks?
- answered-by: whole-page
- writes: select signifier
- yields-to: vault.colour-look, vault.borrowing
- source: W3C Understanding SC 1.4.1 and 1.4.11; Material 3 chips, "Chips aren't buttons" (m3.material.io, as read Oct 2026); GOV.UK Tag; #127 B7.2's carrier table; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: role
- target: Show a selected state by a check, a dot, a 3:1 edge or a weight change as well as any tint, give filters the chip shape, and keep that shape, the selected tint and check-mark columns off static facts.
- reasons: design-critique/references/house-principles.md#carriers-and-reserved-properties
- ledger: BTN-66, BTN-68, BTN-74, COL-2, COL-4, COL-36, COL-63, FCH-9, IMG-179, NAV-4, NAV-16, NAV-114, NAV-158, NAV-262, NEW1-46, NEW2-45, NEW3-6, OTH-20, OTH-21, OTH-23, STA-34, SUR-25, TYF-66
- status: live

### vault.hover-signal
- applies-when: web-surface; every part with a hover state
- question: Does hover change the surface tint, the elevation or both, whichever the project's rules file picks, with a small part (a chip, a checkbox, a small button) changing colour and never shadow, and elevation changing only on a large surface at the rest or raised level, never on an overlay?
- answered-by: builder
- writes: hover signal
- yields-to: level 2
- source: Atlassian Elevation (atlassian.design, as read Oct 2026), on hover by surface colour or by an elevation transition, never on an overlay or very small UI; Polaris depth, Material 3 `ElevatedCardTokens` and `StateTokens`; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: treatment
- target: On hover, change tint, elevation or both as the rules file picks, and where it picks neither, ask the founder rather than choose; change only colour on a small part; never raise an overlay.
- reasons: design-critique/references/surface-styling.md#hover-signals
- ledger: BTN-70, BTN-71, COL-43, COL-67, MOT-35, OTH-21, STA-18, STA-20, STA-22, STA-32
- status: live

### vault.press-state
- applies-when: web-surface; every part a visitor can press or tap
- question: Does a press, touch included, go down (a smaller shadow, a darker fill or a slight scale-down) and never up, in the project's own pressed state, with no ripple unless the project's value system holds one?
- answered-by: builder
- writes: press feedback
- yields-to: level 2
- source: Atlassian, Polaris and Material 3 state tokens; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: treatment
- target: Show every press by the project's own pressed state, moving down: a smaller shadow, a darker fill or a slight scale-down.
- reasons: design-critique/references/surface-styling.md#hover-signals
- ledger: BTN-70, BTN-71, COL-43, COL-67, MOT-35, NAV-46, OTH-21, STA-18, STA-20, STA-32
- status: live

### vault.control-states
- applies-when: web-surface; every button, link and field
- question: Does each button, link and field show a hover and a focus state unlike its rest state, each button and link a press state unlike its rest and hover states, and each disabled control a look unlike its live one?
- answered-by: script
- writes: control state set
- yields-to: vault.press-state, vault.hover-signal, vault.focus, vault.disabled-look
- source: USWDS, Button, Usability guidance (as read Oct 2026): default, hover, active, focus and disabled states; web.dev Learn Accessibility, Design and UX, accessibility annotations (as read Oct 2026): every interactive state designed; strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Give every control distinct rest, hover, focus and press states, and a disabled look apart from its live one.
- script: check-state.py, its states line
- reasons: design-critique/references/surface-styling.md#hover-signals
- ledger: BTN-70, OTH-20
- status: staged

### vault.toggle-state
- applies-when: web-surface; every toggle button (`aria-pressed`)
- question: Does pressing each toggle button flip its `aria-pressed`, its on and off states differing by more than colour: a weight, an outline, an inset, a mark or its text?
- answered-by: script
- writes: toggle state
- yields-to: vault.emphasis-weight
- source: Apple HIG Toggles (29 Mar 2024): "Make sure the visual differences in a toggle's state are obvious"; Material 3, Buttons, Toggle buttons, and Icon buttons, Icon accessibility requirements (as read Oct 2026): a selected state shown by more than colour; WCAG 2.2 1.4.1 Use of Color; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Flip `aria-pressed` on press and mark the on state by a weight, outline, inset, mark or text, not colour alone.
- script: check-state.py, its toggle line
- reasons: design-critique/references/typeface-traits.md#emphasis-takes-bold
- ledger: BTN-74
- status: staged

### vault.focus-ring
- applies-when: web-surface; every focusable part
- question: Is each focus ring 3:1 against every ground it can sit on (a two-colour ring, or one ring colour per ground), every ring at least 2 px thick, a text input's drawn outside the field or as a border at least 2 px thick and 3:1 from its rest state rather than only a recoloured thin border, a row in a list shown by a fill plus a cue besides colour, and a ring drawn with `box-shadow` backed by `outline: <width> solid transparent` for forced-colours mode?
- answered-by: builder
- writes: focus ring form
- yields-to: vault.focus, level 2
- source: W3C Understanding SC 2.4.7, 1.4.11 and 2.4.11, and SC 2.4.13 (AAA) for the 2 px ring and the input's 3:1; GOV.UK focus states; Apple HIG Focus and selection; strength: design-system guidance over WCAG 2.2 AA and AAA
- era: timeless
- owner: vault
- stage: treatment
- target: Draw a focus ring that clears 3:1 on every ground (two colours, or one per ground), make every ring at least 2 px, ring text inputs outside or thicken their border, highlight list rows with a fill and a non-colour cue, and back any `box-shadow` ring with a transparent outline.
- reasons: design-critique/references/surface-styling.md#focus-rings-per-ground-clear-of-sticky-bars
- ledger: BTN-11, COL-2, COL-53, COL-58, OTH-21, STA-1, STA-2, STA-3, STA-4, STA-5, STA-7, STA-8, STA-9, SUR-1, SUR-49
- status: live

### vault.scroll-padding
- applies-when: web-surface; a page with a sticky header or bottom bar
- question: Does the scroll container's `scroll-padding` equal each sticky bar's height on its side, so a focused part never lands under the bar?
- answered-by: builder
- writes: scroll padding
- yields-to: vault.focus
- source: W3C Understanding SC 2.4.11 Focus Not Obscured (Minimum) and technique C43 (WCAG 2.2, 2023); strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: treatment
- inputs: the sticky header's height, the sticky bottom bar's height
- output: `scroll-padding-top` = the header's height; `scroll-padding-bottom` = the bottom bar's height
- target: Set `scroll-padding` on the scroll container to the height of each sticky bar.
- reasons: design-critique/references/surface-styling.md#focus-rings-per-ground-clear-of-sticky-bars
- ledger: BTN-11, COL-2, COL-53, COL-58, LAY-107, STA-1, STA-3, STA-5, STA-7, STA-11, SUR-1, SUR-49
- status: live

### vault.whole-target
- applies-when: web-surface; every composite part that does one thing and is a row, list item or article: a task or list row, a nav item, a card with one destination
- question: Is each row, list item and article that does one thing clickable across its whole visible extent, its label, icon, status and any summary line included, rather than on its label or icon alone?
- answered-by: script
- writes: composite hit area
- yields-to: vault.one-target
- source: GOV.UK Design System, Accordion, "the user can interact anywhere in the heading button", and Task list, "The whole row is linked", after users tried to select the status labels (both as read Oct 2026); NN/g, Loranger, "Clickable Elements" (2015): "Make all elements (e.g., picture, icon, text) that are associated with each other clickable"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Make a composite part with one action one target across its whole extent, label, icon, status and summary together; where it holds a second action, split it by vault.one-target.
- script: check-state.py, its whole line
- reasons: design-critique/references/house-principles.md#whole-targets
- ledger: STA-52
- status: staged

### vault.whole-target-look
- applies-when: web-surface; every composite part that does one thing and is no row, list item or article: an accordion heading, a chip
- question: Does each accordion heading and chip that does one thing take a press anywhere it is drawn, its words, icon and count included, and not only where its words sit?
- answered-by: look
- writes: composite hit area
- yields-to: vault.whole-target
- source: GOV.UK Design System, Accordion, "the user can interact anywhere in the heading button", and Task list, "The whole row is linked", after users tried to select the status labels (both as read Oct 2026); NN/g, Loranger, "Clickable Elements" (2015): "Make all elements (e.g., picture, icon, text) that are associated with each other clickable"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Make a composite part with one action one target across its whole extent, label, icon, status and summary together; where it holds a second action, split it by vault.one-target.
- reasons: design-critique/references/house-principles.md#whole-targets
- ledger: STA-52
- status: staged

### vault.hover-reflow
- applies-when: web-surface; every hover, focus or selected state that changes text
- question: Does each hover, focus or selected state leave every glyph's width as it was, changing colour, underline, grade or fill, and weight only in a uniwidth face, so no text reflows or nudges its neighbours?
- answered-by: script
- writes: state text change
- yields-to: vault.emphasis-weight, level 2
- source: MDN, "Variable fonts guide", Grade (page of 27 Feb 2026): grade differs from weight in that "the physical space the text occupies does not change", so it "can be varied or animated without causing a reflow"; rule-interactions I-17 (design-vault#206): bold is wider than light; strength: web platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Show hover and selection on text by colour, underline, fill or the GRAD axis; change weight only in a uniwidth face.
- script: check-state.py, its reflow line
- reasons: design-critique/references/interaction-and-forms.md#states-change-no-widths
- ledger: STA-28
- status: staged

### vault.coarse-target
- applies-when: web-surface; every target under `(pointer: coarse)`, as on a phone, and under `(pointer: fine)`
- question: Where the primary pointer is coarse, does every target measure 44 by 44 px or more (links within running prose excepted), and is no target shrunk for a fine pointer below what the layout gives it?
- answered-by: script
- writes: coarse-pointer target size
- yields-to: level 2, vault.target-size
- source: WCAG 2.2 SC 2.5.5 Target Size (Enhanced, AAA), 44 by 44 px, "A finger is larger than a mouse pointer"; web.dev, Learn Design, "Interaction", Pointer: targets made larger under `pointer: coarse`, and "think twice before reducing the size of interactive elements" (2021); design-vault#119's 44 px for touch; strength: design-system guidance, WCAG 2.2's AAA figure taken as the house's touch default
- era: timeless
- owner: vault
- stage: value
- inputs: the primary pointer (`pointer` media query), the target's rendered box
- output: coarse pointer 44 × 44 px or more; fine pointer no smaller than with its pointer and hover rules off, its floor `vault.target-size`'s; a project rules file may set its own coarse value, never under `vault.target-size`'s 24 px
- script: check-access.py <page> --out <dir> --pointer [--pointer-table <file>]
- reasons: design-critique/references/interaction-and-forms.md#targets-by-pointer
- ledger: STA-49
- status: staged

### vault.drag-buttons
- applies-when: web-surface; every drop zone, and every carousel, map, drag item and pull-to-refresh the round declares
- question: Does every drop zone hold a file input, button or label or sit beside a file input, every declared carousel and map show two buttons or more (previous and next, zoom in and out), every declared drag item a button, and a view with a declared pull-to-refresh a refresh button?
- answered-by: script
- writes: drag alternative controls
- yields-to: none
- source: WCAG 2.2 (2023) SC 2.5.7 Dragging Movements (AA) and its Understanding page, examples for sliders, task boards, sortable lists and maps; GOV.UK Design System, File upload, "Choose file" button or drag and drop (updated Feb 2026); strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: function
- target: Put a "Choose file" button in or beside every drop zone, previous and next buttons on carousels, zoom buttons on maps, a button on every drag item and a refresh button beside a custom pull-to-refresh.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/interaction-and-forms.md#every-drag-has-a-tap-path
- ledger: BTN-120, FRM-120, NAV-87, NEW1-67
- status: staged

### vault.drag-alternative
- applies-when: web-surface; every part the page lets a visitor drag: a slider, a reorderable list, a drop zone, a swipe carousel or row, a map, a resizable sheet, a custom pull-to-refresh; and every multipoint gesture the page reads, such as a pinch zoom
- question: Can everything a drag or a multipoint gesture such as a pinch does also be done by single taps or clicks with no drag or multipoint gesture (a tap on the slider track, move-up and move-down buttons, a "Choose file" button beside the drop zone, previous and next buttons, map pan and zoom buttons, a refresh button, a tap on the sheet's grabber), keyboard support alone not counting?
- answered-by: look
- writes: drag alternative
- yields-to: vault.drag-buttons
- source: WCAG 2.1 (2018) SC 2.5.1 Pointer Gestures (A): functionality that uses multipoint or path-based gestures can be operated with a single pointer without a path-based gesture, unless essential; WCAG 2.2 (2023) SC 2.5.7 Dragging Movements (AA) and its Understanding page: keyboard equivalence "does not automatically meet this success criterion", examples for sliders, task boards, sortable lists and maps; browser-native scrolling exempt; GOV.UK Design System, File upload, "Choose file" button or drag and drop (updated Feb 2026); Apple HIG Accessibility, "Offer alternatives to gestures" (9 Jun 2025), and Drag and drop, "Offer alternative ways to accomplish drag-and-drop actions" (24 Oct 2023); strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: function
- target: Give every drag a tap or click path that does the same: track taps on sliders, move buttons on sortable lists, a "Choose file" button with a drop zone, previous and next on swipe galleries, pan and zoom buttons on maps and wherever a pinch zooms, a refresh button beside a custom pull-to-refresh.
- reasons: design-critique/references/interaction-and-forms.md#every-drag-has-a-tap-path
- ledger: BTN-120, FRM-120, NAV-87, NEW1-67
- status: staged

### vault.slider-keys
- applies-when: web-surface; every slider, native or custom
- question: Does each slider take Right and Up Arrow to raise its value by one step, Left and Down Arrow to lower it, Home and End for its ends, and a tap or click on its track to set a value?
- answered-by: script
- writes: slider input
- yields-to: none
- source: WAI-ARIA Authoring Practices, Slider pattern, keyboard interaction (as read Oct 2026); WCAG 2.2 (2023) SC 2.1.1 Keyboard and 2.5.7 Dragging Movements, whose Understanding page has a slider that "allows tapping or clicking on any point of the slider track"; strength: W3C authoring practice over WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Build sliders on `<input type="range">`, or give a custom one the APG slider keys and a clickable track.
- script: check-state.py, its slider-keys line
- reasons: design-critique/references/interaction-and-forms.md#every-drag-has-a-tap-path
- ledger: NEW1-41
- status: staged

### vault.drag-tracking
- applies-when: web-surface; every custom slider thumb
- question: Does each custom slider thumb capture its pointer on `pointerdown` (`setPointerCapture`), so it keeps following the pointer past the control's edge until release and hovers nothing else meanwhile, and does the drag select no text (`user-select: none` with Safari's `-webkit-user-select: none`, on the body for the drag's length or on the drag surface, or `preventDefault` on its `pointerdown`)?
- answered-by: script
- writes: drag tracking
- yields-to: level 2
- source: MDN `setPointerCapture()` (Baseline widely available since Jul 2020; page of 1 Oct 2025): its slider example slides "even when your pointer moves outside of its boundaries"; Rauno Freiberg, "Invisible Details of Interaction Design" (Jul 2023): "ensure that the dragging gesture does not cancel when moving away from the slider"; measured on design-vault#277 (docs/research/interaction-defaults.md): in Chromium 149, without capture a drag got 1 move once past its edge and the element under the pointer took `:hover`; with capture it got all 16 and nothing else took `:hover`, but the drag still selected text (the slider's own label) unless the surface had `user-select: none` or its `pointerdown` called `preventDefault`; strength: web platform documentation and a measurement
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: On `pointerdown`, call `setPointerCapture` on the dragged part and stop text selection (`user-select: none` and `-webkit-user-select: none` on the body until `pointerup`, or `preventDefault`); release on `pointerup`. A native range input needs neither.
- script: check-state.py, its drag line
- parts: slider
- reasons: design-critique/references/interaction-and-forms.md#a-drag-holds-its-pointer
- ledger: NEW3-84, VG-NEW-5
- status: live

### vault.drag-tracking-surface
- applies-when: web-surface; every custom drag but a slider thumb: a sheet, a swipe row, a reorderable item
- question: Does each dragged sheet, swipe row or reorderable item hold the pointer from the first press until it is let go (`setPointerCapture` from `pointerdown`), tracking it beyond its own bounds while nothing under it reacts to hover, and stay free of text selection while it moves (a `preventDefault` on `pointerdown`, or `user-select` and `-webkit-user-select` set to `none` on the moving part or the body)?
- answered-by: builder
- writes: drag tracking
- yields-to: vault.drag-tracking
- source: MDN `setPointerCapture()` (Baseline widely available since Jul 2020; page of 1 Oct 2025): its slider example slides "even when your pointer moves outside of its boundaries"; Rauno Freiberg, "Invisible Details of Interaction Design" (Jul 2023): "ensure that the dragging gesture does not cancel when moving away from the slider"; measured on design-vault#277 (docs/research/interaction-defaults.md): in Chromium 149, without capture a drag got 1 move once past its edge and the element under the pointer took `:hover`; with capture it got all 16 and nothing else took `:hover`, but the drag still selected text (the slider's own label) unless the surface had `user-select: none` or its `pointerdown` called `preventDefault`; strength: web platform documentation and a measurement
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: On `pointerdown`, call `setPointerCapture` on the dragged part and stop text selection (`user-select: none` and `-webkit-user-select: none` on the body until `pointerup`, or `preventDefault`); release on `pointerup`.
- parts: bottom-sheet, card
- reasons: design-critique/references/interaction-and-forms.md#a-drag-holds-its-pointer
- ledger: NEW3-84, VG-NEW-5
- status: live

### vault.drag-release
- applies-when: web-surface and has-motion; every dragged or swiped part the visitor lets go of: a sheet, a carousel, a thrown card or panel, a swipe row
- question: When a drag ends, does the part settle on the snap point nearest the position its release velocity projects to (not merely the nearest to where it was let go), a swipe row instead taking no momentum and settling by where it was let go, each setting off the way it was thrown and moving there with no bounce?
- answered-by: script
- writes: release settling
- yields-to: vault.reduced-motion, level 2
- source: Apple WWDC 2018, "Designing Fluid Interfaces": "remember to project momentum", the release velocity and the scroll deceleration rate giving the "projected position" used to pick the end point; Apple WWDC 2023, "Animate with springs": a spring "can start with any initial velocity", and "when you're not sure, use a spring with bounce 0"; Jakub Krehel, "Drag gesture" (as read Oct 2026): for swipe rows, no momentum fling, the row snapping back short of its threshold; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: On release, project the part's position from its velocity, pick the nearest snap point to that, and spring there from the release velocity with no bounce; settle a swipe row by its release position, with no fling.
- parts: bottom-sheet, card
- script: check-flow.py <page> --out <dir> --records [--parts <declaration>]
- reasons: design-critique/references/interaction-and-forms.md#a-released-drag-follows-its-throw
- ledger: NEW3-44
- status: live

### vault.drag-release-spring-code
- applies-when: web-surface and has-motion; every dragged or swiped part the visitor lets go of: a sheet, a carousel, a thrown card or panel, a swipe row
- question: Is each released part's settle defined to start at its release velocity: a spring handed the pointer's velocity as its initial velocity, or a Web Animations or CSS settle whose first keyframe segment's slope matches it, rather than an ease or a spring that starts from rest?
- answered-by: code
- writes: release spring
- yields-to: vault.drag-release, vault.reduced-motion, level 2
- source: Apple WWDC 2023, "Animate with springs": a spring "can start with any initial velocity"; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Spring a released part to its settle point from the release velocity.
- parts: bottom-sheet, card
- reasons: design-critique/references/interaction-and-forms.md#a-released-drag-follows-its-throw
- ledger: NEW3-44
- status: live

### vault.focus-visible
- applies-when: web-surface; every focus style the page sets
- question: Is every focus style set on `:focus-visible` rather than `:focus`, so a mouse or finger press on a button draws no ring while keyboard focus and a focused text field always do, and is no browser ring removed without one put in its place?
- answered-by: script
- writes: focus trigger
- yields-to: vault.focus, level 2
- source: MDN `:focus-visible` (Baseline widely available since Mar 2022; page of 16 Oct 2026): it matches "only if the user needs to be informed where the focus currently is", and "removing focus styles makes keyboard navigation inaccessible for sighted users"; strength: web platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Style focus rings on `:focus-visible`, never `:focus`, and never set `outline: none` without a replacement ring.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/interaction-and-forms.md#focus-shows-for-the-keyboard
- ledger: STA-10
- status: staged

### vault.scroller-focus
- applies-when: web-surface; every scrolling box (`overflow: auto` or `scroll`) that scrolls at the width checked
- question: Can the Tab key reach each scrolling box whose content has no focusable part, by `tabindex="0"` with `role="region"` and a name, so the arrow keys scroll it, and does it show focus as `vault.focus` asks?
- answered-by: script
- writes: scroller focusability
- yields-to: none
- source: WCAG 2.2 (2023) SC 2.1.1 Keyboard; web.dev, Learn CSS, "Overflow", "Scrolling and accessibility": `tabindex="0"`, a name with `aria-labelledby` and a `role` (updated Aug 2025); Chrome for Developers, "Keyboard focusable scrollers" (2024): Chrome 132 makes such a scroller focusable by default, other browsers not said; axe-core rule `scrollable-region-focusable`; strength: WCAG 2.2 A
- era: dated 2027-10-19
- owner: vault
- stage: function
- target: Give a scrolling box with no focusable content `tabindex="0"`, `role="region"` and an `aria-labelledby` name.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/interaction-and-forms.md#keyboard-paths-the-aria-patterns-fix
- ledger: STA-15
- status: staged

### vault.roving-focus
- applies-when: web-surface; every composite widget: a tab list, radio group, chip set, toolbar, listbox, grid or segmented control
- question: Is each composite widget one Tab stop, the arrow keys moving among its items (by roving `tabindex` or `aria-activedescendant`), and does focus enter on its selected item, or its first where none is selected?
- answered-by: script
- writes: composite keyboard traversal
- yields-to: level 2
- source: WAI-ARIA Authoring Practices, "Developing a Keyboard Interface": "the tab sequence should include only one focusable element of a composite UI component", by roving `tabindex` or `aria-activedescendant`; APG Listbox pattern, focus on the selected option, else the first; APG Tabs and Radio Group patterns (all as read Oct 2026); strength: W3C authoring practice
- era: timeless
- owner: vault
- stage: function
- target: Make each tab list, radio group, chip set, toolbar, listbox or grid one Tab stop with arrow keys inside, entering on the selected item or else the first; native radio groups do this already.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/interaction-and-forms.md#keyboard-paths-the-aria-patterns-fix
- ledger: NAV-19, STA-65
- status: staged

### vault.menu-focus
- applies-when: web-surface; every menu a button opens (`role="menu"`), an action menu or a dropdown of commands
- question: When the menu opens, does focus move to its first item (to its last on Up Arrow), do Up and Down Arrow move between items, Escape close it and return focus to the button that opened it, and Tab leave and close it?
- answered-by: script
- writes: menu focus
- yields-to: level 2
- source: WAI-ARIA Authoring Practices, Menu Button pattern, Enter and Space open the menu "and place focus on the first menu item", and Menu and Menubar pattern, arrows, Escape returning focus "to the element or context" that opened it, Tab closing all menus (as read Oct 2026); strength: W3C authoring practice
- era: timeless
- owner: vault
- stage: function
- target: On opening a menu, focus its first item; move with the arrow keys; close on Escape and Tab, returning focus to the menu button on Escape.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/interaction-and-forms.md#keyboard-paths-the-aria-patterns-fix
- ledger: STA-56
- status: staged

### vault.carousel-focus
- applies-when: web-surface; every carousel or slideshow the round declares
- question: Does the carousel stop rotating while focus or the pointer is inside it, put its rotation control first in its Tab order, leave focus where it was when previous or next is pressed, and keep slides out of view out of the Tab order and the accessibility tree (`inert`, or `interactivity: inert`), so Tab never lands on an unseen slide?
- answered-by: script
- writes: carousel focus
- yields-to: level 2
- source: WAI-ARIA Authoring Practices, Carousel pattern (as read Oct 2026): rotation stops "when any element in the carousel receives keyboard focus" and on hover, the rotation control first, next and previous "do not move focus", off-screen slides confusing when "incorrectly hidden"; MDN `inert` (Baseline widely available since Apr 2023; page of 17 Apr 2026): removed "from the tab order and accessibility tree"; Chrome for Developers, "New in web UI, I/O 2025 recap" (14 Aug 2025): `interactivity: inert` makes "off-screen carousel items unfocusable"; strength: W3C authoring practice
- era: dated 2027-10-19
- owner: vault
- stage: function
- target: Pause rotation on focus and hover, put the rotation control first, keep focus on previous and next when pressed, and make slides out of view `inert`.
- script: check-access.py <page> --out <dir> --parts <declaration>
- reasons: design-critique/references/interaction-and-forms.md#keyboard-paths-the-aria-patterns-fix
- ledger: STA-66
- status: staged

### vault.on-focus
- applies-when: web-surface; every part the Tab key reaches
- question: Does taking focus leave the visitor where they are: no part, on focus, opening a page or window, submitting a form, or moving focus elsewhere?
- answered-by: script
- writes: behaviour on focus
- yields-to: none
- source: WCAG 2.2 (2023) SC 3.2.1 On Focus (A); failure F55, script that removes focus when it is received; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Act only on activation, never on focus: no navigation, new window, submission or focus jump when a part is focused.
- script: check-state.py, its on-focus line
- reasons: design-critique/references/interaction-and-forms.md#keyboard-paths-the-aria-patterns-fix
- ledger: STA-68
- status: staged

### vault.key-shortcuts
- applies-when: web-surface; every keyboard shortcut the page adds
- question: Can each shortcut made of a single letter, number, symbol or punctuation key be turned off or remapped to include Ctrl, Alt or another non-printing key, or does it work only while its own component has focus?
- answered-by: script
- writes: keyboard shortcut form
- yields-to: none
- source: WCAG 2.2 (2023) SC 2.1.4 Character Key Shortcuts (A): "reduce accidental activation of keyboard shortcuts", above all for speech-input users; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Give custom shortcuts a modifier key, or a setting to turn them off or remap them, or limit a single-key one to its focused component.
- script: check-state.py, its single-key line
- reasons: design-critique/references/interaction-and-forms.md#keyboard-paths-the-aria-patterns-fix
- ledger: OTH-28
- status: live

### vault.motion-control
- applies-when: web-surface; every page that listens for device motion or orientation
- question: Does the page show the control the round declares as doing what the motion does?
- answered-by: script
- writes: motion control presence
- yields-to: none
- source: WCAG 2.2 (2023) SC 2.5.4 Motion Actuation (A), save motion through an accessibility supported interface or where it is essential; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Pair every shake or tilt feature with a button that does the same.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/interaction-and-forms.md#every-drag-has-a-tap-path
- ledger: NEW2-22
- status: staged

### vault.motion-input
- applies-when: web-surface; every feature worked by shaking, tilting or moving the device or the body
- question: Can each thing device or body motion does also be done with an on-screen control, and can the visitor turn the response to motion off?
- answered-by: look
- writes: motion input alternative
- yields-to: vault.motion-control
- source: WCAG 2.2 (2023) SC 2.5.4 Motion Actuation (A), save motion through an accessibility supported interface or where it is essential; Apple HIG Gestures, "Avoid requiring specific body movements or positions for input" (9 Sep 2024); strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Pair every shake or tilt feature with a button that does the same, and a setting that turns the motion response off.
- reasons: design-critique/references/interaction-and-forms.md#every-drag-has-a-tap-path
- ledger: NEW2-22
- status: staged

### vault.touch-action
- applies-when: web-surface; every `touch-action` the page sets, and every control a visitor may tap twice quickly
- question: Is `touch-action: none`, `pan-x` or `pan-y` set only on a part that handles its own drag or pinch (a map, a canvas, a slider thumb) and offers buttons for what the gesture does, never on the page root, the body or a region the visitor must pinch to read, and do buttons and other controls take `touch-action: manipulation`, keeping pinch zoom while dropping double-tap zoom?
- answered-by: script
- writes: touch-action
- yields-to: vault.reflow
- source: MDN `touch-action` (Baseline widely available since Sep 2019; page of 20 Apr 2026): `none` "may inhibit operating a browser's zooming capabilities", and `manipulation` enables panning and pinch zoom but disables double-tap zoom, which "removes the need for browsers to delay the generation of click events"; WCAG 2.2 (2023) SC 1.4.4 Resize Text, as W3C ACT rule b4f0c3 reads it for the viewport meta, which `vault.reflow` checks; strength: web platform documentation over WCAG 2.2 AA
- era: dated 2027-10-19
- owner: vault
- stage: value
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/interaction-and-forms.md#pinch-zoom-stays-on
- ledger: NEW2-65, VG-NEW-2
- status: staged

### vault.hover-reveal
- applies-when: web-surface; every part hover reveals or changes: a control shown on hover, a tooltip, an edit cue, a card's hidden action, a hover preview
- question: Does everything hover reveals also appear on keyboard focus and on a tap or long-press, and show by default where no input can hover?
- answered-by: script
- writes: reveal trigger
- yields-to: level 2
- source: web.dev Learn Design, "Interaction" (2021): "Don't use hover to hide important information or an important interface element", and with no input that can hover "the extra icon is always visible"; MDN, Media queries, "Use of pointing devices" (modified Sep 2026, as read Oct 2026): "touchscreen and keyboard navigation does not hover"; WAI-ARIA APG Tooltip pattern (as read Oct 2026): shown on "keyboard focus or the mouse hovers", Escape dismisses; Android Developers, Compose Tooltip (updated Oct 2026): hover with a cursor or long-press on touch; strength: platform guidance
- era: timeless
- owner: vault
- stage: function
- target: Show whatever hover reveals on focus too (`:focus-visible`, `:focus-within`) and on tap or long-press; under `@media (any-hover: none)` show it by default.
- script: check-state.py, its reveal line
- reasons: design-critique/references/page-behaviour.md#nothing-on-hover-alone
- ledger: FRM-92, NAV-240, STA-17
- status: live

### vault.editable-cue
- applies-when: web-surface; every value the visitor edits in place, declared as the editable-value part
- question: Does each editable value change its look, or draw an edit cue, on hover and on keyboard focus alike?
- answered-by: script
- writes: edit cue
- yields-to: vault.affordance
- source: Atlassian Design System, Inline edit, Accessibility (as read Oct 2026): the read view shows it can be edited on hover and on focus; WCAG 2.2 Understanding 2.4.7 Focus Visible; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Show an editable value's edit cue on `:hover` and `:focus-visible` alike.
- script: check-state.py, its editable line
- parts: editable-value
- reasons: design-critique/references/page-behaviour.md#nothing-on-hover-alone
- ledger: FRM-92
- status: staged

### vault.hover-content
- applies-when: web-surface; every tooltip, popover or other content that appears on hover or focus
- question: Can content that appears on hover or focus be dismissed with Escape without moving the pointer or focus, can the pointer move onto it without it vanishing, and does it stay until the visitor moves away, dismisses it or it stops being true?
- answered-by: script
- writes: hover content persistence
- yields-to: none
- source: WCAG 2.2 success criterion 1.4.13 Content on Hover or Focus and its Understanding page (updated Jul 2026, as read Oct 2026): dismissible, hoverable, persistent; WAI-ARIA APG Tooltip pattern, Escape dismisses; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: function
- target: Let Escape close any tooltip or hover content, keep it open while the pointer moves onto it, and leave it up until the visitor moves away or dismisses it.
- script: check-state.py, its persist line
- reasons: design-critique/references/page-behaviour.md#nothing-on-hover-alone
- ledger: NAV-236, NAV-240
- status: live

### vault.expanded-state
- applies-when: web-surface; every button that shows and hides a menu, a disclosure, an accordion panel or a nav panel
- question: Does each button that shows and hides a menu or panel carry `aria-expanded`, `true` while it is open and `false` while it is closed, and does a menu trigger also carry `aria-haspopup` (`menu` or `true`)?
- answered-by: script
- writes: expanded state
- yields-to: none
- source: WAI-ARIA Authoring Practices, Menu Button pattern: "When the menu is displayed, the element with role button has aria-expanded set to true. When the menu is hidden, aria-expanded is set to false", and aria-haspopup "menu or true"; Disclosure pattern, the same for a show and hide button (both as read Oct 2026); W3C Understanding SC 4.1.2, states programmatically determined; strength: WCAG 2.2 A, by the WAI-ARIA pattern
- era: timeless
- owner: vault
- stage: function
- target: Give every button that opens a menu or panel `aria-expanded`, `true` when open and `false` when closed, and a menu trigger `aria-haspopup="menu"` as well.
- script: check-state.py, its expanded line
- reasons: design-critique/references/controls-and-feedback.md#controls-say-whether-they-are-open
- ledger: BTN-59
- status: staged

### vault.act-on-release
- applies-when: web-surface; every control a single pointer operates
- question: Does each control act when the pointer is released (a `click`), not when it is pressed, save where the release undoes the press, the action can be aborted before release or undone after it, or acting on the press is essential, as a key of an on-screen keyboard is?
- answered-by: script
- writes: activation event
- yields-to: none
- source: W3C, WCAG 2.2 SC 2.5.2 Pointer Cancellation (2024 edition), its four conditions; Understanding SC 2.5.2 (updated 2025): "The most accessible way to incorporate pointer cancellation is to make activation occur on the up-event", and "the click event ... is an example of an implicit up-event"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Wire every action to `click`, never to `pointerdown`, `mousedown` or `touchstart`, except a press-and-hold the release reverses, an action that can be aborted before release or undone after it, or an on-screen key.
- script: check-state.py, its release line
- reasons: design-critique/references/controls-and-feedback.md#act-on-release
- ledger: BTN-73
- status: staged

### vault.ring-outline
- applies-when: web-surface; every focus ring the page draws itself
- question: Is each focus ring drawn with `outline` and `outline-offset`, which follow the corner radius and take no layout space, and is a transparent outline kept behind any ring a shadow draws?
- answered-by: script
- writes: focus ring drawing
- yields-to: vault.focus-ring, vault.focus
- source: MDN `outline`, outlines follow `border-radius` and take no space (14 Sep 2026), Baseline since 2023-03-27 and widely available since 2025-09-27 (web-features `outline`); MDN `forced-colors`, `box-shadow` forced to none (20 Apr 2026); material-web's focus ring, an outline at the component's radius plus its offset (8 Oct 2025); govuk-frontend `_focused.scss`, its transparent outline behind a shadow ring (26 Mar 2026); web.dev Learn CSS Focus, "Avoid replacing outline styles with box-shadow" (2021); strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Draw focus rings with `outline` and `outline-offset`; back any `box-shadow` ring with a transparent outline.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/edges-and-contrast.md#edges-in-forced-colours
- ledger: STA-3
- status: live

### vault.focus-colour
- applies-when: web-surface; every focus indicator, and every other use of the focus colour
- question: Is the site's focus colour kept off hover and brand accents, either the browser's own two-colour ring or a project colour paired with a second colour so the ring clears 3:1 on every ground it meets?
- answered-by: look
- writes: focus colour
- yields-to: vault.focus-colour-kept, vault.focus-ring, level 2
- source: GOV.UK Design System Colour, `focus` #ffdd00, "Only use this colour to indicate which element is focused on", paired with black for light grounds; @atlaskit/tokens 20.6.1 `color.border.focused`, "Do not use to indicate selection or hover alone", kept apart from `color.border.selected` (both as read Oct 2026); Chromium's default ring since Chrome 83, "a thick dark ring with a thin white outline", for "both light and dark backgrounds" (2020); W3C technique C40, the two-colour indicator (WCAG 2.2, 2023); strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Choose one focus colour, use it for nothing else, and pair it with a second colour, or keep the browser's two-colour ring, so focus shows on every ground.
- reasons: design-critique/references/edges-and-contrast.md#one-focus-colour
- ledger: STA-7
- status: staged

### vault.focus-colour-kept
- applies-when: web-surface; every focus ring the page draws in a colour of its own
- question: Is every focus ring drawn in one colour, black, white and greys aside, and is that colour never also a link's text colour or the fill or edge of a button or of a selected, current, pressed or checked item?
- answered-by: script
- writes: focus colour reuse
- yields-to: none
- source: GOV.UK Design System Colour, `focus` #ffdd00, "Only use this colour to indicate which element is focused on", paired with black for light grounds; @atlaskit/tokens 20.6.1 `color.border.focused`, "Do not use to indicate selection or hover alone", kept apart from `color.border.selected` (both as read Oct 2026); Chromium's default ring since Chrome 83, "a thick dark ring with a thin white outline", for "both light and dark backgrounds" (2020); W3C technique C40, the two-colour indicator (WCAG 2.2, 2023); strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Draw no link, button or selected item in the focus ring's colour.
- script: check-access.py <page> --out <dir>
- reasons: design-critique/references/edges-and-contrast.md#one-focus-colour
- ledger: STA-7
- status: staged
