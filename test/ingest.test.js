"use strict";
const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const ROOT = path.join(__dirname, "..");
const VALIDATOR_FILES = require("./validator-files.js");
const PROGRAMS = ["ingest.js", "bundle.js", ...VALIDATOR_FILES];
const SHOTS = path.join(__dirname, "fixtures", "ingest");
const CLAUDE = path.join(__dirname, "claude-fake.js");
const FIXTURES = path.join(__dirname, "fixtures", "validate");
const GREEN = path.join(FIXTURES, "green.json");
const FIXTURE_IMAGES = path.join(FIXTURES, "images");
const CAP = 20 * 1024 * 1024;
const USAGE = "Usage: node ingest.js [--model <model>]";

const scratch = [];
after(() => {
  for (const dir of scratch) fs.rmSync(dir, { recursive: true, force: true });
});

function makeVault(edit) {
  const dir = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "ingest-")));
  scratch.push(dir);
  for (const name of PROGRAMS) fs.copyFileSync(path.join(ROOT, name), path.join(dir, name));
  fs.mkdirSync(path.join(dir, "data"));
  const galleryPath = path.join(dir, "data", "gallery.json");
  const imagesDir = path.join(dir, "images");
  fs.copyFileSync(GREEN, galleryPath);
  fs.copyFileSync(path.join(ROOT, "data", "styles.json"), path.join(dir, "data", "styles.json"));
  fs.cpSync(FIXTURE_IMAGES, imagesDir, { recursive: true });
  if (edit) {
    const gallery = JSON.parse(fs.readFileSync(galleryPath, "utf8"));
    edit(gallery);
    fs.writeFileSync(galleryPath, JSON.stringify(gallery));
  }
  const answersPath = path.join(dir, "answers.json");
  const callsPath = path.join(dir, "calls.jsonl");
  const env = { ...process.env, WFC_CLAUDE_BIN: CLAUDE, FAKE_CLAUDE_REPLIES: answersPath, FAKE_CLAUDE_LOG: callsPath, FAKE_CLAUDE_WATCH: galleryPath };
  const call = ({ args, prompt, named, watched }) => {
    const image = prompt.match(/^Read the image at this exact path: (.+)$/m)?.[1] ?? null;
    return { model: args[args.indexOf("--model") + 1], prompt, image, imageExisted: named[image] === true, onDisk: JSON.parse(watched).entries.map((entry) => entry.id) };
  };
  const calls = () => (fs.existsSync(callsPath) ? fs.readFileSync(callsPath, "utf8").split("\n").filter(Boolean).map((line) => call(JSON.parse(line))) : []);
  const answer = (answers) => {
    fs.writeFileSync(answersPath, JSON.stringify(answers.map((a) => (a.fail || a.kill ? a : { structured: a }))));
    fs.rmSync(callsPath, { force: true });
  };
  return {
    dir,
    galleryPath,
    imagesDir,
    env,
    answer,
    calls,
    read: () => JSON.parse(fs.readFileSync(galleryPath, "utf8")),
    images: () => fs.readdirSync(imagesDir).sort(),
    run: (args, answers = [extraction("Shot")]) => {
      answer(answers);
      const result = runInProcess(path.join(dir, "ingest.js"), args, { cwd: dir, env });
      return { ...result, calls: calls() };
    },
    validate: () => runInProcess(path.join(dir, "validate.js"), [], { cwd: dir }),
  };
}

const extraction = (title, overrides = {}) => ({
  title,
  collection: "flat-poster",
  new_collection: null,
  page_parts: ["hero"],
  description: "A flat poster. Two colours.",
  note: "Flat colour carries the whole page.",
  keywords: ["minimal"],
  vocabulary: ["flat colour field", "hard-edged shapes", "centred headline", "two-colour palette", "wide margins"],
  image_recipe: "flat poster of [SUBJECT: a palm]",
  composition: "full-bleed poster behind the headline",
  proposed_manta_groups: [],
  ...overrides,
});
const shot = (name) => path.join(SHOTS, name);
const expectedImages = (...added) => [...fs.readdirSync(FIXTURE_IMAGES), ...added].sort();
const out = (result) => `${result.stdout}\n${result.stderr}`;

