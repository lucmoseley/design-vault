"""Pins drive-form.py (#302): python3 test/drive-form.test.py

Loosen the driver and a check that judges what a form does with bad input
reads the page before its errors show, reads a good value where a bad one was
meant, or misses that a submit went on to the next page: the state family's
checks (#312) and the cross-page probe (#306) then judge the wrong state.
"""

import contextlib
import http.server
import importlib.util
import os
import pathlib
import sys
import threading
import time
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path


def library(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


driver = library(
    "drive_form",
    os.path.join(
        HERE, "..", "plugin", "skills", "design-round", "scripts", "drive-form.py"
    ),
)
flow = library(
    "check_flow",
    os.path.join(
        HERE, "..", "plugin", "skills", "design-round", "scripts", "check-flow.py"
    ),
)
PAGE_FILE = pathlib.Path(HERE, "fixtures", "drivers", "form.html").resolve()
PAGE = PAGE_FILE.as_uri()
OPEN = contextlib.ExitStack()
BROWSER = None


def setUpModule():
    global BROWSER
    BROWSER = OPEN.enter_context(flow.chromium())


def tearDownModule():
    OPEN.close()


class OnThePage(unittest.TestCase):
    def setUp(self):
        self.page = BROWSER.new_page()
        self.addCleanup(self.page.close)
        self.page.goto(PAGE)

    def field(self, state, key):
        return next(f for f in state["fields"] if f["key"] == key)


class Fields(OnThePage):
    def test_lists_what_a_visitor_fills_and_a_radio_group_once(self):
        self.assertEqual(
            [f.key for f in driver.fields(self.page, "#book")],
            [
                "#given",
                "#email",
                "#tel",
                "#guests",
                "#arrive",
                "#room",
                'input[name="contact"]',
                "#ref",
                "#note",
                "#terms",
            ],
        )

    def test_reads_the_token_type_and_constraints(self):
        by_key = {f.key: f for f in driver.fields(self.page, "#book")}
        self.assertEqual(by_key["#tel"].token, "section-stay home tel")
        self.assertEqual((by_key["#guests"].min, by_key["#guests"].max), (1, 8))
        # The disabled placeholder is no choice, and the select stands on it.
        self.assertEqual(by_key["#room"].options, ["dorm", "private"])
        self.assertEqual(by_key["#room"].value, "")
        self.assertTrue(by_key['input[name="contact"]'].required)

    def test_the_first_form_when_none_is_named(self):
        self.assertEqual(driver.fields(self.page)[0].key, "#given")

    def test_refuses_a_form_the_page_lacks_and_names_it(self):
        with self.assertRaisesRegex(
            driver.FormError, "no element matches #nowhere"
        ) as caught:
            driver.fields(self.page, "#nowhere")
        self.assertEqual(caught.exception.what, ("#nowhere",))
        with self.assertRaisesRegex(driver.FormError, "#summary is not a form"):
            driver.fields(self.page, "#summary")


class Fill(OnThePage):
    def test_types_key_by_key(self):
        driver.fill(self.page, "#book")
        self.assertEqual(self.page.locator("#given").get_attribute("data-inputs"), "3")

    def test_plants_only_where_asked(self):
        typed = {t.key: t for t in driver.fill(self.page, "#book", bad=["#email"])}
        self.assertEqual(typed["#email"].value, "ada.lovelace@")
        self.assertEqual(typed["#email"].planted, "malformed email")
        self.assertFalse(typed["#email"].valid)
        self.assertEqual(
            typed["#given"], driver.Filled("#given", "Ada", None, True, None)
        )

    def test_a_token_with_section_and_detail_words_gives_its_field_name(self):
        typed = {t.key: t for t in driver.fill(self.page, "#book", bad=["#tel"])}
        self.assertEqual(typed["#tel"].value, "call me")

    def test_a_pattern_no_known_value_meets_is_left_and_said(self):
        typed = {t.key: t for t in driver.fill(self.page, "#book")}
        self.assertIsNone(typed["#ref"].value)
        self.assertIn("pass one in values", typed["#ref"].note)
        self.assertEqual(self.page.input_value("#ref"), "")

    def test_values_fill_what_the_driver_cannot(self):
        typed = {
            t.key: t for t in driver.fill(self.page, "#book", values={"#ref": "AB1234"})
        }
        self.assertEqual(typed["#ref"].value, "AB1234")
        self.assertTrue(typed["#ref"].valid)

    def test_values_are_fitted_to_a_maximum_length(self):
        typed = {t.key: t for t in driver.fill(self.page, "#book")}
        self.assertEqual(typed["#note"].value, "A short message for")

    def test_refuses_a_key_the_form_does_not_have_and_names_it(self):
        with self.assertRaisesRegex(
            driver.FormError, "no field #native-name"
        ) as caught:
            driver.fill(self.page, "#book", bad=["#native-name"])
        self.assertEqual(caught.exception.what, ("#native-name",))

    def test_refuses_one_key_given_as_a_bare_string(self):
        with self.assertRaisesRegex(TypeError, "not the string '#email'"):
            driver.fill(self.page, "#book", bad="#email")

    def test_a_value_the_browser_refuses_is_said(self):
        filled = {
            t.key: t
            for t in driver.fill(self.page, "#values", values={"#v-guests": "99"})
        }
        self.assertFalse(filled["#v-guests"].valid)
        self.assertIn("the browser refuses this value", filled["#v-guests"].note)

    def test_a_field_that_submits_on_change_ends_the_fill_there(self):
        filled = driver.fill(self.page, "#jumpy")
        self.assertEqual(
            filled,
            [
                driver.Filled(
                    "#jumpy-sort", "price", None, None, "setting it left the page"
                )
            ],
        )


class BadSubmit(OnThePage):
    """#book shows its errors 100 ms after the submit."""

    def setUp(self):
        super().setUp()
        driver.fill(self.page, "#book", bad=["#email"], values={"#ref": "AB1234"})
        self.settled = driver.submit(self.page, "#book")
        self.state = self.settled.state

    def test_stays_on_the_page_after_one_submit_event(self):
        self.assertFalse(self.settled.navigated)
        self.assertEqual(self.settled.submits, 1)
        self.assertEqual(self.settled.url, PAGE)

    def test_the_error_state_is_readable(self):
        email = self.field(self.state, "#email")
        self.assertTrue(email["invalid"])
        self.assertFalse(email["valid"])
        self.assertEqual(email["described"], [email["message"]])
        self.assertEqual(self.state["live"], [f"There is a problem {email['message']}"])

    def test_focus_is_readable(self):
        self.assertEqual(self.state["focus"]["id"], "summary")
        self.assertIsNone(self.state["focus"]["key"])

    def test_the_typed_values_are_readable(self):
        self.assertEqual(self.field(self.state, "#email")["value"], "ada.lovelace@")
        self.assertEqual(self.field(self.state, "#given")["value"], "Ada")
        self.assertEqual(
            self.field(self.state, 'input[name="contact"]')["value"], "email"
        )
        self.assertIs(self.field(self.state, "#terms")["value"], True)


class GoodSubmit(OnThePage):
    def test_reaches_the_next_page(self):
        driver.fill(self.page, "#book", values={"#ref": "AB1234"})
        settled = driver.submit(self.page, "#book")
        self.assertTrue(settled.navigated)
        self.assertEqual(settled.submits, 1)
        self.assertEqual(
            settled.url.split("?")[0], PAGE.replace("form.html", "form-next.html")
        )
        self.assertEqual(settled.state["live"], ["We have your booking."])

    def test_a_submit_in_the_next_document_is_counted(self):
        driver.fill(self.page, "#book", values={"#ref": "AB1234"})
        driver.submit(self.page, "#book")
        driver.fill(self.page, "#more")
        self.assertEqual(driver.submit(self.page, "#more").submits, 1)

    def test_a_second_submit_counts_from_itself(self):
        driver.fill(self.page, "#book", bad=["#email"])
        driver.submit(self.page, "#book")
        driver.fill(self.page, "#book", values={"#ref": "AB1234"})
        self.assertEqual(driver.submit(self.page, "#book").submits, 1)


class BrowserChecks(OnThePage):
    """#native leaves its checks to the browser, which stops the submit."""

    def test_a_blocked_submit_fires_no_submit_event_and_focuses_the_first_bad_field(
        self,
    ):
        typed = driver.fill(self.page, "#native", bad=driver.ALL)
        self.assertEqual([t.planted for t in typed], ["left empty", "malformed email"])
        settled = driver.submit(self.page, "#native")
        self.assertFalse(settled.navigated)
        self.assertEqual(settled.submits, 0)
        self.assertEqual(settled.state["focus"]["key"], "#native-name")
        self.assertEqual(
            self.field(settled.state, "#native-email")["value"], "ada.lovelace@"
        )


class HistoryPush(OnThePage):
    def test_an_error_shown_under_a_history_push_is_not_a_new_page(self):
        driver.fill(self.page, "#pushy")
        settled = driver.submit(self.page, "#pushy")
        self.assertFalse(settled.navigated)
        self.assertTrue(settled.url.endswith("form.html?error=1"))
        self.assertEqual(settled.state["live"], ["No beds match that search"])


class After(OnThePage):
    def test_an_action_that_keeps_the_document_reads_it_settled(self):
        state = driver.after(self.page, lambda: self.page.focus("#given"))
        self.assertTrue(state["kept"])
        self.assertEqual(state["focus"]["key"], "#given")

    def test_a_reload_reads_a_new_document(self):
        self.assertFalse(driver.after(self.page, self.page.reload)["kept"])


class Enter(OnThePage):
    def test_enter_in_the_last_line_submits_a_form_with_no_button(self):
        driver.fill(self.page, "#bare")
        settled = driver.submit(self.page, "#bare", by="enter")
        self.assertTrue(settled.navigated)
        self.assertEqual(settled.submits, 1)
        self.assertIn("form-next.html?q=dorm+bed", settled.url)

    def test_a_form_with_no_button_cannot_be_clicked(self):
        with self.assertRaisesRegex(driver.FormError, "no submit button"):
            driver.submit(self.page, "#bare")


class Late(http.server.SimpleHTTPRequestHandler):
    """Serves the fixtures, and answers #remote's POST twice the quiet window
    late, from a thread of its own, so only the request in flight keeps the
    driver waiting."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(PAGE_FILE), **kwargs)

    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        time.sleep(2 * driver.QUIET_MS / 1000)
        body = b"Thanks, you are signed up."
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class InFlight(unittest.TestCase):
    def test_a_request_still_in_flight_is_waited_for(self):
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Late)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        page = BROWSER.new_page()
        self.addCleanup(page.close)
        page.goto(f"http://127.0.0.1:{server.server_port}/form.html")
        driver.fill(page, "#remote")
        settled = driver.submit(page, "#remote")
        self.assertIn("Thanks, you are signed up.", settled.state["live"])


class Unsettled(OnThePage):
    def test_a_page_that_never_settles_times_out(self):
        from playwright.sync_api import TimeoutError as PlaywrightTimeout

        # Three quiet windows: a page that settles at all settles well inside them.
        limit = 3 * driver.QUIET_MS
        with self.assertRaisesRegex(PlaywrightTimeout, f"did not settle in {limit} ms"):
            driver.submit(self.page, "#busy", timeout=limit)


class Values(OnThePage):
    """The value fill() picks for each rule, on #values."""

    def setUp(self):
        super().setUp()
        self.good = {t.key: t for t in driver.fill(self.page, "#values")}
        self.page.reload()
        self.bad = {t.key: t for t in driver.fill(self.page, "#values", bad=driver.ALL)}

    def test_read_only_and_undrawn_fields_are_left_out(self):
        keys = [f.key for f in driver.fields(self.page, "#book")]
        self.assertNotIn("#booked", keys)
        self.assertNotIn("#later", keys)

    def test_a_token_s_field_name_comes_before_and_after_its_detail_words(self):
        self.assertEqual(self.good["#v-post"].value, "SW1A 1AA")
        self.assertEqual(
            (self.bad["#v-post"].value, self.bad["#v-post"].planted),
            ("SW1A", "malformed postal-code"),
        )
        self.assertEqual(self.good["#v-login"].value, "ada.lovelace")

    def test_a_type_with_its_own_syntax_outranks_the_token(self):
        self.assertEqual(self.good["#v-email"].value, "ada.lovelace@example.com")
        self.assertTrue(self.good["#v-email"].valid)
        self.assertEqual(self.good["#v-born"].value, "2030-06-15")

    def test_a_minimum_length_is_met_and_then_missed_by_one(self):
        self.assertEqual(self.good["#v-given"].value, "Adaxx")
        self.assertEqual(
            (self.bad["#v-given"].value, self.bad["#v-given"].planted),
            ("xxxx", "under its minimum length 5"),
        )
        self.assertFalse(self.bad["#v-given"].valid)

    def test_a_number_takes_its_minimum_and_breaks_its_maximum_first(self):
        self.assertEqual(self.good["#v-guests"].value, "3")
        self.assertEqual(self.bad["#v-guests"].planted, "over its maximum 8")
        self.assertEqual(self.bad["#v-guests"].value, "9")
        self.assertEqual(self.bad["#v-nights"].planted, "under its minimum 3")

    def test_a_required_field_with_nothing_else_to_break_is_left_empty(self):
        self.assertEqual(self.bad["#v-name"].planted, "left empty")
        self.assertEqual(self.bad["#v-born"].planted, "left empty")
        self.assertIsNone(self.bad["#v-extra"].value)
        self.assertIn("nothing to plant", self.bad["#v-extra"].note)

    def test_a_bad_value_its_pattern_accepts_is_not_planted(self):
        self.assertIsNone(self.bad["#v-any"].value)
        self.assertIn("its pattern .+ accepts '!!'", self.bad["#v-any"].note)

    def test_a_choice_is_left_unchosen_only_where_a_visitor_could(self):
        self.assertEqual(self.bad["#v-agree"].planted, "left unchosen")
        self.assertFalse(self.bad["#v-agree"].valid)
        self.assertIsNone(self.bad['input[name="v-meal"]'].value)
        self.assertIsNone(self.bad["#v-size"].value)
        self.assertEqual(self.good["#v-floor"].value, "1")


if __name__ == "__main__":
    child.main()
