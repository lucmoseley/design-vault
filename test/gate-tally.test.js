"use strict";
// gate.js tally, which joins the building session's script and code answers with three look critics' into one verdict
// per candidate and question (#160), and list --answered, which hands the critics what a script could not measure:
// driven through the CLI on the fixture gate and answer files in test/fixtures/gate/tally, and on copies of them
// broken one way each. Loosen it and one critic's leniency passes a fault, a split reaches the founder before a
// settle critic has looked closer, or a question no script could measure goes unanswered.
const assert = require("node:assert/strict");
const { gateScratch, refusedWithout, runGate: run } = require("./gate-files.js");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");

const FIXTURES = path.join(__dirname, "fixtures", "gate", "tally");
const GATE = path.join(FIXTURES, "gate.md");
const ANSWERED = path.join(FIXTURES, "answered.json");
const CRITICS = ["critic-a.json", "critic-b.json", "critic-c.json"].map((f) => path.join(FIXTURES, f));

const { writeText, writeSettle, buildBrokenCopy } = gateScratch("gate-tally-");

const tally = ({ answered = ANSWERED, critics = CRITICS, args = ["--asset", "web-surface"], settles = [] } = {}) =>
  run("tally", ...args, "--answered", answered, ...critics.flatMap((c) => ["--critic", c]), ...settles.flatMap((s) => ["--settle", s]), GATE);

// { <candidate>: { <id>: { by, verdict } } } from tally's output.
function parseVerdicts(out) {
  const found = {};
  let current;
  for (const line of out.split("\n")) {
    const head = line.match(/^(\S+): \d+ fault/);
    if (head) found[(current = head[1])] = {};
    const row = line.match(/^ {2}\d+\. (\S+) \(([^)]+)\): (\w+)/);
    if (row) found[current][row[1]] = { by: row[2], verdict: row[3] };
  }
  return found;
}

const said = (answer, evidence = `settled ${answer}`) => ({ answer, evidence });

const refused = refusedWithout(/^Tally of/m);

test("a look question passes on three Yes, is a fault on three No, and is a split for a settle critic on anything else", () => {
  const r = tally();
  assert.equal(r.status, 0, r.out + r.err);
  const v = parseVerdicts(r.out);
  assert.equal(v["v1-arches"]["vault.edge-look"].verdict, "pass");
  assert.equal(v["v1-arches"]["vault.tone-look"].verdict, "fault");
  assert.equal(v["v2-water"]["vault.edge-look"].verdict, "split", "two Yes and one No");
  assert.equal(v["v2-water"]["vault.tone-look"].verdict, "split", "two Yes and one Unsure");
  assert.match(r.out, /^v1-arches: 1 fault\(s\), 0 split, 0 for the founder, 4 pass\.$/m);
  assert.match(r.out, /^v2-water: 2 fault\(s\), 2 split, 0 for the founder, 1 pass\.$/m);
});

test("a settle critic's Yes passes a split, its No makes it a fault, and only its Unsure sends it to the founder", () => {
  const settle = writeSettle({ "v2-water": { "vault.edge-look": said("Yes", "at 8x the edge is one clean curve"), "vault.tone-look": said("Unsure") } });
  const r = tally({ settles: [settle] });
  assert.equal(r.status, 0, r.out + r.err);
  const v = parseVerdicts(r.out);
  assert.equal(v["v2-water"]["vault.edge-look"].verdict, "pass");
  assert.equal(v["v2-water"]["vault.tone-look"].verdict, "founder");
  assert.match(r.out, /^v2-water: 2 fault\(s\), 0 split, 1 for the founder, 2 pass\.$/m);
  // The founder still sees the three critics' answers beside the settle critic's.
  assert.match(r.out, /vault\.edge-look \(look\): pass, 2 Yes and 1 No; settled by \S*settle\.json: Yes\n(?: {5}\S*critic-.\.json: .*\n){3} {5}\S*settle\.json: Yes\. at 8x the edge is one clean curve/);
  const no = writeSettle({ "v2-water": { "vault.edge-look": said("No"), "vault.tone-look": said("No") } });
  assert.equal(parseVerdicts(tally({ settles: [no] }).out)["v2-water"]["vault.edge-look"].verdict, "fault");
});

