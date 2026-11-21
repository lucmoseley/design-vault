"use strict";
// release-check.js, the session-start count of plugin/ changes the marketplace has not released (#58): run against a
// throwaway four-commit repo and a stand-in gh at WFC_GH, so neither the network nor the real pin is read.
// Loosen one and the count is wrong or missing and a fix sits unreleased; the check must still exit 0, as it reports and never refuses.
require("./no-git-env");
const assert = require("node:assert/strict");
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const ROOT = path.join(__dirname, "..");
const SCRIPT = path.join(ROOT, "release-check.js");

const scratch = fs.mkdtempSync(path.join(os.tmpdir(), "release-check-"));
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const git = (...args) => execFileSync("git", ["-c", "core.hooksPath=/dev/null", "-c", "user.name=test", "-c", "user.email=test@example.com", ...args], { cwd: scratch, encoding: "utf8" }).trim();
git("init", "-q", "-b", "main");
const shas = ["plugin/a", "plugin/b", "docs/c", "plugin/d"].map((file) => {
  fs.mkdirSync(path.join(scratch, path.dirname(file)), { recursive: true });
  fs.writeFileSync(path.join(scratch, file), file);
  git("add", file);
  git("commit", "-q", "-m", file);
  return git("rev-parse", "HEAD");
});

const run = (...args) => runInProcess(SCRIPT, ["--repo", scratch, ...args]);

// Runs the check with no --pin against a stand-in gh that runs `body`.
function runWithGh(body) {
  const bin = fs.mkdtempSync(path.join(scratch, "bin-"));
  fs.writeFileSync(path.join(bin, "gh"), `#!/bin/sh\n${body}\n`, { mode: 0o755 });
  return runInProcess(SCRIPT, ["--repo", scratch], { env: { ...process.env, WFC_GH: path.join(bin, "gh") } });
}

// Runs the check against a stand-in gh answering this marketplace.json.
const runWithMarketplace = (marketplace) => runWithGh(`echo ${Buffer.from(JSON.stringify(marketplace)).toString("base64")}`);

test("a pin on the newest plugin/ commit counts nothing unreleased", () => {
  const result = run("--pin", shas[3]);
  assert.equal(result.status, 0);
  assert.match(result.stdout, /: 0 unreleased plugin\/ commits/);
});

test("a pin moved back counts only the plugin/ commits past it", () => {
  for (const [pin, count] of [[shas[1], 1], [shas[0], 2]]) {
    const result = run("--pin", pin);
    assert.equal(result.status, 0);
    assert.match(result.stdout, new RegExp(`: ${count} unreleased plugin/ commits on main`));
  }
});

test("a pin this checkout does not hold is reported, and the check still exits 0", () => {
  const missing = "0".repeat(40);
  const result = run("--pin", missing);
  assert.equal(result.status, 0);
  assert.match(result.stdout, /pin 0000000 is not in this checkout/);
});


test("a failed pin read names gh's reason, and the check still exits 0", () => {
  const result = runWithGh('echo "gh: Not Found (HTTP 404)" >&2; exit 1');
  assert.equal(result.status, 0);
  assert.match(result.stdout, /could not read the marketplace pin \(gh: Not Found \(HTTP 404\)\)/);
});

test("a marketplace with no design-vault sha is reported, and the check still exits 0", () => {
  for (const marketplace of [{ plugins: [] }, { plugins: [{ name: "other", source: { sha: shas[1] } }] }]) {
    const result = runWithMarketplace(marketplace);
    assert.equal(result.status, 0);
    assert.match(result.stdout, /carries no design-vault sha/);
  }
});

test("the pin read from gh is the design-vault entry's sha, and is the one counted past", () => {
  const marketplace = { plugins: [{ name: "other", source: { sha: shas[0] } }, { name: "design-vault", source: { sha: shas[1] } }] };
  const result = runWithMarketplace(marketplace);
  assert.equal(result.status, 0);
  assert.match(result.stdout, new RegExp(`: 1 unreleased plugin/ commits on main past pin ${shas[1].slice(0, 7)} `));
});

test("a --repo that is not a checkout is reported as uncountable, not as a missing pin", () => {
  const result = runInProcess(SCRIPT, ["--repo", os.tmpdir(), "--pin", shas[0]]);
  assert.equal(result.status, 0);
  assert.match(result.stdout, /could not count past pin .*not a git repository/);
});
