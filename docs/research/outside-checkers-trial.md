# Outside checkers beside the vault's scripts, on pages with known faults (#249)

Ticket: design-vault #249, under map #243. Question: what do the tools #246 shortlists find on pages whose faults are known, compared with the vault's own scripts? These figures are the evidence for #250's adopt-or-build ruling. Nothing is wired into the gate.

## Method

- **Tools and versions.**
  - axe-core 4.13.0, the newest release at least 14 days old. `axe.min.js` was vendored as #244 says. Its sha256 matches Deque's `sri-history.json` entry for 4.13.0.
  - IBM `accessibility-checker-engine` 4.0.34. Its browser file `ace.js` (685 KB) was vendored the same way and run with the `WCAG_2_2` policy. Each result's level comes from that policy's rule map, as IBM's own wrapper does.
  - Lighthouse 13.5.0, performance and SEO categories only (#246's shortlist: CLS and SEO). It runs with its default mobile settings and simulated throttling. It came in by #244's Node route: a `package.json` with exact versions and a committed lockfile, in a throwaway worktree.
  - The vault scripts `check-access.py`, `check-layout.py` and `check-load.py` at 722c3f8.
- **Registry check (AGENTS.md).** Weekly downloads for 6–12 Oct 2026: axe-core 79.7M, lighthouse 5.4M, accessibility-checker-engine 21,671. Latest stable releases: axe-core 5 Oct 2026, lighthouse 18 Sep 2026, IBM engine 8 Sep 2026.
- **Install.** `npm install --ignore-scripts` of the three pinned packages added 115 packages in 51 s. Almost all of them are Lighthouse's. #244 found that Claude Code's install of a plugin's packages has a 60 s limit.
- **Pages.**
  - The 31 fixtures in `test/fixtures/access`, `layout` and `load`. Each fixture's comment names its planted faults, and the vault's tests assert them. The key is those comments.
  - The 12 mmm-infra site-look pages from #169 (tags `rounds/site-look-r1` and `rounds/site-look-r2`), served locally.
  - Two shift pages written for this run, because no fixture or page has a layout shift. Each has a 300 px banner put in above the text, one 800 ms after load and one 3 s after load.
- **How the pages loaded.** axe and IBM loaded each page with check-layout's own `load()`: the vault's desktop size (1920 × 633) and phone size (390 × 664, touch), and its settle step. Each tool got a fresh context, so both met the page in the state the vault scripts judge.
- **Matching.** On each page, every vault contrast or focus fault, every axe node and every IBM xpath was resolved to a DOM element. A tool "found" a vault fault when it flagged that element or an element that holds it or is inside it.
- **Lighthouse's accessibility category was not run.** #246 found it scores only axe's violations, so its column for the Access questions would equal axe's definite finds.
- **Levels.** A *definite* finding is an axe violation or an IBM `violation`. A *review* finding is an axe `incomplete` or an IBM `potentialviolation`. IBM's `recommendation` and `manual` results are left out. axe's `best-practice` rules (region, landmark-one-main, page-has-heading-one) are counted on their own.
- **Ground truth.** On fixtures it is the planted key. On pages it is the vault's verdict, checked by eye where tool and script disagree. The vault's page contrast faults were not each checked: 6 that were checked are vault errors (below).
- The raw results and the scripts that produced them were kept only in gitignored scratch and are not preserved.

## Findings per criterion

Counts are element instances at desktop width. The phone width gives the same counts unless named.

### Contrast, 1.4.3

- **Fixtures, 6 planted** (contrast.html: grey body text and its placeholder; faint.html: four dark patches behind one to three letters).
  - Vault: 6 of 6, no false positive. On noise.html (18 grounds: gradients, grain, photos under a scrim) it passes all. It names 2 cases it cannot measure on unmeasurable.html.
  - axe: 1 definite (the grey text). 1 more as review (faint.html's short label). It misses the placeholder and 3 of the 4 patches. It returns 26 review findings across the fixtures: 18 of them are on noise.html, where all text passes.
  - IBM: 1 definite (the grey text). It misses 5. It names unmeasurable.html's 2 cases as review.
  - Both tools agree with the vault on unmeasurable.html: gradient text and text over a canvas cannot be read from CSS.
- **Pages.** The vault fails 108 element-widths: r1 v1 8, r1 v2 95, r1 v4 1, r2 v2 4 (phone only).
  - 6 of r1 v1's 8 are **vault false positives.** "write to me" (red on yellow) and two navy text lines read 1.00:1, because a stroke of the text's own colour crosses the glyphs: a hand-drawn underline and the pad's rules (#257).
  - axe: **0 definite on any page.** All 102 true vault faults are in axe's review list. That includes r2 v2's phone nav, which axe measures as "1:1" but still marks as review, not as a violation. So Lighthouse, which counts only violations, would pass the page with the 1.01:1 nav. axe gives 149 review nodes across the 12 pages at desktop and 146 at phone. 55 and 53 of them are vault faults; the vault passes the rest.
  - IBM: 0 definite. As review it flags 3 of r1 v1's elements a width: the 4.46:1 line, which is true, and the two navy lines, which are the vault's false positives. It flags none of r1 v2's 95, r1 v4's or r2 v2's. It gives 32 review findings a width across the pages.

### Control edges, 1.4.11

- Fixtures, 5 planted (edge.html 3, faint.html 2): vault 5 of 5. axe 0 and IBM 0: neither has a rule for this.
- Pages: no vault fault, no tool finding.

### Target size, 2.5.8

- **Fixtures, 10 planted at desktop and 8 at phone** (target.html 8; touch.html 2, at desktop only, because its buttons grow under a touch screen).
  - Vault: 10 of 10 and 8 of 8, no false positive.
  - axe with its default rules: 0. **axe 4.13.0 ships `target-size` switched off** (`enabled: false`).
  - axe with `target-size` switched on: 10 of 10 and 8 of 8, with touch.html right at both widths. It gives 3 false positives a width: clean.html's unstyled select, button and date input, which WCAG's user-agent exception exempts (#188).
  - IBM: 4 as review (target.html's two card links, its button and its text field). It misses 6: the two 20 px tools 2 px apart, the select, the date input, and touch.html's pair. It gives 2 definite false positives a width: clean.html's two browser checkboxes, which the user-agent exception exempts.
- Pages: no vault fault, no tool finding.

### Link told by colour alone, 1.4.1

- Fixtures, 3 planted (link.html): vault 3 of 3. **axe 3 of 3 definite, the same elements at the same 2.44:1.** IBM 0. No false positive from vault or axe: both pass link.html's two black links in grey text and clean.html's links.
- IBM's `style_color_misuse` gives one review finding on every page whose stylesheet sets a colour (21 fixtures, all 12 pages). It names no element, so it is counted as neither a find nor a false positive.
- Pages: no vault fault, no tool finding.

### Keyboard, 2.1.1

- **Fixtures, 4 planted** (keyboard.html).
  - Vault: 4 of 4.
  - axe: 0.
  - IBM: 2. The `onclick` div is definite. The link with `tabindex="-1"` is review. It misses the span with a click listener and the React handler, because a DOM rule cannot see a listener.
  - IBM false positives on clean.html: 2 definite (`aria_eventhandler_role_valid` on the off-page div and the card, which the vault reaches through the link it holds) and 2 review (the tab list, and the checkbox hidden for a screen reader).
- Pages: the vault passes all 12. No tool finds anything.

### Focus shown and not hidden, 2.4.7 and 2.4.11

- **Fixtures, 7 planted** (focus.html 4, link.html 2, flicker.html 1).
  - Vault: 7 of 7.
  - axe: 0.
  - IBM: 1 as review (link.html's transparent outline). Its `style_focus_visible` gives 27 review findings across the fixtures. The other 26 are on controls that show the browser's ring.
- **Pages.** The vault fails 19 element-widths: r1 v1 6, r1 v4 10, r2 v2 3.
  - axe: 0.
  - IBM: 7 as review, but for a different reason on 3 of them: r2 v2's nav links are flagged as possibly obscured. Its `style_focus_visible` gives 24 review findings a width; 4 are on vault faults.
  - Checked by eye on r1 v1: the nav shows a red ring on maroon. It is visible, but it changes by less than the vault's 3:1. So the fault is real under the house's rule. It is weaker under 2.4.7 AA alone, which asks only that focus be visible; the 3:1 figure is 2.4.13's, at AAA.

### Motion pause, 2.2.2

- Fixtures, 3 planted (loop.html 1, motion.html 2): vault 3 of 3. axe 0, IBM 0. The vault says it cannot measure flicker.html's canvas, unmeasurable.html and r2 v2's drawn image.

### Layout and reflow (vault.reflow, vault.layout)

- **Fixtures.** The vault finds every planted kind: overlap on crowd, slide, under and probe; text cut off on cut and overflow; sideways scroll on nested, overflow, touch and wide; the call to action below the first screen on fold; viewport on nometa and fixed; zoom blocked on fixed.
  - It also reports a viewport fault on 6 fixtures that scroll sideways. The page really is shown at 53–80%, but the cause is the overflow, not the meta, which the row blames. So one fault is reported twice.
  - Excluded from these counts: this run passed `--cta .book` to every layout fixture, so the call-to-action fails on fixtures with no `.book` link are this run's doing.
- axe: zoom blocked, 2 of 2 definite (`meta-viewport`, both metas on fixed). As review, probe's 2 hidden texts ("overlapped by another element"). Nothing else.
- IBM: zoom blocked on fixed, as a recommendation only. Nothing else.
- Lighthouse `viewport-insight`: nometa and fixed, 2 of 2, for width. It does not judge zoom.
- Pages: the tools find nothing on layout. The vault's page findings are as #169 recorded: sideways scroll on r1 v1 (525 px) and r1 v3 (320 px), overlaps on r2 v1 and r2 v7 (r2 v7's include the 2 script errors #169 names), and the email link below the first screen on 9 pages.

### Load: largest paint and layout shift

- **Largest paint (LCP).**
  - late.html reveals its headline 3 s in. The vault fails it. **Lighthouse reports 628 ms and passes it**, because its recording ends before 3 s.
  - blank.html: the vault exits 6 (no LCP element). Lighthouse errors with `NO_FCP`.
  - On the 12 pages, Lighthouse's simulated LCP is 2.9–9.5 s, over 2.5 s on all 12. The vault's applied throttling passes 6 of them (medians 1.5–1.8 s; r1 v4 is 1.7 s against Lighthouse's 9.5 s) and fails 5 (3.7–5.3 s). r1 v3 drew no LCP element in 1 of the vault's 3 runs.
  - No ground truth exists for these pages. The two methods disagree on 6 of 11 pages that both measured.
- **Layout shift (CLS).** The vault measures none.
  - Lighthouse finds the shift 800 ms after load (CLS 0.22, over Google's 0.1 limit). It **misses the same shift 3 s after load (CLS 0).**
  - On the 12 pages, the highest CLS is 0.099 (r2 v5), and none is over 0.1.

### Findings outside the vault's criteria (the tools only)

- **3.1.1 page language:** axe and IBM, definite, on all 29 fixtures with no `lang`. True. Every page has one.
- **2.4.2 page title:** axe, IBM and Lighthouse, definite, on the 3 load fixtures. True.
- **4.1.2 ARIA:** axe `aria-prohibited-attr`, definite, on 4 pages (r1 v1, r1 v2, r1 v5, r2 v5), plus r2 v2 as review. Each is an `aria-label` on a plain `div` texture tile, which screen readers ignore. True.
- **2.5.3 label in name:** IBM `label_name_visible`, definite, on r2 v3, r2 v4 and r2 v5. The home link reads "Mark M. Moseley Moseley Infrastructure Advisory Services", but its name is "Mark M. Moseley, MMM Infra, home". True. axe's default run does not report it.
- **Meta description:** Lighthouse, on 9 of 12 pages and every fixture. It checks only that one is present. True.
- **Best practice and noise.**
  - axe on the fixtures: `region` 99, `landmark-one-main` 28 and `page-has-heading-one` 25 nodes. On the pages, `region` 9.
  - IBM's definite `skip_main_exists` fires on 26 single-block fixtures, where WCAG's 2.4.1 asks no skip link. Those are false positives; no page has it.
  - IBM's review list on the pages runs to about 140 findings a width: `text_sensory_misuse` 39, `text_contrast_sufficient` 32, `style_focus_visible` 24, `text_block_heading` 19, and `style_color_misuse` 12. It also has smaller counts of `style_viewport_resizable`, `blockquote_cite_exists`, `style_background_decorative` and `text_quoted_correctly`.

## Run time

| Tool | Per page, both widths | Notes |
|---|---|---|
| axe-core | 1.4 s median (1.0–2.5) on pages; 0.7 s on fixtures | after the page settles; one width each, two widths |
| IBM engine | 0.9 s median (0.6–1.9) on pages; 0.6 s on fixtures | as above |
| Lighthouse | 13.6 s median (11.5–16.7) on pages; 11.2 s on fixtures | one mobile run, Chrome launch included |
| check-access.py | 22.4 s median (12.6–27.9) on pages; 19.9 s (8.8–67.1) on fixtures | seven questions, both widths |
| check-layout.py | 42.8 s median (34.2–174.5) on pages; 38.3 s on fixtures | 320–1920 px every 5 px, and 2560 |
| check-load.py | 29.1 s median (21.5–53.7) on pages | three throttled runs |

All runs were sequential on this machine: 8 cores and about 4 GB free under WSL2. Loading and settling a page for axe or IBM took 0.9–2.9 s per page on top of the times above.

## Packaging facts found on the way

- Under WSL, Lighthouse's Chrome launcher ignores `--chrome-path` and starts the Windows `chrome.exe`. `CHROME_PATH` pointing at Playwright's Chromium fixes it. A plugin route that ships Lighthouse must set `CHROME_PATH` (#250).
- axe's `target-size` is off by default. An adopted axe must switch it on by name, or 2.5.8 goes unchecked (#250).
- Vendored `ace.js` and `axe.min.js` each ran from a single file injected through `page.add_script_tag`, with `bypass_csp=True`. This run did not check whether either makes network calls.

## Summary for #250

| Criterion | Vault script | axe-core | IBM engine | Lighthouse (performance and SEO only) |
|---|---|---|---|---|
| 1.4.3 contrast, fixtures (6) | 6, 0 FP | 1 definite + 1 review | 1 definite | not run |
| 1.4.3 contrast, pages (102 true) | 102 + 6 FP | 0 definite, 102 in review among ~150 a width | 2 in review | not run |
| 1.4.11 control edges (5) | 5 | 0 | 0 | not run |
| 2.5.8 target size (10 / 8) | 10 / 8, 0 FP | 0 by default; 10 / 8 + 3 FP with the rule on | 4 review, 2 definite FP | not run |
| 1.4.1 link by colour (3) | 3 | 3 definite | 0 | not run |
| 2.1.1 keyboard (4) | 4 | 0 | 2 (1 definite), 2 definite FP | not run |
| 2.4.7 / 2.4.11 focus, fixtures (7) | 7 | 0 | 1 review, 26 review FP | not run |
| 2.4.7 / 2.4.11 focus, pages (19) | 19 | 0 | 7 review | not run |
| 2.2.2 pause (3) | 3 | 0 | 0 | not run |
| Layout and reflow, 12 fixture kinds | all 12, one double report | zoom only | zoom (recommendation) | viewport width only |
| LCP (late.html) | fails it, right | — | — | passes it, wrong |
| CLS (2 planted shifts) | not measured | — | — | 1 of 2 (misses the 3 s one) |
| 3.1.1, 2.4.2, 4.1.2, 2.5.3, meta description | not measured | 3.1.1, 2.4.2, 4.1.2 | 3.1.1, 2.4.2, 2.5.3 | 2.4.2, meta description |
| Time per page | 22–43 s a script | ~1.4 s | ~0.9 s | ~14 s |

What the figures say, for #250 to weigh:

- No tool replaces a vault Access script. On the vault's seven questions, the tools' definite finds are axe's 3 colour-only links and, with its rule switched on, axe's target sizes, which tie the vault's 10 and 8 and add 3 false positives. On the pages' 102 true contrast faults, no tool gives a single definite finding.
- axe's review list holds every page contrast fault, but with about three times as many items the vault passes. A gate that sent axe's "incomplete" to the critics would send them about 150 contrast items a page set per width.
- The tools add four true WCAG findings the vault does not measure (3.1.1, 2.4.2, 4.1.2, 2.5.3) and Lighthouse's meta description.
- Lighthouse's default load window ended before an event 3 s after load: it missed both a late headline (LCP) and a late shift (CLS). A CLS check built into check-load.py could watch for as long as the vault chooses.
- The run found one vault misread, the same-colour stroke (#257).
