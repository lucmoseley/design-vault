#!/usr/bin/env node
/**
 * Usage:
 *   node check-curves.js <file> [<file> ...]
 *   node check-curves.js --bends <file> [<file> ...]
 *   node check-curves.js --bends --json < shapes.json
 *   node check-curves.js --contacts [--json] <file> [<file> ...]
 *
 * Finds curves drawn as chains of straight lines, corners where two curves
 * meet, and kinks where a curve meets a line, in each file: an .svg, or a page
 * saved after its scripts ran (`python3 scripts/browse.py html <url> --out
 * page.html` in the vault). Reads every `d="…"` of a <path> and every
 * `points="…"` of a <polygon> or <polyline> where it is drawn: not in a comment
 * or in <script> or <style> text, nor under display="none" or in <defs>,
 * <clipPath>, <mask>, <symbol>, <marker> or <pattern>, unless a <use> or a
 * url() names it or an element around it.
 *
 * A breach is a run of at least MIN_RUN straight segments in a row, each
 * turning the same way by between MIN_TURN and MAX_TURN degrees. A corner of a
 * rectangle (90°), a straight line cut into pieces (0°) and a zigzag (the turn
 * changes sign) are not breaches.
 *
 * A breach is also a node where two curves meet (a cubic, quadratic or arc on
 * each side) whose tangents differ by more than the angle the path's written
 * precision allows there. A corner vault.curves-script excuses is still
 * reported: say so beside it in the round folder. Where a curve meets a
 * straight line, or a cubic or quadratic whose control points lie on its
 * chord, the node is a breach only when its tangents also differ by less than
 * NEAR_TANGENT.
 *
 * --bends prints where vault.curves-look's 8x shot goes instead: each
 * subpath's tightest bend and its radius, and the vertex that turns most in
 * each run of straight segments that bends like a curve. --json reads shapes
 * from stdin with the transform each is drawn through, and writes the points
 * mapped by it.
 *
 * --contacts lists, for vault.contacts-code, every pair of segments from two
 * shapes that run alongside, CONTACT_PX or less apart once drawn: paths,
 * polygons, polylines, circles, ellipses, rects and lines, through their
 * transforms and their <svg>'s viewBox, in painting order. Each is classed,
 * from where the two fills lie: coincident (the edges agree to the coarser
 * path's written precision, both fills on one side) and underlap (one fill runs
 * on past the other's edge) pass; separate (the ground shows between the edges)
 * and shared edge, no underlap (each fill takes one side of one exact edge)
 * fail. A separate gap that shapes painted after both fill, at both edges and
 * halfway between them, is covered and passes, naming those shapes; whether
 * their paint hides the gap is check-seams.py's to measure (vault.contacts-seam),
 * not this script's. A shape painted before either does not cover it, nor does
 * one in another outermost <svg> or one hidden by visibility. Each line ends with
 * the contact as look-renders.py contacts' --contact, a shell word to pass on
 * unchanged. With --json, one JSON object on stdout instead: { contactPx, notes,
 * unread, contacts }, contactPx being CONTACT_PX, each
 * contact { file, name, cls, verdict, lower, upper, at, along, word, covers },
 * lower and upper the two shapes' selectors, at and along in upper's user units,
 * word the --contact word unquoted, and covers the selectors of a covered
 * contact's covers, in painting order.
 * The file is read as the browser parses it: an .svg, .xhtml, .xht or .xml as XML,
 * as written and case-sensitive; anything else as HTML, through the element tree
 * parse5 builds by the HTML Standard's tree construction, so each shape's
 * selector, painting order and outermost <svg> are the ones the browser's tree
 * gives it, and a <template>'s content is not read. Reading HTML needs the
 * plugin's npm packages (plugin/package.json).
 * --contacts does not read: stroke widths (a stroke is its centre line), a
 * stylesheet's or an animation's geometry, what a <use> draws, an <svg> sized by
 * CSS, whose user units are read as CSS px with a note, and contacts between two
 * outermost <svg>s.
 *
 * Exits 0 with no breach, 1 with one or more (each printed; path data it
 * cannot read counts as one), 2 on bad usage or an unreadable file. --bends exits
 * 0, or 1 where path data could not be read. --contacts exits 0 with no failing
 * contact, 1 with one or more, 6 where a shape could not be read and none
 * failed, 2 on bad usage or an unreadable file.
 */
"use strict";
const fs = require("node:fs");
const { parseArgs } = require("node:util");

// guess, lucmoseley/mmm-infra#16
const MIN_RUN = 4;
// guess, lucmoseley/mmm-infra#16
const MIN_TURN = 0.5;
// guess, lucmoseley/mmm-infra#16
const MAX_TURN = 30;
// guess, #219
const NEAR_TANGENT = 0.1;
// guess, #501
const FLOAT_NOISE = 1e-9;

// Each path command's argument count: https://www.w3.org/TR/SVG2/paths.html#PathDataBNF
const ARGS = { m: 2, l: 2, h: 1, v: 1, c: 6, s: 4, q: 4, t: 2, a: 7, z: 0 };
const NUMBER = /^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?/;

function halfUnit(text) {
  const [, mantissa, exp] = text.match(/^[+-]?([\d.]+)(?:[eE]([+-]?\d+))?$/);
  const places = mantissa.includes(".") ? mantissa.length - mantissa.indexOf(".") - 1 : 0;
  return 0.5 * 10 ** (Number(exp || 0) - places);
}

function tokenise(d) {
  const cmds = [];
  let i = 0;
  let cur = null;
  const skip = () => {
    while (i < d.length && /[\s,]/.test(d[i])) i++;
  };
  for (skip(); i < d.length; skip()) {
    const ch = d[i];
    if (/[a-zA-Z]/.test(ch)) {
      if (!(ch.toLowerCase() in ARGS)) throw new Error(`unknown path command '${ch}'`);
      cur = { cmd: ch, nums: [], errs: [] };
      cmds.push(cur);
      i++;
      continue;
    }
    if (!cur) throw new Error("path data does not start with a command");
    // https://www.w3.org/TR/SVG2/paths.html#PathDataBNF: an arc's flags are single digits that may run together
    const argIndex = cur.nums.length % ARGS[cur.cmd.toLowerCase()];
    if (cur.cmd.toLowerCase() === "a" && (argIndex === 3 || argIndex === 4) && /[01]/.test(ch)) {
      cur.nums.push(Number(ch));
      cur.errs.push(0);
      i++;
      continue;
    }
    const m = d.slice(i).match(NUMBER);
    // guess, #501
    if (!m) throw new Error(`unreadable path data at '${d.slice(i, i + 12)}'`);
    cur.nums.push(Number(m[0]));
    cur.errs.push(halfUnit(m[0]));
    i += m[0].length;
  }
  return cmds;
}

