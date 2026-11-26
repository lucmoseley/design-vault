"use strict";
const fs = require("node:fs");
const path = require("node:path");
const { resolveCore } = require("../scripts/lib/resolve-core.js");

const script = path.join(resolveCore(), "scripts", "lib", "run-in-process.js");
if (!fs.existsSync(script)) throw new Error(`no ${script}: the resolved workflow-core holds no run-in-process.js; point WORKFLOW_CORE_DIR at a core that has it, or reinstall the pinned plugin`);

const { runInProcess, runInProcessAsync } = require(script);

module.exports = { runInProcess, runInProcessAsync };
