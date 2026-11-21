# Dispatch

This candidate: MantaHostels, the homepage, before launch: says what MantaHostels is, collects launch-news contacts by email, and sends visitors to the destination guides. Judge this one page as it stands, as a candidate for the live site.

Stand-ins: none.

# The project: PRODUCT.md

# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

**Primary: the backpacker choosing a hostel**, usually on a phone, mid-trip or planning the next hop, comparing several hostels quickly in order to book. Indonesia first (Bali/Lombok), then Indonesia-wide, then SEA. Dorm inventory is the screen — hostels only, not budget hotels.

**Secondary: the hostel owner or manager**, an independent property (non-franchise) in a market that runs on bank transfer, cash and WhatsApp. Reached by cold B2B outreach; there are no pre-existing owner relationships.

## Product Purpose

A **direct-booking search-and-redirect platform** — a discovery layer, never the merchant. It ranks hostels purely on merit, builds a dense and representative incentivised-review corpus, and routes travellers to book direct (or out via OTA affiliate links if they prefer), so hostels keep more of what travellers pay.

Success is the Trivago/Kayak position for SEA hostels: the trusted discovery layer.

## Positioning

The axis is **findability** — a fuller, more representative review picture plus merit-only ranking, laddering to one outcome: the right hostel, found faster — together with hostel-aligned economics.

Deliberately *not* the axis: social/meet-people (Hostelworld owns it with ~13M reviews of network density; never compete there), choice/certainty (Booking.com owns it), and fake-review policing (both incumbents already do it, so it is the smallest differentiator and must never anchor demand-side positioning).

