# impeccable at each stage

`impeccable` (the plugin) is the house's frontend design tool, pinned at **4.5.0**.

## The pin

- **Check the version before the first impeccable command.** The `impeccable` skill's base directory names the version that runs: `…/impeccable/<version>/skills/impeccable`. On any version but the pin, run no impeccable command and render nothing on the web surface; tell the founder which version runs, and that it needs the pinned one installed or the vault's pin bumped.
- **A bump follows a diff review of the rules** (design-vault#119). Diff every `reference/*.md` between the pin and the new version, and the detector's rule text where its engine version in `scripts/VERSION` (0.1.11 at the pin) has moved. Check each changed rule against its outside source the way design-vault#119 F2 did, and check that each override below still matches the rule it overrides. Record the review on the ticket that bumps the pin, and change the pin, the overrides and the stage table below in the same commit.

## Precedence

- **The house overrides below win over impeccable's text and its detector.** A project's rules file may override any of them, except one that rests on WCAG or the law, and, on behaviour, one that rests on domain evidence, which it overrides only on evidence of its own.
- **The round governs.** Where impeccable asks the user to pick, such as its direction board, the round's candidates and the founder's reply are that pick.
- **The project's rules file wins** over PRODUCT.md and DESIGN.md, which impeccable reads on every run. Both are consumers of the rules file: bring them into line when it changes.
- **Web layouts build code-first.** The project's `.impeccable/config.json` carries `"buildPath": "code"`.
- **A project's own ruling on a command wins**, wherever the project records it. Manta's DESIGN.md carries its rulings on `document` and `extract`.

## By stage

| Stage | Command | When and how |
|---|---|---|
| Setup, first web round | `init` | No PRODUCT.md yet: write it from the rules file (who it is for, the one action, the voice), with one line naming the rules file as the authority. |
| Setup, first web round | `document` | The repo already holds a built site and no DESIGN.md: record the site's current look. Otherwise leave DESIGN.md to the documenter below. |
| Setup, first web round | `hooks on` | Turns on the detector that checks every UI edit. |
| Every session | `impeccable context` | The skill's own setup, run once. Report a `CONTEXT_STALE` line to the founder and leave it; he may ask for `doctor`. |
| Brief | `shape` | Its discovery interview settles a web surface's Intent: two or three questions, then a confirmed brief. Stop it before it picks a look. |
| Round one | `concept-seed` | Run once, `--scope direction` where the look is open (a redesign, a new project) or `--scope surface` where the look is settled and only the page is new. Its assigned direction and challengers fill only the directions that neither a judged reference nor the precedent note (design-round §1b) seeds, each fused into a direction card. Skip its decision page. |
| Round one | new-work | Builds each candidate from its card: new-work §6, code-first, then its §7 inspection and finish reviewer. The card's fields are its direction contract. |
| Later rounds | the axis command | Each variant runs the command for its axis (below), scoped to the section the delta names. |
| Critic | `critique`, `audit` | design-critique §1: the building session dispatches `critique`'s Assessment A and Assessment B as two isolated subagents (gate-check §3), and the whole-page critic merges their reports and runs `audit`. |
| Final | `polish` | Always, on the winner, before the tweak step. |
| Final | `adapt` | Always, for the intermediate width and the phone. |
| Final | `harden` | The surface has a form, live data or user input. |
| Final | `optimize` | `audit` scored performance below 3 of 4. |
| Tweak | `live` | Rung two of the tweak step. Needs the dev server. |
| Winner landed | `extract` | Repeated parts into the project's components and tokens. |
| Winner landed | `impeccable-documenter` | A new or replaced look: writes DESIGN.md from the shipped page. |
| On request | `doctor` | Repairs impeccable's own files when they have fallen behind the installed version. |

### The axis command

| The delta asks for | Command |
|---|---|
| More presence or conviction in one part | `bolder` |
| Calmer, less loud | `quieter` |
| Less clutter, fewer elements | `distill` |
| Type: hierarchy, faces, scale | `typeset` |
| Colour | `colorize` |
| Spacing, grouping, reading order | `layout` |
| Personality, a memorable detail | `delight` |
| Clearer words, labels, messages | `clarify` |
| Motion | `animate` |
| A phone or another device | `adapt` |
| First-run or empty states | `onboard` |
| Long text, errors, other languages | `harden` |
| An effect past the usual | `overdrive`: put its two or three proposals to the founder in this session before any code, then build the one he picks |

A delta naming one axis gets three variants of that command at different strengths. A delta naming several gets three variants that each answer the whole delta, each led by a different axis's command at full strength.

## Left out

- **The comp-led route** (`visualize`, `generate-image`, `impeccable-asset-producer`, and the `region-map` and `component-review` checkpoints) renders images outside the model-selection rule and the spend ceiling. Only the founder switches a project to `"buildPath": "comp"`.
- **`generate`** runs one element's variants straight into `live`; rung two of the tweak step uses `live` itself, after the founder picks the element.
- **`craft`** is a deprecated alias of new-work.
- **`pin`** makes a personal shortcut, the founder's to choose.
- **`impeccable-manual-edit-applier`** runs inside `live` on its own.

## House overrides

The precedence levels are the house's [source precedence](../../design-critique/references/house-principles.md#source-precedence). A finding from impeccable or its detector that a struck rule raised is no finding. One that a conditioned rule raised outside its condition is no finding either. Where the house sets a rule in impeccable's place, the rule is a record in design-critique's [rules/](../../design-critique/rules/), named below; this section says which impeccable line it overrides and why (#272).

### Struck or corrected

- **Weight on light text on dark** (`typeset`: "one step more weight"): `vault.dark-text-weight`. Its extra line height and tracking stand; the weight step goes, since Material's 2022 grade study found no readability need for it. Large text going lighter is a look choice no source splits by size.
- **The eyebrow above a heading** (`craft-floor`: "a ban, not a default"): `vault.ai-look`. GOV.UK sets a caption above a heading to say where the page belongs, so only a decorative eyebrow is an "AI look" default.
- **Stopping a loop offscreen** (`animate`): `vault.pause`. Not enough on its own, since WCAG 2.2 SC 2.2.2 asks for a control on motion that starts by itself and runs over 5 s.
- **Device-width breakpoints** (`adapt`: "Mobile: 320px-767px…", "640, 768, 1024px"): struck, for `vault.breakpoints`, as `adapt`'s own next line says.
- **Ripples as touch feedback** (`adapt`: "ripples, highlights"): `vault.press-state`. The touch feedback stands; the ripple is struck as its form, since it is one design system's pressed-state value and a value comes from the project's value system ([dependency order](../../design-critique/references/house-principles.md#dependency-order), step 4).
- **At most 4 visible options** (`critique`: "≤4 visible options", "8+ items: Overloaded"): struck as a count, for `vault.option-sets`. Short-term memory limits what a visitor holds, not what a grouped list can show.

### Conditions added

- **Body measure** (`craft-floor` 65–75ch, `operate` the same; `typeset` 45–75): `vault.measure`, counted in characters rather than `ch`, on Baymard's range and WCAG 2.2 SC 1.4.8's ceiling.
- **Line height under 1.3** (detector): `vault.leading`, a finding on body text only.
- **`flat-type-hierarchy`** (detector: heading and body under 1.25× in size): `vault.heading-step`, no finding where weight, space or tone carries the step, as `typeset` itself says.
- **Display at most 6rem, tracking no tighter than -0.04em** (`craft-floor`): one author's numbers with no source found; the project's type scale replaces them.
- **Light or dark picked from the use scene** (`craft-floor`): `vault.theme`. The visitor's system setting already says which they want, and most people read long text more easily light (NN/g 2020); shipping both themes doubles the colour work, which is why a one-theme project ships light unless its rules file rules dark.
- **Touch targets of 44×44 px** (`adapt`, `audit`): `vault.target-size`, at WCAG 2.2 SC 2.5.8's 24×24 floor. 44 px (Apple 44 pt, Material 48 dp) is a target a project's rules file may set as its own question; the vault holds only the floor.
- **A hamburger or drawer on mobile** (`adapt`): `vault.visible-nav`. Navigation out of sight is used less and found more slowly (NN/g 2016); keeping four links in view costs header room on a phone, which is why the menu takes over past four.

### The "AI look" bans: dated defaults, review by 14 Apr 2027

The record is `vault.ai-look`. These are impeccable's reaction to 2024–2026 model output (design-vault#119 F3), so they sit at precedence level 6. The rest of the Refuse list keeps impeccable's weight, its light-or-dark row as conditioned above.

A candidate that uses one is reported at P2 at most. It never fails a gate and never decides a pick. At the review date, check each against Anthropic's `frontend-design` list of current AI-made traits, which the House DNA follows, and strike what no longer marks it.

### Sources for the rules the house enforces

The rest of design-vault#119's sample stands, each rule a record citing the outside source that owns it. design-vault#119 cited three of them from memory or second-hand, not re-read: the 4 px step, web.dev's rendering and font guidance, and the W3C images tutorial.


- **Type.** `vault.body-size`: under 16 px, screen reading slows and a phone zooms into a form field; a dense working role fits less at 16 px, so it may go smaller (Carbon's productive set). `vault.paragraph-break`: a gap and an indent each mark a paragraph, so both together say it twice; a gap costs height, an indent keeps dense text compact. `vault.no-justify`: justified web text opens uneven word gaps that slow readers, dyslexic readers most; a ragged edge looks less formal, and as SC 1.4.8 is AAA, a project's rules file may rule otherwise.
- **Colour.** `vault.contrast`: below 4.5:1, or 3:1 for large text, many low-vision readers cannot read the text; pale brand colours lose a text role, and no brand rule lowers the floor. `vault.chroma-ends`: near white and black a screen holds little chroma, so a saturated tint or shade clips or shifts hue; the palette's ends read quieter than its middle.
- **Layout.** `vault.spacing-step`: one 4 px step makes every gap a multiple the eye reads as ordered; an optical nudge off the step needs a reason.
- **Motion.** `vault.motion-duration`: under about 100 ms a change reads as a jump, over 500 ms as a wait, and an exit can be quicker because the visitor has moved on; an authored focal entrance may run longer at the cost of that wait. `vault.motion-easing`: a decelerating curve reads as a thing arriving and settling; an exit or a loop may take another curve. `vault.reduced-motion`: movement can make a visitor with a vestibular disorder ill, and a designed reduced version keeps the meaning that switching motion off loses; it is more work, and as SC 2.3.3 is AAA, a project's rules file may relax it. `vault.motion-properties`: animating width, height, position or margin lays the page out again every frame and stutters, where transform and opacity do not; an effect that needs a layout change must be approximated.
- **Content.** `vault.undo`: a confirmation dialog trains a click-through and still loses the work, where undo lets the visitor recover; it needs the action held back or reversible. `vault.decorative-alt`: a screen reader reads every non-empty alt, so alt on decoration is noise; telling decoration from an image that informs is a judgement, and the second needs its alt.
- **Performance.** `vault.load` and `vault.web-vitals`: past web.dev's thresholds most visitors find a page slow or jumpy; heavy hero media and web fonts are what cost them. `vault.font-display`: without `swap` or `optional`, text stays invisible while the font loads; `swap` shows a fallback that then shifts, and `optional` may never show the web font on a slow first visit.
- Heuristics: Nielsen's ten heuristics (NN/g) stand as impeccable `critique` scores them; they are a frame for judging, not one rule.
