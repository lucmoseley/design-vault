# Image model profiles, part A: qualitative strengths and weaknesses

Ticket: #51. Date of research: 30 Sep 2026.

Tags:
- [measured-independent]: a third party measured it (paper, benchmark, arena with a published method).
- [measured-self-reported]: the maker measured it (technical report, model card).
- [systematic-practitioner]: a practitioner compared many prompts with a stated method. Lower tier.
- [opinion]: a statement with no measurement.


## Raw findings log

### Qwen line (Alibaba)
- Qwen-Image-3.0: release on 21 Jul 2026, only in Qwen Chat. No weights, no technical report, no benchmark scores, no model card. Maker claims: prompts to 4,500 tokens, legible text at 10 px, near-photo skin/hair/paper texture, 12 languages, live web data. Source: https://www.unite.ai/alibaba-launches-qwen-image-3-0-without-benchmarks-or-weights/ (Jul 2026), which points to https://qwen.ai/blog?id=qwen-image-3.0. Tag: [opinion] (maker).
- Qwen-Image-2.0 technical report (arXiv 2605.10730, 11 May 2026): Qwen3-VL condition encoder + MMDiT. Four caption types (general, text, knowledge, structured). Data: photography, graphic design, art, synthetic. VAE trained on text-rich images (PDFs, slides, posters). Human eval only: LMArena text-to-image Elo 1168, rank 9 global. The report gives no GenEval/DPG/OneIG numbers and no limitations section. Source: https://arxiv.org/html/2605.10730v1. Tag: [measured-self-reported].
- Qwen-Image (first version) technical report (arXiv 2508.02324, Aug 2025): 20B MMDiT, Qwen2.5-VL 7B text encoder. Data mix: nature 55 %, design 27 % (posters, UI, slides, art), people 13 %, synthetic text 5 %. Captions: Qwen2.5-VL writes JSON captions. Curriculum from no text to paragraph text. Scores: GenEval 0.91 (RL), DPG 88.32, LongText-Bench EN 0.943 (GPT Image 1: 0.956), OneIG-EN 0.539 with text 0.891 but style 0.418 and diversity 0.197. Source: https://arxiv.org/html/2508.02324. Tag: [measured-self-reported].
  - Why it matters: the design-heavy data (27 %) and synthetic text data explain the text and layout strength. The low OneIG style and diversity sub-scores are a sign of a narrower style range.

### Z-Image / Z-Image-Turbo (Alibaba Tongyi-MAI)
- Technical report arXiv 2511.22699 (27 Nov 2025, rev. 6 Jul 2026): 6B single-stream DiT (S3-DiT). Turbo = 8-step distillation (Decoupled DMD) + RL (DMDR). Captions carry world knowledge and explicit OCR text. A VLM "prompt enhancer" is necessary because the 6B model has "limitations in world knowledge, intent understanding, and complex reasoning". Source: https://arxiv.org/html/2511.22699. Tag: [measured-self-reported].
- Maker scores: CVTG-2K word accuracy Turbo 0.8585 (GPT Image 1: 0.8569, Qwen-Image 0.8288); LongText-Bench Turbo EN 0.917 (Qwen-Image 0.943); Alibaba AI Arena Elo Turbo 1025, rank 4, behind Imagen 4 Ultra 1048 and Seedream 4.0 1039. Same source. Tag: [measured-self-reported].
- The report emphasises photorealism and text. It does not discuss illustration, flat vector, palette or animals. Same source.

### FLUX.2 (Black Forest Labs)
- Launch 25 Nov 2025 (pro, flex, dev 32B open weights; klein later). [max] on 16 Dec 2025 with web "grounded generation". Architecture: Mistral-3 24B VLM text encoder + rectified-flow transformer + new VAE. Maker claims: up to 10 reference images for character/product/style consistency; reliable fine typography; better multi-part prompt following. No benchmark numbers and no limitations in the launch post. Source: https://bfl.ai/blog/flux-2 (25 Nov 2025). Tag: [opinion] (maker claim, no measurement).
- No FLUX.2 technical report on arXiv was found (search 30 Sep 2026).
- Maker prompting guide: hex colours work "best when clearly associated with specific objects"; "use #FF0000 somewhere" gives inconsistent results; no negative prompts; [pro] API limit 9 MP in+out (8 refs at 1 MP). Source: https://docs.bfl.ml/guides/prompting_guide_flux2. Tag: [opinion] (maker documentation).

