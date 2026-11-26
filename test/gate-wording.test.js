"use strict";
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");
const { parseGate } = require("../plugin/skills/design-round/scripts/gate-form.js");
const { RECORD_COUNT } = require("./rule-store.js");

const ROOT = path.join(__dirname, "..");
const SCANNED = ["plugin", "data"]; // #154
const TEXT = /\.(md|js|json|py|sh|html|css|txt)$/;
const BUNDLE = "data/vault-data.js";
const RUN = 8; // guess, #165

const normalised = (text) =>
  text.normalize("NFKC").toLowerCase().replace(/['’]/g, "").split(/[^\p{L}\p{N}]+/u).filter(Boolean).join(" ");
const SLOT = /<[^<>]*>/g;

function stringValues(value) {
  if (typeof value === "string") return [value];
  if (value && typeof value === "object") return Object.values(value).flatMap(stringValues);
  return [];
}

const readable = (file, raw) => (file.endsWith(".json") ? stringValues(JSON.parse(raw)).join("\n") : raw);

function scannedFiles(root) {
  const out = [];
  const walk = (rel) => {
    for (const entry of fs.readdirSync(path.join(root, rel), { withFileTypes: true })) {
      const child = path.posix.join(rel, entry.name);
      if (entry.isDirectory()) {
        if (entry.name !== "__pycache__" && entry.name !== "node_modules") walk(child);
      } else if (TEXT.test(entry.name) && child !== BUNDLE) {
        out.push({ file: child, text: readable(child, fs.readFileSync(path.join(root, child), "utf8")) });
      }
    }
  };
  for (const dir of SCANNED) if (fs.existsSync(path.join(root, dir))) walk(dir);
  return out;
}

// #349, #462
const digest = (text) => crypto.createHash("sha1").update(text).digest("hex");
const hashes = new WeakMap();
const hashOf = (file) => {
  if (!hashes.has(file)) hashes.set(file, digest(file.text));
  return hashes.get(file);
};
const kept = new Map();
const keep = (key, make) => {
  if (!kept.has(key)) kept.set(key, make());
  return kept.get(key);
};

const questionsIn = (text) =>
  parseGate(text).questions.map((q) => ({
    id: q.id,
    words: normalised((q.fields.question?.value ?? "").replace(SLOT, " ")).split(" ").filter(Boolean),
  }));

const runAt = (words, start, size) => words.slice(start, start + size).join(" ");

function firstWindows(words, windows, sizes) {
  const first = new Map();
  for (const size of sizes) {
    for (let j = 0; j + size <= words.length; j++) {
      for (const [n, i] of windows.get(runAt(words, j, size)) ?? []) {
        const earlier = first.get(n);
        if (earlier === undefined || i < earlier) first.set(n, i);
      }
    }
  }
  return first;
}

function copies(files) {
  const hashed = files.map((f) => ({ ...f, hash: hashOf(f) }));
  const questions = hashed
    .filter(({ text, hash }) => keep(`asks ${hash}`, () => /^- question: /m.test(text)))
    .flatMap((gate) => keep(`gate ${gate.hash}`, () => questionsIn(gate.text)).map((q) => ({ ...q, gate: gate.file })))
    .filter(({ words }) => words.length)
    .map((q) => ({ ...q, size: Math.min(RUN, q.words.length) }));
  const sizes = [...new Set(questions.map((q) => q.size))];
  const questionsKey = digest(questions.map((q) => q.words.join(" ")).join("\n"));
  const windows = keep(`windows ${questionsKey}`, () => {
    const made = new Map();
    questions.forEach(({ words, size }, n) => {
      for (let i = 0; i + size <= words.length; i++) {
        const run = runAt(words, i, size);
        if (!made.has(run)) made.set(run, []);
        made.get(run).push([n, i]);
      }
    });
    return made;
  });
  const firstsByFile = hashed.map(({ text, hash }) =>
    keep(`file ${questionsKey} ${hash}`, () => firstWindows(normalised(text).split(" "), windows, sizes)),
  );
  const found = [];
  questions.forEach(({ id, gate, words, size }, question) => {
    hashed.forEach(({ file }, f) => {
      const i = firstsByFile[f].get(question);
      if (i !== undefined && file !== gate) found.push({ file, id, gate, words: runAt(words, i, size) });
    });
  });
  return found;
}

const VAULT_STORE = "plugin/skills/design-critique/rules/";
const tree = scannedFiles(ROOT);
const textOf = (files, file) => files.find((f) => f.file === file).text;
const fileAndId = (found) => found.map((c) => [c.file, c.id]);
const vaultQuestions = tree.filter((f) => f.file.startsWith(VAULT_STORE)).flatMap((f) => parseGate(f.text).questions);

test("no gate question's wording appears outside its gate file in the plugin or the library data (#103)", () => {
  assert.ok(tree.length > 20, `only ${tree.length} files scanned`);
  assert.equal(vaultQuestions.length, RECORD_COUNT);
  const found = copies(tree);
  assert.deepEqual(
    found.map((c) => `${c.file} repeats ${c.id} (${c.gate}): "${c.words}" — cite the id instead`),
    [],
  );
});

test("the proof question has one home, and its three old homes cite its id (#165)", () => {
  assert.ok(vaultQuestions.some((q) => q.id === "vault.proof"));
  for (const file of ["plugin/skills/design-critique/SKILL.md", "plugin/skills/design-round/SKILL.md", "data/gallery.json"]) {
    assert.match(textOf(tree, file), /vault\.proof/, file);
  }
});

const plant = (file, insert) => tree.map((f) => (f.file === file ? { file, text: insert(f.text) } : f));

for (const q of vaultQuestions) {
  test(`a copy of ${q.id}'s wording is refused, in a skill and in the library data`, () => {
    const wording = q.fields.question.value;
    const inSkill = copies(plant("plugin/skills/design-round/SKILL.md", (t) => `${t}\n\nAlways ask: *${wording}*\n`));
    assert.deepEqual(fileAndId(inSkill), [["plugin/skills/design-round/SKILL.md", q.id]]);
    const gallery = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "gallery.json"), "utf8"));
    gallery.dna.never.push(`"${wording.replace(/ /g, "\n")}"`);
    const inData = copies(plant("data/gallery.json", () => readable("data/gallery.json", JSON.stringify(gallery, null, 2))));
    assert.deepEqual(fileAndId(inData), [["data/gallery.json", q.id]]);
  });

  test(`a part copy of ${q.id}'s wording is refused, in a script's comment and in the styles data`, () => {
    const all = normalised(q.fields.question.value).split(" ");
    const middle = all.slice(Math.floor((all.length - RUN) / 2)).slice(0, RUN).join(" ");
    const inScript = copies(plant("plugin/skills/design-round/scripts/check-layout.py", (t) => `${t}\n# Fails when ${middle}.\n`));
    assert.deepEqual(fileAndId(inScript), [["plugin/skills/design-round/scripts/check-layout.py", q.id]]);
    const styles = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "styles.json"), "utf8"));
    styles.vaultQuestionCopy = `Ask: ${middle}`;
    const inData = copies(plant("data/styles.json", () => readable("data/styles.json", JSON.stringify(styles))));
    assert.deepEqual(fileAndId(inData), [["data/styles.json", q.id]]);
  });
}

