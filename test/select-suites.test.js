"use strict";
// test/select-suites.js and test/all.sh's use of it (#146): a commit runs only the suites its staged files can break.
// Loosen a rule and a change lands with its own tests unrun, or the slow suites run on every commit again.
// And all.sh's --shard=k/n (#462): a suite in no shard is never run by the lander's whole run, one in two runs twice.
require("./no-git-env");
// Every command this file runs gets BY_HAND, so it reads as a run by hand whoever runs the file.
// A caller forcing every suite would select every suite in the commits below too; the one case that wants it sets it (#348).
// Run under workflow-core's gate, it would read as a gate run itself; the one case that wants it sets it (#457).
// The gate hands every command it runs its merge parents, empty where it has none; the cases that want them set them.
const { VAULT_ALL_SUITES, WFC_GATE_SEAT, WFC_MERGE_PARENTS, ...BY_HAND } = process.env;
const assert = require("node:assert/strict");
const { execFileSync, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");

const ROOT = path.join(__dirname, "..");
const { plan, planSides } = require("./select-suites.js");
const SCRIPTS = "plugin/skills/design-round/scripts";

// all.sh's own list, as it prints it run by hand: every suite.
const byHand = spawnSync("bash", [path.join(ROOT, "test", "all.sh"), "--plan"], { encoding: "utf8", env: BY_HAND });
const SUITES = byHand.stdout.split("\n").filter((l) => l.startsWith("RUN ")).map((l) => l.slice(4));
const PYTHON = SUITES.filter((s) => s.startsWith("python3 "));
const NODE = SUITES.find((s) => s.startsWith("node "));
const ran = (staged) => {
  const p = plan(SUITES, staged);
  return p.all ? SUITES : p.suites.filter((s) => !s.why).map((s) => s.suite);
};

// The Python suites that never load check-flow.py.
const NO_FLOW = ["python3 test/cutout.test.py", "python3 test/check-render.test.py", "python3 test/check-clip.test.py", "python3 test/palette.test.py", "python3 test/rule-table.test.py", "python3 test/child.test.py"];

test("the lander's --shard=k/n runs each suite in exactly one shard, every nth of the list from the kth (#462)", () => {
  const shardOf = (k, n) => {
    const r = spawnSync("bash", [path.join(ROOT, "test", "all.sh"), "--plan", `--shard=${k}/${n}`], { encoding: "utf8", env: BY_HAND });
    assert.equal(r.status, 0, r.stderr);
    return r.stdout.split("\n").filter((l) => l.startsWith("RUN ")).map((l) => l.slice(4));
  };
  const n = JSON.parse(fs.readFileSync(path.join(ROOT, ".claude", "workflow-core.json"), "utf8")).fullTestShards;
  const shards = Array.from({ length: n }, (_, i) => shardOf(i + 1, n));
  assert.deepEqual(shards.flat().sort(), [...SUITES].sort());
  shards.forEach((shard, i) => assert.deepEqual(shard, SUITES.filter((_, j) => j % n === i)));
});

test("--shard refuses a shard past its count, a zero, and test files beside it, with exit 2, and takes --plan after it", () => {
  for (const [args, said] of [
    [["--shard=5/4"], /--shard wants k\/n with 1 <= k <= n — got '5\/4'/],
    [["--shard=0/4"], /got '0\/4'/],
    [["--shard=1/x"], /got '1\/x'/],
    [["--shard=1/4", "test/gate.test.js"], /--shard takes no test files/],
  ]) {
    const r = spawnSync("bash", [path.join(ROOT, "test", "all.sh"), "--plan", ...args], { encoding: "utf8", env: BY_HAND });
    assert.equal(r.status, 2, args.join(" "));
    assert.match(r.stderr, said);
  }
  const after = spawnSync("bash", [path.join(ROOT, "test", "all.sh"), "--shard=1/4", "--plan"], { encoding: "utf8", env: BY_HAND });
  assert.equal(after.status, 0, after.stderr);
});

test("run by hand, all.sh runs every suite file git tracks in test/ and skips none", () => {
  assert.equal(byHand.status, 0);
  // Tracked files only, so a suite another session is still writing does not fail this session's commit. A listed
  // suite need only be on disk: the commit that adds one runs this before git tracks it, and no-git-env hides its index.
  const tracked = execFileSync("git", ["ls-files", "test/*.test.py", "test/*.test.sh"], { cwd: ROOT, encoding: "utf8", env: BY_HAND })
    .split("\n").filter((f) => /^test\/[^/]+$/.test(f)).map((f) => `${f.endsWith(".py") ? "python3" : "bash"} ${f}`);
  assert.deepEqual(tracked.filter((s) => !SUITES.includes(s)), [], "a tracked suite all.sh does not list");
  const missing = SUITES.filter((s) => s !== NODE && !fs.existsSync(path.join(ROOT, s.split(" ")[1])));
  assert.deepEqual(missing, [], "a suite all.sh lists that is not on disk");
  assert.doesNotMatch(byHand.stdout, /SKIP/);
});

test("a commit staging only docs/, data/ or images/ files runs the fast checks alone", () => {
  const p = plan(SUITES, ["docs/research/adopt-or-build.md", "data/gallery.json", "images/a.png"]);
  assert.deepEqual(ran(["docs/research/adopt-or-build.md", "data/gallery.json", "images/a.png"]), [NODE, "bash test/design-round-pointer.test.sh"]);
  assert.ok(p.suites.filter((s) => s.why).every((s) => /none of the 3 staged file\(s\) is one it reads/.test(s.why)));
});

test("check-flow.py runs every suite that loads it, as do check-frames.py and check-layout.py; contact-sheet.py runs its own alone", () => {
  const fast = [NODE, "bash test/design-round-pointer.test.sh"];
  assert.deepEqual(ran([`${SCRIPTS}/check-flow.py`]), [...fast, ...PYTHON.filter((s) => !NO_FLOW.includes(s))]);
  assert.deepEqual(ran([`${SCRIPTS}/contact-sheet.py`]), [...fast, "python3 test/contact-sheet.test.py", "python3 test/check-load-files.test.py", "python3 test/check-dom.test.py"]);
  assert.deepEqual(ran([`${SCRIPTS}/check-frames.py`]), [...fast, "python3 test/check-frames.test.py", "python3 test/contact-sheet.test.py", "python3 test/check-load-files.test.py", "python3 test/look-renders.test.py", "python3 test/check-seams.test.py", "python3 test/check-dom.test.py"]);
  assert.deepEqual(ran([`${SCRIPTS}/check-layout.py`]), [...fast, "python3 test/check-flow-records.test.py", "python3 test/check-measure.test.py", "python3 test/face-profile.test.py", "python3 test/contact-sheet.test.py", "python3 test/check-layout.test.py", "python3 test/check-access.test.py", "python3 test/check-access-contrast.test.py", "python3 test/check-access-pointer.test.py", "python3 test/probe.test.py", "python3 test/parts-map.test.py", "python3 test/look.test.py", "python3 test/check-load.test.py", "python3 test/check-load-files.test.py", "python3 test/look-renders.test.py", "python3 test/check-seams.test.py", "python3 test/check-dom.test.py", "python3 test/check-markup.test.py", "python3 test/check-style.test.py", "python3 test/check-state.test.py", "python3 test/check-text.test.py"]);
});

test("a suite runs for its own test file, its fixtures, and a script its test runs", () => {
  assert.ok(ran(["test/cutout.test.py"]).includes("python3 test/cutout.test.py"));
  assert.deepEqual(ran(["test/fixtures/flow/new-page.html"]).filter((s) => PYTHON.includes(s)), ["python3 test/check-flow.test.py", "python3 test/check-flow-records.test.py"]);
  assert.deepEqual(ran([`${SCRIPTS}/fall.js`]).filter((s) => PYTHON.includes(s)), ["python3 test/check-flow.test.py", "python3 test/check-load-files.test.py", "python3 test/check-dom.test.py"]);
});

test("a suite runs for a module beside it that it imports by name, as every Chromium suite does test/child.py (#454)", () => {
  const p = plan(SUITES, ["test/child.py"]);
  assert.equal(p.all, undefined, p.all);
  const chosen = ran(["test/child.py"]);
  for (const suite of ["python3 test/child.test.py", "python3 test/check-access.test.py", "python3 test/check-seams.test.py"]) {
    assert.ok(chosen.includes(suite), suite);
  }
  assert.ok(!chosen.includes("python3 test/cutout.test.py"));
});

test("an unrecognised file under plugin/**/scripts/ or test/, or the runner itself, runs every suite", () => {
  for (const stray of [`${SCRIPTS}/new-checker.py`, "test/load/new-load.py", "test/new.test.py", "test/fixtures/new-dir/a.html",
    "test/all.sh", "test/select-suites.js", "package.json", "package-lock.json"]) {
    const p = plan(SUITES, ["docs/a.md", stray]);
    assert.match(p.all ?? "", new RegExp(`^${stray.replace(/[.*]/g, "\\$&")} is staged`), stray);
  }
});

test("a file only the fast checks read is recognised, so it runs no Python suite", () => {
  for (const file of ["plugin/skills/design-project/scripts/client-originals.py", `${SCRIPTS}/higgsfield.js`, "test/fixtures/validate/x.json"]) {
    assert.equal(plan(SUITES, [file]).all, undefined, file);
  }
});

// all.sh as written, and as an edit to its list alone leaves it (#363).
const ALL_SH = fs.readFileSync(path.join(ROOT, "test", "all.sh"), "utf8");
const relist = (from, to) => {
  assert.equal(ALL_SH.split(from).length, 2, from);
  return ALL_SH.replace(from, to);
};

const FAST = [NODE, "bash test/design-round-pointer.test.sh"];
// What a commit staging contact-sheet.py alone runs.
const SHEET = [...FAST, "python3 test/contact-sheet.test.py", "python3 test/check-load-files.test.py", "python3 test/check-dom.test.py"];
const relisting = (after) => plan(SUITES, ["test/all.sh"], { before: ALL_SH, after });
const runs = (p) => p.suites.filter((s) => !s.why).map((s) => s.suite);

test("a commit editing only all.sh's list runs the fast checks and the suites on the lines it added or changed", () => {
  const added = relist("python3 test/palette.test.py\n", "python3 test/palette.test.py\npython3 test/new.test.py\tchromium\n");
  // A suite all.sh does not list yet is the next all.sh's to run; this one plans only the suites it lists.
  assert.deepEqual(runs(relisting(added)), FAST);
  const needs = relist("python3 test/palette.test.py\n", "python3 test/palette.test.py\timages\n");
  assert.deepEqual(runs(relisting(needs)), [...FAST, "python3 test/palette.test.py"]);
  assert.deepEqual(runs(relisting(relist("python3 test/palette.test.py\n", ""))), FAST);
});

test("an edit to all.sh outside its list, another runner file beside it, or an all.sh HEAD or the commit lacks, runs every suite", () => {
  const needs = relist("python3 test/palette.test.py\n", "python3 test/palette.test.py\timages\n");
  for (const after of [`${needs}# touched\n`, relist("set -u\n", "set -eu\n"), null, ALL_SH.replace(/^registry='/m, "suites='")]) {
    assert.match(relisting(after).all ?? "", /^test\/all\.sh is staged/, String(after).slice(0, 40));
  }
  assert.match(plan(SUITES, ["test/all.sh"], { before: null, after: needs }).all, /^test\/all\.sh is staged/);
  assert.match(plan(SUITES, ["test/all.sh", "package.json"], { before: ALL_SH, after: needs }).all, /^test\/all\.sh is staged/);
});

test("a merge runs a suite only where the plan against every parent runs it, and every suite only where every plan does (#457)", () => {
  const side = (label, staged) => ({ label, staged, before: ALL_SH });
  const flow = `${SCRIPTS}/check-flow.py`;
  const sheet = `${SCRIPTS}/contact-sheet.py`;
  // Main brought the runner and a checker in; the branch changed contact-sheet.py alone.
  const merged = planSides(SUITES, [side("HEAD", ["test/all.sh", flow, "docs/a.md"]), side("abc1234", [sheet])], ALL_SH);
  assert.deepEqual(runs(merged), SHEET);
  assert.match(merged.suites.find((s) => s.suite === "python3 test/check-flow.test.py").why, /^against abc1234, none of the 1 staged file\(s\) is one it reads/);
  // Both sides changed a checker: only the suites that read both run.
  assert.deepEqual(runs(planSides(SUITES, [side("HEAD", [flow]), side("abc1234", [sheet])], ALL_SH)),
    ran([flow]).filter((s) => ran([sheet]).includes(s)));
  assert.match(planSides(SUITES, [side("HEAD", ["package.json"]), side("abc1234", ["package-lock.json", "docs/a.md"])], ALL_SH).all, /^package\.json is staged/);
  // One parent is a commit's plain plan, worded as it always was.
  assert.deepEqual(planSides(SUITES, [side("HEAD", [sheet])], ALL_SH), plan(SUITES, [sheet], { before: ALL_SH, after: ALL_SH }));
});

// A throwaway repo holding the vault's test/ and plugin/, its pre-commit hook writing all.sh's --plan.
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), "select-suites-"));
after(() => fs.rmSync(scratch, { recursive: true, force: true }));
const repo = path.join(scratch, "repo");
for (const dir of ["test", "plugin"]) {
  fs.cpSync(path.join(ROOT, dir), path.join(repo, dir), { recursive: true, filter: (src) => !src.includes("__pycache__") });
}
const hooks = path.join(scratch, "hooks");
const planOut = path.join(scratch, "plan.txt");
fs.mkdirSync(hooks);
fs.writeFileSync(path.join(hooks, "pre-commit"), `#!/bin/sh\nbash test/all.sh --plan >"${planOut}"\n`, { mode: 0o755 });
const git = (args, env = BY_HAND) => execFileSync("git", ["-c", "user.name=test", "-c", "user.email=test@example.com", ...args],
  { cwd: repo, encoding: "utf8", env });
