# Image model profiles B: qualitative strengths and weaknesses

Ticket: #51. Date: 30 Sep 2026.

Tags:
- [measured-independent]: a third party measured it with a stated method.
- [measured-self-reported]: the maker measured it.
- [systematic-practitioner]: a practitioner compared many prompts with a stated method. Lower tier.
- [maker-claim]: the maker says it. No measurement.
- [opinion]: a person says it. No measurement.

## Findings log

### F1. GPT Image 2.5 system card (OpenAI, 8 Sep 2026)
- Source: https://deploymentsafety.openai.com/chatgpt-images-2-5 (8 Sep 2026).
- The card gives two variants: GPT-Image-2.5-Sunburst and GPT-Image-2.5-Flare. It does not tell the architecture difference. [maker-claim]
- The card says: "more consistent results when editing images", "improves infographic accuracy and layout", change "setting, style, or composition while retaining more of the details". [maker-claim]
- The card has only safety numbers. It has no image-quality measurement. (Sunburst 1.09% unsafe presented, Flare 1.41%, 2.0 baseline 1.64%.) [measured-self-reported, safety only]
- Maker page https://openai.com/index/introducing-chatgpt-images-2-5/ returned HTTP 403. Secondary summaries (9to5mac 8 Sep 2026; fal.ai model pages) say: up to 4K, up to 16 reference images, Flare = 2 to 4 times faster than GPT Image 2 ("default choice"), Sunburst = "tighter control across edits", for "production-ready campaign creative". [maker-claim, reported second-hand]

### F2. Seedream 4.0 / 4.5 technical report (ByteDance Seed, arXiv 2509.20427, v1 18 Sep 2025, v3 adds 4.5)
- Source: https://arxiv.org/abs/2509.20427
- Architecture: diffusion transformer (DiT) with a high-compression VAE. Fewer image tokens. More than 10x faster than Seedream 3.0. Native 1K to 4K. [maker-claim]
- Data: "billions of text-image pairs"; a special knowledge pipeline (textbook PDFs, formulas). This explains the strong dense-text and chart output. [maker-claim]
- MagicBench 4.0 (human evaluation, 325 T2I prompts): Seedream 4.0 "substantially outperforms competing models in visual aesthetics". The paper gives radar charts only, not numbers. [measured-self-reported]
- DreamEval (1,600 prompts, 128 sub-tasks): "Seedream 4.0 and GPT-4o outperform other models in instruction adherence"; Seedream 4.0 "exhibits greater variability: it has a slightly lower average score, but its 'best-of-4' results are better". Performance "drops at the Hard level, especially in single-image editing". [measured-self-reported]
- Paper's remarks on rivals: "GPT-Image-1 achieves the highest accuracy in instruction following, but ranks lowest in consistency" (editing). "Gemini-2.5 excels at preservation, but shows limited capability in instruction following ... struggles with text editing, especially in Chinese." [measured-self-reported, by a competitor]
- Multi-image editing: Seedream 4.0 leads by "almost 20% in the GSB metric"; "more stable and coherent structures" with 10+ reference images. [measured-self-reported]
- Seedream 4.5 (added section): larger model and more data; better "text-image alignment, structural fidelity, editing consistency, and fine-grained text rendering"; "preserving identity-relevant features" from references; "stronger typographic rendering ... for dense text layouts such as posters". Shown in a figure, no table. [measured-self-reported]

### F3. UniGenBench++ (arXiv 2510.18701 v2, 24 Feb 2026)
- Source: https://arxiv.org/abs/2510.18701. Judge: Gemini-2.5-Pro (a VLM judge, not humans). English short prompts.
- Scores (Style / Attribute / Layout / Text):
  - Nano Banana Pro: 99.30 / 91.95 / 93.28 / 95.65
  - Nano Banana: 98.59 / 87.99 / 91.42 / 73.28
  - GPT-4o: 98.98 / 94.01 / 91.35 / 89.24
  - GPT Image 1.5 (the fetch tool named it "GPT-4o-1.5"; not verified): 99.19 / 96.33 / 94.56 / 97.39
  - Seedream 4.0: 98.80 / 88.57 / 90.67 / 93.97
  - Seedream 4.5: 99.20 / 91.03 / 92.54 / 91.67
  - FLUX.2 dev: 96.60 / 87.39 / 89.55 / 85.34
  - Qwen-Image: 94.70 / 87.93 / 86.57 / 72.13
  - Recraft: 87.20 / 68.16 / 57.84 / 61.78
- Midjourney, Ideogram, Grok are not in the table. [measured-independent]
- Caution: "Style" is near 99 for all top models. It does not separate them. "Style" here means "the named style is present", not quality of the style. The judge is a Google model and it scores a Google model. [opinion, this author]