test("a settle critic may answer a look question the panel passed, and one critic per split may each write its own file", () => {
  const edge = writeSettle({ "v2-water": { "vault.edge-look": said("Yes") }, "v1-arches": { "vault.edge-look": said("No", "the walk's P0: the corner breaks at 8x") } });
  const tone = writeSettle({ "v2-water": { "vault.tone-look": said("Yes") } });
  const r = tally({ settles: [edge, tone] });
  assert.equal(r.status, 0, r.out + r.err);
  const v = parseVerdicts(r.out);
  assert.equal(v["v1-arches"]["vault.edge-look"].verdict, "fault");
  assert.equal(v["v2-water"]["vault.tone-look"].verdict, "pass");
});

test("settle files are refused where they leave a split unsettled, settle what no critics split on, or settle one split twice", () => {
  const edgeOnly = writeSettle({ "v2-water": { "vault.edge-look": said("Yes") } });
  refused(tally({ settles: [edgeOnly] }), /no --settle file settles vault\.tone-look for v2-water, which the critics split on/);
  const both = writeSettle({ "v2-water": { "vault.edge-look": said("Yes"), "vault.tone-look": said("Yes") } });
  const fault = writeSettle({ "v1-arches": { "vault.tone-look": said("Yes") } });
  refused(tally({ settles: [both, fault] }), /settle\.json: settles vault\.tone-look for v1-arches, which no three critics split on/);
  const script = writeSettle({ "v1-arches": { "vault.contrast": said("No") } });
  refused(tally({ settles: [both, script] }), /settles vault\.contrast for v1-arches, which no three critics split on/);
  refused(tally({ settles: [both, edgeOnly] }), /settles vault\.edge-look for v2-water, which \S*settle\.json settles too/);
  const maybe = writeSettle({ "v2-water": { "vault.edge-look": said("maybe"), "vault.tone-look": said("Yes") } });
  refused(tally({ settles: [maybe] }), /answers vault\.edge-look for v2-water "maybe", not one of yes, no, unsure/);
});

test("a critic whose candidates were split across dispatches is tallied from its files comma-joined, each candidate once", () => {
  const whole = JSON.parse(fs.readFileSync(CRITICS[0], "utf8"));
  const half = (candidate, clashes) => buildBrokenCopy(CRITICS[0], (d) => {
    d.answers = { [candidate]: whole.answers[candidate] };
    d.clashes = clashes;
  });
  const joined = `${half("v1-arches", [])},${half("v2-water", whole.clashes)}`;
  const r = tally({ critics: [joined, ...CRITICS.slice(1)] });
  assert.equal(r.status, 0, r.out + r.err);
  assert.deepEqual(parseVerdicts(r.out), parseVerdicts(tally().out));
  assert.match(r.out, /on v2-water: "the hero runs edge to edge"/);
  const twice = `${half("v1-arches", [])},${CRITICS[0]}`;
  refused(tally({ critics: [twice, ...CRITICS.slice(1)] }), /critic-a\.json: answers for v1-arches, which another of \S+ answers too/);
});

test("one critic's file named under two --critic flags is refused, so one critic cannot count as two (#154)", () => {
  const usage = (r) => {
    assert.equal(r.status, 2, r.out + r.err);
    assert.match(r.err, /critic-a\.json is named under two --critic flags/);
  };
  usage(tally({ critics: [CRITICS[0], CRITICS[0], CRITICS[0]] }));
  const half = buildBrokenCopy(CRITICS[1], (d) => (d.answers = { "v1-arches": d.answers["v1-arches"] }));
  usage(tally({ critics: [CRITICS[0], `${half},${CRITICS[0]}`, CRITICS[2]] }));
});

