---
name: design-project
---

# design-project

Run this from the new project's repo, once. The vault is `~/design-vault`; where it is absent, stop and say so.

The project is set up when every step's check holds.

A file git does not track yet reaches a pathspec commit only after `git add -N <path>`; then `git commit -m "…" -- <paths>` as usual.

## 1. Ask the founder, and through him the client

Read the repo's README and CLAUDE.md, and the client's current site where there is one, first. Then send the founder one plain message in two parts.

**His own questions**, for whatever those files leave out:

- "Who is the client: you, designing for yourself, or someone else?";
- the client's name, who the site serves, how senior they are and the register they expect;
- the client's fonts, how the copy should sound and words to avoid, and anything the client has ruled in or out;
- where the client has published writing of their own (posts, papers, talks), for the voice (step 2);
- a message he has written to the client himself, and the client's own words for what is wrong with a picture or page, for the writing-to-the-client file (step 3);
- whether this project's design sessions may judge library entries for it and add its own references to the vault (its `fit.<key>` verdicts and `project: <key>` entries) without asking him each time (design-vault#92 S7).

**The client's questions**, drafted as one message he forwards, or answers himself where he knows: the six set-up questions, then the twelve colour and logo questions, with no cap on the count (design-vault#183 Q2 (B)). Fill in every answer: your best reading from the files, the current site or the category, with its basis in one clause and the main other reading, so that the client only confirms or corrects. A question already answered by the files, the site or earlier messages is left out. Where the founder is the client, as for Manta, ask him in the session, and take S2 and S4 from data first (search logs, reviews, support mail).

