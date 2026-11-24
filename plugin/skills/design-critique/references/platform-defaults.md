# Platform defaults

Why a page's type, text, forms and images follow the standard or browser default their records name (#276). The source checks and browser measurements behind the records are `docs/research/platform-defaults.md` in the design vault.

A project's rules file wins over every record here except a floor WCAG or the law sets ([source precedence](house-principles.md#source-precedence)). A dated record is reviewed a year after writing, or sooner when browsers change the behaviour it rests on.

## Typography

### A face that covers the text

Record: `vault.glyph-coverage`.

- **Why.** The browser picks a font for each character on its own. A character the chosen face lacks is drawn in the next family, or in whatever the visitor's machine has, so one word can mix two faces or show an empty box (CSS Fonts 4 §5.2).
- **Trade-off.** A face that covers many scripts is a larger file. Subsetting by `unicode-range` keeps it small, but each script it leaves out needs a named face of its own.
- **Clash.** None known. `vault.font-stack` sets the order of the stack, and this record checks that its first family covers the text.

### True bold and italic

Record: `vault.true-faces`.

- **Why.** A synthesised bold is a stroke drawn round the regular face, and a synthesised italic is the upright face slanted. Neither is as good as a face designed for the job, and a real italic often has different letter shapes (CSS Fonts 4 §2.8; MDN).
- **Trade-off.** Each true face is another file to load. A variable file whose axes cover the weights counts as true faces, and is not synthesis.
- **Clash.** `vault.type-axes` decides between static and variable files, and this record only asks that every weight and style the page uses is loaded. For CJK text, MDN advises turning synthesis off.

### True small caps

Record: `vault.small-caps`.

- **Why.** Fake small caps are full capitals shrunk down, so their strokes come out too thin and they look too tall next to lowercase. Every type source read rejects them (Butterick; Bringhurst via Rutter; Latin 2023).
- **Trade-off.** Few web fonts draw small caps, and fewer draw them in italic. Without them, the choice is full capitals with tracking, or no caps at all.
- **Clash.** `vault.type-tracking` owns the tracking of capitals and small caps.

### Kerning stays on

Record: `vault.kerning`.

- **Why.** Kerning applies the spacing corrections the type designer built into the font. CSS leaves `auto` to the browser, and the spec tells authors who want kerning to set `normal`.
- **Trade-off.** Little: the way to switch it off, `optimizeSpeed`, trades legibility for speed (MDN `text-rendering`).
- **Clash.** `vault.type-tracking` adds letter spacing, which the browser applies after kerning.

### Fractions

Record: `vault.fractions`.

- **Why.** A true fraction glyph is easier to read than "1/2" in a recipe or a measure (MDN). The OpenType `frac` feature turns every digit-slash-digit sequence into a fraction.
- **Trade-off.** Applied to a whole paragraph, it also rewrites dates and scores, so each fraction needs its own element. It only works in a face that has `frac`.
- **Clash.** `font-variant-numeric` also carries tabular and oldstyle figures. Give the fraction its own declaration after any `font` shorthand, which resets the property.

### The fallback stack

Record: `vault.font-stack`.

- **Why.** With no generic family at the end, a sans face that fails to load falls back to the browser's default serif (MDN). A close fallback also makes the jump smaller when the web font arrives (Latin 2019).
- **Trade-off.** An unusual face has no close system match, so the fallback is a compromise.
- **Clash.** `vault.type-size` matches the fallback's x-height with `font-size-adjust`, and `vault.font-display` sets how the swap happens.

### Fluid type that still zooms

Record: `vault.fluid-zoom`.

- **Why.** Zoom does not enlarge a size set in `vw` alone, which is WCAG failure F94. The more a size depends on the viewport, the less zoom can do (web.dev 2025). Keeping the maximum at 2.5 times the minimum or less lets zoom still double the text.
- **Trade-off.** A smaller range means headings grow less between phone and desktop.
- **Clash.** `vault.fluid-type` sets the `clamp()` form and a maximum at least twice the minimum; this record caps it at 2.5 times. `vault.type-size` sets the minimum, and `vault.reflow` checks the viewport meta's own zoom limit.

