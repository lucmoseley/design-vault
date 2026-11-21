# Research #327: does the PP-OCRv4 text detector find baked-in text on real renders without false alarms?

⚠ **Bound 16 Oct 2026 (#327, review of the landing commit): "found" means any blob anywhere in a text image, not a blob on its text. On the three text renders found, each blob sits on the lettering (THE YARD, HOSTEL twice; checked on crops); `images/`' 69 were not checked box by box. The FAIL rests on the flags, so it stands. Two sample paths are wrong here and in the CSV: MMM Infra's `valley.jpg` is `rounds/aqueduct-storyboard:r2/v1-into-the-valley/valley.jpg`, and the CSV's palette-52 row lacks `r1/`. `~/higgsfield-cutout-54` holds keyed and rembg cutouts of the calibration renders, not new renders, and was skipped. The sweep grid is this trial's choice (untraced); RapidOCR's text score 0.5 is its shipped default (`rapidocr_onnxruntime/config.yaml`).**

Date: 16 Oct 2026. Question: design-vault#327, the baked-text trial #324 runs before anything in the vault depends on onnxruntime-web. Every number is marked **sourced**, **house** or **untraced**.

**Answer: FAIL.** At #324's settings the detector finds 72 of the 76 images that hold text and passes #262's four fixtures, but it flags 32 of the 64 clean images, 17 of them among the 35 clean renders. No threshold setting that still passes the fixtures brings the flags below 18, and that one misses 41 text images. Its false alarms are larger and more confident than the real text it finds, so no tuning separates them. By #324's rule the plugin's npm dependency and the text check are dropped, #329 and #335 close not planned, and `vault.baked-ui-look` covers baked text (§5).

Data: `docs/data/baked-text-trial-2026-10-16.csv` (each image's label, the detector's result, and the RapidOCR cross-check) and `docs/data/baked-text-sweep-2026-10-16.csv` (misses and flags at every threshold tried). The scripts stayed in scratch (`.claude/tmp/c327-06a5cca9/`).

## Sample

140 images:

- **Renders (40).** `~/higgsfield-calibration-2026-09-30/r1` (12), `r2` (13) and `r3` (12); `~/higgsfield-palette-52/r1/v1-gpt-sunburst-palette.png`; MMM Infra's `rounds/aqueduct-storyboard:r2/v1-into-the-valley-still.png` and `valley.jpg`, the same generated aqueduct picture at two sizes. Manta has no round branch. MMM Infra's other round files are storyboards, screenshots, real photographs or logos, not AI renders, and were skipped.
- **The vault's `images/` (96 stills).** The 10 `.webm` clips were skipped because there was no decoder.
- **#262's four fixtures** (1200×800): clean, headline ("BOOK NOW / Open daily 9-5"), garbled ("BOKKO NWOW") and checker.

## Labels

Each image was labelled text or none by eye on a 1280 px copy, with a note of what was seen, before the detector ran on anything.

- **Renders: 5 text, 35 none.** r2/v2-qwen ("THE YARD", "ROOM 2B"), r2/v11-gpt-flare and r2/v12-gpt-sunburst ("HOSTEL"), and two letter-like marks: r2/v6-soul's crest plaque band (about 50×12 px) and r2/v9-flux-flex's door-number plate (about 12×15 px).
- **`images/`: 69 text, 27 none.** Text includes every site screenshot and five small marks: signatures on algarve, painterly-purple and yosemite, a shirt monogram on behance1, and axis numbers on sails-collage.
- **Borderline (3).** algarve, labelled text, has a faint signature. fujiskyline and normandie, labelled none, have marks not readable as writing. §3 reports results with and without them.

## Method

onnxruntime-web 1.30.0 and `ch_PP-OCRv4_det_infer.onnx` from `@gutenye/ocr-models` 1.4.2 (sha256 `30a86f57…6339cdff`) ran from a throwaway install in the job directory, as #262's did. Nothing was installed in the repo. The settings follow #324:

| Value | Setting | Mark |
|---|---|---|
| Long side | 960 px, rounded to a multiple of 32 | sourced: PaddleOCR `det_limit_side_len` (as #324 cites `tools/infer/utility.py`) |
| Normalisation | ImageNet mean and standard deviation, BGR | sourced: PaddleOCR's det preprocessing (as #324 cites) |
| Pixel threshold | probability > 0.3 | sourced: PaddleOCR `det_db_thresh` (as #324 cites) |
| Smallest blob | 4-connected, ≥ 20 px | untraced: #262's run setting |

One departure from PaddleOCR: #262's preparation scales every image to a 960 px long side, so it upscales a small image where PaddleOCR's `limit_type: max` would only shrink one.

## 1. Result at #324's settings

| Group | Found | Of |
|---|---|---|
| Fixtures | 4 correct | 4 |
| Images with text | 72 | 76 |
| Clean images flagged | 32 | 64 |
| Clean renders flagged | 17 | 35 |

**Missed:** r2/v6-soul (highest probability 0.019), r2/v9-flux-flex (0.0), sails-collage (0.0), and yosemite, whose signature peaks at 0.994 but forms no 20 px blob.

**Flagged renders:** r1 v2, v4, v8, v10, v11, v12; r2 v7; r3 v1, v3, v5–v12. palette-52 and both MMM images are clean. The flagged blobs fall on a mascot's body, a sun and its reflection, and a painted face. Some examples:

| Image | Label | Largest blob | Mean probability |
|---|---|---|---|
| r3/v6-soul | none | 38,027 px | 0.994 |
| images/painterly-normal | none | 29,105 px | 0.993 |
| r1/v10-flux-max | none | 18,191 px | 0.979 |
| r2/v11-gpt-flare ("HOSTEL") | text | 1,363 px | 0.992 |
| r2/v12-gpt-sunburst ("HOSTEL") | text | 248 px | 0.971 |
| r2/v2-qwen ("THE YARD") | text | 141 px | 0.987 |

## 2. Tuning

The sweep tried pixel thresholds 0.3, 0.5, 0.7, 0.8, 0.9, 0.95 and 0.99 against smallest blobs of 20, 50, 100, 200, 500, 1000, 2000, 5000 and 10,000 px.

- **The pixel threshold barely matters.** The false-alarm blobs sit at 0.97–0.99 mean probability, the same as the text.
- **The blob size trades misses for flags.** At 20 px: 4 missed, 32 flagged. At 2000 px: 14 missed, 22 flagged. At 5000 px: 41 missed, 18 flagged. At 10,000 px the headline fixture fails.
- **Best setting that passes the fixtures:** 4 missed and 30 flagged, for example 0.99 with 50 px. The rule asks for 0 and 0.

## 3. Borderline labels

Without the three borderline images the best setting is 4 missed, 28 flagged. The fail does not depend on them.

## 4. Cross-check: RapidOCR

To rule out the preparation as the cause, RapidOCR 1.4.4 (onnxruntime 1.30.0, its own PP-OCRv4 det export, mean and standard deviation 0.5, defaults: long side ≥ 736, threshold 0.3, box threshold 0.5) ran in a throwaway venv on all 140 images.

- **Its detector alone** found all 76 images with text and flagged 54 of 64 clean at its defaults. At 960 px with `limit_type: max` it found 74 and flagged 48. The false alarms come from the model, not from #262's preparation.
- **With its recogniser** (text score ≥ 0.5) most flagged renders come back empty or as single junk characters ("三", "C", "仓"), while the fixtures read "BOOK NOW", "Open daily 9-5" and "BOKKO NWOW" and the renders read "HOSTEL" and "YARD", "ROOM". It still flags 8 clean images (six renders) and misses 5 text images. Recognition is a second model and a second dependency, which #324 does not adopt, and it does not reach 0 and 0 either.

## 5. What follows

By #324 §Baked-text trial, on a fail:

- No `plugin/package.json` and no vendored model: the plugin keeps no npm dependency. `vault.baked-text-script` is not added.
- #329 (ship onnxruntime-web) and #335 (the baked-text check in `check-render.py`) close not planned. `check-render.py` keeps its size and checkerboard checks.
- `vault.baked-ui-look` goes into the rule store as a look question, asking whether the art is free of words, letter-like marks, logos, buttons, controls and invented data painted into it. The critics' eye is what catches r2/v6-soul's plaque and r2/v9-flux-flex's door plate, which #324's pipeline found at no setting.

## Bound

Labels are one agent's eye. PaddleOCR's own Python pipeline was not run. RapidOCR, which wraps the same model family, stood in for it. The 20 px blob minimum stays untraced; the verdict does not depend on it, since no blob size in the sweep reaches 0 and 0.
