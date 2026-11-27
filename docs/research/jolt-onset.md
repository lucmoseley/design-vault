# Research: is there a source for JOLT_RATIO (the share of top speed at which a start from rest looks abrupt)?

Derivation scripts: the comment on #221 at https://github.com/lucmoseley/design-vault/issues/221#issuecomment-6193708416.

Question: `check-flow.py` calls a move from rest a "jolt" when its first frame (at 60 fps) runs at JOLT_RATIO = 0.5 or more of the top speed of the move. Is there published research or practice that gives this line, or lets us derive it, or gives a better parameter?

Start point: `docs/research/house-audit-craft.md` §1.6 found no source (Lasseter 1987, Material easing tokens, Apple HIG, Dzhafarov et al. 1993 abstract).

Note on the checker: the "speed" of a frame is the mean speed across that frame interval (displacement / frame time). Thus the share for one easing curve changes with the duration of the move (number of frames). A linear move always gives share 1.0.

Status: complete (see Verdict at the end).

## Findings

### F1. Dragicevic et al. 2011: slow-in/slow-out helps tracking; no threshold

- Source: Dragicevic, Bezerianos, Javed, Elmqvist, Fekete, "Temporal Distortion for Animated Transitions", CHI 2011, doi:10.1145/1978942.1979233. Full text read: https://cs.au.dk/~elm/pdf/timedistort.pdf
- Quotes:
  - Constant rate "produces high accelerations and decelerations on the first and last frames, and has a mechanical look that has been referred to as the "computer signature" [20]."
  - Figure 2 caption: "Note that all techniques except SI/SO have abrupt speed changes at the start and end."
  - Results (generated data): "Mean ERROR was lowest for SI/SO (0.28), then C (0.49), A (0.63), and FI/FO (0.65)."
  - "if the user is not expecting the animation to happen in the first place, a slow and gradual start will help the user to detect that the animation is starting and to adjust to the tracking task accordingly."
  - "Open-loop pursuit is the first visuomotor response to motion and typically lasts 100 ms; it is ballistic and thus not attuned to the velocity or direction of the visual stimulus." "a slow and gradual start of an animated motion will help mitigate any inaccuracies caused by the ballistic behavior of the first open-loop response."
  - Proposed but not tested: "(P3): keep velocity variations as low as possible".
- The four curves tested, as first-frame share of top speed (my calculation, 60 frames, 1 s): SI/SO quadratic about 0.02; constant 1.0; fast-in/fast-out ((2t)^0.75/2) above 1 (its first frame is its fastest). So the study compares only "near 0" with "1 or more".
- Implication for JOLT_RATIO: it supports the rule (a start near 0 is better than a start at 1.0 for tracking). It gives a mechanism: the eye's first 100 ms of pursuit is ballistic. That points to a parameter in absolute units (how far, in degrees, the object goes in the first ~100 ms, before the eye locks on), not a share of top speed.
- Confidence: high on the quotes (full text). The mechanism is the authors' speculation, not their measurement.

### F2. Dzhafarov, Sekuler & Allik 1993: a speed change is detected as the onset of |V1 - V0|; no "abrupt" line

- Source: Dzhafarov, Sekuler, Allik, "Detection of changes in speed and direction of motion: Reaction time analysis", Perception & Psychophysics 54(6):733-750, 1993, doi:10.3758/BF03211798. Full text read (author copy): https://peeps.unet.brandeis.edu/~sekuler/papers/dzhafarovSekuler.pdf
- Quotes:
  - "in the range of speeds used, 0-16 deg/sec (dps), the mean reaction time (MRT) for a given value of V0 depended on |V1 - V0| only: MRT = r + c(V0)/|V1 - V0|^β, where β = 2/3 ... c(V0) is a parameter whose value is constant for low values of V0 (0-4 dps), and increases beginning with some value of V0 between 4 and 8 dps."
  - "By means of a "subtractive normalization," the visual system effectively reduces the detection of velocity changes (a change from V0 to V1) to the detection of motion onset (a change from 0 to V1 - V0)."
  - Fit (Figure 3): "r = 197 msec, c(0) = c(1) = c(2) = c(4) = 0.115, c(8) = 0.187, c(16) = 0.287 (sec^1/3 deg^2/3)". Refit of Hohnsbein & Mateeff 1992 (Figure 11): "r = 231 msec, c(0) = ... = c(2) = 0.082".
  - The stimulus was a step: "constant for a random period and then switched abruptly to another value". Speeds 1, 2, 4, 8, 16 dps; random-dot field.
