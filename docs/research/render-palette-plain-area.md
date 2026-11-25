# Research #338: how far a painterly render may stray off its palette, and how plain a headline area must be

⚠ **Bound 16 Oct 2026 (#338, review of the landing commit): r1 holds 12 renders, not 13. The 3:1 figures 2.2 and 13.3 are the busy render's upper-third box; in the centre box it reads 3.4 and passes 3:1, so the sourced contrast line does not separate busy art either. The masking index is the sourced measure but does not fit painted art; the measures that separate here (local L\* spread, edge density) are unsourced. r2/v7-soul2, labelled textured, also sits inside the plain range on every local measure. `vault.text-over-image` does not exist on main: text over an image is held by `plugin/skills/design-critique/references/surface-styling.md` (Clash, item 12) and measured by `check-access.py`. Rerun with k_L = 2 (`docs/data/render-palette-kl2-2026-10-16.csv`): palette-52's share beyond ΔE00 10 falls from 0.40 to 0.21 against the not-given group's best of 0.50, and its 95th percentile is 16.2, still failing ISO's 5; the verdict stands.**

⚠ **Bound 16 Oct 2026 (#350): §4's look test was put to the founder on #350, not #338, and he ruled none: it is revisited only if off-palette or busy art reaches him past the critics in a real round.**

Date: 16 Oct 2026. Question: design-vault#338, for the build ticket #339 under spec #324. Labels: **opened** (full text or the cited section read), **abstract** (abstract or publisher page only), **secondary** (a citation or search summary; not read). Every number is marked **sourced**, **house** or **untraced**.

**Answer.** Neither question has a number research can defend. Each has a sourced measure; neither has a sourced pass line, and on the real renders on this machine neither measure puts its line where an eye does. By #324's rule, #339 closes not planned and both rules stay with the critics (§4).

Data: `docs/data/render-palette-share-2026-10-16.csv` (per-pixel shares and percentiles), `docs/data/render-palette-kmeans-2026-10-16.csv` (k-means cluster areas) and `docs/data/render-plain-area-2026-10-16.csv` (texture and contrast measures over each box). The instrument stayed in scratch (`.claude/tmp/research-render-numbers/measure.py`). It imports `lab()`, `luminance()` and `de2000()` from `colour_space.py`; its numpy CIEDE2000 matched `de2000()` on 1000 random pairs to 2.8e-14.

## Sample

39 renders: `~/higgsfield-calibration-2026-09-30/r1`–`r3` (13, 13 and 12 models), `~/higgsfield-palette-52/r1/v1-gpt-sunburst-palette.png`, and MMM Infra's `rounds/aqueduct-storyboard:r2/v1-into-the-valley-still.png` (a generated photograph, not painterly). Manta has no round branch with art; MMM Infra's other round files are storyboards of SVG frames, page screenshots, real photographs or logos, and were skipped.

Labels come from the calibration run's `report.md` where it gives one, else from an agent's look at a downscaled copy (r2 v1, v7, v9, v10, v12, palette-52, the MMM still, four r3 mascots). All values are at 1440 px wide, a desktop hero, assumed seen at 60 cm on a 96 ppi screen (about 40 px per degree; assumed, not measured).

## 1. Palette share

### What the sources give

- **The measure is sourced.** Lin & Hanrahan 2013 (CHI, opened) score an image against a colour theme by "hard recoloring error": each pixel's distance to its nearest theme colour, summed over the area. A share of area beyond a ΔE00 is that same map read as a tail share. They set no threshold, and they found people pick theme colours from salient regions, which an area share ignores.
- **The closest standard covers flat patches.** ISO 12647-7:2016 Table 2 (opened, ISO's preview): over all 1617 chart patches, average ΔE00 ≤ 2.5 and 95th percentile ≤ 5.0; spot solids max ≤ 2.5. G7 and Idealliance use the 95th percentile as go/no-go (BabelColor, vendor doc, opened). Each patch is a flat colour against its own aim, not a pixel of a picture against the nearest of several colours: the form carries over, the values do not.
- **Test both directions.** Aharoni et al. 2025 (arXiv 2509.02000, opened) rated palette match as "all palette colors were present in the image and all image colors were close to a palette color". Designers' own images scored 3.9 of 5 against their own palettes, and an image wholly inside its palette (EMD 0) is "severely color-collapsed and heavily posterized".
- **Pre-filtering gains nothing.** S-CIELAB scored PLCC 0.822 against 0.825 for the plain mean of per-pixel CIEDE2000 on 30,000 image pairs (Wang et al. 2023, TPAMI, opened); the authors call simple spatial filtering "far from sufficient". CIE 199:2011 recommends lightness weight k_L = 2 for image differences (secondary, as cited by Liu et al. 2013, abstract); that is for image against image, untested for image against palette.
- **Quantising first** is the published fast route: weighted k-means on a 16³ histogram in Lab (Chang et al. 2015, SIGGRAPH, opened), which warns that dark pixels pull a centre toward black.
- **No study, standard or brand tool gives the share.** Adobe GenStudio's brand check publishes no colour metric (Experience League, opened); none was found for Canva, Frontify or Bynder. Palette-conditioned generation papers rank models by EMD or histogram distances against baselines and set no pass line (Aharoni et al. 2025; Qiu et al. 2025, arXiv 2508.08754, opened).

### What the renders show

Two renders were given the four-hex palette in their prompt (palette-52, and r2/v13-ideogram-json, which carries the same palette); twelve r2 courtyard renders of the same subject were given none.

| Measure (nearest ΔE00 to the palette) | palette given (worst of 2) | not given (best of 12) |
|---|---|---|
| Share of area > 5 | 0.53 | 0.98 |
| Share of area > 10 | 0.40 | 0.54 |
| Share of area > 20 | 0.07 | 0.10 |
| Median | 6.7 | 11.2 |
| 95th percentile | 21.4 | 21.9 |
| Same, blurred σ 16 px: share > 10 | 0.57 | 0.60 |
| k = 16 cluster area > 10 | 0.40 | 0.63 |

- **A render that followed its palette fails any strict line.** palette-52 has 53% of its area more than ΔE00 5 from every palette colour, from soft shading between palette colours, a grey stone floor and lit windows. The print form (95th percentile ≤ 5) fails it at 21.4.
- **Only the middle of the distribution separates**, and on n = 2: share > 5, the median, and k-means area. The tail (95th percentile, share > 20) overlaps, as both groups carry deep shadow and glow.
- **Blurring makes it worse.** A Gaussian in CIELAB, standing in for S-CIELAB, mixes two palette colours at their border into a colour far from both: palette-52's share > 10 rises from 0.40 to 0.57.
- **The answer turns on the palette, not the render.** Against Manta's 20 tokens, palette-52 scores 0.41 beyond 10, as against its own palette (0.40): every one of its colours has a Manta neighbour (its cream is ΔE00 3.3 from sand-border), and the cream sky is 40% of the area. A muted r1 hero that followed no palette passes against Manta at 0.10.
- **A colour count works partly.** On the r3 mascots ("three colours, plain cream"), the share beyond ΔE00 5 from each render's own four-colour fit separates the four that kept the rule (≤ 0.015) from three of the four that broke it (≥ 0.080). It misses the fourth (gpt-flare, 0.007), and the fit spends two centres on the cream ground.

### Verdict

Measure: **sourced** (nearest-palette-colour ΔE00 per pixel, Lin & Hanrahan; read both directions, Aharoni et al.). Pass line: **untraced**: no source sets one, and the sample cannot (two positives, no clean off-palette control).

## 2. Plain headline area

### What the sources give

- **The measure is sourced: the global masking index** (Scharff, Hill & Ahumada 2000, Optics Express 6(4), opened via a Wayback copy):
  `C_M = C_T / sqrt(1 + (C_RMS / 0.05)²)`, where C_RMS = std(Y) / mean(Y) over the box (luminance, not L\*) and C_T is the text's contrast against the box mean. It correlated −0.84 with reading-search time, against −0.64 for text contrast alone; r = 0.89 on transparent text (Scharff & Ahumada 2002, J. Vision, abstract). C₂ = 0.05 is from Scharff, Ahumada & Hill 1999 and Scharff & Ahumada 2003 (SPIE, opened).
- **Its anchors are body text.** Black text (C_T 0.95) on C_RMS 0.15 was not slowed; text at C_T 0.15 on the same texture could not be read (Scharff et al. 2000; letters 0.25°, one tiled texture). By the formula those are C_M ≈ 0.30 and ≈ 0.047 (our arithmetic). No source sets a pass line on C_M or C_RMS.
- **One global number misranks textures.** Neither index ranked Scharff & Ahumada's two web textures right: an even fine texture (C_RMS 0.15) hurt more than a stronger one with plain gaps (0.27) (2003, opened).
- **Which texture masks depends on size.** Letter identification is masked by one band 1.6 ± 0.7 octaves wide, its centre scaling with stroke frequency to the power 2/3 (Majaj et al. 2002, abstract; equation as applied in PMC4179702, opened). For a 48 px cap height that is texture of about 9–27 px period (our conversion, Courier strokes). No study measured headline reading over texture; letters above 1.9° are untested.
- **Light text** acts as if it had about half its contrast (gain asymmetry A = 0.49, Scharff & Ahumada 2003).
- **WCAG F83** (opened) is the published test for text over an image: the darkest pixel (dark text) or lightest (light text) of the area against the text, else the background behind each letter. It is about contrast, not texture.
- **Clutter measures** (Rosenholtz et al. 2007, abstract) were validated for visual search, not reading, and have no absolute line. Material Design 2018 (opened) gives scrim opacities (dark 20–40%, light 40–60%) with no stated basis.

### What the renders show

Boxes: the brief's own (the upper half for r2 and palette-52, the upper third for the MMM still), the upper third the eye judged, and a centre box (x 20–80%, y 0–25%) clear of edge objects.

| Measure, centre box | plain max (10 renders) | scrim: grok | textured: flux-max | busy: recraft |
|---|---|---|---|---|
| Local SD of L\*, 16 px window, 95th percentile | 1.29 | 1.04 | 2.15 | 17.7 |
| Share of pixels with L\* gradient > 2 per px | 0.0011 | 0.00006 | 0.067 | 0.13 |
| Band energy for a 48 px cap height (L\*) | 0.47 | 0.33 | 0.82 | 4.91 |
| C_M for #111 text (min over plain) | 0.26 | 0.26 | 0.51 | 0.14 |

C_M from the data file's `rmsY_box` and `meanL` (Y from L\*, C₂ 0.05, C_T = (Y_box − Y_#111) / Y_box).

- **Busy content separates by 10× on every local measure** (a building in the box: 17.7 against at most 1.29), and a crumpled-paper sky separates on edge density (20× or more) but not on the letter band, being finer than a letter. Each is one render.
- **The one render the eye said needs a scrim (r2 grok, soft cloud strokes) sits inside the plain range on every measure.** Its strokes are hue changes of about 1–1.5 L\*.
- **The sourced index misreads a sky gradient as texture.** Global C_RMS counts a smooth peach-to-blue gradient as masking: at the anchor 0.30, C_M fails qwen (0.29), flux-pro (0.29) and flux-flex (0.26), all plain, and passes the crumpled-paper flux-max (0.51). Scharff's textures were tiled with an even mean; a painted sky is not.
- **The box decides more than any line.** On the brief's own upper half every r2 render fails: qwen, which the report calls "exactly the brief", scores 6.1 local SD, palette-52 26.3. No model left the full half plain. palette-52's upper third scores 7.63 from a vine and tree tips at its edges, and 0.27 in the centre box.
- **Plain is not zero.** Flat cream grounds score 0.02–0.31 local SD; smooth painted skies reach 1.4.
- Against the 5%-worst pixel, the better of white and #111 reaches at least 4.1:1 in every plain sky; only the busy box falls under 3:1 (2.2). A ratio against the box mean hides it (13.3).

### Verdict

Measure: **sourced** (the masking index; F83 for contrast). Pass line: **untraced**: no source sets one, the index's own form misreads painted gradients, and the local measures that do separate busy art rest on one busy and one textured render, with the eye's one scrim call inside the plain range.

## 3. Numbers

| Number | Meaning | Status |
|---|---|---|
| Average ΔE00 ≤ 2.5, 95th percentile ≤ 5.0 | ISO 12647-7 proof over chart patches | sourced (flat patches; fails a render that kept its palette) |
| k_L = 2 | CIEDE2000 lightness weight for images | sourced as cited (CIE 199:2011 via Liu et al. 2013) |
| ΔE00 2 / ~10 / ~15 | Same colour / near miss / two meanings | house (`de00-thresholds.md`; flat pairs) |
| Share of a render's area beyond a ΔE00 | The palette check's line | untraced |
| C₂ = 0.05 | Masking-index constant | sourced (Scharff et al. 1999, 2003) |
| C_M ≈ 0.30 / 0.047 | No slowing / unreadable, body text | derived from sourced cells (our arithmetic) |
| 4.5:1 / 3:1 against the worst pixel | F83 for text over an image | sourced (WCAG 2.2) |
| A C_M, C_RMS or local-SD limit for a headline box | The plain-area check's line | untraced |
| 1440 px, 60 cm, 96 ppi, 40 px per degree | Display condition for every measured value | untraced (assumed) |

## 4. What follows

- **#339 closes not planned**, both halves, by #324 §Order and decision points.
- **No critic question carries either rule yet.** Brand art has no look question on keeping to the ruled palette or on a plain headline area: colour.md's palette questions judge the palette, not a render against it, and imagery.md's `vault.text-over-image` covers only text already placed on a web surface. That page-level case is scripted, as `check-access.py` measures each letter's background as F83 asks. So "stays with the critics" needs two look questions written (#344), for which the findings above give the critic what to look at: the bulk of the art against the ruled colours, not its shadows and glints; both directions (every ruled colour present); and plainness at letter scale inside the area the headline will take, not the brief's whole box.
- **A number the founder's eye could set.** Two of the gaps are house values a look test could settle: the share of area beyond ΔE00 10 at which a render reads off its palette, and the local L\* spread at which a sky needs a scrim. Either would need a sample with more renders a palette was given than this one has; whether to run one is put to the founder on #338.

## Bound

**Read exhaustively:** every render in the sample, measured by the instrument; the calibration `report.md`; design-critique's `rules/` files for a palette or plain-area question.
**Opened:** Scharff, Hill & Ahumada 2000; Scharff, Ahumada & Hill 1999; Scharff & Ahumada 2003; Chung, Legge & Tjan 2002; PMC4179702; WCAG 2.2 Understanding 1.4.3, F83 and G18 (fetch summaries); Material Design 2018 imagery and 2019 text legibility (Wayback); Yu, Samaras & Zelinsky 2014 (review section); ISET `isetcam` S-CIELAB code; Wang et al. 2023; ISO 12647-7:2016 preview (clauses 4.2–4.3, Table 2); Yu, Chung & Myers 2015; BabelColor PatchTool; G7 Master Welcome Kit 2020; Lin & Hanrahan 2013; Aharoni et al. 2025; Qiu et al. 2025 (metrics); Anandh & Ahuja 2026 (metrics); Chang et al. 2015 (§3); Adobe GenStudio "Brand validation"; the CIE 199:2011 publication page.
**Abstract only:** Scharff & Ahumada 2002 (ARVO 403); Legge et al. 1985, 1987; Rubin & Legge 1989; Solomon & Pelli 1994; Majaj et al. 2002; Rosenholtz, Li & Nakano 2007; Liu et al. 2013.
**Secondary:** Zhang & Wandell 1996/1997 (paper not opened; code opened); Johnson & Fairchild 2003; Rubner et al. 2000; Yang et al. 2016 (PDF 403); Zuffi et al. 2007; Apple HIG and WWDC25; G7 numeric tolerances; ISO 12647-2:2013 via Yu et al.
**Could not open:** Optica's current page (CAPTCHA); jov.arvojournals.org (403); CIE 199:2011 full text (sold); ISO 12647-2:2013 full text.
**Not found:** a study, standard or tool setting a share of image area beyond a ΔE from a palette; a pass/fail texture limit for text over an image; a study of headline-size reading over texture.
**Sampled, not exhaustive:** the brand-tool search (Adobe opened, Canva, Frontify and Bynder searched only); the labels marked as an agent's own. The S-CIELAB stand-in is one Gaussian per CIELAB channel, not S-CIELAB's opponent filters.
