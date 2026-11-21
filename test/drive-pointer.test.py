"""Tests plugin/skills/design-round/scripts/drive-pointer.py (#301): python3 test/drive-pointer.test.py

Lose the settle and a check reads a fading tooltip, a snapping knob or a parallax layer partway; lose the
cover check and it reads the state of whatever lies over its target. It drives a real Chromium on one
fixture page, since what it pins is what the browser does under a real mouse.
"""

import contextlib
import importlib.util
import os
import pathlib
import unittest

HERE = os.path.dirname(__file__)
CHILD = importlib.util.spec_from_file_location("child", os.path.join(HERE, "child.py"))
child = importlib.util.module_from_spec(CHILD)
CHILD.loader.exec_module(child)
PAGE = pathlib.Path(HERE, "fixtures", "drivers", "pointer.html").resolve().as_uri()


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
pointer = load(
    "drive_pointer",
    os.path.join(
        HERE, "..", "plugin", "skills", "design-round", "scripts", "drive-pointer.py"
    ),
)
OPEN = contextlib.ExitStack()
BROWSER = []


def setUpModule():
    BROWSER.append(OPEN.enter_context(flow.chromium()))


def tearDownModule():
    OPEN.close()


class OnThePage(unittest.TestCase):
    def setUp(self):
        self.page = BROWSER[0].new_page()
        self.addCleanup(self.page.close)
        self.page.goto(PAGE)

    def style(self, selector, prop):
        return self.page.eval_on_selector(
            selector, f"el => getComputedStyle(el).{prop}"
        )

    def knob_x(self):
        return self.page.evaluate(
            "() => document.getElementById('knob').getBoundingClientRect().left"
            " - document.getElementById('track').getBoundingClientRect().left"
        )


class Hover(OnThePage):
    def test_a_hover_only_tooltip_shows_faded_in_and_goes_on_leaving(self):
        self.assertEqual(self.style("#tip", "opacity"), "0")
        moved = pointer.hover(self.page, "#tip-trigger")
        self.assertTrue(moved.settled)
        self.assertEqual(
            (self.style("#tip", "opacity"), self.style("#tip", "visibility")),
            ("1", "visible"),
        )
        away = pointer.leave(self.page, "#tip-trigger")
        self.assertEqual(self.style("#tip", "opacity"), "0")
        # The trigger is at the top left, so the farthest corner is the bottom right.
        size = self.page.viewport_size
        self.assertEqual((away.x, away.y), (size["width"] - 1, size["height"] - 1))

    def test_a_tooltip_shown_after_a_delay_is_waited_for(self):
        pointer.hover(self.page, "#late-trigger")
        self.assertTrue(self.page.is_visible("#late-tip"))

    def test_returns_where_the_pointer_rests(self):
        box = self.page.locator("#tip-trigger").bounding_box()
        moved = pointer.hover(self.page, "#tip-trigger", at=(0, 1))
        self.assertEqual(
            (round(moved.x), round(moved.y)),
            (round(box["x"]), round(box["y"] + box["height"] - 1)),
        )

    def test_a_target_off_the_screen_is_scrolled_to_first(self):
        self.page.evaluate("scrollTo(0, 2000)")
        pointer.settle(self.page)
        pointer.hover(self.page, "#tip-trigger")
        self.assertEqual(self.style("#tip", "opacity"), "1")


class Press(OnThePage):
    def test_a_press_only_style_shows_while_held_and_goes_on_release(self):
        before = self.style("#press", "backgroundColor")
        pointer.press(self.page, "#press")
        held = self.style("#press", "backgroundColor")
        pointer.release(self.page)
        self.assertEqual(
            (before, held, self.style("#press", "backgroundColor")),
            ("rgb(240, 240, 240)", "rgb(0, 0, 128)", "rgb(240, 240, 240)"),
        )

    def test_a_click_lands_on_release_not_on_press(self):
        def clicks():
            return self.page.get_attribute("#count", "data-clicks")

        pointer.press(self.page, "#count")
        self.assertEqual(clicks(), "0")
        pointer.release(self.page)
        self.assertEqual(clicks(), "1")
        pointer.click(self.page, "#count")
        self.assertEqual(clicks(), "2")

    def test_a_click_on_a_moving_target_waits_for_it_to_come_to_rest(self):
        # #458: a point taken mid-motion lands on whatever moves under it. The still target's
        # pair is test_a_click_lands_on_release_not_on_press.
        self.page.evaluate("sendGlider()")
        pointer.click(self.page, "#glider")
        self.assertEqual(self.page.get_attribute("#glider", "data-clicked-at"), "400px")

    def test_a_click_that_leaves_the_page_is_read_on_the_next(self):
        self.assertTrue(pointer.click(self.page, "#next").settled)
        self.assertTrue(self.page.url.endswith("pointer.html?next"))