### Line height without units

Record: `vault.leading-unitless`.

- **Why.** A unitless line height is passed down as a ratio, so each child works out its own line height from its own font size. A length or percentage is passed down as a fixed number, which squashes larger text inside it (MDN).
- **Trade-off.** None known.
- **Clash.** `vault.type-leading` sets the number, and this record only its form.

### Text spacing overrides

Records: `vault.text-spacing`, `vault.text-spacing-reveal`.

- **Why.** Some readers, including many with dyslexia or low vision, set wider line, paragraph, letter and word spacing with their own style sheet. WCAG 1.4.12 asks that nothing is lost when all four are set at once (F104: no clipping, no overlap).
- **Trade-off.** Boxes that are a fixed height, or that truncate their text, have to grow instead, which can make card rows uneven.
- **Clash.** It adds a pass with the spacing applied to the checks `vault.reflow` already makes.

### One space between sentences

Record: `vault.sentence-space`.

- **Why.** HTML already collapses any run of spaces to one, and current type guidance asks for one space (Butterick; Rutter 2.1.4). Forcing a wider gap with `&nbsp;` also stops the line from breaking there.
- **Trade-off.** None.
- **Clash.** None known.

### Outlined text

Record: `vault.text-stroke`.

- **Why.** The stroke is centred on the letter's outline and by default drawn over the fill, so its inner half eats into the letter. With `stroke fill` order, the letter keeps its shape.
- **Trade-off.** Half the stroke now sits behind the fill, so it has to be twice as wide to look the same.
- **Clash.** None known.

## Forms

### One answer or several

Record: `vault.choice-control`.

- **Why.** A round radio tells a visitor that picking one clears the others, and a square checkbox that each stands alone; the HTML radio group enforces the one-answer case (GOV.UK, USWDS, Atlassian).
- **Trade-off.** A long one-answer list may suit a select box better than radios; the record allows either.
- **Clash.** `vault.carry-select` decides how the selected state shows; this record only picks the control.

### A partly checked group

Record: `vault.mixed-check`.

- **Why.** A group checkbox that shows checked or clear when only some of its group are lies about the group; the mixed dash says "some" (Apple HIG, Atlassian). HTML gives native checkboxes the state and exposes it to screen readers.
- **Trade-off.** The state has no HTML attribute, so it needs script on load and on every change; a server-rendered page without script shows it clear.
- **Clash.** None known.

### Paste is never blocked

Records: `vault.auth-paste`, `vault.field-paste`, `vault.auth-paste-look`.

- **Why.** In a sign-in step, blocking paste or password managers forces a visitor to remember and retype, which WCAG 2.2 SC 3.3.8 fails unless another way in exists. Elsewhere people paste addresses and references they hold in other places (GOV.UK, USWDS).
- **Trade-off.** A confirm-email field loses some of its point when the visitor can paste their typo twice; USWDS suggests a verification link instead.
- **Clash.** `vault.field-paste` yields to `vault.auth-paste` inside a sign-in step.

### Password fields load empty

Record: `vault.password-empty`.

- **Why.** A prefilled password sits in the page source and lets anyone at the device in (Apple HIG); the password manager fills it for the visitor who owns it.
- **Trade-off.** None known.
- **Clash.** `vault.auth-paste` keeps password-manager fill working.

### A choice never moves the visitor on

Record: `vault.on-input`.

- **Why.** A visitor arrowing through radios or a select box, or a screen reader reading the options, changes the value at every step; a page that submits or jumps on change acts before they have chosen (WCAG 2.2 SC 3.2.2, USWDS).
- **Trade-off.** A one-question-at-a-time quiz or a filter that updates results in place feels quicker; updating the shown results is allowed, and moving on needs a button or a warning before the control.
- **Clash.** None known.

### Controls take the page font

Record: `vault.control-font`.

