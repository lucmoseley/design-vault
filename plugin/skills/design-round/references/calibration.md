# The calibration run

When design-round §0's `node round-log.js` prints `calibration due`, three fresh critics re-judge the latest logged rounds, without the founder's verdicts in reach, and are scored against them (design-vault#168). The run holds up no round, and starts once he says so. It runs in the vault, `~/design-vault`; every script below but `gate.js` is at the vault's root.

## The critics' confinement

Each critic is a headless `claude` session that `calibration-critic.js` starts with its working folder set to one round's folder of the packet, under the flags of its `CONFINED` array. So a critic reads its round's brief, gate list, copy bans, candidates and principles, and nothing else: no log, pick, ticket, other round's folder, shell or network. Never run a calibration critic as a subagent, or by any command but `calibration-critic.js`: a subagent can read the logs.

Every critic of a run must run on the Claude Code version and model the canary held on; the scorer refuses any other.

**First held live:** 14 Oct 2026, on Claude Code 2.1.299 and claude-opus-5-5 (design-vault#168). Where the canary fails on a later version, no run goes ahead until the confinement is fixed.

## The run

1. **The rounds.** Every row of `data/round-log.jsonl` after the last calibration run's `round_log_rows` (the last row of `data/calibration-log.jsonl`, or every row where none is logged), and, where fewer than ten are, the log's last ten rows (every row, where it holds fewer): a run due on a change of model or gate may find no new round (design-vault#209). The scorer refuses a manifest that leaves one out. Make the run's folder outside every repo: `run=$(mktemp -d /tmp/calibration-XXXX)`.
2. **The manifest**, `$run/manifest.json`, in the shape `calibration-packet.js`'s header gives: for each round, its ticket, number and tag (`rounds/<slug>-r<n>`), and these five, gathered into `$run/sources/<slug>-r<n>/`:
   - **brief**: the brief as that round's critic was given it, from the brief's ticket: the brief, that round's brief delta, and the corrections its dispatch quoted (§4).
   - **gate list**: the look questions as the gates stand now, whatever made the run due (design-vault#232 Q1 (A)): `node plugin/skills/design-round/scripts/gate.js list --look --asset <class> [--fact <fact>]… plugin/skills/design-critique/rules [<the project's gate>]`.
   - **gate list then**: the look questions of that round's time, which the critics never see. The scorer counts his first pick a Yes only on a question whose wording, its line and `Applies to:` line less its number, is the same in both lists. Where the round folder holds `gate/look.txt`, take it. Otherwise run the same command on the vault's gate and the project's as each stood when the round's tag was made: `git show <commit>:<path>` for a file, and `git archive <commit> plugin/skills/design-critique/rules | tar -x -C <dir>` for the vault's store; before #265 the vault's gate was the one file `plugin/skills/design-critique/gate.md`. Run the `gate.js` and `gate-form.js` of that same commit, `git archive <commit> plugin/skills/design-round/scripts`, since today's refuses a vault question in an older form. Where neither gate file existed then, write `No gate questions existed at this round's time.`
   - **copy bans**: the copy bans that round's critics were given (design-round §4, design-vault#232 Q2): the round folder's `gate/copy-bans.md`. Where it holds none, take them by §4's rule from the project's rules file and the files it sends copy to, as each stood at the round's tag, or write `none`.
   - **candidates**: one folder per candidate, holding only what that round's critic was shown of it: the image itself, or a page's width-sweep screenshots and contact sheets, read from the round's tag (`git -C <project repo> show <tag>:<path>`). Never a report, the critic's or a script's.
3. **The packet.** `node calibration-packet.js --manifest $run/manifest.json --out $run/packet`. Where it refuses, fix the source it names and build again; never edit the packet by hand.
4. **The canary, then the critics.** `node calibration-critic.js --packet $run/packet --model <model> --answers $run/answers`, in the background. `<model>` is the one the rounds' critics ran on, the building session's model. It runs the canary first and no critic where it fails. Where it exits non-zero, tell the founder, quoting what it printed, and stop. Where this session's permission check refuses to start it, ask him to run the same command with `!`.
5. **The score.** `node calibration-score.js --manifest $run/manifest.json --packet $run/packet --answers $run/answers --where "<where>" --row $run/row.jsonl`. `<where>` is the session and date he is told the result in, or the comment's link where it is posted.
6. **The log.** Append `$run/row.jsonl` to `data/calibration-log.jsonl`, run `node calibration-log.js`, and commit the log. Then delete `$run`.
7. **The founder.** Tell him in this session, in plain words, what the score printed:
   - how often the critics agreed with him, on leader picks, on gate questions and on his corrections, each with its likely range: a run of ten rounds cannot tell a good critic from a weak one on picks alone;
   - how often each critic said Unsure;
   - how often a settle critic settled a split, from the rounds' `splits` and `settled` (design-round's gate check, design-vault#170);
   - each disagreement: the round, the candidate, what he said, what the critic said, and the question, lens or unlanded rule it turned on;
   - each question added or reworded since its round, and how the critics answered it on his first pick: a No is a pick of his the new rule would fail, a fact about the rule, not a fault in the critics.

   Ask him nothing about it, unless a disagreement turns on a rule he has not ruled on; that question goes to him as design-round's corrections-log section asks it.
