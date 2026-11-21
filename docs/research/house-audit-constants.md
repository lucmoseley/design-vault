# #183 audit: the guess constants in the plugin scripts

Scope: the guess constants in `plugin/` scripts, except check-flow.py, check-frames.py and check-overlay.py (another agent audits them). Files: check-access.py, check-layout.py, check-measure.py, contact-sheet.py, review-page/review.js, higgsfield.js. Date: 14 Oct 2026.

Key to dispositions:
- DESIGN CLAIM: a published source can set the value. Result is SOURCED, CONFLICTS or GAP.
- NOT A DESIGN CLAIM: an engineering knob. Measurement in use sets it. The entry names that measurement.

## Findings

### H1. higgsfield.js `poll`: first wait 2 s, each wait x1.5, at most 10 s (line 227)

- Class: NOT A DESIGN CLAIM. It is an engineering knob. But the vendor publishes a value for it, so the vendor's value applies.
- Disposition: **SOURCED. The comment "A guess, not tuned against the API" is wrong.** The constant is exactly the Higgsfield recommendation.
- Source: Higgsfield docs, "Polling", https://docs.higgsfield.ai/docs/concepts/polling.md (read in full, 14 Oct 2026). Quote: "1. Start with a two-second interval. 2. Increase the interval gradually up to ten seconds. 3. Add random jitter when many workers poll concurrently." The sample code on that page is `delay = 2.0` ... `time.sleep(delay + random.uniform(0, 0.5))`; `delay = min(delay * 1.5, 10.0)`. The script has the same three numbers.
- Difference: the script adds no jitter. The docs ask for jitter only "when many workers poll concurrently". `render` submits and polls one job at a time (the `for` loop at line 313, with `await poll`). Thus no jitter is necessary.
- Rate limit: https://docs.higgsfield.ai/docs/concepts/rate-limits.md (read in full). The limit is concurrency per account and model (sample: 4 requests), shown in the Console. The docs say: "The API does not currently publish standard rate-limit response headers or `Retry-After`." The docs give no poll-rate limit.
- Founder ruling: none on the interval. #18 ruled only the $3 round ceiling (30 Sep 2026). #18's build note says "polls from 2 s up to 10 s", and its Bound says the agent read the polling page.
- Correction: change the comment to cite docs.higgsfield.ai Polling.
- Confidence: high (95%).

### H2. higgsfield.js `timeoutMs`: 10 minutes for each job (line 270, no comment)