### F4. Qwen-Image-Bench (Alibaba Qwen team, arXiv 2605.28091, May 2026)
- Source: https://arxiv.org/abs/2605.28091. Read in full (text extract).
- Method: 1,000 bilingual prompts, 56 facets, made with professional artists. A judge model (Q-Judger, Qwen3.6-27B) is trained on more than 130,000 labels from 80 art-academy annotators (blind, three reviews). Rank agreement with human experts: Spearman rho = 0.92 (Chinese), 0.90 (English). 18 models, all through official APIs. Midjourney, Ideogram, Recraft, Grok are NOT in the test. [measured-independent; the maker of the benchmark also makes Qwen Image, which is a rival]
- Overall (Chinese prompts): GPT Image 2 64.69; Nano Banana 2.0 59.82; GPT Image 1.5 59.65; Nano Banana Pro 59.45; Qwen Image 2.0 Pro 57.84; Seedream 5.0 57.22; Seedream 4.5 56.78; Seedream 4.0 56.21; FLUX 2 Max 55.33; FLUX 2 Pro 54.57; GPT Image 1 54.07. English: GPT Image 2 65.23; GPT Image 1.5 60.42; Nano Banana 2.0 59.59; Nano Banana Pro 59.33. [measured-independent]
- "GPT Image 2 achieves the highest score on all five L1 pillars simultaneously, forming a dominant profile with no discernible weakness". [measured-independent]
- "Nano Banana Pro climbs to second on Quality, demonstrating superior artifact suppression and physical-logic handling." [measured-independent]
- Seedream trade-off: "Seedream 4.5 scores higher than 5.0 on Quality and Aesthetics, while 5.0 surges ahead on Creative Generation by over 4 points". On Aesthetics the Seedream 4.0/4.5/5.0 models are "near-identical". [measured-independent]
- ANIMALS AND ANATOMY ARE A CEILING FOR ALL MODELS. "Anatomical Fidelity (best 20.9), Physical Logic (best 31.9), Objects (best 41.9), Animals (best 42.6), and Contact Interaction (best 43.3)". The paper says: "current models excel at reproducing visual surface patterns but remain weak at tasks requiring implicit world knowledge". [measured-independent]
- Per-model facet scores that I read from the Fig. 9 and Fig. 10 heatmaps (Chinese prompts). I matched rows to labels by count. Three check values agree with the paper text (Anatomy 20.91, Game Design 91.76, Contact 43.32). Order: GPT Image 2 / Nano Banana 2 / GPT Image 1.5 / Nano Banana Pro / Seedream 5.0 / Seedream 4.5 / FLUX 2 Max:
  - Animals: 42.64 / 26.78 / 32.84 / 31.05 / 22.41 / 37.27 / 28.55. (Seedream 4.0 = 37.57.) Seedream 4.x is second after GPT Image 2. Nano Banana Pro and Seedream 5.0 are weaker.
  - Anatomical fidelity: 20.91 / 10.02 / 13.11 / 11.94 / 10.77 / 16.59 / 8.21.
  - Style Control: 75.85 / 68.00 / 66.12 / 66.59 / 59.07 / 58.71 / 56.91.
  - Art Design: 84.34 / 80.37 / 80.54 / 80.70 / 74.52 / 77.49 / 76.43. Paper: "artistic style transfer is relatively mature".
  - Color Harmony: 75.36 / 71.79 / 70.27 / 69.72 / 68.82 / 68.55 / 66.28.
  - Color (obeys a stated colour attribute): 69.81 / 69.19 / 69.00 / 69.39 / 68.44 / 67.02 / 67.34 approx. Nearly flat. This is a colour NAME test, not a hex palette test.
  - Composition (aesthetic): 69.46 / 63.50 / 61.38 / 61.00 / 60.94 / 57.42 / 57.14.
  - 2D Space (layout): 66.55 / 60.96 / 61.67 / 61.52 / 61.64 / 57.76 / 57.15.
  - Graphic Design: 93.40 / 82.36 / 76.86 / 77.91 / 79.76 / 67.47 / 62.38.
  - Text Accuracy: 78.81 / 62.60 / 58.82 / 64.43 / 80.68 / 65.22 / 26.19. (Seedream 5.0 is highest here.)
  [measured-independent; my reading of a heatmap, so a small reading error is possible]

### F5. Swift-Image paper (arXiv 2608.20334, 20 Aug 2026) — editing results with these models as baselines
- Source: https://arxiv.org/abs/2608.20334. It repeats the Qwen-Image-Bench T2I table (same numbers as F4).
- Editing, five benchmarks averaged (GEdit, ImgEdit, REDEdit, CPI-General, CPI-Practical): GPT Image 2 4.61 (rank 1); Seedream 5 Pro 4.57 (2); Qwen Image 2.0 Pro 4.37; Nano Banana Pro 4.34 (6); Seedream 4.5 4.22 (9). [measured-independent, VLM-judged benchmarks]
- Reference-based (multi-image) editing, CPI sub-table overall: GPT Image 2 4.51; Seedream 5 Pro 4.50; Nano Banana Pro 4.27; Qwen Image 2.0 Pro 4.10; Seedream 4.5 4.06. "Ref-Stylize" (apply the style of a reference): GPT Image 2 4.75; Nano Banana Pro 4.48; Seedream 5 Pro 4.35; Seedream 4.5 4.10. [measured-independent]
- Knowledge-heavy T2I (Pi-ExpertVerse, the authors' own set): GPT Image 2 4.94; Seedream 5 Pro 4.87; Nano Banana Pro 4.78; Seedream 4.5 4.10. [measured-independent, authors' own benchmark]

### F6. Violin benchmark, "AI Obedience" (HIT Shenzhen, CityU HK, CUHK, McGill; arXiv 2603.00166 v2, May 2026)
- Source: https://arxiv.org/abs/2603.00166. Tables read.
- Test: exact pixel obedience. (1) Fill the image with one hex colour, or two to four hex blocks. (2) Draw a shape at an exact place and size. (3) Apply a mask. Metrics are pixel measurements (RGB distance, CIEDE2000, texture, edges). Lower = better. No judge model. [measured-independent]
- Pure hex colour (Var-1, colour-mean): GPT-Image-2 0.051; Seedream-5 0.049; Nano-Banana-2 0.053; FLUX.2 0.057; Qwen-Image 0.057. RGB distance to the target hex: 0.12 to 0.14 for ALL models. Thus no model hits an exact hex value. GPT-Image-2 gives the flattest fill (std-dev 0.006, edge 0.000), but the most high-frequency noise (0.031). [measured-independent]
- Shape at an exact place and size (mask-mean): GPT-Image-2 0.134; Seedream-5 0.207; Nano-Banana-2 0.282; FLUX.2 0.304. GPT-Image-2 is best on place (dist 0.033) and size (0.278). [measured-independent]
- Masking (shape-mean): GPT-Image-2 0.158; Seedream-5 0.280; Nano-Banana-2 0.366; FLUX.2 0.512. [measured-independent]
- The authors say Seedream-5.0 "consistently struggles with the deterministic constraints", "prioritizing learned 'aesthetic patterns' over precise user commands". On GPT-Image-2 they "observed relatively fewer obedience issues" (preliminary). [measured-independent, partly qualitative]
- Scope limit: the test uses Nano-Banana-2, not Nano Banana Pro. Seedream "5" is not the Lite variant by name. No Midjourney.
- Relevance: an exact-place test is the nearest rigorous proxy for "leave this area empty for a headline". [opinion, this author]

