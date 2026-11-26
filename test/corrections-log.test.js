"use strict";
require("./no-git-env");
const assert = require("node:assert/strict");
const { execFileSync, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { test, after } = require("node:test");
const { checkCorrectionsLog } = require("../corrections-log.js");
const { runInProcess } = require("./core-run-in-process.js");
const installGate = require("./log-gate-files");

const ROOT = path.join(__dirname, "..");

const trait = {
  date: "2026-10-13",
  project: "mmm-infra",
  asset: "web-surface",
  where: "https://github.com/lucmoseley/mmm-infra/issues/9#issuecomment-1",
  candidate: "rounds/hero-r2 v3-water-runs",
  words: "the gold is too yellow, it looks cheap",
  stance: "rejected",
  principle: "the accent gold stays muted against the navy",
  missed_by: "critic",
  ruling: "pending",
};
const brief = { ...trait, candidate: null, words: "it's for the owners, not the guests", stance: "kept", principle: "the page speaks to the owner", missed_by: "no rule", ruling: "no rule" };
const ruled = { ...trait, date: "2026-10-14", words: "no drop shadows on the cards", principle: "cards sit flat", missed_by: "gate", ruling: "rule: mmm-infra rules §3 'cards sit flat'" };
const log = (...rows) => rows.map((r) => JSON.stringify(r)).join("\n") + "\n";
const rules = (faults) => faults.map((f) => f.split(":")[0]);

test("a pending row, a no-rule row about no candidate and a ruled row pass, and so does an empty log", () => {
  assert.deepEqual(checkCorrectionsLog(log(trait, brief, ruled)), []);
  assert.deepEqual(checkCorrectionsLog(""), []);
});

test("each malformed row draws its own rule", () => {
  const cases = [
    [{ ...trait, date: "2026-02-30" }, "date"],
    [{ ...trait, date: "13 Oct" }, "date"],
    [{ ...trait, project: "" }, "project"],
    [{ ...trait, where: " " }, "where"],
    [{ ...trait, words: undefined }, "words"],
    [{ ...trait, principle: 3 }, "principle"],
    [{ ...trait, candidate: undefined }, "candidate"],
    [{ ...trait, candidate: "" }, "candidate"],
    [{ ...trait, candidate: "rounds/hero-r2/v3-water-runs" }, "candidate"],
    [{ ...trait, candidate: "hero-r2 v3-water-runs" }, "candidate"],
    [{ ...trait, asset: "website" }, "asset"],
    [{ ...trait, asset: undefined }, "asset"],
    [{ ...trait, stance: "liked" }, "stance"],
    [{ ...trait, stance: null }, "stance"],
    [{ ...trait, missed_by: "the critic" }, "missed-by"],
    [{ ...trait, missed_by: null }, "missed-by"],
    [{ ...trait, ruling: "yes" }, "ruling"],
    [{ ...trait, ruling: "rule:" }, "ruling"],
    [{ ...trait, ruling: "rule: " }, "ruling"],
    [{ ...trait, ruling: null }, "ruling"],
    [{ ...trait, said: "x" }, "unknown-field"],
  ];
  for (const [row, rule] of cases) assert.deepEqual(rules(checkCorrectionsLog(log(row))), [rule], JSON.stringify(row));
});

test("a line that is not one JSON object is refused, and so are the same words from the same place twice", () => {
  assert.deepEqual(rules(checkCorrectionsLog(`${JSON.stringify(trait)}\n{ half`)), ["json"]);
  assert.deepEqual(rules(checkCorrectionsLog("[1]\n")), ["json"]);
  assert.deepEqual(rules(checkCorrectionsLog(log(trait, { ...trait, principle: "another reading" }))), ["duplicate-entry"]);
  assert.deepEqual(checkCorrectionsLog(log(trait, { ...trait, where: "session 2026-10-14" })), [], "the same words said again elsewhere");
  assert.deepEqual(checkCorrectionsLog(log(trait, { ...trait, candidate: "rounds/hero-r2 v1-arches" })), [], "the same words about another candidate");
});

test("the log only grows: HEAD's rows stand, his words never change, and only a pending ruling may be answered (#166)", () => {
  const head = log(trait, brief);
  assert.deepEqual(checkCorrectionsLog(log(trait, brief, ruled), head), [], "appending a row");
  assert.deepEqual(checkCorrectionsLog(log({ ...trait, ruling: "no rule" }, brief), head), [], "answering pending with no rule");
  assert.deepEqual(checkCorrectionsLog(log({ ...trait, ruling: "rule: craft-3" }, brief), head), [], "answering pending with a rule");

  assert.deepEqual(rules(checkCorrectionsLog(log({ ...trait, words: "the gold is too yellow" }, brief), head)), ["words"], "trimming his words");
  assert.deepEqual(rules(checkCorrectionsLog(log({ ...trait, ruling: "maybe" }, brief), head)), ["ruling"], "answering with no ruling");
  assert.deepEqual(rules(checkCorrectionsLog(log({ ...brief, ruling: "rule: craft-3" }), log(brief))), ["rewrite"], "overturning an answered ruling");
  assert.deepEqual(rules(checkCorrectionsLog(log({ ...ruled, ruling: "pending" }), log(ruled))), ["rewrite"], "taking a ruling back to pending");
  assert.deepEqual(rules(checkCorrectionsLog(log({ ...trait, principle: "gold reads cheap" }, brief), head)), ["rewrite"], "rewording the principle");
  assert.deepEqual(rules(checkCorrectionsLog(log({ ...trait, principle: "gold reads cheap", ruling: "no rule" }, brief), head)), ["rewrite"], "rewording while answering");
  assert.deepEqual(rules(checkCorrectionsLog(log(trait), head)), ["rewrite"], "dropping the last row");
  assert.deepEqual(rules(checkCorrectionsLog(log(brief), head)), ["words", "rewrite"], "dropping the first row shifts both");
});

const scratch = [];
after(() => {
  for (const dir of scratch) fs.rmSync(dir, { recursive: true, force: true });
});

function scratchRepo(prefix) {
  const repo = fs.mkdtempSync(path.join(os.tmpdir(), prefix));
  scratch.push(repo);
  installGate(repo, "corrections-log.js");
  fs.mkdirSync(path.join(repo, ".husky"));
  fs.copyFileSync(path.join(ROOT, ".husky/pre-commit.local"), path.join(repo, ".husky/pre-commit.local"));
  fs.mkdirSync(path.join(repo, "data"));
  const git = (...args) =>
    execFileSync("git", ["-c", "core.hooksPath=/dev/null", "-c", "user.name=t", "-c", "user.email=t@t", ...args], { cwd: repo, stdio: "pipe" });
  git("init", "-q");
  return { repo, git, file: path.join(repo, "data", "corrections-log.jsonl") };
}

test("--staged judges the index's log against HEAD's, not the working tree's", () => {
  const { repo, git, file } = scratchRepo("corrections-log-staged-");
  const staged = () => runInProcess(path.join(repo, "corrections-log.js"), ["--staged"], { cwd: repo });

  assert.equal(staged().status, 0, staged().stderr);

  fs.writeFileSync(file, log(trait));
  git("add", "data");
  git("commit", "-q", "-m", "first correction");

  fs.writeFileSync(file, log({ ...trait, words: "too yellow" }));
  assert.equal(staged().status, 0, staged().stderr);

  git("add", "data");
  const refused = staged();
  assert.equal(refused.status, 1);
  assert.match(refused.stderr, /words: line 1 changes his words in HEAD's row for 2026-10-13 mmm-infra/);

  fs.writeFileSync(file, log({ ...trait, ruling: "no rule" }));
  git("add", "data");
  fs.writeFileSync(file, "{ half");
  assert.equal(staged().status, 0, staged().stderr);

  const plain = runInProcess(path.join(repo, "corrections-log.js"), [], { cwd: repo });
  assert.equal(plain.status, 1);
  assert.match(plain.stderr, /json: line 1/);
});

test("the pre-commit refuses a staged log with a fault and lets a clean one through", () => {
  const { repo, git, file } = scratchRepo("corrections-log-hook-");
  fs.writeFileSync(file, log(trait));
  git("add", "data");
  git("commit", "-q", "-m", "first correction");
  const hook = () => spawnSync("sh", [".husky/pre-commit.local"], { cwd: repo, encoding: "utf8" });

  fs.writeFileSync(file, log({ ...trait, words: "too yellow" }));
  git("add", "data");
  const refused = hook();
  assert.equal(refused.status, 1, refused.stdout);
  assert.match(refused.stderr, /corrections-log\.js: the staged data\/corrections-log\.jsonl refused/);
  assert.match(refused.stderr, /words: line 1 changes his words in HEAD's row for 2026-10-13 mmm-infra — they are kept verbatim; log what he says now as a new row/);

  fs.writeFileSync(file, log(trait, brief));
  git("add", "data");
  const clean = hook();
  assert.equal(clean.status, 0, clean.stderr);
  assert.match(clean.stdout, /is a valid corrections log — 2 row\(s\)/);
});

test("--staged with a path is a usage error", () => {
  const result = runInProcess(path.join(ROOT, "corrections-log.js"), ["--staged", "--log", "x"]);
  assert.equal(result.status, 2);
  assert.match(result.stderr, /--staged reads the index's and HEAD's log; it takes no paths/);
});

test("--staged outside a git repo is an error, never an empty log", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "corrections-log-nogit-"));
  scratch.push(dir);
  installGate(dir, "corrections-log.js");
  const result = runInProcess(path.join(dir, "corrections-log.js"), ["--staged"], { cwd: dir });
  assert.equal(result.status, 2, result.stdout);
  assert.match(result.stderr, /could not read the log — /);
});
