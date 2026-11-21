# Research: sources for the near-miss line (ΔE00 ~10) and the two-meanings line (ΔE00 ~15) — #178

Question from the founder: "Are you sure this research does not exist out there, and we have not looked deep enough?"
Earlier pass: `docs/research/brand-palette.md` Part 2 and Gaps item 1. It said that no source gives these two numbers.

Labels for how I reached each source:
- **opened**: I read the full text (or the cited section of the full text).
- **abstract**: I read the abstract or a publisher page only.
- **secondary**: through a search summary or another author's citation. Do not treat as read.

## Findings log

### F1. Szafir 2018, "Modeling Color Difference for Visualization Design" — opened (full text)

- Source: D. A. Szafir, IEEE TVCG 24(1):392-401, 2018, doi 10.1109/TVCG.2017.2744359. Full text from https://par.nsf.gov/servlets/purl/10074616 (10 pages, text extracted).
- Task: **discrimination only.** Two marks, 5° apart, among mid-grey distractors. Each participant says "same" or "different" colour (binary forced choice). Mechanical Turk, uncalibrated displays, 30 in viewing distance assumed, 96 dpi, white ground.
- Metric: **CIELAB ΔE (ΔE76), one axis at a time** (ΔL\*, Δa\*, Δb\*). Not ΔE00.
- Model: detection rate p rises linearly with ΔE (fit through zero, below the "knee" where a difference is "immediately perceptible"). So ND(p) = p / (c + k/s). ND(50%) is the difference that 50% of viewers detect.
- Table 1, points (scatterplot dots), ND(50%) in ΔE76:

| Diameter | L\* | a\* | b\* |
|---|---|---|---|
| 0.25° (6 px) | 8.37 | 16.11 | 19.46 |
| 0.5° (12 px) | 6.74 | 9.98 | 13.34 |
| 1° (25 px) | 5.75 | 7.81 | 10.03 |
| 2° (50 px) | 5.47 | 6.84 | 7.99 |

- Lines (Fig. 5): ND(50%) = 5.73 + 0.50/s (L\*), 7.53 + 0.34/s (a\*), 11.29 + 0.43/s (b\*), s = line thickness in degrees. Bars: elongation lowers the threshold by 5-10 ΔE, up to about a 2:1 aspect ratio.
- "a 2° JND for a scatterplot point was roughly 3 times larger than that predicted in controlled environments".
- The engagement check used "nameably different colors greater than 20∆E at middle sizes". This is the author's design choice for an easy trial. It is **not** a measured line, but it is a published, practical use of "> 20 ΔE76 = nameably different".
- What it gives the two lines: nothing direct. It is a **detection** curve, not an "error vs. on purpose" judgement, and not a "two meanings" judgement. Because the fit is linear through zero, the model puts 100% detection at about 2 × ND(50%) (for example 0.5° dots on b\*: about 27 ΔE76). The paper does not claim the line holds above the knee, so this 2× extension is my reading, not the paper's claim.
- Strength: **P** (peer-reviewed, measured, n = 72 for points).

### F2. Heer & Stone 2012, "Color Naming Models for Color Selection, Image Editing and Palette Design" — opened (full text)

- Source: J. Heer, M. Stone, ACM CHI 2012, doi 10.1145/2207676.2208547. PDF: https://idl.cs.washington.edu/files/2012-ColorNameModels-CHI.pdf. Code and model: https://github.com/StanfordHCI/c3.
- Data: XKCD colour survey, over 3 million free-text names, online, uncalibrated screens. CIELAB bins of 5 × 5 × 5 ("each bin has a radius of ∼1 JND").
- Measures: **saliency** (how reliably one colour gets one name; negative entropy of p(name | colour)) and **name distance** (cosine distance between the name distributions of two colours, 0 = named the same, 1 = no shared name).
- Palette use: "To optimize the presentation of categorical data, we might seek to minimize name overlap (to avoid ambiguity) and maximize salience". Tableau 10 has a mean name distance of 0.96 between its colours; the Excel and Economist palettes "exhibit high naming overlap".
- What it gives the two lines: a **proxy**, not a ΔE number. "Name overlap" is a published, measured test for "people would call these the same colour". The paper sets **no threshold** on name distance and does **not** map it to ΔE. It does not test "error vs. on purpose".
- Strength: **P** for the method; no number for either line.

### F3. Moon & Spencer 1944, "Geometric Formulation of Classical Color Harmony" — tables opened (OSA page), body text secondary

- Source: P. Moon, D. E. Spencer, JOSA 34(1):46-59, 1944, doi 10.1364/JOSA.34.000046. Tables I and II read on https://opg.optica.org/josa/abstract.cfm?uri=josa-34-1-46 (OCR of the tables; the body is behind a paywall). The meaning of "ambiguity" is through a secondary source (arXiv 1709.02252, which quotes the postulate): two harmonic colours must "not be so close together that there is doubt as to whether they were intended to be identical or only similar".
- **This is the near-miss concept, stated in 1944, with numbers.** The "first ambiguity" zone is the band between "identical" and "similar", where the viewer cannot tell if the two colours were meant to be the same.
- Table II, Munsell steps (one hue step = 1/100 of the hue circle):

