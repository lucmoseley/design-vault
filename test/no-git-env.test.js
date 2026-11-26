"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");

test("every test file that runs git requires the guard before anything else (#125)", () => {
  const sources = fs.readdirSync(__dirname).filter((name) => name.endsWith(".test.js")).map((name) => [name, fs.readFileSync(path.join(__dirname, name), "utf8")]);
  const runsGit = sources.filter(([, source]) => /\(\s*["']git["']/.test(source));
  const FILES_MOVED_ONTO_THE_HELPER = 5; // measured 5, #125
  assert.ok(runsGit.length >= FILES_MOVED_ONTO_THE_HELPER, `found only ${runsGit.map(([name]) => name).join(", ")}`);
  for (const [name, source] of runsGit) {
    const firstRequire = source.match(/require\(([^)]*)\)/)?.[1];
    assert.equal(firstRequire, '"./no-git-env"', `${name} runs git without requiring ./no-git-env first`);
  }
});
