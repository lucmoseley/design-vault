#!/usr/bin/env node
/**
 * The vault's one write path: screenshots in, draft entries out
 * (lucmoseley/mantahostels#3631 step 4, lucmoseley/mantahostels#3538).
 *
 * Usage:
 *   node ingest.js [--model <model>] [--project <key>] [--source <url>] <image> [[--source <url>] <image> ...]
 *
 * `--model` names the `claude -p` model for the whole run, sonnet by default.
 * `--project` keeps every image in the run for that one project alone — a
 * client's own site or its rivals — and drops any Manta group proposal.
 * `--source` records where the image that follows it came from, and a web
 * address there also becomes the entry's `site_url`, the page's "Visit site"
 * link; without it the entry says "screenshot, site unrecorded" for the review to fill.
 *
 * For each image, in order:
 *   1. copies it into images/ under a holding name with the sniffed extension —
 *      copying first is what lets `claude -p` read a screenshot from outside the vault;
 *   2. extracts the entry's fields through one `claude -p` call on the copy;
 *   3. renames the copy to <slug>.<ext> and rewrites data/gallery.json by temp
 *      file and rename, so a run killed part-way keeps every image already done;
 *   4. rebuilds data/vault-data.js, so the page opened from its folder shows the
 *      new entry on refresh (#32); a failure there is logged, never counted
 *      against an image already saved.
 *
 * Nothing commits. The uncommitted tree is the draft the founder reviews.
 * `proposed_manta_groups` is a proposal only: the review drops it, or promotes
 * it into `fit.manta` with a verdict. The ingest never writes `fit`.
 */
"use strict";
const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const { writeBundle } = require("./bundle");
const { isWebAddress } = require("./validate");

const ROOT = __dirname;
// #4's cap, as the spec it builds (lucmoseley/mantahostels#3631 step 4) gave it.
const MAX_IMAGE = 20 * 1024 * 1024;
const DEFAULTS = {
  origin: "third-party",
  licence: "No licence held — private reference only",
  source: "screenshot, site unrecorded",
};
const COLLECTION_KEYS = ["id", "name", "description", "deployFor", "vocabulary", "risk", "accent", "imageStyle"];

// SCHEMA and buildPrompt's text are carried verbatim from the spec's step 4;
// only the prompt's four lists are templated. The page-part line and its list
// are #29 Q1 and Q4's; the groups carry their names because each is Manta's own
// use, not the page part its id resembles (#40).
const SCHEMA = JSON.stringify({
  type: "object",
  required: ["title", "collection", "page_parts", "description", "note", "keywords", "vocabulary", "proposed_manta_groups"],
  properties: {
    title: { type: "string" },
    collection: { type: "string" },
    new_collection: { type: ["object", "null"] },
    page_parts: { type: "array", items: { type: "string" } },
    description: { type: "string" },
    note: { type: "string" },
    keywords: { type: "array", items: { type: "string" } },
    vocabulary: { type: "array", items: { type: "string" } },
    image_recipe: { type: ["string", "null"] },
    composition: { type: ["string", "null"] },
    proposed_manta_groups: { type: "array", items: { type: "string" } },
  },
  additionalProperties: false,
});

