#!/usr/bin/env node
/**
 * Copies data/gallery.json and data/styles.json into data/vault-data.js, a
 * script the page loads directly, so index.html opens from its folder with no
 * server: a browser refuses fetch() on a file:// page (#32).
 *
 * Usage:
 *   node bundle.js             rewrites the working tree's data/vault-data.js
 *   node bundle.js --staged    refuses a commit whose staged bundle does not match its staged JSON
 *
 * ingest.js reruns it after every image. Exit codes: 0 clean, 1 the staged
 * bundle is stale, 2 a usage error or a file that could not be read.
 */
"use strict";

const fs = require("fs");
const path = require("path");
const { gitIn } = require("./git-read.js");

const BUNDLE = "data/vault-data.js";

// The JSON goes in verbatim, so a diff of the bundle reads like the diff of the
// file it came from. Parsing first means a malformed file fails here, loudly,
// rather than as a syntax error on the page.
function bundle(galleryText, stylesText) {
  const json = (text, name) => {
    const clean = text.trim(); // trim() drops a byte-order mark too
    try {
      JSON.parse(clean);
    } catch (error) {
      throw new Error(`${name} is not valid JSON — ${error.message}`);
    }
    return clean;
  };
  return (
    "// Derived from data/gallery.json and data/styles.json by `node bundle.js` — never edit it by hand (#32).\n" +
    `window.VAULT_DATA = {\n"gallery": ${json(galleryText, "data/gallery.json")},\n"styles": ${json(stylesText, "data/styles.json")}\n};\n`
  );
}

// Writes the bundle beside the gallery it came from, by temp file and rename so
// a page opened mid-write never reads half of it.
function writeBundle(dataDir) {
  const read = (name) => fs.readFileSync(path.join(dataDir, name), "utf8");
  const target = path.join(dataDir, "vault-data.js");
  const temp = `${target}.tmp-${process.pid}`;
  fs.writeFileSync(temp, bundle(read("gallery.json"), read("styles.json")));
  fs.renameSync(temp, target);
  return target;
}

// Reads the index, never the working tree, so the hook judges this commit's
// bytes and not a parallel session's half-written copy.
function checkStaged(root) {
  const git = gitIn(root);
  const staged = new Set(git("ls-files", "-z", "--", "data/gallery.json", "data/styles.json", BUNDLE).split("\0").filter(Boolean));
  if (!staged.has("data/gallery.json") || !staged.has("data/styles.json"))
    throw new Error("the index holds no data/gallery.json or data/styles.json");
  return staged.has(BUNDLE) && git("show", `:${BUNDLE}`) === bundle(git("show", ":data/gallery.json"), git("show", ":data/styles.json"));
}

function main(argv) {
  const staged = argv[0] === "--staged";
  if (argv.length > (staged ? 1 : 0)) {
    console.error(`bundle.js: unknown argument ${JSON.stringify(argv[staged ? 1 : 0])}`);
    return 2;
  }
  const root = __dirname;
  try {
    if (staged) {
      if (checkStaged(root)) return 0;
      console.error(`bundle.js: the staged ${BUNDLE} does not match the staged data/gallery.json and data/styles.json.`);
      console.error(`  Run node bundle.js, then commit ${BUNDLE} with them.`);
      return 1;
    }
    const target = writeBundle(path.join(root, "data"));
    console.log(`bundle.js: wrote ${path.relative(process.cwd(), target)}`);
    return 0;
  } catch (error) {
    console.error(`bundle.js: ${error.message.split("\n")[0]}`);
    return 2;
  }
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));

module.exports = { writeBundle };