test("a PNG, a JPEG and a WebP from outside the vault land under their sniffed extensions and pass the validator with fit absent (#4)", () => {
  const vault = makeVault();
  const run = vault.run([shot("shot.png"), shot("shot.jpg"), shot("shot.webp")], ["Shot png", "Shot jpg", "Shot webp"].map((t) => extraction(t)));
  assert.equal(run.status, 0, out(run));
  assert.match(run.stdout, /3 of 3 ingested/);
  assert.equal(run.calls.length, 3);
  for (const { image, imageExisted } of run.calls) {
    assert.ok(image.startsWith(vault.imagesDir + path.sep), `claude -p was told to read ${image}, not a copy inside images/`);
    assert.ok(imageExisted, `${image} did not exist when claude -p was called`);
  }
  const added = vault.read().entries.slice(3);
  assert.deepEqual(added.map((e) => e.file), ["shot-png.png", "shot-jpg.jpg", "shot-webp.webp"]);
  for (const entry of added) assert.equal("fit" in entry, false);
  assert.deepEqual(vault.images(), expectedImages("shot-png.png", "shot-jpg.jpg", "shot-webp.webp"));
  const result = vault.validate();
  assert.equal(result.status, 0, result.stderr);
});

test("a mislabelled file lands under the extension its bytes say, and a non-image is refused before any copy or call", () => {
  const vault = makeVault();
  const run = vault.run([shot("mislabelled.png"), shot("not-an-image.png")], [extraction("Mislabelled")]);
  assert.equal(run.status, 1, out(run));
  assert.equal(run.calls.length, 1);
  assert.equal(vault.read().entries.at(-1).file, "mislabelled.webp");
  assert.deepEqual(vault.images(), expectedImages("mislabelled.webp"));
  assert.match(run.stdout, /not-an-image\.png\n {2}✗ not a PNG, JPEG or WebP by its first bytes/);
});

test("an image over the 20 MB cap is refused before any copy or call; one at the cap is taken", () => {
  const vault = makeVault();
  const png = fs.readFileSync(shot("shot.png"));
  const make = (name, size) => {
    const file = path.join(vault.dir, name);
    fs.writeFileSync(file, png);
    fs.truncateSync(file, size);
    return file;
  };
  const run = vault.run([make("over.png", CAP + 1), make("at.png", CAP)], [extraction("At the cap")]);
  assert.equal(run.status, 1, out(run));
  assert.equal(run.calls.length, 1);
  assert.match(run.stdout, /over\.png\n {2}✗ 20\.0 MB is over the 20 MB cap/);
  assert.deepEqual(vault.images(), expectedImages("at-the-cap.png"));
});

test("gallery.json is rewritten after each image, so a failed extraction on image 2 keeps image 1 and the run goes on", () => {
  const vault = makeVault();
  const run = vault.run([shot("shot.png"), shot("shot.jpg"), shot("shot.webp")], [extraction("One"), { fail: "the extractor fell over" }, extraction("Three")]);
  assert.deepEqual(run.calls[1].onDisk.slice(3), ["one"], "image 1 was not on disk when image 2 began");
  assert.equal(run.status, 1, out(run));
  assert.match(run.stdout, /shot\.jpg\n {2}✗ claude -p failed \(exit 1\): the extractor fell over/);
  assert.match(run.stdout, /2 of 3 ingested/);
  assert.deepEqual(vault.read().entries.slice(3).map((e) => e.id), ["one", "three"]);
  assert.deepEqual(vault.images(), expectedImages("one.png", "three.webp"), "the failed image's holding copy was left behind");
  assert.deepEqual(fs.readdirSync(path.join(vault.dir, "data")).sort(), ["gallery.json", "styles.json", "vault-data.js"]);
});

