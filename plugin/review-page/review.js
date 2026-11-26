'use strict';
(function (exports) {
  const COLLECTION = 'answers';
  const PAGE_KEY = '_page';
  // guess, #183
  const NOTE_PAUSE_MS = 900;
  const ID = /^[A-Za-z0-9_.~:@+-]{1,200}$/;

  function checkItems(data) {
    const problems = [];
    if (!data || typeof data !== 'object') return { problems: ['items.json is not a JSON object'] };
    if (!Array.isArray(data.items) || !data.items.length) problems.push('items.json has no "items"');
    const marks = data.marks || [];
    if (!Array.isArray(marks)) problems.push('"marks" is not a list');
    else marks.forEach((m, i) => { if (!m || !ID.test(m.id || '') || !m.label) problems.push(`mark ${i + 1} needs an "id" and a "label"`); });
    // A browser trims the ends, drops tabs and newlines, and reads `\` as `/`: https://url.spec.whatwg.org/#concept-basic-url-parser
    const fileOrHttps = raw => {
      const src = String(raw).replace(/^[\u0000-\u0020]+|[\u0000-\u0020]+$/g, '').replace(/[\t\n\r]/g, '');
      return /^https:\/\//i.test(src) || !(/^[a-z][a-z0-9+.-]*:/i.test(src) || /^[\\/]{2}/.test(src));
    };
    const seen = new Set();
    (Array.isArray(data.items) ? data.items : []).forEach((item, i) => {
      const where = `item ${i + 1}${item && item.id ? ` (${item.id})` : ''}`;
      if (!item || !ID.test(item.id || '')) problems.push(`${where} needs an "id" of letters, digits and _ . ~ : @ + -`);
      else if (item.id === PAGE_KEY) problems.push(`${where}: "${PAGE_KEY}" is the page's own answer`);
      else if (seen.has(item.id)) problems.push(`${where}: the id is used twice`);
      if (item && item.id) seen.add(item.id);
      if (item && !item.name) problems.push(`${where} needs a "name"`);
      if (item && !item.image && !item.link) problems.push(`${where} needs an "image" or a "link"`);
      if (item && 'pickable' in item && typeof item.pickable !== 'boolean') problems.push(`${where}: "pickable" must be true or false`);
      if (item && item.link && !/^https?:\/\//i.test(item.link)) problems.push(`${where}: "link" must start with http:// or https://`);
      if (item && item.image && !fileOrHttps(item.image)) problems.push(`${where}: "image" must be a file beside the page or an https:// address`);
    });
    return { problems };
  }

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
      mark(key, value) { cancelTimer(key); edit(key, 'mark', value); save(key); },
      pick(value) { cancelTimer(PAGE_KEY); edit(PAGE_KEY, 'pick', value); save(PAGE_KEY); },
      note(key, text) {
        cancelTimer(key);
        edit(key, 'note', text);
        timers[key] = setTimer(() => { timers[key] = null; save(key); }, NOTE_PAUSE_MS);
      },
      flush() {
        for (const key of keys) if (timers[key] != null || (dirty[key] && !writing[key])) { cancelTimer(key); save(key); }
      },
      async settle() { while (inFlight.size) await Promise.all([...inFlight]); },
      receive(snap) {
        for (const doc of snap.docs) {
          const key = doc.id;
          if (!keys.has(key) || !doc.exists) continue;
          // #90
          const body = Object.assign({}, doc.data());
          if (busy(key)) { if (!held[key] || Number(body.at) > Number(held[key].at)) held[key] = body; continue; }
          take(key, body);
        }
      },
    };
  }

  Object.assign(exports, { COLLECTION, PAGE_KEY, checkItems, createAnswers });
})(typeof module === 'object' ? module.exports : (window.ReviewPage = {}));
