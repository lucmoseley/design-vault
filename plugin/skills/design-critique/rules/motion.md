# Rule records: motion

Animation: brand motion's pace, length and end frame, and pausing motion that starts by itself. The form is [rules.md](../rules.md)'s.

### vault.flow-script
- applies-when: has-brand-motion; every brand move
- question: Does the motion run with no pause over 250 ms after its first move that the motion brief does not name as a hold; no move from rest, seen at rest, that starts or stops at its jolt line or faster, a share of its top speed that falls as the move lengthens (about 0.5 at 300 ms, 0.37 at 500 ms, 0.29 at 1 s, none under 200 ms), save a landing the motion brief names as a thud or, where it names no landing, any thud, put to the founder as a question and never failed; no move from rest, seen at rest, whose first frame jumps 0.26° of visual angle or more (about 10 px at 60 cm); and no speed step in the middle of a move (a steady speed that suddenly runs 1.3 times as fast or more, or about three quarters as fast or less)?
- answered-by: script
- writes: pace
- yields-to: level 2
- source: the rule is the founder's, lucmoseley/mmm-infra#9 ("long pauses interspersed with rapid jolts"); the 250 ms pause is an agent's working figure, accepted with the other recommendations on lucmoseley/mmm-infra#16; a still before the first move is no pause (docs/research/house-audit-craft.md §1.5, design-vault#220); the jolt line is the middle of docs/research/jolt-onset.md's derived band, set without a look test, design-vault#221 Q1 (B); the 0.26° jump is the lower end of the jumps that drew attention in Sunny and von Mühlenen 2014, though not in their 2011 study (docs/research/jolt-onset.md F10); a start or stop the viewer never sees at rest, outside the viewport, clipped or transparent, is not judged (design-vault#297; docs/research/jolt-onset.md F6, F13); the founder ruled ease-out entrances still count as jolts, design-vault#60 option (A), which design-vault#183 Q3 (B) narrowed to brand motion; the thud is the brief's pick, design-vault#183 Q4 (A); the 1.3× step is the top of the 0.2–0.3 Weber fraction at which a change of speed inside one motion is seen (Snowden and Braddick 1991, Mateeff et al. 2000, abstracts only), design-vault#196; strength: founder ruling for the rule and the two rulings, research for the step and the jolt band, research that disagrees at its size for the jump, an accepted agent recommendation for the point in the band, accepted agent figures for its other numbers
- era: timeless
- owner: vault
- stage: value
- script: check-flow.py
- reasons: design-round/SKILL.md#brand-motion-easing
- ledger: none
- status: live

### vault.flow-code
- applies-when: has-brand-motion; every brand move in the timeline table
- question: Does the timeline table hold none of the faults `vault.flow-script` names, and is every fall or throw on it ballistic, y = ½gt² at one stated pixels-per-metre scale, leaving with the speed it had, ending in a thud, stopping where it hits, or a critically or highly damped spring that carries on at its impact speed, whichever the motion brief picks, or either where it picks none, left for the founder to choose?
- answered-by: code
- writes: pace
- yields-to: vault.flow-script, vault.fall-script, level 2
- source: the gravity rule is the founder's own words, lucmoseley/mmm-infra#9 ("water flow should match a gravitational calculation if falling"); the timeline table and one stated pixels-per-metre scale are an agent's procedure, accepted on lucmoseley/mmm-infra#16; the damped landing is an agent's recommendation, accepted on lucmoseley/mmm-infra#28, and the thud beside it is the brief's pick, design-vault#183 Q4 (A); strength: founder ruling for the rule, accepted agent recommendations for the procedure and the landing
- era: timeless
- owner: vault
- stage: treatment
- target: Write every brand move into the timeline table, and compute each fall or throw from gravity at one stated pixels-per-metre scale, landing as the motion brief picks.
- reasons: design-round/SKILL.md#brand-motion-easing
- ledger: MOT-28, MOT-29, MOT-103
- status: live

