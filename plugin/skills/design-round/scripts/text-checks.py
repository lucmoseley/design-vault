"""text-checks.py — check-text.py's checks (#314): what each text record asks
of a page check-text.py has read, its table and word lists, and how each
load's findings merge into one answer per record.

A load is Load(condition, width, data): data is what check-text.py's page
read returns, with `formatted` added under a locale load and `offer` on the
desktop load. A check takes (load, its table values, the word lists) and
returns a Found.
"""

import collections
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "rule_table", os.path.join(HERE, "rule-table.py")
)
rule_table = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rule_table)

PAGE = "page"
RTL = "rtl"
SEP = " | "
# How much text either side of a miss its report keeps: a guess, enough to
# find it on the page.
CONTEXT = 24
# Running text, for vault.emphasis-share.
PROSE_TAGS = ("p", "li", "dd", "blockquote", "figcaption")
# The kinds of element vault.label-case reads.
CASE_KINDS = ("heading", "button", "link", "list-item", "menu-item")
# Attribute text no visitor sees, which vault.typed-case leaves out.
UNSEEN = ("aria-label", "alt")
WEEKDAYS = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)
TWELVE_HOUR = ("h11", "h12")
# Spaces that join what they sit between, and spaces wider than a word space.
NO_BREAK = "\u00a0\u202f\u2060"
WIDE = "\u00a0\u2000-\u200a\u202f\u205f\u3000"
# A digit group separator: a stop, comma, apostrophe or a no-break or thin
# space; a plain space is not one, being a break between words.
GROUP_CHARS = ".,'’\u00a0\u202f\u2009"
SPACE_GROUP = "\u00a0\u202f\u2009"
CURRENCY = "$€£¥"
WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")
LETTERS = re.compile(r"[^\W\d_]")
# A typed fraction: digits, a slash and digits, with no digit, slash or
# decimal marker either side, so a date such as 1/2/2026 is none.
FRACTION = r"(?<![\d/.,])(\d+)\/(\d+)(?![\d/.,])"

Load = collections.namedtuple("Load", "condition width data")


TableError = rule_table.TableError


class WordsError(Exception):
    pass


# ----------------------------------------------------------------- helpers


def prose(block):
    return "".join(r["text"] for r in block["runs"] if not r["code"])


def code(block):
    return "".join(r["text"] for r in block["runs"] if r["code"])


def snippet(text, start, end=None):
    end = start + 1 if end is None else end
    return " ".join(text[max(0, start - CONTEXT) : end + CONTEXT].split())


def miss(block, text, span, what):
    """A miss on `block`, quoting its text around `span`: a match or (start, end)."""
    start, end = span.span() if hasattr(span, "span") else span
    return {"place": block["place"], "text": snippet(text, start, end), "what": what}


def chars(value):
    return "".join(value.split())


def alternation(words):
    return "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True))


def rendered(run):
    t = run["transform"]
    if t == "uppercase":
        return run["text"].upper()
    if t == "lowercase":
        return run["text"].lower()
    if t == "capitalize":
        return re.sub(r"(?<![^\W\d_])[^\W\d_]", lambda m: m[0].upper(), run["text"])
    return run["text"]


def locale_of(load, block, f):
    """The block's locale data, or None, adding to `f` why a lang tag the
    browser cannot read is not judged."""
    locales = load.data["locales"]
    loc = locales.get(block["lang"])
    if loc is None and block["lang"] in locales:
        u = {"place": "", "what": f"lang {block['lang']!r} is no locale tag"}
        if u not in f.unjudged:
            f.unjudged.append(u)
    return loc


class Found:
    """What one check found under one load: its misses, how many things it
    judged, and what it could not read."""

    def __init__(self):
        self.misses, self.judged, self.unjudged = [], 0, []

    def add(self, m):
        self.misses.append(m)


# ------------------------------------------------------------------ checks


def prose_quotes(load, v, words):
    f = Found()
    straight = re.compile(f"[{re.escape(chars(v['straight']))}]")
    opening = re.compile(
        rf"(?<!\w)(?:{alternation(chars(v['opening']))})(?:\d\ds\b|(?:{alternation(words['elisions'])})\b)",
        re.IGNORECASE,
    )
    for b in load.data["blocks"]:
        text = prose(b)
        if not re.search(r"['\"‘’“”]", text):
            continue
        f.judged += 1
        for m in straight.finditer(text):
            # After a digit a straight mark is a measure, vault.prime-marks'
            # own; before a letter it is still an apostrophe (2026's).
            after_digit = m.start() and text[m.start() - 1].isdigit()
            if after_digit and not text[m.end() : m.end() + 1].isalpha():
                continue
            f.add(miss(b, text, m, f"straight {m[0]} where a curly mark belongs"))
        for m in opening.finditer(text):
            f.add(miss(b, text, m, f"{m[0][0]} opens an elision, which takes ’"))
    return f


