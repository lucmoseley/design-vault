import collections
import re

SEP = " | "

Line = collections.namedtuple("Line", "id check value text")


ANSWERS = ("no match", "pass", "not judged", "fail")


def answer(misses, unjudged, judged):
    if misses:
        return "fail"
    if unjudged:
        return "not judged"
    return "pass" if judged else "no match"


class TableError(Exception):
    pass


def lines(text):
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if line and not line.startswith("#"):
            yield n, line


def parse(text, checks, value):
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
        for f in self.found.values():
            f["answer"] = answer(f["misses"], f["unjudged"], f["id"] in self.judged)
        return list(self.found.values())
