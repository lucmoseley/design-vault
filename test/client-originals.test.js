"use strict";
// Tests plugin/skills/design-project/scripts/client-originals.py (#108): node --test test/client-originals.test.js
// It pins that a held original is never lost, overwritten or swapped for a worse
// copy, and that a send folder holds only held bytes; a gap here lets a client be
// sent re-saved files again, as design-vault#90 P8 did.
require("./no-git-env");
const assert = require("node:assert/strict");
const { execFileSync, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, beforeEach, test } = require("node:test");

const SCRIPT = path.join(__dirname, "..", "plugin", "skills", "design-project", "scripts", "client-originals.py");
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), "client-originals-"));
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

let repo;
let n = 0;
const run = (...args) => spawnSync("python3", [SCRIPT, "--root", repo, ...args], { encoding: "utf8" });
const manifest = () => JSON.parse(fs.readFileSync(path.join(repo, "docs/brand/client-originals.json"), "utf8"));
const store = (...p) => path.join(repo, "private/client-originals", ...p);

// Writes a w x h JPEG at the given quality; the same seed draws the same picture.
function jpeg(name, w, h, quality, seed = 1) {
  const out = path.join(scratch, name);
  execFileSync("python3", ["-c", `
import random, sys
from PIL import Image
random.seed(${seed})
im = Image.new("RGB", (${w}, ${h}))
im.putdata([(random.randrange(256), random.randrange(256), random.randrange(256)) for _ in range(${w * h})])
im.save(sys.argv[1], quality=${quality})`, out]);
  return out;
}

beforeEach(() => {
  repo = path.join(scratch, `repo-${n++}`);
  fs.mkdirSync(repo);
  execFileSync("git", ["init", "-q"], { cwd: repo });
  fs.writeFileSync(path.join(repo, ".gitignore"), "/private/\n");
  assert.equal(run("init").status, 0);
});

test("init refuses a folder git would track, and writes an empty manifest once it is ignored", () => {
  fs.writeFileSync(path.join(repo, ".gitignore"), "");
  const r = run("init");
  assert.equal(r.status, 1);
  assert.match(r.stdout, /REFUSED: .* is not gitignored; add \/private\/ to \.gitignore/);
  assert.equal(run("add", "a", jpeg("a.jpg", 4, 3, 95), "--source", "s", "--status", "exact").status, 1);
  fs.writeFileSync(path.join(repo, ".gitignore"), "/private/\n");
  assert.equal(run("init").status, 0);
  assert.deepEqual(manifest(), {});
});

test("add records the source, bytes, pixel size and hash of a byte-exact copy", () => {
  const file = jpeg("a.jpg", 40, 30, 95);
  assert.equal(run("add", "pool-01", file, "--source", "https://example.com/a.jpg", "--status", "exact").status, 0);
  const e = manifest()["pool-01"];
  assert.deepEqual([e.file, e.w, e.h, e.bytes, e.source, e.status], ["pool-01.jpg", 40, 30, fs.statSync(file).size, "https://example.com/a.jpg", "exact"]);
  assert.ok(fs.readFileSync(store("pool-01.jpg")).equals(fs.readFileSync(file)));
});

