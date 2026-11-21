# Rule records: system

Rules for the full site and the round: function codes, one look per function, the brand layer and the logo, tokens, AI-look defaults, load time and drafts kept. The form is [rules.md](../rules.md)'s.

### vault.drafts-kept
- applies-when: any; every earlier round of this brief, and the drafts of any engine this round edited
- question: Does every earlier round of this brief keep its tag, and does every kept draft whose engine this round edited render the same frames as when it was made?
- answered-by: script
- writes: drafts
- yields-to: level 2
- source: the rule is the founder's, lucmoseley/mmm-infra#9; keeping each round's tag is an agent's procedure, accepted on lucmoseley/mmm-infra#16, and the frame hashes an agent's recommendation, accepted on lucmoseley/mmm-infra#28; strength: founder ruling for the rule, accepted agent recommendations for the checks
- era: timeless
- owner: vault
- stage: value
- script: check-frames.py hash, and `git ls-remote --tags` for the tags
- reasons: design-round/SKILL.md#where-candidates-live
- ledger: none
- status: live

### vault.load
- applies-when: web-surface; the page's main content, on a phone's first load
- question: Does the page's main content, its largest text block or image on the first screen, show within 2.5 s of navigation on Lighthouse's throttled phone?
- answered-by: script
- writes: load
- yields-to: level 2
- source: web.dev, "Largest Contentful Paint (LCP)": 2.5 s or less is good; the throttled phone is Lighthouse's default mobile run (design-vault#170); split from vault.length by the founder's ruling on design-vault#169 Q3 (A); strength: domain evidence
- era: timeless
- owner: vault
- stage: value
- script: check-load.py
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: PAG-54
- status: live

### vault.borrowing
- applies-when: web-surface; every part, against every other part on the page
- question: Does each part show its function only by that function's own look, never one another kind of part keeps for itself (a static label shaped and filled like the button, a heading in the link colour, a fact in the filter chip's shape), with each distinct look meaning one function across the page?
- answered-by: look
- writes: look meaning
- yields-to: none
- source: GOV.UK Design System, Tag; Apple HIG, Color; NN/g, "Beyond Blue Links" (2015); WCAG 2.2 success criterion 3.2.4; the function walk's questions 4 and 5; strength: design-system guidance
- era: timeless
- owner: vault
- stage: function
- target: Give each function one look of its own across the page, and dress no part in another function's look.
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: BTN-63, BTN-64, BTN-65, BTN-66, BTN-67, BTN-68, COL-22, FCH-27, FCH-28, FRM-90, NAV-11, NEW2-39, OTH-9, TXL-7
- status: live

### vault.function-code
- applies-when: any; every part of the asset, decoration included
- question: Does every part carry one function code (N navigate, A act, I text input, S select or filter, T status, R read or R-trust proof, C contain, D decorate), given to the part rather than its whole component, and taken from the brief, the project's rules file or a project document, with a part none of them settles reported as `FIT RISK: function unknown` rather than guessed?
- answered-by: whole-page
- writes: function code
- yields-to: none
- source: WAI-ARIA 1.2 §5.3 role categories, Material 3 component categories, Apple HIG components; the split of I from S and of T from R-trust is #127 B7.1; strength: design-system guidance
- era: dated 2027-10-14
- owner: vault
- stage: function
- target: Give each part one function from the brief, the rules file or a project document, and draw it for that function, a part that navigates as a link (`<a href>`) and one that acts as a `<button>`, whatever it looks like; where none gives it, ask rather than pick.
- reasons: design-critique/references/house-principles.md#the-function-codes
- ledger: BTN-62, BTN-68, FCH-27, FCH-28, NAV-4, NAV-8, NAV-11, NAV-13, NAV-44, NAV-51, NAV-70, PAG-123
- status: live

### vault.decoration-place
- applies-when: web-surface; every piece of decoration, and every functional part beside it
- question: Does decoration stay out of the places a visitor works (where they read, fill in or choose), with no text inside illustration, and does no functional part take the look of decoration, an ad or a promotion?
- answered-by: whole-page
- writes: decoration placement
- yields-to: none
- source: NN/g 2018, banner blindness; Gaver, CHI '91, on false affordance; #127 B7.2's carrier table; strength: domain evidence
- era: timeless
- owner: vault
- stage: role
- target: Keep illustration and background art out of the regions where a visitor reads, fills in or chooses; keep live text out of illustration; style no control, price or proof like an ad.
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: COL-80, IMG-90, IMG-92, IMG-185, PAG-65, SUR-104, TYF-12
- status: live

