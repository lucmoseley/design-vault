# Research: cut-out tools for brand-art renders (design-vault #54)

Date of research: 30 Sep 2026. Researcher: background agent.

Outcome: #54 ran the free local test proposed at the end of this file (results on #54) and ruled the colour key the house cut-out tool, built in #56. The paid Ideogram and Recraft size check is not owed: Ideogram is only the next tool to judge if the key fails, and Recraft is dropped on its own docs.

## Question

Which tool removes the plain background from a brand-art render, so that the asset has transparency?

- Sources of renders: GPT Image 2.5 (2688x1520), Grok Imagine 2.0 (2816x1584), Qwen Image 3, Ideogram 4.0. All come through the Higgsfield API. No render has alpha.
- The prompt sets ONE plain background colour. The subject does not use that colour. Thus the background colour is known before the cut.
- Styles: flat vector-like art, painterly brushstroke art, mascots with outlines.
- Machine: 8 CPU cores, 9 GB RAM, WSL2, no GPU.

## Fact bar

A tool is "drop" if one of these is true:

1. The licence (of the tool or of its model weights) does not permit commercial use.
2. The output has a visible watermark.
3. The service deletes the output and keeps no copy for us. (Deletion after we download the file is a pass.)
4. The resolution ceiling is less than a 2K hero (about 2688x1520 or 2816x1584).
5. A different candidate gives the same result for less money per usable image.

## Tags

- [maker-claim]: the vendor or the model author says it.
- [measured-independent]: a third party measured it.
- [systematic-practitioner]: a practitioner tested it on a set of images with a stated method.
- [opinion]: one person says it, with no method.
- "secondhand": the figure comes from a page that is not the owner of the fact.

## Findings


### F1. remove.bg API (Kaleido / Canva)

- Resolution: PNG output is "Up to 10 Megapixels e.g. 4000x2500". JPG, WebP and ZIP go "Up to 50 Megapixels". The `size=auto` value caps at 25 MP. A preview is 0.25 MP. [maker-claim] Source: https://www.remove.bg/api (read 30 Sep 2026).
- 2K check: 2816x1584 = 4.46 MP. This is less than 10 MP. PNG output keeps the full size. PASS.
- Foreground type: the API has `type=graphic` (added 3 Jun 2024). This is the only hosted API found with a stated "graphic" class. [maker-claim] Source: https://www.remove.bg/api changelog.
- Free tier: "Your first 50 API calls per month are on us". A free call gives a preview (0.25 MP) only. [maker-claim] Source: https://www.remove.bg/api. Preview cap = about 667x375 for a 16:9 image. This is too small for a hero.
- Price (secondhand, verified by CostBench 13 Jun 2026): 3 credits for $3.00; Lite $8.10/month (annual); Pro $35.10/month annual (200 credits) = about $0.18/image; Volume+ $80.10/month annual. One full-resolution image = 1 credit. Pay-as-you-go range is about $1.00 to $0.21 per image by pack size. Source: https://costbench.com/software/ai-media-apis/remove-bg-api/ (secondhand). The official pricing page did not render in the fetch tool.
- Watermark: none stated on paid output. Not found as a statement. [maker-claim by omission]
- Retention: the API returns the file in the HTTP response. Deletion on the server side does not stop us from keeping the file. PASS.
- Licence: a paid SaaS. Output is for commercial use (the product is sold for e-commerce). No clause quoted.
- Node: yes, plain HTTPS POST. No GPU needed.
- Fact-bar result: passes 1-4. FAILS 5 on price: about $0.18-$1.00 per image, against Photoroom $0.02 and Recraft $0.01. DROP (price).

### F2. Photoroom Remove Background API

- Price: Basic plan "$0.02" per image. Minimum is $20/month for 1,000 images (secondhand, search summary of Sep 2026 pages; the official page shows a slider). "Create an account and you get 10 free production calls on the Remove Background API." [maker-claim] Source: https://www.photoroom.com/api/pricing (read 30 Sep 2026).
- Sandbox: sandbox output "carries a watermark". Production output has no watermark. [maker-claim] Source: https://docs.photoroom.com/getting-started/pricing.
- Resolution: "Maximum Resolution: 6,000 pixels on the widest side", "Maximum File Size: 50MB". [maker-claim] Source: https://www.photoroom.com/api/pricing. PASS for 2K.
- Features: Basic plan includes "Green screen despill" and "Uncertainty scoring". [maker-claim]
- Scope: the pricing page mentions only product photography. It does not mention cartoons, illustrations or graphics.
- Node: yes (HTTPS multipart). No GPU.
- Fact-bar result: passes 1-4. Price: $0.02 per image, but a $20/month minimum. For a small volume (tens of images a month) the real cost per image is much higher than $0.02. It loses to Recraft and Ideogram ($0.01, pay per call) on price. DROP (price), unless both of them fail the size or quality test. It is the hosted reserve if the $0.01 tools fail.

### F3. Clipdrop Remove Background API (Jasper)

- Limits: "maximum resolution of 25 megapixels and a max file size of 30 Mb". Output has "the same dimensions as the image_file". "1 successful background removal API call = 1 credit". [maker-claim] Source: https://clipdrop.co/apis/docs/remove-background (read 30 Sep 2026).
- Price: the pricing page did not show a number to the fetch tool. Secondhand reports disagree ("1 credit = $0.01", "5 credits at $0.01 each"), and one reports that the public pricing page now goes to a contact form. Source: search summary of https://www.runflow.io/blog/best-background-remover-api and https://fapihub.com/alternatives/clipdrop/ (secondhand, 2026). Price NOT CONFIRMED.
- Owner: Clipdrop is part of Jasper. Jasper is still in operation in 2026, but it has cut staff. No named "successor" product was found.
- Fact-bar result: resolution PASS. Price not published, sales contact possibly needed. DROP (no published price; cannot be shown to beat Recraft at $0.01).