- What it implies:
  - The visual system reacts to the size of a velocity step in absolute units (deg/s), the same way for an onset from rest and for a step inside a move (for V0 up to 4 deg/s). It does not react to the step as a share of a later top speed.
  - The paper measures how fast a step is detected. It does not measure whether a step looks "abrupt" or "smooth" compared with a ramp. So it gives no JOLT_RATIO value.
  - Worked example (my arithmetic, from the fit): the extra reaction time c/|ΔV|^(2/3) is 115 ms at 1 deg/s, 46 ms at 4 deg/s, 18 ms at 16 deg/s. A larger first-frame step is detected sooner. There is no knee in this curve, so no natural threshold.
- Confidence: high (full text).

### F3. Runeson 1974: a start at constant speed looks fast, then seems to slow; a "natural start" is needed to look even

- Source: Runeson, S., "Constant velocity - not perceived as such", Psychological Research 37:3-23, 1974, doi:10.1007/BF00309076. Abstract only (through search snippets; Springer blocked my fetch). Formula of his "natural motion" (NM) function: not found.
- Abstract wording (as quoted by search, matches the Springer abstract): objects moving with constant velocity "appear to move fast in the beginning and suddenly slow down to a much lower velocity". "To be seen as constant, a movement must start smoothly with a certain acceleration and later level off to a constant velocity (natural motion)." "The results are taken to imply the existence of a perceptual concept of velocity which includes or presupposes a natural start."
- Secondary confirmation, full text read: La Scaleia, Zago, Moscatelli, Lacquaniti, Viviani, "Implied Dynamics Biases the Visual Perception of Velocity", PLoS ONE 9(3):e93020, 2014, doi:10.1371/journal.pone.0093020: a constant-velocity spot is "perceived as moving fast upon entering the visual field and then decelerating to a constant velocity"; Runeson showed "the motion is perceived as uniform when the velocity is mildly increasing at the onset and then levels off"; "to be seen as constant, a uni-directional motion must be mildly accelerated at the onset".
- Related, abstract only: Tayama, "The spatial and temporal conditions for perceiving velocity as constant", Perception 33(4):495-506, 2004, doi:10.1068/p5072: "At the beginning of each stimulus presentation, a moving pattern was perceived as stationary until a critical time had passed"; "Beyond the critical moving distance, velocity was perceived as constant." (Low speeds, gratings.)
- Implication for JOLT_RATIO: this is the nearest theory to the founder's complaint. A start at full speed (share 1.0) is seen as wrong (fast, then a slow-down that is not in the stimulus). A "mild" acceleration at onset removes it. The amount of acceleration (the NM time constant) is in the 1974 full text, which I could not read. So: it supports a rule, and it says the rule is about the first part of the move (an onset ramp of some duration), not one frame.
- Confidence: medium. The claim is consistent in two sources; the numbers are not reached.

### F4. Acceleration detection thresholds: a velocity change of about 20-25 % across the viewing interval

- Brouwer, Brenner, Smeets, "Perception of acceleration with short presentation times: Can acceleration be used in interception?", Perception & Psychophysics 64(7):1160-1168, 2002, doi:10.3758/BF03194764. Abstract only (VU portal summary). Subjects judged which of two dots accelerated; "Most subjects showed a detection threshold even at 300 ms"; observers seem to detect an overall change in velocity across the display, not acceleration itself; about a 25 % change was needed.
- Zaal, Bongers, Pepping, Bootsma, "Base on balls for the Chapman strategy: Reassessing Brouwer, Brenner, and Smeets (2002)", Attention, Perception & Psychophysics, 2012, doi:10.3758/s13414-012-0328-6, PMC3447139 (full text read through a fetch summary): "The threshold used by Brouwer et al. (2002) was 0.25"; "Brouwer et al. (2002) assumed that optical acceleration is detected as a velocity ratio"; Babler & Dannemiller (1993) "considered stimuli of longer durations and had arrived at a threshold value of 0.20", where the velocity ratio is "the change in (optical) velocity over the stimulus interval divided by the average"; thresholds "do vary as a function of stimulus presentation duration and average velocity".
- Implication: these thresholds apply to a move that is already in motion (the ratio is against the mean speed). For a start from rest the ratio is undefined (any start from 0 is an infinite change). So they do not give JOLT_RATIO directly. They give a scale for how much speed change people notice over a few hundred ms: about 20-25 % of the mean.

