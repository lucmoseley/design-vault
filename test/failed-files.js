"use strict";
// The reporter test/all.sh's `node --test` suite runs under (#436): Node's own spec output, unchanged, and each test
// file with a failing test appended once, from the repo root, to the file VAULT_FAILED_FILES names. test/run-lanes.sh
// sets that variable and prints a red suite's files as `FAIL <path>`, the line workflow-core's lander reads.
// Each file's own wall seconds are appended, as `<path>\t<seconds>`, to the file VAULT_FILE_SECONDS names, for the
// core's run-cost report (#370): from its dequeue, before Node spawns the process that loads it, to its own summary,
// or for a file that failed at load and has none, to the last event naming it, on this process's clock. So a file's
// module load and setup count, and files that run side by side each count whole.
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
  const took = (file, at) => {
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
      // A summary naming a file is that file's own; the run's last one names none.
      if (event.type === "test:summary" && began.has(file)) took(file, last.get(file));
    }
    yield event;
  }
  for (const file of began.keys()) took(file, last.get(file));
}

module.exports = async function* failedFiles(events) {
  yield* Readable.from(recorded(events)).compose(new spec());
};
