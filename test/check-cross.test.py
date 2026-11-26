import contextlib
import json
import os
import pathlib
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-cross.py"
)


SCRIPTS = os.path.dirname(SCRIPT)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

cross = siblings.load(SCRIPTS, "check-cross.py")
runner = siblings.load(SCRIPTS, "runner.py")
FIXTURES = pathlib.Path(HERE, "fixtures", "cross").resolve()
with open(cross.TABLE, encoding="utf8") as fh:
    TABLE_TEXT = fh.read()
TABLE = cross.parse(TABLE_TEXT)
RECORDS = list(dict.fromkeys(line.id for line in TABLE))
OPEN = contextlib.ExitStack()
SITES = {}
BROWSER = None
DEVICES = {}
CLI_TIMEOUT_S = 300  # guess, #501


def radius(page):
    return page.eval_on_selector(
        "main", "(el) => getComputedStyle(el).borderTopLeftRadius"
    )


def url(site, page):
    return (FIXTURES / site / page).as_uri()


def run(site, browser):
    home = url(site, "index.html")
    pages, unread = cross.crawl(browser, home, read=radius)
    walks = [cross.walk(browser, url(site, "book.html"), "main form")]
    phones = cross.phone_urls(browser, list(pages), DEVICES["phone"])
    return pages, unread, walks, phones


def swept(site):
    if site not in SITES:
        pages, unread, walks, phones = run(site, BROWSER)
        for _, reason in unread:
            child.raise_if_crashed(reason)
        SITES[site] = pages, unread, walks, phones
    return SITES[site]


def found(site, table=TABLE):
    pages, _, walks, phones = swept(site)
    return {
        f["id"]: f
        for f in cross.findings(
            table, pages, walks, phones=phones, home=url(site, "index.html")
        )
    }


def setUpModule():
    global BROWSER
    DEVICES["phone"] = cross.device(
        next(line.value for line in TABLE if line.check == "phone")
    )
    try:
        cross.device("Pixel 77")
    except cross.TableError as exc:
        DEVICES["unknown"] = exc
    BROWSER = OPEN.enter_context(runner.chromium())


def tearDownModule():
    OPEN.close()


def faults(site):
    marked = set()
    for page in (FIXTURES / site).rglob("*.html"):
        for line in page.read_text().splitlines():
            if "<!-- fault: " in line:
                marked.add(line.split("<!-- fault: ")[1].split(":")[0])
    return marked


class TheFixtures(unittest.TestCase):
    def test_the_fault_site_plants_one_fault_for_each_record_the_table_checks_306(self):
        self.assertEqual(faults("site-fault"), set(RECORDS))
        self.assertEqual(faults("site-clean"), set())

    def test_every_record_fails_on_the_fault_site_with_one_miss_on_the_marked_page(
        self,
    ):
        got = found("site-fault")
        where = {
            "vault.one-site": ("phone", "index.html", "m/index.html"),
            "vault.nav-order": ("order", "rooms.html", "orders Home, About, Rooms"),
            "vault.multiple-ways": (
                "ways",
                "faq.html",
                "reached 1 way(s) (navigation)",
            ),
            "vault.prefilled-repeat": (
                "repeat",
                "book-2.html?",
                "#again (email) arrives as ''",
            ),
        }
        for record, (check, page, what) in where.items():
            with self.subTest(record):
                f = got[record]
                self.assertEqual(f["answer"], "fail")
                self.assertEqual(len(f["misses"]), 1, f["misses"])
                miss = f["misses"][0]
                self.assertEqual(miss["check"], check)
                self.assertIn(f"/site-fault/{page}", miss["page"])
                self.assertIn(what, miss["what"])
        back = got["vault.flow-back"]
        self.assertEqual(back["answer"], "fail")
        self.assertEqual(
            {m["page"] for m in back["misses"]}, {url("site-fault", "book.html")}
        )
        self.assertEqual(
            sorted(m["what"].split(" as ")[0] for m in back["misses"]),
            ["Back shows #email", "Back shows #name"],
        )

    def test_the_clean_site_passes_every_record(self):
        got = found("site-clean")
        self.assertEqual(
            {r: f["answer"] for r, f in got.items()}, dict.fromkeys(RECORDS, "pass")
        )
        for f in got.values():
            self.assertEqual((f["misses"], f["unjudged"]), ([], []))

    def test_the_crawl_reaches_every_linked_page_and_no_unlinked_one(self):
        pages, unread, _, _ = swept("site-fault")
        names = sorted(u.rsplit("/site-fault/", 1)[1] for u in pages)
        self.assertEqual(
            names,
            [
                "about.html",
                "book.html",
                "contact.html",
                "faq.html",
                "index.html",
                "rooms.html",
            ],
        )
        self.assertEqual(unread, [])
        self.assertFalse(any("outside.html" in u for u in pages))

    def test_the_crawl_hands_each_page_to_a_caller_s_read(self):
        pages, _, _, _ = swept("site-fault")
        steps = {u.rsplit("/", 1)[1]: p["read"] for u, p in pages.items()}
        self.assertEqual(steps.pop("rooms.html"), "12px")
        self.assertEqual(set(steps.values()), {"8px"})

    def test_the_flow_walks_both_steps_and_presses_no_back_after_the_last_submit(self):
        _, _, walks, _ = swept("site-clean")
        w = walks[0]
        self.assertEqual(w.ended, cross.LAST_SUBMIT)
        self.assertEqual(
            [s.url.rsplit("/", 1)[1].split("?")[0] for s in w.steps],
            ["book.html", "book-2.html"],
        )
        self.assertIsNotNone(w.steps[0].back)
        self.assertIsNone(w.steps[1].back)
        self.assertEqual(
            w.steps[1].arrived[0][1:], ("email", w.steps[0].typed["#email"])
        )


