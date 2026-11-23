"use strict";
// gate.js check, which refuses a gate file that breaks the form (#157) and a vault rule record that breaks the record
// form (#265): driven through its CLI on one fixture per refusal, each a clean question with one thing broken.
// Loosen one and a question no join can read, or one no critic knows the answerer of, reaches a round's list.
const assert = require("node:assert/strict");
const { runInProcess } = require("./core-run-in-process.js");
const path = require("node:path");
const { test } = require("node:test");

const ROOT = path.join(__dirname, "..");
const SCRIPT = path.join(ROOT, "plugin", "skills", "design-round", "scripts", "gate.js");
const FORM = path.join(ROOT, "plugin", "skills", "design-round", "scripts", "gate-form.js");
const { STORE: VAULT_GATE, RECORD_COUNT, storeRecords } = require("./rule-store.js");
const FIXTURES = path.join(__dirname, "fixtures", "gate");

const check = (...files) => {
  const r = runInProcess(SCRIPT, ["check", ...files.map((f) => (path.isAbsolute(f) ? f : path.join(FIXTURES, f)))]);
  return { status: r.status, out: r.stdout, err: r.stderr };
};

test("the vault's store of rule records passes", () => {
  const { status, out } = check(VAULT_GATE);
  assert.equal(status, 0, out);
  assert.match(out, /pass/);
});

// The records #272 split from the references keep the answerer the house gave them, the builder or the whole-page
// critic, so none joins a gate list and no critic's load moves until #258 re-sorts them. A staged record reaches no
// agent until its tier's load test, so only live ones are held to this.
// A tier made live (#292, #293) adds its gate questions to the map below and its type records to `typed`.
test("a live record outside the pinned gate map and the pinned type-critic list that is not the builder's or the whole-page critic's fails, and so does a pinned record gone missing or moved to another answerer", () => {
  const records = storeRecords().filter((q) => q.fields.status.value === "live").map((q) => [q.id, q.fields["answered-by"].value]);
  const others = records.filter(([, a]) => !["script", "code", "look"].includes(a));
  assert.deepEqual(others.filter(([, a]) => !["builder", "whole-page", "type"].includes(a)), []);
  // The type critic's records (#268): the ones #224's type critic judged, out of the whole-page critic's load.
  // Tier 0's (#292) join them.
  const typed = [
    "vault.heading-step", "vault.paragraph-break", "vault.no-justify", "vault.dna-caps-label", "vault.dark-text-weight", "vault.measure", "vault.body-size", "vault.leading",
    "vault.dashes", "vault.prose-emphasis", "vault.emphasis-cues", "vault.zero-distinct", "vault.face-roles",
  ];
  assert.deepEqual(others.filter(([, a]) => a === "type").map(([id]) => id).sort(), typed.sort());
  assert.deepEqual(Object.fromEntries(records.filter((r) => !others.includes(r))), {
    "vault.curves-script": "script",
    "vault.curves-look": "look",
    "vault.contacts-code": "code",
    "vault.contacts-script": "script",
    "vault.contacts-seam": "script",
    "vault.contacts-look": "look",
    "vault.flow-script": "script",
    "vault.flow-code": "code",
    "vault.fall-script": "script",
    "vault.flow-look": "look",
    "vault.length-range": "code",
    "vault.length": "script",
    "vault.clip-loop": "script",
    "vault.drafts-kept": "script",
    "vault.end-frame": "script",
    "vault.render-size": "script",
    "vault.render-checkerboard": "script",
    "vault.logo-unchanged": "script",
    "vault.logo-ground-script": "script",
    "vault.baked-ui-look": "look",
    "vault.headline-plain-look": "look",
    "vault.reflow": "script",
    "vault.layout": "script",
    "vault.focal-crop": "script",
    "vault.one-site": "script",
    "vault.load": "script",
    "vault.affordance": "look",
    "vault.borrowing": "look",
    "vault.primary-action": "look",
    "vault.one-target": "script",
    "vault.high-stakes": "look",
    "vault.contrast": "script",
    "vault.control-edges": "script",
    "vault.target-size": "script",
    "vault.colour-script": "script",
    "vault.colour-look": "look",
    "vault.render-palette-look": "look",
    "vault.keyboard": "script",
    "vault.focus": "script",
    "vault.pause": "script",
    "vault.icon-optical-size": "script",
    "vault.proof": "code",
    "vault.consistent-help": "code",
    "vault.live-region-ready": "script",
    "vault.validation-timing": "script",
    "vault.on-input": "script",
    "vault.slider-direction": "script",
    "vault.media-alternatives": "code",
    "vault.content-image": "code",
    "vault.key-shortcuts": "script",
    "vault.hover-reveal": "script",
    "vault.hover-content": "script",
    "vault.native-scroll": "script",
    "vault.drag-release": "script",
    "vault.drag-release-spring-look": "look",
    "vault.dialog-default": "script",
    "vault.dialog-default-look": "look",
    "vault.menu-click": "script",
    "vault.submenu-close": "script",
    "vault.interruptions": "script",
    "vault.cookie-banner": "script",
    "vault.cookies-page": "code",
    "vault.figure-face": "script",
    "vault.font-features": "script",
    "vault.glyph-distinct": "script",
    "vault.small-caps": "script",
    "vault.type-axes": "script",
    "vault.ring-outline": "script",
    // The computed-style records check-style.py answers, and the look halves split from them (#309).
    "vault.forced-colour-edges": "script",
    "vault.action-colour": "script",
    "vault.axis-properties": "script",
    "vault.border-shadow": "script",
    "vault.calm-colour-share": "script",
    "vault.caret-shape": "script",
    "vault.dark-raise": "script",
    "vault.edit-wrap": "script",
    "vault.emphasis-cue": "script",
    "vault.emphasis-form": "script",
    "vault.face-count": "script",
    "vault.fallback-metrics": "script",
    "vault.font-smoothing": "script",
    "vault.font-stack": "script",
    "vault.heading-fill": "script",
    "vault.hyphen-char": "script",
    "vault.image-scaling": "script",
    "vault.kept-breaks": "look",
    "vault.kerning": "script",
    "vault.key-action": "script",
    "vault.pixel-image-kind": "look",
    "vault.rtl-sides": "script",
    "vault.ruby-position": "script",
    "vault.shadow-meaning": "look",
    "vault.skip-ink": "script",
    "vault.spacing-step": "script",
    "vault.spelling-mark": "script",
    "vault.surface-shadow": "script",
    "vault.table-print-header": "script",
    "vault.tag-shape": "script",
    "vault.text-stroke": "script",
    "vault.true-faces": "script",
    "vault.white-space": "script",
    "vault.border-width": "script",
    "vault.edge-alpha": "script",
    "vault.gradient-kind": "script",
    "vault.gradient-space": "script",
    "vault.image-edge": "script",
    "vault.justify-space": "script",
    "vault.measure-unit": "script",
    "vault.name-case": "script",
    // #311's live records check-layout.py --records answers.
    "vault.joined-fills": "script",
    "vault.safe-centre": "script",
    "vault.dash-glyphs": "script",
    "vault.emphasis-share": "script",
    "vault.fractions": "script",
    "vault.rtl-digit-order": "script",
    "vault.sentence-space": "script",
    "vault.week-hour": "script",
    // The driven-state records check-state.py answers (#312).
    "vault.space-plays": "script",
    "vault.pinch-anchor": "script",
    "vault.drag-tracking": "script",
    "vault.scroller-input": "script",
  });
});

