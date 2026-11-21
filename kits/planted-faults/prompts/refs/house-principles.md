# House principles

The house's design method, written once (#154, #172): two orders that decide which choice comes first and which source wins, then function fit. [Surface styling](surface-styling.md) and [text presentation](text-presentation.md) are the house's pieces for the treatment step, [brand palette](brand-palette.md) for colour and the logo, and [first-visit trust](first-visit-trust.md) for what a small business's or a solo advisor's site shows a first-time visitor. The research behind every line is in the design vault: `docs/research/principle-interactions.md` §1 and §5 for the orders, `docs/research/function-fit.md` Parts B and D for function fit.

A dated principle is reviewed a year after writing, and sooner when a platform ships a new design language or WCAG a new version (#183, `docs/research/house-audit-method.md` item 5).

## The two orders

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

- **Rule.** Code each part with one function:

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

- **When.** A function belongs to a part, never a whole component: a listing card is a C whose surface is an N, holding R, R-trust, T and its own S and A. Take the function from the brief, the project's rules file or a project document. Where none gives it, never guess it: report `FIT RISK: function unknown`, with the readings and what each changes, and judge nothing that rests on it.
- **Trade-off.** Coding every part costs critic time, and a model may code parts unreliably from a render; coding the component once costs every clash between its parts.
- **Clash.** ARIA's split wins over a look: a part that takes the visitor somewhere is N even when it looks like a button.
- **Era.** Timeless as ARIA's categories; the design-system groupings behind I against S are dated, current; review by 2027-10-14.
- **Source.** WAI-ARIA 1.2 §5.3 role categories, Material 3 component categories, Apple HIG components (primary); the split of I and S and of T and R-trust is #127 B7.1.

### Carriers and reserved properties

- **Rule.** A part shows its function by that function's carriers, and never takes a property another function reserves:

  | Code | Carried by | Reserved: no other function takes it | Who borrows it |
  |---|---|---|---|
  | N | In prose, an underline or 3:1 against the text with a cue on hover and focus (WCAG 1.4.1, G183); in nav and whole-card targets, position; a chevron or arrow where text is not plainly a link. Current page: a cue besides colour. | The link colour and the underline | Headings, labels, status text, emphasis |
  | A | A fill or a 3:1 edge, a verb label, a rung on the emphasis ladder (filled, tonal, outlined, text), hover and press states. The primary action holds the view's strongest colour. | The primary action's colour; a button shape with a fill or edge and a short verb label | Static tags, eyebrows in the button's type, decorative pills |
  | I | An edge or fill at 3:1, a label outside the field, a focus ring | An empty edged box on static content | Summary boxes, banners that look like a search box but are links |
  | S | A selected state not shown by colour alone: a check, a dot, a 3:1 edge, a weight change; the chip shape for filters | The selectable chip's shape, fill and edge; the selected tint; a column of check marks | Static facts as chips, tinted "best" rows, check-mark amenity lists |
  | T | Semantic colour with text or an icon, beside the thing it describes, one colour per status everywhere; an ARIA live region for a change | The semantic colours, and none near the action colour; motion that pulses or blinks | Brand-tinted availability, decorative pulsing |
  | R | Body type, the text-colour ranks, measure, headings. Proof: a plain dated source line, real photos, counts with their source. | For proof, the styling of ads, promotions and urgency | Proof styled as a promotion; a paid badge styled as a merit badge |
  | C | Space first, then a fill step or a border; depth only where it floats or acts | A container look the site declares to mean "tappable" | Static cards beside tappable ones of the same look |
  | D | Illustration, ground colour, display type, the mark, brand motion | Every signifier above; and the reverse, a functional part never takes the decoration's or an ad's look | Background art where the visitor works; text inside illustration |

- **When.** Every part with a code. Which edges need 3:1: [two border roles](surface-styling.md#two-border-roles).
- **Trade-off.** Every reservation takes a tool from brand expression.
- **Clash.** The [brand-layer line](#the-brand-layer-line) settles it. A brand colour that is also a signifier colour keeps the signifier's meaning.
- **Era.** The reservations are timeless; the carriers (underline, chip shape, the emphasis ladder) are dated, current; review by 2027-10-14.
- **Source.** Apple HIG Color, NN/g "Beyond Blue Links" (2015), GOV.UK Tag, WCAG 1.4.1 and 1.4.11, Material 3 (primary); the reserved column for C and D is inferred from false affordance (Gaver 1991) and NN/g banner blindness (2018). The table is #127 B7.2's synthesis, confidence 0.8.

### The function walk

- **Rule.** For each part, in this order, ask:
  1. What is its function code?
  2. Can a visitor act on it, and does it look as if they can? Its cell: perceptible (both), hidden (acts, looks static), false (static, looks actable), or correct rejection (neither). Hidden or false is a fault.
  3. Will a visitor know the action they want is here, and connect this part with it?
  4. Which properties carry its function, and does it take one [reserved](#carriers-and-reserved-properties) for another?
  5. Does each look on the page and the site mean one function? List every distinct treatment and its functions.
  6. Rank the parts by visual weight (squint), and by task priority for this page. Do the two orders match, with one primary action?
  7. Does decoration sit where the visitor works, or does a functional part look like an ad or a promotion?
  8. On a surface a visitor taps, does each target have one action and its own signifier?
  9. Is the moment relaxed or high-stakes (booking, payment, an error)? If high-stakes, is every signifier conventional?
- **When.** Every candidate with a part a visitor acts on or reads. A render answers whether a part looks actable; only the DOM or the code answers whether it is (its role and `href`), its hover and focus rules, its hit area and nesting. Where neither is given, answer those Unsure, never from the render.
- **Trade-off.** One more pass costs critic time, and a critic loses accuracy as checklists are added (#99 V8). A model's "no fault" on questions 4 and 5 is unverified until a seeded test shows it catches a static pill copying a button.
- **Clash.** A false or hidden affordance, a borrowed property, or a primary-action conflict that stops a task is P0, and bars the candidate from leading however it looks. Any other is reported at its severity on design-critique §4's scale.
- **Era.** Timeless.
- **Source.** Gaver (CHI '91) for question 2; the cognitive walkthrough (Wharton et al. 1994) for 3; WCAG 3.2.4 and GOV.UK Tag for 5; Apple HIG and GOV.UK Button for 6; NN/g banner blindness for 7; the HTML `a` content model for 8; Norman (2002) and Google's M3 Expressive research for 9. No source walks a page part by part; the walk is #127 Part D, written by the house.

### The beauty guard

- **Rule.** Judge function before beauty, as a separate pass with its own verdict. Walk the candidate you like most first.
- **When.** Any judgement from a render, by a person or a model.
- **Trade-off.** The separate pass costs time and adds a checklist (above).
- **Clash.** A fault that stops a task is never outweighed by beauty.
- **Era.** Timeless for people; the model-judge evidence (2024–2026) is dated, current; review by 2027-10-14.
- **Source.** NN/g "The Aesthetic-Usability Effect" (2024); Kurosu and Kashimura (CHI '95); Tuch et al. (2012) for the limits; "Fooling the LVLM Judges" (2025, weak). No study measures reviewers missing more faults on a beautiful render; the guard is an inference from these (#127 B1.4, confidence 0.7 for people, 0.75 for a model).

### The brand-layer line

- **Rule.** Be distinctive in the brand layer: ground colour, illustration, display type, voice, motion character, one signature move. Be conventional in the signifiers (what a link, button, field, selected state and status look like) and the interaction structure: lists stay lists, actions keep their labels, navigation stays where visitors look for it.
- **When.** Everywhere, most of all at a high-stakes moment (a price, availability, the handover to book, an error, sign-in), where expression keeps to type, colour role and voice, and moves no signifier. A relaxed moment (a guide page, a home hero) takes more. A dense list takes less novelty than a hero.
- **Trade-off.** Fully conventional reads as the generic "AI look"; fully expressive costs first-impression trust and usability.
- **Clash.** A brand idea that needs an unusual control keeps the control's core signifier (its label, its button or field shape, a link's underline) and must still read at a glance.
- **Era.** Timeless as a structure; what reads as conventional is dated, current; review by 2027-10-14.
- **Source.** Norman (2002) on relaxed and stressed use; Google's M3 Expressive research (2025); Lavie and Tractinsky (2004) on classical against expressive beauty (primary to strong secondary). The line is the house's synthesis (#127 B6.3, confidence 0.8).
