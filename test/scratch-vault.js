"use strict";
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.join(__dirname, "..");

function buildScratchVault(root, stubs) {
  fs.mkdirSync(path.join(root, "test"), { recursive: true });
  fs.mkdirSync(path.join(root, "scripts", "lib"), { recursive: true });
  fs.copyFileSync(path.join(ROOT, "test", "all.sh"), path.join(root, "test", "all.sh"));
  fs.copyFileSync(path.join(ROOT, "scripts", "lib", "resolve-core.js"), path.join(root, "scripts", "lib", "resolve-core.js"));
  for (const [file, body] of Object.entries(stubs)) fs.writeFileSync(path.join(root, "test", file), body);
  execFileSync("git", ["init", "-q", "-b", "main"], { cwd: root });
  return root;
}

function allShEnv(overrides) {
  const env = { ...process.env, WFC_GATE_SEAT: undefined, VAULT_SUITE_BUDGET: undefined, VAULT_ALL_SUITES: undefined, VAULT_SUITE_TIMES: undefined, ...overrides };
  for (const key of Object.keys(env)) if (env[key] === undefined) delete env[key];
  return env;
}

module.exports = { allShEnv, buildScratchVault };