test("a fault or a founder question shows each critic's answer and evidence, a pass shows none", () => {
  const { out } = tally();
  const v2 = out.slice(out.indexOf("v2-water:"));
  for (const [critic, answer] of [["a", "Yes"], ["b", "Unsure"], ["c", "Yes"]]) {
    assert.match(v2, new RegExp(`critic-${critic}\\.json: ${answer}\\. critic ${critic} on vault\\.tone-look`));
  }
  const v1 = out.slice(out.indexOf("v1-arches:"), out.indexOf("v2-water:"));
  assert.doesNotMatch(v1, /on vault\.edge-look/, "v1's edge-look passed, so no evidence");
  assert.match(v1, /critic-a\.json: No\. critic a on vault\.tone-look/);
});

test("a script or code answer stands without the tally, whatever the critics say", () => {
  const v = parseVerdicts(tally().out);
  // critic-a.json answers No to v1-arches' contrast, which its script passed.
  assert.deepEqual(v["v1-arches"]["vault.contrast"], { by: "script", verdict: "pass" });
  assert.deepEqual(v["v1-arches"]["vault.proof"], { by: "code", verdict: "pass" });
  assert.deepEqual(v["v2-water"]["vault.focus"], { by: "script", verdict: "pass" });
  assert.deepEqual(v["v2-water"]["vault.proof"], { by: "code", verdict: "fault" });
  assert.match(tally().out, /vault\.proof \(code\): fault\n {5}the '200 happy guests' count has no source/);
});

test("a script's cannot measure is tallied from the look critics", () => {
  const { out } = tally();
  const v = parseVerdicts(out);
  assert.deepEqual(v["v1-arches"]["vault.focus"], { by: "script cannot measure it, so look", verdict: "pass" });
  assert.deepEqual(v["v2-water"]["vault.contrast"], { by: "script cannot measure it, so look", verdict: "fault" });
  assert.match(out, /script: v2-water\/access\/access\.json, exit 6: the hero text sits on video/);
});

test("check-frames.py's exit 6 sends the vault's end-frame and drafts-kept to the look critics, who answer them", () => {
  // #613: a canvas or scripted build check-frames.py cannot check is answered cannot measure, never judged by eye by
  // the session that built it. On the vault's own gate, so a record moving either question off check-frames shows here.
  const rules = path.join(__dirname, "..", "plugin", "skills", "design-critique", "rules");
  const args = ["--asset", "motion", "--fact", "has-motion", "--fact", "has-brand-motion"];
  const ids = (out, head) => [...out.slice(out.indexOf(head)).split("\n\n")[1].matchAll(/^\d+\. (\S+?)[ :]/gm)].map((m) => m[1]);
  const unmeasured = ["vault.end-frame", "vault.drafts-kept"];
  const scripted = ids(run("list", ...args, rules).out, "Script and code questions");
  assert.ok(unmeasured.every((id) => scripted.includes(id)), scripted.join(", "));
  const exit6 = { answer: "cannot measure", evidence: "v1-build/frames/out.txt, exit 6: a visible canvas" };
  const answered = writeText(
    "frames-answered.json",
    JSON.stringify({ answers: { "v1-build": Object.fromEntries(scripted.map((id) => [id, unmeasured.includes(id) ? exit6 : said("pass")])) } }),
  );
  const listed = run("list", ...args, "--look", "--answered", answered, rules);
  assert.equal(listed.status, 0, listed.out + listed.err);
  for (const id of unmeasured) assert.match(listed.out, new RegExp(`^\\d+\\. ${id.replace(".", "\\.")} \\(script cannot measure it for v1-build\\):`, "m"));
  const looked = ids(listed.out, "Look questions");
  const critic = (n) =>
    writeText(
      `frames-critic-${n}.json`,
      JSON.stringify({ answers: { "v1-build": Object.fromEntries(looked.map((id) => [id, said(id === "vault.end-frame" ? "No" : "Yes")])) }, clashes: [] }),
    );
  const r = run("tally", ...args, "--answered", answered, ...[1, 2, 3].flatMap((n) => ["--critic", critic(n)]), rules);
  assert.equal(r.status, 0, r.out + r.err);
  const v = parseVerdicts(r.out)["v1-build"];
  assert.deepEqual(v["vault.end-frame"], { by: "script cannot measure it, so look", verdict: "fault" });
  assert.deepEqual(v["vault.drafts-kept"], { by: "script cannot measure it, so look", verdict: "pass" });
});

