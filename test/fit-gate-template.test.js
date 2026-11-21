"use strict";
// design-project's client-fit gate template, which a new project copies as its own gate (#159): it must pass gate.js
// check alone and beside the vault gate, every question owned by the project. Break it and every new project's gate
// is refused by the join script before a round can read it.
const assert = require("node:assert/strict");
const { runInProcess } = require("./core-run-in-process.js");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");

const ROOT = path.join(__dirname, "..");
const SCRIPT = path.join(ROOT, "plugin", "skills", "design-round", "scripts", "gate.js");
const FORM = path.join(ROOT, "plugin", "skills", "design-round", "scripts", "gate-form.js");
const VAULT_GATE = path.join(ROOT, "plugin", "skills", "design-critique", "rules");
const TEMPLATE = path.join(ROOT, "plugin", "skills", "design-project", "references", "fit-gate.md");

test("the client-fit gate template passes check, alone and beside the vault's store of rule records", () => {
  for (const files of [[TEMPLATE], [VAULT_GATE, TEMPLATE]]) {
    const r = runInProcess(SCRIPT, ["check", ...files]);
    assert.equal(r.status, 0, r.stdout + r.stderr);
  }
});

test("every question in the client-fit gate template is the project's own, owned by <key>", () => {
  const { parseGate } = require(FORM);
  const { questions } = parseGate(fs.readFileSync(TEMPLATE, "utf8"));
  assert.deepEqual([...new Set(questions.map((q) => q.fields.owner.value))], ["<key>"]);
});

test("the template's colour line is palette.py's measured near-miss test, with the look half yielding to it (#175)", () => {
  const { parseGate } = require(FORM);
  const text = fs.readFileSync(TEMPLATE, "utf8");
  const { questions } = parseGate(text);
  const field = (id, name) => {
    const q = questions.find((x) => x.id === id);
    assert.ok(q, `${id} is in the template`);
    return q.fields[name]?.value;
  };
  assert.equal(field("<key>.colours-script", "answered-by"), "script");
  assert.match(field("<key>.colours-script", "question"), /palette\.py exits 0/);
  assert.match(field("<key>.colours-look", "yields-to"), /^<key>\.colours-script\b/);
  assert.ok(!questions.some((q) => q.id === "<key>.colours"), "the untested look-only colour line is gone");
  assert.match(text, /skills\/design-project\/scripts\/palette\.py/);
});
