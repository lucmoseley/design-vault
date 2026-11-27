"use strict";
require("./no-git-env");
const assert = require("node:assert/strict");
const { execFileSync, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");

const ROOT = path.join(__dirname, "..");
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "suite-budget-"));
after(() => fs.rmSync(dir, { recursive: true, force: true }));

const root = path.join(dir, "repo");
fs.mkdirSync(path.join(root, "test"), { recursive: true });
fs.mkdirSync(path.join(root, "scripts", "lib"), { recursive: true });
fs.copyFileSync(path.join(ROOT, "test", "all.sh"), path.join(root, "test", "all.sh"));
fs.copyFileSync(path.join(ROOT, "scripts", "lib", "resolve-core.js"), path.join(root, "scripts", "lib", "resolve-core.js"));
fs.writeFileSync(path.join(root, "test", "run-lanes.sh"), 'echo "budget=${VAULT_SUITE_BUDGET-unset}"\n');
fs.writeFileSync(path.join(root, "test", "select-suites.js"),
  'for (const suite of process.argv.slice(3)) console.log(`skip\\t${suite}\\tstub`);\n');
fs.writeFileSync(path.join(root, "test", "named.test.js"), "");
fs.mkdirSync(path.join(root, "plugin", "node_modules", "parse5"), { recursive: true });
fs.writeFileSync(path.join(root, "plugin", "node_modules", "parse5", "index.js"), "");
const git = (...args) => execFileSync("git", ["-c", "user.name=test", "-c", "user.email=test@example.com", ...args],
  { cwd: root, encoding: "utf8" });
git("init", "-q", "-b", "main");
git("add", "-A");
git("commit", "-q", "-m", "base");

const CEILING_S = 600;
const SPENT_S = 100;
const fakeCore = (name, ceilingMs) => {
  const at = path.join(dir, name);
  fs.mkdirSync(path.join(at, "scripts", "lib"), { recursive: true });
  fs.writeFileSync(path.join(at, "scripts", "lib", "suite-ceiling.js"), `exports.ceilingMs = () => ${ceilingMs};\n`);
  return at;
};
const TEN_MINUTE_CORE = fakeCore("ten-minutes", CEILING_S * 1000);
const THROWING_CORE = fakeCore("throwing", '{ throw new Error("no ceiling"); }');
const HEX_CORE = fakeCore("hex", `"0x${(CEILING_S * 1000).toString(16)}"`);
const SEAT = { WFC_GATE_SEAT: path.join(dir, "seat.json") };
const FALL_OPEN = "the suite ceiling will not read from workflow-core or is already spent, so this run is not judged against it before it starts";

const allSh = (args, env) => {
  const full = { ...process.env, WFC_GATE_SEAT: undefined, VAULT_SUITE_BUDGET: undefined, VAULT_ALL_SUITES: undefined,
    VAULT_SUITE_TIMES: undefined, WORKFLOW_CORE_DIR: TEN_MINUTE_CORE, SECONDS: String(SPENT_S), ...env };
  for (const key of Object.keys(full)) if (full[key] === undefined) delete full[key];
  const r = spawnSync("bash", ["test/all.sh", ...args], { cwd: root, encoding: "utf8", env: full });
  assert.equal(r.status, 0, r.stderr + r.stdout);
  assert.match(r.stdout, /^budget=/m, "all.sh never reached run-lanes");
  return { budget: r.stdout.match(/^budget=(.*)$/m)[1], out: r.stdout };
};
// #499
const assertCeilingLessSpent = (budget) => {
  assert.match(budget, /^[1-9][0-9]*$/);
  assert.ok(Number(budget) <= CEILING_S - SPENT_S, `budget ${budget} is not the ${CEILING_S} s ceiling less the ${SPENT_S} s spent`);
};

test("in a gate seat, all.sh passes run-lanes the core's ceiling less the seconds it has already spent (#499)", () => {
  assertCeilingLessSpent(allSh(["test/named.test.js"], SEAT).budget);
});

test("inside a commit, with no gate seat, all.sh passes the same budget (#499)", () => {
  assertCeilingLessSpent(allSh([], { GIT_INDEX_FILE: path.join(root, ".git", "index") }).budget);
});

test("run by hand, outside a seat or a commit, all.sh passes run-lanes no budget (#499)", () => {
  const { budget, out } = allSh(["test/named.test.js"], {});
  assert.equal(budget, "unset");
  assert.doesNotMatch(out, /suite ceiling/);
});

test("a budget already set is passed through unchanged (#499)", () => {
  assert.equal(allSh(["test/named.test.js"], { ...SEAT, VAULT_SUITE_BUDGET: "42" }).budget, "42");
});

for (const [why, env] of [
  ["a ceiling that will not read", { WORKFLOW_CORE_DIR: THROWING_CORE }],
  ["a ceiling not written in decimal milliseconds, which bash arithmetic would still read", { WORKFLOW_CORE_DIR: HEX_CORE }],
  ["a ceiling already spent", { SECONDS: String(CEILING_S + SPENT_S) }],
]) {
  test(`in a gate seat, ${why} falls open: no budget, and a line saying the run is not judged against it (#499)`, () => {
    const { budget, out } = allSh(["test/named.test.js"], { ...SEAT, ...env });
    assert.equal(budget, "unset");
    assert.match(out, new RegExp(`^${FALL_OPEN}$`, "m"));
  });
}

test("the installed workflow-core's ceilingMs() returns whole milliseconds, as the fake cores do (#499)", (t) => {
  let real;
  try {
    real = require(path.join(ROOT, "scripts", "lib", "resolve-core.js")).resolveCore({ root: ROOT });
  } catch (error) {
    t.skip(`workflow-core does not resolve here: ${error instanceof Error ? error.message : String(error)}`);
    return;
  }
  const ms = require(path.join(real, "scripts", "lib", "suite-ceiling.js")).ceilingMs();
  assert.ok(Number.isSafeInteger(ms) && ms > 0, `ceilingMs() returned ${ms}`);
});
