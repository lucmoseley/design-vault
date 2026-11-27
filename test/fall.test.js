"use strict";
const assert = require("node:assert/strict");
const path = require("node:path");
const fs = require("node:fs");
const { test } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const SCRIPT = path.join(__dirname, "..", "plugin", "skills", "design-round", "scripts", "fall.js");
const { fall, settle, css } = require(path.join(__dirname, "..", "plugin", "skills", "design-round", "scripts", "fall-motion.js"));
const CHECK_FLOW = path.join(path.dirname(SCRIPT), "check-flow.py");
const FLOW = fs.readFileSync(CHECK_FLOW, "utf8");
const flowValue = (name) => FLOW.match(new RegExp(`^${name} = (.+)$`, "m"))[1];
const VIEW_CM = Number(flowValue("VIEW_CM"));
const stillPx = (cm) => Number(flowValue("STILL_ARCMIN_S")) / ((60 * 180 * Math.atan(2.54 / 96 / cm)) / Math.PI);
const STILL_FRACTION = Number(flowValue("STILL_FRACTION"));
const G = 9.80665;
const SPAN_SPEED_RATIO = 1.15;
const SPEED_SPAN_MS = 1;
const PROGRESS_DECIMALS = 6;
const TIME_DECIMALS = 4;

const DROP = { drop: 240, scale: 800, sink: 4 };

const cli = (...args) => runInProcess(SCRIPT, args);

function played(easing, ms, drop, t) {
  const parts = easing.slice("linear(".length, -1).split(", ").map((p) => p.split(" "));
  const pts = parts.map(([v, pct], i) => [pct ? (parseFloat(pct) / 100) * ms : i === 0 ? 0 : ms, Number(v)]);
  for (let i = 1; i < pts.length; i++) {
    const [ta, va] = pts[i - 1];
    const [tb, vb] = pts[i];
    if (t <= tb) return drop * (tb === ta ? vb : va + ((vb - va) * (t - ta)) / (tb - ta));
  }
  return drop * pts[pts.length - 1][1];
}

function chordAt(r, distance, t) {
  const i = Math.max(1, r.stops.findIndex((s) => s.ms >= t));
  const [a, b] = [r.stops[i - 1], r.stops[i]];
  return distance * (a.progress + ((b.progress - a.progress) * (t - a.ms)) / (b.ms - a.ms));
}

function rounding(r, distance) {
  let top = 0;
  for (let k = 0; k < 4000; k++) top = Math.max(top, Math.abs(r.position((r.ms * (k + 1)) / 4000) - r.position((r.ms * k) / 4000)) / (r.ms / 4000));
  return 0.5 * (10 ** -PROGRESS_DECIMALS * distance + 10 ** -(TIME_DECIMALS + 2) * r.ms * top);
}

test("the fall is y = ½gt² at the stated scale, from rest (#68)", () => {
  const r = fall(DROP);
  const g = G * DROP.scale;
  assert.ok(Math.abs(r.fallMs - 1000 * Math.sqrt((2 * DROP.drop) / g)) < 1e-9);
  assert.ok(Math.abs(r.position(r.fallMs / 2) - DROP.drop / 4) < 1e-9);
  assert.ok(Math.abs(r.impact - g * (r.fallMs / 1000)) < 1e-9);
});

for (const damping of [1, 1.5, 3]) {
  test(`the landing starts at the impact speed and sinks the depth asked for (damping ${damping})`, () => {
    const r = fall({ ...DROP, damping });
    const h = 1e-4;
    const before = (r.position(r.fallMs) - r.position(r.fallMs - h)) / (h / 1000);
    const after = (r.position(r.fallMs + h) - r.position(r.fallMs)) / (h / 1000);
    assert.ok(Math.abs(after - r.impact) / r.impact < 1e-3, `${after} vs ${r.impact}`);
    assert.ok(Math.abs(before - r.impact) / r.impact < 1e-3, `${before} vs ${r.impact}`);
    let deepest = 0;
    for (let t = r.fallMs; t <= r.ms; t += 0.01) deepest = Math.max(deepest, r.position(t) - DROP.drop);
    assert.ok(Math.abs(deepest - DROP.sink) < 1e-3, `${deepest}`);
  });

  test(`the landing arrives at rest as its speed falls to the still speed, with no still tail (damping ${damping}, #152, #196)`, () => {
    const r = fall({ ...DROP, damping });
    assert.ok(Math.abs(r.position(r.ms - 1e-9) - DROP.drop) < 1e-6, `${r.position(r.ms - 1e-9) - DROP.drop} px short`);
    assert.ok(Math.abs(r.still / Math.min(STILL_FRACTION * r.impact, stillPx(VIEW_CM)) - 1) < 1e-9, `${r.still}`);
    const end = -speedAt(r, r.ms - 1e-3) * 1000;
    assert.ok(Math.abs(end / r.still - 1) < 1e-3, `its last speed is ${end} px/s, not ${r.still}`);
    for (let t = r.fallMs + 1; t < r.ms - 1; t += 1) assert.ok(r.position(t) > DROP.drop, `back at rest early, at ${t} ms`);
  });
}

