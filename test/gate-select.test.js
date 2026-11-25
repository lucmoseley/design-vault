"use strict";
// gate.js list as the selector (#273): each reader is handed only the records for its asset, the candidate's parts and its
// stage. Loosen it and the builder is handed treatment rules for parts it never drew, a staged record reaches an agent
// before its load test, a rule whose script is owed reaches nobody, or a gate critic is handed a list past the length
// where recall falls.
const assert = require("node:assert/strict");
const path = require("node:path");
const { test } = require("node:test");
const { gateScratch, runGate: run } = require("./gate-files.js");
const { STORE } = require("./rule-store.js");
const fs = require("node:fs");
const { MAPPED_PARTS, PARTS } = require("../plugin/skills/design-round/scripts/gate-form.js");

const { writeText, buildCopy } = gateScratch("gate-select-");

const WALK = "design-critique/references/house-principles.md#the-function-walk";
const ORDER = "design-critique/references/house-principles.md#dependency-order";

/** One record in rules.md's form, from a compact spec; a project's record with no stage gives the eight fields alone. */
function record(id, { by, stage, when = "web-surface", status = "live", script, parts, reasons = WALK }) {
  const owner = id.slice(0, id.indexOf("."));
  const lines = [
    `### ${id}`, `- applies-when: ${when}; the ${id} part`, `- question: Does ${id} hold?`, `- answered-by: ${by}`, `- writes: ${id}`,
    "- yields-to: none", "- source: a made-up rule; strength: house judgement", "- era: timeless", `- owner: ${owner}`,
  ];
  if (!stage) return lines.join("\n");
  lines.push(`- stage: ${stage}`);
  if (by === "builder" || stage !== "value") lines.push(`- target: Build to ${id}.`);
  if (by === "builder" && stage === "value") lines.push("- inputs: ground lightness", "- output: a step two tones darker");
  if (script) lines.push(`- script: ${script}`);
  if (parts) lines.push(`- parts: ${parts}`);
  lines.push(`- reasons: ${reasons}`, "- ledger: none", `- status: ${status}`);
  return lines.join("\n");
}
const gateText = (name, records) => `# ${name}\n\n${records.map(([id, spec]) => record(id, spec)).join("\n\n")}\n`;
const gateFile = (name, records) => writeText(name, gateText(name, records));

const GATE = gateFile("gate.md", [
  ["vault.walk-look", { by: "look", stage: "function" }],
  ["vault.walk-code", { by: "code", stage: "function" }],
  ["vault.order-whole", { by: "whole-page", stage: "role", reasons: ORDER }],
  ["vault.cta-whole", { by: "whole-page", stage: "function", when: "web-surface and has-cta" }],
  ["vault.motion-whole", { by: "whole-page", stage: "treatment", when: "has-motion" }],
  ["vault.scale-type", { by: "type", stage: "role" }],
  ["vault.card-build", { by: "builder", stage: "treatment", parts: "card" }],
  ["vault.field-build", { by: "builder", stage: "treatment", parts: "textbox, combobox" }],
  ["vault.edge-build", { by: "builder", stage: "treatment" }],
  ["vault.radius-look", { by: "look", stage: "treatment", parts: "button" }],
  ["vault.space-build", { by: "builder", stage: "value" }],
  ["vault.contrast-script", { by: "script", stage: "value", script: "check-access.py" }],
  ["vault.focus-script", { by: "script", stage: "treatment", script: "check-access.py" }],
  ["vault.reflow-script", { by: "script", stage: "value", script: "check-layout.py" }],
  ["vault.measure-owed", { by: "script", stage: "value", script: "owed" }],
  ["vault.later-look", { by: "look", stage: "treatment", status: "staged" }],
  ["vault.later-build", { by: "builder", stage: "function", status: "staged" }],
  ["vault.later-whole", { by: "whole-page", stage: "role", status: "staged" }],
  ["vault.later-type", { by: "type", stage: "role", status: "staged" }],
  ["vault.later-script", { by: "script", stage: "value", script: "check-load.py", status: "staged" }],
  ["vault.print-build", { by: "builder", stage: "role", when: "print" }],
]);

