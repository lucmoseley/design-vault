"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const SCRIPT = path.join(__dirname, "..", "critic-examples.js");
const SCRATCH = fs.mkdtempSync(path.join(os.tmpdir(), "critic-examples-"));
after(() => fs.rmSync(SCRATCH, { recursive: true, force: true }));

const BRIEF = path.join(SCRATCH, "brief.md");
fs.writeFileSync(BRIEF, "Aesthetic: a calm harbour page. Client values: the navy ground, a muted gold accent, photos of the boats.");

let day = 0;
const entry = (stance, words, { asset = "web-surface", project = "mmm-infra", principle = words } = {}) => ({
  date: new Date(Date.UTC(2026, 0, ++day)).toISOString().slice(0, 10),
  project,
  asset,
  where: `session ${day}`,
  candidate: null,
  words,
  stance,
  principle,
  missed_by: "critic",
  ruling: "pending",
});
const many = (stance, n) => Array.from({ length: n }, (_, i) => entry(stance, `${stance} trait ${i + 1}`));

function run(rows, ...args) {
  const log = path.join(fs.mkdtempSync(path.join(SCRATCH, "log-")), "corrections-log.jsonl");
  fs.writeFileSync(log, rows.map((r) => JSON.stringify(r)).join("\n") + "\n");
  const r = runInProcess(SCRIPT, ["--project", "mmm-infra", "--asset", "web-surface", "--brief", BRIEF, "--log", log, ...args]);
  return { status: r.status, out: r.stdout, err: r.stderr };
}

function parseSets(out) {
  const sets = {};
  let current;
  for (const line of out.split("\n")) {
    const head = line.match(/^## Critic (\w)$/);
    if (head) sets[(current = head[1])] = [];
    const item = line.match(/^\d+\. The founder (kept|rejected): "([^"]*)" — /);
    if (item) sets[current].push({ stance: item[1], words: item[2] });
  }
  return sets;
}
const wordsOf = (set) => set.map((e) => e.words).sort();

test("each critic gets as many kept entries as rejected, alternating, ten in all by default (#193)", () => {
  const r = run([...many("kept", 20), ...many("rejected", 40)]);
  assert.equal(r.status, 0, r.err);
  const sets = parseSets(r.out);
  assert.deepEqual(Object.keys(sets), ["a", "b", "c"]);
  for (const [critic, set] of Object.entries(sets)) {
    assert.equal(set.length, 10, critic);
    assert.equal(set.filter((e) => e.stance === "kept").length, 5, critic);
    for (let i = 1; i < set.length; i++) assert.notEqual(set[i].stance, set[i - 1].stance, `${critic} alternates`);
  }
  assert.equal(sets.a[0].stance, "rejected");
  assert.equal(sets.b[0].stance, "kept", "the stance a set opens with alternates by critic");
  assert.match(r.out, /from 20 kept and 40 rejected mmm-infra entries: 5 of each per critic\./);
});

test("the critics' sets are disjoint where each stance holds three critics' share, and still differ where it holds less", () => {
  const full = parseSets(run([...many("kept", 15), ...many("rejected", 15)]).out);
  const seen = [full.a, full.b, full.c].flatMap(wordsOf);
  assert.equal(new Set(seen).size, 30, "fifteen of each stance, five to each critic, none twice");

  const some = parseSets(run([...many("kept", 8), ...many("rejected", 8)]).out);
  assert.notDeepEqual(wordsOf(some.a), wordsOf(some.b));
  assert.notDeepEqual(wordsOf(some.b), wordsOf(some.c));
  for (const set of Object.values(some)) assert.equal(new Set(wordsOf(set)).size, 10, "no entry twice in one set");
});

test("a set is cut to the shorter stance, never filled from the longer, and a log with no entry of one stance deals none", () => {
  const short = run([...many("kept", 2), ...many("rejected", 30)]);
  for (const set of Object.values(parseSets(short.out))) assert.deepEqual(set.map((e) => e.stance).sort(), ["kept", "kept", "rejected", "rejected"]);
  assert.match(short.out, /2 of each per critic, fewer than --count 10 asks, as one stance holds only 2\./);
  assert.doesNotMatch(short.out, /too few entries/, "the rejected entries still differ by critic");
  const tiny = run([...many("kept", 2), ...many("rejected", 2)]);
  assert.match(tiny.out, /The log holds too few entries for the critics' sets to differ\./);

  const none = run(many("rejected", 12));
  assert.equal(none.status, 0, none.err);
  assert.match(none.out, /^No examples for mmm-infra's web-surface critics: the log holds 0 kept and 12 rejected mmm-infra entries/);
  assert.doesNotMatch(none.out, /## Critic/);
});

test("entries for the brief's asset class come first, then those sharing the brief's words, then the newest", () => {
  const rows = [
    entry("kept", "the gold accent stays muted on the navy ground"),
    entry("rejected", "the boats look like stock photos"),
    entry("kept", "older plain trait"),
    entry("kept", "newer plain trait"),
    entry("rejected", "a logo tile far too loud", { asset: "brand-art" }),
    entry("rejected", "rejected plain trait"),
    entry("kept", "the gold accent and the navy, again", { asset: "brand-art" }),
  ];
  const sets = parseSets(run(rows, "--count", "4", "--critics", "1").out);
  assert.deepEqual(sets.a, [
    { stance: "rejected", words: "the boats look like stock photos" },
    { stance: "kept", words: "the gold accent stays muted on the navy ground" },
    { stance: "rejected", words: "rejected plain trait" },
    { stance: "kept", words: "newer plain trait" },
  ]);
});

test("only the project's own entries are dealt, and --count and --critics are knobs", () => {
  const rows = [...many("kept", 6), ...many("rejected", 6), entry("kept", "manta's own taste", { project: "manta" })];
  const sets = parseSets(run(rows, "--count", "4", "--critics", "2").out);
  assert.deepEqual(Object.keys(sets), ["a", "b"]);
  for (const set of Object.values(sets)) {
    assert.equal(set.length, 4);
    assert.ok(!set.some((e) => e.words === "manta's own taste"));
  }
});

test("a log its gate refuses, a missing brief and bad options are refused with exit 2", () => {
  const bad = run([{ ...entry("kept", "x"), stance: "liked" }]);
  assert.equal(bad.status, 2);
  assert.match(bad.err, /refused by its gate — 1 fault\(s\)\n {2}stance: line 1/);
  for (const args of [["--count", "1"], ["--count", "ten"], ["--critics", "0"], ["--asset", "website"]]) {
    const r = run(many("kept", 2), ...args);
    assert.equal(r.status, 2, args.join(" "));
    assert.match(r.err, /usage: node critic-examples\.js/);
  }
  const noBrief = runInProcess(SCRIPT, ["--project", "mmm-infra", "--asset", "web-surface", "--brief", path.join(SCRATCH, "none.md")]);
  assert.equal(noBrief.status, 2);
  assert.match(noBrief.stderr, /ENOENT/);
});
