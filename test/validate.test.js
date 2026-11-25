"use strict";
// validate.js, which refuses a malformed library before it commits (#1, --staged's group check #4): run on fixtures that
// each break green.json once, and a fixture on disk with no refusal asserted fails the run; --staged runs in a throwaway repo.
// Loosen one and a broken gallery.json, or a reference still carrying an unreviewed Manta group, reaches the library.
require("./no-git-env");
const assert = require("node:assert/strict");
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const ROOT = path.join(__dirname, "..");
const VALIDATE = path.join(ROOT, "validate.js");
const FIXTURES = path.join(__dirname, "fixtures", "validate");
const STYLES = path.join(FIXTURES, "style-guide", "styles.json");

function run(args, cwd = ROOT) {
  const result = runInProcess(VALIDATE, args, { cwd });
  const faults = result.stderr.split("\n").filter((line) => line.startsWith("  ")).map((line) => line.trim());
  return { status: result.status, faults, stdout: result.stdout, stderr: result.stderr };
}
const scratch = [];
const tempDir = (prefix) => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), prefix));
  scratch.push(dir);
  return dir;
};
after(() => {
  for (const dir of scratch) fs.rmSync(dir, { recursive: true, force: true });
});
const runFixture = (name) =>
  run(["--gallery", path.join(FIXTURES, `${name}.json`), "--images", path.join(FIXTURES, "images"), "--styles", STYLES]);

test("the green fixture passes", () => {
  const result = runFixture("green");
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /valid schema v3 library — 3 entries/);
});

