#!/usr/bin/env python3
"""The gate trio's planted faults, each one a fault only a held gate record asks about.

  python3 kits/planted-faults/tools/gate-plants.py

Copies three clean pages of the kit (r1-v5, r2-v7, manta-rank) to r1-v5g, r2-v7g and manta-rank-g with 14 faults
planted, spread over the held look records' stages and areas, and none that a live record of any reader asks. It
writes each copy's fixture, its packet (the clean page's brief.md, and parts.txt read afresh by parts-map.py), its
neutral id and source page in packets/meta.json, and its faults into fixtures/key.json as the `gate` set, replacing
any gate set already there. It exits where a plant's record is not held in the store under the stage and area given. The
critic set's faults are left as they are. Unlike plants.py, it leaves no comment in the page naming a plant.

Each fault: id, record (the held record it breaks), stage and area (the record's, from the rule store), what (the
fault in plain words, for the scorer), edits (old -> new, each old must occur exactly once), css (appended in one
<style> before </head>), font (an extra stylesheet <link>).
"""

import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
VAULT = ROOT.parents[1]
STORE = VAULT / "plugin/skills/design-critique/rules"
# guess, #501
RENDER_TIMEOUT = 300
CONDENSED = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400&display=swap">'
ICON = '<svg class="deco" viewBox="0 0 24 24" aria-hidden="true"><path d="{d}" fill="currentColor"/></svg>'
STAR = "M12 2l2.9 6.9 7.1.6-5.4 4.7 1.6 7-6.2-3.8-6.2 3.8 1.6-7L2 9.5l7.1-.6z"
BOLT = "M13 2L4 14h7l-1 8 9-12h-7z"
DROP = "M12 2C8 8 5 11.5 5 15a7 7 0 0014 0c0-3.5-3-7-7-13z"
LEAF = (
    "M20 4C10 4 4 9 4 17c0 1 .2 2 .5 3C6 13 10 10 16 9c-5 2-8 6-9 11h2c1-6 5-9 11-10V4z"
)
SPARK = "M12 1l2.5 8.5L23 12l-8.5 2.5L12 23l-2.5-8.5L1 12l8.5-2.5z"

