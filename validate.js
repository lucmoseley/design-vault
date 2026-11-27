#!/usr/bin/env node
/**
 * Usage:
 *   node validate.js                      the working tree's data/gallery.json, data/styles.json and images/
 *   node validate.js --staged             the index's copies
 *   node validate.js --gallery <file> --images <dir> [--styles <file>]
 *                                         --styles defaults to the styles.json beside the gallery
 *
 * Every fault is one line led by its rule name. Exit codes: 0 clean, 1 faults found, 2 a usage error or a file
 * that could not be read.
 */
"use strict";
const { gitIn } = require("./git-read.js");
const { REPO_MARKDOWN_FORM, parseRepoMarkdown } = require("./repo-markdown.js");
const fs = require("fs");
const path = require("path");

const SCHEMA_VERSION = 3;
const ORIGINS = ["manta-original", "ai-generated", "third-party", "unattributed"];
const PURPOSES = [
  "feedback",
  "spatial-consistency",
  "state-indication",
  "preventing-jarring-change",
  "explanation",
  "delight",
];
const SHEET_SECTION = /^§\d+[a-z]?$/;
const ART_ONLY = "art-only";

const list = (value) => (Array.isArray(value) ? value : []);
const isText = (value) => typeof value === "string" && value.trim() !== "";
const isBare = (name) => isText(name) && !name.includes("/") && !name.includes("\\") && name !== ".." && name !== ".";
const isWebAddress = (value) => {
  try {
    return typeof value === "string" && /^https?:\/\//i.test(value) && Boolean(new URL(value));
  } catch {
    return false;
  }
};

