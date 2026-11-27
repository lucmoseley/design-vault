"use strict";
require("./no-git-env");
const assert = require("node:assert/strict");
const { execFileSync, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { resolveCore } = require("../scripts/lib/resolve-core.js");

const ROOT = path.join(__dirname, "..");
const SCRIPT = path.join(ROOT, "rule-triggers.js");
const { rules } = JSON.parse(fs.readFileSync(path.join(ROOT, "rule-triggers.json"), "utf8"));

const scratch = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "rule-triggers-")));
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const git = (cwd, ...args) => execFileSync("git", ["-c", "core.hooksPath=/dev/null", "-c", "user.name=test", "-c", "user.email=test@example.com", ...args], { cwd, encoding: "utf8" }).trim();
const repo = path.join(scratch, "repo");
fs.mkdirSync(path.join(repo, "plugin"), { recursive: true });
fs.mkdirSync(path.join(repo, "docs"), { recursive: true });
git(repo, "init", "-q", "-b", "main");
fs.writeFileSync(path.join(repo, "README.md"), "x");
git(repo, "add", "README.md");
git(repo, "commit", "-q", "-m", "seed");
const markers = path.join(repo, ".claude", "tmp", "markers");

let sessions = 0;
const freshSession = () => `s${++sessions}`;

function fire(payload, cwd = repo) {
  const result = spawnSync(process.execPath, [SCRIPT], { input: JSON.stringify({ cwd, ...payload }), encoding: "utf8", env: { ...process.env, CLAUDE_PROJECT_DIR: cwd } });
  assert.equal(result.status, 0, result.stderr);
  return result.stdout === "" ? null : JSON.parse(result.stdout).hookSpecificOutput;
}

const edit = (session_id, file_path, extra = {}) => fire({ session_id, tool_name: "Edit", tool_input: { file_path }, ...extra });
const bash = (session_id, command, cwd) => fire({ session_id, tool_name: "Bash", tool_input: { command } }, cwd);

test("the first gallery.json edit of a session is denied with both register and note rules, and a re-send passes", () => {
  const sid = freshSession();
  const out = edit(sid, "data/gallery.json");
  assert.equal(out.permissionDecision, "deny");
  assert.ok(out.permissionDecisionReason.includes(rules["two-registers"].text));
  assert.ok(out.permissionDecisionReason.includes(rules["note-intent"].text));
  assert.ok(!out.permissionDecisionReason.includes(rules["plugin-release"].text));
  assert.equal(edit(sid, "data/gallery.json"), null);
});

test("Write and MultiEdit of gallery.json by absolute path trigger too", () => {
  for (const tool_name of ["Write", "MultiEdit"]) {
    const out = fire({ session_id: freshSession(), tool_name, tool_input: { file_path: path.join(repo, "data", "gallery.json") } });
    assert.equal(out.permissionDecision, "deny", tool_name);
  }
});

test("a subagent is told on its own, the main session's latch notwithstanding", () => {
  const sid = freshSession();
  assert.equal(edit(sid, "data/gallery.json").permissionDecision, "deny");
  assert.equal(edit(sid, "data/gallery.json", { agent_id: "a1" }).permissionDecision, "deny");
  assert.equal(edit(sid, "data/gallery.json", { agent_id: "a1" }), null);
});

test("a node ingest.js run is the same trigger as a gallery.json edit", () => {
  for (const command of ["node ingest.js --from list.txt", "cd /x && node ./ingest.js", "node /home/u/design-vault/ingest.js", "LIMIT=3 node ingest.js"]) {
    const sid = freshSession();
    assert.equal(bash(sid, command).permissionDecision, "deny", command);
    assert.equal(edit(sid, "data/gallery.json"), null, command);
  }
});

test("a payload off every trigger prints nothing", () => {
  const sid = freshSession();
  assert.equal(edit(sid, "data/gallery.json.bak"), null);
  assert.equal(edit(sid, "docs/gallery.md"), null);
  assert.equal(fire({ session_id: sid, tool_name: "Read", tool_input: { file_path: "data/gallery.json" } }), null);
  for (const command of ["node validate.js", "cat ingest.js", "node ingest.json", "git status", "git log -- plugin/", 'echo "after a node ingest.js run"', 'echo "then node x/session-checkout.js land"']) assert.equal(bash(sid, command), null, command);
  assert.equal(bash(sid, "git commit -m 'docs only'"), null);
});

test("session-checkout.js land hands over the release rule as context, once", () => {
  const sid = freshSession();
  const out = bash(sid, "node scripts/lib/resolve-core.js scripts/session-checkout.js land");
  assert.equal(out.permissionDecision, undefined);
  assert.equal(out.additionalContext, rules["plugin-release"].text);
  assert.equal(bash(sid, "node scripts/lib/resolve-core.js scripts/session-checkout.js land"), null);
});

test("a git commit triggers the release rule only where it stages or names a plugin/ path", () => {
  fs.writeFileSync(path.join(repo, "docs", "a.md"), "a");
  git(repo, "add", "docs/a.md");
  assert.equal(bash(freshSession(), "git commit -m docs"), null);
  fs.writeFileSync(path.join(repo, "plugin", "a.md"), "a");
  git(repo, "add", "plugin/a.md");
  assert.equal(bash(freshSession(), "git commit -m plugin").additionalContext, rules["plugin-release"].text);
  git(repo, "reset", "-q");
  assert.equal(bash(freshSession(), "git add plugin/a.md && git commit -m plugin").additionalContext, rules["plugin-release"].text);
  assert.equal(bash(freshSession(), "git -c core.hooksPath=x commit plugin/a.md -m plugin").additionalContext, rules["plugin-release"].text);
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
  assert.equal(edit(sid, "data/gallery.json", { cwd: tree }).permissionDecision, "deny");
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
  const result = spawnSync(process.execPath, [SCRIPT], { input: "{", encoding: "utf8" });
  assert.equal(result.status, 0);
  assert.equal(result.stdout, "");
});