def code_quotes(load, v, words):
    f = Found()
    curly = re.compile(f"[{re.escape(chars(v['curly']))}]")
    for b in load.data["blocks"]:
        text = code(b)
        if not text.strip():
            continue
        f.judged += 1
        for m in curly.finditer(text):
            f.add(miss(b, text, m, f"curly {m[0]} inside code"))
    return f


PAIRS = {"’": "‘", "”": "“"}


def prime_marks(load, v, words):
    f = Found()
    curly = chars(v["curly"])
    mark = re.compile(rf"(?<=\d)['\"′″{re.escape(curly)}]")
    for b in load.data["blocks"]:
        text = prose(b)
        for m in mark.finditer(text):
            # A mark a letter follows is an apostrophe (2026’s), no measure.
            if text[m.end() : m.end() + 1].isalpha():
                continue
            f.judged += 1
            c, before = m[0], text[: m.start()]
            if c not in curly:
                continue
            if c in PAIRS and before.count(PAIRS[c]) > before.count(c):
                continue
            f.add(
                miss(
                    b,
                    text,
                    (m.start() - 1, m.end()),
                    f"curly {c} as a measurement mark",
                )
            )
    return f


def subtraction(hyphen):
    """A spaced hyphen between two numbers an equals sign follows: 5 - 3 = 2."""
    return re.compile(rf"(?<=\d) ?[{hyphen}] ?(?=\d[\d.,]* ?=)")


def math_signs(load, v, words):
    f = Found()
    times = re.compile(
        rf"(?<![\w.,])\d+(?:[.,]\d+)? ?[{re.escape(chars(v['times']))}] ?\d"
    )
    hex_number = re.compile(r"0[xX][0-9A-Fa-f]")
    minus = re.compile(rf"(?:^|(?<=[\s(=:]))[{re.escape(chars(v['minus']))}](?=\d)")
    minus_between = subtraction(re.escape(chars(v["minus"])))
    for b in load.data["blocks"]:
        text = prose(b)
        if not re.search(r"\d", text):
            continue
        f.judged += 1
        for m in times.finditer(text):
            if not hex_number.fullmatch(m[0][:3]):
                f.add(miss(b, text, m, "a letter x where × belongs"))
        for m in [*minus.finditer(text), *minus_between.finditer(text)]:
            f.add(
                miss(
                    b,
                    text,
                    (m.start(), m.end() + 1),
                    "a hyphen where the minus − belongs",
                )
            )
    return f


def dash_glyphs(load, v, words):
    f = Found()
    h, em = re.escape(chars(v["hyphen"])), re.escape(chars(v["em"]))
    double = re.compile(rf"(?<!{h}){h}{h}(?!{h})")
    spaced = re.compile(rf"(?<=\S)[ \u00a0]{h}[ \u00a0](?=\S)")
    minus_between = subtraction(h)
    suffix = rf"(?:{alternation(words['meridiem'])}|%)"
    lead = rf"[{CURRENCY}]?(?P<a>\d+)(?P<a_unit>{suffix})?"
    tail = rf"[{CURRENCY}]?(?P<b>\d+)(?P<b_unit>{suffix})?"
    span = re.compile(rf"(?<![\w.,/{h}]){lead}{h}{tail}(?![\w.,/{h}])")
    # A phone number written as three digits and four: 555-1234.
    phone = re.compile(rf"\d{{3}}{h}\d{{4}}")
    # Em dashes between two words; one opening an attribution, or standing
    # alone in a cell, sets no spacing for the page.
    flush = re.compile(rf"(?<=\w){em}(?=\w)")
    spaced_em = re.compile(rf"(?<=\w)[ \u00a0]{em}[ \u00a0](?=\w)")
    ems = {"flush": [], "spaced": []}
    for b in load.data["blocks"]:
        plain = "".join(r["text"] for r in b["runs"] if not (r["code"] or r["plain"]))
        if not re.search(rf"[{h}{em}–]", plain):
            continue
        f.judged += 1
        for m in double.finditer(plain):
            f.add(miss(b, plain, m, "a double hyphen where a dash belongs"))
        for m in spaced.finditer(plain):
            if not minus_between.match(plain, m.start()):
                f.add(miss(b, plain, m, "a spaced hyphen where a dash belongs"))
        for m in span.finditer(plain):
            if phone.fullmatch(m[0]):
                continue
            first, second = m["a"], m["b"]
            # 2025-26 abbreviates 2025-2026; a time range such as 9am-5pm
            # runs past noon, so its numbers need not rise.
            rises = (
                int(first) < int(second)
                if len(second) >= len(first)
                else int(first[-len(second) :]) < int(second)
            )
            if rises or m["a_unit"] or m["b_unit"]:
                f.add(miss(b, plain, m, "a hyphen in a range, which takes –"))
        ems["flush"] += [(b, plain, m) for m in flush.finditer(plain)]
        ems["spaced"] += [(b, plain, m) for m in spaced_em.finditer(plain)]
    if ems["flush"] and ems["spaced"]:
        # The fewer are the odd ones out; a tie reports the flush ones, a
        # guess, as neither is then the page's way.
        fewer = min(ems, key=lambda k: len(ems[k]))
        other = "spaced" if fewer == "flush" else "set flush"
        for b, text, m in ems[fewer]:
            f.add(
                miss(
                    b,
                    text,
                    m,
                    f"an em dash {'set flush' if fewer == 'flush' else 'spaced'} where the page's others are {other}",
                )
            )
    return f


