"use strict";
// Test support: the core's run-in-process.js, which runs one of the vault's node programs inside the test's
// own process, as base §X3 asks of a program test (#187). It lives in the workflow-core plugin, not this repo,
// so it is loaded from the core the repo's resolve-core.js finds, the same lookup the husky hook shims make (#375).
// node --test with no arguments also loads this file as a test file of no tests, which is harmless.
const fs = require("node:fs");
const path = require("node:path");
const { resolveCore } = require("../scripts/lib/resolve-core.js");

const script = path.join(resolveCore(), "scripts", "lib", "run-in-process.js");
if (!fs.existsSync(script)) throw new Error(`no ${script}: the resolved workflow-core holds no run-in-process.js; point WORKFLOW_CORE_DIR at a core that has it, or reinstall the pinned plugin`);

const { runInProcess, runInProcessAsync } = require(script);

module.exports = { runInProcess, runInProcessAsync };