test("every clash a critic named is printed for the reveal, and None where none was", () => {
  const { out } = tally();
  const clashes = out.slice(out.indexOf("Clashes the critics named")).split("\n").filter((l) => l.startsWith("- "));
  assert.equal(clashes.length, 2);
  assert.match(clashes[0], /critic-a\.json, on v2-water: "the hero runs edge to edge" against "keep 24 px clear around the logo"/);
  assert.match(clashes[1], /critic-c\.json, on the whole round: "one main action per view" against "show both booking buttons"/);
  const quiet = CRITICS.map((c) => buildBrokenCopy(c, (d) => (d.clashes = [])));
  assert.match(tally({ critics: quiet }).out, /Clashes the critics named, for the reveal:\n\nNone\./);
});

test("list --answered adds each question a script could not measure to the critics' list, keeping its number", () => {
  const plain = run("list", "--asset", "web-surface", "--look", GATE);
  assert.doesNotMatch(plain.out, /vault\.contrast|vault\.focus/);
  const r = run("list", "--asset", "web-surface", "--look", "--answered", ANSWERED, GATE);
  assert.equal(r.status, 0, r.out + r.err);
  const items = [...r.out.matchAll(/^(\d+)\. (\S+?)(?: \(([^)]+)\))?:/gm)].map((m) => [m[1], m[2], m[3]]);
  assert.deepEqual(items, [
    ["1", "vault.edge-look", undefined],
    ["2", "vault.tone-look", undefined],
    ["3", "vault.contrast", "script cannot measure it for v2-water"],
    ["4", "vault.focus", "script cannot measure it for v1-arches"],
  ]);
  assert.match(r.out, /: 4 question\(s\)\./);
});

test("a question the asset's facts drop is owed by no one", () => {
  // No critic answers vault.motion-look, which a still asset leaves off the list.
  assert.equal(tally().status, 0);
  refused(tally({ args: ["--asset", "web-surface", "--fact", "has-motion"] }), /critic-a\.json: gives v1-arches no answer to vault\.motion-look/);
});

test("a critic who leaves a look question, or a question no script could measure, unanswered is refused", () => {
  const noLook = buildBrokenCopy(CRITICS[1], (d) => delete d.answers["v2-water"]["vault.tone-look"]);
  refused(tally({ critics: [CRITICS[0], noLook, CRITICS[2]] }), /critic-b\.json: gives v2-water no answer to vault\.tone-look/);
  const noFallback = buildBrokenCopy(CRITICS[2], (d) => delete d.answers["v2-water"]["vault.contrast"]);
  refused(tally({ critics: [CRITICS[0], CRITICS[1], noFallback] }), /critic-c\.json: gives v2-water no answer to vault\.contrast/);
  const noCandidate = buildBrokenCopy(CRITICS[0], (d) => delete d.answers["v1-arches"]);
  refused(tally({ critics: [noCandidate, ...CRITICS.slice(1)] }), /critic-a\.json: gives no answers for v1-arches/);
});

test("a critic's answer outside Yes, No and Unsure, or without one line of evidence, is refused", () => {
  const maybe = buildBrokenCopy(CRITICS[0], (d) => (d.answers["v1-arches"]["vault.edge-look"].answer = "maybe"));
  refused(tally({ critics: [maybe, ...CRITICS.slice(1)] }), /answers vault\.edge-look for v1-arches "maybe", not one of yes, no, unsure/);
  const pass = buildBrokenCopy(CRITICS[0], (d) => (d.answers["v1-arches"]["vault.edge-look"].answer = "pass"));
  refused(tally({ critics: [pass, ...CRITICS.slice(1)] }), /not one of yes, no, unsure/);
  for (const evidence of ["", "two\nlines", undefined]) {
    const bad = buildBrokenCopy(CRITICS[0], (d) => (d.answers["v1-arches"]["vault.edge-look"].evidence = evidence));
    refused(tally({ critics: [bad, ...CRITICS.slice(1)] }), /gives vault\.edge-look for v1-arches no one line of evidence/);
  }
});

