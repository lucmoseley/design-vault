#!/usr/bin/env python3
"""python3 kits/planted-faults/tools/store-refs.py <skills dir> <reader> <out dir> [--asset <class>] [--fact <fact>]... — one critic's rule files from the rule store.

Writes what a critic reader is handed in a round, as the kit's confined critics read it: `records.md`, the output of
`gate.js list --reader <reader>` on <skills dir>'s store, and `sections.md`, every reference section it names, each
cut from its file at its heading and running to the next heading of the same or a higher level. The asset defaults to
the kit's pages: a web surface with a call to action. Copy whole files the prompt names (house-principles.md,
lenses.md) beside them by hand.
"""

import argparse
import pathlib
import re
import subprocess


def slug(heading):
    s = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return s.replace(" ", "-")


def section(path, anchor):
    lines = path.read_text().splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"(#+) (.*)", line)
        if m and slug(m.group(2)) == anchor:
            level = len(m.group(1))
            end = next(
                (
                    j
                    for j in range(i + 1, len(lines))
                    if re.match(rf"#{{1,{level}}} ", lines[j])
                ),
                len(lines),
            )
            return "\n".join(lines[i:end]).strip()
    raise SystemExit(f"{path}: no heading for #{anchor}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skills")
    parser.add_argument("reader")
    parser.add_argument("out")
    parser.add_argument("--asset", default="web-surface")
    parser.add_argument("--fact", action="append", default=None)
    args = parser.parse_args()
    skills = pathlib.Path(args.skills)
    facts = [f for fact in (args.fact or ["has-cta"]) for f in ("--fact", fact)]
    listed = subprocess.run(
        [
            "node",
            skills / "design-round/scripts/gate.js",
            "list",
            "--asset",
            args.asset,
            *facts,
            "--reader",
            args.reader,
            skills / "design-critique/rules",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "records.md").write_text(listed)
    cited = re.findall(
        r"^- (\S+?)#(\S+?): ", listed.split("Reference sections they cite", 1)[1], re.M
    )
    parts = [
        f"<!-- {file}#{anchor} -->\n\n{section(skills / file, anchor)}"
        for file, anchor in cited
    ]
    (out / "sections.md").write_text(
        "# The reference sections the records cite\n\n" + "\n\n".join(parts) + "\n"
    )
    print(f"{out}: {listed.splitlines()[0]} {len(cited)} section(s).")


if __name__ == "__main__":
    main()
