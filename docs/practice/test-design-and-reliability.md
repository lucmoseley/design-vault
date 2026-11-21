# Practice: test-design-and-reliability
Researched: 2026-11-16

Scope: tests that fail for a cause outside the code under test, and when a gate may run such a test again. Each source has one tier: [standard or field body], [named expert], [survey or curated list] or [unverified]. A tool's own docs earn [standard or field body] only for what that tool does.

## 1. Re-running a failed test
- GitLab CI retries a failed job up to 2 more times. `retry:when` limits the retry to named failure types, such as `runner_system_failure`, and `retry:exit_codes` to named exit codes, such as 137 for a SIGKILL. With neither set, every failure type is retried. [standard or field body] GitLab CI/CD YAML reference, `retry` and `retry:when`.
- pytest-rerunfailures' `--only-rerun` re-runs only failures whose error matches a listed expression; `--rerun-except` is the inverse. [standard or field body] pytest-rerunfailures README.
- Google's TAP re-runs a test only where it is marked flaky or the author asks. [unverified] An unsigned reply on the Google Testing Blog post "Flaky Tests at Google and How We Mitigate Them" (2016-05). It sets no default.
- A test that fails and then passes on a re-run leaves no way to tell a bug from noise, so people stop reacting to red. Quarantine such a test and fix it quickly; do not let a re-run hide it. [named expert] Martin Fowler, "Eradicating Non-Determinism in Tests".

**Default:** none from these sources. This repo's re-run below rests on design-vault#431's measurement. [unverified]

## 2. Admission and re-runs answer different causes
- Admitting fewer jobs while memory is low guards the moment a job starts. Memory that falls after admission, from work the gate does not govern, is outside its reach. [unverified] Derived from design-vault#431's measurement. It sets no default.

## In this repo
- `test/child.py` re-runs a gate suite's child once when it failed with Playwright's `Target crashed` and earlyoom's journal names one of that child's renderers, killed while it lived, and says so on stderr (#431).
- `child.main()` re-runs once, on the same evidence, a test that drives a browser in the suite's own process; every Chromium suite in `test/all.sh` runs its tests through it, which `test/chromium-suites.test.js` pins (#438).