class Drag(OnThePage):
    def test_a_dragged_knob_is_read_once_it_has_snapped(self):
        self.assertEqual(self.knob_x(), 0)
        moved = pointer.drag(self.page, "#knob", (130, 0))
        self.assertTrue(moved.settled)
        self.assertEqual(self.knob_x(), 100)

    def test_a_drag_moves_once_a_frame_for_its_duration(self):
        pointer.drag(self.page, "#knob", (130, 0))
        moves, gap = self.page.eval_on_selector(
            "#knob", "el => [Number(el.dataset.moves), Number(el.dataset.gap)]"
        )
        self.assertEqual(moves, round(pointer.DRAG_MS / pointer.FRAME_MS))
        # The shortest gap, not the whole span: on a loaded machine moves sent back to back can still
        # span the drag. 1 ms off is slack for the event clock's rounding.
        self.assertGreaterEqual(gap, pointer.FRAME_MS - 1)

    def test_a_drag_held_is_read_where_the_pointer_is(self):
        pointer.drag(self.page, "#knob", (130, 0), hold=True)
        self.assertEqual(self.knob_x(), 130)
        pointer.release(self.page)
        self.assertEqual(self.knob_x(), 100)

    def test_a_drag_to_an_element_ends_on_its_centre(self):
        # #veil covers #covered, which a drop point may be.
        moved = pointer.drag(self.page, "#knob", "#covered", hold=True)
        box = self.page.locator("#covered").bounding_box()
        self.assertEqual(
            (round(moved.x), round(moved.y)),
            (
                round(box["x"] + (box["width"] - 1) / 2),
                round(box["y"] + (box["height"] - 1) / 2),
            ),
        )

    def test_refuses_a_drop_point_off_the_screen(self):
        with self.assertRaisesRegex(pointer.PointerError, "p#bottom is off the screen"):
            pointer.drag(self.page, "#knob", "#bottom")


class Wheel(OnThePage):
    def layer_y(self):
        return self.page.evaluate(
            "() => new DOMMatrix(getComputedStyle(layer).transform).m42"
        )

    def test_a_scroll_linked_layer_is_read_once_the_scroll_has_settled(self):
        self.assertEqual(self.layer_y(), 0)
        moved = pointer.wheel(self.page, "#scene", dy=300)
        self.assertTrue(moved.settled)
        self.assertEqual(self.page.evaluate("scrollY"), 300)
        self.assertEqual(self.layer_y(), 150)

    def test_an_animation_the_scroll_drives_does_not_hold_the_wait(self):
        self.assertTrue(pointer.wheel(self.page, "#scene", dy=300).settled)
        self.assertNotEqual(
            self.style("#progress", "transform"), "matrix(1, 0, 0, 0, 0, 0)"
        )

    def test_a_sideways_wheel_scrolls_the_strip(self):
        pointer.wheel(self.page, "#strip", dx=200)
        self.assertEqual(
            self.page.eval_on_selector("#strip", "el => el.scrollLeft"), 200
        )
        self.assertEqual(self.page.evaluate("scrollY"), 0)

    def test_a_scroll_eased_by_script_is_waited_for(self):
        self.assertTrue(pointer.wheel(self.page, "#glide", dx=200).settled)
        self.assertEqual(
            self.page.eval_on_selector("#glide", "el => el.scrollLeft"), 200
        )

    def test_a_wheel_with_no_target_scrolls_the_page_from_where_it_stands(self):
        self.page.evaluate("scrollTo(0, 100)")
        pointer.settle(self.page)
        pointer.wheel(self.page, dy=300)
        self.assertEqual(self.page.evaluate("scrollY"), 400)

    def test_refuses_a_wheel_that_does_not_turn(self):
        with self.assertRaisesRegex(ValueError, "needs a dx or a dy"):
            pointer.wheel(self.page, "#scene")


