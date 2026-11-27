#!/usr/bin/env node
"use strict";
const fs = require("node:fs");
const { parseArgs } = require("node:util");
const path = require("node:path");
const { ASSET_CLASSES, ASSET_FACTS, LEVELS, STAGES, OWED, MAPPED_PARTS, PARTS, isBuilderLoaded, parseGate, splitAppliesWhen, checkGates, applies, isGateQuestion } = require("./gate-form.js");

const [LAW_LEVEL, PROJECT_LEVEL, EVIDENCE_LEVEL] = [1, 2, 3];
const CANNOT_MEASURE = "cannot measure";
const MEASURED = ["pass", "fail", CANNOT_MEASURE];
const LOOKED = ["yes", "no", "unsure"];
// #154
const CRITIC_COUNT = 3;
const PARTS_QUESTION = "vault.affordance";
const MINOR = /^minor:/i;
const OTHERS = "others";
// The most look questions one pass asks, as #225 measured recall.
const LOOK_LIMIT = 20;
const READERS = ["gate", "builder", "whole-page", "type", "script"];
const BUILDER_STAGES = ["direction", "build", "finish"];
const SETTLE_VERDICT = { yes: "pass", no: "fault", unsure: "founder" };
const OFF_KEY_VERDICT = { yes: "fault", no: "pass", unsure: "founder" };
const UNLISTED = "unlisted";

function ownLevel(q) {
  if (/^(law|WCAG)\b/.test(strength(q))) return LAW_LEVEL;
  if (q.fields.owner.value !== "vault") return PROJECT_LEVEL;
  return evidenced(q) ? EVIDENCE_LEVEL : null;
}

const strength = (q) => q.fields.source.value.split("; strength: ")[1];
const evidenced = (q) => /^domain evidence\b/.test(strength(q));

function yieldsTo(a, b) {
  const bLevel = ownLevel(b);
  let unread = false;
  for (const t of a.fields["yields-to"].value.split(",").map((s) => s.trim())) {
    if (t === b.id) return true;
    const level = +(t.match(/^level (\d+)$/)?.[1] ?? 0);
    if (!level) continue;
    if (bLevel === null ? level === LEVELS : bLevel <= level) return true;
    if (bLevel === null && level > 2) unread = true;
  }
  return unread ? null : false;
}

function clashes(questions) {
  const found = [];
  questions.forEach((a, i) => {
    for (const b of questions.slice(i + 1)) {
      if (a.fields.writes.value !== b.fields.writes.value) continue;
      const [ab, ba] = [yieldsTo(a, b), yieldsTo(b, a)];
      if (ab !== null && ba !== null && ab !== ba) continue;
      const yielding = ab === null || ba === null ? "unread" : ab ? "each" : "neither";
      const owner = a.fields.owner.value;
      const [la, lb] = [ownLevel(a) ?? Infinity, ownLevel(b) ?? Infinity];
      const [early, earlyYields, lateYields] = stageRank(a) < stageRank(b) ? [a, ab, ba] : [b, ba, ab];
      let reason;
      if (owner !== "vault" && owner === b.fields.owner.value) reason = "same-owner";
      else if (stageRank(a) !== stageRank(b) && hasStage(a) && hasStage(b) && (earlyYields === false || lateYields === true)) reason = "stage";
      else if (yielding === "unread") reason = "unread";
      else if (owner === "vault" && b.fields.owner.value === "vault" && Math.min(la, lb) > LAW_LEVEL) reason = "vault-levels";
      else if (la === lb) reason = "same-level";
      else if (Math.min(la, lb) === PROJECT_LEVEL && Math.max(la, lb) === EVIDENCE_LEVEL && !evidenced(la < lb ? a : b)) reason = "evidence";
      const winner = reason === "stage" ? early : reason ? null : la < lb ? a : b;
      found.push({ a, b, yielding, reason: reason ?? (ownLevel(winner) === LAW_LEVEL ? "law" : "project"), winner });
    }
  });
  return found;
}

const answererOf = (q) => q.fields["answered-by"].value;
const isScriptOwed = (q) => answererOf(q) === "script" && q.fields.script?.value === OWED;

const assetRecords = (files, asset, facts, staged) =>
  files
    .flatMap(({ file, text }) => parseGate(text).questions.map((q) => Object.assign(q, { area: path.basename(file, ".md") })))
    .filter((q) => staged || q.fields.status?.value !== "staged")
    .filter((q) => applies(q.fields["applies-when"].value, asset, facts));

function listGates(files, asset, facts, staged = false) {
  const kept = assetRecords(files, asset, facts, staged).filter((q) => isGateQuestion(q, staged));
  const look = kept.filter((q) => answererOf(q) === "look" || isScriptOwed(q));
  const answered = kept.filter((q) => !look.includes(q));
  const numbered = [...look, ...answered];
  numbered.forEach((q, i) => (q.n = i + 1));
  return { look, answered, clashes: clashes(numbered) };
}

const hasStage = (q) => STAGES.includes(q.fields.stage?.value);
const stageRank = (q) => (hasStage(q) ? STAGES.indexOf(q.fields.stage.value) : STAGES.length);
const coarseToFine = (records) => [...records].sort((a, b) => stageRank(a) - stageRank(b));

function pickRecords(records, reader, stage, partsPresent) {
  const atStage = (q, ...stages) => stages.includes(q.fields.stage?.value);
  const forParts = (q) => !q.fields.parts || q.fields.parts.value.split(",").some((p) => partsPresent.includes(p.trim()));
  const pick = {
    direction: (q) => atStage(q, "function", "role"),
    build: (q) => isBuilderLoaded(q) && (!atStage(q, "treatment") || forParts(q)),
    finish: (q) => answererOf(q) === "script",
  };
  const kept = reader === "builder" ? records.filter(pick[stage]) : records.filter((q) => answererOf(q) === reader);
  return coarseToFine(kept);
}

function parsePartsPresent(text) {
  let data;
  try {
    data = JSON.parse(text);
  } catch (err) {
    return { names: [], faults: [`is not JSON: ${err.message}`] };
  }
  if (!isObject(data) || !("parts" in data || "declared" in data)) return { names: [], faults: ["is neither a parts map, with a `parts` list, nor a parts declaration, with a `declared` object"] };
  const faults = [];
  const names = [];
  if ("parts" in data) {
    faults.push(...partsOf(data).faults);
    if (Array.isArray(data.parts)) names.push(...data.parts.map((p) => p?.role).filter((r) => MAPPED_PARTS.includes(r)));
  }
  if ("declared" in data && !isObject(data.declared)) faults.push("has a `declared` that is not an object of part names");
  for (const [name, selector] of Object.entries(isObject(data.declared) ? data.declared : {})) {
    if (!PARTS.includes(name)) faults.push(`declares ${name}, which is no part in the vocabulary (${PARTS.join(", ")})`);
    else if (!(selector === null || (typeof selector === "string" && selector.trim()))) faults.push(`declares ${name} with neither a CSS selector nor null`);
    else names.push(name);
  }
  return { names: [...new Set(names)], faults };
}

