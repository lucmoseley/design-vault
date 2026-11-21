# design-vault #90: the founder's review of every photo score (mmm-infra#38) and the photo store after it (#23, #40-#43)

⚠ **Bound 13 Oct 2026 (#93): every finding here is ruled. P1, P2, P4–P6, W4 and W6 go to #110; P3 and P15 to #106; P10–P13 and W2 to #107; P8 and W5 to #108; P7, P16 and W3 to #111; P14 to #77. W1 and the design-round part of P13 go to #94. P9 takes no change (Mark-specific).**

⚠ **Bound 13 Oct 2026 (#94): W1 goes to #112 item 4 (the founder's rulings join the client values list the critic answers); the design-round part of P13 goes to #109.**

⚠ **Bound 13 Oct 2026 (#111): P7, P16 and W3 are built as #120, one shared, tested review page in the plugin, used by client-assets and design-round.**

Owner of every proposed change below: #94 (which mmm-infra findings design-vault adopts) rules on each; a finding about judging a client's photos goes to #93 (photo method).

Question: Where did the review of every photo score, and the photo store after it, miss what the founder wanted, or do work again? Which rubric versions fixed a misread of his taste, and which fixed a process fault? Which lessons serve any project, and which are specific to Mark?

Sources: reduced transcripts in `.claude/tmp/dbb2d38b-reduced/`, raw jsonl for drill-down, `gh issue view` on lucmoseley/mmm-infra, `git -C /home/lucmo/mmm-infra log`.

## Findings

### P1: The first review page showed copies of one photo as separate cards, and copy merges then changed three times
- **What happened:** The review page from before #38 gave each file its own card. The founder found the copies himself: C014 = C028 = C031, C002 = C013, "more duplicates". The rebuild (page v4) merged 56 files into 51 cards with SIFT and face matching. Two of those merges were wrong or disputed later. Page 15 said C070 and C047 are "two frames, not one crop". The page-15 analysis called C071/C011 "the second merge error". The v4 hand-off said C047/C070 are separate. The by-eye audit then found C047/C070 are one exposure (face correlation 0.993), and the session reversed its own hand-off ("my error").
- **Founder's words:** "We had already established photos C014, C028, and C031 are the same photo, just cropped and edited, so why are there three separate entries for it?" and "There are more duplicates that are just cropped versions of one another." (ff5a3c16 L14)
- **Evidence:** ff5a3c16 L14, L190-L338; #38 comments 6077668328, 6085170963 (C070/C047), 6092444527 cause 6 (C071/C011), 6092606904, 6092805824, 6092899941.
- **Cost:** 1 founder message of 5 points on the first page. 1 page rebuild. 3 later corrections of the copy groups. 1 background by-eye audit of all 56 files. A founder ruling (C031 at 2.5) did not bind its copies C014 and C028, so C014 sat at P #1 "as if he had not ruled" (6092444527 cause 5).
- **Root cause:** No step merged copies before the founder saw the pool. The copy groups were known ("exposure groups") but the builder used them only to explain a non-listing (ff5a3c16 L102). Copy detection had no stated test: "same exposure" against "adjacent frame" was decided by feature match, then by eye, then by correlation, with different answers.
- **Owner of the fix:** design-vault design-round (reference intake) and any review-page step.
- **Already filed:** no.
- **Proposed change:** Before the founder judges any pool, group the copies. Use one written test: "same exposure" means same pose, same mouth and same hands; a different moment is a separate photo. Show one card per exposure. Make a ruling bind every file in its exposure.
- **Confidence:** 75% (60%-85%) that this is a method gap and not a one-off. It would drop if design-vault already has a dedupe step for client photo pools; I found none in the transcripts.

### P2: The portrait score never looked at a portrait crop, and pixels earned no points, so the founder removed 7 portraits by hand
- **What happened:** R5 (pixels) measured the whole file cover-fit into the slot, not a head-and-shoulders crop. Ruling 2 (from before #38) gave pixels no points, so every score meant "good if Mark sends the original". The scorers credited "best crop" (R15) but nobody drew it. The page then showed a crop the scorers had not seen. The founder found the gap on C048 and C065. The fix went through four forms: an enlargement threshold (4.4x, then 2x), which the founder rejected; a by-eye crop check; a V2 veto at 1.5x (v4); and pixel points R5g (v4.2).
- **Founder's words:** "Does it truly have enough pixels when cropped tight enough on Mark's face to work as a portrait? Is that something you considered for all portrait candidates" (ff5a3c16 L14). "in the summary for C065 it says it could work as a portrait (even getting the #3 slot after a crop), yet the second image you supplied is far too grainy to work. If a different crop was the portrait candidate, why doesn't the document display the version I should actually be looking at?" (ff5a3c16 L1039). "A photo with loads of pixels might look great still if blown up 5x, whereas one with few might look bad blown up 1.2x ... the question is if a crop that works compositionally well for a portrait, also has enough pixels to look good at that crop size" (ff5a3c16 L1228). On page 15: "the resolution of this photo [should hold] it back ... not just because I manually reminded you" (#38 comment 6092444527 cause 3).
- **Evidence:** ff5a3c16 L131-L150, L1098-L1207, L1287; a32b107d L88-L688; #38 comments 6077668328, 6077901365, 6078248083, 6092444527, 6094370505; commits c2e8136 (v4, V2 veto), 2027cbf (v4.2, R5g).
- **Cost:** 7 portrait removals by hand (C048, C065, C054, C014, C012, C019, C018). 3 founder corrections. 1 withdrawn rule (2x). 1 successor session (a32b107d) for the crop check. 2 rubric versions (v4 V2, v4.2 R5g). At page 15, C018, a 250 x 167 px file that may not be Mark, still held banner #5.
- **Root cause:** The rubric scored the source file, not the image as the slot will render it. The "if the original arrives" score was not labelled on the page until v6. This is a process fault. It is also a taste fact: the founder judges how the crop in use looks at screen size, by eye, and not by a ratio.
- **Owner of the fix:** design-vault design-round and design-critique (any asset that uses a supplied photo).
- **Already filed:** no.
- **Proposed change:** Judge a supplied photo as rendered: the actual crop the slot uses, at the target screen size, at 1x and 2x density. Show the founder that render, not the source file. Keep an enlargement figure as context only. Keep two scores apart and label both: "the file we hold" and "if the original arrives".
- **Confidence:** 85% (75%-92%). The founder said it in his own words, and the fix took four forms over about a day and a half (9 Oct 08:19 UTC to v4.2 on 10 Oct). It would drop only if the method already says "judge at slot size"; the critique skill says nothing on supplied photo crops that I found.

### P3: An unvalidated sharpness measure raised a recommendation to 85% and then failed on the next photo
- **What happened:** To settle C048, the session measured "fine detail" (the residual from a 2 px blur). It raised the confidence of option (A) from 60% to 85% on that number. Ten minutes later the founder called C065 "far too grainy", and the measure had ranked C065 sharpest (4.30). The measure counts grain as detail. The session withdrew it. The ruling on C048 stood on the visual check alone.
- **Founder's words:** "the second image you supplied is far too grainy to work" (ff5a3c16 L1039).
- **Evidence:** ff5a3c16 L930-L947; #38 comments 6077726842 ("its only validation" is that it ranks three removals low), 6077901365 ("Correction to my last comment").
- **Cost:** 1 correction comment. No ruling changed. The risk was a confident wrong recommendation.
- **Root cause:** A new measure was validated only against the cases it was built to separate. It was then used to raise a priced confidence.
- **Owner of the fix:** design-vault design-critique (how a critic uses a metric).
- **Already filed:** no.
- **Proposed change:** A measure that was not tested on cases outside its fitting set does not raise a confidence figure. Say "by eye" where the eye decides.
- **Confidence:** 55% (40%-70%) that this needs a method line. It is one instance; it would rise if other sessions show the same pattern.

### P4: The "with a better version" rank was fixed four times, and the founder caught each fault on the page
- **What happened:** The founder asked the page to show which photos are worth chasing from Mark (page v9). The rank "with a better version" then went wrong in four ways. (1) v9 ranked each upgraded photo against every other upgraded photo, so C002 fell from #5 to #9. (2) The v11 fix did not hold for listed photos: the chip compared a list place with a rank on another scale, and the check compared two hidden numbers, so it passed. (3) Page 14 and 15 brought the fault back ("#2 of all eligible (now #2)"); the checker "had matched 0 lines since page 14". (4) The page-15 rank fix brought back the point-8 fault: "would enter the list at #5" beside "not worth chasing". Separately, the chase score added back expression "from an adjacent frame", which is a different photo (29 of 39 chased photos used that credit). Then v4 said "stays" on almost every photo, because pixels still earned nothing; v4.2 fixed that with pixel points.
- **Founder's words:** "The 'with a better version' remarks for C002 = C013 indicate it would drop positions with a better version, which makes no sense." (df4ba6a9 L260). "The fix you implemented seems not to have worked. C002 = C013 still says 'shortlist #2 with a better version: #3' ... which should be impossible" (df4ba6a9 L741). "This is a defect you said you fixed ages ago? A photo can't rank lower with an imporved version, that's non-sensical." (aaca35d8 L1795). "For C012, this makes no sense ... if it would stand #2 on the list with better quality as you say, that would make it an ideal candidate for getting a better version." (a317fdb2 L16 point 8).
- **Evidence:** df4ba6a9 L423-L438 (a mutant passed when it should fail), L756; aaca35d8 L1808-L2123; #38 comments 6079545713, 6080013456, 6085170963, 6085680704, 6092444527 cause 4, 6094116611, 6094370505; commit 2027cbf.
- **Cost:** 5 founder messages. Page versions v11, v13, 15 v2, 16 v1-v3 were each a rank fix or a rank restore. 4 checker rewrites. The chase list size moved 4 -> 31 -> 9 -> 24 -> 19 -> 21 -> 39 -> 11 -> 13 -> 16 in under a day (9 Oct 10:24 to 10 Oct 07:28 UTC).
- **Root cause:** Process. The rank rule ("only this photo improves; at worst it keeps its place") was the founder's from the start, but it lived only in a gitignored builder and was not a written invariant. Each rebuild re-derived it. The checker tested the builder's internal numbers, not the numbers the page prints, and it did not fail on a zero match count.
- **Owner of the fix:** design-vault (any review page the method builds for the founder); workflow-core for the "check what the reader sees" rule.
- **Already filed:** no.
- **Proposed change:** Write each founder rule for a review page as a numbered invariant in a tracked file before the page is built. Check every invariant against the rendered page text. A check that matches zero items fails.
- **Confidence:** 80% (65%-90%). The same fault came back three times after a "fixed" report. It would drop if design-vault never builds review pages of its own; but design-round does present candidates to the founder.

### P5: The page check tested layout, not content, so the founder found the wrong crops and cut-off images
- **What happened:** Every page publish was checked for "no page errors, no sideways scroll" at 1440 and 390 px. That check did not catch what the founder saw. Page v7 showed only the top 520 of 850 px of each portrait crop, so C001 "stopped at his nose". Page 15 showed C064's portrait "plate" as water bottles. Page 15 padded crops grey past the file edge. C016's head was cut by the file itself, and no criterion with points caught it. After v7, the session said "I did not open v7 itself in a browser after publishing".
- **Founder's words:** "something is still wrong with the artifact - it's displaying strange crops like this one (the example is C001)" (a32b107d L726). "there are weird crops being shown as the photo displays, for example this one for C064 ... Why would we want a crop just showing the water bottles?" (aaca35d8 L1795). "The C064 crop is an example - there are other strange choices for other photos. Do a full audit" (aaca35d8 summary, line 611 of the reduced file). "every version of this displayed in the artifact cuts off the top of his head, so I can't judge it" (df4ba6a9 L260 point 4).
- **Evidence:** a32b107d L726-L881; aaca35d8 L1808-L1941; #38 comments 6078325489, 6085680704 ("All 47 crops ... checked by eye on one contact sheet").
- **Cost:** 3 founder messages. 2 republishes. 1 full audit of 47 crops that the builder could have run before the first publish.
- **Root cause:** Process. The pre-publish check was mechanical. Nobody looked at each image the founder would judge, at the size he sees it, before he saw it.
- **Owner of the fix:** design-vault design-round (presenting candidates); design-critique (critic checks the render).
- **Already filed:** no.
- **Proposed change:** Before the founder sees a review page, look at every image on it at display size, on one contact sheet. Confirm each one shows the subject the card names. Record that check in the Bound line.
- **Confidence:** 80% (65%-90%). Two separate crop faults reached the founder. It would drop if the method already requires a by-eye contact sheet before a founder review.

### P6: Founder rules were lost between page rebuilds, because they lived only in a scratch builder
- **What happened:** The founder asked "Are there any other rules you managed to lose somehow? Verify this" after page 15. The audit found 8 lost rules (#38 comment 6085680704): the point-8 contention scale, C029's ruling applied to every use instead of the portrait only, C015's head-cut hold, a stale hard-coded intro, and four more. Page 16 (v4) then lost 18 features of page 15, found by a second audit (#38 comment 6094370505). One feature (clearing a mark) was not restored.
- **Founder's words:** "Are there any other rules you managed to lose somehow? Verify this" (aaca35d8 raw L1847).
- **Evidence:** aaca35d8 raw L1847, reduced L2123; #38 comments 6079046620 ("The logic ... lives only in the gitignored builder"), 6079545713 ("It lives only in `.claude/tmp/review-page/build.py`"), 6085680704, 6094370505.
- **Cost:** 2 full audits (8 and 18 items). 1 founder message. The 9 Oct session had flagged the risk twice on #38 and did not move the logic out of scratch.
- **Root cause:** Process. The page logic that carried founder rulings was gitignored scratch, then swept (P8). Each new builder (`build.py`, `build-v4.py`) started from a copy, not from a list of rules.
- **Owner of the fix:** design-vault design-round; mmm-infra (where the builder now lives in `private/`).
- **Already filed:** no.
- **Proposed change:** Same as P4: a founder ruling on how a review page reads is a tracked, numbered rule with a check. A rebuild runs the old checks before it ships.
- **Confidence:** 75% (60%-85%).

### P7: The calibration page lost the founder's typed notes and clicks, and was reported "fixed" three times before the cause was found
- **What happened:** The calibration page (artifact 145vrdu..., 10 Oct) saved answers to the artifact's `db` store. Typed notes were cut back to their first save ("This ") and portrait marks did not stick. Versions 2, 3 and 4 were each reported fixed. Each was tested in headless Chrome against a stand-in store whose data was not frozen. The real store returns frozen snapshots ("Delivered snapshots and their `data()` are frozen", db.d.ts 0.2.75). The page wrote into the frozen object, which failed silently. Version 5 copied each snapshot and passed a 66-check suite against a stand-in that freezes. The same pattern (`state[d.id] = d.data()`) was in review page 15.
- **Founder's words:** "The artifact keeps deleting text I type in, and reverting boxes at random when I click" (2ca95581 L1333). "Now even more broken. Text boxes cut off" (L1523). "You still haven't fixed this ... You repeatedly not fixing the issue while saying you did is concerning me. Do a full assessment of the document to find issues, and don't report back until you have verified everything works as intented." (L1618).
- **Evidence:** 2ca95581 L1337-L1797; #38 comments 6093066278, 6093571648; b5dc35e1 L6-L67 (the founder tested the save on page 15 himself with "ABCDDE" before he trusted it).
- **Cost:** 4 founder messages, plus 1 test message in b5dc35e1. 5 page versions. About 75 minutes (02:48 to 04:03). The founder had to redo 4 portrait marks and 2 notes.
- **Root cause:** Process. The test double did not follow the documented contract of the real store. "Passed" meant passed against the double. The page was never driven in the founder's own view, and the reports did not say so plainly.
- **Owner of the fix:** workflow-core (artifact page testing) and design-vault (any founder-review page with a feedback store). The page code now lives in mmm-infra `private/`.
- **Already filed:** no.
- **Proposed change:** Keep one tested feedback-box component for founder review pages, in design-vault `plugin/`, with its suite against a store double that freezes snapshots, echoes writes and replays stale copies. Every review page reuses it. Do not report "fixed" for a page fault until the suite fails on the old build and passes on the new one.
- **Confidence:** 80% (65%-90%). The fault cost the founder's trust ("is concerning me"). It would drop if a shared component already exists in workflow-core; I did not find one.

### P8: The pool and its source record were swept from scratch, and the email to Mark went out with re-saved photos
- **What happened:** The pool originals, `faces.json`, `facts-caption.json` and `photo-pool/manifest.json` (the only C-id to source map) lived in `.claude/tmp/`. The session-start sweep deleted them at 01:01 on 10 Oct (24-hour rule). The run files moved to `private/photo-runs/`, but the pool originals were gone. The send folder for Mark was then built from review-page copies, which the page builder had re-encoded. The session checked pixel sizes only. The founder sent the email, then saw the file sizes. Three files had the right pixels but a fraction of the bytes (radio interview 105,857 B against 451,083 B held). Six more were 1,400 px copies of 2,048 px files. Commit c36fb88 added `scripts/photo_best.py`; its first version would itself accept a higher-byte re-save or an upscale as "better" and deleted the held file first (code review, 40d5e01). #42 and #43 then re-fetched 30 files over about 6 hours, 13 through signed-in LinkedIn.
- **Founder's words:** "I'm confused again. I just checked the quality of the files in the folder you gave me ... Is this really the highest resolution copies we have of each file? These are tiny!" (80db786b L445).
- **Evidence:** aaca35d8 L2301-L2439; #38 comment 6085680704 ("Scratch loss, recovered"); e4314260 L915-L1026, L1110-L1450; 80db786b L445-L843; #42 body; commits c36fb88, 40d5e01, e3535d2, e0dc541, 7ce94e2, 2d29604, 3f6a595.
- **Cost:** Mark received degraded files that he may use as his reference. The 6 Oct method that had fetched 2,048 px LinkedIn files (`li/max`) was also lost with the scratch, so #43 re-derived it from session 631cff6d's transcript (f409e0ea L123-L203) and a LinkedIn filter blocked several child runs (76b594d7 L769). 1 founder message. 3 sessions (e4314260 part, 80db786b, #42/#43 sessions) and about 14 Chrome child runs to rebuild the store. 2 commits to fix the store script.
- **Root cause:** Process. Source material for client work was kept in a folder that a sweep deletes. Display copies (re-encoded for a review page) and held originals sat side by side with no mark of which was which. The send check compared pixel size, not bytes against the recorded source.
- **Owner of the fix:** design-vault design-project (where a project keeps client source files); workflow-core (the scratch sweep and the scratch rule); mmm-infra (already fixed by `photo_best.py`).
- **Already filed:** partly. workflow-core#1009 spares an agent's Artefact file from the sweep. Nothing covers run inputs or client source files.
- **Proposed change:** design-project gives each project a gitignored, unswept folder for client-supplied source files, with a manifest of source URL, byte count and pixel size. A review page never writes into it. Anything sent to the client is built from that folder and checked by bytes against the manifest.
- **Confidence:** 85% (75%-92%) that this serves any project that handles client files. Mark-specific only in the LinkedIn re-fetch detail.

### P9: The first draft of the second ask to Mark miscounted what was asked and "sounds a lot like AI slop"
- **What happened:** The #23 draft said four earlier asks were outstanding "in case they got lost". The founder corrected it: six were asked, Mark had said he would look, and two photos needed separate lines. A rewrite against `docs/copy/writing-to-mark.md` and the mantahostels correspondence rules cut it from about 380 to 214 words. The founder then edited it three more times himself before sending. In e4314260 he also asked for "much more concise" photo descriptions.
- **Founder's words:** "I immediately see a big flaw: we have already asked him for 6 photos, not 4, and those emails aren't lost ... Also this sounds a lot like AI slop. Do better" (80db786b L96). "The photo descriptions can be much more concise." (e4314260 L911).
- **Evidence:** 80db786b L96-L416; e4314260 L911-L1026.
- **Cost:** 2 founder corrections, 3 founder edits. 1 redraft.
- **Root cause:** The drafter stated a history fact (what was asked) from a stale #23 summary. The Mark writing guide existed but the first draft did not meet it.
- **Owner of the fix:** mmm-infra (`docs/copy/writing-to-mark.md`); the #89 sibling covers the Mark writing guide in depth.
- **Already filed:** no.
- **Proposed change:** none for design-vault. Mark-specific.
- **Confidence:** 60% (45%-75%) that it is outside design-vault's scope.

### P10: Five rubric versions in one evening chased the founder's expression rulings on the same ten faces, then the dispatcher set three of them by hand
- **What happened:** The founder's round-2 point 6 said expression is "something you consistently get wrong". v3.2 rewrote R8 (expression) to read the eyes first. Its blind run missed 5 of his rulings. v3.3 fixed those and broke two others (C070 engaged look scored 1 as "sidelong"; C054 slack mouth scored 3). v3.4 fixed those. v3.5 added his six reference faces and failed 4 rulings that v3.4 met. v3.6 put the rule's score back. C052 and C016 still "flip-flopped across blind runs" (2.5, 1, 2, 2.5), and the founder chose to have the dispatcher set them to 1. C005's face is 58 px, so the blind scorers could not read it at all; the dispatcher set that one too.
- **Founder's words:** "C055 should be penalised quite heavily for facial expression if it isn't already - that's not a good one. This seems to be something you consistently get wrong, so make sure the research you are doing to judge this in ticket 38 is more thorough - both on what makes a bad expression, and how to detect it using the methods accessible to you." (a317fdb2 L16 point 6). "I don't see much wrong with this as a dynamic portrait" (df4ba6a9 L260 point 1, C070).
- **Evidence:** a317fdb2 L214-L216 (3 research agents), L1368-L1371, L2176-L2179, L2553-L2556, L4497-L4504 (scorer dispatches); aaca35d8 L723-L730, L1087; #38 comments 6082476428, 6082697747, 6083144225, 6084289187, 6085170963; commits 7fca674, 4f406ff, 70b4bde, f450f54, 297f15d, ef2c1bd, 8d9a803, 71904ae.
- **Cost:** 5 blind runs (v3.2 to v3.6) in about 3.5 hours (scorers dispatched 13:11 UTC, v3.6 page at 16:41 UTC). 32 scorer dispatches, 4 redo dispatches, 7 reconcilers, 3 research agents, about 12 concision readers. 9 rubric or regression commits. The session hit the `~/.claude3` weekly limit and needed a rescue (aaca35d8). The page lists moved each run.
- **Root cause:** Process. Each version was written after seeing the faces it was tested on (v3.4 commit: "the bound that the rules were written after seeing the ruled faces"). The regression set was also the training set, with no held-out faces, so each fix overfit and broke a neighbour. The founder's reading of a face (eyes, engagement, "a flap under his chin") is a taste fact that written anchors did not capture at this pixel size.
- **Owner of the fix:** design-vault (a reference on scoring a client's existing assets against the founder's taste).
- **Already filed:** no.
- **Proposed change:** When a blind scorer misses a founder ruling twice on the same criterion, stop revising the rule for that item. Set the ruling, and spend the founder's time on new items near a decision line instead (the v4 calibration trigger). Keep some ruled items out of the rule-writer's sight as a held-out test.
- **Confidence:** 70% (55%-85%). The v4 approach that followed settled the lists in about 5 hours with 2 small founder pages (see Went well W2). It would drop if a sixth version had converged; the record shows the founder's choice to stop, not convergence.

### P11: The weighted score could not represent how the founder judges, so v4 replaced it with vetoes
- **What happened:** v1 to v3.6 ranked photos by a weighted average of 13 to 15 criteria. On page 15 the founder left 16 notes. 9 of the 13 cards he disagreed with traced to one cause: a fatal flaw was outvoted. A face scored 0 still reached 84.6 of 100 in the portrait, with the cut at 85.9. C062 ("should disqualify from all categories") scored 86.0 in the banner. The reverse also held: in banner and article uses, gaze and expression outvoted a strong scene (C003, C035). He chose vetoes first, then a smaller score to rank the survivors, then small calibration sets where the scores are unsure (v4). His "reasonable" face was first read as 2 of 3 (Q2 (A), v3.4 round), and a linear cost then made it C009's largest cost; he re-ruled it as 2.5 and set the bars per use: portrait 2.5 or more, banner and article out at 1 or below (Q2 (B)).
- **Founder's words:** "C062 ... should disqualify from all categories"; on C049, "This begs the question if our portrait criteria need modifying" (both quoted in #38 comment 6092444527). "Q2 B" (2ca95581 L369). Earlier, on what to chase: "even though we don't need many portraits, they must all be held to a very high standard" (df4ba6a9 L664). Standards differ by use: "portraits ... must all be held to a very high standard" (df4ba6a9 L664).
- **Evidence:** 2ca95581 L12, L369, L391; #38 comments 6092444527, 6092514101, 6092539289; commit c2e8136.
- **Cost:** This is the cause behind most of the 16 page-15 notes.
- **Root cause:** Taste structure. The founder judges by vetoes, then an overall impression, with a standard set per use. An additive score assumes every flaw can be paid for by strengths elsewhere. This is a generic fact about how he reviews, not a Mark fact.
- **Owner of the fix:** design-vault design-critique (how a critic turns findings into a verdict) and the supplied-asset reference proposed in P10.
- **Already filed:** no.
- **Proposed change:** Any score the method builds for the founder starts with per-use vetoes, then ranks survivors. Each use states its own bar. Never let a sum of strengths clear a flaw he would rule out.
- **Confidence:** 80% (65%-90%). His own choice (Q1 (A), Q2 (B)) and the 9-of-13 count support it. It would drop if other projects show him trading flaws off; the design-critique "No change for the sake of change" section already favours named deficiencies, which fits.

### P12: Reference faces shown before the read made the blind scorers more generous
- **What happened:** In the v3.4 round, the session recommended skipping anchor faces (Q6 (B), 60%). The founder chose (A) and scored six unlabelled faces of Mark. v3.5 gave scorers that ladder up front and let the ladder level win. The ladder sat above the rule in 101 of 259 rows and below it in 29. Four of his rulings that v3.4 met then failed. C016's own rule reading moved from 1 to 3, so seeing the faces first shifted the read itself. v3.6 made scorers write the rule's score before they opened any ladder face, and used the ladder only as a check.
- **Founder's words:** "accept recommendations, except Q2 A, Q6 A - which ones do you want me to look at and where do I find them?" (a317fdb2 L3689). His ladder note on face A: "his open mouth seems to be bending down, making him look like he has a flap under his chin. Usable as a last resort, but not a good expression" (a317fdb2 L3916).
- **Evidence:** a317fdb2 L3689-L3994; aaca35d8 L345-L755; #38 comments 6083144225 (Q6), 6084289187, 6084572620, 6084587460; commits f450f54, ef2c1bd.
- **Cost:** 1 blind run of 8 scorers plus 2 reconcilers wasted. About 10 minutes of the founder's time on the ladder, which did then serve as six regression lines.
- **Root cause:** Process. An anchor shown before an independent read pulls the read toward it. The ladder's value was as a held-out check, not as a guide.
- **Owner of the fix:** design-vault (supplied-asset reference; also any critic brief that shows the founder's past picks).
- **Already filed:** no.
- **Proposed change:** A blind scorer or critic records its own reading first, then compares with any founder anchor. The anchor never replaces the reading.
- **Confidence:** 65% (50%-80%). One run shows it; the mechanism is the known anchoring effect. It would rise if a design-round critic brief shows the same pull from the founder's earlier picks.

### P13: The blind scorers needed repeated repairs: leaked answers, lost images, and a wrong regression line
- **What happened:** (1) Leaks. Before #38, three of four #33 scorers saw the regression answers inside the rubric (7a2b5ca). In #38 the scorers' copy still pointed at the audit files that hold his verdicts (0afa79e, code review spec finding F3). v3.3's "Why" line sent scorers to #38 (70b4bde). v3.5 scorers saw C009's expected answer in a commit subject, so v3.6 barred `git` and `gh`. (2) Lost images. In the v3.3 run the image limit removed the images for C001 to C006 and C029 to C051 from two scorers ("media removed: request limit"). Rows written without images were discarded and 4 redo agents ran. One scorer wrote "eyes appear centred" where it could not see the irises. (3) A regression line was wrong: line C017 demanded the lighting lift alone and failed a correct score (305e945). (4) A reconciler died after 10 of 16 keys and a fresh one did the rest.
- **Founder's words:** none; the founder did not see these faults.
- **Evidence:** a317fdb2 L1579, L2246-L2328, L2462, L4683; aaca35d8 L133, L641 ("The message names no photo and no score, because every scorer's starting context includes the recent commit messages"); #38 comments 6082697747, 6084587460; commits 7a2b5ca, 0afa79e, 70b4bde, 305e945.
- **Cost:** 4 redo scorers, 1 extra reconciler, 3 leak-fix commits, 2 code-review dispatches. Blindness of C009's line stayed "exposed" for two runs.
- **Root cause:** Process. A subagent's start context includes recent commits and the repo, so "blind" needs more than a cut rubric. A scorer that loses its images does not stop.
- **Owner of the fix:** workflow-core (subagent dispatch: start context and image budget); design-vault design-round §4 (the fresh critic brief).
- **Already filed:** no for the image loss; the leak checks are fixed in mmm-infra's `scripts/scorer-rubric.py`.
- **Proposed change:** A critic or scorer brief requires the agent to state, per item, that it saw the image, and to stop if an image is missing. Commit messages that land a test answer name no item and no score (aaca35d8 already did this).
- **Confidence:** 60% (45%-75%) for the design-vault part. The fresh critic in design-round looks at rendered candidates, so a silent image loss could pass a candidate the critic never saw.

### P14: Questions to the founder hid what to review, or left out what a photo competes against
- **What happened:** Several founder turns went on getting the review set up, not on judging. The founder asked for the cut-off numbers the page did not show. He asked how the event limit works after only C049's case was answered. He did not understand a priced question about how lists are built. The close-calls question first came as a three-option text block. When the page came, C009's tie card did not show the photo it tied with. Each was fixed at once.
- **Founder's words:** "What are the cut-off numbers for the different categories ... I'm seeing some photos with very high scores but 'below the cut' marked." (df4ba6a9 L7). "You never explained how the 'event limit' tag works" (df4ba6a9 L826). "I don't really understand Q1 ... Explain the question and why I would choose each option better." (2ca95581 L369). "You've buried the lead. Show me what you want me to review in C and I'll review it for what you tell me to" (e4314260 L187). "I already can't answer the question for C009 because you don't show me the photo it's competing against" (e4314260 L429).
- **Evidence:** df4ba6a9 L7-L247, L826-L830; 2ca95581 L369; e4314260 L176-L520; f409e0ea L420 ("The question is missing context. What's going on", on #43).
- **Cost:** 6 founder messages. 3 page republishes.
- **Root cause:** Process. A review page or question showed a verdict without the number or the rival that makes it judgeable.
- **Owner of the fix:** design-vault design-round §3 and §The round record.
- **Already filed:** partly, #77 (the round record says how to view each candidate and what to judge). #77 does not cover "show the rival" or "show the threshold beside the verdict".
- **Proposed change:** Fold into #77: every verdict the founder is asked to check shows the threshold it was measured against, and every comparison question shows all sides on one screen.
- **Confidence:** 70% (55%-85%).

### P15: The client email and the rubric disagreed on the same photo, and only the founder noticed
- **What happened:** The #32 email to Mark said "The radio interview further down works well" (C003). The v3.1 rubric scored C003 low as a banner (79.8): it charged the interviewer as a rival subject, and later capped the profile face at 1. The founder asked why. v3.2 changed the second-face rule; v3.5 lifted the profile cap in banner and article (Q5 (B)); C003 rose to 86.8, tied at the banner line, and the founder said yes to it on the close-calls page (v4.3). C009 had the same split: praised in #32, low in the rubric.
- **Founder's words:** "Your criticisms of C003 as a banner image seem mis-guided. For something as wide as a banner, why would two subjects be a problem? Did the research truly indicate that? ... We also praised this photo in our recent email to Mark analysing his current website and it's photos, yet here you don't rate it well. Why the discrepancy and how does that reflect on how we score?" (a317fdb2 L16 point 10).
- **Evidence:** a317fdb2 L16, L362; #38 comments 6083144225 (C003 section), 6085170963, 6095119721.
- **Cost:** 1 founder point. Part of the v3.2 and v3.5 changes.
- **Root cause:** Two judging tracks (the prose critique for the client and the numeric rubric) ran on the same photos with no check that they agree.
- **Owner of the fix:** design-vault design-critique.
- **Already filed:** no.
- **Proposed change:** Where the method holds two verdicts on one item (a prose verdict and a score, or two critics), list the items where they disagree and settle each before the founder sees either.
- **Confidence:** 55% (40%-70%). One clear case and one similar (C009).

### P16: Large single-file review pages cost about 80 chunked reads and several compactions to republish, and split across six links
- **What happened:** Each review page was one HTML file of about 556 KB and up to 881 lines; the live page read in ff5a3c16 came to 167,347 tokens (L626). The Artifact tool refuses a republish until the session reads every line of the live source. Five sessions made 78 chunked reads of saved artifact source (ff5a3c16 11, a32b107d 19, e0962be8 14, df4ba6a9 14, a317fdb2 20) and hit 8 publish refusals. Four of the 9 Oct sessions compacted during or just after such a read. Page 16 became a new artifact "because updating page 15's URL needed a 650 KB read past this session's ceiling". Page 15 became a new artifact because the rescue session ran on a different account. In all, the founder had six links: Widmsy2 (pages 1-14), G1hSZ (15), 3WeUo (ladder faces), 145vrdu (calibration), 7esS6 (16), 5JBJn (close calls). Notes left on one page stay on that page.
- **Founder's words:** none on the cost.
- **Evidence:** a32b107d L405-L604; e0962be8 L300-L444; df4ba6a9 L100-L234; a317fdb2 L2967-L3263; #38 comments 6085170963 ("The page 14 link was published from the `~/.claude3` plan's account"), 6093995217 ("650 KB read").
- **Cost:** About 80 tool reads and 4 compactions of context. 2 new links the founder had to switch to.
- **Root cause:** Process. The page held its data inline, so every data change was a full-page change.
- **Owner of the fix:** design-vault (a shared review-page shell, with P7's feedback component).
- **Already filed:** no.
- **Proposed change:** Build founder review pages as a small HTML shell plus a data file (JSON) and image files published through `files`. A data update then republishes only what changed. Keep one link per review across rebuilds, and publish from the account the founder views in.
- **Confidence:** 60% (45%-75%). I have not tested whether the Artifact read rule applies to a changed data file in the same way as to the page; if it does, the saving is smaller.

## Rubric versions v3.2 to v4.3: taste or process

The rubric went from v3.2 (9 Oct 21:08, +0800) to v4.3 (10 Oct 15:27, +0800): 9 versions and 7 fix commits in about 18 hours of commit time. Earlier versions (v1 to v3.1) belong to sibling #89. "Taste" means the version fixed a misread of what the founder wants. "New ruling" means it applied a founder answer the method asked for on purpose. "Process" means it fixed a fault in the method, the tools or an earlier version.

| Version / commit | What it fixed | Kind | Evidence |
|---|---|---|---|
| v3.2, 7fca674 | Expression read on the eyes, not the mouth; a second face costs only if it competes; removable text scored as removed; recent dates rewarded; head cut by the file holds the photo; event limit 3; chase every photo in contention | Taste (founder's 10 points, a317fdb2 L16) | #38 comment 6082476428 |
| a970440 | Where the eye and mouth crops split | Process (tooling) | commit message |
| 0afa79e | Scorers' copy pointed at the files with his verdicts | Process (blind leak) | a317fdb2 L1579 |
| v3.3, 4f406ff | v3.2 run missed 5 of his faces: mild eye signs outweighed by a speaking mouth | Taste (same misread, second try) | #38 comment 6082476428 |
| v3.4, 70b4bde | v3.3 over-corrected: an engaged look at a listener scored as shifty; a slack open mouth scored 3 | Process (over-fit by v3.3), on a taste criterion | #38 comment 6082697747 |
| 305e945 | Regression line for C017 demanded the wrong fix | Process (regression set error) | commit message |
| v3.5, f450f54 | Risky text judged as if removed; no profile cap in banner and article; six reference faces as a ladder | New rulings (Q3, Q5, Q6) | #38 comment 6083319908 |
| 297f15d | v3.5's ladder step contradicted the portrait cap | Process (internal conflict) | commit message |
| v3.6, ef2c1bd + 8d9a803 | Ladder made scorers generous and failed 4 rulings; rule score restored, reconciler bounded | Process (P12) | #38 comments 6084289187, 6084662030 |
| 71904ae | Dispatcher sets C052 and C016, as blind runs split | Process (stop iterating, P10) | aaca35d8 L1087 |
| v4, c2e8136 | A fatal flaw was outvoted by a weighted average; vetoes first; per-use expression bars; two scores per use; rulings bind every copy | Taste, structural (P11) | #38 comments 6092444527, 6092539289 |
| v4.1, ab60e02 | Calibration answers bind the lists; V6 (rejected for a use); V7 (studio headshot off the article image) | New rulings | #38 comment 6093995217 |
| v4.2, 2027cbf | Pixels earn points per use; each original-fixable cost has a cause; "stays" on almost every card | Process and taste: Ruling 2 (pixels earn nothing) was wrong for his eye (P2) | 2ca95581 L2863 |
| v4.3, f1c7e44 | Close-call answers; a yes asks Mark even past the chase line | New rulings | #38 comment 6095119721 |

Summary: 3 versions fixed a real misread of his taste (v3.2, v3.3, v4), and v4.2 fixed a mixed one. 3 applied rulings the method asked for (v3.5, v4.1, v4.3). The rest (v3.4, v3.6 and 7 fix commits) fixed process faults, most of them faults of the previous version.

## Went well

### W1: Each founder disagreement became a regression line, and a failing run was held back from him
- The regression set grew from 32 lines to 91. Every run was checked against it before a page went to the founder. The v3.5 run failed 4 lines and was "held back from the review page" (aaca35d8 L345), so he never judged a page that broke his own rulings. Mutation tests proved each new line could fail (#38 comments 6092899941, 6093995217, 6095119721).
- design-vault has no such step. A round's brief delta records his choice, but nothing re-checks a later round against his earlier rulings.
- **Proposed change:** design-round keeps the founder's rulings for a brief as a short list of checks, and the critic runs them on every later round. Owner: design-vault design-round §4. Confidence: 65% (50%-80%).

### W2: Calibration on close calls only settled the lists in hours
- v4 sent the founder only the items where his answer could change a list: critics 1 point apart on a veto criterion, or a photo within 3 points of a cut. The calibration page held 31 questions; the close-calls page held 6. The founder chose the close calls over a full 52-card review (e4314260 L176, option (C)). v4 to v4.3 took about 5 hours.
- **Proposed change:** where the method asks the founder to review many items, it first lists the items whose answer can change the outcome, and asks about those. Owner: design-vault design-round §3. Confidence: 70% (55%-85%).

### W3: Feedback boxes on the review page, read back with ArtifactData
- Once the frozen-snapshot fault was fixed (P7), the founder left 16 notes on page 15 and 31 answers on the calibration page, and the next session read them directly. This replaced long chat messages (his round-1 and round-2 feedback came as 7 and 10 numbered points in chat).
- **Proposed change:** keep the tested component (P7) and use it for design-round reviews too. Owner: design-vault. Confidence: 60% (45%-75%).

### W4: Treating each founder note as a symptom found the structural cause
- The founder asked for it: "For every issue I bring to light, don't just check how to fix it in the example I called it out in - see if it applies elsewhere too and address the wider issue." (a317fdb2 L16). The page-15 analysis grouped his 16 notes into 7 causes and measured each over all 51 shots (#38 comment 6092444527). That found the weighted-average fault (P11), which no single note named.
- **Proposed change:** design-round §3: when the founder gives feedback on named items, group the notes by cause and measure each cause across every item before fixing any one. Owner: design-vault. Confidence: 75% (60%-85%).

### W5: The byte-exact best-held store
- `scripts/photo_best.py` (c36fb88, hardened in 40d5e01) keeps one exact file per photo, refuses a worse copy, keeps replaced files in `superseded/`, and builds send folders from the store. #42 and #43 filled all 56 entries as exact.

### W6: Judging the crop by eye at 1x and 2x matched every earlier ruling
- The a32b107d crop check rendered each portrait crop on a 1440 x 900 laptop at 1x and 2x and judged it by eye. Its verdicts matched all four of the founder's earlier removals (#38 comment 6078248083), and he accepted the next three removals on it.

## Lessons for any project, and lessons specific to Mark

**For any project's design work** (founder taste or process, not Mark's face): the Proposed change of P1, P2, P4–P8, P10–P16, W1, W2 and W4, with P11 (vetoes per use, then an overall impression) first.
- "me asking a question doesn't mean I think you're wrong, it means I want to dig deeper" (df4ba6a9 L260): a question from him is not an instruction to change.

**Specific to Mark's photos** (stay in mmm-infra's rubric):
- His expression reads on the eyes; an engaged look toward a listener is good; a slack or downturned open mouth is poor ("a flap under his chin", a317fdb2 L3916).
- A profile face is fine in a banner or article image, not in the portrait.
- A plain studio headshot is "too boring for an article" (#38 comment 6093995217).
- Removable text and logos are judged as if removed, and scrutinised for whether they detract; organiser overlays are asked of Mark as clean files.
- A second person in a wide banner costs only if the eye goes to them.
- Recency is rewarded; no visible date is neutral.
- Event limit 3; chase list capped near 16; per-use need P 3, W 3, A about 4.
- The LinkedIn 2,048 px fetch method (#43) and the Chrome profile pairing (now in the machine notes).

**Answer to map #87's open question** ("whether the design round needs a stage, or a separate skill, for ... a client's photos ... a review page with feedback boxes"): yes, on this evidence. design-round §6 has no asset class for choosing and preparing a client's existing assets, and mmm-infra built that method from nothing over #22 to #43. I propose one reference file, `plugin/skills/design-round/references/supplied-assets.md`, with: copy grouping (P1), render-in-slot judging (P2), vetoes then rank (P11), two scores (held file, original), close-call calibration (W2), founder-ruling checks (W1), a byte-exact store (P8, W5), and a chase list sized by per-use need. Plus one shared review-page shell with the feedback component (P7, P16), used by this asset class and by ordinary rounds. Confidence: 65% (50%-80%); it would drop if no other project expects to work from client-supplied photos.

## Out of scope here (owner named)

- **workflow-core:** the successor launcher failed on a multi-line opening prompt (ff5a3c16 L1287; the hand-off route was later retired, workflow-core#1200). The cross-plan rescue (aaca35d8) filed workflow-core#1145 and #1146.
- **mmm-infra:** the regression file gathered a history sentence per version and needed two concision tickets (#39, #41; 1ed6a869). `scorer-rubric.py` needed about nine edits per version until #40 (3d9de6be). The C030 V2 rule gap is open on #23.

## Bound

- **Read in full:** the reduced transcripts of ff5a3c16, a32b107d, e0962be8, df4ba6a9, b5dc35e1, 3d9de6be, 1ed6a869, 1211fdb3; every FOUNDER line in all 15 named sessions; every ASSISTANT and ERR line of a317fdb2, aaca35d8, 2ca95581 (lines 424-600 and all founder turns), e4314260, 80db786b, 76b594d7, f409e0ea. All 47 comments on mmm-infra#38. The bodies of #23, #38, #39, #40, #41, #42, #43. The full commit messages of the 13 rubric commits. design-vault `plugin/skills/design-round/SKILL.md` §3 to §6 and `design-critique/SKILL.md` §2 to §4. design-vault #77, #78, #87, #89.
- **Sampled:** 2ca95581 outside lines 424-600 (assistant lines only through the summaries); the #23, #40-#43 comment files (fetched, read in part); raw jsonl only at aaca35d8 L1847.
- **Skipped:** the 21 one-prompt Chrome children of 10 Oct (the `~/.claude2/projects/-home-lucmo-mmm-infra*` sessions of that day whose first prompt starts "Task:" or "Call the Chrome tool"). I used the #42 and #43 parent sessions' account of them. Subagent transcripts (scorers, reconcilers, critics) were not opened; their counts come from the parent's Agent calls. The page-15 founder notes were read through the session's analysis comment, not the artifact store.
- **Not verified:** whether the Artifact read rule applies to a changed data file (P16). Whether design-vault has a dedupe or held-out practice outside the three SKILL.md files.
- **Cost counts** (dispatches, reads, compactions) come from `grep` over the reduced transcripts and may miss calls the reducer trimmed.