class Refusals(OnThePage):
    def test_refuses_a_covered_target_naming_the_cover(self):
        with self.assertRaisesRegex(
            pointer.PointerError, r"#covered is covered at .* by div#veil"
        ) as caught:
            pointer.press(self.page, "#covered")
        self.assertEqual(
            (caught.exception.target, caught.exception.cover), ("#covered", "div#veil")
        )

    def test_a_target_in_a_shadow_tree_is_not_covered_by_its_host(self):
        pointer.press(self.page, "#shadowed")
        self.assertEqual(
            self.page.evaluate(
                "() => getComputedStyle(host.shadowRoot.querySelector('button')).backgroundColor"
            ),
            "rgb(0, 0, 128)",
        )

    def test_refuses_a_target_the_page_lacks(self):
        with self.assertRaisesRegex(
            pointer.PointerError, "no element matches #nowhere"
        ):
            pointer.hover(self.page, "#nowhere")

    def test_refuses_a_target_with_no_box(self):
        with self.assertRaisesRegex(pointer.PointerError, "span#late-tip has no box"):
            pointer.hover(self.page, "#late-tip")

    def test_refuses_a_point_outside_the_box(self):
        with self.assertRaisesRegex(ValueError, "two fractions"):
            pointer.hover(self.page, "#tip-trigger", at=(1.5, 0.5))

    def test_takes_an_element_handle(self):
        pointer.hover(self.page, self.page.query_selector("#tip-trigger"))
        self.assertEqual(self.style("#tip", "opacity"), "1")


class Settle(OnThePage):
    def test_a_target_that_never_holds_still_is_pointed_at_once_the_cap_passes_unsettled(
        self,
    ):
        # #spinner turns forever, so its box never holds still; the cap is lowered so the wait is quick,
        # still past the settle's 800 ms quiet window, so a still target reads settled.
        self.addCleanup(setattr, pointer, "SETTLE_CAP_MS", pointer.SETTLE_CAP_MS)
        pointer.SETTLE_CAP_MS = 1500
        self.assertFalse(pointer.hover(self.page, "#spinner").settled)
        self.assertTrue(pointer.hover(self.page, "#count").settled)

    def test_a_page_still_moving_at_the_cap_reads_unsettled(self):
        self.page.evaluate(
            "() => setInterval(() => { document.body.dataset.tick = performance.now(); }, 100)"
        )
        self.assertFalse(pointer.hover(self.page, "#tip-trigger").settled)


