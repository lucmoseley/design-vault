"use strict";
// Which of test/all.sh's suites a commit's staged files can break (#146), judged against HEAD and each merge parent
// (#457). all.sh runs
//   VAULT_SIDES_DIR=<dir> VAULT_SIDES=<HEAD and each parent's sha> VAULT_RUNNER_STAGED=<the commit's all.sh> \
//     node test/select-suites.js --select <suite>…
// which prints `all<TAB><why>` where every suite must run, else `run<TAB><suite>` or `skip<TAB><suite><TAB><why>`
// for each. Only the Python suites are ever skipped; the rest are the fast checks.
// node --test with no arguments also loads this file as a test file of no tests, which is harmless.
const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.join(__dirname, "..");
// This file's path literals are what it looks for, not what it reads.
const SELF = "test/select-suites.js";
// A merge parent is labelled by its sha cut to git's default abbreviation.
const GIT_ABBREV = 7;
// Staging one of these can change which suites run or what they run on.
const RUNNER = new Set(["test/all.sh", "test/select-suites.js", "package.json", "package-lock.json"]);
// A staged file in here that no suite is seen to read runs every suite, since the reading below misses some forms.
const MUST_BE_READ = /^(test\/|plugin\/(.+\/)?scripts\/)/;
// A run of quoted path parts joined by commas: `os.path.join(HERE, "fixtures", "flow")`, `"check-flow.py"`,
// `require("../plugin/…/fall.js")`. Read from the files themselves, so a checker that starts loading another this
// way is seen. Not followed: pathlib's `/`, a `require` without its extension, a join that starts from a variable
// other than the file's own directory or the repo top.
const PART = String.raw`(?:"[\w.@+/-]+"|'[\w.@+/-]+')`;
const RUN_OF_PARTS = new RegExp(String.raw`${PART}(?:\s*,\s*${PART})*`, "g");
// A Python `import name` or `from name import …` at a line's start, read as the module beside the file: the suites put
// their own directory on the path to import test/child.py (#454).
const PY_IMPORT = /^(?:import|from)\s+(\w+)/gm;

const isPath = (rel) => fs.existsSync(path.join(ROOT, rel));
const isFile = (rel) => isPath(rel) && fs.statSync(path.join(ROOT, rel)).isFile();

/**
 * The repo paths `file` names, each resolved from its own directory, or else from the repo top where it is more than
 * one bare word (a lone `"data"` is as often a dictionary key), kept where it exists.
 */
function pathsNamedIn(file) {
  const out = [];
  const text = fs.readFileSync(path.join(ROOT, file), "utf8");
  if (file.endsWith(".py")) {
    for (const [, name] of text.matchAll(PY_IMPORT)) {
      const rel = path.posix.join(path.posix.dirname(file), `${name}.py`);
      if (rel !== file && isFile(rel)) out.push({ rel, lone: false });
    }
  }
  for (const [run] of text.matchAll(RUN_OF_PARTS)) {
    const parts = [...run.matchAll(/["']([^"']+)["']/g)].map((m) => m[1]);
    const lone = parts.length === 1 && !parts[0].includes("/");
    const bases = lone ? [path.posix.dirname(file)] : [path.posix.dirname(file), "."];
    for (const base of bases) {
      const rel = path.posix.join(base, ...parts).replace(/\/+$/, "");
      // `..` to the repo top, or `.`, names the tree the file sits in, not something it reads.
      if (rel === "." || rel.startsWith("..") || file.startsWith(`${rel}/`) || !isPath(rel)) continue;
      out.push({ rel, lone });
      break;
    }
  }
  return out;
}

const isCode = (rel) => /\.(py|js|sh)$/.test(rel);
const filesUnder = (dir) => fs.readdirSync(path.join(ROOT, dir), { recursive: true })
  .map((rel) => path.posix.join(dir, rel.split(path.sep).join("/")));

/**
 * Every path `entries` read, following each code file they name in turn. A directory stands for all under it, and the
 * code files under it are followed for what they name, but are not themselves named, so a script there that no suite
 * names still runs every suite. A directory named by a lone bare word is not followed (#382).
 */
function reads(entries) {
  const seen = new Set(entries);
  const followed = new Set();
  const queue = [...entries];
  while (queue.length) {
    const file = queue.shift();
    if (file === SELF || followed.has(file) || !isPath(file)) continue;
    followed.add(file);
    if (!isFile(file)) {
      queue.push(...filesUnder(file).filter(isCode));
      continue;
    }
    if (!isCode(file)) continue;
    for (const { rel, lone } of pathsNamedIn(file)) {
      if (seen.has(rel)) continue;
      seen.add(rel);
      if (!lone || isFile(rel)) queue.push(rel);
    }
  }
  return seen;
}

