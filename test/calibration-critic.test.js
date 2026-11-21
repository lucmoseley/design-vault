"use strict";
// calibration-critic.js, which runs a calibration critic as a child session confined to one round's folder and
// proves the confinement with a canary (#168). A stand-in `claude` (fixtures/calibration/stub-claude) acts out the
// child, so these tests hold the flags, the working folder, the answers' form and the canary's verdicts; whether the
// real `claude` honours the flags is the live canary's to show. Loosen one and a critic answers with his verdicts in
// reach, or a canary passes that could not have seen a read.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { test, after } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const ROOT = path.join(__dirname, "..");
const SCRIPT = path.join(ROOT, "calibration-critic.js");
const FIXTURES = path.join(__dirname, "fixtures", "calibration");
const STUB = path.join(FIXTURES, "stub-claude", "claude");

const scratch = [];
after(() => {
  for (const dir of scratch) fs.rmSync(dir, { recursive: true, force: true });
});
function tmp(prefix) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), prefix));
  scratch.push(dir);
  return dir;
}

/** One round's packet folder, written by calibration-packet.js from the fixtures, with entry 1. */
function packedRound() {
  const dir = tmp("calibration-critic-");
  const manifest = path.join(dir, "manifest.json");
  const fixture = (...parts) => path.join(FIXTURES, ...parts);
  fs.writeFileSync(manifest, JSON.stringify({
    rounds: [{
      ticket: "lucmoseley/mmm-infra#9", round: 1, tag: "rounds/hero-r1", brief: fixture("hero-r1", "brief.md"), gate_list: fixture("hero-r1", "gate-list.md"),
      gate_list_then: fixture("hero-r1", "gate-list.md"), copy_bans: fixture("hero-r1", "copy-bans.md"),
      candidates: { "v1-arches": fixture("hero-r1", "v1-arches.html"), "v2-slow": fixture("hero-r1", "v2-slow") },
    }],
  }));
  const built = runInProcess(path.join(ROOT, "calibration-packet.js"), ["--manifest", manifest, "--out", path.join(dir, "packet"),
    "--round-log", fixture("round-log.jsonl"), "--corrections-log", fixture("corrections-log.jsonl")]);
  assert.equal(built.status, 0, built.stderr);
  return { dir, round: path.join(dir, "packet", "hero-r1") };
}

function run(args, env = {}) {
  const dir = tmp("calibration-critic-run-");
  const log = path.join(dir, "calls.jsonl");
  const result = runInProcess(SCRIPT, args, { env: { ...process.env, WFC_CLAUDE_BIN: STUB, STUB_LOG: log, ...env } });
  const calls = fs.existsSync(log) ? fs.readFileSync(log, "utf8").trim().split("\n").map((l) => JSON.parse(l)) : [];
  return { ...result, calls, dir };
}

const answer = (a) => ({ answer: a, evidence: "seen in the render" });
const reply = {
  answers: { "v1-arches": { "vault.proof": answer("yes") }, "v2-slow": { "vault.proof": answer("unsure") } },
  principles: { "v1-arches": { 1: answer("no") }, "v2-slow": { 1: answer("yes") } },
  leader: { candidate: "v2-slow", turned_on: "the conversion lens" },
};
function replyFile(dir, data, fence = false) {
  const file = path.join(dir, "reply.txt");
  const text = typeof data === "string" ? data : JSON.stringify(data, null, 2);
  fs.writeFileSync(file, fence ? "```json\n" + text + "\n```\n" : text);
  return file;
}

