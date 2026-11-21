#!/usr/bin/env node
/**
 * fall.js — computes a fall that ends in a damped landing, or a heavy settle, and
 * samples it to a CSS `linear()` easing: the fall of gate question vault.flow-code (design-vault#68)
 * and settle (#105); and checks every fall in a timeline table against them (#333).
 *
 * The fall is y = ½gt² from rest at one stated scale, g = 9.80665 m/s². At
 * impact a spring takes over at the impact speed: critically damped at
 * --damping 1 (the default), more heavily damped above 1. It carries the
 * element --sink px past its rest point and settles back, so a smaller sink is
 * a harder landing. Like a settle, it is aimed just past rest on its way back,
 * so that it arrives there as its speed falls to check-flow.py's still speed,
 * leaving no still tail (#152): the lower of its still share of the impact speed
 * and the slowest speed seen as motion from --view-cm (60) away (#196).
 *
 * The easing runs from the start (0) to the rest point (1), and dips past 1
 * during the landing. Animate the whole drop with it, for the duration it
 * prints: `el.animate([{ transform: "none" }, { transform: "translateY(240px)" }],
 * { duration, easing })`. Its stops keep the played path within --tolerance px
 * (0.02) of the true one, plus the rounding of each stop (progress to 6
 * decimals, time to 4 decimals of a percent), and the true speed within
 * 1.15-fold across each span of 1 ms or more, so check-flow.py finds no speed
 * step in it (#151, #196).
 *
 * A settle is a spring released from rest --settle px from its rest point. Its
 * stiffness is solved so that its speed falls to check-flow.py's still speed
 * at --ms, the length the brief gives, and it is aimed just past
 * rest so that it arrives there at that moment (#142). Its stops keep the same
 * two bounds. Its easing runs 0 to 1 and never passes 1.
 *
 * Exits 0 with the result, 2 on bad usage.
 *
 * --check reads a timeline table in design-round §6's form and recomputes
 * every fall in it, gate question vault.fall-script (#333). A fall is an easing
 * whose arguments name `drop`: a spring sink when they name `sink` too, else a
 * thud, which takes `drop` and `scale` alone. A spring sink's CSS must be the
 * `linear()` this script prints for its arguments, character for character. A
 * thud's must be a `cubic-bezier()` whose path stays within DEFAULT_TOLERANCE px
 * of y = ½gt² over its drop, as `cubic-bezier(1/3, 0, 2/3, 1/3)` is exactly.
 * Every cue on a fall's easing must last its duration, within LENGTH_MS.
 * --landing is the motion brief's pick, and a fall landing the other way is a
 * fault; with none, each fall's landing is listed for the founder.
 *
 * Exits 0 every fall matches / 1 one or more differ, each printed / 2 bad usage,
 * or a table it cannot read / 6 none differs but a fall cannot be recomputed,
 * its scale missing. It needs only Node, so it never exits 3. Exits 0, 1 and 6
 * print on stdout, the rest on stderr.
 */
"use strict";

const fs = require("node:fs");
const { fall, thud, thudStray, settle, css, joltLine, jumpPx, DEFAULT_TOLERANCE, VIEW_CM, FRAME_MS } = require("./fall-motion.js");

const USAGE = `usage: node fall.js --drop PX --scale PX_PER_M --sink PX [--damping Z] [--tolerance PX] [--view-cm CM] [--json]
       node fall.js --settle PX --ms MS [--damping Z] [--tolerance PX] [--view-cm CM] [--json]
       node fall.js --check TABLE [--landing thud|sink]`;

// Each flag that takes a number, and the key it sets.
const FLAGS = { "--drop": "drop", "--scale": "scale", "--sink": "sink", "--settle": "distance", "--ms": "ms", "--damping": "damping", "--tolerance": "tolerance", "--view-cm": "viewCm" };
const FLAG_OF = Object.fromEntries(Object.entries(FLAGS).map(([f, k]) => [k, f]));
// A fall's easing names a fall's flags, less the dashes; a thud names drop and scale alone.
const FALL_ARGS = Object.fromEntries(["--drop", "--scale", "--sink", "--damping", "--tolerance", "--view-cm"].map((f) => [f.slice(2), FLAGS[f]]));
const THUD_ARGS = ["drop", "scale"];
// The table states each length to 1 ms (design-round §6), so a cue within half
// of that of its fall's duration rounds to it.
const LENGTH_MS = 0.5;
// Untraced: a first guess, not measured. A thud's cubic-bezier() is compared with t² at this many points.
const THUD_POINTS = 200;
const CUE_HEAD = ["Cue", "Element", "Start (s)", "Length (s)", "Easing", "To"];
const EASING_HEAD = ["Easing", "CSS"];

