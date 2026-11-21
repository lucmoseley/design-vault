# Research 44 — fact bar for Grok Image 2.0, Qwen Image 3 and Ideogram 4.0 on Higgsfield

Question: lucmoseley/design-vault#44. Date of all reads: 30 Sep 2026.
Fact bar: `plugin/skills/design-round/references/roster.md` lines 5-10.
Key: 1P = the vendor's own page or file. 2P = a secondary source.

## Findings

### F1 — Embedded provenance in the nine local files (1P: the files)

Method: a python `struct` walk of every PNG chunk. `exiftool` is not installed.

| File | Size | Chunks (in order) | Bytes after IEND |
|---|---|---|---|
| r1/v2-qwen.png | 2048x1152 RGB | IHDR, iTXt (630 B, XMP), IDAT x20, IEND | 0 |
| r2/v2-qwen.png | 2048x1152 RGB | IHDR, iTXt (630 B, XMP), IDAT x45, IEND | 0 |
| r3/v2-qwen.png | 2048x1152 RGB | IHDR, iTXt (630 B, XMP), IDAT x12, IEND | 0 |
| r1/v3-grok.png | 2816x1584 RGB | IHDR, IDAT x38, IEND | 0 |
| r2/v3-grok.png | 2816x1584 RGB | IHDR, IDAT x99, IEND | 0 |
| r3/v3-grok.png | 2816x1584 RGB | IHDR, IDAT x20, IEND | 0 |
| r1/v4-ideogram.png | 2560x1440 RGB | IHDR, IDAT x662, IEND | 0 |
| r2/v4-ideogram.png | 2560x1440 RGB | IHDR, IDAT x588, IEND | 0 |
| r3/v4-ideogram.png | 2560x1440 RGB | IHDR, IDAT x133, IEND | 0 |

- No file has a tEXt, zTXt, eXIf, caBX (C2PA / JUMBF) chunk or trailing data.
- Grok and Ideogram files carry no metadata at all.
- Each Qwen file carries one XMP packet with the Chinese national AI-content label (namespace `http://www.tc260.org.cn/ns/AIGC/1.0/`). The r1 packet, in full:
  `<TC260:AIGC>{"Label":"1","ContentProducer":"001191330106MA2CFLDG4R10001","ProduceID":"R-H2gCrEzImG2H_v01Cp6vCw","ReservedCode1":"L-8d5e…b733","ContentPropagator":"001191330106MA2CFLDG4R10001","PropagateID":"R-H2gCrEzImG2H_v01Cp6vCw","ReservedCode2":"L-8d5e…b733"}</TC260:AIGC>`
  `Label":"1"` marks the file as AI-generated. This is an implicit (metadata) label, not a visible mark. A metadata strip (for example a re-save through an image tool) removes it.
- Note: these files passed through Higgsfield. The chunk list shows what Higgsfield delivers, not what each maker emits at source. Higgsfield kept the Qwen XMP, so it probably does not strip metadata; Grok and Ideogram then probably emit none through this route.

### F2 — Visible marks in the nine local files (1P: the files)

Method: I viewed a 3x3 contact sheet of the nine pictures, and a sheet of the four corners of each file (400x200 px crops at full resolution).
- No visible logo, text badge or corner mark is in any of the nine files.
- The only text in a picture is content the model drew as part of the scene (Qwen r2: a "THE YARD" sign). That is not a watermark.

### F3 — Grok Image 2.0: xAI (now "SpaceXAI") terms (1P, read through the Wayback Machine)

Access note: x.ai returns HTTP 403 to WebFetch and to curl. I read the Wayback Machine copies captured on 28 Sep 2026 (read 30 Sep 2026).
- Enterprise terms: https://x.ai/legal/terms-of-service-enterprise, "Last Updated: August 14, 2026" (capture `web.archive.org/web/20260928102641/...`).
- Acceptable Use Policy: https://x.ai/legal/acceptable-use-policy, "Effective: August 14, 2026" (same capture time).
- Consumer terms: https://x.ai/legal/terms-of-service, "Last Updated: September 11, 2026" (capture `20260928134216`).

