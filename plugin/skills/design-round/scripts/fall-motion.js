/**
 * fall-motion.js — the motion maths fall.js prints (design-vault#68, #105): a fall
 * that ends in a damped landing, a heavy settle, and each sampled to the stops of a
 * CSS `linear()` easing. fall.js's header says what each motion is and promises.
 * It sits apart from fall.js so the tests call the maths the program calls (#187).
 */
"use strict";

const G = 9.80665;
// 0.25 left a fall's chord spans long enough to step at slow scales (#151). 0.02 was
// mmm-infra#35's working value; tuned on #151's grid, not derived.
const DEFAULT_TOLERANCE = 0.02;
// Each stop's progress and time, as a share of the length, are rounded to these
// many decimals: well under the tolerance on a 2400 px drop.
const PROGRESS_DECIMALS = 6;
const TIME_DECIMALS = 4;
// A damping this close to 1 takes the critical form: the overdamped one divides
// by the gap between its two roots, which vanishes there.
const CRITICAL_WITHIN = 1e-6;
// A span's chord is checked against the true path at this many points, and a
// span this short in ms is never split again.
const CHORD_POINTS = 32;
const MIN_SPAN_MS = 0.05;
// A span this short in ms is not split for its speed: check-flow.py's frames are
// never this close, and a span starting from rest, or at a landing's turn, never
// passes.
const SPEED_SPAN_MS = 1;
const FRAME_MS = 1000 / 60;
// check-flow.py's STILL_FRACTION, STILL_ARCMIN_S, VIEW_CM and CSS_PX_CM: a move is
// still below the lower of this share of its top speed and the slowest speed seen
// as motion from the viewer's distance (#196). test/fall.test.js holds them equal.
const STILL_SHARE = 0.01;
const STILL_ARCMIN_S = 1;
const VIEW_CM = 60;
const CSS_PX_CM = 2.54 / 96;
// check-flow.py calls a 1.3-fold change between held speeds a step (#196), and a
// played linear() span holds one speed. Each span keeps the true speed within
// this ratio, which left no step on #196's grid of settles of 5-2400 px over
// 400-5000 ms, and falls of 5-2400 px at 3-3000 px/m with sinks of 1-12 px, each
// at 30, 60 and 120 fps and four frame phases; 1.5 stepped in slow landings.
// That two neighbours stay under 1.3-fold is measured there, not guaranteed.
const SPAN_SPEED_RATIO = 1.15;
// check-flow.py's JOLT_BAND and JUMP_DEG, which test/check-flow.test.py holds
// equal: a move whose first frame runs at the middle of the band at its length,
// as a share of its top speed, starts with a jolt, and one whose first frame
// carries it JUMP_DEG of visual angle jumps (#297). Residual: checked at 60 fps
// only, so a settle sampled at 30 fps starts with a jolt it is not warned of
// (#132 Q3).
const JOLT_BAND = [
  [200, 0.8, 0.8],
  [250, 0.54, 0.67],
  [300, 0.43, 0.6],
  [500, 0.27, 0.47],
  [1000, 0.19, 0.39],
  [2000, 0.17, 0.35],
];
const JUMP_DEG = 0.26;

/** check-flow.py's still_px: STILL_ARCMIN_S in CSS px a second, seen from `viewCm`. */
function stillPx(viewCm) {
  return STILL_ARCMIN_S / ((60 * 180 * Math.atan(CSS_PX_CM / viewCm)) / Math.PI);
}

/** check-flow.py's jolt_line: the jolt line for a move of `ms`, or null. */
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

/** check-flow.py's jump_px: JUMP_DEG in CSS px, seen from `viewCm`. */
function jumpPx(viewCm) {
  return (2 * viewCm * Math.tan((JUMP_DEG * Math.PI) / 360)) / CSS_PX_CM;
}

/** The overdamped spring's two decay rates a < b, in units of ω; null at critical damping. */
function roots(zeta) {
  if (zeta - 1 < CRITICAL_WITHIN) return null;
  const r = Math.sqrt(zeta * zeta - 1);
  return [zeta - r, zeta + r];
}

/**
 * The landing's displacement past the rest point, for a spring that starts
 * there with speed v: `shape(u)` at time u, its `slope(u)`, and the `peak` u
 * where it sinks deepest, in units of v/ω, v and 1/ω.
 */
function landingShape(zeta) {
  if (!roots(zeta)) return { shape: (u) => u * Math.exp(-u), slope: (u) => (1 - u) * Math.exp(-u), peak: 1 };
  const [a, b] = roots(zeta);
  return {
    shape: (u) => (Math.exp(-a * u) - Math.exp(-b * u)) / (b - a),
    slope: (u) => (b * Math.exp(-b * u) - a * Math.exp(-a * u)) / (b - a),
    peak: Math.log(b / a) / (b - a),
  };
}

/** The u in (lo, hi) where `before(u)` turns false, by bisection; `before(lo)` holds and `before(hi)` does not. */
function bisect(before, lo, hi) {
  // 100 halvings outrun a double's 53-bit precision, so the interval ends as narrow as floats allow.
  for (let k = 0; k < 100; k++) {
    const mid = (lo + hi) / 2;
    if (before(mid)) lo = mid;
    else hi = mid;
  }
  return hi;
}

/** The u past `from` where `speed(u)`, falling from above `still` there, falls to `still`. */
function fallsTo(speed, still, from) {
  let hi = 2 * from;
  while (speed(hi) > still) hi *= 2;
  return bisect((u) => speed(u) > still, from, hi);
}

