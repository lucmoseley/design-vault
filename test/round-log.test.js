"use strict";
require("./no-git-env");
const assert = require("node:assert/strict");
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { test, after } = require("node:test");
const { checkRoundLog } = require("../round-log.js");
const { runInProcess } = require("./core-run-in-process.js");
const installGate = require("./log-gate-files");

const SCRIPT = path.join(__dirname, "..", "round-log.js");

const picked = {
  date: "2026-10-13",
  project: "mmm-infra",
  ticket: "lucmoseley/mmm-infra#9",
  round: 2,
  first_pick: "v3-water-runs",
  reason: "the water reads as one line",
  confidence: 70,
  critic_pick: "v1-arches",
  agree: false,
};
const noLeader = { ...picked, round: 1, first_pick: null, reason: "none carries the weight yet", confidence: null, agree: null };
const changed = { ...picked, round: 3, first_pick: "v2-slow", critic_pick: "v2-slow", agree: true, final_pick: "v1-fast" };
const counted = { ...picked, round: 4, rejections: 3, on_weakest: 1 };
const settled = { ...picked, round: 5, splits: 4, settled: 3 };
const log = (...rows) => rows.map((r) => JSON.stringify(r)).join("\n") + "\n";
const rules = (faults) => faults.map((f) => f.split(":")[0]);

test("a leader row, a no-leader row, a changed-pick row and rows with weakest-part or settle counts pass, and so does an empty log", () => {
  assert.deepEqual(checkRoundLog(log(picked, noLeader, changed, counted, settled)), []);
  assert.deepEqual(checkRoundLog(log({ ...counted, rejections: 0, on_weakest: 0 })), []);
  assert.deepEqual(checkRoundLog(log({ ...settled, splits: 0, settled: 0 })), []);
  assert.deepEqual(checkRoundLog(""), []);
});

test("a round dated after #170's landing day must carry the settle counts, so a skipped count is not read as no splits (#234)", () => {
  assert.deepEqual(checkRoundLog(log({ ...picked, date: "2026-10-15" })), []);
  assert.deepEqual(checkRoundLog(log({ ...settled, date: "2026-10-16", splits: 0, settled: 0 })), []);
  for (const date of ["2026-10-16", "2027-01-02"]) assert.deepEqual(rules(checkRoundLog(log({ ...picked, date }))), ["settle"], date);
  assert.deepEqual(rules(checkRoundLog(log({ ...picked, date: "2026-10-16", splits: 2 }))), ["settle"]);
  assert.deepEqual(rules(checkRoundLog(log({ ...picked, date: "2026-10-16", settled: 0 }))), ["settle"]);
});

test("each malformed row draws its own rule", () => {
  const cases = [
    [{ ...picked, date: "2026-02-30" }, "date"],
    [{ ...picked, date: "13 Oct" }, "date"],
    [{ ...picked, project: "" }, "project"],
    [{ ...picked, ticket: "mmm-infra#9" }, "ticket"],
    [{ ...picked, round: 0 }, "round"],
    [{ ...picked, round: 1.5 }, "round"],
    [{ ...noLeader, critic_pick: 3 }, "pick"],
    [{ ...picked, reason: " " }, "reason"],
    [{ ...picked, confidence: null }, "confidence"],
    [{ ...picked, confidence: 0.7 * 200 }, "confidence"],
    [{ ...noLeader, confidence: 50 }, "confidence"],
    [{ ...picked, agree: true }, "agree"],
    [{ ...picked, critic_pick: "v3-water-runs" }, "agree"],
    [{ ...picked, critic_pick: null }, "agree"],
    [{ ...noLeader, agree: false }, "agree"],
    [{ ...picked, final_pick: "v3-water-runs" }, "final-pick"],
    [{ ...picked, final_pick: null }, "final-pick"],
    [{ ...picked, firstpick: "v1" }, "unknown-field"],
    [{ ...picked, rejections: 2 }, "weakest"],
    [{ ...picked, on_weakest: 0 }, "weakest"],
    [{ ...counted, on_weakest: 4 }, "weakest"],
    [{ ...counted, rejections: -1, on_weakest: 0 }, "weakest"],
    [{ ...counted, on_weakest: 0.5 }, "weakest"],
    [{ ...counted, rejections: "3" }, "weakest"],
    [{ ...picked, splits: 2 }, "settle"],
    [{ ...picked, settled: 0 }, "settle"],
    [{ ...settled, settled: 5 }, "settle"],
    [{ ...settled, splits: -1, settled: 0 }, "settle"],
    [{ ...settled, settled: 1.5 }, "settle"],
  ];
  for (const [row, rule] of cases) assert.deepEqual(rules(checkRoundLog(log(row))), [rule], JSON.stringify(row));
});

