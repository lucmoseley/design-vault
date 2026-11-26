"use strict";
const assert = require("node:assert/strict");
const { gateScratch, refusedWithout, runGate } = require("./gate-files.js");
const path = require("node:path");
const { test } = require("node:test");

const GATE = path.join(__dirname, "fixtures", "gate", "tally", "gate.md");
const FIXTURES = path.join(__dirname, "fixtures", "gate", "recheck");
const ANSWERED = path.join(FIXTURES, "answered.json");
const BEFORE = path.join(FIXTURES, "before.json");
const CRITICS = ["critic-a.json", "critic-b.json", "critic-c.json"].map((f) => path.join(FIXTURES, f));
const FAULTS = ["v1-arches:vault.tone-look", "v2-water:vault.proof", "v2-water:vault.contrast"];

const { writeSettle, writeText, buildBrokenCopy } = gateScratch("gate-recheck-");

const recheck = ({ answered = ANSWERED, before = BEFORE, critics = CRITICS, faults = FAULTS, settles = [] } = {}) =>
  runGate("recheck", "--asset", "web-surface", ...(before ? ["--before", before] : []), "--answered", answered, ...faults.flatMap((f) => ["--fault", f]), ...critics.flatMap((c) => ["--critic", c]), ...settles.flatMap((s) => ["--settle", s]), GATE);

function parseOutcomes(out) {
  const found = {};
  let current;
  for (const line of out.split("\n")) {
    const head = line.match(/^(\S+): \d+ cleared/);
    if (head) current = head[1];
    const cleared = line.match(/^ {2}(\S+): cleared$/);
    if (cleared) found[`${current} ${cleared[1]}`] = "cleared";
    const split = line.match(/^ {2}(\S+): split, for a settle critic$/);
    if (split) found[`${current} ${split[1]}`] = "split";
    const stopped = line.match(/^ {2}(\S+): stop, for the reveal: (.*)$/);
    if (stopped) found[`${current} ${stopped[1]}`] = [...stopped[2].matchAll(/stop signal (\d)/g)].map((m) => m[1]).join(",");
  }
  return found;
}

const allCritics = (edit) => CRITICS.map((c) => buildBrokenCopy(c, edit));
const refused = refusedWithout(/^Re-check of/m);

test("a fixed fault clears only on three Yes that it is gone and three Yes that nothing else got worse (#193)", () => {
  const r = recheck();
  assert.equal(r.status, 0, r.out + r.err);
  const o = parseOutcomes(r.out);
  assert.equal(o["v1-arches vault.tone-look"], "cleared");
  assert.equal(o["v2-water vault.contrast"], "split", "two Yes and one No is a split, not a clear");
  assert.match(r.out, /^v1-arches: 1 cleared, 0 stopped, 0 split\.$/m);
  assert.match(r.out, /^v2-water: 1 cleared, 0 stopped, 1 split\.$/m);
});

test("a re-check split goes to a settle critic: its Yes clears the fault, and only its Unsure stops it on the third signal", () => {
  const settle = (answer) => writeSettle({ "v2-water": { "vault.contrast": { answer, evidence: `measured: ${answer}` } } });
  const yes = recheck({ settles: [settle("Yes")] });
  assert.equal(yes.status, 0, yes.out + yes.err);
  assert.equal(parseOutcomes(yes.out)["v2-water vault.contrast"], "cleared");
  assert.match(yes.out, /vault\.contrast \(script cannot measure it, so look\): gone, 2 Yes and 1 No; settled by \S*settle\.json: Yes/);
  assert.equal(parseOutcomes(recheck({ settles: [settle("No")] }).out)["v2-water vault.contrast"], "2");
  const unsure = recheck({ settles: [settle("Unsure")] });
  assert.equal(parseOutcomes(unsure.out)["v2-water vault.contrast"], "3");
  assert.match(unsure.out, /vault\.contrast: stop, for the reveal: the critics split and the settle critic is unsure \(stop signal 3\)/);
  refused(recheck({ settles: [writeSettle({ "v1-arches": { "vault.tone-look": { answer: "Yes", evidence: "x" } } })] }), /settles vault\.tone-look for v1-arches, which no three critics split on/);
});