const list = (args, files = [GATE]) => run("list", ...args, ...files);
// The ids a printout numbers, in its order.
const ids = (out) => [...out.matchAll(/^\d+\. (\S+?)(?: \([^)]*\))?:/gm)].map((m) => m[1]);
const ok = (r) => {
  assert.equal(r.status, 0, r.out + r.err);
  return r.out;
};
const DECLARED = (declared) => writeText("declared.json", JSON.stringify({ declared }));
const PARTS_MAP = writeText("parts.json", JSON.stringify({
  parts: [
    { id: "p1", actable: true, href: null, text: "Send", role: "button" },
    { id: "p2", actable: true, href: null, text: "Email", role: "textbox" },
    { id: "p3", actable: false, href: null, text: "Rooms", role: "div" },
  ],
}));
const builder = (stage, ...args) => ["--asset", "web-surface", "--reader", "builder", "--stage", stage, ...args];

test("the gate list keeps its look, script and code split, and a record whose script is owed joins the look questions marked script owed", () => {
  const out = ok(list(["--asset", "web-surface"]));
  assert.deepEqual(ids(out), ["vault.walk-look", "vault.radius-look", "vault.measure-owed", "vault.walk-code", "vault.contrast-script", "vault.focus-script", "vault.reflow-script"]);
  assert.match(out, /^3\. vault\.measure-owed \(script owed\): Does vault\.measure-owed hold\?$/m);
  const look = ok(list(["--asset", "web-surface", "--look"]));
  assert.deepEqual(ids(look), ["vault.walk-look", "vault.radius-look", "vault.measure-owed"]);
  assert.equal(ok(list(["--asset", "web-surface", "--reader", "gate"])), out);
});

test("a staged record is left out of every reader's list unless --staged is given", () => {
  assert.ok(!ids(ok(list(["--asset", "web-surface"]))).includes("vault.later-look"));
  assert.ok(ids(ok(list(["--asset", "web-surface", "--staged"]))).includes("vault.later-look"));
  const readers = [
    [builder("direction"), "vault.later-build"],
    [builder("build", "--parts", DECLARED({})), "vault.later-build"],
    [["--asset", "web-surface", "--reader", "whole-page"], "vault.later-whole"],
    [["--asset", "web-surface", "--reader", "type"], "vault.later-type"],
    [["--asset", "web-surface", "--reader", "script"], "vault.later-script"],
  ];
  for (const [args, id] of readers) {
    assert.ok(!ok(list(args)).includes(id), `${id} without --staged`);
    assert.ok(ids(ok(list([...args, "--staged"]))).includes(id), `${id} with --staged`);
  }
  assert.doesNotMatch(ok(list(builder("finish"))), /check-load\.py/);
  assert.match(ok(list(builder("finish", "--staged"))), /check-load\.py\n {3}Answers: vault\.later-script/);
});

test("tally reads the list --staged gives, so the critics answer a staged look question only then", () => {
  const gate = gateFile("staged.md", [
    ["vault.walk-look", { by: "look", stage: "function" }],
    ["vault.later-look", { by: "look", stage: "treatment", status: "staged" }],
  ]);
  const said = (answer) => ({ answer, evidence: `said ${answer}` });
  const answered = writeText("answered.json", JSON.stringify({ answers: { c1: {} } }));
  const critics = [1, 2, 3].flatMap(() => ["--critic", writeText("critic.json", JSON.stringify({ answers: { c1: { "vault.walk-look": said("Yes") } }, clashes: [] }))]);
  assert.match(ok(run("tally", "--asset", "web-surface", "--answered", answered, ...critics, gate)), /on 1 question\(s\)/);
  const r = run("tally", "--asset", "web-surface", "--staged", "--answered", answered, ...critics, gate);
  assert.equal(r.status, 1, r.out + r.err);
  assert.match(r.out, /gives c1 no answer to vault\.later-look/);
});

test("the builder's direction stage gives the targets of the function and role records for the asset and facts, whatever answers them, whole-page records included", () => {
  const out = ok(list(builder("direction")));
  assert.deepEqual(ids(out), ["vault.walk-look", "vault.walk-code", "vault.order-whole", "vault.scale-type"]);
  assert.match(out, /^1\. vault\.walk-look \(function\): Build to vault\.walk-look\.\n {3}Applies to: the vault\.walk-look part$/m);
  assert.doesNotMatch(out, /Does vault\.\S+ hold/);
  assert.deepEqual(ids(ok(list([...builder("direction"), "--fact", "has-cta"]))), ["vault.walk-look", "vault.walk-code", "vault.cta-whole", "vault.order-whole", "vault.scale-type"]);
  assert.ok(!ids(ok(list(["--asset", "print", "--reader", "builder", "--stage", "direction"]))).includes("vault.walk-look"));
  assert.ok(ids(ok(list(["--asset", "print", "--reader", "builder", "--stage", "direction"]))).includes("vault.print-build"));
});

