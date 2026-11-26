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
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-markup.py"
)
TABLE_FILE = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-markup.table"
)
AXE_FILE = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "vendor", "axe-core", "axe.min.js"
)
SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

markup = siblings.load(SCRIPTS, "check-markup.py")

FIXTURES = pathlib.Path(HERE, "fixtures", "markup").resolve()
FAULT = FIXTURES / "tier01-fault.html"
CLEAN = FIXTURES / "tier01-clean.html"
RECORDS = [
    line.split(" | ")[0]
    for line in pathlib.Path(TABLE_FILE).read_text().splitlines()
    if line.strip() and not line.startswith(("#", "off "))
]
LOGO = ("--part", "logo=header img.logo")
PHONE, DESKTOP = 390, 1920
RUNS = {}
CLI_TIMEOUT_S = 300  # guess, #501


def run(page, *argv, table=None):
    key = (str(page), argv, table)
    if key in RUNS:
        return RUNS[key]
    with tempfile.TemporaryDirectory() as out:
        extra = []
        if table is not None:
            path = pathlib.Path(out, "given.table")
            path.write_text(table)
            extra = ["--table", str(path)]
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                code = markup.main([str(page), "--out", out, *argv, *extra])
            except SystemExit as exc:
                code = exc.code
        written = pathlib.Path(out, "markup.json")
        data = json.loads(written.read_text()) if written.exists() else None
    child.raise_if_crashed(stderr.getvalue())
    RUNS[key] = (code, stdout.getvalue(), stderr.getvalue(), data)
    return RUNS[key]


def found(page, *argv, table=None):
    _, _, _, data = run(page, *argv, table=table)
    return {f["id"]: f for f in data["findings"]}


def faults(page):
    return set(re.findall(r"<!-- fault: (\S+?):", page.read_text()))


def page_file(folder, body):
    path = pathlib.Path(folder, "page.html")
    path.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>t</title></head>'
        f"<body>{body}</body></html>"
    )
    return path


class TheFixtures(unittest.TestCase):
    def test_the_fault_page_plants_one_fault_for_each_record_the_table_checks(self):
        self.assertEqual(faults(FAULT), set(RECORDS))
        self.assertEqual(faults(CLEAN), set())

    def test_every_record_fails_on_the_fault_page_on_its_marked_element_307(self):
        code, stdout, _, data = run(FAULT, *LOGO)
        self.assertEqual(code, 1)
        self.assertEqual(data["answers"], dict.fromkeys(RECORDS, "fail"))
        for f in data["findings"]:
            with self.subTest(f["id"]):
                self.assertIn(f"{f['id']}: fail", stdout)
                self.assertTrue(f["misses"])
                for miss in f["misses"]:
                    self.assertIn(f'data-fault="{f["id"]}"', miss["html"])

    def test_each_page_is_read_at_phone_and_desktop_width(self):
        got = found(FAULT, *LOGO)
        self.assertEqual(
            {m["width"] for m in got["vault.lang-parts"]["misses"]}, {PHONE, DESKTOP}
        )
        self.assertEqual(
            [m["width"] for m in got["vault.label-in-name"]["misses"]], [PHONE]
        )

    def test_the_clean_page_passes_every_record(self):
        code, _, _, data = run(CLEAN, *LOGO)
        self.assertEqual(code, 0)
        self.assertEqual(data["answers"], dict.fromkeys(RECORDS, "pass"))
        for f in data["findings"]:
            self.assertEqual((f["misses"], f["unjudged"]), ([], []))

    def test_the_loaded_axe_is_the_vendored_version(self):
        _, _, _, data = run(CLEAN, *LOGO)
        with open(AXE_FILE, encoding="utf8") as fh:
            self.assertTrue(fh.readline().startswith(f"/*! axe v{data['axe']}"))