/** Throws, naming the flag, where one of `wanted` or a tolerance, view distance or damping given breaks its bound. */
function checkBounds(at, wanted, kind) {
  for (const k of [...wanted, "tolerance", "viewCm"]) {
    if ((wanted.includes(k) || k in at) && !(at[k] > 0)) throw new Error(`${FLAG_OF[k]} wants a number above 0`);
  }
  if ("damping" in at && !(at.damping >= 1)) throw new Error(`--damping wants 1 (critical) or more; under 1 the ${kind === "settle" ? "settle overshoots" : "landing bounces"}`);
}

/** The rows of every markdown table in `text`, each table as { head, rows }, its cells trimmed. */
function parseTables(text) {
  const out = [];
  const cells = (line) => line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
  const lines = text.split(/\r?\n/);
  for (let i = 0; i + 1 < lines.length; i++) {
    if (!lines[i].trim().startsWith("|") || !/^\s*\|[\s|:-]+\|\s*$/.test(lines[i + 1])) continue;
    const table = { head: cells(lines[i]), rows: [] };
    for (i += 2; i < lines.length && lines[i].trim().startsWith("|"); i++) table.rows.push({ line: i + 1, cells: cells(lines[i]) });
    out.push(table);
  }
  return out;
}

/** The cue and easing tables of a timeline table; throws where either is missing or a row will not read. */
function parseTable(text) {
  const all = parseTables(text);
  const find = (head) => all.find((t) => t.head.join("|") === head.join("|"));
  const cueTable = find(CUE_HEAD);
  const easingTable = find(EASING_HEAD);
  if (!cueTable) throw new Error(`no cue table: its head row must be | ${CUE_HEAD.join(" | ")} |`);
  if (!easingTable) throw new Error(`no easing table: its head row must be | ${EASING_HEAD.join(" | ")} |`);
  const easings = new Map();
  for (const { line, cells } of easingTable.rows) {
    if (cells.length !== 2) throw new Error(`line ${line}: an easing row has ${cells.length} cells, not 2; no cell may hold a |`);
    const named = cells[0].match(/^(.+?)(?: \((.*)\))?$/);
    if (!named) throw new Error(`line ${line}: an easing row names no easing`);
    const args = {};
    for (const pair of named[2] ? named[2].split(", ") : []) {
      const kv = pair.match(/^(\S+) (\S+)$/);
      if (!kv || !Number.isFinite(Number(kv[2]))) throw new Error(`line ${line}: argument "${pair}" is not a name and a number`);
      args[kv[1]] = Number(kv[2]);
    }
    const code = cells[1].match(/^`([^`]+)`$/);
    easings.set(named[1], { name: named[1], args, css: code ? code[1] : cells[1], line });
  }
  const cues = cueTable.rows.map(({ line, cells }) => {
    if (cells.length !== CUE_HEAD.length) throw new Error(`line ${line}: a cue row has ${cells.length} cells, not ${CUE_HEAD.length}; no cell may hold a |`);
    const length = Number(cells[3]);
    if (cells[3] === "" || !Number.isFinite(length)) throw new Error(`line ${line}: length "${cells[3]}" is not a number of seconds`);
    if (cells[4] !== "step" && !easings.has(cells[4])) throw new Error(`line ${line}: cue "${cells[0]}" uses easing "${cells[4]}", which the easing table does not hold`);
    return { name: cells[0], easing: cells[4], ms: length * 1000, line };
  });
  return { easings, cues };
}

function thudFault(easing) {
  const m = easing.css.match(/^cubic-bezier\(([^)]*)\)$/);
  const points = m ? m[1].split(",").map((v) => Number(v.trim())) : [];
  if (points.length !== 4 || !points.every(Number.isFinite)) return "its CSS is not a cubic-bezier(), so it is not the fall's t²; write cubic-bezier(0.333333, 0, 0.666667, 0.333333)";
  if (points[0] < 0 || points[0] > 1 || points[2] < 0 || points[2] > 1) return "its cubic-bezier() x values fall outside 0 to 1; write cubic-bezier(0.333333, 0, 0.666667, 0.333333)";
  const stray = thudStray(points, easing.args.drop, THUD_POINTS);
  // The bound a linear() fall keeps its played path within, so both landing forms answer to one (#333).
  if (stray > DEFAULT_TOLERANCE) return `its ${easing.css} strays ${stray.toFixed(3)} px from the fall's t² over its ${easing.args.drop} px drop, past ${DEFAULT_TOLERANCE} px; write cubic-bezier(0.333333, 0, 0.666667, 0.333333)`;
  return null;
}