- **Why.** Browsers give controls their own small system font, so a form set in the page's typeface switches face inside every field (MDN; Comeau).
- **Trade-off.** None for the face; a project may deliberately set a different face on its controls, which its rules file says.
- **Clash.** The project's type records set the face and size; this record only stops the browser's default reaching the field.

### The platform caret

Record: `vault.caret-shape`.

- **Why.** The caret's shape follows the platform's convention and, on some, the editing mode; a visitor knows it from every other field.
- **Trade-off.** The property is Chrome-only and experimental as read, so a non-default shape would show in one browser.
- **Clash.** None known.

### Text areas stay resizable

Record: `vault.textarea-resize`.

- **Why.** A visitor writing more than the box shows drags it taller to read back what they wrote (web.dev); `resize: none` takes that away.
- **Trade-off.** Sideways resizing can break a layout, so the block direction alone is enough; iOS Safari shows no handle at all, where a box that grows with its text serves better.
- **Clash.** None known.

### Editing does not re-wrap

Record: `vault.edit-wrap`.

- **Why.** `pretty` and `balance` choose breaks by looking at later lines, so typing can move words on lines above the caret; `stable` exists for editable text (CSS Text 4). The property inherits, so a page-wide `pretty` reaches every field.
- **Trade-off.** None for editable text; the reading text keeps `pretty`.
- **Clash.** None known.

### Each field brings up its keyboard

Record: `vault.field-keyboard`.

- **Why.** On a phone the field's `type` or `inputmode` picks the keyboard: `@` for email, digits for a phone number or a code (HTML spec; GOV.UK; Baymard).
- **Trade-off.** `type="number"` brings digits, but a scroll can change its value and a wrong entry gets little feedback, so GOV.UK keeps it out unless research shows a need; whole numbers and codes take `inputmode="numeric"` on a text input.
- **Clash.** None known.

### Fields name their purpose

Record: `vault.autocomplete`.

- **Why.** A field that names its purpose lets the browser fill it and lets assistive tools label it, sparing visitors who struggle to type or remember (WCAG 2.2 SC 1.3.5).
- **Trade-off.** None for fields about the visitor; fields about anything else are out of scope.
- **Clash.** None known.

### The Enter key names its action

Record: `vault.enter-key`.

- **Why.** The phone keyboard's Enter key can read "Next", "Done", "Go", "Send" or "Search", so a visitor knows whether pressing it moves on or sends the form (HTML spec; web.dev).
- **Trade-off.** The label is a hint; the page must still make Enter do what it says.
- **Clash.** `vault.enter-submits` decides what Enter does; this record names it.

### Sliders start where reading starts

Record: `vault.slider-direction`.

- **Why.** People expect the lowest value at the reading start, and a native range mirrors itself in a right-to-left page (HTML rendering spec; Atlassian; Apple HIG).
- **Trade-off.** A drawn slider must mirror its fill and arrow keys by hand.
- **Clash.** Vertical sliders are left open: the HTML spec puts their lowest value at the top in a left-to-right page, Apple HIG at the bottom.

### Enter submits the form

Record: `vault.enter-submits`.

- **Why.** Visitors press Enter to send a search or a short form; HTML does it when the form has a submit button that is not disabled, or one text field and no button.
- **Trade-off.** A disabled submit button, a `div` styled as a button, or a form built without `form` silently loses Enter.
- **Clash.** None known.

## Text

### Curly quotes and apostrophes

Record: `vault.prose-quotes`.

- **Why.** Printed quotation marks were always curly; straight ones are a typewriter economy, and Unicode names the curly characters as the preferred quotes and apostrophe for English (Butterick; Unicode NamesList).
- **Trade-off.** Authors type straight quotes, so a build step has to curl them, and a careless one turns a word-initial apostrophe (’70s) into an opening quote; the script checks for that too.
- **Clash.** `vault.code-quotes` and `vault.prime-marks` hold the exceptions: a smart-quote step must leave code and measurement marks alone.

### Straight quotes in code

Record: `vault.code-quotes`.

