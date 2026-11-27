#!/usr/bin/env node
/**
 * Usage:
 *   node rule-triggers.js < <PreToolUse payload>    prints each rule in rule-triggers.json once a session per agent,
 *                                                   at its trigger
 *
 * Triggers:
 *   gallery-write  an Edit, Write or MultiEdit of data/gallery.json in the project directory or a worktree under its
 *                  .claude/worktrees/, or a Bash command running ingest.js. The first such call is denied with its
 *                  rules, and a re-send passes.
 *   plugin-land    a Bash `session-checkout.js land` whose commits past origin/main touch plugin/, or a `git commit`
 *                  staging, naming or (with -a) picking up a plugin/ path. Its rule rides the call's result as
 *                  additionalContext.
 * A Bash program matches only in command position, after heredoc bodies are blanked and quoted text made one word.
 *
 * A latch is one file per trigger, created exclusively in workflow-core's markers directory and named
 * .rule-injected-*-<session_id>, so workflow-core's PreCompact clear-rule-latch.sh removes it and a compacted session
 * is told again. A payload with no session_id cannot latch: its rules ride as additionalContext and nothing is denied.
 * Every outcome exits 0, a fault printing nothing.
 */
"use strict";

const fs = require("fs");
const path = require("path");

const RULES = path.join(__dirname, "rule-triggers.json");
const DENY_FIRST = new Set(["gallery-write"]);
const EDIT_TOOLS = new Set(["Edit", "Write", "MultiEdit"]);
const GALLERY = /^(?:\.claude\/worktrees\/[^/]+\/)?data\/gallery\.json$/;

const AT_COMMAND = String.raw`(?:^|[;&|(])\s*(?:(?:env|time|sudo|nice|nohup|command)\s+)*(?:\w+=\S*\s+)*`;
const ARG = String.raw`[^\s;&|()]+\s+`;
const INGEST = new RegExp(String.raw`${AT_COMMAND}(?:node\s+(?:-\S+\s+)*(?:\S*/)?|\S*/)ingest\.js(?=\s|$|[;&|)])`, "m");
const LAND = new RegExp(String.raw`${AT_COMMAND}node\s+(?:${ARG})*?\S*session-checkout\.js\s+land\b`, "m");
const COMMIT = new RegExp(String.raw`${AT_COMMAND}git(?:\s+(?:-[cC]\s+\S+|--?[\w-]+(?:=\S+)?))*\s+commit\b([^;&|\n]*)`, "m");
const ALL_FLAG = /\s(?:-[A-Za-z]*a[A-Za-z]*|--all)(?=\s|$)/;
const PLUGIN_PATH = /(?:^|[\s=]|\.\/)plugin\//;
const HEREDOC = /<<-?\s*(['"]?)(\w+)\1[^\n]*\n[\s\S]*?\n\s*\2[ \t]*(?=\n|$)/g;
const QUOTED = /'[^']*'|"(?:[^"\\]|\\.)*"/g;

function mainCheckout() {
  const dotGit = path.join(__dirname, ".git");
  if (!fs.statSync(dotGit).isFile()) return __dirname;
  const gitdir = /^gitdir:\s*(.+)$/m.exec(fs.readFileSync(dotGit, "utf8"))[1].trim();
  return path.dirname(path.dirname(path.dirname(path.resolve(__dirname, gitdir))));
}

let core;
const coreLib = (name) => {
  core ??= require("./scripts/lib/resolve-core.js").resolveCore({ root: mainCheckout(), warn: () => {} });
  return require(path.join(core, "scripts", "lib", name));
};

function shellWords(command) {
  return command.replace(HEREDOC, "<<").replace(QUOTED, (quoted) => quoted.slice(1, -1).replace(/[\s;&|()]/g, "_"));
}

function isPluginChange(cwd, args) {
  const { HOOK_GIT_TIMEOUT_MS } = coreLib("git.js");
  try {
    const out = require("child_process").execFileSync("git", ["-C", cwd, ...args], { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"], timeout: HOOK_GIT_TIMEOUT_MS });
    return out.split("\n").some((file) => file.startsWith("plugin/"));
  } catch {
    return true;
  }
}

function candidateOf(payload) {
  const tool = payload.tool_name;
  const input = payload.tool_input || {};
  const cwd = payload.cwd || ".";
  if (EDIT_TOOLS.has(tool)) {
    if (typeof input.file_path !== "string") return null;
    const relative = path.relative(process.env.CLAUDE_PROJECT_DIR || cwd, path.resolve(cwd, input.file_path));
    return GALLERY.test(relative.split(path.sep).join("/")) ? { trigger: "gallery-write" } : null;
  }
  if (tool !== "Bash" || typeof input.command !== "string") return null;
  const command = shellWords(input.command);
  if (INGEST.test(command)) return { trigger: "gallery-write" };
  if (LAND.test(command)) return { trigger: "plugin-land", confirm: () => isPluginChange(cwd, ["diff", "--name-only", "origin/main...HEAD"]) };
  const commit = COMMIT.exec(command);
  if (!commit) return null;
  if (PLUGIN_PATH.test(command)) return { trigger: "plugin-land" };
  return { trigger: "plugin-land", confirm: () => isPluginChange(cwd, ["diff", "--name-only", ALL_FLAG.test(commit[1]) ? "HEAD" : "--cached"]) };
}

const safe = (text) => String(text).replace(/[^A-Za-z0-9_-]/g, "_");

function latchPath(trigger, payload) {
  const { markersDir } = coreLib("marker-root.js");
  const { hostRoot } = coreLib("host-root.js");
  const name = `.rule-injected-design-vault-${trigger}-${safe(payload.agent_id ?? "")}-${safe(payload.session_id)}`;
  return path.join(markersDir(hostRoot(payload.cwd || process.cwd())), name);
}

function claim(latch) {
  try {
    fs.closeSync(fs.openSync(latch, "wx"));
    return true;
  } catch (err) {
    if (err.code === "EEXIST") return false;
    throw err;
  }
}

function decide(payload) {
  const candidate = candidateOf(payload);
  if (!candidate) return null;
  const { trigger, confirm } = candidate;
  const hasSession = typeof payload.session_id === "string" && payload.session_id !== "";
  const latch = hasSession ? latchPath(trigger, payload) : null;
  if (latch && fs.existsSync(latch)) return null;
  if (confirm && !confirm()) return null;
  if (latch && !claim(latch)) return null;
  const { rules } = JSON.parse(fs.readFileSync(RULES, "utf8"));
  const text = Object.values(rules)
    .filter((rule) => rule.trigger === trigger)
    .map((rule) => rule.text)
    .join("\n\n");
  if (latch && DENY_FIRST.has(trigger)) {
    return { permissionDecision: "deny", permissionDecisionReason: `${text}\n\nThese bind on this write; re-send the same call once it meets them. Told once a session.` };
  }
  return { additionalContext: text };
}

function main() {
  try {
    const output = decide(JSON.parse(coreLib("read-fd.js").readFdAll(0).toString("utf8")));
    if (output) coreLib("write-fd.js").writeFd(1, JSON.stringify(coreLib("hook-envelope.js").envelope("PreToolUse", output)));
  } finally {
    process.exit(0);
  }
}

if (require.main === module) main();
