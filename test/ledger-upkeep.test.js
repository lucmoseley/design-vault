"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const ROOT = path.join(__dirname, "..");
const SCRIPT = path.join(ROOT, "ledger-upkeep.js");

const scratch = fs.mkdtempSync(path.join(os.tmpdir(), "ledger-upkeep-"));
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const MISS = { date: "2026-11-02", lead: "Text wrapping on headings: balance or pretty", family: "web platform", issue: "#227" };

let written = 0;
function ledger({ meta = {}, misses = [] } = {}) {
  const file = path.join(scratch, `ledger-${written++}.json`);
  const body = {
    meta: { built: "2026-10-15", rescan: { due: "2027-10-15", issue: "#227" }, sources: { "craft books": {}, "web platform": {} }, ...meta },
    method_misses: misses,
  };
  if (misses === null) delete body.method_misses;
  fs.writeFileSync(file, JSON.stringify(body));
  return file;
}

const warn = (file, today) => runInProcess(SCRIPT, ["--ledger", file, ...(today ? ["--today", today] : [])]);
const check = (file) => runInProcess(SCRIPT, ["--check", "--ledger", file]);

test("the warning is silent until the last scan is 12 months old, and names the age from that day", () => {
  const file = ledger({ meta: { built: "2025-03-10", rescan: { due: "2030-01-01", issue: "#227" } } });
  for (const today of ["2025-03-11", "2026-03-09"]) {
    const result = warn(file, today);
    assert.equal(result.status, 0);
    assert.equal(result.stdout, "", `${today} is before the anniversary`);
  }
  for (const today of ["2026-03-10", "2026-03-11"]) {
    const result = warn(file, today);
    assert.equal(result.status, 0);
    assert.match(result.stdout, /re-scan is due: it was last scanned on 2025-03-10, 12 months ago or more\. Run it by docs\/coverage-ledger-method\.md §7 \(#227\)/);
    assert.doesNotMatch(result.stdout, /meta\.rescan/);
  }
});

test("the warning is silent on meta.rescan's date and names it the day after", () => {
  const file = ledger({ meta: { built: "2026-01-01", rescan: { due: "2026-06-01", issue: "#300" } } });
  for (const today of ["2026-05-31", "2026-06-01"]) assert.equal(warn(file, today).stdout, "", `${today} is not past the date`);
  const result = warn(file, "2026-06-02");
  assert.equal(result.status, 0);
  assert.match(result.stdout, /re-scan is due: meta\.rescan's date, 2026-06-01, has passed\. .*\(#300\)/);
  assert.doesNotMatch(result.stdout, /12 months/);
});

test("a scan on 29 February comes due on 1 March a year on", () => {
  const file = ledger({ meta: { built: "2024-02-29", rescan: { due: "2030-01-01", issue: "#227" } } });
  assert.equal(warn(file, "2025-02-28").stdout, "");
  assert.match(warn(file, "2025-03-01").stdout, /12 months ago or more/);
});

test("with no --today the warning judges the session's own day", () => {
  const recent = new Date();
  recent.setDate(recent.getDate() - 7);
  const built = [recent.getFullYear(), recent.getMonth() + 1, recent.getDate()].map((n) => String(n).padStart(2, "0")).join("-");
  assert.equal(warn(ledger({ meta: { built } })).stdout, "");
  assert.match(warn(ledger({ meta: { built: "2020-01-01", rescan: { due: "2021-01-01", issue: "#227" } } })).stdout, /re-scan is due/);
});

test("a scan date the warning cannot read is reported as unknown, and the warning still exits 0", () => {
  for (const meta of [{ built: "15 Oct 2026" }, { rescan: "Re-scan by 2027-10-15 (#227)" }, { built: "2026-02-30" }]) {
    const result = warn(ledger({ meta }), "2026-10-16");
    assert.equal(result.status, 0);
    assert.match(result.stdout, /meta\.(built|rescan\.due) is not a YYYY-MM-DD date.*whether the re-scan is due is unknown/);
  }
  const missing = warn(path.join(scratch, "absent.json"), "2026-10-16");
  assert.equal(missing.status, 0);
  assert.match(missing.stdout, /could not read .*absent\.json.*unknown/);
});

test("a ledger holding null, or a null method miss, is reported, and the warning still exits 0", () => {
  const nullLedger = path.join(scratch, "null.json");
  fs.writeFileSync(nullLedger, "null");
  const whole = warn(nullLedger, "2026-10-16");
  assert.equal(whole.status, 0, whole.stderr);
  assert.match(whole.stdout, /the ledger is not a JSON object; whether the re-scan is due is unknown/);
  const nullMiss = ledger({ misses: [null] });
  assert.equal(warn(nullMiss, "2026-10-16").status, 0);
  const refused = check(nullMiss);
  assert.equal(refused.status, 1);
  assert.match(refused.stderr, /method_misses\[0\] is not an object/);
});

test("a --today that is not a date, a flag with no value, or an unknown argument is a usage error", () => {
  for (const [args, message] of [
    [["--today", "tomorrow"], /--today takes a YYYY-MM-DD date/],
    [["--check", "--ledger"], /--ledger takes a value/],
    [["--ledger", "--check"], /--ledger takes a value/],
    [["--chek"], /unknown argument "--chek"/],
  ]) {
    const result = runInProcess(SCRIPT, args);
    assert.equal(result.status, 2, args.join(" "));
    assert.match(result.stderr, message);
  }
});

test("the real ledger, rule store and library pass the check", () => {
  const result = runInProcess(SCRIPT, ["--check"]);
  assert.equal(result.status, 0, result.stderr);
});

test("the session start runs the warning", () => {
  const settings = JSON.parse(fs.readFileSync(path.join(ROOT, ".claude", "settings.json"), "utf8"));
  const commands = settings.hooks.SessionStart.flatMap((entry) => entry.hooks.map((hook) => hook.command));
  assert.ok(commands.some((command) => /ledger-upkeep\.js"?$/.test(command)), commands.join("\n"));
});

test("the check accepts a whole method miss and an empty list", () => {
  for (const misses of [[MISS], []]) {
    const result = check(ledger({ misses }));
    assert.equal(result.status, 0, result.stderr);
  }
});

test("#267: the check refuses a method miss missing any field, naming it", () => {
  for (const field of Object.keys(MISS)) {
    for (const value of [undefined, " "]) {
      const miss = { ...MISS, [field]: value };
      if (value === undefined) delete miss[field];
      const result = check(ledger({ misses: [MISS, miss] }));
      assert.equal(result.status, 1, `${field} ${JSON.stringify(value)}`);
      assert.match(result.stderr, new RegExp(`method_misses\\[1\\] lacks ${field}`));
    }
  }
});

test("the check refuses a miss whose date, family or issue is malformed", () => {
  for (const [field, value, message] of [
    ["date", "2 Nov 2026", /method_misses\[0\]\.date is not a YYYY-MM-DD date/],
    ["family", "blogs", /method_misses\[0\]\.family is not a source family in meta\.sources: "blogs"/],
    ["issue", "227", /method_misses\[0\]\.issue is not an issue number/],
  ]) {
    const result = check(ledger({ misses: [{ ...MISS, [field]: value }] }));
    assert.equal(result.status, 1, field);
    assert.match(result.stderr, message);
  }
});

test("the check refuses a ledger with no method-miss list, or an unreadable scan date", () => {
  const none = check(ledger({ misses: null }));
  assert.equal(none.status, 1);
  assert.match(none.stderr, /method_misses is not a list/);
  const undated = check(ledger({ meta: { rescan: "by 2027-10-15" } }));
  assert.equal(undated.status, 1);
  assert.match(undated.stderr, /meta\.rescan\.due is not a YYYY-MM-DD date/);
  assert.match(undated.stderr, /coverage-ledger-method\.md §4 \(verdicts\), §6 \(jobs\), §7 \(scan dates\) and §8/);
  const absent = check(path.join(scratch, "absent.json"));
  assert.equal(absent.status, 2);
  assert.match(absent.stderr, /cannot read .*absent\.json/);
});
