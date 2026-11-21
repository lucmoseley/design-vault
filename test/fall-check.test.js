/**
 * Tests fall.js --check (#333), gate question vault.fall-script: it reads a timeline table in design-round §6's
 * form and recomputes every fall in it. Driven from outside, by exit code and printed findings, on tables with each
 * fault present and absent. Break it and a hand-tuned or stale fall, a cue cut to the wrong length, or a landing
 * the motion brief did not pick passes the gate.
 */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { test, after } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const SCRIPT = path.join(__dirname, "..", "plugin", "skills", "design-round", "scripts", "fall.js");
const { fall, css } = require(path.join(path.dirname(SCRIPT), "fall-motion.js"));
const MMM_INFRA = path.join(__dirname, "fixtures", "fall", "mmm-infra-timeline.txt");

const SINK = { drop: 24, scale: 10, sink: 3 };
const SINK_FALL = fall(SINK);
const THUD = "thud (drop 40, scale 10)";
const THUD_S = "0.903";
const T_SQUARED = "cubic-bezier(0.333333, 0, 0.666667, 0.333333)";

function table({ sinkCss = css(SINK_FALL), sinkS = (SINK_FALL.ms / 1000).toFixed(3), thudCss = T_SQUARED, thudS = THUD_S, thudName = THUD } = {}) {
  return [
    "Timeline: 1.458 s, 3 cues on 2 elements.",
    "",
    "| Cue | Element | Start (s) | Length (s) | Easing | To |",
    "|---|---|---|---|---|---|",
    "| stone appears | stone | 0.000 | 0.000 | step | visibility: visible |",
    `| stone falls 24 px and lands | stone | 0.000 | ${sinkS} | stone | translate: 0px 0px |`,
    `| slab falls 40 px and thuds | slab | 0.100 | ${thudS} | thud | translate: 0px 0px |`,
    "",
    "| Easing | CSS |",
    "|---|---|",
    `| stone (drop 24, scale 10, sink 3) | \`${sinkCss}\` |`,
    `| ${thudName} | \`${thudCss}\` |`,
    "",
    "| Storyboard key | Time (s) |",
    "|---|---|",
    "| end | 1.458 |",
    "",
  ].join("\n");
}

const dir = fs.mkdtempSync(path.join(os.tmpdir(), "fall-check-"));
after(() => fs.rmSync(dir, { recursive: true, force: true }));
let n = 0;
function run(text, ...extra) {
  const file = path.join(dir, `table-${n++}.md`);
  fs.writeFileSync(file, text);
  return runInProcess(SCRIPT, ["--check", file, ...extra]);
}
const fails = (r) => r.stdout.split("\n").filter((l) => l.startsWith("FAIL "));

test("a matching spring sink and thud pass, and with no --landing each fall's landing is listed for the founder", () => {
  const r = run(table());
  assert.equal(r.status, 0, r.stdout + r.stderr);
  assert.deepEqual(fails(r), []);
  assert.match(r.stdout, /landing, for the founder to pick, either passes: stone: lands as a spring sink/);
  assert.match(r.stdout, /landing, for the founder to pick, either passes: thud: lands as a thud/);
  assert.match(r.stdout, /2 fall easing\(s\) recomputed, 0 fault\(s\)/);
});

