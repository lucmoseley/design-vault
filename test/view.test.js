"use strict";
// test/view.test.js — what the library page shows and copies (view.js, #84): filters and counts, sort, view hash
// and the copied briefs, run in-process on a small made-up library so each case names the references it expects.
// Loosen one and a page that hides references, miscounts, loses a shared link or drops a brief line passes.
const assert = require("node:assert/strict");
const { test } = require("node:test");
const { compile } = require("../search.js");
const V = require("../view.js");

const DATA = {
  collections: [
    { id: "flat", name: "Flat Poster", description: "flat-description", vocabulary: ["flat-word"], risk: "flat-risk", styles: ["swiss"] },
    { id: "quiet", name: "Quiet Editorial", description: "quiet-description", vocabulary: ["quiet-word"], risk: "quiet-risk" },
  ],
  page_parts: [{ id: "hero", name: "Opening screen" }, { id: "footer", name: "Footer" }, { id: "pricing", name: "Pricing" }],
  motion_kinds: [{ id: "scroll", name: "Scroll" }, { id: "hover", name: "Pointer" }],
  design_words: [],
  dna: { constants: ["constant-line"], never: ["never-line"] },
  projects: {
    manta: { name: "Manta", groups: [{ id: "hero-art", name: "Hero art — pictures for the hero" }, { id: "icons", name: "Icons" }] },
    acme: { name: "Acme", groups: [] },
  },
  entries: [
    { id: "a", title: "Bravo", added: "2026-01-02", collection: "flat", page_parts: ["hero"], file: "a.png",
      keywords: ["wave", "ink"], description: "a-description", note: "a-note", composition: "a-composition", image_recipe: "a-recipe",
      fit: { manta: { verdict: "fits", take: "a-take", groups: ["hero-art", "icons"], sheet_section: "§8" } } },
    { id: "b", title: "Alpha", added: "2026-03-01", collection: "quiet", page_parts: ["footer"], still: "b.webp", url: "https://b.example",
      motion: { kinds: ["scroll"], trigger: "scroll", from_to: "1 → 1.5", purpose: "delight" },
      fit: { manta: { verdict: "clashes", take: "b-take", groups: [] } } },
    { id: "c", title: "Charlie", added: "2026-02-01", collection: "flat", page_parts: ["hero", "footer"], file: "c.png", motion: { kinds: ["hover"] } },
    { id: "d", title: "Delta", added: "2026-04-01", collection: "quiet", page_parts: ["pricing"], file: "d.png", project: "acme" },
  ],
};
const STYLES = { styles: [
  { id: "swiss", name: "Swiss Grid", vocabulary: ["grid"], recognize: ["columns"], canonical: [{ name: "swiss.example", url: "https://swiss.example" }], risk: "swiss-risk" },
  { id: "brutal", name: "Brutalist", vocabulary: ["raw"], recognize: ["bare html"], canonical: [], risk: "brutal-risk", imageStyle: "brutal-image" },
] };
const NO_PICKS = { look: null, part: null, motion: null, group: null };
const view = (over = {}) => ({
  data: DATA, styles: STYLES, project: "manta", fit: "any", sort: "newest", showStyles: false, queryTests: [],
  prefs: { includeDna: false, overrides: "" }, ...over, pick: { ...NO_PICKS, ...over.pick },
});
const ids = list => list.map(e => e.id);

test("a reference kept for another project is left out of the library", () => {
  assert.deepEqual(ids(V.visibleEntries(view())), ["b", "c", "a"]);
  assert.deepEqual(ids(V.visibleEntries(view({ project: "acme" }))), ["d", "b", "c", "a"]);
});

test("each pick narrows the view, and picks in different ways combine", () => {
  assert.deepEqual(ids(V.visibleEntries(view({ pick: { look: "flat" } }))), ["c", "a"]);
  assert.deepEqual(ids(V.visibleEntries(view({ pick: { part: "footer" } }))), ["b", "c"]);
  assert.deepEqual(ids(V.visibleEntries(view({ pick: { motion: "scroll" } }))), ["b"]);
  assert.deepEqual(ids(V.visibleEntries(view({ pick: { group: "icons" } }))), ["a"]);
  assert.deepEqual(ids(V.visibleEntries(view({ pick: { look: "flat", part: "footer" } }))), ["c"]);
});

test("the fit filter keeps one verdict, and unjudged keeps the references with none", () => {
  assert.deepEqual(ids(V.visibleEntries(view({ fit: "clashes" }))), ["b"]);
  assert.deepEqual(ids(V.visibleEntries(view({ fit: "unjudged" }))), ["c"]);
});

test("the search box narrows the view", () => {
  assert.deepEqual(ids(V.visibleEntries(view({ queryTests: compile("wave", []) }))), ["a"]);
  assert.deepEqual(ids(V.visibleEntries(view({ queryTests: compile("charlie", []) }))), ["c"]);
});

test("a count says what picking that value would leave, under every pick but its own way's", () => {
  const flat = view({ pick: { look: "flat" } });
  assert.equal(V.countFor(flat, "part", "hero"), 2);
  assert.equal(V.countFor(flat, "part", "footer"), 1);
  assert.equal(V.countFor(flat, "look", "quiet"), 1);
  assert.equal(V.countFor(view({ fit: "fits" }), "look", "flat"), 1);
  assert.equal(V.countFor(view({ queryTests: compile("alpha", []) }), "look", "quiet"), 1);
});