class TheTableGivesTheValues(unittest.TestCase):
    def table(self, old, new):
        self.assertIn(old, TABLE_TEXT)
        return cross.parse(TABLE_TEXT.replace(old, new))

    def test_a_lower_ways_bar_passes_the_page_with_one_way(self):
        got = found("site-fault", self.table("ways | >= 2", "ways | >= 1"))
        self.assertEqual(got["vault.multiple-ways"]["answer"], "pass")

    def test_the_home_hub_size_lets_a_small_site_pass_and_no_larger(self):
        six = found("site-fault", self.table("pages <= 4", "pages <= 6"))
        self.assertEqual(six["vault.multiple-ways"]["answer"], "pass")
        five = found("site-fault", self.table("pages <= 4", "pages <= 5"))
        self.assertEqual(five["vault.multiple-ways"]["answer"], "fail")

    def test_a_record_with_no_line_in_the_table_is_not_checked(self):
        table = cross.parse("vault.nav-order | order\n")
        self.assertEqual(
            [f["id"] for f in cross.findings(table, {}, [], phones=None, home="x")],
            ["vault.nav-order"],
        )

    def test_a_check_given_two_values_is_refused_unlike_one_value_twice(self):  # #568
        with self.assertRaisesRegex(
            cross.TableError,
            r"'vault.b \| ways \| >= 1': ways is already given a different value by "
            r"'vault.a \| ways \| >= 2'",
        ):
            cross.parse("vault.a | ways | >= 2\nvault.b | ways | >= 1")
        self.assertEqual(
            len(cross.parse("vault.a | ways | >= 2\nvault.b | ways | >= 2")), 2
        )

    def test_every_record_naming_a_check_is_judged_once(self):  # #568
        table = cross.parse("vault.a | back\nvault.b | back\nvault.b | back")
        s = step("s1", {"#a": "x"}, [("#a", "", "")], back_url="home", held={"#a": "x"})
        got = cross.findings(
            table, {}, [cross.Walk("s1", [s], "end")], phones=None, home="h"
        )
        self.assertEqual(
            [(f["id"], [m["what"] for m in f["misses"]]) for f in got],
            [
                ("vault.a", ["Back went to home, not this step"]),
                ("vault.b", ["Back went to home, not this step"]),
            ],
        )

    def test_the_phone_line_names_the_device_it_loads_as(self):
        self.assertEqual(DEVICES["phone"]["is_mobile"], True)
        self.assertIn(
            "no device 'Pixel 77'; the nearest it knows: Pixel 7",
            str(DEVICES["unknown"]),
        )

    def test_a_malformed_line_is_refused(self):
        for text, why in [
            ("vault.a | hover", "no check 'hover'"),
            ("vault.a | ways", "ways wants a value"),
            ("vault.a | ways | > 2", "ways wants a value"),
            ("vault.a | order | same", "order reads no value"),
            ("vault.a", "want ID | CHECK"),
            (
                "vault.a | ways | >= 2\nvault.b | home-hub | pages <= 4",
                "home-hub relaxes its own record's ways line, and vault.b has none",
            ),
            ("# only a comment", "no lines"),
        ]:
            with self.subTest(text), self.assertRaisesRegex(cross.TableError, why):
                cross.parse(text)