test("a line that is not one JSON object is refused, and so is a second row for one round", () => {
  assert.deepEqual(rules(checkRoundLog(`${JSON.stringify(picked)}\n{ half`)), ["json"]);
  assert.deepEqual(rules(checkRoundLog("[1]\n")), ["json"]);
  assert.deepEqual(rules(checkRoundLog(log(picked, { ...picked, first_pick: "v1-arches", agree: true }))), ["duplicate-round"]);
});

test("the log only grows: HEAD's rows stand, and only a final_pick or the weakest-part counts may be added to one (#95, #193)", () => {
  const head = log(picked, noLeader);
  assert.deepEqual(checkRoundLog(log(picked, noLeader, changed), head), [], "appending a row");
  assert.deepEqual(checkRoundLog(log({ ...picked, final_pick: "v1-arches" }, noLeader), head), [], "adding a final_pick");
  assert.deepEqual(checkRoundLog(log({ ...picked, rejections: 2, on_weakest: 2 }, noLeader), head), [], "adding the weakest-part counts");
  const headCounted = log(counted);
  assert.deepEqual(rules(checkRoundLog(log({ ...counted, on_weakest: 2 }), headCounted)), ["rewrite"], "changing a count");
  assert.deepEqual(rules(checkRoundLog(log({ ...counted, rejections: undefined, on_weakest: undefined }), headCounted)), ["rewrite"], "removing the counts");

  const rewritten = { ...picked, first_pick: "v1-arches", agree: true };
  assert.deepEqual(rules(checkRoundLog(log(rewritten, noLeader), head)), ["rewrite"], "rewriting his first pick");
  assert.deepEqual(rules(checkRoundLog(log(noLeader), head)), ["rewrite", "rewrite"], "dropping the first row shifts both");
  assert.deepEqual(rules(checkRoundLog(log(picked), head)), ["rewrite"], "dropping the last row");
  const headChanged = log(changed);
  assert.deepEqual(rules(checkRoundLog(log({ ...changed, final_pick: "v3-other" }), headChanged)), ["rewrite"], "changing a final_pick");
  assert.deepEqual(rules(checkRoundLog(log({ ...changed, final_pick: undefined }), headChanged)), ["rewrite"], "removing a final_pick");
});

const scratch = [];
after(() => {
  for (const dir of scratch) fs.rmSync(dir, { recursive: true, force: true });
});

test("--staged judges the index's log against HEAD's, not the working tree's", () => {
  const repo = fs.mkdtempSync(path.join(os.tmpdir(), "round-log-staged-"));
  scratch.push(repo);
  const git = (...args) =>
    execFileSync("git", ["-c", "core.hooksPath=/dev/null", "-c", "user.name=t", "-c", "user.email=t@t", ...args], { cwd: repo, stdio: "pipe" });
  installGate(repo, "round-log.js");
  fs.mkdirSync(path.join(repo, "data"));
  const file = path.join(repo, "data", "round-log.jsonl");
  const staged = () => runInProcess(path.join(repo, "round-log.js"), ["--staged"], { cwd: repo });
  git("init", "-q");

  assert.equal(staged().status, 0, staged().stderr);

  fs.writeFileSync(file, log(picked));
  git("add", "data");
  git("commit", "-q", "-m", "first round");

  fs.writeFileSync(file, log({ ...picked, first_pick: "v1-arches", agree: true }));
  assert.equal(staged().status, 0, staged().stderr);

  git("add", "data");
  const refused = staged();
  assert.equal(refused.status, 1);
  assert.match(refused.stderr, /rewrite: line 1 changes HEAD's row for lucmoseley\/mmm-infra#9 r2/);

  fs.writeFileSync(file, log(picked, noLeader));
  git("add", "data");
  fs.writeFileSync(file, "{ half");
  assert.equal(staged().status, 0, staged().stderr);

  const plain = runInProcess(path.join(repo, "round-log.js"), [], { cwd: repo });
  assert.equal(plain.status, 1);
  assert.match(plain.stderr, /json: line 1/);
});

test("--staged with a path is a usage error", () => {
  const result = runInProcess(SCRIPT, ["--staged", "--log", "x"]);
  assert.equal(result.status, 2);
  assert.match(result.stderr, /--staged reads the index's and HEAD's log; it takes no paths/);
});

test("--staged outside a git repo is an error, never an empty log", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "round-log-nogit-"));
  scratch.push(dir);
  installGate(dir, "round-log.js");
  const result = runInProcess(path.join(dir, "round-log.js"), ["--staged"], { cwd: dir });
  assert.equal(result.status, 2, result.stdout);
  assert.match(result.stderr, /could not read the log — /);
});

