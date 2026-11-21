# Research #340: how large a gap or seam at a contact must be before it shows at device pixel ratios 1–3

Date: 16 Oct 2026. Question: design-vault#340, for the build ticket #341 under spec #324. Labels: **opened** (full text or the cited section read), **abstract** (abstract or publisher page only), **secondary** (cited by another source; not read). Every number is marked **sourced**, **derived** (computed here from sourced inputs), **measured** (on this note's renders, in its dataset), **house** or **untraced**.

**Answer.** One threshold serves all three device pixel ratios: a seam shows once its **width × luminance contrast reaches 0.5 arcsec**. That is the floor of thin-line vision (Hecht & Mintz 1939, opened), for a line narrower than the eye's blur. What changes with the ratio is the angle one device pixel spans: about **109″ at DPR 1, 47″ at DPR 2 and 35″ at DPR 3** (derived, §2). The measurement it feeds: from two renders of the contact's two shapes, one over black and one over white, the share of ground in each device pixel along the contact. The contrast of each pixel against the pixel with no ground showing is summed across the edge per unit of its length, then multiplied by the device pixel's angle (§3). ΔE00 is the wrong measure: it is defined for fields over 4°, and a thin line's colour is blurred out before its luminance is (§1.3). The floor is a lab floor; the threshold for a glance in daily use is untraced. On Chromium's renders the choice barely matters for a contrasting ground: every seam and gap there measures 0.3–6,000″, with all but three over 3.5″, and every clean contact measures exactly 0 (§4). So #341 can be built at 0.5″. Overlaps stay with the critic (§5).

