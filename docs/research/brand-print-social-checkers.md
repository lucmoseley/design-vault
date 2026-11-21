# Research #262: outside checkers for brand-art, print and social rules

Date: 15 Oct 2026. Question: design-vault#262. Criteria: design-vault#250 (a) finds, (b) threshold, (c) upkeep, (d) licence, (e) packaging.
Machine: WSL2 Linux. Node and Python 3 are on PATH. ffmpeg, ffprobe, tesseract, gs, qpdf, java and exiftool are not on PATH (prompt; checked below).
Throwaway installs and runs used a job directory (`…/tmp/` below) that is not kept. Nothing is installed in the repo.

Key: PASS, FAIL, PART (partly), N/A. "dl/wk" = npm downloads in the last week (api.npmjs.org). "Release" = date of the latest stable version on the registry.

## 1. SVG vector art

House rules: (R1) every curve is a true curve, and no run of short lines stands in for a curve. (R2) Tangents agree at a node where two curves meet. (R3) A morph: both ends have one command structure (same subpaths, same order, holes as subpaths, same commands, arcs written as C). R1 and R2 are code now: `plugin/skills/design-round/scripts/check-curves.js` (hand-written tokeniser, MIN_RUN 4, MIN_TURN 0.5°, MAX_TURN 30°, NEAR_TANGENT 0.1 rad from FontBakery). R3 is code now: `check-flow.py` refuses a morph whose command structure changes, and writes `morph.svg` for check-curves (SKILL.md line 266).

Runs made (throwaway dir `/home/lucmo/.claude3/jobs/8e34e1ae/tmp/svgo/`, `npm i --ignore-scripts`): svgo 4.1.0 install 3.5 s, 12 MB; svg-path-commander 2.3.3 + svg-pathdata 9.0.0 install 1.6 s.