test("a critic who does not say what clashes it named, or quotes other than two rules, is refused", () => {
  const silent = buildBrokenCopy(CRITICS[1], (d) => delete d.clashes);
  refused(tally({ critics: [CRITICS[0], silent, CRITICS[2]] }), /critic-b\.json: has no `clashes` list/);
  for (const quotes of [["only one rule"], ["a", "b", "c"], ["a", " "]]) {
    const bad = buildBrokenCopy(CRITICS[0], (d) => (d.clashes = [{ candidate: null, quotes }]));
    refused(tally({ critics: [bad, ...CRITICS.slice(1)] }), /clash 1 does not quote exactly two rules/);
  }
  const stranger = buildBrokenCopy(CRITICS[0], (d) => (d.clashes[0].candidate = "v9-nobody"));
  refused(tally({ critics: [stranger, ...CRITICS.slice(1)] }), /names a clash on v9-nobody, which the building session's answers do not name/);
});

test("a critic answering for a candidate or a question that is not on the list is refused", () => {
  const extra = buildBrokenCopy(CRITICS[0], (d) => (d.answers["v9-nobody"] = {}));
  refused(tally({ critics: [extra, ...CRITICS.slice(1)] }), /answers for v9-nobody, which the building session's answers do not name/);
  const typo = buildBrokenCopy(CRITICS[0], (d) => (d.answers["v1-arches"]["vault.edge-lok"] = { answer: "yes", evidence: "x" }));
  refused(tally({ critics: [typo, ...CRITICS.slice(1)] }), /answers vault\.edge-lok for v1-arches, which is not on the list/);
});

test("the building session's answers are refused, naming the gap, where they miss a script or code question or answer another", () => {
  const missing = buildBrokenCopy(ANSWERED, (d) => delete d.answers["v2-water"]["vault.proof"]);
  refused(tally({ answered: missing }), /answered\.json: gives v2-water no answer to vault\.proof/);
  const look = buildBrokenCopy(ANSWERED, (d) => (d.answers["v1-arches"]["vault.edge-look"] = { answer: "pass", evidence: "x" }));
  refused(tally({ answered: look }), /answers vault\.edge-look for v1-arches, which is no script or code question on the list/);
  const yes = buildBrokenCopy(ANSWERED, (d) => (d.answers["v1-arches"]["vault.contrast"].answer = "yes"));
  refused(tally({ answered: yes }), /"yes", not one of pass, fail, cannot measure/);
  const none = buildBrokenCopy(ANSWERED, (d) => (d.answers = {}));
  refused(tally({ answered: none }), /answered\.json: answers for no candidate/);
  refused(run("list", "--asset", "web-surface", "--look", "--answered", missing, GATE), /gives v2-water no answer to vault\.proof/);
});

test("a file that is not JSON is refused, an unreadable one and anything but three critics are bad usage", () => {
  const notJson = writeText("critic.json", "Yes, Yes, No");
  const dir = path.dirname(notJson);
  refused(tally({ critics: [notJson, ...CRITICS.slice(1)] }), /critic\.json: is not JSON/);
  const absent = tally({ critics: [path.join(dir, "absent.json"), ...CRITICS.slice(1)] });
  assert.equal(absent.status, 2);
  assert.match(absent.err, /absent\.json: ENOENT/);
  for (const critics of [CRITICS.slice(0, 2), [...CRITICS, CRITICS[0]]]) {
    const r = tally({ critics });
    assert.equal(r.status, 2);
    assert.match(r.err, /^tally takes 3 look critics' answers/);
  }
  const noAnswered = run("tally", "--asset", "web-surface", ...CRITICS.flatMap((c) => ["--critic", c]), GATE);
  assert.equal(noAnswered.status, 2);
  assert.match(noAnswered.err, /^tally needs the building session's answers/);
});
