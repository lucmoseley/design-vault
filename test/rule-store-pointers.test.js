"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");
const { RECORD_COUNT, storeRecords } = require("./rule-store.js");

const ROOT = path.join(__dirname, "..");
const SKILLS = path.join(ROOT, "plugin", "skills");

function walk(dir, pattern) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) return e.name === "__pycache__" || e.name === "node_modules" ? [] : walk(full, pattern);
    return pattern.test(e.name) ? [full] : [];
  });
}

const anchor = (heading) => heading.trim().toLowerCase().replace(/[^\p{L}\p{N} -]/gu, "").replace(/ /g, "-");
const parseTicked = (line) => [...line.matchAll(/`([^`]+)`/g)].map((m) => m[1]);
const parseReasons = (q) => {
  const [file, hash] = q.fields.reasons.value.split("#");
  return { file, hash };
};
const sections = new Map();
function readSections(file) {
  if (sections.has(file)) return sections.get(file);
  const bySection = new Map();
  let section;
  for (const line of fs.readFileSync(file, "utf8").split("\n")) {
    const heading = line.match(/^#{1,6} (.*)$/);
    if (heading) bySection.set(anchor(heading[1]), (section = { recordsLine: [], mentioned: new Set() }));
    else if (section) {
      if (/^Records?: /.test(line)) section.recordsLine.push(...parseTicked(line));
      for (const t of parseTicked(line)) section.mentioned.add(t);
    }
  }
  sections.set(file, bySection);
  return bySection;
}
const anchors = (file) => new Set(readSections(file).keys());
const REFERENCE = /\/references\/[^/]+\.md$/;

const OLD_HOME = /(?<![\w-])gate\.md\b/;

const HISTORY_READERS = ["plugin/skills/design-round/references/calibration.md"];

test("no file a round reads names gate.md, the store's old home, save to read it from history", () => {
  const read = [...walk(path.join(ROOT, "plugin"), /\.(md|js|py|sh|json)$/), ...fs.readdirSync(ROOT).filter((n) => n.endsWith(".js")).map((n) => path.join(ROOT, n))];
  // measured 60-odd at #265; 40 a guess under it
  assert.ok(read.length > 40, `only ${read.length} files read`);
  const naming = read.map((f) => path.relative(ROOT, f)).filter((f) => !HISTORY_READERS.includes(f) && OLD_HOME.test(fs.readFileSync(path.join(ROOT, f), "utf8")));
  assert.deepEqual(naming, []);
});

test("every record's reasons names a heading that exists in a file under the plugin's skills folder", () => {
  const records = storeRecords();
  assert.equal(records.length, RECORD_COUNT);
  for (const q of records) {
    const { file, hash } = parseReasons(q);
    const target = path.join(SKILLS, file);
    assert.ok(fs.existsSync(target), `${q.id}: ${file} does not exist`);
    assert.ok(hash && anchors(target).has(hash), `${q.id}: ${file} has no heading #${hash}`);
  }
});

test("a reference section names every record whose reasons point at it, on its Records line where it has one, listing each omission", () => {
  const drift = [];
  let checked = 0;
  for (const q of storeRecords()) {
    const { file, hash } = parseReasons(q);
    if (!REFERENCE.test(file)) continue;
    const section = readSections(path.join(SKILLS, file)).get(hash);
    assert.ok(section, `${q.id}: ${file} has no heading #${hash}`);
    checked++;
    const { recordsLine, mentioned } = section;
    if (recordsLine.length ? !recordsLine.includes(q.id) : !mentioned.has(q.id)) drift.push(`${file}#${hash} omits ${q.id}`);
  }
  // measured 469 at #540; 430 a guess under it
  assert.ok(checked > 430, `only ${checked} records checked`);
  assert.deepEqual(drift, []);
});

test("a reference section's Records line names only records whose reasons point at that section, listing each misplaced id", () => {
  const reasons = new Map(storeRecords().map((q) => [q.id, parseReasons(q)]));
  const drift = [];
  let lines = 0;
  for (const file of walk(SKILLS, /\.md$/).filter((f) => REFERENCE.test(f))) {
    const rel = path.relative(SKILLS, file);
    for (const [hash, { recordsLine }] of readSections(file)) {
      if (recordsLine.length) lines++;
      for (const id of recordsLine) {
        const r = reasons.get(id);
        if (r?.file !== rel || r.hash !== hash) drift.push(`${rel}#${hash} names ${id}, whose reasons are ${r ? `${r.file}#${r.hash}` : "absent"}`);
      }
    }
  }
  // measured 283 at #540; 250 a guess under it
  assert.ok(lines > 250, `only ${lines} Records lines read`);
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
  // measured 10 at #265
  assert.ok(links >= 10, `only ${links} links into the store found`);
});