const isObject = (v) => typeof v === "object" && v !== null && !Array.isArray(v);

function readAnswer(a, vocabulary, what, candidate, faults) {
  const answer = typeof a?.answer === "string" ? a.answer.trim().toLowerCase() : null;
  const evidence = typeof a?.evidence === "string" ? a.evidence.trim() : "";
  if (!vocabulary.includes(answer)) faults.push(`answers ${what} for ${candidate} ${JSON.stringify(a?.answer ?? null)}, not one of ${vocabulary.join(", ")}`);
  else if (!evidence || evidence.includes("\n")) faults.push(`gives ${what} for ${candidate} no one line of evidence`);
  else return { answer, evidence };
  return null;
}

function readByPart(a, candidate, faults) {
  if (!isObject(a?.parts)) {
    faults.push(`answers ${PARTS_QUESTION} for ${candidate} whole, not part by part under \`parts\``);
    return null;
  }
  const before = faults.length;
  const parts = Object.fromEntries(Object.entries(a.parts).map(([id, p]) => [id, readAnswer(p, LOOKED, `${PARTS_QUESTION}'s part ${id}`, candidate, faults)]));
  const unlisted = a.unlisted ?? [];
  if (!Array.isArray(unlisted) || !unlisted.every((u) => typeof u === "string" && u.trim() && !u.includes("\n"))) {
    faults.push(`gives ${PARTS_QUESTION} for ${candidate} an \`unlisted\` that is not a list of one-line parts`);
  }
  return faults.length > before ? null : { parts, unlisted: unlisted.map((u) => u.trim()) };
}

function readSettledParts(a, candidate, faults) {
  if (!isObject(a) || !(isObject(a.parts) || UNLISTED in a) || ("parts" in a && !isObject(a.parts))) {
    faults.push(`settles ${PARTS_QUESTION} for ${candidate} with no \`parts\` object and no \`unlisted\` answer`);
    return null;
  }
  const before = faults.length;
  const parts = Object.fromEntries(Object.entries(a.parts ?? {}).map(([id, p]) => [id, readAnswer(p, LOOKED, `${PARTS_QUESTION}'s part ${id}`, candidate, faults)]));
  const unlisted = UNLISTED in a ? readAnswer(a.unlisted, LOOKED, `${PARTS_QUESTION}'s parts off the key`, candidate, faults) : null;
  return faults.length > before ? null : { parts, unlisted };
}

function parseParts(text) {
  try {
    return partsOf(JSON.parse(text));
  } catch (err) {
    return { parts: [], faults: [`is not JSON: ${err.message}`] };
  }
}

function partsOf(data) {
  if (!Array.isArray(data?.parts)) return { parts: [], faults: ["has no `parts` list"] };
  const faults = [];
  const seen = new Set();
  data.parts.forEach((p, i) => {
    if (typeof p?.id !== "string" || !p.id || typeof p.actable !== "boolean" || typeof p.text !== "string") faults.push(`part ${i + 1} has no id, no actable true or false, or no text`);
    else if (seen.has(p.id)) faults.push(`part ${i + 1} has the id ${p.id} again`);
    else if (!(p.dead == null || (typeof p.dead === "string" && p.dead.startsWith("#")))) faults.push(`part ${i + 1} has a \`dead\` that is neither null nor a link's target`);
    seen.add(p?.id);
  });
  if (faults.length) return { parts: [], faults };
  return { parts: data.parts.map((p) => ({ id: p.id, actable: p.actable, href: p.href || null, dead: p.dead ?? null, text: p.text })), faults };
}

function parseAnswers(text, kind) {
  const critic = kind === "critic";
  const byPart = { critic: readByPart, settle: readSettledParts }[kind];
  let data;
  try {
    data = JSON.parse(text);
  } catch (err) {
    return { answers: {}, clashes: [], faults: [`is not JSON: ${err.message}`] };
  }
  const faults = [];
  const vocabulary = kind === "measured" ? MEASURED : LOOKED;
  const answers = {};
  if (!isObject(data?.answers)) faults.push("has no `answers` object of candidates");
  else {
    for (const [candidate, given] of Object.entries(data.answers)) {
      if (!isObject(given)) {
        faults.push(`gives ${candidate} no object of answers`);
        continue;
      }
      answers[candidate] = {};
      for (const [id, a] of Object.entries(given)) {
        answers[candidate][id] = byPart && id === PARTS_QUESTION ? byPart(a, candidate, faults) : readAnswer(a, vocabulary, id, candidate, faults);
      }
    }
  }
  const clashes = [];
  if (critic && !Array.isArray(data?.clashes)) faults.push("has no `clashes` list, which is empty where the critic named none");
  else if (critic) {
    data.clashes.forEach((c, i) => {
      const quotes = Array.isArray(c?.quotes) ? c.quotes.filter((q) => typeof q === "string" && q.trim()).map((q) => q.trim()) : [];
      if (quotes.length !== 2 || c.quotes.length !== 2) faults.push(`clash ${i + 1} does not quote exactly two rules`);
      else if (c.candidate !== null && typeof c.candidate !== "string") faults.push(`clash ${i + 1} names its candidate by neither a name nor null`);
      else clashes.push({ candidate: c.candidate, quotes });
    });
  }
  return { answers, clashes, faults };
}

function answeredFaults({ answered }, answers) {
  const faults = [];
  const ids = new Set(answered.map((q) => q.id));
  if (Object.keys(answers).length === 0) faults.push("answers for no candidate");
  for (const [candidate, given] of Object.entries(answers)) {
    for (const id of Object.keys(given)) if (!ids.has(id)) faults.push(`answers ${id} for ${candidate}, which is no script or code question on the list`);
    for (const q of answered) if (!(q.id in given)) faults.push(`gives ${candidate} no answer to ${q.id}`);
  }
  return faults;
}

const PHASES = [
  { name: "function and role", holds: (q) => stageRank(q) < STAGES.indexOf("treatment") || !hasStage(q) },
  { name: "treatment and value", holds: (q) => !PHASES[0].holds(q) },
];

