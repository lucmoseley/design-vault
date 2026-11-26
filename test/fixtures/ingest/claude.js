"use strict";
const fs = require("node:fs");
const path = require("node:path");

function main() {
  const argv = process.argv.slice(2);
  const prompt = argv[argv.indexOf("-p") + 1];
  const model = argv[argv.indexOf("--model") + 1];
  const image = prompt.match(/^Read the image at this exact path: (.+)$/m)?.[1] ?? null;
  const galleryPath = path.join(process.cwd(), "data", "gallery.json");
  const record = {
    argv,
    model,
    prompt,
    image,
    imageExisted: image !== null && fs.existsSync(image),
    onDisk: JSON.parse(fs.readFileSync(galleryPath, "utf8")).entries.map((entry) => entry.id),
  };
  const log = process.env.FAKE_CLAUDE_CALLS;
  const call = fs.existsSync(log) ? fs.readFileSync(log, "utf8").split("\n").filter(Boolean).length : 0;
  fs.appendFileSync(log, `${JSON.stringify(record)}\n`);

  const answers = JSON.parse(fs.readFileSync(process.env.FAKE_CLAUDE_ANSWERS, "utf8"));
  const answer = answers[call] ?? answers.at(-1);
  if (answer.kill) process.kill(process.ppid, "SIGKILL");
  else if (answer.fail) {
    process.stderr.write(`${answer.fail}\n`);
    process.exitCode = 1;
  } else process.stdout.write(JSON.stringify({ structured_output: answer, total_cost_usd: 0.01, modelUsage: { [`claude-${model}-9`]: {} } }));
}

if (process.env.FAKE_CLAUDE_ANSWERS) main();
