"use strict";
const assert = require("node:assert/strict");
const { test } = require("node:test");
const { compile, searchable, matches, entryTexts } = require("../search.js");

const WORDS = [{ word: "hero", means: ["opening screen", "Top Section"] }];
const finds = (query, text, words = WORDS) => matches(compile(query, words), searchable([text]));

test("every typed word must appear, in any order (#42)", () => {
  assert.ok(finds("screen opening", "a bold opening screen"));
  assert.ok(!finds("opening footer", "a bold opening screen"));
});

test("a typed word matches only the start of a word", () => {
  assert.ok(finds("sea", "a calm seascape"));
  assert.ok(finds("sea", "night-sea mural"));
  assert.ok(!finds("sea", "desk research"));
});

test("a design word also finds the words the data uses for it, whatever their case", () => {
  assert.ok(finds("hero", "a bold opening screen"));
  assert.ok(finds("hero", "the top section of the page"));
  assert.ok(finds("HERO", "the hero"));
  assert.ok(!finds("hero", "a bold opening screen", []));
  assert.ok(!finds("her", "a bold opening screen"));
});

test("an empty query matches everything, and a typed symbol is matched as itself", () => {
  assert.ok(finds("  ", "anything"));
  assert.ok(finds("b&w", "a b&w print"));
  assert.ok(!finds("(", "no bracket here"));
});

const GALLERY = {
  collections: [{ id: "look", name: "Look Name", description: "look-description" }],
  page_parts: [{ id: "hero", name: "Part-Name" }],
  motion_kinds: [{ id: "scroll", name: "Kind-Name" }],
  projects: {
    manta: { groups: [{ id: "g", name: "Group-Name — what the group is for" }] },
    acme: { groups: [{ id: "acme-group", name: "Acme-Group" }] },
  },
};
const ENTRY = {
  title: "title-text", description: "description-text", note: "note-text", founder_note: "founder-text",
  keywords: ["keyword-text"], vocabulary: ["vocabulary-text"], collection: "look", page_parts: ["hero"],
  composition: "composition-text", image_recipe: "recipe-text", mood: "mood-text",
  motion: {
    kinds: ["scroll"], trigger: "trigger-text", purpose: "delight", purpose_note: "purpose-note-text",
    range: "range-text", from_to: "from-to-text", duration: "duration-text", easing: "easing-text",
    evidence: "evidence-text", capture: "capture-text",
  },
  fit: { manta: { groups: ["g"], take: "take-text" }, acme: { groups: ["acme-group"], take: "acme-take" } },
};

test("search reads the founder's words, the plain parts of motion, the look, the parts and the project's groups", () => {
  const text = entryTexts(ENTRY, GALLERY, "manta").join(" ");
  for (const word of ["title-text", "description-text", "note-text", "founder-text", "keyword-text", "vocabulary-text",
    "Look Name", "look-description", "Part-Name", "Kind-Name", "trigger-text", "delight", "purpose-note-text", "Group-Name"])
    assert.ok(text.includes(word), `search should read ${word}`);
  assert.ok(!text.includes("what the group is for"), "a group is searched by its short name");
});

test("search never reads the take, the AI fields or motion's measurements, nor another project's groups (#27)", () => {
  const text = entryTexts(ENTRY, GALLERY, "manta").join(" ");
  for (const word of ["take-text", "acme-take", "Acme-Group", "acme-group", "composition-text", "recipe-text", "mood-text", "range-text",
    "from-to-text", "duration-text", "easing-text", "evidence-text", "capture-text"])
    assert.ok(!text.includes(word), `search should not read ${word}`);
});