### vault.fall-script
- applies-when: has-brand-motion; every fall in the timeline table
- question: Recomputed from the arguments its easing names, does every fall in the timeline table match: a spring sink the exact `linear()` easing fall.js prints for them, a thud the t² curve over √(2 · drop / g) at its stated scale, every cue on it lasting that long to the table's 1 ms, and each landing the form the motion brief picks, with either passing, listed for the founder, where it picks none?
- answered-by: script
- writes: pace
- yields-to: vault.flow-script, level 2
- source: the gravity rule is the founder's own words, lucmoseley/mmm-infra#9 ("water flow should match a gravitational calculation if falling"); recomputing the table's falls is the spec's procedure, design-vault#324 §Fall comparison; the landing is the brief's pick, design-vault#183 Q4 (A); strength: founder ruling for the rule and the landing, an agent's procedure for the recomputation
- era: timeless
- owner: vault
- stage: value
- script: fall.js --check
- reasons: design-round/SKILL.md#brand-motion-easing
- ledger: none
- status: live

### vault.flow-look
- applies-when: has-brand-motion; the whole brand motion, scrubbed at 0.25× speed
- question: Does the motion flow at one continuous pace, or change speed only with what is happening, never long pauses between sudden jolts?
- answered-by: look
- writes: pace
- yields-to: vault.flow-script, vault.flow-code, vault.fall-script, level 2
- source: the rule is close to the founder's own words, lucmoseley/mmm-infra#9 ("one continuous animation of uniform speed, or with speed-ups and slow-downs that feel natural"); the 0.25× scrub is an agent's procedure, accepted on lucmoseley/mmm-infra#16; strength: founder ruling for the rule, an accepted agent procedure for the scrub
- era: timeless
- owner: vault
- stage: treatment
- target: Keep brand motion at one continuous pace, its speed changing only with what happens.
- reasons: design-round/SKILL.md#brand-motion-easing
- ledger: none
- status: live

### vault.length-range
- applies-when: has-brand-motion; the motion brief
- question: Does the motion brief give a length range, with a research source for the asset's placement and audience?
- answered-by: code
- writes: length
- yields-to: level 2
- source: the founder's own words, lucmoseley/mmm-infra#9, with no number; strength: founder ruling
- era: timeless
- owner: vault
- stage: function
- target: Give the motion brief a length range, cited from research for the asset's placement and audience.
- reasons: design-round/SKILL.md#6-per-asset-class
- ledger: none
- status: live

### vault.length
- applies-when: has-brand-motion; the whole brand motion
- question: Does the motion, timed from its first move to its last, run for a length inside the brief's range?
- answered-by: script
- writes: length
- yields-to: vault.length-range, level 2
- source: the founder's own words, lucmoseley/mmm-infra#9, with the range the brief sets; timed from the first move, so a wait before it is vault.load's, by his ruling on design-vault#169 Q3 (A); strength: founder ruling
- era: timeless
- owner: vault
- stage: value
- script: check-flow.py, its length line; for a generated clip, check-clip.py --range
- reasons: design-round/SKILL.md#6-per-asset-class
- ledger: none
- status: live

### vault.clip-loop
- applies-when: motion and has-motion and has-brand-motion; every generated clip
- question: Did the clip's logged request send one still as both its start frame and its end frame?
- answered-by: script
- writes: loop
- yields-to: level 2
- source: the #262 ruling that a script checks a looping clip's request, since no tool the house may ship decodes its frames (spec #324, user story 10, so a loop never asked for is caught before the render is judged); each model's start and end fields are its Higgsfield request schema, cited beside them in loop-fields.json; strength: house ruling for the rule, vendor docs for each field
- era: timeless
- owner: vault
- stage: value
- script: check-clip.py
- reasons: design-round/references/prompts.md#video--image-to-video
- ledger: none
- status: live

