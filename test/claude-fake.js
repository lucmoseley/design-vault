#!/usr/bin/env node
"use strict";
const fs = require("node:fs");
const path = require("node:path");

const VERSION = "2.1.299 (Claude Code)";
const COST_USD = 0.01;

const args = process.argv.slice(2);
const value = (flag) => (args.includes(flag) ? args[args.indexOf(flag) + 1] : undefined);
if (args[0] === "--version") {
  console.log(process.env.FAKE_CLAUDE_VERSION ?? VERSION);
  process.exit(0);
}
const format = value("--output-format");
if (format === "stream-json" && !args.includes("--verbose")) {
  console.error("Error: When using --print, --output-format=stream-json requires --verbose");
  process.exit(1);
}
if (format !== "json" && format !== "stream-json") {
  console.error(`claude-fake: --output-format ${format ?? "(none)"} is not spoken; give json or stream-json`);
  process.exit(2);
}
const given = value("-p");
const prompt = given && !given.startsWith("-") ? given : fs.readFileSync(0, "utf8");
const named = Object.fromEntries([...prompt.matchAll(/(?<=^|\s)(\/[^\s]+?)[.,;:)]*(?=\s|$)/g)].map(([, p]) => [p, fs.existsSync(p)]));
const watch = process.env.FAKE_CLAUDE_WATCH;
const log = process.env.FAKE_CLAUDE_LOG;
const calls = log && fs.existsSync(log) ? fs.readFileSync(log, "utf8").split("\n").filter(Boolean).length : 0;
if (log)
  fs.appendFileSync(log, `${JSON.stringify({ args, cwd: process.cwd(), prompt, named, watched: watch && fs.existsSync(watch) ? fs.readFileSync(watch, "utf8") : null })}\n`);

const replies = JSON.parse(fs.readFileSync(process.env.FAKE_CLAUDE_REPLIES, "utf8"));
if (!replies.length) {
  console.error(`claude-fake: ${process.env.FAKE_CLAUDE_REPLIES} holds no reply for call ${calls + 1}`);
  process.exit(2);
}
const reply = replies[calls] ?? replies.at(-1);
const model = value("--model") ?? "sonnet";
const emit = (event) => process.stdout.write(`${JSON.stringify(event)}\n`);
const stream = format === "stream-json";

function answer(result, structured) {
  emit({
    type: "result", subtype: "success", is_error: false, num_turns: 1, result, total_cost_usd: COST_USD,
    usage: { input_tokens: 1, cache_creation_input_tokens: 0, cache_read_input_tokens: 0, output_tokens: 1 },
    modelUsage: { [model.startsWith("claude-") ? model : `claude-${model}-9`]: { costUSD: COST_USD } },
    ...(structured === undefined ? {} : { structured_output: structured }),
  });
}

if (reply.kill) process.kill(process.ppid, "SIGKILL");
else if (reply.fail) {
  process.stderr.write(`${reply.fail}\n`);
  process.exitCode = 1;
} else {
  if (stream) emit({ type: "system", subtype: "init", cwd: process.cwd(), model });
  if (reply.hang) setTimeout(() => {}, reply.hang * 1000);
  else if (reply.reads) {
    const mode = reply.reads;
    const dirs = [process.cwd(), ...(value("--add-dir") && mode !== "no-add-dir" ? [value("--add-dir")] : [])];
    const readable = (file) => mode === "leak" || (mode !== "blind" && dirs.some((d) => path.resolve(file).startsWith(d + path.sep)));
    let said = "";
    for (const file of [path.join(process.cwd(), "control.md"), ...Object.keys(named).filter((p) => p.endsWith(".md"))]) {
      const text = readable(file) && fs.existsSync(file) ? fs.readFileSync(file, "utf8") : null;
      if (text !== null && stream) emit({ type: "user", message: { role: "user", content: [{ type: "tool_result", tool_use_id: `toolu_${said.length}`, content: text }] } });
      said += `${file}: ${text ?? "permission denied\n"}`;
    }
    answer(said);
  } else if ("structured" in reply) answer(JSON.stringify(reply.structured), reply.structured);
  else answer(reply.text);
}
