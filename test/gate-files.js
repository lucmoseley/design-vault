"use strict";
// Test support for the gate.js suites (#233): gate.js run in-process, and the answers files a test writes or breaks,
// each in a directory of its own under a scratch directory removed once the file's tests end.
// node --test with no arguments also loads this file as a test file of no tests, which is harmless.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const SCRIPT = path.join(__dirname, "..", "plugin", "skills", "design-round", "scripts", "gate.js");

/** gate.js run on `args`: { status, out, err }. */
function runGate(...args) {
  const r = runInProcess(SCRIPT, args);
  return { status: r.status, out: r.stdout, err: r.stderr };
}

/** A scratch directory named from `prefix`, and the helpers that write into it. Call it at a test file's top level. */
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
    /** A file named `name` holding `text` as it is; its path. */
    writeText: (name, text) => fresh("copy", name, text),
    /** A settle critic's answers file holding `answers`; its path. */
    writeSettle: (answers) => fresh("settle", "settle.json", JSON.stringify({ answers })),
    /** A copy of the JSON file `file`, changed by `edit`; its path. */
    buildCopy,
    /** buildCopy() for a copy `edit` breaks. */
    buildBrokenCopy: buildCopy,
  };
}

/** An assertion that gate.js refused the run with a fault matching `pattern`, printing no report headed `heading`. */
const refusedWithout = (heading) => (r, pattern) => {
  assert.equal(r.status, 1, r.out + r.err);
  assert.match(r.out, pattern);
  assert.doesNotMatch(r.out, heading);
};

module.exports = { runGate, gateScratch, refusedWithout };
