# browser-testing-and-accessibility

Researched: 2026-11-13

## Checks that compare pages

- A rule about a set of pages (WCAG 2.2 SC 3.2.3 Consistent Navigation, 2.4.5 Multiple Ways) is checked by reading every page of the set from its DOM and comparing them, not one page alone. W3C auto-wcag (archived), "SC3-2-3 navigational links across pages" and "Multi-page approach" [standard or field body]; the US Access Board's ICT Baseline, "Repetitive Content": review several pages and check each repeated navigation keeps its relative order [standard or field body]
- 3.2.3 compares only the items two pages share: items added or removed do not break it, only a change in their relative order. Understanding SC 3.2.3 [standard or field body]
- 2.4.5 is met by two or more distinct techniques (related links, a contents list, a site map, a search, a list of all pages, the home page linking every page); one list of links counts once, even where it would fit two techniques' descriptions. Its Intent allows a site of three or four pages whose home page links every page and is linked from each. Understanding SC 2.4.5 (updated 5 April 2026) and G185 (updated 15 July 2025) [standard or field body]
- No W3C ACT rule covers 2.4.5 or 3.2.3 (ACT rules list, read 2026-11-13) [standard or field body].

## The browser's Back button in a flow

- Assert what the page shows after Back, its URL and its field values, not that `goBack()` returned. Run a Back check where the back/forward cache is off, as Playwright's Chromium launches it, so it tests the page's own keeping of its answers. qaskills.sh, "Playwright test browser back button history" [unverified]; WebKit's manual test "form-value-restore", which turns the cache off to test the non-cached path [named expert]; GOV.UK Design System, "Question pages": Back returns the previous page "in the state they last saw it" [standard or field body]
- Research: #306.

## Spacing and enlarged-text checks