class ThePartLine(unittest.TestCase):
    def test_axe_reads_only_the_part_and_the_link_that_holds_it(self):
        with tempfile.TemporaryDirectory() as d:
            page = page_file(
                d,
                '<header><a href="/"><img class="logo" src="l.svg" alt="Sea Hostel home"></a>'
                '<a href="https://social.example"><svg></svg></a></header><main><p>x</p></main>',
            )
            got = found(page, *LOGO)["vault.logo-link-name"]
        self.assertEqual((got["answer"], got["misses"]), ("pass", []))

    def test_a_part_with_no_selector_is_not_judged(self):
        got = found(FAULT)["vault.logo-link-name"]
        self.assertEqual(got["answer"], "not judged")
        self.assertEqual(
            {u["what"] for u in got["unjudged"]}, {"no selector for the part logo"}
        )

    def test_a_parts_declaration_gives_the_part_its_selector(self):
        with tempfile.TemporaryDirectory() as d:
            declared = pathlib.Path(d, "parts.json")
            declared.write_text('{"declared": {"logo": "header img.logo"}}')
            got = found(FAULT, "--parts", str(declared))["vault.logo-link-name"]
        self.assertEqual(got["answer"], "fail")

    def test_a_part_the_page_does_not_have_is_no_match(self):
        got = found(FAULT, "--part", "logo=.no-such-logo")["vault.logo-link-name"]
        self.assertEqual((got["answer"], got["misses"]), ("no match", []))


class NeedsReview(unittest.TestCase):
    def test_what_axe_cannot_decide_is_reported_and_never_tallied(self):
        with tempfile.TemporaryDirectory() as d:
            page = page_file(d, '<main><video src="v.mp4" controls></video></main>')
            code, stdout, _, data = run(page, table="vault.media | video-caption\n")
        got = data["findings"][0]
        self.assertEqual(code, 0)
        self.assertEqual((got["answer"], got["misses"]), ("no match", []))
        self.assertEqual({r["rule"] for r in got["review"]}, {"video-caption"})
        self.assertIn("  review [video-caption] ", stdout)


class TheTableGivesTheRules(unittest.TestCase):
    def test_a_record_answers_by_the_rule_ids_its_line_names(self):
        got = found(FAULT, table="vault.lang-parts | html-has-lang\n")
        self.assertEqual(got["vault.lang-parts"]["answer"], "pass")

    def test_an_experimental_rule_runs_where_a_line_names_it(self):
        with open(AXE_FILE, encoding="utf8") as fh:
            axe = fh.read()
        for rule in ("label-content-name-mismatch", "p-as-heading"):
            with self.subTest(rule):
                meta = re.search(r'id:"' + rule + r'",[^{}]*?tags:\[([^\]]*)\]', axe)
                self.assertIn('"experimental"', meta[1])
        got = found(FAULT, *LOGO)
        self.assertEqual(got["vault.label-in-name"]["answer"], "fail")
        self.assertEqual(got["vault.heading-markup"]["answer"], "fail")

    def test_the_off_rules_are_the_vault_s_own(self):
        off = [
            line
            for line in pathlib.Path(TABLE_FILE).read_text().splitlines()
            if line.startswith("off ")
        ]
        self.assertEqual(off, ["off | color-contrast, link-in-text-block, target-size"])

    def test_a_malformed_table_exits_2(self):
        for text, why in (
            ("vault.a\n", "want ID"),
            ("vault.a | Region\n", "not an axe rule id"),
            ("vault.a | region | logo\n", "want part:NAME"),
            ("off | region | part:logo\n", "off line takes no part"),
            ("off | region\n", "no record lines"),
            (
                "off | color-contrast\nvault.a | color-contrast, region\n",
                "color-contrast is off",
            ),
        ):
            with self.subTest(text):
                code, _, err, data = run(CLEAN, table=text)
                self.assertEqual((code, data), (2, None))
                self.assertIn(why, err)

    def test_an_axe_rule_axe_does_not_know_exits_2(self):
        code, _, err, _ = run(CLEAN, table="vault.a | no-such-rule\n")
        self.assertEqual(code, 2)
        self.assertIn("axe knows no rule no-such-rule", err)


class TheCommand(unittest.TestCase):
    def test_the_command_line_runs_and_exits_1_on_a_miss(self):
        with tempfile.TemporaryDirectory() as out:
            done = child.run(
                [sys.executable, SCRIPT, str(FAULT), "--out", out, *LOGO],
                timeout=CLI_TIMEOUT_S,
            )
            data = json.loads(pathlib.Path(out, "markup.json").read_text())
        self.assertEqual(done.returncode, 1)
        self.assertEqual(data["answers"], dict.fromkeys(RECORDS, "fail"))

    def test_a_missing_page_exits_2(self):
        code, _, err, _ = run(FIXTURES / "nowhere.html")
        self.assertEqual(code, 2)
        self.assertIn("no such file", err)


if __name__ == "__main__":
    child.main()