The durable, demand-safe claim names no competitor: **"hostels keep more when guests book direct."** Held off the site until Hostelworld answers the cl. 6.1(c) consent ask or declines the application (#78); Booking.com does not gate it. It then returns to the homepage hero and meta description (#3652).

## Operating Context

- Phone-first, frequently on poor connectivity, often mid-transit.
- The comparison surface is scan-heavy: list rows compared against each other, not read one at a time.
- Booking completes **off-platform** — Manta hands over to the hostel's own booking route or to an OTA. No checkout is built here.
- Solo founder. Every architectural and operational choice assumes solo operation.

## Capabilities and Constraints

Confirmed capabilities: search and sort (vibe, surf/dive proximity, review-keyword search, recency-weighted scores, live availability); a review corpus with category sub-scores; a rewards programme with lifetime review tiers redeemable at partner hostels.

**Hard constraints that bind any interface:**

- **Never display OTA availability or prices for comparison.** Barred by Hostelworld cl. 6.1(c) and Booking.com General Partner Terms cl. 7.2(a)(vi) absent written, correctly-scoped consent, which is not held.
- **Never publish OTA review scores, sub-scores or review counts** on any Manta surface. Manta's own review data is unaffected — publish it freely, and never label it as an OTA's.
- **Never cache or store OTA availability or prices**, and never copy OTA-sourced text, photos, descriptions or review text.
- **Merit ranking is payment-independent.** Rank, listing presence and OTA-exit availability are never a function of partner status. Status-gated features — badge, direct exit, perks, tools — are fine.
- **All prices are tax-inclusive**, declared once at list level ("all prices include taxes"), never per-card noise.
- **No urgency theatre**: no flash pricing, no strikethroughs, no discount countdowns, no scarcity manufacturing.
- **A score never appears without its review count**, always paired with a word from a fixed scale (≥9 Loved · ≥8 Great · ≥7 Solid · below that Mixed). Zero reviews shows "No reviews yet" in muted grey, never an invitation to review.

## Brand Commitments

Binding, and specified in full in `docs/brand/brand-sheet.md` (currently v2.32), which is the canonical source of truth — **implement it, do not re-derive it**.

- North star: **"Loud moments, calm machine."** Beachy, personality-forward, Hostelworld's energy executed with more craft and honesty. Sterile/corporate is the named enemy; effortless is the first feeling.
- **Energy is localised, not uniform** — marketing zones run loud, the working area stays calm and scannable. This is described in the brand sheet as "the brand's spine".
- Name and wordmark: **Manta**Hostels, one word, Quicksand Bold.
- Voice: sentence case, no emoji in product copy, and **no em dash anywhere in website copy** — `·` separates the halves of a metadata title. The brand sheet's §11 names 11 banned AI-writing tells alongside those; `npm run check:copy` gates the lexical ones over `app/`.
- Visual identity is settled and the mascot mark is final (`mark-final.svg`). Illustration-led for decorative surfaces; photography on hostel listings.

## Evidence on Hand

- `docs/brand/brand-sheet.md` — canonical brand spec, complete and current-state only.
- `docs/data/evidence-audit.md` + `evidence-audit.csv` — 228 partnerable properties, 172 confirmed hostels across 23 nodes.
- `docs/brand-assets/` — fonts, logo and mark SVGs.
- `docs/research/competitor-teardown.md` — OTA pricing, UX and review mechanics.

**Absences future work must not fabricate:** there are no customers, no testimonials, no press, no live bookings and no partner hostels yet. The product is pre-launch — a static landing page plus SEO destination-guide routes. Do not invent social proof, review counts, partner logos or usage figures for any surface.

## Product Principles

1. **Trust is the product** — an internal integrity principle, not the demand-side pitch. Rankings and scoring methods are published; estimates round down.
2. **Honesty as UX** — failure states are designed, not hidden. Full hostels are greyed out rather than removed; unmatched hostels get "availability not shown — check with the hostel" rather than a guess.
3. **Merit ranking is inviolable** — never implement rank or presence as a function of payment.
4. **The traveller is always innocent** — a reward code that fails at a front desk is honoured immediately and recovered from the partner afterwards.
5. **Simplicity and tool discipline** — no speculative architecture; a tool earns its place by a concrete recurring task.

## Accessibility & Inclusion

WCAG AA for text is the working floor, and the brand sheet resolves the palette's known contrast traps rather than leaving them to judgement — see its "text-safe partner rule" and its night-ground pattern.

Two project-specific requirements:

- **Error and sold-out states are never signalled by colour alone.** Under protanopia and deuteranopia `coral` and `danger` collapse to the same dark yellow-brown regardless of hue, so a text label or icon is what actually carries the meaning.
- **A focus ring is never removed without a replacement indicator.**


# The project's rules file: DESIGN.md

---
name: MantaHostels
description: Loud moments, calm machine — a beachy hostel-discovery brand where energy never costs a search.
colors:
  ink: "#0A3542"
  lagoon: "#0C93A8"
  lagoon-text: "#08706F"
  turquoise: "#23BFB2"
  sand-page: "#FBF6EA"
  sand-border: "#EDE6D6"
  surface: "#FFFFFF"
  text-muted: "#5C6B72"
  coral: "#FF5D3A"
  coral-hover: "#E64A28"
  coral-active: "#CC3F1F"
  amber: "#F4B942"
  peach: "#eab998"
  success: "#2E8F5B"
  success-text: "#1E6B42"
  warning: "#BB8311"
  warning-text: "#6E4E08"
  danger: "#A6203C"
  muted-night: "#8f999e"
  danger-night: "#F2A0B0"
typography:
  display:
    fontFamily: "Quicksand, 'Trebuchet MS', sans-serif"
    fontWeight: 700
    lineHeight: 1.15
  heading:
    fontFamily: "Quicksand, 'Trebuchet MS', sans-serif"
    fontWeight: 600
    lineHeight: 1.25
  body:
    fontFamily: "'Nunito Sans', system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "'Nunito Sans', system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: 1.4
  cta:
    fontFamily: "'Nunito Sans', system-ui, sans-serif"
    fontSize: "19px"
    fontWeight: 700
    lineHeight: 1.3
rounded:
  chip: "6px"
  control: "8px"
  card: "12px"
  pill: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
components:
  button-primary:
    backgroundColor: "{colors.coral}"
    textColor: "{colors.surface}"
    typography: "{typography.cta}"
    rounded: "{rounded.control}"
    padding: "12px 24px"
  button-primary-hover:
    backgroundColor: "{colors.coral-hover}"
    textColor: "{colors.surface}"
  button-primary-active:
    backgroundColor: "{colors.coral-active}"
    textColor: "{colors.surface}"
  button-outline:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "8px 16px"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "{spacing.md}"
  score-chip:
    backgroundColor: "{colors.turquoise}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.chip}"
    padding: "2px 8px"
  badge-pill:
    backgroundColor: "{colors.amber}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "2px 10px"
  nav:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    height: "72px"
    padding: "0 24px"
  nav-mobile:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    height: "56px"
    padding: "0 16px"
---

# MantaHostels design system

> **`docs/brand/brand-sheet.md` (v2.32) is the source of truth.** This file is a derived, machine-readable restatement for design tooling. Where the two disagree, the brand sheet wins — and the fix is to correct this file, never to re-derive the brand.

## Overview

North star: **"Loud moments, calm machine"** — beachy, personality-forward, Hostelworld's energy done honestly. Sterile/corporate is the enemy; **effortless** is the first feeling, with trustworthy and fun close second.

**Energy is localised, not uniform — this is the brand's spine.** Two zones, and every surface belongs to exactly one:

- **Hero/marketing** (homepage and destination-page top banners, emails, social, rewards): saturated grounds, big type, badges. Volume ~6–7. Its job is *feeling*.
- **Working area** (search results, comparison, filters, booking): white cards on sand, colour only where it carries information. Volume ~4–5. Its job is *speed*.

**Day/night.** Day is the default everywhere (turquoise heroes, sand pages). The night ground (`ink`) appears **only in named, bounded contexts**: the nav bar, footer, reward moments, nightlife content, social tiles, the hero wave, and the interior announcement block. Never per-page on whim. Same hues, same type, same components — only the ground flips.

**What makes a block an interior announcement**, all three or it is page copy: it speaks about Manta's own state — what Manta is doing, or does not yet offer — rather than delivering the page's subject; it comes after the content the page exists to deliver, never inside it; and a page carries at most one. The destination pages' "coming soon" notice is the live instance.

## Colors

**Every colour has exactly one job. Colour that carries no information does not appear in the working area.** Warm = act, cool = read.

| Token | Job — the only job |
|---|---|
| `ink` | Text, headings, night ground, wordmark anchor |
| `lagoon` | Rating-manta fill, focus rings, borders, icon strokes — **fills and strokes, never text** (3.6:1) |
| `lagoon-text` | The text-safe partner: links, ghost-button labels, any lagoon-coloured type |
| `turquoise` | Day hero grounds, score chips, wordmark "Hostels" |
| `sand-page` / `sand-border` | Working-area page ground / card borders and dividers |
| `surface` | Cards — white means elevated and tappable, always |
| `text-muted` | Secondary text (light grounds only — 2.37:1 on ink) |
| `coral` | **CTAs only.** One per view |
| `amber` | **Rewards only.** No "Top rated" pill — §11 bars the string. Never price urgency |
| `peach` | **Illustration and hero art only** — the frangipani-petal accent |
| `success` / `warning` / `danger` | Semantic fills — availability, warnings, errors and sold-out |
| `success-text` / `warning-text` | Text-safe partners for chip labels and semantic copy |
| `muted-night` / `danger-night` | Secondary copy and error/sold-out **on the ink ground only** |

**The text-safe partner rule.** Every colour here was chosen for how it looks as a *fill*. Fill selection optimises for chroma; text selection optimises for luminance contrast, and the two pull in opposite directions. **A colour is not cleared for type until measured against the grounds it will sit on.** Under 4.5:1, it gets a named darker partner and the original is marked fill-only — not a caveat, not a size workaround, never a quiet exception in one component. Assume the next colour added will need one too.

**Semantics are chips, not coloured type.** Render a semantic state as a tinted chip carrying its text partner — `success-text` on a ~15% `success` tint, `warning-text` on a ~16% `warning` tint, `danger` on a ~12% `danger` tint — or as a border or icon. Never set copy in a raw fill colour. The one non-semantic tint is the lagoon wash `#E6F6F8` (~10% `lagoon` on white): hover and selected states only, never a card ground.

**Text on turquoise grounds is ink, never white.** White on `#23BFB2` is 2.3:1. Ink reads 5.7:1. The single sanctioned exemption is the wordmark's "Hostels" half.

**The night pattern — read before putting any component on ink.** In one line: **on ink, text is `white`; the semantic is carried by the existing token as a border, icon or chip fill.** Do not invent light text partners for the night ground — white already reads 13.12:1 on ink, so a light partner buys nothing and forces the token into a lightness collision.

Measured against `ink #0A3542`:

| Clears AA text (≥4.5:1) | Component only (3–4.5:1) | **Fails both** |
|---|---|---|
| `white` 13.12 · `sand-page` 12.16 · `peach` 7.43 · `amber` 7.41 · `danger-night` 6.52 · `turquoise` 5.73 · `muted-night` 4.51 | `coral` 4.30 · `warning` 3.98 · `lagoon` 3.59 · `success` 3.25 | `text-muted` 2.37 · `lagoon-text` 2.22 · `success-text` 2.02 · `danger` 1.81 · `warning-text` 1.72 |

**Fixed text-on-colour pairings:** ink on turquoise (5.7:1) · ink on amber (7.1:1) · white on coral (3.0:1, **and only at ≥19px/700**) · white on ink. Score chips take ink, never white.

## Typography

**Quicksand** for display, headings and UI emphasis — 700 for h1, hero, wordmark and score chips; 600 for h2/h3 and card titles. **Nunito Sans** for body and UI — 400 body, 600–700 labels and buttons. Body 14–15.5px at line-height ~1.6.

**Primary CTA label: Nunito Sans 700, ≥19px.** This scopes to the single coral CTA per view only; outline, ghost and row-level controls sit at 13–16px and are unaffected. Both reasons bind. Brand: the single coral object is the loudest thing in a volume-6 zone, and a 15px label is a timid CTA in a brand whose north star is energy. Accessibility: white on coral is 3.0:1, which clears the 3:1 component floor but fails AA for text unless the label is large — **19px at 700 clears it; 18px does not.** This is a type fix, not a colour fix; darkening coral to reach 4.5:1 loses the brightness that makes it read as pressable.

**Casing:** sentence case for body copy and buttons ("Book this hostel", never "BOOK THIS HOSTEL"). Uppercase is reserved for badges and filter labels, sparingly. No emoji in product copy.

## Layout

**8px spacing grid.** Nav 72px desktop / 56px mobile — 72 fits a 48px mark with 12px padding plus wordmark and an outline "Sign in"; 56 matches platform convention while preserving list density on a scan-heavy product.

**The nav bar is ink on every page type.** One variant, not two — a sand nav on a sand page is 1.00:1 and only exists as a bar by adding a border, while chrome that changes ground between page types reads as a different site section or a rendering fault.

**Below 768px, the links collapse behind a "Menu" button**; the wordmark and toggle share the one 56px row, and the panel opens below it rather than growing the row. Desktop is unchanged — the links stay inline. The current page's nav link carries `aria-current="page"` and drops its underline for semibold instead.

**Listing-card anatomy — photo-led.** A photo fills the left ~35%, flush, with carousel dots. Name top-left, no pill — brand sheet §11 bars "Top rated" (#978); the compound rating on its own line directly beneath the name, chip-first and left-aligned ("8.9 · Great · 214 reviews"); the price block top-right ("Dorms from / Rp 145k / night"); then a bold comparable facts line ("1.2 km to centre · 150 m to the surf") over a muted flavour line carrying the voice; bottom-right is a pure action zone — amenity icons left, Compare plus a quiet outline "View beds" right.

The score is met early in the scan, left-aligned at a fixed position so it forms a vertical column row-to-row, and always ahead of price. **Price stays inside the card box.**

## Elevation & Depth

**Borders first.** `sand-border` at 1–1.5px does the work almost everywhere; box-shadow is reserved for hover and popover states. **Nothing sits at rest under a heavy shadow.** White = elevated and tappable.

## Shapes

Radii: **8px** controls, **10–12px** cards, **6px** score chips, **999px** pills for badges, tags and status chips.

Icons: outline, rounded caps and joins, ~1.75px stroke at 20px (Tabler/Lucide-style), coloured `ink` or `lagoon`. **No emoji and no unicode-glyph icons** — a tick or arrow character is not an icon.

Motion — quick and honest, no bounce or spring theatre. Fast 120ms, standard 180ms, easing `cubic-bezier(0.2, 0, 0, 1)`. Hover lightens or tints a ground; press scales to 0.97. **Motion never announces itself.**

Focus rings use `lagoon`; error-state borders use `danger`. **A focus ring is never removed without a replacement indicator.** Exception: on a turquoise ground the ring is `ink` — `lagoon` is only 1.59:1 there.

## Components

**Rating unit.** Five manta silhouettes at 13–17px. Filled = solid `lagoon`; empty = `lagoon` outline stroke at ~1.5px — outline versus solid is the whole distinction. Half = left-half solid clip. Always accompanied by the numeric score. **Grounds: white, sand and ink only — never turquoise** (`lagoon` on turquoise is 1.59:1).

**Score display.** A score never appears without its review count, and the numeric score is always paired with a word from a fixed scale: **≥9 Loved · ≥8 Great · ≥7 Solid · below that Mixed.** The scale is fixed so it cannot inflate, and "Mixed" exists so the bottom of the range has a real word. Zero reviews shows **"No reviews yet"** in muted grey, in the slot the score would occupy — never an invitation to review. Category sub-scores render on the detail page and in comparison only, never in the results row (brand sheet §7).

**Booking handover, never checkout.** Brand sheet §12a owns it: one handover module, a coral "Book direct with the hostel" exit, ink-outline OTA exits with no OTA price anywhere, the honesty line always visible, "Saved to your trips" as the only confirmation and it promises no reward code.

**Hostel testimonial — a separate component, never a review card.** A quote the property supplied about itself is not a guest review and must not be built as one with the label swapped. It is a pull-quote, not a card: no `surface` white ground, no `sand-border`, no card radius — set it on the `sand-page` ground with a single `lagoon` left rule, quoted, in italic body type. It carries **no rating unit, no score, no sub-scores, no badge, no stay month, no reviewer name or avatar**, and it never counts toward a review count anywhere on the page. Its attribution — "from Hostel X's own guest feedback" — sits inside the component in `text-muted` and is never optional, never a caption a layout can drop. Where testimonials and reviews appear on one page they never interleave: testimonials sit in their own labelled block, above or below the review list, never inside it (#997).

**Buttons.** The single coral CTA per view is the sticky compare bar on a search view, the hero search button on a marketing view. Nav "Sign in" is always an outline. **Row CTAs are never coral and never say "Book"** — coral is one-per-view, and "Book" is a false label because booking happens off-platform. Rows take a quiet outline **"View beds"**.

**Cards.** White, `sand-border` at 1–1.5px, 10–12px radius. Tinted card grounds are reserved for genuinely special rows (partner spotlight), **never list items**.

**Prices.** Tax-inclusive, declared once at list level ("all prices include taxes") — never per-card noise, never strikethrough or discount theatre.

## Do's and Don'ts

**Never:**

- **`coral` as a ground, decoration or wordmark colour.** CTAs only, one per view. This rule is dual-purpose — CTA discipline *and* anti-copycat: a warm-orange button is category-universal ecommerce grammar, a warm-orange page field reads as Hostelworld.
- **Orange brand grounds.** Turquoise/sand is our field; orange is Hostelworld's and is their single strongest recognition cue.
- **The logo mark or the rating unit on a turquoise ground.** 1.20:1 and 1.59:1 respectively. Where either must appear over a turquoise zone it sits on a bounded ink form inside it — a wave band, a nav bar.
- **White type on turquoise** (2.3:1), except the wordmark's "Hostels" half.
- **Raw fill colours as text** — use the named text-safe partner.
- **Light text partners on the night ground** — white is already 13.12:1 there.
- **A hostel-supplied testimonial rendered in review chrome** (its own component, under Components). The property is an interested party, so a quote of its own that reads as an independent guest review is a false claim in Manta's voice, not a styling slip.
- **Urgency theatre** — flash pricing, countdowns, strikethroughs, manufactured scarcity. Banned outright, not just recoloured.
- **Colour alone** to signal error or sold-out. Always a text label or icon too.
- **Gradients in UI.** They live only in the primary logo mark; UI is flat.
- **Emoji in product copy.**

**Do:**

- Keep the working area calm — one focal action, colour only where it carries information.
- Let the loud half be a *claim*, with plain, specific mechanics directly beneath it. A loud line followed by more loudness is the failure mode; the calm half is what makes the loud half credible.
- Design the failure states: greyed-out "no space for your dates" rather than hidden, honest "availability not shown — check with the hostel" rather than a guess.

## References

**Inspiration library** — `docs/inspiration/catalogue.json`: the design vault's Manta-judged references, exported here and never edited in this repo. Each entry's `fit.manta.groups` names the Manta project groups it serves and `page_parts` the parts of a page it is about; `fit.manta.verdict` and `fit.manta.take` say whether and what to take, citing the `docs/brand/brand-sheet.md` section it answers to. Before drafting or judging a surface, read its project group; where it has none, or its group holds no entries, the entries whose `page_parts` name its page part. Take only what an entry's take names; an `adapt` or `off-brand` entry is still precedent.

The library is a consumer of the sheet and overrides nothing in it. An entry's `image_recipe` is prose for recreating a look, never a spec or a token.

**Design-system corpus** — `docs/design-system/`: the Claude Design export, reconciled to the sheet. Read `_ds_manifest.json` for tokens, `guidelines/` for rendered rules, and `ui_kits/` for the search, detail, handover and marketing screens not yet built. Where the corpus and `app/` differ, `app/` is the live build; where either differs from the sheet, the sheet wins.

The corpus is read-only to a design session. `/impeccable extract` consolidates into `app/_components/` and `app/globals.css`, never under `docs/design-system/`; the corpus changes only when it is reconciled to a sheet bump. Never run `/impeccable document` over this file: decline its refresh, overwrite and merge offers (#3466).
