"use strict";
// calibration-packet.js, which writes the folder a calibration run's critics read and refuses one that would carry
// the founder's verdicts to them (#167). Loosen a check and a critic reads his pick, his reason or his words before it
// judges, and the agreement figure measures nothing.
require("./no-git-env");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { test, after } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const SCRIPT = path.join(__dirname, "..", "calibration-packet.js");
const FIXTURES = path.join(__dirname, "fixtures", "calibration");
const fixture = (...parts) => path.join(FIXTURES, ...parts);

const round = (over = {}) => ({
  ticket: "lucmoseley/mmm-infra#9",
  round: 1,
  tag: "rounds/hero-r1",
  brief: fixture("hero-r1", "brief.md"),
  gate_list: fixture("hero-r1", "gate-list.md"),
  gate_list_then: fixture("hero-r1", "gate-list.md"),
  copy_bans: fixture("hero-r1", "copy-bans.md"),
  candidates: { "v1-arches": fixture("hero-r1", "v1-arches.html"), "v2-slow": fixture("hero-r1", "v2-slow") },
  ...over,
});

const scratch = [];
after(() => {
  for (const dir of scratch) fs.rmSync(dir, { recursive: true, force: true });
});

function build(rounds, { roundLog = fixture("round-log.jsonl") } = {}) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "calibration-packet-"));
  scratch.push(dir);
  const manifest = path.join(dir, "manifest.json");
  fs.writeFileSync(manifest, JSON.stringify({ rounds }));
  const out = path.join(dir, "packet");
  const args = ["--manifest", manifest, "--out", out, "--round-log", roundLog, "--corrections-log", fixture("corrections-log.jsonl")];
  const result = runInProcess(SCRIPT, args);
  return { ...result, out, dir };
}
const rules = (stderr) => [...stderr.matchAll(/^ {2}([\w-]+):/gm)].map((m) => m[1]);
const listing = (dir) => fs.readdirSync(dir, { recursive: true }).map((p) => p.split(path.sep).join("/")).sort();

test("a clean round packs its brief, gate list, copy bans, candidates and the entries naming one, and nothing else", () => {
  const { status, stderr, stdout, out } = build([round()]);
  assert.equal(status, 0, stderr);
  assert.match(stdout, /1 round\(s\), 1 corrections entry/);
  assert.deepEqual(listing(out), [
    "hero-r1",
    "hero-r1/brief.md",
    "hero-r1/candidates",
    "hero-r1/candidates/v1-arches.html",
    "hero-r1/candidates/v2-slow",
    "hero-r1/candidates/v2-slow/index.html",
    "hero-r1/copy-bans.md",
    "hero-r1/entries.json",
    "hero-r1/gate-list.md",
  ]);
  // The entry keeps its pointer and its principle; the candidate he faulted, his words, his ruling and where he said
  // it stay out.
  assert.deepEqual(JSON.parse(fs.readFileSync(path.join(out, "hero-r1", "entries.json"), "utf8")), [
    { entry: 1, principle: "the accent gold stays muted against the navy" },
  ]);
});

test("a verdict field in a packed file refuses the packet, and nothing is left where a run would read it", () => {
  const { status, stderr, out, dir } = build([round({ candidates: { ...round().candidates, report: fixture("leaks", "critic-report.json") } })]);
  assert.equal(status, 1);
  assert.deepEqual(rules(stderr), ["verdict-field"]);
  assert.match(stderr, /hero-r1\/candidates\/report\.json holds the verdict field critic_pick/);
  assert.equal(fs.existsSync(out), false);
  assert.deepEqual(fs.readdirSync(dir), ["manifest.json"], "the staging folder is removed too");
});

test("a verdict field written as a bare key refuses the packet, and a bare English word does not", () => {
  const { status, stderr } = build([round({ brief: fixture("leaks", "brief-bare-key.md") })]);
  assert.equal(status, 1);
  assert.deepEqual(rules(stderr), ["verdict-field"]);
  assert.match(stderr, /hero-r1\/brief\.md holds the verdict field first_pick/);
  assert.match(fs.readFileSync(fixture("hero-r1", "brief.md"), "utf8"), /^reason: /m, "the clean brief, which the first test packs, holds a bare reason:");
});

// A brief names its asset class, which is no verdict; whether he kept or rejected a trait is one (#193).
test("a brief naming its asset class packs, and one holding a correction's stance is refused", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "calibration-packet-brief-"));
  scratch.push(dir);
  const brief = (name, line) => {
    const file = path.join(dir, name);
    fs.writeFileSync(file, `${fs.readFileSync(fixture("hero-r1", "brief.md"), "utf8")}\n${line}\n`);
    return file;
  };
  const asset = build([round({ brief: brief("asset.md", '{"asset": "web-surface"}') })]);
  assert.equal(asset.status, 0, asset.stderr);
  const stance = build([round({ brief: brief("stance.md", '{"stance": "kept"}') })]);
  assert.equal(stance.status, 1);
  assert.match(stance.stderr, /hero-r1\/brief\.md holds the verdict field stance/);
});