test("a thud written with exact fractions' neighbours passes; one a tenth off t² fails", () => {
  assert.equal(run(table({ thudCss: "cubic-bezier(0.3333333, 0, 0.6666667, 0.3333333)" })).status, 0);
  const r = run(table({ thudCss: "cubic-bezier(0.33, 0, 0.67, 0.3)" }));
  assert.equal(r.status, 1);
  assert.match(fails(r).join("\n"), /^FAIL thud: its cubic-bezier\(0\.33, 0, 0\.67, 0\.3\) strays [\d.]+ px from the fall's t²/);
});

test("a UI curve on a thud is named as not the fall's t²", () => {
  const r = run(table({ thudCss: "cubic-bezier(0.23, 1, 0.32, 1)" }));
  assert.equal(r.status, 1);
  assert.match(fails(r).join("\n"), /FAIL thud: its cubic-bezier\(0\.23, 1, 0\.32, 1\) strays/);
  const notBezier = run(table({ thudCss: "ease-in" }));
  assert.equal(notBezier.status, 1);
  assert.match(fails(notBezier).join("\n"), /FAIL thud: its CSS is not a cubic-bezier\(\)/);
});

test("a stale spring-sink easing, one stop changed, fails and is named", () => {
  const stale = css(SINK_FALL).replace(/, 0\.25 /, ", 0.250001 ");
  assert.notEqual(stale, css(SINK_FALL));
  const r = run(table({ sinkCss: stale }));
  assert.equal(r.status, 1);
  assert.deepEqual(fails(r), ["FAIL stone: its CSS is not the linear() fall.js computes from its arguments, so it is stale or tuned by hand; rerun fall.js with them"]);
  const otherSink = run(table({ sinkCss: css(fall({ ...SINK, sink: 4 })) }));
  assert.equal(otherSink.status, 1);
  assert.match(fails(otherSink).join("\n"), /FAIL stone: its CSS is not the linear\(\) fall\.js computes/);
});

test("a cue whose length is not its fall's fails and is named, for each landing form; one rounding to it passes", () => {
  const sinkOff = run(table({ sinkS: "1.460" }));
  assert.equal(sinkOff.status, 1);
  assert.deepEqual(fails(sinkOff), ['FAIL cue "stone falls 24 px and lands" (line 6) lasts 1.460 s, but its fall, stone, lasts 1.458 s; set it to that']);
  const thudOff = run(table({ thudS: "0.905" }));
  assert.equal(thudOff.status, 1);
  assert.deepEqual(fails(thudOff), ['FAIL cue "slab falls 40 px and thuds" (line 7) lasts 0.905 s, but its fall, thud, lasts 0.903 s; set it to that']);
  // The thud's √(2 · drop / g) is 903.2 ms, written to 1 ms 0.903; 0.904 is 0.8 ms off.
  const near = run(table({ thudS: "0.904" }));
  assert.equal(near.status, 1);
  assert.match(fails(near).join("\n"), /lasts 0\.904 s, but its fall, thud, lasts 0\.903 s/);
});

test("a landing against --landing fails and is named; the picked one passes and no landing is listed", () => {
  const thudOnly = table({ thudName: "thud (drop 40, scale 10)" }).replace(/^\| stone falls.*\n/m, "").replace(/^\| stone \(.*\n/m, "");
  const sinkOnly = table().replace(/^\| slab falls.*\n/m, "").replace(/^\| thud .*\n/m, "");
  const againstThud = run(sinkOnly, "--landing", "thud");
  assert.equal(againstThud.status, 1);
  assert.deepEqual(fails(againstThud), ["FAIL stone: lands as a spring sink, but the motion brief picks a thud; recompute it as that"]);
  const againstSink = run(thudOnly, "--landing", "sink");
  assert.equal(againstSink.status, 1);
  assert.deepEqual(fails(againstSink), ["FAIL thud: lands as a thud, but the motion brief picks a spring sink; recompute it as that"]);
  for (const [text, pick] of [[sinkOnly, "sink"], [thudOnly, "thud"]]) {
    const r = run(text, "--landing", pick);
    assert.equal(r.status, 0, r.stdout);
    assert.doesNotMatch(r.stdout, /for the founder to pick/);
  }
});

test("a table mmm-infra's engine wrote is read without change, its falls matching", () => {
  const r = runInProcess(SCRIPT, ["--check", MMM_INFRA]);
  assert.equal(r.status, 0, r.stdout + r.stderr);
  assert.match(r.stdout, /stone: lands as a spring sink/);
  assert.match(r.stdout, /slab: lands as a spring sink/);
  assert.match(r.stdout, /2 fall easing\(s\) recomputed, 0 fault\(s\)/);
});

test("a fall naming no scale cannot be recomputed and exits 6, unless another fall fails", () => {
  const noScale = table({ thudName: "thud (drop 40)" });
  const r = run(noScale);
  assert.equal(r.status, 6, r.stdout + r.stderr);
  assert.match(r.stdout, /NOT JUDGED thud: names no scale, so its fall cannot be recomputed from gravity; name its scale in px per metre/);
  assert.match(r.stdout, /landing, for the founder to pick, either passes: thud: lands as a thud/);
  const against = run(noScale, "--landing", "sink");
  assert.equal(against.status, 1, against.stdout);
  assert.match(fails(against).join("\n"), /FAIL thud: lands as a thud, but the motion brief picks a spring sink/);
  const both = run(table({ thudName: "thud (drop 40)", sinkS: "1.460" }));
  assert.equal(both.status, 1);
  assert.match(fails(both).join("\n"), /cue "stone falls 24 px and lands"/);
});

test("bad usage and a table it cannot read exit 2, naming why", () => {
  const cases = [
    [[], /--check wants one table file/],
    [["--landing", "soft"], /--landing wants thud or sink/],
    [["--json"], /--json is not taken with --check/],
  ];
  for (const [extra, why] of cases) {
    const file = path.join(dir, "ok.md");
    fs.writeFileSync(file, table());
    const r = runInProcess(SCRIPT, extra.length ? ["--check", file, ...extra] : ["--check"]);
    assert.equal(r.status, 2, extra.join(" "));
    assert.match(r.stderr, why);
  }
  const unreadable = [
    [table().replace("| Easing | CSS |", "| Name | CSS |"), /no easing table/],
    [table().replace("| Cue | Element |", "| Move | Element |"), /no cue table/],
    [table().replace("| stone (drop 24,", "| pebble (drop 24,"), /cue "stone falls 24 px and lands" uses easing "stone", which the easing table does not hold/],
    [table().replace("| 0.903 |", "| soon |"), /length "soon" is not a number of seconds/],
    [table().replace("| slab falls 40 px and thuds |", "| slab | falls |"), /a cue row has 7 cells, not 6; no cell may hold a \|/],
    [table({ thudName: "thud (drop 40, scale 10, sink-ish 2)" }), /names sink-ish/],
    [table({ thudName: "thud (drop 40, scale 10, tolerance 0.02)" }), /a thud does not take: it names drop and scale alone/],
    [table({ thudName: "thud (drop forty, scale 10)" }), /argument "drop forty" is not a name and a number/],
    [table().replace("| thud (drop 40, scale 10) |", "|  |"), /an easing row names no easing/],
  ];
  for (const [text, why] of unreadable) {
    const r = run(text);
    assert.equal(r.status, 2, String(why));
    assert.match(r.stderr, why);
  }
  const missing = runInProcess(SCRIPT, ["--check", path.join(dir, "missing.md")]);
  assert.equal(missing.status, 2);
  assert.match(missing.stderr, /missing\.md: no such file/);
});

test("a fall whose arguments break fall.js's own bounds fails, even where its curve and length agree with them", () => {
  // A negative drop puts t² and the curve together at 0 px apart and its length out of reach of any cue.
  const negative = run(table({ thudName: "thud (drop -40, scale 10)", thudCss: "cubic-bezier(0.23, 1, 0.32, 1)", thudS: "5.000" }));
  assert.equal(negative.status, 1, negative.stdout);
  assert.deepEqual(fails(negative), ["FAIL thud: --drop wants a number above 0, so it is no fall fall.js computes"]);
  const underdamped = run(table().replace("| stone (drop 24, scale 10, sink 3) |", "| stone (drop 24, scale 10, sink 3, damping 0.5) |"));
  assert.equal(underdamped.status, 1, underdamped.stdout);
  assert.deepEqual(fails(underdamped), ["FAIL stone: --damping wants 1 (critical) or more; under 1 the landing bounces, so it is no fall fall.js computes"]);
  // The bound's edge: a damping of 1 is the critical landing fall.js prints by default, so it passes.
  const critical = run(table().replace("| stone (drop 24, scale 10, sink 3) |", "| stone (drop 24, scale 10, sink 3, damping 1) |"));
  assert.equal(critical.status, 0, critical.stdout);
});
