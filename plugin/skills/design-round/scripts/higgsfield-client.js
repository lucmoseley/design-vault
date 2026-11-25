/**
 * higgsfield-client.js — the client higgsfield.js runs (design-vault#18, design-vault#62): its command line, its two
 * settings, and render(), which prices the jobs, holds them to the round ceiling, submits, polls, saves and records
 * each charge. higgsfield.js's header says what a run does. It sits apart from higgsfield.js so the tests call
 * what the program calls (#187). It spends money: base's risk-path rules bind it.
 */
"use strict";
const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { inspect } = require("util");

const API = "https://api.higgsfield.ai";
const LEDGER = "higgsfield-spend.jsonl";
const ENV_FILE = path.join(os.homedir(), ".higgsfield.env");
const SETTINGS = ["HIGGSFIELD_API_KEY", "HIGGSFIELD_ROUND_CEILING_USD"];
const TERMINAL = new Set(["completed", "failed", "nsfw", "canceled"]);
const STEM = /^v\d+-[a-z0-9]+(?:-[a-z0-9]+)*$/;
const ROUND = /^r\d+$/;
const STILL_BRAND = /^(?:avif|avis|heic|heix|heim|heis|hevc|hevx|mif1|msf1)$/;
const ENDPOINT_ID = /^[a-z0-9][a-z0-9.-]*(?:\/[a-z0-9][a-z0-9.-]*)*$/;
const HINTS = {
  401: " (check HIGGSFIELD_API_KEY)",
  403: " (the balance is too low: top up at open.higgsfield.ai)",
};
/** An HTTP error the API answered with; anything else thrown is a network fault. */
class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

/** The image or video type by its first bytes; null for anything else. */
function sniff(bytes) {
  if (bytes.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) return "png";
  if (bytes.subarray(0, 3).equals(Buffer.from([0xff, 0xd8, 0xff]))) return "jpg";
  if (bytes.subarray(0, 4).toString("latin1") === "RIFF" && bytes.subarray(8, 12).toString("latin1") === "WEBP") return "webp";
  // AVIF and HEIC stills share MP4's ftyp box; any other brand is taken for a clip.
  if (bytes.subarray(4, 8).toString("latin1") === "ftyp" && !STILL_BRAND.test(bytes.subarray(8, 12).toString("latin1"))) return "mp4";
  // Matroska shares WebM's EBML header; WebM names itself in the header's DocType.
  // Looked for in the first 64 bytes: a guess at room for the header's fields before DocType.
  if (bytes.subarray(0, 4).equals(Buffer.from([0x1a, 0x45, 0xdf, 0xa3])) && bytes.subarray(4, 64).includes("webm")) return "webm";
  return null;
}

// To a tenth of a cent: a guess at enough to tell one render's price from another's.
const dollars = (usd) => `$${usd.toFixed(3)}`;

function readCredentials(value) {
  const colon = (value ?? "").indexOf(":");
  if (colon < 1 || colon === value.length - 1) {
    throw new Error("HIGGSFIELD_API_KEY must be set, in the environment or ~/.higgsfield.env, to <key id>:<key secret>, as the Higgsfield console issues them");
  }
  return value;
}

function readCeiling(value) {
  const ceiling = Number(value);
  if (value === undefined || String(value).trim() === "" || !Number.isFinite(ceiling) || ceiling < 0) {
    throw new Error("HIGGSFIELD_ROUND_CEILING_USD must be set, in the environment or ~/.higgsfield.env, to the most one round may spend, in dollars; the founder sets it");
  }
  return ceiling;
}

