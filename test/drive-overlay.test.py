"""Tests plugin/skills/design-round/scripts/drive-overlay.py (#303): python3 test/drive-overlay.test.py

Lose the settle and the fading panel reads shut while it opens; lose the trial and a dialog only a script
opens is never found. One browser serves the module and each test opens a
fresh page in it, so no test sees another's open overlay; the driver's trial cache does outlive a test, so a
test that watches the trial clears it first.
"""

import importlib.util
import inspect
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from playwright.sync_api import Browser

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

FIXTURE = pathlib.Path(HERE, "fixtures", "drivers", "overlay.html").resolve().as_uri()
AT_LOAD = (
    pathlib.Path(HERE, "fixtures", "drivers", "overlay-at-load.html").resolve().as_uri()
)
TOUCH = (
    pathlib.Path(HERE, "fixtures", "drivers", "overlay-touch.html").resolve().as_uri()
)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


flow = load(
    "check_flow",
    os.path.join(
        HERE, "..", "plugin", "skills", "design-round", "scripts", "check-flow.py"
    ),
)
overlay = load(
    "drive_overlay",
    os.path.join(
        HERE, "..", "plugin", "skills", "design-round", "scripts", "drive-overlay.py"
    ),
)

# trigger id: (kind, whether markup names its target, the close control's id, or None for none)
TRIGGERS = {
    "drawer-button": ("disclosure", True, "drawer-button"),
    "side-button": ("disclosure", True, "side-button"),
    "menu-button": ("menu", True, "menu-button"),
    "dialog-button": ("dialog", False, "dialog-close"),
    "command-button": ("dialog", True, "command-close"),
    "notice-button": ("dialog", True, None),
    "popover-button": ("popover", True, "popover-close"),
    "summary": ("details", True, "summary"),
    "panel-button": ("disclosure", False, "panel-close"),
    "sort-button": ("disclosure", False, "sort-button"),
}
BROWSER = flow.chromium()
# The phone band's first screen, measured at 390x664 (#197).
PHONE = {"width": 390, "height": 664}
LEFT_OUT = {
    *overlay.TRIAL_LEAVES_OUT,
    "proxy",
    "storage_state",
    "default_browser_type",
    "record_har_path",
    "record_har_omit_content",
    "record_har_url_filter",
    "record_har_mode",
    "record_har_content",
    "record_video_dir",
    "record_video_size",
}


def setUpModule():
    global browser
    browser = BROWSER.__enter__()


def tearDownModule():
    BROWSER.__exit__(None, None, None)


def key(ov):
    return (ov.trigger or ov.target).get_attribute("id")


