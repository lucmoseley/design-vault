"use strict";
require("./no-git-env");
const assert = require("node:assert/strict");
const { execFileSync, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { resolveCore } = require("../scripts/lib/resolve-core.js");
const { runInProcess } = require("./core-run-in-process.js");

const ROOT = path.join(__dirname, "..");
const SCRIPT = path.join(ROOT, "rule-triggers.js");
const { rules } = JSON.parse(fs.readFileSync(path.join(ROOT, "rule-triggers.json"), "utf8"));
const RELEASE = rules["plugin-release"].text;

const scratch = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "rule-triggers-")));
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const git = (cwd, ...args) => execFileSync("git", ["-c", "core.hooksPath=/dev/null", "-c", "user.name=test", "-c", "user.email=test@example.com", ...args], { cwd, encoding: "utf8" }).trim();
const repo = path.join(scratch, "repo");
fs.mkdirSync(path.join(repo, "plugin"), { recursive: true });
fs.mkdirSync(path.join(repo, "docs"), { recursive: true });
git(repo, "init", "-q", "-b", "main");
fs.writeFileSync(path.join(repo, "README.md"), "x");
fs.writeFileSync(path.join(repo, "plugin", "tracked.md"), "x");
git(repo, "add", "README.md", "plugin/tracked.md");
git(repo, "commit", "-q", "-m", "seed");
git(repo, "update-ref", "refs/remotes/origin/main", "HEAD");
const markers = path.join(repo, ".claude", "tmp", "markers");

let sessions = 0;
const freshSession = () => `s${++sessions}`;

function fire(payload, cwd = repo) {
  const r = runInProcess(SCRIPT, [], { stdin: JSON.stringify({ cwd, ...payload }), cwd, env: { ...process.env, CLAUDE_PROJECT_DIR: cwd } });
  assert.equal(r.status, 0, r.stderr);
  return r.stdout === "" ? null : JSON.parse(r.stdout).hookSpecificOutput;
}

const edit = (session_id, file_path, extra = {}) => fire({ session_id, tool_name: "Edit", tool_input: { file_path }, ...extra });
const bash = (session_id, command, cwd) => fire({ session_id, tool_name: "Bash", tool_input: { command } }, cwd);

test("the first gallery.json edit of a session is denied with both register and note rules, and a re-send passes", () => {
  const sid = freshSession();
  const out = edit(sid, "data/gallery.json");
  assert.equal(out.hookEventName, "PreToolUse");
  assert.equal(out.permissionDecision, "deny");
  assert.ok(out.permissionDecisionReason.includes(rules["two-registers"].text));
  assert.ok(out.permissionDecisionReason.includes(rules["note-intent"].text));
  assert.ok(!out.permissionDecisionReason.includes(RELEASE));
  assert.equal(edit(sid, "data/gallery.json"), null);
});

test("Write and MultiEdit of gallery.json by absolute path trigger too", () => {
  for (const tool_name of ["Write", "MultiEdit"]) {
    const out = fire({ session_id: freshSession(), tool_name, tool_input: { file_path: path.join(repo, "data", "gallery.json") } });
    assert.equal(out.permissionDecision, "deny", tool_name);
  }
});

test("a gallery.json outside the project directory's own data/ is no trigger", () => {
  const sid = freshSession();
  assert.equal(edit(sid, "test/fixtures/lib/data/gallery.json"), null);
  assert.equal(edit(sid, path.join(scratch, "elsewhere", "data", "gallery.json")), null);
});

test("a subagent is told on its own, the main session's latch notwithstanding", () => {
  const sid = freshSession();
  assert.equal(edit(sid, "data/gallery.json").permissionDecision, "deny");
  assert.equal(edit(sid, "data/gallery.json", { agent_id: "a1" }).permissionDecision, "deny");
  assert.equal(edit(sid, "data/gallery.json", { agent_id: "a1" }), null);
});

test("an ingest.js run is the same trigger as a gallery.json edit", () => {
  for (const command of ["node ingest.js --from list.txt", "cd /x && node ./ingest.js", "node /home/u/design-vault/ingest.js", "LIMIT=3 node ingest.js", "env LIMIT=3 node ingest.js", "./ingest.js", 'node "/home/u/my vault/ingest.js"', 'node "$W/ingest.js"']) {
    const sid = freshSession();
    assert.equal(bash(sid, command)?.permissionDecision, "deny", command);
    assert.equal(edit(sid, "data/gallery.json"), null, command);
  }
});

test("a payload off every trigger prints nothing", () => {
  const sid = freshSession();
  assert.equal(edit(sid, "data/gallery.json.bak"), null);
  assert.equal(edit(sid, "docs/gallery.md"), null);
  assert.equal(fire({ session_id: sid, tool_name: "Read", tool_input: { file_path: "data/gallery.json" } }), null);
  for (const command of ["node validate.js", "cat ingest.js", "node ingest.json", "node --test test/ingest.test.js", "node scripts/x.js ingest.js", "git status", "git log -- plugin/", "git commit -m docs"]) assert.equal(bash(sid, command), null, command);
});