test("mmm-infra#35's stone with a 1 px sink lands inside mmm-infra#13's 1000 ms per move (#152)", () => {
  assert.ok(fall({ drop: 24, scale: 10, sink: 1 }).ms < 1000);
});

test("a heavier damping takes longer to settle from the same sink", () => {
  assert.ok(fall({ ...DROP, damping: 2 }).landMs > fall(DROP).landMs);
});

test("the linear() easing stays within the tolerance of the true path, and runs 0 to 1", () => {
  for (const opts of [DROP, { ...DROP, damping: 2 }, { drop: 30, scale: 3000, sink: 1, tolerance: 0.1 }]) {
    const r = fall(opts);
    const easing = css(r);
    assert.match(easing, /^linear\(0, .*, 1\)$/);
    let worst = 0;
    let rounded = 0;
    for (let k = 0; k <= 4000; k++) {
      const t = (r.ms * k) / 4000;
      worst = Math.max(worst, Math.abs(played(easing, r.ms, r.drop, t) - r.position(t)));
      rounded = Math.max(rounded, Math.abs(played(easing, r.ms, r.drop, t) - chordAt(r, r.drop, t)));
    }
    assert.ok(worst <= r.tolerance + rounding(r, r.drop), `${worst} px`);
    assert.ok(rounded <= rounding(r, r.drop), `rounding moved it ${rounded} px`);
  }
});

test("it refuses a missing drop, a zero sink and an underdamped landing, naming each", () => {
  const cases = [
    [["--scale", "800", "--sink", "4"], /--drop wants a number above 0/],
    [["--drop", "240", "--scale", "800", "--sink", "0"], /--sink wants a number above 0/],
    [["--drop", "240", "--scale", "800", "--sink", "4", "--damping", "0.5"], /--damping wants 1/],
    [["--scale", "800", "--sink", "4", "--drop"], /--drop <value>. argument missing/],
    [["--drop=240", "--scale", "800", "--sink", "4"], /--drop wants its value as the next argument, not after =/],
    [["--drop", "240", "--scale", "800", "--sink", "4", "--"], /-- is not taken/],
    [["--drop", "240", "--scale", "800", "--sink", "4", "--landing", "sink"], /--landing is taken with --check alone/],
  ];
  for (const [args, why] of cases) {
    const p = cli(...args);
    assert.equal(p.status, 2, args.join(" "));
    assert.match(p.stderr, why);
    assert.match(p.stderr, /usage: node fall.js/);
  }
});

test("--json prints the timings and the easing (#187)", () => {
  const p = cli("--drop", "240", "--scale", "800", "--sink", "4", "--json");
  assert.equal(p.status, 0);
  const r = JSON.parse(p.stdout);
  assert.equal(r.easing, css(fall(DROP)));
  assert.ok(Math.abs(r.ms - fall(DROP).ms) < 1e-9);
});

test("a landing shorter than a frame is called out as a stop", () => {
  assert.doesNotMatch(cli("--drop", "240", "--scale", "800", "--sink", "4").stdout, /warning/);
  assert.match(cli("--drop", "240", "--scale", "800", "--sink", "0.05").stdout, /warning: the landing is shorter than one 60 fps frame/);
});

const SETTLE = { distance: 300, ms: 900 };

function integrated({ aim, damping = 1 }, omega, t) {
  const h = 1e-5;
  let x = 0;
  let v = 0;
  const a = (x, v) => -omega * omega * (x - aim) - 2 * damping * omega * v;
  for (let s = 0; s < t / 1000 - h / 2; s += h) {
    const [k1x, k1v] = [v, a(x, v)];
    const [k2x, k2v] = [v + (h / 2) * k1v, a(x + (h / 2) * k1x, v + (h / 2) * k1v)];
    const [k3x, k3v] = [v + (h / 2) * k2v, a(x + (h / 2) * k2x, v + (h / 2) * k2v)];
    const [k4x, k4v] = [v + h * k3v, a(x + h * k3x, v + h * k3v)];
    x += (h / 6) * (k1x + 2 * k2x + 2 * k3x + k4x);
    v += (h / 6) * (k1v + 2 * k2v + 2 * k3v + k4v);
  }
  return x;
}

