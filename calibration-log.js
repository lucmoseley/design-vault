#!/usr/bin/env node
/**
 * Checks data/calibration-log.jsonl, one row per calibration run: refuses a malformed row, and any change to a row HEAD holds.
 *
 * Usage:
 *   node calibration-log.js                         the working tree's data/calibration-log.jsonl against HEAD's
 *   node calibration-log.js --staged                the index's copy against HEAD's
 *   node calibration-log.js --log <file> [--previous <file>]
 *
 * A row, as calibration-score.js writes it:
 *   date, and round_log_rows: the round log's row count when the run was scored, which round-log.js counts
 *     "calibration due" from;
 *   model, the critics' Claude model, and canary_held_on, the Claude Code version the canary held on and every critic
 *     ran on;
 *   rounds: each round re-judged, "owner/repo#n r<k>";
 *   pick: { agree, of }, each critic's leader against his first pick;
 *   questions: { <gate question id>: { agree, of, unsure } }, and entries: { <corrections-log line>: { agree, of,
 *     unsure } }, each critic's answer where his verdict is known;
 *   new_questions: { <gate question id>: { yes, no, unsure } }, the critics' answers on his first picks to a question
 *     added or reworded since the round;
 *   critics: three { unsure, answers }, how often each critic answered Unsure;
 *   settles: { splits, settled }, summed over the rounds' round-log rows that count them: how many gate-critic splits
 *     a settle critic answered Yes or No;
 *   disagreements: one per critic answer against his verdict, of a kind in KINDS: "pick", "question" or "entry", an
 *     entry's rule "unlanded" or his "rule: …" ruling and its founder Yes where he kept the trait, No where he rejected
 *     it;
 *   where: the comment's link, or the session and date he was told the result in.
 * Each figure's disagreements number of − agree − unsure (of − agree for pick).
 */
"use strict";
const { isObject, isText, isDate, parseRows, runGate } = require("./log-gate.js");

const LOG = "data/calibration-log.jsonl";
const FIELDS = ["date", "round_log_rows", "model", "canary_held_on", "rounds", "pick", "questions", "entries", "new_questions", "critics", "disagreements", "settles", "where"];
const ROUND = /^[\w.-]+\/[\w.-]+#[1-9]\d* r[1-9]\d*$/;
const VERSION = /^\d+\.\d+\.\d+$/;
const CRITIC_LETTERS = ["a", "b", "c"];
const ANSWERS = ["yes", "no"];
const KINDS = {
  pick: ["round", "critic", "founder", "leader", "turned_on"],
  question: ["round", "critic", "candidate", "on", "founder", "answer", "evidence"],
  entry: ["round", "critic", "candidate", "on", "principle", "rule", "founder", "answer", "evidence"],
};

const isCount = (v) => Number.isInteger(v) && v >= 0;
const isName = (v) => v === null || isText(v);

function figureFaults(at, figure, withUnsure, disagreed) {
  const keys = withUnsure ? ["agree", "of", "unsure"] : ["agree", "of"];
  if (!isObject(figure) || Object.keys(figure).sort().join() !== [...keys].sort().join() || !keys.every((k) => isCount(figure[k])))
    return [`${at} is not { ${keys.join(", ")} }, each a whole number from 0`];
  const left = figure.of - figure.agree - (withUnsure ? figure.unsure : 0);
  if (left < 0) return [`${at} counts more answers than its of, ${figure.of}`];
  if (left !== disagreed) return [`${at} leaves ${left} disagreement(s), and ${disagreed} are listed`];
  return [];
}

function disagreementFaults(at, d, rounds) {
  if (!isObject(d) || !(d.kind in KINDS)) return [`${at}: kind ${JSON.stringify(d?.kind)} is not pick, question or entry`];
  const faults = [];
  const fields = KINDS[d.kind];
  for (const key of Object.keys(d)) if (key !== "kind" && !fields.includes(key)) faults.push(`${at}: ${key} is not a ${d.kind} disagreement's field`);
  if (!rounds.includes(d.round)) faults.push(`${at}: round ${JSON.stringify(d.round)} is not one of the run's rounds`);
  if (!CRITIC_LETTERS.includes(d.critic)) faults.push(`${at}: critic ${JSON.stringify(d.critic)} is not a, b or c`);
  if (d.kind === "pick") {
    if (!isName(d.founder) || !isName(d.leader) || d.founder === d.leader) faults.push(`${at}: founder and leader are not two different picks, each a name or null`);
    if (!isText(d.turned_on)) faults.push(`${at}: turned_on is missing — the lens or question the critic's leader turned on`);
    return faults;
  }
  for (const key of ["candidate", "evidence"]) if (!isText(d[key])) faults.push(`${at}: ${key} is missing`);
  if (!ANSWERS.includes(d.founder) || !ANSWERS.includes(d.answer) || d.founder === d.answer) faults.push(`${at}: founder and answer are not one yes and one no`);
  if (d.kind === "question") {
    if (!isText(d.on)) faults.push(`${at}: on is not a gate question id`);
  } else {
    if (!(Number.isInteger(d.on) && d.on >= 1)) faults.push(`${at}: on is not a corrections-log line`);
    if (!isText(d.principle)) faults.push(`${at}: principle is missing`);
    if (!(d.rule === "unlanded" || (typeof d.rule === "string" && /^rule: \S/.test(d.rule)))) faults.push(`${at}: rule is not "unlanded" or "rule: <gate id or rules-file line>"`);
  }
  return faults;
}

