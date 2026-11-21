"use strict";
// gate.js list, which joins the vault's gate and a project's into one numbered list for an asset (#158): driven
// through its CLI on the vault's store of rule records and on two fixture gates that hold every kind of clash.
// Loosen it and a critic answers a question that does not apply, two critics number one list differently, or two rules
// that cannot both hold reach a round with nobody told.
const assert = require("node:assert/strict");
const { runInProcess } = require("./core-run-in-process.js");
const path = require("node:path");
const { test } = require("node:test");

const ROOT = path.join(__dirname, "..");
const SCRIPT = path.join(ROOT, "plugin", "skills", "design-round", "scripts", "gate.js");
const FORM = path.join(ROOT, "plugin", "skills", "design-round", "scripts", "gate-form.js");
const VAULT_GATE = path.join(ROOT, "plugin", "skills", "design-critique", "rules");
const FIXTURES = path.join(__dirname, "fixtures", "gate");
const FIXTURE_GATES = [path.join(FIXTURES, "list-vault.md"), path.join(FIXTURES, "list-project.md")];

const list = (args, files = [VAULT_GATE]) => {
  const r = runInProcess(SCRIPT, ["list", ...args, ...files]);
  return { status: r.status, out: r.stdout, err: r.stderr };
};
// The ids a list holds, in its numbered order.
const ids = (out) => [...out.matchAll(/^\d+\. (\S+?)(?: \(\w+\))?:/gm)].map((m) => m[1]);
const clashLines = (out) => out.slice(out.indexOf("Clashes, for the reveal:")).split("\n").filter((l) => l.startsWith("- "));
// The one clash line naming both ids, its numbers blanked to N.
const clash = (lines, a, b) => {
  const found = lines.filter((l) => l.includes(` ${a} `) && l.includes(` ${b} `)).map((l) => l.replace(/\d+\. /g, "N. "));
  assert.equal(found.length, 1, `${a} with ${b}:\n${lines.join("\n")}`);
  return found[0];
};
const fixtureClashes = () => clashLines(list(["--asset", "web-surface"], FIXTURE_GATES).out);

const BRAND_MOTION_ONLY = ["vault.flow-script", "vault.flow-code", "vault.fall-script", "vault.flow-look", "vault.length-range", "vault.length", "vault.end-frame"];

test("list keeps the motion questions only for an asset with brand motion", () => {
  const still = list(["--asset", "web-surface"]);
  assert.equal(still.status, 0, still.out + still.err);
  for (const id of BRAND_MOTION_ONLY) assert.ok(!ids(still.out).includes(id), `${id} in a still asset's list`);
  // #183 Q3 (B): interface motion alone, such as a hover, takes the project's motion tokens, not the craft gate.
  const interfaceOnly = list(["--asset", "web-surface", "--fact", "has-motion"]);
  assert.equal(interfaceOnly.status, 0, interfaceOnly.out + interfaceOnly.err);
  for (const id of BRAND_MOTION_ONLY) assert.ok(!ids(interfaceOnly.out).includes(id), `${id} in an interface-motion asset's list`);
  const brand = list(["--asset", "web-surface", "--fact", "has-motion", "--fact", "has-brand-motion"]);
  assert.equal(brand.status, 0, brand.out + brand.err);
  for (const id of BRAND_MOTION_ONLY) assert.ok(ids(brand.out).includes(id), `${id} missing from a brand-motion asset's list`);
});

test("list keeps the clip-loop question for a motion asset alone, not a page's brand motion (#336)", () => {
  const page = list(["--asset", "web-surface", "--fact", "has-motion", "--fact", "has-brand-motion"]);
  assert.ok(!ids(page.out).includes("vault.clip-loop"), "vault.clip-loop in a web surface's list");
  const clip = list(["--asset", "motion", "--fact", "has-motion", "--fact", "has-brand-motion"]);
  assert.equal(clip.status, 0, clip.out + clip.err);
  assert.ok(ids(clip.out).includes("vault.clip-loop"), "vault.clip-loop missing from a motion asset's list");
});

