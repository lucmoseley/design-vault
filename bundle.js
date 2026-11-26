#!/usr/bin/env node
/**
 * Usage:
 *   node bundle.js             rewrites the working tree's data/vault-data.js
 *   node bundle.js --staged    refuses a commit whose staged bundle does not match its staged JSON
 *
 * Exit codes: 0 clean, 1 the staged bundle is stale, 2 a usage error or a file that could not be read.
 */
"use strict";

const fs = require("fs");
const path = require("path");
const { gitIn } = require("./git-read.js");

const BUNDLE = "data/vault-data.js";

function bundle(galleryText, stylesText) {
  const json = (text, name) => {
    const clean = text.trim();
    try {
      JSON.parse(clean);
    } catch (error) {
      throw new Error(`${name} is not valid JSON — ${error.message}`);
    }
    return clean;
  };
  return (
    `window.VAULT_DATA = {\n"gallery": ${json(galleryText, "data/gallery.json")},\n"styles": ${json(stylesText, "data/styles.json")}\n};\n`
  );
}

function writeBundle(dataDir) {
  const read = (name) => fs.readFileSync(path.join(dataDir, name), "utf8");
  const target = path.join(dataDir, "vault-data.js");
  const temp = `${target}.tmp-${process.pid}`;
  fs.writeFileSync(temp, bundle(read("gallery.json"), read("styles.json")));
  fs.renameSync(temp, target);
  return target;
}

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