// Its counts, 1-4 keywords and 5-8 vocabulary terms, are the spec's prompt (lucmoseley/mantahostels#3631 step 4, #4).
function buildPrompt(gallery, imagePath) {
  const ids = (items) => (items ?? []).map((item) => item.id).join(" | ");
  const parts = (gallery.page_parts ?? []).map((part) => `${part.id} (${part.gloss})`).join(" | ");
  const groups = (gallery.projects?.manta?.groups ?? []).map((group) => `${group.id} (${group.name})`).join(" | ");
  return `Read the image at this exact path: ${imagePath}

You are an expert UI designer cataloguing a personal design inspiration library shared by several projects. Analyse this screenshot and return ONLY a JSON object (no markdown fences, no commentary) with this shape:
{
  "title": "short site/brand name visible or descriptive name",
  "collection": "<one of: ${ids(gallery.collections)} | or 'NEW'>",
  "new_collection": { "id": "kebab-id", "name": "Name", "description": "...", "deployFor": "...", "vocabulary": ["..."], "risk": "one bold move suggestion", "accent": "#hex", "imageStyle": "generalised [SUBJECT] image-style template" },
  "page_parts": ["1 or more of: ${parts}: the part of a page the screenshot is about, plus any other part with something worth taking; an ordinary menu or footer is not tagged; art-only stands alone"],
  "description": "two sentences, what is literally on the page: layout, type, colour, imagery",
  "note": "one sentence: the single most stealable idea, written for any project, not one brand",
  "keywords": ["1-4 slugs chosen ONLY from: ${(gallery.keywords_allowed ?? []).join(" | ")}"],
  "vocabulary": ["5-8 objective design-vocabulary terms an expert would use"],
  "image_recipe": "an image-generation prompt recreating the hero/background image STYLE with the subject as [SUBJECT: ...]; null if there is no meaningful hero image",
  "composition": "one sentence on how the hero image sits in the layout; null if none",
  "proposed_manta_groups": ["0 or more of: ${groups}; a proposal only, no verdict"]
}
Rules: keywords must come from the list given, nothing else. vocabulary must be objective and promptable. Only use NEW + new_collection if the screenshot genuinely fits none of the existing collections. Return raw JSON only.`;
}

/** The one paid call, and the seam the tests replace; claude is read from WFC_CLAUDE_BIN where set (base §N7, #124). */
function claudeExtract(prompt, model = "sonnet", log = console.log) {
  let out;
  try {
    out = execFileSync(
      process.env.WFC_CLAUDE_BIN || "claude",
      ["-p", prompt, "--model", model, "--output-format", "json", "--json-schema", SCHEMA, "--tools", "Read", "--max-turns", "4"],
      // Guesses, not measurements (#4): four turns to read the screenshot and answer, five minutes for one
      // screenshot's extraction, and 16 MiB for its JSON answer.
      { cwd: ROOT, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], timeout: 300000, maxBuffer: 16 * 1024 * 1024 },
    );
  } catch (error) {
    const said = String(error.stderr || error.stdout || "").trim().split("\n").at(-1);
    throw new Error(`claude -p failed (${error.signal ?? `exit ${error.status}`}): ${said || "no output"}`);
  }
  const result = JSON.parse(out);
  // A failed answer is quoted to 300 characters: a guess at enough to name the fault.
  if (result.is_error || !result.structured_output)
    throw new Error(`claude -p returned no structured output (${result.subtype ?? "no subtype"}): ${String(result.result ?? "").slice(0, 300)}`);
  // The alias passed is not the model billed, so the line names what answered.
  const answered = Object.keys(result.modelUsage ?? {}).join(", ") || model;
  // To a tenth of a cent: a guess at enough to tell one call's cost from another's.
  if (typeof result.total_cost_usd === "number") log(`  cost $${result.total_cost_usd.toFixed(3)} on ${answered}`);
  return result.structured_output;
}

/** The image type by its first bytes; null for anything else. */
function sniff(bytes) {
  if (bytes.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) return "png";
  if (bytes.subarray(0, 3).equals(Buffer.from([0xff, 0xd8, 0xff]))) return "jpg";
  if (bytes.subarray(0, 4).toString("latin1") === "RIFF" && bytes.subarray(8, 12).toString("latin1") === "WEBP") return "webp";
  return null;
}

function readHead(file) {
  const fd = fs.openSync(file, "r");
  try {
    const head = Buffer.alloc(12);
    return head.subarray(0, fs.readSync(fd, head, 0, 12, 0));
  } finally {
    fs.closeSync(fd);
  }
}

