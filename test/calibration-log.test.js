"use strict";
// calibration-log.js, which refuses a malformed calibration-log row and a commit that rewrites one (#168). --staged's
// reading of git is log-gate.js's, which round-log.test.js covers. Loosen one and a run's figures disagree with the
// disagreements listed under them, or "calibration due" counts from a row no count can read.
require("./no-git-env");
const assert = require("node:assert/strict");
const { execFileSync, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { test, after } = require("node:test");
const { checkCalibrationLog } = require("../calibration-log.js");
const installGate = require("./log-gate-files");

const ROOT = path.join(__dirname, "..");

const pickMiss = { kind: "pick", round: "lucmoseley/mmm-infra#9 r1", critic: "b", founder: "v2-slow", leader: "v1-arches", turned_on: "conversion lens" };
const falseFail = {
  kind: "question",
  round: "lucmoseley/mmm-infra#9 r1",
  critic: "a",
  candidate: "v2-slow",
  on: "vault.colour-look",
  founder: "yes",
  answer: "no",
  evidence: "the error state is red alone",
};
const entryMiss = {
  kind: "entry",
  round: "lucmoseley/mmm-infra#9 r1",
  critic: "c",
  candidate: "v1-arches",
  on: 1,
  principle: "the accent gold stays muted against the navy",
  rule: "unlanded",
  founder: "no",
  answer: "yes",
  evidence: "the gold reads muted beside the navy",
};
const run = {
  date: "2026-10-14",
  round_log_rows: 10,
  model: "claude-opus-5-5",
  canary_held_on: "2.1.299",
  rounds: ["lucmoseley/mmm-infra#9 r1"],
  pick: { agree: 2, of: 3 },
  questions: { "vault.colour-look": { agree: 1, of: 3, unsure: 1 }, "vault.proof": { agree: 3, of: 3, unsure: 0 } },
  entries: { 1: { agree: 2, of: 3, unsure: 0 } },
  new_questions: { "vault.load": { yes: 1, no: 2, unsure: 0 } },
  critics: [
    { unsure: 1, answers: 12 },
    { unsure: 0, answers: 12 },
    { unsure: 0, answers: 12 },
  ],
  disagreements: [pickMiss, falseFail, entryMiss],
  settles: { splits: 4, settled: 3 },
  where: "https://github.com/lucmoseley/design-vault-tracker/issues/168#issuecomment-1",
};
const later = { ...run, date: "2026-11-02", round_log_rows: 20, rounds: ["lucmoseley/mmm-infra#9 r2"], pick: { agree: 1, of: 1 }, questions: {}, entries: {}, disagreements: [] };
const log = (...rows) => rows.map((r) => JSON.stringify(r)).join("\n") + "\n";
const rules = (faults) => faults.map((f) => f.split(":")[0]);

test("a run with every kind of disagreement passes, and so does a clean run and an empty log", () => {
  assert.deepEqual(checkCalibrationLog(log(run, later)), []);
  assert.deepEqual(checkCalibrationLog(""), []);
});

test("each malformed field draws its own rule", () => {
  const cases = [
    [{ ...run, date: "14 Oct" }, "date"],
    [{ ...run, round_log_rows: -1 }, "round-log-rows"],
    [{ ...run, model: "" }, "model"],
    [{ ...run, where: undefined }, "where"],
    [{ ...run, settles: undefined }, "settles"],
    [{ ...run, settles: { splits: 2, settled: 3 } }, "settles"],
    [{ ...run, settles: { splits: 2 } }, "settles"],
    [{ ...run, new_questions: undefined }, "new-questions"],
    [{ ...run, new_questions: { "vault.load": { yes: 1, no: 2 } } }, "new-questions"],
    [{ ...run, new_questions: { "vault.load": { yes: 1, no: -1, unsure: 0 } } }, "new-questions"],
    [{ ...run, canary_held_on: "held" }, "canary"],
    [{ ...later, rounds: [] }, "rounds"],
    [{ ...later, rounds: ["mmm-infra#9 r1"] }, "rounds"],
    [{ ...later, rounds: [...run.rounds, ...run.rounds] }, "rounds"],
    [{ ...run, critics: run.critics.slice(1) }, "critics"],
    [{ ...run, critics: [{ unsure: 13, answers: 12 }, ...run.critics.slice(1)] }, "critics"],
    [{ ...run, firstpick: "v1" }, "unknown-field"],
    [{ ...run, pick: { agree: 2 } }, "pick"],
    [{ ...run, questions: [] }, "questions"],
    [{ ...run, entries: { "line 1": run.entries[1] }, disagreements: [pickMiss, falseFail] }, "entries"],
  ];
  for (const [row, rule] of cases) assert.deepEqual([...new Set(rules(checkCalibrationLog(log(row))))], [rule], JSON.stringify(row));
});

test("each figure's disagreements are listed, no more and no fewer", () => {
  const cases = [
    [{ ...run, pick: { agree: 3, of: 3 } }, "pick"],
    [{ ...run, pick: { agree: 1, of: 3 } }, "pick"],
    [{ ...run, questions: { ...run.questions, "vault.colour-look": { agree: 2, of: 3, unsure: 1 } } }, "questions"],
    [{ ...run, questions: { ...run.questions, "vault.proof": { agree: 3, of: 3, unsure: 1 } } }, "questions"],
    [{ ...run, entries: { 1: { agree: 3, of: 3, unsure: 0 } } }, "entries"],
    [{ ...run, entries: {}, disagreements: [pickMiss, falseFail, entryMiss] }, "entries"],
  ];
  for (const [row, rule] of cases) assert.deepEqual([...new Set(rules(checkCalibrationLog(log(row))))], [rule], JSON.stringify(row));
});

test("a disagreement that names no rule, round or critic of the run, or agrees after all, is refused", () => {
  const swap = (d) => ({ ...run, disagreements: run.disagreements.map((x) => (x.kind === d.kind ? d : x)) });
  const unknownKind = { ...run, disagreements: [{ ...pickMiss, kind: "lens" }, falseFail, entryMiss] };
  assert.deepEqual(rules(checkCalibrationLog(log(unknownKind))), ["disagreement", "pick"], "an unknown kind, which leaves the pick's miss unlisted");
  const cases = [
    swap({ ...pickMiss, leader: "v2-slow" }),
    swap({ ...pickMiss, turned_on: "" }),
    swap({ ...pickMiss, round: "lucmoseley/mmm-infra#9 r7" }),
    swap({ ...pickMiss, critic: "d" }),
    swap({ ...falseFail, answer: "yes" }),
    swap({ ...falseFail, answer: "unsure" }),
    swap({ ...falseFail, evidence: "" }),
    swap({ ...entryMiss, answer: "no" }),
    swap({ ...entryMiss, rule: "pending" }),
    swap({ ...entryMiss, principle: undefined }),
    swap({ ...entryMiss, words: "the gold is too yellow" }),
  ];
  for (const row of cases) assert.deepEqual([...new Set(rules(checkCalibrationLog(log(row))))], ["disagreement"], JSON.stringify(row.disagreements));
  assert.deepEqual(checkCalibrationLog(log(swap({ ...entryMiss, rule: "rule: vault.proof" }))), [], "a landed rule");
  assert.deepEqual(checkCalibrationLog(log(swap({ ...entryMiss, founder: "yes", answer: "no" }))), [], "a trait he kept, which the critic said it breaks");
  assert.deepEqual(checkCalibrationLog(log(swap({ ...pickMiss, founder: null }))), [], "a round he named no leader in");
});

test("the log only grows: HEAD's rows stand unchanged, and no run counts fewer round-log rows than the one before", () => {
  const head = log(run);
  assert.deepEqual(checkCalibrationLog(log(run, later), head), [], "appending a run");
  assert.deepEqual(rules(checkCalibrationLog(log({ ...run, where: "session f521adbb, 2026-10-14" }, later), head)), ["rewrite"]);
  assert.deepEqual(rules(checkCalibrationLog(log(later), head)), ["rewrite"], "dropping a run");
  assert.deepEqual(rules(checkCalibrationLog(log(later, run))), ["round-log-rows"], "a run counted from fewer rows than the one before");
});

const scratch = [];
after(() => {
  for (const dir of scratch) fs.rmSync(dir, { recursive: true, force: true });
});

test("the pre-commit refuses a staged log that rewrites a run and lets an appended run through", () => {
  const repo = fs.mkdtempSync(path.join(os.tmpdir(), "calibration-log-hook-"));
  scratch.push(repo);
  installGate(repo, "calibration-log.js");
  fs.mkdirSync(path.join(repo, ".husky"));
  fs.copyFileSync(path.join(ROOT, ".husky/pre-commit.local"), path.join(repo, ".husky/pre-commit.local"));
  fs.mkdirSync(path.join(repo, "data"));
  const file = path.join(repo, "data", "calibration-log.jsonl");
  const git = (...args) =>
    execFileSync("git", ["-c", "core.hooksPath=/dev/null", "-c", "user.name=t", "-c", "user.email=t@t", ...args], { cwd: repo, stdio: "pipe" });
  const hook = () => spawnSync("sh", [".husky/pre-commit.local"], { cwd: repo, encoding: "utf8" });
  git("init", "-q");
  fs.writeFileSync(file, log(run));
  git("add", "data");
  git("commit", "-q", "-m", "first run");

  fs.writeFileSync(file, log({ ...run, pick: { agree: 3, of: 3 }, disagreements: [falseFail, entryMiss] }));
  git("add", "data");
  const refused = hook();
  assert.equal(refused.status, 1, refused.stdout);
  assert.match(refused.stderr, /calibration-log\.js: the staged data\/calibration-log\.jsonl refused/);
  assert.match(refused.stderr, /rewrite: line 1 changes HEAD's row for the run of 2026-10-14/);

  fs.writeFileSync(file, log(run, later));
  git("add", "data");
  const clean = hook();
  assert.equal(clean.status, 0, clean.stderr);
  assert.match(clean.stdout, /is a valid calibration log — 2 row\(s\)/);
});
