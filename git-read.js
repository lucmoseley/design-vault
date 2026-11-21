"use strict";
/**
 * git-read.js — runs git for the programs that judge a commit from the index or HEAD rather than the working tree
 * (validate.js, bundle.js, log-gate.js), under one cap on what a read may return (#141).
 */
const { execFileSync } = require("child_process");

// Node's default cap, 1 MiB, would refuse the largest read here, bundle.js's `git show` of data/vault-data.js
// (0.37 MB on 14 Oct 2026), once the library grows past it; 256 MiB is a guess at a ceiling no read will near,
// not a measurement.
const MAX_BUFFER = 256 * 1024 * 1024;

/** A runner for git in `root`: its stdout as text; a non-zero exit throws. */
const gitIn = (root) => (...args) => execFileSync("git", args, { cwd: root, encoding: "utf8", maxBuffer: MAX_BUFFER });

module.exports = { gitIn };
