# Lookup walk on the library page (design-vault#20)

⚠ **Bound 2026-09-30 (#38): the collection ids and names below are as they stood before #38 regrouped the library into #24's 16 looks. `painterly-portrait` and `glitched-antiquity` no longer exist: their members are in `illustrated-storybook` (now named Painted Illustration) and `classical-remix` (now named Old Masters Meet Tech). `data/gallery.json` holds the current names.**

Ticket: lucmoseley/design-vault#20, under the wayfinder map #17.
Question: for the searches that the founder makes, how many clicks does each search need on the library page today? Is the route clear? When a search fails, is the cause the organisation, or does the library not hold the reference?

## Method

- Source of the page: `index.html`, `app.js` (commit 2482d69). Data: `data/gallery.json` (92 entries), `data/styles.json` (18 styles).
- I read all 92 entries (title, description, note, keywords, vocabulary, Manta fit take, fit groups, motion, first 260 characters of composition).
- Project picker: the page selects "Manta" by default (`DEFAULT_PROJECT='manta'`, `app.js`). Manta is the only project in `data/gallery.json`. No entry has a `project` field, thus all 92 entries show for Manta. All 92 entries have a Manta fit verdict. The Fit filter has these values: Any, On-brand, Adapt, Off-brand, Unjudged.
- The sidebar has: "All references" (92), "Style guide" (18), 16 collections, and 7 "Manta surfaces".
- The search box matches a lowercase substring against this joined text: title, description, note, keywords, vocabulary, collection name, Manta fit take (`visibleEntries()`, `app.js`). It does not search `composition`, `mood`, `founder_note`, `motion`, `image_recipe` or the collection description. Search applies inside the current sidebar view. It does not reset the view.

- Walk method: I drove the real page with headless Chromium (Python Playwright 1.61) at 1440 × 900 px. A static server in the same script served the repo root. For each route, the script loaded the page fresh, clicked the sidebar item, set the Fit value, and typed the search words. Then it read the card ids in grid order. The scripts and raw output are in `.claude/tmp/walk.py`, `walk-searches.json`, `walk-out.json` and `walk-scored.txt`.
- Start state (measured): the page opens on "All references" with 92 cards. Fit is "Any". Sort is "Newest first".
- Sidebar counts (measured): collections Monumental Editorial 5, Product-Led Minimalism 3, Technical Systems 5, Luminous Futurism 3, Cinematic Still Life 2, Print-Tech Paper 6, Dither Mono 5, Vast Quiet Cinematic 12, Data-as-Texture 5, Classical Remix 3, Glitched Antiquity 2, Illustrated Storybook 14, Flat Poster 17, Mascot Illustration 5, Ink & Botanical 2, Painterly Portrait 3. Manta surfaces: Hero art 41, Page background art 20, Destination art 17, Footer scene 4, Mascot renderings 5, UI chrome and cards 9, Motion references 9.
- Fit filter counts (measured, whole library): On-brand 7, Adapt 64, Off-brand 21, Unjudged 0.

### How I count clicks

- One sidebar item is 1 click.
- One search is 1 click in the box (or the "/" key), then typed words. I write this as "1 + words".
- One Fit value is 2 clicks (open the list, then select).
- In the first screen, 3 cards show fully (one row of 3). The second row shows only partly. Thus a first right reference at position 1 to 3 needs no scroll. At position 4 to 6 it is partly visible. At position 7 or more, the user must scroll.
- "Right" means that I read the entry and it answers the search. "Wrong" means a false hit. "Held" is the number of right entries in all of `data/gallery.json`.

## The searches

### S1. Footer animation

Held: 1 (`site-eaglesnest`, a footer where a dot grows beside each link on hover). The 4 "Footer scene" entries are still pictures for a footer.

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Surface "Footer scene" | 4 | 0 | 4 | none | 1 |
| Surface "Motion references" | 9 | 1 | 8 | 7 | 1 + scroll |
| Search "footer animation" | 0 | 0 | 0 | none | 1 + words |
| Search "animation" / "animated" | 0 | 0 | 0 | none | 1 + words |
| Search "motion" | 7 | 0 | 7 | none | 1 + words |
| Search "footer" | 8 | 1 | 7 | 3 | 1 + words |
| Search "hover" | 3 | 1 | 2 | 3 | 1 + words |
| "Motion references" + search "footer" | 1 | 1 | 0 | 1 | 2 + words |

- Obvious route: a first-time user clicks "Footer scene". It shows 4 still pictures and no animation. The user then types "footer animation" and gets "No references found".
- The letters "animat" occur in no searched field of any entry. They occur only in fields that search does not read: `motion` (5 entries), `founder_note` (1) and `image_recipe` (3). None of these is the footer entry. The card shows a "motion" chip, but the search word "motion" misses the right entry.
- Cause: mostly not held (1 entry). The organisation hides the 1 entry: the surface named "Footer scene" does not contain it.

### S2. A hero with one big photo

Held: 15. Still photos: `ctgt-hero`, `ctgt-alt`, `nexora`, `prompting-company`, `visora`, `royal-gambit-chess`, `root-soil-golden-fields`, `site-izanami`, `drone-from-above`, `drone-see-to-sea`, `rooted-textile-landscape`, `crix-dreamscape-product` (12). Moving photo heroes: `site-khufus` (film), `site-dock` (film), `site-flyward` (photo that opens on scroll) (3). None of the 15 is On-brand for Manta: the brand sheet keeps photos to listings (take on `drone-from-above`, §9).

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Surface "Hero art" | 41 | 9 | 32 | 3 | 1 |
| Collection "Vast Quiet Cinematic" | 12 | 10 | 2 | 1 | 1 |
| Search "hero" | 11 | 4 | 7 | 6 | 1 + words |
| Search "big photo" / "hero photo" | 0 | 0 | 0 | none | 1 + words |
| Search "photo" | 40 | 15 | 25 | 2 | 1 + words |
| Search "photographic" | 31 | 15 | 16 | 2 | 1 + words |
| Search "full-bleed" | 5 | 1 | 4 | 3 | 1 + words |
| "Hero art" + search "photographic" | 20 | 9 | 11 | 2 | 2 + words |
| "Hero art" + Fit "On-brand" | 2 | 0 | 2 | none | 3 |

- Obvious route: "Hero art" (1 click). A right card is in the first row, but 32 of 41 cards are wrong. "Hero art" mixes photos, paintings, portraits, 3D renders and web pages.
- Best route: "Vast Quiet Cinematic" (10 of 12 right). A first-time user does not connect that name to "one big photo".
- The word "hero" finds only 11 entries. The descriptions say "opening section" or "opening screen" (the plain-English register in `CLAUDE.md`), so the design word misses most heroes.
- Cause: organisation and vocabulary. The library holds the references.

### S3. A pricing table

Held: 1, and only as a part. `crix-dreamscape-product` is a full-page screenshot. One of its sections is a pricing block with three plan cards. It is Off-brand for Manta.

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Surface "UI chrome and cards" | 9 | 0 | 9 | none | 1 |
| Collection "Product-Led Minimalism" | 3 | 0 | 3 | none | 1 |
| Search "pricing" | 1 | 1 | 0 | 1 | 1 + words |
| Search "pricing table" | 0 | 0 | 0 | none | 1 + words |
| Search "price" | 0 | 0 | 0 | none | 1 + words |
| Search "table" | 3 | 0 | 3 | none | 1 + words |
| Search "plan" | 12 | 1 | 11 | 4 | 1 + words |

- Obvious route: "UI chrome and cards" (0 right), then "pricing table" (0 results). Only the single word "pricing" finds the one entry. Its card title ("CRIX - Dreamscape Product") does not say "pricing".
- Cause: not held. The library has no reference saved for its pricing table.

### S4. A playful loading state

Held: 1, and only as a part. `site-growon` drops its desk objects in one by one while it loads ("Setting the scene…"). The Manta take rejects that bouncing drop-in.

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Surface "Motion references" | 9 | 1 | 8 | 8 | 1 + scroll |
| Surface "Mascot renderings" | 5 | 0 | 5 | none | 1 |
| Search "loading" / "loader" / "spinner" / "playful" | 0 | 0 | 0 | none | 1 + words |
| Search "load" | 2 | 1 | 1 | 2 | 1 + words |
| Search "empty state" | 2 | 0 | 2 | none | 1 + words |

- Obvious route: search "loading" or "playful". Both give 0 results. The card title of the one entry ("GROWON — a home-screen desk scene you play with; the record player plays music") does not say "loading".
- Cause: not held.

### S5. A dark editorial page

Held: 0 complete dark editorial pages (dark ground, several sections, magazine-style type). Held as a part: 8 dark opening screens where big type leads: `royal-gambit-chess`, `yieldstream`, `cogni`, `monolith`, `drone-mapping-os`, `stardust-pixel-light`, `nightlife-refined`, `nebula-luminous-flower`. 7 of these 8 are Off-brand for Manta. The 8 are in 6 different collections.

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Collection "Monumental Editorial" | 5 | 0 | 5 | none | 1 |
| Collection "Luminous Futurism" | 3 | 2 | 1 | 1 | 1 |
| Collection "Glitched Antiquity" | 2 | 2 | 0 | 1 | 1 |
| Collection "Cinematic Still Life" | 2 | 1 | 1 | 1 | 1 |
| Search "dark editorial" | 0 | 0 | 0 | none | 1 + words |
| Search "editorial" | 8 | 0 | 8 | none | 1 + words |
| Search "dark" | 57 | 7 | 50 | 2 | 1 + words |
| Search "night" | 19 | 8 | 11 | 1 | 1 + words |
| Search "black" | 37 | 6 | 31 | 2 | 1 + words |
| "Monumental Editorial" + search "dark" | 2 | 0 | 2 | none | 2 + words |
| "Style guide" + search "dark" | 2 style cards | — | — | — | 2 + words |

- Obvious route: "Monumental Editorial" (1 click). All 5 entries are light pages. Then "dark editorial" gives 0 results. The word "dark" gives 57 cards, because the descriptions use "dark" for many colours (53 of 57 hits come without the fit take).
- "Night" is the best route (8 of 19 right). A first-time user does not expect the word "night" to tag dark pages.
- The Style guide shows a "Cinematic Dark" style card. It is a style with outside links. It is not a library reference.
- Cause: mostly not held (no complete page). The organisation also hides the 8 parts: there is no "dark" filter, and the "Editorial" collection holds only light pages.

### S6. A night sea scene

Held: 0 pictures of the sea at night. `site-makemepulse` has one night-ocean chapter inside a site, but its still does not show it. Usable stand-ins for the Manta night footer: 2 (`turtles1`, `sumi`: sparse marks, which the takes say to flip to white on the night ground).

| Route | Shows | Right or stand-in | Wrong | First at | Clicks |
|---|---|---|---|---|---|
| Surface "Footer scene" | 4 | 2 | 2 | 1 | 1 |
| Search "night sea" | 0 | 0 | 0 | none | 1 + words |
| Search "night" | 19 | 3 | 16 | 7 | 1 + words + scroll |
| Search "sea" | 25 | 2 | 23 | 11 | 1 + words + scroll |
| Search "ocean" | 2 | 1 | 1 | 2 | 1 + words |
| Search "stars" | 3 | 1 | 2 | 3 | 1 + words |
| Search "seascape" | 11 | 1 | 10 | 7 | 1 + words + scroll |

- Obvious route: "Footer scene" (1 click) gives the 2 stand-ins at once. They are daytime ink drawings on white, not night scenes.
- Cause: not held.

### S7. A mascot

Held: 6: `manta-porcelain`, `decorative-manta`, `rating-or-bkg-art`, `galaxy-manta`, `zentangle-manta` (5 manta mascots) and `dribbble1` (a creature as the whole picture).

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Collection "Mascot Illustration" | 5 | 5 | 0 | 1 | 1 |
| Surface "Mascot renderings" | 5 | 5 | 0 | 1 | 1 |
| Search "mascot" | 11 | 6 | 5 | 2 | 1 + words |
| Search "manta" | 52 | 6 | 46 | 8 | 1 + words + scroll |
| Search "character" | 7 | 2 | 5 | 1 | 1 + words |
| Search "creature" | 3 | 2 | 1 | 1 | 1 + words |

- Obvious route: "Mascot Illustration" or "Mascot renderings" (1 click). Both are clean. Each misses one entry (the collection misses `zentangle-manta`, which is in Ink & Botanical; the surface misses the stag).
- Search "manta" is noisy: 52 hits, of which 47 come only from the Manta fit take.
- Cause: none. This search works.

### S8. Grain texture

Held: 22 entries with a visible grain, speckle, paper or halftone finish: `site-kellywallace`, `algarve`, `dribbble1`, `dribbble2`, `dribbble3`, `fujiskyline`, `vietnam`, `local-waterfall`, `behance1`, `rating-or-bkg-art`, `dribbble4`, `dribbble5`, `rooted-textile-landscape`, `stillpage`, `sails-collage`, `roamfield`, `monolith`, `castle`, `asterisk-login`, `dark-login-rock`, `break-the-pattern`, `dualite`. The keyword `grain` is on 38 entries. For 18 of those 38, the description shows no grain (for example `ctgt-hero`, `prompting-company`, `climora`, `spade`). `dribbble3` and `vietnam` have grain but no `grain` keyword.

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Collection "Print-Tech Paper" | 6 | 5 | 1 | 1 | 1 |
| Collection "Dither Mono" | 5 | 4 | 1 | 1 | 1 |
| Search "grain" | 40 | 22 | 18 | 5 | 1 + words |
| Search "grainy" | 8 | 8 | 0 | 1 | 1 + words |
| Search "texture" | 30 | 18 | 12 | 2 | 1 + words |
| Search "paper" | 13 | 10 | 3 | 1 | 1 + words |
| Search "noise" | 0 | 0 | 0 | none | 1 + words |
| "Page background art" + search "grain" | 8 | 8 | 0 | 1 | 2 + words |

- Obvious route: search "grain" (1 + words). It shows all 22, but 18 of 40 cards are false hits, and the first right card is at position 5.
- Cause: organisation (loose keyword tagging). The library holds the references.

### S9. A navigation bar

Held: 0 references saved for their navigation bar. No note is about a menu. Held as a visible part: 5 entries with a distinct menu bar (`bloomy-paris-builder`, `stillpage`, `roamfield`, `sakura-cosmic-tree`, `sumi`). 28 entries mention a menu in passing.

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Surface "UI chrome and cards" | 9 | 0 | 9 | none | 1 |
| Search "navigation" | 2 | 2 | 0 | 1 | 1 + words |
| Search "nav" | 8 | 5 | 3 | 1 | 1 + words |
| Search "menu" | 28 | 5 | 23 | 6 | 1 + words |
| Search "header" / "navbar" | 0 | 0 | 0 | none | 1 + words |

- Obvious route: "UI chrome and cards" (0 right), or search "navigation" (2 right). The 5 hits show a menu bar only at the top of a larger page.
- Cause: not held as a subject.

### S10. Scroll-driven motion

Held: 4 (`site-visiblecuration`, `site-izanami`, `site-flyward`, `site-everswap`). `site-khufus` also changes its page colour on scroll, as a part.

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Surface "Motion references" | 9 | 4 | 5 | 1 | 1 |
| Search "scroll" | 11 | 4 | 7 | 3 | 1 + words |
| Search "scroll-driven" | 3 | 3 | 0 | 1 | 1 + words |
| Search "scrolling" | 3 | 3 | 0 | 1 | 1 + words |
| Search "parallax" | 1 | 1 | 0 | 1 | 1 + words |
| "Motion references" + Fit "On-brand" | 0 | 0 | 0 | none | 3 |

- Obvious route: "Motion references" (1 click). The titles say "as you scroll", so a user can pick the 4 from the 9.
- Cause: none. This search works. No motion reference is On-brand; all 9 are Adapt.

### S11. A travel poster

Held: 12 (`algarve`, `cambodia`, `phillip-island`, `normandie`, `dribbble2`, `canyonlands`, `chinagreatwall`, `fujiskyline`, `greece`, `luxembourg`, `rome`, `vietnam`).

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Collection "Flat Poster" | 17 | 12 | 5 | 1 | 1 |
| Surface "Destination art" | 17 | 7 | 10 | 4 | 1 |
| Search "travel poster" | 5 | 5 | 0 | 1 | 1 + words |
| Search "poster" | 19 | 12 | 7 | 1 | 1 + words |
| Search "travel" | 11 | 5 | 6 | 1 | 1 + words |
| "Flat Poster" + Fit "On-brand" | 7 | 5 | 2 | 1 | 3 |

- Obvious route: "Flat Poster" (1 click). The 5 wrong cards are near misses (web-page heroes and one top-down scene).
- Search "travel poster" finds only 5 of 12. The collection description says "Travel-poster pictures", but search does not read collection descriptions.
- Cause: none. This search works.

### S12. A login or sign-up page

Held: 5 (`asterisk-login`, `dark-login-rock`, `journey-ascii-login`, `castle` and `vitra`, the last two are waitlist sign-up pages).

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Collection "Dither Mono" | 5 | 3 | 2 | 2 | 1 |
| Surface "UI chrome and cards" | 9 | 4 | 5 | 5 | 1 |
| Search "login" | 3 | 3 | 0 | 1 | 1 + words |
| Search "waitlist" | 2 | 2 | 0 | 1 | 1 + words |
| Search "sign in" | 2 | 0 | 2 | none | 1 + words |
| Search "sign up" | 2 | 0 | 2 | none | 1 + words |
| Search "form" | 18 | 4 | 14 | 13 | 1 + words + scroll |

- Obvious route: search "login" (3 of 5). "Sign in" and "sign up" find only pages with a button of that name.
- Cause: vocabulary. The library holds the references.

### S13. Art that fades into the page with no edge (the founder's background-art principle, mantahostels#3057)

Held: 13 (`algarve`, `yosemite`, `normandie`, `wanderwell1`, `wanderwell2`, `wanderwell3`, `wanderwell4`, `site-khufus`, `site-kellywallace`, `site-dock`, `root-soil-golden-fields`, `crix-dreamscape-product`, `juris`). They are in 5 collections and 4 surfaces.

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Surface "Page background art" | 20 | 5 | 15 | 1 | 1 |
| Search "fade" | 22 | 7 | 15 | 2 | 1 + words |
| Search "into the page" | 7 | 7 | 0 | 1 | 1 + words |
| Search "melt" | 6 | 5 | 1 | 1 | 1 + words |
| Search "haze" | 11 | 3 | 8 | 1 | 1 + words |
| Search "no edge" | 3 | 2 | 1 | 1 | 1 + words |
| Search "seamless" | 1 | 1 | 0 | 1 | 1 + words |

- Obvious route: "Page background art" (1 click). It shows 5 of 13, among 15 other cards.
- No single route shows more than 7 of the 13. The idea lives only in the note prose, in different words (fade, melt, no edge, into the page).
- Cause: organisation. The library holds the references.

### S14. A hover effect

Held: 3 (`site-eaglesnest`, `site-growon`, `site-dock`).

| Route | Shows | Right | Wrong | First right at | Clicks |
|---|---|---|---|---|---|
| Surface "Motion references" | 9 | 3 | 6 | 2 | 1 |
| Search "hover" | 3 | 2 | 1 | 2 | 1 + words |
| Search "pointer" | 2 | 2 | 0 | 1 | 1 + words |
| Search "point at" | 2 | 2 | 0 | 1 | 1 + words |
| Search "interaction" / "micro-interaction" | 0 | 0 | 0 | none | 1 + words |

- Obvious route: "Motion references" or search "hover". Both work. "Hover" misses `site-growon`, which says "point at". The word "hover" is in the `motion` field of 5 entries, but search does not read that field.
- Cause: none serious.

## Other measured facts

- Routes walked: 107 plus 12 Fit routes. Of the 74 search-only routes, 18 returned "No references found": "footer animation", "animation", "animated", "big photo", "hero photo", "price", "pricing table", "loading", "loader", "playful", "spinner", "dark editorial", "night sea", "noise", "header", "navbar", "micro-interaction", "interaction".
- Search reads the whole phrase as one string. Thus a two-word phrase finds only entries that contain those exact two words together. I also tested a word-by-word match (all words, any order) with a copy of the `visibleEntries()` logic. It does not rescue the not-held searches: "footer animation" 0, "pricing table" 0, "playful loading" 0, "dark editorial" 3 (none right). It helps only "hero photo" (5 hits, 4 right) and "night sea" (3 hits, 2 stand-ins).
- The Fit filter is not a way in. Adapt holds 64 of 92 entries. On-brand holds 7, all flat illustrations (5 destination posters and 2 Studio Wanderwell heroes). It narrows a view after the user finds it.
- From the code, not walked: a search stays active when the user clicks a sidebar item (`setActive()` does not clear `query`). A user who searched and then clicks a collection sees that collection filtered by the old words, or an empty page.
- From the code, not walked: on a narrow screen the sidebar is replaced by one "Collection" drop-down list with all 16 collections, 7 surfaces and the Style guide.

## Summary: one row per search

"Obvious route" is the route that a first-time user tries first, in my judgement. "Clicks" is the clicks until the first right card shows.

| # | Search | Obvious route and result | Best route found | Clicks (best) | Held | Verdict |
|---|---|---|---|---|---|---|
| S1 | Footer animation | "Footer scene": 0 of 4 right. Then "footer animation": 0 results | "Motion references" + "footer": 1 of 1 | 2 + words | 1 | Not held (1), and the surface name misleads |
| S2 | Hero with one big photo | "Hero art": 9 of 41 right, first at 3 | "Vast Quiet Cinematic": 10 of 12 | 1 | 15 (0 On-brand) | Held; noisy; best route not obvious |
| S3 | Pricing table | "UI chrome and cards": 0 of 9. Then "pricing table": 0 | Search "pricing": 1 of 1 | 1 + words | 1 part | Not held |
| S4 | Playful loading state | Search "loading" or "playful": 0 | Search "load": 1 of 2 | 1 + words | 1 part | Not held |
| S5 | Dark editorial page | "Monumental Editorial": 0 of 5. Then "dark editorial": 0 | Search "night": 8 of 19 | 1 + words | 0 complete, 8 parts | Mostly not held; parts spread over 6 collections |
| S6 | Night sea scene | "Footer scene": 2 stand-ins of 4 | Same | 1 | 0 | Not held |
| S7 | Mascot | "Mascot Illustration": 5 of 5 | Same, or search "mascot" (6 of 11) | 1 | 6 | Found |
| S8 | Grain texture | Search "grain": 22 of 40, first at 5 | Search "grainy": 8 of 8 | 1 + words | 22 | Held; noisy keywords |
| S9 | Navigation bar | "UI chrome and cards": 0 of 9 | Search "nav": 5 of 8 | 1 + words | 0 as a subject, 5 parts | Not held |
| S10 | Scroll-driven motion | "Motion references": 4 of 9, first at 1 | Search "scroll-driven": 3 of 3 | 1 | 4 | Found |
| S11 | Travel poster | "Flat Poster": 12 of 17, first at 1 | Same | 1 | 12 | Found |
| S12 | Login or sign-up page | Search "login": 3 of 3 | "login" plus "waitlist" | 1 + words | 5 | Found in part; word choice matters |
| S13 | Art that fades into the page | "Page background art": 5 of 20 | Search "into the page": 7 of 7 | 1 + words | 13 | Held; hard to find (spread over 5 collections, 4 surfaces) |
| S14 | Hover effect | "Motion references": 3 of 9, first at 2 | Search "pointer" or "point at": 2 of 2 | 1 + words | 3 | Found |

Tally: 4 searches work well (S7, S10, S11, S14). 4 are held but noisy or hard to find (S2, S8, S12, S13). 6 are not held, or held only as a small part of a larger picture (S1, S3, S4, S5, S6, S9). Of the 5 named searches, 4 are not held (S1, S3, S4, S5). Only S2 is held, and none of its 15 references is On-brand for Manta.

## The three failures that most block the founder

1. **The library does not hold page parts.** Four of the five named searches (footer animation, pricing table, playful loading state, dark editorial page) have 0 or 1 reference, and that one is a small part of a larger picture. A night sea scene and a navigation bar are also not held. The library is mostly pictures and opening screens: "Hero art" 41, "Page background art" 20, "Destination art" 17. Login pages (5) are the exception. These searches need new references.
2. **The sidebar sorts by look and by Manta placement, not by the founder's questions.** The 16 collections are style names ("Vast Quiet Cinematic", "Dither Mono", "Monumental Editorial"). The 7 surfaces say where art goes on Manta. No sidebar item groups by page part, by kind of motion, by dark or light ground, or by technique. Thus the obvious route fails or misleads: "Footer scene" has no footer animation, "UI chrome and cards" has no pricing table or menu, "Monumental Editorial" has no dark page, and "Hero art" is 78% wrong for a photo hero. The best photo-hero route is "Vast Quiet Cinematic", which a first-time user does not pick. The 13 references for "art that fades into the page" are in 5 collections and 4 surfaces, and no route shows more than 7.
3. **Search misses the founder's words and adds false hits.** It matches the whole phrase as one string, so natural two-word phrases give nothing: 18 of 74 searches gave 0 results. It does not read the `motion` field (where "scroll", "hover" and "animation" live), the collection description or `founder_note`. The plain-English descriptions replace design words ("opening screen" for "hero"), so "hero" finds 11 of 41 hero references and "animation", "loading", "header" and "noise" find nothing. It also reads the Manta fit take and loose keywords: "manta" gives 52 hits for 6 right, "dark" 57 for 7, "grain" 40 for 22.

Bound: I read all 92 entries in `data/gallery.json` exhaustively (title, description, note, keywords, vocabulary, Manta fit verdict, take and groups, motion trigger, property and purpose note) and all of `index.html` and `app.js`. I read only the first 260 characters of each `composition`, and I did not read `image_recipe`, `mood` or `founder_note` except by string search. I did not open the images, so "right" rests on the written description of each picture. I listed the 18 style names and "recognize" lines in `data/styles.json` and did not read the rest. I walked 119 routes in headless Chromium at one desktop size (1440 × 900); I did not walk the narrow-screen layout, and the search-then-sidebar behaviour comes from code reading only.