test("a file with no pixel size, such as an SVG logo, is held with none", () => {
  const svg = path.join(scratch, "logo.svg");
  fs.writeFileSync(svg, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"/>');
  assert.equal(run("add", "logo", svg, "--source", "the client's email", "--status", "exact").status, 0);
  assert.deepEqual([manifest().logo.w, manifest().logo.h], [null, null]);
});

test("a copy with fewer pixels never replaces the held file, even with --supersede", () => {
  assert.equal(run("add", "p", jpeg("big.jpg", 40, 30, 95), "--source", "s", "--status", "exact").status, 0);
  const before = fs.readFileSync(store("p.jpg"));
  const r = run("add", "p", jpeg("small.jpg", 20, 15, 95), "--source", "s", "--status", "exact", "--supersede", "newer");
  assert.equal(r.status, 1);
  assert.match(r.stdout, /fewer pixels than the held 40x30/);
  assert.ok(fs.readFileSync(store("p.jpg")).equals(before));
});

test("a different file of the same size replaces the held one only with a stated reason, and the old one is kept aside", () => {
  assert.equal(run("add", "p", jpeg("first.jpg", 40, 30, 60), "--source", "s", "--status", "degraded").status, 0);
  const old = manifest().p.sha256;
  const second = jpeg("second.jpg", 40, 30, 95);
  const refused = run("add", "p", second, "--source", "s", "--status", "exact");
  assert.equal(refused.status, 1);
  assert.match(refused.stdout, /Pass --supersede/);
  assert.equal(run("add", "p", second, "--source", "s", "--status", "exact", "--supersede", "the client's own file").status, 0);
  const [kept] = manifest().p.superseded;
  assert.equal(kept.sha256, old);
  assert.equal(kept.why_replaced, "the client's own file");
  assert.ok(fs.existsSync(store(kept.file)));
  assert.equal(run("verify").status, 0);
});

test("one file is held under one id only", () => {
  const file = jpeg("a.jpg", 40, 30, 95);
  assert.equal(run("add", "one", file, "--source", "s", "--status", "exact").status, 0);
  const r = run("add", "two", file, "--source", "s", "--status", "exact");
  assert.equal(r.status, 1);
  assert.match(r.stdout, /already held as one/);
});

test("verify finds a held file re-saved in place, a stray file and a missing file", () => {
  assert.equal(run("add", "a", jpeg("a.jpg", 40, 30, 95, 1), "--source", "s", "--status", "exact").status, 0);
  assert.equal(run("add", "b", jpeg("b.jpg", 40, 30, 95, 2), "--source", "s", "--status", "exact").status, 0);
  fs.copyFileSync(jpeg("resaved.jpg", 40, 30, 40, 1), store("a.jpg"));
  fs.writeFileSync(store("review-thumb.jpg"), "x");
  fs.rmSync(store("b.jpg"));
  const r = run("verify");
  assert.equal(r.status, 1);
  assert.match(r.stdout, /CHANGED a:/);
  assert.match(r.stdout, /UNLISTED review-thumb\.jpg/);
  assert.match(r.stdout, /MISSING b:/);
});

test("send builds the folder byte-exact from the store, and check refuses a re-saved copy of the same pixel size (#90 P8)", () => {
  assert.equal(run("add", "radio", jpeg("radio.jpg", 40, 30, 95), "--source", "s", "--status", "exact").status, 0);
  const out = path.join(scratch, `send-${n}`);
  const sent = run("send", out, "radio=08-radio-interview");
  assert.equal(sent.status, 0, sent.stdout);
  assert.match(sent.stdout, /ok 08-radio-interview\.jpg = radio/);
  fs.copyFileSync(jpeg("radio-resaved.jpg", 40, 30, 40), path.join(out, "08-radio-interview.jpg"));
  const r = run("check", out);
  assert.equal(r.status, 1);
  assert.match(r.stdout, /NOT HELD 08-radio-interview\.jpg/);
});

test("a degraded original fails the send check unless allowed", () => {
  assert.equal(run("add", "d", jpeg("d.jpg", 40, 30, 95), "--source", "s", "--status", "degraded", "--note", "only a 1400 px copy").status, 0);
  const out = path.join(scratch, `send-${n}`);
  const r = run("send", out, "d");
  assert.equal(r.status, 1);
  assert.match(r.stdout, /DEGRADED d\.jpg = d: only a 1400 px copy/);
  assert.match(r.stdout, /pass --allow-degraded to accept them/);
  assert.equal(run("check", out, "--allow-degraded").status, 0);
});

test("an id with a dot is refused, so two ids never share a stored name", () => {
  const r = run("add", "q.png", jpeg("q.jpg", 4, 3, 95), "--source", "s", "--status", "exact");
  assert.equal(r.status, 1);
  assert.match(r.stdout, /an id is letters, digits/);
});

test("re-adding the same bytes restores a lost original, and a lost one can still be superseded", () => {
  const file = jpeg("lost.jpg", 40, 30, 95);
  assert.equal(run("add", "p", file, "--source", "s", "--status", "exact").status, 0);
  fs.rmSync(store("p.jpg"));
  assert.match(run("add", "p", file, "--source", "s", "--status", "exact").stdout, /restored the lost file/);
  assert.ok(fs.readFileSync(store("p.jpg")).equals(fs.readFileSync(file)));
  fs.rmSync(store("p.jpg"));
  const r = run("add", "p", jpeg("other.jpg", 40, 30, 95, 2), "--source", "s", "--status", "exact", "--supersede", "the original is gone");
  assert.equal(r.status, 0, r.stderr);
  assert.equal(manifest().p.superseded[0].file, null);
  assert.equal(run("verify").status, 0);
});

test("a degraded copy never replaces an exact original, nor a raster a file with no pixel size", () => {
  assert.equal(run("add", "p", jpeg("ex.jpg", 40, 30, 95), "--source", "s", "--status", "exact").status, 0);
  const r = run("add", "p", jpeg("big.jpg", 80, 60, 95), "--source", "s", "--status", "degraded", "--supersede", "bigger");
  assert.equal(r.status, 1);
  assert.match(r.stdout, /a degraded copy cannot replace the exact original/);
  const svg = path.join(scratch, `logo-${n}.svg`);
  fs.writeFileSync(svg, '<svg xmlns="http://www.w3.org/2000/svg"/>');
  assert.equal(run("add", "logo", svg, "--source", "s", "--status", "exact").status, 0);
  const png = run("add", "logo", jpeg("logo.jpg", 400, 300, 95), "--source", "s", "--status", "exact", "--supersede", "bigger");
  assert.equal(png.status, 1);
  assert.match(png.stdout, /raster cannot replace the held file/);
});

test("send writes nothing when one item is unknown or two share a name", () => {
  assert.equal(run("add", "a", jpeg("a.jpg", 4, 3, 95, 1), "--source", "s", "--status", "exact").status, 0);
  assert.equal(run("add", "b", jpeg("b.jpg", 4, 3, 95, 2), "--source", "s", "--status", "exact").status, 0);
  const out = path.join(scratch, `send-${n}`);
  const unknown = run("send", out, "a=hero", "zz");
  assert.equal(unknown.status, 1);
  assert.match(unknown.stdout, /REFUSED zz: not in the store/);
  const twice = run("send", out, "a=hero", "b=hero");
  assert.equal(twice.status, 1);
  assert.match(twice.stdout, /hero\.jpg is already named for a/);
  assert.equal(fs.existsSync(out), false);
});

test("check fails on a folder with no files", () => {
  const out = path.join(scratch, `empty-${n}`);
  fs.mkdirSync(out);
  const r = run("check", out);
  assert.equal(r.status, 1);
  assert.match(r.stdout, /holds no files/);
});
