'use strict';
const $ = id => document.getElementById(id);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let DATA, STYLES, showStyles=false, fit='any', queryTests=[], sort='newest', currentId=null, toastTimer;
// Five picks, as many as a design round's round one has directions (design-round §2).
const MAX_SELECTED=5, DEFAULT_PROJECT='manta';
let project=DEFAULT_PROJECT, selected=new Set(), prefs={includeDna:false,overrides:''};
try { prefs={...prefs,...JSON.parse(localStorage.getItem('taste-vault-preferences')||'{}')}; selected=new Set(JSON.parse(localStorage.getItem('taste-vault-selection')||'[]').slice(0,MAX_SELECTED)); } catch {}
try { project=JSON.parse(localStorage.getItem('taste-vault-project'))||DEFAULT_PROJECT; } catch {}
const collectionFor = id => DATA.collections.find(c=>c.id===id);
const entryFor = id => DATA.entries.find(e=>e.id===id);
// What the page shows and copies is decided in view.js, from the view these lines hold.
const view = () => ({data:DATA,styles:STYLES,project,pick,fit,sort,showStyles,queryTests,prefs});
const projectGroups = () => VaultView.projectGroups(view());
const groupFor = id => projectGroups().find(g=>g.id===id);
const groupLabel = id => VaultView.groupLabel(view(),id);
const fitOf = e => VaultView.fitOf(view(),e);
const projectName = () => VaultView.projectName(view());
const inProject = e => VaultView.inProject(view(),e);
const libraryEntries = () => VaultView.libraryEntries(view());
const verdictOf = e => VaultView.verdictOf(view(),e);
const fitBadge = e => `<span class="fit-badge fit-${verdictOf(e)}">${esc(verdictOf(e))}</span>`;
const siteLink = e => {const site=VaultView.siteAddress(e);return site?`<a class="site-link" href="${esc(site)}" target="_blank" rel="noopener">Visit site <span aria-hidden="true">↗</span></a>`:'';};
const motionSummary = e => VaultView.motionSummary(view(),e);
const partFor = id => DATA.page_parts.find(p=>p.id===id);
const partNames = e => VaultView.partNames(view(),e);
const kindFor = id => DATA.motion_kinds.find(k=>k.id===id);
const styleFor = id => STYLES.styles.find(s=>s.id===id);
const styleNames = c => VaultView.styleNames(view(),c);
const looksFor = s => DATA.collections.filter(c=>(c.styles||[]).includes(s.id));
const dotColour = c => /^#[0-9a-f]{6}$/i.test(c?.accent||'')?c.accent:'#8b91a0';
// How each way in (view.js's WAYS) looks and where it renders: a sidebar nav, or with chips set, a chip row above the grid (#26).
const WAY_LOOKS={
 look:{label:()=>'Look',nav:'collectionNav',item:id=>{const c=collectionFor(id);return {id,name:c.name,icon:`<span class="collection-dot" style="--dot:${dotColour(c)}" aria-hidden="true"></span>`};},title:id=>collectionFor(id).name,about:()=>'A different point of view. Saved for the right project.'},
 part:{label:()=>'Page part',nav:'partChips',chips:true,item:id=>({id,name:partFor(id).name,gloss:partFor(id).gloss}),title:id=>partFor(id).name,about:id=>partFor(id).gloss+'.'},
 motion:{label:()=>'Motion',nav:'motionChips',chips:true,item:id=>({id,name:kindFor(id).name,gloss:kindFor(id).gloss}),title:id=>kindFor(id).name,about:id=>kindFor(id).gloss+'.'},
 group:{label:()=>projectName()+' group',nav:'groupNav',item:id=>({id,name:groupLabel(id),icon:'<span class="nav-icon" aria-hidden="true">◫</span>'}),title:id=>projectName()+' · '+groupLabel(id),about:id=>groupFor(id).name},
};
const WAYS=VaultView.WAYS.map(w=>({...w,...WAY_LOOKS[w.key],items:()=>w.ids(view()).map(WAY_LOOKS[w.key].item)}));
const pick=Object.fromEntries(WAYS.map(w=>[w.key,null]));
const picked = () => VaultView.picked(view()).map(w=>WAYS.find(way=>way.key===w.key));
const pickName = w => w.items().find(i=>i.id===pick[w.key])?.name||pick[w.key];
const imagePath = e => 'images/'+encodeURIComponent(e.file||e.still);
function saveLocal(key,value){try{localStorage.setItem(key,JSON.stringify(value));}catch{}}
// A toast shows for 2.6 s, carried from the seed (cth9191/taste-vault), which gives no reason.
function notify(message){clearTimeout(toastTimer); const host=[...document.querySelectorAll('dialog[open]')].at(-1)||document.body;host.append($('toast'));$('toast').textContent=message;$('toast').classList.add('show');toastTimer=setTimeout(()=>$('toast').classList.remove('show'),2600);}
function openDialog(id){$(id).showModal();}
function closeDialog(id){$(id).close();}
function tags(words){return (words||[]).map(v=>`<span>${esc(v)}</span>`).join('');}
// A keyword is a search word (#25): clicking one searches the whole library for it.
function keywordTags(words){return (words||[]).map(v=>`<button type="button" data-keyword="${esc(v)}" title="Search the library for ${esc(v)}">${esc(v)}</button>`).join('');}
// Focus goes to the box only where it opens no on-screen keyboard over the results.
function searchLibrary(text){document.querySelectorAll('dialog[open]').forEach(d=>d.close());setQuery(text);fit='any';$('fitSelect').value='any';showAll();if(matchMedia('(pointer:fine)').matches)$('searchInput').focus();}
function readHash(){
 const read=VaultView.readHash(view(),location.hash.slice(1));
 if(read.project!==project)setProject(read.project);
 Object.assign(pick,read.pick);showStyles=read.showStyles;
}
function showView(){history.replaceState(null,'','#'+VaultView.viewHash(view()));render();}
function setPick(key,id){pick[key]=id;showStyles=false;showView();}
// A sidebar click (a look or a group) clears the search, so a search never strands the new view on an empty page;
// a chip keeps it, since its counts already reflect the search (#27 Q5).
function pickWay(key,id){if(!WAYS.find(w=>w.key===key).chips)setQuery('');setPick(key,id);}
const choose = (key,id) => pickWay(key,pick[key]===id?null:id);
const clearPicks = () => WAYS.forEach(w=>pick[w.key]=null);
function showAll(){clearPicks();showStyles=false;showView();}
function showStyleGuide(){clearPicks();showStyles=true;showView();}
// A style card's look link is a sidebar click too, and its search was of styles, not references.
const openLook = id => pickWay('look',id);
// The box's words are compiled once per change, not once per reference (search.js).
function setQuery(text){$('searchInput').value=text;queryTests=VaultSearch.compile(text,DATA.design_words);}
const countFor = (w,id) => VaultView.countFor(view(),w.key,id);
const visibleEntries = () => VaultView.visibleEntries(view());
const visibleStyles = () => VaultView.visibleStyles(view());
function renderNav(){
 const library=libraryEntries(), all=!showStyles&&!picked().length;
 const nav=(attrs,classes,label,count,icon)=>`<button class="nav-item${classes}" ${attrs}>${icon}<span>${esc(label)}</span><span class="nav-count">${count}</span></button>`;
 const chip=(attrs,classes,label,count,gloss)=>`<button class="way-chip${classes}" ${attrs} title="${esc(gloss)}">${esc(label)}<span class="nav-count">${count}</span></button>`;
 $('libraryNav').innerHTML=nav('data-all'+(all?' aria-current="page"':''),all?' active':'','All references',library.length,'<span class="nav-icon" aria-hidden="true">▦</span>')+nav('data-styles'+(showStyles?' aria-current="page"':''),showStyles?' active':'','Style guide',STYLES.styles.length,'<span class="nav-icon" aria-hidden="true">◈</span>');
 // A value that would leave nothing is dimmed, never hidden, so the list keeps its shape as picks change.
 WAYS.forEach(w=>$(w.nav).innerHTML=w.items().map(i=>{const chosen=pick[w.key]===i.id, n=countFor(w,i.id);return (w.chips?chip:nav)(`data-facet="${w.key}" data-id="${esc(i.id)}" aria-pressed="${chosen}"`,(chosen?' active':'')+(n||chosen?'':' empty'),i.name,n,w.chips?i.gloss:i.icon);}).join(''));
 $('groupCount').textContent=projectGroups().length;
 $('groupHeading').textContent=projectName()+' groups';
 // A project starts with no groups (#28 Q6).
 $('groupHeading').parentElement.hidden=$('groupNav').hidden=!projectGroups().length;
 $('detailFitHeading').textContent=projectName()+' fit';
 $('collectionCount').textContent=DATA.collections.length;
 $('libraryCount').textContent=library.length+' references · '+DATA.collections.length+' looks';
 // No sidebar on a narrow screen: one select per way in with anything to pick, the Style guide last in the first.
 $('mobileNavigation').innerHTML=WAYS.filter(w=>w.items().length).map((w,index)=>`<label>${esc(w.label())} <select data-way="${w.key}"><option value="">Any</option>${w.items().map(i=>{const chosen=pick[w.key]===i.id, n=countFor(w,i.id);return `<option value="${esc(i.id)}"${chosen?' selected':''}${n||chosen?'':' disabled'}>${esc(i.name)} (${n})</option>`;}).join('')}${index?'':`<option value=":styles"${showStyles?' selected':''}>Style guide</option>`}</select></label>`).join('');
 document.querySelectorAll('[data-way]').forEach(select=>select.onchange=()=>select.value===':styles'?showStyleGuide():pickWay(select.dataset.way,select.value||null));
 document.querySelectorAll('[data-all]').forEach(button=>button.onclick=()=>showAll());
 document.querySelectorAll('[data-styles]').forEach(button=>button.onclick=showStyleGuide);
 document.querySelectorAll('[data-facet]').forEach(button=>button.onclick=()=>choose(button.dataset.facet,button.dataset.id));
}
function renderPicks(){
 const picks=picked();
 $('pickBar').hidden=!picks.length;
 $('pickBar').innerHTML=picks.map(w=>`<button class="pick-chip" data-unpick="${w.key}" aria-label="Remove ${esc(w.label())}: ${esc(pickName(w))}"><small>${esc(w.label())}</small> ${esc(pickName(w))} <span aria-hidden="true">✕</span></button>`).join('')+(picks.length>1?'<button class="pick-clear" data-clear-picks>Clear all</button>':'');
 document.querySelectorAll('[data-unpick]').forEach(button=>button.onclick=()=>setPick(button.dataset.unpick,null));
 document.querySelectorAll('[data-clear-picks]').forEach(button=>button.onclick=()=>showAll());
}
function render(){
 // The nav is rebuilt below, so the control a keyboard user just used is found again and refocused.
 const focused=document.activeElement?.dataset||{}, refocus=focused.way?`[data-way="${focused.way}"]`:focused.facet?`[data-facet="${focused.facet}"][data-id="${CSS.escape(focused.id)}"]`:null;
 renderNav();renderPicks();
 if(refocus)document.querySelector(refocus)?.focus();
 const picks=picked(), only=picks.length===1&&picks[0], list=showStyles?visibleStyles():visibleEntries();
 $('pageTitle').firstChild.textContent=showStyles?'Style guide':picks.length>1?picks.map(pickName).join(' · '):only?only.title(pick[only.key]):'All references';
 $('resultCount').textContent=list.length;
 $('pageDescription').textContent=showStyles?'Explore the visual languages behind the work.':picks.length>1?'References in every pick below.':only?only.about(pick[only.key]):'Collect what catches your eye. Make it your own.';
 $('collectionDetailsButton').hidden=!collectionFor(pick.look);
 $('browseHint').hidden=showStyles;
 $('footerCount').textContent=list.length+(showStyles?' styles':' references')+(queryTests.length?' matching “'+$('searchInput').value+'”':' in view');
 $('emptyState').hidden=list.length>0;
 $('grid').innerHTML=showStyles?list.map(styleCard).join(''):list.map(referenceCard).join('');
 document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>openReference(b.dataset.open));
 document.querySelectorAll('[data-select]').forEach(b=>b.onclick=()=>toggleSelection(b.dataset.select));
 document.querySelectorAll('[data-style-brief]').forEach(b=>b.onclick=()=>copyText(VaultView.styleBrief(view(),b.dataset.styleBrief)));
 document.querySelectorAll('[data-look]').forEach(b=>b.onclick=()=>openLook(b.dataset.look));
 document.querySelectorAll('[data-style-vocabulary]').forEach(b=>b.onclick=()=>copyText(styleFor(b.dataset.styleVocabulary).vocabulary.join(', '),'Vocabulary copied'));
 renderTray();
}
function referenceCard(e){return `<article class="reference-card" data-card="${esc(e.id)}"><button class="select-reference${selected.has(e.id)?' selected':''}" data-select="${esc(e.id)}" aria-label="${selected.has(e.id)?'Deselect':'Select'} ${esc(e.title)} for comparison" aria-pressed="${selected.has(e.id)}">${selected.has(e.id)?'✓':'+'}</button><button class="image-button" data-open="${esc(e.id)}" aria-label="Open ${esc(e.title)}"><img loading="lazy" src="${imagePath(e)}" alt="${esc(e.title)}"><span class="open-label">View reference ↗</span></button><div class="card-meta"><div><h2>${esc(e.title)}</h2><p><span class="collection-dot" style="--dot:${dotColour(collectionFor(e.collection))}" aria-hidden="true"></span>${esc(collectionFor(e.collection).name)}</p><p class="card-fit">${fitBadge(e)}${(fitOf(e)?.groups||[]).map(g=>`<span class="group-chip">${esc(groupLabel(g))}</span>`).join('')}${e.motion?'<span class="group-chip motion">motion</span>':''}</p></div><span class="card-arrow" aria-hidden="true">↗</span></div></article>`;}
function styleCard(s){return `<article class="style-card"><div class="style-preview spx-${esc(s.id)}">${SPECIMENS[s.id]||''}</div><div class="style-copy"><h2>${esc(s.name)}</h2><p>${s.recognize.map(esc).join(' · ')}</p><div class="tags">${tags(s.vocabulary)}</div>${s.warning?`<p class="style-warning">${esc(s.warning)}</p>`:''}<div class="style-links">${s.canonical.filter(c=>/^https?:\/\//.test(c.url)).map(c=>`<a href="${esc(c.url)}" target="_blank" rel="noopener noreferrer">${esc(c.name)} ↗</a>`).join('')}</div>${styleLooks(s)}<div class="style-actions"><button class="button" data-style-brief="${esc(s.id)}">Copy brief</button><button class="button quiet" data-style-vocabulary="${esc(s.id)}">Vocabulary</button></div></div></article>`;}
function renderTray(){
 $('compareTray').hidden=!selected.size;
 $('trayThumbs').innerHTML=[...selected].map(id=>{const e=entryFor(id);return `<img src="${imagePath(e)}" alt="${esc(e.title)}">`;}).join('');
 $('selectionCount').textContent=selected.size+' / '+MAX_SELECTED+' selected';
 $('compareButton').disabled=selected.size<2;
 if(currentId){$('detailSelect').textContent=selected.has(currentId)?'Remove from comparison':'Select to compare';$('detailSelect').setAttribute('aria-pressed',selected.has(currentId));}
}
function toggleSelection(id){
 const focused=document.activeElement?.dataset?.select;
 if(selected.has(id))selected.delete(id);else if(selected.size<MAX_SELECTED)selected.add(id);else{notify(MAX_SELECTED+' selected. Remove one to add another.');return;}
 saveLocal('taste-vault-selection',[...selected]);render();
 if(focused)document.querySelector(`[data-select="${CSS.escape(focused)}"]`)?.focus();
}
function openReference(id){
 const e=entryFor(id);if(!e)return;currentId=id;
 const list=visibleEntries(), at=list.findIndex(x=>x.id===id);
 $('inspectorLabel').textContent=at>=0?`Reference ${at+1} of ${list.length}`:'Reference';
 $('previousReference').disabled=at<=0;$('nextReference').disabled=at<0||at>=list.length-1;
 $('detailImage').src=imagePath(e);$('detailImage').alt=e.title;
 $('detailCollection').textContent=collectionFor(e.collection).name;$('detailTitle').textContent=e.title;$('detailDescription').textContent=e.description||'';
 $('detailSite').innerHTML=siteLink(e);$('detailParts').innerHTML=tags(partNames(e));
 const f=fitOf(e);$('detailFit').innerHTML=f?`${fitBadge(e)} ${f.sheet_section?`<span class="fit-sheet">brand sheet ${esc(f.sheet_section)}</span>`:''}<p class="fit-take">${esc(f.take)}</p>${f.groups.length?`<div class="tags">${f.groups.map(g=>`<span>${esc(groupLabel(g))}</span>`).join('')}</div>`:''}`:`${fitBadge(e)}<p class="fit-take muted">Nobody has judged this reference for ${esc(projectName())}. A verdict is written the first time a ${esc(projectName())} brief cites it.</p>`;
 $('detailNote').textContent=e.note||'A visual reference for your next project.';$('detailKeywords').innerHTML=keywordTags(e.keywords);document.querySelectorAll('[data-keyword]').forEach(b=>b.onclick=()=>searchLibrary(b.dataset.keyword));$('detailVocabulary').innerHTML=tags(e.vocabulary);$('detailVocabulary').parentElement.hidden=!e.vocabulary?.length;
 $('detailMotion').hidden=!e.motion;if(e.motion)$('detailMotionBody').textContent=motionSummary(e);
 $('detailPlacement').textContent=e.composition||(e.url?'A site entry carries no composition; see Motion.':'Use the reference to guide composition and hierarchy.');$('detailRecipe').textContent=e.image_recipe||'No image recipe saved.';$('copyImagePrompt').disabled=!e.image_recipe;
 $('detailPreferenceStatus').textContent=(prefs.includeDna?'Includes your general preferences.':'Reference-led brief · House DNA is off.')+(prefs.overrides.trim()?' Project notes included.':'');
 $('imageStage').classList.remove('zoomed');$('zoomButton').textContent='Zoom in';$('zoomButton').setAttribute('aria-pressed','false');
 renderTray();if(!$('inspector').open)openDialog('inspector');$('imageStage').scrollTop=0;$('imageStage').scrollLeft=0;document.querySelector('.detail-panel').scrollTop=0;
}
function navigateReference(delta){const list=visibleEntries(), index=list.findIndex(e=>e.id===currentId);if(index>=0&&list[index+delta])openReference(list[index+delta].id);}
// A compared reference shows four of its keywords and terms: a guess at what fits its card.
function openComparison(){
 const entries=[...selected].map(entryFor);if(entries.length<2)return;
 $('comparisonGrid').style.setProperty('--compare-columns',entries.length);
 $('comparisonGrid').innerHTML=entries.map(e=>`<article class="compare-item"><div class="compare-image"><img src="${imagePath(e)}" alt="${esc(e.title)}"></div><h3>${esc(e.title)}</h3><p class="detail-family">${esc(collectionFor(e.collection).name)} · ${fitBadge(e)}</p>${siteLink(e)}<div class="tags">${tags([...(e.keywords||[]),...(e.vocabulary||[])].slice(0,4))}</div><p>${esc(e.note)}${fitOf(e)?' <em>'+esc(projectName())+' take: '+esc(fitOf(e).take)+'</em>':''}</p><button class="button" data-inspect="${esc(e.id)}">Inspect reference ↗</button></article>`).join('');
 document.querySelectorAll('[data-inspect]').forEach(b=>b.onclick=()=>openReference(b.dataset.inspect));openDialog('comparison');
}
// Counts what openLook will show: the Style guide holds no picks, and openLook clears the search.
function styleLooks(s){const looks=looksFor(s);return looks.length?`<div class="style-looks"><h3>Your looks that share it</h3><div class="tags">${looks.map(c=>`<button type="button" data-look="${esc(c.id)}" title="Open ${esc(c.name)}">${esc(c.name)} <span class="nav-count">${libraryEntries().filter(e=>e.collection===c.id&&VaultView.fitPasses(view(),e)).length}</span></button>`).join('')}</div></div>`:'';}
async function copyText(text,message='Brief copied'){
 try{await navigator.clipboard.writeText(text);notify(message);}catch{$('copyFallback').value=text;if(!$('copyDialog').open)openDialog('copyDialog');$('copyFallback').focus();$('copyFallback').select();}
}
function openCollection(){const c=collectionFor(pick.look);if(!c)return;$('collectionDialogTitle').textContent=c.name;$('collectionDescription').textContent=c.description;$('collectionUse').textContent=c.deployFor;$('collectionVocabulary').innerHTML=tags(c.vocabulary);$('collectionStyles').textContent=styleNames(c).join(', ');$('collectionStyles').parentElement.hidden=!c.styles?.length;$('collectionRisk').textContent=c.risk;openDialog('collectionDialog');}
function openPreferences(){$('includeDna').checked=!!prefs.includeDna;$('projectOverrides').value=prefs.overrides;$('dnaConstants').innerHTML=DATA.dna.constants.map(s=>`<li>${esc(s)}</li>`).join('');$('dnaConstants').parentElement.hidden=!DATA.dna.constants.length;$('dnaNever').innerHTML=DATA.dna.never.map(s=>`<li>${esc(s)}</li>`).join('');openDialog('preferences');}
function renderProjectOptions(){
 $('projectSelect').innerHTML=Object.entries(DATA.projects||{}).map(([key,p])=>`<option value="${esc(key)}">${esc(p.name||key)}</option>`).join('');
 $('projectSelect').value=project;
 $('fitSelect').innerHTML=['any',...(DATA.projects?.[project]?.verdicts||[]),'unjudged'].map(v=>`<option value="${esc(v)}">${esc(v==='any'?'Any':v[0].toUpperCase()+v.slice(1))}</option>`).join('');
 $('fitSelect').value=fit;
}
function setProject(key){
 project=key;fit='any';saveLocal('taste-vault-project',project);renderProjectOptions();
 selected=new Set([...selected].filter(id=>inProject(entryFor(id))));saveLocal('taste-vault-selection',[...selected]);
 // A pick the new project does not offer (its groups, the page parts its references hold) is dropped.
 WAYS.forEach(w=>{if(!w.items().some(i=>i.id===pick[w.key]))pick[w.key]=null;});
}
function chooseProject(key){setProject(key);showView();}
async function boot(){
 try{
  // Opened from its folder, the page loads data/vault-data.js, since a browser refuses fetch() on file:// (#32).
  if(location.protocol==='file:'){await new Promise((loaded,failed)=>{const s=document.createElement('script');s.src='data/vault-data.js';s.onload=loaded;s.onerror=()=>failed(new Error('The copy of your library this page reads is missing — ask Claude to run node bundle.js.'));document.head.append(s);});({gallery:DATA,styles:STYLES}=window.VAULT_DATA);}
  else [DATA,STYLES]=await Promise.all(['data/gallery.json','data/styles.json'].map(async url=>{const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw new Error('Unable to load your library.');return r.json();}));
  if(!Object.hasOwn(DATA.projects||{},project))project=Object.keys(DATA.projects||{})[0]||DEFAULT_PROJECT;
  renderProjectOptions();
  $('browseHint').firstElementChild.textContent=`Select up to ${MAX_SELECTED} references to compare`;
  selected=new Set([...selected].filter(id=>entryFor(id)&&inProject(entryFor(id))));readHash();showView();
 }catch(error){$('grid').innerHTML=`<div class="empty-state"><h2>Your library couldn't load</h2><p>${esc(error.message)} Refresh the page to try again.</p></div>`;return;}
 $('searchInput').oninput=event=>{setQuery(event.target.value);render();};$('sortSelect').onchange=event=>{sort=event.target.value;render();};
 $('resetSearch').onclick=()=>searchLibrary('');
 $('clearSelection').onclick=()=>{selected.clear();saveLocal('taste-vault-selection',[]);render();};$('compareButton').onclick=openComparison;$('copyCombinedBrief').onclick=()=>copyText(VaultView.buildBrief(view(),[...selected].map(entryFor)));
 $('detailSelect').onclick=()=>toggleSelection(currentId);$('copyReferenceBrief').onclick=()=>copyText(VaultView.buildBrief(view(),[entryFor(currentId)]));$('copyImagePrompt').onclick=()=>copyText(VaultView.imagePrompt(entryFor(currentId)),'Image prompt copied');
 $('previousReference').onclick=()=>navigateReference(-1);$('nextReference').onclick=()=>navigateReference(1);
 $('zoomButton').onclick=()=>{const zoomed=$('imageStage').classList.toggle('zoomed');$('zoomButton').textContent=zoomed?'Fit image':'Zoom in';$('zoomButton').setAttribute('aria-pressed',zoomed);};
 $('preferencesButton').onclick=openPreferences;$('savePreferences').onclick=()=>{prefs={includeDna:$('includeDna').checked,overrides:$('projectOverrides').value};saveLocal('taste-vault-preferences',prefs);closeDialog('preferences');notify('Preferences saved');};
 $('collectionDetailsButton').onclick=openCollection;
 $('copyCollectionBrief').onclick=()=>copyText(VaultView.collectionBrief(view(),collectionFor(pick.look)));
 $('copyCollectionVocabulary').onclick=()=>copyText(collectionFor(pick.look).vocabulary.join(', '),'Vocabulary copied');
 document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>closeDialog(b.dataset.close));
 document.querySelectorAll('dialog').forEach(dialog=>{dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();});dialog.addEventListener('close',()=>{if(dialog.contains($('toast')))document.body.append($('toast'));});});
 window.addEventListener('hashchange',()=>{readHash();showView();});
 $('fitSelect').onchange=event=>{fit=event.target.value;render();};
 $('projectSelect').onchange=event=>chooseProject(event.target.value);
 document.addEventListener('keydown',event=>{const editing=/INPUT|TEXTAREA|SELECT/.test(event.target.tagName);if(event.key==='/'&&!editing&&!document.querySelector('dialog[open]')){event.preventDefault();$('searchInput').focus();}if($('inspector').open&&!editing&&!$('copyDialog').open){if(event.key==='ArrowLeft')navigateReference(-1);if(event.key==='ArrowRight')navigateReference(1);}});
}
boot();