### F7. Hex-colour papers that do NOT test the closed models
- GenColorBench (Computer Vision Center Barcelona, arXiv 2510.20586): 9.8K prompts with hex and RGB. Tests open models only (FLUX, PixArt, SD). FLUX reaches only 13.82% at the coarsest level. https://arxiv.org/abs/2510.20586 [measured-independent, open models only]
- NumColor (arXiv 2603.13547, same group): says diffusion models "fail to interpret numerical colors such as hex codes". Open models only. [measured-independent]
- ACBench / Paint-Anything (arXiv 2609.20816, 20 Sep 2026): object-level hex fidelity; tests FLUX.2, Qwen-Image, Z-Image, SD only. No closed models. [measured-independent, open models only]
- Result: I found NO rigorous study that measures GPT Image 2/2.5, Nano Banana Pro, Seedream 4.5/5 Lite or Midjourney on a multi-colour hex PALETTE in an illustration. Violin (F6) is the only closed-model hex test, and it tests flat fills.

### F8. Seedream 5.0 Lite (ByteDance Seed blog, 13 Feb 2026)
- Source: https://seed.bytedance.com/en/blog/deeper-thinking-more-accurate-generation-introducing-seedream-5-0-lite
- "unified multimodal architecture"; multi-step reasoning; web search while it generates; style transfer from one image. No architecture detail. [maker-claim]
- Elo on ByteDance's own MagicArena "exceeds Seedream 4.5"; no numbers given. [measured-self-reported, no numbers]
- Maker's own limit: "Seedream 5.0 Lite is a relatively small model, and there is still room for improvement in structural stability, realism, and aesthetics." [maker-claim]
- No arXiv report for 5.0 Lite was found.

### F9. Gemini 3 Pro Image (Nano Banana Pro) model card (Google DeepMind, Nov 2025)
- Source: https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Image-Model-Card.pdf. Read in full.
- Architecture: "based on Gemini 3 Pro" (a natively multimodal reasoning LLM). Output up to 64K tokens. No other detail. Knowledge cutoff January 2025. [maker-claim]
- Method: human-rater Elo on Google's own prompt sets. Rivals: Gemini 2.5 Flash Image, GPT-Image 1, Seedream v4 4k, Flux Pro Kontext Max. NOT against GPT Image 1.5/2, Midjourney. [measured-self-reported]
- Elo (NB Pro / NB 2.5 Flash / GPT-Image-1 / Seedream v4 / Flux Kontext Max):
  - Stylization: 1098 / 933 / 1069 / 991 / 908
  - General T2I: 1094 / 1037 / 1025 / 1011 / 907
  - Text rendering: 1198 / 997 / 1150 / 1019 / 854
  - Character editing: 1176 / 1075 / 1016 / 889 / 843
  - Multi-character editing: 1213 / 950 / 997 / 840 / -
  - Multi-input (1-3 images): 1109 / 993 / 970 / 928 / -
  - Visual design: 1104 / 1083 / 1028 / 1038 / 907
  - Infographics: 1268 / 1162 / 1087 / 1049 / 824
  [measured-self-reported]
- Note: on Stylization and General T2I the lead over GPT-Image-1 is small (29 and 69 Elo). The big leads are in editing, text and infographics. [opinion, this author, from the table]
- Maker's own limits: "Text rendering: poor in small text (often blurry in 1k model), long paragraphs"; "Character consistency is not always perfect between input images and generated output image"; "Masked/Doodle based editing: partial instruction following"; "infrequent copying/pasting from user's input image"; "Occasional confusion around spatial localisation (e.g. left/right etc.)"; "Still limited in ... 3D reasoning and factuality". [maker-claim]
- DeepMind product page adds: "it can still struggle with small faces, accurate spelling, and fine details". https://deepmind.google/models/gemini-image/pro/ [maker-claim]

### F10. OpenAI GPT Image lineage: architecture and maker's own guidance
- Architecture: OpenAI's GPT-4o image system card addendum (Mar 2025) says 4o image generation is "an autoregressive model natively embedded within ChatGPT", not diffusion. https://cdn.openai.com/11998be9-5319-4302-bfbf-1167e093f1fb/Native_Image_Generation_System_Card.pdf [maker-claim]. OpenAI did not publish an architecture for GPT Image 2 or 2.5. Wikipedia calls GPT Image 2 "autoregressive with reasoning" and cites TechCrunch 21 Apr 2026; this is second-hand. https://en.wikipedia.org/wiki/GPT_Image
- GPT Image 2 snapshot: gpt-image-2-2026-04-21. https://developers.openai.com/api/docs/models/gpt-image-2 [maker-claim]
- OpenAI prompting guide (21 Apr 2026), maker's own limits: output above 2560x1440 is "more variable"; "Detailed camera specs may be interpreted loosely"; for small or dense text "compare medium or high before shipping". For a character across a series it advises: "Do not redesign the character", keep "Same facial features, proportions, and color palette", reuse anchor images. It gives NO hex-palette guidance. https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide [maker-claim]
- gpt-image-1 known issue, "warm color bias" and over-sharpening: reported by Heise (8 Apr 2025), cited by Wikipedia; Wikipedia says GPT Image 1.5 addresses it. I did NOT find a measured study of the yellow cast. https://www.heise.de/en/background/Image-generator-from-GPT-4o-what-is-probably-behind-the-technical-breakthrough-10343544.html [opinion, press]
- OpenAI on GPT Image 1.5 (16 Dec 2025): results still "imperfect" in scientific accuracy and many small faces. https://openai.com/index/new-chatgpt-images-is-here/ (page returns 403; quoted from search summary) [maker-claim, second-hand]