Which terms apply through Higgsfield: the enterprise terms cover "enterprise (business) users of the SpaceXAI API". They let the customer "distribute or otherwise make the Bundled Service available to Customer's End Users" and state: "No direct contractual relationship is created between SpaceXAI and any End User". So Higgsfield is the xAI customer and the founder is an End User. xAI binds Higgsfield to keep end-user terms "no less protective of SpaceXAI and the Services than this Agreement and the AUP". The AUP "applies to anyone using our Service, including consumers, developers and businesses", so it reaches the founder too.

Operative sentences:
- Ownership (enterprise, "Rights in Input and Output"): "Customer … (b) owns all right, title, and interest in the Output in perpetuity and, to the fullest extent possible under applicable law, SpaceXAI hereby assigns to Customer all of its right, title, and interest in such Output".
- Limits on output (same clause): "Customer will not, and will not permit any third party to: (i) use any Output to train any foundation models … or (ii) misrepresent that any Output was human-generated."
- No clause in the enterprise terms or the AUP bars commercial use of output. The enterprise grant is "solely for Customer's business purposes", which is commercial by nature.
- Attribution: the consumer terms (not the API route) say: "When using Output or SpaceXAI's name, logos, trademarks, or other brand elements, you are required to obtain our permission and attribute your generation of the Output to the Service, as detailed in our Brand Guidelines." The enterprise terms have no such sentence. I did not read the Brand Guidelines.
- Watermark (AUP): prohibits "Stripping, altering or circumventing embedded provenance metadata or watermarks". The Grok files carry no metadata (F1), so there is nothing to strip at present.
- Deletion (enterprise, "Deletion and Retention of User Content"): "All User Content will be automatically and permanently deleted no later than 30 days after the end of the interaction or session in which it was submitted unless a different retention period is … agreed". This is xAI deleting its own server copy from Higgsfield's account. It does not delete the file the founder downloaded.

### F4 — Higgsfield deletes output files after 7 days (1P: Higgsfield's own storage headers)

Method: `curl -I` on three output URLs from the 30 Sep ledgers (`r*/higgsfield-spend.jsonl`), on 30 Sep 2026. Each answered HTTP 200 with this header:
`x-amz-expiration: expiry-date="Thu, 08 Oct 2026 00:00:00 GMT", rule-id="Delete after 7 days"`
- The host is Higgsfield's CloudFront store (`d3u0tzju9qaucj.cloudfront.net`). The S3 lifecycle rule is named "Delete after 7 days". The files were written 30 Sep 2026 09:37-09:40 GMT.
- The rule is on Higgsfield's store, so it applies to every model on the API (Grok, Qwen, Ideogram, and also Recraft, which the roster already trials).
- `scripts/higgsfield.js` downloads each file at once, so the founder's copy is safe. But the fact bar says "it deletes outputs", with no exception for a download. The roster already drops Veo partly because its "files deleted after 2 days". This clash is for the roster owner to rule on: either the bar means "deletes the only copy" (then all three pass, because the script keeps a copy), or it means any server-side deletion (then Higgsfield itself, and so all three models and Recraft through it, fail).

F4 addendum — Higgsfield's documented policy (1P, read 30 Sep 2026):
- https://docs.higgsfield.ai/docs/concepts/billing-and-retention.md, "Output retention": "Generated output is accessible for at least seven days after creation and may be removed after that period. Download completed files to your own storage for long-term retention."
- https://docs.higgsfield.ai/docs/help/faq.md: "Files may be removed from our servers at any time after the 7-day retention period."
- The store header (F4 above) shows that removal is scheduled, not only possible.

### F5 — Higgsfield model pages and price list (1P, read 30 Sep 2026)

Pages read in full:
- https://docs.higgsfield.ai/docs/models/grok-image-2/generate-and-edit.md
- https://docs.higgsfield.ai/docs/models/qwen-image-3/text-to-image.md
- https://docs.higgsfield.ai/docs/models/ideogram-4/generate.md
- The three parent pages (`/docs/models/grok-image-2.md`, `qwen-image-3.md`, `ideogram-4.md`) and `/docs/models/image-generation.md`.

