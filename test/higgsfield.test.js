"use strict";
// higgsfield.js, which spends money on Higgsfield's pay-per-request API (#18): its client run against a stand-in API
// and CDN handed in as fetch, and the program itself only on runs refused before any call, so no request is real and
// nothing is charged.
// Loosen one and a round can pass its spend ceiling, send the key to the CDN, or lose an image it paid for.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const { after, test } = require("node:test");
const { runInProcessAsync } = require("./core-run-in-process.js");

const SCRIPT = path.join(__dirname, "..", "plugin", "skills", "design-round", "scripts", "higgsfield.js");
const { render, parseArgs, settings } = require(path.join(__dirname, "..", "plugin", "skills", "design-round", "scripts", "higgsfield-client.js"));
// The round's ledger, as higgsfield.js's header names it.
const LEDGER = "higgsfield-spend.jsonl";

const KEY = "key-id:key-secret";
const MODEL = "recraft/v4.1/pro/text-to-image";
const PNG = Buffer.concat([Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]), Buffer.alloc(8)]);
const CDN = "https://cdn.example.com/out.png";

const scratch = [];
after(() => {
  for (const dir of scratch) fs.rmSync(dir, { recursive: true, force: true });
});

function roundDir() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "higgsfield-"));
  scratch.push(dir);
  return path.join(dir, "r1");
}

const reply = (status, body) => ({
  ok: status >= 200 && status < 300,
  status,
  text: async () => (typeof body === "string" ? body : JSON.stringify(body)),
  arrayBuffer: async () => body,
});

/**
 * A stand-in for api.higgsfield.ai and its CDN. `statuses` is what successive
 * status polls answer; `submit` may answer a list of replies, one per attempt.
 */
function fakeApi({ usd = "0.094", estimate, statuses = ["in_progress", "completed"], pollReply, submit, images = [{ url: CDN }], video, cdn = () => reply(200, PNG) } = {}) {
  const calls = [];
  let polls = 0;
  let submits = 0;
  let accepted = 0;
  let clock = 0;
  const fetch = async (url, init = {}) => {
    calls.push({ url, method: init.method ?? "GET", headers: init.headers ?? {}, redirect: init.redirect, body: init.body && JSON.parse(init.body) });
    if (url.startsWith("https://cdn.example.com/")) return cdn();
    const { pathname } = new URL(url);
    if (pathname.startsWith("/estimate/")) return reply(200, estimate === undefined ? { credits: "1.500", usd } : estimate);
    if (pathname.startsWith("/requests/")) {
      if (pollReply) return pollReply;
      const status = statuses[Math.min(polls++, statuses.length - 1)];
      return reply(200, { status, request_id: "req-status", ...(status === "completed" ? (video ? { video } : { images }) : {}), ...(status === "failed" ? { error: "Generation failed" } : {}) });
    }
    const answer = submit?.[submits++];
    if (answer instanceof Error) throw answer;
    if (answer) return answer;
    return reply(200, { status: "queued", request_id: `req-${++accepted}` });
  };
  return {
    calls,
    options: (extra = {}) => ({
      credentials: KEY,
      ceiling: "1.00",
      fetch,
      sleep: async (ms) => {
        clock += ms;
      },
      now: () => clock,
      log: () => {},
      ...extra,
    }),
    submissions: () => calls.filter((call) => call.method === "POST" && !new URL(call.url).pathname.startsWith("/estimate/")),
  };
}

const job = (dir, stem = "v1-dusk", extra = {}) => ({ out: path.join(dir, stem), model: MODEL, prompt: "a manta over an ink sea", aspect_ratio: "16:9", ...extra });
const ledger = (dir) =>
  fs
    .readFileSync(path.join(dir, LEDGER), "utf8")
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line));
const outcomes = (dir) => ledger(dir).filter((entry) => entry.status !== "submitting" && entry.status !== "submitted");

test("a job is priced, submitted, polled, saved under its sniffed type and charged to the round's ledger", async () => {
  const dir = roundDir();
  const api = fakeApi();
  const lines = [];
  const failed = await render([job(dir)], api.options({ log: (line) => lines.push(line) }));

  assert.equal(failed, 0);
  assert.deepEqual(fs.readFileSync(path.join(dir, "v1-dusk.png")), PNG);
  const [submit] = api.submissions();
  assert.equal(submit.url, `https://api.higgsfield.ai/${MODEL}`);
  assert.deepEqual(submit.body, { prompt: "a manta over an ink sea", aspect_ratio: "16:9" });
  assert.equal(submit.headers.Authorization, `Key ${KEY}`);
  assert.match(submit.headers["Idempotency-Key"], /^[0-9a-f-]{36}$/);
  const [submitting, submitted, entry] = ledger(dir);
  assert.deepEqual([submitting.status, submitting.usd, submitting.request_id], ["submitting", 0.094, null]);
  assert.deepEqual([submitted.status, submitted.usd, submitted.request_id], ["submitted", 0.094, "req-1"]);
  assert.match(entry.idempotency_key, /^[0-9a-f-]{36}$/);
  assert.ok([submitting, submitted].every((line) => line.idempotency_key === entry.idempotency_key), "each line of a request carries its idempotency key");
  assert.equal(entry.idempotency_key, submit.headers["Idempotency-Key"]);
  assert.equal(entry.usd, 0.094);
  assert.equal(entry.status, "completed");
  assert.equal(entry.request_id, "req-1");
  assert.equal(entry.input.prompt, "a manta over an ink sea");
  assert.equal(entry.candidate, "r1/v1-dusk");
  assert.ok(lines.some((line) => line.includes("$0.094 a request")), "the price is stated before the batch runs");
  assert.ok(lines.some((line) => line.startsWith("saved r1/v1-dusk.png") && line.includes("cost $0.094")));
});

test("the key goes to the API alone, never to the CDN the image downloads from", async () => {
  const api = fakeApi();
  await render([job(roundDir())], api.options());
  const download = api.calls.find((call) => call.url === CDN);
  assert.ok(download);
  assert.equal(download.headers.Authorization, undefined);
  for (const call of api.calls.filter((call) => call.url !== CDN)) assert.equal(new URL(call.url).origin, "https://api.higgsfield.ai");
});