/** A job as the API takes it, with the round folder and file stem it saves to. */
function checkJob(job, index) {
  const where = `job ${index + 1}`;
  if (typeof job?.out !== "string") throw new Error(`${where}: no out path`);
  const stem = path.basename(job.out);
  const roundDir = path.dirname(path.resolve(job.out));
  if (!STEM.test(stem)) throw new Error(`${where}: the out path must end in v<n>-<short-name>, with no extension; got ${JSON.stringify(stem)}`);
  if (!ROUND.test(path.basename(roundDir))) throw new Error(`${where}: the out path must sit in a round folder r<n>/; got ${roundDir}`);
  if (!ENDPOINT_ID.test(job.model ?? "")) throw new Error(`${where}: the model must be an endpoint id such as recraft/v4.1/pro/text-to-image or flux-2-pro; got ${JSON.stringify(job.model)}`);
  if (typeof job.prompt !== "string" || !job.prompt.trim()) throw new Error(`${where}: no prompt`);
  const params = job.params ?? {};
  if (typeof params !== "object" || Array.isArray(params)) throw new Error(`${where}: params must be an object`);
  if (job.max_usd !== undefined && !(Number.isFinite(job.max_usd) && job.max_usd > 0)) {
    throw new Error(`${where}: max_usd must be a positive number of dollars; got ${inspect(job.max_usd)}`);
  }
  const input = { ...params, prompt: job.prompt };
  if (job.aspect_ratio !== undefined) input.aspect_ratio = job.aspect_ratio;
  if (job.resolution !== undefined) input.resolution = job.resolution;
  const round = path.basename(roundDir);
  return { stem, roundDir, round, name: `${round}/${stem}`, model: job.model, input, maxUsd: job.max_usd };
}

function alreadyRendered(job) {
  if (!fs.existsSync(job.roundDir)) return false;
  return fs.readdirSync(job.roundDir).some((file) => file === job.stem || file.startsWith(`${job.stem}.`));
}

function spentIn(roundDir) {
  const file = path.join(roundDir, LEDGER);
  if (!fs.existsSync(file)) return 0;
  const bySubmission = new Map();
  let unkeyed = 0;
  for (const line of fs.readFileSync(file, "utf8").split("\n").filter(Boolean)) {
    const entry = JSON.parse(line);
    const usd = Number(entry.usd);
    // A line with no usable figure would turn the sum to NaN, which passes every ceiling.
    if (!Number.isFinite(usd)) throw new Error(`${file} holds a line with no usd figure: ${line}`);
    // A negative line would free room under the ceiling.
    if (usd < 0) throw new Error(`${file} holds a line with a negative usd figure: ${line}`);
    if (typeof entry.idempotency_key === "string" && entry.idempotency_key) bySubmission.set(entry.idempotency_key, usd);
    else unkeyed += usd;
  }
  return [...bySubmission.values()].reduce((sum, usd) => sum + usd, unkeyed);
}

function record(job, line) {
  fs.mkdirSync(job.roundDir, { recursive: true });
  fs.appendFileSync(path.join(job.roundDir, LEDGER), `${JSON.stringify(line)}\n`);
}

// The key goes to api.higgsfield.ai alone: every URL this sends it to is built from API.
async function call(ctx, method, url, body, headers = {}) {
  const response = await ctx.fetch(url, {
    method,
    headers: { Authorization: `Key ${ctx.credentials}`, ...(body ? { "Content-Type": "application/json" } : {}), ...headers },
    body: body ? JSON.stringify(body) : undefined,
    redirect: "error",
  });
  const text = await response.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    json = undefined;
  }
  if (!response.ok) {
    // A body with no `detail` is quoted to 200 characters: a guess at enough to name the fault.
    const detail = json?.detail === undefined ? text.slice(0, 200) : typeof json.detail === "string" ? json.detail : JSON.stringify(json.detail);
    throw new ApiError(`${method} ${new URL(url).pathname} answered ${response.status}: ${detail}${HINTS[response.status] ?? ""}`, response.status);
  }
  return json;
}

// Retries a network fault or a 5xx; the API's own guidance (docs.higgsfield.ai, Errors and retries). That page
// asks for exponential backoff, with jitter, and a most-attempts cap, but gives no numbers: three tries, 2 s then 4 s
// apart, are guesses. No jitter: one job is retried at a time (docs/research/house-audit-constants.md O1).
// Residual: no total retry deadline, which the page also asks for; the three tries bound the waits, not the calls.
// An error after a transient try is marked `afterFault`, since that earlier try may have reached the API.
async function withRetry(ctx, attempt) {
  let faulted = false;
  for (let tries = 1; ; tries++) {
    try {
      return await attempt();
    } catch (error) {
      const transient = !(error instanceof ApiError) || error.status >= 500;
      if (!transient || tries >= 3) {
        if (faulted && error instanceof Error) error.afterFault = true;
        throw error;
      }
      faulted = true;
      await ctx.sleep(1000 * 2 ** tries);
    }
  }
}

