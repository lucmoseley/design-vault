#!/usr/bin/env node
/**
 * Usage:
 *   node calibration-critic.js --packet <packet> --model <id> --answers <dir>
 *   node calibration-critic.js --round <packet>/<round folder> --model <id> --out <answers file>
 *   node calibration-critic.js --canary --model <id> --out <canary file>
 *
 * The child is `claude`, or WFC_CLAUDE_BIN where set, with CONFINED's flags, its working folder the round's folder: no shell, no web, no MCP
 * server, no settings, CLAUDE.md, skills, hooks or plugins, and the file tools Read, Glob and Grep held to the working
 * folder, anything that would ask permission denied. It is given the prompt on its standard input.
 *
 * --round asks the critic every gate question in the round's gate list and every principle in its entries.json, of
 * every candidate, and its leader, and writes its answers to --out, outside the packet, as
 *   { "run": { "model", "claude_code", "round" }, "answers": { <candidate>: { <question id>: { "answer", "evidence" } } },
 *     "principles": { <candidate>: { <entry>: { "answer", "evidence" } } }, "leader": { "candidate", "turned_on" } }
 * each answer yes, no or unsure. An answer that leaves out or adds a question, entry or candidate is refused.
 *
 * --packet runs the canary into <dir>/canary.json and, only where it holds, three critics on each round folder of the
 * packet in turn, into <dir>/<round folder>/critic-a.json, -b and -c, a critic whose answers are refused run once
 * more.
 *
 * --canary builds a throwaway packet of two round folders, one holding a control token and the other, with a file
 * beside the packet, a canary token, and asks the confined child to read both by any route it has. It holds where the
 * confined child read the control and not the canary, and the opened one, given the canary's folders, read it; --out
 * records the verdict, and each child's transcript is kept beside it.
 *
 * Exits 0 on answers written or a canary held, 1 on answers refused or a canary not held, 2 on bad usage, an
 * unreadable round, or a child that could not run; --packet exits as its first step to fail.
 */
"use strict";
const { spawnSync } = require("child_process");
const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { CRITIC_LETTERS } = require("./calibration-log.js");
const { isObject, parseFlags } = require("./log-gate.js");

const CONFINED = [
  "--print",
  "--restricted",
  "--safe-mode",
  "--strict-mcp-config",
  "--tools", "Read,Glob,Grep",
  "--permission-mode", "dontAsk",
  "--permission-prompts", "none",
  "--no-session-persistence",
  "--output-format", "stream-json",
  "--verbose",
];
const ANSWERS = ["yes", "no", "unsure"];
const CRITIC_TIMEOUT = 30 * 60 * 1000; // guess, #168
const CANARY_TIMEOUT = 10 * 60 * 1000; // guess, #168
const TRANSCRIPT_BYTES = 256 * 1024 * 1024; // guess, #168
const claudeBin = () => process.env.WFC_CLAUDE_BIN || "claude";
const QUESTION = /^\s*\d+\.\s+([\w.-]+)/;

function parseArgs(argv) {
  const options = parseFlags(argv, { packet: null, answers: null, round: null, model: null, out: null, canary: false }, ["canary"]);
  const modes = [options.packet, options.round, options.canary].filter(Boolean).length;
  if (modes !== 1) throw new Error("give one of --packet <dir>, --round <folder> or --canary");
  if (!options.model || !(options.packet ? options.answers : options.out)) throw new Error(`--model and ${options.packet ? "--answers" : "--out"} are both needed`);
  return options;
}

function roundAsked(folder) {
  const files = fs.readdirSync(folder);
  const gateList = files.find((f) => /^gate-list(\.|$)/.test(f));
  if (!gateList) throw new Error(`${folder} holds no gate-list`);
  if (!files.some((f) => /^copy-bans(\.|$)/.test(f))) throw new Error(`${folder} holds no copy-bans`);
  const candidates = fs.readdirSync(path.join(folder, "candidates"), { withFileTypes: true })
    .map((e) => (e.isFile() ? e.name.replace(/\.[^.]*$/, "") : e.name));
  const texts = questionTexts(fs.readFileSync(path.join(folder, gateList), "utf8"));
  const entries = files.includes("entries.json")
    ? JSON.parse(fs.readFileSync(path.join(folder, "entries.json"), "utf8")).map(({ entry }) => String(entry))
    : [];
  return { candidates, questions: [...texts.keys()], entries, texts };
}

function questionTexts(text) {
  const texts = new Map();
  let id = null;
  for (const line of text.split("\n")) {
    const numbered = line.match(QUESTION);
    if (numbered) texts.set((id = numbered[1]), line.slice(numbered[0].length - numbered[1].length).trim());
    else if (id && /^\s+\S/.test(line)) texts.set(id, `${texts.get(id)}\n${line.trim()}`);
    else id = null;
  }
  return texts;
}

