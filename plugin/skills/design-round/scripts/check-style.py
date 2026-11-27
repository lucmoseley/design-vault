#!/usr/bin/env python3
"""Answers the rule records whose answer is a computed style, an authored
declaration or a font face's descriptor, one table line or more per record,
through probe.py.

USAGE
  python3 check-style.py <page> --out DIR [--table FILE] [--parts FILE]
        [--part NAME=SELECTOR]… [--brief KEY=VALUE]… [--step PX]
        [--widths LOW-HIGH] [--timeout MS]

THE TABLE, by default check-style.table beside this script, holds probe.py's
lines in blocks. A block runs from its
header to the next header or `end`; lines before any header run on the
page as it loads:

  under COND…        under conditions.py's conditions: scheme=light or
                     scheme=dark, forced_colours, print, rtl, locale=TAG,
                     pointer=coarse or pointer=fine, block=image, script or
                     font
  at LOW-HIGH        only at the sweep's widths from LOW to HIGH px
  across pages       on every page the page's links reach on its site
                     (check-cross.py's crawl), each read once at
                     ACROSS_WIDTH; a distinct read counts its values across
                     every page together
  compare A B        each line's MUST is `same`: every element's value
                     under condition A equals its value under B, at each
                     width
  when KEY=VALUE     only where --brief gives KEY that value; where --brief
                     gives KEY none, the block's records are not judged

`define $NAME = TEXT` lines name text the lines below use as $NAME.

Each record id's finding is fail where any line misses in any block, else
not judged where any could not be compared, else pass, else no match. DIR/style.json
holds every finding; an earlier run's is deleted. A sweep with a step over 5
px, or not over every width, prints NOT A GATING SWEEP.

EXITS 0 no miss / 1 a miss (each printed) / 2 the arguments, the table or a
selector is wrong / 3 Playwright or its browser is missing / 4 the page did not
render in time / 5 the browser refused the page / 7 a call hung that would never
return. Exits 0 and 1 print on stdout; the rest print on stderr.
An exception it does not handle once loaded exits 2, its traceback on stderr.
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
from crash_exit import run_main  # noqa: E402


probe = siblings.load(HERE, "probe.py")
cross = siblings.load(HERE, "check-cross.py")
conditions = siblings.load(HERE, "conditions.py")
rule_table = siblings.load(HERE, "rule-table.py")
layout = probe.layout
runner = siblings.load(HERE, "runner.py")

TABLE = os.path.join(HERE, "check-style.table")
ACROSS_WIDTH = layout.DESKTOP_WIDTH
SAME = "same"
DEFAULT = "page as it loads"

Block = collections.namedtuple("Block", "kind header given span brief compare rules")


TableError = rule_table.TableError


def parse(text):
    names, blocks = {}, []
    current = _block("plain", DEFAULT)
    pending = []

    def close():
        nonlocal pending
        if pending:
            blocks.append(current._replace(rules=_rules(pending, current)))
        pending = []

    for n, line in rule_table.lines(text):
        try:
            m = re.fullmatch(r"define\s+\$([\w-]+)\s*=\s*(.+)", line)
            header = None if m else _header(line)
            if m:
                names[m[1]] = m[2].strip()
            elif header is None:
                pending.append((n, _expand(line, names)))
        except TableError as exc:
            raise TableError(f"line {n}: {exc}: {line}") from None
        if header is not None:
            close()
            current = header
    close()
    if not blocks:
        raise TableError("the table holds no rule")
    return blocks


def _block(kind, header, **fields):
    base = {"given": {}, "span": None, "brief": None, "compare": None, "rules": []}
    return Block(kind, header, **{**base, **fields})


def _header(line):
    if line == "end":
        return _block("plain", DEFAULT)
    if line == "across pages":
        return _block("across", line)
    word, _, rest = line.partition(" ")
    if word == "under" and rest:
        return _block("plain", line, given=_conditions(rest))
    if word == "at":
        m = re.fullmatch(r"(\d+)-(\d+)", rest)
        if not m or int(m[1]) > int(m[2]):
            raise TableError("at wants LOW-HIGH in px")
        return _block("plain", line, span=(int(m[1]), int(m[2])))
    if word == "compare":
        sides = rest.split()
        if len(sides) != 2:
            raise TableError(
                "compare wants two conditions, e.g. scheme=light scheme=dark"
            )
        return _block("compare", line, compare=tuple(_conditions(s) for s in sides))
    if word == "when":
        key, eq, value = rest.partition("=")
        if not eq or not key.strip() or not value.strip():
            raise TableError("when wants KEY=VALUE")
        return _block("plain", line, brief=(key.strip(), value.strip()))
    return None


def _conditions(text):
    given = {}
    for word in text.split():
        key, eq, value = word.partition("=")
        if key in ("forced_colours", "print", "rtl") and not eq:
            given["print_media" if key == "print" else key] = True
        elif key in ("scheme", "locale", "pointer") and value:
            given[key] = value
        elif key == "block" and value in conditions.BLOCKABLE:
            given["block"] = (value,)
        else:
            raise TableError(
                f"{word!r} is no condition: scheme=, forced_colours, print, rtl, locale=, pointer=, block="
            )
    with contextlib.suppress(KeyError):
        conditions.one_of("scheme", given["scheme"], conditions.SCHEMES)
    with contextlib.suppress(KeyError):
        conditions.one_of("pointer", given["pointer"], conditions.POINTERS)
    return given


def _expand(line, names):
    for name in sorted(names, key=len, reverse=True):
        line = line.replace(f"${name}", names[name])
    left = re.search(r"\$[\w-]+", line)
    if left:
        raise TableError(f"{left[0]} is not defined above")
    return line


def _rules(pending, block):
    out = []
    for n, line in pending:
        if block.kind == "compare":
            head, sep, must = line.rpartition(probe.SEP)
            if not sep or must.strip() != SAME:
                raise TableError(f"line {n}: a compare line's MUST is {SAME}: {line}")
            line = f"{head}{probe.SEP}present"
        try:
            rule = probe.parse(line)[0]
        except probe.TableError as exc:
            raise TableError(f"line {n}: {str(exc).removeprefix('line 1: ')}") from None
        if block.kind in ("across", "compare") and rule.must.ref:
            raise TableError(
                f"line {n}: {block.header} pools values, so its MUST cannot compare with a read: {line}"
            )
        out.append(
            rule._replace(
                line=line if block.kind != "compare" else f"{head}{probe.SEP}{SAME}"
            )
        )
    return out


def run(browser, url, blocks, *, widths, heights, parts, brief, timeout):
    out, looping = [], 0
    for block in blocks:
        if block.brief:
            key, value = block.brief
            if key not in brief:
                out.append((block, _unbriefed(block, key)))
                continue
            if brief[key] != value:
                continue
        if block.kind == "across":
            out.append(
                (block, _across(browser, url, block, parts=parts, timeout=timeout))
            )
            continue
        span = [
            w for w in widths if not block.span or block.span[0] <= w <= block.span[1]
        ]
        if not span:
            continue
        if block.kind == "compare":
            out.append(
                (
                    block,
                    _compare(
                        browser,
                        url,
                        block,
                        widths=span,
                        heights=heights,
                        parts=parts,
                        timeout=timeout,
                    ),
                )
            )
            continue
        swept, loops = probe.sweep(
            browser,
            url,
            block.rules,
            widths=span,
            heights=heights,
            parts=parts,
            timeout=timeout,
            **block.given,
        )
        looping = max(looping, loops)
        out.append((block, probe.findings(block.rules, swept)))
    return out, looping


def _finding(rid):
    return {"id": rid, "answer": "no match", "misses": [], "unjudged": []}


def _unbriefed(block, key):
    out = {}
    for rule in block.rules:
        f = out.setdefault(rule.id, _finding(rule.id))
        f["answer"] = "not judged"
        f["unjudged"].append(
            {
                "line": rule.line,
                "read": rule.read.text,
                "subject": "the brief",
                "value": None,
                "why": f"--brief gives no {key}",
                "from": None,
                "to": None,
            }
        )
    return list(out.values())


def _held(rule, subject, value, why, *, at):
    return {
        "line": rule.line,
        "read": rule.read.text,
        "subject": subject,
        "value": value,
        "why": why,
        "from": at,
        "to": at,
    }


def _across(browser, url, block, *, parts, timeout):

    def read(page):
        page.set_default_timeout(timeout)
        return [probe.values(page, rule, parts) for rule in block.rules]

    pages, _ = cross.crawl(
        browser,
        url,
        read=read,
        viewport={"width": ACROSS_WIDTH, "height": layout.HEIGHTS[-1]},
    )
    out = {}
    for n, rule in enumerate(block.rules):
        f = out.setdefault(rule.id, _finding(rule.id))
        pooled = collections.defaultdict(set)
        judged = False
        for page_url, got in pages.items():
            for subject, group, value, why in got["read"][n]:
                judged = True
                where = f"{subject} on {page_url}"
                if rule.read.distinct:
                    if not why and value is not None and value not in rule.read.excepts:
                        pooled[group].add(value)
                    continue
                if why:
                    f["unjudged"].append(
                        _held(rule, where, value, why, at=ACROSS_WIDTH)
                    )
                    continue
                s = probe.meet(rule, where, value)
                if s.verdict != "pass":
                    f["misses" if s.verdict == "miss" else "unjudged"].append(
                        _held(rule, where, value, s.why, at=ACROSS_WIDTH)
                    )
        for group, found in pooled.items():
            s = probe.meet(rule, f"{group} across {len(pages)} pages", len(found))
            if s.verdict != "pass":
                f["misses"].append(
                    _held(rule, s.subject, len(found), s.why, at=ACROSS_WIDTH)
                )
        if judged:
            f["_judged"] = True
    return _answered(out)


def _compare(browser, url, block, *, widths, heights, parts, timeout):
    sides = []
    for given in block.compare:
        got = []
        for width, page, _ in probe.pages(
            browser, url, widths=widths, heights=heights, timeout=timeout, given=given
        ):
            got.append(
                (width, [probe.values(page, rule, parts) for rule in block.rules])
            )
        sides.append(got)
    out = {}
    names = [" ".join(f"{k}={v}" for k, v in g.items()) for g in block.compare]
    for (width, first), (_, second) in zip(*sides, strict=True):
        for n, rule in enumerate(block.rules):
            f = out.setdefault(rule.id, _finding(rule.id))
            under = collections.defaultdict(list)
            for b in second[n]:
                under[b[0]].append(b)
            for a in first[n]:
                f["_judged"] = True
                b = under[a[0]].pop(0) if under[a[0]] else None
                if b is None:
                    why = f"{a[2]} under {names[0]}, absent under {names[1]}"
                    f["misses"].append(_held(rule, a[0], a[2], why, at=width))
                elif a[3] or b[3]:
                    f["unjudged"].append(
                        _held(rule, a[0], a[2], a[3] or b[3], at=width)
                    )
                elif probe.plain(a[2]) != probe.plain(b[2]):
                    why = f"{a[2]} under {names[0]}, {b[2]} under {names[1]}"
                    f["misses"].append(_held(rule, a[0], a[2], why, at=width))
            for rest in under.values():
                for b in rest:
                    f["_judged"] = True
                    why = f"absent under {names[0]}, {b[2]} under {names[1]}"
                    f["misses"].append(_held(rule, b[0], b[2], why, at=width))
    return _answered(out)


def _answered(out):
    for f in out.values():
        judged = f.pop("_judged", False)
        f["answer"] = rule_table.answer(
            misses=f["misses"], unjudged=f["unjudged"], judged=judged
        )
    return list(out.values())


def merged(ran):
    out = {}
    for block, found in ran:
        for f in found:
            m = out.setdefault(f["id"], _finding(f["id"]))
            for bucket in ("misses", "unjudged"):
                m[bucket] += [{**held, "block": block.header} for held in f[bucket]]
            m["answer"] = max(m["answer"], f["answer"], key=rule_table.ANSWERS.index)
    return list(out.values())


def report(at, widths, found, *, looping, json_path):
    lines = [
        f"check-style: {at.url}",
        f"read {sum(len(b.rules) for b in at.blocks)} rule line(s) for {len(found)} record(s) at {len(widths)} widths, {at.span[0]}–{at.span[1]} px every {at.step} px",
    ]
    if not layout.gating(at):
        lines.append(
            f"NOT A GATING SWEEP: the craft gate needs {layout.LOW}–{layout.HIGH} px every {layout.GATE_STEP} px or finer to {layout.STEPPED}"
        )
    if looping:
        lines.append(
            f"{looping} looping animation(s) never finish, so the page was read mid-loop"
        )
    for f in found:
        lines.append(f"{f['id']}: {f['answer']}")
        for bucket, title in (("misses", "miss"), ("unjudged", "not judged")):
            for held in f[bucket]:
                widths_at = (
                    layout.span(held) if held["from"] is not None else "the brief"
                )
                lines.append(
                    f"  {title}, {held['block']}, {widths_at}: {held['subject']} {held['read']} {probe.shown(held['value'])}: {held['why']}"
                )
    lines.append(f"every finding: {json_path}")
    return "\n".join(lines)


def parse_args(argv):
    p = argparse.ArgumentParser(
        prog="check-style.py",
        description="Answer the computed-style rule records on a page, one finding per record id.",
    )
    p.add_argument("--table", default=TABLE, metavar="FILE", help="the rule table")
    probe.page_arguments(p, "style.json")
    p.add_argument(
        "--brief",
        dest="brief_given",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="a fact the brief states, for when blocks: energy=calm",
    )
    at = p.parse_args(argv)
    probe.page_options(p, at)
    at.heights = layout.HEIGHTS
    at.brief = {}
    for given in at.brief_given:
        key, eq, value = given.partition("=")
        if not eq or not key.strip() or not value.strip():
            p.error(f"--brief wants KEY=VALUE, got {given!r}")
        at.brief[key.strip()] = value.strip()
    try:
        with open(at.table, encoding="utf8") as fh:
            at.blocks = parse(fh.read())
    except OSError as exc:
        p.error(f"cannot read --table {at.table}: {exc.strerror}")
    except TableError as exc:
        p.error(f"--table {at.table}: {exc}")
    at.rules = [r for b in at.blocks for r in b.rules]
    at.url = runner.page_url(p, at.url)
    return p, at


def main(argv):
    p, at = parse_args(argv)
    os.makedirs(at.out, exist_ok=True)
    json_path = os.path.join(at.out, "style.json")
    with contextlib.suppress(FileNotFoundError):
        os.unlink(json_path)
    when = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    widths = layout.sweep_widths(at.step, *at.span)
    blocks = [without(b, at.parts) for b in at.blocks]

    def go():
        with runner.chromium() as browser:
            return run(
                browser,
                at.url,
                [b for b in blocks if b.rules],
                widths=widths,
                heights=at.heights,
                parts=at.parts,
                brief=at.brief,
                timeout=at.timeout,
            )

    try:
        got, code = runner.run_browser(go, at.timeout, at.url)
    except probe.ProbeError as exc:
        p.print_usage(sys.stderr)
        print(f"check-style.py: error: {exc}", file=sys.stderr)
        return 2
    if code:
        return code
    ran, looping = got
    found = merged(ran)
    ids = list(dict.fromkeys(r.id for r in at.rules))
    found = sorted(
        found + [_finding(i) for i in ids if i not in {f["id"] for f in found}],
        key=lambda f: ids.index(f["id"]),
    )
    with open(json_path, "w", encoding="utf8") as fh:
        json.dump(
            {
                "url": at.url,
                "run_at": when.isoformat(),
                "gating": layout.gating(at),
                "step": at.step,
                "span": at.span,
                "parts": at.parts,
                "brief": at.brief,
                "looping_animations": looping,
                "answers": {f["id"]: f["answer"] for f in found},
                "findings": found,
            },
            fh,
            indent=1,
        )
    print(report(at, widths, found, looping=looping, json_path=json_path))
    return 1 if any(f["misses"] for f in found) else 0


# #274
def without(block, parts):

    def reads(rule):
        named = {rule.select.value} if rule.select.source == "part" else set()
        if (
            rule.must.ref
            and rule.must.ref.select
            and rule.must.ref.select.source == "part"
        ):
            named.add(rule.must.ref.select.value)
        return named

    return block._replace(rules=[r for r in block.rules if reads(r) <= set(parts)])


if __name__ == "__main__":
    run_main(main)
