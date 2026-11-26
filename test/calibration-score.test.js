"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { test, after } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const ROOT = path.join(__dirname, "..");
const SCRIPT = path.join(ROOT, "calibration-score.js");
const FIXTURES = path.join(__dirname, "fixtures", "calibration");
const fixture = (...parts) => path.join(FIXTURES, ...parts);

const scratch = [];
after(() => {
  for (const dir of scratch) fs.rmSync(dir, { recursive: true, force: true });
});

const ruled = {
  ...JSON.parse(fs.readFileSync(fixture("corrections-log.jsonl"), "utf8").split("\n")[0]),
  where: "https://github.com/lucmoseley/mmm-infra/issues/9#issuecomment-2",
  words: "that award is made up",
  principle: "every claim of proof cites its source",
  missed_by: "gate",
  ruling: "rule: vault.proof",
};
const FOLDER = { "hero-r1": "mmm-infra.hero-r1", "hero-r2": "mmm-infra.hero-r2" };
const run = { model: "claude-opus-5-5", claude_code: "2.1.299", round: FOLDER["hero-r1"] };
const say = (answer) => ({ answer, evidence: `seen: ${answer}` });
const critics = {
  a: { proof: ["no", "yes"], v1: ["no", "no"], leader: "v2-slow" },
  b: { proof: ["yes", "unsure"], v1: ["yes", "no"], leader: "v1-arches" },
  c: { proof: ["no", "no"], v1: ["unsure", "yes"], leader: "v2-slow" },
};
const critic = ({ proof, v1, leader }) => ({
  run,
  answers: { "v1-arches": { "vault.proof": say(proof[0]) }, "v2-slow": { "vault.proof": say(proof[1]) } },
  principles: { "v1-arches": { 1: say(v1[0]), 3: say(v1[1]) }, "v2-slow": { 1: say("yes"), 3: say("yes") } },
  leader: { candidate: leader, turned_on: `lens of ${leader}` },
});

const HERO_R2_ANSWER = { run: { ...run, round: FOLDER["hero-r2"] }, answers: { "v2a-still": { "vault.proof": say("yes") } }, principles: {}, leader: { candidate: "v2a-still", turned_on: "lens of v2a-still" } };
const PACKED = {
  "hero-r1": { ticket: "lucmoseley/mmm-infra#9", round: 1, tag: "rounds/hero-r1", brief: fixture("hero-r1", "brief.md"), gate_list: fixture("hero-r1", "gate-list.md"),
    gate_list_then: fixture("hero-r1", "gate-list.md"), copy_bans: fixture("hero-r1", "copy-bans.md"),
    candidates: { "v1-arches": fixture("hero-r1", "v1-arches.html"), "v2-slow": fixture("hero-r1", "v2-slow") } },
  "hero-r2": { ticket: "lucmoseley/mmm-infra#9", round: 2, tag: "rounds/hero-r2", brief: fixture("hero-r2", "brief.md"), gate_list: fixture("hero-r2", "gate-list.md"),
    gate_list_then: fixture("hero-r2", "gate-list.md"), copy_bans: fixture("hero-r2", "copy-bans.md"),
    candidates: { "v2a-still": fixture("hero-r2", "v2a-still.html") } },
};