test("list drops the page questions for brand art and keeps them for a web surface, the first screen's only with a call to action", () => {
  assert.ok(!ids(list(["--asset", "brand-art"]).out).includes("vault.reflow"));
  assert.ok(ids(list(["--asset", "web-surface"]).out).includes("vault.reflow"));
  assert.ok(!ids(list(["--asset", "web-surface"]).out).includes("vault.layout"));
  assert.ok(ids(list(["--asset", "web-surface", "--fact", "has-cta"]).out).includes("vault.layout"));
});

test("list keeps the focal box's crop question for brand art and a web surface alone (#334)", () => {
  const { ASSET_CLASSES } = require(FORM);
  const holding = ASSET_CLASSES.filter((asset) => ids(list(["--asset", asset]).out).includes("vault.focal-crop"));
  assert.deepEqual(holding.sort(), ["brand-art", "web-surface"]);
});

test("list gives the critics the ruled-palette and plain-headline questions for brand art alone (#344)", () => {
  const { ASSET_CLASSES } = require(FORM);
  const listed = ASSET_CLASSES.map((asset) => [asset, ids(list(["--asset", asset, "--look"]).out)]);
  for (const id of ["vault.render-palette-look", "vault.headline-plain-look"]) {
    assert.deepEqual(listed.filter(([, held]) => held.includes(id)).map(([asset]) => asset), ["brand-art"], id);
  }
});

test("list matches an and-joined condition only when every term holds, and an or-joined one when any does", () => {
  const listed = (...args) => ids(list(args, FIXTURE_GATES).out);
  assert.ok(!listed("--asset", "web-surface").includes("vault.cta-look"));
  assert.ok(listed("--asset", "web-surface", "--fact", "has-cta").includes("vault.cta-look"));
  assert.ok(!listed("--asset", "print").includes("vault.mark"));
  assert.ok(listed("--asset", "brand-art").includes("vault.mark"));
  assert.ok(listed("--asset", "print", "--fact", "has-traced-mark").includes("vault.mark"));
  assert.ok(listed("--asset", "web-surface", "--fact", "has-payment-control").includes("demo.pay"));
});

test("list numbers the look questions first, then the script and code ones, each in file order", () => {
  const { out } = list(["--asset", "web-surface", "--fact", "has-cta"], FIXTURE_GATES);
  assert.deepEqual(ids(out), [
    "vault.spacing", "vault.cta-look", "demo.contrast", "demo.tone-a", "demo.tone-b",
    "vault.contrast", "vault.target", "vault.law-grid", "vault.house-grid", "vault.house-grid-b", "vault.ranked", "vault.motto", "vault.filters", "vault.law-filters", "vault.labels", "vault.filters-house", "vault.sort",
    "demo.spacing", "demo.voice-a", "demo.voice-b", "demo.target", "demo.focus-a", "demo.focus-b", "demo.caption", "demo.unread", "demo.six", "demo.filters", "demo.labels", "demo.sort", "demo.law-sort",
  ]);
  assert.match(out, /^1\. vault\.spacing: Does vault\.spacing hold\?\n {3}Applies to: every gap$/m);
  assert.match(out, /^6\. vault\.contrast \(script\): /m);
  assert.match(out, /^21\. demo\.target \(code\): /m);
  const look = out.slice(out.indexOf("Look questions"), out.indexOf("Script and code questions"));
  assert.deepEqual(ids(look), ids(out).slice(0, 5));
});

test("a part condition is printed whole, a `; ` inside it included", () => {
  assert.match(list(["--asset", "web-surface"], FIXTURE_GATES).out, /demo\.caption \(code\): Does demo\.caption hold\?\n {3}Applies to: the hero; and its caption$/m);
});

test("--look prints the look questions alone, numbered as in the whole list", () => {
  const args = ["--asset", "web-surface", "--fact", "has-cta"];
  const whole = list(args, FIXTURE_GATES).out;
  const { status, out } = list(["--look", ...args], FIXTURE_GATES);
  assert.equal(status, 0, out);
  assert.equal(out, `${whole.slice(0, whole.indexOf("\n\nScript and code questions")).replace(/30 question/, "5 question")}\n`);
  assert.doesNotMatch(out, /Script and code|Clashes|vault\.contrast/);
});