### F11. ViStoryBench v5 (arXiv 2505.24862 v5, 29 Mar 2026) — character and style consistency across a story
- Source: https://arxiv.org/abs/2505.24862. Table 2 read. Automatic metrics (CSD style similarity, CIDS character similarity, Gemini-3-Pro prompt-alignment judge) plus a user study. [measured-independent]
- ViStoryBench-Lite, with image reference (CSD cross / CIDS cross / Prompt Align / Aesthetics / Copy-paste):
  - GPT-4o image gen (gpt-image-1 lineage): 0.481 / 0.420 / 3.34 / 5.49 / 0.209
  - Gemini 2.5 (Nano Banana): 0.447 / 0.553 / 3.09 / 5.61 / 0.255
  - Gemini 3.0 Pro (Nano Banana Pro): 0.385 / 0.581 / 3.37 / 5.54 / 0.244
  - Seedream 4.0: 0.369 / 0.280 / 3.07 / 5.21 / 0.201
- Reading: Nano Banana Pro keeps the CHARACTER closest to the reference; the GPT-4o lineage keeps the STYLE closest to the reference and scores lowest on aesthetics ("lags in ... Aesthetics Score (5.49)"). Seedream 4.0 is weakest on character match. Paper: "Methods with high character consistency and high copy-paste score often have lower diversity". [measured-independent]
- Human study (character consistency, 0-4): GPT-4o 3.55, Seedream 4.0 3.23, Gemini 2.5 3.19. Nano Banana Pro not in the human study. [measured-independent]
- Limit: none of GPT Image 1.5/2/2.5, Seedream 4.5/5, Midjourney are in this benchmark.

### F12. Design-task papers with older lineage models
- PosterIQ (arXiv 2603.24078, 25 Mar 2026). MLLM judges (GPT-5, Gemini-2.5-Pro), human check on 30 images per task. Poster generation (Seedream-4.0 / Gemini-2.5-Flash-Image / GPT-Image-1 / Qwen-Image): Style 0.591 / 0.590 / 0.633 / 0.620; Composition 0.848 / 0.866 / 0.856 / 0.801; Font 0.342 / 0.391 / 0.299 / 0.286. "Font remains the bottleneck". https://arxiv.org/abs/2603.24078 [measured-independent]
- PaperBanana (Google Cloud AI Research + Peking Univ., arXiv 2601.23265, 30 Jan 2026). Method diagrams (flat, labelled illustration). Judge: Gemini-3-Pro. Nano-Banana-Pro overall 43.2 (aesthetics 65.5) vs GPT-Image-1.5 overall 11.5 (aesthetics 37.0). Authors say GPT-Image-1.5 has "weaker instruction following and text rendering". 50-case blind human test: 72.7% win for Nano-Banana-Pro. https://arxiv.org/abs/2601.23265 [measured-self-reported: Google authors, Google judge, Google model]

### F13. Higgsfield SOUL family and Marketing Studio Image 2.0 Alpha
- Rigorous coverage: NONE found. A search of arXiv for "Higgsfield" found no paper that tests SOUL, SOUL V2, SOUL Cinema or Marketing Studio Image. No Higgsfield technical report or model card was found. All lines below are [maker-claim] or [opinion].
- SOUL (v1): "hyper-realistic, fashion-grade AI photo model with 50+ aesthetic presets". Some presets are stylised (Mixed Media, Artwork, Glitch), but "the core focus remains photorealistic". https://higgsfield.ai/soul [maker-claim]
- SOUL 2.0: "built for creative, fashion-aware, culture-native generation"; "Designed for aesthetics - every image has taste built in"; "Unmatched Realism"; Soul ID keeps "identity locked across every style, pose, and lighting". https://higgsfield.ai/soul-intro [maker-claim]. Designboom (3 Apr 2026) reports: "The technical foundation of Soul 2 is rooted in preference optimization based on human feedback from art directors, photographers, and concept artists." Base model not named. https://www.designboom.com/technology/higgsfield-art-directed-quality-ai-image-generation/ [maker-claim, via press]
- SOUL Cinema (preview 4 Mar 2026): "mainly targets generation of cinematic-grade images"; fixed cinematic style, film grain, depth of field, close-ups; "moving away from 'plastic' textures". It accepts a "Soul HEX" palette: "extract palettes from reference photos and generate brand-consistent and color-matched visuals". https://higgsfield.ai/blog/soul-cinema-preview [maker-claim]. No measurement of Soul HEX palette accuracy was found.
- Higgsfield's own model guide (modified 28 Aug 2026): Soul = "fashion, cinematic, or culture-native visuals. Character consistency"; GPT Image = "accurate text rendering or precise color"; Nano Banana = "strong reference control"; Seedream = "intelligent visual reasoning"; Recraft = "photorealistic or expressive vector-style images". https://higgsfield.ai/creator-hub/help-center/ai-models/which-ai-model-should-i-use [maker-claim, by a reseller]
- Marketing Studio Image 2.0 Alpha: API docs name no underlying model. Parameters: quality "low"/"medium"/"high"; resolution 1k/2k/4k; up to 16 reference image URLs; prompt up to 5000 characters; a preset "enhancement" mode takes a product image plus an optional person image. https://docs.higgsfield.ai/docs/models/marketing-studio-image/generate-and-edit [maker-claim]
  - Inference, NOT verified: the low/medium/high quality set and the 16-reference limit are the same as the GPT Image 2.5 API (F1). This suggests, but does not prove, an OpenAI model under it. [opinion, this author]