test("the build stage adds the treatment records for the parts the candidate declares, every treatment record naming no part, and the builder's own value records", () => {
  const out = ok(list(builder("build", "--parts", DECLARED({ card: ".card" }))));
  assert.deepEqual(ids(out), [
    "vault.walk-look", "vault.walk-code", "vault.order-whole", "vault.scale-type",
    "vault.card-build", "vault.edge-build", "vault.focus-script", "vault.space-build",
  ]);
  assert.match(out, /for a candidate with card: 8 record\(s\)/);
});

test("the build stage reads a parts map's roles as the candidate's parts, and joins it with a declaration", () => {
  const mapped = ids(ok(list(builder("build", "--parts", PARTS_MAP))));
  assert.ok(mapped.includes("vault.field-build") && mapped.includes("vault.radius-look"), mapped.join(", "));
  assert.ok(!mapped.includes("vault.card-build"));
  const both = ids(ok(list(builder("build", "--parts", PARTS_MAP, "--parts", DECLARED({ card: null })))));
  for (const id of ["vault.field-build", "vault.radius-look", "vault.card-build"]) assert.ok(both.includes(id), id);
  const carried = buildCopy(PARTS_MAP, (data) => (data.declared = { card: ".card" }));
  assert.deepEqual(ids(ok(list(builder("build", "--parts", carried)))), both);
});

test("the build stage refuses a parts map holding a part that is not an object, naming it, rather than crashing (#154)", () => {
  const hollow = buildCopy(PARTS_MAP, (data) => data.parts.push(null));
  const r = list(builder("build", "--parts", hollow));
  assert.equal(r.status, 1, r.out + r.err);
  assert.match(r.out, /part \d+ has no id, no actable true or false, or no text/);
  assert.doesNotMatch(r.err, /TypeError/);
});

test("the finish stage gives each script to run and the records it answers, never their text, and names the records whose script is owed", () => {
  const out = ok(list(builder("finish")));
  assert.match(out, /: 2 script\(s\)\.\n\n1\. check-access\.py\n {3}Answers: vault\.focus-script, vault\.contrast-script\n2\. check-layout\.py\n {3}Answers: vault\.reflow-script\n\nScript owed, so the gate critics look instead: vault\.measure-owed\.\n$/);
  assert.doesNotMatch(out, /hold\?|Build to/);
});

test("the whole-page and type critics' readers give the records each answers, coarse to fine, and the reference sections they cite", () => {
  const out = ok(list(["--asset", "web-surface", "--fact", "has-cta", "--fact", "has-motion", "--reader", "whole-page"]));
  assert.deepEqual(ids(out), ["vault.cta-whole", "vault.order-whole", "vault.motion-whole"]);
  assert.match(out, /^1\. vault\.cta-whole \(function\): Does vault\.cta-whole hold\?$/m);
  assert.match(out, new RegExp(`Reference sections they cite, in skills/:\\n\\n- ${WALK}: vault\\.cta-whole, vault\\.motion-whole\\n- ${ORDER}: vault\\.order-whole\\n$`));
  assert.deepEqual(ids(ok(list(["--asset", "web-surface", "--reader", "whole-page"]))), ["vault.order-whole"]);
  assert.deepEqual(ids(ok(list(["--asset", "web-surface", "--reader", "type"]))), ["vault.scale-type"]);
});

test("the script reader gives every record a script answers with its script, an owed one marked so", () => {
  const out = ok(list(["--asset", "web-surface", "--reader", "script"]));
  assert.deepEqual(ids(out), ["vault.focus-script", "vault.contrast-script", "vault.reflow-script", "vault.measure-owed"]);
  assert.match(out, /^1\. vault\.focus-script \(check-access\.py\): /m);
  assert.match(out, /^4\. vault\.measure-owed \(script owed\): /m);
});

// A gate of `function` function or role look questions and `treatment` treatment or owed value ones.
const longGate = (functionCount, treatmentCount) => gateFile("long.md", [
  ...Array.from({ length: functionCount }, (_, i) => [`vault.coarse-${i}`, { by: "look", stage: i % 2 ? "role" : "function" }]),
  ...Array.from({ length: treatmentCount }, (_, i) => [`vault.fine-${i}`, i % 2 ? { by: "script", stage: "value", script: "owed" } : { by: "look", stage: "treatment" }]),
]);

