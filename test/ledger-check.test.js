"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");
const { plan } = require("./select-suites.js");

const SCRIPT = path.join(__dirname, "..", "ledger-upkeep.js");

const scratch = fs.mkdtempSync(path.join(os.tmpdir(), "ledger-check-"));
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const LIBRARY = path.join(scratch, "gallery.json");
fs.writeFileSync(LIBRARY, JSON.stringify({ projects: { manta: { rules: "docs/brand/brand-sheet.md in lucmoseley/mantahostels" } } }));

function record(id, fields = {}) {
  const all = {
    "applies-when": "web-surface; every button",
    question: "Does it hold?",
    "answered-by": "builder",
    writes: "x",
    "yields-to": "none",
    source: "WCAG 2.2 (2023); strength: WCAG 2.2 AA",
    era: "timeless",
    owner: "vault",
    ledger: "ROW-1",
    ...fields,
  };
  const lines = Object.entries(all).filter(([, v]) => v !== null).map(([k, v]) => `- ${k}: ${v}`);
  return [`### ${id}`, ...lines, ""].join("\n");
}

const ALL_HOLD = { sourced: true, conditioned: true, era_labelled: true, carried: true, disposed: true };
const COVERED = { key: "ROW-1", verdict: "covered", era: "T", criteria: ALL_HOLD, house: ["vault.a"], research: [] };
const GAP = {
  key: "ROW-2", verdict: "gap", era: "T", house: [], research: ["docs/research/notes.md:12"],
  criteria: { sourced: false, conditioned: false, era_labelled: false, carried: false, disposed: false },
  tag: { job: "open-job" }, ruling: { fill: true },
};
const OPEN_JOB = { id: "open-job", rows: 1, tier: 0, rank: 1 };

let written = 0;
function check({ rows = [COVERED], jobs = [OPEN_JOB], store = [record("vault.a")], library = LIBRARY } = {}) {
  const dir = path.join(scratch, `case-${written++}`);
  fs.mkdirSync(path.join(dir, "rules"), { recursive: true });
  fs.writeFileSync(path.join(dir, "rules", "area.md"), `# Rule records: area\n\n${store.join("\n")}`);
  const ledger = {
    meta: { built: "2026-10-15", rescan: { due: "2027-10-15", issue: "#227" }, sources: {} },
    rows: [...rows, GAP],
    jobs,
    method_misses: [],
  };
  fs.writeFileSync(path.join(dir, "ledger.json"), JSON.stringify(ledger));
  return runInProcess(SCRIPT, ["--check", "--ledger", path.join(dir, "ledger.json"), "--store", path.join(dir, "rules"), "--library", library]);
}

function refuses(fixture, message) {
  const result = check(fixture);
  assert.equal(result.status, 1, `expected a refusal matching ${message}; stderr: ${result.stderr}`);
  assert.match(result.stderr, message);
  assert.match(result.stderr, /the fields are docs\/coverage-ledger-method\.md §4 \(verdicts\), §6 \(jobs\)/);
}

function passes(fixture) {
  const result = check(fixture);
  assert.equal(result.status, 0, result.stderr);
}

const DONE_ROW = { ...COVERED, research: ["docs/research/notes.md:40"], tag: { job: "done-job" }, ruling: { fill: true } };
const DONE_JOB = { id: "done-job", rows: 1, tier: 0, rank: 2, done: "#275", destinations: { "docs/research/notes.md:40": "vault.a" } };
const done = (job = {}, rows = [DONE_ROW]) => ({ rows, jobs: [OPEN_JOB, { ...DONE_JOB, ...job }] });

test("a fixture whose rows and done job its records support passes, and an open job's undisposed gap is not refused (#266)", () => {
  passes({});
  passes(done());
});

test("a row whose verdict its criteria do not support is refused, naming the row", () => {
  const partial = { ...COVERED, verdict: "partial", criteria: { ...ALL_HOLD, era_labelled: false } };
  for (const [row, message] of [
    [{ ...COVERED, criteria: { ...ALL_HOLD, conditioned: false } }, /row ROW-1 is covered, but its criteria fail conditioned/],
    [{ ...partial, criteria: ALL_HOLD }, /row ROW-1 is partial, but all five criteria hold/],
    [{ ...partial, criteria: { ...ALL_HOLD, carried: false } }, /row ROW-1 is partial, a carried text answering it, but its criteria say nothing carried does/],
    [{ ...GAP, key: "ROW-3", criteria: { ...GAP.criteria, carried: true }, house: ["vault.a"] }, /row ROW-3 is gap, which nothing carried answers, but its criteria say carried/],
    [{ ...partial, house: [] }, /row ROW-1 is carried, but cites no house text/],
    [{ ...GAP, key: "ROW-3", verdict: "researched", research: [], criteria: { ...GAP.criteria, disposed: true } }, /row ROW-3 is researched, but cites no research line/],
    [{ ...GAP, key: "ROW-3", research: [] }, /row ROW-3 has research left undisposed, but cites no research line/],
    [{ ...COVERED, verdict: "done" }, /row ROW-1 has a verdict that is not one of covered, partial/],
    [{ ...COVERED, criteria: { ...ALL_HOLD, disposed: "yes" } }, /row ROW-1 gives no true or false for disposed/],
  ]) refuses({ rows: [row] }, message);
});