### vault.brand-layer
- applies-when: any; every part, and above all a high-stakes moment: a price, availability, the handover to book, an error, sign-in
- question: Does the asset's distinctiveness sit in the brand layer (ground colour, illustration, display type, voice, motion character, one signature move) while every signifier, the interaction structure and the layout (the logo, navigation and search where visitors look for them) stay conventional, a dense list taking less novelty than a hero, a high-stakes moment moving nothing beyond type, colour role and voice, and any unusual control keeping its core signifier?
- answered-by: whole-page
- writes: brand expression
- yields-to: vault.high-stakes
- source: Norman 2002, on relaxed and stressed use; Google's M3 Expressive research (2025); Lavie and Tractinsky 2004, on classical against expressive beauty; Tuch, Presslaber, Stöcklin, Opwis and Bargas-Avila 2012 (IJHCS 70(11)), on prototypical layouts liked within 50 ms; the line is #127 B6.3's synthesis; strength: published research
- era: dated 2027-10-14
- owner: vault
- stage: role
- target: Spend novelty on the ground, illustration, display type, voice, motion character and one signature move; lay out the page and draw links, buttons, fields, selected states and status as convention does, plainest at a price, a booking, an error or sign-in.
- reasons: design-critique/references/house-principles.md#the-brand-layer-line
- ledger: COL-23, COL-79, COL-80, FRM-83, IMG-90, IMG-92, IMG-120, IMG-185, LAY-132, MOT-6, MOT-11, NAV-51, OTH-12, OTH-13, OTH-14, PAG-22, PAG-23, PAG-26, PAG-31, PAG-32, PAG-34, PAG-65, SUR-66, SUR-104, TYF-5, TYF-9, TYF-12, TYS-23
- status: live

### vault.logo-ground
- applies-when: any; every ground the logo, or a lockup holding it, is placed on
- question: Is the full-colour logo placed only on grounds every one of its colours reaches 3:1 against (or a keyline around the mark does), a ground inside the logo's lightness band taking another version or none, each version naming its grounds, a logo that is also a link taking a version that clears 3:1, and clear space measured in units of the mark?
- answered-by: builder
- writes: logo ground
- yields-to: vault.logo-ground-script, level 2
- source: W3C Understanding SC 1.4.3 and 1.4.11, which exempt a logo only where brand guidelines fix it; Spotify and GOV.UK brand guidelines; Aramco and CSU Chico brand guidelines; strength: first-party brand guidelines over WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: treatment
- target: Measure the logo's lightness band with palette.py; put the full-colour logo only on neutral grounds every logo colour clears at 3:1, the reversed version on named dark grounds, the one-colour version on photographs and busy grounds, and a keyline version only where no other works.
- reasons: design-critique/references/brand-palette.md#a-logos-grounds-follow-its-lightness
- ledger: COL-61, COL-66, IMG-165
- status: live

### vault.logo-colour
- applies-when: any; every placement of the logo, on every page
- question: Where the logo does not work on a ground, is its version or the ground changed and never its colours, with a version the client does not hold made only on the client's yes?
- answered-by: builder
- writes: logo colour
- yields-to: vault.logo-unchanged, level 2
- source: Spotify brand guidelines ("Its orientation, color, and composition should remain as indicated"); GOV.UK brand guidelines ("Do not alter colour balance within the wordmark"); strength: first-party brand guidelines
- era: timeless
- owner: vault
- stage: treatment
- target: Swap the logo's version or the ground, never its colours; ask the client before making a version they do not hold; a keyline is an addition, not a recolour.
- reasons: design-critique/references/brand-palette.md#never-recolour-a-logo
- ledger: SUR-92
- status: live

### vault.logo-unchanged
- applies-when: any; every placed client logo
- question: Does every pixel of the placed logo that lies past the edge band of the client's logo file, resampled to the placed size, match that file to within one 8-bit step on each channel and under 2 ΔE00?
- answered-by: script
- writes: logo colour
- yields-to: level 2
- source: the #262 ruling that a script compares a placed logo with the client's logo file, pixel for pixel away from the resampled edge (spec #324, user story 6, so a recolour too small for an eye or a default diff tool is still caught); Spotify and GOV.UK brand guidelines, which fix a logo's colours exactly; the one-step tolerance is measured (#330); the edge band is a guess no source sets (#324's Values); strength: house ruling for the rule, first-party brand guidelines for the exactness, a measurement for the tolerance, an unsourced guess for the band
- era: timeless
- owner: vault
- stage: value
- script: check-logo.py
- reasons: design-critique/references/brand-palette.md#never-recolour-a-logo
- ledger: none
- status: live