The set-up questions, in this order (design-vault#130). Each says what kind of answer it gets:

- **S1** (goal) "What work do you want more of from the site? Name one or two kinds of client or project. Our guess: <the service the current site leads with>."
- **S2** (evidence) "Think of your last three or four clients. How did each first hear of you, and what did they want to check or ask before they got in touch?" A guess about visitors is never offered as the client's answer, so the filled-in answer is "or skip, and we follow what sites like yours put first", naming that.
- **S3** (goal) "When someone visits the site, what should they do before they leave? Our guess: <the current site's main button>. Or is it something else, such as booking a call in your calendar or downloading your CV?"
- **S4** (evidence or estimate) "What must a visitor be sure of before they <S3's action>? Our guess: <the draft for this kind of business in [what a visitor must be sure of](../design-critique/references/first-visit-trust.md#what-a-visitor-must-be-sure-of)>."
- **S5** (fact) "Here are the pages on your current site and what we plan for each: keep, merge or drop. Change any?" A broken or empty page is marked drop, unless the site's statistics show visits to it; a page of the client's own work is marked keep, with drop as the other reading.
- **S6** (fact) "What will you give for the new site: photos, text, time to review? Our guess: <what they have already said, or no new photos and two short reviews>."

Each answer is recorded as the client gives it, with its kind: **fact** (their business), **goal** (their wish), **evidence** (what people asked them, with how many cases) or **estimate** (their guess about visitors). An answer can move kind: "most people want my CV" is an estimate even when it comes back from S1.

The colour and logo questions, in these words:

1. Which colours does the client use now, and where? Give the hex values from the logo, the current site and any printed material.
2. For each colour: must we keep it exactly, may we adjust it a little, or is it free to change?
3. What is each colour for? For example the brand's main colour, text, a background, a button. A colour with no job may be dropped.
4. Which colour, if any, should mean "click here"? Only one colour does that job.
5. Are there colours the client dislikes, or that belong to a rival or to a different kind of business?
6. Light pages, dark sections, or both? Which backgrounds does the client picture: white, warm paper, a strong colour, photographs?
7. Which logo files exist, and is there an original (vector) file? Which versions exist: full colour, white for dark backgrounds, one colour, a small icon?
8. Does the client have written rules for the logo, such as a guidelines PDF with approved backgrounds, clear space or a minimum size?
9. Did the client choose the logo's colours on purpose, or did they come from a program's standard colours?
10. If a version is missing (for example a white logo for a dark band), may we make it, or must the logo stay exactly as it is?
11. Which backgrounds must the logo sit on in the new site: a light page, a dark band or footer, a photograph, a coloured header?
12. May the site's other colours differ from the logo's, as long as they go well with them, or must the site use only the logo's colours?

Then pick a **key** named for the client, not the repo, since one client may have several repos (`acme-ceramics`), and a **name** the founder calls it by. The key must be new in the vault's `data/gallery.json` `projects`.

Check: a new key, a name, an answer or "not yet" for each of his questions, and for each of the client's an answer with its kind or a filled-in answer awaiting them.

## 2. Write the rules file

Create `docs/brand/brand-sheet.md` in the project's repo. Head each section `## §<n> <title>`, because a verdict cites one (`fit.<key>.sheet_section`):

1. **Who it is for** — a `Client:` line naming the client, or `Client: the founder, for himself`; then the audience with its seniority and register, and S1–S6's answers, each with its kind.
2. **Colour** — each colour with its hex value, its job and its status: fixed, may adjust, or free (questions 1–5). A logo colour is fixed unless the client opened it (question 2). Below them, `palette.py`'s colour and ΔE00 tables, with each near-miss settled: snapped to one token, moved apart, or put to the founder where it is the client's call.
3. **Type** — the client's fonts.
4. **Logo and marks** — where the files live. Logos, guidelines PDFs and other brand files stay in this repo under `docs/brand-assets/`; the library holds only screenshots. The client's logo rules (question 8), the versions held and those missing, and whether a missing one may be made (questions 7 and 10). `palette.py`'s lightness band and ground table, over every ground questions 6 and 11 name, with the version to use on each ground and every ground banned. Last, a `Logotype selectors:` line, the CSS selector of each logotype the site sets as live or SVG text, or `none`: WCAG 1.4.3 exempts a logotype from contrast, and check-access.py exempts the text under each selector given as `--logotype` ([rules.md](../design-critique/rules.md#how-the-records-are-answered)'s access records).
5. **Voice** — how the copy sounds, and words the client avoids. Where the client has published writing, derive the voice from it: read it, with subagents where there is much of it, and write `docs/brand/voice-guide.md` beside this file, each trait backed by a quoted line. This section then names the guide and adds the founder's answers.
6. **Standing rules** — anything the client has ruled in or out.

Write the founder's answers, and "open" with the filled-in answer where the client has not replied. Only a fact or a goal becomes a rule in §6 or a question in the gate below; evidence and estimates stay in §1, as defaults a round may test. The House DNA reaches every brief of this project already (design-round §1), so this file carries only what is the client's own.

Measure §2 and §4 with `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-project/scripts/palette.py`: each fixed logo colour as `--logo`, each other colour the client must keep exactly as `--fixed`, every other colour as `--colour`, each large grey surface near the page ground as `--surface <name>`, and each ground as `--ground`. Its lines are the records `vault.colour-distance` and `vault.logo-ground`, with their reasons in [the brand palette reference](../design-critique/references/brand-palette.md).

Then write the project's gate: copy [the client-fit gate](references/fit-gate.md) to `docs/brand/fit-gate.md`, put the key in for `<key>`, and fill its other slots from §1, §2, §4 and §6 (design-vault#91 S2).

Check: the file exists with its six sections; `node ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/client.js docs/brand/brand-sheet.md` prints the client the founder named; §2 and §4 hold `palette.py`'s tables, or §2 says the client gave no colours; `docs/brand/voice-guide.md` exists where the client has published writing; `fit-gate.md` has no `<…>` slot left, and `node ${CLAUDE_PLUGIN_ROOT}/skills/design-round/scripts/gate.js check ${CLAUDE_PLUGIN_ROOT}/skills/design-critique/rules docs/brand/fit-gate.md` passes.

## 3. Wire the project's repo

- Add this line to the repo's `CLAUDE.md`:

  ```
  Design work runs through design-vault:design-round. In the design vault this project is <key>; its rules file is docs/brand/brand-sheet.md, and its project gate, which a round's critic runs first, is docs/brand/fit-gate.md. The client's original files are held in private/client-originals/ by skills/design-project/scripts/client-originals.py in the installed design-vault build, whose header gives the rules; anything sent to the client is built with its send. A message to the client follows docs/copy/writing-to-<client>.md, and when the founder corrects a word or the tone in one, the correction goes into that file in the same turn. Research into the design method itself, not this client, lands in lucmoseley/design-vault's docs/research/ with a pointer left here, by that repo's README §Starting a new project. The installed design-vault build is the folder this prints: `jq -r --arg p "$(git rev-parse --show-toplevel)" '.plugins["design-vault@lucmoseley"] | (map(select(.projectPath == $p)) + map(select(.scope == "user")))[0].installPath' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/installed_plugins.json"`. Never pick a build by sorting or listing the plugin cache folder.
  ```

  Where the founder said yes to the vault question (step 1), the line goes on: `Its design sessions may write fit.<key> verdicts and project: <key> entries in lucmoseley/design-vault (founder sanction, <date>).`
- Merge `Read(/<config dir>/plugins/cache/**)` into the allow list of the repo's `.claude/settings.local.json`, with the config dir as an absolute `//` path (`$CLAUDE_CONFIG_DIR`, or `~/.claude`), so a round's critic can read the plugin's references. The file is per machine: confirm `git check-ignore` covers it, and add it to `.gitignore` where nothing does.

- Switch design mode on, so every round runs impeccable ([design-round's impeccable map](../design-round/references/impeccable.md)). Set `enabledPlugins["impeccable@impeccable"]` to `true` in the repo's `.claude/settings.json`; where the repo carries workflow-core, its `design-mode` skill does this. It loads from the next session, and only where the plugin is installed (design-vault#92 S4). So in each config dir the founder runs (`$CLAUDE_CONFIG_DIR`, and every other `~/.claude*` holding `plugins/installed_plugins.json`), confirm `jq '.plugins["impeccable@impeccable"][]? | select(.scope=="user")' <dir>/plugins/installed_plugins.json` prints an entry. Where it prints nothing, run `CLAUDE_CONFIG_DIR=<dir> claude plugin install impeccable@impeccable --scope user`, after `claude plugin marketplace add pbakaus/impeccable` where that dir has no `impeccable` marketplace, then set `enabledPlugins["impeccable@impeccable"]` to `false` in that dir's `settings.json`, so design mode stays off in every other repo.
- Write `.impeccable/config.json` as `{ "buildPath": "code" }`, merged into any keys already there.
- Give the client's original files a home: run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-project/scripts/client-originals.py init` in the repo, adding `/private/` to `.gitignore` where nothing covers it.
- Copy [the writing-to-the-client template](references/writing-to-client.md) to `docs/copy/writing-to-<client>.md`, named for the client as the founder addresses them (`writing-to-mark.md`). Put the founder's message and the client's words from step 1 in its two slots, or "none yet".

Commit the rules file, `docs/brand/fit-gate.md`, any `docs/brand/voice-guide.md`, the `CLAUDE.md` line, `.claude/settings.json`, `.impeccable/config.json`, `docs/brand/client-originals.json`, `docs/copy/writing-to-<client>.md` and any `.gitignore` change in the project's repo, and push.

Check: the commit is on the remote, the `CLAUDE.md` line has no `<…>` slot left, `settings.local.json` is ignored, the impeccable `jq` above prints a user-scope entry in every config dir, `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-project/scripts/client-originals.py verify` prints `verify: ok`, and `docs/copy/writing-to-<client>.md` has no `<client>` left in it.

## 4. Register it in the library

Add `projects.<key>` to the vault's `data/gallery.json`:

- `name` — the name from step 1.
- `rules` — `docs/brand/brand-sheet.md in <owner>/<repo>`, the owner and repo read from `git remote get-url origin`.
- `gate` — `docs/brand/fit-gate.md in <owner>/<repo>`, where that file passes step 2's `gate.js check`. Leave it out where it does not.
- `desktop` — the desktop screen size, as `1536x864`, that the project's own visitor analytics show most, where it has analytics and that size is not `1920x1080`. Leave it out otherwise: design-round's motion, frame and contact-sheet scripts then render the window a 1920x1080 screen leaves, 1920x945.
- `verdicts` — `["on-brand", "adapt", "off-brand"]`.
- `groups` — `[]`: a project starts with none. A **project group** is one of the project's own uses for a reference, a question the library's shared page parts and motion kinds cannot say, such as Manta's hero art. Add one when the project first has such a question: `{ id, name }`, the name a plain term, then ` — `, then what it covers; an optional `header` adds a line on what a reference there answers.

In the vault, run `node bundle.js`, then the three checks `node validate.js`, `node --test test/*.test.js` and `bash test/design-round-pointer.test.sh`, show the diff, and commit by pathspec, leading with why: this project can now hold verdicts. Push once all three are green.

Check: all three pass, and the page opened from `index.html` lists the name in its **Project** menu.

## 5. The project's own references

Some references belong to this project alone: the client's current site and the rivals they named. Take their screenshots yourself: `python3 ~/design-vault/scripts/browse.py shot <url> --out <png> --full-page`. Open each one and check it by eye, since a video hero can render black; where one does, lay the video's own still over it. Ask the founder only for a page behind a login. Each goes in through the vault's ingest, kept to this project:

`node ingest.js --project <key> --source <url> <image>`

It marks each entry `project: <key>`. Then edit each draft:

- **`note`** — why the founder wants it, in his words (the vault's CLAUDE.md sets the rule).
- **`page_parts`** — the ingest's guess from the vault's `page_parts` list: the part of the page the reference is about, plus any other worth taking.
- **`origin` and `licence`** — the client's own site is `third-party` with licence `the client's own material, used for their project`; a rival keeps the ingest's defaults.
- **`fit`** — leave it out. Step 6 judges it with the rest of the library.

Run `node bundle.js` and `node validate.js`, and commit `data/gallery.json` and `data/vault-data.js` with the new `images/` files. A reference any project could use goes in without `--project`.

Check: every site the founder named for this project is ingested and committed, or he still owes its screenshot because it sits behind a login.

## 6. Judge the library

Round one cites only entries judged for the project (design-round §1), so judge every entry the project may cite now: each one with no `project`, or with `project: <key>`.

1. Split the entries into batches of about 25, one subagent reader per batch. Give each reader the rules file, `docs/brand/fit-gate.md`, design-round §1a step 1 for the `fit.<key>` shape and its rules (a reader leaves `motion` blocks and project groups alone), and its batch's ids. A reader writes nothing: it opens each entry's screenshot (`~/design-vault/images/<file>`) before judging it, and returns one `fit.<key>` draft per entry as JSON.
2. Read every on-brand and adapt take yourself against the rules file, and correct any that claims more than the client said. The founder is not asked to confirm each draft, as §1a step 2 asks for a single citation.
3. Write every block into `data/gallery.json` in one edit, run `node bundle.js` and `node validate.js`, and commit `data/gallery.json` and `data/vault-data.js` in one commit whose message gives the count per verdict. Push it.

Check: `jq '[.entries[] | select((.project == null or .project == "<key>") and .fit["<key>"] == null)] | length' ~/design-vault/data/gallery.json` prints `0`.

## 7. Hand over

Tell the founder, in plain words:

- The library page has his project in its **Project** menu. Picking it shows its verdicts, its own references and, once it has any, its groups.
- How many library entries came out on-brand, adapt and off-brand (step 6). Few on-brand or adapt means the library alone cannot seed round one.
- The client-fit gate every critic runs first, and which of its questions rest on something the client has not settled.
- Design mode is on from his next session here, and the first web round starts by setting impeccable up: its product record, the current site's look where one is built, and its design checker.
- A round starts from "run a design round for the <surface>" in this repo. Its drafts live in this repo on a throwaway `rounds/<slug>` branch, and the round asks him where its record goes (design-round §0).

Check: the message is sent, naming the key and the menu.
