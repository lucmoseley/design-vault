"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { after, test } = require("node:test");
const { runInProcess } = require("./core-run-in-process.js");

const SCRIPT = path.join(__dirname, "..", "plugin", "skills", "design-round", "scripts", "check-curves.js");
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), "check-curves-"));
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

let files = 0;
function check(text) {
  const file = path.join(scratch, `${++files}.svg`);
  fs.writeFileSync(file, text);
  const r = runInProcess(SCRIPT, [file]);
  return { status: r.status, lines: r.stdout.trim().split("\n"), stderr: r.stderr };
}

function report(d) {
  const { status, lines } = check(`<svg><path d="${d}"/></svg>`);
  assert.ok(!lines.some((l) => l.includes("could not read the path")), lines.join("\n"));
  const runs = lines.flatMap((l) => [Number(l.match(/: (\d+) straight segments in a row bend like a curve/)?.[1])].filter(Boolean));
  const corners = lines.flatMap((l) => {
    const m = l.match(/the (?:curves|curve and straight line) meeting at \((\S+), (\S+)\) turn (\S+)° there/);
    return m ? [{ at: [Number(m[1]), Number(m[2])], angle: m[3] }] : [];
  });
  assert.equal(status, runs.length + corners.length ? 1 : 0, lines.join("\n"));
  return { runs, corners };
}
const findRuns = (d) => report(d).runs;
const findCorners = (d) => report(d).corners;

function polygonArc(n, r = 100) {
  const pts = [];
  for (let k = 0; k <= n; k++) {
    const a = Math.PI - (Math.PI * k) / n;
    pts.push(`${(r * Math.cos(a)).toFixed(3)} ${(-r * Math.sin(a)).toFixed(3)}`);
  }
  return `M${pts[0]} L${pts.slice(1).join(" ")}`;
}

test("lucmoseley/mmm-infra#16: a half circle traced as 30 straight lines is one breach", () => {
  assert.deepEqual(findRuns(polygonArc(30)), [30]);
});

test("the same half circle as an arc or a Bézier is clean", () => {
  assert.deepEqual(findRuns("M-100 0 A100 100 0 0 1 100 0"), []);
  assert.deepEqual(findRuns("M-100 0 C-100 -133 100 -133 100 0"), []);
});

test("a rectangle's 90° corners are not a curve", () => {
  assert.deepEqual(findRuns("M0 0 H100 V50 H0 Z"), []);
});

test("a straight line cut into pieces is not a curve", () => {
  assert.deepEqual(findRuns("M0 0 L10 0 L20 0 L30 0 L40 0 L50 0 L60 0"), []);
});

test("a zigzag whose turn changes sign is not a curve", () => {
  assert.deepEqual(findRuns("M0 0 L10 1 L20 0 L30 1 L40 0 L50 1 L60 0"), []);
});

test("fewer straight segments than the minimum run pass, the minimum fails", () => {
  const gentle = (n) => {
    let d = "M0 0";
    let a = 0;
    let x = 0;
    let y = 0;
    for (let k = 0; k < n; k++) {
      x += 10 * Math.cos(a);
      y += 10 * Math.sin(a);
      d += ` L${x.toFixed(4)} ${y.toFixed(4)}`;
      a += (10 * Math.PI) / 180;
    }
    return d;
  };
  assert.deepEqual(findRuns(gentle(3)), []);
  assert.equal(findRuns(gentle(4)).length, 1);
});

test("a turn sharper than 30° breaks the run", () => {
  assert.deepEqual(findRuns(polygonArc(4)), []);
});

test("relative commands and implicit linetos after a moveto are read", () => {
  const abs = polygonArc(12);
  const nums = abs.replace(/[ML]/g, " ").trim().split(/\s+/).map(Number);
  let rel = `m${nums[0]} ${nums[1]}`;
  for (let k = 2; k < nums.length; k += 2) rel += ` ${(nums[k] - nums[k - 2]).toFixed(3)} ${(nums[k + 1] - nums[k - 1]).toFixed(3)}`;
  assert.equal(findRuns(rel).length, 1);
});

test("a new subpath breaks a run", () => {
  const two = "M0 0 L10 0 L19.8 1.7 L29.2 5.1 M100 100 L109 104 L117 110";
  assert.deepEqual(findRuns(two), []);
});

test("arc flags written together are read as two numbers", () => {
  assert.deepEqual(report("M0 0a5 5 0 011 1"), { runs: [], corners: [] });
});

test("a polygon's points are checked like a path", () => {
  const pts = polygonArc(20).replace(/[ML]/g, " ").trim();
  const { status, lines } = check(`<svg><polygon id="arch" points="${pts}"/></svg>`);
  assert.equal(status, 1);
  assert.equal(lines.length, 1);
  assert.match(lines[0], /:1 <polygon id="arch">: 20 straight segments in a row bend like a curve, from \(-100, 0\); draw it as a Bézier or arc$/);
});

test("path data it cannot read is reported, not skipped", () => {
  const { status, lines } = check('<path d="M0 0 L10"/>');
  assert.equal(status, 1);
  assert.equal(lines.length, 1);
  assert.match(lines[0], /<path>: could not read the path: .*takes 2 numbers/);
});

test("it exits 1 on a breach, 0 on a clean file, 2 on a missing file or no file", () => {
  assert.equal(check(`<svg><path d="${polygonArc(30)}"/></svg>`).status, 1);
  const good = check('<svg><path d="M-100 0 A100 100 0 0 1 100 0"/></svg>');
  assert.equal(good.status, 0);
  assert.deepEqual(good.lines, ["no polygon curves, corners between curves or kinks between a curve and a line in 1 file(s)"]);
  const absent = runInProcess(SCRIPT, [path.join(scratch, "absent.svg")]);
  assert.equal(absent.status, 2);
  assert.match(absent.stderr, /absent\.svg: ENOENT/);
  const none = runInProcess(SCRIPT, []);
  assert.equal(none.status, 2);
  assert.match(none.stderr, /^usage: node check-curves\.js <file>/);
});

test("a morph between paths of one structure is curves at every key time; one through a polygon resample is not (#72)", () => {
  const from = "M 0 300 C 0 233 0 167 0 100 C 0 45 45 0 100 0 C 155 0 200 45 200 100 C 200 167 200 233 200 300 Z";
  const to = "M 0 300 C 0 283 0 267 0 250 C 0 167 67 100 150 100 C 233 100 300 167 300 250 C 300 267 300 283 300 300 Z";
  const [a, b] = [from.split(" "), to.split(" ")];
  const matched = (p) => a.map((x, i) => (isNaN(x) ? x : (+x + (b[i] - x) * p).toFixed(2))).join(" ");
  const resample = (d) => {
    const n = d.split(" ").filter((x) => !isNaN(x)).map(Number);
    const pts = [];
    for (let s = 2; s + 6 <= n.length; s += 6) {
      const [x0, y0, x1, y1, x2, y2, x3, y3] = n.slice(s - 2, s + 6);
      for (let k = 0; k < 24; k++) {
        const t = k / 24;
        const u = 1 - t;
        pts.push([u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3, u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3]);
      }
    }
    return pts;
  };
  const [pa, pb] = [resample(from), resample(to)];
  const polygon = (p) => {
    const pts = pa.map(([x, y], k) => `${(x + (pb[k][0] - x) * p).toFixed(2)} ${(y + (pb[k][1] - y) * p).toFixed(2)}`);
    return `M ${pts[0]} L ${pts.slice(1).join(" ")} Z`;
  };
  for (const p of [0, 0.25, 0.5, 0.75, 1]) {
    assert.deepEqual(findRuns(matched(p)), [], `matched at ${p}`);
    assert.deepEqual(findCorners(matched(p)), [], `matched at ${p}`);
    assert.notDeepEqual(findRuns(polygon(p)), [], `polygon at ${p}`);
  }
});

