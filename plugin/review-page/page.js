'use strict';
(function () {
  const R = window.ReviewPage;
  const $ = id => document.getElementById(id);
  const STATUS = { saving: 'Saving…', saved: 'Saved' };
  const PASSING = new Set(['unavailable', 'resource_exhausted']);
  const pickLabel = data => data.pick.label || 'Leader';
  const noPickLabel = data => data.pick.none || 'No leader';

  function el(tag, attrs, kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v == null) continue;
      if (k === 'text') e.textContent = v; else if (k === 'cls') e.className = v; else e.setAttribute(k, v);
    }
    for (const kid of kids || []) if (kid) e.appendChild(kid);
    return e;
  }

  function showProblems(list) {
    $('title').textContent = 'Review page';
    $('problems').hidden = false;
    for (const p of list) $('problem-list').appendChild(el('li', { text: p }));
  }

  function card(item, data) {
    const shot = el('a', { cls: 'shot', href: item.link || item.image, target: '_blank', rel: 'noopener', 'aria-label': `Open ${item.name} in full` },
      [item.image ? el('img', { src: item.image, alt: item.name, loading: 'lazy' }) : el('span', { cls: 'out', text: 'Open it ↗' })]);
    const marks = el('div', { cls: 'marks', role: 'group', 'aria-label': `Mark ${item.name}` },
      (data.marks || []).map(m => el('button', { type: 'button', 'data-mark': m.id, 'data-tone': m.tone, 'aria-pressed': 'false', disabled: '', text: m.label })));
    if (data.pick && item.pickable !== false) marks.appendChild(el('button', { type: 'button', 'data-pick': item.id, 'aria-pressed': 'false', disabled: '', text: pickLabel(data) }));
    return el('article', { cls: 'card', id: `card-${item.id}`, 'data-key': item.id }, [shot, el('div', { cls: 'body' }, [
      el('div', { cls: 'head' }, [el('span', { cls: 'name', text: item.name }), el('span', { cls: 'id', text: item.id })]),
      item.line ? el('p', { cls: 'line', text: item.line }) : null,
      item.tag ? el('span', { cls: 'tag', text: item.tag }) : null,
      marks.children.length ? marks : null,
      el('textarea', { id: `note-${item.id}`, placeholder: 'A note, if you have one', 'aria-label': `Note on ${item.name}`, disabled: '' }),
      el('div', { cls: 'status', id: `status-${item.id}` }),
    ])]);
  }

  function render(data) {
    document.title = data.title || document.title;
    $('title').textContent = data.title || 'Review';
    $('intro').textContent = data.intro || '';
    $('total').textContent = data.items.length;
    $('marked').hidden = !(data.marks || []).length;
    for (const item of data.items) $('cards').appendChild(card(item, data));
    $('set').hidden = false;
    $('set-ask').textContent = data.pageNote || 'A note on the whole set';
    $('set-ask').setAttribute('for', `note-${R.PAGE_KEY}`);
    $('set-box').append(el('textarea', { id: `note-${R.PAGE_KEY}`, disabled: '' }), el('div', { cls: 'status', id: `status-${R.PAGE_KEY}` }));
    if (data.pick) {
      $('leader-tally').hidden = false;
      $('none-pick').hidden = false;
      $('none-pick').appendChild(el('button', { type: 'button', 'data-pick': 'none', 'aria-pressed': 'false', disabled: '', text: noPickLabel(data) }));
    }
  }

  function paint(data, key, answer) {
    const marksOf = data.marks || [];
    if (key === R.PAGE_KEY) {
      document.querySelectorAll('[data-pick]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.pick === answer.pick)));
      document.querySelectorAll('.card').forEach(c => c.classList.toggle('leader', c.dataset.key === answer.pick));
      if (data.pick) {
        const leader = data.items.find(i => i.id === answer.pick);
        $('leader-tally').textContent = leader ? `${pickLabel(data)}: ${leader.name}` : answer.pick === 'none' ? noPickLabel(data) : 'No pick yet';
      }
    } else {
      const c = $(`card-${key}`);
      c.querySelectorAll('[data-mark]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mark === answer.mark)));
      const tone = marksOf.find(m => m.id === answer.mark)?.tone;
      if (tone) c.dataset.markTone = tone; else delete c.dataset.markTone;
    }
    const box = $(`note-${key}`);
    if (box.value !== (answer.note || '')) box.value = answer.note || '';
    $('done').textContent = data.items.filter(i => answers.answer(i.id).mark).length;
  }

  function showSaveStatus(key, state, err) {
    const s = $(`status-${key}`), code = (err && err.code) || 'error';
    s.classList.toggle('failed', state === 'failed');
    s.textContent = state !== 'failed' ? STATUS[state]
      : PASSING.has(code) ? `Not saved yet (${code}). Your answer is still here and saves again when you type or leave the box.`
      : `Not saved (${code}): this view cannot save answers. Reply in chat instead.`;
  }

  let answers;
  async function start() {
    let data;
    try {
      const res = await fetch('items.json', { cache: 'no-store' });
      if (!res.ok) throw new Error(`items.json answered ${res.status}`);
      data = await res.json();
    } catch (e) {
      return showProblems([`items.json could not be read: ${e.message}`]);
    }
    const { problems } = R.checkItems(data);
    if (problems.length) return showProblems(problems);
    render(data);

    let db = null;
    try { db = window.claude && window.claude.use ? await window.claude.use('db') : null; } catch (e) { db = null; }
    if (!db) { $('conn').textContent = 'Answers cannot be saved in this view. Reply in chat instead.'; return; }
    const col = db.collection(R.COLLECTION);
    answers = R.createAnswers({ collection: col, keys: data.items.map(i => i.id),
      onChange: (key, a) => paint(data, key, a), onStatus: showSaveStatus });
    document.querySelectorAll('button, textarea').forEach(e => { e.disabled = false; });
    document.querySelectorAll('[data-mark]').forEach(b => b.addEventListener('click', () => answers.mark(b.closest('.card').dataset.key, b.dataset.mark)));
    document.querySelectorAll('[data-pick]').forEach(b => b.addEventListener('click', () => answers.pick(b.dataset.pick)));
    for (const key of answers.keys) {
      const box = $(`note-${key}`);
      box.addEventListener('input', () => answers.note(key, box.value));
      box.addEventListener('blur', () => answers.flush());
    }
    addEventListener('pagehide', () => answers.flush());
    document.addEventListener('visibilitychange', () => { if (document.hidden) answers.flush(); });
    $('conn').textContent = 'Answers save as you go';
    $('foot').hidden = false;
    col.onSnapshot(snap => answers.receive(snap), err => {
      $('conn').textContent = `Saved answers stopped loading (${err.code}). New answers still save; reload to see others.`;
    });
  }
  start();
})();
