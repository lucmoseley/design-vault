"use strict";
const assert = require("node:assert/strict");
const { test } = require("node:test");
const { parseRepoMarkdown } = require("../repo-markdown.js");

test("a value written as <path> in <owner>/<repo> parses to its file and repo (#569)", () => {
  assert.deepEqual(parseRepoMarkdown("docs/brand/brand-sheet.md in lucmoseley/mantahostels"), { file: "docs/brand/brand-sheet.md", owner: "lucmoseley", repo: "mantahostels" });
});

test("a value off the form parses to null", () => {
  for (const value of [undefined, 3, "docs/brand/brand-sheet.md", "docs/a.txt in o/r", "/docs/a.md in o/r", "docs/../a.md in o/r", "a.md in ../r", "a.md in o/r/extra"])
    assert.equal(parseRepoMarkdown(value), null, JSON.stringify(value));
});
