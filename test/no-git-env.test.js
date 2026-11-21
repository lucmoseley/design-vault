"use strict";
// test/no-git-env.js, the GIT_* guard every git-running test file requires first (#125): read off each test file's text.
// Loosen it and a new test that runs git without the guard can turn the shared vault repo bare when a worktree's hook runs it.
// A file that runs git only through a script it spawns, never through an execFileSync or spawnSync of git, passes unseen.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");

test("every test file that runs git requires the guard before anything else", () => {
  const sources = fs.readdirSync(__dirname).filter((name) => name.endsWith(".test.js")).map((name) => [name, fs.readFileSync(path.join(__dirname, name), "utf8")]);
  const runsGit = sources.filter(([, source]) => /\(\s*["']git["']/.test(source));
  // The five files #125 moved onto the helper, so a detector that finds none fails rather than passes.
  assert.ok(runsGit.length >= 5, `found only ${runsGit.map(([name]) => name).join(", ")}`);
  for (const [name, source] of runsGit) {
    const firstRequire = source.match(/require\(([^)]*)\)/)?.[1];
    assert.equal(firstRequire, '"./no-git-env"', `${name} runs git without requiring ./no-git-env first`);
  }
});
