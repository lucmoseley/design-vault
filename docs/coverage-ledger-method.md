# How the coverage ledger is built

`docs/coverage-ledger.json` lists every web design decision the outside sources name, and whether the house covers each.

## 1. Sources

Six families, each source with a code. The ledger's `meta.sources` names every source and what was read of it; `meta.bound` names what was not.

| Family | Codes |
|---|---|
| Craft books | B, BR, W, R, LT, TH, PU |
| Design systems | H, M, A, G, U |
| Checklists and limits | WC, BY, I (impeccable) |
| Web platform | MD, BL, WD |
| Landing-page practice | NG, CX, UB |
| Practitioner writing from 2023 on | KR, EK, JC, RF, BT, MS |

One more source, VG (Vercel Web Interface Guidelines), is held out: it is coded only after the search ends, as a check (§5).

## 2. Extract, blind

One coder per source. The coder reads no repository file, issue, `docs/research/` or `plugin/` file, so the house's view cannot steer what is found. Read every in-scope page as raw text (`curl -sL`, then strip the HTML), never through a summarising fetch tool.

**Scope:** everything a builder decides that shows on a web page, conversion and trust included. Out: copy wording, technical SEO, page-speed engineering, back-end, native-only matters with no web equal, developer API use that changes nothing shown.

**One row = one decision:** one property of one element in one context, written as the builder's question ("How much letter-spacing on large headings?"). Split a row where the source answers differently by context; never split by value (16 px vs 18 px is one decision). A hard limit is a row (the decision it limits). A CSS feature is a row as the choice it opens. Code what the source names as a choice or rule, even with no answer.

Each row is one JSON line:

```
{"src","loc","quote","element","property","context","decision","gives","answer","era","topic"}
```

`gives` is guidance, limit, default, feature or named; `era` is E where the answer depends on current platforms or fashion, T otherwise. Each coder ends with a Bound: pages read in full, skimmed, and not reached.

## 3. Merge to one grain, blind

Raw rows are split into keyword buckets only to share the work. One merger per bucket turns raw rows into canonical decisions; the grain decides every stop number (§5), so consistency matters most:

- Merge rows that ask the same question in other words, and a limit with the guidance on the same decision.
- Keep the same property on different elements apart only where at least one source treats them apart.
- Never merge on a shared CSS property alone. Values never split.
- Drop a row outside scope, with the reason; move a row that belongs to another bucket.

Moved rows are then placed against the whole decision list, a pass folds duplicate decisions across buckets (`absorbed`), and areas are drawn last, from the merged list. Each row keeps every raw locator as `incidence` per source.

## 4. Verdicts

One agent per area gives each decision a verdict by #210's covered test. All five must hold for `covered`:

1. **sourced:** the answer rests on an outside source, a measured test, or a founder ruling recorded as taste or business fact.
2. **conditioned:** it says when it applies and what it trades against, and names the typeface's measured traits where the answer depends on them.
3. **era_labelled:** it says timeless or era-bound; era-bound cites a source from 2023 on.
4. **carried:** it is written in a file a web round loads (`plugin/skills/*/SKILL.md`, `references/*.md`, `design-critique/rules/*.md`, or a design-round script). A row's `house` cites a rule record by its id and any other text by file:line; a covered row cites record ids alone (#272).
5. **disposed:** a `docs/research/` principle on it has a destination.

Otherwise: `partial` (a carried text answers it, a criterion fails), `researched` (only a research principle answers it), `impeccable-only`, or `gap`. An impeccable line, a project's own value or a ban alone is never covered. The agent opens every record and file:line it cites.

