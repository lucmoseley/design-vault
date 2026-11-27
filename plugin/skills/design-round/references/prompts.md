# Prompt shapes

Claude writes each prompt from the brief. It renders a Higgsfield API model's prompt itself (SKILL.md §6), and the founder pastes the rest into the tool. Replace every bracketed field. The palette below is a placeholder: fill it from the project's own rules file, and never carry one project's colours into another's prompt.

## Art direction — the model-agnostic template

Records: `vault.render-palette-look`, `vault.headline-plain-look`.

Every image prompt starts here.

```text
Create one original artwork for [PRODUCT/PROMISE].
Use the attached [THIS DIRECTION'S REFERENCE FILENAME] only for these observed qualities:
[LIGHT / MATERIAL / SCALE / ATMOSPHERE].

New subject: [PRODUCT-RELEVANT CONCEPT].
Composition: [FOCAL LOCATION, CAMERA, NEGATIVE SPACE, LIGHT DIRECTION].
Palette: [COLOURS]. Intended image container: [ASPECT RATIO / CROP NEEDS].
Mobile crop must retain [FOCAL ELEMENT], wholly inside [THE BRIEF'S FOCAL BOX, IN WORDS: E.G. THE RIGHT THIRD, MID-HEIGHT].

Do not reproduce [SOURCE SUBJECTS] or their distinctive arrangement.
Output artwork only, with no website text, navigation, buttons, logos,
dashboard or fabricated product data.
```

Placeholder palette used in the examples: `[INK] #1A1A2E · [PRIMARY] #3A7CA5 · [ACCENT] #E07A5F · [GROUND] #F4F1DE · [SOFT] #81B29A`.

## Tool dialects