def leading_zero(load, v, words):
    f = Found()
    bare = re.compile(
        rf"(?:^|(?<=[\s(\[−+±{CURRENCY}-]))[{re.escape(chars(v['markers']))}]\d"
    )
    for b in load.data["blocks"]:
        text = prose(b)
        if not re.search(r"\d", text):
            continue
        f.judged += 1
        for m in bare.finditer(text):
            f.add(miss(b, text, m, "a decimal with no zero before its marker"))
    return f


NUMBER = re.compile(rf"(?<![\w.,'’#+\-{SPACE_GROUP}])\d+(?:[{GROUP_CHARS}]\d+)*(?!\w)")
SEPARATOR = re.compile(f"[{GROUP_CHARS}]")


def _same(a, b):
    """Separators equal, every no-break or thin space counting as one."""
    space = f"[{SPACE_GROUP}]"
    return re.sub(space, " ", a) == re.sub(space, " ", b)


def number_shape(token, loc):
    """(integer groups, group separator or None, decimal marker or None) of a
    number token as the locale `loc` reads it, or None where it is no number
    shown as data: a date, a version or a code. The group sizes are CLDR's:
    a lead group of 1 to 3 digits, middle groups of 2 (Indian) or 3, and a
    last group of 3."""
    groups = SEPARATOR.split(token)
    seps = SEPARATOR.findall(token)
    if not seps:
        return None
    kinds = {re.sub(f"[{SPACE_GROUP}]", " ", s) for s in seps}

    def grouped(ints):
        return (
            1 <= len(ints[0]) <= 3
            and all(2 <= len(g) <= 3 for g in ints[1:-1])
            and len(ints[-1]) == 3
        )

    if len(kinds) == 2:
        if len(set(seps[:-1])) != 1 or seps[-1] in seps[:-1]:
            return None
        return (groups[:-1], seps[0], seps[-1]) if grouped(groups[:-1]) else None
    if len(kinds) > 2:
        return None
    if len(seps) >= 2:
        return (groups, seps[0], None) if grouped(groups) else None
    a, b = groups
    if len(b) == 3 and len(a) <= 3:
        if (
            loc["decimal"]
            and _same(seps[0], loc["decimal"])
            and not _same(seps[0], loc["group"] or "")
        ):
            return [a], None, seps[0]
        return [a, b], seps[0], None
    return [a], None, seps[0]


def number_tokens(load, f=None):
    """Each number shown as data, with its block, the block's text, its
    match, its shape and its locale. Numbers follow the page's lang (the
    record's target), so the browser locale counts only where no lang is
    given."""
    f = f if f is not None else Found()
    for b in load.data["blocks"]:
        loc = locale_of(load, b, f)
        if not loc:
            continue
        text = "".join(r["text"] for r in b["runs"] if not (r["code"] or r["plain"]))
        for m in NUMBER.finditer(text):
            shape = number_shape(m[0], loc)
            if shape is not None:
                yield b, text, m, shape, loc