/** Each fall's findings in a parsed table: { faults, unmeasured, landings, checked }. */
function checkTable({ easings, cues }, landing) {
  const faults = [];
  const unmeasured = [];
  const landings = [];
  // Residual: an easing naming no drop is no fall to this check, so a fall written with no arguments goes
  // unseen here and is vault.flow-code's.
  const falls = [...easings.values()].filter((e) => "drop" in e.args);
  for (const e of falls) {
    const sink = "sink" in e.args;
    const form = sink ? "a spring sink" : "a thud";
    const wrong = Object.keys(e.args).filter((k) => !(k in FALL_ARGS) || (!sink && !THUD_ARGS.includes(k)));
    if (wrong.length) throw new Error(`line ${e.line}: fall "${e.name}" names ${wrong.join(", ")}, which ${sink ? "fall.js does not take" : "a thud does not take: it names drop and scale alone"}`);
    landings.push(`${e.name}: lands as ${form}`);
    if (landing && (landing === "sink") !== sink) faults.push(`${e.name}: lands as ${form}, but the motion brief picks ${landing === "sink" ? "a spring sink" : "a thud"}; recompute it as that`);
    if (!("scale" in e.args)) {
      unmeasured.push(`${e.name}: names no scale, so its fall cannot be recomputed from gravity; name its scale in px per metre`);
      continue;
    }
    const at = Object.fromEntries(Object.entries(e.args).map(([k, v]) => [FALL_ARGS[k], v]));
    try {
      checkBounds(at, sink ? ["drop", "scale", "sink"] : THUD_ARGS, "fall");
    } catch (err) {
      faults.push(`${e.name}: ${err.message}, so it is no fall fall.js computes`);
      continue;
    }
    let ms;
    if (sink) {
      const r = fall(at);
      ms = r.ms;
      if (css(r) !== e.css) faults.push(`${e.name}: its CSS is not the linear() fall.js computes from its arguments, so it is stale or tuned by hand; rerun fall.js with them`);
    } else {
      ms = thud(at).ms;
      const fault = thudFault(e);
      if (fault) faults.push(`${e.name}: ${fault}`);
    }
    for (const c of cues.filter((c) => c.easing === e.name)) {
      if (Math.abs(c.ms - ms) > LENGTH_MS) faults.push(`cue "${c.name}" (line ${c.line}) lasts ${(c.ms / 1000).toFixed(3)} s, but its fall, ${e.name}, lasts ${(ms / 1000).toFixed(3)} s; set it to that`);
    }
  }
  return { faults, unmeasured, landings, checked: falls.length - unmeasured.length };
}