### Ideogram (4.0 and 3.0)
- Ideogram 4.0: release 3 Jun 2026, open weights (non-commercial licence; hosted API commercial). 9.3B single-stream DiT, 34 layers, frozen Qwen3-VL-8B text encoder. Trained "exclusively on structured JSON captions" that are "deliberately extremely descriptive". JSON prompt accepts up to 16 hex colours per image (5 per element) and bounding boxes in 0-1000 coordinates. Plain-text prompts do less well than JSON because of the train/inference format gap. Source: https://huggingface.co/ideogram-ai/ideogram-4-nf4 and https://ideogram.ai/blog/ideogram-4.0/ (3 Jun 2026). Tag: [measured-self-reported] (architecture is fact; performance is maker claim).
- Maker scores: 7Bench layout 0.69 mIoU (objects inside requested boxes), X-Omni English OCR 0.97, SpatialGenEval 0.76, PRISM-Bench alignment 0.89. Maker designer-preference study: 4,366 blind votes from graphic designers, Elo GPT Image 2 1141, Ideogram 4.0 1062, Nano Banana 2 1004, Grok Imagine 990. Source: https://ideogram.ai/blog/ideogram-4.0/. Tag: [measured-self-reported].
- The maker does not publish a hex-palette accuracy number. The palette field exists; its accuracy is not measured by any source found. Tag: gap.
- Ideogram 3.0 lineage, MEF (ByteDance Seed, arXiv 2509.17907, Sep 2025): 377 prompts, 4 images each, about 20 trained expert raters. Ideogram 3.0 expert Elo 1078, MOS prompt following 3.91, structure 3.71, aesthetics 3.07 (lowest aesthetics of the rated set). Strength: text in design use. Midjourney V6.1: aesthetics 3.38 best of these three, but weak prompt following (3.36) and structure (3.31). Recraft V3 Raw expert Elo 1021. GPT-4o and Seedream 3.0 were far ahead. Source: https://arxiv.org/html/2509.17907v1. Tag: [measured-independent] (note: the maker of Seedream ran it).
- Perle study (arXiv 2608.14976, 24 Aug 2026): 48 hard compositional prompts (counts, attribute binding, text, spatial limits), four systems. Nano Banana Pro 84.8/100, FLUX.2 82.3, Ideogram 3.0 65.7, Hunyuan 3.0 63.3. Leaders fail on counts and geometric artefacts; trailing models garble text and omit elements. No human calibration. Source: https://arxiv.org/html/2608.14976. Tag: [measured-independent], small sample.

### Palette / hex obedience (cross-model)
- Paint-Anything / ACBench (ByteDance Seed, arXiv 2609.20816, 20 Sep 2026): 1,000 prompts that ask for an object in an exact hex colour. Score 0-100 from RGB mean absolute error (100 = MAE at or below 16). Overall T2I: FLUX.2-dev 51.70, Z-Image-Turbo 33.56, Qwen-Image 25.21, FLUX.1 23.00. Edit: FLUX.2-dev 68.87, Qwen-Image-Edit 54.40. Baselines "often produce colors that are semantically plausible but numerically distant from the requested hex value". GPT Image, Nano Banana, Seedream, Ideogram, Recraft and Grok are not in the test. Source: https://arxiv.org/html/2609.20816. Tag: [measured-independent].
  - FLUX.2 Pro/Flex/Max were not measured; dev is the same family.
- GenColorBench (arXiv 2510.20586, Oct 2025) and NumColor (arXiv 2603.13547, Mar 2026): FLUX.1 only reaches 13.82 % on coarse colour names from hex prompts (random 7.7 %). The cause is tokenisation of numbers. Source: https://arxiv.org/abs/2603.13547. Tag: [measured-independent]. FLUX.1 lineage only.

### Cross-model benchmark papers (open and closed models)
- Qwen-Image-Bench (Qwen team, arXiv 2605.28091, 27 May 2026): 56 facets, judge model Q-Judger trained on 130,000 human labels from 80 art-academy annotators. Overall: GPT Image 2 64.69, Nano Banana 2.0 59.82, Nano Banana Pro 59.45, Qwen Image 2.0 Pro 57.84, Seedream 5.0 57.22, FLUX 2 Max 55.33, FLUX 2 Pro 54.57. FLUX 2 Max/Pro are lowest of this group on "Real-world Fidelity" (49.35 / 47.29) and "Creative Generation" (56.50 / 56.18). "Animals" and "Anatomical Fidelity" are "systemic ceilings" for all models: best Animals score 42.6 (GPT Image 2), best Anatomical Fidelity 20.9. Colour harmony is "relatively mature" (industry mean above 60). Ideogram, Recraft, Grok, Midjourney, Z-Image not tested. Source: https://arxiv.org/html/2605.28091v1. Tag: [measured-self-reported] for Qwen rows; [measured-independent] for other rows (a competitor ran it).
- WeGenBench (Tencent Weixin, arXiv 2606.20100, 18 Jun 2026): 4,000 bilingual prompts; checklist QA, chain-of-thought score, aesthetics 1-5, OCR text F1. FLUX.2-dev QA 0.93, aesthetics 2.69, text F1 0.58 ("struggle[s] with character-level spelling"). Qwen-Image QA 0.91, aesthetics 2.56, text F1 0.46 (Qwen-Image-2512: 0.59). Z-Image aesthetics 2.44; Z-Image-Turbo text F1 0.73 but lower semantic score. GPT-Image-2 QA 0.97, aesthetics 2.84. Seedream-4.5 text F1 0.79 (best). Negation and counting fail for all. Source: https://arxiv.org/html/2606.20100v1. Tag: [measured-independent].
  - Conflict: Qwen's own report puts Qwen-Image text near the top (LongText-EN 0.943); WeGenBench's OCR F1 puts first-version Qwen-Image text lowest (0.46). The benchmarks measure different things (long text vs spelling precision on 4,000 mixed prompts).
- OneIG-Bench (arXiv 2506.07977, Jun 2025), EN: Recraft V3 alignment 0.810, text 0.795, style 0.378, diversity 0.205. Recraft V3 has the best text edit distance at long prompts because of a "layout-first strategy" (it makes a layout, then puts text in). Style by category for Recraft V3: traditional 0.418, media 0.347, anime 0.332. Source: https://arxiv.org/html/2506.07977. Tag: [measured-independent]. Recraft V3 lineage only.

