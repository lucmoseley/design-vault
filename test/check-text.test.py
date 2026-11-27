import contextlib
import io
import json
import os
import pathlib
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-text.py"
)
SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

text = siblings.load(SCRIPTS, "check-text.py")
checks = text.checks
TABLE_FILE = text.TABLE

FIXTURES = pathlib.Path(HERE, "fixtures", "text").resolve()
FAULT = FIXTURES / "tier01-fault.html"
CLEAN = FIXTURES / "tier01-clean.html"
COUNTDOWN = FIXTURES / "countdown.html"
OFFER = ("--part", "offer-deadline=.offer")
TABLE = checks.parse_table(pathlib.Path(TABLE_FILE).read_text())
RECORDS = list(TABLE)
WORDS = checks.parse_words(pathlib.Path(text.WORDS).read_text())
RUNS = {}


def run(page, *argv, table=None, words=None, parts=None):
    key = (str(page), argv, table, words, parts)
    if key in RUNS:
        return RUNS[key]
    with tempfile.TemporaryDirectory() as out:
        extra = []
        for flag, given, name in (
            ("--table", table, "given.table"),
            ("--words", words, "given.words"),
            ("--parts", parts, "parts.json"),
        ):
            if given is not None:
                path = pathlib.Path(out, name)
                path.write_text(given)
                extra += [flag, str(path)]
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                code = text.main([str(page), "--out", out, *argv, *extra])
            except SystemExit as exc:
                code = exc.code
        report = pathlib.Path(out, "text.json")
        data = json.loads(report.read_text()) if report.exists() else None
    child.raise_if_crashed(stderr.getvalue())
    RUNS[key] = (code, stdout.getvalue(), stderr.getvalue(), data)
    return RUNS[key]


def by_id(data):
    return {f["id"]: f for f in data["findings"]}


RUN = {
    "text": "",
    "transform": "none",
    "caps": False,
    "weight": 400,
    "italic": False,
    "code": False,
    "cite": False,
    "plain": False,
    "link": False,
}


def block(body, *, tag="p", kinds=(), lang="en-US", collapse="collapse", **run_fields):
    return {
        "place": "#x",
        "tag": tag,
        "kinds": list(kinds),
        "lang": lang,
        "collapse": collapse,
        "weight": 400,
        "italic": False,
        "runs": [{**RUN, "text": body, **run_fields}],
    }


LOCALE_KEYS = ("tag", "region", "firstDay", "hourCycle", "group", "decimal")
LOCALES = {
    row[0]: dict(zip(LOCALE_KEYS, row, strict=True))
    for row in (
        ("en-US", "US", 7, "h12", ",", "."),
        ("en-GB", "GB", 1, "h23", ",", "."),
        ("en-IN", "IN", 7, "h12", ",", "."),
        ("de-DE", "DE", 1, "h23", ".", ","),
        ("en", None, 7, "h12", ",", "."),
    )
}
LOCALES["x-bad"] = None


def load(*blocks, **data):
    base = {
        "blocks": list(blocks),
        "caps": [],
        "fractions": [],
        "rtl": [],
        "calendars": [],
        "locales": LOCALES,
        "browser": LOCALES["en-US"],
    }
    base.update(data)
    return checks.Load(checks.PAGE, text.conditions.DESKTOP_WIDTH, base)


def found(check, *blocks, values=None, **data):
    rid = "vault." + check.__name__.replace("_", "-")
    return check(load(*blocks, **data), {**TABLE[rid], **(values or {})}, WORDS)


def misses(check, *blocks, **given):
    return [m["what"] for m in found(check, *blocks, **given).misses]