test("each record gives its stage and names its script exactly where a script answers it, a script owed only on a staged record", () => {
  const records = storeRecords();
  assert.equal(records.length, RECORD_COUNT);
  for (const q of records) {
    const f = (name) => q.fields[name]?.value;
    assert.ok(["live", "staged"].includes(f("status")), q.id);
    assert.ok(["function", "role", "treatment", "value"].includes(f("stage")), q.id);
    assert.equal(Boolean(f("script")), f("answered-by") === "script", q.id);
    if (f("status") === "live") assert.notEqual(f("script"), "owed", q.id);
  }
});

test("a clean gate file passes: and- and or-joined conditions, a dated era, an id and a level yielded to, and none", () => {
  const { status, out } = check("clean.md");
  assert.equal(status, 0, out);
  assert.match(out, /^3 gate question\(s\) in 1 file\(s\) pass$/m);
});

const refusals = [
  ["missing-field.md", /:2: demo\.no-writes is missing its writes$/m],
  ["bad-answered-by.md", /:5: demo\.critic is answered by critic, not one of script, code, look, whole-page, type, builder$/m],
  ["bad-era.md", /:9: demo\.era has an era that is neither `timeless` nor `dated <YYYY-MM-DD>`: E \(2026\)$/m],
  ["bad-date.md", /:9: demo\.date has an era .*: dated 2026-02-30$/m],
  ["duplicate-id.md", /:12: demo\.twice is already the id of a question at .*duplicate-id\.md:2$/m],
  ["unresolved-yields-to.md", /:7: demo\.yields yields to demo\.absent, which is no question id/m],
  ["bad-level.md", /:7: demo\.level yields to level 7, which is no question id in the files given and no precedence level \(level 1 to level 6\)$/m],
  ["bad-applies-when.md", /:3: demo\.still names an asset condition outside the vocabulary: still-image /m],
  ["wrong-owner.md", /:2: other\.owner is not prefixed by its owner, `demo\.`$/m],
  ["no-strength.md", /:8: demo\.source gives its source no `; strength: `$/m],
  ["stray-line.md", /:11: demo\.prose holds a line that is not a `- <field>: <value>` field$/m],
  ["repeated-field.md", /:11: demo\.twice-field gives writes twice$/m],
  ["unknown-field.md", /:11: demo\.extra has a field the form does not: id /m],
  ["mixed-joiners.md", /:3: demo\.mixed joins its asset condition with both `and` and `or`/m],
  ["no-part-condition.md", /:3: demo\.no-part gives no part condition/m],
  ["no-question.md", /:1: holds no gate question/m],
  ["record-missing-stage.md", /:1: vault\.no-stage is a vault rule record missing its stage$/m],
  ["record-no-script.md", /:1: vault\.no-script is answered by script but names no script/m],
  ["record-bad-stage.md", /:10: vault\.bad-stage has a stage that is not one of function, role, treatment, value: polish$/m],
  ["record-bad-status.md", /:14: vault\.bad-status has a status that is not one of live, staged: draft$/m],
  ["record-owed-look.md", /:15: vault\.owed-look gives `script: owed` but is answered by look: only a record answered by script names one$/m],
  ["record-no-target.md", /:1: vault\.no-target is loaded by the builder \(stage function\) but gives no target$/m],
  ["record-builder-no-target.md", /:1: vault\.builder-no-target is loaded by the builder \(answered by builder\) but gives no target$/m],
  ["record-inputs-alone.md", /:12: vault\.inputs-alone gives inputs with no output/m],
  ["record-bad-ledger.md", /:13: vault\.bad-ledger names a ledger entry that is no row key \(or `none`\): forms$/m],
  ["project-stage-no-target.md", /:1: demo\.staged is loaded by the builder \(stage role\) but gives no target$/m],
];
for (const [fixture, why] of refusals) {
  test(`check refuses ${fixture} with exit 1, naming the line and the fault, and nothing else`, () => {
    const { status, out } = check(fixture);
    assert.equal(status, 1, out);
    assert.match(out, why);
    assert.equal(out.trim().split("\n").length, 1, out);
  });
}

