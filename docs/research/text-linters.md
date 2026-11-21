# design-vault#245 (map #243): open-source text linters for the house's rules on words on the page

Date: 15 Oct 2026.

**Question.** Which open-source text and content linters (Vale, textlint, alex, write-good, the readability-score packages, retext) can check the house's rules about words on the page? For each rule: can the rule format of the linter express it, or does the rule need DOM context (which element, which page) that a prose linter does not see? Give licence, maintenance and download figures for each tool.

## 1. The rules under test (read from the repo)

Source: `plugin/skills/design-critique/references/first-visit-trust.md` (80 lines, read in full).

- **Item 7.** "A contact route on every page: the email address in full as its own link text, a phone number only where the owner answers it, labelled "Telephone:"" (`first-visit-trust.md:20`).
- **Item 9.** "A privacy note at the form" when a form collects personal data (`:22`).
- **Item 11.** "Task text (navigation, headings, contact, work rows, summaries) in sentences of at most 25 words, technical terms explained once". A specialist's argument may be longer (`:24`).
- **Item 12.** "Identity on every page: the name, a one-line bio, a link home" (`:25`).
- **Item 13.** "a dated CV, the newest work's date, this year's copyright" (`:26`).
- **Field budget.** Required fields: name, email, message for a plain enquiry; "At most one or two optional fields, each labelled optional" (`:33-34`).

Source: House DNA `never` lines, `data/gallery.json` (13 lines, from `jq '.. | objects | select(has("never")) | .never'`). The lines about words:
- "Emoji bullets; lorem ipsum."
- "Taste: copy using "Unlock", "Elevate" or "Seamless"."
- Inside the "template chrome" line: "meta strings joined by middle dots (A · B · C); labels built as "WORD — fragment"; ... "→" appended to link and button text"; "a tracked-out all-caps eyebrow"; "all caps for labels".
- "Fabricated proof, such as an invented testimonial" (judged by `vault.proof`, not by text form).

Source: the copy bans that the gate critics receive. `plugin/skills/design-round/SKILL.md:214` defines them: every line of the **project's** rules file (and of a voice guide it sends copy to) that bans or limits what copy says, "banned words and strings, voice "never" lists, and its honesty, urgency, pricing and claims rules", pasted verbatim into `gate/copy-bans.md`. The vault itself holds no list. The bans are per project. For Manta, the list is `docs/brand/brand-sheet.md` §11 in the mantahostels repo (its *Banned tells*), per `~/mantahostels/docs/copy/outbound-messaging.md:5`.

## 2. Existing in-house copy linters (mantahostels, not the vault)

