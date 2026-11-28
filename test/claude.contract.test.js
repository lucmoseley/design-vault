"use strict";
// #664
const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");

const FAKE = path.join(__dirname, "claude-fake.js");
const installed = !spawnSync("claude", ["--version"], { encoding: "utf8" }).error;
const skip = !installed && "no claude is installed, so there is no real binary to hold the fake to";
// guess #664
const LIVE_TIMEOUT_MS = 120000;
const SCHEMA = JSON.stringify({ type: "object", properties: { answer: { type: "string" } }, required: ["answer"] });
const BARE = ["--model", "haiku", "--no-session-persistence", "--tools", "", "--max-turns", "4"];
const FIELDS_CALLERS_READ = ["type", "subtype", "is_error", "result", "structured_output", "total_cost_usd", "num_turns", "usage", "modelUsage"];

const dir = fs.mkdtempSync(path.join(os.tmpdir(), "claude-contract-"));
after(() => fs.rmSync(dir, { recursive: true, force: true }));

function both(args, { input, reply = { text: "OK" } } = {}) {
  const replies = path.join(dir, "replies.json");
  fs.writeFileSync(replies, JSON.stringify([reply]));
  const call = (bin) => spawnSync(bin, args, { cwd: dir, input, encoding: "utf8", timeout: LIVE_TIMEOUT_MS, env: { ...process.env, FAKE_CLAUDE_REPLIES: replies } });
  return { real: call("claude"), fake: call(FAKE) };
}
const shape = (event) => Object.fromEntries(FIELDS_CALLERS_READ.map((k) => [k, event[k] === null ? "null" : typeof event[k]]));
const usedModels = (event) => Object.keys(event.modelUsage).map((m) => m.startsWith("claude-haiku"));

test("--version prints one version line of the same shape", { skip }, () => {
  for (const r of Object.values(both(["--version"]))) {
    assert.equal(r.status, 0, r.stderr);
    assert.match(r.stdout, /^\d+\.\d+\.\d+ \(Claude Code\)\n$/);
  }
});

test("stream-json under --print without --verbose is refused, naming --verbose", { skip }, () => {
  for (const r of Object.values(both(["--print", "--output-format", "stream-json"], { input: "x" }))) {
    assert.equal(r.status, 1);
    assert.match(r.stderr, /requires --verbose/);
  }
});

test("a -p prompt with --json-schema under --output-format json prints one result object of the same shape", { skip }, () => {
  const runs = both(["-p", "Give the word OK as the answer field.", "--output-format", "json", "--json-schema", SCHEMA, ...BARE], { reply: { structured: { answer: "OK" } } });
  const [real, fake] = [runs.real, runs.fake].map((r) => {
    assert.equal(r.status, 0, r.stderr);
    return JSON.parse(r.stdout);
  });
  assert.deepEqual(shape(fake), shape(real));
  assert.equal(real.subtype, "success");
  assert.deepEqual(Object.keys(real.structured_output), Object.keys(fake.structured_output));
  assert.deepEqual(usedModels(fake), usedModels(real));
});

test("a prompt on stdin under stream-json --verbose prints JSON lines, the system init first and the result last", { skip }, () => {
  const runs = both(["--print", "--output-format", "stream-json", "--verbose", ...BARE], { input: "Reply with the single word OK." });
  const [real, fake] = [runs.real, runs.fake].map((r) => {
    assert.equal(r.status, 0, r.stderr);
    return r.stdout.trim().split("\n").map((line) => JSON.parse(line));
  });
  for (const events of [real, fake]) {
    assert.deepEqual([events[0].type, events[0].subtype], ["system", "init"]);
    assert.equal(events.at(-1).type, "result");
  }
  assert.deepEqual(shape(fake.at(-1)), shape(real.at(-1)));
});