test("a batch that would pass the round's ceiling is refused whole, with nothing submitted", async () => {
  const dir = roundDir();
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, LEDGER), `${JSON.stringify({ usd: 0.85 })}\n`);
  const api = fakeApi();
  await assert.rejects(render([job(dir, "v1-dusk"), job(dir, "v2-tide")], api.options()), /past its \$1\.000 ceiling, so nothing was submitted/);
  assert.equal(api.submissions().length, 0);
});

test("a batch that fits under the ceiling with what the round has spent runs", async () => {
  const dir = roundDir();
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, LEDGER), `${JSON.stringify({ usd: 0.8 })}\n`);
  const api = fakeApi();
  assert.equal(await render([job(dir, "v1-dusk"), job(dir, "v2-tide")], api.options()), 0);
  assert.equal(api.submissions().length, 2);
  assert.equal(outcomes(dir).length, 3);
});

test("generation refuses to run with no ceiling set; --estimate runs without one and submits nothing", async () => {
  const dir = roundDir();
  const api = fakeApi();
  await assert.rejects(render([job(dir)], api.options({ ceiling: undefined })), /HIGGSFIELD_ROUND_CEILING_USD must be set/);
  assert.equal(await render([job(dir)], api.options({ ceiling: undefined, estimateOnly: true })), 0);
  assert.equal(api.submissions().length, 0);
  assert.equal(fs.existsSync(path.join(dir, LEDGER)), false);
});

test("a key without its secret is refused before any call", async () => {
  const api = fakeApi();
  await assert.rejects(render([job(roundDir())], api.options({ credentials: "key-id-only" })), /<key id>:<key secret>/);
  assert.equal(api.calls.length, 0);
});

test("a failed request is not charged, and the batch carries on to the next job", async () => {
  const dir = roundDir();
  const api = fakeApi({ statuses: ["failed", "completed"] });
  const failed = await render([job(dir, "v1-dusk"), job(dir, "v2-tide")], api.options());
  assert.equal(failed, 1);
  assert.equal(fs.existsSync(path.join(dir, "v1-dusk.png")), false);
  assert.ok(fs.existsSync(path.join(dir, "v2-tide.png")));
  assert.deepEqual(
    ledger(dir).map((entry) => [entry.candidate, entry.status, entry.usd]),
    [
      ["r1/v1-dusk", "submitting", 0.094],
      ["r1/v1-dusk", "submitted", 0.094],
      ["r1/v1-dusk", "failed", 0],
      ["r1/v2-tide", "submitting", 0.094],
      ["r1/v2-tide", "submitted", 0.094],
      ["r1/v2-tide", "completed", 0.094],
    ],
  );
});

test("a request still running at the timeout is recorded at its estimate, since it may yet be charged", async () => {
  const dir = roundDir();
  const api = fakeApi({ statuses: ["in_progress"] });
  assert.equal(await render([job(dir)], api.options({ timeoutMs: 30000 })), 1);
  assert.deepEqual(
    ledger(dir).map((entry) => [entry.status, entry.usd]),
    [["submitting", 0.094], ["submitted", 0.094], ["timed-out", 0.094]],
  );
});

test("a submitted job whose status poll fails is recorded at its estimate, the batch carries on, and a rerun counts it against the ceiling", async () => {
  const dir = roundDir();
  const failing = fakeApi({ usd: "0.25", pollReply: reply(404, { detail: "Not found" }) });
  assert.equal(await render([job(dir, "v1-dusk"), job(dir, "v2-tide")], failing.options({ ceiling: "0.60" })), 2);
  assert.equal(failing.submissions().length, 2);
  assert.deepEqual(
    ledger(dir).map((entry) => [entry.status, entry.usd, entry.request_id]),
    [
      ["submitting", 0.25, null],
      ["submitted", 0.25, "req-1"],
      ["unpolled", 0.25, "req-1"],
      ["submitting", 0.25, null],
      ["submitted", 0.25, "req-2"],
      ["unpolled", 0.25, "req-2"],
    ],
  );
  const rerun = fakeApi({ usd: "0.25" });
  await assert.rejects(render([job(dir, "v3-ebb")], rerun.options({ ceiling: "0.60" })), /past its \$0\.600 ceiling/);
  assert.equal(rerun.submissions().length, 0);
});

test("a run abandoned mid-poll leaves its charge on the ledger, so a rerun's ceiling counts it (#571)", async () => {
  const dir = roundDir();
  const stopped = fakeApi({ usd: "0.20", pollReply: new Promise(() => {}) });
  const lines = [];
  render([job(dir, "v1-dusk")], stopped.options({ ceiling: "0.30", log: (line) => lines.push(line) }));
  for (let turns = 0; !stopped.calls.some((call) => call.url.includes("/requests/")); turns++) {
    assert.ok(turns < 100, "the run never reached its first poll");
    await new Promise(setImmediate);
  }
  assert.deepEqual(
    ledger(dir).map((entry) => [entry.status, entry.usd, entry.request_id]),
    [["submitting", 0.2, null], ["submitted", 0.2, "req-1"]],
  );
  assert.ok(lines.includes("r1/v1-dusk: accepted as request req-1"), "the request id is printed before polling");
  fs.rmSync(path.join(dir, "higgsfield.lock"));
  const rerun = fakeApi({ usd: "0.20" });
  await assert.rejects(render([job(dir, "v2-tide")], rerun.options({ ceiling: "0.30" })), /past its \$0\.300 ceiling/);
  assert.equal(rerun.submissions().length, 0);
});

test("a finished request's outcome supersedes its submitted line, so the ceiling counts it once (#571)", async () => {
  const dir = roundDir();
  assert.equal(await render([job(dir, "v1-dusk")], fakeApi({ usd: "0.20" }).options({ ceiling: "0.30" })), 0);
  const rerun = fakeApi({ usd: "0.10" });
  assert.equal(await render([job(dir, "v2-tide")], rerun.options({ ceiling: "0.30" })), 0);
  assert.equal(rerun.submissions().length, 1);
});

test("a run stopped while a lost submission waits to be retried leaves its charge on the ledger (#571)", async () => {
  const dir = roundDir();
  const stopped = fakeApi({ usd: "0.20", submit: [new TypeError("fetch failed")] });
  render([job(dir, "v1-dusk")], stopped.options({ ceiling: "0.30", sleep: () => new Promise(() => {}) }));
  for (let turns = 0; stopped.submissions().length === 0; turns++) {
    assert.ok(turns < 100, "the run never submitted");
    await new Promise(setImmediate);
  }
  fs.rmSync(path.join(dir, "higgsfield.lock"));
  const rerun = fakeApi({ usd: "0.20" });
  await assert.rejects(render([job(dir, "v2-tide")], rerun.options({ ceiling: "0.30" })), /past its \$0\.300 ceiling/);
  assert.equal(rerun.submissions().length, 0);
});