Licence: none of these pages has a licence, ownership, attribution or watermark note. The only licence text on Higgsfield's side is its general terms (roster row, line 24).

Ceiling, as documented:
- Grok: "resolution accepts 1k or 2k". Largest tier: `2k`. Observed at 16:9: 2816x1584 (F1).
- Qwen: `resolution` "1k" or "2k". Usage note: "resolution is a tier; 2k square maps to 1536 by 1536 pixels, not 2048 by 2048." Observed at 16:9: 2048x1152 (F1). So Qwen's long edge at 2k depends on the aspect ratio: 2048 at 16:9, 1536 at 1:1.
- Ideogram 4.0: the schema has no resolution field. Inputs are `prompt`, `image_url`, `aspect_ratio` (23 ratios), `image_weight` and `rendering_speed` (TURBO, DEFAULT, QUALITY). Observed at 16:9 with QUALITY: 2560x1440 (F1). The page does not say whether Higgsfield upscales.

Price list: https://dash.higgsfield.ai/api/v2/pricing/models/ (all 29 entries, 3 pages, fetched 30 Sep 2026):

| Endpoint | Configuration | USD per image |
|---|---|---|
| `xai/grok-imagine-image-2.0` | 1k, quality low | 0.04 |
| `xai/grok-imagine-image-2.0` | 2k, quality medium | 0.08 |
| `alibaba/qwen-image-3/text-to-image` | 1k | 0.04 |
| `alibaba/qwen-image-3/text-to-image` | 2k | 0.075 |
| `ideogram/v4.0` | (no configuration) | 0.03, qualifier "exact" |
| `recraft/v4.1/text-to-image` | 1k, 1:1 | 0.035 |
| `recraft/v4.1/utility/text-to-image` | 1k, 1:1 | 0.035 |
| `recraft/v4.1/pro/text-to-image` | 2k, 1:1 | 0.21 |
| `recraft/v4.1/utility/pro/text-to-image` | 2k, 1:1 | 0.21 |

- The list prices Ideogram at $0.03 only. It has no line for rendering speed. The 30 Sep ledgers show the real charge for `rendering_speed: QUALITY`: `"usd":0.1,"credits":"1.600"` on each of the three Ideogram requests (`r*/higgsfield-spend.jsonl`). So QUALITY costs $0.10.
- Ledger charges for the others match the list: Grok 2k medium `"usd":0.08`, Qwen 2k `"usd":0.075`.
- The Higgsfield price list and the xAI model page disagree on nothing: xAI's own page (https://docs.x.ai/developers/models/grok-imagine-image-2.0) states "Output: $0.04 per image" as the base price, which matches the Higgsfield 1k low figure. I did not find xAI's own 2k medium price on a 1P page.

### F6 — Ideogram 4.0: licence, ceiling, price (1P, read 30 Sep 2026)

Pages read:
- Developer API Agreement and Policy, https://ideogram.ai/legal/api-tos/, "Last revised: August 14, 2024" (read in full).
- Terms of Service, https://ideogram.ai/legal/tos/, "Last revised: August 14, 2024" (sampled by keyword: output, commercial, watermark, attribution).
- Licensing, https://ideogram.ai/licensing/ (read in full).
- Model page, https://ideogram.ai/models/4.0/ (sampled: API, licence and price sections).
- API reference, https://developer.ideogram.ai/api-reference/api-reference/generate-v4 (resolution enum and rendering-speed text extracted from the page source).

