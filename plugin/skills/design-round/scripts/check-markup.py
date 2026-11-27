#!/usr/bin/env python3
"""python3 check-markup.py <page> --out DIR [--table FILE] [--parts FILE] [--part NAME=SELECTOR]

Runs the vendored axe-core in a rendered page and answers each rule record its
table maps to axe rule ids. The page is loaded afresh at phone and desktop
width, and axe runs on it at each.

THE TABLE, by default check-markup.table beside this script, gives each line
as fields split by " | ". Blank lines and lines starting with # are skipped.

  <record id> | <axe rule id>, … [| part:<name>]
                      with part:<name>, axe reads only that
                      declared part's elements and the link or button that
                      holds each, the control whose name the part gives
  off | <axe rule id>, …
                      rules the vault answers by its own scripts: no record
                      line may name one

A rule id axe does not know is refused before any record is answered. Rules axe
tags experimental run where a line names them.

--parts is the building session's parts declaration (design-round §1c); --part gives one
part's selector and wins. A part: line whose part has no selector is not
judged, and goes to the look critics.

Each record id's finding is fail where a rule finds a violation at either
width, else not judged where its part has no selector, else no match where
none of its rules passed or failed anything on the page, else pass. What axe
could not decide ("incomplete", its needs-review list) is printed under its
record as review and kept in the JSON, and never changes an answer and
never goes to a critic. DIR/markup.json holds every
finding; an earlier run's is deleted.

EXITS 0 no miss / 1 a miss (each printed) / 2 the arguments or the table are
wrong / 3 Playwright or its browser is missing / 4 a page did not render in time
/ 5 the browser refused the page / 7 a call hung that would never return. Exits
0 and 1 print on stdout; the rest print on stderr.
"""

import argparse
import collections
import contextlib
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402

AXE = os.path.join(HERE, "..", "vendor", "axe-core", "axe.min.js")


runner = siblings.load(HERE, "runner.py")
layout = siblings.load(HERE, "check-layout.py")
probe = siblings.load(HERE, "probe.py")
rule_table = siblings.load(HERE, "rule-table.py")

TABLE = os.path.join(HERE, "check-markup.table")
SEP = " | "
OFF = "off"
WIDTHS = (layout.PHONE_WIDTH, layout.DESKTOP_WIDTH)
RULE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
PART = re.compile(r"part:(\S+)")

HTML_CHARS = 200  # guess, #501
NO_PART = object()

Line = collections.namedtuple("Line", "id rules part text")
Table = collections.namedtuple("Table", "lines off")


TableError = rule_table.TableError


def _rule_ids(n, given):
    ids = [r.strip() for r in given.split(",")]
    bad = [r for r in ids if not RULE_ID.fullmatch(r)]
    if bad:
        raise TableError(f"line {n}: not an axe rule id: {', '.join(map(repr, bad))}")
    return tuple(ids)


def parse(text):
    lines, off = [], ()
    for n, line in rule_table.lines(text):
        fields = [f.strip() for f in line.split(SEP)]
        if len(fields) not in (2, 3) or not all(fields):
            raise TableError(f"line {n}: want ID | RULE, … [| part:NAME], got {line!r}")
        rules = _rule_ids(n, fields[1])
        if fields[0] == OFF:
            if len(fields) == 3:
                raise TableError(f"line {n}: the off line takes no part, got {line!r}")
            off += rules
            continue
        part = None
        if len(fields) == 3:
            m = PART.fullmatch(fields[2])
            if not m:
                raise TableError(f"line {n}: want part:NAME, got {fields[2]!r}")
            part = m[1]
        lines.append(Line(fields[0], rules, part, line))
    if not lines:
        raise TableError("the table has no record lines")
    named = sorted({r for line in lines for r in line.rules} & set(off))
    if named:
        raise TableError(
            f"{', '.join(named)} is off, answered by the vault's own scripts, and no record line may name it"
        )
    return Table(tuple(lines), off)


RUN_JS = r"""
async ({ rules, selector, htmlChars }) => {
  let context = document;
  if (selector !== null) {
    const held = [...document.querySelectorAll(selector)]
      .flatMap((el) => [el, el.closest("a[href], button, [role=link], [role=button]")])
      .filter(Boolean);
    context = { include: [...new Set(held)] };
    if (!context.include.length) return null;
  }
  const r = await axe.run(context, {
    runOnly: { type: "rule", values: rules },
  });
  const nodes = (list) => list.flatMap((x) => x.nodes.map((n) => ({
    rule: x.id, target: n.target.join(" "), html: n.html.slice(0, htmlChars),
    why: x.help, summary: n.failureSummary ?? "",
  })));
  return {
    violations: nodes(r.violations),
    incomplete: nodes(r.incomplete),
    applied: [...r.violations, ...r.passes].map((x) => x.id),
  };
}
"""


