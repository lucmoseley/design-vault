"use strict";
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.join(__dirname, "..");
const SELF = "test/select-suites.js";
const GIT_ABBREV = 7;
const RUNNER = new Set(["test/all.sh", "test/select-suites.js", "package.json", "package-lock.json"]);
const MUST_BE_READ = /^(test\/|plugin\/(.+\/)?scripts\/)/;
const PART = String.raw`(?:"[\w.@+/-]+"|'[\w.@+/-]+')`;
const RUN_OF_PARTS = new RegExp(String.raw`${PART}(?:\s*,\s*${PART})*`, "g");
const PY_IMPORT = /^(?:import|from)\s+(\w+)/gm;

const isCode = (rel) => /\.(py|js|sh)$/.test(rel);

const posixUnder = (dir, rels) => rels.map((rel) => path.posix.join(dir, rel.split(path.sep).join("/")));
const workTree = {
  isPath: (rel) => fs.existsSync(path.join(ROOT, rel)),
  isFile: (rel) => workTree.isPath(rel) && fs.statSync(path.join(ROOT, rel)).isFile(),
  read: (rel) => fs.readFileSync(path.join(ROOT, rel), "utf8"),
  filesUnder: (dir) => posixUnder(dir, fs.readdirSync(path.join(ROOT, dir), { recursive: true })),
  testFiles: () => posixUnder("test", fs.readdirSync(path.join(ROOT, "test"), { recursive: true })),
};

function commitTree(rev) {
  const git = (args, input) => execFileSync("git", args, { cwd: ROOT, input, maxBuffer: 1 << 30 });
  const blobs = git(["ls-tree", "-r", "-z", "--full-tree", rev]).toString("utf8").split("\0")
    .map((entry) => entry.match(/^\d+ blob (\w+)\t(.+)$/s)).filter(Boolean).map(([, sha, rel]) => ({ sha, rel }));
  const files = blobs.map((b) => b.rel);
  const fileSet = new Set(files);
  const dirs = new Set(files.flatMap((f) => f.split("/").slice(0, -1).map((_, i, parts) => parts.slice(0, i + 1).join("/"))));
  const code = blobs.filter((b) => isCode(b.rel));
  const batch = git(["cat-file", "--batch"], code.map((b) => `${b.sha}\n`).join(""));
  const texts = new Map();
  let at = 0;
  for (const { rel: f } of code) {
    const eol = batch.indexOf(10, at);
    const size = Number(batch.toString("utf8", at, eol).split(" ")[2]);
    texts.set(f, batch.toString("utf8", eol + 1, eol + 1 + size));
    at = eol + 1 + size + 1;
  }
  return {
    isPath: (rel) => fileSet.has(rel) || dirs.has(rel),
    isFile: (rel) => fileSet.has(rel),
    read: (rel) => texts.get(rel),
    filesUnder: (dir) => files.filter((f) => f.startsWith(`${dir}/`)),
    testFiles: () => files.filter((f) => f.startsWith("test/")),
  };
}

function pathsNamedIn(tree, file) {
  const out = [];
  const text = tree.read(file);
  if (file.endsWith(".py")) {
    for (const [, name] of text.matchAll(PY_IMPORT)) {
      const rel = path.posix.join(path.posix.dirname(file), `${name}.py`);
      if (rel !== file && tree.isFile(rel)) out.push({ rel, lone: false });
    }
  }
  for (const [run] of text.matchAll(RUN_OF_PARTS)) {
    const parts = [...run.matchAll(/["']([^"']+)["']/g)].map((m) => m[1]);
    const lone = parts.length === 1 && !parts[0].includes("/");
    const bases = lone ? [path.posix.dirname(file)] : [path.posix.dirname(file), "."];
    for (const base of bases) {
      const rel = path.posix.join(base, ...parts).replace(/\/+$/, "");
      if (rel === "." || rel.startsWith("..") || file.startsWith(`${rel}/`) || !tree.isPath(rel)) continue;
      out.push({ rel, lone });
      break;
    }
  }
  return out;
}