`node ledger-upkeep.js --check` refuses a verdict its criteria do not support (`partial` carried, the other three not; a carried row citing house text, a `researched` or undisposed row citing a research line). It refuses a covered row citing anything but a record in the store, or a record missing its `source`, `applies-when` or `era`, or one whose `ledger` does not list the row. A covered row needs an era of T, E or mixed, and one of era E a record whose `source` names a year from 2023 on, as "WCAG 2.2 (2023)" or "as read Oct 2026" does (#266).

## 5. Stop numbers, per area

- **Saturation:** over 2,000 random source orders (seed 215), the share of rows the last two sources add over the rows found before them. Passes at a median of 0.05 or less.
- **Sample coverage** (Chao and Jost 2012, incidence form): the chance that a decision a new source names is already a row. The ledger passes at 0.75 or more.
- **Chao2:** observed rows over the estimated total, reported but not required (#216 Q1).
- **Notes recall:** a coder who has not read the founder's notes N1–N19 (#202) finds them in the ledger.
- **Held-out recall:** VG is coded blind after the search and each of its rows matched to the ledger: strict recall is matches over rows in scope, loose adds rows a broader ledger row holds (Sampson 2006).

An area is complete enough to fill from when saturation passes and the ledger's sample coverage does (#216 Q1).

`python3 ledger-stop-numbers.py` prints each area's rows, Chao2 ratio, saturation median and sample coverage, in that order, straight from the ledger.

## 6. Tags, rulings and order

Every row not `covered` carries a `tag` from one agent per area group (#216):

- `kinds`: the kinds of site the decision arises on: `any`, `long-read`, `marketing`, `browse`, `forms`, `app`, `commerce`, `media`.
- `fill`: what filling it takes: `carry` (a research principle answers it), `condition` (a carried text lacks conditions, era or source), `source` (impeccable's answer, checked against outside sources), `default` (one standard or the platform fixes it), `research`, or `accept` (out of scope, obsolete or a duplicate, named in `why`).
- `route`: where the answer lands by #212: `script`, `gate`, `whole-page` or `builder`.
- `job`: the research job that fills it, one of top-level `jobs`.

Each tagged row also carries a `ruling`: `fill` true, or false with `why`. A row is filled when its tag is not `accept` and its `kinds` meet a kind the served projects have or plan; `meta.ruling.scope` names them. Each job carries a `tier` and a `rank`, and jobs are filled in rank order:

- **Tier 0:** `carry-*` and `*-defaults` batches.
- **Tier 1:** #208's jobs, in its dependency order.
- **Tiers 2–4:** every other job, by where most of its rows arise: on every served project, on one project only, or only in signed-in tools.
- **Within a tier:** jobs go by rows times sources naming each (capped at 5) times projects reached, per estimated session (25 research rows, 40 condition or source rows, or 60 carry or default rows a session).

A new row takes a tag and a ruling by the same tests, and joins its job's rank.

A filled row keeps its `tag`. A job is marked done by `done`, the issue that filled it (`"#275"`), and `destinations`, which maps every research line its rows cite to where it went: a record id, a project rules file line (`<project key>:<its rules file>:<line>`, the key and file as the library's `projects` give them), or `not carried: <reason>`. `--check` refuses a done job with a row neither covered nor accepted (`ruling.fill` false with its `why`), fewer filled rows tagged to it than its `rows`, or a research line with no destination. An open job is not judged: its rows are the gaps it exists to fill (#266).

## 7. Re-scan

`meta.rescan` gives the due date (`due`), its issue (`issue`) and which families to re-code (`what`). Re-code them, merge new rows into existing keys or new ones, give new rows verdicts, recompute the stop numbers with `ledger-stop-numbers.py`, and update `meta.built` and `meta.rescan`. A row's verdict changes between re-scans only when a ticket fills it, citing the ticket.

`node ledger-upkeep.js` runs at every session start in this repo and warns once `meta.built` is 12 months old or `meta.rescan.due` has passed (#267).

## 8. Method misses

A method miss is a design decision the founder raises that the ledger holds no row for. A lead the ledger holds a row for is not a miss: it goes to that row's job.

1. Search the rows for the decision by element, property and context, and by its other names.
2. Name the source family that should have caught it: the family whose sources name decisions of that kind. Where no source in any family names it, name the nearest family; its fix is a new source.
3. Add an entry to top-level `method_misses`: `date` (YYYY-MM-DD), `lead` (the founder's words), `family` (a `meta.sources` family name) and `issue` (the issue that re-checks that family, filed if none is open). `node ledger-upkeep.js --check` refuses an entry missing a field.
4. Add the decision as a row by §2–§4 and tag it by §6.
5. The issue finds why the family missed it (a source not read, a page `meta.bound` names as unread, a merge that folded it away) and fixes the method: a source added, a page read, a merge rule changed. It re-codes the family by §2.

## 9. Refresh triggers

- **A new impeccable version adopted:** re-code source I by §2, and re-check every `impeccable-only` verdict and every row tagged `fill: source`.
- **A new WCAG version:** re-code source WC, and re-check every row whose `sources` include WC.
- **A new project type:** re-tag `kinds` and re-rule (§6) the rows that kind of site raises, `meta.ruling.scope` gaining it, and check that some family's sources cover that kind of site.
- **A founder lead:** §8.
- **The yearly re-scan:** §7.