test("prose quoting a trigger, in quotes or a heredoc body, prints nothing", () => {
  const sid = freshSession();
  for (const command of [
    'echo "after a node ingest.js run"',
    "printf 'x && node ingest.js'",
    'echo "then node x/session-checkout.js land"',
    "node validate.js; echo 'session-checkout.js land'",
    "echo 'never git commit plugin/ by hand'",
    'rg "git commit" docs/plugin/x',
    "ls node ingest.js",
    "echo then node x/session-checkout.js land",
    "man git commit plugin/x",
    "cat > notes.md <<'EOF'\nnode ingest.js\ngit commit plugin/a.md\nnode session-checkout.js land\nEOF",
  ]) assert.equal(bash(sid, command), null, command);
});

test("session-checkout.js land hands over the release rule as context, once, where its commits touch plugin/", () => {
  const land = "node scripts/lib/resolve-core.js scripts/session-checkout.js land";
  fs.writeFileSync(path.join(repo, "docs", "landed.md"), "a");
  git(repo, "add", "docs/landed.md");
  git(repo, "commit", "-q", "-m", "docs");
  assert.equal(bash(freshSession(), land), null);
  fs.writeFileSync(path.join(repo, "plugin", "landed.md"), "a");
  git(repo, "add", "plugin/landed.md");
  git(repo, "commit", "-q", "-m", "plugin");
  const sid = freshSession();
  const out = bash(sid, land);
  assert.equal(out.permissionDecision, undefined);
  assert.equal(out.additionalContext, RELEASE);
  assert.equal(bash(sid, land), null);
  assert.equal(bash(freshSession(), 'node "/opt/core/scripts/session-checkout.js" land').additionalContext, RELEASE);
  git(repo, "update-ref", "refs/remotes/origin/main", "HEAD");
});

test("a git commit triggers the release rule only where it stages, names or with -a picks up a plugin/ path", () => {
  fs.writeFileSync(path.join(repo, "docs", "a.md"), "a");
  git(repo, "add", "docs/a.md");
  assert.equal(bash(freshSession(), "git commit -m docs"), null);
  fs.writeFileSync(path.join(repo, "plugin", "a.md"), "a");
  git(repo, "add", "plugin/a.md");
  assert.equal(bash(freshSession(), "git commit -m plugin").additionalContext, RELEASE);
  git(repo, "reset", "-q");
  assert.equal(bash(freshSession(), "git add plugin/a.md && git commit -m plugin").additionalContext, RELEASE);
  assert.equal(bash(freshSession(), "git -c core.hooksPath=x commit plugin/a.md -m plugin").additionalContext, RELEASE);
  assert.equal(bash(freshSession(), "git --no-pager commit -m 'x' -- plugin/a.md").additionalContext, RELEASE);
  fs.writeFileSync(path.join(repo, "plugin", "tracked.md"), "changed");
  assert.equal(bash(freshSession(), "git commit -m docs"), null);
  assert.equal(bash(freshSession(), "git commit -am docs").additionalContext, RELEASE);
  assert.equal(bash(freshSession(), "git commit --all -m docs").additionalContext, RELEASE);
  git(repo, "checkout", "-q", "--", "plugin/tracked.md");
});

test("with no session_id nothing is denied and the rules ride as context", () => {
  const out = fire({ tool_name: "Edit", tool_input: { file_path: "data/gallery.json" } });
  assert.equal(out.permissionDecision, undefined);
  assert.ok(out.additionalContext.includes(rules["two-registers"].text));
});

test("a linked worktree latches in the main checkout's markers", () => {
  const tree = path.join(scratch, "tree");
  git(repo, "worktree", "add", "-q", "--detach", tree);
  const sid = freshSession();
  assert.equal(fire({ session_id: sid, tool_name: "Edit", tool_input: { file_path: "data/gallery.json" } }, tree).permissionDecision, "deny");
  assert.ok(fs.readdirSync(markers).some((name) => name.endsWith(`-${sid}`)));
  assert.equal(fs.existsSync(path.join(tree, ".claude")), false);
});

test("workflow-core's PreCompact latch clear tells a compacted session again", () => {
  const sid = freshSession();
  assert.equal(edit(sid, "data/gallery.json").permissionDecision, "deny");
  const clear = spawnSync(path.join(resolveCore(), "scripts", "clear-rule-latch.sh"), [], { input: JSON.stringify({ session_id: sid }), encoding: "utf8", env: { ...process.env, CLAUDE_PROJECT_DIR: repo } });
  assert.equal(clear.status, 0, clear.stderr);
  assert.equal(edit(sid, "data/gallery.json").permissionDecision, "deny");
});

test("an off-trigger call, the common path, loads no repo module and starts no child process", () => {
  const { callCost } = require(path.join(resolveCore(), "scripts", "lib", "call-cost-harness.js"));
  const r = callCost(SCRIPT, [], { stdin: JSON.stringify({ session_id: "pin", cwd: repo, tool_name: "Bash", tool_input: { command: "ls" } }) });
  assert.equal(r.stdout, "");
  assert.deepEqual(r.children, []);
  assert.deepEqual(r.modules.filter((m) => m !== "rule-triggers.js"), []);
});

test("a malformed payload exits 0 printing nothing", () => {
  const r = runInProcess(SCRIPT, [], { stdin: "{" });
  assert.equal(r.status, 0);
  assert.equal(r.stdout, "");
});
