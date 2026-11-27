---
name: design-critique
description: The portable design critique for any project's candidate — a page, a component, an artwork or a screenshot — and for a client asset (a photo, logo, live page or text) judged in place, for the question the client asked. Wraps `impeccable critique` where design mode is on, and adds Gestalt by name, conversion and trust, SEO, and a standard for whether anything should change. Carries no hard bans; a project's own gate does. Use for the fresh critic in a design round, whenever UI work is reviewed, or whenever a client asks what we think of something they already have.
---

# design-critique

This skill holds no brand rules, only the craft gate (§1a), which binds every project, and the [house principles](references/house-principles.md): which choice comes first, which source wins a clash, and how a part's look follows its function. A project's hard bans are that project's gate, which runs first and whose breaches are reported above everything here (Manta's gate is `design-review`). Never restate a project's palette, tokens or component specs. Its rules file owns them.

## 0. A fresh critic

Run in a subagent given the brief, the brief delta and this round's candidates only: never an earlier round, save the two settled shots of a kept draft the gate check gives for `vault.drafts-kept`, and never the building session's transcript. A critic never sees the same draft twice.

**Every image seen, before any verdict.** For each candidate, name each render or screenshot you were given and say you saw it. Where one is missing, will not open, or was removed from your view ("media removed"), stop: report which, and judge nothing (design-vault#90 P13).

**Stand-ins are judged for their craft only.** Where the dispatch lists stand-ins, a finding against what one shows is out of scope: leave it out (design-vault#91 S4). The craft done to it is judged: a cut-out's edge, a crop, scaling, a flattened mark (design-vault#169 B10).

**Only the tests the dispatch names**, where it names any. A problem found outside them, such as by a throttled first visit you thought to run, is a build note (§4): never a breach, a recommendation, or a reason against a candidate. So is a build matter, such as font loading or hosting, whichever test finds it, the audit's performance score included (design-vault#91 S8).

**Screenshots no older than the page.** Before judging a web candidate, compare the run time in each screenshot's name with the candidate's last change, which the dispatch gives. Where a screenshot is older, or the dispatch gives no last change, refuse to judge it and say why (design-vault#78).

A **client asset judged in place** — any photo, logo, live page or text the client already has, judged where it is used now — takes the same fresh critic, given the client's question, the asset and where it is used, in place of a brief. §5 holds the rest of that mode.

**Coarse to fine** (design-vault#258). Judge in three steps, finishing each before the next, and list findings and fixes in the same order: the function walk (§0a); then what stands out, the lenses that need the whole page (§2: hierarchy, grouping, how busy each section is, whether the page hangs together, conversion and trust, and fit with the brief and its tone line); then treatment, how the parts are styled, type among them (§2's house records at `treatment` and `value`, and motion). A verdict on a detail never colours the judgement of the whole. In a design round, a fresh type critic answers the type records (§2a), so you leave those records out, and still judge the type as part of the whole.

## 0a. The function walk, before beauty

Before §1, and before judging any candidate's looks, name the candidate you like most and walk it first, then the rest, by [the function walk](references/house-principles.md#the-function-walk). Give each candidate one row per part: the part, its function code, its affordance cell, any property it borrows, and its rank by visual weight beside its rank by task priority. Below the rows, list each fault by its question number. Report a part whose function [no file gives](references/house-principles.md#the-function-codes) as `FIT RISK: function unknown`. On a page, take whether each part can be acted on, what it is nested in and its hit area from the parts map `vault.one-target` runs (§1a), never from the render. An asset with no part but decoration takes one line saying so.

## 1. The vendored critique, where design mode is on

When the `impeccable` plugin is loaded, check its version against the pin in `${CLAUDE_PLUGIN_ROOT}/skills/design-round/references/impeccable.md`. `impeccable critique` runs its two assessments, A (the design review) and B (the detector and browser evidence), as two isolated subagents. In a design round the building session dispatches them (design-round §4) and gives you each candidate's two reports: merge them as its `critique.md` says under "Generate Combined Critique Report", the first line `Method: dual-agent (A: <id> · B: <id>)` with the two ids the dispatch gives. Drop each finding the project's `.impeccable/critique/ignore.md` matches, where it has one; persist no snapshot; and end with `Questions skipped: the design round puts its questions to the founder`. Anywhere else, run `impeccable critique <target>` and let it finish on its own terms, its degraded banner included where it cannot start subagents. Include its accessibility-dependent persona whatever its persona table selects. On a page or component, also run `impeccable audit <target>`: its accessibility, performance, responsive and theming scores, and the findings behind them. Report its findings, and the detector's, through that file's house overrides.

When the plugin is not loaded, say so in the report's first line, and run the lenses below alone. **Do not write a substitute for the plugin's critique.** Switching design mode on takes a session restart (`design-mode` skill).

## 1a. The craft gate

The craft gate is the vault's live rule records in [rules/](rules/) that a script, the code or the gate critics answer, in the form [rules.md](rules.md) sets out, save the WCAG ones (`vault.contrast`, `vault.control-edges`, `vault.target-size`, `vault.colour-script`, `vault.colour-look`, `vault.keyboard`, `vault.focus`, `vault.pause`); the records hold their wording. In a design round, design-round's [gate check](../design-round/references/gate-check.md) answers this gate: the building session runs the scripts below once, and three gate critics answer the look questions, so the whole-page critic leaves it out (design-vault#170). Run anywhere else, report each question by its id as PASS, FAIL with every breach, or "does not apply" with the reason. One breach fails the candidate. Where a command below starts with a variable rather than a folder, you opened this file by its path: put the installed plugin's folder, the one holding `skills/`, in its place.

- **`vault.curves-script`.** Run `node ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-curves.js` on every SVG file, on the page saved after its scripts ran (`python3 ~/design-vault/scripts/browse.py html <url> --out page.html`), and on the `morph.svg` check-flow.py writes for a morph; any line it prints is a breach, save a corner between two curves, or a kink where a curve meets a line, that the source has or the brief names, a morph's frames passing through one on the way to a named corner included: say so beside it. Then run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-overlay.py <mark> <source> --out <dir>`, which overlays the mark on its source and prints the largest edge offset against the limit for that kind of source. An IoU or area-overlap figure is no evidence of curve fidelity: a 30-segment chain overlaps a smooth curve at above 0.9.
- **`vault.contacts-script`.** Run `node ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-curves.js --contacts` on every SVG file and on the page saved after its scripts ran. Each `separate` or `shared edge, no underlap` line is a breach. A `covered` line passes here on the shapes it names as spanning the gap; whether their paint hides it is `vault.contacts-seam`'s to measure. A shape it names as unread (exit 6) is unmeasured: say so, and judge its contacts under `vault.contacts-code`. Each line ends with its contact as a `--contact` word: pass it to `look-renders.py contacts` unchanged, on the same file.
- **`vault.contacts-seam`.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-seams.py <file> --out <dir>` on every SVG file and on the page saved after its scripts ran, the files `vault.contacts-script` reads. It measures a `covered` contact through the covers `vault.contacts-script` names, so a cover whose paint lets the ground through fails like any other seam. Each FAIL is a breach, at the scales and frames it names. Report a NOT MEASURED contact (exit 6) as unjudged, never as a pass, and judge it under the question its line names: `vault.contacts-code` for a shape it could not read, `vault.contacts-look` otherwise.
- **`vault.contacts-code`.** Start from `check-curves.js --contacts`' list, and add each contact it cannot see: a stroke's width, a shape CSS or a canvas draws, one a `<use>` places, and one between two `<svg>` elements on a page. List every contact (stones on their centring, joints, water on its channel and in its fall), and say what geometry each side is drawn from, and how two fills that share an edge meet.
- **`vault.contacts-look`.** The building session renders it for the critics: `${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/look-renders.py contacts`, which crops each contact `vault.contacts-code` lists, at scales 1, 2 and 3, on the first frame, every key frame and the last, and magnifies each 4× by repeating pixels, never by rendering again. Judge its sheets (design-round's gate check §2).
- **`vault.curves-look`.** The building session renders it for the critics: `${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/look-renders.py bends` finds each curve's tightest bend, as `check-curves.js --bends` does, and shoots it at 8×. A curve an `<img>` draws: run it on the SVG file too. One CSS or a canvas draws: shoot its tightest bend by eye with `look.py zoom --scale 8`, at the `--width` and `--height` the bends report prints.
- **`vault.flow-script`.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-flow.py <page> --out <dir>`. It lists the pauses, jolts, first-frame jumps and speed steps and the length, and the starts and stops it leaves unjudged because the viewer never sees them at rest, and draws each element's speed over time in `speed.svg`: read the chart too. Where it says it cannot measure the page (motion by canvas, video, scroll, or a script other than a path morph), say so: `vault.flow-code` and `vault.flow-look` then carry these flags. Where it lists a stretch as not measured, the browser dropped frames there: judge that stretch in `vault.flow-look`'s scrub. A line it prints for an interface move is no breach: §2's motion lens judges that move.
- **`vault.flow-code`.** Take the timeline table, every move with its element, start, duration and easing: the one the candidate's engine writes itself, with its named cues, where it has one, or else write it by hand.
- **`vault.fall-script`.** Run `node ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/fall.js --check <table> --landing <thud or sink>` on the timeline table, with the landing the motion brief picks, or no `--landing` where it picks none. Each FAIL line is a breach. Report a NOT JUDGED fall, one whose easing names no scale, as unjudged, never as a pass, and judge it under `vault.flow-code`. With no `--landing`, put the landings it lists to the founder as a question.
- **`vault.length`.** Measure the motion from its first move to its last, as check-flow.py prints it, or a generated clip's length (design-vault#169 Q3 (A)), which `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-clip.py <clip>… --range <the motion brief's range, MIN-MAX seconds>` reads from each clip's header: its `length:` line answers this question. A length FAIL is a breach; report a length NOT JUDGED, a header with no duration, as unjudged, never as a pass.
- **`vault.clip-loop`.** The `check-clip.py` run above answers it on every generated clip, by its `loop:` line, reading each clip's request from the round's spend log, or `--log`. A loop FAIL is a breach. Report a loop NOT JUDGED, a model or log line it cannot read, as unjudged, never as a pass.
- **`vault.load`.** On a page, run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-load.py <page>`; its exit 1, a median Largest Contentful Paint over its limit, is a breach.
- **`vault.drafts-kept`.** `git ls-remote --tags origin 'rounds/<slug>-*'` shows each earlier round's tag. You list the tags; you do not open those rounds to judge them. Where this round edited an engine that an earlier round's drafts share, run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-frames.py hash <draft> --out <dir> --check <draft>/hashes.json` on each; a changed frame is a breach. Where it exits other than 0 or 1 on a draft, its 6 for a page it cannot check among them, or the draft has no `hashes.json`, answer `cannot measure`: the gate critics compare the draft's settled first screen with the one its round kept (design-round's gate check §2).
- **`vault.end-frame`.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-frames.py last <page> --at <selector> --asset <mark.svg> [--asset <wordmark.svg>] --out <dir>`; a pixel it counts as different at 1x or 2x is a breach. Any exit but 0 or 1, its 6 for a page it cannot check among them, answers `cannot measure`: the gate critics judge the last frame from the settled shots design-round's gate check §2 makes.
- **`vault.render-size`.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-render.py <render>…` on every brand-art render; it reads each one's model and aspect ratio from the round's spend log, and a render made by hand takes `--model` and `--aspect`. Each FAIL is a breach. Report a NOT JUDGED render as unjudged, never as a pass.
- **`vault.render-checkerboard`.** Where the brief asked for a transparent background, run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-render.py --transparent <render>…`; each checkerboard FAIL is a breach. Report a NOT JUDGED render as unjudged, never as a pass.
- **`vault.logo-unchanged`, `vault.logo-ground-script`.** For each placed client logo, run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-logo.py --logo <the lockup the rules file names> <page> --at <selector>`, or `<artboard image> --box x,y,w,h` on a lossless export of a print or social artboard; each FAIL is a breach of its question. Report a NOT JUDGED check as unjudged, never as a pass.
- **`vault.baked-ui-look`.** No script answers it. The gate critics answer it on every brand-art render at full size, looking closest at signs, plaques, screens and labels.
- **`vault.render-palette-look`.** The gate critics answer it on every brand-art render whose brief rules a palette, given the ruled colours as the brief or the project's rules file lists them, with their hex values. No script answers it.
- **`vault.headline-plain-look`.** The gate critics answer it on every brand-art render whose brief leaves a headline area, given that area's place on the render and the headline's cap height there, and judge it at full size. No script answers it.
- **`vault.one-target`.** On a page, run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/parts-map.py <page> --out <dir>`; each fault it prints is a breach.
- **`vault.affordance`, `vault.borrowing`, `vault.primary-action`, `vault.high-stakes`.** The function walk (§0a) answers them, by its questions 2, 4 and 5, 6, and 9. A P0 it finds under one is that question's breach, and so is every hidden or false part, save the hidden link `vault.affordance` excuses. So is every link the parts map marks `dead`. A lesser fault under the other three is a minor case: reported in the walk at its severity, never a breach.
- **`vault.proof`.** Trace each piece of proof to the project's rules file or a source the client supplied, and name that source; a piece with none is a breach.
- **`vault.reflow`, `vault.layout`.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-layout.py <page> --out <dir> --cta <selector>` with the call to action's selector from the dispatch. It answers each question pass or fail, and each range it prints under one is that question's breach. A run that prints NOT A GATING SWEEP does not count. With no call to action in the brief, leave out `--cta`: `vault.layout` does not apply.
- **`vault.focal-crop`.** For art placed behind a layout whose brief declares a focal box, add `--focal <selector>=x,y,w,h` to that same run, the selector the art's `<img>` or background box and the box in the art file's pixels, once per art. Each range under it is a breach. Report an art it lists as not measured (`cannot measure`, exit 6) as unjudged, never as a pass, and judge its crop by eye in the run's screenshots.

## 2. The added lenses

**Gestalt, by name.** Walk all seven, and for each one say what you found or that you found nothing: proximity · similarity · closure · continuity · common region · figure/ground · common fate (parts that move or change together, at the same moment, read as one group).

**Motion, by its kind.** Judge each motion by the kind the dispatch gives it (design-round §4), and give it no rule of the other kind:
- **Interface motion** keeps to the project's motion tokens, the durations and easings its rules file sets, and impeccable's `animate`.
- **Brand motion** keeps to the craft gate's motion questions and design-round's brand-motion easing: ballistic falls, the landings and holds the motion brief picks, its length from the motion brief. A landing the brief does not pick is `vault.flow-script`'s and `vault.flow-code`'s case. A named hold it does not call still or moving passes either way: list it as a question for the founder, with design-round's trade-off for it, never as a breach (design-vault#183 Q4 (A)).
- A motion the dispatch gives no kind takes the kind its part's function code gives (D is brand, any other interface); say so beside it.

WCAG's motion rules, `vault.pause` and reduced motion, bind both kinds.

**Conversion and trust.** The project's copy bans, from the dispatch, win over this lens (design-vault#121 b6): a point below that they ban, such as a risk-reversal guarantee under an urgency ban, is no finding and no recommendation.
- The 5-second test: above the fold, can a reader say what this is, who it is for and why they should care?
- CTA count and the friction budget.
- Risk-reversal microcopy.
- Objection handling.
- Credibility, and who is behind the product. On a small business's or a solo advisor's site, judge it by the `vault.trust-` records in [rules/](rules/), with the reasons in [first-visit trust](references/first-visit-trust.md).

Report absent social proof as a finding. Never fix it by inventing proof: `vault.proof` (§1a).

**Tone.** Does each candidate sit where its tone line says? The line is the one the dispatch gives for the candidate, else the brief's Tone. Check it on each scale in [tone](references/tone.md#the-five-scales)'s table. A scale the candidate sits off is a finding: name the choices that put it there and which way to move them, by the table's column of the choices that move it. Too loud costs a visitor more than too quiet ([tone](references/tone.md#the-five-scales), its trade-off), so weigh a candidate louder than its line above one quieter by as much. Where neither the dispatch nor the brief gives a tone line, say so in one line and skip this lens.

**SEO.** Title and meta description, the heading outline, internal linking, and above all **whether the `h1`'s promise matches what the page actually contains**. Skip this lens for an asset that is not a page, and say that you skipped it.

**The house records.** Run `node ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/gate.js list --asset <class> [--fact <fact>]… --reader whole-page ${CLAUDE_PLUGIN_ROOT}/skills/design-critique/rules`, with the class and facts the dispatch gives, and answer every record it prints by its question, coarse to fine as it orders them, citing its id with each finding. Read the reference sections it names for their reasons; never read [rules/](rules/) whole. The function walk (§0a) and the trust lens take many of them in their own order; answer each record once. Outside a design round, answer the type critic's records (`--reader type`) and its lens (§2a) here too.

## 2a. The type critic

In a design round, the type critic is a fresh subagent given the brief's type (the faces, scale and type rules the brief and the project's rules file set), this round's candidates, the stand-in list, its own critic examples, and what `gate.js list --asset <class> [--fact <fact>]… --reader type ${CLAUDE_PLUGIN_ROOT}/skills/design-critique/rules` prints, with the reference sections it names: no other rule, reference or report (design-vault#224, design-vault#258). It judges type alone: the faces and how many there are, the size and weight hierarchy, case and tracking, alignment, line spacing, emphasis, line length, the ranks of text colour, and whether like text is set alike; and it answers each record it was given by its question, citing its id. It reports in §4's form, every finding with its severity, the deficiency it removes and who would object, under §3's bar, then its build notes, then any two rules that cannot both hold here, quoting both; it names no leader, runs no gate and no impeccable command.

**Measure** (`vault.measure`). Count the characters the page sets; never work them out from a CSS width: `ch` is the width of a zero, most letters are narrower, so `68ch` can set 85 characters, and `ch` grows with the font size. On a page, run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/check-measure.py <page>`. It renders both ends of each width range the page's breakpoints make. Report the range it prints for each width; each line it lists outside `vault.measure`'s range is a finding. Where it names a stylesheet it could not read, run it again with `--widths` set to both sides of that sheet's breakpoints. On a screenshot, count three full lines of body text by hand at each width you have. Skip this lens, and say so, for an asset with no running text, or where the script finds none.

## 3. No change for the sake of change

**An edit needs a real deficiency that you can defend.** For every recommendation, name the deficiency it removes in plain user terms. Write *"the price is read first, so the score never anchors the comparison"*, not *"this would be more balanced"*. If you cannot finish that sentence, drop the recommendation. Do not soften it.

**Every criticism names who would object, and why, in the asset's real context**: the visitor to that page, the reader of that slot. *"A guest choosing a room cannot see the bed in its only photo"* names one; *"the logo sits off-centre"* names none until you say whom it bothers. A criticism with no one to object is dropped, and so is a trait every good example of its kind shares: a conference photo shows a lanyard, a dorm photo shows other beds.

- **A project rule is not a deficiency to design around.** Point at the project's rules file and move on.
- **Consistency with an existing surface beats a local improvement.**

## 4. Report

One report, in this order, under the `Judged as` line where the verdict is in place (§5):

1. **What you saw**: each candidate's renders, each marked seen (§0).
2. **The project's gate**: PASS, or every breach with its file and line. Where the project has no gate, write "no gate". Then **the craft gate**, question by question, by id, or in a design round "answered by the gate check".
3. **The function walk** (§0a): the candidate you liked most, then each candidate's rows, faults and FIT RISKs.
4. **The vendored critique** as it delivered it, unedited and with its own score, or in a design round as you merged its two reports (§1), then the audit the same way; or the line saying design mode is off.
5. **The added lenses**: Gestalt, motion by its kind, conversion and trust, SEO, and outside a design round measure (§2a), each named and each answered.
6. **Recommendations**, each with the deficiency it removes. Write "none" where the honest answer is none.
7. **Build notes**: problems found outside the tests in scope (§0), or "none".

Tag every breach, finding and recommendation with impeccable's severity: P0 blocking (the asset cannot do its job), P1 major (it does it with real difficulty, confusion or a wrong impression), P2 minor (a workaround exists, or few would notice), P3 polish. A breach of the project's gate or the craft gate is P0. A candidate showing what a House DNA `never` line names, where neither the brief nor the project's rules file asks for it, is reported at P2 at most and never fails a gate or decides a pick (design-vault#173); the DNA's fabricated-proof line is judged by `vault.proof` instead. Where the project's rules file bans the same thing itself, its rule and its severity hold (design-vault#121 b7).

Save every screenshot, sample and script output the report rests on as a file, and name each path in the report, so the building session can commit them beside it.

Then give the **review strip** the round record carries, as three lines:
- the project's gate and the craft gate, each PASS or FAIL with its breach count ("no gate" where the project has none);
- the critique's score, and the audit's where it ran;
- the top finding in one line.

In a design round, end with **your leader**: the one candidate you would take forward among those that pass the project's gate and the craft gate and have no P0 from the function walk, with one line of reason, and the runner-up you weighed it against, with why it lost; or "none" where no candidate does.

## 5. A client asset, judged in place

**The `Judged as` line.** Every in-place verdict opens with `Judged as: <asset> in <slot, page, audience>, for <the question asked>.` Judge only against that line. Research, scores or a rubric made for another slot or question is input, never the verdict: write your verdict from the asset in place before you open it, then use it to check a fact, never to add a fault. A score made for another slot backs a point only where the line says so (design-vault#106, design-vault#89 S1, S7). Run the gates and lenses above as far as they bear on that question, and name each one you skip.

**A fresh render.** A verdict on a live page cites a render of that page at desktop and phone width taken in this session: `python3 ~/design-vault/scripts/browse.py shot <url> --out <file> --full-page --viewport 1920x945`, and again at `390x664`: a desktop's and a phone's viewport, not their screens (design-vault#197, design-vault#237). Judge every item a visitor sees there, file quality included.

**A questioned rule.** When the founder questions an output a rule produced, re-check the rule against its source and context, not only the remedy (design-vault#89 S4).

**Two verdicts on one item** — a prose verdict and a score, or two critics: list where they disagree, and settle each before the founder sees either (design-vault#90 P15).

**An untested measure** — one checked only on the cases it was built from — never raises a confidence figure. Write "by eye" where the eye decides (design-vault#90 P3).

**Writing the verdict to the client.** The project's writing-to-the-client file, where it has one, wins over these:
- Answer only what was asked: no fix or question they did not ask for.
- Every verdict carries its reason, and a fault says why it matters to them. Never cut a reason to save length; cut a point instead.
- Name each item by where it sits on the page ("the photo at the top of the homepage", "top row, middle"), never by our ids, dates or events.
- Use the client's words for a fault, not the scoring words: "blurry", not "soft"; never a slot, criterion or score.
