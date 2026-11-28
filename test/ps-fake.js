"use strict";
const fs = require("node:fs");
const path = require("node:path");

const psLines = (args) => args.map((a, i) => `${String(11 + i).padStart(7)} ${a}`).join("\n");

function fakePs(dir, name, args = [], { reads } = {}) {
  const file = path.join(dir, `ps-${name}`);
  const served = args.length ? `cat <<'EOF'\n${psLines(args)}\nEOF\n` : "";
  const count = `echo >>'${file}.reads'\n[ "$(wc -l <'${file}.reads')" -gt ${reads} ] && exit 0\n`;
  fs.writeFileSync(file, `#!/bin/sh\n${reads === undefined ? "" : count}${served}`, { mode: 0o755 });
  return file;
}

function realPsMatching(dir, name, fixed) {
  const file = path.join(dir, `ps-${name}`);
  fs.writeFileSync(file, `#!/bin/sh\nps "$@" | grep -F '${fixed}' || true\n`, { mode: 0o755 });
  return file;
}

module.exports = { fakePs, psLines, realPsMatching };
