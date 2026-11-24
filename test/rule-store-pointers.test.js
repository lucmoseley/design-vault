"use strict";
// The pointers into the vault's store of rule records (#265): gate.md is gone, so nothing a round reads may still send
// an agent to it; every record's `reasons` names a heading that exists; every link the plugin makes into the store
// lands on a file there; and each reference section's Records line names every record whose `reasons` points at it.
// It reads the live plugin tree, not fixtures, so the commit that adds a stale pointer is the one refused.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");
const { RECORD_COUNT, storeRecords } = require("./rule-store.js");

const ROOT = path.join(__dirname, "..");
const SKILLS = path.join(ROOT, "plugin", "skills");

/** Every file under `dir` whose name matches `pattern`, as absolute paths. */
function walk(dir, pattern) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) return e.name === "__pycache__" || e.name === "node_modules" ? [] : walk(full, pattern);
    return pattern.test(e.name) ? [full] : [];
  });
}

/** A heading's anchor as GitHub renders it: lower-cased, punctuation but hyphens dropped, spaces as hyphens. */
const anchor = (heading) => heading.trim().toLowerCase().replace(/[^\p{L}\p{N} -]/gu, "").replace(/ /g, "-");
const sectionRecords = new Map();
function readSectionRecords(file) {
  if (sectionRecords.has(file)) return sectionRecords.get(file);
  const named = new Map();
  let section;
  for (const line of fs.readFileSync(file, "utf8").split("\n")) {
    const heading = line.match(/^#{1,6} (.*)$/);
    if (heading) named.set((section = anchor(heading[1])), []);
    else if (section && /^Records?: /.test(line)) named.get(section).push(...[...line.matchAll(/`([^`]+)`/g)].map((m) => m[1]));
  }
  sectionRecords.set(file, named);
  return named;
}
const anchors = (file) => new Set(readSectionRecords(file).keys());

// The old home's name, not a project's fit-gate.md.
const OLD_HOME = /(?<![\w-])gate\.md\b/;

// The calibration run reads an old round's gate from git history, where it was this one file.
const HISTORY_READERS = ["plugin/skills/design-round/references/calibration.md"];

test("no file a round reads names gate.md, the store's old home, save to read it from history", () => {
  const read = [...walk(path.join(ROOT, "plugin"), /\.(md|js|py|sh|json)$/), ...fs.readdirSync(ROOT).filter((n) => n.endsWith(".js")).map((n) => path.join(ROOT, n))];
  // A guess well under the 60-odd files the plugin and the root held at #265: fewer means the walk went wrong.
  assert.ok(read.length > 40, `only ${read.length} files read`);
  const naming = read.map((f) => path.relative(ROOT, f)).filter((f) => !HISTORY_READERS.includes(f) && OLD_HOME.test(fs.readFileSync(path.join(ROOT, f), "utf8")));
  assert.deepEqual(naming, []);
});

test("every record's reasons names a heading that exists in a file under the plugin's skills folder", () => {
  const records = storeRecords();
  assert.equal(records.length, RECORD_COUNT);
  for (const q of records) {
    const [file, hash] = q.fields.reasons.value.split("#");
    const target = path.join(SKILLS, file);
    assert.ok(fs.existsSync(target), `${q.id}: ${file} does not exist`);
    assert.ok(hash && anchors(target).has(hash), `${q.id}: ${file} has no heading #${hash}`);
  }
});

test("a reference section's Records line names every record whose reasons point at it", () => {
  const drift = [];
  let checked = 0;
  for (const q of storeRecords()) {
    const [file, hash] = q.fields.reasons.value.split("#");
    if (!/\/references\/[^/]+\.md$/.test(file)) continue;
    const ids = readSectionRecords(path.join(SKILLS, file)).get(hash);
    // #540
    if (!ids?.length) continue;
    checked++;
    if (!ids.includes(q.id)) drift.push(`${file}#${hash} omits ${q.id}`);
  }
  // measured 397 at #511; 350 a guess under it
  assert.ok(checked > 350, `only ${checked} records checked`);
  assert.deepEqual(drift, []);
});

test("every link the plugin makes into the store, or to rules.md, lands on a file there", () => {
  let links = 0;
  for (const file of walk(path.join(ROOT, "plugin"), /\.md$/)) {
    for (const [, href] of fs.readFileSync(file, "utf8").matchAll(/\]\(([^)\s]*rules(?:\/[^)\s]*|\.md[^)\s]*)?)\)/g)) {
      const [target, hash] = href.split("#");
      const resolved = path.resolve(path.dirname(file), target);
      if (!resolved.startsWith(path.join(SKILLS, "design-critique", "rules"))) continue;
      links++;
      assert.ok(fs.existsSync(resolved), `${path.relative(ROOT, file)} links ${href}, which does not exist`);
      if (hash) assert.ok(anchors(resolved).has(hash), `${path.relative(ROOT, file)} links ${href}, which has no such heading`);
    }
  }
  // Each store file's own link to rules.md makes 10 at #265: fewer means the match went wrong.
  assert.ok(links >= 10, `only ${links} links into the store found`);
});