/** A usd figure as the estimate gives it, a number or a numeric string; NaN for anything else, since Number(null) and Number("") are 0. */
function readUsd(value) {
  if (typeof value === "number") return value;
  if (typeof value === "string" && value.trim()) return Number(value);
  return NaN;
}

/** The job's price: the estimate's usd figure, or for a price rule the job's max_usd, left undefined where the job has none. */
async function estimate(ctx, job) {
  const answer = await withRetry(ctx, () => call(ctx, "POST", `${API}/estimate/${job.model}`, job.input));
  const usd = readUsd(answer?.usd);
  if (usd <= 0) throw new Error(`the estimate for ${job.model} is not a positive usd figure: ${JSON.stringify(answer)}`);
  if (Number.isFinite(usd)) return { usd, credits: answer.credits, discount: answer.discount };
  if (answer?.type !== "description") throw new Error(`the estimate for ${job.model} is neither a usd figure nor a price rule: ${JSON.stringify(answer)}`);
  return { usd: job.maxUsd, rule: answer };
}

function priceText(price, suffix = "") {
  if (!price.rule) return `${dollars(price.usd)}${suffix} (${price.credits} credits)`;
  if (price.usd === undefined) return "a price rule, and no max_usd";
  return `at most ${dollars(price.usd)}${suffix}, by its max_usd (the rule: ${JSON.stringify(price.rule)})`;
}

async function submit(ctx, job, idempotencyKey) {
  const accepted = await withRetry(ctx, () => call(ctx, "POST", `${API}/${job.model}`, job.input, { "Idempotency-Key": idempotencyKey }));
  if (typeof accepted?.request_id !== "string" || !accepted.request_id) throw new Error(`the submission carried no request_id: ${JSON.stringify(accepted)}`);
  return accepted;
}

/** Polls an accepted request to a terminal status, or to "timed-out". */
async function poll(ctx, accepted) {
  const statusUrl = `${API}/requests/${encodeURIComponent(accepted.request_id)}/status`;
  const deadline = ctx.now() + ctx.timeoutMs;
  let state = accepted;
  // The first look after 2 s, then each wait half as long again, to 10 s at most: the sample on docs.higgsfield.ai's
  // Polling page, less its jitter, which it asks for only when many workers poll at once.
  let delay = 2000;
  while (!TERMINAL.has(state.status)) {
    if (ctx.now() >= deadline) return { status: "timed-out", request_id: accepted.request_id };
    await ctx.sleep(delay);
    delay = Math.min(delay * 1.5, 10000);
    state = await withRetry(ctx, () => call(ctx, "GET", statusUrl));
  }
  return state;
}

async function download(ctx, url) {
  // No Authorization: the output sits on a CDN, not on the API.
  const response = await ctx.fetch(url);
  if (!response.ok) throw new Error(`the download of ${url} answered ${response.status}`);
  return Buffer.from(await response.arrayBuffer());
}

/** Saves every output a completed request returned; the first takes the stem, any more take -2, -3. */
async function save(ctx, job, outputs) {
  const files = [];
  for (const [index, output] of outputs.entries()) {
    const bytes = await download(ctx, output.url);
    const type = sniff(bytes);
    if (!type) throw new Error(`${output.url} is not a PNG, JPEG, WebP, MP4 or WebM`);
    const file = path.join(job.roundDir, `${job.stem}${index ? `-${index + 1}` : ""}.${type}`);
    fs.writeFileSync(file, bytes);
    files.push(path.join(job.round, path.basename(file)));
  }
  return files;
}

/**
 * Prices the jobs, holds them to the round ceiling, then renders them.
 * Returns how many jobs did not end in a saved file.
 */