- Test 1.4.12 by setting all four values at once (line height 1.5, spacing after paragraphs 2, letter 0.12, word 0.16 × the font size), changing no other property, then checking for text clipped, overlapped or truncated with no way to show it. W3C Understanding SC 1.4.12 and failure F104 [standard or field body]. Neither names a selector for paragraph spacing; F104's examples use `<p>`, as does Faulkner's text spacing bookmarklet, the tool testers cite (WebAIM list, 2018) [unverified].
- Set the overrides so the page cannot outrank them: axe and IBM read only inline `!important` (#246). Inline `!important` on every element outranks every author stylesheet and cascade layer. CSS Cascading and Inheritance Level 5, cascade sorting order [standard or field body].
- Browser zoom and a larger default text size are different mechanisms; 1.4.4 needs only one to reach 200% with no loss, so text that fails to grow under one is a reading, not a failure on its own. W3C Understanding SC 1.4.4 [standard or field body]. Chromium's `Page.setFontSizes` raises the default sizes and holds across navigations: measured on Chromium 149, `1rem` 16→32 px, a fixed `16px` unchanged, monospace 13→26 px (#305) [unverified].
- Research: #305.

## Reading the files a page loads

- A WOFF2 file holds every table in one Brotli stream, back to back in directory order with nothing between them; only glyf, loca and hmtx may be transformed, so cmap, GSUB, GPOS, fvar, name and OS/2 read as they are once the stream is decoded. W3C, WOFF File Format 2.0, §5 [standard or field body]
- Which face drew a text, a web font or the browser's installed fallback, is the browser's own answer: CDP's `CSS.getPlatformFontsForNode` gives each font's family, PostScript name, whether it is a web font and its glyph count. Chrome DevTools Protocol, CSS domain [standard or field body], for what Chromium reports only
- Python's standard library has no Brotli decoder; Chromium decodes a response sent with `Content-Encoding: br` over plain HTTP to 127.0.0.1, and a Playwright `route.fulfill` body is not decoded. Measured on Chromium 149 (#313) [unverified]
- font-file.py, the dependency-free reader check-load.py uses, agrees with fontTools on the feature tags, cmap code points, fvar axes and PostScript name of 24 font files on this machine (16 sfnt, 5 WOFF, 3 WOFF2) and the three fixture fonts (#313) [unverified]

## Running axe-core in the page

- Inject axe's single file into the rendered page and call `axe.run` with `runOnly` of type `rule`: experimental ones run too (measured on 4.13.0 with `label-content-name-mismatch` and `p-as-heading`, #307). axe-core 4.13.0 `doc/API.md`, "No other rule will run" [standard or field body, for the tool's own behaviour]
- Count only axe's violations and passes. Its `incomplete` results "could neither be determined to definitively pass or definitively fail": report them for a person. axe-core `doc/API.md` [standard or field body, for the tool's own behaviour]; W3C WAI, "Selecting Web Accessibility Evaluation Tools": "Tools cannot check all accessibility aspects automatically. Human judgement is required", and they "can produce false or misleading results" [standard or field body]; GOV.UK Service Manual, "Testing for accessibility": "you'll miss some issues if you only do automated testing" [standard or field body]
- Map each house rule to the axe rules that decide it, and check what each misses before trusting it. On 4.13.0, `video-caption` gives only `incomplete` for a video with no track, `aria-progressbar-name` skips a native `<progress>`, and `td-has-header` applies only to tables over 3 by 3 (measured, #307) [standard or field body, for the tool's own behaviour]
- A `Content-Security-Policy` of `script-src 'none'` in a meta tag did not stop `page.evaluate` injecting axe (Chromium under Playwright 1.61.0, measured, #307) [standard or field body, for the tool's own behaviour].
- Research: #307.

## Driving a page into its states

- Hover or focus content (SC 1.4.13): show it, press Escape with the pointer or focus still, and it closes; move the pointer onto it, and it stays; hold still, and it does not close by itself. Understanding 1.4.13, technique SCR39 and failure F95 [standard or field body]
- Pointer cancellation (SC 2.5.2): send a press with no release and check nothing acted; a native `click` passes, as it fires only on a release inside the pressed target. Failure F101, technique G212 [standard or field body]
- On focus and on input (SC 3.2.1, 3.2.2): Tab to each part, change each control, and read the change-of-context signals: a new page or window, a navigation, focus moving off. A change of content, such as a menu opening, is none. WCAG 2.2 glossary "changes of context", G107, F36, F37, F55 [standard or field body]
- Character key shortcuts (SC 2.1.4): with nothing focused, press every printable character and compare the document before and after. F99; ACT rule ffbc54 (proposed) [standard or field body]
- Time limits (SC 2.2.1): install Playwright's `page.clock` before the load, run it forward, and read when the page leaves itself and whether a warning came 20 s before with one action to extend. The fake clock also fakes `requestAnimationFrame` and timers, so no settle wait that uses them may run under it; the Navigation API's `navigate` event gives the leaving's fake time, where `pagehide` fires only once the run ends (measured, #312). Understanding 2.2.1, SCR16; playwright.dev Clock [standard or field body]
- Sliders, menu buttons, disclosures and comboboxes: read `aria-valuenow`, `aria-expanded` and `aria-activedescendant` after each APG key, focus staying on a combobox's input; a suggestion count goes in a `role="status"` region, as GOV.UK's accessible-autocomplete does. WAI-ARIA APG patterns; Understanding 4.1.3 [standard or field body]
- `:visited` hides itself from script: `getComputedStyle` returns the unvisited style, so click the link, go Back and compare screenshots. Headless Chromium keeps no visited history in a normal launch; `launch_persistent_context` with `channel="chromium"` does (measured, Playwright 1.61, #312). MDN `:visited`; Chrome for Developers, "Making :visited more private" [standard or field body]
- Paste: a dispatched `ClipboardEvent` inserts nothing, so grant the clipboard permissions, write it with `navigator.clipboard.writeText` and press Control+V. W3C Clipboard API §5; Playwright `grant_permissions` (measured, #312) [standard or field body]
- A drag: under pointer capture no other element gets `pointerover`, so count those along the path; `:hover` does not tell a captured drag from an uncaptured one. Pointer Events Level 3 §4.1.3 (measured, #312) [standard or field body]
- Research: #312.

## Waiting for a page to settle

- Wait on a signal, not a fixed time: Playwright's own docs say `wait_for_timeout` "should only be used for debugging. Tests using the timer in production are going to be flaky. Use signals such as network events, selectors becoming visible and others instead" (docstring, Playwright 1.61.0, read from the installed package) [standard or field body, for the tool's own behaviour]; Checkly: hard waits "should never appear in production scripts" (checklyhq.com, "Why you should never use page.waitForTimeout()") [named expert]
- A page is stable when it has no pending macrotask: Angular's Testability waits for no outstanding timers (`setTimeout`, `setInterval`, `requestAnimationFrame`) before a test reads the page (angular.dev/api/core/Testability; NG0506) [named expert]
- Agreement (Playwright, Checkly): wait on what the page does, not on a fixed time. Ending a quiet-window wait once nothing the page has queued can still change it rests on Angular alone. drive-pointer.py's `WATCH_JS` does so, with a 100 ms floor for what it cannot see; its comment lists both (#462). Measured: check-state's suite 701 s to 211 s on one lane.
- Research: #462.

## A browser that stops answering

- `page.evaluate` takes no timeout, so `set_default_timeout` does not bound it. Playwright 1.61.0 API docs, `Page.evaluate` [standard or field body, for the tool's own behaviour]
- A renderer killed as it starts can leave the call waiting for ever: no `crash` event, no error, and the browser keeps its zygotes and GPU process but no renderer. Killed 150 ms in, or between calls, it is respawned or raises `Target crashed` at once. Killing the browser makes the waiting call raise `TargetClosedError` (Chromium under Playwright 1.61.0, measured, #432) [standard or field body, for the tool's own behaviour]
- Research: #432.

## Flash analysis (WCAG 2.3.1)

- A general flash is a pair of opposing changes in relative luminance of 0.1 or more where the darker state is under 0.80; a red flash a pair of opposing transitions where one state has R/(R+G+B) ≥ 0.8 and the two differ by more than 0.2 in CIE 1976 u′v′. A transition is the change between adjacent peaks and valleys, a flash is two, and more than three in any one-second window fails unless the flashing covers no more than 25% of any 10° field, estimated as a 341 × 256 px rectangle at 1024 × 768. WCAG 2.2 glossary, "general flash and red flash thresholds", Notes 1–3 [standard or field body]; Understanding SC 2.3.1 [standard or field body]
- Analysers work from captured frames, counting luminance and red transitions per pixel over a trailing one-second window: EA's open-source IRIS counts a transition where the accumulated change reaches ±0.1 (±20 on its red scale) and fails at more than three flashes in a second (github.com/electronicarts/IRIS, README, read 2026-11-16) [named expert]. PEAT (Trace Center) and Harding FPA are the tools Understanding 2.3.1 names; neither was run here [unverified].
- A fine balanced pattern (squares under 0.1° a side) is exempt; averaging frames into cells about that size before counting blurs it out. WCAG 2.2 glossary, Exception [standard or field body]