### svgo 4.1.0
- (a) FAIL. svgo has no lint or report mode. `svgo --help` lists only rewrite options (input, output, precision, config, multipass, pretty, folder); no check, lint or dry-run flag. It reports no finding of any kind.
- (b) N/A (no rule).
- (c) PASS. Released 2026-08-24; 39,635,559 dl/wk (`npm view svgo time`; api.npmjs.org, week 2026-10-06..12).
- (d) PASS. MIT.
- (e) PASS. npm, 7 pure-JS deps (sax, csso, css-tree, css-what, commander, css-select, picocolors); install 3.5 s.
- **Fact that changes the house approach: svgo's default preset breaks the morph rule.** `convertPathData` is in `preset-default` (`plugins/preset-default.js` line 65), with `curveSmoothShorthands`, `straightCurves`, `lineShorthands`, `convertToQ`, `convertToZ` and `makeArcs` all on by default (`plugins/convertPathData.js` lines 77-91). `makeArcs` rewrites a C or S that fits a circle as an `a` arc (lines 429-436). Run on a morph pair with one structure (4 × C each), default preset:
  - end A in: `M 50 100 C … C … C 150 116.667 150 133.333 150 150 C … Z` → out: `M50 100c…s…v50H50Z` (c, s, v, H)
  - end B in: 4 × C → out: `M50 100c…` 4 implicit c
  - The two ends now have different commands. A C whose control points sit on the chord (the morph's straight side, which the house draws as C) becomes `v`/`H`. A second C becomes the shorthand `s`.
- Also: `mergePaths` (in preset-default, line 69) joined two `<path>` elements into one `d` in the same run (`poly.svg`), which changes the subpath count of a shape.
- Also: svgo does not touch a polyline standing in for a curve (`poly.svg`: the 6-segment arc stayed as lines). It neither finds nor fixes R1.
- Rule for the house: never run svgo (or any optimiser with `convertPathData` on) over a morph's ends or keyframes. If svgo is used on static art, run it before `check-curves.js`, not after it, and disable `convertPathData` and `mergePaths` for morph files.

### svglint 4.2.1
- (a) FAIL. Built-in rules are only `elm` (element presence and count), `attr` (attribute values, a regex on `d` at most) and `valid` (XML validity). No geometry rule. A custom rule gets the Cheerio DOM and can read `d`, but then the house writes the check itself (https://github.com/simple-icons/svglint README).
- (b) N/A.
- (c) PASS. Released 2026-02-21; 20,709 dl/wk.
- (d) PASS. MIT.
- (e) PASS (npm, pure JS: cheerio, fast-xml-parser, htmlparser2, glob and 5 more).
- It adds nothing that `check-curves.js` lacks.

### @resvg/resvg-js 2.6.2
- (a) FAIL. It is a renderer (SVG to PNG), with no lint rule.
- (b) N/A.
- (c) FAIL. Latest stable 2.6.2 is from 2024-03-26 (`npm view @resvg/resvg-js time`); `next` is 2.7.0-alpha.2. The 4,012,475 dl/wk do not make up for no stable release in 12 months.
- (d) PASS. MPL-2.0.
- (e) FAIL. 12 per-platform native optionalDependencies (`@resvg/resvg-js-linux-x64-gnu` and others).
- Note: Playwright's Chromium already renders SVG for `look-renders.py`; resvg adds nothing.

### svgpath 2.6.0, svg-pathdata 9.0.0, svg-path-commander 2.3.3 (path parsers)
- (a) FAIL for all three. They parse and transform path data. None reports a polyline standing in for a curve, a tangent break or a structure mismatch.
  - svg-path-commander has predicates. `isPolylineArray` is true for any M+L path (a rectangle too), so it is not R1. `isCurveArray` is `isNormalizedArray(path) && every command in "MC"` (source printed by `node -e`), so it returns false for a closed C path with Z. It also has `equalizePaths` / `equalizeSegments`, which split segments to make two paths match: a rewrite that changes the authored structure, which R3 does not allow.
  - svg-pathdata has `A_TO_C`, `NORMALIZE_ST`, `QT_TO_C` and `REMOVE_COLLINEAR` transformers (exports listed by `node -e`). Rewriters, not checks.
- (b) N/A.
- (c) svgpath FAIL (last release 2022-10-28, 1,543,077 dl/wk). svg-pathdata PASS (2026-03-27, 15,193,284 dl/wk). svg-path-commander PASS (2026-09-02, 117,889 dl/wk).
- (d) PASS. MIT, all three.
- (e) PASS. svg-pathdata has 0 deps; svg-path-commander has 1 (`@thednp/dommatrix`); svgpath 0.
- Possible use: svg-pathdata could replace `check-curves.js`'s own `tokenise()` (a parser seam only). The rule logic stays the house's. Not worth a dependency for one function that works now.

### FontBakery 1.1.0 (outline checks)
- (a) FAIL for SVG. Its outline checks (`outline_colinear_vectors`, `outline_jaggy_segments`, `outline_short_segments`, `outline_alignment_miss`, `outline_semi_vertical`, `outline_direction`) run on a font: `check_outline_colinear_vectors(ttFont, outlines_dict, config)` with condition `outlines_dict` (fonttools/fontbakery `Lib/fontbakery/checks/outline_colinear_vectors.py`). They do not read an SVG file.
- (b) PART. Its constants are fixed in `outline_settings.py` (COLINEAR_EPSILON 0.1 rad, JAG_ANGLE 0.25 rad, SHORT_PATH_EPSILON 0.006). `check-curves.js` already takes COLINEAR_EPSILON from it.
- (c) PASS. 1.1.0 released 2025-10-02 (inside 12 months); 2,871 dl/wk (pypistats.org API).
- (d) PASS. Apache-2.0 (GitHub licence API).
- (e) FAIL as a fit: 60 requirements (PyPI `requires_dist`), Python only.
- Note: `JAG_ANGLE` (0.25 rad) and `outline_jaggy_segments` are the only further idea to borrow: a sharp turn inside a smooth outline.

### Other SVG tools found
- picosvg 0.23.0 (Apache-2.0, 2026-08-14): rewrites an SVG to a small subset ("absolute coordinates, no H or S"), uses skia-pathops (native) for clips and strokes; no report mode (https://github.com/googlefonts/picosvg README). FAIL (a), weak (e).
- svgcheck 0.12.0 (BSD-3-Clause, 2026-04-17): the IETF RFC SVG profile checker (element and attribute allow-list for RFCs). No geometry rule. FAIL (a). Not run.
- svgpathtools 1.8.0 (MIT, 2026-09-05, pure Python): a geometry library (curvature, tangents, intersections). It could compute R2 tangents, but it is a library, not a rule. FAIL (a).

### Family verdict: build (keep `check-curves.js` and `check-flow.py`'s morph check)
No tool has a rule for R1, R2 or R3, so (a) fails for every candidate. Fact for the house: FontBakery's `outline_jaggy_segments` (JAG_ANGLE 0.25 rad) is a further rule the house could borrow, as it borrowed COLINEAR_EPSILON.

## 2. Raster brand art (AI-rendered PNG or JPEG)

Measurements asked: (M1) pixel size against the model's largest size (roster.md gives it, for example Grok Imagine 2k = 2816×1584); (M2) colour count and ΔE00 to the named palette; (M3) a region left plain for a headline (low texture); (M4) a painted checkerboard where transparency was asked (roster.md line 30: Grok Imagine "Paints a checkerboard where transparency is asked for"); (M5) text, logos or UI baked into the image (SKILL.md line 272: "never baked into an image"); (M6) a mobile crop keeps the focal element.

House code already present: `plugin/skills/design-project/scripts/colour_space.py` has `de2000()`, `lab()`, `contrast()`; `palette.py` uses them. Pillow 12.3.0 here has littlecms2, webp, jpg, libtiff, freetype2 and raqm; libimagequant is absent (`PIL.features.check`). numpy 2.4.6.

Fixtures made (`/home/lucmo/.claude3/jobs/8e34e1ae/tmp/scripts/mkfix.py` → `…/tmp/fixtures/`), 1200×800: `clean.png` (painted-like colour field with blurred noise, no text), `text.png` (same ground, "BOOK NOW" 90 px light serif + "Open daily 9-5" 28 px dark), `garbled.png` ("BOKKO NWOW" 90 px, as image models misspell), `checker.png` (20 px white/#ccc checkerboard with a red disc).

### tesseract.js 7.0.0 (M5)
- (a) FAIL on the fixtures. Run: `node …/tmp/scripts/ocr.js` with local `langPath` (`@tesseract.js-data/eng/4.0.0_best_int`), no network.
  - `clean.png`: confidence 31, about 120 junk "words" with per-word confidence up to 93 (for example `4(93)`, `\(80)`, `1(81)`). A false positive unless the house adds a filter.
  - `text.png`: found "Open daily 9-5" at 96, but **missed the 90 px "BOOK NOW" headline**: the large light display text that an image model is most likely to bake in.
  - `garbled.png`: "NWOW" at 77 among junk.
  - `checker.png`: nothing.
  - A filter "≥3 alphanumeric characters and confidence ≥80" leaves `clean` empty and finds only the small line in `text`. Tesseract is a document OCR: it reads dark body text, not display text on a painted ground.
- (b) PART. Confidence is per word; the house would set its own cut. There is no "is text present" threshold.
- (c) PASS. 7.0.0 released 2025-12-15 (inside 12 months); 3,425,510 dl/wk.
- (d) PASS. Apache-2.0 (tesseract.js and tesseract.js-core); `@tesseract.js-data/eng` MIT.
- (e) PART. The OCR engine is WASM inside the npm package (`tesseract.js-core/*.wasm`), not a native binary. **Language data is fetched from a CDN at run time by default**: `src/worker-script/index.js` line 127-130, "If `langPath` if not explicitly set by the user, the jsdelivr CDN is used" (`https://cdn.jsdelivr.net/npm/@tesseract.js-data/${lang}/4.0.0…`). The fix: install `@tesseract.js-data/eng` 1.0.0 from npm (MIT, 13.9 MB, 507,587 dl/wk, released 2023-09-04) and set `langPath` to it, as in the run. Install time: tesseract.js 3.1 s (51 MB), + eng data 2.3 s.
- Verdict: do not adopt.

### PaddleOCR PP-OCRv4 text detector (DBNet) on onnxruntime-web 1.30.0 (M5)
- (a) PASS on the fixtures (4 of 4). Run: `…/tmp/scripts/det-prep.py` (Pillow: 960 px long side, ImageNet mean/std, BGR) then `…/tmp/scripts/det-run.js` (onnxruntime-web, WASM backend, in Node; threshold 0.3 on the probability map, 4-connected blobs ≥20 px):
  - `clean.png`: text-pixel share 0.0000, 0 blobs.
  - `text.png`: share 0.0178, 2 blobs (9,400 px headline, 1,554 px small line).
  - `garbled.png`: share 0.0195, 1 blob (11,968 px).
  - `checker.png`: 0 blobs.
  - It is a detector: it says where text is, not what it says. That is all M5 needs ("any baked text is a fault"). Synthetic fixtures only; real AI renders with lettering-like texture (signage, script patterns) are not tested.
- (b) PASS. The house sets the probability cut, the minimum blob size and any allowed area.
- (c) PART. onnxruntime-web: PASS (1.30.0, 2026-09-14, 5,921,149 dl/wk). Model source PaddleOCR: active (v3.7.0 2026-06-11). The npm carrier used here, `@gutenye/ocr-models` 1.4.2, FAILS (last release 2024-05-20; 25,838 dl/wk). Vendor the one det model instead.
- (d) PASS. onnxruntime MIT (GitHub licence API, microsoft/onnxruntime); PaddleOCR Apache-2.0 (GitHub licence API). `@gutenye/ocr-models` says MIT but carries PaddleOCR's Apache-2.0 models: keep the Apache NOTICE if vendored.
- (e) PASS with weight. onnxruntime-web is WASM, no native binary, no install script needed (`--ignore-scripts` run works); unpacked 144.6 MB; install with the models 5.7 s (163 MB `node_modules`). The det model `ch_PP-OCRv4_det_infer.onnx` is one 4.7 MB file: it can be vendored with a hash test. Session start 1.7 s, 0.3-0.8 s an image on this machine. Not to be confused with `onnxruntime-node` 1.30.0 (301 MB, native, `global-agent` + `adm-zip` deps for its install-time fetch): FAIL (e).
- Verdict: **adopt as a building block** (onnxruntime-web from npm + the vendored det model). The rule logic (thresholds, which areas may hold text) stays a vault script.

### smartcrop 2.0.5 (M6)
- (a) FAIL. It picks the "best" crop by its own skin, saturation and edge score (README, https://github.com/jwagner/smartcrop.js). It does not test whether a given crop keeps a named focal element. The house rule needs the brief's focal element, which only the brief names.
- (b) PART (its weights can be set).
- (c) FAIL. Last release 2021-09-01; 49,063 dl/wk. smartcrop-sharp 2.0.8 is from 2023 and needs sharp (native).
- (d) PASS. MIT.
- (e) PASS (0 deps, 30 kB).
- Not run, since (c) fails.

### image-q 4.0.0 and quantize 1.0.2 (M2)
- (a) N/A as checkers: they reduce colours; they do not test conformance. image-q has a CIEDE2000 distance (`dist/types/src/distance/ciede2000.d.ts` in the 4.0.0 tarball), which the house already has in `colour_space.py` `de2000()`.
- (c) FAIL both. image-q last release 2022-01-08 (3,575,938 dl/wk, mostly via jimp); quantize 2016-04-06.
- (d) PASS (MIT). (e) PASS.

### Pillow (present), for M1-M4
- M1: `Image.open(p).size` against the roster's size. One line; build.
- M2: `Image.getcolors()`, `Image.quantize()` (median cut and fast octree work without libimagequant) give the main colours; the house's own `de2000()` scores each against the palette. Build.
- M3: numpy local standard deviation or gradient energy over the headline box. No library has this as a rule. Build.
- M4: no tool found. A checkerboard is a periodic two-tone grid (white and #ccc or similar); a numpy test on cell-mean alternation or a 2D FFT peak finds it. Build.
- (c) Pillow is the house's existing dependency; (d) MIT-CMU (HPND); (e) machine-wide, already present.

### Family verdict: build, with one building block to adopt
M1-M4 and M6: build on Pillow + numpy + `colour_space.py`; no tool has the house's rule. M5 (baked text): adopt onnxruntime-web + vendored PP-OCRv4 det model as the detector inside a vault script; do not adopt tesseract.js (it missed the headline and reads junk on painted grounds).

## 3. Logo placement

House rules: (L1) placed logo pixels equal the supplied file, never recoloured (SKILL.md line 59: "place the logo from that file"); (L2) every logo colour reaches 3:1 on its ground; (L3) clear space around the mark, in units of the mark (the rules file holds it).
L2 is code now: `palette.py` reports "which grounds the full-colour logo clears at 3:1" (its header).

Fixtures: `logo.png` (200×120, navy #142878 bar + red #dc3c28 disc, transparent ground), `placed-exact.png` (logo pasted at 300,140 on #f5f0e6), `placed-recolour.png` (same, blue channel +6 on logo pixels). The recolour is ΔE00 1.03 (navy) and 1.41 (red) by the house's `colour_space.de2000()`. Pillow `ImageChops.difference`: bbox (310,150,491,251), max channel difference 6. Runs: `…/tmp/scripts/diff.mjs` (install of pixelmatch 8.0.0 + pngjs + looks-same 10.0.1: 1.7 s, 1.6 MB).

| Compare to placed-exact | pixelmatch t=0.1 (default) | t=0.05 | t=0 | looks-same default (ΔE00 2.3) | looks-same tolerance 0 / strict |
|---|---|---|---|---|---|
| placed-exact | 0 px | 0 | 0 | equal | equal |
| placed-recolour | **0 px (missed)** | **0 (missed)** | 14,602 px | **equal (missed)** | not equal |

### pixelmatch 8.0.0
- (a) PART. At its default it misses a ΔE00 1-1.4 recolour; at threshold 0 it finds it. No false positive on the exact placement. It needs an expected image of the same size: the house must render the supplied file at the placed size on the same ground first. It ignores anti-aliased pixels unless `includeAA: true` (README line 47).
- (b) PASS. `threshold` 0-1, "a per-pixel perceptual color difference" (README line 46). It is a YIQ-based scale, not ΔE00, so the house's ΔE00 rule does not map onto it directly.
- (c) PASS. Released 2026-10-06; 10,816,100 dl/wk.
- (d) PASS. ISC (OSI).
- (e) PASS. ESM, one dep (pngjs); 37 kB.

### looks-same 10.0.1
- (a) PART. Same as pixelmatch: default misses the recolour, `tolerance: 0` / `strict: true` finds it, no false positive on the exact placement.
- (b) PASS, and the closest fit. `tolerance` is a CIEDE2000 value: `makeCIEDE2000Comparator(tolerance)` with `colorDiff.diff(lab1, lab2) < tolerance` (`index.js` lines 22-77); default 2.3 is its "Just noticeable difference" (`lib/constants.js` line 19). The house already writes palette rules in ΔE00.
- (c) PASS. Released 2025-08-18 (inside 12 months); 130,347 dl/wk.
- (d) PASS. MIT (Yandex). Its PNG codec `@jsquash/png` 3.1.1 is Apache-2.0.
- (e) PASS. Pure JS + WASM PNG codec (`@jsquash/png/codec/pkg/squoosh_png_bg.wasm`), no native binary.

### resemblejs 5.0.0
- (c) FAIL. Last release 2023-06-06; 54,649 dl/wk. (e) FAIL: depends on `canvas` 2.11.2 (native node-canvas). (d) PASS (MIT). Not run.

### odiff-bin 4.5.0
- (c) PASS (2026-07-23; 160,636 dl/wk). (d) PASS (MIT). (e) FAIL: seven per-platform native optionalDependencies (`@odiff/linux-x64` and others). Not run.

### Pillow ImageChops (present)
- (a) PASS on the fixtures (bbox and max difference above). (b) PASS: any threshold, and the house's own `de2000()` can score each pixel. (c)-(e) PASS: already a house dependency.

### L3 clear space
No tool found that measures clear space. It needs the logo's box and the nearest other content's box: Playwright DOM boxes on a page, or a pixel scan on an artboard. Build.

### Family verdict: build (Pillow + the house's `de2000()`)
L1 needs a rendered expected image at the placed size, which is house work in any case. After that the compare is one Pillow call; looks-same would add a ΔE00 tolerance the house already has. L2 is already `palette.py`. L3: build. Fact for the house: **both diff tools at their defaults pass a ΔE00 1-1.4 recolour of a logo**; any L1 check must set its own tolerance (strict, or a ΔE00 the house names).

## 4. Generated video clips (MP4 from Kling or Wan)

House rules: (V1) the start frame equals the end frame (a loop); (V2) clip length inside a range. V2 needs only the container header; V1 needs decoded frames.

Runs made:
- `…/tmp/scripts/codecs.py`: Playwright 1.61.0 (Python), bundled Chromium 149.0.7827.0, headless, on a routed `https://probe.test/` page (WebCodecs needs a secure context; on `about:blank` `VideoDecoder` is undefined). Result for both the default build and `channel: "chromium"`: H.264 (`avc1.42E01E`, `avc1.640028`) `canPlayType` "", `MediaSource.isTypeSupported` false, `VideoDecoder.isConfigSupported` false; HEVC the same; VP9 and AV1 "probably" / true / true. `channel: "chrome"` failed: "Chromium distribution 'chrome' is not found at /opt/google/chrome/chrome".
- `…/tmp/scripts/mp4info.mjs` (mp4box 2.4.1, from the npm tarball) on the only local MP4 found, `/home/lucmo/design-vault/.claude/drafts/i2/deep/site-khufus/probe/hero.mp4` (a probe of a third-party site, not a Kling or Wan clip): "duration s 10.042", "video avc1.640028 samples 241 … 1788x1156". It is H.264 High, which the bundled Chromium cannot decode.
- Playwright's own ffmpeg (`~/.cache/ms-playwright/ffmpeg-1011/ffmpeg-linux`, LGPL-2.1): its build line has `--disable-everything` and enables only the mjpeg and libvpx VP8 decoders and the matroska and image2pipe demuxers (`-version` output). No H.264 decoder and no MP4 demuxer: not usable.

### ffmpeg / ffprobe
- (a) PASS as a measuring tool (ffprobe duration; frame extraction for V1), with the rule built by the house. (b) PASS (house sets the numbers). (c) PASS (active project). (d) PROBLEM: LGPL-2.1 or GPL by build. (e) FAIL: a per-platform native binary, and absent on this machine.

### imageio-ffmpeg 0.6.0
- (c) FAIL. Last release 2025-01-16, over 12 months ago (PyPI JSON); 5,305,720 dl/wk (pypistats).
- (d) PART: wrapper BSD-2-Clause; the bundled ffmpeg is LGPL/GPL.
- (e) FAIL: "the platform-specific wheels contain the binary executable" (PyPI description); wheels per platform (manylinux2014_x86_64, macOS, win).

### PyAV (`av`) 19.0.1
- (a) PASS as a decoder (H.264 frames in-process; rule built by the house). Not run (not installed; installing machine-wide is outside this task).
- (b) PASS. (c) PASS: released 2026-10-03; 10,175,207 dl/wk (pypistats).
- (d) PART: binding BSD-3-Clause; bundled FFmpeg libraries LGPL.
- (e) WEAK: "Binary wheels are provided on PyPI for Linux, macOS, and Windows with FFmpeg bundled" (PyPI description); per-platform wheels; Python ≥3.12 (this machine's Python is 3.12). Under #250's packaging rule a per-platform native binary fails; as a machine-wide wheel it is the weaker Python route. **The only candidate found that decodes H.264 here without a system binary.**

### mp4box.js (`mp4box`) 2.4.1
- (a) PASS for V2 as a parser (run above: duration 10.042 s, codec, sample count). FAIL for V1: it demuxes samples but does not decode them.
- (b) PASS (the house sets the range).
- (c) PASS. Released 2026-06-19; 584,188 dl/wk.
- (d) PASS. **BSD-3-Clause**, not MIT (`npm view mp4box license`; `LICENSE`: "Copyright (c) 2012. Telecom ParisTech/TSI/MM/GPAC Cyril Concolato").
- (e) PASS. Pure JS, 0 deps, 2.26 MB unpacked.

### Decoding inside Playwright's Chromium
- FAIL for H.264. Playwright: "Chromium does not have all the codecs that Google Chrome or Microsoft Edge are bundling due to various licensing considerations and agreements" and "If your site relies on this kind of codecs … you will also want to use the official channel" (https://playwright.dev/docs/browsers, "Google Chrome & Microsoft Edge"). The Chrome channel is not installed in WSL, and Chrome is not OSI-licensed: (d) fails for that route.
- mp4box.js + WebCodecs in Chromium would work for a VP9 or AV1 clip, not for H.264.

### ffmpeg.wasm (`@ffmpeg/ffmpeg` 0.12.15 + `@ffmpeg/core` 0.12.10)
- (c) FAIL: both last released 2025-01-07.
- (d) PROBLEM: `@ffmpeg/core` is GPL-2.0-or-later (`npm view`).
- (e) FAIL as shipped: the core is fetched from a CDN at run time by default: `CORE_URL = https://unpkg.com/@ffmpeg/core@${CORE_VERSION}/dist/umd/ffmpeg-core.js` (`dist/esm/const.js` line 4). Core 64.7 MB unpacked.

### Others seen, not run
- libav.js 6.10.9 (2026-08-18; LGPL-2.1; 179 MB; 7,820 dl/wk): WASM, (d) LGPL problem.
- tinyh264 0.0.7 (2021) and broadway-player 0.1.1 (2016): (c) FAIL.

### Family verdict
- V2 (length): **build** a small `mvhd` duration reader in Python (one box, no dependency), or **adopt mp4box.js** (passes all five as a parser). Both are cheap; the house rule (the range) is house code either way.
- V1 (start = end frame): **no tool fits** all five. Routes, each with its cost: (1) PyAV wheel machine-wide (LGPL libraries inside, per-platform wheel); (2) ask the model for a VP9/WebM or AV1 output, if it offers one, then decode in Playwright's Chromium with WebCodecs (not checked: whether Kling or Wan offers it); (3) leave V1 to a critic looking at the first and last frames that the model's own preview gives.
- Fact for the house: **Playwright's bundled Chromium cannot decode H.264 MP4** (measured: Chromium 149, `canPlayType` "" and WebCodecs false), so no Playwright-based check can read a Kling or Wan H.264 clip's frames.

## 5. Print (PDF or PNG artboards)

The house has no written print spec. SKILL.md line 269 says only: "Artboards with PNG or PDF export. Any rights holder the project names signs off before print."

### What a preflight checks (primary: Ghent Workgroup user guide, 2026)
Source: `https://gwg.org/wp-content/uploads/2026/07/2026_GWG_USER-GUIDE-PDF-X-workflow.pdf` (36 pages; text read with pypdf, sampled by keyword). ISO 15930 (PDF/X) itself is paywalled and was not read.
- PDF/X itself: "PDF/X documents are by their nature self-contained; all necessary elements such as fonts, images, ICC profiles... are embedded in the file itself. They also must include or define important information such as page boxes, output conditions…". "All PDF/X files contain an 'output intent'. This output intent defines for which print condition the elements within the document have been prepared."
- Beyond PDF/X: "The Ghent Workgroup specifications add requirements for: Minimum and maximum resolution of images; Maximum ink usage (TAC); Minimal line weight and text size; Use of overprint and knockout for specific elements; Usage of spot colors".
- Effective resolution: "determined both by the intrinsic resolution of the image and how that image is used in the design. For example, a 600 ppi resolution that is scaled down to 50% has an effective resolution of 1200 dpi." GWG ships two levels, "GWG2015_..._250ppi" and "GWG2015_..._350ppi". The numeric GWG2015 error and warning limits per segment are in the specification documents, which were not reached (the gwg.org spec PDF link returned an HTML page).
- Colour: the guide recommends "ISO Coated v2 300% (ECI)" as the CMYK profile "for most common printed material" (the 300% is that profile's total ink limit).
- So a preflight checks: (P1) PDF/X version key and output intent; (P2) TrimBox and BleedBox present, bleed size; (P3) every font embedded; (P4) effective image resolution; (P5) colour spaces (no RGB in X-1a; RGB allowed with output intent in X-4; spot colours named); (P6) total ink (TAC) against the profile's limit; (P7) minimum line weight and text size; (P8) transparency (none in X-1a).

### Prototype run: pypdf (already installed, 6.14.2)
`…/tmp/scripts/pdfprobe.py` makes a PDF with Playwright's `page.pdf()` (a text line + a 600×400 px image drawn 3×2 in) and reads it with pypdf only:
- `OutputIntents None | Info GTS_PDFXVersion None` (P1 readable; Chromium writes no output intent).
- `media [0, 0, 576, 432] trim [0, 0, 576, 432] bleed [0, 0, 576, 432]`, and `/TrimBox` and `/BleedBox` keys are present (Chromium writes them equal to the media box: no bleed). P2 readable.
- `font /F4 /AAAAAA+DejaVuSerif embedded True` (P3 readable from `/FontFile*` in the descriptor).
- `image /X5 600 x 400 px, colour space ['/ICCBased', …] drawn 3.0 x 2.0 in, effective ppi 200.0 200.0` (P4 and P5 readable: the CTM tracked through `q`/`Q`/`cm` with `extract_text(visitor_operand_before=…)`; 200 ppi is the planted value).
- Fact for the house: **a PDF from Playwright/Chromium is RGB (ICCBased) with no output intent and no bleed: never PDF/X.** A print file needs another export step.

### veraPDF (library 1.30.3 / tag v1.31.47)
- (a) FAIL. It validates "PDF/A-1, PDF/A-2, PDF/A-3, PDF/A-4, PDF/UA-1, PDF/UA-2 and WTPDF 1.0" (https://docs.verapdf.org/validation/). **No PDF/X.** The repo calls itself "open source PDF/A validation library" (GitHub description).
- (b) N/A. (c) PASS (release 2026-10-09). (d) PASS: dual GPLv3+ / MPLv2+ (README "Licensing"). (e) FAIL: Java 8-25 runtime (README line 32); no Java here.

### Ghostscript
- (a) PART. Not a validator: the Devices page does not mention PDF/X (https://ghostscript.readthedocs.io/en/latest/Devices.html). It can measure ink: `inkcov` counts the share of pixels that mark each of C, M, Y, K; `ink_cov` "also considers the amount of each colourant at each rendered pixel" (page averages, not the per-pixel maximum a TAC rule needs). `tiffsep` writes one gray file per separation, from which a script could compute TAC per pixel.
- (b) PASS via own script. (c) PASS (active). (d) PROBLEM: AGPL-3.0 (or commercial). (e) FAIL: native binary; `gs` absent here.

### pdfcpu v0.16.2
- (a) FAIL. `pdfcpu validate` checks the PDF syntax up to "PDF 2.0 (ISO 32000-2). PDF 2.0 validation support is basic" (README lines 13-16). No PDF/X, ink, or ppi rule seen.
- (c) PASS (2026-10-11). (d) PASS (Apache-2.0). (e) FAIL as a native Go binary per platform; note it also ships a `Js_wasm` build in its release assets (not tried).

### qpdf v12.4.2
- (a) FAIL. `--check` checks "the file's structure as well as encryption, linearization, and encoding of stream data" (https://qpdf.readthedocs.io/en/stable/cli.html). The manual mentions PDF/A only to say qpdf "doesn't specifically know how to generate PDF/A-compliant PDFs"; no PDF/X.
- (c) PASS (2026-09-27). (d) PASS (Apache-2.0). (e) FAIL (native C++; absent here).

### pikepdf 10.17.0
- (a) FAIL (a library on qpdf, no rule). (c) PASS (2026-10-11). (d) PASS (MPL-2.0). (e) WEAK: per-platform wheels with qpdf inside (PyPI files: manylinux, musllinux, macOS, win). pypdf does the same reads here with no native code.

### pypdf 6.20.1 (6.14.2 installed)
- (a) FAIL as a checker (no rule), PASS as the reader for P1-P5 (run above).
- (b) PASS (house sets the numbers). (c) PASS (2026-10-12). (d) PASS (BSD-3-Clause). (e) PASS-weak: pure-Python wheel (`any.whl`), already installed machine-wide.
- It cannot render, so P6 (TAC) and P7 (line weight) are out of its reach.

### pdfjs-dist 6.4.299
- (a) FAIL as a checker; it parses and renders (operator list gives image draws and transforms). (c) PASS (2026-10-03; 33,256,167 dl/wk). (d) PASS (Apache-2.0). (e) PASS-heavy: 34.9 MB; `@napi-rs/canvas` is an optional native dependency, needed only to render in Node.
- It renders to RGB, so it cannot give CMYK separations for P6.

### pdf-lib 1.17.1
- (c) FAIL: last release 2021-11-06 (18,167,409 dl/wk). (d) PASS (MIT). A writer, no rule.

### Scribus Preflight Verifier
- Not reached: the Scribus wiki page (https://wiki.scribus.net/canvas/Preflight_Verifier) returned a bot-block ("Access Denied"). What it checks, and on what input, is not verified. Scribus is a desktop application: (e) FAIL in any case.

### Other PDF/X validators found
- **pdf-compliance 1.0.0** (Rust crate): `validate_pdfx` for "X1a2003, X32003, and X4" (https://docs.rs/pdf-compliance). Licence "AGPL-3.0-only OR LicenseRef-PDFluent-Commercial" (crates.io API). 485 downloads in total, first published 2026-05-02, 1.0.0 on 2026-09-16; earlier betas had a "non-standard" licence. (a) not tested; (c) FAIL (no real use); (d) PROBLEM (AGPL); (e) FAIL (Rust, compiled per platform; library only, no CLI documented).
- **yob/pdf-preflight** (Ruby gem `preflight` 0.3.0, MIT, GitHub licence API): profiles `pdfx1a.rb` and `pdfa1a.rb`; rules include `min_ppi`, `max_ink_density`, `min_bleed`, `only_embedded_fonts`, `no_rgb`, `print_boxes`, `output_intent_for_pdfx`, `no_transparency` (GitHub contents API). (c) FAIL: last gem release 2013-04-28; repo last push 2021-02-24. (e) FAIL: Ruby. **Its rule list is a good checklist to port**, with the house's numbers.
- "lintPDF" (printwithsynergy): seen only in a search snippet (AGPL-3.0, PDF/X-4 suite claimed); its GitHub repo was not found (`gh api repos/printwithsynergy/lint-pdf`: 404). Not verified.

**Does any OSI-licensed PDF/X validator exist?** Yes, two were found, and neither passes #250: pdf-compliance (AGPL-3.0, OSI-approved, about 485 downloads in total, Rust) and the Ruby `preflight` gem (MIT, PDF/X-1a profile, unmaintained since 2013).

### Family verdict: build (pypdf) for P1-P5; no tool fits P6-P7
- P1-P5: build a vault script on pypdf (already installed, pure Python), porting the `preflight` gem's rule list. The prototype above reads every input in about 60 lines.
- P6 (TAC): needs CMYK separations. With no Ghostscript, the route is Pillow `ImageCms` (littlecms2 is present) converting a rendered RGB artboard through the printer's CMYK ICC profile, then summing channels per pixel. Valid only for PNG artboards or a rasterised PDF, and only with the profile the printer names.
- P7 (line weight, text size): no tool; a critic, or a later build.
- First, a house decision is missing: there is no print spec (which PDF/X level, which output profile, which ppi floor, which TAC). The checks cannot take a number until the founder or the printer names one.

## 6. Social images

The house has no written social spec (SKILL.md line 269: "Artboards with PNG or PDF export").

### First-party specs collected

| Surface | Size | Ratio | File size, type | Safe zone with numbers? | Source |
|---|---|---|---|---|---|
| Open Graph protocol | none set | none | none | No | https://ogp.me/ (`og:image:width`/`height` are "The number of pixels wide/high"; page "should specify `og:image:alt`") |
| Facebook link preview (`og:image`) | min 200×200; ≥600×315 for the large preview; recommended ≥1200×630 | "as close to 1.91:1 … as possible" | ≤8 MB | No | https://developers.facebook.com/docs/sharing/webmasters/images/ |
| X `summary_large_image` | min 300×157, max 4096×4096 | 2:1 | <5 MB; JPG, PNG, WEBP, GIF (first frame); "SVG is not supported" | No | developer.x.com cards page, via Wayback snapshot 2026-02-04 (`web.archive.org/web/20260204074639/https://developer.x.com/en/docs/x-for-websites/cards/overview/summary-card-with-large-image`). The live URL now redirects to `docs.x.com/overview`, and the docs.x.com sitemap has no Cards page. |
| LinkedIn link share | min 1200×627; <401 px wide shows as a small thumbnail | 1.91:1 recommended | ≤5 MB | No ("Square and vertical images might be cropped") | https://www.linkedin.com/help/linkedin/answer/a521928 |
| LinkedIn Page post image | 1200×627 | 1.91:1 | PNG/JPEG ≤3 MB (stated in the Pages image section) | No for posts; for cover images only "keep key details away from the edges, especially in the lower-right corner" (no numbers) | https://www.linkedin.com/help/linkedin/answer/a563309 |
| Instagram organic photo | width 320-1080 kept; larger sized down to 1080 | 1.91:1 to 3:4 ("a width of 1080 pixels with a height between 566 and 1440"); outside that "it will be cropped" | not stated | No | help.instagram.com/1631821640426723, Wayback snapshot 2026-09-09 (live page renders only its title to a fetch) |
| Instagram Feed image ad | 1440×1800 | 4:5; min 400×500 ratio, max 191×100; 1% tolerance | ≤30 MB; JPG/PNG; min width 500 | No | https://www.facebook.com/business/ads-guide/update/image/instagram-feed |
| Instagram Stories image ad | 1440×2560 | 9:16, 1% tolerance | ≤30 MB; JPG/PNG; min width 500 | **Yes: top 14%, bottom 35%, 6% each side** free of text, logos and key elements | https://www.facebook.com/business/ads-guide/update/image/instagram-story |
| Instagram Reels image ad | 1440×2560 | 9:16, 1% tolerance | ≤30 MB; JPG/PNG; min width 500 | **Yes: top 14%, bottom 35%, 6% each side** | https://www.facebook.com/business/ads-guide/update/image/instagram-reels |

Notes:
- Only Meta's Stories and Reels ad specs publish a safe zone with numbers. No link-preview spec (OG, Facebook, X, LinkedIn) publishes one. Meta's Ads Guide pages were served in Indonesian to the fetch; the English page was not read.
- Conflict: Instagram's organic help page allows down to 3:4 (1080×1440); the Feed ad spec gives 4:5 (1440×1800). A post made at 4:5 fits both.
- Link-preview ratio: X asks 2:1, Facebook and LinkedIn 1.91:1. One 1200×630 image is 1.905:1; X shows it in a 2:1 frame, so 30 of its 630 rows (4.8%) fall outside the frame if X fits by width (arithmetic; X does not state how it crops).

### open-graph-scraper 6.12.0
- (a) FAIL. Run (throwaway, offline, `ogs({html})`): it returned `[{"height":"630","url":"https://e.test/a.png","width":"1200","type":"png"}]` for tags that claim 1200×630, without fetching the image. On a page with no `og:image` it returned `success: true`, no error. It extracts tags; it checks no size, ratio or file size, and the width and height it gives are the page's claims, not the image's.
- (b) N/A. (c) PASS (2026-06-26; 398,295 dl/wk). (d) PASS (MIT). (e) PASS (4 deps: chardet, cheerio, iconv-lite, undici; install 1.8 s, 12 MB).

### metascraper 5.58.5
- (a) FAIL. A metadata extractor with rule bundles that pick the best title, image and so on from a page (not run; same class as open-graph-scraper). (c) PASS (2026-10-15; 94,965 dl/wk). (d) PASS (MIT). (e) PASS.

### OG validator CLIs
- `npm search "open graph validator"` and `"og image check cli"` returned none: only JSON-schema validators and OG image generators (`@vercel/og`, `satori`, `nuxt-og-image`). The platforms' own inspectors (Facebook Sharing Debugger, LinkedIn Post Inspector) are web tools that need a public URL and a login; they are not packages.

### Family verdict: build
The checks are simple: read the image's real pixel size (Pillow), ratio within the platform's tolerance, file size, type, and for Stories and Reels the 14/35/6% safe zone (the baked-text detector from §2 can test that no text sits inside the margin). For a page, Playwright already reads `og:image` and `twitter:image` and can fetch the image. First, a house decision: which surfaces a project posts to.

## Summary: one row per family (#250 table form)

| Family | Ruling | Deciding criterion |
|---|---|---|
| 1. SVG vector art (true curves, tangents, morph structure) | build: keep `check-curves.js` + `check-flow.py` | (a): no tool has the rule. svgo's default `convertPathData`/`mergePaths` break the morph rule. |
| 2. Raster brand art: size, palette ΔE00, plain headline region, checkerboard, mobile crop | build on Pillow + numpy + `colour_space.py` | (a): no tool has the rule; smartcrop also fails (c) |
| 2. Raster brand art: baked text | adopt onnxruntime-web + vendored PP-OCRv4 det model as the detector, inside a vault script | (a) 4/4 fixtures; tesseract.js fails (a): it missed the 90 px headline and read junk on clean art |
| 3. Logo placement (exact pixels, 3:1, clear space) | build on Pillow + `de2000()`; 3:1 is already `palette.py` | (a)/(b): pixelmatch and looks-same at defaults pass a ΔE00 1-1.4 recolour; they add nothing over Pillow once the threshold is the house's |
| 4. Video: clip length | build (Python `mvhd` reader) or adopt mp4box.js | all five pass for mp4box.js as a parser; the range is house code either way |
| 4. Video: start frame = end frame | no tool fits; critic, or PyAV wheel as a weaker route | (e): every H.264 decoder is native or GPL/LGPL; Playwright's Chromium cannot decode H.264 (measured) |
| 5. Print P1-P5 (PDF/X keys, output intent, boxes, fonts, ppi, colour space) | build on pypdf (installed) | (a): no validator passes; veraPDF has no PDF/X; the two OSI PDF/X validators fail (c) |
| 5. Print P6-P7 (TAC, line weight) | critic now; TAC buildable with Pillow ImageCms + the printer's ICC profile | (e): Ghostscript is native and AGPL |
| 6. Social (size, ratio, file size, Stories/Reels safe zone) | build (Pillow + Playwright) | (a): open-graph-scraper and metascraper extract tags, check nothing |

House decisions this research cannot make (named, not asked): the print spec (PDF/X level, output profile, ppi floor, TAC); which social surfaces a project posts to; the ΔE00 (or strict) tolerance for "never recolour" a logo.

## Bound

- **Read in full**: `check-curves.js` header and constants; svgo 4.1.0 `convertPathData.js` option block and `makeArcs` branch, `preset-default.js` plugin list, CLI `--help`; tesseract.js 7.0.0 `src/worker-script/index.js` lang-loading block; looks-same `index.js` comparator and `constants.js`; pixelmatch README options; mp4box 2.4.1 README info section and LICENSE head; FontBakery `outline_settings.py`; ffmpeg.wasm `const.js`; the `preflight` gem's rule file list and `pdfx1a.rb`; every platform spec page cited in §6 (as returned by the fetch).
- **Sampled**: GWG 2026 PDF/X user guide (keyword search of 36 pages); svglint, picosvg, smartcrop, veraPDF and pdfcpu READMEs (through a summariser or grep); qpdf CLI manual (`--check` entry and PDF/A mentions); Ghostscript Devices page (inkcov, ink_cov, tiffsep).
- **Runs made** (in a throwaway directory; the scripts were not kept): svgo on a morph pair and a polyline; svg-path-commander predicates; tesseract.js offline OCR on 4 fixtures; PP-OCRv4 det on onnxruntime-web on 4 fixtures; pixelmatch, looks-same and Pillow ImageChops on 2 logo placements; Playwright Chromium codec probe; mp4box on one H.264 MP4; Playwright's bundled ffmpeg `-version/-decoders`; pypdf preflight prototype on a Chromium PDF; open-graph-scraper on 2 HTML strings.
- **Fixtures are synthetic.** The text detector and the diff tools were not run on real AI renders or real browser-placed logos.
- **Not reached**: ISO 15930 text (paywalled); GWG2015 numeric limits (spec PDF link returned HTML); Scribus Preflight Verifier (bot-blocked); Meta's safe-zone help article body (returned title only); the lintPDF repository (404); X's current Cards docs (only a Feb 2026 Wayback copy).
- **Not run**: PyAV, imageio-ffmpeg, pikepdf, pdfjs-dist, pdfcpu (native or wasm build), veraPDF (no Java), Ghostscript (absent), smartcrop, metascraper, svglint, FontBakery, picosvg, svgcheck, svgpathtools, pdf-compliance, the `preflight` gem (no Ruby run).
- **Not checked**: the codec Kling and Wan actually return, and whether either can return VP9/WebM or AV1.
