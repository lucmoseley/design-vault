"use strict";
const assert = require("node:assert/strict");
const { test } = require("node:test");

test("fails only under the verdict probe (#491)", () => {
  assert.equal(process.env.WFC_VERDICT_PROBE ?? "", "");
});
