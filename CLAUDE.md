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

- A review of library references put to the founder asks one plain question per reference.

<!-- Formatter of record, source layout, deploy trigger, and any rule that exists
     only because of THIS product. Workflow-wide conventions are already in
     `.claude/workflow-core.md`; do not restate them. -->

## Gotchas specific to this repo

<!-- Things a session will get wrong here that it would not get wrong elsewhere. -->

<!-- guard-registry:begin -->
<!-- Every rule here carries **Enforced** / **Advisory** / **Unenforced** / **Unenforceable**; `scripts/check-guard-registry.js` gates it, and this region is the one CLAUDE.md must carry. -->

<!-- A rule of THIS repo's with a guard behind it goes here. -->
<!-- guard-registry:end -->