### vault.end-frame
- applies-when: has-brand-motion; a brand motion that builds a finished asset
- question: Is the last frame the asset's own end frame, pixel for pixel, never the finished asset laid over the pieces that built it?
- answered-by: script
- writes: end frame
- yields-to: level 2
- source: ending on the logo is the client's brief and the founder's rounds (lucmoseley/mmm-infra#9); "pixel for pixel" is an agent's recommendation, accepted with every recommendation on lucmoseley/mmm-infra#28; strength: accepted agent recommendation
- era: timeless
- owner: vault
- stage: value
- script: check-frames.py last
- reasons: design-round/SKILL.md#6-per-asset-class
- ledger: none
- status: live

### vault.pause
- applies-when: web-surface or has-motion-over-5s; every motion that starts by itself and runs more than 5 s beside other content: an animation, a video, a canvas, and a motion asset on the page it is set into
- question: Does a control on the page pause, stop or hide every motion that starts by itself and runs more than 5 s?
- answered-by: script
- writes: motion control
- yields-to: none
- source: WCAG 2.2 success criterion 2.2.2 Pause, Stop, Hide; the motion-asset scope is the design-vault#169 trial's finding (design-vault#170); strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Give every motion that starts by itself and runs past 5 s a control that pauses, stops or hides it.
- script: check-access.py <page> --out <dir>
- reasons: design-round/references/impeccable.md#struck-or-corrected
- ledger: IMG-156, MOT-4, MOT-97, MOT-99, NAV-83, NEW2-16, NEW2-71
- status: live

### vault.motion-duration
- applies-when: web-surface and has-motion; every interface transition and animation
- question: Does each interface move last 100–500 ms, longer only for an authored focal entrance, with exits faster than entrances?
- answered-by: whole-page
- writes: duration
- yields-to: level 2
- source: NN/g 2020, "Executing UX Animations: Duration and Motion Characteristics"; strength: domain evidence
- era: timeless
- owner: vault
- stage: value
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: MOT-12, MOT-16, MOT-18, MOT-28, MOT-61
- status: live

### vault.motion-easing
- applies-when: web-surface and has-motion; every interface move that enters or settles
- question: Does each interface move that enters or settles use a decelerating curve?
- answered-by: whole-page
- writes: easing
- yields-to: level 2
- source: Material 3 easing and duration tokens; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Ease entrances and settles out (fast start, slow end).
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: MOT-24, MOT-25, MOT-28, MOT-61
- status: live

### vault.reduced-motion
- applies-when: web-surface and has-motion; every animation the page runs
- question: Under `prefers-reduced-motion: reduce`, does the page show a designed reduced version of each animation, keeping its meaning without the movement?
- answered-by: whole-page
- writes: reduced motion
- yields-to: level 2
- source: WCAG 2.2 SC 2.3.3 Animation from Interactions (AAA) and technique C39; strength: design-system guidance over WCAG 2.2 AAA
- era: timeless
- owner: vault
- stage: treatment
- target: Design a reduced-motion version of every animation, a fade or an instant change that keeps its meaning, under `prefers-reduced-motion`.
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: MOT-1, MOT-2
- status: live

### vault.motion-properties
- applies-when: web-surface and has-motion; every interface animation
- question: Does every interface animation move transform and opacity, leaving layout properties (width, height, top, left, margin, padding) unanimated save where the layout change is the point?
- answered-by: whole-page
- writes: animated property
- yields-to: level 2
- source: web.dev, rendering performance; strength: platform guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Animate transform and opacity; animate a layout property only where the layout change is the point.
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: LAY-101, MOT-34, MOT-62, MOT-63, MOT-64
- status: live

### vault.parallax
- applies-when: web-surface and has-motion; every part that moves at a different rate from the page as it scrolls
- question: Is any parallax confined to background or peripheral images, never moving text or a part the visitor's task needs, and does each effect rest at its end position rather than replaying when the visitor scrolls back?
- answered-by: script
- writes: parallax
- yields-to: vault.reduced-motion
- source: W3C Understanding SC 2.3.3 Animation from Interactions (updated 16 Sep 2025, as read Oct 2026): "Another animation that is often non-essential is parallax scrolling", and "Vestibular (inner ear) disorder reactions include dizziness, nausea and headaches"; NN/g, Sherwin, "Parallax Scrolling" usability (20 Jan 2019): "Save parallax effects for background or peripheral images", "leave those objects in their final positions", and "Too much movement, especially of text, can be dizzying"; strength: domain evidence
- era: timeless
- owner: vault
- stage: treatment
- target: Use parallax only on a background or edge image, never on text or a control; let each effect run once and rest; give it the reduced-motion version vault.reduced-motion asks for.
- parts: hero, image
- script: check-flow.py <page> --out <dir> --records [--parts <declaration>]
- reasons: design-critique/references/page-behaviour.md#parallax
- ledger: MOT-73
- status: staged

### vault.carousel-timing
- applies-when: web-surface and has-motion; every carousel that advances by itself
- question: Does the carousel not advance by itself at phone width, and on wider screens hold each frame at least as long as the output gives, pause while hovered or focused, and stop for good once the visitor changes frame?
- answered-by: script
- writes: carousel frame duration
- yields-to: none
- source: Baymard, Scott, "Homepage Carousels" (updated 3 Apr 2025, as read Oct 2026): autorotation "avoided on mobile sites", "5–7 seconds for slides with just a header and a few tags and labels", text-heavy slides "as much as 10 seconds", "paused on hover", stopped once the user changes slides; NN/g, Pernice, "Designing Effective Carousels" (reviewed 7 Aug 2026): "Do not auto-forward on mobile devices", "3 words per second as a guideline"; strength: domain evidence
- era: timeless
- owner: vault
- stage: value
- inputs: the viewport width (phone or wider), the frame's visible word count
- output: phone width: no auto-advance; wider: each frame shown max(5, ⌈words ÷ 3⌉) s, so a headline frame 5 s and a 30-word frame 10 s
- script: check-flow.py <page> --out <dir> --records [--parts <declaration>]
- reasons: design-critique/references/page-behaviour.md#carousels
- ledger: MOT-98
- status: staged

### vault.motion-frequency
- applies-when: web-surface and has-motion; every part that moves, by how often a visitor meets it
- question: Does the motion each link, button and menu item starts when hovered or pressed end in under 150 ms, or is there none?
- answered-by: script
- writes: motion length on frequent states
- yields-to: vault.motion-duration, level 2
- source: Atlassian Design System, Motion, "Tone down motion for frequent experiences": "If someone will trigger this motion dozens of times a day, keep it under 150ms"; IBM Carbon, Motion: "Reserve expressive motion for occasional, important moments"; Rauno Freiberg, "Interaction Design" (Jul 2023), Frequency & Novelty: a command menu's fade seen "hundreds of times a day" becomes "cognitive burden" (all as read Oct 2026); strength: design-system guidance and practitioner writing
- era: timeless
- owner: vault
- stage: treatment
- target: Keep each link's, button's and menu item's hover and press motion under 150 ms, or drop it.
- script: check-flow.py <page> --out <dir> --records [--parts <declaration>]
- reasons: design-critique/references/house-principles.md#expression-by-frequency
- ledger: MOT-10
- status: staged

### vault.motion-frequency-look
- applies-when: web-surface and has-motion; every part that moves, by how often a visitor meets it
- question: Is longer, expressive motion kept for rare moments (a first run, a finished booking, a milestone), and does a list item, or a menu or command palette opened from the keyboard, open under 150 ms or with none?
- answered-by: look
- writes: motion amount by frequency
- yields-to: vault.motion-frequency, vault.motion-duration, level 2
- source: Atlassian Design System, Motion, "Tone down motion for frequent experiences": "If someone will trigger this motion dozens of times a day, keep it under 150ms"; IBM Carbon, Motion: "Reserve expressive motion for occasional, important moments"; Rauno Freiberg, "Interaction Design" (Jul 2023), Frequency & Novelty: a command menu's fade seen "hundreds of times a day" becomes "cognitive burden" (all as read Oct 2026); strength: design-system guidance and practitioner writing
- era: timeless
- owner: vault
- stage: treatment
- target: Spend longer, expressive motion only on rare moments, and open a list item, menu or command palette under 150 ms or with none.
- reasons: design-critique/references/house-principles.md#expression-by-frequency
- ledger: MOT-10
- status: staged

### vault.slow-update
- applies-when: web-surface and has-motion; every animation and transition the page runs
- question: Does each animation and transition run only under `@media (update: fast)`, so a screen that refreshes slowly (`update: slow`, an e-ink reader) or a printed page (`update: none`) shows its end state rather than a stuttering move?
- answered-by: script
- writes: motion on slow-refresh output
- yields-to: level 2
- source: W3C, Media Queries Level 4, the `update` feature (Candidate Recommendation Draft, Feb 2026): `slow` is output that cannot show changes "quickly enough for them to be perceived as a smooth animation. Example: E-ink screens"; web.dev, Learn Design, "Media features" (2025): transitions wrapped in `(update: fast)`; web-features `update`: Baseline widely available since 2026-03-18; strength: platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Put every animation and transition inside `@media (update: fast)`, so slow-refresh screens and print show only the end state.
- script: check-flow.py <page> --out <dir> --records [--parts <declaration>]
- reasons: design-critique/references/controls-and-feedback.md#motion-on-slow-screens
- ledger: MOT-112
- status: staged
