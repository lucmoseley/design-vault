# Research #204: the term for a design's intended feel, the sets of feels, and the choices tied to each

Ticket: lucmoseley/design-vault#204 (child of map #202, founder note N15).

Source strength labels:
- **[P]** Primary source: a peer-reviewed study, a standard, or the first-party document.
- **[P-weak]** Primary source with a small sample, one culture, or one study only.
- **[S]** Secondary source or practitioner convention (books, design-system docs, industry writing).
- **[H]** The house's own files or issues.

Time labels:
- **timeless**: the link comes from perception and holds across eras.
- **era-bound**: the link is a fashion or a convention of one period or culture.

## Part H. What the house holds now (found first)

### H1. Issues on this repo

- No closed issue rules on a term or a set of feels. #204 is the first ticket on the subject. **[H]**
- #24 recorded seed-collection lines such as "Crafted-document energy" and "frontier-company gravitas" as faults against the two-registers rule (design-vault#2 Q6), because the founder could not read them. Thus "energy" has appeared before as a loose design word, not as a defined term. **[H]**
- #2 records the founder's own words about references. They name feels and one choice each: "the whole faded feel of everything ... an almost ethereal feel" (site-khufus), "done with just 2 colours" (turtles1), "the types of colours used here and how they interacted" (vietnam). He connects a feel to a choice in his own speech, but no file keeps the connection. **[H]**
- #42 and #27: search does not read the entry field `mood` (by decision). **[H]**
- #127 and #172 wrote "the brand-layer line" (house-principles.md): be distinctive in the brand layer (ground colour, illustration, display type, voice, motion character), conventional in the signifiers. It cites Lavie and Tractinsky (2004) for classical against expressive beauty. This is the one house reference that names an empirical aesthetics frame. It rules where expression may go, not which feel to aim at. **[H]**
- #104 (`docs/research/design-coverage-gaps.md` W4) found Tuch et al. (2012) and called complexity and prototypicality a **gap**. #3769 on mantahostels brought Lindgaard 2006, Tuch 2012 and Reinecke and Gajos 2014 (`docs/research/manta-design-migration.md` P6). **[H]**
- `docs/research/surface-styling.md` (#117) already ties two choices to "brand tone": card type ("outline = crisp, drawn; fill = quiet, soft; shadow = physical, raised", line 82) and radius scale ("a playful, warm brand can take larger radii; a dense data tool can take smaller ones", line 159). Its source is design-system practice, not a study. **[H]**
- `docs/research/brand-palette.md` (#183 family) uses "energy" for a high-chroma, contrasting figure on its ground, and says the remedy for a "boring" narrow palette is "energy from lightness, scale, type and photographs, not from a new hue". **[H]**

### H2. The library (`data/gallery.json`)

- **Entry `mood`**: 46 of 96 entries have 2 or 3 free mood words. 84 distinct words; the most frequent are warm (10), calm (5), quiet (5), still (5). Only one entry has "loud". No word list, no scale, no link to choices. Search does not read it. **[H]**
- **Collection `vocabulary`** (16 collections, AI register): each line names choices (for example "monumental sans typography", "restrained accent", "extreme negative space", "low-key studio lighting", "refined serif display"). Some lines carry feel words ("restrained", "refined", "quiet CTA"). The collection `description` and `deployFor` say the feel in plain words ("feel expensive", "calm and sure of itself", "Warm, human and a little magical"). Thus each collection is a **named style that bundles a feel with its choices**, but the feel is prose, not a value on a stated scale. **[H]**
- **Collection `imageStyle`**: a prompt template for an image model. Some name feel and choices together ("restrained palette", "dramatic soft side lighting", "wondrous but not childish"). **[H]**
- **`data/styles.json` (the Style guide, 18 styles, upstream copy)**: each style has `recognize` cues (choices: "tight-tracked sans, medium weights", "one muted accent, used rarely", "thick black outlines", "ultra-light oversized display type") and `vocabulary` with feel words ("quiet confidence", "unhurried", "friendly energy", "apothecary restraint", "single screaming hue"). This file is the house's nearest thing to a feel-to-choice table. It is **practitioner convention, era-bound** (it names "the standard aesthetic families of the modern web"), with no source per cue. **[H]**
- **House DNA (`dna`)**: `constants` is empty; `never` holds 13 lines (7 "AI look" tells, 2 "taste" lines, 4 others). One taste line touches feel: "several colours at equal weight, none dominant". The DNA bans looks; it does not state a feel to aim at or link a feel to choices. **[H]**

### H3. The design-round skill

- `plugin/skills/design-round/SKILL.md` §1: the brief field **Aesthetic** is "the direction, in words", one line per direction. **Client values** is "adjectives and short rules". Neither field asks for a feel on a scale, and neither ties an adjective to a choice. **[H]**
- §2 **direction cards**: Evidence, Carry over, Invent ("palette decisions"), Avoid repeating, Build scope, Technique, Model, Family, Beats. **No card field names the feel (tone) the direction aims at.** A critic thus cannot check a candidate against a stated feel, only against Client values adjectives. **[H]**
- `references/prompts.md`: the GPT image template ends "[3-5 MOOD WORDS]; [LIGHT]; [STYLE, WITH ITS TEXTURE]". Mood words go to the image model; nothing says which choices they imply. **[H]**

### H4. impeccable 4.5.0 (`~/.claude2/plugins/cache/impeccable/impeccable/4.5.0/skills/impeccable/`)

- **`quieter` command** (`reference/quieter.md`) is the one place in the house stack that **links a loud-to-quiet feel to concrete choices**: "Reduce saturation: Shift from fully saturated to 70-85% saturation"; "Reduce color variety"; "Neutral dominance ... (10% rule)"; "Gentler contrasts"; "Reduce font weights (900 → 600, 700 → 500)"; "White space: Increase breathing room, reduce density"; "Borders & lines: Reduce thickness, decrease opacity, or remove entirely"; "Simplify shapes: Reduce border radius extremes"; "Clean up effects: Reduce or remove blur effects, glows, multiple shadows"; motion "Shorter distances (10-20px instead of 40px) ... Never bounce or elastic"; "Reduce scale jumps". It names its target "refined and easier on the eyes. Think luxury". It lists intensity sources: saturation, contrast extremes, visual weight, animation, complexity, scale. No source is cited for any number. **[S], convention.**
- **`bolder` command** (`reference/bolder.md`): "Amplify what the system already owns"; "If every element got louder, the section got flatter". It does not list choices that make a design louder; it says to reuse the system's own strongest moves. **[S]**
- **`concept-seed`**: it deals catalogue "worlds" (each with SYSTEM GRAMMAR: palette/material, type/composition, topology, controls/state, responsive/motion). Its only steering axis is a **re-roll register: plain, safer, bolder**, "the user's steering on the familiar-to-bold axis" (`reference/new-work.md:49`). This axis is **novelty against the category default** (the prototypicality axis of Tuch et al.), not the quiet-to-loud axis of N15. **[H]**
- `reference/new-work.md:69`: "Energy is not the enemy of trust ... adjectives describing the product's behavior (quiet support, calm coaching) do not dictate the surface's energy." impeccable uses "energy" as the founder does, and separates it from the product's described behaviour. **[S]**
- `reference/doctor.md:37`: an older PRODUCT.md field `## Register` is deprecated: "Treat that field as absent". The visitor modes (Persuade, Operate, Read, Experience) replaced it. The modes set how far the world may reach into a page, not a feel. **[H]**
- `reference/critique.md:233`: on a "tonal mismatch", ask "Is that the intended tone, or should it feel warmer/bolder/more playful?" and "Offer 2-3 tonal directions". impeccable uses **tone** as the word for intended feel. **[S]**

### H5. The Manta brand sheet (read only; owner: mantahostels)

- `~/mantahostels/docs/brand/brand-sheet.md` §1–§2 (commit 921bd552d, 30 Sep 2026): a **feeling hierarchy** ("effortless first; trustworthy and fun tied close second"), a named enemy ("corporate/sterile"), and a **volume scale per zone**: "Hero/marketing: saturated colour grounds, big type, badges — Volume ~6–7"; "Working area: warm but calm — white cards on sand, colour only where it carries information — Volume ~4–5". "Energy is localised, not uniform." **This is the only house-family file that states a feel as a number on a scale and ties it to choices.** It is Manta's, not the vault's, and the scale has no defined anchors (what volume 1 or 10 looks like). **[H]**

## Part A. Frames that measure how people see a web page

### A1. Lavie and Tractinsky (2004): classical and expressive aesthetics

- Lavie, T. and Tractinsky, N. (2004). "Assessing dimensions of perceived visual aesthetics of web sites". *International Journal of Human-Computer Studies* 60(3): 269–298. Four studies, factor analyses. Two dimensions: **classical** ("orderly and clear design", "aesthetic notions that presided from antiquity until the 18th century") and **expressive** ("the designers' creativity and originality ... the ability to break design conventions"). Source: abstract as printed on the Cambridge talks page (talks.cam.ac.uk/talk/index/7931), read 15 Oct 2026. **[P]** (abstract read; paper not opened).
- Items, as Moshagen and Thielsch (2010, §1) quote them: classical = "aesthetic", "pleasant", "symmetric", "clear", "clean"; expressive = "creative", "fascinating", "original", "sophisticated", "uses special effects". **[P]** (quoted in a primary paper, read in full).
- **Note for N15:** "sophisticated" loads on **expressive**, not on classical. Thus "refined" in the founder's sense is not the same as "classical". A refined page can be orderly (classical) and also original (expressive). The two dimensions are two scales, not two ends of one scale.
- **Limit:** the scales measure how good a page looks in two ways (appraisal). They do not describe a feel such as "loud" or "calm". Moshagen and Thielsch: "the items and scales are too abstract to allow for optimizing the design of a website". **[P]**
- Era: **timeless** as a frame (it rests on old aesthetic theory); the items were set on 2000s websites.

### A2. Moshagen and Thielsch (2010): VisAWI, four facets

- Moshagen, M. and Thielsch, M. T. (2010). "Facets of visual aesthetics". *IJHCS* 68(10): 689–709, doi:10.1016/j.ijhcs.2010.05.006. Author copy read in full (uni-muenster.de), 15 Oct 2026. Seven studies. **[P]**
- Four facets (§ results): **Simplicity** — "clarity, orderliness, homogeneity, grouping, and balance"; **Diversity** — "visual richness, dynamics, variety, creativity, and novelty"; **Colorfulness** — "the evaluation of individual colors and their composition"; **Craftsmanship** — "whether the site was designed with skill and care using modern technologies".
- Items (Table 4, translated from German), for example: Simplicity "The layout appears too dense. (r)", "The layout appears well structured."; Diversity "The layout is pleasantly varied.", "The layout appears dynamic.", "The design appears uninspired. (r)"; Craftsmanship "The layout is not up-to-date. (r)".
- Relation to Lavie and Tractinsky (Table 6, study 5, N = 512): classical aesthetics correlates .82 with Simplicity; expressive aesthetics correlates .80 with Diversity. Thus **classical ≈ simplicity (order, low density)** and **expressive ≈ diversity (richness, dynamics, novelty)**. **[P]**
- **Choice links that the facets give (strong, but only at the level of the facet):** density and structure go to Simplicity; variety, dynamics and novelty go to Diversity. Colour is its own facet and is judged on harmony, not on amount. Craftsmanship includes "up-to-date", which is **era-bound** by its wording.
- **Limit:** like A1, VisAWI is an appraisal scale. A page scores high or low on each facet; the facets do not name a feel to aim at. They do show that "order" and "richness" are separate axes that people judge apart.

### A3. Tuch et al. (2012): visual complexity and prototypicality

- Tuch, A. N., Presslaber, E., Stöcklin, M., Opwis, K. and Bargas-Avila, J. A. (2012). "The role of visual complexity and prototypicality regarding first impression of websites". *IJHCS* 70(11): 794–811, doi:10.1016/j.ijhcs.2012.06.003. Abstract read on research.google/pubs/pub38315, 15 Oct 2026. "VC and PT affect participants' aesthetics ratings within the first 50 ms of exposure"; "websites with low VC and high PT were perceived as highly appealing". **[P]** (abstract read).
- For N15 it adds one thing: **complexity is one of the two fastest-read properties of a page**. A "loud" page is usually a more complex page, and complexity has a measured cost at first sight.
- Era: mechanism **timeless**; what is prototypical for a category is **era-bound**.

### A4. Reinecke and Gajos (2014): colourfulness and complexity across people

- Reinecke, K. and Gajos, K. Z. (2014). "Quantifying visual preferences around the world". *CHI '14*, doi:10.1145/2556288.2557052. Full text read (iis.seas.harvard.edu PDF), 15 Oct 2026. About 2.4 million ratings from about 40,000 people. **[P]**
- The two measures are computed from a screenshot: colourfulness from "the average saturation of colors across all pixels", the Hasler and Süsstrunk colourfulness metric, the number of image areas, quadtree leaves, and "the percentage of pixels containing one of seven colors"; complexity from "the number of areas containing text or other objects", space-based decomposition leaves, and more (§ method, building on Reinecke et al. 2013). Thus **colourfulness and complexity are measurable from pixels**, and they are the two measurable parts of what the founder calls "loud".
- Findings: "websites with a high visual complexity are generally disliked more than those with a low to medium complexity"; appeal peaks at complexity about 4.2 (on the model's scale), with a moderate cost below the peak (Cohen's d = 0.6) and a large cost above it (d = 2.0). For colourfulness, "In most countries, ratings of appeal increase up to a moderate to high colorfulness before steeply declining"; for Finland, Russia, France and Germany appeal peaks at a lower colourfulness. "Females ... liked colorful websites more than males"; "Education level negatively correlates with preferences for colorful and complex sites". The authors say older people's taste for more complex sites may be "a generational effect; older users might simply be more used to text-heavy 'web 1.0' designs". **[P]**
- **Meaning for N15:** the right "volume" is **audience-bound and culture-bound**, and too loud costs more than too quiet. This is an appraisal finding (how well liked), not a feel finding.
- Era: the curve shapes are **timeless** as a pattern; the peak positions are **cultural and era-bound** (2012–2013 web, LabintheWild volunteers).

### A5. Kansei engineering and semantic-differential studies of pages and type

- **Kim, Lee and Choi (2003).** "Designing emotionally evocative homepages: an empirical study of the quantitative relations between design factors and emotional dimensions". *IJHCS* 59(6): 899–940, doi:10.1016/j.ijhcs.2003.06.002. Paper not read (paywall). As Faiola et al. (2011) describe it: 278 adjectives reduced to **13 emotional dimensions** "measured by 30 representative emotive adjectives" ("such as cute, vibrant, mystic"); 36 professional designers made pages for each dimension; 418 South Korean users rated them; the study related design factors to the dimensions. **[P] via secondary.**
- **Faiola, Ho, Tarrant and MacDorman (2011).** "The aesthetic dimensions of U.S. and South Korean responses to web home pages: a cross-cultural comparison". *IJHCI* 27(2): 131–150, doi:10.1080/10447318.2011.537173. Full text read, 15 Oct 2026. U.S. participants (54 completed) "reliably applied translations of the emotional adjectives", but "the aesthetic perceptions of U.S. and South Korean participants formed different aesthetic dimensions composed of different sets of emotional adjectives". **[P-weak]** (small U.S. sample).
- **Meaning for N15:** the one study that mapped page design factors to a full set of feels **did not replicate across cultures**. A fixed list of feel buckets, with fixed choices per bucket, is thus **culture-bound** at the level of fine buckets.
- **Qiu, Watanabe and Omura (2017).** "Images and anatomy of Latin typefaces". *International Journal of Affective Engineering* 16(2): 121–130, doi:10.5057/ijae.IJAE-D-16-00028. Full text read. Kansei study, 88 designers (Japan). Four factors: **elegance** (gorgeous, elegant, romantic, classic, noble, chic, formal), **practicality** (standard, readable, reliable, clear), **tenderness** (pretty, friendly, modern, fresh), **powerfulness** (dynamic, wild). Script, modern serif (high stroke contrast, "thick and thin lines") and old-style serif clusters load on elegance; grotesque and neo-grotesque sans load on practicality. **[P-weak]** (one sample, designers only).
- **Shaikh and Chaparro (2016).** "Perception of fonts: perceived personality traits and appropriate uses". In *Digital Fonts and Reading*, doi:10.1142/9789814759540_0013. Abstract read. 40 typefaces on 15 semantic-differential scales gave **three factors: Potency, Evaluative and Activity**, after Osgood, Suci and Tannenbaum (1957). Ads should match the product's personality; other documents do better with faces higher on Potency and Evaluative than Activity. **[P]** (abstract read). An earlier report by the same group: serif read "more traditional", sans "more casual", monospace "plain and dull". **[P-weak]**

### A6. The general frame under all of these: Evaluation, Potency, Activity

- Osgood's semantic differential found three dimensions of affective meaning: **Evaluation** (good–bad), **Potency** (strong–weak, heavy–light), **Activity** (active–passive, fast–slow). Osgood, May and Miron (1975), *Cross-Cultural Universals of Affective Meaning*, found them in about 30 language communities. Source: as cited by later EPA studies (search summary, 15 Oct 2026); the book was not read. **[S]** for this report;
- The same three axes appear in each domain the founder's note touches:
  - **Colour:** Ou, Luo, Woodcock and Wright (2004), "A study of colour emotion and colour preference. Part I", *Color Research & Application* 29(3): 232–240, doi:10.1002/col.20010: ten scales on 20 colours, 31 British and Chinese observers, gave three factors — **colour activity, colour weight, colour heat** (abstract read; Part III read in full). Activity ≈ Osgood's Activity, weight ≈ Potency. **[P]**
  - **Emotion:** Valdez and Mehrabian (1994), "Effects of color on emotions", *Journal of Experimental Psychology: General* 123(4): 394–409 (PubMed 7996122, abstract read): on the Pleasure–Arousal–Dominance model, "Pleasure = .69B + .22S, Arousal = -.31B + .60S, Dominance = -.76B + .32S" (B brightness, S saturation). **[P]**
  - **Type:** Shaikh and Chaparro (2016), above: Potency, Evaluative, Activity. **[P]**
- **The founder's "energy" is the Activity (arousal) axis.** "Loud" is high Activity, usually with high Potency. His "refined" is not the opposite end of one axis: it is lower Activity, **lower Potency** ("thin lines" are light, not heavy), and high Evaluation (care, craft). Psychology also uses "energy" for this axis: Thayer's "energetic arousal" (Thayer, *The Biopsychology of Mood and Arousal*, 1989; **[S]**, not read).
- Era: **timeless**. The axes are cross-cultural; which choices sit where on them is partly cultural (A5, C below).

### A7. Brand personality (Aaker 1997)

- Aaker, J. L. (1997). "Dimensions of brand personality". *Journal of Marketing Research* 34(3): 347–356. Full text read (JSTOR copy). 631 U.S. respondents, 37 brands, 114 traits; five factors explained 92% of variance. **[P]**
- Five dimensions with their facets (Appendix A): **Sincerity** (down-to-earth, honest, wholesome, cheerful); **Excitement** (daring, spirited, imaginative, up-to-date); **Competence** (reliable, intelligent, successful); **Sophistication** (upper class, charming — traits include "glamorous", "good looking", "smooth"); **Ruggedness** (outdoorsy, tough).
- Aaker's own limit: "the current scale might not be appropriate for measuring brand personality in a different cultural context". **[P]**
- Aaker, Benet-Martínez and Garolera (2001), *JPSP* 81(3): 492–508: Japan shared four dimensions and added **Peacefulness**; Spain shared three and added **Passion**; Competence and Ruggedness were U.S.-specific in that comparison. Source: Stanford GSB and RePEc listings (search summary). **[P]** (abstract level).
- **Meaning for N15:** Aaker measures **who the brand is**, not how the page looks. "Excitement" is the nearest dimension to "loud"; "Sophistication" is the nearest to "refined". A design's feel serves the brand personality; the two are not the same thing.
- Era: the five-factor list is **U.S. 1990s** and **culture-bound**.

## Part B. The terms in use, and the term for the house

| Term | What it names in use | Source | Fit for N15 |
|---|---|---|---|
| **Brand personality** | The human traits of the brand (Aaker's five dimensions). Who the brand is. | Aaker 1997 **[P]** | The cause, not the feel of one design. It sits above the design. |
| **Voice and tone** | Voice is constant; tone changes with the moment. "You have the same voice all the time, but your tone changes." | Mailchimp Content Style Guide **[S]**; NN/g, Moran (2016, reviewed 2023): four tone dimensions, "Formal vs. casual", "Serious vs. funny", "Respectful vs. irreverent", "Matter-of-fact vs. enthusiastic" **[S]** | Written-word terms. The voice/tone split matches the founder's need: one brand, many surfaces, each at its own level. |
| **Visual tone / tone** | The feel a visual design gives. | impeccable `critique.md:233` ("Is that the intended tone"); house `surface-styling.md` ("brand tone") **[S]**, **[H]** | **Best fit.** Already in house use; pairs with voice and tone. |
| **Look and feel** | Loose trade phrase for the whole visual and interaction character. | Common usage **[S]** | Too loose to check. |
| **Design language / visual language** | A whole system of rules and parts (Material calls itself a "visual language", 2014). | Google, as quoted by secondary sources **[S]** | Too large: a language holds many tones. |
| **Style (named style, aesthetic family)** | A named bundle of choices: Swiss, brutalism, quiet luxury. | `data/styles.json` ("Family name in a brief carries fifty decisions") **[H]** | A style *produces* a tone. It is a convention, and era-bound. |
| **Aesthetic register** | Rare in design writing. In impeccable 4.5.0 "register" names the plain/safer/bolder re-roll axis (familiarity), and an old `## Register` field is deprecated. | impeccable **[S]** | Avoid: the word already means other things in the house stack. |
| **Mood** | The emotional atmosphere of an image or scene; a "mood board". | Gallery `mood` field; prompts.md "[3-5 MOOD WORDS]" **[H]** | Keep for image and art. |
| **Energy / volume / intensity / arousal** | One axis: how calm or how loud. | Founder N15; Manta brand sheet "Volume ~6–7"; impeccable `quieter` "visual intensity" and new-work.md "the surface's energy"; psychology: Activity (Osgood), arousal (Mehrabian), energetic arousal (Thayer) **[P]**/**[S]**/**[H]** | The founder's word is correct for **one axis** of tone, not for all of tone. |

**Recommendation (inference, not a source):** call the whole thing **tone** (in full, *visual tone*). State it as positions on a few scales (Part D), one of which is **energy** (the founder's word, Osgood's Activity). Keep **brand personality** for who the brand is, **style** for a named bundle of choices, and **mood** for images.

## Part C. Which choices evidence ties to which feel

Strength key: **Strong** = several primary studies agree; **Moderate** = one good primary study or several weak ones; **Weak** = one small study; **Convention** = design-system or practitioner practice, no study found.

| Choice | Ties to | Evidence and strength | Timeless or bound |
|---|---|---|---|
| **Colour saturation (chroma)** | Higher saturation → more energy (arousal, Activity). | Valdez and Mehrabian 1994: "Arousal = -.31B + .60S" **[P]**. Wilms and Oberfeld 2018, *Psychological Research* 82(5): 896–914 (PubMed 28612080, abstract read): "saturated and bright colors were associated with higher arousal"; stronger skin-conductance response **[P]**. Palmer et al. 2013, *PNAS*, doi:10.1073/pnas.1212562110 (abstract read): in U.S. and Mexican groups, "faster music in the major mode produced color choices that were more saturated, lighter, and yellower" **[P]**. Ou et al. 2004: "colour activity" factor **[P]**. **Strong.** | Timeless (cross-cultural in these samples). |
| **Colour lightness** | Lighter → more pleasant, less dominant (lighter weight). Darker → more dominant, heavier. | Valdez and Mehrabian 1994: "Pleasure = .69B + .22S", "Dominance = -.76B + .32S" **[P]**. Ou et al. 2004: "colour weight" factor **[P]**. **Strong.** | Timeless. |
| **Hue** | Red end more arousing than blue and green (in Wilms and Oberfeld); warm–cool is its own axis. | Wilms and Oberfeld 2018 **[P]**; Ou et al. 2004 "colour heat" **[P]**. But Valdez and Mehrabian found green-yellow, blue-green and green "the most arousing" **[P]**: the studies disagree on hue. Jonauskaite et al. 2020, *Psychological Science* 31(10) (PubMed 32900287): colour–emotion links are largely universal (r = .88 across 30 nations) but nation adds its own pattern **[P]**. **Moderate**; hue effects are smaller and less stable than saturation and lightness effects. | Partly cultural. |
| **Colour count and colourfulness** | More colours, more saturated → more "colourful", more diverse; preference peaks at moderate-to-high then falls steeply. | Reinecke and Gajos 2014 **[P]**; VisAWI Colorfulness judges harmony, not amount **[P]**. House DNA taste line: "several colours at equal weight, none dominant" **[H]**. **Moderate–strong** for the appeal curve; the link to "loud" is direct (pixel saturation is part of the metric). | Peak position cultural and audience-bound. |
| **Contrast (lightness contrast, scale contrast)** | High contrast and big scale jumps → louder; low contrast → quieter. | impeccable `quieter`: "Contrast extremes", "Reduce scale jumps: Smaller contrast between sizes creates calmer feeling" **[S]**. Manta: "big type" in the volume-6–7 zone **[H]**. No study found that isolates contrast as a cause of arousal on a page. **Convention**, consistent with the lightness and size evidence. | Convention. |
| **Line and stroke weight** | Thin → light, weak, delicate (low Potency); thick → heavy, strong. | Albertazzi, Canal, Micciolo and Hachen 2021, "The perceptual organisation of visual elements: lines", *Brain Sciences* 11(12): 1585 (PMC8699471, read): "The highest odds ratios were found for the pairs heavy/lightweight and strong/weak"; "less thick lines were considered feminine, while thicker lines were considered masculine" **[P-weak]** (N = 28 and 25). impeccable `quieter`: "Borders & lines: Reduce thickness" **[S]**. **Moderate**: the direction is clear; no web-page study found. | Timeless for the Potency direction; the "feminine/masculine" reading is cultural. |
| **Type weight** | Heavier weight → more Potency and louder; lighter → quieter, more refined. | Qiu et al. 2017 "powerfulness" factor (dynamic, wild) **[P-weak]**; Shaikh and Chaparro 2016 Potency factor **[P]**; Henderson, Giese and Cote 2004, *Journal of Marketing* 68(4): 60–72 (abstract read): "weight" is one of six typeface design dimensions that drive impressions (pleasing, engaging, reassuring, prominent) **[P]**. impeccable `quieter`: "Reduce font weights (900 → 600, 700 → 500)" **[S]**, no source for the numbers. **Moderate.** | Direction timeless; the numbers are convention. |
| **Type style** | High-contrast (modern) serif, old-style serif and script → elegance; grotesque/neo-grotesque sans → practicality, reliability; serif → traditional; sans → casual; mono → plain. | Qiu et al. 2017 **[P-weak]**; Shaikh, Chaparro and Fox 2006 **[P-weak]**. impeccable `new-work.md:67` warns that subject–face associations ("books wanting a serif ... tech wanting a mono") are the defaults it exists to break **[S]**. **Moderate**, and **era-bound**: what reads "modern" or "traditional" moves with use. | Era- and culture-bound. |
| **Shape: corner radius, curvature** | Round → soft, warm, friendly, comfortable, calmer; angular → hard, durable, sharp, more arousing. | Bar and Neta 2006, *Psychological Science* 17(8) (PubMed 16913943): sharp contours "convey a sense of threat" **[P]**. Bertamini et al. 2016, *British Journal of Psychology* (doi:10.1111/bjop.12132): "curved shapes are, per se, visually pleasant" **[P]**. Jiang, Gorn, Galli and Chattopadhyay 2016, *Journal of Consumer Research* (doi:10.1093/jcr/ucv049): "circular- versus angular-logo shapes activate softness and hardness associations" **[P]**. Albertazzi et al. 2021: curved lines "soft, dynamic, and warm" **[P-weak]**. Pacheco et al. 2015 (ACHI): curved shapes "more positive and less arousing" (search summary) **[P-weak]**. House `surface-styling.md`: "a playful, warm brand can take larger radii; a dense data tool can take smaller ones" **[H]**. **Strong** for the round–soft / angular–hard link; **convention** for any radius number. | Link timeless; preference strength varies by culture and by self-construal (2025 Frontiers study, abstract) **[P-weak]**. |
| **Spacing, density, white space** | More space, less density → calmer, more ordered (classical/simplicity), and in many markets → prestige and quality; dense → busy, louder, more complex. | VisAWI Simplicity item "The layout appears too dense. (r)" **[P]**; Tuch 2012 and Reinecke and Gajos 2014 on complexity **[P]**. White space as prestige: Pracejus, Olsen and O'Guinn 2006, *JCR* 33(1): 82–90: the meaning comes from history, "how objects and symbols derive meaning from their histories" **[P]**; Pracejus, O'Guinn and Olsen 2013, *IJRM* 30(3): 211–218: white space meanings come from 20th-century North American art and "vary across cultures" (abstract, paraphrased by the fetch tool) **[P]**. A 2023 packaging study (China, N = 405) found high white space lowered purchase intention for high-end products, the opposite of the Western reading (abstract) **[P-weak]**. **Strong** for density → complexity; **moderate** for white space → prestige, which is **cultural and era-bound**. | Density link timeless; prestige reading cultural. |
| **Symmetry and order** | Symmetry → stable, quality, premium; asymmetry and broken conventions → expressive. | Lavie and Tractinsky 2004 "symmetric" on classical **[P]**; 2025 *PLoS ONE* (doi:10.1371/journal.pone.0317229): symmetric logos raise perceived quality via "perceived stability" **[P-weak]**; 2022 packaging study (n = 741): "a significant positive effect of symmetry" on premiumness **[P-weak]**. **Moderate.** | Mostly timeless. |
| **Motion: speed, distance, easing, amount** | Fast, large, bouncy, frequent → energetic, expressive; short, gentle, rare → calm, productive. | IBM Carbon: "Productive motion creates a sense of efficiency and responsiveness, while remaining subtle"; "Expressive motion delivers enthusiastic, vibrant, and highly visible movement ... Reserve expressive motion for occasional, important moments" **[S]**. Lockyer, Bartram and Riecke 2011 (Computational Aesthetics): path curvature, speed and layout change "valence, comfort, urgency and intensity" (search summary) **[P-weak]**. Pacheco et al. 2015: slow movement "less arousing and more positive" **[P-weak]**. impeccable `quieter`: "Shorter distances (10-20px instead of 40px) ... Never bounce or elastic" **[S]**. Manta M1: "motion never announces itself" **[H]**. **Moderate** for speed → arousal; **convention** for every number. | Direction timeless; durations and curves era-bound. |
| **The whole "expressive" set** | Colour, shape, size, motion and containment used boldly → "energetic, emotive ... creative, playful, and friendly". | Google, "Better, easier, emotional UX" (M3 Expressive research, design.google, undated, 2025): "46 separate research studies", over 18,000 participants; expressive designs rated higher on "energetic, emotive, positive-vibe, creative, playful, and friendly"; "a strong minority of users preferred calmer, less intense versions"; "When basic interaction paradigms are broken, expressive design can lead to poor usability or negative sentiment" (fetch-tool quotes) **[P]** (first-party, not peer-reviewed). | Era-bound (2025 Android); preference strongest at ages 18–24. |

### C1. What this means for "refined" and "loud"

- **Loud** (high energy): high saturation, many colours at similar weight, high lightness and scale contrast, heavy type and thick lines, angular shapes, dense layout, fast and large motion. Most items have at least moderate evidence for their direction; the motion numbers and the contrast and scale jumps are convention.
- **Refined** (the founder's word): low-to-moderate energy, **light weight** (thin lines, lighter type weight, high-contrast serif or careful sans), restrained colour (few colours, one accent, lower saturation), generous space, precise alignment, and visible care. impeccable `quieter` says it the same way: "'Quieter' doesn't mean boring or generic. It means refined ... Think luxury, not laziness."
- **Where the link is only convention:** every number (saturation 70–85%, weight 900 → 600, radius values, motion distances and durations), and the reading of a named style (quiet luxury, brutalism). **Where it is cultural or era-bound:** type style meaning, white space as prestige, hue meaning, preferred colourfulness and complexity, and every named style.

## Part D. The buckets: scales or named styles

### D1. Scales with empirical support

The evidence supports **scales (dimensions)**, not a fixed list of named feels. Three scales have strong support (energy, weight, order to richness) and two moderate (warmth, which rests on partly cultural hue evidence; familiarity, which rests on Tuch 2012 read as an abstract). The set of five is this report's synthesis; **no study validates these five together as a web-design tone set.**

| Scale | Low end ↔ high end | Evidence | Main choices that move it (Part C) |
|---|---|---|---|
| **Energy** (Activity, arousal) | calm, quiet ↔ loud, lively | Osgood EPA; Valdez and Mehrabian; Wilms and Oberfeld; Ou "colour activity"; M3 Expressive "energetic" | saturation, colour count, contrast and scale jumps, motion speed and amount, density |
| **Weight** (Potency) | light, delicate ↔ heavy, strong | Osgood EPA; Ou "colour weight"; Valdez and Mehrabian Dominance; Albertazzi et al. 2021; Shaikh and Chaparro Potency | line and type weight, lightness (dark = heavy), size |
| **Warmth and softness** | cool, hard ↔ warm, soft | Ou "colour heat"; Jiang et al. 2016; Bar and Neta 2006 | hue (warm–cool), corner radius and curvature, type style (rounded, humanist) |
| **Order ↔ richness** (classical ↔ expressive) | ordered, simple ↔ varied, inventive | Lavie and Tractinsky 2004; VisAWI Simplicity and Diversity (r = .82 and .80) | grid and alignment, symmetry, density, variety of elements, special effects |
| **Familiarity** (prototypicality) | category-typical ↔ novel | Tuch et al. 2012; impeccable's plain/safer/bolder register | layout structure against the category's usual structure |

- A sixth axis, **Evaluation** (good–bad, Craftsmanship in VisAWI), is not a feel to choose: every design aims high on it.
- **"Refined"** is a position across scales: energy low to moderate, weight light, order high, familiarity moderate, craft high. **"Loud"** is energy high, weight usually heavy, richness high. The founder's two words are thus **two regions of a space**, not two ends of one line.

### D2. Named styles: wide professional use, weak empirical support

- Professional practice names styles: the vault's `data/styles.json` (18 "aesthetic families of the modern web") and 16 collections; impeccable's catalogue "worlds". A named style is a **bundle**: a position on the scales above plus signature motifs (halftone dots, thick black outlines, letterspaced caps). **[H]/[S]**
- The bundle is useful in a brief ("Family name in a brief carries fifty decisions", `styles.json`). It is also **era-bound** (Y2K, neo-brutalism, bento grid are dated families) and carries the AI-look risk that the House DNA bans (for example "a warm cream ground ... with a high-contrast serif display" is warm-editorial's look).
- Fine-grained named feel buckets do not hold across cultures: Kim et al.'s 13 Korean dimensions formed different dimensions for U.S. viewers (Faiola et al. 2011) **[P-weak]**; Aaker's five brand dimensions became four-plus-Peacefulness in Japan and three-plus-Passion in Spain **[P]**.
- **How the two relate:** scales describe the feel; named styles are shortcuts to a region of the scales plus a motif set. A style can be placed on the scales (for example, by its `recognize` cues: quiet-luxury "light-weight serif, wide tracking; ivory / taupe / bone palette" = low energy, light weight, warm; neo-brutalism "thick black outlines ... saturated flat fills" = high energy, heavy weight, angular). This placement is this report's reading, not a measured one.

## Part E. House match

| What the house holds | States a feel? | Links feel to choices? | Gap |
|---|---|---|---|
| design-round brief: Aesthetic, Client values (SKILL.md §1) | Yes, as free words and adjectives | No | No scale and no choice list; a critic cannot check "is this as calm as asked". |
| Direction cards (SKILL.md §2) | **No feel field** | No | The card names evidence, technique and palette decisions, but not the tone the direction aims at. |
| prompts.md image template "[3-5 MOOD WORDS]" | Yes, free words | No | Mood words go to the image model with no choices behind them. |
| Gallery entry `mood` (46 of 96 entries, 84 distinct words) | Yes, free words | No | Not on any scale; search does not read it (#27, #42). |
| Collections `description`/`deployFor` (plain) and `vocabulary`/`imageStyle` (AI register) | Yes, in prose | **Yes, by bundle** (named style) | Convention, no strength label, no scale position. |
| `data/styles.json` (Style guide) | Yes (feel words in `vocabulary`) | **Yes, by bundle** (`recognize` cues) | Upstream copy, era-bound, unsourced. |
| House DNA `never` | Only one taste line touches feel | No | The DNA bans looks; it never states a feel to aim at. Its `constants` list is empty. |
| impeccable `quieter` | Yes ("too loud" → "refined") | **Yes, explicitly**, per choice | Numbers unsourced; the direction of each move agrees with the evidence in Part C. `bolder` has no matching list. |
| impeccable `concept-seed` register (plain/safer/bolder) | Familiarity, not energy | No | Its "bolder" is novelty, not loudness. A founder saying "bolder" to mean "louder" gets a different axis. |
| house-principles.md "brand-layer line" (#127) | No | Says *where* expression may go (brand layer, not signifiers) | Rules placement, not level. Compatible with an energy scale. |
| `surface-styling.md` (#117) | "brand tone" | Two links: card type and radius scale | Convention; no scale defined for "tone". |
| Manta brand sheet §1–§2 (Manta's file) | Yes: feeling hierarchy, named enemy | **Yes: volume ~6–7 and ~4–5 per zone, with choices** | No anchors for the scale's ends; project-only; the vault has no equivalent for other projects. |

**Finding:** the house has many feel words and two working feel-to-choice links (impeccable `quieter`, Manta's volume scale). The vault's own round has **no place to state the target tone** and **no reference that ties a tone to choices with evidence strength**. Named styles and collections link feel to choices only as convention bundles.

**Gaps (#208 filled 1 to 4 and accepted 5):**

1. A **tone line** on the brief and on each direction card: the target position on the five scales (or the few that matter for the asset), in plain words for the founder.
2. A **house reference** that ties each scale to its choices, with Part C's strength and era labels, so a builder can move a design along a scale on purpose and a critic can check it.
3. A **critic question**: does the candidate sit where the tone line says, per scale, and which choices put it there?
4. A **vocabulary rule** for the words "bolder", "quieter", "louder", "calmer": energy and weight moves, kept apart from impeccable's familiarity register.
5. Optional: give the gallery `mood` words a scale position, so references can be found by tone.

**Where a question to the founder remains after this research:** the target position for each project and surface on the scales (a taste and business fact), which the tone line asks per brief. His "refined" was a lead to the gap, not a term to define (#208).

## Bound

- **Read in full:** Moshagen and Thielsch 2010 (author copy); Reinecke and Gajos 2014 (CHI PDF); Aaker 1997 (JSTOR copy); Faiola et al. 2011; Qiu, Watanabe and Omura 2017; Ou et al. 2004 Part III.
- **Read through fetch-tool quotes only:** Albertazzi et al. 2021.
- **Abstract only:** Lavie and Tractinsky 2004 (items taken from Moshagen and Thielsch's quotation); Tuch et al. 2012; Valdez and Mehrabian 1994; Wilms and Oberfeld 2018; Jonauskaite et al. 2020; Bar and Neta 2006; Bertamini et al. 2016; Jiang et al. 2016; Palmer et al. 2013; Henderson, Giese and Cote 2004; Shaikh and Chaparro 2016; Pracejus et al. 2006 and 2013; Ou et al. 2004 Part I; the 2022, 2023 and 2025 packaging and logo studies.
- **Search summary only (not opened):** Aaker, Benet-Martínez and Garolera 2001; Osgood, May and Miron 1975; Lockyer, Bartram and Riecke 2011; Pacheco et al. 2015; Thayer 1989; Poffenberger and Barrows 1924 (not used as a source).
- **Not verified, so not used:** Labrecque and Milne 2012 (*JAMS* 40(5): 711–727) saturation and value results for brand personality; Kim, Lee and Choi 2003's factor-to-emotion table; Henderson et al.'s per-dimension results; any typeface weight number.
- **First-party practice read:** IBM Carbon motion overview; Google design.google M3 Expressive research page (undated, 2025); NN/g Moran 2016; Mailchimp voice and tone.
- **House read:** `data/gallery.json` (dna, collections, entry `mood`), `data/styles.json`, design-round `SKILL.md` §1–§2 and `references/prompts.md`, `design-critique/references/house-principles.md`, `docs/research/` (surface-styling, brand-palette, design-coverage-gaps, manta-design-migration, principle-interactions by grep), impeccable 4.5.0 (`quieter.md`, `bolder.md`, `new-work.md`, `critique.md`, `doctor.md`; `concept-seed` run once in `/tmp` against a stand-in PRODUCT.md, then deleted), Manta `docs/brand/brand-sheet.md` §1–§2 (read only).
- **Issues searched** on this repo (all states): tone, feel, vibe (empty first run, then results), personality, energy, mood, aesthetic, style. Read for the terms: #2, #20, #24, #27, #29, #42 (grep of comments), and the house files that #117, #127, #104 wrote. No other tracker in `corpus` was searched.
- **Not done:** no page or render was measured; no study of web pages placed on the five scales of Part D was found or run; Japanese, Chinese and other non-Western sources were read only where cited above.
- Every quotation from a fetched page is as the fetch tool returned it; the tool paraphrases some long passages, and those are marked "paraphrased" or given as summaries.

