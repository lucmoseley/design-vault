import concurrent.futures
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "parts-map.py"
)
FIXTURES = os.path.join(HERE, "fixtures", "parts")
RUNS = ("pill", "card", "clean", "links")
SCRATCH = tempfile.TemporaryDirectory()
DONE = {}


def setUpModule():
    with concurrent.futures.ThreadPoolExecutor(len(RUNS)) as pool:
        DONE.update(zip(RUNS, pool.map(check, RUNS), strict=True))


def tearDownModule():
    SCRATCH.cleanup()


def check(name):
    out = os.path.join(SCRATCH.name, name)
    r = child.run(
        [
            sys.executable,
            SCRIPT,
            os.path.join(FIXTURES, f"{name}.html"),
            "--out",
            out,
        ],
        timeout=600,
    )
    found = None
    if os.path.exists(os.path.join(out, "parts.json")):
        with open(os.path.join(out, "parts.json"), encoding="utf8") as fh:
            found = json.load(fh)
    return r.returncode, r.stdout, r.stderr, found, out


def by_text(found):
    return {p["text"]: p for p in found["parts"]}


class StaticPill(unittest.TestCase):
    def setUp(self):
        self.code, self.out, self.err, self.found, self.dir = DONE["pill"]
        self.parts = by_text(self.found)

    def test_one_tap_target_each_passes(self):
        self.assertEqual(self.code, 0, self.out + self.err)
        self.assertEqual(
            self.found["answers"]["vault.one-target"], {"answer": "pass", "faults": []}
        )

    def test_the_pill_is_listed_and_cannot_be_acted_on(self):
        pill = self.parts["Free breakfast"]
        self.assertFalse(pill["actable"])
        self.assertIn("draws its own box", pill["listed"])
        self.assertIsNone(pill["at"]["desktop"]["hit"])

    def test_the_button_beside_it_can_be_acted_on_with_its_rules(self):
        button = self.parts["Book a bed"]
        self.assertTrue(button["actable"])
        self.assertEqual(button["role"], "button")
        self.assertEqual(button["hover"], [".btn:hover"])
        self.assertEqual(button["focus"], [".btn:focus-visible"])
        self.assertEqual(button["at"]["phone"]["hit"], 100)

    def test_links_carry_their_href(self):
        self.assertTrue(self.parts["Rooms"]["href"].endswith("pill.html#rooms"))
        self.assertTrue(self.parts["Rooms"]["actable"])

    def test_each_reason_a_static_part_could_look_actable_lists_it(self):
        for text, why in (
            ("Open every day", "cursor: pointer"),
            ("Ten minutes from the beach", "underlined"),
            ("A small house by the sea", "a :hover rule selects it"),
            ("Our rooms", "a link's colour"),
            ("Quiet rooms", "draws its own box"),
        ):
            with self.subTest(text):
                self.assertEqual(self.parts[text]["listed"], [why])
                self.assertFalse(self.parts[text]["actable"])

    def test_a_cursor_only_inherited_lists_nothing(self):
        self.assertNotIn("every", self.parts)

    def test_a_disabled_control_cannot_be_acted_on(self):
        self.assertFalse(self.parts["Sold out"]["actable"])

    def test_a_click_the_page_adds_by_script_makes_a_part_actable(self):
        for text in (
            "Read more about the house",
            "See the garden",
            "Open the gallery",
            "See the bar",
            "Hold to hear",
        ):
            with self.subTest(text):
                self.assertTrue(self.parts[text]["actable"])
                self.assertEqual(self.parts[text]["role"], "click handler on p")

    def test_ids_follow_document_order(self):
        self.assertEqual(
            [p["id"] for p in self.found["parts"]], [f"p{i}" for i in range(1, 16)]
        )
        self.assertEqual(self.parts["Rooms"]["id"], "p1")

    def test_the_key_names_each_part_and_never_what_it_does(self):
        with open(os.path.join(self.dir, "key.txt"), encoding="utf8") as fh:
            lines = [ln for ln in fh.read().splitlines() if ln.startswith("p")]
        self.assertEqual(len(lines), 15)
        self.assertTrue(lines[2].startswith('p3  "Book a bed"  desktop at'))
        for line in lines:
            self.assertNotRegex(line, r"button|link|actable|click|static|role")
        for width in ("desktop", "phone"):
            self.assertTrue(
                os.path.getsize(os.path.join(self.dir, f"key-{width}.png")) > 0
            )


class NestedCard(unittest.TestCase):
    def setUp(self):
        self.code, self.out, self.err, self.found, _ = DONE["card"]

    def test_162_two_actions_on_one_tap_target_fail(self):
        self.assertEqual(self.code, 1, self.out + self.err)
        answer = self.found["answers"]["vault.one-target"]
        self.assertEqual(answer["answer"], "fail")
        self.assertEqual(
            [(f["subject"], f["detail"], f["at"]) for f in answer["faults"]],
            [
                (
                    'p2 (button, "Compare")',
                    'is nested inside p1 (link, "Hostel A From €18 a night Compare")',
                    ["desktop", "phone"],
                ),
                (
                    'p4 (button, "Save")',
                    'sits inside the click area of p3 (link, "Hostel B")',
                    ["desktop", "phone"],
                ),
                (
                    'p6 (button, "Share")',
                    'sits inside the click area of p5 (link, "Hostel C")',
                    ["desktop", "phone"],
                ),
            ],
        )
        self.assertIn('p4 (button, "Save") sits inside the click area of p3', self.out)

    def test_nesting_and_click_area_are_kept_apart(self):
        parts = by_text(self.found)
        self.assertEqual(parts["Compare"]["at"]["desktop"]["inside"], "p1")
        self.assertIsNone(parts["Save"]["at"]["desktop"]["inside"])
        self.assertEqual(parts["Save"]["at"]["desktop"]["enclosed_by"], "p3")

    def test_a_part_taking_clicks_off_another_is_named_with_its_share(self):
        card = by_text(self.found)["Hostel A From €18 a night Compare"]["at"]["desktop"]
        self.assertEqual(card["taken_by"], ["p2"])
        self.assertLess(card["hit"], 100)


