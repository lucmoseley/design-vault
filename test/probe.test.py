"""Pins probe.py (#300): python3 test/probe.test.py

It is a suite of the commit gate (test/all.sh): loosening it lets a family
script's rule pass a page that misses it, or fail one that meets it. The rule
table runs on test/fixtures/probe/runner.html, whose every planted miss sits
beside a twin that meets the rule, and must name exactly those misses.
"""

import contextlib
import json
import os
import pathlib
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "probe.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "probe")
RUNNER = os.path.join(FIXTURES, "runner.html")
TABLE = os.path.join(FIXTURES, "runner.table")
CASCADE = pathlib.Path(FIXTURES, "cascade.html").resolve().as_uri()
CONDITIONS = (
    pathlib.Path(HERE, "fixtures", "drivers", "conditions.html").resolve().as_uri()
)
# Five widths, two of them in the phone band and one at the stepped top.
SWEEP = ["--widths", "320-1920", "--step", "400"]


SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

probe = siblings.load(SCRIPTS, "probe.py")
flow = siblings.load(SCRIPTS, "check-flow.py")
layout = siblings.load(SCRIPTS, "check-layout.py")
STACK = contextlib.ExitStack()
BROWSER = None


def setUpModule():
    global BROWSER
    BROWSER = STACK.enter_context(flow.chromium())


def tearDownModule():
    STACK.close()


# A guess at a ceiling no run on these fixtures nears.
RUN_TIMEOUT_S = 120


def run(*args):
    return child.run([sys.executable, SCRIPT, *args], timeout=RUN_TIMEOUT_S)


def declaring(out):
    """A run of the program on runner.html into `out`, given the parts
    declaration `text` as --parts (None gives none) before `args`."""

    def run_at(text, *args):
        given = []
        if text is not None:
            path = os.path.join(out, "parts-declared.json")
            pathlib.Path(path).write_text(text, encoding="utf8")
            given = ["--parts", path]
        return run(RUNNER, "--table", TABLE, "--out", out, *given, *args, *SWEEP)

    return run_at


def values(url, table, parts=None):
    """{subject: (value, verdict)} for each line, read once on `url`, its
    part: lines through `parts`, a name-to-selector map (None declares none)."""
    page = BROWSER.new_page()
    try:
        page.goto(url)
        page.evaluate(layout.SETTLE_JS)
        return [
            {s.subject: (s.value, s.verdict) for s in r.subjects}
            for r in probe.read(page, probe.parse(table), parts)
        ]
    finally:
        page.close()


class OneCopy(unittest.TestCase):
    def test_probe_and_this_suite_share_one_check_flow_and_check_layout(self):  # #562
        self.assertIs(probe.flow, flow)
        self.assertIs(probe.layout, layout)
        self.assertIs(layout.flow, flow)


class TheTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = tempfile.mkdtemp()
        cls.addClassCleanup(shutil.rmtree, cls.out)
        cls.r = run(
            RUNNER, "--table", TABLE, "--out", cls.out, "--part", "hero=.hero", *SWEEP
        )
        with open(os.path.join(cls.out, "probe.json"), encoding="utf8") as fh:
            cls.got = json.load(fh)

    def test_names_exactly_the_planted_misses(self):
        misses = {
            (f["id"], m["subject"], m["value"], m["from"], m["to"])
            for f in self.got["findings"]
            for m in f["misses"]
        }
        self.assertEqual(
            misses,
            {
                ("T-SIZE", "p#fine", "14px", 320, 720),
                ("T-SIZE", "p#gappy", "14px", 320, 320),
                ("T-SIZE", "p#gappy", "14px", 1520, 1920),
                ("T-CAPS", "span#tight", "normal", 320, 1920),
                ("T-CAPS", "span#edge", "0.5px", 320, 1920),
                ("T-NAV", "css:nav a", 5, 720, 1920),
                ("T-PWD", "input#saved-pwd", "hunter2", 320, 1920),
                ("T-ROLE", "div#chip", "16px", 320, 1920),
                ("T-FONT", "Blocking normal normal", "block", 320, 1920),
                ("T-XH", "p#xh-low", 0.3, 320, 1920),
                ("T-SHADOW", "css:.card", 3, 320, 1920),
                ("T-INK", "p#loud", 0.2026, 320, 1920),
                ("T-AUTH", "p#raw", "12px", 320, 1920),
                ("T-PART", "h1#hero", "400", 320, 1920),
            },
        )

    def test_answers_one_finding_per_record_id(self):
        self.assertEqual(
            self.got["answers"],
            {
                **{
                    i: "fail"
                    for i in (
                        "T-SIZE",
                        "T-CAPS",
                        "T-NAV",
                        "T-PWD",
                        "T-ROLE",
                        "T-FONT",
                        "T-XH",
                        "T-SHADOW",
                        "T-INK",
                        "T-AUTH",
                        "T-PART",
                    )
                },
                "T-META": "pass",
                "T-VAR": "pass",
                "T-NONE": "no match",
            },
        )
        self.assertFalse(any(f["unjudged"] for f in self.got["findings"]))

    def test_exits_1_and_prints_each_miss_with_its_widths(self):
        self.assertEqual(self.r.returncode, 1, self.r.stderr)
        self.assertIn(
            "T-SIZE: fail\n  miss, 320–720 px: p#fine style:font-size 14px: not >= 16px (at 320 px)",
            self.r.stdout,
        )
        self.assertIn("T-NONE: no match", self.r.stdout)
        self.assertIn("NOT A GATING SWEEP", self.r.stdout)
        self.assertEqual(
            [w["width"] for w in self.got["widths"]], [320, 720, 1120, 1520, 1920]
        )
        self.assertFalse(self.got["gating"])

    def test_a_table_the_page_meets_exits_0(self):
        with tempfile.TemporaryDirectory() as out:
            table = os.path.join(out, "pass.table")
            with open(table, "w", encoding="utf8") as fh:
                fh.write("T-VAR | css:.gap | style:margin-top | = 12px\n")
            r = run(RUNNER, "--table", table, "--out", out, *SWEEP)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("T-VAR: pass", r.stdout)


