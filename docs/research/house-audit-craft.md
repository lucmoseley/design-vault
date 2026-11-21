# #183 audit: the craft gate and the motion and curve script constants

Scope: the eleven craft questions in `plugin/skills/design-critique/gate.md` §Craft (strength "founder ruling"), and the constants in `plugin/skills/design-round/scripts/check-flow.py`, `check-frames.py` and `check-overlay.py`. `check-curves.js` is also in scope here, because `vault.curves-script` runs it and the sibling constants audit (`research-183-constants.md`) does not list it. Date: 14 Oct 2026.

Key to dispositions:
- SOURCED: a published source supports the value. The entry gives a quote and a URL.
- CONFLICTS: research supports a different value. The entry gives that value and how far the house value is from it.
- GAP: no source can set the value. The entry gives the kind (a point on a measured curve, a taste, a business fact) and what the founder must pick.
- NOT A DESIGN CLAIM: an engineering knob. A measurement in use sets it. The entry names that measurement.

## Part 0. What the founder actually said, and what he accepted

 It is the most important context: the gate labels all eleven questions "strength: founder ruling", but most numbers in them are an agent's.

**P1. His own words (lucmoseley/mmm-infra#9, reply to round two, 5 Oct 2026, recorded word for word, comment 5988390174).** These are the only craft words that come from him and not from an agent:
- Curves: "The curves should all be perfectly smooth and match the trajectory of the original logo's curves exactly, no matter how finely one zooms in".
- Alignment: "stones are laid on a frame, but the frame and the stones dont align at all and have massive gaps between them … Every element should be carefully examined for correct alignment".
- Length: "Did you do research on how long people are willing to watch things like this, how that length should change based on the type of website and clientele … This should have been a carefully optimised consideration".
- Flow: "Most of the motion is janky and sudden, with long pauses interspersed with rapid jolts of animation. Everything should flow smoothly. Either as one continuous animation of uniform speed, or with speed-ups and slow-downs that feel natural to what's happened (e.g. water flow should match a gravitational calculation if falling). It occurs to me that these should be permanent enforced rules for any project I work on".
- Drafts: "I think each of the 10 directions show promise, so I'm not willing to discard any right now."
- He gave no number. He did not speak about page layout (sideways scroll, clipped text, the fold). The nearest words are about round two v5: "I'm not sure the spatial alignment (size and location) of the clickable items relative to the arches is well optimised".

**P2. The numbers came from an agent, and he accepted them in bulk (lucmoseley/mmm-infra#16, 5 Oct 2026).** The ruling comment: "His reply, word for word: 'accept recommendations'. Three questions were put; the recommendation on each is now the ruling." It then lists "The procedures put to him for each rule: curves are drawn as curves, overlaid on the source within 0.5 px and inspected at 8× zoom on the tightest bend. Touching shapes are derived from one shared geometry, with each contact inspected at 4× zoom on every key frame. Every move goes into a timeline table, with unnamed pauses, abrupt starts and stops, and non-ballistic falls flagged, plus a scrub at 0.25× speed." The resolution's own Bound line says: "The 250 ms pause threshold and the 8× and 4× zoom levels are this session's working figures, not from a source." The 0.5 px came from "`docs/research/logo-geometry.md` (its fit residuals, for the 0.5 px tolerance)", that is, from one JPEG logo's fit.

**P3. Later rulings, each an accepted recommendation.**
- design-vault#60, 6 Oct 2026: "ease-out entrances keep counting as jolts — option (A)".
- lucmoseley/mmm-infra#28, 9 Oct 2026: "He took every recommendation". Fold-ins: last frame exactly the logo (92 %), damped landing (#68), mid-move speed step (#69), hashes of kept drafts (65 %).
- design-vault#78, 13 Oct 2026: "the founder accepted Q5 (A)", which was whether to ship a width-sweep script.
- design-vault#132, 14 Oct 2026: "The founder accepted every recommendation … Q1 (A), Q2 (A), Q3 (B)". Q1 (A) made fall.js end a settle "at the moment it looks still", which is check-flow's 1 % still share (STILL_FRACTION).

**P4. Finding on the labels.** `vault.layout` cites "the founder, lucmoseley/mmm-infra#9" as its source. #9 holds no layout ruling (P1). Its real source is the #78 retro finding plus WCAG (see item 1.11). The other ten questions cite #9 correctly for the rule's spirit, but not for any number.

## Part 1. The craft questions

### 1.1 `vault.curves-script`: a true curve, and a trace within 0.5 px

- **Where:** `plugin/skills/design-critique/gate.md:22-30`; the limit is `LIMIT = 0.5` at `plugin/skills/design-round/scripts/check-overlay.py:66`; the polygon test is `MIN_RUN = 4`, `MIN_TURN = 0.5`, `MAX_TURN = 30` at `plugin/skills/design-round/scripts/check-curves.js:25-27`.
- **Ruling:** the rule is his ("perfectly smooth and match the trajectory of the original logo's curves exactly, no matter how finely one zooms in", mmm-infra#9). The 0.5 px is an agent's number, accepted in bulk with "accept recommendations" (mmm-infra#16, P2). Its basis was one JPEG logo's fit residuals (mmm-infra `docs/research/logo-geometry.md` F1-F2: noise floor 0.06 px RMS; best fits 0.36-0.39 px max).
- **Research:**
  - Potrace, the reference bitmap tracer (Selinger 2003, https://potrace.sourceforge.net/potrace.pdf §2.2): a straight segment "approximates the path if d(v0,a) ⩽ 1/2, d(vn,b) ⩽ 1/2, and for each i … there exists some point ci on ab such that d(vi,ci) ⩽ 1/2", in pixel units (max-distance). Its curve step then allows ε: "the tolerance of the curve optimization algorithm; it is pre-set to 0.2" (man page: "-O n, --opttolerance n … The default value is 0.2", https://potrace.sourceforge.net/potrace.1.html). So a standard tracer accepts about 0.5 px from a raster source's pixel edge.
  - check-overlay.py's own measured error is 0.05 px at 8× and 0.08 px at 4× (`check-overlay.py:67-69`, design-vault#73). So the tool can resolve about 0.1 px.
  - Font outline QA tests every join between segments by its tangents, with no zoom: FontBakery `outline_jaggy_segments` reads `prev.tangentAtTime(1)` and `this.tangentAtTime(0)` (https://github.com/fonttools/fontbakery/blob/main/Lib/fontbakery/checks/outline_jaggy_segments.py). Red Arrow (Jens Kutilek's outline checker for RoboFont) flags an "Incorrect smooth connection" when a node's handle is more than 0.49 grid units off the line of its partner (https://github.com/jenskutilek/RedArrow, `outlineTestPen.py` `_checkIncorrectSmoothConnection`).
- **Disposition: SOURCED for a raster source; CONFLICTS for a vector source.**
  - Raster source (a JPEG or PNG logo): 0.5 px at the source's size agrees with potrace's 1/2-px tracing criterion and sits just above the measured fit maximum (0.39 px) of the one logo it was set on.
  - **Vector source: his words ask for an exact match "no matter how finely one zooms in". A 0.5 px offset at the source's size shows as 4 px at 8× zoom. The tool resolves about 0.1 px, so for an SVG source the limit can be about five times tighter. The value he accepted departs from his own rule by that factor.** Research supports: limit = the tool's measured error (about 0.1 px) for a vector source; limit = the source's own measured edge noise, capped at potrace's 0.5 px, for a raster source.
  - **check-curves.js tests only runs of straight segments (`check-curves.js:120-135`: a `curve` segment never joins a run). A corner between two Bézier segments (handles not collinear) passes it, and so does a polygon whose turns are over 30° each (a hexagon, 60°).** Font QA practice tests the tangent at every node. That is the check that meets "any zoom". MIN_RUN 4, MIN_TURN 0.5° and MAX_TURN 30° have no source; FontBakery's nearest constant, `JAG_ANGLE = 0.25` rad (`outline_settings.py`), tests a different fault (a spike).
- **Confidence:** high (0.85) for the raster/vector split; it rests on primary tool docs and the vault's own measurements. A viewing test that showed a 0.3-0.5 px offset of a vector mark invisible at the zooms a visitor uses would move it towards keeping 0.5 px. But that would contradict his "any zoom" words, so it would need his ruling.

### 1.2 `vault.curves-look`: 8× zoom on the tightest bend

- **Where:** `gate.md:32-40`. The 8× also sets `check-overlay.py`'s default scale (`MAX_SCALE`, `check-overlay.py:70`), which is a separate, measured knob (see 2.2).
- **Ruling:** agent's. mmm-infra#16's resolution: "The 250 ms pause threshold and the 8× and 4× zoom levels are this session's working figures, not from a source." He accepted it in bulk.
- **Research:** no published source sets an inspection zoom for curve smoothness. Outline QA tools do not inspect by zoom. They test tangent continuity at each node in the path data (1.1). A tangent break is a fact of the data at every zoom; an 8× view finds only the breaks large enough to see at 8×.
- **Disposition: CONFLICTS.** **His words ask for smoothness "no matter how finely one zooms in"; a fixed 8× look checks one zoom only.** Research practice (FontBakery, Red Arrow) supports an analytic node-tangent check in the script, with the look kept as a back-up for raster or script-drawn curves.
- **Confidence:** high (0.8). A case where a corner shows only in the render and not in the path data (for example a stroke join, or a raster filter) would keep a look question, but not a fixed 8×.

### 1.3 `vault.contacts-code`: both sides of a contact from one curve or its offset

- **Where:** `gate.md:42-50`.
- **Ruling:** his complaint ("the frame and the stones dont align at all and have massive gaps", mmm-infra#9). The "one shared curve or an offset" method is an agent's procedure, accepted in bulk (mmm-infra#16).
- **Research:** the Khronos extension NV_path_rendering_shared_edge, Issue 1 (https://registry.khronos.org/OpenGL/extensions/NV/NV_path_rendering_shared_edge.txt): "Path rendering sometimes requires subregions of two paths to be drawn such that they are 'watertight'. This means that the color samples along this shared contour should not have any coverage gaps or double hits." It then says that with fractional coverage, "an artifact known as 'conflation' … allows a background color to 'leak through' the edge". The extension fixes it only by marking the edge as shared in the renderer.
- **Disposition: SOURCED** (the rule). Shared geometry is the precondition for a watertight contact. **Note: it is not enough in a browser.** Two separately filled shapes that share an exact edge still leak the ground along that edge under anti-aliasing (conflation). A browser has no shared-edge mark. The usual fixes are to draw both sides as one path, or to extend the lower shape under the upper one. The question does not ask for either.
- **Confidence:** medium-high (0.75). I did not measure a conflation seam in Chromium for this audit; a test render of two shapes on one shared Bézier edge would confirm or remove the note.

### 1.4 `vault.contacts-look`: 4× zoom on every contact

- **Where:** `gate.md:52-60`.
- **Ruling:** agent's working figure (mmm-infra#16 Bound line, quoted in 1.2), accepted in bulk.
- **Research:** no source sets an inspection zoom for contacts. A gap or a conflation seam is visible to a visitor at the visitor's device pixel ratio (1× on most desktops, 2-3× on phones). A render at 4× device scale makes a seam narrower relative to the shapes, so it can hide what a 1× visitor sees.
- **Disposition: NOT A DESIGN CLAIM** (an inspection knob). The measurement that settles it: render each contact at the device pixel ratios the project's visitors use (1×, 2×, 3×; from the project's analytics), magnify those pixels without re-rendering, and count edge pixels whose colour lies outside both sides' colours. The question text should say "magnified", not "rendered at", 4×. That is a wording fix, not a founder question.
- **Confidence:** medium (0.65). It depends on how critics read "viewed at 4× zoom" today, which I did not observe.

### 1.5 `vault.flow-script`, part 1: no pause over 250 ms unless the brief names it as a hold

- **Where:** `gate.md:62-70`; `PAUSE_MS = 250` at `check-flow.py:77`.
- **Ruling:** the rule is his ("long pauses interspersed with rapid jolts", mmm-infra#9). The 250 ms is an agent's working figure. The census agrees: "the 250 ms number has no source" (`docs/research/design-rules-census.md:32`). He accepted it in bulk.
- **Research:** Thomas and Johnston, *The Illusion of Life* (1981), on the Moving Hold (scan at https://archive.org/details/disney-animation-the-illusion-of-life, djvu text lines 4348-4362): a pose "was held without movement on the screen for a few frames—at least eight, maybe as many as sixteen … That amounted to less than a second, but it was enough. However, when a drawing was held for that long, the flow of action was broken, the illusion of dimension was lost, and the drawing began to look flat. A way had to be found to 'hold' the drawing and still keep it moving!" At 24 fps, 8 frames is 333 ms and 16 frames is 667 ms.
- **Disposition: SOURCED, approximately.** The only primary source found puts the point where a still spell breaks the flow at 8 frames, 333 ms. 250 ms (6 frames at 24 fps) is 83 ms stricter. Both values are in the band the source supports. No perception paper found sets a "pause" threshold for animation.
  - **Finding on named holds:** the same source says a still hold of 8-16 frames breaks the flow even when it is wanted, and the craft answer is a *moving* hold (the pose drifts on). The gate excuses any still hold the brief names, of any length. Disney practice supports a narrower excuse: a hold that keeps moving, or a still hold only at the very end. The founder's own note on round two v2, "the full-page logo at the end feels like it hangs for a bit too long", agrees with that.
- **Confidence:** medium (0.6). One craft source, about character poses, not shapes; I read the passage in full. A viewing test with stills of 200-400 ms in brand motion would set the point on a measured curve.

### 1.6 `vault.flow-script`, part 2: no move from rest that starts or stops at full speed

- **Where:** `gate.md:64`; `JOLT_RATIO = 0.5` at `check-flow.py:80` ("A guess at where full speed begins; no source found").
- **Ruling:** the rule is his in spirit ("janky and sudden … rapid jolts"). The 50 % number is the #60 builder's deviation: "'full speed' needs a number to measure against". On 6 Oct 2026 he ruled on design-vault#60 that "ease-out entrances keep counting as jolts — option (A)"; the ruling comment says it "rests on the founder's complaint in lucmoseley/mmm-infra#9". The options and their pricing are not on the ticket, so I cannot say if (A) was the agent's recommendation.
- **Research:**
  - Lasseter, "Principles of Traditional Animation Applied to 3D Computer Animation", SIGGRAPH '87, §2.7 (https://www.ics.uci.edu/~fowlkes/class/ics162/exercises/lasseter.pdf): "Slow in and slow out deals with the spacing of the inbetween drawings between the extreme poses. Mathematically, the term refers to second- and third-order continuity of motion." This supports the rule for a move between two rests.
  - The same paper, §2.7, on Luxo Jr.'s heavy base: "we wanted the base to start stationary, then pop up in the air from the momentum of his jump, arc over, then land with a thud, suddenly stationary again … This gave the desired feeling of weight". So for a heavy landing, Pixar's practice is a stop at full speed.
  - Thomas and Johnston (lines 4406-4410): "Too much of this [slow in and slow out] gave a mechanical feel to the action".
  - Material Design's easing tokens (material-components-android `docs/theming/Motion.md`, https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md): standard `cubic-bezier(0.2, 0, 0, 1)` "for utility focused animations that begin and end on screen" starts slowly; standard decelerate `cubic-bezier(0, 0, 0, 1)` is "used for utitlity [sic] focused animations that enter the screen", and emphasized decelerate `cubic-bezier(0.05, 0.7, 0.1, 1)` "for common, M3-styled animations that enter the screen". Both decelerate curves start at their top speed (initial slope infinite and 14× the mean).
  - Apple HIG, Motion (https://developer.apple.com/design/human-interface-guidelines/motion): "Strive for realistic feedback motion that follows people's gestures and expectations." It gives no easing rule.
- **Disposition: SOURCED for a move that begins and ends on screen; CONFLICTS for entrances and for heavy landings.**
  - **His #60 ruling (ease-out entrances are jolts) departs from Material, which puts every element that enters the screen on a decelerate curve that starts at top speed.** `vault.flow-script` applies to any asset with motion, web surfaces included, so a Material-standard entrance on a page fails the vault gate. The census already found the same clash with impeccable's craft floor ("exponential ease-out", `design-rules-census.md:396`). The vault confines "never ease-in" to UI motion (`design-round` brand-motion easing), but it does not confine the jolt rule to brand motion.
  - **The rule also fails Lasseter's "land with a thud, suddenly stationary again", Pixar's way to show weight.** The vault answers this with a damped landing (1.8), which is a choice the founder was not asked about as such.
  - JOLT_RATIO 0.5 itself: **GAP, a point on a measured curve that does not exist yet.** No source gives the share of top speed at which a start looks abrupt. Dzhafarov, Sekuler and Allik (1993, Perception & Psychophysics 54, doi:10.3758/BF03211798; abstract only) found reaction time to a change depends on |V1 − V0|^(2/3), with no threshold for "abrupt". A viewing test (pairs of starts with different first-frame speed shares, viewers say which looks abrupt) would give the curve; the founder then picks the cut-off.
- **Confidence:** high (0.8) on the Material and Lasseter facts, read in primary text. Medium (0.55) on how much the entrance clash matters: it depends on whether web-surface UI entrances ever run through `vault.flow-script` in practice.

### 1.7 `vault.flow-script`, part 3: no speed step of 2× or more in the middle of a move

- **Where:** `gate.md:64`; `STEP_RATIOS = (2, 3, 4)`, `STEP_HOLD = 1.5`, `STEP_HOLD_FRAMES = 3`, `STEP_FLOOR = 0.2` at `check-flow.py:118-121`.
- **Ruling:** he accepted the fold-in on mmm-infra#28 ("He took every recommendation"). The 2× was the ticket's "example, to be tuned" (design-vault#69 body); the builder kept 2× and tuned the guards on 24 synthetic easings so that no smooth easing flags (#69 tuning comment).
- **Research:**
  - Snowden and Braddick (1991), "The temporal integration and resolution of velocity signals", Vision Research 31, doi:10.1016/0042-6989(91)90156-Y (abstract only): speed discrimination thresholds "fell asymptotically to a Weber fraction around 0.06"; to tell a pattern "modulated between two speeds from one which remained at a constant speed", "the minimum depth of the modulation … was found to be equivalent to a Weber fraction of 0.3 at low modulation rates".
  - Mateeff et al. (2000), "The discrimination of abrupt changes in speed and direction of visual motion", Vision Research 40, doi:10.1016/S0042-6989(99)00185-6 (abstract only): for two contiguous motions, "for the lowest value of duration the Weber fraction for contiguous speeds was more than three times as the Weber fractions for separate speeds".
- **Disposition: CONFLICTS (the size), with a sampling limit.** **Research puts a visible change of speed inside one continuous motion at about 1.3× (Weber fraction 0.2-0.3), not 2×. The gate passes a step of up to 2× (Weber fraction 1.0), about three times the detection threshold.** The sweep shows why 2× was kept: at 60 fps, smooth easings change speed by close to 2× per frame near rest, so a lower ratio would flag them. So the ratio is partly a detector knob. The research value cannot be adopted without a detector that tells a step from smooth acceleration (for example, a jump in acceleration rather than in speed). That is an engineering ticket, not a founder question.
- **Confidence:** medium (0.6). I read abstracts only; the stimuli were random-dot fields at 2-16 deg/s, not one shape. The full texts of Snowden and Braddick and of Mateeff et al. would move it.

### 1.8 `vault.flow-code`: a fall or throw is ballistic, y = ½gt² at one px-per-metre scale, and lands on a damped spring

- **Where:** `gate.md:72-80`; `plugin/skills/design-round/scripts/fall.js`.
- **Ruling:** the gravity rule is his own words: "water flow should match a gravitational calculation if falling" (mmm-infra#9). "One stated pixels-per-metre scale" is an agent's procedure (mmm-infra#16), accepted in bulk. The damped landing is mmm-infra#25 fold-in 2, accepted on mmm-infra#28 and built in design-vault#68.
- **Research:**
  - The fall itself is Newtonian mechanics; no source is needed for y = ½gt².
  - Hecht, Kaiser and Banks (1996), "Gravitational acceleration as a cue for absolute size and distance?", Perception & Psychophysics 58, doi:10.3758/BF03206833 (abstract): "observers were much more sensitive to average velocity than to the gravitational acceleration pattern." So the px-per-metre scale, which sets the average speed, is what a viewer judges. Stating one scale per asset is supported.
  - Phan, Jörges, Harris and Kingdom (2024), "A visual bias for falling objects", Perception, doi:10.1177/03010066241228681 (abstract): "more acceleration was needed for a downward-falling object to appear at constant velocity". So a true t² fall looks less accelerated than it is; it does not look over-accelerated.
  - Bozzi (1959) found the motion judged most natural for a block sliding down a slope accelerated in the first third, then ran at constant speed; Shanon (1976) found true uniform acceleration judged more natural for a vertical fall. I saw these only as cited in a search summary (Vicovaro et al.), not in the originals.
  - Landing: Lasseter (1.6) shows Pixar landing a heavy mass "with a thud, suddenly stationary again", with follow-through in the loose parts ("the arms were rotated quickly together two frames after the base lands"). A rigid stone also stops within a few milliseconds in physics, less than one frame.
- **Disposition: SOURCED** (the ballistic fall and the stated scale). **The landing part CONFLICTS:** **he asked for a gravitational calculation; physics and Pixar's practice both end a heavy fall in a stop at full speed (a thud), with follow-through in secondary parts. The house landing (the mass sinks and rises on a spring) is a stylisation chosen so that the jolt rule (1.6) passes. ** Whether a brand piece should land with a thud or a sink is a **taste** the founder was never asked as such. What he needs to pick: thud (with follow-through) or sink, shown side by side on one stone.
- **Confidence:** high (0.8) on the physics and Lasseter text; medium (0.5) on the perception papers, read as abstracts only.

### 1.9 `vault.flow-look`: one continuous pace, scrubbed at 0.25× speed

- **Where:** `gate.md:82-90`.
- **Ruling:** the question is almost his words ("Either as one continuous animation of uniform speed, or with speed-ups and slow-downs that feel natural to what's happened"). The 0.25× scrub is an agent's procedure (mmm-infra#16), accepted in bulk.
- **Research:** Lasseter §2.2 Timing: "More than any other principle, timing defines the weight of an object … A heavy body is slower to accelerate and decelerate than a light one." This supports "change speed only with what is happening".
- **Disposition: SOURCED** (the rule: his words plus Lasseter). The 0.25× scrub is **NOT A DESIGN CLAIM** (an inspection knob). The measurement that settles it: in a sample of rounds, the share of faults that critics find at 0.25× and miss at 1×, against the extra review time.
- **Confidence:** high (0.8) for the rule.

### 1.10 `vault.length-range` and `vault.length`: a length range from research, and the render inside it

- **Where:** `gate.md:92-110`.
- **Ruling:** his own words: "Did you do research on how long people are willing to watch things like this, how that length should change based on the type of website and clientele" (mmm-infra#9). Not an agent's advice.
- **Research:** the rule is a demand for research, so it needs no outside source. Lasseter §2.2 supports the aim: "If too much time is spent on any of these, the audience's attention will wander. If too little time is spent, the movement may be finished before the audience notices it". The length values themselves are each project's research (for mmm-infra, its #13, `animation-length.md`), out of this group's scope.
- **Disposition: SOURCED** (his own requirement; no number in the vault).
- **Confidence:** high (0.9).

### 1.11 `vault.layout`: no sideways scroll, no clipped or overlapping text, the call to action on the first screen

- **Where:** `gate.md:132-140`; `check-layout.py` (its constants are in the sibling audit `research-183-constants.md`).
- **Ruling:** **the source line is wrong.** It cites "the founder, lucmoseley/mmm-infra#9", but #9 holds no layout ruling (P1). The four faults come from a workflow-core retro finding (session 631cff6d), and he accepted design-vault#78 Q5 (A), "Ready for an agent: the sweep as filed", on 13 Oct 2026. The agent recommended (A) at 90 %.
- **Research:**
  - WCAG 2.2 SC 1.4.10 Reflow (https://www.w3.org/TR/WCAG22/#reflow): content can be presented "without loss of information or functionality, and without requiring scrolling in two dimensions" at a width equal to 320 CSS px. SC 1.4.12 Text Spacing asks for "no loss of content or functionality". These cover sideways scroll, clipped text and text hidden under other content.
  - NN/g, "Scrolling and Attention" (15 Apr 2018, https://www.nngroup.com/articles/scrolling-and-attention/): "users spent about 57% of their page-viewing time above the fold", and "Keep major CTAs above the fold."
- **Disposition: SOURCED** (WCAG 2.2 for the three layout faults, NN/g for the call to action). The gate is stricter than WCAG in one way, in line with its aim: it checks every width from 320 to 1920 px, not only 320 px. The source line should cite WCAG 2.2 SC 1.4.10 and 1.4.12 and NN/g 2018, and #78, not mmm-infra#9. With WCAG as a source, the faults would take strength "WCAG 2.2 AA" and level 1, which changes how they yield on a clash.
- **Confidence:** high (0.85). I read the NN/g page through a fetch summary that quoted it. The WCAG 2.2 quotes were re-read at the URL (1.4.10 also names an exception: "parts of the content which require two-dimensional layout for usage or meaning").

### 1.12 `vault.drafts-kept`: every earlier round keeps its tag, and a kept draft renders the same frames

- **Where:** `gate.md:112-120`; `check-frames.py hash`.
- **Ruling:** his words: "I'm not willing to discard any right now" (mmm-infra#9). The tag procedure (mmm-infra#16) and the frame hashes (mmm-infra#28 (C), 65 %) are agents' recommendations, accepted.
- **Disposition: NOT A DESIGN CLAIM.** It is a process and regression rule, not a claim about how a design looks. Its one number, "the same frames" (hash equality), is an equality oracle. The measurement that would change it: the false-failure rate of `hash --check` across Chromium upgrades on real kept drafts (`--check` already names a browser change).
- **Confidence:** high (0.85).

### 1.13 `vault.end-frame`: the last frame is the asset's own end frame, pixel for pixel

- **Where:** `gate.md:122-130`; `check-frames.py last`.
- **Ruling:** mmm-infra#28 Q2 (A), "last frame exactly the logo", 92 %, the agent's recommendation, accepted. The aim (end on the logo) is in Mark's brief and the founder's rounds.
- **Research:** the fault it guards against is a compositing fact. Porter and Duff, "Compositing Digital Images" (SIGGRAPH '84): with the over operator, an edge pixel of coverage α drawn twice reaches 1 − (1 − α)², which is more than α, so a doubled edge is heavier. mmm-infra#25 M1b measured this: 1,390 edge pixels changed, by up to 48 grey levels. I cite Porter and Duff from knowledge of the paper, not a re-read.
- **Disposition: NOT A DESIGN CLAIM** for the zero tolerance (an equality oracle; the design claim under it, that a doubled edge is visible, is a compositing fact). The measurement that would justify a tolerance above zero: the smallest end-frame difference that viewers see as a "pop" at the hand-off, against the false failures on real rounds (none recorded yet; #67 ran synthetic pages only).
- **Confidence:** high (0.8).

## Part 2. The script constants

Every constant below was set by a building agent. None had a founder ruling of its own, except where the row says so. "Ruled" names a ruling that rests on the constant.

### 2.1 The two constants that are design claims

**`DESKTOP = "1280x800"`** (`check-flow.py:93`; "a common laptop screen, a guess at a typical desktop visitor"; every design-round script renders at it unless told).
- Ruling: none.
- Research: StatCounter, desktop screen resolution, worldwide, September 2026 (https://gs.statcounter.com/screen-resolution-stats/desktop/worldwide, read through a fetch summary): 1920×1080 28.07 %, 1536×864 10 %, 1366×768 7.95 %, 1280×720 4.71 %, 2560×1440 3.95 %. 1280×800 is not in the top six. StatCounter reports the screen, not the browser viewport, which is smaller by the browser's own bars.
- Disposition: **CONFLICTS.** The typical desktop screen is 1920×1080, or 1536×864 at 125 % scaling; 1280×800 is narrower than the top three. The best value is a **business fact**: the project's own visitor analytics. Where a project has none, StatCounter's top size, less the browser's bars, is the default research supports.
- Confidence: medium (0.65). It moves with the project's analytics; for a site whose visitors work on laptops it may stand.

**`STILL_FRACTION = 0.01`** (`check-flow.py:96`; "A channel slower than this share of its own top speed counts as still").
- Ruling: it rests under design-vault#132 Q1 (A), accepted 14 Oct 2026: "`fall.js` ends the settle at the moment it looks still". The question told him: "It would flip only if you count that last creep as motion people are meant to see."
- Research: the lowest speed people see as motion is an absolute angle per second, not a share of a move's top speed. Leibowitz (1955, JOSA 45:829, doi:10.1364/JOSA.45.000829) found about 1-2 arcmin/s with a stationary reference; Snowden and Kavanagh (2006, Perception 35, doi:10.1068/p5399) measured lower thresholds near 0.1 deg/s for young adults. I have both figures from secondary summaries only (an MDPI review and Looke et al. 2020); I could not read the originals. One CSS px at 96 px/inch seen from 60 cm is about 1.5 arcmin.
- Disposition: **CONFLICTS (form, not only value).** **For a fast move the 1 % share is well above the motion threshold: a settle after a 500 px/s impact counts as still below 5 px/s, about 7.6 arcmin/s, four to eight times the 1-2 arcmin/s threshold.** Research supports a floor in absolute angular speed (arcmin/s at a stated viewing distance), which for a slow move would be a larger share than 1 %. The practical harm is small: the end of a settle is a very slow stop. The fix is an engineering ticket; it needs a viewing distance per asset class, which is a business fact (desktop about 60 cm, phone about 30 cm).
- Confidence: low-medium (0.45). It rests on secondary numbers, and threshold experiments use long exposures; a settle's creep lasts 300-750 ms, where thresholds are higher (Leibowitz 1955, J Exp Psychol, doi:10.1037/h0042154, title only). Reading the two Leibowitz papers in full would move it.

### 2.2 The engineering knobs (NOT A DESIGN CLAIM)

| Constant | Where | What it controls | The measurement that settles it |
|---|---|---|---|
| `PAUSE_MS = 250` | `check-flow.py:77` | design claim: see 1.5 | — |
| `JOLT_RATIO = 0.5` | `check-flow.py:80` | design claim: see 1.6 (GAP) | — |
| `FPS = 60` | `check-flow.py:82` | sample rate | The faults found at 120 fps and missed at 60 on real round pages (#69 swept 30/60/120 on synthetic moves only), against the share of visitors on 90-120 Hz screens. |
| `QUIET_MS = 2000` | `check-flow.py:85` | when a page counts as done starting things | The longest gap between two beats in real timer-sequenced candidates; set above it with a margin. |
| `PLAY_TIMEOUT_MS = 60000` | `check-flow.py:88` | the wait for a whole page | The longest real candidate's load plus play time. |
| `LOAD_TIMEOUT_MS = 30000` | `check-flow.py:90` | the wait for one load | Already sourced: Playwright's default timeout. |
| `STILL_FRACTION = 0.01` | `check-flow.py:96` | design claim: see 2.1 | — |
| `NOISE = 0.02` | `check-flow.py:100` | float noise floor per channel | Measured for a box's position; for opacity, colour and dash offset, the largest frame-to-frame change of a still element across real pages. Evidence on #60: a linear 50 s fade sits at the floor. |
| `PX_NOISE = 5e-4` | `check-flow.py:106` | float noise in px | Measured on one page (mmm-infra#35); the largest still-box wobble across more real pages, against the smallest real move in a frame (1e-3 px). |
| `STEP_RATIOS = (2, 3, 4)` | `check-flow.py:118` | the step size: see 1.7 (CONFLICTS) | — |
| `STEP_HOLD = 1.5`, `STEP_HOLD_FRAMES = 3`, `STEP_FLOOR = 0.2` | `check-flow.py:119-121` | guards that keep smooth easings, bounces and landings from flagging | Measured: #69's sweep of 24 easings and 9 landings at 30, 60, 120 fps. Still to measure: the false flags and misses on real round pages. |
| `TURN_FRAMES = 2` | `check-flow.py:127` | a reversal inside a frame read as still | Measured: #151's grid, 2,640 runs. A frame-quantisation artefact, not a perception threshold. |
| `REWRITE_FRAMES = 5`, `REWRITE_SPAN_MS = 250` | `check-flow.py:134-135` | detects script-driven motion | The count of setup writes that real framework pages make (React, GSAP, a storyboard's class changes). |
| `DROPPED_FRAMES = 2`, `BROWSER_FRAME_MS = 1000/60` | `check-flow.py:140-141` | when a gap in frames fakes a jolt | Sourced in part: headless Chromium draws at 60 Hz. The rest: the gap lengths a loaded machine leaves (#126). |
| `ATTEMPTS = 3` | `check-flow.py:144` | reloads before a stretch is "not measured" | The success rate per attempt under load. |
| `PALETTE`, chart sizes | `check-flow.py:833`, `:842` | the critic's speed chart | None needed; it is the chart, not the candidate. |
| `FINISH_ROUNDS = 20` | `check-frames.py:83` | how many end chains `last` finishes | The deepest finish-event chain on real candidates. |
| `--margin` default 2 px | `check-frames.py:575` | CSS px compared around the asset's box | The widest legitimate difference outside the box (anti-aliasing bleed, a filter or shadow) on real hand-offs. |
| `LIMIT = 0.5` | `check-overlay.py:66` | design claim: see 1.1 | — |
| `MAX_SCALE, MIN_SCALE = 8, 4` | `check-overlay.py:70` | render scale | Measured: offset error 0.05 px at 8×, 0.08 at 4×, 0.18 at 2×, 0.30 at 1× (#73). |
| `MAX_SIDE = 4096` | `check-overlay.py:73` | memory ceiling | Peak memory of one run at 4096 px, against the machine's limit. |
| `NEAR = 2` | `check-overlay.py:76` | search radius for a raster's strongest ink | The offset error against NEAR on real raster sources of different blur and upscale. |
| `FLOOR = 0.1` | `check-overlay.py:80` | weakest ink counted | The noise amplitude in real sources' grounds (JPEG) against the contrast of their lightest ink part. |
| `SHOTS = 2` | `check-overlay.py:85` | screenshot retries | Measured on #136: the second shot drew. |

Confidence for the table: high (0.85) that each knob is engineering, not taste. A knob moves to "design claim" only if a test shows it changes what a viewer would see, as `STILL_FRACTION` does.

## Part 3. Summary: where a value he ruled on departs from research

Every row is a value that carries "founder ruling", or that a founder ruling rests on, and that research does not support.

1. **0.5 px trace limit for a vector source (1.1).** His words: exact "no matter how finely one zooms in". The tool resolves about 0.1 px. Research supports 0.5 px only for a raster source (potrace).
2. **8× zoom for corners (1.2), and check-curves.js missing corners between Bézier segments (1.1).** Font QA practice tests the tangent at every node, which meets "any zoom"; a fixed 8× look does not.
3. **Ease-out entrances counted as jolts (#60 ruling, 1.6).** Material puts every entering element on a decelerate curve that starts at top speed, and the jolt rule applies to web surfaces too.
4. **No stop at full speed, applied to landings (1.6, 1.8).** He asked for a gravitational calculation; physics and Lasseter's Luxo Jr. land a heavy mass "with a thud, suddenly stationary again". The house spring sink is a stylisation, never put to him as a choice.
5. **Speed step threshold 2× (1.7).** A change inside one motion is visible at about 1.3× (Weber fraction 0.2-0.3). The 2× is held up by the detector, not by perception.
6. **The 1 % "looks still" share behind #132 Q1 (2.1).** Motion threshold is absolute (about 1-2 arcmin/s), so a 1 % share of a fast move is visible motion. Low confidence; small practical harm.

Values that research supports or brackets: the 250 ms pause (Disney's 8-frame hold, 333 ms, 1.5); the ballistic fall at a stated scale (1.8); the length range (his own words, 1.10); the layout faults (WCAG 2.2 and NN/g, 1.11, but with a wrong source line).

Genuine gaps for the founder (each a priced question):
- **JOLT_RATIO (1.6): a point on a measured curve.** No source gives the first-frame share of top speed at which a start looks abrupt. The vault must first measure the curve (a viewing test); then he picks the cut-off.
- **Landing style (1.8): a taste.** Thud with follow-through, or a spring sink, shown side by side on one stone.
- **DESKTOP viewport (2.1): a business fact,** per project, from its analytics.
- **Named holds (1.5): a taste,** whether a named hold must keep moving (Disney's moving hold) or may stand still.

Corrections with no founder question (tickets): an analytic node-tangent check in check-curves.js (1.1, 1.2); a vector/raster split for the 0.5 px limit (1.1); "magnified, not rendered at" 4× for contacts, at the visitors' device pixel ratios (1.4); the source line of `vault.layout` (1.11); a step detector that can go below 2× without flagging smooth easings (1.7); an absolute-speed still floor (2.1); a note on conflation seams at shared edges (1.3).

Bound: Read in full: #183's body; `gate.md` §Craft (lines 1-140); the craft-constant blocks of `check-flow.py` (lines 60-175, 835-850), `check-frames.py` (lines 60-110, 570-580) and `check-overlay.py` (lines 1-90); `check-curves.js` lines 1-135; mmm-infra#9, #16 and #28 with comments; design-vault #60, #67, #68, #69, #73, #151 with bodies and comments, #78's triage and ruling comments, #132's question round; Lasseter (SIGGRAPH '87) §2.2, §2.7, §2.8 in the PDF; *The Illusion of Life* Moving Hold and Slow In and Slow Out passages in the archive.org text; potrace's paper §2.2-2.3 tolerance passages and man page; FontBakery's outline checks and settings; Red Arrow's smooth-connection test; Material's Motion.md easing table; Apple HIG Motion page text; WCAG 2.2 SC 1.4.10 and 1.4.12. Abstracts only: Snowden and Braddick 1991; Mateeff et al. 2000; Dzhafarov et al. 1993; Hecht et al. 1996; Phan et al. 2024; Snowden and Kavanagh 2006. Through a search or fetch summary only: Leibowitz 1955 thresholds, Bozzi 1959 and Shanon 1976, NN/g "Scrolling and Attention", StatCounter, the Khronos shared-edge issue text. From knowledge, not re-read: Porter and Duff 1984. Sampled: `design-rules-census.md` (grep for the craft rows), mmm-infra `logo-geometry.md` (F1-F2 residuals) and `animate-vs-our-method.md` (M1a, gap B, fold-ins). Not read: design-critique SKILL.md §1a beyond its script lines; McIntyre et al. 2001 (no abstract found); the pricing of the #60 ease-out options (not on the ticket).

## Owners

Items 1.1-1.5 and 1.11: #195. Items 1.6-1.9 and §2.1: #196. The ease-out ruling, landings and named holds: #183's questions to the founder.