// Forty characters at most: carried from the seed (cth9191/taste-vault), which gives no reason.
function slugify(s) {
  return String(s ?? "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40).replace(/-+$/, "") || "entry";
}

function writeAtomic(file, text) {
  const temp = `${file}.tmp-${process.pid}`;
  fs.writeFileSync(temp, text);
  fs.renameSync(temp, file);
}

function localDate() {
  const now = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
}

/**
 * Picks the extraction's collection: `{ id }`, plus `block` where it is new.
 * A new one is a draft block: its eight keys, blanks where the model gave none.
 */
function resolveCollection(gallery, result, log) {
  const known = (id) => gallery.collections.some((c) => c.id === id);
  if (result.collection !== "NEW" && known(result.collection)) return { id: result.collection };
  const proposed = (result.collection === "NEW" && result.new_collection) || {};
  const id = slugify(proposed.id || proposed.name || "unsorted");
  if (known(id)) {
    log(`  ! proposed collection "${id}" already exists — filed under it`);
    return { id };
  }
  const block = Object.fromEntries(
    COLLECTION_KEYS.map((key) => [key, key === "vocabulary" ? (Array.isArray(proposed[key]) ? proposed[key] : []) : String(proposed[key] ?? "")]),
  );
  block.id = id;
  block.name ||= id;
  log(
    result.collection === "NEW"
      ? `  + draft collection "${id}" — accept it at review, or move the entry and delete the block`
      : `  + draft collection "${id}": the model named "${result.collection}", which is no collection — file the entry at review`,
  );
  return { id, block };
}

function buildEntry(gallery, result, { id, file, collection, source, project, log }) {
  const allowed = new Set(gallery.keywords_allowed ?? []);
  const keywords = (result.keywords ?? []).filter((word) => allowed.has(word));
  const dropped = (result.keywords ?? []).filter((word) => !allowed.has(word));
  if (dropped.length) log(`  ! keywords outside keywords_allowed dropped: ${dropped.join(", ")}`);
  const partIds = new Set((gallery.page_parts ?? []).map((part) => part.id));
  const pageParts = (result.page_parts ?? []).filter((part) => partIds.has(part));
  const offList = (result.page_parts ?? []).filter((part) => !partIds.has(part));
  if (offList.length) log(`  ! page parts outside page_parts dropped: ${offList.join(", ")}`);
  if (!pageParts.length) log("  ! no page part left — name one at review");
  const groupIds = new Set((gallery.projects?.manta?.groups ?? []).map((g) => g.id));
  const proposedGroups = project && project !== "manta" ? [] : (result.proposed_manta_groups ?? []).filter((g) => groupIds.has(g));
  return {
    id,
    title: result.title,
    collection,
    page_parts: pageParts,
    description: result.description,
    note: result.note,
    keywords,
    vocabulary: result.vocabulary ?? [],
    origin: DEFAULTS.origin,
    source: source ?? DEFAULTS.source,
    ...(isWebAddress(source) ? { site_url: source } : {}),
    licence: DEFAULTS.licence,
    added: localDate(),
    file,
    ...(project ? { project } : {}),
    ...(result.image_recipe ? { image_recipe: result.image_recipe } : {}),
    ...(result.composition ? { composition: result.composition } : {}),
    ...(proposedGroups.length ? { proposed_manta_groups: proposedGroups } : {}),
  };
}

const HOLDING = /^ingest-(\d+)-\d+\.(png|jpg|webp)$/;

// A run killed mid-extraction leaves its holding copy behind, which no
// validator sees; the next run deletes any whose run is no longer alive.
function sweepHoldingCopies(imagesDir, log) {
  for (const name of fs.readdirSync(imagesDir)) {
    const pid = Number(name.match(HOLDING)?.[1]);
    if (!pid) continue;
    try {
      process.kill(pid, 0);
      continue;
    } catch (error) {
      if (error.code === "EPERM") continue;
    }
    fs.rmSync(path.join(imagesDir, name), { force: true });
    log(`  - deleted images/${name}, left by a killed run`);
  }
}

/**
 * Ingests `items` ([{ path, source? }]) into the library at `galleryPath` and
 * `imagesDir`. `extract(imagePath)` defaults to the paid call on `model`,
 * prompted from the library as it stands before each image. Returns the number
 * that failed.
 */
function ingest(items, options = {}) {
  const galleryPath = options.galleryPath ?? path.join(ROOT, "data", "gallery.json");
  const imagesDir = options.imagesDir ?? path.join(ROOT, "images");
  const log = options.log ?? console.log;
  const gallery = JSON.parse(fs.readFileSync(galleryPath, "utf8"));
  if (gallery.schema_version !== 3) throw new Error(`${galleryPath} is not schema_version 3 — migrate it before ingesting into it`);
  const { project } = options;
  if (project !== undefined && !Object.hasOwn(gallery.projects ?? {}, project))
    throw new Error(`--project ${JSON.stringify(project)} is not in projects — set the project up first`);
  const extract = options.extract ?? ((imagePath) => claudeExtract(buildPrompt(gallery, imagePath), options.model, log));
  sweepHoldingCopies(imagesDir, log);
  let failed = 0;

  for (const { path: src, source } of items) {
    log(`→ ${src}`);
    let holding;
    try {
      const size = fs.statSync(src).size;
      if (size > MAX_IMAGE) throw new Error(`${(size / 1024 / 1024).toFixed(1)} MB is over the 20 MB cap`);
      const ext = sniff(readHead(src));
      if (!ext) throw new Error("not a PNG, JPEG or WebP by its first bytes");
      holding = path.join(imagesDir, `ingest-${process.pid}-${Date.now()}.${ext}`);
      fs.copyFileSync(src, holding);

      const result = extract(holding);

      const taken = (candidate) =>
        gallery.entries.some((e) => e.id === candidate) || fs.existsSync(path.join(imagesDir, `${candidate}.${ext}`));
      const base = slugify(result.title);
      let id = base;
      for (let n = 2; taken(id); n++) id = `${base}-${n}`;
      const file = `${id}.${ext}`;
      const collection = resolveCollection(gallery, result, log);
      const entry = buildEntry(gallery, result, { id, file, collection: collection.id, source, project, log });
      fs.renameSync(holding, path.join(imagesDir, file));
      holding = null;
      if (collection.block) gallery.collections.push(collection.block);
      gallery.entries.push(entry);
      writeAtomic(galleryPath, `${JSON.stringify(gallery, null, 2)}\n`);
      log(`  ✓ ${entry.title} → images/${file}, collection ${entry.collection}`);
      try {
        writeBundle(path.dirname(galleryPath));
      } catch (bundleError) {
        log(`  ! saved, but data/vault-data.js was not rebuilt — run node bundle.js: ${bundleError.message.split("\n")[0]}`);
      }
    } catch (error) {
      failed++;
      if (holding) fs.rmSync(holding, { force: true });
      log(`  ✗ ${error.message.split("\n")[0]}`);
    }
  }
  return failed;
}

function parseArgs(argv) {
  const items = [];
  let source;
  let model;
  let project;
  const valueAt = (i, what) => {
    if (!argv[i] || argv[i].startsWith("--")) throw new Error(`${argv[i - 1]} takes ${what}`);
    return argv[i];
  };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--model") model = valueAt(++i, "a model name");
    else if (argv[i] === "--source") source = valueAt(++i, "a url");
    else if (argv[i] === "--project") project = valueAt(++i, "a project key");
    else if (argv[i].startsWith("--")) throw new Error(`unknown argument ${JSON.stringify(argv[i])}`);
    else {
      items.push({ path: argv[i], source });
      source = undefined;
    }
  }
  if (source !== undefined) throw new Error("--source names no image after it");
  if (items.length === 0) throw new Error("no images given");
  return { items, model, project };
}

function main(argv) {
  let items, model, project;
  try {
    ({ items, model, project } = parseArgs(argv));
  } catch (error) {
    console.error(`ingest.js: ${error.message}\nUsage: node ingest.js [--model <model>] [--project <key>] [--source <url>] <image> [[--source <url>] <image> ...]`);
    return 2;
  }
  const failed = ingest(items, { model, project });
  console.log(`\n${items.length - failed} of ${items.length} ingested. Review the draft in data/gallery.json, then run node validate.js before committing.`);
  return failed ? 1 : 0;
}

if (require.main === module) {
  try {
    process.exitCode = main(process.argv.slice(2));
  } catch (error) {
    console.error(`ingest.js: ${error.message}`);
    process.exitCode = 2;
  }
}