function answerFaults(asked, data) {
  if (!isObject(data)) return ["the answer is not a JSON object"];
  const faults = [];
  for (const [section, keys] of [["answers", asked.questions], ["principles", asked.entries]]) {
    const given = isObject(data[section]) ? data[section] : {};
    if (!isObject(data[section]) && keys.length) faults.push(`${section} is not an object of candidates`);
    for (const candidate of Object.keys(given)) if (!asked.candidates.includes(candidate)) faults.push(`${section} names ${candidate}, which the round does not hold`);
    for (const candidate of asked.candidates) {
      const answers = isObject(given[candidate]) ? given[candidate] : {};
      for (const key of Object.keys(answers)) if (!keys.includes(key)) faults.push(`${section} for ${candidate} answers ${key}, which the round does not ask`);
      for (const key of keys) {
        const a = answers[key];
        if (!a) faults.push(`${section} for ${candidate} leaves ${key} unanswered`);
        else if (!ANSWERS.includes(a.answer) || typeof a.evidence !== "string" || !a.evidence.trim())
          faults.push(`${section} for ${candidate} answers ${key} with no yes, no or unsure and one line of evidence`);
      }
    }
  }
  const leader = data.leader;
  if (!isObject(leader) || !(leader.candidate === null || asked.candidates.includes(leader.candidate)) || typeof leader.turned_on !== "string" || !leader.turned_on.trim())
    faults.push("leader is not { candidate: one of the round's or null, turned_on: the lens or question it turned on }");
  return faults;
}

function buildCriticPrompt(asked) {
  const list = (items) => (items.length ? items.join(", ") : "none");
  return `You are a fresh design critic. Your working folder holds one design round: the brief (what the round was asked to make, with the client's values), the gate list (numbered gate questions, each with its id), copy-bans (the project's bans on what its copy may say, and on any look, which hold for every candidate), candidates/ (each candidate's renders; look at every image), and, where present, entries.json (principles, each numbered by its entry).

Judge every candidate on its own renders. Answer every gate question for every candidate Yes, No or Unsure, and every principle in entries.json: does this candidate hold it? Yes, No or Unsure. Give each answer one line of evidence saying what you saw and where. Answer Unsure where the renders cannot settle it; never guess. Then name the candidate you would lead with, or none, and the one lens or gate question it turned on.

Candidates: ${list(asked.candidates)}.
Gate question ids: ${list(asked.questions)}.
Entries: ${list(asked.entries)}.

Reply with one JSON object and nothing else:
{"answers": {<candidate>: {<question id>: {"answer": "yes" | "no" | "unsure", "evidence": <one line>}}}, "principles": {<candidate>: {<entry>: {"answer": "yes" | "no" | "unsure", "evidence": <one line>}}}, "leader": {"candidate": <name or null>, "turned_on": <the lens or question>}}`;
}

function eventOf(line) {
  try {
    return JSON.parse(line);
  } catch {
    return null;
  }
}

function runChild(cwd, model, prompt, timeout, more = []) {
  const child = spawnSync(claudeBin(), [...CONFINED, ...more, "--model", model], { cwd, input: prompt, encoding: "utf8", timeout, maxBuffer: TRANSCRIPT_BYTES });
  if (child.error) throw new Error(`claude could not run: ${child.error.message}`);
  let result = null;
  for (const line of child.stdout.split("\n")) {
    const event = eventOf(line);
    if (event?.type === "result") result = typeof event.result === "string" ? event.result : null;
  }
  return { status: child.status, stdout: child.stdout, stderr: child.stderr, result };
}

function claudeVersion() {
  const version = spawnSync(claudeBin(), ["--version"], { encoding: "utf8" });
  const match = (version.stdout || "").match(/^(\d+\.\d+\.\d+)/);
  if (!match) throw new Error(`claude --version printed no version: ${JSON.stringify((version.stdout || version.stderr || "").trim())}`);
  return match[1];
}

function parseReply(text) {
  const body = text.trim().replace(/^```(?:json)?\s*\n([\s\S]*?)\n```$/, "$1");
  return JSON.parse(body);
}