test("two submissions the API answers with one request_id are still two charges (#571)", async () => {
  const dir = roundDir();
  const same = fakeApi({ usd: "0.20", submit: [reply(200, { status: "queued", request_id: "same" }), reply(200, { status: "queued", request_id: "same" })] });
  assert.equal(await render([job(dir, "v1-dusk"), job(dir, "v2-tide")], same.options({ ceiling: "0.50" })), 0);
  const rerun = fakeApi({ usd: "0.20" });
  await assert.rejects(render([job(dir, "v3-reef")], rerun.options({ ceiling: "0.50" })), /past its \$0\.500 ceiling/);
});

test("a submission answered with an empty request_id is recorded at its estimate, since it may have been charged", async () => {
  const dir = roundDir();
  await assert.rejects(render([job(dir)], fakeApi({ submit: [reply(200, { status: "queued", request_id: "" })] }).options()), /may have reached Higgsfield/);
  assert.deepEqual(
    ledger(dir).map((entry) => [entry.status, entry.usd]),
    [["submitting", 0.094], ["unanswered", 0.094]],
  );
});

test("a submission refused at its first try is recorded at $0, so its estimate leaves the ceiling (#571)", async () => {
  const dir = roundDir();
  await assert.rejects(render([job(dir)], fakeApi({ usd: "0.20", submit: [reply(422, { detail: "aspect_ratio is invalid" })] }).options({ ceiling: "0.30" })), /422/);
  assert.deepEqual(
    ledger(dir).map((entry) => [entry.status, entry.usd]),
    [["submitting", 0.2], ["refused", 0]],
  );
  assert.equal(ledger(dir)[1].http_status, 422);
  assert.equal(ledger(dir)[1].error, undefined, "the API's message, which may echo the request, stays off the ledger");
  assert.equal(await render([job(dir, "v2-tide")], fakeApi({ usd: "0.20" }).options({ ceiling: "0.30" })), 0);
});

function ledgerTurnsReadOnlyAtFirstCall(api, dir, matching, extra) {
  const options = api.options(extra);
  const fetch = options.fetch;
  let turned = false;
  options.fetch = async (url, init = {}) => {
    if (!turned && matching(new URL(url).pathname, init)) {
      fs.chmodSync(path.join(dir, LEDGER), 0o444);
      turned = true;
    }
    return fetch(url, init);
  };
  return options;
}

test("a ledger write that fails once the API accepts a job leaves its request id on screen, and the job is polled on to its URLs (#571, #575)", async () => {
  const dir = roundDir();
  const api = fakeApi();
  const lines = [];
  const options = ledgerTurnsReadOnlyAtFirstCall(api, dir, (pathname, init) => init.method === "POST" && !pathname.startsWith("/estimate/"), { log: (line) => lines.push(line) });
  await assert.rejects(render([job(dir)], options), (error) => {
    assert.equal(error.cause?.code, "EACCES");
    assert.match(error.message, /its completed line could not be written.*request req-1 completed and is charged, its outputs at https:\/\/cdn\.example\.com\/out\.png/);
    return true;
  });
  assert.ok(lines.includes("r1/v1-dusk: accepted as request req-1"));
  assert.ok(lines.some((line) => /^r1\/v1-dusk: its submitted line could not be written.*request req-1 is polled on/.test(line)), lines.join("\n"));
  assert.deepEqual(
    ledger(dir).map((entry) => [entry.status, entry.usd]),
    [["submitting", 0.094]],
    "the submitting line still counts the charge at its estimate",
  );
});

test("a submitted line that cannot be written leaves the job polled on, saved and charged by its outcome line, with the batch carrying on (#575)", async () => {
  const dir = roundDir();
  const api = fakeApi();
  const lines = [];
  const options = ledgerTurnsReadOnlyAtFirstCall(api, dir, (pathname, init) => init.method === "POST" && !pathname.startsWith("/estimate/"), { log: (line) => lines.push(line) });
  const fetch = options.fetch;
  options.fetch = async (url, init = {}) => {
    if (new URL(url).pathname.startsWith("/requests/")) fs.chmodSync(path.join(dir, LEDGER), 0o644);
    return fetch(url, init);
  };
  assert.equal(await render([job(dir, "v1-dusk"), job(dir, "v2-tide")], options), 0);
  assert.ok(lines.some((line) => /^r1\/v1-dusk: its submitted line could not be written/.test(line)), lines.join("\n"));
  assert.ok(fs.existsSync(path.join(dir, "v1-dusk.png")) && fs.existsSync(path.join(dir, "v2-tide.png")));
  assert.deepEqual(
    ledger(dir).map((entry) => [entry.candidate, entry.status]),
    [
      ["r1/v1-dusk", "submitting"],
      ["r1/v1-dusk", "completed"],
      ["r1/v2-tide", "submitting"],
      ["r1/v2-tide", "submitted"],
      ["r1/v2-tide", "completed"],
    ],
  );
  assert.equal(ledger(dir)[1].request_id, "req-1");
});

test("a ledger write that fails once a request completes names its request id and every output URL, and stops the batch naming what ran (#575)", async () => {
  const dir = roundDir();
  const second = "https://cdn.example.com/out-2.png";
  const api = fakeApi({ images: [{ url: CDN }, { url: second }, {}] });
  let polls = 0;
  const options = ledgerTurnsReadOnlyAtFirstCall(api, dir, (pathname) => pathname.startsWith("/requests/") && ++polls === 2);
  await assert.rejects(render([job(dir, "v1-dusk"), job(dir, "v2-tide")], options), (error) => {
    assert.match(error.message, /^r1\/v1-dusk: its completed line could not be written to .*higgsfield-spend\.jsonl \(EACCES/);
    assert.ok(error.message.includes(`request req-1 completed and is charged, its outputs at ${CDN} ${second}, live for at least seven days, and 1 output with no URL`), error.message);
    assert.match(error.message, /No job ran\. Not submitted: r1\/v2-tide$/);
    assert.equal(error.cause.code, "EACCES");
    return true;
  });
  assert.equal(api.submissions().length, 1, "the batch stops at the job whose line was lost");
  assert.equal(api.calls.filter((call) => call.url.startsWith("https://cdn.example.com/")).length, 0, "nothing is downloaded past a lost line");
  assert.equal(fs.existsSync(path.join(dir, "higgsfield.lock")), false, "the round's lock is released");
  assert.deepEqual(
    ledger(dir).map((entry) => [entry.status, entry.usd]),
    [
      ["submitting", 0.094],
      ["submitted", 0.094],
    ],
    "the submitted line still counts the charge at its estimate",
  );
});

test("a torn ledger line, as a run killed mid-write leaves, is refused naming the file and line, before anything is submitted (#575)", async () => {
  for (const torn of ['{"usd":0.094,"candidate":"r1/v1-du', "null", "[0.094]"]) {
    const dir = roundDir();
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, LEDGER), `${JSON.stringify({ usd: 0.094 })}\n\n${torn}`);
    const api = fakeApi();
    await assert.rejects(render([job(dir, "v2-tide")], api.options()), new RegExp(`${path.join(dir, LEDGER).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")} line 3 is not a ledger entry`), torn);
    assert.equal(api.submissions().length, 0, torn);
  }
});