test("a way offers only the page parts and groups the project's library holds", () => {
  const picks = (hash, project = "acme") => V.readHash(view({ project }), hash).pick;
  assert.equal(picks("part=pricing&project=manta").part, null);
  assert.equal(picks("part=pricing&project=acme").part, "pricing");
  assert.equal(picks("motion=hover&project=acme").motion, "hover");
  assert.equal(picks("group=icons&project=manta").group, "icons");
  assert.equal(picks("group=icons&project=acme").group, null);
});

test("the sort is newest first, or by name", () => {
  assert.deepEqual(ids(V.visibleEntries(view())), ["b", "c", "a"]);
  assert.deepEqual(ids(V.visibleEntries(view({ sort: "name" }))), ["b", "a", "c"]);
  assert.deepEqual(V.visibleStyles(view({ sort: "name" })).map(s => s.id), ["brutal", "swiss"]);
  assert.deepEqual(V.visibleStyles(view({ queryTests: compile("grid", []) })).map(s => s.id), ["swiss"]);
});

test("the hash names each pick, and the project only when a pick depends on it", () => {
  assert.equal(V.viewHash(view()), "all");
  assert.equal(V.viewHash(view({ showStyles: true, pick: { look: "flat" } })), "styles");
  assert.equal(V.viewHash(view({ pick: { look: "flat" } })), "look=flat");
  assert.equal(V.viewHash(view({ pick: { look: "flat", group: "icons" } })), "look=flat&group=icons&project=manta");
});

test("a hash read back gives the view it was written from", () => {
  for (const over of [{}, { pick: { look: "flat" } }, { pick: { part: "pricing" }, project: "acme" }, { pick: { look: "quiet", motion: "scroll", group: "icons" } }]) {
    const written = view(over), read = V.readHash(view({ project: over.project === "acme" ? "manta" : "acme" }), V.viewHash(written));
    assert.deepEqual(read.pick, written.pick, JSON.stringify(over));
    if (over.pick?.part || over.pick?.motion || over.pick?.group) assert.equal(read.project, written.project);
  }
  assert.equal(V.readHash(view(), "styles").showStyles, true);
});

test("a hash keeps only the picks and project the library offers, and reads the old one-view hashes", () => {
  const read = V.readHash(view(), "look=gone&part=pricing&group=icons&project=nowhere");
  assert.equal(read.project, "manta");
  assert.deepEqual(read.pick, { look: null, part: null, motion: null, group: "icons" });
  assert.equal(V.readHash(view(), "flat").pick.look, "flat");
  assert.equal(V.readHash(view(), "group:hero-art").pick.group, "hero-art");
});

const lines = text => text.split("\n");
test("a reference's brief carries every line the setup spec names", () => {
  const brief = V.buildBrief(view(), [DATA.entries[0]]);
  for (const line of [
    "Vault: ~/design-vault",
    "Reference: a — Bravo",
    "Screenshot: images/a.png",
    "Collection: Flat Poster (Style guide: Swiss Grid)",
    "Page part: Opening screen",
    "Keywords: wave, ink",
    "Description: a-description",
    "Note (any project): a-note",
    "Manta fit: fits (brand sheet §8), groups Hero art, Icons — take: a-take",
    "Composition: a-composition",
    "Image recipe: a-recipe",
  ]) assert.ok(lines(brief).includes(line), `brief should carry: ${line}`);
});

test("an unjudged reference's brief says so, and a moving one's carries its motion and site", () => {
  const unjudged = V.buildBrief(view(), [DATA.entries[2]]);
  assert.ok(lines(unjudged).includes("Manta fit: unjudged — write the verdict and take before this brief runs"));
  assert.ok(lines(unjudged).includes("Screenshot: images/c.png"));
  const moving = V.buildBrief(view(), [DATA.entries[1]]);
  for (const line of ["Screenshot: images/b.webp", "Site: https://b.example", "Motion: Scroll — scroll — 1 → 1.5 — purpose delight", "Manta fit: clashes — take: b-take"])
    assert.ok(lines(moving).includes(line), `brief should carry: ${line}`);
  assert.ok(!moving.includes("Composition:"));
});

test("a brief of several references asks for one direction per reference, and carries the preferences only when asked", () => {
  const one = V.buildBrief(view(), [DATA.entries[0]]), two = V.buildBrief(view(), DATA.entries.slice(0, 2));
  assert.ok(!one.includes("one direction per reference"));
  assert.ok(two.includes("one direction per reference") && two.includes("Reference: a — Bravo") && two.includes("Reference: b — Alpha"));
  assert.ok(!one.includes("never-line"));
  const withPrefs = V.buildBrief(view({ prefs: { includeDna: true, overrides: " our-direction " } }), [DATA.entries[0]]);
  for (const text of ["- constant-line", "- never-line", "Project-specific directions (take priority):\nour-direction"])
    assert.ok(withPrefs.includes(text), `brief should carry: ${text}`);
});

test("the collection, style and image-prompt copies carry what they name", () => {
  const collection = V.collectionBrief(view(), DATA.collections[0]);
  assert.ok(collection.startsWith("Collection: Flat Poster (Style guide: Swiss Grid)\nflat-description\nVocabulary: flat-word\nDirection to explore: flat-risk"));
  assert.ok(collection.includes("Reference: a — Bravo") && collection.includes("Reference: c — Charlie") && !collection.includes("Reference: b"));
  const style = lines(V.styleBrief(view(), "brutal"));
  for (const line of ["Aesthetic: Brutalist", "Vocabulary: raw", "Direction to explore: brutal-risk", "Image direction: brutal-image"])
    assert.ok(style.includes(line), `style brief should carry: ${line}`);
  const prompt = V.imagePrompt(DATA.entries[0]);
  assert.ok(prompt.includes("a-recipe") && prompt.includes("Composition: a-composition") && prompt.includes("Use images/a.png as a style reference"));
});
