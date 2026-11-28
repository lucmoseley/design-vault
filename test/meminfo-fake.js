"use strict";
const fs = require("node:fs");
const path = require("node:path");

const meminfoLine = (name, kb) => `${`${name}:`.padEnd(16)}${String(kb).padStart(8)} kB`;

function fakeMeminfo(dir, mb) {
  const file = path.join(dir, `meminfo-${mb}`);
  if (!fs.existsSync(file)) fs.writeFileSync(file, `${meminfoLine("MemTotal", 10162176)}\n${meminfoLine("MemAvailable", mb * 1024)}\n`);
  return file;
}

module.exports = { fakeMeminfo, meminfoLine };
