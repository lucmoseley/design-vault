# design-vault #92: how well the setup, library and research-first steps served mmm-infra

⚠ **Bound 13 Oct 2026 (#94): every finding here is ruled. S1, S4, S7, W1, the #21 voice line and the research-landing convention go to #113; S3 to #112 item 1; S2 and S5 to #79; S6 to #75. W2–W5 take no change. The hosting research, the voice-guide humour line and the doc-map gate go to their owners on map #87's Out of scope list.**

Owner of every proposed change below: #94 (which mmm-infra findings design-vault adopts) rules on each; a finding about judging a client's photos goes to #93 (photo method).

Question: how well did design-vault's setup, library and research-first steps serve mmm-infra, from the map chart (mmm-infra#1) to its first design round? Map: design-vault #87. Brief: `.claude/tmp/dbb2d38b-brief.md`.

Language: ASD-STE100 Simplified Technical English.

Transcript paths: `.claude3:<id>` is `/home/lucmo/.claude3/projects/-home-lucmo-mmm-infra/<id>*.jsonl`. `L<n>` is the line in that raw jsonl.

## Summary

- Setup worked. `design-project` registered mmm-infra in one session with no founder correction (W1), and every vault release reached mmm-infra within about a minute (W4).
- The library did not serve Mark's site. No step judged the whole library for a new client, so the founder had to ask (S1). Once judged, the library held no on-brand entry for a development-bank advisor, and round one's library seeds matched layout, not audience (S2, folds into #79).
- Research-first worked for the method but leaked at one hand-off. mmm-infra#14 was the vault's job and fed the vault the same morning (W3), but its advice against one-direction-per-reference never reached `design-round` (S3). mmm-infra#21 was the project's job (see "Whose job").
- Smaller faults: design mode switched on without impeccable installed (S4), a random roll filled an unseeded direction (S5), two sessions read a stale plugin build (S6), and each vault write needed a fresh founder sanction (S7).
- New tickets proposed: S1, S3 (or fold into #79), S4, S7, plus the W1 screenshot step and the #14 research-landing convention. S2 and S5 fold into #79; S6 folds into #75.

## Findings

### S1: The method has no step that judges the whole library for a new project; the founder had to ask for it
- **What happened:** `design-project` (mmm-infra#6, session 44ca65d8) registered mmm-infra and judged only Mark's four named sites. The design-round method judges an entry for a project only when a brief cites it (§1a). On 5 Oct the founder asked which ticket held the library-fit work. No ticket held it. Session 30b6bc74 posted the sweep onto mmm-infra#8 as a scope comment. The founder then pasted an instruction into the running #8 session (631cff6d) by hand. That session sent four sweep readers over the 92 unjudged entries (631cff6d L1301-L1326). The result was 32 adapt, 60 off-brand, 0 on-brand, written to the vault as design-vault `ccaf491` (631cff6d L1438, L1481).
- **Founder's words:** "I imagine part of the work for picking a visual direction for mmminfra.com will involve analysing which pre-existing entries in the design vault are compatible with the type of site we're building and Mark's stated preferences. Which ticket currently holds that effort?" (30b6bc74 L8). Then: "Okay, and will 8 pick this up given that it's already running now that you've added that in? Should I tell it in the session to check the ticket?" (30b6bc74 L92). Then: "I did A, with your add-on line" (30b6bc74 L153).
- **Evidence:** 30b6bc74 L68, L87 ("The round method only judges an entry for a project when a brief cites it. It never sweeps the library."); mmm-infra#8 comments issuecomment-5990791290 and issuecomment-5990816659; 631cff6d L1301-L1481, L1612; design-vault `ccaf491`. Today `plugin/skills/design-project/SKILL.md` §5 still says "`fit` — leave it out. The first brief that cites the entry judges it". `plugin/skills/design-round/SKILL.md` has no sweep step (grep for `sweep|unjudged|whole library` finds only §1a line 48).
- **Cost:** 3 founder messages and one hand paste into another session. 4 sweep subagents, about 5 minutes of wall time. The sweep came late: round one had already started its references, so the #8 session re-picked three tiles' seeds mid-round (631cff6d L1612).
- **Root cause:** `design-project` treats library fit as a lazy, per-citation step. That works for Manta, whose library was built for it. For a new client the library was built for another project, so a round-one pick from unjudged entries has no fit data to pick from.
- **Owner of the fix:** design-vault `plugin/skills/design-project/SKILL.md` (a new step after §5) and `plugin/skills/design-round/SKILL.md` §1 (round one cites only judged entries).
- **Already filed:** no. #79 is near but different: #79 adds precedent research outside the library; this finding is about judging what the library already holds.
- **Proposed change:** add a step 5a to `design-project`: "Judge every library entry for the new project against its rules file. Split the entries into batches for subagents. Each reader opens the screenshot and writes `fit.<key>` in the vault's shape. Review the adapt and on-brand takes, then write them in one commit." Add to design-round §1: "Round one cites only entries with a `fit.<project>` block. If fewer than three entries are on-brand or adapt, say so and run the precedent step (#79)." Keep the per-citation judge in §1a for entries ingested later.
- **Confidence:** 80% (70%-90%) that the step is worth adding. It drops if the founder wants the sweep only on request, because a sweep of 96 entries costs about 4 subagent runs each new project.

### S2: The library sweep found no on-brand entry, and its "adapt" picks matched by layout, not by audience
- **What happened:** The sweep gave 0 on-brand and 36 adapt verdicts for mmm-infra (today's `data/gallery.json`: 36 adapt, 60 off-brand). Round one took three adapt entries (`site-kellywallace`, `prompting-company`, `dualite`) as seeds, each for a layout that fit one of Mark's four background ideas. The founder rejected all five tiles.
- **Founder's words:** "I don't really like any of them. How were these arrived at? Explain how the briefs and references that Mark gave, alongside analysis of the industry and purpose of the site, led you to choose these" (631cff6d L2986).
- **Evidence:** 631cff6d L3013: "The library references matched by layout, not by fit. A startup landing page, an illustrator's shop and an AI tool's homepage were picked because their arrangement fit one of Mark's ideas, not because they look like an advisor to development banks." The precedent sites found after that (mmm-infra `docs/research/site-look-precedent.md`) were never ingested: the vault holds only Mark's four entries with `project: mmm-infra`.
- **Cost:** one full round one (five builds, their critics, one founder review). That cost is already counted under #79.
- **Root cause:** the vault holds mostly hostel, startup and portfolio sites (seeded for Manta and from `taste-vault`). It has no entries for a senior professional-services audience. Zero on-brand verdicts was a signal that the library could not seed round one, and nothing in the method acts on that signal.
- **Owner of the fix:** design-vault `plugin/skills/design-round/SKILL.md` §1 and §2, plus the library (`data/gallery.json`).
- **Already filed:** mostly yes (#79). #79's proposed change already includes "ingest the strongest into the library". This finding adds two facts to #79: the sweep gave 0 on-brand, and the precedent sites were not ingested after round two, so the library is still empty for this field.
- **Proposed change:** fold into #79. Make the trigger measurable: run the precedent step when the sweep (S1) gives fewer than three on-brand entries. Make the ingest of the precedent sites a check of that step, not an option.
- **Confidence:** 75% (60%-85%) that the 0 on-brand count was a usable early signal. It drops if the founder says adapt entries are the normal seeds for a new client.

### S3: mmm-infra#14 told the method not to make one direction per reference; that advice did not reach design-round
- **What happened:** The design-process-order research (mmm-infra#14, session 44d000b9) found that the sources carry a client's references as one shared list of likes, dislikes and reasons that binds every direction. Its short answer says: "Do not turn each site into one direction of one asset." The pointer comment to #16 carried only §7's seven numbered changes. #16 adopted all seven (design-vault `5d1f926`), including the client-values field. The §5/§8 advice on seeding was not in §7, so nobody put it to the founder. `design-round` §1 still says "each cited entry seeds its own direction, and a direction without one is invented". Round one of #8 (631cff6d) then seeded one tile per background idea and per library layout. The founder rejected all five.
- **Founder's words:** "I don't really like any of them. How were these arrived at?" (631cff6d L2986). The session's answer: "I took the shortcut of turning Mark's four background ideas straight into four tiles" (631cff6d L3013).
- **Evidence:** mmm-infra `docs/research/design-process-order.md` §5.1, §8 ("References: carry the reasons ... as one shared list that binds every direction ... Do not turn each site into one direction of one asset"); 44d000b9 L304 (the pointer comment to #16 names only §7); mmm-infra#16 founder ruling comment, 5 Oct 07:27Z (Q1 lists the seven changes only); design-vault `plugin/skills/design-round/SKILL.md` line 34 today. The seed-per-reference rule came from design-vault `07d05b1` and `71cf3ef` (30 Sep), made for Manta so that five picks give "five distinct directions rather than one blend".
- **Cost:** part of the cost #79 counts (round one: five builds, critics, one founder review). No extra cost of its own.
- **Root cause:** a research hand-off that forwards only the numbered proposals loses advice written in other sections. Also, two rules now sit side by side in design-round §1 and pull against each other: "Client values ... every direction answers each line" and "each cited entry seeds its own direction".
- **Owner of the fix:** design-vault `plugin/skills/design-round/SKILL.md` §1 (Reference field) and §2 (direction card Evidence). Put the conflict to the founder first, because the seed rule was his ruling for Manta.
- **Already filed:** no. #79 is about a precedent step before round one. It does not name the seed rule or #14's advice. Fold this into #79 or file it beside it.
- **Proposed change:** ask the founder one question: "Should a round-one direction come from one reference, or from the client-values list with references as evidence?" If the second: change §1 Reference to "Round one cites none to five entries as evidence. Each direction answers the client-values list. A direction may take a cited entry as its seed, but a direction is never only a match to one reference's layout." Also add to the research-landing step in the vault's own docs: a research note that proposes method changes lists every proposal in one numbered section.
- **Confidence:** 65% (50%-80%) that the seed rule was a real cause of round one's rejection and not only the missing industry research. The session's own account names four causes; this is one. It moves up if round two (seeded from precedent research, not one-per-reference) is the reason the founder found winners.

### S4: `design-project` turned design mode on, but impeccable was not installed for the new repo, so the first #8 session rendered nothing
- **What happened:** `design-project` step 3 ran `design-mode.sh on` (44ca65d8 L272, L286). That wrote `impeccable@impeccable: true` into mmm-infra's `.claude/settings.json`. The impeccable plugin was installed only at project scope for mantahostels in all three config dirs. The first #8 session (2b924dbd) loaded design-round, found impeccable missing, and stopped, as design-round says it must. It installed impeccable at user scope in all three config dirs and asked the founder to restart.
- **Founder's words:** none.
- **Evidence:** 2b924dbd L86-L133, L145-L157 ("design mode was already switched on for this repo. But in all three of your config folders ... the tool was installed only for the mantahostels project, so it never loaded here"). `design-project` §6 told the founder "Design mode is on from his next session here", which was false. workflow-core `scripts/design-mode.sh` lines 66-73 (v1.3.10) say `on` "writes `true` and reports success with nothing telling the operator the plugin itself is still missing (mantahostels#3233)".
- **Cost:** one session (about 2 minutes, 1 founder command) and one restart. Low, because #8 was then blocked on #16 anyway. The install also moved impeccable from 4.2.1 to 4.5.0, and the session flagged that the design-round map was written against 4.2.1.
- **Root cause:** `design-project` step 3's check tests only that the commit is pushed and `settings.local.json` is ignored. It does not test that impeccable will load.
- **Owner of the fix:** design-vault `plugin/skills/design-project/SKILL.md` step 3. workflow-core owns `design-mode.sh`, which knows of the gap and does not check.
- **Already filed:** no (searched workflow-core for "impeccable installed user scope" and "design-mode install"; workflow-core#125 is a closed, different fault).
- **Proposed change:** add to step 3's check: "`installed_plugins.json` in `$CLAUDE_CONFIG_DIR` (and in each config dir the founder runs) lists `impeccable@impeccable` with `scope: user`. Where it does not, install it at user scope and set the user-level key to `false`."
- **Confidence:** 85% (75%-95%) that the check would have stopped the lost session. It will not recur on this machine, because the install is now user scope everywhere. It matters for a new config dir or a new machine.

### S5: The one round-one direction no reference seeded came from a random roll, and the roll skipped the session's own best idea
- **What happened:** `references/impeccable.md` tells round one to run impeccable's `concept-seed` once and use "its assigned direction and challengers" to "fill the directions no reference seeds". In 631cff6d the session ran `concept-seed --scope direction --mode persuade` (L213). The roll gave v3 (carved stone). The founder called v3's text and palette childish and off his father's logo colours.
- **Founder's words:** "v3: The font and phrasing of this text box are childish ... Also Mark has chosen certain colours for his logos (blues and blacks/greys) that don't seem to mesh too well with the colour palette chosen here" (631cff6d L3017).
- **Evidence:** 631cff6d L139, L213, L1606 ("The roll seeded one direction only. v3 took it"); L3013: "My own idea list put 'the development-bank report style' first, and the random roll skipped it." design-vault `plugin/skills/design-round/references/impeccable.md` line 21.
- **Cost:** one of round one's five tiles. Inside #79's count.
- **Root cause:** the method fills an unseeded direction by chance, not from the client's audience or field. Where the library has no fit for the client (S2), more directions are unseeded, so chance carries more of round one.
- **Owner of the fix:** design-vault `plugin/skills/design-round/references/impeccable.md` (the Round one row).
- **Already filed:** no. Related to #79, which would seed round one from precedent research and so leave fewer directions to the roll.
- **Proposed change:** in the Round one row add: "Where precedent research (#79) exists, seed the unseeded directions from it first. Use `concept-seed` only for directions that neither a judged reference nor the precedent note seeds."
- **Confidence:** 50% (35%-65%). One tile is thin evidence. It moves up if round two, which had no roll, shows the founder judged its tiles better for that reason.

### S6: Two sessions read an old build of the plugin, because they found it by sorting the cache folder by name
- **What happened:** The plugin cache holds 13 old builds of design-vault, named by sha. Session 30b6bc74 ran `find ~/.claude2/plugins/cache -path '*design-round/SKILL.md' | sort | tail -1` (L63). That picked `c6529a659a34` (29 Sep). The installed build was `0202f18`. The session told the founder that a round-one brief "cites one to three entries, or none" (L87). The installed build said "none to five". Session 4226ac58 did the same with `ls -d .../design-vault/*/ | tail -1` (L131) and got `fa85e44` while `d0a276d` was installed.
- **Founder's words:** none. He did not see the error.
- **Evidence:** 30b6bc74 L63, L87; `git show c6529a6:plugin/skills/design-round/SKILL.md` line 28 ("one to three entry ids"); `git show 0202f18:plugin/skills/design-round/SKILL.md` line 32 ("none to five"); 4226ac58 L131; `~/.claude/plugins/installed_plugins.json` (user scope at `d0a276d`).
- **Cost:** none measured. The wrong number did not change the advice (no sweep step exists in either build). The risk is larger: a session that reads a stale build for a rule that did change would act on the old rule.
- **Root cause:** a session outside a skill load has no named route to the installed build. Sha folder names do not sort by date.
- **Owner of the fix:** design-vault `plugin/skills/design-project/SKILL.md` step 3 (the CLAUDE.md line it writes) and README §Releasing. #75 is the same class of fault for `check-curves.js`.
- **Already filed:** partly (#75 covers one script path, not the cache-sort fault).
- **Proposed change:** fold into #75. Make the CLAUDE.md line that `design-project` writes also say: "The installed build is `jq -r '.plugins[\"design-vault@lucmoseley\"][] | select(.scope==\"user\") | .installPath' ~/.claude/plugins/installed_plugins.json`. Never pick a build by sorting the cache folder."
- **Confidence:** 70% (55%-85%) that a named route stops the guess. Two sessions guessed by sort (30b6bc74, 4226ac58). Session 454739af read the vault's source tree instead (L193). Session 631cff6d listed every build by glob (L7725, L8967).

### S7: Each write a project session makes into the vault needs a fresh founder sanction, so the method's own vault writes cost him a question each time
- **What happened:** The method writes into the vault from a project's session: `design-project` §4-§5 and `design-round` §1a step 3. workflow-core's write-scope rule says a session writes only its own repo unless the instruction names the surface. So the charting session asked the founder to sanction the vault write for #6 (454739af L151, Q5). The library sweep needed a second sanction (30b6bc74 L120 Q2, L141), which the founder had to paste by hand into the running #8 session.
- **Founder's words:** "Q5 A" (454739af L189); "I did A, with your add-on line" (30b6bc74 L153).
- **Evidence:** 454739af L151 Q5 ("This writes to `lucmoseley/design-vault`, which is outside this repo, so I need you to approve it by name"); 30b6bc74 L87 ("#1 only sanctioned that for #6 and #16, so you'd need to approve it"), L141, L157-L165 (a second comment on mmm-infra#8 to correct the first one's "not yet sanctioned" line).
- **Cost:** two question slots and one hand-pasted line. Two extra comments on mmm-infra#8.
- **Root cause:** the vault is a second write surface for every project, but `design-project` never records a standing sanction for it.
- **Owner of the fix:** design-vault `plugin/skills/design-project/SKILL.md` step 1 (ask once) and step 3 (write the line).
- **Already filed:** no.
- **Proposed change:** in step 1 ask the founder once: "May this project's design sessions write its own `fit.<key>` verdicts and `project: <key>` entries in the vault?" On yes, the CLAUDE.md line from step 3 adds: "Its design sessions may write `fit.<key>` blocks and `project: <key>` entries in lucmoseley/design-vault (founder sanction, <date>)."
- **Confidence:** 70% (55%-85%). It drops if the founder wants to approve each vault write by hand.

## Whose job: mmm-infra#14 and mmm-infra#21

- **mmm-infra#14 (design-process order) was the vault's job.** Its question is about the method for every project. Its answer changed `design-round` for every project (design-vault `5d1f926`, via mmm-infra#16). The research file lives in mmm-infra at `docs/research/design-process-order.md`. The vault cites only the issue numbers (`design-round` SKILL.md line 23 and `design-critique` line 22 cite mmm-infra#16). A vault session that wants the sources must open another project's repo. The vault already keeps its own method research under `docs/research/` (eleven files today). Proposed: when a project session researches the method itself, land the note in design-vault `docs/research/` and leave a pointer in the project. Owner: design-vault README or CLAUDE.md (the convention). Confidence: 70% (55%-85%).
- **mmm-infra#21 (Mark's voice) was the project's job.** It reads Mark's own corpus and writes `docs/brand/voice-guide.md`, which the brand sheet §5 now binds. That is client data, so it belongs in mmm-infra. The method part is general: `design-project` §1 asks the founder "how the copy should sound", and §2 writes his answer. Here the better source was the client's own published writing (12 blog posts, 24 papers and talks, 2 corpus readers, about 10 minutes). Proposed (pattern 3): `design-project` §2 Voice adds "Where the client has published writing, derive the voice from it and keep the guide beside the rules file." Confidence: 60% (45%-75%). It drops if most clients have no corpus.

## Did vault fixes reach mmm-infra?

Yes. Every `plugin/` commit on design-vault was released within about one minute. Every mmm-infra session that loaded a design-vault skill loaded the build that was released when it started.

| Release (claude-plugins pin) | Pin time (UTC) | mmm-infra sessions that loaded it by skill load |
|---|---|---|
| `0202f18` | 30 Sep 16:24 | 44ca65d8 (#6), 8ad05cae (#9 r1), 2b924dbd (#8), 8c2c8bf9 (#9 r2) on 4 Oct; 44d000b9 (#14) on 5 Oct |
| `5d1f926` (craft gate, #14's seven changes) | 5 Oct 07:32 | 631cff6d (#8, from 07:44) |
| `919c6b3`, `0aa9fdf`, `fa85e44`, `d0a276d` | 6 Oct 12:13-16:03 | no mmm-infra session loaded a design-vault skill after 6 Oct |

Evidence: `gh api repos/lucmoseley/claude-plugins/commits?path=.claude-plugin/marketplace.json`; `git log -- plugin/` in design-vault; "Base directory for this skill" lines in each raw jsonl under `~/.claude3/projects/-home-lucmo-mmm-infra/` (no `.claude2` mmm-infra session loaded one); `~/.claude/plugins/installed_plugins.json`.

Two limits:
- A long session keeps the skill text it loaded. 631cff6d ran from 5 to 8 Oct on `5d1f926`. The motion-flow check (`919c6b3`) landed on 6 Oct mid-session. That session did not use it; it worked the site look, not motion, so nothing was lost.
- 



## Went well

### W1: `design-project` registered mmm-infra cleanly, in one session, with no founder correction
- Session 44ca65d8 (mmm-infra#6) ran 12:45-12:58 UTC on 4 Oct. It wrote the brand sheet with measured values (logo blue `#0070C0` and arch grey `#404040` read from the logo's pixels, L247-L258). It wired `CLAUDE.md`, design mode and `.impeccable/config.json`, registered the project (design-vault `7f280c0`), and ingested Mark's four sites with his own words as notes (`84a4521`). `validate.js`, 144 tests and the pointer test passed. A headless render confirmed the Project menu (L521, L533). The founder sent no message in it.
- Not yet in the method: the session took the four screenshots itself with headless Chromium (L101-L116), and fixed a Squarespace video hero that rendered black by laying the video's own still over it (L154-L212). `design-project` §5 (same text in `0202f18` and today) says "Ask the founder for screenshots". Proposed: §5 says "Take the screenshots yourself: `python3 ~/design-vault/scripts/browse.py shot <url> --out <png> --full-page`. Check each one by eye; a video hero can render black. Ask the founder only for a page behind a login." Confidence: 75% (60%-90%).
- Small drift: the session wrote `fit` blocks for the four entries (all "adapt") without putting them to the founder. `design-project` §5 says leave `fit` out, and design-round §1a step 2 says put each draft to the founder. No harm followed. No change proposed.

### W2: The library sweep's procedure was sound, once someone asked for it
- 631cff6d split the 92 unjudged entries into four batches, sent one reader per batch with the vault's `fit` shape and a read-only rule, made each reader open the screenshot, then read every adapt take before writing. It caught one take that overstated Mark's lean to the legal pad (L1450).

### W3: Method research done in the project reached the vault the same morning, ruled one proposal at a time
- mmm-infra#14 closed at 05:55 UTC on 5 Oct with seven proposals. Its pointer comment asked #16 to rule them "so the vault is edited once" (44d000b9 L304). The founder ruled them on #16. The vault commit `5d1f926` landed at 07:31 with six mutation tests, the pin moved at 07:32, and the next #8 session loaded it at 07:44. Pick-next held #8 behind #16 (ac637a02 L125), so round one ran on the new method. Not yet in the method: the "rule each proposal on one ticket, edit the vault once, release, then unblock the round" sequence.

### W4: The release step works
- Every `plugin/` commit reached the marketplace pin in about one minute (table above). #58's CLAUDE.md rule and `release-check.js` did their job. No change.

### W5: The charting session kept the vault clean of a reference the founder ruled out
- The founder corrected the reading of LoveFrom: "that site is probably not even worth adding to the design-vault" (454739af L189). The session kept LoveFrom out, and the brand sheet §6 records the ruling. No change.

## Out of scope here (owner named)

- **Hosting research ignored the "built with Claude Code" constraint.** mmm-infra#2 recommended Framer, a no-code builder. The founder overruled it: "The website will absolutely be built using Claude Code, that's a non-negotiable. Much of the reason I'm doing this project is as practice for making the MantaHostels site" (24feac31 L181). `design-project` had already set `.impeccable/config.json` to `buildPath: code` the same hour. Owner: mmm-infra (the map's standing rules), and workflow-core `wayfinder` (a research brief reads the map's rulings). Cost: about four founder messages in 24feac31 (L181-L331), mostly on Vercel terms, which are not a vault matter.
- **The doc-map gate refused `.impeccable/config.json`.** `design-project` step 3 writes that file. workflow-core's doc-map check does not see a tracked file in a dot directory, so the commit failed until the session removed the row (44ca65d8 L402-L450, about 8 calls). Owner: workflow-core `check-doc-map.js`. Not found filed (searched workflow-core for "doc-map hidden directory", "impeccable doc-map", "doc-map dot directory untracked").
- **The voice guide models Mark's humour on a line the founder had just called childish.** At 14:36 UTC on 5 Oct the founder wrote "v3: The font and phrasing of this text box are childish: 'Whichever PPP Law I am currently working on with a client country!'" (631cff6d L3017). mmm-infra#21 (filed 15:01) calls that line "a good sample", and `docs/brand/voice-guide.md` §5 makes it "The model" for humour. The founder may have objected to the tile's font and setting, not to the line. Owner: mmm-infra (put it to the founder). Confidence that this is a real conflict: 45% (30%-60%).
- **"Why ddin't you launch issue 8?"** (ac637a02 L91). #8 was blocked by #16 at pick time. Owner: workflow-core `pick-next` (its report could name each blocked issue's blocker). One founder message.
- mmm-infra#11 (8221599a, account set-up) touched no vault step.

## Bound

- **Read in full (reduced transcripts):** 454739af, 44ca65d8, 30b6bc74, 44d000b9, aa836460, 2b924dbd, and the pick-next sessions 658554f9, 6e832628, df1e0461, ac637a02, 190c1ddc, 73231b82, 9cb59822, 1e02f7bc, a26a7498 (founder turns and vault mentions; none but ac637a02 carried a founder question).
- **Read in part:** 24feac31 (founder turns, opening, close); 8221599a (founder turns and vault mentions only; its subject is accounts); 631cff6d (the sweep L1301-L1612, the round-one rejection L2986-L3017, plugin-path lines, concept-seed lines; not the round-two or photo work, which #88 and other tickets cover); 8ad05cae and 8c2c8bf9 (founder turns only; animation work is #88's); 4226ac58 (L131 only).
- **Raw jsonl drill-down:** 454739af L151, L184; 631cff6d L3013, L3017, L129, L7726, L8967; 30b6bc74 L64-L67; 44ca65d8 L403, L450. "Base directory for this skill" grep over every mmm-infra jsonl in `.claude3` and `.claude2`.
- **Files and records read:** mmm-infra `docs/brand/brand-sheet.md`, `CLAUDE.md`, `docs/research/design-process-order.md` §5-§9, `docs/brand/voice-guide.md` §5; mmm-infra#16, #21 bodies and comments; design-vault #79, #75, #77, #58, #13; `data/gallery.json` `projects.mmm-infra` and every `fit.mmm-infra` verdict; `plugin/skills/design-project/SKILL.md` (today), `plugin/skills/design-round/SKILL.md` §0-§2 (today, `0202f18`, `c6529a6`), `references/impeccable.md`; design-vault `git log -- plugin/`; the claude-plugins pin history; `installed_plugins.json`; workflow-core `scripts/design-mode.sh` (v1.3.10).
- **Not read:** subagent transcripts of the sweep readers; 1bbd72cf (#16) and 6a96e0c1 (#17) beyond what #16's comments say; the round-two record.