test("a failed request's $0 outcome takes its submitted charge off the ceiling (#571)", async () => {
  const dir = roundDir();
  assert.equal(await render([job(dir, "v1-dusk")], fakeApi({ usd: "0.20", statuses: ["failed"] }).options({ ceiling: "0.30" })), 1);
  assert.equal(ledger(dir).at(-1).error, undefined, "the API's text stays off the ledger");
  const rerun = fakeApi({ usd: "0.20" });
  assert.equal(await render([job(dir, "v2-tide")], rerun.options({ ceiling: "0.30" })), 0);
  assert.equal(rerun.submissions().length, 1);
});

test("an estimate that is not a positive usd figure is refused before anything is submitted", async () => {
  for (const usd of ["-5", "0"]) {
    const api = fakeApi({ usd });
    await assert.rejects(render([job(roundDir())], api.options()), /not a positive usd figure/, usd);
    assert.equal(api.submissions().length, 0, usd);
  }
});

test("a ledger line with a negative usd figure is refused, since it would free room under the ceiling", async () => {
  const dir = roundDir();
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, LEDGER), `${JSON.stringify({ usd: -5 })}\n`);
  const api = fakeApi();
  await assert.rejects(render([job(dir)], api.options()), /line 1 holds a negative usd figure/);
  assert.equal(api.submissions().length, 0);
});

test("a submission answered 5xx is retried under the same idempotency key", async () => {
  const api = fakeApi({ submit: [reply(502, { detail: "Bad gateway" })] });
  assert.equal(await render([job(roundDir())], api.options()), 0);
  const keys = api.submissions().map((call) => call.headers["Idempotency-Key"]);
  assert.equal(keys.length, 2);
  assert.equal(keys[0], keys[1]);
});

test("a 403 names the low balance and is not retried", async () => {
  const api = fakeApi({ submit: [reply(403, { detail: "Not enough credits" })] });
  await assert.rejects(render([job(roundDir())], api.options()), /answered 403: Not enough credits \(the balance is too low/);
  assert.equal(api.submissions().length, 1);
});

test("an out path off the r<n>/v<n>-<name> shape, or one already rendered, is refused before any call", async () => {
  const dir = roundDir();
  const api = fakeApi();
  await assert.rejects(render([job(dir, "dusk")], api.options()), /must end in v<n>-<short-name>/);
  await assert.rejects(render([job(dir, "v1-dusk.png")], api.options()), /must end in v<n>-<short-name>/);
  await assert.rejects(render([{ ...job(dir), out: path.join(path.dirname(dir), "drafts", "v1-dusk") }], api.options()), /round folder r<n>/);
  await assert.rejects(render([job(dir), job(dir)], api.options()), /appears twice/);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, "v1-dusk.jpg"), "");
  await assert.rejects(render([job(dir)], api.options()), /already rendered/);
  assert.equal(api.calls.length, 0);
});

test("--set sends JSON where it parses and the plain string otherwise", () => {
  const { jobs, estimateOnly } = parseArgs(["--estimate", "--out", "r1/v1-a", "--model", MODEL, "--prompt", "p", "--set", 'colors=[{"rgb":[40,90,150]}]', "--set", "output_format=png"]);
  assert.equal(estimateOnly, true);
  assert.deepEqual(jobs[0].params, { colors: [{ rgb: [40, 90, 150] }], output_format: "png" });
});

test("--batch takes no single-job flags", () => {
  assert.throws(() => parseArgs(["--batch", "jobs.json", "--prompt", "p"]), /--batch takes no single-job flags/);
});

test("a ledger line with no usd figure stops the batch rather than letting the ceiling read NaN", async () => {
  const dir = roundDir();
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, LEDGER), `${JSON.stringify({ note: "hand edit" })}\n`);
  const api = fakeApi({ usd: "50" });
  await assert.rejects(render([job(dir)], api.options()), /line 1 holds no usd figure/);
  assert.equal(api.submissions().length, 0);
});

test("--estimate over the ceiling says a run would be refused, and submits nothing", async () => {
  const api = fakeApi({ usd: "2" });
  const lines = [];
  assert.equal(await render([job(roundDir())], api.options({ estimateOnly: true, log: (line) => lines.push(line) })), 0);
  assert.ok(lines.some((line) => line.includes("so a run would be refused")));
  assert.equal(api.submissions().length, 0);
});

test("a download that fails after the charge is logged as failed, keeps its ledger line, and the batch carries on", async () => {
  const dir = roundDir();
  let downloads = 0;
  const api = fakeApi({ statuses: ["completed"], cdn: () => (downloads++ === 0 ? reply(404, "gone") : reply(200, PNG)) });
  assert.equal(await render([job(dir, "v1-dusk"), job(dir, "v2-tide")], api.options()), 1);
  assert.equal(fs.existsSync(path.join(dir, "v1-dusk.png")), false);
  assert.ok(fs.existsSync(path.join(dir, "v2-tide.png")));
  assert.deepEqual(
    outcomes(dir).map((entry) => entry.urls),
    [[CDN], [CDN]],
  );
});

test("a request that completes with no image is counted as failed", async () => {
  const dir = roundDir();
  const api = fakeApi({ statuses: ["completed"], images: [] });
  assert.equal(await render([job(dir)], api.options()), 1);
  assert.deepEqual(
    ledger(dir).map((entry) => entry.status),
    ["submitting", "submitted", "completed"],
  );
});

