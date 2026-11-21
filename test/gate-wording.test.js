"use strict";
// One home per gate question (#103 Q6 (A), #165): a gate question's wording lives only in its gate file, and every
// other file in the plugin or the library data cites its id. Loosen it and the pre-commit gate, which runs every
// JavaScript suite, lets a copy land.
// A gate file is any file with a `- question:` line, so a project gate template is guarded once it takes the form.
// The refusals are tested by planting a copy into an in-memory version of the real tree, so the tree's own text is
// what each plant must be told apart from.
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");
const { parseGate } = require("../plugin/skills/design-round/scripts/gate-form.js");
const { RECORD_COUNT } = require("./rule-store.js");

const ROOT = path.join(__dirname, "..");
// What a round reads (#154). README.md and docs/ quote rules as history and research, which no round obeys.
const SCANNED = ["plugin", "data"];
// Leaves out .jsonl, the append-only logs: they hold the founder's words verbatim, which a question may be drafted
// from, and a logged row cannot be reworded.
const TEXT = /\.(md|js|json|py|sh|html|css|txt)$/;
// gallery.json and styles.json bundled, so a copy there is already a copy in them.
const BUNDLE = "data/vault-data.js";
// The shortest run of a question's words that counts as a copy; a question this short or shorter must appear whole.
// Short enough that a copy with its opening or closing clause reworded still holds one; one word longer than a
// measuring script's name for the fault it reports, check-layout.py's "text cut off at the screen's edge".
const RUN = 8;

/** The words of `text`, lower-cased, with markdown and punctuation dropped, joined by single spaces. */
const normalised = (text) =>
  text.normalize("NFKC").toLowerCase().replace(/['’]/g, "").split(/[^\p{L}\p{N}]+/u).filter(Boolean).join(" ");
// A `<…>` slot in a template's question is filled by the project, so it is not the question's wording.
const SLOT = /<[^<>]*>/g;

/** A JSON file's readable text is its string values; a copy there is JSON-escaped. */
function stringValues(value) {
  if (typeof value === "string") return [value];
  if (value && typeof value === "object") return Object.values(value).flatMap(stringValues);
  return [];
}

const readable = (file, raw) => (file.endsWith(".json") ? stringValues(JSON.parse(raw)).join("\n") : raw);

/** Every scanned file under the vault root `root`, each { file (repo-relative), text }. */
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

// copies() runs four times for every vault question, each on the tree with at most one file changed, so each file's
// hash is kept by the file's own object, which plant() passes on untouched, and its matches and the questions' windows
// by a hash of its text and of the questions: a call re-reads only the file a test planted into (#349, #462).
// Residual: nothing is ever dropped, which one test process holding a few hundred small entries can afford.
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

/** A gate file's questions, each { id, words }: its wording's words with the slots dropped. */
const questionsIn = (text) =>
  parseGate(text).questions.map((q) => ({
    id: q.id,
    words: normalised((q.fields.question?.value ?? "").replace(SLOT, " ")).split(" ").filter(Boolean),
  }));

/** The `size` words of `words` from `start`, joined as normalised() joins them. */
const runAt = (words, start, size) => words.slice(start, start + size).join(" ");

/** The first window of each question in `windows` (run → [[question, window]]) found in `words`: question → window. */
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

/**
 * Every copy of a gate question's wording outside its own gate file: { file, id, gate, words }, where `words` is the
 * question's first window found in the file. A question with no words outside its slots has no wording to copy.
 */
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

test("no gate question's wording appears outside its gate file in the plugin or the library data", () => {
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
    // A DNA line in gallery.json, wrapped at every word, so the copy reaches the scan only through the JSON escapes.
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
  // A line no earlier test plants, so no earlier search has read this file with the gate present.
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