test("two calls on the same inputs give the same list, numbering included", () => {
  const args = ["--asset", "web-surface", "--fact", "has-cta", "--fact", "has-motion"];
  const first = list(args, [VAULT_GATE, path.join(FIXTURES, "list-project.md")]);
  assert.equal(first.status, 0, first.out + first.err);
  assert.equal(list(args, [VAULT_GATE, path.join(FIXTURES, "list-project.md")]).out, first.out);
});

test("a vault question that is not law or WCAG gives way to the project's", () => {
  assert.equal(clash(fixtureClashes(), "vault.spacing", "demo.spacing"),
    "- Settled by precedence (the project beats every vault question but law and WCAG, and domain evidence only on evidence of its own): N. vault.spacing and N. demo.spacing both write spacing and neither yields to the other; demo.spacing stands.");
});

test("a project question that departs from a vault question on domain evidence goes to the founder, unless the vault's gives way or the project's rests on evidence too", () => {
  const lines = fixtureClashes();
  assert.equal(clash(lines, "vault.filters", "demo.filters"),
    "- For the founder (the project's rule departs from domain evidence, and stands only on evidence of its own): N. vault.filters and N. demo.filters both write filters and neither yields to the other.");
  assert.ok(!lines.some((l) => l.includes("labels")), lines.join("\n"));
  for (const other of ["vault.filters", "demo.filters"]) {
    assert.match(clash(lines, other, "vault.law-filters"), /^- Settled by precedence \(law and WCAG beat every other rule\): .*; vault\.law-filters stands\.$/);
  }
  assert.match(clash(lines, "vault.sort", "demo.sort"), /^- Settled by precedence \(the project beats .*\): .*; demo\.sort stands\.$/);
  assert.match(clash(lines, "vault.sort", "demo.law-sort"), /^- Settled by precedence \(law and WCAG beat every other rule\): .*; demo\.law-sort stands\.$/);
});

test("a law or WCAG vault question stands against the project's, and against another vault question", () => {
  const lines = fixtureClashes();
  assert.equal(clash(lines, "demo.contrast", "vault.contrast"),
    "- Settled by precedence (law and WCAG beat every other rule): N. demo.contrast and N. vault.contrast both write contrast and neither yields to the other; vault.contrast stands.");
  assert.match(clash(lines, "vault.law-grid", "vault.house-grid"), /^- Settled by precedence \(law and WCAG beat every other rule\): .*; vault\.law-grid stands\.$/);
});

test("the sweep's reflow question stands at level 1, against the project, and its first-screen question below level 2 (#218)", () => {
  const lines = clashLines(list(["--asset", "web-surface", "--fact", "has-cta"], [VAULT_GATE, path.join(FIXTURES, "layout-rivals.md")]).out);
  assert.equal(clash(lines, "vault.reflow", "demo.reflow"),
    "- Settled by precedence (law and WCAG beat every other rule): N. vault.reflow and N. demo.reflow both write reflow and neither yields to the other; vault.reflow stands.");
  // The rival yields to every level and vault.layout to level 2, so the project stands only over a vault question below it.
  assert.equal(clash(lines, "vault.layout", "demo.first-screen"),
    "- Settled by precedence (the project beats every vault question but law and WCAG, and domain evidence only on evidence of its own): N. vault.layout and N. demo.first-screen both write first screen and each yields to the other; demo.first-screen stands.");
});

test("two of one project's questions that clash go to the founder, whether neither yields or each does, or one is law", () => {
  const lines = fixtureClashes();
  assert.equal(clash(lines, "demo.tone-a", "demo.tone-b"), "- For the founder (both are demo's own): N. demo.tone-a and N. demo.tone-b both write tone and neither yields to the other.");
  assert.equal(clash(lines, "demo.voice-a", "demo.voice-b"), "- For the founder (both are demo's own): N. demo.voice-a and N. demo.voice-b both write voice and each yields to the other.");
  assert.equal(clash(lines, "demo.focus-a", "demo.focus-b"), "- For the founder (both are demo's own): N. demo.focus-a and N. demo.focus-b both write focus and neither yields to the other.");
});

test("a vault question and a project's that stand at one level go to the founder", () => {
  assert.equal(clash(fixtureClashes(), "vault.target", "demo.target"),
    "- For the founder (both at one precedence level): N. vault.target and N. demo.target both write target and neither yields to the other.");
});

