"use strict";
const assert = require("node:assert/strict");
const { spawn, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { fakePs, psLines, realPsMatching } = require("./ps-fake");

const dir = fs.mkdtempSync(path.join(os.tmpdir(), "ps-contract-"));
after(() => fs.rmSync(dir, { recursive: true, force: true }));

const suitesCounted = (psBin) => spawnSync("bash", ["-c", 'set -u; source "$0"; others', path.join(__dirname, "lane-readers.sh")],
  { encoding: "utf8", env: { ...process.env, VAULT_PS: psBin } });
const LINE = /^ *(\d+) (.+)$/;
// guess #629
const SHOWN_POLLS = 100;
// guess #629
const SHOWN_POLL_MS = 100;

test("a real ps line for a suite and for a script that is none has the fake's shape and the fake's count",
  { skip: process.env.CI && "ps's live cases run on the founder's machine, never in CI (code-standards base §G7 item 2)" }, async (t) => {
    const held = [["held.test.py", "1"], ["held.py", "0"]].map(([f, n]) => {
      const file = path.join(dir, f);
      fs.writeFileSync(file, "import time\ntime.sleep(60)\n");
      return { file, args: `python3 ${file}`, counted: `${n}\n`, kid: spawn("python3", [file], { stdio: "ignore" }) };
    });
    t.after(() => held.forEach(({ kid }) => kid.kill()));
    const realLine = ({ kid }) => spawnSync("ps", ["-o", "pid=,args=", "-p", String(kid.pid)], { encoding: "utf8" }).stdout.replace(/\n$/, "");
    const shown = () => held.every((h) => realLine(h).match(LINE)?.[2] === h.args);
    for (let i = 0; i < SHOWN_POLLS && !shown(); i++) await new Promise((r) => setTimeout(r, SHOWN_POLL_MS));
    assert.ok(shown(), "the held processes never showed their args to ps");
    for (const [i, h] of held.entries()) {
      assert.equal(realLine(h).match(LINE)[1], String(h.kid.pid));
      assert.equal(psLines([h.args]).match(LINE)[2], h.args);
      for (const psBin of [realPsMatching(dir, `real-${i}`, h.file), fakePs(dir, `fake-${i}`, [h.args])]) {
        const r = suitesCounted(psBin);
        assert.equal(r.status, 0, r.stderr);
        assert.equal(r.stdout, h.counted, `${h.args} through ${psBin}`);
      }
    }
    const whole = suitesCounted("ps");
    assert.equal(whole.status, 0, whole.stderr);
    assert.ok(Number(whole.stdout) >= 1, `the whole of ps counted ${whole.stdout.trim()} suites`);
  });