Data: `docs/data/contact-seams-2026-10-16.csv` (465 crops: each contact's largest ground share, its equivalent ground width and its width × contrast at each DPR). Instrument: `docs/data/contact-seams-2026-10-16.py`, run from the repo root. It builds the fixture page, renders it through `look-renders.py contacts` three times (as drawn, over black, over white), and writes the CSV. Renders were made on Playwright's Chromium 149.0.7827.0.

## 1. What the sources set

### 1.1 The thin-line threshold

- **Hecht & Mintz 1939** (J Gen Physiol 22:593, opened; the full scan). One opaque line on a uniform field. At 30.2 mL (96 cd/m², **derived**: the low end of display white) the threshold width is 0.00785–0.00802 arcmin, about **0.5 arcsec** (Table I, p. 596; "a wire which subtends only 0.5 second of arc", p. 600). **Sourced.** The line is seen because its blurred shadow lowers the light on one row of cones by ΔI/I ≈ 1/105 (pp. 602–603). For lines under about one cone wide (0.5 arcmin), that ΔI/I "is, as a first approximation, directly proportional to the visual angle they subtend" (pp. 605–606). **Sourced.**
- **Width × contrast.** If ΔI/I scales with width, then a line of Weber contrast C and width w is at threshold where w·C ≈ 0.5″. **Derived**: the paper tested opaque lines only, never a line of partial contrast.
- **Its limits.** It is a floor: a trained observer, a uniform field, a long line, no time limit. "The just resolvable angle increases rapidly when the background is irregularly illuminated" (p. 600). Hartridge's 3–4″ is cited there (**secondary**); §4 tests 3.5″, its middle. Whether a seam lighter than its fills has the same threshold as a darker one is **untraced**, as is the effect of a short seam.
- **The eye's blur.** The line spread has a half-width of 1 arcmin at a 3 mm pupil (Westheimer & Campbell 1962, abstract). Campbell & Gubisch 1966 find it 40% narrower (abstract). Hecht's proportionality holds for a line under one cone, about 35″ (p. 601, Fig. 3). A device pixel at DPR 3 (35″) is at that edge and one at DPR 2 (47″) just past it. At DPR 1 (1.3–1.9′) it is about the eye's full blur width. So the rule is at its edge at DPR 2 and 3 and an extrapolation at DPR 1, though a safe one: a resolved line needs more contrast, not less. **Derived.**
- **The luminance step at display white.** One just-noticeable difference is 0.75% at 100 cd/m² and 0.67% at 500 cd/m² (DICOM PS3.14, Equation 7-1, opened; computed from its constants: **derived**).

### 1.2 The visual angle of a device pixel

- CSS's reference pixel is "about 0.0213 degrees" (96 dpi at 28 in; CSS Values and Units 4 §6.2, opened), **sourced**; that is 76.7″ per CSS px (**derived**).
- At the nearest typical viewing distance, one device pixel spans **109″ at DPR 1** (96 dpi at 50 cm, the near end of OSHA's 50–100 cm for monitors, opened), **47″ at DPR 2** (MacBook Air, 224 ppi, Apple's spec page, opened, at 50 cm) and **35″ at DPR 3** (iPhone 16, 460 ppi, opened, at 32.2 cm, Bababekova et al. 2011's mean for web reading, abstract). **Derived.** Farther viewing shrinks these, which only lowers w·C.

### 1.3 Luminance, not ΔE00

- Colour-only acuity ends at 11–12 c/deg (Mullen 1985, abstract), a half-period of about 2.6′. Every device-pixel seam is finer than that. **Sourced** (acuity); **derived** (the comparison).
- S-CIELAB, the Wandell group's code (`scGaussianParameters.m`, opened), blurs its colour channels far more than luminance: 38–43% of their weight in Gaussians of 0.65–0.83° half-width.
- CIEDE2000's reference conditions call for a sample "larger than 4°", side by side, with no texture (Kraushaar 2013, a CIE meeting deck, **secondary** to CIE 142-2001). A 1-device-pixel line is outside them.

### 1.4 The conflation seam

- Two antialiased fills on one exact edge let the ground "leak through" (Khronos NV_path_rendering_shared_edge, Issue 1, opened). The leak is "particularly noticeable when two opaque paths exactly seam at a shared boundary" (Kilgard & Bolz 2012 §4.1.2, opened). Their Fig. 10 names Skia, Chromium's rasteriser, as a renderer that conflates. A Skia engineer calls it "working as intended", avoidable only by MSAA (skia-discuss, 15 June 2020, opened). No source gives a visibility threshold. **Sourced.**
- With coverage a for the first fill and 1 − a for the second, the ground's share of the pixel is **a(1 − a)**: 0.25 at most, at a = 0.5. **Derived**.

## 2. What Chromium's crops show

On 31 contacts (the instrument's `CASES`) on each of five grounds, at DPR 1, 2 and 3:

- **Chromium blends in sRGB-encoded values.** At blue-orange-on-white's vertical shared edge 0.25 CSS px off the grid, at DPR 1, the edge pixel reads (217, 172, 92). Blending in encoded values predicts (217.4, 172.6, 92.8), in linear light (224.2, 179.9, 131.0). **Measured**; the instrument prints the check.
- **A shared edge leaves a ground share of up to 0.25 at its worst pixel, at every DPR** (0.11–0.26 by edge and DPR). Averaged along a slanted or curved edge, the equivalent ground width is 0.15–0.17, 0.081–0.082 and 0.052–0.058 CSS px at DPR 1, 2 and 3. That is about 1/(6·DPR), the mean of a(1 − a). On a vertical edge at fraction f of a device pixel, it is f(1 − f)/DPR. It is zero where the edge falls on a pixel boundary: a vertical edge at x + 0.5 is clean at DPR 2 and seamed at DPR 1 and 3, and one at x + 1/3 is clean only at DPR 3. **Measured.** So the check must run all three DPRs, as `look-renders.py` already does.
- **A gap's equivalent width is its own width plus the conflation remainder.** A 0.5 CSS px gap reads 0.50–0.55, a 1 CSS px gap 0.996–0.999, at every DPR. A 30° slant reads cos 30° of its horizontal gap. **Measured.**
- **An underlap is clean once it is a full device pixel.** A 0.5 CSS px underlap leaks 0.047 CSS px of ground at DPR 1 and none at DPR 2 or 3; a 2 CSS px underlap is clean at all three. **Measured.**

## 3. The measurement

For each contact at each DPR, the check needs three crops: the page as drawn, and the contact's two shapes alone over black, then over white. For each device pixel in the window:

1. ground share g = (white − black) / 255, averaged over the channels (two-backing matting; exact here because Chromium's blend is linear in the encoded ground, §2);
2. the pixel with no ground showing: black / (1 − g), or the fill on the pixel's side where g ≥ 0.95;
3. C = |Y(drawn) − Y(no-ground)| / Y(no-ground), with Y the WCAG relative luminance.

w·C = Σ C over the window ÷ (the edge's length in the window, in device px) × the device pixel's angle (§1.2). **A contact fails at a DPR where w·C ≥ 0.5″.** A ground share at or under 0.5/255 counts as rounding (**untraced**, the instrument's setting).

## 4. The threshold on the fixtures

| | crops | ground showing | w·C ≥ 0.5″ | ≥ 3.5″ | ≥ 10″ | clean crops (w·C) |
|---|---|---|---|---|---|---|
| four contrasting grounds | 372 | 308 | 307 | 305 | 281 | 64 (all 0) |
| near-ground control | 93 | 77 | 50 | 4 | 0 | 16 (all 0) |

The near-ground control's ground lies within 3.3% of the fills' luminance. **Measured.**

- A conflation seam measures 9.8–315″ on light-on-dark, blue-orange-on-white and dark-on-paper. The one crop under 0.5″ is a red ground under a navy and cream pair whose edge pixels come near the ground's luminance.
- The line separates where the ground nears the fills' luminance. There the floor flags a conflation seam of under 1% contrast at DPR 1 (0.7–1.9″), which an everyday threshold might pass.

## 5. What a script cannot measure here

- **An overlap of two opaque fills leaves no trace at the edge.** Its pixels match an underlap's. Its fault is an outline moved out of place, and an edge offset shows at about 4–5″ where the edge's Michelson contrast is 0.22 or more, rising as contrast falls (vernier: Wehrhahn & Westheimer 1990, abstract; Westheimer 1977, abstract, gives 4–6″; **sourced**). That is about 0.1 device pixel at every DPR (**derived**). A crop cannot tell where the outline was meant to run, so the overlap stays with `vault.contacts-look` and `vault.contacts-code`.
- **A translucent fill** reads as ground in the matte wherever it lies. The check reports such a contact as unmeasurable (exit 6).
- **A seam lighter than its fills** (light-on-dark) is held to Hecht's dark-line figure, which is untraced for it. Every such seam here measures 9.8″ or more.

## 6. For #341

- Build `vault.contacts-seam` at w·C ≥ 0.5″ (Hecht & Mintz 1939; partial contrast **derived**), with the device-pixel angles of §1.2 (**derived**), each held in the check's one script.
- The two-backing renders draw only the contact's two shapes, so every other element is hidden for those two shots.
- #341's criterion that "an overlap" over the threshold fails cannot be met: an opaque overlap leaves the same pixels as an underlap (§5). Its fixtures are a closed contact, a gap and a ground-coloured seam.
- **Untraced**: the 0.5/255 rounding gate; the 5 CSS px window and the 4 CSS px fill offset; the 0.95 all-ground switch; the 1e-4 luminance floor. In the instrument alone: the fixture colours, the 0.37 CSS px offset off the pixel grid and the 60 px cell.
- A looser line for everyday viewing would be a house number: no source sets one, and a look test would be needed to measure it.

## Bound

Read in full: Hecht & Mintz 1939; CSS Values 4 §6.2; DICOM PS3.14 §3, §7 and Annex A; the Khronos extension; Kilgard & Bolz 2012 §4.1.2 and Fig. 10; the skia-discuss thread; Apple's iPhone 16 and MacBook Air spec pages; Android's density page; OSHA's monitor eTool; isetcam's `scGaussianParameters.m`. Abstract only: Westheimer & Campbell 1962, Campbell & Gubisch 1966, Mullen 1985, Bababekova et al. 2011, Wehrhahn & Westheimer 1990, Westheimer 1977, Westheimer, Brincat & Wehrhahn 1999. Secondary: Hartridge 1922, CIE 142-2001's reference conditions, Westheimer & McKee 1977. Not reached: Blackwell 1946, Zhang & Wandell 1997, Adobe's trapping pages (HTTP 403). Measured exhaustively: every crop of the 465 in the dataset. Sampled: five grounds and 31 contacts. No real art was measured, as no round on this machine has a contact list from `vault.contacts-code`.