function validate(gallery, imageExists, { staged = false, styleIds = new Set() } = {}) {
  const faults = [];
  const fault = (rule, message) => faults.push(`${rule}: ${message}`);
  const onDisk = (name) => isBare(name) && imageExists(name);
  if (typeof gallery !== "object" || gallery === null)
    return ["shape: the file is not a JSON object"];

  if (gallery.schema_version !== SCHEMA_VERSION)
    fault("schema-version", `schema_version is ${JSON.stringify(gallery.schema_version)} — expected ${SCHEMA_VERSION}`);

  const dna = gallery.dna ?? {};
  for (const key of ["constants", "never"])
    if (!Array.isArray(dna[key]))
      fault("dna-shape", `dna.${key} is missing or not a list`);

  const allowed = new Set(list(gallery.keywords_allowed));
  const familiesOf = new Map();
  for (const [family, words] of Object.entries(gallery.keyword_families ?? {}))
    for (const word of list(words)) familiesOf.set(word, [...(familiesOf.get(word) ?? []), family]);
  for (const [word, families] of familiesOf)
    if (families.length > 1)
      fault("keyword-family", `"${word}" is in more than one keyword family: ${families.join(", ")}`);

  const collections = new Set(list(gallery.collections).map((c) => c?.id));
  for (const [index, c] of list(gallery.collections).entries()) {
    const label = `collections[${index}]${isText(c?.id) ? ` (${c.id})` : ""}`;
    if (typeof c !== "object" || c === null) {
      fault("shape", `${label} is not an object`);
      continue;
    }
    if (!("styles" in c)) continue;
    if (!Array.isArray(c.styles)) {
      fault("style-link", `${label}: styles is not a list`);
      continue;
    }
    const linked = new Set();
    for (const style of c.styles) {
      if (linked.has(style)) fault("style-link", `${label}: styles lists ${JSON.stringify(style)} twice`);
      else if (!styleIds.has(style)) fault("unknown-style", `${label}: style ${JSON.stringify(style)} is not in the Style guide`);
      linked.add(style);
    }
  }
  const checkTagList = (key, rule) => {
    const ids = new Set();
    const names = new Set();
    if (!Array.isArray(gallery[key])) fault(rule, `${key} is missing or not a list`);
    for (const [index, item] of list(gallery[key]).entries()) {
      if (!["id", "name", "gloss"].every((field) => isText(item?.[field])))
        fault(rule, `${key}[${index}] lacks an id, a name or a gloss`);
      else if (ids.has(item.id) || names.has(item.name))
        fault(rule, `${key} lists "${item.name}" (${item.id}) twice`);
      ids.add(item?.id);
      names.add(item?.name);
    }
    return ids;
  };
  const pageParts = checkTagList("page_parts", "page-part-list");
  const motionKinds = checkTagList("motion_kinds", "motion-kind-list");
  if (!Array.isArray(gallery.design_words)) fault("design-word-list", "design_words is missing or not a list");
  const designWords = new Set();
  for (const [index, item] of list(gallery.design_words).entries()) {
    if (!isText(item?.word) || !Array.isArray(item.means) || item.means.length === 0 || !item.means.every(isText))
      fault("design-word-list", `design_words[${index}] lacks a word or the words it means`);
    else if (!/^\S+$/.test(item.word) || item.word !== item.word.toLowerCase())
      fault("design-word-list", `design_words[${index}] (${JSON.stringify(item.word)}): the word is not one lower-case word, so search can never match it`);
    else if (designWords.has(item.word)) fault("design-word-list", `design_words lists "${item.word}" twice`);
    designWords.add(item?.word);
  }
  const projects = gallery.projects ?? {};
  for (const [key, project] of Object.entries(projects)) {
    if (!Array.isArray(project?.groups))
      fault("group-list", `projects.${key}.groups is missing or not a list — a project with no group carries []`);
    for (const [field, required] of [["rules", true], ["gate", false]])
      if ((required || project?.[field] !== undefined) && !parseRepoMarkdown(project?.[field]))
        fault(`project-${field}`, `projects.${key}.${field} ${JSON.stringify(project?.[field])} is not ${REPO_MARKDOWN_FORM}, the path inside the repo`);
    if (project?.desktop !== undefined && !(typeof project.desktop === "string" && /^[1-9]\d*x[1-9]\d*$/.test(project.desktop)))
      fault("project-desktop", `projects.${key}.desktop ${JSON.stringify(project.desktop)} is not a width and height in px, as \`1536x864\``);
  }
  if (!Array.isArray(gallery.entries)) {
    fault("shape", "entries is missing or not a list");
    return faults;
  }

  const seen = new Set();
  gallery.entries.forEach((e, index) => {
    const label = `entries[${index}]${isText(e?.id) ? ` (${e.id})` : ""}`;
    if (typeof e !== "object" || e === null) return fault("shape", `${label} is not an object`);

    if (!isText(e.id)) fault("id", `${label}: id is missing or empty`);
    else if (seen.has(e.id)) fault("duplicate-id", `${label}: id "${e.id}" is used by an earlier entry`);
    seen.add(e.id);

    if (!collections.has(e.collection))
      fault("unknown-collection", `${label}: collection ${JSON.stringify(e.collection)} is not in collections[]`);

    const parts = list(e.page_parts);
    if (parts.length === 0) fault("page-part-missing", `${label}: page_parts is empty`);
    for (const part of parts)
      if (!pageParts.has(part)) fault("unknown-page-part", `${label}: page part "${part}" is not in page_parts`);
    if (parts.includes(ART_ONLY) && parts.length > 1)
      fault("art-only", `${label}: page_parts has ${ART_ONLY} beside ${parts.filter((p) => p !== ART_ONLY).join(", ")} — a picture with no page takes no other part`);

    for (const word of list(e.keywords))
      if (!allowed.has(word)) fault("unknown-keyword", `${label}: keyword "${word}" is not in keywords_allowed`);

    for (const [key, fit] of Object.entries(e.fit ?? {})) {
      const project = Object.hasOwn(projects, key) ? projects[key] : undefined;
      if (!project) {
        fault("unknown-project", `${label}: fit.${key} names no project in projects`);
        continue;
      }
      if (typeof fit !== "object" || fit === null) {
        fault("shape", `${label}: fit.${key} is not an object`);
        continue;
      }
      if (!list(project.verdicts).includes(fit.verdict))
        fault("fit-verdict", `${label}: fit.${key}.verdict ${JSON.stringify(fit.verdict)} is not in projects.${key}.verdicts`);
      if (!Array.isArray(fit.groups))
        fault("group-list", `${label}: fit.${key}.groups is missing or not a list — an entry with no group carries []`);
      const groupIds = new Set(list(project.groups).map((g) => g?.id));
      for (const group of list(fit.groups))
        if (!groupIds.has(group))
          fault("fit-group", `${label}: fit.${key}.groups names "${group}", which is not in projects.${key}.groups`);
      if ("sheet_section" in fit && !(typeof fit.sheet_section === "string" && SHEET_SECTION.test(fit.sheet_section)))
        fault("sheet-section", `${label}: fit.${key}.sheet_section ${JSON.stringify(fit.sheet_section)} is not a "§<n>" citation, e.g. "§8"`);
    }

    if ("project" in e) {
      if (!(isText(e.project) && Object.hasOwn(projects, e.project)))
        fault("unknown-project", `${label}: project ${JSON.stringify(e.project)} names no project in projects`);
      else
        for (const key of Object.keys(e.fit ?? {}))
          if (key !== e.project)
            fault("private-fit", `${label}: belongs only to project ${e.project}, so it carries no fit.${key}`);
    }

    if (!ORIGINS.includes(e.origin))
      fault("origin", `${label}: origin ${JSON.stringify(e.origin)} is not one of ${ORIGINS.join(", ")}`);
    for (const key of ["source", "licence"])
      if (!isText(e[key])) fault("provenance", `${label}: ${key} is missing`);

    const hasImage = "file" in e;
    const hasSite = "url" in e;
    if (hasImage === hasSite)
      fault("limb", `${label}: carries ${hasImage ? "both" : "neither"} of the image limb (file) and the site limb (url) — exactly one`);

    for (const key of ["url", "site_url"])
      if (key in e && !isWebAddress(e[key]))
        fault("web-address", `${label}: ${key} ${JSON.stringify(e[key])} is not an http(s) web address`);
    if (hasSite && "site_url" in e)
      fault("web-address", `${label}: carries site_url — a site entry's url is already its address`);

    if ("motion" in e && !PURPOSES.includes(e.motion?.purpose))
      fault("motion-purpose", `${label}: motion.purpose ${JSON.stringify(e.motion?.purpose)} is not one of ${PURPOSES.join(", ")}`);
    if ("motion" in e && !Array.isArray(e.motion?.kinds))
      fault("motion-kind-missing", `${label}: motion.kinds is missing or not a list`);
    for (const kind of list(e.motion?.kinds))
      if (!motionKinds.has(kind)) fault("unknown-motion-kind", `${label}: motion kind "${kind}" is not in motion_kinds`);

    if (hasImage && !onDisk(e.file))
      fault("missing-image", `${label}: file ${JSON.stringify(e.file)} is not on disk under images/`);
    if (hasSite && !onDisk(e.still))
      fault("missing-still", `${label}: still ${JSON.stringify(e.still)} is not on disk under images/`);
    if ("motion" in e && !onDisk(e.motion?.capture))
      fault("missing-capture", `${label}: motion.capture ${JSON.stringify(e.motion?.capture)} is not on disk under images/`);

    if (staged && "proposed_manta_groups" in e)
      fault("draft-proposal", `${label}: carries proposed_manta_groups — delete it, or promote it into fit.manta with a verdict, before committing`);
  });
  return faults;
}