class Reads(unittest.TestCase):
    def test_a_var_reads_resolved_and_authored_reads_the_sheet(self):
        style, authored = values(
            CASCADE,
            "A | css:#inline-wins, #var-short | style:margin-top | = 0px\n"
            "B | css:#inline-wins, #var-short | authored:margin-top | = x\n",
        )
        self.assertEqual(style["p#inline-wins"][0], "20px")
        self.assertEqual(style["p#var-short"][0], "12px")
        self.assertEqual(authored["p#var-short"][0], "var(--gap) 0")

    def test_authored_takes_the_declaration_the_cascade_picks(self):
        got = values(
            CASCADE,
            "A | css:#layered, #imp, #inherits | authored:color | = x\n"
            "B | css:#spec, #plain-short | authored:padding-top | = x\n"
            "C | css:#inline-wins, #important, #ua | authored:margin-top | = x\n"
            "D | css:#plain-short | authored:padding-left | = x\n"
            "E | css:#ua | authored:display | = x\n",
        )
        self.assertEqual(
            [{k: v[0] for k, v in line.items()} for line in got],
            [
                {
                    "p#layered": "rgb(1, 2, 3)",
                    "p#imp": "rgb(9, 9, 9)",
                    "p#inherits": "",
                },
                {"p#spec": "8px", "p#plain-short": "4px"},
                {"p#inline-wins": "20px", "p#important": "var(--gap)", "p#ua": ""},
                {"p#plain-short": "8px"},
                {"p#ua": ""},
            ],
        )

    def test_an_authored_read_leaves_the_page_as_it_found_it(self):
        page = BROWSER.new_page()
        try:
            page.goto(CASCADE)
            probe.read(page, probe.parse("A | css:p | authored:color | = x"))
            self.assertFalse(page.evaluate(f"'{probe.STASH}' in window"))
        finally:
            page.close()

    def test_a_value_it_cannot_compare_is_not_judged(self):
        (got,) = values(CASCADE, "A | css:#var-short | style:margin | >= 4px\n")
        self.assertEqual(got["p#var-short"], ("12px 0px", "unjudged"))
        (units,) = values(CASCADE, "A | css:#ua | style:margin-top | >= 4ms\n")
        self.assertEqual(units["p#ua"][1], "unjudged")
        (colour,) = values(CASCADE, "A | css:#ua | style:margin-top as alpha | <= 1\n")
        self.assertEqual(colour["p#ua"][1], "unjudged")

    def test_prev_and_next_read_the_element_siblings_either_side(self):
        page = (
            "data:text/html,<body><div style='border:1px solid'>a</div>"
            "<hr id=between><div>b</div><hr id=last></body>"
        )
        before, after = values(
            page,
            "A | css:hr | prev style:border-bottom-width | = 1px\n"
            "B | css:hr | next style:border-top-width | = 0px\n",
        )
        self.assertEqual(before["hr#between"], ("1px", "pass"))
        self.assertEqual(before["hr#last"], ("0px", "miss"))
        self.assertEqual(after["hr#between"], ("0px", "pass"))
        self.assertEqual(after["hr#last"][0], None)

    def test_on_sets_a_rule_colour_on_its_box_over_black_and_white(self):
        page = (
            "data:text/html,<style>"
            "video::cue { color: %23fff; background-color: rgba(0, 0, 0, 0.8) }"
            "video.dim::cue { color: yellow; background-color: rgba(0, 0, 0, 0.3) }"
            "video.token::cue { color: var(--caption); background-color: %23000 }"
            "p { color: %23fff }</style><video></video>"
        )
        on, light = values(
            page,
            "A | sheet where selector matches ::cue | decl:color on decl:background-color | >= 4.5\n"
            "B | sheet where selector matches ::cue | decl:color as luminance | >= 0.9\n",
        )
        self.assertEqual(on["video::cue"], (12.6347, "pass"))
        self.assertEqual(on["video.dim::cue"][1], "miss")
        self.assertNotIn("p", on)
        self.assertEqual(on["video.token::cue"][1], "unjudged")
        self.assertEqual(light["video::cue"], (1.0, "pass"))
        self.assertEqual(light["video.dim::cue"][1], "pass")

    def test_each_comparison_passes_or_misses_by_its_bound(self):
        (got,) = values(
            CASCADE,
            "A | css:#ua | style:margin-top | between 15px and 1em\n",
        )
        self.assertEqual(got["p#ua"], ("16px", "pass"))
        cases = {
            "<= 15px": "miss",
            "< 16px": "miss",
            "> 15.5px": "pass",
            "!= 16px": "miss",
            "between 1rem and 2rem": "pass",
            "in 16px or 2px": "pass",
            "not in 16px or 2px": "miss",
            "matches ^1\\dpx$": "pass",
            "present": "pass",
        }
        table = "".join(
            f"{n} | css:#ua | style:margin-top | {m}\n" for n, m in enumerate(cases)
        )
        got = values(CASCADE, table)
        self.assertEqual([line["p#ua"][1] for line in got], list(cases.values()))
        one, unset = values(
            CASCADE,
            "N | css:#ua | count | != 1\nU | css:#ua | attr:title | = x\n",
        )
        self.assertEqual(one["css:#ua"], (1, "miss"))
        self.assertEqual(unset["p#ua"], (None, "miss"))

    def test_a_face_descriptor_and_a_numeric_attribute(self):
        size, level, low = values(
            CASCADE,
            "A | fonts | face:size-adjust | = 90%\n"
            "B | css:#ua | attr:tabindex | >= 2\n"
            "C | css:#ua | attr:tabindex | <= 2\n",
        )
        self.assertEqual(size["Adjusted normal normal"], ("90%", "pass"))
        self.assertEqual(level["p#ua"], ("3", "pass"))
        self.assertEqual(low["p#ua"], ("3", "miss"))

    def test_a_part_reads_through_the_selector_declared_for_it(self):
        (got,) = values(
            CASCADE,
            "A | part:lead | style:margin-top | = 20px",
            {"lead": "#inline-wins"},
        )
        self.assertEqual(got, {"p#inline-wins": ("20px", "pass")})
        with self.assertRaisesRegex(probe.ProbeError, "no part named 'lead'"):
            values(CASCADE, "A | part:lead | style:margin-top | = 20px")
        with self.assertRaisesRegex(probe.ProbeError, "not a selector"):
            values(CASCADE, "A | css:p[ | style:margin-top | = 20px")


