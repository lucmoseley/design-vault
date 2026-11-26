"use strict";
require("./no-git-env");
const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");

const ROOT = path.join(__dirname, "..");
const ALL_SH = path.join(ROOT, "test", "all.sh");
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "failed-files-"));
after(() => fs.rmSync(dir, { recursive: true, force: true }));

const env = (extra) => {
  const e = { ...process.env, ...extra };
  delete e.NODE_TEST_CONTEXT;
  for (const own of ["VAULT_FAILED_FILES", "VAULT_FILE_SECONDS"]) if (!(own in extra)) delete e[own];
  return e;
};

const T = 'const { test } = require("node:test");\n';
const TESTS = {
  "red.test.js": `${T}test("red", () => { throw new Error("red"); });\ntest("green", () => {});\n`,
  "green.test.js": `${T}test("green", () => {});\n`,
  "unloadable.test.js": 'throw new Error("at load");\n',
  "nested.test.js": `${T}test("outer", async (t) => { await t.test("inner", () => { throw new Error("inner"); }); });\n`,
  "todo.test.js": `${T}test("not yet", { todo: true }, () => { throw new Error("todo"); });\n`,
};

function scratch(name) {
  const root = path.join(dir, name);
  fs.mkdirSync(path.join(root, "test"), { recursive: true });
  for (const f of ["all.sh", "run-lanes.sh", "failed-files.js"]) fs.copyFileSync(path.join(ROOT, "test", f), path.join(root, "test", f));
  for (const [f, body] of Object.entries(TESTS)) fs.writeFileSync(path.join(root, "test", f), body);
  fs.writeFileSync(path.join(root, "test", "palette.test.py"), "import sys\nsys.exit(1)\n");
  fs.writeFileSync(path.join(root, "test", "cutout.test.py"), "print('cutout ran')\n");
  return root;
}

const QUIET_PS = path.join(dir, "quiet-ps");
fs.writeFileSync(QUIET_PS, "#!/bin/sh\n", { mode: 0o755 });
const AMPLE_MEMINFO = path.join(dir, "meminfo");
// guess #627: past run-lanes' top rung of 4050 MB
fs.writeFileSync(AMPLE_MEMINFO, "MemAvailable:   8192000 kB\n");
// #627
const isolatedEnv = () => env({ VAULT_SUITE_LANES: "1", VAULT_PS: QUIET_PS, VAULT_MEMINFO: AMPLE_MEMINFO,
  WFC_GATE_SEAT: "", VAULT_SUITE_BUDGET: "", VAULT_SUITE_TIMES: "" });

const NODE = spawnSync("bash", [ALL_SH, "--plan"], { encoding: "utf8", env: env({}) }).stdout.match(/^RUN (node .*)$/m)[1];
const plan = (...files) => spawnSync("bash", [ALL_SH, "--plan", ...files], { cwd: ROOT, encoding: "utf8", env: env({}) });

test("a node --test run under the reporter writes each file with a failing test once, from the run's root (#436)", () => {
  const root = scratch("reporter");
  const named = path.join(dir, "reporter.failed");
  const r = spawnSync("bash", ["-c", `${NODE} "$@"`, "node", ...Object.keys(TESTS).map((f) => `test/${f}`)],
    { cwd: root, encoding: "utf8", env: env({ VAULT_FAILED_FILES: named }) });
  assert.equal(r.status, 1, r.stderr);
  assert.deepEqual(fs.readFileSync(named, "utf8").trim().split("\n").sort(),
    ["test/nested.test.js", "test/red.test.js", "test/unloadable.test.js"]);
  assert.match(r.stdout, /✖ red/);
  assert.match(r.stdout, /✔ green/);
});

// guess, #370: a load the real clock shows counted, a floor a slow machine only raises
const LOAD_MS = 400;
test("the reporter writes each file's own wall seconds once, its module load counted, from the run's root (#370)", () => {
  const root = scratch("seconds");
  fs.writeFileSync(path.join(root, "test", "slow-load.test.js"),
    `const start = Date.now(); while (Date.now() - start < ${LOAD_MS});\n${T}test("quick", () => {});\n`);
  const seconds = path.join(dir, "seconds.tsv");
  const files = ["test/slow-load.test.js", "test/green.test.js", "test/red.test.js", "test/unloadable.test.js"];
  const r = spawnSync("bash", ["-c", `${NODE} "$@"`, "node", ...files],
    { cwd: root, encoding: "utf8", env: env({ VAULT_FILE_SECONDS: seconds }) });
  assert.equal(r.status, 1, r.stderr);
  const rows = fs.readFileSync(seconds, "utf8").trim().split("\n").map((l) => l.split("\t"));
  assert.deepEqual(rows.map(([f]) => f).sort(), [...files].sort());
  const took = Object.fromEntries(rows.map(([f, s]) => [f, Number(s)]));
  assert.ok(took["test/slow-load.test.js"] >= LOAD_MS / 1000, `${took["test/slow-load.test.js"]} s`);
});