- **Why.** A quote in code is syntax: curled, the copied command or snippet no longer runs (Butterick).
- **Trade-off.** None worth weighing; code set in a text face may look plainer than the prose round it.
- **Clash.** Wins over `vault.prose-quotes` inside `code`, `pre`, `kbd` and `samp`.

### Prime marks

Record: `vault.prime-marks`.

- **Why.** A curly quote after a number reads as a quotation; the prime and double prime are Unicode's characters for feet, inches, minutes and seconds (Unicode NamesList).
- **Trade-off.** Many professional faces lack the primes, so Butterick prefers straight quotes as the reliable mark; the record takes primes only where the face draws them, which the script can check from the font's character map.
- **Clash.** An exception to `vault.prose-quotes`.

### Dashes

Records: `vault.dashes`, `vault.dash-glyphs`.

- **Why.** Hyphen, en dash and em dash each have their own job, and a hyphen standing in for a dash reads as a joined word (Butterick).
- **Trade-off.** Whether a mark joins a range or breaks a sentence is a reading of meaning, so the type critic answers it, not a script; spaced or flush em dashes are a house choice, kept consistent.
- **Clash.** The minus sign is `vault.math-signs`', not a dash.

### Times and minus signs

Record: `vault.math-signs`.

- **Why.** The SI Brochure allows only × between numbers, and the hyphen-minus is a generic stand-in that Unicode gives the minus sign − as the dedicated alternative; the letter x and the hyphen sit at the wrong height and width beside figures.
- **Trade-off.** Butterick allows the en dash as a minus in light arithmetic; the record asks for − because a screen reader and a search both read it as minus.
- **Clash.** None known.

### Leading zero

Record: `vault.leading-zero`.

- **Why.** A bare decimal marker is easily missed, so .5 can be read as 5; the SI Brochure always puts a zero before it.
- **Trade-off.** Some sports and finance conventions write .300 averages or bare decimals; a project rules file can keep them.
- **Clash.** None known.

### Numbers in the locale format

Record: `vault.locale-numbers`.

- **Why.** Countries group and separate digits differently (1.234,5 in German, 1,23,456 in India), and the locale data every browser carries, CLDR through `Intl.NumberFormat`, already knows each one (Atlassian; MDN; CLDR).
- **Trade-off.** A site in one language only needs that language's format; a number formatted from the visitor's browser locale rather than the page's can mix formats on one page.
- **Clash.** Years, phone, order and account numbers are identifiers and take no grouping.

### First weekday and hour cycle

Record: `vault.week-hour`.

- **Why.** A week starts on Monday in Britain, Sunday in the United States and Saturday in Egypt, and the clock runs 12 or 24 hours by locale; CLDR holds both, read through `Intl.Locale` (MDN).
- **Trade-off.** `getWeekInfo` reached Baseline only in July 2026, so older browsers need a fallback table; a scheduling product may let the visitor choose instead.
- **Clash.** A visitor's own setting beats the locale default.

### Headings and lists are markup

Records: `vault.heading-markup`, `vault.list-markup`, `vault.heading-markup-div`.

- **Why.** Size, weight and bullets tell a sighted reader where a section starts and what belongs to a list; screen reader users move by headings and hear a list's length only from the markup, so WCAG 2.2 SC 1.3.1 asks that the structure be in the code (H42, H48).
- **Trade-off.** A heading element brings its level into the outline, so a card title has to fit the page's heading order; a styled list may need its markers redrawn with `::marker`.
- **Clash.** None known.

### The language of each passage

Records: `vault.lang-parts`, `vault.lang-parts-look`.

- **Why.** A screen reader switches voice, and the browser hyphenates, only by the declared language; CSS forbids automatic hyphenation of text whose language is unknown (WCAG 2.2 SC 3.1.2; CSS Text 3; webtypography.net 2.4.5).
- **Trade-off.** Marking every borrowed word is noise; WCAG excepts names, technical terms and words the surrounding language has taken in.
- **Clash.** None known.

### Capitals set by style

Record: `vault.typed-case`.

