#!/usr/bin/env node
/**
 * calibration-packet.js — the calibration packet's builder (design-vault#167): writes the one folder a calibration
 * run's critics may read, holding the logged rounds' candidates, briefs and gate lists, and the corrections entries
 * that name a candidate, and refuses a packet that would carry the founder's verdicts to them.
 *
 * Usage:
 *   node calibration-packet.js --manifest <file> --out <dir> [--round-log <file>] [--corrections-log <file>]
 *
 * The manifest names each round to pack, its paths read from the manifest's own folder:
 *   { "rounds": [ { "ticket": "lucmoseley/mmm-infra#9", "round": 2, "tag": "rounds/hero-r2",
 *                   "brief": "<file>", "gate_list": "<file>", "gate_list_then": "<file>", "copy_bans": "<file>",
 *                   "candidates": { "<name>": "<file or folder>" } } ] }
 *
 * gate_list is the look questions as the gates stand now, and gate_list_then those of the round's time, which
 * calibration-score.js reads and the packet leaves out; copy_bans is the copy bans that round's critics were given
 * (#232).
 *
 * The packet holds one folder per round, named `<project>.<slug>-r<n>` for the project its round-log row names and its
 * tag less `rounds/`, since a tag is set per project and two projects may reuse a brief's slug: brief, gate-list and
 * copy-bans (each keeping its extension), candidates/<name>, and entries.json, the corrections entries of its project
 * naming one of its candidates as { entry: <their corrections-log line>, principle }. Nothing else. An entry leaves out the candidate it names, so a
 * critic asks each principle of every candidate and cannot tell which one he faulted.
 *
 * Refused, with the packet left unwritten:
 *   - a log its own gate refuses (round-log.js, corrections-log.js), as a usage error;
 *   - a round the round log holds no row for, or whose row's project holds a character other than a letter, digit,
 *     _ or -, a source path that does not exist, an empty copy_bans, or a
 *     corrections entry naming a candidate of a packed round that the manifest does not;
 *   - entry-project: a corrections entry naming a packed round's tag under a project no round-log row holds;
 *   - verdict-field: a verdict field name anywhere in the packet, quoted as JSON spells a key, or bare where the
 *     name holds an underscore and so is no English word (`first_pick: v2-slow` in a brief);
 *   - log-line: a row of either log, anywhere in the packet;
 *   - verdict-text: a packed round's reason or a packed entry's words, quoted in that round's own folder. A later
 *     round's brief may quote them, as its Client values quote his words, since its critic reads only its own folder;
 *   - link: a symbolic link inside a candidate folder, which would let a critic read past the packet (a source
 *     that is itself a link is copied as what it points at).
 * A later round's brief delta names the leader the founder picked in an earlier one, which no text check can tell
 * from any other candidate name: a critic re-judging an earlier round reads only that round's folder, which
 * calibration-critic.js confines it to (#168).
 *
 * Exits 0 on a packet written, 1 on a packet refused, 2 on a usage error or an unreadable manifest or log. A vault
 * log that does not exist yet reads as empty; a log path given that does not exist is unreadable.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { parseRows } = require("./log-gate.js");
const roundLog = require("./round-log.js");
const correctionsLog = require("./corrections-log.js");

const ROUND_LOG = "data/round-log.jsonl";
const CORRECTIONS_LOG = "data/corrections-log.jsonl";
// The founder's verdicts in each log's row: every field less what names the round, its asset class, the correction's place, and the
// principle the critics are asked about.
const NOT_VERDICTS = ["date", "project", "asset", "ticket", "round", "where", "candidate", "principle"];
const VERDICT_FIELDS = [...new Set([...roundLog.FIELDS, ...correctionsLog.FIELDS])].filter((f) => !NOT_VERDICTS.includes(f));
const VERDICT_KEY = new RegExp(`"(${VERDICT_FIELDS.join("|")})"\\s*:|\\b(${VERDICT_FIELDS.filter((f) => f.includes("_")).join("|")})\\b`);
const TAG = /^rounds\/([\w.-]+-r([1-9]\d*))$/;
// A candidate's name becomes a path in the packet, so it may not climb out of it.
const NAME = /^(?!\.\.?$)[\w.-]+$/;
const PROJECT = /^[\w-]+$/;

function roundFolder(project, tag) {
  const slug = typeof tag === "string" ? tag.match(TAG) : null;
  return slug && typeof project === "string" && PROJECT.test(project) ? `${project}.${slug[1]}` : null;
}

function parseArgs(argv) {
  const options = { manifest: null, out: null, "round-log": null, "corrections-log": null };
  for (let i = 0; i < argv.length; i++) {
    const name = argv[i].replace(/^--/, "");
    if (!argv[i].startsWith("--") || !(name in options) || !argv[i + 1]) throw new Error(`unknown argument ${JSON.stringify(argv[i])}`);
    options[name] = argv[++i];
  }
  if (!options.manifest || !options.out) throw new Error("--manifest and --out are both needed");
  return options;
}

/** Each round the manifest names, with its folder, logged row and the entries naming its candidates, and the faults in it. */
function planRounds(manifest, base, roundRows, corrections) {
  const faults = [];
  const fault = (rule, message) => faults.push(`${rule}: ${message}`);
  const folders = new Set();
  const rounds = [];
  if (!Array.isArray(manifest.rounds) || manifest.rounds.length === 0) fault("manifest", "rounds is not a list of one or more rounds");
  for (const [index, round] of (Array.isArray(manifest.rounds) ? manifest.rounds : []).entries()) {
    const at = `round ${index + 1}`;
    if (round === null || typeof round !== "object") {
      fault("manifest", `${at}: is not a round object`);
      continue;
    }
    const tag = typeof round.tag === "string" ? round.tag.match(TAG) : null;
    if (!tag || Number(tag[2]) !== round.round) {
      fault("manifest", `${at}: tag ${JSON.stringify(round.tag)} is not rounds/<slug>-r<n> for round ${JSON.stringify(round.round)}`);
      continue;
    }
    const candidates = round.candidates && typeof round.candidates === "object" ? round.candidates : {};
    if (Object.keys(candidates).length === 0) fault("manifest", `${at}: candidates names no candidate`);
    for (const name of Object.keys(candidates)) if (!NAME.test(name)) fault("manifest", `${at}: candidate name ${JSON.stringify(name)} is not a file name`);
    const sources = [["brief", round.brief], ["gate_list", round.gate_list], ["gate_list_then", round.gate_list_then], ["copy_bans", round.copy_bans], ...Object.entries(candidates)];
    for (const [name, source] of sources) {
      if (typeof source !== "string" || !fs.existsSync(path.resolve(base, source)))
        fault("missing", `${at}: ${name}'s source ${JSON.stringify(source)} does not exist`);
    }
    if (typeof round.copy_bans === "string" && fs.existsSync(path.resolve(base, round.copy_bans)) && !fs.readFileSync(path.resolve(base, round.copy_bans), "utf8").trim())
      fault("copy-bans", `${at}: copy_bans's source ${JSON.stringify(round.copy_bans)} is empty — write "none" where the round's critics were given no copy bans`);
    const row = roundRows.find((r) => roundLog.isRowOfRound(r, round));
    if (!row) {
      fault("unlogged", `${at}: the round log holds no row for ${round.ticket} r${round.round}`);
      continue;
    }
    const folder = roundFolder(row.project, round.tag);
    if (!folder) {
      fault("project", `${at}: the round log's project ${JSON.stringify(row.project)} is not a folder name of letters, digits, _ and -`);
      continue;
    }
    if (folders.has(folder)) fault("manifest", `${at}: ${row.project}'s ${round.tag} is packed twice`);
    folders.add(folder);
    const entries = corrections
      .filter(({ row: e }) => correctionsLog.isEntryOfRound(e, row.project, round.tag))
      .map(({ row: e, line }) => ({ line, name: correctionsLog.roundCandidate(e).name, principle: e.principle, words: e.words }));
    for (const { line, name } of entries)
      if (!(name in candidates)) fault("entry-candidate", `${at}: corrections-log line ${line} names ${row.project}'s ${round.tag} ${name}, which the manifest does not pack`);
    rounds.push({ round, folder, row, candidates, entries });
  }
  const projects = new Set(roundRows.map((r) => r.project));
  const tags = new Set(rounds.map(({ round }) => round.tag));
  for (const { row: e, line } of corrections)
    if (tags.has(correctionsLog.roundCandidate(e)?.tag) && !projects.has(e.project))
      fault("entry-project", `corrections-log line ${line} names ${correctionsLog.roundCandidate(e).tag} under project ${JSON.stringify(e.project)}, which no round-log row holds`);
  return { rounds, faults };
}

