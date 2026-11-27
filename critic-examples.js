#!/usr/bin/env node
/**
 * critic-examples.js — deals each critic of a design round its own examples of the founder's taste from
 * data/corrections-log.jsonl.
 *
 * Usage:
 *   node critic-examples.js --project <key> --asset <class> --brief <file> [--count <n>] [--critics <n>] [--log <file>]
 *
 * Only the project's entries are dealt, ranked by relevance to the round: an entry for the brief's asset class first,
 * then by how many words its principle and his words share with the brief, then newest first.
 *
 * Each critic gets as many kept entries as rejected: `--count` (10) halved, or fewer where one stance holds fewer
 * entries. Each critic takes its own window of the most relevant entries of each stance: disjoint sets once each
 * stance holds three critics' share. Each set alternates kept and rejected, the stance it opens with alternating by
 * critic.
 *
 * Prints one section per critic, `## Critic a` and on, each entry his words quoted beside its principle, ready to
 * paste into that critic's dispatch. Exits 0 on a deal, empty where the log holds no entry of one stance; 2 on bad
 * usage, an unreadable file or a log its gate, corrections-log.js, refuses.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { parseArgs } = require("node:util");
const { parseRows } = require("./log-gate.js");
const { checkCorrectionsLog, STANCES } = require("./corrections-log.js");
const { ASSET_CLASSES } = require("./plugin/skills/design-round/scripts/gate-form.js");
const { CRITIC_COUNT } = require("./plugin/skills/design-round/scripts/gate.js");

const LOG = "data/corrections-log.jsonl";
const LETTERS = "abcdefghijklmnopqrstuvwxyz";
const [KEPT, REJECTED] = STANCES;
// guess, #193
const SHORTEST_WORD = 3;
const STOPWORDS = new Set(
  "the and for are but not you all any can had her was one our out has his how its may new now see two who did get him let say she too use that with have this will your from they been more when what were than then them into only some such also just over very most must each much well here there their which would could should about after before where these those while being every other".split(" "),
);

const USAGE = "usage: node critic-examples.js --project <key> --asset <class> --brief <file> [--count <n>] [--critics <n>] [--log <file>]";

const words = (text) => new Set(text.toLowerCase().split(/[^a-z]+/).filter((w) => w.length >= SHORTEST_WORD && !STOPWORDS.has(w)));

function rank(entries, asset, briefWords) {
  const scored = entries.map((e, order) => {
    const shared = [...words(`${e.row.principle} ${e.row.words}`)].filter((w) => briefWords.has(w)).length;
    return { ...e, key: [e.row.asset === asset ? 1 : 0, shared, e.row.date, order] };
  });
  return scored.sort((a, b) => {
    for (let i = 0; i < a.key.length; i++) if (a.key[i] !== b.key[i]) return a.key[i] < b.key[i] ? 1 : -1;
    return 0;
  });
}

function windows(ranked, n, critics) {
  const pool = ranked.slice(0, critics * n);
  const step = Math.floor(pool.length / critics);
  return Array.from({ length: critics }, (_, c) => Array.from({ length: n }, (_, j) => pool[(c * step + j) % pool.length]));
}

function deal(rows, { project, asset, brief, count, critics }) {
  const own = rows.filter(({ row }) => row.project === project);
  const briefWords = words(brief);
  const kept = rank(own.filter(({ row }) => row.stance === KEPT), asset, briefWords);
  const rejected = rank(own.filter(({ row }) => row.stance === REJECTED), asset, briefWords);
  const n = Math.min(Math.floor(count / 2), kept.length, rejected.length);
  if (n === 0) return { sets: Array.from({ length: critics }, () => []), kept: kept.length, rejected: rejected.length, n };
  const [k, r] = [windows(kept, n, critics), windows(rejected, n, critics)];
  const sets = k.map((keptSet, c) => keptSet.flatMap((entry, j) => (c % 2 ? [entry, r[c][j]] : [r[c][j], entry])));
  return { sets, kept: kept.length, rejected: rejected.length, n };
}

function print({ sets, kept, rejected, n }, { project, asset, count }) {
  const from = `${kept} kept and ${rejected} rejected ${project} entries`;
  if (n === 0) {
    console.log(`No examples for ${project}'s ${asset} critics: the log holds ${from}, and a set takes as many of each.`);
    return;
  }
  const short = n < Math.floor(count / 2) ? `, fewer than --count ${count} asks, as one stance holds only ${n}` : "";
  console.log(`Examples for ${project}'s ${asset} critics, from ${from}: ${n} of each per critic${short}.`);
  const same = sets.length > 1 && sets.every((s) => s.map((e) => e.line).sort().join() === sets[0].map((e) => e.line).sort().join());
  if (same) console.log("The log holds too few entries for the critics' sets to differ.");
  sets.forEach((set, c) => {
    console.log(`\n## Critic ${LETTERS[c]}\n`);
    set.forEach(({ row }, i) => console.log(`${i + 1}. The founder ${row.stance}: "${row.words}" — ${row.principle}`));
  });
}

function main(argv) {
  let values;
  try {
    ({ values } = parseArgs({
      args: argv,
      options: { project: { type: "string" }, asset: { type: "string" }, brief: { type: "string" }, count: { type: "string", default: "10" }, critics: { type: "string", default: String(CRITIC_COUNT) }, log: { type: "string" } },
    }));
  } catch (err) {
    console.error(`${err.message}\n${USAGE}`);
    return 2;
  }
  const count = Number(values.count);
  const critics = Number(values.critics);
  let why = null;
  if (!values.project || !values.brief) why = "--project and --brief are both needed";
  else if (!ASSET_CLASSES.includes(values.asset)) why = `--asset is ${values.asset ?? "missing"}, not one of ${ASSET_CLASSES.join(", ")}`;
  else if (!(Number.isInteger(count) && count >= 2)) why = `--count ${values.count} is not a whole number from 2`;
  else if (!(Number.isInteger(critics) && critics >= 1 && critics <= LETTERS.length)) why = `--critics ${values.critics} is not a whole number from 1 to ${LETTERS.length}`;
  if (why) {
    console.error(`${why}\n${USAGE}`);
    return 2;
  }
  let brief, text;
  try {
    brief = fs.readFileSync(values.brief, "utf8");
    const log = values.log ?? path.join(__dirname, LOG);
    text = fs.existsSync(log) || values.log ? fs.readFileSync(log, "utf8") : "";
  } catch (err) {
    console.error(`critic-examples.js: ${err.message}`);
    return 2;
  }
  const faults = checkCorrectionsLog(text);
  if (faults.length) {
    console.error(`critic-examples.js: the corrections log is refused by its gate — ${faults.length} fault(s)`);
    for (const f of faults) console.error(`  ${f}`);
    return 2;
  }
  const options = { project: values.project, asset: values.asset, brief, count, critics };
  print(deal(parseRows(text, () => {}), options), options);
  return 0;
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));
