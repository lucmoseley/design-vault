#!/usr/bin/env node
/**
 * Usage:
 *   node ledger-upkeep.js                      warns once the re-scan is due, and prints nothing before
 *   node ledger-upkeep.js --check              refuses a malformed method miss, a scan date the warning cannot read,
 *                                              a row its criteria or records do not support, or a job marked done with
 *                                              a row unfilled or a research line with no destination
 *   node ledger-upkeep.js --ledger <file>      reads that ledger instead of docs/coverage-ledger.json
 *   node ledger-upkeep.js --store <dir>        reads that rule store instead of design-critique's rules/
 *   node ledger-upkeep.js --library <file>     reads the library's projects from that file instead of data/gallery.json
 *   node ledger-upkeep.js --today <YYYY-MM-DD> judges the warning on that day instead of today
 *
 * When the re-scan is due: docs/coverage-ledger-method.md §7. The warning exits 0 whatever the ledger holds.
 * --check exits 1 on any fault. Either mode exits 2 on a usage error, and --check also on a ledger, store or library
 * it cannot read.
 */
"use strict";

const fs = require("fs");
const path = require("path");

const { parseGate } = require("./plugin/skills/design-round/scripts/gate-form.js");
const { REPO_MARKDOWN_FORM, parseRepoMarkdown } = require("./repo-markdown.js");