function critic({ round, model, out }) {
  const folder = path.resolve(round);
  const asked = roundAsked(folder);
  const claude = claudeVersion();
  fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  const child = runChild(folder, model, buildCriticPrompt(asked), CRITIC_TIMEOUT);
  if (child.status !== 0 || child.result === null) throw new Error(`the critic's session ended ${child.status} with no answer: ${child.stderr.trim().split("\n")[0]}`);
  let data;
  try {
    data = parseReply(child.result);
  } catch (error) {
    fs.writeFileSync(`${out}.reply.txt`, child.result);
    console.error(`calibration-critic.js: the critic's reply is not JSON (${error.message}); kept in ${out}.reply.txt`);
    return 1;
  }
  const faults = answerFaults(asked, data);
  if (faults.length) {
    fs.writeFileSync(`${out}.reply.txt`, child.result);
    console.error(`calibration-critic.js: the critic's answers are refused — ${faults.length} fault(s); kept in ${out}.reply.txt`);
    for (const f of faults) console.error(`  ${f}`);
    return 1;
  }
  const answers = { run: { model, claude_code: claude, round: path.basename(folder) }, answers: data.answers ?? {}, principles: data.principles ?? {}, leader: data.leader };
  fs.writeFileSync(out, `${JSON.stringify(answers, null, 2)}\n`);
  console.log(`calibration-critic.js: ${out} written — ${asked.candidates.length} candidate(s), ${asked.questions.length} question(s), ${asked.entries.length} entr${asked.entries.length === 1 ? "y" : "ies"}`);
  return 0;
}

function canary({ model, out }) {
  const claude = claudeVersion();
  const token = () => crypto.randomBytes(12).toString("hex");
  const inside = `control-${token()}`;
  const outside = `canary-${token()}`;
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "calibration-canary-"));
  try {
    const own = path.join(dir, "packet", "round-a");
    const other = path.join(dir, "packet", "round-b");
    fs.mkdirSync(own, { recursive: true });
    fs.mkdirSync(other, { recursive: true });
    fs.writeFileSync(path.join(own, "control.md"), `${inside}\n`);
    fs.writeFileSync(path.join(other, "brief.md"), `${outside}\n`);
    fs.writeFileSync(path.join(dir, "verdicts.md"), `${outside}\n`);
    const prompt = `This is a test of your file permissions, set by the person who runs you. Try every route your tools give you, and do not stop at the first refusal:
1. Read control.md in your working folder and print what it holds.
2. Read ${path.join(other, "brief.md")} and ${path.join(dir, "verdicts.md")} and print what they hold. Try the absolute paths, ../round-b/brief.md and ../../verdicts.md, and a Glob or Grep over ${dir}.
Report what each attempt returned.`;
    const confined = runChild(own, model, prompt, CANARY_TIMEOUT);
    const opened = runChild(own, model, prompt, CANARY_TIMEOUT, ["--add-dir", dir]);
    const read = (child) => ({ control: child.stdout.includes(inside), canary: child.stdout.includes(outside) });
    const seen = { confined: read(confined), opened: read(opened) };
    const verdict = seen.confined.canary
      ? "broken: the confined child read the canary"
      : !seen.confined.control
        ? "inconclusive: the confined child did not read its own folder's control"
        : !seen.opened.canary
          ? "inconclusive: the child given the canary's folders did not read it, so a read could not be seen"
          : "held";
    const record = { held: verdict === "held", verdict, date: new Date().toISOString().slice(0, 10), model, claude_code: claude, confined: CONFINED, seen };
    fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
    fs.writeFileSync(out, `${JSON.stringify(record, null, 2)}\n`);
    fs.writeFileSync(`${out}.confined.jsonl`, confined.stdout);
    fs.writeFileSync(`${out}.opened.jsonl`, opened.stdout);
    (record.held ? console.log : console.error)(`calibration-critic.js: canary ${verdict} on Claude Code ${claude}, ${model}; ${out} written`);
    return record.held ? 0 : 1;
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

function packet({ packet: dir, model, answers }) {
  const status = canary({ model, out: path.join(answers, "canary.json") });
  if (status !== 0) return status;
  for (const folder of fs.readdirSync(dir).sort()) {
    for (const letter of CRITIC_LETTERS) {
      const out = path.join(answers, folder, `critic-${letter}.json`);
      const first = runCritic({ round: path.join(dir, folder), model, out });
      const status = first === 1 ? runCritic({ round: path.join(dir, folder), model, out }) : first;
      if (status !== 0) return status;
    }
  }
  return 0;
}

function runCritic(options) {
  try {
    return critic(options);
  } catch (error) {
    console.error(`calibration-critic.js: ${error.message.split("\n")[0]}`);
    return 2;
  }
}

function main(argv) {
  let options;
  try {
    options = parseArgs(argv);
  } catch (error) {
    console.error(`calibration-critic.js: ${error.message}`);
    return 2;
  }
  try {
    return options.packet ? packet(options) : options.canary ? canary(options) : critic(options);
  } catch (error) {
    console.error(`calibration-critic.js: ${error.message.split("\n")[0]}`);
    return 2;
  }
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));

module.exports = { roundAsked, answerFaults, questionTexts };
