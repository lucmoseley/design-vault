#!/usr/bin/env node
/**
 * Usage:
 *   node corrections-log.js                         the working tree's data/corrections-log.jsonl against HEAD's
 *   node corrections-log.js --staged                the index's copy against HEAD's
 *   node corrections-log.js --log <file> [--previous <file>]
 *
 * Refuses a malformed row of data/corrections-log.jsonl, and a row that rewrites one HEAD holds, save a pending
 * ruling answered. candidate is null where the correction was not about one candidate. asset is the brief's asset
 * class, from gate-form.js's vocabulary, and stance whether his words keep a trait or reject one. ruling is "pending"
 * until he answers, then "no rule" or "rule: <gate id or rules-file line>".
 *
 * The command line, its exit codes and the reading of the log from git are log-gate.js's.
 */
"use strict";
const { ROUND_CANDIDATE, isText, isDate, parseRows, runGate } = require("./log-gate.js");
const { ASSET_CLASSES } = require("./plugin/skills/design-round/scripts/gate-form.js");

const LOG = "data/corrections-log.jsonl";
const FIELDS = ["date", "project", "asset", "where", "candidate", "words", "stance", "principle", "missed_by", "ruling"];
const MISSED_BY = ["lint", "gate", "critic", "building session", "no rule"];
const STANCES = ["kept", "rejected"];

const LANDED = /^rule: \S/;
const isRuling = (value) => value === "pending" || value === "no rule" || (typeof value === "string" && LANDED.test(value));

function checkCorrectionsLog(text, previousText = "") {
  const faults = [];
  const fault = (rule, message) => faults.push(`${rule}: ${message}`);
  const rows = parseRows(text, fault);
  const seen = new Set();
  for (const { row, line } of rows) {
    const at = `line ${line}`;
    for (const key of Object.keys(row)) if (!FIELDS.includes(key)) fault("unknown-field", `${at}: ${key} is not a corrections-log field`);
    if (!isDate(row.date)) fault("date", `${at}: date ${JSON.stringify(row.date)} is not a YYYY-MM-DD day`);
    for (const field of ["project", "where", "words", "principle"]) if (!isText(row[field])) fault(field, `${at}: ${field} is missing`);
    if (!(row.candidate === null || (typeof row.candidate === "string" && ROUND_CANDIDATE.test(row.candidate))))
      fault("candidate", `${at}: candidate ${JSON.stringify(row.candidate)} is not "rounds/<slug>-r<n> <name>", or null`);
    if (!ASSET_CLASSES.includes(row.asset)) fault("asset", `${at}: asset ${JSON.stringify(row.asset)} is not one of ${ASSET_CLASSES.join(", ")}`);
    if (!STANCES.includes(row.stance)) fault("stance", `${at}: stance ${JSON.stringify(row.stance)} is not "kept" or "rejected"`);
    if (!MISSED_BY.includes(row.missed_by))
      fault("missed-by", `${at}: missed_by ${JSON.stringify(row.missed_by)} is not one of ${MISSED_BY.map((m) => JSON.stringify(m)).join(", ")}`);
    if (!isRuling(row.ruling)) fault("ruling", `${at}: ruling ${JSON.stringify(row.ruling)} is not "pending", "no rule" or "rule: <gate id or rules-file line>"`);
    const key = JSON.stringify([row.where, row.candidate, row.words]);
    if (seen.has(key)) fault("duplicate-entry", `${at}: these words from ${JSON.stringify(row.where)} about ${JSON.stringify(row.candidate)} already have a row`);
    seen.add(key);
  }

  const before = parseRows(previousText, (rule, message) => fault("previous", `HEAD's log, ${message}`));
  before.forEach(({ row: old }, index) => {
    const now = rows[index]?.row;
    const oldRow = `${old.date} ${old.project}`;
    if (!now) return fault("rewrite", `HEAD's row ${index + 1} (${oldRow}) is gone — the log only grows`);
    if (now.words !== old.words) return fault("words", `line ${rows[index].line} changes his words in HEAD's row for ${oldRow} — they are kept verbatim; log what he says now as a new row`);
    const kept = { ...now };
    if (old.ruling === "pending" && now.ruling !== "pending") kept.ruling = "pending";
    if (JSON.stringify(kept) !== JSON.stringify(old))
      fault("rewrite", `line ${rows[index].line} changes HEAD's row for ${oldRow} — only a pending ruling may be answered; log a change of mind as a new row`);
  });
  return faults;
}

const main = (argv) => runGate(argv, { log: LOG, name: "corrections-log.js", noun: "corrections log", check: checkCorrectionsLog });

if (require.main === module) process.exitCode = main(process.argv.slice(2));

const roundCandidate = ({ candidate }) => {
  if (candidate === null) return null;
  const [tag, name] = candidate.split(" ");
  return { tag, name };
};
const isEntryOfRound = (e, project, tag) => e.project === project && roundCandidate(e)?.tag === tag;

module.exports = { checkCorrectionsLog, roundCandidate, isEntryOfRound, FIELDS, LANDED, STANCES };
