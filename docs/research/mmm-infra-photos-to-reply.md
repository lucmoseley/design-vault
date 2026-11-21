# Research: why the critiques of Mark's photos were wrong, up to the #32 reply (design-vault #89)

⚠ **Bound 13 Oct 2026 (#93): every finding here is ruled. S1, S4, S5 and S7 go to #106; S3, S8, S11 and S12 to #107; S5 and S10 to #110; S6 and S9 to #108; S14's review page to #111. S2 is a cause with no change of its own; S13 sits in map #87's Out of scope.**

Owner of every proposed change below: #94 (which mmm-infra findings design-vault adopts) rules on each; a finding about judging a client's photos goes to #93 (photo method).

Question: Where did the work on photos of Mark, up to the reply on the current site's photos (lucmoseley/mmm-infra#32), miss what the founder wanted, or have to redo work? Why were the criticisms wrong? Did design-vault's critique method (design-critique, design-round) play a part, was it missing, or was it bypassed?

Sources: reduced transcripts in `/home/lucmo/design-vault/.claude/tmp/dbb2d38b-reduced/`. Raw transcripts in `~/.claude3/projects/-home-lucmo-mmm-infra/<id>.jsonl`. Line numbers `L<n>` are jsonl lines. mmm-infra issues and `docs/`.

Status: complete (13 Oct 2026).

## Findings

### S1: The first reply answered a different question from the one Mark asked
- **What happened:** Mark asked: "What are your thoughts regarding the existing photos on the website?" The session reused the #22 study. That study asked which photos can carry the *new* site. The first two drafts told Mark which photos to keep or retire for the new site. The founder had to say that Mark asked about the photos as they are used now. Only then did the session render the live page and measure each photo in its slot.
- **Founder's words:** "Again a bad job. He didn't ask about the new site, he just asked what I think of the photos used on the old site. Again, he didn't specify for what purpose, so we should judge reletative to the way he is currently using them on that site" (6212cdfa L242)
- **Evidence:** 6212cdfa L216 (draft 1, "two of the photos ... worth keeping. The rest are better retired"), L238 (draft 2, same frame), L245-L357 (live render and slot measurement, only after the correction).
- **Cost:** 2 drafts discarded. 2 founder messages (L234, L242). About 50 minutes.
- **Root cause:** The session treated earlier research as the answer. It did not first restate the client's question and the context of use. The #22 rubric scored photos for new-site slots (P, W, A). Mark's question had a different context: the photo in its current slot on the Wix site.
- **Owner of the fix:** design-vault design-critique (a "context of use" step before any judgement of an existing asset).
- **Already filed:** no.
- **Proposed change:** Before a critique of an existing asset, the critic writes one line: "Judged as: <asset> in <slot, page, audience>, for <the question asked>." The critic judges only against that line. Earlier research for a different slot is input, not the verdict.
- **Confidence:** 80% (70%-90%) that this was the first failure. A transcript of an earlier session that framed Mark's question differently would lower it.

### S2: The false criticisms came from a self-written rubric, reused as settled
- **What happened:** The third draft judged each photo in its current slot. It still said the radio-interview photo was a "phone snapshot", that "the interviewer gets as much of the frame as you do", that Mark was "not in a jacket", and that the container ship pulled the eye. The founder called the criticism "ridiculous". The session then found that these points came straight from the #22 rubric: R3 (other people, logos), R22 (distraction), R13 and the dress and phone-quality lines. That rubric marks its own inferences "[I]" 118 times. Its R3 rested on Getty's stock-licence model-release rule and the World Bank's terms for its own logo. Its R22 rested on Mark's "busyness" remark, which was about page layouts. The #22 result posted the shortlist and did not say that it depended on these inferred rules. Under v2, 145 of 174 photo-and-slot pairs were ineligible; 77 of them only by R3 or R22.
- **Founder's words:** "This whole criticism is ridiculous." (6212cdfa L442); "This now feels a serious issue that you are presented criticisms that don't hold up. Could that type of behaviour infected the photo analysis in general? ... This is now a mission critical failure." (6212cdfa L456)
- **Evidence:** 6212cdfa L438, L452, L459, L503; cf61181e L463 summary ("R13 caused the radio-booth criticism directly"), L707; mmm-infra#22 correction comment (6212cdfa L588); mmm-infra#30 resolution.
- **Cost:** The whole chain #29 -> #30 (4 audit agents; the two whose usage shows took 186k and 211k tokens) -> #33 (rescore of 58 photos on v3) -> #37 -> #38. The #32 reply waited from 8 Oct 09:59 until after #33 closed (see later findings). The founder lost one message per false point (L435, L442) and one message to escalate (L456).
- **Root cause:** Three causes stacked. (1) A rubric criterion carried a source from another field (stock licensing, a bank's logo terms). (2) A single 0 on one criterion vetoed a photo, and one scorer alone could veto (cf61181e L463). (3) The session that wrote the reply copied rubric verdicts into a human message without a "would a sensible viewer say this?" check.
- **Owner of the fix:** design-vault design-critique §3 (the rule already exists, see S5); the project rubric itself is mmm-infra.
- **Already filed:** no (design-vault). The mmm-infra side is closed by #30 and rubric v3.
- **Proposed change:** See S3 and S5.
- **Confidence:** 90% (85%-95%) on the cause chain. The session itself traced each false point to a rubric line, and the #30 audit agreed.

### S3: The rubric's dispatch prompt asked for vetoes and seeded the two false rules
- **What happened:** On 6 Oct the founder asked for a deep photo study that is "rigorously verified for alignment with detailed principles". The building session sent a rubric agent. Its prompt told the agent to write the rubric "BLIND", with no photo of Mark seen. It asked for "a gate flag where a failure disqualifies a photo from a slot regardless of other scores". Facet 9 named "other people in frame, other organisations' logos (implied endorsement)". The agent built R3 on exactly that. No step tested the finished rubric against photos a sensible person accepts before the two blind scorers used it. The verification step (a second agent, "Verify the photo rubric's sources") checked that each citation existed. It did not check that the source supports the rule in this context.
- **Founder's words:** "I feel like this is an area where it would be very easy for you to do a lazy analysis of the photos that would end up making bad choices, and I want to very intentionally make sure that does not happen. The study should be deep, multi-faceted, and rigorously verified for alignment with detailed principles" (631cff6d L7620)
- **Evidence:** 631cff6d L7742 (rubric agent prompt, raw jsonl), L8154 (source-check agent), L8215 (rubric v2 from the check); cf61181e L463 (the audit's root causes: single-criterion veto, sources used outside their field, scorers blind to the setting).
- **Cost:** Rubric v1 and v2 work (3 agents) was largely replaced by v3 two days later. The #22 shortlist was too narrow, so the 7 Oct originals request to Mark may have missed photos (6212cdfa L503, L520).
- **Root cause:** "Rigorous" was read as "many sources, blind authoring, two scorers, hard gates". Each of these raises agreement and traceability. None of them checks that a criterion matches what the intended viewer would object to. A blind rubric also cannot see the setting of a photo (an interview shows an interviewer).
- **Owner of the fix:** design-vault (a new reference for any scoring rubric a project builds to judge assets: client photos, references, candidates).
- **Already filed:** no.
- **Proposed change:** Add a short rule set for any rubric that judges assets. (1) A criterion's source must be from the same field and use; a rule borrowed from another field is a note, not a gate. (2) Only a named, short list of faults may veto, and a veto needs both scorers plus a written reason a reader would reject the asset. (3) Before first use, score a handful of known-good and known-bad assets that the founder has ruled on, and fix any criterion that faults a known-good one. #30's v3 adopted (1) and (2) for mmm-infra. Item (3) became the regression file (#37). None of this is in design-vault.
- **Confidence:** 75% (60%-85%) that a design-vault rubric rule would have stopped R3 and R22. It would fall if the session that built the rubric would not have loaded a design-vault skill for a research ticket at all (see S6).

### S4: The founder's 7 Oct question was an early signal of the same fault, and was treated narrowly
- **What happened:** On 7 Oct the founder read the draft email to Mark. It asked for photos "where other people could be cropped out" and said "a plain background helps". He asked why. The session answered that the scorers had judged a clean edit unrealistic for most event photos, and "Nobody tested it". It named four strong near-misses that others in frame or logos had removed. It then tested the edit tools (photo-edit-test). It did not question whether "others in frame" was a fault at all. The same rule produced the radio-photo criticism the next morning.
- **Founder's words:** "Why are we asking for photos \"where other people could be cropped out\" or saying that \"a plain backgroun helps\". Surely these tasks are trivial?" (631cff6d L8894)
- **Evidence:** 631cff6d L8894, L8898; 6212cdfa L442, L459.
- **Cost:** About 17 hours between the signal and the failure. The edit-tool work went ahead on a shortlist that was too narrow.
- **Root cause:** A founder question about one consequence of a rule was answered as a question about the remedy (can the tool remove the people?) and not about the rule (is a colleague in frame a fault?).
- **Owner of the fix:** design-vault design-critique (part of the S5 change), or none.
- **Already filed:** no.
- **Proposed change:** When the founder questions an output that a criterion produced, re-check the criterion against its source and context, not only the remedy. One sentence in design-critique §3 is enough.
- **Confidence:** 55% (40%-70%). The founder's words were about effort, not about the rule, so a reader could fairly have taken them as he did.

### S5: design-vault's critique was never used on the photos, and its own standard would have stopped the false points
- **What happened:** No session from #22 to #32 loaded `design-vault:design-critique` or `design-vault:design-round`. The skills show only in the skill listing and in mmm-infra's CLAUDE.md line "Design work runs through design-vault:design-round". The photo work ran as wayfinder research tickets, with self-written rubrics, blind scorers and reconcilers. design-critique §3 (pinned 919c6b3, 6 Oct) already says: "An edit needs a real deficiency that you can defend. For every recommendation, name the deficiency it removes in plain user terms ... If you cannot finish that sentence, drop the recommendation." The radio-photo points ("phone snapshot", "not in a jacket", "the interviewer gets as much of the frame") fail that test. #30's v3 rebuilt the same idea inside mmm-infra: a disqualifier needs "A reader would reject this photo for this slot because ...".
- **Founder's words:** "If we are criticisng, be need to know why blur is bad, especially as it seems to have been an intentional choice. If you're not sure why, check relevant literature on web design." (2cfe57f4 L454)
- **Evidence:** zero `Skill` calls to design-vault in 6212cdfa, cf61181e, 25002955, a0d78fee, a6d9243a, ef9936fe, f84e2526, 2effb712, 0f5ce7d9, 2cfe57f4 (raw jsonl grep: only listing and CLAUDE.md hits). design-vault `plugin/hooks/design-round-pointer.sh` fires only on the skills `design`, `prototype`, `animate`, `design-mode` and `impeccable`. design-critique's description scopes it to "any project's candidate — a page, a component, an artwork or a screenshot". design-round §6 lists no asset class for a client's existing photos.
- **Cost:** The cost of S2, S3 and S7: the v2 rubric's false gates, the v3 rebuild, and two days of drafts.
- **Root cause:** The method was missing for this kind of work, not refused. (1) Judging a client's existing photos, or his live site, is not a "candidate" in a round. (2) The pointer hook watches rendering skills, and photo work renders nothing. (3) The founder's demand for rigour sent the work to the research skill, which owns sources, not judgement.
- **Owner of the fix:** design-vault design-critique (scope and §3), design-round §6 (an asset class), design-round-pointer.sh (trigger), or a new skill.
- **Already filed:** no. The map's "Not yet specified" names this question ("Whether the design round needs a stage, or a separate skill, for work that is not one of its candidate types: a client's photos, the text written to the client").
- **Proposed change:** Widen design-critique's scope to "an existing asset judged in place" (a client's photo, a live page). Add a §3 test that every criticism names who would object and why, in the asset's real context. Give design-round §6 a "client-supplied assets" class: census, judge in place, choose for the new design, edit. Point at it from any rubric a project builds to score assets.
- **Confidence:** 65% (50%-80%) that routing the work through design-critique §3 would have stopped the radio-photo points on 8 Oct. It would fall if a session in critique mode still deferred to a project rubric it took as settled.

### S6: The founder corrected the same two faults in the reply on two days, because the 8 Oct corrections lived only in chat
- **What happened:** On 8 Oct the founder said the reply was "far too long" (L234) and "reads like AI slop" (L362). He corrected "soft" (L404) and "stretched" (L427). The session applied mantahostels' `outbound-messaging.md` rule 15 in chat. It put the corrected draft in the #32 body ("a bit blurry", no "stretched"). It wrote no rule. On 9 Oct a new session redrafted from scorer notes. The new draft said "looks a bit soft" and "with the photo stretched to the full width". The founder again said "reads as AI slop and is far too long" (L364) and "What does soft mean?" (L454). Only then did a session write `docs/copy/writing-to-mark.md` (commit efe0c9e).
- **Founder's words:** "Right, so immediately this reads as AI slop and is far too long. Check what rules we have to prevent AI slop sound (the mantahostels repo should have a few), and try again. At most half the length, ideally less" (2cfe57f4 L364); "What does soft mean? That's not a lay-mans term for photos." (2cfe57f4 L454)
- **Evidence:** 6212cdfa L234, L362, L404, L427; mmm-infra#32 body; 2cfe57f4 L329, L364, L454, L931.
- **Cost:** About 4 founder messages repeated on 9 Oct. Two lost drafts (L329, L449).
- **Root cause:** A founder's wording correction is a rule for every later message to the same reader. The 8 Oct session recorded the corrected text but not the rule. The next session reused rubric words ("soft", "stretched", "copy", "weakest") because no translation step existed.
- **Owner of the fix:** mmm-infra (done: `docs/copy/writing-to-mark.md`). For design-vault: none, unless design-vault takes on writing to a client (see S9).
- **Already filed:** no.
- **Proposed change:** In any project, when the founder corrects a word or tone in a draft to a named reader, write the rule into that reader's guide in the same turn. design-vault could ship a template for that guide (see the reusability section).
- **Confidence:** 85% (75%-90%). The words repeat exactly across the two sessions.

### S7: After the "deep re-evaluation", the 9 Oct reply was wrong again, because the re-evaluation never judged the current site
- **What happened:** On 9 Oct the founder asked if the re-evaluation (#30, #33, #36) made the reply ready. The session said "Yes, we're ready" (L313). It mapped the v3.1 new-site scores (slots P, W, A) onto the six gallery tiles and the homepage photos. It did not render the gallery. The founder's screenshot then showed four errors: (1) the "Shanghai skyline" photo was not visible and the top-left tile showed Mark's whole head (the head-crop claim came from one 1440 px render on 8 Oct, and the #32 body said "Wix crops differ at other widths"); (2) the top-left photo, praised by the scorers as a "calm speech frame", had an odd mid-word face; (3) the AIIB photo was called weakest by the hero-slot test, not the gallery test; (4) the grainy top-right photo was not faulted, because the v3 reporting rule bans calling low file quality "a fault of the photo". The session then wrote: "The current-site evaluation was never actually done."
- **Founder's words:** "I stopped editing here because I'm not sure I agree with your gallery criticims, which raises a larger question of if we have to re-do that effort again and why you still seem incapable of good analysis" (2cfe57f4 L535); "I don't even see the Shangai skyline photo in the gallery" (2cfe57f4 L454)
- **Evidence:** 2cfe57f4 L6, L136-L183 (scores pulled, no render), L313, L329, L454, L535, L601 (full raw text: "I mapped those ranks onto the old gallery and never looked at the page as Mark sees it; your screenshot was the first rendered view"); mmm-infra#32 body ("Wix crops differ at other widths"); commit efe0c9e (rubric v3.1 banner: not for judging the live site).
- **Cost:** 3 more drafts (L329, L449, L523) before the founder wrote the first two paragraphs himself (L535), then the gallery half (L1368). About 9 founder messages on 9 Oct. The founder fixed his final text on 9 Oct at 06:00 (L1368), about 21 hours after the first draft. The transcript does not record when he sent it.
- **Root cause:** This is S1 again, one level up. The fix for S2 was to repair the rubric. The rubric was built for a different question (choosing photos for the new site). Nobody re-asked whether a rubric was the right tool for Mark's question. The founder's word "deep re-evaluation" pointed at the rubric, and the session did not challenge that frame.
- **Owner of the fix:** design-vault design-critique (the "Judged as" line from S1, and "judge a live page from a render of it at the reader's widths").
- **Already filed:** no.
- **Proposed change:** Same as S1 and S5, plus one check: a verdict on a live page cites a render of that page at desktop and phone width taken in this session. A score made for another slot can support a verdict only if the line says so.
- **Confidence:** 85% (75%-95%). The session's own diagnosis at L601 says the same.

### S8: Rubric v3 fixed the false positives by loosening rules, and so let real faults through
- **What happened:** #30 rewrote the criteria so that "speaking" and "on-theme backdrops" stop counting against a photo, and so that file size and slot-only scores are never "stated as a fault of a photo". On 9 Oct this let through a face caught mid-word (C005, full marks from both scorers) and hid the grain in C010. In the same session the founder found the reverse fault too: C009 (the gallery's bottom-right photo) ranked 25th-36th because of the lettering beside his head, its age, and "mouth open" and gaze. The founder: "I don't think the expression / gaze in this photo as bad at all."
- **Founder's words:** "To me it looks like he has an odd facial expression so I wouldn't have chosen it." (2cfe57f4 L535, item 1); "I don't think the expression / gaze in this photo as bad at all." (2cfe57f4 L1509)
- **Evidence:** 2cfe57f4 L601 items 1 and 3, L1302, L1506; mmm-infra#38 (filed at L845, widened at L1789).
- **Cost:** #38 and everything after it (sibling ticket #90 covers that). One new regression line (C005).
- **Root cause:** Rubric v3 Part 7 had a two-sided regression set: "Must not be disqualified" (the known false positives) and "Must still be caught". But the must-catch lines came from model notes, not from the founder. The only expression line, C044 ("rounded 'o' mouth mid-word"), came from one v2 scorer who never had the image on disk. v3.1 dropped it as unverified (a6d9243a L478). After that, R8 had no must-fail case, and a mid-word face passed. Blind scorers who have never seen Mark cannot judge "an odd face for him". The founder's eye was not asked for the must-catch side until 9 Oct.
- **Owner of the fix:** design-vault (the rubric reference proposed in S3).
- **Already filed:** no. #38 in mmm-infra covers the mmm-infra side; #90 covers it.
- **Proposed change:** Add to S3's rule set: each criterion keeps at least one must-pass and one must-fail case, and each case carries a ruling by the founder (or by a person who knows the subject), not a model note. When a case is dropped, the criterion is flagged as untested until a new case replaces it.
- **Confidence:** 70% (55%-85%). Rubric v3 Part 7 and the v3.1 change list support the cause. A founder-ruled must-fail case for R8 might still have missed C005 if the case was a different kind of odd face.

### S9: The reply was drafted with rules for cold business email, which cut the reasons the founder wanted kept
- **What happened:** Both days, the founder asked for the "AI slop" rules, and both sessions borrowed mantahostels' `docs/copy/outbound-messaging.md` and its lint. Those rules are for cold business email. They only subtract (banned words, no em dashes, no hedges, match the other person's length). After "too long", the session cut the reasons, because "to a cutting pass they look like padding" (2cfe57f4 L601). The 157-word draft (L449) was short and telegraphic. The founder rewrote two paragraphs to show the register: each judgement with its reason, "I think", a spaced hyphen, plain words such as "pixelated". The lint failed his own sentence on "I think". The session then checked the lint against research (Oba, Berger and Boghrati 2026 on "I think"; Kooti et al. 2015 on reply length; Jakesch et al. 2023 on cues of AI text) and filed mantahostels#3665, #3666 and #3667.
- **Founder's words:** "This is really weirdly written, but I'll fix the first couple sentences as a guide for you to fix the rest. Assess the changes I made - the intention behind them - and then why the skills and guideliness you were using to make your drafts didn't catch these types of edits." (2cfe57f4 L535); "The business-correspondance skill should have rules based in research, not ones that are ad-hoc chosen an applied" (2cfe57f4 L609)
- **Evidence:** 6212cdfa L362-L399; 2cfe57f4 L364-L449, L535, L601, L609, L1048; mmm-infra commits efe0c9e, 8fc7b0f, a15407d.
- **Cost:** 3 drafts on 9 Oct. The founder wrote the final reply himself (L1368).
- **Root cause:** No guide existed for writing to this reader. The nearest rulebook was for another genre, and its rules had no evidence grade. A subtract-only rule set cannot add what the reader needs (the reason for each verdict, the photo's place on the page).
- **Owner of the fix:** mmm-infra (done) and mantahostels (filed). design-vault: only if it takes the "text to the client" stage named in the map's "Not yet specified".
- **Already filed:** mantahostels#3665, #3666, #3667. No design-vault ticket.
- **Proposed change:** design-vault's `design-project` could scaffold a "writing to the client" file per project: a voice sample, the client's own words for design faults, "answer only what was asked", and "list unverified claims under the draft". Whether to take this is the map's open question.
- **Confidence:** 60% (45%-75%) that a design-vault scaffold is the right home. A project-local file did fix it, so the gain from a shared scaffold is the second project, not this one.

### S10: Photo edits removed things with no recorded reason, and the edit critics passed a visible fault
- **What happened:** In #31 the founder checked the four edits that the critics had passed. He asked why the name card was wiped and why the lectern text was removed. The session found a reason for the card (it showed another person's name) but no recorded reason for the lectern text ("added to the brief in critic round two with no reason written down"). The founder also found a background light left at Mark's hairline in the Jakarta edit. The critics had passed it. In the same session the agent raised two worries about smoothed skin, re-priced the question round three times in one minute, then measured and found both worries false. The #30 edit audit found the cause in the critic prompts: "You are a strict photo-retouching critic ... Your job is to find every fault." No prompt said "no fault" was an expected result. The pass line moved between rounds of the same edit. The second blind critic (item 21) was never run in rounds 2 to 6.
- **Founder's words:** "Q1 not ready to decide. What was the point of wiping the name card. How does that improve the image? ... Q3 the edit leaves one of the background lights in the picture ... Q4 why wipe the text from the lecturn? what purpose does that serve?" (25002955 L208)
- **Evidence:** 25002955 L169, L174, L185, L203, L208, L270, L423; mmm-infra `docs/research/photo-audit-edits.md` Finding 5 and Finding 7.
- **Cost:** C074 redone (lectern text restored). C017 fix added to #23. 3 re-issued question rounds. 2 founder messages.
- **Root cause:** An edit brief had no "deficiency this edit removes" field. A critic told to find every fault reports faults no viewer sees, and one critic alone missed a fault a viewer does see. design-critique §0 and §3 already cover both points for a candidate: a fresh critic, "Write 'none' where the honest answer is none", and "An edit needs a real deficiency that you can defend". The photo-edit critics were hand-made in 631cff6d and did not use them.
- **Owner of the fix:** design-vault design-round (the brand-art step and the S5 asset class) and design-critique §3.
- **Already filed:** no.
- **Proposed change:** Every edit to a client's photo records, in one line, the deficiency it removes for the reader. The edit critic runs under design-critique, with "Ready, no change is an expected result" stated in its prompt, the reader named, and two critics where the round says two. The edit audit's critic prompt v3 (`photo-audit-edits.md` Finding 5) is a good base and is mostly not Mark-specific.
- **Confidence:** 70% (55%-85%). The audit read the actual critic prompts. A design-critique route would not by itself have seen the Jakarta light, since that fault needs the light-cause check the audit added.

### S11: Most of the rubric work after #30 repaired the rubric's own consistency, and none of it checked the reply's question
- **What happened:** Between 8 Oct 16:27 and 9 Oct 04:22, five sessions worked the rubric: #33 (rescore, 4 blind scorers, 2 reconcilers, a regression run that failed 4 of 32 lines), its successor (v3.1, a caption re-read, a D1 conflict), #37 (scorers had read the regression answers, so a scorer-copy script and banners), #23's D7 item (the threshold disagreed with its own example), and #36 (likeness). Three of the four #33 failures were faults in the regression lines, not in the scores: C012 and C059 lines did not match the files, and the C044 line came from a v2 scorer who never had the image. The founder answered each choice with "accept recommendation" (a0d78fee L1729, a6d9243a L549, f84e2526 L129, 0f5ce7d9 L252). The 9 Oct reply then failed on points this work never tested (S7).
- **Founder's words:** "accept recommendation" (a0d78fee L1729; a6d9243a L549; f84e2526 L129; 0f5ce7d9 L252)
- **Evidence:** a0d78fee L1491, L1631, L1769 (300,000-token ceiling); a6d9243a L478, L539; f84e2526 L92; 2effb712 L712; 0f5ce7d9 L226; session sizes in the session index (a0d78fee 18,594 KB).
- **Cost:** About 5 sessions and more than 12 agent dispatches (scorers, reconcilers, a caption re-read, review axes, concision readers). No founder correction, but no gain for the #32 reply.
- **Root cause:** The founder asked for rigour. Rigour was built as internal consistency (blindness, agreement, regression lines, no leaks). Validity against the founder's eye was tested last, on 9 Oct, and then failed at once (S7, S8). A rubric with 28 criteria, 7 disqualifiers and 31 regression lines has many places to disagree with itself, and each one costs a founder decision.
- **Owner of the fix:** design-vault (part of the S3 rubric reference).
- **Already filed:** no.
- **Proposed change:** Put the founder's eye early and cheap. Before a scoring machine is built, show him a contact sheet of a sample (10 to 15 assets) with the draft verdicts, and fix the criteria from his reactions. Build blind scorers and regression machinery only where the sample shows that the criteria hold.
- **Confidence:** 55% (40%-70%). A founder sample on 6 Oct might have caught R3 and R22 two days early. The founder's own words asked for depth, so a lighter process may not have satisfied him either.

### S12: The likeness step proposed judges the founder had not chosen, and shortlisted photos he found too blurry to use
- **What happened:** In #36 the agent recommended that Mark and Angélique rank the likeness sheets. The founder ruled them out. He then found three photos on the portrait shortlist "far too blurry to be used for anything". Part of the cause: the scorers' portrait crop was never recorded, so the sheets used an estimated crop that enlarged small faces. Part is the v3 ruling that low resolution never disqualifies (ask for the original).
- **Founder's words:** "Angelique and Mark will not be involved. You and me are the only judges that will be used here" (ef9936fe L298); "A, C, and I are far too blurry to be used for anything. Note that I'm ranking what looks like him, not what's a \"good photo\" of him" (ef9936fe L367)
- **Evidence:** ef9936fe L266, L293, L298, L367, L498.
- **Cost:** 1 founder message on the judges. 3 shortlist places removed.
- **Root cause:** Mostly mmm-infra-specific (who may be asked, Mark's limited effort). One general part: a scorer's verdict on a slot did not record the crop or view it judged, so a later reviewer saw a different picture.
- **Owner of the fix:** mmm-infra; design-vault only for the general part (record the view judged, see S3).
- **Already filed:** no.
- **Proposed change:** In the S3 rubric reference: every score records the exact crop and display size it was judged at.
- **Confidence:** 50% (35%-65%) that the general part matters beyond this project.

### S13: Process faults in the same sessions, owned by workflow-core
- **What happened:** (a) The 8 Oct session read the founder's "Great" as acceptance of its recommendation and started filing. The founder: "I haven't accepted your recommendations. DOn't assume that" (6212cdfa L555). (b) The same session ended with the reply to Mark and the founder's eye check living only in chat and in a closed issue's comment. The founder: "Why the fuck would you end a session when its work hasn't completed, unless you filed a ticket to make sure none of that future work or results recording can get lost." (6212cdfa L734)
- **Owner of the fix:** workflow-core.
- **Already filed:** (b) already filed (workflow-core#898, closed). (a) no workflow-core issue found by three searches, each run twice.
- **Proposed change:** Out of scope for design-vault. Name (a) to workflow-core.
- **Confidence:** 80% (70%-90%) on the facts; low on whether (a) is already covered by a rule I did not find.

### S14: The review page for the founder cropped the photos, and the agent's own screenshot showed it
- **What happened:** At the end of #32 the session built a review page of all 56 scored photos. The founder: "The artifact is unusuable because you've cropped photos in strange ways". The agent: "My first screenshot showed the same crop and I missed it."
- **Evidence:** 2cfe57f4 L1606-L1619, L1821, L1836.
- **Owner of the fix:** sibling ticket #90 covers the #38 review page. Close to design-vault #78 (width-sweep layout check) and #77 (round record says how to view each candidate).
- **Already filed:** related to #78.

## What in mmm-infra's guide and audits serves any project

Files read: `docs/copy/writing-to-mark.md` (in full); `docs/research/photo-audit-edits.md`, `photo-audit-face.md`, `photo-audit-scene.md`, `photo-audit-literature.md` (#30, 8 Oct; summaries, cross-cutting sections and verdict tables read, criterion detail sampled); `photo-audit-expression.md`, `photo-audit-gaze-people.md`, `photo-audit-text-context.md` (#38, 9 Oct, sibling #90's period; headings and the taxonomy sampled).

### `docs/copy/writing-to-mark.md`

| Part | Any project? | Why |
|---|---|---|
| Rule 1, answer only what was asked; no fix or question that serves our records | General | Any client message. The #32 failures (S1, S7, closing question) are not specific to Mark. |
| Rule 2, every judgement carries its reason, and a fault says why it matters to the reader; never cut a reason to save length | General | It answers the subtract-only fault (S9). Graded Moderate (Shute 2008). |
| Rule 3, "I think" on an opinion; hedge a fact the client knows better | General | Graded Moderate (Oba, Berger and Boghrati 2026), read from summaries only. |
| Rule 4, name each item by where it sits on the page | General | Any critique of a client's live page. |
| Rule 5, use the client's words, not the rubric's | General as a rule; the word list (pixelated, blurry, grainy) is general for photos | It is the two-register convention design-vault already holds for the founder (CLAUDE.md "Two readers, two registers"), turned outward to the client. |
| Rule 6, judge a live site from a look at the page at desktop and phone width, file quality included; rubric scores never stand in | General | The core fix for S1 and S7. Belongs in design-critique. |
| Rule 7, length fits the question | General | Graded Weak. |
| Rule 8, a string check does not show a draft sounds human | General | Graded Moderate (Jakesch et al. 2023). |
| Rule 9, fault the picture, never the person's face | General for any photo of the client himself | |
| "Before showing a draft": list each unverified claim under the draft | General | It made the founder's checks fast on 9 Oct. |
| The voice sample, "Hi Dad", the father-son register, the event names | Mark-specific | |

### The photo-audit files

| Part | Any project? | Notes |
|---|---|---|
| The audit method of #30: for each criterion ask (1) does the source say it, (2) would it fault what a sensible viewer accepts, tested on named false positives, (3) is it judged in the context of use, (4) keep, rewrite or drop | General | Reusable for any rubric that judges assets (S3). |
| `photo-audit-scene.md` Finding 1: a single 0 vetoes; one scorer's 0 can veto; a veto that rests on a scorer's guess about an edit | General | A structural fault of any veto-based rubric. |
| `photo-audit-scene.md` Finding 2: a source used outside its field (stock-licence release rules, a bank's own logo terms, a press code) | General | The lesson is general. The source list is about photos of people. |
| `photo-audit-scene.md` Finding 3: releases for people at public events, UK, US and Germany; caption a possible endorser with role and year | General for any client's event photos | Legal summary by an agent, marked [I]; not legal advice. |
| `photo-audit-face.md` §3: cross-cutting causes (a slot anchor reported as a fault of the photo; a 0 with no tested source; one defect counted twice; a file limit leaking into a content score) | General | Any multi-slot rubric. |
| `photo-audit-face.md` §4 criterion verdicts (R7-R16) | Partly general | The face-perception sources (gaze, expression, light, camera distance) serve any portrait of a client. The weights and slots P, W, A are mmm-infra's. |
| `photo-audit-edits.md` Findings 1-4: judge an edit at the size a reader sees it, not at image-pixel zoom; noise, edge and fringe checks recalibrated | General for photo editing | The thresholds were calibrated on this project's pairs. |
| `photo-audit-edits.md` Finding 5 and the critic prompt v3: "Ready, no change is an expected and common result"; out-of-scope list; name the reader | General | Its first sentence names Mark and the MDB reader; the rest is general. Strong candidate for design-critique (S10). |
| `photo-audit-edits.md` Finding 7: an edit can change what the photo claims happened; over-clean grounds read as studio; an edit can be worse for the slot; the set can stop agreeing; preferred order of edits (crop, text removal, recolour, ground replacement, person removal) | General | Any client-photo edit. |
| `photo-audit-literature.md` Part C: criticisms looked for and NOT supported (phone photo, "dated" clothes, an old portrait as such, other people in frame as such, an event logo as such, self-promotion) | General | A "do not add" list. It names the exact false criticisms of 8 Oct. |
| `photo-audit-literature.md` L1-L13 | Mixed | L2 (the role the photo shows), L5 (context the reader cannot read), L7 (people who know the subject grade likeness best), L10 (faces and text pull the eye) are general. L1 (development-sector ethics), L6 (international MDB reader) and L12 are specific to this audience. |
| `photo-audit-expression.md` §2 taxonomy of bad and good speaking faces (B1-B11, G1-G6) and the tie rule "a speaking face passes when the eyes are engaged and the mouth has a reason" | General for any photo of a person speaking | The costs rest on the founder's verdicts on 12 faces of Mark, so the weights are Mark-calibrated. #90 owns its review. |
| `photo-audit-gaze-people.md`, `photo-audit-text-context.md` | Mostly Mark-specific | Founder points on named photos (C003, C009, C016, C029); the R25 recency thresholds and R3b text rules have a general core (text in a photo draws the eye; a scene's date is a weak cost). #90 owns them. |
| Slot names P, W, A; R-numbers and weights; C-ids; the EIB-logo and no-disclosure rulings | Mark-specific | |

## Went well

### W1: The founder's escalation became a source-and-context audit with the false points as test cases
- **What happened:** The founder asked not to "just patch the one failure we caught, but systemicatically evaulate and examine our criteria" (6212cdfa L620). #30 ran four parallel audits. The five known false positives became fixed test cases. One audit searched for fair criticisms the rubric missed, and listed those it looked for and did not find.
- **Evidence:** 6212cdfa L620; cf61181e L268-L282, L463, L707.
- **Not yet in design-vault:** yes. **Proposed:** the core of the S3 rubric reference.

### W3: Measuring before asserting withdrew false claims
- **What happened:** In 6212cdfa the session zoomed in to confirm a crop before claiming it (L341-L357) and confirmed "soft" on a zoom (L407-L423). In 25002955 skin-patch measurement withdrew two false worries (L203). In 0f5ce7d9 the camera's frame size showed that Mark's original could not settle the D7 question (L226). In a6d9243a each changed regression line was broken on purpose to confirm it can fail, which found a check that passed when the scorers disagreed (L415-L428).
- **Not yet in design-vault:** the general rule is in AGENTS.md ("Verify before you assert"). The photo-specific forms (zoom on the displayed render; measure a patch) are not in design-critique.

## Answer in short

The criticisms were wrong for three reasons, in this order:
1. **Wrong question** (S1, S7).
2. **A rubric that vetoed on borrowed sources** (S2, S3, S4).
3. **A fix that moved the error** (S8, S11).

design-vault's critique method was **missing, not bypassed by choice** (S5, S10).

Proposed design-vault changes, for the map to rule on:
- **A. design-critique:** widen the scope to "an existing asset judged in place". Add a "Judged as: <asset> in <slot, page, audience>, for <the question asked>" line, a verdict on a live page from a fresh render at desktop and phone width, and a §3 test that names who would object and why (S1, S5, S7).
- **B. design-round §6:** a "client-supplied assets" class: census, judge in place, choose for the new design, edit. Every edit records the deficiency it removes. The edit critic runs under design-critique with "no change is an expected result" (S5, S10).
- **C. A reference for any rubric that scores assets:** sources from the same field; a short named veto list needing both scorers plus a reader's sentence; a two-sided regression set with founder rulings on each side; record the crop and size judged; a founder contact-sheet sample before any scoring machine (S3, S8, S11, S12).
- **D. Optional, the map's open question:** a per-project "writing to the client" scaffold in design-project (S9).

## Bound

- **Read in full (reduced transcripts):** 6212cdfa, cf61181e, 25002955, 2cfe57f4 (lines 1-360 and 520-898 in full; lines 360-520 are the context summary and a concision pass, scanned by their ASSISTANT lines only, with no founder message). Read without tool lines: a0d78fee, a6d9243a, ef9936fe, f84e2526, 2effb712, 0f5ce7d9.
- **Raw transcript lines read:** 631cff6d L7742 (the rubric agent's prompt); 2cfe57f4 L601 and L1048 (full text).
- **631cff6d** (the #8 and #22 session) is outside my session list. I read only its founder lines from L7313 to L9455 and the #22 portion around L7620-L7742 and L8886-L8898. I did not read the rubric v1 or v2 agents' own transcripts.
- **Issues:** mmm-infra#32 body read. #22, #29, #30, #33 read only as quoted in the transcripts. workflow-core searched for the S13 faults.
- **design-vault as it was:** design-critique SKILL.md at 919c6b3 read in full; design-round SKILL.md at 919c6b3 searched for photo and asset terms; `plugin/hooks/design-round-pointer.sh` read.
- **mmm-infra docs:** `docs/copy/writing-to-mark.md` read in full; rubric v3 Part 7 read; the seven photo-audit files sampled as listed in the reusability section. I did not read the rubric v2 (`photo-rubric.md`) itself.
- **Not checked:** whether the founder sent the reply, and when; Mark's answer.
