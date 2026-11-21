# design-vault #88: mmm-infra logo and animation work, misses and redone work

⚠ **Bound 13 Oct 2026 (#94): every finding here is ruled. L1 goes to #73; L3 to #79; L5 and L9 to #112; L11 and L12 to #114. L2 takes no change (#95's agreement log covers the calibration column); L4 was fixed by 5d1f926; L13 takes no change (mmm-infra#35 already binds its one case to the craft gate). L6, L7, L10 and L14 were already filed (#72, #77, #85, #73). L8, L15 and L16 are workflow-core's.**

Owner of every proposed change below: #94 (which mmm-infra findings design-vault adopts) rules on each; a finding about judging a client's photos goes to #93 (photo method).

Question: where did mmm-infra's logo and animation work miss what the founder wanted, or redo work, beyond design-vault #67–#73 and #75?
Sources: the reduced transcripts in `.claude/tmp/dbb2d38b-reduced/`, raw jsonl for drill-down, mmm-infra issues, design-vault git history of `plugin/`.
Status: complete (13 Oct 2026).

## Findings

### L1: Ten storyboard drafts drew the logo as straight-segment chains, and every check passed them
- **What happened:** Round one (8ad05cae, 4 Oct) traced the logo JPG into about 30 straight segments per curve. All five round-one drafts and all five round-two drafts (8c2c8bf9) drew from that trace. The builder's own overlay gave "mark overlap 0.90" and later 0.93. The round-one critic measured "IoU 0.96" and wrote "the end frame *is* the logo" as a strength. The round-two critic gave 21–22/28 and did not name the faceting. The founder found it at first look.
- **Founder's words:** "You've done a bad job rendering the logo in every single version. All of the "curves" have clearly disjointed corners in them, that make the whole product look like shoddy work." (8c2c8bf9 L605)
- **Evidence:** 8ad05cae L169–L202 (raster trace), L330 ("mark overlap 0.90, residue is anti-aliasing"); `rounds/aqueduct-storyboard-drafts:r1/critique.md` ("What holds up across the engine"); 8c2c8bf9 L623–L628 (zoom check), L665 ("Our engine traced each arch and the top band as about 30 straight segments, and all ten candidates draw from that trace").
- **Cost:** 2 rounds (10 drafts, 4 builder subagents, 2 critic dispatches), about 16 h of wall time to the founder's verdict, one long founder message. It started the drawing-board re-chart (mmm-infra#13–#17).
- **Root cause:** An area-overlap figure (IoU) cannot see faceting: a 30-segment chain overlaps a smooth curve at above 0.9. The method had no curve-fidelity check, and the engine traced a small raster instead of fitting curves.
- **Owner of the fix:** design-vault design-critique and design-round scripts.
- **Already filed:** fixed by design-vault 5d1f926 (craft rule 1 and `check-curves.js`, from mmm-infra#16). The end-to-end 0.5 px overlay tool is #73. The checker's path is #75.
- **Proposed change:** none new. One addition to #73: say in rule 1 that an IoU or overlap ratio is not evidence of curve fidelity, because the builder and the critic both used one as proof.
- **Confidence:** 90% (80–95%) that this is the largest single cause of the founder's round-two rejection. His message leads with it, and the session confirmed it in the file.

### L2: The fresh critic praised the faults the founder rejected most
- **What happened:** The critic judged against the brief's words, not against physics or timing research. Round one: "Every candidate runs under a minute" is listed under "What holds up" (drafts ran 14–30 s). Round two, v3 "Water runs": "Smooth: yes. Short: yes (shortest)", "Continuity: one unbroken line", 22/28 and 16/20, the top score of the round. The founder called the same draft the main bad example for pacing and for the water's path. The critic did not report the water running uphill over the band's crest, the timber frames that did not fit the stones, or the jolt-and-pause pacing.
- **Founder's words:** "Round 2 v3 "water runs" is an excellent example of this done badly, where the pace at which water runs feels very disjointed and makes no logical sense to what's happening in the animation." (8c2c8bf9 L605). "stones are laid on a frame, but the frame and the stones dont align at all and have massive gaps between them, making the whole thing look like it was done by a child." (same line)
- **Evidence:** `rounds/aqueduct-storyboard-drafts:r1/critique.md` (S-list, "What holds up"); `r2/critique.md` lines 53, 60–61, 125, 137; 8c2c8bf9 L543 (the scores were the only quality signal put next to each option in Q1).
- **Cost:** The critic signal pointed the founder at the wrong leaders. He spent his review re-deriving four faults (curves, alignment, flow, length) by eye. 2 critic dispatches of no use for the leader choice.
- **Root cause:** design-critique (0202f18) had no lens for physical plausibility of motion, contact alignment, motion flow, or length research. The critic took Mark's "under a minute" and the brief's "smooth, short" as the measure. impeccable's heuristics score UI qualities and did not move this.
- **Owner of the fix:** design-vault design-critique.
- **Already filed:** mostly fixed by 5d1f926 (craft rules 2–4 run by the builder and again by the critic) and a48fb01 (`check-flow.py`). The jolt and mid-move gaps are #68 and #69.
- **Proposed change:** the current review strip (design-round §4, lines 111–117) already puts the gate result first and bars a failing candidate from the lead. One gap stays open: nothing records where the critic and the founder disagree. The round record's "founder's choice" column could also hold his verdict per candidate, so a later session can see whether critic scores predict his picks.
- **Confidence:** 50% (35–65%) that the calibration column is worth its cost. No motion round has run since 5d1f926, so the new gate's agreement with the founder is untested. It rises if the site-look rounds in 631cff6d show the same score-and-verdict split.

### L3: Round one took Mark's ideas as the letter of the brief, in the motion round as well as the identity round
- **What happened:** All five round-one drafts built the logo stone by stone in Mark's construction order. The founder had to rule that Mark's ideas are suggestions and that other families (the logo turning into something else) must be explored. Round two then widened. After round two he still listed families that no draft explored: camera moves to a top or side view, perspective change, scroll-driven background.
- **Founder's words:** "Mark's suggestions for the animation shouldn't be taken as law, but as suggestions. We can also explore other ideas, including starting with his logo and having it turn into something else. Multiple directions should be examined, taking the spirit of what he asked for rather than the letter." (8ad05cae L799). "We didn't get any examples of exploring the direction of the logo changing perspective. ... We need more rounds of creative discussion and ideas before we can make decisions here." (8c2c8bf9 L605)
- **Evidence:** 8ad05cae L782 (five build-the-logo directions); L860–L868 (round two brief); 8c2c8bf9 L605 point 3.
- **Cost:** 1 round (round one) spent inside one family; 2 founder messages.
- **Root cause:** design-round seeds directions from library entries and the brief. It has no step that lists the families a motion asset can take (build, transform, camera move, scroll-driven, in-page) before cards are written.
- **Owner of the fix:** design-vault design-round.
- **Already filed:** #79 covers the same fault for the identity round in 631cff6d (5–8 Oct). The transcripts show it happened one day earlier, in the motion round (4 Oct).
- **Proposed change:** add to #79: before round one of a motion asset, the cards cover at least three distinct families, named in the round record, and the client's own idea is one family at most.
- **Confidence:** 70% (55–80%). It falls if the 5d1f926 "client-values field" already makes a session read the client's ideas as spirit.

### L4: The motion round ran before the site's look, and no draft length came from research
- **What happened:** #9 (animation) depended only on the construction research and the pipeline pick. It did not wait for #8 (the site's look), so the intro was designed with no palette or identity. Each draft's length was "what its build came to". Research (#13) later set 3–5 s to a usable page; every intro-placement draft ran 10–30 s.
- **Founder's words:** "Did you deeply consider the overall artistic direction the website should be going in before making these? I don't remember discussing that or going through design rounds to establish it." and "This should have been a carefully optimised consideration, not a hap-hazard generation. Most of what you created takes far too long" (8c2c8bf9 L605)
- **Evidence:** 8c2c8bf9 L665 ("the animation ticket (#9) depended only on the construction research and the pipeline choice"; "no timing research was done"), L914.
- **Cost:** part of the same 2 rounds as L1; 3 research subagents (#13, #14, #15) after the fact.
- **Root cause:** design-round (0202f18) had no gate on the look being settled before a motion round, and no motion brief with a length range.
- **Owner of the fix:** design-vault design-round.
- **Already filed:** fixed by 5d1f926 (no motion round while the look is open; a motion brief; rule 4, length from research). Beat tables that check the length before render are #70.
- **Proposed change:** none.
- **Confidence:** 90% (80–95%).

### L5: "Into the valley" used a technique the session had never built, with no technique research first
- **What happened:** Round two v1 cut photo "windows" into the arches and then showed a still photo for 4.5 s. The first view through the arches was the photo's own stonework. The critic found the window shapes wrong and the still tail (18/28). The founder called the whole draft "awful" and asked for a research step for this kind of scene progression.
- **Founder's words:** "If we were to explore this direction, it should have first included a research step on how to best build a scene progression of this type." (8c2c8bf9 L605)
- **Evidence:** 8c2c8bf9 L264–L347 (built in about 5 min by the lead session itself); `r2/critique.md` lines 176–180.
- **Cost:** 1 draft, $0.60 of Higgsfield credit, one paragraph of founder review.
- **Root cause:** design-round has no rule that a direction which needs a technique new to the project (a photo reveal, a morph, a camera move through a scene) gets a short technique study before it is built. #72 covers morphs only.
- **Owner of the fix:** design-vault design-round.
- **Already filed:** no. #72 (morph method) is close but covers path morphs only.
- **Proposed change:** in design-round §2, a direction card names its core technique. Where the project has no kept precedent for that technique, the card cites a short study (precedent sites or a reference film) before the build.
- **Confidence:** 55% (40–70%). Only one draft shows it. It rises if the identity or animate-comparison sessions show the same pattern.

### L6: "The arch through time" replaced a shape instead of morphing it, and a rectangle flashed
- **What happened:** The founder saw stray rectangles at the left edge and a horizontal bar that flashed in the last scene. He traced the bar to a replace instead of a morph. The critic found floating-deck moments but not the flash.
- **Founder's words:** "I think the random flash of a rectangle later, happened because you replaced the arch in the original scene rather than morphing it." (8c2c8bf9 L605)
- **Already filed:** #72 (morph method).

### L7: The founder had to ask where to review the work, after the preview server died
- **What happened:** The round-two hand-off gave `http://127.0.0.1:8792/`, served by a process with a 4 h timeout. The founder came back 13 h later and asked where to look. Round one's hand-off gave only a branch and folder.
- **Founder's words:** "Where do I go to see an review all that you've made across both rounds? Give me simple and easy steps to follow, doing what work you can so I don't have to" (8c2c8bf9 L558)
- **Evidence:** 8c2c8bf9 L238 (`timeout 4h`), L534, L558, L585 (new server, 12 h).
- **Already filed:** #77 (viewing route in the round record). A localhost link with a timeout is not a viewing route.

### L8: Plain-language miss on the first question round
- **What happened:** The round-one session put the founder's Seedance remark to him as a priced question about a "ruling", with references to #5 and the roster. He could not follow it and was confused why Seedance was "a bad fit" when scroll-world used it.
- **Founder's words:** "What ruling? I'm not ready to decide yet, explain this all a bit better in simple lay-mans terms. ... Make all this clearer before we proceed" (8ad05cae L789)
- **Evidence:** 8ad05cae L701–L736, L789, L795 (the plain re-explanation with an analogy, which worked: next reply was "Otherwise accept recommendations").
- **Cost:** 1 founder message, about 25 min.
- **Root cause:** the question used tracker jargon ("ruling", "#5", "override") and dropped the reason he raised it.
- **Owner of the fix:** workflow-core (question-round style), not design-vault.
- **Already filed:** workflow-core#478 (question rounds decidable first time) and #628 (re-pitch in plain words on "explain simpler"), both closed. A second case is L15.
- **Confidence:** 50% (35–65%) that this is a pattern and not a one-off.

### L9: Round one ran with design mode off, so its critic had no impeccable scores
- **What happened:** design-round (0202f18) line 25 said: "Where the `impeccable` skill is not loaded, tell the founder to switch design mode on and restart, and render nothing." The rule covered "a web-surface round". The session treated the intro as a motion asset, rendered five drafts, and the critic reported "Design mode is off in the critic's session". The founder heard of it only in the hand-off.
- **Evidence:** 8ad05cae L25 (no impeccable skill in the session's skill list), L740–L755, L782; `git show 0202f18:plugin/skills/design-round/SKILL.md` line 25.
- **Cost:** low. Round two ran with impeccable and still missed L1 and L2, so the scores would not have saved the round.
- **Root cause:** the rule's scope ("web-surface round") did not say whether a homepage intro counts.
- **Owner of the fix:** design-vault design-round.
- **Already filed:** no.
- **Proposed change:** say that an asset that plays on a web page (an intro, a hero motion) is a web-surface round for the design-mode check, or say it is not.
- **Confidence:** 60% (45–75%) that the scope is still ambiguous today; check the current line 25 wording before filing.

### L10: The craft rules shipped into the vault the same morning, with no concision pass and no pressure test
- **What happened:** 1bbd72cf (#16) wrote about 400 words of rules into design-round and design-critique, plus `check-curves.js`, in about 12 minutes after the ruling. It mutation-tested the script (six mutations). It released the plugin. It ran the concision pass only on the mmm-infra note and said so. No baseline-agent pressure test of the new rule text ran. Later sessions found rule-text faults: rule 3 ("falls that follow gravity") conflicts with `check-flow.py`'s jolt rule (#68). Rule 1 names a 0.5 px overlay with no tool (#73). The critique names `check-curves.js` with no path (#75).
- **Founder's words:** "accept recommendations" (1bbd72cf L161). No correction from him in this session.
- **Evidence:** 1bbd72cf L197–L350, L437 ("The new rules text in the design vault (about 400 words in the round method and the critic's checklist) was pushed and released without one."); design-vault 5d1f926.
- **Cost:** three later tickets (#68, #73, #75) trace to wording or tooling gaps in this one commit.
- **Root cause:** a cross-repo edit from an mmm-infra session ran the mmm-infra commit gates but not design-vault's prose steps. design-vault has no rule that a skill change gets a pressure test.
- **Owner of the fix:** design-vault (CLAUDE.md or README §Releasing).
- **Already filed:** #85 (pressure-test skill changes).
- **Confidence:** 60% (45–75%) that a pressure test would have caught one of the three. A fresh reader of rule 1 asks "with what tool?".

### L11: The first "how many directions go to Mark" question hid the load it was meant to limit
- **What happened:** 6a96e0c1 (#17) priced "at most six distinct directions", with five build drafts merged as variants inside one direction. The founder saw that this moved the count, not the load. He asked for two limits and for research behind each. Later he asked for 3 against 4 priced with reasons, and for research on the answer format. The session then ran two research subagents and landed `docs/research/option-load.md` and `docs/research/client-feedback-format.md` in mmm-infra.
- **Founder's words:** "This is a confusing question, because we are really managing Mark's cognitive decision load. "One direction with 6 variants" is going to be heavier than "One direction with one variant", so you're kind of just moving to question to "how many total variants". ... lets be clear what we're doing here and back the decisions up in research" (6a96e0c1 L202). "the optimal format should be a research question." (L424)
- **Evidence:** 6a96e0c1 L197, L202, L222, L424, L429; mmm-infra 06102e8, 66c010e.
- **Cost:** 2 founder corrections, 2 research subagents (plus 2 concision readers), about 1 h.
- **Root cause:** the first pricing used two web searches, not research. The question framed the count of directions, not the count of items Mark judges.
- **Owner of the fix:** design-vault design-round (see L12). The pricing style is workflow-core's.
- **Already filed:** no.
- **Confidence:** 70% (55–80%).

### L12: The client-review rules from #17 live only in mmm-infra
- **What happened:** #17 settled, with research, how a client sees a round: three directions, one per family; one variant each by default; 4 items as the target and 6 as the ceiling; the same finish on each item (3–5 stills plus a rough clip); a rating per item, one pick with a reason, "you choose" as a valid answer; an optional "shape it" box (keep, change, bring in from another idea, avoid); and a "You said → what I did" list at the final yes. design-round today says nothing on how many candidates go to a client or how the client answers.
- **Evidence:** 6a96e0c1 L589, L671; `grep -i 'client|how many'` on current `plugin/skills/design-round/SKILL.md` finds only the "Client values" brief field (line 35).
- **Owner of the fix:** design-vault design-round.
- **Already filed:** no.
- **Proposed change:** add a short "Client review" section to design-round that cites the two mmm-infra research files and carries the limits and the answer format above as the default for any project with a client.
- **Confidence:** 65% (50–80%) that this is wanted in the vault. It falls if the founder sees Mark's family-only review as a one-off.

### L13: The interior-face geometry research went out before the founder's rigour standard, and was stopped and re-sent
- **What happened:** b421876f filed #18–#20 and dispatched the #19 split-geometry agent with a brief that asked for candidate curves. Two minutes later the founder added a standard. The session stopped the agent (it had written nothing) and re-sent it with a physical arch model, a light model, and a curvature plot. Then a network error (EAI_AGAIN) killed both agents. A third dispatch finished.
- **Founder's words:** "if we planned to distinguish the "interior surface", this should be done very carefully with a rigorous physics and perspective analysis, with the separating curve deliniating the interior from exterior of each arch being smooth and its shape being considered and optimised very carefully to mesh with the form of the existing logo" (b421876f L251)
- **Evidence:** b421876f L234, L251–L287, L308–L334.
- **Cost:** 1 founder message; 1 stopped agent (no work lost). The network failure cost 2 more dispatches; that is not a method fault.
- **Root cause:** the craft rules (5d1f926, 2 h earlier) bind design-round candidates. They do not say that research which produces geometry for a candidate meets the same curve standard. The session wrote the brief without them.
- **Owner of the fix:** design-vault design-round (one line), or none.
- **Already filed:** no. The `check-curves.js` path hunt in this session is #75.
- **Proposed change:** craft rule 1 and 2 also bind any geometry a research ticket hands to a round: it states its model, its fit error in px, and passes `check-curves.js`.
- **Confidence:** 45% (30–60%). The founder caught it at once, and the cost was small.

### L14: Measurement scripts for the mark were lost twice
- **What happened:** #15's research (cb39287f) cut the scripts that fitted the logo; the landed file says they "ran in a scratch directory and were not kept". #19's landing (b421876f) deleted its scripts after the ruff lint hook refused them. Later, #25 found that no kept tool does the 0.5 px overlay check that rule 1 names.
- **Evidence:** mmm-infra `docs/research/logo-geometry.md` line 5; `docs/research/split-geometry.md` line 9; b421876f L816–L872.
- **Already filed:** workflow-core#1022 (closed: name `ruffExclude` so a research instrument is not deleted to pass the lint) and design-vault #73 (the overlay tool).

### L15: A second plain-language miss, in the animate decision
- **What happened:** 50c3dea1 (#28) put Q2 as "which fold-ins do we adopt" with five lettered groups. The founder accepted Q1, Q3 and Q4 but could not read Q2. The plain re-pitch ("Fold in means we copy an idea from `animate` into our own method; we use none of its code") worked at once.
- **Founder's words:** "Accept recommendations except for Q2. For Q2, I'm confused what you recommendation means, so not ready to decide" (50c3dea1 L159)
- **Evidence:** 50c3dea1 L125–L166.
- **Cost:** 1 founder message, about 1 min.
- **Already filed:** workflow-core#478, #628 (closed).

### L16: The founder had to ask whether a research agent was still alive
- **What happened:** The #15 agent wrote F4 and then worked for 30 min with no growth in its findings file, against its brief to append each finding as it landed. The founder asked. The session checked the work folder and found it alive.
- **Founder's words:** "Is the background agent still alive, or is it stalled?" (cb39287f L117)
- **Evidence:** cb39287f L112–L130.
- **Cost:** 1 founder message.
- **Owner of the fix:** workflow-core (artefact-append rule for subagents).
- **Already filed:** not searched in full.

## Why mmm-infra#35 and #20 stalled

- **#20 (two-tone prototype)** waits on mmm-infra#8 (the site's look). #8 hit a "chicken and egg" problem on 6 Oct: the founder could not pick a palette without the photo, or the photo without the palette (#8 comment, 6 Oct). The work then moved to the photo research (#38: rubric v3.4 to v4.3, 9–10 Oct) and stopped on 11 Oct, waiting on photos from Mark. #18 and #19 are done. Nothing on #20 itself is at fault.
- **#35 (shared round engine on the true logo SVG)** waits on design-vault #67, #68 and #69. All three are open, unassigned and have no comments. Each carries `takes:implement`, which is the founder's own slash command and is refused to agents. So no agent session can start them, and no transcript in this set shows the founder running `/implement` on them. After 8 Oct, design-vault commits went to the Higgsfield discount (#61–#64) and the code-standards move (workflow-core#973) instead.
- **Cost of the stall:** none so far. #9's next round also waits on #8 and #20, so #35 is not on the critical path. When #8 settles, #67–#69 plus #35 stand between it and the next storyboard round.
- **Confidence:** 75% (60–85%) for #35. The `takes:implement` routing is a fact. That it is the cause, not only the founder's priorities, is an inference.

## Were design-round and design-critique followed?

As they were on 4 Oct (design-vault 0202f18):
- **Followed:** direction cards; a fresh critic per round with only that round's candidates; a round record on #9; a review strip per candidate; Q rounds with priced options.
- **Bypassed or ambiguous:** the design-mode check (L9).
- **Lacked a step the work needed:** a curve-fidelity check (L1); physical and timing lenses in the critique (L2); a gate on the look being settled before motion, and a motion brief with a length from research (L4); a step for "no leader emerged" (round two rendered five new directions, not "three variants of the leader" as line 78 said); a list of motion families before round one (L3); a technique study for a new technique (L5).
- **Fixed since:** 5d1f926 (5 Oct) added the craft gate (curves, contacts, flow, length, drafts tag), the look-first gate, the motion brief, style tiles with a motion sketch, the client-values field, stills before a playable build, and "step back when no leader emerges" (design-round line 82). a48fb01 (6 Oct) added `check-flow.py`.
- **Not yet tested:** no motion round has run since 5d1f926. The gate and the engine rules (#35, #67–#69) have not met a real candidate.

## Went well

- **The founder's words kept verbatim.** Each long reply was posted word for word on #9, then a per-draft ledger quoted him draft by draft (8c2c8bf9 L645, L788). Later sessions (6a96e0c1 L192) read the raw transcript to check his exact words before pricing a question. This caught a misread: the "narrowing" was his, before the send.
- **Drafts tagged and pushed** (`rounds/aqueduct-storyboard-drafts`, 8c2c8bf9 L695) when he asked that nothing be deleted. It is now craft rule 5.
- **Faults confirmed in the file before agreeing.** The session zoomed the source JPG to prove the corners were the trace's, not the logo's (8c2c8bf9 L623–L665).
- **Research landed before the 24 h sweep.** Short answers were copied onto #13, #14 and #15 the moment each agent reported (8c2c8bf9 L883, L907, L942).
- **A founder idea grounded in the client's record.** 77d763a8 read Mark's CV and tied each "arch at work" morph to a real project of his (solar, hydro, power line). Not in the method: a direction about the client's work cites his own projects.
- **Evidence over a bake-off.** 7dc55449 closed #27 without a build, because reading the tool's code already proved it could not land on the logo. It saved about 150k–300k tokens.

## Bound

- **Read in full (reduced transcripts):** 8ad05cae, 8c2c8bf9, 1bbd72cf, 6a96e0c1, b421876f, 77d763a8, cb39287f, ac77e960, 4226ac58, 7dc55449, 50c3dea1. The founder's round-two reply was read in full from the raw jsonl (8c2c8bf9 L605).
- **Read in part:** raw 8ad05cae lines for design mode; `rounds/aqueduct-storyboard-drafts:r1/critique.md` (first 80 lines) and `r2/critique.md` (grep for the founder's four fault classes); design-round at 0202f18 (grep) and today (grep); design-critique §1a; design-vault plugin log from 3 Oct.
- **Issues read:** design-vault #67–#73, #75, #77–#79 (bodies), labels on #67–#73; mmm-infra #35, #20 (bodies, blockers), #8 (last two comments). workflow-core searched for plain-language, critic score, ruff and aqueduct terms.
- **Not read:** subagent transcripts (builders, critics, research agents); the round-two builder outputs beyond their reports; the 631cff6d site-look rounds (another ticket's scope); any design-vault session after 8 Oct.
- **Not verified:** whether the founder ever ran `/implement` on #67–#69 outside these sessions; the exact word count of round-two founder review time.