// Each fixture is green.json with one malformation, so it must draw exactly
// that one refusal.
const refusals = {
  "schema-version": /^schema-version: schema_version is 2 — expected 3$/,
  "dna-constants-missing": /^dna-shape: dna\.constants is missing/,
  "dna-never-missing": /^dna-shape: dna\.never is missing/,
  "duplicate-id": /^duplicate-id: entries\[2\] \(porcelain\): id "porcelain"/,
  "unknown-collection": /^unknown-collection: .*"flat-posters" is not in collections\[\]/,
  "unknown-keyword": /^unknown-keyword: .*"ink-lines" is not in keywords_allowed/,
  "page-part-missing": /^page-part-missing: entries\[2\] \(unjudged\): page_parts is empty/,
  "unknown-page-part": /^unknown-page-part: entries\[0\] \(porcelain\): page part "hero-art" is not in page_parts$/,
  "art-only": /^art-only: entries\[0\] \(porcelain\): page_parts has art-only beside hero/,
  "page-part-list": /^page-part-list: page_parts lists "Hero" \(hero\) twice/,
  "page-part-name-twice": /^page-part-list: page_parts lists "Hero" \(opening-screen\) twice/,
  "page-part-gloss-missing": /^page-part-list: page_parts\[1\] lacks an id, a name or a gloss/,
  "keyword-family": /^keyword-family: "minimal" is in more than one keyword family: Colour, Scene$/,
  "unknown-project": /^unknown-project: .*fit\.acme names no project/,
  "fit-verdict": /^fit-verdict: .*"on brand" is not in projects\.manta\.verdicts/,
  "fit-group": /^fit-group: .*"mascot-rendering", which is not in projects\.manta\.groups/,
  "fit-groups-missing": /^group-list: entries\[0\] \(porcelain\): fit\.manta\.groups is missing or not a list/,
  "sheet-section": /^sheet-section: .*"8" is not a "§<n>" citation/,
  origin: /^origin: .*"chase" is not one of manta-original, ai-generated, third-party, unattributed$/,
  "source-missing": /^provenance: .*source is missing/,
  "licence-missing": /^provenance: .*licence is missing/,
  "both-limbs": /^limb: .*carries both of the image limb/,
  "neither-limb": /^limb: .*carries neither of the image limb/,
  "motion-purpose": /^motion-purpose: .*"wow" is not one of/,
  "motion-kind-missing": /^motion-kind-missing: entries\[1\] \(site-layers\): motion\.kinds is missing or not a list$/,
  "unknown-motion-kind": /^unknown-motion-kind: entries\[1\] \(site-layers\): motion kind "hover" is not in motion_kinds$/,
  "motion-kind-list": /^motion-kind-list: motion_kinds lists "Scroll" \(scrolling\) twice$/,
  "motion-kind-list-missing": /^motion-kind-list: motion_kinds is missing or not a list$/,
  "design-word-list-missing": /^design-word-list: design_words is missing or not a list$/,
  "design-word-twice": /^design-word-list: design_words lists "hero" twice$/,
  "design-word-means-empty": /^design-word-list: design_words\[1\] lacks a word or the words it means$/,
  "design-word-means-not-text": /^design-word-list: design_words\[1\] lacks a word or the words it means$/,
  "design-word-capital": /^design-word-list: design_words\[0\] \("Hero"\): the word is not one lower-case word/,
  "design-word-two-words": /^design-word-list: design_words\[0\] \("top section"\): the word is not one lower-case word/,
  "missing-image": /^missing-image: .*"gone\.png" is not on disk under images\/$/,
  "still-undefined": /^missing-still: entries\[1\] \(site-layers\): still undefined is not on disk under images\/$/,
  "still-not-bare": /^missing-still: .*"\.\.\/images\/site-layers\.png" is not on disk under images\/$/,
  "missing-still": /^missing-still: .*"gone\.png" is not on disk under images\/$/,
  "capture-undefined": /^missing-capture: entries\[1\] \(site-layers\): motion\.capture undefined is not on disk under images\/$/,
  "capture-not-bare": /^missing-capture: .*"\.\.\/images\/site-layers\.webm" is not on disk under images\/$/,
  "missing-capture": /^missing-capture: .*"gone\.webm" is not on disk under images\/$/,
  "capture-image-motion": /^missing-capture: entries\[0\] \(porcelain\): motion\.capture undefined/,
  "project-groups-missing": /^group-list: projects\.acme\.groups is missing or not a list/,
  "id-missing": /^id: entries\[2\]: id is missing or empty$/,
  "fit-not-object": /^shape: .*fit\.manta is not an object$/,
  "fit-inherited-key": /^unknown-project: .*fit\.constructor names no project/,
  "project-unknown": /^unknown-project: entries\[0\] \(porcelain\): project "acme" names no project in projects$/,
  "private-fit": /^private-fit: entries\[0\] \(porcelain\): belongs only to project acme, so it carries no fit\.manta$/,
  "site-url-scheme": /^web-address: entries\[0\] \(porcelain\): site_url "javascript:alert\(1\)" is not an http\(s\) web address$/,
  "site-url-relative": /^web-address: entries\[0\] \(porcelain\): site_url "example\.com" is not an http\(s\) web address$/,
  "site-url-no-slashes": /^web-address: entries\[0\] \(porcelain\): site_url "http:example\.com" is not an http\(s\) web address$/,
  "url-scheme": /^web-address: entries\[1\] \(site-layers\): url "javascript:alert\(1\)" is not an http\(s\) web address$/,
  "site-url-on-site": /^web-address: entries\[1\] \(site-layers\): carries site_url — a site entry's url is already its address$/,
  "unknown-style": /^unknown-style: collections\[0\] \(flat-poster\): style "cinematic-drak" is not in the Style guide$/,
  "style-twice": /^style-link: collections\[0\] \(flat-poster\): styles lists "cinematic-dark" twice$/,
  "style-not-list": /^style-link: collections\[0\] \(flat-poster\): styles is not a list$/,
  "collection-not-object": /^shape: collections\[1\] is not an object$/,
  "entries-missing": /^shape: entries is missing or not a list$/,
};

for (const [name, message] of Object.entries(refusals))
  test(`refuses ${name}`, () => {
    const result = runFixture(name);
    assert.equal(result.status, 1, result.stdout);
    assert.equal(result.faults.length, 1, `expected one fault, got:\n${result.faults.join("\n")}`);
    assert.match(result.faults[0], message);
  });