test("a completed reply whose outputs are not objects with a URL is charged and counted failed, and the batch carries on (#559)", async () => {
  const dir = roundDir();
  const api = fakeApi({ statuses: ["completed"], images: [null] });
  assert.equal(await render([job(dir, "v1-dusk"), job(dir, "v2-tide")], api.options()), 2);
  assert.deepEqual(
    outcomes(dir).map((entry) => [entry.candidate, entry.status, entry.usd, entry.urls, entry.unreadable]),
    [
      ["r1/v1-dusk", "completed", 0.094, [], 1],
      ["r1/v2-tide", "completed", 0.094, [], 1],
    ],
  );
});

test("a completed reply with one output unreadable saves the rest and is counted failed (#559)", async () => {
  const dir = roundDir();
  const api = fakeApi({ statuses: ["completed"], images: ["not-an-object", { url: CDN }] });
  assert.equal(await render([job(dir)], api.options()), 1);
  assert.deepEqual(fs.readFileSync(path.join(dir, "v1-dusk.png")), PNG);
  assert.deepEqual(outcomes(dir)[0].urls, [CDN]);
});

test("a completed reply whose images is one object rather than a list keeps its URL; one that is a string is unreadable (#559)", async () => {
  const single = roundDir();
  assert.equal(await render([job(single)], fakeApi({ statuses: ["completed"], images: { url: CDN } }).options()), 0);
  assert.deepEqual(outcomes(single)[0].urls, [CDN]);
  const text = roundDir();
  assert.equal(await render([job(text)], fakeApi({ statuses: ["completed"], images: CDN }).options()), 1);
  assert.deepEqual([outcomes(text)[0].urls, outcomes(text)[0].unreadable], [[], 1]);
});

test("a job with an unreadable output whose download then fails is counted failed once (#559)", async () => {
  const dir = roundDir();
  const api = fakeApi({ statuses: ["completed"], images: [null, { url: CDN }], cdn: () => reply(500, "") });
  assert.equal(await render([job(dir)], api.options()), 1);
});

function holdFirstPoll() {
  let release;
  let reached;
  const polling = new Promise((resolve) => {
    reached = resolve;
  });
  const sleep = () => {
    if (release) return Promise.resolve();
    reached();
    return new Promise((resolve) => {
      release = resolve;
    });
  };
  return { sleep, polling, release: () => release() };
}

test("a second batch on a round whose batch is still running is refused, submitting nothing, and runs once it ends (#559)", async () => {
  const dir = roundDir();
  const held = holdFirstPoll();
  const running = render([job(dir, "v1-dusk")], fakeApi().options({ sleep: held.sleep }));
  await held.polling;

  for (const stem of ["v1-dusk", "v2-tide"]) {
    const second = fakeApi();
    await assert.rejects(render([job(dir, stem)], second.options()), /r1 is held by another higgsfield\.js run \(process \d+, since .+\), so nothing was submitted; rerun once it ends, or delete .*higgsfield\.lock if process \d+ is no higgsfield\.js run$/);
    assert.equal(second.calls.length, 0);
  }

  held.release();
  assert.equal(await running, 0);
  assert.equal(fs.existsSync(path.join(dir, "higgsfield.lock")), false);
  const later = fakeApi();
  assert.equal(await render([job(dir, "v2-tide")], later.options()), 0);
  assert.equal(later.submissions().length, 1);
});

test("a batch refused at the ceiling leaves the round unlocked (#559)", async () => {
  const dir = roundDir();
  await assert.rejects(render([job(dir)], fakeApi().options({ ceiling: "0.05" })), /past its \$0\.050 ceiling/);
  assert.equal(fs.existsSync(path.join(dir, "higgsfield.lock")), false);
  assert.equal(await render([job(dir)], fakeApi().options()), 0);
});

test("a lock left by a run that ended, or one that cannot be read, is refused and left in place (#559)", async () => {
  const dir = roundDir();
  fs.mkdirSync(dir);
  const lockFile = path.join(dir, "higgsfield.lock");
  const { pid } = spawnSync(process.execPath, ["-e", ""]);
  const dead = JSON.stringify({ pid, at: "2026-01-01T00:00:00.000Z" });
  for (const [content, why] of [
    [dead, /r1 holds the lock of a higgsfield\.js run that ended without releasing it \(process \d+, since 2026-01-01T00:00:00\.000Z\), so nothing was submitted\. A job it submitted may be charged and missing from the ledger: check the Higgsfield console, then delete .*higgsfield\.lock/],
    ["", /r1 holds a lock that cannot be read, .*higgsfield\.lock, so nothing was submitted; delete it once no higgsfield\.js run is working on the round/],
  ]) {
    fs.writeFileSync(lockFile, content);
    const api = fakeApi();
    await assert.rejects(render([job(dir)], api.options()), why);
    assert.equal(api.calls.length, 0);
    assert.equal(fs.readFileSync(lockFile, "utf8"), content);
  }
});

test("one round reached by two spellings is held to its ceiling once, for the whole batch (#559)", async () => {
  const dir = roundDir();
  fs.mkdirSync(dir);
  const alias = path.join(path.dirname(dir), "alias");
  fs.symlinkSync(path.dirname(dir), alias);
  const api = fakeApi();
  const twoSpellings = [job(dir, "v1-dusk"), job(path.join(alias, "r1"), "v2-tide")];
  await assert.rejects(render(twoSpellings, api.options({ ceiling: "0.15" })), /past its \$0\.150 ceiling, so nothing was submitted/);
  assert.equal(api.submissions().length, 0);
  await assert.rejects(render([job(dir, "v1-dusk"), job(path.join(alias, "r1"), "v1-dusk")], api.options()), /r1\/v1-dusk appears twice in the batch/);
});

test("a round not yet made, reached by two spellings through a symlink to a folder not yet made, is one round (#559)", async () => {
  const base = path.dirname(roundDir());
  const alias = path.join(base, "alias");
  fs.symlinkSync(path.join(base, "real"), alias);
  const api = fakeApi();
  const twoSpellings = [job(path.join(alias, "r1"), "v1-dusk"), job(path.join(base, "real", "r1"), "v2-tide")];
  await assert.rejects(render(twoSpellings, api.options({ ceiling: "0.15" })), /past its \$0\.150 ceiling, so nothing was submitted/);
  assert.equal(api.submissions().length, 0);
});