const CIRCLE = "M100 0 C100 55.228 55.228 100 0 100 C-55.228 100 -100 55.228 -100 0 C-100 -55.228 -55.228 -100 0 -100 C55.228 -100 100 -55.228 100 0 Z";

test("#195: a circle drawn as four cubics with collinear handles has no corner", () => {
  assert.deepEqual(findCorners(CIRCLE), []);
});

test("one handle 1 unit off its partner's line is a corner of about 1°, at that node", () => {
  const nudged = CIRCLE.replace("55.228 100 0 100", "55.228 101 0 100");
  const corners = findCorners(nudged);
  assert.equal(corners.length, 1);
  assert.deepEqual(corners[0].at, [0, 100]);
  assert.equal(corners[0].angle, ((Math.atan(1 / 55.228) * 180) / Math.PI).toPrecision(3));
});

test("a corner at the node a closepath returns to is found", () => {
  const nudged = CIRCLE.replace("M100 0 C100 55.228", "M100 0 C101 55.228");
  assert.deepEqual(findCorners(nudged).map((c) => c.at), [[100, 0]]);
});

test("a deliberate cusp between two curves, a pointed arch's apex, is reported", () => {
  const corners = findCorners("M0 100 C0 40 30 10 50 0 C70 10 100 40 100 100");
  assert.equal(corners.length, 1);
  assert.deepEqual(corners[0].at, [50, 0]);
});

test("two arcs joined smoothly pass, two arcs meeting in a point fail", () => {
  assert.deepEqual(findCorners("M-100 0 A100 100 0 0 1 100 0 A100 100 0 0 1 -100 0 Z"), []);
  assert.deepEqual(findCorners("M0 0 A50 50 0 0 1 50 50 A50 50 0 0 0 100 100"), []);
  const pointed = findCorners("M0 100 A100 100 0 0 1 50 13.397 A100 100 0 0 1 100 100");
  assert.equal(pointed.length, 1);
  assert.equal(pointed[0].angle, "60.0");
});

test("an arc's tangent is read from its radii and rotation, as a cubic standing in for it shows", () => {
  const phi = Math.PI / 6;
  const pt = (t) => [200 * Math.cos(t) * Math.cos(phi) - 100 * Math.sin(t) * Math.sin(phi), 200 * Math.cos(t) * Math.sin(phi) + 100 * Math.sin(t) * Math.cos(phi)];
  const dir = (t) => [-200 * Math.sin(t) * Math.cos(phi) - 100 * Math.cos(t) * Math.sin(phi), -200 * Math.sin(t) * Math.sin(phi) + 100 * Math.cos(t) * Math.cos(phi)];
  const [a, b] = [pt(0), pt(Math.PI / 2)];
  const h = dir(Math.PI / 2).map((v) => v * 0.3);
  const f = (v) => v.toFixed(6);
  const smooth = `M${f(a[0])} ${f(a[1])} A200 100 30 0 1 ${f(b[0])} ${f(b[1])} C${f(b[0] + h[0])} ${f(b[1] + h[1])} 0 300 50 300`;
  assert.deepEqual(findCorners(smooth), []);
  const turned = smooth.replace(/C\S+ \S+/, `C${f(b[0] + h[0] + 2)} ${f(b[1] + h[1])}`);
  assert.equal(findCorners(turned).length, 1);
});

test("S and T are smooth by construction; S after a line starts from its node", () => {
  assert.deepEqual(findCorners("M0 0 C10 20 30 20 40 0 S70 -20 80 0"), []);
  assert.deepEqual(findCorners("M0 0 Q20 30 40 0 T80 0"), []);
  assert.deepEqual(findCorners("M0 0 L40 0 S70 -20 80 0"), []);
  assert.equal(findCorners("M0 0 C10 20 30 20 40 0 Q50 30 80 0").length, 1);
});

const LETTER_D = "M0 0 H40 C95 0 95 100 40 100 H0 Z";

test("a curve meeting a straight line at a corner passes, as a D's bowl meeting its stem is meant", () => {
  assert.deepEqual(findCorners("M0 0 C80 0 80 100 0 100 Z"), []);
});

test("a curve meeting a straight line exactly along it passes", () => {
  assert.deepEqual(findCorners(LETTER_D), []);
});

test("#219: a curve meeting a straight line 2° off is a kink, at that node, whichever comes first", () => {
  assert.deepEqual(findCorners(LETTER_D.replace("C95 0", "C94.966 1.919")), [{ at: [40, 0], angle: "2.00" }]);
  assert.deepEqual(findCorners(LETTER_D.replace("95 100 40", "94.966 98.081 40")), [{ at: [40, 100], angle: "2.00" }]);
  assert.deepEqual(findCorners(LETTER_D.replace("H40 C95 0", "C10 0 30 0 40 0 C94.966 1.919")), [{ at: [40, 0], angle: "2.00" }]);
});

test("a curve meeting a straight line is a kink under FontBakery's 0.1 rad (5.7°), a corner over it", () => {
  assert.deepEqual(findCorners(LETTER_D.replace("C95 0", "C94.747 5.272")).map((c) => c.angle), ["5.50"]);
  assert.deepEqual(findCorners(LETTER_D.replace("C95 0", "C94.699 5.749")), []);
});

test("a break within Red Arrow's 0.49 grid units passes, the same break on a finer grid fails, a larger one fails", () => {
  assert.deepEqual(findCorners("M-40 10 C-30 5 -10 0 0 0 C30 1 35 0 40 0"), []);
  assert.equal(findCorners("M-40 10 C-30 5 -10 0 0 0 C30 1.000 35 0 40 0").length, 1);
  assert.equal(findCorners("M-40 10 C-30 5 -10 0 0 0 C30 2 35 0 40 0").length, 1);
});

test("an arc of no length is skipped, so it cannot hide the corner across it", () => {
  assert.equal(findCorners("M0 0 C10 20 30 20 40 0 A10 10 0 0 1 40 0 C50 20 70 -20 80 0").length, 1);
});

test("a cubic whose handles lie on its chord is a straight side, as a morph draws one, so its corners and tangent joins pass", () => {
  assert.deepEqual(findCorners("M 0 300 C 0 233 0 167 0 100 C 0 45 45 0 100 0 C 155 0 200 45 200 100 C 200 167 200 233 200 300 C 133 300 67 300 0 300 Z"), []);
});

test("a segment of no length is skipped, so the curves either side of it are compared", () => {
  assert.deepEqual(findCorners("M0 0 C10 20 30 20 40 0 L40 0 C50 -20 70 -20 80 0"), []);
  assert.equal(findCorners("M0 0 C10 20 30 20 40 0 L40 0 C50 20 70 -20 80 0").length, 1);
});

