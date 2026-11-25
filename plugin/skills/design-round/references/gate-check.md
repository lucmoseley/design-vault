# The three-critic gate check

design-round §4 answers every gate question this way (design-vault#170). `gate.js` is `${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/gate.js`; its header gives the answers files' form. `look.py`, beside it, is the settle critic's view tool (§4): `zoom`, `scrub`, `measure` and `pixels`. Everything this check writes goes in the round folder's `gate/`.

## 1. The list

Declare the asset's class and facts, then join the vault's gate and the project's, the file the library records as `projects.<key>.gate`, where it has one:

`node gate.js list --asset <class> [--fact <fact>]… ${CLAUDE_PLUGIN_ROOT}/skills/design-critique/rules [<project gate>] > gate/list.txt`

Its clash section waits for the reveal (§6).

## 2. Script and code questions, once, before any critic

On every candidate, answer each question in the list's script and code section, once. A script question takes the script its record's `script` field names, run as design-critique §1a or [rules.md](../../design-critique/rules.md#how-the-records-are-answered) says: its answer is that script's last run in the building session's finish stage (design-round §1c). A code question is answered by reading the code. Keep each script's output and exit code in `<candidate>/`. Write every answer to `gate/answered.json`, keyed by candidate name: `pass`, `fail` or `cannot measure`, each with one line of evidence naming the output's path and exit code. A `fail` is a fault (§5). `check-flow.py`'s exit 1 on interface moves alone is a pass (design-critique §1a). Where `vault.one-target` is on the list, its answer is the finish run of `parts-map.py <candidate page> --out <candidate>/parts`, and for `vault.load`, of `check-load.py <candidate page>`: for each, exit 0 is pass, 1 fail, any other cannot measure.

Then make the critics' list:

`node gate.js list --asset <class> [--fact <fact>]… --look --answered gate/answered.json <gate files> > gate/look.txt`

**Over 20 look questions, passes of at most 20** (design-vault#225, #414). Where `gate/look.txt` has more than 20, it prints them cut into numbered passes: the function-and-role passes first, then the treatment-and-value passes, each in stage then area order, cut at a stage's edge or else an area's where it can. Each pass goes to its own fresh trio: every function-and-role pass runs §3's three gate critics at once, each on `gate/look-<n>.txt`, made with `--pass <n>`, its files named `-<n>` before the extension (`gate/critic-a-<n>.json`, `gate/tally-<n>.txt`), then §4 and §5 over their faults; once their fixes land, make `gate/look.txt` again with the re-run `gate/answered.json` and run the treatment-and-value passes it prints the same way. A pass's number holds for the answers file it was listed with, so each `tally` takes the same `--pass` and `--answered` as its list. A treatment-and-value pass still runs where its fixes leave 20 questions or fewer. The other critics in §3 run once, not once a pass.

**The look renders** (design-vault#228). `look-renders.py`, beside `gate.js`, makes the renders two look questions name. Where `vault.contacts-look` is on `gate/look.txt`, run `python3 look-renders.py contacts <candidate page> --contact <name>=<selector>@<x>,<y>… --out <candidate>/look/contacts`, one `--contact` for each contact your `vault.contacts-code` answer lists, at the point where its two sides meet, in that element's own coordinates. Where `vault.curves-look` is on it, run `python3 look-renders.py bends <candidate page> --out <candidate>/look/bends`, and again on each SVG file the page draws through an `<img>` or a CSS `url()`. A curve CSS or a canvas draws has no path data: shoot its tightest bend by eye with `look.py zoom --scale 8` into `<candidate>/look/by-eye/sheet-<k>.png`. For a web surface, run each again with `--width 390`, into `contacts-390` and `bends-390`. Exit 6 names what could not be rendered, a contact on no element or path data `check-curves.js` cannot read: fix it and run again. On a page that cannot be rendered frame by frame, exit 6 prints the route by hand, `look.py zoom` at each contact at `--scale` 1, 2 and 3, each shot magnified 4× with Pillow's `Image.NEAREST`, and at each bend at `--scale 8`; those show the settled page only, so say in the round record that its key frames went unshown. Where a candidate has no contact, or `bends` prints that the question does not apply, write one line saying so for the critics.

## 3. The dispatches

Dispatch every critic at once, each a fresh subagent. Each is given what design-round §4 gives a critic: the brief, the brief delta, this round's candidates only, the stand-in list and its own examples from the corrections log. No critic sees another's answers.

**Each critic's examples are its own** (design-vault#193). Run `node ~/design-vault/critic-examples.js --project <key> --asset <class> --brief <brief file> --critics 5`. It prints a set for each of critics `a` to `e`. Give set `a`, `b` and `c` to the gate critics writing `critic-a.json`, `-b` and `-c`, set `d` to the whole-page critic and set `e` to the type critic, pasted as printed. Where it prints no examples, the critics get none.

**Three gate critics.** Each gets `gate/look.txt` and at most 6 candidates a dispatch (design-vault#169). Where a round has more, a fresh subagent takes the rest as the same critic, with the same examples, writing `gate/critic-a2.json` and on. Each writes its own answers file, `gate/critic-a.json`, `-b` or `-c`. Where `vault.affordance` is on the list, each also gets every candidate's `parts/key.txt` and `parts/key-*.png`, never `parts.json`, which says what each part does. Where §2 made look renders, each gets every candidate's `look/*/sheet-*.png`, never the single crops, and §2's line for a candidate with none. **A dispatch takes at most 30 sheets as well as 6 candidates**; where its candidates' sheets pass 30, it takes fewer candidates. A candidate whose own sheets pass 30 has `contacts` run again with `--times 0,end`, and the round record names the key frames that went unshown; one still past 30 gets a dispatch to itself, over the bound, said in the round record, since `gate.js` refuses a critic answering one candidate in two files. A sheet costs at most 1568 visual tokens, so 30 is under 50,000, a guess at what a critic can read beside its candidates' shots. The prompt, after the inputs:

> Answer every question in the list for every candidate: Yes, No or Unsure, each with one line of evidence saying what you saw and where. Yes passes. Answer Unsure where the render cannot settle the question; never guess. A question you pass with a minor case, a lesser fault the question does not fail, answer Yes with evidence beginning `Minor:`. Answer `vault.affordance` part by part, from the key and the render, never the code: for each part on the candidate's key, Yes where it looks as if a visitor can act on it, No where it looks as if they cannot, Unsure where the render cannot settle it; under `unlisted`, one line for each part off the key that looks as if a visitor can act on it. Answer `vault.contacts-look` and `vault.curves-look` from the look sheets, already rendered and magnified as each question asks; where a candidate has none for one of them, answer Yes with evidence beginning `Does not apply:` and the reason you were given. A stand-in is not judged for what it shows, but the craft done to it is: a cut-out's edge, a crop, scaling, a flattened mark (design-vault#169 B10). Answer only these questions: no critique, no score, no leader. Then name any two rules that cannot both hold here, quoting both. Write your answers to `<path>` as JSON, `{ "answers": { <candidate>: { <question id>: { "answer", "evidence" } } }, "clashes": [{ "candidate": <name or null>, "quotes": [<rule>, <rule>] }] }`, with `vault.affordance`'s answer as `{ "parts": { <part id>: { "answer", "evidence" } }, "unlisted": [<line>] }`. Leave `clashes` empty where you found none.

**impeccable's two assessments**, where the round runs impeccable (design-round §0). `impeccable critique` requires its Assessment A (the design review) and Assessment B (the detector and browser evidence) to run as isolated subagents. For each candidate, dispatch two fresh subagents at once, neither seeing the other's output: one runs Assessment A and one Assessment B, each as the pinned impeccable's `reference/critique.md` gives it under its own heading, on the candidate's page, and writes what that heading says to return to `<candidate>/impeccable/a.md` or `b.md`. Neither gets the brief's critic examples or another critic's report. Give the whole-page critic both files and each subagent's agent id.

**One whole-page critic** runs design-critique without its gates. It merges impeccable's two assessments into its critique (design-critique §1), runs impeccable's audit and the lenses, and names its leader, by design-critique §4's bar, and the runner-up it beat. Where its leader keeps a fault after §5, its runner-up leads if it has none, or else the round has no critic leader; the reveal says which. It is asked the same clash question, and its report quotes both rules of each clash it names.

**One type critic** runs design-critique §2a, given `node gate.js list --asset <class> [--fact <fact>]… --reader type ${CLAUDE_PLUGIN_ROOT}/skills/design-critique/rules > gate/type.txt`, the reference sections it names, the brief's type and every candidate. It writes `type-critic.md` in the round folder, which the building session appends to the whole-page critic's report under the heading "The type critic". It is asked the same clash question. Its findings are fixed and re-checked as the whole-page critic's are.

## 4. The tally

`node gate.js tally --asset <class> [--fact <fact>]… --answered gate/answered.json --critic gate/critic-a.json --critic gate/critic-b.json --critic gate/critic-c.json [--parts <candidate>=<candidate>/parts/parts.json]… <gate files> > gate/tally.txt`, with one `--parts` for each candidate where `vault.affordance` is on the list. A critic split over dispatches is one `--critic`, comma-joined: `--critic gate/critic-a.json,gate/critic-a2.json`.

Exit 1 means an answers file breaks the form, each fault printed. Fix your own. For a critic's, dispatch a fresh critic in its place. Each candidate's question comes out as:

- **pass**: three Yes, or a script or code pass; any minor case prints under it;
- **fault**: three No, or a script or code fail; fix it (§5);
- **split**: anything else, an Unsure included. It goes to a settle critic.

**The settle step** (design-vault#169 Q1 (A)). For each split, dispatch one fresh critic, all at once, given only that question's wording, the candidate, all three critics' answers and evidence from `gate/tally.txt`, and `look.py`. Where the whole-page critic's function walk finds a P0 under a function question the tally passes, that question gets a settle critic too, with the walk's row beside the three answers. The prompt:

> Settle this one question for this candidate by looking closer: zoom, scrub or measure with look.py, never by weighing the three answers. Answer Yes, No or Unsure with one line of evidence naming what you zoomed, scrubbed or measured, and where. Answer Unsure only where looking closer still cannot settle it. Write `{ "answers": { <candidate>: { <question id>: { "answer", "evidence" } } } }` to `<path>`.

Under `vault.affordance` it answers each split part, and `unlisted` where a critic named a part off the key, as `gate.js`'s header gives. Each writes `gate/settle-<n>.json`. Then run the tally again with one `--settle gate/settle-<n>.json` for each, into `gate/tally.txt`: Yes passes, No is a fault, and only Unsure goes to the founder. Count the round's splits and how many the settle critics answered Yes or No, for the round log (design-round §3 step 5).

## 5. Fix and re-check

Fix each fault. **A clash a critic names is never fixed by the building session**, however plain the fix looks: it goes to the reveal.

**Keep the before renders** (design-vault#320). Before a pass's first fix, copy `gate/answered.json` to `gate/before-<n>.json`, `<n>` counting the re-checks, and, for each candidate the pass fixes, every folder of renders §3's critics got into `<candidate>/before-<n>/`. After each fix, re-run that candidate's script and code questions and update `gate/answered.json`. A script or code fault is gone only where its re-run passes. Then make each of its renders again, into its own folder, as it was first made:

- `layout/`, by the sweep (design-round §4);
- `sheet/`, by `contact-sheet.py`;
- `parts/`, by `parts-map.py`;
- `look/`, by `look-renders.py`, its `--contact` points from the re-run `vault.contacts-code` answer, and by §2's by-eye zooms.

The re-check critics get those renders from both `<candidate>/before-<n>/` and the re-run, each as §3's critics got it, the dispatch naming `before-<n>/` as renders from before the fix, and for a `vault.affordance` fault, that fault's lines from `gate/tally.txt`.

**Three fresh critics re-check** (design-vault#193). Once a pass of fixes lands, dispatch three at once, given `gate/look.txt`, each fixed candidate before and after, at most 6 candidates a dispatch as in §3, and each fault's question id and wording. Each answers, Yes, No or Unsure with one line of evidence:

- "Is this fault gone?", for each fault that is a look question or that its re-run could not measure;
- "Does the change leave every other question on the list no worse than before?", once for each fixed candidate, as `others`, naming any question it made worse.

**A `vault.affordance` fault is judged against both keys** (design-vault#320). Its lines number parts as the before key does, and the re-run numbers them afresh, so the critic finds each part on the new key by its text and place. The dispatch adds one line for each part a `hidden`, `false`, `dead` or off-the-key line names, and each part only on the new key: whether a visitor can act on it now, which the building session reads from both parts maps, matching parts by text and place. The critic answers Yes only where each of those parts looks as its line says, and every other part looks as actable, or not, as it did on the before key. A named part the fix removed counts as mended, and its evidence says so.

Each writes its answers to `gate/recheck-<n>-a.json`, `-b` or `-c`, in the form `gate.js`'s header gives, a critic split over dispatches comma-joined in its `--critic` as in §4. Then:

`node gate.js recheck --asset <class> [--fact <fact>]… --before gate/before-<n>.json --answered gate/answered.json --fault <candidate>:<id>… --critic gate/recheck-<n>-a.json --critic gate/recheck-<n>-b.json --critic gate/recheck-<n>-c.json [--parts <candidate>=<candidate>/parts/parts.json --before-parts <candidate>=<candidate>/before-<n>/parts/parts.json]… <gate files> > gate/recheck-<n>.txt`, with one `--parts`, the re-run map, and one `--before-parts` for each fixed candidate where `vault.affordance` is on the list. A link the re-run map marks dead keeps a `vault.affordance` fault whatever the critics answer.

A split re-check answer goes to a settle critic as in §4, given both renders, and the recheck runs again with each `--settle gate/recheck-<n>-settle-<m>.json`. A fault clears only on Yes to both its questions, three Yes or a settle critic's, or on its re-run's pass and Yes to `others`, and only where no script or code question that passed in `gate/before-<n>.json` fails now and, for a fault but `vault.affordance`'s, no link is dead in the re-run parts map that was not in `<candidate>/before-<n>/parts/parts.json`. Exit 1 is a broken file, as in §4. Every other fault prints `stop, for the reveal` with the stop signals it met.

**Stop fixing a fault on the first stop signal.** The fault goes to the reveal:

1. the fix breaks another question: No to `others`, a script or code question that passed now fails, or, for a fault but `vault.affordance`'s, a link the re-run parts map marks dead was not dead before;
2. the same question fails again after a fix aimed at it: its re-run fails, or No that it is gone;
3. the critics split on either question and the settle critic is Unsure;
4. a clash is named that quotes the rule the fault breaks.

**design-round §4's "Re-checks stop" rule still bounds the loop.** Every gate fault is a P0, save one a stop signal has sent to the reveal. The whole-page critic's findings are fixed and re-checked as design-round §4 says, on the same count.

## 6. The blind view and the reveal

**The blind view** carries one thing from this check: a candidate with a fault left after §5 keeps the `can't lead: fails <gate>` tag of design-round §3 step 2. `<gate>` is the vault gate or the project's gate, whichever owns a question it fails. No split, Unsure, clash, tally or count reaches the founder before his pick.

**At the reveal** (design-round §3 step 4), the round record gives these beside the gate each belongs to, under the question's number and id:

- each fault left, and the stop signal or the cap that ended its fixing;
- each founder question, with all three critics' answers and evidence and the settle critic's, from `gate/tally.txt`;
- each minor case the tally reports, which the round does not fix;
- each clash a critic named, the whole-page and type critics' included, quoting both rules; a clash that touches no question on the list goes under the gate list as a whole;
- each clash in `gate/list.txt`, settled by precedence or for the founder.

The review strip's first line gives each gate's PASS or FAIL with its fault count, and how many questions are for the founder.