// longGate()'s ids from `prefix` in the order a pass asks them: its first stage's, the even ones, then its second's.
const passOrder = (prefix, count) => {
  const all = Array.from({ length: count }, (_, i) => `vault.${prefix}-${i}`);
  return [...all.filter((_, i) => i % 2 === 0), ...all.filter((_, i) => i % 2)];
};

// A directory of gate files, one per area as the vault's store keeps them, from { <area>: [[id, spec], ...] }; its path.
function areaGate(areas) {
  const [first, ...rest] = Object.entries(areas);
  const dir = path.dirname(gateFile(`${first[0]}.md`, first[1]));
  for (const [area, records] of rest) fs.writeFileSync(path.join(dir, `${area}.md`), gateText(area, records));
  return dir;
}
// `count` look records at `stage` in one area, named `<area>-<stage>-<i>`.
const looks = (area, stage, count) => Array.from({ length: count }, (_, i) => [`vault.${area}-${stage}-${i}`, { by: "look", stage }]);
const named = (area, stage, count) => looks(area, stage, count).map(([id]) => id);
// Each pass of a printout as { label, ids }, in order.
const passesOf = (out) => out.split(/^Pass \d+, /m).slice(1).map((p) => ({ label: p.slice(0, p.indexOf(":\n")), ids: ids(p) }));

test("a list of 21 look questions runs in 2 passes, its function and role questions before its treatment and value ones, and 20 stay one pass", () => {
  const project = gateFile("project.md", [["demo.unstaged", { by: "look" }]]);
  const out = ok(list(["--asset", "web-surface", "--look"], [longGate(11, 9), project]));
  assert.match(out, /^Gate list for web-surface: 21 question\(s\)\.$/m);
  assert.match(out, /^Look questions, for the critics, in 2 passes of at most 20, as there are more than 20, each to a fresh trio:$/m);
  assert.deepEqual(passesOf(out), [
    { label: "function and role: function: long; role: long; no stage: project", ids: [...passOrder("coarse", 11), "demo.unstaged"] },
    { label: "treatment and value, once the function and role passes' fixes land: treatment: long; value: long", ids: passOrder("fine", 9) },
  ]);
  // 21 in one stage and area: two passes, as even as they can be.
  const one = ok(list(["--asset", "web-surface", "--look"], [areaGate({ walk: looks("walk", "function", 21) })]));
  assert.deepEqual(passesOf(one).map((p) => p.ids), [named("walk", "function", 21).slice(0, 10), named("walk", "function", 21).slice(10)]);
  const twenty = ok(list(["--asset", "web-surface", "--look"], [longGate(11, 9)]));
  assert.doesNotMatch(twenty, /Pass 1/);
  assert.match(twenty, /^Look questions, for the critics:$/m);
});

test("a list of 40 look questions in one phase is cut at the area its stage changes at, never through an area", () => {
  const gate = areaGate({
    a: [...looks("a", "function", 12), ...looks("a", "role", 12)],
    b: [...looks("b", "function", 8), ...looks("b", "role", 8)],
  });
  const out = ok(list(["--asset", "web-surface", "--look"], [gate]));
  assert.match(out, /^Gate list for web-surface: 40 question\(s\)\.$/m);
  assert.deepEqual(passesOf(out), [
    { label: "function and role: function: a, b", ids: [...named("a", "function", 12), ...named("b", "function", 8)] },
    { label: "function and role: role: a, b", ids: [...named("a", "role", 12), ...named("b", "role", 8)] },
  ]);
  // Where every cut but the evenest goes through an area, the cut goes at an area's edge, however uneven.
  const edged = ok(list(["--asset", "web-surface", "--look"], [areaGate({ a: looks("a", "function", 5), b: looks("b", "function", 15), c: looks("c", "function", 5) })]));
  assert.deepEqual(passesOf(edged).map((p) => p.ids), [named("a", "function", 5), [...named("b", "function", 15), ...named("c", "function", 5)]]);
  // Between a cut at an area's edge and one at a stage's, as even as each other, the stage's wins.
  const staged = ok(list(["--asset", "web-surface", "--look"], [areaGate({ a: looks("a", "function", 12), b: looks("b", "function", 6), c: looks("c", "role", 12) })]));
  assert.deepEqual(passesOf(staged).map((p) => p.ids), [[...named("a", "function", 12), ...named("b", "function", 6)], named("c", "role", 12)]);
});