test("a covered row citing a record the store lacks, or a cite that is no record, is refused", () => {
  refuses({ rows: [{ ...COVERED, house: ["vault.a", "vault.gone"] }] }, /row ROW-1 is covered, but cites vault\.gone, which the rule store lacks/);
  refuses({ rows: [{ ...COVERED, house: ["plugin/skills/design-critique/SKILL.md:64"] }] }, /cites plugin\/skills\/design-critique\/SKILL\.md:64, which is no record id: a covered row cites records alone/);
});

test("a covered row whose record is missing its source, conditions or era, or does not list the row, is refused", () => {
  for (const [field, named] of [["source", "source"], ["applies-when", "conditions \\(applies-when\\)"], ["era", "era"]]) {
    refuses({ store: [record("vault.a", { [field]: null })] }, new RegExp(`row ROW-1 is covered, but its record vault\\.a is missing its ${named}`));
  }
  refuses({ store: [record("vault.a", { ledger: "ROW-9" })] }, /row ROW-1 is covered, but its record vault\.a does not list it in its ledger/);
});

test("an era-bound covered row needs a record citing a source from 2023 on", () => {
  const old = record("vault.old", { source: "NN/g 2020, on dark mode, #2024's ruling; strength: domain evidence" });
  const bound = { ...COVERED, era: "E", house: ["vault.old"] };
  refuses({ rows: [bound], store: [old] }, /row ROW-1 is era-bound and covered, but none of its records \(vault\.old\) cites a source from 2023 on/);
  passes({ rows: [{ ...bound, house: ["vault.old", "vault.a"] }], store: [old, record("vault.a")] });
  passes({ rows: [{ ...bound, era: "T" }], store: [old] });
  passes({ rows: [bound], store: [record("vault.old", { source: "Atlassian Elevation (as read Oct 2026); strength: design-system guidance" })] });
  refuses({ rows: [{ ...bound, era: "" }], store: [old] }, /row ROW-1 is covered, but its era is not one of T, E, mixed: ""/);
});

test("a done job with a row neither covered nor accepted with a reason is refused; one accepted with a reason passes", () => {
  const open = { ...GAP, key: "ROW-5", tag: { job: "done-job" }, research: [], criteria: { ...GAP.criteria, disposed: true } };
  const twoRows = (row) => done({ rows: 2 }, [DONE_ROW, row]);
  refuses(twoRows(open), /job done-job is done, but rows ROW-5 are neither covered nor accepted with a reason/);
  refuses(twoRows({ ...open, ruling: { fill: false } }), /rows ROW-5 are neither covered nor accepted/);
  passes(done({}, [DONE_ROW, { ...open, ruling: { fill: false, why: "shop-only; reopens with a shop (#216 Q2 B)" } }]));
});

test("a done job whose rows lost its tag is refused", () => {
  refuses(done({ rows: 3 }), /job done-job is done with 1 of its 3 rows still tagged to it/);
});

test("a done job citing a research line with no destination is refused; each kind of destination passes", () => {
  const at = /job done-job is done, but its research line docs\/research\/notes\.md:40 has /;
  const to = (destination) => done({ destinations: { "docs/research/notes.md:40": destination } });
  refuses(done({ destinations: {} }), new RegExp(`${at.source}no destination`));
  refuses(to("vault.gone"), new RegExp(`${at.source}"vault\\.gone", which is no record in the rule store`));
  refuses(to("shop:docs/brand/brand-sheet.md:12"), new RegExp(`${at.source}"shop:docs/brand/brand-sheet\\.md:12", which is no record in the rule store, no`));
  refuses(to("manta:docs/brand/other.md:12"), new RegExp(`${at.source}.*not a line of manta's rules file, docs/brand/brand-sheet\\.md`));
  refuses(to("not carried: "), new RegExp(`${at.source}a \`not carried: \` with no reason`));
  passes(to("manta:docs/brand/brand-sheet.md:12"));
  passes(to("not carried: the house's dependency order already settles it"));
});

test("a job marked done by anything but an issue number is refused", () => {
  refuses(done({ done: true }), /job done-job is marked done by true, not an issue number like #275/);
});

test("a rule store or library it cannot read is a usage error", () => {
  const result = check({ library: path.join(scratch, "absent.json") });
  assert.equal(result.status, 2);
  assert.match(result.stderr, /cannot read the rule store or the library/);
});

test("a commit staging the ledger, a store file or a research note runs the node suite that holds this check", () => {
  for (const staged of ["docs/coverage-ledger.json", "plugin/skills/design-critique/rules/buttons.md", "docs/research/surface-styling.md"]) {
    const p = plan(["node --test", "python3 test/palette.test.py"], [staged]);
    assert.ok(p.all || p.suites.find((s) => s.suite === "node --test").why === null, staged);
  }
});