async function render(jobs, options = {}) {
  const log = options.log ?? console.log;
  const ctx = {
    credentials: readCredentials(options.credentials),
    fetch: options.fetch ?? globalThis.fetch,
    sleep: options.sleep ?? ((ms) => new Promise((resolve) => setTimeout(resolve, ms))),
    now: options.now ?? Date.now,
    // Ten minutes a job: a guess. The Polling page asks for a timeout fit to the model and gives no number; timing
    // each model's jobs to completion would set it (docs/research/house-audit-constants.md H2).
    timeoutMs: options.timeoutMs ?? 10 * 60 * 1000,
  };
  const ceiling = options.estimateOnly && options.ceiling === undefined ? undefined : readCeiling(options.ceiling);

  const checked = jobs.map(checkJob);
  const outs = new Set();
  for (const job of checked) {
    const out = path.join(job.roundDir, job.stem);
    if (outs.has(out)) throw new Error(`${job.name} appears twice in the batch`);
    outs.add(out);
    if (alreadyRendered(job)) throw new Error(`${job.name} is already rendered; give the candidate a new v<n>`);
  }
  const roundDirs = [...new Set(checked.map((job) => job.roundDir))];

  const priced = [];
  for (const job of checked) priced.push({ ...job, price: await estimate(ctx, job) });
  for (const job of priced) log(`${job.name}  ${job.model}  ${priceText(job.price, " a request")}`);

  const unpriced = priced.filter((job) => job.price.usd === undefined);
  if (unpriced.length) {
    const names = unpriced.map((job) => `${job.name} (the rule: ${JSON.stringify(job.price.rule)})`).join("; ");
    const message = `the estimate carried no usd figure for ${names}. Work out the most each can cost from its rule and give the job a max_usd`;
    if (!options.estimateOnly) throw new Error(`${message}; nothing was submitted`);
    log(`${message}; a run would be refused`);
    return 0;
  }

  const over = [];
  for (const roundDir of roundDirs) {
    const round = path.basename(roundDir);
    const batch = priced.filter((job) => job.roundDir === roundDir).reduce((sum, job) => sum + job.price.usd, 0);
    const spent = spentIn(roundDir);
    log(`${round}: this batch ${dollars(batch)}, already spent ${dollars(spent)}, ceiling ${ceiling === undefined ? "unset" : dollars(ceiling)}`);
    if (ceiling !== undefined && spent + batch > ceiling + 1e-9) over.push(round);
  }
  if (over.length) {
    const overMessage = `the batch would take ${over.join(", ")} past its ${dollars(ceiling)} ceiling`;
    if (!options.estimateOnly) throw new Error(`${overMessage}, so nothing was submitted; the founder raises HIGGSFIELD_ROUND_CEILING_USD, or the batch shrinks`);
    log(`${overMessage}, so a run would be refused`);
  }
  if (options.estimateOnly) return 0;

  let failed = 0;
  for (const [index, job] of priced.entries()) {
    const { name } = job;
    const entry = { at: new Date(ctx.now()).toISOString(), candidate: name, model: job.model, idempotency_key: crypto.randomUUID(), request_id: null, usd: job.price.usd, credits: job.price.credits, discount: job.price.discount, rule: job.price.rule, input: job.input };
    // #571
    record(job, { ...entry, status: "submitting", files: [] });
    let accepted;
    try {
      accepted = await submit(ctx, job, entry.idempotency_key);
    } catch (error) {
      const ran = priced.slice(0, index).map((other) => other.name);
      const ranText = ran.length ? `Ran: ${ran.join(", ")}` : "No job ran";
      // A refusal the API answered at the first try was not charged; a network fault, a 5xx (always retried, so
      // marked afterFault), an answer with no request_id, or a refusal answering a retry may have been.
      if (error instanceof ApiError && !error.afterFault) {
        record(job, { ...entry, usd: 0, status: "refused", http_status: error.status, files: [] });
        if (error.status !== 403) throw error;
        const rest = priced.slice(index).map((other) => other.name);
        throw new Error(`${error.message}. ${ranText}. Not submitted: ${rest.join(", ")}`, { cause: error });
      }
      record(job, { ...entry, status: "unanswered", files: [] });
      const rest = priced.slice(index + 1).map((other) => other.name);
      throw new Error(`${error.message}. ${name} may have reached Higgsfield, so it is recorded at its estimate. ${ranText}. Not submitted: ${rest.length ? rest.join(", ") : "none"}`, { cause: error });
    }
    entry.request_id = accepted.request_id;
    log(`${name}: accepted as request ${accepted.request_id}`);
    record(job, { ...entry, status: "submitted", files: [] });
    let state;
    try {
      state = await poll(ctx, accepted);
    } catch (error) {
      state = { status: "unpolled", error: error.message };
    }
    if (state.status === "timed-out" || state.status === "unpolled") {
      record(job, { ...entry, status: state.status, files: [] });
      const why = state.status === "unpolled" ? `its status could not be read (${state.error})` : `still running after ${ctx.timeoutMs / 1000} s`;
      log(`✗ ${name}: ${why}; recorded at its estimate, since it may yet be charged. Request ${accepted.request_id}`);
      failed++;
      continue;
    }
    if (state.status !== "completed") {
      record(job, { ...entry, usd: 0, status: state.status, files: [] });
      log(`✗ ${name}: ${state.status}${state.error ? ` (${state.error})` : ""}; not charged`);
      failed++;
      continue;
    }
    // An image model answers `images: [...]`, a video model `video: { url }`.
    const outputs = [...(Array.isArray(state.images) ? state.images : []), ...(state.video?.url ? [state.video] : [])];
    // Recorded before the download: the charge stands even if the download fails,
    // and the ledger then keeps the output's URL, live for at least seven days.
    record(job, { ...entry, status: "completed", urls: outputs.map((output) => output.url) });
    if (!outputs.length) {
      log(`✗ ${name}: completed with no image or video`);
      failed++;
      continue;
    }
    try {
      const files = await save(ctx, job, outputs);
      log(`saved ${files.join(", ")}  cost ${priceText(job.price)}`);
    } catch (error) {
      log(`✗ ${name}: charged, but not saved: ${error.message}. The ledger keeps its URL`);
      failed++;
    }
  }
  for (const roundDir of roundDirs) {
    log(`${path.basename(roundDir)} has spent ${dollars(spentIn(roundDir))} of ${dollars(ceiling)}`);
  }
  return failed;
}