Licence:
- Output is the user's and commercial use is open. ToS 2.1: "We do not claim any ownership rights in your User Input or User Output, and we do not restrict your ability to use User Output for your own purposes (including for commercial purposes)." Licensing FAQ: "Can I use Ideogram outputs commercially? Yes. Ideogram does not claim ownership of outputs generated with the model. You can use outputs commercially as long as you respect third-party rights and follow the Acceptable Use Policy. The exception is using outputs to train models that compete with Ideogram."
- Attribution falls on the reseller, not on the picture. API terms 2.3.1: "Developer agrees to clearly (a) identify on the Developer Application that any User Output generated by users of the Developer Applications via use of the Ideogram API was created by the Ideogram AI Model (e.g., via a "Powered by Ideogram" tagline)". Here the "Developer" is Higgsfield and the "Developer Application" is Higgsfield's product. No clause requires the founder to credit Ideogram on a published asset.
- Honesty duty, API terms 2.3(H): do not represent "that the User Output is entirely human generated". Disclosure is "encouraged", not required.
- Risk to note: Ideogram 4.0 has open weights. Their free licence is non-commercial: "Download Ideogram model weights from Hugging Face for research, evaluation, and personal projects. Free under the Ideogram Non-Commercial Model Agreement." Third-party access on self-hosted weights needs Enterprise ("Customer-facing or third-party access: Talk to sales" for Enterprise; "Not permitted" for open weights). Higgsfield does not state whether it calls Ideogram's hosted API or runs the weights. If Higgsfield runs the free weights, that is Higgsfield's breach with Ideogram; the licensing FAQ still says outputs are usable commercially. I found no sentence that bars an end user's commercial use on any route. (Inference, not a quote.)

Watermark: ToS 4.x lists as prohibited "(H) remove any watermarks included on any User Output or otherwise generated by the Services". The API reference and the model page say nothing about a watermark, C2PA or an invisible mark. The three Higgsfield files carry no metadata and no visible mark (F1, F2). The Hugging Face model card is gated (HTTP 401); I did not read it.