function segments(d) {
  const out = [];
  let x = 0;
  let y = 0;
  let sx = 0;
  let sy = 0;
  let lastCtrl = null;
  for (const { cmd, nums } of tokenise(d)) {
    const lower = cmd.toLowerCase();
    const rel = cmd === lower;
    const n = ARGS[lower];
    if (n === 0) {
      out.push({ kind: "line", from: [x, y], to: [sx, sy], close: true });
      [x, y] = [sx, sy];
      lastCtrl = null;
      continue;
    }
    if (nums.length === 0 || nums.length % n !== 0) throw new Error(`'${cmd}' takes ${n} numbers per segment, got ${nums.length}`);
    for (let k = 0; k < nums.length; k += n) {
      const a = nums.slice(k, k + n);
      const pt = (i) => (rel ? [x + a[i], y + a[i + 1]] : [a[i], a[i + 1]]);
      let nx = x;
      let ny = y;
      if (lower === "h") nx = rel ? x + a[0] : a[0];
      else if (lower === "v") ny = rel ? y + a[0] : a[0];
      else [nx, ny] = pt(n - 2);
      const seg = { kind: "line", from: [x, y], to: [nx, ny] };
      const reflects = lastCtrl !== null && lastCtrl.of.includes(lower);
      const reflected = reflects ? [2 * x - lastCtrl.at[0], 2 * y - lastCtrl.at[1]] : [x, y];
      if (lower === "c") seg.ctrl = [pt(0), pt(2)];
      else if (lower === "s") seg.ctrl = [reflected, pt(0)];
      else if (lower === "q") seg.ctrl = [pt(0)];
      else if (lower === "t") seg.ctrl = [reflected];
      // https://www.w3.org/TR/SVG2/paths.html#ArcOutOfRangeParameters: a zero radius draws a straight line
      else if (lower === "a" && a[0] !== 0 && a[1] !== 0) seg.arc = { rx: Math.abs(a[0]), ry: Math.abs(a[1]), phi: (a[2] * Math.PI) / 180, large: a[3], sweep: a[4] };
      if (seg.ctrl || seg.arc) seg.kind = "curve";
      lastCtrl = seg.ctrl ? { at: seg.ctrl[seg.ctrl.length - 1], of: seg.ctrl.length === 2 ? "cs" : "qt" } : null;
      // https://www.w3.org/TR/SVG2/paths.html#PathDataMovetoCommands: a moveto's later pairs are implicit linetos
      if (lower === "m" && k === 0) {
        out.push({ kind: "move" });
        [sx, sy] = [nx, ny];
      } else out.push(seg);
      [x, y] = [nx, ny];
    }
  }
  return out;
}

function arcCentre(s) {
  const { rx: rx0, ry: ry0, phi, large, sweep } = s.arc;
  const [cos, sin] = [Math.cos(phi), Math.sin(phi)];
  const [hx, hy] = [(s.from[0] - s.to[0]) / 2, (s.from[1] - s.to[1]) / 2];
  const x1 = cos * hx + sin * hy;
  const y1 = -sin * hx + cos * hy;
  const grow = Math.sqrt(Math.max(1, (x1 * x1) / (rx0 * rx0) + (y1 * y1) / (ry0 * ry0)));
  const [rx, ry] = [rx0 * grow, ry0 * grow];
  const num = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1;
  const coef = (large === sweep ? -1 : 1) * Math.sqrt(Math.max(0, num / (rx * rx * y1 * y1 + ry * ry * x1 * x1)));
  const [cx, cy] = [(coef * rx * y1) / ry, (-coef * ry * x1) / rx];
  const start = Math.atan2((y1 - cy) / ry, (x1 - cx) / rx);
  const end = Math.atan2((-y1 - cy) / ry, (-x1 - cx) / rx);
  let turn = end - start;
  if (sweep && turn < 0) turn += 2 * Math.PI;
  if (!sweep && turn > 0) turn -= 2 * Math.PI;
  const centre = [cos * cx - sin * cy + (s.from[0] + s.to[0]) / 2, sin * cx + cos * cy + (s.from[1] + s.to[1]) / 2];
  return { rx, ry, cos, sin, centre, start, end, turn };
}

function arcTangent(s, at) {
  const { rx, ry, cos, sin, start, end } = arcCentre(s);
  const t = at === "end" ? end : start;
  const dir = s.arc.sweep ? 1 : -1;
  const [tx, ty] = [-rx * Math.sin(t) * dir, ry * Math.cos(t) * dir];
  const len = Math.hypot(tx, ty);
  const chord = Math.hypot(s.to[0] - s.from[0], s.to[1] - s.from[1]);
  return [((cos * tx - sin * ty) / len) * chord, ((sin * tx + cos * ty) / len) * chord];
}

function tangent(s, at) {
  const pts = [s.from, ...(s.ctrl || []), s.to];
  if (at === "end") pts.reverse();
  const [x0, y0] = pts[0];
  const next = pts.slice(1).find(([px, py]) => px !== x0 || py !== y0);
  if (!next) return null;
  if (s.arc) return arcTangent(s, at);
  return at === "end" ? [x0 - next[0], y0 - next[1]] : [next[0] - x0, next[1] - y0];
}

function bends(s, err) {
  if (s.arc) return true;
  if (!s.ctrl) return false;
  const [dx, dy] = [s.to[0] - s.from[0], s.to[1] - s.from[1]];
  const len = Math.hypot(dx, dy);
  return s.ctrl.some(([px, py]) => (len === 0 ? Math.hypot(px - s.from[0], py - s.from[1]) : Math.abs((px - s.from[0]) * dy - (py - s.from[1]) * dx) / len) > err);
}