def locale_numbers(load, v, words):
    f = Found()
    least = int(v["digits"])
    formatted = load.data.get("formatted", {})
    near_time = re.compile(rf"^\s?(?:{alternation(words['time-words'])})(?!\w)")
    before_time = re.compile(rf"(?<!\w)(?:{alternation(words['time-words'])})\s?$")
    for b, text, m, shape, loc in number_tokens(load, f):
        ints, group, decimal = shape
        if near_time.match(text[m.end() :]) or before_time.search(text[: m.start()]):
            continue
        digits = "".join(ints)
        if len(digits) < least and decimal is None:
            continue
        f.judged += 1
        if decimal is not None and not _same(decimal, loc["decimal"] or ""):
            f.add(
                miss(
                    b,
                    text,
                    m,
                    f"decimal marker {decimal!r}, where {loc['tag']} writes {loc['decimal']!r}",
                )
            )
            continue
        want = formatted[(loc["tag"], digits)]
        got = (group or "").join(ints)
        if not _same(got, want):
            f.add(miss(b, text, m, f"{got} where {loc['tag']} writes {want}"))
    return f


def week_hour(load, v, words):
    """Against the text's lang, or under a locale load the browser's locale,
    the visitor's own choice. A lang naming no region (en) is not judged:
    its week and clock differ by region."""
    f = Found()
    browser = load.data.get("browser")

    def wants(loc, key):
        return {x[key] for x in (loc, browser) if x and x[key]}

    def regionless(lang, place):
        if lang and not load.data["locales"][lang]["region"]:
            f.unjudged.append(
                {
                    "place": place,
                    "what": f"lang {lang!r} names no region, so its week and clock are unknown",
                }
            )
            return True
        return False

    for c in load.data["calendars"]:
        loc = locale_of(load, c, f)
        if loc is None or regionless(c["lang"], c["place"]):
            continue
        firsts = wants(loc, "firstDay")
        if not firsts:
            f.unjudged.append(
                {
                    "place": c["place"],
                    "what": "the browser gives no first weekday for its locale",
                }
            )
            continue
        f.judged += 1
        if c["first"] not in firsts:
            f.add(
                {
                    "place": c["place"],
                    "text": "",
                    "what": f"the week starts on {WEEKDAYS[c['first'] - 1]}, where {loc['tag']} starts it on {WEEKDAYS[loc['firstDay'] - 1]}",
                }
            )
    meridiem = alternation(words["meridiem"])
    twelve = re.compile(rf"(?<![\d:.])\d{{1,2}}(?:[:.][0-5]\d)? ?(?:{meridiem})(?!\w)")
    twenty_four = re.compile(
        rf"(?<![\d:.])([01]?\d|2[0-3]):[0-5]\d(?![\d:])(?! ?(?:{meridiem})(?!\w))"
    )
    # A time just after an opening bracket is a duration, a video's or a
    # track's (14:32).
    duration = re.compile(r"\(\s*$")
    for b in load.data["blocks"]:
        loc = locale_of(load, b, f)
        if not loc or not loc["hourCycle"]:
            continue
        text = prose(b)
        times = [*twelve.finditer(text), *twenty_four.finditer(text)]
        if not times or regionless(b["lang"], b["place"]):
            continue
        cycles = wants(loc, "hourCycle")
        twelve_ok = bool(cycles & set(TWELVE_HOUR))
        twenty_four_ok = bool(cycles - set(TWELVE_HOUR))
        for m in twelve.finditer(text):
            f.judged += 1
            if not twelve_ok:
                f.add(
                    miss(
                        b,
                        text,
                        m,
                        f"a 12-hour time, where {loc['tag']} uses {loc['hourCycle']}",
                    )
                )
        for m in twenty_four.finditer(text):
            # An hour of 1 to 12 with no meridiem reads as either cycle.
            if 1 <= int(m[1]) <= 12 or duration.search(text[: m.start()]):
                continue
            f.judged += 1
            if not twenty_four_ok:
                f.add(
                    miss(
                        b,
                        text,
                        m,
                        f"a 24-hour time, where {loc['tag']} uses {loc['hourCycle']}",
                    )
                )
    return f


def acronyms_of(words):
    return set(
        words["acronyms"]
        + words["currencies"]
        + words["time-zones"]
        + words["meridiem"]
    )