test("a clean run prints calibration due at ten rows since the last calibration run, and not before (#167)", () => {
  const vault = fs.mkdtempSync(path.join(os.tmpdir(), "round-log-due-"));
  scratch.push(vault);
  installGate(vault, "round-log.js");
  fs.mkdirSync(path.join(vault, "data"));
  execFileSync("git", ["init", "-q"], { cwd: vault });
  const rounds = (n) => log(...Array.from({ length: n }, (_, i) => ({ ...picked, round: i + 1 })));
  const run = (rows, calibration, ...flags) => {
    fs.writeFileSync(path.join(vault, "data", "round-log.jsonl"), rounds(rows));
    const file = path.join(vault, "data", "calibration-log.jsonl");
    if (calibration === undefined) fs.rmSync(file, { force: true });
    else fs.writeFileSync(file, calibration);
    return runInProcess(path.join(vault, "round-log.js"), flags.length ? flags : ["--log", "data/round-log.jsonl"], { cwd: vault });
  };
  const due = (result) => (result.status === 0 ? (result.stdout.match(/calibration \w+.*/) ?? [null])[0] : result.stderr);

  assert.equal(due(run(9)), null, "nine rows and no run yet");
  assert.equal(due(run(10)), "calibration due — 10 rounds logged since the last calibration run");
  assert.equal(due(run(14, '{"round_log_rows":5}\n')), null, "nine since the run at row 5");
  assert.equal(due(run(15, '{"round_log_rows":5}\n')), "calibration due — 10 rounds logged since the last calibration run");
  assert.equal(due(run(15, '{"round_log_rows":2}\n{"round_log_rows":10}\n')), null, "the last run counts, not the first");
  assert.match(due(run(15, '{"round_log_rows":"ten"}\n')), /^calibration unknown — .*line 1: round_log_rows "ten"/, "an unreadable run says so");

  execFileSync("git", ["add", "data/round-log.jsonl"], { cwd: vault });
  const staged = run(10, undefined, "--staged");
  assert.equal(staged.status, 0, staged.stderr);
  assert.doesNotMatch(staged.stdout, /calibration/);
});

const gitAt = (repo, time, ...args) =>
  execFileSync("git", ["-c", "core.hooksPath=/dev/null", "-c", "user.name=t", "-c", "user.email=t@t", ...args], {
    cwd: repo,
    stdio: "pipe",
    env: { ...process.env, GIT_COMMITTER_DATE: time, GIT_AUTHOR_DATE: time },
  });
const commit = (repo, time, file, text) => {
  fs.mkdirSync(path.dirname(path.join(repo, file)), { recursive: true });
  fs.writeFileSync(path.join(repo, file), text);
  gitAt(repo, time, "add", "-A", path.dirname(file));
  gitAt(repo, time, "commit", "-q", "-m", file);
};
const record = (id, fields = {}) =>
  `### ${id}\n${Object.entries({ question: `Does ${id} hold?`, "answered-by": "look", status: "live", ...fields })
    .filter(([, value]) => value !== null)
    .map(([name, value]) => `- ${name}: ${value}\n`)
    .join("")}\n`;
