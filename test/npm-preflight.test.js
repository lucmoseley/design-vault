"use strict";
require("./no-git-env");
const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { allShEnv, buildScratchVault } = require("./scratch-vault");

const dir = fs.mkdtempSync(path.join(os.tmpdir(), "npm-preflight-"));
after(() => fs.rmSync(dir, { recursive: true, force: true }));

const INSTALL = "npm ci --ignore-scripts --prefix plugin";
const MISSING = new RegExp(`MISSING the plugin's npm packages at plugin/package-lock.json's versions.*install: ${INSTALL}`);
const LOADS = "module.exports = {};";
const lockfile = (extra = {}) => ({
  lockfileVersion: 3,
  packages: { "": { dependencies: { parse5: "8.1.1" } }, "node_modules/parse5": { version: "8.1.1" }, ...extra },
});

let vaults = 0;
function runAllShIn({ lock, parse5 } = {}) {
  const root = buildScratchVault(path.join(dir, String(++vaults)), {
    "run-lanes.sh": "echo lanes\n",
    "select-suites.js": "",
    "named.test.js": "",
  });
  if (lock) {
    fs.mkdirSync(path.join(root, "plugin"));
    fs.writeFileSync(path.join(root, "plugin", "package.json"), JSON.stringify({ private: true, dependencies: { parse5: "8.1.1" } }));
    fs.writeFileSync(path.join(root, "plugin", "package-lock.json"), JSON.stringify(lock));
  }
  if (parse5) {
    const at = path.join(root, "plugin", "node_modules", "parse5");
    fs.mkdirSync(at, { recursive: true });
    fs.writeFileSync(path.join(at, "package.json"), JSON.stringify({ version: parse5.version }));
    fs.writeFileSync(path.join(at, "index.js"), parse5.body);
  }
  return spawnSync("bash", ["test/all.sh", "test/named.test.js"], { cwd: root, encoding: "utf8", env: allShEnv({}) });
}

const passes = (r) => {
  assert.equal(r.status, 0, r.stderr + r.stdout);
  assert.match(r.stdout, /^lanes$/m);
};

test("a tree with no plugin/package.json runs its node suites with no npm check", () => {
  passes(runAllShIn());
});

for (const [why, parse5] of [
  ["no plugin/node_modules", undefined],
  ["a parse5 at another version than the lockfile's", { version: "8.1.0", body: LOADS }],
  ["a parse5 at the lockfile's version that will not load", { version: "8.1.1", body: "throw new Error('truncated');" }],
]) {
  test(`${why} fails before any suite runs, naming the install`, () => {
    const r = runAllShIn({ lock: lockfile(), parse5 });
    assert.notEqual(r.status, 0, r.stdout);
    assert.doesNotMatch(r.stdout, /^lanes$/m);
    assert.match(r.stderr, MISSING);
  });
}

test("the lockfile's versions installed, and loading, pass the check", () => {
  passes(runAllShIn({ lock: lockfile(), parse5: { version: "8.1.1", body: LOADS } }));
});

test("a lockfile entry npm ci never installs here (a link, an optional or a dev package) is not asked for", () => {
  const extra = {
    "node_modules/linked": { resolved: "../linked", link: true },
    "node_modules/other-os": { version: "1.0.0", optional: true },
    "node_modules/tooling": { version: "1.0.0", dev: true },
  };
  passes(runAllShIn({ lock: lockfile(extra), parse5: { version: "8.1.1", body: LOADS } }));
});