function cutPasses(questions) {
  const areas = [...new Set(questions.map((q) => q.area))];
  const ordered = [...questions].sort((a, b) => stageRank(a) - stageRank(b) || areas.indexOf(a.area) - areas.indexOf(b.area));
  const inside = (j, key) => (j > 0 && key(ordered[j - 1]) === key(ordered[j]) ? 1 : 0);
  const stage = (q) => stageRank(q);
  const area = (q) => `${stageRank(q)} ${q.area}`;
  const best = [{ cost: [0, 0, 0, 0], from: null }];
  const cheaper = (a, b) => a.reduce((d, x, k) => d || x - b[k], 0);
  for (let i = 1; i <= ordered.length; i++) {
    for (let j = Math.max(0, i - LOOK_LIMIT); j < i; j++) {
      const [passes, stageCuts, areaCuts, squares] = best[j].cost;
      const cost = [passes + 1, stageCuts + inside(j, stage), areaCuts + inside(j, area), squares + (i - j) ** 2];
      if (!best[i] || cheaper(cost, best[i].cost) < 0) best[i] = { cost, from: j };
    }
  }
  const passes = [];
  for (let i = ordered.length; i > 0; i = best[i].from) passes.unshift(ordered.slice(best[i].from, i));
  return passes;
}

function lookPasses({ look, answered }, answers) {
  const unmeasured = new Map();
  for (const [candidate, given] of Object.entries(answers ?? {})) {
    for (const q of answered) if (given[q.id]?.answer === CANNOT_MEASURE) unmeasured.set(q, [...(unmeasured.get(q) ?? []), candidate]);
  }
  const looked = [...look, ...answered.filter((q) => unmeasured.has(q))];
  const passes = PHASES.flatMap((phase, i) => cutPasses(looked.filter(phase.holds)).map((questions) => ({ questions, phase: i })));
  return { looked, unmeasured, split: looked.length > LOOK_LIMIT, passes };
}

const inPass = (pass, q, measured) => !pass || pass.has(q.id) || (measured !== undefined && measured.answer !== CANNOT_MEASURE);

const lookedAt = (list, answers, candidate, pass) =>
  [...list.look, ...list.answered.filter((q) => answers[candidate][q.id].answer === CANNOT_MEASURE)].filter((q) => inPass(pass, q, answers[candidate][q.id]));

function criticFaults(list, answers, critic, maps, pass) {
  const faults = [];
  const candidates = Object.keys(answers);
  const known = new Set([...list.look, ...list.answered].map((q) => q.id));
  for (const candidate of Object.keys(critic.answers)) if (!candidates.includes(candidate)) faults.push(`answers for ${candidate}, which the building session's answers do not name`);
  for (const candidate of candidates) {
    const given = critic.answers[candidate];
    if (!given) {
      faults.push(`gives no answers for ${candidate}`);
      continue;
    }
    for (const id of Object.keys(given)) if (!known.has(id)) faults.push(`answers ${id} for ${candidate}, which is not on the list`);
    for (const q of lookedAt(list, answers, candidate, pass)) if (!(q.id in given)) faults.push(`gives ${candidate} no answer to ${q.id}`);
    const byPart = given[PARTS_QUESTION];
    if (!byPart || !maps[candidate]) continue;
    const ids = maps[candidate].map((p) => p.id);
    for (const id of Object.keys(byPart.parts)) if (!ids.includes(id)) faults.push(`answers ${PARTS_QUESTION}'s part ${id} for ${candidate}, which is not on its parts map`);
    for (const id of ids) if (!(id in byPart.parts)) faults.push(`gives ${candidate} no answer to ${PARTS_QUESTION}'s part ${id}`);
  }
  for (const { candidate } of critic.clashes) if (candidate !== null && !candidates.includes(candidate)) faults.push(`names a clash on ${candidate}, which the building session's answers do not name`);
  return faults;
}

function panelVerdict(looked) {
  const all = (answer) => looked.every((l) => l.answer === answer);
  return all("yes") ? "pass" : all("no") ? "fault" : "split";
}

const settleKey = (...at) => at.join("\u0000");

function lookVerdict(looked, settled) {
  const panel = panelVerdict(looked);
  return { verdict: settled ? SETTLE_VERDICT[settled.answer] : panel, panel, settled };
}

function verdictOf(q, measured, look, settled) {
  if (measured && measured.answer !== CANNOT_MEASURE) return { q, verdict: measured.answer === "pass" ? "pass" : "fault", measured };
  const looked = look();
  return { q, ...lookVerdict(looked, settled), measured, looked };
}

function tallyGates(list, answers, critics, maps, settled, pass) {
  return Object.keys(answers).map((candidate) => {
    const rows = [...list.look, ...list.answered].filter((q) => inPass(pass, q, answers[candidate][q.id])).map((q) =>
      q.id === PARTS_QUESTION
        ? affordanceRow(q, candidate, critics, maps[candidate], settled)
        : verdictOf(q, answers[candidate][q.id], () => critics.map(({ name, answers: given }) => ({ name, ...given[candidate][q.id] })), settled.get(settleKey(candidate, q.id))),
    );
    return { candidate, rows };
  });
}

function affordanceRow(q, candidate, critics, map, settled) {
  const parts = map.map((p) => {
    const looked = critics.map(({ name, answers: given }) => ({ name, ...given[candidate][q.id].parts[p.id] }));
    const { verdict, panel, settled: settle } = lookVerdict(looked, settled.get(settleKey(candidate, q.id, p.id)));
    const looks = { pass: true, fault: false }[verdict] ?? null;
    const cell = p.dead ? "dead" : looks === null ? verdict : looks === p.actable ? "pass" : p.actable ? "hidden" : "false";
    return { p, looked, looks, panel, settled: settle, cell };
  });
  for (const r of parts) {
    const twin = r.cell === "hidden" && r.p.href && parts.find((o) => o.p.href === r.p.href && o.cell === "pass" && o.p.actable);
    if (twin) Object.assign(r, { cell: "minor", twin: twin.p });
  }
  const unlisted = critics.flatMap(({ name, answers: given }) => given[candidate][q.id].unlisted.map((line) => ({ name, line })));
  const settle = settled.get(settleKey(candidate, q.id, UNLISTED));
  const offKey = unlisted.length ? { verdict: settle ? OFF_KEY_VERDICT[settle.answer] : "split", settled: settle } : null;
  const cells = new Set([...parts.map((r) => r.cell), offKey?.verdict === "fault" ? "false" : offKey?.verdict]);
  const verdict = ["hidden", "false", "dead"].some((c) => cells.has(c)) ? "fault" : ["split", "founder"].find((v) => cells.has(v)) ?? "pass";
  return { q, verdict, parts, unlisted, offKey };
}

function settleKeys(results, recheck) {
  const owed = new Map();
  const open = new Map();
  const add = (key, what, split) => (split ? [owed, open] : [open]).forEach((m) => m.set(key, what));
  for (const { candidate, rows, faults, others } of results) {
    if (recheck) {
      for (const f of faults) if (f.looked && !f.deadParts) add(settleKey(candidate, f.q.id), `${f.q.id} for ${candidate}`, f.panel === "split");
      add(settleKey(candidate, OTHERS), `${OTHERS} for ${candidate}`, others.panel === "split");
      continue;
    }
    for (const r of rows) {
      if (r.parts) {
        for (const { p, cell } of r.parts) if (cell === "split") add(settleKey(candidate, r.q.id, p.id), `${r.q.id}'s part ${p.id} for ${candidate}`, true);
        if (r.offKey) add(settleKey(candidate, r.q.id, UNLISTED), `${r.q.id}'s parts off the key for ${candidate}`, true);
      } else if (r.looked && r.panel !== "fault") add(settleKey(candidate, r.q.id), `${r.q.id} for ${candidate}`, r.panel === "split");
    }
  }
  return { owed, open: recheck ? owed : open };
}

