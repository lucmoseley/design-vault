#!/usr/bin/env node
/**
 * The round log's gate: data/round-log.jsonl holds one row per design round, across every project, with the
 * founder's first pick made before he read the critic and the critic's own pick (design-vault#95). It refuses a
 * malformed row, and a row that rewrites one HEAD already holds: the log keeps his first pick.
 *
 * Usage:
 *   node round-log.js [--model <id>] [--gate <file> ...]    the working tree's data/round-log.jsonl against HEAD's
 *   node round-log.js --staged                              the index's copy against HEAD's
 *   node round-log.js --log <file> [--previous <file>]
 *
 * A row (FIELDS) takes final_pick only once he leads with another candidate than his first pick. A round he names no
 * leader in has first_pick null and confidence null; agree is null wherever either pick is null. Once his notes on the
 * round are logged as corrections, a round whose record named weakest parts adds rejections, how many of them reject a
 * candidate's trait, and on_weakest, how many of those fall on a named weakest part (#193). A round dated from
 * SETTLES_FROM carries splits, how many look answers the gate check's three critics split on, and settled, how many of
 * those a settle critic answered Yes or No (#170); an older one may (#234).
 *
 * A clean run, save --staged, also prints "calibration due" (#167), giving each reason, once the last row of
 * data/calibration-log.jsonl, the last calibration run, is out of date (#193): ten rows have landed here since its
 * round_log_rows; --model, the critics' Claude model, is not its model; or a commit after the one that logged the run
 * changed a record a gate list carries in the vault's gate or a --gate file (a project's gate). A rules file calls no run
 * (#232 Q2), and nor does a staged record or one the builder or the whole-page or type critic answers, since no gate
 * critic reads it (#323). design-round §0 reads the line.
 *
 * The command line, its exit codes and the reading of the log from git are log-gate.js's.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { isText, isDate, parseRows, runGate } = require("./log-gate.js");
const { gitIn } = require("./git-read.js");
const { parseGate, isGateQuestion } = require("./plugin/skills/design-round/scripts/gate-form.js");

const LOG = "data/round-log.jsonl";
const CALIBRATION_LOG = "data/calibration-log.jsonl";
// The vault's gate is its store of rule records, a directory of gate files.
const VAULT_STORE = "plugin/skills/design-critique/rules";
// A calibration run every ten logged rounds: the founder's ruling on #100 Q9 (B), a knob no source sets (#183). A run
// also re-judges at least this many, so one due on a change is measured on the same sample (#209).
const CALIBRATION_EVERY = 10;
const FIELDS = ["date", "project", "ticket", "round", "first_pick", "reason", "confidence", "critic_pick", "agree", "final_pick", "rejections", "on_weakest", "splits", "settled"];
// The fields a committed row may gain, each once.
const ADDED_LATER = ["final_pick", "rejections", "on_weakest"];
// #170's gate check, which every round runs, landed on 15 Oct 2026, so a round of that day may predate it.
const SETTLES_FROM = "2026-10-16";
const TICKET = /^[\w.-]+\/[\w.-]+#[1-9]\d*$/;

const isPick = (value) => value === null || isText(value);
const isCount = (value) => Number.isInteger(value) && value >= 0;
/**
 * Returns every fault in the log `text`. `previousText` is the log HEAD holds: each of its rows must stand
 * unchanged at the same place, save an ADDED_LATER field added where it had none.
 */
