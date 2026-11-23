"use strict";
// test/run-lanes.sh, which runs test/all.sh's suites side by side within the machine's 3-suite ceiling (#363).
// Loosen it and a red suite lands, one suite's output is spliced into another's, or a commit's suites start a 4th on
// a machine core docs/environment.md §6 measured only to 3. Loosen its VAULT_SUITE_BUDGET refusal and a commit planning
// more than its lanes can end is killed at workflow-core's suite ceiling, with no verdict (#473).
require("./no-git-env");
const assert = require("node:assert/strict");
const { spawn, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, describe, test } = require("node:test");

const LANES = path.join(__dirname, "run-lanes.sh");
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "run-lanes-"));
after(() => fs.rmSync(dir, { recursive: true, force: true }));

// A suite named as test/all.sh names a Python one, so the ps count reads it as a suite.
// The pause, 1 s unless LANE_SLEEP says otherwise, is a guess: long enough that suites a run starts together still
// overlap on a loaded machine. With LANE_KID set it first starts a child that sleeps as long, as a suite starts a
// checker and a browser.
const FAKE = path.join(dir, "lane.test.py");
fs.writeFileSync(FAKE, `import os, subprocess, sys, time
d, name, code = sys.argv[1], sys.argv[2], int(sys.argv[3])
run = os.path.join(d, "running")
os.makedirs(run, exist_ok=True)
open(os.path.join(run, name), "w").close()
def note():
    with open(os.path.join(d, "peaks"), "a") as fh:
        fh.write(f"{len(os.listdir(run))}\\n")
note()
if os.environ.get("LANE_KID"):
    subprocess.Popen([sys.executable, "-c", "import sys, time; time.sleep(float(sys.argv[1]))", os.environ["LANE_SLEEP"], d])
print(f"{name} one", flush=True)
time.sleep(float(os.environ.get("LANE_SLEEP", "1")))
print(f"{name} two", flush=True)
note()
os.remove(os.path.join(run, name))
sys.exit(code)
`);

// Written once each: a rewrite while a concurrent case's run reads it would show that run no memory reading.
const meminfo = (mb) => {
  const file = path.join(dir, `meminfo-${mb}`);
  if (!fs.existsSync(file)) fs.writeFileSync(file, `MemTotal:       10162176 kB\nMemAvailable:   ${mb * 1024} kB\n`);
  return file;
};
// A stand-in for ps printing `lines` as the machine's processes.
const ps = (name, lines) => {
  const file = path.join(dir, `ps-${name}`);
  fs.writeFileSync(file, `#!/bin/sh\ncat <<'EOF'\n${lines.join("\n")}\nEOF\n`, { mode: 0o755 });
  return file;
};
const QUIET = ps("quiet", []);
// Above the ladder's last rung, so memory never holds a suite back.
const AMPLE = 8000;

let runs = 0;
function run(args, env) {
  return new Promise((resolve) => {
    const child = spawn("bash", [LANES, ...args], { env: { ...process.env, VAULT_SUITE_LANES: "", VAULT_SUITE_TIMES: "", VAULT_SUITE_BUDGET: "", ...env } });
    const out = { stdout: "", stderr: "" };
    child.stdout.on("data", (b) => (out.stdout += b));
    child.stderr.on("data", (b) => (out.stderr += b));
    child.on("close", (status) => resolve({ ...out, status }));
  });
}

/**
 * Runs run-lanes.sh on `n` fake suites, the `red` ones exiting 1; resolves to its process and the most lanes seen at
 * once. With `own`, each suite runs a copy of the fake of its own, `<d>/s<i>.test.py`, so a red one's file is its own.
 */
async function lanes(n, { env = {}, red = [], psFor, own } = {}) {
  const d = path.join(dir, `run-${runs++}`);
  fs.mkdirSync(d);
  if (psFor) env = { ...env, VAULT_PS: psFor(d) };
  const fake = (i) => {
    if (!own) return FAKE;
    const copy = path.join(d, `s${i}.test.py`);
    fs.copyFileSync(FAKE, copy);
    return copy;
  };
  const suites = Array.from({ length: n }, (_, i) => `python3 ${fake(i)} ${d} s${i} ${red.includes(i) ? 1 : 0}`);
  const proc = await run(suites, { VAULT_MEMINFO: meminfo(AMPLE), VAULT_PS: QUIET, ...env });
  assert.equal(proc.status, red.length ? 1 : 0, proc.stderr);
  const peaks = fs.readFileSync(path.join(d, "peaks"), "utf8").trim().split("\n").map(Number);
  return { proc, peak: Math.max(...peaks), suites };
}

