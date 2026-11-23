# Taste Vault

> **This is `lucmoseley/design-vault`**, a public repo published as one squashed commit; its history, seeded from [cth9191/taste-vault](https://github.com/cth9191/taste-vault), and its issue tracker stay in the private `lucmoseley/design-vault-tracker`. It is becoming the home of the portable design method (the `design-vault` Claude Code plugin under `plugin/`) and one merged inspiration library. Upstream changes are taken by path-scoped cherry-pick from the `upstream` remote, never by data; nothing is pushed upstream.

**Inspiration in, vocabulary out.** A local, zero-build design-taste gallery that turns screenshots of sites you love into objective design vocabulary, clustered collections, and paste-ready briefs for Codex, Claude Code and other coding assistants.

Built as the companion tool for the video **[Turn Claude Into A Design GENIUS In 3 Simple Steps](https://youtu.be/7FU98O0JLHs)**. This repo ships with my real vault — 46 entries across 12 collections plus my House DNA.

---

## From references to an original design

The repo now includes **Reference to Design**, a reusable skill and prompt pack developed through the Vantage landing-page study.

**Three directions → pick one → three variations → refine.**

Once you choose a composition, an optional [polish studio](skills/reference-to-design/references/polish.md) lets you compare Original, Restrained and Expressive presets, tune individual details, and save a clean preview. The [prompt pack](skills/reference-to-design/references/prompts.md) includes the exact prompt for this stage.

- [Copy-and-paste prompts](skills/reference-to-design/references/prompts.md): exact reusable wording for planning, building, refining and correcting results.
- [Install and use the skill](docs/reference-to-design.md): use it with your chosen design guidance or the model's own judgment.
- [Example brief and video sequence](examples/vantage.md): a fictional AI financial research product's marketing page.
- [Optional skill comparison](skills/reference-to-design/references/comparison.md): matched inputs and limitations when comparing treatments.

Browse several actual reference screenshots, identify recurring visual principles, and decide what to carry over and what to invent for your product. Build three comparable directions, select one, then explore variations inside that aesthetic. One direction is enough if you have already settled on it.

The aim is a recognizable design family with an independent subject and composition. Avoid transferring the source's subject, layout, palette and focal placement together. Also avoid reducing the collection to a vague style label that yields a generic page.

The gallery's vocabulary and image recipes are starting points. Open the screenshots themselves and adapt the recipes to the new product; swapping one source object for a similar object may still be too literal. Keep website text, controls and product data in live UI. Image generation and static mockups are optional, depending on the visual question you need to resolve.

The reference library, prompts and skill are included in this repo. The twenty-output development study is a separate local experiment.

---

## Quick start

```bash
git clone https://github.com/lucmoseley/design-vault.git ~/design-vault
```

Open `index.html` in a browser — double-click it, or bookmark it. No server is needed: opened from its folder, the page reads `data/vault-data.js`, a copy of `data/gallery.json` and `data/styles.json` that `node bundle.js` writes. From Windows, the WSL checkout is `\\wsl.localhost\Ubuntu\home\lucmo\design-vault\index.html`.

`ingest.js` rewrites the bundle after every image, and a commit whose bundle does not match the JSON is refused.

`python server.py --port 4610` (or `serve.bat` on Windows) still serves the page at http://127.0.0.1:4610, reading the JSON files directly. `server.py` binds to `127.0.0.1` only and serves without authentication; that unauthenticated local bind is accepted as-is — it is never exposed on another interface.

No third-party dependencies. The gallery is read-only: no request writes to disk, and new references arrive through the ingest below.

**For ingesting your own screenshots** you additionally need:

- [Node.js](https://nodejs.org)
- [Claude Code](https://claude.com/claude-code) CLI on your PATH

---

## Starting a new project

In the new project's repo, ask Claude to set the project up for design. The `design-project` skill registers it in the library with its verdicts and no groups yet, writes its rules file and its client-fit gate, wires the repo to the design round, ingests the references that belong to it alone, and judges every library entry for it. A design round in a project the library does not know offers it first.

**Research into the method lands here.** A project session that researches the design method itself, not its own client, lands the note in this repo's `docs/research/` and leaves a pointer in the project. A research note that proposes method changes lists every proposal in one numbered section (#92 S3, "Whose job").

## Using the vault in a project

1. Pick the project under **Project**. Browse **All references**, or pick a **look** and one of the project's **groups** (its own uses for a reference, such as Manta's hero art; hidden for a project with none) in the sidebar, and, from the chips above the grid, a **page part** (hero, footer, pricing, art only and the rest) and a **motion** kind, named by what sets the motion off (scroll, pointer, plays by itself, scene change, or plays once as it appears). The picks combine, each value shows how many references it would leave, and each pick shows above the grid, where a click removes it. The address keeps the picks, so a reload or a shared link lands on the same view. On a narrow screen every way in is one dropdown above the page. Narrow by **Fit** — on-brand, adapt, off-brand or unjudged. Search finds references in plain words: every word you type must start a word somewhere in a reference, in any order ("sea" finds seascape, never research), across its title, description, notes, keywords, vocabulary, look, page parts, motion and the project's groups — never the fit take. A design word also finds the plain words the library uses for it (hero finds "opening screen", parallax finds Scroll). Clicking a look or a group clears the search; a chip keeps it. The Style guide's search matches the same way. Sort by newest or name. A reference kept for one project shows only while that project is picked.
2. Open a screenshot to read its description, its fit for the picked project and its note — or, for a site, how it moves. Use **Zoom in** to view the original at full size.
3. Select up to five references and **Compare** them side by side. **Copy combined brief** includes every selected screenshot path, its design notes and its fit.
4. Paste the brief into your coding assistant, fill in your project, audience and required content, then build and iterate.

**Copy design brief** creates a single-reference brief: each reference is headed `Reference: <id> — <title>` and carries a `<project> fit:` line with the verdict, the group where it has one, and the take, or `unjudged` where nobody has judged it for the picked project yet. Expand **Image recipe** to copy an artwork prompt with composition guidance. Briefs work with Codex or other coding assistants and do not require a particular design skill or image-generation provider.

**My preferences** controls whether general House DNA is included (off by default); on, the brief lists what you usually avoid (`dna.never`) and what you usually keep (`dna.constants`, empty until you state one). Project notes take priority over general preferences. These settings and your comparison selection are saved in this browser.

## Ingesting your own inspiration

```bash
node ingest.js --source https://example.com ~/Downloads/shot-1.png ~/Downloads/shot-2.webp
```

`--project <key>` keeps every image in the run for that one project — a client's own site or its rivals. `--source <url>` records where the next image came from, here `shot-1.png`, and a web address there also becomes its `site_url`; without it the entry says `screenshot, site unrecorded`. Each image must be a PNG, JPEG or WebP of 20 MB or less, judged by its bytes, not its name. It is copied into `images/`, read by one `claude -p` call on Sonnet (about $0.07 an image; `--model haiku` costs about $0.045 but drafts visibly worse entries, per #10), renamed to its slug, and written into `data/gallery.json` straight away, so a run stopped part-way keeps what it finished.

The ingest also sets each entry's page parts from the library's list; check them in the draft. It reads stills only, so a moving site is recorded by hand, and whoever writes its `motion` block also lists its motion kinds there. Each entry is filed under an existing collection or, when it fits none, under a new collection the ingest drafts at the end of the collections list — keep it, or move the entry and delete it. `origin` and `licence` take the defaults for a screenshot of someone else's site. `proposed_manta_groups` is a suggestion that the review deletes, or promotes into `fit.manta` with a verdict; a commit still carrying it is refused.

Review the draft in a Claude session, run `node validate.js`, then commit. Refresh the page after.

## Making it yours

To start your own vault:

1. Open `data/gallery.json`
2. Set `meta.owner` to your name. A copied brief opens with a `Vault: ~/design-vault` line and gives each `Screenshot:` relative to it (`images/<file>`), so a brief pasted into a tracked record never carries a home-directory path.
3. Either keep my collections as starting points, or reset: set `"entries": []` and `"collections": []`, then rewrite `dna.constants` and `dna.never` for your own eye — the never-list matters as much as the constants
4. Delete my screenshots from `images/` if you want a clean slate, then ingest your own

Editing `data/gallery.json` by hand is always fine — it's the source of truth; run `node bundle.js` after, so the page opened from its folder shows the edit. Re-cluster by changing an entry's `collection`.

`data/styles.json` powers the **Style guide** view: the standard aesthetic families of the modern web (editorial minimalism, warm editorial, brutalism, …), each with recognition cues, vocabulary, canonical example sites, and its own COPY BRIEF button — borrowed language for looks your own inspo doesn't cover yet. A style that one of your looks shares lists that look with its reference count; click it to open the look. The look's details and every copied brief name the styles it shares.

## Structure

```
index.html          # interface markup
styles.css          # responsive gallery and dialogs
app.js              # the page: rendering, dialogs, selection and comparison
search.js           # the search box's matching rule, shared with its tests
view.js             # what the page shows and copies, shared with its tests
specimens.js        # 18 visual style specimens
specimens.css       # specimen styling
server.py           # read-only localhost static server
data/gallery.json   # entries + collections + House DNA — the taste database
data/styles.json    # reference aesthetic families of the modern web
data/vault-data.js  # derived by bundle.js — never edit by hand
data/round-log.jsonl # one row per design round: the founder's pick before the critic's, and the critic's
data/corrections-log.jsonl # one row per correction the founder makes in a round, in his words, and his ruling on it
data/calibration-log.jsonl # one row per calibration run: how far three fresh critics agreed with the founder, and each disagreement
images/             # screenshots, site stills and site recordings (.webm)
ingest.js           # claude -p vision extraction pipeline
validate.js         # the library's gate: refuses a malformed data/gallery.json
bundle.js           # copies the JSON into data/vault-data.js, so index.html opens with no server
round-log.js        # the round log's gate: refuses a malformed row, or a committed one rewritten
corrections-log.js  # the corrections log's gate: refuses a malformed row, or a committed one rewritten
critic-examples.js  # deals each design-round critic its own examples from the corrections log
calibration-packet.js # writes the folder a calibration run's critics read, refusing one that holds a verdict
calibration-critic.js # runs a calibration run's three critics, each a headless claude held to one round's folder, after a canary proves the hold
calibration-score.js # scores the critics against the founder's verdicts and writes the run's calibration-log row
calibration-log.js  # the calibration log's gate: refuses a malformed row, or a committed one rewritten
log-gate.js         # what the logs' gates share: reading a log from git, and their command line
release-check.js    # counts the plugin/ commits the marketplace pin has not released
ledger-upkeep.js    # warns at session start when the coverage ledger's re-scan is due, and checks the ledger
ledger-stop-numbers.py # the coverage ledger's stop numbers per area, recomputed at each re-scan
test/               # node --test suites and their fixtures
serve.bat           # Windows one-click server
plugin/             # the design-vault Claude Code plugin: skills design-round, design-critique, design-project and client-assets, the design-round pointer hook, design-round's Higgsfield render script and colour-key cut-out
skills/reference-to-design/ # installable workflow + prompt pack
examples/vantage.md # portable product brief and video sequence
docs/reference-to-design.md # skill installation and usage
```

## Data model

- **file** — `schema_version: 3` at the top level; entry fields are snake_case, while collection keys keep upstream's names (`deployFor`, `imageStyle`)
- **entry** — the validator requires `id, collection, origin, source, licence` and exactly one limb: a screenshot (`file`, with `vocabulary[], image_recipe, composition`) or a site (`url`, with `still, motion`). `file`, `still` and `motion.capture` (the site's recording) are each a bare file name under `images/`. Every entry names one or more `page_parts[]`, ids from the top-level `page_parts` list of 22 (`{ id, name, gloss }`): the part of a page it is about, plus any other worth taking, or `art-only` alone for a picture with no page around it. A site's `motion` block carries `kinds[]`, ids from the top-level `motion_kinds` list of five (`{ id, name, gloss }`): what sets off the motion it is kept for, plus any other worth taking. The list must be present and may be empty, as on a site kept for its still art. The gallery also reads `title, added, description, note, keywords[]`, optional `mood`, `fit.<project> { groups[], verdict, take, sheet_section }`, whose `groups` may be empty but is always a list, as is each project's own `groups`, optional `project`, which keeps the entry for that one project and allows no other project's `fit`, and, on a screenshot of a website, optional `site_url`, that site's address — never an individual artwork's page (#16). `url` and `site_url` must be http(s) addresses; the page links either as **Visit site ↗**
- **design_words** — the design-word list: `{ word, means[] }` pairs, each a word the founder types (one lower-case word, each once) and the words the data uses for it, which search also looks for. The copied brief never prints it
- **collection** — a deployable look → `vocabulary` block, `deployFor`, `risk` suggestion, `accent`, collection-level `imageStyle` template, and optional `styles[]`, the ids of the Style guide styles its pages share, each once. The link lives on the collection so `data/styles.json` stays as upstream ships it
- **dna** — `constants[]` + `never[]`, optionally included via My preferences
- **project** — `projects.<key>`: `name`, `rules` (its rules file as `<path> in <owner>/<repo>`), `verdicts[]`, `groups[]`, and optional `gate`, its gate file written like `rules` (#159)

## Validating the library

`node validate.js` checks `data/gallery.json` against schema v3, and each collection's `styles` against `data/styles.json`, and prints each fault led by its rule name; the rules are the `fault(...)` calls in `validate.js`. It exits 1 on any fault, and 2 on a usage error or a file it cannot read. `node --test` runs its tests, with no dependency to install.

`node --test` also covers the library page's logic and its server. `test/view.test.js` tests what the page shows and copies through `view.js`: the filters and their counts, the sort, the view hash, and every copied brief's lines. `test/server.test.js` runs `server.py` (needs `python3`) against a scratch vault and checks each refusal: a dot-path, however it is spelled, a directory listing, a path that climbs out of the vault, and any address but `127.0.0.1`. The page's look is checked by eye from screenshots, not by tests: it is presentation, which `AGENTS.md` keeps test effort off (#84).

The same check runs before every commit that stages `data/gallery.json`, `data/styles.json` or anything under `images/`, judging the staged copies (`node validate.js --staged`). A commit that stages either JSON file or `data/vault-data.js` runs `node bundle.js --staged`, which refuses a staged bundle that does not match the staged JSON. Both live in `.husky/pre-commit.local`, which workflow-core's `.husky/pre-commit` sources last. Git takes its hooks from `.husky/` because `core.hooksPath` is set to it, and a clone does not carry that setting: on a new clone, run workflow-core's `init-adopter.js` in the vault, or `git config core.hooksPath .husky` by hand.

`node round-log.js` checks `data/round-log.jsonl`, the design round's log of the founder's picks (design-round §3), and refuses any change to a row HEAD holds except adding its `final_pick`, or its `rejections` and `on_weakest` counts (#193). It also refuses a row dated from 16 Oct 2026 that lacks `splits` and `settled`, the gate check's counts (#234). A commit that stages the log runs `node round-log.js --staged` from `.husky/pre-commit.local`. Run by hand, it also prints `calibration due` once ten rows have landed since the last calibration run, the last row of `data/calibration-log.jsonl` (#167), and also where `--model` names another model than that run's, or where a commit after it changed a gate-list record in the vault's gate or in a project's gate given by `--gate` (#193, #232). A gate-list record is a live one that a script, the code or the gate critics answer (#323).

`node calibration-packet.js --manifest <file> --out <dir>` writes the packet a calibration run's critics read: each logged round's brief, gate list and candidates, and the principles of the corrections entries naming one. It refuses a packet holding a verdict field, a line of either log, a packed round's reason or entry's words, or a symbolic link; its header gives the manifest's shape.

`node corrections-log.js` checks `data/corrections-log.jsonl`, the founder's corrections in his own words (design-round §3), and refuses any change to a row HEAD holds except answering its `pending` ruling. Each row names its asset class and its `stance`, `kept` or `rejected`, by which `node critic-examples.js` deals each critic its own examples. A commit that stages the log runs `node corrections-log.js --staged` from `.husky/pre-commit.local`.

`node calibration-log.js` checks `data/calibration-log.jsonl`, one row per calibration run (#168), and refuses a malformed row, a run's figures that disagree with the disagreements listed under them, and any change to a row HEAD holds. A commit that stages the log runs `node calibration-log.js --staged` from `.husky/pre-commit.local`. The run itself is design-round's `references/calibration.md`.

`node ledger-upkeep.js` runs at every session start, beside `release-check.js`, and warns once `docs/coverage-ledger.json` is due its re-scan, by `docs/coverage-ledger-method.md` §7; it prints nothing before. `node ledger-upkeep.js --check` refuses a malformed method miss (§8), a scan date the warning cannot read (#267), a row whose verdict its criteria or the rule records it cites do not support (§4), and a fill job marked done with a row unfilled or a research line with no destination (§6, #266); `node --test` runs it on the real ledger, store and library, and `test/ledger-check.test.js` on one fixture per refusal.

`bash test/design-round-pointer.test.sh` tests the plugin's hook, `python3 test/cutout.test.py` its cut-out script (with numpy, Pillow and scipy), `python3 test/check-render.test.py` its render check, the size and the painted checkerboard (with numpy and Pillow), `python3 test/check-logo.test.py` its placed-logo check (with Playwright's Chromium and Pillow), `python3 test/check-clip.test.py` its generated-clip check, the length from the MP4 header and the loop request from the spend log, `python3 test/check-flow.test.py` its motion-flow sampler (with Playwright's Chromium, and Node for the `fall.js` easings it plays), `python3 test/check-flow-records.test.py` its motion records check, `check-flow.py --records` (with Playwright's Chromium, numpy and Pillow), `python3 test/check-frames.test.py` its frame check (with Playwright's Chromium), `python3 test/check-overlay.test.py` its mark-on-source overlay (with Playwright's Chromium, numpy, Pillow and scipy), `python3 test/check-measure.test.py` its line-length count (with Playwright's Chromium), `python3 test/face-profile.test.py` its face profile, the x-height, width, weight and optical size the type records read (with Playwright's Chromium, numpy and Pillow), `python3 test/contact-sheet.test.py` its motion contact sheet (with Playwright's Chromium and Pillow), `python3 test/check-layout.test.py` its width sweep and focal-box check (with Playwright's Chromium), `python3 test/check-access.test.py` its access check (with Playwright's Chromium, numpy and Pillow), `python3 test/check-access-contrast.test.py` the access check's contrast ladder, controls on photos, text on fills, chart marks, forced-colour edges and colour schemes (with Playwright's Chromium, numpy and Pillow), `python3 test/check-access-pointer.test.py` its targets-by-pointer mode (with Playwright's Chromium, numpy and Pillow), `python3 test/child.test.py` the runner every Chromium suite starts its checkers and runs its tests through, which on a run past its time limit prints where the run was stuck and its processes, and runs once more a run or a test whose browser crashed after earlyoom killed one of its renderers (with Playwright, for the greenlets it waits in), `python3 test/parts-map.test.py` its parts map (with Playwright's Chromium, numpy and Pillow), `python3 test/look.test.py` the settle critic's view tool (with Playwright's Chromium, numpy and Pillow), `python3 test/check-load.test.py` its load check (with Playwright's Chromium), `python3 test/check-load-files.test.py` its file check, the records on the fonts, icons and storage a page loads (with Playwright's Chromium), `python3 test/drive-overlay.test.py` the overlay driver the check scripts open menus, dialogs and popovers with (with Playwright's Chromium), `python3 test/conditions.test.py` the page-condition emulation its family scripts open pages under (with Playwright's Chromium), `python3 test/look-renders.test.py` the gate critics' look renders (with Playwright's Chromium, numpy and Pillow), `python3 test/check-seams.test.py` its seam check, the ground showing along each contact at device pixel ratios 1, 2 and 3 (with Playwright's Chromium, numpy and Pillow), `python3 test/drive-form.test.py` the form driver the checks fill and submit forms with (with Playwright's Chromium), `python3 test/drive-pointer.test.py` the pointer driver they hover, press, drag and wheel-scroll with (with Playwright's Chromium), `python3 test/probe.test.py` the shared page probe the family scripts read a page's DOM and computed style with (with Playwright's Chromium), `python3 test/check-cross.test.py` the cross-page probe that compares a site's pages and walks its flows (with Playwright's Chromium), `python3 test/check-dom.test.py` the DOM check that answers the DOM records through the probe (with Playwright's Chromium, numpy and Pillow), `python3 test/check-markup.test.py` the markup adapter that runs the vendored axe-core in a page (with Playwright's Chromium), `python3 test/check-style.test.py` the computed-style check that answers the style records through the probe (with Playwright's Chromium, numpy and Pillow), `python3 test/check-state.test.py` the driven-state checks that hover, press, type, submit, drag and wait on a page (with Playwright's Chromium and Pillow), and `python3 test/check-text.test.py` the text check that reads a page's words, characters, case and number formats (with Playwright's Chromium); `node --test` runs none of them, and runs the plugin's Node scripts' suites instead, `test/fall-check.test.js` among them, the timeline table's fall check.

`bash test/all.sh` runs every suite above and exits 1 if any fails. It runs up to three at once, through `test/run-lanes.sh` (#363): another starts only while the machine runs fewer than three suites, this run's own counted, and `MemAvailable` clears that count's rung, the ceiling and ladder of workflow-core's `docs/environment.md` §6. Each suite's output prints whole when it ends, with its wall time; `VAULT_SUITE_LANES=1` runs them one at a time. The suites start longest first, by the seconds each last took green, kept in `vault-suite-times/` in the git directory every worktree shares (#457). `bash test/all.sh --shard=k/n` runs every nth suite of the list from the kth on; workflow-core's lander runs the whole list as the four `fullTestShards` shards `.claude/workflow-core.json` declares, each a run of its own under its suite ceiling (workflow-core#2667), as one lane of every suite took 1403 s and each shard 200 to 498 s at load averages up to 30 (#462). It splits by place in the list, so the lander's `shard timings not refreshed — splitting by file count` line is expected. A commit's own gate run is not sharded. It is refused before any suite starts where the kept seconds of what it plans, laid longest first on the lanes the machine opens at that moment, end past workflow-core's suite ceiling, so a commit planning every suite on one lane gets that verdict at once rather than a kill at 840 s (#473); a lane that opens later is not counted, so a refused commit can pass once the machine is quieter. A red prints `FAIL <path>` on stderr for each failing test file, from the repo root, the line workflow-core's lander reads to bisect a red batch; `node --test` names its files through `test/failed-files.js`, its reporter. `bash test/all.sh <test file>…` runs only those files, a `.test.js` one under `node --test` and any other by the suite that runs it; a file on disk that no suite lists runs nothing and passes (#436). It is the declared `commands.test` in `.claude/workflow-core.json`, and `test/verdict-canary.test.js` its declared `commands.testCanary` (#491): while workflow-core's verdict proof stands, the lander's run before `main` moves is the gate and commits run no suite; while it is stale or failed, workflow-core's pre-commit runs it and refuses the commit on a red (#85). A missing tool, Python package or Chromium fails it before any suite runs, naming the install step; each Python one is checked only where a suite that needs it runs. `test/all.sh` keeps the one list of suites and what each needs, and its header names the edits a new suite still owes.

Inside a commit it runs only the suites the staged files can break (#146). `node --test` and the hook test always run. No selector here reads `docs/test-read-edges.json`, workflow-core's map of the tests that read each file, so a file losing readers there drops no test from a commit (#485). A Python suite runs only where a staged file is its test, a fixture it reads, or a script it runs or loads; `test/select-suites.js` reads these from the quoted paths in the tests and scripts themselves, so a checker that starts loading another the way they do now is followed without a list to update. A staged file under `test/` or `plugin/**/scripts/` that no suite is seen to read, or `test/all.sh`, `test/select-suites.js`, `package.json` or the lockfile, runs every suite; an edit to `test/all.sh`'s list of suites alone runs only the suites on the lines it added or changed (#363). workflow-core's commit gate runs it in a worktree of the commit's tree, without git's index variable, and the staged files still choose there by the `WFC_GATE_SEAT` the gate sets (#457). A merge is judged against each of its parents, from `MERGE_HEAD` or the gate's `WFC_MERGE_PARENTS`, and runs only the suites every parent's plan runs, since a suite whose files all match one parent passed there (#457). Run by hand, or inside a commit with `VAULT_ALL_SUITES=1`, it runs every suite; `bash test/all.sh --plan` prints what it would run and runs nothing.

`test/load/` holds load tests run by hand, never by the gate: `check-overlay-shot.py` (#136) and `sibling-shots.py` (#139) stall Chromium's screenshots beside CPU busy loops. A load test starts its busy loops at the lowest CPU priority (`nice -n 19`), has them end themselves at a ceiling, and prints before the first starts how many will run, for how long at most, and that other sessions' suites run slower meanwhile (#147). Both scripts take this from `loop()` in `check-overlay-shot.py`.

## Installing the plugin on a second machine

Documented, not yet run. `gh auth login` (git access over HTTPS comes from `gh auth git-credential`); `claude plugin marketplace add lucmoseley/claude-plugins`; `claude plugin install design-vault@lucmoseley`. Clone the vault itself (`git clone https://github.com/lucmoseley/design-vault.git ~/design-vault`) only on a machine where the inspiration generator or the gallery runs — a consumer that only runs design rounds needs the plugin alone. In each consumer project, add `Read(//home/lucmo/.claude/plugins/cache/**)` to the allow list in its `.claude/settings.local.json` so subagents can read the plugin's references; this is a per-machine step.

The design-round scripts need Python 3, four packages installed machine-wide at the versions `plugin/requirements.txt` pins, and Playwright's Chromium: `python3 -m pip install -r <plugin root>/requirements.txt`, then `python3 -m playwright install chromium`. The plugin root is the `installPath` that `~/.claude/plugins/installed_plugins.json` gives `design-vault@lucmoseley`, or `plugin/` in a vault clone. A script's install hint, where it prints one, names that file by its full path. Replacing this machine-wide route with a per-plugin install is weighed in `docs/research/plugin-dependency-route.md` (#244, #254).

## Releasing a plugin change

Before step 2, a change to a skill under `plugin/skills/` is pressure-tested with workflow-core's `pressure-test` skill: a baseline agent given the changed skill does what it now says (#85).

1. Commit the change in your session's worktree and land it: `node scripts/lib/resolve-core.js scripts/session-checkout.js land`. Run `node scripts/lib/resolve-core.js scripts/landing-status.js --wait` in the background, and go on only once it reports the commit landed, not dropped.
2. In `lucmoseley/claude-plugins`, bump the `sha` in `.claude-plugin/marketplace.json`'s `design-vault` entry to the `origin/main` commit that carries the change, and push.
3. Run `claude plugin marketplace update lucmoseley` then `claude plugin update design-vault@lucmoseley`. The plugin installs at user scope, so this updates every project on the machine, and each session started afterwards loads the new build. On this machine `~/.claude2/plugins` and `~/.claude3/plugins` are symlinks to `~/.claude/plugins`, so one run covers all three config dirs.

A vault commit reaches no consumer until step 2. `node release-check.js` counts the `plugin/` commits on `main` past the pin, and runs at every session start in this repo (`.claude/settings.json`). The `lucmoseley` marketplace does not auto-update unless switched on under `/plugin` → Marketplaces, so the session that releases runs step 3 itself.

Neither `plugin/.claude-plugin/plugin.json` nor the marketplace entry carries a `version`, and neither may: while one is set, a release that leaves it unchanged gets "already at the latest version" from step 3, whatever the sha, and no consumer moves. `claude plugin validate`'s missing-version warning is expected.

## License

The code is MIT © Chase (Chase AI) — see [LICENSE](LICENSE). Both image sets in `images/` — Chase's screenshots and the Manta references — are third-party: all rights to those designs remain with their creators, and no licence to them is held. This vault is private and never redistributes `images/`.
