"use strict";

const FIELDS = ["applies-when", "question", "answered-by", "writes", "yields-to", "source", "era", "owner"];
const RECORD_FIELDS = ["stage", "target", "inputs", "output", "script", "parts", "reasons", "ledger", "status"];
const RECORD_REQUIRED = ["stage", "reasons", "ledger", "status"];
const ALL_FIELDS = [...FIELDS, ...RECORD_FIELDS];
const ANSWERERS = ["script", "code", "look", "whole-page", "type", "builder"];
// #121
const STAGES = ["function", "role", "treatment", "value"];
const BUILDER_RECORD_STAGES = ["function", "role", "treatment"];

const isBuilderLoaded = (q) => q.fields["answered-by"]?.value === "builder" || BUILDER_RECORD_STAGES.includes(q.fields.stage?.value);
const STATUSES = ["live", "staged"];
const OWED = "owed";
const GATE_ANSWERERS = ["script", "code", "look"];
const MAPPED_PARTS = ["link", "button", "textbox", "combobox", "checkbox", "radio", "switch", "slider", "tab", "menuitem", "option", "iframe"];
const PARTS = [...MAPPED_PARTS, "hero", "card", "image", "icon", "logo", "form", "nav", "dialog", "toast", "bottom-sheet", "table", "chart", "video", "badge", "testimonial", "primary-action", "destructive-action", "secondary-text", "tag", "list-header", "service-bar", "brand-bar", "user-name", "misspelling", "pixel-image", "cookie-banner", "carousel", "map", "drag-item", "pull-to-refresh", "resizable-sheet", "motion-control", "offer-deadline", "editable-value", "zoomable", "select-all", "empty-state", "category-tile"];
const LEDGER_KEY = /^[A-Z][A-Z0-9]*(-[A-Z0-9]+)+$/;
const ASSET_CLASSES = ["web-surface", "brand-art", "motion", "identity", "print", "social"];
const ASSET_FACTS = ["has-motion", "has-motion-over-5s", "has-brand-motion", "has-cta", "has-payment-control", "has-traced-mark"];
const ASSET_TERMS = [...ASSET_CLASSES, ...ASSET_FACTS];
const LEVELS = 6;

