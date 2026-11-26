"use strict";
const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.join(__dirname, "..");

module.exports = function installGate(dir, gate) {
  for (const file of [gate, "log-gate.js", "git-read.js", "plugin/skills/design-round/scripts/gate-form.js"]) {
    fs.mkdirSync(path.dirname(path.join(dir, file)), { recursive: true });
    fs.copyFileSync(path.join(ROOT, file), path.join(dir, file));
  }
};
