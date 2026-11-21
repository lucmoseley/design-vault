# Critic transcripts: degraded mode and partial reads (design-vault #212)

Questions:
1. Does the critic start two sub-agents for impeccable critique Assessment A and Assessment B, or does it run in one context (degraded)?
2. Does the critic read each rule file fully or in part?

## Rows

### R1. mmm-infra, aqueduct storyboard round 1 (production, design-round critic)
- Session: ~/.claude3/projects/-home-lucmo-mmm-infra/8ad05cae-f462-41f7-b908-8e50850a442f/subagents/agent-a5e3c76335f3b2f67.jsonl
- Date: 2026-10-04. Model: claude-opus-5-5. Dispatched by: design-round §4 fresh critic.
- Sub-agents for A and B: NEITHER. The critic did not run impeccable critique at all. Its report says, for each candidate: "Vendored critique: not run, because impeccable is not loaded. Audit not run." No DEGRADED line.
- Rule files read: design-critique SKILL.md (Skill call, full body injected); brand sheet `docs/brand/brand-sheet.md` (whole, 46 lines). critique.md: not read. audit.md: not read. gate.md: not read. house-principles.md: not read.
- Scripts: none of check-layout.py / check-measure.py. It wrote its own Playwright and PIL contrast scripts.
- Context at verdict: about 140,800 input tokens.


## Findings by the dispatching session (cd0197f4)

Method: a script parsed every subagent transcript under the three config dirs (~/.claude, ~/.claude2, ~/.claude3), each Manta session counted once. A run counts as a production critic when the project is mmm-infra or mantahostels, its dispatch prompt names design-critique, "fresh critic" or "critique critic", or it calls the critique skill, and it is not a code-review axis.

- **Runs found:** 50 production critic runs. 46 are from one mmm-infra session (631cff6d, 5 Oct 2026, site-look rounds). The others are 8c2c8bf9 and 8ad05cae (4 Oct), 3180c97e (13 Oct, Sonnet 5.5) and fdd20a08 (Manta, 6 Sep). Model: claude-opus-5-5 in 48.
- **Sub-agents:** no critic run started a sub-agent (0 of 50).
- **impeccable critique:** 21 of 50 ran it. All 21 ran Assessment A and Assessment B in one context. None printed the `⚠️ DEGRADED: single-context` banner that critique.md requires. 29 of 50 did not run impeccable. These were mostly re-check critics and critics that had a per-candidate brief file.
- **Where the split did run:** on Manta (6 Sep 2026, fdd20a08) a main session ran `impeccable critique` and started Assessment A as an isolated sub-agent. One Manta run (21 Aug, 275eb05a) printed the DEGRADED banner.
- **critique.md reads:** 18 reads in the runs that ran impeccable. 17 were `cat` through Bash. In 16 of those 17, the output was more than the Bash limit, so the critic got a 2 KB preview and a saved-file path. Afterwards, 13 of them used Read on the saved file (whole: 806 lines is less than the Read default). 3 used `sed -n 1,200p` or `20,200p` and then grep, so they read part of the file. One read `sed -n 20,300p` directly. Result: about 14 of 18 read the file whole and 4 read part. The two-level-chain risk (B6) did not occur in this form. The cat-then-preview path is a different risk.
- **audit.md:** read whole (cat or Read) in most runs. 4 used `sed -n 1,114p` to `1,140p` (the file is 137 lines, so these were almost whole).
- **design-critique's gate.md, house-principles.md, surface-styling.md:** no production critic read them. All three were first committed on 14 Oct 2026 (25fdc3c, d9b846e, 6cfa8d8). The only production critic run after that date is 3180c97e (13 Oct). So **the critic's current rule load has not run in production**. All evidence about that load comes from pressure-test and trial critics.
- **Context at the verdict** (input + cache read + cache write on the last assistant turn): median about 170,000 tokens, range 31,000 to 261,000. This is about 1.7 times #211's estimate of 95,000 to 110,000. Images, script output and tool turns make up most of it, not the rule files.

**Meaning for #212:** partial reads of critique.md are a small risk (4 of 18).

**Bound:** all 129 matching subagent transcripts were parsed by script (tool calls, last usage and assistant text only). The 50 production rows were listed in full. Tool results were inspected only for the critique.md `cat` calls in sessions 631cff6d and 8c2c8bf9. The two Manta DEGRADED hits were read in their first prompt and banner lines only.
