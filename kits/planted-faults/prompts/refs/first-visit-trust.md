# First-visit trust

What a first-time visitor to a small business's or a solo advisor's site must see before they get in touch, when each item applies, and how clashes between items resolve (#144, #176). The research behind every line is `docs/research/first-visit-trust.md` in the design vault.

A project's rules file wins over every line here except a floor WCAG or the law sets, and, on behaviour, a line resting on domain evidence, which it departs from only on evidence of its own ([source precedence](house-principles.md#source-precedence)). A dated line is reviewed a year after writing, or sooner when a platform ships a new design language or WCAG a new version.

## The checklist

An advisor sells judgement (a consultant, a lawyer); a trade does jobs at an address (a plumber); a consumer practice serves the public by appointment (a clinic). Report a missing item only where its Applies column holds.

| # | Item | Applies | Era | Source |
|---|---|---|---|---|
| 1 | A named, real person and a real photo of the face; no stock people | Always for a solo practice; a firm shows its lead and its real team | Timeless | NN/g 2010, 2019; Stanford 2002 |
| 2 | What the practice does, for whom, where | Always | Timeless | NN/g 2019; design-critique §2's 5-second test |
| 3 | Qualifications shown as evidence of work | Always for an advisor; a trade or consumer practice shows licences and finished jobs instead | Timeless | World Bank Procurement Regulations §7.34–7.39; ADB 2026; Stanford 2002 |
| 4 | Publications and talks, each on its own page, a PDF behind an HTML gateway page | When the practice sells judgement | Dated, 2024–25 surveys; review by 2027-10-14 | Edelman–LinkedIn 2024 (secondary); NN/g 2020 |
| 5 | Fees, or how the price is set | A price set in advance is shown; a bespoke price gets its method or an estimate on request | Timeless | UK Provision of Services Regulations 2009 regs 8–9; NN/g 2006, 2019 |
| 6 | Location | Always the base country; a trade or consumer practice shows its full address and the area it serves; an international advisor shows the regions of its work | Timeless | NN/g 2019; Stanford 2002 |
| 7 | A contact route on every page: the email address in full as its own link text, a phone number only where the owner answers it, labelled "Telephone:" | Always. A booking link has no source either way: the owner decides | Timeless; the format current in 2026 | NN/g 2016, 2019; GOV.UK A to Z |
| 8 | An enquiry form, within [the field budget](#the-field-budget) | Only when the reply needs facts people forget to give in an email (a trade's postcode and job type), or the owner wants no public email | Timeless | GOV.UK question protocol; NN/g 2016 |
| 9 | A privacy note at the form | When a form collects personal data under UK or EU GDPR | Dated, current law | ICO, UK GDPR Art. 13 |
| 10 | Legal identity: legal form, register and VAT numbers, professional body, in the footer or a legal page | A UK provider; other countries' rules were not researched | Dated, current law | UK SI 2009/2999 reg. 8; SI 2002/2013 reg. 6 |
| 11 | Task text (navigation, headings, contact, work rows, summaries) in sentences of at most 25 words, technical terms explained once | Always for task text; a specialist's argument may run longer in the owner's voice | Timeless | GOV.UK "Use clear language" |
| 12 | Identity on every page: the name, a one-line bio, a link home | Wherever visitors land on deep pages, as an article a social post links to | Timeless | NN/g 2002 |
| 13 | Dates that show the site is current: a dated CV, the newest work's date, this year's copyright | Always | Timeless | Stanford 2002; NN/g 2016 |
| 14 | Third-party proof: testimonials, logos, named clients | Only real proof, used with consent, by `vault.proof`; with none held, links out to work that named bodies host | Timeless | NN/g 2016, 2019 |

A response-time promise is not an item: no independent source supports one.

## Principles

### The field budget

- **Rule.** A required field is one the first reply needs, by the question protocol: ask only where you need the answer to deliver the service and know what you will do with it. For a plain enquiry that is name, email and message. Each other field names the action its answer changes before the reply. At most one or two optional fields, each labelled optional.
- **When.** Any enquiry form, item 8.
- **Trade-off.** A field cut raises the number of enquiries and lowers what each one says. Where more qualified leads are worth fewer leads is the owner's business fact.
- **Clash.** A wish to qualify the lead gives way to the protocol: the copy and the reply qualify.
- **Era.** Timeless.
- **Source.** GOV.UK Service Manual, "Structuring forms" (domain evidence); NN/g, Whitenton 2016 (domain evidence, a heuristic, not a measured curve); Seckler et al., CHI 2014, left field count out as a business decision (`docs/research/house-audit-visual.md` V10, #183).

### Feel the CV

- **Rule.** For a reader who hires through procurement (a development bank's or a government's staff, arriving from a LinkedIn profile), show standing through work, not adjectives:
  - selected work as rows of period, body, role, country or region, and one line of what was done, sorted by theme;
  - checkable specifics (named bodies, roles, dates), never size words such as "40 years of experience";
  - standing shown by who asked ("The Asian Development Bank asked me to prepare …");
  - the newest article or talk on the home page, with its venue, before the CV;
  - a photo at a named event;
  - each credential stated once, in the profile, as a plain fact;
  - the CV both on the page, to read, and as a dated PDF, to take;
  - every fact agreeing with the LinkedIn profile, whose About text, skills and endorsements are not repeated.
- **When.** An advisor whose buyers select individuals against terms of reference. A reader who buys on referral or price takes the checklist alone.
- **Trade-off.** Specifics can expose a confidential mandate: a row names a client only where the owner clears it, and otherwise names the kind of body and the region.
- **Clash.** Rows that name bodies against a rule that bans named clients: the rows name employers and the bodies that publicly asked for or published the work.
- **Era.** Timeless as a pattern; the procurement rules are current to the 2025 World Bank and 2026 ADB texts; review by 2027-10-14.
- **Source.** Inference: no study tests felt against listed credentials. Built from the World Bank Procurement Regulations §7.34–7.39, an ADB selection deck (2026) and a World Bank-financed CV form (2025), which judge relevant experience by project kind and region (primary rules); NN/g 2010 and Edelman–LinkedIn 2024 (secondary).

## Clashes

| Clash | Resolution |
|---|---|
| Show fees against a bespoke-quote practice | The law draws the line: item 5. NN/g's representative prices suit packaged services, not bespoke work. |
| A face against a firm that wants to look bigger | Show the real people. A "we" for one person or a stock team is invented proof (`vault.proof`). |
| Fewer fields against qualifying the lead | [The field budget](#the-field-budget). |
| A credential stated once against making the reader feel the CV | [Feel the CV](#feel-the-cv). |
| A clear way to get in touch against never ending a page on "contact me" | The route is structure, not a sales line: the address as link text in every footer and a "Contact" label in the navigation. Pages end on the owner's idea. |
| Plain English against the owner's long sentences | Split by copy type: item 11. |
| An on-page CV against a PDF CV | Both, as in [feel the CV](#feel-the-cv). |
| A full address the law asks for against a home-based sole trader | The law wins where it applies; a service address may meet it. |
| Work rows that name bodies against a rule banning named clients | As [feel the CV](#feel-the-cv)'s Clash line. |
| Third-party proof against inventing none | Item 14. |
| A phone number against an owner who travels | Item 7. |

## What a visitor must be sure of

The default draft answer to the set-up question "What must a visitor be sure of before they write to you?" (`docs/research/function-questions.md` S4), offered to the client to correct. It decides the proof that sits next to the main action.

- **An advisor:** that you have done this kind of work for organisations like theirs, in their region, and that a real, named person does it (items 1, 3, 4).
- **A trade:** that you are licensed, have finished jobs like theirs near them, and what a call-out costs (items 3, 5, 6).
- **A consumer practice:** who will see them, where, what it costs or how the price is set, and that their details are safe (items 1, 5, 6, 9).
