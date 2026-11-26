import os
import re
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402

SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "check-logo.py"
)
NAVY, RED, CREAM = (20, 40, 120), (220, 60, 40), (245, 240, 230)
BOX = (300, 140, 200, 120)
TIMEOUT_S = 180  # guess, #501


def run(*args):
    out = child.run([sys.executable, SCRIPT, *args], timeout=TIMEOUT_S)
    return out.returncode, out.stdout, out.stderr


def logo(recolour=0, keyline=False, ground=None):
    image = Image.new("RGBA", (200, 120), ground or (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    if keyline:
        draw.rounded_rectangle((6, 26, 114, 94), 6, fill=(255, 255, 255, 255))
        draw.ellipse((116, 16, 194, 104), fill=(255, 255, 255, 255))
    draw.rectangle((12, 32, 108, 88), fill=(*NAVY[:2], NAVY[2] + recolour, 255))
    draw.ellipse((122, 22, 188, 98), fill=(*RED[:2], RED[2] + recolour, 255))
    return image


def svg(recolour=0):
    return (
        "<svg xmlns='http://www.w3.org/2000/svg' width='200' height='120' viewBox='0 0 200 120'>"
        f"<rect x='12' y='32' width='96' height='56' fill='rgb(20,40,{120 + recolour})'/>"
        f"<circle cx='155' cy='60' r='33' fill='rgb(220,60,{40 + recolour})'/></svg>"
    )


class Fixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def path(self, name):
        return os.path.join(self.tmp.name, name)

    def save(self, name, image):
        image.save(self.path(name))
        return self.path(name)

    def artboard(self, placed, ground=CREAM, size=None, box=BOX):
        board = (
            ground.copy()
            if isinstance(ground, Image.Image)
            else Image.new("RGB", (800, 400), ground)
        )
        if size:
            placed = placed.resize(size, Image.LANCZOS)
        board.paste(placed, box[:2], placed)
        return self.save("board.png", board)


class OnAnArtboard(Fixtures):
    def test_an_exact_placement_passes_both(self):
        code, out, err = run(
            "--logo",
            self.save("logo.png", logo()),
            self.artboard(logo()),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 0, out + err)
        self.assertRegex(
            out, r"unchanged: PASS — \d+ pixels inside the 4 px edge band match"
        )
        self.assertIn("ground: PASS", out)
        self.assertRegex(out, r"#142878 .*reaches [\d.]+:1 at least, against #f5f0e6")

    def test_a_placement_resampled_by_another_filter_passes_inside_the_band(self):
        small = logo().resize((100, 60), Image.BILINEAR)
        board = self.artboard(small, box=(300, 140, 100, 60))
        code, out, err = run(
            "--logo", self.save("logo.png", logo()), board, "--box", "300,140,100,60"
        )
        self.assertEqual(code, 0, out + err)
        self.assertIn("edge band 4 px", out)

    def test_a_recolour_under_2_de00_fails_330(self):
        code, out, _ = run(
            "--logo",
            self.save("logo.png", logo()),
            self.artboard(logo(recolour=6)),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"unchanged: FAIL — \d+ of \d+ pixels differ")
        de = float(re.search(r"ΔE00 ([\d.]+)", out).group(1))
        self.assertTrue(1.0 <= de <= 1.42, out)
        self.assertIn("place the logo file unchanged", out)

    def test_a_one_step_rounding_passes(self):
        code, out, _ = run(
            "--logo",
            self.save("logo.png", logo()),
            self.artboard(logo(recolour=1)),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 0, out)

    def test_a_one_step_shift_on_every_channel_of_a_near_black_fails_at_2_de00(self):
        dark = Image.new("RGBA", (200, 120), (0, 0, 0, 0))
        ImageDraw.Draw(dark).rectangle((12, 32, 188, 88), fill=(25, 25, 25, 255))
        moved = dark.copy()
        ImageDraw.Draw(moved).rectangle((12, 32, 188, 88), fill=(26, 24, 26, 255))
        code, out, _ = run(
            "--logo",
            self.save("dark.png", dark),
            self.artboard(moved),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 1, out)
        self.assertIn("#1a181a where the file has #191919, ΔE00 2.34", out)

    def test_a_logo_on_a_ground_under_3_to_1_fails_naming_the_colour(self):
        code, out, _ = run(
            "--logo",
            self.save("logo.png", logo()),
            self.artboard(logo(), ground=(128, 128, 128)),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 1, out)
        self.assertIn("unchanged: PASS", out)
        self.assertIn("ground: FAIL", out)
        self.assertRegex(
            out,
            r"#dc3c28 \(\d+% of the logo's edge\) reaches 1\.\d\d:1 against #808080 at \(\d+,\d+\); 100% of the ground is under 3:1",
        )
        self.assertRegex(out, r"#142878 .*reaches 3\.\d\d:1 at least")
        self.assertIn("take another version of the logo, or another ground", out)

    def test_a_ground_failing_only_in_the_ring_outside_the_box_fails(self):
        board = Image.new("RGB", (800, 400), CREAM)
        ImageDraw.Draw(board).rectangle((292, 100, 298, 300), fill=(128, 128, 128))
        code, out, _ = run(
            "--logo",
            self.save("logo.png", logo()),
            self.artboard(logo(), ground=board),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"#dc3c28 .* against #808080 at \(29\d,\d+\)")

    def test_a_gradient_ground_fails_where_it_falls_under_3_to_1(self):
        board = Image.new("RGB", (800, 400))
        board.putdata(
            [
                (v, v, v)
                for _ in range(400)
                for v in [255 - x * 140 // 799 for x in range(800)]
            ]
        )
        code, out, _ = run(
            "--logo",
            self.save("logo.png", logo()),
            self.artboard(logo(), ground=board),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"#dc3c28 .* under 3:1")

    def test_a_keyline_version_passes_on_its_keyline(self):
        dark = (32, 32, 32)
        plain = run(
            "--logo",
            self.save("logo.png", logo()),
            self.artboard(logo(), ground=dark),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(plain[0], 1, plain[1])
        self.assertRegex(plain[1], r"#142878 .* against #202020 at")
        keyed = logo(keyline=True)
        code, out, err = run(
            "--logo",
            self.save("keyline.png", keyed),
            self.artboard(keyed, ground=dark),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 0, out + err)
        self.assertRegex(
            out,
            r"ground: PASS — #ffffff \(100% of the logo's edge\) reaches [\d.]+:1 at least, against #202020",
        )

    def test_a_supplied_file_with_an_opaque_ground_is_refused_naming_why(self):
        opaque = logo(ground=(255, 255, 255, 255))
        code, out, err = run(
            "--logo",
            self.save("opaque.png", opaque),
            self.artboard(opaque),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 2, out + err)
        self.assertEqual(out, "")
        self.assertIn(
            "opaque.png has no transparent pixel, so its own ground would be compared as logo",
            err,
        )
        rgb = self.save("rgb.jpg", opaque.convert("RGB"))
        code, _, err = run(
            "--logo", rgb, self.artboard(logo()), "--box", "300,140,200,120"
        )
        self.assertEqual(code, 2)
        self.assertIn("rgb.jpg has no transparent pixel", err)
        self.assertIn("supply the version with a transparent ground", err)

    def test_a_logo_too_small_to_hold_a_pixel_past_the_band_is_not_judged(self):
        tiny = logo().resize((8, 5), Image.LANCZOS)
        code, out, _ = run(
            "--logo",
            self.save("logo.png", logo()),
            self.artboard(tiny, box=(300, 140, 8, 5)),
            "--box",
            "300,140,8,5",
        )
        self.assertEqual(code, 6, out)
        self.assertRegex(
            out, r"unchanged: NOT JUDGED — no logo pixel lies \d+ px inside its edges"
        )
        self.assertIn("check it by eye at 4× zoom", out)

    def test_a_not_judged_check_never_hides_a_fault(self):
        tiny = logo().resize((8, 5), Image.LANCZOS)
        board = self.artboard(tiny, ground=(128, 128, 128), box=(300, 140, 8, 5))
        code, out, _ = run(
            "--logo", self.save("logo.png", logo()), board, "--box", "300,140,8,5"
        )
        self.assertEqual(code, 1, out)
        self.assertIn("unchanged: NOT JUDGED", out)
        self.assertIn("ground: FAIL", out)

    def test_out_marks_the_faults_in_red(self):
        out_dir = self.path("out")
        code, out, _ = run(
            "--logo",
            self.save("logo.png", logo()),
            self.artboard(logo(recolour=6)),
            "--box",
            "300,140,200,120",
            "--out",
            out_dir,
        )
        self.assertEqual(code, 1, out)
        self.assertEqual(
            sorted(os.listdir(out_dir)), ["expected.png", "ground.png", "unchanged.png"]
        )
        with Image.open(os.path.join(out_dir, "unchanged.png")) as marked:
            self.assertEqual(marked.getpixel((66, 66)), (255, 0, 0))
        with Image.open(os.path.join(out_dir, "ground.png")) as marked:
            self.assertEqual(marked.getpixel((66, 66))[:3], (20, 40, 126))

    def test_bad_usage_exits_2_naming_the_argument(self):
        board, mark = self.artboard(logo()), self.save("logo.png", logo())
        jpeg = self.save("board.jpg", Image.open(board).convert("RGB"))
        for args, says in (
            (
                ("--logo", mark, board, "--box", "700,140,200,120"),
                "--box 700,140,200,120 runs past",
            ),
            (
                ("--logo", mark, board, "--box", "300,140,0,120"),
                "--box wants X,Y,W,H in whole pixels, W and H above 0",
            ),
            (("--logo", mark, board, "--box", "300,140"), "--box wants X,Y,W,H"),
            (
                ("--logo", mark, self.path("absent.png"), "--box", "300,140,200,120"),
                "no such file: ",
            ),
            (
                ("--logo", self.path("absent.png"), board, "--box", "300,140,200,120"),
                "cannot read ",
            ),
            (("--logo", mark, board), "one of the arguments --at --box is required"),
            (
                ("--logo", mark, jpeg, "--box", "300,140,200,120"),
                "is a JPEG, whose compression changes the logo's pixels: give a lossless export",
            ),
        ):
            with self.subTest(args=args[2:]):
                code, out, err = run(*args)
                self.assertEqual(code, 2, out + err)
                self.assertEqual(out, "")
                self.assertIn(says, err)

    def test_a_thin_accent_under_3_to_1_fails_though_it_is_under_the_blend_share(self):
        mark = logo()
        ImageDraw.Draw(mark).ellipse((58, 30, 61, 33), fill=(240, 224, 96, 255))
        code, out, _ = run(
            "--logo",
            self.save("accent.png", mark),
            self.artboard(mark),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 1, out)
        self.assertRegex(
            out, r"#f0e060 \(1% of the logo's edge\) reaches 1\.\d\d:1 against #f5f0e6"
        )

    def test_a_thin_colour_past_the_end_of_a_mix_of_two_logo_colours_is_judged(self):
        mark = Image.new("RGBA", (200, 120), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mark)
        draw.rectangle((10, 20, 95, 100), fill=(60, 60, 60, 255))
        draw.rectangle((105, 20, 190, 100), fill=(110, 110, 110, 255))
        draw.rectangle((140, 20, 145, 21), fill=(170, 170, 170, 255))
        code, out, _ = run(
            "--logo",
            self.save("greys.png", mark),
            self.artboard(mark, ground=(255, 255, 255)),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 1, out)
        self.assertRegex(
            out, r"#aaaaaa \(1% of the logo's edge\) reaches 2\.32:1 against #ffffff"
        )

    def test_a_seam_between_two_colours_inside_the_logo_is_banded(self):
        mark = Image.new("RGBA", (200, 120), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mark)
        draw.rectangle((10, 10, 99, 109), fill=(*NAVY, 255))
        draw.rectangle((100, 10, 189, 109), fill=(*RED, 255))
        small = mark.resize((150, 90), Image.BILINEAR)
        board = self.artboard(small, box=(300, 140, 150, 90))
        code, out, err = run(
            "--logo", self.save("halves.png", mark), board, "--box", "300,140,150,90"
        )
        self.assertEqual(code, 0, out + err)

    def test_a_resampled_keyline_version_passes_with_its_colour_edges_banded(self):
        keyed = logo(keyline=True)
        small = keyed.resize((100, 60), Image.BILINEAR)
        board = self.artboard(small, ground=(32, 32, 32), box=(300, 140, 100, 60))
        code, out, err = run(
            "--logo", self.save("keyline.png", keyed), board, "--box", "300,140,100,60"
        )
        self.assertEqual(code, 0, out + err)

    def test_a_blend_where_two_logo_colours_meet_the_outline_is_not_judged_as_a_colour(
        self,
    ):
        big = Image.new("RGBA", (800, 480), (0, 0, 0, 0))
        draw = ImageDraw.Draw(big)
        draw.rectangle((40, 80, 401, 400), fill=(0, 0, 0, 255))
        draw.rectangle((402, 80, 760, 400), fill=(255, 255, 255, 255))
        mark = big.resize((200, 120), Image.LANCZOS)
        code, out, err = run(
            "--logo",
            self.save("halves.png", mark),
            self.artboard(mark, ground=(119, 119, 119)),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 0, out + err)
        self.assertRegex(out, r"#000000 .*at least")
        self.assertRegex(out, r"#ffffff .*at least")

    def test_shades_of_one_colour_are_judged_as_that_colour(self):
        noisy = logo()
        noisy.putdata(
            [
                (r + i % 4, g + i // 4 % 4, b + i // 16 % 4, a)
                if (r, g, b) == NAVY
                else (r, g, b, a)
                for i, (r, g, b, a) in enumerate(noisy.get_flattened_data())
            ]
        )
        code, out, _ = run(
            "--logo",
            self.save("noisy.png", noisy),
            self.artboard(noisy, ground=(32, 32, 32)),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 1, out)
        self.assertRegex(
            out,
            r"#1[4-7]2[89ab]7[89ab] \(\d\d% of the logo's edge\) reaches 1\.\d\d:1 against #202020",
        )

    def test_a_transparent_artboard_is_refused(self):
        board = Image.new("RGBA", (800, 400), (0, 0, 0, 0))
        board.paste(logo(), BOX[:2], logo())
        code, _, err = run(
            "--logo",
            self.save("logo.png", logo()),
            self.save("clear.png", board),
            "--box",
            "300,140,200,120",
        )
        self.assertEqual(code, 2)
        self.assertIn("has transparent pixels: give its flattened export", err)


class OnAPage(Fixtures):
    def page(self, src, ground="#f5f0e6", style="", extra=""):
        html = (
            f"<!doctype html><html><body style='margin:0;background:{ground}'>"
            f"<img id='logo' src='{src}' style='position:absolute;left:300px;top:140px;width:200px;height:120px;{style}'>"
            f"{extra}</body></html>"
        )
        path = self.path("page.html")
        with open(path, "w", encoding="utf8") as f:
            f.write(html)
        return path

    def svg_file(self, name, recolour=0):
        path = self.path(name)
        with open(path, "w", encoding="utf8") as f:
            f.write(svg(recolour))
        return path

    def test_an_exact_raster_placement_passes_at_2x(self):
        self.save("logo.png", logo())
        code, out, err = run(
            "--logo", self.path("logo.png"), self.page("logo.png"), "--at", "#logo"
        )
        self.assertEqual(code, 0, out + err)
        self.assertIn("in 400x240 px at (600,280) (--at #logo), edge band 7 px", out)

    def test_a_recoloured_raster_fails(self):
        self.save("logo.png", logo())
        self.save("served.png", logo(recolour=6))
        code, out, _ = run(
            "--logo",
            self.path("logo.png"),
            self.page("served.png"),
            "--at",
            "#logo",
            "--scale",
            "1",
        )
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"unchanged: FAIL .*ΔE00 1\.\d\d")

    def test_an_exact_svg_placement_passes(self):
        mark = self.svg_file("logo.svg")
        code, out, err = run("--logo", mark, self.page("logo.svg"), "--at", "#logo")
        self.assertEqual(code, 0, out + err)
        self.assertIn("edge band 2 px", out)

    def test_a_recoloured_svg_fails(self):
        mark = self.svg_file("logo.svg")
        self.svg_file("served.svg", recolour=6)
        code, out, _ = run("--logo", mark, self.page("served.svg"), "--at", "#logo")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"unchanged: FAIL .*ΔE00 1\.\d\d")
        self.assertIn("place the logo file unchanged", out)

    def test_a_page_ground_under_3_to_1_fails(self):
        mark = self.svg_file("logo.svg")
        code, out, _ = run(
            "--logo", mark, self.page("logo.svg", ground="#808080"), "--at", "#logo"
        )
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"#dc3c28 .* against #808080")
        self.assertIn("take another version of the logo, or another ground", out)

    def test_an_svg_with_an_opaque_ground_is_refused(self):
        path = self.path("opaque.svg")
        with open(path, "w", encoding="utf8") as f:
            f.write(
                svg().replace(
                    "<rect", "<rect width='100%' height='100%' fill='#fff'/><rect", 1
                )
            )
        code, out, err = run("--logo", path, self.page("opaque.svg"), "--at", "#logo")
        self.assertEqual(code, 2, out + err)
        self.assertIn("has no transparent pixel", err)
        self.assertIn("supply the version with a transparent ground", err)

    def test_an_svg_stroke_thinner_than_a_placed_pixel_is_judged_at_the_file_resolution(
        self,
    ):
        mark = self.path("stroke.svg")
        with open(mark, "w", encoding="utf8") as f:
            f.write(
                "<svg xmlns='http://www.w3.org/2000/svg' width='200' height='120' viewBox='0 0 200 120'>"
                "<rect x='12' y='32' width='96' height='56' fill='rgb(20,40,120)'/>"
                "<rect x='150.25' y='20' width='0.5' height='80' fill='rgb(240,224,96)'/></svg>"
            )
        code, out, err = run(
            "--logo", mark, self.page("stroke.svg"), "--at", "#logo", "--scale", "1"
        )
        self.assertEqual(code, 1, out + err)
        self.assertRegex(
            out, r"#f0e060 \(\d+% of the logo's edge\) reaches 1\.19:1 against #f5f0e6"
        )

    def test_an_svg_placed_off_the_pixel_grid_passes_inside_its_band(self):
        mark = self.svg_file("logo.svg")
        code, out, err = run(
            "--logo",
            mark,
            self.page("logo.svg", style="transform:translate(0.3px,0.3px)"),
            "--at",
            "#logo",
        )
        self.assertEqual(code, 0, out + err)

    def test_a_selector_matching_two_elements_cannot_be_judged(self):
        self.save("logo.png", logo())
        code, out, _ = run(
            "--logo",
            self.path("logo.png"),
            self.page("logo.png", extra="<img src='logo.png'>"),
            "--at",
            "img",
        )
        self.assertEqual(code, 6, out)
        self.assertIn("--at img matches 2 elements, not one", out)
        self.assertIn("Compare it with the file by eye.", out)

    def test_a_logo_under_an_endless_animation_cannot_be_judged(self):
        self.save("logo.png", logo())
        page = self.page(
            "logo.png",
            style="animation:pulse 1s infinite",
            extra="<style>@keyframes pulse{to{opacity:.5}}</style>",
        )
        code, out, _ = run("--logo", self.path("logo.png"), page, "--at", "#logo")
        self.assertEqual(code, 6, out)
        self.assertIn(
            "1 animation(s) never end, so the logo may be read mid-motion", out
        )

    def test_a_logo_drawn_partly_off_the_page_cannot_be_judged(self):
        self.save("logo.png", logo())
        code, out, _ = run(
            "--logo",
            self.path("logo.png"),
            self.page("logo.png", style="left:-50px"),
            "--at",
            "#logo",
        )
        self.assertEqual(code, 6, out)
        self.assertIn("--at #logo is drawn partly off the page", out)

    def test_a_selector_matching_no_element_cannot_be_judged(self):
        self.save("logo.png", logo())
        code, out, _ = run(
            "--logo", self.path("logo.png"), self.page("logo.png"), "--at", "#absent"
        )
        self.assertEqual(code, 6, out)
        self.assertIn("--at #absent matches 0 elements, not one", out)
        self.assertIn("Compare it with the file by eye.", out)


if __name__ == "__main__":
    child.main()
