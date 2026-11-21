"use strict";
// Required first by every test file that runs git, itself or through a script it runs (#125).
// A commit from a linked worktree hands its hook an absolute GIT_DIR, and a scratch `git init` under it
// re-initialises that repo as bare (#116); so no GIT_* for the file's own git calls, its scripts' or its
// in-process ones. node --test runs each file in its own process, so the deletion stays in the file that
// requires it, and a file that does not is still exposed when a hook runs it on its own.
// node --test with no arguments also loads this file as a test file of no tests, which is harmless.
for (const k of Object.keys(process.env)) if (k.startsWith("GIT_")) delete process.env[k];
