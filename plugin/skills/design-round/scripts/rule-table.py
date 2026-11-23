"""The rule tables the design-round checks read, and the answers they give.

Each check script loads this file the way it loads probe.py:

    rules = _load("rule_table", os.path.join(HERE, "rule-table.py"))
    for n, line in rules.lines(text): ...          # each rule line, numbered
    table = rules.parse(text, CHECKS, value)        # ID | CHECK [| VALUE]
    answers = rules.Answers(table, "where")         # one finding per record id

A bad line raises TableError, naming the line; the check exits 2 on it.
"""

import collections
import re

SEP = " | "

# One `ID | CHECK [| VALUE]` line: the record id, the check, the value the
# script's `value` hook made of it, and the line as written.
Line = collections.namedtuple("Line", "id check value text")


class TableError(Exception):
    """A table line a check cannot read: exit 2."""


def lines(text):
    """(n, line) for each line holding a rule: stripped, numbered from 1,
    with blank lines and `#` comments left out."""
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if line and not line.startswith("#"):
            yield n, line


def parse(text, checks, value):
    """The `ID | CHECK [| VALUE]` lines of `text` as Line records, in order.

    `checks` maps each check to the pattern its whole VALUE must match, or to
    None for a check that reads none. `value(n, check, match)` gives the
    Line's value: `match` is the VALUE's full match, or None where the check
    reads none; it may raise TableError for a value the pattern lets through.
    """
    out = []
    for n, line in lines(text):
        fields = [f.strip() for f in line.split(SEP)]
        if len(fields) not in (2, 3) or not all(fields):
            raise TableError(f"line {n}: want ID | CHECK [| VALUE], got {line!r}")
        check = fields[1]
        if check not in checks:
            raise TableError(
                f"line {n}: no check {check!r}; the checks are {', '.join(checks)}"
            )
        shape, given = checks[check], fields[2] if len(fields) == 3 else None
        if shape is None:
            if given is not None:
                raise TableError(f"line {n}: {check} reads no value, got {given!r}")
            out.append(Line(fields[0], check, value(n, check, None), line))
            continue
        shape = re.compile(shape)
        m = shape.fullmatch(given or "")
        if not m:
            raise TableError(
                f"line {n}: {check} wants a value like {shape.pattern!r}, got {given!r}"
            )
        out.append(Line(fields[0], check, value(n, check, m), line))
    if not out:
        raise TableError("the table has no lines")
    return out


class Answers:
    """The findings being gathered, one per record id in table order.

    Each miss, unjudged and review entry is {"check", <places>, "what"}.
    With one place named, `at` is its value; with more, `at` is a dict of
    them, or None, and a place it lacks is None. `review` adds the review
    list, for findings a person must look at.
    """

    def __init__(self, table, *places, review=False):
        self.places = places
        self.found = {}
        for line in table:
            self.found[line.id] = {
                "id": line.id,
                "answer": "no match",
                "misses": [],
                "unjudged": [],
            }
            if review:
                self.found[line.id]["review"] = []
        self.judged = set()

    def _entry(self, line, at, what):
        if len(self.places) == 1:
            at = {self.places[0]: at}
        at = at or {}
        return {
            "check": line.check,
            **{place: at.get(place) for place in self.places},
            "what": what,
        }

    def miss(self, line, at, what):
        self.judged.add(line.id)
        self.found[line.id]["misses"].append(self._entry(line, at, what))

    def unjudged(self, line, at, what):
        self.found[line.id]["unjudged"].append(self._entry(line, at, what))

    def review(self, line, at, what):
        self.found[line.id]["review"].append(self._entry(line, at, what))

    def met(self, line):
        self.judged.add(line.id)

    def done(self):
        """The findings, each answered: fail on a miss, else not judged on an
        unjudged entry, else pass where a line was compared, else no match."""
        for f in self.found.values():
            if f["misses"]:
                f["answer"] = "fail"
            elif f["unjudged"]:
                f["answer"] = "not judged"
            elif f["id"] in self.judged:
                f["answer"] = "pass"
        return list(self.found.values())