test("a video answered as a list keeps its URL (#559)", async () => {
  const dir = roundDir();
  assert.equal(await render([job(dir)], fakeApi({ statuses: ["completed"], video: [{ url: CDN }] }).options()), 0);
  assert.deepEqual(outcomes(dir)[0].urls, [CDN]);
});

test("a lock that cannot be released is logged, and the batch's other locks and outcome stand (#559)", async () => {
  const first = roundDir();
  const second = roundDir();
  const held = holdFirstPoll();
  const lines = [];
  const running = render([job(first, "v1-dusk"), job(second, "v1-dusk")], fakeApi().options({ sleep: held.sleep, log: (line) => lines.push(line) }));
  await held.polling;
  fs.rmSync(path.join(first, "higgsfield.lock"));
  fs.mkdirSync(path.join(first, "higgsfield.lock"));
  held.release();
  assert.equal(await running, 0);
  assert.equal(fs.existsSync(path.join(second, "higgsfield.lock")), false);
  assert.ok(lines.some((line) => /^✗ could not release .*higgsfield\.lock: .*; delete it by hand$/.test(line)));
});

test("a network fault on submission is retried under the same idempotency key", async () => {
  const api = fakeApi({ submit: [new TypeError("fetch failed")] });
  assert.equal(await render([job(roundDir())], api.options()), 0);
  const calls = api.calls.filter((call) => call.method === "POST" && !new URL(call.url).pathname.startsWith("/estimate/"));
  assert.equal(calls.length, 2);
  assert.equal(calls[0].headers["Idempotency-Key"], calls[1].headers["Idempotency-Key"]);
});

test("a submission whose every try ends on a network fault is recorded at its estimate and stops the batch", async () => {
  const dir = roundDir();
  const fault = new TypeError("fetch failed");
  const api = fakeApi({ usd: "0.25", statuses: ["completed"], submit: [undefined, fault, fault, fault] });
  await assert.rejects(
    render([job(dir, "v1-dusk"), job(dir, "v2-tide"), job(dir, "v3-reef")], api.options({ ceiling: "0.80" })),
    /fetch failed\. r1\/v2-tide may have reached Higgsfield[^]*Ran: r1\/v1-dusk\. Not submitted: r1\/v3-reef/,
  );
  assert.deepEqual(
    outcomes(dir).map((entry) => [entry.candidate, entry.status, entry.usd, entry.request_id]),
    [["r1/v1-dusk", "completed", 0.25, "req-1"], ["r1/v2-tide", "unanswered", 0.25, null]],
  );
  const rerun = fakeApi({ usd: "0.25" });
  await assert.rejects(render([job(dir, "v4-ebb"), job(dir, "v5-swell")], rerun.options({ ceiling: "0.80" })), /past its \$0\.800 ceiling/);
});

test("a submission that may have reached the API is recorded at its estimate: 5xx to the last try, no request_id, or a refusal answering a retry", async () => {
  const cases = {
    "5xx to the last try": [reply(502, {}), reply(502, {}), reply(502, {})],
    "no request_id": [reply(200, { status: "queued" })],
    "a 422 after a lost answer": [new TypeError("fetch failed"), reply(422, { detail: "aspect_ratio is invalid" })],
    "a 403 after a lost answer": [new TypeError("fetch failed"), reply(403, { detail: "Not enough credits" })],
  };
  for (const [what, submit] of Object.entries(cases)) {
    const dir = roundDir();
    await assert.rejects(render([job(dir)], fakeApi({ submit }).options()), /may have reached Higgsfield/, what);
    assert.deepEqual(
      ledger(dir).map((entry) => [entry.status, entry.usd, entry.request_id]),
      [["submitting", 0.094, null], ["unanswered", 0.094, null]],
      what,
    );
  }
});

test("every call to the API refuses to follow a redirect", async () => {
  const api = fakeApi();
  await render([job(roundDir())], api.options());
  for (const call of api.calls.filter((call) => call.url !== CDN)) assert.equal(call.redirect, "error");
});

test("two different r1 folders in one batch are not taken for the same candidate", async () => {
  const api = fakeApi();
  assert.equal(await render([job(roundDir()), job(roundDir())], api.options()), 0);
});

// FLUX.2 and GPT Image 2.5 estimate as a price rule in words, with no usd figure (#49).
const RULE = { type: "description", description: "$0.03 for its first output megapixel, plus $0.015 for every additional output megapixel" };

test("a job priced by a rule and given no max_usd is refused before anything is submitted, naming the rule", async () => {
  const dir = roundDir();
  const api = fakeApi({ estimate: RULE });
  await assert.rejects(render([job(dir)], api.options()), /carried no usd figure.*first output megapixel.*max_usd/s);
  assert.equal(api.submissions().length, 0);
});

test("--estimate names every job priced by a rule with no max_usd, rather than stopping at the first", async () => {
  const dir = roundDir();
  const api = fakeApi({ estimate: RULE });
  const lines = [];
  assert.equal(await render([job(dir, "v1-dusk"), job(dir, "v2-tide")], api.options({ estimateOnly: true, log: (line) => lines.push(line) })), 0);
  const refusal = lines.find((line) => line.includes("a run would be refused"));
  assert.match(refusal, /r1\/v1-dusk.*first output megapixel/);
  assert.match(refusal, /r1\/v2-tide/);
  assert.equal(api.submissions().length, 0);
});

test("a job priced by a rule is held to the ceiling at its max_usd", async () => {
  const dir = roundDir();
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, LEDGER), `${JSON.stringify({ usd: 0.7 })}\n`);
  const api = fakeApi({ estimate: RULE });
  await assert.rejects(render([job(dir, "v1-dusk", { max_usd: 0.2 }), job(dir, "v2-tide", { max_usd: 0.2 })], api.options()), /past its \$1\.000 ceiling, so nothing was submitted/);
  assert.equal(api.submissions().length, 0);
});

test("a job priced by a rule runs under its max_usd and is charged to the ledger at that figure, with the rule beside it", async () => {
  const dir = roundDir();
  const api = fakeApi({ estimate: RULE });
  const lines = [];
  assert.equal(await render([job(dir, "v1-dusk", { max_usd: 0.25 })], api.options({ log: (line) => lines.push(line) })), 0);
  const [submit] = api.submissions();
  assert.equal(submit.body.max_usd, undefined, "max_usd is ours, not the API's");
  const [entry] = outcomes(dir);
  assert.equal(entry.usd, 0.25);
  assert.deepEqual(entry.rule, RULE);
  assert.ok(lines.some((line) => line.includes("at most $0.250") && line.includes("first output megapixel")));
});