function check(argv) {
  let file;
  let landing = null;
  try {
    for (let i = 0; i < argv.length; i++) {
      if (argv[i] === "--check" && i + 1 < argv.length && file === undefined) file = argv[++i];
      else if (argv[i] === "--landing" && ["thud", "sink"].includes(argv[i + 1]) && landing === null) landing = argv[++i];
      else if (argv[i] === "--landing") throw new Error("--landing wants thud or sink, once");
      else throw new Error(argv[i] === "--check" ? "--check wants one table file" : `${argv[i]} is not taken with --check`);
    }
  } catch (err) {
    console.error(`${err.message}\n${USAGE}`);
    return 2;
  }
  let result;
  try {
    result = checkTable(parseTable(fs.readFileSync(file, "utf8")), landing);
  } catch (err) {
    console.error(`${file}: ${err.code === "ENOENT" ? "no such file; pass the table the engine wrote" : err.message}`);
    return 2;
  }
  for (const f of result.faults) console.log(`FAIL ${f}`);
  for (const u of result.unmeasured) console.log(`NOT JUDGED ${u}`);
  if (!landing) for (const l of result.landings) console.log(`landing, for the founder to pick, either passes: ${l}`);
  console.log(`${result.checked} fall easing(s) recomputed, ${result.faults.length} fault(s)`);
  if (result.faults.length) return 1;
  return result.unmeasured.length ? 6 : 0;
}

function parse(argv) {
  const at = { damping: 1, tolerance: DEFAULT_TOLERANCE, viewCm: VIEW_CM, json: false };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--json") at.json = true;
    else if (FLAGS[argv[i]] && i + 1 < argv.length) at[FLAGS[argv[i]]] = Number(argv[++i]);
    else if (FLAGS[argv[i]]) throw new Error(`${argv[i]} wants a value`);
    else throw new Error(`unknown argument ${argv[i]}`);
  }
  at.settle = "distance" in at;
  const [wanted, other] = at.settle ? [["distance", "ms"], ["drop", "scale", "sink"]] : [["drop", "scale", "sink"], ["ms"]];
  for (const k of other) if (k in at) throw new Error(`--${k} is not taken by a ${at.settle ? "settle" : "fall"}`);
  checkBounds(at, wanted, at.settle ? "settle" : "fall");
  return at;
}

function main(argv) {
  if (argv.includes("--check")) return check(argv);
  let at;
  try {
    at = parse(argv);
  } catch (err) {
    console.error(`${err.message}\n${USAGE}`);
    return 2;
  }
  let r;
  try {
    r = at.settle ? settle(at) : fall(at);
  } catch (err) {
    console.error(`${err.message}\n${USAGE}`);
    return 2;
  }
  const easing = css(r);
  // A fall starts from rest at g, far under any jolt line.
  const line = at.settle ? joltLine(r.ms) : null;
  const firstPx = r.position(Math.min(FRAME_MS, r.ms)) - r.position(0);
  if (at.json) {
    const { position, ...rest } = r;
    console.log(JSON.stringify({ ...rest, joltLine: line, firstPx, easing }));
    return 0;
  }
  if (at.settle) {
    console.log(`settle: ${at.distance} px from rest arrives at ${at.ms} ms, its speed down to ${r.still.toPrecision(2)} px/s, which looks still (damping ${at.damping})`);
    console.log(`spring: ω ${r.omega.toFixed(2)} rad/s, stiffness ${r.stiffness.toFixed(1)} per unit mass, aimed ${(r.aim - at.distance).toFixed(2)} px past rest`);
    if (line !== null && r.startShare >= line) console.log(`warning: its first 60 fps frame runs at ${Math.round(100 * r.startShare)} % of its top speed, over check-flow.py's jolt line of ${Math.round(100 * line)} % at ${at.ms} ms; raise --ms`);
  } else {
    console.log(`fall: ${at.drop} px at ${at.scale} px/m takes ${r.fallMs.toFixed(1)} ms and lands at ${r.impact.toFixed(0)} px/s`);
    console.log(`landing: sinks ${at.sink} px past rest and settles in ${r.landMs.toFixed(1)} ms (damping ${at.damping})`);
    if (r.landMs < FRAME_MS) console.log(`warning: the landing is shorter than one 60 fps frame, so it plays as a stop at full speed; raise --sink`);
  }
  if (firstPx >= jumpPx(at.viewCm)) console.log(`warning: its first 60 fps frame carries it ${firstPx.toFixed(1)} px, which check-flow.py flags as a jump; ${at.settle ? "raise --ms or shorten --settle" : "lower --scale"}`);
  console.log(`duration: ${r.ms.toFixed(1)} ms, ${r.stops.length} stops within ${at.tolerance} px`);
  console.log(`easing: ${easing}`);
  return 0;
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));
