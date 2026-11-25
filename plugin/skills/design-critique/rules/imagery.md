# Rule records: imagery

Pictures, icons and drawn marks: curves, where shapes touch, stroke weight, text over photos and alt text. The form is [rules.md](../rules.md)'s.

### vault.curves-script
- applies-when: any; every curve the asset draws, and a traced or redrawn mark against its source
- question: Is every curve drawn as a true curve, with no run of straight segments standing in for one and no node where two curves meet whose tangents differ by more than the path's written precision allows, nor a node where a curve meets a straight line whose tangents differ by more than that but under 5.7°, save a corner or kink the source has or the brief names, and does a traced or redrawn mark lie within 0.1 px of the edge of an SVG source that draws no raster image, or 0.5 px of a raster source's, at the source's size?
- answered-by: script
- writes: curve
- yields-to: level 2
- source: the rule is the founder's, lucmoseley/mmm-infra#9 ("perfectly smooth … no matter how finely one zooms in"); 0.5 px, an agent's working figure he accepted on lucmoseley/mmm-infra#16, holds against a raster source (design-vault#195), borne out by potrace's half-pixel tracing criterion (Selinger 2003, §2.2), and the polygon test's thresholds are a building agent's guesses with no source; design-vault#195 sets 0.1 px for an SVG source, check-overlay.py's resolution (design-vault#73), and adds the node-tangent test font QA tools such as FontBakery run, with Red Arrow's allowance; design-vault#219 extends it to a curve meeting a straight line, under FontBakery's 0.1 rad bound for two lines read as one direction; strength: founder ruling for the rule, an accepted agent figure for 0.5 px that potrace's criterion bears out, tool research for 0.1 px, the node-tangent test and its 5.7° bound, unsourced guesses for the polygon test
- era: timeless
- owner: vault
- stage: value
- script: check-curves.js, then check-overlay.py <mark> <source>
- reasons: design-round/SKILL.md#6-per-asset-class
- ledger: IMG-7
- status: live

### vault.curves-look
- applies-when: any; the tightest bend of every curve
- question: Viewed at 8× zoom, is the tightest bend of every curve free of corners?
- answered-by: look
- writes: curve
- yields-to: vault.curves-script, level 2
- source: the rule is the founder's, lucmoseley/mmm-infra#9; the 8× zoom is an agent's working figure that no source sets, accepted with the other recommendations on lucmoseley/mmm-infra#16 (docs/research/house-audit-craft.md §1.2); strength: founder ruling for the rule, an accepted agent figure for the zoom
- era: timeless
- owner: vault
- stage: treatment
- target: Draw every curve as fitted curves, so its tightest bend shows no corner at 8× zoom.
- reasons: design-round/SKILL.md#6-per-asset-class
- ledger: IMG-7
- status: live

### vault.contacts-code
- applies-when: any; every place two elements touch
- question: Is each side of every contact drawn from one shared curve, or an offset of it, rather than two shapes drawn separately and placed by eye, and where two fills meet along that curve, are they one path, or does one run on under the other past it?
- answered-by: code
- writes: contact
- yields-to: vault.contacts-script, vault.contacts-seam, level 2
- source: the rule is the founder's, lucmoseley/mmm-infra#9; the shared curve is an agent's procedure, accepted with the other recommendations on lucmoseley/mmm-infra#16; one path or an underlap cures the conflation seam, where two fills on one exact edge each cover part of an edge pixel and the ground shows through (Khronos NV_path_rendering_shared_edge, Issue 1) (design-vault#195); strength: founder ruling for the rule, an accepted agent procedure and a rendering fact for its method
- era: timeless
- owner: vault
- stage: treatment
- target: Draw both sides of every contact from one shared curve or its offset; where two fills meet on it, make them one path or run one on under the other.
- reasons: design-round/SKILL.md#6-per-asset-class
- ledger: none
- status: live