class Sweep(unittest.TestCase):
    def test_conditions_reach_the_page_and_phone_widths_touch(self):
        rules = probe.parse(
            "BG | css:body | style:background-color | = rgb(17, 17, 17)\n"
            "TOUCH | css:#target | style:height | = 44px\n"
        )
        dark, _ = probe.sweep(
            BROWSER, CONDITIONS, rules, widths=[320, 1024], scheme="dark"
        )
        light, _ = probe.sweep(BROWSER, CONDITIONS, rules, widths=[320], scheme="light")

        def verdict(swept, i):
            return [r.subjects[0].verdict for r in swept[i][1]]

        self.assertEqual(verdict(dark, 0), ["pass", "pass"])
        self.assertEqual(verdict(dark, 1), ["pass", "miss"])
        self.assertEqual(verdict(light, 0), ["miss", "pass"])

    def test_it_reads_once_entrance_animations_finish(self):
        rules = probe.parse("GROW | css:#grow | style:font-size | = 20px")
        swept, _ = probe.sweep(BROWSER, CASCADE, rules, widths=[1024])
        self.assertEqual(swept[0][1][0].subjects[0].value, "20px")


class Findings(unittest.TestCase):
    def test_a_miss_outranks_a_value_not_judged_in_the_finding(self):
        rules = probe.parse(
            "U | css:#var-short | style:margin | >= 4px\n"
            "F | css:#var-short | style:margin | >= 4px\n"
            "F | css:#ua | style:margin-top | >= 20px\n"
            "P | css:#ua | style:margin-top | >= 4px\n"
        )
        swept, _ = probe.sweep(BROWSER, CASCADE, rules, widths=[1024])
        found = probe.findings(rules, swept)
        self.assertEqual(
            [
                (f["id"], f["answer"], len(f["misses"]), len(f["unjudged"]))
                for f in found
            ],
            [("U", "not judged", 0, 1), ("F", "fail", 1, 1), ("P", "pass", 0, 0)],
        )


class Refusals(unittest.TestCase):
    def test_a_bad_table_line_names_its_line(self):
        for line, why in (
            ("A | css:p | style:color", "ID \\| SELECTS"),
            ("A | css:p | style:color | = red | blue", "ID \\| SELECTS"),
            ("A | xpath://p | style:color | = red", "SELECTS wants"),
            ("A | all fonts | face:display | = swap", "drop all"),
            ("A | css:p | face:display | = swap", "face: reads go with fonts"),
            ("A | fonts | style:color | = red", "face: reads go with fonts"),
            ("A | role:Button! | count | = 1", "not an ARIA role"),
            ("A | css:p | colour:x | = red", "READS wants"),
            ("A | css:p | distinct count | = 1", "distinct wants"),
            (
                "A | css:p | attr:href as alpha | = 1",
                "only style, ground, backdrop, decl take as",
            ),
            (
                "A | css:p | style:color on style:background-color | > 1",
                "on sets one decl",
            ),
            ("A | css:p | selector | = p", "read the sheet's rules"),
            ("A | css:p | style:color | ~ red", "MUST wants"),
            ("A | css:p | style:width | >= wide", "not a number"),
            ("A | css:p | authored:width | >= 4px", "compares numbers"),
            ("A | css:p | style:color | matches (", "not a regular expression"),
        ):
            with (
                self.subTest(line=line),
                self.assertRaisesRegex(probe.TableError, "line 2: .*" + why),
            ):
                probe.parse("# a comment\n" + line)
        with self.assertRaisesRegex(probe.TableError, "no rule"):
            probe.parse("# only a comment\n")

    def test_the_program_exits_2_on_a_bad_table_or_an_undeclared_part(self):
        with tempfile.TemporaryDirectory() as out:
            bad = os.path.join(out, "bad.table")
            with open(bad, "w", encoding="utf8") as fh:
                fh.write("A | css:p | style:color\n")
            r = run(RUNNER, "--table", bad, "--out", out, *SWEEP)
            self.assertEqual(r.returncode, 2)
            self.assertIn("line 1", r.stderr)
            stale = os.path.join(out, "probe.json")
            pathlib.Path(stale).write_text("{}", encoding="utf8")
            r = run(RUNNER, "--table", TABLE, "--out", out, *SWEEP)
            self.assertEqual(r.returncode, 2)
            self.assertFalse(
                os.path.exists(stale), "an earlier run's values outlive a failed one"
            )
            self.assertIn("no part named 'hero'", r.stderr)
            r = run(RUNNER, "--table", TABLE, "--out", out, "--part", "hero", *SWEEP)
            self.assertEqual(r.returncode, 2)
            self.assertIn("--part wants NAME=SELECTOR", r.stderr)

    def test_the_parts_declaration_maps_part_lines_and_part_overrides_it(self):
        with tempfile.TemporaryDirectory() as out:
            run_at = declaring(out)

            def t_part(*args):
                r = run_at(*args)
                self.assertIn(r.returncode, (0, 1), r.stderr)
                with open(os.path.join(out, "probe.json"), encoding="utf8") as fh:
                    return r.returncode, json.load(fh)["answers"]["T-PART"]

            hero = '{"declared": {"hero": ".hero", "form": null}}'
            self.assertEqual(t_part(hero), t_part(None, "--part", "hero=.hero"))
            self.assertEqual(t_part(hero)[1], "fail")
            self.assertEqual(t_part(hero, "--part", "hero=.nothing")[1], "no match")
            unselected = '{"declared": {"hero": null}}'
            self.assertEqual(
                t_part(unselected, "--part", "hero=.nothing")[1], "no match"
            )

    def test_it_refuses_a_parts_declaration_it_cannot_use_naming_the_way_out(
        self,
    ):
        form = '{"declared": {<part>: <its CSS selector, or null>}}'
        with tempfile.TemporaryDirectory() as out:
            run_at = declaring(out)
            r = run_at('{"declared": {"hero": null}}')
            self.assertEqual(r.returncode, 2)
            self.assertIn("declares hero with no selector", r.stderr)
            self.assertIn("give one with --part", r.stderr)
            for text, why in (
                ("{", "is not JSON"),
                ('{"parts": []}', 'has no "declared" object'),
                ('{"declared": {"hero": ""}}', "declares hero with neither"),
            ):
                r = run_at(text)
                self.assertEqual(r.returncode, 2, text)
                self.assertIn(why, r.stderr)
                self.assertIn(form, r.stderr)