function readSettles(files, results, recheck) {
  const { owed, open } = settleKeys(results, recheck);
  const settled = new Map();
  const faults = [];
  const fileSettle = (name, key, what, a) => {
    if (!open.has(key)) faults.push(`${name}: settles ${what}, which no three critics split on`);
    else if (settled.has(key)) faults.push(`${name}: settles ${open.get(key)}, which ${settled.get(key).name} settles too`);
    else settled.set(key, { name, ...a });
  };
  for (const { name, answers } of files) {
    for (const [candidate, given] of Object.entries(answers)) {
      for (const [id, a] of Object.entries(given)) {
        if (recheck || id !== PARTS_QUESTION) fileSettle(name, settleKey(candidate, id), `${id} for ${candidate}`, a);
        else {
          for (const [part, pa] of Object.entries(a.parts)) fileSettle(name, settleKey(candidate, id, part), `${id}'s part ${part} for ${candidate}`, pa);
          if (a.unlisted) fileSettle(name, settleKey(candidate, id, UNLISTED), `${id}'s parts off the key for ${candidate}`, a.unlisted);
        }
      }
    }
  }
  for (const [key, what] of owed) if (!settled.has(key)) faults.push(`no --settle file settles ${what}, which the critics split on`);
  return { settled, faults };
}

function parseFixed(values, list, answers) {
  const fixed = new Map();
  const faults = [];
  const known = new Set([...list.look, ...list.answered].map((q) => q.id));
  for (const value of values) {
    const cut = value.indexOf(":");
    const [candidate, id] = cut < 0 ? [value, ""] : [value.slice(0, cut), value.slice(cut + 1)];
    if (!(candidate in answers)) faults.push(`--fault ${value} names ${candidate || "no candidate"}, which the building session's answers do not name`);
    else if (!known.has(id)) faults.push(`--fault ${value} names ${id || "no question"}, which is not on the list`);
    else if (fixed.get(candidate)?.includes(id)) faults.push(`--fault ${value} is given twice`);
    else fixed.set(candidate, [...(fixed.get(candidate) ?? []), id]);
  }
  return { fixed, faults };
}

function recheckOwed(list, answers, candidate, ids) {
  const looks = new Set(list.look.map((q) => q.id));
  return [...ids.filter((id) => looks.has(id) || answers[candidate][id].answer === CANNOT_MEASURE), OTHERS];
}

function recheckCriticFaults(list, answers, fixed, critic) {
  const faults = [];
  for (const candidate of Object.keys(critic.answers)) if (!fixed.has(candidate)) faults.push(`answers for ${candidate}, which no --fault names`);
  for (const [candidate, ids] of fixed) {
    const given = critic.answers[candidate];
    if (!given) {
      faults.push(`gives no answers for ${candidate}`);
      continue;
    }
    const owed = recheckOwed(list, answers, candidate, ids);
    for (const id of Object.keys(given)) if (!owed.includes(id)) faults.push(`answers ${id} for ${candidate}, which its re-check does not ask`);
    for (const id of owed) if (!(id in given)) faults.push(`gives ${candidate} no answer to ${id}`);
  }
  return faults;
}

const STOPS = { 1: "the fix breaks another question", 2: "the same question fails again", 3: "the critics split and the settle critic is unsure" };

function recheckFaults(list, answers, before, fixed, critics, settled, maps) {
  const byId = new Map([...list.look, ...list.answered].map((q) => [q.id, q]));
  return [...fixed].map(([candidate, ids]) => {
    const lookedAt = (id) => critics.map(({ name, answers: given }) => ({ name, ...given[candidate][id] }));
    const othersLooked = lookedAt(OTHERS);
    const others = { ...lookVerdict(othersLooked, settled.get(settleKey(candidate, OTHERS))), looked: othersLooked };
    const broken = list.answered.filter((q) => before[candidate]?.[q.id]?.answer === "pass" && answers[candidate][q.id].answer === "fail");
    const newDead = byId.has(PARTS_QUESTION) && ids.some((id) => id !== PARTS_QUESTION) ? { q: byId.get(PARTS_QUESTION), parts: newlyDead(maps.before[candidate], maps.now[candidate]) } : null;
    const faults = ids.map((id) => {
      let fault = verdictOf(byId.get(id), answers[candidate][id], () => lookedAt(id), settled.get(settleKey(candidate, id)));
      const deadParts = id === PARTS_QUESTION ? maps.now[candidate].filter((p) => p.dead) : [];
      if (deadParts.length) fault = { ...fault, verdict: "fault", deadParts };
      const stops = [];
      if (others.verdict === "fault" || broken.length || (id !== PARTS_QUESTION && newDead?.parts.length)) stops.push(1);
      if (fault.verdict === "fault") stops.push(2);
      if (fault.verdict === "founder" || others.verdict === "founder") stops.push(3);
      return { ...fault, stops, unsettled: [fault.verdict, others.verdict].includes("split") };
    });
    return { candidate, faults, others, broken, newDead };
  });
}

function newlyDead(before, now) {
  const left = before.filter((p) => p.dead).map((p) => p.dead);
  return now.filter((p) => {
    const i = p.dead ? left.indexOf(p.dead) : -1;
    if (i >= 0) left.splice(i, 1);
    return p.dead && i < 0;
  });
}

