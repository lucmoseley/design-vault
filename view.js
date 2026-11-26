'use strict';
(function (exports) {
  const search = typeof module === 'object' ? require('./search.js') : window.VaultSearch;
  const VAULT = '~/design-vault';

  const inProject = (v, e) => !e.project || e.project === v.project;
  const libraryEntries = v => v.data.entries.filter(e => inProject(v, e));
  const fitOf = (v, e) => e.fit?.[v.project];
  const verdictOf = (v, e) => fitOf(v, e)?.verdict || 'unjudged';
  const projectName = v => v.data.projects?.[v.project]?.name || v.project;
  const projectGroups = v => v.data.projects?.[v.project]?.groups || [];
  const groupLabel = (v, id) => (projectGroups(v).find(g => g.id === id)?.name || id).split(' — ')[0];
  const named = (list, ids) => (ids || []).map(id => list.find(item => item.id === id)?.name || id);
  const partNames = (v, e) => named(v.data.page_parts, e.page_parts);
  const kindsOf = e => e.motion?.kinds || [];
  const kindNames = (v, e) => named(v.data.motion_kinds, kindsOf(e));
  const styleNames = (v, c) => named(v.styles.styles, c.styles);
  const collectionLine = (v, c) => c.name + (c.styles?.length ? ` (Style guide: ${styleNames(v, c).join(', ')})` : '');
  const siteAddress = e => [e.url, e.site_url].find(u => /^https?:\/\//i.test(u || ''));
  const referencePath = e => 'images/' + (e.file || e.still);
  const motionSummary = (v, e) => [kindNames(v, e).join(', '), [e.motion.trigger, e.motion.property].filter(Boolean).join(' · '), e.motion.from_to,
    e.motion.easing && 'easing ' + e.motion.easing, e.motion.purpose && 'purpose ' + e.motion.purpose + (e.motion.purpose_note ? ': ' + e.motion.purpose_note : ''),
    e.motion.reduced && 'reduced motion: ' + e.motion.reduced].filter(Boolean).join(' — ');

  const WAYS = [
    { key: 'look', ids: v => v.data.collections.map(c => c.id), has: (v, e, id) => e.collection === id },
    { key: 'part', projectScoped: true, has: (v, e, id) => (e.page_parts || []).includes(id),
      ids: v => v.data.page_parts.filter(p => libraryEntries(v).some(e => (e.page_parts || []).includes(p.id))).map(p => p.id) },
    { key: 'motion', projectScoped: true, has: (v, e, id) => kindsOf(e).includes(id),
      ids: v => v.data.motion_kinds.filter(k => libraryEntries(v).some(e => kindsOf(e).includes(k.id))).map(k => k.id) },
    { key: 'group', projectScoped: true, ids: v => projectGroups(v).map(g => g.id), has: (v, e, id) => (fitOf(v, e)?.groups || []).includes(id) },
  ];
  const picked = v => WAYS.filter(w => v.pick[w.key]);

  const searchTexts = new WeakMap();
  function searchText(v, e) {
    if (!searchTexts.has(v.data)) searchTexts.set(v.data, new Map());
    const cache = searchTexts.get(v.data), key = v.project + '\n' + e.id;
    if (!cache.has(key)) cache.set(key, search.searchable(search.entryTexts(e, v.data, v.project)));
    return cache.get(key);
  }
  const matchesQuery = (v, e) => !v.queryTests.length || search.matches(v.queryTests, searchText(v, e));
  const fitPasses = (v, e) => v.fit === 'any' || verdictOf(v, e) === v.fit;
  const passes = (v, e, exceptKey) => WAYS.every(w => w.key === exceptKey || !v.pick[w.key] || w.has(v, e, v.pick[w.key])) && fitPasses(v, e) && matchesQuery(v, e);
  const countFor = (v, key, id) => libraryEntries(v).filter(e => passes(v, e, key) && WAYS.find(w => w.key === key).has(v, e, id)).length;
  const visibleEntries = v => libraryEntries(v).filter(e => passes(v, e))
    .sort(v.sort === 'name' ? (a, b) => a.title.localeCompare(b.title) : (a, b) => b.added.localeCompare(a.added));
  const visibleStyles = v => v.styles.styles.filter(s => search.matches(v.queryTests, search.searchable([s.name, ...s.vocabulary, ...s.recognize])))
    .sort(v.sort === 'name' ? (a, b) => a.name.localeCompare(b.name) : () => 0);

  function viewHash(v) {
    if (v.showStyles) return 'styles';
    const params = new URLSearchParams(picked(v).map(w => [w.key, v.pick[w.key]]));
    if (picked(v).some(w => w.projectScoped)) params.set('project', v.project);
    return params.toString() || 'all';
  }
  const OLD_GROUP_HASH = 'group:';
  function readHash(v, hash) {
    const params = new URLSearchParams(hash.includes('=') ? hash : ''), linked = params.get('project') ?? '';
    const project = Object.hasOwn(v.data.projects || {}, linked) ? linked : v.project, at = { ...v, project };
    if (v.data.collections.some(c => c.id === hash)) params.set('look', hash);
    if (hash.startsWith(OLD_GROUP_HASH)) params.set('group', hash.slice(OLD_GROUP_HASH.length));
    const pick = Object.fromEntries(WAYS.map(w => [w.key, w.ids(at).includes(params.get(w.key)) ? params.get(w.key) : null]));
    return { project, pick, showStyles: hash === 'styles' };
  }

  function preferenceBlock(v) {
    const { prefs, data } = v;
    const parts = [
      prefs.includeDna && data.dna.constants.length ? `General preferences (defaults, not absolute rules):\n${data.dna.constants.map(s => '- ' + s).join('\n')}` : '',
      prefs.includeDna ? `Usually avoid (defaults, not absolute rules):\n${data.dna.never.map(s => '- ' + s).join('\n')}` : '',
      prefs.overrides.trim() ? `Project-specific directions (take priority):\n${prefs.overrides.trim()}` : '',
    ].filter(Boolean);
    return parts.length ? [...parts, 'Follow the selected references and explicit project directions when they differ from general preferences.'].join('\n\n') + '\n\n' : '';
  }
  const sheetCite = f => f.sheet_section ? ` (brand sheet ${f.sheet_section})` : '';
  const groupCite = (v, f) => f.groups.length ? `, group${f.groups.length > 1 ? 's' : ''} ${f.groups.map(id => groupLabel(v, id)).join(', ')}` : '';
  function entrySection(v, e) {
    const f = fitOf(v, e), collection = v.data.collections.find(c => c.id === e.collection);
    return `Reference: ${e.id} — ${e.title}\nScreenshot: ${referencePath(e)}\nCollection: ${collectionLine(v, collection)}\nPage part: ${partNames(v, e).join(', ')}`
      + `${siteAddress(e) ? '\nSite: ' + siteAddress(e) : ''}${e.keywords?.length ? '\nKeywords: ' + e.keywords.join(', ') : ''}${e.vocabulary?.length ? '\nVocabulary: ' + e.vocabulary.join(', ') : ''}`
      + `${e.description ? '\nDescription: ' + e.description : ''}${e.note ? '\nNote (any project): ' + e.note : ''}`
      + `\n${projectName(v)} fit: ${f ? `${f.verdict}${sheetCite(f)}${groupCite(v, f)} — take: ${f.take}` : 'unjudged — write the verdict and take before this brief runs'}`
      + `${e.motion ? '\nMotion: ' + motionSummary(v, e) : '\nComposition: ' + (e.composition || 'Use the reference image for composition.')}${e.image_recipe ? '\nImage recipe: ' + e.image_recipe : ''}`;
  }
  const buildBrief = (v, entries) => `Vault: ${VAULT}\nBuild [describe the website or product] for [audience].\nPrimary action: [what the visitor should do].\nRequired content: [sections and copy].\n\n`
    + `${entries.map(e => entrySection(v, e)).join('\n\n---\n\n')}\n\n`
    + `${entries.length > 1 ? 'Use these as a reference set. Create one direction per reference, each built from its own reference alone, before choosing one.\n\n' : ''}`
    + `${preferenceBlock(v)}Read the reference images before designing. Borrow their visual treatment and hierarchy; write for our product and use our content. Do not reuse sample claims or endorsements. Generate original image assets where useful with the available image-generation tool, using the recipes and composition notes. Build real responsive HTML text, controls, and components around those assets. Verify the result in a browser on desktop and mobile.`;
  const collectionBrief = (v, c) => `Collection: ${collectionLine(v, c)}\n${c.description}\nVocabulary: ${c.vocabulary.join(', ')}\nDirection to explore: ${c.risk}\n\n`
    + buildBrief(v, libraryEntries(v).filter(e => e.collection === c.id));
  function styleBrief(v, id) {
    const s = v.styles.styles.find(style => style.id === id);
    return `Build [project] for [audience].\nPrimary action: [action].\n\nAesthetic: ${s.name}\nVocabulary: ${s.vocabulary.join(', ')}\nReferences: ${s.canonical.map(c => c.name + ' ' + c.url).join('\n')}\nDirection to explore: ${s.risk}\nImage direction: ${s.imageStyle || 'Use type and layout to lead.'}\n\n${preferenceBlock(v)}Implement as a responsive interface and verify desktop and mobile in a browser.`;
  }
  const imagePrompt = e => `Vault: ${VAULT}\n${e.image_recipe}\n\nComposition: ${e.composition || 'Use the reference composition.'}\n\nUse ${referencePath(e)} as a style reference. Match treatment, texture, palette and balance while adapting the subject to our project. Return the artwork asset only; keep interface text and controls in code.`;

  Object.assign(exports, {
    inProject, libraryEntries, fitOf, verdictOf, projectName, projectGroups, groupLabel, partNames,
    styleNames, siteAddress, motionSummary, WAYS, picked, fitPasses, countFor, visibleEntries,
    visibleStyles, viewHash, readHash, buildBrief, collectionBrief, styleBrief, imagePrompt,
  });
})(typeof module === 'object' ? module.exports : (window.VaultView = {}));
