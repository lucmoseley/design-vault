"use strict";
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

const isPath = (rel) => fs.existsSync(path.join(ROOT, rel));
const isFile = (rel) => isPath(rel) && fs.statSync(path.join(ROOT, rel)).isFile();

function pathsNamedIn(file, gone) {
  const out = [];
  const text = fs.readFileSync(path.join(ROOT, file), "utf8");
  if (file.endsWith(".py")) {
    for (const [, name] of text.matchAll(PY_IMPORT)) {
      const rel = path.posix.join(path.posix.dirname(file), `${name}.py`);
      if (rel !== file && (gone.has(rel) || isFile(rel))) out.push({ rel, lone: false });
    }
  }
  for (const [run] of text.matchAll(RUN_OF_PARTS)) {
    const parts = [...run.matchAll(/["']([^"']+)["']/g)].map((m) => m[1]);
    const lone = parts.length === 1 && !parts[0].includes("/");
    const bases = lone ? [path.posix.dirname(file)] : [path.posix.dirname(file), "."];
    for (const base of bases) {
      const rel = path.posix.join(base, ...parts).replace(/\/+$/, "");
      if (rel === "." || rel.startsWith("..") || file.startsWith(`${rel}/`) || !(gone.has(rel) || isPath(rel))) continue;
      out.push({ rel, lone });
      break;
    }
  }
  return out;
}

const isCode = (rel) => /\.(py|js|sh)$/.test(rel);
const filesUnder = (dir) => fs.readdirSync(path.join(ROOT, dir), { recursive: true })
  .map((rel) => path.posix.join(dir, rel.split(path.sep).join("/")));

function reads(entries, gone) {
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
    for (const { rel, lone } of pathsNamedIn(file, gone)) {
      if (seen.has(rel)) continue;
      seen.add(rel);
      if (!lone || isFile(rel)) queue.push(rel);
    }
  }
  return seen;
}

const isCoveredBy = (read, p) => [...read].some((r) => p === r || p.startsWith(`${r}/`));
const isPlacedBy = (read, p) => read.has(p) || [...read].some((r) => r.startsWith("test/") && p.startsWith(`${r}/`));

function entries(suite) {
  const words = suite.split(/\s+/).filter(isFile);
  if (words.length) return words;
  return fs.readdirSync(path.join(ROOT, "test"), { recursive: true })
    .map((rel) => path.posix.join("test", rel.split(path.sep).join("/")))
    .filter((rel) => rel.endsWith(".js"));
}

const REGISTRY = /^registry='([^']*)'$/m;

function registryChange(before, after) {
  if (before == null || after == null || !REGISTRY.test(before) || !REGISTRY.test(after)) return null;
  if (before.replace(REGISTRY, "") !== after.replace(REGISTRY, "")) return null;
  const lines = (text) => text.match(REGISTRY)[1].split("\n");
  const had = new Set(lines(before));
  return lines(after).filter((l) => !had.has(l)).map((l) => l.split("\t")[0]);
}

const withDirsAbove = (p) => p.split("/").map((_, i, parts) => parts.slice(0, i + 1).join("/"));

function plan(suites, staged, side = {}) {
  const changed = staged.filter((p) => RUNNER.has(p));
  const relisted = changed.length === 1 && changed[0] === "test/all.sh" ? registryChange(side.before, side.after) : null;
  if (changed.length && !relisted) return { all: `${changed[0]} is staged, and it decides which suites run` };
  const gone = new Set((side.gone ?? []).flatMap(withDirsAbove));
  const read = new Map(suites.map((s) => [s, reads(entries(s), gone)]));
  const stray = staged.find((p) => MUST_BE_READ.test(p) && !gone.has(p) && ![...read.values()].some((r) => isPlacedBy(r, p)));
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

function planSides(suites, sides, after) {
  const plans = sides.map((side) => ({ label: side.label, ...plan(suites, side.staged, { before: side.before, after, gone: side.gone }) }));
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