test("two vault questions below law go to the founder, as the rule records do not rank them, one on domain evidence included", () => {
  const lines = fixtureClashes();
  assert.equal(clash(lines, "vault.house-grid", "vault.house-grid-b"),
    "- For the founder (both are vault questions below law, which the rule records do not rank): N. vault.house-grid and N. vault.house-grid-b both write grid and neither yields to the other.");
  assert.match(clash(lines, "vault.filters", "vault.filters-house"), /^- For the founder \(both are vault questions below law, which the rule records do not rank\): /);
});

test("a yield to level 3 to 5 against a vault question goes to the founder, and level 6 yields to every level", () => {
  const lines = fixtureClashes();
  assert.equal(clash(lines, "vault.ranked", "demo.unread"),
    "- For the founder (it turns on a vault level the rule records do not record): N. vault.ranked and N. demo.unread both write rank and whether one yields to the other is not read.");
  assert.ok(!lines.some((l) => l.includes("motto")), lines.join("\n"));
});

test("the fixtures' clashes are those, and no more", () => {
  assert.equal(fixtureClashes().length, 19, fixtureClashes().join("\n"));
});

test("a clash is reported only where both questions apply to the asset", () => {
  const lines = clashLines(list(["--asset", "brand-art"], FIXTURE_GATES).out);
  assert.ok(!lines.some((l) => l.includes("demo.tone-b") || l.includes("spacing")), lines.join("\n"));
});

test("the vault's own gate holds no clash for any asset", () => {
  const { ASSET_CLASSES, ASSET_FACTS } = require(FORM);
  for (const asset of ASSET_CLASSES) {
    const { status, out } = list(["--asset", asset, ...ASSET_FACTS.flatMap((f) => ["--fact", f])]);
    assert.equal(status, 0, out);
    assert.match(out, /Clashes, for the reveal:\n\nNone\.$/m, `${asset}:\n${out}`);
  }
});

test("list leaves out a staged record and every record the whole-page critic, the type critic or the builder answers", () => {
  const { out } = list(["--asset", "web-surface"], [path.join(FIXTURES, "record-clean.md")]);
  assert.deepEqual(ids(out), ["vault.edge-look", "vault.edge-script"]);
});

test("list refuses a malformed gate file with check's faults and exit 1", () => {
  const { status, out } = list(["--asset", "web-surface"], [VAULT_GATE, path.join(FIXTURES, "bad-era.md")]);
  assert.equal(status, 1);
  assert.match(out, /bad-era\.md:9: demo\.era has an era that is neither/);
  assert.doesNotMatch(out, /Gate list/);
});

test("list refuses bad usage with exit 2, saying why on stderr", () => {
  const refusals = [
    [["--asset", "web-surface"], [], /list takes the vault's gate and at most one project's, not 0 paths/],
    [["--asset", "web-surface"], [VAULT_GATE, VAULT_GATE, VAULT_GATE], /list takes the vault's gate and at most one project's, not 3 paths/],
    [[], [VAULT_GATE], /--asset is missing/],
    [["--asset", "page"], [VAULT_GATE], /--asset is page, not one of web-surface/],
    [["--asset", "web-surface", "--fact", "has-video"], [VAULT_GATE], /--fact has-video is not one of has-motion/],
    [["--asset", "motion"], [VAULT_GATE], /a motion asset needs --fact has-motion too/],
    [["--asset", "web-surface", "--fact", "has-motion-over-5s"], [VAULT_GATE], /has-motion-over-5s needs --fact has-motion too/],
    [["--asset", "web-surface", "--fact", "has-brand-motion"], [VAULT_GATE], /has-brand-motion needs --fact has-motion too/],
    [["--asset", "motion", "--fact", "has-motion"], [VAULT_GATE], /a motion asset needs --fact has-brand-motion too/],
    [["--asset", "web-surface", "--colour", "red"], [VAULT_GATE], /Unknown option '--colour'/],
  ];
  for (const [args, files, why] of refusals) {
    const r = list(args, files);
    assert.equal(r.status, 2, args.join(" "));
    assert.match(r.err, why);
    assert.match(r.err, /usage: node gate\.js check /);
  }
});
