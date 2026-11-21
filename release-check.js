#!/usr/bin/env node
/**
 * Prints how many commits touching plugin/ `main` holds past the sha the
 * lucmoseley marketplace pins (#58).
 *
 * Usage:
 *   node release-check.js               reads the pin from lucmoseley/claude-plugins with gh, or $WFC_GH
 *   node release-check.js --pin <sha>   counts past that sha instead
 *   node release-check.js --repo <dir>  counts in that checkout instead of this one
 *
 * It reports and never refuses: every outcome, a failed pin read included,
 * exits 0, since a session start must not fail on the network.
 */
"use strict";

const { execFileSync } = require("child_process");

const MARKETPLACE_API = "repos/lucmoseley/claude-plugins/contents/.claude-plugin/marketplace.json";

const report = (line) => console.log(`design-vault release check: ${line}`);

// The first line of what a failed command said, which names the cause, where
// its message names only the command.
const reason = (err) => (String(err.stderr || "").trim() || err.message).split("\n")[0];

function parsePin(marketplace) {
  const entry = (marketplace.plugins || []).find((p) => p.name === "design-vault");
  return entry?.source?.sha || null;
}

// gh is read from WFC_GH where set, so a test points it at a stub (base §N7, #124). The 10 s timeout is a guess
// at how long a session start may wait on GitHub before this check gives up.
function readPin() {
  const content = execFileSync(process.env.WFC_GH || "gh", ["api", MARKETPLACE_API, "--jq", ".content"], { encoding: "utf8", timeout: 10000, stdio: ["ignore", "pipe", "pipe"] });
  return parsePin(JSON.parse(Buffer.from(content, "base64").toString("utf8")));
}

// Commits on main past `pin` that touch plugin/, or null when this checkout
// does not hold the pin. Throws when `repo` is not a checkout.
function unreleased(repo, pin) {
  const git = (...args) => execFileSync("git", ["-C", repo, ...args], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
  git("rev-parse", "--git-dir");
  try {
    git("cat-file", "-e", `${pin}^{commit}`);
  } catch {
    return null;
  }
  return Number(git("rev-list", "--count", `${pin}..main`, "--", "plugin/").trim());
}

function main(argv) {
  const arg = (name) => {
    const i = argv.indexOf(name);
    return i === -1 ? undefined : argv[i + 1];
  };
  const repo = arg("--repo") || __dirname;
  let pin = arg("--pin");
  if (!pin) {
    try {
      pin = readPin();
    } catch (err) {
      return report(`could not read the marketplace pin (${reason(err)}); unreleased plugin/ commits unknown`);
    }
    if (!pin) return report("the marketplace carries no design-vault sha; unreleased plugin/ commits unknown");
  }
  // Seven hex digits: git's default short sha.
  const short = pin.slice(0, 7);
  let count;
  try {
    count = unreleased(repo, pin);
  } catch (err) {
    return report(`could not count past pin ${short} (${reason(err)})`);
  }
  if (count === null) report(`pin ${short} is not in this checkout; run git fetch, then count again`);
  else if (count === 0) report(`0 unreleased plugin/ commits past pin ${short}`);
  else report(`${count} unreleased plugin/ commits on main past pin ${short} — release them by README §Releasing a plugin change`);
}

if (require.main === module) main(process.argv.slice(2));
