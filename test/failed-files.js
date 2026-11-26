"use strict";
// The reporter test/all.sh's `node --test` suite runs under (#436): Node's own spec output, unchanged, and each test
// file with a failing test appended once, from the repo root, to the file VAULT_FAILED_FILES names. test/run-lanes.sh
// sets that variable and prints a red suite's files as `FAIL <path>`, the line workflow-core's lander reads.
// node --test with no arguments also loads this file as a test file of no tests, which is harmless.
const fs = require("node:fs");
const path = require("node:path");
const { Readable } = require("node:stream");
const { spec } = require("node:test/reporters");

const fromRoot = (file) => path.relative(process.cwd(), file).split(path.sep).join("/");

const isFileTest = (event) => event.type === "test:complete" && event.data.nesting === 0
  && path.resolve(event.data.name) === event.data.file;

async function* recorded(events) {
  const named = new Set();
  const fileMs = new Map();
  for await (const event of events) {
    const { file, todo } = event.data ?? {};
    // A failing todo test fails no run, so it names no file.
    if (event.type === "test:fail" && file && !todo && process.env.VAULT_FAILED_FILES) {
      const rel = fromRoot(file);
      if (!named.has(rel)) {
        named.add(rel);
        fs.appendFileSync(process.env.VAULT_FAILED_FILES, `${rel}\n`);
      }
    }
    if (file && isFileTest(event)) fileMs.set(file, event.data.details.duration_ms);
    yield event;
  }
  if (!process.env.VAULT_FILE_SECONDS) return;
  for (const [file, ms] of fileMs) fs.appendFileSync(process.env.VAULT_FILE_SECONDS, `${fromRoot(file)}\t${(ms / 1000).toFixed(3)}\n`);
}

module.exports = async function* failedFiles(events) {
  yield* Readable.from(recorded(events)).compose(new spec());
};