/** Runs the validator on green.json after `mutate` has changed a copy of it. */
const runMutated = (mutate) => {
  const gallery = JSON.parse(fs.readFileSync(path.join(FIXTURES, "green.json"), "utf8"));
  mutate(gallery);
  const file = path.join(tempDir("validate-mutated-"), "gallery.json");
  fs.writeFileSync(file, JSON.stringify(gallery));
  return run(["--gallery", file, "--images", path.join(FIXTURES, "images"), "--styles", STYLES]);
};

test("a reference kept for one project passes with that project's own verdict", () => {
  const result = runMutated((gallery) => {
    gallery.projects.acme = { name: "Acme", rules: "docs/brand/brand-sheet.md in acme/acme", verdicts: ["on-brand"], groups: [{ id: "hero", name: "Hero" }] };
    gallery.entries[0].project = "acme";
    gallery.entries[0].fit = { acme: { verdict: "on-brand", groups: ["hero"], take: "Keep the quiet header." } };
  });
  assert.equal(result.status, 0, result.stderr);
});

test("a judged reference with no group, and a project with none, pass", () => {
  const result = runMutated((gallery) => {
    gallery.entries[0].fit.manta.groups = [];
    gallery.projects.acme = { name: "Acme", rules: "docs/brand/brand-sheet.md in acme/acme", verdicts: ["on-brand"], groups: [] };
    gallery.entries[2].fit = { acme: { verdict: "on-brand", groups: [], take: "Keep the quiet header." } };
  });
  assert.equal(result.status, 0, result.stderr);
});

test("a style listed twice is refused as twice even when it is also unknown", () => {
  const result = runMutated((gallery) => {
    gallery.collections[0].styles = ["nope", "nope"];
  });
  assert.deepEqual(result.faults.map((f) => f.split(":")[0]), ["unknown-style", "style-link"]);
});

test("a screenshot's site_url passes when it is an http or https address", () => {
  const result = runMutated((gallery) => {
    gallery.entries[0].site_url = "https://example.com/work?id=1";
    gallery.entries[2].site_url = "http://example.org";
  });
  assert.equal(result.status, 0, result.stderr);
});

test("a project's gate file written as <path> in <owner>/<repo> passes", () => {
  const result = runMutated((gallery) => {
    gallery.projects.manta.gate = "docs/brand/fit-gate.md in lucmoseley/mantahostels";
  });
  assert.equal(result.status, 0, result.stderr);
});

const badRepoMarkdown = [
  null,
  42,
  "",
  "docs/brand/fit-gate.md",
  "docs/brand/fit-gate.md in mantahostels",
  "docs/brand/fit-gate.md in lucmoseley/mantahostels/extra",
  "docs/brand/fit-gate.txt in lucmoseley/mantahostels",
  "/docs/brand/fit-gate.md in lucmoseley/mantahostels",
  "docs/../../fit-gate.md in lucmoseley/mantahostels",
  "docs\\..\\..\\fit-gate.md in lucmoseley/mantahostels",
  "C:/fit-gate.md in lucmoseley/mantahostels",
  "docs/brand/fit-gate.md in ../..",
];
// rules is required (design-project §4), so leaving it out is refused too; gate is optional.
for (const [field, values] of [["gate", badRepoMarkdown], ["rules", [undefined, ...badRepoMarkdown]]])
  for (const value of values)
    test(`a project ${field} of ${JSON.stringify(value)} is refused as one project-${field} fault naming projects.manta.${field}`, () => {
      const result = runMutated((gallery) => {
        gallery.projects.manta[field] = value;
      });
      assert.equal(result.status, 1, result.stdout);
      assert.equal(result.faults.length, 1, `expected one fault, got:\n${result.faults.join("\n")}`);
      assert.match(result.faults[0], new RegExp(`^project-${field}: projects\\.manta\\.${field} `));
    });