- Consequence for the founder: SOUL models are built for photoreal fashion and cinematic people shots. The maker does not claim flat vector or painterly illustration, animals, or mascots. [maker-claim, absence]

### F14. MultiBanana (Univ. of Tokyo, CVPR 2026; arXiv 2511.22989 v2, 26 Mar 2026) — many reference images
- Source: https://arxiv.org/abs/2511.22989. Judges: Gemini 2.5 and GPT-5 averaged; Qwen3-VL cross-check. Versions of Nano Banana (2.5 Flash Image) and GPT-Image-1 "as of January 2026". Funded partly by Google Japan. [measured-independent]
- Scores (10-point): single reference: Nano Banana 7.817, GPT-Image-1 7.804. Two references: Nano Banana 4.891, GPT-Image-1 6.585. Many objects: 4.453 vs 5.086. With background: 3.575 vs 5.019. [measured-independent]
- Finding: closed models "incorporate all required subjects but suffer from compositional distortion due to overfitting to reference details"; open models (Qwen-Image-Edit) "generate visually cleaner outputs but often omit some reference subjects". Both fail more on cross-domain references (photo vs anime), scale gaps, rare concepts. [measured-independent]
- With an agent that rewrites the prompt, GPT-Image-1 improved; Nano Banana "showed no improvement and, in some cases, performance degraded". [measured-independent]
- Limit: Nano Banana Pro and GPT Image 2/2.5 are not tested.

### F15. GenScale (Boston Univ. + Creatify AI, arXiv 2609.00525, Sep 2026) — relative object size
- Source: https://arxiv.org/abs/2609.00525. Models "achieve high visual realism and yet often violate real-world size relationships". The best model (Nano Banana 2) reaches only 56.5% on one task. GPT-Image-2, Nano Banana 2, Seedream v4.5, FLUX.2 all tested. [measured-independent]
- Relevance: a mascot beside people or objects can get the wrong size. [opinion, this author]

### F16. Seedream 3.0 technical report (ByteDance Seed, arXiv 2504.11346, Apr 2025) — lineage, and rival observations
- Source: https://arxiv.org/abs/2504.11346. Relevant sections read.
- Human expert evaluation (Bench-377; alignment, structure, aesthetics): Seedream 3.0 beats Midjourney v6.1 on overall aesthetics and in the design category, "though it lags slightly behind in categories such as art". "Midjourney exhibits superior aesthetic capabilities but shows limited proficiency in functional alignment and structural fidelity." [measured-self-reported, by a rival of Midjourney]
- Portrait arena (over 50,000 battles): Seedream 3.0 and Midjourney v6.1 "both rank first"; Midjourney "excels in conveying emotional expressions". [measured-self-reported]
- On GPT-4o image generation (gpt-image-1 lineage): "images generated by GPT-4o tend to have a dark yellowish hue and exhibit significant noise" (Fig. 20, examples, no number). GPT-4o editing "tends to struggle with preserving the original image, particularly regarding IP and ID consistency". Gemini-2.0 editing "often produces issues with color naturalness". [opinion with examples, by a rival; not measured]
- This is the only primary written source I found for the GPT yellow cast. It applies to the 2025 model. F4 and F6 show GPT Image 2 near the top on Color Harmony and flat fills, so the cast is not measured as a problem in 2026. [opinion, this author]

### F17. Midjourney: rigorous coverage
- Current model: V8.1, default since spring 2026 (V8.1 released 14 Apr 2026; update post 30 Apr 2026). Maker says it reads prompts better, "holding on to small details"; "moodboards and srefs now super stable"; aesthetic "in the spirit of V7". https://updates.midjourney.com/v8-1-updates/ and https://updates.midjourney.com/v8-1-is-now-the-default-model/ [maker-claim]
- NO peer-reviewed paper or benchmark paper that tests Midjourney V7, V8 or V8.1 was found. Midjourney has no public API, so API-based benchmarks (F3, F4, F5, F6, F11) leave it out. [absence, checked by search]
- Lineage evidence only:
  - GenAI-Bench (CMU/Meta, arXiv 2406.13743, 2024): human ratings, basic prompts: Midjourney v6 4.0 vs DALL-E 3 4.3; advanced prompts: 3.4 vs 3.4. https://arxiv.org/abs/2406.13743 [measured-independent, old version]
  - Seedream 3.0 report (F16): Midjourney v6.1 best in "art", weaker in alignment and structure. [measured-self-reported by a rival]
- Practitioner reviews that rank Midjourney V7 first on "artistic style" (e.g. VePrompts, June 2026) do not publish prompt counts, raters or outputs. They fail the source bar. Not used.

### F18. Prompt rewriting (a behaviour, from makers' docs)
- OpenAI: in the Responses API image tool, "the mainline model ... will automatically revise your prompt"; the text used is returned in revised_prompt. https://developers.openai.com/api/docs/guides/image-generation [maker-claim]
- Nano Banana Pro is "based on Gemini 3 Pro", a reasoning model (F9). GPT Image 2 "reasons before it generates" (press). Seedream 5.0 Lite does "multi-step reasoning" (F8). So three of the model families put a language model between the prompt and the pixels. [maker-claim]
- Evidence on the cost of this: Violin (F6) says Seedream-5.0 prefers "learned 'aesthetic patterns' over precise user commands". MultiBanana (F14): prompt rewriting by an agent helped GPT-Image-1 but not Nano Banana. No study isolates rewriting as the cause of style drift in these models. [measured-independent, partial]

