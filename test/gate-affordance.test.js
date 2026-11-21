"use strict";
// gate.js tally on vault.affordance (#162), the one question the look critics answer part by part: each part on
// parts-map.py's key looks actable or not, and the tally compares that with whether the map says a visitor can act on
// it. Loosen it and a static pill styled as a button, a control that looks like nothing, or a link going nowhere passes
// the gate, or a split reaches the founder before a settle critic has looked closer.
const assert = require("node:assert/strict");
const { gateScratch, refusedWithout, runGate: run } = require("./gate-files.js");
const path = require("node:path");
const { test } = require("node:test");

const FIXTURES = path.join(__dirname, "fixtures", "gate", "affordance");
const GATE = path.join(FIXTURES, "gate.md");
const ANSWERED = path.join(FIXTURES, "answered.json");
const CRITICS = ["critic-a.json", "critic-b.json", "critic-c.json"].map((f) => path.join(FIXTURES, f));
const CANDIDATES = ["pill", "hidden", "minor", "split", "clean", "unlisted"];
const PARTS = Object.fromEntries(CANDIDATES.map((c) => [c, path.join(FIXTURES, `parts-${c}.json`)]));

const { writeSettle, buildBrokenCopy } = gateScratch("gate-affordance-");

const tally = ({ critics = CRITICS, parts = PARTS, settles = [] } = {}) =>
  run("tally", "--asset", "web-surface", "--answered", ANSWERED, ...critics.flatMap((c) => ["--critic", c]),
    ...Object.entries(parts).flatMap(([c, f]) => ["--parts", `${c}=${f}`]), ...settles.flatMap((s) => ["--settle", s]), GATE);
// A settle critic's file settling the split candidate's p2 and the unlisted candidate's parts off the key; its path.
const settleBoth = ({ p2 = "No", offKey = "No" } = {}) => writeSettle({
  split: { "vault.affordance": { parts: { p2: { answer: p2, evidence: `settle on p2: ${p2}` } } } },
  unlisted: { "vault.affordance": { unlisted: { answer: offKey, evidence: `settle off the key: ${offKey}` } } },
});

// One candidate's block of tally's output.
const block = (out, candidate) => {
  const start = out.indexOf(`\n${candidate}: `);
  const end = out.slice(start + 1).search(/\n(\S+: \d+ fault|Clashes)/);
  return out.slice(start + 1, start + 1 + end);
};
const verdict = (out, candidate, id) => block(out, candidate).match(new RegExp(`^ {2}\\d+\\. ${id.replace(".", "\\.")} \\(([^)]+)\\): (\\w+)`, "m"))?.slice(1);

const refused = refusedWithout(/^Tally of/m);

test("a part that cannot be acted on but looks as if it can is false, and one that can but does not look it is hidden: each a fault", () => {
  const r = tally();
  assert.equal(r.status, 0, r.out + r.err);
  assert.deepEqual(verdict(r.out, "pill", "vault.affordance"), ["look, part by part", "fault"]);
  assert.match(block(r.out, "pill"), /^ {5}p2 "Free breakfast": false, it cannot be acted on and looks as if it can \(3 Yes\)$/m);
  assert.deepEqual(verdict(r.out, "hidden", "vault.affordance"), ["look, part by part", "fault"]);
  assert.match(block(r.out, "hidden"), /^ {5}p2 "Read more": hidden, it can be acted on and does not look it \(3 No\)$/m);
  assert.match(r.out, /^pill: 1 fault\(s\), 0 split, 0 for the founder, 2 pass\.$/m);
});

