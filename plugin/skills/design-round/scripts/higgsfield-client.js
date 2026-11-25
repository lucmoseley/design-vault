"use strict";
const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { inspect } = require("util");
const { API, QUOTED_BODY_CHARS, RETRY_DEADLINE_MS, RefusalError, isTransient, withRetry } = require("./higgsfield-api.js");

const LEDGER = "higgsfield-spend.jsonl";
const LOCK = "higgsfield.lock";
const ENV_FILE = path.join(os.homedir(), ".higgsfield.env");
const SETTINGS = ["HIGGSFIELD_API_KEY", "HIGGSFIELD_ROUND_CEILING_USD"];
const TERMINAL = new Set(["completed", "failed", "nsfw", "canceled"]);
const STEM = /^v\d+-[a-z0-9]+(?:-[a-z0-9]+)*$/;
const ROUND = /^r\d+$/;
const STILL_BRAND = /^(?:avif|avis|heic|heix|heim|heis|hevc|hevx|mif1|msf1)$/;
const ENDPOINT_ID = /^[a-z0-9][a-z0-9.-]*(?:\/[a-z0-9][a-z0-9.-]*)*$/;
const DOCTYPE_WITHIN_BYTES = 64; // #583 guess
const PRICE_DECIMALS = 3; // #583 guess
const JOB_TIMEOUT_MS = 10 * 60 * 1000; // #183 guess
// Higgsfield's recommended poll schedule: https://docs.higgsfield.ai/docs/concepts/polling.md
const POLL_FIRST_WAIT_MS = 2000;
const POLL_WAIT_GROWTH = 1.5;
const POLL_LONGEST_WAIT_MS = 10000;
// https://www.rfc-editor.org/rfc/rfc9110#section-15.5.9 https://www.rfc-editor.org/rfc/rfc6585#section-4
const READ_AGAIN_STATUSES = new Set([408, 429]);

class BatchStoppedError extends Error {
  constructor(message, { stoppedAt, ran, notSubmitted, mayBeCharged, cause }) {
    super(message, { cause });
    this.name = "BatchStoppedError";
    this.stoppedAt = stoppedAt;
    this.ran = ran;
    this.notSubmitted = notSubmitted;
    this.mayBeCharged = mayBeCharged;
  }
}

class LedgerLineError extends Error {
  constructor(file, line, text, fault) {
    super(`${file} line ${line} ${fault}: ${text}`);
    this.name = "LedgerLineError";
    this.file = file;
    this.line = line;
    this.text = text;
  }
}

function sniff(bytes) {
  if (bytes.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) return "png";
  if (bytes.subarray(0, 3).equals(Buffer.from([0xff, 0xd8, 0xff]))) return "jpg";
  if (bytes.subarray(0, 4).toString("latin1") === "RIFF" && bytes.subarray(8, 12).toString("latin1") === "WEBP") return "webp";
  // HEIF stills (AVIF, HEIC) share MP4's ftyp box, told apart by brand: https://mp4ra.org/registered-types/brands
  if (bytes.subarray(4, 8).toString("latin1") === "ftyp" && !STILL_BRAND.test(bytes.subarray(8, 12).toString("latin1"))) return "mp4";
  // Matroska shares WebM's EBML header; WebM names itself in the DocType: https://www.webmproject.org/docs/container/
  if (bytes.subarray(0, 4).equals(Buffer.from([0x1a, 0x45, 0xdf, 0xa3])) && bytes.subarray(4, DOCTYPE_WITHIN_BYTES).includes("webm")) return "webm";
  return null;
}

const dollars = (usd) => `$${usd.toFixed(PRICE_DECIMALS)}`;

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
  for (const [index, line] of fs.readFileSync(file, "utf8").split("\n").entries()) {
    if (!line) continue;
    let entry;
    try {
      entry = JSON.parse(line);
    } catch {
      entry = undefined;
    }
    const refuse = (fault) => new LedgerLineError(file, index + 1, line, fault);
    // #575
    if (entry === null || typeof entry !== "object" || Array.isArray(entry)) {
      const error = refuse("is not a ledger entry, as a run killed mid-write leaves");
      error.message += ". Check the Higgsfield console for that job's charge, then mend the line to carry it";
      throw error;
    }
    const usd = Number(entry.usd);
    if (!Number.isFinite(usd)) throw refuse("holds no usd figure");
    if (usd < 0) throw refuse("holds a negative usd figure");
    if (typeof entry.idempotency_key === "string" && entry.idempotency_key) bySubmission.set(entry.idempotency_key, usd);
    else unkeyed += usd;
  }
  return [...bySubmission.values()].reduce((sum, usd) => sum + usd, unkeyed);
}

