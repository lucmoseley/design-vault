"use strict";
require("./no-git-env");
const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");

const ROOT = path.join(__dirname, "..");
const source = fs.readFileSync(path.join(ROOT, "test", "all.sh"), "utf8");
const known = source.match(/^known_needs=\(([^)]*)\)$/m)[1];
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "suite-needs-"));
after(() => fs.rmSync(dir, { recursive: true, force: true }));

// #609
const runWithNeed = (word) => {
  const root = fs.mkdtempSync(path.join(dir, "repo-"));
  fs.mkdirSync(path.join(root, "test"));
  fs.writeFileSync(path.join(root, "test", "all.sh"),
    source.replace(/^registry='/m, `registry='python3 test/planted.test.py\t${word}\n`));
  return spawnSync("bash", ["test/all.sh", "--plan"], { cwd: root, encoding: "utf8" });
};

for (const word of ["gpu", "image", "chromium2"]) {
  test(`a suite needing '${word}', no word known_needs holds, is refused with exit 2 naming every known word`, () => {
    const r = runWithNeed(word);
    assert.equal(r.status, 2, r.stderr + r.stdout);
    assert.equal(r.stderr,
      `test/all.sh: python3 test/planted.test.py needs '${word}', which is none of ${known}\n`);
  });
}
