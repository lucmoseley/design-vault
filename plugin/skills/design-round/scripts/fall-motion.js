"use strict";
const G = 9.80665;
const DEFAULT_TOLERANCE = 0.02; // guess, #151
const PROGRESS_DECIMALS = 6; // guess, #151
const TIME_DECIMALS = 4; // guess, #151
const CRITICAL_WITHIN = 1e-6; // guess, #501
const CHORD_POINTS = 32; // guess, #501
const MIN_SPAN_MS = 0.05; // guess, #501
const SPEED_SPAN_MS = 1; // guess, #142
const FRAME_MS = 1000 / 60;
const STILL_SHARE = 0.01; // guess, #501
const STILL_ARCMIN_S = 1; // guess, #501
const VIEW_CM = 60; // guess, #501
const CSS_PX_CM = 2.54 / 96;
const SPAN_SPEED_RATIO = 1.15; // measured: no step at 1.15 on a grid of 1,020 falls and settles, steps at 1.5, #196
// measured in docs/research/jolt-onset.md, #297
const JOLT_BAND = [
  [200, 0.8, 0.8],
  [250, 0.54, 0.67],
  [300, 0.43, 0.6],
  [500, 0.27, 0.47],
  [1000, 0.19, 0.39],
  [2000, 0.17, 0.35],
];
const JUMP_DEG = 0.26; // measured in docs/research/jolt-onset.md, #297

function stillPx(viewCm) {
  return STILL_ARCMIN_S / ((60 * 180 * Math.atan(CSS_PX_CM / viewCm)) / Math.PI);
}

function joltLine(ms) {
  if (ms < JOLT_BAND[0][0]) return null;
  for (let i = 1; i < JOLT_BAND.length; i++) {
    const [a, loA, hiA] = JOLT_BAND[i - 1];
    const [b, loB, hiB] = JOLT_BAND[i];
    if (ms <= b) return (loA + hiA + ((ms - a) / (b - a)) * (loB + hiB - loA - hiA)) / 2;
  }
  const [, lo, hi] = JOLT_BAND[JOLT_BAND.length - 1];
  return (lo + hi) / 2;
}

function jumpPx(viewCm) {
  return (2 * viewCm * Math.tan((JUMP_DEG * Math.PI) / 360)) / CSS_PX_CM;
}

function roots(zeta) {
  if (zeta - 1 < CRITICAL_WITHIN) return null;
  const r = Math.sqrt(zeta * zeta - 1);
  return [zeta - r, zeta + r];
}

function landingShape(zeta) {
  if (!roots(zeta)) return { shape: (u) => u * Math.exp(-u), slope: (u) => (1 - u) * Math.exp(-u), peak: 1 };
  const [a, b] = roots(zeta);
  return {
    shape: (u) => (Math.exp(-a * u) - Math.exp(-b * u)) / (b - a),
    slope: (u) => (b * Math.exp(-b * u) - a * Math.exp(-a * u)) / (b - a),
    peak: Math.log(b / a) / (b - a),
  };
}

function bisect(before, lo, hi) {
  for (let k = 0; k < 100; k++) {
    const mid = (lo + hi) / 2;
    if (before(mid)) lo = mid;
    else hi = mid;
  }
  return hi;
}

function fallsTo(speed, still, from) {
  let hi = 2 * from;
  while (speed(hi) > still) hi *= 2;
  return bisect((u) => speed(u) > still, from, hi);
}

function arrivingLanding(zeta, still) {
  const landing = landingShape(zeta);
  const rest = settleShape(zeta);
  const aim = (e) => landing.shape(e) / (1 - rest(e));
  const arrivalSpeed = (e) => aim(e) * landing.shape(e) - landing.slope(e);
  const end = fallsTo(arrivalSpeed, still, landing.peak);
  const shape = (u) => landing.shape(u) - aim(end) * (1 - rest(u));
  const slope = (u) => landing.slope(u) - aim(end) * landing.shape(u);
  return { shape, slope, peak: bisect((u) => slope(u) > 0, 0, landing.peak), end };
}

const fallSeconds = (drop, scale) => Math.sqrt((2 * drop) / (G * scale));

function thud({ drop, scale }) {
  return { drop, scale, ms: fallSeconds(drop, scale) * 1000 };
}

function thudStray([x1, y1, x2, y2], drop, count) {
  const at = (a, b, s) => 3 * (1 - s) * (1 - s) * s * a + 3 * (1 - s) * s * s * b + s * s * s;
  let worst = 0;
  for (let k = 0; k <= count; k++) {
    const x = k / count;
    const s = bisect((u) => at(x1, x2, u) < x, 0, 1);
    worst = Math.max(worst, Math.abs(at(y1, y2, s) - x * x) * drop);
  }
  return worst;
}