| Zone | Value only | Chroma only | Hue only |
|---|---|---|---|
| Identity | 0 to 1 jnd | 0 to 1 jnd | 0 to 1 jnd |
| 1st ambiguity | 1 jnd to ½ | 1 jnd to 3 | 1 jnd to 7 |
| Similarity | ½ to 1½ | 3 to 5 | 7 to 12 |
| 2nd ambiguity | 1½ to 2½ | 5 to 7 | 12 to 28 |
| Contrast | 2½ to 10 | 7 and more | 28 to 50 |

- **My conversion to ΔE00** (script `.claude/tmp/de00-tools/munsell-zones.py`; Munsell renotation data `real.dat` from rit-mcsl.org; xyY under Illuminant C to CIELAB with the C white, no chromatic adaptation; half steps by linear interpolation in xyY; values = median over the 40 renotation hues; value zones on greys through the ASTM D1535 value function). **Approximate.** The CIEDE2000 code is `scripts/de00-look-test.py`, imported, and its self-test passed.

| Upper bound of zone, ΔE00 | Value (greys, V3-V7) | Chroma (base C2 / C4, V4-V7) | Hue (V4-V7, C4 / C6 / C8 / C10) |
|---|---|---|---|
| 1st ambiguity ends | 3.6-4.9 | 9.3-9.7 / 6.7-7.1 | 7.0-7.6 / 9.0-9.3 / 10.7-11.1 / 12.2-12.5 |
| Similarity ends | 10.2-15.0 | 13.1-13.7 / 9.9-10.5 | 12.0-12.7 / 15.2-15.8 / 18.0-18.7 / 20.6-20.9 |
| 2nd ambiguity ends (contrast starts) | 16.2-24.5 | 15.7-16.6 / 12.2-13.3 | 25.5-26.8 / 32.2-33.5 / 38.5-40.3 / 43.8-45.0 |

- Check of the conversion: 1 Munsell value step = ΔL\* ≈ 10, and 1 hue step at chroma 4 = ΔE00 1.0. Both are as expected.
- Read: for a **hue or chroma** shift, the "doubt whether meant identical" band ends at about **ΔE00 7-12**. That brackets the house near-miss line of ~10. For a **lightness-only** shift it ends much earlier, at about ΔE00 4-5. Moon & Spencer then put a **second** ambiguity band (between "similar" and "contrast") that ends at about ΔE00 13-17 for chroma, 16-24 for lightness and 25-45 for hue.
- Strength: **P, but a theory.** Moon & Spencer took the zones from classical harmony writing, not from an experiment with observers (secondary: Ou & Luo 2006 call the model of "weak theoretical basis and poor predictive value"). The zones are about **harmony** (pleasing or not), not about meaning.

### F4. Chuang & Ou 2001, "Influence of a holistic color interval on color harmony" — opened (full text)