const STORE = "plugin/skills/design-critique/rules";
function calibrationRepos(name, storeText, calibration, logged) {
  const vault = fs.mkdtempSync(path.join(os.tmpdir(), `round-log-${name}-`));
  const project = fs.mkdtempSync(path.join(os.tmpdir(), `round-log-${name}-project-`));
  scratch.push(vault, project);
  installGate(vault, "round-log.js");
  for (const repo of [vault, project]) execFileSync("git", ["init", "-q"], { cwd: repo });
  commit(vault, "2026-10-01T10:00:00Z", "data/round-log.jsonl", log(picked));
  commit(vault, "2026-10-01T10:00:00Z", `${STORE}/content.md`, storeText);
  commit(project, "2026-10-01T10:00:00Z", "docs/brand/fit-gate.md", record("mmm-infra.audience"));
  commit(vault, logged, "data/calibration-log.jsonl", calibration);
  const run = (...flags) => {
    const r = runInProcess(path.join(vault, "round-log.js"), flags, { cwd: vault });
    assert.equal(r.status, 0, r.stderr);
    return r.stdout.split("\n").filter((l) => /calibration/.test(l)).map((l) => l.replace(/^round-log\.js: /, ""));
  };
  return { vault, project, gateFile: path.join(project, "docs", "brand", "fit-gate.md"), run };
}