test("clean rule records pass: every answerer and stage, a staged record, a script owed, and inputs with their output", () => {
  const { status, out } = check("record-clean.md");
  assert.equal(status, 0, out);
  assert.match(out, /^6 gate question\(s\) in 1 file\(s\) pass$/m);
});

test("a project's questions with the eight fields alone pass beside the store, the client-fit template's among them", () => {
  const template = path.join(ROOT, "plugin", "skills", "design-project", "references", "fit-gate.md");
  const { status, out } = check("clean.md", template, VAULT_GATE);
  assert.equal(status, 0, out);
});

test("each of the six precedence levels resolves, and level 0 does not", () => {
  const { checkGates } = require(FORM);
  const text = require("node:fs").readFileSync(path.join(FIXTURES, "bad-level.md"), "utf8");
  for (let n = 0; n <= 7; n++) {
    const { faults } = checkGates([{ file: "g.md", text: text.replace("level 7", `level ${n}`) }]);
    assert.equal(faults.length, n >= 1 && n <= 6 ? 0 : 1, `level ${n}`);
  }
});

test("a project gate yielding to a vault question passes beside the vault gate, and is refused alone", () => {
  assert.equal(check("yields-to-vault.md", VAULT_GATE).status, 0);
  const alone = check("yields-to-vault.md");
  assert.equal(alone.status, 1);
  assert.match(alone.out, /yields to vault\.layout, which is no question id in the files given/);
});

test("a fault in a later file given is refused too", () => {
  const { status, out } = check(VAULT_GATE, "missing-field.md");
  assert.equal(status, 1);
  assert.match(out, /missing-field\.md:2: demo\.no-writes is missing its writes/);
});

test("an id one file repeats from another is refused", () => {
  const { status, out } = check("clean.md", "clean.md");
  assert.equal(status, 1);
  assert.match(out, /demo\.cta-script is already the id of a question at .*clean\.md:7/);
});

test("bad usage and an unreadable file exit 2, saying why on stderr", () => {
  for (const args of [[], ["lint", path.join(FIXTURES, "clean.md")]]) {
    const r = runInProcess(SCRIPT, args);
    assert.equal(r.status, 2);
    assert.match(r.stderr, /^usage: node gate\.js check /);
  }
  const absent = check("absent.md");
  assert.equal(absent.status, 2);
  assert.match(absent.err, /absent\.md: ENOENT/);
  const fs = require("node:fs");
  const bare = fs.mkdtempSync(path.join(require("node:os").tmpdir(), "gate-empty-"));
  try {
    const empty = check(bare);
    assert.equal(empty.status, 2);
    assert.match(empty.err, /gate-empty-\w+: a directory holding no \.md gate file/);
  } finally {
    fs.rmSync(bare, { recursive: true, force: true });
  }
});
