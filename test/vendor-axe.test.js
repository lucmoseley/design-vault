"use strict";
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");

const SOURCE = path.join(__dirname, "..", "plugin/skills/design-round/vendor/axe-core/SOURCE");
const AXE = path.join(__dirname, "..", "plugin/skills/design-round/vendor/axe-core/axe.min.js");
const LICENSE = path.join(__dirname, "..", "plugin/skills/design-round/vendor/axe-core/LICENSE");
const read = fs.readFileSync;
// guess, #501
const HEADER_BYTES = 200;

test("#307: the vendored axe.min.js hashes to Deque's published sha256 for its version", () => {
  const source = read(SOURCE).toString("utf8");
  const version = source.match(/^axe-core (\d+\.\d+\.\d+),/)?.[1];
  const sri = source.match(/^sha256: (sha256-[A-Za-z0-9+/=]+)$/m)?.[1];
  assert.ok(version && sri, "SOURCE names the version and its sha256");
  const file = read(AXE);
  assert.equal(`sha256-${crypto.createHash("sha256").update(file).digest("base64")}`, sri);
  assert.ok(file.toString("utf8", 0, HEADER_BYTES).startsWith(`/*! axe v${version}\n`), "the file is the version SOURCE names");
});

test("the vendored axe-core keeps its licence beside it", () => {
  assert.match(read(LICENSE).toString("utf8"), /^Mozilla Public License, version 2\.0$/m);
});