### Recraft (V4, V4.1)
- V4: release 17 Feb 2026. "Ground-up rebuild", "developed in close collaboration with designers", tuned for composition and "cohesive color". Native editable SVG in Vector and Vector Pro. No benchmarks, no architecture, no training data statement. Source: https://www.recraft.ai/blog/introducing-recraft-v4-design-taste-meets-image-generation (17 Feb 2026). Tag: [opinion] (maker).
- V4 at launch did not support style creation, prompt-based editing, image sets, artistic-level control. Source: https://www.recraft.ai/docs/recraft-models/recraft-V4. Tag: maker documentation.
- V4.1: release 14 May 2026. The main model "experiments with angle, light, and composition the way a good creative director would"; V4.1 Utility "focuses on flat lighting, front-facing composition, and simple scenes". The maker says short prompts are enough. Source: https://www.recraft.ai/blog/recraft-v4-1-more-beautiful-by-nature (14 May 2026). Tag: [opinion] (maker).
  - Meaning for this job: the maker itself says the main model adds its own composition choices. That is a risk for exact layout obedience; Utility is the maker's literal mode.
- API: `controls.colors` (an array of preferred colours) and `background_color` work on "All models"; `style` / `style_id` work on all models except V4.1 Flash. Source: https://www.recraft.ai/docs/api-reference/endpoints. Tag: maker documentation. No source measures how exactly Recraft obeys this palette control.
- No arXiv paper or independent benchmark with Recraft V4 or V4.1 was found (search 30 Sep 2026). No SVG benchmark paper found tests Recraft (SVG-Score, arXiv 2609.03806, does not include it).

### IMG.LY GenAI Benchmarks (lower tier, but a published method)
- Method: suite pilot-0, method pilot-1, 23 models, 37 prompts, 2,550 generations, scores computed 14 Sep 2026. Same prompt for all models, default parameters, 3 seeds or samples. Colour accuracy is measured from pixels: CIEDE2000 distance between the requested hexes and the dominant output swatches (5 = under 2, 4 = under 5, 3 = under 10, 2 = under 20). Composition = a Claude VLM checks that the requested negative space exists and is clean. Prompt adherence = VLM checklist. The blind expert panel is still "pending". Source: https://img.ly/ai-benchmarks/methodology.md. Tag: [systematic-practitioner]. Cautions: colour and composition rest on only 9 runs per model; the judge is a VLM; IMG.LY sells a gateway whose default route is FLUX.2 (a conflict of interest).
- Scores (colour accuracy / composition-negative-space / prompt adherence / text, each out of 5; n = 9 / 9 / 111 / 24):
  - GPT Image 2: 4.1 / 4.2 / 4.9 / 5.0 (best colour in the field).
  - Nano Banana Pro: 3.7 / 3.6 / 4.6 / 5.0.
  - Seedream 4.5: 2.9 / 4.2 / 4.4 / 4.9.
  - Grok Imagine Image 2.0: 2.9 / 4.7 / 4.9 / 5.0. It painted a checkerboard instead of alpha in 9 of 9 transparency tries.
  - Recraft V4.1 (raster): 2.9 / 4.3 / 4.7 / 5.0. Alpha channel present, but 47 % of pixels come back partly transparent. The vector endpoint is not tested.
  - FLUX.2 (base): 2.8 / 4.2 / 4.4 / 4.9. FLUX.2 [pro]: 2.3 / 4.4 / 4.5 / 5.0 (colour 18th of 23).
  - Ideogram 3.0: 2.8 / 4.0 / 3.9 / 4.7 (text 20th of 23; "reputation-versus-measurement" result). Ideogram 4.0 not yet in the run.
  - Qwen Image 3.0: 2.6 / 3.9 / 4.7 / 5.0; slowest endpoint (141 s).
  - Qwen-Image (first version): 2.0 / 4.7 / 3.9 / 4.8; worst duotone brand-colour result (0.67 of 5 on that prompt).
  - Recraft V3: 1.9 / 3.0 / 3.3 / 4.0 (22nd of 23 on colour, composition and adherence).
  - Z-Image Turbo, FLUX.2 Flex, FLUX.2 Max, Midjourney: not in the run.
  Sources: https://img.ly/ai-benchmarks/models/<slug>.md for slugs gpt-image-2, nano-banana-pro, seedream-4-5, grok-imagine-image-2, recraft-v4-1, flux-2, flux-2-pro, ideogram-v3, qwen-image-3, qwen-image, recraft-v3 (read 30 Sep 2026). Tag: [systematic-practitioner].
- Date conflict: IMG.LY calls Qwen Image 3.0 "Alibaba's September release"; unite.ai reports the chat launch on 21 Jul 2026. The API may have come later. Not resolved.