- **Why.** CSS asks that the true case live in the source: a restyle can then drop the capitals, copied text keeps its case, and case mapping follows the language (German ß, Turkish i).
- **Trade-off.** Chromium 149 exposes the transformed capitals to its accessibility tree too, so CSS capitals do not by themselves fix screen reader spelling; the gain is in the source, copying and language.
- **Clash.** `vault.dna-caps-label` decides whether a label is in capitals at all; this record only decides how.

### Underlines skip descenders

Record: `vault.skip-ink`.

- **Why.** An underline through descenders blurs the letters; the browser's `auto` default breaks it round them (MDN; Typography Handbook).
- **Trade-off.** `auto` does not skip in some CJK faces, where `all` (Baseline only since May 2026) is needed.
- **Clash.** `vault.link-style` sets the underline's offset and thickness; this record only keeps the skip.

### The hyphenation character

Record: `vault.hyphen-char`.

- **Why.** The browser picks the line-end hyphen from the content language's conventions, so overriding it rarely helps (MDN).
- **Trade-off.** Depends on `lang` being declared (`vault.lang-parts`).
- **Clash.** None known.

### The browser's spelling mark

Record: `vault.spelling-mark`.

- **Why.** Visitors know the browser's wavy underline as "misspelt" from every other site; a custom checker drawing the same mark through `spelling-error` keeps that meaning (MDN).
- **Trade-off.** Spellcheck marks names, codes and identifiers as errors, so those fields turn it off.
- **Clash.** None known.

### Right-to-left mirroring

Record: `vault.rtl-sides`.