function parseValue(text) {
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

function parseArgs(argv) {
  const job = {};
  const params = {};
  let batch;
  let estimateOnly = false;
  const valueAt = (i, what) => {
    if (argv[i] === undefined || argv[i].startsWith("--")) throw new Error(`${argv[i - 1]} takes ${what}`);
    return argv[i];
  };
  for (let i = 0; i < argv.length; i++) {
    const flag = argv[i];
    if (flag === "--estimate") estimateOnly = true;
    else if (flag === "--batch") batch = valueAt(++i, "a jobs file");
    else if (flag === "--out") job.out = valueAt(++i, "a path r<n>/v<n>-<name>");
    else if (flag === "--model") job.model = valueAt(++i, "an endpoint id");
    else if (flag === "--prompt") job.prompt = valueAt(++i, "a prompt");
    else if (flag === "--aspect-ratio") job.aspect_ratio = valueAt(++i, "a ratio such as 16:9");
    else if (flag === "--resolution") job.resolution = valueAt(++i, "a resolution tier");
    else if (flag === "--max-usd") job.max_usd = Number(valueAt(++i, "the most the job can cost, in dollars"));
    else if (flag === "--set") {
      const pair = valueAt(++i, "<field>=<value>");
      const equals = pair.indexOf("=");
      if (equals < 1) throw new Error(`--set takes <field>=<value>; got ${JSON.stringify(pair)}`);
      params[pair.slice(0, equals)] = parseValue(pair.slice(equals + 1));
    } else throw new Error(`unknown argument ${JSON.stringify(flag)}`);
  }
  if (batch === undefined) {
    if (Object.keys(params).length) job.params = params;
    return { jobs: [job], estimateOnly };
  }
  if (Object.keys(job).length || Object.keys(params).length) throw new Error("--batch takes no single-job flags");
  const jobs = JSON.parse(fs.readFileSync(batch, "utf8"));
  if (!Array.isArray(jobs) || jobs.length === 0) throw new Error(`${batch} must hold a non-empty JSON array of jobs`);
  return { jobs, estimateOnly };
}

/** The two settings, each from the environment or else from the key file; the file's other lines are ignored. */
function settings(env, file = ENV_FILE) {
  const fromFile = {};
  if (fs.existsSync(file)) {
    for (const line of fs.readFileSync(file, "utf8").split("\n")) {
      const match = /^\s*(?:export\s+)?([A-Z_][A-Z0-9_]*)=(.*)$/.exec(line);
      if (match) fromFile[match[1]] = match[2].trim().replace(/^(["'])(.*)\1$/, "$2");
    }
  }
  return Object.fromEntries(SETTINGS.map((name) => [name, env[name] ?? fromFile[name]]));
}

module.exports = { render, parseArgs, settings };