The model-selection rule in [roster.md](roster.md) picks the model; its section below gives the prompt. Ask for the largest size the tool offers. Where a model has no palette field, name each colour in words with its hex beside it (design-vault#51). State what you want, never what you do not want ("a plain unbroken sky", not "no clouds"). Where a subject needs a transparent background, ask for one plain background colour the subject doesn't use: no model here returns transparency.

The `--` lines are `scripts/higgsfield.js` arguments, beside `--out` and `--prompt`.

### GPT Image 2.5

Write full descriptive sentences, not keyword lists: the style and subject, the layout with the empty area given its size and place, each surface with its colour, then the mood, the light and the style again with its texture. GPT follows an explicit constraint best, so close the palette with "use only these [N] colours". It takes no palette as data. For a mascot or character across renders, pass the leader as a reference image and write "Do not redesign the character", the one negative worth keeping.

```text
A [STYLE] of [SUBJECT] [ACTION] in [SETTING], seen from [ANGLE]. The [UPPER HALF] is a smooth, unbroken [GROUND IN WORDS] ([GROUND HEX]) [SKY / WALL], left plain and open for a headline. The [SUBJECT] fills the [LOWER HALF]: [EACH SURFACE, WITH ITS COLOUR IN WORDS AND HEX]. Use only these [N] colours: [INK IN WORDS] [INK HEX], [PRIMARY IN WORDS] [PRIMARY HEX], [ACCENT IN WORDS] [ACCENT HEX] and [GROUND IN WORDS] [GROUND HEX]. [3-5 MOOD WORDS]; [LIGHT]; [STYLE, WITH ITS TEXTURE].

--model marketing-studio/image/sunburst --resolution 2k --aspect-ratio 16:9 --set quality=high --set enhance_prompt=false --max-usd 0.6
```

`enhance_prompt=false` stops Higgsfield rewriting the prompt. Stay at 2k: 4k costs about $1 an image, past the cap. Swap `sunburst` for `flare` only where the founder asks for Flare.

### Grok Imagine 2.0

Grok rewrites every prompt, and nothing turns that off. It takes no negative prompt and no seed, so state every constraint as a positive fact. Write full sentences in five layers: subject, setting, composition, light, then the finish, which names the style and the exact colour count. Name the empty surface twice. Pass at most 5 reference images: Higgsfield says 10, xAI says 5.

```text
[SUBJECT] [ACTION] in [SETTING]. Composition: the subject fills the [LOWER THIRD / RIGHT HALF], seen from [ANGLE]; the [UPPER HALF] is a single flat [GROUND IN WORDS] ([GROUND HEX]) [SKY / WALL], smooth and even, left clear for a headline. Light: [e.g. flat, even, shadowless]. Finish: [STYLE, e.g. painterly illustration with visible brushstrokes], exactly [N] colours: [INK IN WORDS] [INK HEX], [PRIMARY IN WORDS] [PRIMARY HEX], [ACCENT IN WORDS] [ACCENT HEX] and [GROUND IN WORDS] [GROUND HEX]; the [UPPER HALF] stays plain [GROUND IN WORDS].

--model xai/grok-imagine-image-2.0 --resolution 2k --aspect-ratio 16:9 --set quality=medium
```

Always send `quality=medium`: xAI's own default is lower than Higgsfield's.

### Qwen Image 3

Switch off the prompt rewrite with both `prompt_extend` and `enable_thinking` false. Thinking on with the rewrite off is refused. Write full sentences in layers: the subject, the layout and the empty area, the palette, the style. Put what must not appear in `negative_prompt`, always including text, and keep the `seed` so a winner can be re-run.

```text
A [STYLE] in exactly [N] colours: [INK IN WORDS] [INK HEX], [PRIMARY IN WORDS] [PRIMARY HEX], [ACCENT IN WORDS] [ACCENT HEX] and [GROUND IN WORDS] [GROUND HEX]. [SUBJECT] [ACTION] in [SETTING], seen from [ANGLE]. The subject sits in the [LOWER THIRD / RIGHT HALF]; the [UPPER HALF] is one plain, unbroken [GROUND IN WORDS] [SKY / WALL] with nothing in it. [EACH REMAINING SURFACE, STATED AS WHAT IT IS]. [TEXTURE AND FINISH].

--model alibaba/qwen-image-3/text-to-image --resolution 2k --aspect-ratio 16:9 --set prompt_extend=false --set enable_thinking=false --set seed=[SEED] --set 'negative_prompt=text, letters, words, signage, logos, watermark, extra animals, [WHAT THE STYLE EXCLUDES]'
```

### Ideogram 4.0

Always send a JSON caption as the prompt (design-vault#49): the palette goes in as data, as uppercase hex in `color_palette` (up to 16), and a `bbox` pins each element in place, so the empty area stays where you put it. A plain prompt may go through Ideogram's own rewrite: whether Higgsfield runs it is untested. Describe the empty background as a positive surface, since Ideogram ignores negatives. Keep the caption under 2,048 characters and its keys in this order. On Higgsfield it takes no negative prompt, seed, style or resolution field.

The worked example: design-vault#49's courtyard, on the placeholder palette. It lost the dusk, so name the time of day in `background` as well. Its one negative, "no hard shadows", is as sent: write "soft shadows".

```text
{"high_level_description":"A soft painterly illustration of a quiet hostel courtyard at dusk seen from above, the upper half left as plain open sky for a headline.","style_description":{"aesthetics":"calm, warm, quiet, restrained","lighting":"soft even dusk light, a warm glow from a few windows, no hard shadows","medium":"illustration","art_style":"soft painterly illustration, visible brush texture, simple shapes","color_palette":["#1A1A2E","#3A7CA5","#E07A5F","#F4F1DE"]},"compositional_deconstruction":{"background":"A smooth, unbroken #F4F1DE dusk sky fills the top half; the courtyard fills the bottom half.","elements":[{"type":"obj","bbox":[520,60,990,940],"desc":"A quiet hostel courtyard seen from above: whitewashed #F4F1DE walls, deep #1A1A2E shadows, a small tree, a few tables, warm #E07A5F lantern light, #3A7CA5 blue doors and shutters"}]}}

--model ideogram/v4.0 --aspect-ratio 16:9 --set rendering_speed=QUALITY
```

`bbox` is `[y_min, x_min, y_max, x_max]` on a 0–1000 grid from the top left: `[520,60,990,940]` fills the lower half.

### Midjourney

Write one line: a noun phrase first, then the parameters. Midjourney ignores hex codes, so name the colours in words and give their count as a phrase.

```text
[STYLE] of [SUBJECT], [COMPOSITION], [COLOURS IN WORDS], [N]-colour palette --ar 21:9 --hd --stylize 80 --raw --chaos 0 --no [WHAT THE STYLE EXCLUDES], text
```

`--sref <url> --sw 100` to `400` locks a reference style. `--oref` locks an object, not a style. Inpainting an HD image drops it back to SD.

Check a saved render with `check-render.py <render> --model midjourney/v8.2 --aspect 21:9` (`midjourney/v8.1` for `--v 8.1`, `midjourney/v7` for a V7 upscale). No Midjourney size is on record yet, so each reads NOT JUDGED until one is measured into [render-sizes.json](render-sizes.json).

### Nano Banana Pro · Seedream

These run only on Higgsfield's web plan, in the web app or through the CLI, and the plan is not held. Write the same full sentences as for GPT Image 2.5. Both honour hex codes approximately at best: upload a swatch strip of the palette as a reference image, and check the output with a colour picker. Seedream takes up to 14 reference images, which suits a consistent series.

### Recraft

On Recraft's own API the style is an enum, not an adjective: `vector_illustration` for SVG, `digital_illustration` for raster. Keep the prompt short and about the objects, and let the enum carry the idiom. Give the palette as data, `controls.colors` as RGB, and only the colours the scene uses.

```text
[INK] [26,26,46] · [PRIMARY] [58,124,165] · [ACCENT] [224,122,95] · [GROUND] [244,241,222] · [SOFT] [129,178,154]

prompt: [SUBJECT] [PLACED IN] [SETTING], [ONE OR TWO COMPOSITION DETAILS]
```

Once the project has a finished artwork, build a custom style from it and reuse it by id.

### Video — image to video

Record: `vault.clip-loop`.

Use the same still as the start frame and the end frame, so the prompt describes **motion only**, never the scene. Length, resolution and sound are the project's ruling. Kling caps a same-frame clip at 5 s.

```text
slow gentle drift: [ONE ELEMENT] rises and falls once, [A SECOND ELEMENT] shifts a few pixels, a single small [DETAIL] crosses the frame; camera locked, nothing else changes
```

Luma: put the still in both `keyframes.frame0` and `frame1`, with `loop: true`. Kling: Image to Video with "Add End Frame". Through `higgsfield.js`, `--set` the still's URL as `image_url` and as the end field, `last_image_url` for Kling 3.0 or `end_image_url` for Wan 2.7. `check-clip.py` reads both from the spend log.

## Repair shapes

The founder writes a repair as a brief delta. The next round's variants render from it, and it is never fired mid-round.

### `repair: too close to <entry>`

```text
The leader is too close to [ENTRY], especially [SUBJECT / COMPOSITION].
Re-open the reference and our actual render. Identify the combination that
makes them feel too similar. Keep [PRINCIPLES WE LIKE], but propose and
render a new product-relevant subject and composition. A similar object
in a different colour is not enough. Keep the leader for comparison.
```

### `repair: too generic against <direction>`

```text
The leader lost the character of [DIRECTION] and its references
([ENTRY IDS]). Re-open several screenshots and compare them with our actual
render. Identify three concrete principles we missed, such as image scale,
type hierarchy, density or material. Restore those principles while keeping
our own subject and composition. Explain the changes in terms of the
visible evidence.
```

## Optional: a finishing studio with presets

Tweak rung three in full (see [polish.md](polish.md)). Use it after the founder stops. Replace `[VERSION]` with the final's name or URL.

```text
I choose [VERSION]. Preserve that original and all previous comparisons.
Build a separate polish studio with a live preview and a robust, collapsible
tweak panel. Keep the chosen composition, product story and aesthetic.
Use the project's existing stack and our current design approach.

Add Original, Restrained and Expressive presets with meaningful differences.
Original must restore the unchanged chosen design. Each preset should set
real values I can then edit individually; show when I've customized a preset.

Give me a useful range of controls organized into these groups, adapting the
examples to this page:

- Typography and layout: a small selection of suitable available typefaces,
  headline weight, scale, line height and letter spacing; section spacing.
- Hero imagery: brightness, contrast, saturation, crop position, zoom and
  hero height. Keep text and controls independent of image adjustments.
- Graphic details: controls for the visual system this design actually uses.
  For a technical aesthetic, that might be grid pattern, cell size, intensity,
  annotation bracket size and accent-rule thickness. Choose equivalent
  details for other aesthetics rather than adding an unrelated grid.
- Color and buttons: accent color, button corners and relevant hover,
  focus and pressed treatments. Keep labels legible across color changes.
- Motion: off/subtle/expressive, entrance style (such as rise, fade or slide),
  travel distance, duration and stagger, plus individual switches for the
  opening sequence, section reveals and interaction feedback.
- Signature footer: original and enhanced treatments that fit this product,
  with useful graphic size, detail and animation controls. For a wireframe
  illustration, these might include line weight, glow and window details;
  do not force that graphic onto a different brand.

Every control must visibly affect its intended property. Show current values
and units. Use useful ranges, explain desktop-only controls, and disable or
hide settings that do not apply (for example, weight on a fixed-weight font).
The panel should be keyboard usable, scroll independently, and collapse on
small screens so I can inspect the page. Avoid controls added just for count.

Include compare-original/restore at the same preview width, replay entrance,
preview/jump to the signature footer, reset-to-preset, and hide/show panel.
Save custom settings and restore them on reopening. Include versioned JSON
export/import and a clean preview that retains the current custom values,
with a way back to the panel. Clearly explain where Save stores settings;
saving a browser preset does not apply a final design to source or publish it.
Keep older saved settings usable when adding controls, and reject invalid
imports without losing the current working settings.

Apply appearance changes live; use replay to review entrance timing.
Keep the page immediately usable, respect reduced motion and cancel prior
animations when replaying or changing settings. Motion Off must suppress
added movement. Keep the original page's navigation and product demo working.

Inspect desktop, intermediate and mobile renders. Verify controls against
actual rendered styles/behavior, representative range extremes and font
choices, presets, compare/restore, replay, reset, save/reload, import/export,
clean preview and reduced motion. Fix clipping, overlap or broken controls.

Open the studio and summarize what's available. Let me choose final settings
before applying them to a separate finished page without the tweak UI.
```

## The design record

Post it as the brief's closing comment at the stop step. The round records link from it and are not repeated.

```markdown
# Design record
## Brief
The five fields as written, the motion brief where there is one, then every brief delta in order:
## References inspected
Entry id / screenshot opened / observed evidence:
## Direction cards
Name / evidence / carry over / invent / avoid repeating / build scope:
## Rounds
Round / record comment link / drafts tag / leader / delta:
## Asset decisions
Purpose / tool / input references / exact prompt / output path:
## Selection and revision
Final candidate / tweak rung used / changes after the stop / prior version kept at:
## Verification
Viewport sizes / visual findings / interactions checked / remaining limitations:
## Build notes
Note / which round's critic or session found it / where it goes next:
```
