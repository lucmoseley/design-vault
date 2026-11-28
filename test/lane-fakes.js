"use strict";
// #629
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

function viaReaders(fn, env = {}) {
  const full = { ...process.env, ...env };
  for (const seam of ["VAULT_PS", "VAULT_MEMINFO"]) if (!(seam in env)) delete full[seam];
  return spawnSync("bash", ["-c", `set -u; declare -A lane=(); source "$0"; ${fn}`, path.join(__dirname, "lane-readers.sh")],
    { encoding: "utf8", env: full });
}

const AMPLE_MB = Number(fs.readFileSync(path.join(__dirname, "run-lanes.sh"), "utf8").match(/^rungs=\(.* (\d+)\)$/m)[1]);

// https://github.com/torvalds/linux/blob/master/fs/proc/meminfo.c
const meminfoLine = (name, kb) => `${`${name}:`.padEnd(16)}${String(kb).padStart(8)} kB`;

function fakeMeminfo(dir, mb) {
  const file = path.join(dir, `meminfo-${mb}`);
  if (!fs.existsSync(file)) fs.writeFileSync(file, `${meminfoLine("MemTotal", 10162176)}\n${meminfoLine("MemAvailable", mb * 1024)}\n`);
  return file;
}

const psLines = (args) => args.map((a, i) => `${String(11 + i).padStart(7)} ${a}`).join("\n");

function fakePs(dir, name, args = []) {
  const file = path.join(dir, `ps-${name}`);
  fs.writeFileSync(file, args.length ? `#!/bin/sh\ncat <<'EOF'\n${psLines(args)}\nEOF\n` : "#!/bin/sh\n", { mode: 0o755 });
  return file;
}

function idleMachine(dir) {
  const cgroup = path.join(dir, "cgroup-unlimited");
  fs.mkdirSync(cgroup, { recursive: true });
  return {
    VAULT_PS: fakePs(dir, "quiet"), VAULT_MEMINFO: fakeMeminfo(dir, AMPLE_MB), VAULT_CGROUP: cgroup,
    WFC_GATE_SEAT: "", VAULT_SUITE_LANES: "", VAULT_LANE_WAIT_S: "", VAULT_SUITE_BUDGET: "", VAULT_SUITE_TIMES: "",
  };
}

module.exports = { AMPLE_MB, fakeMeminfo, fakePs, idleMachine, meminfoLine, psLines, viaReaders };
