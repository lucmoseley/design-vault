"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const SCRIPT = path.join(__dirname, "..", "plugin", "skills", "design-round", "scripts", "gate.js");

function runGate(...args) {
  const r = runInProcess(SCRIPT, args);
  return { status: r.status, out: r.stdout, err: r.stderr };
}

function gateScratch(prefix) {
  const scratch = fs.mkdtempSync(path.join(os.tmpdir(), prefix));
  after(() => fs.rmSync(scratch, { recursive: true, force: true }));
  const fresh = (kind, name, text) => {
    const out = path.join(fs.mkdtempSync(path.join(scratch, `${kind}-`)), name);
    fs.writeFileSync(out, text);
    return out;
  };
  function buildCopy(file, edit) {
    const data = JSON.parse(fs.readFileSync(file, "utf8"));
    edit(data);
    return fresh("copy", path.basename(file), JSON.stringify(data));
  }
  return {
    writeText: (name, text) => fresh("copy", name, text),
    writeSettle: (answers) => fresh("settle", "settle.json", JSON.stringify({ answers })),
    buildCopy,
    buildBrokenCopy: buildCopy,
  };
}

const refusedWithout = (heading) => (r, pattern) => {
  assert.equal(r.status, 1, r.out + r.err);
  assert.match(r.out, pattern);
  assert.doesNotMatch(r.out, heading);
};

module.exports = { runGate, gateScratch, refusedWithout };