def typed_case(load, v, words):
    f = Found()
    letters, least = int(v["letters"]), int(v["least"])
    acronyms = acronyms_of(words)
    for b in load.data["blocks"]:
        if b.get("attr") in UNSEEN:
            continue
        text = prose(b)
        found = list(WORD.finditer(text))
        if not found:
            continue
        f.judged += 1
        caps = [
            len(w[0]) >= least and w[0].isupper() and w[0] not in acronyms
            for w in found
        ]
        # Two capitals words side by side: only spaces between them, so a
        # comma's list (EUR, USD) is no pair.
        pair = [
            caps[i] and caps[i + 1] and not text[w.end() : found[i + 1].start()].strip()
            for i, w in enumerate(found[:-1])
        ]
        for i, w in enumerate(found):
            if not caps[i]:
                continue
            beside = (i and pair[i - 1]) or (i < len(pair) and pair[i])
            if len(w[0]) >= letters or beside:
                f.add(
                    miss(
                        b, text, w, "text typed in capitals, which text-transform sets"
                    )
                )
                break
    return f


def caps_extent(load, v, words):
    f = Found()
    most_lines, most_words = int(v["lines"]), int(v["words"])
    acronyms = acronyms_of(words)
    for u in load.data["caps"]:
        found = WORD.findall(u["text"])
        if not found:
            continue
        if not u["styled"] and all(w in acronyms or not w.isupper() for w in found):
            continue
        f.judged += 1
        if u["lines"] > most_lines or len(found) > most_words:
            f.add(
                {
                    "place": u["place"],
                    "text": snippet(u["text"], 0, len(u["text"])),
                    "what": f"{len(found)} words on {u['lines']} line(s) in capitals, past {most_words} words on {most_lines}",
                }
            )
    return f


# Text that is an address, not a label: an email, a URL or a handle.
ADDRESS = re.compile(r"@|://|^www\.", re.IGNORECASE)
# A word with a capital inside it (iPhone, eBay) keeps its own case.
INNER_CAPITAL = re.compile(r"^\w*[a-z]\w*[A-Z]")


def label_case(load, v, words):
    """vault.label-case: a later capitalised word is title case when it is
    lower-cased elsewhere on the page or in [common-words]; a name never is."""
    f = Found()
    share = float(v["share"])
    names = set(words["proper-nouns"]) | acronyms_of(words)
    common = set(words["common-words"])
    for b in load.data["blocks"]:
        common |= {w for w in WORD.findall(prose(b)) if w.islower()}
    for b in load.data["blocks"]:
        if not set(b["kinds"]) & set(CASE_KINDS):
            continue
        runs = [r for r in b["runs"] if not r["code"] and LETTERS.search(r["text"])]
        if not runs or all(r["caps"] for r in runs):
            continue
        text = "".join(rendered(r) for r in runs).strip()
        found = list(WORD.finditer(text))
        if not found or ADDRESS.search(text):
            continue
        f.judged += 1
        first = found[0][0]
        if (
            text[0].isalpha()
            and first[0].islower()
            and first not in names
            and not INNER_CAPITAL.match(first)
        ):
            f.add(
                miss(
                    b,
                    text,
                    (0, len(first)),
                    "starts in lower case, where sentence case starts with a capital",
                )
            )
            continue
        capital, title = [], []
        for i, w in enumerate(found[1:], 1):
            word = w[0]
            starts = re.search(r"[.!?:]\s*$", text[found[i - 1].end() : w.start()])
            if starts or word.isupper() or word in names or not word[0].isupper():
                continue
            capital.append(word)
            if word.lower() in common:
                title.append(word)
        if title and len(title) >= share * len(capital):
            f.add(
                miss(
                    b,
                    text,
                    (0, len(text)),
                    f"title case ({', '.join(title)}), where sentence case belongs",
                )
            )
    return f


def emphasis_share(load, v, words):
    f = Found()
    least, share, longest = int(v["words"]), float(v["share"]), int(v["run"])
    heavy = float(v["weight"])
    for b in load.data["blocks"]:
        if b["tag"] not in PROSE_TAGS or b.get("attr"):
            continue
        text, marks = "", []
        for r in b["runs"]:
            if r["code"]:
                continue
            strong = r["weight"] >= heavy and r["weight"] > b["weight"]
            slant = r["italic"] and not b["italic"]
            text += r["text"]
            # A bold link is the link's style, vault.link-style's own.
            marks += [(strong or slant) and not (r["cite"] or r["link"])] * len(
                r["text"]
            )
        found = list(WORD.finditer(text))
        if len(found) < least:
            continue
        f.judged += 1
        emphatic = [all(marks[w.start() : w.end()]) for w in found]
        run = best = 0
        for e in emphatic:
            run = run + 1 if e else 0
            best = max(best, run)
        if sum(emphatic) / len(found) > share:
            f.add(
                miss(
                    b,
                    text,
                    (0, len(text)),
                    f"{sum(emphatic)} of {len(found)} words in bold or italic, past {share:.0%}",
                )
            )
        if best > longest:
            f.add(
                miss(
                    b,
                    text,
                    (0, len(text)),
                    f"a run of {best} words in bold or italic, past {longest}",
                )
            )
    return f