const HEADING = /^(#{1,6})\s+(.*?)\s*$/;
const FIELD = /^- ([\w-]+):\s*(.*?)\s*$/;

function parseGate(text) {
  const questions = [];
  const faults = [];
  let current = null;
  text.split("\n").forEach((raw, i) => {
    const line = i + 1;
    const heading = raw.match(HEADING);
    if (heading) {
      current = heading[1] === "###" ? { id: heading[2], line, fields: {} } : null;
      if (current) questions.push(current);
      return;
    }
    if (!current || raw.trim() === "") return;
    const field = raw.match(FIELD);
    if (!field) return faults.push({ line, message: `${current.id} holds a line that is not a \`- <field>: <value>\` field` });
    const [, name, value] = field;
    if (!ALL_FIELDS.includes(name)) faults.push({ line, message: `${current.id} has a field the form does not: ${name} (the fields are ${ALL_FIELDS.join(", ")})` });
    else if (current.fields[name]) faults.push({ line, message: `${current.id} gives ${name} twice` });
    else current.fields[name] = { value, line };
  });
  return { questions, faults };
}

function splitAppliesWhen(value) {
  const cut = value.indexOf("; ");
  return cut < 0 ? { condition: value.trim(), part: "" } : { condition: value.slice(0, cut).trim(), part: value.slice(cut + 2).trim() };
}

function appliesWhenFault(value) {
  const { condition, part } = splitAppliesWhen(value);
  if (!part) return "gives no part condition after its asset condition and `; `";
  if (condition === "any") return null;
  const joiners = [" and ", " or "].filter((j) => condition.includes(j));
  if (joiners.length > 1) return `joins its asset condition with both \`and\` and \`or\`: ${condition}`;
  const unknown = (joiners.length ? condition.split(joiners[0]) : [condition]).map((t) => t.trim()).filter((t) => !ASSET_TERMS.includes(t));
  return unknown.length ? `names an asset condition outside the vocabulary: ${unknown.join(", ")} (it is any, or ${ASSET_TERMS.join(", ")})` : null;
}

function eraFault(value) {
  if (value === "timeless") return null;
  const dated = value.match(/^dated (\d{4})-(\d{2})-(\d{2})$/);
  if (dated) {
    const [y, m, d] = dated.slice(1).map(Number);
    const date = new Date(Date.UTC(y, m - 1, d));
    if (date.getUTCFullYear() === y && date.getUTCMonth() === m - 1 && date.getUTCDate() === d) return null;
  }
  return `has an era that is neither \`timeless\` nor \`dated <YYYY-MM-DD>\`: ${value}`;
}

function recordFaults(q) {
  const f = q.fields;
  const value = (name) => f[name]?.value;
  const out = [];
  const isVault = value("owner") === "vault";
  if (isVault) for (const name of RECORD_REQUIRED) if (!value(name)) out.push([`is a vault rule record missing its ${name}`, q.line]);
  const answerer = value("answered-by");
  if (value("stage") && !STAGES.includes(value("stage"))) out.push([`has a stage that is not one of ${STAGES.join(", ")}: ${value("stage")}`, f.stage.line]);
  if (value("status") && !STATUSES.includes(value("status"))) out.push([`has a status that is not one of ${STATUSES.join(", ")}: ${value("status")}`, f.status.line]);
  if (answerer === "script" && isVault && !value("script")) out.push([`is answered by script but names no script (the script and its mode, or \`${OWED}\`)`, q.line]);
  if (value("script") && answerer && answerer !== "script") out.push([`gives \`script: ${value("script")}\` but is answered by ${answerer}: only a record answered by script names one`, f.script.line]);
  const loaded = isBuilderLoaded(q);
  if (loaded && !value("target")) out.push([`is loaded by the builder (${answerer === "builder" ? "answered by builder" : `stage ${value("stage")}`}) but gives no target`, q.line]);
  const isLoadJudgeable = value("stage") ? STAGES.includes(value("stage")) : !isVault;
  if (!loaded && isLoadJudgeable && value("target")) out.push([`gives a target no reader prints (${value("stage") ? `stage ${value("stage")}` : "no stage"}, answered by ${answerer ?? "nobody"}): only a record at ${BUILDER_RECORD_STAGES.join(", ")}, or answered by builder, gives one`, f.target.line]);
  if (value("parts")) {
    const unknown = value("parts").split(",").map((p) => p.trim()).filter((p) => !PARTS.includes(p));
    if (value("stage") !== "treatment") out.push([`names parts at stage ${value("stage") ?? "none"}: only a treatment record is chosen by the candidate's parts`, f.parts.line]);
    else if (unknown.length) out.push([`names a part outside the vocabulary: ${unknown.join(", ")} (the parts are ${PARTS.join(", ")})`, f.parts.line]);
  }
  if (Boolean(value("inputs")) !== Boolean(value("output"))) out.push([`gives ${value("inputs") ? "inputs with no output" : "an output with no inputs"}: a value several factors combine into names both`, (f.inputs ?? f.output).line]);
  if (value("ledger") && value("ledger") !== "none") {
    const bad = value("ledger").split(",").map((k) => k.trim()).filter((k) => !LEDGER_KEY.test(k));
    if (bad.length) out.push([`names a ledger entry that is no row key (or \`none\`): ${bad.join(", ")}`, f.ledger.line]);
  }
  return out;
}

function checkGates(files) {
  const faults = [];
  const parsed = files.map(({ file, text }) => ({ file, ...parseGate(text) }));
  const firstSeen = new Map();
  for (const { file, questions, faults: unread } of parsed) {
    faults.push(...unread.map((f) => ({ file, ...f })));
    if (questions.length === 0) faults.push({ file, line: 1, message: "holds no gate question (a `### <id>` heading)" });
    for (const q of questions) {
      const seen = firstSeen.get(q.id);
      if (seen) faults.push({ file, line: q.line, message: `${q.id} is already the id of a question at ${seen.file}:${seen.line}` });
      else firstSeen.set(q.id, { file, line: q.line });
    }
  }
  for (const { file, questions } of parsed) {
    for (const q of questions) {
      const fault = (message, at = q.line) => faults.push({ file, line: at, message: `${q.id} ${message}` });
      for (const name of FIELDS) if (!q.fields[name]?.value) fault(`is missing its ${name}`);
      const { "applies-when": appliesWhen, "answered-by": answeredBy, era, owner, source, "yields-to": yieldsTo } = q.fields;
      if (appliesWhen?.value) {
        const why = appliesWhenFault(appliesWhen.value);
        if (why) fault(why, appliesWhen.line);
      }
      if (answeredBy?.value && !ANSWERERS.includes(answeredBy.value)) fault(`is answered by ${answeredBy.value}, not one of ${ANSWERERS.join(", ")}`, answeredBy.line);
      if (era?.value) {
        const why = eraFault(era.value);
        if (why) fault(why, era.line);
      }
      if (source?.value && !/; strength: \S/.test(source.value)) fault("gives its source no `; strength: `", source.line);
      if (owner?.value && !(q.id.startsWith(`${owner.value}.`) && q.id.length > owner.value.length + 1)) fault(`is not prefixed by its owner, \`${owner.value}.\``);
      for (const [message, at] of recordFaults(q)) fault(message, at);
      if (yieldsTo?.value) {
        for (const t of yieldsTo.value.split(",").map((s) => s.trim())) {
          if (t === "none" || firstSeen.has(t)) continue;
          const level = t.match(/^level (\d+)$/);
          if (level && +level[1] >= 1 && +level[1] <= LEVELS) continue;
          fault(`yields to ${t || "an empty entry"}, which is no question id in the files given and no precedence level (level 1 to level ${LEVELS})`, yieldsTo.line);
        }
      }
    }
  }
  return { faults, count: parsed.reduce((n, { questions }) => n + questions.length, 0) };
}

const isGateQuestion = (q, staged = false) => (staged || q.fields.status?.value !== "staged") && GATE_ANSWERERS.includes(q.fields["answered-by"].value);

function applies(appliesWhen, asset, facts) {
  const { condition } = splitAppliesWhen(appliesWhen);
  if (condition === "any") return true;
  const holds = (term) => term === asset || facts.includes(term);
  if (condition.includes(" or ")) return condition.split(" or ").some((t) => holds(t.trim()));
  return condition.split(" and ").every((t) => holds(t.trim()));
}

module.exports = { ASSET_CLASSES, ASSET_FACTS, LEVELS, STAGES, OWED, MAPPED_PARTS, PARTS, isBuilderLoaded, parseGate, splitAppliesWhen, checkGates, applies, isGateQuestion };
