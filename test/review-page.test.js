"use strict";
// The shared review page's feedback boxes and data check (plugin/review-page/review.js, #120),
// run in-process against a store double that behaves as the real `db` store does where mmm-infra's pages failed (#90 P7):
// it freezes every snapshot it delivers and its data(), echoes the page's own writes back, and can replay an older copy late.
// Loosen the double and the note test passes on a broken page.
const assert = require("node:assert/strict");
const { test } = require("node:test");
const R = require("../plugin/review-page/review.js");

// One collection of the store. Every delivery carries every document, as the real store's query snapshots do.
function storeDouble() {
  const bodies = new Map(), listeners = new Set(), writes = [];
  const snapOf = (id, body) => Object.freeze({
    id, exists: true, data: () => body, metadata: Object.freeze({ fromCache: false, hasPendingWrites: false }),
  });
  const deliver = override => {
    const docs = [...bodies].map(([id, body]) => snapOf(id, override && override.id === id ? Object.freeze({ ...override.body }) : body));
    const snap = Object.freeze({ docs, size: docs.length, empty: !docs.length });
    for (const next of listeners) next(snap);
  };
  return {
    writes,
    seed(id, body) { bodies.set(id, Object.freeze({ ...body })); },
    body: id => bodies.get(id),
    deliver,
    replay(id, body) { deliver({ id, body }); },
    collection: {
      doc: id => ({
        async set(body) {
          writes.push({ id, body });
          bodies.set(id, Object.freeze({ ...body }));
          deliver();
        },
      }),
      onSnapshot(next) { listeners.add(next); deliver(); return () => listeners.delete(next); },
    },
  };
}

// The page's timers, run by hand; the clock moves only when the test moves it.
function harness(store, keys = ["v1", "v2"]) {
  const timers = new Map();
  let nextId = 1, clock = 1000;
  const page = R.createAnswers({
    collection: store.collection, keys, now: () => clock,
    setTimer: (fn) => { const id = nextId++; timers.set(id, fn); return id; },
    clearTimer: (id) => timers.delete(id),
  });
  store.collection.onSnapshot(snap => page.receive(snap));
  return {
    page,
    tick(ms = 1) { clock += ms; },
    /** The pause after typing ends: every waiting note saves. */
    pause() { const due = [...timers.values()]; timers.clear(); due.forEach(fn => fn()); },
  };
}

test("a typed note survives its own echo and a stale replay (#90 P7)", async () => {
  const store = storeDouble();
  // An answer saved on an earlier visit, so the page starts from a delivered (frozen) snapshot.
  store.seed("v1", { mark: "keep", note: "", at: 500 });
  const { page, tick, pause } = harness(store);
  assert.equal(page.answer("v1").mark, "keep");

  page.note("v1", "This ");
  tick(); pause();
  // He keeps typing while the first save is still on its way back.
  page.note("v1", "This is the one");
  await page.settle();
  assert.equal(page.answer("v1").note, "This is the one", "the echo of the first save replaced what he typed after it");

  tick(); pause(); await page.settle();
  store.replay("v1", { mark: "keep", note: "This ", at: 1001 });
  assert.equal(page.answer("v1").note, "This is the one", "a late copy of the first save replaced the second");
  assert.equal(store.body("v1").note, "This is the one");
  assert.equal(store.body("v1").mark, "keep", "saving the note dropped the mark");
});

test("a mark sticks through its echo and a stale replay, and a second click keeps it", async () => {
  const store = storeDouble();
  const { page, tick } = harness(store);
  page.mark("v2", "drop");
  await page.settle();
  tick();
  page.mark("v2", "keep");
  await page.settle();
  store.replay("v2", { mark: "drop", note: "", at: 1000 });
  assert.equal(page.answer("v2").mark, "keep");
  page.mark("v2", "keep");
  await page.settle();
  assert.equal(store.body("v2").mark, "keep");
});

test("a reload restores every card's mark and note, and the page's note and pick", async () => {
  const store = storeDouble();
  const first = harness(store);
  first.page.mark("v1", "keep");
  first.page.note("v1", "the water reads as one line");
  first.page.note(R.PAGE_KEY, "push the blue further");
  first.page.pick("v1");
  first.page.flush();
  await first.page.settle();

  const reloaded = harness(store);
  assert.deepEqual(
    { mark: reloaded.page.answer("v1").mark, note: reloaded.page.answer("v1").note },
    { mark: "keep", note: "the water reads as one line" });
  assert.equal(reloaded.page.answer(R.PAGE_KEY).note, "push the blue further");
  assert.equal(reloaded.page.answer(R.PAGE_KEY).pick, "v1");
});

test("a rebuild that keeps a card's id keeps its answer, and an answer for a dropped card is left alone", async () => {
  const store = storeDouble();
  store.seed("v1", { mark: "keep", note: "kept", at: 500 });
  store.seed("old", { mark: "drop", note: "gone", at: 500 });
  const { page } = harness(store, ["v1", "v3"]);
  assert.equal(page.answer("v1").note, "kept");
  assert.deepEqual(page.answer("old"), {});
  assert.equal(store.body("old").note, "gone");
});

test("another tab's newer answer is taken once this page has nothing unsaved", async () => {
  const store = storeDouble();
  const { page, pause } = harness(store);
  page.note("v1", "first");
  pause(); await page.settle();
  store.replay("v1", { mark: "", note: "from the other tab", at: 5000 });
  assert.equal(page.answer("v1").note, "from the other tab");
});