function parseArgs(argv) {
  const options = { staged: false, gallery: null, images: null, styles: null };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--staged") options.staged = true;
    else if (["--gallery", "--images", "--styles"].includes(arg) && argv[i + 1]) options[arg.slice(2)] = argv[++i];
    else throw new Error(`unknown argument ${JSON.stringify(arg)}`);
  }
  if (options.staged && (options.gallery || options.images || options.styles))
    throw new Error("--staged reads the index's data/gallery.json, data/styles.json and images/; it takes no paths");
  return options;
}

function loadStaged(root) {
  const git = gitIn(root);
  const text = git("show", ":data/gallery.json");
  const staged = new Set(git("ls-files", "-z", "--", "images/").split("\0").filter(Boolean));
  return {
    label: "the staged data/gallery.json",
    text,
    readStyles: () => git("show", ":data/styles.json"),
    imageExists: (file) => staged.has(`images/${file}`),
  };
}

function loadFiles(root, options) {
  const galleryPath = path.resolve(options.gallery ?? path.join(root, "data", "gallery.json"));
  const imagesDir = path.resolve(options.images ?? path.join(root, "images"));
  const stylesPath = path.resolve(options.styles ?? path.join(path.dirname(galleryPath), "styles.json"));
  return {
    label: path.relative(process.cwd(), galleryPath) || galleryPath,
    text: fs.readFileSync(galleryPath, "utf8"),
    readStyles: () => fs.readFileSync(stylesPath, "utf8"),
    imageExists: (file) => fs.statSync(path.join(imagesDir, file), { throwIfNoEntry: false })?.isFile() === true,
  };
}

function main(argv) {
  let options;
  try {
    options = parseArgs(argv);
  } catch (error) {
    console.error(`validate.js: ${error.message}`);
    return 2;
  }
  const root = __dirname;
  let source;
  try {
    source = options.staged ? loadStaged(root) : loadFiles(root, options);
  } catch (error) {
    console.error(`validate.js: could not read the gallery — ${error.message.split("\n")[0]}`);
    return 2;
  }
  let gallery;
  try {
    gallery = JSON.parse(source.text.replace(/^﻿/, ""));
  } catch (error) {
    console.error(`validate.js: ${source.label} refused\n  json: ${error.message}`);
    return 1;
  }
  let stylesText;
  try {
    stylesText = source.readStyles();
  } catch (error) {
    console.error(`validate.js: could not read the Style guide — ${error.message.split("\n")[0]}`);
    return 2;
  }
  let styleIds;
  try {
    const guide = JSON.parse(stylesText.replace(/^﻿/, ""));
    if (!Array.isArray(guide?.styles)) throw new Error("it has no styles list");
    styleIds = new Set(guide.styles.map((s) => s?.id));
  } catch (error) {
    console.error(`validate.js: the Style guide refused\n  style-guide: ${error.message}`);
    return 1;
  }
  const faults = validate(gallery, source.imageExists, { staged: options.staged, styleIds });
  if (faults.length) {
    console.error(`validate.js: ${source.label} refused — ${faults.length} fault(s)`);
    for (const f of faults) console.error(`  ${f}`);
    return 1;
  }
  console.log(`validate.js: ${source.label} is a valid schema v3 library — ${gallery.entries.length} entries`);
  return 0;
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));

module.exports = { isWebAddress };