class Driver(unittest.TestCase):
    def setUp(self):
        self.page = browser.new_page()
        self.page.goto(FIXTURE)
        self.found = {key(ov): ov for ov in overlay.find(self.page)}

    def tearDown(self):
        self.page.close()

    def control_id(self, state):
        return (
            state["control"].split("#", 1)[1].split(" ", 1)[0]
            if state["control"]
            else None
        )

    def test_find_lists_each_trigger_once_then_what_opened_by_itself(self):
        got = {i: (ov.kind, ov.declared) for i, ov in self.found.items()}
        self.assertEqual(
            got,
            {**{i: e[:2] for i, e in TRIGGERS.items()}, "welcome": ("dialog", False)},
        )
        self.assertEqual(
            list(self.found)[-3:], ["sort-button", "dialog-button", "welcome"]
        )

    def test_the_trial_leaves_the_callers_page_as_it_loaded(self):
        overlay._trials.clear()
        overlay.find(self.page)
        self.assertEqual(self.page.url, FIXTURE)
        self.assertEqual(self.page.text_content("#like"), "Like")
        self.assertTrue(self.page.evaluate("document.getElementById('sheet').hidden"))
        self.assertEqual(
            self.page.evaluate(
                "[...document.querySelectorAll('dialog[open]')].map((d) => d.id)"
            ),
            ["welcome"],
        )

    def test_find_within_an_element_lists_only_its_triggers_and_a_second_summary_is_none(
        self,
    ):
        overlay.open(self.page, self.found["summary"])
        got = overlay.find(self.page, within=self.page.query_selector("details"))
        self.assertEqual([key(ov) for ov in got], ["summary"])

    def test_a_modal_open_at_load_is_listed_and_shut_on_the_trial_page_before_it_tries(
        self,
    ):
        page = browser.new_page()
        self.addCleanup(page.close)
        page.goto(AT_LOAD)
        got = {key(ov): (ov.kind, ov.declared) for ov in overlay.find(page)}
        self.assertEqual(
            got, {"rooms-button": ("dialog", False), "cookies": ("dialog", False)}
        )

    def test_a_button_that_only_shuts_an_open_overlay_is_no_trigger(self):
        for trigger in ("popover-button", "command-button", "dialog-button"):
            with self.subTest(trigger=trigger):
                ov = self.found[trigger]
                overlay.open(self.page, ov)
                self.assertEqual(overlay.find(self.page, within=ov.target), [])
                overlay.close(self.page, ov)

    def test_a_trigger_inside_a_shut_menu_is_listed_only_once_the_menu_is_open(self):
        ov = self.found["menu-button"]
        self.assertNotIn("move", self.found)
        self.assertNotIn("report", self.found)
        overlay.open(self.page, ov)
        got = overlay.find(self.page, within=ov.target)
        self.assertEqual(
            [(key(o), o.kind, o.declared) for o in got],
            [("move", "menu", False), ("report", "dialog", False)],
        )
        state = overlay.open(self.page, got[1])
        self.assertEqual(
            (state["open"], got[1].target.get_attribute("id")), (True, "report-dialog")
        )

    def test_each_overlay_opens_by_click_and_by_keyboard(self):
        for trigger, (_, _, control) in TRIGGERS.items():
            for by in ("click", "keyboard"):
                with self.subTest(trigger=trigger, by=by):
                    ov = self.found[trigger]
                    self.assertFalse(overlay.read(self.page, ov)["open"])
                    state = overlay.open(self.page, ov, by=by)
                    self.assertEqual((state["open"], state["settled"]), (True, True))
                    overlay.close(self.page, ov, by="click" if control else "escape")

    def test_each_overlay_closes_by_its_control_clicked_and_keyed(self):
        for trigger, (_, _, control) in TRIGGERS.items():
            for by in ("click", "keyboard"):
                with self.subTest(trigger=trigger, by=by):
                    ov = self.found[trigger]
                    overlay.open(self.page, ov)
                    state = overlay.close(self.page, ov, by=by)
                    self.assertEqual(self.control_id(state), control)
                    self.assertEqual(state["open"], control is None)
                    if control is None:
                        overlay.close(self.page, ov, by="escape")

    def test_escape_closes_each_but_the_details_which_a_page_must_script_to(self):
        for trigger in TRIGGERS:
            with self.subTest(trigger=trigger):
                ov = self.found[trigger]
                overlay.open(self.page, ov, by="keyboard")
                state = overlay.close(self.page, ov, by="escape")
                self.assertEqual(state["open"], trigger == "summary")
                self.assertIsNone(state["control"])
                if state["open"]:
                    overlay.close(self.page, ov, by="click")

    def test_a_dialog_open_at_load_is_read_and_closed_but_never_opened(self):
        ov = self.found["welcome"]
        self.assertIsNone(ov.trigger)
        self.assertEqual(overlay.read(self.page, ov)["open"], True)
        with self.assertRaises(ValueError):
            overlay.open(self.page, ov)
        state = overlay.close(self.page, ov, by="click")
        self.assertEqual(
            (state["open"], self.control_id(state), state["expanded"]),
            (False, "welcome-close", None),
        )

    def test_a_menu_opened_by_keyboard_takes_focus_and_sets_aria_expanded(self):
        ov = self.found["menu-button"]
        state = overlay.open(self.page, ov, by="keyboard", key="ArrowDown")
        self.assertEqual(
            (state["open"], state["expanded"], state["focus_inside"]),
            (True, "true", True),
        )
        self.assertEqual(state["focus"], 'li "Rename"')
        state = overlay.close(self.page, ov, by="escape")
        self.assertEqual(
            (state["open"], state["expanded"], state["focus_inside"]),
            (False, "false", False),
        )
        self.assertEqual(state["focus"], 'button#menu-button "Actions"')

    def test_focus_on_a_details_summary_is_not_inside_what_it_opened(self):
        state = overlay.open(self.page, self.found["summary"], by="keyboard")
        self.assertEqual((state["open"], state["focus_inside"]), (True, False))

    def test_a_modal_dialog_reads_modal_and_a_popover_does_not(self):
        self.assertTrue(overlay.open(self.page, self.found["dialog-button"])["modal"])
        overlay.close(self.page, self.found["dialog-button"])
        self.assertFalse(overlay.open(self.page, self.found["popover-button"])["modal"])

    def test_a_target_no_markup_names_is_what_its_first_open_draws(self):
        ov = self.found["panel-button"]
        self.assertIsNone(ov.target)
        overlay.open(self.page, ov)
        self.assertEqual(ov.target.get_attribute("id"), "panel")

    def test_of_what_a_first_open_draws_an_overlay_role_beats_a_larger_element(self):
        ov = self.found["sort-button"]
        overlay.open(self.page, ov)
        self.assertEqual(ov.target.get_attribute("id"), "sort-list")

    def test_a_fading_panel_reads_open_and_shut_only_once_its_fade_ends(self):
        ov = self.found["panel-button"]
        opacity = "getComputedStyle(document.getElementById('panel')).opacity"
        self.assertTrue(overlay.open(self.page, ov)["open"])
        self.assertEqual(self.page.evaluate(opacity), "1")
        self.assertFalse(overlay.close(self.page, ov, by="escape")["open"])
        self.assertEqual(self.page.evaluate(opacity), "0")