test("a job whose estimate carries a usd figure is charged at that figure, whatever its max_usd", async () => {
  const dir = roundDir();
  const api = fakeApi();
  assert.equal(await render([job(dir, "v1-dusk", { max_usd: 0.01 })], api.options()), 0);
  assert.equal(outcomes(dir)[0].usd, 0.094);
});

test("a max_usd that is not a positive number is refused before any call", async () => {
  const api = fakeApi({ estimate: RULE });
  for (const max_usd of [0, -1, "0.2", Infinity, null]) {
    await assert.rejects(render([job(roundDir(), "v1-dusk", { max_usd })], api.options()), /max_usd must be a positive number/);
  }
  assert.equal(api.calls.length, 0);
});

test("--max-usd sets a single job's max_usd", () => {
  const { jobs } = parseArgs(["--out", "r1/v1-a", "--model", MODEL, "--prompt", "p", "--max-usd", "0.3"]);
  assert.equal(jobs[0].max_usd, 0.3);
});

test("an estimate whose usd is null or blank is not read as $0", async () => {
  for (const usd of [null, "", " "]) {
    const api = fakeApi({ estimate: { ...RULE, usd } });
    await assert.rejects(render([job(roundDir())], api.options()), /carried no usd figure/);
    assert.equal(api.submissions().length, 0);
  }
});

test("an estimate that is neither a usd figure nor a price rule is refused, whatever the job's max_usd", async () => {
  for (const estimate of [{}, { detail: "oops" }, null]) {
    const api = fakeApi({ estimate });
    await assert.rejects(render([job(roundDir(), "v1-dusk", { max_usd: 0.25 })], api.options()), /neither a usd figure nor a price rule/);
    assert.equal(api.submissions().length, 0);
  }
});

test("a --max-usd that is not a number is refused, naming what was given", async () => {
  const { jobs } = parseArgs(["--out", path.join(roundDir(), "v1-a"), "--model", MODEL, "--prompt", "p", "--max-usd", "abc"]);
  await assert.rejects(render(jobs, fakeApi().options()), /max_usd must be a positive number of dollars; got NaN/);
});

test("a job priced by a rule that times out is recorded at its max_usd, with the rule beside it", async () => {
  const dir = roundDir();
  const api = fakeApi({ estimate: RULE, statuses: ["in_progress"] });
  assert.equal(await render([job(dir, "v1-dusk", { max_usd: 0.25 })], api.options({ timeoutMs: 30000 })), 1);
  const [entry] = outcomes(dir);
  assert.equal(entry.status, "timed-out");
  assert.equal(entry.usd, 0.25);
  assert.deepEqual(entry.rule, RULE);
});

test("an endpoint id of one segment, as FLUX.2's flux-2-pro, is accepted and sent to its own path", async () => {
  const api = fakeApi();
  assert.equal(await render([job(roundDir(), "v1-dusk", { model: "flux-2-pro" })], api.options()), 0);
  assert.equal(api.submissions()[0].url, "https://api.higgsfield.ai/flux-2-pro");
  await assert.rejects(render([job(roundDir(), "v1-dusk", { model: ".hidden" })], api.options()), /must be an endpoint id/);
});

function envFile(text) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "higgsfield-env-"));
  scratch.push(dir);
  const file = path.join(dir, ".higgsfield.env");
  fs.writeFileSync(file, text);
  return file;
}

test("the key and ceiling are read from ~/.higgsfield.env where the environment lacks them, so no session has to find them", () => {
  const file = envFile('# set by the founder\nexport HIGGSFIELD_API_KEY="id:secret"\nexport HIGGSFIELD_ROUND_CEILING_USD=3\nexport OTHER=x\n');
  assert.deepEqual(settings({}, file), { HIGGSFIELD_API_KEY: "id:secret", HIGGSFIELD_ROUND_CEILING_USD: "3" });
});

test("a variable already in the environment wins over the file", () => {
  const file = envFile("export HIGGSFIELD_API_KEY=file:key\nHIGGSFIELD_ROUND_CEILING_USD='2'\n");
  assert.deepEqual(settings({ HIGGSFIELD_API_KEY: "env:key" }, file), { HIGGSFIELD_API_KEY: "env:key", HIGGSFIELD_ROUND_CEILING_USD: "2" });
});

test("with no key file the environment alone is used", () => {
  assert.deepEqual(settings({ HIGGSFIELD_ROUND_CEILING_USD: "3" }, path.join(os.tmpdir(), "no-such-dir-49", ".higgsfield.env")), { HIGGSFIELD_API_KEY: undefined, HIGGSFIELD_ROUND_CEILING_USD: "3" });
});

const MP4 = Buffer.concat([Buffer.from([0, 0, 0, 0x20]), Buffer.from("ftypisom"), Buffer.alloc(8)]);
const WEBM = Buffer.concat([Buffer.from([0x1a, 0x45, 0xdf, 0xa3, 0x9f, 0x42, 0x86, 0x81, 0x01, 0x42, 0x82, 0x84]), Buffer.from("webm"), Buffer.alloc(8)]);
const CLIP = "https://cdn.example.com/out.mp4";

test("a completed video is saved under its sniffed type, with its URL in the ledger", async () => {
  for (const [bytes, type] of [
    [MP4, "mp4"],
    [WEBM, "webm"],
  ]) {
    const dir = roundDir();
    const api = fakeApi({ video: { url: CLIP }, cdn: () => reply(200, bytes) });
    const lines = [];
    assert.equal(await render([job(dir, "v1-drift")], api.options({ log: (line) => lines.push(line) })), 0);
    assert.deepEqual(fs.readFileSync(path.join(dir, `v1-drift.${type}`)), bytes);
    assert.deepEqual(outcomes(dir)[0].urls, [CLIP]);
    assert.ok(lines.some((line) => line.startsWith(`saved r1/v1-drift.${type}`)));
  }
});

