# House principles

The house's design method (#154, #172): two orders that decide which choice comes first and which source wins, then function fit. [Surface styling](surface-styling.md) and [text presentation](text-presentation.md) give the reasons for the treatment step's records, [brand palette](brand-palette.md) for colour and the logo, and [first-visit trust](first-visit-trust.md) for what a small business's or a solo advisor's site shows a first-time visitor. The research behind every line is in the design vault: `docs/research/principle-interactions.md` §1 and §5 for the orders, `docs/research/function-fit.md` Parts B and D for function fit.

A dated principle is reviewed a year after writing, and sooner when a platform ships a new design language or WCAG a new version (#183, `docs/research/house-audit-method.md` item 5).

## The two orders

Every record carries both: its `stage` is its step in the dependency order, and its `source` strength and `yields-to` place it in the source precedence.

### Dependency order

- **Rule.** Decide each part in four steps. An earlier step wins a clash with a later one by default:

  | Step | Decides | Reads | Decided by |
  |---|---|---|---|
  | 1 Function | One function code per part | The part, not its component; the page's task priority; the brief | [The function codes](#the-function-codes) |
  | 2 Role | The signifier and token role that carry the function: primary action, control edge, link, status chip, card edge | Brand tone and the zone's energy; density; whether the visitor reads or operates | [Carriers](#carriers-and-reserved-properties); prominence by task priority |
  | 3 Treatment | The property that expresses the role: border, fill, shadow, shape, weight, motion | The ground; the treatments next to it; the device and input | WCAG, then domain evidence, then surface styling and text presentation |
  | 4 Value | The number | The project's one value system | The project's rules file |

- **When.** Every part of an asset, decoration included.
- **Trade-off.** Function first takes signifier properties away from brand expression. The [brand-layer line](#the-brand-layer-line) says where expression stays free.
- **Clash.** The earlier step wins: where the brand radius makes a static chip look like a filter chip, the chip takes another shape. A later step's finding against an earlier decision is reported, never dropped: it goes back to the brief or to the founder. Where a project's rules file fixes one look across functions (one pill for buttons, filter chips and static facts), the walk's fault on each part where that look means two functions stands, and goes to the founder as a clash until the project rules on it.
- **Era.** Timeless.
- **Source.** House synthesis over WAI-ARIA 1.2, Material 3 and Apple HIG for step 1, and the sources of each later step (`principle-interactions.md` §1, #121; confidence 0.7). The direction, abstract before concrete, is Garrett's (The Elements of User Experience, 2000) and Material 3's token tiers (a role named once, a value filling it). Garrett also names "a ripple effect up and down the planes" (#183 item 1).

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

## Function fit

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

### Whole targets

Records: `vault.whole-target`, `vault.whole-target-look`.

- **Why.** A visitor aims at the whole thing they see, not at its label. GOV.UK linked the whole task row after users tried to press the status labels, and makes the whole accordion heading the button; NN/g found a larger target catches more of the clicks people mean.
- **Trade-off.** A row or card that is one target cannot hold a second action without hiding it; the second action splits the part into separate targets.
- **Clash.** `vault.one-target` wins: a part with two actions is two targets, each with its own signifier.

### Top tasks on the homepage

Record: `vault.top-tasks`.

- **Why.** Visitors come to a homepage for a few things, and look for a way into each; NN/g found a homepage should give clear starting points for its main one to four tasks, and McGovern that the tasks that matter are often fewer than five. A homepage built around one action leaves the visitor who came for the second thing hunting.
- **Trade-off.** Each starting point given a place on the first screen takes weight from the main action; past four or so they flatten into a list of equal links.
- **Clash.** `vault.primary-action` wins on weight: the first task is the main action and the rest are quieter entries. Which tasks they are is the brief's, from what visitors ask the client (`design-project` §1, S2).

### The beauty guard

- **Rule.** Judge function before beauty, as a separate pass with its own verdict. Walk the candidate you like most first.
- **When.** Any judgement from a render, by a person or a model.
- **Trade-off.** The separate pass costs time and adds a checklist (above).
- **Clash.** A fault that stops a task is never outweighed by beauty.
- **Era.** Timeless for people; the model-judge evidence (2024–2026) is dated, current; review by 2027-10-14.
- **Source.** NN/g "The Aesthetic-Usability Effect" (2024); Kurosu and Kashimura (CHI '95); Tuch et al. (2012) for the limits; "Fooling the LVLM Judges" (2025, weak). No study measures reviewers missing more faults on a beautiful render; the guard is an inference from these (#127 B1.4, confidence 0.7 for people, 0.75 for a model).

### The brand-layer line

Record: `vault.brand-layer`.

- **Why the stakes set the room.** Under stress a visitor relies on what they already know (Norman 2002), so a price, availability, the handover to book, an error or sign-in takes the least novelty; a guide page or a home hero takes the most.
- **Trade-off.** Fully conventional reads as the generic "AI look"; fully expressive costs first-impression trust and usability.
- **Clash.** A brand idea that needs an unusual control keeps that control's core signifier (its label, its button or field shape, a link's underline), which still reads at a glance.

### The default button in a dialog

Records: `vault.dialog-default`, `vault.dialog-default-look`.

- **Why.** People press the button that stands out, or press Return, without reading it first (Apple HIG).
- **Trade-off.** Where a visitor chose the destructive action themselves (emptying the bin), it stays the default even though it cannot be undone, and saves a step (Apple HIG); opening focus on the safe button instead costs the visitor one more click.
- **Clash.** `vault.primary-action` still holds one main action a view; in a dialog, a destructive action is never it. `vault.undo` decides whether the dialog should appear at all.

### Icons earn their place

Record: `vault.icon-use`.

- **Why.** Few icons mean the same thing to everyone: home, print and the magnifier for search (NN/g). Any other icon is guessed at, so it needs words beside it, and one symbol used for two things breaks even the known ones (GOV.UK).
- **Trade-off.** Labels take room. In a tool people return to every day, they learn its icons, and GOV.UK allows icons more freely there.
- **Clash.** `vault.carry-act` allows an icon-only button whose glyph is clear, and wins there.

### Images earn their place

Record: `vault.image-earns`.

- **Why.** Visitors study images that carry what they came for and skip pictures added for decoration; a real portrait outdrew a longer written bio (NN/g, reviewed 2026).
- **Trade-off.** An image can carry a feeling the brief names, such as a place's mood, so the test is information or a named feeling, not information alone.
- **Clash.** `vault.decoration-place` keeps decoration out of where the visitor works; this record asks whether the image belongs at all.

### Expression by frequency

Records: `vault.motion-frequency`, `vault.delight-frequency`, `vault.motion-frequency-look`.

- **Why.** Frequent parts move briefly or not at all, and expression is kept for the rare moments where it is noticed.
- **Trade-off.** A product kept plain everywhere it is used often can feel flat; its character then rests on the brand layer and the rare moments.
- **Clash.** `vault.high-stakes` and `vault.brand-layer` win: no delight goes on a price, a booking handover or an error. `vault.motion-duration` sets the range for every move; `vault.motion-frequency` keeps frequent parts at its short end.

### Distinct from the category leaders

Record: `vault.brand-distinct`.

- **Why.** A brand cue that a category leader already owns reminds the visitor of the leader, not of this brand. Romaniuk's research puts uniqueness first: an asset must evoke one brand only.
- **Trade-off.** Avoiding a category's usual colour or style can make a site look like it belongs to another category; the conventional parts of `vault.brand-layer` keep it recognisable.
- **Not carried.** Romaniuk's other measure, fame, is the share of category buyers who name the brand from the asset alone. It needs a survey of buyers, which no critic or script in a round can run.
- **Clash.** `vault.brand-layer` wins: navigation, controls and layout stay conventional even where competitors share them.

### Every element earns its place

Record: `vault.element-count`.

- **Why.** Every extra element competes with the ones the visitor needs and makes them harder to see (NN/g, heuristic 8). The test is relevance, not minimalism: a rich page that shows only what the task needs passes, and a sparse page that hides something the task needs fails.
- **Trade-off.** Hiding rarely used features behind a menu or a link costs the few who need them a step.
- **Clash.** None known.
- **Why no script answers it.** A count of elements or controls has no threshold to meet: the right number follows the page's task, which only a reader of the page judges.