const isCoveredBy = (read, p) => [...read].some((r) => p === r || p.startsWith(`${r}/`));
// A fixture is placed by the directory a suite reads; a script or a test only by its own name.
const isPlacedBy = (read, p) => read.has(p) || (p.startsWith("test/fixtures/") && isCoveredBy(read, p));

/** The files a suite starts from: those its command names, or for `node --test` every .js file under test/. */
function entries(suite) {
  const words = suite.split(/\s+/).filter(isFile);
  if (words.length) return words;
  return fs.readdirSync(path.join(ROOT, "test"), { recursive: true })
    .map((rel) => path.posix.join("test", rel.split(path.sep).join("/")))
    .filter((rel) => rel.endsWith(".js"));
}

// all.sh's list of suites, one a line: `registry='…'`.
const REGISTRY = /^registry='([^']*)'$/m;

/**
 * The suites on lines an edit to all.sh added or changed, where it changed nothing outside its list of suites (#363),
 * else null. `before` is null where HEAD has no all.sh.
 */
function registryChange(before, after) {
  if (before == null || after == null || !REGISTRY.test(before) || !REGISTRY.test(after)) return null;
  if (before.replace(REGISTRY, "") !== after.replace(REGISTRY, "")) return null;
  const lines = (text) => text.match(REGISTRY)[1].split("\n");
  const had = new Set(lines(before));
  return lines(after).filter((l) => !had.has(l)).map((l) => l.split("\t")[0]);
}

/**
 * { all: why } where every suite must run, else { suites: [{ suite, why }] }, `why` null for one that runs.
 * `runner` holds all.sh as HEAD and the commit have it, so an edit to its list alone runs only the suites it lists anew.
 */
function plan(suites, staged, runner = {}) {
  const changed = staged.filter((p) => RUNNER.has(p));
  const relisted = changed.length === 1 && changed[0] === "test/all.sh" ? registryChange(runner.before, runner.after) : null;
  if (changed.length && !relisted) return { all: `${changed[0]} is staged, and it decides which suites run` };
  const read = new Map(suites.map((s) => [s, reads(entries(s))]));
  const stray = staged.find((p) => MUST_BE_READ.test(p) && ![...read.values()].some((r) => isPlacedBy(r, p)));
  if (stray) return { all: `${stray} is staged, and no suite is known to read it` };
  return {
    suites: suites.map((suite) => ({
      suite,
      why: !suite.startsWith("python3 ") || relisted?.includes(suite) || staged.some((p) => isCoveredBy(read.get(suite), p))
        ? null
        : `none of the ${staged.length} staged file(s) is one it reads`,
    })),
  };
}

/**
 * The plan for a commit judged against each of its parents (#457): `sides` holds, per parent, its `label`, the paths
 * the commit changes from it and all.sh as it has it. A suite whose every read is unchanged from one parent passed
 * there, so a merge runs a suite only where every parent's plan runs it, and every suite only where every plan does.
 */
function planSides(suites, sides, after) {
  const plans = sides.map((side) => ({ label: side.label, ...plan(suites, side.staged, { before: side.before, after }) }));
  const choosing = plans.filter((p) => !p.all);
  if (!choosing.length) return { all: plans[0].all };
  return {
    suites: suites.map((suite, i) => {
      const skipped = choosing.find((p) => p.suites[i].why);
      return { suite, why: skipped ? (plans.length > 1 ? `against ${skipped.label}, ${skipped.suites[i].why}` : skipped.suites[i].why) : null };
    }),
  };
}

if (process.argv[2] === "--select") {
  // all.sh hands over, per parent in VAULT_SIDES_DIR, `<name>.paths` (the paths the commit changes from it) and
  // `<name>.head` (its all.sh, absent where it has none), and the commit's all.sh, each read before it unsets the
  // commit's git environment.
  const readCopy = (file) => (file && fs.existsSync(file) ? fs.readFileSync(file, "utf8") : null);
  const dir = process.env.VAULT_SIDES_DIR ?? "";
  const sides = (process.env.VAULT_SIDES ?? "").split(" ").filter(Boolean).map((name) => ({
    label: name === "HEAD" ? name : name.slice(0, GIT_ABBREV),
    staged: fs.readFileSync(path.join(dir, `${name}.paths`), "utf8").split("\n").filter(Boolean),
    before: readCopy(path.join(dir, `${name}.head`)),
  }));
  if (!sides.length) throw new Error("select-suites.js: VAULT_SIDES names no side to judge the commit against");
  const p = planSides(process.argv.slice(3), sides, readCopy(process.env.VAULT_RUNNER_STAGED));
  if (p.all) console.log(`all\t${p.all}`);
  else for (const { suite, why } of p.suites) console.log(why ? `skip\t${suite}\t${why}` : `run\t${suite}`);
}

module.exports = { plan, planSides };