test("a run killed during image 3 of 3 leaves images 1 and 2 in a gallery.json that still parses and validates, and the next run deletes the stray copy", () => {
  const vault = makeVault();
  vault.answer([extraction("Shot"), extraction("Shot"), { kill: true }]);
  const child = spawnSync(process.execPath, [path.join(vault.dir, "ingest.js"), shot("shot.png"), shot("shot.jpg"), shot("shot.webp")], {
    cwd: vault.dir,
    env: vault.env,
    encoding: "utf8",
  });
  assert.equal(child.signal, "SIGKILL", child.stderr);
  assert.equal(vault.calls().length, 3);
  assert.deepEqual(vault.read().entries.slice(3).map((e) => e.file), ["shot.png", "shot-2.jpg"]);
  const result = vault.validate();
  assert.equal(result.status, 0, result.stderr);

  const stray = vault.images().filter((name) => name.startsWith("ingest-"));
  assert.equal(stray.length, 1, `expected image 3's holding copy, found ${vault.images().join(", ")}`);
  const run = vault.run([shot("shot.webp")]);
  assert.equal(run.status, 0, out(run));
  assert.deepEqual(vault.images(), expectedImages("shot.png", "shot-2.jpg", "shot-3.webp"));
  assert.ok(run.stdout.includes(`deleted images/${stray[0]}, left by a killed run`), run.stdout);
});

test("a holding copy whose run is still alive is left alone", () => {
  const vault = makeVault();
  const live = path.join(vault.imagesDir, `ingest-${process.pid}-1.png`);
  fs.copyFileSync(shot("shot.png"), live);
  const run = vault.run([shot("shot.jpg")]);
  assert.equal(run.status, 0, out(run));
  assert.ok(fs.existsSync(live));
});

test("the fields the pixels cannot supply take their defaults, and --source sets the next image's source only", () => {
  const vault = makeVault();
  const run = vault.run([shot("shot.png"), "--source", "https://example.com", shot("shot.jpg"), shot("shot.webp"), "--source", "Dribbble, author unrecorded", shot("shot.png")]);
  assert.equal(run.status, 0, out(run));
  const [first, second, third, fourth] = vault.read().entries.slice(3);
  assert.equal(first.origin, "third-party");
  assert.equal(first.licence, "No licence held — private reference only");
  assert.equal(first.source, "screenshot, site unrecorded");
  assert.equal(second.source, "https://example.com");
  assert.equal(second.site_url, "https://example.com");
  assert.equal(third.source, "screenshot, site unrecorded", "--source carried over to the image after the one it named");
  assert.equal("site_url" in first, false);
  assert.equal("site_url" in third, false);
  assert.equal(fourth.source, "Dribbble, author unrecorded");
  assert.equal("site_url" in fourth, false, "a prose source is no address to link");
  assert.match(first.added, /^\d{4}-\d{2}-\d{2}$/);
});

test("a command line that names no image after --source, no value after a flag, or no image at all is refused before anything is touched", () => {
  const vault = makeVault();
  for (const [args, said] of [
    [[shot("shot.png"), "--source"], "--source takes a url"],
    [[shot("shot.png"), "--source", "https://example.com"], "--source names no image after it"],
    [[shot("shot.png"), "--model"], "--model takes a model name"],
    [["--model", shot("shot.png")], "no images given"],
    [[shot("shot.png"), "--project"], "--project takes a project key"],
    [[], "no images given"],
  ]) {
    const run = vault.run(args);
    assert.equal(run.status, 2, `${args.join(" ")}\n${out(run)}`);
    assert.ok(run.stderr.startsWith(`ingest.js: ${said}\n${USAGE}`), run.stderr);
    assert.equal(run.calls.length, 0);
  }
  assert.deepEqual(vault.images(), expectedImages());
  assert.equal(vault.read().entries.length, 3);
});