const LEDGER = path.join(__dirname, "docs", "coverage-ledger.json");
const STORE = path.join(__dirname, "plugin", "skills", "design-critique", "rules");
const LIBRARY = path.join(__dirname, "data", "gallery.json");
const MISS_FIELDS = ["date", "lead", "family", "issue"];
const FLAGS = new Set(["--check", "--ledger", "--store", "--library", "--today"]);
const CRITERIA = ["sourced", "conditioned", "era_labelled", "carried", "disposed"];
const CARRIED_BY_VERDICT = { covered: true, partial: true, researched: false, "impeccable-only": false, gap: false };
const VERDICTS = Object.keys(CARRIED_BY_VERDICT);
const ERAS = ["T", "E", "mixed"];
const RECORD_NEEDS = { source: "source", "applies-when": "conditions (applies-when)", era: "era" };
// #210
const RECENT_YEAR = /(?<![#\d])20(2[3-9]|[3-9]\d)(?!\d)/;
const NOT_CARRIED = /^not carried: \S/;

const report = (line) => console.log(`design-vault re-scan check: ${line}`);
const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);

function isDay(text) {
  if (typeof text !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(text)) return false;
  const date = new Date(`${text}T00:00:00Z`);
  return !Number.isNaN(date.getTime()) && date.toISOString().startsWith(text);
}

function yearAfter(text) {
  const [y, m, d] = text.split("-").map(Number);
  return new Date(Date.UTC(y + 1, m - 1, d)).toISOString().slice(0, 10);
}

function localToday() {
  const now = new Date();
  return [now.getFullYear(), now.getMonth() + 1, now.getDate()].map((n) => String(n).padStart(2, "0")).join("-");
}

function dueReasons(meta, today) {
  const reasons = [];
  if (today >= yearAfter(meta.built)) reasons.push(`it was last scanned on ${meta.built}, 12 months ago or more`);
  if (today > meta.rescan.due) reasons.push(`meta.rescan's date, ${meta.rescan.due}, has passed`);
  return reasons;
}

function faults(ledger) {
  if (!isObject(ledger)) return { dates: ["the ledger is not a JSON object"], misses: [] };
  const meta = isObject(ledger.meta) ? ledger.meta : {};
  const dates = [];
  if (!isDay(meta.built)) dates.push(`meta.built is not a YYYY-MM-DD date: ${JSON.stringify(meta.built)}`);
  if (!isDay(meta.rescan?.due)) dates.push(`meta.rescan.due is not a YYYY-MM-DD date: ${JSON.stringify(meta.rescan?.due)}`);
  if (!Array.isArray(ledger.method_misses)) return { dates, misses: ["method_misses is not a list"] };
  const families = Object.keys(isObject(meta.sources) ? meta.sources : {});
  const misses = [];
  ledger.method_misses.forEach((miss, i) => {
    const at = `method_misses[${i}]`;
    if (!isObject(miss)) return misses.push(`${at} is not an object`);
    for (const field of MISS_FIELDS) {
      if (typeof miss[field] !== "string" || !miss[field].trim()) misses.push(`${at} lacks ${field}`);
    }
    if (miss.date && !isDay(miss.date)) misses.push(`${at}.date is not a YYYY-MM-DD date: ${JSON.stringify(miss.date)}`);
    if (miss.family && !families.includes(miss.family)) misses.push(`${at}.family is not a source family in meta.sources: ${JSON.stringify(miss.family)}`);
    if (miss.issue && !/^#\d+$/.test(miss.issue)) misses.push(`${at}.issue is not an issue number like #227: ${JSON.stringify(miss.issue)}`);
  });
  return { dates, misses };
}

const listed = (list) => list.join(", ");

function readStore(dir) {
  const records = new Map();
  for (const name of fs.readdirSync(dir).filter((n) => n.endsWith(".md")).sort()) {
    for (const q of parseGate(fs.readFileSync(path.join(dir, name), "utf8")).questions) {
      records.set(q.id, Object.fromEntries(Object.entries(q.fields).map(([field, { value }]) => [field, value])));
    }
  }
  return records;
}

function readProjects(file) {
  const projects = JSON.parse(fs.readFileSync(file, "utf8")).projects;
  return new Map(Object.entries(isObject(projects) ? projects : {}).map(([key, p]) => [key, parseRepoMarkdown(p?.rules)?.file ?? null]));
}

function destinationFault(destination, records, projects) {
  if (typeof destination !== "string" || !destination.trim()) return "no destination";
  if (destination.startsWith("not carried")) return NOT_CARRIED.test(destination) ? null : "a `not carried: ` with no reason";
  const line = destination.match(/^([\w-]+):(.+):(\d+)$/);
  if (line && projects.has(line[1])) {
    if (projects.get(line[1]) === null) return `${JSON.stringify(destination)}, but ${line[1]}'s rules in the library are not ${REPO_MARKDOWN_FORM}`;
    return line[2] === projects.get(line[1]) && +line[3] > 0 ? null : `${JSON.stringify(destination)}, which is not a line of ${line[1]}'s rules file, ${projects.get(line[1])}`;
  }
  return records.has(destination) ? null : `${JSON.stringify(destination)}, which is no record in the rule store, no \`<project>:<rules file>:<line>\` and no \`not carried: <reason>\``;
}

function rowFaults(row, records) {
  const at = `row ${row.key}`;
  const out = [];
  if (!VERDICTS.includes(row.verdict)) return [`${at} has a verdict that is not one of ${listed(VERDICTS)}: ${JSON.stringify(row.verdict)}`];
  const criteria = isObject(row.criteria) ? row.criteria : {};
  const unread = CRITERIA.filter((c) => typeof criteria[c] !== "boolean");
  if (unread.length) return [`${at} gives no true or false for ${listed(unread)} in its criteria`];
  const failing = CRITERIA.filter((c) => !criteria[c]);
  const house = Array.isArray(row.house) ? row.house : [];
  const research = Array.isArray(row.research) ? row.research : [];
  if (row.verdict === "covered" && failing.length) out.push(`${at} is covered, but its criteria fail ${listed(failing)}`);
  if (row.verdict !== "covered" && !failing.length) out.push(`${at} is ${row.verdict}, but all five criteria hold, which is covered`);
  if (row.verdict !== "covered" && criteria.carried !== CARRIED_BY_VERDICT[row.verdict]) {
    out.push(criteria.carried ? `${at} is ${row.verdict}, which nothing carried answers, but its criteria say carried` : `${at} is ${row.verdict}, a carried text answering it, but its criteria say nothing carried does`);
  }
  if (criteria.carried && !house.length) out.push(`${at} is carried, but cites no house text`);
  if (row.verdict === "researched" && !research.length) out.push(`${at} is researched, but cites no research line`);
  if (!criteria.disposed && !research.length) out.push(`${at} has research left undisposed, but cites no research line`);
  if (row.verdict !== "covered") return out;
  if (!ERAS.includes(row.era)) out.push(`${at} is covered, but its era is not one of ${listed(ERAS)}: ${JSON.stringify(row.era)}`);
  const cited = [];
  for (const id of house) {
    const record = records.get(id);
    if (!record) {
      out.push(/:\d+$/.test(id) ? `${at} is covered, but cites ${id}, which is no record id: a covered row cites records alone (#272)` : `${at} is covered, but cites ${id}, which the rule store lacks`);
      continue;
    }
    cited.push([id, record]);
    const missing = Object.keys(RECORD_NEEDS).filter((field) => !record[field]?.trim());
    if (missing.length) out.push(`${at} is covered, but its record ${id} is missing its ${listed(missing.map((f) => RECORD_NEEDS[f]))}`);
    if (!String(record.ledger ?? "").split(",").map((k) => k.trim()).includes(row.key)) out.push(`${at} is covered, but its record ${id} does not list it in its ledger`);
  }
  if (row.era === "E" && cited.length && !cited.some(([, r]) => RECENT_YEAR.test(r.source ?? ""))) {
    out.push(`${at} is era-bound and covered, but none of its records (${listed(cited.map(([id]) => id))}) cites a source from 2023 on`);
  }
  return out;
}

function jobFaults(job, rows, records, projects) {
  if (!isObject(job) || job.done === undefined) return [];
  const at = `job ${job.id}`;
  if (typeof job.done !== "string" || !/^#\d+$/.test(job.done)) return [`${at} is marked done by ${JSON.stringify(job.done)}, not an issue number like #275`];
  const out = [];
  const own = rows.filter((r) => r.tag?.job === job.id);
  const accepted = (r) => r.ruling?.fill === false && typeof r.ruling.why === "string" && r.ruling.why.trim();
  const open = own.filter((r) => r.verdict !== "covered" && !accepted(r)).map((r) => r.key);
  if (open.length) out.push(`${at} is done, but rows ${listed(open)} are neither covered nor accepted with a reason`);
  // #216
  const filled = own.filter((r) => r.ruling?.fill !== false).length;
  if (Number.isInteger(job.rows) && filled < job.rows) out.push(`${at} is done with ${filled} of its ${job.rows} rows still tagged to it: a filled row keeps its tag`);
  const destinations = isObject(job.destinations) ? job.destinations : {};
  const lines = [...new Set(own.flatMap((r) => (Array.isArray(r.research) ? r.research : [])))];
  for (const line of lines) {
    const why = destinationFault(destinations[line], records, projects);
    if (why) out.push(`${at} is done, but its research line ${line} has ${why}`);
  }
  return out;
}

function parse(argv) {
  const opts = {};
  for (let i = 0; i < argv.length; i++) {
    const flag = argv[i];
    if (!FLAGS.has(flag)) return { error: `unknown argument ${JSON.stringify(flag)}` };
    if (flag === "--check") opts.check = true;
    else if (i + 1 >= argv.length || argv[i + 1].startsWith("--")) return { error: `${flag} takes a value` };
    else opts[flag.slice(2)] = argv[++i];
  }
  if (opts.today !== undefined && !isDay(opts.today)) return { error: `--today takes a YYYY-MM-DD date, not ${JSON.stringify(opts.today)}` };
  return { opts };
}

function main(argv) {
  const { opts, error } = parse(argv);
  if (error) {
    console.error(`ledger-upkeep: ${error}`);
    return 2;
  }
  const file = opts.ledger || LEDGER;
  let ledger;
  try {
    ledger = JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (err) {
    if (opts.check) {
      console.error(`ledger-upkeep: cannot read ${file}: ${err.message}`);
      return 2;
    }
    // #267
    report(`could not read ${file} (${err.message.split("\n")[0]}); whether the re-scan is due is unknown`);
    return 0;
  }
  const { dates, misses } = faults(ledger);
  if (opts.check) {
    let records, projects;
    try {
      records = readStore(opts.store || STORE);
      projects = readProjects(opts.library || LIBRARY);
    } catch (err) {
      console.error(`ledger-upkeep: cannot read the rule store or the library: ${err.message}`);
      return 2;
    }
    const rows = Array.isArray(ledger?.rows) ? ledger.rows.filter(isObject) : [];
    const jobs = Array.isArray(ledger?.jobs) ? ledger.jobs : [];
    const supportFaults = [...rows.flatMap((row) => rowFaults(row, records)), ...jobs.flatMap((job) => jobFaults(job, rows, records, projects))];
    const found = [...dates, ...misses, ...supportFaults];
    for (const fault of found) console.error(`ledger-upkeep: ${fault}`);
    if (found.length) console.error("ledger-upkeep: the fields are docs/coverage-ledger-method.md §4 (verdicts), §6 (jobs), §7 (scan dates) and §8 (method misses)");
    return found.length ? 1 : 0;
  }
  if (dates.length) {
    report(`${dates.join("; ")}; whether the re-scan is due is unknown`);
    return 0;
  }
  const reasons = dueReasons(ledger.meta, opts.today || localToday());
  if (reasons.length) report(`the coverage ledger's re-scan is due: ${reasons.join(", and ")}. Run it by docs/coverage-ledger-method.md §7 (${ledger.meta.rescan.issue || "its issue"}).`);
  return 0;
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));