function speedAt(r, t) {
  const h = 1e-4;
  return (r.position(t + h) - r.position(t - h)) / (2 * h);
}

for (const damping of [1, 1.5, 3]) {
  test(`the settle is a spring released from rest that arrives at its length, its speed down to the still speed (damping ${damping})`, () => {
    const r = settle({ ...SETTLE, damping });
    assert.ok(Math.abs(r.stiffness - r.omega * r.omega) < 1e-9);
    assert.ok(r.aim > SETTLE.distance && r.aim < 1.01 * SETTLE.distance, `aimed at ${r.aim}`);
    for (const t of [50, 150, 400, 800]) {
      const want = integrated({ aim: r.aim, damping }, r.omega, t);
      assert.ok(Math.abs(r.position(t) - want) < 1e-6, `${t} ms: ${r.position(t)} vs ${want}`);
    }
    const h = 1e-4;
    assert.ok(r.position(h) / h < 1e-3 * (SETTLE.distance / SETTLE.ms), "it starts at rest");
    assert.ok(Math.abs(SETTLE.distance - r.position(SETTLE.ms - 1e-9)) < 1e-6);
    let top = 0;
    for (let t = 1; t < SETTLE.ms; t += 1) top = Math.max(top, speedAt(r, t));
    assert.ok(Math.abs(r.still / Math.min(STILL_FRACTION * top * 1000, stillPx(VIEW_CM)) - 1) < 1e-3, `it ends at ${r.still} px/s`);
    const end = speedAt(r, SETTLE.ms - 1e-3) * 1000;
    assert.ok(Math.abs(end / r.still - 1) < 1e-3, `its last speed is ${end} px/s, not ${r.still}`);
    let last = 0;
    for (let t = 0; t <= SETTLE.ms; t += 1) {
      assert.ok(r.position(t) >= last && r.position(t) <= SETTLE.distance, `${t} ms`);
      last = r.position(t);
    }
  });
}

test("the still floor these cases hold fall.js to is check-flow.py's own, 0.66 px/s from 60 cm (#142, #196)", () => {
  assert.equal(flowValue("CSS_PX_CM"), "2.54 / 96");
  assert.ok(Math.abs(stillPx(VIEW_CM) - 0.66) < 0.01, `${stillPx(VIEW_CM)}`);
});

test("a slow fall or settle ends at its still share, and a viewer farther off sees a fast one still sooner (#196)", () => {
  const slow = settle({ distance: 10, ms: 3000 });
  let top = 0;
  for (let t = 1; t < slow.ms; t += 1) top = Math.max(top, speedAt(slow, t));
  assert.ok(slow.still < stillPx(VIEW_CM));
  assert.ok(Math.abs(slow.still / (STILL_FRACTION * top * 1000) - 1) < 1e-3, `it ends at ${slow.still} px/s`);
  const gentle = fall({ drop: 24, scale: 3, sink: 1 });
  assert.ok(gentle.still < stillPx(VIEW_CM));
  assert.ok(Math.abs(gentle.still / (STILL_FRACTION * gentle.impact) - 1) < 1e-9, `${gentle.still}`);
  const near = settle(SETTLE);
  assert.ok(Math.abs(near.still / stillPx(VIEW_CM) - 1) < 1e-9, `${near.still}`);
  const far = settle({ ...SETTLE, viewCm: 2 * VIEW_CM });
  assert.ok(Math.abs(far.still / stillPx(2 * VIEW_CM) - 1) < 1e-9 && far.still > near.still);
  const p = cli("--settle", "300", "--ms", "900", "--view-cm", "120");
  assert.equal(p.status, 0);
  assert.match(p.stdout, /its speed down to 1\.3 px\/s/);
});