def page(url, navs=(), links=(), search=False):
    return {
        "url": url,
        "navs": [list(n) for n in navs],
        "links": list(links),
        "search": search,
        "mobile": [],
    }


def link(href, nav=False):
    return {"href": href, "nav": nav}


ORDER = cross.parse("vault.order | order")
WAYS = cross.parse("vault.ways | ways | >= 2\nvault.ways | home-hub | pages <= 4")
FLOW = cross.parse("vault.back | back\nvault.repeat | repeat")


def answer(table, pages=None, walks=(), home="h"):
    return cross.findings(table, pages or {}, list(walks), phones=None, home=home)[0]


class TheOrderCheck(unittest.TestCase):
    def test_items_added_or_removed_keep_the_shared_order(self):
        pages = {
            "a": page("a", [["1", "2", "3"]]),
            "b": page("b", [["1", "x", "3"]]),
            "c": page("c", [["1", "2"]]),
        }
        self.assertEqual(answer(ORDER, pages)["answer"], "pass")

    def test_a_navigation_sharing_under_two_targets_is_not_compared(self):
        pages = {"a": page("a", [["1", "2"]]), "b": page("b", [["2", "9"]])}
        self.assertEqual(answer(ORDER, pages)["answer"], "no match")

    def test_each_navigation_meets_the_one_it_shares_most_with(self):
        pages = {
            "a": page("a", [["1", "2", "3"]]),
            "b": page("b", [["1", "9"], ["1", "2", "3"]]),
        }
        self.assertEqual(answer(ORDER, pages)["answer"], "pass")

    def test_a_pagination_s_moving_previous_and_next_are_not_shared_items(self):
        def pages_nav(prev, nxt, numbers):
            return [
                f"Previous -> {prev}",
                *(f"{n} -> p{n}" for n in numbers),
                f"Next -> {nxt}",
            ]

        pages = {
            "p4": page("p4", [pages_nav("p3", "p5", [1, 2, 3, 5])]),
            "p2": page("p2", [pages_nav("p1", "p3", [1, 3, 4, 5])]),
        }
        self.assertEqual(answer(ORDER, pages)["answer"], "pass")

    def test_a_page_out_of_order_is_named_once(self):
        pages = {u: page(u, [["1", "2", "3"]]) for u in "abcd"}
        pages["b"] = page("b", [["2", "1", "3"]])
        got = answer(ORDER, pages)
        self.assertEqual([m["page"] for m in got["misses"]], ["b"])


