// Hides the fallback its script replaces, so a blocked script leaves it shown.
// node --test loads every .js under test/, where there is no document.
globalThis.document?.addEventListener("DOMContentLoaded", () => {
  document.getElementById("fallback").hidden = true;
});