function findCorners(d) {
  const corners = [];
  const err = Math.min(...tokenise(d).flatMap((c) => c.errs.filter((e) => e > 0)));
  const check = (a, b) => {
    const curves = [bends(a, err), bends(b, err)].filter(Boolean).length;
    if (curves === 0) return;
    const [u, v] = [tangent(a, "end"), tangent(b, "start")];
    const angle = Math.atan2(Math.abs(u[0] * v[1] - u[1] * v[0]), u[0] * v[0] + u[1] * v[1]);
    const allowed = Math.atan((0.98 * err) / Math.min(Math.hypot(...u), Math.hypot(...v))) + FLOAT_NOISE;
    const kink = curves === 1;
    if (angle > allowed && (!kink || angle < NEAR_TANGENT)) corners.push({ at: a.to, angle: (angle * 180) / Math.PI, allowed: (allowed * 180) / Math.PI, kink });
  };
  let sub = [];
  const close = (closed) => {
    for (let k = 1; k < sub.length; k++) check(sub[k - 1], sub[k]);
    if (closed && sub.length > 1) check(sub[sub.length - 1], sub[0]);
    sub = [];
  };
  for (const s of segments(d)) {
    if (s.kind === "move") close(false);
    else {
      if (tangent(s, "start")) sub.push(s);
      if (s.close) close(true);
    }
  }
  close(false);
  return corners;
}

// guess, #228
const BEND_SAMPLES = 200;
// guess, #228
const BEND_STEPS = 60;

function affine([a, b, c, d, e, f] = [1, 0, 0, 1, 0, 0]) {
  const vector = ([x, y]) => [a * x + c * y, b * x + d * y];
  return { vector, point: (p) => vector(p).map((v, i) => v + [e, f][i]) };
}

function curveAt(s, map) {
  const out = ({ p, d1, d2 }) => ({ p: map.point(p), d1: map.vector(d1), d2: map.vector(d2) });
  if (s.arc) {
    const { rx, ry, cos, sin, centre, start, turn } = arcCentre(s);
    const rot = ([x, y]) => [cos * x - sin * y, sin * x + cos * y];
    return (t) => {
      const a = start + turn * t;
      const [px, py] = rot([rx * Math.cos(a), ry * Math.sin(a)]);
      return out({
        p: [centre[0] + px, centre[1] + py],
        d1: rot([-rx * Math.sin(a) * turn, ry * Math.cos(a) * turn]),
        d2: rot([-rx * Math.cos(a) * turn * turn, -ry * Math.sin(a) * turn * turn]),
      });
    };
  }
  const pts = [s.from, ...s.ctrl, s.to];
  const casteljau = (ps, t) => {
    let row = ps;
    while (row.length > 1) row = row.slice(1).map((q, i) => [row[i][0] + (q[0] - row[i][0]) * t, row[i][1] + (q[1] - row[i][1]) * t]);
    return row[0] || [0, 0];
  };
  const diff = (ps, k) => ps.slice(1).map((q, i) => [(q[0] - ps[i][0]) * k, (q[1] - ps[i][1]) * k]);
  const n = pts.length - 1;
  const first = diff(pts, n);
  const second = diff(first, n - 1);
  return (t) => out({ p: casteljau(pts, t), d1: casteljau(first, t), d2: casteljau(second, t) });
}

function curvature({ d1, d2 }) {
  const speed = Math.hypot(...d1);
  return speed === 0 ? Infinity : Math.abs(d1[0] * d2[1] - d1[1] * d2[0]) / speed ** 3;
}

function sharpest(s, map) {
  const at = curveAt(s, map);
  const k = (t) => curvature(at(t));
  let best = 0;
  for (let i = 1; i <= BEND_SAMPLES; i++) if (k(i / BEND_SAMPLES) > k(best / BEND_SAMPLES)) best = i;
  let [lo, hi] = [Math.max(0, best - 1) / BEND_SAMPLES, Math.min(BEND_SAMPLES, best + 1) / BEND_SAMPLES];
  const g = (Math.sqrt(5) - 1) / 2;
  for (let i = 0; i < BEND_STEPS; i++) {
    const [a, b] = [hi - g * (hi - lo), lo + g * (hi - lo)];
    if (k(a) > k(b)) hi = b;
    else lo = a;
  }
  const t = [best / BEND_SAMPLES, (lo + hi) / 2].reduce((x, y) => (k(y) > k(x) ? y : x));
  return { at: at(t).p, radius: 1 / k(t) };
}

function tightestBends(d, matrix) {
  const map = affine(matrix);
  const err = Math.min(...tokenise(d).flatMap((c) => c.errs.filter((e) => e > 0)));
  const out = [];
  let best = null;
  const close = () => {
    if (best) out.push(best);
    best = null;
  };
  for (const s of segments(d)) {
    if (s.kind === "move") close();
    else if (s.kind === "curve" && bends(s, err)) {
      const b = sharpest(s, map);
      if (!best || b.radius < best.radius) best = b;
    }
  }
  close();
  for (const r of findRuns(d)) out.push({ at: map.point(r.sharpest), segments: r.segments });
  return out;
}

function pointsToPath(points, closed) {
  const nums = points.trim().split(/[\s,]+/).filter(Boolean);
  if (nums.length < 4) return "";
  return `M${nums.slice(0, 2).join(" ")} L${nums.slice(2).join(" ")}${closed ? " Z" : ""}`;
}

function turn(s1, s2) {
  const a1 = Math.atan2(s1.to[1] - s1.from[1], s1.to[0] - s1.from[0]);
  const a2 = Math.atan2(s2.to[1] - s2.from[1], s2.to[0] - s2.from[0]);
  let t = ((a2 - a1) * 180) / Math.PI;
  while (t > 180) t -= 360;
  while (t <= -180) t += 360;
  return t;
}

function findRuns(d) {
  const lines = segments(d).map((s) => (s.kind === "line" && s.from[0] === s.to[0] && s.from[1] === s.to[1] ? null : s));
  const runs = [];
  let run = 0;
  let sign = 0;
  let start = null;
  let sharp = null;
  const close = () => {
    if (run >= MIN_RUN) runs.push({ start, segments: run, sharpest: sharp.at });
    run = 0;
    sign = 0;
  };
  let prev = null;
  for (const s of lines) {
    if (s === null) continue;
    if (s.kind !== "line") {
      close();
      prev = null;
      continue;
    }
    if (prev) {
      const t = turn(prev, s);
      const mag = Math.abs(t);
      const sgn = Math.sign(t);
      if (mag >= MIN_TURN && mag <= MAX_TURN && (sign === 0 || sgn === sign)) {
        if (run === 0) {
          run = 1;
          start = prev.from;
          sharp = null;
        }
        run++;
        sign = sgn;
        if (!sharp || mag > sharp.mag) sharp = { at: s.from, mag };
      } else {
        close();
        if (mag >= MIN_TURN && mag <= MAX_TURN) {
          run = 2;
          start = prev.from;
          sign = sgn;
          sharp = { at: s.from, mag };
        }
      }
    }
    prev = s;
  }
  close();
  return runs;
}