### F4. Recraft API removeBackground

- Endpoint: `POST https://external.api.recraft.ai/v1/images/removeBackground`. Input: "no more than 10 MB in size, have resolution no more than 16 MP, max dimension no more than 4096 pixels and min dimension no less than 256 pixels." Output format `png` or `webp`; response as `url`, `b64_json` or `multipart`. SVG input gives SVG output. [maker-claim] Source: https://www.recraft.ai/docs/api-reference/endpoints (read 30 Sep 2026).
- 2K check: 2816 < 4096 and 4.46 MP < 16 MP. PASS.
- Price: "Image background removal | $0.01 | 10 | Per request". Vectorize is also $0.01. [maker-claim] Source: https://www.recraft.ai/docs/api-reference/pricing (read 30 Sep 2026).
- Ownership: on a paid API, "you will fully own the generated content". The Free plan is non-commercial. [maker-claim] Source: https://www.recraft.ai/blog/ownership-and-commercial-use-faq and https://www.recraft.ai/docs/trust-and-security/ownership. Note: this clause is about generated images. A clause about images that the user uploads for editing was not found. The user owns the input, so risk is low.
- Retention: `b64_json` returns the file in the response. PASS.
- Also on Replicate as `recraft-ai/recraft-remove-background`. Source: https://replicate.com/recraft-ai/recraft-remove-background/api.
- Node: yes. No GPU.
- Fact-bar result: PASS 1-4. SURVIVES (hosted lead).

### F5. Bria: hosted API and RMBG-1.4 / RMBG-2.0 weights

- RMBG-2.0 weights licence: "Creative Commons Attribution–Non-Commercial (CC BY-NC 4.0)". Commercial use needs "a commercial agreement with BRIA". The weights are gated (log in and accept conditions). About 0.2 B parameters. Inference size 1024x1024. [maker-claim] Source: https://huggingface.co/briaai/RMBG-2.0 (read 30 Sep 2026).
- RMBG-1.4 weights licence: "The model is released under a Creative Commons license for non-commercial use. Commercial use is subject to a commercial agreement with BRIA." 44.1 M parameters. Inference size 1024x1024. Training set: over 12,000 hand-labelled images, "87.70% photorealistic, 12.30% non-photorealistic". [maker-claim] Source: https://huggingface.co/briaai/RMBG-1.4.
- Result for the local weights: FAIL rule 1 (non-commercial). DROP. This also drops rembg's `bria-rmbg` model (see F11).
- Hosted Bria RMBG 2.0 (commercial use permitted through the API): $0.018 per image on fal.ai; "Trained exclusively on licensed data for safe and risk-free commercial use". [maker-claim] Source: https://fal.ai/models/fal-ai/bria/background/remove (read 30 Sep 2026). Bria's own platform: also $0.018 per image, free trial of 100 API calls (secondhand, search summary; Bria's docs pricing URL gave HTTP 404). Pixazo resells at $0.04 (secondhand).
- Resolution: fal's page says "Up to 1024x1024 pixels (preserves input dimensions)". Interpretation: the mask is computed at 1024x1024 and scaled up to the input size. The output keeps the input size, but edge detail is limited by the 1024 mask. [maker-claim, interpretation mine]
- Replicate also hosts `bria/remove-background`: "non-binary masks allowing for 256 levels of transparency". Price not shown in the fetch. Source: https://replicate.com/bria/remove-background.
- Fact-bar result (hosted): PASS 1-4, but $0.018 > Recraft $0.01. DROP (price), unless Recraft quality fails.

### F6. fal.ai hosted models (BiRefNet v2, Bria)

- BiRefNet v2 on fal: variants "General Use (Light), General Use (Light 2K), General Use (Heavy), Matting, Portrait, General Use (Dynamic)". Operating resolution "1024x1024, 2048x2048, 2304x2304" (2304 only for Dynamic). `refine_foreground` default true. Output png, webp or gif. [maker-claim] Source: https://fal.ai/models/fal-ai/birefnet/v2/api (read 30 Sep 2026).
- Commercial use: the page marks the model "Commercial use". [maker-claim] Source: https://fal.ai/models/fal-ai/birefnet/v2.
- Price: the page shows "$0 per compute second". This looks like a display fault, not a real free price. Real price NOT CONFIRMED. (fal bills most models per output or per GPU second.)
- Retention: not stated on the page. With `sync_mode` the result comes back as a data URI, so we keep the file. PASS.
- Fact-bar result: PASS 1, 2, 3, 4 (2048 operating size is the best hosted edge detail found). Price unknown but very likely below $0.01 (Replicate runs the same model for about $0.0014, see F7). This is the hosted way to run BiRefNet if the local CPU run is too slow. SURVIVES as a fallback.

### F7. Replicate hosted models

