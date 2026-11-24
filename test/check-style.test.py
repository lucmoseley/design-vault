"""Pins check-style.py (#309): python3 test/check-style.test.py

It is a suite of the commit gate (test/all.sh): loosening it lets a page pass
a computed-style record it misses, or fail one it meets.
test/fixtures/probe/style-fault.html plants one fault per record, on an
element whose id is f- and the record's name, and every record must fail on
its plant, or on the whole selection where WHOLE names it. A record's
extra plants take f-<record>-<variant>.
test/fixtures/probe/style-clean.html meets every record but those UNMET names,
and nothing may fail or go unjudged there.
"""

import collections
import concurrent.futures
import importlib.util
import json
import math
import os
import re
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-style.py"
)
TABLE = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-style.table"
)
RULES = os.path.join(HERE, "..", "plugin", "skills", "design-critique", "rules")
FIXTURES = os.path.join(HERE, "fixtures", "probe")
FAULT = os.path.join(FIXTURES, "style-fault.html")
CLEAN = os.path.join(FIXTURES, "style-clean.html")
PARTS = os.path.join(FIXTURES, "style-parts.json")
# One phone width, which the `at 320-640` block reads, and two wider ones,
# where prose runs past 50 characters a line and headings reach 48 px.
SWEEP = ["--widths", "320-1920", "--step", "800"]
# A page's sweep runs a few minutes; ten is a hung browser.
RUN_TIMEOUT_S = 600
# Records whose plant misses on the whole selection, never one element. Each
# is the miss's subject, or how it starts.
WHOLE = {
    "vault.button-size": "role:button",
    "vault.action-colour": "role:button where ",
    "vault.calm-colour-share": "body",
    "vault.text-steps": "ground rgb(250, 250, 250)",
    "vault.fallback-metrics": "@font-face f-fallback-metrics",
}
# Records the clean page cannot meet as anything but no match.
# Faces under type-size's 0.52 reference: Georgia 0.481 and Times 0.447,
# measured (docs/research/typeface-traits.md R5); 0.4784, check-style's
# reading of the plants' `font-size-adjust: 0.481` in Chromium (#514).
UNDER_REFERENCE_XHEIGHTS = (0.481, 0.4784, 0.447)
UNMET = {
    # Justified text is allowed only where a project's rules file names it,
    # and vault.text-align refuses it on a page with none.
    "vault.justify-space",
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


style = load("check_style", SCRIPT)
RAN = {}
WORK = []


def check(page, out):
    return child.run(
        [
            sys.executable,
            SCRIPT,
            page,
            "--out",
            out,
            "--parts",
            PARTS,
            "--brief",
            "energy=calm",
            *SWEEP,
        ],
        timeout=RUN_TIMEOUT_S,
    )


def setUpModule():
    """Both pages run once, side by side."""
    work = tempfile.mkdtemp(prefix="check-style-")
    WORK.append(work)
    pages = {"fault": FAULT, "clean": CLEAN}
    with concurrent.futures.ThreadPoolExecutor(len(pages)) as pool:
        done = {
            name: pool.submit(check, page, os.path.join(work, name))
            for name, page in pages.items()
        }
    for name, job in done.items():
        proc = job.result()
        found = os.path.join(work, name, "style.json")
        with open(found, encoding="utf8") as fh:
            RAN[name] = (proc, json.load(fh)["findings"])


def tearDownModule():
    for work in WORK:
        shutil.rmtree(work, ignore_errors=True)


def plant_at(plant):
    """A plant's id in a miss's subject, never a longer id it begins."""
    return re.compile(re.escape("#" + plant) + r"(?![\w-])")


def read_records():
    records = {}
    for name in os.listdir(RULES):
        with open(os.path.join(RULES, name), encoding="utf8") as fh:
            for chunk in re.split(r"^### ", fh.read(), flags=re.M)[1:]:
                rid, _, body = chunk.partition("\n")
                records[rid.strip()] = dict(
                    re.findall(r"^- ([\w-]+): (.*)$", body, flags=re.M)
                )
    return records


def table_ids():
    with open(TABLE, encoding="utf8") as fh:
        blocks = style.parse(fh.read())
    return list(dict.fromkeys(r.id for b in blocks for r in b.rules))


class Pages(unittest.TestCase):
    def test_the_fault_page_fails_every_record_on_its_plant(self):
        proc, found = RAN["fault"]
        self.assertEqual(proc.returncode, 1, proc.stderr)
        by_id = {f["id"]: f for f in found}
        self.assertEqual(sorted(by_id), sorted(table_ids()))
        for rid, f in by_id.items():
            with self.subTest(rid):
                self.assertEqual(f["answer"], "fail")
                subjects = [m["subject"] for m in f["misses"]]
                if rid in WHOLE:
                    hit = [
                        s
                        for s in subjects
                        if s == WHOLE[rid]
                        or s.startswith(WHOLE[rid])
                        and WHOLE[rid].endswith(" ")
                    ]
                else:
                    plant = plant_at("f-" + rid.removeprefix("vault."))
                    hit = [s for s in subjects if plant.search(s)]
                self.assertTrue(hit, f"no miss on its plant: {subjects[:5]}")
                self.assertIn(f"{rid}: fail", proc.stdout)
        self.assertIn("every finding: ", proc.stdout)

    def test_type_size_fails_each_plant_on_the_one_floor_it_breaks(self):
        """#479, #514. Pass pair: test_the_clean_page_reports_nothing."""
        _, found = RAN["fault"]
        (f,) = [f for f in found if f["id"] == "vault.type-size"]
        for plant, read in (
            ("f-type-size-tall", "style:font-size"),
            ("f-type-size-short", "style:font-size times xheight"),
            ("f-type-size-nearest", "style:font-size times xheight"),
            ("f-type-size-nearest-dense", "style:font-size times xheight"),
        ):
            with self.subTest(plant):
                at = plant_at(plant)
                reads = {m["read"] for m in f["misses"] if at.search(m["subject"])}
                self.assertEqual(reads, {read})

    def test_every_block_of_the_table_misses_on_the_fault_page(self):
        _, found = RAN["fault"]
        with open(TABLE, encoding="utf8") as fh:
            headers = {b.header for b in style.parse(fh.read())}
        missed = collections.defaultdict(list)
        for f in found:
            for m in f["misses"]:
                missed[m["block"]].append(m)
        self.assertEqual(sorted(missed), sorted(headers))
        for m in missed["at 320-640"]:
            self.assertLessEqual(m["to"], 640, m["subject"])

    def test_the_clean_page_reports_nothing(self):
        proc, found = RAN["clean"]
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        for f in found:
            with self.subTest(f["id"]):
                want = "no match" if f["id"] in UNMET else "pass"
                self.assertEqual(f["answer"], want, f["unjudged"][:3])
        self.assertNotIn(": fail", proc.stdout)

    def test_a_bad_width_span_is_refused_by_name(self):
        proc = child.run(
            [
                sys.executable,
                SCRIPT,
                CLEAN,
                "--out",
                tempfile.gettempdir(),
                "--widths",
                "640-320",
            ],
            timeout=RUN_TIMEOUT_S,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("--widths wants LOW-HIGH within", proc.stderr)


class Records(unittest.TestCase):
    def test_every_record_the_table_answers_names_this_script(self):
        records = read_records()
        for rid in table_ids():
            with self.subTest(rid):
                self.assertIn(rid, records)
                self.assertEqual(records[rid].get("answered-by"), "script")
                self.assertRegex(records[rid].get("script", ""), r"^check-style\.py ")

    def test_type_size_prescribes_a_size_its_x_height_rows_pass(self):
        """#514."""
        output = read_records()["vault.type-size"]["output"]
        with open(TABLE, encoding="utf8") as fh:
            table = fh.read()

        def floor(role, read):
            (px,) = re.findall(
                rf"^vault\.type-size \| \${role} \| {read} \| >= ([\d.]+)px$",
                table,
                flags=re.M,
            )
            return float(px)

        for role in ("prose", "dense"):
            base = floor(role, "style:font-size")
            least = floor(role, "style:font-size times xheight")
            ratio = least / base
            self.assertIn(
                f"max({base:g}, {base:g} × {ratio:g} ÷ xheight) px, rounded up", output
            )
            for xheight in UNDER_REFERENCE_XHEIGHTS:
                with self.subTest(role=role, xheight=xheight):
                    size = max(base, math.ceil(base * ratio / xheight))
                    self.assertGreaterEqual(size * xheight, least)


class Table(unittest.TestCase):
    def test_a_bad_table_names_its_line(self):
        for text, why in (
            ("A | css:p | $gap | = 0", r"line 1: \$gap is not defined above"),
            ("at 640-320\nA | css:p | text | present", "line 1: at wants LOW-HIGH"),
            (
                "under dusk\nA | css:p | text | present",
                "line 1: 'dusk' is no condition",
            ),
            ("when energy\nA | css:p | text | present", "line 1: when wants KEY=VALUE"),
            (
                "compare scheme=dark\nA | css:p | text | present",
                "line 1: compare wants two",
            ),
            (
                "compare scheme=light scheme=dark\nA | css:p | style:color | = red",
                "line 2: a compare line's MUST is same",
            ),
            (
                "across pages\nA | css:p | style:color | = body style:color",
                "line 2: across pages pools values",
            ),
            ("# only a comment", "the table holds no rule"),
        ):
            with self.subTest(text):
                self.assertRaisesRegex(style.TableError, why, style.parse, text)

    def test_a_define_and_the_blocks_reach_their_lines(self):
        blocks = style.parse(
            "define $p = css:p\n"
            "A | $p | text | present\n"
            "at 320-640\nB | $p | text | present\n"
            "under scheme=dark print\nC | $p | text | present\n"
            "end\nD | $p | text | present"
        )
        got = [(b.header, b.span, b.given, [r.id for r in b.rules]) for b in blocks]
        self.assertEqual(
            got,
            [
                ("page as it loads", None, {}, ["A"]),
                ("at 320-640", (320, 640), {}, ["B"]),
                (
                    "under scheme=dark print",
                    None,
                    {"scheme": "dark", "print_media": True},
                    ["C"],
                ),
                ("page as it loads", None, {}, ["D"]),
            ],
        )
        self.assertEqual(blocks[0].rules[0].select.text, "css:p")

    def test_a_when_block_waits_on_its_brief(self):
        blocks = style.parse("when energy=calm\nA | css:body | text | present")
        kwargs = {"widths": [320], "heights": (), "parts": {}, "timeout": 1}
        ran, _ = style.run(None, "about:blank", blocks, brief={}, **kwargs)
        self.assertEqual(
            [f["answer"] for _, found in ran for f in found], ["not judged"]
        )
        ran, _ = style.run(
            None, "about:blank", blocks, brief={"energy": "loud"}, **kwargs
        )
        self.assertEqual(ran, [])

    def test_a_line_on_an_undeclared_part_drops_out(self):
        (block,) = style.parse(
            "A | part:hero | text | present\n"
            "B | css:p | style:width | > all of (part:card) style:width\n"
            "C | css:p | text | present"
        )
        kept = style.without(block, {"hero": ".hero"})
        self.assertEqual([r.id for r in kept.rules], ["A", "C"])

    def test_the_worst_answer_wins_across_blocks(self):
        blocks = style.parse(
            "A | css:p | text | present\nat 320-640\nA | css:p | text | present"
        )
        found = style.merged(
            [
                (
                    blocks[0],
                    [{"id": "A", "answer": "pass", "misses": [], "unjudged": []}],
                ),
                (
                    blocks[1],
                    [
                        {
                            "id": "A",
                            "answer": "fail",
                            "misses": [{"x": 1}],
                            "unjudged": [],
                        }
                    ],
                ),
            ]
        )
        self.assertEqual(
            found,
            [
                {
                    "id": "A",
                    "answer": "fail",
                    "misses": [{"x": 1, "block": "at 320-640"}],
                    "unjudged": [],
                }
            ],
        )


if __name__ == "__main__":
    child.main()