// #575
function record(job, line) {
  fs.mkdirSync(job.roundDir, { recursive: true });
  const file = path.join(job.roundDir, LEDGER);
  const before = fs.existsSync(file) ? fs.statSync(file).size : 0;
  try {
    fs.appendFileSync(file, `${JSON.stringify(line)}\n`);
  } catch (error) {
    if (fs.existsSync(file) && fs.statSync(file).size > before) {
      try {
        fs.truncateSync(file, before);
      } catch (cutError) {
        error.message += `; the part it wrote is left torn, as cutting it back failed: ${cutError.message}`;
      }
    }
    throw error;
  }
}

function batchStopped(message, priced, index, { submissionSent, mayBeCharged = submissionSent, cause }) {
  const ran = priced.slice(0, index).map((other) => other.name);
  const notSubmitted = priced.slice(submissionSent ? index + 1 : index).map((other) => other.name);
  const text = `${message}. ${ran.length ? `Ran: ${ran.join(", ")}` : "No job ran"}. Not submitted: ${notSubmitted.length ? notSubmitted.join(", ") : "none"}`;
  return new BatchStoppedError(text, { stoppedAt: priced[index].name, ran, notSubmitted, mayBeCharged, cause });
}

// #583
function readFolderId(dir) {
  const { dev, ino } = fs.statSync(dir, { bigint: true });
  return `${dev}:${ino}`;
}

const asList = (value) => (value == null ? [] : Array.isArray(value) ? value : [value]);

function isHolderAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return error.code === "EPERM";
  }
}

// #583
function readMadeId(dir) {
  const { dev, ino, birthtimeNs } = fs.statSync(dir, { bigint: true });
  return `${dev}:${ino}:${birthtimeNs}`;
}

// #583
function makeFolder(dir, made) {
  const missing = [];
  for (let at = dir; ; at = path.dirname(at)) {
    try {
      fs.lstatSync(at);
      break;
    } catch (error) {
      if (error.code !== "ENOENT" || path.dirname(at) === at) throw error;
      missing.unshift(at);
    }
  }
  for (const at of missing) {
    try {
      fs.mkdirSync(at);
    } catch (error) {
      if (error.code === "EEXIST" && fs.statSync(at).isDirectory()) continue;
      throw error;
    }
    made.push({ at: fs.realpathSync.native(at), id: readMadeId(at) });
  }
}

function tryMakeFolder(dir, made) {
  try {
    makeFolder(dir, made);
    return true;
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
    return false;
  }
}

// #574
function makeRoundFolders(jobs, made) {
  const waitingOnAnotherJobsFolder = jobs.filter((job) => !tryMakeFolder(job.roundDir, made));
  for (const job of waitingOnAnotherJobsFolder) makeFolder(job.roundDir, made);
}

// #577
function takeBack(made, log) {
  for (const { at, id } of [...made].sort((a, b) => b.at.length - a.at.length)) {
    try {
      if (readMadeId(at) === id) fs.rmdirSync(at);
    } catch (error) {
      if (error.code !== "ENOENT" && error.code !== "ENOTEMPTY") log(`✗ could not take back ${at}: ${error.message}; delete it by hand if it is empty`);
    }
  }
}

// #559
function lock(roundDir) {
  const file = path.join(roundDir, LOCK);
  const mine = JSON.stringify({ pid: process.pid, token: crypto.randomUUID(), at: new Date().toISOString() });
  try {
    fs.writeFileSync(file, mine, { flag: "wx" });
    return { file, mine };
  } catch (error) {
    if (error.code !== "EEXIST") throw error;
  }
  let holder;
  try {
    holder = JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    holder = undefined;
  }
  const round = path.basename(roundDir);
  if (!Number.isInteger(holder?.pid)) {
    throw new Error(`${round} holds a lock that cannot be read, ${file}, so nothing was submitted; delete it once no higgsfield.js run is working on the round`);
  }
  if (isHolderAlive(holder.pid)) {
    throw new Error(`${round} is held by another higgsfield.js run (process ${holder.pid}, since ${holder.at}), so nothing was submitted; rerun once it ends, or delete ${file} if process ${holder.pid} is no higgsfield.js run`);
  }
  throw new Error(
    `${round} holds the lock of a higgsfield.js run that ended without releasing it (process ${holder.pid}, since ${holder.at}), so nothing was submitted. A job it submitted may be charged and missing from the ledger: check the Higgsfield console, then delete ${file}`,
  );
}

// #559
function unlockAll(held, log) {
  for (const one of held) {
    try {
      if (fs.readFileSync(one.file, "utf8") === one.mine) fs.rmSync(one.file);
    } catch (error) {
      if (error.code !== "ENOENT") log(`✗ could not release ${one.file}: ${error.message}; delete it by hand`);
    }
  }
}