class Watched(OnThePage):
    """WATCH_JS installed before the page's scripts (#462). The quiet window is set past the cap, so a settle
    reads True only where it ended early, on nothing queued. These cross the real clock, as what they pin is the
    page's own timers and loads, which a fake clock would replace: a 400 ms timer sits past the 100 ms floor and
    inside the 1.5 s cap."""

    def setUp(self):
        self.page = BROWSER[0].new_page()
        self.addCleanup(self.page.close)
        self.page.add_init_script(pointer.WATCH_JS)
        self.page.goto(PAGE)
        for name, value in (("QUIET_MS", 60000), ("SETTLE_CAP_MS", 1500)):
            self.addCleanup(setattr, pointer, name, getattr(pointer, name))
            setattr(pointer, name, value)

    def test_a_page_with_nothing_queued_settles_before_the_window_closes(self):
        self.assertTrue(pointer.settle(self.page))

    def test_a_timer_due_inside_the_window_is_waited_for(self):
        self.page.evaluate(
            "() => setTimeout(() => { document.body.dataset.late = 'yes'; }, 400)"
        )
        self.assertTrue(pointer.settle(self.page))
        self.assertEqual(self.page.evaluate("() => document.body.dataset.late"), "yes")

    def test_a_timer_due_after_the_window_closes_holds_nothing(self):
        self.page.evaluate("() => setTimeout(() => {}, 3600000)")
        self.assertTrue(pointer.settle(self.page))

    def test_a_cleared_timer_holds_nothing(self):
        self.page.evaluate("() => clearTimeout(setTimeout(() => {}, 400))")
        self.assertTrue(pointer.settle(self.page))

    def test_an_interval_due_inside_the_window_holds_it(self):
        self.page.evaluate("() => setInterval(() => {}, 400)")
        self.assertFalse(pointer.settle(self.page))

    def test_an_animation_frame_loop_holds_it(self):
        self.page.evaluate(
            "() => { const loop = () => requestAnimationFrame(loop); loop(); }"
        )
        self.assertFalse(pointer.settle(self.page))

    def test_an_idle_callback_holds_it(self):
        self.page.evaluate(
            "() => { const again = () => requestIdleCallback(again); again(); }"
        )
        self.assertFalse(pointer.settle(self.page))

    def held(self):
        """A page on a made-up http site, whose /held request is answered never: a file page cannot fetch."""
        held = []
        self.page.route(
            "http://vault.test/",
            lambda route: route.fulfill(content_type="text/html", body="<p>held</p>"),
        )
        self.page.route("http://vault.test/held", lambda route: held.append(route))
        self.page.goto("http://vault.test/")
        self.addCleanup(lambda: [route.abort() for route in held])
        return held

    def test_a_fetch_in_flight_holds_it(self):
        held = self.held()
        self.page.evaluate("() => { fetch('/held').catch(() => {}); }")
        self.assertFalse(pointer.settle(self.page))
        self.assertEqual(len(held), 1)

    def test_a_request_in_flight_holds_it(self):
        held = self.held()
        self.page.evaluate(
            "() => { const r = new XMLHttpRequest(); r.open('GET', '/held'); r.send(); }"
        )
        self.assertFalse(pointer.settle(self.page))
        self.assertEqual(len(held), 1)

    def test_changes_the_watch_cannot_see_still_hold_it_while_they_last(self):
        # A posted message is no timer, so only the quiet floor waits out its changes.
        self.page.evaluate(
            """() => {
              const { port1, port2 } = new MessageChannel(), end = performance.now() + 300;
              port1.onmessage = () => {
                document.body.dataset.tick = performance.now();
                if (performance.now() < end) port2.postMessage(0);
                else document.body.dataset.done = "yes";
              };
              port2.postMessage(0);
            }"""
        )
        self.assertTrue(pointer.settle(self.page))
        self.assertEqual(self.page.evaluate("() => document.body.dataset.done"), "yes")

    def test_a_timer_given_as_a_string_is_waited_for(self):
        self.page.evaluate(
            "() => setTimeout(\"document.body.dataset.late = 'yes'\", 400)"
        )
        self.assertTrue(pointer.settle(self.page))
        self.assertEqual(self.page.evaluate("() => document.body.dataset.late"), "yes")

    def test_a_timer_runs_with_the_window_as_this(self):
        self.page.evaluate(
            "() => setTimeout(function () { 'use strict'; document.body.dataset.self = String(this === window); }, 0)"
        )
        self.assertTrue(pointer.settle(self.page))
        self.assertEqual(self.page.evaluate("() => document.body.dataset.self"), "true")

    def test_a_scheduler_task_due_inside_the_window_is_waited_for(self):
        self.page.evaluate(
            "() => { scheduler.postTask(() => { document.body.dataset.late = 'yes'; }, { delay: 400 }); }"
        )
        self.assertTrue(pointer.settle(self.page))
        self.assertEqual(self.page.evaluate("() => document.body.dataset.late"), "yes")

    def test_a_fetch_whose_body_is_unread_holds_it(self):
        self.held()
        self.page.route(
            "http://vault.test/reply", lambda route: route.fulfill(body="ready")
        )
        self.page.evaluate("() => { window.got = fetch('/reply'); }")
        self.assertFalse(pointer.settle(self.page))

    def test_a_fetch_whose_body_is_read_holds_nothing(self):
        self.held()
        self.page.route(
            "http://vault.test/reply", lambda route: route.fulfill(body="ready")
        )
        self.page.evaluate(
            "() => { fetch('/reply').then((r) => r.text()).then((t) => { document.body.dataset.got = t; }); }"
        )
        self.assertTrue(pointer.settle(self.page))
        self.assertEqual(self.page.evaluate("() => document.body.dataset.got"), "ready")

    def test_an_image_still_loading_holds_it(self):
        self.held()
        self.page.evaluate(
            "() => { const i = new Image(); i.src = '/held'; document.body.append(i); }"
        )
        self.assertFalse(pointer.settle(self.page))

    def test_a_font_still_loading_holds_it(self):
        self.held()
        self.page.evaluate(
            "() => { const f = new FontFace('Held', 'url(/held)'); document.fonts.add(f); f.load().catch(() => {}); }"
        )
        self.assertFalse(pointer.settle(self.page))

    def test_a_request_whose_send_throws_holds_nothing(self):
        self.page.evaluate("() => { try { new XMLHttpRequest().send(); } catch {} }")
        self.assertTrue(pointer.settle(self.page))

    def test_a_tooltip_shown_after_a_delay_is_still_waited_for(self):
        pointer.hover(self.page, "#late-trigger")
        self.assertTrue(self.page.is_visible("#late-tip"))

    def test_a_faded_tooltip_is_still_read_faded_in(self):
        pointer.hover(self.page, "#tip-trigger")
        self.assertEqual(self.style("#tip", "opacity"), "1")


if __name__ == "__main__":
    child.main()
