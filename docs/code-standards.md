# Code standards — design-vault's local file

This repo's own choices beside the workflow-core plugin's standards base, `docs/code-standards-base.md` under the plugin root (workflow-core#947).

## Route rows and risk paths

| Path | Code kind |
|---|---|
| `app.js` | library, composition root: the library page's entry point, which loads the library by `fetch` or a script tag, keeps the selection, project and preferences in `localStorage`, writes the clipboard and the address bar, and hands what to show and copy to `view.js` and `search.js` (#381) |
| `specimens.js` | library: the style guide's static specimen table |
| `search.js` | library: the search box's rule, shared by the page and its tests (#27, #42) |
| `view.js` | library: what the page shows and copies, shared by the page and its tests (#84) |
| `server.py` | program: the read-only local server |
| `ledger-stop-numbers.py` | program: the coverage ledger's stop numbers per area, run by hand at a re-scan (#352) |
| `data/vault-data.js` | library: a static data table derived from `data/gallery.json` and `data/styles.json` by `node bundle.js`, so a fault in it is fixed in `bundle.js` (#32) |
| `plugin/review-page/review.js` | library: the shared review page's logic: checking the data file and the feedback boxes (#120) |
| `git-read.js` | library: git run for the programs that judge a commit from the index or HEAD, under one read cap (#141) |
| `log-gate.js` | library: what the round, corrections and calibration logs' gates share, reading a log from git and their command line, and the row reader the calibration packet and critic examples use (#166, #168) |
| `plugin/skills/design-round/scripts/access-pixels.py` | library: the pixel maths check-access.py measures its screenshots with (#198) |
| `plugin/skills/design-round/scripts/access-answers.py` | library: check-access.py's questions, and how each width's findings merge into one answer per question (#214) |
| `plugin/skills/design-round/scripts/access-keys.py` | library: check-access.py's keyboard and focus questions read from its Tab walk and from keys and mouse presses on a page of their own (#315) |
| `plugin/skills/design-round/scripts/access-pointer.py` | library: check-access.py's --pointer question, read from pages it opens under each pointer through the browser and conditions.py it is handed (#317) |
| `plugin/skills/design-round/scripts/access-boxes.py` | library: the boxes of generated `::before` and `::after` text, read from Chromium's DevTools for check-access.py's contrast question (#189) |
| `plugin/skills/design-round/scripts/access-contrast.py` | library: check-access.py's contrast questions past text and field edges, with their table's parser (#316) |
| `plugin/skills/design-round/scripts/text-checks.py` | library: check-text.py's checks, its table and word lists, and how each load's findings merge into one answer per record, split out so its tests call what the program calls (#314) |
| `plugin/skills/design-round/scripts/fail_open.py` | library: the core's `fail_open` and `expected` reporters, held in the plugin, which ships without the core (#380) |
| `plugin/skills/design-round/scripts/siblings.py` | library: loads a design-round script's siblings once per process, cached by real path, so every caller shares one copy of each error class (#558) |
| `plugin/skills/design-round/scripts/rule-table.py` | library: the rule tables' line reader, `ID \| CHECK [\| VALUE]` grammar and per-record answers, for the family scripts (#413) |
| `plugin/skills/design-round/scripts/probe.py` | library: reads a page's DOM and computed style against a rule table at check-layout.py's widths, one finding per record id, for the family scripts; also a program that runs one table (#300) |
| `plugin/skills/design-round/scripts/layout-records.py` | library: the record checks check-layout.py --records runs at each width and on its own loads, and how the sweep's widths give each record one answer, its values read from `check-layout.table` (#311) |
| `plugin/skills/design-round/scripts/motion-records.py` | library: the record checks check-flow.py --records runs, the probes it injects and how each record's checks give it one answer, its values read from `check-flow.table` (#318) |
| `plugin/skills/design-round/scripts/check-cross.py` | library: opens every page of a site and walks each flow, for the records that compare pages, its values read from `check-cross.table`; also a program that answers them (#306) |
| `plugin/skills/design-round/scripts/check-dom.py` | library: loads a page at phone and desktop width, right to left and at a missing address, and writes the DOM facts probe.py has no read for onto it, for the records on counts, attributes, presence and head tags, its values read from `check-dom.table`; also a program that answers them (#310) |
| `plugin/skills/design-round/scripts/check-load.py` | library: loads a page once and reads every font, image, stylesheet and script file it fetches, for the records on those files, its values read from `check-load.table`; also a program that answers them and times LCP (#170, #313) |
| `plugin/skills/design-round/scripts/font-file.py` | library: the font tables check-load.py reads (cmap, GSUB, GPOS, fvar, name, OS/2) from sfnt, WOFF and WOFF2 files, with no font library (#313) |
| `plugin/skills/design-round/scripts/spend-log.py` | library: reads a round's spend log and finds a candidate's line in it, for check-render.py and check-clip.py (#336) |
| `plugin/skills/design-round/scripts/check-markup.py` | library: runs the vendored axe-core in a page, for check-state.py's driven states too (#312); also a program that answers the markup records `check-markup.table` maps to axe rule ids (#307) |
| `plugin/skills/design-round/scripts/look-renders.py` | library: the contact crops check-seams.py measures, with a hook that shoots its mattes at each frame and scale (#341); also a program that renders vault.contacts-look's and vault.curves-look's sheets (#228) |
| `plugin/skills/design-round/scripts/check-state.py` | program: drives a page into the states a visitor reaches, by hover, press, keys, forms, overlays and the clock, and answers the records `check-state.table` maps to its checks (#312) |
| `plugin/skills/design-round/scripts/conditions.py` | library: opens a page under forced colours, a colour scheme, print, a locale, right-to-left, a pointer type or blocked requests, for the family scripts (#304) |
| `plugin/skills/design-round/scripts/drive-overlay.py` | library: finds a page's menus, dialogs and popovers and opens and closes them by click, keyboard and Escape, for the family scripts (#303) |
| `plugin/skills/design-round/scripts/drive-form.py` | library: fills a form with valid or planted invalid values, submits it, and reads the page once it settles, for the family scripts (#302) |
| `plugin/skills/design-round/scripts/drive-pointer.py` | library: hovers, presses, clicks, drags and wheel-scrolls a page with the mouse and returns once it settles, for the family scripts (#301) |
| `plugin/skills/design-round/scripts/fall-motion.js` | library: the fall and settle maths fall.js prints, split out so its tests call what the program calls (#187) |
| `plugin/skills/design-round/scripts/higgsfield-client.js` | library, risk path: higgsfield.js's command line, settings and render client, split out so its tests call what the program calls (#187) |
| `plugin/skills/design-round/scripts/gate-form.js` | library: the gate question form gate.js reads and checks, and the asset vocabulary corrections-log.js and critic-examples.js share with it (#187) |
| `plugin/review-page/page.js` | library, composition root: the review page's entry point, which reads `items.json` by `fetch`, opens the artifact store through `window.claude`, and hands every rule on checking and saving answers to review.js (#120, #381) |
| `kits/planted-faults/tools/*.py` | program: the planted-fault kit's research scripts, run by hand for a test of a critic's load; `runner.py` and `score.py` are also imported by the scripts beside them (#238) |

**Risk paths.** `plugin/skills/design-round/scripts/higgsfield.js` and `plugin/skills/design-round/scripts/higgsfield-client.js`, the client it runs, spend money: they call Higgsfield's pay-per-request API under `HIGGSFIELD_ROUND_CEILING_USD` and hold `HIGGSFIELD_API_KEY`.

## Local rules

**§LG1 · Python file names (workflow-core#1252).** A Python file run or loaded by path takes a kebab-case name, as its JS siblings do: a program, its test `test/<program>.test.py`, and a hand-run harness under `test/load/`. None is imported by module name (tests load their subject through `siblings.load`), so workflow-core#1252's reason for snake_case, that a hyphenated module cannot be imported, does not reach them. A module imported by name takes snake_case.

## §W — what tooling already enforces

The gates `.husky/pre-commit.local` adds to the floor. Each refuses the commit on any fault its checker prints, and where git cannot be read.

| Gate | Refuses | Staged paths that arm it |
|---|---|---|
| `node validate.js --staged` | a library that is not a well-formed schema v3 one: an unknown keyword, group, verdict, project, style or collection, a duplicate id, a missing image or still (#1) | `data/gallery.json`, `data/styles.json`, anything under `images/` |
| `node bundle.js --staged` | a `data/vault-data.js` missing from the index or not matching the staged JSON (#32) | `data/gallery.json`, `data/styles.json`, `data/vault-data.js` |
| `node round-log.js --staged` | a malformed row, or a row that changes one HEAD holds beyond adding its `final_pick`, `rejections` or `on_weakest` (#95) | `data/round-log.jsonl` |
| `node corrections-log.js --staged` | a malformed row, or a row that changes one HEAD holds beyond answering its pending ruling (#166) | `data/corrections-log.jsonl` |
| `node calibration-log.js --staged` | a malformed row, a run whose figures disagree with the disagreements listed under them, or any change to or removal of a row HEAD holds (#168) | `data/calibration-log.jsonl` |

No CI job runs: with `landingTester` pinned `local` (#531), the lander's own run of `commands.test` before `main` moves is the only gate past a commit.