const NODE_WRITTEN = new Set(["path", "polygon", "polyline"]);

function nodeWrittenShapes(tree) {
  const { shapes, referable, refs } = drawnShapes(tree);
  return [...shapes, ...referable.filter((s) => s.ids.some((i) => refs.has(i)))]
    .filter((s) => NODE_WRITTEN.has(s.tag.toLowerCase()))
    .sort((a, b) => a.offset - b.offset);
}

function checkTree(tree) {
  const breaches = [];
  for (const { line, tag, id, d, error } of nodeWrittenShapes(tree)) {
    if (error !== undefined) {
      breaches.push({ line, tag, id, error });
      continue;
    }
    let runs;
    let corners;
    try {
      runs = findRuns(d);
      corners = findCorners(d);
    } catch (err) {
      breaches.push({ line, tag, id, error: err.message });
      continue;
    }
    for (const r of runs) breaches.push({ line, tag, id, ...r });
    for (const c of corners) breaches.push({ line, tag, id, corner: c });
  }
  return breaches;
}

// guess, #331
const CONTACT_PX = 2;
// guess, #331
const ALONGSIDE = 30;
// guess, #331
const FLAT_PX = 1e-3;
// guess, #331
const STEP_PX = 0.25;
// guess, #331
const PROBE_PX = 1e-4;
// guess, #331
const MAX_PIECES = 1e5;

const CLASSES = ["separate", "shared edge, no underlap", "covered", "underlap", "coincident"];
const FAULTS = new Set(CLASSES.slice(0, 2));

const IDENTITY = [1, 0, 0, 1, 0, 0];
// https://www.w3.org/TR/SVG2/struct.html#DefsElement: shapes in these are not drawn where they stand
const UNDRAWN = new Set(["defs", "clipPath", "mask", "symbol", "marker", "pattern"]);
const SVG_NS = "http://www.w3.org/2000/svg";
const RAW = new Set(["script", "style"]);
// a file:// page's parser follows its extension's MIME type: https://source.chromium.org/chromium/chromium/src/+/main:net/base/mime_util.cc
const XML_FILE = /\.(?:svg|xhtml?|xht|xml)$/i;
const NUMBER_ONLY = new RegExp(`${NUMBER.source}$`);

function parseLength(v) {
  const text = v?.trim().replace(/px$/, "");
  return text !== undefined && NUMBER_ONLY.test(text) ? Number(text) : null;
}

function compose([a, b, c, d, e, f], [A, B, C, D, E, F]) {
  return [a * A + c * B, b * A + d * B, a * C + c * D, b * C + d * D, a * E + c * F + e, b * E + d * F + f];
}

function invert([a, b, c, d, e, f]) {
  const det = a * d - b * c;
  return [d / det, -b / det, -c / det, a / det, (c * f - d * e) / det, (b * e - a * f) / det];
}

function stretch([a, b, c, d]) {
  const sum = a * a + b * b + c * c + d * d;
  return Math.sqrt((sum + Math.sqrt(Math.max(0, sum * sum - 4 * (a * d - b * c) ** 2))) / 2);
}

function parseTransform(text) {
  let m = IDENTITY;
  const rest = text.replace(/(matrix|translate|scale|rotate|skewX|skewY)\s*\(([^)]*)\)/g, (_, fn, args) => {
    const n = args.trim().split(/[\s,]+/).filter(Boolean).map(Number);
    const counts = { matrix: [6], translate: [1, 2], scale: [1, 2], rotate: [1, 3], skewX: [1], skewY: [1] }[fn];
    if (!counts.includes(n.length) || !n.every(Number.isFinite)) throw new Error(`unreadable transform '${text}'`);
    const rad = (n[0] * Math.PI) / 180;
    let t;
    if (fn === "matrix") t = n;
    else if (fn === "translate") t = [1, 0, 0, 1, n[0], n[1] ?? 0];
    else if (fn === "scale") t = [n[0], 0, 0, n[1] ?? n[0], 0, 0];
    else if (fn === "skewX") t = [1, 0, Math.tan(rad), 1, 0, 0];
    else if (fn === "skewY") t = [1, Math.tan(rad), 0, 1, 0, 0];
    else {
      const [cx, cy] = [n[1] ?? 0, n[2] ?? 0];
      const [cos, sin] = [Math.cos(rad), Math.sin(rad)];
      t = compose(compose([1, 0, 0, 1, cx, cy], [cos, sin, -sin, cos, 0, 0]), [1, 0, 0, 1, -cx, -cy]);
    }
    m = compose(m, t);
    return "";
  });
  if (/[^\s,]/.test(rest)) throw new Error(`unreadable transform '${text}'`);
  return m;
}

function viewport(attrs) {
  const [x, y, w, h] = [parseLength(attrs.x) ?? 0, parseLength(attrs.y) ?? 0, parseLength(attrs.width), parseLength(attrs.height)];
  const box = (attrs.viewBox ?? "").trim().split(/[\s,]+/).map(Number);
  if (box.length !== 4 || !box.every(Number.isFinite) || box[2] <= 0 || box[3] <= 0) return { map: [1, 0, 0, 1, x, y], sized: true };
  if (!w || !h) return { map: [1, 0, 0, 1, x - box[0], y - box[1]], sized: false };
  const [align, fit] = (attrs.preserveAspectRatio ?? "xMidYMid meet").trim().split(/\s+/);
  if (align === "none") return { map: [w / box[2], 0, 0, h / box[3], x - (box[0] * w) / box[2], y - (box[1] * h) / box[3]], sized: true };
  const s = (fit === "slice" ? Math.max : Math.min)(w / box[2], h / box[3]);
  const room = (axis, size, viewSize) => ({ Min: 0, Mid: 0.5, Max: 1 })[axis] * (size - viewSize * s) || 0;
  return { map: [s, 0, 0, s, x - box[0] * s + room(align.slice(1, 4), w, box[2]), y - box[1] * s + room(align.slice(5, 8), h, box[3])], sized: true };
}

