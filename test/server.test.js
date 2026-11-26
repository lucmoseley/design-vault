"use strict";
const assert = require("node:assert/strict");
const { after, before, test } = require("node:test");
const { spawn } = require("node:child_process");
const fs = require("node:fs");
const http = require("node:http");
const os = require("node:os");
const path = require("node:path");

const SECRET = "secret-the-server-must-never-send";
let scratch, server, port;

before(async () => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "vault-server-"));
  const vault = path.join(scratch, "vault");
  for (const dir of ["vault/.git", "vault/folder"]) fs.mkdirSync(path.join(scratch, dir), { recursive: true });
  for (const file of ["outside.txt", "vault/.env", "vault/.git/config"]) fs.writeFileSync(path.join(scratch, file), SECRET);
  fs.writeFileSync(path.join(vault, "page.txt"), "a page");
  fs.writeFileSync(path.join(vault, "folder/page.txt"), "a page");
  fs.copyFileSync(path.join(__dirname, "..", "server.py"), path.join(vault, "server.py"));
  server = spawn("python3", [path.join(vault, "server.py"), "--port", "0"], { stdio: ["ignore", "pipe", "pipe"] });
  port = await new Promise((resolve, reject) => {
    let said = "";
    server.on("error", reject);
    server.on("exit", code => reject(new Error(`server.py exited with ${code} before it was running: ${said}`)));
    server.stdout.on("data", chunk => { said += chunk; const at = said.match(/127\.0\.0\.1:(\d+)/); if (at) resolve(Number(at[1])); });
    server.stderr.on("data", chunk => { said += chunk; });
  });
});

after(() => {
  server?.kill();
  fs.rmSync(scratch, { recursive: true, force: true });
});

const request = (target, { method = "GET", host = "127.0.0.1" } = {}) => new Promise((resolve, reject) => {
  const req = http.request({ host, port, path: target, method }, res => {
    let body = "";
    res.on("data", chunk => { body += chunk; });
    res.on("end", () => resolve({ status: res.statusCode, body }));
  });
  req.on("error", reject);
  req.end();
});

test("a page in the vault is served", async () => {
  assert.deepEqual(await request("/page.txt"), { status: 200, body: "a page" });
});

test("/api/health answers", async () => {
  const res = await request("/api/health");
  assert.equal(res.status, 200);
  assert.deepEqual(JSON.parse(res.body), { status: "ok" });
});

test("a dot-file or dot-directory path is refused, however it is spelled (#84: percent-encoded)", async () => {
  for (const target of ["/.env", "/.git/config", "/.git/", "/%2eenv", "/%2Egit/config", "/folder/../.env"]) {
    for (const method of ["GET", "HEAD"]) {
      const res = await request(target, { method });
      assert.equal(res.status, 404, `${method} ${target}`);
      assert.ok(!res.body.includes(SECRET), `${method} ${target}`);
    }
  }
});

test("a directory gets no listing", async () => {
  for (const target of ["/", "/folder/"]) {
    const res = await request(target);
    assert.equal(res.status, 403, target);
    assert.ok(!res.body.includes("page.txt"), target);
  }
});

test("a path that climbs out of the vault serves nothing outside it", async () => {
  for (const target of ["/../outside.txt", "/folder/../../outside.txt", "/%2e%2e/outside.txt", "/%2E%2E%2Foutside.txt", "/..%2f..%2foutside.txt"]) {
    const res = await request(target);
    assert.ok(!res.body.includes(SECRET), target);
    assert.equal(res.status, 404, target);
  }
});

test("the server binds to 127.0.0.1 only", async () => {
  await assert.rejects(request("/page.txt", { host: "127.0.0.2" }), { code: "ECONNREFUSED" });
});