for (const desktop of [null, 1536, "", "1536", "1536x", "1536 x 864", "1536X864", "0x864", "-1536x864", "1536.5x864", "1536x864px"])
  test(`a project desktop of ${JSON.stringify(desktop)} is refused as one project-desktop fault naming projects.manta.desktop`, () => {
    const result = runMutated((gallery) => {
      gallery.projects.manta.desktop = desktop;
    });
    assert.equal(result.status, 1, result.stdout);
    assert.equal(result.faults.length, 1, `expected one fault, got:\n${result.faults.join("\n")}`);
    assert.match(result.faults[0], /^project-desktop: projects\.manta\.desktop /);
  });

test("a project desktop given as a width and height is accepted (#196)", () => {
  const result = runMutated((gallery) => {
    gallery.projects.manta.desktop = "1536x864";
  });
  assert.equal(result.status, 0, result.stdout);
});

test("every failing fixture on disk has a refusal asserted above", () => {
  const onDisk = fs.readdirSync(FIXTURES).filter((f) => f.endsWith(".json") && f !== "green.json");
  assert.deepEqual(onDisk.map((f) => f.slice(0, -5)).sort(), Object.keys(refusals).sort());
});

test("a file that is not JSON is refused, not thrown", () => {
  const dir = tempDir("validate-");
  fs.writeFileSync(path.join(dir, "gallery.json"), "{ not json");
  const result = run(["--gallery", path.join(dir, "gallery.json"), "--images", FIXTURES]);
  assert.equal(result.status, 1);
  assert.match(result.stderr, /json: /);
});

test("an unknown argument is a usage error", () => {
  assert.equal(run(["--gallry", "x"]).status, 2);
});

test("--staged with --styles is a usage error", () => {
  assert.equal(run(["--staged", "--styles", STYLES]).status, 2);
});

test("a gallery that cannot be read exits 2, not the faults code", () => {
  const result = run(["--gallery", path.join(FIXTURES, "absent.json")]);
  assert.equal(result.status, 2);
  assert.match(result.stderr, /could not read the gallery/);
});

test("a Style guide that cannot be read exits 2, not the faults code", () => {
  const result = run(["--gallery", path.join(FIXTURES, "green.json"), "--images", path.join(FIXTURES, "images"), "--styles", path.join(FIXTURES, "absent.json")]);
  assert.equal(result.status, 2);
  assert.match(result.stderr, /could not read the Style guide/);
});

test("a Style guide that is not JSON, or holds no styles list, is refused", () => {
  const dir = tempDir("validate-styles-");
  for (const [text, message] of [["{ not json", /^style-guide: /], ['{"description":"d"}', /^style-guide: it has no styles list$/]]) {
    fs.writeFileSync(path.join(dir, "styles.json"), text);
    const result = run(["--gallery", path.join(FIXTURES, "green.json"), "--images", path.join(FIXTURES, "images"), "--styles", path.join(dir, "styles.json")]);
    assert.equal(result.status, 1, result.stderr);
    assert.match(result.faults[0], message);
  }
});

// The ingest's draft passes the working-tree check, so the founder can validate
// mid-review, but a commit carrying its group proposal is refused.
test("--staged alone refuses an entry still carrying proposed_manta_groups", () => {
  const repo = tempDir("validate-proposal-");
  const git = (...args) => execFileSync("git", ["-c", "core.hooksPath=/dev/null", ...args], { cwd: repo, stdio: "pipe" });
  fs.copyFileSync(VALIDATE, path.join(repo, "validate.js"));
  fs.copyFileSync(path.join(ROOT, "git-read.js"), path.join(repo, "git-read.js"));
  fs.mkdirSync(path.join(repo, "data"));
  fs.copyFileSync(STYLES, path.join(repo, "data", "styles.json"));
  fs.cpSync(path.join(FIXTURES, "images"), path.join(repo, "images"), { recursive: true });
  const gallery = JSON.parse(fs.readFileSync(path.join(FIXTURES, "green.json"), "utf8"));
  gallery.entries[0].proposed_manta_groups = ["mascot-renderings"];
  fs.writeFileSync(path.join(repo, "data", "gallery.json"), JSON.stringify(gallery));
  git("init", "-q");
  git("add", "data", "images/");

  const draft = runInProcess(path.join(repo, "validate.js"), [], { cwd: repo });
  assert.equal(draft.status, 0, draft.stderr);
  const staged = runInProcess(path.join(repo, "validate.js"), ["--staged"], { cwd: repo });
  assert.equal(staged.status, 1);
  assert.match(staged.stderr, /draft-proposal: entries\[0\] .*carries proposed_manta_groups — delete it, or promote it into fit\.manta/);
});

