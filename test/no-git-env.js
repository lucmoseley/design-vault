"use strict";
// #116
for (const k of Object.keys(process.env)) if (k.startsWith("GIT_")) delete process.env[k];