- Retention: "all input parameters, output values, output files, and logs are automatically removed after an hour, by default." [maker-claim] Source: https://replicate.com/docs/topics/predictions/data-retention (read 30 Sep 2026). A script downloads the file at once, so rule 3 PASSES.
- `men1scus/birefnet`: about $0.0014 per run ("714 runs per $1"), Nvidia A100 80GB, "within 1 seconds". [maker-claim, Replicate estimate] Source: https://replicate.com/men1scus/birefnet (read 30 Sep 2026). Which BiRefNet checkpoint and which resolution it uses: not found on the page.
- `851-labs/background-remover`: "$0.00062 to run on Replicate, or 1612 runs per $1", Nvidia T4, about 3 s, uses "the transparent-background python package" (InSPyReNet). [maker-claim] Source: https://replicate.com/851-labs/background-remover. InSPyReNet licence: see F13.
- Node: Replicate has an official Node client. No local GPU.
- Fact-bar result: community BiRefNet on Replicate is the cheapest hosted run found (about $0.0014). But the checkpoint and the resolution are not stated, and a cold start can add time. SURVIVES as a fallback, same as F6.

### F8. Adobe Firefly Services / Photoshop API Remove Background

- Features: mode "cutout" or "mask"; options `trim`, `backgroundColor`, `colorDecontamination` ("reduces color bleeding"). [maker-claim] Source: https://developer.adobe.com/firefly-services/docs/photoshop/guides/remove-background/ (read 30 Sep 2026).
- Access: Firefly Services needs an enterprise agreement. A community answer says the minimum is a 3-year contract with 50 seats, and "this isn't something an individual can sign up for". Secondhand (Adobe community forum, found by search 30 Sep 2026; https://community.adobe.com/questions-404/firefly-api-access-1478448). A "$0.02 per image" figure also appears (secondhand, sudomock.com), but it is not an Adobe rate card. The legacy Photoshop API v1 reached end of life on 31 Jul 2026 (secondhand, sudomock.com).
- Fact-bar result: not available to a solo founder at a per-image price. DROP (rule 5 / not purchasable).

### F9. Picsart API

- Remove background: 2 credits per image (one secondhand source says 5). 200 free credits at sign-up (another source says 50). Rough cost "around $0.05 per image". All secondhand (search summary of picsart.io pages, 30 Sep 2026). The official pricing page did not render in the fetch tool.
- Resolution: one secondhand summary gives the same figures as remove.bg (PNG 10 MP). Not confirmed on a Picsart page.
- Fact-bar result: about $0.05 per image > Recraft $0.01. DROP (price).

### F10. Cloudinary background removal

- Cost unit: `e_background_removal` counts "75" transformations for each use. [maker-claim] Source: https://cloudinary.com/documentation/transformation_counts (read 30 Sep 2026). One credit = "1,000 transformations" (or 1 GB storage or 1 GB bandwidth). Free plan: "25 monthly credits". Plus: $99/month ($89 annual), 225 credits. [maker-claim] Source: https://cloudinary.com/pricing.
- Arithmetic: one removal = 0.075 credit. The Free plan's 25 credits cover about 333 removals a month if nothing else uses the credits. On Plus, cost is about $0.03 per removal inside a $89-99 monthly fee.
- Free-plan access: secondhand sources say background removal "can be used on the free plan, though usage limits apply". NOT CONFIRMED on a Cloudinary page. The old "AI Background Removal add-on" is closed to accounts made after 1 Feb 2026; the `e_background_removal` transformation replaces it (secondhand).
- Resolution: "a limit of 6144 x 6144 pixels on its input images". A "fine edges" option exists "for images with objects having delicate edges like fur". [maker-claim] Source: https://cloudinary.com/documentation/background_removal. PASS for 2K.
- Illustrations: the documentation shows only photo examples.
- Watermark on free plan: none found.
- Fact-bar result: if the free plan really allows it, it is free for small volume, which beats Recraft on rule 5. But it needs an account, an upload to a CDN, and the free-plan access is not confirmed. Its model is not named and has no illustration evidence. KEEP AS A POSSIBLE, NOT A LEAD.

### F11. rembg (local, Python, CPU)

- Tool licence: "Licensed under the MIT License". The README also says: "Model weights carry their own licenses, independent of rembg's MIT license — check the linked source before using any model commercially." [maker-claim] Source: https://github.com/danielgatis/rembg (read 30 Sep 2026; repo pushed 20 Sep 2026, 24.9k stars).
- TRAP: the default model is now `bria-rmbg` (BRIA RMBG-2.0, CC BY-NC 4.0). The code calls `new_session("bria-rmbg")` when no model is given. Source: https://raw.githubusercontent.com/danielgatis/rembg/main/rembg/bg.py (line 324, read 30 Sep 2026). A script that calls `remove()` with no `-m` uses a non-commercial model. Always pass the model name.
- Install (CPU): `pip install "rembg[cpu,cli]"`. It runs on ONNX Runtime. It has a CLI, a Python API and an HTTP server (`rembg s`), so a Node script can call it through the CLI or the HTTP server.
- Model licences, per the upstream repo (GitHub API, read 30 Sep 2026) and ONNX file size (rembg release v0.0.0):

| rembg model | Upstream | Weights licence | ONNX size | Inference size | Commercial? |
| --- | --- | --- | --- | --- | --- |
| u2net / u2netp / silueta | xuebinqin/U-2-Net | Apache-2.0 | 167 / 4 / 42 MiB | 320 | Yes |
| isnet-general-use | xuebinqin/DIS | Apache-2.0 | 170 MiB | 1024 | Yes |
| isnet-anime | SkyTNT/anime-segmentation | Apache-2.0 | 167 MiB | 1024 | Yes |
| birefnet-general | ZhengPeng7/BiRefNet | MIT | 927 MiB | 1024 | Yes |
| birefnet-general-lite | ZhengPeng7/BiRefNet | MIT | 213 MiB | 1024 | Yes |
| birefnet-massive / -dis / -hrsod / -cod / -portrait | ZhengPeng7/BiRefNet | MIT | 927 MiB each | 1024 | Yes |
| BiRefNet_HR-general (release file, not yet a named session found) | ZhengPeng7/BiRefNet | MIT | 1048 MiB | 2048 | Yes |
| bria-rmbg (DEFAULT) | briaai/RMBG-2.0 | CC BY-NC 4.0 | 976 MiB | 1024 | NO - drop |
| ViTMatte (edge refiner, `-vm`) | hustvl/ViTMatte | MIT | 109-379 MiB | - | Yes |
| sam | Meta SAM | Apache-2.0 | 8-1177 MiB | - | Yes (needs a point prompt) |

- Note on training data: the weights are MIT or Apache-2.0. Some training sets (for example DUTS, DIS5K, HRSOD) are research datasets. No clause was found that carries a dataset restriction onto the weights. This is a residual risk, not a fact-bar failure.
- Mask resolution: every session computes the mask at its inference size (1024x1024 for the modern models) and then resizes the mask to the input size with Lanczos (`mask.resize(img.size, Image.Resampling.LANCZOS)`). Source: rembg `sessions/birefnet_general.py` line 48. So the output keeps 2688x1520 or 2816x1584, but edge detail is from a 1024 mask stretched about 2.7x wide. Rule 4 PASSES on size; edge sharpness is a quality question.
- Edge modes: naive (default), `-dc` decontaminate ("It only changes color, never coverage"), `-a` closed-form alpha matting ("much slower", "can fail to converge"), `-vm` ViTMatte. `-ppm` makes a binary mask with "no partially transparent pixels at all". [maker-claim] Source: rembg README §Choosing an edge mode.
- CPU time: rembg's own figure was not found. See F12 for BiRefNet CPU figures.
- Fact-bar result: PASS 1-5 with an explicit commercial model (`birefnet-general`, `birefnet-general-lite`, `isnet-anime`, `isnet-general-use`). FAIL with the default model. SURVIVES as the local runner.

### F12. BiRefNet (local weights) and its checkpoints

- Licence: MIT for code and for every HF checkpoint checked (`cardData.license = mit` for BiRefNet, BiRefNet_HR, BiRefNet_dynamic, BiRefNet_lite, BiRefNet_lite-2K, BiRefNet-matting, BiRefNet_HR-matting). Source: https://huggingface.co/api/models/ZhengPeng7/<name> (read 30 Sep 2026).
- Checkpoints relevant to a 2K hero (all [maker-claim], source https://github.com/ZhengPeng7/BiRefNet README):
  - `BiRefNet` (General, swin_v1_large, 1024x1024). HF safetensors 423 MiB.
  - `BiRefNet_HR` (General, "trained on images in 2048x2048"). 423 MiB.
  - `BiRefNet_dynamic` ("trained on images in a dynamic resolution range from 256x256 to 2304x2304", "robust performance on any resolution"). 423 MiB.
  - `BiRefNet_lite-2K` (swin_v1_tiny, "takes inputs in a much higher resolution (2560x1440)"). 169 MiB. Its input is close to the 16:9 renders.
  - `BiRefNet_HR-matting` (2048x2048, soft alpha). 423 MiB.
- Training data of General: photo sets only (DIS5K, DUTS, HRSOD, UHRSD, HRS10K, P3M, humans; the 2048 set adds AM-2k, AIM-500, Distinctions-646 and others). No anime, cartoon or illustration set is named. [maker-claim] Source: BiRefNet README model-zoo table.
- CPU speed at 1024x1024, AMD Ryzen 5 5600X (6 cores), fp32 [maker-claim of vision.cpp, measured on BiRefNet by a third party = measured-independent for BiRefNet]: Full model 16.3 s (vision.cpp) / 18.3 s (PyTorch); Lite model 4.5 s (vision.cpp) / 10.9 s (PyTorch) / 7.0 s (ONNX Runtime). Source: https://github.com/Acly/vision.cpp README §Performance (read 30 Sep 2026).
- Estimate for this machine (my inference, not measured): a 2048 checkpoint does about 4x the work of 1024. Expect about 1 minute or more per image for BiRefNet_HR on 8 WSL2 cores, and about 15-20 s for the 1024 Full model. Acceptable for a few hero assets.
- GPU memory at 1024: "5.5G GPU memory is needed for inference in 1024x1024" [maker-claim, BiRefNet README]. CPU RAM figure: NOT FOUND. My estimate: 3-6 GB peak for the Full model at 1024 in ONNX Runtime. This is close to the free RAM on this machine (about 2 GB free, 9 GB total, at the time of research). A 2048 run could exceed it. Test the Lite model first.
- Fact-bar result: PASS 1-4, free. SURVIVES.

### F13. BEN2 and InSPyReNet (transparent-background)

- BEN2 Base: MIT, 94.6 M parameters; "trained on the DIS5k and our 22K proprietary segmentation dataset"; `refine_foreground` post-process, default False. A separate closed "full" model is sold through backgrounderase.com. HF files: BEN2_Base.onnx 212 MiB. [maker-claim] Source: https://huggingface.co/PramaLLC/BEN2 (read 30 Sep 2026). No illustration figures. Fact-bar: PASS 1-4. No evidence it beats BiRefNet on art. KEEP AS AN OPTION, NOT A LEAD.
- InSPyReNet / `transparent-background` package: MIT (both repos). Modes: base (1024x1024), fast (384x384), base-nightly. `--resize dynamic` option ("sharper, potentially unstable"). CPU is supported; GPU is recommended. Source: https://github.com/plemeri/transparent-background (read 30 Sep 2026). No illustration figures found. KEEP AS AN OPTION, NOT A LEAD.

### F14. ToonOut (BiRefNet fine-tuned on anime) - the only illustration benchmark found

- What: BiRefNet General (the "checkpoint saved after 244 training epochs") fine-tuned on "a custom dataset of 1,228 high-quality anime images of characters and objects". Paper submitted 8 Sep 2025. Source: https://arxiv.org/abs/2509.06839 and https://arxiv.org/html/2509.06839.
- Licence: code and weights MIT; dataset CC-BY 4.0. Source: https://github.com/MatteoKartoon/BiRefNet and https://huggingface.co/joelseytre/toonout. Weights file `birefnet_finetuned_toonout.pth` = 844 MiB (PyTorch, not ONNX). A GGUF version for CPU (vision.cpp) exists: https://huggingface.co/Acly/BiRefNet-toonout-GGUF (MIT). Replicate endpoints: `sprited/birefnet-toonout`.
- Results on their 126-image anime test set (Table 1). The authors made ToonOut, so the ToonOut row is [maker-claim]. The other rows are third-party models measured by these authors, so they are [measured-independent] for those vendors. Date: Sep 2025.

| Model | Pixel Accuracy | Boundary IoU | MAE |
| --- | --- | --- | --- |
| ToonOut | 99.5% | 95.6% | 0.03 |
| Photoroom (API) | 99.2% | 95.2% | 0.04 |
| BRIA RMBG 2.0 | 97.8% | 92.4% | 0.08 |
| BiRefNet (General, base) | 95.3% | 88.5% | 0.15 |

- Pixel Accuracy definition: a pixel is correct when |pred - GT alpha| <= 10 (of 255), after one erosion of the error mask "to avoid penalizing edge artifacts"; PA = (1 - incorrect/foreground pixels)^2. So this metric forgives thin edge errors. Boundary IoU is the better edge figure.
- Named failure modes of base BiRefNet on anime: "the area between a character's ponytail and head, between limbs and torso, folds in clothing" and "hair strands, fingers, detailed object contours". These are exactly the interior-hole and thin-part cases in our brief. [measured-independent for BiRefNet]
- Limits for our use: test images are anime characters, not flat vector spot art or painterly art. The test set is from the same source as the training set (in-distribution), which favours ToonOut. Background colour of the test images: not stated in my extraction. Halo/fringe and partial-transparency share: NOT MEASURED in the paper.
- Fact-bar result for ToonOut weights: PASS 1-4, free. SURVIVES as the best-evidenced local model for outlined mascot art.

### F4 (update). Recraft: a size caveat that can fail rule 4

- Recraft's own Studio documentation says: "Remove background functionality works with images with resolution of 1024 by the smaller side. For images with large resolution there might be some artifacts on the border of the image." And: "When using Remove background on large images, Recraft automatically downscales the image before applying edits, which can result in a noticeable loss of quality in the final output." [maker-claim] Source: https://www.recraft.ai/docs/recraft-studio/image-editing/background-tools (read 30 Sep 2026).
- It also says the tool "is especially tuned for AI-generated images". [maker-claim, same page]
- Our renders have a smaller side of 1520 or 1584 px. So they are above the 1024 limit. The API page accepts up to 16 MP / 4096 px as INPUT, but no page says the OUTPUT keeps the input size. It is possible that the API returns a downscaled image, or a full-size image with a soft edge. NOT VERIFIED. A test call ($0.01) must check the output size before Recraft is chosen.

### F15. IMG.LY GenAI Benchmarks: transparency (context, not a cut-out test)

- 23 image models were asked for transparent PNGs. "20 of 23 scored exactly zero" on alpha. GPT Image 1.5: 4.22/5; Recraft V3: 2.00/5; Recraft V4.1: 2.00/5. [measured-independent] Scores computed 14 Sep 2026. Source: https://img.ly/ai-benchmarks/findings/transparency/.
- Scoring bands: "5 for a clean cutout under 10% partial pixels, 3 from 10% to 25% partial, 2 above 25%, 1 when a channel exists but the image is opaque, 0 when there is no channel." Source: https://img.ly/ai-benchmarks/methodology/. So a Recraft score of 2 means more than 25% of pixels were partly transparent (the brief's 47% figure is consistent with this; the exact 47% was not found on the pages I read).
- Their advice: "Plan for deterministic background removal and edge cleanup after generation; prompt engineering does not produce a usable alpha channel". [opinion of the benchmark authors]
- Note: IMG.LY sells a background-removal library, `@imgly/background-removal-node`, licensed "AGPL" with a commercial licence on request (support@img.ly). Source: https://github.com/imgly/background-removal-js. AGPL permits commercial use but forces source release for a networked service. For a local build step it is usable, but no illustration evidence was found and the model is not named on the page. NOT A LEAD.

### F16. Deterministic colour key (known background colour)


- Theory: a pixel on an edge is a mix: `observed = alpha * foreground + (1 - alpha) * background`. With a known background colour B, one image gives 3 equations and 4 unknowns (alpha and three foreground channels). So one image cannot give an exact answer. The usual extra rule is "take the largest alpha that keeps the foreground colour in range". Source: the GIMP/GEGL colour-to-alpha source comment ("maximizing alpha without taking b1 above 1 gives ... alpha = (a1-c1) / (1-c1)"). https://raw.githubusercontent.com/GNOME/gegl/master/operations/common-gpl3+/color-to-alpha.c (read 30 Sep 2026).
- GEGL colour-to-alpha algorithm (GIMP "Color to Alpha"): for each channel, distance d = |pixel - colour|. Below `transparency_threshold` the channel gives alpha 0; above `opacity_threshold` it gives alpha 1; between, alpha rises linearly. The pixel alpha is the maximum over the three channels. Then the colour is un-mixed: `dst = c + (dst - c) / alpha`. This un-mixing removes the background tint from edge pixels (it is a despill / decontamination by construction). Licence: GPL-3.0-or-later. GPL does not bar commercial use and does not cover output images. Re-implementing the maths in our own Node code is simple (about 30 lines).
- Weak point of a global colour key: EVERY pixel in the image is judged by distance only. A subject pixel that is near the background colour in all channels becomes partly transparent. Examples: a pale shadow on a pale background; a painterly brushstroke that the model blended into the background; a drop shadow that the model painted. ImageMagick's guide states the same: "Parts of the image object which are close to the background color, or worse still, exactly matches the background, will be thought of as being the same as the background." Source: https://usage.imagemagick.org/masking/ (read 30 Sep 2026).
- Strong point: interior holes. A key removes enclosed background (between an arm and a body) without any learning. A key also gives exact un-mixed edge colour, so no background-colour halo, if B is exact.
- Second weak point for AI renders: the "plain" background is rarely one exact value. Generators add noise, gradients, vignettes and compression. The key must use a tolerance band (transparency_threshold) sampled from the image border, or a per-region background estimate. Evidence on how flat GPT Image 2.5, Grok, Qwen or Ideogram backgrounds really are: NOT FOUND. Our own test must measure the border's colour spread.
- ImageMagick's recommended method for a known background: a difference image against the background, two thresholds (definitely background, definitely subject), then an edge band normalised to partial alpha. "This method is probably the best and most universal background removal technique." Source: https://usage.imagemagick.org/masking/. A two-background "triangulation" method (Smith and Blinn, "Blue Screen Matting", SIGGRAPH 1996) gives exact alpha, but it needs the same subject on two backgrounds. A generator cannot repeat a render exactly, so it is not usable here.
- Hybrid (my recommendation for the test, not a published method): (a) flood-fill from the border and from every enclosed region whose colour is within tolerance of B, to get "sure background"; (b) erode a model mask or the key mask to get "sure subject"; (c) in the thin band between, compute alpha with the GEGL formula or with pymatting; (d) un-mix colour (GEGL formula, or pymatting `estimate_foreground_ml`). pymatting: MIT, CPU only for alpha, needs a trimap ("Trimaps ... classify the image into foreground, background and unknown regions"). Source: https://github.com/pymatting/pymatting README (read 30 Sep 2026). Its maintainers say conjugate gradients with incomplete-Cholesky preconditioning "outperforms the other methods by a large margin". Runtime figures are only in charts: NOT EXTRACTED.
- Node route: `sharp` (Apache-2.0, already common in Node) reads raw RGBA; the key and un-mix are simple per-pixel loops. CPU time for 4.5 MP: well under 1 s (my estimate, not measured). RAM: about 4.5 MP x 4 channels x 4 bytes (float) = about 72 MB.
- Licence, watermark, retention, resolution: all PASS (our own code, full resolution, no upscale of a mask). Price: free.
- Quality evidence on AI illustrations: NOT FOUND (no benchmark measured a colour key against learned models on art).
- Fact-bar result: PASS 1-5. SURVIVES.

### F17. Ideogram Remove Background API (new candidate, found during research)

- Endpoint: `POST https://api.ideogram.ai/v1/remove-background`, multipart, "max size 25MB", JPEG/WebP/PNG. "Image links are available for a limited period of time; if you would like to keep the image, you must download it." A safety check can return an empty URL (`is_image_safe: false`). [maker-claim] Source: https://developer.ideogram.ai/api-reference/tools/remove-background.md (read 30 Sep 2026). "Ideogram selects the best model for each tool", so the model is not named.
- Price: "$0.01 per image". Marketing page gives the input limit as 10 MB (the API reference says 25 MB). Claim: it "preserve[s] graphic detail in lettering, badges, illustrations, and print-on-demand artwork" and "outperforms" remove.bg and Photoroom. [maker-claim, no data shown] Source: https://ideogram.ai/features/background-remover/ (read 30 Sep 2026).
- Resolution cap and output size: NOT STATED. Must be tested.
- Retention: signed URL that expires; a script downloads at once. PASS.
- Node: yes (the reference shows a `fetch` example).
- Fact-bar result: PASS 1, 2, 3; rule 4 unverified; price ties Recraft at $0.01. SURVIVES as the second hosted $0.01 option. It is also the only vendor that makes a claim about illustrations.

### F18. Routes that avoid the cut (native alpha or layers)


- GPT Image 2.5 on OpenAI's own API: "to enable transparent backgrounds with either `gpt-image-2.5-sunburst` or `gpt-image-2.5-flare` ... set `background: "transparent"` and use `output_format: "png"` or `"webp"`". Sizes: multiples of 16, "neither edge may exceed 3840 pixels", total pixels up to 8,294,400; "Resolutions above `2560x1440` are experimental." [maker-claim] Source: https://developers.openai.com/api/docs/guides/image-generation (read 30 Sep 2026). The OpenAI cookbook adds: "Prompt instructions take priority over `background="transparent"`" - a prompt that names a background colour can defeat the flag. Source: https://developers.openai.com/cookbook/examples/multimodal/transparent-image-assets-for-campaigns-and-presentations. Transparency was first previewed for gpt-image-2 on 21 Aug 2026 (secondhand, docs.apiyi.com).
  - Consequence: our default model (GPT Image 2.5 Sunburst) CAN return alpha, but only on OpenAI's direct API (or resellers such as Runware), not through Higgsfield. The house rule "ask for one plain background colour" conflicts with this flag. A GPT Image 2.5 figure was NOT FOUND. Runware's guide warns: "A halo that is invisible on a white page is obvious against a dark theme" [maker-claim/opinion]. Source: https://runware.ai/docs/models/openai-gpt-image-2-5-flare/guides/transparent-backgrounds.
  - One practitioner test (JXP, platform chat tool, not the API flag, 1 image, undated) got no alpha (all 255) from a prompt; on a solid green prompt "62.6% of all pixels fell within a tight color-match tolerance" and saw a "faint green-tinted highlight". [opinion, n=1] Source: https://www.jxp.com/gpt-image/blog/gpt-image-2-5-transparent-background.
- Ideogram transparent generation: priced for model 3.0 only ($0.04 Turbo 1X to $0.26 Quality 4X); "Layerize" costs "$0.09 per input image". Updated 22 Jun 2026 (secondhand, https://developer.puter.com/tutorials/ideogram-api-pricing/). No 4.0 transparent route found. Not a cut-out tool for our renders.
- Qwen-Image-Layered: Apache-2.0, decomposes an image into RGBA layers, at 640x640 or 1024x1024; about $0.05 on fal (secondhand). FAILS rule 4 (1024) and rule 5. DROP.

### F19. withoutBG open model

- Licence: Apache-2.0 for withoutBG parts, Meta DINOv3 licence for the backbone. Output "at up to 768px output resolution". About 320 MB weights, about 2 GB RAM, 2-5 s per image. Secondhand search summary of https://withoutbg.com/open-model and https://withoutbg.com/open-model/license (read 30 Sep 2026).
- Fact-bar result: FAILS rule 4 (768 px). DROP. (rembg also wraps withoutBG's paid cloud API; price not checked.)

### F4 (update 2). Recraft output size: a secondhand report says it is downscaled

- Transparify (7 Jun 2026, no author) says: "Remove Background works cleanly at about 1024px on the smaller side; larger images get auto-downscaled and can show border artifacts". No data is given, and Transparify sells a competing tool. [opinion, secondhand] Source: https://transparify.app/blog/recraft-transparent-background.
- Replicate's page for `recraft-ai/recraft-remove-background` says it is "Tuned for AI-Generated Content" and "If you generate images on Replicate with Recraft Remove Background, then you can use the images commercially". [maker-claim] Source: https://replicate.com/recraft-ai/recraft-remove-background.
- Status: Recraft's own Studio doc (F4 update) plus this report make a rule-4 failure LIKELY for 1520-1584 px tall renders. One paid test call must confirm. Until then, treat Recraft as "at risk on rule 4".

### F20. Other evidence on illustration cut-outs (weak)

- "The model is trained exclusively on 1,228 anime images, so performance on non-anime stylized art (Western comic books, cartoons, vector art, 3D renders) is not guaranteed and likely inferior to the original BiRefNet." [opinion] aimodels44, HackerNoon, 21 Jul 2026. Source: https://hackernoon.com/birefnet-toonout-anime-background-removal-with-995percent-accuracy.
- GIGAZINE test of rembg on an AI-generated anime character and photos: u2net "cropping appears somewhat rough"; isnet-anime gives a "slight haze", improvable with `-a` and a threshold; birefnet-general "nearly 1GB ... the quality is higher and more accurate". [opinion, 3 images, no numbers] 10 May 2026. Source: https://gigazine.net/gsc_news/en/20260510-rembg/.
- A practitioner tool, Alpha Chroma Studio, exists for exactly our workflow: "ask the generator for a flat helper color, then remove that known color with controls made for alpha edges, antialiasing, glow, and compression noise". It offers "tolerance, softness, cleanup, despill, choke, feather, and hole fill". Browser tool, no API found. [maker-claim] Source: https://alphachromastudio.com/ (search summary, 30 Sep 2026).
- Systematic test of any tool on flat vector spot art or painterly brushstroke art: NOT FOUND.
- Measured halo/fringe from the background colour, and measured share of partly transparent pixels after a cut-out (as opposed to native generation): NOT FOUND for any tool.

## Fact-bar summary

| Candidate | 1 Licence | 2 Watermark | 3 Retention | 4 2K size | 5 Price / image | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Colour key + edge un-mix (own code) | pass | pass | pass | pass (native size) | free | SURVIVES |
| rembg + BiRefNet / isnet-anime (local) | pass (name the model; default is NC) | pass | pass | pass, mask from 1024 | free | SURVIVES |
| ToonOut (local BiRefNet fine-tune) | pass (MIT) | pass | pass | pass, mask from 1024 | free | SURVIVES |
| BiRefNet_HR / dynamic / lite-2K (local) | pass (MIT) | pass | pass | pass, mask from 2048-2560 | free | SURVIVES (RAM risk) |
| BEN2 base, InSPyReNet (local) | pass | pass | pass | pass | free | option, no art evidence |
| Ideogram remove-background | pass | pass | pass (download) | unverified | $0.01 | SURVIVES (hosted) |
| Recraft removeBackground | pass | pass | pass | at risk (downscale) | $0.01 | at risk |
| Replicate / fal BiRefNet | pass (MIT) | pass | pass (1 h) | pass | ~$0.0014 (Replicate) | hosted fallback |
| Cloudinary e_background_removal | not checked | pass | pass | pass (6144) | free tier? ~$0.03 paid | possible, unconfirmed |
| Photoroom API | pass | sandbox only | pass | pass (6000) | $0.02, $20/mo min | drop (5); hosted reserve, best measured anime result |
| Bria RMBG 2.0 hosted | pass | pass | pass | mask 1024 | $0.018 | drop (5) |
| Bria RMBG-1.4 / 2.0 weights, rembg `bria-rmbg` | FAIL (CC BY-NC) | - | - | - | - | drop (1) |
| remove.bg API | pass | pass | pass | pass (10 MP PNG) | ~$0.18-$1.00 | drop (5) |
| Picsart API | pass | pass | pass | unconfirmed | ~$0.05 | drop (5) |
| Clipdrop API | pass | pass | pass | pass (25 MP) | not published | drop (5) |
| Adobe Firefly Services | enterprise only | - | - | - | contract | drop |
| withoutBG open model | pass | pass | pass | FAIL (768 px) | free | drop (4) |
| Qwen-Image-Layered | pass | pass | pass | FAIL (1024) | ~$0.05 | drop (4, 5) |

## Conclusion: survivors and the free local test

### Survivors (3 + 1 hosted)

1. Deterministic colour key with edge un-mix (own code). Reason: the background colour is known. It works at native size, removes enclosed background (interior holes) by construction, and un-mixes the edge colour (no halo) if the tolerance is right. Risk: a non-flat generated background, and subject pixels near the key colour (pale shadows, painterly blends).
2. BiRefNet family through rembg (local, CPU). Use `birefnet-general-lite` first (213 MiB), then `birefnet-general` (927 MiB). Pair with `-dc` (decontaminate). Risk: interior holes and thin parts (ToonOut's named failures); mask computed at 1024 and stretched.
3. ToonOut (local). The only model with a measured illustration result: 99.5% PA / 95.6% Boundary IoU on 126 anime images, against Photoroom 99.2% / 95.2% and base BiRefNet 95.3% / 88.5% (authors' own test, Sep 2025). Risk: anime-only training.
4. Hosted fallback (costs money; not in the free test): Ideogram remove-background ($0.01, the only vendor that claims illustration quality, size cap not stated) or BiRefNet on Replicate (about $0.0014). Recraft is at risk on rule 4.

A decision outside the tool list: GPT Image 2.5 Sunburst returns real alpha on OpenAI's direct API with `background: "transparent"` (F18). If the founder routes transparent assets there, no cut is needed for GPT renders. The cut is still needed for Grok, Qwen and Ideogram 4.0 renders.

### What a free local test on this machine needs

Test set: 6-9 existing renders from the four models, covering flat vector, painterly and outlined mascot, each with one enclosed background region and one thin outline. Measure on each: (a) interior holes cleared (yes/no), (b) background-colour fringe (mean distance from the key colour of pixels with 0 < alpha < 255, after compositing on black and on white), (c) share of partly transparent pixels in the subject, (d) CPU time and peak RAM (`/usr/bin/time -v`).

Software and downloads (sizes from PyPI and GitHub/HF APIs, 30 Sep 2026; install sizes of dependencies are estimates):

| Test arm | Install | Model files | Peak RAM (estimate) | CPU time (estimate at 2688x1520) |
| --- | --- | --- | --- | --- |
| Colour key + un-mix | nothing: Python 3.12, numpy 2.4 and Pillow 12.3 are already on this machine | none | < 300 MB | < 2 s |
| rembg lite | `pip install "rembg[cpu]"` in a venv (rembg 2.0.85; onnxruntime 1.30 wheel = 22 MiB; plus scipy, scikit-image, pymatting, numba: est. 150-250 MB). Do NOT install `[cli]`: it pulls gradio. | `birefnet-general-lite` 213 MiB; `isnet-anime` 167 MiB | est. 1.5-2.5 GB | about 5-10 s (vision.cpp/ONNX figures at 1024: 4.5-7.0 s on 6 cores) |
| rembg full | same venv | `birefnet-general` 927 MiB | est. 3-5 GB (risky with ~2 GB free now) | about 16-20 s (16.3-18.3 s at 1024 on 6 cores) |
| ToonOut | option A: vision.cpp (MIT, build with cmake) + `BiRefNet-ToonOut-F16.gguf` 419 MiB. Option B: PyTorch CPU wheel (est. ~200 MB) + BiRefNet repo code + `birefnet_finetuned_toonout.pth` 844 MiB | 419 or 844 MiB | est. 2-4 GB | about 16-20 s (same size as BiRefNet Full) |
| Edge refine (optional) | in rembg: `-vm` | ViTMatte small 109 MiB | +0.5-1 GB | slower than `-a` |

Rules for the test run:
- Always pass `-m` / `new_session("<model>")`. The rembg default `bria-rmbg` is CC BY-NC.
- Run one model at a time. Check `free -m` first; about 2 GB was free at research time. Reap finished sessions before the full-size BiRefNet or ToonOut run.
- Total download for all arms: about 1.8 GB with option A for ToonOut (213 + 167 + 927 + 419 MiB + wheels), about 2.2 GB with option B.
- The 2048 checkpoints (BiRefNet_HR 1048 MiB ONNX; BiRefNet_dynamic GGUF 419 MiB) need about 4x the compute of 1024. Test them only if the 1024 masks show stair-steps on 2K edges.
- A paid confirmation of Ideogram and Recraft output size costs $0.02 total. It is NOT part of the free test and needs the founder's approval.

Figures marked "est." are my estimates, not measurements.