const USAGE = `usage: node gate.js check <gate file> [<gate file> ...]
       node gate.js list --asset <class> [--fact <fact> ...] [--staged] [--reader gate] [--look] [--answered <file>] [--pass <n>]
                         <vault gate> [<project gate>]
       node gate.js list --asset <class> [--fact <fact> ...] [--staged] --reader builder --stage direction|finish <vault gate> [<project gate>]
       node gate.js list --asset <class> [--fact <fact> ...] [--staged] --reader builder --stage build --parts <file> [--parts <file> ...]
                         <vault gate> [<project gate>]
       node gate.js list --asset <class> [--fact <fact> ...] [--staged] --reader whole-page|type|script <vault gate> [<project gate>]
       node gate.js tally --asset <class> [--fact <fact> ...] [--staged] --answered <file> --critic <file> --critic <file>
                          --critic <file> [--pass <n>] [--parts <candidate>=<parts.json> ...] [--settle <file> ...] <vault gate> [<project gate>]
       node gate.js recheck --asset <class> [--fact <fact> ...] [--staged] --before <file> --answered <file> --fault <candidate>:<id> [--fault ...]
                            --critic <file> --critic <file> --critic <file> [--parts <candidate>=<parts.json> --before-parts <candidate>=<parts.json> ...]
                            [--settle <file> ...] <vault gate> [<project gate>]
  a gate file may be a directory, every .md file in it: the vault's gate is skills/design-critique/rules;
  --staged adds the staged records to whatever the command reads;
  list's --parts names the parts the candidate has: parts.json from parts-map.py, whose part roles count where they are one of
  ${MAPPED_PARTS.join(", ")}, or the building session's parts declaration, {"declared": {<part>: <its CSS selector, or null>}},
  or one parts map carrying a "declared" beside its "parts", which tally and recheck also take; <part> is one of
  ${PARTS.join(", ")};
  a --critic may be several files, comma-joined, where its candidates were split across dispatches;
  --pass names one of the passes of at most ${LOOK_LIMIT} questions a look list runs in, by stage then area, which list then prints
  alone and tally then tallies, with every script and code answer; tally needs one on a list of more than ${LOOK_LIMIT};
  <class> is one of ${ASSET_CLASSES.join(", ")}; <fact> one of ${ASSET_FACTS.join(", ")}`;

function readerFault({ reader = "gate", stage, look, answered, pass, parts }) {
  if (!READERS.includes(reader)) return `--reader is ${reader}, not one of ${READERS.join(", ")}`;
  if (reader === "builder" && !BUILDER_STAGES.includes(stage)) return `--reader builder takes --stage ${BUILDER_STAGES.join(", ")}, not ${stage ?? "none"}`;
  if (reader !== "builder" && stage) return `--stage is the builder's, not --reader ${reader}'s`;
  if (reader !== "gate" && (look || answered || pass)) return `--look, --answered and --pass are the gate list's, not --reader ${reader}'s`;
  const build = reader === "builder" && stage === "build";
  if (build && !parts?.length) return "--stage build needs the parts the candidate has, --parts <parts map or parts declaration>";
  if (!build && parts?.length) return "--parts is the build stage's alone, --reader builder --stage build";
  return null;
}

function readAssetArgs({ asset, fact: facts = [] }) {
  if (!ASSET_CLASSES.includes(asset)) return { why: `--asset is ${asset ?? "missing"}, not one of ${ASSET_CLASSES.join(", ")}` };
  const unknown = facts.filter((f) => !ASSET_FACTS.includes(f));
  if (unknown.length) return { why: `--fact ${unknown.join(", ")} is not one of ${ASSET_FACTS.join(", ")}` };
  const motionNeededBy = asset === "motion" ? "a motion asset" : ["has-motion-over-5s", "has-brand-motion"].find((f) => facts.includes(f));
  if (motionNeededBy && !facts.includes("has-motion")) return { why: `${motionNeededBy} needs --fact has-motion too` };
  if (asset === "motion" && !facts.includes("has-brand-motion")) return { why: "a motion asset needs --fact has-brand-motion too" };
  return { asset, facts: [...new Set(facts)] };
}

const SETTLED = { stage: "the dependency order decides first, and a later step never changes an earlier one", law: "within one step, law and WCAG beat every other rule", project: "within one step, the project beats every vault question but law and WCAG, and domain evidence only on evidence of its own" };
const FOR_FOUNDER = {
  "same-owner": "both are {owner}'s own",
  "same-level": "both at one precedence level",
  unread: "it turns on a vault level the rule records do not record",
  "vault-levels": "both are vault questions below law, which the rule records do not rank",
  evidence: "the project's rule departs from domain evidence, and stands only on evidence of its own",
};
const YIELDING = { neither: "neither yields to the other", each: "each yields to the other", unread: "whether one yields to the other is not read" };

function passLabel({ questions, phase }) {
  const asked = new Map();
  for (const q of questions) asked.set(stageOf(q), new Set([...(asked.get(stageOf(q)) ?? []), q.area]));
  const when = phase === 0 ? "" : `, once the ${PHASES[0].name} passes' fixes land`;
  return `${PHASES[phase].name}${when}: ${[...asked].map(([stage, areas]) => `${stage}: ${[...areas].join(", ")}`).join("; ")}`;
}

function printList({ look, answered, clashes: found }, { asset, facts }, lookOnly, { looked, unmeasured, split, passes }, pass) {
  const tag = (q, answerer) => {
    if (unmeasured.has(q) && !answerer) return ` (${q.fields["answered-by"].value} cannot measure it for ${unmeasured.get(q).join(", ")})`;
    if (isScriptOwed(q)) return " (script owed)";
    return answerer ? ` (${q.fields["answered-by"].value})` : "";
  };
  const item = (q, answerer) => `${q.n}. ${q.id}${tag(q, answerer)}: ${q.fields.question.value}\n${appliesTo(q)}`;
  const section = (questions, answerer) => (questions.length ? questions.map((q) => item(q, answerer)).join("\n") : "None.");
  const shown = pass ? passes[pass - 1].questions : looked;
  console.log(`Gate list for ${assetLine({ asset, facts })}: ${(lookOnly ? shown : [...look, ...answered]).length} question(s).`);
  if (!split && !pass) console.log(`\nLook questions, for the critics:\n\n${section(looked, false)}`);
  else if (pass) console.log(`\nLook questions, for the critics, pass ${pass} of ${passes.length}, ${passLabel(passes[pass - 1])}:\n\n${section(shown, false)}`);
  else {
    console.log(`\nLook questions, for the critics, in ${passes.length} passes of at most ${LOOK_LIMIT}, as there are more than ${LOOK_LIMIT}, each to a fresh trio:`);
    passes.forEach((p, i) => console.log(`\nPass ${i + 1}, ${passLabel(p)}:\n\n${section(p.questions, false)}`));
  }
  if (lookOnly) return;
  console.log(`\nScript and code questions, for the building session:\n\n${section(answered, true)}`);
  console.log("\nClashes, for the reveal:\n");
  if (!found.length) return console.log("None.");
  for (const { a, b, yielding, reason, winner } of found) {
    const pair = `${a.n}. ${a.id} and ${b.n}. ${b.id} both write ${a.fields.writes.value} and ${YIELDING[yielding]}`;
    if (winner) console.log(`- Settled by precedence (${SETTLED[reason]}): ${pair}; ${winner.id} stands.`);
    else {
      console.log(`- For the founder (${FOR_FOUNDER[reason].replace("{owner}", a.fields.owner.value)}): ${pair}.`);
    }
  }
}

