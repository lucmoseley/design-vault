"use strict";
// The plugin manifest carries no version (#13), read straight off the file: a set version outranks the
// marketplace's sha pin, so loosen this and a sha-only release never reaches an installed consumer.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");

const ROOT = path.join(__dirname, "..");
const MANIFEST = path.join(ROOT, "plugin", ".claude-plugin", "plugin.json");

test("the plugin manifest carries no version", () => {
  const manifest = JSON.parse(fs.readFileSync(MANIFEST, "utf8"));
  assert.equal(Object.hasOwn(manifest, "version"), false);
});