test("the reporter's seconds are the runner's own duration for the file, never the reporter's clock (#626)", () => {
  const seconds = path.join(dir, "runner.tsv");
  const feed = `const complete = (name, ms) => ({ type: "test:complete",
      data: { file: require("node:path").resolve("test/a.test.js"), name, nesting: 0, details: { duration_ms: ms } } });
    (async () => { for await (const _ of require(${JSON.stringify(path.join(__dirname, "failed-files.js"))})(
      [complete("inner", 1), complete("test/a.test.js", 2), complete("test/a.test.js", 1234)])); })();`;
  const r = spawnSync(process.execPath, ["-e", feed], { cwd: dir, encoding: "utf8", env: env({ VAULT_FILE_SECONDS: seconds }) });
  assert.equal(r.status, 0, r.stderr);
  assert.equal(fs.readFileSync(seconds, "utf8"), "test/a.test.js\t1.234\n");
});

test("without VAULT_FAILED_FILES the reporter still prints Node's report and the run's red", () => {
  const root = scratch("unset");
  const r = spawnSync("bash", ["-c", `${NODE} test/red.test.js`],
    { cwd: root, encoding: "utf8", env: env({}) });
  assert.equal(r.status, 1, r.stderr);
  assert.match(r.stdout, /✖ red/);
});

test("all.sh on named files runs only them, .js ones in one node --test run, and prints FAIL per failing file", () => {
  const root = scratch("named");
  const r = spawnSync("bash", ["test/all.sh", "./test/red.test.js", "test/green.test.js", "test/palette.test.py"],
    { cwd: root, encoding: "utf8", env: isolatedEnv() });
  assert.equal(r.status, 1, r.stdout + r.stderr);
  assert.deepEqual(r.stderr.trim().split("\n").sort(), ["FAIL test/palette.test.py", "FAIL test/red.test.js"]);
  assert.deepEqual(r.stdout.match(/^== .*(?= \(\d+ s\)$)/gm), [
    `== ${NODE} test/red.test.js test/green.test.js`,
    "== python3 test/palette.test.py",
  ]);
  assert.doesNotMatch(r.stdout, /unloadable|cutout ran/);
});

test("all.sh on named files that pass exits 0 and counts the suites it ran", () => {
  const root = scratch("green");
  const r = spawnSync("bash", ["test/all.sh", "test/green.test.js", "test/cutout.test.py"],
    { cwd: root, encoding: "utf8", env: isolatedEnv() });
  assert.equal(r.status, 0, r.stdout + r.stderr);
  assert.match(r.stdout, /cutout ran/);
  assert.match(r.stdout, /^2 named suite\(s\) passed$/m);
});

test("all.sh named a file twice runs it once", () => {
  const r = plan("test/palette.test.py", "./test/palette.test.py", "test/fall.test.js", "./test/fall.test.js");
  assert.equal(r.status, 0, r.stderr);
  assert.equal(r.stdout, `RUN ${NODE} test/fall.test.js\nRUN python3 test/palette.test.py\n`);
});

test("all.sh named a file on disk that no suite lists, a .js file not a test among them, runs nothing for it and passes", () => {
  const r = plan("plugin/skills/design-round/scripts/fall.js", "README.md");
  assert.equal(r.status, 0, r.stderr);
  assert.equal(r.stdout, "SKIP plugin/skills/design-round/scripts/fall.js — no suite lists it\n"
    + "SKIP README.md — no suite lists it\nno named file has a suite to run\n");
});

test("all.sh named a file not on disk runs nothing, exits 2 and says what to name", () => {
  for (const [file, way] of [["test/absent.test.py", "name a .test.js file or a suite file this list runs"],
    ["test/absent.test.js", "name a test file on disk"]]) {
    const r = plan(file);
    assert.equal(r.status, 2, file);
    assert.equal(r.stdout, "");
    assert.equal(r.stderr, `test/all.sh: no ${file} — ${way}\n`);
  }
});