function readUsd(value) {
  if (typeof value === "number") return value;
  if (typeof value === "string" && value.trim()) return Number(value);
  return NaN;
}

async function estimate(ctx, job) {
  const answer = await withRetry(ctx, "POST", `${API}/estimate/${job.model}`, { body: job.input });
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
  const accepted = await withRetry(ctx, "POST", `${API}/${job.model}`, { body: job.input, headers: { "Idempotency-Key": idempotencyKey } });
  if (typeof accepted?.request_id !== "string" || !accepted.request_id) throw new Error(`the submission carried no request_id: ${JSON.stringify(accepted)}`);
  return accepted;
}

async function poll(ctx, accepted) {
  const statusUrl = `${API}/requests/${encodeURIComponent(accepted.request_id)}/status`;
  const deadline = ctx.now() + ctx.timeoutMs;
  const unpolled = (fault) => ({ status: "unpolled", error: fault.message, request_id: accepted.request_id });
  let state = accepted;
  let delay = POLL_FIRST_WAIT_MS;
  let lastReadFault;
  while (!TERMINAL.has(state.status)) {
    if (ctx.now() >= deadline) return lastReadFault ? unpolled(lastReadFault) : { status: "timed-out", request_id: accepted.request_id };
    await ctx.sleep(delay);
    delay = Math.min(delay * POLL_WAIT_GROWTH, POLL_LONGEST_WAIT_MS);
    // #589
    try {
      const read = await withRetry(ctx, "GET", statusUrl);
      if (typeof read?.status !== "string") throw new Error(`GET ${new URL(statusUrl).pathname} answered no status: ${read === undefined ? "its body is not JSON" : JSON.stringify(read).slice(0, QUOTED_BODY_CHARS)}`);
      state = read;
      lastReadFault = undefined;
    } catch (error) {
      if (!isTransient(error) && !READ_AGAIN_STATUSES.has(error.status)) return unpolled(error);
      lastReadFault = error;
    }
  }
  return state;
}

async function download(ctx, url) {
  // #583
  const response = await ctx.fetch(url);
  if (!response.ok) throw new Error(`the download of ${url} answered ${response.status}`);
  return Buffer.from(await response.arrayBuffer());
}

async function save(ctx, job, outputs, files) {
  for (const [index, output] of outputs.entries()) {
    const bytes = await download(ctx, output.url);
    const type = sniff(bytes);
    if (!type) throw new Error(`${output.url} is not a PNG, JPEG, WebP, MP4 or WebM`);
    const file = path.join(job.roundDir, `${job.stem}${index ? `-${index + 1}` : ""}.${type}`);
    fs.writeFileSync(file, bytes);
    files.push(path.join(job.round, path.basename(file)));
  }
}

async function render(jobs, options = {}) {
  const log = options.log ?? console.log;
  const ctx = {
    credentials: readCredentials(options.credentials),
    fetch: options.fetch ?? globalThis.fetch,
    sleep: options.sleep ?? ((ms) => new Promise((resolve) => setTimeout(resolve, ms))),
    now: options.now ?? Date.now,
    timeoutMs: options.timeoutMs ?? JOB_TIMEOUT_MS,
    retryDeadlineMs: options.retryDeadlineMs ?? RETRY_DEADLINE_MS,
    timeout: options.timeout ?? AbortSignal.timeout,
  };
  const ceiling = options.estimateOnly && options.ceiling === undefined ? undefined : readCeiling(options.ceiling);

  const checked = jobs.map(checkJob);
  const made = [];
  // #559
  const held = [];
  try {
    try {
      makeRoundFolders(checked, made);
    } catch (error) {
      if (!options.estimateOnly || error.code === undefined) throw error;
      log(`a round folder cannot be made (${error.message}), so a run would be refused`);
      return 0;
    }
    let roundDirs;
    try {
      const byKey = new Map();
      for (const job of checked) {
        const key = readFolderId(job.roundDir);
        if (!byKey.has(key)) byKey.set(key, job.roundDir);
        job.roundDir = byKey.get(key);
        job.round = path.basename(job.roundDir);
        job.name = `${job.round}/${job.stem}`;
      }
      roundDirs = [...byKey.values()];
      if (!options.estimateOnly) for (const roundDir of roundDirs) held.push(lock(roundDir));
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
      throw new Error(`a round folder went away before the batch could lock it (${error.message}), most likely taken back by an --estimate of the same round, so nothing was submitted; rerun`, { cause: error });
    }
    return await runBatch(ctx, checked, roundDirs, ceiling, options, log);
  } finally {
    unlockAll(held, log);
    if (options.estimateOnly) takeBack(made, log);
  }
}

