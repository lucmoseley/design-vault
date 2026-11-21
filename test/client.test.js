"use strict";
// client.js, which reads the rules file's `Client:` line, the switch for design-round's client-only steps (#114):
// driven through its CLI on three fixture rules files and on one-line files written per test. Loosen it and a project
// the founder designs for himself gets client questions, or a client is shown a round no one screened.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { test } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const ROOT = path.join(__dirname, "..");
const SCRIPT = path.join(ROOT, "plugin", "skills", "design-round", "scripts", "client.js");
const FIXTURES = path.join(__dirname, "fixtures", "client");

const client = (file) => {
  const r = runInProcess(SCRIPT, [file]);
  return { status: r.status, out: r.stdout, err: r.stderr };
};
// client.js run on a throwaway rules file holding `text`.
const clientOn = (text) => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "client-"));
  const file = path.join(dir, "brand-sheet.md");
  fs.writeFileSync(file, text);
  try {
    return { ...client(file), file };
  } finally {
    fs.rmSync(dir, { recursive: true });
  }
};

test("a rules file with no Client: line skips the client steps", () => {
  const r = client(path.join(FIXTURES, "no-line.md"));
  assert.equal(r.status, 0, r.err);
  assert.match(r.out, /^founder: skip the client steps \(no Client: line\)\n$/);
});

test("a Client: line naming the founder skips the client steps", () => {
  const r = client(path.join(FIXTURES, "founder.md"));
  assert.equal(r.status, 0, r.err);
  assert.match(r.out, /^founder: skip the client steps \(Client: the founder, for himself\)\n$/);
});

test("a Client: line naming someone else runs them, bold and bulleted as mmm-infra writes it", () => {
  const r = client(path.join(FIXTURES, "outside.md"));
  assert.equal(r.status, 0, r.err);
  assert.equal(r.out, "outside: run the client steps for Mark M Moseley, trading as MMM Infra.\n");
});

test("a missing rules file is refused, never read as the founder's", () => {
  const r = client(path.join(FIXTURES, "absent.md"));
  assert.equal(r.status, 2);
  assert.equal(r.out, "");
  assert.match(r.err, /absent\.md/);
});

test("an empty Client: line is refused with exit 2, naming the file and the line to write", () => {
  const r = clientOn("## §1 Who it is for\n\n- **Client:**\n- **Audience:** anyone\n");
  assert.equal(r.status, 2);
  assert.equal(r.out, "");
  assert.ok(r.err.includes(r.file), r.err);
  assert.match(r.err, /empty Client: line; name the client, or write "Client: the founder, for himself"/);
});

test("the founder without 'the' skips them, but a name that only starts with 'the founder' runs them", () => {
  assert.match(clientOn("Client: Founder, for himself\n").out, /^founder: /);
  assert.match(clientOn("Client: the founder\n").out, /^founder: /);
  assert.equal(clientOn("Client: the founder's sister, Ana\n").out, "outside: run the client steps for the founder's sister, Ana\n");
});

test("a bold label with its colon outside the bold is read as one too", () => {
  assert.equal(clientOn("- **Client**: Mark\n").out, "outside: run the client steps for Mark\n");
});

test("design-round runs it, and set-up writes the line it reads", () => {
  const skill = (name) => fs.readFileSync(path.join(ROOT, "plugin", "skills", name, "SKILL.md"), "utf8");
  const has = (name, text) => assert.ok(skill(name).includes(text), `${name}/SKILL.md lacks: ${text}`);
  has("design-round", "skills/design-round/scripts/client.js <the project's rules file>");
  has("design-project", "Who is the client: you, designing for yourself, or someone else?");
  has("design-project", "`Client: the founder, for himself`");
});
