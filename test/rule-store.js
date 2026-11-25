"use strict";
// Test support for the suites that read the vault's store of rule records (#265): where it is, how many records it
// holds, and its records read the way gate.js reads a directory, every .md file in name order.
// node --test with no arguments also loads this file as a test file of no tests, which is harmless.
const fs = require("node:fs");
const path = require("node:path");
const { parseGate } = require("../plugin/skills/design-round/scripts/gate-form.js");

const STORE = path.join(__dirname, "..", "plugin", "skills", "design-critique", "rules");
const RECORD_COUNT = 488;

const storeRecords = () =>
  fs.readdirSync(STORE).filter((n) => n.endsWith(".md")).sort().flatMap((n) => parseGate(fs.readFileSync(path.join(STORE, n), "utf8")).questions);

module.exports = { STORE, RECORD_COUNT, storeRecords };