function checkRoundLog(text, previousText = "") {
  const faults = [];
  const fault = (rule, message) => faults.push(`${rule}: ${message}`);
  const rows = parseRows(text, fault);
  const rounds = new Set();
  for (const { row, line } of rows) {
    const at = `line ${line}`;
    for (const key of Object.keys(row)) if (!FIELDS.includes(key)) fault("unknown-field", `${at}: ${key} is not a round-log field`);
    if (!isDate(row.date)) fault("date", `${at}: date ${JSON.stringify(row.date)} is not a YYYY-MM-DD day`);
    if (!isText(row.project)) fault("project", `${at}: project is missing`);
    if (!(typeof row.ticket === "string" && TICKET.test(row.ticket)))
      fault("ticket", `${at}: ticket ${JSON.stringify(row.ticket)} is not owner/repo#n`);
    if (!(Number.isInteger(row.round) && row.round >= 1)) fault("round", `${at}: round ${JSON.stringify(row.round)} is not a whole number from 1`);
    const key = `${row.ticket} r${row.round}`;
    if (rounds.has(key)) fault("duplicate-round", `${at}: ${key} already has a row — one row per round`);
    rounds.add(key);
    for (const pick of ["first_pick", "critic_pick"])
      if (!isPick(row[pick])) fault("pick", `${at}: ${pick} is not a candidate's name or null`);
    if (!isText(row.reason)) fault("reason", `${at}: reason is missing — his one line, or why he named no leader`);
      if (row.first_pick === null) {
      if (row.confidence !== null) fault("confidence", `${at}: confidence is ${JSON.stringify(row.confidence)} on a round with no leader — null`);
    } else if (!(typeof row.confidence === "number" && row.confidence >= 0 && row.confidence <= 100))
      fault("confidence", `${at}: confidence ${JSON.stringify(row.confidence)} is not a percentage from 0 to 100`);
    const compared = isText(row.first_pick) && isText(row.critic_pick);
    const agree = compared ? row.first_pick === row.critic_pick : null;
    if (row.agree !== agree)
      fault("agree", `${at}: agree is ${JSON.stringify(row.agree)} — ${compared ? `the picks ${agree ? "match" : "differ"}, so ${agree}` : "a pick is null, so null"}`);
    if ("final_pick" in row && !(isText(row.final_pick) && row.final_pick !== row.first_pick))
      fault("final-pick", `${at}: final_pick is written only where he leads with another candidate than first_pick`);
    for (const [whole, part, rule] of [["rejections", "on_weakest", "weakest"], ["splits", "settled", "settle"]]) {
      const counts = [whole, part].filter((f) => f in row);
      if (counts.length === 1) fault(rule, `${at}: ${counts[0]} is written only beside ${counts[0] === whole ? part : whole}`);
      else if (counts.length === 2 && !(isCount(row[whole]) && isCount(row[part]) && row[part] <= row[whole]))
        fault(rule, `${at}: ${whole} ${JSON.stringify(row[whole])} and ${part} ${JSON.stringify(row[part])} are not whole numbers from 0, ${part} at most ${whole}`);
    }
    // A row with one count of the two is the pair check's fault above.
    if (isDate(row.date) && row.date >= SETTLES_FROM && !("splits" in row) && !("settled" in row))
      fault("settle", `${at}: splits and settled are missing — a round dated from ${SETTLES_FROM} carries the gate check's counts, 0 and 0 where its critics split on nothing`);
  }

  const before = parseRows(previousText, (rule, message) => fault("previous", `HEAD's log, ${message}`));
  before.forEach(({ row: old }, index) => {
    const now = rows[index]?.row;
    if (!now) return fault("rewrite", `HEAD's row ${index + 1} (${old.ticket} r${old.round}) is gone — the log only grows`);
    const kept = { ...now };
    for (const field of ADDED_LATER) if (!(field in old)) delete kept[field];
    if (JSON.stringify(kept) !== JSON.stringify(old))
      fault("rewrite", `line ${rows[index].line} changes HEAD's row for ${old.ticket} r${old.round} — only a final_pick, or rejections and on_weakest, may be added to it`);
  });
  return faults;
}

/**
 * { since, last }: how many of the round log's rows landed after the last calibration run in `calibrationText`, every
 * row where no run is logged yet, and that run's row, or null. Throws on a calibration-log line that is not a JSON
 * object, or where the last run's round_log_rows is not a whole number from 0.
 */
function calibrationState(text, calibrationText) {
  // runGate reports only on a log its check has passed, so no fault is left to report.
  const rows = parseRows(text, () => {}).length;
  const runs = parseRows(calibrationText, (rule, message) => {
    throw new Error(`${CALIBRATION_LOG}, ${message}`);
  });
  if (!runs.length) return { since: rows, last: null };
  const { row, line } = runs[runs.length - 1];
  if (!isCount(row.round_log_rows))
    throw new Error(`${CALIBRATION_LOG} line ${line}: round_log_rows ${JSON.stringify(row.round_log_rows)} is not a whole number from 0`);
  return { since: rows - row.round_log_rows, last: { ...row, line } };
}

/** A git runner in `file`'s directory, or null where its repo has no commit yet. Throws where git cannot read it. */
function repoOf(file) {
  if (!fs.existsSync(file)) throw new Error(`${file} does not exist`);
  const git = gitIn(path.dirname(file));
  try {
    git("rev-parse", "--verify", "-q", "HEAD");
  } catch (error) {
    // A repo with no commit yet holds no commit of the file.
    if (error.status === 1) return null;
    throw new Error(`git cannot read ${file}: ${String(error.stderr || error.message).trim().split("\n")[0]}`);
  }
  return git;
}

/** A commit time git gives as `%ct`, as an ISO time in UTC: git's own `%cI` prints a zero offset as `+00:00` before 2.45 and `Z` from it. */
const commitTime = (seconds) => new Date(Number(seconds) * 1000).toISOString().replace(".000Z", "Z");

