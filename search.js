'use strict';
(function (exports) {
  const escapeRegExp = text => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  function compile(query, designWords) {
    return query.toLowerCase().split(/\s+/).filter(Boolean).map(word => {
      const alternatives = [word, ...(designWords.find(d => d.word === word)?.means || [])];
      return new RegExp('(^|[^a-z0-9])(' + alternatives.map(a => escapeRegExp(a.toLowerCase())).join('|') + ')');
    });
  }

  const searchable = texts => texts.filter(Boolean).join(' ').toLowerCase();
  const matches = (tests, text) => tests.every(test => test.test(text));

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
