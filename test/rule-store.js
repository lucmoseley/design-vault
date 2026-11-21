"use strict";
// Test support for the suites that read the vault's store of rule records (#265): where it is, how many records it
// holds, and its records read the way gate.js reads a directory, every .md file in name order.
// node --test with no arguments also loads this file as a test file of no tests, which is harmless.
const fs = require("node:fs");
const path = require("node:path");
const { parseGate } = require("../plugin/skills/design-round/scripts/gate-form.js");

const STORE = path.join(__dirname, "..", "plugin", "skills", "design-critique", "rules");
// The 28 questions gate.md held at #265, the 78 #272 split out of the house references, #328's vault.render-size,
// #327's vault.baked-ui-look, #270's two House DNA clash records, #331's vault.contacts-script, the 15 staged
// records #278 filled, the eight #282 filled, the 48 #275 filled, the 11 #280 filled, the 28 #277 filled, the 56 #276
// filled, the 18 #279 filled, the 14 #281 filled, the 15 #285 filled, the 16 #283 filled, the eight #288 filled, the
// seven #286 filled, the seven #287 filled, the 16 #284 filled, the 19 #291 filled and the four #289
// filled, the two #306's splits added, #330's two logo records, #307's eight splits of the markup records,
// #305's reveal record, #309's 22 splits of the computed-style records, #313's three splits, #311's vault.bar-fit
// and vault.pane-split, #310's 14 DOM records, #314's five splits of the text records, #312's four state
// records, six look halves and the builder half of vault.drag-tracking, #316's vault.chart-carried, #333's
// vault.fall-script, #315's focus-colour split, #332's vault.render-checkerboard, #334's
// vault.focal-crop, #336's vault.clip-loop, #341's vault.contacts-seam, #344's two look records and #318's
// vault.motion-frequency-look and vault.drag-release-spring-look; a record added or removed changes it on purpose.
const RECORD_COUNT = 482;

const storeRecords = () =>
  fs.readdirSync(STORE).filter((n) => n.endsWith(".md")).sort().flatMap((n) => parseGate(fs.readFileSync(path.join(STORE, n), "utf8")).questions);

module.exports = { STORE, RECORD_COUNT, storeRecords };
