"use strict";
// The reporter test/all.sh's `node --test` suite runs under (#436): Node's own spec output, unchanged, and each test
// file with a failing test appended once, from the repo root, to the file VAULT_FAILED_FILES names. test/run-lanes.sh
// sets that variable and prints a red suite's files as `FAIL <path>`, the line workflow-core's lander reads.
// node --test with no arguments also loads this file as a test file of no tests, which is harmless.
const fs = require("node:fs");
const path = require("node:path");
const { performance } = require("node:perf_hooks");
const { Readable } = require("node:stream");
const { spec } = require("node:test/reporters");

const fromRoot = (file) => path.relative(process.cwd(), file).split(path.sep).join("/");

async function* recorded(events) {
  const named = new Set();
  const began = new Map();
  const last = new Map();
  const recordSeconds = (file, at) => {
    const seconds = ((at - began.get(file)) / 1000).toFixed(3);
    fs.appendFileSync(process.env.VAULT_FILE_SECONDS, `${fromRoot(file)}\t${seconds}\n`);
    began.delete(file);
  };
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
    if (file && process.env.VAULT_FILE_SECONDS) {
      if (event.type === "test:dequeue" && !began.has(file)) began.set(file, performance.now());
      last.set(file, performance.now());
      if (event.type === "test:summary" && began.has(file)) recordSeconds(file, last.get(file));
    }
    yield event;
  }
  for (const file of began.keys()) recordSeconds(file, last.get(file));
}

module.exports = async function* failedFiles(events) {
  yield* Readable.from(recorded(events)).compose(new spec());
};