function parseAttrs(text) {
  return [...text.matchAll(/([\w:.-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g)].map(([, name, dq, sq]) => [name, dq ?? sq]);
}

function buildAttrs(list) {
  const attrs = Object.fromEntries(list);
  const important = new Set();
  for (const decl of (attrs.style ?? "").split(";")) {
    const [name, ...value] = decl.split(":");
    if (!value.length) continue;
    const prop = keyword(name);
    const raw = value.join(":");
    const isImportant = /!\s*important\s*$/i.test(raw);
    if (important.has(prop) && !isImportant) continue;
    if (isImportant) important.add(prop);
    attrs[prop] = raw.replace(/!\s*important\s*$/i, "").trim();
  }
  return attrs;
}

// https://www.w3.org/TR/CSS21/syndata.html#characters: CSS keywords and property names are ASCII case-insensitive
const keyword = (v) => v.trim().toLowerCase();

function basicShape(tag, attrs) {
  let err = Infinity;
  const num = (name) => {
    if (attrs[name] === undefined) return 0;
    const n = parseLength(attrs[name]);
    if (n === null) throw new Error(`unreadable ${name} '${attrs[name]}'`);
    err = Math.min(err, halfUnit(attrs[name].trim().replace(/px$/, "")));
    return n;
  };
  const oval = (cx, cy, rx, ry) => `M${cx - rx} ${cy}A${rx} ${ry} 0 1 0 ${cx + rx} ${cy}A${rx} ${ry} 0 1 0 ${cx - rx} ${cy}Z`;
  let d = null;
  if (tag === "circle") {
    const [cx, cy, r] = ["cx", "cy", "r"].map(num);
    if (r > 0) d = oval(cx, cy, r, r);
  } else if (tag === "ellipse") {
    const [cx, cy, rx, ry] = ["cx", "cy", "rx", "ry"].map(num);
    if (rx > 0 && ry > 0) d = oval(cx, cy, rx, ry);
  } else if (tag === "line") d = `M${num("x1")} ${num("y1")}L${num("x2")} ${num("y2")}`;
  else {
    const [x, y, w, h] = ["x", "y", "width", "height"].map(num);
    const [rxIn, ryIn] = ["rx", "ry"].map((k) => (attrs[k] === undefined ? null : num(k)));
    const [rx, ry] = [Math.min(rxIn ?? ryIn ?? 0, w / 2), Math.min(ryIn ?? rxIn ?? 0, h / 2)];
    const [r, b] = rx > 0 && ry > 0 ? [rx, ry] : [0, 0];
    const corner = (cx, cy) => (r ? `A${r} ${b} 0 0 1 ${cx} ${cy}` : "");
    if (w > 0 && h > 0) d = `M${x + r} ${y}H${x + w - r}${corner(x + w, y + b)}V${y + h - b}${corner(x + w - r, y + h)}H${x + r}${corner(x, y + h - b)}V${y + b}${corner(x + r, y)}Z`;
  }
  return d && { d, err };
}

const DRAWN = new Set(["path", "polygon", "polyline", "circle", "ellipse", "rect", "line"]);

// https://www.w3.org/TR/css-cascade-5/#inherit-initial: on an inherited property unset acts as inherit
const isInheritedValue = (v) => v === undefined || ["inherit", "unset"].includes(keyword(v));

function parseXmlTree(text) {
  const tree = { children: [] };
  const stack = [{ name: null, node: tree, ns: null }];
  const markup = /<!--[\s\S]*?-->|<!\[CDATA\[[\s\S]*?\]\]>|<[!?][^>]*>|<\/([\w:.-]+)\s*>|<([\w:.-]+)((?:[^>"']|"[^"]*"|'[^']*')*)>/g;
  let m;
  while ((m = markup.exec(text))) {
    const [, closing, tag, rest] = m;
    if (closing) {
      const k = stack.findLastIndex((el, i) => i > 0 && el.name === closing);
      if (k > 0) stack.length = k;
      continue;
    }
    if (!tag) continue;
    const parent = stack[stack.length - 1];
    const attrs = parseAttrs(rest);
    const ns = attrs.find(([n]) => n === "xmlns")?.[1] ?? parent.ns;
    const node = { name: tag, ns, attrs, children: [], line: text.slice(0, m.index).split("\n").length, offset: m.index };
    parent.node.children.push(node);
    if (!/\/\s*$/.test(rest)) stack.push({ name: tag, node, ns });
    if (RAW.has(tag.toLowerCase())) {
      const end = text.indexOf(`</${tag}`, markup.lastIndex);
      markup.lastIndex = end < 0 ? text.length : end;
    }
  }
  return tree;
}

function parseHtmlTree(text) {
  const parse5 = loadParse5();
  if (!parse5) return null;
  const elements = (n) => n.childNodes.filter((c) => c.tagName !== undefined).map(element);
  const element = (n) => ({
    name: n.tagName,
    ns: n.namespaceURI,
    attrs: n.attrs.map((a) => [a.prefix ? `${a.prefix}:${a.name}` : a.name, a.value]),
    children: elements(n),
    line: n.sourceCodeLocation?.startLine,
    offset: n.sourceCodeLocation?.startOffset,
  });
  return { children: elements(parse5.parse(text, { sourceCodeLocationInfo: true, scriptingEnabled: true })) };
}

let parse5Loaded;

function loadParse5() {
  if (parse5Loaded !== undefined) return parse5Loaded;
  try {
    parse5Loaded = require("parse5");
  } catch (err) {
    const fix = err.code === "MODULE_NOT_FOUND"
      ? "the design-vault plugin's npm packages are not installed; run `claude plugin update design-vault@lucmoseley`, or in a vault clone `npm ci --ignore-scripts --prefix plugin`"
      : `Node ${process.versions.node} cannot require() parse5, an ES module; run it on Node 20.19 or later`;
    console.error(`check-curves.js cannot read an HTML file (${err.message.split("\n")[0]}): ${fix}`);
    parse5Loaded = null;
  }
  return parse5Loaded;
}

function drawnShapes(tree) {
  const out = [];
  const referable = [];
  const refs = new Set();
  const notes = [];
  const enter = (node, parent, chain) => {
    const name = node.ns == null || node.ns === SVG_NS ? node.name : null;
    const attrs = buildAttrs(node.attrs);
    const { line, name: tag, offset } = node;
    const id = attrs.id;
    for (const v of Object.values(attrs)) for (const [, ref] of v.matchAll(/url\(\s*["']?#([^)"'\s]+)/g)) refs.add(ref);
    const href = attrs.href ?? attrs["xlink:href"];
    if (href?.startsWith("#")) refs.add(href.slice(1));
    const el = {
      selector: id ? (/^[A-Za-z_][\w-]*$/.test(id) ? `#${id}` : `[id="${id.replace(/["\\]/g, "\\$&")}"]`) : chain,
      root: parent.root ?? (name === "svg" ? offset : null),
      ids: id ? [...parent.ids, id] : parent.ids,
      matrix: parent.matrix,
      fill: isInheritedValue(attrs.fill) ? parent.fill : keyword(attrs.fill) !== "none",
      evenodd: isInheritedValue(attrs["fill-rule"]) ? parent.evenodd : keyword(attrs["fill-rule"]) === "evenodd",
      undrawn: parent.undrawn || UNDRAWN.has(name) || (attrs.display !== undefined && keyword(attrs.display) === "none"),
      // https://www.w3.org/TR/SVG2/render.html#VisibilityControl: inherited, and a descendant may set it back to visible
      visible: isInheritedValue(attrs.visibility) ? parent.visible : keyword(attrs.visibility) === "visible",
      transformError: parent.transformError,
    };
    try {
      if (name === "svg") {
        const { map, sized } = viewport(attrs);
        if (!sized) notes.push(`${line} <${tag}> gives no width and height in px, so its user units are read as CSS px`);
        el.matrix = compose(el.matrix, map);
      }
      if (attrs.transform) el.matrix = compose(el.matrix, parseTransform(attrs.transform));
    } catch (err) {
      el.transformError ??= err.message;
    }
    if (DRAWN.has(name)) {
      const list = el.undrawn ? referable : out;
      const base = { line, tag, id, offset, ...(el.undrawn ? { ids: el.ids } : { order: out.length + 1 }) };
      try {
        let shape;
        if (name === "path") shape = attrs.d && { d: attrs.d };
        else if (name === "polygon" || name === "polyline") shape = attrs.points && { d: pointsToPath(attrs.points, name === "polygon") };
        else shape = basicShape(name, attrs);
        if (shape?.d) {
          shape.err ??= Math.min(...tokenise(shape.d).flatMap((c) => c.errs.filter((e) => e > 0)));
          const fill = el.fill && name !== "line";
          list.push({ ...base, ...shape, matrix: el.matrix, fill, visible: el.visible, evenodd: el.evenodd, selector: el.selector, root: el.root, transformError: el.transformError });
        }
      } catch (err) {
        list.push({ ...base, error: err.message });
      }
    }
    return el;
  };
  const visit = (node, parent) => {
    const seen = {};
    for (const child of node.children) {
      // https://www.w3.org/TR/selectors-4/#the-nth-of-type-pseudo: siblings of one type share a local name and a namespace
      const type = `${child.ns} ${child.name}`;
      seen[type] = (seen[type] ?? 0) + 1;
      visit(child, enter(child, parent, parent.selector === null ? ":root" : `${parent.selector}>${child.name}:nth-of-type(${seen[type]})`));
    }
  };
  visit(tree, { selector: null, root: null, ids: [], matrix: IDENTITY, fill: true, evenodd: false, undrawn: false, visible: true, transformError: undefined });
  return { shapes: out, referable, refs, notes };
}

function flatten(s, map, scale) {
  if (s.kind === "line") return [map.point(s.from), map.point(s.to)];
  let n;
  if (s.arc) {
    const { rx, ry, turn } = arcCentre(s);
    const r = Math.max(rx, ry) * scale;
    n = Math.abs(turn) / (2 * Math.acos(Math.max(-1, 1 - FLAT_PX / r)));
  } else {
    const pts = [s.from, ...s.ctrl, s.to].map(map.point);
    const degree = pts.length - 1;
    const bend = Math.max(...pts.slice(2).map((p, i) => Math.hypot(pts[i][0] - 2 * pts[i + 1][0] + p[0], pts[i][1] - 2 * pts[i + 1][1] + p[1])));
    n = Math.sqrt(((degree * (degree - 1)) / 8) * (bend / FLAT_PX));
  }
  n = Math.min(MAX_PIECES, Math.max(1, Math.ceil(n)));
  const at = curveAt(s, map);
  return Array.from({ length: n + 1 }, (_, i) => at(i / n).p);
}

const boxOf = (pts) => pts.reduce(([x0, y0, x1, y1], [x, y]) => [Math.min(x0, x), Math.min(y0, y), Math.max(x1, x), Math.max(y1, y)], [Infinity, Infinity, -Infinity, -Infinity]);
const isInBox = ([x, y], [x0, y0, x1, y1], pad) => x >= x0 - pad && x <= x1 + pad && y >= y0 - pad && y <= y1 + pad;
const doBoxesMeet = (a, b, pad) => a[0] <= b[2] + pad && b[0] <= a[2] + pad && a[1] <= b[3] + pad && b[1] <= a[3] + pad;

function outline(shape) {
  const map = affine(shape.matrix);
  const scale = stretch(shape.matrix);
  const edges = [];
  const rings = [];
  let ring = null;
  let n = 0;
  const add = (pts) => {
    n++;
    if (pts.some((p) => p[0] !== pts[0][0] || p[1] !== pts[0][1])) edges.push({ n, pts, box: boxOf(pts) });
  };
  const end = (closed) => {
    if (!ring) return;
    const [first, last] = [ring[0], ring[ring.length - 1]];
    if (!closed && shape.fill && (first[0] !== last[0] || first[1] !== last[1])) add([last, first]);
    rings.push(ring);
    ring = null;
  };
  for (const s of segments(shape.d)) {
    if (s.kind === "move") {
      end(false);
      continue;
    }
    const pts = flatten(s, map, scale);
    ring = ring ? ring.concat(pts.slice(1)) : pts;
    add(pts);
    if (s.close) end(true);
  }
  end(false);
  return { ...shape, scale, edges, rings };
}

function isFilledAt(shape, [x, y]) {
  if (!shape.fill) return false;
  let winding = 0;
  for (const ring of shape.rings) {
    for (let i = 0; i < ring.length; i++) {
      const [[ax, ay], [bx, by]] = [ring[i], ring[(i + 1) % ring.length]];
      const side = (bx - ax) * (y - ay) - (x - ax) * (by - ay);
      if (ay <= y && by > y && side > 0) winding++;
      else if (ay > y && by <= y && side < 0) winding--;
    }
  }
  return shape.evenodd ? winding % 2 !== 0 : winding !== 0;
}

function nearest(edge, p) {
  let best = null;
  const { pts } = edge;
  for (let i = 1; i < pts.length; i++) {
    const [a, b] = [pts[i - 1], pts[i]];
    const [dx, dy] = [b[0] - a[0], b[1] - a[1]];
    const len = Math.hypot(dx, dy);
    if (len === 0) continue;
    const u = Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (len * len)));
    const q = [a[0] + u * dx, a[1] + u * dy];
    const d = Math.hypot(p[0] - q[0], p[1] - q[1]);
    if (!best || d < best.d) best = { d, q, dir: [dx / len, dy / len], end: (i === 1 && u === 0) || (i === pts.length - 1 && u === 1) };
  }
  return best;
}

function sides(shape, [x, y], [dx, dy]) {
  return [isFilledAt(shape, [x + dy * PROBE_PX, y - dx * PROBE_PX]), isFilledAt(shape, [x - dy * PROBE_PX, y + dx * PROBE_PX])];
}

function classify(shape, p, dir, other, f, tol) {
  const mid = [(p[0] + f.q[0]) / 2, (p[1] + f.q[1]) / 2];
  const apart = () => (isFilledAt(shape, mid) || isFilledAt(other, mid) ? "underlap" : "separate");
  if (f.d > tol) return apart();
  const [x1, x2] = sides(shape, p, dir);
  let [y1, y2] = sides(other, f.q, f.dir);
  if (dir[0] * f.dir[0] + dir[1] * f.dir[1] < 0) [y1, y2] = [y2, y1];
  if (x1 !== x2 && y1 !== y2 && x1 !== y1) return f.d <= 2 * FLAT_PX ? "shared edge, no underlap" : apart();
  return (x1 && x2) || (y1 && y2) ? "underlap" : "coincident";
}

function alongside(shape, a, other, b, tol) {
  const found = [];
  const turn = Math.sin((ALONGSIDE * Math.PI) / 180);
  for (let i = 1; i < a.pts.length; i++) {
    const [s, e] = [a.pts[i - 1], a.pts[i]];
    const len = Math.hypot(e[0] - s[0], e[1] - s[1]);
    if (len === 0) continue;
    const dir = [(e[0] - s[0]) / len, (e[1] - s[1]) / len];
    const steps = Math.ceil(len / STEP_PX);
    for (let k = 0; k < steps; k++) {
      const p = [s[0] + (e[0] - s[0]) * ((k + 0.5) / steps), s[1] + (e[1] - s[1]) * ((k + 0.5) / steps)];
      if (!isInBox(p, b.box, CONTACT_PX)) continue;
      const f = nearest(b, p);
      if (f.d > CONTACT_PX || f.end || Math.abs(dir[0] * f.dir[1] - dir[1] * f.dir[0]) > turn) continue;
      const at = [(p[0] + f.q[0]) / 2, (p[1] + f.q[1]) / 2];
      found.push({ cls: classify(shape, p, dir, other, f, tol), at, dir, gap: [p, at, f.q], d: f.d });
    }
  }
  return found;
}

function findContacts(shapes) {
  const drawn = shapes.map(outline);
  const contacts = [];
  for (let j = 1; j < drawn.length; j++) {
    const upper = drawn[j];
    const toUser = affine(invert(upper.matrix));
    const above = drawn.slice(j + 1).filter((s) => s.root === upper.root);
    const coversOf = (gap) => above.filter((s) => s.visible && gap.every((pt) => isFilledAt(s, pt)));
    for (const lower of drawn.slice(0, j)) {
      if (lower.root !== upper.root) continue;
      const tol = Math.max(lower.err * lower.scale, upper.err * upper.scale) + 2 * FLAT_PX;
      for (const a of lower.edges) {
        for (const b of upper.edges) {
          if (!doBoxesMeet(a.box, b.box, CONTACT_PX)) continue;
          const both = [alongside(lower, a, upper, b, tol), alongside(upper, b, lower, a, tol)];
          for (const f of both.flat()) {
            const covers = f.cls === "separate" ? coversOf(f.gap) : [];
            if (covers.length) Object.assign(f, { cls: "covered", covers });
          }
          const cls = CLASSES.find((c) => both.flat().some((f) => f.cls === c));
          if (!cls) continue;
          const [onA, onB] = both.map((found) => found.filter((f) => f.cls === cls));
          const run = onA.length ? onA : onB;
          const ds = [...onA, ...onB].map((f) => f.d);
          const covers = [...new Set([...onA, ...onB].flatMap((f) => f.covers ?? []))].sort((s, t) => s.order - t.order);
          const mid = run[Math.floor(run.length / 2)];
          const ahead = [mid.at[0] + mid.dir[0], mid.at[1] + mid.dir[1]];
          contacts.push({ lower, upper, a: a.n, b: b.n, cls, tol, at: toUser.point(mid.at), along: toUser.point(ahead), near: Math.min(...ds), far: Math.max(...ds), covers });
        }
      }
    }
  }
  return contacts;
}

const shellWord = (s) => `'${s.replace(/'/g, "'\\''")}'`;
// guess, #331
const roundPx = (v) => +v.toPrecision(2);

function verdict(c, file) {
  const apart = c.near === c.far ? `${roundPx(c.near)} px` : `${roundPx(c.near)}–${roundPx(c.far)} px`;
  if (c.cls === "separate") return `the edges run ${apart} apart and never meet, so the ground shows between them; draw both sides from one shared curve, and run one fill on under the other`;
  if (c.cls === "covered") {
    const covers = c.covers.map((s) => where(file, s)).join(" and ");
    return `the edges run ${apart} apart, and ${covers}, painted over both, ${c.covers.length === 1 ? "spans" : "span"} the gap; whether ${c.covers.length === 1 ? "its" : "their"} paint hides it is measured by check-seams.py (vault.contacts-seam), not here`;
  }
  if (c.cls === "shared edge, no underlap") return "the two fills meet on one exact edge and each covers part of its edge pixels, so the ground shows through the seam; make them one path, or run one on under the other";
  if (c.cls === "underlap") return `one fill runs on under the other, the edges ${apart} apart`;
  return `the edges match within the ${roundPx(c.tol)} px the paths' written precision allows`;
}

function printContacts(argv) {
  let parsed;
  try {
    parsed = parseArgs({ args: argv, options: { json: { type: "boolean" } }, allowPositionals: true, strict: true });
  } catch (err) {
    console.error(`check-curves.js: ${err.message}`);
    parsed = { values: {}, positionals: [] };
  }
  const { json } = parsed.values;
  const files = parsed.positionals;
  if (files.length === 0) {
    console.error("usage: node check-curves.js --contacts [--json] <file> [<file> ...]");
    return 2;
  }
  const trees = readFiles(files);
  if (!trees) return 2;
  const [notes, unread, listed] = [[], [], []];
  for (const { file, tree } of trees) {
    const { shapes: found, notes: noted } = drawnShapes(tree);
    for (const note of noted) notes.push(`${file}:${note}`);
    const readable = [];
    for (const s of found) {
      let error = s.error ?? s.transformError;
      try {
        if (error === undefined) segments(s.d);
      } catch (err) {
        error = err.message;
      }
      if (error !== undefined) unread.push(`${where(file, s)}: could not read the shape, so its contacts are not measured: ${error}; judge them under vault.contacts-code`);
      else if (s.matrix[0] * s.matrix[3] !== s.matrix[1] * s.matrix[2]) readable.push(s);
    }
    const names = new Set();
    for (const c of findContacts(readable)) {
      const label = (s) => (s.id ?? `${s.tag}${s.order}`).replace(/[^\w.-]/g, "_");
      let name = `${label(c.lower)}.${c.a}-${label(c.upper)}.${c.b}`;
      for (let k = 2; names.has(name); k++) name = `${label(c.lower)}.${c.a}-${label(c.upper)}.${c.b}-${k}`;
      names.add(name);
      // guess, #331
      const fixed = (pt) => pt.map((v) => +v.toFixed(3));
      const word = `${name}=${c.upper.selector}@${fixed(c.at).join(",")}`;
      const pair = `${where(file, c.lower)} segment ${c.a} and ${where(file, c.upper)} segment ${c.b}`;
      listed.push({ file, name, cls: c.cls, verdict: verdict(c, file), pair, lower: c.lower.selector, upper: c.upper.selector, at: fixed(c.at), along: fixed(c.along), word, covers: c.covers.map((s) => s.selector) });
    }
  }
  const faults = listed.filter((c) => FAULTS.has(c.cls)).length;
  if (json) console.log(JSON.stringify({ contactPx: CONTACT_PX, notes, unread, contacts: listed.map(({ pair, ...c }) => c) }));
  else {
    for (const line of [...notes, ...unread]) console.log(line);
    for (const c of listed) console.log(`${c.pair}: ${c.cls}: ${c.verdict}. --contact ${shellWord(c.word)}`);
    if (listed.length === 0 && !unread.length) console.log(`no two shapes come within ${CONTACT_PX} px of each other along an edge in ${files.length} file(s)`);
    else if (listed.length) console.log(`${listed.length} contact(s) in ${files.length} file(s), ${faults} failing`);
  }
  if (faults) return 1;
  return unread.length ? 6 : 0;
}

function readFiles(files) {
  const out = [];
  for (const file of files) {
    let text;
    try {
      text = fs.readFileSync(file, "utf8");
    } catch (err) {
      console.error(`${file}: ${err.message}`);
      return null;
    }
    const tree = XML_FILE.test(file) ? parseXmlTree(text) : parseHtmlTree(text);
    if (!tree) return null;
    out.push({ file, tree });
  }
  return out;
}

const where = (file, { line, tag, id }) => `${file}:${line} <${tag}${id ? ` id="${id}"` : ""}>`;
const pointText = (p) => p.map((v) => +v.toFixed(2)).join(", ");

function printBendsJson() {
  let list;
  try {
    list = JSON.parse(fs.readFileSync(0, "utf8"));
  } catch (err) {
    list = err;
  }
  const isShape = (s) => s && (typeof s.d === "string" || typeof s.points === "string");
  if (!Array.isArray(list) || !list.every(isShape)) {
    console.error("--bends --json wants a JSON array of { d } or { points, closed } shapes on stdin");
    return 2;
  }
  const read = (s) => {
    try {
      return tightestBends(s.d ?? pointsToPath(s.points, s.closed), s.matrix);
    } catch (err) {
      return { error: err.message };
    }
  };
  console.log(JSON.stringify(list.map(read)));
  return 0;
}

function printBends(files) {
  if (files[0] === "--json") return printBendsJson();
  if (files.length === 0) {
    console.error("usage: node check-curves.js --bends <file> [<file> ...] | --bends --json < shapes.json");
    return 2;
  }
  const trees = readFiles(files);
  if (!trees) return 2;
  let unread = 0;
  for (const { file, tree } of trees) {
    for (const shape of nodeWrittenShapes(tree)) {
      let found;
      let { error } = shape;
      if (error === undefined) {
        try {
          found = tightestBends(shape.d);
        } catch (err) {
          error = err.message;
        }
      }
      if (error !== undefined) {
        unread++;
        console.log(`${where(file, shape)}: could not read the path: ${error}`);
        continue;
      }
      for (const b of found) {
        if (b.segments) console.log(`${where(file, shape)}: ${b.segments} straight segments bend like a curve, turning most at (${pointText(b.at)})`);
        else console.log(`${where(file, shape)}: tightest bend at (${pointText(b.at)}), radius ${+b.radius.toPrecision(3)}`);
      }
    }
  }
  return unread ? 1 : 0;
}

function main(argv) {
  if (argv[0] === "--bends") return printBends(argv.slice(1));
  if (argv[0] === "--contacts") return printContacts(argv.slice(1));
  if (argv.length === 0) {
    console.error("usage: node check-curves.js <file> [<file> ...]");
    return 2;
  }
  const trees = readFiles(argv);
  if (!trees) return 2;
  let found = 0;
  for (const { file, tree } of trees) {
    for (const b of checkTree(tree)) {
      found++;
      if (b.error) console.log(`${where(file, b)}: could not read the path: ${b.error}`);
      else if (b.corner?.kink) console.log(`${where(file, b)}: the curve and straight line meeting at (${pointText(b.corner.at)}) turn ${b.corner.angle.toPrecision(3)}° there, past the ${b.corner.allowed.toPrecision(2)}° their written precision allows but under the ${((NEAR_TANGENT * 180) / Math.PI).toPrecision(2)}° a meant corner turns; put the curve's handle in line with the straight side, unless vault.curves-script excuses the kink`);
      else if (b.corner) console.log(`${where(file, b)}: the curves meeting at (${pointText(b.corner.at)}) turn ${b.corner.angle.toPrecision(3)}° there, past the ${b.corner.allowed.toPrecision(2)}° their written precision allows; put the handles either side of the node on one line, unless vault.curves-script excuses the corner`);
      else console.log(`${where(file, b)}: ${b.segments} straight segments in a row bend like a curve, from (${pointText(b.start)}); draw it as a Bézier or arc`);
    }
  }
  if (found === 0) console.log(`no polygon curves, corners between curves or kinks between a curve and a line in ${argv.length} file(s)`);
  return found === 0 ? 0 : 1;
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));
