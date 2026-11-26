# First-visit trust

Why a first-time visitor to a small business's or a solo advisor's site needs what its records ask before they get in touch, and how clashes between them resolve (#144, #176, #272). The research behind every line is `docs/research/first-visit-trust.md` in the design vault.

Where a project's rules file and a record here disagree, [source precedence](house-principles.md#source-precedence) decides. A dated record is reviewed a year after writing, or sooner when a platform ships a new design language or WCAG a new version.

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

## Principles

### The field budget

Record: `vault.field-budget`.

- **Why.** The question protocol asks only for what the service needs and the asker knows what to do with; for a plain enquiry, the first reply needs no more than who wrote and what they want.
- **Trade-off.** A field cut raises the number of enquiries and lowers what each one says. Where more qualified leads are worth fewer leads is the owner's business fact.
- **Clash.** A wish to qualify the lead gives way to the protocol: the copy and the reply qualify.

### Feel the CV

Record: `vault.trust-cv`.

- **Why.** Procurement staff judge relevant experience by project kind and region, against terms of reference (World Bank Procurement Regulations §7.34–7.39), so specifics they can check carry more than size words. A reader who buys on referral or price takes the checklist alone.
- **Trade-off.** Specifics can expose a confidential mandate.
- **Clash.** Rows that name bodies against a rule that bans named clients: the rows name employers and the bodies that publicly asked for or published the work.

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

## What a visitor must be sure of

The default draft answer to the set-up question "What must a visitor be sure of before they write to you?" (`docs/research/function-questions.md` S4), offered to the client to correct. It decides the proof that sits next to the main action.

- **An advisor:** that you have done this kind of work for organisations like theirs, in their region, and that a real, named person does it (items 1, 3, 4).
- **A trade:** that you are licensed, have finished jobs like theirs near them, and what a call-out costs (items 3, 5, 6).
- **A consumer practice:** who will see them, where, what it costs or how the price is set, and that their details are safe (items 1, 5, 6, 9).