function writePacket(dir, rounds, base) {
  for (const { round, folder, candidates, entries } of rounds) {
    const into = path.join(dir, folder);
    fs.mkdirSync(path.join(into, "candidates"), { recursive: true });
    const copy = (source, target) => fs.cpSync(path.resolve(base, source), target, { recursive: true, dereference: true });
    copy(round.brief, path.join(into, `brief${path.extname(round.brief)}`));
    copy(round.gate_list, path.join(into, `gate-list${path.extname(round.gate_list)}`));
    copy(round.copy_bans, path.join(into, `copy-bans${path.extname(round.copy_bans)}`));
    for (const [name, source] of Object.entries(candidates)) {
      const isFile = fs.statSync(path.resolve(base, source)).isFile();
      copy(source, path.join(into, "candidates", isFile ? `${name}${path.extname(source)}` : name));
    }
    if (entries.length) {
      const principles = entries.map(({ line, principle }) => ({ entry: line, principle }));
      fs.writeFileSync(path.join(into, "entries.json"), `${JSON.stringify(principles, null, 2)}\n`);
    }
  }
}

/** Every fault in the folder `dir` of the packet at `root`: what it holds that carries a verdict. */
function scanPacket(root, dir, logLines, verdictTexts) {
  const faults = [];
  for (const entry of fs.readdirSync(dir, { recursive: true, withFileTypes: true })) {
    const file = path.join(entry.parentPath, entry.name);
    const rel = path.relative(root, file);
    if (entry.isSymbolicLink()) faults.push(`link: ${rel} is a symbolic link — a critic could read past the packet`);
    if (!entry.isFile()) continue;
    const text = fs.readFileSync(file, "utf8");
    const key = text.match(VERDICT_KEY);
    if (key) faults.push(`verdict-field: ${rel} holds the verdict field ${key[1] ?? key[2]}`);
    for (const { log, line, raw } of logLines)
      if (text.includes(raw)) faults.push(`log-line: ${rel} holds ${log} line ${line}`);
    for (const { what, value } of verdictTexts)
      if (value.trim() !== "" && text.includes(value)) faults.push(`verdict-text: ${rel} quotes ${what}, ${JSON.stringify(value)}`);
  }
  return faults;
}

