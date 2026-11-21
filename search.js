'use strict';
/**
 * search.js — the search box's rule, shared by the page (app.js) and its tests (#27, #42).
 * Every typed word must start a word somewhere in what a reference says, in any
 * order ("sea" finds "seascape", never "research"), and a word on the library's
 * design-word list also finds the words the data uses for it (hero → opening screen).
 */
(function (exports) {
  const escapeRegExp = text => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  // One test per typed word; an empty query has none, so it matches everything.
  function compile(query, designWords) {
    return query.toLowerCase().split(/\s+/).filter(Boolean).map(word => {
      const alternatives = [word, ...(designWords.find(d => d.word === word)?.means || [])];
      return new RegExp('(^|[^a-z0-9])(' + alternatives.map(a => escapeRegExp(a.toLowerCase())).join('|') + ')');
    });
  }

  // The lower-cased text a query is tested against.
  const searchable = texts => texts.filter(Boolean).join(' ').toLowerCase();
  const matches = (tests, text) => tests.every(test => test.test(text));

  // What search reads of a reference (#27 Q2, Q3): never the fit take, composition, image_recipe or
  // mood, and of motion only its plain parts, never range, from_to, duration, easing, evidence or capture.
  function entryTexts(e, gallery, project) {
    const named = (list, ids) => (ids || []).map(id => list.find(item => item.id === id)?.name || id);
    const collection = gallery.collections.find(c => c.id === e.collection);
    const groups = gallery.projects?.[project]?.groups || [];
    return [
      e.title, e.description, e.note, e.founder_note, ...(e.keywords || []), ...(e.vocabulary || []),
      collection?.name, collection?.description, ...named(gallery.page_parts, e.page_parts),
      ...named(gallery.motion_kinds, e.motion?.kinds), e.motion?.trigger, e.motion?.purpose, e.motion?.purpose_note,
      ...named(groups, e.fit?.[project]?.groups).map(name => name.split(' — ')[0]),
    ];
  }

  Object.assign(exports, { compile, searchable, matches, entryTexts });
})(typeof module === 'object' ? module.exports : (window.VaultSearch = {}));