test("a note typed before the saved answers arrive is kept", async () => {
  const store = storeDouble();
  store.seed("v1", { mark: "keep", note: "old", at: 500 });
  const page = R.createAnswers({ collection: store.collection, keys: ["v1"], setTimer: () => 1, clearTimer: () => {} });
  page.note("v1", "new");
  store.collection.onSnapshot(snap => page.receive(snap));
  assert.equal(page.answer("v1").note, "new");
});

test("two saves in one millisecond both reach another open view", async () => {
  const store = storeDouble();
  const a = harness(store), b = harness(store);
  a.page.mark("v1", "keep");
  a.page.note("v1", "and this");
  a.page.flush();
  await a.page.settle();
  assert.deepEqual([b.page.answer("v1").mark, b.page.answer("v1").note], ["keep", "and this"]);
});

test("another tab's answer that lands while this page is saving is taken once the save ends", async () => {
  const store = storeDouble();
  // This page's write reaches the store, then the other tab's newer write lands before this page hears back.
  const col = {
    doc: id => ({ async set(body) {
      await store.collection.doc(id).set(body);
      await store.collection.doc(id).set({ mark: "drop", note: "from the other tab", at: body.at + 5000 });
    } }),
    onSnapshot: store.collection.onSnapshot,
  };
  const page = R.createAnswers({ collection: col, keys: ["v1"] });
  col.onSnapshot(snap => page.receive(snap));
  page.mark("v1", "keep");
  await page.settle();
  assert.deepEqual([page.answer("v1").mark, page.answer("v1").note], ["drop", "from the other tab"]);
});

test("a failed save stays on screen and goes again on flush", async () => {
  const store = storeDouble();
  const statuses = [];
  let fail = true;
  const col = {
    doc: id => ({ set: async body => { if (fail) throw { code: "unavailable" }; return store.collection.doc(id).set(body); } }),
    onSnapshot: store.collection.onSnapshot,
  };
  const page = R.createAnswers({ collection: col, keys: ["v1"], onStatus: (k, s) => statuses.push(s) });
  page.mark("v1", "keep");
  await page.settle();
  assert.equal(page.answer("v1").mark, "keep");
  assert.deepEqual(statuses, ["saving", "failed"]);
  fail = false;
  page.flush();
  await page.settle();
  assert.equal(store.body("v1").mark, "keep");
});

test("an answer box the page does not have is refused, not silently created", () => {
  const page = R.createAnswers({ collection: storeDouble().collection, keys: ["v1"] });
  assert.throws(() => page.mark("nope", "keep"), /no answer box "nope"/);
});

test("the data check names every fault in items.json", () => {
  const good = { marks: [{ id: "keep", label: "Keep" }], items: [{ id: "v1", name: "Arches", image: "img/v1.webp" }, { id: "v2", name: "Live", link: "https://x.example" }] };
  assert.deepEqual(R.checkItems(good).problems, []);
  const bad = {
    marks: [{ id: "keep" }],
    items: [
      { id: "v1", name: "A", image: "a.png" }, { id: "v1", name: "B", image: "b.png" },
      { id: "_page", name: "C", image: "c.png" }, { id: "has space", name: "D", image: "d.png" },
      { id: "v5", image: "e.png" }, { id: "v6", name: "F" }, { id: "v7", name: "G", link: "javascript:alert(1)" }, { id: "v8", name: "H", image: "javascript:alert(1)" }, { id: "v9", name: "I", image: "i.png", pickable: "no" },
    ],
  };
  const problems = R.checkItems(bad).problems.join("\n");
  for (const fault of [/mark 1 needs/, /\(v1\): the id is used twice/, /"_page" is the page's own answer/, /\(has space\) needs an "id"/,
    /\(v5\) needs a "name"/, /\(v6\) needs an "image" or a "link"/, /\(v7\): "link" must start with http/, /\(v8\): "image" must be a file beside/, /\(v9\): "pickable" must be true or false/]) {
    assert.match(problems, fault);
  }
  assert.deepEqual(R.checkItems({}).problems, ['items.json has no "items"']);
});

test("a figure for the whole set lets its cards go without a picture of their own (#221)", () => {
  const shared = { figure: "img/lanes.svg", items: [{ id: "a", name: "A" }, { id: "b", name: "B", image: "img/b.svg" }] };
  assert.deepEqual(R.checkItems(shared).problems, []);
  assert.match(R.checkItems({ ...shared, figure: "javascript:alert(1)" }).problems.join("\n"), /"figure" must be a file beside/);
});

test("an address on another host with no scheme is not a file beside the page (#554)", () => {
  for (const src of ["//evil.example/x.png", "\\\\evil.example/x.png", "/\\evil.example/x.png", "\\/evil.example/x.png"]) {
    assert.match(R.checkItems({ figure: src, items: [{ id: "a", name: "A" }] }).problems.join("\n"), /"figure" must be a file beside/, src);
    assert.match(R.checkItems({ items: [{ id: "a", name: "A", image: src }] }).problems.join("\n"), /\(a\): "image" must be a file beside/, src);
  }
  for (const src of ["/img/x.png", "img/x.png", "https://cdn.example/x.png"])
    assert.deepEqual(R.checkItems({ items: [{ id: "a", name: "A", image: src }] }).problems, [], src);
});