/**
 * The landing's displacement past the rest point, in units of v/ω at time u in
 * units of 1/ω, for a spring that starts there with speed v and is aimed just
 * past it on the way back, so that it arrives at rest as its speed falls to
 * `still` of v: `shape(u)`, its `slope(u)`, the `peak` u where it sinks
 * deepest, and the `end` u where it arrives (#152).
 */
function arrivingLanding(zeta, still) {
  const landing = landingShape(zeta);
  const rest = settleShape(zeta);
  // Aimed `aim(e)` past rest, it is back at rest at e: a spring's response to
  // its aim is a settle's, whose speed is the landing's shape.
  const aim = (e) => landing.shape(e) / (1 - rest(e));
  const arrivalSpeed = (e) => aim(e) * landing.shape(e) - landing.slope(e);
  const end = fallsTo(arrivalSpeed, still, landing.peak);
  const shape = (u) => landing.shape(u) - aim(end) * (1 - rest(u));
  const slope = (u) => landing.slope(u) - aim(end) * landing.shape(u);
  return { shape, slope, peak: bisect((u) => slope(u) > 0, 0, landing.peak), end };
}

/** The seconds a fall from rest takes over `drop` px at `scale` px/m: √(2 · drop / g). */
const fallSeconds = (drop, scale) => Math.sqrt((2 * drop) / (G * scale));

/** A thud: the fall alone, which stops dead where it hits, so its curve is t² over the fall's length. */
function thud({ drop, scale }) {
  return { drop, scale, ms: fallSeconds(drop, scale) * 1000 };
}

/**
 * The most px the `cubic-bezier(x1, y1, x2, y2)` of `points` strays from a fall's t² over `drop`,
 * at `count` evenly spaced points; `cubic-bezier(1/3, 0, 2/3, 1/3)` is t² exactly. x1 and x2 must lie in 0 to 1.
 */
function thudStray([x1, y1, x2, y2], drop, count) {
  const at = (a, b, s) => 3 * (1 - s) * (1 - s) * s * a + 3 * (1 - s) * s * s * b + s * s * s;
  let worst = 0;
  for (let k = 0; k <= count; k++) {
    const x = k / count;
    // The curve's own parameter where it reaches x: its x only rises while x1 and x2 lie in 0 to 1.
    const s = bisect((u) => at(x1, x2, u) < x, 0, 1);
    worst = Math.max(worst, Math.abs(at(y1, y2, s) - x * x) * drop);
  }
  return worst;
}

/**
 * The fall and landing for one drop. Returns its timings, speeds, the
 * position (in px from the start) at any time in ms, and the `linear()` stops.
 */
function fall({ drop, scale, sink, damping = 1, tolerance = DEFAULT_TOLERANCE, viewCm = VIEW_CM }) {
  const g = G * scale;
  const fallS = fallSeconds(drop, scale);
  const impact = g * fallS;
  const still = Math.min(STILL_SHARE * impact, stillPx(viewCm));
  const { shape, slope, peak, end } = arrivingLanding(damping, still / impact);
  // Sink depth = (impact / ω) · shape(peak), so ω follows from the sink asked for.
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

/**
 * The share of the distance a spring released from rest has still to go:
 * `rest(u)` at time u in units of 1/ω. It only falls, from 1 towards 0.
 */
function settleShape(zeta) {
  if (!roots(zeta)) return (u) => (1 + u) * Math.exp(-u);
  const [a, b] = roots(zeta);
  return (u) => (b * Math.exp(-a * u) - a * Math.exp(-b * u)) / (b - a);
}

/**
 * A heavy settle over `distance` px lasting `ms`. Returns ω, the stiffness per
 * unit mass (ω²), the px it is `aim`ed at, the position in px at any time in ms,
 * the `linear()` stops, and the share of its top speed its first 60 fps frame
 * runs at.
 */
function settle({ distance, ms, damping = 1, tolerance = DEFAULT_TOLERANCE, viewCm = VIEW_CM }) {
  if (!(distance > tolerance / 2)) throw new RangeError("--settle wants more than half the tolerance; a shorter one is already at rest");
  const rest = settleShape(damping);
  // A spring released from rest moves at the speed a landing sinks by, in units
  // of aim·ω: the derivative of the one is the other.
  const { shape: speed, peak } = landingShape(damping);
  // In px/s, ending at u: ω and the aim both follow from where it ends.
  const pxSpeed = (end) => (u) => (distance / (1 - rest(end))) * (end / (ms / 1000)) * speed(u);
  let end = fallsTo(speed, STILL_SHARE * speed(peak), peak);
  // Faster than the still floor there, it ends later, where it falls to the floor.
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

/**
 * Times in ms where the piecewise-linear path through them stays within
 * `tolerance` px of `position`: each span is halved until its chord is close
 * enough at every one of CHORD_POINTS points inside it, and until the true
 * `speed` at those points differs at most SPAN_SPEED_RATIO-fold, in any span of
 * SPEED_SPAN_MS or more that reaches the `still` speed. Each of `joins`, such as
 * a fall's impact, is always a stop.
 */
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
    // check-flow.py reads a slower span, such as one at a landing's turn, as
    // still, so it has no step.
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

/** The stops as a CSS `linear()` easing. */
function css(result) {
  const parts = result.stops.map((s, i, all) => {
    const value = +s.progress.toFixed(PROGRESS_DECIMALS);
    if (i === 0 || i === all.length - 1) return `${value}`;
    return `${value} ${+((100 * s.ms) / result.ms).toFixed(TIME_DECIMALS)}%`;
  });
  return `linear(${parts.join(", ")})`;
}

module.exports = { fall, thud, thudStray, settle, css, joltLine, jumpPx, DEFAULT_TOLERANCE, VIEW_CM, FRAME_MS };
