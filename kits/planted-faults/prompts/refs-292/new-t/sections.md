# The reference sections the records cite

<!-- design-round/references/impeccable.md#conditions-added -->

### Conditions added

- **Body measure** (`craft-floor` 65–75ch, `operate` the same; `typeset` 45–75): `vault.measure`, counted in characters rather than `ch`, on Baymard's range and WCAG 2.2 SC 1.4.8's ceiling.
- **Line height under 1.3** (detector): `vault.leading`, a finding on body text only.
- **`flat-type-hierarchy`** (detector: heading and body under 1.25× in size): `vault.heading-step`, no finding where weight, space or tone carries the step, as `typeset` itself says.
- **Display at most 6rem, tracking no tighter than -0.04em** (`craft-floor`): one author's numbers with no source found; the project's type scale replaces them.
- **Light or dark picked from the use scene** (`craft-floor`): `vault.theme`. The visitor's system setting already says which they want, and most people read long text more easily light (NN/g 2020); shipping both themes doubles the colour work, which is why a one-theme project ships light unless its rules file rules dark.
- **Touch targets of 44×44 px** (`adapt`, `audit`): `vault.target-size`, at WCAG 2.2 SC 2.5.8's 24×24 floor. 44 px (Apple 44 pt, Material 48 dp) is a target a project's rules file may set as its own question; the vault holds only the floor.
- **A hamburger or drawer on mobile** (`adapt`): `vault.visible-nav`. Navigation out of sight is used less and found more slowly (NN/g 2016); keeping four links in view costs header room on a phone, which is why the menu takes over past four.

<!-- design-critique/references/text-presentation.md#ranking-text -->

### Ranking text

Record: `vault.emphasis-cues`.

- **Why.** Weight and a second text colour rank text without breaking the type scale; size steps add up quickly, so they stay small. Text made both lighter and smaller than body text loses legibility twice. Three levels of contrast are enough for a complex view (NN/g).
- **Trade-off.** Ranking by weight adds visual noise if many things are bold.
- **Clash.** `vault.heading-step` sets the step between a heading and its body, and `vault.text-steps` holds text colour to two readable steps, so the third level of contrast comes from weight or size.

<!-- design-critique/references/typeface-traits.md#one-job-per-face -->

### One job per face

Record: `vault.face-roles`.

- **Why.** A second face works when each face keeps one job, body or headings; a third rarely works, and four almost never (Butterick). Too many faces blur the hierarchy and make an interface look inconsistent (Apple). Code needs a monospace face, because its dense punctuation reads better there. Design systems split the faces the same way: USWDS by role tokens, Atlassian with a brand face for marketing and a plain one for the app.
- **Trade-off.** One family is lighter to load and always consistent; a second face adds voice and file weight.
- **Clash.** `vault.brand-layer` says where expressive display type belongs; this record says how many faces there are and which job each holds.

<!-- design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces -->

### Sources for the rules the house enforces

The rest of design-vault#119's sample stands, each rule a record citing the outside source that owns it. design-vault#119 cited three of them from memory or second-hand, not re-read: the 4 px step, web.dev's rendering and font guidance, and the W3C images tutorial.