test("a list of 200 look questions runs in the fewest passes of at most 20, every function and role pass first, each in stage then area order", () => {
  const AREAS = ["a", "b", "c", "d", "e"];
  const STAGES = ["function", "role", "treatment", "value"];
  // Each area's file gives its stages out of order, so only the cut puts them in order.
  const gate = areaGate(Object.fromEntries(AREAS.map((area) => [area, [...STAGES].reverse().flatMap((stage) => looks(area, stage, 10))])));
  const out = ok(list(["--asset", "web-surface", "--look"], [gate]));
  assert.match(out, /^Gate list for web-surface: 200 question\(s\)\.$/m);
  const passes = passesOf(out);
  assert.equal(passes.length, 10);
  for (const p of passes) assert.ok(p.ids.length <= 20, `${p.label}: ${p.ids.length}`);
  assert.deepEqual(passes.flatMap((p) => p.ids), STAGES.flatMap((stage) => AREAS.flatMap((area) => named(area, stage, 10))));
  assert.deepEqual(passes.map((p) => p.label.slice(0, p.label.indexOf(":"))), [...Array(5).fill("function and role"), ...Array(5).fill("treatment and value, once the function and role passes' fixes land")]);
});

test("a question the building session could not measure is cut with its own area's questions", () => {
  const gate = areaGate({
    a: [...looks("a", "function", 2), ["vault.a-code", { by: "code", stage: "function" }]],
    b: looks("b", "function", 2),
  });
  const answered = writeText("answered.json", JSON.stringify({ answers: { c1: { "vault.a-code": { answer: "cannot measure", evidence: "no page" } } } }));
  const out = ok(list(["--asset", "web-surface", "--look", "--answered", answered, "--pass", "1"], [gate]));
  assert.deepEqual(ids(out), [...named("a", "function", 2), "vault.a-code", ...named("b", "function", 2)]);
});

test("the vault's store, staged records and all, gives a web surface no pass over 20 look questions", () => {
  for (const facts of [[], ["has-motion", "has-cta", "has-payment-control", "has-traced-mark"]]) {
    const out = ok(list(["--asset", "web-surface", "--staged", ...facts.flatMap((f) => ["--fact", f])], [STORE]));
    const looked = Number(out.match(/^Look questions, for the critics, in (\d+) passes/m)?.[1] ?? 1);
    const passes = passesOf(out.slice(0, out.indexOf("\nScript and code questions")));
    assert.equal(passes.length, looked > 1 ? looked : 0);
    for (const p of passes) assert.ok(p.ids.length <= 20, `${p.label}: ${p.ids.length}`);
  }
});

test("list --pass prints one pass alone, cut on a list of any length, and is refused as a pass the list does not run in", () => {
  const long = longGate(11, 10);
  const first = ok(list(["--asset", "web-surface", "--look", "--pass", "1"], [long]));
  assert.match(first, /^Gate list for web-surface: 11 question\(s\)\.$/m);
  assert.match(first, /^Look questions, for the critics, pass 1 of 2, function and role: function: long; role: long:$/m);
  assert.deepEqual(ids(first), passOrder("coarse", 11));
  const second = ok(list(["--asset", "web-surface", "--look", "--pass", "2"], [long]));
  assert.deepEqual(ids(second), passOrder("fine", 10));
  // A treatment pass whose fixes left 20 questions or fewer still asks only its own stages.
  const shrunk = ok(list(["--asset", "web-surface", "--look", "--pass", "2"], [longGate(11, 4)]));
  assert.deepEqual(ids(shrunk), passOrder("fine", 4));
  const r = list(["--asset", "web-surface", "--look", "--pass", "3"], [long]);
  assert.equal(r.status, 2, r.out);
  assert.match(r.err, /--pass is 3, but this look list runs in 2 pass\(es\)/);
  for (const bad of ["0", "x", "1.5"]) {
    const refused = list(["--asset", "web-surface", "--look", "--pass", bad], [long]);
    assert.equal(refused.status, 2, refused.out);
    assert.match(refused.err, new RegExp(`--pass is ${bad.replace(".", "\\.")}, not a pass number`));
  }
});