test("a fault whose script or code re-run settles it takes the re-run's word, and no critic answers it", () => {
  const o = parseOutcomes(recheck().out);
  assert.equal(o["v2-water vault.proof"], "cleared");
  const failed = buildBrokenCopy(ANSWERED, (d) => (d.answers["v2-water"]["vault.proof"] = { answer: "fail", evidence: "the count still has no source" }));
  const r = recheck({ answered: failed });
  assert.equal(parseOutcomes(r.out)["v2-water vault.proof"], "2");
  assert.match(r.out, /vault\.proof \(code re-run\): not gone\n {5}the count still has no source/);
  const asked = allCritics((d) => (d.answers["v2-water"]["vault.proof"] = { answer: "yes", evidence: "x" }));
  refused(recheck({ critics: asked }), /critic-a\.json: answers vault\.proof for v2-water, which its re-check does not ask/);
});

test("three No that a fault is gone stop it on the second signal, and one No or Unsure is a split", () => {
  const no = allCritics((d) => (d.answers["v1-arches"]["vault.tone-look"].answer = "No"));
  assert.equal(parseOutcomes(recheck({ critics: no }).out)["v1-arches vault.tone-look"], "2");
  const unsure = [buildBrokenCopy(CRITICS[0], (d) => (d.answers["v1-arches"]["vault.tone-look"].answer = "Unsure")), ...CRITICS.slice(1)];
  const r = recheck({ critics: unsure });
  assert.equal(parseOutcomes(r.out)["v1-arches vault.tone-look"], "split");
  assert.match(r.out, /vault\.tone-look \(look\): split, for a settle critic, 2 Yes and 1 Unsure\n {5}\S*critic-a\.json: Unsure\./);
});

test("three No that nothing else got worse stop every fault fixed on that candidate on the first signal", () => {
  const broke = allCritics((d) => (d.answers["v2-water"].others = { answer: "No", evidence: "the darkened video now hides the focus ring" }));
  const r = recheck({ critics: broke });
  const o = parseOutcomes(r.out);
  assert.equal(o["v2-water vault.proof"], "1", "a re-run's pass does not clear a fix that broke another question");
  assert.equal(o["v2-water vault.contrast"], "1", "a split left unsettled where a stop signal already holds");
  assert.equal(o["v1-arches vault.tone-look"], "cleared", "another candidate's fix stands");
  assert.match(r.out, /every other question: broken, 3 No\n(?: {5}\S*critic-.\.json: No\. the darkened video now hides the focus ring\n){3}/);
  const split = [buildBrokenCopy(CRITICS[2], (d) => (d.answers["v1-arches"].others.answer = "No")), ...CRITICS.slice(0, 2)];
  assert.equal(parseOutcomes(recheck({ critics: split }).out)["v1-arches vault.tone-look"], "split");
  const othersSettle = writeSettle({ "v1-arches": { others: { answer: "No", evidence: "the edge test now fails" } }, "v2-water": { "vault.contrast": { answer: "Yes", evidence: "x" } } });
  assert.equal(parseOutcomes(recheck({ critics: split, settles: [othersSettle] }).out)["v1-arches vault.tone-look"], "1");
});

test("a script or code question the candidate passed before the fix and fails after it stops every fault fixed on it", () => {
  const broke = buildBrokenCopy(ANSWERED, (d) => (d.answers["v1-arches"]["vault.contrast"] = { answer: "fail", evidence: "v1-arches/access/access.json, exit 1: the new tone fails 4.5:1" }));
  const r = recheck({ answered: broke });
  assert.equal(parseOutcomes(r.out)["v1-arches vault.tone-look"], "1", "three Yes from the critics do not outweigh the re-run");
  assert.match(r.out, /3\. vault\.contrast \(script re-run\): passed before the fix, fails now\n {5}v1-arches\/access\/access\.json, exit 1/);
  const v2 = buildBrokenCopy(ANSWERED, (d) => (d.answers["v2-water"]["vault.proof"].answer = "fail"));
  assert.equal(parseOutcomes(recheck({ answered: v2 }).out)["v2-water vault.proof"], "2");
});

test("a re-check critic must answer each fault it is owed and the other questions, for exactly the candidates fixed", () => {
  const noOthers = buildBrokenCopy(CRITICS[1], (d) => delete d.answers["v1-arches"].others);
  refused(recheck({ critics: [CRITICS[0], noOthers, CRITICS[2]] }), /critic-b\.json: gives v1-arches no answer to others/);
  const noFault = buildBrokenCopy(CRITICS[2], (d) => delete d.answers["v2-water"]["vault.contrast"]);
  refused(recheck({ critics: [CRITICS[0], CRITICS[1], noFault] }), /critic-c\.json: gives v2-water no answer to vault\.contrast/);
  const wandered = buildBrokenCopy(CRITICS[0], (d) => (d.answers["v1-arches"]["vault.edge-look"] = { answer: "no", evidence: "x" }));
  refused(recheck({ critics: [wandered, ...CRITICS.slice(1)] }), /answers vault\.edge-look for v1-arches, which its re-check does not ask/);
  refused(recheck({ faults: FAULTS.slice(1) }), /critic-a\.json: answers for v1-arches, which no --fault names/);
  const pass = buildBrokenCopy(CRITICS[0], (d) => (d.answers["v1-arches"].others.answer = "pass"));
  refused(recheck({ critics: [pass, ...CRITICS.slice(1)] }), /answers others for v1-arches "pass", not one of yes, no, unsure/);
});