// Each case runs its own fake suites in a directory of its own, so the cases run at once.
describe("run-lanes.sh", { concurrency: true }, () => {
  test("every suite runs, and only a red one's test file is named, as `FAIL <path>`, with exit 1", async () => {
    const { proc, suites } = await lanes(4, { red: [2], own: true });
    assert.equal(proc.status, 1, proc.stderr);
    assert.equal(proc.stderr, `FAIL ${suites[2].split(" ")[1]}\n`);
    for (const s of suites) assert.match(proc.stdout, new RegExp(`^== ${s.replace(/[.]/g, "\\.")} \\(\\d+ s\\)$`, "m"));
  });

  test("two reds print a FAIL line each", async () => {
    const { proc, suites } = await lanes(3, { red: [0, 2], own: true });
    const lines = proc.stderr.trim().split("\n").sort();
    assert.deepEqual(lines, [0, 2].map((i) => `FAIL ${suites[i].split(" ")[1]}`).sort());
  });

  // As test/failed-files.js does for node --test.
  test("a red suite that writes its failing files to VAULT_FAILED_FILES is named by those alone", async () => {
    const writer = path.join(dir, "writer.sh");
    fs.writeFileSync(writer, 'code=$1; shift; printf "%s\\n" "$@" >>"$VAULT_FAILED_FILES"; exit "$code"\n');
    const proc = await run([`sh ${writer} 1 test/a.test.js test/b.test.js`, `sh ${writer} 0 test/green.test.js`],
      { VAULT_MEMINFO: meminfo(AMPLE), VAULT_PS: QUIET });
    assert.equal(proc.status, 1, proc.stderr);
    assert.equal(proc.stderr, "FAIL test/a.test.js\nFAIL test/b.test.js\n");
  });

  test("a red suite that names no test file, or several, and writes none is printed `RED  <suite>`", async () => {
    const two = path.join(dir, "two.test.py");
    fs.writeFileSync(two, "");
    const several = `sh -c false ${FAKE} ${two}`;
    const proc = await run(["false", several], { VAULT_MEMINFO: meminfo(AMPLE), VAULT_PS: QUIET });
    assert.equal(proc.status, 1);
    assert.deepEqual(proc.stderr.trim().split("\n").sort(), ["RED  false", `RED  ${several}`]);
  });

  test("an all-green run exits 0 and prints nothing to stderr", async () => {
    const { proc } = await lanes(2);
    assert.equal(proc.status, 0, proc.stderr);
    assert.equal(proc.stderr, "");
  });

  test("each suite's output is printed whole under its own header, though the suites ran side by side", async () => {
    const { proc, peak } = await lanes(3);
    assert.equal(peak, 3);
    for (let i = 0; i < 3; i++) assert.match(proc.stdout, new RegExp(`\\(\\d+ s\\)\\ns${i} one\\ns${i} two\\n`));
  });

  test("with memory to spare and nothing else running, three suites run at once and never a fourth", async () => {
    assert.equal((await lanes(5)).peak, 3);
  });

  test("VAULT_SUITE_LANES=1 runs one suite at a time", async () => {
    assert.equal((await lanes(3, { env: { VAULT_SUITE_LANES: "1" } })).peak, 1);
  });

  test("a VAULT_SUITE_LANES that is no count of 1 or more runs nothing and exits 2", async () => {
    const proc = await run(["true"], { VAULT_SUITE_LANES: "0" });
    assert.equal(proc.status, 2);
    assert.match(proc.stderr, /VAULT_SUITE_LANES wants 1 or more — got '0'/);
  });

  // Past the ceiling, one suite still runs, as the one-at-a-time run always did.
  for (const [others, lines, n, peak] of [
    ["one", ["  11 /usr/bin/python3 test/check-flow.test.py"], 3, 2],
    ["two", ["  11 python3 test/check-flow.test.py", "  12 /home/u/.nvm/bin/node --test"], 3, 1],
    ["three", ["  11 python3 -m pytest", "  12 node --test", "  13 node /r/node_modules/.bin/vitest run"], 2, 1],
  ]) {
    test(`with ${others} suite(s) running elsewhere on the machine, ${peak} of this run's go at once`, async () => {
      assert.equal((await lanes(n, { env: { VAULT_PS: ps(others, lines) } })).peak, peak);
    });
  }

  test("a checker, a node --test child, a wrapper shell and a vitest list are no suites", async () => {
    const busy = ps("busy", [
      "  11 python3 plugin/skills/design-round/scripts/check-access.py page.html",
      "  12 /usr/bin/node --test-concurrency=0 --test-isolation=process test/fall.test.js",
      '  13 bash -c python3 test/check-flow.test.py',
      "  14 node --testing",
      "  15 node /r/node_modules/.bin/vitest list --json",
      "  16 bash -c node_modules/.bin/vitest run",
      "  17 timeout 300 node_modules/.bin/vitest run",
    ]);
    assert.equal((await lanes(3, { env: { VAULT_PS: busy } })).peak, 3);
  });

  test("this run's own suites are counted once, not again as the machine's", async () => {
    // The real ps, narrowed to this run's fake suites, so it sees its own lanes and nothing else on the machine.
    const psFor = (d) => {
      const own = path.join(d, "ps");
      fs.writeFileSync(own, `#!/bin/sh\nps "$@" | grep -F '${FAKE} ${d} ' || true\n`, { mode: 0o755 });
      return own;
    };
    // Longer than the 1 s default, since each launch here waits on a real ps: a guess.
    assert.equal((await lanes(3, { psFor, env: { LANE_SLEEP: "1.5" } })).peak, 3);
  });

  for (const [mb, peak] of [[3399, 1], [3400, 2], [4049, 2], [4050, 3]]) {
    test(`at ${mb} MB available, ${peak} suite(s) run at once: a second waits for 3,400 MB and a third for 4,050 MB`, async () => {
      assert.equal((await lanes(3, { env: { VAULT_MEMINFO: meminfo(mb) } })).peak, peak);
    });
  }

  test("where ps cannot be read, suites run one at a time", async () => {
    assert.equal((await lanes(2, { env: { VAULT_PS: "false" } })).peak, 1);
  });

  test("where the memory reading cannot be had, suites run one at a time", async () => {
    assert.equal((await lanes(2, { env: { VAULT_MEMINFO: path.join(dir, "absent") } })).peak, 1);
  });

  test("suites start longest first by their kept green seconds, one with none kept first; a red keeps its old figure (#457)", async () => {
    const d = path.join(dir, "timed");
    const kept = path.join(d, "times");
    fs.mkdirSync(kept, { recursive: true });
    const suite = (name, code = 0) => `python3 ${FAKE} ${d} ${name} ${code}`;
    // The file run-lanes.sh keeps a suite's seconds in, named by the POSIX cksum of its command line.
    const file = (s) => path.join(kept, spawnSync("cksum", { input: s, encoding: "utf8" }).stdout.split(" ")[0]);
    // Far past what a fake suite takes, so a figure it writes is told from its seed by value, never by its size.
    const seed = { short: 5000, long: 30000, red: 77000 };
    for (const [name, secs] of Object.entries(seed)) fs.writeFileSync(file(suite(name, name === "red" ? 1 : 0)), `${secs}\n`);
    const given = [suite("short"), suite("red", 1), suite("new"), suite("long")];
    // One lane, so the order they end in is the order they started in.
    const proc = await run(given, { VAULT_MEMINFO: meminfo(AMPLE), VAULT_PS: QUIET, VAULT_SUITE_LANES: "1", VAULT_SUITE_TIMES: kept });
    assert.equal(proc.status, 1, proc.stderr);
    const ended = [...proc.stdout.matchAll(/^== python3 \S+ \S+ (\w+) /gm)].map((m) => m[1]);
    assert.deepEqual(ended, ["new", "red", "long", "short"]);
    for (const name of ["short", "new", "long"]) {
      const secs = fs.readFileSync(file(suite(name)), "utf8");
      assert.match(secs, /^\d+\n$/, name);
      assert.notEqual(Number(secs), seed[name], name);
    }
    assert.equal(fs.readFileSync(file(suite("red", 1)), "utf8"), "77000\n");
  });

  test("without VAULT_SUITE_TIMES, suites start in the order given", async () => {
    const d = path.join(dir, "untimed");
    fs.mkdirSync(d);
    const given = ["b", "a", "c"].map((n) => `python3 ${FAKE} ${d} ${n} 0`);
    const proc = await run(given, { VAULT_MEMINFO: meminfo(AMPLE), VAULT_PS: QUIET, VAULT_SUITE_LANES: "1", VAULT_SUITE_TIMES: "" });
    assert.deepEqual([...proc.stdout.matchAll(/^== python3 \S+ \S+ (\w+) /gm)].map((m) => m[1]), ["b", "a", "c"]);
  });

  /**
   * Runs four fake suites kept at 6, 5, 4 and 3 s, and one with none kept where `untimed`, under VAULT_SUITE_BUDGET
   * (#473), in a directory of their own: a green run rewrites the seconds it keeps.
   */
  let budgeted = 0;
  function underBudget(budget, env = {}, { untimed = false } = {}) {
    const d = path.join(dir, `budget-${budgeted++}`);
    const times = path.join(d, "times");
    fs.mkdirSync(times, { recursive: true });
    const suite = (name) => `python3 ${FAKE} ${d} ${name} 0`;
    const given = [];
    for (const [name, secs] of [["a", 6], ["b", 5], ["c", 4], ["d", 3]]) {
      const sum = spawnSync("cksum", { input: suite(name), encoding: "utf8" }).stdout.split(" ")[0];
      fs.writeFileSync(path.join(times, sum), `${secs}\n`);
      given.push(suite(name));
    }
    if (untimed) given.push(suite("new"));
    return run(given, { VAULT_MEMINFO: meminfo(AMPLE), VAULT_PS: QUIET, VAULT_SUITE_TIMES: times, VAULT_SUITE_BUDGET: String(budget), ...env })
      .then((proc) => ({ ...proc, ran: fs.existsSync(path.join(d, "peaks")) }));
  }

  test("a run whose kept seconds end past VAULT_SUITE_BUDGET on one lane is refused before any suite starts (#473)", async () => {
    const proc = await underBudget(17, { VAULT_SUITE_LANES: "1" });
    assert.equal(proc.status, 1, proc.stderr);
    assert.equal(proc.ran, false);
    assert.match(proc.stderr, /refused before any suite ran: the 4 suites' kept green seconds sum to 18 s, which on the 1 lane\(s\) the machine opens now end at about 18 s, past VAULT_SUITE_BUDGET's 17 s, the time left under workflow-core's suite ceiling \(workflow-core#2667\) inside a commit\. Run it again once fewer suites run on the machine and more memory is free/);
  });

  test("a run whose kept seconds end at VAULT_SUITE_BUDGET runs", async () => {
    const proc = await underBudget(18, { VAULT_SUITE_LANES: "1" });
    assert.equal(proc.status, 0, proc.stderr);
    assert.equal(proc.ran, true);
  });

  test("the budget is judged on the lanes open at the start, longest first onto the one that frees first", async () => {
    // Three lanes end at 7 s (6, 5, 4 + 3); with one suite running elsewhere, two end at 9 s (6 + 3, 5 + 4).
    const three = await underBudget(8);
    assert.equal(three.status, 0, three.stderr);
    const two = await underBudget(8, { VAULT_PS: ps("one-budget", ["  11 python3 test/check-flow.test.py"]) });
    assert.equal(two.status, 1, two.stderr);
    assert.equal(two.ran, false);
    assert.match(two.stderr, /on the 2 lane\(s\) the machine opens now end at about 9 s, past VAULT_SUITE_BUDGET's 8 s/);
  });

  test("a suite with no seconds kept counts as none against the budget", async () => {
    const proc = await underBudget(18, { VAULT_SUITE_LANES: "1" }, { untimed: true });
    assert.equal(proc.status, 0, proc.stderr);
  });

  test("a VAULT_SUITE_BUDGET that is no whole count of seconds runs nothing and exits 2", async () => {
    const proc = await underBudget(0);
    assert.equal(proc.status, 2);
    assert.equal(proc.ran, false);
    assert.match(proc.stderr, /VAULT_SUITE_BUDGET wants whole seconds, 1 or more — got '0'/);
  });

  for (const [signal, status] of [["SIGINT", 130], ["SIGTERM", 143]]) {
    test(`a run stopped by ${signal} exits ${status} and stops the suites it started, and what they started`, async () => {
      const d = path.join(dir, `stopped-${signal}`);
      fs.mkdirSync(d);
      const child = spawn("bash", [LANES, ...["a", "b"].map((n) => `python3 ${FAKE} ${d} ${n} 0`)], {
        // Each suite and its child sleep far past the test's own waits, so only the stop can end them.
        env: { ...process.env, VAULT_SUITE_LANES: "", VAULT_MEMINFO: meminfo(AMPLE), VAULT_PS: QUIET, LANE_SLEEP: "30", LANE_KID: "1" },
      });
      const running = path.join(d, "running");
      // The suites and their children, not run-lanes.sh itself, whose own command line names `d` too.
      const alive = () => spawnSync("pgrep", ["-f", d], { encoding: "utf8" }).stdout.trim().split("\n")
        .filter((pid) => pid && Number(pid) !== child.pid);
      // Guesses: up to 10 s for both suites and their children to start, and 2 s for them to be gone once stopped.
      for (let i = 0; i < 100 && !(fs.existsSync(running) && fs.readdirSync(running).length === 2 && alive().length === 4); i++) {
        await new Promise((r) => setTimeout(r, 100));
      }
      assert.equal(alive().length, 4, "both suites and their children started");
      const code = new Promise((r) => child.on("exit", r));
      child.kill(signal);
      assert.equal(await code, status);
      for (let i = 0; i < 20 && alive().length; i++) await new Promise((r) => setTimeout(r, 100));
      assert.deepEqual(alive(), [], "a suite or its child outlived the run");
    });
  }
});