def known(page):
    return set(page.evaluate("axe.getRules().map((r) => r.ruleId)"))


def run_axe(page, rules, selector):
    return page.evaluate(
        RUN_JS,
        {"rules": list(rules), "selector": selector, "htmlChars": HTML_CHARS},
    )


def axe_on(page, rules, selector):
    if not page.evaluate("() => !!window.axe"):
        with open(AXE, encoding="utf8") as fh:
            page.evaluate(fh.read())
    return run_axe(page, rules, selector)


def sweep(browser, url, *, table, parts, source, timeout):
    page = browser.new_page()
    page.set_default_timeout(timeout)
    out = {}
    for width in WIDTHS:
        layout.load(page, url, width, layout.HEIGHTS)
        page.evaluate(source)
        missing = sorted({r for line in table.lines for r in line.rules} - known(page))
        if missing:
            raise TableError(f"axe knows no rule {', '.join(missing)}")
        out[width] = {}
        for line in table.lines:
            if line.part is not None and line.part not in parts:
                out[width][line.id] = NO_PART
                continue
            selector = parts[line.part] if line.part is not None else None
            out[width][line.id] = run_axe(page, line.rules, selector)
    version = page.evaluate("axe.version")
    page.close()
    return version, out


def findings(table, swept):
    out = []
    for line in table.lines:
        f = {
            "id": line.id,
            "answer": "no match",
            "misses": [],
            "review": [],
            "unjudged": [],
        }
        applied = False
        for width, results in swept.items():
            got = results[line.id]
            if got is NO_PART:
                f["unjudged"].append(
                    {"width": width, "what": f"no selector for the part {line.part}"}
                )
                continue
            if got is None:
                continue
            f["misses"] += [{"width": width, **n} for n in got["violations"]]
            f["review"] += [{"width": width, **n} for n in got["incomplete"]]
            applied = applied or bool(set(got["applied"]) & set(line.rules))
        f["answer"] = rule_table.answer(
            misses=f["misses"], unjudged=f["unjudged"], judged=applied
        )
        out.append(f)
    return out


def report(url, found):
    lines = [f"check-markup: {url}"]
    for f in found:
        lines.append(f"{f['id']}: {f['answer']}")
        for m in f["misses"]:
            lines.append(f"  - [{m['rule']}] {m['width']} px {m['target']}: {m['why']}")
        for m in f["unjudged"]:
            lines.append(f"  ? {m['width']} px: {m['what']}")
        for m in f["review"]:
            lines.append(
                f"  review [{m['rule']}] {m['width']} px {m['target']}: {m['why']}"
            )
    return "\n".join(lines)


def parse_args(argv):
    p = argparse.ArgumentParser(
        prog="check-markup.py",
        description="Run axe-core in a page and answer the markup records its table maps to axe rule ids.",
    )
    p.add_argument("url", help="an http(s) URL, or a local HTML file")
    p.add_argument("--out", required=True, metavar="DIR", help="where markup.json goes")
    probe.part_arguments(p)
    p.add_argument("--table", default=TABLE, metavar="FILE", help="the rule table")
    p.add_argument(
        "--timeout",
        type=int,
        default=runner.LOAD_TIMEOUT_MS,
        metavar="MS",
        help="for each load",
    )
    at = p.parse_args(argv)
    at.parts, _ = probe.part_options(p, at)
    try:
        with open(at.table, encoding="utf8") as fh:
            at.table = parse(fh.read())
    except OSError as exc:
        p.error(f"cannot read --table {at.table}: {exc.strerror}")
    except TableError as exc:
        p.error(f"--table {at.table}: {exc}")
    at.url = runner.page_url(p, at.url)
    return p, at


def main(argv):
    p, at = parse_args(argv)
    when = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    os.makedirs(at.out, exist_ok=True)
    json_path = os.path.join(at.out, "markup.json")
    with contextlib.suppress(FileNotFoundError):
        os.unlink(json_path)
    with open(AXE, encoding="utf8") as fh:
        source = fh.read()

    def run():
        with runner.chromium() as browser:
            return sweep(
                browser,
                at.url,
                table=at.table,
                parts=at.parts,
                source=source,
                timeout=at.timeout,
            )

    try:
        got, code = runner.run_browser(run, at.timeout, at.url)
    except TableError as exc:
        p.print_usage(sys.stderr)
        print(f"check-markup.py: error: --table: {exc}", file=sys.stderr)
        return 2
    if code:
        return code
    version, swept = got
    found = findings(at.table, swept)
    with open(json_path, "w", encoding="utf8") as fh:
        json.dump(
            {
                "url": at.url,
                "run_at": when.isoformat(),
                "axe": version,
                "parts": at.parts,
                "answers": {f["id"]: f["answer"] for f in found},
                "findings": found,
            },
            fh,
            indent=1,
        )
    print(report(at.url, found))
    return 1 if any(f["misses"] for f in found) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