### vault.logo-ground-script
- applies-when: any; every placed client logo
- question: Does each colour of the client's logo file that meets its transparent ground reach 3:1 against every pixel of the ground it was rendered on, inside its box and in a ring just outside it?
- answered-by: script
- writes: logo ground
- yields-to: level 2
- source: the #262 ruling that a script reads the rendered ground (spec #324, user story 7, so a logo on a photograph or gradient meets the same rule as one on a declared colour); 3:1 is WCAG 2.2 SC 1.4.11's level for graphics, which W3C Understanding SC 1.4.3 and 1.4.11 apply to a logo whose ground the designer chooses; the ring and edge widths, how near the ground a colour counts as meeting it, the share and the distance off a straight mix under which a colour is taken for a blend and the scale an SVG is read at are guesses no source sets (#324's Values, #330); strength: house ruling for the script, WCAG 2.2 AA for the level, an unsourced guess for the widths
- era: timeless
- owner: vault
- stage: value
- script: check-logo.py
- reasons: design-critique/references/brand-palette.md#a-logos-grounds-follow-its-lightness
- ledger: none
- status: live

### vault.web-vitals
- applies-when: web-surface; the page on a phone
- question: Does the page respond to input within 200 ms (INP) and shift its layout by under 0.1 (CLS)?
- answered-by: whole-page
- writes: responsiveness and stability
- yields-to: vault.load, level 2
- source: web.dev Core Web Vitals; strength: platform guidance
- era: dated 2027-10-14
- owner: vault
- stage: value
- target: Keep interaction to next paint under 200 ms and cumulative layout shift under 0.1, reserving space for images, embeds and late fonts.
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: IMG-134, LAY-101, NAV-46
- status: live

### vault.ai-look
- applies-when: web-surface; the whole candidate
- question: Does the candidate avoid impeccable's dated "AI look" defaults (same-size icon cards as the page's structure, nested cards, the hero-metric template, a decorative eyebrow that names no section, place or category, section numbers, gradient text, glass on content, a coloured side border, hard offset shadows, monospace as a costume, an overused font), save any the brief, a direction card or the project's rules file earns back?
- answered-by: whole-page
- writes: AI-look default
- yields-to: level 5
- source: impeccable 4.5.0 `craft-floor` Refuse list and its detector rules (`overused-font`, `side-tab` among them); GOV.UK Design System headings, for the eyebrow that names a section; strength: impeccable "AI look" ban
- era: dated 2027-04-14
- owner: vault
- stage: treatment
- target: Leave out impeccable's AI-look defaults unless the brief, a direction card or the rules file asks for one; an eyebrow naming the section, place or category is fine.
- reasons: design-round/references/impeccable.md#the-ai-look-bans-dated-defaults-review-by-14-apr-2027
- ledger: COL-29, COL-80, COL-84, LAY-125, LAY-126, NEW2-77, PAG-144, PAG-145, SUR-15, SUR-78, TYF-9, TYF-10, TYF-23
- status: live

