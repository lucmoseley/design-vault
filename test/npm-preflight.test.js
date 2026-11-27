"use strict";
require("./no-git-env");
const assert = require("node:assert/strict");
const { execFileSync, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");

const ROOT = path.join(__dirname, "..");
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "npm-preflight-"));
after(() => fs.rmSync(dir, { recursive: true, force: true }));

const INSTALL = "npm ci --ignore-scripts --prefix plugin";
const LOCK = { lockfileVersion: 3, packages: { "": { dependencies: { parse5: "8.1.1" } }, "node_modules/parse5": { version: "8.1.1" } } };

let vaults = 0;
function vault(plugin) {
  const root = path.join(dir, String(++vaults));
  fs.mkdirSync(path.join(root, "test"), { recursive: true });
  fs.mkdirSync(path.join(root, "scripts", "lib"), { recursive: true });
  fs.copyFileSync(path.join(ROOT, "test", "all.sh"), path.join(root, "test", "all.sh"));
  fs.copyFileSync(path.join(ROOT, "scripts", "lib", "resolve-core.js"), path.join(root, "scripts", "lib", "resolve-core.js"));
  fs.writeFileSync(path.join(root, "test", "run-lanes.sh"), "echo lanes\n");
  fs.writeFileSync(path.join(root, "test", "select-suites.js"), "");
  fs.writeFileSync(path.join(root, "test", "named.test.js"), "");
  if (plugin !== null) {
    fs.mkdirSync(path.join(root, "plugin"));
    fs.writeFileSync(path.join(root, "plugin", "package.json"), JSON.stringify({ private: true, dependencies: { parse5: "8.1.1" } }));
    fs.writeFileSync(path.join(root, "plugin", "package-lock.json"), JSON.stringify(LOCK));
    if (plugin.installed) {
      fs.mkdirSync(path.join(root, "plugin", "node_modules", "parse5"), { recursive: true });
      fs.writeFileSync(path.join(root, "plugin", "node_modules", "parse5", "package.json"), JSON.stringify({ version: plugin.installed }));
    }
  }
  execFileSync("git", ["init", "-q", "-b", "main"], { cwd: root });
  const env = { ...process.env };
  for (const key of ["WFC_GATE_SEAT", "VAULT_SUITE_BUDGET", "VAULT_ALL_SUITES", "VAULT_SUITE_TIMES", "GIT_INDEX_FILE"]) delete env[key];
  return spawnSync("bash", ["test/all.sh", "test/named.test.js"], { cwd: root, encoding: "utf8", env });
}

test("a tree with no plugin/package.json runs its node suites with no npm check", () => {
  const r = vault(null);
  assert.equal(r.status, 0, r.stderr + r.stdout);
  assert.match(r.stdout, /^lanes$/m);
});

for (const [why, plugin] of [
  ["no plugin/node_modules", {}],
  ["a parse5 at another version than the lockfile's", { installed: "8.1.0" }],
]) {
  test(`${why} fails before any suite runs, naming the install`, () => {
    const r = vault(plugin);
    assert.notEqual(r.status, 0, r.stdout);
    assert.doesNotMatch(r.stdout, /^lanes$/m);
    assert.match(r.stderr, new RegExp(`MISSING the plugin's npm packages at plugin/package-lock.json's versions.*install: ${INSTALL}`));
  });
}

test("the lockfile's versions installed pass the check", () => {
  const r = vault({ installed: "8.1.1" });
  assert.equal(r.status, 0, r.stderr + r.stdout);
  assert.match(r.stdout, /^lanes$/m);
});
