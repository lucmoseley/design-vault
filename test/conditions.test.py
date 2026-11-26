"""Pins conditions.py (#304): python3 test/conditions.test.py

It is a suite of the commit gate (test/all.sh): loosening it lets a family
script read a page it believes is in forced colours, dark, print, another
locale, right-to-left, under a coarse pointer or with scripts blocked, when
the page loaded plain. Each condition is read on the fixture both with it and
without it, so a condition that does nothing fails here.
"""

import contextlib
import os
import pathlib
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

FIXTURES = os.path.join(HERE, "fixtures", "drivers")
URL = pathlib.Path(FIXTURES, "conditions.html").resolve().as_uri()
# Any width past the fixture's 80 px logical box; the rtl box is read against it.
VIEWPORT = {"width": 400, "height": 300}


SCRIPTS = os.path.join(
    os.path.dirname(__file__), "..", "plugin", "skills", "design-round", "scripts"
)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

conditions = siblings.load(SCRIPTS, "conditions.py")
flow = siblings.load(SCRIPTS, "check-flow.py")
STACK = contextlib.ExitStack()
BROWSER = None


def setUpModule():
    global BROWSER
    BROWSER = STACK.enter_context(flow.chromium())


def tearDownModule():
    STACK.close()


def read(js, **given):
    with conditions.open_page(BROWSER, URL, viewport=VIEWPORT, **given) as page:
        return page.evaluate(js)


def style(selector, prop):
    return f"getComputedStyle(document.querySelector({selector!r})).{prop}"


class ForcedColours(unittest.TestCase):
    def test_drops_the_box_shadow(self):
        shadow = style("#shadow", "boxShadow")
        self.assertNotEqual(read(shadow), "none")
        self.assertEqual(read(shadow, forced_colours=True), "none")


class Scheme(unittest.TestCase):
    def test_dark_switches_the_custom_property(self):
        ground = "getComputedStyle(document.documentElement).getPropertyValue('--ground').trim()"
        self.assertEqual(read(ground), "rgb(255, 255, 255)")
        self.assertEqual(read(ground, scheme="light"), "rgb(255, 255, 255)")
        self.assertEqual(read(ground, scheme="dark"), "rgb(17, 17, 17)")


class Print(unittest.TestCase):
    def test_applies_the_print_rule(self):
        shown = style("#screen-only", "display")
        self.assertEqual(read(shown), "block")
        self.assertEqual(read(shown, print_media=True), "none")


class Locale(unittest.TestCase):
    def test_changes_intl_output(self):
        number = "document.getElementById('number').textContent"
        self.assertEqual(read(number, locale="en-US"), "1,234,567.5")
        self.assertEqual(read(number, locale="de-DE"), "1.234.567,5")


class RightToLeft(unittest.TestCase):
    BOX = "(() => { const r = document.getElementById('logical').getBoundingClientRect(); return [r.left, r.right]; })()"

    def test_mirrors_the_logical_margin(self):
        self.assertEqual(read(self.BOX), [30, 80])
        self.assertEqual(
            read(self.BOX, rtl=True), [VIEWPORT["width"] - 80, VIEWPORT["width"] - 30]
        )

    def test_the_page_reads_rtl_from_its_first_script(self):
        self.assertEqual(read("window.dirAtLoad"), "ltr")
        self.assertEqual(read("window.dirAtLoad", rtl=True), "rtl")


class Pointer(unittest.TestCase):
    COARSE = "matchMedia('(pointer: coarse)').matches"
    HEIGHT = "document.getElementById('target').getBoundingClientRect().height"

    def test_coarse_matches_pointer_coarse(self):
        self.assertTrue(read(self.COARSE, pointer="coarse"))
        self.assertEqual(read(self.HEIGHT, pointer="coarse"), 44)

    def test_fine_and_no_pointer_match_pointer_fine_not_coarse(self):
        for given in ({}, {"pointer": "fine"}):
            with self.subTest(**given):
                self.assertFalse(read(self.COARSE, **given))
                self.assertTrue(read("matchMedia('(pointer: fine)').matches", **given))
                self.assertEqual(read(self.HEIGHT, **given), 24)


class Block(unittest.TestCase):
    FALLBACK = "document.getElementById('fallback').hidden"
    PHOTO = "document.getElementById('photo').naturalWidth"

    def test_a_blocked_script_leaves_its_fallback_shown(self):
        self.assertTrue(read(self.FALLBACK))
        self.assertFalse(read(self.FALLBACK, block=("script",)))
        self.assertEqual(read(self.PHOTO, block=("script",)), 20)

    def test_scripts_off_shows_noscript_and_runs_no_script(self):
        noscript = "!!document.getElementById('noscript')"
        self.assertFalse(read(noscript))
        self.assertFalse(read(noscript, block=("script",)))
        self.assertTrue(read(noscript, scripts_off=True))
        self.assertIsNone(read("window.dirAtLoad ?? null", scripts_off=True))

    def test_a_blocked_image_does_not_load(self):
        self.assertEqual(read(self.PHOTO), 20)
        self.assertEqual(read(self.PHOTO, block=("image",)), 0)
        self.assertTrue(read(self.FALLBACK, block=("image",)))


class Combined(unittest.TestCase):
    def test_dark_rtl_and_coarse_hold_together_on_one_page(self):
        got = read(
            "[getComputedStyle(document.documentElement).getPropertyValue('--ground').trim(),"
            " document.documentElement.dir, matchMedia('(pointer: coarse)').matches]",
            scheme="dark",
            rtl=True,
            pointer="coarse",
        )
        self.assertEqual(got, ["rgb(17, 17, 17)", "rtl", True])

    def test_init_scripts_run_before_the_page(self):
        got = read("window.seen", init_scripts=("window.seen = document.readyState",))
        self.assertEqual(got, "loading")


class Refusals(unittest.TestCase):
    def test_names_the_value_it_cannot_emulate(self):
        for given, word in (
            ({"scheme": "sepia"}, "scheme"),
            ({"pointer": "pen"}, "pointer"),
            ({"locale": ""}, "locale"),
            ({"block": ("document",)}, "block"),
        ):
            # No browser: a refusal comes before it is touched.
            with self.subTest(**given), self.assertRaisesRegex(ValueError, word):
                with conditions.open_page(None, URL, **given):
                    pass


if __name__ == "__main__":
    child.main()