/** A log's rows, each with its raw line, once its own gate passes it; throws on a log it refuses or cannot read. */
function readLog(file, given, { name, check }) {
  if (!given && !fs.existsSync(file)) return [];
  const text = fs.readFileSync(file, "utf8");
  const faults = check(text);
  if (faults.length) throw new Error(`${name} is refused by its gate — ${faults[0]}`);
  // The gate has passed every line, so no fault is left to report.
  return parseRows(text, () => {}).map((row) => ({ ...row, log: name }));
}

function main(argv) {
  let options, manifest, base, roundRows, correctionRows;
  try {
    options = parseArgs(argv);
    const manifestFile = path.resolve(options.manifest);
    manifest = JSON.parse(fs.readFileSync(manifestFile, "utf8"));
    if (manifest === null || typeof manifest !== "object" || Array.isArray(manifest)) throw new Error(`${options.manifest} is not a manifest object`);
    base = path.dirname(manifestFile);
    const log = (option, vaultPath, gate) => readLog(path.resolve(options[option] ?? path.join(__dirname, vaultPath)), options[option] !== null, gate);
    roundRows = log("round-log", ROUND_LOG, { name: "the round log", check: roundLog.checkRoundLog });
    correctionRows = log("corrections-log", CORRECTIONS_LOG, { name: "the corrections log", check: correctionsLog.checkCorrectionsLog });
    if (fs.existsSync(path.resolve(options.out))) throw new Error(`${options.out} already exists — a packet is written fresh`);
  } catch (error) {
    console.error(`calibration-packet.js: ${error.message.split("\n")[0]}`);
    return 2;
  }
  const out = path.resolve(options.out);
  const refuse = (faults) => {
    console.error(`calibration-packet.js: packet refused — ${faults.length} fault(s)`);
    for (const f of faults) console.error(`  ${f}`);
    return 1;
  };

  const { rounds, faults } = planRounds(manifest, base, roundRows.map(({ row }) => row), correctionRows);
  if (faults.length) return refuse(faults);

  // Written beside --out and moved there only once clean, so a refused packet never stands where a run would read it.
  fs.mkdirSync(path.dirname(out), { recursive: true });
  const staging = fs.mkdtempSync(path.join(path.dirname(out), ".calibration-packet-"));
  try {
    writePacket(staging, rounds, base);
    const leaks = rounds.flatMap(({ round, folder, row, entries }) => {
      const verdictTexts = [
        { what: `${round.ticket} r${round.round}'s reason`, value: row.reason },
        ...entries.map(({ line, words }) => ({ what: `corrections-log line ${line}'s words`, value: words })),
      ];
      return scanPacket(staging, path.join(staging, folder), [...roundRows, ...correctionRows], verdictTexts);
    });
    if (leaks.length) return refuse(leaks);
    fs.renameSync(staging, out);
  } finally {
    fs.rmSync(staging, { recursive: true, force: true });
  }
  const packed = rounds.reduce((n, { entries }) => n + entries.length, 0);
  console.log(`calibration-packet.js: ${path.relative(process.cwd(), out) || out} written — ${rounds.length} round(s), ${packed} corrections entr${packed === 1 ? "y" : "ies"}`);
  return 0;
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));

module.exports = { readLog, roundFolder, ROUND_LOG, CORRECTIONS_LOG };