const assetLine = ({ asset, facts }) => [asset, ...facts].join(", ");
const UNNAMED_SCRIPT = "a project's script, unnamed";
const appliesTo = (q) => `   Applies to: ${splitAppliesWhen(q.fields["applies-when"].value).part}`;
const stageOf = (q) => q.fields.stage?.value ?? "no stage";
function groupIds(records, key) {
  const groups = new Map();
  for (const q of records) groups.set(key(q), [...(groups.get(key(q)) ?? []), q.id]);
  return groups;
}
const numberedLines = (records, line) => (records.length ? records.map((q, i) => `${i + 1}. ${line(q)}\n${appliesTo(q)}`).join("\n") : "None.");

function printTargets(records, given, stage, partsPresent) {
  const parts = stage === "build" ? `, for a candidate with ${partsPresent.length ? partsPresent.join(", ") : "none of the parts the records name"}` : "";
  console.log(`Targets for the building session, ${assetLine(given)}, at the ${stage} stage${parts}: ${records.length} record(s).\n`);
  console.log(numberedLines(records, (q) => `${q.id} (${stageOf(q)}): ${(q.fields.target ?? q.fields.question).value}`));
}

function printScripts(records, given) {
  const scripts = groupIds(records.filter((r) => !isScriptOwed(r)), (q) => q.fields.script?.value ?? "");
  console.log(`Scripts for the building session to run at the finish stage, ${assetLine(given)}, each until it passes: ${scripts.size} script(s).\n`);
  console.log(scripts.size ? [...scripts].map(([script, ids], i) => `${i + 1}. ${script || UNNAMED_SCRIPT}\n   Answers: ${ids.join(", ")}`).join("\n") : "None.");
  const owed = records.filter(isScriptOwed);
  if (owed.length) console.log(`\nScript owed, so the gate critics look instead: ${owed.map((q) => q.id).join(", ")}.`);
}

const READER_NAMES = { "whole-page": "the whole-page critic", type: "the type critic", script: "the scripts" };

function printRecords(records, given, reader) {
  console.log(`Records for ${READER_NAMES[reader]}, ${assetLine(given)}, coarse to fine: ${records.length} record(s).\n`);
  const label = (q) => (reader === "script" ? (isScriptOwed(q) ? "script owed" : q.fields.script?.value ?? UNNAMED_SCRIPT) : stageOf(q));
  console.log(numberedLines(records, (q) => `${q.id} (${label(q)}): ${q.fields.question.value}`));
  if (reader === "script") return;
  const sections = groupIds(records.filter((r) => r.fields.reasons), (q) => q.fields.reasons.value);
  console.log(`\nReference sections they cite, in skills/:\n\n${sections.size ? [...sections].map(([s, ids]) => `- ${s}: ${ids.join(", ")}`).join("\n") : "None."}`);
}

const capitalise = (word) => word[0].toUpperCase() + word.slice(1);

const countLine = (looked) => LOOKED.map((a) => [a, looked.filter((l) => l.answer === a).length]).filter(([, k]) => k).map(([a, k]) => `${k} ${capitalise(a)}`).join(" and ");

const deadLine = (p) => `dead, it goes to ${p.dead === "#" ? "# alone" : `${p.dead}, which nothing on the page carries`}`;

const CELLS = {
  pass: ({ counts }) => `pass (${counts})`,
  false: ({ counts }) => `false, it cannot be acted on and looks as if it can (${counts})`,
  hidden: ({ counts }) => `hidden, it can be acted on and does not look it (${counts})`,
  minor: ({ counts, twin }) => `hidden, minor: ${twin.id} looks actable and goes to the same place (${counts})`,
  dead: ({ counts, p }) => `${deadLine(p)} (${counts})`,
  split: ({ counts }) => `split, for a settle critic, ${counts}`,
  founder: ({ counts }) => `for the founder, ${counts}`,
};

const settledTail = (settled) => (settled ? `; settled by ${settled.name}: ${capitalise(settled.answer)}` : "");

function printByPart(q, verdict, parts, unlisted, offKey) {
  console.log(`  ${q.n}. ${q.id} (look, part by part): ${verdict}`);
  for (const { p, looked, cell, twin, panel, settled } of parts) {
    if (cell === "pass" && !settled) continue;
    console.log(`     ${p.id} "${p.text}": ${CELLS[cell]({ counts: countLine(looked) + settledTail(settled), twin, p })}`);
    if (panel === "split") for (const l of looked) console.log(`       ${l.name}: ${capitalise(l.answer)}. ${l.evidence}`);
    if (settled) console.log(`       ${settled.name}: ${capitalise(settled.answer)}. ${settled.evidence}`);
  }
  for (const { name, line } of unlisted) console.log(`     ${name} names a part off the key: ${line}`);
  if (offKey?.settled) console.log(`     parts off the key: ${offKey.verdict === "fault" ? "false, one looks as if it can be acted on" : offKey.verdict}${settledTail(offKey.settled)}. ${offKey.settled.evidence}`);
  else if (offKey) console.log("     parts off the key: split, for a settle critic");
}

function printTally(results, critics, clashesNamed) {
  const questions = results[0].rows.length;
  const owed = results[0].rows.filter((r) => isScriptOwed(r.q)).length;
  console.log(`Tally of ${results.length} candidate(s) on ${questions} question(s)${owed ? `, ${owed} of them script owed` : ""}, from ${critics.map((c) => c.name).join(", ")}.`);
  for (const { candidate, rows } of results) {
    const count = (verdict) => rows.filter((r) => r.verdict === verdict).length;
    console.log(`\n${candidate}: ${count("fault")} fault(s), ${count("split")} split, ${count("founder")} for the founder, ${count("pass")} pass.`);
    for (const row of rows) {
      const { q, verdict, measured, looked, parts, unlisted, offKey } = row;
      const answerer = q.fields["answered-by"].value;
      if (parts) {
        printByPart(q, verdict, parts, unlisted, offKey);
        continue;
      }
      if (!looked) {
        console.log(`  ${q.n}. ${q.id} (${answerer}): ${verdict}`);
        if (verdict !== "pass") console.log(`     ${measured.evidence}`);
        continue;
      }
      const [tail, lines] = printLooked(row, "     ");
      const by = measured ? `${answerer} cannot measure it, so look` : isScriptOwed(q) ? "script owed, so look" : "look";
      console.log(`  ${q.n}. ${q.id} (${by}): ${verdict}, ${tail}`);
      if (verdict !== "pass" && measured) console.log(`     ${answerer}: ${measured.evidence}`);
      for (const line of lines) console.log(line);
    }
  }
  console.log("\nClashes the critics named, for the reveal:\n");
  if (!clashesNamed.length) return console.log("None.");
  for (const { name, candidate, quotes } of clashesNamed) console.log(`- ${name}, on ${candidate ?? "the whole round"}: "${quotes[0]}" against "${quotes[1]}"`);
}

