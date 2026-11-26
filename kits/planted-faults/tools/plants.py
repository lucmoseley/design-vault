#!/usr/bin/env python3
import json
import sys
import pathlib

FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap">'

PAGES = {
    "r2-v1p": {
        "src": "src/r2/v1-counsels-paper/index.html",
        "out": "fixtures/r2-v1p/index.html",
        "faults": [
            {
                "id": "v1p-F",
                "kind": "function",
                "sub": "missing action",
                "what": "The 'Write to me directly' email strip is removed from the first screen; with no email in the footer, the page now offers no way at all to contact Mark.",
                "edits": [
                    (
                        """      <div class="address">
        <span class="address-label">Write to me directly</span>
        <a href="mailto:Mark.Moseley@MMMinfra.com">Mark.Moseley<wbr>@MMMinfra.com</a>
      </div>
""",
                        "",
                    )
                ],
            },
            {
                "id": "v1p-G",
                "kind": "global",
                "sub": "hierarchy broken across sections",
                "what": "The article specimen's title ('The World's Best Public-Private Partnership Law') is set at 88 px, medium weight: louder and larger than the hero line, so a lower section outranks the first screen.",
                "css": ".prose .art-title{font-size:88px!important;line-height:1.02!important;font-weight:500!important;letter-spacing:-0.02em}@media (max-width:700px){.prose .art-title{font-size:46px!important}}",
            },
            {
                "id": "v1p-T",
                "kind": "type",
                "sub": "third typeface",
                "what": "The article's subhead ('So, what are the key chapter topics?') and the 'Download' label are set in Archivo Black, a heavy geometric display sans: a third face clashing with the Newsreader/Public Sans pair.",
                "fonts": True,
                "css": ".prose h3:not(.art-title),.prose .downloads h4{font-family:'Archivo Black',sans-serif!important;font-weight:400!important;font-size:26px!important;letter-spacing:0}",
            },
            {
                "id": "v1p-C",
                "kind": "colour-surface",
                "sub": "off-palette ground",
                "what": "The Motion section sits on a saturated lavender ground (#CDB8F5), a colour outside the palette of paper, grey, blue and pad yellow.",
                "css": "section[aria-labelledby=h-motion]{background:#CDB8F5;padding:48px 24px}",
            },
            {
                "id": "v1p-R",
                "kind": "treatment",
                "sub": "like parts treated unlike",
                "what": "The four palette swatches have four different corner treatments (square, 12 px, fully round, 4 px with a 3 px blue border), so like parts look unlike.",
                "css": ".swatch:nth-child(2) .swatch-chip{border-radius:12px}.swatch:nth-child(3) .swatch-chip{border-radius:50%}.swatch:nth-child(4) .swatch-chip{border-radius:4px;border:3px solid #0070C0!important}",
            },
        ],
    },
    "r2-v3p": {
        "src": "src/r2/v3-annotated-brief/index.html",
        "out": "fixtures/r2-v3p/index.html",
        "faults": [
            {
                "id": "v3p-F",
                "kind": "function",
                "sub": "dead action",
                "what": "The hero's 'Write to me' button and the address beside it look exactly as before but are no longer a link: nothing happens on click (the parts map lists them as not actable).",
                "edits": [
                    (
                        """      <a class="action" href="mailto:Mark.Moseley@MMMinfra.com">
        <span class="btn">Write to me</span>
        <span class="addr">Mark.Moseley@MMMinfra.com</span>
      </a>""",
                        """      <span class="action">
        <span class="btn">Write to me</span>
        <span class="addr">Mark.Moseley@MMMinfra.com</span>
      </span>""",
                    )
                ],
            },
            {
                "id": "v3p-G",
                "kind": "global",
                "sub": "two primary actions in one view",
                "what": "A second filled blue button, 'Book a consultation', sits beside 'Write to me' at the same size and weight: two primary actions in the first view.",
                "edits": [
                    (
                        """        <span class="addr">Mark.Moseley@MMMinfra.com</span>
      </span>
    </div>""",
                        """        <span class="addr">Mark.Moseley@MMMinfra.com</span>
      </span>
      <a class="action" href="#consult" style="margin-left:16px"><span class="btn">Book a consultation</span></a>
    </div>""",
                    )
                ],
            },
            {
                "id": "v3p-T",
                "kind": "type",
                "sub": "tracked capitals for running text",
                "what": "The hero's second paragraph ('I advise multilateral development banks…') is set in tracked sans capitals, bold: three-plus lines of all-caps running text that is slow to read, against the brief's 'never tracked capitals'.",
                "css": ".hero p.body.r2{text-transform:uppercase;letter-spacing:.12em;font-family:'Public Sans',sans-serif;font-weight:600;font-size:15px;line-height:1.7}",
            },
            {
                "id": "v3p-C",
                "kind": "colour-surface",
                "sub": "gradient ground",
                "what": "The hero sits on a blue-to-lilac diagonal gradient (#E3EEFF to #F1E4FF) instead of the flat warm paper, against the tile's own 'no texture: the paper is a flat warm tone'.",
                "css": ".hero{background:linear-gradient(135deg,#E3EEFF 0%,#F1E4FF 100%);box-shadow:0 0 0 100vmax #EDE9FF;clip-path:inset(0 -100vmax)}",
            },
            {
                "id": "v3p-R",
                "kind": "treatment",
                "sub": "like parts treated unlike",
                "what": "The article's document row 'Download' control is a rounded pill with a blue outline, while the page's other action ('Write to me') is a square filled block: two unlike control shapes for one kind of part.",
                "css": ".article .doc .dl{border:1.5px solid #0070C0;border-radius:999px;padding:6px 14px}",
            },
        ],
    },
    "r2-v5p": {
        "src": "src/r2/v5-house-blue-field/index.html",
        "out": "fixtures/r2-v5p/index.html",
        "faults": [
            {
                "id": "v5p-F",
                "kind": "function",
                "sub": "dead action",
                "what": "The hero's white email button ('Mark.Moseley@MMMinfra.com →') now points to '#': it looks the same but goes nowhere, so the one action on the first screen is dead.",
                "edits": [
                    (
                        '<a class="btn" href="mailto:Mark.Moseley@MMMinfra.com">',
                        '<a class="btn" href="#">',
                    )
                ],
            },
            {
                "id": "v5p-G",
                "kind": "global",
                "sub": "busy section",
                "what": "The blue hero is made busy: a row of five outlined tag pills under the lead, a repeating diagonal line pattern over the whole field and a huge ghosted 'PPP' watermark behind the heading.",
                "edits": [
                    (
                        """      <div class="action">
        <span class="ask">Write to me at</span>""",
                        """      <ul class="tags"><li>PPP Law</li><li>Infrastructure</li><li>Development banks</li><li>Governments</li><li>Risk allocation</li></ul>
      <div class="action">
        <span class="ask">Write to me at</span>""",
                    )
                ],
                "css": ".tags{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 0;padding:0}.tags li{border:1.5px solid rgba(255,255,255,.85);border-radius:999px;padding:5px 14px;font:600 14px/1.2 var(--sans)}.field{background-image:repeating-linear-gradient(45deg,rgba(255,255,255,.10) 0 2px,transparent 2px 22px);position:relative}.field{overflow:hidden}.hero-copy{position:relative}.hero-copy::before{content:'PPP';position:absolute;left:-20px;top:-60px;font:700 300px/1 var(--serif);color:rgba(255,255,255,.10);z-index:0;pointer-events:none}.hero-copy>*{position:relative;z-index:1}",
            },
            {
                "id": "v5p-T",
                "kind": "type",
                "sub": "type hierarchy inverted",
                "what": "In the article specimen the subhead ('So, what are the key chapter topics?') is set at 40 px bold, larger and heavier than the article's own title above it: the type hierarchy is upside down.",
                "css": "article.post h4{font-size:40px!important;line-height:1.15!important;font-weight:700!important}",
            },
            {
                "id": "v5p-C",
                "kind": "colour-surface",
                "sub": "second accent colour",
                "what": "Links in the article specimen (the lecture link) are set in orange (#E4572E) instead of the house blue: a fifth colour on a 'four colours, no accent' palette, and links no longer share one colour.",
                "css": "article.post a{color:#E4572E!important;text-decoration-color:#E4572E!important}article.post li::marker{color:#E4572E}",
            },
            {
                "id": "v5p-R",
                "kind": "treatment",
                "sub": "spacing rhythm broken",
                "what": "Inside the article specimen the spacing collapses: the photo butts against the paragraph above, the caption touches the subhead below, and the list items are crammed at tight leading, unlike the rhythm of the rest of the page.",
                "css": "article.post figure{margin:0!important}article.post figcaption{margin:0!important}article.post h4{margin-top:0!important}article.post li{margin:0!important;line-height:1.05!important}article.post ul{margin:2px 0!important}",
            },
        ],
    },
    "r2-v7p": {
        "src": "src/r2/v7-mark-at-work/index.html",
        "out": "fixtures/r2-v7p/index.html",
        "faults": [
            {
                "id": "v7p-F",
                "kind": "function",
                "sub": "missing action",
                "what": "The main navigation (Profile, Articles and talks, Blog) is removed: the first screen offers no way to reach the rest of the site.",
                "edits": [
                    (
                        """    <ul class="links">
      <li><a href="#article">Profile</a></li>
      <li><a href="#article">Articles and talks</a></li>
      <li><a href="#article">Blog</a></li>
    </ul>
""",
                        "",
                    )
                ],
            },
            {
                "id": "v7p-G",
                "kind": "global",
                "sub": "hierarchy broken across sections",
                "what": "A loud full-width house-blue band ('Get Mark's briefings on PPP reform' at 56 px with a white 'Subscribe' button) is inserted straight under the hero, competing with the hero and its one action.",
                "edits": [
                    (
                        """<main class="spec">""",
                        """<section style="background:#0070C0;color:#fff;padding:72px 32px;text-align:center"><p style="font:400 56px/1.1 var(--serif);margin:0 auto 28px;max-width:16em">Get Mark's briefings on PPP reform</p><a href="#subscribe" style="display:inline-block;background:#fff;color:#0070C0;font:600 18px/1 var(--sans);padding:18px 32px;text-decoration:none">Subscribe</a></section>
<main class="spec">""",
                    )
                ],
            },
            {
                "id": "v7p-T",
                "kind": "type",
                "sub": "centred running text",
                "what": "The article specimen's long paragraphs and list are centred, so every line starts at a different place and the long text is hard to read.",
                "css": ".article p:not(.byline),.article ol,.article h4{text-align:center}",
            },
            {
                "id": "v7p-C",
                "kind": "colour-surface",
                "sub": "stacked edges and heavy elevation",
                "what": "The PDF download row is boxed with a pale blue fill, a blue border, a heavy drop shadow and rounded corners: four edge treatments stacked on one static row of a flat page.",
                "css": ".downloads li{background:#EAF3FF;border:1px solid #0070C0;border-radius:12px;box-shadow:0 14px 32px rgba(0,0,0,.28);padding:8px 16px}",
            },
            {
                "id": "v7p-R",
                "kind": "treatment",
                "sub": "like parts treated unlike",
                "what": "The specimen section labels are styled three ways: 'Palette' as tracked blue capitals, 'Texture' as a large italic serif, the rest as the original small grey labels.",
                "css": "#h-palette{text-transform:uppercase;letter-spacing:.18em;color:#0070C0!important;font-weight:700!important}#h-texture{font:italic 400 34px/1.2 var(--serif)!important}",
            },
        ],
    },
    "manta-home-p": {
        "src": "src/manta/home.self.html",
        "out": "fixtures/manta-home-p/index.html",
        "faults": [
            {
                "id": "mhp-F",
                "kind": "function",
                "sub": "dead action",
                "what": "The three destination cards (Canggu, Uluwatu, Kuta Lombok) still look like link cards with a 'Best hostels >' chevron, but are no longer links: nothing happens on click.",
                "edits": [
                    (
                        '<a class="dest-card" aria-label="Best hostels in Canggu, Bali" href="/best-hostels-in/canggu">',
                        '<div class="dest-card">',
                    ),
                    (
                        '<a class="dest-card" aria-label="Best hostels in Uluwatu, Bali" href="/best-hostels-in/uluwatu">',
                        '<div class="dest-card">',
                    ),
                    (
                        '<a class="dest-card" aria-label="Best hostels in Kuta Lombok, Lombok" href="/best-hostels-in/kuta-lombok">',
                        '<div class="dest-card">',
                    ),
                    (
                        '</svg></span></a></li><li><div class="dest-card">',
                        '</svg></span></div></li><li><div class="dest-card">',
                        2,
                    ),
                    ("</svg></span></a></li></ul>", "</svg></span></div></li></ul>"),
                ],
            },
            {
                "id": "mhp-G",
                "kind": "global",
                "sub": "hierarchy broken across sections",
                "what": "The 'Where we're starting' heading is set at about 120 px bold, bigger than the hero's MantaHostels wordmark, so the second section outranks the first screen.",
                "css": "#destinations .section__title{font-size:120px!important;line-height:1!important;font-weight:700!important;letter-spacing:-0.02em}@media (max-width:700px){#destinations .section__title{font-size:58px!important}}",
            },
            {
                "id": "mhp-T",
                "kind": "type",
                "sub": "third typeface",
                "what": "The destination cards' region labels and place names are set in a monospace typewriter face, a third face foreign to the site's Quicksand/Nunito Sans pair.",
                "css": ".dest-card__region,.dest-card__name{font-family:'Courier New',Courier,monospace!important}.dest-card__name{font-size:22px!important}",
            },
            {
                "id": "mhp-C",
                "kind": "colour-surface",
                "sub": "off-palette edge and heavy elevation",
                "what": "The destination cards get a 3 px purple border and a heavy drop shadow at rest: an edge colour outside the palette and elevation the rest of the page does not use.",
                "css": ".dest-card{border:3px solid #7B2CBF!important;box-shadow:0 16px 32px rgba(0,0,0,.30)!important}",
            },
            {
                "id": "mhp-R",
                "kind": "treatment",
                "sub": "like parts treated unlike",
                "what": "The secondary 'Explore destinations' button has square corners while the primary button beside it is a pill: the two buttons no longer share one shape.",
                "css": ".btn--secondary{border-radius:0!important}",
            },
        ],
    },
    "manta-canggu-p": {
        "src": "src/manta/canggu.self.html",
        "out": "fixtures/manta-canggu-p/index.html",
        "faults": [
            {
                "id": "mcp-F",
                "kind": "function",
                "sub": "missing action",
                "what": "The 'coming soon' notice no longer carries the email link, so the panel announces the launch but gives the visitor no way to be told or to get in touch from it.",
                "edits": [
                    (
                        '<p><a href="mailto:luc@mantahostels.com">luc@mantahostels.com</a></p></div>',
                        "</div>",
                    )
                ],
            },
            {
                "id": "mcp-G",
                "kind": "global",
                "sub": "busy section",
                "what": "The 'Good for' section is made busy: twelve chips in six bright fill colours, each with its own border colour, crowd the section.",
                "edits": [
                    (
                        '<ul class="chips"><li>First-time surfers</li><li>Remote workers</li><li>Long stays</li><li>Meeting people</li></ul>',
                        '<ul class="chips"><li>First-time surfers</li><li>Remote workers</li><li>Long stays</li><li>Meeting people</li><li>Yoga</li><li>Nightlife</li><li>Budget</li><li>Cafés</li><li>Couples</li><li>Solo travellers</li><li>Scooter riders</li><li>Sunsets</li></ul>',
                    )
                ],
                "css": ".chips li:nth-child(6n+1){background:#FFD166;border-color:#EF476F!important}.chips li:nth-child(6n+2){background:#06D6A0;border-color:#118AB2!important}.chips li:nth-child(6n+3){background:#EF476F;color:#fff;border-color:#FFD166!important}.chips li:nth-child(6n+4){background:#118AB2;color:#fff;border-color:#06D6A0!important}.chips li:nth-child(6n+5){background:#C77DFF;border-color:#3A0CA3!important}.chips li:nth-child(6n){background:#F15BB5;color:#fff;border-color:#00BBF9!important}.chips li{border-width:2px!important;border-style:solid!important}",
            },
            {
                "id": "mcp-T",
                "kind": "type",
                "sub": "justified text",
                "what": "Every body paragraph is justified in a narrow column, opening uneven word gaps (rivers), worst at phone width.",
                "css": "main.page p{text-align:justify;hyphens:none}",
            },
            {
                "id": "mcp-C",
                "kind": "colour-surface",
                "sub": "semantic colour misused",
                "what": "The 'coming soon' notice panel is set on an alarm red (#C1121F) instead of the ink ground, so a friendly launch note reads as an error or warning.",
                "css": ".notice{background:#C1121F!important}",
            },
            {
                "id": "mcp-R",
                "kind": "treatment",
                "sub": "like parts treated unlike",
                "what": "The section headings are styled three ways: 'Vibe' turquoise, italic and underlined; 'What to look for' small tracked capitals; 'Surf' and 'Good for' as before.",
                "css": ".guide-section:nth-of-type(2) h2{color:#1FB5A8!important;font-style:italic;text-decoration:underline}.guide-section:nth-of-type(4) h2{text-transform:uppercase;letter-spacing:.16em;font-size:15px!important}",
            },
        ],
    },
}


