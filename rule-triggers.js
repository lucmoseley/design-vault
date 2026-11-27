#!/usr/bin/env node
/**
 * Usage:
 *   node rule-triggers.js < <PreToolUse payload>    prints each rule in rule-triggers.json once a session per agent,
 *                                                   at its trigger
 *
 * Triggers:
 *   gallery-write  an Edit, Write or MultiEdit of data/gallery.json, or a Bash command running ingest.js. A Bash
 *                  program matches only in command position, so prose quoting it mid-line does not fire it. Its rules
 *                  bind before the write, so the first such call is denied with them and a re-send passes.
 *   plugin-land    a Bash `session-checkout.js land`, or a `git commit` staging or naming a plugin/ path. Its rule
 *                  binds after the land, so it rides the call's result as additionalContext.
 *
 * A latch is a file created exclusively in the main checkout's .claude/tmp/markers, named
 * .rule-injected-*-<session_id> so workflow-core's PreCompact clear-rule-latch.sh removes it and a compacted session
 * is told again. A payload with no session_id cannot latch: its rules ride as additionalContext and nothing is denied.
 * Every outcome exits 0, a fault printing nothing, since a rule reminder must never block the call it rides.
 */
"use strict";

const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const RULES = path.join(__dirname, "rule-triggers.json");
const DENY_FIRST = new Set(["gallery-write"]);
const EDIT_TOOLS = new Set(["Edit", "Write", "MultiEdit"]);

const AT_COMMAND = String.raw`(?:^|[;&|(])\s*(?:\w+=\S*\s+)*node\s+`;
const INGEST = new RegExp(String.raw`${AT_COMMAND}(?:\S*/)?ingest\.js(?=\s|$|[;&|)])`, "m");
const LAND = new RegExp(String.raw`${AT_COMMAND}(?:\S+\s+)*?\S*session-checkout\.js\s+land\b`, "m");
const COMMIT = /\bgit\b(?:\s+-[cC]\s+\S+)*\s+commit\b/;
const PLUGIN_PATH = /(?:^|[\s'"=./])plugin\//;

const git = (cwd, ...args) => execFileSync("git", ["-C", cwd, ...args], { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"], timeout: 5000 });

function stagesPlugin(cwd) {
  try {
    return git(cwd, "diff", "--cached", "--name-only").split("\n").some((file) => file.startsWith("plugin/"));
  } catch {
    return false;
  }
}

function triggerOf(payload) {
  const tool = payload.tool_name;
  const input = payload.tool_input || {};
  if (EDIT_TOOLS.has(tool)) {
    const file = typeof input.file_path === "string" ? path.resolve(payload.cwd || ".", input.file_path) : "";
    return file.endsWith(`${path.sep}data${path.sep}gallery.json`) ? "gallery-write" : null;
  }
  if (tool !== "Bash" || typeof input.command !== "string") return null;
  const command = input.command;
  if (INGEST.test(command)) return "gallery-write";
  if (LAND.test(command)) return "plugin-land";
  if (COMMIT.test(command) && (PLUGIN_PATH.test(command) || stagesPlugin(payload.cwd || "."))) return "plugin-land";
  return null;
}

function markersDir(cwd) {
  const common = git(cwd, "rev-parse", "--path-format=absolute", "--git-common-dir").trim();
  const root = path.basename(common) === ".git" ? path.dirname(common) : git(cwd, "rev-parse", "--show-toplevel").trim();
  const dir = path.join(root, ".claude", "tmp", "markers");
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

const safe = (text) => String(text).replace(/[^A-Za-z0-9_-]/g, "_");

function claim(dir, id, payload) {
  const name = `.rule-injected-design-vault-${id}-${safe(payload.agent_id ?? "")}-${safe(payload.session_id)}`;
  try {
    fs.closeSync(fs.openSync(path.join(dir, name), "wx"));
    return true;
  } catch (err) {
    if (err.code === "EEXIST") return false;
    throw err;
  }
}

function decide(payload, readRules) {
  const trigger = triggerOf(payload);
  if (!trigger) return null;
  const rules = readRules();
  const ids = Object.keys(rules).filter((id) => rules[id].trigger === trigger);
  const latched = typeof payload.session_id === "string" && payload.session_id !== "";
  const due = latched ? ids.filter((id) => claim(markersDir(payload.cwd || process.env.CLAUDE_PROJECT_DIR || "."), id, payload)) : ids;
  if (due.length === 0) return null;
  const text = due.map((id) => rules[id].text).join("\n\n");
  if (latched && DENY_FIRST.has(trigger)) {
    return { hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: `${text}\n\nThese bind on this write; re-send the same call once it meets them. Told once a session.` };
  }
  return { hookEventName: "PreToolUse", additionalContext: text };
}

function main() {
  let output = null;
  try {
    output = decide(JSON.parse(fs.readFileSync(0, "utf8")), () => JSON.parse(fs.readFileSync(RULES, "utf8")).rules);
  } catch {
    output = null;
  }
  if (output) process.stdout.write(JSON.stringify({ hookSpecificOutput: output }));
  process.exit(0);
}

if (require.main === module) main();

module.exports = { decide, triggerOf };
