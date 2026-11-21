"""Pins check-access.py's --pointer mode, vault.coarse-target (#317): python3 test/check-access-pointer.test.py

The fault fixture plants one fault for each of the record's two branches, marked
#coarse-target and #coarse-target-fine. A suite of the commit gate (test/all.sh): a target a finger cannot hit would otherwise
reach the critic as a pass.
"""

import concurrent.futures
import http.server
import importlib.util
import json
import os
import sys
import tempfile
import threading
import unittest

HERE = os.path.dirname(__file__)
SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-access.py"
)
LIBRARY = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "access-pointer.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "access")
FAULT = os.path.join(FIXTURES, "target-pointer-fault.html")
CLEAN = os.path.join(FIXTURES, "target-pointer-clean.html")
SHEETS = os.path.join(FIXTURES, "target-pointer-sheets.html")

CHILD = importlib.util.spec_from_file_location("child", os.path.join(HERE, "child.py"))
child = importlib.util.module_from_spec(CHILD)
CHILD.loader.exec_module(child)

spec = importlib.util.spec_from_file_location("access_pointer", LIBRARY)
pointing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pointing)

QID = "vault.coarse-target"
# How long one run may take, in s. A guess, unmeasured.
RUN_S = 300
SCRATCH = tempfile.TemporaryDirectory()
DONE = {}
# The page and its style sheet, each served from an origin of its own.
SITE = tempfile.TemporaryDirectory()
SERVERS = []


class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE.name, **kwargs)

    def log_message(self, *args):
        pass


def run(name, page, *args):
    out = os.path.join(SCRATCH.name, name)
    r = child.run(
        [sys.executable, SCRIPT, page, "--out", out, "--pointer", *args],
        timeout=RUN_S,
    )
    found = None
    path = os.path.join(out, "pointer.json")
    if os.path.exists(path):
        with open(path, encoding="utf8") as fh:
            found = json.load(fh)
    return r.returncode, r.stdout + r.stderr, found


def table(name, text):
    path = os.path.join(SCRATCH.name, f"{name}.table")
    with open(path, "w", encoding="utf8") as fh:
        fh.write(text)
    return path


def serve():
    for _ in range(2):
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Quiet)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        SERVERS.append(server)
    page, sheet = (f"http://127.0.0.1:{s.server_address[1]}" for s in SERVERS)
    with open(os.path.join(SITE.name, "sheet.css"), "w", encoding="utf8") as fh:
        fh.write("@media (hover: hover) { button { width: 20px; height: 20px } }\n")
    with open(os.path.join(SITE.name, "page.html"), "w", encoding="utf8") as fh:
        fh.write(
            '<!doctype html><meta charset="utf-8"><link rel="stylesheet" '
            f'href="{sheet}/sheet.css"><style>button {{ appearance: none; border: 0; '
            'width: 44px; height: 44px }</style><button aria-label="Go"></button>\n'
        )
    return f"{page}/page.html", sheet


def setUpModule():
    page, DONE["sheet"] = serve()
    runs = {
        "fault": (FAULT,),
        # --pointer reads no contrast table, so a missing one cannot stop it.
        "clean": (
            CLEAN,
            "--contrast-table",
            os.path.join(SCRATCH.name, "absent-contrast.table"),
        ),
        "sheets": (SHEETS,),
        "table24": (
            FAULT,
            "--pointer-table",
            table("t24", "vault.coarse-target | coarse | 24px\n"),
        ),
        "cross": (page,),
    }
    with concurrent.futures.ThreadPoolExecutor(len(runs)) as pool:
        jobs = {name: pool.submit(run, name, *args) for name, args in runs.items()}
        DONE.update({name: job.result() for name, job in jobs.items()})


def tearDownModule():
    for server in SERVERS:
        server.shutdown()
    SITE.cleanup()
    SCRATCH.cleanup()


def faults(found):
    return {f["subject"]: f for f in found["answers"][QID]["faults"]}


class Pointer(unittest.TestCase):
    def test_the_fault_page_names_each_plant_at_both_widths_and_nothing_else(self):
        code, said, found = DONE["fault"]
        self.assertEqual(code, 1, said)
        got = faults(found)
        self.assertEqual(
            set(got), {"button#coarse-target", "button#coarse-target-fine"}, said
        )
        self.assertEqual(
            got["button#coarse-target"]["detail"],
            "is 60x24 px under a coarse pointer; 44x44 px needed",
        )
        self.assertEqual(
            got["button#coarse-target-fine"]["detail"],
            "is 20x44 px under a fine pointer, smaller than the 44x44 px it is given with its pointer and hover media rules off",
        )
        for f in got.values():
            self.assertEqual(f["at"], ["desktop", "phone"])

    def test_the_clean_page_passes_with_its_prose_link_skip_link_and_labelled_checkbox_and_no_contrast_table(
        self,
    ):
        code, said, found = DONE["clean"]
        self.assertEqual(code, 0, said)
        self.assertEqual(list(found["answers"]), [QID])
        self.assertEqual(found["answers"][QID]["answer"], "pass")
        self.assertEqual(found["answers"][QID]["notes"], [])

    def test_a_shrink_is_found_through_a_linked_sheet_style_media_and_a_nested_rule(
        self,
    ):
        code, said, found = DONE["sheets"]
        self.assertEqual(code, 1, said)
        self.assertEqual(
            set(faults(found)),
            {"button#linked", "button#style-media", "button#nested"},
            said,
        )

    def test_the_coarse_floor_is_the_tables(self):
        code, said, found = DONE["table24"]
        self.assertEqual(code, 1, said)
        self.assertEqual(set(faults(found)), {"button#coarse-target-fine"}, said)

    def test_a_sheet_from_another_origin_is_left_on_and_named(self):
        code, said, found = DONE["cross"]
        self.assertEqual(code, 0, said)
        self.assertEqual(
            [n["note"] for n in found["answers"][QID]["notes"]],
            [
                (
                    f"the style sheet {DONE['sheet']}/sheet.css cannot be read, as another site's cannot without CORS, "
                    "so its pointer and hover rules were left on"
                )
            ],
        )

    def test_a_table_it_cannot_run_exits_2_saying_why(self):
        for name, path, said in (
            (
                "under",
                table("under", "vault.coarse-target | coarse | 20px\n"),
                "coarse may not be under vault.target-size's 24px",
            ),
            (
                "unit",
                table("unit", "vault.coarse-target | coarse | 44\n"),
                "coarse wants a value like 44px",
            ),
            ("empty", table("empty", "# nothing\n"), "no coarse line"),
            (
                "missing",
                os.path.join(SCRATCH.name, "absent.table"),
                "cannot read --pointer-table",
            ),
        ):
            with self.subTest(name):
                code, out, _ = run(name, CLEAN, "--pointer-table", path)
                self.assertEqual(code, 2, out)
                self.assertIn(said, out)


class Table(unittest.TestCase):
    def test_the_records_coarse_line_gives_its_floor(self):
        self.assertEqual(
            pointing.parse_table("# a\nvault.coarse-target | coarse | 48px\n", 24), 48.0
        )

    def test_a_floor_under_the_least_a_second_line_another_record_or_mode_is_refused(
        self,
    ):
        for text in (
            "vault.coarse-target | coarse | 23px",
            "vault.coarse-target | coarse | 44px\nvault.coarse-target | coarse | 48px",
            "vault.coarse-target | fine | 44px",
            "vault.target-size | coarse | 44px",
        ):
            with self.subTest(text=text), self.assertRaises(pointing.TableError):
                pointing.parse_table(text, 24)


if __name__ == "__main__":
    child.main()
