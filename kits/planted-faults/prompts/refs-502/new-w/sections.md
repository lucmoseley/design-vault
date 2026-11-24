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

<!-- design-critique/references/first-visit-trust.md#the-checklist -->

## The checklist

An advisor sells judgement (a consultant, a lawyer); a trade does jobs at an address (a plumber); a consumer practice serves the public by appointment (a clinic). Each item's record says which of them it applies to; report a missing item only there.

| # | Item | Record | Why, and what it costs |
|---|---|---|---|
| 1 | A named, real person and their face | `vault.trust-person` | Visitors read portraits longer than bios and ignore stock people; the humans behind a business bolster trust (NN/g 2010, 2019). The cost is a real photograph to get. |
| 2 | What the practice does, for whom, where | `vault.trust-offer` | A hard-to-find "what the company does" was a main dissatisfaction (NN/g 2019). Saying it plainly narrows who feels addressed. |
| 3 | Qualifications as evidence of work | `vault.trust-credentials` | A development bank picks an individual on relevant qualifications and experience, judged against the job (World Bank, ADB). A list reads as a claim; work shown reads as proof, and takes room. |
| 4 | Publications and talks | `vault.trust-publications` | About three-quarters of decision-makers trust thought leadership over marketing to judge capability (Edelman–LinkedIn 2024, secondary). Old or thin work shown hurts more than none. |
| 5 | Fees, or how the price is set | `vault.trust-fees` | Hidden prices look dubious, and custom work can list representative cases (NN/g 2006, 2016, 2019); UK law asks a provider for its price or method. A stated price can lose a buyer who would have asked. |
| 6 | Location | `vault.trust-location` | A physical location bolsters trust (NN/g 2019; Stanford 2002). A home address is private, so a town or region may stand in. |
| 7 | A contact route on every page | `vault.trust-contact` | Prominent contact information builds trust, at least an email and a phone (NN/g 2016, 2019). Each route shown is one the owner must answer. |
| 8 | An enquiry form, within [the field budget](#the-field-budget) | `vault.trust-form`, `vault.field-budget` | Short forms, with one or two labelled optional fields, are finished more (NN/g 2016; GOV.UK question protocol). Fewer fields mean less to qualify a lead by; [the field budget](#the-field-budget) weighs that. |
| 9 | A privacy note at the form | `vault.trust-privacy` | UK GDPR Art. 13 makes privacy information due when the data is taken (ICO). It adds a line beside the button. |
| 10 | Legal identity | `vault.trust-legal` | UK law makes a provider show its name, legal form, address and register numbers (SI 2009/2999 reg. 8; SI 2002/2013 reg. 6). It adds footer weight. |
| 11 | Task text in short sentences | `vault.trust-plain-words` | GOV.UK splits sentences over 25 words so more people read them first time. A specialist's argument may run longer in the owner's voice. |
| 12 | Identity on every page | `vault.trust-identity` | A visitor from a social post lands deep, so the name and a link home belong on every page (NN/g 2002). It costs header room on each page. |
| 13 | Dates that show the site is current | `vault.trust-current` | A site shown recently reviewed is trusted more (Stanford 2002; NN/g 2016). A visible date that goes stale says the opposite. |
| 14 | Third-party proof | `vault.trust-proof`, `vault.proof` | Being connected to the rest of the web is a trust factor, and readers check a testimonial's author (NN/g 2016, 2019). Only real, checkable proof counts. |

A response-time promise is not an item: no independent source supports one. A booking link has no source either way: the owner decides.

<!-- design-critique/references/first-visit-trust.md#clashes -->

## Clashes

| Clash | Resolution |
|---|---|
| Show fees against a bespoke-quote practice | The law draws the line: `vault.trust-fees`. NN/g's representative prices suit packaged services, not bespoke work. |
| A face against a firm that wants to look bigger | Show the real people. A "we" for one person or a stock team is invented proof (`vault.proof`). |
| Fewer fields against qualifying the lead | [The field budget](#the-field-budget). |
| A credential stated once against making the reader feel the CV | [Feel the CV](#feel-the-cv). |
| A clear way to get in touch against never ending a page on "contact me" | The route is structure, not a sales line: `vault.trust-contact`. |
| Plain English against the owner's long sentences | Split by copy type: `vault.trust-plain-words`. |
| An on-page CV against a PDF CV | Both, as in [feel the CV](#feel-the-cv). |
| A full address the law asks for against a home-based sole trader | The law wins where it applies; a service address may meet it (`vault.trust-location`). |
| Work rows that name bodies against a rule banning named clients | As [feel the CV](#feel-the-cv)'s Clash line. |
| Third-party proof against inventing none | `vault.trust-proof`. |
| A phone number against an owner who travels | `vault.trust-contact`. |

<!-- design-critique/references/first-visit-trust.md#feel-the-cv -->

### Feel the CV

Record: `vault.trust-cv`.

- **Why.** Procurement staff judge relevant experience by project kind and region, against terms of reference (World Bank Procurement Regulations §7.34–7.39), so specifics they can check carry more than size words. A reader who buys on referral or price takes the checklist alone.
- **Trade-off.** Specifics can expose a confidential mandate.
- **Clash.** Rows that name bodies against a rule that bans named clients: the rows name employers and the bodies that publicly asked for or published the work.

<!-- design-critique/references/house-principles.md#every-element-earns-its-place -->

### Every element earns its place

Record: `vault.element-count`.

- **Why.** Every extra element competes with the ones the visitor needs and makes them harder to see (NN/g, heuristic 8). The test is relevance, not minimalism: a rich page that shows only what the task needs passes, and a sparse page that hides something the task needs fails.
- **Trade-off.** Hiding rarely used features behind a menu or a link costs the few who need them a step.
- **Clash.** None known.
- **Why no script answers it.** A count of elements or controls has no threshold to meet: the right number follows the page's task, which only a reader of the page judges.

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

<!-- design-critique/references/interaction-and-forms.md#data-has-three-more-states -->

### Data has three more states

Record: `vault.data-states`.

- **Why.** An empty box reads as broken: the visitor cannot tell loading from failure from no results (NN/g, Kaplan 2021). A skeleton holds the layout for a short first load, and a progress indicator tells the truth about a long one (Carbon). An empty state is the place to say why and what to do next.
- **Clash.** `vault.carry-status` says how a status looks; this record says which states must exist.

<!-- design-critique/references/interaction-and-forms.md#error-pages-are-plain -->

### Error pages are plain

Record: `vault.error-page`.

- **Why.** A visitor on an error page is already let down; a code, a joke or red text adds confusion or blame (GOV.UK error page patterns). What they need is what happened, what became of their answers and where to go.
- **Trade-off.** A brand may want personality on a 404; the house keeps wit to low-stakes surfaces, and an error is not one.

<!-- design-critique/references/first-visit-trust.md#the-field-budget -->

### The field budget

Record: `vault.field-budget`.

- **Why.** The question protocol asks only for what the service needs and the asker knows what to do with; for a plain enquiry, the first reply needs no more than who wrote and what they want.
- **Trade-off.** A field cut raises the number of enquiries and lowers what each one says. Where more qualified leads are worth fewer leads is the owner's business fact.
- **Clash.** A wish to qualify the lead gives way to the protocol: the copy and the reply qualify.

<!-- design-critique/references/house-principles.md#the-function-walk -->

### The function walk

For each part, in this order, the whole-page critic answers:

1. its function code: `vault.function-code`;
2. whether a visitor can act on it and whether it looks as if they can: `vault.affordance`. Its cell is perceptible (both), hidden (acts, looks static), false (static, looks actable) or correct rejection (neither); hidden or false is a fault;
3. whether a visitor will know the action they want is here: `vault.findable-action`;
4. which properties carry its function, and whether it takes one reserved for another: the carrier records above and `vault.borrowing`;
5. whether each look on the page and the site means one function: `vault.borrowing`;
6. its rank by visual weight against its rank by task priority, with one primary action: `vault.weight-order`, `vault.primary-action`;
7. whether decoration sits where the visitor works: `vault.decoration-place`;
8. on a surface a visitor taps, whether each target has one action: `vault.one-target`;
9. whether the moment is high-stakes, and its signifiers conventional: `vault.high-stakes`, `vault.brand-layer`.

- **When.** Every candidate with a part a visitor acts on or reads. A render answers whether a part looks actable; only the DOM or the code answers whether it is (its role and `href`), its hover and focus rules, its hit area and nesting. Where neither is given, answer those Unsure, never from the render.
- **Trade-off of the rules.** Every actable part looking actable costs a quiet surface some calm: a dimmed field or a borderless control reads cleaner but is found later or not at all (Gaver 1991; NN/g on low contrast). One main action per view lets a visitor find the next step at a glance; a second action of near-equal priority pays, taking a lesser look and being found less, and where two choices are truly equal `vault.primary-action`'s "at most one" lets neither take the main look. Ranking parts by task priority puts information above decoration, which spends a hero image's pull; the brand speaks through the brand layer instead (`vault.brand-layer`).
- **Trade-off of the walk.** One more pass costs critic time, and a critic loses accuracy as checklists are added (#99 V8). A model's "no fault" on questions 4 and 5 is unverified until a seeded test shows it catches a static pill copying a button.
- **Clash.** A false or hidden affordance, a borrowed property, or a primary-action conflict that stops a task is P0, and bars the candidate from leading however it looks. Any other is reported at its severity on design-critique §4's scale.
- **Source.** No source walks a page part by part; the walk is #127 Part D, written by the house. Each question's source is its record's.

<!-- design-critique/references/house-principles.md#top-tasks-on-the-homepage -->

### Top tasks on the homepage

Record: `vault.top-tasks`.

- **Why.** Visitors come to a homepage for a few things, and look for a way into each; NN/g found a homepage should give clear starting points for its main one to four tasks, and McGovern that the tasks that matter are often fewer than five. A homepage built around one action leaves the visitor who came for the second thing hunting.
- **Trade-off.** Each starting point given a place on the first screen takes weight from the main action; past four or so they flatten into a list of equal links.
- **Clash.** `vault.primary-action` wins on weight: the first task is the main action and the rest are quieter entries. Which tasks they are is the brief's, from what visitors ask the client (`design-project` §1, S2).

<!-- design-critique/references/busyness.md#how-busy-for-which-visitor -->

## How busy for which visitor

Record: `vault.busy-density`.

- **Why.** Density is the value a visitor gets over the time and space the interface takes (Ström-Awn), so the right level follows the task. A working tool for repeat, skilled people goes dense: the Shopify admin "is high density by default", and Material makes high density opt-in for "List, tables, and long forms". A page judged at first sight pays for complexity: appeal falls strongly at high complexity and slightly at low (Reinecke et al. 2013).
- **Trade-off.** Too sparse fails too: NN/g found pages "too sparse" (2018) and, on wide screens, content dispersed across viewports, with "a clear preference for a condensed layout" (2023). Flat signifiers cost 22% more time and hold only where information density is low (Moran 2017).
- **Clash.** What a visitor tolerates follows age and culture: people over 45 liked low complexity more (Reinecke et al.), and Chinese users preferred "fairly high information density" while still missing features on complex sites (Cheng and Nielsen 2016). The record moves a step only where the brief states the audience. The one-step moves are the house's; neither study measured a step. `vault.tone-space` sets the space between groups by tone and yields to this record on a working view's density.

<!-- design-critique/references/house-principles.md#the-function-codes -->

### The function codes

Record: `vault.function-code`. The codes:

| Code | Function | Examples |
|---|---|---|
| N | Navigate: takes the visitor somewhere | link, nav item, a card that is one link |
| A | Act: does something here | button |
| I | Text input | text field, search box |
| S | Select or filter | checkbox, radio, filter chip, switch, sort |
| T | Status: a state that changes | availability, loading, saved, error |
| R | Read; **R-trust** for proof | heading, body, photo; source line, review count |
| C | Contain or group | card, section, sheet, divider |
| D | Decorate or brand | illustration, ground, the mark |

- **Why per part.** A listing card is a C whose surface is an N, holding R, R-trust, T and its own S and A. A guessed function makes every later judgement on the part a guess too, so the report carries the readings and what each changes, and judges nothing that rests on it.
- **Trade-off.** Coding every part costs critic time, and a model may code parts unreliably from a render; coding the component once costs every clash between its parts.
- **Clash.** ARIA's split wins over a look: a part that takes the visitor somewhere is N even when it looks like a button.

<!-- design-critique/references/house-principles.md#source-precedence -->

### Source precedence

- **Rule.** Inside one step, a higher level wins. The levels, highest first:
  1. law and WCAG 2.2 AA;
  2. the project's rules file and gate;
  3. domain evidence (Baymard, NN/g, GOV.UK, USWDS);
  4. expert craft ranges;
  5. impeccable's craft rules;
  6. impeccable's "AI look" bans.

  On look (the value system, the brand), the project wins at level 2 as listed. On behaviour (what a part does, how a visitor reaches it), a project rule that departs from level-3 evidence wins only on evidence of its own, recorded in its rules file; without it, the clash goes to the founder.
- **When.** Two rules set one property of one part to different values and neither yields to the other. Between steps, the dependency order decides first.
- **Trade-off.** A project rule may beat better evidence at level 4 on a recorded reason. Asking evidence for a behaviour that departs from level 3 slows a client's own idea down.
- **Clash.** Two rules the levels cannot rank go to the founder: two of one project's rules, or two vault rules below level 2 where neither names the other in `yields-to`.
- **Era.** Timeless as an order; the sources named at each level are dated, current; review by 2027-10-14.
- **Source.** `adopt-or-build.md` F5 (#119); the founder's ruling on #103 Q5 (A). The behaviour bar is GOV.UK's (Service Manual, "Making your service look like GOV.UK"; #183 item 2).

<!-- design-critique/references/house-principles.md#carriers-and-reserved-properties -->

### Carriers and reserved properties

Each function's carriers, and the properties it keeps for itself, are its record's; `vault.borrowing` checks the reserved properties across the page.

| Code | Record | Who commonly borrows its reserved properties |
|---|---|---|
| N | `vault.carry-navigate`, `vault.colour-script` | Headings, labels, status text, emphasis |
| A | `vault.carry-act`, `vault.primary-action` | Static tags, eyebrows in the button's type, decorative pills |
| I | `vault.carry-input`, `vault.control-edges` | Summary boxes, banners that look like a search box but are links |
| S | `vault.carry-select` | Static facts as chips, tinted "best" rows, check-mark amenity lists |
| T | `vault.carry-status` | Brand-tinted availability, decorative pulsing |
| R | `vault.carry-read`, `vault.proof` | Proof styled as a promotion; a paid badge styled as a merit badge |
| C | `vault.carry-contain`, `vault.grouping` | Static cards beside tappable ones of the same look |
| D | `vault.decoration-place`, `vault.brand-layer` | Background art where the visitor works; text inside illustration |

- **Why.** A visitor reads a property as the function they have learnt it carries; a part that borrows one makes a false promise (Gaver 1991), and a functional part dressed as decoration or an ad is skipped (NN/g banner blindness, 2018). Which edges need 3:1: [two border roles](surface-styling.md#two-border-roles).
- **Trade-off.** Every reservation takes a tool from brand expression.
- **Clash.** The [brand-layer line](#the-brand-layer-line) settles it. A brand colour that is also a signifier colour keeps the signifier's meaning.
- **Source.** The table is #127 B7.2's synthesis, confidence 0.8; the reserved column for C and D is inferred from false affordance and banner blindness.

<!-- design-critique/references/tone.md#colour-share -->

## Colour share

Record: `vault.tone-colour-share`.

- **Why.** Neutrals carry "most backgrounds, text, and shapes" (Atlassian), and USWDS splits the non-neutral colour 60/30/10 with the neutral base usually "the predominant tone". More colour on the surface makes a page more colourful, and saturation raises arousal (below). A small accent share is what makes the accent stand out: the 10% "lifts the subject out from its background" (Rauno, "Novelty", 2026, who offers it as an observation, not a prescription).
- **Trade-off.** A restrained share keeps colour for meaning and action (Dannaway, 2026) and reads calm; a committed or drenched surface gives energy and brand presence and leaves colour less room to signal. The appeal curve peaks at moderate-to-high colourfulness and varies by audience, so the share is set for the audience, not by a fixed number.
- **Clash.** The House DNA's taste line bans several colours at equal weight with none dominant, which a share that names one leading hue meets. The bands take USWDS's 60/30/10 and impeccable's four strategies with its 30–60% for a committed surface, both convention; matching them to energy is the house's, not measured.

<!-- design-round/references/impeccable.md#struck-or-corrected -->

### Struck or corrected

- **Weight on light text on dark** (`typeset`: "one step more weight"): `vault.dark-text-weight`. Its extra line height and tracking stand; the weight step goes, since Material's 2022 grade study found no readability need for it. Large text going lighter is a look choice no source splits by size.
- **The eyebrow above a heading** (`craft-floor`: "a ban, not a default"): `vault.ai-look`. GOV.UK sets a caption above a heading to say where the page belongs, so only a decorative eyebrow is an "AI look" default.
- **Stopping a loop offscreen** (`animate`): `vault.pause`. Not enough on its own, since WCAG 2.2 SC 2.2.2 asks for a control on motion that starts by itself and runs over 5 s.
- **Device-width breakpoints** (`adapt`: "Mobile: 320px-767px…", "640, 768, 1024px"): struck, for `vault.breakpoints`, as `adapt`'s own next line says.
- **Ripples as touch feedback** (`adapt`: "ripples, highlights"): `vault.press-state`. The touch feedback stands; the ripple is struck as its form, since it is one design system's pressed-state value and a value comes from the project's value system ([dependency order](../../design-critique/references/house-principles.md#dependency-order), step 4).
- **At most 4 visible options** (`critique`: "≤4 visible options", "8+ items: Overloaded"): struck as a count, for `vault.option-sets`. Short-term memory limits what a visitor holds, not what a grouped list can show.

<!-- design-critique/references/surface-styling.md#dividers-against-space-and-fill -->

### Dividers against space and fill

Records: `vault.dividers`, `vault.grouping`.

- **Why.** A divider only groups, so it needs no 3:1.
- **Trade-off.** Space needs room; a line costs a pixel but adds noise in every gap.
- **Clash.** A border or divider that groups differently from the spacing makes the grouping ambiguous, so the spacing is fixed first rather than a line added to override it.

<!-- design-critique/references/layout-and-data.md#space-marks-the-most-important-part -->

### Space marks the most important part

Record: `vault.space-emphasis`.

- **Why.** Open space around a part sets it apart as its own group, and a part set apart draws the eye (NN/g, Gordon 2021; Harley 2020). Space ranks a part without adding colour or weight.
- **Trade-off.** Space costs room: a dense working view, a table or a dashboard, cannot spare it and ranks by size, weight and tone.
- **Clash.** `vault.weight-order` settles which part leads; this record only says how space serves it.

<!-- design-critique/references/tone.md#symmetry -->

## Symmetry

Record: `vault.tone-symmetry`.

- **Why.** "Asymmetry is dynamic and engaging. It creates a sense of energy and movement. Symmetry is quiet and static" (NN/g, 2020). Symmetric logos raise perceived quality through perceived stability (Wu, PLoS ONE, 2025).
- **Trade-off.** Symmetry reads stable and trustworthy and can read static; asymmetry gives energy and needs balance by weight so it reads as chosen.
- **Clash.** Wu's effect holds only under low mental load and was measured on logos, so on a busy working page symmetry buys less. impeccable lets Persuade and Experience surfaces go asymmetric and keeps Operate and Read predictable (`layout.md`).

<!-- design-critique/references/busyness.md#what-makes-a-page-busy -->

## What makes a page busy

Records: `vault.busy-cues`, `vault.element-count`.

- **Why.** A page looks busy when parts of low value compete with the parts the visitor needs, not when it holds many parts (NN/g, 2021), and a busy-looking page can pass by showing "sufficient information, and only sufficient information". Clutter's usual sources are redundant items, decorative icons, type flourishes, over-detailed or watermark images (NN/g homepage guidelines; Whitenton 2013) and borders, backgrounds and shadows used to group what space should group (Gordon 2021; Polaris). Perceived complexity is predicted (R2 .65, Reinecke et al. 2013, 450 sites) mostly by how much of the page is text and non-text content, how many text groups and how many image areas it holds; colour adds little, and symmetry and balance dropped out of the model. Screenshot metrics explain about half of complexity ratings along three lines: amount, organisation and how well parts stand apart (Miniukovich and De Angeli, abstracts). Rosenholtz's Feature Congestion measures clutter as how hard it is to add an item that still draws the eye. No source sets a value above which a web page is too busy, so the record is judged by eye, by the squint test.
- **Trade-off.** Cutting to look minimal can drop what the task needs; `vault.element-count` keeps the needed parts however busy they look.

<!-- design-critique/references/grounds-and-gradients.md#section-grounds -->

### Section grounds

Record: `vault.section-ground`.

- **Why.** A band of colour is a common region (Palmer 1992), so it groups what sits inside it and splits it from what is outside. That makes it a statement that the function has changed. GOV.UK keeps its strong full-width panel for confirmation and interruption pages and "never" for anything else. Polaris keeps working areas free of bright fills. Butterick lists "layouts built with large blocks of color" among the '90s habits. NN/g found that a full-width line or a large gap can read as the end of the page. A band edge is the same kind of break (an inference), so a sliver of the next section should show past it.
- **Trade-off.** Alternating bands make a long marketing page easy to chunk, but they add no information once every section has one, and each edge risks a false floor.
- **Clash.** How much of the page is in colour at all is `vault.tone-colour-share`'s. A project's own zone rule, such as Manta's loud marketing and calm working zones, sits in its rules file and wins.

<!-- design-critique/references/house-principles.md#the-brand-layer-line -->

### The brand-layer line

Record: `vault.brand-layer`.

- **Why the stakes set the room.** Under stress a visitor relies on what they already know (Norman 2002), so a price, availability, the handover to book, an error or sign-in takes the least novelty; a guide page or a home hero takes the most.
- **Trade-off.** Fully conventional reads as the generic "AI look"; fully expressive costs first-impression trust and usability.
- **Clash.** A brand idea that needs an unusual control keeps that control's core signifier (its label, its button or field shape, a link's underline), which still reads at a glance.

<!-- design-critique/references/surface-styling.md#one-shape-family -->

### One shape family

Record: `vault.shape-family`.

- **Why.** Rounder shapes read softer and sharper ones harder (Bar and Neta 2006), so the rounding carries the brand's tone. Mixed corners at random read as unbalanced (Apple WWDC25).
- **Trade-off.** One fixed family is calm but can feel flat. Material 3 Expressive (2025) is said to invite tension between shapes, but its page could not be read; a brief that wants that tension says so in its rules file.
- **Clash.** The UI transfer from the curvature studies is an inference, not a finding; the brief's tone wins.

<!-- design-critique/references/house-principles.md#expression-by-frequency -->

### Expression by frequency

Records: `vault.motion-frequency`, `vault.delight-frequency`.

- **Why.** Frequent parts move briefly or not at all, and expression is kept for the rare moments where it is noticed.
- **Trade-off.** A product kept plain everywhere it is used often can feel flat; its character then rests on the brand layer and the rare moments.
- **Clash.** `vault.high-stakes` and `vault.brand-layer` win: no delight goes on a price, a booking handover or an error. `vault.motion-duration` sets the range for every move; `vault.motion-frequency` keeps frequent parts at its short end.

<!-- design-critique/references/house-principles.md#distinct-from-the-category-leaders -->

### Distinct from the category leaders

Record: `vault.brand-distinct`.

- **Why.** A brand cue that a category leader already owns reminds the visitor of the leader, not of this brand. Romaniuk's research puts uniqueness first: an asset must evoke one brand only.
- **Trade-off.** Avoiding a category's usual colour or style can make a site look like it belongs to another category; the conventional parts of `vault.brand-layer` keep it recognisable.
- **Not carried.** Romaniuk's other measure, fame, is the share of category buyers who name the brand from the asset alone. It needs a survey of buyers, which no critic or script in a round can run.
- **Clash.** `vault.brand-layer` wins: navigation, controls and layout stay conventional even where competitors share them.

<!-- design-critique/references/tone.md#setting-the-direction -->

## Setting the direction

Record: `vault.tone-direction`.

- **Why.** A direction that names its tone lets a critic check "is this as calm as asked" rather than read adjectives. Palette, face and corner shape each move the scales, so one picked without the others pulls the feel apart.
- **Trade-off.** A named style ("quiet luxury", neo-brutalism) carries fifty decisions in two words, and a dated look with them; it is placed on the scales and its motifs taken on purpose, never as the tone itself.
- **Clash.** impeccable's direction step chooses a world and a colour strategy (`new-work.md` §4); the scales say what feel that world must reach, and the brief's tone wins where the two disagree. A product's described behaviour ("calm coaching") does not set the surface's energy (impeccable `new-work.md`).

<!-- design-critique/references/tone.md#mixed-aesthetics -->

## Mixed aesthetics

Record: `vault.tone-mix`.

- **Why.** A deliberate mix of eras, such as bitmap type over a Renaissance painting, "creates a moment of curiosity", useful "for driving first impressions and establishing tone" and not "often in productivity software" (Rauno, "Contrasting Aesthetics", 2024). It works with "authoring intent", and by holding the rest of the part constant.
- **Trade-off.** A mix raises richness and novelty and costs consistency, the same patterns everywhere inside the system (NN/g, consistency and standards). Carbon allows a contrasting type moment where a visitor enters a product and the page "opens up", not inside a card or data table.
- **Clash.** Faces from different periods are mixed with care (Google Fonts Knowledge, pairing), and two faces are the usual limit, each with one role (Butterick). The mix stays in the brand layer: `vault.brand-layer` wins where a mix would touch a signifier.

<!-- design-critique/references/tone.md#typeface-by-tone -->

## Typeface by tone

Record: `vault.tone-face`.

- **Why.** "Different fonts convey different feelings, and you want a font that complements the tone of your text" (Typography Handbook, 2026). Readers "react to it in an emotional way before anything else", so a face is chosen for how it makes readers feel, then for how it works (Google Fonts Knowledge, "Emotive considerations").
- **Trade-off.** A face with a point of view carries the tone in display type; a neutral, readable body face lets it, and system faces suit tools and dashboards (Typography Handbook, 2026; Carbon's productive and expressive type sets). Size, weight and spacing then follow the face (`vault.type-size` and the other typeface-traits records).
- **Clash.** What a face evokes is cultural and moves with time: "these associations can change over time, too" (Google Fonts Knowledge). A subject association alone (books want a serif) is the default impeccable exists to break.

<!-- design-critique/references/text-presentation.md#near-black-and-the-house-dna -->

### Near-black and the House DNA

Record: `vault.dna-near-black`.

- **Why.** Anthropic's `frontend-design` counts "tinted near-black (#0B0B0B, #111) standing in for black" as template chrome that turns up whatever the subject (3 Sep 2026). Both values carry no hue, so "tinted" there reads as black lightened, not a hue: the tell is a stock dark nobody chose.
- **Trade-off.** A dark tinted toward the main hue ties the page to its brand, at the cost of one more token to keep in step.
- **Clash.** On a dark ground, and for near-black text, the tint rule wins over House DNA `never` line 5. A near-black ground is one of the neutral greys `vault.text-tint` tints, and `vault.logo-anchors` tints dark grounds toward a logo's hue. The line still catches a near-black standing in for black that nothing chose, a hue-less stock value above all, reported at P2 at most like every DNA miss.

<!-- design-critique/references/tone.md#saturation -->

## Saturation

Record: `vault.tone-saturation`.

- **Why.** Saturation raises arousal ("Arousal = −.31B + .60S"; Valdez and Mehrabian 1994), and "saturated and bright colors were associated with higher arousal" (Wilms and Oberfeld 2018).
- **Trade-off.** High chroma carries energy and draws the eye, so it is spent where attention should go; neon "may distract users" (NN/g, 2025).
- **Clash.** A chroma past the display's gamut is clipped and changes look (jakub.kr), so a loud tone stays inside it. impeccable's 70–85% saturation for quieter is a convention with no source.

<!-- design-critique/references/busyness.md#coloured-boxes -->

## Coloured boxes

Record: `vault.box-fills`.

- **Why.** A filled, labelled rectangle reads as a button: "giving headings a background color will make them resemble buttons when they're not", and "Avoid having many colorful boxes of different sizes on a page", since people "have difficulty picking out the clickable elements when similar-looking items compete" (NN/g, Loranger 2015). Polaris keeps vibrant fills for "smaller surface areas" such as buttons and badges, and calls bright or contrasting container colours "a cluttered UI"; a grey ground "visually recedes".
- **Trade-off.** No source gives a count of coloured boxes a page may hold; the record judges competition with the controls, not a number. A marketing hero may take a coloured ground on purpose (`docs/research/surface-styling.md` B5.3); Polaris's lines are admin guidance, so the large-container clause binds working views only.

<!-- design-critique/references/tone.md#white-space -->

## White space

Record: `vault.tone-space`.

- **Why.** Density adds to a page's visual complexity, which people judge within 50 ms and like low (Tuch et al. 2012); past its peak, complexity costs appeal steeply (Reinecke and Gajos 2014). More space reads calmer and more ordered. "Some whitespace has meaning almost as salient as the darker pixels" (Ström-Awn, 2024).
- **Trade-off.** "Too much white space can be perceived as a lack of content and substance, whereas too little can come off as disorganized" (CXL). A working tool for skilled users earns density by the value per screen it gives (Ström-Awn's Bloomberg Terminal); how dense a working view goes is `vault.busy-density`'s ([busyness](busyness.md#how-busy-for-which-visitor)).
- **Clash.** What white space means in advertising comes from 20th-century North American art and rhetoric, and "its meanings are sufficiently different across cultures" (Pracejus, O'Guinn and Olsen 2013), so any reading of it beyond calm and order is cultural. `vault.space-emphasis` places space around the leading part; this record sets the page's total.

<!-- design-round/references/impeccable.md#the-ai-look-bans-dated-defaults-review-by-14-apr-2027 -->

### The "AI look" bans: dated defaults, review by 14 Apr 2027

The record is `vault.ai-look`. These are impeccable's reaction to 2024–2026 model output (design-vault#119 F3), so they sit at precedence level 6. The rest of the Refuse list keeps impeccable's weight, its light-or-dark row as conditioned above.

A candidate that uses one is reported at P2 at most. It never fails a gate and never decides a pick. At the review date, check each against Anthropic's `frontend-design` list of current AI-made traits, which the House DNA follows, and strike what no longer marks it.