// --staged is the hook's mode: it must judge the index, not the working tree,
// which can hold a parallel session's half-written copy.
test("--staged reads the gallery and images from the index, not the working tree", () => {
  const repo = tempDir("validate-staged-");
  const git = (...args) => execFileSync("git", ["-c", "core.hooksPath=/dev/null", ...args], { cwd: repo, stdio: "pipe" });
  fs.copyFileSync(VALIDATE, path.join(repo, "validate.js"));
  fs.copyFileSync(path.join(ROOT, "git-read.js"), path.join(repo, "git-read.js"));
  fs.mkdirSync(path.join(repo, "data"));
  fs.copyFileSync(STYLES, path.join(repo, "data", "styles.json"));
  fs.cpSync(path.join(FIXTURES, "images"), path.join(repo, "images"), { recursive: true });
  const green = fs.readFileSync(path.join(FIXTURES, "green.json"), "utf8");
  const galleryPath = path.join(repo, "data", "gallery.json");
  fs.writeFileSync(galleryPath, green);
  git("init", "-q");
  git("add", "data", "images/");
  const staged = () => runInProcess(path.join(repo, "validate.js"), ["--staged"], { cwd: repo });

  // A broken working-tree copy and a deleted working-tree image do not reach the staged check.
  fs.writeFileSync(galleryPath, "{ half-written");
  fs.rmSync(path.join(repo, "images", "porcelain.png"));
  assert.equal(staged().status, 0, staged().stderr);

  // A staged Style guide without a linked style is refused even with a good working-tree copy.
  const stylesPath = path.join(repo, "data", "styles.json");
  fs.writeFileSync(stylesPath, JSON.stringify({ styles: [{ id: "cinematic-dark", name: "Cinematic Dark" }] }));
  git("add", "data/styles.json");
  fs.copyFileSync(STYLES, stylesPath);
  assert.match(staged().stderr, /unknown-style: .*"quiet-luxury"/);
  git("add", "data/styles.json");

  // A bad staged gallery is refused even with a good working-tree copy.
  fs.writeFileSync(galleryPath, fs.readFileSync(path.join(FIXTURES, "schema-version.json"), "utf8"));
  git("add", "data/gallery.json");
  fs.writeFileSync(galleryPath, green);
  assert.match(staged().stderr, /schema-version: schema_version is 2/);

  // An image removed from the index is missing, even while it sits on disk.
  git("add", "data/gallery.json");
  fs.copyFileSync(path.join(FIXTURES, "images", "porcelain.png"), path.join(repo, "images", "porcelain.png"));
  git("rm", "-q", "--cached", "images/porcelain.png");
  const result = staged();
  assert.equal(result.status, 1);
  assert.match(result.stderr, /missing-image: .*"porcelain\.png"/);

  // A site still removed from the index is missing too, even while it sits on disk.
  git("add", "images/porcelain.png");
  git("rm", "-q", "--cached", "images/site-layers.png");
  const still = staged();
  assert.equal(still.status, 1);
  assert.match(still.stderr, /missing-still: .*"site-layers\.png"/);
  assert.doesNotMatch(still.stderr, /missing-image/);

  // So is a site recording removed from the index.
  git("add", "images/site-layers.png");
  git("rm", "-q", "--cached", "images/site-layers.webm");
  const capture = staged();
  assert.equal(capture.status, 1);
  assert.match(capture.stderr, /missing-capture: .*"site-layers\.webm"/);
  assert.doesNotMatch(capture.stderr, /missing-still/);
});