class TrialUnderCallerOptions(unittest.TestCase):
    def opened(self, resize=False, **options):
        context = browser.new_context(**options)
        self.addCleanup(context.close)
        page = context.new_page()
        if resize:
            page.set_viewport_size(PHONE)
        page.goto(TOUCH)
        return {key(ov): ov.target.get_attribute("id") for ov in overlay.find(page)}

    def test_an_opener_drawn_for_touch_alone_is_found_at_phone_width_and_kept_apart(
        self,
    ):
        overlay._trials.clear()
        both = {"info-button": "info", "map-button": "map"}
        self.assertEqual(self.opened(viewport=PHONE), both)
        self.assertEqual(
            self.opened(viewport=PHONE, has_touch=True), {"book-button": "book", **both}
        )

    def test_the_trial_takes_the_pages_viewport_where_the_caller_resized_it(self):
        overlay._trials.clear()
        self.assertEqual(self.opened(), {"info-button": "info"})
        self.assertEqual(
            self.opened(resize=True), {"info-button": "info", "map-button": "map"}
        )

    def test_every_option_the_caller_set_reaches_the_trial_context(self):
        options = dict(
            viewport=PHONE,
            screen={**PHONE, "height": 844},
            ignore_https_errors=True,
            java_script_enabled=False,
            bypass_csp=True,
            user_agent="trial-test",
            locale="de-DE",
            timezone_id="Europe/Berlin",
            geolocation={"latitude": 52.5, "longitude": 13.4},
            permissions=["geolocation"],
            extra_http_headers={"X-Trial": "1"},
            offline=True,
            http_credentials={"username": "u", "password": "p"},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True,
            color_scheme="dark",
            reduced_motion="reduce",
            forced_colors="active",
            contrast="more",
            base_url="http://localhost/",
            strict_selectors=True,
            service_workers="block",
        )
        folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, folder)
        cert, private = (os.path.join(folder, n) for n in ("c.pem", "k.pem"))
        subprocess.run(
            ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes"]
            + ["-keyout", private, "-out", cert, "-days", "1", "-subj", "/CN=t"],
            check=True,
            capture_output=True,
        )
        options["client_certificates"] = [
            {"origin": "https://localhost", "certPath": cert, "keyPath": private}
        ]

        left = {n.replace("_", "") for n in overlay.TRIAL_LEAVES_OUT}

        def held(context):
            return {
                k: v
                for k, v in context._impl_obj._options.items()
                if k.lower() not in left
            }

        no_viewport = {"no_viewport": True, "color_scheme": "null"}
        self.assertEqual(
            set(options) | set(no_viewport) | LEFT_OUT,
            set(inspect.signature(Browser.new_context).parameters) - {"self"},
        )
        for given in (options, no_viewport):
            with self.subTest(given=sorted(given)):
                context = browser.new_context(**given)
                self.addCleanup(context.close)
                carried = overlay._trial_options(context.new_page())
                trial = browser.new_context(**carried)
                self.addCleanup(trial.close)
                self.assertEqual(held(trial), held(context))  # #552


if __name__ == "__main__":
    child.main()