- **Why.** In a right-to-left language text starts at the right and the layout mirrors; direction set in the markup and sides written as logical properties make that happen without a second stylesheet (W3C i18n; web.dev; Apple HIG).
- **Trade-off.** Items that must stay fixed regardless of direction (a media player's controls, a map) keep physical sides.
- **Clash.** Agrees with `vault.no-justify`, which decides justification; this record decides the sides.

### Digits in right-to-left text

Records: `vault.rtl-digits`, `vault.rtl-digit-order`.

- **Why.** The Unicode bidirectional algorithm keeps every run of digits left to right inside right-to-left text, with no markup needed in most cases (UAX #9); a number's digits never reverse (Apple HIG).
- **Trade-off.** Punctuation between numbers (phone numbers, ranges) can still reorder, which `bdi` or `dir` on the number fixes.
- **Clash.** None known.

### White space

Records: `vault.white-space`, `vault.kept-breaks`.

- **Why.** HTML collapses spaces and line breaks so source can be wrapped freely; code, verse and addresses carry meaning in their breaks and keep them (CSS Text 3; MDN).
- **Trade-off.** Preserved white space does not reflow, so code blocks need horizontal scroll on a phone.
- **Clash.** None known.

### Ruby annotations

Record: `vault.ruby-position`.

- **Why.** Japanese typography puts ruby above horizontal text and right of vertical text, and below "very rare" (W3C JLREQ §3.3.4); the browser default already does so.
- **Trade-off.** Two-level annotation (reading and meaning) needs `alternate` or `under` for the second level.
- **Clash.** None known.

## Images and media

### Icons are vector

Records: `vault.icon-vector`, `vault.flat-art-vector`.

- **Why.** An SVG icon stays sharp at every size and screen density from one file; a PNG icon needs a file per size and blurs between them (Apple HIG Icons; web.dev, Icons).
- **Trade-off.** Art with texture, shading or photographic detail is heavier as SVG than as a raster file, so it stays raster.
- **Clash.** `vault.stroke-weight` sets the icon's line weight; this record only sets its file format.

### Favicon and touch icon

Record: `vault.favicon`.

- **Why.** Browsers choose a tab icon from the `rel="icon"` links by type and size, and iOS reads only `apple-touch-icon` for a home-screen icon, so a site needs both; GOV.UK's head is the tested set.
- **Trade-off.** Three files to keep in step with the logo; an SVG favicon can carry a dark-mode variant, which the ICO cannot.
- **Clash.** None known.

### Pinch zoom anchors between the fingers

Record: `vault.pinch-anchor`.

- **Why.** A pinch reads as grabbing a point, so the zoom has to grow from the spot between the fingers; zooming about the image's centre slides the part the visitor reached for away (rauno.me, "Invisible Details of Interaction Design").
- **Trade-off.** A custom zoom has to claim the gesture with `touch-action`, which takes the page's own zoom away on that surface; keeping the surface to the image keeps it everywhere else.
- **Clash.** `vault.reflow` keeps the page's own zoom, a WCAG floor, and wins.

### Hard-edged images scale without smoothing

Records: `vault.image-scaling`, `vault.pixel-image-kind`.

- **Why.** The browser smooths an enlarged image, which suits a photo but blurs pixel art and the squares of a QR code; `pixelated` keeps each pixel square (MDN, `image-rendering`).
- **Trade-off.** `pixelated` at a non-whole scale shows uneven pixels; `crisp-edges` is the closer fit for line drawings but only reached every browser in May 2026, so it waits until Baseline widely available.
- **Clash.** None known.

### Right-to-left icons

Records: `vault.rtl-icons`, `vault.rtl-fixed-icons`.

- **Why.** Readers of a right-to-left language read forward as leftward, so arrows, back and next, and icons of text must flip to keep their meaning; marks, clocks and objects held in the right hand look the same everywhere (Apple HIG; Material Design 1).
- **Trade-off.** Each icon is a judgment, and a flipped set doubles the icons to keep.
- **Clash.** Apple says to flip any control showing progress; Material keeps media playback buttons and their progress bar left-to-right as tape direction. Material is the more specific rule, so the record follows it for media.

### Right-to-left images

Record: `vault.rtl-images`.

- **Why.** A mirrored photograph shows reversed text, a wrong-handed person and a false place, and can breach its licence (Apple HIG).
- **Trade-off.** An image whose layout points the reader's way, a figure looking toward the copy, may need a second version.
- **Clash.** None known.

### Right-to-left image order

Record: `vault.rtl-image-order`.

- **Why.** An ordered set is read in the page's direction, so in right-to-left the first item sits at the right (Apple HIG); flex and grid in source order do this by themselves.
- **Trade-off.** None worth naming; an unordered set may stay as it is.
- **Clash.** `vault.visual-order` keeps source order, which this record relies on.

### Captions, transcripts and audio description

Records: `vault.media-alternatives`, `vault.video-captions`.

- **Why.** A deaf visitor needs captions, a blind visitor needs what is only shown described, and a transcript serves both and search engines. WCAG 2.2 sets it at level A for prerecorded media (1.2.1–1.2.3) and AA for live captions and audio description (1.2.4, 1.2.5).
- **Trade-off.** At level A a full transcript can stand in for audio description, but AA asks for the description itself.
- **Clash.** None known.

### Flashing stays below three a second

Record: `vault.flash-limit`.

- **Why.** Flashes faster than three a second over a large part of the screen can trigger seizures, so WCAG 2.2 SC 2.3.1 bars them at level A, for all content on the page.
- **Trade-off.** Strobe effects, rapid cuts and lightning are out unless small or slowed.
- **Clash.** None: `vault.pause` and `vault.reduced-motion` stop or calm motion but do not make a flash safe, so this applies under both.

### Space plays and pauses

Record: `vault.space-plays`.

- **Why.** Visitors expect Space to play and pause (Apple HIG), and the browser's own player does this while it has focus.
- **Trade-off.** A page-wide Space shortcut would steal Space from scrolling and from buttons, so the key works only while the player has focus.
- **Clash.** `vault.keyboard` makes the player reachable; this record sets the key once it is reached.

### Content images are elements

Records: `vault.content-image`, `vault.background-image-role`.

- **Why.** A screen reader cannot read a CSS background image, and no alt text can be attached to one, so an image the visitor needs must be an element (WCAG technique F3; MDN).
- **Trade-off.** Cropping with `object-fit` replaces `background-size: cover`, with the same result.
- **Clash.** `vault.decorative-alt` covers the other direction, decoration as `alt=""` or a background; together they settle every image.