function printLooked({ panel, looked, settled }, indent) {
  const tail = countLine(looked) + settledTail(settled);
  const settledLine = settled ? [`${indent}${settled.name}: ${capitalise(settled.answer)}. ${settled.evidence}`] : [];
  if (panel !== "pass") return [tail, [...looked.map((l) => `${indent}${l.name}: ${capitalise(l.answer)}. ${l.evidence}`), ...settledLine]];
  const minor = looked.filter((l) => MINOR.test(l.evidence));
  return [`${tail}${minor.length ? ", a minor case reported" : ""}`, [...minor.map((l) => `${indent}${l.name}: ${l.evidence}`), ...settledLine]];
}

function printRecheck(results, critics, answered) {
  const count = results.reduce((n, { faults }) => n + faults.length, 0);
  console.log(`Re-check of ${count} fault(s) on ${results.length} candidate(s), from ${critics.map((c) => c.name).join(", ")}.`);
  const said = { pass: "gone", fault: "not gone", split: "split, for a settle critic", founder: "for the founder" };
  for (const { candidate, faults, others, broken, newDead } of results) {
    const cleared = faults.filter((f) => !f.stops.length && !f.unsettled).length;
    const stopped = faults.filter((f) => f.stops.length).length;
    console.log(`\n${candidate}: ${cleared} cleared, ${stopped} stopped, ${faults.length - cleared - stopped} split.`);
    for (const fault of faults) {
      const { q, verdict, measured, looked, deadParts = [] } = fault;
      const answerer = q.fields["answered-by"].value;
      if (!looked) {
        console.log(`  ${q.n}. ${q.id} (${answerer} re-run): ${said[verdict]}`);
        if (verdict !== "pass") console.log(`     ${measured.evidence}`);
        continue;
      }
      const [tail, lines] = printLooked(fault, "     ");
      console.log(`  ${q.n}. ${q.id} (${measured ? `${answerer} cannot measure it, so look` : "look"}): ${said[verdict]}, ${tail}`);
      if (verdict !== "pass" && measured) console.log(`     ${answerer}: ${measured.evidence}`);
      for (const line of lines) console.log(line);
      for (const p of deadParts) console.log(`     re-run parts map: ${p.id} "${p.text}": ${deadLine(p)}`);
    }
    const [tail, lines] = printLooked(others, "     ");
    console.log(`  every other question: ${{ pass: "no worse", fault: "broken", split: "split, for a settle critic", founder: "for the founder" }[others.verdict]}, ${tail}`);
    for (const line of lines) console.log(line);
    for (const q of broken) console.log(`  ${q.n}. ${q.id} (${q.fields["answered-by"].value} re-run): passed before the fix, fails now\n     ${answered[candidate][q.id].evidence}`);
    if (newDead?.parts.length) console.log(`  ${newDead.q.n}. ${newDead.q.id} (re-run parts map): a link going nowhere since the fix`);
    for (const p of newDead?.parts ?? []) console.log(`     ${p.id} "${p.text}": ${deadLine(p)}`);
    for (const { q, stops, unsettled } of faults) {
      if (stops.length) console.log(`  ${q.id}: stop, for the reveal: ${stops.map((n) => `${STOPS[n]} (stop signal ${n})`).join("; ")}`);
      else if (unsettled) console.log(`  ${q.id}: split, for a settle critic`);
      else console.log(`  ${q.id}: cleared`);
    }
  }
}

function gatePaths(given) {
  let names;
  try {
    if (!fs.statSync(given).isDirectory()) return [given];
    names = fs.readdirSync(given).filter((n) => n.endsWith(".md")).sort();
  } catch (err) {
    console.error(`${given}: ${err.message}`);
    return null;
  }
  if (!names.length) console.error(`${given}: a directory holding no .md gate file`);
  return names.length ? names.map((n) => path.join(given, n)) : null;
}

function readText(file) {
  try {
    return fs.readFileSync(file, "utf8");
  } catch (err) {
    console.error(`${file}: ${err.message}`);
    return null;
  }
}

function sharedCriticFile(critics) {
  const owner = new Map();
  for (const [index, files] of critics.entries()) {
    for (const file of files.split(",")) {
      let real;
      try {
        real = fs.realpathSync(file);
      } catch {
        real = path.resolve(file);
      }
      if (owner.has(real) && owner.get(real) !== index) return `${file} is named under two --critic flags, so one critic would count as two`;
      owner.set(real, index);
    }
  }
  return null;
}

function readFile(files, kind) {
  const read = { name: files, answers: {}, clashes: [], faults: [] };
  for (const file of files.split(",")) {
    const text = readText(file);
    if (text === null) return null;
    const one = parseAnswers(text, kind);
    read.faults.push(...one.faults.map((m) => `${file}: ${m}`));
    for (const [candidate, given] of Object.entries(one.answers)) {
      if (candidate in read.answers) read.faults.push(`${file}: answers for ${candidate}, which another of ${files} answers too`);
      read.answers[candidate] = given;
    }
    read.clashes.push(...one.clashes);
  }
  return read;
}

function partsOwed(command, list, candidates, fixed) {
  const [named, stranger] = command === "tally" ? [candidates, "which the building session's answers do not name"] : [[...fixed.keys()], "which no --fault names"];
  const owed = list.look.some((q) => q.id === PARTS_QUESTION) ? named : [];
  return { owed, named, stranger, since: `${PARTS_QUESTION} is on the list` };
}

function readPartsMaps(given, flag, command, { owed, named, stranger, since }) {
  const bare = given.find((v) => !/^[^=]+=./.test(v));
  if (bare !== undefined) return { usage: `${flag} takes <candidate>=<parts.json>, not ${bare}` };
  const files = Object.fromEntries(given.map((v) => [v.slice(0, v.indexOf("=")), v.slice(v.indexOf("=") + 1)]));
  const usage = Object.keys(files).filter((c) => !named.includes(c)).map((c) => `${flag} names ${c}, ${stranger}`)[0] ??
    owed.filter((c) => !files[c]).map((c) => `${command} needs a parts map for ${c}, ${flag} ${c}=<parts.json>, since ${since}`)[0];
  if (usage) return { usage };
  const maps = {};
  const faults = [];
  for (const c of owed) {
    const text = readText(files[c]);
    if (text === null) return {};
    const read = parseParts(text);
    maps[c] = read.parts;
    faults.push(...read.faults.map((m) => `${files[c]}: ${m}`));
  }
  return { maps, faults };
}

function printReader(files, given, { reader, stage, staged, parts = [] }) {
  const partsPresent = [];
  const faults = [];
  for (const file of parts) {
    const text = readText(file);
    if (text === null) return 2;
    const read = parsePartsPresent(text);
    partsPresent.push(...read.names.filter((n) => !partsPresent.includes(n)));
    faults.push(...read.faults.map((m) => `${file}: ${m}`));
  }
  for (const m of faults) console.log(m);
  if (faults.length) return 1;
  const records = pickRecords(assetRecords(files, given.asset, given.facts, Boolean(staged)), reader, stage, partsPresent);
  if (reader === "builder" && stage === "finish") printScripts(records, given);
  else if (reader === "builder") printTargets(records, given, stage, partsPresent);
  else printRecords(records, given, reader);
  return 0;
}