test("it prints a kink with its angle, the angle allowed and the angle a corner turns, and exits 1", () => {
  const { status, lines } = check(`<svg><path id="d" d="${LETTER_D.replace("C95 0", "C94.966 1.919")}"/></svg>`);
  assert.equal(status, 1);
  assert.equal(lines.length, 1);
  assert.match(lines[0], /<path id="d">: the curve and straight line meeting at \(40, 0\) turn 2\.00° there, past the [\d.e-]+° their written precision allows but under the 5\.7° a meant corner turns; put the curve's handle in line with the straight side, unless vault\.curves-script excuses the kink$/);
});

test("it prints a corner with its angle and the angle allowed, and exits 1", () => {
  const { status, lines } = check('<svg><path id="apex" d="M0 100 C0 40 30 10 50 0 C70 10 100 40 100 100"/></svg>');
  assert.equal(status, 1);
  assert.equal(lines.length, 1);
  assert.match(lines[0], /<path id="apex">: the curves meeting at \(50, 0\) turn 53\.1° there, past the [\d.]+° their written precision allows; put the handles either side of the node on one line, unless vault\.curves-script excuses the corner$/);
});

function bendsOf(...shapes) {
  const r = runInProcess(SCRIPT, ["--bends", "--json"], { stdin: JSON.stringify(shapes.map((s) => (typeof s === "string" ? { d: s } : s))) });
  assert.equal(r.status, 0, r.stderr);
  return JSON.parse(r.stdout);
}
const near = (got, want) => assert.ok(Math.abs(got - want) < 1e-3, `${got} is not ${want}`);

test("#228: the tightest bend of the parabola y = x² is its vertex, radius 0.5", () => {
  const [[b]] = bendsOf("M -10 100 Q 0 -100 10 100");
  near(b.at[0], 0);
  near(b.at[1], 0);
  near(b.radius, 0.5);
});

test("an arc's tightest bend is the end of its long axis, radius ry²/rx", () => {
  const [[b]] = bendsOf("M 0 -5 A 10 5 0 0 1 0 5");
  near(b.at[0], 10);
  near(b.at[1], 0);
  near(b.radius, 2.5);
});

test("a cubic's tightest bend is found off its ends and middle, where y = x³ bends hardest", () => {
  const [bends] = bendsOf("M -1 -1 C -0.333333333 1 0.333333333 -1 1 1");
  const x = (1 / 45) ** 0.25;
  near(Math.abs(bends[0].at[0]), x);
  near(Math.abs(bends[0].at[1]), x ** 3);
});

test("each subpath that curves has its own bend, and a corner of straight lines has none", () => {
  const [two, lines] = bendsOf("M0 0 C 0 10 10 10 10 0 M 50 0 A 5 5 0 0 0 60 0", "M0 0 L 10 0 L 10 10");
  assert.equal(two.length, 2);
  near(two[1].radius, 5);
  assert.deepEqual(lines, []);
});

test("a run of straight lines standing in for a curve is shot where it turns most", () => {
  const [[run]] = bendsOf({ points: "0,0 10,0 19.9,1 29.5,3.5 38,8 45,14", closed: false });
  assert.equal(run.segments, 5);
  assert.deepEqual(run.at, [29.5, 3.5]);
});

test("a stretched shape's bend is found as drawn: the parabola stretched 4x across turns hardest at its vertex, radius 8", () => {
  const [[b]] = bendsOf({ d: "M -10 100 Q 0 -100 10 100", matrix: [4, 0, 0, 1, 100, 50] });
  near(b.at[0], 100);
  near(b.at[1], 50);
  near(b.radius, 8);
});

test("--bends --json refuses anything but an array of shapes", () => {
  for (const stdin of ["not json", JSON.stringify(["M0 0"]), JSON.stringify({ d: "M0 0" })]) {
    const r = runInProcess(SCRIPT, ["--bends", "--json"], { stdin });
    assert.equal(r.status, 2, stdin);
    assert.match(r.stderr, /wants a JSON array of \{ d \} or \{ points, closed \} shapes/);
  }
});

test("--bends names a file it cannot read, and exits 1 on path data it cannot read", () => {
  const missing = runInProcess(SCRIPT, ["--bends", path.join(scratch, "none.svg")]);
  assert.equal(missing.status, 2);
  assert.match(missing.stderr, /none\.svg: ENOENT/);
  const file = path.join(scratch, "unreadable.svg");
  fs.writeFileSync(file, '<svg><path d="M0 0 X"/></svg>');
  const bad = runInProcess(SCRIPT, ["--bends", file]);
  assert.equal(bad.status, 1);
  assert.match(bad.stdout, /could not read the path: unknown path command 'X'/);
});

test("path data it cannot read comes back as an error, and the rest still answer", () => {
  const [bad, good] = bendsOf("M0 0 X", "M -10 100 Q 0 -100 10 100");
  assert.match(bad.error, /unknown path command 'X'/);
  near(good[0].radius, 0.5);
});

test("--bends on a file names each shape's tightest bend", () => {
  const file = path.join(scratch, "bends.svg");
  fs.writeFileSync(file, '<svg>\n<path id="p" d="M -10 100 Q 0 -100 10 100"/>\n</svg>');
  const r = runInProcess(SCRIPT, ["--bends", file]);
  assert.equal(r.status, 0, r.stderr);
  assert.equal(r.stdout.trim(), `${file}:2 <path id="p">: tightest bend at (0, 0), radius 0.5`);
});

test("a polygon curve that is not drawn where it stands, in <defs>, a comment or a <script> string, is not checked (#355)", () => {
  const pts = polygonArc(20).replace(/[ML]/g, " ").trim();
  const file = path.join(scratch, "hidden.html");
  fs.writeFileSync(file, `<!doctype html><html><head><script>const s = '<polygon points="${pts}"/>';</script></head><body>
<!-- <polygon points="${pts}"/> -->
<svg><defs><polygon points="${pts}"/></defs>
<polygon id="drawn" points="${pts}"/></svg></body></html>`);
  const r = runInProcess(SCRIPT, [file]);
  assert.equal(r.status, 1);
  assert.deepEqual(r.stdout.trim().split("\n").map((l) => l.match(/:(\d+) <polygon[^>]*>: 20 straight segments in a row/)?.[1]), ["4"]);
  const bends = runInProcess(SCRIPT, ["--bends", file]);
  assert.equal(bends.status, 0, bends.stdout);
  assert.deepEqual(bends.stdout.trim().split("\n").map((l) => l.match(/:(\d+) <polygon id="drawn">: 20 straight segments bend like a curve/)?.[1]), ["4"]);
});

test("a polygon curve in <defs>, a <symbol> or a <marker> is checked where a <use> or a url() draws it, by its own id or an ancestor's", () => {
  const pts = polygonArc(20).replace(/[ML]/g, " ").trim();
  const file = path.join(scratch, "used.svg");
  fs.writeFileSync(file, `<svg>
<symbol id="sprite"><polygon id="a" points="${pts}"/></symbol>
<marker id="tip"><polygon id="b" points="${pts}"/></marker>
<defs><polygon id="c" points="${pts}"/><polygon id="unused" points="${pts}"/></defs>
<use href="#sprite"/><use xlink:href="#c"/><path d="M0 0 H10" marker-end="url(#tip)"/>
<polygon id="last" points="${pts}"/></svg>`);
  const ids = (r) => r.stdout.trim().split("\n").map((l) => l.match(/<polygon id="(\w+)">: 20 straight segments/)?.[1]);
  const r = runInProcess(SCRIPT, [file]);
  assert.equal(r.status, 1);
  assert.deepEqual(ids(r), ["a", "b", "c", "last"]);
  assert.deepEqual(ids(runInProcess(SCRIPT, ["--bends", file])), ["a", "b", "c", "last"]);
  assert.deepEqual(contactsIn(`<defs>${A()}</defs>\n${B()}\n<use href="#a"/>`).found, []);
});

test("a transform it cannot read does not stop the default mode or --bends checking the path drawn through it", () => {
  const { status, lines } = check(`<svg><g transform="wobble(2)"><path d="${polygonArc(30)}"/></g></svg>`);
  assert.equal(status, 1);
  assert.match(lines[0], /: 30 straight segments in a row bend like a curve/);
  const file = path.join(scratch, "wobble.svg");
  fs.writeFileSync(file, '<svg><path transform="wobble(2)" d="M -10 100 Q 0 -100 10 100"/></svg>');
  const r = runInProcess(SCRIPT, ["--bends", file]);
  assert.equal(r.status, 0, r.stdout);
  assert.match(r.stdout, /tightest bend at \(0, 0\), radius 0\.5/);
});

const A = (right = 50) => `<path id="a" fill="#c00" d="M10 10 H${right} V50 H10 Z"/>`;
const B = (left = 50) => `<path id="b" fill="#00c" d="M${left} 10 H90 V50 H${left} Z"/>`;
const CONTACT = /^([\w.-]+)=(?:(.+)@)?(-?[\d.]+),(-?[\d.]+)$/;

function contactsIn(body, size = 'width="100" height="100" viewBox="0 0 100 100"') {
  const file = path.join(scratch, `${++files}.svg`);
  fs.writeFileSync(file, `<svg xmlns="http://www.w3.org/2000/svg" ${size}>\n${body}\n</svg>`);
  const r = runInProcess(SCRIPT, ["--contacts", file]);
  const lines = r.stdout.trim().split("\n");
  const found = lines.flatMap((l) => {
    const m = l.match(/ segment (\d+) and .+ segment (\d+): (.+?): .+ --contact '([^']*)'$/);
    return m ? [{ segments: [Number(m[1]), Number(m[2])], cls: m[3], contact: m[4] }] : [];
  });
  return { status: r.status, lines, found, stderr: r.stderr };
}
const classes = (r) => r.found.map((c) => c.cls);

