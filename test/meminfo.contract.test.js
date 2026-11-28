"use strict";
const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { fakeMeminfo, meminfoLine } = require("./meminfo-fake");

const dir = fs.mkdtempSync(path.join(os.tmpdir(), "meminfo-contract-"));
after(() => fs.rmSync(dir, { recursive: true, force: true }));

const availableMb = (file) => spawnSync("bash", ["-c", 'set -u; source "$0"; available_mb', path.join(__dirname, "lane-readers.sh")],
  { encoding: "utf8", env: { ...process.env, VAULT_MEMINFO: file } });

test("the kernel's MemAvailable line has the fake's shape, and run-lanes reads each as its kB over 1024", () => {
  const real = fs.readFileSync("/proc/meminfo", "utf8");
  const snapshot = path.join(dir, "meminfo-real");
  fs.writeFileSync(snapshot, real);
  const line = real.split("\n").find((l) => l.startsWith("MemAvailable:"));
  const kb = Number(line.match(/(\d+) kB$/)[1]);
  assert.equal(meminfoLine("MemAvailable", kb), line);
  const mb = Math.floor(kb / 1024);
  for (const file of [snapshot, fakeMeminfo(dir, mb)]) {
    const r = availableMb(file);
    assert.equal(r.status, 0, r.stderr);
    assert.equal(r.stdout, `${mb}\n`, file);
  }
});