test("a --fault naming a stranger, a question off the list or a fault twice is refused", () => {
  refused(recheck({ faults: [...FAULTS, "v9-nobody:vault.proof"] }), /--fault v9-nobody:vault\.proof names v9-nobody, which the building session's answers do not name/);
  refused(recheck({ faults: [...FAULTS, "v1-arches:vault.motion-look"] }), /names vault\.motion-look, which is not on the list/);
  refused(recheck({ faults: [...FAULTS, "v1-arches"] }), /--fault v1-arches names no question/);
  refused(recheck({ faults: [...FAULTS, FAULTS[0]] }), /--fault v1-arches:vault\.tone-look is given twice/);
});

test("a re-check takes three critics and at least one --fault, or it is bad usage", () => {
  for (const critics of [CRITICS.slice(0, 1), [...CRITICS, CRITICS[0]]]) {
    const r = recheck({ critics });
    assert.equal(r.status, 2);
    assert.match(r.err, /^recheck takes 3 re-check critics' answers/);
  }
  const noBefore = recheck({ before: null });
  assert.equal(noBefore.status, 2);
  assert.match(noBefore.err, /^recheck needs the building session's answers from before the fix, --before <file>/);
  const none = recheck({ faults: [] });
  assert.equal(none.status, 2);
  assert.match(none.err, /^recheck needs each fault fixed, --fault <candidate>:<id>/);
});

const AFFORDANCE = path.join(__dirname, "fixtures", "gate", "affordance");
const AFFORDANCE_ANSWERED = path.join(AFFORDANCE, "answered.json");
const CLEAN_PARTS = path.join(AFFORDANCE, "parts-clean.json");
const DEAD_PARTS = buildBrokenCopy(CLEAN_PARTS, (d) => (d.parts[0].dead = "#rooms"));

function recheckAffordance({ fault = "vault.affordance", parts = [`clean=${CLEAN_PARTS}`], before = [`clean=${DEAD_PARTS}`], answer = "Yes", settles = [] } = {}) {
  const critics = ["a", "b", "c"].map((x) => writeText(`recheck-${x}.json`, JSON.stringify({ answers: { clean: {
    [fault]: { answer, evidence: `the fault looks gone: ${answer}` },
    others: { answer: "Yes", evidence: "nothing else changed" },
  } } })));
  return runGate("recheck", "--asset", "web-surface", "--before", AFFORDANCE_ANSWERED, "--answered", AFFORDANCE_ANSWERED,
    "--fault", `clean:${fault}`, ...critics.flatMap((c) => ["--critic", c]), ...parts.flatMap((p) => ["--parts", p]),
    ...before.flatMap((p) => ["--before-parts", p]), ...settles.flatMap((f) => ["--settle", f]), path.join(AFFORDANCE, "gate.md"));
}

test("a dead link still on the re-run parts map keeps vault.affordance's fault whatever the critics answer, and a fixed one clears on their Yes (#260)", () => {
  const fixed = recheckAffordance();
  assert.equal(fixed.status, 0, fixed.out + fixed.err);
  assert.equal(parseOutcomes(fixed.out)["clean vault.affordance"], "cleared");
  const left = recheckAffordance({ parts: [`clean=${DEAD_PARTS}`] });
  assert.equal(left.status, 0, left.out + left.err);
  assert.equal(parseOutcomes(left.out)["clean vault.affordance"], "2", "three Yes do not clear a link the map says goes nowhere");
  assert.match(left.out, /vault\.affordance \(look\): not gone, 3 Yes\n {5}re-run parts map: p1 "Rooms": dead, it goes to #rooms, which nothing on the page carries$/m);
  const split = recheckAffordance({ parts: [`clean=${DEAD_PARTS}`], answer: "Unsure" });
  assert.equal(split.status, 0, split.out + split.err);
  assert.equal(parseOutcomes(split.out)["clean vault.affordance"], "2", "a dead link owes no settle critic");
  const settle = writeSettle({ clean: { "vault.affordance": { answer: "Yes", evidence: "looks fine" } } });
  refused(recheckAffordance({ parts: [`clean=${DEAD_PARTS}`], answer: "Unsure", settles: [settle] }), /settles vault\.affordance for clean, which no three critics split on/);
  const killed = recheckAffordance({ parts: [`clean=${DEAD_PARTS}`], before: [`clean=${CLEAN_PARTS}`] });
  assert.equal(killed.status, 0, killed.out + killed.err);
  assert.equal(parseOutcomes(killed.out)["clean vault.affordance"], "2", "a link a fix aimed at vault.affordance left dead is that question failing again, not another one broken");
  assert.match(killed.out, /vault\.affordance: stop, for the reveal: the same question fails again \(stop signal 2\)$/m);
  assert.doesNotMatch(killed.out, /a link going nowhere since the fix/, "no line names a stop no fault met");
});

test("a fix aimed at another fault that leaves a link going nowhere stops on the first signal whatever the critics answer, and one that does not clears (#264)", () => {
  const edge = (before, parts) => recheckAffordance({ fault: "vault.edge-look", before: [`clean=${before}`], parts: [`clean=${parts}`] });
  const kept = edge(CLEAN_PARTS, CLEAN_PARTS);
  assert.equal(kept.status, 0, kept.out + kept.err);
  assert.equal(parseOutcomes(kept.out)["clean vault.edge-look"], "cleared");
  const broke = edge(CLEAN_PARTS, DEAD_PARTS);
  assert.equal(broke.status, 0, broke.out + broke.err);
  assert.equal(parseOutcomes(broke.out)["clean vault.edge-look"], "1", "three Yes to others do not outweigh a link the map says the fix killed");
  assert.match(broke.out, /^ {2}1\. vault\.affordance \(re-run parts map\): a link going nowhere since the fix\n {5}p1 "Rooms": dead, it goes to #rooms, which nothing on the page carries$/m);
  assert.equal(parseOutcomes(edge(DEAD_PARTS, DEAD_PARTS).out)["clean vault.edge-look"], "cleared", "a link dead before the fix is not one the fix broke");
  const renumbered = buildBrokenCopy(DEAD_PARTS, (d) => {
    d.parts.unshift({ id: "p0", actable: false, href: null, text: "Welcome." });
    d.parts.forEach((p, i) => (p.id = `p${i + 1}`));
    d.parts[1].text = "Our rooms";
  });
  assert.equal(parseOutcomes(edge(DEAD_PARTS, renumbered).out)["clean vault.edge-look"], "cleared", "the same dead link, renumbered and reworded, is not new");
  const moved = buildBrokenCopy(DEAD_PARTS, (d) => (d.parts[0].dead = "#"));
  assert.equal(parseOutcomes(edge(DEAD_PARTS, moved).out)["clean vault.edge-look"], "1", "a dead link sent somewhere else that goes nowhere is new");
  const twice = buildBrokenCopy(DEAD_PARTS, (d) => d.parts.push({ id: "p3", actable: true, href: "#rooms", dead: "#rooms", text: "See rooms" }));
  assert.equal(parseOutcomes(edge(DEAD_PARTS, twice).out)["clean vault.edge-look"], "1", "a second link to the same missing place is new");
});

test("a re-check where vault.affordance is on the list needs each fixed candidate's re-run parts map and its map from before the fix, and takes no other", () => {
  for (const fault of ["vault.affordance", "vault.edge-look"]) {
    const none = recheckAffordance({ fault, parts: [] });
    assert.equal(none.status, 2);
    assert.match(none.err, /^recheck needs a parts map for clean, --parts clean=<parts\.json>, since vault\.affordance is on the list/);
    const noBefore = recheckAffordance({ fault, before: [] });
    assert.equal(noBefore.status, 2);
    assert.match(noBefore.err, /^recheck needs a parts map for clean, --before-parts clean=<parts\.json>, since vault\.affordance is on the list/);
  }
  const stranger = recheckAffordance({ parts: [`clean=${CLEAN_PARTS}`, `pill=${CLEAN_PARTS}`] });
  assert.equal(stranger.status, 2);
  assert.match(stranger.err, /^--parts names pill, which no --fault names/);
  const extra = recheck();
  assert.equal(extra.status, 0, "a re-check where vault.affordance is off the list needs no --parts");
});
