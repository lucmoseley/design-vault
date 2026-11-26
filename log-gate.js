"use strict";
const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const { gitIn } = require("./git-read.js");

const isText = (value) => typeof value === "string" && value.trim() !== "";
const isDate = (value) => {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const day = new Date(`${value}T00:00:00Z`);
  return !Number.isNaN(day.getTime()) && day.toISOString().startsWith(value);
};

function parseRows(text, fault) {
  const rows = [];
  text.replace(/^﻿/, "").split("\n").forEach((line, index) => {
    if (line.trim() === "") return;
    try {
      const row = JSON.parse(line);
      if (typeof row !== "object" || row === null || Array.isArray(row)) throw new Error("not a JSON object");
      rows.push({ row, line: index + 1, raw: line.trim() });
    } catch (error) {
      fault("json", `line ${index + 1}: ${error.message}`);
    }
  });
  return rows;
}

function parseArgs(argv, extra = {}) {
  const options = { staged: false, log: null, previous: null };
  for (const [name, times] of Object.entries(extra)) options[name] = times === "many" ? [] : null;
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    const own = arg.slice(2);
    if (arg === "--staged") options.staged = true;
    else if (["--log", "--previous"].includes(arg) && argv[i + 1]) options[own] = argv[++i];
    else if (arg.startsWith("--") && Object.hasOwn(extra, own)) {
      if (!argv[i + 1]) throw new Error(`${arg} takes a value: ${arg} <value>`);
      if (extra[own] === "many") options[own].push(argv[++i]);
      else options[own] = argv[++i];
    } else throw new Error(`unknown argument ${JSON.stringify(arg)}`);
  }
  if (options.staged && (options.log || options.previous)) throw new Error("--staged reads the index's and HEAD's log; it takes no paths");
  return options;
}

function gitLog(root, log, fromHead) {
  const git = gitIn(root);
  if (fromHead) {
    const head = spawnSync("git", ["rev-parse", "--verify", "-q", "HEAD"], { cwd: root, encoding: "utf8" });
    if (head.status === 1) return "";
    if (head.status !== 0) throw new Error(`git rev-parse HEAD failed: ${(head.stderr || "").trim()}`);
    if (git("ls-tree", "--name-only", "HEAD", "--", log).trim() === "") return "";
    return git("show", `HEAD:${log}`);
  }
  if (git("ls-files", "--", log).trim() === "") return "";
  return git("show", `:${log}`);
}

function runGate(argv, { log, name, noun, check, report, extra }) {
  let options;
  try {
    options = parseArgs(argv, extra);
  } catch (error) {
    console.error(`${name}: ${error.message}`);
    return 2;
  }
  const root = __dirname;
  let label, text, previousText;
  try {
    if (options.staged) {
      label = `the staged ${log}`;
      text = gitLog(root, log, false);
      previousText = gitLog(root, log, true);
    } else {
      const file = path.resolve(options.log ?? path.join(root, log));
      label = path.relative(process.cwd(), file) || file;
      text = fs.readFileSync(file, "utf8");
      previousText = options.previous ? fs.readFileSync(path.resolve(options.previous), "utf8") : options.log ? "" : gitLog(root, log, true);
    }
  } catch (error) {
    console.error(`${name}: could not read the log — ${error.message.split("\n")[0]}`);
    return 2;
  }
  const faults = check(text, previousText);
  if (faults.length) {
    console.error(`${name}: ${label} refused — ${faults.length} fault(s)`);
    for (const f of faults) console.error(`  ${f}`);
    return 1;
  }
  const count = text.split("\n").filter((line) => line.trim() !== "").length;
  console.log(`${name}: ${label} is a valid ${noun} — ${count} row(s)`);
  for (const line of report ? report(text, options) : []) console.log(`${name}: ${line}`);
  return 0;
}

module.exports = { isText, isDate, parseRows, runGate };
