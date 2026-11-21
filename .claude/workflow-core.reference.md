<!-- CORE-OWNED. Written by workflow-core's init and REWRITTEN on every bump.
     Do not edit, and never import it. -->

# Workflow core — reference

## Switching a module on

The modules are `roadmap`, `governance`, `site` and `mutation`. To switch one on, add it to `modules` in `.claude/workflow-core.json`, then run `node /home/lucmo/.claude/plugins/cache/workflow-core/workflow-core/3.0.0/scripts/init-adopter.js --no-plugin-install`: it keeps the founder, modules and plugin pin already written. Commit what it wrote; the new rules load at the next session. Until a subject's switch is set, `check-gate-switches.js` refuses every commit.

## Repo-health checks on demand

The repo-health checkers — stranded claims, stale queue markers and git locks, stray scratch among them — run on demand with `node /home/lucmo/.claude/plugins/cache/workflow-core/workflow-core/3.0.0/scripts/status-report.js`, or `--only <part of a name>` for some. A checker's finding never changes its exit code.

## Page checks under `site`

The core's one page check is `check-website-copy.js`, which refuses a commit staging `app/` that adds a banned tell from the brand sheet's §11. Add any other to `.husky/pre-commit.local`.

A commit-message refusal of this repo's own goes in `.husky/commit-msg.local`, which the core's commit-msg hook sources last, on every route, with the message file as `$1` and the route as `$route`.

## Plugin provenance

- url source, ref v3.0.0, HEAD c30e0173ccf997cd689871d2b7f97862422fde3e
- the seven husky hooks run from `WFC_PLUGIN_ROOT` in both branches, so this is what the last init or upgrade installed, not what the hooks run today