function setUp({ canary = { held: true, verdict: "held", model: run.model, claude_code: run.claude_code }, change = {}, roundRows = 1, rounds = ["hero-r1"], firstPick, stance = "rejected", goldRuling, settle, then } = {}) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "calibration-score-"));
  scratch.push(dir);
  const corrections = path.join(dir, "corrections-log.jsonl");
  const [gold, ...rest] = fs.readFileSync(fixture("corrections-log.jsonl"), "utf8").trim().split("\n");
  fs.writeFileSync(corrections, [JSON.stringify({ ...JSON.parse(gold), stance, ...(goldRuling ? { ruling: goldRuling } : {}) }), ...rest, JSON.stringify(ruled)].join("\n") + "\n");
  const roundLog = path.join(dir, "round-log.jsonl");
  const rows = fs.readFileSync(fixture("round-log.jsonl"), "utf8").trim().split("\n").slice(0, roundRows).map((l) => JSON.parse(l));
  if (firstPick) rows[0] = { ...rows[0], first_pick: firstPick, agree: firstPick === rows[0].critic_pick };
  if (settle) rows[0] = { ...rows[0], ...settle };
  fs.writeFileSync(roundLog, rows.map((r) => JSON.stringify(r)).join("\n") + "\n");
  const manifest = path.join(dir, "manifest.json");
  fs.writeFileSync(manifest, JSON.stringify({ rounds: rounds.map((r) => (r === "hero-r1" && then !== undefined ? { ...PACKED[r], gate_list_then: then } : PACKED[r])) }));
  const logs = ["--round-log", roundLog, "--corrections-log", corrections];
  const built = runInProcess(path.join(ROOT, "calibration-packet.js"), ["--manifest", manifest, "--out", path.join(dir, "packet"), ...logs]);
  assert.equal(built.status, 0, built.stderr);
  for (const r of rounds) fs.mkdirSync(path.join(dir, "answers", FOLDER[r]), { recursive: true });
  fs.writeFileSync(path.join(dir, "answers", "canary.json"), JSON.stringify(canary));
  const answer = { "hero-r1": (name) => change[name] ?? critic(critics[name]), "hero-r2": () => HERO_R2_ANSWER };
  for (const r of rounds) for (const name of Object.keys(critics)) fs.writeFileSync(path.join(dir, "answers", FOLDER[r], `critic-${name}.json`), JSON.stringify(answer[r](name)));
  const calibrationLog = path.join(dir, "calibration-log.jsonl");
  fs.writeFileSync(calibrationLog, "");
  const score = (...more) =>
    runInProcess(SCRIPT, ["--manifest", manifest, "--packet", path.join(dir, "packet"), "--answers", path.join(dir, "answers"),
      "--where", "session f521adbb, 2026-10-14", "--row", path.join(dir, "row.jsonl"), ...logs, "--calibration-log", calibrationLog, ...more]);
  return { dir, score, calibrationLog, row: () => JSON.parse(fs.readFileSync(path.join(dir, "row.jsonl"), "utf8")) };
}

test("each critic's answers are counted against his verdicts, and every disagreement is listed with what it turned on (#168)", () => {
  const { score, row } = setUp();
  const result = score();
  assert.equal(result.status, 0, result.stderr);
  const r = row();
  assert.equal(r.date, new Date().toISOString().slice(0, 10));
  assert.equal(r.round_log_rows, 1);
  assert.equal(r.model, "claude-opus-5-5");
  assert.equal(r.canary_held_on, "2.1.299");
  assert.deepEqual(r.rounds, ["lucmoseley/mmm-infra#9 r1"]);
  assert.deepEqual(r.pick, { agree: 2, of: 3 });
  assert.deepEqual(r.questions, { "vault.proof": { agree: 3, of: 6, unsure: 1 } });
  assert.deepEqual(r.entries, { 1: { agree: 1, of: 3, unsure: 1 }, 3: { agree: 2, of: 3, unsure: 0 } });
  assert.deepEqual(r.new_questions, {});
  assert.deepEqual(r.critics, [{ unsure: 0, answers: 6 }, { unsure: 1, answers: 6 }, { unsure: 1, answers: 6 }]);
  const round = "lucmoseley/mmm-infra#9 r1";
  assert.deepEqual(r.disagreements, [
    { kind: "pick", round, critic: "b", founder: "v2-slow", leader: "v1-arches", turned_on: "lens of v1-arches" },
    { kind: "question", round, critic: "b", candidate: "v1-arches", on: "vault.proof", founder: "no", answer: "yes", evidence: "seen: yes" },
    { kind: "entry", round, critic: "b", candidate: "v1-arches", on: 1, principle: "the accent gold stays muted against the navy", rule: "unlanded", founder: "no", answer: "yes", evidence: "seen: yes" },
    { kind: "question", round, critic: "c", candidate: "v2-slow", on: "vault.proof", founder: "yes", answer: "no", evidence: "seen: no" },
    { kind: "entry", round, critic: "c", candidate: "v1-arches", on: 3, principle: "every claim of proof cites its source", rule: "rule: vault.proof", founder: "no", answer: "yes", evidence: "seen: yes" },
  ]);
  assert.equal(r.where, "session f521adbb, 2026-10-14");

  assert.match(result.stdout, /Leader picks: 2 of 3 agree \(67%, likely 21–94%\)/);
  assert.match(result.stdout, /Gate questions: 3 of 6 agree \(50%, likely 19–81%\), 1 Unsure/);
  assert.match(result.stdout, /Unsure answers: critic a 0 of 6, critic b 1 of 6, critic c 1 of 6\./);
  assert.match(result.stdout, /critic c: v2-slow fails vault\.proof, where he picked it first — seen: no/);
  assert.match(result.stdout, /critic b: v1-arches holds "the accent gold stays muted against the navy" \(corrections-log line 1, an unlanded rule\)/);
});

