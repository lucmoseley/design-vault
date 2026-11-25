# Tool roster

One row per tool, with a **house disposition** decided on facts alone (lucmoseley/mantahostels#3551). A project's guide overrides any row. Manta's `docs/brand/design-process.md` §Tool roster is the first set of overrides. **The two sets drift, and that is accepted:** nothing syncs them. Prices are secondary figures, so confirm them in the browser before paying.

**The fact bar.** A tool is `drop` house-wide where:
- its licence bars commercial use;
- its output is watermarked: a mark you can see in the picture, not a label in the file's metadata or an invisible one like SynthID (design-vault#47 Q2);
- it deletes outputs, leaving no copy: a vendor that deletes its copy after the file is saved passes (design-vault#47 Q1);
- its ceiling is below a 2K hero;
- or a roster tool already beats it on price for the same purpose, counted per usable image, so a tool whose test gave nothing usable is beaten by any that did (design-vault#47 Q7).

A clash with a project's stack, brand sheet or `DESIGN.md` is never a house reason: it goes to the project's row. The House DNA is a taste and decides no tool.

**Dispositions.** These are the spellings Manta's roster uses: `use`, `use — first, always`, `use — as candidates`, `use — as search, no MCP`, `use — last`, `use — rung one`, `use — every round`, `trial — one month`, `trial — via Higgsfield`, `trial — one clip`, `build when needed — rung two`, `drop` and `retired`. The vault adds these:
- `unjudged` — listed, but nobody has tried it or read its licence.
- `per project` — passes the fact bar. The deciding clash is stack or taste.
- `use — every command at its stage` — a tool whose commands [impeccable.md](impeccable.md) places stage by stage.
- `use — rung two` and `build when needed — rung three` — the vault's tweak step, where `impeccable live` sits between DevTools and the slider panel (design-vault#57).

For an image model, `use — first, always` renders every direction by default and `use — as candidates` renders a direction only where the model-selection rule below sends it there (design-vault#47 Q19, design-vault#52).

Manta's `refused` is its delete-zone's word and is never a house disposition.

## Image generation (lucmoseley/mantahostels#3078, design-vault#47)

| Tool | Purpose | Asset class | Free or paid | House disposition | Fact | Dialect |
|---|---|---|---|---|---|---|
| Higgsfield | The harness: one account reaching several image models, by two routes | Brand art | Paid — API pay-as-you-go, $5 minimum top-up, billed apart from the web plans | trial — one month | **API:** Claude renders through `scripts/higgsfield.js` (design-vault#18), billed to the API balance. **Discount** (design-vault#61): every model on sale is 15% off from sign-up, and the account's `/estimate` already takes it off Kling 3.0 and Wan 2.7. Three models picked in the console get their maximum discount: 50% on Kling 3.0 and Wan 2.7, 30% on Seedance 2.0, 15% on GPT Image 2.5; none on Grok, Ideogram or Qwen. A pick is final, and its discount lasts a set number of days, longer after larger top-ups; the founder picks in design-vault#64. Web plan credits never change API prices. **Balance:** the API documents no balance endpoint, so nothing warns before a batch runs short. Keep the balance at or above the round's ceiling before a round starts. API funds expire a year after they are added. **`max_usd` for a price rule:** work it out at the rule's list rate, never a discounted one (design-vault#63). Neither the public price list nor the key's `GET /models` list is complete: FLUX.2 answers the free `/estimate` call but is on neither (design-vault#47). **CLI:** `@higgsfield/cli` signs in with the web account and bills the web plan's credits. It reaches the web app's catalogue, Nano Banana Pro and Seedream among it. It is installed and signed in, but the plan is free with 0 credits, and Starter is held until a style goes unserved (design-vault#47 Q14). Higgsfield deletes each output a week after it is made; `higgsfield.js` saves it at once, so this passes the fact bar. Ownership clause (terms of 26 Jul 2026): Higgsfield claims no ownership of outputs and does not restrict their commercial use. It may train its models on inputs and outputs, except under an Enterprise Agreement. A third-party model's use policy applies where it is stricter. | none of its own; the model's rules apply |
| GPT Image 2.5 — Sunburst, the default; Flare | Every direction, unless the rule below sends it elsewhere | Brand art | Inside Higgsfield — API, priced per token | use — first, always | Benchmarks: design-vault#51. `marketing-studio/image/sunburst`, `quality` `high`, `enhance_prompt` `false`: 2k gives 2688x1520. 4k is offered, at about $1 an image. The estimate is a price rule, so each job carries `max_usd` `0.6`, the most one image can cost, until the founder reads a real charge off the console. Ownership clause (OpenAI's terms and use policy, read 30 Sep 2026): OpenAI gives the output to its customer, Higgsfield, claims none of it and bars no commercial use, so Higgsfield's clause above decides, and it restricts none. The files arrive with no metadata and no visible mark. Never present one as made by a person; disclose AI generation where a law requires it; no real person's likeness without consent (design-vault#55). | [prompts.md §GPT Image 2.5](prompts.md#gpt-image-25) |
| Grok Imagine 2.0 | Candidate: the painterly-brushstroke look | Brand art | Inside Higgsfield — API, $0.08 | use — as candidates | `xai/grok-imagine-image-2.0`, `quality` `medium`, 2k: 2816x1584. Rewrites every prompt, with no switch. Paints a checkerboard where transparency is asked for. | [prompts.md §Grok](prompts.md#grok-imagine-20) |
| Qwen Image 3 | Candidate: no rule sends a direction to it yet | Brand art | Inside Higgsfield — API, $0.075 | use — as candidates | `alibaba/qwen-image-3/text-to-image`, always with `prompt_extend` and `enable_thinking` `false`, or it adds clutter and stray text. 2k gives 2048x1152 at 16:9, 1536x1536 square. | [prompts.md §Qwen](prompts.md#qwen-image-3) |
| Ideogram 4.0 | Candidate: a locked palette, and the grainy magazine-print look | Brand art | Inside Higgsfield — API, $0.10 at `QUALITY` | use — as candidates | `ideogram/v4.0`, `rendering_speed` `QUALITY` ($0.03 at `TURBO`, $0.06 at `DEFAULT`): 2560x1440. Higgsfield passes its JSON caption through, so the palette goes in as hex data and a box pins each element (design-vault#49). | [prompts.md §Ideogram](prompts.md#ideogram-40) |
| Nano Banana Pro · Seedream 4.5 | Other idioms, on the web plan | Brand art | Inside Higgsfield — web plan credits | use — last | Reachable only on the web plan, in the web app or through the CLI (`nano_banana_2`, `seedream_v4_5`). On the API, Nano Banana Pro answers `503 model_disabled`. None ships until its ownership clause has been read. | [prompts.md §Nano Banana Pro](prompts.md#nano-banana-pro--seedream) |
| Midjourney | Painterly families; the taste control | Brand art | Paid — Basic ~$10/mo, 3.3 fast hours | trial — one month | Rated best for the painterly idiom. It runs by hand in the browser: no API, and no honest MCP. It never enters a production loop. Upgrade to Standard only if the fast hours run out. The model-selection rule never routes to it. | [prompts.md §Midjourney](prompts.md#midjourney) |
| Recraft's own API | Native SVG | Brand art | Paid — about $0.08 an image (secondhand, lucmoseley/mantahostels#3092) | unjudged | The route to native SVG, which Higgsfield's Recraft does not return (design-vault#47 Q15). | [prompts.md §Recraft](prompts.md#recraft) |
| Recraft V4.1 via Higgsfield | — | Brand art | Inside Higgsfield — API, $0.21 at 2K | drop | Grok does the same job at $0.08 (design-vault#47 Q6). | — |
| FLUX.2 Pro · Flex · Max | — | Brand art | Inside Higgsfield — API | drop | 1920x1088 at most on Higgsfield, below a 2K hero. Reversal: a route over 2K. | — |
| Z-Image Turbo · SOUL V2 | — | Brand art | Inside Higgsfield — API | drop | Beaten on price per usable image: neither made a usable image on 30 Sep. | — |
| SOUL | — | Brand art | Inside Higgsfield — API, $0.19 | drop | Made for photos. For brand art, Grok beats it at $0.08. | — |
| OpenAI, Google, Flux, Seedream, Ideogram — direct subscriptions | — | Brand art | Paid | drop | Higgsfield reaches four: GPT Image 2.5 and Ideogram 4.0 through its API, with Ideogram's JSON palette, and Nano Banana Pro and Seedream on its web plan. Flux direct would be a route to FLUX.2 over 2K, the FLUX.2 row's reversal, which is the founder's to take. Reversal: if the Higgsfield trial is dropped, this row names which returns. | — |

### The model-selection rule (design-vault#52)

GPT Image 2.5 Sunburst renders every direction unless a rule below sends it elsewhere. **The first rule that matches decides.**

| # | Condition the card or brief states | Model | Why |
|---|---|---|---|
| 1 | The chosen model is down | **No switch.** Retry once after a minute. Then hold the whole round with `held.md` in its folder (§0 of the skill), post nothing on the brief's ticket, and tell the founder in the session, with the error and the request id. Every later session on the brief retries first. After a day, draft a Higgsfield support message; the founder adds `waiting:external` when he sends it. A model withdrawn for good is a roster question for him. | The founder: "not having the correct model available never passes to an inferior one … We do not sacrifice quality for happenstance." GPT's own outage included. The one outage on record: design-vault#34. |
| 2 | The batch won't fit the round's spend ceiling | **No switch.** Render what fits, in card order, and ask the founder to raise the ceiling. The round stays held, with `held.md` in its folder, until he does. | Only the founder sets the ceiling. |
| 3 | The subject is an animal that must look right (a mascot, a named species), or the card passes more reference images than the target model takes | GPT Image 2.5, whatever the look or palette | GPT leads the only animal benchmark (42.6 of 100) and drew the only true manta on 30 Sep. Reference limits: Sunburst 16, Grok 5 (xAI's figure; Higgsfield says 10), Ideogram 1, Qwen none (one to three on its edit endpoint only). |
| 4 | The brief *locks* the palette: its own lines say the colours are exact | Ideogram 4.0, with the palette in its JSON caption | On one textured test, 55% of the scene's pixels fell within ΔE 10 of the palette, against GPT's 16%. A palette that is only *anchored*, like Manta's (lucmoseley/mantahostels#3058 Q3), is not locked. |
| 5 | The look is "grainy, muted, magazine-print illustration" | Ideogram 4.0 | A look none of the others drew on 30 Sep. |
| 6 | The look is "painterly, with visible brushstrokes" | Grok Imagine 2.0 | The founder's 30 Sep notes. |
| — | Any other look; layout; animal anatomy; reference images; text | GPT Image 2.5 Sunburst | GPT leads each on independent evidence (design-vault#51). Copy is never put into an image (§6 of the skill). |

So a locked-palette mascot stays on GPT (rule 3), and a locked palette with the painterly look goes to Ideogram, with "painterly, visible brushstrokes" in its caption (rule 4).

- **Transparency never picks a model.** None of the API models returns it. The prompt asks for one loud plain background colour, far from the palette and from the direction (a chroma green), and no ground shadow unless the asset wants one. The [colour key](#cut-out-design-vault54) then removes it.
- **No round-one quota.** If no rule fires, all five directions render on GPT.
- **The look list is closed.** Only the founder adds a look rule, after a round shows a candidate beating GPT on a look. A card names its look by the rule's exact wording; whether a direction *is* that look is the one judgement left, and it sits on the card.
- **Later rounds and edits stay on the leader's model.**
- **Each model's largest output** per aspect ratio, with its source, is in [render-sizes.json](render-sizes.json), which `check-render.py` reads for `vault.render-size`. A model added to this table gets its row there, sizes from its docs or a render at its largest tier.

## Cut-out (design-vault#54)

Record: `vault.render-checkerboard`.

For brand art that needs a transparent background, such as a mascot or a spot illustration placed on a page.

| Tool | Purpose | Asset class | Free or paid | House disposition | Fact | Dialect |
|---|---|---|---|---|---|---|
| Colour key — the house's own script | Remove the render's plain background | Brand art | Free | use — first, always | Keys out the background colour where it touches the frame's edge, then un-mixes a thin edge band against the nearest solid colour. Full size. Fails where the subject shares the key colour. It keeps a painted ground shadow. Untested on soft painterly edges. [`scripts/cutout.py`](../scripts/cutout.py) (design-vault#56). Reversal: a real asset it can't separate; Ideogram's remover ($0.01) is the next to judge. | the transparency line of the model-selection rule |
| BiRefNet — local through rembg (`birefnet-general`, `-lite`) · on Replicate | — | Brand art | Free, MIT · Replicate about $0.0014 an image | unjudged | Never seen working here. Locally, this 9 GB machine's low-memory guard stopped it three times, at 3.1–4.2 GB. Replicate needs an account. | — |
| rembg `isnet-anime` | — | Brand art | Free, Apache-2.0 | drop | Nothing usable on 30 Sep. | — |
| BRIA RMBG-1.4 · RMBG-2.0 — rembg's default model | — | Brand art | Free weights; hosted Bria $0.018 | drop | The weights bar commercial use (CC BY-NC) without a contract. rembg loads RMBG-2.0 when no model is named, so every rembg call names one. | — |
| Recraft's remove-background | — | Brand art | Paid | drop | Recraft's docs say it works at 1024 px on the short side and shrinks larger images, below a 2K hero. Not confirmed by a call. | — |
| Photoroom · remove.bg · Picsart · Adobe | — | Brand art | Paid | drop | The colour key beats each on price. Adobe: enterprise contract only. | — |

## Image to video (lucmoseley/mantahostels#3079)

| Tool | Purpose | Asset class | Free or paid | House disposition | Fact | Dialect |
|---|---|---|---|---|---|---|
| Luma Ray 3.2 | Looping clip from a still | Motion and video | Pay-as-you-go, ~$0.30 a clip | trial — one clip | The only native `loop` flag. `keyframes.frame0` and `frame1` take the same still. Run it from a script by hand. | [prompts.md §Video](prompts.md#video--image-to-video) |
| Kling 3.0 | The same, start frame = end frame | Motion and video | Inside Higgsfield — API, list $0.084 a second (design-vault#63) | trial — via Higgsfield | `kling-video/v3.0/std/image-to-video`. That price holds with `sound` `off`; sound is on by default, at $0.126 a second. Similar frames avoid a shot switch. That mode caps at 5 s. If the Higgsfield trial is dropped, Kling moves to a direct account, whose free tier bars commercial use. | [prompts.md §Video](prompts.md#video--image-to-video) |
| Wan 2.7 | The same | Motion and video | Inside Higgsfield — API, list $0.10 a second (design-vault#63) | trial — via Higgsfield | `wan/v2.7/image-to-video`, at 720p; 1080p is $0.15 a second. Its weights are open. Self-hosting needs 16 GB of VRAM. | [prompts.md §Video](prompts.md#video--image-to-video) |
| Veo 3.1 · Seedance 2.x · Runway Gen-4 · Pika 2.5 | — | Motion and video | Paid | drop | Veo: 4 s minimum, audio, files deleted after 2 days, SynthID. Seedance 2.0: about $0.30 a second at 1280x720, 3.6 times Kling 3.0 without sound (design-vault#63); its end frame is unverified. Runway: Luma beats it on price and on loop control. Pika: 480p, watermarked, no commercial use. | — |

- **Each Higgsfield video model's start-frame and end-frame fields**, read from its request schema, are in [loop-fields.json](loop-fields.json), which `check-clip.py` reads for `vault.clip-loop`. A video model added to this table gets its row there.

## Component sourcing (lucmoseley/mantahostels#3081)

| Tool | Purpose | Asset class | Free or paid | House disposition | Fact | Dialect |
|---|---|---|---|---|---|---|
| The project's own primitives | The whole working area | Web surfaces | — | use — first, always | — | — |
| shadcn/ui | Structure and keyboard behaviour for interactive primitives | Web surfaces | Free, MIT | use | — | — |
| Magic UI | Hero and marketing motion | Web surfaces | Free, MIT | use | — | — |
| React Bits | Structure | Web surfaces | Free, MIT + Commons Clause | use | Shipping it inside a site is permitted. A rewrite is still a ported version, and it is never redistributed as a component. | — |
| 21st.dev | A search layer, not a library: copy the prompt by hand | Web surfaces | Free signup, two copies a day | use — as search, no MCP | Its terms grant nothing off-platform. The right to use a component comes from its author, so read it per component. | — |
| `site-clone --analyze-only` | Teardown of a real page, as text | Web surfaces | Free, MIT | use — last | Not a component source. Never commit or publish its output, never copy a token file wholesale, and never run it at a site that refuses a script. | — |
| Aceternity UI | — | Web surfaces | Use licence | unjudged | Its licence page does not confirm that the free components are covered. | — |

## Tweak step (lucmoseley/mantahostels#3081)

| Tool | Purpose | Asset class | Free or paid | House disposition | Fact | Dialect |
|---|---|---|---|---|---|---|
| Chrome DevTools — Styles pane and Changes panel | Edit a `:root` custom property on the dev server, then copy the CSS diff into chat | Web surfaces | Free | use — rung one | Nothing to install. | — |
| `impeccable live` | The founder picks one element in the browser and chooses among three generated alternatives | Web surfaces | Free | use — rung two | Needs the project's dev server running. | — |
| Tweakpane | A slider panel bound to custom properties, with copy-to-clipboard read-back | Web surfaces | Free, MIT, zero dependencies | build when needed — rung three | Built to [polish.md](polish.md) the first time a favourite moves several axes at once. `lil-gui` is the fallback; `leva` brings zustand, Radix and more (lucmoseley/mantahostels#3081). | — |
| Google Stitch | Generated screens | Web surfaces | Free | per project | Returns Tailwind HTML, which is fine on a Tailwind site. | — |
| `stitch-skill` — Google Stitch's plugin | The same, from the agent | Web surfaces | Free | per project | Assumes Tailwind and React Router. Caveat: its install overwrites whichever `DESIGN.md` sits at the project root. | — |

## Skills and surfaces

| Tool | Purpose | Asset class | Free or paid | House disposition | Fact | Dialect |
|---|---|---|---|---|---|---|
| `design-vault:design-critique` | The portable critique on every candidate, beside the project's gate | Every class | Free | use — every round | Runs in a fresh subagent each round. | — |
| impeccable | Every web-surface stage: the brief's interview, building candidates, the variant axes, critique and audit, finishing, and the tweak step's `live` | Web surfaces, motion | Free | use — every command at its stage | [impeccable.md](impeccable.md) maps each command. Its comp-led image route stays off. | — |
| Claude Code `/design` | Posters, flyers, cards and brochures as artboards; PNG/PDF export | Print | — | use | Off on this machine until the founder's settings flip (lucmoseley/mantahostels#3055). | — |
| Claude Design | — | — | — | retired | One residual: a fresh build for a print partner that needs an editable Canva file, never a sync (lucmoseley/mantahostels#2999). | — |
| `power-design` | Slides and a meta layer over a design | Web surfaces, print | Free | per project | Outputs standalone HTML outside the app, and its scraping route is paid Firecrawl. Both are stack clashes. The slide path and the meta layer are real elsewhere. | — |
| `awesome-design-md` | — | — | Free | drop | It carries no instruction. Its install overwrites whichever project's `DESIGN.md` sits at the root. One brand file can be read in the browser without installing it. | — |
| `taste-skill` | Taste rules for generated UI | Web surfaces | Free | per project | Needs an image tool the harness lacks, and costs ~1.7k always-on tokens. | — |