def nonbreaking(load, v, words):
    f = Found()
    most = int(v["joined"])
    gap = rf"[ {NO_BREAK}]"
    patterns = (
        (
            re.compile(
                rf"(?<![\w.])\d+(?:[.,]\d+)?({gap})(?:{alternation(words['units'])})(?!\w)"
            ),
            "a number and its unit",
        ),
        (
            re.compile(
                rf"(?<!\w)(?:{alternation(words['reference-labels'])})({gap})(?=\d|[A-Z]\b)"
            ),
            "a reference and its number",
        ),
        (
            re.compile(
                rf"(?<!\w)(?:{alternation(words['honorifics'])})({gap})(?=[A-Z])"
            ),
            "an honorific and the name",
        ),
        (
            re.compile(rf"(?:{alternation(words['signs'])})({gap})(?=\w)"),
            "a sign and its word",
        ),
        (re.compile(rf"(?<=\d)({gap})[×=+−]({gap})?(?=\d)"), "a short expression"),
        (re.compile(rf"(?<=\d[×=+−])({gap})(?=\d)"), "a short expression"),
    )
    joined = re.compile(rf"[^\s]+(?:[{NO_BREAK}][^\s]+){{{most + 1},}}")
    for b in load.data["blocks"]:
        text = prose(b)
        for pattern, what in patterns:
            for m in pattern.finditer(text):
                f.judged += 1
                if " " in [m[i] for i in range(1, (m.lastindex or 0) + 1)]:
                    f.add(miss(b, text, m, f"a breaking space between {what}"))
        for m in joined.finditer(text):
            f.judged += 1
            n = len(re.findall(f"[{NO_BREAK}]", m[0]))
            f.add(miss(b, text, m, f"{n} no-break spaces in a row, past {most}"))
    return f


def soft_hyphens(load, v, words):
    f = Found()
    most = int(v["words"])
    for b in load.data["blocks"]:
        text = prose(b)
        carrying = [w for w in text.split() if "\u00ad" in w]
        if not carrying:
            continue
        f.judged += 1
        if len(carrying) > most:
            at = text.index("\u00ad")
            f.add(
                miss(
                    b,
                    text.replace("\u00ad", "-"),
                    (at, at + 1),
                    f"{len(carrying)} words carry soft hyphens, past {most}",
                )
            )
    return f


def sentence_space(load, v, words):
    f = Found()
    ends = re.escape(chars(v["ends"]))
    closers = r"[\"”’)\]]*"
    wide = re.compile(rf"(?<=[{ends}]){closers}(\s*[{WIDE}]\s*)(?=[A-Z])")
    doubled = re.compile(rf"(?<=[{ends}]){closers}( {{2,}})(?=[A-Z])")
    labels = set(words["reference-labels"]) | set(words["honorifics"])
    for b in load.data["blocks"]:
        text = prose(b)
        if not re.search(rf"[{ends}]{closers}\s", text):
            continue
        f.judged += 1
        found = list(wide.finditer(text))
        if b["collapse"] != "collapse":
            found += list(doubled.finditer(text))
        for m in found:
            before = re.search(r"(\S+)$", text[: m.start()])
            if before and before[1] in labels:
                continue
            f.add(miss(b, text, m, "a wide or doubled space between sentences"))
    return f


def fractions(load, v, words):
    """A fraction is a rising pair over a denominator the table names, with
    no counting word before it: 9/10 is a rating and Slide 1/5 a count."""
    f = Found()
    feature = v["feature"]
    denominators = set(v["denominators"].split())
    counting = re.compile(
        rf"(?<!\w)(?:{alternation(words['count-words'])})\s*$", re.IGNORECASE
    )
    for x in load.data["fractions"]:
        top, bottom = x["text"].split("/")
        if not int(top) < int(bottom) or bottom not in denominators:
            continue
        if counting.search(x["before"]):
            continue
        f.judged += 1
        if feature not in x["numeric"].split():
            what = f"a typed fraction set without {feature}"
        elif not x["alone"]:
            what = f"{feature} on an element holding more than the fraction"
        elif not x["drawsFeature"]:
            what = f"the face draws no glyphs for {feature}"
        else:
            continue
        f.add({"place": x["place"], "text": x["text"], "what": what})
    return f


