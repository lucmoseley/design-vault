# Research for design-vault#45: prompt dialects for Grok Image 2.0, Qwen Image 3 and Ideogram 4.0 on Higgsfield

⚠ **Bound 2026-09-30 (#49): §9 item 2 is settled. Higgsfield passes an Ideogram 4.0 JSON caption through: one r2 render (`~/higgsfield-calibration-2026-09-30/r2/v13-ideogram-json`) kept its palette and its bbox, though it missed "dusk". §9 item 1 is settled for `QUALITY` only, at $0.10 a render; `TURBO` and `DEFAULT` were not priced.**

Language: ASD-STE100 Simplified Technical English.
Source marks: 1P = the page of the vendor that owns the fact. 2P = a secondary page. LOCAL = a file on this machine.

## 0. Local ground truth (the run of 30 Sep 2026)

- LOCAL `~/higgsfield-calibration-2026-09-30/r{1,2,3}-jobs.json` and the ledgers: the run sent these fields and no others.
  - Qwen (`alibaba/qwen-image-3/text-to-image`): `prompt`, `aspect_ratio: "16:9"`, `resolution: "2k"`. The run did not set `prompt_extend` or `enable_thinking`. Cost: $0.075 (1.200 credits) for each image.
  - Grok (`xai/grok-imagine-image-2.0`): `prompt`, `aspect_ratio: "16:9"`, `resolution: "2k"`, `quality: "medium"`. Cost: $0.080 (1.280 credits) for each image.
  - Ideogram (`ideogram/v4.0`): `prompt`, `aspect_ratio: "16:9"`, `rendering_speed: "QUALITY"`. No `resolution` field. Cost: $0.100 (1.600 credits) for each image.
- LOCAL `report.md`: output sizes were Grok 2816x1584, Ideogram 2560x1440, Qwen 2048x1152.
- LOCAL `report.md`: Qwen kept the upper half as an empty sky (r2). Qwen also added objects and text that the prompt did not ask for (fish, stars, a second manta, "THE YARD"). The report gives the prompt rewrite as the probable cause. This is an inference, not a measured fact: the ledger does not keep a rewritten prompt.
- LOCAL `report.md`: Grok gave the only mascot in exactly three colours (r3). Grok put soft cloud strokes in the "empty" sky (r2).
- LOCAL `report.md`: Ideogram gave a grainy, muted, editorial look. Its colours were duller than the prompt asked (teal, not ink-blue).
- LOCAL `plugin/skills/design-round/scripts/higgsfield.js`: `--set <field>=<value>` adds a field to the request body. A value that parses as JSON goes as JSON. So `--set prompt_extend=false` sends the boolean `false`, and `--set seed=42` sends a number.

## 1. Higgsfield: the price list (fetched 30 Sep 2026)

Source: 1P https://dash.higgsfield.ai/api/v2/pricing/models/ (pages 1 to 4, JSON).

- `xai/grok-imagine-image-2.0` ("Grok Imagine 2.0", released 2026-08-01): two price options. `1k` + `quality: low` = $0.04. `2k` + `quality: medium` = $0.08. Operation types: `text2image`, `image_edit`.
- `alibaba/qwen-image-3/text-to-image`: `1k` = $0.04, `2k` = $0.075. The sibling mode `alibaba/qwen-image-3/edit` has the same prices.
- `ideogram/v4.0` (released 2026-06-01): one option only, $0.03, qualifier "exact". The list has no price for each `rendering_speed`. The run of 30 Sep got $0.10 from the estimate endpoint for `QUALITY` (LOCAL ledger). The estimate endpoint (`POST /estimate/<endpoint id>`) is the only source for these prices.

## 2. Higgsfield: the model pages (fetched 30 Sep 2026)

Higgsfield's docs index says: the model page is the authority for the request schema, and `/docs/openapi.json` is only supplementary. 1P https://docs.higgsfield.ai/docs/llms.txt

### 2.1 Qwen Image 3, text to image

Source: 1P https://docs.higgsfield.ai/docs/models/qwen-image-3/text-to-image (read in full, as `.md`).

All fields of the request body (the JSON schema has `"additionalProperties": false`, so the API refuses any other field):

| Field | Type | Default | Values / notes |
|---|---|---|---|
| `prompt` | string, required | none | Chinese or English. `minLength: 1`. No character maximum. "Alibaba recommends at most 4,500 tokens" (advisory). |
| `negative_prompt` | string | none | "Content, styles, or artifacts to avoid in the output." |
| `seed` | integer | none | 0 to 2147483647. "for similar, reproducible results". |
| `resolution` | string | `1k` | `1k`, `2k`. Both give PNG. "2k square maps to 1536 by 1536 pixels, not 2048 by 2048." |
| `aspect_ratio` | string | `1:1` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `7:9`, `9:7`, `9:16`, `16:9`, `21:9`. |
| `prompt_extend` | boolean | `true` | "Improve the prompt before generation. Required when thinking mode is enabled." |
| `enable_thinking` | boolean | `true` | "Use model reasoning to improve image quality. Requires prompt enhancement." |
| `prompt_extend_mode` | string | `direct` | `direct`, `agent`. "agent enhancement is text-to-image only." |

- The usage note says: "enable_thinking defaults to true and requires prompt_extend=true. **Set both to false to disable enhancement.**" So Higgsfield documents this pair as the way to stop the rewrite.
- The schema has a rule: if the request sends `enable_thinking: true`, it must also send `prompt_extend: true`.
- There is **no `watermark` field** on Higgsfield's Qwen endpoints.
- There is no reference image on the text-to-image endpoint ("No reference images are accepted by this endpoint"). There is no palette field.
- The edit endpoint (`alibaba/qwen-image-3/edit`) takes `image_urls`, 1 to 3 public URLs, required. It has the same `seed`, `negative_prompt`, `prompt_extend`, `enable_thinking` fields. There `prompt_extend_mode` accepts only `direct`. 1P https://docs.higgsfield.ai/docs/models/qwen-image-3/edit

With `--set` (LOCAL `higgsfield.js`): `--set prompt_extend=false --set enable_thinking=false --set seed=7 --set 'negative_prompt=text, letters, watermark'`.

### 2.2 Ideogram 4.0

Source: 1P https://docs.higgsfield.ai/docs/models/ideogram-4/generate (read in full, as `.md`).

All fields of the request body (`"additionalProperties": false`):

| Field | Type | Default | Values / notes |
|---|---|---|---|
| `prompt` | string, required | none | 2 to 2048 characters. |
| `image_url` | string (uri) | none | One image. "Omit image_url for text-to-image; provide image_url for remix/editing." |
| `image_weight` | integer | none | 1 to 100. "applies to editing requests only". |
| `aspect_ratio` | string | `1:1` | 23 values, including `16:9`, `22:9`, `23:9`, `3:1`. |
| `rendering_speed` | string | `DEFAULT` | `TURBO`, `DEFAULT`, `QUALITY` (case-sensitive). |

- Higgsfield's Ideogram endpoint has **no** `magic_prompt`, `style_type`, `style_preset`, `color_palette`, `negative_prompt`, `seed`, `num_images`, `resolution` or style-reference field. So none of Ideogram's own palette or style controls can go through Higgsfield.
- The one image input (`image_url`) is for remix/edit, not a style reference. The page does not say that it transfers a style only.
- The page does not say whether Higgsfield turns Ideogram's own "magic prompt" on or off. This is unknown.

### 2.3 Grok Image 2.0

Source: 1P https://docs.higgsfield.ai/docs/models/grok-image-2/generate-and-edit (read in full, as `.md`).

| Field | Type | Default | Values / notes |
|---|---|---|---|
| `prompt` | string, required | none | No length limit given. |
| `quality` | string | `medium` | `low`, `medium` only. "quality accepts low or medium only". |
| `resolution` | string | `1k` | `1k`, `2k`. |
| `aspect_ratio` | string | `auto` | `auto`, `1:1`, `1:2`, `2:1`, `3:2`, `2:3`, `4:3`, `3:4`, `16:9`, `9:16`. |
| `image_urls` | array of uri | none | 0 to 10 "ordered public image reference URLs". Omit for generation. Supply for editing. |

- "The request produces one image; no batch count is declared." So there is no `n` field.
- There is no `seed`, `negative_prompt`, `style` or palette field on the page. This schema does not show `additionalProperties: false`, so the API possibly accepts other fields.
- "Reference images may be resized during preprocessing before submission."

## 3. Qwen Image 3: the maker's docs (Alibaba Model Studio)

### 3.1 Facts from Alibaba (1P)

Source A: 1P https://www.alibabacloud.com/help/en/model-studio/qwen-image-generation-and-editing-api-reference ("Last Updated: Sep 28, 2026"; read in full as text).
Source B: 1P https://www.alibabacloud.com/help/en/model-studio/text-to-image ("Key capabilities" part read in full; the example gallery sampled).
Source C: 1P https://www.alibabacloud.com/help/en/model-studio/text-to-image-prompt (read in full).

- Models: `qwen-image-3.0-pro` (flagship) and `qwen-image-3.0` ("balances quality and speed"). Source A. Higgsfield's page does not say which of the two its endpoint calls. This is unknown.
- `prompt`: "Both Chinese and English are supported. Recommended maximum: 4,500 tokens." Source A.
- `negative_prompt`: "describes content you do not want to appear in the image". Source A gives no length limit. Source B: "Describes what to exclude from the image, such as "blurry" or "extra fingers." This parameter helps refine the output quality."
- `prompt_extend`: "Whether to enable intelligent prompt rewriting. Default: true (recommended). When enabled, the model optimizes the positive prompt ... which significantly improves results for simple descriptions." Source A.
- Source B gives the rule for when to turn it off (this is the nearest 1P text to "literal adherence"): "Enable this feature for brief or general prompts to significantly improve image quality. **Disable this feature if you need precise control over image details, have provided a comprehensive prompt, or if response latency is a concern.** To disable it, set the prompt_extend parameter to false." It also says: "Enabling this feature adds 3 to 5 seconds to the generation time, as a large model is used to rewrite the prompt."
- `prompt_extend_mode`: `direct` = "Direct Prompt Enhancement (DPE), suitable for most scenarios"; `agent` = "Agent Prompt Enhancement (APE), provides more refined rewriting. Only supports text-to-image (T2I)". Source A.
- `enable_thinking`: "Enables thinking mode. The default is true. This enhances model reasoning to improve image quality, but increases generation time. It requires prompt_extend=true." Source A.
- `seed`: 0 to 2147483647. "Use a fixed seed for reproducible results." Source A.
- `watermark`: boolean, "Default: false." Source A. Alibaba has this field, but Higgsfield does not (section 2.1).
- The DashScope response has `rewrite_status` ("The prompt rewriting status"). Source A does not document a field that returns the rewritten prompt. Higgsfield's response has only `images` (section 2).
- Size: at 2K, Alibaba lists 16:9 as 2688*1536. Source B. The run of 30 Sep got 2048x1152 from Higgsfield's `2k` tier (LOCAL).
- Source B: "For best results, use a structured prompt." Source C gives the formula "Subject + Setting + Style + Camera + Atmosphere + Detail modifiers". But Source C says that it is written for "Wan - text-to-image V2", not for Qwen Image 3. Use it only as a general guide.
- Alibaba's pages that I read do not say how the model treats hex codes against colour names. They do not say how to ask for an empty area. I found no 1P statement on these two points.

### 3.2 Secondary guidance (2P)

Source D: 2P https://runware.ai/docs/models/alibaba-qwen-image-3-0/guides/prompting (read in full).
Source E: 2P https://runware.ai/docs/models/alibaba-qwen-image-3-0/guides/prompt-extension (sampled: key sentences only).

- "an LLM rewrites your prompt before the model sees it unless you switch that off." Source D.
- "Set promptExtend to false while you iterate. Otherwise you are tuning a prompt the model never sees, and two runs of the same wording will not match." Source D.
- Negative prompt: "It trims a render rather than redirecting it, so treat it as a cleanup pass over a prompt that already works." Source D.
- "Say "no text" when you don't want any. The model renders lettering readily." Source D. This agrees with the run of 30 Sep ("THE YARD", "ROOM 2B").
- All examples in Source D are full descriptive sentences in layers: the subject, then the arrangement, then the light, then the style and palette words, then "no people, no text".
- With the rewrite on, a fixed seed does not repeat the image: "it produces a fresh prompt on every call and the seed then locks the noise for a description that keeps moving." `agent` "travels further from what you typed" than `direct`. Source E.

### 3.3 Conclusion for Qwen

- Prompt shape: full descriptive sentences, in layers. The length limit is large (about 4,500 tokens, advisory).
- For brand art with a fixed palette and a fixed empty area, send `prompt_extend=false` and `enable_thinking=false`.
- Use `negative_prompt` for text and clutter ("text, letters, signage, watermark, extra creatures"). Also say "no text" in the prompt (2P).
- Send a `seed`, and keep it. With the rewrite off, the seed repeats the image (2P).
- No palette field and no reference image on the text-to-image endpoint. Colours go in the prompt as words. The hex behaviour is not documented (no 1P source).
- Empty area: the run of 30 Sep kept the empty sky best with the rewrite on (LOCAL). It is not known whether the rewrite helped or not. Test once with the rewrite off.

## 4. Ideogram 4.0: the maker's docs

Sources:
- F: 1P https://developer.ideogram.ai/api-reference/generate-images/generate-v4.md (Ideogram's own API, "Generate with Ideogram 4.0"; read in full).
- G: 1P https://docs.ideogram.ai/using-ideogram/getting-started/prompting-guide/4.-json-prompting-ideogram-4.0 (read in full).
- H: 1P https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md (the open-weight model's prompting guide; read in full).
- I: 1P https://ideogram.ai/blog/ideogram-4.0/ (technical blog; the parts on speed presets, JSON and palette read, benchmarks sampled).
- J: 1P https://docs.ideogram.ai/using-ideogram/getting-started/prompting-guide/4-handling-negatives.md (read in full).
- K: 1P https://docs.ideogram.ai/using-ideogram/getting-started/prompting-guide/3-prompt-structure.md (read in full).
- L: 2P https://developer.puter.com/tutorials/ideogram-api-pricing/ (prices; read through WebFetch summary).

### 4.1 The model is trained on JSON captions

- "Ideogram 4 is trained exclusively on **structured JSON captions**." H. "Natural language prompts still work well — but providing a JSON object that follows the caption schema gives you capabilities that go far beyond what natural language can express." G.
- The caption has three top-level keys: `high_level_description` (string, "strongly recommended"), `style_description` (object), `compositional_deconstruction` (object, required, with `background` and `elements`). H.
- `style_description` keys, in this strict order for art that is not a photo: `aesthetics`, `lighting`, `medium`, `art_style`, `color_palette`. `medium` examples: `"illustration"`, `"painting"`, `"graphic_design"`. `art_style` example: "flat vector illustration, bold outlines". H.
- `color_palette`: "Hex color codes that steer the image's dominant colors. Up to 16 entries." Per element: "Up to 5 hex entries." Hex must be uppercase `#RRGGBB`. H, G. Blog: palette conditioning steers "the dominant colors directly, not through descriptive language." I.
- Palette tips: "Include background colors in the palette if you want to control the overall tone". "Include contrast pairs — both highlight and shadow colors". G, H.
- `bbox`: `[y_min, x_min, y_max, x_max]` in 0 to 1000 normalized coordinates, origin at top-left. "[0, 0, 500, 1000] places an element in the top half of the image." "if you omit them, the model will place the element freely". G. "The model honors the boxes". I.
- When to use JSON: G's table recommends JSON for "Design work, posters, branded graphics", "Specific color palette" and repeatable layouts. G says the gain of JSON is "not quality, but repeatability and compositional control."
- Key order matters: "The model was trained on JSON with a consistent key order, so maintaining it improves generation quality." H.

### 4.2 Magic Prompt

- On Ideogram's own API there are two prompt fields. `text_prompt`: "When supplied, magic-prompt is enabled automatically." `json_prompt`: "When supplied, magic-prompt is disabled and the structured prompt is consumed by the diffusion model directly." They are mutually exclusive. F.
- On the ideogram.ai web app, a JSON prompt turns Magic Prompt off automatically ("Magic Prompt : OFF (automatically turned off when using JSON format for Ideogram 4.0)"). G.
- The response has `prompt`: "The prompt used for the generation. This may be different from the original prompt." And `seed` (returned, not sent). F. Higgsfield's response gives only `images` (section 2).

### 4.3 Fields that Ideogram 4.0 does not have

- Ideogram's own v4 endpoint has these request fields only: `text_prompt`, `json_prompt`, `resolution` (1K and 2K presets, 38 values), `rendering_speed`, `enable_copyright_detection`. F. So v4 has **no** `style_type`, no style presets, no `negative_prompt`, no request `seed`, no top-level `color_palette` and no style-reference image. The palette lives inside the JSON caption. By contrast, Ideogram's own **3.0** endpoint has `seed`, `magic_prompt`, `negative_prompt`, `color_palette` ("ColorPaletteWithPresetNameOrMembers"), `style_codes`, `style_type`, `style_preset` and `style_reference_images`. 1P https://developer.ideogram.ai/api-reference/generate-images/generate-v3.md (field list read).
- Negative prompt: Ideogram tells you to "Turn negatives into positives": "Don't write "no people in the room" — write "an empty room with chairs neatly arranged"". "Ideogram, like many text-to-image AIs, struggles with understanding negation." J.

### 4.4 rendering_speed

- Ideogram's API: `rendering_speed` enum `FLASH`, `TURBO`, `DEFAULT`, `QUALITY`; default `DEFAULT`. "rendering_speed=FLASH is coming soon; requests with rendering_speed=FLASH currently return a 400." F. Higgsfield offers `TURBO`, `DEFAULT`, `QUALITY` (section 2.2).
- The blog links the tiers to sampler presets: `V4_QUALITY_48` "runs 45 steps at gw=7 followed by 3 polish steps at gw=3"; "The shorter V4_DEFAULT_20 and V4_TURBO_12 presets follow the same shape with two and one polish steps respectively. The polish tail tightens fine detail without over-saturating the global composition." I. The preset names show 48, 20 and 12 steps. The naming of a hosted `rendering_speed` to these open-weight presets is my inference from the shared names. Ideogram does not state it on the API page.
- The maker does not publish a side-by-side look difference between DEFAULT and QUALITY. More steps usually give finer detail. That is general knowledge, not an Ideogram statement.
- Prices on Ideogram's own API (2P, L, which cites ideogram.ai/api-pricing): Turbo $0.03, Default $0.06, Quality $0.10. I could not read the 1P price page: https://ideogram.ai/api-pricing redirects to https://ideogram.ai/pricing/?pricing_tab=api, and the API prices load by script, so the fetched HTML has no figures.
- On Higgsfield: the price list shows one Ideogram price, $0.03 "exact" (section 1). The estimate for QUALITY was $0.10 (LOCAL). The $0.03 figure agrees with Ideogram's **Turbo** price (2P), not with a Default price. So the claim "DEFAULT = $0.03" in the question is NOT confirmed.

### 4.5 What Higgsfield passes through

- Higgsfield's field is one string, `prompt`, 2 to 2048 characters (section 2.2). The page does not say whether Higgsfield sends it to Ideogram as `text_prompt` or as `json_prompt`, or whether it detects JSON the way the web app does. This is unknown. If it goes as `text_prompt`, Magic Prompt always runs on Higgsfield, and a JSON caption in the string gets rewritten.
- Test to settle it (one render, $0.03 to $0.10): send a compact JSON caption (under 2048 characters) as `prompt`, with a `color_palette` and a `bbox` for the empty area. If the output keeps the hex colours and the empty box, Higgsfield passes JSON through.
- The run of 30 Sep sent plain text. So Magic Prompt (or Higgsfield's own handling) possibly caused the colour drift (teal, not ink-blue). This is a hypothesis only.
- Higgsfield's `image_url` + `image_weight` are for remix. Ideogram's own API has a separate "Remix with Ideogram 4.0" endpoint (F's index). I did not read that page.

### 4.6 Conclusion for Ideogram

- Best path for a fixed palette and a fixed empty area: a compact JSON caption in `prompt`, with `color_palette` as uppercase hex and a `bbox` layout. This depends on the pass-through test in 4.5.
- Fallback: plain text in the image-summary-first order of K (summary sentence, subject, setting, lighting and palette, composition, finish). State every exclusion as its positive opposite (J). Name the colours in words.

## 5. Grok Image 2.0: the maker's docs (xAI)

Sources:
- M: 1P https://docs.x.ai/developers/model-capabilities/images/generation.md (read in full).
- N: 1P https://docs.x.ai/developers/rest-api-reference/inference/images.md (generation part read in full; edit part sampled).
- O: 1P https://docs.x.ai/developers/migration/imagine-image-quality-nov-2.md (read in full).
- P: 1P https://docs.x.ai/developers/model-capabilities/imagine.md, .../images/editing.md, .../images/multi-image-editing.md, .../pricing.md (sampled).
- Q: 1P https://x.ai/news/grok-imagine-image-2 (launch post, 7 Aug 2026; read in full).
- R: 2P https://runware.ai/docs/models/xai-grok-imagine-image-2-0/guides/prompting (read the first half).

### 5.1 quality

- xAI: "Allowed values are `low`, `medium`, and `auto`. When omitted, the default is `auto` ... Auto currently uses `low` for image generation and `medium` for image editing. Images are billed at the quality they are served at." "The parameter is only supported for `grok-imagine-image-2.0`." M.
- "`medium` spends more compute on each image for finer detail; choose it where output quality matters more than cost." O.
- Higgsfield offers only `low` and `medium`, and its default is `medium` (section 2.3). Always send `quality: medium` explicitly. xAI's own list price is "$0.04 / image" (P, pricing page). The xAI page does not give a separate `medium` or `2k` price.

### 5.2 Other fields

- xAI generation request fields: `aspect_ratio`, `model`, `n` ("Number of images to be generated", 1 to 10), `prompt`, `quality` (M), `resolution` (`1k`, `2k`, `1.5k`), `response_format`, `storage_options`, `user`. N.
- There is **no** `seed`, `negative_prompt`, `style` or palette field on xAI's generation endpoint. N, M.
- Higgsfield's aspect ratios are 10; xAI also offers `21:9`, `5:2`, `19.5:9`, `20:9` (M), but Higgsfield does not list them.
- Reference images: xAI's editing endpoint takes one `image` or `images` (multi-reference) and says "Use up to five source images". "refer to them as <IMAGE_0>, <IMAGE_1>, etc. in the prompt." N, P. Higgsfield allows up to 10 `image_urls` (section 2.3). xAI describes style transfer by prompt: "Transform existing images by describing the desired aesthetic in your prompt." P (editing page).

### 5.3 Prompt revision

- xAI's API rewrites the prompt before it draws. The usage block in the response counts "Prompt text tokens consumed by the prompt-rewriting (upsampler) LLM", "Rewritten-prompt text tokens generated by the prompt-rewriting (upsampler) LLM" and "Reasoning (thinking) tokens generated by the prompt-rewriting (upsampler) LLM". N.
- xAI's current 1P pages have **no field to turn the rewrite off**, and the 1P response schema has **no `revised_prompt` field**. A 2P search summary says a `revised_prompt` output exists; I did not find it on a 1P page.
- Higgsfield's Grok response gives only `images` (section 2.3). So on Higgsfield you cannot see the rewritten prompt.

### 5.4 Prompt shape

- xAI's launch post: "2.0 follows instructions closely, down to the details. It plans typography and layout the way a designer would". It has a "Mascot Maker" and an "Icon Maker" template in the consumer app. Q. xAI publishes no prompting guide for the API (no prompting page in https://docs.x.ai/llms.txt).
- 2P (R): full descriptive sentences, in five layers: "the subject, the setting, the composition, the light, and the finish". "The finish clause sets the register, editorial photography versus product render versus flat illustration, and skipping it hands the look to the model." "There is no character ceiling to worry about in practice, but detail past a point competes with itself".
- Colour names against hex: no 1P or 2P statement found.
- Empty area: no 1P statement. In the run of 30 Sep, Grok put soft cloud strokes in the sky that the prompt asked to be "plain empty" (LOCAL). With no negative prompt, state the empty area as a positive surface, and give it a size and a position.

### 5.5 Conclusion for Grok

- Send `quality: medium`, `resolution: 2k`, `aspect_ratio: 16:9`. There is nothing else to set for generation on Higgsfield.
- Write full sentences in five layers, with the style ("flat vector illustration") in the finish clause. Give the colour count and each colour in words.
- The rewrite is always on and cannot be turned off. So keep every constraint explicit and positive, and repeat the key one (the empty area) in the composition clause.
- A palette swatch can go in `image_urls` as a reference, but then the request becomes an edit (xAI's edit endpoint). Its effect on colour is not documented. Test before use.

## 6. Question 5: reference image or palette as data, on Higgsfield

| Model on Higgsfield | Palette as data | Reference image | Source |
|---|---|---|---|
| Qwen Image 3 text-to-image | No | No ("No reference images are accepted by this endpoint") | 1P Higgsfield 2.1 |
| Qwen Image 3 edit (`alibaba/qwen-image-3/edit`) | No | Yes, `image_urls`, 1 to 3, required (an edit, not a style reference) | 1P Higgsfield 2.1 |
| Ideogram 4.0 | No field. Possibly a `color_palette` inside a JSON caption sent as `prompt`, if Higgsfield passes JSON through (not tested) | `image_url` (one) + `image_weight`, for remix/edit | 1P Higgsfield 2.2; 1P Ideogram 4.1 |
| Grok Image 2.0 | No | `image_urls`, 0 to 10 on Higgsfield (xAI says up to 5); this makes the request an edit | 1P Higgsfield 2.3; 1P xAI 5.2 |

Of the three makers, only Ideogram takes a palette as data (hex in the JSON caption). Recraft (in `prompts.md`) is still the only model with a palette field on Higgsfield.

## 7. Summary of the prompt shape (question 1)

| | Qwen Image 3 | Ideogram 4.0 | Grok Image 2.0 |
|---|---|---|---|
| Form | Full sentences, in layers (2P); "structured prompt" (1P, Alibaba) | JSON caption is native (1P); plain text goes through Magic Prompt (1P) | Full sentences, five layers (2P) |
| Length limit | Advisory 4,500 tokens (1P) | 2 to 2048 characters on Higgsfield (1P) | None given (1P) |
| Colours | Words. Hex not documented | Uppercase hex in `color_palette`, up to 16 (1P, JSON only) | Words. Hex not documented |
| Negative prompt | Yes, `negative_prompt` (1P) | No. "Turn negatives into positives" (1P) | No field (1P) |
| Rewrite | `prompt_extend` + `enable_thinking`, both default on; "Set both to false to disable enhancement" (1P) | Magic Prompt on for plain text, off for JSON (1P, Ideogram API); Higgsfield handling unknown | Always on, no switch (1P, usage fields) |
| Seed | Yes, `seed` (1P) | No request seed on v4 (1P) | No (1P) |
| Empty area | Kept it best on 30 Sep (LOCAL); no 1P guidance | `bbox` places elements; describe the empty background as a positive surface (1P) | No guidance; drew clouds in the "empty" sky on 30 Sep (LOCAL) |

## 8. DRAFT dialects for `prompts.md`

The drafts use the placeholder palette of `prompts.md`: `[INK] #1A1A2E · [PRIMARY] #3A7CA5 · [ACCENT] #E07A5F · [GROUND] #F4F1DE · [SOFT] #81B29A`.

### DRAFT — Qwen Image 3

On Higgsfield (`alibaba/qwen-image-3/text-to-image`), switch off the prompt rewrite with `--set prompt_extend=false --set enable_thinking=false`: with the rewrite on, it adds things nobody asked for, such as extra creatures and signs, and the same seed does not give the same image twice. Write full sentences in layers, from the subject, to the layout and the empty area, to the palette in words, to the style. Put what must not appear in `negative_prompt`, always including text, and keep a `seed` so a winner can be re-run. It takes no palette data and no reference image, so name each colour in words.

```text
A [STYLE: flat vector illustration / soft painterly illustration] in exactly [N] colours: [INK IN WORDS], [PRIMARY IN WORDS], [ACCENT IN WORDS] and [GROUND IN WORDS]. [SUBJECT] [ACTION] in [SETTING], seen from [ANGLE]. The subject sits in the [LOWER THIRD / RIGHT HALF]; the [UPPER HALF / LEFT HALF] is one plain, unbroken [GROUND IN WORDS] [SKY / WALL / FIELD] with nothing in it. [EACH REMAINING SURFACE, STATED AS WHAT IT IS]. Clean edges, flat fills, no texture.

negative_prompt: text, letters, words, signage, logos, watermark, extra animals, stars, bubbles, gradients, photographic detail
--set prompt_extend=false --set enable_thinking=false --set seed=[N] --resolution 2k --aspect-ratio 16:9
```

### DRAFT — Ideogram 4.0

Ideogram 4.0 is trained on JSON captions, and its maker recommends JSON for brand graphics and a set palette: the palette goes in as uppercase hex, up to 16 colours, and a `bbox` pins each element in place, so the empty area stays where you put it. Before relying on this through Higgsfield, test one render at the cheapest `rendering_speed` to confirm that a JSON caption sent as `prompt` keeps its hex colours and layout; if it does not, write plain sentences in the maker's order, starting with a one-sentence summary of the whole image. Ideogram ignores negatives ("no clouds"), so describe the positive opposite ("a plain unbroken sky"). On Higgsfield it takes no negative prompt, no seed, no style preset and no palette field. Price each `rendering_speed` with `--estimate` before choosing one; `QUALITY` cost $0.10 on 30 Sep.

```text
{"high_level_description":"A [STYLE] of [SUBJECT] [ACTION] in [SETTING], the [UPPER HALF] left as plain open [SKY] for a headline.","style_description":{"aesthetics":"[3-5 MOOD WORDS], flat, restrained","lighting":"[LIGHT, e.g. soft even dusk light, no hard shadows]","medium":"illustration","art_style":"[e.g. flat vector illustration, clean geometric shapes, flat colour fills]","color_palette":["#1A1A2E","#3A7CA5","#E07A5F","#F4F1DE"]},"compositional_deconstruction":{"background":"[THE WHOLE BACKGROUND AS WHAT IT IS, e.g. A smooth, unbroken #F4F1DE sky fills the top half; a flat #3A7CA5 sea fills the bottom half.]","elements":[{"type":"obj","bbox":[[Y_MIN],[X_MIN],[Y_MAX],[X_MAX]],"desc":"[SUBJECT, ITS SHAPE AND POSE, ITS COLOURS IN WORDS]"}]}}

--set rendering_speed=[TURBO | DEFAULT | QUALITY] --aspect-ratio 16:9    (no resolution field; keep the caption under 2,048 characters, hex in upper case, keys in this order)
```

`bbox` is `[y_min, x_min, y_max, x_max]` on a 0-1000 grid from the top-left; `[550,300,950,700]` keeps the subject in the lower half, centred.

### DRAFT — Grok Image 2.0

Always send `--set quality=medium` with `--resolution 2k` on Higgsfield. xAI's own API defaults to the lower quality, while Higgsfield's page says medium, so set it rather than trust either default. xAI always rewrites the prompt and there is no switch to stop it, and it takes no negative prompt or seed, so every constraint must be a stated, positive fact. Write full sentences in five layers: subject, setting, composition (with the empty area given its size and place), light, then the finish, which names the style and the exact colour count. On 30 Sep it was the only model that kept to exactly three colours, but it drew soft clouds into an "empty" sky, so name the empty surface twice.

```text
[SUBJECT] [ACTION] in [SETTING]. Composition: the subject fills the [LOWER THIRD / RIGHT HALF], seen from [ANGLE]; the [UPPER HALF] is a single flat [GROUND IN WORDS] [SKY / WALL] with no clouds, marks or texture, left clear for a headline. Light: [e.g. flat, even, shadowless]. Finish: [STYLE: flat vector illustration with clean edges and flat fills], exactly [N] colours: [INK IN WORDS], [PRIMARY IN WORDS], [ACCENT IN WORDS] and [GROUND IN WORDS]; the [UPPER HALF] stays plain [GROUND IN WORDS].

--set quality=medium --resolution 2k --aspect-ratio 16:9
```

(Note on the Grok template: "no clouds, marks or texture" is a negative. It is kept because Grok has no negative field and the 30 Sep run drew clouds. If a test shows that it adds clouds, change it to the positive form only.)

## 9. Open items (each needs a test or a key)

1. Ideogram price for each `rendering_speed` on Higgsfield. The price list shows only $0.03. Run `node plugin/skills/design-round/scripts/higgsfield.js --estimate` once for `TURBO`, `DEFAULT`, `QUALITY` (free, needs `HIGGSFIELD_API_KEY`).
2. Does Higgsfield send a JSON caption to Ideogram as `json_prompt` (Magic Prompt off)? One render with the DRAFT Ideogram template settles it.
3. Qwen with `prompt_extend=false` and `enable_thinking=false`: does it still keep the empty sky as well as on 30 Sep? One render of the r2 prompt.
4. Grok `image_urls` limit: Higgsfield says 10, xAI says 5.
5. Which Qwen model Higgsfield calls (`qwen-image-3.0` or `qwen-image-3.0-pro`). Higgsfield's page does not say.
6. Qwen size: Higgsfield's `2k` gave 2048x1152 for 16:9; Alibaba's own 2K 16:9 is 2688*1536. Higgsfield gives no way to ask for the larger size.

**Bound:** Read in full: Higgsfield's model pages for Qwen Image 3 text-to-image and edit, Ideogram 4.0 generate, and Grok Image 2.0 generate-and-edit (as `.md`); Higgsfield's price list (all 4 JSON pages; only the three models' entries examined); Alibaba's Qwen Image 3.0 API reference; Alibaba's text-to-image prompt guide (which says it is for Wan V2); Ideogram's v4 generate API page (`.md`); the Ideogram 4 open-source prompting guide; Ideogram's JSON prompting, prompt structure and handling-negatives pages; xAI's image generation page, migration guide and Imagine Image 2.0 launch post; the local `prompts.md`, `higgsfield.js`, `report.md`, the three jobs files and the three ledgers. Sampled only: Alibaba's text-to-image overview (the key capabilities part); Ideogram's 4.0 blog (the speed presets, JSON and palette parts); Ideogram's v3 generate page (the field list); xAI's REST images reference (the edit part), and its Imagine overview, editing, multi-image editing and pricing pages; Runware's Qwen prompt-extension guide (key sentences) and Grok prompting guide (first half). 2P used as-is: Runware's Qwen prompting guide (read in full) and Puter's Ideogram price page (WebFetch summary). Could not read: the 1P Ideogram API price page (https://ideogram.ai/api-pricing), whose prices load by script. Not done: Higgsfield's `--estimate` for each Ideogram tier (no API key in this session), and no test render.