test("a critic runs confined, in its round's folder, and its answers are written with the run beside them", () => {
  const { dir, round } = packedRound();
  const out = path.join(dir, "answers", "hero-r1", "critic-a.json");
  const result = run(["--round", round, "--model", "claude-opus-5-5", "--out", out], { STUB_REPLY: replyFile(dir, reply, true) });
  assert.equal(result.status, 0, result.stderr);
  const [version, child] = [result.calls.length, result.calls.at(-1)];
  assert.equal(version, 1, "--version runs on the stub without logging, so the one call logged is the critic");
  assert.equal(child.cwd, fs.realpathSync(round));
  for (const flag of ["--restricted", "--safe-mode", "--strict-mcp-config", "--no-session-persistence"]) assert.ok(child.args.includes(flag), flag);
  const value = (flag) => child.args[child.args.indexOf(flag) + 1];
  assert.equal(value("--tools"), "Read,Glob,Grep");
  assert.equal(value("--permission-mode"), "dontAsk");
  assert.equal(value("--permission-prompts"), "none");
  assert.equal(value("--model"), "claude-opus-5-5");
  assert.ok(!child.args.includes("--add-dir"), "a critic is given no folder but its round's");
  assert.match(child.prompt, /Candidates: v1-arches, v2-slow\.\nGate question ids: vault\.proof\.\nEntries: 1\./);
  assert.match(child.prompt, /copy-bans \(the project's bans on what its copy may say, and on any look, which hold for every candidate\)/);

  const written = JSON.parse(fs.readFileSync(out, "utf8"));
  assert.deepEqual(written.run, { model: "claude-opus-5-5", claude_code: "2.1.299", round: "hero-r1" });
  assert.deepEqual(written.leader, reply.leader);
  assert.deepEqual(written.principles, reply.principles);
});

test("answers that leave out, add or misspell an answer are refused and the reply kept", () => {
  const { dir, round } = packedRound();
  const out = path.join(dir, "critic-a.json");
  const cases = [
    [{ ...reply, answers: { ...reply.answers, "v2-slow": {} } }, /answers for v2-slow leaves vault\.proof unanswered/],
    [{ ...reply, principles: { ...reply.principles, "v3-new": { 1: answer("no") } } }, /principles names v3-new, which the round does not hold/],
    [{ ...reply, answers: { ...reply.answers, "v1-arches": { "vault.proof": answer("yes"), "vault.other": answer("no") } } }, /answers vault\.other, which the round does not ask/],
    [{ ...reply, principles: { ...reply.principles, "v1-arches": { 1: answer("maybe") } } }, /answers 1 with no yes, no or unsure/],
    [{ ...reply, leader: { candidate: "v9", turned_on: "x" } }, /leader is not/],
    ["I would lead with v2-slow.", /the critic's reply is not JSON/],
  ];
  for (const [data, message] of cases) {
    const result = run(["--round", round, "--model", "m", "--out", out], { STUB_REPLY: replyFile(dir, data) });
    assert.equal(result.status, 1, JSON.stringify(data));
    assert.match(result.stderr, message);
    assert.equal(fs.existsSync(out), false);
    assert.ok(fs.existsSync(`${out}.reply.txt`));
  }
  const noLeader = run(["--round", round, "--model", "m", "--out", out], { STUB_REPLY: replyFile(dir, { ...reply, leader: { candidate: null, turned_on: "none carries the brief" } }) });
  assert.equal(noLeader.status, 0, noLeader.stderr);
});

test("the canary holds where the confined child reads its own folder and not the canary, and the control reads both", () => {
  const dir = tmp("calibration-canary-test-");
  const out = path.join(dir, "canary.json");
  const held = run(["--canary", "--model", "m", "--out", out]);
  assert.equal(held.status, 0, held.stderr);
  const record = JSON.parse(fs.readFileSync(out, "utf8"));
  assert.equal(record.held, true);
  assert.equal(record.claude_code, "2.1.299");
  assert.deepEqual(record.seen, { confined: { control: true, canary: false }, opened: { control: true, canary: true } });

  const [confined, opened] = held.calls;
  assert.ok(!confined.args.includes("--add-dir"));
  assert.deepEqual(opened.args.filter((a) => a !== "--add-dir" && !a.startsWith(path.dirname(path.dirname(confined.cwd)))), confined.args, "the opened child is the confined one plus --add-dir");
  assert.equal(fs.existsSync(confined.cwd), false, "the throwaway packet is removed");
  assert.match(fs.readFileSync(`${out}.confined.jsonl`, "utf8"), /permission denied/, "each child's transcript is kept");
  assert.match(fs.readFileSync(`${out}.opened.jsonl`, "utf8"), /canary-[0-9a-f]{24}/);
});

test("a canary read, a control unread, or a canary no control could see fails the canary", () => {
  const dir = tmp("calibration-canary-test-");
  const out = path.join(dir, "canary.json");
  const cases = [
    ["leak", /canary broken: the confined child read the canary/],
    ["blind", /canary inconclusive: the confined child did not read its own folder's control/],
    ["no-add-dir", /canary inconclusive: the child given the canary's folders did not read it/],
  ];
  for (const [mode, message] of cases) {
    const result = run(["--canary", "--model", "m", "--out", out], { STUB_MODE: mode });
    assert.equal(result.status, 1, mode);
    assert.match(result.stderr, message);
    assert.equal(JSON.parse(fs.readFileSync(out, "utf8")).held, false);
  }
});

test("bad usage, a folder that is no round, or a claude with no version is a usage error", () => {
  const { dir, round } = packedRound();
  const out = path.join(dir, "x.json");
  const bare = path.join(dir, "bare");
  fs.cpSync(round, bare, { recursive: true });
  fs.rmSync(path.join(bare, "copy-bans.md"));
  const cases = [
    [run(["--round", round, "--out", out]), /--model and --out are both needed/],
    [run(["--round", round, "--canary", "--model", "m", "--out", out]), /give one of --packet <dir>, --round <folder> or --canary/],
    [run(["--model", "m", "--out", out]), /give one of --packet <dir>, --round <folder> or --canary/],
    [run(["--packet", path.dirname(round), "--model", "m", "--out", out]), /--model and --answers are both needed/],
    [run(["--round", round, "--model", "m", "--out", out, "--seed", "1"]), /unknown argument "--seed"/],
    [run(["--round", dir, "--model", "m", "--out", out]), /holds no gate-list/],
    [run(["--round", bare, "--model", "m", "--out", out]), /holds no copy-bans/],
    [run(["--canary", "--model", "m", "--out", out], { STUB_VERSION: "unknown" }), /claude --version printed no version/],
  ];
  for (const [result, message] of cases) {
    assert.equal(result.status, 2, result.stderr);
    assert.match(result.stderr, message);
  }
});

test("--packet runs the canary, then three critics on each round folder; a canary not held runs no critic", () => {
  const { dir, round } = packedRound();
  const answers = path.join(dir, "answers");
  const result = run(["--packet", path.dirname(round), "--model", "m", "--answers", answers], { STUB_REPLY: replyFile(dir, reply) });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.calls.length, 5, "the canary's two children, then three critics");
  assert.ok(result.calls.slice(2).every((c) => c.cwd === fs.realpathSync(round)));
  assert.equal(JSON.parse(fs.readFileSync(path.join(answers, "canary.json"), "utf8")).held, true);
  for (const c of ["a", "b", "c"]) assert.equal(JSON.parse(fs.readFileSync(path.join(answers, "hero-r1", `critic-${c}.json`), "utf8")).run.round, "hero-r1");

  const leaked = run(["--packet", path.dirname(round), "--model", "m", "--answers", path.join(dir, "leaked")], { STUB_MODE: "leak", STUB_REPLY: replyFile(dir, reply) });
  assert.equal(leaked.status, 1);
  assert.equal(leaked.calls.length, 2, "no critic runs once the canary is read");
});

test("--packet runs a refused critic once more, and stops where it is refused twice", () => {
  const { dir, round } = packedRound();
  const answers = path.join(dir, "answers");
  const result = run(["--packet", path.dirname(round), "--model", "m", "--answers", answers], { STUB_REPLY: replyFile(dir, { ...reply, leader: null }) });
  assert.equal(result.status, 1);
  assert.equal(result.calls.length, 4, "the canary's two children, then critic a twice");
  assert.match(result.stderr, /leader is not/);
  assert.equal(fs.existsSync(path.join(answers, "hero-r1", "critic-b.json")), false);
});

// calibration-score.js counts his first pick a Yes only on a question these texts call unchanged since its round (#232).
test("a question's wording is its numbered line and the indented lines under it, less its number", () => {
  const { questionTexts } = require(SCRIPT);
  const list = (n, part) => `Look questions, for the critics:\n\n${n}. vault.colour-look: Is every meaning colour carries also carried by text?\n   Applies to: ${part}\n${n + 1}. vault.borrowing: Does each part show its function only by its own look?\n`;
  const then = questionTexts(list(1, "every state"));
  assert.deepEqual([...then.keys()], ["vault.colour-look", "vault.borrowing"]);
  assert.equal(then.get("vault.colour-look"), "vault.colour-look: Is every meaning colour carries also carried by text?\nApplies to: every state");
  const renumbered = questionTexts(list(3, "every state"));
  assert.equal(renumbered.get("vault.colour-look"), then.get("vault.colour-look"), "a question moved down the list is unchanged");
  assert.notEqual(questionTexts(list(1, "every state and error")).get("vault.colour-look"), then.get("vault.colour-look"), "a changed Applies to line rewords it");
  assert.equal(renumbered.get("vault.borrowing"), then.get("vault.borrowing"));
});
