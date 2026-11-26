"use strict";
require("./no-git-env");
const assert = require("node:assert/strict");
const { execFileSync, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const ROOT = path.join(__dirname, "..");
const { writeBundle } = require(path.join(ROOT, "bundle.js"));
const read = (file) => fs.readFileSync(path.join(ROOT, file), "utf8");

const scratch = [];
after(() => {
  for (const dir of scratch) fs.rmSync(dir, { recursive: true, force: true });
});

function makeRepo(files) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "bundle-"));
  scratch.push(dir);
  const git = (...args) => execFileSync("git", ["-c", "core.hooksPath=/dev/null", "-c", "user.name=test", "-c", "user.email=test@example.com", ...args], { cwd: dir, encoding: "utf8" });
  git("init", "-q");
  for (const file of files) {
    fs.mkdirSync(path.join(dir, path.dirname(file)), { recursive: true });
    fs.copyFileSync(path.join(ROOT, file), path.join(dir, file));
  }
  fs.mkdirSync(path.join(dir, "data"));
  fs.writeFileSync(path.join(dir, "data", "gallery.json"), '{"entries":[]}\n');
  fs.writeFileSync(path.join(dir, "data", "styles.json"), "[]\n");
  runInProcess(path.join(dir, "bundle.js"), [], { cwd: dir });
  git("add", "data");
  git("commit", "-q", "-m", "seed");
  const stage = (file, text) => {
    fs.writeFileSync(path.join(dir, file), text);
    git("add", file);
  };
  return { dir, git, stage };
}

function bundle(galleryText, stylesText) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "bundle-data-"));
  scratch.push(dir);
  fs.writeFileSync(path.join(dir, "gallery.json"), galleryText);
  fs.writeFileSync(path.join(dir, "styles.json"), stylesText);
  return fs.readFileSync(writeBundle(dir), "utf8");
}

const load = (text) => {
  const window = {};
  new Function("window", text)(window);
  return window.VAULT_DATA;
};

test("the bundle, run as a script, hands the page both files exactly as parsed", () => {
  const data = load(bundle(read("data/gallery.json"), read("data/styles.json")));
  assert.deepEqual(data.gallery, JSON.parse(read("data/gallery.json")));
  assert.deepEqual(data.styles, JSON.parse(read("data/styles.json")));
});

test("a byte-order mark is dropped, and a malformed file is refused by name rather than bundled", () => {
  assert.deepEqual(load(bundle('﻿{"a":1}', "[]")).gallery, { a: 1 });
  assert.throws(() => bundle('{"a":', "[]"), /data\/gallery\.json is not valid JSON/);
  assert.throws(() => bundle("{}", "[,]"), /data\/styles\.json is not valid JSON/);
});

test("the working tree's data/vault-data.js matches its gallery.json and styles.json", () => {
  assert.equal(read("data/vault-data.js"), bundle(read("data/gallery.json"), read("data/styles.json")), "run node bundle.js");
});

test("--staged refuses a commit whose bundle lags its JSON, and passes one that carries both (#32)", () => {
  const repo = makeRepo(["bundle.js", "git-read.js"]);
  const staged = () => runInProcess(path.join(repo.dir, "bundle.js"), ["--staged"], { cwd: repo.dir });
  assert.equal(staged().status, 0);

  repo.stage("data/gallery.json", '{"entries":[1]}\n');
  const stale = staged();
  assert.equal(stale.status, 1);
  assert.match(stale.stderr, /Run node bundle\.js/);

  runInProcess(path.join(repo.dir, "bundle.js"), [], { cwd: repo.dir });
  repo.git("add", "data/vault-data.js");
  assert.equal(staged().status, 0);
});

test("an unknown argument is refused by name", () => {
  for (const args of [["--stage"], ["--staged", "extra"]]) {
    const result = runInProcess(path.join(ROOT, "bundle.js"), args);
    assert.equal(result.status, 2);
    assert.match(result.stderr, new RegExp(`unknown argument "${args.at(-1)}"`));
  }
});

test("pre-commit.local ends the hook on a refusing gate, under plain sh with more of the hook after it", () => {
  const repo = makeRepo(["bundle.js", "validate.js", "git-read.js", ".husky/pre-commit.local"]);
  const hook = () => spawnSync("sh", ["-c", ". ./.husky/pre-commit.local; echo HOOK-WENT-ON"], { cwd: repo.dir, encoding: "utf8" });

  repo.stage("data/styles.json", "[1]\n");
  const stale = hook();
  assert.notEqual(stale.status, 0, "a stale bundle let the hook go on");
  assert.doesNotMatch(stale.stdout, /HOOK-WENT-ON/);
  repo.git("reset", "-q", "--", "data/styles.json");

  repo.stage("data/gallery.json", '{"broken":');
  const malformed = hook();
  assert.notEqual(malformed.status, 0, "a malformed gallery let the hook go on");
  assert.doesNotMatch(malformed.stdout, /HOOK-WENT-ON/);
});

test("each pre-commit.local gate exits with its checker's own code, beside \"ends the hook on a refusing gate\" (#518)", () => {
  const gates = [
    ["validate.js", "data/styles.json"],
    ["bundle.js", "data/vault-data.js"],
    ["round-log.js", "data/round-log.jsonl"],
    ["corrections-log.js", "data/corrections-log.jsonl"],
    ["calibration-log.js", "data/calibration-log.jsonl"],
  ];
  const repo = makeRepo(["bundle.js", "git-read.js", ".husky/pre-commit.local"]);
  for (const [checker] of gates) fs.writeFileSync(path.join(repo.dir, checker), "process.exit(Number(process.env.STUB_EXIT));\n");
  for (const [checker, file] of gates) {
    repo.stage(file, "x\n");
    for (const code of [2, 3]) {
      const result = spawnSync("sh", ["-c", ". ./.husky/pre-commit.local; echo HOOK-WENT-ON"], { cwd: repo.dir, encoding: "utf8", env: { ...process.env, STUB_EXIT: String(code) } });
      assert.equal(result.status, code, `${checker}'s gate did not pass exit ${code} on`);
      assert.doesNotMatch(result.stdout, /HOOK-WENT-ON/);
    }
    repo.git("reset", "-q", "--", file);
  }
});