- Source: M.-C. Chuang, L.-C. Ou, Color Res. Appl. 26(1):29-39, 2001. Full text from the NYCU repository (API text bitstream, https://ir.lib.nycu.edu.tw/handle/11536/29880).
- Stimulus and task: 1035 two-colour pairs on a CRT, test pattern radius 6 cm, viewing distance 30-40 cm (a large field, roughly 17-22° across). 15 reliable observers rate **harmony** (pleasing or not). Metric: **ΔE\*ab (ΔE76)**, data grouped into 10-unit bins.
- Result: harmony is a cubic function of ΔE\*ab (R² = 0.92). A horizontal line through the inflection point cuts the curve at **ΔE\*ab 30.2, 75.3 and 120.4**. Below 30.2 is a "disharmony" region, 30.2-75.3 "harmony", 75.3-120.4 "disharmony", beyond 120.4 "harmony". The authors say this "roughly corresponds" to Moon & Spencer's first ambiguity, similarity, second ambiguity and contrast. Lightness difference drives the pattern; chroma and hue differences alone show none.
- What it gives the two lines: a **weak proxy**. The cut at 30.2 is the point where the curve crosses its own inflection level, not a judgement of "error" or "meaning". The 10-unit bins are too coarse to place a line near ΔE00 10. The authors also reject Moon & Spencer's per-attribute zones ("may be inappropriate in predicting perceived color harmony").
- Conversion: not done. ΔE\*ab 30 between arbitrary pairs maps to a wide ΔE00 range (roughly 15-30, depending on chroma), so a single figure would mislead.
- Strength: **P** (measured), but on harmony, not on the near-miss question.

### F5. Brychtová & Çöltekin 2016, "The effect of spatial distance on the discriminability of colors in maps" — opened (full text)

- Source: A. Brychtová, A. Çöltekin, Cartography and Geographic Information Science 44(3), online 2016, doi 10.1080/15230406.2016.1140074. Author PDF: http://coltekin.net/arzu/publications/brychtova_coltekin-2016.pdf.
- **It is the one source found that states a ΔE00 number as a minimum for categorical colours in a display.**
- Metric: **ΔE00** (CIEDE2000, Sharma 2005), controlled at 0, 2, 4, 6, 8, 10.
- Stimulus: choropleth maps. Map areas 30-45 px (online, about 50 cm viewing) and 60-90 px (lab, 70 cm, 23 in IPS monitor, ICC profile). Two marked areas at three gaps: adjacent (< 1.5°), medium (2.5-3.5°), far (6-13°). Qualitative scheme = six hues at about constant lightness (yellow, orange, red, violet, blue, green). Sequential = six greens that differ in L\* only.
- Task: **discrimination** ("decide if their color is the same"), and for sequential only, rank three areas by lightness. Not naming, not meaning. Observers: 211 online, 32 in the lab.
- Result, verbatim: "for qualitative colors, the largest tested color distance ΔE00 = 10 yields considerably higher levels of accuracy in color discrimination (even when the spatial gap between the two colors is large), thus we recommend ΔE00 = 10 to practicing cartographers and other information visualization designers." And: "perceptual difference between shades of qualitative schemes should be at least ΔE00 = 10, because this level of color distance allows to correctly distinguish map symbols even if they are far apart." Sequential: "Accuracy at ΔE00 = 10 is particularly high (more than 90%) at all spatial distances." Lightness-only (sequential) pairs need more distance than hue pairs at the same ΔE00.
- Limits: **10 was the largest ΔE00 tested**, so "at least 10" is the top of the tested range, not a measured knee. The task is "same or different", so the number is a **discrimination floor for categories**, measured with real map layouts and gaps. It does not test "reads as an error" or "reads as two meanings".
- Use for the house lines:
  - Two-meanings line: **sourced floor ≥ ΔE00 10** for colours that must be told apart as categories on a display, small areas (30-90 px), up to 13° apart. The house's 15 is above this floor; the paper gives no evidence for or against 15.
  - Near-miss line: indirect. Below ΔE00 10, a measurable share of viewers fail to tell two map colours apart when they are not adjacent; so a pair below 10 can be seen as "the same" by some viewers and "different" by others. That is the condition for a near-miss.
- Strength: **P** (peer-reviewed, measured, ΔE00 native, no conversion needed).

### F6. Datawrapper's colour-blind check: a shipped ΔE00 threshold of 9.2 — opened (source code)

- Source: `services/app/src/lib/components/editor/ColorblindCheck.svelte`, datawrapper/datawrapper at commit 58de8fd (17 Sep 2023), lines 190-224, read through the GitHub API. It uses chroma-js ^2.4.2, whose `deltaE` is CIEDE2000 (chroma.js v2.4.0 `src/utils/delta-e.js`: "Delta E (CIE 2000)", read). Author of the method: Gregor Aisch (blog https://www.vis4.net/blog/1802-datawrapper-color-blind-check/, opened: no metric or number given there; it promises a later technical post, which I did not find).
- The rule in the code: `smallestPercievableDistance = 9.2` and `ratioThres = 5`. For each pair of chart colours: if ΔE00 (normal vision) < 9.2, the pair is **skipped** (treated as not meant to be told apart). Otherwise the pair fails if, under simulated colour-blindness, ΔE00 drops below 9.2 **and** shrinks by more than 5×. The chart fails if 3% or more of pairs fail.
- So Datawrapper treats **ΔE00 ≈ 9.2 as the smallest difference at which two chart colours count as distinguishable categories**. The code does not say where 9.2 comes from. The code averages ΔE in both directions, which is needed only for an asymmetric formula (CMC l:c); that hints the number may date from an older chroma.js `deltaE`. I could not confirm this. Treat the metric of the original calibration as unknown.
- Re-use: the R package Ra11y (nicucalcea/Ra11y, `R/test_colourblind.R`) copies 9.2 and 5 and cites the Datawrapper line.
- What it gives: a **practice number** for line 2's floor (distinct categories in a chart), close to Brychtová & Çöltekin's ΔE00 10. Not measured; origin unstated.
- Strength: **Pr** (widely used production tool; first-party code; no stated basis).

### F7. Lu et al. 2021, Palettailor — opened (arXiv full text)

- Source: K. Lu, M. Feng, X. Chen, M. Sedlmair, O. Deussen, D. Lischinski, Z. Cheng, Y. Wang, "Palettailor: Discriminable Colorization for Categorical Data", IEEE TVCG 27(2), 2021 (VIS 2020). arXiv 2009.02969.
- Verbatim: "we employ a hard constraint into our optimization: each two colors should have a minimal CIEDE2000 distance of 10, so that each pair of colors can be distinguished even for large spatial distances." And: "a noticeable difference threshold τ, which is suggested to be 10, cf. [5]", where [5] = Brychtová & Çöltekin 2016 (F5).
- What it gives: a peer-reviewed categorical-palette generator that **adopts ΔE00 ≥ 10 as a hard floor** between category colours. It is not an independent measurement; it inherits F5's number.
- Strength: **P** (adoption of F5 in a TVCG method).

### F8. Tseng, Wang, Quadri & Szafir 2024, "Revisiting Categorical Color Perception in Scatterplots" — opened (arXiv full text)

- Source: EuroVis 2024 short paper, arXiv 2404.03787.
- Verbatim (§2.2): "As the difference between colors increases, perceptual distance metrics become less useful. However, measures such as color name difference [HS12] provide a metric for color uniqueness or relatedness for larger color differences [GLS16]."
- What it gives: no number. It supports the **naming proxy** (F2) as the field's current tool for large differences, and it states that ΔE metrics weaken at the scale of the house lines.
- Strength: **P** (statement of the field's view, by the author of F1).

### F1a. Szafir 2018 ND(50%) converted to ΔE00 — my calculation

- Script: `.claude/tmp/de00-tools/axis-steps.py`. It moves each base colour of a grid (Szafir's range: L\* 30-65, a\* -36..48, b\* -48..48, step 5/12/12, grey left out, sRGB gamut only) by the one-axis step, both ways, and takes ΔE00 (CIEDE2000 from `scripts/de00-look-test.py`, self-test passed). **Approximate**: the result depends on the base colour (p10-p90 shown).

| Dot diameter | ΔL\* step → ΔE00 | Δa\* step → ΔE00 | Δb\* step → ΔE00 |
|---|---|---|---|
| 0.25° (6 px) | 7.4 (6.5-8.4) | 9.5 (5.8-14.7) | 10.4 (8.2-13.5) |
| 0.5° (12 px) | 6.1 (5.3-6.7) | 5.8 (3.7-9.2) | 7.1 (5.6-9.2) |
| 1° (25 px) | 5.2 (4.6-5.7) | 4.6 (2.9-7.2) | 5.4 (4.0-6.9) |
| 2° (50 px) | 5.0 (4.3-5.4) | 4.0 (2.5-6.3) | 4.2 (3.2-5.5) |

- Read: on a web screen, the difference that **half** of viewers notice is about **ΔE00 4-5 for 50 px patches** and about **ΔE00 7-10 for 6 px dots**. With the paper's linear model, nearly all viewers notice at about twice these values (ΔE00 ~8-10 large, ~15-20 tiny), but that is an extension past the fitted range.

### F9. Colorgorical (Gramazio, Laidlaw & Schloss 2017) — opened (source code and paper §4)

- Source: github.com/connorgr/colorgorical, `src/model/model.py` and `src/model/util/jnd.py`, read through the GitHub API. Paper: C. C. Gramazio, D. H. Laidlaw, K. B. Schloss, "Colorgorical: Creating discriminable and preferable color palettes for information visualization", IEEE TVCG 23(1), 2017 (VIS 2016).
- Rule in the code: a candidate colour is removed unless it differs from every colour already in the palette by at least **3 × the Stone, Szafir & Setlur 2014 ND(50%)** on at least one CIELAB axis, at a default mark size of 1/3° (`noticeableDifferenceAngle=1.0/3.0`; `ndL, ndA, ndB = [d*3 for d in jnd.cieLabJND(...)]`). With the 2014 model (ND = 5.079 + 0.751/s, 5.339 + 1.541/s, 5.349 + 2.871/s) this is ΔL\* ≥ 22.0, or Δa\* ≥ 29.9, or Δb\* ≥ 41.9.
- My conversion (same script and grid as F1a): ΔL\* 22.0 → ΔE00 19.6 (16.8-21.9); Δa\* 29.9 → 18.0 (11.6-29.2); Δb\* 41.9 → 22.5 (18.3-28.4). So Colorgorical's hard floor between categorical colours is roughly **ΔE00 ≥ 18-22** (one-axis case; approximate). Then it scores palettes on CIEDE2000, name difference, name uniqueness and pair preference.
- What it gives: a **design-tool floor for line 2** (two categories in one chart) that is well **above** the house 15.
- Paper, **opened** (PDF in the repo, `src/public/static/pdf/colorgorical.pdf`, §4): "We use a small, conservative visual angle in our calculations (1/3°) and multiply the function's suggested interval by three for extra caution." So the factor 3 is a stated **caution margin**, not a measured line.
- Strength: **P** for the rule as published; the factor 3 is a judgement ("extra caution"), not a measurement.

### F10. Brand-colour tolerance in print: what the trade measures — opened (trade articles); weak

- Paravina et al. 2015 (dentistry, through search summary; **not opened**): 50:50 perceptibility threshold ΔE00 0.8, 50:50 acceptability threshold ΔE00 1.8, for ceramic tooth samples. J Esthet Restor Dent 27(S1), doi 10.1111/jerd.12149. This is the classic PT/AT pair. Both lines are far below the house lines; the field measures **acceptability of a mismatch to a target**, not "reads as on purpose".
- Eddy Hagen, insights4print.ceo (opened, two posts):
  - Survey 2019 (https://www.insights4print.ceo/2019/03/new-survey-the-influence-of-color-deviations-damaged-packages-on-shopping-behavior-and-brand-loyalty/): 108 people, six Coca-Cola reds at ΔE00 0, 2.1, 3.1, 4.3, 8.6, 9.2, on uncontrolled screens. "about 1 out of 4 people would even reject a 2,1 dE00 package"; rejection looks random at low ΔE00 and shows "a clear and gradual increase" at 8.6 and 9.2. Per-value figures are only in charts not given as text.
  - Shelf case 2025 (https://www.insights4print.ceo/2025/01/and-no-one-called-it-a-brands-worst-nightmare-11-de00-between-adjacent-packages/): two versions of one coffee pack side by side on one shelf, blue **11 ΔE00** apart (gold 9 ΔE00). Of more than 1,500 viewers of a neutral post, few commented on colour; one commenter "assumed it was a different coffee because the colour was so different". The maker confirmed a redesign.
- What it gives: **anecdote only**, but in the right direction. At about ΔE00 9-11, side by side, some viewers read two versions of one brand colour as **two different products** (an intentional difference), and others do not see a problem. This is the zone the house calls the near-miss edge.
- Strength: **Pr** (practitioner, convenience samples, uncontrolled). Not a source for a number.

### F11. Is ΔE00 meaningful at 10-20? (large colour differences) — abstracts only

- Luo, Xu, Pointer, Melgosa, Cui, Li, Xiao, Huang 2023, "A comprehensive test of colour-difference formulae and uniform colour spaces using available visual datasets", Color Res. Appl. 48(3):267-282, doi 10.1002/col.22844. Open access (CC BY-NC-ND), but Wiley returned 403 to every route I tried, so **abstract only** (through the UGR/UJaén record and search summary): 28 data sets in three groups (large differences; small differences, surface; small differences, display), 17 formulae; CAM16-UCS was best in all groups and is recommended.
- Huang et al. 2022, "Optimizing Color-Difference Formulas for 3D-Printed Objects", Sensors 22(22):8869 (abstract page, https://eprints.whiterose.ac.uk/id/eprint/193809/): 440 pairs, from below to above 5 CIELAB units; "the CIEDE2000, CAM02-, and CAM16-based formulas were equivalent"; CIELAB was worse.
- Read: past ΔE00 ≈ 5, ΔE00 is still about as good as the newer spaces at **ranking** pairs, but every formula has large error on large-difference data (STRESS about 30 or more in the TU Berlin tables found by search; not checked). So ΔE00 10 against 15 is a usable rank. It is not a precise perceptual step, which is what the earlier pass said.
- Strength: **P (abstract)**.

### F12. "Same colour name" as a function of ΔE00 — my calculation from Heer & Stone's c3 model

- Data: c3 model, `data/xkcd/c3_data.json` from https://github.com/StanfordHCI/c3 (Heer & Stone 2012, F2): 8,325 CIELAB bins of 5 units, 153 names, counts from the XKCD survey (free naming of single colours on uncalibrated screens).
- Script: `.claude/tmp/de00-tools/c3-names.py`. For every pair of bins (both in sRGB, both named ≥ 100 times: 6,618 bins, about 11 million pairs under ΔE00 40), it buckets by ΔE00 and reports (a) Heer & Stone's cosine name distance, (b) the share of pairs whose most frequent name differs, and (c) the same with names collapsed to their head colour word ("lightblue", "darkblue", "skyblue" → "blue"; 67 groups). The vectorised CIEDE2000 matches `scripts/de00-look-test.py` to 1e-9 on 200 random pairs.

| ΔE00 | Median name distance | Most frequent name differs | Head colour word differs |
|---|---|---|---|
| 0-2 | 0.00 | 6% | 5% |
| 4-6 | 0.04 | 21% | 16% |
| 8-10 | 0.13 | 38% | 30% |
| 10-12 | 0.20 | 45% | 36% |
| 12-14 | 0.29 | 53% | 43% |
| 14-16 | 0.38 | 59% | 49% |
| 16-18 | 0.50 | 65% | 56% |
| 20-22 | 0.69 | 76% | 68% |
| 24-26 | 0.84 | 84% | 78% |
| 28-30 | 0.92 | 90% | 85% |

- With a stricter sample (bins named ≥ 500 times: 956 bins, mostly well-named category centres) every curve moves up by about ΔE00 4: the most frequent name differs for 50% of pairs at ΔE00 16-18, and the median name distance reaches 0.5 at about 20-22.
- Read:
  - Below about **ΔE00 6-10**, most pairs carry the **same name** (the most frequent name agrees for 62-80% of pairs; the name distributions nearly coincide). People would call both "the same colour". A visible difference there has no name to explain it. This fits the near-miss idea.
  - At **ΔE00 12-18**, it is about a **coin toss** whether two colours get different names. At about **ΔE00 20-25**, three in four pairs get different names.
- Limits: naming was of **one colour alone**, not of two side by side; side by side, people see smaller differences (F1, F5). Uncalibrated screens. This is an **average over colour space**: inside a large category (greens, blues) the name may hold over ΔE00 30; at a boundary (blue/purple, orange/brown) it may change within ΔE00 5. So a per-pair check (do the two colours share a name?) is better than one ΔE00 number. The thresholds in the table are my analysis of a published model, **not** a figure the paper gives.
- Strength: **derived from P data** (method mine; not peer-reviewed).

### F13. cols4all (Tennekes), palette-analysis tool: ΔE00 bands 10 and 15 for categorical palettes — opened (paper vignette)

- Source: "Analysing and comparing color palettes with cols4all", vignette `01_paper.Rmd` of the R package cols4all 0.11 (M. Tennekes, CRAN), https://cols4all.github.io/cols4all-R/articles/01_paper.html. A paper-style text; I found no journal version.
- Metric: CIEDE2000 (cites Sharma, Wu & Dalal 2005). Its "rule of thumb" (Table 1, **no citation**): 0-1 "Not perceptible at all"; 1-2 "Perceptible through close observation"; 2-5 "Noticeable difference"; 5-10 "Strong color difference"; **10-15 "Substantial color difference"; 15+ "Vastly different colors"**.
- Rule for categorical palettes, on the **smallest pairwise ΔE00 under simulated colour-blindness** (deutan, protan, tritan): < 2 bad; 2-10 in between; **≥ 10 "+" (colour-blind friendly); ≥ 15 "++"**, added "to highlight palettes for which the colors can be distinguished with ease … especially useful for applications in which the colored objects are small, e.g. lines and points."
- What it gives: the **same two numbers as the house (10 and 15)**, used as category-distinctness bands in a published tool. But they are a stated rule of thumb with no source, applied to simulated colour-blind vision, and they are about "can be told apart", not about "error vs. on purpose".
- Strength: **Pr** (tool documentation; numbers unsourced).

### F14. Healey 1996, "Choosing Effective Colours for Data Visualization" — opened (full text, UBC TR-96-10)

- Source: C. G. Healey, IEEE Visualization '96, pp. 263-270. PDF: https://www.cs.ubc.ca/sites/default/files/tr/1996/TR-96-10_0.pdf.
- Task: **pre-attentive search** (is a target colour present among distractors; response time and error). Isoluminant colours on a circle in CIELUV; 38 observers; 8-bit Macintosh display.
- Distances used (ΔE\*uv between neighbouring colours): 3 colours 129.9; 5 colours 88.2; 7 colours 65.1; 9 colours 51.3. Three and five colours searched fast and accurate (about 2.5% error); at seven, some targets failed until colours were moved into the centres of their **named colour regions**; "seven isoluminant colours is the maximum we can display at one time, while still allowing rapid and accurate identification".
- What it gives: a line for **instant, parallel pick-out** of a category, far above both house lines (neighbours about 50-65 ΔE\*uv apart; I did not convert to ΔE00, because the paper gives the colours only as a construction, and an isoluminant hue difference of that size is far past the range where any formula is calibrated). It also shows that equal ΔE does not give equal separation: **colour-name category** matters (same lesson as F2, F12).
- Strength: **P**. Relevant to line 2 only as an upper reference ("pops out at a glance"), not as the floor.

### F15. Li & Nagai 2024, "Increasing magnitude of color differences amplifies category effects" — opened (full text, Europe PMC)

- Source: K. Li, T. Nagai, Scientific Reports 14:13665, 2024, doi 10.1038/s41598-024-64215-0 (PMC11176193).
- Task: discrimination thresholds (staircase) and **supra-threshold difference scaling** (MLDS) at 32 isoluminant hues, u′v′ chromaticity, 20 cd/m². Units are u′v′, not ΔE; no ΔE00 figure.
- Result: no category effect on just-noticeable differences (agrees with Witzel & Gegenfurtner 2013, cited there), but "increased sensitivities at many color category boundaries in suprathreshold color difference perception", and "the influence of color categories on the perception of color differences may become more pronounced as the magnitude of color differences increases."
- What it gives: **mechanism support** for using colour names (F2, F12) at the scale of the house lines: at large differences, whether two colours fall in one named category or two changes how different they look. No number.
- Strength: **P**.

### F16. Hye, McNutt & Isaacs 2026, "Ten Years Later: Replicating Two Color Discrimination Studies" — opened (arXiv full text)

- Source: arXiv 2608.24789 (25 Aug 2026), 5 pages. Replicates Szafir 2018 (F1), N = 144, crowdsourced, CIELAB Euclidean ΔE.
- ND(50%) for scatterplot dots: at 0.25°, L\* 8.46, a\* 13.89, b\* 20.56; at 2.0°, L\* 4.61, a\* 5.62, b\* 8.00. Close to F1's 8.37/16.11/19.46 and 5.47/6.84/7.99. Thresholds "appeared to be more affected by variations in display, adaptive brightness, and viewing settings than by variations in individuals' color practices" (artists and make-up users did no better).
- What it gives: confirms F1 and F1a ten years on. Detection only.
- Strength: **P (preprint)**.

### F17. Mylonas, Griffin & Stockman 2020, "Online versus Offline Colour Naming Experiments" — opened (one-page abstract)

- Source: LIM 2020 abstract, https://nul.repository.guildhe.ac.uk/id/eprint/269/ (PDF opened).
- Stimuli: 600 Munsell-renotation colours, about 2° on neutral grey. Online: 447 observers; lab: 10 observers who named all 600.
- Result: the centres of the 11 basic colour terms agree between online and lab with mean **ΔE00 4.58** (SD 2.83). Between individual lab observers, the centres of the same basic term differ by mean **ΔE00 7.91** (SD 3.22).
- What it gives: a **proxy for the size of one named colour as people hold it**. Two people's "red" sit about ΔE00 8 apart. So a difference under about ΔE00 8 lies inside normal disagreement about where one named colour sits; it does not make a new named colour.
- Strength: **P (abstract)**.

### F18. Stone, Szafir & Setlur 2014, "An Engineering Model for Color Difference as a Function of Size" — opened (full text)

- Source: M. Stone, D. A. Szafir, V. Setlur, 22nd IS&T Color and Imaging Conference (CIC 22), 2014. PDF: http://www.danielleszafir.com/2014CIC_48_Stone_v3.pdf.
- Task: same/different for two coloured squares 4° apart, crowdsourced, 11 sizes from 6° to 1/3°. Metric: CIELAB per axis.
- Verbatim: "For practical design under uncontrolled conditions, we find the required difference, or in our notation, ND(50,2), is closer to 6 … For 0.33 degrees, the required difference is closer to 11". For large sizes ND(50) tends to (5.1, 5.3, 5.3) on (L\*, a\*, b\*). This is the model Colorgorical multiplies by 3 (F9).
- What it gives: detection only, as F1. A 50%-detection difference of about 6 ΔE76 at 2° and 11 at 1/3°.
- Strength: **P**.

### F19. ISCC-NBS name blocks: step between neighbouring fine names — my calculation

- Data: Lab values of the 267 ISCC-NBS centroid colours, from the "NBS/ISCC Color System" file (tx4.us, copied in github.com/Aye-saac/aye-saac `data/colour/lab.txt`). The file says that some out-of-gamut centroids were moved to the sRGB edge. **Approximate.**
- Script: `.claude/tmp/de00-tools/iscc-nn.py`. Result: the nearest other centroid is at median **ΔE00 5.4** (p10 3.0, p90 7.7).
- Read: with a **fine** vocabulary of 267 names ("light pink", "moderate pink"), the name changes about every ΔE00 5. With an **everyday** vocabulary (F12, 153 names), the most frequent name changes for half of pairs at about ΔE00 13. So "different name" is a usable test only if the vocabulary is fixed. Everyday names (F12) fit the house question better, because the founder and users do not use the fine names.
- Strength: derived; weak.

## Synthesis

### (a) Numbers that a source gives for one of the two lines

**Line 2 (two meanings in one view):**

| Number | Metric | Size and conditions | Task | Source | Strength |
|---|---|---|---|---|---|
| ≥ 10 | ΔE00 | Map areas 30-90 px, up to 13° apart, web and lab screens | Same/different discrimination of category colours | Brychtová & Çöltekin 2016 (F5) | P; 10 was the largest value tested |
| ≥ 10 | ΔE00 | Scatterplots | Hard floor in a palette generator | Lu et al. 2021, Palettailor (F7), citing F5 | P (adoption) |
| ≥ 9.2 | ΔE00 (chroma.js) | Any chart | Floor for "distinguishable" in a colour-blind check | Datawrapper source code (F6) | Pr; origin not stated |
| ≥ 10 "+", ≥ 15 "++" | ΔE00, under simulated colour-blindness | Charts; ++ "for small objects, lines and points" | Rule-of-thumb bands | cols4all (F13) | Pr; unsourced |
| ≈ 18-22 (my conversion of 3 × ND(50) at 1/3°) | CIELAB one axis → ΔE00 | Small marks | Floor in a palette generator, "for extra caution" | Gramazio et al. 2017, Colorgorical (F9) | P (rule); the margin is a judgement |
| ≈ 50-65 | ΔE\*uv (not converted) | Isoluminant targets | Instant visual search ("pop-out") | Healey 1996 (F14) | P; upper reference only |

**Line 1 (near-miss):**

| Number | Metric | Conditions | Task | Source | Strength |
|---|---|---|---|---|---|
| Ends at ≈ 7-12 (hue, chroma), ≈ 4-5 (lightness only) | Munsell steps → ΔE00 (my conversion) | Theory | "Doubt whether intended identical or only similar" (first ambiguity zone) | Moon & Spencer 1944 (F3) | P, but a theory; never confirmed by experiment; later work rejects the per-attribute zones (F4) |

### (b) Proxies that sources support

1. **Same colour name.** The field's test for "reads as one colour" is name agreement (Heer & Stone 2012, F2; Tseng et al. 2024, F8). My analysis of the c3 model (F12): below about ΔE00 6-10 most pairs share a name; at ΔE00 12-18 it is a coin toss; at ΔE00 20-25 three in four pairs get different names. Category effects grow with the size of a difference (Li & Nagai 2024, F15), so names matter most at the scale of the house lines.
2. **Spread of one named colour between people.** Two observers' centres of the same basic colour term differ by mean ΔE00 7.9 (Mylonas et al. 2020, F17).
3. **Detection share.** On web screens, half of viewers see a difference at about ΔE00 4-5 (50 px) and 7-10 (6 px dots) (Szafir 2018, F1, F1a; Stone et al. 2014, F18; replicated 2026, F16). The linear model puts nearly all viewers at about twice that.
4. **Trade tolerance.** Print and dentistry set acceptability at ΔE00 about 2-4 and 1.8 (F10). That is a "match to target" line, below both house lines. An anecdote: two packs of one coffee 11 ΔE00 apart, side by side, read to one viewer as two different products (F10).

### (c) What no source gives, after this search

- **No study asks viewers if a visible colour difference looks like a mistake or like a choice.** The near-miss line is defined by attribution of intent. Every measured task found is discrimination (same/different), visual search, naming, harmony rating, or acceptability against a target.
- **No study measures how far apart two colours must be to carry two meanings with a redundant label.** The category studies measure discrimination of categories without labels (F5) or search (F14).
- Searches made: colour naming and categorical perception (Heer & Stone, c3, Mylonas, Witzel, Li & Nagai, ISCC-NBS); visualisation palettes (Szafir, Stone et al., Gramazio/Colorgorical, Palettailor, Tseng et al., Healey, Tableau 10, Datawrapper, cols4all, colorblindcheck, Ra11y, Carbon, Cloudscape); cartography (Brychtová & Çöltekin); harmony (Moon & Spencer, Chuang & Ou, Ou & Luo, Szabó et al.); tolerance (Paravina, print, brand-colour surveys); large differences (Luo et al. 2023, Huang et al. 2022); free-text searches for intent and error judgements of colour and of other visual near-misses.

## Verdict per line

### Line 1, near-miss (house ≈ ΔE00 10): sourced proxy, not a sourced number

- Four independent proxies meet at about ΔE00 7-12:
  - Moon & Spencer's first ambiguity zone ends at about ΔE00 7-12 for hue and chroma (theory, F3).
  - Most pairs below about ΔE00 6-10 carry the same everyday colour name (F12).
  - People disagree by about ΔE00 8 on where one named colour sits (F17).
  - At small sizes, half of viewers see only differences above about ΔE00 7-10 (F1a).
- So the earlier pass was **premature in part**: 10 has support from sources, as a convergent proxy. It is still **not a measured "error" line**.
- **Conflict for lightness-only pairs.** Moon & Spencer end the ambiguity at about ΔE00 4-5 for lightness. Brychtová & Çöltekin found that lightness-only pairs need **more** ΔE00 than hue pairs to be told apart. The sources do not settle which way lightness goes. Treat a lightness-only near-miss (two greys) as a case for the look test.
- **Strictness choice for the founder:** which share of viewers may read a pair as "the same colour". For example (F12): "six in ten pairs share their most frequent name" gives about ΔE00 9-10; "eight in ten pairs share it" gives about ΔE00 5; "nine in ten" gives about ΔE00 2-3. The look test already built for #178 (cards at ΔE00 4, 7, 10, 13, 16) is the right instrument for the attribution of intent, which no source measures.

### Line 2, two meanings (house ≈ ΔE00 15): sourced floor at 10; 15 is a margin choice

- **Sourced number:** ΔE00 ≥ 10 is a measured, published floor for colours that must be told apart as categories on a display, up to 13° apart (F5). Palettailor adopts it (F7). Datawrapper ships 9.2 (F6).
- **Tools set higher margins:** cols4all calls ≥ 15 the "ease" band for small marks (unsourced, F13). Colorgorical works out to about ΔE00 18-22 "for extra caution" (F9).
- **Naming proxy:** at ΔE00 15, about half of pairs get different everyday names; at ΔE00 20-22, about two in three to three in four (F12, head word and full name).
- So **15 sits between the measured floor (10) and the cautious tool floors (about 20)**.
- **Size matters:** small marks (6-12 px dots, thin lines, small text) need about twice the difference of 50 px fields to reach the same detection share (F1, F18). F5's areas were 30-90 px.
- **Strictness choice for the founder:**
  - 10: the measured discrimination floor, for meanings that also carry a label or icon.
  - 15: a margin over that floor; half of pairs get different names.
  - 20: two in three to three in four pairs get different names; about Colorgorical's cautious floor; for small marks or no label.

## Bound

**Read in full (opened):** Szafir 2018 (TVCG, 10 pp.); Stone, Szafir & Setlur 2014 (CIC, 6 pp., the method and ND passages); Hye, McNutt & Isaacs 2026 (arXiv, 5 pp.); Heer & Stone 2012 (CHI, the name-distance and palette sections); Brychtová & Çöltekin 2016 (CaGIS, 18 pp. author copy); Chuang & Ou 2001 (Color Res. Appl., repository text); Lu et al. 2021 Palettailor (arXiv, the constraint sections); Tseng et al. 2024 (arXiv, 5 pp.); Gramazio et al. 2017 Colorgorical (PDF in its repo, §4) and its code (`model.py`, `jnd.py`); Healey 1996 (UBC TR, method and results); Li & Nagai 2024 (Sci. Rep., Europe PMC text, abstract, introduction and methods); Datawrapper `ColorblindCheck.svelte` and chroma.js v2.4.0 `delta-e.js`; Ra11y `test_colourblind.R`; colorblindcheck `palette_check.R`; cols4all paper vignette; insights4print posts (2019 survey, 2025 shelf case); vis4.net colour-blind check post; Mylonas et al. 2020 (one-page abstract).

**Opened in part:** Moon & Spencer 1944: Tables I and II only, from the OSA abstract page (body behind a paywall); its definition of ambiguity through arXiv 1709.02252.

**Data used for my own calculations:** Munsell renotation `real.dat` (rit-mcsl.org); c3 model `c3_data.json` (StanfordHCI/c3); ISCC-NBS centroid Lab file (tx4.us copy). Scripts in `.claude/tmp/de00-tools/`: `munsell-zones.py`, `axis-steps.py`, `c3-names.py`, `iscc-nn.py`, `pdf2txt.py`. Each imports CIEDE2000 from `scripts/de00-look-test.py` and runs its Sharma 2005 self-test first. Downloaded sources are in `.claude/tmp/de00-src/`.

**Abstract or search summary only:** Luo et al. 2023 (Wiley returned 403 on every route; record pages only); Huang et al. 2022 (abstract page); Paravina et al. 2015 (search summary); Brychtová & Çöltekin 2015 IJC and 2017 ColorBrewer paper (search summaries and the ICC 2015 abstract); Ou & Luo 2006 and Szabó, Bodrogi & Schanda 2010 (citations only; the patent copy found was a scanned image); Witzel & Gegenfurtner 2013 and 2015 (search summary and as cited by Li & Nagai).

**Could not open:** Tableau 10 palette blog (403, and the page body did not load by curl); Springer page for the 2017 ColorBrewer paper (bot challenge); ResearchGate copies (403); TU Berlin STRESS tables for large differences (not tried after the search summary).

**Not done:** no new look test or observer data; no conversion of Healey's ΔE\*uv distances; no check of Datawrapper's git history for the origin of 9.2.
