#!/usr/bin/env node
/**
 * Usage:
 *   node calibration-score.js --manifest <file> --packet <dir> --answers <dir> --where <text> --row <file>
 *                             [--round-log <file>] [--corrections-log <file>] [--calibration-log <file>]
 *
 * The manifest and packet are calibration-packet.js's. --answers holds canary.json and, for each round folder of the
 * packet, critic-a.json, critic-b.json and critic-c.json, all as calibration-critic.js writes them. Each critic must
 * have run on the model and Claude Code version the canary held on. The manifest must hold every round logged since
 * the last run's round_log_rows and, where fewer than ten were, the last ten logged (every round, where fewer are
 * logged), each with his first pick among its candidates.
 *
 * The critics answer the look questions as the gates stand now, each round's gate_list. His verdicts,
 * from the logs: a round's first pick, which each critic's leader agrees with or not; a gate question worded as in
 * the round's gate_list_then is a Yes on the candidate he picked first, and a No on a candidate an entry names whose ruling is that question's
 * rule; an entry's principle is a Yes on the candidate it names where he kept the trait, a No where he rejected it. Each critic's answer where his verdict is known is
 * counted: agreeing, Unsure, or a disagreement, listed with the question, lens or unlanded rule it turned on. A
 * question added or reworded since the round tests the rule, not the critic: the critics' answers on his first pick
 * are counted apart, in new_questions, and each No is printed as a pick of his the new rule would fail. The row also
 * sums the rounds' splits and settled from the round log, how often the settle step settled a split, and the
 * report says how many of the rounds carried those counts.
 *
 * Prints the result for the founder and writes the row to --row, once calibration-log.js passes it after the
 * calibration log's rows; the session appends it there. Exits 0 on a row written, 1 on answers or a row refused, 2 on
 * bad usage or an unreadable file.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { readLog, roundFolder, ROUND_LOG, CORRECTIONS_LOG } = require("./calibration-packet.js");
const roundLog = require("./round-log.js");
const correctionsLog = require("./corrections-log.js");
const { roundAsked, answerFaults, questionTexts } = require("./calibration-critic.js");
const { checkCalibrationLog, CRITICS } = require("./calibration-log.js");

const CALIBRATION_LOG = "data/calibration-log.jsonl";
const RULE = /^rule: (\S+)$/;
const roundName = ({ ticket, round }) => `${ticket} r${round}`;

function parseArgs(argv) {
  const options = { manifest: null, packet: null, answers: null, where: null, row: null, "round-log": null, "corrections-log": null, "calibration-log": null };
  for (let i = 0; i < argv.length; i++) {
    const name = argv[i].replace(/^--/, "");
    if (!argv[i].startsWith("--") || !(name in options) || !argv[i + 1]) throw new Error(`unknown argument ${JSON.stringify(argv[i])}`);
    options[name] = argv[++i];
  }
  const missing = ["manifest", "packet", "answers", "where", "row"].filter((k) => !options[k]);
  if (missing.length) throw new Error(`--${missing.join(", --")} needed`);
  return options;
}

const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const figure = () => ({ agree: 0, of: 0, unsure: 0 });

function count(fig, answer, expected) {
  fig.of++;
  if (answer === expected) fig.agree++;
  else if (answer === "unsure") fig.unsure++;
  else return true;
  return false;
}

function score(rounds) {
  const pick = { agree: 0, of: 0 };
  const questions = {};
  const entries = {};
  const newQuestions = {};
  const critics = CRITICS.map(() => ({ unsure: 0, answers: 0 }));
  const disagreements = [];
  const failedPicks = [];
  for (const { name, asked, unchanged, row, entries: named, critics: given } of rounds) {
    const known = [];
    const know = (candidate, q, expected) => {
      const at = known.findIndex((k) => k.candidate === candidate && k.q === q);
      known.splice(at < 0 ? known.length : at, at < 0 ? 0 : 1, { candidate, q, expected });
    };
    if (row.first_pick !== null) for (const q of unchanged) know(row.first_pick, q, "yes");
    for (const e of named) {
      const rule = e.ruling.match(RULE);
      if (rule && asked.questions.includes(rule[1])) know(e.candidate, rule[1], e.expected);
    }
    for (const q of asked.questions) questions[q] ??= figure();
    const ruleTests = row.first_pick === null ? [] : asked.questions.filter((q) => !unchanged.includes(q) && !known.some((k) => k.candidate === row.first_pick && k.q === q));
    given.forEach((data, i) => {
      const critic = CRITICS[i];
      for (const section of ["answers", "principles"])
        for (const byKey of Object.values(data[section]))
          for (const a of Object.values(byKey)) {
            critics[i].answers++;
            if (a.answer === "unsure") critics[i].unsure++;
          }

      pick.of++;
      if (data.leader.candidate === row.first_pick) pick.agree++;
      else disagreements.push({ kind: "pick", round: name, critic, founder: row.first_pick, leader: data.leader.candidate, turned_on: data.leader.turned_on });

      for (const q of ruleTests) {
        const { answer, evidence } = data.answers[row.first_pick][q];
        newQuestions[q] ??= { yes: 0, no: 0, unsure: 0 };
        newQuestions[q][answer]++;
        if (answer === "no") failedPicks.push({ round: name, critic, candidate: row.first_pick, on: q, evidence });
      }
      for (const { candidate, q, expected } of known) {
        const { answer, evidence } = data.answers[candidate][q];
        if (count(questions[q], answer, expected)) disagreements.push({ kind: "question", round: name, critic, candidate, on: q, founder: expected, answer, evidence });
      }
      for (const e of named) {
        const { answer, evidence } = data.principles[e.candidate][String(e.line)];
        entries[e.line] ??= figure();
        if (count(entries[e.line], answer, e.expected))
          disagreements.push({ kind: "entry", round: name, critic, candidate: e.candidate, on: e.line, principle: e.principle, rule: correctionsLog.LANDED.test(e.ruling) ? e.ruling : "unlanded", founder: e.expected, answer, evidence });
      }
    });
  }
  return { figures: { pick, questions, entries, new_questions: newQuestions, critics, disagreements }, failedPicks };
}

function wilson(agree, of) {
  const z = 1.96;
  const p = agree / of;
  const centre = (p + (z * z) / (2 * of)) / (1 + (z * z) / of);
  const half = (z * Math.sqrt((p * (1 - p)) / of + (z * z) / (4 * of * of))) / (1 + (z * z) / of);
  return `${Math.round(100 * Math.max(0, centre - half))}–${Math.round(100 * Math.min(1, centre + half))}%`;
}

function report(row, failedPicks, counted) {
  const sum = (figs) => Object.values(figs).reduce((t, f) => ({ agree: t.agree + f.agree, of: t.of + f.of, unsure: t.unsure + f.unsure }), figure());
  const line = (what, { agree, of, unsure }) =>
    of ? `${what}: ${agree} of ${of} agree (${Math.round((100 * agree) / of)}%, likely ${wilson(agree, of)})${unsure ? `, ${unsure} Unsure` : ""}` : `${what}: none of his verdicts to compare`;
  const { splits, settled } = row.settles;
  const settle = splits ? `settled ${settled} of ${splits} splits (${Math.round((100 * settled) / splits)}%, likely ${wilson(settled, splits)}).` : "no split logged in these rounds.";
  const out = [
    `Calibration of ${row.rounds.length} round(s), three critics on ${row.model}, confined (canary held on Claude Code ${row.canary_held_on}).`,
    line("Leader picks", { ...row.pick, unsure: 0 }),
    line("Gate questions", sum(row.questions)),
    ...Object.entries(row.questions).filter(([, f]) => f.of).map(([id, f]) => `  ${line(id, f)}`),
    line("Corrections entries", sum(row.entries)),
    `Unsure answers: ${row.critics.map((c, i) => `critic ${CRITICS[i]} ${c.unsure} of ${c.answers}`).join(", ")}.`,
    `Settle step: ${settle} ${counted} of ${row.rounds.length} round(s) carried the counts.`,
    `Disagreements: ${row.disagreements.length}.`,
  ];
  for (const d of row.disagreements) {
    if (d.kind === "pick") out.push(`- ${d.round}, critic ${d.critic}: led ${d.leader ?? "none"} where he picked ${d.founder ?? "none"}, on ${d.turned_on}`);
    else if (d.kind === "question") out.push(`- ${d.round}, critic ${d.critic}: ${d.candidate} ${d.answer === "no" ? "fails" : "passes"} ${d.on}, where he ${d.founder === "yes" ? "picked it first" : "ruled it fails"} — ${d.evidence}`);
    else out.push(`- ${d.round}, critic ${d.critic}: ${d.candidate} ${d.answer === "yes" ? "holds" : "breaks"} "${d.principle}" (corrections-log line ${d.on}, ${d.rule === "unlanded" ? "an unlanded rule" : d.rule}), where he ${d.founder === "yes" ? "kept it" : "faulted it"} — ${d.evidence}`);
  }
  const tested = Object.entries(row.new_questions);
  if (tested.length) {
    out.push("Questions added or reworded since their rounds, tested against his first picks (the rule, not the critics):");
    for (const [id, n] of tested) out.push(`  ${id}: ${n.yes} Yes, ${n.no} No, ${n.unsure} Unsure`);
    for (const f of failedPicks) out.push(`- ${f.round}, critic ${f.critic}: ${f.candidate}, his first pick, fails ${f.on} — ${f.evidence}`);
  }
  return out.join("\n");
}

function main(argv) {
  let options, rounds, row, previous, failedPicks, counted;
  try {
    options = parseArgs(argv);
    const log = (option, vaultPath, gate) => readLog(path.resolve(options[option] ?? path.join(__dirname, vaultPath)), options[option] !== null, gate);
    const roundRows = log("round-log", ROUND_LOG, { name: "the round log", check: roundLog.checkRoundLog });
    const corrections = log("corrections-log", CORRECTIONS_LOG, { name: "the corrections log", check: correctionsLog.checkCorrectionsLog });
    const calibrationFile = path.resolve(options["calibration-log"] ?? path.join(__dirname, CALIBRATION_LOG));
    previous = options["calibration-log"] || fs.existsSync(calibrationFile) ? fs.readFileSync(calibrationFile, "utf8") : "";
    const canary = readJson(path.join(options.answers, "canary.json"));
    if (canary.held !== true) throw new Error(`the canary did not hold (${canary.verdict}) — no critic of this run may be scored; run calibration-critic.js --packet again once the confinement is fixed`);

    const faults = [];
    const lastRun = previous.trim() ? JSON.parse(previous.trim().split("\n").at(-1)).round_log_rows : 0;
    const judged = readJson(options.manifest).rounds.map(roundName);
    const owedFrom = Math.min(lastRun, Math.max(0, roundRows.length - roundLog.CALIBRATION_EVERY));
    roundRows.slice(owedFrom).forEach(({ row: x }, i) => {
      if (judged.includes(roundName(x))) return;
      faults.push(owedFrom + i >= lastRun
        ? `the manifest leaves out ${roundName(x)}, logged since the last run — this run would mark it calibrated unjudged`
        : `the manifest leaves out ${roundName(x)}, one of the last ${roundLog.CALIBRATION_EVERY} rounds logged, which a run due with fewer new rounds re-judges — add it to the manifest`);
    });
    rounds = readJson(options.manifest).rounds.map((r) => {
      const name = roundName(r);
      const logged = roundRows.find(({ row: x }) => roundLog.isRowOfRound(x, r));
      if (!logged) throw new Error(`the round log holds no row for ${name}`);
      const folder = roundFolder(logged.row.project, r.tag);
      if (!folder) throw new Error(`${name}: ${JSON.stringify(logged.row.project)}'s ${JSON.stringify(r.tag)} names no packet folder — build the packet with calibration-packet.js`);
      const asked = roundAsked(path.join(options.packet, folder));
      let unchanged = [];
      if (typeof r.gate_list_then !== "string")
        faults.push(`${name}: the manifest names no gate_list_then, the look questions of the round's time, which his first pick is scored on (#232)`);
      else {
        const then = questionTexts(fs.readFileSync(path.resolve(path.dirname(options.manifest), r.gate_list_then), "utf8"));
        unchanged = asked.questions.filter((q) => then.get(q) === asked.texts.get(q));
      }
      const entries = corrections
        .filter(({ row: e }) => correctionsLog.isEntryOfRound(e, logged.row.project, r.tag))
        .map(({ row: e, line }) => ({ line, candidate: correctionsLog.roundCandidate(e).name, principle: e.principle, ruling: e.ruling, expected: e.stance === "kept" ? "yes" : "no" }));
      if (logged.row.first_pick !== null && !asked.candidates.includes(logged.row.first_pick))
        faults.push(`${name}: his first pick ${logged.row.first_pick} is not one of the packet's candidates — add it to the manifest`);
      const critics = CRITICS.map((c) => {
        const file = path.join(options.answers, folder, `critic-${c}.json`);
        if (!fs.existsSync(file)) throw new Error(`${file} does not exist — run calibration-critic.js --packet for the whole run`);
        const data = readJson(file);
        const at = path.relative(process.cwd(), file) || file;
        for (const f of answerFaults(asked, data)) faults.push(`${at}: ${f}`);
        if (data.run?.round !== folder) faults.push(`${at}: answers round ${JSON.stringify(data.run?.round)}, not ${folder}`);
        if (data.run?.model !== canary.model || data.run?.claude_code !== canary.claude_code)
          faults.push(`${at}: ran on ${data.run?.model} and Claude Code ${data.run?.claude_code}, and the canary held on ${canary.model} and ${canary.claude_code}`);
        return data;
      });
      return { name, asked, unchanged, row: logged.row, entries, critics };
    });
    if (faults.length) {
      console.error(`calibration-score.js: answers refused — ${faults.length} fault(s)`);
      for (const f of faults) console.error(`  ${f}`);
      return 1;
    }
    const scored = score(rounds);
    failedPicks = scored.failedPicks;
    counted = rounds.filter((r) => "splits" in r.row).length;
    row = {
      date: new Date().toISOString().slice(0, 10),
      round_log_rows: roundRows.length,
      model: canary.model,
      canary_held_on: canary.claude_code,
      rounds: rounds.map(({ name }) => name),
      ...scored.figures,
      settles: Object.fromEntries(["splits", "settled"].map((key) => [key, rounds.reduce((t, r) => t + (r.row[key] ?? 0), 0)])),
      where: options.where,
    };
  } catch (error) {
    console.error(`calibration-score.js: ${error.message.split("\n")[0]}`);
    return 2;
  }
  const line = JSON.stringify(row);
  const faults = checkCalibrationLog(`${previous}${previous && !previous.endsWith("\n") ? "\n" : ""}${line}\n`, previous);
  if (faults.length) {
    console.error(`calibration-score.js: the row is refused by calibration-log.js — ${faults.length} fault(s)`);
    for (const f of faults) console.error(`  ${f}`);
    return 1;
  }
  fs.writeFileSync(options.row, `${line}\n`);
  console.log(report(row, failedPicks, counted));
  return 0;
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));
