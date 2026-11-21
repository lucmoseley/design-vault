# mmm-infra site-look round (#8): what went wrong or was done again

⚠ **Bound 13 Oct 2026 (#94): every finding here is ruled. S1 takes no change: the critic stays before the founder's first look (#94 Q1 (B), #95). S2 goes to #113 (a client-fit project gate written at set-up); S3, S4, S5 and S8 to #109; S6 to #112 and #78; S7 to #78; S9 to #112; S10 to #114; S12 to #77. P1–P4 went to #93. S11 is workflow-core's (workflow-core#924).**

Owner of every proposed change below: #94 (which mmm-infra findings design-vault adopts) rules on each; a finding about judging a client's photos goes to #93 (photo method).

Ticket: design-vault #91. Question: where did lucmoseley/mmm-infra#8 ("What should the new mmminfra.com look like?") miss what the founder wanted, or do work again, beyond design-vault #77 and #78?

Sessions: `.claude3:631cff6d` (raw: `/home/lucmo/.claude3/projects/-home-lucmo-mmm-infra/631cff6d-e88f-4197-b29b-84f4621ba7d8.jsonl`, 5-8 Oct 2026). `.claude3:2b924dbd` (raw: `/home/lucmo/.claude3/projects/-home-lucmo-mmm-infra/2b924dbd-a1d5-4c61-af49-7abb54471191.jsonl`, 4 Oct 2026).

Line cites `L<n>` are lines of the raw jsonl. `[agent-<id>] L<n>` is a line of that subagent's jsonl.

Already filed from this session, so not found again here: #77 (round record), #78 (width sweep), #79 (precedent research before round one).

## Findings

### V0: Which method version the session ran
- **What happened:** 631cff6d loaded `design-vault:design-round` at L75. It read the skill files from `/home/lucmo/.claude3/plugins/cache/lucmoseley/design-vault/5d1f926dd769-5e689e2b/` (L83, L182, L600). That is design-vault commit 5d1f926 (5 Oct 2026 15:31 +0800, "Make the founder's craft rules a gate in every project's design rounds", lucmoseley/mmm-infra#16). The session started 13 minutes after that commit (07:44 UTC = 15:44 +0800). So the session ran the craft gate and the #14 process changes on their first day. workflow-core was v1.3.8. impeccable was 4.5.0 (L144), but the design-round guide was written against 4.2.1 (2b924dbd L157).
- 2b924dbd (4 Oct) read the skill from `~/.claude/plugins/cache/lucmoseley/design-vault/0202f1862ca3-5e689e2b/` (2b924dbd L70). That is commit 0202f18 (1 Oct). `~/.claude2/plugins` and `~/.claude3/plugins` are symlinks to `~/.claude/plugins` (commit fcb6c52), so the path is not a fault.
- **Evidence:** 631cff6d L75, L83, L600; 2b924dbd L64, L70; `git log 5d1f926 -1`.
- **Confidence:** 95% (90-99%). The cache path names the sha.


### S1: Round one went through the full craft loop before the founder made a taste read
- **What happened:** Round one (5 Oct, 07:44 to 14:07) sent about 33 agents before the founder saw a tile: 5 finish reviewers, 5 more after the first 5 stopped, 4 vault-sweep agents, 5 builders and 13 critic dispatches. Builders rebuilt v2 and v3 and fixed v1, v4 and v5. Then the founder rejected all five tiles on direction, not on craft.
- **Founder's words:** "I don't really like any of them" (631cff6d L2986). v1: "childish feel... opposite of what a C-suite trusted lawyer wants to project"; v5: "boring" (631cff6d L3017).
- **Evidence:** Dispatches at L711–L715, L871–L875, L1902–L2826. Round record issuecomment-5993040762. The session's own review on mmm-infra#8: "the critics judged craft, not direction."
- **Cost:** About 6.5 hours and about 33 agent runs on five directions that the founder then dropped. The craft fixes did not carry into round two.
- **Root cause:** design-round §2 and §5 put impeccable's finishing rows and the critics in front of the founder's first look. The method has no cheap "direction read" step (still frames or one screen per direction) before a craft pass in round one. §6 has a ladder for brand art, but a web identity round went straight to playable builds.
- **Owner of the fix:** design-vault `plugin/skills/design-round/SKILL.md` §2.
- **Already filed:** no. #79 covers precedent research before round one. #77 covers the round record. Neither covers the order "taste read first, craft pass second".
- **Proposed change:** In round one of an identity or whole-site look, show the founder one static first screen per direction, with only a width check (#78), before any finish reviewer or critic runs. Run the critic loop only on the directions he keeps.
- **Confidence:** 70% (55%–80%) that this order would have saved most of the 33 runs. It moves down if round-two data shows the critics' craft fixes changed which tiles he chose.

### S2: The critics had brand and audience signal but did not rank it first
- **What happened:** The round-one critic prompt (raw L1895, critic-common.md) asked for the craft gate, impeccable critique and audit, Gestalt, conversion, SEO, and "Answer every Client values line". It said "no project gate". A sample of the critic reports shows that critics saw the brand problems and filed them low. critic-v2c wrote "It reads as an engineering practice, not a lawyer-advisor". critic-v3 and critic-v4 wrote that the logo colour change is "Mark's call... not a defect" and "not a finding against the tile". No sampled critic flagged a childish feel (grep of r1/reviews at tag rounds/site-look-r1-v1e for childish, playful, juvenile, cute: no match).
- **Founder's words:** v3: "Mark has chosen certain colours for his logos (blues and blacks/greys) that don't seem to mesh too well with the colour palette chosen here"; v2: "too 'in-your-face techy'. He is not an engineer or architect" (631cff6d L3017). Then the standing instruction "personal expert advisor", not "the firm is the brand" (631cff6d L3206).
- **Evidence:** critic-v2c L97, critic-v3 L97 and L178, critic-v4 L112 (r1/reviews in mmm-infra at tag rounds/site-look-r1-v1e). The founder's L3206 rule became an "advisor test" that round two ran before craft.
- **Cost:** Part of S1.
- **Root cause:** design-critique has no client-fit gate that runs before the craft gate and can fail a tile. "Client values" is one list in the brief (design-round L35), answered at the end of a long report. An open brand question (logo colours) was treated as "not a defect" instead of "a fit risk to show the founder".
- **Owner of the fix:** design-vault `plugin/skills/design-critique/SKILL.md` and `plugin/skills/design-round/SKILL.md` §1 (brief).
- **Already filed:** no. #77 asks the round record to trace each candidate to the client's wishes. That is the record side. This is the critic side.
- **Proposed change:** Add a "client fit" gate as step one of design-critique: audience seniority and register, the client's own colours and marks, and any standing rule like the advisor test. A fail stops the craft review for that tile. An open client question goes into the round record as a risk, not out as "not a defect".
- **Confidence:** 65% (50%–80%) that a fit gate first would have stopped v1, v2 and v3 before the founder saw them. A full read of all 13 round-one critic reports would move it.

### S3: The critic loop had no stop rule and went down to sub-pixel findings
- **What happened:** Round two sent 7 first critics and 27 re-checks (v2: 9 re-checks, v7: 6, v4: 5, v1: 4). Each new critic found smaller things. The v2 re-checks went down to 0.5 px grid offsets, 11 px against 11.14 px lettering and Replay behaviour mid-motion. The founder chose v1 and v7. He did not choose v2 (10 critic runs) or v4 (6).
- **Founder's words:** none on the loop itself. His choice is at 631cff6d L7597.
- **Evidence:** 631cff6d L7061–L7272. The session said "Each new critic has found smaller things" near L7098. At L7272 the session said that a faulty measuring script gave figures that it had quoted to the founder.
- **Cost:** About 34 critic runs over about 19 hours of wall time. About 15 of them went to two tiles that the founder did not keep. One wrong figure went to the founder.
- **Root cause:** design-critique and design-round give no stop rule for re-checks: no cap, no severity floor (for example "stop when a pass finds no P0 or P1"), and no "show the founder first, then polish the keepers". design-round §5 says "There is no cap on rounds". That is about rounds, but no rule bounds critic passes inside a round either.
- **Owner of the fix:** design-vault `plugin/skills/design-critique/SKILL.md`.
- **Already filed:** no (searched design-vault for critic loop, convergence; workflow-core#1545 asks how many reviewer runs a code change needs, which is the same question for code, not for design).
- **Proposed change:** A re-check passes when it finds no P0 or P1. Stop at the first such pass, or after two re-checks, and list what is left as P2 in the round record. A measurement quoted to the founder comes from a script that a test or a second method has checked.
- **Confidence:** 75% (60%–85%) that a P1 floor would have cut the re-checks by half with no change to his choice. It moves down if a sub-pixel finding changed a founder verdict.

### S4: The critics had no list of stand-ins, so they judged placeholders
- **What happened:** Round-two critics did not agree on the Gelasio stand-in lettering. v1, v2 and v3 critics counted it as a breach. The session put this to the founder as Q1. Later the session polished placeholder photos (the v7 mask and lectern sign, chin crops across 682 sizes) that a real photo was to replace.
- **Founder's words:** "accept recommendation" (631cff6d L7275), which gave ruling (A): the stand-in is accepted.
- **Evidence:** 631cff6d L7275 and the round-two record issuecomment-6014665801.
- **Cost:** One founder question, repeated while he was away (see S11), and critic and builder time on art that was then thrown away.
- **Root cause:** The critic prompt did not carry a "these parts are stand-ins; do not judge them" list.
- **Owner of the fix:** design-vault `plugin/skills/design-critique/SKILL.md` (critic input), with #77.
- **Already filed:** partly, #77 (record side only).
- **Proposed change:** Add to #77: the same placeholder list goes into every critic prompt, and a critic finding against a listed stand-in is out of scope.
- **Confidence:** 80% (70%–90%) that the list would have removed the Gelasio question. The polish on placeholder photos is a judgement call; 60% (40%–75%) that the list would have stopped it.

### S5: A critic finding on one tile was not checked on the other tiles
- **What happened:** In round two, v2 failed the advisor test because Mark's name was not in the navigation (631cff6d L4763). The same gap was in v7. The session fixed v7 only later (L6185), after a v7 critic found it again.
- **Founder's words:** none.
- **Evidence:** 631cff6d L4763, L6185.
- **Cost:** One extra critic pass and fix cycle on v7.
- **Root cause:** No step says "when a critic finds a gap that comes from the brief or a shared rule, check the sibling tiles for it".
- **Owner of the fix:** design-vault `plugin/skills/design-round/SKILL.md` (critique step).
- **Already filed:** no.
- **Proposed change:** After each critic pass, sort findings into "this tile only" and "shared rule". Apply a shared-rule finding to every tile in the round before the next pass.
- **Confidence:** 60% (45%–75%). Only one clear case was found. A count across all 34 round-two critic reports would move it.

### S6: Builders drew the logo too large, and no canonical lockup existed
- **What happened:** In round two the builders made the wordmark 1.5 to 1.9 times too large in v4, v5 and v6. The session then wrote `craft/lockup.py` to measure it. In round one the v5 builder cropped the logo's crown (critic re-dispatch at L1986).
- **Founder's words:** none on the size.
- **Evidence:** 631cff6d L1986, L3869.
- **Cost:** Re-builds on three tiles and one new script, made in the middle of a round.
- **Root cause:** The brief gave builders the logo paths but no lockup asset (mark plus wordmark, fixed ratio, clear space, minimum size) and no check. Each builder set the size by eye.
- **Owner of the fix:** design-vault `plugin/skills/design-round/SKILL.md` §1 (brief): an identity round starts with a lockup sheet. The mmm-infra lockup itself is mmm-infra's.
- **Already filed:** no.
- **Proposed change:** Where a client has a logo, the brief carries one lockup file and its rules, and the width check (#78) also checks the lockup ratio and clear space.
- **Confidence:** 70% (55%–85%) that a lockup file would have stopped the size errors.

### S7: Finish reviewers got screenshots older than the pages
- **What happened:** In round one five finish reviewers started (L711–L715). They found that the screenshots were older than the pages (L807, L814). The session stopped three and sent five new ones (L871–L875).
- **Founder's words:** none.
- **Evidence:** 631cff6d L711–L715, L807, L814, L871–L875.
- **Cost:** Five agent runs lost.
- **Root cause:** No step makes the screenshots again, or checks their time against the page files, before reviewers start.
- **Owner of the fix:** design-vault `plugin/skills/design-round/SKILL.md` (render step), or the width-sweep script that #78 will add.
- **Already filed:** no. It can fold into #78: the sweep makes the screenshots, so they are new when the critics start.
- **Proposed change:** The reviewer dispatch shows each screenshot's time and each page's last change. A screenshot older than its page stops the dispatch.
- **Confidence:** 85% (75%–95%) that this check stops the same loss.

### S8: A critic made a new test outside the brief, and the result went to the founder
- **What happened:** Only the v1 critics tested a throttled 3G first visit. The test found a font-load problem. The session put Q1 to the founder (631cff6d L2749). He answered with ruling (B): font loading is a build decision, not a round decision.
- **Founder's words:** "accept recommendation" (631cff6d L2765).
- **Evidence:** 631cff6d L2749, L2765. Ruling posted at mmm-infra#8 issuecomment-5995749871.
- **Cost:** One founder question on a build matter. The test ran on one tile of five, so it did not compare the tiles.
- **Root cause:** The critic prompt did not say which tests are in scope. A critic added one, and the session did not sort "build matter" from "round matter" before it asked the founder.
- **Owner of the fix:** design-vault `plugin/skills/design-critique/SKILL.md`.
- **Already filed:** no.
- **Proposed change:** The critic prompt names its tests. A critic that finds a problem outside them writes it as a note for the build, not as a breach. A build matter does not go to the founder in a design round.
- **Confidence:** 60% (40%–75%). One case only.

### S9: The tiles dressed the page in the object's props, and earlier rounds on a sibling ticket were not read
- **What happened:** The founder liked the pad and blueprint looks better in the mmm-infra#9 animation storyboard than in the round-one tiles. The session compared them. The tiles "turned every dial up" and dressed the whole page in the object's props. The storyboard kept them quiet, as a ground.
- **Founder's words:** pad and blueprint can be saved with changes to "shades, busyness, borders" (631cff6d L3118); his better reaction to the storyboard (631cff6d L3139).
- **Evidence:** 631cff6d L3066, L3118, L3139. The session's own review on mmm-infra#8 says the tiles turned Mark's four suggested animation backgrounds into whole-site looks.
- **Cost:** Part of S1. A known good treatment from a sibling ticket was not used.
- **Root cause:** Two gaps. (1) No rule says "a client's idea for one part (an animation ground) is not a whole-site direction; keep a metaphor quiet". (2) The brief step does not read the founder's verdicts on sibling tickets of the same project.
- **Owner of the fix:** design-vault `plugin/skills/design-round/SKILL.md` §1 and §2.
- **Already filed:** partly. #79 asks for precedent research before round one (outside work). Reading the project's own earlier rounds is not in #79.
- **Proposed change:** The brief step reads every round record on the project's other tickets and copies the founder's verdicts into Client values. A direction card that comes from one client idea says which part the idea was for.
- **Confidence:** 55% (40%–70%) that this would have changed round one. It is a judgement about taste, so the range is wide.

### S10: The brief had no client-effort limits, so the round-three plan assumed a photo shoot
- **What happened:** The round-three plan assumed that Mark would do a photo shoot.
- **Founder's words:** "Mark will not be doing a photo shoot for this. He doesn't want to do any effort here." (631cff6d L7785)
- **Evidence:** 631cff6d L7785. The plan then changed to the #22 photo work in the same session.
- **Cost:** One plan thrown away. The later photo search (P1 to P4) followed from this.
- **Root cause:** The brief has no line for what the client will and will not give (time, photos, copy, approvals).
- **Owner of the fix:** design-vault `plugin/skills/design-round/SKILL.md` §1 (brief).
- **Already filed:** no.
- **Proposed change:** Add a "Client gives" line to the brief: assets on hand, assets he will make, and his time per round. A plan that needs more than the line says is a question for the founder before the plan is written.
- **Confidence:** 80% (65%–90%) that the line would have caught it.

### S11: The same question went to the founder about eight times while he was away
- **What happened:** The Gelasio stand-in Q1 (S4) was printed in about eight messages while the founder was offline for about 16 hours.
- **Founder's words:** "accept recommendation" (631cff6d L7275).
- **Evidence:** 631cff6d between the Q1 post and L7275.
- **Cost:** Turns and screen space. No wrong action.
- **Root cause:** A background wake re-posts the round.
- **Owner of the fix:** workflow-core.
- **Already filed:** workflow-core#924 (filed 8 Oct from a later session, closed).
- **Proposed change:** none here.
- **Confidence:** 90% (80%–95%) that it is the same fault.

### S12: The local preview server died during a critic pass
- **What happened:** The preview server stopped in the middle of the round-one critique (631cff6d L2440). Later the founder could not open the round links in Chrome (L7492).
- **Founder's words:** see #77 (L7492).
- **Evidence:** 631cff6d L2440, L7492.
- **Cost:** A critic re-run and a lost founder look.
- **Root cause:** Rounds are served from one localhost process with no health check.
- **Owner of the fix:** design-vault `plugin/skills/design-round/SKILL.md`.
- **Already filed:** already filed (#77), which asks for a viewing link that works.
- **Proposed change:** none beyond #77. Add to #77 that critics check the server is up before they start.
- **Confidence:** 70% (55%–85%).

### P1–P4: The #22 photo work inside this session (route to the photo-method ticket, g1)
These four are inside 631cff6d (6 to 8 Oct). The t3 session list does not include them.
- **P1: The shortlist had a duplicate.** The session showed "five" photos. Founder: "I believe 3 and 6 are the same photo" (631cff6d L8792). No dedup step. Owner: the photo method (g1). Already filed: no. Confidence 85% (75%–95%).
- **P2: An untested judgement became an ask to Mark.** Blind scorers called a clean edit "unrealistic", and the session drafted email asks to Mark from that. Founder: "Surely these tasks are trivial?" (631cff6d L8894). The session said that the judgement was not tested. Owner: g1. Already filed: no. Confidence 75% (60%–85%).
- **P3: The session reported a stalled script as running, and named a paid tool as free.** The founder found the stall (631cff6d L9084). Founder: "I thought you said this was a free tool?" about FLUX Erase, with a $10 minimum (631cff6d L9403). Owner: g1 for the photo tool list; the status report fault is general. Already filed: no. Confidence 70% (55%–85%).
- **P4: The session showed a self-checked edit, not a blind-checked one.** Founder: "you should be checking the work before me. Research how to spot bad work of this type and apply those principles to your critiques" (631cff6d L9413). After this, six rounds of blind edit critics ran, with a quality bar at L9431 and L9455. Owner: g1 (whether photo judging enters the method). Already filed: no; g1 decides it. Confidence 80% (65%–90%).
- Note: 631cff6d L9883 holds a credential. L11664 is a waiting:external mistake, already filed (workflow-core#869).

## Went well
- **The advisor test, run before craft in round two.** It came from the founder's L3206 rule. Round two found the two looks he kept (v1 and v7).
- **The voice guide.** The founder's L3225 voice note became mmm-infra#21, a voice guide that the later copy used.
- **Founder rulings went onto the ticket word for word** (issuecomment-5995749871 and the round-two reply issuecomment-6018689130), so later sessions could read them.
- **The rubric checker in the #22 photo work** found a reversed cue, a misread study and unsourced cutoffs before the scorers ran.
- **Blind scorers** (s1, s2) gave independent scores. When s2 stalled, the session resumed it and did not start again.
- **The session reviewed its own round one on mmm-infra#8** and named the cause ("the critics judged craft, not direction").
- **Self-correction at L7568** ("That was wrong. Six of the seven open with his line...") before the founder acted on the wrong claim.

## Bound
- **Read in full:** the reduced text of 631cff6d (`/home/lucmo/design-vault/.claude/tmp/dbb2d38b-reduced/631cff6d.txt`) up to the end of round two and the round-three plan, all founder lines, and the round-one critic prompt (raw L1895). 2b924dbd in full. mmm-infra#8 comments in full.
- **Sampled:** the #22 photo tail of 631cff6d (founder lines and the session's answers, tool lines skipped). Round-one critic reports: grep only, over critic-v1, v3, v4, v5b and v2c at tag rounds/site-look-r1-v1e. The 104 subagent reports: listed and counted, not read.
- **Not read:** the round-two critic reports one by one (the S3 and S5 counts come from the main transcript, not from the reports). The design-critique skill at commit 5d1f926 was not compared line by line with the current one; the current design-round and design-critique were searched for a client-fit gate, a re-check stop rule, a stand-in list for critics, a sibling sweep, a lockup rule and a screenshot age check, and none was found.
- **Tracker search:** design-vault for critic loop, convergence, stand-in, placeholder, logo lockup, client values, brand fit, screenshot stale, sibling. workflow-core for repeated questions, founder offline, re-ask, critic convergence. Overlaps found: #77, #78, #79, workflow-core#924, workflow-core#869, workflow-core#1545 (code side only).
