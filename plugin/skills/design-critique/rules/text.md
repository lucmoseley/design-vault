# Rule records: text

How running text and inline links are set. The form is [rules.md](../rules.md)'s.

### vault.colour-script
- applies-when: web-surface; every link inside a line of text, at desktop and phone width
- question: Does every link inside a line of text differ from the text around it by more than colour (an underline, a border, a background, bold or italic), or else reach 3:1 contrast against that text?
- answered-by: script
- writes: colour signal
- yields-to: none
- source: WCAG 2.2 success criterion 1.4.1 Use of Color, by sufficient technique G183 and failure F73, with no hover or focus cue asked (design-vault#190); strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: treatment
- target: Underline every link in running text, or mark it by another cue than colour, or give it 3:1 against the text.
- script: check-access.py
- reasons: design-critique/references/text-presentation.md#the-link-rule
- ledger: BTN-63, BTN-64, COL-4, COL-20, COL-76, IMG-35, OTH-20, STA-16, STA-18, TXL-1, TXL-2, TXL-6, TXL-7, TXL-8, TXL-9, TYF-57
- status: live

### vault.link-style
- applies-when: web-surface; every link
- question: Is a link in running text underlined, thinly and with an offset clear of descenders, unless a colour at 3:1 against its text marks it instead, and does hover change something besides colour, such as the underline's offset or thickness?
- answered-by: builder
- writes: link style
- yields-to: vault.colour-script
- source: W3C Understanding SC 1.4.1 and technique G183; GOV.UK Design System links; NN/g, Nielsen 2004; Apple HIG Color; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Underline prose links by default, always where body text is tinted near the link's hue; on hover, move or thicken the underline.
- reasons: design-critique/references/text-presentation.md#the-link-rule
- ledger: BTN-13, BTN-64, COL-4, COL-20, COL-76, STA-16, STA-18, TXL-1, TXL-2, TXL-3, TXL-6, TXL-7, TXL-8, TXL-9, TYF-57
- status: live

### vault.paragraph-break
- applies-when: web-surface; every run of paragraphs
- question: Are paragraphs set apart by space between them or by a first-line indent, never both?
- answered-by: type
- writes: paragraph break
- yields-to: level 2
- source: Butterick, Practical Typography; strength: expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Separate paragraphs by space or by a first-line indent, one or the other.
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: TXL-53
- status: live

### vault.no-justify
- applies-when: web-surface; every block of running text
- question: Is running text set flush to its reading side and ragged at the other, never justified?
- answered-by: type
- writes: text alignment
- yields-to: level 2
- source: WCAG 2.2 SC 1.4.8 Visual Presentation (AAA); Butterick, Practical Typography; strength: expert craft range over WCAG 2.2 AAA
- era: timeless
- owner: vault
- stage: treatment
- target: Set running text flush left (flush right in a right-to-left language), never justified.
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: TXL-44
- status: live

### vault.prose-quotes
- applies-when: web-surface; every quotation mark and apostrophe in prose, headings, labels and alt text, outside code
- question: Does every quotation mark and apostrophe outside code use the curly character (‘ ’ “ ”), each apostrophe the closing single quote ’ even at a word's start (’70s), never a straight ' or "?
- answered-by: script
- writes: prose quote-mark glyph
- yields-to: level 2
- source: Butterick, Practical Typography, "Straight and curly quotes" ("straight quotes should never, ever appear in your documents") and "Apostrophes" ("Apostrophes always point downward"); Unicode 18.0 NamesList, U+0027: "2019 is preferred for apostrophe", and the paired English quotation marks 2018/2019 and 201C/201D; jakub.kr notes, 8 Aug 2026, curling straight quotes at build time; strength: Unicode character annotation and expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Write curly quotes and apostrophes in all prose, or curl straight ones at build time with a smart-quote step that leaves code alone; give a word-initial apostrophe ’, not ‘.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#curly-quotes-and-apostrophes
- ledger: TXL-101, TXL-103
- status: staged

### vault.code-quotes
- applies-when: web-surface; every code sample, inline code, command or value a visitor may copy, in `code`, `pre`, `kbd` or `samp`
- question: Does every quote mark and backtick inside code keep the straight character it has in the language (' " `), never curled?
- answered-by: script
- writes: code quote-mark glyph
- yields-to: none
- source: Butterick, Practical Typography, "Straight and curly quotes": straight quotes and backticks in software code "should never be converted to curly quotes", being "part of the code syntax"; strength: expert craft range, and code that runs only with the straight character
- era: timeless
- owner: vault
- stage: treatment
- target: Keep code in `code` or `pre` and exclude those elements from any smart-quote step, so its quotes and backticks stay straight.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#straight-quotes-in-code
- ledger: TXL-102
- status: staged

### vault.prime-marks
- applies-when: web-surface; every foot, inch, arcminute or arcsecond mark after a number
- question: Is each foot, inch, minute or second mark after a number the prime ′ or double prime ″ where the face draws them, else the straight ' or ", never a curly quote?
- answered-by: script
- writes: measurement mark glyph
- yields-to: level 2
- source: Unicode 18.0 NamesList: U+2032 PRIME "= minutes, feet", U+2033 DOUBLE PRIME "= seconds, inches"; Butterick, Practical Typography, "Foot and inch marks": the marks "are not curly", primes are "less common in professional fonts", so straight quotes are "the most reliable tools for the job"; strength: Unicode character annotation and expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Set measurement marks as ′ and ″ (`&prime;`, `&Prime;`) where the face has them, else straight ' and ", kept out of the smart-quote step, with a no-break space inside a feet-and-inches value.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#prime-marks
- ledger: TXL-104
- status: staged

### vault.dashes
- applies-when: web-surface; every hyphen and dash in prose, headings and labels
- question: Does each dash do its one job: a hyphen inside a compound word, an en dash for a range or a pairing (1880–1912, London–Paris), an em dash for a break in a sentence, never a hyphen or a double hyphen for either dash?
- answered-by: type
- writes: dash glyph
- yields-to: vault.dash-glyphs, level 2
- source: Butterick, Practical Typography, "Hyphens and dashes": the en dash for "a range of values" and a connection between words, the em dash "to make a break between parts of a sentence", set flush or with word spaces where it looks cramped on screen; Unicode 18.0 NamesList, U+002D, "used generically for hyphen, minus sign or en dash, all of which have dedicated alternatives"; strength: expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Use – for ranges and pairings and — for breaks in a sentence, the em dash's spacing one way across the site; keep the hyphen for compound words.
- reasons: design-critique/references/platform-defaults.md#dashes
- ledger: TXL-105
- status: live

### vault.dash-glyphs
- applies-when: web-surface; every hyphen and dash in prose, headings and labels
- question: Is no hyphen or double hyphen standing in for a dash: no double hyphen, no hyphen spaced between words, no hyphen in a number range (1880–1912, never 1880-1912), and are the page's em dashes between two words all spaced or all set flush?
- answered-by: script
- writes: dash glyph
- yields-to: level 2
- source: Butterick, Practical Typography, "Hyphens and dashes": the en dash for "a range of values" and a connection between words, the em dash "to make a break between parts of a sentence", set flush or with word spaces where it looks cramped on screen; Unicode 18.0 NamesList, U+002D, "used generically for hyphen, minus sign or en dash, all of which have dedicated alternatives"; strength: expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Use – for ranges and — for breaks in a sentence, and set the em dash's spacing one way across the site.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#dashes
- ledger: TXL-105
- status: live

### vault.math-signs
- applies-when: web-surface; every arithmetic expression, negative number and dimension (3 × 4 m) in text
- question: Does a multiplication or dimension use ×, never the letter x, and a negative number or subtraction use the minus −, never a hyphen?
- answered-by: script
- writes: arithmetic sign glyph
- yields-to: level 2
- source: BIPM SI Brochure, 9th ed., V4.01 (June 2026), §5.4.6: "When multiplying numbers only the multiplication sign × should be used"; Butterick, Practical Typography, "Math symbols": "12 × 34 − 56 = 352" right, the × "properly part of dimensional notations"; Unicode 18.0 NamesList, U+002D used generically for the minus sign, which has U+2212 as its dedicated alternative; strength: international standard (SI) and expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Write × (`&times;`) in products and dimensions and − (`&minus;`) for negatives and subtraction, outside code.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#times-and-minus-signs
- ledger: NEW2-1
- status: staged

### vault.leading-zero
- applies-when: web-surface; every number between −1 and 1 written with a decimal marker, outside code
- question: Does every decimal number between −1 and 1 show a zero before its decimal marker (0.25, −0.234), never a bare .25?
- answered-by: script
- writes: leading zero
- yields-to: level 2
- source: BIPM SI Brochure, 9th ed., V4.01 (June 2026), §5.4.4: "If the number is between +1 and −1, then the decimal marker is always preceded by a zero. For example −0.234 but not −.234"; Butterick, Practical Typography, "Grids of numbers": "add a leading zero for clarity"; strength: international standard (SI)
- era: timeless
- owner: vault
- stage: treatment
- target: Write a zero before the decimal marker of any number between −1 and 1, and format such numbers with `minimumIntegerDigits` left at 1.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#leading-zero
- ledger: NEW3-83
- status: staged

### vault.locale-numbers
- applies-when: web-surface; every number of four or more digits or with a decimal part shown as data (a price, count or measurement), outside code and identifiers such as years, phone and order numbers
- question: Is each such number formatted for the page's locale by `Intl.NumberFormat` or an i18n library using CLDR (de 1.234,5; en-IN 1,23,456; fr with narrow no-break spaces), never with separators written into a template?
- answered-by: script
- writes: number format
- yields-to: level 2
- source: Unicode CLDR 48.2 (17 Mar 2026); MDN `Intl.NumberFormat` (as read Oct 2026), locale examples de-DE and en-IN; Atlassian Badge, Accessibility: "Use your app's internationalization library or the browser's internationalization features"; NN/g, Nielsen 2001, guideline 112, a thousands separator for the locale; strength: Unicode locale data and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Format displayed numbers with `Intl.NumberFormat(<page locale>)` or the project's i18n library, the locale taken from the page's language (the visitor's choice where the site offers several).
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#numbers-in-the-locale-format
- ledger: OTH-2
- status: staged

### vault.week-hour
- applies-when: web-surface; every calendar, date picker, schedule or clock time shown
- question: Does each calendar start its week on the locale's first day, and each time show the locale's 12- or 24-hour cycle, both from CLDR (through `Intl.Locale` `getWeekInfo()` and `getHourCycles()`, or `Intl.DateTimeFormat`), unless the visitor has chosen otherwise?
- answered-by: script
- writes: first weekday and hour cycle
- yields-to: level 2
- source: web-features `intl-locale-info`, Baseline low 2026-07-21; MDN `Intl.Locale.prototype.getWeekInfo()` (firstDay from UTS 35 week data) and `getHourCycles()` (as read Oct 2026); strength: Unicode locale data
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Take a calendar's first weekday from `new Intl.Locale(locale).getWeekInfo().firstDay` (with a CLDR-backed fallback where `getWeekInfo` is missing) and format times with `Intl.DateTimeFormat`, never a hard-coded Sunday or 12-hour clock.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#first-weekday-and-hour-cycle
- ledger: OTH-8
- status: live

### vault.heading-markup
- applies-when: web-surface; every section title, card title and other text that heads the content after it
- question: Is every paragraph styled as a heading (bold, italic or larger than the text after it) built as a heading element, and does every heading element hold text?
- answered-by: script
- writes: heading markup
- yields-to: none
- source: WCAG 2.2 success criterion 1.3.1 Info and Relationships, Understanding page, sufficient techniques H42 "Using h1-h6 to identify headings" and ARIA12, failure F2; Atlassian Typography, Heading: "Use heading styles, rather than bold or a change of font size"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Build each section title as a heading element at its outline level, and style the level, never a `div` or `p` made to look like one.
- script: check-markup.py
- reasons: design-critique/references/platform-defaults.md#headings-and-lists-are-markup
- ledger: PAG-8
- status: staged

### vault.heading-markup-div
- applies-when: web-surface; every `div` or `span` styled as a section title, card title or other text that heads the content after it
- question: Is no `div` or `span` made to look like a title by its weight or size?
- answered-by: script
- writes: heading markup of styled blocks
- yields-to: none
- source: WCAG 2.2 success criterion 1.3.1 Info and Relationships, Understanding page, sufficient techniques H42 "Using h1-h6 to identify headings" and ARIA12, failure F2; Atlassian Typography, Heading: "Use heading styles, rather than bold or a change of font size"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Set every title in an `h1`–`h6`, never a `div` or `span` given a heading's weight or size.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#headings-and-lists-are-markup
- ledger: PAG-8
- status: staged

### vault.list-markup
- applies-when: web-surface; every run of items set one under another with bullets, numbers, icons or rules between them
- question: Is every run of content that reads as a list built as `ul`, `ol` or `dl` with `li` (or `dt` and `dd`), never as paragraphs with typed bullets, line breaks or `div`s?
- answered-by: script
- writes: list markup
- yields-to: none
- source: WCAG 2.2 success criterion 1.3.1, Understanding page, technique H48 "Using ol, ul and dl for lists or groups of links"; Butterick, Practical Typography, "Bulleted and numbered lists": "Use automated lists"; web.dev Learn CSS, Lists: a `display: list-item` lookalike "won't be read as a list item to screen readers"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Build list-like content as `ul`, `ol` or `dl`, drawing bullets and numbers with `::marker` or `list-style`, never typing them.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#headings-and-lists-are-markup
- ledger: TXL-73
- status: staged

### vault.lang-parts
- applies-when: web-surface; the page, and every element with a `lang` or `xml:lang`
- question: Does the `html` element carry the page's language in a `lang`, and does every `lang` and `xml:lang` on the page name a valid language, the two agreeing on `html`?
- answered-by: script
- writes: language tags
- yields-to: none
- source: WCAG 2.2 success criteria 3.1.1 and 3.1.2 Language of Parts, Understanding page and technique H58; CSS Text 3 (Editor's Draft, as read Oct 2026), `hyphens`: the UA "must therefore only automatically hyphenate text for which the content language is known"; webtypography.net rule 2.4.5, hyphenating a foreign word by its own language; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: treatment
- target: Put a valid `lang` on `html`, and write every `lang` as a language tag.
- script: check-markup.py
- reasons: design-critique/references/platform-defaults.md#the-language-of-each-passage
- ledger: TXL-33
- status: staged

### vault.lang-parts-look
- applies-when: web-surface; every passage or phrase in a language other than the page's, save proper names, technical terms and words the surrounding language has taken in
- question: Does each passage or phrase in a language other than the page's carry its own `lang`?
- answered-by: look
- writes: language of parts
- yields-to: vault.lang-parts
- source: WCAG 2.2 success criteria 3.1.1 and 3.1.2 Language of Parts, Understanding page and technique H58; CSS Text 3 (Editor's Draft, as read Oct 2026), `hyphens`: the UA "must therefore only automatically hyphenate text for which the content language is known"; webtypography.net rule 2.4.5, hyphenating a foreign word by its own language; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: treatment
- target: Put `lang` on the element around any quotation, title or phrase in another language.
- reasons: design-critique/references/platform-defaults.md#the-language-of-each-passage
- ledger: TXL-33
- status: staged

### vault.typed-case
- applies-when: web-surface; every text shown in capitals or small capitals for style (a label, button, heading or eyebrow), save acronyms and initialisms
- question: Is text shown in capitals for style typed in its normal case in the source and set in capitals by `text-transform` or `font-variant-caps`, with only acronyms and initialisms typed in capitals: no word of six or more letters, and no two words of two or more letters with only a space between them, typed in capitals unless the acronym list names them?
- answered-by: script
- writes: capitalisation method
- yields-to: vault.name-case, vault.text-case, level 2
- source: CSS Text 3 (Editor's Draft, as read Oct 2026), `text-transform`: "Authors must not rely on text-transform for semantic purposes; rather the correct casing and semantics should be encoded in the source document text", and it "must not affect the content of a plain text copy & paste operation"; MDN `text-transform`, language-specific case mapping by `lang`; strength: W3C specification
- era: timeless
- owner: vault
- stage: treatment
- target: Type labels and headings in the case `vault.text-case` gives and capitalise them in CSS; type an acronym in capitals only because it is one.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#capitals-set-by-style
- ledger: TXL-99
- status: staged

### vault.skip-ink
- applies-when: web-surface; every underlined text
- question: Does each underline break where it would cross a descender, by leaving `text-decoration-skip-ink` at `auto` (`all` for CJK text), never `none`?
- answered-by: script
- writes: underline skip-ink
- yields-to: level 2
- source: MDN `text-decoration-skip-ink` (as read Oct 2026): initial `auto`, `all` for CJK fonts where `auto` does not skip; web-features `text-decoration-skip-ink-all`, Baseline low 2026-05-07; Typography Handbook, Underlining; strength: browser default and craft guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Leave `text-decoration-skip-ink` at its `auto` default, setting `all` on Chinese, Japanese or Korean text; never `none`.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: link
- reasons: design-critique/references/platform-defaults.md#underlines-skip-descenders
- ledger: TXL-11
- status: live

### vault.hyphen-char
- applies-when: web-surface; every text hyphenated at line ends
- question: Is the character marking a hyphenation break left to the browser's `hyphenate-character: auto`, which takes it from the content language?
- answered-by: script
- writes: hyphenation character
- yields-to: level 2
- source: MDN `hyphenate-character` (as read Oct 2026): `auto` selects "an appropriate string based on the content language's typographic conventions"; web-features `hyphenate-character`, Baseline low 2023-09-18, high 2026-03-18; strength: browser default
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Leave `hyphenate-character` unset (`auto`), with the text's `lang` declared.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#the-hyphenation-character
- ledger: TXL-32
- status: live

### vault.spelling-mark
- applies-when: web-surface; every field a visitor types prose into (a `textarea`, a free-text `input`, a contenteditable region)
- question: Does each prose field keep the browser's own spelling mark (spellcheck left on), turning it off only for codes, names and passwords, and does any custom checker mark errors with `text-decoration-line: spelling-error` or `grammar-error`?
- answered-by: script
- writes: spelling error mark
- yields-to: level 2
- source: MDN `text-decoration-line` (as read Oct 2026): `spelling-error` uses "the user agents' method of highlighting spelling mistakes"; web-features `text-decoration-spelling-grammar`, Baseline low 2025-12-12; measured on design-vault#276 (docs/research/platform-defaults.md), Chromium 149 only; strength: browser default
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Leave `spellcheck` at its default on prose fields, set `spellcheck="false"` on code, username and identifier fields, and draw a custom checker's marks with `spelling-error` and `grammar-error`.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: textbox
- reasons: design-critique/references/platform-defaults.md#the-browsers-spelling-mark
- ledger: TXL-108
- status: live

### vault.rtl-sides
- applies-when: web-surface; every page or part shown in a right-to-left language
- question: Is the direction set by `dir="rtl"` in the markup, and are text alignment, margins, padding and borders set by logical properties (`start`, `end`, `inline-start`), so the layout mirrors, a paragraph of left-to-right text inside staying aligned to its own language?
- answered-by: script
- writes: inline sides and text alignment
- yields-to: level 2
- source: W3C Internationalization, "Structural markup and right-to-left text in HTML": `dir="rtl"` on `html`, "Never use CSS to apply the base direction", start and end rather than left and right; web.dev Learn Design, Internationalization, logical properties (as read Oct 2026); Apple HIG, Right to left, Text alignment; strength: W3C guidance and platform guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Put `dir` on `html` (and `dir="auto"` on user text), and write every inline side as a logical property: `text-align: start`, `margin-inline-start`, `padding-inline-end`, `border-inline-start`.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#right-to-left-mirroring
- ledger: TXL-47
- status: live

### vault.rtl-digits
- applies-when: web-surface; every number inside right-to-left text
- question: Do the digits of each number keep their left-to-right order inside right-to-left text, left to the bidirectional algorithm, while a sequence of numbers showing progress or order (a slider's scale, steps) runs in the reading direction?
- answered-by: builder
- writes: digit order
- yields-to: vault.rtl-digit-order, level 2
- source: Unicode UAX #9, Unicode Bidirectional Algorithm, revision 52 (2026-09-01), §3.3.6: numeric text "will always end up with an even level"; §2.7, markup over explicit formatting characters; Apple HIG, Right to left, Numbers and characters: "Don't reverse the order of numerals in a specific number"; strength: Unicode standard and platform guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Leave digit order to the bidirectional algorithm, never reversing a number's digits by hand or by CSS; isolate a number with `bdi` or `dir` only where neighbouring punctuation reorders; reverse only sequences that show a direction.
- reasons: design-critique/references/platform-defaults.md#digits-in-right-to-left-text
- ledger: NEW2-51
- status: live

### vault.rtl-digit-order
- applies-when: web-surface; every number inside right-to-left text
- question: Are the digits of each number inside right-to-left text drawn in their left-to-right order, never reversed by hand or by CSS?
- answered-by: script
- writes: digit order
- yields-to: level 2
- source: Unicode UAX #9, Unicode Bidirectional Algorithm, revision 52 (2026-09-01), §3.3.6: numeric text "will always end up with an even level"; §2.7, markup over explicit formatting characters; Apple HIG, Right to left, Numbers and characters: "Don't reverse the order of numerals in a specific number"; strength: Unicode standard and platform guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Leave digit order to the bidirectional algorithm, never reversing a number's digits by hand or by CSS; isolate a number with `bdi` or `dir` only where neighbouring punctuation reorders.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/platform-defaults.md#digits-in-right-to-left-text
- ledger: NEW2-51
- status: live

### vault.white-space
- applies-when: web-surface; every paragraph, list item, heading, table cell, definition and quotation
- question: Does each paragraph, list item, heading, table cell, definition and quotation keep the browser's white-space collapsing?
- answered-by: script
- writes: white-space collapse
- yields-to: level 2
- source: MDN `white-space-collapse`: initial `collapse`, `preserve`, `preserve-breaks`; web-features `white-space-collapse`, Baseline low 2024-03-19, high 2026-09-19; strength: browser default
- era: timeless
- owner: vault
- stage: treatment
- target: Leave prose at `white-space-collapse: collapse`; set code in `pre`, and verse or addresses with `preserve-breaks`, never `br` tags for spacing.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#white-space
- ledger: NEW2-6
- status: live

### vault.kept-breaks
- applies-when: web-surface; code, poetry, addresses and other text whose line breaks carry meaning
- question: Does text whose line breaks carry meaning, and only that text, keep its typed breaks and repeated spaces, by `pre`, `white-space-collapse: preserve` or `preserve-breaks`?
- answered-by: look
- writes: white-space collapse
- yields-to: vault.white-space, level 2
- source: MDN `white-space-collapse`: initial `collapse`, `preserve`, `preserve-breaks`; web-features `white-space-collapse`, Baseline low 2024-03-19, high 2026-09-19; strength: browser default
- era: timeless
- owner: vault
- stage: treatment
- target: Leave prose at `white-space-collapse: collapse`; set code in `pre`, and verse or addresses with `preserve-breaks`, never `br` tags for spacing.
- reasons: design-critique/references/platform-defaults.md#white-space
- ledger: NEW2-6
- status: live

### vault.ruby-position
- applies-when: web-surface; every ruby (pronunciation) annotation
- question: Does each ruby annotation sit over its base text in horizontal writing and to its right in vertical, by `ruby` markup and the browser's default `ruby-position`, set `under` only where the brief asks for a second level or a rare style?
- answered-by: script
- writes: ruby position
- yields-to: level 2
- source: W3C, Requirements for Japanese Text Layout (WG Note, 11 Aug 2020) §3.3.4: "ruby is attached to the right of base characters in vertical writing mode, and above in horizontal writing mode"; MDN `ruby-position` (as read Oct 2026), initial `alternate`; web-features `ruby-position`, Baseline low 2024-12-11; strength: W3C typographic requirement and browser default
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Mark annotations with `ruby` and `rt` and leave `ruby-position` at its default.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#ruby-annotations
- ledger: NEW2-7
- status: live

### vault.visited-links
- applies-when: web-surface; every link
- question: Do links in a list of articles, guides or results a visitor comes back to show a visited colour, clearly different and less saturated than the unvisited one and still 4.5:1 on its ground, while navigation, cards, controls and links to pages whose content keeps changing show none?
- answered-by: script
- writes: visited link style
- yields-to: level 2
- source: GOV.UK Design System, Links, the no-visited-state modifier "where it is not helpful … when linking to pages with frequently-changing content" (as read Oct 2026); NN/g, "113 Design Guidelines for Homepage Usability" (2001), "a clearly discernable and less saturated color for visited links", not grey; W3C Understanding SC 1.4.1, colour-only visited no failure while links meet SC 1.4.3; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Give links in content lists a visited colour, less saturated than the link colour and 4.5:1 on its ground; leave nav, cards and controls without one.
- script: check-state.py, its visited line
- parts: link
- reasons: design-critique/references/text-presentation.md#visited-links
- ledger: TXL-5
- status: staged

### vault.prose-emphasis
- applies-when: web-surface; emphasis inside running text
- question: Within running text, is emphasis kept to a few key words or phrases rather than long runs, with bold rather than italic in a sans serif and italic kept for titles and quotations there?
- answered-by: type
- writes: emphasis in running text
- yields-to: vault.emphasis-share, vault.emphasis-form, vault.link-style, level 2
- source: Butterick, Practical Typography, "Bold or italic": "think of them as mutually exclusive", "use bold and italic as little as possible", sans italics "just have a gentle slant that doesn't stand out", underlined bold "terrible"; USWDS Typography, "Avoid long sections of italic or bold text" (as read Oct 2026); GOV.UK font override classes, "Use bold text sparingly"; MDN, Accessibility: CSS and JavaScript, bold and italic "very recognizable"; strength: expert craft range and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Emphasise a few words in prose with bold or italic, never both and never an underline; in a sans serif use bold, keeping italic for titles and quotations.
- reasons: design-critique/references/text-presentation.md#emphasis-in-running-text
- ledger: TYF-57, TYF-59
- status: live

### vault.emphasis-share
- applies-when: web-surface; emphasis inside running text
- question: In each paragraph of running text of 20 words or more, does emphasis (bold at weight 600 or more, or italic, outside links) cover no more than a quarter of its words, with no emphasised run longer than ten words?
- answered-by: script
- writes: emphasis in running text
- yields-to: vault.emphasis-form, vault.link-style, level 2
- source: Butterick, Practical Typography, "Bold or italic": "use bold and italic as little as possible"; USWDS Typography, "Avoid long sections of italic or bold text" (as read Oct 2026); GOV.UK font override classes, "Use bold text sparingly"; strength: expert craft range and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Emphasise a few words in prose, never a quarter of a paragraph or a run of more than ten words.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/text-presentation.md#emphasis-in-running-text
- ledger: TYF-59
- status: live

### vault.emphasis-form
- applies-when: web-surface; emphasis inside running text
- question: Is emphasised text never underlined, and never both bold and italic?
- answered-by: script
- writes: emphasis form
- yields-to: none
- source: Butterick, Practical Typography, "Bold or italic": "think of them as mutually exclusive", "use bold and italic as little as possible", sans italics "just have a gentle slant that doesn't stand out", underlined bold "terrible"; USWDS Typography, "Avoid long sections of italic or bold text" (as read Oct 2026); GOV.UK font override classes, "Use bold text sparingly"; MDN, Accessibility: CSS and JavaScript, bold and italic "very recognizable"; strength: expert craft range and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Emphasise with bold or italic alone, never an underline.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/text-presentation.md#emphasis-in-running-text
- ledger: TYF-57
- status: live

### vault.sibling-emphasis
- applies-when: web-surface; one item set apart from equal siblings: new, recommended, current or selected in a list, row or set of cards
- question: Does an item set apart from its equal siblings differ by a step a glance catches, bold or heavier against regular (never semibold against regular), a fill on the item itself, its size or its position, and not by a hue that marks links or actions, nor by a tag where buttons sit?
- answered-by: look
- writes: sibling emphasis
- yields-to: vault.primary-action, level 2
- source: USWDS Tag, "To call attention to new or updated content, consider changing the background color of the object itself or experiment with changing the font weight" and "Avoid tags if they might appear in the same area of the page as buttons" (as read Oct 2026); Google Fonts Knowledge, "Avoid using semibold for emphasis in regular text. Use bold or extrabold" (as read Oct 2026); Apple HIG Color, an interactive colour on noninteractive text "is confusing" (16 Dec 2025); strength: design-system guidance
- era: timeless
- owner: vault
- stage: role
- target: Set one item apart from its equals by bold, its own fill, size or place; keep link and action hues and tags off it.
- reasons: design-critique/references/text-presentation.md#one-among-equals
- ledger: TXL-86
- status: staged

### vault.list-marker
- applies-when: web-surface; every bulleted list
- question: Does each bulleted list mark its items with a plain geometric marker (a disc, a circle, a dash, or the face's own bullet), no larger than it needs to be noticed, with an icon in its place only where each icon repeats its item's meaning and is hidden from screen readers, and never an emoji?
- answered-by: script
- writes: list marker
- yields-to: vault.list-markup, level 2
- source: Butterick, Practical Typography, "Bulleted and numbered lists": bullets "big enough to be noticeable, but no bigger"; "Simple geometric dingbats are better than pictorial ones"; USWDS, Icon list (updated Dec 2024): "The icon should only reinforce the text of the list item", icons `aria-hidden`, the standard list for running text; Oregon State University, College of Health, digital accessibility, "Don't Use Emojis as Bullets" (as read Oct 2026): a screen reader reads each one by name; strength: craft book and design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Mark a bulleted list with a plain geometric marker, no larger than it needs to be seen; use icons in its place only where each repeats its item, `aria-hidden`; never emoji.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/text-presentation.md#list-markers
- ledger: TXL-66
- status: staged

### vault.text-align
- applies-when: web-surface; every block of running text, a table's text cells included
- question: Does each block of running text keep one straight edge, on the side its language reads from, and an uneven opposite edge, with no justified block outside those the project's rules file names?
- answered-by: script
- writes: running text alignment
- yields-to: level 2
- source: GOV.UK Design System, "Font override classes" (GOV.UK Frontend v6): "Do not 'justify' blocks of body copy text", "you should usually left-align body copy text"; USWDS Typography: "Justified text, common in print, does not yet display well enough in a web browser to be considered a best practice", "Set type flush left"; WCAG 2.2 (2023) SC 1.4.8 (AAA) and failure F88, uneven word spacing makes "rivers of white" for readers with some cognitive disabilities; Butterick, Practical Typography, "Justified text": justification needs hyphenation and he will "always left-align" a web page; Bringhurst via Rutter, webtypography.net 2.1.3: narrow measures and "Many unserifed faces look best when set ragged"; strength: design-system guidance over WCAG 2.2 AAA
- era: timeless
- owner: vault
- stage: treatment
- target: Set running text flush left (flush right in a right-to-left language) and ragged at the other edge; justify only a block the project's rules file names.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/alignment-and-width.md#ragged-not-justified
- ledger: TXL-44
- status: staged

### vault.justify-space
- applies-when: web-surface; a block the project's rules file allows to be justified
- question: Does justified text put its extra space between words, with `hyphens: auto` and the page's `lang` set, never between letters in a language that spaces its words?
- answered-by: script
- writes: justification spacing
- yields-to: vault.text-align
- source: Butterick, Practical Typography, "Justified text": the extra space, "Please—put it between the words", and "you must also turn on hyphenation"; MDN, `text-justify` (modified Jul 2026): `inter-word` "is most appropriate for languages that separate words using spaces", `inter-character` for "languages like Japanese", initial value `auto`, "Limited availability", not Baseline; Rutter, webtypography.net 2.1.3: "Effective justification of text can only be achieved if long words are hyphenated"; strength: expert craft range and platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Where the project allows justified text, set `hyphens: auto` with the page's `lang`, and leave `text-justify` at `auto` or `inter-word`; never `inter-character` in a language that spaces its words.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/alignment-and-width.md#where-justification-is-allowed
- ledger: TXL-49
- status: live

### vault.centred-text
- applies-when: web-surface; every centred text block
- question: Is every centred text block a heading, a title, a short phrase or a passage of three lines or fewer, never a block of running text longer than that?
- answered-by: script
- writes: centred text
- yields-to: level 2
- source: Butterick, Practical Typography, "Centered text": "acceptable when used for short phrases or titles", "Whole text blocks should not be centered"; Latin, "5 keys to accessible web typography" (2019): "Don't center-align paragraphs that are longer than 2 or 3 lines of text"; Dannaway, UI design tips, tip 15 (updated Jul 2026): "Centre alignment can work for headings and short text", longer body text is harder to read "because the starting point of each line constantly changes"; USWDS Typography: "most websites benefit from a consistent use of left-aligned text"; strength: expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Centre only headings, titles, short phrases and passages of three lines or fewer; set longer text flush left.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/alignment-and-width.md#centre-only-short-text
- ledger: TXL-45
- status: staged

### vault.alignment-count
- applies-when: web-surface; every section, and every component with more than one text block
- question: Does each section and component set its text blocks in one alignment, save a table's right-aligned numbers and headings and a centred block of three lines or fewer?
- answered-by: script
- writes: alignment count
- yields-to: vault.table-align, vault.centred-text
- source: Dannaway, UI design tips 14, tip 8 (updated Jul 2026): "The more different types of alignment you use (left, right, or centre), the more complex and messy an interface can look", worst "within a small component or section", "Sticking with a single alignment (or as few as possible)"; impeccable 4.5.0, distill.md: "Pick left or center, stick with it"; USWDS Typography: "a consistent use of left-aligned text"; NN/g, "Why Does a Design Look Good?" (2021, modified Nov 2025): "Any alignment inconsistencies should be purposeful"; strength: expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Pick one alignment for a section's or component's text, left by default, and keep it.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/alignment-and-width.md#one-alignment-a-section
- ledger: TXL-46
- status: staged

### vault.text-columns
- applies-when: web-surface; running text set in CSS columns (`column-count` or `column-width`)
- question: Is running text set in CSS columns only where the whole multi-column block fits one screen's height, and does a heading over the block span all its columns?
- answered-by: script
- writes: multi-column text
- yields-to: level 2
- source: Butterick, Practical Typography, "Columns" ("Fine in print, not on the web"): "a web page has an indefinite bottom edge", columns help "where you have a small amount of text or a list of links that can fit on a browser single screen"; MDN, "Multiple-column layout" (modified Oct 2026): `column-span: all` makes an element span every column, content "continues below the element, creating a new set of columns", with a spanning subhead as the example; impeccable 4.5.0, distill.md: "Use available space generously instead of complex multi-column layouts"; that a heading over the block spans it is the house's, as no source read says when a heading must span; strength: expert craft range and platform documentation, with a house rule for headings
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Set columns only for a block that fits one screen's height, sized by `vault.line-length`, and give a heading inside it `column-span: all`.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/alignment-and-width.md#text-in-columns
- ledger: LAY-50, LAY-51
- status: staged

### vault.side-indent
- applies-when: web-surface; running text set narrower than its column by side padding or margin on the paragraph
- question: Is running text's line length set by its column's width, with side indents on a paragraph kept for set-apart blocks (block quotations, notes), each still holding the line length `vault.line-length` gives?
- answered-by: script
- writes: side indent
- yields-to: vault.line-length
- source: Butterick, Practical Typography, "Line length": "establish the basic length using page margins", side indents "reserve that for special situations (for instance, block quotations)", and "start with long enough lines so that the indented parts also fall within the target range"; "Page margins": margins "have the greatest effect on line length"; strength: expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Set the measure on the column, not by indenting paragraphs; indent only block quotations and similar set-apart blocks, and keep their lines in range.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/alignment-and-width.md#margins-set-the-measure
- ledger: TXL-60
- status: staged

### vault.text-case
- applies-when: web-surface; every heading, page title, button label, link, tag or status label, list item, menu item and tooltip
- question: Is each of these in sentence case, capitals kept for the first word, proper nouns and acronyms, one case for each kind of element across the site, with no title case and no capitals beyond the short labels `vault.caps-extent` allows, unless the project's rules file names another case?
- answered-by: look
- writes: letter case by element
- yields-to: vault.label-case, vault.badge-case, vault.caps-extent, level 2
- source: GOV.UK Design System, Headings (as read Nov 2026): "Write all headings in sentence case"; GOV.UK style guide, A to Z, Capitalisation (as read Nov 2026): "Always use sentence case, even in page titles and service names"; GOV.UK Button: "Write button text in sentence case"; GOV.UK Tag, changed in GOV.UK Frontend v5.0.0 (Dec 2023) from uppercase bold to sentence case, since "uppercase text can be harder to read, particularly for longer tag text"; Atlassian Button and Lozenge (as read Nov 2026): "Use sentence-case capitalization. Don't use title case capitalization or all caps"; Atlassian Empty state: "Always use sentence case for titles and headings"; USWDS Button: "Use sentence-case capitalization for button labels", and USWDS List: "Use sentence case and begin lists with a capital letter"; Butterick, "Headings": "Always Avoid Title Case, Because Your Headings Aren't Titles"; Apple HIG, Writing (as read Nov 2026): "Choose a style for each UI element type and use it consistently"; NN/g, Nielsen and Tahir 2001, homepage guideline: "Use consistent capitalization", as an odd item "gives that one item undue emphasis"; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Write headings, titles, buttons, links, tags, list items, menu items and tooltips in sentence case, capitalising only the first word, names and acronyms, and keep one case per kind of element across the site.
- reasons: design-critique/references/text-presentation.md#sentence-case-by-element
- ledger: TXL-95, TXL-96, TXL-97, BTN-51
- status: staged

### vault.label-case
- applies-when: web-surface; every heading, button label, link, list item and menu item shown on the page
- question: Does each of these that starts with a letter start with a capital, with no title case: no common word after the first capitalised where the page's own text or the common-words list has it in lower case, beyond the names and acronyms the word lists hold, where the project's rules file sets no other case?
- answered-by: script
- writes: letter case by element
- yields-to: vault.badge-case, vault.caps-extent, level 2
- source: GOV.UK Design System, Headings (as read Nov 2026): "Write all headings in sentence case"; GOV.UK style guide, A to Z, Capitalisation (as read Nov 2026): "Always use sentence case, even in page titles and service names"; GOV.UK Button: "Write button text in sentence case"; GOV.UK Tag, changed in GOV.UK Frontend v5.0.0 (Dec 2023) from uppercase bold to sentence case, since "uppercase text can be harder to read, particularly for longer tag text"; Atlassian Button and Lozenge (as read Nov 2026): "Use sentence-case capitalization. Don't use title case capitalization or all caps"; Atlassian Empty state: "Always use sentence case for titles and headings"; USWDS Button: "Use sentence-case capitalization for button labels", and USWDS List: "Use sentence case and begin lists with a capital letter"; Butterick, "Headings": "Always Avoid Title Case, Because Your Headings Aren't Titles"; Apple HIG, Writing (as read Nov 2026): "Choose a style for each UI element type and use it consistently"; NN/g, Nielsen and Tahir 2001, homepage guideline: "Use consistent capitalization", as an odd item "gives that one item undue emphasis"; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Write headings, buttons, links, list items and menu items in sentence case, capitalising only the first word, names and acronyms.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>] [--own-case]
- reasons: design-critique/references/text-presentation.md#sentence-case-by-element
- ledger: TXL-95, TXL-97, BTN-51
- status: staged

### vault.badge-case
- applies-when: web-surface; every badge the building session declares
- question: Is each badge's text left in the case it was written, with no upper-case or title-case transform?
- answered-by: script
- writes: badge case
- yields-to: none
- source: GOV.UK Design System, Headings (as read Nov 2026): "Write all headings in sentence case"; GOV.UK style guide, A to Z, Capitalisation (as read Nov 2026): "Always use sentence case, even in page titles and service names"; GOV.UK Button: "Write button text in sentence case"; GOV.UK Tag, changed in GOV.UK Frontend v5.0.0 (Dec 2023) from uppercase bold to sentence case, since "uppercase text can be harder to read, particularly for longer tag text"; Atlassian Button and Lozenge (as read Nov 2026): "Use sentence-case capitalization. Don't use title case capitalization or all caps"; Atlassian Empty state: "Always use sentence case for titles and headings"; USWDS Button: "Use sentence-case capitalization for button labels", and USWDS List: "Use sentence case and begin lists with a capital letter"; Butterick, "Headings": "Always Avoid Title Case, Because Your Headings Aren't Titles"; Apple HIG, Writing (as read Nov 2026): "Choose a style for each UI element type and use it consistently"; NN/g, Nielsen and Tahir 2001, homepage guideline: "Use consistent capitalization", as an odd item "gives that one item undue emphasis"; strength: design-system guidance
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Write badges in sentence case, never transformed to capitals or title case.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/text-presentation.md#sentence-case-by-element
- ledger: TXL-96
- status: staged

### vault.name-case
- applies-when: web-surface; every place the asset shows a name a person entered: a profile, a greeting, a list of people, a confirmation page
- question: Is each name a person entered shown in the case they typed, with no `text-transform`, capitalising script or upper-case-only field changing it?
- answered-by: script
- writes: name case
- yields-to: level 2
- source: USWDS, Create a user profile, Name (as read Nov 2026): "Do not normalize casing in names. In some names, such as McNamara and van der Waals, casing is part of the name"; W3C Internationalization, "Personal names around the world" (as read Nov 2026): "Forms should preserve the case the user enters", and "Don't require names to be entered all in upper case"; strength: design-system guidance and W3C guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Show every name exactly as its owner typed it; put no case transform on a name, even where its row or heading is styled in capitals.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/text-presentation.md#names-as-typed
- ledger: TXL-100
- status: live

### vault.hyphens-body
- applies-when: web-surface; every block of running text, a table's text cells and list items included
- question: Does running text take the hyphenation its alignment, line length and language call for: `hyphens: auto` with `lang` declared where it is justified, ragged under 40 characters a line, or ragged under 50 in a language of long compound words, and the default `manual` elsewhere?
- answered-by: script
- writes: body text hyphenation
- yields-to: vault.justify-space, vault.heading-hyphens
- source: Butterick, Practical Typography, "Hyphenation": "Mandatory for justified text; optional otherwise", for left-aligned text "Hyphenation doesn't improve text legibility. In this case, consider turning it off", and "As line length gets shorter, hyphenation becomes essential"; Rutter, Web Typography, "Numerals and tables" p. 130: in narrow table columns "You can hyphenate, however, particularly if the table columns would otherwise have a pronounced rag"; webtypography.net 2.1.2 (Bringhurst): "For multiple column work, a better average is 40 to 50 characters"; web.dev, Learn Design, "Internationalization": "Some languages, like German, have long words in common usage", "avoid designing narrow columns", "use CSS to introduce hyphens"; MDN `hyphens` (modified 21 Jul 2026): browsers "will only hyphenate if this attribute is present and the appropriate hyphenation dictionary is available"; web-features `hyphens`, Baseline low 2023-09-18, high 2026-03-18; no source gives a count for a narrow line, so the 40 and 50 cut-offs are the house's, set at the edges of Bringhurst's column band; strength: house rule over expert craft range and platform documentation
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- inputs: the block's alignment (`vault.text-align`), its line length in characters as set (`vault.line-length`), its content language
- output: justified → `hyphens: auto` (`vault.justify-space`); ragged and under 40 characters → `auto`; ragged and under 50 in a language of long compound words (German and the like) → `auto`; ragged otherwise → leave `manual`; `auto` always with `lang` on the element or an ancestor
- target: Leave ragged body text unhyphenated at a normal measure; turn on `hyphens: auto`, with `lang` declared, for narrow columns, cards, table cells and phone-width blocks under 40 characters, or under 50 in a long-word language.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/line-breaks.md#hyphenate-by-measure
- ledger: TXL-28, TXL-29
- status: staged

### vault.hyphen-chars
- applies-when: web-surface; every block set to `hyphens: auto`
- question: Does hyphenated text keep at least two letters before the break and three after it, in words of five letters or more, by `hyphenate-limit-chars: 5 2 3`?
- answered-by: script
- writes: hyphenation character limits
- yields-to: level 2
- source: webtypography.net 2.4.1 (Bringhurst): "leave at least two characters behind and take at least three forward"; CSS Text Module Level 4 (Editor's Draft, 26 Oct 2026), `hyphenate-limit-chars`: "If the word does not meet the required minimum number of characters in the word / before the hyphen / after the hyphen, then the word must not be hyphenated", `auto` suggested as "2 for before and after, and 5 for the word total"; MDN `hyphenate-limit-chars` (modified 28 Sep 2026): "Limited availability"; web-features `hyphenate-limit-chars`: not Baseline, Chrome 109, Firefox 137, no Safari; `5 2 3` is the house's, joining CSS's five-letter word total to Bringhurst's two and three; strength: house rule over expert craft range and web platform specification
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Wherever `hyphens: auto` is set, set `hyphenate-limit-chars: 5 2 3` beside it.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/line-breaks.md#hyphenation-limits
- ledger: TXL-30
- status: staged

### vault.hyphen-lines
- applies-when: web-surface; every block set to `hyphens: auto`, as rendered
- question: Do no more than three lines in a row end in a hyphenation break, with `hyphenate-limit-lines: 3` set where the browser takes it?
- answered-by: script
- writes: hyphenation line limit
- yields-to: level 2
- source: webtypography.net 2.4.3 (Bringhurst): "Avoid more than three consecutive hyphenated lines"; CSS Text Module Level 4 (Editor's Draft, 26 Oct 2026): `hyphenate-limit-lines` "indicates the maximum number of successive hyphenated lines in an element", initial `no-limit`, and `pretty` may avoid "hyphenation on too many consecutive lines"; caniuse, `hyphenate-limit-lines` (as read Nov 2026): Safari 27.3 alone, `-webkit-hyphenate-limit-lines` Safari 6 on; strength: expert craft range and web platform specification
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Beside `hyphens: auto`, set `hyphenate-limit-lines: 3` and `-webkit-hyphenate-limit-lines: 3`; where a render still shows four hyphenated lines in a row, widen the column.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/line-breaks.md#hyphenation-limits
- ledger: TXL-31
- status: staged

### vault.soft-hyphens
- applies-when: web-surface; every word the browser's hyphenation breaks wrongly or cannot break (a trade name, a jargon word, an unusual proper name)
- question: Is hyphenation left to the browser's dictionary (`hyphens: auto` with `lang`), with a soft hyphen (`&shy;`) placed by hand only inside such a word, never scattered through running text to stand in for automatic hyphenation?
- answered-by: script
- writes: manual hyphenation points
- yields-to: vault.hyphens-body
- source: Butterick, Practical Typography, "Optional hyphens": "Some words bedevil hyphenation engines", the problem "usually afflicts words that aren't in a standard hyphenation dictionary, like jargon words, unusual proper names, and words with nonstandard spellings, like trade names", the HTML entity `&shy;`; "Hyphenation": "The nonbreaking hyphen and the optional hyphen solve most hyphenation problems, and even those are pretty rare"; MDN `hyphens` (modified 21 Jul 2026): under `auto`, "suggested line break opportunities … will override automatic break point selection when present"; MDN, "Wrapping and breaking text" (modified 12 Aug 2026): "A soft break only breaks if breaking is needed"; strength: expert craft range and platform documentation
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- target: Let `hyphens: auto` and `lang` hyphenate; put `&shy;` by hand only inside a word the browser breaks wrongly.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/line-breaks.md#soft-hyphens-by-hand
- ledger: TXL-34
- status: staged

### vault.heading-hyphens
- applies-when: web-surface; every heading, title and display line
- question: Is every heading left unhyphenated, `hyphens` `manual` or `none`, never `auto`?
- answered-by: script
- writes: heading hyphenation
- yields-to: level 2
- source: Butterick, Practical Typography, "Headings": "Suppress hyphenation in headings"; "Hyphenation": "headings are relatively short, so hyphenation often causes more problems than it solves"; strength: expert craft range
- era: timeless
- owner: vault
- stage: treatment
- target: Set `hyphens: manual` on headings, overriding any page-wide `auto`.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/line-breaks.md#headings-are-not-hyphenated
- ledger: TXL-35
- status: staged

### vault.text-wrap
- applies-when: web-surface; every heading, caption, block quotation and pull quote, every paragraph and list item of running text
- question: Does each text role take the line-wrapping style its role and length call for: `text-wrap: balance` on headings, captions and quotations of six lines or fewer, `pretty` on paragraphs and list items, neither on page-wide `*` or on editable text, and no hard `<br>` placed to even out a heading's lines?
- answered-by: script
- writes: text wrap style
- yields-to: vault.edit-wrap
- source: MDN `text-wrap` (modified 27 Aug 2026): `balance` for content "limited to a short number of lines, such as headings, captions, and blockquotes", "six or less for Chromium and ten or less for Firefox"; MDN `text-wrap-style` (modified 8 Jun 2026): `pretty` "intended for body copy where good typography is favored over performance", "should be only used for longer blocks of text when the layout is more important than speed"; CSS Text Module Level 4 (Editor's Draft, 26 Oct 2026): `balance` "in the case of 5 or fewer lines must not change" the line count, `pretty` "possibly use it selectively where it matters most"; Chrome for Developers, "CSS text-wrap: balance": "It is not a good idea to apply text-wrap balancing to your entire design", "Balancing won't change the inline-size of the element", and in "a card (or any container with borders or shadows)" balancing "creates imbalance to the contained element"; "CSS text-wrap: pretty": `pretty` adjusts "previous lines to make room" for a word "alone at the end of a text block"; Comeau, "Custom CSS reset" (updated 3 Jun 2026): `pretty` on `p`, `balance` on `h1`–`h6`, and "no detectable speed difference"; Comeau, "Browser support" (2024): without support "there also isn't any downside"; Typography Handbook (updated for 2026): `balance` "Only apply to short text – headings, captions, pull quotes", "Do not use on body text", `pretty` on "p, li"; Butterick, "Widow and orphan control": browsers "are happy to put a small word alone on the last line of a paragraph, which always looks bad", "don't use a hard line break or carriage return"; his "Hard line breaks" evens a heading's lines by hand with `<br />`, which the house replaces with `balance`, and the bordered-box exception to `pretty` is the house's; web-features: `text-wrap-balance` Baseline low 2024-05-13, `text-wrap-pretty` not Baseline (Chrome 117, Safari 26, no Firefox); strength: web platform specification and named practitioners
- era: dated 2027-11-13
- owner: vault
- stage: treatment
- inputs: the text's role (heading, title, caption, block quotation, pull quote, paragraph, list item, editable region), its rendered line count, whether it sits left-aligned in a bordered or shaded box of fixed width
- output: heading, title, caption or quotation of six lines or fewer → `balance`, except left-aligned in a bordered or shaded fixed-width box → `pretty`; paragraph or list item of running text → `pretty`; text over six lines in a balanced role → `pretty`; editable region → `vault.edit-wrap`; never set on `*`
- target: Give headings, captions and pull quotes `text-wrap: balance` and paragraphs and list items `text-wrap: pretty`, by element, never on `*`; use `pretty` for a left-aligned heading inside a bordered card; never even out a heading with `<br>`.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/line-breaks.md#balance-headings-pretty-paragraphs
- ledger: TXL-36, TXL-37
- status: staged

### vault.nonbreaking
- applies-when: web-surface; every number with its unit or label, every short reference, short expression, honorific or phrase read as one unit, in prose, headings and labels
- question: Is each such group joined by a no-break space (`&nbsp;`, U+00A0) so a line never splits it: a number and its unit (6.2&nbsp;mm, 2.54&nbsp;cm), a reference mark or label and its number (§&nbsp;1782, ¶&nbsp;49, Fig.&nbsp;23, page&nbsp;3, chapter&nbsp;5, Ex.&nbsp;A), a short expression (4&nbsp;×&nbsp;4), an honorific and the name (Ms.&nbsp;Marvel), a copyright or trademark symbol and the word it sits against (©&nbsp;2026), with no run of no-break spaces longer than a short phrase?
- answered-by: script
- writes: no-break joins
- yields-to: vault.sentence-space
- source: Butterick, Practical Typography, "Nonbreaking spaces": "Put a nonbreaking space before any numeric or alphabetic reference to prevent awkward breaks", "after other abbreviated reference marks (Ex. A, Fig. 23)", "honorifics and titles (Sgt. Rock, Ms. Marvel)", "trademark and copyright symbols", "you should use the `&nbsp;` escape code, as it makes the nonbreaking space visible and explicit"; webtypography.net 2.4.6 (Bringhurst): "Link short numerical and mathematical expressions with hard spaces", examples "6.2 mm", "4 × 4", "page 3", "chapter 5"; NN/g, "113 Design Guidelines for Homepage Usability" (2001), guideline 23: "Use non-breaking spaces between words in phrases that need to go together in order to be scannable and understood", since "text must fit into narrow spaces"; strength: expert craft range and usability research guideline
- era: timeless
- owner: vault
- stage: treatment
- target: Write `&nbsp;` between a number and its unit, a reference label and its number, the parts of a short expression, an honorific and its name, and a © or ™ and the word it sits against; join nothing longer than a short phrase, so a phone line can still break.
- script: check-text.py <page> --out <dir> [--parts <declaration>] [--words <file>]
- reasons: design-critique/references/line-breaks.md#groups-that-never-split
- ledger: NEW2-36
- status: staged