class FaultPage(unittest.TestCase):
    def test_314_fails_each_record_at_its_planted_element_alone(self):
        code, out, _, data = run(FAULT, *OFFER)
        self.assertEqual(code, 1, out)
        got = by_id(data)
        self.assertEqual(sorted(got), sorted(RECORDS))
        for rid in RECORDS:
            with self.subTest(rid):
                self.assertEqual(got[rid]["answer"], "fail", out)
                own = "#" + rid.removeprefix("vault.")
                for m in got[rid]["misses"]:
                    self.assertTrue(
                        m["place"] == own or m["place"].startswith(own + " "), m
                    )
                self.assertIn(f"{rid}: fail\n  - ", out)

    def test_plants_one_element_per_record(self):
        planted = set(re.findall(r'id="([\w-]+)"', FAULT.read_text()))
        self.assertEqual(planted, {r.removeprefix("vault.") for r in RECORDS})

    def test_reads_numbers_under_each_locale_and_digits_right_to_left(self):
        got = by_id(run(FAULT, *OFFER)[3])
        self.assertEqual(
            got["vault.locale-numbers"]["misses"][0]["under"],
            ["locale=en-US", "locale=de-DE"],
        )
        self.assertIn("rtl", got["vault.rtl-digit-order"]["misses"][0]["under"])


class CleanPage(unittest.TestCase):
    def test_passes_every_record_and_misreads_no_correct_text(self):
        code, out, _, data = run(CLEAN, *OFFER)
        self.assertEqual(code, 0, out)
        self.assertEqual(data["answers"], dict.fromkeys(RECORDS, "pass"))
        self.assertTrue(out.startswith("check-text: file://"), out)


class Arguments(unittest.TestCase):
    def test_reads_each_limit_from_the_table(self):
        given = pathlib.Path(TABLE_FILE).read_text()
        for old, new in (
            ("vault.caps-extent | words | 4", "vault.caps-extent | words | 20"),
            ("vault.caps-extent | lines | 1", "vault.caps-extent | lines | 3"),
            ("vault.emphasis-share | run | 10", "vault.emphasis-share | run | 30"),
            (
                "vault.emphasis-share | share | 0.25",
                "vault.emphasis-share | share | 0.9",
            ),
        ):
            given = given.replace(old, new)
        got = by_id(run(FAULT, *OFFER, table=given)[3])
        self.assertEqual(got["vault.caps-extent"]["answer"], "pass")
        self.assertEqual(got["vault.emphasis-share"]["answer"], "pass")

    def test_a_project_word_list_names_words_that_are_not_title_case(self):
        names = "[proper-nouns]\nMore\nAbout\nOur\nRooms\n"
        got = by_id(run(FAULT, *OFFER, words=names)[3])
        self.assertEqual(got["vault.label-case"]["answer"], "pass")

    def test_own_case_leaves_label_case_not_judged(self):
        got = by_id(run(FAULT, *OFFER, "--own-case")[3])
        self.assertEqual(got["vault.label-case"]["answer"], "not judged")

    def test_an_undeclared_offer_part_has_no_match_and_a_null_one_is_not_judged(self):
        self.assertEqual(
            by_id(run(FAULT)[3])["vault.offer-end-date"]["answer"], "no match"
        )
        null = json.dumps({"declared": {"offer-deadline": None}})
        self.assertEqual(
            by_id(run(FAULT, parts=null)[3])["vault.offer-end-date"]["answer"],
            "not judged",
        )

    def test_a_ticking_deadline_fails_as_a_countdown(self):
        got = by_id(run(COUNTDOWN, *OFFER)[3])["vault.offer-end-date"]
        self.assertEqual(
            [m["what"] for m in got["misses"]],
            ["its text changes while watched: a countdown"],
        )

    def test_a_table_without_two_records_still_runs(self):
        given = "\n".join(
            line
            for line in pathlib.Path(TABLE_FILE).read_text().splitlines()
            if not line.startswith(("vault.fractions", "vault.rtl-digit-order"))
        )
        code, out, _, data = run(FAULT, *OFFER, table=given)
        self.assertEqual(code, 1, out)
        self.assertNotIn("vault.fractions", by_id(data))

    def test_refuses_a_wrong_table_before_any_load(self):
        good = pathlib.Path(TABLE_FILE).read_text()
        for name, given, said in (
            (
                "unknown record",
                good + "vault.nope | x | 1\n",
                "holds no check for vault.nope",
            ),
            (
                "unknown key",
                good + "vault.dash-glyphs | nope | 1\n",
                "reads no key 'nope'",
            ),
            ("repeated key", good + "vault.dash-glyphs | em | —\n", "gives em twice"),
            (
                "not a number",
                good.replace("| words | 4", "| words | four"),
                "wants a number",
            ),
            (
                "missing key",
                good.replace("vault.dash-glyphs | em | —\n", ""),
                "vault.dash-glyphs gives no em",
            ),
            ("bad watch", good.replace("2000ms", "2s"), "wants a time in ms"),
        ):
            with self.subTest(name):
                code, _, err, data = run(FAULT, table=given)
                self.assertEqual(code, 2)
                self.assertIn(said, err)
                self.assertIsNone(data)

    def test_refuses_an_unknown_word_list(self):
        code, _, err, _ = run(FAULT, words="[nope]\nx\n")
        self.assertEqual(code, 2)
        self.assertIn("no list [nope]", err)


