#!/usr/bin/env node
/**
 * Usage:
 *   node client.js <rules file>
 *
 * Reads a project's rules file for its `Client:` line. The first line whose label is `Client:` counts, bulleted or bold or neither
 * (`- **Client:** Mark M Moseley`, `**Client**: Mark`). Where it names someone
 * other than the founder it prints `outside: run the client steps for <name>`.
 * Where it reads "the founder" (alone, or before a comma or "for himself"), or
 * the file has no such line, it prints
 * `founder: skip the client steps (<why>)`. Exits 0 either way, and 2 on a file
 * it cannot read or an empty `Client:` line.
 */
"use strict";
const fs = require("node:fs");

const CLIENT_LINE = /^[ \t]*(?:[-*][ \t]+)?(?:\*\*)?Client(?::\*\*|\*\*:|:)[ \t]*(.*?)[ \t]*$/m;
const FOUNDER = /^(?:the\s+)?founder(?:$|[,.;]|\s+for himself)/i;

function main(args) {
  if (args.length !== 1) {
    process.stderr.write("usage: node client.js <rules file>\n");
    return 2;
  }
  const [file] = args;
  let text;
  try {
    text = fs.readFileSync(file, "utf8");
  } catch (err) {
    process.stderr.write(`client.js: cannot read ${file}: ${err.message}\n`);
    return 2;
  }
  const match = text.match(CLIENT_LINE);
  const founder = (why) => process.stdout.write(`founder: skip the client steps (${why})\n`);
  if (!match) {
    founder("no Client: line");
  } else if (!match[1]) {
    process.stderr.write(
      `client.js: ${file} has an empty Client: line; name the client, or write "Client: the founder, for himself"\n`,
    );
    return 2;
  } else if (FOUNDER.test(match[1])) {
    founder(`Client: ${match[1]}`);
  } else {
    process.stdout.write(`outside: run the client steps for ${match[1]}\n`);
  }
  return 0;
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));