class TheWaysCheck(unittest.TestCase):
    def site(self, n, **extra):
        pages = {f"p{i}": page(f"p{i}") for i in range(n)}
        pages.update(extra)
        return pages

    def test_a_link_from_the_page_itself_is_no_way_to_it(self):
        pages = self.site(5, p1=page("p1", links=[link("p1", nav=True), link("p1")]))
        misses = {m["page"] for m in answer(WAYS, pages)["misses"]}
        self.assertIn("p1", misses)

    def test_navigation_and_another_link_are_two_ways(self):
        pages = self.site(
            5,
            p0=page("p0", links=[link("p1", nav=True)]),
            p2=page("p2", links=[link("p1")]),
        )
        misses = {m["page"] for m in answer(WAYS, pages)["misses"]}
        self.assertNotIn("p1", misses)

    def test_two_navigation_links_are_one_way(self):
        pages = self.site(
            5,
            p0=page("p0", links=[link("p1", nav=True)]),
            p2=page("p2", links=[link("p1", nav=True)]),
        )
        self.assertIn("p1", {m["page"] for m in answer(WAYS, pages)["misses"]})

    def test_a_search_anywhere_is_a_way_to_every_page(self):
        pages = self.site(
            5,
            p0=page(
                "p0", links=[link(f"p{i}", nav=True) for i in range(5)], search=True
            ),
        )
        for p in list(pages):
            pages[p]["links"] = pages[p]["links"] or [link("p0", nav=True)]
        self.assertEqual(answer(WAYS, pages)["misses"], [])

    def test_a_flow_step_is_exempt(self):
        step = cross.Step("p1", {}, [], None)
        pages = self.site(5)
        got = answer(WAYS, pages, walks=[cross.Walk("p3", [step], "done")], home="p0")
        self.assertEqual({m["page"] for m in got["misses"]}, {"p0", "p2", "p4"})

    def test_the_home_hub_holds_on_a_small_site_for_a_page_linked_both_ways(self):
        pages = {
            "h": page("h", links=[link("a", nav=True)]),
            "a": page("a", links=[link("h", nav=True)]),
        }
        got = answer(WAYS, pages)
        self.assertEqual([m["page"] for m in got["misses"]], ["h"])

    def test_the_home_hub_needs_the_page_to_link_back(self):
        # "links from and to the home page": https://www.w3.org/WAI/WCAG22/Understanding/multiple-ways.html
        pages = {"h": page("h", links=[link("a", nav=True)]), "a": page("a")}
        self.assertIn("a", {m["page"] for m in answer(WAYS, pages)["misses"]})

    def test_the_home_hub_needs_the_home_page_to_link_every_page(self):
        pages = {
            "h": page("h", links=[link("a", nav=True)]),
            "a": page("a", links=[link("h", nav=True)]),
            "b": page("b", links=[link("h", nav=True)]),
        }
        self.assertIn("a", {m["page"] for m in answer(WAYS, pages)["misses"]})

    def test_the_home_hub_relaxes_its_own_records_ways_line_and_no_other(self):  # #572
        table = cross.parse(
            "vault.x | ways | >= 2\n"
            "vault.x | home-hub | pages <= 4\n"
            "vault.y | ways | >= 2"
        )
        pages = {
            "h": page("h", links=[link("a", nav=True)]),
            "a": page("a", links=[link("h", nav=True)]),
        }
        got = {
            f["id"]: {m["page"] for m in f["misses"]}
            for f in cross.findings(table, pages, [], phones=None, home="h")
        }
        self.assertEqual(got, {"vault.x": {"h"}, "vault.y": {"h", "a"}})


def step(url, typed, arrived, *, back_url=None, held=None):
    back = (
        None
        if back_url is None
        else {
            "url": back_url,
            "fields": [{"key": k, "value": v} for k, v in (held or {}).items()],
        }
    )
    return cross.Step(url, typed, arrived, back)


class TheFlowChecks(unittest.TestCase):
    def test_back_to_another_page_misses(self):
        s = step("s1", {"#a": "x"}, [("#a", "", "")], back_url="home", held={"#a": "x"})
        got = cross.findings(
            FLOW, {}, [cross.Walk("s1", [s], "end")], phones=None, home="h"
        )[0]
        self.assertEqual(
            [m["what"] for m in got["misses"]], ["Back went to home, not this step"]
        )

    def test_back_with_a_fragment_on_the_step_url_is_the_step(self):
        s = step(
            "s1", {"#a": "x"}, [("#a", "", "")], back_url="s1#top", held={"#a": "x"}
        )
        self.assertEqual(
            cross.findings(
                FLOW, {}, [cross.Walk("s1", [s], "end")], phones=None, home="h"
            )[0]["answer"],
            "pass",
        )

    def test_a_flow_that_stops_at_its_first_step_is_not_judged(self):
        s = step("s1", {"#a": "x"}, [("#a", "", "")])
        back, repeat = cross.findings(
            FLOW,
            {},
            [cross.Walk("s1", [s], "a submit that did not move on")],
            phones=None,
            home="h",
        )
        for got in (back, repeat):
            self.assertEqual(got["answer"], "not judged")
            self.assertIn("a submit that did not move on", got["unjudged"][0]["what"])

    def repeat(self, first_token, later_token, later_value):
        s1 = step(
            "s1",
            {"#a": "v"},
            [("#a", first_token, "")],
            back_url="s1",
            held={"#a": "v"},
        )
        s2 = step("s2", {}, [("#b", later_token, later_value)])
        return cross.findings(
            FLOW, {}, [cross.Walk("s1", [s1, s2], "end")], phones=None, home="h"
        )[1]

    def test_a_repeated_token_must_arrive_holding_the_earlier_value(self):
        self.assertEqual(self.repeat("email", "email", "v")["answer"], "pass")
        self.assertEqual(self.repeat("email", "EMAIL", "")["answer"], "fail")

    def test_tokens_that_differ_by_section_or_mode_are_not_compared(self):
        self.assertEqual(
            self.repeat("shipping street-address", "billing street-address", "")[
                "answer"
            ],
            "no match",
        )
        self.assertEqual(
            self.repeat("section-a email", "section-b email", "")["answer"], "no match"
        )

    def test_on_off_and_bare_detail_words_are_no_token(self):
        for token in ("on", "off", "shipping", ""):
            with self.subTest(token):
                self.assertEqual(self.repeat(token, token, "")["answer"], "no match")