class Clean(unittest.TestCase):
    def setUp(self):
        self.code, self.out, self.err, self.found, _ = DONE["clean"]
        self.parts = by_text(self.found)

    def test_a_button_grown_for_a_coarse_pointer_is_measured_grown_at_phone_width(self):
        close = self.parts["×"]["at"]
        self.assertEqual(
            (close["desktop"]["box"][2:], close["phone"]["box"][2:]),
            ([20, 20], [44, 44]),
        )

    def test_one_action_per_target_passes_with_no_faults(self):
        self.assertEqual(self.code, 0, self.out + self.err)
        self.assertEqual(self.found["answers"]["vault.one-target"]["answer"], "pass")

    def test_a_reset_rule_on_every_elements_hover_leaves_its_sheet_read(self):
        self.assertEqual(self.found["unread_stylesheets"], [])

    def test_a_listener_delegating_the_whole_page_makes_nothing_actable(self):
        self.assertTrue(
            all(not p["role"].startswith("click handler") for p in self.found["parts"])
        )

    def test_a_checkbox_in_its_label_and_a_summary_are_one_target_each(self):
        box = self.parts["Send me news"]
        self.assertEqual(box["role"], "checkbox")
        self.assertIsNone(box["at"]["desktop"]["enclosed_by"])
        self.assertTrue(self.parts["Opening hours"]["actable"])

    def test_a_field_is_named_by_its_label(self):
        self.assertEqual(self.parts["Email"]["role"], "textbox")

    def test_two_buttons_side_by_side_are_not_one_inside_the_other(self):
        for text in ("−", "+"):
            with self.subTest(text):
                self.assertEqual(self.parts[text]["at"]["desktop"]["hit"], 100)
                self.assertIsNone(self.parts[text]["at"]["desktop"]["enclosed_by"])

    def test_a_static_box_is_listed_and_fails_nothing(self):
        self.assertEqual(
            self.parts["Breakfast is included."]["listed"], ["draws its own box"]
        )
        self.assertEqual(len(self.found["parts"]), 12)


class DeadLinks(unittest.TestCase):
    def setUp(self):
        self.code, self.out, self.err, self.found, _ = DONE["links"]
        self.parts = by_text(self.found)

    def test_a_link_to_hash_alone_or_to_a_missing_id_is_dead(self):
        for text, target in (
            ("Book a bed", "#"),
            ("Destinations", "#destinations"),
            ("Late rooms", "#late"),
        ):
            with self.subTest(text):
                self.assertEqual(self.parts[text]["dead"], target)
                self.assertTrue(self.parts[text]["actable"])

    def test_a_link_to_an_id_a_name_top_its_own_click_quoted_words_or_another_page_is_not(
        self,
    ):
        for text in (
            "Rooms",
            "Old anchor",
            "Summer",
            "Back to top",
            "Menu",
            "Quoted",
            "Elsewhere",
        ):
            with self.subTest(text):
                self.assertIsNone(self.parts[text]["dead"])

    def test_dead_links_are_printed_and_leave_one_target_passing(self):
        self.assertEqual(self.code, 0, self.out + self.err)
        self.assertRegex(
            self.out,
            r'(?m)^  p\d+ \("Destinations"\) goes to #destinations, which nothing on the page carries$',
        )
        self.assertRegex(self.out, r'(?m)^  p\d+ \("Book a bed"\) goes to # alone$')


class Usage(unittest.TestCase):
    def test_an_earlier_runs_files_are_gone_when_a_load_fails(self):
        out = os.path.join(SCRATCH.name, "stale")
        os.makedirs(out)
        stale = ("parts.json", "key.txt", "key-desktop.png", "key-phone.png")
        for name in stale:
            with open(os.path.join(out, name), "w") as fh:
                fh.write("old")
        r = child.run(
            [
                sys.executable,
                SCRIPT,
                "http://127.0.0.1:9/",
                "--out",
                out,
                "--timeout",
                "5000",
            ],
            timeout=120,
        )
        self.assertIn(r.returncode, (4, 5), r.stdout + r.stderr)
        self.assertIn("the browser could not load http://127.0.0.1:9/", r.stderr)
        self.assertEqual([n for n in stale if os.path.exists(os.path.join(out, n))], [])

    def test_no_out_is_a_usage_error(self):
        r = child.run(
            [sys.executable, SCRIPT, os.path.join(FIXTURES, "clean.html")],
            timeout=60,
        )
        self.assertEqual(r.returncode, 2)
        self.assertIn("the following arguments are required: --out", r.stderr)


if __name__ == "__main__":
    child.main()