test("a video whose download fails keeps its URL in the ledger, counted as failed", async () => {
  const dir = roundDir();
  const api = fakeApi({ statuses: ["completed"], video: { url: CLIP }, cdn: () => reply(404, "gone") });
  const lines = [];
  assert.equal(await render([job(dir, "v1-drift")], api.options({ log: (line) => lines.push(line) })), 1);
  assert.deepEqual(fs.readdirSync(dir), [LEDGER]);
  assert.deepEqual(outcomes(dir)[0].urls, [CLIP]);
  assert.ok(lines.some((line) => line.includes("charged, but not saved") && line.includes("The ledger keeps its URL")));
});

test("an MP4 of any brand but a still's is saved, since it was charged", async () => {
  const dir = roundDir();
  const m4v = Buffer.concat([Buffer.from([0, 0, 0, 0x20]), Buffer.from("ftypM4V "), Buffer.alloc(8)]);
  const api = fakeApi({ video: { url: CLIP }, cdn: () => reply(200, m4v) });
  assert.equal(await render([job(dir, "v1-drift")], api.options()), 0);
  assert.deepEqual(fs.readFileSync(path.join(dir, "v1-drift.mp4")), m4v);
});

test("a Matroska file that is not WebM, or an AVIF or HEIC still, is not saved as a video", async () => {
  const mkv = Buffer.from(WEBM.toString("latin1").replace("webm", "mkvx"), "latin1");
  const still = (brand) => Buffer.concat([Buffer.from([0, 0, 0, 0x20]), Buffer.from(`ftyp${brand}`), Buffer.alloc(8)]);
  for (const bytes of [mkv, still("avif"), still("heic")]) {
    const dir = roundDir();
    const api = fakeApi({ video: { url: CLIP }, cdn: () => reply(200, bytes) });
    assert.equal(await render([job(dir, "v1-drift")], api.options()), 1);
    assert.deepEqual(fs.readdirSync(dir), [LEDGER]);
  }
});

test("the estimate's discount is recorded on the ledger line beside the usd, which is already net of it", async () => {
  const dir = roundDir();
  const discount = { percentage: 15, credits: "1.008", usd: "0.063" };
  const api = fakeApi({ video: { url: CLIP }, cdn: () => reply(200, MP4), estimate: { credits: "5.712", usd: "0.357", discount } });
  assert.equal(await render([job(dir, "v1-drift")], api.options()), 0);
  const [entry] = outcomes(dir);
  assert.equal(entry.usd, 0.357);
  assert.deepEqual(entry.discount, discount);
});

test("a refusal at the first try part-way through a batch, a 403 or any other, keeps the API's message and names the jobs that ran and those not submitted (#570)", async () => {
  const cases = {
    "a 403": [reply(403, { detail: "Not enough credits" }), /answered 403: Not enough credits \(the balance is too low[^]*/],
    "a 422": [reply(422, { detail: "aspect_ratio is invalid" }), /answered 422: aspect_ratio is invalid/],
  };
  for (const [what, [refusal, apiMessage]] of Object.entries(cases)) {
    const dir = roundDir();
    const api = fakeApi({ statuses: ["completed"], submit: [undefined, refusal] });
    await assert.rejects(
      render([job(dir, "v1-dusk"), job(dir, "v2-tide"), job(dir, "v3-reef")], api.options()),
      new RegExp(`${apiMessage.source}\\. Ran: r1\\/v1-dusk\\. Not submitted: r1\\/v2-tide, r1\\/v3-reef$`),
      what,
    );
    assert.equal(api.submissions().length, 2, what);
    assert.deepEqual(
      outcomes(dir).map((entry) => [entry.candidate, entry.status, entry.usd]),
      [["r1/v1-dusk", "completed", 0.094], ["r1/v2-tide", "refused", 0]],
      what,
    );
  }
});

test("a completed video answer with no url is counted as failed, with nothing downloaded", async () => {
  const dir = roundDir();
  const api = fakeApi({ statuses: ["completed"], video: {} });
  assert.equal(await render([job(dir, "v1-drift")], api.options()), 1);
  assert.deepEqual(outcomes(dir)[0].urls, []);
  assert.equal(api.calls.filter((call) => call.url.startsWith("https://cdn.example.com/")).length, 0);
});

test("a 403 on the batch's first job says no job ran", async () => {
  const api = fakeApi({ submit: [reply(403, { detail: "Not enough credits" })] });
  await assert.rejects(render([job(roundDir())], api.options()), /No job ran\. Not submitted: r1\/v1-dusk/);
});

/**
 * Runs higgsfield.js with `args` and HOME a throwaway folder holding `envFileText` as its .higgsfield.env, or none
 * where it is omitted, so the founder's own key file is never read.
 */
async function program(args, envFileText) {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), "higgsfield-home-"));
  scratch.push(home);
  if (envFileText !== undefined) fs.writeFileSync(path.join(home, ".higgsfield.env"), envFileText);
  return runInProcessAsync(SCRIPT, args, { cwd: home, env: { PATH: process.env.PATH, HOME: home } });
}

test("the program refuses bad usage with exit 2, naming the fault and the usage", async () => {
  for (const [args, why] of [
    [["--out", "r1/v1-a", "--model"], /^higgsfield\.js: --model takes an endpoint id\n/],
    [["--batch", "jobs.json", "--prompt", "p"], /^higgsfield\.js: --batch takes no single-job flags\n/],
    [["--colour", "red"], /^higgsfield\.js: unknown argument "--colour"\n/],
  ]) {
    const r = await program(args);
    assert.equal(r.status, 2, args.join(" "));
    assert.match(r.stderr, why);
    assert.match(r.stderr, /Usage: node higgsfield\.js \[--estimate\] --out/);
  }
});

// Each run below is refused before the API is called: by the key or the ceiling, and failing that by the out path,
// which sits in no round folder.
test("the program with no key exits 1 naming where to set it, before any call", async () => {
  const r = await program(["--out", "dusk", "--model", MODEL, "--prompt", "p"]);
  assert.equal(r.status, 1);
  assert.match(r.stderr, /^higgsfield\.js: HIGGSFIELD_API_KEY must be set, in the environment or ~\/\.higgsfield\.env, to <key id>:<key secret>/);
});

test("the program reads the key from ~/.higgsfield.env, and with no ceiling set exits 1 before any call", async () => {
  const r = await program(["--out", "dusk", "--model", MODEL, "--prompt", "p"], "export HIGGSFIELD_API_KEY=id:secret\n");
  assert.equal(r.status, 1);
  assert.match(r.stderr, /^higgsfield\.js: HIGGSFIELD_ROUND_CEILING_USD must be set/);
});