function checkCalibrationLog(text, previousText = "") {
  const faults = [];
  const fault = (rule, message) => faults.push(`${rule}: ${message}`);
  const rows = parseRows(text, fault);
  let lastCount = 0;
  for (const { row, line } of rows) {
    const at = `line ${line}`;
    for (const key of Object.keys(row)) if (!FIELDS.includes(key)) fault("unknown-field", `${at}: ${key} is not a calibration-log field`);
    if (!isDate(row.date)) fault("date", `${at}: date ${JSON.stringify(row.date)} is not a YYYY-MM-DD day`);
    if (!isCount(row.round_log_rows)) fault("round-log-rows", `${at}: round_log_rows ${JSON.stringify(row.round_log_rows)} is not a whole number from 0`);
    else if (row.round_log_rows < lastCount) fault("round-log-rows", `${at}: round_log_rows ${row.round_log_rows} is below the run before's ${lastCount} — the round log only grows`);
    else lastCount = row.round_log_rows;
    for (const key of ["model", "where"]) if (!isText(row[key])) fault(key, `${at}: ${key} is missing`);
    if (!(typeof row.canary_held_on === "string" && VERSION.test(row.canary_held_on)))
      fault("canary", `${at}: canary_held_on ${JSON.stringify(row.canary_held_on)} is not the Claude Code version the canary held on`);
    const rounds = Array.isArray(row.rounds) ? row.rounds : [];
    if (!rounds.length || !rounds.every((r) => typeof r === "string" && ROUND.test(r)) || new Set(rounds).size !== rounds.length)
      fault("rounds", `${at}: rounds is not a list of one or more different "owner/repo#n r<k>"`);
    if (!(Array.isArray(row.critics) && row.critics.length === CRITIC_LETTERS.length && row.critics.every((c) => isObject(c) && Object.keys(c).sort().join() === "answers,unsure" && isCount(c.answers) && isCount(c.unsure) && c.unsure <= c.answers)))
      fault("critics", `${at}: critics is not three { unsure, answers }, unsure no more than answers`);
    const tested = row.new_questions;
    if (!(isObject(tested) && Object.entries(tested).every(([id, n]) => id.trim() !== "" && isObject(n) && Object.keys(n).sort().join() === "no,unsure,yes" && Object.values(n).every(isCount))))
      fault("new-questions", `${at}: new_questions is not an object of gate question ids, each { yes, no, unsure }, whole numbers from 0`);
    const { settles } = row;
    if (!(isObject(settles) && Object.keys(settles).sort().join() === "settled,splits" && isCount(settles.splits) && isCount(settles.settled) && settles.settled <= settles.splits))
      fault("settles", `${at}: settles is not { splits, settled }, settled no more than splits`);

    const disagreements = Array.isArray(row.disagreements) ? row.disagreements : [];
    if (!Array.isArray(row.disagreements)) fault("disagreements", `${at}: disagreements is not a list`);
    disagreements.forEach((d, i) => {
      for (const f of disagreementFaults(`${at} disagreement ${i + 1}`, d, rounds)) fault("disagreement", f);
    });
    const disagreed = (kind, on) => disagreements.filter((d) => d?.kind === kind && (on === undefined || String(d.on) === on)).length;
    for (const f of figureFaults(`${at}: pick`, row.pick, false, disagreed("pick"))) fault("pick", f);
    for (const [field, kind, isKey] of [["questions", "question", (k) => k.trim() !== ""], ["entries", "entry", (k) => /^[1-9]\d*$/.test(k)]]) {
      if (!isObject(row[field])) {
        fault(field, `${at}: ${field} is not an object`);
        continue;
      }
      for (const [on, figure] of Object.entries(row[field])) {
        if (!isKey(on)) fault(field, `${at}: ${field} key ${JSON.stringify(on)} is not a ${kind === "entry" ? "corrections-log line" : "gate question id"}`);
        for (const f of figureFaults(`${at}: ${field} ${on}`, figure, true, disagreed(kind, on))) fault(field, f);
      }
      for (const d of disagreements) if (d?.kind === kind && !(String(d.on) in row[field])) fault(field, `${at}: a ${kind} disagreement is on ${JSON.stringify(d.on)}, which ${field} does not count`);
    }
  }

  const before = parseRows(previousText, (rule, message) => fault("previous", `HEAD's log, ${message}`));
  before.forEach(({ row: old }, index) => {
    const now = rows[index];
    if (!now) return fault("rewrite", `HEAD's row ${index + 1} (${old.date}) is gone — the log only grows`);
    if (JSON.stringify(now.row) !== JSON.stringify(old)) fault("rewrite", `line ${now.line} changes HEAD's row for the run of ${old.date} — a run's figures never change; log a new run`);
  });
  return faults;
}

const main = (argv) => runGate(argv, { log: LOG, name: "calibration-log.js", noun: "calibration log", check: checkCalibrationLog });

if (require.main === module) process.exitCode = main(process.argv.slice(2));

module.exports = { checkCalibrationLog, CRITIC_LETTERS };
