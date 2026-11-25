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
// overlap on a loaded machine; a 4th argument sets one suite's own. With LANE_KID set it first starts a child that sleeps
// as long, as a suite starts a checker and a browser. A 5th argument holds that many MB, written, before the first note.
const FAKE = path.join(dir, "lane.test.py");
fs.writeFileSync(FAKE, `import os, subprocess, sys, time
d, name, code = sys.argv[1], sys.argv[2], int(sys.argv[3])
pause = float(sys.argv[4]) if len(sys.argv) > 4 else float(os.environ.get("LANE_SLEEP", "1"))
held = b"\\x01" * (int(sys.argv[5]) * 1024 * 1024) if len(sys.argv) > 5 else b""
run = os.path.join(d, "running")
os.makedirs(run, exist_ok=True)
open(os.path.join(run, name), "w").close()
def note():
    with open(os.path.join(d, "peaks"), "a") as fh:
        fh.write(f"{len(os.listdir(run))} {name}\\n")
note()
if os.environ.get("LANE_KID"):
    subprocess.Popen([sys.executable, "-c", "import sys, time; time.sleep(float(sys.argv[1]))", os.environ["LANE_SLEEP"], d])
print(f"{name} one", flush=True)
time.sleep(pause)
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
// The file run-lanes.sh keeps a suite's seconds in under `times`, named by the POSIX cksum of its command line.
const keptFile = (times, suite) => path.join(times, spawnSync("cksum", { input: suite, encoding: "utf8" }).stdout.split(" ")[0]);

// No gate seat, though this test may run under one, and a cgroup directory setting no limit.
const UNLIMITED = fs.mkdtempSync(path.join(dir, "cgroup-"));
const UNSEATED = { WFC_GATE_SEAT: "", VAULT_CGROUP: UNLIMITED, VAULT_LANE_WAIT_S: "" };

let runs = 0;
// #370
function run(args, env, { cwd } = {}) {
  return new Promise((resolve) => {
    const full = { ...process.env, ...UNSEATED, VAULT_SUITE_LANES: "", VAULT_SUITE_TIMES: "", VAULT_SUITE_BUDGET: "", CI: "1", ...env };
    for (const key of Object.keys(full)) if (full[key] === undefined) delete full[key];
    const child = spawn("bash", [LANES, ...args], { cwd, env: full });
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
  const counts = fs.readFileSync(path.join(d, "peaks"), "utf8").trim().split("\n").map((l) => Number(l.split(" ")[0]));
  return { proc, peak: Math.max(...counts), suites };
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

  const THREE = ["  11 python3 -m pytest", "  12 node --test", "  13 node /r/node_modules/.bin/vitest run"];
  for (const [others, lines, n, peak] of [
    ["one", ["  11 /usr/bin/python3 test/check-flow.test.py"], 3, 2],
    ["two", ["  11 python3 test/check-flow.test.py", "  12 /home/u/.nvm/bin/node --test"], 3, 1],
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

  for (const [mb, peak] of [[2500, 1], [3399, 1], [3400, 2], [4049, 2], [4050, 3]]) {
    test(`at ${mb} MB available, ${peak} suite(s) run at once: a first waits for 2,500 MB, a second for 3,400 MB and a third for 4,050 MB`, async () => {
      assert.equal((await lanes(3, { env: { VAULT_MEMINFO: meminfo(mb) } })).peak, peak);
    });
  }

  // Waiting out the bound is real time: VAULT_LANE_WAIT_S=0 refuses on the second poll, a second in.
  for (const [why, env] of [
    ["the machine already runs 3 suites", { VAULT_PS: ps("three", THREE) }],
    ["MemAvailable is short of the first rung", { VAULT_MEMINFO: meminfo(2499) }],
  ]) {
    test(`where ${why}, the first suite waits for its rung too, and the run is refused at VAULT_LANE_WAIT_S`, async () => {
      const d = path.join(dir, `held-${runs++}`);
      fs.mkdirSync(d);
      const proc = await run([`python3 ${FAKE} ${d} s0 0`], { VAULT_MEMINFO: meminfo(AMPLE), VAULT_PS: QUIET, ...env, VAULT_LANE_WAIT_S: "0" });
      assert.equal(proc.status, 1, proc.stderr);
      assert.equal(fs.existsSync(path.join(d, "peaks")), false, "a suite ran");
      assert.match(proc.stdout, /waiting up to 0 s for the machine to run fewer suites or free more memory/);
      assert.match(proc.stderr, /^test\/run-lanes\.sh: refused: after 0 s the machine still runs too many suites/);
    });
  }

  test("a first suite held for its rung starts once it frees", async () => {
    const d = path.join(dir, "freed");
    fs.mkdirSync(d);
    // A ps that reports 3 suites on its first two reads and none after.
    const reads = path.join(d, "reads");
    const freeing = ps("freeing", []);
    fs.writeFileSync(freeing, `#!/bin/sh
echo >>'${reads}'
[ "$(wc -l <'${reads}')" -gt 2 ] && exit 0
cat <<'EOF'
${THREE.join("\n")}
EOF
`);
    const proc = await run([`python3 ${FAKE} ${d} s0 0 0.1`], { VAULT_MEMINFO: meminfo(AMPLE), VAULT_PS: freeing });
    assert.equal(proc.status, 0, proc.stderr);
    assert.ok(fs.existsSync(path.join(d, "peaks")), "the suite never ran");
  });

  test("an unparsable VAULT_LANE_WAIT_S runs nothing and exits 2", async () => {
    const proc = await run(["true"], { VAULT_LANE_WAIT_S: "soon" });
    assert.equal(proc.status, 2);
    assert.match(proc.stderr, /VAULT_LANE_WAIT_S wants whole seconds — got 'soon'/);
  });

  // A cgroup directory whose limit leaves `roomMb` free: memory.max less memory.current plus inactive_file.
  const cgroup = (name, roomMb) => {
    const c = path.join(dir, `cgroup-${name}`);
    fs.mkdirSync(c, { recursive: true });
    const mib = 1024 * 1024;
    fs.writeFileSync(path.join(c, "memory.max"), `${3584 * mib}\n`);
    fs.writeFileSync(path.join(c, "memory.current"), `${(3584 - roomMb + 100) * mib}\n`);
    fs.writeFileSync(path.join(c, "memory.stat"), `anon 1\ninactive_file ${100 * mib}\nactive_file 5\n`);
    return c;
  };
  for (const [room, peak] of [[899, 1], [900, 2], [1549, 2], [1550, 3]]) {
    test(`with ${room} MB left under this run's cgroup limit, ${peak} suite(s) run at once: a second needs 900 MB there and a third 1,550 MB`, async () => {
      assert.equal((await lanes(3, { env: { VAULT_CGROUP: cgroup(`room-${room}`, room) } })).peak, peak);
    });
  }
  // The suites' own memory is real, so their cgroup's room is read after each start: a fixed room stands for it.
  test("a cgroup limit of max reads as no limit", async () => {
    const c = cgroup("max", 0);
    fs.writeFileSync(path.join(c, "memory.max"), "max\n");
    assert.equal((await lanes(3, { env: { VAULT_CGROUP: c } })).peak, 3);
  });

  describe("under a gate seat (#434)", () => {
    let seats = 0;
    // workflow-core's queue marker for a gate seat, as queue-run.js --gate writes it.
    const marker = (fields) => {
      const file = path.join(dir, `seat-${seats++}.json`);
      fs.writeFileSync(file, typeof fields === "string" ? fields
        : JSON.stringify({ at: Date.now(), role: "gate", repo: "design-vault", session: null, command: "bash test/all.sh", ...fields }));
      return file;
    };
    // A machine the ladder would hold every suite on.
    const FULL = () => ({ VAULT_PS: ps("seat-full", THREE), VAULT_MEMINFO: meminfo(0), VAULT_LANE_WAIT_S: "0" });

    test("a seat this run sits under sizes its lanes by its charge alone: no ps count or MemAvailable is read", async () => {
      const env = { ...FULL(), WFC_GATE_SEAT: marker({ pid: process.pid, chargeMb: 3350 }) };
      assert.equal((await lanes(3, { env })).peak, 3);
    });

    // A second lane needs the ladder's 900 MB rise free beside the lanes' own PSS, a third 1,550 MB.
    for (const [chargeMb, peak] of [[899, 1], [1549, 2], [3350, 3]]) {
      test(`a seat charged ${chargeMb} MB runs ${peak} suite(s) at once`, async () => {
        const env = { ...FULL(), WFC_GATE_SEAT: marker({ pid: process.pid, chargeMb }) };
        assert.equal((await lanes(3, { env })).peak, peak);
      });
    }

    test("a lane's PSS, with every process under it, counts against the charge", async () => {
      // s0 and s1 open at once, the second on the 900 MB rise of a 1,100 MB charge. Once s0 ends, s2 would need
      // that rise again beside s1, whose child holds 300 MB, so it waits for s1.
      const d = path.join(dir, "pss");
      fs.mkdirSync(d);
      const wrap = path.join(d, "wrap.sh");
      fs.writeFileSync(wrap, '"$@"\n');
      const suites = [`python3 ${FAKE} ${d} s0 0 0.6`, `sh ${wrap} python3 ${FAKE} ${d} s1 0 3 300`, `python3 ${FAKE} ${d} s2 0 0.1`];
      const proc = await run(suites, { ...FULL(), VAULT_SUITE_LANES: "2", WFC_GATE_SEAT: marker({ pid: process.pid, chargeMb: 1100 }) });
      assert.equal(proc.status, 0, proc.stderr);
      const notes = fs.readFileSync(path.join(d, "peaks"), "utf8").trim().split("\n").map((l) => l.split(" "));
      assert.ok(notes.some(([c, n]) => n === "s0" && c === "2"), "s0 and s1 never ran together");
      assert.deepEqual(notes.filter(([, n]) => n === "s2").map(([c]) => c), ["1", "1"], "s2 ran beside s1's 300 MB");
    });

    for (const [why, file] of [
      ["names a pid that is not this run's ancestor", () => marker({ pid: 2 ** 22 + 1, chargeMb: 3350 })],
      ["does not parse", () => marker("{ not json")],
      ["carries no chargeMb", () => marker({ pid: process.pid })],
      ["names a file that is not there", () => path.join(dir, "no-seat.json")],
    ]) {
      test(`a seat marker that ${why} leaves the ladder in force`, async () => {
        const d = path.join(dir, `unseated-${seats++}`);
        fs.mkdirSync(d);
        const proc = await run([`python3 ${FAKE} ${d} s0 0`], { ...FULL(), WFC_GATE_SEAT: file() });
        assert.equal(proc.status, 1, proc.stderr);
        assert.equal(fs.existsSync(path.join(d, "peaks")), false, "a suite ran past the ladder");
      });
    }

    test("the budget counts the lanes the charge opens, not the machine's", async () => {
      const proc = await underBudget(8, { ...FULL(), WFC_GATE_SEAT: marker({ pid: process.pid, chargeMb: 3350 }) });
      assert.equal(proc.status, 0, proc.stderr);
      assert.equal(proc.ran, true);
    });
  });

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
    const file = (s) => keptFile(kept, s);
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
   * Runs four kept fake suites, and one with none kept where `untimed`, under VAULT_SUITE_BUDGET (#473): a green run
   * rewrites the seconds it keeps.
   */
  let budgeted = 0;
  function underBudget(budget, env = {}, { untimed = false } = {}) {
    const d = path.join(dir, `budget-${budgeted++}`);
    const times = path.join(d, "times");
    fs.mkdirSync(times, { recursive: true });
    const suite = (name) => `python3 ${FAKE} ${d} ${name} 0`;
    const given = [];
    for (const [name, secs] of [["a", 6], ["b", 5], ["c", 4], ["d", 3]]) {
      fs.writeFileSync(keptFile(times, suite(name)), `${secs}\n`);
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
    assert.match(proc.stderr, /refused before any suite ran: the 4 suites' kept green seconds sum to 18 s, which on the 1 lane\(s\) the machine opens now end at about 18 s, past VAULT_SUITE_BUDGET's 17 s, the time a gate run has left under workflow-core's suite ceiling \(workflow-core#2667\)\. VAULT_SUITE_LANES caps this run at 1 lane\(s\); raise it, or run it again once fewer suites run on the machine and more memory is free/);
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
    assert.equal(proc.ran, true);
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

  describe("the run-cost report (#370)", () => {
    const coreStandIn = (name, { throws } = {}) => {
      const core = path.join(dir, `core-${name}`);
      fs.mkdirSync(path.join(core, "scripts", "lib"), { recursive: true });
      const called = path.join(core, "called.json");
      fs.writeFileSync(path.join(core, "scripts", "lib", "run-cost-report.js"), throws ? 'throw new Error("at load");\n'
        : `exports.reportForRun = (root, timings) => {
  require("node:fs").writeFileSync(${JSON.stringify(called)}, JSON.stringify({ root, timings }));
  return ["STAND-IN REPORT"];
};\n`);
      return { core, called };
    };
    const selfTimingSuite = (d, name, lines, code = 0) => {
      const file = path.join(d, `${name}.test.sh`);
      fs.writeFileSync(file, `printf '${lines.map((l) => `${l}\\n`).join("")}' >>"$VAULT_FILE_SECONDS"\nexit ${code}\n`);
      return `bash ${file}`;
    };
    const scratch = (name) => {
      const d = path.join(dir, `cost-${name}`);
      fs.mkdirSync(d);
      return d;
    };
    const ROOT = spawnSync("git", ["rev-parse", "--show-toplevel"], { cwd: __dirname, encoding: "utf8" }).stdout.trim();
    const quiet = (core) => ({ VAULT_MEMINFO: meminfo(AMPLE), VAULT_PS: QUIET, CI: "", WORKFLOW_CORE_DIR: core });

    for (const red of [false, true]) {
      test(`a ${red ? "red" : "green"} run hands the report each file's own seconds, after the suites' output, and exits as its suites ${red ? "failed" : "passed"}`, async () => {
        const d = scratch(red ? "red" : "green");
        const { core, called } = coreStandIn(red ? "red" : "green");
        const one = path.join(d, "one.test.py");
        fs.writeFileSync(one, `import sys\nsys.exit(${red ? 1 : 0})\n`);
        const many = selfTimingSuite(d, "many", ["test/a.test.js\t1.250", "test/b.test.js\t0.040"]);
        const proc = await run([`python3 ${one}`, many, "true"],
          quiet(core));
        assert.equal(proc.status, red ? 1 : 0, proc.stderr);
        assert.equal(proc.stderr.includes(`FAIL ${one}`), red);
        const { root, timings } = JSON.parse(fs.readFileSync(called, "utf8"));
        assert.equal(root, ROOT);
        assert.deepEqual(Object.keys(timings).sort(), [one, "test/a.test.js", "test/b.test.js"].sort());
        assert.equal(timings["test/a.test.js"], 1.25);
        assert.equal(timings["test/b.test.js"], 0.04);
        assert.ok(Number.isFinite(timings[one]) && timings[one] >= 0, `${timings[one]} s for one.test.py`);
        assert.match(proc.stdout, /\n== true \(\d+ s\)\n(.*\n)*STAND-IN REPORT\n$/);
      });
    }

    test("with CI set the report is not called", async () => {
      const d = scratch("ci");
      const { core, called } = coreStandIn("ci");
      const proc = await run([selfTimingSuite(d, "many", ["test/a.test.js\t12"])], { ...quiet(core), CI: "true" });
      assert.equal(proc.status, 0, proc.stderr);
      assert.equal(fs.existsSync(called), false);
      assert.doesNotMatch(proc.stdout, /STAND-IN|run-cost/);
    });

    for (const code of [0, 1]) {
      test(`a report that will not run prints one line and leaves the exit at ${code}`, async () => {
        const d = scratch(`broken-${code}`);
        const { core } = coreStandIn(`broken-${code}`, { throws: true });
        const many = selfTimingSuite(d, "many", ["test/a.test.js\t12"], code);
        const proc = await run([many], quiet(core));
        assert.equal(proc.status, code, proc.stderr);
        assert.equal(proc.stdout.match(/run-cost/g).length, 1);
        assert.match(proc.stdout, /test\/run-lanes\.sh: workflow-core's run-cost report would not run \(at load\); the suites' verdict stands \(#370\)\.\n$/);
        assert.deepEqual(proc.stderr.split("\n").filter(Boolean), code ? [`FAIL ${many.replace(/^bash /, "")}`] : []);
      });
    }

    test("the core's own report names a new test file timed past its budget, after the suites' output", async () => {
      const d = scratch("core");
      const git = (...args) => spawnSync("git", ["-c", "user.name=t", "-c", "user.email=t@t", ...args], { cwd: d, encoding: "utf8" });
      git("init", "-q");
      fs.writeFileSync(path.join(d, "old.test.py"), "");
      git("add", "old.test.py");
      git("commit", "-qm", "base");
      fs.writeFileSync(path.join(d, "new.test.py"), "");
      const proc = await run([selfTimingSuite(d, "many", ["new.test.py\t12.5", "old.test.py\t11"])],
        { ...quiet(undefined), WFC_SHARD_TIMINGS: path.join(d, "absent.csv") }, { cwd: d });
      assert.equal(proc.status, 0, proc.stderr);
      assert.match(proc.stdout, /^== bash .*many\.test\.sh \(\d+ s\)\nRUN COST: new\.test\.py took 12\.5 s, over the 10 s budget — new since HEAD: /);
      assert.doesNotMatch(proc.stdout, /old\.test\.py/);
    });
  });
});