git(["init", "-q", "-b", "main"]);
git(["-c", "core.hooksPath=/dev/null", "add", "-A"]);
git(["-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "base"]);
git(["config", "core.hooksPath", hooks]);
const touch = (rel) => fs.appendFileSync(path.join(repo, rel), "\n# touched\n");
const planRuns = () => fs.readFileSync(planOut, "utf8").split("\n").filter((l) => l.startsWith("RUN ")).map((l) => l.slice(4));

test("a commit through its own index file, as commit-paths.js makes, is judged on that index, not the shared one", () => {
  // The shared index stages check-flow.py; the private one stages contact-sheet.py alone.
  touch(`${SCRIPTS}/check-flow.py`);
  git(["add", `${SCRIPTS}/check-flow.py`]);
  touch(`${SCRIPTS}/contact-sheet.py`);
  const index = path.join(scratch, "private-index");
  const env = { ...BY_HAND, GIT_INDEX_FILE: index };
  git(["read-tree", "HEAD"], env);
  git(["add", `${SCRIPTS}/contact-sheet.py`], env);
  git(["commit", "-q", "-m", "private"], env);
  assert.deepEqual(planRuns(), SHEET);
  assert.match(fs.readFileSync(planOut, "utf8"), /^SKIP python3 test\/check-flow\.test\.py — /m);
});

test("a plain commit is judged on the shared index, and VAULT_ALL_SUITES=1 runs every suite", () => {
  git(["commit", "-q", "-m", "shared"], { ...BY_HAND, VAULT_ALL_SUITES: "1" });
  assert.deepEqual(planRuns(), SUITES);
  touch(`${SCRIPTS}/check-flow.py`);
  git(["add", `${SCRIPTS}/check-flow.py`]);
  git(["commit", "-q", "-m", "shared"]);
  assert.deepEqual(planRuns(), SUITES.filter((s) => !NO_FLOW.includes(s)));
});

test("in workflow-core's gate, which drops GIT_INDEX_FILE and sets WFC_GATE_SEAT, staged files choose; by hand they do not (#457)", () => {
  const planIn = (env) => {
    const r = spawnSync("bash", ["test/all.sh", "--plan"], { cwd: repo, encoding: "utf8", env: { ...BY_HAND, ...env } });
    assert.equal(r.status, 0, r.stderr);
    return { runs: r.stdout.split("\n").filter((l) => l.startsWith("RUN ")).map((l) => l.slice(4)), out: r.stdout };
  };
  // The cases above share this repo's index; one left staged would read as this case's commit.
  assert.equal(git(["diff", "--cached", "--name-only"]), "");
  const gate = { WFC_GATE_SEAT: path.join(scratch, "seat.json") };
  assert.deepEqual(planIn(gate).runs, FAST);
  touch(`${SCRIPTS}/contact-sheet.py`);
  git(["add", `${SCRIPTS}/contact-sheet.py`]);
  try {
    const staged = planIn(gate);
    assert.deepEqual(staged.runs, SHEET);
    assert.match(staged.out, /^SKIP python3 test\/check-flow\.test\.py — /m);
    assert.deepEqual(planIn({}).runs, SUITES);
  } finally {
    git(["commit", "-q", "-m", "contact sheet"]);
  }
});

test("a commit staging the runner runs every suite through all.sh, and so does a selection that fails", () => {
  touch("test/all.sh");
  git(["add", "test/all.sh"]);
  git(["commit", "-q", "-m", "runner"]);
  assert.deepEqual(planRuns(), SUITES);
  assert.match(fs.readFileSync(planOut, "utf8"), /^all suites: test\/all\.sh is staged/m);
  const selector = path.join(repo, "test", "select-suites.js");
  const kept = fs.readFileSync(selector, "utf8");
  fs.writeFileSync(selector, "process.exit(1);\n");
  try {
    fs.writeFileSync(path.join(repo, "notes.md"), "a\n");
    git(["add", "notes.md"]);
    git(["commit", "-q", "-m", "docs"]);
  } finally {
    fs.writeFileSync(selector, kept);
  }
  assert.deepEqual(planRuns(), SUITES);
  assert.match(fs.readFileSync(planOut, "utf8"), /^all suites: test\/select-suites\.js could not choose/m);
});

test("a commit through all.sh editing only its list runs only the suite on the line it changed", () => {
  const sh = path.join(repo, "test", "all.sh");
  const text = fs.readFileSync(sh, "utf8");
  fs.writeFileSync(sh, text.replace("python3 test/palette.test.py\n", "python3 test/palette.test.py\timages\n"));
  const index = path.join(scratch, "list-index");
  const env = { ...BY_HAND, GIT_INDEX_FILE: index };
  git(["read-tree", "HEAD"], env);
  git(["add", "test/all.sh"], env);
  git(["commit", "-q", "-m", "list"], env);
  assert.deepEqual(planRuns(), [...FAST, "python3 test/palette.test.py"]);
});

test("a merge commit through all.sh is judged against MERGE_HEAD, or in the gate against WFC_MERGE_PARENTS (#457)", () => {
  git(["checkout", "-q", "-b", "branch"]);
  touch(`${SCRIPTS}/contact-sheet.py`);
  git(["add", "-A"]);
  git(["commit", "-q", "-m", "branch"], { ...BY_HAND, VAULT_ALL_SUITES: "1" });
  git(["checkout", "-q", "main"]);
  touch("test/all.sh");
  touch(`${SCRIPTS}/check-flow.py`);
  git(["add", "-A"]);
  git(["commit", "-q", "-m", "main"], { ...BY_HAND, VAULT_ALL_SUITES: "1" });
  const main = git(["rev-parse", "main"]).trim();
  git(["checkout", "-q", "branch"]);
  git(["merge", "-q", "--no-commit", "--no-ff", "main"]);
  const planIn = (env) => {
    const r = spawnSync("bash", ["test/all.sh", "--plan"], { cwd: repo, encoding: "utf8", env: { ...BY_HAND, ...env } });
    assert.equal(r.status, 0, r.stderr);
    return { runs: r.stdout.split("\n").filter((l) => l.startsWith("RUN ")).map((l) => l.slice(4)), out: r.stdout };
  };
  const seat = { WFC_GATE_SEAT: path.join(scratch, "seat.json") };
  try {
    // The gate's own worktree has no MERGE_HEAD; the variable stands for it, read first.
    assert.deepEqual(planIn({ ...seat, WFC_MERGE_PARENTS: main }).runs, SHEET);
    assert.deepEqual(planIn({ ...seat, WFC_MERGE_PARENTS: "" }).runs, SUITES);
    const unread = planIn({ ...seat, WFC_MERGE_PARENTS: "unread: no git" });
    assert.deepEqual(unread.runs, SUITES);
    assert.match(unread.out, /^merge parents unread, so judged against HEAD alone: no git$/m);
    const bad = planIn({ ...seat, WFC_MERGE_PARENTS: "f".repeat(40) });
    assert.deepEqual(bad.runs, SUITES);
    assert.match(bad.out, /^merge parent f{40} will not read/m);
    // A hook `git merge` runs before writing MERGE_HEAD sees the merged head as GITHEAD_<sha> alone.
    const mergeHead = path.join(repo, ".git", "MERGE_HEAD");
    const heads = fs.readFileSync(mergeHead, "utf8");
    fs.rmSync(mergeHead);
    try {
      assert.deepEqual(planIn({ GIT_INDEX_FILE: path.join(repo, ".git", "index"), [`GITHEAD_${main}`]: "main" }).runs, SHEET);
      assert.deepEqual(planIn({ GIT_INDEX_FILE: path.join(repo, ".git", "index") }).runs, SUITES);
    } finally {
      fs.writeFileSync(mergeHead, heads);
    }
  } finally {
    git(["commit", "-q", "--no-edit"]);
  }
  assert.deepEqual(planRuns(), SHEET);
  assert.match(fs.readFileSync(planOut, "utf8"), /^SKIP python3 test\/check-flow\.test\.py — against [0-9a-f]{7}, none of /m);
});
