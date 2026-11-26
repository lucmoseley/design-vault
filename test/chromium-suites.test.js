// full-sweep-only: #438
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");

const ROOT = path.join(__dirname, "..");
const EXEMPT = new Set(["test/child.test.py"]);

const listed = fs.readFileSync(path.join(ROOT, "test", "all.sh"), "utf8").match(/^registry='([^']*)'$/m)[1];
const chromium = listed
  .split("\n")
  .map((line) => line.split("\t"))
  .filter(([, needs = ""]) => needs.split(" ").includes("chromium"))
  .map(([suite]) => suite.split(" ").at(-1))
  .filter((suite) => !EXEMPT.has(suite));

test("the registry is read: a suite known to start Chromium is among those tagged", () => {
  assert.ok(chromium.includes("test/check-access.test.py"), chromium.join(", "));
});

for (const suite of chromium) {
  test(`${suite} runs its tests through child.main() (#438)`, () => {
    const text = fs.readFileSync(path.join(ROOT, suite), "utf8");
    assert.match(text, /\n {4}child\.main\(/);
    assert.doesNotMatch(text, /unittest\.main\(/);
  });
}