test("the prompt's collection, keyword and Manta group lists are read from gallery.json", () => {
  const prompt = makeVault().run([shot("shot.png")]).calls[0].prompt;
  assert.match(prompt, /^Read the image at this exact path: \/.+\/images\/ingest-\d+-\d+\.png\n/);
  assert.ok(prompt.includes(`"collection": "<one of: flat-poster | or 'NEW'>"`), prompt);
  assert.ok(prompt.includes("1-4 slugs chosen ONLY from: ink-line | minimal | scroll-driven"), prompt);
  assert.ok(prompt.includes("0 or more of: mascot-renderings (Mascot renderings) | motion-references (Motion references); a proposal only"), prompt);
  assert.ok(prompt.includes("1 or more of: hero (The opening screen) | footer (The bottom of the page) | art-only (A picture with no page around it): the part"), prompt);

  const changed = makeVault((gallery) => {
    gallery.collections.push({ id: "ink-botanical" });
    gallery.keywords_allowed.push("night");
    gallery.projects.manta.groups.pop();
  }).run([shot("shot.png")]).calls[0].prompt;
  assert.ok(changed.includes("<one of: flat-poster | ink-botanical | or 'NEW'>"), changed);
  assert.ok(changed.includes("ONLY from: ink-line | minimal | scroll-driven | night\""), changed);
  assert.ok(changed.includes("0 or more of: mascot-renderings (Mascot renderings); a proposal only"), changed);
});

test("a NEW collection lands as a draft block of the eight collection keys, the entry filed under it", () => {
  const vault = makeVault();
  const run = vault.run([shot("shot.png")], [extraction("Risograph", { collection: "NEW", new_collection: { id: "risograph-print", name: "Risograph Print", accent: "#FF48B0" } })]);
  assert.equal(run.status, 0, out(run));
  const gallery = vault.read();
  assert.deepEqual(gallery.collections.at(-1), {
    id: "risograph-print",
    name: "Risograph Print",
    description: "",
    deployFor: "",
    vocabulary: [],
    risk: "",
    accent: "#FF48B0",
    imageStyle: "",
  });
  assert.equal(gallery.entries.at(-1).collection, "risograph-print");
  assert.match(run.stdout, /draft collection "risograph-print" — accept it at review/);
  const result = vault.validate();
  assert.equal(result.status, 0, result.stderr);
});

test("the ingest sets the page parts on a new reference, dropping any not on the list", () => {
  const vault = makeVault();
  const run = vault.run([shot("shot.png")], [extraction("Parts", { page_parts: ["hero", "hero-art", "footer"] })]);
  assert.equal(run.status, 0, out(run));
  assert.deepEqual(vault.read().entries.at(-1).page_parts, ["hero", "footer"]);
  assert.match(run.stdout, /page parts outside page_parts dropped: hero-art/);
  const result = vault.validate();
  assert.equal(result.status, 0, result.stderr);
});

test("an extraction with no page part on the list is saved with none and flagged for the review", () => {
  const vault = makeVault();
  const run = vault.run([shot("shot.png")], [extraction("Partless", { page_parts: ["hero-art"] })]);
  assert.equal(run.status, 0, out(run));
  assert.deepEqual(vault.read().entries.at(-1).page_parts, []);
  assert.ok(run.stdout.includes("  ! no page part left — name one at review\n"), run.stdout);
});

test("the draft never carries a verdict: off-list keywords and group ids are dropped, and fit is never written", () => {
  const vault = makeVault();
  const run = vault.run(
    [shot("shot.png"), shot("shot.jpg")],
    [
      extraction("Proposed", { keywords: ["minimal", "neon"], proposed_manta_groups: ["mascot-renderings", "hero-art"] }),
      extraction("Unproposed", { image_recipe: null, composition: null }),
    ],
  );
  assert.equal(run.status, 0, out(run));
  assert.match(run.stdout, /keywords outside keywords_allowed dropped: neon/);
  const [proposed, unproposed] = vault.read().entries.slice(3);
  assert.deepEqual(proposed.keywords, ["minimal"]);
  assert.deepEqual(proposed.proposed_manta_groups, ["mascot-renderings"]);
  for (const key of ["proposed_manta_groups", "image_recipe", "composition"]) assert.equal(key in unproposed, false, key);
  for (const entry of [proposed, unproposed]) assert.equal("fit" in entry, false);
  const result = vault.validate();
  assert.equal(result.status, 0, result.stderr);
});

