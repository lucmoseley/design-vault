// Every suite test/all.sh tags `chromium` runs its tests through test/child.py's main(), which runs once more a test
// earlyoom broke (#438).
// A node test, since the gate runs every one on each commit: a commit touching only that suite still meets this.
// full-sweep-only: it reads every suite all.sh tags `chromium`, a list it takes from all.sh at run time.
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");

const ROOT = path.join(__dirname, "..");
// child.test.py's renderers are stand-ins, and it pins main() itself.
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
  test(`${suite} runs its tests through child.main()`, () => {
    const text = fs.readFileSync(path.join(ROOT, suite), "utf8");
    assert.match(text, /\n {4}child\.main\(/);
    assert.doesNotMatch(text, /unittest\.main\(/);
  });
}