test(`a fall's and a settle's true speed changes at most ${SPAN_SPEED_RATIO}-fold across each span of ${SPEED_SPAN_MS} ms or more that is not still (#142, #151, #196)`, () => {
  const settles = [SETTLE, { ...SETTLE, damping: 2 }, { distance: 10, ms: 3000 }, { distance: 2400, ms: 5000 }].map(settle);
  const falls = [DROP, { ...DROP, damping: 2 }, { drop: 24, scale: 10, sink: 3 }, { drop: 2400, scale: 3, sink: 12 }].map(fall);
  for (const r of [...settles, ...falls]) {
    const name = r.drop ? `fall ${r.drop}/${r.scale}/${r.sink}/${r.damping}` : `settle ${r.distance}/${r.ms}/${r.damping}`;
    const speed = (t) => Math.abs(speedAt(r, Math.min(t, r.ms - 1e-3)));
    for (let i = 1; i < r.stops.length; i++) {
      const [a, b] = [r.stops[i - 1].ms, r.stops[i].ms];
      if (b - a < SPEED_SPAN_MS) continue;
      const v = Array.from({ length: 33 }, (_, k) => speed(a + ((b - a) * k) / 32));
      // guess, #151
      if (Math.max(...v) >= (r.still / 1000) * 1.01) assert.ok(Math.max(...v) <= SPAN_SPEED_RATIO * Math.min(...v) * 1.01, `${name}: ${a}–${b} ms`);
    }
  }
});

test("a settle's linear() easing stays within the tolerance of its closed form, and runs 0 to 1 (#105)", () => {
  for (const opts of [SETTLE, { ...SETTLE, damping: 2 }, { distance: 40, ms: 500, tolerance: 0.1 }, { distance: 1200, ms: 1600 }]) {
    const r = settle(opts);
    const easing = css(r);
    assert.match(easing, /^linear\(0, .*, 1\)$/);
    let worst = 0;
    let rounded = 0;
    for (let k = 0; k <= 4000; k++) {
      const t = (r.ms * k) / 4000;
      worst = Math.max(worst, Math.abs(played(easing, r.ms, r.distance, t) - r.position(t)));
      rounded = Math.max(rounded, Math.abs(played(easing, r.ms, r.distance, t) - chordAt(r, r.distance, t)));
    }
    assert.ok(worst <= r.tolerance + rounding(r, r.distance), `${worst} px`);
    assert.ok(rounded <= rounding(r, r.distance), `rounding moved it ${rounded} px`);
  }
});

test("a settle whose first frame would jolt or jump is called out; a heavy one is not (#297)", () => {
  assert.doesNotMatch(cli("--settle", "300", "--ms", "900").stdout, /warning/);
  const p = cli("--settle", "300", "--ms", "200");
  assert.equal(p.status, 0);
  assert.match(p.stdout, /warning: its first 60 fps frame runs at \d+ % of its top speed, over check-flow.py's jolt line of 80 % at 200 ms; raise --ms/);
  assert.match(p.stdout, /warning: its first 60 fps frame carries it \d+\.\d px, which check-flow.py flags as a jump; raise --ms or shorten --settle/);
  const far = cli("--settle", "1200", "--ms", "1200");
  assert.doesNotMatch(far.stdout, /jolt line/);
  assert.match(far.stdout, /flags as a jump/);
  assert.throws(() => settle({ distance: 0.005, ms: 900 }), /--settle wants more than half the tolerance/);
});

test("it refuses a settle with no length, a fall's flags, or one already at rest, naming each", () => {
  const cases = [
    [["--settle", "300"], /--ms wants a number above 0/],
    [["--settle", "300", "--ms", "900", "--sink", "4"], /--sink is not taken by a settle/],
    [["--drop", "240", "--scale", "800", "--sink", "4", "--ms", "900"], /--ms is not taken by a fall/],
    [["--settle", "0.005", "--ms", "900"], /--settle wants more than half the tolerance/],
    [["--settle", "300", "--ms", "900", "--damping", "0.5"], /under 1 the settle overshoots/],
  ];
  for (const [args, why] of cases) {
    const p = cli(...args);
    assert.equal(p.status, 2, args.join(" "));
    assert.match(p.stderr, why);
    assert.match(p.stderr, /--settle PX --ms MS/);
  }
});

test("--json prints a settle's spring and easing", () => {
  const p = cli("--settle", "300", "--ms", "900", "--json");
  assert.equal(p.status, 0);
  const r = JSON.parse(p.stdout);
  assert.equal(r.easing, css(settle(SETTLE)));
  assert.equal(r.ms, 900);
  assert.ok(Math.abs(r.stiffness - settle(SETTLE).stiffness) < 1e-9);
});