test("#331: two fills that meet on one exact edge fail as the conflation seam", () => {
  const r = contactsIn(`${A()}\n${B()}`);
  assert.deepEqual(r.found.map((c) => [c.cls, c.segments]), [["shared edge, no underlap", [2, 4]]]);
  assert.equal(r.status, 1);
  assert.match(r.lines[0], /:2 <path id="a"> segment 2 and .+:3 <path id="b"> segment 4: shared edge, no underlap: .+make them one path, or run one on under the other\./);
});

test("two fills a unit apart are separate and fail, the gap's width printed", () => {
  const r = contactsIn(`${A()}\n${B(51)}`);
  assert.deepEqual(classes(r), ["separate"]);
  assert.equal(r.status, 1);
  assert.match(r.lines[0], /separate: the edges run 1 px apart and never meet, so the ground shows between them; draw both sides from one shared curve, and run one fill on under the other\./);
});

test("a fill run on a unit past the edge, under the other, is an underlap and passes", () => {
  const r = contactsIn(`${A(51)}\n${B()}`);
  assert.deepEqual(classes(r), ["coincident", "underlap", "coincident"]);
  assert.equal(r.status, 0);
  assert.match(r.lines.at(-1), /^3 contact\(s\) in 1 file\(s\), 0 failing$/);
});

test("the upper fill run on over the lower passes too, since the ground never shows", () => {
  const r = contactsIn(`${A()}\n${B(49)}`);
  assert.ok(classes(r).includes("underlap"), r.lines.join("\n"));
  assert.equal(r.status, 0, r.lines.join("\n"));
});

test("edges that match with both fills on one side are coincident and pass, listed for the look renders", () => {
  const r = contactsIn(`${A()}\n<path id="shine" fill="#fff" d="M30 10 H50 V30 H30 Z"/>`);
  assert.deepEqual(r.found.map((c) => [c.cls, c.segments]), [["coincident", [1, 1]], ["coincident", [2, 2]]]);
  assert.equal(r.status, 0);
});

test("an arch both shapes share, the upper drawing it backwards, is a seam; shifted a unit into the lower, an underlap", () => {
  const ground = '<path fill="#c00" d="M10 90 L10 50 C30 40 70 40 90 50 L90 90 Z"/>';
  const sky = (dy) => `<path id="sky" fill="#0c0" d="M90 ${50 + dy} C70 ${40 + dy} 30 ${40 + dy} 10 ${50 + dy} L10 5 L90 5 Z"/>`;
  assert.deepEqual(classes(contactsIn(`${ground}\n${sky(0)}`)), ["shared edge, no underlap"]);
  const r = contactsIn(`${ground}\n${sky(1)}`);
  assert.deepEqual([...new Set(classes(r))].sort(), ["coincident", "underlap"], r.lines.join("\n"));
  assert.equal(r.status, 0);
});

test("two circles that only kiss are separate: the ground shows either side of the kiss", () => {
  const r = contactsIn('<circle cx="50" cy="50" r="40" fill="#c00"/>\n<circle cx="130" cy="50" r="40" fill="#00c"/>', 'width="200" height="100"');
  assert.deepEqual([...new Set(classes(r))], ["separate"]);
  assert.equal(r.status, 1);
});

test("the 2 px is measured at the drawn size: a unit's gap drawn 4x is not listed, drawn at 1x or 1.9x it is", () => {
  const gap = `${A()}\n${B(51)}`;
  assert.deepEqual(classes(contactsIn(gap, 'width="400" height="400" viewBox="0 0 100 100"')), []);
  assert.deepEqual(classes(contactsIn(`<g transform="scale(4)">${gap}</g>`, 'width="400" height="400"')), []);
  assert.deepEqual(classes(contactsIn(`<g transform="scale(0.25)"><g transform="scale(4)">${gap}</g></g>`, 'width="400" height="400" viewBox="0 0 100 100"')), []);
  assert.deepEqual(classes(contactsIn(gap)), ["separate"]);
  assert.deepEqual(classes(contactsIn(gap, 'width="190" height="190" viewBox="0 0 100 100"')), ["separate"]);
});

test("shapes that meet only at a corner, or end to end on one line, are not a contact", () => {
  const r = contactsIn('<path fill="#c00" d="M10 10 H50 V50 H10 Z"/>\n<path fill="#00c" d="M50 50 H90 V90 H50 Z"/>');
  assert.deepEqual(r.found, []);
  assert.equal(r.status, 0);
  assert.match(r.lines[0], /^no two shapes come within 2 px of each other along an edge in 1 file\(s\)$/);
});

test("one path's own subpaths are not two shapes, and a shape that is not drawn where it stands is not read", () => {
  assert.deepEqual(contactsIn('<path d="M10 10 H50 V50 H10 Z M50 10 H90 V50 H50 Z"/>').found, []);
  for (const hidden of ["<defs>", "<clipPath id='c'>", "<mask id='m'>", "<symbol id='s'>"]) {
    const close = hidden.match(/<(\w+)/)[1];
    assert.deepEqual(contactsIn(`${A()}\n${hidden}${B()}</${close}>`).found, [], hidden);
  }
  assert.deepEqual(contactsIn(`${A()}\n<path display="none" d="M50 10 H90 V50 H50 Z"/>`).found, []);
});

test("the fill rule decides a seam: a square in an even-odd ring's hole meets it on one edge, in a nonzero ring it is lapped", () => {
  const ring = (rule) => `<path fill-rule="${rule}" fill="#c00" d="M10 10 H90 V90 H10 Z M30 30 H70 V70 H30 Z"/>`;
  const plug = '<path fill="#00c" d="M30 30 H70 V70 H30 Z"/>';
  const kinds = (body) => [...new Set(classes(contactsIn(body)))];
  assert.deepEqual(kinds(`${ring("evenodd")}\n${plug}`), ["shared edge, no underlap"]);
  assert.deepEqual(kinds(`${ring("nonzero")}\n${plug}`), ["underlap"]);
  assert.deepEqual(kinds(`<g fill-rule="evenodd">${ring("inherit")}</g>\n${plug}`), ["shared edge, no underlap"]);
  assert.deepEqual(kinds(`${ring("nonzero").replace("<path", '<path style="fill-rule: evenodd"')}\n${plug}`), ["shared edge, no underlap"]);
});

