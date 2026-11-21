'use strict';
/**
 * review.js — the shared review page's logic (#120): checking the data file, and the feedback boxes that keep the founder's
 * answers in the page's `db` store. Shared by the page (page.js) and its tests (test/review-page.test.js);
 * nothing here reads the page or the network.
 */
(function (exports) {
  // The page's own answers share the collection with the cards', under an id no card may take.
  const COLLECTION = 'answers';
  const PAGE_KEY = '_page';
  // How long after the last keystroke a note saves, carried from mmm-infra's fixed page (calibrate-v4 template.html:243).
  // It is above the gap between keys for almost every typist (Dhakal et al., CHI 2018) but under the 1-2 s pause writing
  // research ends a burst of typing at (Chenu et al., Frontiers in Psychology 2014), so it may save mid-burst: an extra
  // write only, as a note also saves on blur and on leaving the page (design-vault#183's audit, R1).
  const NOTE_PAUSE_MS = 900;
  // The store's document-id grammar (the artifact `db` contract 0.2.75, db.d.ts PATH GRAMMAR), so a card id is also a valid answer key.
  const ID = /^[A-Za-z0-9_.~:@+-]{1,200}$/;

  /** The data file, checked: every problem named, so a bad items.json shows its faults instead of a blank page. */
  function checkItems(data) {
    const problems = [];
    if (!data || typeof data !== 'object') return { problems: ['items.json is not a JSON object'] };
    if (!Array.isArray(data.items) || !data.items.length) problems.push('items.json has no "items"');
    const marks = data.marks || [];
    if (!Array.isArray(marks)) problems.push('"marks" is not a list');
    else marks.forEach((m, i) => { if (!m || !ID.test(m.id || '') || !m.label) problems.push(`mark ${i + 1} needs an "id" and a "label"`); });
    const fileOrHttps = src => !/^[a-z][a-z0-9+.-]*:/i.test(src) || /^https:\/\//i.test(src);
    if (data.figure && !fileOrHttps(data.figure)) problems.push('"figure" must be a file beside the page or an https:// address');
    const seen = new Set();
    (Array.isArray(data.items) ? data.items : []).forEach((item, i) => {
      const where = `item ${i + 1}${item && item.id ? ` (${item.id})` : ''}`;
      if (!item || !ID.test(item.id || '')) problems.push(`${where} needs an "id" of letters, digits and _ . ~ : @ + -`);
      else if (item.id === PAGE_KEY) problems.push(`${where}: "${PAGE_KEY}" is the page's own answer`);
      else if (seen.has(item.id)) problems.push(`${where}: the id is used twice`);
      if (item && item.id) seen.add(item.id);
      if (item && !item.name) problems.push(`${where} needs a "name"`);
      if (item && !item.image && !item.link && !data.figure) problems.push(`${where} needs an "image" or a "link"`);
      if (item && 'pickable' in item && typeof item.pickable !== 'boolean') problems.push(`${where}: "pickable" must be true or false`);
      // Each opens the card's full view, so a javascript: address is refused here rather than at the click.
      if (item && item.link && !/^https?:\/\//i.test(item.link)) problems.push(`${where}: "link" must start with http:// or https://`);
      if (item && item.image && !fileOrHttps(item.image)) problems.push(`${where}: "image" must be a file beside the page or an https:// address`);
    });
    return { problems };
  }

  /**
   * The feedback boxes, over one collection of the store: one answer per card id and one for the page.
   * A card's answer is { mark, note }; the page's is { note, pick }.
   * Each saved answer carries `at`, the time of the edit, so an older copy never replaces a newer one.
   *
   * The store delivers every answer on any change, including this page's own writes and, late, older copies.
   * Two rules keep what was typed: while an answer has an edit not yet saved or saving, the store's newest copy of it
   * is held back; once saved, only a copy newer than the last edit is taken. Every snapshot is copied before use: the store
   * freezes what it delivers, and an edit written into a frozen answer is lost (#90 P7).
   */
  function createAnswers(opts) {
    const col = opts.collection;
    const keys = new Set(opts.keys);
    keys.add(PAGE_KEY);
    const onChange = opts.onChange || (() => {});
    const onStatus = opts.onStatus || (() => {});
    const now = opts.now || (() => Date.now());
    const setTimer = opts.setTimer || setTimeout;
    const clearTimer = opts.clearTimer || clearTimeout;
    const answers = {}, dirty = {}, timers = {}, writing = {}, queued = {}, lastAt = {}, held = {};
    const inFlight = new Set();

    const answer = key => Object.assign({}, answers[key]);
    function edit(key, field, value) {
      if (!keys.has(key)) throw new Error(`no answer box "${key}"`);
      if (!answers[key]) answers[key] = {};
      answers[key][field] = value;
      dirty[key] = true;
      onChange(key, Object.assign({}, answers[key]));
    }
    function save(key) {
      if (writing[key]) { queued[key] = true; return; }
      writing[key] = true;
      // A stamp after the last one, even when the clock has not moved, so this write outranks the one before it.
      const at = Math.max(now(), (lastAt[key] || 0) + 1);
      lastAt[key] = at;
      dirty[key] = false;
      onStatus(key, 'saving');
      const body = key === PAGE_KEY
        ? { note: answer(key).note || '', pick: answer(key).pick || '', at }
        : { mark: answer(key).mark || '', note: answer(key).note || '', at };
      const done = Promise.resolve()
        .then(() => col.doc(key).set(body))
        .then(() => onStatus(key, 'saved'), err => {
          // Still on screen and still unsaved: the next edit, or flush, tries again.
          dirty[key] = true;
          onStatus(key, 'failed', err);
        })
        .then(() => {
          writing[key] = false;
          inFlight.delete(done);
          if (queued[key]) { queued[key] = false; save(key); } else if (!busy(key)) takeHeld(key);
        });
      inFlight.add(done);
    }
    const busy = key => dirty[key] || writing[key] || timers[key] != null;
    function take(key, body) {
      const at = Number(body.at) || 0;
      if (lastAt[key] && !(at > lastAt[key])) return;
      lastAt[key] = at;
      answers[key] = body;
      onChange(key, Object.assign({}, body));
    }
    function takeHeld(key) {
      const body = held[key];
      held[key] = null;
      if (body) take(key, body);
    }
    function cancelTimer(key) {
      if (timers[key] == null) return;
      clearTimer(timers[key]);
      timers[key] = null;
    }

    return {
      keys: [...keys],
      answer,
      /** A mark on a card, saved at once; the note as typed goes with it. */
      mark(key, value) { cancelTimer(key); edit(key, 'mark', value); save(key); },
      /** The page's single pick across cards: a card id, or "none" for no leader. Saved at once. */
      pick(value) { cancelTimer(PAGE_KEY); edit(PAGE_KEY, 'pick', value); save(PAGE_KEY); },
      /** A note as typed, saved after a pause. */
      note(key, text) {
        cancelTimer(key);
        edit(key, 'note', text);
        timers[key] = setTimer(() => { timers[key] = null; save(key); }, NOTE_PAUSE_MS);
      },
      /** Save every note still waiting on its pause: on leaving a box, or the page. */
      flush() {
        for (const key of keys) if (timers[key] != null || (dirty[key] && !writing[key])) { cancelTimer(key); save(key); }
      },
      /** Resolves once every write started so far, and any it queued, has settled. */
      async settle() { while (inFlight.size) await Promise.all([...inFlight]); },
      /** One delivery of the collection, as onSnapshot hands it. */
      receive(snap) {
        for (const doc of snap.docs) {
          const key = doc.id;
          if (!keys.has(key) || !doc.exists) continue;
          // A copy: the delivered body is frozen, and this page edits its answers in place.
          const body = Object.assign({}, doc.data());
          // Held, not dropped: the store sends a document again only when it changes, so another tab's answer that
          // lands mid-save would otherwise never be seen.
          if (busy(key)) { if (!held[key] || Number(body.at) > Number(held[key].at)) held[key] = body; continue; }
          take(key, body);
        }
      },
    };
  }

  Object.assign(exports, { COLLECTION, PAGE_KEY, checkItems, createAnswers });
})(typeof module === 'object' ? module.exports : (window.ReviewPage = {}));
