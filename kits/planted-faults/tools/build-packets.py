#!/usr/bin/env python3
import json
import random
import pathlib
import glob
from PIL import Image

R1 = "".join(open("src/r1/README.md").readlines()[:102])
R2 = open("src/r2/README.md").read()
BS1, BS2 = open("src/brand-sheet-r1.md").read(), open("src/brand-sheet.md").read()
PRODUCT = open("/home/lucmo/mantahostels/PRODUCT.md").read()
DESIGN = open("/home/lucmo/mantahostels/DESIGN.md").read()
MMM_STAND = "Stand-ins: every photograph captioned 'Placeholder' is a stand-in until the image round; a finding against a stand-in photograph itself (its choice, crop or quality) is out of scope. The style-tile parts below the first screen (palette, type pair, texture, article specimen, motion sketch) are part of the candidate and are judged."
MANTA_STAND = "Stand-ins: none."
C = {
    "r1-v1": ("mmm1", "round 1, direction v1 Legal pad"),
    "r1-v2": ("mmm1", "round 1, direction v2 General arrangement"),
    "r1-v3": ("mmm1", "round 1, direction v3 Inscription"),
    "r1-v5": ("mmm1", "round 1, direction v5 House colours"),
    "r2-v1": ("mmm2", "round 2, direction v1 Counsel's paper"),
    "r2-v7": ("mmm2", "round 2, direction v7 Mark at work"),
    "r2-v1p": ("mmm2", "round 2, direction v1 Counsel's paper"),
    "r2-v3p": ("mmm2", "round 2, direction v3 The annotated brief"),
    "r2-v5p": ("mmm2", "round 2, direction v5 House colours, one blue field"),
    "r2-v7p": ("mmm2", "round 2, direction v7 Mark at work"),
    "manta-home-p": (
        "manta",
        "the homepage, before launch: says what MantaHostels is, collects launch-news contacts by email, and sends visitors to the destination guides",
    ),
    "manta-canggu-p": (
        "manta",
        "a destination guide, Canggu: helps a backpacker judge whether Canggu suits them and what to look for in a hostel there; hostel listings are not live yet",
    ),
    "manta-rank": (
        "manta",
        "How we rank: explains how MantaHostels ranks hostels, so a visitor can trust the ranking",
    ),
}
PERSONA = {
    "mmm1": "a senior official at a multilateral development bank, looking for an independent legal advisor on a Public-Private Partnership law",
    "mmm2": "a senior official at a multilateral development bank, looking for an independent legal advisor on a Public-Private Partnership law",
    "manta": "a backpacker in their twenties planning a first trip to Bali and Lombok, deciding where to stay",
}


def brief(proj, which):
    if proj == "mmm1":
        return f"# Dispatch\n\nThis candidate: {which}, mmm-infra #8 (the look of Mark Moseley's site). Judge this one candidate.\n\n{MMM_STAND}\n\n# The round's brief\n\n{R1}\n\n# The project's rules file: brand sheet\n\n{BS1}"
    if proj == "mmm2":
        return f"# Dispatch\n\nThis candidate: {which}, mmm-infra #8 (the look of Mark Moseley's site). Judge this one candidate.\n\n{MMM_STAND}\n\n# The round's brief\n\n{R2}\n\n# The project's rules file: brand sheet\n\n{BS2}"
    return f"# Dispatch\n\nThis candidate: MantaHostels, {which}. Judge this one page as it stands, as a candidate for the live site.\n\n{MANTA_STAND}\n\n# The project: PRODUCT.md\n\n{PRODUCT}\n\n# The project's rules file: DESIGN.md\n\n{DESIGN}"


names = list(C)
random.Random(224).shuffle(names)
ids = {n: f"c{i + 1:02d}" for i, n in enumerate(names)}
for n, (proj, which) in C.items():
    d = pathlib.Path("packets") / n
    (d / "brief.md").write_text(brief(proj, which))
    ims = [Image.open(f) for f in sorted(glob.glob(str(d / "shots/desktop-*.png")))]
    H = sum(i.height for i in ims)
    full = Image.new("RGB", (1440, H), "white")
    y = 0
    for i in ims:
        full.paste(i, (0, y))
        y += i.height
    full.thumbnail((1568, 1568))
    full.save(d / "overview.png")
json.dump(
    {"ids": ids, "project": {n: C[n][0] for n in C}, "persona": PERSONA},
    open("packets/meta.json", "w"),
    indent=1,
)
print(ids)