function reads(tree, entries) {
  const seen = new Set(entries);
  const followed = new Set();
  const queue = [...entries];
  while (queue.length) {
    const file = queue.shift();
    if (file === SELF || followed.has(file) || !tree.isPath(file)) continue;
    followed.add(file);
    if (!tree.isFile(file)) {
      queue.push(...tree.filesUnder(file).filter(isCode));
      continue;
    }
    if (!isCode(file)) continue;
    for (const { rel, lone } of pathsNamedIn(tree, file)) {
      if (seen.has(rel)) continue;
      seen.add(rel);
      if (!lone || tree.isFile(rel)) queue.push(rel);
    }
  }
  return seen;
}

const isCoveredBy = (read, p) => [...read].some((r) => p === r || p.startsWith(`${r}/`));
const isPlacedBy = (read, p) => read.has(p) || [...read].some((r) => r.startsWith("test/") && p.startsWith(`${r}/`));

function entries(tree, suite) {
  const words = suite.split(/\s+/).filter(tree.isFile);
  if (words.length) return words;
  return tree.testFiles().filter((rel) => rel.endsWith(".js"));
}

const REGISTRY = /^registry='([^']*)'$/m;

function registryChange(before, after) {
  if (before == null || after == null || !REGISTRY.test(before) || !REGISTRY.test(after)) return null;
  if (before.replace(REGISTRY, "") !== after.replace(REGISTRY, "")) return null;
  const lines = (text) => text.match(REGISTRY)[1].split("\n");
  const had = new Set(lines(before));
  return lines(after).filter((l) => !had.has(l)).map((l) => l.split("\t")[0]);
}

function plan(suites, staged, side = {}) {
  const changed = staged.filter((p) => RUNNER.has(p));
  const relisted = changed.length === 1 && changed[0] === "test/all.sh" ? registryChange(side.before, side.after) : null;
  if (changed.length && !relisted) return { all: `${changed[0]} is staged, and it decides which suites run` };
  const readIn = (tree) => new Map(suites.map((s) => [s, reads(tree, entries(tree, s))]));
  const now = readIn(workTree);
  const gone = new Set(side.gone ?? []);
  const then = gone.size ? readIn(commitTree(side.rev)) : null;
  const read = (suite, p) => (gone.has(p) ? then : now).get(suite);
  const stray = staged.find((p) => MUST_BE_READ.test(p) && !suites.some((s) => isPlacedBy(read(s, p), p)));
  if (stray) return { all: `${stray} is staged, and no suite is known to read it` };
  return {
    suites: suites.map((suite) => ({
      suite,
      why: !suite.startsWith("python3 ") || relisted?.includes(suite) || staged.some((p) => isCoveredBy(read(suite, p), p))
        ? null
        : `none of the ${staged.length} staged file(s) is one it reads`,
    })),
  };
}

function planSides(suites, sides, after) {
  const plans = sides.map((side) => ({ label: side.label, ...plan(suites, side.staged, { before: side.before, after, gone: side.gone, rev: side.rev }) }));
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
  const readCopy = (file) => (file && fs.existsSync(file) ? fs.readFileSync(file, "utf8") : null);
  const dir = process.env.VAULT_SIDES_DIR ?? "";
  const sides = (process.env.VAULT_SIDES ?? "").split(" ").filter(Boolean).map((name) => ({
    label: name === "HEAD" ? name : name.slice(0, GIT_ABBREV),
    rev: name,
    staged: fs.readFileSync(path.join(dir, `${name}.paths`), "utf8").split("\n").filter(Boolean),
    gone: fs.readFileSync(path.join(dir, `${name}.gone`), "utf8").split("\n").filter(Boolean),
    before: readCopy(path.join(dir, `${name}.head`)),
  }));
  if (!sides.length) throw new Error("select-suites.js: VAULT_SIDES names no side to judge the commit against");
  const p = planSides(process.argv.slice(3), sides, readCopy(process.env.VAULT_RUNNER_STAGED));
  if (p.all) console.log(`all\t${p.all}`);
  else for (const { suite, why } of p.suites) console.log(why ? `skip\t${suite}\t${why}` : `run\t${suite}`);
}

module.exports = { plan, planSides };