function main(argv) {
  const [command, ...rest] = argv;
  let paths = rest;
  let values = {};
  let given;
  const isRecheck = command === "recheck";
  const critiqued = command === "tally" || isRecheck;
  if (command === "list" || critiqued) {
    const options = { asset: { type: "string" }, fact: { type: "string", multiple: true }, answered: { type: "string" }, staged: { type: "boolean" }, parts: { type: "string", multiple: true } };
    if (!isRecheck) options.pass = { type: "string" };
    if (command === "list") Object.assign(options, { look: { type: "boolean" }, reader: { type: "string" }, stage: { type: "string" } });
    else Object.assign(options, { critic: { type: "string", multiple: true }, settle: { type: "string", multiple: true } });
    if (isRecheck) Object.assign(options, { fault: { type: "string", multiple: true }, before: { type: "string" }, "before-parts": { type: "string", multiple: true } });
    let parsed;
    try {
      parsed = parseArgs({ args: rest, options, allowPositionals: true });
    } catch (err) {
      console.error(`${err.message}\n${USAGE}`);
      return 2;
    }
    ({ values, positionals: paths } = parsed);
    given = readAssetArgs(values);
    let why = given.why ?? (paths.length < 1 || paths.length > 2 ? `${command} takes the vault's gate and at most one project's, not ${paths.length} paths` : null);
    if (!why && command === "list") why = readerFault(values);
    if (!why && values.pass !== undefined && !/^[1-9]\d*$/.test(values.pass)) why = `--pass is ${values.pass}, not a pass number`;
    if (!why && critiqued && !values.answered) why = `${command} needs the building session's answers, --answered <file>`;
    if (!why && critiqued && values.critic?.length !== CRITIC_COUNT) why = `${command} takes ${CRITIC_COUNT} ${command === "tally" ? "look" : "re-check"} critics' answers, --critic <file> each, not ${values.critic?.length ?? 0}`;
    if (!why && critiqued) why = sharedCriticFile(values.critic);
    if (!why && isRecheck && !values.fault?.length) why = "recheck needs each fault fixed, --fault <candidate>:<id>";
    if (!why && isRecheck && !values.before) why = "recheck needs the building session's answers from before the fix, --before <file>";
    if (why) {
      console.error(`${why}\n${USAGE}`);
      return 2;
    }
  } else if (command !== "check" || paths.length === 0) {
    console.error(USAGE);
    return 2;
  }
  const files = [];
  for (const given of paths) {
    const named = gatePaths(given);
    if (named === null) return 2;
    for (const file of named) {
      const text = readText(file);
      if (text === null) return 2;
      files.push({ file, text });
    }
  }
  const { faults, count } = checkGates(files);
  for (const f of faults) console.log(`${f.file}:${f.line}: ${f.message}`);
  if (faults.length) return 1;
  if (command === "check") {
    console.log(`${count} gate question(s) in ${files.length} file(s) pass`);
    return 0;
  }
  const reader = values.reader ?? "gate";
  if (reader !== "gate") return printReader(files, given, values);
  const list = listGates(files, given.asset, given.facts, Boolean(values.staged));
  const answered = values.answered && readFile(values.answered, "measured");
  const pass = values.pass && Number(values.pass);
  const before = values.before && readFile(values.before, "measured");
  const critics = (values.critic ?? []).map((files) => readFile(files, isRecheck ? "recheck" : "critic"));
  const settles = (values.settle ?? []).map((file) => readFile(file, isRecheck ? "recheck" : "settle"));
  if (answered === null || before === null || critics.includes(null) || settles.includes(null)) return 2;
  const named = (name, faults) => faults.map((m) => `${name}: ${m}`);
  const formFaults = [answered, before, ...critics, ...settles].filter(Boolean).flatMap(({ faults: f }) => f);
  for (const file of [answered, before].filter(Boolean)) if (!formFaults.length) formFaults.push(...named(file.name, answeredFaults(list, file.answers)));
  const split = lookPasses(list, answered?.answers);
  let passIds = null;
  if (!formFaults.length && !isRecheck) {
    if (!pass && split.split && critiqued) {
      console.error(`the look list has ${split.looked.length} questions, more than ${LOOK_LIMIT}, so its critics answer it in ${split.passes.length} passes: tally each with --pass 1 to ${split.passes.length}\n${USAGE}`);
      return 2;
    }
    if (pass > split.passes.length) {
      console.error(`--pass is ${pass}, but this look list runs in ${split.passes.length} pass(es)\n${USAGE}`);
      return 2;
    }
    if (pass) passIds = new Set(split.passes[pass - 1].questions.map((q) => q.id));
  }
  let fixed;
  if (!formFaults.length && isRecheck) {
    const read = parseFixed(values.fault, list, answered.answers);
    fixed = read.fixed;
    formFaults.push(...read.faults);
  }
  const maps = {};
  if (!formFaults.length && critiqued) {
    const owing = partsOwed(command, list, Object.keys(answered.answers), fixed);
    for (const [key, flag] of isRecheck ? [["now", "parts"], ["before", "before-parts"]] : [["now", "parts"]]) {
      const read = readPartsMaps(values[flag] ?? [], `--${flag}`, command, owing);
      if (read.usage) {
        console.error(`${read.usage}\n${USAGE}`);
        return 2;
      }
      if (!read.maps) return 2;
      maps[key] = read.maps;
      formFaults.push(...read.faults);
    }
  }
  if (!formFaults.length) {
    for (const c of critics) {
      const faults = isRecheck ? recheckCriticFaults(list, answered.answers, fixed, c) : criticFaults(list, answered.answers, c, maps.now, passIds);
      formFaults.push(...named(c.name, faults));
    }
  }
  const judge = (settled) =>
    isRecheck ? recheckFaults(list, answered.answers, before.answers, fixed, critics, settled, maps) : tallyGates(list, answered.answers, critics, maps.now, settled, passIds);
  let settled = new Map();
  if (!formFaults.length && settles.length) {
    const read = readSettles(settles, judge(settled), isRecheck);
    settled = read.settled;
    formFaults.push(...read.faults);
  }
  for (const m of formFaults) console.log(m);
  if (formFaults.length) return 1;
  if (command === "list") printList(list, given, Boolean(values.look), split, pass);
  else if (isRecheck) printRecheck(judge(settled), critics, answered.answers);
  else printTally(judge(settled), critics, critics.flatMap(({ name, clashes: named }) => named.map((c) => ({ name, ...c }))));
  return 0;
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));

module.exports = { CRITIC_COUNT };