- **Type.** `vault.body-size`: under 16 px, screen reading slows and a phone zooms into a form field; a dense working role fits less at 16 px, so it may go smaller (Carbon's productive set). `vault.paragraph-break`: a gap and an indent each mark a paragraph, so both together say it twice; a gap costs height, an indent keeps dense text compact. `vault.no-justify`: justified web text opens uneven word gaps that slow readers, dyslexic readers most; a ragged edge looks less formal, and as SC 1.4.8 is AAA, a project's rules file may rule otherwise.
- **Colour.** `vault.contrast`: below 4.5:1, or 3:1 for large text, many low-vision readers cannot read the text; pale brand colours lose a text role, and no brand rule lowers the floor. `vault.chroma-ends`: near white and black a screen holds little chroma, so a saturated tint or shade clips or shifts hue; the palette's ends read quieter than its middle.
- **Layout.** `vault.spacing-step`: one 4 px step makes every gap a multiple the eye reads as ordered; an optical nudge off the step needs a reason.
- **Motion.** `vault.motion-duration`: under about 100 ms a change reads as a jump, over 500 ms as a wait, and an exit can be quicker because the visitor has moved on; an authored focal entrance may run longer at the cost of that wait. `vault.motion-easing`: a decelerating curve reads as a thing arriving and settling; an exit or a loop may take another curve. `vault.reduced-motion`: movement can make a visitor with a vestibular disorder ill, and a designed reduced version keeps the meaning that switching motion off loses; it is more work, and as SC 2.3.3 is AAA, a project's rules file may relax it. `vault.motion-properties`: animating width, height, position or margin lays the page out again every frame and stutters, where transform and opacity do not; an effect that needs a layout change must be approximated.
- **Content.** `vault.undo`: a confirmation dialog trains a click-through and still loses the work, where undo lets the visitor recover; it needs the action held back or reversible. `vault.decorative-alt`: a screen reader reads every non-empty alt, so alt on decoration is noise; telling decoration from an image that informs is a judgement, and the second needs its alt.
- **Performance.** `vault.load` and `vault.web-vitals`: past web.dev's thresholds most visitors find a page slow or jumpy; heavy hero media and web fonts are what cost them. `vault.font-display`: without `swap` or `optional`, text stays invisible while the font loads; `swap` shows a fallback that then shifts, and `optional` may never show the web font on a slow first visit.
- Heuristics: Nielsen's ten heuristics (NN/g) stand as impeccable `critique` scores them; they are a frame for judging, not one rule.

<!-- design-critique/references/platform-defaults.md#dashes -->

### Dashes

Record: `vault.dashes`.

- **Why.** Hyphen, en dash and em dash each have their own job, and a hyphen standing in for a dash reads as a joined word (Butterick).
- **Trade-off.** Whether a mark joins a range or breaks a sentence is a reading of meaning, so the type critic answers it, not a script; spaced or flush em dashes are a house choice, kept consistent.
- **Clash.** The minus sign is `vault.math-signs`', not a dash.

<!-- design-critique/references/text-presentation.md#emphasis-in-running-text -->

### Emphasis in running text

Record: `vault.prose-emphasis`.

- **Why.** Bold and italic stand out because they are rare; used often, nothing stands out. A sans serif's italic barely slants, so bold does the job there. Underline belongs to links.
- **Trade-off.** In an interface already full of semibold labels, bold in prose loses some force.
- **Clash.** `vault.link-style` owns the underline.

<!-- design-critique/references/text-presentation.md#capitals-on-labels-and-the-house-dna -->

### Capitals on labels and the House DNA

Record: `vault.dna-caps-label`.

- **Why.** Anthropic's `frontend-design` names "using all caps for labels" among the commonest tells of a generated page (3 Sep 2026): capitals reached for by habit, not for the content.
- **Trade-off.** Typographers set short strings in capitals, headers, captions and labels among them, with 5–12% added tracking (Butterick). The reading cost is weaker than assumed: Arditi and Cho (2007) found capitals read faster than mixed case near the acuity limit, and no slower at larger sizes.
- **Clash.** House DNA `never` line 7 against the case research (`docs/research/text-presentation.md` B2.3): a label in capitals that nothing asked for is weighed as the DNA's tell alone, at P2 at most, and one the brief or the rules file asks for passes. Neither is a legibility fault while it stays under one line. Capitals running longer are impeccable's "all-caps body text" finding. `vault.ai-look` decides whether a decorative eyebrow belongs at all, never its case.

<!-- design-round/references/impeccable.md#struck-or-corrected -->

### Struck or corrected

- **Weight on light text on dark** (`typeset`: "one step more weight"): `vault.dark-text-weight`. Its extra line height and tracking stand; the weight step goes, since Material's 2022 grade study found no readability need for it. Large text going lighter is a look choice no source splits by size.
- **The eyebrow above a heading** (`craft-floor`: "a ban, not a default"): `vault.ai-look`. GOV.UK sets a caption above a heading to say where the page belongs, so only a decorative eyebrow is an "AI look" default.
- **Stopping a loop offscreen** (`animate`): `vault.pause`. Not enough on its own, since WCAG 2.2 SC 2.2.2 asks for a control on motion that starts by itself and runs over 5 s.
- **Device-width breakpoints** (`adapt`: "Mobile: 320px-767px…", "640, 768, 1024px"): struck, for `vault.breakpoints`, as `adapt`'s own next line says.
- **Ripples as touch feedback** (`adapt`: "ripples, highlights"): `vault.press-state`. The touch feedback stands; the ripple is struck as its form, since it is one design system's pressed-state value and a value comes from the project's value system ([dependency order](../../design-critique/references/house-principles.md#dependency-order), step 4).
- **At most 4 visible options** (`critique`: "≤4 visible options", "8+ items: Overloaded"): struck as a count, for `vault.option-sets`. Short-term memory limits what a visitor holds, not what a grouped list can show.

<!-- design-critique/references/typeface-traits.md#telling-characters-apart -->

### Telling characters apart

Record: `vault.glyph-distinct`.

- **Why.** Readers with dyslexia and others confuse I, l and 1, and O and 0; in a reference number or code there are no words around them to help.
- **Trade-off.** A slashed zero looks technical in running prose, so it is kept to codes and data.
- **Clash.** None known.

<!-- design-critique/references/typeface-traits.md#figures -->

### Figures

Records: `vault.figure-face`, `vault.figures`.

- **Why.** Numbers line up in a column only when every digit is the same width; in a sentence, proportional digits space more evenly; lining digits sit at capital height, so they match capitals. A face without tabular digits cannot be fixed by CSS.
- **Trade-off.** USWDS sets table amounts in a monospace face; the text face's tabular digits keep one typeface and do the same alignment, so the monospace face is the fallback.
- **Clash.** `vault.face-roles` keeps a monospace face for code; it sets compared numbers only where the text face has no tabular figures.