### F19. BizGenEval (Microsoft + SJTU + Fudan, arXiv 2603.25732, 26 Mar 2026) — commercial design content
- Source: https://arxiv.org/abs/2603.25732. Read in part. 400 prompts, 8,000 human-verified yes/no checklist items, MLLM judge; slides, charts, web pages, posters, science figures. Scores hard / easy. [measured-independent]
- By capability, HARD set (Layout / Attribute binding / Text / Knowledge):
  - Nano Banana Pro: 72.2 / 65.6 / 86.4 / 82.6
  - Nano Banana 2.0: 68.4 / 57.4 / 83.4 / 64.6
  - Seedream 5.0: 67.6 / 42.4 / 43.4 / 41.8
  - GPT-Image-1.5: 51.6 / 25.8 / 40.4 / 26.0
  - Seedream 4.5: 35.4 / 22.4 / 41.4 / 21.4
  - FLUX.2-Pro: 6.1 / 0.0 / 0.0 / 0.2
- Paper: "Layout Control and Attribute Binding remain more challenging, especially on the hard subsets". GPT-Image-1.5 shows a "homogenization" error (all chart markers get the same value). [measured-independent]
- GPT Image 2 is NOT in the BizGenEval paper. The SenseNova-U1.5 report (F20) ran it: Layout 88.5, Attribute 81.9, Text 83.9, Knowledge 74.2 (hard). That puts GPT Image 2 first on layout and attribute binding. [measured-independent, by a third lab; NB Pro numbers in that table equal BizGenEval's own]

### F20. SenseNova-U1.5 report (SenseTime, arXiv 2609.11929, Sep 2026) — closed models as baselines on OneIG-Bench, LongText, BizGenEval
- Source: https://arxiv.org/abs/2609.11929. Tables read.
- OneIG-Bench EN (Alignment / Text / Reasoning / Style / Diversity / Overall):
  - Nano Banana Pro: 0.889 / 0.962 / 0.333 / 0.483 / 0.247 / 0.583
  - Seedream 5.0 Pro: 0.899 / 0.886 / 0.341 / 0.431 / 0.207 / 0.553
  - GPT Image 2: 0.903 / 0.741 / 0.352 / 0.443 / 0.139 / 0.516
  [measured-independent]
- OneIG metric meaning (from the OneIG paper, arXiv 2506.07977): Style = similarity of style embeddings (CSD + OneIG style encoder) between the output and reference images of the NAMED style. Diversity = 1 minus DreamSim similarity between several outputs of the same prompt. So: Nano Banana Pro best hits a named style; GPT Image 2 gives the MOST SIMILAR outputs for one prompt (lowest diversity, 0.139). [measured-independent]
- Reading for the founder: low diversity is good for a matching set, bad for exploring options. This is the only measured "sameness" number I found. [opinion, this author]
- LongText-Bench (image-level accuracy): Nano Banana Pro 0.49, GPT Image 2 0.38, Seedream 5.0 Pro 0.17. [measured-independent]

### F4 addendum. Qwen-Image-Bench "Naturalness" and "Material Texture" facets (artefact proxies)
- Same heatmap, same column order (GPT Image 2 / Nano Banana 2 / GPT Image 1.5 / Nano Banana Pro / Qwen 2.0 Pro / Seedream 5.0 / Seedream 4.5 / Seedream 4.0 / FLUX 2 Max):
  - Naturalness: 50.18 / 42.04 / 42.38 / 45.69 / 42.00 / 35.31 / 43.04 / 41.32 / 40.20
  - Material Texture: 76.74 / 72.13 / 74.04 / 75.15 / 74.06 / 65.16 / 72.25 / 72.90 / 72.52
- Seedream 5.0 is lowest of the top models on both. This agrees with ByteDance's own note that 5.0 Lite has "room for improvement in structural stability, realism, and aesthetics" (F8). [measured-independent]
- No rigorous study that names "plastic skin" or "over-rendering" for these models was found.

### F21. ImageBench V1 (independent site, 2026) — LOWER TIER
- Source: https://imagebench.ai/imagebench-v1/fal--google--nano-banana-pro-vs-openai--gpt-image-2. 192 prompts, 6 categories, VLM judge plus an aesthetic preference model, all outputs published. Owner and date not stated on the page. The site itself says labels "can contain mistakes". [systematic-practitioner]
- Nano Banana Pro vs GPT Image 2 pass rates: Text 100% vs 100%; Spatial 89% vs 91%; Human realism 57% vs 69%; Truthfulness 56% vs 74%; Professional studio 89% vs 100%; Graphical design 92% vs 100%. [systematic-practitioner]
- The fetch tool reported that the overall leaderboard places the GPT Image 2.5 variants first and does not list Midjourney, Higgsfield or Seedream 4.5. I could not read the rows directly. Not relied on.

### F8 correction. Which "Seedream 5" the papers tested
- Qwen-Image-Bench (F4), BizGenEval (F19) and SenseNova-U1.5 (F20) cite the URL https://seed.bytedance.com/en/seedream5_0_lite for their "Seedream 5.0" / "Seedream-5.0-Pro". Thus their numbers ARE for Seedream 5.0 Lite (the name "Pro" in SenseNova is their label). [measured-independent, checked in the reference lists]
- Violin (F6) gives no reference for "Seedream-5". Swift-Image (F5) cites the Seedream 4.0 paper for "Seedream5 Pro". For these two, the variant is not known.

---

## Model profiles


### GPT Image 2 (OpenAI, 21 Apr 2026) and GPT Image 2.5 Flare / Sunburst (8 Sep 2026)
Best at:
- Overall creative work. First on all five pillars of Qwen-Image-Bench, with "no discernible weakness" (F4, May 2026). [measured-independent]
- Graphic design (93.4), Style Control (75.85), Color Harmony (75.36), Composition (69.46), 2D layout (66.55). First on each (F4). [measured-independent]
- Animals (42.64) and anatomy (20.91): first, but on a scale where all models fail (F4). [measured-independent]
- Exact place and size of a shape, and masks. Clearly first of the closed models (F6, May 2026). [measured-independent]
- Layout and attribute binding in commercial design: hard-set layout 88.5, attribute 81.9, first (F19/F20, Sep 2026). [measured-independent]
- Editing, and applying the style of a reference image ("Ref-Stylize" 4.75, first) (F5, Aug 2026). [measured-independent]
- Very similar outputs for one prompt (OneIG Diversity 0.139, the lowest) (F20). Good for a uniform set. [measured-independent]
Worst at:
- Long and dense text is behind Nano Banana Pro: OneIG Text 0.741 vs 0.962; LongText 0.38 vs 0.49 (F20). [measured-independent]
- Exact hex colour. RGB distance to the target is 0.137, the same as the other models (F6). [measured-independent]
- Prompt rewriting. In the Responses API a language model rewrites the prompt before the image model sees it (F18). [maker-claim]
- Lineage (gpt-image-1, 2025): "dark yellowish hue" and noise (F16, rival's examples); poor identity keeping in edits (F2, F16); lowest aesthetics in ViStoryBench (F11). F4 and F6 do not show these problems for GPT Image 2. [opinion by rivals / measured-independent for the old model]
- GPT Image 2.5: NO independent quality study found. The system card has safety numbers only. No published quality difference between Flare and Sunburst (F1). [maker-claim]
Evidence strength: GPT Image 2 = STRONG (five independent papers, 2026). GPT Image 2.5 = WEAK (maker claims and arenas only; three weeks old).

### Nano Banana Pro (Google, Gemini 3 Pro Image, Nov 2025)
Best at:
- Text, including long text: OneIG Text 0.962, LongText 0.49, BizGenEval text 86.4 (F19, F20). [measured-independent]
- Hitting a NAMED style: OneIG Style 0.483, best of the three families (F20). [measured-independent]
- Keeping a character like its reference: ViStoryBench character similarity 0.581, best of the large models (F11). [measured-independent]
- Clean images: second on the Quality pillar, "superior artifact suppression" (F4). [measured-independent]
- Most variety of the three families (OneIG Diversity 0.247) (F20). [measured-independent]
- Maker's human Elo leads in editing, multi-character editing, infographics, stylization vs gpt-image-1 and Seedream 4.0 (F9). [measured-self-reported]
Worst at:
- Animals 31.05, behind GPT Image 2 (42.64) and Seedream 4.5 (37.27) (F4). [measured-independent]
- Style Control 66.59 and Graphic Design 77.91, well behind GPT Image 2 (75.85, 93.4) (F4). [measured-independent]
- Editing overall: sixth in Swift-Image; reference-based 4.27 vs 4.51 for GPT Image 2 (F5). [measured-independent]
- Maker's own list: blurry small text at 1K, character consistency "not always perfect", left/right confusion, copy-paste from the input image (F9). [maker-claim]
- Lineage (Nano Banana 2.5): distortion when it has many reference images; a prompt-rewriting agent did not help it (F14). Weak instruction following in edits (F2). [measured-independent / measured-self-reported by a rival]
Evidence strength: STRONG (model card with human Elo, plus six independent papers).

### Seedream 4.5 (ByteDance; release date not checked)
Best at:
- Animals (37.27) and anatomy (16.59): second after GPT Image 2 (F4). [measured-independent]
- Quality and Aesthetics higher than Seedream 5.0 (F4). [measured-independent]
- Maker: better identity keeping from references and dense poster text than 4.0 (F2, figure only). [measured-self-reported]
Worst at:
- Commercial layout and attribute binding: hard layout 35.4, attribute 22.4 (F19). [measured-independent]
- Style Control 58.71, Composition 57.42, Graphic Design 67.47 (F4). [measured-independent]
- Editing: ninth in Swift-Image (4.22); reasoning edits 3.79 (F5). [measured-independent]
- Lineage (4.0): weakest character match in ViStoryBench (0.280) (F11); "greater variability", better "best-of-4" than average (F2). [measured-independent / measured-self-reported]
Evidence strength: MODERATE (in four independent papers; the maker's 4.5 section has no table).

### Seedream 5.0 Lite (ByteDance, 13 Feb 2026)
Best at:
- Text accuracy: 80.68, first in Qwen-Image-Bench (F4). [measured-independent]
- Creative Generation: more than 4 points above Seedream 4.5 (F4). [measured-independent]
- Commercial layout: hard 67.6, near Nano Banana 2.0 (F19). [measured-independent]
Worst at:
- Animals 22.41, the lowest of the top group; Naturalness 35.31; Material Texture 65.16 (F4). [measured-independent]
- Obedience: it prefers "learned 'aesthetic patterns' over precise user commands" (F6; variant not named in that paper). [measured-independent]
- Style: OneIG Style 0.431, lowest of three; LongText 0.17 (F20). [measured-independent]
- Maker: "relatively small model ... room for improvement in structural stability, realism, and aesthetics" (F8). [maker-claim]
Evidence strength: MODERATE (three independent papers name the Lite URL; no technical report).

### Midjourney V8.1 (default since spring 2026; V7 before)
Best at:
- Maker: better prompt reading; "moodboards and srefs now super stable" (F17). [maker-claim]
- Lineage only: Midjourney v6.1 led Seedream 3.0 in "art" and in portrait emotion (F16). [measured-self-reported by a rival, 2025]
Worst at:
- Lineage only: "limited proficiency in functional alignment and structural fidelity" (v6.1, F16); prompt adherence below DALL-E 3 in human ratings (v6, F17). [measured-self-reported by a rival / measured-independent, old]
Evidence strength: NONE for V7/V8/V8.1. No API, so no 2026 benchmark paper tests it. Its "taste control" role rests on the founder's own judgement, not on outside measurement.

### Higgsfield SOUL, SOUL V2, SOUL Cinema, Marketing Studio Image 2.0 Alpha
Best at (maker claims only):
- SOUL / SOUL 2.0: photoreal fashion and "culture-native" people shots; Soul ID keeps a person's identity; preference-tuned on feedback from art directors (F13). [maker-claim]
- SOUL Cinema: fixed film-still look; "Soul HEX" palette from a reference photo (F13). [maker-claim]
- Marketing Studio Image 2.0 Alpha: product marketing images; up to 16 references; 1k-4k (F13). Underlying model not named. [maker-claim]
Worst at:
Evidence strength: NONE (no paper, no model card, no benchmark).

---

## Cross-model: which model the rigorous evidence favours, per brand-art job

1. Hero image with empty space for a headline.
   - Favours GPT Image 2. It is first on exact place and size (F6), commercial layout (F19/F20), 2D space and composition (F4).
   - Next: Nano Banana Pro (layout hard 72.2), then Seedream 5.0 Lite (67.6). Seedream 4.5 is weak (35.4).
   - Silent: no study tests "keep this area empty" in an illustration. Midjourney and Higgsfield are not tested.

2. Page background.
   - No benchmark tests backgrounds as such. Proxies: Color Harmony (GPT Image 2 75.36; Nano Banana Pro 69.72; Seedream 4.5 68.55), clean images (Nano Banana Pro second on Quality) (F4), flat fills (GPT Image 2 flattest, but most fine noise) (F6).
   - Silent: tiling, low contrast behind text, and seamless edges are not studied for any model.

3. Mascot or spot illustration (a manta ray).
   - ALL models fail here. Best Animals score is 42.6 of 100; best Anatomy is 20.9 (F4). Expect anatomy errors from every model and plan a correction step.
   - Order on Animals: GPT Image 2 (42.64) > Seedream 4.0/4.5 (37.6/37.3) > GPT Image 1.5 (32.8) > Nano Banana Pro (31.1) > Seedream 5.0 Lite (22.4) (F4).
   - Keeping the same character from a reference: Nano Banana Pro best in ViStoryBench (F11), but its maker says this is "not always perfect" (F9).
   - Relative size errors are common (F15).
   - Silent: no study tests marine animals, stylised mascots, or fin and gill anatomy.

4. A matching set in one style.
   - Favours GPT Image 2 for a uniform set: first on Style Control (75.85 vs 66.59 for Nano Banana Pro) (F4); first on applying a reference style in edits (F5); least variation between outputs (F20). The GPT lineage also kept style closest to a reference in ViStoryBench (F11).
   - Nano Banana Pro is best at matching a NAMED style (F20) and at keeping a character (F11).
   - Silent: no study measures drift across a set of 10 or more brand images. Midjourney style references are not tested.

5. Obeying a fixed colour palette (hex).
   - Silent for multi-colour palettes in an illustration, for every model in this list.
   - The only closed-model hex test (flat fills) shows no model hits the exact value; all are about 0.12 to 0.14 RGB distance from the target (F6).
   - Obeying a colour NAME is nearly equal across models (about 67 to 70) (F4).
   - Attribute binding, hard set (includes colour and other properties): GPT Image 2 81.9 > Nano Banana Pro 65.6 > Seedream 5.0 Lite 42.4 > Seedream 4.5 22.4 (F19/F20).
   - Open-model papers show diffusion models do not parse hex codes well (F7). Higgsfield "Soul HEX" is a maker claim with no measurement (F13).

Flat vector vs painterly: no rigorous study splits these two styles for these models. Qwen-Image-Bench "Art Design" is high for all (GPT Image 2 84.3; Nano Banana Pro 80.7; Seedream 4.5 77.5; Seedream 5.0 Lite 74.5), and the authors call style transfer "relatively mature" (F4).

Comparisons with the other named models (only where a rigorous source makes them):
- FLUX.2 (Pro/Max/dev): below all closed models in this list on Qwen-Image-Bench (F4), BizGenEval (F19) and UniGenBench++ (F3). Best open model on Violin (F6).
- Qwen Image 2.0 Pro: fifth overall on Qwen-Image-Bench, between Nano Banana Pro and Seedream 5.0 Lite; strong text, weaker anatomy (F4). (The benchmark is by the Qwen team.)
- Recraft: UniGenBench++ Style 87.20, Layout 57.84, far below the models in this list (F3). No rigorous test of its vector output.
- Ideogram: only 2025 lineage tests (Seedream 3.0 report, IMAGINE-E). No 2026 rigorous source.
- Grok Imagine: only GenScale (relative size error 0.785 vs 0.592 for a Gemini model and 0.692 for GPT) (F15). No other rigorous source.

---

## Bound

- Read in full or in all relevant parts (text extracts): Qwen-Image-Bench (2605.28091); Swift-Image (2608.20334) tables; Violin (2603.00166) tables and discussion; BizGenEval (2603.25732) tables; SenseNova-U1.5 (2609.11929) benchmark tables; ViStoryBench v5 (2505.24862) Table 2; MultiBanana (2511.22989) results and conclusion; Seedream 3.0 report (2504.11346) comparison sections; Gemini 3 Pro Image model card (all 7 pages); OneIG-Bench (2506.07977) metric section; GenAI-Bench (2406.13743) human-rating tables.
- Sampled through a summarising fetch tool (numbers not checked cell by cell): Seedream 4.0/4.5 report (2509.20427); UniGenBench++ (2510.18701); ChatGPT Images 2.5 system card; PosterIQ (2603.24078); PaperBanana (2601.23265); GenScale (2609.00525, one table read); ACBench (2609.20816); GenColorBench, NumColor (checked model lists only); Seedream 5.0 Lite blog; Midjourney V8.1 update post; OpenAI prompting guide and model page; Higgsfield pages; ImageBench.
- Could not reach: openai.com announcement pages for Images 2.0, 2.5 and 1.5 (HTTP 403); docs.midjourney.com (HTTP 403). No GPT Image 2 system card is listed on OpenAI's Deployment Safety Hub. No technical report exists that I could find for GPT Image 2/2.5, Seedream 5.0 Lite, Midjourney V7/V8, or any Higgsfield model.
- Arena Elo numbers are out of scope here (see `image-model-benchmarks.md`).
