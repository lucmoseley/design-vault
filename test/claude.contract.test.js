"use strict";
const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");

const FAKE = path.join(__dirname, "claude-fake.js");
const JSON_RECORDED = path.join(__dirname, "fixtures", "claude", "json-schema.json");
const STREAM_RECORDED = path.join(__dirname, "fixtures", "claude", "stream-json.jsonl");
const RECORD = "CLAUDE_RECORD=1 node --test test/claude.contract.test.js";
const installed = !spawnSync("claude", ["--version"], { encoding: "utf8" }).error;
const live = process.env.CI ? "claude's live cases run on the founder's machine, never in CI (code-standards base §G7 item 2)"
  : !installed && "no claude is installed, so there is no real binary to hold the fake to";
const record = !process.env.CLAUDE_RECORD && `a recording spends haiku tokens, so it runs only under ${RECORD}`;
// guess #664
const LIVE_TIMEOUT_MS = 120000;
// guess #664
const MAX_TURNS = "4";
const SCHEMA = JSON.stringify({ type: "object", properties: { answer: { type: "string" } }, required: ["answer"] });
const BARE = ["--model", "haiku", "--no-session-persistence", "--tools", "", "--max-turns", MAX_TURNS];
const JSON_CALL = { args: ["-p", "Give the word OK as the answer field.", "--output-format", "json", "--json-schema", SCHEMA, ...BARE], reply: { structured: { answer: "OK" } } };
const STREAM_CALL = { args: ["--print", "--output-format", "stream-json", "--verbose", ...BARE], input: "Reply with the single word OK.", reply: { text: "OK" } };
const TYPE = "type";
const RESULT_READ = {
  type: TYPE, subtype: TYPE, is_error: TYPE, result: TYPE, structured_output: "skeleton", total_cost_usd: TYPE, num_turns: TYPE, modelUsage: TYPE,
  usage: { input_tokens: TYPE, output_tokens: TYPE, cache_read_input_tokens: TYPE, cache_creation_input_tokens: TYPE },
};

const dir = fs.mkdtempSync(path.join(os.tmpdir(), "claude-contract-"));
after(() => fs.rmSync(dir, { recursive: true, force: true }));

function call(bin, { args, input, reply = { text: "OK" } }) {
  const replies = path.join(dir, "replies.json");
  fs.writeFileSync(replies, JSON.stringify([reply]));
  return spawnSync(bin, args, { cwd: dir, input: input ?? "", encoding: "utf8", timeout: LIVE_TIMEOUT_MS, env: { ...process.env, FAKE_CLAUDE_REPLIES: replies } });
}
function skeleton(v, key) {
  if (key === "type" || key === "subtype") return v;
  if (v === null) return "null";
  if (Array.isArray(v)) return v.length ? [skeleton(v[0])] : [];
  if (typeof v === "object") return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, skeleton(x, k)]));
  return typeof v;
}
const typeOf = (s) => (Array.isArray(s) ? "array" : s && typeof s === "object" ? "object" : s);
function read(s, spec) {
  return Object.fromEntries(Object.entries(spec).map(([k, how]) => [k,
    s?.[k] === undefined ? "absent" : how === "skeleton" ? s[k] : typeof how === "object" ? read(s[k], how) : k === "type" ? s[k] : typeOf(s[k])]));
}
const events = (stdout) => stdout.trim().split("\n").map((line) => skeleton(JSON.parse(line)));
const recorded = (file) => fs.readFileSync(file, "utf8").trim().split("\n").map((line) => JSON.parse(line));
const usedModels = (s) => Object.keys(s.modelUsage).map((m) => m.startsWith("claude-haiku"));
const stale = `the recording may be stale: ${RECORD}`;

test("the real claude's json and stream-json answers are recorded as their shapes", { skip: live || record }, () => {
  for (const [file, spec] of [[JSON_RECORDED, JSON_CALL], [STREAM_RECORDED, STREAM_CALL]]) {
    const r = call("claude", spec);
    assert.equal(r.status, 0, r.stderr);
    fs.writeFileSync(file, `${events(r.stdout).map((e) => JSON.stringify(e)).join("\n")}\n`);
  }
});

test("--version prints one version line of the same shape", { skip: live }, () => {
  for (const bin of ["claude", FAKE]) {
    const r = call(bin, { args: ["--version"] });
    assert.equal(r.status, 0, r.stderr);
    assert.match(r.stdout, /^\d+\.\d+\.\d+ \(Claude Code\)\n$/);
  }
});

test("stream-json under --print without --verbose is refused, naming --verbose", { skip: live }, () => {
  for (const bin of ["claude", FAKE]) {
    const r = call(bin, { args: ["--print", "--output-format", "stream-json"], input: "x" });
    assert.equal(r.status, 1, bin);
    assert.match(r.stderr, /requires --verbose/);
  }
});

test("a -p --json-schema call under --output-format json prints one result object of the recorded shape", () => {
  const r = call(FAKE, JSON_CALL);
  assert.equal(r.status, 0, r.stderr);
  const [fake] = events(r.stdout);
  const [real] = recorded(JSON_RECORDED);
  assert.deepEqual(read(fake, RESULT_READ), read(real, RESULT_READ), stale);
  assert.deepEqual(usedModels(fake), usedModels(real), stale);
});

test("a stdin prompt under stream-json --verbose prints the system init first and a result of the recorded shape last", () => {
  const r = call(FAKE, STREAM_CALL);
  assert.equal(r.status, 0, r.stderr);
  const [fake, real] = [events(r.stdout), recorded(STREAM_RECORDED)];
  for (const each of [fake, real]) assert.deepEqual([each[0].type, each[0].subtype, each.at(-1).type], ["system", "init", "result"]);
  assert.deepEqual(read(fake.at(-1), RESULT_READ), read(real.at(-1), RESULT_READ), stale);
});