test("a shape with no fill is read at its line alone: on an edge it is coincident, a unit off it separate", () => {
  const line = (x) => `<path fill="none" stroke="#000" d="M${x} 10 V50"/>`;
  assert.deepEqual(classes(contactsIn(`${A()}\n${line(50)}`)), ["coincident"]);
  assert.deepEqual(classes(contactsIn(`${A()}\n${line(51)}`)), ["separate"]);
  assert.deepEqual(classes(contactsIn(`<g fill="none"><path d="M10 10 H50 V50 H10 Z"/></g>\n${B()}`)), ["coincident"]);
});

test("a contact prints as a --contact look-renders.py takes: the upper shape's selector and the meeting point in its user units", () => {
  const r = contactsIn(`${A()}\n<g transform="translate(60 0)"><path transform="scale(0.5)" fill="#00c" d="M-20 20 H60 V100 H-20 Z"/></g>`);
  assert.equal(r.found.length, 1, r.lines.join("\n"));
  const [, name, selector, x, y] = r.found[0].contact.match(CONTACT);
  assert.equal(name, "a.2-path2.4");
  assert.equal(selector, ":root>g:nth-of-type(1)>path:nth-of-type(1)");
  assert.equal(Number(x), -20);
  assert.ok(Number(y) > 20 && Number(y) < 100, y);
  const ids = contactsIn(`${A()}\n<g id="right"><g><path fill="#00c" d="M50 10 H90 V50 H50 Z"/></g></g>`);
  assert.match(ids.found[0].contact, /^a\.2-path2\.4=#right>g:nth-of-type\(1\)>path:nth-of-type\(1\)@50,/);
  assert.match(contactsIn(`${A()}\n${B()}`).found[0].contact, /^a\.2-b\.4=#b@50,[\d.]+$/);
});

test("each contact between the same two shapes has its own name", () => {
  const r = contactsIn(`${A()}\n<path id="b" fill="#00c" d="M50 10 H90 V50 H50 V30 Z"/>`);
  assert.deepEqual(r.found.map((c) => c.contact.match(CONTACT)[1]), ["a.2-b.4", "a.2-b.5"]);
  const short = contactsIn(`${A()}\n<path id="b" fill="#00c" d="M50 10 H90 V50 H50 V30.1 V30 Z"/>`);
  assert.deepEqual(short.found.map((c) => c.contact.match(CONTACT)[1]), ["a.2-b.4", "a.2-b.5", "a.2-b.6"]);
});

test("a shape it cannot read is named and exits 6, unless another contact fails", () => {
  const unread = contactsIn(`${A()}\n<path d="M50 10 L90"/>\n<rect x="50" y="10" width="40" height="forty"/>`);
  assert.equal(unread.status, 6);
  assert.match(unread.lines[0], /:3 <path>: could not read the shape, so its contacts are not measured: 'L' takes 2 numbers per segment, got 1; judge them under vault\.contacts-code$/);
  assert.match(unread.lines[1], /:4 <rect>: could not read the shape, so its contacts are not measured: unreadable height 'forty'; judge them under vault\.contacts-code$/);
  assert.equal(contactsIn(`${A()}\n${B()}\n<path d="M0 0 L90"/>`).status, 1);
  for (const transform of ["rotate(oops)", "translate(5) wobble(2)"]) {
    const r = contactsIn(`${A()}\n<path transform="${transform}" d="M50 10 H90 V50 H50 Z"/>`);
    assert.equal(r.status, 6, transform);
    assert.ok(r.lines[0].endsWith(`:3 <path>: could not read the shape, so its contacts are not measured: unreadable transform '${transform}'; judge them under vault.contacts-code`), r.lines[0]);
  }
});

test("an <svg> sized by CSS is read at its user units, with a note saying so", () => {
  const r = contactsIn(`${A()}\n${B(51)}`, 'viewBox="0 0 100 100"');
  assert.match(r.lines[0], /:1 <svg> gives no width and height in px, so its user units are read as CSS px$/);
  assert.deepEqual(classes(r), ["separate"]);
});

test("--contacts with no file, or a file it cannot read, is bad usage", () => {
  const none = runInProcess(SCRIPT, ["--contacts"]);
  assert.equal(none.status, 2);
  assert.match(none.stderr, /^usage: node check-curves\.js --contacts \[--json\] <file>/);
  const typo = runInProcess(SCRIPT, ["--contacts", "--jsn", path.join(scratch, "none.svg")]);
  assert.equal(typo.status, 2);
  assert.match(typo.stderr, /^check-curves\.js: Unknown option '--jsn'/);
  const missing = runInProcess(SCRIPT, ["--contacts", path.join(scratch, "none.svg")]);
  assert.equal(missing.status, 2);
  assert.match(missing.stderr, /none\.svg: ENOENT/);
});

test("--contacts --json gives each contact's two shapes, its point and a point 1 CSS px on along its edge, the flag read before or after the files", () => {
  const file = path.join(scratch, "json.svg");
  fs.writeFileSync(file, `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 100 50"><path id="a" d="M5 5 H25 V45 H5 Z"/><path id="b" d="M25.5 5 H45 V45 H25.5 Z"/></svg>`);
  for (const args of [["--contacts", "--json", file], ["--contacts", file, "--json"]]) {
    const r = runInProcess(SCRIPT, args);
    assert.equal(r.status, 1, r.stderr);
    const { notes, unread, contacts } = JSON.parse(r.stdout);
    assert.deepEqual([notes, unread], [[], []]);
    assert.equal(contacts.length, 1);
    const [c] = contacts;
    assert.deepEqual([c.cls, c.lower, c.upper], ["separate", "#a", "#b"]);
    assert.equal(Math.hypot(c.along[0] - c.at[0], c.along[1] - c.at[1]), 0.5);
    assert.equal(Math.abs(c.along[0] - c.at[0]), 0, "along runs down the vertical edge");
    assert.equal(c.word, `${c.name}=#b@${c.at.join(",")}`);
  }
});

test("a saved page's shapes are read past its script and style text, its void tags and its comments", () => {
  const file = path.join(scratch, "page.html");
  fs.writeFileSync(file, `<!doctype html><html><head><meta charset="utf-8"><style>/* <path d="M0 0"> */</style>
<script>if (1 < 2) document.title = "<svg>";</script></head><body><br><img src="x.png"><!-- a > b <path d="M1 1 H5"/> -->
<div><svg width="100" height="100">${A()}<path fill="#00c" d="M51 10 H90 V50 H51 Z"/></svg></div></body></html>`);
  const r = runInProcess(SCRIPT, ["--contacts", file]);
  assert.equal(r.status, 1, r.stdout);
  const selector = ":root>body:nth-of-type(1)>div:nth-of-type(1)>svg:nth-of-type(1)>path:nth-of-type(2)";
  assert.ok(r.stdout.includes(`: separate: `) && r.stdout.includes(` --contact 'a.2-path2.4=${selector}@50.5,`), r.stdout);
});

test("shapes in two <svg>s on one page are not compared: the page, not the file, places each <svg>", () => {
  const file = path.join(scratch, "two-svgs.html");
  const svg = (body) => `<svg width="100" height="100">${body}</svg>`;
  fs.writeFileSync(file, `<!doctype html><html><body>${svg(A())}${svg(B(51))}</body></html>`);
  const r = runInProcess(SCRIPT, ["--contacts", file]);
  assert.equal(r.status, 0, r.stdout);
  assert.match(r.stdout, /^no two shapes come within 2 px/);
});

test("fills either side of edges the precision cannot part are judged by what is drawn: 0.4 px over, or 0.4 px apart", () => {
  const over = '<path id="a" fill="#c00" d="M10.0 10.0 H50.4 V50.0 H10.0 Z"/>';
  const under = contactsIn(`${over}\n${B()}`);
  assert.deepEqual(classes(under), ["coincident", "underlap", "coincident"]);
  assert.equal(under.status, 0);
  const apart = '<path id="b" fill="#00c" d="M50.4 10.0 H90.0 V50.0 H50.4 Z"/>';
  const r = contactsIn(`${A()}\n${apart}`);
  assert.deepEqual(classes(r), ["separate"]);
  assert.equal(r.status, 1);
});

test("edges a hair apart agree within the coarser path's written precision: coincident, unless both are written finer", () => {
  const shine = '<path id="shine" fill="#fff" d="M30 10 H49.7 V30 H30 Z"/>';
  assert.deepEqual(classes(contactsIn(`${A()}\n${shine}`)), ["coincident", "coincident"]);
  const fine = '<path id="a" fill="#c00" d="M10.0 10.0 H50.0 V50.0 H10.0 Z"/>';
  assert.deepEqual(classes(contactsIn(`${fine}\n${shine}`)), ["coincident", "underlap"]);
});

test("an open subpath's fill closes with a straight line, and that line is an edge too", () => {
  const r = contactsIn(`${A()}\n<path id="b" fill="#00c" d="M50 10 H90 V50 H50"/>`);
  assert.deepEqual(r.found.map((c) => [c.cls, c.segments]), [["shared edge, no underlap", [2, 4]]]);
});

test("a viewBox is fitted as preserveAspectRatio says: met, a unit is 1 px; stretched with none, 4 px across", () => {
  const gap = `${A()}\n${B(51)}`;
  assert.deepEqual(classes(contactsIn(gap, 'width="400" height="100" viewBox="0 0 100 100"')), ["separate"]);
  assert.deepEqual(classes(contactsIn(gap, 'width="400" height="100" viewBox="0 0 100 100" preserveAspectRatio="none"')), []);
  assert.deepEqual(classes(contactsIn(gap, 'width="400" height="100" viewBox="0 0 100 100" preserveAspectRatio="xMinYMin slice"')), []);
});

test("a square standing a unit deep in a wider one is an underlap; its sides, crossing the wider one's top square on, are not contacts", () => {
  const r = contactsIn('<path fill="#c00" d="M10 50 H90 V90 H10 Z"/>\n<path id="post" fill="#00c" d="M30 10 H70 V51 H30 Z"/>');
  assert.deepEqual(r.found.map((c) => [c.cls, c.segments]), [["underlap", [1, 3]]]);
  const lean = contactsIn('<path fill="#c00" d="M10 50 H90 V90 H10 Z"/>\n<path id="post" fill="#00c" d="M30 10 H70 L84.92 51 L15.08 51 Z"/>');
  assert.deepEqual(lean.found.map((c) => c.segments), [[1, 3]]);
});

const STRIP = (attrs = "") => `<path id="strip" fill="#0c0"${attrs} d="M48 10 H52 V50 H48 Z"/>`;
const gapClass = (r) => r.found.find((c) => c.contact.startsWith("a.2-b.4="))?.cls;

test("#356: a gap a shape painted after both fills is covered and passes, its line naming the cover", () => {
  const r = contactsIn(`${A(49)}\n${B(51)}\n${STRIP()}`);
  assert.equal(gapClass(r), "covered", r.lines.join("\n"));
  assert.match(r.lines.find((l) => l.includes(": covered: ")), /: covered: the edges run 2 px apart, but \S+:4 <path id="strip">, painted over both, fills the gap\. --contact 'a\.2-b\.4=#b@/);
  assert.equal(r.status, 0, r.lines.join("\n"));
});

test("a gap over a shape painted before both, or between them, still fails as separate, naming no cover", () => {
  for (const body of [`${STRIP()}\n${A(49)}\n${B(51)}`, `${A(49)}\n${STRIP()}\n${B(51)}`]) {
    const r = contactsIn(body);
    assert.equal(gapClass(r), "separate", r.lines.join("\n"));
    assert.equal(r.status, 1);
    assert.ok(!r.lines.some((l) => l.includes("painted over both")), r.lines.join("\n"));
  }
});

function assertUncovered(cover) {
  const r = contactsIn(`${A(49)}\n${B(51)}\n${cover}`);
  assert.equal(gapClass(r), "separate", cover);
  assert.equal(r.status, 1, cover);
  assert.ok(r.lines.some((l) => /: separate: .+draw both sides from one shared curve.+--contact 'a\.2-b\.4=/.test(l)), cover);
}

test("a translucent shape over the gap does not cover it, nor does one that fills only its middle", () => {
  for (const cover of [STRIP(' opacity="0.5"'), STRIP(' style="fill-opacity: 50%"'), `<g opacity=".9">${STRIP()}</g>`, `<g fill-opacity="0.5">${STRIP()}</g>`]) assertUncovered(cover);
  assert.equal(gapClass(contactsIn(`${A(49)}\n${B(51)}\n${STRIP(' opacity="1" fill-opacity="100%"')}`)), "covered");
  assertUncovered('<path id="strip" fill="#0c0" d="M49.5 10 H50.5 V50 H49.5 Z"/>');
});

test("a shape hidden by visibility, or clipped or masked, does not cover the gap; one set visible again in a hidden group does", () => {
  const clip = '<defs><clipPath id="k"><rect width="1" height="1"/></clipPath><mask id="n"><rect width="1" height="1" fill="#fff"/></mask></defs>';
  for (const cover of [STRIP(' visibility="hidden"'), STRIP(' style="visibility: collapse"'), `<g visibility="hidden">${STRIP()}</g>`, `${clip}${STRIP(' clip-path="url(#k)"')}`, `${clip}<g mask="url(#n)">${STRIP()}</g>`]) {
    assertUncovered(cover);
  }
  assert.equal(gapClass(contactsIn(`${A(49)}\n${B(51)}\n<g visibility="hidden">${STRIP(' visibility="visible"')}</g>`)), "covered");
  assert.equal(gapClass(contactsIn(`${A(49)}\n${B(51)}\n${STRIP(' clip-path="none"')}`)), "covered");
});

test("a shape in another <svg> on the page does not cover a gap, since the page, not the file, places it", () => {
  const file = path.join(scratch, "cover-elsewhere.html");
  fs.writeFileSync(file, `<!doctype html><html><body><svg width="100" height="100">${A(49)}${B(51)}</svg><svg width="100" height="100">${STRIP()}</svg></body></html>`);
  const r = runInProcess(SCRIPT, ["--contacts", file]);
  assert.equal(r.status, 1, r.stdout);
  assert.match(r.stdout, /: separate: .+--contact 'a\.2-b\.4=/);
});

test("--contacts names each shape in a group whose transform it cannot read as unread, rather than measuring it through the wrong map", () => {
  const r = contactsIn(`${A()}\n<g transform="wobble(2)">${B(51)}</g>`);
  assert.equal(r.status, 6, r.lines.join("\n"));
  assert.match(r.lines[0], /:3 <path id="b">: could not read the shape, so its contacts are not measured: unreadable transform 'wobble\(2\)'/);
});

function assertUnproved(body, why, prefix = "") {
  const r = contactsIn(`${prefix}${A(49)}\n${B(51)}\n${body}`);
  assert.equal(gapClass(r), "covered", body);
  assert.equal(r.status, 6, `${body}\n${r.lines.join("\n")}`);
  const line = r.lines.find((l) => l.includes(": covered: "));
  assert.match(line, /would fill the gap, but its paint is not proved opaque \(.+\), so the gap is not measured; judge it under vault\.contacts-code\. --contact /, body);
  assert.ok(line.includes(why), `${why}\n${line}`);
  assert.match(r.lines.at(-1), /, 0 failing, \d+ not measured$/);
}

test("#541: a cover whose fill colour carries alpha lets the ground through: the gap fails as separate, naming the alpha", () => {
  for (const fill of ["#0c08", "#00cc0080", "rgba(0, 204, 0, 0.5)", "rgb(0 204 0 / 50%)", "hsla(120, 100%, 40%, .5)", "oklch(0.7 0.2 140 / 0.5)", "transparent"]) {
    assertUncovered(`<path id="strip" fill="${fill}" d="M48 10 H52 V50 H48 Z"/>`);
  }
  const r = contactsIn(`${A(49)}\n${B(51)}\n<path id="strip" style="fill: rgba(0,204,0,0.5)" d="M48 10 H52 V50 H48 Z"/>`);
  assert.match(r.lines.find((l) => l.includes("a.2-b.4=")), /<path id="strip">, painted over both, lets the ground through \(fill rgba\(0,204,0,0\.5\), of alpha 0\.5\)/);
  assertUncovered('<g color="rgba(0,0,0,0.5)"><path id="strip" fill="currentColor" d="M48 10 H52 V50 H48 Z"/></g>');
  for (const fill of ["#0c0", "#00cc00ff", "rgb(0, 204, 0)", "rgba(0, 204, 0, 1)", "hsl(120 100% 40% / 100%)", "green", "currentColor"]) {
    const ok = contactsIn(`${A(49)}\n${B(51)}\n<path id="strip" fill="${fill}" d="M48 10 H52 V50 H48 Z"/>`);
    assert.equal(gapClass(ok), "covered", fill);
    assert.equal(ok.status, 0, `${fill}\n${ok.lines.join("\n")}`);
  }
});

test("#541: a gradient cover passes only where every stop it paints with is opaque, its own or the ones its href lends it", () => {
  const strip = (id) => `<path id="strip" fill="url(#${id})" d="M48 10 H52 V50 H48 Z"/>`;
  const defs = `<defs><linearGradient id="solid"><stop offset="0" stop-color="#0c0"/><stop offset="1" stop-color="rgb(0 0 200)"/></linearGradient>
<linearGradient id="fade"><stop offset="0" stop-color="#0c0"/><stop offset="1" stop-color="#0c0" stop-opacity="0.5"/></linearGradient>
<radialGradient id="lent" href="#fade"/><radialGradient id="lentSolid" xlink:href="#solid"/><linearGradient id="empty"/></defs>`;
  for (const id of ["solid", "lentSolid"]) assert.equal(contactsIn(`${A(49)}\n${B(51)}\n${defs}${strip(id)}`).status, 0, id);
  for (const id of ["fade", "lent", "empty"]) assertUncovered(`${defs}${strip(id)}`);
  assertUnproved(`<defs><pattern id="dots"><rect width="1" height="1"/></pattern></defs>${strip("dots")}`, "a pattern, which it does not read");
  assertUnproved(strip("nowhere"), "which names no paint server in the file");
  assertUnproved(`<defs><pattern id="p"><rect width="1" height="1"/></pattern><linearGradient id="viaPattern" href="#p"/></defs>${strip("viaPattern")}`, "a gradient whose href #p names no gradient in the file");
});

test("#541: a cover that sets a blend mode, on it or an ancestor, lets the ground through; mix-blend-mode normal does not", () => {
  for (const cover of [STRIP(' mix-blend-mode="multiply"'), `<g style="mix-blend-mode: screen">${STRIP()}</g>`]) assertUncovered(cover);
  const r = contactsIn(`${A(49)}\n${B(51)}\n${STRIP(' style="mix-blend-mode: multiply"')}`);
  assert.match(r.lines.find((l) => l.includes("a.2-b.4=")), /lets the ground through \(mix-blend-mode multiply on line 4\)/);
  assert.equal(gapClass(contactsIn(`${A(49)}\n${B(51)}\n${STRIP(' style="mix-blend-mode: normal"')}`)), "covered");
});

test("#541: a cover in a document whose stylesheet may thin paint is not measured; one setting only opaque paint still passes", () => {
  for (const css of [".t{opacity:.5}", "path { fill-opacity: 0.5 !important }", "/* c */ g{mix-blend-mode:multiply}", ".s{fill:rgba(0,0,0,.5)}", "#strip{display:none}", "@import url(x.css);", "stop{stop-opacity:.3}", "@keyframes f{to{opacity:0}}"]) {
    assertUnproved(STRIP(' class="t"'), "stylesheet", `<style>${css}</style>\n`);
  }
  assertUnproved(STRIP(' class="t"'), "a stylesheet rule setting opacity: .5", "<style><![CDATA[.t{opacity:.5}]]></style>\n");
  for (const css of [".t{fill:#0c0}", "svg{display:block} body{background:#fff;opacity:1}", "/* .t{opacity:.5} */"]) {
    const r = contactsIn(`<style>${css}</style>\n${A(49)}\n${B(51)}\n${STRIP(' class="t"')}`);
    assert.equal(gapClass(r), "covered", css);
    assert.equal(r.status, 0, `${css}\n${r.lines.join("\n")}`);
  }
  assertUnproved(STRIP(' opacity="0.5"'), "may override", "<style>.t{fill:#0c0}</style>\n");
  const file = path.join(scratch, "linked.html");
  fs.writeFileSync(file, `<!doctype html><html><head><link rel="stylesheet" href="art.css"></head><body><svg width="100" height="100">${A(49)}${B(51)}${STRIP()}</svg></body></html>`);
  const linked = runInProcess(SCRIPT, ["--contacts", file]);
  assert.equal(linked.status, 6, linked.stdout);
  assert.match(linked.stdout, /: covered: .+a linked stylesheet, which it does not read/);
});

test("#541: a cover through a filter, or with an opacity or colour it cannot read, is not measured", () => {
  assertUnproved(STRIP(' filter="url(#blur)"'), "filter url(#blur) on line 4");
  assertUnproved(STRIP(' style="fill-opacity: var(--a)"'), "fill-opacity var(--a)");
  assertUnproved(`<g opacity="calc(1)">${STRIP()}</g>`, "opacity calc(1) on line 4");
  assertUnproved(STRIP(' fill="var(--brand)"'), "fill var(--brand), a colour it cannot read");
});

test("#324: a cover's style declarations are read in any case, an !important one over a later plain one, and only the -webkit- forms browsers apply", () => {
  const styled = (style) => `<path id="strip" style="${style}" d="M48 10 H52 V50 H48 Z"/>`;
  for (const style of ["fill:#0c0; Opacity:.5", "fill:#0c0; opacity: .5 !important", "fill:#0c0; FILL-OPACITY: 50%", "fill:#0c0; opacity:.3 !important; opacity:1", "fill: rgba(0,204,0,.3); -webkit-fill: #0c0", "fill:#0c0; opacity:.3; -webkit-opacity:1", "fill:#0c0; fill-opacity:.3; -webkit-fill-opacity:1", "fill: NONE", "fill:#0c0; display: None", "fill:#0c0; -webkit-mask-image: linear-gradient(#000, transparent)", "fill:#0c0; -webkit-mask-box-image: url(m.png)", "fill:#0c0; mask-border: url(m.png) 30", "fill:#0c0; -webkit-mask-box-image-source: url(m.png)"]) {
    assertUncovered(styled(style));
  }
  assertUnproved(STRIP(' style="-webkit-filter: opacity(.2)"'), "filter opacity(.2) on line 4");
  assertUnproved(STRIP(' class="t"'), "a stylesheet rule setting filter: blur(1px)", "<style>.t{-webkit-filter:blur(1px)}</style>\n");
  const ok = contactsIn(`${A(49)}\n${B(51)}\n${styled("FILL:#0c0; Opacity: 1 !important; opacity: .5; -webkit-filter: none; Visibility: Visible")}`);
  assert.equal(gapClass(ok), "covered", ok.lines.join("\n"));
  assert.equal(ok.status, 0, ok.lines.join("\n"));
});

test("#324: unset takes an inherited paint from the parent, a keyword it does not resolve leaves the cover unread, and a mask-image lets the ground through", () => {
  const strip = (style) => `<path id="strip" style="${style}" d="M48 10 H52 V50 H48 Z"/>`;
  for (const kw of ["unset", "inherit", "UNSET"]) {
    assertUncovered(`<g style="fill: rgba(0,204,0,.3)">${strip(`fill: ${kw}`)}</g>`);
    assertUncovered(`<g color="rgba(0,0,0,.3)"><path id="strip" fill="currentColor" style="color: ${kw}" d="M48 10 H52 V50 H48 Z"/></g>`);
  }
  for (const kw of ["initial", "revert", "revert-layer"]) assertUnproved(strip(`fill: ${kw}`), `fill ${kw}, a colour it cannot read`);
  assertUncovered(STRIP(' style="mask-image: linear-gradient(#000, transparent)"'));
  const ok = contactsIn(`${A(49)}\n${B(51)}\n<g style="fill: #0c0">${strip("fill: unset; clip-path: unset; mask: initial; mask-image: none")}</g>`);
  assert.equal(gapClass(ok), "covered", ok.lines.join("\n"));
  assert.equal(ok.status, 0, ok.lines.join("\n"));
});

test("#324: a gradient cover whose stop an <animate> or <set> changes is not measured, a stop inherits the gradient's stop-color only when told to, and an href naming no gradient says so", () => {
  const strip = '<path id="strip" fill="url(#g)" d="M48 10 H52 V50 H48 Z"/>';
  assertUnproved(`<defs><linearGradient id="g"><stop stop-color="#0c0"><animate attributeName="stop-opacity" values="1;0.1"/></stop></linearGradient></defs>${strip}`, "a gradient with a <animate> of stop-opacity");
  assertUnproved(`<defs><linearGradient id="g"><stop id="s0" stop-color="#0c0"/></linearGradient></defs>${strip}<set href="#s0" attributeName="stop-opacity" to="0.1"/>`, "a gradient with a <set> of stop-opacity");
  assertUnproved(`<defs><linearGradient id="h"><stop id="s1" stop-color="#0c0"/></linearGradient><linearGradient id="g" href="#h"/></defs>${strip}<set href="#s1" attributeName="stop-color" to="transparent"/>`, "a gradient with a <set> of stop-color");
  assertUnproved(`<defs><linearGradient id="g" href="#gone"/></defs>${strip}`, "a gradient whose href #gone names no gradient in the file");
  assertUnproved(`<defs><linearGradient id="g" href="#a"/></defs>${strip}`, "a gradient whose href #a names no gradient in the file");
  assertUncovered(`<defs><linearGradient id="g" stop-color="transparent"><stop stop-color="inherit"/></linearGradient></defs>${strip}`);
  for (const defs of [`<linearGradient id="g" stop-color="transparent"><stop/></linearGradient>`, `<linearGradient id="g" stop-color="#0c0"><stop style="stop-color: inherit"/></linearGradient>`, `<linearGradient id="g"><stop stop-color="#0c0"><animate attributeName="offset" values="0;1"/></stop></linearGradient>`]) {
    const ok = contactsIn(`${A(49)}\n${B(51)}\n<defs>${defs}</defs>${strip}`);
    assert.equal(ok.status, 0, `${defs}\n${ok.lines.join("\n")}`);
  }
});

test("#541: of several shapes over a gap, an opaque one covers it wherever it lies; one whose paint is unread outranks a translucent one", () => {
  const thin = STRIP(' fill-opacity="0.5"');
  for (const body of [`${thin}\n${STRIP()}`, `${STRIP()}\n${thin}`]) {
    const r = contactsIn(`${A(49)}\n${B(51)}\n${body}`);
    assert.match(r.lines.find((l) => l.includes("a.2-b.4=")), /: covered: the edges run 2 px apart, but \S+ <path id="strip">, painted over both, fills the gap\./, body);
  }
  assertUnproved(`${thin}\n${STRIP(' filter="url(#f)"')}`, "filter url(#f) on line 5");
  assertUnproved(`<g opacity="0.5">${STRIP(' filter="url(#f)"')}</g>\n${STRIP(' filter="url(#f)"')}`, "filter url(#f) on line 5");
});

test("#541: a cover whose paint an <animate> or <set> changes, on it, an ancestor or by href, is not measured", () => {
  const anim = '<animate attributeName="fill-opacity" values="1;0.2" dur="1s"/>';
  assertUnproved(`<path id="strip" fill="#0c0" d="M48 10 H52 V50 H48 Z">${anim}</path>`, "a <animate> of fill-opacity on line 4, which it does not play");
  assertUnproved(`<g><set attributeName="visibility" to="hidden"/>${STRIP()}</g>`, "a <set> of visibility");
  assertUnproved(`${STRIP()}<animate href="#strip" attributeName="opacity" values="1;0"/>`, "a <animate> of opacity");
  assert.equal(gapClass(contactsIn(`${A(49)}\n${B(51)}\n<path id="strip" fill="#0c0" d="M48 10 H52 V50 H48 Z"><animate attributeName="d" dur="1s"/></path>`)), "covered");
});

test("#541: --contacts --json marks a pass resting on paint it could not prove opaque", () => {
  const file = path.join(scratch, "unproved.svg");
  fs.writeFileSync(file, `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><style>.t{opacity:.5}</style>${A(49)}${B(51)}${STRIP()}</svg>`);
  const r = runInProcess(SCRIPT, ["--contacts", "--json", file]);
  assert.equal(r.status, 6, r.stdout);
  const { contacts } = JSON.parse(r.stdout);
  const gap = contacts.find((c) => c.name === "a.2-b.4");
  assert.deepEqual([gap.cls, gap.unproved], ["covered", true]);
});

test("#489: an underlap whose upper fill is translucent, sets a blend mode or sits under a stylesheet that may thin paint is not measured; opaque, it passes", () => {
  for (const attrs of [' fill-opacity="0.5"', ' fill="#00c8"', ' mix-blend-mode="multiply"']) {
    const r = contactsIn(`${A(51)}\n<path id="b" fill="#00c"${attrs} d="M50 10 H90 V50 H50 Z"/>`.replace('fill="#00c" fill=', "fill="));
    assert.ok(classes(r).includes("underlap"), attrs);
    assert.equal(r.status, 6, `${attrs}\n${r.lines.join("\n")}`);
    assert.match(r.lines.find((l) => l.includes(": underlap: ")), /but the upper fill does not hide the lower \(.+\) where they overlap, so the band is not measured; judge it under vault\.contacts-look\. --contact /);
  }
  assert.equal(contactsIn(`<path id="a" fill="#c00" fill-opacity="0.5" d="M10 10 H51 V50 H10 Z"/>\n${B()}`).status, 0);
  const sheet = contactsIn(`<style>p{color:var(--ink)}</style>\n${A(51)}\n${B()}`);
  assert.equal(sheet.status, 6, sheet.lines.join("\n"));
  assert.match(sheet.lines.find((l) => l.includes(": underlap: ")), /the upper fill is not proved opaque \(a stylesheet rule setting color: var\(--ink\), which it does not match to shapes\)/);
  const fixture = path.join(__dirname, "fixtures", "check-seams", "translucent.html");
  const r = runInProcess(SCRIPT, ["--contacts", fixture]);
  assert.equal(r.status, 6, r.stdout);
  assert.match(r.stdout, /: underlap: .+but the upper fill does not hide the lower \(fill-opacity 0\.5\) where they overlap.+--contact 'under\.2-over\.4=#over@/);
});
