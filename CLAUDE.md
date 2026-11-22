# CLAUDE.md

@AGENTS.md
@.claude/workflow-core.md

<!-- Repo-owned. workflow-core's init writes this file ONCE and never touches it
     again. Everything below is yours to edit. The workflow rules live in
     `.claude/workflow-core.md`, which is rewritten on every core bump — do not
     edit that file; override through `.claude/workflow-core.json` (`overrides`,
     `disabled`) instead. -->

## Project

design-vault — the founder's private design vault: the portable design method as the `design-vault` Claude Code plugin (`plugin/`) and one inspiration library (`data/gallery.json`, `images/`) serving every project the founder designs, seeded from `cth9191/taste-vault`. Founder: Luc Moseley.
State: being built — the build order is the spec lucmoseley/mantahostels#3631.

## Ground truth

<!-- Where the truth about THIS project lives, and which file wins when two disagree.
     Keep it to what a session must know before its first edit. -->

## Commands

<!-- Only what `.claude/workflow-core.json`'s `commands.*` declares. A command absent
     there means "this repo has none", and the core's checks skip it saying so. -->

- `bash test/all.sh` runs every vault suite; while its verdict proof stands the lander's run before `main` moves is the gate and commits run none (#491); while the proof is stale or failed the pre-commit gate runs it and refuses a red (#85), running there only the suites the staged files can break — `VAULT_ALL_SUITES=1` forces all (#146, README §Validating the library). `node --test` alone runs only the JavaScript suites.

## Conventions specific to this repo

- **Two readers, two registers.** The founder reads `title`, `description`, `note`, `fit.<project>.take` and a collection's `name`, `description` and `deployFor`: plain English a non-designer follows, any design term glossed in a few words. `image_recipe`, `vocabulary`, `composition` and a collection's `imageStyle`, `vocabulary` and `risk` feed an AI and stay technical (design-vault#2 Q6).
- **A `note` carries the founder's intent, not the picture's contents.** Draft it from his own words about why he saved the reference — the ten-site note in lucmoseley/mantahostels#3037, the background-art principles in lucmoseley/mantahostels#3057 — and lead with what he was after: a feel, a behaviour, one part. Where no words of his exist, name the overall feel, hedge at most one likely part, and say no note from him was found; he saved many references "for specific small parts of them, or their vague overall 'vibe'". A review put to him asks one plain question per reference.
- **A session that lands a commit touching `plugin/` releases it before it ends**, by README §Releasing a plugin change. `release-check.js` prints the unreleased count at session start; it reports and never refuses (#58).

<!-- Formatter of record, source layout, deploy trigger, and any rule that exists
     only because of THIS product. Workflow-wide conventions are already in
     `.claude/workflow-core.md`; do not restate them. -->

## Gotchas specific to this repo

<!-- Things a session will get wrong here that it would not get wrong elsewhere. -->

<!-- guard-registry:begin -->
<!-- Every rule here carries **Enforced** / **Advisory** / **Unenforced** / **Unenforceable**; `scripts/check-guard-registry.js` gates it, and this region is the one CLAUDE.md must carry. -->

<!-- A rule of THIS repo's with a guard behind it goes here. -->
<!-- guard-registry:end -->