test("a change of the critics' model, or a gate-list record changed after the last run was logged, makes calibration due, naming the gate and that commit's time", () => {
  const { vault, project, gateFile, run } = calibrationRepos("events", record("vault.proof"), '{"round_log_rows":1,"model":"claude-opus-5-5"}\n', "2026-10-03T10:00:00Z");

  assert.deepEqual(run("--model", "claude-opus-5-5", "--gate", gateFile), [], "same model, nothing changed since the run");
  assert.deepEqual(run(), [], "no model given is no model change");
  assert.deepEqual(run("--model", "claude-opus-5-6"), ["calibration due — the critics' model is claude-opus-5-6, and the last run's was claude-opus-5-5"]);

  commit(project, "2026-10-04T10:00:00Z", "docs/brand/fit-gate.md", record("mmm-infra.audience") + record("mmm-infra.marks"));
  const [projectGate] = run("--gate", gateFile);
  assert.match(projectGate, /^calibration due — \S*docs\/brand\/fit-gate\.md changed at 2026-10-04T10:00:00Z, after the last run was logged$/);

  commit(vault, "2026-10-05T10:00:00Z", `${STORE}/layout.md`, record("vault.layout"));
  const [both] = run("--model", "claude-opus-5-6", "--gate", gateFile);
  assert.match(both, /^calibration due — the critics' model is claude-opus-5-6, .*; plugin\/skills\/design-critique\/rules changed at 2026-10-05T10:00:00Z, after the last run was logged; \S*docs\/brand\/fit-gate\.md changed/);

  commit(vault, "2026-10-06T10:00:00Z", "data/calibration-log.jsonl", '{"round_log_rows":1,"model":"claude-opus-5-5"}\n{"round_log_rows":1,"model":"claude-opus-5-6"}\n');
  assert.deepEqual(run("--model", "claude-opus-5-6", "--gate", gateFile), [], "a run logged after the changes clears them");

  const unread = run("--model", "claude-opus-5-5", "--gate", path.join(project, "docs", "gone.md"));
  assert.equal(unread.length, 2);
  assert.match(unread[0], /^calibration due — the critics' model is claude-opus-5-5/);
  assert.match(unread[1], /^calibration unknown — \S*gone\.md does not exist$/);
  commit(vault, "2026-10-07T10:00:00Z", "data/calibration-log.jsonl", '{"round_log_rows":1,"model":"claude-opus-5-5"}\n{"round_log_rows":1}\n');
  assert.deepEqual(run("--model", "claude-opus-5-5"), ["calibration unknown — data/calibration-log.jsonl line 2: the last run records no model"]);
});

test("--log, --previous, --model and --gate each take a value, and any other option, --rules among them, is a usage error", () => {
  for (const [args, said] of [[["--log"], /^round-log\.js: Option '--log <value>' argument missing\n$/], [["--previous"], /'--previous <value>' argument missing/], [["--model"], /'--model <value>' argument missing/], [["--gate"], /'--gate <value>' argument missing/], [["--colour", "x"], /Unknown option '--colour'/], [["--rules", "x"], /Unknown option '--rules'/], [["--log", ""], /^round-log\.js: Option '--log <value>' argument missing\n$/]]) {
    const r = runInProcess(SCRIPT, args);
    assert.equal(r.status, 2, args.join(" "));
    assert.match(r.stderr, said);
  }
});

test("only a change to a record a gate list carries makes calibration due, not one to a staged or non-gate record (#323)", () => {
  const store = STORE;
  const live = record("vault.proof");
  const kept = record("vault.kept");
  const repos = calibrationRepos("records", live + kept, '{"round_log_rows":1}\n', "2026-10-02T10:00:00Z");
  const { vault, project, gateFile } = repos;
  const run = () => repos.run("--gate", gateFile);

  const staged = record("vault.staged", { status: "staged" });
  commit(vault, "2026-10-03T10:00:00Z", `${store}/content.md`, live + kept + staged);
  assert.deepEqual(run(), [], "a staged record added");
  commit(vault, "2026-10-04T10:00:00Z", `${store}/content.md`, live + kept + record("vault.staged", { status: "staged", question: "Reworded?" }));
  assert.deepEqual(run(), [], "a staged record edited");
  const others = ["builder", "whole-page", "type"].map((by) => record(`vault.${by}`, { "answered-by": by })).join("");
  commit(vault, "2026-10-05T10:00:00Z", `${store}/system.md`, others);
  assert.deepEqual(run(), [], "live builder, whole-page and type records added");
  fs.writeFileSync(path.join(vault, store, "layout.md"), live);
  commit(vault, "2026-10-06T10:00:00Z", `${store}/content.md`, staged + kept);
  assert.deepEqual(run(), [], "a live record moved to another file");
  commit(project, "2026-10-06T08:00:00Z", "docs/brand/fit-gate.md", record("mmm-infra.audience", { status: null }));
  assert.deepEqual(run(), [], "a live record's status left out, which leaves it live");
  commit(project, "2026-10-06T10:00:00Z", "docs/brand/fit-gate.md", record("mmm-infra.audience") + record("mmm-infra.draft", { status: "staged" }));
  assert.deepEqual(run(), [], "a staged record added to a project's gate");

  commit(vault, "2026-10-07T10:00:00Z", `${store}/layout.md`, record("vault.proof", { question: "Is it proofed?" }));
  commit(vault, "2026-10-08T10:00:00Z", `${store}/content.md`, staged + record("vault.kept", { question: "Still kept?" }));
  commit(vault, "2026-10-08T12:00:00Z", `${store}/content.md`, record("vault.staged", { status: "staged", question: "Again?" }) + record("vault.kept", { question: "Still kept?" }));
  assert.deepEqual(run(), [`calibration due — ${store} changed at 2026-10-08T10:00:00Z, after the last run was logged`], "two live look records edited, then a staged one: the latest live change");

  commit(vault, "2026-10-09T10:00:00Z", "data/calibration-log.jsonl", '{"round_log_rows":1}\n{"round_log_rows":1}\n');
  assert.deepEqual(run(), [], "a run logged after the change clears it");
  commit(vault, "2026-10-10T10:00:00Z", `${store}/content.md`, record("vault.staged", { status: "live", question: "Again?" }) + record("vault.kept", { question: "Still kept?" }));
  assert.deepEqual(run(), [`calibration due — ${store} changed at 2026-10-10T10:00:00Z, after the last run was logged`], "a staged record made live");
  commit(project, "2026-10-11T10:00:00Z", "docs/brand/fit-gate.md", record("mmm-infra.audience", { "answered-by": "script" }));
  assert.match(run()[0], /; \S*docs\/brand\/fit-gate\.md changed at 2026-10-11T10:00:00Z, after the last run was logged$/, "a project's live record edited, and its staged one dropped");

  const git = (time, ...args) => gitAt(vault, time, ...args);
  git("2026-10-12T10:00:00Z", "checkout", "-q", "-b", "side");
  commit(vault, "2026-10-12T10:00:00Z", `${store}/content.md`, record("vault.staged", { status: "live", question: "On a branch?" }) + record("vault.kept", { question: "Still kept?" }));
  git("2026-10-12T10:00:00Z", "checkout", "-q", "-");
  commit(vault, "2026-10-13T10:00:00Z", "data/calibration-log.jsonl", '{"round_log_rows":1}\n{"round_log_rows":1}\n{"round_log_rows":1}\n');
  assert.deepEqual(run(), [], "a run logged after every change on the main line");
  git("2026-10-14T10:00:00Z", "merge", "-q", "--no-ff", "--no-edit", "side");
  assert.deepEqual(run(), [`calibration due — ${store} changed at 2026-10-14T10:00:00Z, after the last run was logged`], "the branch merged after the run");
});