class Checks(unittest.TestCase):
    def test_quotes_fail_straight_and_misopened_marks_and_pass_measures(self):
        self.assertEqual(len(misses(checks.prose_quotes, block("the ‘70s and ‘em"))), 2)
        self.assertEqual(misses(checks.prose_quotes, block("‘Emma’ is 5' tall")), [])
        self.assertEqual(len(misses(checks.prose_quotes, block("2026's list"))), 1)
        self.assertEqual(misses(checks.prime_marks, block("“Top 10” rooms")), [])
        self.assertEqual(misses(checks.prime_marks, block("2026’s best list")), [])
        self.assertEqual(len(misses(checks.prime_marks, block("a 6” shelf"))), 1)
        self.assertEqual(misses(checks.code_quotes, block("say “hi”")), [])

    def test_math_signs_fail_a_hyphen_for_minus_and_pass_hex(self):
        self.assertEqual(misses(checks.math_signs, block("colour 0x1F and −5 °C")), [])
        self.assertEqual(len(misses(checks.math_signs, block("it is -5 °C"))), 1)
        self.assertEqual(len(misses(checks.math_signs, block("take 5 - 3 = 2"))), 1)

    def test_dash_glyphs_fail_hyphen_ranges_and_pass_dates_and_phones(self):
        for body in ("from 1880-1912", "season 2025-26", "open 9am-5pm", "$10-$20"):
            with self.subTest(body):
                self.assertEqual(
                    misses(checks.dash_glyphs, block(body)),
                    ["a hyphen in a range, which takes –"],
                )
        for body in ("on 2026-11-15", "call 555-1234", "take 5 - 3 = 2"):
            with self.subTest(body):
                self.assertEqual(misses(checks.dash_glyphs, block(body)), [])
        self.assertEqual(
            misses(checks.dash_glyphs, block("call 555-12", plain=True)), []
        )

    def test_dash_glyphs_fail_odd_em_spacing_between_words_only(self):
        mixed = found(checks.dash_glyphs, block("a — b — c"), block("d—e"))
        self.assertEqual([m["text"] for m in mixed.misses], ["d—e"])
        alone = (block("a—b"), block("— Jane, a guest"), block(" — "))
        self.assertEqual(misses(checks.dash_glyphs, *alone), [])

    def test_leading_zero_fails_a_bare_decimal_and_passes_a_file_name(self):
        self.assertEqual(misses(checks.leading_zero, block("see file.js")), [])
        self.assertEqual(len(misses(checks.leading_zero, block("rate (.5)"))), 1)

    def test_each_emphasis_and_no_break_limit_fails_alone(self):
        bold, plain = {**RUN, "weight": 700}, RUN

        def paragraph(*counts, link=False):
            b = block("")
            b["runs"] = [
                {**(plain if i % 2 else bold), "text": "word " * n, "link": link}
                for i, n in enumerate(counts)
            ]
            return misses(checks.emphasis_share, b)

        self.assertEqual(
            paragraph(11, 37), ["a run of 11 words in bold or italic, past 10"]
        )
        self.assertEqual(
            paragraph(4, 10, 4, 10, 4, 8),
            ["12 of 40 words in bold or italic, past 25%"],
        )
        self.assertEqual(paragraph(11, 37, link=True), [])
        self.assertEqual(
            misses(checks.nonbreaking, block("a\u00a0b\u00a0c\u00a0d\u00a0e")), []
        )

    def test_locale_numbers_fail_a_foreign_marker_or_grouping(self):
        de = block("Preis 1,234.50", lang="de-DE")
        self.assertEqual(
            misses(checks.locale_numbers, de, formatted={("de-DE", "1234"): "1.234"}),
            ["decimal marker '.', where de-DE writes ','"],
        )
        india = block("pay 123,456 now", lang="en-IN")
        self.assertEqual(
            len(
                misses(
                    checks.locale_numbers,
                    india,
                    formatted={("en-IN", "123456"): "1,23,456"},
                )
            ),
            1,
        )
        for body in ("um 10.30 Uhr", "on 15.11.2026"):
            with self.subTest(body):
                got = misses(checks.locale_numbers, block(body, lang="de-DE"))
                self.assertEqual(got, [])
        us = block("pay 1,234", lang="en-US")
        self.assertEqual(
            misses(checks.locale_numbers, us, formatted={("en-US", "1234"): "1,234"}),
            [],
        )

    def test_a_lang_tag_the_browser_cannot_read_is_not_judged(self):
        for check in (checks.locale_numbers, checks.week_hour):
            with self.subTest(check.__name__):
                got = found(check, block("pay 1,234 at 13:00", lang="x-bad"))
                self.assertEqual(
                    (got.misses, got.unjudged),
                    ([], [{"place": "", "what": "lang 'x-bad' is no locale tag"}]),
                )

    def test_week_hour_fails_the_other_cycle_and_takes_the_visitors(self):
        self.assertEqual(len(misses(checks.week_hour, block("opens 13:00"))), 1)
        self.assertEqual(
            len(
                misses(
                    checks.week_hour,
                    block("opens 3 pm", lang="en-GB"),
                    browser=LOCALES["de-DE"],
                )
            ),
            1,
        )
        self.assertEqual(misses(checks.week_hour, block("opens 9:30")), [])
        self.assertEqual(misses(checks.week_hour, block("the tour (14:32)")), [])
        visitor = found(
            checks.week_hour, block("opens 13:00"), browser=LOCALES["de-DE"]
        )
        self.assertEqual(visitor.misses, [])
        calendar = [{"place": "#c", "lang": "en-GB", "first": 7}]
        de, us = LOCALES["de-DE"], LOCALES["en-US"]
        self.assertEqual(
            len(misses(checks.week_hour, calendars=calendar, browser=de)), 1
        )
        self.assertEqual(misses(checks.week_hour, calendars=calendar, browser=us), [])

    def test_week_hour_leaves_a_regionless_or_unknown_locale_not_judged(self):
        got = found(checks.week_hour, block("from 14:00", lang="en"))
        self.assertEqual((got.misses, len(got.unjudged)), ([], 1))
        unknown = {**LOCALES, "xx": {**LOCALES["en-US"], "firstDay": None}}
        got = found(
            checks.week_hour,
            calendars=[{"place": "#c", "lang": "xx", "first": 7}],
            locales=unknown,
            browser=None,
        )
        self.assertEqual((got.misses, len(got.unjudged)), ([], 1))

    def test_typed_case_fails_typed_capitals_and_passes_acronyms_and_lists(self):
        for body in (
            "prices in USD EUR",
            "ends 17:00 EST EDT",
            "the BAR, POOL and gym",
            "rooms A B and C",
            "the UNESCO site, FAQ",
            "we take EUR, USD and GBP",
            "11:59 PM EST",
        ):
            with self.subTest(body):
                self.assertEqual(misses(checks.typed_case, block(body)), [])
        self.assertEqual(len(misses(checks.typed_case, block("WELCOME home"))), 1)
        self.assertEqual(len(misses(checks.typed_case, block("BOOK NOW"))), 1)
        label = block("Open the BOOKING FORM")
        label["attr"] = "aria-label"
        self.assertEqual(misses(checks.typed_case, label), [])

    def test_label_case_fails_title_case_and_a_lower_first_letter(self):
        for body in (
            "Book Now",
            "Learn More",
            "Terms And Conditions",
            "Read More About Our Rooms",
        ):
            with self.subTest(body):
                self.assertEqual(
                    len(misses(checks.label_case, block(body, kinds=["link"]))), 1
                )
        self.assertEqual(
            misses(checks.label_case, block("book a bed", kinds=["button"])),
            ["starts in lower case, where sentence case starts with a capital"],
        )
        styled = block(
            "our shared dorm rooms", kinds=["heading"], transform="capitalize"
        )
        self.assertEqual(len(misses(checks.label_case, styled)), 1)

    def test_label_case_passes_names_digits_addresses_and_inner_capitals(self):
        for body in (
            "Hostels in Lisbon and Porto",
            "24-hour reception",
            "iPhone app",
            "hello@example.com",
            "Our rooms in May",
        ):
            with self.subTest(body):
                self.assertEqual(
                    misses(checks.label_case, block(body, kinds=["list-item"])), []
                )
        self.assertEqual(misses(checks.label_case, block("see our terms")), [])

    def test_label_case_reads_a_word_the_page_writes_in_lower_case_as_common(self):
        heading = block("Shared Rooms", kinds=["heading"])
        self.assertEqual(misses(checks.label_case, heading), [])
        prose_ = block("our rooms are shared")
        self.assertEqual(len(misses(checks.label_case, heading, prose_)), 1)

    def test_nonbreaking_fails_a_broken_group_and_passes_a_trailing_mark(self):
        for body in ("see Fig. 2", "ask Ms. Marvel", "© 2026 the hostel"):
            with self.subTest(body):
                self.assertEqual(len(misses(checks.nonbreaking, block(body))), 1)
        for body in ("Acme® offers coffee", "12 Oxford St. Open daily"):
            with self.subTest(body):
                self.assertEqual(misses(checks.nonbreaking, block(body)), [])
        joined = block("a\u00a0b\u00a0c\u00a0d\u00a0e\u00a0f")
        self.assertEqual(len(misses(checks.nonbreaking, joined)), 1)

    def test_sentence_space_fails_a_kept_double_space_only(self):
        self.assertEqual(
            misses(checks.sentence_space, block("see Fig.\u00a0A for it")), []
        )
        kept = block("End.  Next one.", collapse="preserve")
        self.assertEqual(len(misses(checks.sentence_space, kept)), 1)
        self.assertEqual(misses(checks.sentence_space, block("End.  Next one.")), [])

    def test_fractions_fail_each_unset_fraction_and_pass_counts_and_ratings(self):
        def one(text_="1/2", before="", **x):
            return misses(
                checks.fractions,
                fractions=[
                    {
                        "place": "#f",
                        "text": text_,
                        "before": before,
                        "numeric": "diagonal-fractions",
                        "alone": True,
                        "drawsFeature": True,
                        **x,
                    }
                ],
            )

        self.assertEqual(one(), [])
        self.assertEqual(len(one(alone=False)), 1)
        self.assertEqual(len(one(drawsFeature=False)), 1)
        self.assertEqual(len(one(numeric="normal")), 1)
        for fraction, before in (
            ("9/10", "Rated "),
            ("1/5", "Slide "),
            ("8/31", ""),
            ("10/12", "size "),
        ):
            with self.subTest(fraction):
                self.assertEqual(one(fraction, before, numeric="normal"), [])

    def test_offer_end_date_wants_a_date_a_time_and_a_zone(self):
        def lacks(body):
            got = found(
                checks.offer_end_date,
                offer=[
                    {"place": "#o", "text": body, "later": body, "months": ["November"]}
                ],
            )
            return [m["what"] for m in got.misses]

        for body in (
            "Ends 30 November 2026 at 11:59 pm CST",
            "Ends at midnight GMT on 30 November 2026",
            "Ends 30 November 2026, 23:59 Europe/Lisbon",
        ):
            with self.subTest(body):
                self.assertEqual(lacks(body), [])
        self.assertEqual(lacks("Ends 30.11.2026 CET"), ["no time shown"])
        self.assertEqual(
            lacks("Save €12.50 until 30 November 2026 GMT"), ["no time shown"]
        )


if __name__ == "__main__":
    child.main(verbosity=2)
