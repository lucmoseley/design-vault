# How design sources divide web and interface design into topics, and how to show a topic list is complete (#207, map #202)

⚠ **Bound 15 Oct 2026 (#210): B2's method is adopted, with five source families plus current practitioner writing, an area stop at 90% of Chao2, and one held-out source coded blind as a fourth check. The ledger build is #215.**

Status: complete (15 Oct 2026).

Question: How do authoritative design sources divide web and interface design into topics? Which method gives confidence that a coverage list made from them is complete?

Source strength labels (same as #104):
- **Primary**: the standard, spec or first-party owner of the claim (W3C, a design system's own site, a book's own table of contents, a methods paper's own text).
- **Strong secondary**: an established expert reference, or a peer-reviewed paper about a method.
- **Weak**: blog, vendor marketing, opinion, search-result snippet only.

Label key: **T** = timeless. **E** = era-bound (the guidance changes with platforms or fashion; current practice 2023 on).

Granularity key (the level at which a source names a topic):
- **G1 subject**: a whole field ("Typography", "Color").
- **G2 sub-subject**: a group of decisions ("Type scale", "Elevation").
- **G3 single decision**: one choice a designer makes on one property ("tracking of headings", "border or ring", "how many typefaces").

## Part A. Topic trees from authoritative sources

### A1. Apple Human Interface Guidelines (primary; read through the page JSON, 15 Oct 2026)

Source: `developer.apple.com/tutorials/data/design/human-interface-guidelines{,/foundations,/typography,/color,/materials,/components}.json` (the data behind the HIG pages).

- **Top level (G1):** Getting started; Foundations; Patterns; Components; Inputs; Technologies.
- **Foundations (G1–G2):** Accessibility; App icons; Branding; Color; Dark Mode; Icons; Images; Immersive experiences; Inclusion; Layout; Materials; Motion; Privacy; Right to left; SF Symbols; Spatial layout; Typography; Writing.
- **Components (G1 groups):** Content; Layout and organization; Menus and actions; Navigation and search; Presentation; Selection and input; Status; System experiences.
- **Typography page (to G3).** Each guideline is one bold sentence. The sentence is the decision:
  - Ensuring legibility: font sizes most people can read (a table of default and minimum size per platform); test legibility in context; "In general, avoid light font weights".
  - Conveying hierarchy: adjust weight, size and colour to show hierarchy; **"Minimize the number of typefaces you use, even in a highly customized interface"**; prioritise important content when text size changes.
  - Using system fonts: SF and NY families; **variable font format and optical sizing** ("Variable fonts support optical sizing"); built-in text styles; **"If necessary, adjust tracking in interface mockups"** (the system font adjusts tracking at every point size).
  - Specifications: a **tracking value table per point size**, per family (SF Pro, SF Pro Rounded, New York, SF Compact).
  - Custom fonts; Dynamic Type (layout at all text sizes, truncation, icon scaling).
- **Color page (to G3):** best practices (one colour, one meaning; light, dark and increased-contrast contexts; artwork and translucency affect nearby colours); inclusive colour; system colours (do not hard-code, do not redefine semantic meanings); Liquid Glass colour; colour management (wide colour, profiles). Specifications: system colours and **a scale of six system grays**. No warm or cool grey choice.
- **Materials page (to G3):** Liquid Glass (not in the content layer; sparingly; clear glass only over rich backgrounds); standard materials (choose by meaning; vibrant colours for legibility on materials). **Separators have one vibrancy level.**
- **Borders and dividers.** The HIG has no guidance page or bold guideline on borders, rings or dividers. The decision shows only as API colour tokens linked from the Color page: `separator`, "the color for thin borders or divider lines that allows some underlying content to be visible", and `opaqueSeparator`, "that hides any underlying content". Thus the HIG names *translucent against opaque divider lines* (border opacity) as a token, not as a guideline.
- **Granularity:** G3 for typography, colour and materials (every bold sentence is one decision). Stops at G2 or below for surfaces (no border, ring or divider guidance).
- **Era:** Liquid Glass (2025) and visionOS are E. Legibility, number of typefaces and hierarchy are T. Tracking-by-size tables are T in principle (optical tracking) but specific to Apple's fonts.

### A2. IBM Carbon (primary; carbondesignsystem.com, 15 Oct 2026)

Source: `carbondesignsystem.com/elements/typography/overview/` (fetched through the summarising fetch tool; the page text was not read raw, so the G3 lists below are as the tool reported them).

- **Foundations (G1):** 2x Grid; Accessibility; Carbon for AI; Color; Content; Icons; Pictograms; Motion; Spacing; Themes; Typography.
- **Components (G2, 42):** Accordion … Tile, Toggle, Tooltip, Tree view, UI shell. **Patterns (G2, 18):** common actions, dialogs, disabled states, disclosures, empty states, filtering, fluid styles, forms, global header, loading, login, notifications, overflow content, read-only states, search, status indicators, text toolbar. **Data visualisation** has its own tree (chart types, anatomy, axes, colour palettes, legends, dashboards).
- **Typography page (to G2, partly G3):** type tokens and sets (productive vs expressive; fixed vs fluid headings); typeface IBM Plex (sans, serif, mono stacks); scale (one formula, 12–92 px); style (weights 300/400/600; italic for named uses); type colour (neutral text, blue links, coloured type only for code and alerts).
- **Not named on the typography page (as the tool reported):** tracking, line-height values, case, line length, variable fonts.
- **Granularity:** G2 mostly. It names a decision (weights, italic use, type colour) where IBM has made the choice for the user; it does not name the open decisions a web designer faces.
- **Era:** productive/expressive split and Plex are house choices (E for IBM); weight/size trade-off is T.

### A3. Material Design 3 (primary for the tree; strong secondary for G3 content)

Source: `m3.material.io/sitemap.xml` (lastmod July 2026) gives the full tree. The pages render by script, so the page text was not read. G3 content comes from the Android Wear "Fonts" page (`developer.android.com/design/ui/wear/guides/styles/typography/fonts`, M3 Expressive, read through the fetch tool) and search snippets.

- **Styles (G2):** Color (roles; choosing a scheme; dynamic colour from content or user source; static baseline and custom brand; advanced: adjust, apply, define); Elevation (overview, applying, tokens); Icons (applying, designing); Motion (easing and duration; transitions; specs); **Shape** (corner radius scale; principles; shape morph); Spacing (applying, tokens); **Typography** (overview; fonts; type scale tokens; applying type; **editorial treatments**).
- **Foundations (G2):** accessibility (building for all; colour contrast; elements, flow, structure); content design (alt text; global writing; notifications; style guide); design tokens; interaction (gestures, inputs, selection; **states and state layers**); layout (breakpoints compact to extra-large; canonical layouts feed / list-detail / supporting pane; grids and spacing; **density**; scaffold of bars, panes, rails; adaptive design); usability; writing (text resizing, **text truncation**).
- **Components (G2, 37):** app bars, badges, bottom sheets, button groups, buttons, cards, carousel, checkbox, chips, date pickers, dialogs, **divider**, FABs, icon buttons, lists, loading indicator, menus, navigation bar/drawer/rail, progress indicators, radio, search, segmented buttons, side sheets, sliders, snackbar, split button, switch, tabs, text fields, time pickers, toolbars, tooltips.
- **G3 seen:** the M3 Expressive scale uses **Roboto Flex as a variable font**; the two axes "most applicable for product design" are weight and width; "Be careful of using too light a weight type for body text"; "Use lighter weights at larger font sizes, such as display type"; a narrow width "allows more characters to fit per line". Each type-scale token carries font, size, line height, weight and **tracking** (tracking per role; values not read at source, snippet only).
- **Granularity:** the tree stops at G2; its token tables and component pages reach G3 (from memory, not read here: a divider component with inset and full-width variants; a state-layer opacity per state). M3 has a **Divider component page** and a **shape (corner) scale page**.
- **Era:** M3 Expressive (May 2025), dynamic colour and shape morph are E. Hierarchy and legibility are T.

### A4. Atlassian Design System (primary; atlassian.design, 15 Oct 2026, through the fetch tool)

- **Foundations (G2):** Tokens; Accessibility; Content; Spacing; Grid; Color; Typography; Motion; Iconography; Illustrations; Logos; **Elevation**; **Border**; **Radius**.
- **Border page (G3):** default width 1px "for all standard component borders and dividers"; selected 2px; **focus ring 2px**, always paired with `color.border.focused`; pair width token with colour token; an accent border on a subtle accent background to meet 3:1. Opacity and the choice border-vs-other-separation are not on the page.
- **Elevation page (G3, the deepest surface source found):** four levels (sunken, default, raised, overlay) plus overflow; "Don't apply sunken elevations on raised or overlay"; on raised or overlay use **"whitespace or borders instead"**; a flat card pairs with a border; raised only for movable cards, "limit to one focal point per screen", "Don't use [raised] to group content when a border or whitespace would work"; dark mode: higher surfaces are lighter; scrolled state shows **a border at the cut-off point**; "Avoid excessive use of raised and overlay elevations … they can make the UI busy"; z-index table.
- **Typography page (G3 for sizes and weights):** brand font vs app fonts (Atlassian Sans + Mono; Charlie Sans for brand only — a **how-many-fonts by role** decision); heading tokens with sizes and line heights; "Only use one h1 per page"; body weights Regular / Medium (beside line icons) / Bold "sparingly"; paragraph spacing per size. Not named: tracking, case, alignment, line length, italics, variable fonts.
- **Granularity:** G3 for surfaces and type sizes. Atlassian is the only design system found with separate Border, Radius and Elevation foundations that say when to use a border, whitespace or a shadow.
- **Era:** token values E ("subject to change"); the separation logic (border vs whitespace vs elevation) is T.

### A5. USWDS (primary; designsystem.digital.gov, through the fetch tool)

- **Design tokens (G2):** Color; **Typesetting** (font family, font size, font weight, **letterspacing**, line height, **measure (line length)**, normalisation); Flex; **Opacity**; Order; **Shadow**; Spacing units; Z-index. **Utilities:** border, **outline**, shadow, text styles, paragraph styles, and others.
- **G3 seen:** typefaces are **normalised** to one optical size so swapping a face keeps the same apparent size; six target line heights; letterspacing tokens −0.03em to 0.15em. The letterspacing page gives values but **no rule for when** to track headings, capitals or small text.
- **Granularity:** G3 as a token list (a named property with values), G2 as guidance. It names tracking and opacity as decisions but does not rule them.
- **Era:** T for measure and normalisation; token values E.

### A6. GOV.UK Design System (primary; design-system.service.gov.uk, through the fetch tool)

- **Styles (G2):** page template; layout; spacing; **section break**; typeface; type scale; headings; paragraphs; links; lists; font override classes; colour; images. Plus Components and Patterns (not listed here).
- **G3 seen:** **section break**: an `<hr>` that is invisible by default (space only) with a `--visible` modifier for a line, in sizes m / l / xl — this is the divider decision (line or space) as a named style; lead paragraph 24px "only use it once per page"; body 19px, small 16px "sparingly"; GDS Transport only on service.gov.uk.
- **Granularity:** G3 for a few decisions, but narrow: GOV.UK states only what its own house does. It does not discuss tracking, case, italics or alignment on the style pages.
- **Era:** T (plain, accessible service pages). The v6 type scale (larger text on small screens) is E.

### A7. GitHub Primer and Shopify Polaris (primary; trees only)

- **Primer (primer.style, through the fetch tool):** Foundations: colour usage, content, icons, layout, responsive, typography. Primitives: colour, size, typography, token names. UI patterns (10) and scenario patterns (9). 60+ components. CSS utilities include **Borders** and **Box shadow**. Page bodies not read. G2.
- **Polaris:** `polaris.shopify.com/design` now redirects (301) to `shopify.dev/docs/api/polaris`, which lists only component references for app surfaces. The design foundations Polaris once published are not online at that address. Not used.

### A8. Refactoring UI (Wathan and Schoger, 2018) (strong secondary; TOC read from `refactoringui.com/book`)

- **Chapters (G1):** Starting from scratch; Hierarchy is everything; Layout and spacing; Designing text; Working with color; Creating depth; Working with images; Finishing touches; Leveling up.
- **Sections (G3; 50 of them, each one decision stated as an imperative).** The ones on type and surfaces:
  - Designing text: establish a type scale; use good fonts; **keep your line length in check**; baseline, not center; line-height is proportional; not every link needs a color; **align with readability in mind**; **use letter-spacing effectively**.
  - Working with color: ditch hex for HSL; you need more colors than you think; define your shades up front; don't let lightness kill your saturation; **greys don't have to be grey**; accessible doesn't have to mean ugly; don't rely on color alone.
  - Creating depth: emulate a light source; shadows convey elevation; shadows can have two parts; even flat designs can have depth; overlap elements to create layers.
  - Finishing touches: supercharge the defaults; **add color with accent borders**; decorate your backgrounds; don't overlook empty states; **use fewer borders**; think outside the box.
  - Hierarchy: not all elements are equal; size isn't everything; don't use grey text on colored backgrounds; de-emphasize to emphasize; labels are a last resort; separate visual from document hierarchy; balance weight and contrast; **semantics are secondary**.
  - Starting from scratch: **choose a personality**; **limit your choices**.
- **Granularity:** G3 throughout. The TOC alone names a single decision per line. This is the closest outside source to "one decision a designer makes".
- **Era:** mostly T. "Ditch hex for HSL" is E (OKLCH is current practice; HSL is not perceptually uniform). Some taste (accent borders, decorated backgrounds) is E: craft-floor in impeccable now refuses a coloured side border above 1px.

### A9. Butterick's Practical Typography, 2nd edition (strong secondary; TOC and four pages read at `practicaltypography.com`)

- **Parts (G1):** Why typography matters; Type composition; Text formatting; Font recommendations; Page layout; Sample documents; Appendix; Commentary.
- **Pages (G3; one page per decision):**
  - Text formatting: underlining; goofy fonts; monospaced fonts; bold or italic; **all caps**; point size; headings; **letterspacing**; kerning; **color**; alternate figures; small caps; hierarchical headings; OpenType features; **mixing fonts**; metrics vs optical spacing.
  - Page layout: **centered text**; justified text; first-line indents; space between paragraphs; line spacing; **line length**; page margins; body text; hyphenation; block quotations; lists; tables; **rules & borders**; **widow and orphan control**; space above and below; columns; grids; maxims of page layout.
  - Appendix: screen-reading considerations; responsive web design. Commentary: **"The scorpion express: thoughts on variable fonts"**.
- **Key rules (summary page), the type-and-surface ones:** body 15–25 px on the web; line spacing 120–145%; line length 45–90 characters; bold or italic "as little as possible", never together; all caps fine "for less than one line"; centred text sparingly; **add 5–12% letterspacing to all caps and small caps**; indent or paragraph space, not both.
- **Pages read in full through the fetch tool:**
  - *Mixing fonts:* mixing is "never a requirement"; "most documents can handle a second font, few can handle a third, and almost none can handle four or more"; give each font a consistent role; one font per paragraph.
  - *Letterspacing:* caps and small caps take 0.05–0.12em; lowercase normally takes none; **typographers often remove letterspacing from lowercase at large sizes such as headlines**; add some below 9 pt.
  - *Rules & borders:* use sparingly; **try extra space above and below first**; ½–1 pt thickness; no dotted, dashed or double borders; a rule with a heading goes above it.
- **Granularity:** G3. Print-first, with web notes.
- **Era:** T (rules of type). Point sizes for print are not web values; the web range (15–25 px) is given.

### A10. Bringhurst, The Elements of Typographic Style (strong secondary; rules §2–3 read from Rutter's web edition `webtypography.net/toc`; later chapters from memory, not verified)

- **Structure:** each chapter holds numbered rules, and **every rule is one decision in one sentence** (G3). Verified rules (web edition): 2.1.2 choose a comfortable measure; 2.1.3 set ragged if ragged setting suits the text; **2.1.6 letterspace all strings of capitals and small caps**; **2.1.7 don't letterspace the lower case without a reason**; 2.1.8 kern consistently and modestly; 2.1.9 don't alter the widths or shapes of letters without cause; 2.2.1 choose a basic leading that suits the typeface, text and measure; 2.2.2 add and delete vertical space in measured intervals; 2.3 paragraphs; 2.4 hyphenation and pagination (2.4.8 never begin a page with the last line of a multi-line paragraph — a widow rule); 3.1.1 don't compose without a scale; 3.2.1 titling figures with full caps.
- **Not verified (memory):** chapter 6 "Choosing & Combining Type", whose rules include combining faces sparingly; chapter 3 sections on italic and bold.
- **Granularity:** G3. Print-first; the web edition is a partial port (chapters 2–3 only).
- **Era:** T.

### A11. Other books (chapter level only)

- **Lupton, Thinking with Type, 3rd ed. (2024)** (weak: retailer and library listings only; `thinkingwithtype.com` did not answer): three parts, Letter, Text, Grid. The 3rd edition adds "**variable fonts and optical sizes**" and responsive layout. Section names (tracking, line spacing, alignment, hierarchy, mixing typefaces, capitals and small capitals) are from memory and not verified.
- **Tidwell et al., Designing Interfaces, 3rd ed. (2020)** (weak: library record): chapters 1–5 confirmed (designing for people; organising content; getting around; layout of screen elements; **visual style and aesthetics**). Its visual-style patterns in the 2nd edition (from memory, not verified) included "few hues, many values", "corner treatments", "borders that echo fonts", **"hairlines"** and "contrasting font weights".
- **Lidwell, Holden and Butler, Universal Principles of Design (2010)** (weak: library record): 125 principles in alphabetical order. Each principle is G2 (for example legibility, readability, signal-to-noise ratio, figure-ground, common region). They are mechanisms, not single property decisions. Entry list not read.
- **Müller-Brockmann, Grid Systems in Graphic Design (1981):** not opened. Its subject is the grid (type area, columns, leading and type size against the grid); it is a G2 source for layout, not for surfaces.

### A12. Curricula (primary for their own outlines; all stop at G1–G2)

- **NN/g** (`nngroup.com/ux-certification/`, `/courses/`, `/courses/visual-design/`): certification specialties are AI, Interaction, Research and Management; 55 live courses, **one** visual-design course ("Visual Design Fundamentals"). Its outline: visual hierarchy and layout; grid systems; **choosing a typeface; line width and height for white space; mixing and matching typefaces; typography accessibility**; imagery (illustration, icons, photography); a design system and palette (consistency, brand, choosing colours, colour for interaction, colour accessibility). G2. No tracking, case, borders, dividers or greys.
- **Interaction Design Foundation** (`ixdf.org/courses`, `/courses/visual-design-the-ultimate-guide`): visual courses are Visual Design, Visual Perception, Gestalt and Web Design, UI Design Patterns, Mobile UI, Object-Oriented UI. "Visual Design: The Ultimate Guide" lessons: visual principles; **colour theory** (modes, systems, why colours change, symbolism); **typography** (anatomy, "how to talk type", type grids, "how to design with type"); grid systems. G2. A separate master class is titled "Own Your Typographic Decisions in UI Design" (not opened).
- **University syllabus — MIT 6.4500 Design for the Web** (`designftw.csail.mit.edu/schedule`): 26 lectures, of which the visual ones are graphic design, layout, **typography**, **colour**, animation and feedback, universal web design. Lecture titles only. G1.
- **Judgement:** curricula teach subjects (G1–G2). They are good for checking that no *subject* is missing. They are useless for finding *decisions*: none named tracking, case, borders, dividers or grey temperature.

### A13. Checklists

- **WCAG 2.2** (primary; `w3.org/TR/WCAG22/`, read through the fetch tool). Success criteria are G3 testable statements. Type and surface criteria: 1.4.3 contrast; 1.4.4 resize text; 1.4.8 visual presentation (AAA: **width no more than 80 characters**, not justified, line spacing, paragraph spacing, user-selectable colours); 1.4.10 reflow; **1.4.11 non-text contrast** (3:1 for component boundaries — this binds a border that is the only boundary of a control, and so limits border opacity); **1.4.12 text spacing** (no loss at line height 1.5, paragraph spacing 2×, **letter spacing 0.12em**, word spacing 0.16em); 2.4.7 focus visible; 2.4.11 focus not obscured; **2.4.13 focus appearance** (AAA: an indicator area at least a 2 CSS px perimeter, 3:1 between states — this is the ring decision). WCAG names *limits*, not *design choices*: it bounds N1, N5, N11 and N14 but does not ask the design question. T for the principles, E for the version (2.2 is October 2023).
- **impeccable 4.5.0** (primary for itself; read `reference/typeset.md`, `reference/craft-floor.md` in full; detector rule list from `docs/research/impeccable-checks.md` F5).
  - Commands (G1): typeset, colorize, layout, animate, adapt, clarify, harden, polish, bolder, quieter, distill, delight, overdrive, optimize, audit, critique, and others.
  - `typeset` (G2–G3): faces and roles ("Is every family necessary?" — **how many fonts**); hierarchy steps; role scale; reading (45–75ch measure; line height, contrast and **tracking tuned to the face**); stress (long headings, localisation, zoom, fallback); delivery (**"variable-font settings"**, fallback metrics); light text on dark needs more line height, tracking and weight; tabular and label features; paragraph spacing or indent, not both; "do not … introduce a second family without a clear role".
  - `craft-floor` (G3): body measure 65–75ch; display max 6rem; **tracking floor −0.04em**; **"balanced headings"**; shadows need offset and blur; tint secondary text on coloured surfaces, "never gray"; **focus rings themed**; underline offset; nested cards wrong; coloured side border above 1px refused; hairline border plus wide diffuse shadow flagged.
  - Detector (G3, about 61 rules): crushed letter spacing; wide tracking on body text; **all-caps body text**; line length over ~80 characters; line height under 1.3; justified text; body under 12 px; flat type hierarchy; overused fonts; gray text on a coloured background; side-tab accent border; thick accent border on a rounded card; nested cards; cream page background; glowing shadows.
  - Granularity: G3, but **as defaults and refusals, not as a list of open decisions**.
  - Era: E (it targets the 2024–2026 "AI look"); the type rules inside it are T.

### A14. Granularity: which sources reach a single decision

| Source | Deepest level it names | Where it reaches G3 | Strength |
|---|---|---|---|
| Refactoring UI | **G3 in the TOC itself** | every section title | strong secondary |
| Butterick | **G3, one page per decision** | text formatting, page layout | strong secondary |
| Bringhurst | **G3, one numbered rule per decision** | every rule | strong secondary |
| Apple HIG | **G3, one bold sentence per decision** | typography, colour, materials; not borders | primary |
| Atlassian | **G3** for surfaces and type sizes | border, elevation, typography | primary |
| impeccable | G3 as defaults and refusals | typeset, craft floor, detector | primary for itself |
| WCAG 2.2 | G3 as testable limits | 1.4.x, 2.4.x | primary |
| USWDS | G3 as token names, G2 as guidance | typesetting tokens | primary |
| GOV.UK | G3, few and house-specific | section break, paragraphs | primary |
| Material 3 | G2 tree; G3 inside token tables and component pages | divider, type scale tokens | primary (tree) |
| Carbon, Primer | G2 | — | primary |
| Curricula (NN/g, IxDF, MIT) | G1–G2 | — | primary for own outline |
| Lupton, Tidwell, Lidwell, Müller-Brockmann | G1–G2 as read here | not verified | weak (listings) |


## Part B. How to show a topic list is complete

### B1. Methods other fields use

1. **Merge the trees (union, then deduplicate).** Each source's G3 items become rows. Two items merge when they name the same property in the same context (for example "letterspacing of capitals" in Butterick and Bringhurst 2.1.6). This is an inventory, not a test of completeness. Cost: the reading, plus one normalisation pass.
2. **Saturation (qualitative research).** Guest, Namey and Chen (2020), *PLOS ONE* 15(5): e0232076 (primary, PMC full text read through the fetch tool): take a **base size** (default four interviews), then count new themes in each **run** of two or three further interviews, as a share of the base count. Stop when the share is at or below a **new-information threshold** of ≤5% or 0%. The authors state a limit: "it is possible an important theme will emerge later … The honest answer to this is that we don't know". They reorder the interviews at random (bootstrap) to test order effects. Cost: low — a count per added source. Weakness: it says when *this order* of sources stops adding, not how many topics no source names.
3. **Capture–recapture / species-richness estimators.** Chao and Colwell (2017), "Thirty years of progeny from Chao's inequality", *SORT* 41(1) (primary, PDF read): with T independent sampling units, Q1 = items found in exactly one unit, Q2 = in exactly two, the estimated **lower bound** of the true count is **Chao2 = S_obs + ((T−1)/T) · Q1² / (2·Q2)** (if Q2 = 0: S_obs + ((T−1)/T) · Q1(Q1−1)/2). It is exact only if all items are equally likely to be found; it stays a valid *lower bound* under heterogeneity. The sampling units must be "sampled randomly and independently". Medicine uses the two-source form to estimate missed studies: Kastner et al. 2009, *J Clin Epidemiol* 62(2):149–157 (abstract level, via search) found their four databases had about 68–81% of the estimated studies. A test by Motschall et al. (Cochrane Colloquium 2009, abstract) got 56 missed articles from one model and an implausible 1,439 from another, and called the use "questionable". Cost: low once the incidence table exists (one formula). Weakness: design sources are **not independent** (design systems copy each other and the craft books), so the estimate is a floor, possibly a low one.
4. **Systematic-review search practice.** Cochrane Handbook ch. 4 (primary, read through the fetch tool): search two or more databases ("A search of MEDLINE alone is not considered adequate", 4.2.2); add citation searching (4.3.5, 4.4.2). §4.4.11 "When to stop searching": check the strategy **finds known key publications**, but "it is not enough … for the strategy to find only those records"; **relative recall** (each search scored against the pooled set; Sampson et al. 2006, *BMC Med Res Methodol* 6:33, abstract via search); **capture–recapture** ("needs results from at least two searches"); stop when new terms yield **no new relevant records**. Cost: medium. Strength: it combines several checks and uses a **known-item test set**.
5. **Card sorting** (NN/g, `nngroup.com/articles/card-sorting-definition/`, primary): reveals how people *group* known items; open sort makes the groups, closed sort tests them; 15+ participants for qualitative work. It is "a method for grouping known items", **not for finding missing ones**. Useful later, to group the merged list into areas a skill loads; no use for completeness.

### B2. Recommendation: a systematic-review-style search with three stopping checks

Use method 4 as the frame, with methods 2 and 3 as its stopping checks and the founder's notes as the known-item test set:

1. **Frame (sources).** Choose sources in three independent families, so that the capture–recapture assumption is less wrong: (a) craft books at G3 (Refactoring UI, Butterick, Bringhurst; add one current web book); (b) design systems with G3 guidance (HIG, Atlassian, M3 component and token pages, GOV.UK, USWDS); (c) checklists and limits (WCAG 2.2, impeccable's rule list, Baymard for its areas). Curricula only as a G1 cross-check that no subject is missing.
2. **Extract at G3.** One row per *decision*: property × element × context (for example "letter-spacing × heading × large size"). Record which sources name it (an incidence table, one column per source).
3. **Stop check 1, saturation.** After a base of four sources, add sources in runs of two; stop when a run adds ≤5% new rows (Guest et al.). Randomise order once to see that the stop is not an artefact of order.
4. **Stop check 2, Chao2 per area.** Compute Chao2 per area (typography, surfaces, colour, layout …). If S_obs is below about 80–90% of Chao2, the area is not saturated: add a source from a family not yet used. Report Chao2 as a floor.
5. **Stop check 3, known-item recall.** Hold the founder's notes (N1–N19) and any later founder lead out of the search. After the search, score how many the list found. A miss means the frame lacks a source family (as #104's frame lacked G3 sources). Per Cochrane, finding them is necessary, not enough.

**Cost (estimate, from this ticket's own run):** reading one G3 source for two areas and coding its rows took about 15–25 minutes of agent work here (fetch tool, about 10–30k tokens per source). The full method, at about 12–15 sources × 8–10 areas, is about 120–150 source-area readings: **about 2–4 sessions of agent work (roughly 1.5–3M tokens), plus about 30 minutes of founder time** only for gaps the search leaves open (a taste or business fact). Books that are not online (Refactoring UI body text, Bringhurst, Lupton) cost more: their TOCs are online, their content is not, so G3 rows from them rest on the TOC line alone unless someone reads the book.

**Why not the others alone.** Saturation alone stops early when the first sources share a family (the design systems repeat each other: N9 grey temperature appears on none of the design-system pages read here, and only in Refactoring UI).

## Part C. Small test: four sources, typography and surfaces only

### C1. Set-up

- **Sources (T = 4, chosen from three families):** R = Refactoring UI (TOC, A8); B = Butterick (TOC, key rules and four pages, A9); H = Apple HIG (typography, colour, materials, A1); A = Atlassian (typography, border, elevation, A4). impeccable was left out because it is the house's incumbent, and the test asks what *outside* sources find.
- **Coding:** one row per G3 decision named in the source's own text as recorded in Part A. Two sources share a row when they name the same property for the same element. The incidence table and script are at `/tmp/r207s/incidence.py` (not in the repo); its rows are below.
- **Bias warning:** the coder (this agent) had read the founder's notes before coding. The rows come from the sources' own headings and sentences, written in Part A before the match, but a blind coder would be cleaner. In the full run, a session that has not seen the notes must code the rows.

### C2. The union (55 rows)

Typography (32): body size; type scale for roles; typeface choice; **how many typefaces and the role of each**; **line length**; line height; letter-spacing in general; **letter-spacing of capitals**; **letter-spacing of large or heading text**; **when to set all caps**; bold and italic; weight for hierarchy; avoid light weights; **alignment**; **text colour and grey text**; link styling; baseline alignment; paragraph spacing or indent; hyphenation; **short word alone on the last line** (Butterick: browsers "are happy to put a small word alone on the last line", which "always looks bad"); kerning; alternate figures; OpenType features; small caps; monospace; **variable fonts and optical sizing**; user text scaling; truncation; heading levels; visual vs document hierarchy; typeface personality; space above and below headings.

Surfaces (23): shadow for elevation; light source and two-part shadows; elevation levels; depth without shadow; overlapping layers; **border, or space / shadow / background instead**; border thickness; border style; accent borders; **dividers and separators**; **border or separator opacity**; **focus ring**; selected-state border; decorated backgrounds; surface colour levels; **grey temperature**; grey and shade scale; materials (translucency, blur); light, dark and high-contrast surfaces; scroll-edge border or shadow; too many raised surfaces make the UI busy; z-index; 3:1 contrast for borders.

### C3. Does the union surface the founder's topics without being told?

| Note | Found? | Rows and sources | Level |
|---|---|---|---|
| **N1** text readability details | **Yes, partly** (7 of 8 parts) | size (BHA), weight (RH, BA), measure (RB), line height (RBA), letter-spacing (RBH), text colour (RBH), alignment (RB), last-line short word (B). **Missed:** `text-wrap: balance` for headings and opacity as a separate means of text colour. The *problem* of a lone last word is found; the *2023–24 CSS fix* (`text-wrap: pretty`, `balance`) is not. | G3 |
| **N4** variable fonts | **Yes** | HIG: "Variable fonts support optical sizing"; Butterick commentary on variable fonts. (M3 Expressive, outside the four, also: Roboto Flex weight and width axes.) | G3 |
| **N5** outer rings vs borders | **Partly** | Atlassian names the **focus ring** as a 2px border width paired with a focus colour; WCAG 2.4.13 limits it. No source of the four names *ring or border* as a styling choice for a button at rest. | G3 for focus only |
| **N6** dividers | **Yes** | Butterick rules & borders ("try [more space] first"; rule above a heading); Atlassian ("whitespace or borders instead"; 1px "for all standard component borders and dividers"); HIG separators; Refactoring UI "Use fewer borders". GOV.UK and M3 outside the four also have it. | G3 |
| **N9** cool, neutral, warm greys | **Yes, singleton** | Refactoring UI only: "Greys don't have to be grey". HIG gives a grey scale but no temperature. | G3 |
| **N10** how many fonts | **Yes** | Butterick (second font fine, third rare, four almost never; a consistent role per font); HIG ("Minimize the number of typefaces"); Atlassian (brand font vs app font). Not "by site size and function". | G3 |
| **N11** border opacity | **Partly, singleton** | HIG only, and only as colour tokens: `separator` "allows some underlying content to be visible" vs `opaqueSeparator`. No source gives guidance on *when* or *how much*. | token level |
| **N14** heading tracking | **Yes** | Butterick: remove letterspacing from large lowercase "such as headlines"; HIG: tracking table by point size; Refactoring UI "Use letter-spacing effectively" (TOC line). | G3 |
| **N16** uppercase vs lowercase | **Yes, singleton** | Butterick "all caps" page and rule ("fine for less than one line"; add 5–12% letterspacing). | G3 |

**Hit rate:** 6 of 9 found in full (N4, N6, N9, N10, N14, N16); 3 of 9 in part (N1, N5, N11); **0 of 9 missed outright**.

### C4. What the estimators say about this small union

From the script (T = 4 sources):

| Area | Rows found (S_obs) | Found by one source (Q1) | By two (Q2) | Chao2 lower bound | S_obs ÷ Chao2 |
|---|---|---|---|---|---|
| Typography | 32 | 13 | 12 | 37.3 | 86% |
| Surfaces | 23 | 15 | 6 | 37.1 | **62%** |
| Both | 55 | 28 | 18 | 71.3 | 77% |

- **Saturation not reached.** Over all 24 source orders, the fourth source still adds 4–10 new rows (7–18% of 55). Guest et al.'s ≤5% rule says: keep adding sources.
- **Surfaces are the thin area.** Chao2 says at least about 14 surface decisions remain unnamed by these four sources. This agrees with the founder's notes: three of the four surface notes (N5, N9, N11) were found by one source at most.
- **The founder's topics sit in the rare tail.** Of the nine, four rows are singletons (N9, N11, N16, the focus ring for N5) and two are doubletons (N4, N14).
- **Caveat.** The four sources are not independent (Atlassian and HIG share the design-system genre; Butterick and Refactoring UI share craft-book habits), and rows differ in how easy they are to find. Chao2 is therefore a floor. The surfaces figure (62%) is the useful signal, not the exact number.

### C5. Era labels for the topics found

- **Timeless (T):** measure, line height, letter-spacing of capitals and of large text, all caps, how many typefaces, alignment, dividers vs space, grey temperature, border thickness, elevation by light.
- **Era-bound (E):** `text-wrap: balance/pretty` (MDN: the `text-wrap` property is Baseline widely available since March 2024, "some parts … varying levels of support"; `balance` is limited to short blocks, six lines in Chromium and ten in Firefox; `pretty` uses a slower algorithm for body copy "when the number of orphans should be kept to a minimum"); variable fonts in UI (system fonts went variable around 2020; M3 Expressive Roboto Flex 2025); Liquid Glass and materials (2025); OKLCH over HSL; WCAG 2.2 (October 2023) as the limit set; focus-ring styling under 2.4.13.
- **The test's lesson on era:** the timeless notes were all found by the craft books; the era-bound part of N1 (`text-wrap`) was found by none of the four. The full run therefore needs one **current web-platform source** (for example web.dev or MDN's CSS typography guides, or a 2023-on web typography book) as its own family.

## Answer

1. **How sources divide the field.** Design systems divide it into foundations (type, colour, layout and spacing, elevation or materials, shape or radius, border, motion, icons, content, accessibility) and components. Craft books divide it into subjects and then into decisions. Curricula divide it into subjects only. **Only the craft books (Refactoring UI, Butterick, Bringhurst) and the bold-sentence design systems (Apple HIG, Atlassian's border and elevation pages) name single decisions** such as "letter-spacing of capitals", "greys don't have to be grey", "minimize the number of typefaces" or "whitespace or borders instead". #104 drew its ~20 areas at the curricula's level (G1), so it could not see decision-level gaps.
2. **The method to use.** A systematic-review-style search: sources from at least three independent families (craft books, design systems with G3 guidance, checklists and current web-platform docs); extraction at one row per decision with an incidence column per source; three stopping checks — saturation (≤5% new rows per run of two sources, Guest et al. 2020), a Chao2 lower bound per area (stop when found rows reach about 80–90% of it), and recall of a held-out known-item set (the founder's notes), as Cochrane §4.4.11 does with known studies. Card sorting comes after, to group the list for loading, not to find gaps.
3. **Its cost.** About 2–4 agent sessions (roughly 1.5–3M tokens) for 12–15 sources over 8–10 areas, and about 30 minutes of the founder's time for the gaps the search cannot settle. Books not online are the costly part: their TOCs give the decision names, but not their content.
4. **The small test.** Four sources, two areas, 55 decision rows. It surfaced 6 of the 9 founder topics in full and 3 in part, and missed none outright. The parts it missed are the ring-vs-border choice at rest (N5), *when and how much* border opacity (N11, a token in HIG only) and the 2023–24 CSS wrap controls (N1). Chao2 marks surfaces as the unsaturated area (62% of the lower bound found), which is where the founder's partial hits sit.

## Bound

**Read in full (raw text or JSON):** Apple HIG typography, colour, materials, foundations and components JSON (headings and bold guideline sentences; the separator token abstracts); `webtypography.net/toc`; Chao and Colwell 2017 (*SORT* 41(1)), §2.1–2.2 including the Chao2 formula (extracted from the PDF); impeccable 4.5.0 `reference/typeset.md` and `reference/craft-floor.md`; this repo's `docs/research/design-coverage-gaps.md` (Coverage frame, header, Bound) and `docs/research/impeccable-checks.md` F5; issues #207 and #202.

**Read through the summarising fetch tool (page text, not raw; a small model reported it):** Carbon typography; Atlassian foundations, border, typography, elevation; USWDS design tokens, typesetting, letterspacing; GOV.UK styles, section break, typeface, paragraphs; Primer foundations nav; Android Wear (M3 Expressive) fonts; Refactoring UI TOC; Butterick TOC, summary of key rules, mixing fonts, letterspacing, rules & borders, widow and orphan control; NN/g certification, course list, Visual Design Fundamentals outline, card-sorting article; IxDF course list and Visual Design course outline; MIT 6.4500 schedule; WCAG 2.2 (first 100k characters: 1.4 and 2.4 lists, 1.4.8, 1.4.11, 1.4.12, 2.4.13); Guest, Namey and Chen 2020 (PMC); Cochrane Handbook ch. 4 (§4.2–4.4.11); MDN `text-wrap`.

**Sampled:** Material 3 — the sitemap only (tree to G2); its pages render by script and were not read. M3 tracking tokens: search snippet only.

**Snippet level only (search results, not opened):** Kastner et al. 2009 and the later capture–recapture studies; Motschall et al. 2009; Sampson et al. 2006; Lupton 3rd ed. listings; Tidwell 3rd ed. chapter list; Lidwell catalogue record; the Chao2 bias-corrected form on MetricGate and Genstat (superseded by the Chao and Colwell PDF).

**Not opened:** Polaris foundations (the old address redirects to component references only); Atlassian radius page; Primer and Carbon page bodies beyond typography; M3 page bodies; Refactoring UI body text (the "letter-spacing" and "greys" sections are counted from their TOC lines only); Bringhurst chapters 3.3 on (italic, bold, combining type) and the print book; Lupton, Tidwell, Lidwell and Müller-Brockmann books and TOCs; IxDF master class "Own Your Typographic Decisions in UI Design"; university syllabi other than MIT 6.4500; Baymard; web.dev typography guides; this repo's `text-presentation.md` and `surface-styling.md` (#123, #117) — the test was against outside sources only, so it makes no claim on what the house already covers.