def rtl_digit_order(load, v, words):
    f = Found()
    for x in load.data["rtl"]:
        f.judged += 1
        if x["reversed"]:
            f.add(
                {
                    "place": x["place"],
                    "text": x["text"],
                    "what": "a number's digits drawn right to left",
                }
            )
    return f


def offer_end_date(load, v, words):
    """Read off load.data['offer']: None where the part is absent, a string
    saying why it is not judged, else each element's text and its text once
    the watch passed."""
    f = Found()
    got = load.data.get("offer")
    if got is None:
        return f
    if isinstance(got, str):
        f.unjudged.append({"place": "", "what": got})
        return f
    meridiem = alternation(words["meridiem"])
    clock = re.compile(
        rf"(?<![\d.,])\d{{1,2}}(?:[:.][0-5]\d|\s?(?:{meridiem})(?!\w))(?![\d.,])"
        rf"|(?<!\w)(?:{alternation(words['clock-words'])})(?!\w)",
        re.IGNORECASE,
    )
    numeric_date = re.compile(
        r"(?<!\d)(?:\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{4}-\d{2}-\d{2})(?!\d)"
    )
    price = re.compile(
        rf"[{CURRENCY}]\s?\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)?\s?[{CURRENCY}]"
    )
    zone = re.compile(
        rf"(?<!\w)(?:(?:{alternation(words['time-zones'])})(?:\s?[+−-]\d{{1,2}}(?::?\d\d)?)?"
        r"|[A-Z][a-z]+/[A-Z][A-Za-z_]+)(?!\w)"
    )
    for x in got:
        f.judged += 1
        text = x["text"]
        month = re.compile(
            rf"(?<!\w)(?:{alternation(x['months'])})(?!\w)", re.IGNORECASE
        )
        dated = numeric_date.search(text) or (
            month.search(text) and re.search(r"\d", text)
        )
        # A price's figures are no time (€12.50); the clock's own bounds
        # already refuse a date's (30.11.2026).
        undated = price.sub(" ", text)
        lacks = [
            name
            for name, ok in (
                ("an end date", dated),
                ("a time", clock.search(undated)),
                ("a time zone", zone.search(text)),
            )
            if not ok
        ]
        if x["later"] != text:
            f.add(
                {
                    "place": x["place"],
                    "text": snippet(text, 0, len(text)),
                    "what": "its text changes while watched: a countdown",
                }
            )
        if lacks:
            f.add(
                {
                    "place": x["place"],
                    "text": snippet(text, 0, len(text)),
                    "what": f"no {', no '.join(n.split(' ', 1)[1] for n in lacks)} shown",
                }
            )
    return f


# Each record's check, the keys its table lines must give, and the loads it
# reads: the page's own at both widths, right to left, or the locales.
Check = collections.namedtuple("Check", "run keys loads")
CHECKS = {
    "vault.prose-quotes": Check(prose_quotes, ("straight", "opening"), PAGE),
    "vault.code-quotes": Check(code_quotes, ("curly",), PAGE),
    "vault.prime-marks": Check(prime_marks, ("curly",), PAGE),
    "vault.math-signs": Check(math_signs, ("times", "minus"), PAGE),
    "vault.dash-glyphs": Check(dash_glyphs, ("hyphen", "em"), PAGE),
    "vault.leading-zero": Check(leading_zero, ("markers",), PAGE),
    "vault.locale-numbers": Check(locale_numbers, ("locales", "digits"), "locale"),
    "vault.week-hour": Check(week_hour, ("locales",), "locale"),
    "vault.typed-case": Check(typed_case, ("letters", "least"), PAGE),
    "vault.caps-extent": Check(caps_extent, ("lines", "words"), PAGE),
    "vault.label-case": Check(label_case, ("share",), PAGE),
    "vault.emphasis-share": Check(
        emphasis_share, ("words", "share", "run", "weight"), PAGE
    ),
    "vault.nonbreaking": Check(nonbreaking, ("joined",), PAGE),
    "vault.soft-hyphens": Check(soft_hyphens, ("words",), PAGE),
    "vault.sentence-space": Check(sentence_space, ("ends",), PAGE),
    "vault.fractions": Check(fractions, ("feature", "denominators"), PAGE),
    "vault.rtl-digit-order": Check(rtl_digit_order, ("digits",), RTL),
    "vault.offer-end-date": Check(offer_end_date, ("part", "watch"), PAGE),
}
NUMBER_KEYS = {
    "digits",
    "letters",
    "least",
    "lines",
    "words",
    "share",
    "run",
    "weight",
    "joined",
}


