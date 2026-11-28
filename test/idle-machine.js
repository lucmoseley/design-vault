"use strict";
const fs = require("node:fs");
const path = require("node:path");
const { fakeMeminfo } = require("./meminfo-fake");
const { fakePs } = require("./ps-fake");

const AMPLE_MB = Number(fs.readFileSync(path.join(__dirname, "run-lanes.sh"), "utf8").match(/^rungs=\(.* (\d+)\)$/m)[1]);

function idleMachine(dir) {
  const cgroup = path.join(dir, "cgroup-unlimited");
  fs.mkdirSync(cgroup, { recursive: true });
  return {
    VAULT_PS: fakePs(dir, "quiet"), VAULT_MEMINFO: fakeMeminfo(dir, AMPLE_MB), VAULT_CGROUP: cgroup,
    WFC_GATE_SEAT: "", VAULT_SUITE_LANES: "", VAULT_LANE_WAIT_S: "", VAULT_SUITE_BUDGET: "", VAULT_SUITE_TIMES: "",
  };
}

module.exports = { idleMachine };