PAGES = {
    "r1-v5g": {
        "src": "r1-v5",
        "faults": [
            {
                "id": "v5g-carousel",
                "record": "vault.carousel-use",
                "stage": "function",
                "area": "navigation",
                "what": "The hero, one message, is dressed as a carousel: previous and next arrows and four dots ('1 / 4') sit under the 'Get in touch' button, as if the opening rotated through slides.",
                "edits": [
                    (
                        'stroke-width="1.6"/></svg></a>',
                        'stroke-width="1.6"/></svg></a><div class="slides"><button type="button" aria-label="Previous slide">&#8249;</button>'
                        '<span class="dots"><i class="on"></i><i></i><i></i><i></i></span><span class="count">1 / 4</span>'
                        '<button type="button" aria-label="Next slide">&#8250;</button></div>',
                    )
                ],
                "css": ".slides{display:flex;align-items:center;gap:14px;margin-top:40px;font:500 15px 'Source Sans 3',sans-serif;color:#404040}"
                ".slides button{width:40px;height:40px;border:1px solid #404040;border-radius:50%;background:#fff;font-size:22px;line-height:1;cursor:pointer;color:#404040}"
                ".slides .dots{display:flex;gap:8px}.slides .dots i{width:9px;height:9px;border-radius:50%;background:#dedede}.slides .dots i.on{background:#0070c0}",
            },
            {
                "id": "v5g-current",
                "record": "vault.sibling-emphasis",
                "stage": "role",
                "area": "text",
                "what": "In the header navigation the current page's link, Profile, is set apart from Articles, Blog and Contact only by the logo blue the page keeps for its links and its one button, with no change of weight, fill, size or place.",
                "edits": [
                    (
                        '<nav aria-label="Main"><a href="#">Profile</a>',
                        '<nav aria-label="Main"><a href="#" aria-current="page">Profile</a>',
                    )
                ],
                "css": ".top nav a[aria-current]{color:var(--blue)}",
            },
            {
                "id": "v5g-case",
                "record": "vault.text-case",
                "stage": "treatment",
                "area": "text",
                "what": "The section headings and two button labels are in title case: 'Type Pair', 'An Article Page', 'Motion Sketch', 'Get In Touch' and 'Play Again'.",
                "edits": [
                    (
                        '<h2 id="h-type">Type pair</h2>',
                        '<h2 id="h-type">Type Pair</h2>',
                    ),
                    (
                        '<h2 id="h-art">An article page</h2>',
                        '<h2 id="h-art">An Article Page</h2>',
                    ),
                    (
                        '<h2 id="h-mot">Motion sketch</h2>',
                        '<h2 id="h-mot">Motion Sketch</h2>',
                    ),
                    ('">Get in touch <svg', '">Get In Touch <svg'),
                    (
                        'id="replay">Play again</button>',
                        'id="replay">Play Again</button>',
                    ),
                ],
            },
            {
                "id": "v5g-icon",
                "record": "vault.button-icon",
                "stage": "treatment",
                "area": "buttons",
                "what": "The motion sketch's replay button carries a four-pointed sparkle icon before its label, a symbol with no settled meaning for 'play again', where a replay arrow or no icon would do.",
                "edits": [
                    (
                        'id="replay">Play Again</button>',
                        'id="replay">' + ICON.format(d=SPARK) + "Play Again</button>",
                    )
                ],
                "css": "#replay .deco{width:15px;height:15px;vertical-align:-2px;margin-right:7px;color:#0070c0}",
            },
            {
                "id": "v5g-split",
                "record": "vault.pane-split",
                "stage": "role",
                "area": "layout",
                "what": "At desktop width the opening's two panes are split the wrong way: the portrait stand-in, the supporting pane, takes more than half the width, and the name, lead and 'Get in touch' button, the main pane, are squeezed into the rest.",
                "css": "@media (min-width:761px){.hero{grid-template-columns:minmax(0,1fr) 55%!important}h1 .ln>span{white-space:normal}}",
            },
        ],
    },
    "r2-v7g": {
        "src": "r2-v7",
        "faults": [
            {
                "id": "v7g-icons",
                "record": "vault.icon-use",
                "stage": "function",
                "area": "imagery",
                "what": "Each section heading (Palette, Type pair, Texture, An article page, Motion sketch) opens with a large blue decorative icon (a star, a lightning bolt, a drop, a leaf, a sparkle) that marks no action or information.",
                "edits": [
                    (f'<h2 id="h-{h}">', f'<h2 id="h-{h}">' + ICON.format(d=d))
                    for h, d in (
                        ("palette", STAR),
                        ("type", BOLT),
                        ("texture", DROP),
                        ("article", LEAF),
                        ("motion", SPARK),
                    )
                ],
                "css": "h2 .deco{width:30px;height:30px;vertical-align:-9px;margin-right:12px;color:#0070C0}",
            },
            {
                "id": "v7g-stack",
                "record": "vault.stack-order",
                "stage": "function",
                "area": "layout",
                "what": "At phone width the article specimen's side note ('Text on a 32 px line…', 'Grey for reading…') stacks above the article itself, so the supporting pane comes before the main content.",
                "css": "@media (max-width:900px){.article-wrap .aside{order:-1}}",
            },
            {
                "id": "v7g-zebra",
                "record": "vault.zebra-rows",
                "stage": "treatment",
                "area": "data",
                "what": "The short motion timeline table, four narrow columns, has heavy alternating row fills, saturated mid-blue and pale grey, on a table too small for the eye to lose its row.",
                "css": ".timeline tbody tr:nth-child(odd) td{background:#7FA7D1!important;color:#10202f}.timeline tbody tr:nth-child(even) td{background:#E6E6E6!important}",
            },
            {
                "id": "v7g-condensed",
                "record": "vault.type-width",
                "stage": "treatment",
                "area": "typography",
                "what": "The article's running text (its paragraphs and numbered list) is set in a condensed sans, Roboto Condensed, a narrow width in long reading text.",
                "font": CONDENSED,
                "css": ".article > p:not(.byline),.article ol li{font-family:'Roboto Condensed',sans-serif!important;font-weight:400}",
            },
            {
                "id": "v7g-align",
                "record": "vault.alignment-break",
                "stage": "treatment",
                "area": "layout",
                "what": "The Texture section alone is pushed about 120 px in from the left edge every other section shares, for no reason the page shows.",
                "css": ".part[aria-labelledby=h-texture]{padding-left:120px}@media (max-width:700px){.part[aria-labelledby=h-texture]{padding-left:40px}}",
            },
        ],
    },
    "manta-rank-g": {
        "src": "manta-rank",
        "faults": [
            {
                "id": "mrg-oneoff",
                "record": "vault.text-style-count",
                "stage": "value",
                "area": "typography",
                "what": "The sentence under the lede ('Scores weight toward recent stays…') is set in a style found nowhere else on the page: an italic serif, larger than the body text, in purple.",
                "edits": [
                    (
                        "</p><p>Scores weight toward",
                        '</p><p class="aside-note">Scores weight toward',
                    )
                ],
                "css": ".prose p.aside-note{font:italic 400 1.2rem/1.5 Georgia,'Times New Roman',serif;color:#7a3fa0}",
            },
            {
                "id": "mrg-tabbar",
                "record": "vault.component-swap",
                "stage": "role",
                "area": "layout",
                "what": "At phone width the header's Menu button, which opens Destinations and How we rank, is gone, and a bar fixed to the bottom of the screen takes its place with other links in it: Search, Saved and Account.",
                "edits": [
                    (
                        "<next-route-announcer",
                        '<nav class="tabbar" aria-label="Main"><a href="/search">Search</a><a href="/saved">Saved</a><a href="/account">Account</a></nav><next-route-announcer',
                    )
                ],
                "css": ".tabbar{display:none}@media (max-width:767px){.site-nav__toggle{display:none!important}"
                ".tabbar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:20;justify-content:space-around;background:#0a3542;border-top:1px solid #23bfb2;padding:6px 0 10px}"
                ".tabbar a{color:#fff;font-weight:600;min-height:44px;display:inline-flex;align-items:center;text-decoration:none}}",
            },
            {
                "id": "mrg-deadline",
                "record": "vault.offer-deadline",
                "stage": "treatment",
                "area": "content",
                "what": "A red strip under the navigation sells the partner tier with a ticking countdown, 'Partner launch price ends in 02:14:37', and a 'Only 3 spots left' badge.",
                "edits": [
                    (
                        '</nav><button type="button" class="site-nav__backdrop"',
                        '</nav><div class="urgent"><span>Partner launch price: 40% off ends in <b class="clock">02:14:37</b></span>'
                        '<em>Only 3 spots left!</em></div><button type="button" class="site-nav__backdrop"',
                    )
                ],
                "css": ".urgent{display:flex;justify-content:center;align-items:center;gap:16px;flex-wrap:wrap;background:#D7191C;color:#fff;font-weight:700;padding:10px 16px;font-size:16px}"
                ".urgent .clock{font-variant-numeric:tabular-nums;font-size:20px;background:#fff;color:#D7191C;padding:2px 8px;border-radius:4px}"
                ".urgent em{font-style:normal;background:#FFD400;color:#111;padding:3px 10px;border-radius:999px;text-transform:uppercase;font-size:13px}",
            },
            {
                "id": "mrg-card",
                "record": "vault.card-type",
                "stage": "treatment",
                "area": "surfaces",
                "what": "A row of three destination cards (Canggu, Uluwatu, Ubud) under the ranking principles, each a link of the same kind, and the middle one alone (Uluwatu) is shaped differently: square corners where the others are rounded, and its text centred where theirs is set left.",
                "edits": [
                    (
                        "average.</li></ol><section><h2>Ranking method",
                        'average.</li></ol><ul class="dest-grid dest-row"><li><a class="dest-card" href="/destinations/canggu"><span class="dest-card__region">Bali</span><span class="dest-card__name">Canggu</span><span class="dest-card__cta">See the ranking</span></a></li>'
                        '<li><a class="dest-card" href="/destinations/uluwatu"><span class="dest-card__region">Bali</span><span class="dest-card__name">Uluwatu</span><span class="dest-card__cta">See the ranking</span></a></li>'
                        '<li><a class="dest-card" href="/destinations/ubud"><span class="dest-card__region">Bali</span><span class="dest-card__name">Ubud</span><span class="dest-card__cta">See the ranking</span></a></li></ul>'
                        "<section><h2>Ranking method",
                    )
                ],
                "css": ".prose ul.dest-row{padding:0;margin-top:24px}.prose ul.dest-row li{margin:0}.prose ul.dest-row a{text-decoration:none;font-weight:inherit}"
                ".prose ul.dest-row li:nth-child(2) .dest-card{border-radius:0;align-items:center;text-align:center;justify-content:center}",
            },
        ],
    },
}