def apply(name, spec):
    html = pathlib.Path(spec["src"]).read_text()
    css, fonts = [], False
    for f in spec["faults"]:
        for e in f.get("edits", []):
            old, new = e[0], e[1]
            want = e[2] if len(e) > 2 else 1
            n = html.count(old)
            if n != want:
                sys.exit(
                    f"{f['id']}: edit matched {n} times, wanted {want}: {old[:60]!r}"
                )
            html = html.replace(old, new)
        if f.get("css"):
            css.append(f"/* {f['id']} */ " + f["css"])
        fonts = fonts or f.get("fonts", False)
    tag = (FONT if fonts else "") + "<style>" + "\n".join(css) + "</style>"
    assert html.count("</head>") == 1
    html = html.replace("</head>", tag + "</head>")
    out = pathlib.Path(spec["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


if __name__ == "__main__":
    key = []
    for name, spec in PAGES.items():
        apply(name, spec)
        for f in spec["faults"]:
            key.append(
                {
                    "candidate": name,
                    "id": f["id"],
                    "kind": f["kind"],
                    "sub": f["sub"],
                    "what": f["what"],
                }
            )
    pathlib.Path("fixtures/key.json").write_text(json.dumps(key, indent=1))
    print(len(key), "faults on", len(PAGES), "pages")