# --------------------------------------------------------- table and words


def parse_table(text):
    values = {}
    for n, line in rule_table.lines(text):
        fields = [x.strip() for x in line.split(SEP)]
        if len(fields) != 3 or not all(fields):
            raise TableError(f"line {n}: want ID | KEY | VALUE, got {line!r}")
        rid, key, value = fields
        if rid not in CHECKS:
            raise TableError(f"line {n}: check-text.py holds no check for {rid}")
        if key not in CHECKS[rid].keys:
            raise TableError(
                f"line {n}: {rid} reads no key {key!r}; it reads {', '.join(CHECKS[rid].keys)}"
            )
        if key in values.setdefault(rid, {}):
            raise TableError(f"line {n}: {rid} gives {key} twice")
        if key in NUMBER_KEYS:
            try:
                float(value)
            except ValueError:
                raise TableError(
                    f"line {n}: {rid} {key} wants a number, got {value!r}"
                ) from None
        if key == "watch" and not re.fullmatch(r"\d+ms", value):
            raise TableError(f"line {n}: {rid} watch wants a time in ms, got {value!r}")
        values[rid][key] = value
    if not values:
        raise TableError("the table holds no record line")
    for rid, given in values.items():
        lacking = [k for k in CHECKS[rid].keys if k not in given]
        if lacking:
            raise TableError(f"{rid} gives no {', '.join(lacking)}")
    return values


LISTS = (
    "acronyms",
    "currencies",
    "proper-nouns",
    "common-words",
    "elisions",
    "units",
    "reference-labels",
    "honorifics",
    "signs",
    "time-words",
    "clock-words",
    "meridiem",
    "time-zones",
    "count-words",
)


def parse_words(text, into=None, name="the word lists"):
    """The word lists `text` gives, appended to `into` where given: the
    caller's lists, so a project's file adds to the vault's."""
    lists = into if into is not None else {k: [] for k in LISTS}
    current = None
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.fullmatch(r"\[([\w-]+)\]", line)
        if m:
            if m[1] not in LISTS:
                raise WordsError(
                    f"{name} line {n}: no list [{m[1]}]; the lists are {', '.join(LISTS)}"
                )
            current = m[1]
        elif current is None:
            raise WordsError(f"{name} line {n}: an entry before any [list] header")
        else:
            lists[current].append(line)
    return lists


# ---------------------------------------------------------------- findings


def wanted(check, load, v, desktop):
    """Whether a check reads this load."""
    if check.loads == PAGE:
        return load.condition == PAGE
    if check.loads == RTL:
        return load.condition in (PAGE, RTL) and load.width == desktop
    return load.condition.split("=", 1)[-1] in v["locales"].split()


def findings(values, loads, words, desktop, *, unjudged=None):
    """One finding per record: fail where any load misses, else not judged
    where it could not read something, else pass where it judged anything,
    else no match. `unjudged` maps a record id to why it is not judged at
    all, such as a project's own case."""
    out = []
    for rid, v in values.items():
        check = CHECKS[rid]
        f = {"id": rid, "answer": "no match", "misses": [], "unjudged": []}
        if rid in (unjudged or {}):
            f["answer"] = "not judged"
            f["unjudged"].append({"place": "", "what": unjudged[rid]})
            out.append(f)
            continue
        judged = 0
        seen = {}
        for load in loads:
            if not wanted(check, load, v, desktop):
                continue
            got = check.run(load, v, words)
            judged += got.judged
            where = load.condition if load.condition != PAGE else f"{load.width} px"
            for m in got.misses:
                key = (m["place"], m["text"], m["what"])
                if key in seen:
                    if where not in seen[key]["under"]:
                        seen[key]["under"].append(where)
                else:
                    seen[key] = {**m, "under": [where]}
                    f["misses"].append(seen[key])
            for u in got.unjudged:
                if u not in f["unjudged"]:
                    f["unjudged"].append(u)
        f["answer"] = rule_table.answer(f["misses"], f["unjudged"], judged)
        out.append(f)
    return out