class Grammar(unittest.TestCase):
    """The table grammar check-style.table runs on (#309), judged on rows
    built by hand, as the browser hands them back."""

    def judge(self, line, got, refs=None):
        """The verdict and value `line` makes of one element whose reads,
        in probe.wanted()'s order, gave `got`; None where a where filter
        drops it."""
        rule = probe.parse(line)[0]
        self.assertEqual(len(got), len(probe.wanted(rule)))
        row = {
            "subject": "x",
            "uid": 1,
            "groups": [],
            "fontSize": 16,
            "rootSize": 16,
            "values": got,
        }
        found = probe.judged(rule, [row], refs)
        return (found[0].verdict, found[0].value) if found else None

    def test_where_filters_take_the_shortest_read_that_leaves_a_must(self):
        rule = probe.parse(
            "A | css:p where style:font-size < 16px where lines >= 2 | text | present"
        )[0]
        self.assertEqual(
            [(r.text, m.text) for r, m in rule.select.where],
            [("style:font-size", "< 16px"), ("lines", ">= 2")],
        )

    def test_a_where_filter_drops_the_elements_it_does_not_hold_for(self):
        line = "A | css:p where style:font-size < 16px | style:color | = rgb(0, 0, 0)"
        black = {"value": "rgb(0, 0, 0)"}
        self.assertEqual(
            self.judge(line, [black, {"value": "14px"}]), ("pass", "rgb(0, 0, 0)")
        )
        self.assertIsNone(self.judge(line, [black, {"value": "16px"}]))

    def test_two_reads_combine(self):
        size, height = {"value": "16px"}, {"value": "24px"}
        self.assertEqual(
            self.judge(
                "A | css:p | style:line-height per style:font-size | between 1.4 and 1.6",
                [height, size],
            ),
            ("pass", 1.5),
        )
        self.assertEqual(
            self.judge(
                "A | css:p | style:font-size times xheight | >= 8.32px",
                [size, {"value": 0.52}],
            ),
            ("pass", "8.32px"),
        )
        self.assertEqual(
            self.judge(
                "A | css:b | style:font-weight minus parent style:font-weight | >= 300",
                [{"value": "700"}, {"value": "600"}],
            ),
            ("miss", 100.0),
        )
        self.assertEqual(
            self.judge(
                "A | css:p | style:font-size per style:width | > 0",
                [size, {"value": "50%"}],
            )[0],
            "unjudged",
        )

    def test_equal_compares_quantities_as_numbers_and_normal_spacing_is_zero(self):
        self.assertEqual(
            self.judge(
                "A | css:p | style:letter-spacing | = 0px", [{"value": "normal"}]
            )[0],
            "pass",
        )
        self.assertEqual(
            self.judge(
                "A | css:p | style:letter-spacing | = 0px", [{"value": "0.32px"}]
            )[0],
            "miss",
        )
        self.assertEqual(
            self.judge(
                "A | css:p | style:color | = rgb(0, 0, 0)", [{"value": "rgb(0,  0, 0)"}]
            )[0],
            "pass",
        )

    def test_multiple_of_a_step(self):
        self.assertEqual(
            self.judge(
                "A | css:p | style:padding-top | multiple of 4px", [{"value": "12px"}]
            )[0],
            "pass",
        )
        self.assertEqual(
            self.judge(
                "A | css:p | style:padding-top | multiple of 4px", [{"value": "10px"}]
            )[0],
            "miss",
        )

    def test_within_a_share_of_another_read(self):
        line = "A | css:code | style:font-size | within 3% of parent style:font-size"
        self.assertEqual(
            self.judge(line, [{"value": "15.6px"}, {"value": "16px"}])[0], "pass"
        )
        self.assertEqual(
            self.judge(line, [{"value": "15px"}, {"value": "16px"}])[0], "miss"
        )

    def test_a_scope_word_alone_is_a_value_not_a_read(self):
        """check-dom.table's vault.enter-key MUST `= next` is a value (#520)."""
        must = probe.parse("A | css:input | attr:enterkeyhint | = next")[0].must
        self.assertEqual((must.values, must.ref), (("next",), None))
        must = probe.parse("A | css:p | style:color | = next style:color")[0].must
        self.assertEqual(must.ref.read.scope, "next")

    def test_all_of_holds_against_every_other_element(self):
        line = "A | part:cta | height | > all of (role:button) height"
        others = [(1, "53px", {}), (2, "45px", {})]
        self.assertEqual(self.judge(line, [{"value": "53px"}], others)[0], "pass")
        self.assertEqual(
            self.judge(line, [{"value": "53px"}], [*others, (3, "53px", {})])[0], "miss"
        )

    def test_not_matches_and_a_lens(self):
        self.assertEqual(
            self.judge(
                "A | css:p | style:font-family | not matches (?i)mono",
                [{"value": '"DejaVu Sans Mono"'}],
            )[0],
            "miss",
        )
        white = {"value": "rgb(255, 255, 255)", "rgba": [255, 255, 255, 255]}
        self.assertEqual(
            self.judge("A | css:p | ground as luminance | >= 0.1791", [white]),
            ("pass", 1.0),
        )

    def test_a_bad_line_is_refused(self):
        for line, why in (
            (
                "A | css:p where distinct style:color <= 2 | text | present",
                "where reads each element",
            ),
            (
                "A | css:p where text = all of (css:a) text | text | present",
                "where compares within",
            ),
            ("A | css:p | text | > all of (css:a text", "closing"),
            ("A | css:p | decl:color | present", "select sheet"),
            ("A | sheet | style:color | present", "sheet takes only"),
            (
                "A | css:p | parent authored:color | present",
                "parent reads another element",
            ),
            ("A | css:p | text of ::marker | present", "goes with a style"),
            ("A | css:p | pixels:chroma-share x | present", "wants a number"),
            ("A | css:p | distinct style:color within grid | <= 1", "within wants"),
            (
                "A | css:p | style:width | within 3% of 16px",
                "within N% of wants a read",
            ),
        ):
            with self.subTest(line):
                self.assertRaisesRegex(probe.TableError, why, probe.parse, line)


if __name__ == "__main__":
    child.main()
