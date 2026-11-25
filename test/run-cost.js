"use strict";
// test/run-lanes.sh's call of workflow-core's run-cost report (#370): node test/run-cost.js <tree root> <seconds file>
// It prints the core's lines for that tree, or on any failure one line, and exits 0. node --test with no arguments
// also loads this file as a test file of no tests, which runs nothing as it names no files.
const fs = require("node:fs");
const path = require("node:path");

const [root, seconds] = process.argv.slice(2);
if (root && seconds) {
  try {
    const { resolveCore } = require("../scripts/lib/resolve-core.js");
    const core = resolveCore({ root: path.join(__dirname, "..") });
    const report = require(path.join(core, "scripts", "lib", "run-cost-report.js"));
    const timings = {};
    for (const row of fs.readFileSync(seconds, "utf8").split("\n").filter(Boolean)) {
      const [file, secs] = row.split("\t");
      timings[file] = Number(secs);
    }
    for (const line of report.reportForRun(root, timings)) console.log(line);
  } catch (error) {
    const why = error instanceof Error ? error.message.split("\n")[0] : String(error);
    console.log(`test/run-lanes.sh: workflow-core's run-cost report would not run (${why}), so no test file's cost is judged; the suites' verdict stands (#370).`);
  }
}