Ceiling — the roster row is out of date:
- The roster says "Its 1536 px ceiling is below a 2K hero". That is true of Ideogram 3.0: its API page (https://developer.ideogram.ai/api-reference/api-reference/generate-v3) lists presets whose long edge stops at 1536 (for example 1536x640, 1536x512).
- Ideogram 4.0 has a separate enum, `ResolutionV4`, described as "The 1K and 2K resolutions supported for Ideogram 4.0 image generation." Its 38 values include 2048x2048, 2560x1440, 2560x1600, 2880x1440 and up to 3328x1248 (long edge 3328). The model page says "realistic 2K images".
- 2560x1440, the Higgsfield output at 16:9, is a native Ideogram 4.0 preset. So the 30 Sep files are not an upscale by Higgsfield; they are Ideogram 4.0's own 2K output for 16:9. (Inference from the enum match; Higgsfield does not state its pipeline.)

Price:
- Ideogram's own price (model page): "Turbo $0.03 / image", "Default $0.06 / image", "Quality $0.10 / image".
- Higgsfield lists one figure, $0.03 "exact", and charged $0.10 for QUALITY (F5). The Higgsfield $0.03 thus matches Ideogram's TURBO tier, not DEFAULT. The calibration report (`~/higgsfield-calibration-2026-09-30/report.md`) says "$0.03 list figure (that is the DEFAULT tier)". That claim is unverified and probably wrong: DEFAULT is likely $0.06 on Higgsfield too. Confirm with the estimate endpoint before relying on it.

### F7 — Qwen Image 3: licence, label, ceiling (1P, read 30 Sep 2026)

Pages read:
- Alibaba Cloud International Website Product Terms of Service, §4.48 "Alibaba Cloud Model Studio", https://www.alibabacloud.com/help/en/legal/latest/alibaba-cloud-international-website-product-terms-of-service-v-3-8-0, "Last Updated: Aug 28, 2026" (§4.48 read in full; the rest of the 31,000-word document not read). The Model Studio "Related agreements" page (Last Updated Sep 28, 2026) names this document first among the agreements that "govern your use of Model Studio".
- Model Studio service-specific terms (China site, English), https://help.aliyun.com/en/model-studio/bailian-service-notes (read in full; no date shown).
- Qwen Image Generation and Editing 3.0 API reference, https://www.alibabacloud.com/help/en/model-studio/qwen-image-generation-and-editing-api-reference, "Last Updated: Sep 28, 2026" (sampled by keyword).

Licence:
- Ownership and use, §4.48.1(e): "Model Studio does not claim ownership of any Intellectual Property Rights in the Output. You may use the Input and Output, provided your use complies with applicable laws, the Agreement, and our rules." No clause bars commercial use of paid-API output.
- The only commercial bar is on free trials, in the China-site service terms: "The content you generate through model trials may only be used to evaluate the model's performance. It may not be used for any other purpose, including any commercial purpose." This covers the console's trial feature, not paid calls through Higgsfield.
- Labelling duty, §4.48.1(g)(ii): "You shall, if required under applicable laws, conduct labelling or marking on the Outputs in a conspicuous manner, including but not limited to adding watermarks and/or attaching statements when publishing or disseminating any Outputs". The duty depends on the law where the founder publishes; the terms do not impose it by themselves. The China-site terms add, for trials: "You must not remove or tamper with labels such as "AI-generated" added by the trial service."
- Resale, §4.48.1(d)(v): the customer shall not "resell Model Studio or AI models provided through Model Studio … unless expressly authorised by us". This binds Higgsfield, not the founder. Higgsfield does not say whether it holds that authority or which Alibaba route it uses.
- Attribution: none required.

Label (the XMP chunk in F1):
- The API reference gives the visible mark as opt-in: `watermark` "Whether to add a watermark. Default: false." Higgsfield's schema does not expose `watermark` (F5), and the files show no visible mark (F2).
- The API reference does not mention the metadata label. The label in the files uses the TC260 AIGC namespace (TC260 is China's national information-security standards committee). This matches the implicit-label duty in China's rules for labelling AI-generated content (2P, from memory; not read this session). Its `ContentProducer` value embeds an 18-character Chinese unified social credit code beginning `91330106`, a Hangzhou (Xihu district) region code (2P inference). So Higgsfield probably reaches Qwen through an Alibaba mainland endpoint.
- Reading for the fact bar: the output carries a machine-readable AI label in metadata, not a watermark in the pixels. The roster does not say whether a metadata label counts as "watermarked". The roster already holds Google output "carries SynthID" at `use — as candidates`, which suggests an invisible mark alone is not a drop.

Ceiling:
- Maker's own ceiling: "Text-to-image (T2I): Pixel area from 512x512 to 2048x2048. Aspect ratio: 1:8 to 8:1." So direct from Alibaba, a 16:9 image may reach about 4.2 MP (for example near 2720x1530).
- Through Higgsfield: the `2k` tier gave 2048x1152 at 16:9 (2.36 MP), and Higgsfield states "2k square maps to 1536 by 1536 pixels". Higgsfield thus caps Qwen below the maker's ceiling.
- URL lifetime at the maker: "The link is valid for 24 hours." Higgsfield re-hosts the file on its own store for 7 days (F4).

F7 addendum (2P): a web-search summary (read 30 Sep 2026; sources listed included https://github.com/QwenLM/Qwen-Image and https://en.wikipedia.org/wiki/Qwen) states that Qwen Image 3.0 launched in July 2026 as an API-only model with no published weights. I did not confirm this on a Qwen or Alibaba page. If true, no open-weight licence applies, and the Alibaba Cloud product terms above govern.

### F8 — Price against the roster (1P prices from F5; the purpose comparison is my reading)

At the settings used on 30 Sep, per image: Qwen 2k $0.075; Grok 2k medium $0.08; Ideogram QUALITY $0.10 (TURBO $0.03; DEFAULT unconfirmed, likely $0.06).
- Recraft V4.1 at 1K ($0.035) is cheaper than all three, but 1K is itself below a 2K hero, so it does not serve the same purpose (a 2K hero).
- Recraft V4.1 Pro at 2K ($0.21) serves a 2K hero and costs 2.1 to 2.8 times more than the three. It does not beat them on price.
- Recraft's own purpose is "Flat art, native SVG, palette as data". None of the three takes a palette as data or returns SVG, so for that purpose Recraft has no rival among them.
- Midjourney (Basic ~$10 a month, roster row) is run by hand and "never enters a production loop". It does not serve the same purpose as an API model.
- No other roster row is sold on Higgsfield's API. So no roster tool beats any of the three on price for a 2K hero.
- Among the three: if all three join the roster for one and the same purpose, the price rule would then weigh them against each other (Qwen cheapest, Ideogram QUALITY dearest). The 30 Sep report gives each a distinct look ("A look none of the others have" for Ideogram), which argues for three purposes, not one. That is a taste call for the founder.

## Verdicts

Fact bar rules, per model.

| Fact | Grok Image 2.0 | Qwen Image 3 | Ideogram 4.0 |
|---|---|---|---|
| Licence bars commercial use | No (1P, F3) | No for paid API; yes for free trials only (1P, F7) | No (1P, F6) |
| Output watermarked | No mark found; no metadata (1P, F1-F3) | No visible mark; XMP AI label in metadata (1P, F1, F2, F7) | No mark found; no metadata (1P, F1, F2, F6) |
| Deletes outputs | Higgsfield store deletes after 7 days; xAI copy within 30 days (1P, F3, F4) | Higgsfield store deletes after 7 days (1P, F4) | Higgsfield store deletes after 7 days (1P, F4) |
| Ceiling below a 2K hero | No: 2816x1584 at 16:9 (1P, F1, F5) | Borderline: 2048x1152 at 16:9, 1536x1536 at 1:1 (1P, F1, F5, F7) | No: 2560x1440 at 16:9, native 4.0 preset; up to 3328 long edge (1P, F1, F6) |
| Roster tool cheaper for same purpose | No (F8) | No (F8) | No (F8) |

- **Grok Image 2.0 (`xai/grok-imagine-image-2.0`): passes**, subject to the roster owner's ruling on Higgsfield's 7-day deletion (F4). Duties that go with it: do not claim a human made the output; do not strip provenance marks (AUP).
- **Qwen Image 3 (`alibaba/qwen-image-3/text-to-image`): passes**, subject to two rulings: Higgsfield's 7-day deletion (F4), and whether a metadata-only AI label counts as "watermarked" (F7). Its 16:9 output is exactly 2048 px wide, so it meets a 2K hero only if "2K" means 2048 px; a 1:1 hero at 1536 px falls short.
- **Ideogram 4.0 (`ideogram/v4.0`): passes**, subject to the same 7-day ruling (F4). The roster's `drop` row rests on a 1536 px ceiling that belongs to Ideogram 3.0; 4.0 outputs 2K natively, which meets the row's own reversal condition ("the ceiling lifts").
- **Unknown for all three:** whether Higgsfield holds reseller rights from each maker (xAI enterprise terms permit Bundled Services; Alibaba requires express authority to resell; Ideogram requires the hosted API or an Enterprise licence for third-party access). This is Higgsfield's contractual risk, not a bar on the founder's output. No maker states that an end user's commercial use fails if the reseller lacks rights.
- **Correction to carry into the roster or report:** the calibration report's "$0.03 … is the DEFAULT tier" for Ideogram is probably wrong; Ideogram's own list puts $0.03 at TURBO and $0.06 at DEFAULT (F6).

**Bound:**
- Read in full: xAI enterprise terms and AUP (via Wayback captures of 28 Sep 2026, because x.ai returned 403); Ideogram Developer API Agreement; Ideogram licensing page; Alibaba Cloud product terms §4.48 (Model Studio) only; Model Studio service-specific terms (China site); Higgsfield docs pages for the three models, billing-and-retention, FAQ, docs index; Higgsfield price list (all 29 entries); the PNG chunk list of all nine files; the calibration report and three spend ledgers.
- Sampled by keyword: xAI consumer terms; Ideogram Terms of Service; Ideogram 4.0 model page; Ideogram v4 and v3 API reference pages; Qwen 3.0 API reference; xAI image docs (read through WebFetch summaries, which may paraphrase: the xAI image-generation page and the xAI model page).
- Not read: Alibaba Cloud product terms outside §4.48; xAI Brand Guidelines; Ideogram Usage Policy and Acceptable Use Policy; Ideogram Hugging Face card (gated, HTTP 401); Higgsfield's own terms of service (the roster's 26 Jul 2026 summary was taken as given); China's AI-content labelling rules (cited from memory as 2P).
- Not tested: an invisible pixel watermark in any file (no detector run); Ideogram DEFAULT price and TURBO size on Higgsfield (no request sent); the identity behind the Qwen label's producer code.
