"use strict";
const { execFileSync } = require("child_process");

// guess, #141
const MAX_BUFFER = 256 * 1024 * 1024;

const gitIn = (root) => (...args) => execFileSync("git", args, { cwd: root, encoding: "utf8", maxBuffer: MAX_BUFFER });

module.exports = { gitIn };