/** When `file` was last committed, as an ISO time, or null where git holds no commit of it. Throws where git cannot read it. */
function lastCommitted(file) {
  const git = repoOf(file);
  const seconds = git && git("log", "-1", "--format=%ct", "--", path.basename(file)).trim();
  return seconds ? commitTime(seconds) : null;
}

/** The records a gate list carries in the gate files `texts`, as one text that no move between files or reordering changes. */
const gateRecords = (texts) =>
  texts
    .flatMap((text) => parseGate(text).questions)
    .filter((q) => q.fields["answered-by"] && isGateQuestion(q))
    // status only puts a record on the list or off it, which the filter has already read.
    .map((q) => JSON.stringify([q.id, ...Object.entries(q.fields).filter(([name]) => name !== "status").map(([name, { value }]) => `${name}: ${value}`).sort()]))
    .sort()
    .join("\n");

/**
 * The time, as an ISO time, of the last commit after `since` on the first-parent line that changed a record a gate
 * list carries in `file` (a gate file, or a directory of them), against its first parent; null where none did. A merge
 * stands for its branch's commits, so a change made on a branch before the run and merged after it counts. Throws where
 * git cannot read it.
 */
function lastGateChange(file, since) {
  const git = repoOf(file);
  if (!git) return null;
  const name = path.basename(file);
  const blobs = new Map();
  const records = (commit) =>
    commit
      ? gateRecords(
          git("ls-tree", "-r", "-z", commit, "--", name)
            .split("\0")
            .filter(Boolean)
            .map((entry) => {
              // <mode> blob <object>\t<path>
              const blob = entry.split("\t")[0].split(" ")[2];
              if (!blobs.has(blob)) blobs.set(blob, git("cat-file", "blob", blob));
              return blobs.get(blob);
            }),
        )
      : "";
  const commits = git("log", "--first-parent", "--format=%H%x09%P%x09%ct", "--", name)
    .split("\n")
    .filter(Boolean)
    .map((line) => line.split("\t"))
    .map(([commit, parents, seconds]) => [commit, parents, commitTime(seconds)])
    .filter(([, , time]) => Date.parse(time) > Date.parse(since));
  for (const [commit, parents, time] of commits) if (records(commit) !== records(parents.split(" ")[0])) return time;
  return null;
}

/**
 * The reasons a calibration run is due, as the header gives them, and why any could not be read: { reasons, unknown }.
 * A reason that cannot be read hides none of the others.
 */
function calibrationReasons(text, calibrationText, options) {
  const reasons = [];
  const unknown = [];
  const read = (check) => {
    try {
      check();
    } catch (error) {
      unknown.push(error.message);
    }
  };
  let last = null;
  read(() => {
    const state = calibrationState(text, calibrationText);
    last = state.last;
    if (state.since >= CALIBRATION_EVERY) reasons.push(`${state.since} rounds logged since the last calibration run`);
  });
  if (!last) return { reasons, unknown };
  if (options.model) {
    if (!isText(last.model)) unknown.push(`${CALIBRATION_LOG} line ${last.line}: the last run records no model`);
    else if (options.model !== last.model) reasons.push(`the critics' model is ${options.model}, and the last run's was ${last.model}`);
  }
  read(() => {
    // A run's row never changes once logged, so the log's last commit is the one that logged the last run. The files
    // sit in other repos, so the run is placed among their commits by time, not history: a change committed while a run
    // was being logged, or with a date set back, is missed.
    const landed = lastCommitted(path.join(__dirname, CALIBRATION_LOG));
    if (!landed) return;
    const gate = path.join(__dirname, VAULT_STORE);
    for (const file of [...(fs.existsSync(gate) ? [gate] : []), ...options.gate.map((f) => path.resolve(f))]) {
      read(() => {
        const changed = lastGateChange(file, landed);
        if (changed) reasons.push(`${path.relative(process.cwd(), file) || file} changed at ${changed}, after the last run was logged`);
      });
    }
  });
  return { reasons, unknown };
}

function calibrationReport(text, options) {
  if (options.staged) return [];
  const file = path.join(__dirname, CALIBRATION_LOG);
  // Fails open (#167): the calibration log is #168's, and a fault in it must not refuse a round log this gate passed.
  const { reasons, unknown } = calibrationReasons(text, fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "", options);
  return [...(reasons.length ? [`calibration due — ${reasons.join("; ")}`] : []), ...unknown.map((why) => `calibration unknown — ${why}`)];
}

const main = (argv) =>
  runGate(argv, { log: LOG, name: "round-log.js", noun: "round log", check: checkRoundLog, report: calibrationReport, extra: { model: "one", gate: "many" } });

if (require.main === module) process.exitCode = main(process.argv.slice(2));

module.exports = { checkRoundLog, FIELDS, CALIBRATION_EVERY };
