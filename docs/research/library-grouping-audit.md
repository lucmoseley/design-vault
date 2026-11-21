# Research: how the 92 references are grouped today (design-vault#21)

⚠ **Bound 2026-09-30 (#23): the three open questions at the end of this file now belong to #29 (how a reference gets its page part and motion kind), not #23. They are asked when the existing references are tagged.**

⚠ **Bound 2026-09-30 (#24): the split, merge and move options in §1.3 and §1.4, the eight strong second collections in §1.2, and the Style guide relation in §2 are decided in #24 (the collections decision). The weaker second collections in §1.2 stay where they are.**

⚠ **Bound 2026-09-30 (#29): the three open questions at the end are settled in #29 (how a reference gets its page part and motion kind), and none of them is asked. The six paintings take "Art only" whatever they were saved for. site-kellywallace's founder note ("has a great feel to the artwork") answers its question. asterisk-login leaves Destination art, and spade stays. The §5 and §6 draft tags, in #23's names and with #29's changes, are now what the backfill applies. The vocabularies in §5.1 and §6.1 are replaced by #29's lists.**
<!-- concision mark 1: see Concision marks -->

⚠ **Bound 2026-09-30 (#38): the collection ids and names below are as they stood before #38 regrouped the library into #24's 16 looks. `painterly-portrait` and `glitched-antiquity` no longer exist: their members are in `illustrated-storybook` (now named Painted Illustration) and `classical-remix` (now named Old Masters Meet Tech). `data/gallery.json` holds the current names.**

Ticket: lucmoseley/design-vault#21, under the wayfinder map #17.
Status: draft evidence for a decision. The draft tags in this file are not data. Do not copy them into `data/gallery.json`.

## Sources

- `data/gallery.json` at commit 2482d69: all 92 entries, the 16 `collections`, `keywords_allowed`, `keyword_families`, `projects.manta.groups`. I read each entry: title, description, note, keywords, vocabulary, composition, fit, and the `motion` block on the 10 site entries.
- `data/styles.json`: all 18 styles.
- `app.js` line 39 (`visibleEntries`) and line 37 (`tags`), and `index.html` line 31: the page filters and the search box.
- `plugin/skills/design-project/SKILL.md` line 56: the website surface list.

## Where the entries come from


| Source (`source` field) | Entries | What they are |
|---|---|---|
| `cth9191/taste-vault` (Chase's screenshots) | 46 | Full web pages: headline, menu, buttons and one picture. Added 20 Jul and 8 Sep 2026. |
| The founder's `brand_assets` folder, Dribbble, Behance, Firefly, his own screenshots | 36 | Mostly artwork with no page around it. Added 5 and 6 Sep 2026. |
| The founder's note of ten sites | 10 | Live sites, saved for how they move. Each has a `motion` block. |

Most collection and group problems below come from this split.

## 1. Collections

### 1.1 Size of each collection

| Collection | Entries | Members |
|---|---|---|
| flat-poster | 17 | algarve, cambodia, phillip-island, normandie, dribbble2, dribbble3, wanderwell2, canyonlands, chinagreatwall, fujiskyline, greece, luxembourg, rome, vietnam, wanderwell1, wanderwell3, wanderwell4 |
| illustrated-storybook | 14 | site-everswap, site-kellywallace, site-makemepulse, jon-juarez-home, mountain-landscape, mountains, local-waterfall, behance1, squirrel, dribbble4, bloomy-paris-builder, marble, vitra, linq |
| vast-quiet-cinematic | 12 | site-izanami, site-flyward, site-khufus, yosemite, root-soil-golden-fields, ctgt-hero, ctgt-alt, nexora, prompting-company, cogni, visora, crix-dreamscape-product |
| print-tech-paper | 6 | dribbble5, rooted-textile-landscape, stillpage, spade, sails-collage, roamfield |
| data-as-texture | 5 | climora, ascii-web-section, igloo, stillness-voxel, journey-ascii-login |
| dither-mono | 5 | monolith, castle, asterisk-login, dark-login-rock, sumi |
| mascot-illustration | 5 | manta-porcelain, dribbble1, decorative-manta, rating-or-bkg-art, galaxy-manta |
| monumental-editorial | 5 | site-visiblecuration, site-eaglesnest, atelo-interior-gallery, sakura-studio-art-gallery, ambientica-shaping-spaces |
| technical-systems | 5 | drone-mapping-os, drone-thermal-specimen, drone-see-to-sea, drone-thermion-heatmap, drone-from-above |
| classical-remix | 3 | juris, break-the-pattern, dualite |
| luminous-futurism | 3 | stardust-pixel-light, sakura-cosmic-tree, nebula-luminous-flower |
| painterly-portrait | 3 | painterly-fantasy, painterly-normal, painterly-purple |
| product-led-minimalism | 3 | site-dock, zuno-orange-workspace, synthos-ai-workspace |
| cinematic-still-life | 2 | site-growon, royal-gambit-chess |
| glitched-antiquity | 2 | nightlife-refined, yieldstream |
| ink-botanical | 2 | turtles1, zentangle-manta |

The top three collections hold 43 of 92 entries (47%). Seven collections hold 3 entries or fewer.

### 1.2 Entries that can belong to two collections

The second collection comes from words in the entry's own description, note or vocabulary.

| Entry | Now in | Also fits | Reason, from the entry |
|---|---|---|---|
| algarve | flat-poster | illustrated-storybook | "dry-brush gouache", "streaky strokes", "no outlines". It is painted, not flat shapes. |
| fujiskyline | flat-poster | print-tech-paper | "vintage screen-print", "distressed paper texture", "worn and scratched" paper. |
| normandie | flat-poster | (weak) none | Poster, but "no horizon line" and "airbrushed soft fades". The flat-poster vocabulary asks for a "crisp horizon line". |
| dribbble3 | flat-poster | vast-quiet-cinematic | Top-down river, one small boat, "negative space". No horizon, no bands. |
| wanderwell2 | flat-poster | (technique) page-melt | The note is about matching the picture's edges to the page colours, not about the poster look. |
| yosemite | vast-quiet-cinematic | illustrated-storybook | "painted", "broad, flat brush strokes". The collection's `imageStyle` asks for a photograph. |
| site-flyward | vast-quiet-cinematic | monumental-editorial (weak) | A travel page with a map-hole reveal and a terrace photo. It is not "one enormous atmospheric landscape". |
| cogni | vast-quiet-cinematic | luminous-futurism | "glowing bands of light", keyword `light-trails`, near-black ground. Its note says "swap the landscape for pure light". |
| crix-dreamscape-product | vast-quiet-cinematic | product-led-minimalism | Dashboard screenshots, pricing cards, feature cards. Its own note says it is "busier with product detail". |
| linq | illustrated-storybook | vast-quiet-cinematic | "hazy painted landscape", "misty lake", dimmed. |
| mountain-landscape | illustrated-storybook | vast-quiet-cinematic | Seven layers of haze, "atmospheric perspective", one colour family. |
| dribbble4 | illustrated-storybook | mascot-illustration | One character with two rabbits on a plain blush ground: "one character ... the background stays plain". |
| site-growon | cinematic-still-life | (no collection) immersive-3d style | A 3D desk scene you play with. The still-life look is incidental. |
| dribbble1 | mascot-illustration | flat-poster (weak) | A stag, not a mascot. Its group is page-background-art. |
| dribbble5 | print-tech-paper | mascot-illustration | A single winged creature seen from above, symmetrical, "filled edge to edge with pattern". Same shape idea as manta-porcelain. |
| zentangle-manta | ink-botanical | mascot-illustration | "The manta in other idioms". Its group is mascot-renderings. |
| manta-porcelain | mascot-illustration | ink-botanical | Blue ornament line fill, keyword `ink-line`, "density gradient edge to centre". Same idea as the ink-botanical `imageStyle`. |
| sumi | dither-mono | ink-botanical | "sumi-e ink wash", "brush and watered-down ink". It has no dither. Its note says "without any dotted texture". |
| dark-login-rock | dither-mono | (weak) vast-quiet-cinematic | Grainy photo, no dither, no `dither` keyword. |
| monolith | dither-mono | glitched-antiquity / classical-remix | "dithered Parthenon", a classical subject under machine texture. |
| journey-ascii-login | data-as-texture | dither-mono | "split-screen form + art", monochrome. This is the dither-mono layout. |
| igloo | data-as-texture | vast-quiet-cinematic | "one lit object" in "a world of one colour". Keyword `dither`, no ASCII. |
| stillness-voxel | data-as-texture | illustrated-storybook | Voxel landscape in pastel. It is a calm scene, not data. |
| spade | print-tech-paper | technical-systems | Topographic lines, mono data callouts, coordinates. |
| roamfield | print-tech-paper | flat-poster | A travel landscape poster in halftone. Its group includes destination-art. |
| sakura-studio-art-gallery | monumental-editorial | illustrated-storybook | Three storybook landscape panels. Its note says "the pictures feel like a storybook". |

26 of 92 entries (28%) have a plausible second collection. 8 of the 26 are strong (the entry's own words name the other look): algarve, fujiskyline, yosemite, cogni, crix-dreamscape-product, zentangle-manta, sumi, journey-ascii-login.

### 1.3 Collections that can split

**flat-poster (17).** The descriptions show three different things:

- Destination posters (8): canyonlands, chinagreatwall, fujiskyline, greece, luxembourg, rome, vietnam, cambodia. One landmark, bold shapes, often keyword `retro-poster`. Seven of the eight are in the destination-art group.
- Quiet art that melts into the page (6): algarve, phillip-island, normandie, dribbble2, dribbble3, wanderwell2. All are in page-background-art. Their notes talk about "lost edges", "fade into the page", "one warm colour family", "calm enough to sit behind a page".
- Web page heroes (3): wanderwell1, wanderwell3, wanderwell4. These are screenshots of a live page with menu and headline. All are in hero-art.

The collection name ("Flat Poster") fits only the first set well.

**illustrated-storybook (14).** It holds painted landscapes (jon-juarez-home, mountain-landscape, mountains, local-waterfall, behance1, squirrel), one character picture (dribbble4), four page screenshots (bloomy-paris-builder, marble, vitra, linq) and three motion sites (site-everswap, site-kellywallace, site-makemepulse). The common thread is "painted", not "storybook". The keyword `painterly` is on 9 of the 14.

**vast-quiet-cinematic (12).** Nine entries fit ("mist", "fog", "one huge picture"). Three do not: yosemite (a painting), cogni (light trails), crix-dreamscape-product (a full product page). site-flyward fits weakly.

### 1.4 Collections that can merge

**classical-remix (3) + glitched-antiquity (2).** All five put a classical artwork (painting, statue, engraving) inside a modern tech page. The descriptions differ only in the treatment: classical-remix is light and soft (sky blue, white); glitched-antiquity is dark and corrupted (glyph rain, datamosh). break-the-pattern already puts a technical overlay ("thin circles like a technical diagram") on the painting, which is near to the glyph overlay. monolith (dither-mono) is a third member of the same idea. A merged collection has 5 or 6 entries, with light and dark as two variants.

**ink-botanical (2) + sumi.** turtles1 is sumi-e brush, zentangle-manta is a pattern fill. sumi (now dither-mono) is "sumi-e ink wash". If zentangle-manta moves to mascot-illustration, ink-botanical keeps turtles1 and gains sumi: two sumi-e entries, one idea (few marks, much bare paper).

**cinematic-still-life (2).** royal-gambit-chess fits the definition. site-growon does not: the founder saved it because "the home-page picture [is] something to play with". Without growon the collection has 1 entry. Options: keep it as a one-entry collection, or merge royal-gambit-chess into a wider "dark photo" set (cinematic-still-life + luminous-futurism have the same dark ground and one lit subject).

**painterly-portrait (3).** All three notes say "a sample of a painting style" and "the portrait itself is incidental". The founder saved them for brushwork, not for faces. The collection name says "portrait", which is the part he calls incidental. They can merge into a painted-art collection with illustrated-storybook's painted landscapes, or stay as "painting-style samples".

**technical-systems (5).** All five are sections of one mock-up site (DRONE). The notes say "keep this with the DRONE ... references as one matching family". It is one source, not five independent references.

### 1.5 The ten site entries

The ten site entries sit in style collections by the look of their page: monumental-editorial 2, product-led-minimalism 1, vast-quiet-cinematic 3, illustrated-storybook 3, cinematic-still-life 1. But the founder saved 9 of them for their motion (group motion-references). site-kellywallace is the exception: its motion block says "the motion is not what he liked". Thus for 9 entries, the collection describes the part he did not save them for.

## 2. Style guide against collections

Key: **twin** = the style and the collection describe the same look (same ground, type and image idea). **Neighbour** = they share two or more `recognize` or `vocabulary` points but differ on one main point. **Unrelated** = no collection shares more than one point.

| # | Style | Nearest collection | Relation | Reason |
|---|---|---|---|---|
| 1 | Editorial Minimalism | product-led-minimalism | twin | Both: calm near-white ground, sans, one accent, the product screenshot as the picture. The two `imageStyle` lines ask for the same image. |
| 2 | Warm Editorial | print-tech-paper | neighbour | Both: warm paper ground, one clay or ember accent. Print-tech adds halftone and registration marks; Warm Editorial adds serif body text. |
| 3 | Terminal-Core | data-as-texture | neighbour | Both: monospace, amber on dark, ASCII. Terminal-Core is the UI voice; data-as-texture is the picture. |
| 4 | Swiss / International | monumental-editorial | neighbour | Both: huge flush-left grotesque, asymmetric layout. Swiss has no imagery; monumental-editorial has an inset photo. technical-systems also shares the grid and one hot accent. |
| 5 | Brutalist (Raw Web) | none | unrelated | No entry uses default browser styles. |
| 6 | Neo-Brutalism | none | unrelated | No entry has thick black outlines or hard offset shadows. |
| 7 | Neon Brutalist | glitched-antiquity | unrelated (weak) | Shares only "single hot accent on black". No type clash, no zine crop. |
| 8 | Data-Dense Pro | technical-systems | neighbour | Both: mono for data, charts or heat maps as the picture (drone-thermion-heatmap). Data-Dense is a dark dashboard; technical-systems is mostly white with huge type. |
| 9 | Cinematic Dark | cinematic-still-life and luminous-futurism | neighbour | Both: near-black ground, one lit subject, atmosphere. The Cinematic Dark `imageStyle` ("emerging from near-black darkness, single dramatic rim light") is close to cinematic-still-life's. |
| 10 | Glass / Soft-Futurism | product-led-minimalism (synthos) | unrelated (weak) | Only synthos has pastel light ribbons, and only nebula has the `glass` keyword. House DNA bans glassmorphism. |
| 11 | Playful Color / Illustrated | mascot-illustration | neighbour | Both: a mascot as a main part. Playful Color is saturated, flat and bouncy; mascot-illustration renders one figure in a material idiom. illustrated-storybook shares "illustration first". |
| 12 | Y2K / Retro-Futurism | none | unrelated | No chrome, no scan lines. |
| 13 | Japanese Minimalism (Ma) | ink-botanical | neighbour | Both: ink on pale paper, most of the picture empty (turtles1 is nine-tenths bare paper). sumi (dither-mono) is the same. vast-quiet-cinematic shares "silence as scale". |
| 14 | Quiet Luxury | cinematic-still-life | neighbour | Both: still-life product photography, restraint. Quiet Luxury is ivory and light; cinematic-still-life is dark. |
| 15 | Tactile / Skeuomorph | none | unrelated | No entry uses knobs, dials or machined materials. |
| 16 | Immersive 3D / WebGL Scroll | none (see note) | unrelated to any collection | But four entries are this style: site-everswap (built by Lusion, which is a canonical site of this style), site-growon, site-makemepulse, igloo. They sit in three different collections. |
| 17 | Bento Grid | none | unrelated | No entry is a bento layout. House DNA bans uniform card grids. crix-dreamscape-product has card sections but no bento. |
| 18 | Magazine / Print DNA | monumental-editorial | neighbour | Both: print authority, editorial type. print-tech-paper shares the print texture. |

Totals: 1 twin, 9 neighbours (counting style 9 once), 8 unrelated.

### 2.1 Collections that no style covers

Seven of the 16 collections have no twin or neighbour in the Style guide:

| Collection | Entries | Nearest style, and why it does not cover it |
|---|---|---|
| flat-poster | 17 | Playful Color shares flat fills, but asks for high saturation and mascots. No style is a travel poster. |
| illustrated-storybook | 14 | Playful Color shares "illustration first", but not painted, graded palettes. |
| vast-quiet-cinematic | 12 | Japanese Minimalism shares empty space, and Cinematic Dark shares atmosphere, but no style is a vast landscape photo with small type. |
| dither-mono | 5 | Neon Brutalist mentions halftone grain, but not 1-bit dither or split form-plus-art. |
| classical-remix | 3 | none |
| glitched-antiquity | 2 | none |
| painterly-portrait | 3 | none |

These seven hold 56 of 92 entries (61%). The Style guide describes standard web looks: type, UI and layout. The library's weight is in pictures. The two lists are mostly different axes, not two versions of one list.

## 3. Keywords

### 3.1 How many entries carry each keyword

32 keywords are allowed. All 32 are in use. No entry uses a keyword outside the list. Each entry has 2 to 7 keywords (1 entry has 2, 28 have 3, 37 have 4, 20 have 5, 5 have 6, 1 has 7).

"Spread" is the number of the 16 collections that have one or more entries with the keyword.

| Keyword | Entries | % of 92 | Spread | Family now |
|---|---|---|---|---|
| minimal | 47 | 51% | 15 | Medium |
| grain | 38 | 41% | 12 | Medium |
| photographic | 31 | 34% | 11 | Medium |
| gradient | 25 | 27% | 10 | Medium |
| saturated | 22 | 24% | 11 | Colour |
| flat-vector | 18 | 20% | 5 (14 in flat-poster) | Medium |
| painterly | 18 | 20% | 7 (9 in illustrated-storybook) | Medium |
| dense | 15 | 16% | 7 | Medium |
| geometric | 15 | 16% | 5 | Medium |
| night | 15 | 16% | 9 | Scene |
| organic-curve | 15 | 16% | 6 | Medium |
| monochrome | 14 | 15% | 7 | Colour |
| pastel | 11 | 12% | 5 | Colour |
| seascape | 11 | 12% | 6 | Scene |
| dawn | 10 | 11% | 6 | Scene |
| 3d | 7 | 8% | 4 | Medium |
| ink-line | 7 | 8% | 5 | Medium |
| retro-poster | 7 | 8% | 2 (6 in flat-poster) | Medium |
| tropical | 7 | 8% | 2 | Scene |
| halftone | 6 | 7% | 2 | Medium |
| ascii | 5 | 5% | 2 | Medium |
| dither | 5 | 5% | 3 | Medium |
| engraved | 4 | 4% | 4 | Medium |
| hand-lettered | 4 | 4% | 3 | Medium |
| light-trails | 4 | 4% | 2 | Medium |
| scroll-driven | 3 | 3% | 2 | Motion |
| page-transition | 2 | 2% | 2 | Motion |
| ambient-loop | 1 | 1% | 1 | Motion |
| glass | 1 | 1% | 1 | Medium |
| glitch | 1 | 1% | 1 | Medium |
| hover | 1 | 1% | 1 | Motion |
| parallax | 1 | 1% | 1 | Motion |

### 3.2 Keywords that barely separate the entries

- **minimal (47, 15 of 16 collections).** Only glitched-antiquity has no `minimal` entry. The word has two meanings in the data. On the seed page screenshots it means "much empty space on the page" (ctgt-hero, visora, ambientica). On the founder's art it means "few shapes" (dribbble2, luxembourg, turtles1). Two entries carry both `minimal` and `dense`: manta-porcelain and drone-thermion-heatmap.
- **grain (38, 12 collections).** It is on posters, photos, ASCII, dither and paintings. It does not separate a look.
- **gradient (25, 10 collections).** It means a sky fade (cambodia, dribbble3), a soft painted blend (painterly-*), a light ribbon (synthos) and a fog fade (ctgt-alt). Four different things.
- **saturated (22, 11 collections)** and **photographic (31, 11 collections)** separate more. `photographic` splits photo from drawn art. But 10 of the 31 are in one collection (vast-quiet-cinematic).
- **night (15)** is mostly "dark ground", not a night scene. Only 6 of 15 show night or dusk (site-growon, galaxy-manta, drone-mapping-os, sakura-cosmic-tree, climora, nightlife-refined). The other 9 are not night scenes: 8 are dark pages or dark studio shots (site-izanami, site-eaglesnest, royal-gambit-chess, stardust-pixel-light, nebula-luminous-flower, dark-login-rock, yieldstream, cogni), and 1 is a white page (sumi, where the "night" is star speckle in the ink).
- **dawn (10)** means "low warm light, dawn or dusk" (nexora sunset, linq dusk, root-soil dusk). break-the-pattern has no dawn in its description. climora carries both `night` and `dawn`.

### 3.3 Keywords that separate well

These keywords pick a small set that shares one clear look: `halftone` (6), `ascii` (5), `dither` (5), `light-trails` (4), `retro-poster` (7), `flat-vector` (18), `3d` (7), `tropical` (7), `seascape` (11), `ink-line` (7), `engraved` (4).

But many of these repeat a collection. `flat-vector` is 14 of 18 in flat-poster. `halftone` is 4 of 6 in print-tech-paper. `ascii` is 3 of 5 in data-as-texture. `dither` is 3 of 5 in dither-mono. `light-trails` is 3 of 4 in luminous-futurism. `retro-poster` is 6 of 7 in flat-poster. Where a keyword repeats a collection, it adds little. Where it crosses collections, it adds much: `ascii` joins data-as-texture and glitched-antiquity; `dither` joins dither-mono, data-as-texture (igloo) and glitched-antiquity (yieldstream); `halftone` joins print-tech-paper and dither-mono.

### 3.4 Keywords in the wrong family

The `keyword_families` has four families: Medium (20), Colour (3), Scene (4), Motion (5). Against that list:

| Keyword | Family now | What it really is | Reason |
|---|---|---|---|
| minimal | Medium | amount of detail (density) | It is not a way of making a picture. Its opposite `dense` is also in Medium. |
| dense | Medium | amount of detail (density) | Same as above. |
| geometric | Medium | shape language | It describes the shapes, not the medium. |
| organic-curve | Medium | shape language | Same as above. |
| gradient | Medium | colour treatment | A fade between colours. Used for sky fades and fog fades. |
| grain | Medium | surface finish (texture) | It is added on top of any medium: photo, vector, paint. |
| retro-poster | Medium | genre or era | A poster tradition, not a medium. |
| light-trails | Medium | subject or effect | Streaks of light are the subject of the picture. |
| glass | Medium | material look | One entry only. House DNA bans glassmorphism. |
| night | Scene | mostly colour (dark ground) | See 3.2: 9 of 15 are not night scenes; 8 of them are dark pages. |
| dawn | Scene | light (time of day) | Correct family if "Scene" includes light. It means dawn or dusk. |

The true media are: flat-vector, ink-line, engraved, photographic, hand-lettered, 3d, halftone, dither, ascii, glitch, painterly.

A possible re-cut of the families, as evidence only: **Medium** (the 11 above), **Finish** (grain, gradient), **Shape** (geometric, organic-curve), **Density** (minimal, dense), **Colour** (pastel, saturated, monochrome, and a "dark" to replace most `night` uses), **Scene** (seascape, tropical, night, dawn), **Genre** (retro-poster), **Motion** (see 3.5).

### 3.5 The Motion keywords

The 5 Motion keywords are on the 10 site entries only: 8 tags on 7 sites. Three sites have no motion keyword: site-growon, site-kellywallace, site-makemepulse. Three tags disagree with the entry's own `motion` block:

| Entry | Keyword now | What the `motion` block says |
|---|---|---|
| site-visiblecuration | scroll-driven, parallax | The block says "no parallax": the heading and circles "move 1:1". The motion is a scroll zoom and a held title. `parallax` is wrong. |
| site-khufus | page-transition | The motion is a looping film of drifting dust ("autoplays muted and loops"), plus a scroll-linked colour change. That is an ambient loop, not a page transition. |
| site-everswap | page-transition | The motion is a camera flight driven by the wheel (a virtual scroll). That is scroll-driven. It does have scene hand-overs inside it. |


### 3.6 How a keyword is reached on the page

The page has no keyword filter. `app.js` line 39: the page filters by collection or Manta group (the side menu), by fit verdict (the Fit select), and by the search box. The keyword tags in the detail panel are plain `<span>` elements (`tags()`, line 37). They are not links. Thus the search box is the only way to reach every one of the 32 keywords.

The search box does a plain substring match over title, description, note, keywords, vocabulary, collection name and the Manta take. It does not search `composition`, `image_recipe` or `motion`. So a keyword search also finds entries whose prose contains the word:

| Search | Tagged | Found by search |
|---|---|---|
| glass | 1 | 5 |
| night | 15 | 19 (for example "nightlife") |
| hover | 1 | 3 |
| dither | 5 | 7 |
| gradient | 25 | 28 |
| grain | 38 | 40 |
| pastel | 11 | 13 |
| engraved, glitch, monochrome, dawn, saturated | 4, 1, 14, 10, 22 | 5, 2, 15, 11, 23 |

The other 20 keywords give the same count by search and by tag.

## 4. Manta surface groups

### 4.1 Group sizes

| Group | Entries | Axis |
|---|---|---|
| hero-art | 41 | page part (with an art condition) |
| page-background-art | 20 | kind of artwork (with a page-layer condition) |
| destination-art | 17 | kind of artwork |
| ui-chrome-and-cards | 9 | page part |
| motion-references | 9 | behaviour (motion) |
| mascot-renderings | 5 | kind of artwork |
| footer-scene | 4 | page part (with an art condition) |

13 entries are in two groups.

### 4.2 Page parts and kinds of artwork

The seven groups mix three axes:

- **Page parts:** hero-art (the hero), footer-scene (the footer), ui-chrome-and-cards (cards, chips, menu, controls). Each tells where on a page the reference applies.
- **Kinds of artwork:** destination-art (poster scenes of a place), mascot-renderings (the manta in other idioms), page-background-art (ambient art behind the working area). Each tells what the picture is. page-background-art also names a page layer, but its members are chosen as art: 16 of its 20 are pictures with no page.
- **Behaviour:** motion-references. It tells how a thing moves, not where or what.

Two page-part groups carry an art condition in their name. "Hero art" means "how the homepage hero scene composes". "Footer scene" means "a sparse sea scene on the night ground". Their members do not always meet the condition:

- footer-scene has 4 members. Only monolith shows a footer (a giant cropped wordmark). turtles1 is a picture with no page. sumi is a white page with an ink painting under a headline. climora is a hero. site-eaglesnest, the one entry that the founder saved for a footer, is in motion-references only.
- Two placements in destination-art do not match the group's header ("poster scenes of a place"): asterisk-login (a login page with a photo of a person on a slope) and spade (a topographic drawing of a coffee-cup lid on a finance page).

### 4.3 hero-art: what the 41 entries share

- All 41 show one picture at the top of a page, or a picture that could go there. The group header says a hero-art reference "answers how a hero scene composes, never what colour it is".
- 32 of 41 are Chase's seed screenshots (`cth9191/taste-vault`). 9 are the founder's own saves.
- No site entry is in hero-art. The three motion sites whose motion lives in the hero (site-visiblecuration, site-dock, site-khufus) are in motion-references only.
- Verdicts: 22 adapt, 17 off-brand, 2 on-brand (wanderwell3, wanderwell4). 17 of the library's 21 off-brand verdicts are in hero-art.

### 4.4 hero-art: where the 41 entries differ

The composition of each entry (from its `composition` and description) puts it in one of six kinds:

| Hero kind | Count | Entries |
|---|---|---|
| Full-bleed picture, type on its calm zone | 22 | wanderwell1, wanderwell3, wanderwell4, royal-gambit-chess, stardust-pixel-light, bloomy-paris-builder, nebula-luminous-flower, root-soil-golden-fields, drone-from-above, stillpage, ctgt-hero, ctgt-alt, nexora, prompting-company, climora, igloo, break-the-pattern, marble, linq, cogni, visora, roamfield |
| Split: picture on one half, text or form on the other | 6 | juris, dualite, nightlife-refined, yieldstream, castle, drone-thermion-heatmap |
| Giant type with an inset picture or a strip of pictures | 5 | atelo-interior-gallery, ambientica-shaping-spaces, sakura-studio-art-gallery, sakura-cosmic-tree, drone-mapping-os |
| Product screenshot as the picture | 1 | zuno-orange-workspace |
| A full long page, not only the hero | 1 | crix-dreamscape-product |
| Artwork with no page around it | 6 | squirrel, dribbble4, dribbble5, painterly-fantasy, painterly-normal, painterly-purple |

Other differences:

- **What the reference teaches.** For the 32 seed screenshots, the lesson is layout and type (where the headline sits, a two-tone headline in ctgt-alt, a wordmark as a window in marble). For the 6 pieces of pure artwork, the lesson is a painting style ("a sample of a painting style", painterly-normal).
- **Look.** The 41 cover 14 of the 16 collections. Only ink-botanical and mascot-illustration have no hero-art entry.
- **Page kind.** Most are software landing pages (AI tools, SaaS, drones). Three are travel pages (wanderwell1, wanderwell3, wanderwell4) and one is travel booking (roamfield).

### 4.5 Consequence for a page-part axis

A page-part axis that keeps "hero" as one value does not split it. The hero kinds in 4.4 are a possible second level under "hero".

## 5. Draft page-part tag per entry

### 5.1 Vocabulary

Six values, from the brief. They start from the design-project skill's website list (`plugin/skills/design-project/SKILL.md` line 56: hero, page-layout, type-and-colour, imagery, navigation-and-footer, motion). The brief drops type-and-colour and adds "cards and controls".

| Value | Meaning |
|---|---|
| hero | The opening screen: picture, headline, menu and main button together. |
| page layout | How sections sit and join down a page, or how a page splits. |
| navigation and footer | The menu bar or the footer. |
| cards and controls | Cards, chips, buttons, forms, inputs. |
| art | Imagery or art only: a picture with no page around it. |
| motion | How a thing moves. |

Method: I read each entry's description, note and composition. The first tag (bold) is the part the note is about. Other tags are parts that the shot also shows clearly. An entry is "pure artwork" when its only tag is `art`.


### 5.2 The table

| Entry | Collection | Manta groups now | Draft page-part tag | Reason |
|---|---|---|---|---|
| manta-porcelain | mascot-illustration | mascot-renderings | **art** | A creature decorated in porcelain pattern; no page. |
| site-visiblecuration | monumental-editorial | motion-references | **motion** + hero | Scroll zoom of the hero picture; the title holds. |
| site-dock | product-led-minimalism | motion-references | **motion** + hero | Ambient loop inside the hero landscape. |
| site-izanami | vast-quiet-cinematic | motion-references | **motion** + page layout | Scene fades into the next section as you scroll. |
| site-flyward | vast-quiet-cinematic | motion-references | **motion** + page layout, hero | Hero reveal, coastline section edges, a trail between sections. |
| site-everswap | illustrated-storybook | motion-references | **motion** + page layout | The whole page is one camera flight. |
| site-khufus | vast-quiet-cinematic | motion-references | **motion** + hero | Hazy film loop in the hero; its base melts into the next section. |
| site-eaglesnest | monumental-editorial | motion-references | **motion** + navigation and footer | Footer link hover. |
| site-growon | cinematic-still-life | motion-references | **motion** + hero | Home-page scene you can point at and click. |
| site-kellywallace | illustrated-storybook | page-background-art | **art** + page layout | Unframed drawings set through the page; the motion is not the point. |
| site-makemepulse | illustrated-storybook | motion-references | **motion** + page layout | Scene-to-scene passage through the whole piece. |
| algarve | flat-poster | page-background-art | **art** | Painted cove; no page. |
| cambodia | flat-poster | page-background-art | **art** | Poster scene; no page. |
| dribbble1 | mascot-illustration | page-background-art | **art** | Stag illustration; no page. |
| jon-juarez-home | illustrated-storybook | page-background-art | **art** | Illustration; no page. |
| yosemite | vast-quiet-cinematic | page-background-art | **art** | Painting; no page. |
| phillip-island | flat-poster | page-background-art | **art** | Painting; no page. |
| mountain-landscape | illustrated-storybook | page-background-art | **art** | Painting; no page. |
| normandie | flat-poster | page-background-art | **art** | Poster; no page. |
| dribbble2 | flat-poster | page-background-art | **art** | Illustration; no page. |
| dribbble3 | flat-poster | page-background-art | **art** | Illustration; no page. |
| mountains | illustrated-storybook | page-background-art | **art** | Painting; no page. |
| wanderwell2 | flat-poster | page-background-art | **page layout** + art | A band between two sections, its edges matched to their colours. |
| canyonlands | flat-poster | destination-art | **art** | Poster; no page. |
| chinagreatwall | flat-poster | destination-art | **art** | Poster; no page. |
| fujiskyline | flat-poster | destination-art | **art** | Print; no page. |
| greece | flat-poster | destination-art | **art** | Poster; no page. |
| luxembourg | flat-poster | destination-art | **art** | Poster; no page. |
| rome | flat-poster | destination-art | **art** | Poster; no page. |
| vietnam | flat-poster | destination-art | **art** | Poster; no page. |
| local-waterfall | illustrated-storybook | destination-art | **art** | Painting; no page. |
| behance1 | illustrated-storybook | destination-art, page-background-art | **art** | Illustration; no page. |
| turtles1 | ink-botanical | footer-scene | **art** | Ink drawing; no page. |
| decorative-manta | mascot-illustration | mascot-renderings | **art** | Mascot rendering; no page. |
| rating-or-bkg-art | mascot-illustration | mascot-renderings | **art** | Mascot rendering; no page. |
| galaxy-manta | mascot-illustration | mascot-renderings | **art** | Mascot rendering; no page. |
| zentangle-manta | ink-botanical | mascot-renderings | **art** | Mascot rendering; no page. |
| wanderwell1 | flat-poster | hero-art | **hero** + page layout | Hero picture whose lowest colour runs on under the title. |
| wanderwell3 | flat-poster | hero-art | **hero** + page layout | Hero whose snow becomes the white page. |
| wanderwell4 | flat-poster | hero-art | **hero** | Headline on empty sky, button on empty sea. |
| squirrel | illustrated-storybook | hero-art | **art** | Painting; no page. |
| dribbble4 | illustrated-storybook | hero-art | **art** | Character illustration; no page. |
| dribbble5 | print-tech-paper | hero-art | **art** | Risograph moth; no page. |
| painterly-fantasy | painterly-portrait | hero-art, page-background-art | **art** | Painting-style sample; no page. |
| painterly-normal | painterly-portrait | hero-art, page-background-art | **art** | Painting-style sample; no page. |
| painterly-purple | painterly-portrait | hero-art, page-background-art | **art** | Painting-style sample; no page. |
| atelo-interior-gallery | monumental-editorial | hero-art | **hero** | Image strip over a giant offset headline. |
| zuno-orange-workspace | product-led-minimalism | ui-chrome-and-cards, hero-art | **hero** + cards and controls | Product screenshot hero; dashboard cards and paired buttons. |
| royal-gambit-chess | cinematic-still-life | hero-art | **hero** | Full-bleed photo, text on the dark half. |
| sakura-studio-art-gallery | monumental-editorial | destination-art, hero-art | **hero** + page layout | Art strip, statistics rail and a large white gap. |
| synthos-ai-workspace | product-led-minimalism | ui-chrome-and-cards | **page layout** + cards and controls | A lower band that explains the product in three panels. |
| ambientica-shaping-spaces | monumental-editorial | hero-art | **hero** | Giant headline with one inset photo. |
| stardust-pixel-light | luminous-futurism | hero-art | **hero** + cards and controls | Full-bleed art; one floating case-study card. |
| drone-mapping-os | technical-systems | hero-art | **hero** | Giant name over an annotated picture. |
| drone-thermal-specimen | technical-systems | ui-chrome-and-cards | **page layout** | Picture framed by specification columns. |
| rooted-textile-landscape | print-tech-paper | destination-art | **hero** + cards and controls | Split headline row, logo row, textured photo; the button repeats the clipped corner. |
| sakura-cosmic-tree | luminous-futurism | hero-art | **hero** | Inset picture under the menu, headline below. |
| bloomy-paris-builder | illustrated-storybook | hero-art | **hero** + cards and controls | Illustrated city with a real input box in the sky. |
| nebula-luminous-flower | luminous-futurism | hero-art | **hero** | Full-bleed art, text on the dark side. |
| root-soil-golden-fields | vast-quiet-cinematic | hero-art, destination-art | **hero** | Sky becomes the page background. |
| drone-see-to-sea | technical-systems | ui-chrome-and-cards | **hero** + page layout | Giant headline over a labelled photo; numbered sections below. |
| drone-thermion-heatmap | technical-systems | hero-art | **hero** + page layout | Split: text column and heat map. |
| drone-from-above | technical-systems | hero-art | **hero** | Full-bleed photo with grid and headline. |
| stillpage | print-tech-paper | page-background-art, hero-art | **hero** | Paper ground, halftone tree, headline. |
| spade | print-tech-paper | destination-art | **hero** + cards and controls | Headline panel with data-callout chips. |
| sails-collage | print-tech-paper | page-background-art | **art** + page layout | A collage used as the page ground; no page UI in the shot. |
| monolith | dither-mono | footer-scene | **hero** + navigation and footer | Split hero, then a footer with a cropped giant wordmark. |
| castle | dither-mono | hero-art | **hero** + cards and controls | Split waitlist: form and dithered picture. |
| asterisk-login | dither-mono | ui-chrome-and-cards, destination-art | **cards and controls** + page layout | Login card beside a photo. |
| dark-login-rock | dither-mono | ui-chrome-and-cards | **cards and controls** + page layout | Login form beside a photo. |
| ctgt-hero | vast-quiet-cinematic | hero-art | **hero** | Full-bleed photo, tiny centred type. |
| ctgt-alt | vast-quiet-cinematic | hero-art | **hero** | Fog zone holds a two-tone headline. |
| nexora | vast-quiet-cinematic | hero-art | **hero** | Full-bleed photo, headline on the sky. |
| prompting-company | vast-quiet-cinematic | hero-art | **hero** | Full-bleed photo, serif headline. |
| climora | data-as-texture | hero-art, footer-scene | **hero** | Full-bleed data-cloud picture. |
| ascii-web-section | data-as-texture | ui-chrome-and-cards | **cards and controls** + page layout | A card grid with tabs, toggles and Expand buttons. |
| igloo | data-as-texture | hero-art | **hero** | Full-screen 3D scene. |
| juris | classical-remix | hero-art | **hero** + cards and controls | Split painting and chat input. |
| break-the-pattern | classical-remix | hero-art | **hero** | Full-bleed painting, centred headline. |
| marble | illustrated-storybook | hero-art | **hero** + cards and controls | Wordmark masks the sky; form on the water. |
| vitra | illustrated-storybook | destination-art, ui-chrome-and-cards | **hero** + page layout | Split waitlist with illustration panel. |
| linq | illustrated-storybook | hero-art | **hero** | Dimmed painting behind a phone UI. |
| nightlife-refined | glitched-antiquity | hero-art | **hero** | Split: statue and headline. |
| yieldstream | glitched-antiquity | hero-art | **hero** | Split: engraving and headline. |
| cogni | vast-quiet-cinematic | hero-art | **hero** | Light trails, centred headline. |
| visora | vast-quiet-cinematic | hero-art | **hero** | Empty sky over a dune strip. |
| stillness-voxel | data-as-texture | destination-art, page-background-art | **hero** | Headline above a voxel diorama. |
| roamfield | print-tech-paper | hero-art, destination-art | **hero** + navigation and footer | Full-bleed halftone scene; floating pill menu. |
| dualite | classical-remix | hero-art | **hero** | Split: painting and headline. |
| journey-ascii-login | data-as-texture | ui-chrome-and-cards | **cards and controls** + page layout | Login form beside ASCII art. |
| crix-dreamscape-product | vast-quiet-cinematic | hero-art | **page layout** + cards and controls, navigation and footer | A full long page: sections, pricing cards, footer wordmark. |
| sumi | dither-mono | footer-scene | **hero** | Headline over an ink-wash painting. |

### 5.3 Counts

| Tag | As first tag | On the entry at all |
|---|---|---|
| hero | 41 | 46 |
| art | 34 | 35 |
| motion | 9 | 9 |
| page layout | 4 | 20 |
| cards and controls | 4 | 14 |
| navigation and footer | 0 | 4 |

**Pure artwork that fits no page part: 32 entries (35%).** They are: manta-porcelain, algarve, cambodia, dribbble1, jon-juarez-home, yosemite, phillip-island, mountain-landscape, normandie, dribbble2, dribbble3, mountains, canyonlands, chinagreatwall, fujiskyline, greece, luxembourg, rome, vietnam, local-waterfall, behance1, turtles1, decorative-manta, rating-or-bkg-art, galaxy-manta, zentangle-manta, squirrel, dribbble4, dribbble5, painterly-fantasy, painterly-normal, painterly-purple.

All 32 are the founder's own saves. Two more entries have `art` as the first tag but also show a page: site-kellywallace and sails-collage.

### 5.4 What the table shows

- **The page-part axis splits the library by source.** 45 of the 46 seed screenshots have a page part as first tag (mostly hero); the exception is sails-collage, a collage with no page UI. 32 of the founder's 36 non-site saves are pure art.
- **`navigation and footer` is thin.** Only 4 entries show it clearly: site-eaglesnest, monolith, roamfield, crix-dreamscape-product. No entry is first about a menu bar.
- **`hero` is 41 as first tag, but not the same 41 as the hero-art group.** Seven hero-art members are not tagged hero: crix-dreamscape-product (a full page) and six pieces of pure art (squirrel, dribbble4, dribbble5, painterly-fantasy, painterly-normal, painterly-purple). Twelve entries are tagged hero but are not in hero-art: five motion sites whose motion is in the hero (site-visiblecuration, site-dock, site-flyward, site-growon, site-khufus) and seven page screenshots (drone-see-to-sea, monolith, rooted-textile-landscape, spade, stillness-voxel, sumi, vitra).
- **`cards and controls` against ui-chrome-and-cards.** Three group members are not tagged cards and controls: drone-see-to-sea and drone-thermal-specimen (their lesson is the big headline or the spec columns) and vitra (a split hero). Eight entries show a clear control but are not in the group: bloomy-paris-builder, castle, crix-dreamscape-product, juris, marble, rooted-textile-landscape, spade, stardust-pixel-light. Most of these are an input or a form inside a hero.
- **type-and-colour.** The skill's list has it; the brief's list does not. Several seed entries are first about type: ctgt-alt (two-tone headline), atelo-interior-gallery and ambientica-shaping-spaces (giant offset headline), marble (wordmark as a window). With no type value, they fall under `hero`.

## 6. Draft motion-kind tag for the 10 site entries

### 6.1 Vocabulary

Each `motion` block has a `trigger` field. The trigger is the clearest split between the ten, so the draft motion kind follows it:

| Motion kind | Meaning |
|---|---|
| scroll-scrubbed | The change follows the scroll position. It stops when you stop. |
| ambient loop | It plays on its own. Nobody triggers it. |
| pointer response | It answers the pointer: hover, point, click. |
| scene transition | A triggered, timed change from one scene to the next. |
| entrance on view | It plays once, when a part loads or scrolls into view. |
| still | The part he liked does not move. |

### 6.2 The table

| Entry | Draft motion kind (main + other) | Evidence in the `motion` block | Keyword now | Purpose (block) |
|---|---|---|---|---|
| site-visiblecuration | **scroll-scrubbed** + entrance on view | "scroll (scrubbed ...)"; video scale 1 → 1.5 "linear in scroll"; title held by `position: fixed`; CTA band "once-only in-view entrance" | scroll-driven, parallax | delight |
| site-dock | **ambient loop** + pointer response | "autoplay loop ... nothing is scrolled or hovered"; 6.03 s video; moss spreads on hover (description) | ambient-loop | delight |
| site-izanami | **scroll-scrubbed** (a scene crossfade) | "scroll (scrubbed; Lenis ...)"; forest alpha 1 → 0 "across exactly one viewport of scroll" | scroll-driven | preventing-jarring-change |
| site-flyward | **scroll-scrubbed** (mask reveal, path draw, drifting edges) | "scroll — native page scroll"; hole 100vw → 750vw; `stroke-dashoffset` 5,246 → 0 "scrub: true"; edge layers translateY as each section passes | scroll-driven | spatial-consistency |
| site-everswap | **scroll-scrubbed** (camera flight) + pointer response | "mouse wheel, touch drag or keyboard ... driving a virtual scroll"; camera "read frame by frame ... at the scroll ratio"; "pointer-look eases at 0.1 per frame" | page-transition | spatial-consistency |
| site-khufus | **ambient loop** + scroll-scrubbed + entrance on view | "none for the film — it autoplays muted and loops"; closing section "maps scroll progress to its background colour"; headline lines rise in | page-transition | delight |
| site-eaglesnest | **pointer response** | "pointer enter and leave on a footer menu item — pure CSS :hover"; 500 ms expo-out | hover | feedback |
| site-growon | **pointer response** + entrance on view | "the pointer — its position turns the scene, hovering an object lifts it, clicking an object sets off that object's reaction"; drop-in on load | (none) | delight |
| site-kellywallace | **still** (the art) | "none on the artwork — the drawings are still images"; `purpose_note`: "the motion is not what he liked" | (none) | delight |
| site-makemepulse | **scene transition** + pointer response | "one gesture (drag, click, or a 2.5 s hold) unlocks a Next button, and Next starts the move to the next scene"; 1.75 s per scene change; "the pointer's position pans the view" | (none) | delight |

### 6.3 Counts and findings

- Main kind: scroll-scrubbed 4, ambient loop 2, pointer response 2, scene transition 1, still 1.
- As any kind: pointer response 5, scroll-scrubbed 5, entrance on view 3, ambient loop 2, scene transition 1, still 1.
- site-flyward does have a parallax-like drift (edge layers move at a different speed), but it has no `parallax` keyword.
- "Entrance on view" is in 4 blocks: the 3 tagged above and site-kellywallace (on its text only). It is never the part he saved.
- The `purpose` field is a second possible axis: delight 6, spatial-consistency 2, preventing-jarring-change 1, feedback 1. The `band` field is marketing on 9 and ui on 1 (site-eaglesnest).
- Reduced-motion handling, from each `reduced` field: site-dock pauses the video; site-growon skips most motion but plays sound; site-kellywallace skips its entrances; site-khufus lands only the headline and the film plays on. The other six have no handling.
- "Scene transition" and "scroll-scrubbed" overlap in meaning. site-izanami and site-everswap move from scene to scene, but the scroll drives them. site-makemepulse is the only one where a click starts a timed change. If one kind must hold both, name it by trigger (as here), not by effect.

## 7. Findings for the decisions under #17


1. **The library has two populations.** 46 seed page screenshots and 46 founder saves (36 pictures, 10 sites). Collections, Manta groups and page parts all split along this line (Sources, 4.3, 5.4).
2. **Collections mix look and subject.** flat-poster holds three different things (destination posters, quiet page-melt art, web heroes). illustrated-storybook means "painted". painterly-portrait names the part the founder calls incidental (1.3, 1.4).
3. **Five small collections are merge candidates:** classical-remix + glitched-antiquity (+ monolith); ink-botanical + sumi; cinematic-still-life without site-growon has 1 entry; painterly-portrait is a set of painting-style samples; technical-systems is one mock-up site (1.4).
4. **26 entries (28%) have a plausible second collection; 8 strongly** (1.2).
5. **The Style guide and the collections are mostly different axes.** 1 twin, 9 neighbours, 8 unrelated. 7 collections, with 61% of the entries, have no style. The Immersive 3D style matches four entries in three collections (2, 2.1).
6. **Half the keywords do little work.** `minimal` (47), `grain` (38) and `gradient` (25) each cross 10 or more collections. `night` means "dark ground" on 9 of 15. Nine Medium keywords are not media (3.2, 3.4).
7. **The motion keywords are wrong on 3 of 7 tagged sites and absent on 3 sites** (3.5, 6.3).
8. **Search is the only way to reach a keyword,** and it matches prose too, so a keyword search is not a tag filter (3.6).
9. **The Manta groups mix page parts, kinds of art and one behaviour.** footer-scene holds only one footer. hero-art is 45% of the library and holds six different hero kinds plus six pure paintings (4.2, 4.4).
10. **A page-part axis gives 32 pure-art entries (35%) no value except "art".** navigation and footer is thin (4 entries). Type has no value in the brief's list (5.3, 5.4).
11. **A motion-kind axis by trigger fits the ten blocks:** scroll-scrubbed 4, ambient loop 2, pointer response 2, scene transition 1, still 1 (6.3).

## Open questions (for the founder, one plain question each; owner: #23, the ways-in decision)

- The six painterly and character pictures in hero-art (squirrel, dribbble4, dribbble5, painterly-fantasy, painterly-normal, painterly-purple): did you save these for a painting style, or for a hero?
- site-kellywallace: is the lesson the drawings, or how they sit on the page without frames?
- asterisk-login and spade in destination-art: are these kept for a place scene, or for something else on the page?

Bound: I read exhaustively all 92 entries in `data/gallery.json` (title, description, note, keywords, vocabulary, composition, fit groups and verdict, source, added date, and all 10 `motion` blocks in full; I read the `fit.manta.take` text in full for the first 12 entries and used only groups and verdict for the other 80), all 16 collections, `keywords_allowed`, `keyword_families`, `projects.manta.groups`, all 18 styles in `data/styles.json`, the filter and search code in `app.js` (lines 37 and 39) and `index.html` line 31, and line 56 of the design-project skill. I did not read `image_recipe` on any entry. I opened 4 of the images (`monolith.png`, `crix-dreamscape-product.png`, `ascii-web-section.png`, `sails-collage.png`) and did not open the other 88 images or any of the 10 `.webm` captures; the page-part tags for those 88 come from the text only. I did not read the mantahostels issues that the notes cite.

## Concision marks

1. The #29 banner at the head: its sentences on the six paintings, site-kellywallace and asterisk-login/spade restate #29's resolution, which holds them. Read the banner's first sentence and its last two; skip the middle.