test("a log line pasted into a brief refuses the packet", () => {
  const { status, stderr } = build([round({ brief: fixture("leaks", "brief-pasted-row.md") })]);
  assert.equal(status, 1);
  assert.ok(rules(stderr).includes("log-line"), stderr);
  assert.match(stderr, /log-line: hero-r1\/brief\.md holds the round log line 1/);

  // A log saved with a byte-order mark: its first row is still found pasted without one.
  const { dir } = build([round()]);
  const marked = path.join(dir, "round-log.jsonl");
  fs.writeFileSync(marked, `\uFEFF${fs.readFileSync(fixture("round-log.jsonl"), "utf8")}`);
  const result = build([round({ brief: fixture("leaks", "brief-pasted-row.md") })], { roundLog: marked });
  assert.match(result.stderr, /log-line: hero-r1\/brief\.md holds the round log line 1/);
});

test("his words or his reason quoted in a brief refuse the packet", () => {
  const words = build([round({ brief: fixture("leaks", "brief-quoting-words.md") })]);
  assert.equal(words.status, 1);
  assert.deepEqual(rules(words.stderr), ["verdict-text"]);
  assert.match(words.stderr, /quotes corrections-log line 1's words/);

  const reason = build([round({ brief: fixture("leaks", "brief-quoting-reason.md") })]);
  assert.equal(reason.status, 1);
  assert.deepEqual(rules(reason.stderr), ["verdict-text"]);
  assert.match(reason.stderr, /quotes lucmoseley\/mmm-infra#9 r1's reason/);
});

// A critic reads only its own round's folder (calibration-critic.js), so a later round's Client values may quote an
// earlier round's words and reason, as the round's own critic was given them (#168).
test("a later round's brief quoting an earlier round's words and reason is packed beside that round", () => {
  const r2 = round({
    round: 2,
    tag: "rounds/hero-r2",
    brief: fixture("hero-r2", "brief.md"),
    gate_list: fixture("hero-r2", "gate-list.md"),
    gate_list_then: fixture("hero-r2", "gate-list.md"),
    copy_bans: fixture("hero-r2", "copy-bans.md"),
    candidates: { "v2a-still": fixture("hero-r2", "v2a-still.html") },
  });
  const { status, stderr, out } = build([round(), r2]);
  assert.equal(status, 0, stderr);
  assert.match(fs.readFileSync(path.join(out, "hero-r2", "brief.md"), "utf8"), /the gold is too yellow/);
  assert.match(fs.readFileSync(path.join(out, "hero-r2", "brief.md"), "utf8"), /the water reads as one line/);
});

test("a symbolic link inside a candidate refuses the packet, since a critic following it reads past the packet", () => {
  const { dir } = build([round()]);
  const candidate = path.join(dir, "linked");
  fs.mkdirSync(candidate);
  fs.symlinkSync(fixture("hero-r1", "v1-arches.html"), path.join(candidate, "index.html"));
  const { status, stderr, out } = build([round({ candidates: { ...round().candidates, linked: candidate } })]);
  assert.equal(status, 1);
  assert.deepEqual(rules(stderr), ["link"]);
  assert.match(stderr, /hero-r1\/candidates\/linked\/index\.html is a symbolic link/);
  assert.equal(fs.existsSync(out), false);
});

test("an unlogged round, a missing source, empty copy bans, an unpacked candidate an entry names, or an unsafe name is refused", () => {
  const cases = [
    [round({ round: 4, tag: "rounds/hero-r4" }), ["unlogged"]],
    [round({ brief: fixture("hero-r1", "no-such-brief.md") }), ["missing"]],
    [round({ copy_bans: undefined }), ["missing"]],
    [round({ copy_bans: fixture("hero-r1", "copy-bans-empty.md") }), ["copy-bans"]],
    [round({ gate_list_then: undefined }), ["missing"]],
    [round({ candidates: { "v2-slow": fixture("hero-r1", "v2-slow") } }), ["entry-candidate"]],
    [round({ candidates: { ...round().candidates, "..": fixture("hero-r1", "v2-slow") } }), ["manifest"]],
    [round({ tag: "rounds/hero-r3" }), ["manifest"]],
  ];
  for (const [r, expected] of cases) {
    const { status, stderr, out } = build([r]);
    assert.equal(status, 1, JSON.stringify(r));
    assert.deepEqual(rules(stderr), expected, stderr);
    assert.equal(fs.existsSync(out), false);
  }
  assert.deepEqual(rules(build([round(), round()]).stderr), ["manifest"], "one round packed twice");
});

test("an existing --out, a missing argument, or a log missing or refused by its gate is a usage error", () => {
  const { dir } = build([round()]);
  const manifest = path.join(dir, "manifest.json");
  const run = (...args) => runInProcess(SCRIPT, args);
  const broken = path.join(dir, "broken.jsonl");
  fs.writeFileSync(broken, "{ half\n");
  const cases = [
    [run("--manifest", manifest, "--out", dir), /already exists/],
    [run("--manifest", manifest), /--manifest and --out are both needed/],
    [build([round()], { roundLog: broken }), /the round log is refused by its gate — json: line 1/],
    [build([round()], { roundLog: path.join(dir, "no-such-log.jsonl") }), /no-such-log\.jsonl/],
  ];
  for (const [result, message] of cases) {
    assert.equal(result.status, 2, result.stderr);
    assert.match(result.stderr, message);
  }
});