### F5. The visual system integrates velocity over 100-140 ms (Werkhoven et al. 1992); speed needs about 100 ms to resolve (Snowden & Braddick 1991)

- Werkhoven, Snippe, Toet, "Visual processing of optic acceleration", Vision Research 32(12):2313-2329, 1992, doi:10.1016/0042-6989(92)90095-Z. Abstract read (PubMed 1288008):
  - "human detection of velocity vector modulations is not directly based on the acceleration signal".
  - "A functional description of the first stage is a second order low-pass temporal filter having a characteristic time constant of 40 msec. In effect, the temporal low-pass filter is an integration of the velocity vector modulation within a temporal window of 100-140 msec."
  - "The threshold standard deviations for this variance detection stage are estimated to be 17% for speed modulations and 9% for motion direction modulations."
- Snowden & Braddick, "The temporal integration and resolution of velocity signals", Vision Research 31(5):907-914, 1991, doi:10.1016/0042-6989(91)90156-Y. Abstract read (PubMed 2035273): speed discrimination thresholds "fell asymptotically to a Weber fraction around 0.06 over a period of approx. 100 msec"; to tell a pattern modulated between two speeds from a constant one, "the minimum depth of the modulation ... was found to be equivalent to a Weber fraction of 0.3 at low modulation rates".
- Calderone & Kaiser, "Visual acceleration detection: effect of sign and motion orientation", Perception & Psychophysics 45(5):391-394, 1989, doi:10.3758/BF03210711 (abstract): at 0.7-1.7 deg/s, "Thresholds, expressed as the proportion of velocity change, did not differ significantly among the average velocities; thus, a consistent Weber-like fraction is suggested".
- Babler & Dannemiller, J Exp Psychol HPP 19(1):15-31, 1993, doi:10.1037/0096-1523.19.1.15 (abstract): "Detection of acceleration required a total change in velocity that was about 20% of the average velocity."
- Hohnsbein & Mateeff, "The time it takes to detect changes in speed and direction of visual motion", Vision Research 38(17):2569-2573, 1998, doi:10.1016/S0042-6989(98)00014-5 (abstract): "the detection time was a function of (V1-V0) almost independent of the value of V0. This finding supports the hypothesis of Dzhafarov et al."; "The time to detect an abrupt cessation of motion was equal to the time for detection of an increase in speed by a factor of two."
- Implication for JOLT_RATIO (important): one frame at 60 fps is 16.7 ms. This is far shorter than the 100-140 ms window in which the eye-brain system pools velocity. So the speed of the first frame alone is not a quantity the viewer sees. A line that a viewer can see must be stated over a window of about 100 ms (about 6 frames at 60 fps), not over one frame.
- Confidence: high for the quotes (abstracts, which state the numbers). The extension from periodic modulation (their stimulus) to a start from rest is my inference, not their test.

### F6. Material Design practice: "full velocity" starts are for elements that come from off-screen; on-screen starts from rest use the standard curve

- Material Design (2016), "Duration and easing", archived https://web.archive.org/web/2016id_/https://material.google.com/motion/duration-easing.html (full page read):
  - "Acceleration and deceleration changes should be smooth across the duration of an animation so that movement doesn't appear mechanical."
  - "Deceleration curve ("Easing out") Objects enter the screen at full velocity from off-screen and slowly decelerate to a resting point."
  - "Standard curve ... Objects quickly accelerate and slowly decelerate between on-screen locations."
- Material Design 2 (2019), "Speed", archived https://web.archive.org/web/2019id_/https://material.io/design/motion/speed.html (full page read):
  - "Elements that begin and end at rest use standard easing. They speed up quickly and slow down gradually, in order to emphasize the end of the transition." CSS "cubic-bezier(0.4, 0.0, 0.2, 1)".
  - "Incoming elements are animated using deceleration easing, which starts a transition at peak velocity (the fastest point of an element's movement) and ends at rest." CSS "cubic-bezier(0.0, 0.0, 0.2, 1)".