def apply(name, spec):
    html = (ROOT / "fixtures" / spec["src"] / "index.html").read_text()
    css, links = [], []
    for f in spec["faults"]:
        for old, new in f.get("edits", []):
            if html.count(old) != 1:
                sys.exit(
                    f"{f['id']}: edit matched {html.count(old)} times, wanted 1: {old[:60]!r}"
                )
            html = html.replace(old, new)
        if f.get("css"):
            css.append(f["css"])
        if f.get("font"):
            links.append(f["font"])
    assert html.count("</head>") == 1
    html = html.replace(
        "</head>", "".join(links) + "<style>" + "\n".join(css) + "</style></head>"
    )
    out = ROOT / "fixtures" / name / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return out


def packet(name, spec, page):
    folder = ROOT / "packets" / name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "brief.md").write_text(
        (ROOT / "packets" / spec["src"] / "brief.md").read_text()
    )
    with tempfile.TemporaryDirectory() as pm:
        script = VAULT / "plugin/skills/design-round/scripts/parts-map.py"
        subprocess.run(
            [sys.executable, str(script), str(page), "--out", pm],
            check=True,
            capture_output=True,
            timeout=RENDER_TIMEOUT,
        )
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools/parts-txt.py"),
                f"{pm}/parts.json",
                str(folder / "parts.txt"),
            ],
            check=True,
        )