async function runBatch(ctx, checked, roundDirs, ceiling, options, log) {
  const outs = new Set();
  for (const job of checked) {
    const out = path.join(job.roundDir, job.stem);
    if (outs.has(out)) throw new Error(`${job.name} appears twice in the batch`);
    outs.add(out);
    if (alreadyRendered(job)) throw new Error(`${job.name} is already rendered; give the candidate a new v<n>`);
  }

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
    const ledgerFault = (status, error) => `${name}: its ${status} line could not be written to ${path.join(job.roundDir, LEDGER)} (${error.message})`;
    // #575
    const recordOrStop = (line, howFar, { submissionSent = true, mayBeCharged } = {}) => {
      try {
        record(job, line);
      } catch (error) {
        throw batchStopped(`${ledgerFault(line.status, error)}; ${howFar}`, priced, index, { submissionSent, mayBeCharged, cause: error });
      }
    };
    // #571
    recordOrStop({ ...entry, status: "submitting", files: [] }, "it was not submitted", { submissionSent: false });
    let accepted;
    try {
      accepted = await submit(ctx, job, entry.idempotency_key);
    } catch (error) {
      // #583
      if (error instanceof RefusalError && !error.mayHaveReached) {
        recordOrStop({ ...entry, usd: 0, status: "refused", http_status: error.status, files: [] }, `it was refused, not charged: ${error.message}`, { submissionSent: false });
        throw batchStopped(error.message, priced, index, { submissionSent: false, cause: error });
      }
      recordOrStop({ ...entry, status: "unanswered", files: [] }, `it may have reached Higgsfield: ${error.message}`);
      throw batchStopped(`${error.message}. ${name} may have reached Higgsfield, so it is recorded at its estimate`, priced, index, { submissionSent: true, cause: error });
    }
    entry.request_id = accepted.request_id;
    log(`${name}: accepted as request ${accepted.request_id}`);
    // #575
    try {
      record(job, { ...entry, status: "submitted", files: [] });
    } catch (error) {
      log(`${ledgerFault("submitted", error)}; request ${accepted.request_id} is polled on, and its outcome line stands in for it`);
    }
    const state = await poll(ctx, accepted);
    if (state.status === "timed-out" || state.status === "unpolled") {
      const why = state.status === "unpolled" ? `its status could not be read (${state.error})` : `still running after ${ctx.timeoutMs / 1000} s`;
      recordOrStop({ ...entry, status: state.status, files: [] }, `request ${accepted.request_id}: ${why}`);
      log(`✗ ${name}: ${why}; recorded at its estimate, since it may yet be charged. Request ${accepted.request_id}`);
      failed++;
      continue;
    }
    if (state.status !== "completed") {
      recordOrStop({ ...entry, usd: 0, status: state.status, files: [] }, `request ${accepted.request_id} ended ${state.status}, not charged`, { mayBeCharged: false });
      log(`✗ ${name}: ${state.status}${state.error ? ` (${state.error})` : ""}; not charged`);
      failed++;
      continue;
    }
    const listed = [...asList(state.images), ...asList(state.video)];
    const outputs = listed.filter((output) => typeof output?.url === "string" && output.url !== "");
    const unreadable = listed.length - outputs.length;
    // #583
    const urls = outputs.map((output) => output.url);
    const unreadableText = unreadable ? `, and ${unreadable} output${unreadable > 1 ? "s" : ""} with no URL` : "";
    let ledgerError;
    try {
      record(job, { ...entry, status: "completed", urls, ...(unreadable ? { unreadable } : {}) });
    } catch (error) {
      ledgerError = error;
    }
    let succeeded = outputs.length > 0 && !unreadable;
    if (unreadable) log(`✗ ${name}: charged, but ${unreadable} of its ${listed.length} outputs carried no URL`);
    else if (!outputs.length) log(`✗ ${name}: completed with no image or video`);
    const files = [];
    if (outputs.length) {
      try {
        await save(ctx, job, outputs, files);
        log(`saved ${files.join(", ")}  cost ${priceText(job.price)}`);
      } catch (error) {
        log(`✗ ${name}: charged, but not saved: ${error.message}. ${ledgerError ? "Its URLs are below" : "The ledger keeps its URLs"}`);
        succeeded = false;
      }
    }
    // #575
    if (ledgerError) {
      const outputsText = urls.length ? `its outputs at ${urls.join(" ")}, live for at least seven days, ${files.length === urls.length ? `saved as ${files.join(", ")}` : files.length ? `only ${files.join(", ")} saved` : "not saved"}` : "with no output URL";
      throw batchStopped(`${ledgerFault("completed", ledgerError)}; request ${accepted.request_id} completed and is charged, ${outputsText}${unreadableText}`, priced, index, { submissionSent: true, cause: ledgerError });
    }
    if (!succeeded) failed++;
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