test("tally on a split list needs --pass, and tallies that pass's look answers with every script and code answer", () => {
  const long = longGate(11, 10);
  const scripted = gateFile("scripted.md", [["vault.reflow-script", { by: "script", stage: "value", script: "check-layout.py" }]]);
  const said = (answer) => ({ answer, evidence: `said ${answer}` });
  const answered = writeText("answered.json", JSON.stringify({ answers: { c1: { "vault.reflow-script": said("pass") } } }));
  const passIds = (pass) => (pass === 1 ? Array.from({ length: 11 }, (_, i) => `vault.coarse-${i}`) : Array.from({ length: 10 }, (_, i) => `vault.fine-${i}`));
  const critic = (name, questions) => writeText(name, JSON.stringify({ answers: { c1: Object.fromEntries(questions.map((id) => [id, said("Yes")])) }, clashes: [] }));
  const tally = (pass, questions) => {
    const critics = ["a", "b", "c"].flatMap((c) => ["--critic", critic(`critic-${c}-${pass}.json`, questions)]);
    return run("tally", "--asset", "web-surface", "--answered", answered, ...critics, ...(pass ? ["--pass", String(pass)] : []), long, scripted);
  };
  const whole = tally(null, [...passIds(1), ...passIds(2)]);
  assert.equal(whole.status, 2, whole.out);
  assert.match(whole.err, /the look list has 21 questions, more than 20, so its critics answer it in 2 passes: tally each with --pass 1 to 2/);
  for (const pass of [1, 2]) {
    const out = ok(tally(pass, passIds(pass)));
    assert.match(out, new RegExp(`^Tally of 1 candidate\\(s\\) on ${passIds(pass).length + 1} question\\(s\\)`, "m"));
    assert.deepEqual([...out.matchAll(/^ {2}\d+\. (\S+) \(/gm)].map((m) => m[1]), [...passIds(pass), "vault.reflow-script"]);
  }
  const short = tally(1, passIds(1).slice(1));
  assert.equal(short.status, 1, short.out);
  assert.match(short.out, /gives c1 no answer to vault\.coarse-0/);
});

test("tally tallies any pass of a list of 3 or more, and refuses a pass the list does not run in", () => {
  const gate = areaGate({ a: looks("a", "function", 15), b: looks("b", "function", 10), c: looks("c", "treatment", 5) });
  const said = (answer) => ({ answer, evidence: `said ${answer}` });
  const answered = writeText("answered.json", JSON.stringify({ answers: { c1: {} } }));
  const critic = (name, questions) => writeText(name, JSON.stringify({ answers: { c1: Object.fromEntries(questions.map((id) => [id, said("Yes")])) }, clashes: [] }));
  const tally = (pass) => {
    const critics = ["a", "b", "c"].flatMap((c) => ["--critic", critic(`critic-${c}.json`, named("c", "treatment", 5))]);
    return run("tally", "--asset", "web-surface", "--answered", answered, ...critics, "--pass", String(pass), gate);
  };
  const out = ok(tally(3));
  assert.deepEqual([...out.matchAll(/^ {2}\d+\. (\S+) \(/gm)].map((m) => m[1]), named("c", "treatment", 5));
  const r = tally(4);
  assert.equal(r.status, 2, r.out);
  assert.match(r.err, /--pass is 4, but this look list runs in 3 pass\(es\)/);
});

test("tally counts the questions whose script is owed apart, and the critics answer them as look questions", () => {
  const gate = gateFile("owed.md", [
    ["vault.walk-look", { by: "look", stage: "function" }],
    ["vault.measure-owed", { by: "script", stage: "value", script: "owed" }],
    ["vault.contrast-script", { by: "script", stage: "value", script: "check-access.py" }],
  ]);
  const said = (answer) => ({ answer, evidence: `said ${answer}` });
  const answered = writeText("answered.json", JSON.stringify({ answers: { c1: { "vault.contrast-script": said("pass") } } }));
  const critic = (owed) => writeText("critic.json", JSON.stringify({ answers: { c1: { "vault.walk-look": said("Yes"), "vault.measure-owed": said(owed) } }, clashes: [] }));
  const critics = [critic("No"), critic("No"), critic("No")].flatMap((c) => ["--critic", c]);
  const out = ok(run("tally", "--asset", "web-surface", "--answered", answered, ...critics, gate));
  assert.match(out, /^Tally of 1 candidate\(s\) on 3 question\(s\), 1 of them script owed, from /m);
  assert.match(out, /^ {2}2\. vault\.measure-owed \(script owed, so look\): fault, 3 No$/m);
  const scripted = writeText("answered.json", JSON.stringify({ answers: { c1: { "vault.contrast-script": said("pass"), "vault.measure-owed": said("pass") } } }));
  const r = run("tally", "--asset", "web-surface", "--answered", scripted, ...critics, gate);
  assert.equal(r.status, 1, r.out + r.err);
  assert.match(r.out, /answers vault\.measure-owed for c1, which is no script or code question on the list/);
});

test("tally takes a parts map carrying the building session's declaration as it takes the map alone", () => {
  const fixtures = path.join(__dirname, "fixtures", "gate", "affordance");
  const tally = (parts) => run("tally", "--asset", "web-surface", "--answered", path.join(fixtures, "answered.json"),
    ...["a", "b", "c"].flatMap((c) => ["--critic", path.join(fixtures, `critic-${c}.json`)]),
    ...["pill", "hidden", "minor", "split", "clean", "unlisted"].flatMap((c) => ["--parts", `${c}=${parts(path.join(fixtures, `parts-${c}.json`))}`]),
    path.join(fixtures, "gate.md"));
  const plain = ok(tally((f) => f));
  assert.equal(ok(tally((f) => buildCopy(f, (data) => (data.declared = { card: ".card" })))), plain);
});

test("list refuses a --parts file that is neither a parts map nor a declaration, or declares a part outside the vocabulary, with exit 1", () => {
  const refusals = [
    [writeText("bad.json", "{"), /bad\.json: is not JSON/],
    [writeText("bad.json", JSON.stringify({ hero: ".hero" })), /is neither a parts map, with a `parts` list, nor a parts declaration/],
    [DECLARED({ marquee: ".marquee" }), /declares marquee, which is no part in the vocabulary \(link, button/],
    [DECLARED({ card: 3 }), /declares card with neither a CSS selector nor null/],
    [writeText("bad.json", JSON.stringify({ declared: ["card"] })), /has a `declared` that is not an object of part names/],
  ];
  for (const [file, why] of refusals) {
    const r = list(builder("build", "--parts", file));
    assert.equal(r.status, 1, r.out + r.err);
    assert.match(r.out, why);
    assert.doesNotMatch(r.out, /Targets for/);
  }
});

test("list refuses a reader, stage or parts flag given where it does not belong, with exit 2", () => {
  const refusals = [
    [["--asset", "web-surface", "--reader", "layout"], /--reader is layout, not one of gate, builder, whole-page, type, script/],
    [["--asset", "web-surface", "--reader", "builder"], /--reader builder takes --stage direction, build, finish, not none/],
    [builder("sketch"), /takes --stage direction, build, finish, not sketch/],
    [["--asset", "web-surface", "--stage", "build"], /--stage is the builder's, not --reader gate's/],
    [["--asset", "web-surface", "--reader", "type", "--look"], /--look, --answered and --pass are the gate list's, not --reader type's/],
    [builder("build"), /--stage build needs the parts the candidate has/],
    [builder("direction", "--parts", PARTS_MAP), /--parts is the build stage's alone/],
  ];
  for (const [args, why] of refusals) {
    const r = list(args);
    assert.equal(r.status, 2, args.join(" "));
    assert.match(r.err, why);
    assert.match(r.err, /usage: node gate\.js check /);
  }
});

test("check refuses parts on a record that is not a treatment record, and a part outside the vocabulary", () => {
  const bad = gateFile("bad.md", [
    ["vault.role-parts", { by: "builder", stage: "role", parts: "card" }],
    ["vault.odd-parts", { by: "builder", stage: "treatment", parts: "card, marquee" }],
  ]);
  const r = run("check", bad);
  assert.equal(r.status, 1, r.out + r.err);
  assert.match(r.out, /bad\.md:\d+: vault\.role-parts names parts at stage role: only a treatment record is chosen by the candidate's parts/);
  assert.match(r.out, /bad\.md:\d+: vault\.odd-parts names a part outside the vocabulary: marquee \(the parts are link, /);
});

test("the parts vocabulary is the one rules.md lists, and every part it takes from a parts map is a role parts-map.py gives", () => {
  const rules = fs.readFileSync(path.join(__dirname, "..", "plugin", "skills", "design-critique", "rules.md"), "utf8");
  const line = rules.split("\n").find((l) => l.startsWith("- `parts`"));
  // Every bare word the line sets in code but the field's name and its stage.
  const named = [...line.matchAll(/`([a-z-]+)`/g)].map((m) => m[1]).filter((w) => !["parts", "treatment"].includes(w));
  assert.deepEqual(named, PARTS);
  const partsMap = fs.readFileSync(path.join(__dirname, "..", "plugin", "skills", "design-round", "scripts", "parts-map.py"), "utf8");
  for (const role of MAPPED_PARTS) assert.match(partsMap, new RegExp(`role=${role}\\b|'${role}'|${role}: '${role}'`), role);
});

test("design-round §1c's three stage commands run as written on the vault's store, its parts declaration in the form gate.js reads", () => {
  const root = path.join(__dirname, "..", "plugin", "skills");
  const section = fs.readFileSync(path.join(root, "design-round", "SKILL.md"), "utf8").split("### 1c. The building session")[1].split(/\n##? /)[0];
  const commands = [...section.matchAll(/`node gate\.js list ([^`]*?) > [^`]*`/g)].map((m) => m[1]);
  assert.deepEqual(commands.map((c) => c.match(/--stage (\w+)/)?.[1]), ["direction", "build", "finish"]);
  const form = '{"declared": {<part>: <its CSS selector, or null>}}';
  assert.ok(section.includes(`\`${form}\``), "§1c gives the declaration's form");
  assert.ok(run("list").err.includes(form), "gate.js's usage gives the same form");
  const declared = writeText("parts-declared.json", form.replace("<part>", '"hero"').replace("<its CSS selector, or null>", '".hero"'));
  for (const c of commands) {
    const args = c.replace("<asset>", "--asset web-surface").replace("<round folder>/<candidate>/parts-declared.json", declared).replace("<gate files>", path.join(root, "design-critique", "rules"));
    const r = run("list", ...args.split(" "));
    assert.equal(r.status, 0, `${c}: ${r.err}`);
  }
});

const lookWriting = (id, stage, writes, { strength = "house judgement", yields = "none" } = {}) =>
  record(id, { by: "look", stage })
    .replace(`- writes: ${id}`, `- writes: ${writes}`)
    .replace("strength: house judgement", `strength: ${strength}`)
    .replace("- yields-to: none", `- yields-to: ${yields}`);
const clashLine = (out, a, b) => out.split("\n").find((l) => l.startsWith("- ") && l.includes(` ${a} and `) && l.includes(` ${b} both`));

test("a clash between two stages is settled by the dependency order, the earlier standing over any level unless whether it yields is unread; within a stage, or with no stage, the level decides (#549)", () => {
  const vault = writeText("vault.md", `# vault\n\n${[
    lookWriting("vault.edge-style", "function", "part-edge"),
    lookWriting("vault.law-gap", "value", "gap", { strength: "law: a made-up statute" }),
    lookWriting("vault.early-edge", "function", "edge-width", { yields: "level 4" }),
    lookWriting("vault.late-edge", "treatment", "edge-width"),
    lookWriting("vault.early-fill", "function", "fill"),
    lookWriting("vault.late-fill", "treatment", "fill", { yields: "level 4" }),
    lookWriting("vault.tone", "treatment", "tone"),
    lookWriting("vault.pace", "role", "pace"),
  ].join("\n\n")}\n`);
  const project = writeText("acme.md", `# acme\n\n${[
    lookWriting("acme.edge-style", "treatment", "part-edge"),
    lookWriting("acme.gap", "role", "gap"),
    lookWriting("acme.tone", "treatment", "tone"),
    lookWriting("acme.pace", undefined, "pace"),
    lookWriting("acme.early-gap", "role", "inset"),
    lookWriting("acme.late-gap", "value", "inset"),
  ].join("\n\n")}\n`);
  assert.equal(run("check", vault, project).status, 0);
  const out = ok(list(["--asset", "web-surface"], [vault, project]));
  const byOrder = "Settled by precedence (the dependency order decides first, and a later step never changes an earlier one)";
  assert.match(clashLine(out, "vault.edge-style", "acme.edge-style"), new RegExp(`^- ${byOrder.replace(/[()]/g, "\\$&")}: .*; vault\\.edge-style stands\\.$`));
  assert.match(clashLine(out, "vault.law-gap", "acme.gap"), /\(the dependency order .*; acme\.gap stands\.$/);
  assert.match(clashLine(out, "vault.tone", "acme.tone"), /^- Settled by precedence \(within one step, the project beats .*; acme\.tone stands\.$/);
  assert.match(clashLine(out, "vault.pace", "acme.pace"), /^- Settled by precedence \(within one step, the project beats .*; acme\.pace stands\.$/);
  assert.match(clashLine(out, "acme.early-gap", "acme.late-gap"), /\(the dependency order .*; acme\.early-gap stands\.$/);
  assert.match(clashLine(out, "vault.early-fill", "vault.late-fill"), /\(the dependency order .*; vault\.early-fill stands\.$/);
  assert.match(clashLine(out, "vault.early-edge", "vault.late-edge"), /^- For the founder \(it turns on a vault level the rule records do not record\)/);
});