def asked(load):
    lists = ROOT / "prompts/gate-415" / load
    return set(
        re.findall(
            r"^\d+\. (vault\.[\w-]+)",
            "".join(p.read_text() for p in lists.glob("look-*.txt")),
            re.M,
        )
    )


def check_store(spec):
    for f in spec["faults"]:
        area = f["area"]
        text = (
            (STORE / f"{area}.md").read_text()
            if (STORE / f"{area}.md").exists()
            else ""
        )
        m = re.search(
            rf"^### {re.escape(f['record'])}\n(.*?)(?=^### |\Z)", text, re.S | re.M
        )
        fields = dict(re.findall(r"^- ([\w-]+): (.*)$", m.group(1), re.M)) if m else {}
        if fields.get("status") != "staged" or fields.get("stage") != f["stage"]:
            sys.exit(
                f"{f['id']}: {f['record']} is not a held {f['stage']} record in {area}.md"
            )
        if f["record"] not in asked("G-new") or f["record"] in asked("G-old"):
            sys.exit(
                f"{f['id']}: {f['record']} is not a question the held look list alone asks; re-cut the lists with runner.py gate-lists"
            )


def main():
    meta_file = ROOT / "packets/meta.json"
    meta = json.load(open(meta_file))
    key_file = ROOT / "fixtures/key.json"
    key = [k for k in json.load(open(key_file)) if k.get("set") != "gate"]
    for name, spec in PAGES.items():
        check_store(spec)
        page = apply(name, spec)
        packet(name, spec, page)
        if name not in meta["ids"]:
            meta["ids"][name] = f"c{len(meta['ids']) + 1:02d}"
        meta["project"][name] = meta["project"][spec["src"]]
        for f in spec["faults"]:
            key.append(
                {
                    "candidate": name,
                    "set": "gate",
                    **{k: f[k] for k in ("id", "record", "stage", "area", "what")},
                }
            )
    meta["gate_pages"] = sorted(PAGES)
    meta["sources"] = {name: spec["src"] for name, spec in sorted(PAGES.items())}
    json.dump(meta, open(meta_file, "w"), indent=1, ensure_ascii=False)
    key_file.write_text(json.dumps(key, indent=1))
    print(
        sum(len(s["faults"]) for s in PAGES.values()),
        "gate faults on",
        len(PAGES),
        "pages",
    )


if __name__ == "__main__":
    main()