### vault.token-roles
- applies-when: any; every colour, space, radius, shadow, type and motion value the asset sets
- question: Does every value the asset sets come from the project's one value system through a token named by its role (primary action, control edge, surface, status), one role taking one value everywhere, rather than a raw value chosen for one element?
- answered-by: builder
- writes: value source
- yields-to: level 2
- source: Material 3's token tiers, a role named once and a value filling it; Garrett, The Elements of User Experience (2000), abstract before concrete; the house's dependency order (#121); strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Name each colour, space, radius, shadow, type style and motion by its role, fill each role from the project's value system, and set no raw value on a single element.
- reasons: design-critique/references/house-principles.md#dependency-order
- ledger: COL-33, COL-34, MOT-13, OTH-10, OTH-11, SUR-61, TXL-3
- status: live

### vault.wcag-aa
- applies-when: any; the whole asset, every success criterion that applies to it
- question: Does the asset meet every WCAG 2.2 level A and AA success criterion that applies to it, with no project, brand or craft rule lowering one?
- answered-by: whole-page
- writes: accessibility level
- yields-to: none
- source: WCAG 2.2 (October 2023), level AA, and the law that adopts it; the founder's ruling on #103 Q5 (A); strength: WCAG 2.2 AA
- era: dated 2027-10-14
- owner: vault
- stage: function
- target: Build to WCAG 2.2 AA throughout; where a rule here or in the project lowers a criterion, the criterion wins.
- reasons: design-critique/references/house-principles.md#source-precedence
- ledger: OTH-43
- status: live

### vault.shape-family
- applies-when: web-surface; the whole page's shapes: corners, buttons, cards, images, decoration
- question: Does the page keep one shape family, its rounding chosen from the brand's tone and held fixed across parts, rather than round and sharp corners mixed at random?
- answered-by: whole-page
- writes: shape family
- yields-to: vault.radius-meaning, level 2
- source: Apple WWDC25 session 356, "Get to know the new design system" (2025): shapes "should complement the system's rhythm and tone, not clash with it"; corners "too pinched— or flared ... can create tension and break the sense of balance"; Atlassian Radius, tokens for "consistency and cohesion" (as read Oct 2026); Bar and Neta, Psychological Science 17(8), 2006: sharp contours may "convey a sense of threat", and contour type has "a critical influence on people's attitude toward that object"; strength: design-system guidance, and the house's inference from Bar and Neta for the tie to brand tone
- era: timeless
- owner: vault
- stage: role
- target: Choose the page's rounding from the brand's tone, rounder for warm and playful and tighter for a precise tool, and keep it on every part.
- reasons: design-critique/references/surface-styling.md#one-shape-family
- ledger: NEW2-44
- status: live

### vault.logo-version
- applies-when: web-surface; the logo in the header, and every other placement whose width shrinks with the screen
- question: Does the full logo, mark and name, show wherever its width allows, and the mark alone only where space is tight and the page's context makes clear whose it is?
- answered-by: script
- writes: logo version by width
- yields-to: level 2
- source: Atlassian Design System, Logo, usage (as read Oct 2026): "Only use logomarks on their own when the context is very clear and where possible pair with descriptive text"; Atlassian navigation system, top nav items (as read Oct 2026): below 1024 px only the icon is shown; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Show the full logo where it fits, and the mark alone at narrow widths where the page already says whose it is.
- script: check-layout.py <page> --out <dir> --records --parts <declaration>
- parts: logo
- reasons: design-critique/references/brand-palette.md#a-logos-version-follows-its-width
- ledger: IMG-161
- status: staged

### vault.logo-link-name
- applies-when: web-surface; a logo that links to the home page
- question: Does a logo that links home have an accessible name, on its link or its image?
- answered-by: script
- writes: home-link logo name presence
- yields-to: none
- source: WCAG 2.2 success criteria 1.1.1 Non-text Content and 2.4.4 Link Purpose (In Context); W3C WAI Images Tutorial, "Functional images", example 1: a logo linking to the home page takes "W3C home" because "its primary function is to link to the homepage"; Atlassian Design System, Logo, usage, accessibility (as read Oct 2026): always include the brand name, never the word "logo", "Go to the Atlassian home page"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: treatment
- target: Give a logo that links home the organisation's name and "home" as its alt text or link name.
- script: check-markup.py, with the logo part declared
- parts: logo
- reasons: design-critique/references/markup-and-navigation.md#names-match-what-is-shown
- ledger: IMG-170
- status: staged

### vault.logo-link-words
- applies-when: web-surface; a logo that links to the home page
- question: Does the accessible name of a logo that links home name the organisation and where the link goes, never "logo" or a file name?
- answered-by: script
- writes: home-link logo name
- yields-to: none
- source: WCAG 2.2 success criteria 1.1.1 Non-text Content and 2.4.4 Link Purpose (In Context); W3C WAI Images Tutorial, "Functional images", example 1: a logo linking to the home page takes "W3C home" because "its primary function is to link to the homepage"; Atlassian Design System, Logo, usage, accessibility (as read Oct 2026): always include the brand name, never the word "logo", "Go to the Atlassian home page"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: treatment
- target: Give a logo that links home the organisation's name and "home" as its alt text or link name.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- parts: logo
- reasons: design-critique/references/markup-and-navigation.md#names-match-what-is-shown
- ledger: IMG-170
- status: staged

### vault.native-html
- applies-when: web-surface; every control: buttons, links, form fields, menus, tabs
- question: Is every control built from the HTML element that carries its role (`button`, `a href`, `input`, `select`), never a `div` or `span` given that role by ARIA, and does no element restate or override its own role?
- answered-by: script
- writes: element choice
- yields-to: none
- source: for native elements before ARIA, W3C, Using ARIA, the first rule of ARIA use: where a native element has the semantics and behaviour required, use it (Discontinued Draft, 24 Feb 2026), and web.dev, Learn Accessibility, "ARIA and HTML", "Rule 1: Don't use ARIA" (2022); for restated roles, W3C, ARIA in HTML (Recommendation, 11 Aug 2026), §1: setting a role that matches an element's implicit role is NOT RECOMMENDED; strength: W3C guidance
- era: timeless
- owner: vault
- stage: function
- target: Build each control from its native element, and add an ARIA role only where no element carries it.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/markup-and-navigation.md#native-elements-carry-their-role
- ledger: OTH-19
- status: staged

### vault.generated-content
- applies-when: web-surface; the line numbers of every code block
- question: Are a code block's line numbers kept out of what a screen reader announces, by an empty alternative (`content: counter(line) / ""`) or `aria-hidden` on their element?
- answered-by: script
- writes: announced line numbers
- yields-to: none
- source: W3C failure F87 (WCAG 2.2 success criterion 1.3.1): inserting non-decorative content with `::before` and `::after`; web.dev, Learn CSS, "Pseudo-elements": "anything other than an empty string will likely be announced by a screen reader"; MDN, `content` (modified Aug 2026, read Oct 2026): alternative text after a `/` is "intended for speech output by screen-readers"; MDN browser-compat-data: that alternative text since Chrome 77, Firefox 128 and Safari 17.4; strength: platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Give a code block's line numbers an empty alternative or put them on an `aria-hidden` element.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/markup-and-navigation.md#decorative-generated-content
- ledger: NEW2-35
- status: staged

### vault.generated-content-look
- applies-when: web-surface; every `::before` and `::after` whose `content` holds text or a symbol
- question: Is every `::before` and `::after` symbol a screen reader announces one that carries meaning, a decorative one kept out by an empty alternative (`content: "→" / ""`) or `aria-hidden` on its element?
- answered-by: look
- writes: announced generated content
- yields-to: vault.generated-content
- source: W3C failure F87 (WCAG 2.2 success criterion 1.3.1): inserting non-decorative content with `::before` and `::after`; web.dev, Learn CSS, "Pseudo-elements": "anything other than an empty string will likely be announced by a screen reader"; MDN, `content` (modified Aug 2026, read Oct 2026): alternative text after a `/` is "intended for speech output by screen-readers"; MDN browser-compat-data: that alternative text since Chrome 77, Firefox 128 and Safari 17.4; strength: platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Give decorative generated content an empty alternative (`content: "→" / ""`) or put it on an `aria-hidden` element.
- reasons: design-critique/references/markup-and-navigation.md#decorative-generated-content
- ledger: NEW2-35
- status: staged

### vault.delight-frequency
- applies-when: any; the whole asset, its parts ranked by how often a visitor uses them
- question: Does the asset spend its delight (a playful illustration, an expressive animation, a surprising detail) on the moments a visitor meets rarely (a first visit, a confirmed booking, an empty state), keeping the parts used most plain and quick?
- answered-by: whole-page
- writes: delight by frequency
- yields-to: vault.high-stakes, vault.brand-layer
- source: Benji Taylor, "Family Values" (Jul 2024), Delight through selective emphasis: "Delight tends to increase as the frequency of feature usage decreases"; IBM Carbon, Motion: "Reserve expressive motion for occasional, important moments" (as read Oct 2026); strength: practitioner writing and design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Put the playful and surprising touches on the rare moments, a first visit, a confirmation, an empty state, and keep the parts visitors use most plain and quick.
- reasons: design-critique/references/house-principles.md#expression-by-frequency
- ledger: OTH-17
- status: live

### vault.brand-distinct
- applies-when: any; a brand whose category has leaders a visitor knows
- question: Does each signature of the brand layer (its ground colour, mark, display type, illustration style) differ from the strongest cue of each leading competitor in the category, rather than share one?
- answered-by: whole-page
- writes: distinctness from competitors
- yields-to: vault.brand-layer
- source: Romaniuk, Building Distinctive Brand Assets (OUP 2018), read through Ehrenberg-Bass Institute, "Brands of distinction" (as read Oct 2026): an asset must be "unique", one that "only evokes the one brand", and "famous", and "Of these two, uniqueness is most important"; strength: marketing science, book read at summary level
- era: timeless
- owner: vault
- stage: role
- target: Name each category leader's strongest cue and give the brand's ground colour, mark, display type and illustration style a different one.
- reasons: design-critique/references/house-principles.md#distinct-from-the-category-leaders
- ledger: PAG-32
- status: live

### vault.tone-direction
- applies-when: any; the whole asset, and each direction card, where the brief leaves the look free
- question: Does each direction card's tone line place the direction on the five scales (energy, weight, warmth, order to richness, familiarity), with its palette, typeface and corner shape each moving the design toward that position, and any named style placed on the scales rather than standing in for the tone?
- answered-by: whole-page
- writes: overall aesthetic direction
- yields-to: vault.brand-layer, level 2
- source: Google Design, "Better, Easier, Emotional UX" (13 May 2025), M3 Expressive's 46 studies and a strong minority preferring calmer versions; Ou, Luo, Woodcock and Wright 2004, colour activity, weight and heat; Jiang, Gorn, Galli and Chattopadhyay 2016, round soft and angular hard; NN/g, "5 Principles of Visual Design in UX" (Mar 2020), symmetry quiet and asymmetry energetic; Tuch et al. 2012, complexity and prototypicality; the five-scale set is #204's synthesis; strength: published research
- era: dated 2027-10-19
- owner: vault
- stage: role
- target: State each direction's tone as a position on energy, weight, warmth, order to richness and familiarity, and pick its palette, typeface and corner shape to reach it; treat a named style as a shortcut to a position, not the tone.
- reasons: design-critique/references/tone.md#setting-the-direction
- ledger: NEW1-14
- status: live

### vault.tone-words
- applies-when: any; a request to make the asset bolder, quieter, louder or calmer
- question: Does the change move the choices `output` gives for the word, leaving the layout's familiarity as it was unless more unusual directions were asked for in those words?
- answered-by: builder
- writes: scales a tone word moves
- yields-to: vault.brand-layer, level 2
- source: Valdez and Mehrabian 1994 and Wilms and Oberfeld 2018, saturation and arousal; NN/g, "5 Principles of Visual Design in UX" (Mar 2020), symmetry quiet; IBM Carbon, motion overview, productive and expressive motion (as read Oct 2026); impeccable 4.5.0 `quieter`, `bolder` and the concept-seed register; the four meanings are the house's mapping, no source defines the words; strength: published research and design-system guidance
- era: timeless
- owner: vault
- stage: role
- inputs: the word asked for (louder, bolder, quieter, calmer)
- output: louder, energy up: more saturated colour, more of the surface in colour, bigger jumps in size and lightness, more and larger motion, a denser page; bolder, weight and the lead up: heavier type and lines, darker or more solid fills, a bigger display size, the leading part made stronger rather than every part; quieter, energy down: lower saturation, less of the surface in colour, smaller jumps in size and lightness, less and shorter motion; calmer, energy down and order up: quieter's moves plus more white space, fewer parts, a symmetric or plainly aligned layout, slower and gentler motion
- target: Move the choices `output` lists for the word asked; keep the layout's familiarity unless asked for something more unusual, even in an impeccable direction round.
- reasons: design-critique/references/tone.md#bolder-quieter-louder-and-calmer
- ledger: none
- status: live

### vault.tone-mix
- applies-when: web-surface; every place the asset mixes contrasting aesthetics, such as type or imagery of different eras
- question: Is each mix of contrasting aesthetics deliberate, placed in the brand layer at a first impression or an entry point rather than inside a working view's cards, tables or controls, with one aesthetic leading and the rest of the part held constant?
- answered-by: whole-page
- writes: mix of contrasting styles
- yields-to: vault.brand-layer, level 2
- source: Rauno, "Contrasting Aesthetics" (Jan 2024), for first impressions and tone, not productivity software; IBM Carbon, typography style strategies (Apr 2026), contrasting moments at entry points outside containers; Google Fonts Knowledge, Stocks, "Pairing typefaces" (as read Oct 2026), periods mixed with care; Butterick, "Mixing fonts", two faces with fixed roles; NN/g, "Consistency and standards" (2021); strength: expert and design-system practice
- era: dated 2027-10-19
- owner: vault
- stage: role
- target: Mix eras or styles only on purpose, at a first impression or an entry point in the brand layer, one aesthetic leading, and hold the rest of that part constant; keep working views to one aesthetic.
- reasons: design-critique/references/tone.md#mixed-aesthetics
- ledger: NEW1-15
- status: live