- Material 3 tokens (material-components-android docs/theming/Motion.md, read): standard decelerate `cubic-bezier: 0, 0, 0, 1` "for utitlity focused animations that enter the screen"; emphasized decelerate `0.05, 0.7, 0.1, 1` "for common, M3-styled animations that enter the screen".
- Implication: Material's own logic agrees with the jolt rule for a start that the viewer sees: an element at rest on screen starts slow. A full-speed start is for an element whose start is off-screen, so the viewer never sees the step from 0. This gives a principled scope condition: the rule should apply when the start position is visible, not when the element enters from outside the frame (or, by extension, from behind a mask or at opacity 0). Material never states how slow "slow" must be.
- Confidence: high (primary pages, archived).

### F7. My calculation: the first-frame share of standard curves at 60 fps, and its dependence on duration

Script: `shares.py` (#221, derivation scripts comment) (cubic-bezier evaluated per frame; share = first frame's displacement / largest frame displacement, as check-flow.py measures it). The table gives the first-frame share; the 1000 ms column came from an earlier run of the same script with that duration in its list.

| curve | 100 ms | 150 ms | 250 ms | 300 ms | 500 ms | 1000 ms |
|---|---|---|---|---|---|---|
| linear | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| CSS `ease` (0.25,0.1,0.25,1) | 0.62 | 0.48 | 0.34 | 0.31 | 0.25 | 0.21 |
| CSS `ease-in-out` | 0.21 | 0.13 | 0.08 | 0.06 | 0.04 | 0.02 |
| M2 standard (0.4,0,0.2,1) | 0.23 | 0.12 | 0.06 | 0.05 | 0.03 | 0.01 |
| M3 standard (0.2,0,0,1) | 1.00 | 0.57 | 0.25 | 0.18 | 0.09 | 0.04 |
| CSS `ease-out`, all decelerate curves | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

- At JOLT_RATIO 0.5, the M3 standard curve (Material's curve for a move that begins and ends on screen) is a jolt at 150 ms and below, and CSS `ease` is a jolt at 100 ms; both pass at 250 ms.
- Every pure "ease-out" (initial slope above 0) gives 1.00 at every duration. Every curve with initial slope 0 falls under 0.5 once it is long enough. So in practice the 0.5 line separates "initial slope 0" from "initial slope above 0", except for short moves. Any line between about 0.35 and 0.95 gives the same verdicts on these curves at 250 ms and more (CSS `ease` at 250 ms is 0.34). The exact value matters only for short moves and for hand-made or spring curves.

### F8. Apple practice: continuous position AND velocity; from rest, velocity starts at 0

- Apple, WWDC23 session 10158 "Animate with springs", transcript read at https://developer.apple.com/videos/play/wwdc2023/10158/ :
  - "So one goal we have is to make our animations have continuous position and velocity."
  - "If we look at the motion of a linear animation instead, there's a sharp corner and a jump in velocity as the animation starts and ends."
  - "Remember that for this base case, we need to preserve a velocity of 0 at the beginning. So the velocity of the product of our two component curves should be flat around 0."
  - "A spring can start with any initial velocity, so we get a natural feeling where our animation picks up right where the gesture ends."
  - "There's no single point when the object is abruptly done."
- Apple, WWDC18 session 803 "Designing Fluid Interfaces" (transcript read): no rule on start velocity. It says "the system is preserving all your energy and momentum, and gracefully transferring it into the interface", and recommends "starting with 100% damping".
- My calculation (`spring.py` (#221, derivation scripts comment)), a critically damped spring from rest, x(t) = 1 - (1 + ωt)e^(-ωt), ω = 2π/response:

| response | first-frame share at 60 fps | top speed reached at |
|---|---|---|
| 0.2 s | 0.53 | about 32 ms |
| 0.3 s | 0.38 | about 48 ms |
| 0.5 s | 0.25 | about 80 ms |
| 1.0 s | 0.13 | about 160 ms |

- Implication: Apple gives a principled rule that is not a share: **velocity must be continuous**. From rest, the start velocity is 0; after a gesture or an interrupted move, the start velocity equals the velocity just before. A velocity jump at the start is the fault, whatever its size. This is the same rule as Lasseter's "second-order continuity" (audit §1.6). But Apple's own velocity-continuous springs reach top speed in 30-80 ms, which is inside the 100-140 ms window where the eye pools velocity (F5). So "continuous" in the mathematics does not by itself mean "looks smooth". A stiff spring (response 0.2 s) gives 0.53 at frame 1 and fails JOLT_RATIO 0.5 though its velocity is continuous. The checker cannot see continuity at one frame: at 60 fps, every start has a jump from 0 to the first frame's mean speed.
- Confidence: high on the quotes (primary transcript).

### F9. Cook, Saygin, Swain & Blakemore 2009: a measured threshold for "less natural" when constant velocity is mixed into a smooth-start profile (the closest data found)

- Source: Cook, Saygin, Swain, Blakemore, "Reduced sensitivity to minimum-jerk biological motion in autism spectrum conditions", Neuropsychologia 47(14):3275-3278, 2009, doi:10.1016/j.neuropsychologia.2009.07.010. Full text read: https://pmc.ncbi.nlm.nih.gov/articles/PMC2779370/
- Method quotes:
  - "The velocity profile of the movement was varied between 100% natural motion (minimum-jerk (MJ) for the hand; gravitational (G) for the ball) and 100% constant velocity (CV). Participants were asked to judge which animation was 'less natural' in a two-interval forced-choice paradigm".
  - Hand: "a vertical sinusoidal movement of amplitude 110 mm and frequency 0.5 Hz". Ball: "a vertical downward movement of amplitude 215 mm and frequency 1 Hz. Thus, the tennis ball appeared from the top of the screen and finished off the bottom of the screen."
  - "Motion morph = p1 (Prototype 1) + p2 (Prototype 2)". "The reference animation was always a combination of 85% natural motion and 15% CV". Three-down one-up staircase, "targets the 79.4% correct point".
- Result quotes: "mean MJ thresholds for NC: 0.29 ± 0.02"; "mean G thresholds for NC: 0.48 ± 0.05" (NC = control group, N = 16). "The NC group exhibited mean thresholds for MJ motion of 30%, indicating that, on average, 70% of the velocity profile must be MJ for the target to be discriminated as 'less natural' than the reference (which contained 85% MJ)."
- Derivation (mine; script `cook.py` (#221, derivation scripts comment)). Both natural prototypes start at speed 0; the CV prototype starts at its full speed. So a morph with CV weight c starts at speed c (in units of the mean speed), and its top speed is (1 - c) x peak + c, where peak = 1.875 for minimum jerk and 2 for free fall. Start share s = c / ((1 - c) x peak + c). I checked this against a 60 fps frame sampling of the hand morph; it agrees to 0.001.

| condition | reference (c = 0.15) start share | threshold start share (79 % correct) |
|---|---|---|
| hand, minimum jerk (c = 0.29) | 0.09 | 0.18 |
| ball, free fall (c = 0.48) | 0.08 | 0.32 |

- What it implies: when viewers compare a smooth-start move (share about 0.09) with one that has more constant velocity mixed in, they reliably call the second one "less natural" once its start share reaches about 0.18 (a hand) to 0.32 (a ball). If the same step size holds from a true zero start, a share of about 0.1-0.25 above a smooth start is noticeable. That is below the current 0.5.
- Assumptions and limits (important):
  1. Viewers judged the whole move, not only the start. The CV mix also flattens the mid-move speed peak and, for the hand, adds a direction reversal at each turn with a velocity jump of 2c. I cannot separate how much of the threshold came from the start.
  2. "Detectably less natural" (79 % in a forced choice) is not the same as "looks like a jolt". A noticeable difference can still look acceptable.
  3. One study, N = 16 controls, 1 s half-cycles, 110-215 mm on an unstated screen at an unstated distance. Not replicated for onsets.
  4. The ball "appeared from the top of the screen", so its start may have been at or above the screen edge. Then its onset was partly not visible.
- Confidence: high on the quoted numbers (full text); low-to-medium on the share translation as a jolt line.

### F10. Attention capture: a smooth constant-speed start (share 1.0) did not capture attention; a jump of 0.26-1.05 deg did

- Abrams & Christ, "Motion onset captures attention", Psychological Science 14(5):427-432, 2003, doi:10.1111/1467-9280.01458 (abstract, PubMed 12930472): "motion per se does not automatically attract attention. We show here, however, that the onset of motion does indeed attract attention." Their motion was refreshed at 15 Hz (per Sunny & von Mühlenen 2011, below).
- Sunny & von Mühlenen, "Motion onset does not capture attention when subsequent motion is "smooth"", Psychonomic Bulletin & Review 18(6):1050-1056, 2011, doi:10.3758/s13423-011-0152-3. Full text read (author copy): https://wrap.warwick.ac.uk/39951/1/WRAP_SunnyvonMuhlenen.pdf
  - Stimulus: letters "moving on a circular path (radius = 1.3°) at a constant speed of 8.7°/s"; "a 100-Hz stimulus was updated every 10 ms (displaced by 0.09°), producing the impression of smooth motion, whereas an 8-Hz stimulus was updated every 120 ms (displaced by 1.05°)". Motion started at full speed (a constant-speed start, share 1.0).
  - "When motion is smooth, neither the onset of motion nor continuous motion capture attention. However, when motion is jerky, the onset of motion (but not continuous motion) appears to capture attention." Smooth = 100 and 33 Hz (0.09° and 0.26° per update); jerky = 17 and 8 Hz (0.52° and 1.05° per update).
- Sunny & von Mühlenen, "The role of flicker and abrupt displacement in attention capture by motion onsets", Attention, Perception & Psychophysics 76(2):508-518, 2014, doi:10.3758/s13414-013-0587-x (abstract, PubMed 24264514): "An abrupt displacement between 0.26° and 1.05° captured attention, irrespective of whether the stimulus subsequently continued to move smoothly (Exp. 2) or whether it remained stationary".
- Implication: by the measure of attention capture (one objective sign of "sudden"), a start at full speed (8.7 deg/s, share 1.0) is not sudden when each frame step is small (0.09 deg). What made a start sudden was a spatial jump per update of about 0.26 deg or more (0.5 deg or more in the 2011 design). That points to an absolute per-frame displacement (deg per frame) as a parameter, not a share of top speed. Conversion at 60 cm and 96 CSS px/inch: 1 deg is about 1.05 cm, about 40 CSS px; 0.26 deg is about 10 px in one frame (about 620 px/s at 60 fps); 8.7 deg/s is about 345 px/s.
- Limits: attention capture is not the same as "looks janky". Both studies used small letters at 12.5 deg eccentricity, not a large element at the fixation point. The two papers disagree at 0.26 deg (no capture in 2011 at 33 Hz; capture in 2014 Exp. 2).
- Confidence: high on quotes (2011 full text, 2014 abstract).

### F11. Causal and animacy perception: what a sudden start means to a viewer; no share line

- Tremoulet & Feldman, "Perception of animacy from the motion of a single object", Perception 29(8):943-951, 2000, doi:10.1068/p3101 (abstract, PubMed 11145086): "Naive subjects' ratings of animacy were significantly influenced by (i) the magnitude of the speed change, (ii) the angular magnitude of the direction change ..."; "observers classify as animate only those objects whose motion trajectories are otherwise unlikely to occur in the observed setting."
- Gyulai, "Considerations on perception of "animacy" in the motion of a single object", Perceptual and Motor Skills 99(3):1014-1026, 2004, doi:10.2466/pms.99.3.1014-1026 (abstract): a pilot study of "introduction of a sudden stop or of a pause" and "one or more sudden accelerations or decelerations"; "it is possible to distinguish between animate and inanimate motion of a single object on the basis only of the kinetic conditions."
- Michotte (1946/1963), through search summaries only (secondary, not verified): the launching impression is strongest when the launched object moves slower than the launcher; when the launched object is faster, "the launching effect gives way to the triggering effect" (it looks self-propelled).
- Implication: a start with a velocity step reads as caused by an outside push (launching, if something hits it) or as self-propelled (animacy, if nothing hits it). An inert object that starts with no visible cause and with a velocity step is "unlikely to occur in the observed setting", so it reads as alive or as wrong. This explains why a sudden start looks wrong for a brand mark and right for a hit. It gives no share number. Tremoulet & Feldman's stimuli were speed changes inside a move, not starts from rest; their speed-change values are in the full text, which I did not read.
- Confidence: medium (abstracts; Michotte secondary).

### F12. Smooth pursuit: the eye needs about 100 ms to start following; this bears on long moves only

- de Brouwer, Yuksel, Blohm, Missal, Lefèvre, "What triggers catch-up saccades during visual tracking?", J Neurophysiol 87(3):1646-1650, 2002, doi:10.1152/jn.00432.2001 (abstract): "for T(XE) between 40 and 180 ms, no saccade is triggered and target tracking remains purely smooth. Conversely, when T(XE) becomes smaller than 40 ms or larger than 180 ms, a saccade is triggered after a short latency (around 125 ms)."
- Dragicevic et al. 2011 (F1) on pursuit: "Open-loop pursuit is the first visuomotor response to motion and typically lasts 100 ms".
- Implication: a target that leaves the gaze point at speed v builds a position error of about v x 0.1 s before the eye moves at all. A large error at the start forces a catch-up saccade (a jump of the gaze), which a viewer may feel as a jolt. This depends on absolute speed (deg/s) and the time it lasts, not on a share. For short UI moves (under about 250 ms) the move ends before pursuit is under way, so this mechanism mostly does not apply. I did not find a source that turns this into an onset line, so I record it as a direction only.
- Confidence: high on the quotes; the link to "jolt" is my inference.

### F13. IBM Carbon practice: a "standard" curve for moves seen from start to end that starts above zero speed

- IBM Carbon Design System, Motion overview, https://carbondesignsystem.com/elements/motion/overview/ (page read through a fetch summary): "Strictly linear movement appears unnatural to the human eye." "Elements on the screen should speed up quickly and slow down smoothly, obeying the physics of a light-weight material." "Use `standard-easing` when an element is visible from the beginning to the end of a motion." Tokens: standard productive `cubic-bezier(0.2, 0, 0.38, 0.9)`, standard expressive `cubic-bezier(0.4, 0.14, 0.3, 1)`, entrance productive `cubic-bezier(0, 0, 0.38, 0.9)`, entrance expressive `cubic-bezier(0, 0, 0.3, 1)`. The page also asks: "Do micro-interactions use `ease-out` on user input?"
- My calculation (first-frame share at 60 fps; durations are Carbon's duration tokens as I recall them, 70/110/150/240/400/700 ms, not re-read on the page):

| curve | 70 ms | 110 ms | 150 ms | 240 ms | 400 ms | 700 ms |
|---|---|---|---|---|---|---|
| standard productive | 0.81 | 0.52 | 0.42 | 0.29 | 0.17 | 0.10 |
| standard expressive (initial slope 0.14/0.4 = 0.35 x mean speed) | 0.53 | 0.32 | 0.29 | 0.23 | 0.20 | 0.18 |
| entrance (both) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

- Implication: Carbon's expressive standard curve, made for an element "visible from the beginning to the end", starts on purpose at a non-zero speed: about 0.2-0.3 of its top at 60 fps. So one major design system accepts a start share near 0.2-0.3 for an on-screen start, and uses a full-speed start ("ease-out") for entrances and for a response to user input. This is practice, not a measurement, and Carbon gives no reason for the 0.14.
- Confidence: medium-high (primary page via summary; the share numbers are mine).

## Derivation: a line from measured thresholds (Werkhoven et al. 1992's model)

Scripts: `werkhoven.py` (#221, derivation scripts comment), `werkhoven_onset.py` (#221, derivation scripts comment) (edit the duration list to rerun at other durations).

Model (from F5, abstract values): the viewer sees speed through a second-order low-pass filter, h(t) = (t/τ²)e^(-t/τ), τ = 40 ms; a change in speed is seen when the standard deviation (SD) of the filtered speed change reaches 17 % of the mean speed.

Question put to the model: at which start share s can a viewer tell a move from the same move with a smooth start (s = 0)?

Assumptions (each one can move the answer):
1. Werkhoven's stage 2 detects modulation around a constant speed. I use it to compare two profiles (the difference between their filtered speeds). They did not test this.
2. The SD is taken over the move plus a 100 ms tail, against the move's mean speed. A shorter window for the start (for example only the first half) gives lower thresholds for long moves.
3. The 17 % is at their threshold criterion (from the abstract; I did not read the percent-correct level).
4. Base move: minimum jerk (Flash & Hogan 1985), as Cook et al. used. Two families: (a) "whole move" = Cook's morph (1 - c) x minimum jerk + c x linear; (b) "start only" = speed raised to s x peak before the peak, minimum jerk after it, rescaled to the same distance.

Results (first-frame share at 60 fps at the threshold):

| duration | (a) whole-move family | (b) start-only family |
|---|---|---|
| 150 ms | not seen, even at 1.0 | not seen, even at 1.0 |
| 200 ms | 0.80 | 0.80 |
| 250 ms | 0.54 | 0.67 |
| 300 ms | 0.43 | 0.60 |
| 500 ms | 0.27 | 0.47 |
| 1000 ms | 0.19 | 0.39 |
| 2000 ms | 0.17 | 0.35 |

Cross-check against a measurement (F9, Cook et al. 2009, 1 s moves). Ignoring the filter, the model's threshold step in CV weight is Δc = 0.17 / SD(1 - natural speed) = 0.26 for minimum jerk and 0.29 for free fall; with the filter, 0.31 for minimum jerk. Cook measured Δc = 0.33 for the ball (free fall): the model agrees within about 15 %. For the hand (minimum jerk) Cook measured Δc = 0.14, half the model's value; Cook's own reading is that people are more sensitive to biological motion. So the model is about right for a non-living object and too lax by about 2x for motion that reads as a human hand.

What the derivation says:
- **The line depends on the move's duration.** A fixed 0.5 is about right for moves of 300-500 ms (derived 0.43-0.60 for 300 ms, 0.27-0.47 for 500 ms). It is too strict for short moves: under about 200 ms the eye cannot resolve the start at all (the whole move is inside one or two 100-140 ms integration windows), so even a linear move's start cannot be told from an eased one by this measure. It is too lax for long moves: at 1-2 s the derived line is 0.17-0.39.
- **The line is a share, not an absolute speed, in this model.** Werkhoven's stage 2 is relative (17 % of mean speed), and Calderone & Kaiser (F5) found "a consistent Weber-like fraction" across 0.7-1.7 deg/s. So, for the question "does the start look less smooth than an eased start?", a share of top speed is the right kind of parameter, provided it is measured on the filtered (pooled) speed or scaled by duration, not on one raw frame.

## Verdict

**(2), weakly: no source gives the line, but one can be derived from measured thresholds, with stated assumptions; and the derived line is not a fixed share.**

1. No published research or design practice I found gives "the share of top speed at which a start from rest looks abrupt". The audit's GAP stands as a statement about direct sources. Searched and read: Dzhafarov et al. 1993 (full text), Dragicevic et al. 2011 (full text), Cook et al. 2009 (full text), Sunny & von Mühlenen 2011 (full text), Apple WWDC23 (transcript), Material 2016/2019 (archived pages), Carbon (page); abstracts of Werkhoven et al. 1992, Snowden & Braddick 1991, Brouwer et al. 2002, Babler & Dannemiller 1993, Calderone & Kaiser 1989, Hohnsbein & Mateeff 1998, Mateeff et al. 1995, Runeson 1974, Tayama 2004, Abrams & Christ 2003, Sunny & von Mühlenen 2014, Tremoulet & Feldman 2000, de Brouwer et al. 2002.
2. The nearest theory is Runeson 1974 (a constant-speed start looks fast then slowing; a "natural start" is needed). It supports the rule but its numbers are in a full text I could not reach.
3. Derived band (Werkhoven model + Cook cross-check): **about 0.4-0.6 for 300 ms moves, 0.3-0.5 for 500 ms, 0.2-0.4 for 1 s, and no visible line under about 200 ms.** Halve the long-move values for anything that reads as a living or hand-made gesture (Cook's hand result).
4. What the parameter should be, in place of a fixed first-frame share:
   - (a) For "the start looks less smooth than an eased one": a share of top speed, but measured on the speed pooled over the eye's 100-140 ms window (Werkhoven's τ = 40 ms filter), or a share line that falls with duration (the table above). One raw 16.7 ms frame is below what a viewer resolves, and its share changes with duration for the same curve (F7: M3 standard is 0.57 at 150 ms, 0.18 at 300 ms).
   - (b) For "the start is a jump": an absolute first-frame displacement, about 0.26 deg (about 10 CSS px at 60 cm) or more (Sunny & von Mühlenen), independent of the share.
   - (c) Scope: practice (Material, Carbon) and causal perception (Michotte, Tremoulet & Feldman) both exempt starts the viewer does not see from rest (entry from off-screen) and starts caused by something (a user's input, a hit). Apple's rule is velocity continuity: from rest, start at 0; after a gesture, start at the gesture's speed.
5. Gaps: Runeson's NM function parameters; Werkhoven's full text (speed range and threshold criterion); no study tests start-share directly; Cook's viewing distance and screen are not stated; whether "detectably less natural" equals the founder's "jolt" is a taste he holds. #221 set the line at the band's midpoints (0.5 at 300 ms, 0.37 at 500 ms, 0.29 at 1 s), with no viewing test. #297 builds 4(a), 4(b), and 4(c) for a brand move that enters from outside the frame; 4(c) for interface motion is #196's Q3 (B) ruling.
