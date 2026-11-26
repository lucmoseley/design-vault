"use strict";
const fs = require("node:fs");
const path = require("node:path");
const { parseGate } = require("../plugin/skills/design-round/scripts/gate-form.js");

const STORE = path.join(__dirname, "..", "plugin", "skills", "design-critique", "rules");
const RECORD_COUNT = 488;

const storeRecords = () =>
  fs.readdirSync(STORE).filter((n) => n.endsWith(".md")).sort().flatMap((n) => parseGate(fs.readFileSync(path.join(STORE, n), "utf8")).questions);

module.exports = { STORE, RECORD_COUNT, storeRecords };