### vault.contacts-script
- applies-when: any; every place two separately drawn paths nearly touch
- question: Where segments of two separately drawn shapes run alongside within 2 px of each other at the drawn size, does each pair either match to the paths' written precision with both fills on one side, or have one fill run on past the other's edge, the upper fill opaque, leaving no exact edge with a fill on each side, or, where a gap parts them, have an opaque shape painted after both fill it?
- answered-by: script
- writes: contact
- yields-to: level 2
- source: the rule is the founder's, lucmoseley/mmm-infra#9; the #262 ruling that a script lists the contacts (spec #324, user story 19); a fill on each side of one exact edge is the conflation seam (Khronos NV_path_rendering_shared_edge, Issue 1); an opaque shape painted later hides a gap or an underlap's lower edge, as each element paints over those before it (SVG 2, §3.3–3.4) (#356, #489); the 2 px is a guess no source sets (#324's Values); strength: founder ruling for the rule, house ruling for the script, a rendering fact for the seam and the cover, an unsourced guess for the 2 px
- era: timeless
- owner: vault
- stage: value
- script: check-curves.js --contacts
- reasons: design-round/SKILL.md#6-per-asset-class
- ledger: none
- status: live

### vault.contacts-seam
- applies-when: any; every place two separately drawn paths nearly touch
- question: On every key frame at scales 1×, 2× and 3×, with the contact's two shapes drawn alone over black and over white to find the ground in each pixel, does every contact keep the ground's width times its luminance contrast along the edge under 0.5 arcsec?
- answered-by: script
- writes: contact
- yields-to: vault.contacts-script, level 2
- source: the rule is the founder's, lucmoseley/mmm-infra#9; a thin line is seen once it reaches 0.5 arcsec (Hecht & Mintz 1939), its width times contrast form and the device pixel's angle at each ratio derived from it in docs/research/contact-seams.md (#340); strength: founder ruling for the rule, a vision-science floor for the threshold, derived figures for the angles
- era: timeless
- owner: vault
- stage: value
- script: check-seams.py
- reasons: design-round/SKILL.md#6-per-asset-class
- ledger: none
- status: live

### vault.contacts-look
- applies-when: any; every place two elements touch, on the first frame, every key frame and the last
- question: Rendered at device pixel ratios 1, 2 and 3, and each render magnified 4× without being drawn again, does every contact close with no gap, no overlap and no seam of the ground along an edge both sides share (the conflation seam, which a shared edge does not cure)?
- answered-by: look
- writes: contact
- yields-to: vault.contacts-code, vault.contacts-script, vault.contacts-seam, level 2
- source: the rule is the founder's, lucmoseley/mmm-infra#9; the 4× is an agent's working figure, accepted with the other recommendations on lucmoseley/mmm-infra#16 (design-vault#195); strength: founder ruling for the rule, an accepted agent figure for the magnification
- era: timeless
- owner: vault
- stage: treatment
- target: Close every contact with no gap, overlap or seam of the ground at device pixel ratios 1, 2 and 3, on every key frame.
- reasons: design-round/SKILL.md#6-per-asset-class
- ledger: none
- status: live

### vault.stroke-weight
- applies-when: web-surface; every interface icon, border and focus ring
- question: Does each icon's stroke match the weight of the text beside it, do borders and icon strokes sit in one line-weight band thinner than the focus ring, and does a light icon on a dark ground take a lighter stroke?
- answered-by: builder
- writes: stroke weight
- yields-to: level 2
- source: Apple HIG Icons and SF Symbols, on matching icon and text weight; Material Symbols, on a lower grade for a light symbol on a dark ground; the band and the ring's step above it are the house's inference, which no source states; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Match icon weight to the adjacent text, keep borders and icon strokes in one band below the focus ring's width, and lighten an icon's stroke on a dark ground.
- reasons: design-critique/references/surface-styling.md#interactions
- ledger: COL-71, IMG-5, IMG-10, NEW3-77, STA-4, SUR-1, SUR-5, TYF-69
- status: live

### vault.text-on-photo
- applies-when: web-surface; every piece of text set over a photograph or a varied image
- question: Is text over a photograph or varied image set on a panel, or over a scrim that holds its contrast against the worst pixel under it?
- answered-by: builder
- writes: text over image
- yields-to: vault.contrast
- source: W3C Understanding SC 1.4.3 Contrast (Minimum), on text over images; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: treatment
- target: Put text over a busy photograph on a panel, or darken or lighten the image under it until the worst pixel clears the text's contrast floor.
- reasons: design-critique/references/surface-styling.md#one-scrim-token
- ledger: BTN-10, COL-11, IMG-129, SUR-104
- status: live

### vault.decorative-alt
- applies-when: web-surface; every image that is decoration alone
- question: Does every image that is pure decoration carry an empty `alt=""`?
- answered-by: whole-page
- writes: decorative alt text
- yields-to: none
- source: W3C WAI Images Tutorial, decorative images; strength: WCAG 2.2 A technique
- era: timeless
- owner: vault
- stage: treatment
- target: Give a decorative image `alt=""`, or set it as a CSS background.
- reasons: design-round/references/impeccable.md#sources-for-the-rules-the-house-enforces
- ledger: IMG-27, IMG-93
- status: live

### vault.render-size
- applies-when: brand-art; every render
- question: Is the render at least as wide and as tall as its model's largest output for the requested aspect ratio, as render-sizes.json records it?
- answered-by: script
- writes: size
- yields-to: level 2
- source: the #262 ruling that a script checks a render's size against its model's largest output (spec #324, user story 1, so a hero never ships at a size the model could have doubled); each size is the model's docs or a measured render, cited beside it in render-sizes.json; strength: house ruling for the rule, docs or a measurement for each size
- era: timeless
- owner: vault
- stage: value
- script: check-render.py
- reasons: design-round/references/roster.md#the-model-selection-rule-design-vault52
- ledger: none
- status: live

### vault.render-checkerboard
- applies-when: brand-art; every render whose brief asks for a transparent background
- question: Is the render free of a painted checkerboard, a two-tone grid drawn where the background should be transparent?
- answered-by: script
- writes: ground
- yields-to: level 2
- source: the #262 ruling that a script finds a painted checkerboard where transparency was asked, by cell-mean alternation or a 2D FFT peak (spec #324, user story 2, so a fake transparent background never reaches a page); Grok Imagine 2.0 painted one in 9 of 9 transparency tries (IMG.LY benchmark, docs/research/image-model-profiles-a.md) and in 3 of 3 of #332's; the detector's figures are set on fixtures and those renders; strength: house ruling for the rule; the detector's figures untraced
- era: timeless
- owner: vault
- stage: value
- script: check-render.py
- reasons: design-round/references/roster.md#cut-out-design-vault54
- ledger: none
- status: live

### vault.baked-ui-look
- applies-when: brand-art; every render
- question: Is the render free of anything a viewer would read or press painted into it: words or letter-like marks, however small or garbled, logos, buttons, controls and invented figures or data?
- answered-by: look
- writes: baked
- yields-to: level 2
- source: design-round §6's rule that copy, controls and data stay live, never baked into an image (spec #324, user stories 3 and 30); a look question rather than a script because PaddleOCR's PP-OCRv4 text detector flagged at least 18 of 64 clean images at every setting that found the text on #262's fixtures (#327, docs/research/baked-text-trial.md); strength: house ruling for the rule, a measurement for not answering it by script
- era: timeless
- owner: vault
- stage: treatment
- target: Leave every word, logo, control and figure out of the render, and set each as live text or place it as its own asset over the art.
- reasons: design-round/SKILL.md#6-per-asset-class
- ledger: none
- status: live

### vault.headline-plain-look
- applies-when: brand-art; every render whose brief leaves an area plain for a headline
- question: Inside the area the headline will take, is the art plain at the scale of a letter, with no object, edge or fine texture under it, a smooth gradient counting as plain?
- answered-by: look
- writes: plain area
- yields-to: level 2
- source: #338's research (docs/research/render-palette-plain-area.md §2): texture masks letters most in a band of sizes scaled to the strokes (Majaj et al. 2002) and the global masking index (Scharff, Hill & Ahumada 2000) misreads a smooth painted gradient as texture; no study or standard sets a texture limit for text over an image, so the line is the critic's judgement, no number having been found (#339 closed not planned; #350 ruled no look test); strength: published research for what to look at, the critic's judgement for the line
- era: timeless
- owner: vault
- stage: treatment
- target: Prompt and pick renders whose headline area is an even ground or a smooth gradient, every object, edge and fine texture kept outside where the letters will sit.
- reasons: design-round/references/prompts.md#art-direction--the-model-agnostic-template
- ledger: none
- status: live

### vault.focal-crop
- applies-when: brand-art or web-surface; art whose brief declares a focal box
- question: At every width of the sweep, does the page show the whole of the focal box the art's brief declares, within the art's element, its clipping ancestors and the screen's sides?
- answered-by: script
- writes: crop
- yields-to: level 2
- source: the #262 ruling that a script checks the art keeps its focal element at every width (spec #324, user story 8); "wholly visible at every width" is the plain reading of "keeps the focal element", untraced; MDN `object-position` and web.dev, "Responsive images" §Constrain, on choosing which part of a cropped image stays in view; strength: house ruling for the rule, untraced for its bound
- era: timeless
- owner: vault
- stage: treatment
- target: Size and position the art, by object-fit and object-position or background-size and background-position, so the brief's focal box stays wholly in view at every width.
- script: check-layout.py --focal <selector>=x,y,w,h
- reasons: design-round/SKILL.md#1-the-brief
- ledger: IMG-137
- status: live

### vault.icon-use
- applies-when: web-surface; every icon on the page other than a logo
- question: Does each icon mark an action or a piece of information a visitor looks for (a phone number, a download, a share) rather than decorate, take the conventional symbol for that one meaning and no other, and carry a visible text label, save the few icons nearly everyone knows (home, print, the magnifier for search) and the icon-only controls `vault.carry-act` allows, each with an accessible name?
- answered-by: look
- writes: icon use
- yields-to: vault.carry-act, level 2
- source: GOV.UK Design System, Images, Icons (updated March 2023, as read Oct 2026): "Avoid using icons in most cases. People can understand a single icon to mean different things", "helpful to include a visible text label alongside any icons", "Do not use a single icon to represent more than one thing"; USWDS Icon: "Use icons only in a common or conventional way"; Apple HIG Icons (9 Jun 2025): "familiar visual metaphors" and standard symbols for common actions; NN/g, Harley, "Icon Usability" (2014): only home, print and search are near-universal, and "Icons Need a Text Label"; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: function
- target: Use an icon only for an action or a fact visitors look for, draw it with the conventional symbol and use that symbol for nothing else, and label it in text unless it is home, print or search.
- reasons: design-critique/references/house-principles.md#icons-earn-their-place
- ledger: IMG-18, IMG-22
- status: staged

### vault.current-icon
- applies-when: web-surface; every nav or tab set whose items carry icons and mark the current or selected one
- question: Does the current or selected item's icon take its filled form, drawn with at least a quarter more ink than the median of the set's other icons?
- answered-by: script
- writes: current item icon fill
- yields-to: vault.carry-select, level 2
- source: Apple HIG SF Symbols (updated Jul 2025, as read Oct 2026): "use the fill variant to indicate selection"; Google for Developers, Material Symbols guide (2024): "To convey a state transition, use the fill axis"; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Switch the selected tab or nav item's icon to its filled form.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- parts: icon
- reasons: design-critique/references/surface-styling.md#outline-and-filled-icons
- ledger: IMG-29
- status: staged

### vault.icon-fill
- applies-when: web-surface; every interface icon with an outline and a filled form
- question: Does each icon take its outline form by default, beside text, in toolbars and lists, and its filled form only for a selected or current item (the current tab or nav item) or the few statuses that must draw the eye, never filled throughout?
- answered-by: look
- writes: icon fill
- yields-to: vault.current-icon, vault.carry-select, level 2
- source: Apple HIG SF Symbols (updated Jul 2025, as read Oct 2026): outline "works well in toolbars, lists, and other places where you display a symbol alongside text"; "use the fill variant to indicate selection"; "an iOS tab bar prefers the fill variant, whereas a toolbar takes the outline variant"; Google for Developers, Material Symbols guide (2024): the fill axis renders "both unfilled and filled states. To convey a state transition, use the fill axis"; Atlassian Lozenge: "Use filled icons intentionally to draw user attention ... Don't overuse filled icons"; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Draw icons outlined by default and beside text; switch the selected tab or nav item's icon to its filled form, and fill only the few status icons that must stand out.
- parts: icon
- reasons: design-critique/references/surface-styling.md#outline-and-filled-icons
- ledger: IMG-29, NEW2-67
- status: staged

### vault.icon-optical-size
- applies-when: web-surface; every interface icon drawn at more than one size, or at a size other than its design size
- question: Does each icon drawn at another size keep its intended stroke weight, by the set's optical-size axis, a drawing made for that size or a fixed stroke, rather than a stroke scaled with the icon?
- answered-by: script
- writes: icon stroke across sizes
- yields-to: vault.stroke-weight, level 2
- source: Google for Developers, Material Symbols guide (2024), opsz axis: "For the image to look the same at different sizes, the stroke weight (thickness) changes as the icon size scales. Optical size offers a way to automatically adjust the stroke weight"; Lucide docs, Stroke width (as read Oct 2026): by default the stroke "will be relative to the size of the icon"; `nonScalingStroke` keeps it "constant no matter the size of the icon"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Size icons with the set's optical-size axis where it has one; otherwise set the stroke for each size, or use a non-scaling stroke, so a larger icon does not grow heavier than the text beside it.
- parts: icon
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/surface-styling.md#icon-stroke-across-sizes
- ledger: NEW3-78
- status: live

### vault.image-earns
- applies-when: web-surface; every photo and illustration on the page that is not an icon or the logo
- question: Does each image carry information the visitor uses (the product, the place, the real person, the evidence) or a feeling the brief names, none being generic stock or AI filler set to fill space?
- answered-by: look
- writes: image presence
- yields-to: level 2
- source: NN/g, Nielsen, "Photos as Web Content" (2010, reviewed 13 Aug 2026, as read Oct 2026): users "pay close attention to photos and other images that contain relevant information", ignore "fluffy pictures used to 'jazz up' web pages", "pure filler", and gave real staff portraits more time than longer bios; strength: domain evidence
- era: timeless
- owner: vault
- stage: function
- target: Use an image only where it shows what the visitor came to judge or a feeling the brief names; prefer a real photo of the person, place or product to generic stock or AI art; leave the slot empty rather than fill it.
- reasons: design-critique/references/house-principles.md#images-earn-their-place
- ledger: IMG-74
- status: staged

### vault.map-list
- applies-when: web-surface; a results page for things a visitor compares by place (stays, venues, shops), at widths with room for two columns
- question: Does the results page show the list beside an interactive map in one view on the page itself, not the map in a separate tab or an overlay?
- answered-by: look
- writes: map and list layout
- yields-to: none
- source: Baymard, Collins, "The Optimal Layout for Hotel & Property Rental Search Results" (8 Feb 2022, as read Oct 2026): a "'Split View' layout containing the property listings side by side with an interactive map", directly on the results page and never in an overlay; 65% of users on list-default sites did not use a map, 95% used Hilton's split view; mobile not tested; strength: domain evidence
- era: timeless
- owner: vault
- stage: role
- target: On a wide results page for things chosen by place, put the list and an interactive map side by side on the page; never put the map behind a tab or in an overlay at those widths.
- reasons: design-critique/references/layout-and-data.md#list-beside-map
- ledger: IMG-111
- status: staged

### vault.icon-vector
- applies-when: web-surface; every interface icon: icons in buttons, links, navigation and lists
- question: Is every interface icon an SVG (inline, a sprite or an `.svg` file), with no PNG, JPEG, WebP or GIF standing in for one?
- answered-by: script
- writes: icon file format
- yields-to: level 2
- source: Apple HIG, Icons, Best practices (as read Oct 2026): "If you create a custom interface icon, use a vector format like PDF or SVG", while PNG "doesn't support scaling, so you have to supply multiple versions"; web.dev, Learn Design, "Icons", Scalable vector graphics: "If you use an SVG, it's responsive by default"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Draw every interface icon as SVG.
- script: check-load.py <page> --files --out <dir> [--parts <declaration>]
- parts: icon
- reasons: design-critique/references/platform-defaults.md#icons-are-vector
- ledger: IMG-16
- status: staged

### vault.flat-art-vector
- applies-when: web-surface; every simple flat illustration: spot art of a few flat shapes
- question: Is every simple flat illustration drawn as vector art in SVG rather than saved as a raster image?
- answered-by: code
- writes: illustration file format
- yields-to: vault.icon-vector, level 2
- source: Apple HIG, Icons, Best practices (as read Oct 2026): "If you create a custom interface icon, use a vector format like PDF or SVG", while PNG "doesn't support scaling, so you have to supply multiple versions"; web.dev, Learn Design, "Icons", Scalable vector graphics: "If you use an SVG, it's responsive by default"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Draw simple flat illustrations as SVG; keep raster files for photographs and art with texture or shading.
- parts: image
- reasons: design-critique/references/platform-defaults.md#icons-are-vector
- ledger: IMG-16
- status: staged

### vault.favicon
- applies-when: web-surface; the document head of every page
- question: Does the head link an SVG icon with `sizes="any"` and a 48 × 48 `favicon.ico` fallback (`rel="icon"`), and a 180 × 180 PNG `rel="apple-touch-icon"`, each file present?
- answered-by: script
- writes: favicon and touch icon
- yields-to: level 2
- source: GOV.UK Design System, Page template, head (as read Oct 2026): `favicon.ico` at `sizes="48x48"`, `favicon.svg` at `sizes="any"`, `apple-touch-icon` a 180 px PNG; MDN, `rel` "icon" (as read Oct 2026): the browser picks among icons by `media`, `type` and `sizes`, and iOS ignores `rel="icon"` for an `apple-touch-icon`; WHATWG HTML, Link type "icon": with none linked a browser may fetch `/favicon.ico`; strength: design-system guidance and web platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: value
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#favicon-and-touch-icon
- ledger: IMG-37
- status: staged

### vault.pinch-anchor
- applies-when: web-surface; every image or surface with its own pinch zoom: a product gallery's zoom, a lightbox, a map or plan
- question: Does a custom pinch zoom scale about the point midway between the visitor's two fingers, so that point stays under them as they spread?
- answered-by: script
- writes: zoom origin
- yields-to: vault.reflow, level 2
- source: rauno.me, Freiberg, "Invisible Details of Interaction Design" (Jul 2023), §Metaphors: "the interface needs to first establish an anchor point from where the zooming originates", drawn "on the center of both" fingers; that the page's own zoom stays is `vault.reflow`'s, by W3C ACT rule b4f0c3; strength: expert craft
- era: timeless
- owner: vault
- stage: treatment
- target: Anchor a custom pinch zoom at the midpoint between the two fingers and keep it under them; claim the gesture with `touch-action` on the zoomable surface alone.
- script: check-state.py, its pinch line
- parts: zoomable
- reasons: design-critique/references/platform-defaults.md#pinch-zoom-anchors-between-the-fingers
- ledger: IMG-101
- status: live

### vault.image-scaling
- applies-when: web-surface; every image the round declares as the `pixel-image` part
- question: Is each image the round declares as `pixel-image` set to `image-rendering: pixelated`, so it scales without blur?
- answered-by: script
- writes: image-rendering
- yields-to: level 2
- source: MDN, `image-rendering` (as read Oct 2026): `smooth` is "intended for images such as photos", `crisp-edges` and `pixelated` scale by nearest neighbour for "pixel art or line drawings"; web-features (as read Oct 2026): `pixelated` Baseline widely available since 2024-04-05, `crisp-edges` Baseline newly available 2026-05-07 (Chrome 148), so `pixelated` reaches every current browser; strength: web platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Set `image-rendering: pixelated` on enlarged pixel art, codes and hard-edged diagrams; leave photographs at the default.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: pixel-image
- reasons: design-critique/references/platform-defaults.md#hard-edged-images-scale-without-smoothing
- ledger: IMG-143
- status: live

### vault.pixel-image-kind
- applies-when: web-surface; every raster image shown larger than its natural size whose content is pixels or hard edges: pixel art, a QR or bar code, a screenshot of interface or a line diagram
- question: Is each such image declared as the round's `pixel-image` part, and is no photograph declared as one?
- answered-by: look
- writes: image-rendering
- yields-to: vault.image-scaling, level 2
- source: MDN, `image-rendering` (as read Oct 2026): `smooth` is "intended for images such as photos", `crisp-edges` and `pixelated` scale by nearest neighbour for "pixel art or line drawings"; web-features (as read Oct 2026): `pixelated` Baseline widely available since 2024-04-05, `crisp-edges` Baseline newly available 2026-05-07 (Chrome 148), so `pixelated` reaches every current browser; strength: web platform documentation
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Set `image-rendering: pixelated` on enlarged pixel art, codes and hard-edged diagrams; leave photographs at the default.
- reasons: design-critique/references/platform-defaults.md#hard-edged-images-scale-without-smoothing
- ledger: IMG-143
- status: live

### vault.rtl-fixed-icons
- applies-when: web-surface; every icon on a page in a right-to-left language, rendered with `dir="rtl"`
- question: In the right-to-left render, is every icon named as a clock, check mark, search glass, media control, slash or logo kept in its left-to-right form?
- answered-by: script
- writes: fixed icon mirroring
- yields-to: none
- source: Apple HIG, Right to left, Interface icons (as read Oct 2026): "Don't flip logos or universal signs and marks", avoid flipping real-world objects such as clocks, keep a slash; Material Design 1, Bidirectionality (m1.material.io): never mirror clocks or right-handed objects, and "Do not mirror media playback buttons and the media progress indicator"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: In right-to-left, keep logos, check marks, slashes, clocks, the search glass and media playback controls as they are.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- parts: icon
- reasons: design-critique/references/platform-defaults.md#right-to-left-icons
- ledger: IMG-28
- status: staged

### vault.rtl-icons
- applies-when: web-surface; every icon on a page in a right-to-left language, rendered with `dir="rtl"`
- question: In the right-to-left render, are icons showing reading direction or forward and back movement mirrored (back, next, previous, a text-lines icon, a volume slider), while logos, check marks, slashes, clocks and clockwise arrows, right-handed objects such as a search glass, and media playback buttons and their progress bar keep their left-to-right form?
- answered-by: look
- writes: icon mirroring
- yields-to: vault.rtl-fixed-icons
- source: Apple HIG, Right to left, Interface icons and Controls (as read Oct 2026): flip icons for text or reading direction and forward or backward motion, "Don't flip logos or universal signs and marks", avoid flipping real-world objects such as clocks, keep a slash; Material Design 1, Bidirectionality (m1.material.io): mirror back and forward buttons and icons showing forward movement, never clocks, refresh, history, right-handed objects or slashes, and "Do not mirror media playback buttons and the media progress indicator"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: In right-to-left, mirror icons that show reading direction or forward and back; keep logos, check marks, slashes, clocks, right-handed tools and media playback controls as they are.
- parts: icon
- reasons: design-critique/references/platform-defaults.md#right-to-left-icons
- ledger: IMG-28
- status: staged

### vault.rtl-images
- applies-when: web-surface; every photograph, illustration and piece of art on a page in a right-to-left language
- question: In the right-to-left render, does every photograph, illustration and piece of art show unflipped, with any image whose content follows reading direction drawn again rather than mirrored?
- answered-by: script
- writes: image mirroring
- yields-to: none
- source: Apple HIG, Right to left, Images (as read Oct 2026): "Avoid flipping images like photographs, illustrations, and general artwork. Flipping an image often changes the image's meaning"; for content tied to reading direction, "consider creating a new version"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Never mirror a photograph or illustration for right-to-left; make a new version of one whose content follows reading direction.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: image
- reasons: design-critique/references/platform-defaults.md#right-to-left-images
- ledger: IMG-146
- status: staged

### vault.rtl-image-order
- applies-when: web-surface; every set of images in a meaningful order (chronological, ranked, numbered steps, a gallery's sequence) on a page in a right-to-left language
- question: In the right-to-left render, does an ordered image set run from right to left, its first item at the right?
- answered-by: script
- writes: image set order
- yields-to: none
- source: Apple HIG, Right to left, Images (as read Oct 2026): "Reverse the positions of images when their order is meaningful … chronological, alphabetical, or favorite"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Lay an ordered image set out in the page's direction, with flex or grid in source order, so right-to-left starts at the right.
- script: check-layout.py <page> --out <dir> --records
- parts: image
- reasons: design-critique/references/platform-defaults.md#right-to-left-image-order
- ledger: IMG-147
- status: staged

### vault.video-captions
- applies-when: web-surface; every `video` element not marked `muted`
- question: Does every `video` that plays sound carry a captions track, a `track` with `kind="captions"` or `kind="subtitles"`?
- answered-by: script
- writes: video captions track
- yields-to: none
- source: WCAG 2.2 success criteria 1.2.2 Captions (Prerecorded), level A, and 1.2.4 Captions (Live), level AA; HTML Living Standard, the `track` element, its `kind` keywords `captions` and `subtitles`; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Give every video that plays sound a `track kind="captions"`.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#captions-transcripts-and-audio-description
- ledger: IMG-154
- status: staged

### vault.media-alternatives
- applies-when: web-surface; every video, audio clip and podcast the page plays, save one that is itself an alternative to text on the page and is labelled so
- question: Does every prerecorded video with sound carry captions and audio description (or a described version), every live video with sound carry captions, every prerecorded audio-only clip a transcript, and every prerecorded silent video a transcript or an audio track, with the transcript on the page beside the player or linked from it?
- answered-by: code
- writes: media text alternatives
- yields-to: vault.video-captions
- source: WCAG 2.2 success criteria 1.2.1 Audio-only and Video-only (Prerecorded), 1.2.2 Captions (Prerecorded) and 1.2.3 Audio Description or Media Alternative (Prerecorded), all level A, and 1.2.4 Captions (Live) and 1.2.5 Audio Description (Prerecorded), level AA; web.dev, Learn Accessibility, "Video and audio": transcript in context beside the player, or linked; strength: WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: function
- target: Give prerecorded video captions and audio description, live video captions, audio-only a transcript, silent video a transcript or narration, and put each transcript beside its player or link to it.
- reasons: design-critique/references/platform-defaults.md#captions-transcripts-and-audio-description
- ledger: IMG-154
- status: live

### vault.flash-limit
- applies-when: web-surface or has-motion; every video, animation, canvas and image that flashes or strobes, and a motion asset
- question: Does nothing on the page flash more than three times in any one second, or does every faster flash stay below the general and red flash thresholds: no more than a quarter of any 10° field, about 341 × 256 px at 1024 × 768?
- answered-by: script
- writes: flashing
- yields-to: none
- source: WCAG 2.2 success criterion 2.3.1 Three Flashes or Below Threshold, and its glossary's general flash and red flash thresholds; Understanding 2.3.1, technique G15 (a tool such as PEAT); strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Keep every flash to three a second or fewer, or small enough to fall below WCAG's flash area; edit media that strobes.
- script: check-flow.py <page> --out <dir> --records [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#flashing-stays-below-three-a-second
- ledger: IMG-157
- status: staged

### vault.space-plays
- applies-when: web-surface; every video and audio player
- question: Does Space toggle play and pause while the player or its play button has focus, as a native `video` element with `controls` does, with no page-wide single-key shortcut that fires while focus is elsewhere?
- answered-by: script
- writes: play and pause key
- yields-to: level 2
- source: Apple HIG, Playing video, Best practices (as read Oct 2026): "people expect to press Space on a connected keyboard to play or pause", and a custom player follows the system player; measured on design-vault#276 (docs/research/platform-defaults.md), Chromium 149 only; WCAG 2.2 Understanding 2.1.4: a shortcut active only while its component has focus meets the criterion; strength: design-system guidance and a measurement
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Use the browser's `<video controls>`, or a custom player whose focused player and play button toggle on Space; scope any single-key shortcut to the focused player.
- script: check-state.py, its space line
- parts: video
- reasons: design-critique/references/platform-defaults.md#space-plays-and-pauses
- ledger: NEW1-70
- status: live

### vault.background-image-role
- applies-when: web-surface; every element announced as an image: `role="img"`, or a name on an element with no role
- question: Does no element announced as an image draw its picture only as a CSS background?
- answered-by: script
- writes: announced image element
- yields-to: none
- source: WCAG 2.2 success criterion 1.1.1 Non-text Content, failure F3, conveying information "exclusively using CSS background images"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Draw every picture that is announced as an image as an `img`, `picture` or `svg`, never as a CSS background.
- script: check-dom.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/platform-defaults.md#content-images-are-elements
- ledger: NEW2-70
- status: staged

### vault.content-image
- applies-when: web-surface; every image a visitor needs to understand the page: a product, a person, a place, a chart, a picture of text
- question: Is every image that carries content an `img`, `picture` or an `svg` with `role="img"`, with alt text, none of it only a CSS background?
- answered-by: code
- writes: image element
- yields-to: vault.background-image-role
- source: WCAG 2.2 success criterion 1.1.1 Non-text Content, failure F3, conveying information "exclusively using CSS background images"; MDN, Backgrounds and borders, accessibility (as read Oct 2026): background images "should be purely decorative. Any important content should be part of the HTML page"; strength: WCAG 2.2 A
- era: timeless
- owner: vault
- stage: function
- target: Put every image that carries content in an `img` or `picture` with alt text; use `background-image` for decoration alone.
- reasons: design-critique/references/platform-defaults.md#content-images-are-elements
- ledger: NEW2-70
- status: live

### vault.illustration-detail
- applies-when: any; every illustration the asset draws or commissions
- question: Does each illustration use as few elements as carry its message, in flat fills from the palette or its tints, with no shadow or gradient save to show depth or a telling feature, and the same line widths, radii and colours across a set?
- answered-by: look
- writes: illustration detail
- yields-to: level 2
- source: GOV.UK Design System, Images, "Creating illustrations" (as read Oct 2026): "Use as few visual elements as possible to communicate your message", "Use flat blocks of colour", "Avoid using shadows or gradients, except when needed to show a distinctive feature of an object or to communicate layering or depth", consistent "colours, line widths and border radiuses"; strength: design-system guidance
- era: timeless
- owner: vault
- stage: treatment
- target: Draw illustrations with the fewest elements that carry the message, flat palette fills, no decorative shadow or gradient, and one set of line widths and radii.
- reasons: design-critique/references/interaction-and-forms.md#illustrations-stay-simple
- ledger: IMG-80
- status: staged

### vault.photo-text-fix
- applies-when: web-surface; every piece of text set over a photograph, gradient or other varied image
- question: Is the fix for text over an image chosen for the worst image the slot can hold and the worst place the text can land, by the lookup below, with a solid `background-color` set behind the image for when it fails to load?
- answered-by: builder
- writes: text-over-image fix
- yields-to: vault.text-on-photo, vault.contrast
- source: NN/g, "Text Over Images" (2015, updated 13 Jan 2026): plan for "the worst-case background image and text placement", a floor fade, blur or semi-opaque box, a box raised from 30% to 50% to pass; W3C technique G18, a halo or fog, and failure F83, measured at the darkest or lightest part of the image (WCAG 2.2, 2023); MDN Backgrounds and borders, a fallback `background-color` (28 Sep 2026); Apple HIG Image views, a text shadow or background layer; strength: design-system guidance over WCAG 2.2 AA
- era: timeless
- owner: vault
- stage: treatment
- inputs: whether the slot holds one fixed image or any image (a content-managed slot); where the text sits; the text's size
- output: one fixed image that clears the floor at its worst pixel, no fix; text on an image's lower part, a darkening floor fade; text over any image a slot can hold, a semi-opaque panel raised until the worst image clears, or a scrim over the whole image; a text shadow or halo alone only where the worst image then clears
- target: Pick the fix for the worst image the slot can take: a floor fade under text at the bottom, a panel or scrim for any image, a shadow only where the worst image clears with it; and set a solid background colour behind the image.
- reasons: design-critique/references/edges-and-contrast.md#edges-and-text-over-images
- ledger: COL-11
- status: live

### vault.edge-over-image
- applies-when: web-surface; every control, chip or icon set over a photograph or busy ground
- question: Does each control, chip or icon over a photograph sit on a solid or near-solid backing plate that holds 3:1 against every colour the image can put beside it, rather than on a hairline or a shadow alone?
- answered-by: script
- writes: control over an image
- yields-to: vault.control-edges, level 2
- source: Dannaway, "UI design tips", tip 7 (2026): an icon over a photo given a solid white backing so it passes "regardless of the photo"; W3C Understanding SC 1.4.11 (WCAG 2.2, 2023), 3:1 against every adjacent colour, and SC 2.4.13, "a solid box with a border to guarantee there is sufficient contrast across variations of background images" for a focus indicator; strength: expert writing, applying WCAG 2.2 SC 1.4.11
- era: timeless
- owner: vault
- stage: treatment
- target: Put a control or chip that sits on a photo on its own solid or near-solid plate, not on a hairline or shadow.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- reasons: design-critique/references/edges-and-contrast.md#edges-and-text-over-images
- ledger: SUR-43
- status: staged

### vault.image-edge
- applies-when: web-surface; every photo, avatar and thumbnail whose own edge can match the ground it sits on
- question: Does such an image take a 1 px hairline in the text colour at about 8–15% alpha, flipped per theme, drawn inside it with `outline` and `outline-offset: -1px`, and solid in a high-contrast theme?
- answered-by: script
- writes: image hairline
- yields-to: level 2
- source: GitHub Primer Avatar, `box-shadow: 0 0 0 1px` at 15% alpha, the emphasis colour in high-contrast themes (@primer/primitives 11.10.0, Avatar.module.css 14 Oct 2024); Shopify Polaris Thumbnail, a 1px 8% inset ring on an overlay above the image (9 Jul 2024, archived); Krehel, "Details that make interfaces feel better" (on or before Mar 2026), a 1px 10% outline inset by `outline-offset: -1px`, black or white by mode; strength: design-system guidance
- era: dated 2027-10-19
- owner: vault
- stage: treatment
- target: Give photos, avatars and thumbnails a 1 px inset hairline of the text colour at about 10% alpha, flipped per theme, drawn with an outline so forced colours keeps it.
- script: check-style.py <page> --out <dir> [--parts <declaration>]
- parts: image
- reasons: design-critique/references/edges-and-contrast.md#edges-and-text-over-images
- ledger: SUR-108
- status: live