- IMG.LY per-prompt results closest to the brand-art jobs (mean of 3 samples each; VLM adherence and pixel colour, out of 5). Tag: [systematic-practitioner]; n = 3 per model per prompt, so read as a hint only.
  - "Flat illustration ... exactly two brand colors #FF3B30 and #1D1D1F on pure white" (https://img.ly/ai-benchmarks/prompts/b01-two-color.md): colour Grok 2.0 4.00, Qwen Image 3.0 4.00, Recraft V4.1 3.33, FLUX.2 [pro] 3.33, FLUX.2 3.33, Ideogram 3.0 4.00; GPT Image 2.5 Sunburst, Nano Banana Pro, Seedream 5.0 Pro 5.00. Adherence Recraft V4.1 and Grok 5.00; FLUX.2 3.80; Recraft V3 2.50.
  - "Friendly fox mascot logo ... flat vector style, three colors maximum, thick clean outlines, centered emblem" (https://img.ly/ai-benchmarks/prompts/l02-mascot.md): adherence Qwen Image 3.0 4.73, Recraft V4.1 4.47, Grok 2.0 4.47, FLUX.2 [pro] 3.90, FLUX.2 3.90, Ideogram 3.0 3.30; GPT Image 2.5 5.00, Nano Banana Pro 3.60. Raster endpoints only; Recraft vector mode not tested.
  - "Set of six flat line icons ... uniform 2px stroke, single accent color, 3x2 grid" (a set-consistency test; https://img.ly/ai-benchmarks/prompts/l01-icon-set.md): Recraft V4.1, Qwen Image 3.0, Grok 2.0 all 5.00; FLUX.2 [pro] 4.33; FLUX.2 4.00; Ideogram 3.0 3.00; Recraft V3 1.33.

### Editing from a reference, and keeping one subject the same
- EdiVal-Agent (UT Austin, UCLA, Microsoft, Lambda; arXiv 2509.13399 v3, ICLR 2026): 16 editing models, three edit turns, object-level automatic scoring. FLUX.2-max rank 4: instruction following 75.55 / 55.27 / 39.36 over turns 1-3, content consistency 92.91 / 88.30 / 85.78; best of the flow-matching models. Seedream 4.0 rank 1 (IF 75.93 / 55.58 / 41.59, CC 92.51 / 88.03 / 85.86); GPT-Image-1.5 rank 2; Nano Banana 2 rank 3. Qwen-Image-Edit (first version) rank 9: IF 72.90 / 44.06 / 22.55, "degrades more rapidly over subsequent turns" (exposure bias). Source: https://arxiv.org/html/2509.13399. Tag: [measured-independent].
- MultiBanana (arXiv 2511.22989, Nov 2025): multi-reference generation. Qwen-Image-Edit-2509 scores 3.699/10 with two references and 2.256/10 with 3+ objects; open models "tend to omit some reference subjects altogether"; background replacement 2.033/10, lowest tested. Cross-domain references (photo + anime) lower every model. Nano Banana best on single-reference consistency. Source: https://arxiv.org/html/2511.22989. Tag: [measured-independent]. Qwen-Image-Edit-2509 lineage only.
- VIF-Bench (Univ. of Tokyo, arXiv 2609.37709, 29 Sep 2026): 1,241 multi-reference tasks. Overall Nano Banana Pro 6.96, GPT-Image-1.5 7.60, Qwen-Image-Edit-2511 4.94, FLUX.1 Kontext 4.61. Qwen-Image-Edit-2511 visual-instruction adherence 2.50 against Nano Banana Pro 5.67. FLUX.2, Grok, Z-Image, Seedream not tested. Source: https://arxiv.org/html/2609.37709. Tag: [measured-independent].
- Persistent identity (Phota Labs, arXiv 2609.04151, Sep 2026): identity similarity falls as edits accumulate for most methods (GPT-Image-2 about 0.71 to 0.53 over four edits). FLUX.2 and Ideogram 4 are tested only with a LoRA; faces only. The authors say identity beyond the face (animals, mascots) is future work. Source: https://arxiv.org/html/2609.04151. Tag: [measured-independent]; the authors sell the method they test.
- Gap: no rigorous source measures how well any of the six models keeps a non-human mascot (for example a manta ray) the same across a series.

### Layout and structured design (posters, slides, web pages)
- BizGenEval (SJTU, Microsoft and others; arXiv 2603.25732, 26 Mar 2026): 400 prompts over slides, web pages, charts, posters, scientific figures; 8,000 human-checked checklist questions; Gemini-3-Flash judge with 90.88 % agreement with humans. Scores hard / easy, columns Layout, Attribute, Text, Knowledge, Average:
  - Nano-Banana-Pro 72.2/91.2, 65.6/92.2, 86.4/95.0, 82.6/96.2, 76.7/93.7.
  - Seedream-5.0 67.6/89.0, 42.4/77.2, 43.4/75.6, 41.8/75.2, 48.8/79.2.
  - GPT-Image-1.5 51.6/84.8, 25.8/75.2, 40.4/82.8, 26.0/83.6, 35.9/81.6.
  - Z-Image average 8.2/43.8, layout 26.8/69.2. Z-Image-Turbo 11.0/60.6, 1.2/35.0, 1.2/29.8, 0.2/4.0, 3.4/32.4.
  - FLUX.2-dev 17.2/67.8, 1.2/49.2, 1.0/43.0, 0.0/8.2, 4.9/42.0.
  - Qwen-Image-2512 22.2/70.6, 1.2/47.8, 1.8/39.2, 0.0/6.4, 6.3/41.0. Qwen-Image 10.4/51.2, ..., average 2.8/23.8.
  - FLUX.2-Pro 6.1/36.2, 0.0/22.9, 0.0/13.7, 0.2/11.7, 1.6/21.1 (lower than FLUX.2-dev; the paper does not explain this; it used each API's default settings).
  - Findings: "stylistic generation does not imply precise composition"; "natural image competence does not transfer to commercial documents"; all open models score near zero on hard text and knowledge questions. Ideogram, Recraft, Grok not tested.
  Source: https://arxiv.org/html/2603.25732 (numbers checked against the raw HTML table). Tag: [measured-independent].
- 7Bench (Izzo et al., arXiv 2508.12919) is an independent layout-in-boxes benchmark. Ideogram ran it on its own model (0.69 mIoU, above "all closed-source models tested"). No independent run of Ideogram 4.0 on 7Bench was found. Tag: [measured-self-reported].

### Style range, variety and artefacts
- OneIG-Bench EN, as reported in the Z-Image report (Table 7; arXiv 2511.22699v1): style / diversity: GPT Image 1 0.462 / 0.151; Qwen-Image 0.418 / 0.197; Seedream 3.0 0.413 / 0.277; Z-Image 0.387 / 0.194; Recraft V3 0.378 / 0.205; Z-Image-Turbo 0.368 / 0.139 (lowest diversity of the top ten); text: Z-Image-Turbo 0.994, Z-Image 0.987, Qwen-Image 0.891. Source: https://arxiv.org/html/2511.22699v1 (checked in raw HTML). Tag: [measured-self-reported] for Z-Image rows; other rows copied from the OneIG paper.
- Diversity collapse in distilled and RL-tuned flow models is a documented general effect: "diversity collapse in the generated samples is due to the collapse of the internal MMDiT features" (FLUX.1-dev, FLUX.2-Klein-4B, Qwen-Image measured). Source: https://arxiv.org/html/2606.27371 (Jun 2026). Tag: [measured-independent]. Z-Image-Turbo is not in that test.
- RealGen (arXiv 2512.00473, Dec 2025), photorealism by forensic detector: GPT-Image-1 75.63, Seedream 3.0 63.47, Qwen-Image 57.47, FLUX-Pro (FLUX.1 line) 57.45. Artefacts named: Qwen-Image "often generates overly smooth skin, exhibiting a typical AI artifact"; FLUX-dev "excessive oiliness and unnatural highlights"; GPT-Image-1 "AI plastic" feel and a yellow-green cast. Source: https://arxiv.org/html/2512.00473v1. Tag: [measured-independent]. First-version Qwen-Image and FLUX.1 lineage only; FLUX.2 and later Qwen not tested.
- Animal anatomy: no per-model animal score is published, and no source tests a manta ray or other sea animals.

### Ideogram 4.0: independent check of text and prompt format
- Transformer Lab (not Ideogram; arXiv 2606.12280 v2, 12 Jun 2026): 63 prompts with machine-checkable text, PP-OCR. FP8 open-weight Ideogram 4.0 reached 54 % OCR exact match with JSON captions and "≈0%" with raw natural-language prompts. "Text legibility is a property of how the model is prompted." n = 63, so the confidence band is wide. Source: https://arxiv.org/html/2606.12280. Tag: [measured-independent].
  - Meaning: Ideogram 4.0 needs its JSON caption format. A route that sends a plain sentence (and does not convert it) will lose most of the text and layout strength. The repo commit 38c1688 records that Higgsfield passes an Ideogram 4.0 JSON caption through.
  - The gap between 54 % exact match (independent) and the maker's 0.97 OCR accuracy (X-Omni) is partly a metric difference (whole-string exact match vs character accuracy). Not resolved.

### Qwen line: maker admissions about earlier weaknesses
- Qwen-Image-2512 (Dec 2025) model card: it "significantly reduces the 'AI-generated' look ... especially for human subjects" and gives "more detailed rendering of landscapes, animal fur". Source: https://huggingface.co/Qwen/Qwen-Image-2512. Tag: [opinion] (maker).

### Grok Imagine (xAI)
- Grok Imagine Image 2.0: release 7 Aug 2026. Maker claims: follows instructions "down to the details", "plans typography and layout the way a designer would", keeps consistency across generations and edits, region edits, up to 5 reference images, "world-building" with a consistent style across character, location and prop. Arena claim: second in text-to-image and image edit on 7 Aug 2026. No architecture, no training data, no technical report, no limitations. Source: https://x.ai/news/grok-imagine-image-2 (7 Aug 2026). Tag: [opinion] (maker).
- Lineage: Aurora (9 Dec 2024) is "an autoregressive mixture-of-experts network trained to predict the next token from interleaved text and image data", trained "on billions of examples from the internet"; maker says it "excels at photorealistic rendering". Source: https://x.ai/news/grok-image-generation-release. Tag: [opinion] (maker). Whether Imagine Image 2.0 still uses the Aurora design is not stated anywhere found: unknown.
- No arXiv paper that measures Grok Imagine was found (30 Sep 2026). A risk paper (arXiv 2604.24197) lists its features from xAI documents only and says its scores are "not empirical benchmark results".

### Prompt rewriting by route (maker documents)
- Ideogram 4.0 live service: Magic Prompt is always AUTO. "Plain text gets expanded. A valid, well-formed JSON prompt passes through as-is." Hex codes must be uppercase #RRGGBB; up to 16 per image, 5 per element; a full palette with background and shadow values "outperforms" a single brand colour. Bounding boxes "land inside their declared box consistently"; keep to five or fewer elements. Text accuracy 97 % for large English, about 90 % for small English; weak on small non-English text and full paragraphs. Source: https://ideogram.ai/blog/ideogram-4-json-prompting/ (18 Jun 2026). Tag: [measured-self-reported] for the percentages; the rest is maker guidance.
- Z-Image: whether a given API route applies the maker's prompt enhancer: unknown.
- FLUX.2 [flex] exposes steps and guidance and "excels at text and fine details" (maker, https://bfl.ai/blog/flux-2).
- Grok Imagine and Qwen Image 3: no maker statement on prompt rewriting was found. Unknown.

---

## Per-model profiles

Key to short source names (full URLs are in the log above):
- BizGenEval = arXiv 2603.25732 (Mar 2026). EdiVal = arXiv 2509.13399 (ICLR 2026). ACBench = arXiv 2609.20816 (Sep 2026). WeGenBench = arXiv 2606.20100 (Jun 2026). QIB = Qwen-Image-Bench, arXiv 2605.28091 (May 2026). OneIG = arXiv 2506.07977. MEF = arXiv 2509.17907 (Sep 2025). Perle = arXiv 2608.14976 (Aug 2026). RealGen = arXiv 2512.00473 (Dec 2025). TLab = arXiv 2606.12280 (Jun 2026). MultiBanana = arXiv 2511.22989. VIF = arXiv 2609.37709. IMG.LY = img.ly/ai-benchmarks (scores of 14 Sep 2026).

### 1. Grok Imagine Image 2.0 (xAI)
Best at:
- Prompt adherence and composition with clear empty space. IMG.LY adherence 4.9/5 (3rd of 23), composition 4.7/5 (5th); flat two-colour, mascot and icon-set prompts all 4.47-5.00. IMG.LY, Sep 2026, [systematic-practitioner].
- Short text in the image: 5.0/5. IMG.LY, [systematic-practitioner]. (Almost every current model also scores 5.0 on this.)
- Maker claims: layout "the way a designer would", consistency across edits, 5-image reference, style "world-building". x.ai, 7 Aug 2026, [opinion].
Worst at:
- Exact hex colour: 2.9/5 (mean CIEDE2000 about 10-20). IMG.LY, [systematic-practitioner].
- Transparency: paints a checkerboard; 0 of 9 real alpha channels. IMG.LY, [systematic-practitioner].
- Designer preference: Elo 990, below Ideogram 4.0 (1062), Nano Banana 2 (1004), GPT Image 2 (1141). Ideogram blog, 3 Jun 2026, run by a competitor.
Evidence strength: WEAK. No technical report, no paper, no benchmark paper includes it. Architecture of 2.0 unknown (Aurora lineage is autoregressive MoE; not confirmed for 2.0).

### 2. Qwen Image 3 (Alibaba), with Qwen-Image / 2512 / 2.0 lineage
Best at:
- Text-heavy design images (posters, slides, infographics). Lineage data: 27 % design images and 5 % synthetic text in training; LongText-Bench EN 0.943; OneIG text 0.891. Qwen-Image report, Aug 2025, [measured-self-reported]. Qwen Image 3 claims 10 px legible text and 4,500-token prompts. Qwen blog via unite.ai, Jul 2026, [opinion].
- Prompt adherence (Qwen Image 3): IMG.LY 4.7/5 (9th of 23); mascot prompt 4.73 and icon-set 5.00, both above FLUX.2 and Ideogram 3.0. IMG.LY, [systematic-practitioner].
- Qwen Image 2.0 Pro overall 57.84 on QIB, above Seedream 5.0 and FLUX 2 Max/Pro, below GPT Image 2 and Nano Banana Pro. QIB, May 2026, [measured-self-reported] (Qwen's own benchmark).
Worst at:
- Exact hex colour, whole line. ACBench: Qwen-Image 25.21/100, lowest open model measured. [measured-independent]. IMG.LY: Qwen Image 3 2.6/5, Qwen-Image 2.0/5 (worst duotone result). [systematic-practitioner].
- Composition / negative space (Qwen Image 3): 3.9/5, below Grok, Recraft V4.1, FLUX.2. IMG.LY, [systematic-practitioner].
- Dense business layouts and multi-constraint design (lineage): Qwen-Image-2512 average 6.3/41.0 against Nano Banana Pro 76.7/93.7. BizGenEval, [measured-independent].
- Plastic look: first version "overly smooth skin, a typical AI artifact". RealGen, [measured-independent]. Maker says 2512 reduced the "AI-generated look". [opinion].
- Editing across several turns and several references (lineage): Qwen-Image-Edit falls from IF 72.90 to 22.55 over three turns (EdiVal, [measured-independent]); Qwen-Image-Edit-2509 omits reference subjects (MultiBanana, [measured-independent]); 2511 adherence 2.50 against Nano Banana Pro 5.67 (VIF, [measured-independent]).
- Narrow style range and low variety (lineage): OneIG style 0.418 is good, but diversity 0.197. [measured-self-reported].
- Speed: Qwen Image 3 slowest endpoint measured, 141 s. IMG.LY.
Evidence strength: MEDIUM for the lineage, WEAK for Qwen Image 3 itself (no report, no weights, no benchmark scores from the maker; only IMG.LY measures it).

### 3. Ideogram 4.0 (and 3.0)
Best at:
- Layout by bounding box and in-image text, when prompted in JSON. 7Bench 0.69 mIoU; X-Omni OCR 0.97; designer Elo 1062 (2nd, first open-weight). Ideogram blog, 3 Jun 2026, [measured-self-reported].
- Palette as a first-class input: up to 16 uppercase hex codes per image. Maker guide, Jun 2026. Accuracy not measured by anyone: GAP.
Worst at:
- Plain-sentence prompts: text exact match 54 % with JSON, "≈0%" with raw natural language (open FP8 weights, 63 prompts). TLab, Jun 2026, [measured-independent]. The live API expands plain text to JSON (Magic Prompt AUTO), which should reduce this risk on the hosted route.
- Small non-English text and full paragraphs; numbers in labels. Maker guide, [measured-self-reported].
- 3.0 lineage: lowest aesthetics of the MEF set (3.07/5) though good prompt following (3.91) — [measured-independent]; 65.7/100 on hard compositional prompts against FLUX.2 82.3 and Nano Banana Pro 84.8 — Perle, [measured-independent], 48 prompts; IMG.LY: 3.0 text 4.7/5 (20th of 23), adherence 3.9, colour 2.8, mascot 3.30, icon set 3.00 — [systematic-practitioner].
Evidence strength: MEDIUM-WEAK for 4.0. Strong maker numbers with a published method, one small independent check (TLab). No independent layout, palette, style or anatomy test of 4.0. 3.0 lineage is well measured but is a different model.

### 4. Recraft V4.1 (Pro, standard, Vector), with V3/V4 lineage
Best at:
- Design-ready raster output: IMG.LY blended 3.63/5 (3rd of 23); adherence 4.7/5; text 5.0/5; composition 4.3/5; flat two-colour adherence 5.00; icon set 5.00; mascot 4.47. [systematic-practitioner].
- Native editable SVG (Vector, Vector Pro): maker says the only model that makes structured-layer SVG. Recraft, Feb/May 2026, [opinion]. No benchmark paper tests it: GAP.
- Palette as an API input: `controls.colors` on all models; saved styles (`style_id`) on all but V4.1 Flash. Recraft API docs. Accuracy not measured: GAP.
- Maker says V4 was tuned "in close collaboration with designers" for composition and "cohesive color". [opinion]. No architecture or data statement.
Worst at:
- Exact hex colour when given in the prompt text: 2.9/5. IMG.LY, [systematic-practitioner]. (IMG.LY did not use `controls.colors`; the prompt carried the hexes.)
- Transparency: alpha exists but 47 % of pixels are partly transparent. IMG.LY.
- Literal composition: the main V4.1 model "experiments with angle, light, and composition"; the maker points literal work to V4.1 Utility. Recraft, 14 May 2026, [opinion].
- V3 lineage: 22nd of 23 on colour, composition and adherence at IMG.LY; OneIG style 0.378 and diversity 0.205; MEF Elo 1021. Treat V3 evidence as history only; V4 is a "ground-up rebuild".
Evidence strength: WEAK for V4/V4.1 (no paper, no report; one practitioner suite).

### 5. Z-Image Turbo (Alibaba Tongyi-MAI)
Best at:
- Short in-image text for its size: OneIG text 0.994 (EN), CVTG-2K 0.8585. Z-Image report, Nov 2025, [measured-self-reported]. WeGenBench text F1 0.73, above FLUX.2-dev 0.58, Qwen-Image 0.46, GPT-Image-2 0.56, below Seedream-4.5 0.79. [measured-independent].
- Photoreal images at 8 steps; Alibaba AI Arena Elo 1025, 4th. [measured-self-reported].
- Hex colour, relative to Qwen: ACBench 33.56 against Qwen-Image 25.21 and FLUX.2-dev 51.70. [measured-independent].
Worst at:
- Variety and style reach: OneIG diversity 0.139 (lowest of the top ten), style 0.368. [measured-self-reported]. Few-step distillation causes this kind of collapse in general (arXiv 2606.27371, [measured-independent], Z-Image not in that test).
- Knowledge, intent, complex reasoning: maker says the 6B model needs a VLM prompt enhancer. [measured-self-reported].
- Dense design layouts: BizGenEval Turbo 3.4/32.4 average, layout 11.0/60.6 (the full Z-Image does better, 26.8/69.2). [measured-independent].
- Aesthetics: WeGenBench Z-Image 2.44/5, lowest of the open models listed here. [measured-independent].
- No source tests flat vector, painterly styles, mascots or animals for Z-Image. GAP.
Evidence strength: MEDIUM. A full technical report plus two independent benchmark papers; nothing on illustration styles.

### 6. FLUX.2 Pro / Flex / Max (Black Forest Labs), with FLUX.1 lineage
Best at:
- Editing and keeping an image steady over several edits: FLUX.2-max EdiVal rank 4 of 16, consistency 92.91 to 85.78 over three turns, level with Seedream 4.0 and Nano Banana 2. [measured-independent].
- Hex colour, among the open models measured: FLUX.2-dev ACBench 51.70 (best baseline); edit 68.87. [measured-independent]. The maker guide says hex works "best when clearly associated with specific objects". [opinion].
- Hard compositional prompts: FLUX.2 82.3/100, close to Nano Banana Pro 84.8. Perle, 48 prompts, [measured-independent].
- Composition with empty space: IMG.LY FLUX.2 4.2, [pro] 4.4 (7th). [systematic-practitioner].
- Multi-reference up to 10 images (8 at 1 MP on [pro] API); Mistral-3 24B VLM encoder. Maker, Nov 2025, [opinion].
Worst at:
- Exact hex colour in practice: IMG.LY [pro] 2.3/5 (18th of 23), base 2.8. [systematic-practitioner]. ACBench best open score is still only about half of the maximum.
- Dense business layouts and text: FLUX.2-Pro BizGenEval 1.6/21.1, below FLUX.2-dev 4.9/42.0 (unexplained; default API settings). [measured-independent]. Spelling: FLUX.2-dev text F1 0.58, "struggle[s] with character-level spelling". WeGenBench, [measured-independent].
- Real-world fidelity and creative generation: FLUX 2 Max 49.35 / 56.50, lowest of the frontier group on QIB. [measured-independent] (a competitor's benchmark).
- Animals and anatomy: part of the all-model "systemic ceiling" on QIB; no per-model number. [measured-independent].
- FLUX.1 lineage artefacts: "excessive oiliness and unnatural highlights" (RealGen, [measured-independent]); hex tokenisation failure (NumColor, [measured-independent]). Not measured for FLUX.2.
- No negative prompts. Maker guide.
Evidence strength: MEDIUM-STRONG. The most independently measured model in this list, but no BFL technical report, and Flex is never measured apart from the family.

---

## Cross-model view by brand-art job

Scope: only my six models. "Favours" means the rigorous evidence points that way; it does not mean the evidence is strong.

1. Hero image with empty space for a headline.
- Evidence favours: Ideogram 4.0 (bounding boxes; 7Bench 0.69 mIoU, maker-measured; must go through JSON or Magic Prompt) and Grok 2.0 (IMG.LY negative-space 4.7). Then Recraft V4.1 (4.3; use Utility for a literal layout), FLUX.2 [pro] (4.4). Qwen Image 3 is weaker (3.9).
- Silent: no peer-reviewed test measures "leave a clean area for a headline". IMG.LY's VLM check (n = 9 per model) is the only direct measure. BizGenEval measures dense layouts, not one clean area.

2. Page background.
- Evidence is silent. No source tests low-contrast, texture-like or tileable backgrounds, seams or banding for any of the six. IMG.LY has a gradient-banding prompt, but only Seedream 4.5's win on it is reported.

3. Mascot or spot illustration (manta ray; anatomy matters).
- Flat mascot style: IMG.LY fox-mascot prompt favours Qwen Image 3 (4.73), Recraft V4.1 (4.47), Grok 2.0 (4.47) over FLUX.2 (3.90) and Ideogram 3.0 (3.30). n = 3 each, [systematic-practitioner].
- Anatomy: every model tested has an animal "ceiling" (QIB best 42.6 of 100). No source gives a per-model animal or sea-animal score for any of the six. Silent. The founder's own tests stay the best evidence for a manta ray.

4. Matching set in one style.
- Set consistency of flat icons: IMG.LY favours Recraft V4.1, Qwen Image 3, Grok 2.0 (all 5.00) over FLUX.2 [pro] (4.33) and Ideogram 3.0 (3.00). n = 3 each.
- Holding a subject through edits: FLUX.2-max is the only one of the six with a strong independent result (EdiVal). The Qwen edit lineage drifts (EdiVal, MultiBanana, VIF).
- Saved style: Recraft `style_id` and Ideogram style references exist; no source measures how well they hold a style across a set.
- Silent: no benchmark of T2IS type (sets of images in one style) includes any of the six.

5. Palette obedience (hex).
- No model in the list is good at exact hex from prompt text. Measured order (open models, ACBench): FLUX.2-dev 51.70 > Z-Image-Turbo 33.56 > Qwen-Image 25.21. IMG.LY: Grok 2.9, Recraft V4.1 2.9, FLUX.2 2.8, Ideogram 3.0 2.8, Qwen Image 3 2.6, FLUX.2 [pro] 2.3; GPT Image 2 (4.1) and Nano Banana Pro (3.7) do better.
- Two models take the palette as a structured input rather than prompt text: Ideogram 4.0 (JSON palette) and Recraft (`controls.colors`). This design avoids the tokenisation cause found in NumColor. No source measures either. This is the largest useful gap: a small in-house test of these two inputs would settle it.

Comparisons with the outside models (rigorous sources only): Nano Banana Pro leads dense layout, text and attribute binding (BizGenEval) and multi-reference instruction (VIF); GPT Image 2 leads QIB overall, animals, and IMG.LY colour; Seedream 4.0 leads multi-turn editing (EdiVal) and Seedream 4.5 leads WeGenBench text F1. Midjourney: the only rigorous source is MEF (V6.1, Sep 2025): best aesthetics of its tier but weak prompt following and structure. No rigorous source covers Midjourney V7 or later.

---

## Bound
- Read in full or near full (tables checked): Qwen-Image report (2508.02324); Z-Image report (2511.22699, Table 7 checked in raw HTML); BizGenEval (2603.25732, table checked in raw HTML); IMG.LY methodology and 11 model pages and 3 prompt pages.
- Read in part (abstract, main tables, key sections through a fetch summariser): Qwen-Image-2.0 report, Qwen-Image-Bench, WeGenBench, ACBench/Paint-Anything, EdiVal-Agent, MultiBanana, VIF-Bench, persistent-identity paper, MEF, OneIG, RealGen, Perle, TLab quantization paper, diversity-collapse paper, GenColorBench, NumColor, TextPecker, FEPBench abstract; maker pages for Ideogram 4.0 (blog, model card, JSON guide), Recraft V4 and V4.1 (blog, docs, API), FLUX.2 (blog, prompting guide), Grok Imagine 2.0 and Aurora posts, Qwen-Image-2512 card.
- Could not reach: WACV 2026 workshop paper "We Still See Broken Limbs" (HTTP 403); Artificial Analysis per-style categories (page gives no category data; see [image-model-benchmarks.md](https://github.com/lucmoseley/design-vault/blob/b4a0b43d5/docs/research/image-model-benchmarks.md)).
- Not searched: LMArena and Artificial Analysis rankings (the other agent's scope); YouTube and blog reviews (excluded by the source bar).