class ThePhoneAndSiteChecks(unittest.TestCase):
    def test_a_page_naming_a_separate_mobile_page_misses_though_it_stays_put(self):
        table = cross.parse("vault.one-site | phone | Pixel 7")
        got = cross.findings(
            table, {}, [], phones={"a": ("a", ["m"]), "b": ("b", [])}, home="a"
        )[0]
        self.assertEqual(
            [(m["page"], m["what"]) for m in got["misses"]],
            [("a", "names a separate mobile page, m")],
        )

    def test_the_site_is_the_home_origin_or_the_home_folder_and_below(self):
        home = "file:///s/site/index.html"
        for url, on in [
            ("file:///s/site/rooms.html", True),
            ("file:///s/site/m/index.html", True),
            ("file:///s/other/index.html", False),
            ("https://example.com/", False),
        ]:
            with self.subTest(url):
                self.assertEqual(cross.on_site(home, url), on)
        web = "https://a.example/index.html"
        for url, on in [
            ("https://a.example/x/rooms", True),
            ("http://a.example/rooms", False),
            ("https://b.example/rooms", False),
            ("file:///a.example/rooms", False),
        ]:
            with self.subTest(url):
                self.assertEqual(cross.on_site(web, url), on)


class TheCommandLine(unittest.TestCase):
    def main(self, *argv):
        done = child.run(
            [sys.executable, SCRIPT, *map(str, argv)],
            timeout=CLI_TIMEOUT_S,
        )
        return done.returncode, done.stdout, done.stderr

    def test_the_fault_site_exits_1_and_writes_its_findings(self):
        with tempfile.TemporaryDirectory() as out:
            stale = pathlib.Path(out, "cross.json")
            stale.write_text("{}")
            site = FIXTURES / "site-fault"
            code, printed, _ = self.main(
                site / "index.html",
                "--flow",
                site / "book.html",
                "--form",
                "main form",
                "--out",
                out,
            )
            self.assertEqual(code, 1)
            written = json.loads(stale.read_text())
            self.assertEqual(written["answers"], dict.fromkeys(RECORDS, "fail"))
            for record in RECORDS:
                self.assertIn(f"{record}: fail", printed)

    def test_a_site_with_no_miss_exits_0(self):
        with tempfile.TemporaryDirectory() as out:
            table = pathlib.Path(out, "order.table")
            table.write_text("vault.nav-order | order\n")
            code, printed, _ = self.main(
                FIXTURES / "site-clean" / "index.html", "--table", table, "--out", out
            )
            self.assertEqual(code, 0, printed)
            self.assertIn("vault.nav-order: pass", printed)

    def test_a_bad_table_exits_2(self):
        with tempfile.TemporaryDirectory() as out:
            bad = pathlib.Path(out, "bad.table")
            bad.write_text("vault.a | hover\n")
            code, _, err = self.main(
                FIXTURES / "site-clean" / "index.html", "--table", bad, "--out", out
            )
            self.assertEqual(code, 2)
            self.assertIn(
                "no check 'hover'; the checks are phone, order, ways, home-hub, back, repeat",
                err,
            )

    def test_an_unknown_device_exits_2(self):
        with tempfile.TemporaryDirectory() as out:
            bad = pathlib.Path(out, "bad.table")
            bad.write_text("vault.a | phone | Nokia 3310\n")
            code, _, err = self.main(
                FIXTURES / "site-clean" / "index.html", "--table", bad, "--out", out
            )
            self.assertEqual(code, 2)
            self.assertIn("no device 'Nokia 3310'; the nearest it knows: ", err)

    def test_a_missing_home_page_exits_2(self):
        with tempfile.TemporaryDirectory() as out:
            code, _, err = self.main(FIXTURES / "nowhere.html", "--out", out)
            self.assertEqual(code, 2)
            self.assertIn("no such file", err)


if __name__ == "__main__":
    child.main()