- Class: NOT A DESIGN CLAIM. It is an engineering knob.
- Source check: the Polling page says only "Set an application-level timeout appropriate for the selected model." It gives no number. The Errors page (https://docs.higgsfield.ai/docs/concepts/errors.md, read in full) says "Set maximum attempts and a total retry deadline", also with no number.
- Measurement that sets it: record the time from submission to `completed` for each model in the spend ledger (`higgsfield-spend.jsonl`) for real rounds. Set the timeout above the slowest observed time for that model (for example, the 99th percentile plus a margin). A video model will need more time than a still model (#62 adds video).
- Founder ruling: none found.
- Correction: give the constant a comment that says it is a guess, and name the measurement.
- Confidence: medium that 10 min is enough for still images; low for video.

### R1. review.js `NOTE_PAUSE_MS = 900`: the pause that ends a burst of typing (line 12)

- What it does: a note box saves 900 ms after the last keystroke (line 128). A mark, a pick, leaving the box and leaving the page save at once (`flush`). Thus the value sets only how often a note saves while the founder types. It does not set whether a note is lost.
- Class: the comment makes a DESIGN CLAIM ("the pause that ends a burst of typing"). Typing research can set that claim. The use is an engineering knob (the number of writes against the age of the last save).
- Disposition: **CONFLICTS for the claim. The constant is acceptable for the use.**
  - Writing research defines a burst as text between pauses of at least 1 s or 2 s. Chenu, Pellegrino, Jisa, Fayol (2014), "Interword and intraword pause threshold in the writing of texts by children and adolescents", Frontiers in Psychology, https://www.frontiersin.org/articles/10.3389/fpsyg.2014.00182/full (read through a fetch summary with exact quotes, not in full): "the most used criterion is a threshold of 1 s (Schilperoord, 2002)"; "hence the thresholds of 1 or 2 s most commonly used with adults"; "there is no precise reason advanced for the thresholds of 1 or 2 s". The 2 s threshold of Chenoweth and Hayes (2001), "Fluency in writing", Written Communication 18: 80-98, comes only from secondary citations (search summary). I did not read the original.
  - Keystroke timing: Dhakal, Feit, Kristensson, Oulasvirta (2018), "Observations on Typing from 136 Million Keystrokes", CHI 2018, https://doi.org/10.1145/3173574.3174220 (PDF from userinterfaces.aalto.fi; I read the results section). Quote: "Average inter-key interval is 238.656 ms (SD = 111.6) ... slow typists have an IKI of over 480 ms, sometimes as high as 900 ms". This is copy typing on a physical keyboard. On phones, Palin et al. (MobileHCI 2019) report 36.2 WPM (abstract only). That is approximately 330 ms for each character (my calculation at 5 characters a word).
  - Thus 900 ms is above the gap between keys for almost all typists, but below the 1 s to 2 s pause that the research uses to end a burst. The constant departs from the research value by 10% to 55%.
  - Library default for the same job: react-autosave saves at most each "2000" ms ("The number of milliseconds between save attempts. Defaults to 2000"), https://github.com/jollyjerr/react-autosave README (read). Lodash `debounce` has no default wait.
- Effect of the conflict: small. A shorter pause causes more saves in a pause inside a sentence.
- Measurement that sets the use: count the `db` writes per note in one real review session, and find whether a write in progress (`writing`) ever queues a second write. If the count stays low, 900 ms is sufficient. If the store throttles writes, change to 1000 ms to 2000 ms.
- Founder ruling: none found. The value came from mmm-infra's `private/photo-runs/calibrate-v4/template.html` line 243 (`setTimeout(..., 900)`), which has no comment that gives a source. #120 has no comment about the pause.
- Correction: change the comment. Say it is a save debounce, not a burst boundary; cite the 1 s to 2 s burst threshold and Dhakal 2018; keep 900 or change to 1000 ms. No question to the founder.
- Confidence: high that the burst claim is below the research threshold. Medium on the best save value, until the write count is measured.

### A1. check-access.py `DRAWN = 1.05`: below this contrast a box draws no edge or fill ("#f9f9f9 on white") (line 111)

- What it does: `control_edge` (line 456) walks out from a control through its wrappers. The first box whose best edge or fill reaches 1.05:1 against its surroundings is the box that WCAG 1.4.11 judges. If no box reaches 1.05, the control "draws no edge" and `vault.control-edges` passes for it (#163 build note).
- Class: DESIGN CLAIM. It claims the lightest fill step that a person sees as a separate fill. Perception research and design-system practice can set it.
- Disposition: **CONFLICTS.**
 - Practice: design systems ship deliberate surface steps below 1.05:1. In this repo, `docs/research/de00-greys.md` G1a (computed from the published hex): Radix gray 1/2 `#fcfcfc`/`#f9f9f9` 1.03; Fluent Background1/Background2 `#ffffff`/`#fafafa` 1.04; Fluent Background2/Background3 1.04; Material 3 surface/surfaceContainerLow 1.04; M3 surfaceContainerLow/surfaceContainer 1.05. I added Tailwind v4: `--color-gray-50: oklch(98.5% 0.002 247.839)` (= `#f9fafb`) on white is 1.044:1; neutral-50 and zinc-50 (`#fafafa`) 1.044; slate-50 1.047 (source: https://github.com/tailwindlabs/tailwindcss/blob/main/packages/tailwindcss/theme.css, lines 214-262; my calculation, ). Bootstrap 5.3 `$body-tertiary-bg` = `$gray-100` `#f8f9fa` is 1.054, just above (https://github.com/twbs/bootstrap/blob/v5.3.3/scss/_variables.scss lines 10, 445). Primer `bgColor-muted` `#f6f8fa` 1.065 (@primer/primitives light.css, unpkg).
 - Perception: the DICOM Grayscale Standard Display Function (PS3.14, built on Barten's contrast-sensitivity model; constants from https://dicom.nema.org/medical/dicom/2024c/output/chtml/part14/chapter_7.html, read through a fetch summary) gives one just-noticeable difference as 0.69% to 0.77% of luminance at 80 to 300 cd/m2 (my calculation from Equation 7-1, ; the equation form reproduces L(1) = 0.05 and L(1023) = 3993 cd/m2). `#f9f9f9` is 5.3% darker than white and Tailwind gray-50 is 4.4% darker. Thus each is approximately 6 to 7 JNDs: visible to a normal viewer under good conditions.
  - Departure: the constant puts the lightest fills that four systems ship on purpose (1.03 to 1.05) in the class "draws nothing". With Tailwind, the most common lightest panel (`bg-gray-50`) falls below the line. Result: a field that has only a gray-50 fill on white is not judged by its own fill. If no wrapper draws an edge, it passes `vault.control-edges`. WCAG 1.4.11 would judge that fill as the visual information that identifies the field, and it fails 3:1.
- Measurement that also applies: a box that draws nothing reads exactly 1.00:1 against flat surroundings (the medians are equal). Thus the noise floor is set by gradients, JPEG noise and photos, not by flat fills. Render fixtures of Radix, Fluent, M3, Tailwind and Bootstrap fields and of plain boxes over gradients and photos. Set DRAWN between the highest noise reading and 1.03. A value near 1.02 is likely; this is not measured.
- GAP that remains: which step "survives a poor screen" (ambient glare, a low-cost panel) is a point on a measured curve. I found no published curve for web UI fills. This gap does not block the correction: the script asks "did the author draw a fill", not "can every viewer see it".
- Founder ruling: none found.
- Confidence: high (85%) that 1.05 is above several shipped surface steps. Medium on the replacement value until the noise fixture is measured.

### A2. check-access.py `WORST_SHARE = 5`: the share of a text box's background pixels that may fall below the needed contrast (line 103)

- What it does: the script hides the text, takes a screenshot, and composites the CSS text colour over each background pixel in the text's line boxes. It takes the 5th percentile of the ratios as "worst" (line 395). Thus up to 5% of the line-box area may fail.
- Class: mixed. WCAG sets WHICH pixels must contrast (a DESIGN CLAIM). The share is an allowance for measurement noise (an engineering knob).
- Disposition: **CONFLICTS in part.**
  - WCAG F83 (https://www.w3.org/WAI/WCAG22/Techniques/failures/F83, read in full): "there would need to be sufficient contrast between the text and those parts of the image that are most like the text and behind the text." Its quickcheck uses "the area of the image that is darkest (for dark text) or lightest (for light text)", then "check to see if the background behind each letter has sufficient contrast with the letter." WCAG gives no area allowance.
  - WCAG supports a noise allowance only for dithering: Understanding 1.4.3, relative luminance Note 4 (https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html, read by keyword): "For colors that are dithered at the source, the average values of the colors that are dithered should be used". Its anti-aliasing note tells the tester to use the specified colours, "rather than the text as presented on screen". The script already does this, because it hides the text. Thus the comment's reason "an anti-aliased edge" does not apply to glyphs; it applies only to edges inside the background.
  - Departure: in a line box, glyph ink covers only part of the area. A dark patch of 5% of the box can sit behind several letters. F83 fails that case, and the script passes it. The script is stricter in another way: it reads the whole line box, not only the area behind letters.
- Measurement that sets the knob: fixtures of text over flat colour, a gradient, a JPEG photo with fine noise, and a photo with one dark feature behind 2 to 3 letters. Find the lowest share that passes the noise-only fixtures and fails the feature fixture. A per-letter test (F83 step 2) is the alternative that removes the share.
- Founder ruling: none found.
- Confidence: high that WCAG has no area allowance. Low on the correct share until the fixtures are run.

### A3. check-access.py `AROUND = (3, 6)`: surroundings read 3 to 5 px outside a control, "past a 1-2 px ring" (line 106)

- Class: NOT A DESIGN CLAIM. WCAG 1.4.11 says only "adjacent color(s)" (https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html, read by keyword). The pixel offset is a sampling knob.
- Relevant fact: the script blurs focus before the screenshot (`BLUR_JS`), so a focus ring is not present. Rings at rest come from author CSS. Tailwind v4 `ring` is `0 0 0 1px` and `ring-<number>` is `<number>px` (https://tailwindcss.com/docs/box-shadow, first 100k characters read). A `ring-4` or a ring with `ring-offset` puts the first sample line (3 px) on the ring. The median over three lines (3, 4, 5 px) then still reads mostly the true ground for a ring of at most 4 px.
- Measurement: render controls with the ring and shadow styles of Tailwind UI, Bootstrap and Material at rest. Confirm that the median of the read lines equals the page ground for each.
- Founder ruling: none found. Confidence: medium that (3, 6) is sufficient for common styles.

### A4. check-access.py `WRAP, WRAPPERS = 12, 3`: a wrapper at most 12 px taller a side, at most 3 wrappers out (line 114)

- Class: NOT A DESIGN CLAIM. These knobs decide which DOM box is the visual field around a control. No published source sets them.
- Measurement: run the check over the founder's past candidates and a set of real sites. For each control, record the box that a person names as its field, and its distance in px and in wrappers. Set WRAP and WRAPPERS to cover that set. #163 found one case (a bordered label around a search input), which is inside both limits.
- Founder ruling: none found. Confidence: medium.

### A5. check-access.py `FILL_INSET = 4`: fill read 4 px inside the control, past its border (line 117)

- Class: NOT A DESIGN CLAIM. It is a sampling margin.
- Evidence already in the repo: #163's mutation run says "The survivor sets the fill inset to 0 and goes uncaught because the fill is read by its median." Thus the value has no effect on the tested fixtures.
- Measurement: a fixture with a thick border (for example 4 px or more) and a small control (for example 24 px tall). Then the border is a large share of the box and the median moves. Set the inset to the thickest border expected.
- Founder ruling: none found. Confidence: high that the value is harmless at common border widths (1 to 2 px).

### Data used by V1 to V6 (viewport sizes)

- StatCounter Global Stats, screen resolution, worldwide, September 2026, CSV export of the top 20 rows plus "Other" for each device class (fetched 14 Oct 2026 from gs.statcounter.com `chart.php?...&csv=1`; pages https://gs.statcounter.com/screen-resolution-stats/{mobile,desktop,tablet}/worldwide). StatCounter reports the screen size in CSS px, not the browser viewport. "Other" is 35.3% (mobile), 22.7% (desktop) and 42.6% (tablet), so the shares below are of the whole market, and the order of rows inside "Other" is unknown.
  - Mobile: 414x896 13.3%, 360x800 7.58%, 384x832 7.1%, 390x844 6.02%, 393x873 4.19%, 360x780 3.39%. By width: 360 16.3%, 414 13.3%, 384 10.4%, 390 6.0%. No row below 360 wide.
  - Desktop: 1920x1080 28.08%, 1536x864 9.99%, 1366x768 7.95%, 1280x720 4.7%, 2560x1440 3.95%, 1280x1200 3.68%, 1440x900 2.94%. Wider than 1920: 6.4% in the named rows (2560x1440 3.95%, 2560x1600 1.74%, others).
  - Tablet: 768x1024 8.08%, 1280x800 7.86%, 800x1280 7.86%, 820x1180 5.06%, 810x1080 5.03%.
- Browser viewports (screen less the browser's bars): Playwright 1.61.1 `deviceDescriptorsSource.json` (installed copy under `~/miniforge3/.../playwright/driver/package/lib/server/`, read for the rows named). iPhone 13 and 14: viewport 390x664 on a 390x844 screen. iPhone 15: 393x659 on 393x852. iPhone 11: 414x715 on 414x896. Pixel 7: 412x839 on 412x915. Thus iOS Safari takes approximately 180 to 190 px and Android Chrome approximately 76 px. The iPad and desktop rows give no screen-less-bars figure (the iPad rows equal common screen sizes; "Desktop Chrome" is a fixed 1280x720 test default). These are the Playwright team's device figures, not a usage survey.
- No published source gives the distribution of desktop or tablet viewport heights. StatCounter publishes screens only. Adrian Roselli, "Where's the Viewport Size Data?" (2012, search result title only) says the same.

### V1. check-layout.py `HEIGHTS = (640, 900, 720)`: the first-screen height for phone, tablet and desktop (line 79)

- Class: DESIGN CLAIM. Each value claims the visible height of a common device's browser, which sets "the call to action is on the first screen".
- Disposition, per band:
 - Phone 640: **CONFLICTS, small and on the strict side.** The comment derives it from "a 390x844 phone" less the browser's bars. Playwright gives that device's viewport as 664. 640 is 24 px (3.6%) lower. The most common phone screens give taller viewports: 414x896 (13.3%) gives 715 in iOS Safari; 360x800 (7.6%) gives approximately 724 in Android Chrome (800 less 76, my estimate). Thus 640 is below every common phone's first screen.
  - Tablet 900: **CONFLICTS with its own derivation; the value is on the strict side.** The comment names "a 1024x1366 tablet", but 1024 is outside the band (768 to 1023 px wide), and 1366 less bars is approximately 1290, not 900. The common screens inside the band are 768x1024 (8.1%), 800x1280 (7.9%), 820x1180 (5.1%) and 810x1080 (5.0%). Less approximately 75 px of browser bars (my estimate), the shortest is approximately 950. Thus 900 is approximately 50 px below the shortest common tablet first screen.
  - Desktop 720: **CONFLICTS with its own derivation; size of the error not measured.** 768 less 720 is 48 px. That is less than the operating-system taskbar plus the browser's tab strip and toolbar together, so a maximized browser on a 1366x768 screen shows less than 720. The value does fit a different device: the second most common desktop screen, 1536x864 (10%, a 1920x1080 panel at 125% scale), less approximately 145 px of bars (my estimate, not measured) gives approximately 720.
- GAP: the right height is a point on a measured curve (the share of visitors who see the call to action). No published viewport-height distribution exists. A measurement can close most of it without the founder: `window.innerHeight` in a maximized Chrome and Edge on Windows 11 at 1366x768 and 1536x864, and in iPadOS Safari at 768x1024. The founder decides only how strict the check must be (for example, "the call to action is visible on 90% of devices"), which is a taste or business fact.
- Founder ruling: #78 Q5 (A) (13 Oct 2026) accepted "a stated viewport height per width band" without numbers. The numbers came from the build agent (#78 build note: "Viewport heights are chosen, not measured").
- Correction: correct the comment's devices (phone: 390x844 = 664 by Playwright, 640 is a 24 px margin; tablet: 768x1024; desktop: 1536x864 or 1366x768 with a measured toolbar height).
- Confidence: high for the phone (Playwright figures). Medium for tablet and desktop, until the innerHeight measurement.

### V2. check-layout.py `LOW, HIGH = 320, 1920` and check-measure.py `NARROWEST, WIDEST = 320, 1920` (lines 72 and 59)

- Class: DESIGN CLAIM (the narrowest and widest widths a page must work at).
- Disposition:
  - 320: **SOURCED, but for a different reason than the comments give.** WCAG 2.2 SC 1.4.10 Reflow (https://www.w3.org/WAI/WCAG22/Understanding/reflow.html, read through a fetch summary with exact quotes): "Vertical scrolling content at a width equivalent to 320 CSS pixels"; "320 CSS pixels is equivalent to a starting viewport width of 1280 CSS pixels wide at 400% zoom." The check-layout comment says "the narrowest phone in use". StatCounter shows no phone row below 360 wide in September 2026. Thus 320 is the WCAG reflow width (a desktop user at 400% zoom), not a phone. Change the comment to cite 1.4.10.
  - 1920: **CONFLICTS, small.** 1920x1080 is the most common desktop screen (28.1%). But at least 5.7% of desktop screens are 2560 CSS px wide (2560x1440 3.95%, 2560x1600 1.74%), and more may be in "Other". A layout with no maximum width can fail only above 1920 (a stretched line, a gap between columns). The sweep never renders those widths.
- Founder ruling: **yes, for check-layout. The founder accepted #78 Q5 (A), "the sweep as filed", on 13 Oct 2026. The filed sweep was "every width from 320 to 1920 px". That ruled upper bound departs from the research: it leaves out at least 5.7% of desktop screens (2560 px wide, StatCounter September 2026).** A fix is cheap: add one render at 2560 to the screenshots and the measure check, not a full 5 px sweep to 2560. The founder ruled on agent advice, so no question is necessary unless the correction changes the gate's cost.
- check-measure's comment ("A first guess at common screens, unmeasured") is wrong about 320 for the same reason. Its two ends are the same as check-layout's, so the same correction applies.
- Confidence: high (primary data and the WCAG text).

### V3. check-layout.py `BANDS`: splits at 768 and 1024 px, "the usual tablet and desktop breakpoints" (line 76)

- Class: DESIGN CLAIM (a convention).
- Disposition: SOURCED. Tailwind CSS default breakpoints (https://tailwindcss.com/docs/responsive-design, read): `md` 48rem (768px), `lg` 64rem (1024px). Bootstrap 5 uses 768 for `md` but 992 for `lg`, so "usual" is true for Tailwind and true for 768 only in Bootstrap.
- Founder ruling: none found. Confidence: high. Add the Tailwind citation to the comment.

### V4. check-layout.py `SHOT_WIDTHS` 390 and 1440, "a common phone (390) and desktop (1440)"; check-access.py `VIEWPORTS = (("desktop", 1440, 720), ("phone", 390, 640))` (lines 82 and 81)

- Class: DESIGN CLAIM ("common").
- Disposition:
  - 390: SOURCED as common, not the most common. 390 wide is 6.0% of phone screens and fourth by width (360 16.3%, 414 13.3%, 384 10.4%).
 - 1440: **CONFLICTS.** 1440 wide is 2.94% of desktop screens (1440x900), seventh in the named rows. The common desktop widths are 1920 (29.1%), 1536 (11.5%), 1280 (10.4%) and 1366 (8.0%). 1440 is a design-tool frame width, not a common screen. The check-layout comment cites design-critique §5's render widths as the reason. Thus this departure is inherited from `design-critique/SKILL.md` line 101 (`--viewport 1440x900`).
  - check-access's heights come from V1 (720 and 640) and take V1's disposition.
- Effect: the sweep in check-layout covers every width at 5 px, so the screenshot width matters only for what the critic sees. check-access measures only at 1440 and 390, so a contrast or target fault that appears only at another width is not seen. That is a smaller risk, because contrast seldom changes with width.
- Founder ruling: none found on 1440 or 390.
- Confidence: high on the shares. If the vault keeps one desktop render, 1536 or 1920 is better supported than 1440.

### V5. check-measure.py `--height` default 900 (line 324)

- Class: NOT A DESIGN CLAIM. Characters per line do not depend on the viewport height, except for a page that sizes text or columns in `vh` units.
- Measurement: none necessary for the common case. For consistency, use the V1 band heights. A page with `vh`-sized text needs the real band height, which V1's measurement gives.
- Founder ruling: none found. Confidence: high that the value has almost no effect.

### V6. contact-sheet.py `--phone` default 390x844, "a common phone's viewport ... a guess" (line 219)

- Class: DESIGN CLAIM ("common phone viewport").
- Disposition: **CONFLICTS, small.** 390x844 is a common phone SCREEN (6.0%, fourth). It is not a viewport: Playwright gives that device's Safari viewport as 390x664. The most common phone screen is 414x896 (13.3%). A frame at 390x844 shows approximately 180 px more page than a visitor sees with Safari's bars shown.
- Effect: a motion that starts below the first screen appears in the sheet as if visible. This matters for an entrance animation tied to the first screen.
- Correction: use 390x664 (or V1's phone height) and change the comment to cite Playwright's iPhone 13/14 viewport and StatCounter.
- Founder ruling: none found. #71's build note records the choice as an agent's ("Phone size is a viewport width only ... 390x844").
- Confidence: high.

### C1. contact-sheet.py `TILE = {"desktop": 320, "phone": 180}`, `SHEET_WIDTH = 1680`, `SHEET_SCALE = 2` (lines 50-55)

- What they do: each frame becomes a tile 320 CSS px wide (desktop, a quarter of the 1280 px frame) or 180 (phone). Tiles wrap at 1680 CSS px. The sheet is drawn at device scale 2.
- Class: NOT A DESIGN CLAIM. They are presentation knobs for the reader of the sheet: a Claude critic and the founder. A primary source bounds them for the critic.
- Source that bounds them: Claude vision docs (https://platform.claude.com/docs/en/build-with-claude/vision, read in full, 14 Oct 2026). "Claude 4.7 and later models": max long edge "2576 px", "4784" visual tokens; one visual token is a 28x28 px patch; "Images larger than either limit are downscaled before processing". Limitations: Claude "might hallucinate or make mistakes when interpreting ... very small images under 200 pixels".
- My calculation ( the sheet's header and caption heights are approximate): a desktop sheet with 5 or more frames is approximately 3392 px wide at scale 2, so the model downscales it to 2576. A desktop tile reaches the critic approximately 486 px wide for a 1 s or 2 s motion, 429 px for 5 s and 322 px for 10 s. A phone tile reaches the critic approximately 360, 292, 241 and 172 px wide for 1, 2, 5 and 10 s. Thus the phone tiles of a motion of approximately 8 s or more fall below the 200 px line in the docs. Scale 2 gives the critic no extra detail when the sheet is wider than 2576 px; it helps only the founder on a high-density screen.
- Measurement that sets them: (1) the effective tile width after the model's resize, for the longest motion the vault reviews; keep each tile at 200 px or more. (2) A fixture with a known one-frame fault (a jolt or a missing element) at each tile size; find the smallest tile at which a fresh critic finds it. Split a long motion into more than one sheet before the tile shrinks below that size.
- Founder ruling: none found. #71's build and review notes do not discuss tile size.
- Confidence: high for the vision limits (primary). Medium for my sheet-height model. I did not check whether Claude Code's Read tool resizes an image before the model's own resize.

### M1. check-measure.py `SHOWN = 3`: out-of-range lines quoted for each block before the rest are only counted (line 62)

- Class: NOT A DESIGN CLAIM. It is a report-length knob.
- Measurement: in the critic runs that #86 already pressure-tested, count whether a critic ever needed a fourth quoted line to name the fault or to find it on the page. If no critic did, 3 is sufficient. A plain alternative: quote the shortest and the longest out-of-range line, which names both ends of the fault.
- Founder ruling: none found. Confidence: medium.

### M2. check-measure.py `words(text, n=8)`: the first eight words, "enough to find the line on the page" (line 250)

- Class: NOT A DESIGN CLAIM. It is a report knob.
- Measurement: over a sample of real pages, take every counted line and find the share whose first n words are unique on the page. Choose the smallest n that makes almost all lines unique. A search in the page for the quoted words is how a reader finds the line, so uniqueness is the test.
- Founder ruling: none found. Confidence: medium that 8 is enough for prose; boilerplate lines (for example, repeated card text) can repeat at any n.

### O1. Other bare constants in the same files

- check-access.py `EDGE_LINES = range(-2, 3)` (line 108): lines read as a control's edge. Offsets -2 and -1 are outside the box; 0, 1 and 2 are the box's first three pixel rows (offset 0 is the first row inside, `side_lines` line 410). Thus the comment "2 px outside the box to 3 px inside it" is correct. NOT A DESIGN CLAIM. Measurement: the same fixture set as A3 (common border and ring styles). No founder ruling.
- check-access.py `BOLD_CUE = 600` (line 99): the comment gives its reason (G183 names bold with no figure; 600 is CSS semibold). A DESIGN CLAIM with a stated GAP in WCAG. Not a "guess" constant; not audited further here.
- higgsfield.js `withRetry`: at most 3 tries, waits of 2 s and 4 s (lines 179-188). The comment cites the docs for WHAT to retry. The Errors page says "Use exponential backoff with jitter. Set maximum attempts and a total retry deadline." The docs give no numbers. NOT A DESIGN CLAIM. The script adds no jitter; one sequential worker does not need it (same reason as H1). No founder ruling.
- check-layout.py `GATE_STEP = 5` and contact-sheet.py `GAP = PAD = 16`: each comment states a reason (#78's "at most 5 px"; one caption line and a little more). Not audited further.

## Summary

| # | Constant | Class | Disposition | Founder ruled? |
|---|---|---|---|---|
| H1 | higgsfield poll 2 s, x1.5, 10 s | engineering (vendor value) | SOURCED: Higgsfield Polling page, exact match; the "guess" comment is wrong | no |
| H2 | higgsfield timeout 10 min | engineering | measure: time to `completed` per model from the ledger | no |
| R1 | review.js pause 900 ms | claim in comment; engineering in use | CONFLICTS for "ends a burst" (research: 1-2 s); acceptable as a save debounce | no |
| A1 | DRAWN 1.05 | design claim | CONFLICTS: four systems ship deliberate surface steps at 1.03-1.05; Tailwind gray-50 on white is 1.044, approximately 6 JNDs | no |
| A2 | WORST_SHARE 5% | mixed | CONFLICTS in part: WCAG F83 has no area allowance behind letters; noise allowance needs fixtures | no |
| A3 | AROUND (3, 6) | engineering | measure with common ring styles | no |
| A4 | WRAP 12, WRAPPERS 3 | engineering | measure over real controls | no |
| A5 | FILL_INSET 4 | engineering | harmless at 1-2 px borders (#163 mutation evidence); measure thick borders | no |
| V1 | HEIGHTS 640/900/720 | design claim | phone CONFLICTS small (664 by Playwright; strict side); tablet and desktop derivations wrong; GAP: no published viewport-height curve, measurable | numbers no (#78 ruled only "a stated height") |
| V2 | 320-1920 span | design claim | 320 SOURCED (WCAG 1.4.10, not "narrowest phone"); 1920 CONFLICTS small (5.7%+ of desktops are 2560) | **yes, #78 Q5 (A): departs from research at the top end** |
| V3 | bands 768/1024 | design claim | SOURCED (Tailwind md/lg) | no |
| V4 | shot widths 390 and 1440 | design claim | 390 SOURCED as common; 1440 CONFLICTS (2.9% of desktops; inherited from design-critique §5) | no |
| V5 | check-measure height 900 | engineering | almost no effect | no |
| V6 | contact-sheet phone 390x844 | design claim | CONFLICTS small: a screen, not a viewport (390x664) | no |
| C1 | tile 320/180, sheet 1680, scale 2 | engineering, bounded by Claude vision limits | measure: tile width after the model's resize; phone tiles drop below 200 px at approximately 8 s or more | no |
| M1 | SHOWN 3 | engineering | measure in critic runs | no |
| M2 | first 8 words | engineering | measure uniqueness of n-word prefixes | no |
| O1 | EDGE_LINES -2..2 | engineering | comment correct; measure with A3 fixtures | no |

Questions for the founder: none is necessary from this group. V1's strictness ("the call to action is visible on what share of devices") is the only taste or business fact, and the strict values now in the script are a safe default until he asks for it.

Bound: read in full: the Higgsfield Polling, Rate limits and Errors pages; WCAG F83; the Claude vision page; Dhakal et al. 2018 results section (Table 3 and the IKI paragraph); StatCounter September 2026 CSV exports (top 20 rows plus Other, three device classes); the Playwright 1.61.1 device rows named in V1; Tailwind theme.css colour lines and the responsive-design breakpoint table; Bootstrap 5.3.3 `_variables.scss` lines named; the repo's `docs/research/de00-greys.md` G1 and G1a; the code of every constant above; issues #78, #71, #163, #86, #18, #120 grepped for rulings. Sampled or read through a summary only: WCAG Understanding 1.4.3, 1.4.10 and 1.4.11 (by keyword or fetch summary); Chenu et al. 2014 (fetch summary with exact quotes); Chenoweth and Hayes 2001 (secondary citations only, original not read); Palin et al. 2019 (abstract only); DICOM PS3.14 chapter 7 (constants by fetch summary; the equation form is from memory but reproduces the standard's end points); Tailwind box-shadow page (first 100k characters); react-autosave README (fetch summary); Adrian Roselli 2012 (title only). Not measured: browser toolbar heights on desktop and tablet (V1), the noise floor for DRAWN (A1), the WORST_SHARE fixtures (A2), Claude Code's own image resize (C1).

## Owners

Every correction here: #197.
