#!/usr/bin/env python3
"""python3 parts-txt.py <parts.json> <out.txt> — the parts map as the critic reads it, with file paths reduced to what a link points at."""

import json
import sys

d = json.load(open(sys.argv[1]))


def target(h):
    if not h:
        return None
    if h.startswith("file://"):
        frag = h.split("#", 1)[1] if "#" in h else ""
        return "#" + frag if "#" in h else "this page"
    return h


lines = [
    "The parts map: what each part of the page does, read from its DOM by a script at 1440 px and 390 px.",
    "'acts' means a visitor can act on it (link, button, control); 'static' means a click does nothing.",
    "Static parts are listed only where they could look actable (pointer cursor, own box, underline, hover rule or link colour).",
    "",
]
for p in d["parts"]:
    t = p["text"] if len(p["text"]) <= 70 else p["text"][:69] + "…"
    s = f'{p["id"]}  "{t}"  ' + (
        "acts: "
        + (p.get("role") or "?")
        + (f" -> {target(p.get('href'))}" if p.get("href") else "")
        if p["actable"]
        else "static"
    )
    why = []
    if not p["actable"]:
        if p.get("cursor") == "pointer":
            why.append("pointer cursor")
        if p.get("hover"):
            why.append("hover rule")
        for r in p.get("listed") or []:
            why.append(str(r))
    if why:
        s += "  (could look actable: " + ", ".join(dict.fromkeys(why)) + ")"
    lines.append(s)
ot = d.get("answers", {}).get("vault.one-target", {})
if ot.get("faults"):
    lines += ["", "Nested targets: " + "; ".join(map(str, ot["faults"]))]
open(sys.argv[2], "w").write("\n".join(lines) + "\n")
