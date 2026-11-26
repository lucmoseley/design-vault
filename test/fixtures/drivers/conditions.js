// https://nodejs.org/api/test.html#running-tests-from-the-command-line: node --test loads every .js under test/
globalThis.document?.addEventListener("DOMContentLoaded", () => {
  document.getElementById("fallback").hidden = true;
});