function fall({ drop, scale, sink, damping = 1, tolerance = DEFAULT_TOLERANCE, viewCm = VIEW_CM }) {
  const g = G * scale;
  const fallS = fallSeconds(drop, scale);
  const impact = g * fallS;
  const still = Math.min(STILL_SHARE * impact, stillPx(viewCm));
  const { shape, slope, peak, end } = arrivingLanding(damping, still / impact);
  const omega = (impact * shape(peak)) / sink;
  const past = (s) => (impact / omega) * shape(omega * s);
  const landS = end / omega;
  const ms = (fallS + landS) * 1000;
  const position = (t) => {
    const s = Math.min(Math.max(t, 0), ms) / 1000;
    if (s <= fallS) return 0.5 * g * s * s;
    if (t >= ms) return drop;
    return drop + past(s - fallS);
  };
  const spanSpeed = (t) => (t <= fallS * 1000 ? (g * t) / 1000 : impact * Math.abs(slope(omega * (t / 1000 - fallS))));
  return { drop, scale, sink, damping, tolerance, viewCm, fallMs: fallS * 1000, landMs: landS * 1000, ms, impact, still, position, stops: stops(position, ms, [fallS * 1000], drop, tolerance, spanSpeed, still) };
}

function settleShape(zeta) {
  if (!roots(zeta)) return (u) => (1 + u) * Math.exp(-u);
  const [a, b] = roots(zeta);
  return (u) => (b * Math.exp(-a * u) - a * Math.exp(-b * u)) / (b - a);
}

function settle({ distance, ms, damping = 1, tolerance = DEFAULT_TOLERANCE, viewCm = VIEW_CM }) {
  if (!(distance > tolerance / 2)) throw new RangeError("--settle wants more than half the tolerance; a shorter one is already at rest");
  const rest = settleShape(damping);
  const { shape: speed, peak } = landingShape(damping);
  const pxSpeed = (end) => (u) => (distance / (1 - rest(end))) * (end / (ms / 1000)) * speed(u);
  let end = fallsTo(speed, STILL_SHARE * speed(peak), peak);
  if (pxSpeed(end)(end) > stillPx(viewCm)) end = fallsTo((u) => pxSpeed(u)(u), stillPx(viewCm), end);
  const omega = end / (ms / 1000);
  const aim = distance / (1 - rest(end));
  const endSpeed = speed(end);
  const position = (t) => (t >= ms ? distance : aim * (1 - rest((omega * Math.max(t, 0)) / 1000)));
  let top = 0;
  for (let t = 0; t < ms; t += FRAME_MS) top = Math.max(top, position(Math.min(t + FRAME_MS, ms)) - position(t));
  const startShare = position(Math.min(FRAME_MS, ms)) / top;
  const spanSpeed = (t) => speed((omega * t) / 1000);
  return { distance, damping, tolerance, viewCm, ms, omega, stiffness: omega * omega, aim, still: aim * omega * endSpeed, startShare, position, stops: stops(position, ms, [], distance, tolerance, spanSpeed, endSpeed) };
}

function stops(position, ms, joins, distance, tolerance, speed, still) {
  const close = (a, b) => {
    const pa = position(a);
    const pb = position(b);
    const speeds = [speed(a), speed(b)];
    for (let k = 1; k < CHORD_POINTS; k++) {
      const t = a + ((b - a) * k) / CHORD_POINTS;
      if (Math.abs(pa + ((pb - pa) * k) / CHORD_POINTS - position(t)) > tolerance) return false;
      speeds.push(speed(t));
    }
    if (b - a < SPEED_SPAN_MS || Math.max(...speeds) < still) return true;
    return Math.max(...speeds) <= SPAN_SPEED_RATIO * Math.min(...speeds);
  };
  const out = [];
  const split = (a, b) => {
    if (b - a < MIN_SPAN_MS || close(a, b)) out.push(b);
    else {
      split(a, (a + b) / 2);
      split((a + b) / 2, b);
    }
  };
  out.push(0);
  [0, ...joins].forEach((a, i, all) => split(a, i + 1 < all.length ? all[i + 1] : ms));
  return out.map((t) => ({ ms: t, progress: position(t) / distance }));
}

function css(result) {
  const parts = result.stops.map((s, i, all) => {
    const value = +s.progress.toFixed(PROGRESS_DECIMALS);
    if (i === 0 || i === all.length - 1) return `${value}`;
    return `${value} ${+((100 * s.ms) / result.ms).toFixed(TIME_DECIMALS)}%`;
  });
  return `linear(${parts.join(", ")})`;
}

module.exports = { fall, thud, thudStray, settle, css, joltLine, jumpPx, DEFAULT_TOLERANCE, VIEW_CM, FRAME_MS };