test("a part that looks as it is, actable or not, passes and is not printed", () => {
  const { out } = tally();
  assert.deepEqual(verdict(out, "clean", "vault.affordance"), ["look, part by part", "pass"]);
  assert.doesNotMatch(block(out, "clean"), /p1 "Rooms"|p2 "Breakfast/);
  assert.doesNotMatch(block(out, "pill"), /p1 "Book a bed"/);
});

test("a hidden link that goes where a part that looks actable goes is reported and does not fail", () => {
  const { out } = tally();
  assert.deepEqual(verdict(out, "minor", "vault.affordance"), ["look, part by part", "pass"]);
  assert.match(block(out, "minor"), /^ {5}p2 "Photo of Hostel A": hidden, minor: p1 looks actable and goes to the same place \(3 No\)$/m);
  const elsewhere = buildBrokenCopy(PARTS.minor, (d) => (d.parts[1].href = "#b"));
  assert.deepEqual(verdict(tally({ parts: { ...PARTS, minor: elsewhere } }).out, "minor", "vault.affordance"), ["look, part by part", "fault"]);
  const unseen = CRITICS.map((c) => buildBrokenCopy(c, (d) => (d.answers.minor["vault.affordance"].parts.p1.answer = "No")));
  assert.deepEqual(verdict(tally({ critics: unseen }).out, "minor", "vault.affordance"), ["look, part by part", "fault"], "p1 looks static too");
  const nowhere = buildBrokenCopy(PARTS.hidden, (d) => (d.parts[0].href = null));
  assert.deepEqual(verdict(tally({ parts: { ...PARTS, hidden: nowhere } }).out, "hidden", "vault.affordance"), ["look, part by part", "fault"], "two parts that go nowhere do not go to the same place");
});

test("a link the map marks as going nowhere is dead, a fault however it looks and owing no settle critic (#236)", () => {
  const dead = buildBrokenCopy(PARTS.clean, (d) => (d.parts[0].dead = "#destinations"));
  const looked = tally({ parts: { ...PARTS, clean: dead } });
  assert.deepEqual(verdict(looked.out, "clean", "vault.affordance"), ["look, part by part", "fault"]);
  assert.match(block(looked.out, "clean"), /^ {5}p1 "Rooms": dead, it goes to #destinations, which nothing on the page carries \(3 Yes\)$/m);
  const placeholder = buildBrokenCopy(PARTS.split, (d) => (d.parts[1].dead = "#"));
  const split = tally({ parts: { ...PARTS, split: placeholder } });
  assert.deepEqual(verdict(split.out, "split", "vault.affordance"), ["look, part by part", "fault"]);
  assert.match(block(split.out, "split"), /^ {5}p2 "Our rooms": dead, it goes to # alone \(1 Yes and 1 No and 1 Unsure\)$/m);
  const live = buildBrokenCopy(PARTS.clean, (d) => (d.parts[0].dead = null));
  assert.deepEqual(verdict(tally({ parts: { ...PARTS, clean: live } }).out, "clean", "vault.affordance"), ["look, part by part", "pass"]);
  const shapeless = buildBrokenCopy(PARTS.clean, (d) => (d.parts[0].dead = true));
  refused(tally({ parts: { ...PARTS, clean: shapeless } }), /parts-clean\.json: part 1 has a `dead` that is neither null nor a link's target/);
});

test("a part the critics split on, or a part a critic names off the key, is a split for a settle critic, with every critic's evidence", () => {
  const { out } = tally();
  assert.deepEqual(verdict(out, "split", "vault.affordance"), ["look, part by part", "split"]);
  const split = block(out, "split");
  assert.match(split, /^ {5}p2 "Our rooms": split, for a settle critic, 1 Yes and 1 No and 1 Unsure$/m);
  for (const [critic, answer] of [["a", "Yes"], ["b", "No"], ["c", "Unsure"]]) {
    assert.match(split, new RegExp(`^ {7}\\S*critic-${critic}\\.json: ${answer}\\. critic ${critic} on p2$`, "m"));
  }
  assert.deepEqual(verdict(out, "unlisted", "vault.affordance"), ["look, part by part", "split"]);
  assert.match(block(out, "unlisted"), /^ {5}parts off the key: split, for a settle critic$/m);
  assert.match(block(out, "unlisted"), /^ {5}\S*critic-a\.json names a part off the key: the 'Call us' line at the foot is in the link colour$/m);
});

test("a false part outranks a split on another part: the question is a fault", () => {
  const both = buildBrokenCopy(PARTS.split, (d) => d.parts.push({ id: "p3", actable: false, href: null, text: "Free breakfast" }));
  const critics = CRITICS.map((c) => buildBrokenCopy(c, (d) => (d.answers.split["vault.affordance"].parts.p3 = { answer: "Yes", evidence: "a filled pill" })));
  const { out } = tally({ critics, parts: { ...PARTS, split: both } });
  assert.deepEqual(verdict(out, "split", "vault.affordance"), ["look, part by part", "fault"]);
  assert.match(block(out, "split"), /p2 "Our rooms": split/);
});

test("a settle critic settles each split part and the parts off the key: Yes to a static part, or to a part off the key, is false", () => {
  const passed = tally({ settles: [settleBoth()] });
  assert.equal(passed.status, 0, passed.out + passed.err);
  assert.deepEqual(verdict(passed.out, "split", "vault.affordance"), ["look, part by part", "pass"]);
  assert.match(block(passed.out, "split"), /^ {5}p2 "Our rooms": pass \(1 Yes and 1 No and 1 Unsure; settled by \S*settle\.json: No\)\n(?: {7}\S*critic-.\.json: .*\n){3} {7}\S*settle\.json: No\. settle on p2: No$/m);
  assert.deepEqual(verdict(passed.out, "unlisted", "vault.affordance"), ["look, part by part", "pass"]);
  const failed = tally({ settles: [settleBoth({ p2: "Yes", offKey: "Yes" })] });
  assert.match(block(failed.out, "split"), /p2 "Our rooms": false, it cannot be acted on and looks as if it can/);
  assert.deepEqual(verdict(failed.out, "unlisted", "vault.affordance"), ["look, part by part", "fault"]);
  assert.match(block(failed.out, "unlisted"), /parts off the key: false, one looks as if it can be acted on; settled by/);
  const unsure = tally({ settles: [settleBoth({ p2: "Unsure", offKey: "Unsure" })] });
  assert.deepEqual(verdict(unsure.out, "split", "vault.affordance"), ["look, part by part", "founder"]);
  assert.deepEqual(verdict(unsure.out, "unlisted", "vault.affordance"), ["look, part by part", "founder"]);
});

test("a settle critic may not settle a part the critics agreed on, nor the parts off the key where none was named", () => {
  const agreed = buildBrokenCopy(settleBoth(), (d) => (d.answers.split["vault.affordance"].parts.p1 = { answer: "No", evidence: "x" }));
  refused(tally({ settles: [agreed] }), /settles vault\.affordance's part p1 for split, which no three critics split on/);
  const none = buildBrokenCopy(settleBoth(), (d) => (d.answers.clean = { "vault.affordance": { unlisted: { answer: "No", evidence: "x" } } }));
  refused(tally({ settles: [none] }), /settles vault\.affordance's parts off the key for clean, which no three critics split on/);
  const empty = buildBrokenCopy(settleBoth(), (d) => (d.answers.split["vault.affordance"] = {}));
  refused(tally({ settles: [empty] }), /settles vault\.affordance for split with no `parts` object and no `unlisted` answer/);
});

test("a look question passed with a minor case prints it, as rules.md's function walk asks", () => {
  const { out } = tally();
  assert.deepEqual(verdict(out, "clean", "vault.edge-look"), ["look", "pass"]);
  assert.match(block(out, "clean"), /vault\.edge-look \(look\): pass, 3 Yes, a minor case reported\n {5}\S*critic-b\.json: Minor: the footer rule is a shade light\n/);
  assert.doesNotMatch(block(out, "pill"), /critic a on vault\.edge-look/, "a plain pass prints no evidence");
});

test("a critic who answers vault.affordance whole, misses a part or answers one off the key is refused", () => {
  const whole = buildBrokenCopy(CRITICS[0], (d) => (d.answers.pill["vault.affordance"] = { answer: "Yes", evidence: "all fine" }));
  refused(tally({ critics: [whole, ...CRITICS.slice(1)] }), /critic-a\.json: answers vault\.affordance for pill whole, not part by part under `parts`/);
  const missing = buildBrokenCopy(CRITICS[1], (d) => delete d.answers.pill["vault.affordance"].parts.p2);
  refused(tally({ critics: [CRITICS[0], missing, CRITICS[2]] }), /critic-b\.json: gives pill no answer to vault\.affordance's part p2/);
  const stranger = buildBrokenCopy(CRITICS[2], (d) => (d.answers.pill["vault.affordance"].parts.p9 = { answer: "No", evidence: "x" }));
  refused(tally({ critics: [...CRITICS.slice(0, 2), stranger] }), /critic-c\.json: answers vault\.affordance's part p9 for pill, which is not on its parts map/);
});

test("a part's answer outside Yes, No and Unsure, without one line of evidence, or a bad unlisted line is refused", () => {
  const maybe = buildBrokenCopy(CRITICS[0], (d) => (d.answers.pill["vault.affordance"].parts.p2.answer = "maybe"));
  refused(tally({ critics: [maybe, ...CRITICS.slice(1)] }), /answers vault\.affordance's part p2 for pill "maybe", not one of yes, no, unsure/);
  const mute = buildBrokenCopy(CRITICS[0], (d) => (d.answers.pill["vault.affordance"].parts.p2.evidence = ""));
  refused(tally({ critics: [mute, ...CRITICS.slice(1)] }), /gives vault\.affordance's part p2 for pill no one line of evidence/);
  for (const unlisted of ["one line", [""], ["two\nlines"]]) {
    const bad = buildBrokenCopy(CRITICS[0], (d) => (d.answers.pill["vault.affordance"].unlisted = unlisted));
    refused(tally({ critics: [bad, ...CRITICS.slice(1)] }), /gives vault\.affordance for pill an `unlisted` that is not a list of one-line parts/);
  }
});

test("a parts map is owed for each candidate where vault.affordance is on the list, and only those, in the map's form", () => {
  const { pill, ...rest } = PARTS;
  const none = tally({ parts: rest });
  assert.equal(none.status, 2);
  assert.match(none.err, /^tally needs a parts map for pill, --parts pill=<parts\.json>/);
  const stranger = tally({ parts: { ...PARTS, nobody: PARTS.pill } });
  assert.equal(stranger.status, 2);
  assert.match(stranger.err, /^--parts names nobody, which the building session's answers do not name/);
  const bare = run("tally", "--asset", "web-surface", "--answered", ANSWERED, ...CRITICS.flatMap((c) => ["--critic", c]), "--parts", "pill", GATE);
  assert.equal(bare.status, 2);
  assert.match(bare.err, /^--parts takes <candidate>=<parts\.json>, not pill/);
  const shapeless = buildBrokenCopy(PARTS.pill, (d) => delete d.parts[1].actable);
  refused(tally({ parts: { ...PARTS, pill: shapeless } }), /parts-pill\.json: part 2 has no id, no actable true or false, or no text/);
  const twice = buildBrokenCopy(PARTS.pill, (d) => (d.parts[1].id = "p1"));
  refused(tally({ parts: { ...PARTS, pill: twice } }), /parts-pill\.json: part 2 has the id p1 again/);
});
