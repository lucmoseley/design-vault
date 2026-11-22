"use strict";
// This repo's verdict canary (`commands.testCanary`, #491): it passes on every run but workflow-core's verdict
// probe's, where WFC_VERDICT_PROBE=1 makes it fail, so the probe sees `bash test/all.sh` name a red file.
// Make it fail on a normal run and every run goes red; make it pass under the probe and every commit runs the
// whole-suite gate again.
const assert = require("node:assert/strict");
const { test } = require("node:test");

test("fails only under the verdict probe", () => {
  assert.equal(process.env.WFC_VERDICT_PROBE ?? "", "");
});