- `~/mantahostels/scripts/check-website-copy.js` (225 lines) with `scripts/lib/website-copy.js` and `scripts/lib/copy-extract.js`: a regex gate on "the half of [§11's] list a regex can judge" in `app/` source strings (#858). Its header says why the other half is not scanned: "False ranges is the one that looks scannable and is not: its only lexical shape, "from X to Y", is what a place blurb says about geography ... so a pattern would fire mostly on correct copy. False agency is the same problem in the other direction" (`website-copy.js:8-17`). It names "FOUR MORE MISSES, each the price of a false positive refused" (#2812). It also says: "A false positive is almost always the first [where copy lives]; a missed tell is almost always the second [what is banned]".
- `~/mantahostels/scripts/lint-correspondence.js` (382 lines) + `scripts/lib/correspondence-rules.js` (81 lines): the email lint of `docs/copy/outbound-messaging.md`.



## 3. The trial on record: false positives from subtractive copy linting

`docs/research/mmm-infra-photos-to-reply.md:104` (S9): the session drafted a client reply with mantahostels' outbound-messaging rules and lint. "The lint failed his own sentence on 'I think'." The founder's sentence was an opinion with no ask.

The tickets that this filed show the cause (read with `gh issue view`, all CLOSED):
- mantahostels#3665: the lint FAILed "i think" **anywhere**, but rule 14 bans it only "in front of the ask". So the lint was wider than its own rule. The cited evidence (Oba, Berger & Boghrati, J. Consumer Psychology 2026) finds personal hedges ("I think") made a speaker **more** persuasive. The rulebook now says "a single "could you" ... is fine ... and so is "I think" on an opinion" (`outbound-messaging.md:294`).
- mantahostels#3663: "the new lint fails [semicolons] and the rulebook recommends them". A second false positive of the same shape.
- mantahostels#3667: "Which of rule 15's machine-writing tells does evidence support, given that readers' own cues for AI text are shown to be flawed".
- The rulebook now says: "A clean lint run finds no known tell, and never shows that a message reads human" (`outbound-messaging.md:324`).

**What this shows.** Two of two recorded false-positive episodes came from a word ban applied **without its context** (position relative to the ask; a recommended punctuation mark). Neither fault was in the matching engine. Both were in the scope of the rule. A third-party linter does not change this: Vale, textlint and retext also match tokens without knowing "in front of the ask". The trial is evidence against **context-dependent** bans in any lint. It is weak evidence against **context-free** bans ("Unlock", "lorem ipsum", "→" at the end of link text), which have one meaning in any position.

## 4. Vale

**Facts (primary sources).**
- Repo `vale-cli/vale` (was `errata-ai/vale`; GitHub redirects). Licence MIT. Not archived. Last push 14 Oct 2026. 6,238 stars (`gh api repos/vale-cli/vale`).
- **18 releases in the last 12 months**, v3.13.0 (22 Oct 2025) to v3.24.0 (1 Oct 2026) (`gh api repos/vale-cli/vale/releases`). The cadence in Aug–Oct 2026 is about one release each week.
- **Runtime shape.** One static Go binary. The v3.24.0 release assets are 12.3–13.3 MB archives for Linux, macOS and Windows on x86-64 and arm64. It needs no Node and no Python. `vale_3.24.0_Linux_64-bit.tar.gz` has 89,586 downloads two weeks after release (release asset `download_count`). Install figures through wrappers: PyPI `vale` (a third-party wrapper by daniperez; "Vale as such is not included in this package but downloaded the first time you execute `vale`") has 92,767 downloads last week (pypistats); npm `@vvago/vale` ("Download pre-built vale binaries") has 72,617 downloads last week. Both wrappers **download a binary at first run**. For the vault plugin (it runs from its install folder with no `node_modules`, inventory §5 item 4) this is the same packaging problem that stopped axe-core in #163, in a different form: a 13 MB binary per platform to fetch and pin, or a network download at first use.
- **Rule format.** YAML rules, one per file, each `extends:` one check type: existence, substitution, occurrence, repetition, consistency, conditional, capitalization, metric, readability, spelling, sequence, script (`vale-cli/vale.sh` `docs/checks/`). `script` rules run Tengo with only the `text`, `fmt` and `math` modules: "We don't want to enable the `os` module because of the security" (`internal/check/script.go:92-96`). So **a Vale rule cannot read the clock**; "this year" must be written into the rule by the caller.
- **HTML input.** HTML5 is built in. Vale skips `script`, `style`, `pre`, `noscript`, `iframe` and inline `code`/`tt`/`kbd`/`samp`; it lints `alt` text and `<meta name="description">` as prose (`docs/formats/html.md`). It reads the **file**, not a rendered page. A candidate that builds its text with JavaScript must first be dumped (for example Playwright `page.content()`, which the vault scripts already drive).
- **Scopes (the DOM question).** A rule names a scope. Built-in markup scopes: `heading` (`heading.h1`…), `table.header`, `table.cell`, `list`, `blockquote`, `alt`; inline scopes `link`, `code`, `strong`, `emphasis` (v3.17.0+); prose units `sentence`, `paragraph`, `summary`, `raw` (`docs/topics/scopes.md`). **Since v3.21.0 (9 Sep 2026) a `doc(...)` term selects elements by CSS selector** (Selectors Level 4: `>`, `+`, `~`, `:not()`, `:has()`, `nth` family, attribute selectors, plus `:contains()`). "A selection that matches nothing in a file still produces its block, empty, on line one. That is how a rule reports that a section is missing: an `occurrence` rule with `min: 1`" (`scopes.md`, Selections; v3.21.0 release notes). So Vale now sees **which element** text is in. This feature is about five weeks old; its sibling-combinator and `:is()` support came in v3.23.0 (25 Sep 2026).
- **Limits that stay.** (a) Vale lints one file at a time, so "on every page" means "run on each page file", which is fine; it cannot compare pages. (b) A selection "with no prose in it ... selects fine and then has nothing to lint" (`scopes.md`). So Vale cannot count `<input>` elements or read the `required` attribute as data. It can only use them inside a selector. (c) `metric` variables are prose counts (words, sentences, syllables, headings, lists, readability formulas, `sentence_length_sd`); there is no "count of elements matching X" variable (`docs/checks/metric.md`). (d) `:contains()` "matches any part of the text, ignoring case".
- **Readability in Vale.** `metric` with `scope: sentence` and `formula: words`, `condition: "> 25.0"` expresses item 11 directly. Built-in score variables (v3.23.0+): ARI, Coleman–Liau, Dale–Chall, Flesch–Kincaid, Flesch reading ease, Gunning fog, LIX, SMOG.
- **Ready-made styles.** `vale-cli/packages` (MIT, pushed 28 Sep 2026) lists packages such as Microsoft, Google, write-good, alex, proselint, Readability, Joblint. The write-good and alex styles are Vale ports of those word lists.

**Ready-made Vale styles that touch the house rules** (`vale-cli/packages` `library.json`, read in full; 29 entries):
- `AiTells` (krishnasunkam/vale-ai-tells, MIT, created 13 Jul 2026, 1 star): 17 rules (em dash, "serves as", "not just X, but Y", clichés, `LinkText` "click here"). Its README says each rule was "scored ... against a labeled benchmark", but the public `bench/` is "a small synthetic version". No figures are published. Weak evidence.
- `ai-tells` (tbhb/vale-ai-tells, MIT, created 2 Dec 2025, pushed 11 Oct 2026, 118 stars). Not read past its listing.
- `Readability` (vale-cli/readability): ARI, Coleman–Liau, Flesch–Kincaid, Flesch reading ease, Gunning fog, LIX, SMOG.
- `A11y` (jdkato/a11y, created 24 Sep 2026): "alt text, link text, heading structure ... from the parts of WCAG 2.2 that live in the text".


## 5. textlint

- Repo `textlint/textlint`, MIT, pushed 15 Oct 2026, 3,201 stars. npm `textlint` 15.8.0 (1 Aug 2026), **13 releases in the last 12 months**, **225,632 downloads last week**; `@textlint/kernel` 360,587 (npm registry and downloads API). Needs Node ≥ 20.18.0; 24 direct dependencies.
- **Rule format: a JavaScript function** over textlint's AST (TxtAST). So a rule can hold any logic, the clock included. This is the most expressive format here, and also the least "linter-like": a textlint rule for a DOM rule is a hand-written script with textlint's reporter around it.
- **HTML needs `textlint-plugin-html`** (MIT, 1.0.1 of 9 Aug 2024, **0 releases in 12 months**, 9,248 downloads last week, 26 stars, 4 open issues). It parses with `rehype-parse` and maps only `p`, `ul`/`ol`, `li`, `q`/`blockquote`, `code`, `hr`, `br`, `em`, `strong`, `a`, `img`, `h1`–`h6` to TxtAST types. Every other element keeps its tag name as its node type ("other case, return original tagName"; `src/mapping.ts`, `src/html-to-ast.ts`). So a rule can find a `form` or `footer` node, but the plugin's own comment says "Almost rule should not handle this node" (issue #19). Static HTML only.
- Relevant ready-made rules: `textlint-rule-sentence-length` 5.2.1 (MIT, 3 Jan 2026, 138,321/week). It counts **characters, not words**: "`max` default: 100. The total number of characters allowed on each sentences" (README). So the house's 25-word line needs a custom rule. `textlint-rule-prh` 6.1.0 (MIT, 20 Apr 2025, 272,707/week): a YAML word-substitution list (built for Japanese proofreading). `textlint-filter-rule-allowlist` 4.0.0 (40,806/week, last release 1 Jul 2021) to allow named exceptions. `textlint-rule-write-good` 2.0.0 (11,976/week, last release 6 Jun 2021) and `textlint-rule-alex` 5.0.0 (3,491/week, last release 4 Feb 2024) wrap those tools.
- Much of the textlint rule ecosystem is Japanese (`textlint-rule-max-ten`, 126,567/week, counts Japanese commas; `textlint-rule-preset-ja-technical-writing`, 108,476/week). The download totals above are driven by that user base.

## 6. alex

- Repo `get-alex/alex`, MIT, last push 27 Nov 2024 (a README integration link). npm `alex` 11.0.1 of **18 Aug 2023; 0 releases in 12 months**; 35,135 downloads last week.
- It is retext-equality + retext-profanities behind a CLI. It reads plain text, HTML, MDX and Markdown.
- **It cannot carry a house word list.** Its config takes `allow` / `deny` as arrays of its own rule ids, `noBinary`, and `profanitySureness` (README). There is no field for a custom banned word.
- The README's `profanitySureness` table rates each word by "Use as a profanity" against "Use in clean text". That is the tool's own admission that its words are ambiguous in context, and that the user must pick a false-positive trade-off.
- **No house rule is about inclusive or profane language.**

## 7. write-good

- Repo `btford/write-good`, MIT, last push 10 Mar 2025 (a README link). npm `write-good` 1.0.8 of **16 Feb 2021; 0 releases in 12 months**; 74,477 downloads last week.
- The README calls it a "Naive linter for English prose". Checks: passive voice, lexical illusions (a repeated word), "so" at sentence start, "there is/are" at start, weasel words, adverbs, wordy phrases, clichés, E-Prime. A `checks` option takes a custom check set (the `schreib-gut` example), so a word list is possible.
- Plain text and Markdown in; no HTML element context. Its passive, adverb and weasel checks are style advice that **no house rule asks for**. They are the same subtractive kind of rule that failed "I think" in §3.

## 8. retext (unified)

- Repo `retextjs/retext`, MIT, pushed 4 Feb 2025, 0 open issues. npm `retext` 9.0.0 of **6 Sep 2023; 0 releases in 12 months**; 5,116,924 downloads last week. That figure is mostly transitive (retext is a unified dependency of other tools; `unified` itself has 62.8 M/week), so it does not measure direct use.
- Plugins checked: `retext-readability` 8.0.0 (Sep 2023, 3,740/week), `retext-simplify` 8.0.0 (Sep 2023, 7,465/week), `retext-equality` 7.1.0 (May 2024, 43,636/week), `retext-profanities` 8.0.0 (Sep 2023, 42,784/week), `retext-emoji` 9.0.0 (Sep 2023, 9,794/week), `retext-intensify` 7.0.0 (Sep 2023, 2,444/week). **None has a release in the last 12 months.**
- **Rule format: a JavaScript unified plugin** over nlcst (a sentence/word tree). HTML reaches it through `rehype-retext` 5.0.1 (2 Apr 2025, 39,928/week), which converts the HTML tree to nlcst. The element names do not survive into nlcst, so a retext plugin does not know which element a word is in. A rule that needs the element must be written on the HTML tree (hast), which is then a DOM script.
- No retext plugin takes a generic banned-word list. A house list needs a small custom plugin (`nlcst-search`).

## 9. Readability-score packages

| Package | Registry | Licence | Latest | Releases in 12 months | Downloads |
|---|---|---|---|---|---|
| `text-readability` | npm | ISC on npm; the linked repo `clearnote01/readability` says MIT | 1.1.1, 6 Mar 2025 | 0 | 20,401/week |
| `readability-scores` | npm | MIT | 1.0.8, 15 May 2020 | 0 (repo pushed Oct 2022, 5 stars) | 1,077/week |
| `textstat` | PyPI | MIT | 0.7.13, 18 Feb 2026 (and 1.0.0a1, Nov 2025) | 4 | 259,820/week (pypistats) |
| `py-readability-metrics` | PyPI | MIT | 1.4.5, 2 Aug 2020 | 0 | 5,544/week |
| `readability` (andreasvc) | PyPI | Apache-2.0 (classifier) | 0.3.2, 14 Jan 2025 | 0 | 4,374/week |

- These are **libraries that return scores**, not linters. They have no rule format, no element context and no pass/fail.
- The house rule (item 11) is **not a readability formula**. It is a word count per sentence (≤ 25) on task text.
- They count, and their counts are coarse. Example: `textstat`'s `count_sentences` splits on `[.!?]` and **drops every "sentence" of 2 words or fewer** from the count (`textstat/backend/counts/_count_sentences.py`). That is wrong for UI text, where nav labels and buttons are 1–2 word "sentences" with no full stop. A segmenter that does not know element boundaries joins a heading, a nav label and a paragraph into one long "sentence" when they have no terminal punctuation between them.
- Readability formulas are known to be unstable on short texts (practitioner consensus; I did not find a primary study for texts under 100 words). UI copy is short.

## 10. Published evidence on false positives

- **Only one measured false-discovery rate was found for any prose linter.** Pacer, Suchow et al., "Linting science prose and the science of prose linting", SciPy 2016 (PDF at suchow.io, read: the evaluation and future-work sections). On an earlier corpus of professionally edited essays (Harper's, The New Yorker, The Atlantic): "Proselint's false discovery rate of 1 false positive to 10 true positives was 20× better than the next best tool, Microsoft Word, which had a false discovery rate of 2 false positives to 1 true positive". The same paper: "Applying these rules without consideration of the context will systematically introduce false positives." Proselint (BSD-3-Clause, PyPI 0.16.0 of 14 Nov 2025, 5,967/week) is not in the brief's tool list; it is named here only as the source of the figure.
- **No published false-positive rate was found for Vale, textlint, alex, write-good or retext.**
- **House evidence (§2, §3).** Three recorded cases, all in mantahostels: "I think" (mantahostels#3665) and semicolons (#3663) failed by a lint wider than its rule; and `website-copy.js` refusing to scan "false ranges" because the pattern "would fire mostly on correct copy". All three are the same fault: **a word ban whose rule depends on context** (position, purpose, meaning).

## 11. Per-rule list

Key: **linter** = a prose linter's rule format can express it; **DOM** = needs which element, an attribute, a count of controls, or computed style, that a prose linter does not see (Vale ≥ 3.21 `doc(...)` sees element *names and nesting* but not attribute values as data, controls, counts or CSS); **judgement** = a critic decides.

| Rule | Verdict | Why |
|---|---|---|
| Item 11: task text ≤ 25 words a sentence | **linter**, scoped by **DOM** | Vale `metric`, `scope: sentence`, `formula: words`, `condition: "> 25.0"`, narrowed with `doc(...)` to nav, headings, footer, list items. textlint needs a custom rule (its `sentence-length` counts characters). Which text is "task text" against "a specialist's argument" needs element marks or a judgement. "Technical terms explained once": **judgement**. |
| Item 7: email in full as its own link text | **DOM** | The check compares the `mailto:` `href` with the link's text. Vale can select `doc(a[href^="mailto:"])` but cannot compare an attribute value with the text. Vale also ignores URLs in prose (`docs/formats/html.md`); whether it ignores email addresses was **not verified**. |
| Item 7: "Telephone:" label on a phone number | **DOM** (linter possible, false-positive risk) | A regex rule ("a phone-shaped number not after `Telephone:`") is expressible in Vale (its engine, `regexp2`, has lookbehind). But a phone-number regex also fires on VAT and register numbers, which item 10 puts in the same footer. A `tel:` link read from the DOM has no such risk. |
| Item 12: name on every page | **linter** | Vale `occurrence`, `min: 1`, the owner's name as the token, run on each page file. Per-project token. |
| Item 12: link home on every page | **DOM** | Needs the `href` of a link (often a logo with only `alt`). |
| Item 12: one-line bio | **judgement** | |
| Item 13: this year's copyright | **linter**, year supplied by the caller | Regex `©\s*(\d{4}\s*[–-]\s*)?2026`. Vale cannot read the clock (Tengo `os`/`times` not enabled, `script.go:92-96`), so the caller writes the year into the rule. textlint can read the clock. A JavaScript-written year (`new Date().getFullYear()`) is seen only in a rendered dump. |
| Item 13: dated CV, newest work's date | **judgement** (DOM helps) | Which date is the newest work is content knowledge. |
| Item 9: privacy note at the form | **DOM** | Vale can write `occurrence` on `doc(form)` or `doc(section:has(form))` with token `(?i)privacy`, `min: 1`. But "a selection that matches nothing ... still produces its block, empty" (`scopes.md`), so the rule fires on every page **without** a form. The rule is conditional on a form that collects personal data (`input[type=email]`): a DOM fact. Whether the note meets UK GDPR Art. 13: **judgement**. |
| Field budget: ≤ 3 required, ≤ 2 optional, each labelled "optional" | **DOM** | Counts of `input`/`select`/`textarea`, the `required` attribute and the label text. No prose linter counts controls; Vale `metric` has no element-count variable for them. "Each other field names the action its answer changes": **judgement**. |
| DNA: "Unlock", "Elevate", "Seamless" | **linter** (warning only) | Vale `existence`, case-insensitive. Context risk is real: "unlock your locker with the app" is literal on a hostel page. The DNA line is a "Taste" line, P2 at most (`design-critique/SKILL.md:98`). Report, never gate. |
| DNA: lorem ipsum | **linter** | Context-free. No false-positive risk found. |
| DNA: emoji bullets | **linter**, partly **DOM** | Vale `existence`, `scope: list`, a leading `\p{So}`. An emoji drawn by CSS (`::before`, `list-style`) is not in the source text: **DOM** (computed style). Manta allows an emoji "carrying information in a badge or a legend": **judgement**. |
| DNA template chrome: middle-dot meta strings; "WORD — fragment" labels | **linter** | Regex on text. Context risk: Manta's §11 item 11 itself *prescribes* `·` to separate metadata halves, so the project's rules file can earn it back (`impeccable.md` "AI look" bans). |
| DNA template chrome: "→" appended to link and button text | **linter** (when typed), **DOM** (when drawn by CSS) | Vale `scope: link`, token `→\s*$`; a button needs `doc(button)`. A CSS `::after` arrow is invisible to a prose linter. |
| DNA template chrome: tracked-out all-caps eyebrow; all caps for labels; monospace for small labels; tinted near-black | **DOM** (computed style) | `text-transform`, `letter-spacing`, `font-family`, `color` are CSS. A prose linter sees caps only when they are typed. |
| DNA: one headline word accented in italic, bold or colour | **DOM**, partly linter | `em`/`strong` inside a heading can be selected (`doc(h1 em)`); colour is computed style. |
| DNA: fabricated proof | **judgement** | `vault.proof`. |
| Project copy bans (worked case: Manta brand sheet §11, 14 items) | lexical half **linter**; the rest **judgement** or **DOM** | Manta already lints items 1–5 and 10–13 with its own 225-line regex gate. Item 9 title-case headings: **linter** (Vale `capitalization`, `scope: heading`, `match: $sentence`, with exceptions for names). Item 8 boldface overuse ("one job per screen"): **DOM** (count of bold per viewport). Items 6 false ranges, 7 synonym cycling, 14 false agency: **judgement** (Manta's own header refuses 6 and 14 as regexes). Honesty, urgency, pricing and claims rules (design-round §4): **judgement**. |

**Count.** Of 19 rows: linter alone 5 (name, copyright, lorem ipsum, banned DNA words, chrome strings); linter scoped by DOM or partly DOM 4 (item 11, emoji bullets, arrows, headline accent); DOM 5 (email link text, link home, privacy note, field budget, CSS-drawn chrome); judgement 3 (bio, CV dates, fabricated proof); split 2 (project copy bans; Telephone label). **The rules that a pure prose linter settles are all short regexes over visible text.**

## Recommendation

1. **Do not adopt alex, write-good, retext or the readability-score packages for the house rules.** alex and write-good check things no house rule asks for, alex cannot take a house word list, and none of the five npm packages has had a release in 12 months. Confidence **85% (75%–95%)**.
2. **Put the DOM rules (items 7, 9, 12 link home, the field budget) and, with them, the two text rules a linter could also do (item 11 sentence length, item 13 copyright year) into one Playwright script on the existing substrate**, read from the rendered page by element. The inventory already marks them "all DOM-countable, all critic-only today". A rendered page also sees JavaScript-built text, which every static linter misses. Item 11 runs per element, so element boundaries end sentences. Confidence that this costs less and finds more than any linter here: **75% (60%–90%)**.
3. **For word lists (DNA words, chrome strings, a project's lexical bans), keep the list as data and run it in the same script on the rendered text of each element**, as Manta's `website-copy.js` does. Vale is the only tool worth a trial, if a project's list grows large: its YAML rules, `doc(...)` scopes and weekly releases fit the job. Against it: a 12–13 MB binary per platform outside the plugin's install folder (the same packaging problem that stopped axe-core in #163), and its element-selection feature is five weeks old (v3.21.0, 9 Sep 2026). Confidence that a hand list beats Vale for the vault today: **60% (45%–75%)**. This flips if a project wants to reuse public Vale styles (Microsoft, Google, AiTells) as they are.
4. **Lint only context-free bans, and report word bans as warnings (P2), not gate failures.** The three recorded house cases (§3, §10) are all context-dependent bans that a token match cannot scope. Confidence **80% (70%–90%)**.

No question for the founder comes out of this research: each point above is settled by a source or by the repo.

**Bound.** Read exhaustively: `first-visit-trust.md` (all 80 lines); the House DNA `never` lines (all 13, by `jq`); every hit of `copy ban|banned|bans` under `plugin/`; `mmm-infra-photos-to-reply.md` S9; mantahostels#3663, #3665, #3666, #3667 titles and #3665 in full; Manta brand sheet §11 banned-tells list (14 items, first 220 characters each); `website-copy.js` header; Vale docs `topics/scopes.md`, `formats/html.md`, `checks/script.md`, `checks/metric.md` in full; Vale `internal/check/script.go` imports; Vale release list for 12 months and v3.21.0 notes; `vale-cli/packages` `library.json`; textlint-plugin-html `mapping.ts` and the head of `html-to-ast.ts`; textstat `_count_sentences.py`; npm registry and downloads API, PyPI JSON and pypistats, and GitHub repo metadata for every tool named. Sampled only: the READMEs of alex, write-good, textlint-rule-sentence-length, textlint-rule-prh, vale-ai-tells (krishnasunkam) and the Vale PyPI wrapper (grep or head); the Pacer et al. paper (evaluation and future-work sections, by text extraction). Not read: Vale's `occurrence`, `existence`, `conditional`, `readability` check docs (downloaded, not read in full); tbhb/vale-ai-tells; the inside of Manta's `lint-correspondence.js`. Not verified: whether Vale ignores email addresses as it ignores URLs; how Vale blocks text in a bare `<div>`; any primary study of readability formulas on texts under 100 words (only practitioner sources found). Nothing was installed or run.