test("--project keeps every image in the run for that project alone, drops Manta proposals, and refuses a project not in the library", () => {
  const vault = makeVault((gallery) => {
    gallery.projects.acme = { name: "Acme", rules: "docs/brand/brand-sheet.md in acme/acme", verdicts: ["on-brand"], groups: [{ id: "hero", name: "Hero" }] };
  });
  const rival = [extraction("Rival", { proposed_manta_groups: ["mascot-renderings"] })];

  const refused = vault.run(["--project", "globex", shot("shot.png")], rival);
  assert.equal(refused.status, 2, out(refused));
  assert.equal(refused.stderr, 'ingest.js: --project "globex" is not in projects — set the project up first\n');
  assert.equal(refused.calls.length, 0);
  assert.deepEqual(vault.images(), expectedImages());

  const run = vault.run(["--project", "acme", shot("shot.png"), shot("shot.jpg")], rival);
  assert.equal(run.status, 0, out(run));
  for (const entry of vault.read().entries.slice(3)) {
    assert.equal(entry.project, "acme");
    assert.equal("proposed_manta_groups" in entry, false);
  }
  const result = vault.validate();
  assert.equal(result.status, 0, result.stderr);
});

test("--model reaches the claude -p call for every image, and a run without it asks for sonnet", () => {
  const vault = makeVault();
  const haiku = vault.run(["--model", "haiku", shot("shot.png"), shot("shot.jpg")]);
  assert.equal(haiku.status, 0, out(haiku));
  const sonnet = vault.run([shot("shot.png"), shot("shot.jpg")]);
  assert.equal(sonnet.status, 0, out(sonnet));
  assert.deepEqual([...haiku.calls, ...sonnet.calls].map((call) => call.model), ["haiku", "haiku", "sonnet", "sonnet"]);
  for (const [run, model] of [[haiku, "haiku"], [sonnet, "sonnet"]])
    assert.deepEqual(run.stdout.split("\n").filter((line) => line.includes("cost")), [`  cost $0.010 on claude-${model}`, `  cost $0.010 on claude-${model}`]);
});

test("each image rebuilds data/vault-data.js from the gallery it just wrote", () => {
  const vault = makeVault();
  const bundlePath = path.join(vault.dir, "data", "vault-data.js");
  const run = vault.run([shot("shot.png")], [extraction("Bundled")]);
  assert.equal(run.status, 0, out(run));
  const written = fs.readFileSync(bundlePath, "utf8");
  assert.ok(written.includes('"Bundled"'), "the bundle does not carry the new entry");
  fs.rmSync(bundlePath);
  const rebuilt = runInProcess(path.join(vault.dir, "bundle.js"), [], { cwd: vault.dir });
  assert.equal(rebuilt.status, 0, rebuilt.stderr);
  assert.equal(written, fs.readFileSync(bundlePath, "utf8"));
});

test("a bundle that cannot be rebuilt is logged, and the image it follows still counts as ingested", () => {
  const vault = makeVault();
  fs.writeFileSync(path.join(vault.dir, "data", "styles.json"), "[,");
  const run = vault.run([shot("shot.png")], [extraction("Kept")]);
  assert.equal(run.status, 0, out(run));
  assert.ok(vault.read().entries.some((e) => e.title === "Kept"));
  assert.match(run.stdout, /data\/vault-data\.js was not rebuilt — run node bundle\.js/);
});