test("an entry ruled onto a rules-file line is reported as that rule, not as an unlanded one (#154)", () => {
  const line = "rule: rules.md §2 accent gold stays muted";
  const { score, row } = setUp({ goldRuling: line });
  const result = score();
  assert.equal(result.status, 0, result.stderr);
  assert.equal(row().disagreements.find((d) => d.kind === "entry" && d.on === 1).rule, line);
  assert.match(result.stdout, /\(corrections-log line 1, rule: rules\.md §2 accent gold stays muted\)/);
});

test("a question added or reworded since the round counts no Yes on his first pick, and its answers there are counted apart", () => {
  for (const then of [fixture("hero-r1", "gate-list-reworded.md"), fixture("hero-r1", "gate-list-empty.md")]) {
    const { score, row } = setUp({ then });
    const result = score();
    assert.equal(result.status, 0, result.stderr);
    const r = row();
    assert.deepEqual(r.questions, { "vault.proof": { agree: 2, of: 3, unsure: 0 } });
    assert.deepEqual(r.new_questions, { "vault.proof": { yes: 1, no: 1, unsure: 1 } });
    assert.deepEqual(r.disagreements.filter((d) => d.kind === "question").map((d) => [d.critic, d.candidate]), [["b", "v1-arches"]]);
    assert.match(result.stdout, /Questions added or reworded since their rounds, tested against his first picks \(the rule, not the critics\):\n {2}vault\.proof: 1 Yes, 1 No, 1 Unsure\n- lucmoseley\/mmm-infra#9 r1, critic c: v2-slow, his first pick, fails vault\.proof — seen: no/);
  }
});

test("a new question an entry of his rules on, on his first pick, is scored as that entry and not counted apart", () => {
  const { score, row } = setUp({ firstPick: "v1-arches", then: fixture("hero-r1", "gate-list-reworded.md") });
  const result = score();
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(row().new_questions, {});
  assert.deepEqual(row().questions, { "vault.proof": { agree: 2, of: 3, unsure: 0 } });
});

test("a manifest round naming no gate list of its round's time is refused, naming gate_list_then", () => {
  const { dir, score } = setUp();
  const manifest = path.join(dir, "manifest.json");
  const { gate_list_then: _, ...bare } = PACKED["hero-r1"];
  fs.writeFileSync(manifest, JSON.stringify({ rounds: [bare] }));
  const result = score();
  assert.equal(result.status, 1);
  assert.match(result.stderr, /lucmoseley\/mmm-infra#9 r1: the manifest names no gate_list_then/);
});

test("the settle step's rate is summed from the rounds' log rows, saying how many rounds carried the counts, a zero count included (#234)", () => {
  const counted = setUp({ settle: { splits: 5, settled: 4 } });
  const result = counted.score();
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(counted.row().settles, { splits: 5, settled: 4 });
  assert.match(result.stdout, /Settle step: settled 4 of 5 splits \(80%, likely 38–96%\)\. 1 of 1 round\(s\) carried the counts\./);
  const none = setUp();
  const plain = none.score();
  assert.deepEqual(none.row().settles, { splits: 0, settled: 0 });
  assert.match(plain.stdout, /Settle step: no split logged in these rounds\. 0 of 1 round\(s\) carried the counts\./);
  const zero = setUp({ settle: { splits: 0, settled: 0 } }).score();
  assert.match(zero.stdout, /Settle step: no split logged in these rounds\. 1 of 1 round\(s\) carried the counts\./);
});

test("an entry whose trait he kept is a Yes on its candidate, so a critic's No disagrees", () => {
  const { score, row } = setUp({ stance: "kept" });
  const result = score();
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(row().entries[1], { agree: 1, of: 3, unsure: 1 });
  assert.deepEqual(row().disagreements.filter((d) => d.kind === "entry" && d.on === 1).map((d) => [d.critic, d.founder, d.answer]), [["a", "yes", "no"]]);
  assert.match(result.stdout, /critic a: v1-arches breaks "the accent gold stays muted against the navy" \(corrections-log line 1, an unlanded rule\), where he kept it/);
});

test("a manifest that leaves out a round logged since the last run, or packs no first pick of his, scores nothing", () => {
  const left = setUp({ roundRows: 2 }).score();
  assert.equal(left.status, 1);
  assert.match(left.stderr, /the manifest leaves out lucmoseley\/mmm-infra#9 r2, logged since the last run/);

  const unpacked = setUp({ firstPick: "v3-gone" }).score();
  assert.equal(unpacked.status, 1);
  assert.match(unpacked.stderr, /his first pick v3-gone is not one of the packet's candidates/);
});

function lastRunOnAnotherModel() {
  const { score, row } = setUp({ roundRows: 2, rounds: ["hero-r1", "hero-r2"] });
  assert.equal(score().status, 0);
  return { ...row(), model: "claude-opus-5-1" };
}

function roundLogOf(count) {
  const [r1, r2] = fs.readFileSync(fixture("round-log.jsonl"), "utf8").trim().split("\n");
  return [r1, r2, ...Array.from({ length: count - 2 }, (_, k) => JSON.stringify({ ...JSON.parse(r2), round: k + 3 }))].join("\n") + "\n";
}

test("a run due on a change of model, with no round logged since the last run, re-judges the last ten logged and writes a row the log takes (#209)", () => {
  const last = lastRunOnAnotherModel();
  const { score, calibrationLog, row } = setUp({ roundRows: 2, rounds: ["hero-r1", "hero-r2"] });
  fs.writeFileSync(calibrationLog, `${JSON.stringify(last)}\n`);
  const result = score();
  assert.equal(result.status, 0, result.stderr);
  assert.equal(row().round_log_rows, 2);
  assert.deepEqual(row().rounds, ["lucmoseley/mmm-infra#9 r1", "lucmoseley/mmm-infra#9 r2"]);
  fs.writeFileSync(`${calibrationLog}.next`, `${JSON.stringify(last)}\n${JSON.stringify(row())}\n`);
  const logged = runInProcess(path.join(ROOT, "calibration-log.js"), ["--log", `${calibrationLog}.next`, "--previous", calibrationLog]);
  assert.equal(logged.status, 0, logged.stderr);
});

test("a manifest that leaves out one of the last ten rounds, or one since the last run, is refused, each named as which", () => {
  const last = lastRunOnAnotherModel();
  const cases = [
    [1, 2, ["hero-r1"], /leaves out lucmoseley\/mmm-infra#9 r2, logged since the last run/],
    [2, 2, ["hero-r1"], /leaves out lucmoseley\/mmm-infra#9 r2, one of the last 10 rounds logged, which a run due with fewer new rounds re-judges — add it to the manifest/],
    [1, 2, ["hero-r2"], /leaves out lucmoseley\/mmm-infra#9 r1, one of the last 10 rounds logged/],
  ];
  for (const [lastRows, roundRows, rounds, message] of cases) {
    const { score, calibrationLog } = setUp({ roundRows, rounds });
    fs.writeFileSync(calibrationLog, `${JSON.stringify({ ...last, round_log_rows: lastRows })}\n`);
    const result = score();
    assert.equal(result.status, 1, result.stderr);
    assert.match(result.stderr, message);
    assert.equal(result.stderr.match(/leaves out/g).length, 1, result.stderr);
  }
});

test("past ten rounds, a run owes every round since the last, and no round older than both", () => {
  const fresh = setUp();
  fs.writeFileSync(path.join(fresh.dir, "round-log.jsonl"), roundLogOf(12));
  const twelve = fresh.score();
  assert.equal(twelve.status, 1);
  assert.match(twelve.stderr, /leaves out lucmoseley\/mmm-infra#9 r2, logged since the last run/);
  assert.match(twelve.stderr, /leaves out lucmoseley\/mmm-infra#9 r12, logged since the last run/);

  const stale = setUp({ roundRows: 2, rounds: ["hero-r2"] });
  fs.writeFileSync(path.join(stale.dir, "round-log.jsonl"), roundLogOf(12));
  fs.writeFileSync(stale.calibrationLog, `${JSON.stringify({ ...lastRunOnAnotherModel(), round_log_rows: 12 })}\n`);
  const old = stale.score();
  assert.equal(old.status, 1);
  assert.match(old.stderr, /leaves out lucmoseley\/mmm-infra#9 r12, one of the last 10 rounds logged/);
  assert.equal(old.stderr.match(/leaves out/g).length, 10, "r3 to r12 are owed");
  assert.doesNotMatch(old.stderr, /#9 r1,/, "r1 is past the window");
});

test("a canary that did not hold, or a critic file missing, scores nothing", () => {
  const notHeld = setUp({ canary: { held: false, verdict: "broken: the confined child read the canary" } }).score();
  assert.equal(notHeld.status, 2);
  assert.match(notHeld.stderr, /the canary did not hold \(broken: the confined child read the canary\) — no critic of this run may be scored; run calibration-critic\.js --packet again/);

  const { dir, score } = setUp();
  fs.rmSync(path.join(dir, "answers", FOLDER["hero-r1"], "critic-c.json"));
  const missing = score();
  assert.equal(missing.status, 2);
  assert.match(missing.stderr, /critic-c\.json does not exist — run calibration-critic\.js --packet for the whole run/);
});

test("a critic that ran off the canary's version or model, on another round, or left a question unanswered is refused", () => {
  const cases = [
    [{ ...critic(critics.a), run: { ...run, claude_code: "2.1.300" } }, /ran on claude-opus-5-5 and Claude Code 2\.1\.300, and the canary held on claude-opus-5-5 and 2\.1\.299/],
    [{ ...critic(critics.a), run: { ...run, model: "claude-sonnet-5-5" } }, /ran on claude-sonnet-5-5/],
    [{ ...critic(critics.a), run: { ...run, round: FOLDER["hero-r2"] } }, /answers round "mmm-infra\.hero-r2", not mmm-infra\.hero-r1/],
    [{ ...critic(critics.a), answers: { "v1-arches": {}, "v2-slow": critic(critics.a).answers["v2-slow"] } }, /leaves vault\.proof unanswered/],
  ];
  for (const [a, message] of cases) {
    const { score, dir } = setUp({ change: { a } });
    const result = score();
    assert.equal(result.status, 1, result.stderr);
    assert.match(result.stderr, message);
    assert.equal(fs.existsSync(path.join(dir, "row.jsonl")), false);
  }
});

test("a row calibration-log.js refuses after the log's runs is not written", () => {
  const { score, dir, calibrationLog, row } = setUp();
  assert.equal(score().status, 0);
  const first = row();
  fs.writeFileSync(calibrationLog, `${JSON.stringify({ ...first, round_log_rows: 5 })}\n`);
  fs.rmSync(path.join(dir, "row.jsonl"));
  const refused = score();
  assert.equal(refused.status, 1);
  assert.match(refused.stderr, /round-log-rows: line 2: round_log_rows 1 is below the run before's 5/);
  assert.equal(fs.existsSync(path.join(dir, "row.jsonl")), false);
});

test("a missing argument is a usage error", () => {
  const result = runInProcess(SCRIPT, ["--manifest", "m.json"]);
  assert.equal(result.status, 2);
  assert.match(result.stderr, /--packet, --answers, --where, --row needed/);
});

test("two projects' rounds of one tag pack each project's entries into its own folder, and score them (#551)", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "calibration-score-"));
  scratch.push(dir);
  const [mmmRow] = fs.readFileSync(fixture("round-log.jsonl"), "utf8").split("\n");
  const mantaRow = { date: "2026-10-15", project: "manta", ticket: "lucmoseley/mantahostels#50", round: 1, first_pick: "v1-arches", reason: "the arches frame the sea", confidence: 60, critic_pick: "v1-arches", agree: true };
  const roundLog = path.join(dir, "round-log.jsonl");
  fs.writeFileSync(roundLog, `${mmmRow}\n${JSON.stringify(mantaRow)}\n`);
  const [gold] = fs.readFileSync(fixture("corrections-log.jsonl"), "utf8").split("\n");
  const mantaEntry = { ...JSON.parse(gold), project: "manta", where: "https://github.com/lucmoseley/mantahostels/issues/50#issuecomment-1", candidate: "rounds/hero-r1 v2-slow", words: "too sleepy for a hostel", principle: "the hero moves at a walking pace" };
  const corrections = path.join(dir, "corrections-log.jsonl");
  fs.writeFileSync(corrections, `${gold}\n${JSON.stringify(mantaEntry)}\n`);
  const manifest = path.join(dir, "manifest.json");
  fs.writeFileSync(manifest, JSON.stringify({ rounds: [PACKED["hero-r1"], { ...PACKED["hero-r1"], ticket: "lucmoseley/mantahostels#50" }] }));
  const logs = ["--round-log", roundLog, "--corrections-log", corrections];
  const packet = path.join(dir, "packet");
  const built = runInProcess(path.join(ROOT, "calibration-packet.js"), ["--manifest", manifest, "--out", packet, ...logs]);
  assert.equal(built.status, 0, built.stderr);
  const packed = (folder) => JSON.parse(fs.readFileSync(path.join(packet, folder, "entries.json"), "utf8"));
  assert.deepEqual(packed("mmm-infra.hero-r1"), [{ entry: 1, principle: "the accent gold stays muted against the navy" }]);
  assert.deepEqual(packed("manta.hero-r1"), [{ entry: 2, principle: "the hero moves at a walking pace" }]);

  const agreeing = (folder, pick, entry, faulted) => ({
    run: { ...run, round: folder },
    answers: Object.fromEntries(["v1-arches", "v2-slow"].map((c) => [c, { "vault.proof": say(c === pick ? "yes" : "no") }])),
    principles: Object.fromEntries(["v1-arches", "v2-slow"].map((c) => [c, { [entry]: say(c === faulted ? "no" : "yes") }])),
    leader: { candidate: pick, turned_on: `lens of ${pick}` },
  });
  fs.mkdirSync(path.join(dir, "answers"));
  fs.writeFileSync(path.join(dir, "answers", "canary.json"), JSON.stringify({ held: true, verdict: "held", model: run.model, claude_code: run.claude_code }));
  for (const [folder, pick, entry, faulted] of [["mmm-infra.hero-r1", "v2-slow", 1, "v1-arches"], ["manta.hero-r1", "v1-arches", 2, "v2-slow"]]) {
    fs.mkdirSync(path.join(dir, "answers", folder));
    for (const c of Object.keys(critics)) fs.writeFileSync(path.join(dir, "answers", folder, `critic-${c}.json`), JSON.stringify(agreeing(folder, pick, entry, faulted)));
  }
  const calibrationLog = path.join(dir, "calibration-log.jsonl");
  fs.writeFileSync(calibrationLog, "");
  const result = runInProcess(SCRIPT, ["--manifest", manifest, "--packet", packet, "--answers", path.join(dir, "answers"), "--where", "session f521adbb, 2026-10-15",
    "--row", path.join(dir, "row.jsonl"), ...logs, "--calibration-log", calibrationLog]);
  assert.equal(result.status, 0, result.stderr);
  const r = JSON.parse(fs.readFileSync(path.join(dir, "row.jsonl"), "utf8"));
  assert.deepEqual(r.rounds, ["lucmoseley/mmm-infra#9 r1", "lucmoseley/mantahostels#50 r1"]);
  assert.deepEqual(r.pick, { agree: 6, of: 6 });
  assert.deepEqual(r.entries, { 1: { agree: 3, of: 3, unsure: 0 }, 2: { agree: 3, of: 3, unsure: 0 } });
  assert.deepEqual(r.disagreements, []);
});