test("a copy reworded at both ends, wrapped across lines, still holds a run of the question's words and is refused", () => {
  const plain = "Is every piece of proof the asset shows the project's own, from a source it can name, with none invented?";
  assert.equal(vaultQuestions.find((q) => q.id === "vault.proof").fields.question.value, plain);
  const reworded = "Check that each\npiece of proof the asset shows the **project's**\nown — a source it can name — and flag fakes.";
  const found = copies(plant("plugin/skills/design-critique/SKILL.md", (t) => `${t}\n${reworded}\n`));
  assert.deepEqual(found.map((c) => c.id), ["vault.proof"]);
});

const CALM_GATE = {
  file: "plugin/skills/design-project/references/demo-gate.md",
  text: "### demo.calm\n- question: Does the page keep a single quiet accent colour against its white ground?\n",
};

test("a project gate file found in the plugin is a home too: its wording copied elsewhere is refused, its id cited is not", () => {
  assert.deepEqual(copies([...tree, CALM_GATE]), []);
  const cited = plant("plugin/skills/design-round/SKILL.md", (t) => `${t}\nAnswer \`demo.calm\`.\n`);
  assert.deepEqual(copies([...cited, CALM_GATE]), []);
  const copied = plant("plugin/skills/design-round/SKILL.md", (t) => `${t}\nKeep a single quiet accent colour against its white ground.\n`);
  assert.deepEqual(fileAndId(copies([...copied, CALM_GATE])), [["plugin/skills/design-round/SKILL.md", "demo.calm"]]);
});

test("a copy is reported by the first run of the question's words the file holds", () => {
  const copied = plant("plugin/skills/design-round/SKILL.md", (t) => `${t}\nThe page keeps a single quiet accent colour against its white ground.\n`);
  assert.deepEqual(copies([...copied, CALM_GATE]).map((c) => c.words), ["a single quiet accent colour against its white"]);
});

test("a gate added after a search is looked for in the files that search already read", () => {
  const copied = plant("plugin/skills/design-round/SKILL.md", (t) => `${t}\nEach page should keep a single quiet accent colour against its white ground.\n`);
  assert.deepEqual(copies(copied), []);
  assert.deepEqual(fileAndId(copies([...copied, CALM_GATE])), [["plugin/skills/design-round/SKILL.md", "demo.calm"]]);
});

test("a question shorter than the run is refused when copied whole", () => {
  const projectGate = { file: "plugin/demo-gate.md", text: "### demo.upright\n- question: Is the logo upright?\n" };
  const copied = plant("plugin/skills/design-round/SKILL.md", (t) => `${t}\nCheck: is the logo upright?\n`);
  assert.deepEqual(copies([...copied, projectGate]).map((c) => c.id), ["demo.upright"]);
});

test("a template's `<…>` slot is not its question's wording, so the step that fills it may say the same", () => {
  const template = {
    file: "plugin/demo-template.md",
    text: "### <key>.fit\n- question: Does the feel fit <who the site serves, how senior they are and the register they expect>?\n",
  };
  const filler = plant("plugin/skills/design-round/SKILL.md", (t) => `${t}\n- who the site serves, how senior they are and the register they expect;\n`);
  assert.deepEqual(copies([...filler, template]), []);
});
